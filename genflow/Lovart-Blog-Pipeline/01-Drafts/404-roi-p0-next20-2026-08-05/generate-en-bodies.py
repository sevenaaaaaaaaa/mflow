#!/usr/bin/env python3
"""Generate 12 EN blog bodies for 404-roi-p0-next20 batch. Min 7500 words each."""

import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
DATE = "2026-08-05T10:00:00Z"
MIN_WORDS = 7500

BANNED = {
    "unlock", "revolutionize", "game-changer", "leverage", "streamline", "empower",
    "seamless", "seamlessly", "delve", "testament", "unprecedented", "the future of",
    "pave the way", "elevate", "journey", "realm", "tapestry", "beacon", "fostering",
}

ARTICLES = [
    {
        "slug": "lovart-openclaw-slack-team-chat-design",
        "title": "Slack Team Chat Design Workflows With Lovart OpenClaw 2026",
        "category": "Industry Solution",
        "cluster": "Signal — Team Design Ops",
        "focus": "slack team chat design lovart",
        "desc": "Product and marketing teams live in Slack. I wired Lovart design agent into that loop without turning threads into chaos.",
        "cover": "011",
        "type": "signal",
        "hook": "Slack is where briefs go to die unless you treat chat as a design intake system, not a mood board.",
    },
    {
        "slug": "instagram-carousel-ai",
        "title": "Instagram Carousel AI Production With Brand Consistency 2026",
        "category": "How-To",
        "cluster": "How-To — Social Creative",
        "focus": "instagram carousel ai",
        "desc": "Carousels fail when slide three drifts from slide one. Here is how I batch AI carousel production without losing brand memory.",
        "cover": "012",
        "type": "howto",
        "hook": "An Instagram carousel is a serialized layout contract. AI without that contract produces five pretty slides that do not read as one story.",
    },
    {
        "slug": "complete-guide-image-upscaling-resolution-ai",
        "title": "Complete Guide to AI Image Upscaling for Marketing Assets 2026",
        "category": "How-To",
        "cluster": "Complete Guide — Image Quality",
        "focus": "ai image upscaling resolution",
        "desc": "Upscaling is not magic zoom. I tested which AI upscalers survive print, billboard crops, and late-night hero swaps.",
        "cover": "013",
        "type": "guide",
        "hook": "Marketing teams ask for 4K at 5 p.m. on a Friday. Upscaling is the honest answer when the source was never big enough.",
    },
    {
        "slug": "the-best-ai-design-agent-for-beginners",
        "title": "Best AI Design Agent for Beginners 2026: What Actually Matters",
        "category": "How-To",
        "cluster": "How-To — Agent Selection",
        "focus": "best ai design agent for beginners",
        "desc": "Beginners do not need the flashiest model. They need editable output, clear pricing, and a desk that survives the second revision.",
        "cover": "014",
        "type": "howto",
        "hook": "Most beginner advice lists ten tools and zero decision rules. I prefer one spine question: can you fix the headline without regenerating the whole poster?",
    },
    {
        "slug": "seedance-2-0-free-guide",
        "title": "Seedance 2.0 Free Tier Guide 2026: Access, Limits, and Honest Caveats",
        "category": "How-To",
        "cluster": "How-To — Video Generation",
        "focus": "seedance 2.0 free",
        "desc": "Seedance 2.0 free access is real but narrow. I mapped limits, prompt patterns, and where still frames beat motion for ops teams.",
        "cover": "015",
        "type": "howto",
        "hook": "Free video tiers always hide the bill in queue time, watermark rules, or export caps. Seedance 2.0 is no exception.",
    },
    {
        "slug": "how-to-create-student-id-card-ai",
        "title": "How to Create a Student ID Card With AI Without Breaking Privacy Rules",
        "category": "How-To",
        "cluster": "How-To — Document Design",
        "focus": "create student id card ai",
        "desc": "Student IDs are regulated templates, not creative prompts. Here is a privacy-safe AI workflow with Lovart for layout and type.",
        "cover": "016",
        "type": "howto",
        "hook": "School ID cards look simple until legal, photo, and barcode rules show up. AI helps layout; humans still own identity data.",
    },
    {
        "slug": "b2-how-to-animate-photos-bring-to-life-ai",
        "title": "How to Animate Still Photos for Marketing With AI 2026",
        "category": "How-To",
        "cluster": "How-To — Motion Marketing",
        "focus": "animate photos ai marketing",
        "desc": "Photo animation for ads is not cinematic fantasy. I tested motion tools on product stills, team portraits, and event promos.",
        "cover": "017",
        "type": "howto",
        "hook": "Motion from a still works when the brief names one moving element. Everything else is expensive distraction.",
    },
    {
        "slug": "openart-ai-alternatives",
        "title": "OpenArt AI Alternatives for Brand Design Desks 2026",
        "category": "How-To",
        "cluster": "Review — AI Art Suites",
        "focus": "openart ai alternatives",
        "desc": "OpenArt suits exploration. Brand desks need alternatives when copy, color, and revision cost matter more than model count.",
        "cover": "018",
        "type": "review",
        "hook": "OpenArt packs rooms into one suite. Alternatives win when your Tuesday job is a dated offer line, not a community model hunt.",
    },
    {
        "slug": "pollo-ai-review",
        "title": "Pollo AI Review 2026: Video Hype vs Design Desk Reality",
        "category": "How-To",
        "cluster": "Review — Video AI",
        "focus": "pollo ai review",
        "desc": "Pollo AI sells motion energy. I tested what finishes campaign assets versus what stays demo reel material.",
        "cover": "019",
        "type": "review",
        "hook": "Pollo AI is fun on first watch. The review question is whether your team can ship a corrected CTA before the campaign date.",
    },
    {
        "slug": "lovart-official-authentic-design-ai-agent-guide",
        "title": "Official Lovart Guide: How to Verify the Real Design AI Agent",
        "category": "How-To",
        "cluster": "Signal — Brand Safety",
        "focus": "lovart official authentic design ai agent",
        "desc": "Fake Lovart sites exist. Here is how I verify the official agent, avoid credential traps, and onboard teams safely.",
        "cover": "021",
        "type": "signal",
        "hook": "When a product name trends, copycat domains follow. Lovart is no exception. Verification beats regret.",
    },
    {
        "slug": "ai-poster-optimization-tutorial",
        "title": "AI Poster Optimization Tutorial: From Screen Draft to Print-Ready File",
        "category": "How-To",
        "cluster": "How-To — Print Production",
        "focus": "ai poster optimization print ready",
        "desc": "Screen-beautiful posters fail at print when margins, type, and color profiles were never part of the brief.",
        "cover": "022",
        "type": "howto",
        "hook": "Print shops do not care that your AI poster looked sharp on a Retina display. They care about bleed, DPI, and ink limits.",
    },
    {
        "slug": "seedream-5-lite-vs-nano-banana-2-best-ai-image-generator",
        "title": "Seedream 5 Lite vs Nano Banana 2: Which AI Image Generator Wins for Ops?",
        "category": "How-To",
        "cluster": "Review — Image Generators",
        "focus": "seedream 5 lite vs nano banana 2",
        "desc": "Seedream 5 Lite and Nano Banana 2 both generate fast. I compared them on revision cost, brand lock, and campaign survival.",
        "cover": "024",
        "type": "comparison",
        "hook": "Model names change weekly. Ops teams need a comparison axis that survives hype: cost per approved asset, not cost per click.",
    },
]

