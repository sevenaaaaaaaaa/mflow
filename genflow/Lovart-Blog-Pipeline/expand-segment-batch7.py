#!/usr/bin/env python3
"""Insert expansion blocks before Derivative Scenarios to reach 2000+ words."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "01-Drafts"
MARKER = "## Derivative Scenarios"

EXPANSIONS = {
    "segment-ai-design-dental-clinics.md": """

## Part 4: Operational Playbooks for Dental Groups

### Monday morning production rhythm

Block ninety minutes for marketing production—not scattered five-minute tasks between patients. In **ChatCanvas**, open your practice **Brand Kit** project. Queue: one education graphic, two social posts, one Google Business update. Use **Fast Mode** for drafts; switch to **Thinking Mode** when a campaign needs clinical tone review (implant consults vs pediatric fun).

### Multi-location governance

DSOs often ship corporate palettes that feel cold at the neighborhood office. Solve with layered **Brand Kit** notes: corporate logo placement rules (top-right, minimum clear space) plus local photography prompts ("show our actual front desk team style, not models"). Export a **PDF brand one-pager** for each office manager so vendors stop improvising.

### Vendor handoff without rework

Print shops reject RGB files and low-resolution logos weekly. Export PNG at 300 DPI effective size using **Upscale**. Package PSD layers when the shop requests editable headlines for bilingual inserts. Your front desk should never re-type phone numbers in WordArt again.

### Measuring what matters

Track cost per booked consult from Meta and Google, not likes. A/B headline zones on the same hero image using **Touch Edit** to swap offers ("$99 whitening consult" vs "free electric toothbrush with cleaning"). Keep the visual constant; test copy in **Text Edit** so performance data stays clean.

### Integrating with your patient communication stack

Lovart does not replace your PMS or email platform—it feeds them. Export heroes sized for Mailchimp, rectangles for SMS MMS limits, and square crops for Instagram. Consistent visuals increase recognition when the reminder text arrives.

### When to escalate to a human designer

Rebrand launches, full website UI, and complex implant brochures may still need an agency. Lovart wins on **velocity and volume** after identity exists. Hybrid stacks are normal: agency sets strategy, Lovart runs weekly production.

---

## Prompt Library (Dental)

| Use case | Starter prompt |
|----------|----------------|
| New patient welcome | "Postcard front: welcoming family dental, Brand Kit, soft photography, 'Your first visit' headline zone." |
| Implant consult | "Consult room poster: calm explainer icons, no gore, Brand Kit, premium but approachable." |
| Team hiring | "We're hiring hygienist Instagram graphic, Brand Kit, friendly team photo style." |
| Review request | "Thank-you card insert graphic, five-star prompt, QR zone, Brand Kit." |

For agent behavior fundamentals, see [how to chat and generate any design type](/blog/how-to-chat-generate-any-design-type-lovart-agent).

[IMAGE 3 PLACEHOLDER — Weekly dental marketing production calendar on ChatCanvas]

""",
    "segment-ai-design-agent-law-firms.md": """

## Part 4: Governance and Production Standards

### Marketing committee approvals

Assign a partner sponsor and a marketing ops owner. Lovart projects should live in shared folders with naming conventions: `ClientAlert_2026-06_Template_v3`. Version chaos destroys billable trust.

### Disclaimer blocks as first-class layout zones

Build master templates with locked footer bands: "This material is not legal advice," jurisdiction lines, and required bar numbers. **Text Edit** updates matter names on seminar slides without touching backgrounds.

### Lateral recruiting at scale

Twenty lateral announcements per year is a design bottleneck. Template: attorney portrait left, credentials right, practice group color accent from **Brand Kit**. Batch exports for LinkedIn, firm website, and internal intranet.

### Conflict-conscious imagery

Avoid prompts that imply specific outcomes, gavels on fire, or courtroom drama unless litigation brand intentionally uses them. **Thinking Mode** prompt: *"Conservative financial institution audience; no aggressive metaphors."*

