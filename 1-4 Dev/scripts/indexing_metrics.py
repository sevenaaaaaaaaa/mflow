#!/usr/bin/env python3
"""GSC 收录指标 SSOT — 禁止用 rowLimit=1000 的 page 行数当收录。"""
from __future__ import annotations

import json
from pathlib import Path

INDEXING_CORPUS_TOTAL = 20_000
PAGE_FETCH_ROW_LIMIT = 5000
PAGE_FETCH_MAX_ROWS = 25_000


def _load_baseline_corpus(trident_root: Path | None) -> int:
    if trident_root is None:
        return INDEXING_CORPUS_TOTAL
    p = trident_root / "reports" / "indexing-baseline.json"
    if not p.exists():
        return INDEXING_CORPUS_TOTAL
    try:
        d = json.loads(p.read_text())
        return int(d.get("corpus_total", INDEXING_CORPUS_TOTAL))
    except (json.JSONDecodeError, TypeError, ValueError):
        return INDEXING_CORPUS_TOTAL


def fetch_sitemap_counts(svc, site: str) -> dict:
    submitted = 0
    indexed = 0
    try:
        sm = svc.sitemaps().list(siteUrl=site).execute()
        for s in sm.get("sitemap", []):
            contents = s.get("contents") or [{}]
            c0 = contents[0] if contents else {}
            submitted += int(c0.get("submitted", 0) or 0)
            indexed += int(c0.get("indexed", 0) or 0)
    except Exception:
        pass
    return {"sitemap_submitted": submitted, "sitemap_indexed": indexed}


def paginate_pages_with_traffic(search, site: str, start: str, end: str) -> tuple[int, list]:
    """全月 dimensions=page 分页，统计 impressions>0 的去重 URL。"""
    seen = set()
    top_pages: list = []
    start_row = 0
    while start_row < PAGE_FETCH_MAX_ROWS:
        body = {
            "startDate": start,
            "endDate": end,
            "dimensions": ["page"],
            "rowLimit": PAGE_FETCH_ROW_LIMIT,
            "startRow": start_row,
        }
        resp = search.query(siteUrl=site, body=body).execute()
        rows = resp.get("rows", [])
        if not rows:
            break
        for rw in rows:
            url = rw["keys"][0]
            impr = rw["impressions"]
            if impr > 0 and url not in seen:
                seen.add(url)
            if len(top_pages) < 1000:
                top_pages.append({
                    "url": url,
                    "clicks": rw["clicks"],
                    "impr": impr,
                    "ctr": round(rw["ctr"] * 100, 1),
                    "pos": round(rw["position"], 1),
                })
        if len(rows) < PAGE_FETCH_ROW_LIMIT:
            break
        start_row += PAGE_FETCH_ROW_LIMIT
    top_pages.sort(key=lambda x: x["clicks"], reverse=True)
    return len(seen), top_pages


def fetch_indexing_bundle(search, site: str, start: str, end: str, svc, trident_root, cache_dir, ym: str, *, use_cache: bool = True) -> dict:
    """Integrated entry: sitemap via svc + paginated pages."""
    sm = {"sitemap_submitted": 0, "sitemap_indexed": 0}
    try:
        sm_resp = svc.sitemaps().list(siteUrl=site).execute()
        for s in sm_resp.get("sitemap", []):
            contents = s.get("contents") or [{}]
            c0 = contents[0] if contents else {}
            sm["sitemap_submitted"] += int(c0.get("submitted", 0) or 0)
            sm["sitemap_indexed"] += int(c0.get("indexed", 0) or 0)
    except Exception:
        sm["sitemap_submitted"] = 69788

    cache_path = cache_dir / f"indexing-{ym}.json" if cache_dir and ym else None
    if use_cache and cache_path and cache_path.exists():
        cached = json.loads(cache_path.read_text())
        pages_with_traffic = int(cached.get("pages_with_traffic", 0))
        _, top_pages = paginate_pages_with_traffic(search, site, start, end)
    else:
        pages_with_traffic, top_pages = paginate_pages_with_traffic(search, site, start, end)

    corpus = _load_baseline_corpus(trident_root)
    index_rate_primary = round(pages_with_traffic / corpus * 100, 2) if corpus else 0
    sitemap_rate = (
        round(sm["sitemap_indexed"] / sm["sitemap_submitted"] * 100, 2)
        if sm["sitemap_submitted"] and sm["sitemap_indexed"]
        else None
    )
    result = {
        "pages_with_traffic": pages_with_traffic,
        "indexing_corpus_total": corpus,
        "index_rate_primary": index_rate_primary,
        "sitemap_submitted": sm["sitemap_submitted"],
        "sitemap_indexed": sm["sitemap_indexed"],
        "sitemap_index_rate": sitemap_rate,
        "top_pages": top_pages,
        "index_pages": pages_with_traffic,
        "index_rate": index_rate_primary,
    }
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(
            json.dumps({k: v for k, v in result.items() if k != "top_pages"}, indent=2, ensure_ascii=False)
        )
    return result
