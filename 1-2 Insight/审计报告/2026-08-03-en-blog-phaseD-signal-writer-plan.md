# Phase D 执行铁律 — 必须走 `lovart-blog-signal-writer`

> 日期：2026-08-03  
> 对象：严格克隆残留（非 loose 子串误伤）  
> 清单 SSOT：`Output/QA-Memo/en-phaseD-signal-queue-2026-08-03.{json,csv}`  
> 写作队列：`1-3 GenFlow/Lovart-Blog-Pipeline/01-Drafts/_signal-queue-2026-08-03-en-phaseD.md`

## 结论

1. **数量多 ≠ 可以批量灌。** Phase D 每一篇都必须走 `lovart-blog-signal-writer` Content Refresh：信号 → 选题定稿 → 分类子 skill 真写 → quality gates → `status: ready` → **人审** → `lovart-sanity-publish`（只 patch body / 规范字段）。
2. **禁止**：expand/pad 脚本、薄 Local draft 充数、规则改标题冒充重写、同会话批量产出几十篇「看起来够长」的壳文。
3. **污染口径纠正**：loose「6 use cases」子串会误伤已恢复 History 正文（如 haiper）。Phase D 只认 **严格指纹**——`(h2==24 && pad marker) OR Canva 开场整句`。

## 库存（严格指纹，去重 slug）

| 层级 | 规则 | 篇数 | 处置 |
|------|------|-----:|------|
| **D0** | imp≥1000 或 clicks≥10 | **8** | 本周起逐篇 signal-writer |
| **D1** | imp 100–999 | **41** | 随后两周滚动 |
| **D2** | 低/无 GSC | **305** | 低优先级；可并行考虑 noindex/降权，但仍要真写才换正文 |
| **合计 unique** | | **354** | — |

（文档级严格克隆约 357，含少数同 slug twin；写作按 unique slug。）

## Signal Writer 硬门禁（每篇）

| 门 | 要求 |
|----|------|
| 入口 | 仅 `lovart-blog-signal-writer`；`lovart-blog-serp-writer` 作废 |
| 子 skill | 按意图只选一个：review / how-to / complete-guide / best-practice / insight / stack… |
| 字数 | **全分类 ≥7,500 词**（2026-07-17 铁律；旧分档已废止；`<7500` 不得 ready；禁脚本灌字） |
| 结构 | 第一性原理→策略→实操；Derivative Scenarios + FAQ；术语表正确（MCoT/ChatCanvas/…） |
| 内链 | 仅 verified slug；禁止编造 `/blog/` |
| Anti-Slop | 禁用词 / AI tell / 占位图 → BLOCK |
| 指纹 | 成稿不得再命中 24-H2 共享骨架或 Canva 开场 |
| 发布 | `status: ready` 停住；**人审授权**后才 Sanity patch |

## 产能（现实节奏）

| 产能 | D0（8） | D0+D1（49） | 全量 354 |
|------|--------:|------------:|---------:|
| 5 ready/周 | ~2 周 | ~10 周 | ~71 周 |
| 10 ready/周 | ~1 周 | ~5 周 | ~36 周 |

建议稳态：**每周 5–10 篇 ready**，先清空 D0，再吞 D1；D2 不抢带宽。

## D0 开写顺序（GSC 降序）

1. `ai-image-models-compared-2026` — Review/Comparison，目标 ≥7500 — `lovart-review`
2. `how-to-edit-faces-retouch-portraits-ai` — How-To ≥7500
3. `how-to-choose-ai-video-model` — How-To ≥7500
4. `how-to-face-swap-ai-photos-videos` — How-To ≥7500（clicks≥10）
5. `free-vs-paid-ai-tools-compared` — Comparison ≥7500
6. `how-to-choose-ai-art-platform` — How-To ≥7500
7. `10-ai-design-prompts-that-actually-work` — clicks 15 → Review/How-To，≥7500
8. `edit-elements-layered-editing-ai-deep-dive` — clicks 10 → Feature/How-To，≥7500

> D0 现有 ready 稿若 <7500，必须按 RULES-20 multi-turn 扩写达标后再进人审/Sanity；不得按旧分档放行。

## 与 A/B/C 的边界

- A/B/C 已恢复的 History/Local 正文：**止损去克隆**，不等于 signal-writer 终态。
- WEAK 恢复稿另有 refresh 队列；**不与 Phase D 严格克隆混为一谈**。
- Freepik 等已用 ready 稿换掉克隆的，从 Phase D 剔除。

## 下一动作

说「开写 D0」或点名 slug → 按 signal-writer 串行写第 1 篇 → gates → `ready` → 等人审。
