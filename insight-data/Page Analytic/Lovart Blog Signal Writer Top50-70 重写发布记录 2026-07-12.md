---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-12
status: published-top50-70-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top50-70 重写发布记录 2026-07-12

## 结论

本轮按用户指定范围执行英文 Blog Top 100 第一阶段 signal refresh，已完成 Top 50-70，共 21 个 published 文档，并 patch 到 Sanity production。

为避免 rank 60 重复处理，本轮拆成 Top 50-59 与 Top 60-70 两批执行。Top 41-49 本轮未处理，后续可补。

本轮仍属于第一阶段：按 GSC 查询信号修正搜索意图、标题/SEO、结构块、FAQ、E-E-A-T、内链、图片 brief、CTA 与 Article JSON-LD。最终 7,500 词多轮长文扩写会在 Top 100 第一阶段完成后统一进入第二阶段。

## 已发布范围

Top 50-59：

1. `complete-guide-ai-sketch-drawing-generation`
2. `instagram-stories-ai-guide`
3. `how-to-upscale-images-ai-bing`
4. `ai-business-card-design`
5. `ai-design-tools-pricing-comparison-2026`
6. `b42-ai-design-pricing-guide-bing`
7. `6-best-ai-character-consistency-tools-2026`
8. `ai-illustration-mistakes`
9. `what-is-goenhance-ai`
10. `ai-lip-sync-video-2026`

Top 60-70：

1. `ai-price-list-maker-small-business`
2. `imagineart-review`
3. `7-best-ai-poster-design-tools-2026`
4. `ai-art-platforms-compared-2026`
5. `expression-sheets-generating-a-grid-of-emotions-for-one-character`
6. `5-best-ai-texture-material-generators-2026`
7. `infinite-canvas-ai-design-ui`
8. `complete-guide-ai-poster-design-printing`
9. `storyboarding-consistent-character-video-script-ai`
10. `inside-mcot-engine-ai-design-reasoning`
11. `ai-illustration-prompts`

## 线上验收

published 视角复扫结果：

- 21/21 `seo.noIndex=false`
- 21/21 Article JSON-LD 存在
- 21/21 含 FAQ
- 21/21 含 Derivative Scenarios
- 21/21 含 E-E-A-T Notes
- 21/21 含 Internal Links
- 21/21 含 Image Appendix
- 21/21 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- Top 50-59 dry-run：`tmp/top50-59-signal-rewrite-dryrun.json`
- Top 50-59 apply：`tmp/top50-59-signal-rewrite-applied.json`
- Top 60-70 dry-run：`tmp/top60-70-signal-rewrite-dryrun.json`
- Top 60-70 apply：`tmp/top60-70-signal-rewrite-applied.json`
- published 复扫：`tmp/top50-70-published-verify.json`

