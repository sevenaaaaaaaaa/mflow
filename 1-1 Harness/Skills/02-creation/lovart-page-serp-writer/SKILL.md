---
name: lovart-page-serp-writer
description: Lovart 页面与落地页创作 skill。Use when writing, planning, rewriting, or generating Lovart Tools, Features, Product, Solution, Scenario, Topic, comparison pages, category education pages, SEO pages, or composite-v2 landing copy from SERP intent and Sanity storylines.
disable-model-invocation: true
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# Lovart Page SERP Writer

## Support-Only 入口约束

本 skill 只作为 `lovart-landing-page` 的内部写作支撑层，不直接响应用户请求。用户要求生成、重写、刷新、修复任何 Tools / Features / Product / Scenario / Solution / Topic / Landing Page 时，必须先进入 `lovart-landing-page` 父 skill，由父 skill 判断是否调用本 skill。

## Purpose

Generate Lovart page copy and page JSON that matches search intent, Sanity page type, Refresh-Page storylines, and anti-slop requirements.

This skill supports `lovart-landing-page`; it does not replace the parent landing-page skill, publishing, or import skills.

## Required Inputs

Collect or infer:

- Query / page topic / slug.
- Page category: `tool`, `feature`, `product`, `solution`, `scenario`, `topic`, or undecided landing page.
- Target language(s).
- Output mode: strategy brief, section copy, composite-v2 JSON, legacy copy, or rewrite.
- SERP competitors and user intent.

## 必读文案真源

开始写 copy 前，必须同时参考（结构与文案绑定同源存放在故事线里）：

- 机器绑定：`../../../../../1-3 GenFlow/Page Gen/Refresh-Page/landing-storylines.json` / `solution-storylines.json` / `scenarios-storylines.json` / `page-copy-bindings.json`
- 人类写作意图：`../lovart-landing-page/references/landing-copy-constraints-ssot.md`
- 立场：`../../../../../1-3 GenFlow/Page Gen/Refresh-Page/PAGE-BRIEF.md`
- 结构学习：`../../../../../1-2 Insight/Keywords Research/Landing Copy Benchmarks/README.md`

规则顺序：

1. `PAGE-BRIEF` 定页面立场
2. 读该故事线的 copy 绑定：intent / heroMust / requiredSections / proofTypes / ctaStyle / faqFocus / benchmarkPool
3. SSOT 解释绑定背后必须包含什么
4. benchmark 池定“这一类页的承诺结构像什么”

intent 以故事线为准（`page-copy-bindings.json` 的 `masterIntents` + `intentCrosswalk`）。若缺任何一项，不直接写 Hero。

## SERP Intent First

Before writing, classify query intent:

- Direct tool job: build a tool landing page.
- Broad category: build a hub/category education page.
- Comparison/alternative: build a comparison page.
- Technical quality problem: build education-first page.
- Marketing workflow: build tool + use-case page.
- Model name: build model comparison or routing explainer.
- Audience/persona: build persona section or use-case page.
- Utility feature: support a larger workflow unless Lovart has a strong standalone feature.

Read `../lovart-content-creation-orchestrator/references/serp-and-competitor-sources.md`.

## Page Routing

Read `../lovart-content-creation-orchestrator/references/page-routing.md`.

Sanity `compositePage` categories to support:

- `feature`
- `tool`
- `product`
- `solution`
- `scenario`
- `topic`

Tools default to composite-v2 and follow `../lovart-landing-page/tools-v2-template.md`.

## Storyline Selection

Use Refresh-Page storylines:

- Feature: `F1-F7`
- Tool: `T1-T5`, `T-long`
- Product: `P1-P3`
- Solution: `S1-S3`
- Scenario: `C1-C3`
- Topic: `K1-K2`
- Cross-category narrative: `N1-N6`

Examples:

- Standard tool: `T1`
- Single-purpose utility: `T2`
- Tool collection: `T3`
- Competitor comparison: `T4`
- SEO-heavy reading page: `T5`
- Existing production long page: `T-long`
- Agent full workflow: `F7`
- Industry vertical: `F5`, `S2`, or `S3`

