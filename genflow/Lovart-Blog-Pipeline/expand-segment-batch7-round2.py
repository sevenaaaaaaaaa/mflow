#!/usr/bin/env python3
"""Second expansion pass — insert before FAQ to reach 2000+ words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## FAQ"

COMMON = """
## Lovart Platform Notes for {industry_label}

### Fast Mode vs Thinking Mode

Use **Fast Mode** when you are iterating visual options: layout sketches, color directions, social sizes. Switch to **Thinking Mode** when the brief includes constraints—regulatory tone, sponsor logo rules, genre conventions, or multi-step campaigns. **MCoT (Mind Chain of Thought)** surfaces a plan you can edit before pixels burn credits.

### Model routing without model loyalty

Lovart is inference-agnostic: **Nano Banana Pro** for photoreal product and portrait work, **Nano Banana 2** for crisp type, **Seedream** for dense layouts, **Seedance 2.0** and **Veo 3** for motion. The **Design Agent** selects routes; you override when you know the job.

### Commercial rights and client work

Paid plans include commercial use per current [Lovart pricing](https://lovart.ai/pricing) terms. For client services, document that deliverables were AI-assisted if contracts require it. Start trials at [Lovart signup](https://lovart.ai/signup).

### Export checklist

Before handoff: confirm resolution, color profile notes for print, font legibility at smallest size, and alt text for accessibility. **Upscale** for banners; export PSD when vendors edit type.

### Onboarding path

New teams should complete the [ChatCanvas getting started guide](/blog/05-pillar-getting-started-lovart), then configure [Brand Kit for every industry](/blog/complete-guide-brand-kit-every-industry-lovart) before batch production.

[IMAGE 4 PLACEHOLDER — Lovart Thinking Mode plan panel before generation]

"""

EXTRA = {
    "segment-ai-design-dental-clinics.md": ("Dental Clinics", """
### Insurance and benefits seasonality

Open enrollment and benefits reminders compete for attention each fall. Pre-build templates in August so September emails ship on time. Visual consistency increases recall when patients confuse multiple provider letters.

### Pediatric vs adult sub-brands

Use illustration-forward templates for pediatric spaces without contaminating adult implant marketing. Separate ChatCanvas folders, shared corporate logo rules only.

### Reputation management

Review request cards and social thank-you posts should match office photography style—patients post them online, extending brand reach.

### Emergency closure graphics

Snow day and closure announcements need pre-approved templates. **Text Edit** updates dates; publish to Google Business and Instagram within minutes.
"""),
    "segment-ai-design-agent-law-firms.md": ("Law Firms", """
### Practice area landing pages

Each practice group needs distinct hero imagery while sharing firm typography. Build six master heroes; rotate on the website quarterly via CMS uploads.

### Diversity and inclusion communications

Representation matters in recruiting visuals. Prompt for inclusive photography styles; avoid tokenism by pairing visuals with substantive program copy written by HR.

### Crisis communications

Pre-draft neutral holding statement graphics—not sensational. Partner approval still required; Lovart accelerates layout only.

### Alumni and event reunions

Reunion materials often lag brand updates. Run old logos through **Brand Kit** refresh templates before printing nametags.
"""),
    "segment-ai-design-nonprofits-donations.md": ("Nonprofits", """
### Grant vs public messaging

Foundations want data; public donors want story. Maintain two template families under one **Brand Kit** color system.

### Legacy society communications

Major donor societies expect premium print. **Upscale** covers and foil-simulated gradients for PDF proofs before physical proofs.

### Advocacy campaigns

Policy advocacy needs clear typographic hierarchy for calls to action. Test mobile legibility—many supporters read on phones in transit.

### Merchandise for walks and runs

T-shirt designs with event year badges sell nostalgia. **Text Edit** updates year and city annually.
"""),
    "segment-ai-design-restaurants-cafes.md": ("Restaurants", """
### Health inspection and certification badges

Display ServSafe or local equivalent on hiring posts—not on food heroes where they clutter appetite cues.

### Allergen communication

Icons for gluten-free or vegan LTOs should follow a consistent icon set stored in **Brand Kit** references.

### Partnership co-marketing

Brewery collabs and influencer takeovers need co-logo templates with legal clearance zones.

### Seasonal patio openings

Exterior signage and Instagram Reels covers should launch the same day—batch in one session.
"""),
    "segment-ai-design-beauty-skincare-brands.md": ("Beauty Brands", """
### Sampling and trial sachets

Micro packaging graphics repeat at scale—Identity Lock on primary bottle shape for line consistency.

### Retailer endcaps

Endcap visuals are violent competition. High contrast, three-word benefit, product centered.

### Dermatologist co-sign campaigns

Leave credential text zones for MD quotes; legal reviews partner titles carefully.

### Sustainability claims

Eco icons and refill messaging need accurate copy—visual leaf icons do not substitute for substantiation.
"""),
    "segment-ai-design-interior-designers.md": ("Interior Designers", """
### Contractor coordination sheets

Export labeled elevation callouts for trades—even when conceptual, they align field conversations.

### Staging for vacant units

Developers need quick staging renders for leasing. Speed wins listings.

### Lighting studies

Request morning vs evening versions with **Touch Edit** on window glow—not full rerenders.

### Sustainability storytelling

Material eco labels on boards increasingly win corporate clients.
"""),
    "segment-ai-design-podcasters.md": ("Podcasters", """
### Cross-promotion swaps

Swap show art templates with partner podcasts—dual logo safe zones prevent awkward crops.

### Transcription clips

Quote cards from episodes need transcript accuracy—pull text from your editor, paste via **Text Edit**.

### Network ad sales

Produce a media kit PDF: downloads, demographics, cover art, sample clips stills.

### Live streaming overlays

OBS-ready PNG overlays with transparent safe zones for chat widgets.
"""),
    "segment-ai-design-authors-publishers.md": ("Authors and Publishers", """
### Book fair materials

Booth banners and signing table cards share event **Brand Kit** for consortia publishers.

### Reading group guides

PDF discussion guides with chapter art headers increase book club adoption.

### Award submissions

Copy-specific award logos onto submission covers using **Touch Edit** placement zones.

### Reprint and anniversary editions

Anniversary badges on covers refresh backlist without full redesign costs.
"""),
    "segment-ai-design-event-planners.md": ("Event Planners", """
### RFID and digital check-in

Wayfinding integrates with apps—QR art must scan. Test contrast and quiet zone.

### Catering cards

Dietary icon sets (vegan, halal, nuts) consistent across menus and place cards.

### Sustainability events

Digital-first invitations reduce print; keep PDF versions for sponsors who require paper.

### Multi-day conferences

Day-specific color accents help attendees navigate tracks while staying on brand.
"""),
}


def main():
    for fname, (label, extra) in EXTRA.items():
        path = OUT / fname
        text = path.read_text(encoding="utf-8")
        if "## Lovart Platform Notes for" in text:
            print(f"SKIP {fname}")
            continue
        block = COMMON.format(industry_label=label) + extra
        text = text.replace(MARKER, block.strip() + "\n\n" + MARKER, 1)
        path.write_text(text, encoding="utf-8")
        print(f"{fname}: {len(text.split())} words")


if __name__ == "__main__":
    main()
