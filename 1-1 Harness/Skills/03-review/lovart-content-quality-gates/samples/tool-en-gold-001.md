---
sample_id: tool-en-gold-001
verdict: gold
content_type: tool
language: en
focus_query: ai commercial generator
rubric_score: 91
block_triggered: no
dimension_scores:
  reader_scenario: 15
  serp_intent: 15
  information_density: 14
  evidence_trust: 13
  conversion_next: 10
  structure: 10
  anti_slop_language: 9
  localization: 5
  completeness: 9
preflight:
  pass: true
  codes: []
reusable_pattern: "Hero IO sentence + 3-step workflow + buyer use cases + proof formats + FAQ objections + low-risk CTA"
anti_patterns: []
source: serp_observed
tags: [commercial, marketing-video, T1, hero-io]
storyline: T1
---

# Sample: AI commercial tool landing (gold structure)

> **Source type**: `external` — structural synthesis from Creatify, OpenArt, Topview SERP patterns. **Do not copy vendor wording.**

## Excerpt

> **Hero**  
> Turn a product photo, URL, or script into 9:16, 16:9, and 1:1 ad variants — then edit hooks and CTAs without reshooting.
>
> **Workflow**  
> 1. **Input**: Upload product image, paste URL, or drop a campaign brief.  
> 2. **Generate**: Pick platform (Meta, TikTok, YouTube), voice, captions, and 3–5 hook variants.  
> 3. **Refine**: Swap scenes, fix product label drift, export MP4 or share review link.
>
> **FAQ**  
> - Can I use outputs in paid ads? → Commercial terms by plan; check asset rights.  
> - What if the product label moves between shots? → Re-lock reference frame before export.  
> - Do I need a video editor? → No timeline skills; touch edits per scene.

## Why this verdict

| Dimension | Score | Note |
|---|---:|---|
| SERP intent | 15 | First screen = job + input + output + formats |
| Information density | 14 | Every block names concrete artifacts |
| Evidence | 13 | Formats, platforms, edit path — not "stunning" |
| Conversion | 10 | FAQ answers hesitation; CTA implied low-risk |
| Anti-slop | 9 | Adjectives replaced by IO spec; one "without reshooting" is acceptable constraint |

**Gold because**: Matches Template A from SERP Pattern Library; maps to storyline `T1`.

## Reuse for Lovart

- **Structure**: Copy section order into Page Ledger: hero → workflow → use cases → proof → FAQ → CTA.
- **Do not copy**: Performance metrics, G2 claims, or competitor-specific modules unless verified.

## Preflight expectation

Composite JSON built from this structure should pass `checkCompositePage` with FAQ ≥3 and CTA present.

## Ledger snapshot

| Section | module_job | input | output |
|---|---|---|---|
| hero | State commercial job | photo/URL/script | 9:16, 16:9, 1:1 variants |
| workflow | Show path | brief | edited MP4 |
| faq | Remove legal/edit anxiety | — | commercial, drift, skill |

## Related

- SERP: `global-en-serp-copy-research-2026-06.md` § Creatify, OpenArt, Template A
- Pair with: `tool-en-bad-001`
- Storyline: `T1`, `T-long`
