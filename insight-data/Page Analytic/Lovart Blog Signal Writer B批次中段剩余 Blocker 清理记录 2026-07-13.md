---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: partial-complete-batch-b-mid
project: lovart
dataset: production
---

# Lovart Blog Signal Writer B批次中段剩余 Blocker 清理记录 2026-07-13

## 结论

本轮在限定范围 `531-532`、`613`、`623-624`、`629`、`699/701`、`709/712` 内，已安全完成可隔离条目的第一阶段 signal refresh：`613`、`629`。

其余未推进条目均属于 **重复英文 published 文档** blocker。按项目铁律，本轮未做删除、合并或破坏性修复，只保留 blocker 与建议。

## 分类结果

- 重复英文 published 文档：
  - `531-532` → slug `best-ai-design-agent-for-content-creator`
  - `623-624` → slug `canva-templates-vs-lovart-generative-layouts-which-is-truly-unique`
  - `699/701` → slug `lovart-vs-canva-2026`
  - `709/712` → slug `hedra-ai-vs-lovart`
- 禁用词冲突：
  - `613` → 原默认生成路径会把 `the future of` 带回 title/query 文本；已通过脚本收窄修复并完成 refresh
- 异常 slug：
  - `629` → slug `https-www-lovart-ai-zh-blog-vector-logo-export-why-you-need-svg-files-for-signage-and-print`；本轮仅做 signal refresh，不改 slug

## 已完成 signal refresh

### Rank 613

- dry-run：通过
- apply：已完成
- published verify：通过
- English published slug count：`1`

### Rank 629

- dry-run：通过
- apply：已完成
- published verify：通过
- English published slug count：`1`

## 未解决 blocker

### Rank 531-532

- 最小原因：同一英文 slug 当前已有 `2` 个 published 文档
- IDs：
  - `best-ai-design-agent-for-content-creator`
  - `blog-best-ai-design-agent-for-content-creator-en`
- 建议：先人工确定保留主文档 `_id`，再单独设计去重/归并方案；不要在 signal refresh 批处理中直接推进

### Rank 623-624

- 最小原因：同一英文 slug 当前已有 `2` 个 published 文档
- IDs：
  - `c5f79b2a-1702-4be4-a750-6baa7b33020f`
  - `canva-templates-vs-lovart-generative-layouts-which-is-truly-uniq`
- 建议：先人工确定 canonical published 文档，再做后续去重；不要在 signal refresh 批处理中直接推进

### Rank 699/701

- 最小原因：同一英文 slug 当前已有 `2` 个 published 文档
- IDs：
  - `bd-lovart-vs-canva-2026`
  - `blog-lovart-vs-canva-2026-en`
- 说明：该组此前已完成 signal refresh，本轮仅确认 blocker 仍存在

### Rank 709/712

- 最小原因：同一英文 slug 当前已有 `2` 个 published 文档
- IDs：
  - `0fqG5ke3o5nAjEjVNKlO71`
  - `hedra-ai-vs-lovart`
- 说明：该组此前已完成 signal refresh，本轮仅确认 blocker 仍存在

## 过程产物

- 批处理脚本：`tmp/rewrite_signal_batch.py`
- 基脚本调整：`tmp/rewrite_top10_signal_blogs.py`
- `613` dry-run：`tmp/top613-signal-rewrite-dryrun.json`
- `613` apply：`tmp/top613-signal-rewrite-applied.json`
- `613` verify：`tmp/top613-published-verify.json`
- `613` uniqueness：`tmp/top613-published-uniqueness.json`
- `629` dry-run：`tmp/top629-signal-rewrite-dryrun.json`
- `629` apply：`tmp/top629-signal-rewrite-applied.json`
- `629` verify：`tmp/top629-published-verify.json`
- `629` uniqueness：`tmp/top629-published-uniqueness.json`
- `531-532` uniqueness：`tmp/top531-532-published-uniqueness.json`
- `623-624` uniqueness：`tmp/top623-624-published-uniqueness.json`
