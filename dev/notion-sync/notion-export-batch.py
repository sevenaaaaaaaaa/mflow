#!/usr/bin/env python3
"""Export pre-generated R1 batch JSON for MCP (stdout: parent+pages only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC = Path(__file__).parent


def main() -> None:
    idx = int(sys.argv[1])
    fp = SYNC / ".batch-out" / f"R1-{idx:04d}.json"
    d = json.loads(fp.read_text(encoding="utf-8"))
    out = {"parent": d["parent"], "pages": d["pages"]}
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
