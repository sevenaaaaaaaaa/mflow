#!/usr/bin/env python3
"""
双月报 V2：合并两月 GSC/GA4 快照 → 调用 seo_monthly_v2.generate_report。

对比规则（seo_report_standards COMPARE_BASELINE bimonthly）：
  本双月（连续两自然月）vs 上两自然月。
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS = _SCRIPT_DIR.parent
sys.path.insert(0, str(_SCRIPTS))
sys.path.insert(0, str(_SCRIPT_DIR))

from path_constants import BIMONTHLY_DIR, SNAPSHOT_DIR, TRIDENT
from snapshot_merge import (
    merge_bing_months,
    merge_ga4_snapshots,
    merge_gsc_snapshots,
    merge_sgeo_snapshots,
)
from seo_report_standards import bimonthly_post_run_checklist, print_pre_run_checklist

_BIMONTH_LABELS = ("1–2月", "3–4月", "5–6月", "7–8月", "9–10月", "11–12月")


def bimonth_months(year: int, b: int) -> list[str]:
    if not 1 <= b <= 6:
        raise ValueError(f"bimonth must be 1..6, got {b}")
    m1 = (b - 1) * 2 + 1
    return [f"{year}-{m1:02d}", f"{year}-{m1 + 1:02d}"]


def prev_bimonth(year: int, b: int) -> tuple[int, int]:
    if b == 1:
        return year - 1, 6
    return year, b - 1


def parse_bimonth_arg(s: str) -> tuple[int, int]:
    u = s.upper().strip()
    if "-B" in u:
        y, b = u.split("-B", 1)
        return int(y), int(b)
    y, m = s.split("-")
    return int(y), (int(m) - 1) // 2 + 1


def iter_bimonths(from_arg: str, to_arg: str) -> list[tuple[int, int]]:
    fy, fb = parse_bimonth_arg(from_arg)
    ty, tb = parse_bimonth_arg(to_arg)
    out: list[tuple[int, int]] = []
    y, b = fy, fb
    while (y, b) <= (ty, tb):
        out.append((y, b))
        b += 1
        if b > 6:
            b, y = 1, y + 1
    return out


def bimonth_meta(year: int, b: int) -> dict:
    months = bimonth_months(year, b)
    py, pb = prev_bimonth(year, b)
    prev_months = bimonth_months(py, pb)
    label = _BIMONTH_LABELS[b - 1]
    m1, m2 = int(months[0][5:7]), int(months[1][5:7])
    pm1, pm2 = int(prev_months[0][5:7]), int(prev_months[1][5:7])
    return {
        "report_ym": months[-1],
        "bimonth_id": f"{year}-B{b}",
        "bimonth_months": months,
        "bimonth_prev_months": prev_months,
        "title_year_month": f"{year}年 B{b}（{label}）",
        "report_heading": f"Lovart SEO 双月复盘报告 — {year}年 B{b}（{label}）",
        "perspective_line": "双月窗（连续两自然月 vs 上两自然月；结构同月报 V2）",
        "period_line": f"{months[0]}~{months[1]} (双月) vs {prev_months[0]}~{prev_months[1]} (上双月)",
        "prev_label": f"{pm1}–{pm2}月",
        "curr_label": f"{m1}–{m2}月",
        "prev_start": f"{prev_months[0]}-01",
        "prev_end": f"{prev_months[-1]}-28",
        "curr_start": f"{months[0]}-01",
        "curr_end": f"{months[-1]}-28",
        "footer_gsc": f"{prev_months[0]}~{prev_months[1]} vs {months[0]}~{months[1]}",
    }


def _load_period_snapshots(months: list[str], kind: str) -> list[dict]:
    from seo_monthly_v2 import load_ga4_from_legacy_cache, load_snapshot

    out: list[dict] = []
    missing: list[str] = []
    for ym in months:
        snap = load_snapshot(kind, ym)
        if snap is None and kind == "ga4":
            snap = load_ga4_from_legacy_cache(ym)
        if snap is None:
            missing.append(ym)
        else:
            out.append(snap)
    if missing:
        raise FileNotFoundError(
            f"缺 {kind} 快照 {missing}；请先 backfill-snapshots 或 render-monthly --render-only"
        )
    return out


def _load_sgeo_period(months: list[str]) -> dict:
    from lovart_seo_geo_metrics import ingest_for_month, load_seo_geo_snapshot

    snaps = []
    for ym in months:
        s = load_seo_geo_snapshot(ym)
        if s is None:
            s = ingest_for_month(ym)
        snaps.append(s)
    return merge_sgeo_snapshots(snaps)


def run_bimonthly_report(year: int, b: int, *, render_only: bool = True) -> Path:
    import seo_monthly_v2 as m
    from seo_monthly_extras import load_metrics_history, save_metrics_snapshot

    meta = bimonth_meta(year, b)
    months = meta["bimonth_months"]
    prev_months = meta["bimonth_prev_months"]

    print_pre_run_checklist(
        "bimonthly",
        meta["period_line"].split(" vs ")[0].strip(),
        meta["period_line"].split(" vs ")[1].strip(),
    )
    print(f"  ℹ️  双月报 render-only：合并快照 {months} vs {prev_months}\n")

    if not render_only:
        raise SystemExit("双月报当前仅支持 --render-only（从月快照合并；不直连 API）")

    print("[1/3] 加载并合并 GSC/GA4 快照...")
    g_curr = merge_gsc_snapshots(_load_period_snapshots(months, "gsc"))
    g_prev = merge_gsc_snapshots(_load_period_snapshots(prev_months, "gsc"))
    ga4_curr = merge_ga4_snapshots(_load_period_snapshots(months, "ga4"))
    ga4_prev = merge_ga4_snapshots(_load_period_snapshots(prev_months, "ga4"))

    m.refresh_keyword_brand_splits(g_curr)
    m.refresh_keyword_brand_splits(g_prev)
    m.rebuild_region_brand_lists(g_curr)
    m.rebuild_region_brand_lists(g_prev)

    print("[2/3] 分层 / 竞品 / Bing / DataWorks...")
    g_curr["brand_kw"], g_curr["nonbrand_kw"] = m.partition_keywords(g_curr["keywords"])
    g_prev["brand_kw"], g_prev["nonbrand_kw"] = m.partition_keywords(g_prev["keywords"])
    g_curr["tiers"] = m.compute_tiers(g_curr["keywords"], g_curr["brand_kw"], g_curr["nonbrand_kw"])
    g_prev["tiers"] = m.compute_tiers(g_prev["keywords"], g_prev["brand_kw"], g_prev["nonbrand_kw"])
    comp_curr = m.match_competitors(g_curr["nonbrand_kw"])
    comp_prev = m.match_competitors(g_prev["nonbrand_kw"])
    pdirs_prev = m.page_dir_analysis(g_prev["pages"])
    pdirs_curr = m.page_dir_analysis(g_curr["pages"])

    metrics_dir = TRIDENT / "reports" / "monthly" / ".metrics"
    hist = load_metrics_history(metrics_dir, m.OUT_DIR, months[-1])
    save_metrics_snapshot(metrics_dir, months[-1], g_curr, ga4_curr, comp_curr, pdirs_curr)

    sgeo_curr = _load_sgeo_period(months)
    sgeo_prev = _load_sgeo_period(prev_months)

    try:
        bing_data = json.loads((TRIDENT / "reports" / "bing-full.json").read_text())
    except Exception:
        bing_data = {}
    bing_curr = merge_bing_months(bing_data, months, build_bundle=m.build_bing_bundle)
    bing_prev = merge_bing_months(bing_data, prev_months, build_bundle=m.build_bing_bundle)

    print("[3/3] 生成双月 V2 报告（generate_report）...")
    report = m.generate_report(
        g_prev,
        g_curr,
        ga4_prev,
        ga4_curr,
        comp_prev,
        comp_curr,
        pdirs_prev,
        pdirs_curr,
        meta,
        hist,
        sgeo_prev=sgeo_prev,
        sgeo_curr=sgeo_curr,
        bing_prev_override=bing_prev,
        bing_curr_override=bing_curr,
    )

    BIMONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    out = BIMONTHLY_DIR / f"Lovart-SEO-{year}-B{b}.md"
    out.write_text(report)
    print(f"\n  📄 {out}")
    print(f"  📊 {len(report):,} chars, {len(report.splitlines())} lines")
    print("\n  双月报 V2 自检（seo_report_standards）：")
    for item in bimonthly_post_run_checklist():
        print(f"    [ ] {item}")
    print("\n✅ Done!")
    return out


def render_bimonth(year: int, b: int, tier: str = "draft") -> Path:
    """批处理入口（见 bimonth_with_tier.run）。"""
    from bimonth_with_tier import run

    run(year, b, data_tier=tier, render_only=True)
    return BIMONTHLY_DIR / f"Lovart-SEO-{year}-B{b}.md"
