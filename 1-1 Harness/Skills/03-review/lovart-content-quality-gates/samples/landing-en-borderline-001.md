---
sample_id: landing-en-borderline-001
verdict: borderline
content_type: tool
language: en
focus_query: ai design agent
rubric_score: 72
block_triggered: no
dimension_scores:
  reader_scenario: 11
  serp_intent: 10
  information_density: 9
  evidence_trust: 8
  conversion_next: 8
  structure: 7
  anti_slop_language: 6
  localization: 5
  completeness: 8
preflight:
  pass: true
  codes: [AS_BANNED_PHRASE]
reusable_pattern: "Strong category claim but needs one end-to-end workflow proof and deduped modules"
anti_patterns:
  - Duplicated sections / repeated title strings
  - "The brain behind the beauty" filler
  - Feature enumeration without sample workflow
  - Category education missing (agent vs generator)
source: serp_observed
tags: [ai-design-agent, lovart-production, borderline, F7]
storyline: F7
---

# Sample: AI design agent page (borderline)

> **Source**: SERP research notes on Lovart `ai design agent` page weaknesses. Representative synthetic excerpt.

## Excerpt

> **Hero**  
> Stop Prompting. Start Directing. The world's first AI design agent.
>
> **Section (repeated)**  
> AI Design Agent — The brain behind the beauty. Generate stunning assets with seamless AI power.
>
> **Features grid**  
> MCoT · ChatCanvas · Touch Edit · Brand Kit · Nano Banana …
>
> **Comparison table**  
> Lovart vs traditional tools (rows without "best for")

## Why this verdict

| Dimension | Score | Note |
|---|---:|---|
| SERP intent | 10 | Query is category + transactional — page leans feature list |
| Information density | 9 | Repeats title; abstract taglines |
| Evidence | 8 | Features named but no walked-through campaign example |
| Structure | 7 | Duplication hurts scan |
| Anti-slop | 6 | stunning, seamless, world's first without proof |

**Borderline**: Has FAQ, CTA, comparison — but needs rewrite per SERP P1 recommendations.

## Reuse for Lovart

- **Rewrite to gold**: Lead with brief → campaign system workflow; add agent vs generator education; dedupe modules.
- **Ledger**: F7 slots with one `proof` section = full sample project.

## Related

- SERP: `global-en-serp-copy-research-2026-06.md` § Lovart AI Design Agent
- Pair with: `tool-en-gold-001`
- Storyline: `F7`, `T5` for education blocks
