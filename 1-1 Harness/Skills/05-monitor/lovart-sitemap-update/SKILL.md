# lovart-sitemap-update

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-sitemap-update/SKILL.md` |

Step 7 of Lovart Content Pipeline — 内容发布后自动重新生成 sitemap、llms.txt、robots.txt 等 SEO 资产，并部署到服务器。

## Triggers

- "更新 sitemap" / "update sitemap"
- "刷新 SEO 资产" / "refresh SEO assets"
- "重新生成 llms.txt" / "regenerate llms.txt"
- Pipeline Orchestrator 调用 Step 7
- 每周一凌晨 cron 自动执行

## Prerequisites

- `generate-all.py` 和 `config.example.json` 存在于 Skills 目录
- 输出目标：`1-Project/1-4 Dev/Sitemap/`（已有 32 个文件）
- Python 3.9+
- 网络可用

## Workflow

### Phase 1: 判断执行模式

```
IF 本次有新博客/功能/工具页发布:
    → 完整模式：重新爬取 + 生成
ELSE IF 仅翻译/更新:
    → 快速模式：跳过爬取，用缓存
ELSE:
    → 离线模式：完全不联网
```

### Phase 2: 执行生成

```bash
cd "1-Project/1-1 Harness/Skills"

# 完整模式（新内容发布后）
python3 generate-all.py config.example.json

# 快速模式（翻译/小更新后）
python3 generate-all.py config.example.json --skip-crawl

# 离线模式
python3 generate-all.py config.example.json --offline
```

### Phase 3: 验证输出

```bash
# 检查生成文件完整性
ls -la output/sitemap-index.xml
ls -la output/sitemap-blog.xml
ls -la output/llms.txt
ls -la output/robots.txt

# 统计 URL 数量
wc -l output/all-urls.txt

# 对比上次的 URL 数量变化
diff <(sort output/all-urls.txt) <(sort output/all-urls.txt.bak) | head -20
```

### Phase 4: 同步到项目 Sitemap 目录

```bash
# 复制到项目 Sitemap 目录（Obsidian 可见）
cp output/sitemap-*.xml "1-Project/1-4 Dev/Sitemap/"
cp output/llms*.txt "1-Project/1-4 Dev/Sitemap/"
cp output/robots.txt "1-Project/1-4 Dev/Sitemap/"
cp output/all-urls.txt "1-Project/1-4 Dev/Sitemap/"
cp -r output/schema-snippets/ "1-Project/1-4 Dev/Sitemap/schema-snippets/"
```

### Phase 5: 部署到服务器

```bash
# 方式 A：rsync 到服务器
rsync -avz output/ user@server:/var/www/lovart/public/ \
  --include="sitemap-*.xml" \
  --include="llms*.txt" \
  --include="robots.txt" \
  --exclude="*"

# 方式 B：通过 Vercel/Netlify CI 触发
# git add output/ && git commit -m "chore: update SEO assets $(date +%Y-%m-%d)" && git push

# 方式 C：通过 S3/CDN 上传
# aws s3 sync output/ s3://lovart-public/ --include "sitemap-*" --include "llms*" --include "robots.txt"
```

### Phase 6: 提交给搜索引擎

```bash
# Ping Google
curl "https://www.google.com/ping?sitemap=https://www.lovart.ai/sitemap-index.xml"

# Ping Bing（覆盖元宝）
curl "https://www.bing.com/ping?sitemap=https://www.lovart.ai/sitemap-index.xml"

# Ping IndexNow (Bing/Yandex/Seznam/Naver)
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "www.lovart.ai",
    "key": "{INDEXNOW_KEY}",
    "urlList": [
      "https://www.lovart.ai/blog/{new_slug_1}",
      "https://www.lovart.ai/blog/{new_slug_2}"
    ]
  }'
```

### Phase 7: 验证部署

```bash
# 确认文件可访问
curl -sI "https://www.lovart.ai/sitemap-index.xml" | head -3
curl -sI "https://www.lovart.ai/robots.txt" | head -3
curl -sI "https://www.lovart.ai/llms.txt" | head -3

# 验证新 URL 在 sitemap 中
grep "{new_slug}" output/sitemap-blog.xml
```

## Sitemap Update Report

```markdown
# Sitemap Update Report — YYYY-MM-DD

| 指标 | 更新前 | 更新后 | 变化 |
|------|--------|--------|------|
| 总 URL 数 | 13,962 | 14,028 | +66 |
| Blog URL 数 | 8,870 | 8,920 | +50 |
| 新增语言版本 | — | +16 (4 篇 × 4 语言) | — |
| llms-blog.txt 条目 | 855 | 860 | +5 |

## 新增 URL
- https://www.lovart.ai/blog/{slug-1}
- https://www.lovart.ai/zh/blog/{slug-1}
- ...

## 搜索引擎 Ping 状态
- Google: ✅ 200 OK
- Bing: ✅ 200 OK
- IndexNow: ✅ 202 Accepted

## 服务器部署
- ✅ sitemap-index.xml — 200 OK
- ✅ robots.txt — 200 OK
- ✅ llms.txt — 200 OK
```

## Cron 配置

```bash
# 每周一凌晨 2 点自动执行（快速模式）
0 2 * * 1 cd "/path/to/Skills" && python3 generate-all.py config.example.json --skip-crawl && bash deploy-seo-assets.sh >> logs/sitemap-cron.log 2>&1
```

## Downstream

本步骤为 Pipeline 终点。输出汇总到 Pipeline Orchestrator 最终报告。
