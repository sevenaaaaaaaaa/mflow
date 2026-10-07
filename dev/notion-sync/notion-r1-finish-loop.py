#!/usr/bin/env python3
"""Prepare R1-only MCP batches until queue empty."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
PUSH = SYNC / "notion-push-batch.py"
OUT = Path("/tmp/notion-r1-finish")
LARGE = 30000
CHUNK = 14000
DS = "235b9609-b155-491e-9801-b1504abe99c2"


def strip_h1(content: str) -> str:
    return re.sub(r"^#\s+.+\n+", "", content, count=1)


def prepare(limit: int = 3) -> dict:
    raw = subprocess.check_output([sys.executable, str(PUSH), "R1", str(limit)], text=True)
    data = json.loads(raw)
    if data["count"] == 0:
        return {"done": True}
    pages = []
    paths = []
    large_ops = []
    queue = {json.loads(l)["rel_path"]: json.loads(l) for l in (SYNC / "sync-queue.jsonl").read_text().splitlines() if l.strip()}
    for p in data["pages"]:
        rel = p["properties"]["Source Path"]
        paths.append(rel)
        content = p.get("content", "")
        body = strip_h1(content)
        if len(content) >= LARGE:
            pages.append({"properties": p["properties"]})
            chunks = [body[i : i + CHUNK] for i in range(0, len(body), CHUNK)] or [""]
            large_ops.append({"rel_path": rel, "chunks": chunks})
        else:
            pages.append({"properties": p["properties"], "content": body})
    OUT.mkdir(exist_ok=True)
    payload = {"parent": {"data_source_id": DS, "type": "data_source_id"}, "pages": pages}
    (OUT / "create.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    meta = {"paths": paths, "large_ops": large_ops, "count": data["count"]}
    (OUT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return meta


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print(json.dumps(prepare(limit), ensure_ascii=False))
