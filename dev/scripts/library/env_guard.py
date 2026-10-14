#!/usr/bin/env python3
"""env_guard.py — development / production separation for external writes (stdlib only).

Environment:
  env() -> "production" | "development"
    1) MFLOW_ENV wins (generic APP_ENV is ignored on purpose): prod/production/live -> production; anything else -> development
    2) otherwise by platform: Linux (the server) -> production; macOS / others -> development

Opt-in for a deliberate live write from a development machine:
  MFLOW_ALLOW_LIVE_WRITES=1  or  pass `--live` on the command line
  (`--live` is removed from sys.argv when this module is imported, so argparse never sees it).

Strict mode (raise instead of dry-run): MFLOW_LIVE_WRITE_STRICT=1 or require_live_write(strict=True).

Two layers:
  * require_live_write(action) — explicit check for a code path that writes (returns True to proceed).
  * install() — in-process transport guard. Patches urllib (OpenerDirector.open), requests
    (Session.request) and smtplib (SMTP.sendmail). In development, requests that are classified as
    external production writes (see classify_write) are turned into a dry-run:
      - Sanity mutate      -> forced to Sanity's native dryRun (validated, nothing persisted)
      - everything else    -> not sent; a fake 200 response with {"skipped": "development"} is returned
    Reads (GET/HEAD and known read-only POST endpoints such as GROQ queries) are never touched.
    In production install() is a no-op.

CLI (for shell scripts):
  python3 env_guard.py env                # prints production|development
  python3 env_guard.py check "<action>"   # exit 0 = may write; exit 3 = skip (development dry-run)
"""
import functools
import inspect
import io
import json
import os
import sys
import urllib.parse

SKIPPED = "development"
EXIT_SKIPPED = 3

_TRUE = {"1", "true", "yes", "on", "y"}
_PROD = {"prod", "production", "live", "server"}

_CLI_LIVE = False
if "--live" in sys.argv[1:]:
    _CLI_LIVE = True
    sys.argv[:] = [sys.argv[0]] + [a for a in sys.argv[1:] if a != "--live"]


class LiveWriteBlocked(RuntimeError):
    """Raised in strict mode when a development run attempts an external write."""


# ---------------------------------------------------------------- environment

def env(environ=None, platform=None):
    environ = os.environ if environ is None else environ
    raw = (environ.get("MFLOW_ENV") or "").strip().lower()
    if raw:
        return "production" if raw in _PROD else "development"
    platform = sys.platform if platform is None else platform
    return "production" if platform.startswith("linux") else "development"


def is_production(environ=None, platform=None):
    return env(environ, platform) == "production"


def is_development(environ=None, platform=None):
    return env(environ, platform) == "development"


def live_writes_allowed(environ=None):
    environ = os.environ if environ is None else environ
    return _CLI_LIVE or (environ.get("MFLOW_ALLOW_LIVE_WRITES", "").strip().lower() in _TRUE)


def _strict_default():
    return os.environ.get("MFLOW_LIVE_WRITE_STRICT", "").strip().lower() in _TRUE


def _notice(action):
    print(f"[env_guard] 开发环境（{env()}）：已拦截对外写入「{action}」，按 dry-run/预览处理，未写入线上。"
          f" 确需从本机真实写入：加 --live 或设置 MFLOW_ALLOW_LIVE_WRITES=1；或到服务器上运行。",
          file=sys.stderr, flush=True)


def require_live_write(action, *, allow_flag=False, strict=None):
    """Return True if the caller may perform the external write `action`.

    production -> always True. development -> True only with an explicit opt-in
    (allow_flag / --live / MFLOW_ALLOW_LIVE_WRITES=1); otherwise prints a notice and returns False
    (or raises LiveWriteBlocked in strict mode)."""
    if is_production() or allow_flag or live_writes_allowed():
        return True
    if strict is None:
        strict = _strict_default()
    if strict:
        raise LiveWriteBlocked(f"开发环境禁止对外写入：{action}（加 --live 或 MFLOW_ALLOW_LIVE_WRITES=1 显式放行）")
    _notice(action)
    return False


def skipped_result(action, **extra):
    """Recognisable result for a write that was skipped in development."""
    d = {"ok": True, "skipped": SKIPPED, "dry_run": True, "env": env(), "action": action,
         "note": "开发环境未写入线上（dry-run）；--live 或 MFLOW_ALLOW_LIVE_WRITES=1 可放行"}
    d.update(extra)
    return d


