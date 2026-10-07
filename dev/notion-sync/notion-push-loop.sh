#!/usr/bin/env bash
# Prepare batch payloads for Notion MCP push. Run from agent with CallMcpTool per batch file.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SYNC_DIR="$(dirname "$0")"
OUT_DIR="/tmp/notion-push-batches"
mkdir -p "$OUT_DIR"
rm -f "$OUT_DIR"/*.json

for BATCH in K1 H1; do
  i=0
  while true; do
    payload=$(python3 "$SYNC_DIR/notion-push-next.py" "$BATCH" 3)
    count=$(echo "$payload" | python3 -c "import sys,json; print(json.load(sys.stdin)['count'])")
    if [ "$count" -eq 0 ]; then
      break
    fi
    i=$((i+1))
    file="$OUT_DIR/${BATCH}-${i}.json"
    echo "$payload" | python3 -c "
import sys, json
d=json.load(sys.stdin)
with open('$file','w',encoding='utf-8') as f:
    json.dump({'parent': d['parent'], 'pages': d['pages'], 'rel_paths': d['rel_paths']}, f, ensure_ascii=False)
print('$file', d['count'], d['rel_paths'])
"
    # Simulate push by recording - REMOVE in production; agent records after MCP success
  done
done

python3 "$SYNC_DIR/notion-push-next.py" counts
