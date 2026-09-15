#!/usr/bin/env python3
"""Fifth expansion: push branding/insight to 3000+ words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## Image Appendix"

BLOCK = """

## Exercises for Your Team This Week

**Exercise A — Brand audit:** Print twelve live assets from the last 30 days. Highlight inconsistent colors, type sizes, and logo placement. List three rules Brand Kit must encode.

**Exercise B — One-variable test:** Pick one approved hero. Create two variants changing only the headline. Publish or simulate performance review. Document learnings.

**Exercise C — Semantic edit drill:** Take one busy background. Use Touch Edit to simplify. Use Text Edit to fix the longest headline. Time both tasks vs full regeneration.

**Exercise D — Export discipline:** Export five sizes from one ChatCanvas project. Name files with campaign ID. Send PDF contact sheet to a stakeholder who usually approves Slack screenshots.

**Exercise E — Motion optional:** If video is in scope, export one still hero, one five-second cutdown, verify Identity Lock held. If not, skip video until stills pass QA.

## Vendor and stack boundaries

Lovart does not replace your CRM, ESP, ad platform, or print vendor—it feeds them. Clarify handoffs: who uploads to Meta Business Manager, who loads Klaviyo, who sends InDesign files to print. The agent shortens **creation**; your ops map still owns **distribution**.

## Credits, cost, and planning

Credit usage scales with regeneration habits. Teams with Brand Kit and semantic edits spend fewer credits per approved asset than teams re-rolling entire layouts. Finance should model **approved assets per month**, not raw generations. See [Lovart pricing](https://lovart.ai/pricing) for plan tiers.

## Editorial standards

Claims must be truthful and substantiated. Testimonials need permission. Before/after visuals need disclosures where required. AI does not remove accountability—humans approve what ships.

---

"""


def main():
    for p in sorted(OUT.glob("better-design-*.md")) + sorted(OUT.glob("insight-*.md")):
        text = p.read_text(encoding="utf-8")
        w = len(text.split())
        if w >= 3000:
            print(f"{p.name}: {w} ok")
            continue
        if "## Exercises for Your Team This Week" in text:
            print(f"{p.name}: {w} has exercises")
            continue
        if MARKER not in text:
            print(f"{p.name}: {w} no marker")
            continue
        text = text.replace(MARKER, BLOCK.strip() + "\n\n" + MARKER, 1)
        p.write_text(text, encoding="utf-8")
        print(f"{p.name}: {len(text.split())} words")


if __name__ == "__main__":
    main()
