"""
web_router — Given a URL, automatically pick the right tool
(Firecrawl / Tavily / Hermes curl / Playwright MCP) to handle it.

This is the entry point for any "fetch web content" task in the Lovart pipeline.
The single rule: try cheap first (Hermes curl), escalate only on failure.

Usage:
    from web_router import fetch_url
    result = fetch_url("https://www.lovart.ai/changelog")
    # result is {tool, ok, markdown, error, ...}

    fetch_url("https://example.com", schema={...})   # if Firecrawl is used,
                                                      # schema applies
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

# ---------- detect Playwright Python (vendored at ~/Library/Caches/lovart-tools-venv) ----------
PW_VENV_PY = Path.home() / "Library" / "Caches" / "lovart-tools-venv" / "bin" / "python"
if PW_VENV_PY.exists():
    # When running under system python (no playwright in site-packages),
    # inject PW_VENV_PY's site-packages into path so we can import playwright.
    pw_site = PW_VENV_PY.parent.parent / "lib" / "python3.13" / "site-packages"
    if pw_site.exists() and str(pw_site) not in sys.path:
        sys.path.insert(0, str(pw_site))

# ---------- blacklist: Firecrawl rejects these, try Hermes curl / Playwright ----------
FC_BLACKLIST = (
    "linkedin.com",
    "instagram.com",
    "facebook.com",
    "messenger.com",
    "whatsapp.com",
)

# ---------- heuristics: SPA sites — Hermes curl gets nothing useful ----------
SPA_HINTS = (
    "notion.so",
    "vercel.com",
    "framer.com",
    "webflow.io",
    "react.app",
)

# ---------- common Chrome UA for Hermes curl attempts ----------
CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# ---------- visible-text extraction (rough but stdlib only) ----------
_TAG_RE = re.compile(r"<script[^>]*>.*?</script>", re.S | re.I)
_STYLE_RE = re.compile(r"<style[^>]*>.*?</style>", re.S | re.I)
_TAG_STRIP_RE = re.compile(r"<[^>]+>")


def _visible_text(html: str) -> str:
    body = _TAG_RE.sub(" ", html)
    body = _STYLE_RE.sub(" ", body)
    body = _TAG_STRIP_RE.sub(" ", body)
    return re.sub(r"\s+", " ", body).strip()


@dataclass
class FetchResult:
    tool: str
    ok: bool
    url: str
    markdown: str = ""
    title: str = ""
    error: str = ""
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        out = {
            "tool": self.tool,
            "ok": self.ok,
            "url": self.url,
            "markdown": self.markdown,
            "title": self.title,
            "error": self.error,
        }
        out.update(self.extra or {})
        return out


# ---------- tool adapters ----------

def _hermes_curl(url: str, timeout: int = 20) -> FetchResult:
    req = urllib.request.Request(url, headers={"User-Agent": CHROME_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
            title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
            title = title_m.group(1).strip()[:200] if title_m else ""
            visible = _visible_text(body)
            # Heuristic: page is useful if visible text > 400 chars
            ok = len(visible) >= 400
            return FetchResult(
                tool="hermes_curl",
                ok=ok,
                url=url,
                markdown=visible,
                title=title,
                error="" if ok else f"only {len(visible)} chars visible (likely SPA/login wall)",
                extra={"http_status": r.status, "visible_chars": len(visible)},
            )
    except urllib.error.HTTPError as e:
        return FetchResult(
            tool="hermes_curl",
            ok=False,
            url=url,
            error=f"HTTP {e.code}",
            extra={"http_status": e.code},
        )
    except Exception as e:
        return FetchResult(tool="hermes_curl", ok=False, url=url, error=f"{type(e).__name__}: {e}")


def _firecrawl_scrape(url: str, schema: dict | None = None, prompt: str | None = None,
                       timeout: int = 120) -> FetchResult:
    """Primary tool for SPA sites + structured extraction."""
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        return FetchResult(tool="firecrawl", ok=False, url=url,
                           error="FIRECRAWL_API_KEY not set")
    payload: dict[str, Any] = {"url": url, "onlyMainContent": True}
    if schema:
        fmt = {"type": "json", "schema": schema}
        if prompt:
            fmt["prompt"] = prompt
        payload["formats"] = [fmt, "markdown"]
    else:
        payload["formats"] = ["markdown"]
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v2/scrape",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "lovart-web-router/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        if not d.get("success"):
            return FetchResult(tool="firecrawl", ok=False, url=url,
                               error=d.get("error", "unknown"), extra={"raw": d})
        data = d.get("data") or {}
        meta = data.get("metadata") or {}
        return FetchResult(
            tool="firecrawl",
            ok=True,
            url=url,
            markdown=data.get("markdown") or "",
            title=meta.get("title", ""),
            extra={
                "credits_used": d.get("creditsUsed"),
                "json": (data.get("json") if schema else None),
            },
        )
    except urllib.error.HTTPError as e:
        return FetchResult(tool="firecrawl", ok=False, url=url,
                           error=f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}")
    except Exception as e:
        return FetchResult(tool="firecrawl", ok=False, url=url,
                           error=f"{type(e).__name__}: {e}")


# ---------- playwright adapter (login-gated + heavy SPA) ----------
LOGIN_HINTS = (
    # sites that strictly require login to render any useful content
    "accounts.google.com",
    "mail.google.com",
    "gmail.com",
    "app.slack.com",
    "notion.so",   # workspace pages (notion.so/product is public; workspace is gated)
    "trello.com",
    "asana.com",
    "linear.app",
    "github.com",  # private repos
    "gitlab.com",
)


def _playwright(url: str, *, wait_selector: str | None = None, wait_ms: int = 2000,
                via: str = "auto") -> FetchResult:
    """Playwright adapter: heavy JS / login-gated sites. Delegates to one of
    the playwright/ adapters (python or mcp)."""
    tools_dir = Path(__file__).resolve().parent
    pw_dir = tools_dir / "playwright"
    sys.path.insert(0, str(pw_dir))

    if via in ("auto", "python"):
        try:
            from python_adapter import fetch as pw_fetch
            r = pw_fetch(url, wait_selector=wait_selector, wait_ms=wait_ms)
            r.setdefault("via", "playwright_python")
            if r.get("ok"):
                return FetchResult(
                    tool="playwright", ok=True, url=url,
                    markdown=r.get("markdown", ""),
                    title=r.get("title", ""),
                    extra=r,
                )
            # python failed, try mcp
            if via == "auto":
                return _playwright(url, wait_selector=wait_selector,
                                   wait_ms=wait_ms, via="mcp")
            return FetchResult(tool="playwright", ok=False, url=url,
                               error=r.get("error", "unknown"))
        except Exception as e:
            if via == "auto":
                return _playwright(url, wait_selector=wait_selector,
                                   wait_ms=wait_ms, via="mcp")
            return FetchResult(tool="playwright", ok=False, url=url,
                               error=f"{type(e).__name__}: {e}")

    if via == "mcp":
        from mcp_adapter import fetch as mcp_fetch
        r = mcp_fetch(url, wait_selector=wait_selector, wait_ms=wait_ms)
        return FetchResult(
            tool="playwright", ok=r.get("ok", False), url=url,
            markdown=r.get("markdown", ""), title=r.get("title", ""),
            error=r.get("error", ""),
            extra={"via": r.get("via", "playwright_mcp"), **r},
        )
    return FetchResult(tool="playwright", ok=False, url=url,
                       error=f"unknown via: {via}")


def _tavily_search(query: str, limit: int = 5) -> FetchResult:
    key = os.environ.get("TAVILY_API_KEY")
    if not key:
        return FetchResult(tool="tavily", ok=False, url=query,
                           error="TAVILY_API_KEY not set")
    payload = {"api_key": key, "query": query, "max_results": limit,
               "include_raw_content": True, "search_depth": "advanced"}
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        results = d.get("results", [])
        # stitch results into a single markdown block
        md_parts = [f"# Tavily results for: {query}\n"]
        for x in results[:limit]:
            md_parts.append(f"## {x.get('title','')}\n{x.get('url','')}\n\n"
                            f"{(x.get('content') or x.get('raw_content') or '')[:1500]}\n")
        return FetchResult(
            tool="tavily", ok=True, url=query, markdown="\n".join(md_parts),
            extra={"results_count": len(results)},
        )
    except Exception as e:
        return FetchResult(tool="tavily", ok=False, url=query,
                           error=f"{type(e).__name__}: {e}")


# ---------- router ----------

def fetch_url(url: str, *, schema: dict | None = None, prompt: str | None = None,
              force_tool: str | None = None, use_login: bool = False) -> FetchResult:
    """Auto-route: cheap first, escalate on failure.

    Strategy:
      1. If force_tool given, use it directly.
      2. If use_login=True OR URL in login-hint list, go straight to Playwright.
      3. If URL domain in Firecrawl blacklist, try Hermes curl.
      4. If URL domain looks like SPA, go straight to Firecrawl (Hermes won't get JS).
      5. Otherwise: Hermes curl first; if visible text < 400 chars, fall back to Firecrawl.
      6. Last resort: Playwright (handles both login + JS-render edge cases).
    """
    if force_tool == "hermes_curl":
        return _hermes_curl(url)
    if force_tool == "firecrawl":
        return _firecrawl_scrape(url, schema=schema, prompt=prompt)
    if force_tool == "tavily":
        return _tavily_search(url)
    if force_tool == "playwright":
        return _playwright(url)
    if force_tool:
        return FetchResult(tool=force_tool, ok=False, url=url,
                           error=f"unknown tool: {force_tool}")

    domain = url.split("/")[2] if "://" in url else url

    if use_login or any(l in domain for l in LOGIN_HINTS):
        return _playwright(url)

    if any(b in domain for b in FC_BLACKLIST):
        return _hermes_curl(url)
    if any(s in domain for s in SPA_HINTS):
        return _firecrawl_scrape(url, schema=schema, prompt=prompt)
    # default: cheap first
    cheap = _hermes_curl(url)
    if cheap.ok:
        return cheap
    # escalate to firecrawl
    fc = _firecrawl_scrape(url, schema=schema, prompt=prompt)
    if fc.ok:
        return fc
    # last resort: playwright (handles JS-rendered content firecrawl missed)
    return _playwright(url)


def search_query(query: str, *, limit: int = 5, force_tool: str | None = None) -> FetchResult:
    """Use Tavily for semantic search. Falls back to Firecrawl /v2/search."""
    if force_tool in (None, "tavily"):
        if os.environ.get("TAVILY_API_KEY"):
            return _tavily_search(query, limit=limit)
    if force_tool in (None, "firecrawl"):
        return _firecrawl_search(query, limit=limit)
    return FetchResult(tool=force_tool or "auto", ok=False, url=query,
                       error="no search tool available")


def _firecrawl_search(query: str, limit: int = 5) -> FetchResult:
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        return FetchResult(tool="firecrawl_search", ok=False, url=query,
                           error="FIRECRAWL_API_KEY not set")
    payload = {"query": query, "limit": limit}
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v2/search",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        results = (d.get("data") or {}).get("web", [])
        md_parts = [f"# Firecrawl search results for: {query}\n"]
        for x in results[:limit]:
            md_parts.append(f"- [{x.get('title','')}]({x.get('url','')})")
        return FetchResult(
            tool="firecrawl_search", ok=True, url=query,
            markdown="\n".join(md_parts),
            extra={"credits_used": d.get("creditsUsed"), "results_count": len(results)},
        )
    except Exception as e:
        return FetchResult(tool="firecrawl_search", ok=False, url=query,
                           error=f"{type(e).__name__}: {e}")


# ---------- CLI ----------

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: web_router.py <url|query> [--tool firecrawl|hermes_curl|tavily|search] "
              "[--schema PATH] [--prompt TEXT] [--out PATH]")
        return 2
    target = sys.argv[1]
    args = {"force_tool": None, "schema": None, "prompt": None, "out": None}
    i = 2
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--tool":
            args["force_tool"] = sys.argv[i + 1]
            i += 2
        elif a == "--schema":
            with open(sys.argv[i + 1]) as f:
                args["schema"] = json.load(f)
            i += 2
        elif a == "--prompt":
            args["prompt"] = sys.argv[i + 1]
            i += 2
        elif a == "--out":
            args["out"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if target.startswith("http://") or target.startswith("https://"):
        r = fetch_url(target, schema=args["schema"], prompt=args["prompt"],
                      force_tool=args["force_tool"])
    else:
        r = search_query(target, force_tool=args["force_tool"])

    out = json.dumps(r.to_dict(), ensure_ascii=False, indent=2)
    if args["out"]:
        Path(args["out"]).write_text(out)
        print(f"OK via {r.tool}: -> {args['out']} "
              f"({len(r.markdown):,} markdown chars, ok={r.ok})")
    else:
        print(out)
    return 0 if r.ok else 1


if __name__ == "__main__":
    sys.exit(main())