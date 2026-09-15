#!/usr/bin/env python3
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## FAQ"
ADD = """

## Implementation Checklist (First 30 Days)

Week one: audit existing assets—logos, colors, fonts, top ten recurring deliverables. Week two: configure **Brand Kit** and import into **ChatCanvas**. Week three: rebuild three high-frequency templates (social, print, presentation). Week four: train stakeholders on approval flow and export standards.

Document prompt winners in a shared sheet: prompt text, model used, export settings, and performance notes. Avoid reinventing successful campaigns. Assign one owner for **Brand Kit** changes; everyone else uses templates.

Schedule a monthly review: Which assets drove measurable results? Which templates aged? Retire clichéd stock directions. Refresh photography prompts seasonally.

Connect Lovart output to your analytics: UTM parameters on CTAs, unique promo codes on graphics, QR links per channel. Design without measurement is decoration.

When scaling to external vendors, send **Brand Kit** PDF plus exported masters—never raw prompts containing confidential strategy.

For teams comparing AI design agents vs single-model image tools, see [how to chat and generate any design type](/blog/how-to-chat-generate-any-design-type-lovart-agent) and [Midjourney vs Lovart](/blog/midjourney-vs-lovart-ai-design-showdown-2026).

[IMAGE 5 PLACEHOLDER — 30-day rollout checklist whiteboard style]

"""

SKIP = {"segment-ai-design-dental-clinics.md"}

def main():
    for p in sorted(OUT.glob("segment-ai-design-*.md")):
        if p.name in SKIP:
            print(p.name, len(p.read_text().split()), "(skip)")
            continue
        t = p.read_text(encoding="utf-8")
        if "## Implementation Checklist" in t:
            print(p.name, len(t.split()), "(done)")
            continue
        t = t.replace(MARKER, ADD.strip() + "\n\n" + MARKER, 1)
        p.write_text(t, encoding="utf-8")
        print(p.name, len(t.split()))


if __name__ == "__main__":
    main()
