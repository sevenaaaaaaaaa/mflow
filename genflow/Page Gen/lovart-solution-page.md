# Lovart Solution Page Skill

## Description

Generate and validate Lovart **Solution** landing pages (`category: solution`, `composite-v2`, 12 sections). Uses the **v2 dual-axis storyline system**: 6 persona (P1–P6) + 6 industry (I1–I6) storylines.

**Trigger Phrases**: solution page, write solution JSON, solution storyline, 方案页, Solution 故事线, 行业轴, 人群轴

---

## SSOT (read first)

| File | Purpose |
|------|---------|
| `solution-storylines-v2.json` | Machine-readable 12 storylines + selection rules + coverage |
| `SOLUTION-TAXONOMY.md` | Human-readable axis balance and selection priority |
| `SOLUTION-PRODUCTION.md` | Production workflow and example index |
| `../Refresh-Page/README.md` | Section `type` field schemas |
| `../Refresh-Page/preview-data.json` | Copy-paste JSON skeletons per `type` |

**Industry signals beat persona signals.** If still ambiguous → `solution-p-marketing`.

---

## Storyline IDs (v2)

### Persona axis (P1–P6)

| ID | Code | Hero | Proof segment |
|----|------|------|---------------|
| `solution-p-marketing` | P1 | `hero-cinematic` | `testimonial` |
| `solution-p-founder` | P2 | `hero-journey` | `testimonial` |
| `solution-p-design` | P3 | `hero-cinematic` | `review-grid-3col` |
| `solution-p-agency` | P4 | `hero-mosaic` | `review-grid-4col` |
| `solution-p-enterprise` | P5 | `hero-cinematic` + `bento-6` | `review-grid-3col` |
| `solution-p-individual` | P6 | `hero-split` | `testimonial` + `comparison-before-after` |

### Industry axis (I1–I6) — all have JSON examples

| ID | Code | Hero | Proof segment |
|----|------|------|---------------|
| `solution-i-ecommerce` | I1 | `hero-journey` | `review-grid-3col` |
| `solution-i-saas` | I2 | `hero-cinematic` | `review-grid-3col` |
| `solution-i-local` | I3 | `hero-journey` | `testimonial` |
| `solution-i-wellness` | I4 | `hero-cinematic` | `testimonial` + `comparison-before-after` |
| `solution-i-mission` | I5 | `hero-journey` | `testimonial` |
| `solution-i-creator` | I6 | `hero-gallery` | `testimonial` + `showcase-horizontal` |

Full 12-section order: `storylines[ID].sections` in SSOT.

---

## Workflow

### Step 0 — Route storyline

1. Read slug, title, and content strategy draft.
2. Match `selectionRules` in SSOT (industry rules first).
3. Announce chosen `storyline` ID and axis.
4. Do **not** use deprecated IDs (`solution-team`, `solution-solo`, etc.) in new JSON.

### Step 1 — Build JSON

Required top-level fields:

```json
{
  "_type": "compositePage",
  "category": "solution",
  "schemaVersion": "composite-v2",
  "storyline": "solution-i-saas",
  "slug": "ai-design-solution-for-saas",
  "language": "en",
  "section": [],
  "bodyJson": "[]",
  "seo": { "noIndex": true }
}
```

- `section`: ordered array of 12 objects, each with `"type"` matching SSOT.
- `bodyJson`: `JSON.stringify(section)` as a string.

### Step 2 — Validate

- Section count = 12.
- `type` sequence exactly matches `storylines[storyline].sections`.
- No legacy section keys (`heroSection`, `faqSection`, etc.).
- Draft examples use `seo.noIndex: true` until preflight passes.

### Step 3 — Reference examples

Copy tone/structure from `en/`:

- Industry: `_generate-industry-examples.js` output (I1–I6).
- Persona: `_generate-examples.js` output (P1 marketing, P4 agency; shopify = I1).

---

## Common mis-routes (fix these)

| Content | Wrong | Correct |
|---------|-------|---------|
| Small business hub | `solution-p-individual` | `solution-i-local` |
| Fitness / wellness hub | `solution-p-individual` | `solution-i-wellness` |
| Startups markdown | `solution-p-marketing` | `solution-p-founder` |
| Shopify / DTC | `solution-p-marketing` | `solution-i-ecommerce` |

---

## Harness placement

Canonical copy: this file. Mirror to `1-5 Harness/Skills/lovart-solution-page.md` when that directory is writable.
