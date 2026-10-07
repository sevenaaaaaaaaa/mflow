# Composite v2 Draft Pages — Local A/B Storylines

> Generated: 2026-05-31  
> **Status: synced to Sanity production — 15 docs, `--missing` only (2026-05-29).**  
> `seo.noIndex: true` on all drafts. Slugs prefixed with `draft-` — **did not overwrite** `788-en`, `293-en`, `849-en`, etc.

## Sync record

| Item | Value |
|------|-------|
| NDJSON | `~/lovart/import-composite-v2-drafts.ndjson` |
| Report | `~/lovart/import-composite-v2-drafts-report.json` |
| Dataset | `production` / `o11tm2qe` |
| Imported | **15** new documents |
| Mode | `--missing` only (non-destructive) |

**英文测试 URL 清单（无 `/en/`）**：[`TEST-URLS-en.md`](./TEST-URLS-en.md)

## Themes

| Theme | Features variants | Tools variants |
|-------|-------------------|----------------|
| **AI Logo Maker** | F1, F2, F4, F5, F6 | T1, T2, T4 |
| **AI Sales Deck PPT Generator** | F1, F2, F7, S1 | T1, T2, N5 |

## How to preview

1. Copy `bodyJson` into frontend preview fixture, or import via `import-page.js --dry-run`
2. Run preflight: `node scripts/preflight-content.js --type composite-v2 --dir "../Pages/drafts/composite-v2/Features/en"`

## Variant index

| # | Theme | Type | Storyline | Slug | Section flow |
|---|-------|------|-----------|------|--------------|
| 1 | ai-logo-maker | feature | F1 | `draft-ai-logo-maker-f1` | prompt-launcher → workflow-horizontal → feature-grid → testimonial → faq → cta-default |
| 2 | ai-logo-maker | feature | F2 | `draft-ai-logo-maker-f2` | hero-cinematic → prompt-launcher → capability-tabs → comparison-table → faq → cta-default |
| 3 | ai-logo-maker | feature | F4 | `draft-ai-logo-maker-f4` | hero-split → comparison-before-after → feature-detail → canvas-wall → faq → cta-default |
| 4 | ai-logo-maker | feature | F5 | `draft-ai-logo-maker-f5` | hero-journey → portrait-grid-3 → showcase-stacked → review-grid-3col → faq → cta-default |
| 5 | ai-logo-maker | feature | F6 | `draft-ai-logo-maker-f6` | hero-gallery → tool-grid → proof-block → faq → cta-default |
| 6 | ai-logo-maker | tool | T1 | `draft-ai-logo-maker-t1` | prompt-launcher → bento-2 → workflow-horizontal → feature-detail → testimonial → faq → cta-default |
| 7 | ai-logo-maker | tool | T2 | `draft-ai-logo-maker-t2` | hero-split → comparison-before-after → workflow-horizontal → faq → cta-default |
| 8 | ai-logo-maker | tool | T4 | `draft-ai-logo-maker-t4` | hero-split → comparison-table → proof-block → review-grid-4col → faq → cta-default |
| 9 | ai-sales-deck-ppt-generator | feature | F1 | `draft-ai-sales-deck-ppt-generator-f1` | prompt-launcher → workflow-horizontal → feature-grid → testimonial → faq → cta-default |
| 10 | ai-sales-deck-ppt-generator | feature | F2 | `draft-ai-sales-deck-ppt-generator-f2` | hero-cinematic → prompt-launcher → capability-tabs → comparison-table → faq → cta-default |
| 11 | ai-sales-deck-ppt-generator | feature | F7 | `draft-ai-sales-deck-ppt-generator-f7` | hero-journey → feature-detail → workflow-vertical → stats → faq → cta-default |
| 12 | ai-sales-deck-ppt-generator | feature | S1 | `draft-ai-sales-deck-ppt-generator-s1` | hero-cinematic → proof-block → comparison-table → workflow-vertical → review-grid-3col → faq → cta-default |
| 13 | ai-sales-deck-ppt-generator | tool | T1 | `draft-ai-sales-deck-ppt-generator-t1` | prompt-launcher → bento-2 → workflow-horizontal → feature-detail → testimonial → faq → cta-default |
| 14 | ai-sales-deck-ppt-generator | tool | T2 | `draft-ai-sales-deck-ppt-generator-t2` | hero-split → comparison-before-after → workflow-horizontal → faq → cta-default |
| 15 | ai-sales-deck-ppt-generator | tool | N5 | `draft-ai-sales-deck-ppt-generator-n5` | hero-split → pricing-block → comparison-table → faq → cta-default |

## Notes per variant

### draft-ai-logo-maker-f1
- **Storyline:** F1
- **Intent:** Trial → workflow → feature grid → testimonial → FAQ. Baseline conversion path for logo generation.

### draft-ai-logo-maker-f2
- **Storyline:** F2
- **Intent:** Cinematic hero + capability tabs + comparison table. For premium / agency alternative positioning.

### draft-ai-logo-maker-f4
- **Storyline:** F4
- **Intent:** Before/after + canvas wall. For rebrand and template-escape narrative.

### draft-ai-logo-maker-f5
- **Storyline:** F5
- **Intent:** Hero journey + portrait grid + showcase. Full launch identity story.

### draft-ai-logo-maker-f6
- **Storyline:** F6
- **Intent:** Hero gallery + tool grid + proof. Ecosystem / multi-entry positioning.

### draft-ai-logo-maker-t1
- **Storyline:** T1
- **Intent:** Classic tool page: launcher → bento → workflow → detail → social proof.

### draft-ai-logo-maker-t2
- **Storyline:** T2
- **Intent:** Short path: hero → before/after → workflow. Fast intent capture.

### draft-ai-logo-maker-t4
- **Storyline:** T4
- **Intent:** Comparison table + reviews. Decision-stage traffic.

### draft-ai-sales-deck-ppt-generator-f1
- **Storyline:** F1
- **Intent:** Baseline sales deck feature page with full capability grid.

### draft-ai-sales-deck-ppt-generator-f2
- **Storyline:** F2
- **Intent:** Premium sales enablement with tabs and comparison.

### draft-ai-sales-deck-ppt-generator-f7
- **Storyline:** F7
- **Intent:** Journey + vertical workflow + stats. End-to-end RevOps narrative.

### draft-ai-sales-deck-ppt-generator-s1
- **Storyline:** S1
- **Intent:** Enterprise rollout playbook for revenue teams.

### draft-ai-sales-deck-ppt-generator-t1
- **Storyline:** T1
- **Intent:** Tool landing for deck generation keyword intent.

### draft-ai-sales-deck-ppt-generator-t2
- **Storyline:** T2
- **Intent:** Minimal tool path for high-intent searches.

### draft-ai-sales-deck-ppt-generator-n5
- **Storyline:** N5
- **Intent:** Pricing block + comparison for bottom-funnel.


## If you pick a winner for production

1. Choose slug (e.g. keep `ai-logo-maker` or new SEO slug)
2. Remove `draft-` prefix, `draftStatus`, set `seo.noIndex: false`
3. Preflight → `import-page.js --dry-run` → user confirms import
