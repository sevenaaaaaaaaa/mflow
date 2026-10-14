#!/usr/bin/env python3
"""Brand keyword matcher — single entry point for all SEO / weekly / competitor scripts.

The public repo ships only a generic matcher driven by the active site profile
(`brand_terms` in ops/site.json or MFLOW_BRAND_NAME, see dev/scripts/library/site_profile.py):
a query is "brand" when it contains one of the terms (case-insensitive, whitespace-insensitive).

A brand can ship a richer matcher (misspellings, transliterations, fuzzy rules) as
ops/brands/<brand_slug>/code/brand_match.py exposing the same API (is_brand, partition_keywords,
BRAND_PATTERNS, ...). When present it replaces the generic implementation transparently.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent / "library"))
import site_profile  # noqa: E402

_brand = site_profile.load_brand_module("brand_match")

if _brand is not None:
    globals().update({k: v for k, v in vars(_brand).items() if not k.startswith("__")})
else:
    _TERMS = [t.strip().lower() for t in site_profile.get("brand_terms", []) if str(t).strip()]
    BRAND_PATTERNS = [r"\b" + re.escape(t) + r"\b" for t in _TERMS]
    _BRAND_ROOTS = frozenset(_TERMS)
    _TRANSLIT_FRAGMENTS: tuple = ()
    _FUZZY_DENY: frozenset = frozenset()
    _ART_SUFFIX_TOKENS: frozenset = frozenset()
    _SHORT_ROOTS: frozenset = frozenset()

    def is_brand(q: str) -> bool:
        ql = (q or "").lower().strip()
        if not ql or not _TERMS:
            return False
        compact = re.sub(r"\s+", "", ql)
        return any(re.search(p, ql) for p in BRAND_PATTERNS) or any(
            t.replace(" ", "") in compact for t in _TERMS)

    def partition_keywords(keywords: Iterable[dict]) -> tuple[list, list]:
        brand, nonbrand = [], []
        for k in keywords:
            (brand if is_brand(k.get("q", k.get("query", ""))) else nonbrand).append(k)
        return brand, nonbrand
