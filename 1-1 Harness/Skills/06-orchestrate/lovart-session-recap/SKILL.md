---
name: lovart-session-recap
description: |
  Quick session recovery when user returns after a break. Derived from
  Claude Code's away-summary-generation prompt. Produces a 40-word recap
  of goal + current task + next action. No markdown, no narrative.
source: https://github.com/Piebald-AI/claude-code-system-prompts
  (agent-prompt-away-summary-generation.md)
version: 1.0
---

# Session Recap Protocol

> When the user says "继续" / "what were we doing" / "recap" / returns after a break,
> produce this EXACT format. No preamble, no markdown, no greeting.

## Format

```
{overall goal in one clause}. Currently: {current task}. Next: {one concrete action}.
```

## Rules

- **Under 40 words total.** Hard limit.
- **No markdown formatting.** Plain text only.
- **No root-cause narrative.** Don't explain why things are the way they are.
- **No fix internals.** Don't describe what you fixed or how.
- **No secondary to-dos.** Only the ONE next action.
- **No em-dash tangents.** Stay on the main thread.
- **Lead with the goal.** The user needs to remember WHERE they were, not HOW.

## Example

```
Building Lovart content pipeline. Currently: validating governance check on 39 scripts. Next: write session log.
```

## Anti-patterns (DO NOT)

```
❌ "Welcome back! We were working on the tool governance system. We had just finished
    running the governance check on all 39 scripts and they all passed. We also fixed
    the G5 false positive issue. The next step is to write the session log and update
    MEMORY-PROJECT."
✅ "Building Lovart pipeline. Currently: 39/39 governance PASS. Next: session log."
```

```
❌ "## Recap\n\n- We created 3 new skills\n- We archived 2 profiles\n- We slimmed SOULs\n\n### Next steps\n1. Write session log\n2. Update MEMORY-PROJECT"
✅ "Lovart pipeline overhaul. Currently: all tests pass. Next: session log."
```
