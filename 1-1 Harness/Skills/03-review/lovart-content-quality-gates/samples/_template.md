---
sample_id: {type}-{lang}-{verdict}-###
verdict: good
content_type: blog
language: en
focus_query:
rubric_score: 0
block_triggered: no
dimension_scores:
  reader_scenario: 0
  serp_intent: 0
  information_density: 0
  evidence_trust: 0
  conversion_next: 0
  structure: 0
  anti_slop_language: 0
  localization: 0
  completeness: 0
preflight:
  pass: false
  codes: []
reusable_pattern:
anti_patterns: []
source: internal
tags: []
---

# Sample: {title}

## Excerpt

> （粘贴 150–400 词代表性片段）

## Why this verdict

| Dimension | Score | Note |
|---|---:|---|
| Reader / scenario | | |
| SERP intent | | |
| … | | |

## Reuse for Lovart

- **Structure**:
- **Do not copy**:

## Preflight expectation

```text
node anti-slop-preflight.js --file this-sample.md --strict
→ pass / fail
→ codes:
```

## Ledger snapshot（good/gold 建议填写）

| Section | Job |
|---|---|
| | |

## Related

- SERP:
- Storyline:
- Pair with bad sample:
