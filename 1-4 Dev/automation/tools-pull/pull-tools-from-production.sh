#!/usr/bin/env bash
# Production → local Tools sync (project-level entry; launchd / cron / Cursor Automation).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
STUDIO_DIR="${SANITY_STUDIO_DIR:-$PROJECT_ROOT/1-4 Dev/lovart.sanity.studio}"
source "$PROJECT_ROOT/1-4 Dev/automation/local-dev-env.sh"
ensure_lovart_local_dev_dirs

if [[ ! -d "$STUDIO_DIR/scripts" ]]; then
  echo "Sanity studio scripts not found: $STUDIO_DIR" >&2
  echo "Set SANITY_STUDIO_DIR to lovart.sanity.studio" >&2
  exit 1
fi

export PROJECT_ROOT
export LOVART_LOCAL_DEV_ROOT LOVART_LOCAL_OUTPUT_DIR
cd "$STUDIO_DIR"
exec node scripts/pull-tools-from-production.js "$@"
