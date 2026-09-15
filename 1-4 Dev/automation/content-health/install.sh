#!/usr/bin/env bash
# Install weekly Sanity content health check via macOS launchd.
set -euo pipefail

INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"
HEALTH_SCRIPT="$INSTALL_DIR/weekly-health-check.sh"
LOG_DIR="${LOVART_LOG_DIR:-$HOME/Library/Logs/Lovart}"
LAUNCH_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.lovart.content-health-weekly.plist"
PLIST_SRC="$INSTALL_DIR/$PLIST_NAME"
PLIST_DEST="$LAUNCH_DIR/$PLIST_NAME"

chmod +x "$HEALTH_SCRIPT"
mkdir -p "$LOG_DIR"

cp "$PLIST_SRC" "/tmp/$PLIST_NAME"
sed -i '' "s|__HEALTH_SCRIPT__|$HEALTH_SCRIPT|g" "/tmp/$PLIST_NAME"
sed -i '' "s|__LOG_DIR__|$LOG_DIR|g" "/tmp/$PLIST_NAME"

launchctl unload "$PLIST_DEST" 2>/dev/null || true
cp "/tmp/$PLIST_NAME" "$PLIST_DEST"
launchctl load "$PLIST_DEST"

echo "✅ $PLIST_NAME installed"
echo "   Script: $HEALTH_SCRIPT"
echo "   Schedule: Monday 08:30"
echo "   Log: $LOG_DIR/content-health-weekly.log"
echo ""
echo "Manual run: bash \"$HEALTH_SCRIPT\""
echo "Status: launchctl list | grep com.lovart.content-health"
