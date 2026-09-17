---
name: lovart-stack-by-stack
description: Stack × Stack 子技能，用于写 tool stack、workflow stack、A+B vs C+D 的整栈比较文章。
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# lovart-stack-by-stack

Stack × Stack 子技能，用于写 tool stack、workflow stack、A+B vs C+D 的整栈比较文章。

先加载：

- `lovart-core`
- `lovart-blog`
- `lovart-content-quality-gates`

并遵守共享治理文件：

- `1-1 Harness/Skills/02-creation/references-blog-subskill-governance.md`

## Triggers

- "write a stack comparison"
- "tool stack comparison"
- "stack vs stack"
- "workflow stack"
- "整栈对比文章"

## Minimum requirements

- 定义每一套 stack
- 比较 workflow friction、handoff、成本、适用人群
- 明确谁该选什么，不允许 everyone-wins

## References

Read [references/benchmark-seed-v1.md](references/benchmark-seed-v1.md) for the first Stack × Stack benchmark base and five core stack-comparison lanes.

Read [references/benchmark-seed-v2.md](references/benchmark-seed-v2.md) to extend coverage into creator stacks, B2B marketing stacks, orchestration layers, and context-switch cost analysis.

Read [references/benchmark-seed-v3.md](references/benchmark-seed-v3.md) to deepen ownership, operating-model, and team-boundary comparisons in multi-tool stacks.

Read [references/lovart-stack-by-stack-playbook.md](references/lovart-stack-by-stack-playbook.md) for comparison structure, tested-workflow expectations, and anti-patterns.

Read [references/lovart-stack-by-stack-review-checklist.md](references/lovart-stack-by-stack-review-checklist.md) before approving a draft.
