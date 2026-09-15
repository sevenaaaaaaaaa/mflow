#!/usr/bin/env python3
"""月报 Draft/Full 数据完整度层（不修改 seo_report_standards 时的扩展 SSOT）。"""
from __future__ import annotations

DATA_TIER_DRAFT = "draft"
DATA_TIER_FULL = "full"
VALID_DATA_TIERS = (DATA_TIER_DRAFT, DATA_TIER_FULL)


def has_valid_dataworks(
    sgeo: dict | None,
    report_ym: str | None = None,
    datawork_dir=None,
) -> bool:
    """终稿条件：存在当月标准 xlsx 且快照含 natural all_uv。"""
    if report_ym and datawork_dir is not None:
        from pathlib import Path

        d = Path(datawork_dir)
        if not (d / f"{report_ym} SEO GEO.xlsx").is_file() and not (
            d / f"{report_ym} SEO GEO.xls"
        ).is_file():
            return False
    if not sgeo:
        return False
    if not sgeo.get("source_file"):
        return False
    nat = (sgeo.get("channel_totals") or {}).get("natural") or sgeo.get("natural") or {}
    return bool(nat.get("all_uv"))


def data_tier_watermark(
    data_tier: str,
    report_ym: str,
    sgeo_curr: dict | None,
    datawork_dir=None,
) -> str:
    if has_valid_dataworks(sgeo_curr, report_ym, datawork_dir) and data_tier == DATA_TIER_FULL:
        return "> **数据完整度**: Final v1（DataWorks 已接入）"
    if has_valid_dataworks(sgeo_curr, report_ym, datawork_dir):
        return "> **数据完整度**: Final v1（DataWorks 已接入）"
    return (
        f"> **数据完整度**: Draft v0（缺 DataWorks `{report_ym}`；"
        f"§二/§三 A·B/§六 为占位，补齐 xlsx 后 `--render-only --data-tier full` 升级）"
    )


def render_dataworks_placeholder_section(report_ym: str) -> str:
    return f"""
---

## 六、自然搜索产品数据（DataWorks 平台拆解）

> ⚠️ **Draft 占位** — 未找到 `1-2 Insight/From Datawork/{report_ym} SEO GEO.xlsx`。以下表格保留结构，待 DataWorks 补齐后重渲染。

### 6.1 渠道汇总（SEO / GEO / 合计）

| 渠道 | 访问 UV | 新增注册 | 新增付费 UV | 新增付费额 | 累计付费 UV |
|------|--------:|--------:|----------:|---------:|----------:|
| SEO | —（待 DataWorks） | — | — | — | — |
| GEO | —（待 DataWorks） | — | — | — | — |
| 合计 | —（待 DataWorks） | — | — | — | — |

### 6.2 SEO 搜索引擎 — Top 平台

| # | 平台 | UV | 新增注册 | 新增付费 | 新增→付费 |
|---|------|---:|--------:|--------:|----------:|
| — | —（待 DataWorks） | — | — | — | — |

### 6.3 GEO / AI 发现 — Top 平台

| # | 平台 | UV | 新增注册 | 新增付费 | 新增→付费 |
|---|------|---:|--------:|--------:|----------:|
| — | —（待 DataWorks） | — | — | — | — |

### 6.4 引擎对比 Google vs Bing(Microsoft)

| 指标 | Google | Bing(Microsoft) |
|------|--------|-------------------|
| 全漏斗 | —（待 DataWorks） | —（待 DataWorks） |

"""


def render_dau_draft_card(pl: str, cl: str) -> str:
    return f"""#### A. 全渠道 DAU 比例（DataWorks 日均）

> ⚠️ Draft 占位 — 待 DataWorks xlsx

| 渠道 | {pl} | {cl} | 环比 |
|------|-----:|-----:|------|
| SEO+GEO 合计 | —（待 DataWorks） | — | — |
| SEO | — | — | — |
| GEO | — | — | — |

"""


def render_product_draft_card(pl: str, cl: str) -> str:
    return f"""#### B. 自然搜索用户大盘数据（DataWorks）

> ⚠️ Draft 占位 — 待 DataWorks xlsx

| 指标 | {pl} | {cl} | 环比 |
|------|-----:|-----:|------|
| 访问 UV | —（待 DataWorks） | — | — |
| 新增注册 UV | — | — | — |
| 新增付费 UV | — | — | — |

"""


def monthly_post_run_checklist_draft() -> list[str]:
    return [
        "Draft 模式：文首含 Draft v0 水印",
        "§四～§十一 GSC+GA4+Bing 数据完整",
        "§六 含 DataWorks 占位表",
        "补齐 xlsx 后 --render-only --data-tier full 升级",
    ]
