#!/usr/bin/env python3
"""Prepare next MCP operation for R1 bulk push. Agent calls MCP then runs advance."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
STATE = Path("/tmp/notion-r1-exec-state.json")
CHUNK = 14000
LARGE = 30000
DS = "235b9609-b155-491e-9801-b1504abe99c2"

PRE_CREATED = {
    "insight-data/Trident Insights/reports/monthly/Lovart-SEO-2025-07.md": "379fc0c7-1bd5-8156-a680-e7435b6de763",
    "insight-data/Trident Insights/reports/monthly/Lovart-SEO-2025-08.md": "379fc0c7-1bd5-81ed-8359-c14eeaae7b90",
}


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def chunks(content: str) -> list[str]:
    body = strip_h1(content)
    return [body[i : i + CHUNK] for i in range(0, len(body), CHUNK)] or [""]


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"phase": "init", "batch_idx": 0, "page_idx": 0, "chunk_idx": 0, "page_id": None, "failures": []}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def pending_items() -> list[tuple[Path, dict, str]]:
    done = done_paths()
    items: list[tuple[Path, dict, str]] = []
    for fp in sorted(BATCH_DIR.glob("R1-*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        for page, rel in zip(data["pages"], data["paths"]):
            if rel not in done:
                items.append((fp, page, rel))
    return items


def next_op() -> dict | None:
    st = load_state()
    items = pending_items()
    if not items:
        return None

    # Special: 2025-07 blank page needs content fill
    rel_fix = "insight-data/Trident Insights/reports/monthly/Lovart-SEO-2025-07.md"
    if rel_fix in done_paths() and st.get("fix_2025_07") != "done":
        page = None
        for _, p, rel in items:
            if rel == rel_fix:
                page = p
                break
        if page is None:
            # find in any batch file
            for fp in BATCH_DIR.glob("R1-*.json"):
                data = json.loads(fp.read_text(encoding="utf-8"))
                for p, rel in zip(data["pages"], data["paths"]):
                    if rel == rel_fix:
                        page = p
                        break
        if page:
            cidx = st.get("fix_chunk", 0)
            cs = chunks(page.get("content", ""))
            pid = PRE_CREATED[rel_fix]
            if cidx == 0:
                op = {"tool": "notion-update-page", "args": {"page_id": pid, "command": "replace_content", "new_str": cs[0]}}
            elif cidx < len(cs):
                op = {"tool": "notion-update-page", "args": {"page_id": pid, "command": "insert_content", "content": cs[cidx], "position": {"type": "end"}}}
            else:
                st["fix_2025_07"] = "done"
                save_state(st)
                return next_op()
            st["fix_chunk"] = cidx + 1
            save_state(st)
            return {"op": op, "meta": {"fix": rel_fix, "chunk": cidx, "total_chunks": len(cs)}}

    idx = st.get("item_idx", 0)
    if idx >= len(items):
        return None

    fp, page, rel = items[idx]
    phase = st.get("phase", "create")
    content = page.get("content", "")
    props = page["properties"]
    clen = len(content)

    if phase == "create":
        if clen < LARGE:
            op = {
                "tool": "notion-create-pages",
                "args": {
                    "parent": {"data_source_id": DS, "type": "data_source_id"},
                    "pages": [{"properties": props, "content": strip_h1(content)}],
                },
            }
            st["phase"] = "record"
        else:
            op = {
                "tool": "notion-create-pages",
                "args": {
                    "parent": {"data_source_id": DS, "type": "data_source_id"},
                    "pages": [{"properties": props}],
                },
            }
            st["phase"] = "content"
            st["chunk_idx"] = 0
        save_state(st)
        return {"op": op, "meta": {"rel_path": rel, "name": props.get("Name"), "phase": "create", "content_len": clen, "batch": fp.name}}

    if phase == "content":
        pid = st.get("page_id")
        if not pid:
            return {"error": "missing page_id", "meta": {"rel_path": rel}}
        cs = chunks(content)
        cidx = st.get("chunk_idx", 0)
        if cidx >= len(cs):
            st["phase"] = "record"
            save_state(st)
            return next_op()
        if cidx == 0:
            op = {"tool": "notion-update-page", "args": {"page_id": pid, "command": "replace_content", "new_str": cs[0]}}
        else:
            op = {"tool": "notion-update-page", "args": {"page_id": pid, "command": "insert_content", "content": cs[cidx], "position": {"type": "end"}}}
        st["chunk_idx"] = cidx + 1
        save_state(st)
        return {"op": op, "meta": {"rel_path": rel, "phase": "content", "chunk": cidx, "total_chunks": len(cs)}}

    if phase == "record":
        op = {"tool": "record", "args": {"paths": [rel]}}
        st["phase"] = "create"
        st["item_idx"] = idx + 1
        st["page_id"] = None
        st["chunk_idx"] = 0
        save_state(st)
        return {"op": op, "meta": {"rel_path": rel, "phase": "record"}}

    return None


def advance(page_id: str | None = None, error: str | None = None) -> dict:
    st = load_state()
    if error:
        items = pending_items()
        idx = st.get("item_idx", 0)
        rel = items[idx][2] if idx < len(items) else "?"
        st.setdefault("failures", []).append({"rel_path": rel, "error": error})
        st["phase"] = "create"
        st["item_idx"] = idx + 1
        st["page_id"] = None
        save_state(st)
        return status()
    if page_id:
        st["page_id"] = page_id
        save_state(st)
    return status()


def status() -> dict:
    done = done_paths()
    total = pending = 0
    for line in (SYNC / "sync-queue.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] != "R1":
            continue
        total += 1
        if e["rel_path"] not in done:
            pending += 1
    st = load_state()
    return {"total": total, "synced": total - pending, "pending": pending, "state": st, "failures": st.get("failures", [])}


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        print(json.dumps(status(), ensure_ascii=False))
    elif cmd == "next":
        op = next_op()
        if op is None:
            print(json.dumps({"done": True, **status()}, ensure_ascii=False))
        else:
            print(json.dumps(op, ensure_ascii=False))
    elif cmd == "advance":
        pid = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("ERR:") else None
        err = sys.argv[2][4:] if len(sys.argv) > 2 and sys.argv[2].startswith("ERR:") else None
        print(json.dumps(advance(pid, err), ensure_ascii=False))
    elif cmd == "reset":
        STATE.unlink(missing_ok=True)
        print(json.dumps(status(), ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
