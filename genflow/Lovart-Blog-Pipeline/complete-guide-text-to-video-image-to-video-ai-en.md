---
title: "Text-to-Video & Image-to-Video AI 2026: Generate Footage That Survives Delivery"
slug: complete-guide-text-to-video-image-to-video-ai
date: "2025-11-02"
language: en
page_type: Blog Post
category: "Complete Guide"
author: Lovart Content Team
description: "A production field guide to text-to-video and image-to-video AI in 2026. Job-first model routing, CRAFT prompting, temporal consistency fixes, Lovart ChatCanvas workflows, cost math, and QA gates that catch melting frames before clients do."
focus_keyword: "text to video ai"
---

# Text-to-Video & Image-to-Video AI 2026: Generate Footage That Survives Delivery

I shipped a client ad last March with a text-to-video hero that looked perfect in the preview player and melted on frame 47 when we slowed it to 50%. The logo held. The product did not. The client's Slack message was one word: "why."

That clip cost me about $18 in credits and two days of trust. It also forced the rule I now use for every moving-image brief: video models are not "image models with time." They fail in time. If you do not design for temporal consistency, camera grammar, and repair loops, you are collecting demos, not delivering footage.

This guide is the operating system I use for text-to-video (T2V) and image-to-video (I2V) in 2026. It covers job-first model routing, CRAFT prompting, Lovart production workflows, cost per accepted second, and the QA gates that catch the melting-frame class of failures before a client sees them.

## 1. Why This Matters in 2026

### TL;DR

- Treat T2V and I2V as different jobs, not the same button.
- Optimize for accepted seconds, not generated seconds.
- Prefer short coherent clips (4–8s) over long hopeful clips.
- Lock identity and product truth before you ask for camera poetry.
- Build a repair path (extend, restitch, Touch Edit stills, retime) into every estimate.

### What actually changed

In 2024, most public T2V demos were two to four seconds of almost-right motion. In 2026, major stacks can hold a subject for 8–12 seconds with usable camera moves, and I2V can turn a strong still into a product orbit or lifestyle push that survives social compression.

Adobe's creative ops notes and platform self-reports through 2025–2026 put generative video inside a growing share of short-form ad tests. The practical shift for small teams is not "film is dead." It is that stock b-roll and simple product motion are no longer automatic purchase decisions. If your brief is "warm steam over a mug, slow push-in, 6 seconds, logo safe," generative can beat a $79 stock clip on cost and brand fit — when you run a real QA loop.

### The metric that matters

`cost_per_accepted_second = (credits + editor_hours * rate) / seconds that ship`

A stack that generates 120 seconds and ships 18 is more expensive than a stack that generates 40 and ships 28. I log accepted seconds weekly. Vanity generation counts lie.

## 2. Text-to-Video vs Image-to-Video — Stop Mixing the Jobs

### Text-to-video (T2V)

You describe a scene and motion. The model invents appearance and movement together. Best when you do not have a locked hero still, or when you want exploratory motion design.

Strength: flexible worldbuilding.  
Weakness: identity and product truth drift unless you constrain hard.

### Image-to-video (I2V)

You upload a still (often a brand-locked product or character frame) and ask for motion. The model must respect the frame while inventing dynamics.

Strength: brand and SKU continuity.  
Weakness: bad stills become bad movies; motion can fight the composition.

### My default routing

```text
Have a brand-locked still / SKU truth?     -> I2V first
Need exploratory mood / scene invention?  -> T2V first, then freeze a hero still
Need multi-clip character continuity?     -> still sheet + I2V, not pure T2V spam
Need editable brand layout + motion?      -> Lovart still system, then I2V
```

I used to T2V everything because it felt magical. Magical is not a delivery strategy. Magical is how you get three faces for one founder across four ads.

## 3. The Lovart Workflow Formula for Moving Images

When Lovart is the operating layer, video is rarely "type a cinematic novel and pray." It is still → motion → repair → export.

### Context → Constraints → Canvas → Correction → Conversion

1. Context: Brand Kit, logo, two approved stills, one anti-reference (motion you hate).
2. Constraints: duration, ratio, camera move, what must not change (logo, label, face).
3. Canvas: generate stills in ChatCanvas; pick the frame that already composes for motion.
4. Correction: Touch Edit local still faults before I2V; do not animate a broken pack label.
5. Conversion: I2V 4–8s clips; extend only when the ending frame still holds identity.

### Best workflow by team size

Solo: one still batch, one I2V batch, hard 8-second cap until QA improves.

Brand team (2–5): still owner + motion owner. Still owner can veto any I2V source frame.

Agency: sell T2V for pitch energy; produce awarded work through I2V from locked frames whenever SKU or face continuity matters.

## 4. Comparison Matrix and Platform Selection Guide

I keep this ASCII card on the studio wall. It is not a beauty contest.

```text
Job                              | First pick                 | Second pick            | Avoid as default
---------------------------------|----------------------------|------------------------|-------------------------
Product orbit / pack motion      | I2V from locked still      | T2V with hard refs     | Long T2V hoping for SKU
Lifestyle b-roll                 | T2V short clips            | Stock + grade          | 20s one-shot fantasies
Character continuity across ads  | Still sheet + I2V          | Limited T2V + lock     | Pure multi-clip T2V
Social ad tests (many variants)  | Lovart stills + I2V        | Runway/Pika variants   | One 15s "hero film"
Enterprise / policy-sensitive    | Approved vendor stack      | Licensed private ops   | Mystery checkpoints
Editorial camera language        | Runway / Sora-class T2V    | Kling cinematic        | Template meme tools
Brand system + motion together   | Lovart ChatCanvas path     | Still lock then I2V    | Random model hopping
```

