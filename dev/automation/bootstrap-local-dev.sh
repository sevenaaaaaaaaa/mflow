#!/usr/bin/env bash
# Bootstrap external MFlow Local Dev directories.
#
# Safe by design: creates directories and .gitkeep files only.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=local-dev-env.sh
source "$SCRIPT_DIR/local-dev-env.sh"

ensure_mflow_local_dev_dirs

find "$MFLOW_LOCAL_DEV_ROOT" -type d | while read -r dir; do
  touch "$dir/.gitkeep"
done

cat <<EOF
MFlow Local Dev is ready:
  $MFLOW_LOCAL_DEV_ROOT

Output:
  $MFLOW_LOCAL_OUTPUT_DIR
Backup:
  $MFLOW_LOCAL_BACKUP_DIR
Sanity pulls:
  $MFLOW_LOCAL_SANITY_DIR/production-pulls
WordPress readonly pulls:
  $MFLOW_LOCAL_WORDPRESS_DIR/readonly-pulls
Git:
  $MFLOW_LOCAL_GIT_DIR
EOF
