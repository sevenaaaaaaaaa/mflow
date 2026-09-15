#!/usr/bin/env python3
"""年报与整体史报告：从月快照聚合。"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from path_constants import ANNUAL_DIR, LIFETIME_DIR, OUT_DIR, SNAPSHOT_DIR

ANNUAL_DIR.mkdir(parents=True, exist_ok=True)
LIFETIME_DIR.mkdir(parents=True, exist_ok=True)


def _load_gsc(ym: str) -> int:
    for p in (SNAPSHOT_DIR / f"gsc-{ym}.json", OUT_DIR / f"gsc-5k-{ym}.json"):
        if p.is_file():
            try:
                d = json.loads(p.read_text())
                t = d.get("tiers") or d
                return int(t.get("_total_clicks") or 0)
            except PermissionError:
                return 0
    return 0


def render_year(year: int, tier: str = "draft") -> Path:
    months = [f"{year}-{m:02d}" for m in range(1, 13)]
    clicks = [(ym, _load_gsc(ym)) for ym in months]
    total = sum(c for _, c in clicks)
    prev_total = sum(_load_gsc(f"{year-1}-{m:02d}") for m in range(1, 13))

    lines = ["| 月 | GSC 点击 |", "|---|---:|"]
    for ym, c in clicks:
        lines.append(f"| {ym} | {c:,} |")

    yoy = "—"
    if prev_total:
        d = total - prev_total
        yoy = f"{'↑' if d>0 else '↓'}{d:+,} / {d/prev_total*100:.1f}%"

    report = f"""# Lovart SEO 年度复盘报告 — {year}

> **生成**: {date.today().isoformat()}  
> **数据完整度**: {tier}  
> **同比**: {year} vs {year-1} GSC 点击 {yoy}

---

## 全年 GSC 点击趋势

{chr(10).join(lines)}

| 全年合计 | {year-1} | {year} | 同比 |
|----------|--------:|--------:|------|
| GSC 点击 | {prev_total:,} | {total:,} | {yoy} |

## 战略索引

- 月报：`reports/monthly/`
- 双月报：`reports/bimonthly/`
- 季报：`reports/quarterly/`
- 专题：`reports/topics/`
- 整体史：`reports/lifetime/`

"""
    out = ANNUAL_DIR / f"Lovart-SEO-{year}.md"
    out.write_text(report)
    _render_lifetime_appendix(year, clicks, tier)
    print(f"✅ {out}")
    return out


def _render_lifetime_appendix(latest_year: int, series: list, tier: str) -> None:
    """跨所有可用月份的 KPI 曲线附录。"""
    all_months = []
    for y in range(latest_year - 1, latest_year + 1):
        for m in range(1, 13):
            ym = f"{y}-{m:02d}"
            c = _load_gsc(ym)
            if c:
                all_months.append((ym, c))
    lines = ["| 月 | GSC 点击 |", "|---|---:|"]
    for ym, c in all_months:
        lines.append(f"| {ym} | {c:,} |")
    report = f"""# Lovart SEO 整体史报告 — 截至 {date.today().isoformat()}

> **数据完整度**: {tier}  
> Part A：可用月 GSC 点击曲线（来自月快照）  
> Part B：收录/竞品/双引擎详见各月报与专题  
> Part C：DataWorks 可用月的转化漏斗见月报 §六（缺则 Draft）

---

## Part A — KPI 曲线

{chr(10).join(lines)}

## Part B — 演进主题（手工索引）

- 收录率演进：见月报 §三 卡 F、`topics/indexing-*`
- 品牌依赖：见 `topics/keywords-brand-*`
- Google vs Bing：见 `topics/dual-engine-*`

## Part C — DataWorks 覆盖

见 `reports/_inventory/history-coverage.json` 的 `dataworks_xlsx` 字段。

"""
    out = LIFETIME_DIR / f"Lovart-SEO-lifetime-{date.today().isoformat()}.md"
    out.write_text(report)
    print(f"✅ {out}")
