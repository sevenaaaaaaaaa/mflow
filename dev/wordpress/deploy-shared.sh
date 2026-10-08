#!/bin/bash
# deploy-shared.sh — 部署共享资产格式的复刻页 payload（按 slug 自动查页 ID 更新）
# 用法：deploy-shared.sh <payload.json> [payload.json ...]
set -e
USER=$(head -1 /tmp/.wp-auth.tmp)
PASS=$(tail -1 /tmp/.wp-auth.tmp)
CJ=/tmp/.wp-cjSH
BASE="https://blogs.lovart.ai"

curl -s --max-time 30 -c "$CJ" "$BASE/wp-login.php" -o /dev/null
curl -s --max-time 30 -b "$CJ" -c "$CJ" -X POST "$BASE/wp-login.php" \
  --data-urlencode "log=$USER" --data-urlencode "pwd=$PASS" \
  --data-urlencode "wp-submit=Log In" -o /dev/null
NONCE=$(curl -s --max-time 30 -b "$CJ" "$BASE/wp-admin/admin-ajax.php?action=rest-nonce")

for F in "$@"; do
  SLUG=$(python3 -c "import json,io;print(json.load(io.open('$F',encoding='utf-8'))['slug'])")
  # 查页 ID（已发布页按 slug 查询）
  PAGE=$(curl -s --max-time 30 -b "$CJ" "$BASE/wp-json/wp/v2/pages?slug=$SLUG&_fields=id,slug,status")
  PID=$(echo "$PAGE" | python3 -c "
import json,sys,io
d = json.load(io.StringIO(sys.stdin.read()))
print(d[0]['id'] if d else '')")
  if [ -z "$PID" ]; then
    echo "  $SLUG: 无已有页，跳过（用 deploy-homepage.sh 首建）"
    continue
  fi
  CODE=$(curl -s --max-time 180 -b "$CJ" -X POST "$BASE/wp-json/wp/v2/pages/$PID" \
    -H "Content-Type: application/json" -H "X-WP-Nonce: $NONCE" \
    --data-binary @"$F" -o /tmp/sh-res.json -w "%{http_code}")
  # 更新后模板可能被 WP 重置，补一次 elementor_canvas（与 fix-solutions.sh 相同做法）
  curl -s --max-time 60 -b "$CJ" -X POST "$BASE/wp-json/wp/v2/pages/$PID" \
    -H "Content-Type: application/json" -H "X-WP-Nonce: $NONCE" \
    --data '{"template":"elementor_canvas"}' -o /dev/null
  echo "  $SLUG (id=$PID) http=$CODE"
done
echo "=== 部署完成 ==="