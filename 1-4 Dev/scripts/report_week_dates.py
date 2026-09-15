#!/usr/bin/env python3
"""复盘周 / 自然周日期解析（周报 SSOT）。"""
from __future__ import annotations

from datetime import date, timedelta

GSC_LAG_DAYS = 2


def _md(d: date) -> str:
    return f"{d.month}/{d.day:02d}"


def latest_complete_review_tuesday(ref: date | None = None, gsc_lag: int = GSC_LAG_DAYS) -> date:
    ref = ref or date.today()
    candidate = ref if ref.weekday() == 1 else ref - timedelta(days=(ref.weekday() - 1) % 7)
    while (ref - candidate).days < gsc_lag:
        candidate -= timedelta(days=7)
    return candidate


def review_week_containing(anchor: date) -> date:
    if anchor.weekday() == 1:
        return anchor
    days_since_wed = (anchor.weekday() - 2) % 7
    wed = anchor - timedelta(days=days_since_wed)
    return wed + timedelta(days=6)


def resolve_review_week(
    week_anchor: str | None = None,
    gsc_lag: int = GSC_LAG_DAYS,
    ref: date | None = None,
) -> tuple[str, str, str, str, int]:
    ref = ref or date.today()
    if week_anchor:
        week_end = review_week_containing(date.fromisoformat(week_anchor))
    else:
        week_end = latest_complete_review_tuesday(ref, gsc_lag)
    week_start = week_end - timedelta(days=6)
    prev_end = week_start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=6)
    nd = (week_end - week_start).days + 1
    iso = lambda d: d.isoformat()
    return iso(week_start), iso(week_end), iso(prev_start), iso(prev_end), nd


def build_review_trend_windows(week_end: date) -> list[tuple[str, str, str]]:
    rows = []
    for i in range(3, -1, -1):
        te = week_end - timedelta(days=7 * i)
        ws = te - timedelta(days=6)
        rows.append((f"W{4 - i}\n{_md(ws)}-{_md(te)}", ws.isoformat(), te.isoformat()))
    return rows


def latest_complete_natural_sunday(ref: date | None = None, gsc_lag: int = GSC_LAG_DAYS) -> date:
    ref = ref or date.today()
    candidate = ref if ref.weekday() == 6 else ref - timedelta(days=(ref.weekday() + 1) % 7)
    while (ref - candidate).days < gsc_lag:
        candidate -= timedelta(days=7)
    return candidate


def natural_week_containing(anchor: date) -> date:
    if anchor.weekday() == 6:
        return anchor
    return anchor + timedelta(days=(6 - anchor.weekday()) % 7)


def resolve_natural_week(
    week_anchor: str | None = None,
    gsc_lag: int = GSC_LAG_DAYS,
    ref: date | None = None,
) -> tuple[str, str, str, str, int]:
    ref = ref or date.today()
    if week_anchor:
        week_end = natural_week_containing(date.fromisoformat(week_anchor))
    else:
        week_end = latest_complete_natural_sunday(ref, gsc_lag)
    week_start = week_end - timedelta(days=6)
    prev_end = week_start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=6)
    nd = 7
    iso = lambda d: d.isoformat()
    return iso(week_start), iso(week_end), iso(prev_start), iso(prev_end), nd


def build_natural_trend_windows(week_end: date) -> list[tuple[str, str, str]]:
    rows = []
    for i in range(3, -1, -1):
        te = week_end - timedelta(days=7 * i)
        ws = te - timedelta(days=6)
        rows.append((f"W{4 - i}\n{_md(ws)}-{_md(te)}", ws.isoformat(), te.isoformat()))
    return rows


def iter_review_weeks(start: date, end: date) -> list[tuple[str, str]]:
    """List (week_start, week_end) Tue-ended review weeks overlapping [start, end]."""
    out: list[tuple[str, str]] = []
    d = review_week_containing(start)
    while d <= end:
        ws = d - timedelta(days=6)
        if ws <= end:
            out.append((ws.isoformat(), d.isoformat()))
        d += timedelta(days=7)
    return out


def iter_natural_weeks(start: date, end: date) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    d = natural_week_containing(start)
    while d <= end:
        ws = d - timedelta(days=6)
        if ws <= end:
            out.append((ws.isoformat(), d.isoformat()))
        d += timedelta(days=7)
    return out


def month_range(from_ym: str, to_ym: str) -> list[str]:
    y1, m1 = map(int, from_ym.split("-"))
    y2, m2 = map(int, to_ym.split("-"))
    out = []
    y, m = y1, m1
    while (y, m) <= (y2, m2):
        out.append(f"{y}-{m:02d}")
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out
