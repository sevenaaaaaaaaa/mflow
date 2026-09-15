#!/usr/bin/env bash
# Bootstrap external Lovart Local Dev directories.
#
# Safe by design: creates directories and .gitkeep files only.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=local-dev-env.sh
source "$SCRIPT_DIR/local-dev-env.sh"

ensure_lovart_local_dev_dirs

find "$LOVART_LOCAL_DEV_ROOT" -type d | while read -r dir; do
  touch "$dir/.gitkeep"
done

cat <<EOF
Lovart Local Dev is ready:
  $LOVART_LOCAL_DEV_ROOT

Output:
  $LOVART_LOCAL_OUTPUT_DIR
Backup:
  $LOVART_LOCAL_BACKUP_DIR
Sanity pulls:
  $LOVART_LOCAL_SANITY_DIR/production-pulls
WordPress readonly pulls:
  $LOVART_LOCAL_WORDPRESS_DIR/readonly-pulls
Git:
  $LOVART_LOCAL_GIT_DIR
EOF
