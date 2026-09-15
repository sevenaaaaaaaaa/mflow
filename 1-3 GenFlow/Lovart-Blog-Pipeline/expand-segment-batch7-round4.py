#!/usr/bin/env python3
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## Implementation Checklist"
MIN_WORDS = 2000

CASE = {
    "segment-ai-design-authors-publishers.md": """
### Case walkthrough: indie thriller launch in fourteen days

Day 1–2: Genre research prompts in **Thinking Mode** produce four cover directions. Author picks direction; lock palette in **Brand Kit**. Day 3–5: Finalize title typography with **Text Edit** after copyedit. Day 6–8: Amazon ad sizes, Facebook placements, and newsletter hero from one mockup scene. Day 9–10: Audiobook retailer banner and social quote templates. Day 11–12: Bookstore signing poster and bookmark. Day 13–14: QA all exports, spell-check every **Text Edit** layer, upload to ads manager.

This cadence is impossible when each asset requires a separate designer booking. Lovart collapses parallel work into one governed project.

### Rights and distributor hygiene

Keep a changelog of cover versions tied to ISBN metadata. Retailers reject mismatched titles. Export archive ZIP per title: cover, ads, social, print.

""",
    "segment-ai-design-beauty-skincare-brands.md": """
### Case walkthrough: serum launch across DTC and retail

Week 1 establishes bottle **Identity Lock** and marble hero scene. Week 2 generates retailer grid and influencer kit. Week 3 produces clinical claim layouts with blank legal zones for regulatory pass. Week 4 launches paid social matrix—nine ads from three hooks. **Touch Edit** swaps shade swatches for EU SKU differences without reshooting.

Measure CPA per hook; retire losers; **Text Edit** new headlines on winners.

### Sampling and GWP

Gift-with-purchase cards and insert cards share Brand Kit; batch before fulfillment center deadline.

""",
    "segment-ai-design-event-planners.md": """
### Case walkthrough: corporate gala in three weeks

Week 1: identity and invitation PDF. Week 2: sponsor program, wayfinding, table numbers, volunteer badges. Week 3: day-of AV holds, Instagram recap frames, thank-you email hero. Rain plan signage pre-exported.

Sponsor changes hit **Text Edit** on program spreads hours before print—no full InDesign rebuild.

### Load-in coordination

Number files by install order: `01_registration`, `02_stage`, etc. Vendors on site lose less time searching email threads.

""",
    "segment-ai-design-interior-designers.md": """
### Case walkthrough: residential pitch in five days

Day 1: client intake → mood direction. Day 2–3: three room concepts plus material board. Day 4: **Touch Edit** furniture swaps from feedback call. Day 5: PDF deck + optional **Upscale** prints for client meeting.

Winning pitches often include one "hero moment" render—dining at dusk, primary suite, or kitchen island scene—supported by consistent typography across slides.

### Post-win production

After contract, shift from sales renders to documentation handoff; Lovart remains useful for client updates during construction.

""",
    "segment-ai-design-podcasters.md": """
### Case walkthrough: show rebrand before season launch

Archive old art. Build master cover with legibility tests. Roll episode template. Produce launch trailer stills + **Seedance 2.0** motion bumpers. Ship media kit to sponsors.

Cross-post to YouTube podcast with matching thumbnails—algorithm rewards consistency.

### Monetization assets

Patreon tier icons, affiliate ad read graphics, and live show posters share one ChatCanvas project named by season.

""",
    "segment-ai-design-nonprofits-donations.md": """
### Case walkthrough: year-end campaign

October: creative brief and Brand Kit refresh. November week 1: Giving Tuesday hero + email. Week 2: peer-to-peer toolkit. Week 3: reminder series. Week 4: thank-you and impact report teaser.

Impact numbers come from programs team; design never invents statistics.

### Board preview

Export PDF storyboard of campaign sequence for board approval before media spend goes live.

""",
    "segment-ai-design-restaurants-cafes.md": """
### Case walkthrough: seasonal menu change

Friday kitchen finalizes dishes. Saturday morning Lovart session: menu PDF, table tents, delivery thumbs, Stories. Saturday afternoon manager sign-off. Sunday night social tease. Monday lunch live.

Speed beats competitors still waiting on agency revisions.

### Off-season brand building

Winter is for brand storytelling: chef portraits, supplier stories, cocktail culture content—maintain engagement between LTOs.

""",
}


def main():
    for fname, block in CASE.items():
        path = OUT / fname
        t = path.read_text(encoding="utf-8")
        w = len(t.split())
        if w >= MIN_WORDS:
            print(f"{fname}: {w} ok")
            continue
        if "### Case walkthrough:" in t:
            print(f"{fname}: already has case")
            continue
        if MARKER not in t:
            print(f"{fname}: no marker")
            continue
        t = t.replace(MARKER, block.strip() + "\n\n" + MARKER, 1)
        path.write_text(t, encoding="utf-8")
        print(f"{fname}: {len(t.split())} words")


if __name__ == "__main__":
    main()
