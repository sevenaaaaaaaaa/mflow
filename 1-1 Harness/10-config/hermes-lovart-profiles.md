# Hermes Lovart Profiles

> Last updated: 2026-07-02
> Purpose: keep Hermes Agent sessions small by loading only the skills needed for one Lovart work line.

## Commands

Install or refresh all Lovart profiles:

```bash
bash "1-4 Dev/automation/install-hermes-lovart-profiles.sh"
```

Start a profile:

```bash
hermes -p lovart-reports
hermes -p lovart-creation
hermes -p lovart-quality
hermes -p lovart-ops
hermes -p lovart-distribution
hermes -p lovart-management
```

Legacy aliases kept for cron compatibility:

```bash
hermes -p lovart-seo
hermes -p lovart-content
```

## Profile Map

| Profile | Model target | Use for | Main rules | Main skill set |
|---|---|---|---|---|
| `lovart-reports` | `deepseek-chat` | SEO reports, Sentinel, SERP, competitor intelligence, OKR analysis | `RULES-00`, `RULES-10` | `lovart-data-ingestion`, `lovart-trident-data-engine`, `lovart-sentinel*`, `lovart-seo-report*`, `lovart-seo-content-ops`, `lovart-seo-internal-linking` |
| `lovart-creation` | `deepseek-v4-pro` | Blog, Tool, Feature, Product, Solution, Scenario, Topic, Landing production | `RULES-00`, `RULES-20` | `lovart-content-calendar`, `lovart-content-creation-orchestrator`, `lovart-blog-*`, `lovart-page-serp-writer`, `lovart-landing-page`, `lovart-composite-page-design`, `lovart-refresh-page-generator`, `lovart-image-generation`, `lovart-i18n-pipeline` |
| `lovart-quality` | `deepseek-chat` | Anti-Slop, content QA, i18n QA, page health audits | `RULES-00`, `RULES-30` | `lovart-anti-slop`, `lovart-article-quality-template`, `lovart-content-audit`, `lovart-content-health-audit`, `lovart-content-quality-gates`, `lovart-landing-image-audit`, `lovart-sanity-preflight` |
| `lovart-ops` | `deepseek-chat` | Sitemap, IndexNow, Sanity operations, CRO/material operations | `RULES-00`, `RULES-40` | `lovart-sitemap-update`, `lovart-sanity-*`, `sanity-cms-*`, `lovart-seo-technical` |
| `lovart-distribution` | `deepseek-chat` | Domestic and overseas distribution, offsite drafts, platform adaptation | `RULES-00`, `RULES-50` | `lovart-content-distribution`, `lovart-multi-platform-push`, `ai-self-media-article`, `xurl`, `notion` |
| `lovart-management` | `deepseek-chat` | Project management, Hermes optimization, Kanban, knowledge architecture | `RULES-00`, `RULES-60` | `lovart-pipeline-orchestrator`, `lovart-content-creation-orchestrator`, `lovart-project-architecture`, `kanban-*`, `external-skills`, `hermes-agent` |

All profiles also get a tiny common set: `markdown-viewer`, `computer-use`, `obsidian`, and `lovart-project-architecture`.

## Operating Rules

- Use one profile for one work line. Do not mix reports, creation, publishing, and distribution in the same session.
- If the request belongs to another work line, the active profile should route the user to the right profile instead of loading unrelated skills.
- Re-run the installer after adding or renaming Lovart skills.
- The installer backs up the previous profile `skills/` folder under `~/.hermes/profile-skill-backups/`.
- Profile prompts are stored in each profile's `SOUL.md`; the source mapping is this document plus `install-hermes-lovart-profiles.sh`.
