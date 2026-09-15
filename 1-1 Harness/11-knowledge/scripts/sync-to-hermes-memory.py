#!/usr/bin/env python3
"""
sync-to-hermes-memory.py — push MEMORY-PROJECT.md facts into Hermes MEMORY.md.

Design (conservative, idempotent, auditable):
  - Hermes MEMORY.md is one-line-per-fact with `§` separators between topics.
  - We treat MEMORY-PROJECT.md as ground truth for project slice.
  - We pick a SUBSET of sections ('project slice') — only SSOT for tools/routing/Sanity/Profiles/HOW — that are
    universally true for all tools, not user preferences.
  - For each section, we render to one line, fingerprint, and only insert if absent.
  - Create a backup before any write; keep last 14 days of backups.
  - Idempotent: re-running within same day adds at most one new entry.

Boundary: USER.md NEVER touched. We write to MEMORY.md only.

Usage:
  python3 sync-to-hermes-memory.py --root <vault>
  python3 sync-to-hermes-memory.py --root <vault> --dry-run

Exit codes: 0 ok, 1 hard err, 2 noop
"""

import argparse
import datetime
import hashlib
import re
import shutil
import sys
from pathlib import Path


# Sections we mirror to global memory (project slice)
SLICE_NUMS = {0, 1, 2, 4, 7, 8}

# Sections explicitly NOT mirrored (user-corrections = USER.md only; cross-project = Hermes MEMORY.md already)
EXCLUDE_NUMS = {5, 9, 10, 11}

# Marker inside Hermes MEMORY.md where bridged facts live
BRIDGE_MARKER = "BridFacts"


FRONT = re.compile(r"^---\n.*?\n---\n", re.DOTALL | re.MULTILINE)


def fingerprint(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def render_section(text: str) -> str:
    """Strip markdown char to single-line plain-fact form."""
    s = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    # collapse bullets / numbered lists
    s = re.sub(r"^\s*[-*]\s+", "", s, flags=re.MULTILINE)
    s = re.sub(r"^\s*\d+\.\s+", "", s, flags=re.MULTILINE)
    # table-row cleanup
    s = re.sub(r"\s*\|\s*", "；", s)
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    out = "；".join(lines)
    # cap
    return out[:1000]


def split_project_sections(project_md: str):
    chunks = re.split(r"(?=^## § )", project_md, flags=re.MULTILINE)
    sections = []
    for c in chunks:
        m = re.match(r"## §\s*(\d+)\b", c)
        if not m:
            continue
        n = int(m.group(1))
        if n in EXCLUDE_NUMS:
            continue
        if n not in SLICE_NUMS:
            continue
        sections.append((m.group(0).strip(), c))
    return sections


def backup(path: Path):
    if not path.exists():
        return None
    bkdir = path.parent / ".backups"
    bkdir.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bk = bkdir / f"MEMORY-{stamp}.bak"
    shutil.copy2(path, bk)
    # keep last 14
    bks = sorted(bkdir.glob("MEMORY-*.bak"))
    while len(bks) > 14:
        bks[0].unlink()
        bks = bks[1:]
    return bk


def already_bridged(hermes_text: str, fp: str) -> bool:
    return fp in hermes_text


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=str(Path(__file__).resolve().parents[3]))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    vault = Path(args.root).expanduser()

    project_path = vault / "1-1 Harness" / "11-knowledge" / "MEMORY-PROJECT.md"
    hermes_path = Path.home() / ".hermes" / "memories" / "MEMORY.md"

    if not project_path.exists():
        sys.stderr.write(f"sync-to-hermes: missing {project_path}\n")
        return 1

    project_text = project_path.read_text("utf-8")
    # strip leading frontmatter if any
    project_text = re.sub(r"^---\n.*?\n---\n", "", project_text, count=1, flags=re.DOTALL)

    sections = split_project_sections(project_text)
    new_facts = []
    for head, body in sections:
        line = render_section(body)
        fp = fingerprint(head + "::" + line)
        if not already_bridged(project_text + (hermes_path.read_text("utf-8") if hermes_path.exists() else ""), fp):
            new_facts.append((fp, line))

    if not new_facts:
        print("sync-to-hermes: noop (all § 0/1/2/4/7/8 already bridged)")
        return 2

    today = datetime.date.today().isoformat()
    body_line = f"[{today}/梦幻桥] {BRIDGE_MARKER}: " + " ◆ ".join(line for _, line in new_facts)
    body_line_for_header = f"Bridged§{today}: " + " ✓ ".join(fp for fp, _ in new_facts)

    # load Hermes MEMORY
    hermes_text = hermes_path.read_text("utf-8") if hermes_path.exists() else ""

    # locate insertion point: after the first line containing "Dream" OR end of file.
    # Newer entries go at END so older context isn't displaced.
    lines = hermes_text.splitlines()

    # idempotent: if today's marker is already present, no-op
    if today in hermes_text and "梦幻桥" in hermes_text:
        # Check fp already there
        if all(fp in hermes_text for fp, _ in new_facts):
            print("sync-to-hermes: noop (today's facts already bridged)")
            return 2

    if args.dry_run:
        print("DRY RUN. Would write:")
        print(f"  header (replace): {body_line_for_header}")
        print(f"  body line: {body_line[:200]}...")
        return 0

    bk = backup(hermes_path)
    if bk:
        print(f"backup → {bk}")

    # find existing "BridFacts" header; replace it.
    new_lines = []
    fp_set = set(fp for fp, _ in new_facts)
    replaced_header = False
    for l in lines:
        if re.match(r"^Bridged§\d{4}-\d{2}-\d{2}:\s", l):
            # merge: keep existing facts + add new ones
            existing_fps = set(re.findall(r"\b[a-f0-9]{12}\b", l))
            merged = existing_fps | fp_set
            merged_str = " ✓ ".join(sorted(merged))
            new_lines.append(f"Bridged§{today}: {merged_str}")
            replaced_header = True
        else:
            new_lines.append(l)
    if not replaced_header:
        new_lines.append(f"Bridged§{today}: " + " ✓ ".join(sorted(fp_set)))

    # find body line insertion: right after the existing "BridFacts/" or some sentinel like § separator
    inserted = False
    out = []
    for i, l in enumerate(new_lines):
        out.append(l)
        if not inserted and BRIDGE_MARKER in l and "梦幻桥" not in l and "FYI" not in l:
            # this is the OLD marker-disambiguator block, append new body line there
            pass
    # simpler: find any line boldstarting with "[YYYY-MM-DD/幻" and skip-insert
    final = []
    bridged_line_inserted = False
    for l in new_lines:
        final.append(l)
        if not bridged_line_inserted and re.match(r"^\[\d{4}-\d{2}-\d{2}/梦幻桥\] BridFacts:", l):
            # already there; do nothing (caller will treat as no-op upstream)
            bridged_line_inserted = True
    # actually rewrite: drop any prior "梦幻桥" lines then append new at bottom
    cleaned = [l for l in new_lines if not re.match(r"^\[\d{4}-\d{2}-\d{2}/梦幻桥\] BridFacts:", l)]
    # also drop prior header line so we re-emit
    cleaned = [l for l in cleaned if not re.match(r"^Bridged§\d{4}-\d{2}-\d{2}:\s", l)]
    cleaned.append(f"Bridged§{today}: " + " ✓ ".join(sorted(fp_set)))
    cleaned.append("§")  # separator
    cleaned.append(body_line)

    hermes_path.write_text("\n".join(cleaned) + "\n", encoding="utf-8")
    print(f"sync-to-hermes: wrote {len(new_facts)} facts to Hermes MEMORY.md (header + body lines)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
