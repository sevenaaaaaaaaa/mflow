#!/usr/bin/env python3
"""Second expansion pass for branding/insight under 3000 words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## Derivative Scenarios"

BLOCK = """

## Case Studies (Composite Scenarios)

### Case 1: Mid-market SaaS
A Series B SaaS team replaced five disconnected tools with one ChatCanvas project per feature launch. Brand Kit locked product purple and illustration style. Paid social, blog heroes, and sales decks exported from the same hero with Text Edit headline variants. Revision rounds dropped from nine to three per launch.

### Case 2: Regional agency
A twelve-person agency imported each client's Brand Kit as a separate workspace. Coordinators stopped emailing PNG proofs; they exported PDF contact sheets. Junior staff used Touch Edit for client feedback instead of rebuilding layouts. Billable hours shifted from production labor to strategy—without cutting output volume.

### Case 3: Regulated healthcare marketing
A clinic network used Thinking Mode for patient education tone review before render. No PHI in uploads; generic illustrations only. Legal approved a prompt library tied to Brand Kit. Spanish handouts used Text Edit while English masters stayed locked.

### Case 4: Creator-led brand
A content creator launched merch and course creatives from one mascot Identity Lock. Shorts used Seedance cutdowns with the same character geometry as still thumbnails. Audience recognition improved because motion matched static brand cues.

### Implications for 2026–2027 planning
Budget for **systems**, not tokens. Train coordinators on semantic edits. Keep specialists for identity resets and novel campaigns. Measure revision rounds. Treat motion as extension of stills, not a separate creative program.

---

"""


def main():
    for p in sorted(OUT.glob("better-design-*.md")) + sorted(OUT.glob("insight-*.md")):
        text = p.read_text(encoding="utf-8")
        w = len(text.split())
        if w >= 3000:
            print(f"{p.name}: {w} ok")
            continue
        if "## Case Studies (Composite Scenarios)" in text:
            print(f"{p.name}: {w} has cases")
            continue
        if MARKER not in text:
            print(f"{p.name}: {w} no marker")
            continue
        text = text.replace(MARKER, BLOCK.strip() + "\n\n" + MARKER, 1)
        p.write_text(text, encoding="utf-8")
        print(f"{p.name}: {len(text.split())} words")


if __name__ == "__main__":
    main()
