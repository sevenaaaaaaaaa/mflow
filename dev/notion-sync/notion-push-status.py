#!/usr/bin/env python3
"""Push all pending batches from .batch-out via Notion MCP (run inside Cursor agent)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
APPLY = SYNC / "notion-apply-batch.py"
PUSH = SYNC / "notion-push-batch.py"


def pending_batches() -> list[str]:
    batches = ["R2", "R3", "A1"]
    out = []
    for batch in batches:
        while True:
            raw = subprocess.check_output(
                [sys.executable, str(PUSH), batch, "3"], text=True, encoding="utf-8"
            )
            data = json.loads(raw)
            if data["count"] == 0:
                break
            out.append((batch, data))
    return out


def main() -> None:
    summary: dict[str, int] = {"R2": 0, "R3": 0, "A1": 0}
    pending = pending_batches()
    print(json.dumps({"pending_calls": len(pending), "preview": [
        {"batch": b, "count": d["count"], "names": [p["properties"].get("Name") for p in d["pages"]]}
        for b, d in pending[:5]
    ]}, ensure_ascii=False, indent=2))
    print("\nAgent: for each pending batch, call notion-create-pages with parent+pages, then notion-record-push.py", file=sys.stderr)


if __name__ == "__main__":
    main()
