#!/usr/bin/env python3
"""季报：从月快照聚合，不直连 API。"""
from __future__ import annotations

import json
from calendar import monthrange
from datetime import date
from pathlib import Path

from path_constants import OUT_DIR, QUARTERLY_DIR, SNAPSHOT_DIR, TRIDENT

QUARTERLY_DIR.mkdir(parents=True, exist_ok=True)


def _quarter_months(year: int, q: int) -> list[str]:
    start_m = (q - 1) * 3 + 1
    return [f"{year}-{start_m + i:02d}" for i in range(3)]


def _prev_quarter(year: int, q: int) -> tuple[int, int]:
    if q == 1:
        return year - 1, 4
    return year, q - 1


def _load_gsc_summary(ym: str) -> dict | None:
    for p in (SNAPSHOT_DIR / f"gsc-{ym}.json", OUT_DIR / f"gsc-5k-{ym}.json"):
        if not p.is_file():
            continue
        try:
            d = json.loads(p.read_text())
        except PermissionError:
            return None
        tiers = d.get("tiers") or {}
        clicks = d.get("total_clicks")
        if clicks is None:
            clicks = tiers.get("_total_clicks") or sum(
                k.get("clicks", 0) for k in d.get("keywords") or []
            )
        impr = d.get("total_impr") or tiers.get("_total_impr", 0)
        brand = tiers.get("品牌词") if isinstance(tiers.get("品牌词"), dict) else {}
        brand_share = brand.get("share")
        if brand_share is None and clicks:
            bcl = sum(k.get("clicks", 0) for k in d.get("brand_kw") or [])
            brand_share = round(bcl / clicks * 100, 1)
        return {
            "clicks": clicks or 0,
            "impr": impr or 0,
            "brand_share": brand_share if brand_share is not None else 0,
        }
    return None


def render_quarter(year: int, quarter: int, tier: str = "draft") -> Path:
    months = _quarter_months(year, quarter)
    py, pq = _prev_quarter(year, quarter)
    prev_months = _quarter_months(py, pq)

    rows_curr, rows_prev = [], []
    for ym in months:
        s = _load_gsc_summary(ym)
        rows_curr.append((ym, s or {}))
    for ym in prev_months:
        s = _load_gsc_summary(ym)
        rows_prev.append((ym, s or {}))

    def sum_clicks(rows):
        return sum((r[1].get("clicks") or 0) for r in rows)

    c_curr, c_prev = sum_clicks(rows_curr), sum_clicks(rows_prev)
    chg = "—"
    if c_prev:
        d = c_curr - c_prev
        chg = f"{'↑' if d>0 else '↓'}{d:+,} / {d/c_prev*100:.1f}%"

    trend_lines = ["| 月 | GSC 点击 | 品牌占比 |", "|---|---:|---:|"]
    for ym, s in rows_curr:
        trend_lines.append(f"| {ym} | {(s.get('clicks') or 0):,} | {s.get('brand_share', '—')}% |")

    report = f"""# Lovart SEO 季度报告 — {year}年Q{quarter}

> **周期**: {months[0]} ~ {months[-1]} vs {prev_months[0]} ~ {prev_months[-1]}  
> **生成**: {date.today().isoformat()}  
> **数据完整度**: {tier}（季报由月快照聚合；产品漏斗见各月报 §六）

---

## OKR 季度达成看板（GSC 代理）

| 指标 | 上季合计 | 本季合计 | 环比 |
|------|--------:|--------:|------|
| GSC 点击 | {c_prev:,} | {c_curr:,} | {chg} |

## 本季逐月趋势

{chr(10).join(trend_lines)}

## 章节索引

- 关键词/品牌/竞品/页面/地区：见各月专题报告 `reports/topics/`
- 月报全文：`reports/monthly/Lovart-SEO-YYYY-MM.md`
- 双月报（两月 vs 上两月）：`reports/bimonthly/Lovart-SEO-YYYY-Bn.md`

## TODO

| 优先级 | 行动项 |
|--------|--------|
| P1 | 补齐 DataWorks 后重跑月报 Final，再刷新季报 |
| P2 | 对照 SKILL 季报模板补 GA4 逐月与会话质量表 |

"""
    out = QUARTERLY_DIR / f"Lovart-SEO-{year}-Q{quarter}.md"
    out.write_text(report)
    print(f"✅ {out}")
    return out
