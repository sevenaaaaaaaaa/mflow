# the brand Blog Subskill Governance

Shared governance reference for the brand blog subskills across Cursor / Hermes / Claude / Codex-facing skill trees.

Every blog subskill must inherit:

- `mflow-core`
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

- `content-101`
- `complete-guide`
- `insight-trend`
- `thought-leadership`
- `better-design`
- `best-practice`
- `stack-by-stack`
- `review`
