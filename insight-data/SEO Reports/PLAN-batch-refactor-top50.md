# Batch Refactoring Plan — TOP 50 Blog Posts by GSC Impressions

> **Status**: PLANNING
> **Created**: 2026-07-06
> **Target**: 50 blog posts from 改造建议/ directory, ranked by GSC impressions

---

## Executive Summary

Batch refactor50 blog posts according to their refactoring plans in `/Output/SEO-Reports/改造建议/`. Each post will be rewritten to ≥7500 words, converted to Portable Text, and patched to Sanity production.

---

## TOP 50 Posts by GSC Impressions

| Rank | Impressions | Slug |
|------|-------------|------|
| 1 | 1943 | lovart-worlds-first-professional-ai-design-agent |
| 2 | 1926 | dreamina-ai-review |
| 3 | 1396 | the-best-ai-design-agent-for-beginners |
| 4 | 1025 | lovart-nano-banana-2-ai-design-agent |
| 5 | 1000 | imagefx-review |
| 6 | 986 | wan-2.1-ai-review |
| 7 | 941 | complete-guide-object-removal-inpainting-ai |
| 8 | 880 | ai-animal-pet-generators-compared |
| 9 | 848 | best-agent-for-sbos |
| 10 | 829 | best-ai-design-tools-in-2025-complete-comparison-guide-for-creators-and-marketers |
| 11 | 794 | ai-video-models-compared-2026 |
| 12 | 793 | ai-design-tools-2025 |
| 13 | 782 | amazon-requirements-ai-white-background-images |
| 14 | 766 | lovart-ai-image-generator-create-stunning-images-with-ai |
| 15 | 715 | responsible-ai-design-lovart |
| 16 | 694 | complete-guide-ai-art-platform-selection-2026 |
| 17 | 684 | complete-guide-ai-video-model-selection-2026 |
| 18 | 662 | capcut-ai-review |
| 19 | 656 | ai-design-global-adoption-trends-2026 |
| 20 | 645 | ai-image-models-compared-2026 |
| 21 | 625 | best-haiper-ai-alternatives-in-2025-video-generation-compared |
| 22 | 591 | law-firm-branding-trust-authority-design-2027 |
| 23 | 587 | video-generators-review |
| 24 | 547 | hailuo-ai-review-2025-cinematic-video-generation-tested-hands-on |
| 25 | 524 | haiper-ai-review-2025-features-pricing-and-real-world-performance-test |
| 26 | 522 | ultimate-guide-ai-design-agent-canvas-for-creators-business |
| 27 | 520 | loveart-ai-business-creative-workflows |
| 28 | 510 | step-by-step-ai-design-replace-photoshop-25-types |
| 29 | 457 | 02-wiki-batch-generation-best-practices |
| 30 | 451 | freepik-ai-image-generator-review |
| 31 | 441 | vidu-ai-review-2025-ai-video-generation-platform-features-and-verdict |
| 32 | 435 | ai-powered-design-agent-for-creators |
| 33 | 433 | small-business-design-tools-compared |
| 34 | 429 | the-best-ai-agent-driven-canvas-for-digital-nomads-with-lovart-all-in-one-design-agent |
| 35 | 419 | ai-floor-plan-tools-compared |
| 36 | 418 | ai-commercial-license-country-comparison-2026 |
| 37 | 413 | content-refresh-ai-design-tool-reviews-2027 |
| 38 | 378 | shutterstock-ai-review |
| 39 | 377 | adobe-firefly-review-2025-features-pricing-and-honest-hands-on-test |
| 40 | 365 | lovart-account-enforcement |
| 41 | 357 | best-ai-design-agent-for-e-book-author |
| 42 | 347 | how-to-chat-generate-any-design-type-lovart-agent |
| 43 | 343 | complete-guide-ai-background-wallpaper-pattern-design |
| 44 | 342 | imagineart-review |
| 45 | 342 | midjourney-character-reference-vs-lovart-nano-banana-consistency-test |
| 46 | 326 | ai-design-freelance-pricing-guide-2026 |
| 47 | 325 | ai-design-contracts-freelancers-agencies-should-include |
| 48 | 323 | seedance-2-orchestration-lovart-ai-agent |
| 49 | 314 | figma-vs-ai-design-agents |
| 50 | 304 | capcut-ai-review-2025-features-pros-cons-and-honest-verdict |

---

## Architecture

### Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    BATCH REFACTORING PIPELINE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Phase 1:     │    │ Phase 2:     │    │ Phase 3:     │       │
│  │ Data Pull    │───▶│ Content Gen  │───▶│ Publishing   │       │
│  │              │    │              │    │              │       │
│  │ • GROQ query │    │ • LLM rewrite│    │ • MD → PT    │       │
│  │ • Save local │    │ • 7500+ words│    │ • Patch      │       │
│  │ • Match plans│    │ • Quality    │    │ • Verify     │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 1: Data Collection

