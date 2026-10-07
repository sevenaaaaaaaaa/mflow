#!/usr/bin/env python3
"""Prepare next Notion MCP batch: save payload + print rel_paths for recording."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
OUT = Path("/tmp/notion-r1-current-batch.json")


def main() -> None:
    batch = sys.argv[1] if len(sys.argv) > 1 else "R1"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    raw = subprocess.check_output(
        [sys.executable, str(SYNC / "notion-push-batch.py"), batch, str(limit)],
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(raw)
    OUT.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    paths = [p["properties"]["Source Path"] for p in payload["pages"]]
    print(json.dumps({"count": payload["count"], "paths": paths, "file": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
