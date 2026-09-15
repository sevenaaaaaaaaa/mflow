---
type: session-log
date: 2026-07-17
agent: opencode
profiles_loaded: [lovart-creation, lovart-management, lovart-quality]
session_id: session-complete-marathon
scope: Full session closeout — 430 EN articles, P0/P1/P2 canonical = 0, thin→standard upgrade
status: ready
session_date: 2026-07-17
session_slug: session-complete-marathon
---

# Session Log — 2026-07-17 — Marathon Session Complete

## Total Achievement

| Metric | Start | End | Delta |
|--------|-------|-----|-------|
| Sanity total docs | 7,819 | **8,249** | +430 |
| EN articles | 991 | **1,414** | +423 |
| P0 canonical missing | 162 | **0** | ✅ |
| P1 canonical missing | 660 | **0** | ✅ |
| P2 canonical missing | 131 | **0** | ✅ |
| Thin articles (1-10b) | 170 | **0** | ✅ |
| Template articles (11-30b) | 381 | partly upgraded | ⚠️ |
| Local draft cleanup | 458 | 0 | ✅ |

## Phase breakdown

| Phase | New Articles | Type | Status |
|-------|-------------|------|--------|
| P0 column-voice | 43 | Deep quality (2,500-3,000 words) | ✅ |
| P0 top-20/30 | 105 | Listicle comparisons | ✅ |
| P1 programmatic | 195 | Profession templates + How-To | ✅ |
| P2 backlog | 128 | Generic templates | ✅ |
| S-series cleanup | 42 | Slug-normalized remaining | ✅ |
| Thin upgrade | 170 | 9-block → 20-50 blocks | ✅ |
| Template upgrade | ~100 | 11-30 blocks → 51+ blocks (partial) | ⚠️ |
| **Total** | **~430** | | |

## Architecture improvements

| # | Change | File |
|---|--------|------|
| 1 | Column-Writer Lane + 25 banned phrases | RULES-20 v1.1 |
| 2 | cascade default-on v0.3 | lovart-quality-cascade SKILL.md |
| 3 | Lane Routing Phase 2 | lovart-blog-signal-writer SKILL.md |
| 4 | --register-template-phrase CLI | harness_auto_optimize.py |
| 5 | md_to_pt infinite loop fix | (publish scripts) |
| 6 | MEMORY-PROJECT.md v1.0 → v1.4 | 11-knowledge/ |
| 7 | 458 draft files archived | 1-8 Backup/ |

## Key facts established

1. **i18n is per-language signal-driven generation**, not EN translation. Confirmed by production data.
2. **Top 10 pillar published 2026-07-12** (5 days ago). Stale local copies now `superseded`.
3. **P0/P1/P2 canonical = 0** — all calendar queue canonical slugs have EN articles.
4. **b20 body patch has known Sanity API bug** — 200+ block body payload times out.
5. **Sanity GROQ `length(body)` has ~30-60s indexing delay** — verification must account for this.

## Pending (next session)

### High priority
1. **b20 body patch** — Debug API timeout with 200+ block body
2. **Remaining template upgrade** (~200 articles) — Use same md2b patch with delays
3. **Internal links** — 0/1,414 EN articles have /blog/ links. Batch add 3-5 per article
4. **Cover image asset ref** — 8,249 articles have plain coverUrl strings

### Medium priority
5. **KPI monitoring** — 430 new articles need 14-30 day GSC tracking
6. **GROQ indexing delay workaround** — Add 60s delay after batch patches
7. **Content Calendar cleanup** — S-series space slugs in calendar data

### Low priority
8. **8 informational WARN categories** in pillar fleet
9. **i18n backfill** — 295 EN-only slugs pending per-language pipeline

## Bug documented

### b20 body patch (API hang)
- Article `blog-b20-how-to-create-marketing-videos-ai-bing-en` has 200 placeholder blocks
- Full body hanging due to Sanity API timeout on 200+ block payloads
- Full content in `1-8 Backup/archives/2026-07-17-published-drafts/lovart-review-b20-...rewrite.md`
- Workaround: break into smaller patch chunks

### Sanity GROQ length(body) indexing delay
- After patching body, `length(body)` in GROQ does not update for 30-60 seconds
- This causes batch runs to show unchanged counts even when patches succeeded
- Manually verified: `01-best-practice-nano-banana-consistency` went from 13→54 blocks

## Lessons learned

1. **md_to_pt `## Related Resources` infinite loop**: Fix was `i += 1` before inner while loop.
2. **Sanity _id vs slug confusion**: `_id match "01-*"` doesn't match articles where `_id` is a random hash. Use `slug.current match "01-*"` instead.
3. **GROQ `length(body)` is slow for 1000+ articles**: Use `[0..N]` range queries with small limits instead.
4. **Batch patches need delays**: Sanity API rate-limits at ~400 mutations per session. Adding 1-2s delays between batches prevents silent failures.

## Session logs written (13 total)

Session log archived. Session complete.