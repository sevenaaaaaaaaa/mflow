#!/usr/bin/env python3
"""Push all pending K1/H1 batches via stdin/stdout MCP bridge.

Agent usage:
  python3 notion-push-mcp-runner.py emit-next   # JSON: mcp args + rel_paths
  python3 notion-push-mcp-runner.py record A B C  # after MCP success
  python3 notion-push-mcp-runner.py status
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC_DIR = Path(__file__).parent
BATCH_DIR = Path("/tmp/notion-push-batches")
PROGRESS = SYNC_DIR / "sync-pushed.jsonl"
QUEUE = SYNC_DIR / "sync-queue.jsonl"


def done_paths() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def pending_batch_files() -> list[Path]:
    done = done_paths()
    out: list[Path] = []
    for batch in ("K1", "H1"):
        for path in sorted(BATCH_DIR.glob(f"{batch}-*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if any(r not in done for r in data["rel_paths"]):
                out.append(path)
    return out


def record(rel_paths: list[str]) -> None:
    with PROGRESS.open("a", encoding="utf-8") as f:
        for rel in rel_paths:
            f.write(json.dumps({"rel_path": rel, "status": "synced"}, ensure_ascii=False) + "\n")


def counts() -> dict:
    done = done_paths()
    stats: dict[str, dict[str, int]] = {}
    for b in ("K1", "H1"):
        total = synced = 0
        for line in QUEUE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != b:
                continue
            total += 1
            if e["rel_path"] in done:
                synced += 1
        stats[b] = {"total": total, "synced": synced, "remaining": total - synced}
    return stats


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        print(json.dumps(counts(), ensure_ascii=False, indent=2))
        files = pending_batch_files()
        print(f"pending_batches={len(files)}", file=sys.stderr)
        return
    if cmd == "emit-next":
        files = pending_batch_files()
        if not files:
            print(json.dumps({"done": True, "counts": counts()}, ensure_ascii=False))
            return
        data = json.loads(files[0].read_text(encoding="utf-8"))
        print(
            json.dumps(
                {
                    "file": str(files[0]),
                    "batch": data["batch"],
                    "rel_paths": data["rel_paths"],
                    "mcp": {"parent": data["parent"], "pages": data["pages"]},
                    "remaining_batches": len(files),
                    "counts": counts(),
                },
                ensure_ascii=False,
            )
        )
        return
    if cmd == "record":
        record(sys.argv[2:])
        print(json.dumps({"recorded": len(sys.argv) - 2, "counts": counts()}, ensure_ascii=False))
        return
    raise SystemExit(f"unknown cmd: {cmd}")


if __name__ == "__main__":
    main()
