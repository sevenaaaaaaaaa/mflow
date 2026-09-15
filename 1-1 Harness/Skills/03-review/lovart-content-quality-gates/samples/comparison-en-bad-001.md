---
sample_id: comparison-en-bad-001
verdict: bad
content_type: comparison
language: en
focus_query: canva alternatives
rubric_score: 31
block_triggered: yes
dimension_scores:
  reader_scenario: 5
  serp_intent: 6
  information_density: 4
  evidence_trust: 3
  conversion_next: 4
  structure: 4
  anti_slop_language: 3
  localization: 5
  completeness: 3
preflight:
  pass: false
  codes: [AS_BANNED_PHRASE, UX_FAQ]
reusable_pattern: null
anti_patterns:
  - Competitor bashing without criteria
  - No "best for" for alternatives
  - Lovart wins every row
  - No test method or sources
  - Reads like sales page not comparison
source: internal_synthetic
tags: [comparison, T4-negative, BLOCK]
---

# Sample: Biased comparison (bad)

## Excerpt

> ## Why Canva falls short
>
> Canva is outdated and limited. Unlike Canva, Lovart is the only true AI design agent that revolutionizes everything.
>
> ## Lovart vs everyone
>
> Lovart beats all competitors on quality, speed, and price. Other tools cannot match our seamless workflow.
>
> ## Conclusion
>
> Switch to Lovart today — the clear winner.

## Why this verdict

| Dimension | Score | Note |
|---|---:|---|
| SERP intent | 6 | Comparison searchers want fair selection — not delivered |
| Evidence | 3 | Unsupported superlatives; no scenarios |
| Anti-slop | 3 | revolutionizes, seamless, only true |

**BLOCK (Rubric)**: Comparison without fair verdict and use cases.

## Reuse for Lovart

- **Structure**: Never publish; use in audit training.
- **Fix**: Add criteria table, weak-when rows, and `[待考证]` on competitor claims.

## Related

- Pair with: `comparison-en-good-001`
- Rubric Blog BLOCK: no fair selection framework