def dry_run_in_development(action, param="dry_run"):
    """Decorator for functions with a dry-run switch (e.g. `dry_run=True`).

    In development without opt-in, a call that asks for a real write is downgraded to dry-run and the
    returned dict is tagged with {"skipped": "development"}. Production / opt-in: unchanged."""
    def deco(fn):
        sig = inspect.signature(fn)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            if bound.arguments.get(param) or require_live_write(action):
                return fn(*args, **kwargs)
            bound.arguments[param] = True
            out = fn(*bound.args, **bound.kwargs)
            if isinstance(out, dict):
                out.setdefault("skipped", SKIPPED)
                out["env"] = env()
            return out

        wrapper._mflow_guarded = True
        return wrapper
    return deco


# ---------------------------------------------------------------- classification

_READ_METHODS = {"GET", "HEAD", "OPTIONS"}
# Hosts that receive IM / notification messages (any non-GET is a send).
_IM_HOSTS = ("hooks.slack.com", "slack.com", "api.telegram.org", "qyapi.weixin.qq.com",
             "oapi.dingtalk.com", "discord.com", "discordapp.com")


def _extra_hosts():
    raw = os.environ.get("MFLOW_WRITE_GUARD_HOSTS", "")
    return [h.strip().lower() for h in raw.split(",") if h.strip()]


def classify_write(method, url):
    """Return a short label if (method, url) is an external production write, else None."""
    method = (method or "GET").upper()
    if method in _READ_METHODS:
        return None
    try:
        p = urllib.parse.urlsplit(url)
    except Exception:
        return None
    host = (p.hostname or "").lower()
    path = p.path or "/"
    if host in ("127.0.0.1", "localhost", "::1", ""):
        return None
    if host.endswith(".api.sanity.io") or host.endswith(".apicdn.sanity.io"):
        if "/data/query/" in path or path.rstrip("/").endswith("/query"):
            return None
        return "sanity-mutate" if "/data/mutate/" in path else "sanity-write"
    if "/wp-json/" in path or path.endswith("/xmlrpc.php") or path.endswith("/wp-login.php") \
            or "/wp-admin/" in path:
        return "wordpress"
    if host == "api.notion.com":
        if path.endswith("/query") or path.rstrip("/").endswith("/v1/search"):
            return None
        return "notion"
    if host in ("open.feishu.cn", "open.larksuite.com"):
        if "/auth/" in path or path.rstrip("/").endswith("/search"):
            return None
        return "feishu"
    if host == "api.cloudflare.com":
        return "cloudflare"
    if "indexnow" in host or "indexnow" in path.lower():
        return "indexnow"
    if host == "api.github.com":
        return "github"
    if any(host == h or host.endswith("." + h) for h in _IM_HOSTS):
        return "im"
    for h in _extra_hosts():
        if host == h or host.endswith("." + h):
            return "custom"
    return None


def _sanity_dry_url(url):
    p = urllib.parse.urlsplit(url)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if k != "dryRun"]
    q.append(("dryRun", "true"))
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, urllib.parse.urlencode(q), p.fragment))


def _sanity_dry_body(body):
    """Force {"dryRun": true} into a Sanity mutate JSON body; None if the body is not JSON."""
    if isinstance(body, (bytes, bytearray)):
        body = bytes(body).decode("utf-8", "replace")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            return None
    if not isinstance(body, dict):
        return None
    out = dict(body)
    out["dryRun"] = True
    return out


def _already_dry(body, url):
    """True if the caller itself asked Sanity for a dryRun (no notice needed)."""
    if "dryRun=true" in (urllib.parse.urlsplit(url).query or ""):
        return True
    try:
        if isinstance(body, (bytes, bytearray)):
            body = bytes(body).decode("utf-8", "replace")
        if isinstance(body, str):
            body = json.loads(body)
        return isinstance(body, dict) and body.get("dryRun") is True
    except Exception:
        return False


def _skip_payload(label, method, url):
    # code=0 keeps Feishu-style callers ("code != 0 means error") on the happy path
    return skipped_result(f"{label} {method} {url}", label=label, code=0)


# ---------------------------------------------------------------- fake responses

class _SkippedHTTPResponse(io.BytesIO):
    """Minimal stand-in for http.client.HTTPResponse returned by urlopen."""

    def __init__(self, url, payload):
        super().__init__(json.dumps(payload, ensure_ascii=False).encode())
        self.url = url
        self.status = self.code = 200
        self.reason = "OK (skipped: development)"
        self.headers = self.msg = {"Content-Type": "application/json", "X-MFlow-Skipped": SKIPPED}

    def getcode(self):
        return self.status

    def geturl(self):
        return self.url

    def info(self):
        return self.headers

    def getheader(self, name, default=None):
        return self.headers.get(name, default)


