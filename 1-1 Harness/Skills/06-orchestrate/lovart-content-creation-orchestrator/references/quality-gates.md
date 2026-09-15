# Content Creation Quality Gates

Use this before returning or publishing Blog Markdown, Tools JSON, Features JSON, compositePage content, or localized variants.

## Source Files

| Source | Purpose |
|---|---|
| `1-1 Harness/Skills/lovart-content-quality-gates/SKILL.md` | Preflight commands and lifecycle gates. |
| `1-1 Harness/Skills/lovart-content-audit/SKILL.md` | Blog deep audit for quality, compliance, culture, and brand consistency. |
| `1-1 GEO Readme/文档/04-质量治理/Anti-Slop.md` | Anti-slop writing standards. |
| `1-2 Insight/Keywords Research/SERP Copy Intelligence/global-en-serp-copy-research-2026-06.md` | SERP page patterns and anti-slop lessons. |
| `1-2 Insight/Keywords Research/SERP Copy Intelligence/global-en-competitor-landscape-2026-06.md` | Real competitors and competition dimensions. |

## Lifecycle

```text
CREATE → TRANSLATE → UPDATE → PRE-PUBLISH → POST-PUBLISH → DEEP QA
```

## SERP Alignment Gate

Before writing or publishing, verify:

- The first screen/opening answers the dominant query intent.
- The page or article uses the correct page type.
- Competitor strengths and gaps are known.
- Lovart has a defensible angle.
- FAQ covers top SERP objections.
- CTA responds to the user's likely hesitation.
- The content includes a concrete workflow, not only feature claims.

## Anti-Slop Gate

Reject or rewrite when:

- Copy uses generic phrases: "unlock", "revolutionize", "seamless", "AI-powered platform" without specifics.
- Content lacks a named reader or use case.
- CTA could appear on any SaaS page.
- H2 sections are summaries with no judgment, example, mechanism, or next action.
- Final third is thinner than the opening.
- Translated text reads like direct translation rather than localization.

## Fact Gate

Mark `[待考证]` when not verified:

- Pricing.
- Export formats.
- Model support.
- Integrations.
- Performance metrics.
- User count or adoption data.
- Competitor claims.
- Commercial rights.

## Automated Preflight

Common commands:

```bash
cd "1-4 Dev/lovart.sanity.studio"
node scripts/preflight-content.js --type tools --strict
node scripts/preflight-content.js --type features --lang en,ja
node scripts/preflight-content.js --type blog-md
node scripts/preflight-content.js --type blog-i18n
node scripts/preflight-content.js --ndjson ~/lovart/import-tools.ndjson
```

## BLOCK Conditions

- Invalid language or filename.
- Bad slug.
- Broken bodyJson.
- Legacy section type in composite-v2 Tools.
- Missing FAQ or CTA where required.
- Bad Blog links: `/博客文章/`, `/cluster/`, `.md)`, `](#)`, `](/)`.
- Visible image placeholders in Blog body.
- Translation markers left in output.

## Final Response Checklist

When returning generated content, include:

- Content route.
- SERP intent.
- Storyline or narrative framework.
- Sources used.
- `[待考证]` items, if any.
- Preflight command to run.
