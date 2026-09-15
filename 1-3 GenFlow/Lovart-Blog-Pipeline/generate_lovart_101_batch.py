#!/usr/bin/env python3
"""Generate all Lovart 101 drafts (>=4500 words each)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.lovart_101_common import (  # noqa: E402
    DRAFTS,
    closing_blocks,
    faq_schema,
    howto_schema,
    pick_cover_url,
    write_draft,
)
from lib.lovart_101_content.articles import ALL_SPECS as ARTICLES  # noqa: E402


def update_production_plan(results: list[tuple[str, int, str]]) -> None:
    plan = Path(__file__).resolve().parents[1] / "PRODUCTION-PLAN.md"
    text = plan.read_text(encoding="utf-8")
    for slug, words, filename in results:
        status_cell = f"draft-done (~{words}w)"
        pat = (
            rf"(\| \d+ \| \*\*101-\d+:\*\*[^\|]+\| `{re.escape(slug)}`"
            rf"[^\|]+\|[^\|]+\| )(?:pending|draft-done \(~[^)]+\))("
            rf" \| `{re.escape(filename)}` \|)"
        )
        text, n = re.subn(pat, rf"\1{status_cell}\2", text, count=1)
        if n == 0:
            pat2 = rf"(\| [^\|]+ \| )(?:pending|draft-done \(~[^)]+\))( \| `{re.escape(filename)}` \|)"
            text, _ = re.subn(pat2, rf"\1{status_cell}\3", text, count=1)
    plan.write_text(text, encoding="utf-8")


def main() -> None:
    results: list[tuple[str, int, str]] = []
    for spec in ARTICLES:
        body = spec["body_builder"]()
        words = len(body.split())
        if words < 4500:
            raise SystemExit(f"{spec['filename']}: only {words} words (need >=4500)")
        structured = spec["structured"]()
        w = write_draft(spec["filename"], spec["meta"], body, structured)
        results.append((spec["meta"]["slug"], w, spec["filename"]))
        print(f"OK {spec['filename']}: {w} words")
    update_production_plan(results)
    print(f"Updated PRODUCTION-PLAN.md ({len(results)} rows)")


if __name__ == "__main__":
    main()
