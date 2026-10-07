#!/usr/bin/env python3
"""Prepare R2 batch payloads for Notion MCP (properties-only create + content chunks)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
CHUNK = 12000
DS = "235b9609-b155-491e-9801-b1504abe99c2"


def done_paths() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def pending_batches() -> list[Path]:
    done = done_paths()
    out: list[Path] = []
    for path in sorted(BATCH_DIR.glob("R2-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if any(r not in done for r in data["rel_paths"]):
            out.append(path)
    return out


def props_payload(batch_file: Path) -> dict:
    data = json.loads(batch_file.read_text(encoding="utf-8"))
    pages = [{"properties": p["properties"]} for p in data["mcp"]["pages"]]
    return {
        "batch_file": str(batch_file),
        "batch": data["batch"],
        "index": data["index"],
        "rel_paths": data["rel_paths"],
        "create": {
            "parent": {"data_source_id": DS, "type": "data_source_id"},
            "pages": pages,
        },
    }


def content_updates(batch_file: Path, page_ids: list[str]) -> list[dict]:
    data = json.loads(batch_file.read_text(encoding="utf-8"))
    updates: list[dict] = []
    for page, pid in zip(data["mcp"]["pages"], page_ids):
        content = page.get("content", "")
        if not content:
            continue
        if len(content) <= 25000:
            updates.append(
                {
                    "page_id": pid,
                    "name": page["properties"].get("Name", ""),
                    "command": "replace_content",
                    "new_str": content,
                }
            )
        else:
            chunks = [content[i : i + CHUNK] for i in range(0, len(content), CHUNK)]
            for j, chunk in enumerate(chunks):
                updates.append(
                    {
                        "page_id": pid,
                        "name": page["properties"].get("Name", ""),
                        "command": "insert_content",
                        "content": chunk,
                        "position": {"type": "end"} if j else {"type": "start"},
                        "chunk": j + 1,
                        "chunks": len(chunks),
                    }
                )
    return updates


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        pending = pending_batches()
        print(json.dumps([p.name for p in pending], ensure_ascii=False))
        return
    if cmd == "next-props":
        pending = pending_batches()
        if not pending:
            print(json.dumps({"done": True}))
            return
        print(json.dumps(props_payload(pending[0]), ensure_ascii=False))
        return
    if cmd == "content":
        batch_file = Path(sys.argv[2])
        page_ids = sys.argv[3:]
        print(json.dumps(content_updates(batch_file, page_ids), ensure_ascii=False))
        return
    if cmd == "counts":
        done = done_paths()
        total = synced = 0
        for line in (SYNC / "sync-queue.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != "R2":
                continue
            total += 1
            if e["rel_path"] in done:
                synced += 1
        print(json.dumps({"R2": {"total": total, "synced": synced, "remaining": total - synced}}, ensure_ascii=False))
        return
    raise SystemExit(f"unknown cmd: {cmd}")


if __name__ == "__main__":
    main()
