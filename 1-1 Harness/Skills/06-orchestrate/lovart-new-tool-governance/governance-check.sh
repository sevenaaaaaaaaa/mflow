#!/usr/bin/env bash
# governance-check.sh — shell wrapper for governance_check.py
# Usage: bash governance-check.sh /path/to/script.py
#        bash governance-check.sh /path/to/script.sh

set -euo pipefail

SCRIPT_PATH="${1:-}"
if [[ -z "$SCRIPT_PATH" ]]; then
  echo "[err] usage: governance-check.sh <script-path>" >&2
  exit 2
fi

HERE="$(cd "$(dirname "$0")" && pwd)"
PY_CHECK="$HERE/governance_check.py"

if [[ ! -f "$PY_CHECK" ]]; then
  echo "[err] governance_check.py not found at $PY_CHECK" >&2
  exit 2
fi

python3 "$PY_CHECK" "$SCRIPT_PATH" "$@"
