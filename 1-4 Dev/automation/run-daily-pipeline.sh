#!/usr/bin/env bash
# Daily Lovart ops: GSC fetch → Sentinel collect/report → Feishu summary.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
NOTIFY="$SCRIPT_DIR/report-notify/report-notify.sh"
source "$SCRIPT_DIR/local-dev-env.sh"
ensure_lovart_local_dev_dirs
# GSC/GA4 API pulls need google-* libs — use the trident venv (falls back to system python3)
PYTHON="${LOVART_PYTHON:-python3}"
STAMP="$(date +%Y-%m-%d)"
FAIL=0

notify() {
  bash "$NOTIFY" --type "$1" --status "$2" --summary "$3" --artifact "${4:-}" || true
}

run_step() {
  local name="$1"
  shift
  echo ""
  echo "========== $name =========="
  if "$@"; then
    echo "OK: $name"
    return 0
  else
    echo "FAIL: $name"
    FAIL=1
    return 1
  fi
}

gsc_script() {
  local p
  for p in \
    "$PROJECT_ROOT/1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/scripts/gsc_fetch.py" \
    "$PROJECT_ROOT/1-4 Dev/scripts/trident/gsc_fetch.py"; do
    [[ -f "$p" ]] && { echo "$p"; return 0; }
  done
  return 1
}

feishu_script() {
  local p
  for p in \
    "$PROJECT_ROOT/1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/scripts/push_to_feishu.py" \
    "$PROJECT_ROOT/1-4 Dev/scripts/trident/push_to_feishu.py"; do
    [[ -f "$p" ]] && { echo "$p"; return 0; }
  done
  return 1
}

cd "$PROJECT_ROOT"

# D01 GSC daily
if GSC="$(gsc_script)"; then
  run_step "gsc-daily" "$PYTHON" "$GSC" --daily \
    && notify gsc-daily ok "GSC daily fetch $STAMP" "1-2 Insight/Trident Insights/" \
    || notify gsc-daily fail "GSC daily failed $STAMP" ""
else
  echo "SKIP gsc-daily (script missing)"
fi

# D02/D03 Sentinel
SENTINEL="$PROJECT_ROOT/1-4 Dev/scripts/sentinel"
if [[ -f "$SENTINEL/collect.py" && -f "$SENTINEL/report.py" ]]; then
  run_step "sentinel-collect" "$PYTHON" "$SENTINEL/collect.py" --brand lovart --mode daily --source all \
    && run_step "sentinel-daily" "$PYTHON" "$SENTINEL/report.py" --mode daily \
    && notify sentinel-daily ok "Sentinel daily $STAMP" "1-2 Insight/Lovart ORM/daily/" \
    || notify sentinel-daily fail "Sentinel daily failed $STAMP" ""
else
  echo "SKIP sentinel (scripts missing)"
fi

# D05 Feishu daily summary (optional — needs webhook)
if FEISHU="$(feishu_script)"; then
  if "$PYTHON" "$FEISHU" --daily-summary 2>/dev/null; then
    notify feishu-daily ok "Feishu daily summary sent $STAMP" ""
  else
    echo "SKIP feishu-daily (no webhook or push failed — non-fatal)"
    notify feishu-daily warn "Feishu daily skipped or failed $STAMP" ""
  fi
else
  echo "SKIP feishu-daily (script missing)"
fi

# D06 Harness Auto-Optimization Data Gatherer
HARNESS_AUTO_OPTIMIZE="$PROJECT_ROOT/1-4 Dev/scripts/harness_auto_optimize.py"
if [[ -f "$HARNESS_AUTO_OPTIMIZE" ]]; then
  run_step "harness-auto-optimize" "$PYTHON" "$HARNESS_AUTO_OPTIMIZE" \
    && notify harness-auto-optimize ok "Harness daily learning report generated $STAMP" "1-2 Insight/Harness-Learning/" \
    || notify harness-auto-optimize fail "Harness daily learning failed $STAMP" ""
else
  echo "SKIP harness-auto-optimize (script missing)"
fi

# D07 Harness Sync & Compile
HARNESS_SYNC="$PROJECT_ROOT/1-4 Dev/scripts/harness_sync.py"
if [[ -f "$HARNESS_SYNC" ]]; then
  run_step "harness-sync" "$PYTHON" "$HARNESS_SYNC" \
    && notify harness-sync ok "Harness rules synchronized across all clients $STAMP" "" \
    || notify harness-sync fail "Harness sync failed $STAMP" ""
else
  echo "SKIP harness-sync (script missing)"
fi

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  notify daily-pipeline ok "Daily pipeline ok $STAMP" "$LOVART_LOCAL_OUTPUT_DIR/automation-reports/"
  echo "✅ Daily pipeline complete"
  exit 0
fi
notify daily-pipeline fail "Daily pipeline had failures $STAMP" "$LOVART_LOCAL_OUTPUT_DIR/automation-reports/"
echo "❌ Daily pipeline had failures"
exit 1
