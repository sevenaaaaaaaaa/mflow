---
title: "Export Formats Guide: PNG, SVG, PDF, Print Files — When to Use Each"
slug: 03-wiki-export-formats-guide
date: "2026-07-22"
language: en
page_type: Blog Post
category: "Lovart 101"
author: Lovart Content Team
description: "A production field guide to Lovart export formats in 2026. PNG vs JPEG vs WebP vs SVG vs PDF vs TIFF/EPS, social and ecommerce presets, print CMYK pitfalls, batch export naming, and a QA checklist that catches the wrong file before a client does."
focus_keyword: "export formats guide"
---

# Export Formats Guide: PNG, SVG, PDF, Print Files — When to Use Each

I have watched a perfect brand system die in the last mile three times this year. Once as a JPEG logo with crunchy edges. Once as an RGB "print PDF" that shifted on press. Once as a 72 PPI banner sent to a fabric printer who asked, politely, if we were joking.

Export format choice is not glamorous. It is the difference between work that survives delivery and work that looks amateur after it already left ChatCanvas. This guide is the route card I want every teammate to read before they click download.

It covers raster vs vector decisions, the formats you will actually use with Lovart in 2026, platform presets, print traps, batch naming, and a QA gate that catches the wrong file in under two minutes.

## 1. Why Export Format Matters in 2026

### TL;DR

- Pick format by job: transparency, photo, logo scale, print, motion still, email.
- SVG/PDF for scalable marks; PNG for crisp UI/text with alpha; JPEG/WebP for photos; TIFF/PDF for serious print paths.
- Never send a screen PNG to a press and hope.
- Name files with ratio + format + color space + version.
- QA the export, not only the canvas preview.

### The failure pattern

Teams obsess over generation models and ignore delivery containers. The canvas looks sharp. The export is wrong. The client sees the export. Your brand reputation lives in the export.

## 2. The Decision Tree I Actually Use

```text
Need transparency / sharp UI text?
  yes -> PNG (digital) or SVG (if true vector mark)
  no  -> continue

Photo or complex texture?
  yes -> JPEG or WebP (digital); TIFF/PDF (print path)
  no  -> continue

Logo / icon / flat illustration that must scale?
  yes -> SVG (web/app); PDF/EPS (print vendors who ask)
  no  -> continue

Going to press / packaging / large format?
  yes -> PDF/TIFF with print specs; confirm CMYK/ICC with vendor
  no  -> RGB digital formats

Email client destination?
  yes -> PNG or JPEG (SVG support is unreliable)

## 3. Raster Formats (Pixel Grids)

Raster files store pixels. Enlarge past their data and they break.

### PNG

Best for: UI, screenshots, text-heavy graphics, logos when SVG is unavailable, anything needing alpha.

Strengths: lossless, alpha, sharp edges.  
Weaknesses: heavy for photos; not a press-native format by itself.

Studio rule: if text must stay razor-sharp on a transparent social asset, PNG first.

### JPEG

Best for: photographs, lifestyle heroes, backgrounds without transparency.

Strengths: small files for photos.  
Weaknesses: artifacts around type and logos; no alpha.

Studio rule: never deliver a primary logo as JPEG.

### WebP

Best for: modern web delivery when the stack supports it.

Strengths: efficient.  
Weaknesses: some legacy email/PPT paths still hate it.

Studio rule: web performance yes; universal client handoff maybe not.

### TIFF

Best for: print pipelines and archival raster masters when vendors ask.

Strengths: high fidelity options.  
Weaknesses: huge; overkill for social.

### GIF

Best for: tiny looping UI moments, not modern brand photography.

Studio rule: gradients and photos in GIF are how banding happens.

## 4. Vector and Document Formats

### SVG

Best for: icons, logos, simple illustrations on web/app.

Strengths: infinite scale, editable paths in capable tools.  
Weaknesses: complex photoreal content does not belong here; some email clients fail.

### PDF

Best for: multi-page decks, print submission packages, "send one file" vendor drops.

Strengths: portable, can contain vector + image + fonts depending on export settings.  
Weaknesses: "PDF" is not one setting — screen PDF and print PDF are different animals.

### EPS

Still requested by some print vendors for logos. Confirm before making it your default religion. Many modern shops accept PDF.

## 5. Platform Presets That Prevent Remakes

### Social

```text
Feed square     1080x1080   PNG or JPEG
Portrait        1080x1350   PNG or JPEG
Story/Reels     1080x1920   PNG or JPEG / MP4 for motion
LinkedIn/X      follow platform current specs; keep safe margins
```

Export at the target pixel size. Do not upscale a 800px wide export and pray.

### Ecommerce

```text
PDP main        platform-specific; often JPEG on white/light
Gallery         consistent ratio set
Transparency    PNG if the channel truly supports it
Zoom            higher pixel masters help; soft JPEG logos do not
```

### Print

Talk to the vendor before you invent a "print pack." Ask:

- PDF/X profile or TIFF preference
- CMYK / ICC expectations
- bleed, slug, safe type
- minimum PPI at final size
- font outlining requirements

If the vendor cannot answer, find another vendor.

## 6. Lovart Export Workflow (Context → Conversion)

1. Context: know destination before you generate.
2. Constraints: ratio, color space intention, transparency need.
3. Canvas: compose in ChatCanvas with Brand Kit locked.
4. Correction: Touch Edit local faults before export.
5. Conversion: export the right container; name it; QA it.

The expensive mistake is designing for "whatever" and exporting five wrong files at the deadline.

## 7. Color Space Without Mysticism

RGB is for screens. CMYK is for many ink-on-paper paths. Soft proofing helps; vendor confirmation decides.

Operational rules:

- Social/web ads: RGB
- Packaging/press: follow vendor profile
- Do not assume an RGB PNG "converted in your head" is press-ready
- Brand Kit hex values are screen truths; ink truths need print process awareness

## 8. Resolution and PPI Reality

PPI only makes sense with physical size. A 1080px asset can be perfect for a phone feed and useless for a 24-inch poster.

Quick gut checks:

- Social feed: export at destination pixels
- Letter/A4 flyer: aim for ~300 PPI at final inches
- Large format often allows lower PPI because viewing distance increases — confirm with printer

## 9. Transparency and Matte Traps

PNG alpha on dark canvases can grow ugly fringes when placed on light backgrounds if matte handling is wrong. QA exports on both light and dark checker contexts when edges matter.

SVG transparency and PNG transparency are not interchangeable in every app. Test the destination.

## 10. Text in Exports

If type must stay editable for a teammate, do not flatten into a photo JPEG as your only master. Keep a layered/working source when the workflow allows, and export flattened delivery formats separately.

Generative text inside pixels remains a QA tax. Prefer real text layers in the finishing tool when claims must stay perfect.

## 11. Batch Export and Naming

```text
brand_campaign_channel_ratiopx_colorspace_v##_status.ext

