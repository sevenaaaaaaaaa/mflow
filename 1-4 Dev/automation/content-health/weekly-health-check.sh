#!/usr/bin/env bash
# Weekly Sanity content health check (auth, future dates, cover/composite 404, light preflight).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$PROJECT_ROOT/local-dev-env.sh"
ensure_lovart_local_dev_dirs
STUDIO="$PROJECT_ROOT/../lovart.sanity.studio"
PULL_DIR="${LOVART_PULL_DIR:-$LOVART_LOCAL_TEMP_DIR/lovart/pull}"
STAMP="$(date +%Y%m)"
AUDIT_ARCHIVE="${LOVART_AUDIT_ARCHIVE:-$LOVART_LOCAL_OUTPUT_DIR/quality-audits/$(date +%Y-%m)}"

mkdir -p "$PULL_DIR" "$AUDIT_ARCHIVE"

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
