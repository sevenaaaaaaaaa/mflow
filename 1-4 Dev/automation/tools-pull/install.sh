#!/usr/bin/env bash
# Install weekly Tools pull (production → local) via macOS launchd.
set -euo pipefail

INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"
PULL_SCRIPT="$INSTALL_DIR/pull-tools-from-production.sh"
LOG_DIR="${LOVART_LOG_DIR:-$HOME/Library/Logs/Lovart}"
LAUNCH_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.lovart.tools-pull-weekly.plist"
PLIST_SRC="$INSTALL_DIR/$PLIST_NAME"
PLIST_DEST="$LAUNCH_DIR/$PLIST_NAME"

chmod +x "$PULL_SCRIPT"
mkdir -p "$LOG_DIR"

cp "$PLIST_SRC" "/tmp/$PLIST_NAME"
sed -i '' "s|__PULL_SCRIPT__|$PULL_SCRIPT|g" "/tmp/$PLIST_NAME"
sed -i '' "s|__LOG_DIR__|$LOG_DIR|g" "/tmp/$PLIST_NAME"

launchctl unload "$PLIST_DEST" 2>/dev/null || true
cp "/tmp/$PLIST_NAME" "$PLIST_DEST"
launchctl load "$PLIST_DEST"

echo "✅ $PLIST_NAME installed"
echo "   Script: $PULL_SCRIPT"
echo "   Schedule: Monday 07:00"
echo "   Log: $LOG_DIR/tools-pull-weekly.log"
echo ""
echo "Manual run: bash \"$PULL_SCRIPT\""
echo "Status: launchctl list | grep com.lovart.tools-pull"
