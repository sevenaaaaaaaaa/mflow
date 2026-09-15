#!/usr/bin/env bash
# 启动 Wechatsync 桥接并等待 Arc/Chrome 扩展连接
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

: "${WECHATSYNC_TOKEN:?缺少 WECHATSYNC_TOKEN}"

PORT="${SYNC_WS_PORT:-9527}"
HTTP_PORT=$((PORT + 1))
WAIT_SECS="${1:-90}"

# 结束占用端口的旧进程
if command -v lsof >/dev/null 2>&1; then
  PIDS=$(lsof -i :"$PORT" -t 2>/dev/null || true)
  if [[ -n "$PIDS" ]]; then
    echo "清理端口 $PORT 上的旧进程: $PIDS"
    kill $PIDS 2>/dev/null || true
    sleep 1
  fi
fi

LOG=$(mktemp /tmp/wechatsync-wait.XXXXXX.log)
echo "启动桥接 (Token 已配置)..."
printf 'n\n' | wechatsync platforms --auth --timeout "$((WAIT_SECS * 1000))" >"$LOG" 2>&1 &
WPID=$!

cleanup() {
  kill "$WPID" 2>/dev/null || true
  kill $(lsof -i :"$PORT" -t 2>/dev/null) 2>/dev/null || true
}
trap cleanup EXIT

echo "等待扩展连接 (最多 ${WAIT_SECS}s)..."
echo "→ 请在 Arc 中点击「文章同步助手」图标，确认「同步桥接」为开启且显示「已连接」"
echo "→ 若一直等待连接，把服务器地址改为: ws://127.0.0.1:${PORT}"
echo

for ((i=1; i<=WAIT_SECS/3; i++)); do
  sleep 3
  STATUS=$(curl -s "http://127.0.0.1:${HTTP_PORT}/status" 2>/dev/null || echo "")
  if [[ -z "$STATUS" ]]; then
    echo "[$i] CLI 尚未就绪..."
    continue
  fi
  echo "[$i] $STATUS"
  if echo "$STATUS" | grep -q '"connected":true'; then
    echo
    echo "✓ 扩展已连接"
    tail -30 "$LOG"
    trap - EXIT
    exit 0
  fi
done

echo
echo "✗ 超时：扩展未连接"
tail -30 "$LOG"
exit 1
