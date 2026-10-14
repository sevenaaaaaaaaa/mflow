#!/usr/bin/env bash
# install.sh — render a launchd plist template and load it.
#   bash dev/automation/plists/install.sh com.mflow.daily-pipeline
# Placeholders: __MFLOW_ROOT__ (this checkout), __MFLOW_LOCAL_DEV_ROOT__, __HOME__.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MFLOW_ROOT="${MFLOW_ROOT:-$(cd "$HERE/../../.." && pwd)}"
LOCAL_DEV="${MFLOW_LOCAL_DEV_ROOT:-$HOME/Documents/MFlow Local Dev}"
name="${1:?usage: install.sh <label>   (e.g. com.mflow.daily-pipeline)}"
src="$HERE/$name.plist"
[[ -f "$src" ]] || src="$MFLOW_ROOT/dev/scripts/sentinel/$name.plist"
[[ -f "$src" ]] || { echo "template not found: $name" >&2; exit 1; }
dest="$HOME/Library/LaunchAgents/$name.plist"
mkdir -p "$LOCAL_DEV/Logs"
sed -e "s#__MFLOW_ROOT__#${MFLOW_ROOT}#g" -e "s#__MFLOW_LOCAL_DEV_ROOT__#${LOCAL_DEV}#g" -e "s#__HOME__#${HOME}#g" "$src" > "$dest"
plutil -lint "$dest" >/dev/null
launchctl unload "$dest" 2>/dev/null || true
launchctl load "$dest"
echo "loaded $dest"
