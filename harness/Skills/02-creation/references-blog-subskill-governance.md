# the brand Blog Subskill Governance

Shared governance reference for the brand blog subskills across Cursor / Hermes / Claude / Codex-facing skill trees.

Every blog skill must inherit:

- `mflow-core`（= RULES-00-iron 全文，经 harness_sync 编译为 .cursor 规则；引用悬空历史见 HARNESS-SKILLS-AUDIT）
- blog production rules
- quality-gate rules

And must not bypass:

- category labeling
- publish-date consistency
- cover strategy
- internal-link routing
- FAQ / layout integrity
- anti-slop and publish-readiness checks

## Mandatory publishability checks

- clear primary blog category
- title / slug / language present
- publish-date intent present
- cover present or cover strategy defined
- internal links planned
- article-type structure stable
- no broken hierarchy
- no duplicated core sections or FAQ blocks
- quality gates acknowledged

## Applies to（2026-10-03 起 8 个类型子技能并入 blog-writer/references/types/，以 GUIDE.md 形式存在，不再是独立技能）

- `references/types/101/GUIDE.md`
- `references/types/best-practice/GUIDE.md`
- `references/types/better-design/GUIDE.md`
- `references/types/complete-guide/GUIDE.md`
- `references/types/insight-trend/GUIDE.md`
- `references/types/review/GUIDE.md`
- `references/types/stack-by-stack/GUIDE.md`
- `references/types/thought-leadership/GUIDE.md`
