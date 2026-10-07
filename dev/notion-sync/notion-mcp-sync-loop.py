#!/usr/bin/env python3
"""Prepare next MCP batch from sync-queue for agent-driven push loop."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
QUEUE = SYNC / "sync-queue.jsonl"
PROGRESS = SYNC / "sync-pushed.jsonl"
PUSH = SYNC / "notion-push-batch.py"
RECORD = SYNC / "notion-record-push.py"
OUT_DIR = Path("/tmp/notion-mcp-sync")
LARGE = 30000
CHUNK = 14000
BATCH_ORDER = ("K1", "H1", "S1", "R2", "R1")


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def done_paths() -> set[str]:
    s: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                s.add(json.loads(line)["rel_path"])
    return s


def counts() -> dict:
    done = done_paths()
    out: dict[str, dict[str, int]] = {}
    for b in BATCH_ORDER + ("R3", "A1"):
        total = synced = 0
        for line in QUEUE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != b:
                continue
            total += 1
            if e["rel_path"] in done:
                synced += 1
        out[b] = {"total": total, "synced": synced, "pending": total - synced}
    done_n = len(done)
    return {
        "synced_unique": done_n,
        "pending_total": sum(v["pending"] for v in out.values()),
        "by_batch": out,
    }


def next_batch_for(batch: str, limit: int) -> dict | None:
    raw = subprocess.check_output(
        [sys.executable, str(PUSH), batch, str(limit)], text=True, encoding="utf-8"
    )
    data = json.loads(raw)
    if data["count"] == 0:
        return None
    pages = []
    paths = []
    ops = []
    for p in data["pages"]:
        rel = p["properties"]["Source Path"]
        content = p.get("content", "")
        clen = len(content)
        paths.append(rel)
        if clen >= LARGE:
            pages.append({"properties": p["properties"]})
            body = strip_h1(content)
            chunks = [body[i : i + CHUNK] for i in range(0, len(body), CHUNK)] or [""]
            ops.append(
                {
                    "rel_path": rel,
                    "mode": "large",
                    "chunks": len(chunks),
                    "followups": [
                        {"tool": "notion-update-page", "phase": "replace" if i == 0 else "insert", "chunk_idx": i}
                        for i in range(len(chunks))
                    ],
                }
            )
        else:
            pages.append({"properties": p["properties"], "content": strip_h1(content)})
            ops.append({"rel_path": rel, "mode": "inline", "content_len": clen})
    return {
        "batch": batch,
        "parent": data["parent"],
        "pages": pages,
        "paths": paths,
        "ops": ops,
        "mcp": {"parent": data["parent"], "pages": pages},
    }


def find_next_batch(limit: int = 5) -> dict | None:
    for batch in BATCH_ORDER:
        payload = next_batch_for(batch, limit)
        if payload:
            return payload
    return None


def prepare(limit: int = 5) -> dict:
    OUT_DIR.mkdir(exist_ok=True)
    payload = find_next_batch(limit)
    if not payload:
        return {"done": True, **counts()}
    # store chunk bodies for large R1 follow-ups
    chunk_file = OUT_DIR / "chunks.json"
    chunk_map: dict[str, list[str]] = {}
    if any(op["mode"] == "large" for op in payload["ops"]):
        for p, op in zip(payload["pages"], payload["ops"]):
            if op["mode"] != "large":
                continue
            rel = op["rel_path"]
            for line in QUEUE.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                e = json.loads(line)
                if e["rel_path"] == rel:
                    body = strip_h1(e["content"])
                    chunk_map[rel] = [body[i : i + CHUNK] for i in range(0, len(body), CHUNK)] or [""]
                    break
        chunk_file.write_text(json.dumps(chunk_map, ensure_ascii=False), encoding="utf-8")
    mcp_file = OUT_DIR / "create.json"
    mcp_file.write_text(json.dumps(payload["mcp"], ensure_ascii=False), encoding="utf-8")
    meta_file = OUT_DIR / "meta.json"
    meta = {
        "batch": payload["batch"],
        "paths": payload["paths"],
        "ops": payload["ops"],
        "mcp_file": str(mcp_file),
        "chunk_file": str(chunk_file) if chunk_map else None,
        "counts": counts(),
    }
    meta_file.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return meta


def record(paths: list[str]) -> dict:
    if paths:
        subprocess.check_call([sys.executable, str(RECORD), *paths])
    return counts()


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if cmd == "status":
        print(json.dumps(counts(), ensure_ascii=False, indent=2))
    elif cmd == "prepare":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        print(json.dumps(prepare(limit), ensure_ascii=False))
    elif cmd == "record":
        print(json.dumps(record(sys.argv[2:]), ensure_ascii=False))
    elif cmd == "chunk":
        rel = sys.argv[2]
        idx = int(sys.argv[3])
        chunk_map = json.loads((OUT_DIR / "chunks.json").read_text(encoding="utf-8"))
        print(json.dumps({"rel_path": rel, "chunk_idx": idx, "content": chunk_map[rel][idx]}, ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
