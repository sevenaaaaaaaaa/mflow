---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: published-top121-150-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top121-150 重写发布记录 2026-07-13

## 结论

本轮继续执行第二层 `B_indexed_or_visible_refresh`，已完成 Top 121-150，共 30 个 published 文档，并 patch 到 Sanity production。

本轮仍属于第一阶段 signal refresh：按 GSC 查询信号修正搜索意图、标题/SEO、结构块、FAQ、E-E-A-T、内链、图片 brief、CTA 与 Article JSON-LD。最终 7,500 词多轮长文扩写会在更大范围第一阶段完成后统一进入第二阶段。

## 已发布范围

Top 121-135：

1. `01-cluster-brand-kit-from-scratch`
2. `ai-texture-generator-tools-compared`
3. `8-best-ai-object-removers-watermark-removers-2026`
4. `15-best-free-ai-design-tools-2026`
5. `fotor-ai-review-2025-photo-editing-and-ai-art-generator-tested`
6. `how-to-generate-cinematic-video-prompts`
7. `03-best-practice-psd-vs-png`
8. `how-to-use-free-ai-design-tools`
9. `03-cluster-color-psychology-ai-design`
10. `how-to-transform-age-body-ai-portraits`
11. `10-best-ai-print-design-tools-2026`
12. `02-cluster-brand-style-guide-ai`
13. `01-industry-hair-salon-menu`
14. `ai-art-generator-tools-compared`
15. `ai-collage-moodboard-tools-compared`

Top 136-150：

1. `brand-kit-martial-arts-lovart`
2. `ai-poster-tools-compared`
3. `8-best-ai-background-wallpaper-generators-2026`
4. `ai-illustrations-social-media`
5. `6-best-ai-art-platforms-2026`
6. `lovart-ai-image-generator-create-stunning-images`
7. `complete-guide-ai-avatar-digital-identity`
8. `best-ai-design-agent-for-makeup-studio-owner`
9. `adobe-firefly-vs-ai-design-agents`
10. `best-luma-dream-machine-alternatives-in-2025-ai-video-tools`
11. `ai-print-materials-tools-compared`
12. `5-best-ai-image-models-compared-2026`
13. `b33-ai-background-remover-comparison-bing`
14. `pollo-ai-vs-lovart-comparison`
15. `best-ai-design-agent-for-bubble-tea-shop-owner`

## 线上验收

published 视角复扫结果：

- 30/30 `seo.noIndex=false`
- 30/30 Article JSON-LD 存在
- 30/30 含 FAQ
- 30/30 含 Derivative Scenarios
- 30/30 含 E-E-A-T Notes
- 30/30 含 Internal Links
- 30/30 含 Image Appendix
- 30/30 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- Top 121-135 dry-run：`tmp/top121-135-signal-rewrite-dryrun.json`
- Top 121-135 apply：`tmp/top121-135-signal-rewrite-applied.json`
- Top 136-150 dry-run：`tmp/top136-150-signal-rewrite-dryrun.json`
- Top 136-150 apply：`tmp/top136-150-signal-rewrite-applied.json`
- published 复扫：`tmp/top121-150-published-verify.json`

