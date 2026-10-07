---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-12
status: published-top41-49-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top41-49 重写发布记录 2026-07-12

## 结论

本轮补齐此前跳过的英文 Blog Top 41-49，共 9 个 published 文档，并 patch 到 Sanity production。

本轮仍属于第一阶段 signal refresh：按 GSC 查询信号修正搜索意图、标题/SEO、结构块、FAQ、E-E-A-T、内链、图片 brief、CTA 与 Article JSON-LD。最终 7,500 词多轮长文扩写会在 Top 100 第一阶段完成后统一进入第二阶段。

## 已发布范围

1. `runway-vs-pika-vs-kling-2026`
2. `capcut-ai-review`
3. `ai-animation-from-script`
4. `free-ai-design-tools-online-no-signup-2026`
5. `how-to-use-nano-banana-pro-free`
6. `best-image-to-video-tools-2026`
7. `the-vectorize-toggle-turning-ai-art-into-scalable-graphics`
8. `ai-face-swap-ethics-legal-2026`
9. `ai-menu-design-restaurant-layout`

## 线上验收

published 视角复扫结果：

- 9/9 `seo.noIndex=false`
- 9/9 Article JSON-LD 存在
- 9/9 含 FAQ
- 9/9 含 Derivative Scenarios
- 9/9 含 E-E-A-T Notes
- 9/9 含 Internal Links
- 9/9 含 Image Appendix
- 9/9 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- dry-run：`tmp/top41-49-signal-rewrite-dryrun.json`
- apply：`tmp/top41-49-signal-rewrite-applied.json`
- published 复扫：`tmp/top41-49-published-verify.json`

