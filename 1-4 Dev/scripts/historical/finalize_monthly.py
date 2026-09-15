#!/usr/bin/env python3
"""Phase 6：DataWorks 补齐后 ingest + 重渲染 Final 月报。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SCRIPTS))
sys.path.insert(0, str(_SCRIPT_DIR))

from apply_draft_tier import process_file
from seo_report_tier import DATA_TIER_FULL

PYTHON = sys.executable
MONTHLY = _SCRIPTS / "seo_monthly_v2.py"
INGEST = _SCRIPTS / "lovart_seo_geo_metrics.py"
from path_constants import DATAWORK_DIR, PROJECT


def finalize_month(ym: str, render_only: bool = True) -> None:
    validate_full_for_month(ym)
    if not render_only:
        subprocess.run([PYTHON, str(INGEST), "--month", ym], check=True, cwd=str(_SCRIPTS))
    tier_script = _SCRIPT_DIR / "monthly_with_tier.py"
    subprocess.run(
        [PYTHON, str(tier_script), "--month", ym, "--data-tier", DATA_TIER_FULL, "--render-only", "--resume"],
        check=True,
        cwd=str(_SCRIPT_DIR),
    )
    print(f"✅ Finalized {ym}")


def validate_full_for_month(ym: str) -> None:
    from apply_draft_tier import load_sgeo
    from seo_report_tier import has_valid_dataworks

    sgeo = load_sgeo(ym)
    if not has_valid_dataworks(sgeo, ym, DATAWORK_DIR):
        xlsx = DATAWORK_DIR / f"{ym} SEO GEO.xlsx"
        raise SystemExit(f"缺 DataWorks: {xlsx} — 放入后运行 lovart_seo_geo_metrics.py --month {ym}")


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--month", required=True)
    p.add_argument("--ingest", action="store_true")
    args = p.parse_args()
    finalize_month(args.month, render_only=not args.ingest)
