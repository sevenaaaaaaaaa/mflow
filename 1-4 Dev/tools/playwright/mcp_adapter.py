"""
mcp_adapter.py — bridge web_router to a running @playwright/mcp server.

Use this when:
  - Claude Code / Cursor is already driving @playwright/mcp (no extra browser spawn)
  - You want to compose Playwright + other tools in one MCP-aware pipeline

The adapter speaks to the MCP server over stdio (default) or HTTP (if
PLAYWRIGHT_MCP_URL is set). It shells out via `npx -y @playwright/mcp` if
the server isn't already running.

Auth: inherits from your MCP client (Claude/Cursor config), or override via
PLAYWRIGHT_MCP_URL=http://localhost:8931

CLI:
    python3 mcp_adapter.py https://app.notion.so/
    python3 mcp_adapter.py https://example.com --wait-selector "main"
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# The @playwright/mcp server exposes the following JSON-RPC methods we care about:
#   - browser.navigate { url }
#   - browser.wait_for { time?: N, selector?: "..." }
#   - browser.snapshot { }   -> { html, title, url, body_text }
#   - browser.close { }
#
# If the MCP server is HTTP (e.g., via `mcp-remote`), point at its /messages
# endpoint with PLAYWRIGHT_MCP_URL.


def _post_jsonrpc(url: str, method: str, params: dict, req_id: int = 1) -> dict:
    payload = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def fetch_http(url: str, *, wait_selector: str | None = None, wait_ms: int = 2000,
               mcp_url: str | None = None) -> dict[str, Any]:
    """Drive an HTTP-mode @playwright/mcp server."""
    mcp_url = mcp_url or os.environ.get("PLAYWRIGHT_MCP_URL", "http://localhost:8931/messages")
    t0 = time.time()
    try:
        _post_jsonrpc(mcp_url, "browser.navigate", {"url": url}, req_id=1)
        if wait_selector:
            _post_jsonrpc(mcp_url, "browser.wait_for", {"selector": wait_selector}, req_id=2)
        else:
            _post_jsonrpc(mcp_url, "browser.wait_for", {"time": wait_ms / 1000}, req_id=2)
        snap = _post_jsonrpc(mcp_url, "browser.snapshot", {}, req_id=3)
        result = snap.get("result", {})
        return {
            "ok": True,
            "title": result.get("title", ""),
            "markdown": result.get("body_text", ""),
            "url_after_redirects": result.get("url", url),
            "elapsed_s": round(time.time() - t0, 2),
            "via": f"mcp_http:{mcp_url}",
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "elapsed_s": round(time.time() - t0, 2), "via": f"mcp_http:{mcp_url}"}


def fetch_stdio(url: str, *, wait_selector: str | None = None, wait_ms: int = 2000,
                timeout: int = 60) -> dict[str, Any]:
    """Spawn `npx -y @playwright/mcp` and pipe a single navigate+snapshot sequence.

    This is a best-effort glue layer: the real MCP protocol uses Content-Length
    framed JSON-RPC over stdio. We use a simplified one-shot shell command instead,
    which works for batch jobs (start fresh MCP per request). For interactive
    sessions, use Claude/Cursor's MCP integration directly.
    """
    t0 = time.time()
    code = f"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto({url!r}, wait_until='domcontentloaded', timeout=30000)
        if {wait_selector!r}:
            try:
                await page.wait_for_selector({wait_selector!r}, timeout=10000)
            except Exception:
                pass
        else:
            await page.wait_for_timeout({wait_ms})
        body = await page.locator('body').inner_text()
        title = await page.title()
        print('<<<RESULT>>>' + json.dumps({{'title': title, 'body': body}}))
        await browser.close()

asyncio.run(main())
"""
    try:
        proc = subprocess.run(
            ["npx", "-y", "@playwright/mcp", "--stdio"],
            input=code.encode(),
            capture_output=True,
            timeout=timeout,
        )
        out = proc.stdout.decode("utf-8", "replace")
        if "<<<RESULT>>>" not in out:
            return {"ok": False, "error": f"no marker in output: {out[-300:]}",
                    "elapsed_s": round(time.time() - t0, 2)}
        payload = out.split("<<<RESULT>>>", 1)[1].strip().split("\n", 1)[0]
        parsed = json.loads(payload)
        return {
            "ok": True,
            "title": parsed.get("title", ""),
            "markdown": parsed.get("body", ""),
            "body_chars": len(parsed.get("body", "")),
            "elapsed_s": round(time.time() - t0, 2),
            "via": "mcp_stdio_via_npx",
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout after {timeout}s",
                "elapsed_s": round(time.time() - t0, 2)}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "elapsed_s": round(time.time() - t0, 2)}


def fetch(url: str, **kwargs) -> dict[str, Any]:
    """Auto: use HTTP mode if PLAYWRIGHT_MCP_URL set or MCP running locally, else stdio."""
    mcp_url = os.environ.get("PLAYWRIGHT_MCP_URL")
    if mcp_url:
        return fetch_http(url, mcp_url=mcp_url, **kwargs)
    # Check if localhost MCP server is up
    try:
        with urllib.request.urlopen("http://localhost:8931/health", timeout=1):
            return fetch_http(url, **kwargs)
    except Exception:
        return fetch_stdio(url, **kwargs)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: mcp_adapter.py <url> [--wait-selector SEL] [--wait-ms N] [--mode http|stdio|auto] [--out PATH]")
        return 2

    url = sys.argv[1]
    args = {"wait_selector": None, "wait_ms": 2000, "mode": "auto", "out": None}
    i = 2
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--wait-selector":
            args["wait_selector"] = sys.argv[i + 1]
            i += 2
        elif a == "--wait-ms":
            args["wait_ms"] = int(sys.argv[i + 1])
            i += 2
        elif a == "--mode":
            args["mode"] = sys.argv[i + 1]
            i += 2
        elif a == "--out":
            args["out"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    print(f"[{time.strftime('%H:%M:%S')}] MCP GET {url} (mode={args['mode']})")
    if args["mode"] == "http":
        r = fetch_http(url, wait_selector=args["wait_selector"], wait_ms=args["wait_ms"])
    elif args["mode"] == "stdio":
        r = fetch_stdio(url, wait_selector=args["wait_selector"], wait_ms=args["wait_ms"])
    else:
        r = fetch(url, wait_selector=args["wait_selector"], wait_ms=args["wait_ms"])

    if args["out"]:
        Path(args["out"]).write_text(json.dumps(r, ensure_ascii=False, indent=2))
        print(f"OK: title={r.get('title','')[:60]!r}  body={r.get('body_chars','?')} "
              f"chars  elapsed={r.get('elapsed_s')}s  via={r.get('via')}  -> {args['out']}")
    else:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())