### Knowledge management tie-in

Store approved Lovart exports in your DMS with metadata. Future pitches reuse tone, not just pixels.

---

## Prompt Library (Law)

| Use case | Starter prompt |
|----------|----------------|
| Client alert | "One-page PDF alert layout, firm Brand Kit, headline zone, body text columns, disclaimer footer." |
| Practice group brochure | "Tri-fold services brochure, corporate M&A, navy palette, icon row for capabilities." |
| Pro bono report | "Annual pro bono impact cover, dignified photography style, Brand Kit." |
| Podcast sponsorship | "Hosted podcast ad graphic, 3000x3000, logo safe zones." |

Learn semantic editing for last-minute partner edits: [Edit Elements best practices](/blog/how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits).

[IMAGE 3 PLACEHOLDER — Law firm template library with disclaimer footers locked]

""",
    "segment-ai-design-nonprofits-donations.md": """

## Part 4: Campaign Architecture for Development Teams

### The campaign brief sheet

Before opening Lovart, document: audience segment, offer, proof points, channels, and ethical photo rules. Feed that paragraph into **Thinking Mode** so MCoT plans assets coherently—not as isolated images.

### Sustainer vs acquisition visuals

Monthly donors respond to impact proof; acquisition audiences need problem-solution clarity. Use different hero templates but one **Brand Kit**. Never mix emotional tones on the same landing page.

### Board-ready reporting

Annual reports are design-heavy and deadline-brutal. Generate divider pages, pull-quote layouts, and photo essays from text outlines. Partners add audited numbers; you own layout velocity.

### Corporate partnership kits

Co-brand templates with sponsor logo girds. **Touch Edit** updates sponsor lockups per event without redesigning gala programs.

### Volunteer enablement

Train volunteers on three approved templates only. Creativity within guardrails beats chaos.

---

## Prompt Library (Nonprofit)

| Use case | Starter prompt |
|----------|----------------|
| Monthly appeal | "Email hero: sustainer thank-you, warm photography, Brand Kit, donate CTA zone." |
| Volunteer drive | "Poster: volunteer orientation date, inclusive photography, Brand Kit." |
| Program launch | "Instagram carousel slide 1: new youth program, hopeful tone, no stereotypes." |
| Grant summary | "One-page impact snapshot for foundation, large numerals, Brand Kit." |

Pair with [nano banana consistent results](/blog/nano-banana-consistent-results-lovart-best-practice) when repeating mascot or icon characters across campaigns.

[IMAGE 3 PLACEHOLDER — Nonprofit campaign brief to asset set workflow diagram]

""",
    "segment-ai-design-restaurants-cafes.md": """

## Part 4: Multi-Channel Restaurant Operations

### The weekly LTO cadence

Kitchen calendar drives creative. Sunday: confirm specials. Monday: generate hero + social + table tent in one **ChatCanvas** session. Tuesday: manager approval. Wednesday: live. Lovart compresses what used to be a Friday panic.

### Delivery marketplace specs

Document crop ratios per platform in your **Brand Kit** internal notes. Uber Eats, DoorDash, and Grubhub differ—generate all from one master dish photo with **Touch Edit** background swaps.

### Franchise and multi-unit operators

Corporate **Brand Kit** with local insert zones: city name, store photo, regional LTO. Franchisees cannot change logo colors; they can select approved specials from dropdown templates you maintain.

### Catering sales enablement

B2B catering is high margin; visuals close deals. One-sheet PDFs with package tiers, **Smart Mockup** buffet photos, and testimonial blocks.

### Training and hiring

Uniform badges, training manual covers, and hiring flyers should match dining room aesthetic—reduces cultural drift for new staff.

---

## Prompt Library (Restaurant)

| Use case | Starter prompt |
|----------|----------------|
| Daily special chalkboard | "Chalkboard style special board, hand-lettered feel, Brand Kit colors, item name zone." |
| Wine pairing | "Table tent wine pairing, elegant minimal, Brand Kit, 4x6 print." |
| Loyalty program | "Punch card graphic, brand mascots optional, print-ready." |
| Ghost kitchen brand | "Delivery-only brand logo, bold readable on dark app backgrounds." |

