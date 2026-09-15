#!/usr/bin/env bash
# Weekly Lovart ops pipeline (local SSOT — Cursor Automation should call this).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$SCRIPT_DIR/local-dev-env.sh"
PYTHON="${LOVART_PYTHON:-python3}"
ensure_lovart_local_dev_dirs
NOTIFY="$SCRIPT_DIR/report-notify/report-notify.sh"
STAMP="$(date +%Y-%m-%d)"
FAIL=0

notify() {
  local type="$1" status="$2" summary="$3" artifact="${4:-}"
  bash "$NOTIFY" --type "$type" --status "$status" --summary "$summary" --artifact "$artifact" || true
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

cd "$PROJECT_ROOT"

# 1 Trident
if [[ -f "$PROJECT_ROOT/1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/scripts/run_all.sh" ]]; then
  run_step "trident-weekly" bash "$PROJECT_ROOT/1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/scripts/run_all.sh" \
    && notify trident-weekly ok "Trident weekly fetch completed $STAMP" "$LOVART_LOCAL_OUTPUT_DIR/Data Ingestion/" \
    || notify trident-weekly fail "Trident weekly failed $STAMP" ""
else
  echo "SKIP trident (run_all.sh missing)"
fi

# 2 Tools pull
run_step "tools-pull" bash "$SCRIPT_DIR/tools-pull/pull-tools-from-production.sh" \
  && notify tools-pull ok "Tools pull completed $STAMP" "$LOVART_LOCAL_OUTPUT_DIR/composite-v2-audit/pull-tools-latest.json" \
  || notify tools-pull fail "Tools pull failed $STAMP" ""

# 3 Content health
run_step "content-health" bash "$SCRIPT_DIR/content-health/weekly-health-check.sh" \
  && notify content-health ok "Weekly health check passed $STAMP" "$LOVART_LOCAL_TEMP_DIR/lovart/pull/" \
  || notify content-health fail "Weekly health check failed $STAMP" "$LOVART_LOCAL_TEMP_DIR/lovart/pull/"

# 4 SEO weekly
if [[ -f "$PROJECT_ROOT/1-4 Dev/scripts/weekly_review_v3.py" ]]; then
  run_step "seo-weekly" "$PYTHON" "$PROJECT_ROOT/1-4 Dev/scripts/weekly_review_v3.py" \
    && notify seo-weekly ok "SEO weekly report generated $STAMP" "1-2 Insight/Trident Insights/reports/weekly/" \
    || notify seo-weekly fail "SEO weekly failed $STAMP" ""
else
  echo "SKIP seo-weekly (script missing)"
fi

# 5 Sentinel weekly
SENTINEL="$PROJECT_ROOT/1-4 Dev/scripts/sentinel"
if [[ -f "$SENTINEL/report.py" ]]; then
  run_step "sentinel-weekly" "$PYTHON" "$SENTINEL/report.py" --mode weekly \
    && notify sentinel-weekly ok "Sentinel weekly report $STAMP" "1-2 Insight/Lovart ORM/weekly/" \
    || notify sentinel-weekly fail "Sentinel weekly failed $STAMP" ""
else
  echo "SKIP sentinel-weekly"
fi

# Optional: chain post-SEO content webhook when weekly SEO ok
if [[ "$FAIL" -eq 0 && -n "${LOVART_POST_SEO_WEBHOOK:-}" ]]; then
  echo ""
  echo "========== post-seo-webhook =========="
  if curl -sf -X POST "$LOVART_POST_SEO_WEBHOOK" -H "Content-Type: application/json" \
    -d "{\"source\":\"weekly-pipeline\",\"date\":\"$STAMP\",\"status\":\"ok\"}"; then
    notify post-seo-trigger ok "Post-SEO webhook fired $STAMP" ""
  else
    notify post-seo-trigger warn "Post-SEO webhook failed $STAMP" ""
  fi
fi

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  notify weekly-pipeline ok "All weekly pipeline steps passed $STAMP" "$LOVART_LOCAL_OUTPUT_DIR/automation-reports/"
  echo "✅ Weekly pipeline complete"
  exit 0
fi
notify weekly-pipeline fail "One or more weekly steps failed $STAMP" "$LOVART_LOCAL_OUTPUT_DIR/automation-reports/"
echo "❌ Weekly pipeline had failures"
exit 1
