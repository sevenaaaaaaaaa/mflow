#!/usr/bin/env python3
"""Expand how-to drafts under 1800 words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## Derivative Scenarios"

BLOCK = """

## Deep Dive: Production Calendar Integration

Slot Lovart production into the same calendar as copy and media buying—not as a rescue step on publish day. **Monday** locks Brand Kit and channel specs; **Tuesday** approves hero; **Wednesday** generates size variants; **Thursday** optional motion; **Friday** QA export pack with filenames your DAM expects.

### Handoff to ads managers
Export a contact sheet PDF from ChatCanvas listing every size, headline variant, and CTA. Media buyers should not guess which PNG belongs to which placement. Include hex codes in the cover email when platforms compress colors.

### Handoff to developers
For PDP or landing page updates, export 2x PNG heroes and document alt text in the CMS. Developers need dimensions, not adjectives.

### Analytics feedback loop
When a variant wins, duplicate the artboard as `winner-v1` and iterate one variable. Losers stay archived for audit—not deleted—so teams learn what failed without re-prompting from memory.

### Working with agencies
Agencies can work inside your Brand Kit project as collaborators while you retain the Design Context Core. Ship them the brief, not a folder of reference Pinterest boards without hex codes.

---

"""


def main():
    for p in sorted(OUT.glob("how-to-*.md")):
        text = p.read_text(encoding="utf-8")
        w = len(text.split())
        if w >= 1800:
            print(f"{p.name}: {w} ok")
            continue
        if "## Deep Dive: Production Calendar Integration" in text:
            print(f"{p.name}: {w} already expanded")
            continue
        if MARKER not in text:
            print(f"{p.name}: {w} no marker")
            continue
        text = text.replace(MARKER, BLOCK.strip() + "\n\n" + MARKER, 1)
        p.write_text(text, encoding="utf-8")
        print(f"{p.name}: {len(text.split())} words")


if __name__ == "__main__":
    main()