### Cost shape from our 6-week log (internal)

```text
Stack                            | Credits | Editor hours / 10 clips | Accept rate | Notes
---------------------------------|---------|-------------------------|-------------|------
T2V-only (mixed vendors)         | high    | 6.5h                    | 34%         | pretty, drifty
I2V from random stills           | med     | 5.0h                    | 41%         | garbage-in
I2V from Lovart-locked stills    | med     | 2.8h                    | 71%         | our default
Hybrid (2 T2V heroes + I2V sys)  | med-high| 3.4h                    | 66%         | pitch + production
```

Accept rate means "client or channel-ready without a full regenerate." Your numbers will differ. The shape usually holds: locked stills beat hopeful novels.

## 5. Advanced Prompt Architecture: CRAFT for Video

Still prompting rewards adjectives. Video prompting rewards chronology and camera grammar. I use CRAFT on every serious clip.

### C — Context

Location, time of day, weather, style reference. Example: "small-batch coffee bar at 7:45am, cool window light, quiet luxury grade, no neon cyberpunk."

### R — Reference

Map assets to roles. Example: "@[Still 1] is the hero mug and must not reshape; @[Still 2] is lighting reference only."

### A — Action

Physical motion in order. Example: "steam rises slowly; barista hand does not enter frame; mug stays planted on oak."

### F — Framing

Camera. Example: "slow push-in, 35mm feel, locked horizon, no handheld shake, end on logo-safe negative space right."

### T — Timing & Sync

Duration and beats. Example: "0–2s hold, 2–6s push-in, 6–8s settle; cut-safe ending frame."

### Full CRAFT example (I2V product)

"Context: daylight product tabletop, chalk ceramic mug, soft window left. Reference: @[PackStill] locked geometry and logo stamp. Action: gentle steam drift upward, no liquid splash, no hand. Framing: 15% push-in over 6 seconds, tripod-stable, shallow depth. Timing: 6s total, ending frame must remain logo-legible for freeze."

### Separate generation prompts from repair prompts

Generation: scene + camera + timing.  
Repair: "hold identity, reduce finger melt on frame 40–48 only" or "re-generate from ending frame, continue steam, do not redesign mug."

If you paste the novel into a repair request, the model invents a new world.

## 6. Temporal Consistency — Why Footage Melts

Temporal consistency is the visible failure mode of T2V/I2V. Each frame is aware of neighbors imperfectly. Objects change texture, teeth shimmer, logos crawl, fabric becomes soup.

### Failure patterns I see weekly

1. Identity crawl — face or pack subtly morphs every half-second.
2. Texture boil — wood grain and fabric shimmer like a bad upscale.
3. Physics cheat — liquid ignores gravity; cloth clips through table.
4. Camera stutter — push-in that secretly rescales the subject.
5. Ending trash — last 12 frames collapse because the model ran out of coherence budget.

### Mitigations that actually help

- Prefer 4–8s over 12–20s for production clips.
- I2V from a clean, high-res still with readable logo.
- Specify what must not change in one blunt sentence.
- Generate two seeds; pick the stable one; do not average them in your head.
- Extend from a clean ending frame instead of asking for a hero 20s shot.
- Freeze and Touch Edit a mid-frame if a still repair opens a better I2V restart.

### The 50% speed test

Before client delivery, play the clip at 50% speed. Melts hide at 1x and scream at 0.5x. This one habit has saved me more than any model upgrade.

## 7. Image-to-Video in Lovart — Practical Loop

### Step-by-step

1. Build or confirm Brand Kit.
2. Generate or upload the still in ChatCanvas.
3. QA the still like it is a final ad frame (because it is the DNA of the clip).
4. Touch Edit label/logo/material faults on the still first.
5. Run I2V with a short CRAFT motion prompt (4–8s).
6. Review at 1x and 0.5x.
7. If usable, export; if structural fail, new still or new motion prompt; if local fail near end, extend from an earlier clean frame.

### What Lovart is good at here

- Keeping the still inside a brand conversation.
- Pairing motion with assets that already obey Identity Lock.
- Letting designers repair stills without leaving the agent workflow.

### What still needs honesty

Multi-clip character permanence across independent generations is not "solved." If a campaign needs the same founder face in six videos, build a still sheet and force I2V from those stills. Do not trust T2V to remember a person like a human actor.

### Resolution and frame rate expectations

Practical delivery in our work: 1080p at 24fps is the workhorse. Higher resolutions help when the platform needs them, but they do not fix a temporally unstable subject. 60fps often means interpolation artifacts on generative bases. Prefer stable 24fps over fake-smooth 60 if the subject crawls.

## 8. Production Case Studies

### Case 1 — Meal prep brand, 12 social clips in a week

Brief: 12 product-forward clips, 6 seconds each, same tray identity.

Fail path: pure T2V. Tray contents reshuffled themselves. Client noticed on clip 4.

Ship path: Lovart still lock for the hero tray, I2V for motion variants (steam, slow push, slight orbit). Accept rate 9/12 on first batch; 3 regenerated after 0.5x review. Editor time: ~3.5 hours including captions.

Lesson: food is a temporal consistency bully. Lock the plate.

### Case 2 — DTC mug launch landing loop

Brief: 8-second loop for hero header.

We I2V'd from a Nano Banana Pro still with logo stamp crisp. First motion prompt asked for "dynamic energy" and invented a hand. Second prompt banned hands and limited steam. Shipped.

