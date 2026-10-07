#!/usr/bin/env bash
# Wrapper: run report-notify from project root.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec bash "$SCRIPT_DIR/report-notify.sh" "$@"
