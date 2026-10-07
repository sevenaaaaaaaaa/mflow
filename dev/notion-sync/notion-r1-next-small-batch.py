#!/usr/bin/env python3
"""Emit next MCP create-pages payload for up to N small (<30KB) pending R1 pages."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
LARGE = 30000


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def main() -> None:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    done = done_paths()
    parent = None
    pages: list[dict] = []
    paths: list[str] = []

    for fp in sorted(BATCH_DIR.glob("R1-*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        for page, rel in zip(data["pages"], data["paths"]):
            if rel in done:
                continue
            if len(page.get("content", "")) >= LARGE:
                continue
            parent = data["parent"]
            pages.append({"properties": page["properties"], "content": strip_h1(page["content"])})
            paths.append(rel)
            if len(pages) >= limit:
                break
        if len(pages) >= limit:
            break

    if not pages:
        print(json.dumps({"done": True, "count": 0}))
        return

    out = {"parent": parent, "pages": pages, "paths": paths, "count": len(pages)}
    Path("/tmp/mcp-create-batch.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