Lesson: vague energy words invite extras. Ban the extras.

### Case 3 — B2B conference teaser

Brief: abstract network motion, no fake executives.

T2V worked because no SKU and no face. Two clips accepted of five. Cost was fine because no identity tax.

Lesson: abstract motion is where T2V earns its keep.

### Case 4 — Founder story attempt that failed

We tried T2V to "keep the founder consistent" across three scenes. It did not. We rebuilt from a photographed still sheet and I2V for subtle motion only (parallax, blink-free, camera drift). Less cinematic. More trustworthy.

Lesson: cameras still win when a specific real person is the product.

## 9. The Five Production Failures That Kill Video Campaigns

### Failure 1 — Animating a bad still

If the logo is soft in the still, motion will not invent sharpness. Fix stills first.

### Failure 2 — Writing novel prompts without timing

"Cinematic epic commercial" is not a prompt. CRAFT timing is a prompt.

### Failure 3 — Chasing length

A stable 6s clip beats an ambitious 16s morph. Editors can cut. Melts cannot be cut into trust.

### Failure 4 — No 0.5x QA

If you only watch at 1x on a phone while walking, you will ship crawls.

### Failure 5 — Measuring success as clips generated

Measure accepted seconds and revision rounds. A folder of 80 almost-clips is inventory, not progress.

## 10. Camera Grammar That Models Understand

Models respond better to boring camera language than to film-school poetry.

Useful:

- slow push-in / pull-out
- locked tripod
- slight orbit left 10 degrees
- static hold
- top-down settle

Risky:

- "dramatic handheld documentary energy"
- "complex crane that reveals destiny"
- whip pans on product labels
- orbit + zoom + subject walk simultaneously

One motion verb per clip is a good default. Stacking three camera moves is how you get geometry soup.

## 11. Audio, Captions, and Post

Generative video rarely ends at the mp4.

- Add captions in a real editor for readability.
- Score with licensed music; do not assume model audio is campaign-safe.
- Keep logo end cards as real design layers when possible.
- Preserve a still poster frame that already matches Brand Kit.

I treat generative clips as raw media. The finishing room still exists. Teams that skip finishing ship "AI look" even when the motion is fine.

## 12. Cost, Credits, and When Stock Still Wins

### When generative wins

- Brand-specific product motion
- Rapid variant testing
- Abstract / mood b-roll tied to palette
- No suitable stock exists for your SKU

### When stock or camera wins

- Real events and real people documentation
- Complex hand choreography
- Legal sensitivity around likeness
- Long-form narrative continuity

### Rough budgeting habit

Price the edit, not only the generate. Our internal rule: if editor hours are not in the estimate, the estimate is fiction.

## 13. Cross-Platform Specs

```text
Reels / Shorts / TikTok   9:16    1080x1920    6-12s common
Feed video                1:1 or 4:5          keep faces/logo center-safe
YouTube bumper            16:9                6s or 15s
Landing loop              16:9 or 1:1         clean loop needs clean end frame
Paid social               platform safe zones avoid top UI collision
```

Generate in the hardest ratio first when the same motion must live in multiple crops. Adapting 16:9 product orbits into 9:16 often amputates the pack.

## 14. Team Playbooks

### Solo

Batch stills in the morning, I2V after lunch, QA at 0.5x before dinner. Do not generate while answering Slack. Motion QA needs attention.

### Small team

Still owner can reject source frames. Motion owner owns CRAFT prompts and seed logs. Channel owner owns ratio crops.

### Agency

Put route rules in the SOW: exploration T2V vs production I2V. Clients understand cost when you show accept-rate math from a pilot.

## 15. 14-Day Pilot Plan

Days 1–2: baseline your current tool with one real brief (10 clips attempt).  
Days 3–5: I2V from carefully locked stills only.  
Days 6–8: T2V for abstract/mood only.  
Days 9–11: hybrid (2 T2V heroes + I2V system).  
Days 12–14: compare cost per accepted second; write route card.

No logs, no decision — only opinions.

## 16. Model Landscape Notes (2026 Production View)

I am not ranking models by Twitter screenshots. I am ranking them by how they fail in delivery.

### Sora-class cinematic T2V

Strong at world and camera language. Useful for mood films and pitch pieces. Identity permanence across separate generations remains a management problem, not a solved checkbox. Use for exploration and selected heroes.

### Runway-class directed motion

Strong when you think in shots and iterations. Good repair culture in the product workflow. Still benefits from short clip discipline.

### Kling / cinematic Asian-market stacks

Often excellent motion aesthetics for certain styles. Same temporal rules apply: short clips, hard constraints, 0.5x QA.

### Pika-class social-native tools

Fast for meme energy and lightweight social. Not my default for SKU-honest product orbits.

### Lovart video path

Wins when the still system and brand kit already exist. The advantage is not a claim that one video backbone beats every lab model on pure cinema. The advantage is production: ChatCanvas stills, Identity Lock, Touch Edit before motion, and a designer-operable loop.

If a vendor demo shows a perfect 20-second one-take with a stable hero product and a stable face, ask for the still references, seed discipline, and number of discarded takes. Discarded takes are part of the real cost.

## 17. Deep Dive: Product Video Paths

### Path V1 — White-sweep micro-orbit

Source: locked PDP still. Motion: 10–15 degree orbit or push-in. Ban hands. Ban reflections that invent extra logos. Duration: 5–6s.

### Path V2 — Lifestyle tabletop

Source: brand-locked lifestyle still with real SKU composite if needed. Motion: steam, light shift, slow push. Watch for food boil and cloth shimmer.

