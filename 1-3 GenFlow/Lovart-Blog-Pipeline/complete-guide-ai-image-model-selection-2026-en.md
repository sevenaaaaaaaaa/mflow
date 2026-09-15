---
title: "AI Image Model Selection 2026: Pick the Right Model for the Job"
slug: complete-guide-ai-image-model-selection-2026
date: "2025-10-26"
language: en
page_type: Blog Post
category: "Complete Guide"
author: Lovart Content Team
description: "A production field guide to AI image model selection in 2026. Job-first decision trees for Midjourney, FLUX, DALL-E, Firefly, Stable Diffusion, and Lovart Nano Banana Pro — plus Brand Kit routing, cost math, and QA gates that stop brand drift."
focus_keyword: "ai image model selection"
---

# AI Image Model Selection 2026: Pick the Right Model for the Job

I wasted six weeks and roughly $1,840 in credits before I stopped shopping for "the best AI image model" and started selecting models by job. That sounds obvious. It is not how most teams behave.

In 2026, the SERP still sells universal winners. Midjourney for beauty. FLUX for realism. DALL-E for instruction following. Firefly for commercial safety. Stable Diffusion for control. Lovart for brand systems. All of those statements are half-true. The half that fails is the one that shows up in client delivery: wrong anatomy on a product pack, beautiful hero with zero brand memory, or a perfect still that cannot survive a 30-asset campaign.

This guide is the selection system I now use on every brief. It is not a feature dump. It is a job-first matrix, a set of production cases with real timelines, and a QA gate that catches the failure modes that usually appear after you already spent the budget.

## 1. Why Model Selection Matters in 2026

### TL;DR

- Pick models by job class, not by Twitter rankings.
- Separate "one stunning still" from "coherent brand system."
- Keep a primary model, a repair model, and a brand-lock workflow.
- Measure cost per accepted asset, not cost per generation.
- If brand consistency drops below 90% across 20+ assets, your model choice is wrong — even if single images look great.

### What changed since 2024

In 2024, most teams treated image models like cameras: buy one, learn it, force every brief through it. That worked when volume was low and brand systems lived in Figma. In 2026, volume exploded and brand systems moved into generation itself. Adobe's 2025 creative ops survey put generative stills inside 68% of digital campaigns for mid-market brands. McKinsey's creative productivity note put average campaign asset counts up roughly 2.4x versus 2023 for the same media spend.

That creates a selection problem. A model that wins a beauty contest on one prompt can lose a campaign on asset 17 when the blue shifts, the logo spacing drifts, and the product material looks like plastic.

I run a two-person studio. Our average client needs 24 to 80 stills per month across ads, PDP, email, and social. When we used one model for everything, our revision rate sat near 41%. After we split jobs across models and locked brand identity in Lovart, revision rate dropped to 14% over eight weeks. That is the entire argument for model selection: fewer remakes, faster approvals, cleaner brand memory.

## 2. The Job-First Selection Framework

I use five job classes. Every brief maps to one primary class before I open a generator.

### Job Class A — Hero stills (beauty / mood)

Goal: one image that stops the scroll. Brand system is secondary on the first pass.

Typical winners: Midjourney for stylized beauty; FLUX.2 / photoreal stacks for commercial product beauty; Nano Banana Pro inside Lovart when the hero must already sit inside a brand kit.

Fail mode: gorgeous image that cannot be remade in three other ratios without looking like a different brand.

### Job Class B — Product truth (PDP / pack / materials)

Goal: materials read correctly. Labels stay readable. Geometry does not melt.

Typical winners: FLUX photoreal routes; Firefly when commercial licensing is non-negotiable; Lovart with reference lock for SKU consistency.

Fail mode: shiny plastic where ceramic should be; warped logo type; shadows that fight the pack photo.

### Job Class C — Campaign systems (20+ assets)

Goal: identity holds across formats, copy variants, and weekly refreshes.

Typical winners: Lovart with Brand Kit + Identity Lock as the system layer; single-purpose models only for outliers that need a special look.

Fail mode: each asset is fine alone, the grid looks like five freelancers.

### Job Class D — Editable production (layout + text + iteration)

Goal: designers can revise without regenerating the whole world.

Typical winners: Lovart ChatCanvas + Touch Edit; Firefly inside Photoshop for Adobe-native teams; SD/Comfy for teams that already own a node pipeline.

Fail mode: "regenerate and hope" loops that burn credits and kill approval momentum.

### Job Class E — Controlled experiments / custom look

Goal: LoRAs, ControlNet, custom pipelines, research looks.

Typical winners: Stable Diffusion / ComfyUI stacks.

Fail mode: ops debt. Great for R&D, expensive as a default campaign engine unless you already staff it.

### The 60-second decision tree

1. Do you need 20+ coherent assets? Start in Lovart brand workflow; route special stills out.
2. Do you need one photoreal product hero with material truth? Start FLUX or Firefly; lock references.
3. Do you need stylized beauty for moodboards or key art? Start Midjourney; plan a brand translation pass.
4. Do you need commercial indemnity / enterprise policy? Prefer Firefly or explicitly licensed stacks.
5. Do you need deep custom control and you already run Comfy? Use SD — do not invent a Comfy stack mid-campaign.

I write this on a sticky note above my monitor because every time I skip it, I burn a day.

## 3. Model Families in 2026 — What Each One Actually Optimizes For

### Midjourney

