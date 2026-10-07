---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: published-top626-628-complete
project: lovart
dataset: production
---

# Lovart Blog Signal Writer Top626-628 重写发布记录 2026-07-13

## 结论

本轮已完成 Top 626-628，共 3 个 published 英文文档的第一阶段 signal refresh，并已 patch 到 Sanity production。

本批严格沿用主线脚本执行：基于 GSC 查询信号刷新 title、description、seo、Article JSON-LD，并补齐 FAQ、Derivative Scenarios、E-E-A-T Notes、Internal Links、Image Appendix 与 signup CTA。

本轮未进入第二阶段长文升级；全部文档均停留在第一阶段 signal refresh 范围内。

## 已发布范围

Top 626-628：

1. `brand-kit-dance-studio-lovart`
2. `case-study-filmmaker-ai-movie-poster`
3. `how-to-create-avatars-cartoons-characters-ai`

## dry-run 摘要

- rank 626 `brand-kit-dance-studio-lovart`：`full-rewrite`，正文字符数 `9025 -> 10640`，区块数 `63 -> 92`
- rank 627 `case-study-filmmaker-ai-movie-poster`：`preserve+signal`，正文字符数 `15962 -> 20274`，区块数 `87 -> 119`
- rank 628 `how-to-create-avatars-cartoons-characters-ai`：`preserve+signal`，正文字符数 `51779 -> 55596`，区块数 `236 -> 268`

dry-run 结果：`BLOCK=0`

## 线上验收

published 视角复扫结果（English published docs）：

- 3/3 `seo.noIndex=false`
- 3/3 Article JSON-LD 存在，且 `@type=Article`
- 3/3 含 FAQ
- 3/3 含 Derivative Scenarios
- 3/3 含 E-E-A-T Notes
- 3/3 含 Internal Links
- 3/3 含 Image Appendix
- 3/3 含 `https://www.lovart.ai/signup` CTA
- 禁用词与占位符：0 BLOCK

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- Top 626-628 dry-run：`tmp/top626-628-signal-rewrite-dryrun.json`
- Top 626-628 apply：`tmp/top626-628-signal-rewrite-applied.json`
- published 复扫：`tmp/top626-628-published-verify.json`
