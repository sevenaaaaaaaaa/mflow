#!/usr/bin/env python3
"""Expand all queue entries into per-page MCP payload files for agent batch push."""
from __future__ import annotations

import json
from pathlib import Path

SYNC = Path(__file__).parent
QUEUE = SYNC / "sync-queue.jsonl"
PROGRESS = SYNC / "sync-pushed.jsonl"
OUT = Path("/tmp/notion-page-payloads")
PARENT = {"data_source_id": "1ea57b16-b0fe-40bb-9b23-b362ed44605d", "type": "data_source_id"}


def done() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    done_set = done()
    manifest = []
    for batch in ("K1", "H1"):
        for line in QUEUE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != batch or e["rel_path"] in done_set:
                continue
            safe = e["rel_path"].replace("/", "__")
            path = OUT / f"{batch}__{safe}.json"
            payload = {
                "parent": PARENT,
                "pages": [{"properties": e["properties"], "content": e["content"]}],
                "rel_path": e["rel_path"],
                "batch": batch,
            }
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            manifest.append(str(path))
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"pending_pages": len(manifest), "manifest": str(OUT / "manifest.json")}))


if __name__ == "__main__":
    main()
