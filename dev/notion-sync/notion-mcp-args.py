#!/usr/bin/env python3
"""Push one prepared batch file via Notion MCP (stdin JSON args for external caller)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(data["mcp"], ensure_ascii=False))