harbor_spring26_meta_1080x1350_rgb_v03_approved.png
harbor_spring26_print_flyer_pdfx_v02_review.pdf
harbor_mark_primary_svg_v01.svg
```

Batch rules:

- one job class per batch folder
- do not mix exploration and approved finals
- keep a sidecare note for print specs

## 12. Comparison Matrix (ASCII)

```text
Format | Transparency | Best for              | Avoid for
-------|--------------|-----------------------|--------------------
PNG    | yes          | UI/text/alpha social  | huge photo libraries
JPEG   | no           | photos/lifestyle      | logos/type masters
WebP   | yes/varies   | modern web            | stubborn email/PPT
SVG    | yes          | icons/logos/web scale | photoreal scenes
PDF    | n/a wrap     | decks/print packages  | assuming one PDF fits all
TIFF   | optional     | print raster masters  | casual social posts
GIF    | limited      | tiny loops            | gradients/photos
EPS    | n/a wrap     | legacy logo vendors   | default web delivery
```

## 13. Case Studies (First Person)

### Case 1 — Logo JPEG disaster

Client uploaded our logo into their POS software from a JPEG export a freelancer made "because it was smaller." Halo artifacts everywhere. We replaced with SVG + PNG fallbacks. Rule tattooed on the wall: logos leave as SVG/PNG, never JPEG.

### Case 2 — RGB brochure

A beautiful RGB PDF went to a quick printer. Skin tones shifted. We rebuilt with vendor PDF/X guidance and a proof. Cost: one day. Lesson: ask first.

### Case 3 — Story export from square master

Marketing cropped a 1:1 hero into 9:16 and cut off the product label. We now generate/export hardest ratio first when multi-ratio delivery is promised.

### Case 4 — WebP-only handoff

A partner could not open WebP in their ancient CMS. We keep JPEG/PNG fallbacks for handoff packs even when the website uses WebP.

## 14. The Five Export Failures That Kill Delivery

1. Wrong container for the job (JPEG logo, GIF photo, screen PDF to press)
2. Wrong pixels for the channel
3. No transparency when the layout needs it
4. No naming discipline, so approved files cannot be found
5. No QA on the actual export

## 15. QA Checklist Before You Send

1. Format matches destination
2. Pixel dimensions match channel
3. Transparency correct (or correctly absent)
4. Logo edges clean at 100% zoom
5. Text readable at mobile size
6. Color space intention documented for print
7. File name explains itself
8. Opened in a dumb viewer, not only Lovart preview
9. Light and dark background edge check if alpha
10. Companion formats included if handoff needs fallbacks

## 16. Team Playbooks

Solo: destination-first brief sticky note above monitor.  
Small team: exporter role on deadline day.  
Agency: put format matrix in the SOW deliverables table.

## 17. Print Vendor Email Template

```text
Subject: Print specs confirmation — [job name]