def _requests_skipped(url, payload, method):
    import requests  # only called when requests is in use
    r = requests.models.Response()
    r.status_code = 200
    r.url = url
    r.reason = "OK (skipped: development)"
    r._content = json.dumps(payload, ensure_ascii=False).encode()
    r.encoding = "utf-8"
    r.headers["Content-Type"] = "application/json"
    r.headers["X-MFlow-Skipped"] = SKIPPED
    r.request = requests.models.Request(method, url).prepare()
    return r


# ---------------------------------------------------------------- transport patches

_INSTALLED = False


def install(force=False):
    """Install the in-process transport guard (idempotent). No-op in production unless force."""
    global _INSTALLED
    if _INSTALLED or (is_production() and not force):
        return _INSTALLED
    _patch_urllib()
    _patch_requests()
    _patch_smtplib()
    _INSTALLED = True
    return True


def _guard_active():
    return is_development() and not live_writes_allowed()


def _t(timeout):
    # Keep urllib's own default timeout sentinel when the caller passed none.
    return () if timeout is None else (timeout,)


def _patch_urllib():
    import urllib.request as ur
    orig = ur.OpenerDirector.open
    if getattr(orig, "_mflow_guard", False):
        return

    def open(self, fullurl, data=None, timeout=None, *args, **kwargs):  # noqa: A001
        req = fullurl if isinstance(fullurl, ur.Request) else ur.Request(fullurl, data)
        if data is not None and isinstance(fullurl, ur.Request):
            req.data = data
            data = None
        if _guard_active():
            method = req.get_method()
            url = req.full_url
            label = classify_write(method, url)
            if label:
                if _strict_default():
                    raise LiveWriteBlocked(f"开发环境禁止对外写入：{label} {method} {url}")
                if label == "sanity-mutate":
                    body = _sanity_dry_body(req.data)
                    if body is not None:
                        if not _already_dry(req.data, url):
                            _notice(f"Sanity mutate → 已强制改为原生 dryRun（{url.split('?')[0]}）")
                        req.data = json.dumps(body).encode()
                        req.full_url = _sanity_dry_url(url)
                        req.remove_header("Content-length")
                        return orig(self, req, None, *_t(timeout), *args, **kwargs)
                _notice(f"{label} {method} {url}")
                return _SkippedHTTPResponse(url, _skip_payload(label, method, url))
        return orig(self, req, data, *_t(timeout), *args, **kwargs)

    open._mflow_guard = True
    ur.OpenerDirector.open = open


def _patch_requests():
    try:
        import requests
    except Exception:
        return
    orig = requests.Session.request
    if getattr(orig, "_mflow_guard", False):
        return

    def request(self, method, url, *args, **kwargs):
        if _guard_active():
            label = classify_write(str(method), str(url))
            if label:
                if _strict_default():
                    raise LiveWriteBlocked(f"开发环境禁止对外写入：{label} {method} {url}")
                if label == "sanity-mutate" and not args:
                    src = kwargs.get("json") if kwargs.get("json") is not None else kwargs.get("data")
                    body = _sanity_dry_body(src)
                    if body is not None:
                        if not _already_dry(src, str(url)):
                            _notice(f"Sanity mutate → 已强制改为原生 dryRun（{str(url).split('?')[0]}）")
                        kwargs.pop("data", None)
                        kwargs["json"] = body
                        return orig(self, method, _sanity_dry_url(str(url)), **kwargs)
                _notice(f"{label} {str(method).upper()} {url}")
                return _requests_skipped(str(url), _skip_payload(label, str(method).upper(), str(url)),
                                         str(method).upper())
        return orig(self, method, url, *args, **kwargs)

    request._mflow_guard = True
    requests.Session.request = request


def _patch_smtplib():
    import smtplib
    orig = smtplib.SMTP.sendmail
    if getattr(orig, "_mflow_guard", False):
        return

    def sendmail(self, from_addr, to_addrs, msg, *args, **kwargs):
        if _guard_active():
            if _strict_default():
                raise LiveWriteBlocked(f"开发环境禁止发送邮件：{to_addrs}")
            _notice(f"发送邮件 → {to_addrs}")
            return {}
        return orig(self, from_addr, to_addrs, msg, *args, **kwargs)

    sendmail._mflow_guard = True
    smtplib.SMTP.sendmail = sendmail


# ---------------------------------------------------------------- CLI

def _main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "env":
        print(env())
        return 0
    if argv[0] == "check":
        action = " ".join(argv[1:]) or "external write"
        try:
            return 0 if require_live_write(action) else EXIT_SKIPPED
        except LiveWriteBlocked as e:
            print(f"[env_guard] {e}", file=sys.stderr)
            return 2
    print(f"unknown command: {argv[0]}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
