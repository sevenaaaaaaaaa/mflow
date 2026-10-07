#!/usr/bin/env python3
"""Return next batch payload + rel_paths for Notion MCP push loop."""
from __future__ import annotations

import json
import sys
from pathlib import Path

QUEUE = Path(__file__).parent / "sync-queue.jsonl"
PROGRESS = Path(__file__).parent / "sync-pushed.jsonl"


def done_paths() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def next_batch(batch: str, limit: int = 3) -> dict:
    done = done_paths()
    pages = []
    rel_paths: list[str] = []
    ds_id = "1ea57b16-b0fe-40bb-9b23-b362ed44605d"
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if batch and e["batch"] != batch:
            continue
        if e["rel_path"] in done:
            continue
        ds_id = e["data_source_id"]
        rel_paths.append(e["rel_path"])
        pages.append({"properties": e["properties"], "content": e["content"]})
        if len(pages) >= limit:
            break
    return {
        "batch": batch,
        "parent": {"data_source_id": ds_id, "type": "data_source_id"},
        "pages": pages,
        "rel_paths": rel_paths,
        "count": len(pages),
    }


def counts() -> dict:
    done = done_paths()
    out: dict[str, dict[str, int]] = {}
    for b in ("K1", "H1"):
        total = remaining = 0
        for line in QUEUE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != b:
                continue
            total += 1
            if e["rel_path"] not in done:
                remaining += 1
        out[b] = {"total": total, "synced": total - remaining, "remaining": remaining}
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "counts":
        print(json.dumps(counts(), ensure_ascii=False))
    else:
        batch = sys.argv[1] if len(sys.argv) > 1 else "K1"
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        print(json.dumps(next_batch(batch, limit), ensure_ascii=False))
