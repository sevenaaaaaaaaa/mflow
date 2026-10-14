# Content Feedback Loop

SSOT: `harness/Docs/S4-质量审核/Content-Feedback-Loop.md`

Post-publish: register content → monthly GSC import → evaluate → update samples/preflight/ledger.

```bash
cd "harness/Skills/content-quality-gates/scripts"
node feedback-loop-cli.js list
```

Rewrite tasks must re-open Production Ledger, not patch from memory.