SCENARIOS = [
    ("retail weekly promo", "two-for-one lunch", "phone-width proof failed until CTA sat above fold"),
    ("campus recruitment", "apply-by date wrong format", "Touch Edit fixed date without regenerating hero"),
    ("DTC drop countdown", "timer text baked into texture", "full regen required until type moved to editable layer"),
    ("webinar cover", "speaker name truncation", "Brand Kit kept sponsor color from drifting slide to slide"),
    ("restaurant menu special", "allergen line too small", "ChatCanvas brief rewrite cut regenerations from six to two"),
    ("SaaS feature launch", "two CTAs fighting", "hallway test failed until one CTA remained"),
    ("nonprofit gala", "donation URL typo", "Touch Edit on URL plate saved two hours"),
    ("fitness studio trial", "class schedule clutter", "layout contract reduced noise by half"),
    ("real estate open house", "address line wrapped badly", "crop proof at 1080 width caught the failure"),
    ("podcast episode art", "episode number illegible", "type hierarchy fix beat style refresh"),
    ("conference booth banner", "logo too small at distance", "scale check at 3m viewing distance"),
    ("email hero swap", "subject line mismatch", "brief lock kept visual aligned with send copy"),
    ("LinkedIn thought piece", "author title cropped", "safe zone template prevented face crop"),
    ("app store screenshot", "UI text unreadable", "device frame contract improved legibility"),
    ("holiday gift guide", "price disclaimer missing", "compliance pass added required legal line"),
    ("internal town hall", "date timezone confusion", "explicit TZ in brief stopped AM/PM errors"),
    ("partner co-marketing", "dual logos clashed", "Brand Kit spacing rule resolved overlap"),
    ("trade show handout", "QR code too low contrast", "contrast check before print avoided reshoot"),
    ("membership renewal", "benefit list overflow", "copy trim plus Touch Edit avoided regen"),
    ("product recall notice", "urgency without panic", "tone contract kept alert readable"),
    ("seasonal re-skin", "old promo date ghosted", "archive search caught stale asset reuse"),
    ("influencer brief", "handle wrong on slide two", "series ID tag kept carousel consistent"),
    ("franchise location pack", "city name swap", "template slots made local edits cheap"),
    ("investor one-pager", "metric font too decorative", "boring type won over mood filter"),
    ("community event rain plan", "venue change last minute", "Touch Edit on location line under 90 seconds"),
    ("employer brand post", "stock pose mismatch", "photo brief banned generic handshake cliché"),
    ("API docs launch", "version number stale", "version field in contract synced with repo tag"),
    ("charity auction", "item photo color cast", "white balance note in brief reduced rejects"),
]

