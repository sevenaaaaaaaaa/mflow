#!/bin/bash
set -e
USER=$(head -1 /tmp/.wp-auth.tmp)
PASS=$(tail -1 /tmp/.wp-auth.tmp)
CJ=/tmp/.wp-cjS
BASE="https://blogs.lovart.ai"
curl -s --max-time 30 -c "$CJ" "$BASE/wp-login.php" -o /dev/null
curl -s --max-time 30 -b "$CJ" -c "$CJ" -X POST "$BASE/wp-login.php" \
  --data-urlencode "log=$USER" --data-urlencode "pwd=$PASS" \
  --data-urlencode "wp-submit=Log In" -o /dev/null
NONCE=$(curl -s --max-time 30 -b "$CJ" "$BASE/wp-admin/admin-ajax.php?action=rest-nonce")
for F in /tmp/replica-solutions/*.json; do
  [ -f "$F" ] || continue
  SLUG=$(basename "$F" .json)
  RES=$(curl -s --max-time 180 -b "$CJ" -X POST "$BASE/wp-json/wp/v2/pages" \
    -H "Content-Type: application/json" -H "X-WP-Nonce: $NONCE" \
    --data-binary @"$F")
  ID=$(echo "$RES" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id', d.get('code','ERR')))")
  echo "  $SLUG → $ID"
done
echo "=== done ==="
