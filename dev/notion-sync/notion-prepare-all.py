#!/usr/bin/env python3
"""Single-pass: write MCP payload files for all pending pages in given batches."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC = Path(__file__).parent
QUEUE = SYNC / "sync-queue.jsonl"
PROGRESS = SYNC / "sync-pushed.jsonl"
OUT = SYNC / ".batch-out"


def load_done() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def main() -> None:
    batches = sys.argv[1:] if len(sys.argv) > 1 else ["R2", "R3", "A1"]
    want = set(batches)
    done = load_done()
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()

    pending: dict[str, list[dict]] = {b: [] for b in batches}
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] not in want or e["rel_path"] in done:
            continue
        pending[e["batch"]].append(e)

    manifest = []
    for batch in batches:
        items = pending[batch]
        idx = 0
        for i in range(0, len(items), 3):
            chunk = items[i : i + 3]
            idx += 1
            pages = []
            for c in chunk:
                props = dict(c["properties"])
                if batch == "A1" and "Source Path" in props:
                    props["Output Path"] = props.pop("Source Path")
                pages.append({"properties": props, "content": c["content"]})
            payload = {
                "batch": batch,
                "index": idx,
                "count": len(chunk),
                "rel_paths": [c["rel_path"] for c in chunk],
                "mcp": {
                    "parent": {"data_source_id": chunk[0]["data_source_id"], "type": "data_source_id"},
                    "pages": pages,
                },
            }
            fname = f"{batch}-{idx:03d}.json"
            (OUT / fname).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            manifest.append({"batch": batch, "file": fname, "count": len(chunk), "rel_paths": payload["rel_paths"]})

    summary = {
        "total": sum(m["count"] for m in manifest),
        "files": len(manifest),
        "by_batch": {b: sum(m["count"] for m in manifest if m["batch"] == b) for b in batches},
        "manifest": manifest,
    }
    (OUT / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
