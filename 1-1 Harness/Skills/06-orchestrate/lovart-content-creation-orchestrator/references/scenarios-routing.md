# Scenarios Routing Reference

Use when `category: scenario` or the reader question is role/workflow fit ("can Lovart work for my job?").

## Source Files

| Source | Purpose |
|---|---|
| `Refresh-Page/scenarios-storylines.json` | 14 storylines, `sections` arrays, theme signals |
| `Refresh-Page/SCENARIOS-PRODUCTION.md` | Production guide, acceptance checklist |
| `Refresh-Page/STORYLINE-BY-DIRECTION.md` §4.4 | Human-readable storyline catalog |
| `Refresh-Page/PAGE-BRIEF.md` | Step 0: confirm scenario vs solution vs product |
| `lovart.sanity.studio/scripts/lib/scenarios-*-theme.js` | Five pilot theme copy blocks |

## When to Use Scenario (not Solution / Product)

| Signal | Use `scenario` |
|---|---|
| Hero subject is a **role** or **weekly workflow** | Yes |
| Hero subject is **org/industry package** | Prefer `solution` |
| Hero subject is **Lovart product name** | Prefer `product` |
| Hero subject is **one tool capability** | Prefer `tool` / `feature` |

## Storyline Selection (14 IDs)

| Need | Storyline |
|---|---|
| Default / first draft | `scenarios-A` |
| Output-first tabs, social batching | `scenarios-B` |
| Full-funnel or weekly loop | `scenarios-journey` |
| Brand-led, cinematic opener | `scenarios-cinematic` |
| Three parallel scenario lanes | `scenarios-portrait` |
| Step-by-step with media | `scenarios-vertical` |
| Six-touchpoint capability scan | `scenarios-bento6` |
| Two outcomes only | `scenarios-bento2` |
| Visual upgrade proof | `scenarios-before-after` |
| Education hub / SEO | `scenarios-blog` |
| Multi-case horizontal carousel | `scenarios-showcase` |
| Staged vertical case story | `scenarios-stacked` |
| Long-quote narrative proof | `scenarios-testimonial` |
| Dense review wall | `scenarios-reviews4` |

## Theme → Preferred Storylines

| Theme | Preferred |
|---|---|
| `ecommerce-operator` | `scenarios-journey`, `scenarios-bento6` |
| `social-media-manager` | `scenarios-B`, `scenarios-showcase` |
| `freelance-designer` | `scenarios-vertical`, `scenarios-stacked` |
| `marketing-director` | `scenarios-bento6`, `scenarios-reviews4` |
| `brand-manager` | `scenarios-cinematic`, `scenarios-before-after` |

## Composite-v2 Rules

- `category: "scenario"`
- `schemaVersion: "composite-v2"`
- Exactly **11** sections; order from `scenarios-storylines.json`
- `storylineId` / `storylineTemplate` = `scenarios-*`
- Pilot drafts: `slug` prefix `draft-`, `seo.noIndex: true`
- No `pricing-block`, `prompt-launcher`, `tool-grid`, `logo-loop`

## Generation

```bash
node scripts/generate-scenarios-storyline-drafts.js          # P0
node scripts/generate-scenarios-new-themes.js                # P1
node scripts/preflight-content.js --dir "<drafts/en>" --composite-v2
```

Publish: `lovart-scenarios-sanity-publish` skill (`import --missing` only).
