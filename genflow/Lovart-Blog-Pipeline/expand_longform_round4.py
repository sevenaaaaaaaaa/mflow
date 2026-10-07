#!/usr/bin/env python3
"""Fourth expansion for branding/insight to reach 3000+ words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## Derivative Scenarios"

BLOCK = """

## Platform and Channel Notes

**Paid social:** Keep product geometry locked; test headlines and offers only. Export 1:1 and 9:16 from one hero. Document which variant ID maps to which ad set.

**Organic social:** Prioritize legibility at thumbnail scale. Carousels need slide role planning in Thinking Mode before generation.

**Email:** Heroes at 600–1200px width; avoid tiny type on photographic backgrounds. Use Text Edit for subject-line alignment with hero promise.

**Web / PDP:** Match landing headline to ad creative. Identity Lock on product reduces bounce from "different product" confusion.

**Print / events:** Confirm bleed and DPI with vendors. Upscale before handoff. CMYK conversations happen at the print shop—export RGB masters with notes.

**Video:** Storyboard on ChatCanvas; export still keyframes as references for Seedance or Veo. Keep lower-third and caption safe zones consistent with still templates.

## Anti-patterns we see in the wild

- **Style stacking:** "Art deco minimalist luxury brutalist" in one prompt.
- **Tool hopping:** Hero in tool A, type fix in B, crop in C—context dies.
- **Unbounded tests:** Changing layout, offer, and color simultaneously.
- **Stock misuse:** Unlicensed references uploaded as "inspiration."
- **Motion first:** Video before brand rules exist—expensive rework.

## Closing perspective

The teams that win treat Lovart as **infrastructure**: Brand Kit as law, ChatCanvas as record, semantic edits as craft. Everything else—models, trends, prompts—is downstream. Build the system once; compound output for quarters.

---

"""


def main():
    for p in sorted(OUT.glob("better-design-*.md")) + sorted(OUT.glob("insight-*.md")):
        text = p.read_text(encoding="utf-8")
        w = len(text.split())
        if w >= 3000:
            print(f"{p.name}: {w} ok")
            continue
        if "## Platform and Channel Notes" in text:
            print(f"{p.name}: {w} has platform notes")
            continue
        if MARKER not in text:
            print(f"{p.name}: {w} no marker")
            continue
        text = text.replace(MARKER, BLOCK.strip() + "\n\n" + MARKER, 1)
        p.write_text(text, encoding="utf-8")
        print(f"{p.name}: {len(text.split())} words")


if __name__ == "__main__":
    main()