Hi [vendor],
We are preparing finals for [piece] at [final size] with [bleed].
Please confirm preferred delivery format (PDF/X version or TIFF),
color profile, font outlining needs, and minimum PPI at size.
Also confirm proof process and turnaround.
Thanks,
[name]
```

Send this before you export twenty wrong files.

## 18. Social Compression Survival

Platforms recompress. Soft logos die. Export sharper masters, keep clearspace, test on a phone over cellular, and avoid tiny type.

## 19. When to Keep a Working Master

Keep a working master when:

- text may change
- variants will multiply
- print and digital both needed
- legal/compliance may request edits

Delivery formats are outputs. Working masters are insurance.

## 20. FAQ Seed

### PNG or SVG for logos?

SVG when it is a true vector mark for web/app. PNG fallback for places SVG fails. Both beat JPEG.

### Can I print from PNG?

Sometimes for casual jobs; for serious press work, follow vendor PDF/TIFF instructions.

### Is WebP always better?

Better for many websites; not always better for partner handoffs.

### What about PDF for Instagram?

Usually wrong tool. Export social pixels as PNG/JPEG/MP4.

## 21. Deep Dive: PNG in Production

PNG is the workhorse of digital design delivery for a reason. When I need a Story sticker, a UI mock, a price callout with crisp type, or a product cutout on a transparent field, PNG is usually the first honest answer.

Where teams abuse PNG is photography. A 4000px lifestyle photo saved as PNG can be tens of megabytes for no visual gain over a well-encoded JPEG. That bloat slows CMS uploads, clogs Slack, and makes email marketers hate you.

My PNG rules:

- Use PNG8 only when you truly understand indexing tradeoffs; most brand teams should default to PNG24/32 mindset for quality.
- Keep alpha edges clean; zoom to 100% and check hair, shadows, and logo corners.
- For multi-size app icons, export from vector when possible; do not successively downscale dirty rasters.
- If a marketplace rejects transparency, flatten onto the required background color intentionally, not accidentally.

## 22. Deep Dive: JPEG Without Regret

JPEG is not the enemy. Lazy JPEG is the enemy. I use JPEG for:

- PDP secondaries that are photographic
- Blog heroes that are photos
- Paid social photos where transparency is unnecessary

I set quality high enough that skin and gradients do not posterize, then stop. Endless "quality 100" religion creates giant files without visible benefit in the channel.

Never use JPEG for:

- primary marks
- tiny UI icons
- screenshots where UI text must remain forensic-sharp
- any asset that will be re-saved repeatedly through a junk pipeline

Re-encoding JPEG through three tools is how mud appears.

## 23. Deep Dive: SVG Discipline

SVG success depends on clean shapes. A "vector export" of a messy traced photo is not a logo strategy. In Lovart workflows, treat SVG as the container for marks and simple illustration systems that must scale from favicon to booth wall.

Practical SVG checks:

- opens in browser
- color matches Brand Kit intent
- does not rely on huge embedded rasters pretending to be vector
- file size sane
- named `..._mark_primary_v01.svg` not `final_final3.svg`

If a print vendor asks for EPS and your mark is clean PDF/SVG, ask whether PDF is acceptable. Many say yes in 2026.

## 24. Deep Dive: PDF as a Package, Not a Magical Save

Saying "I sent a PDF" is like saying "I sent a file." What kind?

Screen deck PDF: RGB, interactive-ish, lighter.  
Print PDF: standards, fonts, bleed, intended profiles.

I keep separate export presets mentally:

- `deck-screen`
- `proof-print`
- `vendor-final`

If your team has one PDF button for everything, you will eventually pay a printer to educate you.

## 25. Ecommerce Export Pack Blueprint

For a typical SKU launch pack I deliver:

```text
/sku_name/
  pdp_main_rgb_2000.jpg
  pdp_alt_01_rgb_2000.jpg
  pdp_alt_02_rgb_2000.jpg
  cutout_master_rgb.png
  social_1x1_1080.png
  social_9x16_1080x1920.png
  brand_note.txt
```

The cutout master is PNG. The PDP mains follow channel rules. Social are separate, not clumsy crops done by an intern at midnight without safe margins.

## 26. Social Export Pack Blueprint

```text
/campaign_week/
  feed_1x1/
  feed_4x5/
  stories_9x16/
  approved/
  exploration/
