# Preflight Anti-Slop Gates

SSOT: `1-1 GEO Readme/文档/04-质量治理/Preflight-Anti-Slop-Gates.md`

After content draft, before returning to user:

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"
node anti-slop-preflight.js --file <draft> [--strict]
```

Pair with Ledger shrinkage check (manual) and Rubric scoring.

Codes: `AS_*` for anti-slop; existing `UX_*`, `MD_*`, `I18N_*` in studio preflight.
