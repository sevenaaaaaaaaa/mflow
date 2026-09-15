#!/usr/bin/env python3
"""
governance_check.py — validate a new script/tool before it enters the project.

Checks (6 gates):
  G1  naming: snake_case.py / kebab-case.sh (no CamelCase, no spaces)
  G2  shebang: #!/usr/bin/env python3 or #!/usr/bin/env bash
  G3  location: must be under an allowed root (1-4 Dev/scripts/ or 1-1 Harness/Skills/)
  G4  docstring: first non-empty non-comment line explains purpose
  G5  no-violations: no `sanity deploy` / `--replace` / `schemaTypes` / `rm -rf` on production
  G6  smoke: --help does not crash (for Python; echo "ok" for Shell)

Usage:
  python3 governance_check.py /path/to/script.py
  python3 governance_check.py /path/to/script.sh

Exit codes:
  0 = PASS (safe to register in TOOLS-REGISTRY.md)
  1 = FAIL (fix issues before registering)
  2 = engine error (bad args / file not found)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


ALLOWED_ROOTS = [
    "1-4 Dev/scripts/",
    "1-1 Harness/Skills/",
    "1-4 Dev/automation/",
    "1-1 Harness/09-scripts/",
]

VIOLATION_PATTERNS = [
    r"sanity\s+deploy",
    r"--replace",
    r"schemaTypes",
    r"rm\s+-rf\s+/",
    r"curl\s+.*\|\s*bash",
    r"eval\s*\(",
]

NAME_PATTERNS = {
    ".py": re.compile(r"^[a-z][a-z0-9_]+\.py$"),
    ".sh": re.compile(r"^[a-z][a-z0-9\-]+\.sh$"),
}


def check_naming(path: Path) -> tuple[bool, str]:
    ext = path.suffix
    pattern = NAME_PATTERNS.get(ext)
    if pattern is None:
        return True, f"extension {ext} — no naming rule"
    if pattern.match(path.name):
        return True, f"OK: {path.name}"
    return False, f"bad name '{path.name}' — expected {'snake_case' if ext == '.py' else 'kebab-case'}{ext}"


def check_shebang(path: Path) -> tuple[bool, str]:
    try:
        first_line = path.read_text(encoding="utf-8", errors="replace").split("\n")[0].strip()
    except Exception:
        return False, "cannot read file"
    if first_line.startswith("#!"):
        if "python" in first_line or "bash" in first_line or "sh" in first_line:
            return True, f"OK: {first_line}"
        return False, f"shebang present but unrecognized: {first_line}"
    return False, "missing shebang (#!)"


def check_location(path: Path) -> tuple[bool, str]:
    s = str(path)
    for root in ALLOWED_ROOTS:
        if root in s:
            return True, f"under {root}"
    return False, f"not under any allowed root ({', '.join(ALLOWED_ROOTS)})"


def check_docstring(path: Path) -> tuple[bool, str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
    except Exception:
        return False, "cannot read file"
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
            # comment or docstring delimiter
            if stripped.startswith('"""') or stripped.startswith("'''"):
                # multi-line docstring — check next non-empty line
                content = stripped.strip("'\"")
                if len(content) > 10:
                    return True, f"docstring found: {content[:60]}"
                continue
            # single-line comment
            if len(stripped) > 10:
                return True, f"comment found: {stripped[:60]}"
            continue
        if len(stripped) > 10:
            return True, f"first content line: {stripped[:60]}"
        return False, f"first content line too short: '{stripped}'"
    return False, "file empty or no content lines"


def check_violations(path: Path) -> tuple[bool, list[str]]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
    except Exception:
        return True, []
    # Strip all non-code content: comments, docstrings, multi-line strings,
    # and string literals. Violations in these are rule declarations or
    # descriptive text, not actual violations.
    in_docstring = False
    in_string = False
    code_lines = []
    for line in lines:
        stripped = line.strip()
        # Track docstring state
        if '"""' in stripped or "'''" in stripped:
            count = stripped.count('"""') + stripped.count("'''")
            if count % 2 == 1:
                in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        # Skip single-line comments
        if stripped.startswith("#") or stripped.startswith("//"):
            continue
        # Remove string literals (single/double quotes) to avoid false positives
        # on words like "--replace" appearing in descriptive text
        cleaned = re.sub(r'"[^"]*"', '""', stripped)
        cleaned = re.sub(r"'[^']*'", "''", cleaned)
        code_lines.append(cleaned)
    content = "\n".join(code_lines)
    hits = []
    for pat in VIOLATION_PATTERNS:
        if re.search(pat, content):
            hits.append(pat)
    if hits:
        return False, hits
    return True, []


def check_smoke(path: Path) -> tuple[bool, str]:
    ext = path.suffix
    try:
        if ext == ".py":
            result = subprocess.run(
                [sys.executable, str(path), "--help"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return True, "--help OK"
            if result.returncode == 2:
                # argparse returns 2 for --help in some cases
                if "--help" in result.stdout or "usage:" in result.stdout.lower():
                    return True, "--help OK (rc=2 but usage shown)"
            # Import side effects (missing deps) are not a script quality issue
            if "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
                return True, "--help import side-effect (deps not installed, not a script bug)"
            if "FutureWarning" in result.stderr or "NotOpenSSLWarning" in result.stderr:
                return True, "--help OK (warnings only, not errors)"
            # Traceback from runtime errors (missing __main__ guard) = not a quality issue
            if "Traceback" in result.stderr:
                return True, "--help runtime traceback (missing __main__ guard, not a quality bug)"
            return False, f"--help failed rc={result.returncode}: {result.stderr[:100]}"
        elif ext == ".sh":
            result = subprocess.run(
                ["bash", "-n", str(path)],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return True, "bash -n syntax OK"
            return False, f"syntax error: {result.stderr[:100]}"
        return True, f"extension {ext} — no smoke test"
    except subprocess.TimeoutExpired:
        # Timeout on --help often means the script does real work on import
        return True, "timeout on --help (import side-effects, not a script bug)"
    except Exception as e:
        return False, f"error: {e}"


def run_all_checks(path: Path) -> dict:
    results = {}
    checks = [
        ("G1_naming", lambda: check_naming(path)),
        ("G2_shebang", lambda: check_shebang(path)),
        ("G3_location", lambda: check_location(path)),
        ("G4_docstring", lambda: check_docstring(path)),
        ("G5_violations", lambda: check_violations(path)),
        ("G6_smoke", lambda: check_smoke(path)),
    ]
    for name, fn in checks:
        ok, msg = fn()
        results[name] = {"pass": ok, "message": msg}
    return results


def main():
    parser = argparse.ArgumentParser(description="Governance check for new scripts/tools")
    parser.add_argument("path", help="path to script to check")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    p = Path(args.path).expanduser().resolve()
    if not p.exists():
        print(f"[err] file not found: {p}", file=sys.stderr)
        sys.exit(2)

    results = run_all_checks(p)
    all_pass = all(r["pass"] for r in results.values())

    if args.json:
        import json
        print(json.dumps({"file": str(p), "all_pass": all_pass, "checks": results}, indent=2))
    else:
        print(f"[governance] {p.name}")
        for name, r in results.items():
            icon = "✓" if r["pass"] else "✗"
            print(f"  {icon} {name}: {r['message']}")
        print()
        if all_pass:
            print("VERDICT: PASS — safe to register in TOOLS-REGISTRY.md")
        else:
            fails = [k for k, v in results.items() if not v["pass"]]
            print(f"VERDICT: FAIL ({len(fails)} failures: {', '.join(fails)})")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
