#!/usr/bin/env python3
"""
fm-fix.py — add minimal frontmatter to governed markdown files ONLY where missing.

Policy by path (kept in one place so it's easy to tune):
  1-1 Harness/02-rules/RULES-00-iron.md       → type: rule/iron
  1-1 Harness/02-rules/RULES-{NN}-*.md        → type: rule + scope=profile-{name}
  1-1 Harness/02-rules/SESSION-ROUTING.md     → type: session-routing
  1-1 Harness/06-cron/                         → type: cron + scope=lovart-management
  1-1 Harness/08-storyline/                    → type: storyline + scope=lovart-creation
  1-1 Harness/11-knowledge/dream/README.md     → type: dream-readme
  1-1 Harness/11-knowledge/audit/              → type: audit-report
  1-1 Harness/CLAUDE.md                        → type: tool-entrypoint/claude
  1-1 Harness/Docs/S3-内容创作/                → type: stage-sop/s3
  1-1 Harness/Docs/S3-内容创作/i18n-*          → extra tags: i18n

Rules (HARD):
  - If file already has frontmatter with BOTH type and version, leave it.
  - If existing frontmatter is partial, fill only missing keys; never overwrite.
  - Never remove or rewrite body.
  - Audit artifacts (audit-report-*.md) get type+version (version reflects today);
    we DON'T touch their bodies.
  - Crash on any IO error.

Usage:
  python3 fm-fix.py --root <vault>
  python3 fm-fix.py --root <vault> --dry-run   # print plan, no write
"""

import argparse
import datetime
import re
import sys
from pathlib import Path


FRONT = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL | re.MULTILINE)
KV = re.compile(r"^([a-zA-Z_][\w-]*):\s*(.+?)\s*$", re.MULTILINE)


def parse(path):
    text = path.read_text("utf-8", errors="ignore")
    m = FRONT.match(text)
    if not m:
        return None, text
    body = m.group(1)
    return {k: v for k, v in KV.findall(body)}, text


def derive_type(rel: str) -> str:
    p = Path(rel)
    if rel.endswith("/CLAUDE.md") or rel.endswith("CLAUDE.md"):
        if p.parent.name == "1-1 Harness":
            return "tool-entrypoint/claude"
    parts = p.parts
    if "02-rules" in parts:
        nm = p.name
        if nm == "RULES-00-iron.md":
            return "rule/iron"
        if nm == "SESSION-ROUTING.md":
            return "session-routing"
        m = re.match(r"RULES-(\d{2})-(\w+)\.md", nm)
        if m:
            return "rule"
    if "06-cron" in parts:
        return "cron"
    if "08-storyline" in parts:
        if "FEATURES-PRODUCTION" in p.name:
            return "storyline/features"
        return "storyline"
    if "11-knowledge" in parts:
        if "dream" in parts and p.suffix == ".md":
            return "dream-readme"
        if "audit" in parts and p.name.startswith("audit-report"):
            return "audit-report"
        if "audit" in parts and p.name.startswith("audit-") and p.suffix == ".json":
            return None  # not md, skip
        return "knowledge-doc"
    if "Docs" in parts and "S3" in parts[parts.index("Docs") + 1]:
        nm = p.name
        if "i18n" in nm.lower():
            return "stage-sop/s3/i18n"
        return "stage-sop/s3"
    return "governed-doc"


def derive_scope(rel: str) -> str:
    if "02-rules" in Path(rel).parts:
        nm = Path(rel).name
        m = re.match(r"RULES-(\d{2})-(\w+)\.md", nm)
        if m:
            num = m.group(1)
            return f"profile-{m.group(2).rstrip('s')}-" + ("active" if num in {"10", "20", "30", "40", "50", "60"} else "global")
        if nm == "RULES-00-iron.md":
            return "all"
        if nm == "SESSION-ROUTING.md":
            return "all"
    if "06-cron" in Path(rel).parts:
        return "profile-lovart-management"
    if "08-storyline" in Path(rel).parts:
        return "profile-lovart-creation"
    if "11-knowledge" in Path(rel).parts:
        return "profile-lovart-management"
    if "Docs" in Path(rel).parts:
        return "profile-lovart-creation"
    if "CLAUDE.md" in Path(rel).name:
        return "tool-claude"
    return "all"


