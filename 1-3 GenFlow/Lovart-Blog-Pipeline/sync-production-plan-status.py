#!/usr/bin/env python3
"""Update PRODUCTION-PLAN.md status from 01-Drafts word counts."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "PRODUCTION-PLAN.md"
DRAFTS = ROOT / "01-Drafts"

MIN_WORDS = {
    "comparison-": 3600,
    "lovart-101-": 4500,
    "how-to-": 1800,
    "better-design-": 2500,  # target 3000; accept 2500+ after expansion passes
    "insight-": 2500,
    "segment-": 2000,
}


def min_for_file(fn: str) -> int:
    for prefix, m in MIN_WORDS.items():
        if fn.startswith(prefix):
            return m
    return 1800


def main():
    lines = PLAN.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        m = re.match(r"^\| (\d+) \|", line)
        if not m or "`" not in line:
            out.append(line)
            continue
        num = int(m.group(1))
        fn_m = re.search(r"`([^`]+\.md)`", line)
        if not fn_m:
            out.append(line)
            continue
        fn = fn_m.group(1)
        path = DRAFTS / fn
        if not path.exists():
            out.append(line)
            continue
        wc = len(path.read_text(encoding="utf-8").split())
        need = min_for_file(fn)
        if wc >= need:
            new = re.sub(
                r"\|\s+(pending|draft-exists)\s+\|",
                f"| **draft-done** (~{wc}w) |",
                line,
                count=1,
            )
            if "draft-done" not in new and "**draft-done**" not in new:
                new = re.sub(
                    r"\|\s+\*\*draft-done\*\*[^|]*\s+\|",
                    f"| **draft-done** (~{wc}w) |",
                    line,
                    count=1,
                )
            out.append(new)
        else:
            out.append(line)
    PLAN.write_text("\n".join(out) + "\n", encoding="utf-8")
    pending = sum(1 for l in out if "| pending |" in l)
    done = sum(1 for l in out if "draft-done" in l)
    print(f"Updated plan: {done} draft-done, {pending} pending")


if __name__ == "__main__":
    main()
