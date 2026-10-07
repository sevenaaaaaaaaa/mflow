#!/usr/bin/env bash
# 打印 Cursor Agent 执行海外 MCP 发布的提示词
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PENDING="${1:-}"

if [[ -z "$PENDING" ]]; then
  LATEST=$(ls -t "$ROOT"/queue/mcp-pending-*.json 2>/dev/null | head -1 || true)
  if [[ -z "$LATEST" ]]; then
    echo "用法: mcp-flush-prompt.sh queue/mcp-pending-xxx.json"
    echo "或先运行: node scripts/dispatch-publish.js --manifest queue/dispatch-XXX.json --global-only"
    exit 1
  fi
  PENDING="$LATEST"
fi

[[ "$PENDING" != /* ]] && PENDING="$ROOT/$PENDING"

if [[ ! -f "$PENDING" ]]; then
  echo "文件不存在: $PENDING"
  exit 1
fi

REL="${PENDING#$ROOT/}"

cat <<EOF
请读取 ${REL}，对 jobs[] 中每个条目：

1. 用 content-distribution MCP 的 hints(channel) 获取约束
2. 按 Gate 0 从 body 生成 Variant（摘要，非主站全文；含 canonical）
3. 调用 publish(content_id, channel, variant)
4. manual_browser 档（medium/reddit/twitter）给出 compose URL 并等我确认
5. 成功后写入 queue/published.json 与 logs/

canonical: $(jq -r '.canonical_url // empty' "$PENDING" 2>/dev/null || true)
jobs: $(jq -r '[.jobs[].platform] | join(", ")' "$PENDING" 2>/dev/null || echo "(见文件)")
EOF