### Path V3 — Hands on product

Avoid generative hands unless you budget for pain. If hands are required, photograph them or accept high remake rates.

### Path V4 — Before/after transformation

Prefer two locked stills and a controlled transition over one T2V that "morphs the customer." Morphs are where bodies melt.

### Path V5 — Marketplace and performance ads

Many platforms compress aggressively. Soft logos die. Generate with thicker clearspace and test the export on a phone using cellular data, not only Wi-Fi on a retina desktop.

## 18. Deep Dive: Character and Founder Continuity

This is the most requested feature and the most overpromised.

What works today:

- Photograph or generate a still sheet (front, three-quarter, expression set).
- I2V for subtle motion only.
- Keep wardrobe locked in the still.
- Limit scene changes; change backgrounds in still space first when possible.

What fails:

- Asking T2V to "use the same woman from yesterday's clip" with no still binding.
- Multi-scene narrative with wardrobe changes in pure generation.
- Dialogue-heavy face closeups if you need trust (teeth and eyes are temporal victims).

If the person is the brand, budget a camera day. Use generative for b-roll and product motion around the real footage.

## 19. Prompt Library (Steal the Structure)

### Product push-in

"I2V from @[SKUStill]. Slow push-in 12%, tripod, 6 seconds, soft daylight, no hands, logo stamp remains sharp, ending frame freeze-safe."

### Steam / atmosphere

"I2V from @[HeroStill]. Gentle steam upward only, no liquid motion, no new props, 5 seconds, locked camera."

### Abstract brand motion

"T2V. Soft particle network over deep navy field, slow parallax, no people, no readable fake UI text, 6 seconds, 16:9, quiet luxury grade."

### Ending card prep

"I2V from @[PosterStill]. Minimal motion, hold composition, subtle light breathe, 4 seconds, leave right third clean for later text overlay in editor."

### Extension

"Continue from ending frame. Keep mug geometry identical. Steam only. No camera change. 4 more seconds."

## 20. QA Gates for Every Clip

1. Identity hold: subject recognizes itself at start and end.
2. Logo/label: readable on freeze frames at 1s intervals.
3. Texture boil: check wood, fabric, hair at 0.5x.
4. Physics: liquid, cloth, shadows behave believably enough for the channel.
5. Camera: one intended move; no accidental zoom-rescale.
6. Extras: no surprise hands, faces, or props.
7. Audio plan: silence is fine; random model audio is not automatically cleared.
8. Ratio safety: subject survives platform UI overlays.
9. Compression test: phone + cellular re-encode check.
10. Metadata/archive: name the file with model route + still id + date.

If gate 1 or 2 fails, the clip is not "almost done." It is a regenerate.

## 21. Naming and Archive

`brand_campaign_job_ratio_route_stillid_v##_status.mp4`

Example:

`harbor_spring26_V1_9x16_i2v_still14_v02_approved.mp4`

Store:

- source still
- CRAFT prompt
- seed/session if available
- reject reason if rejected

Without this, teams regenerate approved work and call it "iteration."

## 22. Client Scripts That Prevent Religious Arguments

### "We want a two-minute AI film by Friday"

"We can explore a trailer made of stable 6-second shots. A continuous two-minute generative one-take is a research risk, not a delivery promise. Here's a shot list with accept-rate assumptions."

### "Just make the founder walk through five locations"

"For a specific person, we should shoot plates or lock a still sheet and keep motion subtle. Pure T2V will create lookalikes, not continuity."

### "Why is this more expensive than stock?"

"Stock is cheap when it fits. Brand-true product motion often does not exist in stock. We price accepted seconds, including edit and QA."

## 23. Integration With Still Design Systems

Video does not replace Brand Kit discipline. It inherits it.

If your still system is messy, your video system will be expensive chaos. The cheapest video improvement I made in the last year was not a new model subscription. It was forcing Brand Kit honesty and still QA before anyone was allowed to click I2V.

Related reading inside our library:

- AI image model selection guide for still routing
- Amazon white-background guide when marketplace stills feed I2V
- Best agent for SBOs when the team needs an operating system, not a toy generator

## 24. Ethics, Disclosure, and Trust

- Do not present generative events as documentary reality.
- Be careful with likeness, minors, and implied endorsements.
- Disclose when channels or clients require it.
- Keep a human responsible for claims on screen.

Trust is a brand asset. Temporal melts are not the only way to lose it. Fake realism can lose it faster.

## 25. What Most Guides Skip

Generated clips are metadata-poor. No real lens EXIF, no true location, no trustworthy timestamp. If you run a media library, tag generative assets explicitly or your archive becomes fiction.

Also: model updates change failure modes. A route card should expire each quarter. Rerun a 10-clip pilot when the vendor ships a "new generation."

## 26. Worked Example: One Brief, Three Routes

Client: two-location pottery studio. Need: 1 landing loop, 8 Reels, 4 paid social cuts. Deadline: six days.

### Route A — T2V everything

Pretty clay-studio fantasies. Mug logos crawled. Hands appeared holding mugs that were not theirs. Accept: 2/15. Timeline slip.

### Route B — I2V from random website PNGs

Website PNGs were soft and oversharpened. Motion amplified the artifacts. Accept: 4/12.

### Route C — Lovart still lock + I2V (shipped)

Day 1–2: still system for three hero mugs. Day 3–4: I2V variants with CRAFT prompts. Day 5: edit, captions, compression tests. Day 6: revisions on copy only. Accept: 11/14 generative attempts. Editor hours: ~7 including finishing.

This is the route card evidence I now show in kickoffs.

