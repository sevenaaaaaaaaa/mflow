"""
tavily_search — semantic web search with cleaned content.

Use when: you need to "look up X" but don't have a specific URL yet.
Output is LLM-ready (markdown-stitched).

Auth: $TAVILY_API_KEY
CLI:
    python3 tavily_search.py "best AI design agent 2026" --limit 5
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.tavily.com/search"
OUT_DIR = Path(__file__).resolve().parent.parent / "Output" / "Tavily"


def search(query: str, limit: int = 5) -> dict:
    key = os.environ.get("TAVILY_API_KEY")
    if not key:
        raise SystemExit("ERROR: set TAVILY_API_KEY first.")
    payload = {
        "api_key": key,
        "query": query,
        "max_results": limit,
        "include_raw_content": True,
        "search_depth": "advanced",
    }
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: tavily_search.py <query> [--limit N]")
        return 2
    query = sys.argv[1]
    limit = 5
    for i, a in enumerate(sys.argv):
        if a == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"search-{dt.date.today().isoformat()}-{query[:40].replace(' ','_')}.json"
    print(f"[{dt.datetime.now():%H:%M:%S}] Tavily: {query!r}")
    try:
        d = search(query, limit=limit)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:200]}", file=sys.stderr)
        return 1
    results = d.get("results", [])
    out.write_text(json.dumps({"query": query, "fetched_at": dt.datetime.now().isoformat(),
                               "results": results}, ensure_ascii=False, indent=2))
    print(f"OK: {len(results)} results -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())