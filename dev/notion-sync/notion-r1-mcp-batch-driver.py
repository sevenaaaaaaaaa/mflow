#!/usr/bin/env python3
"""Prepare next R1 MCP batch; agent calls notion-create-pages then `record`."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
SMALL = SYNC / "notion-r1-next-small-batch.py"
FINISH = SYNC / "notion-r1-finish-loop.py"
RECORD = SYNC / "notion-record-push.py"
STATUS = SYNC / "notion-mcp-sync-loop.py"
OUT = Path("/tmp/notion-r1-mcp-driver")
STATE = OUT / "state.json"


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"phase": "small", "failures": []}


def save_state(st: dict) -> None:
    OUT.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def prepare_small(limit: int = 3) -> dict:
    raw = subprocess.check_output([sys.executable, str(SMALL), str(limit)], text=True)
    data = json.loads(raw)
    if data.get("done"):
        return {"done": True, "phase": "small"}
    OUT.mkdir(exist_ok=True)
    mcp = {"parent": data["parent"], "pages": data["pages"]}
    mcp_file = OUT / "create.json"
    mcp_file.write_text(json.dumps(mcp, ensure_ascii=False), encoding="utf-8")
    meta = {
        "phase": "small",
        "paths": data["paths"],
        "count": data["count"],
        "mcp_file": str(mcp_file),
        "tool": "notion-create-pages",
    }
    (OUT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return meta


def prepare_large() -> dict:
    raw = subprocess.check_output([sys.executable, str(FINISH), "1"], text=True)
    data = json.loads(raw)
    if data.get("done"):
        return {"done": True, "phase": "large"}
    create = json.loads((Path("/tmp/notion-r1-finish/create.json")).read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    mcp_file = OUT / "create.json"
    mcp_file.write_text(json.dumps(create, ensure_ascii=False), encoding="utf-8")
    meta = {
        "phase": "large",
        "paths": data["paths"],
        "large_ops": data.get("large_ops", []),
        "count": data["count"],
        "mcp_file": str(mcp_file),
        "tool": "notion-create-pages",
        "step": "create",
    }
    (OUT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return meta


def prepare() -> dict:
    st = load_state()
    phase = st.get("phase", "small")
    if phase == "small":
        meta = prepare_small(3)
        if meta.get("done"):
            st["phase"] = "large"
            save_state(st)
            meta = prepare_large()
    else:
        meta = prepare_large()
    if meta.get("done"):
        return {"done": True, "status": json.loads(subprocess.check_output([sys.executable, str(STATUS), "status"], text=True))}
    save_state({**st, "pending_meta": meta})
    meta["status"] = json.loads(subprocess.check_output([sys.executable, str(STATUS), "status"], text=True))
    return meta


def record(paths: list[str]) -> dict:
    if paths:
        subprocess.check_call([sys.executable, str(RECORD), *paths])
    return json.loads(subprocess.check_output([sys.executable, str(STATUS), "status"], text=True))


def note_failure(path: str, err: str) -> dict:
    st = load_state()
    st.setdefault("failures", []).append({"rel_path": path, "error": err})
    save_state(st)
    return st


def chunk_updates(page_id: str, rel_path: str) -> list[dict]:
    meta = json.loads((OUT / "meta.json").read_text(encoding="utf-8"))
    for op in meta.get("large_ops", []):
        if op["rel_path"] == rel_path:
            updates = []
            chunks = op["chunks"]
            updates.append({"tool": "notion-update-page", "page_id": page_id, "command": "replace_content", "new_str": chunks[0]})
            for c in chunks[1:]:
                updates.append({"tool": "notion-update-page", "page_id": page_id, "command": "insert_content", "content": c})
            return updates
    return []


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if cmd == "prepare":
        print(json.dumps(prepare(), ensure_ascii=False))
    elif cmd == "record":
        print(json.dumps(record(sys.argv[2:]), ensure_ascii=False))
    elif cmd == "fail":
        print(json.dumps(note_failure(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    elif cmd == "chunks":
        print(json.dumps(chunk_updates(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    elif cmd == "mcp":
        print((OUT / "create.json").read_text(encoding="utf-8"))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
