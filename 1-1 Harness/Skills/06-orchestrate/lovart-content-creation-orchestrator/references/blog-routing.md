# Blog Routing Reference

Use this to choose the right Blog type before writing.

## Source Files

| Source | Purpose |
|---|---|
| `1-6 Knowledge Base/博客分类.md` | 8 strategy categories: Topics, Lovart101, How-To, Segment, Best Practice, Better Design, Insight&Trend, Lovart Digest. |
| `1-3 Content Gen/Content Calendar/` | Production calendar folders with 14 practical columns. |
| `1-1 Harness/Skills/lovart-content-writer.md` | 12 content types and 11 narrative frameworks. |
| `1-1 Harness/Skills/lovart-blog-automation/SKILL.md` | Phase 0 research and writing sequence. |
| `1-1 Harness/Skills/lovart-blog-automation/references/writing-spec.md` | Frontmatter, category mapping, word count, FAQ, image_briefs, links. |
| `1-1 Harness/Skills/lovart-content-quality-gates/SKILL.md` | Preflight and audit gates. |

## Unified Blog Route Table

| User Intent / SERP Shape | Writer Content Type | Sanity Category | Calendar Folder | Framework |
|---|---|---|---|---|
| Teach a task | Tutorial / How-To | `How-To` | `01-How-To` | The Journey / Field Guide |
| Compare tools | Comparison / Alternative | `How-To` | `02-Comparison` | The Duel |
| Explain an industry/persona | Segment Deep-Dive | `Industry Solution` | `03-Industry-Segment` | The Economist / Field Guide |
| Career/user story angle | Segment / Case Study | `Industry Solution` or `Customer Story` | `04-Career` | The Proof / Journey |
| Trend or thought leadership | Narrative / Insight | `Insight & Trend` | `05-Insight-Trend` | The Economist / Myth-Buster |
| Customer outcome | Case Study | `Customer Story` | `06-Case-Study` | The Proof |
| Seasonal campaign | How-To / Better Design | `How-To` or `Branding` | `07-Seasonal` | Field Guide |
| Product usage tip | Best Practice | `Best Practice` | `08-Best-Practice` | Field Guide / Cookbook |
| Design education | Better Design | `Branding` | `09-Better-Design` | Encyclopedia / Journey |
| Ethics/legal | Narrative / Glossary | `Insight & Trend` | `10-Ethics-Legal` | Economist |
| SEO cluster | Pillar / Cluster / Glossary | `Pillar` or `Cluster` | `11-Programmatic-SEO` | Encyclopedia |
| Weekly/monthly roundup | Lovart Digest | `News` or `Lovart Digest` if available | `12-Digest` | Curator |
| Onboarding | Lovart 101 / Best Practice | `Lovart 101` | `13-Onboarding` | Encyclopedia / Field Guide |
| Product update | News / Best Practice | `News` | `14-Product-Update` | Curator / Field Guide |

## Required Route Statement

Before writing, output:

```text
Content type:
Sanity category:
Calendar folder:
Funnel stage:
Narrative framework:
Focus keyword:
Target languages:
Because:
```

## Funnel Defaults

| Funnel | Typical Types |
|---|---|
| TOFU | Insight, Trend, Better Design, Glossary, Digest |
| MOFU | How-To, Tutorial, Segment, Pillar, Best Practice |
| BOFU | Comparison, Case Study, Alternative, Product Update |
| Post-Purchase | Best Practice, Digest, Onboarding |

## Minimum Quality Bar

- Comparison: fair verdict, scenario tests, limitations, no fanboy tone.
- How-To: concrete steps, finished output, screenshots/image briefs, FAQ.
- Insight: real thesis, evidence, counterpoint, implications.
- Segment: persona, job-to-be-done, industry examples, trust signals.
- Pillar/101: definition, category map, workflow, FAQ, internal links.
- Best Practice: one product problem, one practical fix, no bloated theory.

## Sanity Markdown Notes

- Use Sanity-legal category values.
- `Comparison`, `Better Design`, and `Segment` are writing types, not always legal category values.
- Use `image_briefs`; never place image placeholders in body.
- Verify internal links before final publishing.
