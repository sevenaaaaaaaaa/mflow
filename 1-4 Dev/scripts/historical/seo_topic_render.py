#!/usr/bin/env python3
"""从月报/快照拆出维度专题报告（6 类）。"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from path_constants import MONTHLY_DIR, SNAPSHOT_DIR, TOPICS_DIR

TOPIC_SPECS = (
    ("keywords-brand", "关键词与品牌非品牌", ("## 四、关键词", "## 五、自然搜索")),
    ("competitor", "竞品非品牌词覆盖", ("## 八、竞品", "## 九、页面")),
    ("pages", "页面目录与 Top", ("## 九、页面目录", "## 十一、分地区")),
    ("regions", "分地区 GSC+GA4", ("## 十一、分地区", "## 十二、TODO")),
    ("dual-engine", "Google vs Bing 双引擎", ("## 四、关键词", "## 五、自然搜索")),
    ("indexing", "收录与索引", ("### F.", "## 四、关键词")),
)


def _extract_section(md: str, start: str, end: str) -> str:
    i = md.find(start)
    if i < 0:
        return f"> 月报中未找到 `{start}`\n"
    j = md.find(end, i + len(start))
    if j < 0:
        return md[i:]
    return md[i:j]


def _dual_engine_excerpt(md: str) -> str:
    parts = []
    for marker in ("4.16", "C-Bing", "§13", "十三、Bing", "11.10"):
        if marker in md:
            idx = md.find(marker)
            parts.append(md[idx : idx + 2500])
    return "\n\n---\n\n".join(parts[:4]) if parts else "> 无双引擎块\n"


def _indexing_excerpt(md: str, ym: str) -> str:
    chunk = _extract_section(md, "## 三、SEO Dashboard", "## 四、")
    ix = SNAPSHOT_DIR / f"indexing-{ym}.json"
    extra = ""
    if ix.is_file():
        try:
            d = json.loads(ix.read_text())
            extra = f"\n\n收录快照：`indexing-{ym}.json` — indexed {d.get('pages_with_traffic', '—')}\n"
        except Exception:
            pass
    return chunk + extra


def render_topic(ym: str, slug: str, title: str, start: str, end: str) -> Path:
    monthly = MONTHLY_DIR / f"Lovart-SEO-{ym}.md"
    if not monthly.is_file():
        raise FileNotFoundError(f"缺月报 {monthly}")
    md = monthly.read_text()
    if slug == "dual-engine":
        body = _dual_engine_excerpt(md)
    elif slug == "indexing":
        body = _indexing_excerpt(md, ym)
    else:
        body = _extract_section(md, start, end)

    report = f"""# Lovart SEO 专题 — {title} — {ym}

> **来源**: [Lovart-SEO-{ym}.md](../monthly/Lovart-SEO-{ym}.md)  
> **生成**: {date.today().isoformat()}  
> **类型**: 维度专题（从月报拆片，无新 API）

---

{body}
"""
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    out = TOPICS_DIR / f"Lovart-SEO-topic-{slug}-{ym}.md"
    out.write_text(report)
    print(f"  topic {out.name}")
    return out


def render_all_topics(ym: str) -> list[Path]:
    return [render_topic(ym, slug, title, start, end) for slug, title, (start, end) in TOPIC_SPECS]
