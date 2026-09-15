#!/usr/bin/env python3
"""月报入口包装：调用 seo_monthly_v2 + Draft/Full 后处理（主脚本不可写时的替代 CLI）。"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SCRIPT_DIR))

from apply_draft_tier import process_file
from path_constants import MONTHLY_DIR
from seo_report_tier import DATA_TIER_DRAFT, DATA_TIER_FULL

PYTHON = sys.executable
MONTHLY = _SCRIPTS / "seo_monthly_v2.py"


def run(
    month: str,
    *,
    data_tier: str = DATA_TIER_DRAFT,
    resume: bool = False,
    render_only: bool = False,
    refresh_indexing: bool = False,
    refresh_brand: bool = False,
) -> None:
    cmd = [PYTHON, str(MONTHLY), "--month", month]
    if resume:
        cmd.append("--resume")
    if render_only:
        cmd.append("--render-only")
    if refresh_indexing:
        cmd.append("--refresh-indexing")
    if refresh_brand:
        cmd.append("--refresh-brand")
    try:
        subprocess.run(cmd, check=True, cwd=str(_SCRIPTS))
    except subprocess.CalledProcessError:
        if data_tier != DATA_TIER_DRAFT:
            raise
        out = MONTHLY_DIR / f"Lovart-SEO-{month}.md"
        if not out.is_file():
            raise
        print(f"  ⚠️ 月报生成有警告，继续 Draft 后处理: {month}")
    process_file(month, data_tier)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Monthly report with data-tier post-process")
    p.add_argument("--month", required=True)
    p.add_argument("--data-tier", default=DATA_TIER_DRAFT, choices=[DATA_TIER_DRAFT, DATA_TIER_FULL])
    p.add_argument("--resume", action="store_true")
    p.add_argument("--render-only", action="store_true")
    p.add_argument("--refresh-indexing", action="store_true")
    p.add_argument("--refresh-brand", action="store_true")
    args = p.parse_args()
    run(
        args.month,
        data_tier=args.data_tier,
        resume=args.resume,
        render_only=args.render_only,
        refresh_indexing=args.refresh_indexing,
        refresh_brand=args.refresh_brand,
    )
