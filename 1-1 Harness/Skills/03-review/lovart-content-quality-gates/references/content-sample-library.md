# Content Sample Library (Skill Reference)

SSOT: `1-1 GEO Readme/文档/04-质量治理/Content-Sample-Library.md`  
Samples: `../samples/` · Index: `../samples/index.json`

## CLI

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"
node sample-library-cli.js list
node sample-library-cli.js pair blog
node sample-library-cli.js show tool-en-gold-001
node sample-library-cli.js calibrate
```

## Before writing

1. `pair <content_type>` — load gold + bad anchors.
2. Copy `reusable_pattern` into Production Ledger.
3. After draft: `anti-slop-preflight.js --strict` + compare to bad sample codes.

## Defaults

| Type | Gold/Good | Bad |
|---|---|---|
| blog | blog-en-good-001 | blog-en-bad-001 |
| tool | tool-en-gold-001 | tool-en-bad-001 |
| comparison | comparison-en-good-001 | comparison-en-bad-001 |
| i18n | — | i18n-ja-bad-001 |
