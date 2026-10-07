#!/usr/bin/env python3
"""Push pending sync batches to Notion via MCP-style JSON + record progress."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC_DIR = Path(__file__).parent
QUEUE = SYNC_DIR / "sync-queue.jsonl"
PROGRESS = SYNC_DIR / "sync-pushed.jsonl"
PUSH = SYNC_DIR / "notion-push-batch.py"
RECORD = SYNC_DIR / "notion-record-push.py"


def emit_batch(batch: str, limit: int = 3) -> dict | None:
    out = subprocess.check_output(
        [sys.executable, str(PUSH), batch, str(limit)],
        text=True,
        encoding="utf-8",
    )
    data = json.loads(out)
    if data["count"] == 0:
        return None
    paths = [p["properties"]["Source Path"] for p in data["pages"]]
    return {"batch": batch, "count": data["count"], "paths": paths, "mcp": data}


def record(paths: list[str]) -> None:
    subprocess.check_call([sys.executable, str(RECORD), *paths])


def push_batch(batch: str, limit: int = 3) -> dict | None:
    payload = emit_batch(batch, limit)
    if not payload:
        return None
    # Caller handles MCP; we only prepare + record after success
    return payload


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: notion-push-loop.py <batch> [limit]", file=sys.stderr)
        sys.exit(1)
    batch = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    payload = emit_batch(batch, limit)
    if not payload:
        print(json.dumps({"batch": batch, "count": 0}))
        return
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