```

Exploration never uploads to Ads Manager. Approved only. Each approved file includes ratio in the name so nobody asks which is which in a Zoom call.

## 27. Presentation and Pitch Decks

Pitch decks fail when screenshots are soft and logos are JPEG. Export UI captures as PNG. Keep the company mark as SVG in the slide master when the software allows. When clients ask for a "PDF version," generate a screen PDF intentionally and tell them it is not a press file.

## 28. Motion Still Posters

Every video needs a poster frame. Export that poster as PNG or high-quality JPEG at the video ratio. Do not grab a random fuzzy frame from a compressed MP4 if you still have the still master in ChatCanvas. The still master is almost always better.

## 29. Email Design Exports

Email is hostile. Assume SVG will fail somewhere. Export critical headers as PNG or JPEG at 2x when retina matters, keep file weight reasonable, and test in real clients. Background images and transparency tricks vary; design for degradation.

## 30. Large Format and Retail

Retail posters and booth walls are where pixel math humiliates people. Calculate needed pixels from final inches and PPI guidance from the printer. A feed post is not a booth wall. If you only have a 1080px asset, say no or redesign.

## 31. Accessibility and Export

Low-contrast text baked into a JPEG cannot be fixed by a screen reader. Keep meaningful text as real text when possible. If text must be in image form, make contrast strong and size large. Export QA includes mobile glance testing.

## 32. Case File: Three-Week Brand Kit Delivery

A two-person studio hired us to deliver a brand kit: mark, social templates, pitch deck cover, and basic packaging sticker. They did not hire us to teach file formats. They still needed file formats.

Week 1: mark approved in ChatCanvas; delivered SVG + PNG + PDF one-pager.  
Week 2: social templates exported as PNG at 1:1 and 9:16; working notes kept for copy swaps.  
Week 3: sticker art delivered as PDF per sticker printer spec after an email confirmation.

The only argument we had was when their internal marketer re-exported the SVG mark to JPEG for "convenience." Convenience cost them a reprint. We put the format matrix on page one of the brand kit PDF after that.

## 33. Case File: Marketplace Suppression Scare

An Amazon-style listing used a main image with the wrong background treatment and soft label type from a low-quality JPEG export. Listing quality suffered. We rebuilt from a higher-res cutout PNG flattened correctly to channel background rules. Export discipline is commerce infrastructure.

## 34. Case File: Agency Handoff Chaos

An agency partner sent fifty files named `Asset_1` through `Asset_50` mixed WebP/PNG/JPEG with no ratios in names. Our producer spent two hours sorting. Now our intake rejects packs without naming conventions. Being kind does not mean accepting entropy.

## 35. Training Juniors on Exports

Day one exercise: take the same composition and export JPEG logo, PNG logo, SVG mark (if applicable). Compare at 100% and after a fake "upload compression" pass. Juniors remember what they break.

Day two exercise: write a vendor questions email.  
Day three exercise: build a social pack with correct pixels.  
Day four: reverse-audit a live campaign folder.

## 36. Preflight Script for Deadline Day

Producer asks:

1. Where does this publish?
2. What exact pixels?
3. Transparency yes/no?
4. Print vendor spec received?
5. Fallback formats needed?
6. Who opens the export for QA?

If anyone answers "just export whatever," stop the line.

## 37. Common Myths

Myth: higher megabytes always means better.  
Reality: wrong format with high weight is still wrong.

Myth: SVG always beats PNG.  
Reality: SVG wins for clean scalable marks; PNG wins for many raster UI realities.

Myth: PDF is always print-ready.  
Reality: only if built as a print PDF with correct specs.

Myth: the canvas preview is the delivery.  
Reality: the file you attach is the delivery.

Myth: one master ratio can crop to all channels without redesign.  
Reality: sometimes, often not for product packing.

## 38. Color Banding and Gradients

Gradients reveal format sins. GIF banding is obvious. Aggressive JPEG can posterize soft skies. PNG handles many UI gradients better. For print gradients, talk to the vendor about screening and file type. If a sky looks dirty, inspect format before you redesign the whole campaign.

## 39. ICC Profiles Without Panic

You do not need to become a color scientist this week. You do need to stop ignoring profile conversations when money hits paper. Ask vendors for the profile they want. Keep RGB brand hexes for screens. Soft proof when stakes are high. Approve a physical proof when stakes are higher.

## 40. Export Matrix by Job Class

```text
Job class              | Default export        | Fallback           | Notes
-----------------------|-----------------------|--------------------|--------------------
Logo digital           | SVG + PNG             | PDF one-pager      | never JPEG primary
Social still           | PNG/JPEG at pixels    | -                  | hardest ratio first
PDP photo              | JPEG per channel      | PNG cutout master  | follow marketplace rules
UI screenshot          | PNG                   | -                  | preserve text edges
Pitch deck             | screen PDF + PNG bits | editable source    | not press PDF
Packaging sticker      | vendor PDF/TIFF       | -                  | email specs first
Email header           | PNG/JPEG              | -                  | avoid SVG dependency
Booth wall             | printer-directed      | -                  | calculate pixels
Video poster           | PNG/JPEG at ratio     | -                  | from still master
```

## 41. Lovart-Specific Practical Tips

- Lock Brand Kit before batch exports so color does not drift across a fifty-file dump.
- Touch Edit before export; exporting a known flaw multiplies work.
- Identity Lock helps consistency; it does not choose file format for you.
- When generating for multi-channel campaigns, write the channel list in the brief so exports are planned, not improvised.
- Keep exploration watermarks out of approved export folders.

## 42. Handoff Pack for Clients

Include:

- approved finals
- fallback formats if needed
- logo suite (SVG/PNG/PDF)
- a one-page "how to use these files" note
- what not to do (no JPEG logo re-save, no upscaling 1080 to billboard)

Clients misuse files. Educate in the pack.

## 43. Versioning Strategy

`v01` exploration, `v02` internal revise, `v03_approved` client-ready. Never overwrite `v03_approved` with a stealth edit. New version number. Archives save careers.

## 44. Storage and CDN Thoughts

Heavy TIFFs do not belong in a public CMS. Store print masters in drive structures with access control. Public web should get web-appropriate formats. This is obvious until someone syncs the print folder to the website by accident.

## 45. Security and Metadata

Exports can carry metadata. For sensitive client work, follow your studio hygiene rules on metadata scrubbing where appropriate. Do not leak internal path names and junk titles into public files if your toolchain writes them.

## 46. International Partners

Partners abroad may still request EPS or weird size conventions. Do not argue ideology. Confirm, deliver, document. Keep your internal masters clean SVG/PDF/PNG regardless.

## 47. Extended FAQ

### What format should I export from Lovart for Instagram?

Export at the target ratio and pixel size as PNG or JPEG. Use PNG when you need transparency or ultra-crisp type. Use JPEG for photographic scenes without alpha.

### What format for a logo package?

SVG + PNG at multiple sizes + a PDF logo sheet. Add EPS only if a vendor demands it.

### What format for print flyers?

Ask the printer. Often a print-ready PDF with bleed. Do not send a 1080px social PNG.

### Can I use WebP everywhere?

No. Use it where the stack supports it; keep fallbacks for stubborn handoffs.

### Why does my JPEG logo look dirty?

Because JPEG is the wrong container for sharp-edged marks. Switch to PNG/SVG.

### Why did my print colors shift?

RGB-to-press expectations mismatch is common. Confirm profiles and proof.

### Should screenshots be JPEG?

Prefer PNG for UI screenshots.

### How do I export for both feed and stories?

Create dedicated 1:1 and 9:16 compositions or safe adaptations. Do not rely on blind center crops for product labels.

### What is a good file naming example?

`acme_launch_meta_1080x1350_rgb_v04_approved.png`

### Do I need TIFF if I have PDF?

Only if the vendor asks. PDF packages cover many modern print paths.

## 48. One-Page Route Card

```text
LOVART STUDIO — EXPORT ROUTE CARD

