#!/usr/bin/env bash
# Bootstrap: open all Cursor Automation drafts + print checklist (user Save once each).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
AUTO="$DIR/../../../.cursor/automations"
echo "Lovart Automation Bootstrap"
echo "Workflow JSONs in: $AUTO"
ls -1 "$AUTO"/*.workflow.json 2>/dev/null || true
echo ""
echo "1. Cursor → Automations → import each JSON (or ask Agent open_automation)"
echo "2. Run once each after Save"
echo "3. Unload launchd: bash $DIR/unload-all-launchd.sh"
echo "4. Notion DB: Lovart Ops Reports (see automation-reports/notion-config.json)"
