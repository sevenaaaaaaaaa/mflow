#!/usr/bin/env python3
"""Prepare notion-update-page insert_content payloads from a body file."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CHUNK = 7000


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def main() -> None:
    page_id = sys.argv[1]
    body_file = Path(sys.argv[2])
    start_offset = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    content = strip_h1(body_file.read_text(encoding="utf-8"))
    tail = content[start_offset:]
    out_dir = Path("/tmp/notion-mcp-inserts")
    out_dir.mkdir(exist_ok=True)
    paths = []
    for i in range(0, len(tail), CHUNK):
        payload = {
            "page_id": page_id,
            "command": "insert_content",
            "content": tail[i : i + CHUNK],
            "position": {"type": "end"},
        }
        p = out_dir / f"{page_id[:8]}-{start_offset + i}.json"
        p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        paths.append(str(p))
    print(json.dumps({"count": len(paths), "paths": paths, "total_chars": len(tail)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
