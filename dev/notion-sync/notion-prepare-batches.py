#!/usr/bin/env python3
"""Prepare all MCP batch files for K1/H1 from sync-queue (ignoring already-pushed)."""
from __future__ import annotations

import json
from pathlib import Path

QUEUE = Path(__file__).parent / "sync-queue.jsonl"
PROGRESS = Path(__file__).parent / "sync-pushed.jsonl"
OUT_DIR = Path("/tmp/notion-push-batches")


def done_paths() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def main() -> None:
    done = done_paths()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.json"):
        old.unlink()

    manifest = []
    for batch in ("K1", "H1"):
        pending = []
        for line in QUEUE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != batch or e["rel_path"] in done:
                continue
            pending.append(e)

        for i in range(0, len(pending), 3):
            chunk = pending[i : i + 3]
            n = i // 3 + 1
            rel_paths = [e["rel_path"] for e in chunk]
            payload = {
                "parent": {
                    "data_source_id": chunk[0]["data_source_id"],
                    "type": "data_source_id",
                },
                "pages": [
                    {"properties": e["properties"], "content": e["content"]}
                    for e in chunk
                ],
                "rel_paths": rel_paths,
                "batch": batch,
                "count": len(chunk),
            }
            path = OUT_DIR / f"{batch}-{n:02d}.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            manifest.append(str(path))

    print(json.dumps({"files": manifest, "total_batches": len(manifest)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
