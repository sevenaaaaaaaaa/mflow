#!/usr/bin/env python3
"""Expand branding/insight drafts under 3000 words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## What Practitioners Should Do Next"

BLOCK = """

## Extended Analysis: Systems vs Tools

The market still markets "AI art" as magic buttons. Production teams know better: marketing is a **system** of briefs, approvals, exports, and analytics feedback. A tool that only generates images optimizes the wrong step if Brand Kit, semantic edits, and multi-format export are external.

### Design Context Core
Think of Brand Kit plus ChatCanvas project history as your **Design Context Core**—the memory that should survive employee turnover and agency changes. When a new contractor arrives, they should open one project, not twelve Slack threads of PNGs.

### Economics of revision
Each full regeneration costs time and credits; each **Text Edit** costs minutes. Teams that learn semantic edits first report higher satisfaction than teams chasing the newest model name. Model loyalty is a vendor story; revision discipline is a margin story.

### Motion as an extension of stills
Motion should inherit color, type, and subject lock from still heroes—not restart creative direction in a separate video tool. Seedance 2.0 and Veo 3 inside Lovart exist to continue the same campaign brain, not to invent a second brain.

### Cross-functional alignment
Legal cares about claims. Brand cares about palette. Performance cares about variable isolation. Product cares about screenshot accuracy. A Design Agent workflow surfaces conflicts early via Thinking Mode plans stakeholders can comment on before render.

### What to measure in Q3–Q4 2026
- Time from brief to approved export pack
- Revision rounds per hero
- Percent of assets exported from a single ChatCanvas project
- Incidents of off-brand publishes (should fall)

### Further reading on Lovart
- [Edit Elements vs outdated habits](/blog/how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits)
- [Touch Edit best practice](/blog/touch-edit-best-practice-3-gestures-lovart)
- [Batch social content](/blog/batch-generate-30-days-social-media-content-ai)
- [Composition rules](/blog/composition-rules-design-rule-of-thirds-golden-ratio)
- [Typography 101](/blog/typography-101-font-pairing-rules-non-designers)

---

"""


def main():
    for p in sorted(OUT.glob("better-design-*.md")) + sorted(OUT.glob("insight-*.md")):
        text = p.read_text(encoding="utf-8")
        w = len(text.split())
        if w >= 3000:
            print(f"{p.name}: {w} ok")
            continue
        if "## Extended Analysis: Systems vs Tools" in text:
            print(f"{p.name}: {w} expanded")
            continue
        if MARKER not in text:
            print(f"{p.name}: {w} no marker")
            continue
        text = text.replace(MARKER, BLOCK.strip() + "\n\n" + MARKER, 1)
        p.write_text(text, encoding="utf-8")
        print(f"{p.name}: {len(text.split())} words")


if __name__ == "__main__":
    main()
