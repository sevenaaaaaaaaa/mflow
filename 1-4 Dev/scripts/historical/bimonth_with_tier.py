#!/usr/bin/env python3
"""双月报 + Draft/Full 后处理。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from apply_draft_tier import apply_draft_to_report, load_sgeo
from path_constants import BIMONTHLY_DIR, DATAWORK_DIR
from seo_bimonthly import bimonth_months, run_bimonthly_report
from seo_report_tier import DATA_TIER_DRAFT, DATA_TIER_FULL, has_valid_dataworks


def run(year: int, b: int, *, data_tier: str = DATA_TIER_DRAFT, render_only: bool = True) -> None:
    months = bimonth_months(year, b)
    try:
        run_bimonthly_report(year, b, render_only=render_only)
    except FileNotFoundError:
        raise

    path = BIMONTHLY_DIR / f"Lovart-SEO-{year}-B{b}.md"
    tier = data_tier
    if data_tier == DATA_TIER_FULL and not all(
        has_valid_dataworks(load_sgeo(ym), ym, DATAWORK_DIR) for ym in months
    ):
        raise SystemExit(
            f"full 需要两月 DataWorks xlsx：{months[0]} / {months[1]}"
        )

    text = apply_draft_to_report(path.read_text(), months[-1], tier)
    # 双月 Draft 水印注明两月 xlsx
    if tier == DATA_TIER_DRAFT and not all(
        has_valid_dataworks(load_sgeo(ym), ym, DATAWORK_DIR) for ym in months
    ):
        old = f"缺 DataWorks `{months[-1]}`"
        new = f"缺 DataWorks `{months[0]}` / `{months[1]}`"
        text = text.replace(old, new)
    path.write_text(text)
    print(f"✅ tier={tier} {path.name}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--year", type=int, required=True)
    p.add_argument("--b", type=int, required=True, help="1..6")
    p.add_argument("--data-tier", default=DATA_TIER_DRAFT, choices=[DATA_TIER_DRAFT, DATA_TIER_FULL])
    args = p.parse_args()
    run(args.year, args.b, data_tier=args.data_tier)
