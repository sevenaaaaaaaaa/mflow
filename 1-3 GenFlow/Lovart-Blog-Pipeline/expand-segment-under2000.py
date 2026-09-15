#!/usr/bin/env python3
"""Add expansion block to segment files still under 2000 words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## Derivative Scenarios"

BLOCK = """

## Scaling Production Without Losing Trust

Teams that win with Lovart treat visual production like editorial: briefs, templates, and QA—not heroic one-off prompts. Block recurring calendar slots (weekly for social, monthly for print) and keep all assets in one **ChatCanvas** project per brand or location.

**Volume without drift:** Export a contact sheet PDF showing every size variant before stakeholders approve. When legal or compliance requests a copy change, use **Text Edit** on the affected layer instead of regenerating entire layouts—your margins and photography stay locked.

**Handoff discipline:** Name files with campaign ID and date (`2026-q2-whitening-v3-slide4.png`). Print vendors and ad platforms reject mystery downloads. For multi-vendor stacks, Lovart remains the generation layer; your DAM or PMS remains the system of record for approved finals.

**Training non-designers:** Start with Brand Kit setup, then one high-frequency deliverable (e.g., Instagram post or patient handout). Expand to video only after still workflows are stable. Link new users to [ChatCanvas getting started](/blog/05-pillar-getting-started-lovart) and [Brand Kit setup in five minutes](/blog/brand-kit-setup-5-minutes-lovart-best-practice).

**When to pause AI volume:** Rebrand launches, regulated claims, or crisis communications still deserve human creative direction. Lovart accelerates the middle—not the strategy reset.

**Measurement:** Track time-to-approved-export and revision rounds per campaign—not raw image count. Fewer rounds with Brand Kit usually beats more generations without governance.

---

"""


def main():
    for p in sorted(OUT.glob("segment-ai-design-*.md")):
        text = p.read_text(encoding="utf-8")
        w = len(text.split())
        if w >= 2000:
            print(f"{p.name}: {w} ok")
            continue
        if "## Scaling Production Without Losing Trust" in text:
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
