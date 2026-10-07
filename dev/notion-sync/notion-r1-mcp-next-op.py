#!/usr/bin/env python3
"""Emit next single MCP op for R1 sync (agent calls CallMcpTool then `advance`).

Workflow mirrors notion-r1-next-small-batch + notion-r1-finish-loop:
- small: create (props only) -> replace_content -> record
- large: create (props only) -> replace_content chunk0 -> insert chunks -> record

Usage:
  python3 notion-r1-mcp-next-op.py emit     # write /tmp/notion-r1-current-op.json
  python3 notion-r1-mcp-next-op.py advance [--page-id ID] [--error MSG]
  python3 notion-r1-mcp-next-op.py status
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
PROGRESS = SYNC / "sync-pushed.jsonl"
STATE = Path("/tmp/notion-r1-mcp-next-state.json")
OUT = Path("/tmp/notion-r1-current-op.json")
DS = "235b9609-b155-491e-9801-b1504abe99c2"
LARGE = 30000
CHUNK = 14000
PRE_CREATED = {
    "insight-data/Trident Insights/reports/topics/Lovart-SEO-topic-dual-engine-2026-04.md": "37afc0c7-1bd5-811c-b587-fea5d9fbd948",
}


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"phase": "small", "failures": []}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def chunks(body: str) -> list[str]:
    return [body[i : i + CHUNK] for i in range(0, len(body), CHUNK)] or [""]


def pending_small_batch(limit: int = 1) -> dict | None:
    raw = subprocess.check_output([sys.executable, str(SYNC / "notion-r1-next-small-batch.py"), str(limit)], text=True)
    data = json.loads(raw)
    if data.get("done"):
        return None
    return data


def pending_large_batch() -> dict | None:
    raw = subprocess.check_output([sys.executable, str(SYNC / "notion-r1-finish-loop.py"), "1"], text=True)
    data = json.loads(raw)
    if data.get("done"):
        return None
    return data


def status() -> dict:
    raw = subprocess.check_output([sys.executable, str(SYNC / "notion-mcp-sync-loop.py"), "status"], text=True)
    return json.loads(raw)


def emit() -> dict:
    st = load_state()
    if st.get("rel_path"):
        return advance_internal(st)

    phase = st.get("phase", "small")
    batch = pending_small_batch(1) if phase == "small" else None
    if batch is None and phase == "small":
        st["phase"] = "large"
        save_state(st)
        phase = "large"
        batch = None
    if batch is None and phase == "large":
        batch = pending_large_batch()
    if batch is None:
        return {"done": True, "status": status()}

    rel = batch["paths"][0]
    page = batch["pages"][0]
    body = strip_h1(page.get("content", ""))
    is_large = len(page.get("content", "")) >= LARGE
    pid = PRE_CREATED.get(rel)
    st = {
        "phase": phase,
        "rel_path": rel,
        "properties": page["properties"],
        "body": body,
        "is_large": is_large,
        "chunks": chunks(body) if is_large else [body],
        "chunk_idx": 0,
        "page_id": pid,
        "step": "update" if pid else "create",
        "failures": st.get("failures", []),
    }
    save_state(st)
    return advance_internal(st)


def advance_internal(st: dict) -> dict:
    rel = st["rel_path"]
    step = st.get("step", "create")

    if step == "create":
        op = {
            "tool": "notion-create-pages",
            "args": {
                "parent": {"data_source_id": DS, "type": "data_source_id"},
                "pages": [{"properties": st["properties"]}],
            },
            "meta": {"rel_path": rel, "step": "create"},
        }
        st["step"] = "replace"
        save_state(st)
        OUT.write_text(json.dumps(op, ensure_ascii=False), encoding="utf-8")
        return {**op, "status": status()}

    if step == "replace":
        if not st.get("page_id"):
            return {"error": "missing page_id after create", "rel_path": rel}
        idx = st["chunk_idx"]
        cs = st["chunks"]
        if idx == 0:
            op = {
                "tool": "notion-update-page",
                "args": {"page_id": st["page_id"], "command": "replace_content", "new_str": cs[0]},
                "meta": {"rel_path": rel, "step": "replace", "chunk": idx, "total": len(cs)},
            }
        else:
            op = {
                "tool": "notion-update-page",
                "args": {"page_id": st["page_id"], "command": "insert_content", "content": cs[idx]},
                "meta": {"rel_path": rel, "step": "insert", "chunk": idx, "total": len(cs)},
            }
        st["chunk_idx"] = idx + 1
        if st["chunk_idx"] >= len(cs):
            st["step"] = "record"
        save_state(st)
        OUT.write_text(json.dumps(op, ensure_ascii=False), encoding="utf-8")
        return {**op, "status": status()}

    if step == "record":
        subprocess.check_call([sys.executable, str(SYNC / "notion-record-push.py"), rel])
        save_state({"phase": st.get("phase", "small"), "failures": st.get("failures", [])})
        return {"recorded": rel, "status": status(), "next": "emit again"}

    return {"error": f"unknown step {step}"}


def advance(page_id: str | None = None, error: str | None = None) -> dict:
    st = load_state()
    if error:
        st.setdefault("failures", []).append({"rel_path": st.get("rel_path"), "error": error})
        save_state({"phase": st.get("phase", "small"), "failures": st["failures"]})
        if st.get("rel_path"):
            subprocess.check_call([sys.executable, str(SYNC / "notion-record-push.py"), st["rel_path"]])
        return {"failed": st.get("rel_path"), "status": status()}
    if page_id:
        st["page_id"] = page_id
        save_state(st)
    return {"ok": True, "page_id": page_id, "status": status()}


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "emit"
    if cmd == "emit":
        print(json.dumps(emit(), ensure_ascii=False))
    elif cmd == "advance":
        pid = None
        err = None
        for a in sys.argv[2:]:
            if a.startswith("ERR:"):
                err = a[4:]
            else:
                pid = a
        print(json.dumps(advance(pid, err), ensure_ascii=False))
    elif cmd == "status":
        print(json.dumps({**status(), "state": load_state()}, ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
