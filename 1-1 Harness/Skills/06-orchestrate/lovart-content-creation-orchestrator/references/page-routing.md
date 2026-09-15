# Page Routing Reference

Use this before writing Lovart landing/page copy or generating composite-v2 JSON.

## Source Files

| Source | Purpose |
|---|---|
| `1-3 Content Gen/Page Gen/Refresh-Page/STORYLINES.md` | F/T/P/S/C/K/N storylines and module recipes. |
| `1-3 Content Gen/Page Gen/Refresh-Page/scenarios-storylines.json` | Scenarios 14 storylines (`scenarios-*`). |
| `1-3 Content Gen/Page Gen/Refresh-Page/solution-storylines.json` | Solution 6 storylines. |
| `1-3 Content Gen/Page Gen/Refresh-Page/SCENARIOS-PRODUCTION.md` | Scenarios production guide. |
| `references/scenarios-routing.md` | Scenarios theme + storyline selection. |
| `1-3 Content Gen/Page Gen/Refresh-Page/PAGE-MODULE-MATRIX.md` | Component matrix and module direction. |
| `1-1 Harness/Skills/lovart-landing-page/SKILL.md` | Persona, PMF, source verification, CTA, social proof. |
| `1-1 Harness/Skills/lovart-landing-page/tools-v2-template.md` | Tools composite-v2 JSON template and language batches. |
| `1-4 Dev/lovart.sanity.studio/schemaTypes/compositePageType.ts` | Sanity `compositePage` category source. |

## Sanity Categories

`compositePage` categories:

- `feature`
- `tool`
- `product`
- `solution`
- `scenario`
- `topic`

URL patterns:

- `/features/{slug}`
- `/tools/{slug}`
- `/product/{slug}`
- `/solution/{slug}`
- `/scenarios/{slug}`
- `/topic/{slug}`

`Landing Page` is a design/storyline direction, not yet a confirmed standalone Sanity category. Map it to `product`, `solution`, `topic`, or another existing category unless schema changes are explicitly requested.

## Storyline Routing

| Page Need | Storyline | Use When |
|---|---|---|
| Standard feature | `F1` | Common feature pages with trial, steps, capability, proof, FAQ. |
| Model / cinematic | `F2` | Model pages and visually strong feature pages. |
| Video / multimodal | `F3` | Video, image-to-video, multimodal pages. |
| Editing / retouching | `F4` | Before/after, editing, image repair. |
| Industry vertical | `F5` | Restaurant, real estate, ecommerce, law firm, etc. |
| Tool matrix | `F6` | Nano/model/tool collection pages. |
| Agent full workflow | `F7` | AI design agent, campaign workflow, system pages. |
| Standard tool | `T1` | Direct tool job with prompt/workflow/features/FAQ. |
| Single utility | `T2` | Narrow task, quick understanding, few steps. |
| Tool collection | `T3` | Directory, hub, multi-tool selection. |
| Competitor comparison | `T4` | Versus/alternative pages. |
| SEO-heavy reading page | `T5` | Low-interaction educational SEO pages. |
| Production long page | `T-long` | Existing long-chain Tools page or full-funnel page. |
| Product page | `P1-P3` | Core product or package pages. |
| Solution page | `S1-S6` | Business/industry solutions; see `solution-storylines.json`. |
| Scenario page | `scenarios-A` … `scenarios-reviews4` | Role/workflow narrative; see `scenarios-routing.md`. |
| Topic page | `K1-K2` | Topic hub, blog/tools hybrid. |
| Narrative overlay | `N1-N6` | AIDA, proof, price conversion, content + conversion. |

## SERP Page Type Mapping

| SERP Intent | Sanity Category | Storyline |
|---|---|---|
| Direct tool job | `tool` | `T1` or `T2` |
| Tool comparison / alternative | `tool` or `topic` | `T4` |
| Broad category hub | `topic` | `K1` or `K2` |
| Category education | `feature` or `topic` | `F7`, `T5`, or `K2` |
| Industry solution | `solution` or `scenario` | `S1-S6`, `scenarios-journey`, `F5` |
| Role / job workflow | `scenario` | `scenarios-*` per `scenarios-routing.md` |
| Product/platform page | `product` | `P1-P3` |
| Heavy SEO educational page | `topic` or `tool` | `T5` or `scenarios-blog` |

## Tools Composite-v2 Rules

- Formal source: `1-3 Content Gen/Page Gen/Pages/Tools/{lang}/{slug}-{lang}.json`.
- Languages: `en`, `zh`, `zh-TW`, `de`, `fr`, `it`, `ja`, `ko`, `pt`, `ru`.
- Required top-level fields: `slug`, `language`, `category`, `schemaVersion`, `storylineTemplate`, `title`, `description`, `bodyJson`, `seo`.
- `bodyJson` must be a stringified JSON array.
- Use `media.src`, not legacy `image_url`.
- No legacy `heroSection`, `contentSection`, `threeColumnSection`, `textImageSection`, `testimonialSection`, `faqSection` inside Tools v2.

## Scenarios Composite-v2 Rules

- Formal pilot source: `Pages/drafts/scenarios-storyline/Scenarios/en/`.
- `category: "scenario"` · **11** sections · `storylineId`: `scenarios-*`.
- SSOT: `scenarios-storylines.json` + `SCENARIOS-PRODUCTION.md`.
- Pilot: `draft-*` slug, `seo.noIndex: true`.
- Publish: `lovart-scenarios-sanity-publish` (`import --missing` only).

## Page Copy Gate

Every page must answer:

- Who is this for?
- What input does the user provide?
- What output do they get?
- What can they edit?
- What can they export or use commercially?
- Why trust this page?
- What should they do next?
