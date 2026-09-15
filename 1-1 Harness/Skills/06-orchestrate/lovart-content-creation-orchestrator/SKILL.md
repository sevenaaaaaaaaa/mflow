---
name: lovart-content-creation-orchestrator
description: Lovart 内容创作总控 skill。Use when creating or planning Lovart blog posts, landing pages, Tools/Features/Solution/Scenario/Topic pages, SEO pages, comparison pages, multilingual content, or any content that should use SERP/competitor research, Anti-Slop, i18n, and Quality Gates before drafting.
---

# Lovart Content Creation Orchestrator

## Role

Route every Lovart content request through a research-backed workflow before writing. This skill does not replace existing Blog, Landing Page, Sanity publish, or Quality Gates skills; it decides which one to use and injects SERP intent, competitor evidence, anti-slop rules, localization, and verification requirements.

## Mandatory Workflow

### Step 0: Resolve state and routing (NEW 2026-07-20)

Before doing anything, determine the current state of the item and which profile/skill to use:

```bash
# 1) See what pipeline items exist and their stage
python3 $HARNESS_ROOT/Skills/06-orchestrate/lovart-pipeline-state/pipeline_state.py next

# 2) Ask router for the right profile and skill to use right now
python3 $HARNESS_ROOT/Skills/06-orchestrate/lovart-router/router.py decide
```

If `decide` says **reroute** to a different profile, **stop and tell the user** which profile to switch to. Do not continue in the wrong profile.

If `decide` says **execute_skill**, note the `skills_to_load` and proceed to Step 1.

If `decide` says **info_only**, answer the user's question using `pipeline_state.py get` and stop.

### 1. Classify the request

Identify the output type before drafting:

- Blog article / content calendar / research brief
- Tool landing page / Feature / Product / Solution / Scenario / Topic
- Comparison / alternative page
- Category education page
- SEO page / hub / programmatic long-tail page
- Multilingual rewrite / localization
- Quality review / rewrite only

If unclear, ask whether the user wants Blog, page JSON, strategy brief, or review.

### 2. Build a SERP + competitor brief

Before writing, create a short brief with:

- Focus query and intent cluster.
- SERP page type: tool landing, hub, comparison, category education, deep guide, utility support.
- Top competitor pages or internal observed samples.
- What competitors answer well.
- What competitors miss.
- Lovart's defensible angle.
- Required proof, FAQ, CTA, and internal links.

Use `references/serp-and-competitor-sources.md`.

### 3. Route to the specialist

- Blog: use `lovart-blog-signal-writer` (GSC/ORM signal-driven, higher quality standard).
- Page / landing / Tools / Features / compositePage: use `lovart-page-serp-writer`.
- Quality verification: use `lovart-content-quality-gates`.
- Publishing/import: use the existing Sanity publish skills.

### 4. Apply shared gates before output

All drafts must pass these gates:

- **Fact sourcing**: product claims, pricing, integrations, model support, export formats, and competitor claims must be verified or marked `[待考证]`.
- **Anti-slop**: no generic AI copy, no empty "unlock/revolutionize" language, no context-free CTA.
- **SERP alignment**: first screen or opening section must answer the dominant intent.
- **Workflow specificity**: name input, generation path, edit path, output, and next action where relevant.
- **i18n strategy**: language is rewritten for market intent, not translated sentence by sentence.
- **No shrinkage**: long content must preserve depth in the final third.

### 5. Use references only when needed

Keep this skill short. Read only the reference that matches the task:

- `references/serp-and-competitor-sources.md`
- `references/blog-routing.md`
- `references/page-routing.md`
- `references/i18n-localization.md`
- `references/quality-gates.md`

## Output Contract

For any creation task, start by stating:

```text
Content route: [Blog | Tool | Feature | Product | Solution | Scenario | Topic | Comparison | Category Education]
SERP intent: [tool | category | comparison | technical | model | audience | utility]
Primary skill: [lovart-blog-signal-writer | lovart-page-serp-writer]
Required checks: SERP brief / fact sourcing / Anti-slop / i18n / Quality Gates
```

Then produce either the brief, outline, Markdown draft, or page JSON requested by the user.
