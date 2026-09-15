# Content Feedback Loop (Skill Reference)

SSOT: `1-1 GEO Readme/文档/04-质量治理/Content-Feedback-Loop.md`  
Register: `../feedback/register.json`

## After publish

Add entry when content goes live:

```bash
cd scripts
node feedback-loop-cli.js add \
  --id my-slug --type tool --lang en \
  --query "ai commercial generator" \
  --url "https://www.lovart.ai/tools/my-slug" \
  --score 86 --sample tool-en-gold-001
```

## Monthly review

```bash
node feedback-loop-cli.js import --csv ../feedback/gsc-import-example.csv
node feedback-loop-cli.js evaluate
node feedback-loop-cli.js report --month 2026-06 --out ../feedback/reviews/2026-06.md
```

## Signal → action quick ref

| Signal | Actions |
|---|---|
| SIG_CTR_LOW | ACT_REWRITE_HERO, ACT_DEMOTE_SAMPLE |
| SIG_RANK_STUCK | ACT_SERp_REFRESH |
| SIG_RANK_UP | ACT_PROMOTE_SAMPLE, ACT_LEDGER_DEFAULT |
| SIG_ORM_NEGATIVE | ACT_ADD_BAD_SAMPLE, ACT_BLOCK_PHRASE |

Full matrix in SSOT §3.
