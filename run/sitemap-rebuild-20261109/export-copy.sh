#!/usr/bin/env bash
# 把当前交付包整理一份到系统下载目录（给前端老师）
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE="${1:-$(date +%Y%m%d)}"
DEST="$HOME/Downloads/Lovart-Sitemap-$DATE"
rm -rf "$DEST" && mkdir -p "$DEST"
cp "$SRC"/sitemap-*.xml "$DEST"/
cp "$SRC"/robots.txt "$SRC"/llms.txt "$SRC"/llms-blog.txt "$SRC"/llms-full.txt "$DEST"/
cp "$SRC"/README.md "$SRC"/robots-llms-说明.md "$SRC"/给前端-替换说明.md "$DEST"/
cp "$SRC"/deploy-check.sh "$SRC"/gsc-submit.py "$DEST"/
cd "$HOME/Downloads" && rm -f "Lovart-Sitemap-$DATE.zip" && zip -rXq "Lovart-Sitemap-$DATE.zip" "Lovart-Sitemap-$DATE"
echo "文件夹: $DEST"
echo "压缩包: $HOME/Downloads/Lovart-Sitemap-$DATE.zip"
echo "文件数: $(ls "$DEST" | wc -l | tr -d ' ')"
