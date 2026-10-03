# Hermes the brand Profiles

> Last updated: 2026-07-02
> Purpose: keep Hermes Agent sessions small by loading only the skills needed for one the brand work line.

## Commands

Install or refresh all the brand profiles:

```bash
bash "1-4 Dev/automation/install-hermes-profiles.sh"
```

Start a profile:

```bash
hermes -p mflow-reports
hermes -p mflow-creation
hermes -p mflow-quality
hermes -p mflow-ops
hermes -p mflow-distribution
hermes -p mflow-management
```

Legacy aliases kept for cron compatibility:

```bash
hermes -p mflow-seo
hermes -p mflow-content
```

## Profile Map

| Profile | Model target | Use for | Main rules | Main skill set |
|---|---|---|---|---|
| `mflow-reports` | `deepseek-chat` | SEO reports, Sentinel, SERP, competitor intelligence, OKR analysis | `RULES-00`, `RULES-10` | `data-ingestion`, `trident-data-engine`, `mflow-sentinel*`, `mflow-seo-report*`, `mflow-seo-content-ops`, `mflow-seo-internal-linking` |
| `mflow-creation` | `deepseek-v4-pro` | Blog, Tool, Feature, Product, Solution, Scenario, Topic, Landing production | `RULES-00`, `RULES-20` | `content-calendar`, `content-creation-orchestrator`, `mflow-blog-*`, `landing-writer`, `mflow-composite-page-design`, `mflow-refresh-page-generator`, `image-generation`, `mflow-i18n-pipeline` |
| `mflow-quality` | `deepseek-chat` | Anti-Slop, content QA, i18n QA, page health audits | `RULES-00`, `RULES-30` | `mflow-anti-slop`, `mflow-article-quality-template`, `content-audit`, `mflow-content-health-audit`, `content-quality-gates`, `mflow-landing-image-audit`, `sanity-preflight` |
| `mflow-ops` | `deepseek-chat` | Sitemap, IndexNow, Sanity operations, CRO/material operations | `RULES-00`, `RULES-40` | `sitemap-update`, `mflow-sanity-*`, `sanity-cms-*`, `mflow-seo-technical` |
| `mflow-distribution` | `deepseek-chat` | Domestic and overseas distribution, offsite drafts, platform adaptation | `RULES-00`, `RULES-50` | `content-distribution`, `multi-platform-push`, `ai-self-media-article`, `xurl`, `notion` |
| `mflow-management` | `deepseek-chat` | Project management, Hermes optimization, Kanban, knowledge architecture | `RULES-00`, `RULES-60` | `pipeline-orchestrator`, `content-creation-orchestrator`, `mflow-project-architecture`, `kanban-*`, `external-skills`, `hermes-agent` |

All profiles also get a tiny common set: `markdown-viewer`, `computer-use`, `obsidian`, and `mflow-project-architecture`.

## Operating Rules

- Use one profile for one work line. Do not mix reports, creation, publishing, and distribution in the same session.
- If the request belongs to another work line, the active profile should route the user to the right profile instead of loading unrelated skills.
- Re-run the installer after adding or renaming the brand skills.
- The installer backs up the previous profile `skills/` folder under `~/.hermes/profile-skill-backups/`.
- Profile prompts are stored in each profile's `SOUL.md`; the source mapping is this document plus `install-hermes-profiles.sh`.
