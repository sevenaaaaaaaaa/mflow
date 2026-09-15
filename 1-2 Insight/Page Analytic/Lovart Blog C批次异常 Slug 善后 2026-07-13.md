---
type: audit-report
scope: sanity-blog-c-batch
date: 2026-07-13
status: resolved
project: lovart
dataset: production
---

# Lovart Blog C批次异常 Slug 善后 2026-07-13

## 结论

`https-www-lovart-ai-zh-blog-human-ai-cocreation-lovart-canvas-solopreneur-design` 已完成正式善后。

- 异常 slug 已迁移为：`human-ai-cocreation-lovart-canvas-solopreneur-design`
- 旧 slug 在 published 文档中已归零
- 新 slug 下共有 `8` 个多语言 blog 文档
- 同步修复了由 URL 残留带来的 title / SEO title / og alt / structuredData 污点

## 为什么这次可以直接迁移

- 目标干净 slug 在迁移前未被占用
- 本地 GSC 缓存中未命中旧 URL 页面信号
- 因此本轮选择直接完成内容侧 slug 切换，而不是继续保留异常 URL

## 迁移范围

共处理 `8` 篇 published blog：

- `en`
- `zh`
- `ja`
- `fr`
- `ru`
- `pt`
- `de`
- `es`

## 本轮同步修复

- `slug.current`：全部改为 `human-ai-cocreation-lovart-canvas-solopreneur-design`
- 对标题为空或直接等于旧 URL 的文档，修正为可读标题
- 对 `seo.title` / `metaTitle` 为 URL 残留的文档，修正为正常标题
- 对 `seo.ogImage.alt` 为 URL 残留的文档，修正为正常 alt
- 对 `seo.structuredData.json`：
  - 统一把 `@type` 调整为 `Article`
  - 修正 `headline`
  - 修正 `mainEntityOfPage` 中旧 slug 残留

## 结果

- `old slug published count = 0`
- `new slug published count = 8`
- `seo.noIndex` 维持 `false`
- 未删除 production 文档

## 备注

本轮完成的是 **Sanity 内容侧** 的 slug 善后。

由于旧 URL 已不再对应 published 文档，若后续需要把旧路径继续做成 `301`，那属于前端 / 基础设施层动作，不在本次内容侧修复范围内。

## 过程产物

- `tmp/abnormal-slug-doc.json`
- `tmp/c-batch-abnormal-slug-dryrun.json`
- `tmp/c-batch-abnormal-slug-apply.json`
- `tmp/c-batch-abnormal-slug-verify.json`
