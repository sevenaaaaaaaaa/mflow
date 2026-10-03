# Lovart Blog Writing Specification

## Frontmatter Requirements

Every draft in `01-Drafts/` **must** include these YAML fields:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title` | string | ✅ | ≤70 chars, lead with target keyword |
| `slug` | string | ✅ | lowercase, hyphens only, matches URL |
| `date` | string | ✅ | `YYYY-MM-DD` planned publish date |
| `language` | string | ✅ | always `en` |
| `category` | string | ✅ | must be Sanity-legal: `How-To`, `Best Practice`, `Branding`, `Insight & Trend`, `Lovart 101`, `Industry Solution` |
| `author` | string | ✅ | `Lovart Content Team` |
| `description` | string | ✅ | ≤300 chars, list page excerpt |
| `keywords` | list | ✅ | 5-8 SEO keywords |
| `tags` | list | ✅ | 3-6 topic tags |
| `cover_url` | url | ✅ | from pool, stable hash |
| `alt_text` | string | ✅ | `{focus_keyword} — Lovart AI Design Agent blog cover` |
| `seo_title` | string | | ≤60 chars |
| `seo_description` | string | | 150-160 chars |
| `status` | string | | `draft` / `publish` |
| `content_cluster` | string | | cluster name for internal linking |
| `difficulty` | string | | `beginner` / `intermediate` / `advanced` |
| `tool` | string | | comma-separated Lovart features |
| `focus_keyword` | string | | primary keyword |
| `seo_schema` | string | | `Article` / `FAQ` / `HowTo` |
| `estimated_read` | string | | e.g. `12 min` |
| `page_type` | string | | `Blog Post` |
| `image_briefs` | list | | slots 1–4 production notes (not in body) |

## Category Mapping

Frontmatter `category` must use Sanity-legal names. Map writing types to categories:

| Writing Type | Sanity `category` |
|-------------|-------------------|
| Comparison | `How-To` |
| Lovart 101 | `Lovart 101` |
| How-To | `How-To` |
| Best Practice | `Best Practice` |
| Segment | `Industry Solution` |
| Better Design | `Branding` |
| Insight & Trend | `Insight & Trend` |

**Never** write `Comparison`, `Better Design`, or `Segment` as category values.

## Sanity-Legal Categories (complete list)

`AI Image Tools`, `AI Video Tools`, `Best Practice`, `Branding`, `How-To`, `Insight & Trend`, `Lovart 101`, `Industry Solution`, `Customer Story`, `News`, `Pillar`, `Cluster`

## Word Count Targets

**Universal floor (2026-07-17):** every article type / Sanity category must reach **≥7,500 English words** before `status: ready`. Old per-type ladders (Comparison 3600 / 101 4500 / How-To 1800 / Best Practice 1800 / Segment 2800) are **abolished**.

| Article Type | Minimum |
|-------------|---------|
| All types (Comparison, 101, How-To, Best Practice, Segment, Insight, Review, Complete Guide, …) | **7500** |

Write via multi-turn (RULES-20); do not pad with template sentences to hit the floor.

## Content Structure

All articles must include:

1. **H2 intro hook** — problem statement, pain point, or clickbait-adjacent opening
2. **Derivative Scenarios** — at least 3 use cases with concrete examples
3. **FAQ section** — 3-5 Q&A pairs targeting long-tail keywords
4. **E-E-A-T signals** — mention MCoT, ChatCanvas, Touch Edit, Nano Banana where relevant
5. **Internal links** — only to verified slugs + `[Lovart signup](https://lovart.ai/signup)` + `[pricing](https://lovart.ai/pricing)`
6. **Image briefs** — `image_briefs:` in frontmatter (slots 1–4); **never** `[IMAGE N PLACEHOLDER]` in body
7. **Footer cluster links** — 3-4 related article links from same content cluster

## Brand Terminology

Use these terms consistently:
- **MCoT** (Mind Chain of Thought) — Lovart's reasoning engine
- **ChatCanvas** — the chat-to-canvas interface
- **Touch Edit** — gesture-based editing
- **Edit Elements** — semantic layer decomposition
- **Nano Banana** / **Nano Banana Pro** — model series
- **Brand Kit** — the brand identity system
- **Design Agent** — the AI agent concept

## Cover Image Allocation

Pool: `1-Project/1-6 Knowledge Base/Cover Url 随机调取.md` (56+ unique URLs). `scripts/pick-cover.py` defaults to this current pool.

```bash
python3 scripts/pick-cover.py <slug>
```

Stable hash ensures same slug → same cover every time. If collision with another article, manually set a different value.

## Verified Internal Links

Only link to slugs that exist on the live site. Verify with:
```bash
curl -sI "https://blogs.lovart.ai/{slug}" | head -1
```

## Feishu Document Sync (optional)

Feishu wiki integration is `blocked-by-missing-source` after the 2026-06 reorg. Current Feishu-related scripts are Trident report push helpers, not Blog wiki sync:

- `1-4 Dev/scripts/trident/push_to_feishu.py`
- `1-1 Harness/Skills/lovart-trident-data-engine/scripts/push_to_feishu.py`

Do not treat `1-Project/Wordpress/Feishu-Knowledge-Base/` as an active path until a new owner and source are confirmed.
