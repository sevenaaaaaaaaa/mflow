#!/usr/bin/env python3
"""R1 batch MCP push helper: emit-next / record / status for pre-generated .batch-out/R1-*.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
QUEUE = SYNC / "sync-queue.jsonl"
STATE = Path("/tmp/notion-r1-push-state.json")


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def batch_files() -> list[Path]:
    return sorted(BATCH_DIR.glob("R1-*.json"))


def pending_files() -> list[Path]:
    done = done_paths()
    out: list[Path] = []
    for fp in batch_files():
        data = json.loads(fp.read_text(encoding="utf-8"))
        if any(p not in done for p in data.get("paths", [])):
            out.append(fp)
    return out


def record(rel_paths: list[str]) -> None:
    with PROGRESS.open("a", encoding="utf-8") as f:
        for rel in rel_paths:
            f.write(json.dumps({"rel_path": rel, "status": "synced"}, ensure_ascii=False) + "\n")


def status() -> dict:
    done = done_paths()
    total = pending = 0
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] != "R1":
            continue
        total += 1
        if e["rel_path"] not in done:
            pending += 1
    files = pending_files()
    return {
        "batch": "R1",
        "total": total,
        "synced": total - pending,
        "pending": pending,
        "pending_batches": len(files),
    }


def emit_next() -> None:
    files = pending_files()
    if not files:
        print(json.dumps({"done": True, **status()}, ensure_ascii=False))
        return
    fp = files[0]
    data = json.loads(fp.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "file": str(fp),
                "index": int(fp.stem.split("-")[1]),
                "paths": data["paths"],
                "mcp": {"parent": data["parent"], "pages": data["pages"]},
                "content_lens": [len(p.get("content", "")) for p in data["pages"]],
                **status(),
            },
            ensure_ascii=False,
        )
    )


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        print(json.dumps(status(), ensure_ascii=False))
    elif cmd == "emit-next":
        emit_next()
    elif cmd == "record":
        record(sys.argv[2:])
        print(json.dumps(status(), ensure_ascii=False))
    else:
        raise SystemExit(f"unknown cmd: {cmd}")


if __name__ == "__main__":
    main()
