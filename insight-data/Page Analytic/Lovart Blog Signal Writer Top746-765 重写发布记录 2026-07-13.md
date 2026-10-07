---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: published-top746-765-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top746-765 重写发布记录 2026-07-13

## 结论

本轮已完成 Top 746-765，共 20 个 published 英文文档的第一阶段 signal refresh，并已 patch 到 Sanity production。

本批沿用主线脚本执行：基于 GSC 查询信号修正搜索意图，刷新 title、description、seo、Article JSON-LD，并补齐 FAQ、Derivative Scenarios、E-E-A-T Notes、Internal Links、Image Appendix 与 signup CTA。

本轮未进入第二阶段长文升级；全部文档均停留在第一阶段 signal refresh 范围内。

## 已发布范围

Top 746-765：

1. `brand-kit-for-real-estate-agent`
2. `how-to-create-price-guides-without-photoshop`
3. `how-to-create-service-price-lists-without-photoeshop`
4. `lip-sync-ai-tutorial`
5. `brand-kit-urgent-care-lovart`
6. `how-to-politely-argue-with-ai-iteration-tips`
7. `saving-the-shoot-fix-missing-prop-product-photo-ai`
8. `03-career-chatcanvas-client-review`
9. `brand-kit-for-consultants`
10. `brand-kit-for-nail-studio-owners`
11. `brand-kit-for-side-hustlers`
12. `how-to-create-portfolio-pages-without-photoshop`
13. `brand-kit-doctor-lovart`
14. `halloween-restaurant-marketing-guide-2027`
15. `brand-kit-for-bakery-owner`
16. `brand-kit-for-coffee-shop-owners`
17. `how-to-create-business-flyers-without-photoshop`
18. `how-to-create-course-sales-pages-without-photoeshop`
19. `canva-vs-ai-design-agents-2026`
20. `a-step-by-step-guide-to-create-instagram-posts-without-photoshop-2`

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

rank 748 与 rank 763 的既有 published slug 分别为 `how-to-create-service-price-lists-without-photoeshop`、`how-to-create-course-sales-pages-without-photoeshop`，存在 `photoeshop` 拼写异常；rank 753 的既有 published slug 为 `03-career-chatcanvas-client-review`，带数字前缀；rank 759 为 `halloween-restaurant-marketing-guide-2027`，标题年份与当前发布日不同。

本轮仅按 `746-765` 范围执行第一阶段 signal refresh；上述条目的 dry-run、apply、published 复扫与 English published slug 唯一性检查均通过，且当前 `published_en_count=1`，因此本段继续沿用既有 published slug 处理，未判定为 blocker。

因此，本段判断为：signal refresh 已完成，published 复扫通过，无需因本段异常 slug 或标题年份中断本批。

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- Top 746-765 dry-run：`tmp/top746-765-signal-rewrite-dryrun.json`
- Top 746-765 apply：`tmp/top746-765-signal-rewrite-applied.json`
- published 复扫：`tmp/top746-765-published-verify.json`
- published 唯一性检查：`tmp/top746-765-published-uniqueness.json`
