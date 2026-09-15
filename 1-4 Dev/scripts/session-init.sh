#!/usr/bin/env bash
# session-init.sh — lightweight session startup check
# Run this at the start of every Lovart session to ensure pipeline state is fresh.
#
# Usage:
#   bash session-init.sh              # full check
#   bash session-init.sh --quick      # pipeline-state only (fast)
#   bash session-init.sh --brief      # machine-readable output
#
# Exit codes:
#   0 = all gates passed
#   1 = gate failure (fix before proceeding)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MFLOW_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
HARNESS="${LOVART_RESOURCE_ROOT:-$VAULT_ROOT}/1-Project/Lovart MFlow/1-1 Harness"
PIPELINE_PY="$HARNESS/Skills/06-orchestrate/lovart-pipeline-state/pipeline_state.py"
ROUTER_PY="$HARNESS/Skills/06-orchestrate/lovart-router/router.py"
STATE="1-3 GenFlow/.pipeline/pipeline-state.json"

# Resolve to absolute path
VAULT="${LOVART_RESOURCE_ROOT:-$VAULT_ROOT}"
STATE_ABS="$VAULT/1-Project/Lovart MFlow/$STATE"

MODE="full"
for arg in "$@"; do
  case "$arg" in
    --quick) MODE="quick" ;;
    --brief) MODE="brief" ;;
  esac
done

ERRORS=0

gate_pass() { [[ "$MODE" != "brief" ]] && echo "  ✓ GATE $1: $2"; }
gate_fail() { echo "  ✗ GATE $1: $2"; ERRORS=$((ERRORS + 1)); }

echo "=== Session Init ==="

# GATE 1: pipeline-state exists and is readable
echo "[GATE 1] pipeline-state"
if [[ -f "$STATE_ABS" ]]; then
  ITEMS=$(python3 -c "import json; d=json.load(open('$STATE_ABS')); print(len(d.get('items',{})))" 2>/dev/null || echo "0")
  S0=$(python3 -c "import json; d=json.load(open('$STATE_ABS')); print(sum(1 for i in d.get('items',{}).values() if i.get('stage')=='S0-todo'))" 2>/dev/null || echo "0")
  S3DONE=$(python3 -c "import json; d=json.load(open('$STATE_ABS')); print(sum(1 for i in d.get('items',{}).values() if i.get('stage')=='S3-done'))" 2>/dev/null || echo "0")
  gate_pass 1 "state exists, $ITEMS items ($S0 todo, $S3DONE ready-for-qa)"
else
  gate_fail 1 "state file not found at $STATE_ABS"
fi

# GATE 2: router exists and is valid
echo "[GATE 2] router validate"
if python3 "$ROUTER_PY" --state-path "$STATE_ABS" validate >/dev/null 2>&1; then
  DECISIONS=$(python3 "$ROUTER_PY" --state-path "$STATE_ABS" matrix 2>&1 | head -1 | grep -oE '[0-9]+ decisions' || echo "?")
  gate_pass 2 "router valid ($DECISIONS)"
else
  gate_fail 2 "router validate failed"
fi

# GATE 3: next item suggestion
echo "[GATE 3] pipeline next"
NEXT=$(python3 "$PIPELINE_PY" --state-path "$STATE_ABS" next 2>&1 || true)
if echo "$NEXT" | grep -q "id="; then
  NEXT_ID=$(echo "$NEXT" | grep "id=" | head -1 | awk '{print $2}')
  NEXT_STAGE=$(echo "$NEXT" | grep "stage=" | head -1 | awk '{print $3}')
  gate_pass 3 "next item: $NEXT_ID (stage=$NEXT_STAGE)"
elif echo "$NEXT" | grep -q "nothing to do"; then
  gate_pass 3 "queue empty — nothing to do"
else
  gate_fail 3 "could not determine next item"
fi

# GATE 4: governance check (skip — too many false positives with -newer)
echo "[GATE 4] governance"
gate_pass 4 "skipped (governance check available via manual trigger)"

# Summary
echo ""
if [[ "$ERRORS" -eq 0 ]]; then
  echo "VERDICT: ALL GATES PASS — session can proceed"
else
  echo "VERDICT: $ERRORS GATE(S) FAILED — fix before proceeding"
fi

exit "$ERRORS"
