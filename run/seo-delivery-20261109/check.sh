#!/usr/bin/env bash
# 合并交付包一体验收：sitemap / robots / llms
set -u
B="https://www.lovart.ai"
PASS=0; FAIL=0
chk() { # $1=描述 $2=实际 $3=期望
  if [ "$2" = "$3" ]; then printf "  PASS  %-46s %s\n" "$1" "$2"; PASS=$((PASS+1));
  else printf "  FAIL  %-46s got=%s want=%s\n" "$1" "$2" "$3"; FAIL=$((FAIL+1)); fi; }
get() { curl -sS -m 30 "$B/$1"; }
locs() { get "$1" | grep -c "<loc>"; }

echo "== sitemap =="
chk "index 子项数"        "$(get sitemap-index.xml | grep -c "<sitemap>")" 30
chk "features locs"       "$(locs sitemap-features.xml)" 5814
chk "tools locs"          "$(locs sitemap-tools.xml)" 1145
chk "blog locs"           "$(locs sitemap-blog.xml)" 1509
chk "blog-de locs"        "$(locs sitemap-blog-de.xml)" 728
chk "lang-ja locs"        "$(locs sitemap-lang-ja.xml)" 757
chk "scenarios 已清空"    "$(locs sitemap-scenarios.xml)" 0
chk "draft- 残留"         "$(get sitemap-lang-ja.xml | grep -c "draft-")" 0

echo "== robots =="
RB="$(get robots.txt)"
chk "Sitemap 条数"        "$(printf "%s" "$RB" | grep -c "^Sitemap:")" 1
chk "Sitemap 指向 index"  "$(printf "%s" "$RB" | grep -c "sitemap-index.xml")" 1
chk "Crawl-delay 条数"    "$(printf "%s" "$RB" | grep -c "Crawl-delay")" 0

echo "== llms =="
chk "llms.txt 版本"       "$(get llms.txt | grep -c "Generated: 2026-11-09")" 1
chk "llms-blog 条数"      "$(get llms-blog.txt | grep -c "^- \[")" 1510
chk "llms-full 条数"      "$(get llms-full.txt | grep -c "^- \[")" 15426

echo
echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