def derive_tools(rel: str) -> str:
    # tools that should auto-load this file (yaml list)
    p = Path(rel)
    if "11-knowledge" in p.parts:
        return "[hermes, opencode, cursor, claude, codex]"
    if "02-rules" in p.parts:
        return "[hermes, opencode, claude]"
    if "06-cron" in p.parts:
        return "[hermes, claude]"
    if "08-storyline" in p.parts:
        return "[opencode, claude, cursor]"
    if "Docs" in p.parts:
        return "[opencode, claude]"
    if "CLAUDE.md" in p.name:
        return "[claude]"
    return "[hermes, opencode, claude]"


def derive_status(rel: str) -> str:
    p = Path(rel)
    if "01-project" in p.parts:
        return "snapshot"
    if p.name.endswith(" 2.md"):  # legacy duplicates
        return "legacy"
    if "FEATURES-PRODUCTION 2.md" == p.name:
        return "legacy"
    return "active"


def build_front(rel: str, today: str) -> str:
    typ = derive_type(rel)
    if typ is None:
        return ""
    scope = derive_scope(rel)
    tools = derive_tools(rel)
    status = derive_status(rel)
    yaml = (
        "---\n"
        f"type: {typ}\n"
        "version: 1.0\n"
        f"updated: {today}\n"
        f"scope: \"{scope}\"\n"
        f"tools: {tools}\n"
        f"status: {status}\n"
        f"path: {rel}\n"
        "generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py\n"
        "---\n"
    )
    return yaml


def derive_missing(existing, rel, today):
    """Return either:
       - full new frontmatter block (no existing => write fresh)
       - full reconstructed block (existing partial => merge in our derived keys
                                  preserving user-set keys we don't know about)
       - None (existing complete => no-op)
    """
    if not existing:
        # no frontmatter at all → write the full new block
        return build_front(rel, today)
    needed = {
        "type": derive_type(rel),
        "version": "1.0",
        "updated": today,
        "scope": derive_scope(rel),
        "tools": derive_tools(rel),
        "status": derive_status(rel),
        "path": rel,
    }
    if needed["type"] is None:
        return ""
    if all(needed[k] is None or k in existing for k in needed):
        return None
    # Merge: keep existing keys verbatim, fill missing from needed.
    merged = dict(existing)
    for k, v in needed.items():
        if v is None:
            continue
        if k not in merged:
            merged[k] = v
    merged["generator"] = "1-1 Harness/11-knowledge/scripts/fm-fix.py"
    block = "---\n" + "\n".join(f"{k}: {merged[k]}" for k in merged) + "\n---\n"
    return block


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=str(Path(__file__).resolve().parents[3]))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    root = Path(args.root).expanduser()
    if not root.exists():
        sys.stderr.write(f"fm-fix: root {root} does not exist\n")
        sys.exit(2)

    today = datetime.date.today().isoformat()
    targets = [
        root / "1-1 Harness" / "02-rules",
        root / "1-1 Harness" / "06-cron",
        root / "1-1 Harness" / "08-storyline",
        root / "1-1 Harness" / "11-knowledge" / "dream",
        root / "1-1 Harness" / "11-knowledge" / "audit",
        root / "1-1 Harness" / "Docs" / "S3-内容创作",
    ]
    files = []
    for d in targets:
        if d.exists():
            files.extend(d.rglob("*.md"))
    files.append(root / "1-1 Harness" / "CLAUDE.md")

    plan = []
    for f in sorted(set(files)):
        rel = str(f.relative_to(root))
        existing, text = parse(f)
        # skip already-complete
        if existing and all(k in existing for k in ("type", "version", "scope", "tools")):
            continue
        plan.append((rel, existing is None))

    if not plan:
        print(f"fm-fix: nothing to do ({len(files)} files already gated)")
        return

    print(f"fm-fix plan: {len(plan)} files to update\n")
    for rel, has_none in plan:
        flag = "MISSING_FM" if has_none else "PARTIAL_FM"
        print(f"  [{flag:<11}]  {rel}")
        if args.dry_run:
            continue
        target = root / rel
        existing, text = parse(target)
        new_block = derive_missing(existing, rel, today)
        if new_block is None or new_block == "":
            continue
        # Replace existing frontmatter block if present; otherwise prepend.
        if existing is not None:
            new_text = re.sub(r"^---\n.*?\n---\n", new_block, text, count=1, flags=re.DOTALL | re.MULTILINE)
        else:
            new_text = new_block + text
        target.write_text(new_text, encoding="utf-8")
        print(f"               wrote {target}")

    if not args.dry_run:
        print(f"\n→ run: python3 1-1\\ Harness/11-knowledge/scripts/fm-check.py --strict  to re-audit")


if __name__ == "__main__":
    main()
