#!/usr/bin/env python3
"""Step through R2 MCP page pushes: emit next args, advance after success."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
QUEUE = SYNC / ".mcp-args-queue.txt"
RECORD = SYNC / "notion-record-push.py"
STATE = SYNC / ".mcp-r2-push-state.json"


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"index": 0}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def queue_files() -> list[Path]:
    if not QUEUE.exists():
        return []
    return [Path(p) for p in QUEUE.read_text(encoding="utf-8").splitlines() if p.strip()]


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "emit"
    files = queue_files()
    st = load_state()
    idx = st.get("index", 0)

    if cmd == "status":
        print(json.dumps({"total": len(files), "index": idx, "remaining": max(0, len(files) - idx)}, ensure_ascii=False))
        return

    if cmd == "emit":
        if idx >= len(files):
            print(json.dumps({"done": True, "remaining": 0}))
            return
        data = json.loads(files[idx].read_text(encoding="utf-8"))
        print(
            json.dumps(
                {
                    "file": str(files[idx]),
                    "index": idx,
                    "remaining": len(files) - idx,
                    "rel_path": data["rel_path"],
                    "parent": data["parent"],
                    "pages": data["pages"],
                },
                ensure_ascii=False,
            )
        )
        return

    if cmd == "advance":
        rel = sys.argv[2] if len(sys.argv) > 2 else None
        if idx >= len(files):
            print(json.dumps({"error": "no pending"}))
            return
        data = json.loads(files[idx].read_text(encoding="utf-8"))
        expected = data["rel_path"]
        if rel and rel != expected:
            raise SystemExit(f"rel_path mismatch: expected {expected!r}, got {rel!r}")
        subprocess.check_call([sys.executable, str(RECORD), expected])
        st["index"] = idx + 1
        save_state(st)
        print(json.dumps({"recorded": expected, "next_index": st["index"], "remaining": len(files) - st["index"]}, ensure_ascii=False))
        return

    raise SystemExit(f"unknown cmd: {cmd}")


if __name__ == "__main__":
    main()
