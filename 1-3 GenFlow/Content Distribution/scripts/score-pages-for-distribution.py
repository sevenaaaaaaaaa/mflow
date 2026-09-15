#!/usr/bin/env python3
"""
Score lovart.ai pages for off-site distribution from Trident GA/GSC snapshots.

Usage:
  python3 score-pages-for-distribution.py --days 28
  python3 score-pages-for-distribution.py --days 28 --sample
  python3 score-pages-for-distribution.py --input ~/path/ga4-pages.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = ROOT / "queue"

BLACKLIST_PATTERNS = [
    r"^/$",
    r"^/pricing",
    r"^/en/?$",
    r"^/zh/?$",
    r"^/ja/?$",
]

ALLOWED_PREFIXES = ("/blog/", "/tools/", "/features/")

PLATFORM_RULES = [
    (r"/tools/", ["pinterest", "deviantart", "medium"]),
    (r"/blog/.*tutorial|/blog/.*how-to|/blog/.*guide", ["devto", "hashnode", "medium", "zhihu"]),
    (r"/blog/", ["medium", "devto", "linkedin", "zhihu"]),
    (r"/features/", ["linkedin", "medium"]),
]


def norm(values: list[float], v: float) -> float:
    if not values:
        return 0.0
    lo, hi = min(values), max(values)
    if hi <= lo:
        return 1.0 if v >= hi else 0.0
    return (v - lo) / (hi - lo)


def is_blacklisted(path: str) -> bool:
    p = path.split("?")[0]
    return any(re.search(pat, p) for pat in BLACKLIST_PATTERNS)


def allowed_path(path: str) -> bool:
    p = path.split("?")[0]
    if is_blacklisted(p):
        return False
    return any(p.startswith(prefix) or f"/en{prefix}" in p or f"/zh{prefix}" in p for prefix in ALLOWED_PREFIXES)


def recommend_platforms(path: str) -> list[str]:
    for pattern, platforms in PLATFORM_RULES:
        if re.search(pattern, path, re.I):
            return platforms
    return ["medium"]


def tier(score: float) -> str:
    if score >= 75:
        return "S"
    if score >= 60:
        return "A"
    if score >= 45:
        return "B"
    return "C"


def trident_root() -> Path:
    env = os.environ.get("TRIDENT_ROOT")
    if env:
        return Path(env).expanduser()
    # 2026-09-14: derive from script location (Content Distribution/scripts/ -> project root)
    return Path(__file__).resolve().parents[2] / "1-4 Dev"


def load_ga_pages(input_path: Path | None, trident: Path) -> list[dict]:
    if input_path and input_path.exists():
        data = json.loads(input_path.read_text())
        return data if isinstance(data, list) else data.get("pages", data.get("rows", []))

    snap_dir = trident / "Output/Data Ingestion/monthly-snapshots"
    if snap_dir.exists():
        files = sorted(snap_dir.glob("ga4-pages-*.json"), reverse=True)
        if files:
            data = json.loads(files[0].read_text())
            return data if isinstance(data, list) else data.get("pages", [])

    return []


def sample_pages() -> list[dict]:
    return [
        {
            "pagePath": "/en/blog/ai-logo-design-guide",
            "sessions": 12400,
            "avg_engagement_time": 142,
            "engagement_rate": 0.58,
            "gsc_clicks_mom": 0.12,
            "non_brand_share": 0.72,
        },
        {
            "pagePath": "/en/tools/ai-logo-generator",
            "sessions": 8900,
            "avg_engagement_time": 95,
            "engagement_rate": 0.51,
            "gsc_clicks_mom": 0.08,
            "non_brand_share": 0.65,
        },
        {
            "pagePath": "/en/blog/lovart-vs-midjourney",
            "sessions": 6200,
            "avg_engagement_time": 178,
            "engagement_rate": 0.62,
            "gsc_clicks_mom": 0.15,
            "non_brand_share": 0.81,
        },
        {
            "pagePath": "/en/features/ai-poster-maker",
            "sessions": 3100,
            "avg_engagement_time": 88,
            "engagement_rate": 0.44,
            "gsc_clicks_mom": -0.02,
            "non_brand_share": 0.55,
        },
        {
            "pagePath": "/pricing",
            "sessions": 50000,
            "avg_engagement_time": 40,
            "engagement_rate": 0.3,
            "gsc_clicks_mom": 0.0,
            "non_brand_share": 0.1,
        },
    ]


def normalize_row(row: dict) -> dict | None:
    path = row.get("pagePath") or row.get("path") or row.get("page_path") or ""
    if not path or not allowed_path(path):
        return None

    sessions = float(row.get("sessions") or row.get("screenPageViews") or 0)
    eng_time = float(row.get("avg_engagement_time") or row.get("averageSessionDuration") or row.get("engagement_time") or 0)
    eng_rate = float(row.get("engagement_rate") or row.get("engagementRate") or 0)
    if eng_rate > 1:
        eng_rate /= 100.0
    gsc_mom = float(row.get("gsc_clicks_mom") or row.get("clicks_mom") or 0)
    nb_share = float(row.get("non_brand_share") or row.get("non_brand_query_share") or 0.5)

    slug = path.rstrip("/").split("/")[-1] or "page"
    canonical = f"https://lovart.ai{path}" if path.startswith("/") else path

    return {
        "pagePath": path,
        "canonical_url": canonical,
        "slug": slug,
        "sessions": sessions,
        "avg_engagement_time": eng_time,
        "engagement_rate": eng_rate,
        "gsc_clicks_mom": gsc_mom,
        "non_brand_share": nb_share,
    }


def score_pages(rows: list[dict]) -> list[dict]:
    normed = [normalize_row(r) for r in rows]
    items = [x for x in normed if x]
    if not items:
        return []

    for key in ("sessions", "avg_engagement_time", "engagement_rate", "gsc_clicks_mom", "non_brand_share"):
        vals = [float(i[key]) for i in items]
        for i in items:
            i[f"_norm_{key}"] = norm(vals, float(i[key]))

    weights = {
        "sessions": 0.35,
        "avg_engagement_time": 0.25,
        "engagement_rate": 0.20,
        "gsc_clicks_mom": 0.10,
        "non_brand_share": 0.10,
    }

    for i in items:
        i["score"] = round(
            sum(weights[k] * i[f"_norm_{k}"] * 100 for k in weights),
            1,
        )
        i["tier"] = tier(i["score"])
        i["recommended_platforms"] = recommend_platforms(i["pagePath"])
        i["track"] = "syndication" if i["tier"] in ("S", "A") else ("native" if i["tier"] == "B" else "skip")
        for k in list(i.keys()):
            if k.startswith("_norm_"):
                del i[k]

    items.sort(key=lambda x: x["score"], reverse=True)
    return items


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28, help="Lookback window (metadata only)")
    ap.add_argument("--sample", action="store_true", help="Use built-in sample data")
    ap.add_argument("--input", type=Path, help="GA pages JSON file")
    ap.add_argument("--top", type=int, default=10, help="Max candidates in output")
    args = ap.parse_args()

    trident = trident_root()
    if args.sample:
        raw = sample_pages()
        source = "sample"
    else:
        raw = load_ga_pages(args.input, trident)
        source = str(args.input) if args.input else str(trident / "Output/Data Ingestion/monthly-snapshots")

    if not raw:
        print("No GA page data found. Use --sample or --input PATH")
        print(f"TRIDENT_ROOT tried: {trident}")
        raise SystemExit(2)

    scored = score_pages(raw)
    candidates = [c for c in scored if c["tier"] != "C"][: args.top]

    today = date.today().isoformat()
    out_candidates = QUEUE_DIR / f"candidates-{today}.json"
    payload = {
        "generated_at": datetime.now().isoformat(),
        "lookback_days": args.days,
        "source": source,
        "trident_root": str(trident),
        "candidates": candidates,
    }
    out_candidates.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

    pending = {
        "updated": today,
        "items": [
            {
                "id": f"{c['slug']}-{today}",
                "canonical_url": c["canonical_url"],
                "tier": c["tier"],
                "score": c["score"],
                "platforms": c["recommended_platforms"][:2],
                "track": c["track"],
                "status": "pending_draft",
            }
            for c in candidates
            if c["tier"] in ("S", "A")
        ][:5],
    }
    (QUEUE_DIR / "pending.json").write_text(json.dumps(pending, indent=2, ensure_ascii=False) + "\n")

    print(f"Scored {len(scored)} pages, {len(candidates)} candidates (non-C)")
    print(f"Wrote {out_candidates}")
    print(f"Updated {QUEUE_DIR / 'pending.json'} ({len(pending['items'])} items)")
    for c in candidates[:5]:
        print(f"  [{c['tier']}] {c['score']:5.1f} {c['pagePath']} -> {','.join(c['recommended_platforms'][:3])}")


if __name__ == "__main__":
    main()
