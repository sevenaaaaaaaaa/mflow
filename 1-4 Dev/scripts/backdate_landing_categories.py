#!/usr/bin/env python3
"""Backdate compositePage releaseDate for 7 landing categories.

Rule (2026-07-08, replaces AB-P08 fixed floor):
- Homepage-featured slugs: releaseDate in [exec_day - 59d, exec_day], evenly spread;
  rank #1 = newest (exec_day), rank #N = oldest in window.
- All other slugs: releaseDate strictly before window start (60d outside).
- All language variants of a slug share the same releaseDate.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

PROJECT_ID = "o11tm2qe"
DATASET = "production"
API_VERSION = "2024-01-01"
QUERY_URL = f"https://{PROJECT_ID}.api.sanity.io/v{API_VERSION}/data/query/{DATASET}"
MUTATE_URL = f"https://{PROJECT_ID}.api.sanity.io/v{API_VERSION}/data/mutate/{DATASET}"

RANKING_PATH = (
    Path(__file__).resolve().parents[2]
    / "1-2 Insight/排序分析/landing_pages_ranking_v2.json"
)
OUT_DIR = Path.home() / "Documents/Lovart Local Dev/Output/quality-audits"

HOME_SLOTS: dict[str, int] = {
    "tool": 6,
    "feature": 8,
    "topic": 12,
    "solution": 11,
    "product": 2,
    "landing": 3,
    "scenario": 0,
}

EXCLUDE_FEATURED: dict[str, set[str]] = {
    "solution": {"designers", "business-owners", "marketers", "download"},
    "landing": set(),
}

EMPTY_TITLE_SLUGS = {"designers", "business-owners", "marketers", "download"}


def token() -> str:
    return Path("/tmp/sanitytoken.txt").read_text(encoding="utf-8").strip()


def num(v: Any, default: float = 0.0) -> float:
    if v is None:
        return default
    if isinstance(v, (int, float)):
        return float(v)
    return default


def tier(item: dict[str, Any]) -> int:
    u30 = num(item.get("ga4_30d_users"))
    clicks = num(item.get("gsc_clicks"))
    impr = num(item.get("gsc_impr"))
    if u30 > 0 or clicks > 0 or impr > 0:
        return 0
    if num(item.get("score")) > 0 or num(item.get("lang_count")) > 0 or num(item.get("bodyLen")) > 0:
        return 1
    return 2


def sort_ranking(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda x: (
            tier(x),
            -num(x.get("score")),
            -num(x.get("ga4_30d_users")),
            -num(x.get("gsc_clicks")),
            x.get("slug") or "",
        ),
    )


def iso_noon(d: date) -> str:
    return datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.000Z"
    )


def featured_dates(count: int, win_start: date, win_end: date) -> list[str]:
    if count <= 0:
        return []
    if count == 1:
        return [iso_noon(win_end)]
    span = (win_end - win_start).days
    out: list[str] = []
    for i in range(count):
        # rank 1 (i=0) -> win_end; rank N -> win_start
        frac = (count - 1 - i) / (count - 1)
        d = win_start + timedelta(days=round(frac * span))
        out.append(iso_noon(d))
    return out


def outside_date(index: int, win_start: date) -> str:
    # index 0 = closest before window; larger index = older
    return iso_noon(win_start - timedelta(days=index + 1))


def pick_featured_slugs(cat: str, ranked: list[dict[str, Any]]) -> list[str]:
    need = HOME_SLOTS.get(cat, 0)
    if need <= 0:
        return []
    exclude = EXCLUDE_FEATURED.get(cat, set())
    picked: list[str] = []
    for item in ranked:
        slug = item.get("slug")
        if not slug or slug in exclude:
            continue
        if cat == "landing" and str(slug).lower() in {"none", "null"}:
            continue
        if cat == "solution" and (not item.get("title") or slug in EMPTY_TITLE_SLUGS):
            continue
        picked.append(slug)
        if len(picked) >= need:
            break
    return picked


def build_slug_dates(cat: str, ranked: list[dict[str, Any]], win_start: date, win_end: date) -> dict[str, str]:
    featured = pick_featured_slugs(cat, ranked)
    feat_dates = featured_dates(len(featured), win_start, win_end)
    slug_to_date: dict[str, str] = {}
    for slug, dt in zip(featured, feat_dates):
        slug_to_date[slug] = dt

    outside_idx = 0
    for item in ranked:
        slug = item.get("slug")
        if not slug or slug in slug_to_date:
            continue
        slug_to_date[slug] = outside_date(outside_idx, win_start)
        outside_idx += 1
    return slug_to_date


def groq(query: str) -> Any:
    r = requests.get(
        QUERY_URL,
        params={"query": query},
        headers={"Authorization": f"Bearer {token()}"},
        timeout=120,
    )
    r.raise_for_status()
    return r.json().get("result")


def fetch_category_docs(cat: str) -> list[dict[str, Any]]:
    q = (
        f'*[_type=="compositePage" && category=="{cat}"]'
        '{_id,language,"slug":slug.current,releaseDate,publishedAt,title}'
    )
    return groq(q) or []


def mutate(patches: list[dict[str, Any]], apply: bool) -> None:
    if not patches:
        return
    if not apply:
        return
    chunk = 200
    for i in range(0, len(patches), chunk):
        body = {"mutations": patches[i : i + chunk]}
        r = requests.post(
            MUTATE_URL,
            headers={"Authorization": f"Bearer {token()}", "Content-Type": "application/json"},
            json=body,
            timeout=120,
        )
        r.raise_for_status()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write patches to Sanity production")
    parser.add_argument("--exec-day", default=str(date.today()), help="Execution day YYYY-MM-DD")
    args = parser.parse_args()

    exec_day = date.fromisoformat(args.exec_day)
    win_end = exec_day
    win_start = exec_day - timedelta(days=59)

    ranking = json.loads(RANKING_PATH.read_text(encoding="utf-8"))
    categories = ranking["categories"]

    report: dict[str, Any] = {
        "exec_day": str(exec_day),
        "window": {"start": str(win_start), "end": str(win_end)},
        "rule": "featured in 60d window; others before window start",
        "categories": {},
        "totals": {"docs": 0, "changed": 0, "patches": 0},
        "apply": args.apply,
    }

    all_patches: list[dict[str, Any]] = []

    for cat in ["tool", "feature", "topic", "solution", "product", "landing", "scenario"]:
        ranked = sort_ranking(categories.get(cat, {}).get("ranking", []))
        slug_dates = build_slug_dates(cat, ranked, win_start, win_end)

        docs = fetch_category_docs(cat)
        # scenario may have docs not in ranking JSON
        if cat == "scenario":
            slugs_sorted = sorted(
                {d.get("slug") for d in docs if d.get("slug")},
                key=lambda s: s or "",
            )
            for i, slug in enumerate(slugs_sorted):
                slug_dates[slug] = outside_date(i, win_start)

        cat_report: dict[str, Any] = {
            "featured_slugs": pick_featured_slugs(cat, ranked),
            "slug_count_ranking": len(ranked),
            "doc_count_sanity": len(docs),
            "changed": 0,
            "samples": [],
        }

        for doc in docs:
            slug = doc.get("slug")
            if not slug:
                new_dt = outside_date(0, win_start)
            else:
                new_dt = slug_dates.get(slug)
                if not new_dt:
                    new_dt = outside_date(cat_report["changed"] + 1000, win_start)

            old_dt = doc.get("releaseDate")
            if old_dt == new_dt:
                continue
            cat_report["changed"] += 1
            if len(cat_report["samples"]) < 5:
                cat_report["samples"].append(
                    {
                        "_id": doc["_id"],
                        "slug": slug,
                        "language": doc.get("language"),
                        "old": old_dt,
                        "new": new_dt,
                    }
                )
            all_patches.append({"patch": {"id": doc["_id"], "set": {"releaseDate": new_dt}}})

        report["categories"][cat] = cat_report
        report["totals"]["docs"] += len(docs)
        report["totals"]["changed"] += cat_report["changed"]

    report["totals"]["patches"] = len(all_patches)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"landing-backdate-plan-{exec_day}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    mutate(all_patches, args.apply)
    if args.apply:
        print(f"APPLIED {len(all_patches)} patches")
    else:
        print(f"DRY RUN — {len(all_patches)} patches planned. Re-run with --apply to write.")
    print(f"Plan saved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