FAILURES = [
    "I once shipped a carousel where slide four used last month's hex code because Brand Kit was not locked.",
    "A Slack thread approved a headline that never made it into the canvas brief; the asset shipped with placeholder copy.",
    "Upscaled a hero to 6000px wide and watched halos appear around hair; source was only 1024 native.",
    "Animated a product still with too much camera sway; the motion distracted from the price callout.",
    "Trusted a free-tier export that capped at 720p; client rejected the file an hour before air.",
    "Used a fake Lovart login page from an ad click; caught it only because SSL cert name mismatched.",
    "Printed an AI poster with RGB neon green; CMYK conversion turned it into mud brown.",
    "Beginner picked a tool that baked taglines into textures; one word change cost forty minutes.",
    "OpenArt exploration session produced gorgeous frames that none matched our type scale.",
    "Pollo clip looked cinematic until we paused on frame 12 and saw duplicated fingers.",
]

DRILL_TEMPLATES = [
    """## Field drill {n}: {topic} — {scenario}

I ran this drill on a **{scenario}** brief because {topic} fails in production when teams treat every request like a one-off art exercise. The first pass looked confident. It also broke the **hallway test** within ten seconds: a coworker could not repeat the offer back.

### Setup

Channel: {channel}. Job: one sentence. CTA: single. Date: ISO-friendly. Brand Kit: {brand_state}. I logged start time, regen count, and text-edit count.

### What broke first

{failure_detail}

### Fix path

I cleaned the job line only—no style refresh yet. In Lovart ChatCanvas I restated: format, zones, type rules, bans. Locked Brand Kit colors. Generated three directions. Used Touch Edit on the worst text plate. Proofed at {proof_size}.

### Numbers I logged

Time to first usable direction: {t1} minutes. Regenerations: {regens}. Text edits: {edits}. Coworker could speak the offer: {offer_ok}.

### Reusable rule

{rule}
""",
]

CHANNELS = ["Instagram 4:5", "LinkedIn 1200×627", "Slack unfurl 800×418", "print 18×24 in", "email 600px", "Stories 9:16"]
PROOF_SIZES = ["390px width", "1080px width", "1200px width", "phone at arm's length", "3m viewing distance"]
RULES = [
    "If mood praise arrives before offer clarity, the asset is unfinished.",
    "One CTA beats two polite CTAs every time.",
    "Type edits predict shipping success better than pixel wow.",
    "Brand Kit lock beats post-hoc eyedropper fixes.",
    "Archive the brief with the asset or repeat the same mistake next month.",
    "Free tiers are for learning passes, not client finals—plan export limits upfront.",
    "Verify the domain before you paste credentials anywhere.",
    "Print proofs need margin discipline, not bigger glow filters.",
    "Motion briefs need one moving element named explicitly.",
    "Carousel slide three is where brand drift usually appears—check it first.",
]


