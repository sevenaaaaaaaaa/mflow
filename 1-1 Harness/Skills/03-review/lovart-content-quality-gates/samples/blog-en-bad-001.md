---
sample_id: blog-en-bad-001
verdict: bad
content_type: blog
language: en
focus_query: ai design tools
rubric_score: 28
block_triggered: yes
dimension_scores:
  reader_scenario: 3
  serp_intent: 4
  information_density: 2
  evidence_trust: 2
  conversion_next: 2
  structure: 4
  anti_slop_language: 1
  localization: 5
  completeness: 3
preflight:
  pass: false
  codes: [AS_BANNED_DENSITY, AS_GENERIC_H2, AS_THIN_H2, UX_FAQ, UX_CTA]
reusable_pattern: null
anti_patterns:
  - "In today's fast-paced" opening
  - Generic H2 labels (Benefits, Features, Conclusion)
  - No reader, no example, no mechanism
  - No FAQ, no real CTA
  - Future-of-design closing without action
source: internal_fixture
tags: [anti-slop, textbook-bad, training]
---

# Sample: Generic AI design blog (bad)

## Excerpt

> In today's fast-paced world, unlock seamless creativity with our AI-powered platform.
>
> ## Benefits
>
> AI is changing everything. It is very powerful.
>
> ## Features
>
> More generic text without examples.
>
> ## Conclusion
>
> The future of design is bright. Contact us someday.

## Why this verdict

| Dimension | Score | Note |
|---|---:|---|
| Reader / scenario | 3 | No named reader or use case |
| SERP intent | 4 | Does not answer any specific query |
| Information density | 2 | Removing any paragraph changes nothing |
| Evidence | 2 | Zero examples, data, or limits |
| Conversion | 2 | "Contact us someday" is not a CTA |
| Anti-slop | 1 | Hits 5+ banned phrases in <100 words |
| Completeness | 3 | Thin sections; no FAQ |

**BLOCK**: generic H2, no FAQ, no CTA, banned phrase density.

## Reuse for Lovart

- **Structure**: Use only as negative few-shot in prompts.
- **Do not copy**: Anything.

## Preflight expectation

```text
node anti-slop-preflight.js --file ../scripts/_fixtures/slop-sample.md --strict → fail
BLOCK: AS_BANNED_DENSITY, UX_FAQ, UX_CTA
WARN: AS_GENERIC_H2, AS_THIN_H2
```

## Related

- Pair with: `blog-en-good-001`
- Full fixture: `scripts/_fixtures/slop-sample.md`
- Rubric: Blog extra BLOCK — generic H2, no examples
