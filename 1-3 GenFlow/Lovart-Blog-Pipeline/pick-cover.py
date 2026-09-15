#!/usr/bin/env python3
"""Assign a stable cover URL from the Lovart blog card pool (per slug)."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

DEFAULT_POOL = Path(
    "/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/"
    "1-2 Insight/Knowledge Base/Cover Url 随机调取.md"
)
URL_RE = re.compile(
    r"https://liblibai-online\.liblib\.cloud/blog-card-cover/\d+\.png"
)


def load_pool(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    seen: set[str] = set()
    pool: list[str] = []
    for url in URL_RE.findall(text):
        if url not in seen:
            seen.add(url)
            pool.append(url)
    if not pool:
        raise SystemExit(f"No cover URLs found in {path}")
    return pool


def pick_cover(slug: str, pool: list[str]) -> str:
    digest = hashlib.sha256(slug.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(pool)
    return pool[index]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", nargs="?", help="Article slug")
    parser.add_argument(
        "--pool",
        type=Path,
        default=DEFAULT_POOL,
        help="Path to Cover Url markdown file",
    )
    parser.add_argument(
        "--alt",
        help="Optional alt text (defaults to slug-based description)",
    )
    args = parser.parse_args()
    pool = load_pool(args.pool)
    if not args.slug:
        print(f"Pool size: {len(pool)} unique URLs")
        return
    url = pick_cover(args.slug, pool)
    alt = args.alt or f"Cover image for Lovart blog article: {args.slug}"
    print(url)
    print(f"alt_text: {alt}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
