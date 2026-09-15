# Preflight Anti-Slop Gates (Skill Reference)

SSOT: `1-1 GEO Readme/文档/04-质量治理/Preflight-Anti-Slop-Gates.md`

## Quick commands

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"

node anti-slop-preflight.js --file path/to/article.md
node anti-slop-preflight.js --file path/to/tool-en.json --strict
node anti-slop-preflight.js --dir path/to/folder --glob "*.md" --report out.json
```

## When to run

| Stage | Tool |
|---|---|
| After Blog/Page draft (CREATE) | `anti-slop-preflight.js` |
| Before import (PRE-PUBLISH) | `preflight-content.js` + `anti-slop-preflight.js --strict` |
| Deep review | Content-Quality-Rubric + `lovart-content-audit` |

## New error codes

`AS_BANNED_PHRASE`, `AS_BANNED_DENSITY`, `AS_GENERIC_H2`, `AS_THIN_H2`, `AS_LOW_DENSITY_H2`, `AS_H2_COUNT`, `AS_SHRINKAGE`, `AS_HERO_IO`

## Implementation

- Rules: `../scripts/lib/anti-slop-rules.js`
- CLI: `../scripts/anti-slop-preflight.js`
- Merge target: `1-4 Dev/lovart.sanity.studio/scripts/preflight-content.js`
