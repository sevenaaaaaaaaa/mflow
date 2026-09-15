#!/usr/bin/env python3
"""Lovart 品牌词识别 SSOT — 所有 SEO/周报/竞品脚本统一引用。"""
from __future__ import annotations

import re
from typing import Iterable

BRAND_PATTERNS = [
    r"\blovart\b",
    r"\bloveart\b",
    r"\blovert\b",
    r"\blevert\b",
    r"\blovartia\b",
    r"\bart\s*ai\b",
    r"\bart\s+ia\b",
    r"\bia\s+art\b",
    r"\b(love|lovert|lover|levert)\s*(art|ai|ia)\b",
    r"\b(love)\s*(ia)\b",
    r"\blov[a-z0-9]*art[a-z0-9]*\b",
    r"\blov[a-z0-9]*ard\b",
    r"\blov\s+art\b",
    r"\blo\s+art\b",
    r"\bart\s+love\b",
    r"\bart\s+lov\b",
    r"\bartlov[a-z]*\b",
    r"\bluv\s+art\b",
    r"\blov\s+ia\b",
    r"\blov\s+ai\b",
    r"\blo\s+ai\b",
    r"\blavard\s+ai\b",
    r"\blawat\s+ai\b",
    r"\blavorat\b",
    r"\blouvat\b",
    r"\blavrt\b",
    r"\bl9vart\b",
    r"\blo\s*v\s*a\s*r\s*t\b",
    r"\biloveart\b",
    r"\bvol[a-z]*art\b",
    r"\blev[a-z]*art\b",
    r"\blouvar[a-z]*\b",
    r"\bluv[a-z]*art\b",
    r"\blo[a-z]*art[a-z]*\b",
    r"\bliv[a-z]*art\b",
    r"\blow[a-z]*art\b",
    r"\blave[a-z]*rt\b",
    r"\blorvat\b",
    r"\blavort\b",
    r"\blav[o0]rt\b",
    r"\blav[oa]r?t\b",
    r"\blavart[a-z]*\b",
    r"\blav[a-z]*art[a-z]*\b",
    r"\blawat\b",
    r"\blavard\b",
    r"lovart[\u4e00-\u9fff]+",
    r"[лЛ][оО][вВ][аА][рР][тТ]",
    r"ラブアート",
    r"[\u0644][\u0648][\u0641][\u0627\u0648]?\s*[\u0631\u0639]?\s*[\u062A\u0631]?\s*[\u062A]?",
    r"[\u0644][\u0648][\u0641][\u0631][\u062a]",
    r"[\u0644]\s*[\u0648]\s*[\u0627]\s*[\u0631]\s*[\u062a]",
    r"[\u0644]\s*[\u0627]\s*[\u0648]\s*[\u0627]\s*[\u0631]\s*[\u062a]",
    r"\bnano\s*banana\b",
    r"\bnanobanana\b",
    r"\bchatcanvas\b",
    r"\bmcot\b",
    r"\bbrand\s*kit\b.*lovart",
    r"\blova\b",
    r"\blovar\b",
    r"лаварт",
    r"ловарт",
    r"лов\s+арт",
    r"لاف\s*ارت",
    r"لف\s*ارت",
    r"لو\s*فارت",
    r"لافرت",
    r"لافارت",
    r"لافورت",
    r"لووارت",
    r"لوآرت",
]

# 非拉丁字母常见音译/误拼（子串匹配）
_TRANSLIT_FRAGMENTS = (
    "ロバート", "ラバート", "ラバート", "らぶあーと", "らばーと", "らぶあー",
    "ロバートai", "ラバートai",
    "로바트", "로버트", "로버트",
    "洛瓦特", "咯var", "咯var他",
    "لوفارت", "لافارت",
)

_LOVART_CANONICAL = "lovart"
_LOVEART_CANONICAL = "loveart"
_LOVERT_CANONICAL = "lovert"

# 品牌词根（分词匹配用）
_BRAND_ROOTS = frozenset({
    "lo", "lov", "love", "lovert", "levert", "lovert", "lover", "luv", "lav", "louv",
    "lavort", "lavart", "lavard", "lawat", "lavrt", "lavorat", "louvat", "lorvat",
    "lovart", "loveart", "lovartai", "lovar", "lovat", "lova", "louart", "lovurt", "lavrat",
    "lvart", "l9vart", "artlov", "iloveart", "volart", "levart",
})
_ART_SUFFIX_TOKENS = frozenset({"art", "ai", "ia", "rt"})

# 过宽的单 token 仅在与 art/ai 组合或整句极短时命中
_SHORT_ROOTS = frozenset({"lo", "lov", "luv", "lav"})