## 27. Extended Pitfalls

### Pitfall: style references that fight the SKU

A film-reference still can overwrite product truth. Mark references as "grade only" vs "geometry lock."

### Pitfall: text in the video frame

Generative text in pixels remains a QA tax. Prefer captions and end cards in the editor.

### Pitfall: looping without an ending plan

A loop needs the last frame to match the first emotionally and geometrically. If it does not, edit a dissolve or redesign the still for loopability.

### Pitfall: overusing camera orbit on labels

Orbits that reveal a pack's side panel will expose any generative label nonsense. Keep orbits tiny for commerce.

### Pitfall: generating while hungry for novelty

Novelty hunting increases remakes. Lock a motion template for a campaign week, then vary lightly.

## 28. Scoring Rubric for Tool Pilots

Score 1–5:

1. Temporal stability
2. Instruction obedience (camera + bans)
3. Brand/SKU hold
4. Repair/extend usability
5. Cost per accepted second

Ship threshold: average ≥3.8 and temporal stability ≥4. A tool can win cinema and lose production.

## 29. Contractor Rules

1. No finals from exploration folders.
2. Source stills must be approved before I2V.
3. Deliver prompt + still id with every clip.
4. Payment milestone includes 0.5x QA pass.
5. One motion verb default unless creative director approves complexity.

## 30. Education vs Commerce Motion

Education can tolerate stylized motion and abstract metaphors. Commerce must protect SKU geometry and claim safety. Keep two defaults. Do not let a playful explainer style leak into PDP loops without a decision.

## 31. Accessibility

- Burned-in tiny text fails mobile readers; use real captions.
- Avoid seizure-hostile flicker.
- Do not rely on color alone for meaning in diagrams that move.
- If people are depicted, specify representation explicitly; silence reverts to defaults.

## 32. One-Page Route Card

```text
LOVART STUDIO — T2V / I2V ROUTE CARD (2026)

SKU / face continuity  -> I2V from locked stills (4-8s)
Abstract mood          -> T2V short clips
Pitch cinema           -> T2V exploration, not automatic production
Real person documentary-> camera
Default duration       -> 6s
Mandatory QA           -> 0.5x playback + logo freeze checks
Repair order           -> fix still, then motion; extend from clean end frame
Metric                 -> cost per accepted second

Never
  - animate a soft logo still
  - promise multi-scene identity without a still sheet
  - ship without compression test
```

## 33. Field Notes From Failed Takes (So You Skip Them)

Take 17: asked for "subtle life." Model added a cat. Ban animals if they are not in the brief.

Take 29: 12-second push-in. Frames 1–7 perfect. Frames 8–12 mug handle liquefied. Cut at 6s would have shipped. Greed did not.

Take 41: used a screenshot from Instagram as I2V source. Compression blocks became moving infection. Use original still exports.

Take 58: two camera moves + walking subject + steam. Rejected for geometry. One verb would have passed.

Take 70: beautiful T2V cafe scene that invented a competitor's cup colorway. Brand Kit was not in the loop. Pretty theft is still theft of focus.

## 34. How I Brief Editors When Clips Are Generative

I hand editors:

- approved clips
- poster frames
- banned cut patterns (do not slow to 20% if temporal boil appears)
- caption style sheet
- a note on which clips are loopable

Editors are not dumpsters for almost-media. If a clip needs them to "fix the melt in finishing," the clip failed QA.

## 35. Quarterly Default Refresh

Every quarter:

1. Run the same pottery-style pilot brief (or your equivalent).
2. Compare accept rate and cost per accepted second.
3. Update the route card.
4. Retire dead vendor habits.

Defaults that never expire become superstition.

## Related Resources

- [AI Image Model Selection 2026](/blog/ai-image-model-selection-guide-2026)
- [Amazon White Background AI Guide](/blog/amazon-requirements-ai-white-background-images)
- [Best AI Design Agent for SBOs](/blog/best-ai-design-agent-for-sbos-2026)
- [Lovart video generator](/tools/video-generator)


## 36. Shot Listing Like a Tiny Film Unit

Generative video fails when teams think in "make me an ad" and succeeds when they think in shots.

A shippable social ad is often:

1. Hook still motion (1–2s feel, even inside a 6s clip)
2. Product proof motion
3. End card freeze

That can be one clip with disciplined timing or three clips cut together. Cutting is allowed. Melting is not.

### Mini shot list template

```text
Shot 1 | I2V | 6s | push-in on mug | ban hands | 9:16
Shot 2 | I2V | 5s | steam only | locked camera | 9:16
Shot 3 | still+editor | 2s | end card | real typography
```

If a stakeholder insists on one continuous generative take, price the risk as a separate line item called "continuity research." Do not hide it inside "content package."

## 37. Negative Constraints Library

Copy these into prompts when relevant:

- no hands
- no extra fingers
- no new logos
- no readable fake UI text
- no brand-name misspellings
- no camera shake
- no cutaways
- no people in background
- no warping of label geometry
- no morphing between products
- keep horizon locked
- keep subject scale stable

I keep them in a note called "boring bans." Boring bans print money.

## 38. Seed Discipline and Variation Strategy

When a clip almost works, change one variable:

- seed only, or
- camera only, or
- duration only

Changing prompt, seed, camera, and model at once makes learning impossible. For variant ads, lock motion grammar and vary stills or background colorways inside Brand Kit ranges.

## 39. Color, Grade, and Brand Drift in Motion

Motion reveals grade drift that stills hide. A teal shift across six seconds can make a brand look like a different company mid-clip.

Controls:

