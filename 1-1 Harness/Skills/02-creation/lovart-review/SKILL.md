---
name: lovart-review
description: Review 子技能，用于写单品评测、best-of roundups、versus pages、tested-and-compared 类型博客。
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# lovart-review

Review 子技能，用于写单品评测、best-of roundups、versus pages、tested-and-compared 类型博客。

先加载：

- `lovart-core`
- `lovart-blog`
- `lovart-content-quality-gates`

并遵守共享治理文件：

- `1-1 Harness/Skills/02-creation/references-blog-subskill-governance.md`

研究参考：

- `.cursor/skills/lovart-review-benchmark-research/`

## Triggers

- "write a review"
- "tool review"
- "best X"
- "tested and compared"
- "评测 / 测评文章"

## Minimum requirements

- 明确评测对象和 criteria
- strengths / weaknesses / audience-fit
- clear recommendation logic
- 不得写成产品页伪装的 review