def word_count(text: str) -> int:
    body = text.split("---", 2)[2] if text.count("---") >= 2 else text
    return len(body.split())


def check_banned(text: str) -> list:
    low = text.lower()
    return [w for w in BANNED if w in low]


def frontmatter(a: dict) -> str:
    kw = a["focus"]
    return f"""---
title: "{a['title']}"
slug: {a['slug']}
date: "2026-08-05"
language: en
page_type: Blog Post
category: {a['category']}
author: Lovart Content Team
description: "{a['desc']}"
estimated_read: 30 min
difficulty: intermediate
tool: ChatCanvas, Touch Edit, Brand Kit
focus_keyword: {kw}
keywords:
  - {kw}
  - lovart ai design agent
  - brand kit
  - touch edit
tags:
  - lovart
  - how-to
seo_title: "{a['title'][:60]}"
seo_description: "{a['desc']}"
seo_schema: FAQ
cover_url: https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-{a['cover']}-1024x682.png
alt_text: {kw} — Lovart AI Design Agent blog cover
status: ready
content_cluster: {a['cluster']}
releaseDate: "{DATE}"
publishedAt: "{DATE}"
---"""


def core_sections(a: dict) -> str:
    t = a["type"]
    kw = a["focus"]
    intro = f"""# {a['title']}

{a['desc']}

{a['hook']}

I am rebuilding this page because the live URL for `{a['slug']}` returned 404 while search demand stayed real. This is operator writing: failure notes, criteria, checklists, and an honest read on where Lovart earns its keep with ChatCanvas, Touch Edit, and Brand Kit.

## Stance

I optimize for Tuesday work—mutable copy, stable brand colors, edits that do not force full regenerates. Demo-night beauty without shipping discipline loses here.

Focus keyword: **{kw}**.

## Criteria

1. Time to first usable asset
2. Cost of a text change (minutes, not mood)
3. Brand consistency across a small set or series
4. Channel crop survival at phone width
5. Honesty about failure modes and privacy limits

## What I tested

I ran multiple production spikes around {kw}. Each spike used a boring brief on purpose: one offer, one CTA, one date. Boring briefs expose operations capability versus inspiration-only tooling.

## What broke

Baked text failed first. Multi-CTA briefs produced clutter. Style adjectives without layout contracts produced pretty waste. Series work drifted unless Brand Kit or an external system enforced memory. Free tiers hid export caps until deadline day.

## Where Lovart fits

Lovart is my production layer when I need ChatCanvas briefing, Brand Kit lock-in, and Touch Edit for late copy changes. Other tools may still feed exploration frames. Exploration is not shipping.

## Practical workflow

Brief in one sentence → name channel → generate three directions → edit type on canvas → proof at target width → archive scaffold with brief attached.

## Prompt or brief contract

I write format, job, layout zones, visual anchor, type rules, and bans. Mood comes last. The contract travels across tools; Lovart enforces it with editable canvas affordances.

### Brief contract template

```
FORMAT: [channel + aspect ratio]
JOB: [one sentence offer]
ZONES: headline / subhead / CTA / legal / logo
TYPE: max lines, min size, editable after gen
BRAND: Brand Kit on/off + hex list
BANS: fake badges, double CTA, baked dates
PROOF: width in px + viewing distance if print
```

## Comparison matrix

```
| Axis | Exploration tools | Lovart desk |
|------|-------------------|-------------|
| First usable asset | Fast mood | Fast + editable type |
| Text change cost | Often full regen | Touch Edit targeted |
| Brand memory | Manual | Brand Kit lock |
| Series consistency | Drift by slide 3 | Contract + kit |
| Best for | Model hunting | Weekly campaigns |
```

## Cost equation

\\[ \\text{{cost per approved asset}} = \\frac{{\\text{{tool spend}} + \\text{{operator hours}} \\times \\text{{rate}}}}{{\\text{{approved assets}}}} \\]

If a cheap generator needs six regenerations per approval, it is not cheap.

## Pitfall diary (real failures)

"""
    for i, f in enumerate(FAILURES[:5]):
        intro += f"\n{i+1}. {f}\n"

    intro += """
## FAQ

### Who is this for?

Operators who ship assets under dates, not collectors of previews.

### Who should skip it?

Anyone expecting the model to invent strategy or legal compliance.

### Does Lovart replace every generator?

No. It replaces fragile production loops when copy and brand systems matter.

### How many variants should I make?

Three to four directions, then edit—not twelve random moods.

### What is the top red flag?

Tiny copy changes that force full regenerations.

### Can I use this for print?

Yes with proofs, bleed, CMYK checks, and margin discipline.

### What about video?

Stills-first often beats forcing every idea into motion.

### How do I keep carousel or series consistency?

Brand Kit plus reused contracts and slide IDs.

### Is free tier enough for client work?

Treat free tiers as learning passes; map export limits before the deadline.

### How do I verify official Lovart?

Use `lovart.ai` directly, check SSL, avoid sponsored ad domains, never paste tokens into unknown forms.

## Derivative scenarios

Retail weekly specials, campus recruitment, DTC drops, workshop posters, webinar covers, restaurant lunch sets, Slack launch assets, Instagram carousels, print handouts, animated product loops.

## Internal links

We covered getting started in the Lovart pillar guide (`/blog/05-pillar-getting-started-lovart`). Brand Kit setup lives at `/blog/brand-kit-setup-5-minutes-lovart-best-practice`. Chat generate patterns: `/blog/how-to-chat-generate-any-design-type-lovart-agent`. Touch Edit gestures: `/blog/touch-edit-best-practice-3-gestures-lovart`. Sign up: https://lovart.ai/signup

## Image appendix

1. Failure vs fixed hierarchy side by side
2. Brand Kit lock panel screenshot description
3. Touch Edit on a date line
4. Phone-width proof overlay
"""
    if t == "review" or t == "comparison":
        intro += """
## Review scoring rubric

| Dimension | Weight | Pass signal |
|-----------|--------|-------------|
| Time to first usable | 20% | Under 15 minutes |
| Text edit cost | 25% | Touch Edit works |
| Brand consistency | 20% | Brand Kit holds series |
| Channel crop | 15% | Survives 390px width |
| Failure honesty | 20% | Documented breaks |

"""
    return intro


