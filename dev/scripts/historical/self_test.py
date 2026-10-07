#!/usr/bin/env python3
"""离线自检（不依赖 API / 不强制写 reports）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from apply_draft_tier import apply_draft_to_report
from report_inventory import scan_coverage
from seo_report_tier import DATA_TIER_DRAFT
from week_dates_local import iter_natural_weeks, iter_review_weeks, month_range


def test_draft_watermark() -> None:
    md = "# Test\n\n> **周期**: 2025-03\n\n---\n\n## 七、品牌词\n"
    out = apply_draft_to_report(md, "2025-03", DATA_TIER_DRAFT)
    assert "Draft v0" in out
    assert "待 DataWorks" in out
    print("  ✓ draft watermark + §六 placeholder")


def test_month_range() -> None:
    assert month_range("2025-11", "2026-02") == ["2025-11", "2025-12", "2026-01", "2026-02"]
    print("  ✓ month_range")


def test_week_iters() -> None:
    from datetime import date

    rw = iter_review_weeks(date(2026, 1, 1), date(2026, 1, 31))
    nw = iter_natural_weeks(date(2026, 1, 1), date(2026, 1, 31))
    assert rw and nw
    print(f"  ✓ week iters review={len(rw)} natural={len(nw)}")


def test_inventory_schema() -> None:
    data = scan_coverage("2025-01", "2026-06")
    assert "months" in data and "summary" in data
    assert "api_earliest_actual_gsc" in data
    print(f"  ✓ inventory schema ({data['summary']['months_with_gsc']} gsc months)")


def main() -> None:
    print("historical self_test")
    test_month_range()
    test_week_iters()
    test_draft_watermark()
    test_inventory_schema()
    print("✅ all passed")


if __name__ == "__main__":
    main()
