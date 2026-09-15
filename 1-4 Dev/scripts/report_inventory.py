#!/usr/bin/env python3
"""扫描历史数据覆盖，输出 reports/_inventory/history-coverage.json。"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from report_week_dates import month_range

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT = _SCRIPT_DIR.parents[1]
SNAPSHOT_DIR = _PROJECT / "1-4 Dev/Output/Data Ingestion/monthly-snapshots"
DATAWORK_DIR = _PROJECT / "1-2 Insight/From Datawork"
TRIDENT = _PROJECT / "1-2 Insight/Trident Insights"
REPORTS = TRIDENT / "reports"
INVENTORY_DIR = REPORTS / "_inventory"
BING_FULL = REPORTS / "bing-full.json"


def _has_snapshot(kind: str, ym: str) -> bool:
    return (SNAPSHOT_DIR / f"{kind}-{ym}.json").is_file()


def _has_dataworks(ym: str) -> bool:
  patterns = [
      DATAWORK_DIR / f"{ym} SEO GEO.xlsx",
      DATAWORK_DIR / f"{ym} SEO GEO.xls",
  ]
  return any(p.is_file() for p in patterns)


def _has_bing_month(ym: str, bing_data: dict | None) -> bool:
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

    weekly_review = list((REPORTS / "weekly").glob("Lovart-SEO-review-*.md")) if (REPORTS / "weekly").is_dir() else []
    weekly_natural = list((REPORTS / "weekly").glob("Lovart-SEO-Week_*.md")) if (REPORTS / "weekly").is_dir() else []
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
            "rendered_topics": len(list((REPORTS / "topics").glob(f"*-{ym}.md"))) if (REPORTS / "topics").is_dir() else 0,
        }

    ref = date.today()
    api_earliest_hint = (ref.replace(day=1) - timedelta(days=16 * 31)).strftime("%Y-%m")

    return {
        "generated": date.today().isoformat(),
        "range": {"from": from_ym, "to": to_ym},
        "api_earliest_hint_gsc_16mo": api_earliest_hint,
        "paths": {
            "snapshots": str(SNAPSHOT_DIR),
            "dataworks": str(DATAWORK_DIR),
            "monthly_reports": str(REPORTS / "monthly"),
            "weekly_reports": str(REPORTS / "weekly"),
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
