#!/usr/bin/env python3
"""Emit next pending R1 batch as MCP-ready JSON on stdout.

Usage:
  python3 notion-r1-mcp-invoke.py next     # full MCP args JSON
  python3 notion-r1-mcp-invoke.py paths    # rel_paths for last/next batch file
  python3 notion-r1-mcp-invoke.py list     # pending batch files summary
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def pending_files() -> list[Path]:
    done = done_paths()
    out: list[Path] = []
    for fp in sorted(BATCH_DIR.glob("R1-*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        if any(p not in done for p in data.get("paths", [])):
            out.append(fp)
    return out


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    files = pending_files()
    if cmd == "list":
        rows = []
        for fp in files:
            d = json.loads(fp.read_text(encoding="utf-8"))
            rows.append(
                {
                    "file": fp.name,
                    "paths": d["paths"],
                    "content_lens": [len(p.get("content", "")) for p in d["pages"]],
                }
            )
        print(json.dumps({"count": len(rows), "batches": rows}, ensure_ascii=False))
        return
    if not files:
        print(json.dumps({"done": True}))
        return
    fp = files[0]
    data = json.loads(fp.read_text(encoding="utf-8"))
    mcp = {"parent": data["parent"], "pages": data["pages"]}
    if cmd == "next":
        print(json.dumps({"file": str(fp), "paths": data["paths"], "mcp": mcp}, ensure_ascii=False))
    elif cmd == "paths":
        print(json.dumps(data["paths"], ensure_ascii=False))
    elif cmd == "mcp-only":
        print(json.dumps(mcp, ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