See [Touch Edit best practice](/blog/touch-edit-best-practice-3-gestures-lovart) for quick garnish and color fixes on food heroes.

[IMAGE 3 PLACEHOLDER — Restaurant LTO weekly cadence from kitchen calendar to live ads]

""",
    "segment-ai-design-beauty-skincare-brands.md": """

## Part 4: DTC Beauty Launch Mechanics

### Shade rollout factory

When shade 16 launches, duplicate Identity Lock bottle scenes, **Touch Edit** swatch labels, and regenerate retailer grids. Document hex codes in **Brand Kit** per shade family.

### Clinical vs lifestyle sub-lines

Clinical SKUs need white space and ingredient callouts; lifestyle SKUs allow bolder set design. Sub-palettes under one parent kit prevent brand schizophrenia.

### Retailer compliance packets

Build templates with mandatory legal zones left blank for regulatory affairs. Speed approvals by separating "locked layout" from "editable claims."

### Creator seeding at scale

Export Canva-friendly PNG sets if creators insist—or keep them in Lovart templates with **Text Edit** for their codes. Track which template drives highest affiliate CTR.

### Post-purchase email visuals

Unboxing inserts, reorder reminders, and educational drips should match Amazon hero aesthetics—customers notice disconnect.

---

## Prompt Library (Beauty)

| Use case | Starter prompt |
|----------|----------------|
| Routine carousel | "Instagram carousel: 3-step routine, bottles Identity Lock, Brand Kit, educational tone." |
| Press kit | "Press page hero, product line on gradient, logo zone, high-res export." |
| Subscription box | "Unboxing insert card, minimal type, Brand Kit, thank-you message zone." |
| SPF campaign | "Summer SPF launch banner, beach light, product center, regulatory placeholder footer." |

[IMAGE 3 PLACEHOLDER — Beauty shade rollout grid with Identity Lock bottles]

""",
    "segment-ai-design-interior-designers.md": """

## Part 4: Studio Business Development

### Proposal win rate

Clients hire confidence. Decks with cohesive renders outperform mood-board collages scraped from Pinterest. Lovart is a sales accelerant, not just a styling toy.

### Phased deliverable mapping

Concept phase: atmospheric renders. Design development: material boards. Construction: partner with CAD vendor—do not promise permit drawings from AI alone.

### Photographer collaboration

Shoot key spaces; use Lovart to test furniture options before purchase orders. Reduces costly returns.

### Hospitality vs residential tone

Hotels need durability cues and brand standards; homes need warmth. Encode separate prompt libraries in **Brand Kit** notes per practice area.

### Fee justification

Bill visual production as a line item. Clients understand "presentation package" fees easier than hidden hours in "design."

---

## Prompt Library (Interior)

| Use case | Starter prompt |
|----------|----------------|
| Powder room | "Small powder room concept, dramatic wallpaper, brass fixtures, photoreal." |
| Outdoor living | "Patio concept at dusk, string lights, fire pit, Brand Kit frame." |
| Office reception | "Corporate reception, logo wall zone, calm neutrals, people-scale cues." |
| Material board | "Flat lay material board: stone, wood, fabric swatches, labeled." |

[IMAGE 3 PLACEHOLDER — Interior design proposal deck flow from concept to contract]

""",
    "segment-ai-design-podcasters.md": """

## Part 4: Growth and Monetization Visuals

### Platform-specific safe zones

Apple Podcasts, Spotify, and YouTube each crop differently. Test cover art at 55px, 300px, and full bleed. Lovart exports multiple crops from one master.

### Guest workflow

Send guests a branded question card template and optional video frame before recording. They arrive on-brand; your editor saves time.

### Merch and Patreon tiers

Tier icons, Discord banners, and Patreon headers should match show **Brand Kit**. Fans recognize you across ecosystems.

