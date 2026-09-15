---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: published-top151-180-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top151-180 重写发布记录 2026-07-13

## 结论

本轮继续执行第二层 `B_indexed_or_visible_refresh`，已完成 Top 151-180，共 30 个 published 文档，并 patch 到 Sanity production。

本轮仍属于第一阶段 signal refresh：按 GSC 查询信号修正搜索意图、标题/SEO、结构块、FAQ、E-E-A-T、内链、图片 brief、CTA 与 Article JSON-LD。最终 7,500 词多轮长文扩写会在更大范围第一阶段完成后统一进入第二阶段。

## 已发布范围

Top 151-165：

1. `ai-illustration-guide-how-to-generate-professional-artwork-from-prompts`
2. `nano-banana-2-lovart-commercial-workflow`
3. `how-to-gen-product-photography-with-ai`
4. `lovart-digest-june-2026-week4`
5. `s27---midjourney-vs-dalle-vs-lovart-three-way`
6. `food-truck-wrap-design-ai`
7. `image-to-video-ai-2026-workflow`
8. `the-best-ai-agent-driven-canvas-for-spa-with-lovart-all-in-one-design-agent`
9. `dall-e-alternatives-2026`
10. `github-ai-coding-tools-comparison-2026`
11. `03-industry-certificate-design-ai`
12. `best-ai-design-agent-for-freelancer`
13. `ai-subscription-fatigue-utility-gap`
14. `picsart-ai-vs-lovart-comparison`
15. `s20-5-ai-design-trends-2026`

Top 166-180：

1. `01-canva-vs-lovart`
2. `03-wiki-export-formats-guide`
3. `06-pillar-design-templates-category`
4. `fast-logo-creation`
5. `ai-interior-design-tools-compared`
6. `logo-design-guide`
7. `lovart-vs-rentahuman-ai-design-comparison`
8. `lovart-ai-complete-overview-features-capabilities`
9. `pictory-ai-review-2025-ai-video-editor-features-pricing-and-test`
10. `adobe-creative-cloud-alternatives-2026`
11. `product-photos-ai-2026-guide`
12. `s11-how-to-use-ai-for-design-beginner-guide`
13. `lovart-digest-june-2026-week1`
14. `best-haiper-ai-alternatives-in-2025-video-generation-compared`
15. `content-gap-analysis-q2-2026`

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
- Top 151-165 dry-run：`tmp/top151-165-signal-rewrite-dryrun.json`
- Top 151-165 apply：`tmp/top151-165-signal-rewrite-applied.json`
- Top 166-180 dry-run：`tmp/top166-180-signal-rewrite-dryrun.json`
- Top 166-180 apply：`tmp/top166-180-signal-rewrite-applied.json`
- published 复扫：`tmp/top151-180-published-verify.json`

