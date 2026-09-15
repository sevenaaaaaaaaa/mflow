#!/usr/bin/env bash
# Unload all Lovart launchd jobs (use when migrating to Cursor / other agent schedulers).
set -euo pipefail

LAUNCH_DIR="$HOME/Library/LaunchAgents"

for plist in "$LAUNCH_DIR"/com.lovart.*.plist; do
  [ -f "$plist" ] || continue
  label="$(basename "$plist" .plist)"
  launchctl unload "$plist" 2>/dev/null || true
  echo "unloaded: $label"
done

echo ""
echo "Remaining:"
launchctl list 2>/dev/null | grep com.lovart || echo "(none)"