### Ad read graphics

Host-read ads need simple lower-thirds: sponsor logo, promo code zone, Brand Kit colors. Batch per season.

### Network shows

Multiple hosts? **Identity Lock** each face treatment while varying episode titles.

---

## Prompt Library (Podcast)

| Use case | Starter prompt |
|----------|----------------|
| Season launch | "Season 3 cover badge overlay on master art, Brand Kit." |
| Clip thumbnail | "YouTube clip thumb, bold 6-word title zone, host photo Identity Lock." |
| Live show | "Venue poster, date city list, QR zone, Brand Kit." |
| Newsletter | "Substack header, wide crop, show logo left, mood background." |

[IMAGE 3 PLACEHOLDER — Podcast distribution crop guide Apple Spotify YouTube]

""",
    "segment-ai-design-authors-publishers.md": """

## Part 4: Publishing Operations

### Imprint-level Brand Kits

Publishers manage multiple authors. Parent imprint kit + per-series sub-kits prevent cover chaos across lists.

### Metadata alignment

Title, subtitle, and series number must match retailer metadata. **Text Edit** after copydesk approval—never ship placeholder lorem.

### International editions

Cover art may stay; typography changes per language. Regenerate spine widths for translated title lengths.

### Audiobook and podcast cross-promo

Unified visual world across print, audio retailer pages, and author social—listeners and readers should recognize one brand.

### Backlist revitalization

Refresh covers for backlist titles with modern genre grammar while **Identity Lock** on author name placement.

---

## Prompt Library (Publishing)

| Use case | Starter prompt |
|----------|----------------|
| BookBub ad | "BookBub featured deal ad, 600x300, 3D mockup, price callout zone." |
| Author Q&A | "Instagram question sticker background, Brand Kit, book world texture." |
| Signing poster | "Bookstore signing poster, author photo zone, date time placeholders." |
| Box set | "Box set collection banner, three spines aligned, Brand Kit." |

[IMAGE 3 PLACEHOLDER — Publishing imprint hierarchy Brand Kit parent and series child]

""",
    "segment-ai-design-event-planners.md": """

## Part 4: Day-Of and Vendor Coordination

### Run-of-show graphics

Hold slides, countdown timers, and walk-in loops share event **Brand Kit**. AV team receives PNG sequences named by timestamp.

### Volunteer and staff badges

Color-code roles (VIP, staff, vendor) with consistent typography. Print on-site backup templates.

### Weather and contingency signage

Indoor redirect signs should be pre-designed, not handwritten. **Text Edit** updates room numbers in minutes.

### Post-event content

Recap templates ready before the event: hashtag frames, thank-you sponsors, save-the-date for next year.

### Budget tiers

Offer clients Good/Better/Best packages with defined asset counts—Lovart makes tier upsells credible because production is fast.

---

## Prompt Library (Events)

| Use case | Starter prompt |
|----------|----------------|
| Table number | "Table card 5x7, art deco motif, large numeral, Brand Kit." |
| Photo wall | "Step and repeat pattern, sponsor logo grid placeholders, 8x8 ft scale note." |
| Digital check-in | "iPad welcome screen, event logo, WiFi instructions zone." |
| Award ceremony | "Winner announcement slide, name zone, Brand Kit, 16:9." |

[IMAGE 3 PLACEHOLDER — Event day-of signage package table tent wayfinding stage]

""",
}


def main():
    for fname, block in EXPANSIONS.items():
        path = OUT / fname
        text = path.read_text(encoding="utf-8")
        if MARKER not in text:
            print(f"SKIP {fname}: marker missing")
            continue
        if "Part 4:" in text:
            print(f"SKIP {fname}: already expanded")
            continue
        text = text.replace(MARKER, block.strip() + "\n\n" + MARKER, 1)
        path.write_text(text, encoding="utf-8")
        print(f"Expanded {fname} -> {len(text.split())} words")


if __name__ == "__main__":
    main()
