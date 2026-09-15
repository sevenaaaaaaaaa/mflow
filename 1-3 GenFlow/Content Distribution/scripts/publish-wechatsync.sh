#!/usr/bin/env bash
# Wechatsync CLI → Arc/Chrome 扩展 → 国内平台（默认草稿）
# 前置：扩展已开启「同步桥接」，且 WECHATSYNC_TOKEN 与扩展内 Token 一致
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

: "${WECHATSYNC_TOKEN:?请在 .env 设置 WECHATSYNC_TOKEN（与 Arc 扩展「同步桥接」里显示的 Token 一致）}"

FILE="${1:?用法: publish-wechatsync.sh <draft.md> [platforms]}"
PLATFORMS="${2:-zhihu,baijiahao}"

exec wechatsync sync "$FILE" --platforms "$PLATFORMS"
