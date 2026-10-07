#!/usr/bin/env python3
"""Emit next N pages from sync-queue.jsonl as JSON for Notion MCP create-pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

QUEUE = Path(__file__).parent / "sync-queue.jsonl"
PROGRESS = Path(__file__).parent / "sync-pushed.jsonl"


def main() -> None:
    batch = sys.argv[1] if len(sys.argv) > 1 else ""
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    done = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])

    pages = []
    ds_id = None
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if batch and e["batch"] != batch:
            continue
        if e["rel_path"] in done:
            continue
        ds_id = e["data_source_id"]
        pages.append(
            {
                "properties": e["properties"],
                "content": e["content"],
            }
        )
        if len(pages) >= limit:
            break

    print(
        json.dumps(
            {"parent": {"data_source_id": ds_id, "type": "data_source_id"}, "pages": pages, "count": len(pages)},
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
