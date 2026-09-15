---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: published-top786-805-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top786-805 重写发布记录 2026-07-13

## 结论

本轮已完成 Top 786-805，共 20 个 published 英文文档的第一阶段 signal refresh，并已 patch 到 Sanity production。

本批沿用主线脚本执行：基于 GSC 查询信号修正搜索意图，刷新 title、description、seo、Article JSON-LD，并补齐 FAQ、Derivative Scenarios、E-E-A-T Notes、Internal Links、Image Appendix 与 signup CTA。

本轮未进入第二阶段长文升级；全部文档均停留在第一阶段 signal refresh 范围内。

## 已发布范围

Top 786-805：

1. `best-ai-design-agent-for-consultants`
2. `lovart-product-update-may-2026`
3. `veed-io-alternative`
4. `brand-kit-plumber-lovart`
5. `best-ai-design-agent-for-financial-advisors`
6. `b26-how-to-create-restaurant-menus-ai-bing`
7. `google-veo-3-ai-review-2025-features-test-results-and-final-verdict`
8. `best-ai-design-agent-for-restaurant-owners`
9. `best-ai-design-agent-for-makeup-studio-owners`
10. `complete-guide-real-estate-marketing-design-ai`
11. `how-to-generate-ai-art-from-text`
12. `best-ai-design-agent-for-content-creators`
13. `best-ai-design-agent-for-handmade-sellers`
14. `lovart-vs-venngage-2026`
15. `brand-kit-for-beauty-salon-owner`
16. `case-study-bootstrapper-free-ai-tools-growth`
17. `best-ai-design-agent-for-personal-trainers`
18. `best-ai-design-agent-for-solo-practitioner`
19. `ai-vs-traditional-designers-2`
20. `brand-consistency-design-guide`

## 线上验收

published 视角复扫结果（English published docs）：

- 20/20 `seo.noIndex=false`
- 20/20 Article JSON-LD 存在，且 `@type=Article`
- 20/20 含 FAQ
- 20/20 含 Derivative Scenarios
- 20/20 含 E-E-A-T Notes
- 20/20 含 Internal Links
- 20/20 含 Image Appendix
- 20/20 含 `https://www.lovart.ai/signup` CTA
- English published slug 唯一性检查：20/20 `published_en_count=1`
- 禁用词与占位符：0 BLOCK

## 本段判断

rank 791 的既有 published slug 为 `b26-how-to-create-restaurant-menus-ai-bing`，带批次/来源前缀；rank 792 的既有 published slug 为 `google-veo-3-ai-review-2025-features-test-results-and-final-verdict`，slug 中保留了 2025 年份，且对应 published `_id` 为截断式 `google-veo-3-ai-review-2025-features-test-results-and-final-verd`；rank 804 的既有 published slug 为 `ai-vs-traditional-designers-2`，带数字后缀。

本轮仅按 `786-805` 范围执行第一阶段 signal refresh；上述条目的 dry-run、apply、published 复扫与 English published slug 唯一性检查均通过，且当前 `published_en_count=1`，因此本段继续沿用既有 published slug 处理，未判定为 blocker。

因此，本段判断为：signal refresh 已完成，published 复扫通过，无需因本段异常 slug、历史年份或数字后缀中断本批。

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- Top 786-805 dry-run：`tmp/top786-805-signal-rewrite-dryrun.json`
- Top 786-805 apply：`tmp/top786-805-signal-rewrite-applied.json`
- published 复扫：`tmp/top786-805-published-verify.json`
- published 唯一性检查：`tmp/top786-805-published-uniqueness.json`
