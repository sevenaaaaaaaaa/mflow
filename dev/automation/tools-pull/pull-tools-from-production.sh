#!/usr/bin/env bash
# Production → local Tools sync (project-level entry; launchd / cron / Cursor Automation).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
STUDIO_DIR="${SANITY_STUDIO_DIR:-$PROJECT_ROOT/dev/mflow.sanity.studio}"
source "$PROJECT_ROOT/dev/automation/local-dev-env.sh"
ensure_mflow_local_dev_dirs

if [[ ! -d "$STUDIO_DIR/scripts" ]]; then
  echo "Sanity studio scripts not found: $STUDIO_DIR" >&2
  echo "Set SANITY_STUDIO_DIR to mflow.sanity.studio" >&2
  exit 1
fi

export PROJECT_ROOT
export MFLOW_LOCAL_DEV_ROOT MFLOW_LOCAL_OUTPUT_DIR
cd "$STUDIO_DIR"
exec node scripts/pull-tools-from-production.js "$@"