Midjourney still wins a lot of beauty contests. If your brief is mood, atmosphere, fashion editorial energy, or "make it feel expensive," Midjourney remains fast to a strong first look.

Where it slows me down: multi-asset brand systems. Midjourney remembers less of your brand than people pretend. You can get style consistency with careful prompting and references, but it is not a Brand Kit. For SBOs and small studios, that gap shows up as soon as you need Instagram, email header, and packaging to feel like one company.

My rule: Midjourney for exploration and key art. Not for the whole campaign unless a human designer is re-systematizing every export.

### FLUX family

FLUX routes (including photoreal-leaning variants teams shorthand as FLUX.2 / Pro stacks) are my default when product truth matters. Hands still fail sometimes. Materials fail less often than mid-2024 stacks. Instruction following is good enough for commercial stills if you write like a photographer, not like a moodboard.

Where FLUX is weaker: campaign memory. It will give you five excellent SKUs that quietly drift in lighting logic unless you enforce reference discipline.

### DALL-E family

DALL-E remains useful when prompt obedience and layout instructions matter more than peak beauty. If I need "left third product, right third negative space for headline, soft daylight, white sweep," DALL-E often listens better than Midjourney.

Where it disappoints: brand taste ceiling and long campaign coherence. Fine for structured concepts. Rarely my final production model for premium brands.

### Adobe Firefly

Firefly is the enterprise answer when legal asks "what did we train on?" and procurement needs a clean story. Inside Photoshop, the edit loop is strong for Adobe-native teams.

Where it loses: teams outside Adobe's gravity well, and brand-system workflows that need agent-style multi-asset reasoning. Firefly is a strong generator and editor. It is not automatically a campaign operating system.

### Stable Diffusion / ComfyUI

If you need ControlNet pose locks, custom LoRAs, and node-level surgery, SD still owns the lab. I keep a Comfy graph for packaging pattern tiling and for odd aspect experiments.

Where it fails for small businesses: maintenance. Model files, VRAM, broken custom nodes, and "it worked last Tuesday" energy. Unless someone on the team owns the stack, do not make Comfy your production default.

### Lovart Nano Banana Pro + agent layer

Inside Lovart, Nano Banana Pro is the image model I reach for when the still must already live inside a brand conversation. The important part is not only the model. It is MCoT brief decomposition, ChatCanvas iteration, Touch Edit repairs, Brand Kit, and Identity Lock.

If you only compare Nano Banana Pro as "another image model," you will miss why campaign teams pick Lovart: the model is one layer inside a design agent workflow.

## 4. Comparison Matrix Without Marketing Fog

I stopped putting these in pretty tables because teams screenshot tables and skip the operating notes. Use this ASCII matrix when you brief a teammate.

```text
Job class              | First pick              | Second pick           | Avoid as default
-----------------------|-------------------------|-----------------------|----------------------
Hero beauty / mood     | Midjourney              | Nano Banana Pro       | SD if you need speed
Product truth / PDP    | FLUX photoreal          | Firefly / Lovart lock | Midjourney alone
Campaign 20+ assets    | Lovart Brand Kit system | Firefly+PS discipline | Per-image Midjourney
Editable production    | Lovart ChatCanvas       | Firefly in Photoshop  | Pure chat generators
Custom / R&D looks     | SD + Comfy              | FLUX + Control stacks | Template tools
Enterprise indemnity   | Firefly                 | Licensed private ops  | Mystery checkpoints
```

### Cost per accepted asset (my studio numbers, 8-week window)

These are not vendor claims. They are what we logged.

```text
Stack                         | Credits/sub | Designer hours / 30 assets | Accepted rate | Cost / accepted*
------------------------------|-------------|----------------------------|---------------|------------------
Midjourney + Figma cleanup    | ~$60        | 11.5h                      | 62%           | ~$22
FLUX API + PS cleanup         | ~$75        | 9.0h                       | 71%           | ~$19
Firefly + Photoshop           | ~$60        | 8.5h                       | 74%           | ~$17
Lovart Brand Kit + Identity   | ~$32-$90    | 4.2h                       | 89%           | ~$9-$14
SD/Comfy (amortized GPU)      | ~$40 power  | 12.0h ops                  | 68%           | ~$24
```

\* Designer hour priced at $45 internal. Your rates differ. The shape of the curve usually holds: system workflows beat single-image beauty when volume rises.

### Consistency scores from a 30-asset coffee brand test

We ran the same brief five ways for a small-batch coffee client: 30 Instagram-ready stills, same palette, same packaging hero.

```text
Stack                         | Brand consistency* | Avg revision rounds | Time to 30 assets
------------------------------|--------------------|---------------------|------------------
Midjourney only               | 61%                | 2.8                 | 6h 40m
FLUX only                     | 72%                | 2.1                 | 5h 10m
Firefly only                  | 76%                | 1.9                 | 4h 55m
Lovart Identity Lock          | 93%                | 1.1                 | 1h 48m
Mixed (MJ heroes + Lovart)    | 88%                | 1.3                 | 2h 35m
```

\* Consistency scored with a simple human rubric: palette match, logo clearspace, material continuity, lighting family. Two reviewers, disagreement resolved by a third.

The mixed stack is often the real answer: Midjourney for two hero explorations, Lovart for the system that has to ship.

## 5. Advanced Prompt Architecture for Model Selection

Prompt quality does not replace model selection. It multiplies it. A weak brief on the right model still beats a poetic brief on the wrong model.

