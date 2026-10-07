#!/usr/bin/env python3
"""Automate R1 Notion MCP push loop: prepare batches until queue empty."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
PUSH = SYNC / "notion-push-batch.py"
RECORD = SYNC / "notion-record-push.py"
PROGRESS = SYNC / "sync-pushed.jsonl"
BATCH_DIR = Path("/tmp/notion-r1-batches")
BATCH_DIR.mkdir(exist_ok=True)


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def pending_count(batch: str) -> int:
    done = done_paths()
    n = 0
    for line in (SYNC / "sync-queue.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] == batch and e["rel_path"] not in done:
            n += 1
    return n


def prepare_all(batch: str, limit: int) -> list[Path]:
    files: list[Path] = []
    i = 0
    while True:
        raw = subprocess.check_output(
            [sys.executable, str(PUSH), batch, str(limit)], text=True, encoding="utf-8"
        )
        payload = json.loads(raw)
        if payload["count"] == 0:
            break
        fp = BATCH_DIR / f"{batch}-{i:04d}.json"
        fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        files.append(fp)
        # simulate push by recording - NO, only prepare
        # temporarily record to advance? No - this is prepare only
        # We need to break infinite loop - push-batch reads progress file
        # Without recording, same batch repeats. So prepare_all can't work without recording.
        break
    return files


def status(batch: str) -> dict:
    done = done_paths()
    total = pending = 0
    for line in (SYNC / "sync-queue.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] != batch:
            continue
        total += 1
        if e["rel_path"] not in done:
            pending += 1
    return {"batch": batch, "total": total, "synced": total - pending, "pending": pending}


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    batch = sys.argv[2] if len(sys.argv) > 2 else "R1"
    if cmd == "status":
        print(json.dumps(status(batch), ensure_ascii=False))
    elif cmd == "next-meta":
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        raw = subprocess.check_output(
            [sys.executable, str(PUSH), batch, str(limit)], text=True, encoding="utf-8"
        )
        payload = json.loads(raw)
        out = BATCH_DIR / "current.json"
        out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        print(
            json.dumps(
                {
                    "count": payload["count"],
                    "paths": [p["properties"]["Source Path"] for p in payload["pages"]],
                    "names": [p["properties"].get("Name") for p in payload["pages"]],
                    "content_lens": [len(p.get("content", "")) for p in payload["pages"]],
                    "file": str(out),
                },
                ensure_ascii=False,
            )
        )
    elif cmd == "record":
        subprocess.run([sys.executable, str(RECORD), *sys.argv[3:]], check=True)
        print(json.dumps(status(batch), ensure_ascii=False))
    else:
        raise SystemExit(f"unknown cmd {cmd}")


if __name__ == "__main__":
    main()
