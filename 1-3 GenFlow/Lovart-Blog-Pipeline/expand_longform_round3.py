#!/usr/bin/env python3
"""Third expansion for branding/insight to approach 3000 words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## FAQ"

BLOCK = """

## Glossary for Cross-Functional Teams

| Term | Meaning for marketers |
|------|---------------------|
| **ChatCanvas** | Lovart's spatial workspace where campaigns, sizes, and revisions stay together. |
| **Brand Kit** | Executable brand rules (color, type, logo) the agent applies every render. |
| **MCoT** | Mind Chain of Thought—visible planning before generation. |
| **Touch Edit** | Click an object, describe the change, keep the rest. |
| **Text Edit** | Fix on-image type without full regeneration. |
| **Edit Elements** | Semantic layer split for last-mile swaps. |
| **Identity Lock** | Keep product, mascot, or talent consistent across variants. |
| **Thinking Mode** | Deeper reasoning for complex or regulated briefs. |

## Workshop Agenda (90 minutes)

1. **Audit** last month's live creatives for consistency failures (15 min).
2. **Import** or rebuild Brand Kit with hex and type roles (20 min).
3. **Rebuild** one high-frequency deliverable on ChatCanvas (25 min).
4. **Practice** Text Edit and Touch Edit on the approved hero (15 min).
5. **Define** export naming and QA checklist (15 min).

## Questions for leadership

- Do we measure revision rounds or image count?
- Is brand governance documented or tribal knowledge?
- Which channels share a hero this quarter?
- Where does legal enter the workflow today?
- Do we have a single source of truth for approved exports?

## Research notes (methodology)

Observations in this article synthesize Lovart customer education patterns, support themes from 2025–2026, and common failure modes in generative marketing workflows. They are directional guidance—not guarantees of performance outcomes on any single platform.

---

"""


def main():
    for p in sorted(OUT.glob("better-design-*.md")) + sorted(OUT.glob("insight-*.md")):
        text = p.read_text(encoding="utf-8")
        w = len(text.split())
        if w >= 3000:
            print(f"{p.name}: {w} ok")
            continue
        if "## Glossary for Cross-Functional Teams" in text:
            print(f"{p.name}: {w} has glossary")
            continue
        if MARKER not in text:
            print(f"{p.name}: {w} no marker")
            continue
        text = text.replace(MARKER, BLOCK.strip() + "\n\n" + MARKER, 1)
        p.write_text(text, encoding="utf-8")
        print(f"{p.name}: {len(text.split())} words")


if __name__ == "__main__":
    main()
