#!/usr/bin/env python3
"""preflight_tools_page_rewrite.py — landing-page-grade gate for Tools full-page rewrites.

Aligns with lovart-landing-page + COPY-PREFLIGHT.md. Use before patching bodyJson/TDK.

Usage:
  python3 preflight_tools_page_rewrite.py --file page.json
  python3 preflight_tools_page_rewrite.py --ndjson batch.ndjson --strict

Exit: 0 pass, 1 BLOCK
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Reuse TDK language gate
sys.path.insert(0, str(Path(__file__).resolve().parent))
from preflight_tdk_i18n import check_page as check_tdk  # noqa: E402

BRAND_PLACEHOLDER = re.compile(r"__品牌\d+__|__BRAND\d+__")
EN_BOILER = re.compile(
    r"\b(Create professional|Use Lovart'?s AI design agent for|Professional Design Tool|"
    r"in seconds with|From concept to finished asset|One agent\. Every creative surface)\b",
    re.I,
)
MIXED_SHELL = re.compile(
    r"通过 Lovart AI|透過Lovart AI|通过Lovart AI|Lovart AI 디자인|Lovart AIデザインエージェントで作成|"
    r"MCoT发动机|MCoT 引擎최적화|品牌意识输出",
)
IMAGE_BAD = re.compile(r"IMAGE PLACEHOLDER|\[REAL SCREENSHOT REQUIRED\]")
SLUG_DUMP = re.compile(r"for ai [a-z0-9-]+|ai content repurposer task", re.I)
MIN_DESC = {
    "en": 120,
    "de": 120,
    "fr": 120,
    "it": 120,
    "pt": 120,
    "ru": 120,
    "ja": 90,
    "ko": 90,
    "zh": 80,
    "zh-TW": 80,
}


def body_sections(page: dict) -> list[dict]:
    raw = page.get("bodyJson")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return []
    return raw if isinstance(raw, list) else []


def hero_section(sections: list[dict]) -> dict:
    for sec in sections[:5]:
        if isinstance(sec, dict) and str(sec.get("type", "")).lower().startswith("hero"):
            return sec
    return sections[0] if sections and isinstance(sections[0], dict) else {}


def all_strings(obj) -> list[str]:
    out: list[str] = []

    def walk(v):
        if isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, str) and v.strip():
            out.append(v.strip())

    walk(obj)
    return out


def check_page(page: dict, strict: bool = True) -> list[dict]:
    issues: list[dict] = []
    lang = page.get("language") or "en"
    sections = body_sections(page)
    joined = "\n".join(all_strings(page))

    def block(code: str, field: str, reason: str, sample: str = "") -> None:
        issues.append(
            {
                "code": code,
                "severity": "BLOCK",
                "field": field,
                "language": lang,
                "reason": reason,
                "sample": sample[:120],
                "id": page.get("_id") or page.get("id") or page.get("slug"),
            }
        )

    if page.get("category") != "tool":
        block("TOOLS_RW_CATEGORY", "category", "not_tool")
    if page.get("schemaVersion") != "composite-v2":
        block("TOOLS_RW_SCHEMA", "schemaVersion", "not_composite_v2")
    if not sections:
        block("TOOLS_RW_BODY", "bodyJson", "empty_or_invalid_body")
        return issues

    legacy = [s.get("type") for s in sections if isinstance(s, dict) and str(s.get("type", "")).endswith("Section")]
    if legacy:
        block("TOOLS_RW_LEGACY", "bodyJson", "legacy_section_types", ",".join(legacy[:3]))

    if BRAND_PLACEHOLDER.search(joined):
        block("TOOLS_RW_PLACEHOLDER", "bodyJson", "brand_placeholder")
    if EN_BOILER.search(joined):
        block("TOOLS_RW_EN_BOILER", "bodyJson", "english_boilerplate")
    if MIXED_SHELL.search(joined):
        block("TOOLS_RW_MIXED_SHELL", "bodyJson", "mixed_language_shell")
    if IMAGE_BAD.search(joined):
        block("TOOLS_RW_IMAGE", "bodyJson", "image_placeholder")
    if SLUG_DUMP.search(joined):
        block("TOOLS_RW_SLUG_DUMP", "bodyJson", "slug_dump_copy")

    hero = hero_section(sections)
    ht = str(hero.get("title") or page.get("title") or "")
    hd = str(hero.get("description") or page.get("description") or "")
    if len(hd) < MIN_DESC.get(lang, 120):
        block("TOOLS_RW_HERO_SHORT", "hero.description", "hero_description_too_short", hd)
    if not any(k in hd.lower() for k in ("输入", "输出", "input", "output", "upload", "上传", "生成", "export", "导出")):
        if lang in ("en", "de", "fr", "it", "pt", "ru") and not re.search(r"\b(from|turn|upload|export|generate)\b", hd, re.I):
            block("TOOLS_RW_HERO_IO", "hero.description", "hero_missing_input_or_output", hd)
        if lang in ("zh", "zh-TW", "ja", "ko") and not re.search(
            r"(输入|输出|入力|出力|上传|上傳|アップロード|書き出し|生成|导出|匯出|から|업로드|내보내)",
            hd,
        ):
            block("TOOLS_RW_HERO_IO", "hero.description", "hero_missing_input_or_output", hd)

    faq = next((s for s in sections if isinstance(s, dict) and s.get("type") == "faq"), None)
    faq_items = faq.get("items") if isinstance(faq, dict) else None
    if not isinstance(faq_items, list) or len(faq_items) < 3:
        block("TOOLS_RW_FAQ", "faq.items", "faq_lt_3")
    else:
        weak = sum(
            1
            for it in faq_items
            if isinstance(it, dict) and len(str(it.get("answer") or "")) < 40
        )
        if weak >= 2:
            block("TOOLS_RW_FAQ_WEAK", "faq.items", "faq_answers_too_thin")

    cta = any(isinstance(s, dict) and s.get("type") == "cta-default" for s in sections)
    if not cta:
        block("TOOLS_RW_CTA", "bodyJson", "missing_cta_default")

    # Only sections that normally carry a narrative `description` at section level.
    desc_types = {
        "hero-split",
        "hero-cinematic",
        "bento-2",
        "bento-4",
        "prompt-launcher",
        "workflow-horizontal",
        "workflow-vertical",
        "feature-detail",
        "cluster-block-dense",
        "cta-default",
    }
    thin = 0
    content_secs = 0
    for sec in sections:
        if not isinstance(sec, dict):
            continue
        st = sec.get("type")
        if st not in desc_types:
            continue
        content_secs += 1
        if len(str(sec.get("description") or "")) < 35:
            thin += 1
    if content_secs and thin / content_secs >= 0.55:
        block("TOOLS_RW_THIN", "bodyJson", "mostly_thin_sections")

    seo = page.get("seo") or {}
    if str(page.get("title") or "") != str(seo.get("title") or page.get("title") or ""):
        if seo.get("title") and page.get("title") and seo.get("title") != page.get("title"):
            block("TOOLS_RW_TDK_SYNC", "seo.title", "title_seo_out_of_sync")
    if seo.get("description") and page.get("description") and seo.get("description") != page.get("description"):
        block("TOOLS_RW_TDK_SYNC", "seo.description", "description_seo_out_of_sync")

    for row in check_tdk(page, strict=strict):
        if row.get("severity") == "BLOCK":
            issues.append({**row, "code": "TOOLS_RW_" + row.get("code", "TDK")})

    return issues


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--ndjson")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)
    pages: list[dict] = []
    if args.file:
        pages.append(json.loads(Path(args.file).read_text(encoding="utf-8")))
    elif args.ndjson:
        for line in Path(args.ndjson).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                pages.append(json.loads(line))
    else:
        ap.print_help()
        return 2

    blocks = 0
    for page in pages:
        for issue in check_page(page, strict=args.strict):
            if issue.get("severity") == "BLOCK":
                blocks += 1
                print(json.dumps(issue, ensure_ascii=False))

    print(f"TOOLS_REWRITE pages={len(pages)} BLOCK={blocks}")
    return 1 if blocks else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
