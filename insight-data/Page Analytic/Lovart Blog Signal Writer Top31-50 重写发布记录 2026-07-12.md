---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-12
status: published-top31-50-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top31-50 重写发布记录 2026-07-12

## 结论

本轮已完成英文 Blog 第一批队列中的 Top 31-50 signal refresh，并 patch 到 Sanity production 的 published 文档。

本轮仍属于阶段一：覆盖高优先级页面的 GSC intent、结构、SEO、FAQ、E-E-A-T、内链、图片 brief、CTA 与 Article JSON-LD；不是 7,500 词终稿扩写阶段。

## 线上验收

published 视角复扫结果：

- 20/20 `seo.noIndex=false`
- 20/20 Article JSON-LD 存在
- 20/20 含 GSC signal intro
- 20/20 含 FAQ
- 20/20 含 Derivative Scenarios
- 20/20 含 E-E-A-T Notes
- 20/20 含 Internal Links
- 20/20 含 Image Appendix
- 20/20 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- dry-run 报告：`tmp/signal-batch-31-50-dryrun.json`
- apply 报告：`tmp/signal-batch-31-50-applied.json`

