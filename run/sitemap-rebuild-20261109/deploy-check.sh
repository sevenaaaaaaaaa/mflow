#!/usr/bin/env bash
# 部署后验收：文件长什么样、条数对不对
set -u
B="https://www.lovart.ai"
get() { curl -sS -m 25 "$B/$1"; }
for f in sitemap-index.xml sitemap-features.xml sitemap-tools.xml sitemap-blog.xml sitemap-blog-de.xml sitemap-lang-ja.xml; do
  xml="$(get $f)"
  n=$(printf '%s' "$xml" | grep -c '<loc>')
  lm=$(printf '%s' "$xml" | grep -o '<lastmod>[^<]*' | head -1 | sed 's/<lastmod>//')
  printf '%-24s locs=%-6s lastmod=%s\n' "$f" "$n" "$lm"
done
echo "--- draft- 残留（期望 0）---"
printf 'scenarios locs: %s\n' "$(get sitemap-scenarios.xml | grep -c '<loc>')"
echo "--- 新档样本 ---"
get sitemap-features.xml | grep -o '<loc>[^<]*' | sed 's/<loc>//' | head -3
