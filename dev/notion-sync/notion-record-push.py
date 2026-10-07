#!/usr/bin/env python3
import json, sys
from pathlib import Path
PROGRESS = Path(__file__).parent / "sync-pushed.jsonl"
for rel in sys.argv[1:]:
    PROGRESS.open("a", encoding="utf-8").write(json.dumps({"rel_path": rel, "status": "synced"}, ensure_ascii=False) + "\n")
