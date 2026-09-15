#!/usr/bin/env python3
"""自然周批跑：monkey-patch 日期窗并输出 Lovart-SEO-Week_ 文件名。"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SCRIPTS))

try:
    from report_week_dates import build_natural_trend_windows, resolve_natural_week
except (ImportError, PermissionError):
    from week_dates_local import build_natural_trend_windows, resolve_natural_week  # type: ignore

from path_constants import TRIDENT

WEEKLY = TRIDENT / "reports" / "weekly"


def run_natural_week(week_anchor: str | None = None, gsc_lag: int = 2) -> Path:
    import weekly_review_v3 as w

    w.resolve_review_week = lambda *a, **kw: resolve_natural_week(week_anchor, gsc_lag)
    w.build_review_trend_windows = build_natural_trend_windows
    w.run_review_week(week_anchor, gsc_lag)

    GS, GE, _, _, _ = resolve_natural_week(week_anchor, gsc_lag)
    review_path = WEEKLY / f"Lovart-SEO-review-{GS}-{GE}.md"
    natural_path = WEEKLY / f"Lovart-SEO-Week_{GS}_{GE}.md"
    if review_path.is_file():
        text = review_path.read_text()
        text = text.replace("复盘周报", "自然周报").replace("复盘周", "自然周（周一~周日）")
        text = text.replace("最近4个复盘周趋势", "最近4个自然周趋势")
        natural_path.write_text(text)
        print(f"✅ {natural_path.name}")
        return natural_path
    raise FileNotFoundError(review_path)
