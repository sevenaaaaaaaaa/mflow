#!/usr/bin/env python3
"""MFlow Console — interactive workbench for the Lovart content workflow.

One stdlib-only HTTP service. Serves the console UI and a small JSON API that
wraps the existing SSOT tools (pipeline_state.py / router.py / quality hooks /
daily pipeline). Nothing here bypasses the iron rules: publishing actions are
display-only; state transitions still go through pipeline_state.py.

Run (systemd mflow-console.service):
    /var/www/mflow/.venv/bin/python "1-4 Dev/console/console.py"

Auth: password from env MFLOW_CONSOLE_PASSWORD (see run/env.sh).
"""
import importlib.util
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import time
from http import cookies as http_cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
CONSOLE_DIR = Path(__file__).resolve().parent
STATE_FILE = PROJECT / "1-3 GenFlow" / ".pipeline" / "pipeline-state.json"
EVENTS_FILE = PROJECT / "1-3 GenFlow" / ".pipeline" / "events.jsonl"
DAILY_LOG = PROJECT / "run" / "logs" / "daily.out.log"
DAILY_PID = PROJECT / "run" / "logs" / "daily.pid"
PORT = int(os.environ.get("MFLOW_CONSOLE_PORT", "8088"))
PASSWORD = os.environ.get("MFLOW_CONSOLE_PASSWORD", "")

PS_PATH = PROJECT / "1-1 Harness" / "Skills" / "06-orchestrate" / "lovart-pipeline-state" / "pipeline_state.py"
ROUTER_PATH = PROJECT / "1-1 Harness" / "Skills" / "06-orchestrate" / "lovart-router" / "router.py"
HOOKS = ["pre-write-check.sh", "post-write-check.sh", "pre-import-check.sh", "post-generation-check.sh"]

SESSIONS = set()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PS = load_module("mflow_pipeline_state", PS_PATH)
try:
    ROUTER = load_module("mflow_router", ROUTER_PATH)
    ROUTER_DECISIONS = ROUTER.DECISIONS
except Exception as e:  # router import must never kill the console
    ROUTER = None
    ROUTER_DECISIONS = []
    print(f"[console] router import failed: {e}", file=sys.stderr)


def run_tool(args, timeout=60):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT))
        return {"rc": r.returncode, "out": (r.stdout + r.stderr)[-4000:]}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "out": "timeout"}


def pipeline_call(*args):
    return run_tool([sys.executable, str(PS_PATH), *args])


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return default


def api_state():
    state = read_json(STATE_FILE, {})
    items = sorted(state.get("items", {}).values(),
                   key=lambda i: i.get("updated_at", ""), reverse=True)
    events = []
    if EVENTS_FILE.exists():
        lines = EVENTS_FILE.read_text().strip().split("\n")[-40:]
        events = [json.loads(l) for l in lines if l.strip()]
    decisions = [
        {"stage": d.get("stage"), "scenario": d.get("scenario"),
         "profile": d.get("profile"), "action": d.get("action")}
        for d in ROUTER_DECISIONS
    ]
    timers = run_tool(["systemctl", "list-timers", "mflow-*", "--no-pager"], timeout=15)
    return {
        "items": items,
        "legal_transitions": {k: sorted(v) for k, v in PS.TRANSITIONS.items()},
        "phases": PS.PHASES,
        "events": events,
        "decisions": decisions,
        "timers": timers["out"][-2000:],
        "daily": daily_status(),
        "sentinel": latest_file("1-2 Insight/Lovart ORM", "Lovart-Sentinel-*-daily.md"),
        "fmcheck": latest_file("1-1 Harness/11-knowledge/audit/reports", "fm-check-*.txt"),
    }


