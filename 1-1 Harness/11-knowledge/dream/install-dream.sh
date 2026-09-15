#!/usr/bin/env bash
# Lovart MFlow Dream 一键落地（绝对路径 + 严格引用 + iCloud 兼容）
#
# 用法：bash /Users/seveno/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/MindRe/1-Project/Lovart\ MFlow/1-1\ Harness/11-knowledge/dream/install-dream.sh
#
# 干三件事（按需可注释）：
#   A. 安装 launchd plist（每天 02:30 跑 consolidate.sh）
#   B. 加 opencode 自定义命令 `kg` 和 `dream`（如果你的 OPENCODE=opencode 已配）
#   C. 第一次手动跑一次梦境，证明链路通

set -euo pipefail

VAULT="/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/MindRe/1-Project/Lovart MFlow"
KNOW="$VAULT/1-1 Harness/11-knowledge"
DREAM="$KNOW/dream"
SCRIPTS="$KNOW/scripts"
LAUNCH="$HOME/Library/LaunchAgents"

echo "[1/5] verify core paths exist"
for p in \
  "$VAULT" \
  "$KNOW"/README.md \
  "$KNOW"/KNOWLEDGE-TREE.md \
  "$KNOW"/MEMORY-PROJECT.md \
  "$KNOW"/entities.yaml \
  "$KNOW"/relationships.yaml \
  "$DREAM"/consolidate.sh \
  "$DREAM"/audit.sh \
  "$DREAM"/lovart.dream.plist \
  "$SCRIPTS"/kg \
  "$SCRIPTS"/kg-emit-jsonl.py \
  "$SCRIPTS"/kg-query.py \
  "$SCRIPTS"/fm-check.py; do
  if [ ! -e "$p" ]; then
    echo "  ✗ MISSING: $p"
    exit 2
  fi
  echo "  ✓ $p"
done

echo ""
echo "[2/5] refresh JSONL mirror + kg stats"
bash "$SCRIPTS/kg" emit
bash "$SCRIPTS/kg" stats

echo ""
echo "[3/5] run audit (writes today's report)"
bash "$DREAM/audit.sh" | sed -n '1,40p'
cat "$KNOW/audit/reports/audit-report-$(date +%F).md" | head -25

echo ""
echo "[4/5] install launchd plist"
mkdir -p "$LAUNCH"
# 1. replace /REPLACE_WITH_VAULT_ROOT/ in plist
PLIST_SRC="$DREAM/lovart.dream.plist"
PLIST_DST="$LAUNCH/com.lovart.dream.plist"
sed "s|/REPLACE_WITH_VAULT_ROOT|$VAULT|g" "$PLIST_SRC" > "$PLIST_DST"
echo "  wrote $PLIST_DST"
# 2. unload (ignore errors) + load
launchctl unload "$PLIST_DST" 2>/dev/null || true
launchctl load "$PLIST_DST" && echo "  ✓ launchd loaded: com.lovart.dream"
launchctl list | grep com.lovart.dream | head -1 || true

echo ""
echo "[5/5] trigger dream once now (optional sanity)"
# 用 launchctl kickstart 立即跑一次；如果 launcher 不支持则直接 bash 调
launchctl kickstart -k "gui/$(id -u)/com.lovart.dream" 2>/dev/null || \
  bash "$DREAM/consolidate.sh" --no-touch || true

echo ""
echo "DONE."
echo "Next:"
echo "  - tail -f /tmp/com.lovart.dream.out.log   # 看 02:30 跑的输出"
echo "  - ls -t \"$KNOW/audit/reports/\" | head              # 看最近的报告"
echo "  - 任意 agent 启动 Profile 前都应该先读:"
echo "      \"$KNOW/README.md\""
echo "      \"$KNOW/KNOWLEDGE-TREE.md\""
echo ""
