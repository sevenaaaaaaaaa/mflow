---
name: lovart-blog-serp-writer
description: Lovart Blog 创作 skill。Use when writing, planning, outlining, researching, localizing, or rewriting Lovart blog posts, including How-To, Comparison, Insight, Lovart 101, Segment, Best Practice, Better Design, Case Study, Digest, Glossary, and SERP-driven SEO articles.
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# Lovart Blog SERP Writer

## Purpose

Create Lovart blog content that is better than generic AI writing: research-backed, SERP-aware, expert-positioned, human-readable, localized, and Sanity-ready.

This skill extends existing Blog workflows rather than replacing them. Use:

- `lovart-content-writer.md` for detailed content type and narrative rules.
- `lovart-blog-automation/SKILL.md` for research → planning → writing → publishing sequence.
- `lovart-content-quality-gates/SKILL.md` for preflight and audit.

## Required Inputs

Collect or infer:

- Focus keyword / topic.
- Target reader and funnel stage.
- Desired category or content type.
- Target language(s).
- Whether output is a research brief, outline, draft, rewrite, or QA.

If missing, pick a sensible default and state it.

## Phase 0: SERP Research Brief

Before writing, produce a brief:

- Query and search intent.
- Top 3-5 SERP pages or known competitor pages.
- Page types competing for the query.
- H2/FAQ gaps.
- What readers expect.
- Lovart-specific angle.
- Internal links and cluster opportunities.
- Evidence needed and claims to verify.

Read `../lovart-content-creation-orchestrator/references/serp-and-competitor-sources.md`.

## Blog Routing

Route through `../lovart-content-creation-orchestrator/references/blog-routing.md`.

Minimum route decision:

```text
Content type: [one of 12 writer types]
Blog category: [Sanity legal category]
Funnel: [TOFU | MOFU | BOFU | Post-Purchase]
Narrative framework: [one of 11 frameworks]
Target languages: [EN | EN+zh | EN+zh+ja | EN+zh+ja+zh-TW | etc.]
```

Do not default every article to How-To. If SERP is comparison-heavy, write comparison. If SERP is definition-heavy, write pillar/category education. If SERP is high-intent tool selection, write a decision guide.

## Writing Rules

### Structure

Every article must include:

- A non-generic opening hook.
- Clear reader promise.
- SERP-aware H2 structure.
- At least 3 concrete use cases or examples unless the format is glossary/digest.
- FAQ with 3-5 long-tail questions.
- E-E-A-T signals: experience, method, sources, limitations.
- Lovart angle: MCoT, ChatCanvas, Touch Edit, Brand Kit, Nano Banana only when relevant and verified.
- Internal links to verified slugs plus signup/pricing when appropriate.
- `image_briefs` in frontmatter; no visible image placeholders in body.

### Anti-Slop

Apply `1-1 GEO Readme/文档/04-质量治理/Anti-Slop.md` and Quality Gates:

- No "In today's fast-paced..." openings.
- No "Part 1 / Part 2" section headings.
- No fake data or unsupported comparisons.
- No generic "AI design tools are changing creativity" intros.
- Every H2 must add a judgment, mechanism, example, counterpoint, or action.

### Anti-Shrinkage

For long articles:

- Draft a section ledger before writing.
- Write in chunks when needed.
- Final third must be as specific as the first third.
- Every major H2 must satisfy at least 3 of: judgment, example, mechanism, reader insight, next action.

## Sanity Markdown Requirements

Follow `../lovart-blog-automation/references/writing-spec.md`:

- Required frontmatter.
- Sanity-legal category values.
- Kebab-case slug.
- SEO title and description.
- 5-8 keywords.
- 3-6 tags.
- `image_briefs`.
- No bad links: `/博客文章/`, `/cluster/`, `.md)`, `](#)`, `](/)`.

## Localization

For multilingual Blog work, read `../lovart-content-creation-orchestrator/references/i18n-localization.md`.

Rules:

- English is not automatically the best content shape for every market.
- Rewrite title, meta, hook, examples, FAQ, and CTA for local search intent.
- Blog common languages: `en`, `zh`, `ja`, `zh-TW`, with possible `pt`, `ru`.
- Do not create `es` unless explicitly authorized due to current language policy debt.

## Final QA

Before returning a draft, include a short checklist:

- SERP intent answered.
- Category and framework selected.
- Facts verified or marked `[待考证]`.
- FAQ covers real objections.
- Internal links are valid or marked for verification.
- Anti-slop and anti-shrinkage checked.
- i18n plan stated if multilingual.
