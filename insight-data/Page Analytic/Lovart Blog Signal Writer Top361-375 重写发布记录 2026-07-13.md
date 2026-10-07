---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: published-top361-375-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top361-375 重写发布记录 2026-07-13

## 结论

本轮继续执行第一阶段 signal refresh，已完成 Top 361-375，共 15 个 published 文档，并 patch 到 Sanity production。

本批严格按主线要求执行：基于 GSC 查询信号修正搜索意图，刷新 title、description、seo、Article JSON-LD，并补齐 FAQ、Derivative Scenarios、E-E-A-T Notes、Internal Links、Image Appendix 与 signup CTA。

## 已发布范围

Top 361-375：

1. `how-to-chat-generate-ui-layout-lovart`
2. `animate-old-photos-ai-2026`
3. `how-to-add-textured-grain-posters`
4. `how-to-chat-generate-mockup-lovart`
5. `04-best-practice-touch-edit`
6. `how-to-design-restaurant-menu-brand-ai`
7. `why-i-tested-seaart`
8. `adobe-express-vs-lovart-comparison`
9. `invideo-vs-lovart-video-editing-comparison`
10. `s21---lovart-customer-success-story`
11. `best-ai-design-agent-for-dropshipper`
12. `ai-design-agent-for-artisan-bakery-branding`
13. `canva-alternatives-2026`
14. `step-by-step-youtube-thumbnails-without-photoshop`
15. `adobe-firefly-alternatives-2026`

## 线上验收

published 视角复扫结果：

- 15/15 `seo.noIndex=false`
- 15/15 Article JSON-LD 存在，且 `@type=Article`
- 15/15 含 FAQ
- 15/15 含 Derivative Scenarios
- 15/15 含 E-E-A-T Notes
- 15/15 含 Internal Links
- 15/15 含 Image Appendix
- 15/15 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- Top 361-375 dry-run：`tmp/top361-375-signal-rewrite-dryrun.json`
- Top 361-375 apply：`tmp/top361-375-signal-rewrite-applied.json`
- published 复扫：`tmp/top361-375-published-verify.json`
