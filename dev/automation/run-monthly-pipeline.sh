#!/usr/bin/env bash
# Monthly the brand ops: SEO monthly + content audit + sentinel summary.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
NOTIFY="$SCRIPT_DIR/report-notify/report-notify.sh"
source "$SCRIPT_DIR/local-dev-env.sh"
PYTHON="${MFLOW_PYTHON:-python3}"
ensure_mflow_local_dev_dirs
STAMP="$(date +%Y-%m-%d)"
FAIL=0

# Previous calendar month YYYY-MM (macOS / Linux)
if date -v-1m +%Y-%m >/dev/null 2>&1; then
  MONTH="$(date -v-1m +%Y-%m)"
else
  MONTH="$(date -d 'last month' +%Y-%m)"
fi

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

cd "$PROJECT_ROOT"
STUDIO="$PROJECT_ROOT/dev/mflow.sanity.studio"

# M01 SEO monthly
if [[ -f "$PROJECT_ROOT/dev/scripts/seo_monthly_v2.py" ]]; then
  run_step "seo-monthly" "$PYTHON" "$PROJECT_ROOT/dev/scripts/seo_monthly_v2.py" --month "$MONTH" \
    && notify seo-monthly ok "SEO monthly $MONTH generated $STAMP" "insight-data/Trident Insights/reports/monthly/" \
    || notify seo-monthly fail "SEO monthly $MONTH failed $STAMP" ""
else
  echo "SKIP seo-monthly"
fi

# M03 Content quality audit
if [[ -f "$STUDIO/scripts/audit-content-quality.js" ]]; then
  run_step "content-audit" bash -c "cd \"$STUDIO\" && node scripts/audit-content-quality.js" \
    && notify content-audit ok "Content audit completed $STAMP" "$MFLOW_LOCAL_OUTPUT_DIR/quality-audits/" \
    || notify content-audit fail "Content audit failed $STAMP" ""
else
  echo "SKIP content-audit (audit-content-quality.js missing)"
fi

# M02 Sentinel monthly-style rollup (weekly mode on month boundary)
SENTINEL="$PROJECT_ROOT/dev/scripts/sentinel"
if [[ -f "$SENTINEL/report.py" ]]; then
  run_step "sentinel-monthly" "$PYTHON" "$SENTINEL/report.py" --mode weekly \
    && notify sentinel-monthly ok "Sentinel monthly rollup $STAMP" "insight-data/ORM/" \
    || notify sentinel-monthly fail "Sentinel monthly failed $STAMP" ""
fi

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  notify monthly-pipeline ok "Monthly pipeline ok for $MONTH ($STAMP)" "$MFLOW_LOCAL_OUTPUT_DIR/automation-reports/"
  echo "✅ Monthly pipeline complete ($MONTH)"
  exit 0
fi
notify monthly-pipeline fail "Monthly pipeline failures $MONTH ($STAMP)" "$MFLOW_LOCAL_OUTPUT_DIR/automation-reports/"
exit 1
