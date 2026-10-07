#!/usr/bin/env bash
# dream/reflect.sh — Layer 2: scan session logs, extract recurring patterns.
#
# Boundary:
#   - READ-ONLY on KB / skills / rules (only writes to dream/recurring-patterns/)
#   - Promotion to rules happens in Layer 3 (PR workflow), not here
#
# Schedule: launchd 02:30 daily (per dream/lovart.dream.plist). Can also run manually.

set -euo pipefail

SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KNOWLEDGE_ROOT="$(cd "$SELF/.." && pwd)"
VAULT_ROOT="$(cd "$KNOWLEDGE_ROOT/../.." && pwd)"
LOG="$SELF/.reflect-log"
mkdir -p "$(dirname "$LOG")"

echo "[$(date +%FT%T)] reflect start" >> "$LOG"

PYTHON_OUT="$(python3 "$SELF/reflect.py" --root "$VAULT_ROOT" 2>&1)"
echo "$PYTHON_OUT" >> "$LOG"
echo "$PYTHON_OUT"

echo "[$(date +%FT%T)] reflect done" >> "$LOG"