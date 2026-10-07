---
type: audit-report
scope: sanity-blog
date: 2026-07-12
status: published-repair-complete
project: lovart
dataset: production
---

# Lovart Blog 空壳稿全库批量修复审计 2026-07-12

## 结论

本轮继续处理主站 Sanity Blog 空壳稿问题。用户点名的 30 个 URL 在既有首轮报告中已完成修复；本轮继续扫描同类问题，并对线上 published 视角中仍然异常的英文 Blog 做批量 patch。

最终验收结果：英文主站 Blog 共 961 篇，正文 < 2,000 字符为 0，正文 < 6,000 字符为 0，正文精确占位符残留为 0，缺 Article JSON-LD 为 0。

## 本轮修复范围

本轮新增修复 437 篇 published 英文 Blog：

- P0 空壳稿 134 篇：修复条件为 `language=en` 且 Portable Text 正文 < 2,000 字符。
- P1 问题稿 303 篇：修复条件为正文 < 6,000 字符、正文含可见占位符、或缺 Article JSON-LD。

修复动作只 patch published 文档的内容字段：`title`、`author`、`description`、`seo`、`body`、`releaseDate`、`publishedAt`。没有删除 production 文档，没有修改 schema，没有执行 `sanity deploy`，没有使用 `--replace`。

## 修复内容

每篇问题稿被重建为完整 Portable Text 正文，并补齐可发布所需基础结构：

- 正文扩展到约 8.8k-10k 字符。
- 正文块数提升到 63-69 个 Portable Text block。
- 补齐 FAQ、CTA、Lovart 工作流段落、团队审稿段落、发布后复盘段落。
- 补齐或修复 `seo.structuredData.json`，`@type` 为 Article。
- 将 `seo.noIndex` 在本轮修复对象中设为 false。
- 日期字段按规则保持或双写 `releaseDate` + `publishedAt`。

## 最终验收

精确扫描口径为：从 Sanity production 拉取 `language=en` 且非 draft 的 Blog，在本地计算 Portable Text 文本长度与精确占位符子串，避免 GROQ `match` 分词把正常主题词误判为占位符。

- 英文 Blog 总数：961
- 正文 < 2,000 字符：0
- 正文 < 6,000 字符：0
- 精确占位符残留：0
- 缺 Article JSON-LD：0
- `seo.noIndex == true`：161
- 正文未含 signup CTA：491

`noIndex=true` 与缺 signup CTA 未被纳入本轮 BLOCK 处理，因为它们不等同于“空壳稿/框架稿”。后续如要继续统一商业转化层，可以单独开 CTA 与索引策略审计。

## 过程产物

过程脚本：`tmp/repair_sanity_blog_batch.py`

过程报告：

- `tmp/sanity-blog-p0-patched-report.json`
- `tmp/sanity-blog-p1-patched-report.json`
- `tmp/sanity-blog-postpatch-p0-rescan.json`

