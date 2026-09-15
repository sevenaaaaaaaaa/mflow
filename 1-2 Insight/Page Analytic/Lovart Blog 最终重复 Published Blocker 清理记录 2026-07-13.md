---
type: audit-report
scope: sanity-blog-signal-refresh
date: 2026-07-13
status: resolved
project: lovart
dataset: production
---

# Lovart Blog 最终重复 Published Blocker 清理记录 2026-07-13

## 结论

本轮已把 B 批次尾部遗留的重复 published blocker 全部收口。

- 英文重复 published slug `531/532`、`623/624`、`699/701`、`709/712` 已全部处理完毕
- 额外发现并一并处理了 `hedra-ai-vs-lovart` 的意大利语重复 published 文档
- 处理方式为：**保留 1 个 canonical published 文档，其他重复 published 退回 draft**
- 未删除 production 文档，符合“修复优先于删除”的项目铁律

## 本轮保留的 canonical published

- `best-ai-design-agent-for-content-creator`
  - 保留：`best-ai-design-agent-for-content-creator`
  - 退回 draft：`blog-best-ai-design-agent-for-content-creator-en`

- `canva-templates-vs-lovart-generative-layouts-which-is-truly-unique`
  - 保留：`canva-templates-vs-lovart-generative-layouts-which-is-truly-uniq`
  - 退回 draft：`c5f79b2a-1702-4be4-a750-6baa7b33020f`

- `lovart-vs-canva-2026`
  - 保留：`bd-lovart-vs-canva-2026`
  - 退回 draft：`blog-lovart-vs-canva-2026-en`

- `hedra-ai-vs-lovart`（英文）
  - 保留：`hedra-ai-vs-lovart`
  - 退回 draft：`0fqG5ke3o5nAjEjVNKlO71`

- `hedra-ai-vs-lovart`（意大利语）
  - 保留：`Ip5hch9IxGqVzC92ps25NV`
  - 退回 draft：`y2MFYERGQO0IvWXX59UBXK`

## 复扫结果

对以下 4 个最终 blocker slug 做 published 复扫后，结果如下：

- `best-ai-design-agent-for-content-creator`：每语言 published 数均为 `1`
- `canva-templates-vs-lovart-generative-layouts-which-is-truly-unique`：每语言 published 数均为 `1`
- `lovart-vs-canva-2026`：英文 published 数为 `1`
- `hedra-ai-vs-lovart`：英文 published 数为 `1`，意大利语 published 数为 `1`

即：**本轮追踪的重复 published blocker 已归零**。

## 处理说明

- 本轮未改动正文结构，不影响已完成的 signal refresh 成果
- 本轮未设置 `noIndex`
- 本轮未做 destructive delete，仅执行 unpublish，使重复 published 文档回到 draft 状态

## 过程产物

- 中段 blocker 旧记录：`1-2 Insight/Page Analytic/Lovart Blog Signal Writer B批次中段剩余 Blocker 清理记录 2026-07-13.md`
- 重复文档检查缓存：`tmp/final-duplicate-docs-inspect.json`
- 最终唯一性摘要：`tmp/final-blocker-summary.json`
