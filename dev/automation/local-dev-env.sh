#!/usr/bin/env bash
# Shared the brand local-dev path contract.

set -euo pipefail

if [[ -z "${MFLOW_LOCAL_DEV_ROOT:-}" ]]; then
  # 2026-09-13: 2026-08-01 planned move to ~/MFlow Local Dev never landed; real root still in Documents
  export MFLOW_LOCAL_DEV_ROOT="$HOME/Documents/MFlow Local Dev"
fi

export MFLOW_LOCAL_OUTPUT_DIR="${MFLOW_LOCAL_OUTPUT_DIR:-$MFLOW_LOCAL_DEV_ROOT/Output}"
export MFLOW_LOCAL_BACKUP_DIR="${MFLOW_LOCAL_BACKUP_DIR:-$MFLOW_LOCAL_DEV_ROOT/Backup}"
export MFLOW_LOCAL_SANITY_DIR="${MFLOW_LOCAL_SANITY_DIR:-$MFLOW_LOCAL_DEV_ROOT/Sanity}"
export MFLOW_LOCAL_WORDPRESS_DIR="${MFLOW_LOCAL_WORDPRESS_DIR:-$MFLOW_LOCAL_DEV_ROOT/WordPress}"
export MFLOW_RESOURCE_ROOT="${MFLOW_RESOURCE_ROOT:-$(cd "${BASH_SOURCE[0]%/*}/../../../.." && pwd)}"
export MFLOW_LOCAL_GIT_DIR="${MFLOW_LOCAL_GIT_DIR:-$MFLOW_LOCAL_DEV_ROOT/Git}"
export MFLOW_LOCAL_LOG_DIR="${MFLOW_LOCAL_LOG_DIR:-$MFLOW_LOCAL_DEV_ROOT/Logs}"
export MFLOW_LOCAL_TEMP_DIR="${MFLOW_LOCAL_TEMP_DIR:-$MFLOW_LOCAL_DEV_ROOT/Temp}"
# GSC/GA4 API pulls need google-* libs; trident-venv is provisioned by setup (see 00-INDEX 04)
export MFLOW_PYTHON="${MFLOW_PYTHON:-$MFLOW_LOCAL_DEV_ROOT/trident-venv/bin/python}"
[[ -x "$MFLOW_PYTHON" ]] || export MFLOW_PYTHON="$(command -v python3)"
export MFLOW_PULL_DIR="${MFLOW_PULL_DIR:-$MFLOW_LOCAL_OUTPUT_DIR/Page Gen/_pull}"

ensure_mflow_local_dev_dirs() {
  mkdir -p \
    "$MFLOW_LOCAL_OUTPUT_DIR/automation-reports" \
    "$MFLOW_LOCAL_OUTPUT_DIR/composite-v2-audit" \
    "$MFLOW_LOCAL_OUTPUT_DIR/quality-audits" \
    "$MFLOW_LOCAL_OUTPUT_DIR/Data Ingestion" \
    "$MFLOW_LOCAL_OUTPUT_DIR/Warehouse" \
    "$MFLOW_LOCAL_OUTPUT_DIR/Page Gen/_pull" \
    "$MFLOW_LOCAL_BACKUP_DIR/archives" \
    "$MFLOW_LOCAL_BACKUP_DIR/governance-backups" \
    "$MFLOW_LOCAL_SANITY_DIR/production-pulls" \
    "$MFLOW_LOCAL_WORDPRESS_DIR/readonly-pulls" \
    "$MFLOW_LOCAL_GIT_DIR/object-stores" \
    "$MFLOW_LOCAL_GIT_DIR/worktrees" \
    "$MFLOW_LOCAL_LOG_DIR" \
    "$MFLOW_LOCAL_TEMP_DIR"
}
