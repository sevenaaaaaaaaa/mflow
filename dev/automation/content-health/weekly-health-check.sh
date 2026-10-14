#!/usr/bin/env bash
# Weekly Sanity content health check (auth, future dates, cover/composite 404, light preflight).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
source "$SCRIPT_DIR/../local-dev-env.sh"
ensure_mflow_local_dev_dirs
STUDIO="${SANITY_STUDIO_DIR:-$PROJECT_ROOT/dev/mflow.sanity.studio}"
# API-only fallback when the studio checkout is absent (site-specific → ops/, not in the public repo)
FALLBACK="${MFLOW_CONTENT_HEALTH_FALLBACK:-$PROJECT_ROOT/ops/content-health/fallback-health-audit.py}"
PULL_DIR="${MFLOW_PULL_DIR:-$MFLOW_LOCAL_TEMP_DIR/mflow/pull}"
STAMP="$(date +%Y%m)"
AUDIT_ARCHIVE="${MFLOW_AUDIT_ARCHIVE:-$MFLOW_LOCAL_OUTPUT_DIR/quality-audits/$(date +%Y-%m)}"

mkdir -p "$PULL_DIR" "$AUDIT_ARCHIVE"

if [[ ! -d "$STUDIO/scripts" ]]; then
  echo "⚠️  Sanity studio not found at $STUDIO (set SANITY_STUDIO_DIR) — skipping studio checks."
  if [[ -f "$FALLBACK" ]]; then
    echo "=== fallback: API-only audit ($FALLBACK) ==="
    MFLOW_AUDIT_DIR="$MFLOW_LOCAL_OUTPUT_DIR/quality-audits" "${MFLOW_PYTHON:-python3}" "$FALLBACK"
    echo "✅ fallback audit complete"
    exit 0
  fi
  echo "No fallback audit at $FALLBACK" >&2
  exit 1
fi

cd "$STUDIO"

echo "=== check-sanity-auth ==="
node scripts/check-sanity-auth.js

echo "=== audit-blog-future-release-dates ==="
node scripts/audit-blog-future-release-dates.js --report "$PULL_DIR/blog-future-dates.json"

echo "=== audit-blog-covers ==="
node scripts/audit-blog-covers.js --check-http --report "$PULL_DIR/blog-cover-audit-$STAMP.json"

echo "=== audit-composite-images-404 ==="
node scripts/audit-composite-images-404.js --report "$PULL_DIR/composite-image-404-$STAMP.json"

echo "=== preflight tools (sample) ==="
node scripts/preflight-content.js --type tools --sample-urls 5

echo "=== preflight features (sample) ==="
node scripts/preflight-content.js --type features --sample-urls 5

cp "$PULL_DIR/blog-future-dates.json" "$AUDIT_ARCHIVE/" 2>/dev/null || true
cp "$PULL_DIR/blog-cover-audit-$STAMP.json" "$AUDIT_ARCHIVE/" 2>/dev/null || true
cp "$PULL_DIR/composite-image-404-$STAMP.json" "$AUDIT_ARCHIVE/" 2>/dev/null || true

echo "✅ weekly health check complete — reports in $PULL_DIR and $AUDIT_ARCHIVE"