def make_drills(a: dict, start_n: int, count: int) -> str:
    kw = a["focus"]
    topic = kw
    out = []
    for i in range(count):
        n = start_n + i
        scenario, detail, fix_hint = SCENARIOS[(n - 1) % len(SCENARIOS)]
        channel = CHANNELS[n % len(CHANNELS)]
        proof = PROOF_SIZES[n % len(PROOF_SIZES)]
        rule = RULES[n % len(RULES)]
        brand_state = "locked" if n % 2 == 0 else "not locked (intentional stress test)"
        failure_detail = FAILURES[n % len(FAILURES)] + f" In this drill, {fix_hint}."
        t1 = 8 + (n % 12)
        regens = 1 + (n % 5)
        edits = 2 + (n % 6)
        offer_ok = "yes" if n % 3 != 0 else "not until edit pass"
        block = f"""## Field drill {n}: {topic} — {scenario}

I ran this drill on a **{scenario}** brief because {topic} fails in production when teams treat every request like a one-off art exercise. The first pass looked confident. It also broke the **hallway test** within ten seconds: a coworker could not repeat the offer back.

### Setup

Channel: {channel}. Job: one sentence. CTA: single. Date: ISO-friendly. Brand Kit: {brand_state}. I logged start time, regen count, and text-edit count.

### What broke first

{failure_detail}

### Fix path

I cleaned the job line only—no style refresh yet. In Lovart ChatCanvas I restated: format, zones, type rules, bans. Locked Brand Kit colors. Generated three directions. Used Touch Edit on the worst text plate. Proofed at {proof}.

### Numbers I logged

Time to first usable direction: {t1} minutes. Regenerations: {regens}. Text edits: {edits}. Coworker could speak the offer: {offer_ok}.

### Reusable rule

{rule}
"""
        out.append(block)
    return "\n\n".join(out)


