#!/usr/bin/env bash
# Archive automation run → local vault + optional Feishu; Notion via Agent/MCP follow-up.
#
# Usage:
#   bash report-notify.sh --type seo-weekly --status ok --summary "..." \
#     --artifact "1-2 Insight/Trident Insights/reports/weekly/foo.md"
#
# Env:
#   LOVART_PROJECT_ROOT  (default: auto-detect from script)
#   FEISHU_WEBHOOK_URL   (optional; or feishu.json in trident credentials)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="${LOVART_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
source "$PROJECT_ROOT/1-4 Dev/automation/local-dev-env.sh"
ensure_lovart_local_dev_dirs
DATE="$(date +%Y-%m-%d)"
TIME="$(date +%H:%M:%S)"
STAMP="${DATE}T${TIME}"

TYPE=""
STATUS="ok"
SUMMARY=""
ARTIFACT=""
EXTRA_JSON=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type) TYPE="$2"; shift 2 ;;
    --status) STATUS="$2"; shift 2 ;;
    --summary) SUMMARY="$2"; shift 2 ;;
    --artifact) ARTIFACT="$2"; shift 2 ;;
    --extra-json) EXTRA_JSON="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

[[ -n "$TYPE" ]] || { echo "Missing --type"; exit 1; }

REPORT_DIR="$LOVART_LOCAL_OUTPUT_DIR/automation-reports/$DATE"
mkdir -p "$REPORT_DIR"

MANIFEST="$REPORT_DIR/${TYPE}-${STAMP}.json"
cat > "$MANIFEST" <<EOF
{
  "type": "$TYPE",
  "status": "$STATUS",
  "summary": $(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$SUMMARY"),
  "artifact": "$ARTIFACT",
  "timestamp": "$STAMP",
  "extra": ${EXTRA_JSON:-null}
}
EOF

# Markdown digest for Obsidian + Notion paste
MD="$REPORT_DIR/${TYPE}-${STAMP}.md"
{
  echo "# Lovart Automation Report: $TYPE"
  echo ""
  echo "| Field | Value |"
  echo "|-------|-------|"
  echo "| Status | **$STATUS** |"
  echo "| Time | $STAMP |"
  echo "| Artifact | ${ARTIFACT:-—} |"
  echo ""
  echo "## Summary"
  echo ""
  echo "$SUMMARY"
  echo ""
  echo "## Next actions"
  echo ""
  if [[ "$STATUS" == "ok" ]]; then
    echo "- [ ] Sync to Notion (Ops Reports database)"
    echo "- [ ] If SEO/Sentinel gap: run content-generation automation"
    echo "- [ ] If publish batch: run quality-gates automation"
  else
    echo "- [ ] **Do not publish** until resolved"
    echo "- [ ] Check Anti-Bugs registry for matching AB-* id"
  fi
} > "$MD"

# Rolling index
INDEX="$LOVART_LOCAL_OUTPUT_DIR/automation-reports/INDEX.md"
{
  echo "| $STAMP | $TYPE | $STATUS | [$MD]($MD) |"
} >> "$INDEX"

echo "Local report → $MD"
echo "Manifest → $MANIFEST"

# Feishu (optional)
FEISHU_JSON="$PROJECT_ROOT/1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials/feishu.json"
WEBHOOK="${FEISHU_WEBHOOK_URL:-}"
if [[ -z "$WEBHOOK" && -f "$FEISHU_JSON" ]]; then
  WEBHOOK="$(python3 -c "import json; print(json.load(open('$FEISHU_JSON')).get('webhook_url',''))" 2>/dev/null || true)"
fi

if [[ -n "$WEBHOOK" ]]; then
  ICON="✅"
  [[ "$STATUS" != "ok" ]] && ICON="🚨"
  PAYLOAD=$(python3 - <<PY
import json
print(json.dumps({
  "msg_type": "text",
  "content": {"text": f"$ICON Lovart [$TYPE] $STATUS\\n$SUMMARY\\n$MD"}
}))
PY
)
  curl -sf -X POST "$WEBHOOK" -H "Content-Type: application/json" -d "$PAYLOAD" >/dev/null \
    && echo "Feishu → sent" || echo "Feishu → failed (check webhook)"
else
  echo "Feishu → skipped (no webhook)"
fi

# Email: macOS mail stub (set LOVART_REPORT_EMAIL to enable)
if [[ -n "${LOVART_REPORT_EMAIL:-}" ]]; then
  SUBJECT="Lovart [$TYPE] $STATUS — $DATE"
  mail -s "$SUBJECT" "$LOVART_REPORT_EMAIL" < "$MD" 2>/dev/null && echo "Email → $LOVART_REPORT_EMAIL" || echo "Email → failed"
fi

echo ""
echo "Notion DB: Lovart Ops Reports"
NOTION_CFG="$LOVART_LOCAL_OUTPUT_DIR/automation-reports/notion-config.json"
if [[ -f "$NOTION_CFG" ]]; then
  python3 -c "import json; c=json.load(open('$NOTION_CFG')); print('  url:', c.get('database_url','')); print('  data_source_id:', c.get('data_source_id',''))"
fi
echo "Notion: Agent uses notion-create-pages (see automation/NOTION-TAIL.md)"
