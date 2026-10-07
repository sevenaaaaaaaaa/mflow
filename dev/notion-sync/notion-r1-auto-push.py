#!/usr/bin/env python3
"""Automated R1 Notion push loop via pre-generated batches.

Usage (agent drives MCP between steps):
  python3 notion-r1-auto-push.py prepare     # regen .batch-out/R1-*.json
  python3 notion-r1-auto-push.py emit        # next MCP payload -> /tmp/notion-r1-mcp-current.json
  python3 notion-r1-auto-push.py paths       # rel_paths for current emit
  python3 notion-r1-auto-push.py record      # record paths from last emit
  python3 notion-r1-auto-push.py status
  python3 notion-r1-auto-push.py run-shell   # emit all small batches metadata

For large pages (>40KB content), emit splits to single-page payloads automatically.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
QUEUE = SYNC / "sync-queue.jsonl"
STATE = Path("/tmp/notion-r1-auto-state.json")
MCP_OUT = Path("/tmp/notion-r1-mcp-current.json")
MAX_PAIR_CONTENT = 80000  # split batch if combined content exceeds this


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def prepare() -> dict:
    done = done_paths()
    pending = []
    ds_id = None
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] != "R1":
            continue
        if e["rel_path"] in done:
            continue
        ds_id = e["data_source_id"]
        pending.append(e)

    BATCH_DIR.mkdir(exist_ok=True)
    jobs: list[dict] = []
    i = 0
    idx = 0
    while i < len(pending):
        chunk = []
        total = 0
        while i < len(pending) and len(chunk) < 2:
            p = pending[i]
            clen = len(p.get("content", ""))
            if chunk and total + clen > MAX_PAIR_CONTENT:
                break
            if not chunk and clen > MAX_PAIR_CONTENT:
                chunk.append(p)
                i += 1
                break
            chunk.append(p)
            total += clen
            i += 1
        pages = [{"properties": e["properties"], "content": e["content"]} for e in chunk]
        payload = {
            "parent": {"data_source_id": ds_id, "type": "data_source_id"},
            "pages": pages,
            "paths": [e["rel_path"] for e in chunk],
        }
        fp = BATCH_DIR / f"R1-{idx:04d}.json"
        fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        jobs.append({"file": str(fp), "paths": payload["paths"], "content_lens": [len(p["content"]) for p in pages]})
        idx += 1

    STATE.write_text(json.dumps({"job_index": 0, "jobs": len(jobs)}, ensure_ascii=False), encoding="utf-8")
    return {"pending": len(pending), "jobs": len(jobs)}


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"job_index": 0}


def pending_job_files() -> list[Path]:
    done = done_paths()
    out = []
    for fp in sorted(BATCH_DIR.glob("R1-*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        if any(p not in done for p in data.get("paths", [])):
            out.append(fp)
    return out


def emit() -> dict:
    files = pending_job_files()
    if not files:
        return {"done": True, **status()}
    fp = files[0]
    data = json.loads(fp.read_text(encoding="utf-8"))
    mcp = {"parent": data["parent"], "pages": data["pages"]}
    MCP_OUT.write_text(json.dumps(mcp, ensure_ascii=False), encoding="utf-8")
    out = {
        "file": str(fp),
        "paths": data["paths"],
        "content_lens": [len(p.get("content", "")) for p in data["pages"]],
        "mcp_file": str(MCP_OUT),
        "remaining_jobs": len(files),
        **status(),
    }
    Path("/tmp/notion-r1-last-paths.json").write_text(json.dumps(data["paths"], ensure_ascii=False), encoding="utf-8")
    return out


def record() -> dict:
    paths = json.loads(Path("/tmp/notion-r1-last-paths.json").read_text(encoding="utf-8"))
    with PROGRESS.open("a", encoding="utf-8") as f:
        for rel in paths:
            f.write(json.dumps({"rel_path": rel, "status": "synced"}, ensure_ascii=False) + "\n")
    return status()


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
    return {"batch": "R1", "total": total, "synced": total - pending, "pending": pending, "pending_jobs": len(pending_job_files())}


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "prepare":
        print(json.dumps(prepare(), ensure_ascii=False))
    elif cmd == "emit":
        print(json.dumps(emit(), ensure_ascii=False))
    elif cmd == "paths":
        p = Path("/tmp/notion-r1-last-paths.json")
        print(p.read_text(encoding="utf-8") if p.exists() else "[]")
    elif cmd == "record":
        print(json.dumps(record(), ensure_ascii=False))
    elif cmd == "status":
        print(json.dumps(status(), ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
