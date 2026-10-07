#!/usr/bin/env python3
"""Emit next R1 sync step as JSON for agent MCP calls.

Steps per file:
  small: create_props -> replace_content (1 chunk) -> record
  large: create_props -> replace_content chunk0 -> insert_content chunks1..n -> record

Usage:
  python3 notion-r1-step-queue.py next       # next step JSON
  python3 notion-r1-step-queue.py status
  python3 notion-r1-step-queue.py done <rel>  # mark file complete after all steps
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SYNC = Path(__file__).parent
QUEUE = SYNC / "sync-queue.jsonl"
PROGRESS = SYNC / "sync-pushed.jsonl"
STATE = Path("/tmp/notion-r1-step-state.json")
DS = "235b9609-b155-491e-9801-b1504abe99c2"
LARGE = 30000
CHUNK = 14000


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def pending_entries() -> list[dict]:
    done = done_paths()
    out = []
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] != "R1" or e["rel_path"] in done:
            continue
        out.append(e)
    return out


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def chunks(body: str) -> list[str]:
    return [body[i : i + CHUNK] for i in range(0, len(body), CHUNK)] or [""]


def next_step() -> dict:
    st = load_state()
    pending = pending_entries()

    # Resume in-progress file
    if st.get("rel_path"):
        rel = st["rel_path"]
        entry = next((e for e in pending if e["rel_path"] == rel), None)
        if entry is None:
            st = {}
            save_state({})
        else:
            return advance(st, entry)

    if not pending:
        return {"done": True, "synced": len(done_paths())}

    # Prefer small files first
    pending.sort(key=lambda e: (len(e.get("content", "")) >= LARGE, e["rel_path"]))
    entry = pending[0]
    body = strip_h1(entry.get("content", ""))
    st = {
        "rel_path": entry["rel_path"],
        "phase": "create_props",
        "chunk_idx": 0,
        "page_id": None,
        "chunks": chunks(body) if len(entry.get("content", "")) >= LARGE else [body],
    }
    save_state(st)
    return advance(st, entry)


def advance(st: dict, entry: dict) -> dict:
    rel = st["rel_path"]
    props = entry["properties"]
    phase = st["phase"]

    if phase == "create_props":
        st["phase"] = "replace_content"
        save_state(st)
        return {
            "rel_path": rel,
            "step": "create_props",
            "mcp": {
                "tool": "notion-create-pages",
                "args": {
                    "parent": {"data_source_id": DS, "type": "data_source_id"},
                    "pages": [{"properties": props}],
                },
            },
        }

    if phase == "replace_content":
        if not st.get("page_id"):
            return {"error": "missing page_id after create", "rel_path": rel}
        idx = st["chunk_idx"]
        st["phase"] = "insert_content" if idx + 1 < len(st["chunks"]) else "record"
        save_state(st)
        return {
            "rel_path": rel,
            "step": "replace_content",
            "chunk": idx,
            "mcp": {
                "tool": "notion-update-page",
                "args": {
                    "page_id": st["page_id"],
                    "command": "replace_content",
                    "new_str": st["chunks"][idx],
                },
            },
        }

    if phase == "insert_content":
        idx = st["chunk_idx"] + 1
        if idx >= len(st["chunks"]):
            st["phase"] = "record"
            save_state(st)
            return advance(st, entry)
        st["chunk_idx"] = idx
        if idx + 1 >= len(st["chunks"]):
            st["phase"] = "record"
        save_state(st)
        return {
            "rel_path": rel,
            "step": "insert_content",
            "chunk": idx,
            "mcp": {
                "tool": "notion-update-page",
                "args": {
                    "page_id": st["page_id"],
                    "command": "insert_content",
                    "content": st["chunks"][idx],
                },
            },
        }

    if phase == "record":
        save_state({})
        return {
            "rel_path": rel,
            "step": "record",
            "cmd": ["python3", str(SYNC / "notion-record-push.py"), rel],
        }

    return {"error": f"unknown phase {phase}"}


def set_page_id(page_id: str) -> None:
    st = load_state()
    st["page_id"] = page_id
    save_state(st)


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
    return {"total": total, "synced": total - pending, "pending": pending, "state": load_state()}


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    if cmd == "status":
        print(json.dumps(status(), ensure_ascii=False))
    elif cmd == "set-page-id" and len(sys.argv) > 2:
        set_page_id(sys.argv[2])
        print(json.dumps({"ok": True, "page_id": sys.argv[2]}, ensure_ascii=False))
    elif cmd == "next":
        print(json.dumps(next_step(), ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
