#!/usr/bin/env python3
"""Emit next S1 MCP batch args from pre-prepared files or notion-push-next.py."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC_DIR = Path(__file__).parent
BATCH_DIR = Path("/tmp/notion-s1-batches")
PUSH_NEXT = SYNC_DIR / "notion-push-next.py"
PROGRESS = SYNC_DIR / "sync-pushed.jsonl"


def done_paths() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def next_prepared() -> dict | None:
    done = done_paths()
    for path in sorted(BATCH_DIR.glob("S1-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if any(r not in done for r in data["rel_paths"]):
            return {
                "file": str(path),
                "parent": data["parent"],
                "pages": data["pages"],
                "rel_paths": data["rel_paths"],
                "count": data["count"],
            }
    return None


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    if cmd == "next":
        batch = next_prepared()
        if not batch:
            out = subprocess.check_output(
                [sys.executable, str(PUSH_NEXT), "S1", "3"], text=True, encoding="utf-8"
            )
            data = json.loads(out)
            if data["count"] == 0:
                print(json.dumps({"done": True}))
                return
            batch = {
                "parent": data["parent"],
                "pages": data["pages"],
                "rel_paths": data["rel_paths"],
                "count": data["count"],
            }
        print(json.dumps(batch, ensure_ascii=False))
        return
    if cmd == "status":
        done = done_paths()
        total = synced = 0
        for line in (SYNC_DIR / "sync-queue.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != "S1":
                continue
            total += 1
            if e["rel_path"] in done:
                synced += 1
        pending_batches = sum(
            1
            for p in sorted(BATCH_DIR.glob("S1-*.json"))
            if any(
                r not in done
                for r in json.loads(p.read_text(encoding="utf-8"))["rel_paths"]
            )
        )
        print(
            json.dumps(
                {
                    "total_s1": total,
                    "synced": synced,
                    "remaining": total - synced,
                    "pending_batches": pending_batches,
                },
                ensure_ascii=False,
            )
        )
        return
    raise SystemExit(f"unknown cmd: {cmd}")


if __name__ == "__main__":
    main()