- declare grade references as "grade only"
- avoid stacking a second aesthetic reference that fights Brand Kit
- check first, middle, and last frames in a grid
- if mid-clip grade wanders, shorten or regenerate; do not "fix in color" as a fantasy plan unless you have a real finishing pipeline

## 40. Extending Clips Without Destroying Them

Extension works when the ending frame is clean. Extension fails when you extend from a melt.

Procedure:

1. Scrub to last clean frame.
2. Export that frame if needed.
3. Extend with "continue, no redesign, same camera."
4. QA the seam at 0.5x.

If the seam shows a wardrobe or handle pop, cut before the seam and accept a shorter clip. Short and stable beats long and haunted.

## 41. Using Generative Video in Performance Marketing

Performance teams want volume. Generative can provide volume only if templates exist.

Weekly performance template example:

- 3 product push-ins from the same still family
- 3 lifestyle I2V with different backgrounds but locked SKU
- 2 abstract transitions for thumb-stop tests
- captions varied in editor, not in pixels

Kill criteria: if CPA tests show creative fatigue, change still composition or first-frame poster before you change models. First frames win auctions more often than model brand names.

## 42. Storyboarding With Still Frames First

My cheapest preflight is a six-frame still storyboard in ChatCanvas before any I2V spend. Stakeholders approve faces, packs, and compositions as stills. Only then do we spend motion credits.

This prevents the most expensive meeting in creative ops: arguing about motion while the underlying still was never approved.

## 43. Common Myths

Myth: longer context windows fixed continuity.  
Reality: better, not solved. Still sheets still win.

Myth: 4K output means production ready.  
Reality: 4K melt is still melt.

Myth: one perfect prompt replaces a workflow.  
Reality: workflows absorb variance; prompts do not.

Myth: if it looks good on the vendor site, it will look good on Meta compression.  
Reality: test exports on a phone.

Myth: AI video means no editor.  
Reality: editors become more valuable when generation is cheap and judgment is scarce.

## 44. Studio Scheduling Template

```text
Monday     still generation + still QA
Tuesday    I2V batch A + 0.5x QA
Wednesday  repairs / extensions / selects
Thursday   edit + captions + compression tests
Friday     revisions + archive + route notes
```

If you generate every day and QA never, you are building a haunted hard drive.

## 45. When to Stop and Shoot

Stop generative attempts when:

- hands are story-critical
- a specific real person must be unmistakably themselves across scenes
- legal requires captured reality
- you have failed two structured pilots with locked stills and short clips

Stopping is professionalism. Infinite generation is avoidance.

## 46. Detailed CRAFT Walkthrough: Coffee Mug Campaign

Context: Harbor Batch spring campaign, morning window light, cream and deep brown palette, quiet cafe, no neon, no cyberpunk, no rainy blade-runner nonsense.

Reference: @[MugStillA] geometry and logo lock; @[GradeRef] for soft daylight only; anti-reference @[CompetitorAd] meaning do not copy that exaggerated steam explosion.

Action: steam rises slowly from mug; surface liquid stays calm; no spoon; no hand; no second mug entering frame.

Framing: 9:16, subject centered lower third safe from UI, slow push-in approximately 12 percent, tripod-stable, no orbit.

Timing: 0–1.5s near-static hold for thumb-stop readability; 1.5–5.5s push; 5.5–6.5s settle; ending frame must be freeze-safe for end-card overlay in editor.

Result expectations: if logo softens, regenerate from a sharper still rather than "enhancing" in motion. If steam becomes fog that erases the badge, reduce atmosphere language and ban heavy fog.

## 47. Detailed CRAFT Walkthrough: Abstract B2B Teaser

Context: OpsForum 2026 teaser, deep navy field, teal accents, enterprise-calm, no literal office comedy.

Reference: brand gradient sheet only; no people references.

Action: soft nodes connect into a network; motion is parallax, not explosion; no UI screens with fake metrics.

Framing: 16:9, slow lateral parallax, locked horizon.

Timing: 6s, loopable if first and last frames are designed as cousins; if not loopable, plan a dissolve in edit.

This is where T2V shines because there is no SKU tax and no face tax.

## 48. Budget Spreadsheet Columns Worth Keeping

Track these columns per batch:

- brief id
- route (T2V/I2V/hybrid)
- source still id
- model/vendor
- seconds generated
- seconds accepted
- editor hours
- credit cost
- reject reasons (tags)
- channel destination

After twenty batches, your tags will teach you more than any keynote. In our studio, "hands" and "logo crawl" were the top reject tags for a full quarter. That single insight changed our default bans and saved more money than switching vendors twice.

## 49. Training Juniors Without Destroying Margins

Juniors should not learn on client SKUs. Give them a synthetic brand kit and a closed brief. Require route card compliance. Review their 0.5x QA notes, not only their pretty selects.

Promotion criterion: can they explain why a clip failed in one sentence that matches a reject tag? If they can only say "it looks weird," they are not ready to spend client credits.

## 50. Closing Operating Manifesto for Motion

1. Stills first when identity matters.
2. Short clips beat hopeful epics.
3. One camera verb by default.
4. Ban extras explicitly.
5. QA at half speed.
6. Price editing and QA.
7. Expire defaults each quarter.
8. Cameras still exist for reality.

If you internalize only the stills-first rule, your accept rate will rise even on a mediocre week.


## 51. Pre-Mortem: How a Motion Sprint Dies

A motion sprint dies when the kickoff starts with model names. It dies when the shared drive fills with unlabelled mp4s. It dies when stakeholders approve a T2V pitch film and then expect the same identity permanence in twelve performance variants without a still sheet.

