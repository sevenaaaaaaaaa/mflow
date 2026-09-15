#!/usr/bin/env python3
"""
dream/reflect.py — Layer 2 of self-growth loop.

Scans 1-1 Harness/11-knowledge/sessions/*.md (excluding _drafts/ + SESSION-TEMPLATE.md)
and extracts Patterns Observed (P#-prefixed bullets). Tallies frequency across
all session logs; writes a recurring-patterns/{YYYY-QW}.md report.

Output structure:
  - Pattern frequency (by unique-source count + by mention count)
  - Decisions frequency (D#) - for awareness only, not promoted
  - Open Questions frequency (Q#) - for awareness only
  - Patterns ≥2 sources → "candidate for PR workflow"
  - Patterns ≥3 sources → "strong recommendation"

Boundary:
  - Reflect is READ-ONLY (does NOT modify any KB doc, rule, or skill)
  - Only writes to recurring-patterns/ directory
  - Promotions happen via separate PR workflow (Layer 3, not implemented yet)

Usage:
  bash dream/reflect.sh                        # runs the script
  python3 dream/reflect.py --dry-run           # print stats, do not write
  python3 dream/reflect.py --root <vault>      # custom vault path

Output:
  audit/recurring-patterns/{YYYY-QW}.md (or per ISO week)
"""

import argparse
import datetime
import re
import sys
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
KNOWLEDGE = HERE.parent  # 1-1 Harness/11-knowledge/
SESSIONS_DIR = KNOWLEDGE / "sessions"
RECURRING_DIR = KNOWLEDGE / "dream" / "recurring-patterns"


# Regex matchers for P# / D# / Q# bullets in session logs
P_RE = re.compile(r"^\s*[-*]\s*\*?\*?P(\d+)\b", re.MULTILINE)
D_RE = re.compile(r"^\s*[-*]\s*\*?\*?D(\d+)\b", re.MULTILINE)
Q_RE = re.compile(r"^\s*[-*]\s*\*?\*?Q(\d+)\b", re.MULTILINE)


def extract_patterns(text: str) -> dict[str, str]:
    """Return {P1: 'text', P2: 'text', ...} from a session log."""
    patterns = {}
    for m in P_RE.finditer(text):
        n = m.group(1)
        # grab surrounding text (next ~200 chars after match)
        start = m.start()
        end = m.end()
        # find next newline
        nl = text.find("\n", end)
        snippet = text[end:nl if nl > 0 else end + 200].strip()[:300]
        # take first 1-2 sentences
        snippet = re.split(r"[-*]\s*\*?\*?[PDQ]\d+\b", snippet)[0].strip()
        # also strip leading markdown artifacts
        snippet = re.sub(r"^\s*[\*_`>]*", "", snippet)
        snippet = re.sub(r"\s*[._`:]+$", "", snippet)
        patterns[n] = snippet.strip()
    return patterns


def extract_decisions(text: str) -> dict[str, str]:
    decisions = {}
    for m in D_RE.finditer(text):
        n = m.group(1)
        end = m.end()
        nl = text.find("\n", end)
        snippet = text[end:nl if nl > 0 else end + 200].strip()[:200]
        snippet = re.sub(r"^\s*[\*_`>]*", "", snippet)
        decisions[n] = snippet.strip()
    return decisions


def extract_questions(text: str) -> dict[str, str]:
    questions = {}
    for m in Q_RE.finditer(text):
        n = m.group(1)
        end = m.end()
        nl = text.find("\n", end)
        snippet = text[end:nl if nl > 0 else end + 200].strip()[:200]
        snippet = re.sub(r"^\s*[\*_`>]*", "", snippet)
        questions[n] = snippet.strip()
    return questions


def scan_sessions(sessions_dir: Path) -> list[dict]:
    """Returns a list of {file, slug, date, patterns, decisions, questions}."""
    out = []
    if not sessions_dir.exists():
        return out
    for p in sorted(sessions_dir.rglob("*.md")):
        if p.name in ("SESSION-TEMPLATE.md",) or "_drafts" in p.parts:
            continue
        if not p.name[:10].replace("-", "").isdigit():
            continue  # not YYYY-MM-DD prefix
        text = p.read_text("utf-8", errors="ignore")
        # parse slug from filename
        stem = p.stem
        # strip YYYY-MM-DD- prefix
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
        date = p.name[:10]
        out.append({
            "file": str(p.relative_to(sessions_dir.parent)),
            "slug": slug,
            "date": date,
            "patterns": extract_patterns(text),
            "decisions": extract_decisions(text),
            "questions": extract_questions(text),
        })
    return out


def aggregate(sessions: list[dict]) -> tuple[dict, dict, dict]:
    """Aggregate per-P/D/Q across all sessions.

    Returns (p_agg, d_agg, q_agg) where each is:
      {p_num: {"snippet": str, "sources": [file, ...], "mentions": int}}
    """
    def build(sessions, extractor):
        agg = defaultdict(lambda: {"snippet": "", "sources": [], "mentions": 0})
        for s in sessions:
            for n, snippet in extractor(s).items():
                rec = agg[n]
                if not rec["snippet"]:
                    rec["snippet"] = snippet
                rec["sources"].append(s["file"])
                rec["mentions"] += 1
        return dict(agg)

    return (
        build(sessions, lambda s: s["patterns"]),
        build(sessions, lambda s: s["decisions"]),
        build(sessions, lambda s: s["questions"]),
    )


