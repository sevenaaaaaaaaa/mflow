"""
hermes_curl — stdlib fallback for sites Firecrawl blacklists.

Best for: LinkedIn, Instagram (login walls), or any static-HTML page where
Firecrawl isn't worth the credit.

Auth: none.
CLI:
    python3 hermes_curl.py https://www.linkedin.com/
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
OUT_DIR = Path(__file__).resolve().parent.parent / "Output" / "HermesCurl"

_TAG_RE = re.compile(r"<script[^>]*>.*?</script>", re.S | re.I)
_STYLE_RE = re.compile(r"<style[^>]*>.*?</style>", re.S | re.I)
_TAG_STRIP_RE = re.compile(r"<[^>]+>")


def fetch(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": CHROME_UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", "replace")
        return {"http_status": r.status, "raw_chars": len(body), "body": body}


def visible_text(html: str) -> str:
    body = _TAG_RE.sub(" ", html)
    body = _STYLE_RE.sub(" ", body)
    body = _TAG_STRIP_RE.sub(" ", body)
    return re.sub(r"\s+", " ", body).strip()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: hermes_curl.py <url>")
        return 2
    url = sys.argv[1]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{dt.date.today().isoformat()}-{url.split('/')[2]}.json"
    print(f"[{dt.datetime.now():%H:%M:%S}] GET {url}")
    try:
        d = fetch(url)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}", file=sys.stderr)
        return 1
    visible = visible_text(d["body"])
    payload = {
        "url": url,
        "fetched_at": dt.datetime.now().isoformat(),
        "http_status": d["http_status"],
        "raw_chars": d["raw_chars"],
        "visible_chars": len(visible),
        "title_m": re.search(r"<title>(.*?)</title>", d["body"], re.S | re.I),
        "visible": visible[:50000],
    }
    if payload["title_m"]:
        payload["title"] = payload["title_m"].group(1).strip()[:200]
        del payload["title_m"]
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"OK: visible={len(visible):,} chars -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())