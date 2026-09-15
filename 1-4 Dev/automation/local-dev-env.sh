#!/usr/bin/env bash
# Shared Lovart local-dev path contract.

set -euo pipefail

if [[ -z "${LOVART_LOCAL_DEV_ROOT:-}" ]]; then
  # 2026-09-13: 2026-08-01 planned move to ~/Lovart Local Dev never landed; real root still in Documents
  export LOVART_LOCAL_DEV_ROOT="$HOME/Documents/Lovart Local Dev"
fi

export LOVART_LOCAL_OUTPUT_DIR="${LOVART_LOCAL_OUTPUT_DIR:-$LOVART_LOCAL_DEV_ROOT/Output}"
export LOVART_LOCAL_BACKUP_DIR="${LOVART_LOCAL_BACKUP_DIR:-$LOVART_LOCAL_DEV_ROOT/Backup}"
export LOVART_LOCAL_SANITY_DIR="${LOVART_LOCAL_SANITY_DIR:-$LOVART_LOCAL_DEV_ROOT/Sanity}"
export LOVART_LOCAL_WORDPRESS_DIR="${LOVART_LOCAL_WORDPRESS_DIR:-$LOVART_LOCAL_DEV_ROOT/WordPress}"
export LOVART_RESOURCE_ROOT="${LOVART_RESOURCE_ROOT:-$(cd "${BASH_SOURCE[0]%/*}/../../../.." && pwd)}"
export LOVART_LOCAL_GIT_DIR="${LOVART_LOCAL_GIT_DIR:-$LOVART_LOCAL_DEV_ROOT/Git}"
export LOVART_LOCAL_LOG_DIR="${LOVART_LOCAL_LOG_DIR:-$LOVART_LOCAL_DEV_ROOT/Logs}"
export LOVART_LOCAL_TEMP_DIR="${LOVART_LOCAL_TEMP_DIR:-$LOVART_LOCAL_DEV_ROOT/Temp}"
# GSC/GA4 API pulls need google-* libs; trident-venv is provisioned by setup (see 00-INDEX 04)
export LOVART_PYTHON="${LOVART_PYTHON:-$LOVART_LOCAL_DEV_ROOT/trident-venv/bin/python}"
[[ -x "$LOVART_PYTHON" ]] || export LOVART_PYTHON="$(command -v python3)"
export LOVART_PULL_DIR="${LOVART_PULL_DIR:-$LOVART_LOCAL_OUTPUT_DIR/Page Gen/_pull}"

ensure_lovart_local_dev_dirs() {
  mkdir -p \
    "$LOVART_LOCAL_OUTPUT_DIR/automation-reports" \
    "$LOVART_LOCAL_OUTPUT_DIR/composite-v2-audit" \
    "$LOVART_LOCAL_OUTPUT_DIR/quality-audits" \
    "$LOVART_LOCAL_OUTPUT_DIR/Data Ingestion" \
    "$LOVART_LOCAL_OUTPUT_DIR/Warehouse" \
    "$LOVART_LOCAL_OUTPUT_DIR/Page Gen/_pull" \
    "$LOVART_LOCAL_BACKUP_DIR/archives" \
    "$LOVART_LOCAL_BACKUP_DIR/governance-backups" \
    "$LOVART_LOCAL_SANITY_DIR/production-pulls" \
    "$LOVART_LOCAL_WORDPRESS_DIR/readonly-pulls" \
    "$LOVART_LOCAL_GIT_DIR/object-stores" \
    "$LOVART_LOCAL_GIT_DIR/worktrees" \
    "$LOVART_LOCAL_LOG_DIR" \
    "$LOVART_LOCAL_TEMP_DIR"
}
