#!/bin/bash
set -e
USER=$(head -1 /tmp/.wp-auth.tmp)
PASS=$(tail -1 /tmp/.wp-auth.tmp)
CJ=/tmp/.wp-cjS3
BASE="https://blogs.lovart.ai"
curl -s --max-time 30 -c "$CJ" "$BASE/wp-login.php" -o /dev/null
curl -s --max-time 30 -b "$CJ" -c "$CJ" -X POST "$BASE/wp-login.php" \
  --data-urlencode "log=$USER" --data-urlencode "pwd=$PASS" \
  --data-urlencode "wp-submit=Log In" -o /dev/null
NONCE=$(curl -s --max-time 30 -b "$CJ" "$BASE/wp-admin/admin-ajax.php?action=rest-nonce")
# 已知 ID 映射（Round 部署输出）
declare -A MAP=(
  [18295]=ai-design-for-fitness-wellness-hub
  [18296]=ai-design-for-small-business-hub
  [18297]=ai-design-solution-for-agencies
  [18298]=ai-design-solution-for-creators
  [18299]=ai-design-solution-for-marketing-teams
  [18300]=ai-design-solution-for-nonprofits
  [18301]=ai-design-solution-for-saas
  [18302]=ai-design-solution-for-shopify
  [18303]=good-design-for-business-owners
  [18304]=good-design-for-marketers
)
for PID in 18295 18296 18297 18298 18299 18300 18301 18302 18303 18304; do
  SLUG=${MAP[$PID]}
  F="/tmp/replica-solutions/$SLUG.json"
  [ -f "$F" ] || { echo "  no payload: $SLUG"; continue; }
  CODE=$(curl -s --max-time 180 -b "$CJ" -X POST "$BASE/wp-json/wp/v2/pages/$PID" \
    -H "Content-Type: application/json" -H "X-WP-Nonce: $NONCE" \
    --data-binary @"$F" -o /tmp/sres-$PID.json -w "%{http_code}")
  curl -s --max-time 60 -b "$CJ" -X POST "$BASE/wp-json/wp/v2/pages/$PID" \
    -H "Content-Type: application/json" -H "X-WP-Nonce: $NONCE" \
    --data '{"template":"elementor_canvas"}' -o /dev/null
  echo "  $SLUG (id=$PID) http=$CODE"
done
echo "=== 修复完成 ==="
