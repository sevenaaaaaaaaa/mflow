---
name: lovart-best-practice
description: Best Practice 子技能，用于写 workflow best practices、creative ops 规范、协作与 handoff 规范、参数使用习惯、团队级操作守则。
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# lovart-best-practice

Best Practice 子技能，用于写 workflow best practices、creative ops 规范、协作与 handoff 规范、参数使用习惯、团队级操作守则。

先加载：

- `00-INDEX`
- `lovart-blog-serp-writer`
- `lovart-content-quality-gates`

并遵守共享治理文件：

- `1-1 Harness/Skills/02-creation/references-blog-subskill-governance.md`

## Triggers

- "write a best practice post"
- "workflow best practices"
- "creative ops best practices"
- "最佳实践文章"

## Minimum requirements

- 明确 workflow scope
- 区分 must-do 与 nice-to-have
- 包含 QA / failure prevention
- 包含 handoff 或 scaling 逻辑

## References

Read [references/benchmark-seed-v1.md](references/benchmark-seed-v1.md) for the first benchmark base and the five core Best Practice topic lanes.

Read [references/benchmark-seed-v2.md](references/benchmark-seed-v2.md) to extend coverage into prompt governance, brand consistency, documentation upkeep, and audit-ready workflow operations.

Read [references/benchmark-seed-v3.md](references/benchmark-seed-v3.md) to close gaps around follow-up discipline, maintenance loops, and long-lived team operating quality.

Read [references/lovart-best-practice-playbook.md](references/lovart-best-practice-playbook.md) for structure, required moves, and Lovart-specific operating angles.

Read [references/lovart-best-practice-review-checklist.md](references/lovart-best-practice-review-checklist.md) before treating a draft as category-ready.
