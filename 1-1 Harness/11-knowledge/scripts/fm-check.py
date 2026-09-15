#!/usr/bin/env python3
"""
fm-check.py — verify every governed file has its required frontmatter keys.

Governance contract:
  Required keys: type, version, last_consolidated OR updated OR generated
  Optional keys: tools, profiles, owner, status, tags, cross_refs

Per-file governance style (each file declares its own type):
  - kb-doc / kb-doc (queries / rules / docs) require [type, version]
  - session-log  (sessions/*.md) — different schema: requires session_date + session_slug
  - session-template (session schema doc) has its own frontmatter convention

Scope (default):
  1-1 Harness/02-rules/*.md
  1-1 Harness/05-skills/**/*.md (SKILL.md and references/)
  1-1 Harness/06-cron/**/*.md
  1-1 Harness/08-storyline/**/*.md
  1-1 Harness/11-knowledge/**/*.md (EXCEPT sessions/  handled separately)
  docs/skill-manifest.json             # per-skill identity (TODO)
  1-1 Harness/CLAUDE.md

Usage:
  python3 fm-check.py [--root path] [--fix] [--strict]
  --root  : vault root (default = parent's parent's parent)
  --fix   : add missing required keys with placeholder values (review)
  --strict: exit 1 if any missing key
"""

import argparse
import re
import sys
from pathlib import Path


REQUIRED = ["type", "version"]
OPTIONAL = ["status", "owner", "updated", "last_consolidated", "generated", "tools", "profiles", "tags"]

# Per-file-type required key map: deviation from default
ALT_REQUIRED = {
    "session-log":     ["session_date", "session_slug"],   # NOT type/version
    "session-template": ["type", "version"],                # type=session-template is OK with default
}


FRONT = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL | re.MULTILINE)
KV = re.compile(r"^([a-zA-Z_][\w-]*):\s*(.+?)\s*$", re.MULTILINE)


def parse(path):
    text = path.read_text("utf-8", errors="ignore")
    m = FRONT.match(text)
    if not m:
        return None, text
    body = m.group(1)
    return {k: v for k, v in KV.findall(body)}, text


def required_keys_for(meta, path):
    """Pick the right required-keys set based on declared type OR path."""
    typ = (meta.get("type") or "").strip()
    if typ in ALT_REQUIRED:
        return ALT_REQUIRED[typ]
    # Path-based fallback for session logs that didn't declare type
    rel = str(path)
    if "/sessions/" in rel and rel.endswith(".md") and "/sessions/_drafts" not in rel:
        # Session log files are name-pattern YYYY-MM-DD-slug.md
        import re as _re
        if _re.search(r"/sessions/\d{4}-\d{2}-\d{2}-[^/]+\.md$", rel):
            return ["session_date", "session_slug"]
    return REQUIRED


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=str(Path(__file__).resolve().parents[3]))
    p.add_argument("--fix", action="store_true")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()

    root = Path(args.root).expanduser()
    if not root.exists():
        sys.stderr.write(f"fm-check: root {root} does not exist\n")
        sys.exit(2)

    targets = [
        root / "1-1 Harness" / "02-rules",
        root / "1-1 Harness" / "06-cron",
        root / "1-1 Harness" / "08-storyline",
        root / "1-1 Harness" / "11-knowledge",
        root / "1-1 Harness" / "Docs" / "S3-内容创作",
    ]
    files = []
    for d in targets:
        if d.exists():
            # Exclude sessions dir from default scan; handled separately
            if str(d).endswith("11-knowledge"):
                for p in d.rglob("*.md"):
                    rel = p.relative_to(root)
                    if "11-knowledge/sessions/" in str(rel):
                        # include sessions but use ALT_REQUIRED
                        files.append(p)
                    else:
                        files.append(p)
            else:
                files.extend(d.rglob("*.md"))

    files += [root / "1-1 Harness" / "CLAUDE.md"]

    missing = []
    for f in files:
        meta, text = parse(f)
        if meta is None:
            missing.append((f, "NO_FRONTMATTER"))
            continue
        req = required_keys_for(meta, f)
        bad_keys = [k for k in req if not meta.get(k)]
        if bad_keys:
            missing.append((f, f"missing:{','.join(bad_keys)}"))

    if not missing:
        print(f"fm-check OK — {len(files)} files, all frontmatter valid")
        return

    print(f"fm-check — {len(missing)}/{len(files)} need attention:\n")
    for f, why in missing:
        print(f"  {f.relative_to(root)}  →  {why}")

    if args.strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
