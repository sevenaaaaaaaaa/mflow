#!/usr/bin/env python3
"""Loop preflight over all 19 retained pillar files; produce decision table."""
import subprocess
from pathlib import Path
import re

DRAFTS = Path("1-3 GenFlow/Lovart-Blog-Pipeline/01-Drafts")
NODE_SCRIPT = "1-1 Harness/Skills/03-review/lovart-content-quality-gates/scripts/anti-slop-preflight.js"

files = sorted(DRAFTS.glob("lovart-review-*-rewrite.md"))
print(f"Auditing {len(files)} files\n")

results = []
for f in files:
    proc = subprocess.run(
        ["node", NODE_SCRIPT, "--file", str(f), "--pro", "--skip-remote"],
        capture_output=True, text=True, cwd="."
    )
    out = proc.stdout.strip()
    # Parse meta
    status = "OK" if "[OK]" in out else "BLOCK"
    # Extract meta JSON
    meta_match = re.search(r'meta:\s*(\{[^}]+\})', out)
    meta = meta_match.group(1) if meta_match else "{}"

    # Extract issues
    issues_match = re.findall(r'(BLOCK|WARN) (\w+):\s*(.+?)(?=^\s*BLOCK|\s*WARN|\Z)', out, re.MULTILINE | re.DOTALL)
    issues = []
    for sev, code, msg in issues_match[:6]:
        msg = msg.strip().split('\n')[0][:120]
        issues.append(f"{sev} {code}")

    # Get word count
    text = f.read_text()
    wc = len(text.split())

    short = f.name.replace("lovart-review-", "").replace("-rewrite", "")
    print(f"{status:6s} | {wc:5d}w | {short[:55]:55s} | {'; '.join(issues)[:60]}")
    results.append((status, wc, short, issues, f.name))

# Summary
print(f"\n=== Summary ===")
ok = sum(1 for r in results if r[0] == "OK")
fail = sum(1 for r in results if r[0] == "FAIL")
print(f"OK (no BLOCK): {ok}")
print(f"FAIL (BLOCK > 0): {fail}")

# Categorize
print(f"\n=== Decisions ===")
print("\nDecision rule:")
print("- [OK] + no internal_links WARN → KEEP (already production-quality)")
print("- [OK] but WARNs (especially internal_links) → LIGHT POLISH (5-10 min fixes)")
print("- [FAIL] = BLOCK present → REFACTOR via multi-turn + column-writer Lane Deep (~45 min/file)")
print()
for status, wc, short, issues, fname in results:
    if status == "OK":
        if any("SEO_INTERNAL_LINKS" in i for i in issues):
            verdict = "LIGHT POLISH"
        elif any("PQ_PATCHWORK" in i for i in issues) and len(issues) <= 2:
            verdict = "KEEP (1-2 informational WARNs)"
        else:
            verdict = "KEEP"
    else:
        verdict = "REFACTOR"
    print(f"  {verdict:18s} | {fname}")

# Save decision table
import json
decision_path = Path("tmp/pillar-audit-decisions-2026-07-17.json")
decision_path.parent.mkdir(exist_ok=True)
decision_path.write_text(json.dumps([
    {
        "file": r[4],
        "status": r[0],
        "word_count": r[1],
        "issues": r[3],
        "decision": (
            "KEEP" if r[0] == "OK" and not any("SEO_INTERNAL_LINKS" in i for i in r[3]) else
            "LIGHT POLISH" if r[0] == "OK" else
            "REFACTOR"
        )
    } for r in results
], indent=2, ensure_ascii=False))
print(f"\nWrote decisions to {decision_path}")
