#!/usr/bin/env bash
# 检查 Wechatsync CLI ↔ 浏览器扩展连接状态
set -euo pipefail

PORT="${SYNC_WS_PORT:-9527}"
HTTP_PORT=$((PORT + 1))

echo "== Wechatsync 连接检查 =="
echo "WebSocket 端口: $PORT"
echo "HTTP 状态端口:  $HTTP_PORT"
echo

if command -v lsof >/dev/null 2>&1; then
  OCCUPIER=$(lsof -i :"$PORT" -t 2>/dev/null | head -1 || true)
  if [[ -n "$OCCUPIER" ]]; then
    echo "✓ 端口 $PORT 有进程监听 (PID $OCCUPIER)"
    ps -p "$OCCUPIER" -o command= 2>/dev/null || true
  else
    echo "✗ 端口 $PORT 无监听 — 需先运行 wechatsync sync/platforms/auth"
  fi
else
  echo "? 无法检测端口（无 lsof）"
fi
echo

STATUS=$(curl -s "http://127.0.0.1:${HTTP_PORT}/status" 2>/dev/null || echo "")
if [[ -n "$STATUS" ]]; then
  echo "HTTP /status: $STATUS"
  if echo "$STATUS" | grep -q '"connected":true'; then
    echo "✓ 扩展已连接，可以同步"
    exit 0
  else
    echo "✗ CLI 在跑但扩展未连接"
  fi
else
  echo "✗ 无法访问 http://127.0.0.1:${HTTP_PORT}/status"
fi

echo
echo "排查清单（Arc 同样适用，基于 Chromium）："
echo "  1. Arc → 扩展「文章同步助手」→ 设置 → 开启「同步桥接 / CLI·MCP 连接」"
echo "  2. 复制扩展里显示的 Token → 写入 .env 的 WECHATSYNC_TOKEN"
echo "  3. 先清理旧桥接: kill \$(lsof -i :${PORT} -t)  （旧进程若没带 Token 会报 Invalid token）"
echo "  4. 运行前点开扩展弹窗唤醒 Service Worker: open -a Arc chrome-extension://hchobocdmclopcbnibdnoafilagadion/src/popup/index.html"
echo "  5. 服务器地址留空；若仍连不上，改为 ws://127.0.0.1:${PORT}"
echo "  6. 一键等待连接: bash scripts/wechatsync-wait-connect.sh 60"
exit 1