## Copy Requirements

Every page must name:

- Buyer or audience.
- Input: prompt, product URL, image, script, brief, reference, brand kit.
- Output: logo, ad, commercial, brand video, product mockup, campaign set, export format.
- Edit path: ChatCanvas, Touch Edit, Text Edit, variations, review loop.
- Proof: example, workflow, output spec, testimonial, limitations, or verified metric.
- CTA: contextual and risk-aware.
- FAQ: at least 3 high-intent questions.

## Hero Formula

Hero must include at least 4 of these 5 dimensions:

- page subject
- buyer
- input
- output
- risk reducer

Bad Hero patterns:

- abstract AI slogan only
- product claim without user job
- output claim without edit path or proof

## Proof Rules

Weak proof alone is not enough. Logo walls and vague trust claims must be paired with at least one stronger proof:

- explicit deliverable
- workflow
- output format / rights
- before-after
- testimonial with use case
- limitation or trade-off

## FAQ Rules

FAQ should answer objections, not encyclopedia questions. Prioritize:

- commercial / rights
- export / format / input constraints
- editability and collaboration
- fit for team / industry / workflow
- difference from adjacent page types or competitor alternatives

## CTA Rules

CTA must match intent:

- trial/search: start free / try now / no credit card
- competitor: compare workflow / switch / see differences
- brand trust: explore / see examples / watch overview
- offer/retarget: claim / upgrade / unlock / start plan

Do not reuse the same CTA sentence across all page types.

## Page-Type Copy Emphasis

### `tool`

- Sell the specific job first
- Name input/output fast
- Keep platform explanation secondary

### `feature`

- Focus on one friction and the control after generation
- Show before/after or workflow change

### `product`

- Explain where the product sits in the larger Lovart stack
- Emphasize governance, collaboration, and long-term value

### `solution`

- Lead with team problem and workflow replacement
- Translate features into throughput / handoff / governance outcomes

### `scenario`

- Lead with role or industry pain
- Hero subject should be the scenario, not the product name

### `topic`

- Educate first
- Use decision framework, internal links, and fit guidance

### `landing`

- Match the storyline intent exactly
- Optimize for conversion moment, not content breadth

## Fact Sourcing

Use the `lovart-landing-page` source protocol:

- Product facts from Lovart docs/site/verified local knowledge.
- Pricing, integrations, model support, export formats must be verified.
- Unknown claims must be marked `[待考证]`.
- Do not invent social proof numbers.

## Tools Composite-v2 Output

If generating Tools JSON:

- One file per language.
- `category: "tool"`.
- `schemaVersion: "composite-v2"`.
- `storylineTemplate`: `T1-T5`, `N5`, or `T-long`.
- `bodyJson`: stringified JSON array.
- Use `media.src`, not legacy `image_url`.
- No legacy section types.
- Include `faq` and CTA.
- Batch languages in groups of up to 3.

## Localization

Read `../lovart-content-creation-orchestrator/references/i18n-localization.md`.

Pages support: `en`, `de`, `fr`, `it`, `ja`, `ko`, `pt`, `ru`, `zh-TW`, `zh`.

Each language must localize:

- Title and SEO description.
- Hero promise.
- CTA.
- FAQ.
- Examples and pain points.

## Quality Gates

Before final output:

- Check SERP intent alignment.
- Check story line and Sanity category.
- Check Hero covers subject + buyer + input/output + risk reducer.
- Check visible proof exists in body, not only logos.
- Check no generic AI copy.
- Check no unsupported claims.
- Check CTA matches traffic stage and page type.
- Check FAQ answers objections instead of weak definition questions.
- Check i18n file naming and language rules if generating JSON.
- Recommend `preflight-content.js --type tools --strict` for Tools.
- Recommend composite-v2 cross-language verification for multi-language pages.
- Recommend `COPY-PREFLIGHT.md` before final delivery.
