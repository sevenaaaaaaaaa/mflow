#!/usr/bin/env python3
"""Apply one prepared batch file to sync-pushed.jsonl after MCP success."""
import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
RECORD = SYNC / "notion-record-push.py"


def main() -> None:
    batch_file = Path(sys.argv[1])
    data = json.loads(batch_file.read_text(encoding="utf-8"))
    subprocess.check_call([sys.executable, str(RECORD), *data["rel_paths"]])
    print(json.dumps({"batch": data["batch"], "index": data["index"], "count": data["count"], "rel_paths": data["rel_paths"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