Run a pre-mortem in fifteen minutes:

- Where will hands appear unwanted?
- Which logo is most likely to crawl?
- Which ratio will crop the pack?
- Who has veto on source stills?
- What is the maximum clip length allowed this week?

Write answers in the brief. Briefs prevent hauntings.

## 52. Example Weekly Prompt Pack (Coffee)

Prompt pack A: push-in, no hands, 6s, 9:16, steam light.  
Prompt pack B: static steam only, 5s, 9:16.  
Prompt pack C: tiny orbit 8 degrees, 6s, logo-safe.  
Prompt pack D: abstract beans-to-network metaphor T2V, 6s, 16:9, no fake text.

Do not invent twenty prompts. Invent four and execute them across still variants. Consistency in motion grammar makes A/B tests interpretable.

## 53. Handling Stakeholder "Make It More Cinematic"

Cinematic often means "add three camera moves and a crane." Translate the request:

- richer light on the still first
- cleaner grade reference
- slightly slower push
- better poster frame

If they still want chaos camera, schedule an exploration clip labelled non-delivery. Protect the production batch.

## 54. File Types and Delivery Hygiene

Deliver:

- master progressive mp4 (h.264 or platform preference)
- poster frame png from a clean freeze
- caption file if required
- still source used for I2V

Do not deliver only a compressed social export. Archives need masters. Future you will need to re-cut.

## 55. Legal Notes Without Playing Lawyer

I am not your counsel. Operationally:

- licensed music only
- avoid implied celebrity cameos
- be careful generating recognizable private property as "your store"
- disclose generative methods when a channel or client contract requires it
- keep human approval on product claims shown on screen

Put these checks next to QA, not in a forgotten PDF.

## 56. Comparing Against a Camera Day Honestly

Camera day costs more upfront and can still be cheaper when:

- founder face continuity is mandatory
- hands demonstrate a product
- real customers and real spaces matter

Generative is cheaper when:

- SKU motion is simple
- variants are many
- abstract visuals dominate

The mature studio offers both. Ideology is not a pricing strategy.

## 57. Stress Test: The Logo Freeze Grid

Export frames at 0s, 1s, 2s, 3s, 4s, 5s, end. Put them in a contact sheet. If any freeze fails logo readability, the clip fails. This grid catches crawls that scrubbing misses because your brain fills gaps in motion.

## 58. Stress Test: The Crop Gauntlet

Take the same clip through 9:16, 1:1, and 16:9 center crops. If the product leaves safe zones in any crop you promised the client, regenerate with more headroom or make ratio-specific clips. One master to rule all ratios is a myth for product motion.

## 59. What I Want Vendor Roadmaps to Optimize

Not longer fantasy takes. Better identity hold at 6–8s. Better logo stability. Better extension seams. Better control over "do not add hands." Better provenance metadata for archives. Until then, workflows beat wishlists.

## 60. Final Field Checklist Before You Hit Publish

- route matches job class
- source still approved
- CRAFT prompt archived
- duration ≤ policy max
- 0.5x QA done
- logo freeze grid done
- compression test on phone done
- captions/audio plan done
- file named and archived
- reject tags updated if anything failed along the way

If you cannot check these boxes, you are not publishing a video. You are publishing hope.


## 61. Appendix: Motion Brief One-Pager

```text
Campaign:
Job class: (SKU motion / abstract / founder / performance)
Route: I2V / T2V / hybrid
Source still ids:
Duration max:
Ratio(s):
Camera verb (one):
Bans:
Must hold:
Success metric: accepted seconds
QA owner:
Edit owner:
Due date:
```

Fill this before credits spend. If a producer cannot fill it, they are not ready to generate.

## 62. Appendix: Reject Tag Dictionary

- hands_unwanted
- logo_crawl
- texture_boil
- physics_cheat
- camera_stutter
- ending_collapse
- identity_drift
- extra_prop
- fake_text
- compression_fail
- crop_fail
- audio_unusable

Tags make retrospectives fast. "It looks weird" does not.


## 63. A Second Worked Example: SaaS Feature Teaser

Brief: 8-second teaser for a dashboard feature, no fake metrics that imply false results, no invented customer faces.

Route: T2V abstract UI motion was tempting and dangerous because fake dashboards hallucinate numbers. We built a still in Lovart with intentional blurred modules and no readable KPIs, then I2V'd a slow parallax. Accept on second try.

Lesson: if text can become a claim, keep it out of generative pixels. Blur is not laziness; it is risk control.

## 64. A Third Worked Example: Retail Promo Variants

Brief: twenty 6-second variants for a weekend promo.

We locked three still compositions and ran the same push-in CRAFT pack across colorway-safe background changes. Editors swapped caption offers. Generative provided motion; marketing provided offers. Accept rate 16/20. The four rejects were texture boil on a fabric backdrop — we banned that backdrop mid-week.

Lesson: volume comes from template discipline, not from prompt chaos.

## 65. Why Half-Speed QA Feels Embarrassing and Still Works

Teams skip 0.5x because it feels pedantic. Pedantry is cheaper than a client seeing a melting handle in a paid comment thread. Make half-speed a ritual with a checkbox in your project tool. Rituals beat inspiration when money is on the line.

## 66. Last Word Before the FAQ

If you came for a single vendor crown, you came to the wrong guide. If you came for a way to ship motion without haunted frames, start tomorrow with one locked still, one camera verb, one six-second I2V, and a half-speed review. That single loop will teach your team more than another week of bookmarking demo reels.


## 67. Production Calendar Language for Motion Weeks

