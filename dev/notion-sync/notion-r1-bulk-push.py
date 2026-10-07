#!/usr/bin/env python3
"""Generate MCP operation queue for R1 bulk push. Agent executes ops via CallMcpTool."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
CHUNK = 14000
LARGE = 30000
DS = "235b9609-b155-491e-9801-b1504abe99c2"

# Already created, pending content fill only
PRE_CREATED = {
    "insight-data/Trident Insights/reports/monthly/Lovart-SEO-2025-06.md": "379fc0c7-1bd5-8122-9bf5-d7667d662bce",
    "insight-data/Trident Insights/reports/monthly/Lovart-SEO-2025-07.md": "379fc0c7-1bd5-8156-a680-e7435b6de763",
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


def content_chunks(content: str) -> list[str]:
    body = strip_h1(content)
    return [body[i : i + CHUNK] for i in range(0, len(body), CHUNK)] or [""]


def pending_batches() -> list[Path]:
    done = done_paths()
    out: list[Path] = []
    for fp in sorted(BATCH_DIR.glob("R1-*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        if any(p not in done for p in data.get("paths", [])):
            out.append(fp)
    return out


def ops_for_page(page: dict, rel_path: str, page_id: str | None = None) -> list[dict]:
    content = page.get("content", "")
    props = page["properties"]
    ops: list[dict] = []

    if page_id:
        chunks = content_chunks(content)
        ops.append({"tool": "notion-update-page", "args": {"page_id": page_id, "command": "replace_content", "new_str": chunks[0]}})
        for c in chunks[1:]:
            ops.append({"tool": "notion-update-page", "args": {"page_id": page_id, "command": "insert_content", "content": c, "position": {"type": "end"}}})
        ops.append({"tool": "record", "args": {"paths": [rel_path]}})
        return ops

    if len(content) < LARGE:
        ops.append({
            "tool": "notion-create-pages",
            "args": {
                "parent": {"data_source_id": DS, "type": "data_source_id"},
                "pages": [{"properties": props, "content": strip_h1(content)}],
            },
            "expect_page_id": True,
            "rel_path": rel_path,
        })
        ops.append({"tool": "record", "args": {"paths": [rel_path]}})
    else:
        ops.append({
            "tool": "notion-create-pages",
            "args": {
                "parent": {"data_source_id": DS, "type": "data_source_id"},
                "pages": [{"properties": props}],
            },
            "expect_page_id": True,
            "rel_path": rel_path,
        })
        chunks = content_chunks(content)
        ops.append({"tool": "notion-update-page", "args": {"page_id": "$PAGE_ID", "command": "replace_content", "new_str": chunks[0]}})
        for c in chunks[1:]:
            ops.append({"tool": "notion-update-page", "args": {"page_id": "$PAGE_ID", "command": "insert_content", "content": c, "position": {"type": "end"}}})
        ops.append({"tool": "record", "args": {"paths": [rel_path]}})
    return ops


def build_queue(limit_batches: int | None = None) -> list[dict]:
    queue: list[dict] = []
    batches = pending_batches()
    if limit_batches:
        batches = batches[:limit_batches]
    for fp in batches:
        data = json.loads(fp.read_text(encoding="utf-8"))
        for page, rel in zip(data["pages"], data["paths"]):
            if rel in done_paths():
                continue
            pid = PRE_CREATED.get(rel)
            queue.extend(ops_for_page(page, rel, pid))
    return queue


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
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
        print(json.dumps({"total": total, "synced": total - pending, "pending": pending, "pending_batches": len(pending_batches())}, ensure_ascii=False))
    elif cmd == "queue":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
        q = build_queue(limit)
        out = Path("/tmp/notion-r1-ops-queue.json")
        out.write_text(json.dumps(q, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"ops": len(q), "file": str(out)}, ensure_ascii=False))
    elif cmd == "next-op":
        qfile = Path("/tmp/notion-r1-ops-queue.json")
        state_file = Path("/tmp/notion-r1-ops-state.json")
        if not qfile.exists():
            build_queue()
            q = build_queue()
            qfile.write_text(json.dumps(q, ensure_ascii=False), encoding="utf-8")
            state_file.write_text(json.dumps({"index": 0, "page_ids": {}}, ensure_ascii=False), encoding="utf-8")
        q = json.loads(qfile.read_text(encoding="utf-8"))
        state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {"index": 0, "page_ids": {}}
        idx = state["index"]
        if idx >= len(q):
            print(json.dumps({"done": True}))
            return
        op = q[idx]
        print(json.dumps({"index": idx, "total": len(q), "op": op}, ensure_ascii=False))
    elif cmd == "advance":
        state_file = Path("/tmp/notion-r1-ops-state.json")
        state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {"index": 0, "page_ids": {}}
        state["index"] = state.get("index", 0) + 1
        if len(sys.argv) > 2:
            rel = sys.argv[2]
            pid = sys.argv[3]
            state.setdefault("page_ids", {})[rel] = pid
        state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(state, ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
