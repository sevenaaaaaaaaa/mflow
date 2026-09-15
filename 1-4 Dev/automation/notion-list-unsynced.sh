#!/usr/bin/env bash
# List automation-report JSON manifests from last N days (for Notion sync Agent).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$PROJECT_ROOT/1-4 Dev/automation/local-dev-env.sh"
ensure_lovart_local_dev_dirs
REPORTS="$LOVART_LOCAL_OUTPUT_DIR/automation-reports"
DAYS="${1:-7}"

echo "Unsynced candidates (last $DAYS days) — Agent should dedupe by Title+Date in Notion:"
echo "data_source_id: 61514ed3-39e2-4d84-b860-8334d740823e"
echo ""

find "$REPORTS" -name '*.json' -mtime "-${DAYS}" 2>/dev/null | sort -r | while read -r f; do
  python3 -c "
import json, sys
p = sys.argv[1]
d = json.load(open(p))
print(f\"{d.get('timestamp','?')} | {d.get('status','?')} | {d.get('type','?')} | {p}\")
print(f\"  summary: {d.get('summary','')[:120]}\")
" "$f"
done
