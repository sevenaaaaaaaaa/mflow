---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-12
status: published-top11-20-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top11-20 重写发布记录 2026-07-12

## 结论

本轮继续执行英文 Blog Top 100 第一阶段 signal refresh，已完成 Top 11-20，并 patch 到 Sanity production 的 published 文档。

本轮仍属于第一阶段：按 GSC 查询信号修正搜索意图、标题/SEO、结构块、FAQ、E-E-A-T、内链、图片 brief、CTA 与 Article JSON-LD。它不是最终 7,500 词多轮长文终稿；长文扩写会在 Top 100 第一阶段完成后统一进入第二阶段。

## 已发布的 10 个文档

1. `pika-ai-review-2025-ai-video-generation-platform-hands-on-test`
2. `text-art-ascii-tools-compared`
3. `seedream-4-5-free-guide`
4. `ai-powered-design-agent-for-creators`
5. `best-ai-design-tools-2026`
6. `best-ai-design-tools-2026`（第二个同 slug 文档）
7. `media-io-review`
8. `luma-dream-machine-review-2025-features-pricing-and-honest-performance-test`
9. `hedra-ai-review`
10. `imagefx-review`

## 线上验收

published 视角复扫结果：

- 10/10 `seo.noIndex=false`
- 10/10 Article JSON-LD 存在
- 10/10 含 FAQ
- 10/10 含 Derivative Scenarios
- 10/10 含 E-E-A-T Notes
- 10/10 含 Internal Links
- 10/10 含 Image Appendix
- 10/10 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- dry-run 报告：`tmp/top11-20-signal-rewrite-dryrun.json`
- apply 报告：`tmp/top11-20-signal-rewrite-applied.json`

