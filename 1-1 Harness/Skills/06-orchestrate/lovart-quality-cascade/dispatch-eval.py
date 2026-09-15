#!/usr/bin/env python3
"""
dispatch-eval.py — dispatch evaluator (critic) agent of the cascade loop.

Reads <criteria.yaml> + draft text (from stdin) and produces a structured
quality-report json.

Backend selection via $LOVART_CASCADE_EVAL_BACKEND:
  mock      — pattern-based local evaluator (default; deterministic)
  hermes    — Hermes subprocess
  opencode  — OpenCode TBD

The mock backend is implemented here. Hermes backend delegates to hermes-agent
with profile lovart-quality and parses stdout as JSON.

Output: a JSON quality-report dict written to stdout (the orchestrate.py parent
writes it to disk as quality-report-vN.json).
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mock_eval(text: str, criteria_path: Path) -> dict:
    import yaml
    criteria = yaml.safe_load(criteria_path.read_text("utf-8"))
    block_hits = []
    warn_hits = []
    for rule in (criteria.get("block_if") or []):
        if rule.get("pattern"):
            hits = list(re.finditer(rule["pattern"], text, re.MULTILINE))
            if rule.get("threshold") and len(hits) >= rule["threshold"]:
                for hit in hits[:3]:
                    block_hits.append({
                        "rule_id": rule["id"],
                        "span": [hit.start(), hit.end()],
                        "matched": hit.group(0)[:80],
                    })
                if len(hits) > 3:
                    block_hits.append({
                        "rule_id": rule["id"],
                        "note": f"+{len(hits)-3} more matches truncated",
                    })
        if rule["id"] == "table-row":
            nlines = sum(1 for l in text.splitlines() if re.match(rule["pattern"], l))
            if nlines > rule["threshold"]:
                block_hits.append({
                    "rule_id": "table-row",
                    "note": f"{nlines} table rows > threshold {rule['threshold']}",
                })
    for rule in (criteria.get("warn_if") or []):
        warn_hits.append({
            "rule_id": rule["id"],
            "triggered": False,
            "note": "warn evaluator stub; details in v0.3",
        })
    BLOCK = len(block_hits) > 0
    import datetime
    return {
        "evaluator": "mock-pattern",
        "criteria_version": criteria.get("criteria_version", "0.1"),
        "BLOCK": BLOCK,
        "block_count": len(block_hits),
        "warn_count": len(warn_hits),
        "block_hits": block_hits,
        "warn_hits": warn_hits,
        "raw_chars": len(text),
        "raw_lines": len(text.splitlines()),
        "evaluated_at": datetime.datetime.now().isoformat(),
    }


def hermes_eval(text: str, criteria_path: Path, profile: str) -> dict:
    hermes_bin = os.environ.get("HERMES_BIN", str(Path.home() / ".hermes/bin/hermes-agent"))
    if not Path(hermes_bin).exists():
        raise RuntimeError(f"hermes eval backend: bin not found at {hermes_bin}")
    parts = [
        "# criteria",
        criteria_path.read_text("utf-8"),
        "# draft",
        text,
        "# directive: produce JSON quality-report matching schema {BLOCK:bool, block_count:int, block_hits:[{rule_id,span,matched}], warn_hits:[...]}. Read criteria.yaml and apply block_if rules. Do NOT rewrite.",
    ]
    prompt = "\n\n".join(parts)
    proc = subprocess.run([hermes_bin, "-p", profile, "evaluate", "--stdin"],
                          input=prompt, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(f"hermes eval failed: {proc.stderr[:200]}")
    return json.loads(proc.stdout)


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--criteria", required=True, help="path to criteria.yaml")
    p.add_argument("--critic-profile", default="lovart-quality")
    args = p.parse_args()

    text = sys.stdin.read()
    backend = os.environ.get("LOVART_CASCADE_EVAL_BACKEND", "mock")
    if backend == "mock":
        report = mock_eval(text, Path(args.criteria))
    elif backend == "hermes":
        report = hermes_eval(text, Path(args.criteria), args.critic_profile)
    elif backend == "opencode":
        sys.stderr.write("dispatch-eval.py: opencode backend not yet implemented (planned v0.3)\n")
        sys.exit(3)
    else:
        sys.stderr.write(f"dispatch-eval.py: unknown backend: {backend}\n")
        sys.exit(2)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