def iso_week(d: datetime.date) -> str:
    iso = d.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def render_report(week_str: str, sessions: list[dict],
                  p_agg: dict, d_agg: dict, q_agg: dict,
                  generated_at: str) -> str:
    lines = [
        f"---",
        f"type: recurring-patterns-report",
        f"version: 1.0",
        f"week: {week_str}",
        f"generated: {generated_at}",
        f"generator: 1-1 Harness/11-knowledge/dream/reflect.py",
        f"sessions_scanned: {len(sessions)}",
        f"---",
        f"",
        f"# Recurring Patterns — {week_str}",
        f"",
        f"> Generated by `dream/reflect.sh`. READ-ONLY script: this report does NOT modify any",
        f"> rules / skills / KB docs. Promotion to rules happens via separate PR workflow (Layer 3).",
        f"",
        f"## Summary",
        f"",
        f"- Sessions scanned: **{len(sessions)}**",
        f"- Unique patterns observed: **{len(p_agg)}**",
        f"- Unique decisions made: **{len(d_agg)}**",
        f"- Unique open questions: **{len(q_agg)}**",
        f"",
    ]

    # PR candidates (≥2 unique sources)
    candidates = sorted(
        [(n, rec) for n, rec in p_agg.items() if len(rec["sources"]) >= 2],
        key=lambda kv: (-len(kv[1]["sources"]), -kv[1]["mentions"], kv[0]),
    )
    strong = sorted(
        [(n, rec) for n, rec in p_agg.items() if len(rec["sources"]) >= 3],
        key=lambda kv: (-len(kv[1]["sources"]), kv[0]),
    )

    lines.append("## PR Candidates (≥2 unique sources = rule/skill spawn candidate)")
    lines.append("")
    if not candidates:
        lines.append("_None yet. Need ≥2 sessions mentioning same P# across sources._")
    else:
        for n, rec in candidates:
            mark = "★ STRONG" if n in {x[0] for x in strong} else ""
            lines.append(f"### P{n} {mark}")
            lines.append(f"- **Sources ({len(rec['sources'])} unique, {rec['mentions']} mentions)**:")
            for src in rec["sources"]:
                lines.append(f"  - `{src}`")
            lines.append(f"- **Snippet**: {rec['snippet']}")
            lines.append("")
    lines.append("")

    lines.append("## All Patterns (frequency view)")
    lines.append("")
    lines.append("| P# | Sources | Mentions | Snippet |")
    lines.append("|----|---------|----------|---------|")
    for n, rec in sorted(p_agg.items(), key=lambda kv: (-len(kv[1]["sources"]), kv[0])):
        snip = rec["snippet"][:80].replace("|", "/")
        lines.append(f"| P{n} | {len(rec['sources'])} | {rec['mentions']} | {snip} |")
    lines.append("")

    lines.append("## Decisions (informational — not promoted)")
    lines.append("")
    if not d_agg:
        lines.append("_None._")
    else:
        lines.append("| D# | Sources | Snippet |")
        lines.append("|----|---------|---------|")
        for n, rec in sorted(d_agg.items(), key=lambda kv: (-len(kv[1]["sources"]), kv[0])):
            snip = rec["snippet"][:80].replace("|", "/")
            lines.append(f"| D{n} | {len(rec['sources'])} | {snip} |")
    lines.append("")

    lines.append("## Open Questions (informational — lifecycle tracked in MEMORY-PROJECT.md)")
    lines.append("")
    if not q_agg:
        lines.append("_None._")
    else:
        lines.append("| Q# | Sources | Snippet |")
        lines.append("|----|---------|---------|")
        for n, rec in sorted(q_agg.items(), key=lambda kv: (-len(kv[1]["sources"]), kv[0])):
            snip = rec["snippet"][:80].replace("|", "/")
            lines.append(f"| Q{n} | {len(rec['sources'])} | {snip} |")
    lines.append("")

    lines.append("## Sessions Scanned")
    lines.append("")
    if not sessions:
        lines.append("_None._")
    else:
        for s in sessions:
            lines.append(f"- `{s['date']}` — {s['slug']}  ({len(s['patterns'])} P / {len(s['decisions'])} D / {len(s['questions'])} Q)")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Promotion Workflow (Layer 3 — TBD)")
    lines.append("")
    lines.append("To promote a pattern into a real rule/skill, future workflow:")
    lines.append("1. Review `## PR Candidates` section above")
    lines.append("2. For each P# = candidate: agent drafts `1-1 Harness/02-rules/<topic>.md` (or skill SKILL.md)")
    lines.append("3. Submit PR-equivalent proposal (Layer 3)")
    lines.append("4. User approves → commit to harness")
    lines.append("5. Pattern P# is moved to 'Promoted' section of next reflect run")
    lines.append("")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=str(KNOWLEDGE.parent.parent))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    sessions_dir = root / "1-1 Harness" / "11-knowledge" / "sessions"
    recurring_dir = root / "1-1 Harness" / "11-knowledge" / "dream" / "recurring-patterns"

    sessions = scan_sessions(sessions_dir)
    p_agg, d_agg, q_agg = aggregate(sessions)

    # determine ISO week
    today = datetime.date.today()
    week_str = iso_week(today)

    generated_at = datetime.datetime.now().isoformat(timespec="seconds")

    if args.dry_run:
        print(f"DRY RUN — scanned {len(sessions)} session(s)")
        print(f"  patterns: {len(p_agg)} ({(sorted(p_agg.keys()))[:5]}...)")
        print(f"  decisions: {len(d_agg)}")
        print(f"  questions: {len(q_agg)}")
        return

    recurring_dir.mkdir(parents=True, exist_ok=True)
    report = render_report(week_str, sessions, p_agg, d_agg, q_agg, generated_at)
    out = recurring_dir / f"{week_str}.md"
    out.write_text(report, encoding="utf-8")
    print(f"reflect: wrote {out} ({len(sessions)} sessions, {len(p_agg)} patterns)")


if __name__ == "__main__":
    sys.exit(main())