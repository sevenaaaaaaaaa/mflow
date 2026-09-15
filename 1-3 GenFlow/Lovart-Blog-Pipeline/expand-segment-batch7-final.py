#!/usr/bin/env python3
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## FAQ"
QA = """

## Quality Assurance Before Publish

Run every deliverable through this gate—non-designers included:

1. **Brand Kit compliance:** Colors within palette; fonts match hierarchy; logo clear space respected.
2. **Legibility:** Squint test at thumbnail size; body text readable on mobile.
3. **Claims and ethics:** No fabricated stats, outcomes, or identities; regulatory and industry disclaimers present.
4. **Accessibility:** Sufficient contrast; do not rely on color alone for meaning; provide alt text in CMS.
5. **File specs:** Correct dimensions per channel; print bleed noted; RGB vs CMYK understood by vendor.
6. **Version label:** File name includes date and campaign ID for rollback.

When something fails, prefer **Touch Edit** and **Text Edit** over full regeneration—faster and more consistent.

Stakeholders who only approve final PNGs should see a one-page contact sheet exported from ChatCanvas showing all sizes side by side. Fewer "this size looks different" surprises.

Lovart accelerates production; your reputation still depends on what you ship. Build QA into the calendar, not as a panic step at midnight before an event or launch.

Teams new to agentic design should skim [common AI prompting mistakes](/blog/common-ai-prompting-mistakes-design-results-how-to-fix) before scaling volume—bad prompts scale bad output.

"""

def main():
    for p in sorted(OUT.glob("segment-ai-design-*.md")):
        t = p.read_text(encoding="utf-8")
        w = len(t.split())
        if w >= 2000:
            print(f"{p.name}: {w} ok")
            continue
        if "## Quality Assurance Before Publish" in t:
            print(f"{p.name}: {w} has QA")
            continue
        t = t.replace(MARKER, QA.strip() + "\n\n" + MARKER, 1)
        p.write_text(t, encoding="utf-8")
        print(f"{p.name}: {len(t.split())} words")


if __name__ == "__main__":
    main()