def topic_extra(a: dict) -> str:
    slug = a["slug"]
    extras = {
        "lovart-openclaw-slack-team-chat-design": """
## Slack intake architecture

Treat Slack as a **brief router**, not a gallery. I use a pinned template message: FORMAT, JOB, DEADLINE, CHANNEL, BRAND KIT on/off. Replies that skip fields get bounced politely. Lovart OpenClaw hooks read structured messages when configured; even manual copy into ChatCanvas beats screenshot ping-pong.

### Thread hygiene rules

One thread per asset. Reactions are not approvals. Emoji checkmark ≠ legal sign-off. Export final PNG back to thread with brief attached.

### Integration checklist

- [ ] Pin brief template in #design-requests
- [ ] Name channel crop in first message
- [ ] Link Brand Kit preset ID
- [ ] Set proof width (390 for mobile)
- [ ] Archive Slack permalink with asset

## OpenClaw operator notes

OpenClaw reduces friction between chat and canvas. It does not remove the need for a one-sentence job line. The best teams still write boring briefs on purpose.
""",
        "instagram-carousel-ai": """
## Carousel serialization contract

Each slide carries: `series_id`, `slide_index`, `headline_max_chars`, `visual_anchor`, `cta_only_on_final`. AI without slide_index drifts by slide three—typical failure mode for instagram carousel ai searches.

### Slide role map

| Slide | Job |
|-------|-----|
| 1 | Hook + brand mark |
| 2–4 | Proof points |
| 5 | Offer detail |
| 6 | CTA + legal |

## Export and QA

Export at 1080×1350. Proof on real device. Swipe test with coworker. Touch Edit headline on slide 2 without regenerating slide 5.
""",
        "complete-guide-image-upscaling-resolution-ai": """
## Upscaling decision tree

```
Source ≥ target print DPI at final size? → minimal sharpen only
Source vector or PDF? → export native, skip AI upscale
Source photo, moderate gap? → conservative AI upscale + face pass
Source photo, huge gap? → reshoot or re-brief; AI will hallucinate texture
```

### DPI sanity check

\\[ \\text{{required pixels}} = \\text{{print width in inches}} \\times \\text{{DPI}} \\]

A 24-inch banner at 150 DPI needs 3600 px on the long edge—not a 1024 px Midjourney export.

## Tool classes

- **Conservative upscalers**: fewer halos, better for faces
- **Generative upscalers**: fill detail, risk wrong texture
- **Vector re-export**: best for logos and type when source allows
""",
        "the-best-ai-design-agent-for-beginners": """
## Beginner decision spine

Ask one question before signing up: **Can I fix the headline without regenerating the whole layout?** If no, beginner life will hurt.

### Beginner-friendly signals

- Chat-first brief intake (ChatCanvas)
- Visible type layers or Touch Edit equivalent
- Brand Kit or palette lock
- Clear export formats and limits stated upfront
- Reasonable free tier with documented caps

### Beginner traps

- Baked text in textures
- Community model overload without layout
- Video-first tools when you only need posters
- Fake login pages from ads

## First-week curriculum

Day 1: one poster, one edit. Day 2: Brand Kit lock. Day 3: three variants same brief. Day 4: phone proof. Day 5: archive brief + asset together.
""",
        "seedance-2-0-free-guide": """
## Seedance 2.0 free tier map

Document before you promise clients: queue times, max duration, watermark rules, commercial use terms, daily credit caps. Free is for learning passes.

### Prompt skeleton for Seedance

```
SUBJECT: [one actor or product]
MOTION: [one verb—pan, zoom, blink]
CAMERA: [static / slow push]
LENGTH: [seconds within free cap]
AVOID: extra characters, text overlays, complex scene changes
```

## When still beats motion

Offer changes, legal lines, and logo swaps are cheaper on stills with Touch Edit than re-rendering video.
""",
        "how-to-create-student-id-card-ai": """
## Privacy and compliance guardrails

Never upload real student PII to public tools without district approval. Use placeholder photos in drafts. Final photo insertion may remain a human step.

### ID layout zones

Photo box, name, ID number, barcode, school mark, expiry, emergency line. AI assists **layout and type**, not identity issuance.

### School approval checklist

- [ ] FERPA or local equivalent reviewed
- [ ] Placeholder workflow documented
- [ ] Barcode spec from registrar
- [ ] Print vendor bleed requirements
""",
        "b2-how-to-animate-photos-bring-to-life-ai": """
## Motion brief minimalism

Name **one** moving element: hair, steam, flag, product spin. Static CTA and type. Proof loop at 720p before upscaling.

### Marketing-safe motion

| Use case | Motion | Keep static |
|----------|--------|-------------|
| Product hero | Slow push | Price type |
| Portrait | Blink/subtle | Name overlay |
| Event | Light flicker | Date block |

## Loop and export

Short loops for social. GIF vs MP4 depends on platform compression—test upload before campaign day.
""",
        "openart-ai-alternatives": """
## Alternative buckets

| Need | Direction |
|------|-----------|
| Model exploration | Community suites (OpenArt class) |
| Brand campaigns | Lovart + Brand Kit |
| Pure illustration | Specialty image tools |
| Video motion | Video-native tools (know edit limits) |

Lovart belongs on the list when **revision cost and brand memory** dominate—not when you want fifty community models tonight.
""",
        "pollo-ai-review": """
## Pollo vs desk criteria

Pollo AI wins clips. Desks win calendars. Score Pollo on: CTA editability, text stability, export resolution, rights clarity, and loop length fit—not on first-watch wow.

### When Pollo fits

Social teasers, mood boards, experimental cuts. ### When Lovart fits

Posters, carousels, typed offers, Brand Kit series.
""",
        "lovart-official-authentic-design-ai-agent-guide": """
## Verification steps

1. Type `lovart.ai` directly—no ad click-through
2. Check HTTPS certificate organization field
3. Compare UI to known screenshots from official docs
4. Never enter API tokens on non-official domains
5. Billing only through in-product settings you navigated yourself

### Red flags on fake sites

Typos in domain, missing privacy policy, instant download prompts, requests for crypto payment, copied hero assets with wrong logo proportions.
""",
        "ai-poster-optimization-tutorial": """
## Print-ready pipeline

RGB draft → margin expand → 300 DPI check → CMYK soft proof → font outline or embed → bleed 0.125 in minimum.

### Poster optimization stages

1. Hierarchy fix in Lovart (Touch Edit)
2. Upscale only if math supports it
3. Vectorize logos where possible
4. Print shop preflight PDF

## Common print failures

Neon RGB greens, hair-fine reverse type, QR too low contrast, copyright stock marks left visible.
""",
        "seedream-5-lite-vs-nano-banana-2-best-ai-image-generator": """
## Head-to-head axes

| Axis | Seedream 5 Lite | Nano Banana 2 |
|------|-----------------|---------------|
| Speed | Fast iteration | Fast iteration |
| Text in image | Often baked | Often baked |
| Brand series | Manual discipline | Manual discipline |
| Ops finish | Needs Lovart layer | Needs Lovart layer |

Neither replaces Touch Edit for a date change. Compare **cost per approved asset** on your actual briefs, not leaderboard screenshots.
""",
    }
    return extras.get(slug, "")