When you put generative video on a content calendar, write the calendar like ops, not like vibes.

Bad calendar line: "AI video for launch."

Good calendar line: "I2V batch from stills 12–14; six 6s push-ins; captions offer A/B; QA owner Mina; publish Thu."

The second line can be staffed. The first line becomes a Slack argument on Wednesday night.

## 68. How Many Clips Should You Generate to Get Ten Accepts?

Internal heuristic after locked stills and short-clip policy:

- abstract T2V: generate about 1.8x what you need
- SKU I2V: generate about 1.4x what you need
- founder-sensitive motion: generate 2.5x or switch to camera

If you are generating 5x and accepting 1x, your stills, bans, or duration policy are wrong. Do not buy another subscription until those three are audited.

## 69. The Editor's Veto

Give editors veto power on generative selects. Designers fall in love with motion they fought for. Editors see the cut. If an editor says a clip cannot be cut without exposing a melt, believe them. Rebuild. The veto saves accounts.

## 70. Closing Note on Taste Versus Stability

Taste gets you hired. Stability keeps you hired. Generative video culture overweights taste because demos are taste contests. Client delivery is a stability contest with taste as a constraint. Optimize for both, but never trade stability away in the last hour before a launch.


## 71. Glossary for Motion Reviews

**Accepted second** — a second of footage that can ship without generative remake.  
**Anti-reference** — an example of motion or style you explicitly do not want.  
**Clean ending frame** — a final frame stable enough to freeze, extend, or overlay.  
**Continuity research** — paid exploration for hard identity problems, not a hidden production promise.  
**CRAFT** — context, reference, action, framing, timing.  
**Half-speed QA** — reviewing at 0.5x to expose crawls and boils.  
**Identity crawl** — slow morphing of face, logo, or product across frames.  
**I2V** — image-to-video.  
**Motion verb** — the single primary camera or subject action in a clip.  
**Poster frame** — still used for platform thumbnails and reviews.  
**Route card** — one-page defaults for which jobs use which generation path.  
**Still sheet** — a set of locked images used to bind identity across clips.  
**T2V** — text-to-video.  
**Texture boil** — shimmering unstable surfaces in motion.  
**Truth still** — a source image trusted for SKU geometry and branding.

Share this glossary in kickoffs so review comments use the same language.


## 72. What To Do in the Next 90 Minutes

Minute 0–15: pick one real SKU still and run still QA.  
Minute 15–30: write one CRAFT prompt with bans.  
Minute 30–55: generate three 6-second I2V attempts.  
Minute 55–70: half-speed QA and logo freeze grid.  
Minute 70–90: archive selects, tag rejects, write one route note.

If you finish that loop, you have started a production practice. If you instead watch twenty demo reels, you have only refreshed your envy.


## 73. Reminder: Delivery Is the Product

Demos reward surprise. Delivery rewards boredom in the right places: stable logos, short clips, predictable camera verbs, and archives someone else can reopen next quarter. If your motion practice feels slightly bureaucratic, you are probably doing it correctly.








## 74. Route Card Habit

If your team argues about models again this week, reopen the route card before you reopen the vendor pricing page. Model debates without a job class and an accept-rate log are entertainment. Route cards turn the same energy into a decision that juniors can execute without a meeting.

## 75. Keep the Half-Speed Habit Loud

Half-speed QA feels nerdy until the first time it catches a logo crawl in a paid ad. Put it in the checklist software your team already uses. Do not leave it as a tribal memory. Tribal memories evaporate on holidays and freelancer weeks.

## 76. Ship the Boring Clip

When two clips are close, ship the more stable one even if the other is slightly more dramatic. Drama that melts in comments is not drama. It is churn. Stability compounds across a campaign week; drama usually does not. Stability is a creative choice, not the absence of taste.

## FAQ

### What is the difference between text-to-video and image-to-video?

T2V invents appearance and motion from words. I2V animates a still and is usually better when brand or SKU continuity matters.

### Which text-to-video model is best in 2026?

Best for what job? Cinematic exploration, social volume, or SKU-honest product motion are different answers. Pick by job class and measure accepted seconds.

### How do I write prompts that produce usable video?

Use CRAFT: context, reference roles, action order, framing, timing. Ban extras. Prefer one camera move.

### Why do AI videos melt?

Temporal consistency limits. Shorten clips, lock stills, reduce stacked motions, QA at 0.5x.

### Can text-to-video replace stock footage?

Sometimes, for brand-specific or abstract b-roll. Not for documentary reality.

### How does image-to-video work with Lovart?

Lock a strong still in ChatCanvas, repair with Touch Edit if needed, then generate short motion with hard constraints.

### What resolution and frame rate should I target?

1080p24 is the production workhorse for most social. Higher resolution does not fix identity crawl.

### Can I keep a character consistent across multiple clips?

Reliably only with a still sheet and I2V discipline. Pure multi-clip T2V identity is not a safe promise.

### How much does generation cost?

Credits vary widely; editor hours dominate weak workflows. Track cost per accepted second.

### Will text-to-video replace cameras?

No for capturing real events and specific people honestly. Yes as a growing source of motion graphics and productized b-roll.

## Final Recommendation

Default production route:

1. Build still truth in Lovart.
2. I2V for 4–8s brand motion.
3. Reserve T2V for abstract/exploratory heroes.
4. QA at 0.5x.
5. Finish captions and audio in a real editor.
6. Log accepted seconds.

I did not learn this from a keynote. I learned it from frame 47. If you only take one habit from this guide, make it the half-speed review before anything leaves the studio.

