---
type: strategy-queue
scope: blog-quality-upgrade
date: 2026-07-13
status: ready
project: lovart
dataset: production
---

# Lovart Blog 高质量升级队列 2026-07-13

## 结论

本轮从今天已经处理过的 blog 中重建高质量升级队列，共纳入 `886` 篇。

这份队列不再按 rank 段推进，而是按升级角色推进：

- `pillar_candidate`：`89`
- `deep_refresh_candidate`：`354`
- `keep_refresh_only`：`137`
- `cluster_support_only`：`306`

## 范围

已纳入的处理范围为：

- `Top 1-255`
- `Top 301-435`
- `Top 466-961`
- 另含此前单独收口的 blocker rank：`531/532`、`613`、`623/624`、`629`

其中 `C_long_tail_low_value_review` 已按结构 / 清洁 / slug 善后收口，因此也进入升级队列，但默认不走全量长文化。

## 分层统计

- A 批次：`100`
- B 批次：`656`
- C 批次：`130`

### A 批次

- pillar：`89`
- deep refresh：`11`

### B 批次

- deep refresh：`341`
- keep refresh：`137`
- cluster support：`178`

### C 批次

- deep refresh pilot：`2`
- keep refresh：`0`
- cluster support：`128`

## 标签规则

- `pillar_candidate`：高信号且具 broad intent / canonical 潜力，适合做支柱页。
- `deep_refresh_candidate`：不一定做支柱，但值得进入第二阶段深写与证据补强。
- `keep_refresh_only`：保留现有 signal refresh 成果，只补轻量证据、FAQ、标题和 cluster 抛光。
- `cluster_support_only`：承担 cluster 支持位，不做大篇幅升级。

## 各标签示例

### Pillar 候选

- `freepik-ai-image-generator-review` — Review — Review; broad-intent; 268718 impressions; 736 clicks; pos 7.3; strong pillar potential
- `ai-branding-design` — How-To — How-To; broad-intent; 19118 impressions; 435 clicks; pos 10.6; strong pillar potential
- `what-is-civitai-red` — Complete Guide — Complete Guide; broad-intent; 18972 impressions; 45 clicks; pos 6.7; strong pillar potential
- `ai-poster-prompts-tutorial` — How-To — How-To; broad-intent; 6106 impressions; 213 clicks; pos 5.7; strong pillar potential
- `craiyon-ai-review` — Review — Review; broad-intent; 10846 impressions; 42 clicks; pos 6.8; strong pillar potential
- `complete-guide-consistent-ai-character-design` — Complete Guide — Complete Guide; broad-intent; 13872 impressions; 19 clicks; pos 11.3; strong pillar potential
- `text-art-ascii-tools-compared` — Review — Review; broad-intent; 4652 impressions; 49 clicks; pos 6.7; strong pillar potential
- `seedream-4-5-free-guide` — How-To — How-To; broad-intent; 3201 impressions; 68 clicks; pos 8.6; strong pillar potential

### Deep Refresh 候选

- `how-to-use-veo3-free` — How-To — How-To; 5554 impressions; 154 clicks; pos 8.6; worth second-stage depth upgrade
- `the-vectorize-toggle-turning-ai-art-into-scalable-graphics` — How-To — How-To; 1308 impressions; 15 clicks; pos 7.8; worth second-stage depth upgrade
- `ai-business-card-design` — How-To — How-To; 1323 impressions; 13 clicks; pos 8.6; worth second-stage depth upgrade
- `inside-mcot-engine-ai-design-reasoning` — How-To — How-To; 1331 impressions; 6 clicks; pos 7.0; worth second-stage depth upgrade
- `expression-sheets-generating-a-grid-of-emotions-for-one-character` — Best Practice — Best Practice; 636 impressions; 12 clicks; pos 8.2; worth second-stage depth upgrade
- `b27-how-to-generate-ai-art-commercial-bing` — How-To — How-To; 1327 impressions; 2 clicks; pos 10.2; worth second-stage depth upgrade
- `ai-design-cost-complete-breakdown-2026` — How-To — How-To; 1390 impressions; pos 7.7; worth second-stage depth upgrade
- `ai-price-list-maker-small-business` — How-To — How-To; 640 impressions; 10 clicks; pos 8.4; worth second-stage depth upgrade

### Keep Refresh

- `law-firm-branding-trust-authority-design-2027` — How-To — How-To; 1613 impressions; 2 clicks; pos 22.9; maintain signal refresh state
- `ai-video-background-changer` — How-To — How-To; 850 impressions; 10 clicks; pos 20.2; maintain signal refresh state
- `how-to-choose-ai-image-model` — How-To — How-To; 1256 impressions; pos 16.8; maintain signal refresh state
- `midjourney-character-reference-vs-lovart-nano-banana-consistency-test` — Review — Review; 651 impressions; pos 14.0; maintain signal refresh state
- `invideo-vs-lovart-video-editing-comparison` — Review — Review; broad-intent; 69 impressions; pos 13.9; maintain signal refresh state
- `01-industry-hair-salon-menu` — How-To — How-To; 806 impressions; 2 clicks; pos 8.4; maintain signal refresh state
- `faceapp-alternative` — Review — Review; broad-intent; 81 impressions; pos 14.0; maintain signal refresh state
- `04-midjourney-vs-lovart` — Review — Review; 177 impressions; 3 clicks; pos 6.4; maintain signal refresh state

### Cluster Support

- `creating-negative-space-ai-leave-room-for-text` — Best Practice — Best Practice; 872 impressions; 4 clicks; pos 6.5; best kept as cluster support
- `how-to-create-music-videos-ai-beat-sync` — How-To — How-To; 748 impressions; 5 clicks; pos 10.7; best kept as cluster support
- `canva-alternatives-2026` — Review — Review; broad-intent; 55 impressions; pos 14.4; best kept as cluster support
- `adobe-firefly-alternatives-2026` — Review — Review; broad-intent; 52 impressions; pos 18.5; best kept as cluster support
- `veo-ai-free-vs-lovart` — Review — Review; 242 impressions; 3 clicks; pos 7.7; best kept as cluster support
- `01-cluster-brand-kit-from-scratch` — Best Practice — Best Practice; 449 impressions; 6 clicks; pos 6.8; best kept as cluster support
- `best-ai-design-agent-for-amazon-seller` — Best Practice — Best Practice; broad-intent; 110 impressions; pos 17.9; best kept as cluster support
- `best-ai-tools-for-ecommerce-2026` — Best Practice — Best Practice; broad-intent; 108 impressions; pos 18.3; best kept as cluster support

## 输出文件

- 升级队列 CSV：`1-2 Insight/Page Analytic/Lovart Blog 高质量升级队列 2026-07-13.csv`
- 升级队列 JSON：`tmp/blog-upgrade-queue-2026-07-13.json`