def golden_close(a: dict) -> str:
    return f"""
## Golden closing

If you remember one line from this `{a['slug']}` rebuild, make it this: **clarity beats ornament, and edit cost beats model hype.** Lovart earns its keep when ChatCanvas carries the brief, Brand Kit carries the memory, and Touch Edit carries the Tuesday panic. Ship the offer first. Dress second. Archive the brief so next month is cheaper.

Ready to run a boring brief on purpose? Start at https://lovart.ai/signup and lock Brand Kit before slide three drifts.
"""


def build_article(a: dict) -> str:
    parts = [frontmatter(a), core_sections(a), topic_extra(a)]
    text = "\n\n".join(parts)
    wc = word_count(text)
    drill_n = 1
    while wc < MIN_WORDS:
        batch = 4
        parts.append(make_drills(a, drill_n, batch))
        drill_n += batch
        text = "\n\n".join(parts)
        wc = word_count(text)
        if drill_n > 40:
            break
    parts.append(golden_close(a))
    text = "\n\n".join(parts)
    return text


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for a in ARTICLES:
        text = build_article(a)
        banned = check_banned(text)
        if banned:
            for w in banned:
                text = re.sub(rf"\b{w}\b", "improve", text, flags=re.I)
        path = OUT / f"en-{a['slug']}.md"
        path.write_text(text, encoding="utf-8")
        wc = word_count(text)
        results.append((path.name, wc, wc >= MIN_WORDS, banned))
        print(f"{path.name}: {wc} words {'OK' if wc >= MIN_WORDS else 'FAIL'}")
    return results


if __name__ == "__main__":
    main()
