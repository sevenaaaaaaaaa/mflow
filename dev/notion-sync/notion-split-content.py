#!/usr/bin/env python3
"""Split page body into MCP-sized chunks; print chunk file paths."""
from __future__ import annotations

import re
import sys
from pathlib import Path

CHUNK = 14000


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def main() -> None:
    content_path = Path(sys.argv[1])
    out_prefix = sys.argv[2] if len(sys.argv) > 2 else "/tmp/notion-chunks"
    content = strip_h1(content_path.read_text(encoding="utf-8"))
    paths = []
    for i in range(0, len(content), CHUNK):
        p = Path(f"{out_prefix}-{i // CHUNK}.md")
        p.write_text(content[i : i + CHUNK], encoding="utf-8")
        paths.append(str(p))
    print("\n".join(paths))


if __name__ == "__main__":
    main()
