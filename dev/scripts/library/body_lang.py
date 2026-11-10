# -*- coding: utf-8 -*-
"""body_lang.py — bodyJson language / placeholder gate (shared).

detect/check the body text of a composite page against its declared language.
Used by preflight_tdk_i18n.py, tdk_report.py and sanity_publisher.publish_composite().
"""
from __future__ import annotations

import json
import re

HAN = re.compile(r"[\u4e00-\u9fff]")
KANA = re.compile(r"[\u3040-\u30ff]")
HANGUL = re.compile(r"[\uac00-\ud7af]")
CYRILLIC = re.compile(r"[\u0400-\u04FF]")
LATIN_WORD = re.compile(r"[A-Za-z]{2,}")
PLACEHOLDER = re.compile(r"__品牌\d+__|\{\{[^}]{1,40}\}\}|%s|\$pt\b|\{\{brand\}\}")
LEAK = re.compile(r"核心矩陣|P1 爆發|Bing 發現|关键词矩阵|GSC 曝光|曝光最高的页面|内部矩阵")

BRAND_TERMS = re.compile(
    r"(Lovart|MCoT|ChatCanvas|Touch Edit|Text Edit|Brand Kit|Nano Banana Pro?|Nano Banana 2|Seedance|Seedream|Flux|Midjourney|OpenAI|Photoshop|Figma|Canva|YouTube|TikTok|Instagram|Pinterest|Twitter|LinkedIn|AWS|API|SVG|PNG|JPG|PDF|GSC|SEO|CRO|UGC|AI|UI|UX)",
    re.I,
)

LATIN_LANGS = ("en", "de", "fr", "it", "pt", "es")
CJK_LANGS = ("ja", "ko", "zh", "zh-TW")


def body_text(body) -> str:
    """Flatten bodyJson (string or list) into one searchable text."""
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            return body
    if not isinstance(body, list):
        return ""
    out = []

    def walk(node):
        if isinstance(node, str):
            out.append(node)
        elif isinstance(node, list):
            for n in node:
                walk(n)
        elif isinstance(node, dict):
            for k, v in node.items():
                if k in ("src", "href", "step", "type", "variant", "@type"):
                    continue
                walk(v)

    walk(body)
    return " ".join(out)


def check_body(lang: str, body) -> list[str]:
    """Return reason codes; empty list = pass."""
    if not body:
        return []
    text = body_text(body)
    if not text.strip():
        return []
    reasons = []
    han = len(HAN.findall(text))
    kana = len(KANA.findall(text))
    hangul = len(HANGUL.findall(text))
    cyr = len(CYRILLIC.findall(text))
    latin = len(LATIN_WORD.findall(text))
    cjk = han + kana + hangul
    latin_chars = len(re.findall(r"[A-Za-z]", text))

    if PLACEHOLDER.search(text):
        reasons.append("placeholder")
    if LEAK.search(text):
        reasons.append("internal_leak")

    if lang in LATIN_LANGS:
        # Non-Latin body on a Latin-language page.
        if cjk >= 20 and (cjk / max(1, cjk + latin_chars)) > 0.05:
            reasons.append("cjk_body")
        if lang == "en" and han > 20:
            reasons.append("han_body")
        if lang == "ru" and cyr < 20:
            reasons.append("no_cyrillic")
    elif lang == "ru":
        if cjk >= 20:
            reasons.append("cjk_body")
        if cyr < 20:
            reasons.append("no_cyrillic")
    elif lang == "ja":
        if hangul >= 20:
            reasons.append("ko_body")
        if kana == 0 and han >= 20:
            reasons.append("no_kana_body")
        elif kana < 10 and han >= 80:
            reasons.append("no_kana_body")
    elif lang == "ko":
        if kana >= 20:
            reasons.append("ja_body")
        if hangul < 10 and (han >= 50 or latin >= 30):
            reasons.append("no_hangul_body")
    elif lang in LATIN_LANGS:
        pass
    elif lang in ("zh", "zh-TW"):
        if kana >= 10:
            reasons.append("ja_body")
        if hangul >= 10:
            reasons.append("ko_body")
        if han < 30 and latin >= 30:
            reasons.append("no_han_body")
    return reasons


def detect_lang(body) -> str:
    """Best-effort script label for reporting."""
    text = body_text(body)
    han = len(HAN.findall(text))
    kana = len(KANA.findall(text))
    hangul = len(HANGUL.findall(text))
    cyr = len(CYRILLIC.findall(text))
    latin = len(LATIN_WORD.findall(text))
    if kana > max(han, hangul) * 0.1 and kana > 20:
        return "ja"
    if hangul > 20:
        return "ko"
    if han > latin * 2 and han > 40:
        return "zh"
    if cyr > latin * 1.5 and cyr > 40:
        return "ru"
    return "latin"