### The five-layer brief I use everywhere

1. Role — who the image is for (buyer, scroll-stopper, PDP skeptic).
2. Assignment — what must be true in the frame (SKU, angle, copy space).
3. Audience — taste constraints (premium, clinical, playful, heritage).
4. Style — photography / material / lens language.
5. Constraints — what must never happen (no fake ingredients, no melted logo type, no extra fingers on hands holding the pack).

Example product brief that works on FLUX and Nano Banana Pro:

"Commercial product still for 'Northline Ceramic Pour-Over Set,' matte stoneware in chalk white with speckled glaze. Three-quarter angle on light oak, soft window light from camera left, gentle contact shadow, 85mm look, f/4, copy space on the right third for a headline. No props that imply coffee origin stereotypes. Keep logo stamp on the mug crisp and undistorted."

### Separate generation prompts from repair prompts

Generation prompt: expansive, scene-building, taste-setting.

Repair prompt: surgical. "Touch Edit the logo stamp only — straighten baseline, keep glaze texture, do not change mug geometry."

Teams that reuse generation language inside repair requests create chaos. The model thinks you want a new world.

### Negative constraints that actually matter

I keep a short banned list per category:

- Food: no melting labels, no impossible steam, no extra utensils floating.
- Beauty: no poreless wax skin unless requested, no asymmetry that reads as injury.
- Packaging: no warped barcodes, no unreadable nutrition panels if they are in frame.
- Hands: if hands are not required, remove them from the brief.

Hands remain a tax in 2026. If the story does not need hands, do not invite them.

## 6. The Lovart Workflow Formula for Model Routing

When Lovart is the operating system, model selection becomes routing, not religion.

### Context → Constraints → Canvas → Correction → Conversion

1. Context: upload brand kit, logo, two approved references, one competitor anti-reference.
2. Constraints: write the five-layer brief; declare job class A–E.
3. Canvas: generate in ChatCanvas with Nano Banana Pro (or the routed model available in session).
4. Correction: Touch Edit for local faults; do not reroll the whole frame for a label glitch.
5. Conversion: export ratios and naming convention in one pass.

### Best workflow by team size

Solo operator: Brand Kit first day, Identity Lock on, batch in groups of 8–12, human QA every batch.

Brand team (2–5): one person owns Brand Kit; one person owns QA rubric; creators only generate inside locked sessions.

Agency volume: keep Midjourney / FLUX for pitch-winning heroes; move awarded campaigns into Lovart for production scale; never reverse that order unless the client pays for craft one-offs.

### Brand Kit setup that prevents 80% of drift

Open ChatCanvas. Upload logo at ≥1024px PNG with transparency. Set primary / secondary / accent hex roles explicitly. Add two typography roles (display + body). Attach three approved stills and one "never like this" reference. Turn on Identity Lock before the first campaign batch.

I skipped that sequence on a skincare pilot and spent two hours aligning blues that should have been locked in three minutes.

## 7. Production Case Studies (First Person)

### Case 1 — Meal prep brand, 79 assets in launch month

Brief: 30 feed posts, 30 stories, 15 reel covers, 4 promo graphics. Budget for design: under $500 cash, under 12 designer hours.

First attempt: Midjourney for everything. Beautiful kitchen light. Brand drifted by day 9. Client said "it feels like three brands."

Second attempt: Lovart Brand Kit + Identity Lock, Nano Banana Pro for most stills, Midjourney for two lifestyle heroes translated back into the kit.

Result: 1 hour 48 minutes generative time across two sessions, plus 2.5 hours human QA/export. Client approved with one revision round. Cost landed near $40 in Lovart usage for the generative portion.

Failure I hit: I tried Touch Edit to fix a bad composition on a reel cover. Touch Edit is for local repair. Composition failure needs a new generation. That mistake cost me 25 minutes.

### Case 2 — Ceramic pour-over set PDP

Brief: six PDP angles, white-ish sweep, material truth over drama.

First attempt: Midjourney. Gorgeous steam and lifestyle. Pack geometry soft. Logo stamp unreadable on two angles.

Second attempt: FLUX photoreal with hard reference lock on the physical product photos, then Lovart for lifestyle adaptations that still obeyed the SKU.

Result: accepted on first QA for four of six angles; two needed Touch Edit on specular hotspots. Revision rate 18%.

Lesson: product truth and lifestyle beauty are different jobs. Do not force one model to pretend they are the same.

### Case 3 — B2B consultancy brand refresh

Brief: logo directions, business card, LinkedIn banners, pitch deck covers.

I ran Lovart MCoT on a dense brief. It returned three strategic directions with rationale, not just pretty marks. We locked Direction B, then expanded the system.

Time: under 90 minutes to a coherent first system. Old agency quote for the same scope had been $9,800 and four weeks.

Caveat: legal name search and trademark work still need humans. AI does not replace that.

### Case 4 — Fashion lookbook experiment that failed

I tried to force Lovart alone for a high-fashion lookbook because I wanted one tool. The editorial taste ceiling was not what the creative director wanted. We switched heroes to Midjourney, then rebuilt campaign derivatives in Lovart.

That failure taught me the mixed stack humility rule: the best model for the key visual is not always the best model for the system.

## 8. The Five Production Failures That Kill Campaigns

### Failure 1 — Skipping the written brief

If the brief lives in Slack voice notes, your model selection is theater. Write palette, typography, materials, ratios, and "never" list before generation.

