---
sample_id: tool-en-bad-001
verdict: bad
content_type: tool
language: en
focus_query: ai design generator
rubric_score: 34
block_triggered: yes
dimension_scores:
  reader_scenario: 4
  serp_intent: 5
  information_density: 3
  evidence_trust: 3
  conversion_next: 3
  structure: 5
  anti_slop_language: 2
  localization: 5
  completeness: 4
preflight:
  pass: false
  codes: [AS_BANNED_DENSITY, UX_FAQ, UX_CTA, AS_HERO_IO]
reusable_pattern: null
anti_patterns:
  - Hero is vision-only ("revolutionize creative workflow")
  - No input/output named
  - No edit or export path
  - Feature bullets without workflow
  - Missing FAQ and CTA
  - "For creators and businesses" persona
source: internal_synthetic
tags: [tool-landing, anti-slop, T1-negative]
---

# Sample: Vision-only tool page (bad)

## Excerpt

> **Hero**  
> Revolutionize your creative workflow with our AI-powered design platform. Stunning visuals for creators and businesses.
>
> **Features**  
> - AI-powered generation  
> - Seamless collaboration  
> - Unlock your brand potential  
> - Cutting-edge models  
>
> **CTA**  
> Get started today.

## Why this verdict

| Dimension | Score | Note |
|---|---:|---|
| SERP intent | 5 | Tool query needs IO in 5 seconds — missing |
| Information density | 3 | Features are labels, not mechanisms |
| Evidence | 3 | No formats, limits, or examples |
| Conversion | 3 | CTA ignores hesitation (rights, edit, cost) |
| Anti-slop | 2 | Four banned phrases in hero + features |

**BLOCK (Landing Rubric)**: Hero only vision; no FAQ; no edit/export path.

## Reuse for Lovart

- **Structure**: Negative example for `lovart-page-serp-writer` and Page Ledger checks.
- **Rewrite direction**: Replace hero with "Turn [brief] into [campaign kit] with [edit path]."

## Preflight expectation

Composite JSON with this copy → `UX_FAQ`, `UX_CTA`, `AS_HERO_IO`, `AS_BANNED_DENSITY`.

## Related

- Pair with: `tool-en-gold-001`
- SERP Anti-Slop Lessons: "for creators and businesses" without scenario