# 模糊匹配排除（常见非品牌英文词）
_FUZZY_DENY = frozenset({
    "logo", "logos", "login", "local", "logic", "load", "loan", "lock", "loop",
    "lose", "lost", "lone", "lobe", "logs", "loid", "lofi", "lore",
})


def _levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        return _levenshtein(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (0 if ca == cb else 1)))
        prev = cur
    return prev[-1]


def _normalize_compact(q: str) -> str:
    """去空格/标点，常见 OCR/键盘误触替换。"""
    s = re.sub(r"[^a-z0-9\u0400-\u04ff\u3040-\u30ff\u4e00-\u9fff]+", "", (q or "").lower())
    return (
        s.replace("9", "v")
        .replace("0", "o")
        .replace("1", "l")
        .replace("5", "s")
    )


def _multi_token_brand(ql: str) -> bool:
    tokens = re.findall(r"[a-z0-9]+", ql)
    if not tokens:
        return False
    if len(tokens) == 1 and tokens[0] == "lo":
        return True
    roots = []
    arts = []
    for t in tokens:
        tc = _normalize_compact(t)
        if tc in _ART_SUFFIX_TOKENS:
            arts.append(tc)
            continue
        if tc in _BRAND_ROOTS:
            roots.append(tc)
            continue
        if _fuzzy_lovart_token(tc):
            roots.append(tc)
    # 须存在明确品牌词根，避免 logo+ai 误判
    if arts and roots and not (roots == ["logo"] or (len(roots) == 1 and roots[0] in _FUZZY_DENY)):
        return True
    if len(tokens) == 2:
        a, b = tokens[0].lower(), tokens[1].lower()
        pairs = {
            ("lo", "art"), ("lo", "ai"), ("lo", "ia"),
            ("lov", "art"), ("lov", "ai"), ("lov", "ia"),
            ("luv", "art"), ("art", "love"), ("art", "lov"),
            ("love", "art"), ("levert", "ai"), ("lovert", "ai"),
            ("lavard", "ai"), ("lawat", "ai"),
        }
        if (a, b) in pairs or (b, a) in pairs:
            return True
    return False


def _compact_form_brand(ql: str) -> bool:
    c = _normalize_compact(ql)
    if not c or len(c) > 24:
        return False
    if c in ("lo", "lov", "luv"):
        return True
    anchors = (
        _LOVART_CANONICAL,
        _LOVEART_CANONICAL,
        _LOVERT_CANONICAL,
        "lovartai",
        "lavorat",
        "louvat",
        "lavort",
        "lavard",
        "lawat",
        "artlov",
        "artlove",
        "iloveart",
    )
    for anchor in anchors:
        if c == anchor:
            return True
        if len(c) >= 5 and len(c) <= len(anchor) + 3 and _levenshtein(c, anchor) <= 2:
            return True
    if re.search(r"^l[o0uv][vaeiou]*r?t", c) and len(c) <= 12:
        return True
    if c.startswith("artlov") or c.startswith("artlove"):
        return True
    if "loveart" in c or "lovart" in c:
        return True
    return False


def _fuzzy_lovart_token(token: str) -> bool:
    t = _normalize_compact(token)
    if not t or len(t) > 14 or t in _FUZZY_DENY:
        return False
    if t in _BRAND_ROOTS:
        return True
    if re.fullmatch(r"l[o0uv][vaeiou]*r?t", t) and 4 <= len(t) <= 10:
        return True
    if not re.fullmatch(r"[a-z0-9]{2,12}", t):
        return False
    if len(t) >= 5:
        for anchor in (_LOVART_CANONICAL, _LOVEART_CANONICAL, _LOVERT_CANONICAL, "lavort", "lavard"):
            if _levenshtein(t, anchor) <= 2:
                return True
    if len(t) == 4 and t in ("lova", "lovu", "luvi"):
        return True
    if t.startswith(("lov", "lav", "luv", "louv", "lev", "lor")) and (
        "art" in t or t.endswith("rt") or "ard" in t
    ):
        return True
    return False


def _translit_brand(q: str) -> bool:
    if not q:
        return False
    for frag in _TRANSLIT_FRAGMENTS:
        if frag in q:
            return True
    return False


def is_brand(q: str) -> bool:
    ql = (q or "").lower().strip()
    if not ql:
        return False
    if _translit_brand(q):
        return True
    for p in BRAND_PATTERNS:
        if re.search(p, ql):
            return True
    if _multi_token_brand(ql):
        return True
    if _compact_form_brand(ql):
        return True
    for token in re.findall(r"[a-zA-Z0-9]+", ql):
        if _fuzzy_lovart_token(token):
            return True
    return False


def partition_keywords(keywords: Iterable[dict]) -> tuple[list, list]:
    brand, nonbrand = [], []
    for k in keywords:
        (brand if is_brand(k.get("q", k.get("query", ""))) else nonbrand).append(k)
    return brand, nonbrand
