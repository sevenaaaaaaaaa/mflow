# Lovart Blog Subskill Governance

Shared governance reference for Lovart blog subskills across Cursor / Hermes / Claude / Codex-facing skill trees.

Every blog subskill must inherit:

- `lovart-core`
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

## Applies to

- `lovart-101`
- `lovart-complete-guide`
- `lovart-insight-trend`
- `lovart-thought-leadership`
- `lovart-better-design`
- `lovart-best-practice`
- `lovart-stack-by-stack`
- `lovart-review`
