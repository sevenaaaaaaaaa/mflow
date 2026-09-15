"""
Lovart Changelog -> Structured JSON, via Firecrawl /v2/scrape.

Zero-dep stdlib only (works under Hermes venv quirks).

Drops outputs into:
  /Users/seveno/Documents/Lovart Local Dev/Output/Firecrawl/
    └── changelog-YYYY-MM-DD.json

Auth: $FIRECRAWL_API_KEY (export in shell, never paste into chat).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.firecrawl.dev/v2/scrape"
URL = "https://www.lovart.ai/changelog"
OUT_DIR = Path.home() / "Documents" / "Lovart Local Dev" / "Output" / "Firecrawl"

SCHEMA = {
    "type": "object",
    "properties": {
        "releases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Release date, e.g. May 6, 2026"},
                    "title": {"type": "string", "description": "Exact heading as on page"},
                    "summary": {"type": "string", "description": "One-sentence plain-English impact"},
                    "category": {"type": "string", "description": "Model | Feature | UI | Bug fix | Integration"},
                },
                "required": ["date", "title", "summary"],
            },
        }
    },
}

PROMPT = (
    "Extract every changelog entry on this page. For each entry provide its release "
    "date, the exact title as written, a one-sentence plain-English summary of what "
    "changed and why it matters to a Lovart user, and the category "
    "(Model / Feature / UI / Bug fix / Integration). Order from newest to oldest."
)


def fetch(api_key: str) -> dict:
    payload = {
        "url": URL,
        "formats": [{"type": "json", "schema": SCHEMA, "prompt": PROMPT}],
        "onlyMainContent": True,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "lovart-firecrawl/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        print("ERROR: set FIRECRAWL_API_KEY first.", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    out_path = OUT_DIR / f"changelog-{today}.json"

    print(f"[{today}] POST {API}")
    try:
        resp = fetch(key)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}", file=sys.stderr)
        return 1

    if not resp.get("success"):
        print("ERROR response:", json.dumps(resp, indent=2)[:500], file=sys.stderr)
        return 1

    data = resp.get("data") or {}
    payload_out = {
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source_url": URL,
        "title": (data.get("metadata") or {}).get("title"),
        "credits_used": resp.get("creditsUsed"),
        "releases": (data.get("json") or {}).get("releases", []),
    }

    out_path.write_text(json.dumps(payload_out, ensure_ascii=False, indent=2))
    print(f"OK: {len(payload_out['releases'])} releases -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())