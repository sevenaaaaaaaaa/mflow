#!/usr/bin/env bash
# Weekly the brand ops pipeline (local SSOT — Cursor Automation should call this).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$SCRIPT_DIR/local-dev-env.sh"
PYTHON="${MFLOW_PYTHON:-python3}"
ensure_mflow_local_dev_dirs
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
if [[ -f "$PROJECT_ROOT/harness/Skills/01-strategy/trident-data-engine/scripts/run_all.sh" ]]; then
  run_step "trident-weekly" bash "$PROJECT_ROOT/harness/Skills/01-strategy/trident-data-engine/scripts/run_all.sh" \
    && notify trident-weekly ok "Trident weekly fetch completed $STAMP" "$MFLOW_LOCAL_OUTPUT_DIR/Data Ingestion/" \
    || notify trident-weekly fail "Trident weekly failed $STAMP" ""
else
  echo "SKIP trident (run_all.sh missing)"
fi

# 2 Tools pull
run_step "tools-pull" bash "$SCRIPT_DIR/tools-pull/pull-tools-from-production.sh" \
  && notify tools-pull ok "Tools pull completed $STAMP" "$MFLOW_LOCAL_OUTPUT_DIR/composite-v2-audit/pull-tools-latest.json" \
  || notify tools-pull fail "Tools pull failed $STAMP" ""

# 3 Content health
run_step "content-health" bash "$SCRIPT_DIR/content-health/weekly-health-check.sh" \
  && notify content-health ok "Weekly health check passed $STAMP" "$MFLOW_LOCAL_TEMP_DIR/mflow/pull/" \
  || notify content-health fail "Weekly health check failed $STAMP" "$MFLOW_LOCAL_TEMP_DIR/mflow/pull/"

# 3.5 主站内容全语言审计（节奏/开关在 dev/automation/quality-cadence.json mainContentAudit.weekly）
MAIN_AUDIT_DIR="$PROJECT_ROOT/run/main-audit"
mkdir -p "$MAIN_AUDIT_DIR"
if [[ "$(python3 -c "import json;print(json.load(open('$PROJECT_ROOT/dev/automation/quality-cadence.json'))['mainContentAudit']['weekly']['enabled'])" 2>/dev/null)" == "True" ]]; then
  AUDIT_JSON="$MAIN_AUDIT_DIR/main-audit-weekly-$STAMP.json"
  run_step "main-content-audit" env PYTHONIOENCODING=utf-8 "$PYTHON" "$PROJECT_ROOT/dev/scripts/audit-main-content.py" \
    --out "$AUDIT_JSON" --md "$MAIN_AUDIT_DIR/main-audit-weekly-$STAMP.md" \
    && notify main-content-audit ok "Main-site content audit done $STAMP" "$MAIN_AUDIT_DIR" \
    || notify main-content-audit fail "Main-site content audit failed $STAMP" ""
  # 3.6 主站修复计划：机械 patch（field_patch 批量用）+ 重写队列（后台 preset 消费）
  if [[ -f "$AUDIT_JSON" ]] && [[ "$(python3 -c "import json;print(json.load(open('$PROJECT_ROOT/dev/automation/quality-cadence.json'))['mainContentFix']['enabled'])" 2>/dev/null)" == "True" ]]; then
    run_step "main-content-fixplan" env PYTHONIOENCODING=utf-8 "$PYTHON" "$PROJECT_ROOT/dev/scripts/fix-main-content.py" \
      --audit "$AUDIT_JSON" --outdir "$MAIN_AUDIT_DIR" --write-patch \
      && notify main-content-fixplan ok "Main-site fix plan + rewrite queue refreshed $STAMP" "$MAIN_AUDIT_DIR" \
      || notify main-content-fixplan fail "Main-site fix plan failed $STAMP" ""
  fi
else
  echo "SKIP main-content-audit (quality-cadence weekly disabled)"
fi

# 4 SEO weekly
if [[ -f "$PROJECT_ROOT/dev/scripts/weekly_review_v3.py" ]]; then
  run_step "seo-weekly" "$PYTHON" "$PROJECT_ROOT/dev/scripts/weekly_review_v3.py" \
    && notify seo-weekly ok "SEO weekly report generated $STAMP" "insight-data/Trident Insights/reports/weekly/" \
    || notify seo-weekly fail "SEO weekly failed $STAMP" ""
else
  echo "SKIP seo-weekly (script missing)"
fi

# 5 Sentinel weekly
SENTINEL="$PROJECT_ROOT/dev/scripts/sentinel"
if [[ -f "$SENTINEL/report.py" ]]; then
  run_step "sentinel-weekly" "$PYTHON" "$SENTINEL/report.py" --mode weekly \
    && notify sentinel-weekly ok "Sentinel weekly report $STAMP" "insight-data/ORM/weekly/" \
    || notify sentinel-weekly fail "Sentinel weekly failed $STAMP" ""
else
  echo "SKIP sentinel-weekly"
fi

# Optional: chain post-SEO content webhook when weekly SEO ok
if [[ "$FAIL" -eq 0 && -n "${MFLOW_POST_SEO_WEBHOOK:-}" ]]; then
  echo ""
  echo "========== post-seo-webhook =========="
  if curl -sf -X POST "$MFLOW_POST_SEO_WEBHOOK" -H "Content-Type: application/json" \
    -d "{\"source\":\"weekly-pipeline\",\"date\":\"$STAMP\",\"status\":\"ok\"}"; then
    notify post-seo-trigger ok "Post-SEO webhook fired $STAMP" ""
  else
    notify post-seo-trigger warn "Post-SEO webhook failed $STAMP" ""
  fi
fi

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  notify weekly-pipeline ok "All weekly pipeline steps passed $STAMP" "$MFLOW_LOCAL_OUTPUT_DIR/automation-reports/"
  echo "✅ Weekly pipeline complete"
  exit 0
fi
notify weekly-pipeline fail "One or more weekly steps failed $STAMP" "$MFLOW_LOCAL_OUTPUT_DIR/automation-reports/"
echo "❌ Weekly pipeline had failures"
exit 1