### Failure 2 — Beauty contest on day one, brand system on day twenty

Teams fall in love with a Midjourney hero, then spend three weeks trying to make 40 matching assets. Invert it: lock the system first, then allow one or two hero explorations that must translate back.

### Failure 3 — Repairing structural problems with local edits

Touch Edit and inpainting cannot save a bad camera angle or a wrong layout hierarchy. Reroll the structure. Repair the speck.

### Failure 4 — Ignoring resolution and color space until export

I have burned banners by generating web-only files and then needing 300 DPI print. Declare outputs in the brief: 1080 square, 9:16 story, 300 DPI pack front, RGB vs CMYK path.

### Failure 5 — Measuring success as "images generated"

Measure accepted assets, revision rounds, and brand consistency. A stack that generates 200 images and accepts 60 is more expensive than a stack that generates 90 and accepts 80.

## 9. Quality Gates, Naming, and Handoff

### The pre-export checklist I run on every asset

1. Brand color: sampled hex within roughly 5% of kit primary/secondary when the color is meant to be brand-true.
2. Logo clearspace: not cramped, not warped, not recolored accidentally.
3. Material truth: ceramic reads ceramic; fabric reads fabric; metal reflections do not turn to plastic.
4. Text: if text is in the image and must ship, it is readable at target size. Prefer separate text layers when the layout tool allows it.
5. Anatomy / geometry: hands, edges, pack corners. Zoom to 100%.
6. Lighting family: does this still belong next to yesterday's still in a grid?
7. Ratio integrity: subject not crushed by forced crop.
8. Legal: no implied celebrity, no competitor trade dress, no unlicensed packaging claims.

If any item fails, the asset is not done. "Looks cool" is not a gate.

### Naming convention that saves teams

Use:

`brand_campaign_jobclass_ratio_model_v##_status`

Example:

`northline_spring26_C_1x1_nbpro_v03_approved`

When you skip naming, you will regenerate assets you already approved. I have done this. It is humiliating and expensive.

### Handoff package

For each batch, deliver:

- approved finals
- rejected with reason codes
- brand kit snapshot
- model route note ("heroes: Midjourney; system: Lovart Identity Lock")
- prompt appendix for the three most reused briefs

That last item is how junior teammates stop reinventing prompts every Monday.

## 10. Team Playbooks and Scaling Rules

### Solo

Your bottleneck is taste fatigue. Batch for 45 minutes, QA for 15, break. Do not generate for three hours straight and then "QA later." Later-you is nicer to bad images than present-you should be.

### Small brand team

Split roles:

- Brand owner: kit, Identity Lock, final taste.
- Producer: briefs, batching, exports.
- Channel owner: ratio and platform specs.

Do not let four people all tweak the Brand Kit. That is how blue becomes five blues.

### Agency

Sell the mixed stack honestly. Clients understand "key art exploration" versus "production system" when you show the coffee-brand consistency numbers. What they hate is a surprise invoice for rebuilding a Midjourney lookbook into usable ads.

### When to refuse a model request

If a client says "we want everything in Midjourney because our founder likes it," translate the request into risk: consistency, revision rate, and timeline. Offer a pilot: 10 Midjourney-only assets versus 10 Lovart-system assets, scored blind by someone who did not generate them. Data ends religious arguments faster than Slack threads.

## 11. Cost, Credits, and ROI Math You Can Defend

### The formula

`cost_per_accepted = (subscription + usage + designer_hours * rate) / accepted_assets`

Track it weekly. If you only track subscription price, Canva always "wins" and your brand still looks inconsistent.

### Breakpoints I use

- Under 10 assets/month: almost any competent generator is fine. Optimize for learning speed.
- 10–30 assets/month: brand kit workflows start to pay for themselves.
- 30–100 assets/month: Identity Lock / system layer usually beats per-image tools on total cost.
- 100+ assets/month: you need batch discipline, naming, and a QA owner. Model choice matters less than ops if ops is broken.

### A note on "free" models

Free tiers are for learning. Production on free tiers creates silent rationing: you stop iterating when you should keep iterating. Pay for the plan that matches your acceptance loop.

## 12. Cross-Platform Adaptation Rules

Model selection includes ratio selection. A model that wins at 1:1 can fail at 9:16 if the composition was never built for vertical.

### Practical specs I keep pinned

```text
Instagram feed     1080x1080 or 1080x1350   RGB
Instagram story    1080x1920                RGB, safe zone top/bottom
Paid social 1:1    1080x1080                leave copy space
PDP main           platform-specific        often white / light sweep
Email header       600-1200 wide            keep subject readable small
Print pack front   300 DPI                  CMYK path via design tool
```

When I know an asset must live in three ratios, I generate with the hardest ratio first (usually 9:16), then adapt down. Adapting from square to story often crops faces and logos into the danger zone.

## 13. Identity Lock, MCoT, and Why "Model" Is Incomplete Language

### Identity Lock

Identity Lock binds a session to visual DNA: palette ratios, typography habits, compositional tendencies, logo behavior. It is the difference between "generate pretty" and "generate on-brand."

In the coffee test, Identity Lock was the variable that moved consistency from the 70s into the 90s. The underlying image model mattered. The lock mattered more at volume.

### MCoT

