"""
Lovart Sentinel - Brave Search API Scanner

Uses Brave Search API instead of scraping search.brave.com, which quickly
returns 429 for repeated SERP requests.

Token lookup order:
1. BRAVE_SEARCH_API_KEY
2. BRAVE_API_KEY
3. scripts/sentinel/credentials/brave_search_api_key
4. scripts/sentinel/bing_credentials/brave_search_api_key
"""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

import requests

try:
    from ._common import banner
except ImportError:  # Allows direct local execution.
    def banner(name: str) -> dict:
        return {"source": name}


QUERIES = {
    "brand": "lovart ai",
    "official": "www.lovart.ai",
    "review": "lovart ai review",
    "design_agent": "ai design agent",
    "logo": "ai logo generator",
    "ko_design_agent": "AI 디자인 에이전트",
    "ja_brand": "Lovart AI デザイン",
}

PARASITES = [
    "lovart-ai.com",
    "lovart.pro",
    "lovart.io",
    "lovart.info",
    "lovart.me",
]


def _token() -> str | None:
    for key in ("BRAVE_SEARCH_API_KEY", "BRAVE_API_KEY"):
        if os.environ.get(key):
            return os.environ[key].strip()

    root = Path(__file__).resolve().parents[1]
    candidates = [
        root / "credentials" / "brave_search_api_key",
        root / "bing_credentials" / "brave_search_api_key",
    ]
    for path in candidates:
        if path.exists() and path.read_text().strip():
            return path.read_text().strip()
    return None


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def _classify_results(items: list[dict]) -> dict:
    top_domains = []
    seen = set()
    lovart_positions = []
    parasite_hits = []

    for i, item in enumerate(items, start=1):
        url = item.get("url") or ""
        domain = _domain(url)
        if domain and domain not in seen:
            seen.add(domain)
            top_domains.append(domain)
        if "lovart.ai" in domain:
            lovart_positions.append(i)
        if any(p in domain for p in PARASITES):
            parasite_hits.append({"position": i, "domain": domain, "url": url})

    return {
        "top_domains": top_domains[:10],
        "lovart_positions": lovart_positions,
        "best_lovart_position": min(lovart_positions) if lovart_positions else None,
        "parasite_hits": parasite_hits,
    }


def collect(brand_config: dict | None = None) -> dict:
    data = dict(banner("Brave Search API Scan"))
    token = _token()
    data["queries"] = QUERIES
    data["data_source_type"] = "official_api"
    data["status"] = "missing_token" if not token else "ok"

    if not token:
        data["instructions"] = (
            "Set BRAVE_SEARCH_API_KEY or create "
            "1-4 Dev/scripts/sentinel/credentials/brave_search_api_key, "
            "then run collect.py --source serp_brave_api."
        )
        return data

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": token,
    }
    results = {}

    for name, query in QUERIES.items():
        try:
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": query, "count": 10, "search_lang": "en"},
                headers=headers,
                timeout=20,
            )
            payload = response.json() if response.content else {}
            items = (payload.get("web") or {}).get("results") or []
            results[name] = {
                "query": query,
                "status_code": response.status_code,
                "items": [
                    {
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "description": item.get("description"),
                    }
                    for item in items[:10]
                ],
                **_classify_results(items),
            }
        except Exception as exc:
            results[name] = {
                "query": query,
                "error": f"{type(exc).__name__}: {exc}",
            }

    data["results"] = results
    return data


if __name__ == "__main__":
    import json

    print(json.dumps(collect(), ensure_ascii=False, indent=2))