**Script**: `pull-existing-blogs.py`

```python
# GROQ query to pull existing blog posts
*[_type == "blog" && seo.noIndex != true && !(_id in path("drafts.**"))]{
    _id,
    title,
    "slug": slug.current,
    body,
    language,
    "cover": cover.url,
    description,
    seo,
    _updatedAt
}
```

**Output**: `/Output/SEO-Reports/Refactoring/01-existing/{slug}.json`

### Phase 2: Content Generation

**Script**: `refactor-blog-post.py`

For each post:
1. Read existing content from Phase 1 output
2. Read refactoring plan from `改造建议/{slug}.md`
3. Extract:
   - Frontmatter rewrite (title, description)
   - H1/H2 optimization
   - Long-tail content (150-300 words)
   - FAQ (2-3 Q&As)
   - Internal links
4. Generate new content using LLM (DeepSeek V4 Pro)
5. Ensure ≥7500 words
6. Quality check (anti-slop, brand terms)

**Output**: `/Output/SEO-Reports/Refactoring/02-rewritten/{slug}.md`

### Phase 3: Publishing

**Script**: `patch-to-sanity.py`

1. Convert MD → Portable Text (using convert.js logic)
2. Create Sanity patch document
3. Execute `sanity dataset import --missing`
4. Verify: `length(pt::text(body)) ≥ 7500`

**Output**: `/Output/SEO-Reports/Refactoring/03-patched/{slug}.json`

---

## Key Components

### 1. Sanity Configuration

```python
SANITY_CONFIG = os.path.expanduser("~/.config/sanity/config.json")
PROJECT_ID = "o11tm2qe"
DATASET = "production"
API_VERSION = "v2024-01-01"
```

### 2. LLM Configuration

```python
# MiniMax M3 for content generation (Anthropic-compatible)
LLM_PROVIDER = "minimax-anthropic"
LLM_MODEL = "MiniMax-M3"
LLM_ENDPOINT = "https://api.minimaxi.com/anthropic"
LLM_CONTEXT = 200000
LLM_OUTPUT = 65536
MIN_WORDS = 7500
```

**⚠️ API Key Required**: Minimax API key not found in config. User must provide:
- `MINIMAX_API_KEY` environment variable, or
- Store in `~/.config/minimax/credentials.json`

### 3. Quality Gates

```python
QUALITY_CHECKS = [
    "word_count >= 7500",
    "no_slop_words",  # No "stands as", "testament", etc.
    "brand_terms_used",  # MCoT, ChatCanvas, Touch Edit, etc.
    "faq_count >= 2",
    "internal_links >= 3",
    "h2_density >= 1 per 500 words",
]
```

### 4. Portable Text Conversion

Based on archived `convert.js`:
```javascript
function htmlToPortableText(html) {
    // Convert HTML to Portable Text blocks
    // Supports: h1-h6, p, ul, ol, blockquote, pre, table, img
}
```

---

## Execution Plan

### Batch Processing Strategy

- **Batch size**: 10 posts per run
- **Parallel**: 3 LLM calls concurrently
- **Estimated time**: ~30 minutes per batch (5 batches total = 2.5 hours)
- **Token usage**: ~375K words × ~1.3 tokens/word = ~487K tokens

### Step-by-Step Execution

```bash
# Step 1: Pull existing posts from Sanity
python3 scripts/pull-existing-blogs.py --slugs-file top50-slugs.txt

# Step 2: Generate rewritten content (batch of 10)
python3 scripts/refactor-blog-post.py --batch 1 --size 10

# Step 3: Quality check
python3 scripts/quality-check.py --batch 1

# Step 4: Patch to Sanity
python3 scripts/patch-to-sanity.py --batch 1 --dry-run
python3 scripts/patch-to-sanity.py --batch 1

# Step 5: Verify
python3 scripts/verify-word-count.py --batch 1

# Repeat for batches 2-5
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| LLM rate limits | Implement exponential backoff, batch size reduction |
| Word count < 7500 | Auto-expand with additional sections |
| Sanity patch failures | Dry-run first, retry with backoff |
| Quality issues | Pre-publish quality gate, manual review for batch 1 |
| Token cost | Monitor usage, optimize prompts |

---

## Success Criteria

- [ ] 50 posts rewritten to ≥7500 words each
- [ ] All posts patched to Sanity production
- [ ] 0 patch failures
- [ ] Quality gates passed (no slop, brand terms, FAQ, internal links)
- [ ] Word count verification: `length(pt::text(body)) ≥ 7500` for all 50 posts

---

## Next Steps

1. **Approve plan**: User confirms architecture
2. **Create scripts**: Implement `pull-existing-blogs.py`, `refactor-blog-post.py`, `patch-to-sanity.py`
3. **Test batch 1**: Run first batch of 10 posts
4. **Review output**: Manual quality check on batch 1
5. **Scale to50**: Execute remaining batches
