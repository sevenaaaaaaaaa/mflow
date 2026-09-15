#!/usr/bin/env python3
"""
Submit Lovart URLs to IndexNow.

Default mode is dry-run. Real submission requires:
1. INDEXNOW_KEY env var, or credentials/indexnow_key
2. The same key hosted at https://www.lovart.ai/{KEY}.txt

Examples:
  python3 "1-4 Dev/scripts/multi_seo/indexnow_submit.py"
  INDEXNOW_KEY=... python3 "1-4 Dev/scripts/multi_seo/indexnow_submit.py" --submit
  python3 "1-4 Dev/scripts/multi_seo/indexnow_submit.py" --urls urls.txt --submit
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

import requests


HOST = "www.lovart.ai"
BASE_URL = f"https://{HOST}"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
DEFAULT_SITEMAPS = [
    f"{BASE_URL}/sitemap-homepage.xml",
    f"{BASE_URL}/sitemap-tools.xml",
    f"{BASE_URL}/sitemap-features.xml",
    f"{BASE_URL}/sitemap-blog.xml",
    f"{BASE_URL}/sitemap-lang-ko.xml",
    f"{BASE_URL}/sitemap-lang-ja.xml",
    f"{BASE_URL}/sitemap-lang-zh.xml",
]


def _credential_paths() -> list[Path]:
    script_dir = Path(__file__).resolve().parent
    return [
        script_dir / "credentials" / "indexnow_key",
        script_dir.parent / "sentinel" / "credentials" / "indexnow_key",
        script_dir.parent / "sentinel" / "bing_credentials" / "indexnow_key",
    ]


def load_key() -> str | None:
    if os.environ.get("INDEXNOW_KEY"):
        return os.environ["INDEXNOW_KEY"].strip()
    for path in _credential_paths():
        if path.exists() and path.read_text().strip():
            return path.read_text().strip()
    return None


def fetch_sitemap_urls(sitemap_url: str, limit: int) -> list[str]:
    req = urllib.request.Request(sitemap_url, headers={"User-Agent": "LovartIndexNow/1.0"})
    with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as response:
        body = response.read()
    root = ET.fromstring(body)
    urls = []
    for elem in root.iter():
        if elem.tag.endswith("loc") and elem.text:
            loc = elem.text.strip()
            if loc.startswith(BASE_URL):
                urls.append(loc)
            if len(urls) >= limit:
                break
    return urls


def default_urls(limit_per_sitemap: int) -> list[str]:
    urls = []
    seen = set()
    for sitemap in DEFAULT_SITEMAPS:
        try:
            for url in fetch_sitemap_urls(sitemap, limit_per_sitemap):
                if url not in seen:
                    seen.add(url)
                    urls.append(url)
        except Exception as exc:
            print(f"WARN failed to read {sitemap}: {type(exc).__name__}: {exc}", file=sys.stderr)
    priority = [
        BASE_URL + "/",
        BASE_URL + "/ko",
        BASE_URL + "/ja",
        BASE_URL + "/tools",
        BASE_URL + "/features",
        BASE_URL + "/features/ai-design-agent",
        BASE_URL + "/pricing",
    ]
    return priority + [url for url in urls if url not in priority]


def read_url_file(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def key_file_status(key: str | None) -> dict:
    if not key:
        return {"status": "missing_key"}
    url = f"{BASE_URL}/{key}.txt"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LovartIndexNow/1.0"})
        with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as response:
            body = response.read(200).decode("utf-8", errors="replace").strip()
            return {
                "url": url,
                "status_code": response.status,
                "content_type": response.headers.get("content-type", ""),
                "matches_key": body == key,
                "body_start": body[:80],
            }
    except Exception as exc:
        return {"url": url, "error": f"{type(exc).__name__}: {exc}"}


def submit(key: str, urls: list[str]) -> requests.Response:
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE_URL}/{key}.txt",
        "urlList": urls,
    }
    return requests.post(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit Lovart URLs to IndexNow")
    parser.add_argument("--urls", type=Path, help="Text file with one URL per line")
    parser.add_argument("--limit-per-sitemap", type=int, default=5)
    parser.add_argument("--submit", action="store_true", help="Actually submit to IndexNow")
    args = parser.parse_args()

    key = load_key()
    urls = read_url_file(args.urls) if args.urls else default_urls(args.limit_per_sitemap)
    urls = [url for url in urls if url.startswith(BASE_URL)]

    print(json.dumps({
        "host": HOST,
        "key_present": bool(key),
        "key_file": key_file_status(key),
        "url_count": len(urls),
        "urls": urls[:50],
        "dry_run": not args.submit,
    }, ensure_ascii=False, indent=2))

    if not args.submit:
        return 0
    if not key:
        print("ERROR INDEXNOW_KEY missing.", file=sys.stderr)
        return 2
    status = key_file_status(key)
    if not status.get("matches_key"):
        print("ERROR IndexNow key file is not deployed or does not match key.", file=sys.stderr)
        return 3

    response = submit(key, urls)
    print(f"IndexNow status={response.status_code} body={response.text[:500]}")
    return 0 if response.status_code in (200, 202) else 1


if __name__ == "__main__":
    raise SystemExit(main())
