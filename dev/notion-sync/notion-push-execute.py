#!/usr/bin/env python3
"""Emit MCP create-pages args for next pending batch file (K1 then H1)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

BATCH_DIR = Path("/tmp/notion-push-batches")
PROGRESS = Path(__file__).parent / "sync-pushed.jsonl"


def done_paths() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def pending_files() -> list[Path]:
    done = done_paths()
    out: list[Path] = []
    for batch in ("K1", "H1"):
        for path in sorted(BATCH_DIR.glob(f"{batch}-*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if any(r not in done for r in data["rel_paths"]):
                out.append(path)
    return out


def main() -> None:
    action = sys.argv[1] if len(sys.argv) > 1 else "next"
    if action == "list":
        print(json.dumps([str(p) for p in pending_files()], ensure_ascii=False))
        return
    if action == "next":
        files = pending_files()
        if not files:
            print(json.dumps({"done": True}))
            return
        path = files[0]
        data = json.loads(path.read_text(encoding="utf-8"))
        print(
            json.dumps(
                {
                    "file": str(path),
                    "batch": data["batch"],
                    "rel_paths": data["rel_paths"],
                    "mcp": {"parent": data["parent"], "pages": data["pages"]},
                },
                ensure_ascii=False,
            )
        )
        return
    if action == "record":
        rels = sys.argv[2:]
        PROGRESS.open("a", encoding="utf-8").writelines(
            json.dumps({"rel_path": r, "status": "synced"}, ensure_ascii=False) + "\n"
            for r in rels
        )
        print("recorded", len(rels))
        return
    if action == "counts":
        done = done_paths()
        stats = {}
        queue = Path(__file__).parent / "sync-queue.jsonl"
        for b in ("K1", "H1"):
            total = synced = 0
            for line in queue.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                e = json.loads(line)
                if e["batch"] != b:
                    continue
                total += 1
                if e["rel_path"] in done:
                    synced += 1
            stats[b] = {"total": total, "synced": synced, "remaining": total - synced}
        print(json.dumps(stats, ensure_ascii=False))
        return
    raise SystemExit(f"unknown action: {action}")


if __name__ == "__main__":
    main()
