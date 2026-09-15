"""
python_adapter.py — Playwright Python sync adapter for web_router.

Use this when you need:
  - Logged-in pages (Gmail, Notion workspace, Slack, etc.)
  - Heavy SPAs that block JS-driven content
  - Cookies / session persistence across calls

The adapter takes care of:
  - Chromium launch (headless, sandboxed, configurable)
  - Optional cookie injection from $LOVART_BROWSER_COOKIES_JSON
  - Markdown extraction via inner_text + best-effort cleanup
  - Persistent profile dir so you can log in once, reuse forever

CLI:
    PYTHONPATH= $VENV/bin/python python_adapter.py https://app.notion.so/...
    PYTHONPATH= $VENV/bin/python python_adapter.py https://gmail.com/ --user-data-dir ~/.lovart-browser
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

DEFAULT_USER_DATA_DIR = Path.home() / "Library" / "Caches" / "lovart-browser-profile"


def _strip_to_markdown(text: str) -> str:
    """Rough cleanup of inner_text into something like markdown.

    Real apps would call html2text / markdownify on inner_html, but stdlib-only
    here keeps the adapter dependency-free."""
    # collapse whitespace runs
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # treat ALL-CAPS short lines as headings
    lines = []
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if 3 <= len(s) <= 80 and s.upper() == s and re.search(r"[A-Z]", s):
            lines.append(f"## {s}")
        else:
            lines.append(s)
    return "\n".join(lines).strip()


def fetch(
    url: str,
    *,
    wait_selector: str | None = None,
    wait_ms: int = 2000,
    user_data_dir: str | None = None,
    headless: bool = True,
    cookies: list[dict] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """Open URL in headless Chromium with optional cookie injection / persistent profile.

    Returns dict: {ok, title, markdown, html_chars, http_status, elapsed_s, error}.
    """
    user_data_dir = user_data_dir or os.environ.get("LOVART_BROWSER_USER_DATA_DIR",
                                                    str(DEFAULT_USER_DATA_DIR))
    Path(user_data_dir).mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=headless,
                user_agent=CHROME_UA,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1280, "height": 800},
            )
            try:
                page = browser.pages[0] if browser.pages else browser.new_page()
                if cookies:
                    page.context.add_cookies(cookies)

                resp = page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=timeout * 1000)
                    except PWTimeout:
                        pass
                page.wait_for_timeout(wait_ms)

                title = page.title()
                body_text = page.locator("body").inner_text()
                md = _strip_to_markdown(body_text)

                return {
                    "ok": True,
                    "title": title,
                    "markdown": md,
                    "body_chars": len(body_text),
                    "http_status": resp.status if resp else None,
                    "url_after_redirects": page.url,
                    "elapsed_s": round(time.time() - t0, 2),
                }
            finally:
                browser.close()
    except PWTimeout as e:
        return {"ok": False, "error": f"PlaywrightTimeout: {e}", "elapsed_s": round(time.time() - t0, 2)}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "elapsed_s": round(time.time() - t0, 2)}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python_adapter.py <url> [--wait-selector SEL] [--wait-ms N] "
              "[--user-data-dir PATH] [--headless false] [--cookies JSON] [--out PATH]")
        return 2

    url = sys.argv[1]
    args: dict[str, Any] = {
        "wait_selector": None,
        "wait_ms": 2000,
        "user_data_dir": None,
        "headless": True,
        "cookies": None,
        "out": None,
    }
    i = 2
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--wait-selector":
            args["wait_selector"] = sys.argv[i + 1]
            i += 2
        elif a == "--wait-ms":
            args["wait_ms"] = int(sys.argv[i + 1])
            i += 2
        elif a == "--user-data-dir":
            args["user_data_dir"] = sys.argv[i + 1]
            i += 2
        elif a == "--headless":
            args["headless"] = sys.argv[i + 1].lower() != "false"
            i += 2
        elif a == "--cookies":
            args["cookies"] = json.loads(sys.argv[i + 1])
            i += 2
        elif a == "--out":
            args["out"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    print(f"[{time.strftime('%H:%M:%S')}] Playwright GET {url}")
    r = fetch(url, **{k: v for k, v in args.items() if k != "out"})
    if args["out"]:
        Path(args["out"]).parent.mkdir(parents=True, exist_ok=True)
        Path(args["out"]).write_text(json.dumps(r, ensure_ascii=False, indent=2))
        print(f"OK: title={r.get('title','')[:60]!r}  body={r.get('body_chars',0):,} "
              f"chars  elapsed={r.get('elapsed_s')}s  -> {args['out']}")
    else:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())