#!/usr/bin/env bash
# Monthly Lovart ops: SEO monthly + content audit + sentinel summary.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
NOTIFY="$SCRIPT_DIR/report-notify/report-notify.sh"
source "$SCRIPT_DIR/local-dev-env.sh"
PYTHON="${LOVART_PYTHON:-python3}"
ensure_lovart_local_dev_dirs
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
STUDIO="$PROJECT_ROOT/1-4 Dev/lovart.sanity.studio"

# M01 SEO monthly
if [[ -f "$PROJECT_ROOT/1-4 Dev/scripts/seo_monthly_v2.py" ]]; then
  run_step "seo-monthly" "$PYTHON" "$PROJECT_ROOT/1-4 Dev/scripts/seo_monthly_v2.py" --month "$MONTH" \
    && notify seo-monthly ok "SEO monthly $MONTH generated $STAMP" "1-2 Insight/Trident Insights/reports/monthly/" \
    || notify seo-monthly fail "SEO monthly $MONTH failed $STAMP" ""
else
  echo "SKIP seo-monthly"
fi

# M03 Content quality audit
if [[ -f "$STUDIO/scripts/audit-content-quality.js" ]]; then
  run_step "content-audit" bash -c "cd \"$STUDIO\" && node scripts/audit-content-quality.js" \
    && notify content-audit ok "Content audit completed $STAMP" "$LOVART_LOCAL_OUTPUT_DIR/quality-audits/" \
    || notify content-audit fail "Content audit failed $STAMP" ""
else
  echo "SKIP content-audit (audit-content-quality.js missing)"
fi

# M02 Sentinel monthly-style rollup (weekly mode on month boundary)
SENTINEL="$PROJECT_ROOT/1-4 Dev/scripts/sentinel"
if [[ -f "$SENTINEL/report.py" ]]; then
  run_step "sentinel-monthly" "$PYTHON" "$SENTINEL/report.py" --mode weekly \
    && notify sentinel-monthly ok "Sentinel monthly rollup $STAMP" "1-2 Insight/Lovart ORM/" \
    || notify sentinel-monthly fail "Sentinel monthly failed $STAMP" ""
fi

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  notify monthly-pipeline ok "Monthly pipeline ok for $MONTH ($STAMP)" "$LOVART_LOCAL_OUTPUT_DIR/automation-reports/"
  echo "✅ Monthly pipeline complete ($MONTH)"
  exit 0
fi
notify monthly-pipeline fail "Monthly pipeline failures $MONTH ($STAMP)" "$LOVART_LOCAL_OUTPUT_DIR/automation-reports/"
exit 1
