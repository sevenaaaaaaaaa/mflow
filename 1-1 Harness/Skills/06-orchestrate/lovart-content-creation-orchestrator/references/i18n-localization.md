# I18n and Localization Reference

Use this for multilingual Blog, Tools, Features, and compositePage content.

## Source Files

| Source | Purpose |
|---|---|
| `1-1 GEO Readme/文档/02-模块上手/i18n-多语言.md` | i18n workflow commands, principles, supported languages. |
| `1-4 Dev/lovart.sanity.studio/scripts/i18n-workflow.js` | Studio i18n workflow: prepare, apply, verify, publish. |
| `1-4 Dev/lovart.sanity.studio/scripts/lib/i18n-manifest.js` | EN SSOT slot manifest and target languages. |
| `1-4 Dev/lovart.sanity.studio/scripts/verify-composite-v2-crosslang.js` | Cross-language structure verification. |
| `1-1 Harness/Skills/lovart-content-quality-gates/SKILL.md` | L5 i18n checks and preflight. |
| `1-1 GEO Readme/文档/04-质量治理/Anti-Slop.md` | Language boundaries and anti-translation-slop rules. |

## Supported Languages

Pages / Tools / compositePage:

```text
en de fr it ja ko pt ru zh-TW zh
```

Blog common:

```text
en zh ja zh-TW
```

Blog extension when requested:

```text
pt ru
```

`es` is a special debt language: there is existing online Blog content, but new Blog/Tools/Features production should not default to `es` unless explicitly authorized.

## Localization Principles

- Multilingual work is rewriting, not sentence-by-sentence translation.
- Localize search intent, title, meta, hook, examples, FAQ, and CTA.
- Preserve Lovart brand terms consistently: MCoT, ChatCanvas, Touch Edit, Text Edit, Edit Elements, Brand Kit, Nano Banana.
- Avoid English sentence structure leaking into Japanese, Chinese structure leaking into English, or Simplified Chinese leaking into Traditional Chinese.
- If local SERP evidence is unavailable, state that the language version is strategy-derived and should be validated.

## File and Slug Rules

- JSON file name: `{slug}-{lang}.json`.
- JSON `slug` and `language` must match file name.
- Slug is kebab-case, no spaces, underscores, or leading/trailing `/`.
- Same slug across languages, different `_id`.
- Tools v2: one JSON file per language.

## Batch Rule for Tools

When generating 10 language files, output at most 3 languages per batch:

| Batch | Languages |
|---|---|
| 1 | `en`, `zh`, `zh-TW` |
| 2 | `ja`, `ko`, `de` |
| 3 | `fr`, `ru`, `pt` |
| 4 | `it` |

## Preflight Checks

Common checks:

- `I18N_LANG`
- `I18N_FILENAME`
- `I18N_MARKER`
- `I18N_GAP`
- `SEO_SLUG`
- `MD_LINK`
- `URL_PATH`
- `UX_*`

Useful commands:

```bash
cd "1-4 Dev/lovart.sanity.studio"
npm run i18n:prepare
npm run i18n:apply
npm run i18n:verify
npm run i18n:publish
npm run i18n:verify:crosslang
node scripts/preflight-content.js --type tools --lang en,ja,pt
node scripts/preflight-content.js --type blog-i18n
```

## Language Quality Gate

Before finalizing a localized draft:

- Title is locally natural and SEO-aware.
- Meta description is not a literal source-language translation.
- Examples fit the market.
- CTA matches local buyer hesitation.
- FAQ uses local query phrasing.
- No `(section_xx)` markers remain.
- Structure matches source when required.