def latest_file(rel, pattern):
    base = PROJECT / rel
    if not base.exists():
        return None
    files = sorted(base.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return str(files[0].relative_to(PROJECT)) if files else None


def daily_status():
    running = False
    if DAILY_PID.exists():
        pid = DAILY_PID.read_text().strip()
        running = bool(pid) and Path(f"/proc/{pid}").exists()
    tail = ""
    if DAILY_LOG.exists():
        tail = "\n".join(DAILY_LOG.read_text().strip().split("\n")[-30:])
    return {"running": running, "tail": tail}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _authed(self):
        if not PASSWORD:
            return True
        raw = self.headers.get("Cookie", "")
        try:
            c = http_cookies.SimpleCookie(raw)
            return c["mflow_session"].value in SESSIONS
        except (KeyError, CookieError if False else Exception):
            return False

    def _body(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return {}

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            if not self._authed():
                return self._send(200, (CONSOLE_DIR / "login.html").read_bytes(), "text/html; charset=utf-8")
            return self._send(200, (CONSOLE_DIR / "console.html").read_bytes(), "text/html; charset=utf-8")
        if not self._authed():
            return self._send(401, {"error": "unauthorized"})
        if self.path == "/api/state":
            return self._send(200, api_state())
        if self.path == "/api/daily/log":
            return self._send(200, daily_status())
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/api/login":
            body = self._body()
            if secrets.compare_digest(str(body.get("password", "")), PASSWORD):
                sid = secrets.token_urlsafe(32)
                SESSIONS.add(sid)
                self.send_response(200)
                self.send_header("Set-Cookie", f"mflow_session={sid}; HttpOnly; Path=/; SameSite=Lax")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            else:
                self._send(403, {"ok": False, "error": "wrong password"})
            return
        if not self._authed():
            return self._send(401, {"error": "unauthorized"})
        body = self._body()
        if self.path == "/api/logout":
            try:
                c = http_cookies.SimpleCookie(self.headers.get("Cookie", ""))
                SESSIONS.discard(c["mflow_session"].value)
            except Exception:
                pass
            return self._send(200, {"ok": True})
        if self.path == "/api/item/upsert":
            item_id = str(body.get("id", "")).strip()
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}", item_id):
                return self._send(400, {"error": "id 必须是小写字母/数字/连字符（2-79 位）"})
            args = ["upsert", "--id", item_id,
                    "--category", str(body.get("category", "blog")),
                    "--target-type", str(body.get("target_type", "blog"))]
            r = pipeline_call(*args)
            return self._send(200 if r["rc"] == 0 else 400, r)
        if self.path == "/api/item/advance":
            r = pipeline_call("advance", "--id", str(body.get("id", "")),
                              "--to", str(body.get("to", "")),
                              "--reason", str(body.get("reason", "console"))[:200])
            return self._send(200 if r["rc"] == 0 else 400, r)
        if self.path == "/api/router/decide":
            if ROUTER is None:
                return self._send(500, {"error": "router unavailable"})
            try:
                d = ROUTER._match_decision(str(body.get("stage", "")), str(body.get("scenario", "default")))
                if not d:
                    return self._send(404, {"error": "无匹配决策（stage/scenario 不在矩阵中）"})
                return self._send(200, {"ok": True, "verdict": {
                    "stage": d.get("stage"), "scenario": d.get("scenario"),
                    "action": d.get("action"), "profile": d.get("profile"),
                    "skills": d.get("skills"), "reason": d.get("reason")}})
            except Exception as e:
                return self._send(400, {"error": str(e)[:300]})
        if self.path == "/api/hook/run":
            hook = str(body.get("hook", ""))
            if hook not in HOOKS:
                return self._send(400, {"error": "unknown hook"})
            f = Path(str(body.get("file", ""))).resolve()
            if not f.exists() or PROJECT not in f.parents:
                return self._send(400, {"error": "file 必须在项目目录内"})
            r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks" / hook), "--file", str(f)], timeout=120)
            return self._send(200, r)
        if self.path == "/api/daily/run":
            if daily_status()["running"]:
                return self._send(409, {"error": "每日管线已在运行中"})
            log = open(DAILY_LOG, "a")
            proc = subprocess.Popen(
                ["bash", str(PROJECT / "1-4 Dev/automation/run-daily-pipeline.sh")],
                stdout=log, stderr=subprocess.STDOUT, cwd=str(PROJECT))
            DAILY_PID.write_text(str(proc.pid))
            return self._send(200, {"ok": True, "pid": proc.pid})
        return self._send(404, {"error": "not found"})


def main():
    if not PASSWORD:
        print("[console] WARN: MFLOW_CONSOLE_PASSWORD 未设置，控制台无密码", file=sys.stderr)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[console] MFlow Console on :{PORT} (project={PROJECT})")
    server.serve_forever()


if __name__ == "__main__":
    main()
