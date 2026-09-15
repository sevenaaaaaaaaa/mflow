#!/usr/bin/env python3
"""扫描历史数据覆盖，输出 reports/_inventory/history-coverage.json。"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent


def month_range(from_ym: str, to_ym: str) -> list[str]:
    y1, m1 = map(int, from_ym.split("-"))
    y2, m2 = map(int, to_ym.split("-"))
    out: list[str] = []
    y, m = y1, m1
    while (y, m) <= (y2, m2):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out

from path_constants import (
    BING_FULL,
    DATAWORK_DIR,
    INVENTORY_DIR,
    OUT_DIR,
    REPORTS,
    SNAPSHOT_DIR,
    TRIDENT,
)


def _has_snapshot(kind: str, ym: str) -> bool:
    if (SNAPSHOT_DIR / f"{kind}-{ym}.json").is_file():
        return True
    if kind == "gsc":
        legacy = OUT_DIR / f"gsc-5k-{ym}.json"
        return legacy.is_file()
    return False


def _has_dataworks(ym: str) -> bool:
    patterns = [
        DATAWORK_DIR / f"{ym} SEO GEO.xlsx",
        DATAWORK_DIR / f"{ym} SEO GEO.xls",
    ]
    return any(p.is_file() for p in patterns)


def _earliest_snapshot_month(kind: str) -> str | None:
    found: list[str] = []
    if SNAPSHOT_DIR.is_dir():
        for p in SNAPSHOT_DIR.glob(f"{kind}-20*.json"):
            try:
                ym = p.stem.split("-", 1)[1]
                if len(ym) == 7 and ym[4] == "-":
                    found.append(ym)
            except Exception:
                continue
    if kind == "gsc" and OUT_DIR.is_dir():
        for p in OUT_DIR.glob("gsc-5k-20*.json"):
            ym = p.stem.replace("gsc-5k-", "")
            if len(ym) == 7:
                found.append(ym)
    return min(found) if found else None


def _has_bing_month(ym: str, bing_data: dict | None) -> bool:
    if (SNAPSHOT_DIR / f"bing-{ym}.json").is_file():
        return True
    if not bing_data:
        return False
    return ym in (bing_data.get("keywords_monthly") or {})


def scan_coverage(from_ym: str, to_ym: str) -> dict:
    bing_data = None
    if BING_FULL.is_file():
        try:
            bing_data = json.loads(BING_FULL.read_text())
        except Exception:
            bing_data = {}

    weekly_dir = REPORTS / "weekly"
    weekly_review = list(weekly_dir.glob("Lovart-SEO-review-*.md")) if weekly_dir.is_dir() else []
    weekly_natural = list(weekly_dir.glob("Lovart-SEO-Week_*.md")) if weekly_dir.is_dir() else []
    daily_dir = REPORTS / "daily"

    months = {}
    for ym in month_range(from_ym, to_ym):
        months[ym] = {
            "gsc": _has_snapshot("gsc", ym),
            "ga4": _has_snapshot("ga4", ym),
            "seo_geo": _has_snapshot("seo-geo", ym),
            "bing": _has_bing_month(ym, bing_data),
            "dataworks_xlsx": _has_dataworks(ym),
            "rendered_monthly": (REPORTS / "monthly" / f"Lovart-SEO-{ym}.md").is_file(),
            "rendered_topics": len(list((REPORTS / "topics").glob(f"*-{ym}.md")))
            if (REPORTS / "topics").is_dir()
            else 0,
        }

    ref = date.today()
    api_earliest_hint = (ref.replace(day=1) - timedelta(days=16 * 31)).strftime("%Y-%m")
    earliest_gsc = _earliest_snapshot_month("gsc")
    earliest_ga4 = _earliest_snapshot_month("ga4")
    summary = {
        "months_with_gsc": sum(1 for v in months.values() if v["gsc"]),
        "months_with_ga4": sum(1 for v in months.values() if v["ga4"]),
        "months_with_dataworks": sum(1 for v in months.values() if v["dataworks_xlsx"]),
        "months_rendered_monthly": sum(1 for v in months.values() if v["rendered_monthly"]),
        "months_ready_draft": sum(
            1 for v in months.values() if v["gsc"] and v["ga4"] and v["rendered_monthly"]
        ),
    }

    return {
        "generated": date.today().isoformat(),
        "range": {"from": from_ym, "to": to_ym},
        "api_earliest_hint_gsc_16mo": api_earliest_hint,
        "api_earliest_actual_gsc": earliest_gsc,
        "api_earliest_actual_ga4": earliest_ga4,
        "summary": summary,
        "paths": {
            "snapshots": str(SNAPSHOT_DIR),
            "dataworks": str(DATAWORK_DIR),
            "monthly_reports": str(REPORTS / "monthly"),
            "weekly_reports": str(weekly_dir),
        },
        "counts": {
            "review_weekly_md": len(weekly_review),
            "natural_weekly_md": len(weekly_natural),
            "daily_md": len(list(daily_dir.glob("*.md"))) if daily_dir.is_dir() else 0,
        },
        "months": months,
    }


def main(from_ym: str = "2025-01", to_ym: str | None = None) -> Path:
    to_ym = to_ym or date.today().strftime("%Y-%m")
    INVENTORY_DIR.mkdir(parents=True, exist_ok=True)
    data = scan_coverage(from_ym, to_ym)
    out = INVENTORY_DIR / "history-coverage.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"✅ {out} ({len(data['months'])} months)")
    return out


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Scan SEO data coverage")
    p.add_argument("--from", dest="from_ym", default="2025-01")
    p.add_argument("--to", dest="to_ym", default=None)
    args = p.parse_args()
    main(args.from_ym, args.to_ym)
