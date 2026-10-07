#!/usr/bin/env bash
# Push all pending K1/H1 batches: prints one JSON line per batch for agent MCP calls.
set -euo pipefail
SYNC_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SYNC_DIR/notion-push-execute.py" list | python3 -c "
import json, sys
for f in json.load(sys.stdin):
    d=json.load(open(f))
    print(json.dumps({
        'file': f,
        'batch': d['batch'],
        'rel_paths': d['rel_paths'],
        'parent': d['parent'],
        'pages': d['pages'],
    }, ensure_ascii=False))
"