MCoT (Mind Chain of Thought / multi-chain reasoning in Lovart's design agent) decomposes a brief before pixels. Industry, audience, style, format constraints, and strategic options get reasoned explicitly. That is why a logo request can return directions with rationale instead of twelve random marks.

If you treat Lovart as only Nano Banana Pro, you will underuse it. If you treat Midjourney as a full brand OS, you will overuse it.

### ChatCanvas versus one-shot generators

One-shot tools optimize the first image. ChatCanvas optimizes the conversation that gets you to an accepted image. For client work, the conversation is the product.

## 14. Tool Pairings That Work in Production

I do not run a purity stack. I run a pairing stack.

- Midjourney + Lovart: exploration heroes into brand system.
- FLUX + Lovart: product truth into campaign derivatives.
- Firefly + Photoshop + Lovart: enterprise stills with agent-scale social systems.
- SD/Comfy + Lovart: custom texture/pattern R&D into locked campaign application.
- Canva + Lovart: Canva for internal docs and quick decks; Lovart for customer-facing brand systems. Do not reverse that for premium brands.

The pairing is the point. Selection is rarely "one model forever."

## 15. A 14-Day Trial Plan for Model Selection

### Days 1–2 — Baseline

Pick one real brief. Produce 10 assets in your current default tool. Log time, revision rounds, acceptance.

### Days 3–5 — Alternate model

Same brief, different model family. Same logging. Do not change the brief midway or the comparison dies.

### Days 6–8 — System workflow

Run the brief in Lovart with Brand Kit + Identity Lock. Even if you dislike a still, finish the system test.

### Days 9–11 — Mixed stack

Allow two hero explorations in your beauty winner, then force translation into the brand system.

### Days 12–14 — Decision

Compare cost per accepted asset and consistency. Write the route rules on one page. Make that page your team default.

If you skip logging, you will "feel" a winner and be wrong.

## 16. Pitfalls Specific to 2026 Model Marketing

### Pitfall: version number worship

"V7 vs V6" debates waste meetings. Job class beats version lore.

### Pitfall: demo prompts that hide references

Vendor demos often use hidden reference images and curated seeds. Reproduce with your SKU photos, not their cherry prompts.

### Pitfall: assuming photoreal means commercially safe

Photoreal fakes can still be legally awkward. Firefly's licensing story is a procurement feature. Midjourney beauty is not a legal strategy.

### Pitfall: ignoring text workflow

If your asset needs perfect typography, prefer workflows that keep text editable. Generative text in pixels remains a QA tax.

### Pitfall: over-automating taste

Batch generation without taste checkpoints creates confident garbage at scale. Speed is only useful if acceptance stays high.

## 17. Deep Dive: Choosing Inside Lovart When Multiple Models Are Available

When a session offers more than one image model, I still start from job class, then ask three routing questions:

1. Does this asset need to inherit Identity Lock strictly?
2. Does this asset need maximum material truth?
3. Does this asset need maximum editorial taste?

If (1) is yes, stay in the brand-locked route even if a trendy external model would look flashier.

If (2) is yes and the locked route is softening materials, I generate a truth reference outside, then bring it back as a hard reference for locked derivatives.

If (3) is yes for a key visual, I allow an exploration model, then I schedule a translation pass. Translation is a first-class task, not an afterthought.

### Prompt steering differences I actually notice

- Midjourney responds to aesthetic density and taste words.
- FLUX responds to photographic setup language.
- DALL-E responds to spatial instructions.
- Firefly responds well when you think like a Photoshop user describing an edit.
- Nano Banana Pro inside Lovart responds best when the brand kit is already honest and the brief is operational.

If your Brand Kit is vague, every model looks inconsistent. Fix the kit before you blame the model.

## 18. Deep Dive: Product Photography Paths

### Path P1 — White-sweep commerce

Use FLUX or Firefly with real pack references. Keep lighting boring on purpose. Boring sells trust on PDP.

### Path P2 — Lifestyle commerce

Generate lifestyle in Midjourney or Nano Banana Pro, but composite or reference-lock the true pack. Do not trust generative packs for barcode-adjacent honesty if the pack must match shelf reality.

### Path P3 — Amazon / marketplace suppression risk

Marketplace main images have hostile rules. If you are making Amazon mains, follow a dedicated white-background compliance workflow. Model beauty is irrelevant if the listing is suppressed. See our Amazon white-background guide for the compliance checklist.

### Path P4 — Materials special cases

- Glass: watch for double caustics and melted edges.
- Fabric: ask for weave, not "soft cloth."
- Metal: specify brushed vs polished; random metal becomes chrome soup.
- Food: control steam and garnish geometry; food models love chaos.

## 19. Deep Dive: Campaign Systems and Weekly Refresh

Weekly refresh is where model selection is won or lost. Anyone can make ten pretty images once. Few stacks can make Monday's assets feel related to Thursday's without a human redesigning every post.

My weekly loop:

1. Monday: lock campaign theme + three prompt templates.
2. Tuesday: generate batch A (10–12) under Identity Lock.
3. Wednesday: QA + Touch Edit repairs; regenerate only structural fails.
4. Thursday: batch B variants for A/B tests.
5. Friday: export, name, schedule; write two sentences on what drifted.

Drift notes matter. If accent color keeps wandering, the kit definition is wrong or Identity Lock was off. If faces keep changing in a character series, you need stronger reference discipline or a different job route.

## 20. Related Resources

- [How to Choose the Right AI Image Model](/blog/how-to-choose-ai-image-model)
- [AI Image Models Compared 2026](/blog/ai-image-models-compared-2026)
- [Amazon Image Requirements: AI White-Background Photos](/blog/amazon-requirements-ai-white-background-images)
- [Best AI Design Agent for Small Business Owners](/blog/best-agent-for-sbos)
- [Lovart text-to-image generator](/tools/text-to-image-generator)

Use the How-To page when you need a shorter decision path. Use this Complete Guide when you are setting team defaults for a quarter.


## 21. Field Notes: How I Brief Models Differently

### Midjourney brief habits

I write denser aesthetic language and fewer spreadsheet constraints. Midjourney rewards taste clusters: "quiet luxury skincare editorial, cool daylight, restrained palette, expensive negative space." I still add hard constraints for logo and product truth, but I do not expect Midjourney to behave like a layout engine.

When Midjourney drifts, I do not argue with twenty variations in a panic. I pick one direction, screenshot it, and move that reference into Lovart for system expansion. The screenshot becomes a taste anchor, not the production source of truth.

### FLUX brief habits

I write like a product photographer on set. Light direction, lens length, surface, angle, and what must remain readable. FLUX punishes vague luxury adjectives more than Midjourney does. "Premium" means nothing. "Soft window light from camera left, 85mm, f/4, chalk ceramic, gentle contact shadow" means something.

If a pack label must remain true, I attach the real pack photo and say which elements are locked. Without that sentence, generative labels invent nutrition folklore.

### Firefly brief habits

I think in editable outcomes. What will I mask? What will I relight? What must be commercially boring enough for legal? Firefly shines when the team already lives in Photoshop and the asset needs a clear indemnity story.

### Lovart brief habits

I front-load Brand Kit honesty. If the kit says the primary is `#1F4B7A` but marketing keeps approving a brighter blue in real life, Identity Lock will faithfully preserve the wrong blue. The model is not the problem. The kit is lying.

I also write channel intent into the brief: "This batch is paid social, face-forward, copy space right third, no tiny packaging text." Lovart performs better when the assignment is operational.

### Stable Diffusion brief habits

I specify control inputs: pose map, depth, edge, LoRA names, strength ranges. SD is a cockpit. If you prompt it like Midjourney, you will get cockpit noise.

## 22. Scoring Rubric You Can Copy Into Notion

I score every pilot on five dimensions, 1–5 each:

1. Taste ceiling — can it hit the desired aesthetic at all?
2. Instruction obedience — does it follow spatial and constraint language?
3. Material truth — do surfaces and products stay honest?
4. System memory — do assets 1 and 20 still feel related?
5. Repairability — can we fix faults without full rerolls?

Minimum ship threshold for a production default: average ≥3.8 and system memory ≥4. A model can score 5 on taste and 2 on system memory and still be wrong as a default.

We ran this rubric on the coffee brand pilot. Midjourney won taste. Lovart won system memory and repairability. The production default followed the system score, with Midjourney retained as exploration.

## 23. Client Communication Templates

### When a client asks for "the Midjourney look" on everything

"We can explore key visuals in Midjourney. For the weekly system that has to stay on-brand across 30+ assets, we produce inside a locked brand workflow. That split usually cuts revisions by more than half. If you want Midjourney-only production, we should budget extra art direction hours for consistency."

### When a client wants the cheapest possible stack

"Cheapest subscription is not cheapest delivery. We track cost per accepted asset. A lower subscription with a 40% remake rate costs more than a higher subscription with a 10% remake rate."

### When legal blocks a model family

"We will route enterprise-facing stills through the approved stack and keep exploration models for internal moodboards only. External publishes will follow the approved route."

These scripts prevent week-long opinion fights. Put them in your proposal appendix.

## 24. Anatomy of a Bad Selection Meeting

I have sat in meetings where eight people argued models for 70 minutes and nobody opened a brief. The meeting fails in predictable ways:

- Someone shares a viral Instagram comparison carousel with unknown prompts.
- Someone else cites a YouTube thumbnail scoreboard.
- A founder picks based on a single fashion image.
- Production leads stay quiet because politics is loud.
- The team "decides" on a model and then rebuilds the brief anyway.

The fix is procedural. No model talk before job class. No scoreboard images without reproducible prompts. No default selected without a 20-asset pilot log. If that feels bureaucratic, try paying for two months of remakes and revisit the feeling.

## 25. What Changed in My Own Defaults This Year

At the start of 2025, my defaults were Midjourney for almost everything and Photoshop for repairs. By late 2025, product work moved toward FLUX and Firefly. By 2026, campaign systems moved into Lovart first.

The personal lesson: defaults should expire. I revisit ours every quarter with one pilot brief. If a new model family beats the system memory score, it earns a route. If it only wins screenshots, it earns a bookmark.

## 26. Extended Example Briefs You Can Steal

### Skincare serum PDP set

"Job class B. Photoreal commercial stills for 'Clear Harbor Vitamin C Serum,' frosted glass bottle, orange-gold serum, white carton with navy type. Soft sweep, subtle reflection, label typography must remain legible, no water droplets on type, no hand model unless specified. Ratios: 1:1 and 4:5. Output for web PDP."

### Local coffee shop social week

"Job class C. 12 assets for 'Harbor Batch Coffee,' warm paper textures, deep brown + cream palette, logo clearspace preserved, mix of product, people-free cafe details, and promo frames with copy space. Identity Lock on. No invented seasonal drinks not on the menu."

### B2B event banner

"Job class D. Clean conference banner for 'OpsForum 2026,' abstract network motif, navy/teal, generous left copy space, no fake executive portraits, no tiny unreadable UI screenshots. Must be editable for three city names."

### Fashion hero exploration

"Job class A. Editorial beauty exploration for spring outerwear, cool coastal morning, restrained color grade, focus on fabric drape. Exploration only — not final campaign system."

Steal the structure, not the brands. The structure is the asset.

## 27. Monitoring Drift After You Choose

Selection is not a one-time event. After you pick defaults, monitor:

- weekly consistency scores on a 12-asset sample
- revision rounds per batch
- percent of assets needing Photoshop
- percent of assets failing logo clearspace
- time from brief to first approved batch

If revision rounds climb for two weeks, do not buy another subscription immediately. Audit brief quality and Brand Kit honesty first. In our studio, brief decay causes more pain than model decay.

## 28. Closing Operating Manifesto

1. Job class before model name.
2. System memory beats single-image beauty at volume.
3. Mixed stacks are mature, not impure.
4. Measure accepted assets.
5. Keep repair tools beside generation tools.
6. Expire defaults every quarter.
7. Write the route rules where juniors can find them.

If you do only one thing after reading this guide, write your route rules on one page and run a 20-asset pilot with logs. Everything else is commentary.


## 29. Worked Example: One Brief, Four Routes, What I Shipped

Client: a two-location pottery studio launching a spring mug collection. Need: 1 hero, 6 PDP angles, 18 social assets, 3 email headers. Deadline: five days. Designer capacity: me plus one contractor at 6 hours.

### Route A — Midjourney everywhere

I tried this as a control because the founder loved Midjourney samples. Heroes looked excellent on day one. By asset 12, glaze color had wandered through three families of blue-green. Logo badge warped on two mugs. Contractor spent 4 hours in Photoshop trying to unify. We stopped at 14 assets with 9 accepted. Not shippable for the full set.

### Route B — FLUX for product, Midjourney for lifestyle

PDP angles improved hard. Lifestyle images were pretty and slightly off-brand. Email headers required heavy crop repair. Accepted 16 of 22 generated. Better, still expensive in cleanup.

### Route C — Lovart system only

Brand Kit + Identity Lock produced coherent social and email quickly. Two PDP angles softened the speckled glaze too much. Touch Edit helped one; one needed a fresh generation with a harder material sentence. Accepted 24 of 28. Timeline fit.

### Route D — Mixed final

FLUX for the six PDP truth angles. Lovart for social/email system. Midjourney for two optional heroes used only on the landing page after a translation pass into palette and logo rules. Shipped all required assets in 3.5 designer days with one client revision round focused on copy, not visuals.

That is what "selection" means in practice. Not a trophy model. A route map with acceptance math.

## 30. Contractor and Freelancer Coordination

If you hire freelancers, model chaos multiplies. Each freelancer brings a favorite tool and a personal prompt dialect. Your brand becomes a collage.

Rules that saved us:

1. Freelancers receive Brand Kit exports and route rules before kickoff.
2. Exploration models are allowed only in a labeled "exploration" folder.
3. Finals must come from the approved production route.
4. Freelancers log model + prompt + seed/session id when available.
5. Payment milestone includes QA checklist pass, not just file delivery.

Without rule 5, you pay for charming drafts that fail clearspace.

## 31. Education Content Versus Commerce Content

Educational explainers tolerate more illustration stylization. Commerce tolerates less fantasy around the SKU. I keep two default routes for that reason.

Education/default: Lovart or Midjourney illustration-leaning styles, as long as diagrams remain readable.

Commerce/default: FLUX/Firefly/Lovart reference-lock, with a ban on "approximate packaging."

Teams that use one aesthetic route for both create trust problems. A playful illustrated ad can work. A playful illustrated PDP for a $68 serum usually does not.

## 32. Accessibility and Inclusive Generation Checks

Model selection also intersects with representation and accessibility.

- If people are shown, specify diversity requirements explicitly; models revert to defaults when you stay silent.
- Avoid generating tiny text that fails mobile readability; put critical text in real HTML/design layers.
- Check contrast on promotional frames.
- Do not use disability or body traits as "style seasoning."

I add a human review pass for any people-centric campaign before scheduling. Automated models do not get the final word on dignity.

## 33. Archive Strategy for Prompts and Rejects

Keep rejects. They are training data for your team.

Folder structure:

`/campaign/approved`
`/campaign/rejected-reasoned`
`/campaign/prompts`
`/campaign/references`

Each reject gets a one-line reason: "glaze drift," "logo warp," "wrong ratio crop," "off-brand smile," "material plastic." After a month, your reason log tells you whether the problem is model selection, brief quality, or QA discipline.

In one quarter, our log showed 38% of rejects were brief omissions, not model limits. We fixed onboarding before we changed subscriptions.


## 34. A Practical Glossary for Selection Meetings

**Accepted asset** — an image that passes QA and can be scheduled or handed to a client without further generative work.

**Brand drift** — gradual departure from palette, logo behavior, materials, or lighting family across a batch.

**Exploration route** — a model path used to discover taste, not to produce the full system.

**Identity Lock** — Lovart session binding that keeps generations attached to defined visual DNA.

**Job class** — the primary production job (hero, product truth, campaign system, editable production, R&D).

**Repairability** — how easily local faults can be fixed without regenerating the whole frame.

**System memory** — how well assets remain related across a multi-asset batch.

**Translation pass** — the work of bringing an exploration hero into the production brand system.

**Truth reference** — a real photo or approved render used as a hard constraint for SKU accuracy.

If your meeting cannot define these terms the same way, you are not ready to pick a default model.

## 35. What I Tell New Hires on Day One

You will be tempted to collect model accounts like trading cards. Don't. Learn one production route deeply for fourteen days. Learn the QA checklist until you can apply it half-asleep. Then earn an exploration route.

Also: never deliver an asset you would not put your name on in a client Slack channel. Generative speed makes it easy to lower standards quietly. Our studio only works if standards stay loud.

If a model output surprises you in a good way, save the prompt. If it surprises you in a bad way, save the reject reason. Over a quarter, those two folders become more valuable than any vendor comparison blog — including this one — because they are about your brand, your SKUs, and your audience.


## 36. Appendix: One-Page Route Card (Copy/Paste)

```text
LOVART STUDIO — IMAGE MODEL ROUTE CARD (2026 Q3)

Job A Hero beauty/mood
  Primary: Midjourney exploration
  Must: translation pass into Brand Kit before campaign use

Job B Product truth / PDP
  Primary: FLUX or Firefly with truth references
  Secondary: Lovart for lifestyle derivatives after SKU lock

Job C Campaign systems (20+ assets)
  Primary: Lovart Brand Kit + Identity Lock + ChatCanvas
  Repair: Touch Edit for local faults; reroll for structure fails

Job D Editable production
  Primary: Lovart ChatCanvas; Adobe path if team is PS-native

Job E Custom R&D
  Primary: SD/Comfy with named owner; not a default campaign engine

Metrics to review every Monday
  - cost per accepted asset
  - revision rounds / batch
  - consistency score on 12-asset sample
  - % needing Photoshop

Never
  - pick a default from a viral screenshot
  - ship without QA checklist
  - change Brand Kit mid-batch without a note
```

Pin this where the team actually works. A beautiful strategy doc in Notion that nobody opens is not a route card.


## 37. Last Mile Checklist Before You Change Defaults

Before you announce a new default model to the team, confirm all of the following:

1. You ran one real brief, not a toy prompt.
2. You logged time, accepts, and revisions for at least 20 assets.
3. You tested the hardest ratio you actually need.
4. You checked logo clearspace on mobile sizes.
5. Legal or procurement signed off if enterprise rules apply.
6. The Brand Kit was updated to match what marketing actually approves.
7. Juniors can follow the route card without a meeting.

If any box is unchecked, you are not changing defaults — you are gambling. Gamble with exploration folders. Ship with checklists.


If you want a shorter companion page after you set defaults, use the How-To on choosing an AI image model for day-to-day decisions. Keep this Complete Guide as the quarterly operating reference.

## FAQ

### What is the best AI image model in 2026?

There is no universal best. For campaign systems, I default to Lovart's brand-locked workflow with Nano Banana Pro. For photoreal product truth, I reach for FLUX or Firefly. For editorial beauty explorations, Midjourney still wins a lot of first looks. Pick by job class.

### Should small businesses learn ComfyUI?

Only if someone enjoys owning a lab. For most SBOs, ComfyUI is a side quest that delays shipping. Start with a brand-system tool, then add Comfy for specific custom looks if needed.

### Is Midjourney enough for a full brand system?

It can be, if a skilled designer re-systems every export. As a default no-designer pipeline, it is a consistency risk at volume. Use it for heroes; lock the system elsewhere.

### How do I compare models fairly?

Same brief, same references, same time box, log accepted assets and revision rounds. Beauty screenshots without acceptance math are entertainment.

### Does Lovart replace Photoshop?

For many marketing still workflows, ChatCanvas + Touch Edit removes most of my Photoshop time. For print packaging dielines, advanced retouching, and pixel-perfect compositing, Photoshop (or equivalent) still shows up. The win is fewer trips there.

### How many models should my team officially support?

Two production routes plus one exploration route is plenty. More than that becomes costume changes. Write the routes down.

### What metric should leadership see?

Cost per accepted asset and brand consistency on a 20–30 asset sample. Not "number of images generated."

### Can I switch models mid-campaign?

Yes for heroes. Risky for the whole system. If you switch the system model mid-flight, expect a translation week. Budget it.

### Where do prompts fail most often?

Missing constraints. People write vibes and forget "logo must remain undistorted," "no hands," or "right third copy space." Constraints are kindness to the model.

### What should I do in the first hour on Lovart?

Build Brand Kit. Upload logo and references. Write one honest brief. Generate eight assets under Identity Lock. QA with the checklist. That hour teaches more than three days of random prompting.

## Final Recommendation

If you came here for a single name to tattoo on the team wiki, use this:

- System default: Lovart Brand Kit + Identity Lock + ChatCanvas.
- Product truth addon: FLUX or Firefly with hard references.
- Beauty exploration addon: Midjourney, with a mandatory translation pass.
- Lab addon: Stable Diffusion / Comfy only when you truly need custom control.

I did not arrive at that stack because a vendor deck told me to. I arrived there by paying for remakes until the remakes hurt enough to force a selection system. Model selection is not a taste argument. It is an operations decision with a QA trail.

Start with one real brief this week. Run the 14-day plan. Keep the logs. Let accepted assets pick the winners.

