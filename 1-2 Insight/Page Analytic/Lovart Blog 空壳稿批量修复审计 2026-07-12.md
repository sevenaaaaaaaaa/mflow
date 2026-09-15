---
type: audit-report
scope: sanity-blog
date: 2026-07-12
status: published-repair-complete
project: lovart
dataset: production
---

# Lovart Blog 空壳稿批量修复审计 2026-07-12

## 结论

本轮已修复并发布 31 个主站 Sanity blog 文档。修复对象来自用户指出的问题 URL，并包含 `lovart-vs-canva-2026` 的两个同 slug 英文文档。

修复前的共同问题是：正文只有约 3.6k 字符或更短、body 块数约 30 或更少、SEO description 出现重复模板句、部分文章缺 CTA/FAQ/结构化数据，个别文章仍有占位符或默认 SEO。

修复后 published 视角验收结果：31/31 文档通过。短正文、占位符、CTA 缺失、JSON-LD 缺失、noIndex=true 的 BLOCK 计数均为 0。

## 已完成修复

本轮没有删除 production 文档，没有修改 schema，没有执行 `sanity deploy`，没有使用 `--replace`。流程是：读取线上 published 文档，生成对应 draft，复验 draft，发布 draft。

修复内容包括：

- 将空壳/框架正文替换为完整 Portable Text 正文。
- 每篇正文提升到 63-69 个 body block。
- 每篇正文提升到约 8.8k-10k 字符。
- 补齐 FAQ、CTA、Lovart 使用场景、渠道落地、团队审稿、发布后复盘段落。
- 替换重复模板 SEO description。
- 补齐 `seo.structuredData.json`，类型为 Article。
- 设置 `seo.noIndex=false`。
- 保留原 slug、文档 `_id`、category、releaseDate/publishedAt。

已发布的修复 slug：

- `lip-sync-ai-tutorial`
- `lovart-vs-canva-2026`（两个英文文档均已修复）
- `ai-tools-for-small-business`
- `image-to-video-ai-tools`
- `ai-art-generator-tutorial`
- `ai-background-remover-tools`
- `ai-design-agent-explained`
- `ai-design-for-ecommerce-sellers`
- `ai-headshot-generator-2026`
- `lovart-vs-midjourney-comparison`
- `ai-image-editor-vs-photoshop`
- `ai-image-generator-free-tools`
- `ai-photo-generator-for-ecommerce`
- `ai-picture-generator-guide`
- `ai-portrait-generator-tools`
- `ai-video-generator-comparison-2026`
- `best-ai-image-generators-2026`
- `best-ai-photo-editors-2026`
- `create-product-photos-with-ai`
- `how-to-create-ai-videos-free`
- `before-after-design-transformation`
- `color-accessibility-design-guide`
- `data-visualization-design-guide`
- `lovart-official-chinese-entry-guide`
- `ai-design-for-agencies-2026`
- `ai-design-for-authors-and-writers`
- `ai-design-for-coaches-and-consultants`
- `ai-design-for-course-creators`
- `ai-design-for-graphic-designers-2026`
- `ai-design-asset-management-guide`

## 线上验收

发布后用 Sanity published 视角复查：

- 修复文档数：31
- `textLength < 8500`：0
- 正文占位符命中：0
- CTA 缺失：0
- Article JSON-LD 缺失：0
- `seo.noIndex == true`：0

抽样结果显示：

- `lovart-vs-canva-2026`：正文 10,000 字符，SEO title 为 `Lovart vs Canva 2026 | Lovart`
- `before-after-design-transformation`：正文 8,996 字符，SEO title 为 `Before and After Design Transformation | Lovart`
- `ai-art-generator-tutorial`：正文 8,952 字符，SEO title 为 `AI Art Generator Tutorial | Lovart`
- `ai-background-remover-tools`：正文 8,978 字符，SEO title 为 `AI Background Remover Tools | Lovart`
- `ai-design-agent-explained`：正文 8,949 字符，SEO title 为 `AI Design Agent Explained | Lovart`

## 剩余风险

本轮只修用户指出的首批问题 URL及其同 slug duplicate。全库同类问题仍存在，需要继续分批修。

发布后重新扫描英文 blog：

- P0 空壳稿（正文 < 2,000 字符）：134 篇
- 短正文稿（正文 < 6,000 字符）：264 篇
- 占位符残留：96 篇
- 重复模板句 `honest review, real experience` 残留：4 篇

下一批 P0 头部清单：

- `google-imagefx-alternative`：910 字符，noIndex=true
- `veed-io-alternative`：954 字符，noIndex=true
- `deevid-ai-alternative`：988 字符，noIndex=true
- `civitai-alternative`：1,037 字符，noIndex=true
- `ai-banner-maker`：1,047 字符，noIndex=true
- `ai-poster-maker`：1,055 字符，noIndex=true
- `brand-kit-for-real-estate-agent`：1,067 字符，noIndex=true
- `brand-kit-for-bakery-owner`：1,073 字符，noIndex=true
- `bestpractice-build-brand-with-ai`：1,074 字符，noIndex=true
- `brand-kit-for-beauty-salon-owner`：1,081 字符，noIndex=true
- `brand-kit-for-coffee-shop-owner`：1,081 字符，noIndex=true
- `brand-kit-for-gym-owner`：1,084 字符，noIndex=true
- `best-ai-tools-for-ecommerce-2026`：1,155 字符，seo=null
- `ai-image-generation-quality-benchmark-2026`：1,172 字符，noIndex=false
- `best-ai-tools-for-small-business-2026`：1,211 字符，seo=null
- `best-ai-tools-for-social-media-2026`：1,235 字符，seo=null
- `free-ai-color-palette-generator`：1,253 字符，seo=null
- `runway-vs-pika-vs-kling-2026`：1,272 字符，seo=null
- `free-ai-banner-maker-guide`：1,275 字符，seo=null

## 修复脚本

过程脚本保存在 `tmp/repair_sanity_blog_batch.py`。它只写 `drafts.<id>`，再通过 Sanity publish 将 draft 发布；不删除生产文档，不触碰 schema。

过程报告保存在 `tmp/sanity-blog-repair-report.json`。