Digital mark     -> SVG + PNG
Social still     -> PNG/JPEG at channel pixels
Photo PDP        -> JPEG (+ PNG cutout master)
UI capture       -> PNG
Email            -> PNG/JPEG
Print            -> vendor PDF/TIFF after email confirm
Deck             -> screen PDF
Never            -> JPEG logos, GIF photos, social PNG to press
QA               -> open export, zoom 100%, mobile glance, name check
```

## 49. Closing Manifesto

1. Destination first.  
2. Format is part of design.  
3. Names are part of QA.  
4. Print asks before print exports.  
5. Fallbacks beat ideology.  
6. Preview is not delivery.  
7. Teach clients how to not destroy the files.

If you only improve one habit this week, stop shipping JPEG logos. That single fix will raise perceived quality more than another prompt tweak.


## 50. Workshop: Rebuild a Bad Handoff Pack in 45 Minutes

Bring a messy folder. Set a timer.

Minutes 0–10: sort exploration vs approved. Delete or quarantine junk names.  
Minutes 10–20: relabel approved files with brand_campaign_channel_ratio_v_status.  
Minutes 20–30: identify missing fallbacks (SVG/PNG logo suite gaps).  
Minutes 30–40: open each approved export at 100% and on mobile.  
Minutes 40–45: write a one-page client note: what each folder is for.

Teams that run this workshop once stop pretending naming is optional.

## 51. Destination Cards (Copy Into Briefs)

### Meta feed card

Ratio 1:1 or 4:5, 1080+ px, RGB, PNG/JPEG, safe margin for UI, no critical type in bottom overlay zone if platform UI competes.

### Story card

9:16, 1080x1920, RGB, PNG/JPEG, top/bottom safe zones, logo not in corner death zones.

### PDP card

Channel background rules, exact pixel minimums, JPEG or flattened PNG per rules, no fake props that violate marketplace policies.

### Printer card

Final size, bleed, profile, font outline expectations, proof cycle, contact name.

If a brief has no destination card, it is not a production brief yet.

## 52. How Export Choices Interact With Generative Artifacts

Generative textures can hide or exaggerate format problems. A subtle texture boil may look acceptable in-canvas and ugly after JPEG quantization. A thin generated line may disappear in aggressive compression. QA compressed outputs, not only masters.

When you know a channel compresses hard, avoid micro type and hairline rules in the composition stage. Format cannot save a design that depends on one-pixel poetry.

## 53. Collaboration With Developers

Dev teams want predictable assets: consistent dimensions, predictable alpha, sometimes `@2x` naming. Ask whether they prefer SVG icons or PNG sprites. Deliver a README in the zip. Developers are allies when you speak in pixels and packages.

## 54. Collaboration With Media Buyers

Media buyers care about weight, ratio, and policy. A 20MB PNG may fail upload. Offer optimized delivery versions without destroying the master archive. Keep masters and delivery encodes in separate folders so optimization does not erase the source of truth.

## 55. The "Final_Final" Archaeology Problem

If your drive still contains `final_final_really_v7`, you are paying a hidden tax. Adopt versions and statuses. Teach account managers to only pull `_approved` files. Archaeology is not a creative skill; it is a process failure symptom.

## 56. Exporting for White-Label Partners

Partners may rebrand. Provide logo suite clearspace rules and file dos/donts. Do not give them only a flattened JPEG campaign ad as their brand kit. They will cut the logo out with a wand tool and summon demons.

## 57. When Not to Export Yet

Do not export for delivery when:

- Brand Kit still drifting
- copy not approved
- vendor specs not received for print
- ratio list incomplete for paid
- legal/claims review pending on text-in-image

Exporting early creates zombie files that somehow get published.

## 58. Red Team Questions for Any Export Pack

- Which file would a tired intern upload by mistake?
- Which file is a JPEG logo?
- Which print file lacks a documented spec?
- Which social file is the wrong ratio?
- Which "approved" file is actually exploration?

If you cannot answer quickly, the pack is not ready.



## 59. Extended Case: Product Launch in Five Channels

Channels: website PDP, Meta, Stories, email, one-sheet PDF for sales.

We built a still master set in Lovart first, then exported:

- PDP JPEGs per web spec
- PNG cutouts for design system
- Meta 4:5 PNG/JPEG set
- Stories 9:16 set with safe zones
- email header PNG under weight budget
- sales one-sheet as screen PDF, with a note that it is not for offset print

Sales later asked for a "poster." We refused to upscale the one-sheet and scheduled a proper print path. Saying no protected the brand.

## 60. Extended Case: Restaurant Menu Refresh

Menus combine type, prices, and photos. We kept type in the layout tool for the print menu PDF, used photographic JPEGs for food, and PNG for icons. A staff member previously had exported the whole menu as one giant JPEG from a photo of a laptop screen. That is not a workflow; that is a cry for help. We documented exports in a laminated back-of-house sheet because restaurants are chaotic in the best way.

## 61. Extended Case: App Icon Pipeline

App icons need merciless size sets. Source from clean vector where possible, export PNGs at required sizes, avoid "scale up from 48px." Review on actual devices. SVG may not be the store upload format; PNG sizes still matter.

## 62. Metrics for Export Process Health

Track for a month:

- number of client complaints tied to file quality
- number of printer rejections
- number of ads rejected for size/ratio
- time spent renaming files
- percent of packs with README

If renaming time is high, naming rules are not enforced at creation.

## 63. Contract Language Snippet for Deliverables

```text
Digital deliverables will include channel-specific exports (ratios/pixels listed in Exhibit A)
plus a logo suite (SVG/PNG/PDF). Print deliverables require vendor specification confirmation
before final export. JPEG logos are not acceptable primary mark deliverables.
```

Put it in writing once and spare yourself ten arguments.

## 64. What Changed in Our Defaults Since 2024

- More WebP for web, still not for every handoff
- More insistence on destination cards in briefs
- More SVG+PNG logo suites, less EPS by default
- More refusal to upscale social assets into print
- More reverse audits on approved folders

Defaults should expire. Revisit quarterly.



## 65. Field Notes Library

Note A: A black PNG logo on transparent looked fine until placed on a dark hero; edges vanished. Provide light/dark logo variants.  
Note B: A PDF deck embedded tiny JPEG logos; zooming during pitch looked unprofessional. Replace embedded marks.  
Note C: A WebP sequence broke a retailer CMS; provide ZIP with PNG duplicates.  
Note D: A "CMYK PDF" that was not actually CMYK wasted a proof cycle. Verify with inspector tools/vendor.  
Note E: A team used screenshots of Lovart UI as finals including chat chrome. Crop carefully; export clean.

## 66. Checklist Poster Text (Print This)

Destination? Pixels? Format? Alpha? Color space? Name? Fallback? Opened outside Lovart? Mobile glance? Approved folder only?

Tape it near the designer who always rushes.

## 67. Pairing With Other Guides

Export format choice pairs with image model selection (still quality upstream) and commercial-use policy (what you are allowed to ship). A perfect PNG of a risky lookalike face is still a bad delivery. Format excellence does not erase other gates.

## 68. 14-Day Adoption Plan

Days 1–2: publish route card.  
Days 3–4: rename one live campaign pack correctly.  
Days 5–6: build logo suite standard.  
Days 7–8: add destination cards to brief template.  
Days 9–10: run workshop on a messy folder.  
Days 11–12: add contract deliverable language.  
Days 13–14: reverse-audit and fix gaps.

## 69. Closing Operator Reminder

Every week, someone will ask for "just a quick export." Quick is fine. Random is not. Ask where it will live. Choose the container on purpose. That is professional design ops in one minute.



## Extra Drill: Explain the Format Out Loud

Before uploading, say aloud: "This is a [format] because [destination need]." If you cannot finish the sentence, you are guessing. Guessing is how JPEG logos ship.

If two teammates disagree on format, write the destination card together before exporting either option. Agreement upstream is cheaper than duplicate exports downstream.

## 70. Production Appendix: Sample Logo Suite README

```text
LOGO SUITE — HOW TO USE
- primary_mark.svg : use for web/app whenever possible
- primary_mark.png : fallback where SVG fails
- primary_mark_on_dark.png : for dark backgrounds
- logo_sheet.pdf : overview for humans
DO NOT
- convert the mark to JPEG
- add drop shadows that alter clearspace
- stretch proportions
- recolor outside Brand Kit without design approval
```

Include this README in every brand zip. It prevents a shocking amount of damage.

## 71. Production Appendix: Sample Social Pack README

```text
/approved/ contains only launch-ready files
Filenames include ratio and version
Do not upload /exploration/
If you need a new size, request a proper export; do not stretch
```

## 72. Production Appendix: Printer Response Checklist

When the printer replies, store preferred format, profile name, bleed values, proof type, due dates, and contact person. No reply, no print export. That sentence alone is a margin protector.

## 73. Why This Page Exists on the GSC Slug

Searchers landing on export format queries usually need a decision, not a myth. This guide answers which container, which pixels, which fallback, and which QA. If your team bookmarks one wiki page for delivery, keep this route card visible on deadline days.

## 74. Final Ops Habit

Once a week, reverse-audit one approved folder. If you find a JPEG logo, a wrong ratio, or an exploration file in approved, fix the process that allowed it. Export quality is culture, not a one-time tutorial.


## 75. Channel Spec Sheets You Can Paste Into Notion

### Meta / Instagram stills

- Feed: 1080x1080 or 1080x1350, RGB, PNG or JPEG
- Story/Reels cover still: 1080x1920, RGB, PNG or JPEG
- Keep key product/label away from UI chrome zones
- Upload from `/approved/` only
- Weight: optimize delivery copy if platform complains; keep master untouched

### Google Display style stills

- Follow active size list from the media buyer
- Exact pixels matter more than aesthetic cropping after the fact
- PNG for sharp type; JPEG for photo-only banners
- Provide a backup size set if the plan includes multiple placements

### Email

- Header widths commonly 600–1200 CSS px depending on template
- PNG/JPEG only for critical heroes
- Watch total email weight; giant PNGs get clipped by clients
- Test dark-mode oddities when logos are transparent

### Website CMS

- Hero: modern stack may accept WebP with JPEG/PNG fallback
- Icons: SVG preferred when clean
- Open Graph image: usually 1200x630 JPEG/PNG — design intentionally, do not random crop

### Sales PDF

- Screen PDF for emailing humans
- If sales later asks for print, restart with printer card, do not pretend the screen PDF is press-ready

## 76. The Physics of Upscaling Fantasies

Upscaling tools improved. They did not repeal information theory for every case. A soft 800px logo will not become a perfect booth wall through wishful enhancement. If the job is large format, create for large format. Budget the generation and layout at the right scale. Upscaling is a rescue tool, not a plan.

## 77. Soft Proof Culture

For packaging and brochures, soft proofing is a conversation starter, not a final verdict. Use it to catch catastrophic shifts early. Still approve a physical proof when the SKU color is part of brand equity. Document who approved which proof version. Arguments evaporate when the proof log exists.

## 78. Handing Files to Non-Designers

Non-designers will:

- flatten everything to JPEG
- stretch ratios to fill slides
- screenshot instead of using the SVG
- grab the first file in the folder

So design the folder against human failure: README on top, approved only, logo suite obvious, don'ts explicit. Empathy is part of export design.

## 79. Archive Periods

Keep approved finals at least through the campaign plus a buffer for complaints, retailers, and "can we run that again?" requests. Exploration can be purged on a shorter cadence if storage hurts, but never purge the only logo SVG because someone thinks the PNG is enough.

## 80. Multi-Brand Studios

If you serve multiple brands, prefix every filename with brand codes. Nothing causes faster chaos than two clients both named "Aura" and a folder of `aura_final.png` files. Brand code discipline is export discipline.

## 81. Crisis Rebuild Kit

When a live ad is wrong:

1. Pull the bad file out of paid
2. Identify whether the issue is format, ratio, compression, or design
3. Rebuild from master, not from the compressed download
4. Version up
5. Reverse-audit how it passed approved
6. Patch checklist

Rebuilding from a Meta download is how generation loss compounds.

## 82. Pairing Exports With Analytics Naming

If media ops track creative codes, mirror those codes in filenames. Analytics and design should not speak different languages. A weekly five-minute sync on naming saves a monthly reporting mess.


## 83. Detailed Walkthrough: From ChatCanvas to Meta Upload

1. Brief lists destination cards for 4:5 and 9:16.  
2. Generate/lock stills under Brand Kit.  
3. Touch Edit label clarity.  
4. Export `brand_camp_meta_1080x1350_rgb_v01.png` and story equivalent.  
5. Open both outside Lovart.  
6. Mobile glance.  
7. Move to `/approved/`.  
8. Media buyer uploads only from approved.  
9. If platform rejects weight, create `..._delivery.jpg` derivative without deleting PNG master.

That is a boring pipeline. Boring pipelines print money.

## 84. Detailed Walkthrough: From ChatCanvas to Sticker Printer

1. Email printer with template questions.  
2. Receive PDF/TIFF + bleed answer.  
3. Layout with bleed and safe type.  
4. Export print PDF per instructions.  
5. Soft proof; then physical proof if required.  
6. Archive proof approvals beside the PDF.  

If step 1 is skipped, step 6 becomes a postmortem.

## 85. Detailed Walkthrough: Logo Suite Refresh

1. Approve mark in canvas.  
2. Produce SVG clean paths / clean export.  
3. PNG on clear for light backgrounds.  
4. PNG on clear or dedicated on-dark variant.  
5. PDF sheet with clearspace diagram.  
6. README don'ts.  
7. Deprecate old suite with dated archive folder.  

Never leave old and new suites mixed without dates.

## 86. What I Want Tools to Make Easier

One-click destination presets help only if teams still understand the why. Presets without literacy create confident wrong exports at scale. Use presets as accelerators after the route card is learned.

## 87. Glossary

**Approved folder** — files allowed to publish.  
**Delivery derivative** — optimized encode for a channel, not the master.  
**Destination card** — ratio/pixels/format constraints for a channel.  
**Fallback** — alternate format for stubborn software.  
**Master** — highest-integrity source you keep.  
**Printer card** — vendor-confirmed print specs.  
**Route card** — studio defaults for format choice.  
**Screen PDF** — PDF meant for digital reading, not press.  
**Working file** — editable source for future changes.

## 88. If You Remember Only Ten Rules

1. No JPEG logos.  
2. Destination first.  
3. Hardest ratio first when promised.  
4. SVG+PNG logo suites.  
5. Ask printers before exporting press files.  
6. Name with ratio and version.  
7. Approved ≠ exploration.  
8. QA outside the canvas.  
9. Keep masters when making delivery encodes.  
10. Teach clients how to not destroy files.


## 89. Office Hours Script for Sticky Format Questions

When someone pings "what format?", answer with questions first:

1. Where will it be published or printed?
2. Does it need transparency?
3. Is it a logo, photo, UI, or layout package?
4. Who must open it next (designer, buyer, printer, client CMS)?
5. Do we already have a destination card?

Only then recommend a container. If you answer "just PNG" to every ping, you train the team to stop thinking.

## 90. Onboarding Assignment (Graded)

Assignment: build a mini pack for a fake brand "Northline Mug".

Deliverables:

- logo suite README + SVG/PNG/PDF sheet
- one Meta 4:5 approved export
- one Story 9:16 approved export
- one screen PDF one-pager
- a printer questions email draft (not a fake print PDF)

Pass criteria: naming correct, no JPEG logo, approved/exploration split, README present, destination cards cited.

New hires who fail this do not touch live client approved folders alone.

## 91. The Cost of Wrong Exports (Plain Math)

Suppose a designer earns $45/hour internally.

- 90 minutes renaming chaos: $67
- 1 printer rejection + rebuild afternoon: $180+
- 1 paid media flight with wrong ratio crop: media waste + reshoot time
- 1 client trust hit from crunchy logo in a board deck: unpriced but real

Format literacy is cheaper than heroics. Put the route card where the team can see it.

## 92. Closing Paragraph for Deadline Weeks

Deadline weeks create tunnel vision. People export whatever the dialog defaults to. That is why the destination card must exist before the crisis. Fill it on Monday. Export on Thursday. QA on Thursday. Publish on Friday. If you try to invent specs on Friday at 5pm, the weekend will own you.


## 93. Bookmark This If You Ship Creative Weekly

If your job touches creative delivery even sideways — designer, producer, media buyer, founder — keep this page bookmarked beside your Brand Kit. Generation quality gets the spotlight. Export quality decides whether that spotlight looks sharp or accidental. Make the container decision explicit, every time, out loud, with a filename that proves you meant it.


## 94. Real Talk: Defaults in Export Dialogs

Export dialogs remember the last setting used by the last panicked human. That means your "default" may secretly be yesterday's wrong JPEG at 72% quality. Before a batch, consciously set format, ratio, and naming. Do not trust ghost settings.

## 95. Cross-Functional RACI for Exports

- Responsible: designer/exporter
- Accountable: producer on deadline day
- Consulted: media buyer for paid sizes; printer for press
- Informed: account manager when pack is in `/approved/`

If everyone is accountable, no one is. Write names on the campaign ticket.

## 96. Sample Ticket Fields

```text
Campaign:
Destinations:
Ratios/pixels:
Formats:
Fallbacks:
Print vendor contacted (y/n):
Exporter:
QA opener:
Approved folder path:
```

Tickets without these fields spawn wrong exports.

## 97. Handling Client-Provided Bad Masters

Clients send JPEG logos constantly. Do not quietly build a whole campaign on top. Request better masters, or rebuild the mark into a clean suite as a paid task. Silent acceptance makes their bad file your production foundation.

## 98. Seasonal Campaign Velocity

During holiday velocity spikes, format errors multiply. Freeze the route card. Ban exceptions unless producer-approved. Speed without freezes creates December incidents in January invoices.

## 99. Accessibility Export Notes for Type-Heavy Graphics

If a graphic is the only place a legal disclaimer exists, reconsider. Put critical legal text in HTML/caption layers when channels allow. For unavoidable image text, export PNG, max readability, and keep a plain-text companion in the caption.

## 100. Final Anchor

Export format choice is design. Treat it with the same seriousness you treat composition. The file that leaves your studio is the work. Make the container worthy of the craft inside it.


## 101. Deadline-Week Printed Card

Keep a printed route card near the team for deadline weeks. When someone asks for a quick export, point at the card before pointing at the export button. That tiny friction prevents expensive randomness. It also teaches juniors that delivery is part of craft, not an afterthought bolted on when Slack turns red.

## 102. Review Agenda Item

Add "export pack reverse audit" as a standing five-minute agenda item in weekly creative ops. Rotate who runs it. Publicly fix one issue each week. Culture changes through repetition, not through a single wiki read.

## 103. The Last Mile Pledge

We pledge not to ship JPEG logos, not to invent print specs alone, not to upload exploration files, and not to treat canvas preview as delivery. Sign it ironically if you must. Follow it unironically.


## 104. Practitioner Postscript

I used to think export talk was for production artists at big agencies with dedicated traffic managers. Then I watched small teams lose days to avoidable file mistakes. If you are small, you need the route card more, not less, because nobody else will catch the error before the client does. Build the habit while the team is tiny. It scales better than talent myths.


## 105. A Short Story About a Board Deck

We once supported a founder pitching the same afternoon we delivered a mark. Someone grabbed a PNG from chat, dropped it into Keynote, then exported the whole deck to a heavily compressed PDF. In the meeting room, the mark freckled. Nobody blamed Keynote. They blamed the brand.

After that, our delivery email for logo suites included three lines in bold energy without banned fluff: use the SVG in slides when possible, use PNG if needed, never redistributes as JPEG. We also attached a slide-ready PNG at generous pixels. The format guide is not academic. It is how you keep a mark alive after it leaves your hands.

## 106. Keep Two Zips

Zip A: `brand_logo_suite_vX.zip` for identity.  
Zip B: `campaign_channel_exports_vX.zip` for campaign finals.

Mixing them guarantees someone will upload a logo sheet page as a Meta ad someday. Separation is kindness.


## 107. One Last Checklist Line

Before any upload, answer in one sentence in the ticket: "Exported as [format] at [pixels] for [destination]." If that sentence is missing, the task is not done. This is the whole guide compressed into a gate that even a busy Friday can enforce.


## 108. Share the Route Card in Slack

Pin the ASCII route card in the creative channel. When someone asks for format advice, reply with the card link first. Over time the questions get better, and the exports get less random. That is the win condition for a wiki page like this.

## 109. Maker Versus Shipper Mindset

Makers care about the canvas. Shippers care about the file that survives contact with other software. Great studios hire for both and refuse to treat shipping as an insult to creativity. If you only make and never ship cleanly, you are collecting previews. Previews do not pay invoices. Delivered files do.

## 110. Endnote for Producers

Producers: you are allowed to block a handoff for format reasons. Design ego will survive. Client trust might not survive another crunchy logo in a board deck. Use the checklist line. Be the adult in the room for containers.

## FAQ


### PNG vs JPEG vs SVG — quick pick?

PNG for crisp digital graphics with possible transparency. JPEG for photos without transparency. SVG for scalable marks and simple vector illustration.

### Is PDF one format?

No. Screen PDFs and print PDFs are different deliverables.

### Can Lovart replace my print shop advice?

No. Lovart helps you create; the printer defines press constraints.

### What should be in every logo zip?

SVG, PNG, PDF sheet, usage don'ts, version number.

### How do I avoid story crop disasters?

Design 9:16 intentionally or with safe zones; do not amputate labels.

### Are giant PNG photos better?

Usually worse for workflows. Use JPEG/WebP for photo weight.

### What if a client insists on one file for everything?

Educate once in writing, then deliver a pack anyway for the channels that matter.

## Final Recommendation

Treat exports as a designed system. Build packs by channel. Name ruthlessly. QA the file that leaves the building. The model that generated the image will not apologize to your client when the JPEG logo freckles on a 4K slide. You will.
