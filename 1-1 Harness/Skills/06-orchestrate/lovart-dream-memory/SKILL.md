---
description: 梦境记忆 skill。夜间自动整理会话记忆并更新项目记忆。
---
# Dream: Memory Consolidation

> You are performing a dream — a reflective pass over your memory files.
> Synthesize what you've learned recently into durable, well-organized memories
> so that future sessions can orient quickly.

## Phase 1 — Orient

- Read `1-1 Harness/11-knowledge/MEMORY-PROJECT.md` (project facts)
- Read `~/.hermes/memories/MEMORY.md` (user preferences)
- Read `~/.hermes/memories/USER.md` (user profile)
- Check `1-1 Harness/11-knowledge/sessions/` for recent session logs
- Note what's already documented — improve, don't duplicate

## Phase 2 — Gather recent signal

- Scan `1-1 Harness/11-knowledge/sessions/` for un-processed logs (status != archived)
- For each unprocessed log: extract Patterns Observed + Decisions Made
- Cross-reference with `entities.yaml` and `relationships.yaml` for graph updates
- Check `1-3 GenFlow/.pipeline/events.jsonl` for pipeline activity
- Check `1-4 Dev/scripts/.archive/` for new archivals

## Phase 3 — Merge into MEMORY-PROJECT

- Add new § sections to `MEMORY-PROJECT.md` (§ number = highest existing + 1)
- Each entry must have a source tag: ⚙️ (dream-generated) / ✋ (user-corrected) / 📌 (hard rule)
- Update `version` field in frontmatter
- Bump `last_consolidated` date
- Do NOT remove existing entries — only add or mark stale with ~~strikethrough~~

## Phase 4 — Sync to Hermes MEMORY.md

- Run `bash 1-1 Harness/11-knowledge/scripts/sync-to-hermes-memory.sh` if it exists
- Or manually: extract project-specific facts from MEMORY-PROJECT.md
- Write to `~/.hermes/memories/MEMORY.md` under a `## [lovart]` heading
- Keep global MEMORY.md under 2200 chars — project facts are compressed references

## Phase 5 — Prune

- Mark entries older than 30 days with ~~strikethrough~~ (don't delete)
- Entries with 📌 tags are NEVER pruned
- Check for duplicates across MEMORY-PROJECT.md and MEMORY.md
- Merge duplicates, keep the more recent version

## Output

After consolidation, print:
```
[dream] processed N session logs
[dream] added M new entries to MEMORY-PROJECT.md
[dream] synced to Hermes MEMORY.md
[dream] pruned K stale entries
```

## Anti-patterns

- **Don't** create new files — everything goes into existing MEMORY-PROJECT.md
- **Don't** delete entries — only add or strikethrough
- **Don't** change existing entry content — only append new sections
- **Don't** modify `entities.yaml` or `relationships.yaml` directly — that's the graph layer
- **Don't** run this during normal sessions — only during dream cycles (cron/manual trigger)
