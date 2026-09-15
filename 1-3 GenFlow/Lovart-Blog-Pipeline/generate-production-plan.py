#!/usr/bin/env python3
"""Build PRODUCTION-PLAN.md from cursor-lovart-blog-system-prompt.md article list."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "cursor-lovart-blog-system-prompt.md"
# Reorg 2026-06: cover pool lives in the Knowledge Base.
COVER_FILE = Path(
    "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/"
    "LifeOS Pro PARA Vault/1-Project/1-6 Knowledge Base/Cover Url 随机调取.md"
)
DRAFTS = ROOT / "01-Drafts"
OUT = ROOT / "PRODUCTION-PLAN.md"

URL_RE = re.compile(
    r"https://liblibai-online\.liblib\.cloud/blog-card-cover/\d+\.png"
)


def pick(slug: str, pool: list[str]) -> str:
    i = int(hashlib.sha256(slug.encode()).hexdigest()[:8], 16) % len(pool)
    return pool[i]


def prefix_for_index(n: int) -> str:
    if n <= 23:
        return "comparison"
    if n <= 38:
        return "lovart-101"
    if n <= 71:
        return "how-to"
    if n <= 78:
        return "better-design"
    if n <= 84:
        return "insight"
    return "segment"


def parse_articles(text: str) -> list[tuple[int, str, str]]:
    items: list[tuple[int, str, str]] = []
    seen: set[int] = set()
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^(\d+)\.\s+(.+)$", lines[i].strip())
        if not m:
            i += 1
            continue
        num = int(m.group(1))
        if num in seen or num > 93:
            i += 1
            continue
        rest = m.group(2).strip()
        slug = None
        title = rest
        slug_m = re.search(r"slug:\s+`([^`]+)`", rest)
        if slug_m:
            slug = slug_m.group(1)
            title = re.sub(r"\s*-?\s*slug:.*", "", rest).strip()
        else:
            dash_m = re.match(r"^(.+?)\s+[—–]\s+`([^`]+)`\s*$", rest)
            if dash_m:
                title, slug = dash_m.group(1).strip(), dash_m.group(2).strip()
            else:
                block = "\n".join(lines[i : i + 12])
                slug_m2 = re.search(r"slug:\s+`([^`]+)`", block)
                if slug_m2:
                    slug = slug_m2.group(1)
        if slug:
            items.append((num, title, slug))
            seen.add(num)
        i += 1
    return sorted(items, key=lambda x: x[0])


def draft_status(slug: str) -> str:
    for f in DRAFTS.glob("*.md"):
        if slug in f.name:
            return "draft-exists"
    return "pending"


def main() -> None:
    pool = list(dict.fromkeys(URL_RE.findall(COVER_FILE.read_text(encoding="utf-8"))))
    articles = parse_articles(PROMPT.read_text(encoding="utf-8"))
    lines = [
        "# Lovart Blog Production Plan",
        "",
        f"> {len(articles)} articles from system prompt. Covers: stable hash per slug ({len(pool)} URLs).",
        "> Output: `01-Drafts/`. Gold sample #1 complete.",
        "",
        "| # | title | slug | cover (tail) | status | filename |",
        "|---|-------|------|--------------|--------|----------|",
    ]
    for num, title, slug in articles:
        cover = pick(slug, pool)
        pf = prefix_for_index(num)
        fname = f"{pf}-{slug}.md"
        status = draft_status(slug)
        if num == 1:
            status = "draft-done"
        short_title = title[:50] + ("…" if len(title) > 50 else "")
        lines.append(
            f"| {num} | {short_title} | `{slug}` | `...{cover[-16:]}` | {status} | `{fname}` |"
        )
    lines.append("")
    lines.append(f"**Parsed:** {len(articles)} / 93 expected.")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({len(articles)} rows)")


if __name__ == "__main__":
    main()
