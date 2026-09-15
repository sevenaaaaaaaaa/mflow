#!/usr/bin/env python3
"""月报 Markdown 后处理：注入 Draft 水印 / §六 占位 / 校验 Final。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))
from seo_report_tier import (
    DATA_TIER_DRAFT,
    DATA_TIER_FULL,
    data_tier_watermark,
    has_valid_dataworks,
    render_dau_draft_card,
    render_dataworks_placeholder_section,
    render_product_draft_card,
)

from path_constants import DATAWORK_DIR, SNAPSHOT_DIR, TRIDENT


def load_sgeo(ym: str) -> dict | None:
    p = SNAPSHOT_DIR / f"seo-geo-{ym}.json"
    if p.is_file():
        try:
            return json.loads(p.read_text())
        except Exception:
            return None
    xlsx = DATAWORK_DIR / f"{ym} SEO GEO.xlsx"
    if xlsx.is_file():
        return {"source_file": str(xlsx.name)}
    return None


def _apply_section_two_three_draft(md: str, report_ym: str) -> str:
    """§二 OKR / §三 卡 A·B：缺 DataWorks 时插入 Draft 脚注或占位卡。"""
    note = (
        f"> ⚠️ **Draft** — 缺 DataWorks `{report_ym}`，"
        f"§二 OKR 产品 UV / §三 卡 A·B 为 GA4 参考或占位；终稿见 `--data-tier full`。\n\n"
    )
    anchor2 = "## 二、OKR 月达成看板"
    if anchor2 in md and "Draft" not in md.split(anchor2, 1)[1][:200]:
        md = md.replace(anchor2, f"{anchor2}\n\n{note}", 1)

    y, m = map(int, report_ym.split("-"))
    pl = f"{m - 1 if m > 1 else 12}月"
    cl = f"{m}月"
    for card_marker, renderer in (
        ("#### A. 全渠道 DAU 比例", render_dau_draft_card),
        ("#### B. 自然搜索用户大盘数据", render_product_draft_card),
    ):
        if card_marker in md and "待 DataWorks" not in md.split(card_marker, 1)[1][:400]:
            idx = md.find(card_marker)
            nxt = md.find("\n#### ", idx + 10)
            if nxt < 0:
                nxt = md.find("\n---", idx + 10)
            if nxt > idx:
                md = md[:idx] + renderer(pl, cl) + md[nxt:]
    return md


def _strip_data_tier_watermarks(md: str) -> str:
    lines = [ln for ln in md.split("\n") if not ln.startswith("> **数据完整度**")]
    return "\n".join(lines)


def _insert_watermark(md: str, wm: str) -> str:
    if wm in md:
        return md
    if "> **竞品词库**" in md:
        return md.replace("> **竞品词库**", f"{wm}\n> **竞品词库**", 1)
    if "> **周期**" in md:
        lines = md.split("\n")
        out_lines = []
        inserted = False
        for line in lines:
            out_lines.append(line)
            if not inserted and line.startswith("> **周期**"):
                out_lines.append(wm)
                inserted = True
        return "\n".join(out_lines)
    head = md.split("\n", 8)
    if any(re.match(r"^\*\*周期\*\*", ln) for ln in head):
        parts = md.split("\n", 1)
        rest = parts[1] if len(parts) > 1 else ""
        return f"{parts[0]}\n\n{wm}\n\n{rest.lstrip()}"
    lines = md.split("\n")
    if lines and lines[0].startswith("#"):
        i = 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        return "\n".join(lines[:i] + [wm, ""] + lines[i:])
    if "---" in md:
        return md.replace("---\n", f"---\n\n{wm}\n\n", 1)
    return f"{wm}\n\n{md}"


def apply_draft_to_report(md: str, report_ym: str, data_tier: str) -> str:
    sgeo = load_sgeo(report_ym)
    wm = data_tier_watermark(data_tier, report_ym, sgeo, DATAWORK_DIR)
    md = _strip_data_tier_watermarks(md)
    md = _insert_watermark(md, wm)

    if not has_valid_dataworks(sgeo, report_ym, DATAWORK_DIR) and data_tier == DATA_TIER_DRAFT:
        md = _apply_section_two_three_draft(md, report_ym)
        if "## 六、自然搜索产品数据" not in md or "待 DataWorks" not in md:
            placeholder = render_dataworks_placeholder_section(report_ym)
            if "## 六、自然搜索产品数据" in md:
                md = re.sub(
                    r"\n---\n\n## 六、自然搜索产品数据.*?(?=\n---\n\n## 七、)",
                    "\n" + placeholder + "\n",
                    md,
                    count=1,
                    flags=re.S,
                )
            else:
                anchor = "\n## 七、品牌词"
                if anchor in md:
                    md = md.replace(anchor, placeholder + anchor, 1)
    return md


def validate_full(report_ym: str) -> None:
    sgeo = load_sgeo(report_ym)
    if not has_valid_dataworks(sgeo, report_ym, DATAWORK_DIR):
        raise SystemExit(
            f"full 模式需要 DataWorks：请放入 {DATAWORK_DIR}/{report_ym} SEO GEO.xlsx "
            f"并运行 ingest，或先用 --data-tier draft"
        )


def process_file(report_ym: str, data_tier: str = DATA_TIER_DRAFT) -> Path:
    if data_tier == DATA_TIER_FULL:
        validate_full(report_ym)
    path = TRIDENT / "reports" / "monthly" / f"Lovart-SEO-{report_ym}.md"
    if not path.is_file():
        raise SystemExit(f"月报不存在: {path}")
    try:
        text = apply_draft_to_report(path.read_text(), report_ym, data_tier)
        path.write_text(text)
    except PermissionError as e:
        raise SystemExit(f"iCloud 文件未解锁，无法读写月报: {path}\n{e}") from e
    print(f"✅ tier={data_tier} {path.name}")
    return path


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--month", required=True)
    p.add_argument("--data-tier", default=DATA_TIER_DRAFT, choices=[DATA_TIER_DRAFT, DATA_TIER_FULL])
    args = p.parse_args()
    process_file(args.month, args.data_tier)
