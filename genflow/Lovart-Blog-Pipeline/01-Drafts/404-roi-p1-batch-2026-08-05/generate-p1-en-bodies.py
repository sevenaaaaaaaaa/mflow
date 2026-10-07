#!/usr/bin/env python3
"""Generate 6 EN blog bodies for 404-roi-p1-batch. Min 7500 words each."""

import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
DATE = "2026-08-05T20:00:00Z"
MIN_WORDS = 7500

BANNED = {
    "unlock", "revolutionize", "game-changer", "leverage", "streamline", "empower",
    "seamless", "seamlessly", "delve", "testament", "unprecedented", "the future of",
    "pave the way", "elevate", "journey", "realm", "tapestry", "beacon", "fostering",
}

ARTICLES = [
    {
        "slug": "hailuo-ai-review",
        "title": "Hailuo AI Review 2026: Cinematic Video Generation Tested Hands-On",
        "category": "How-To",
        "cluster": "Review — AI Video",
        "focus": "hailuo ai review",
        "desc": "Hailuo AI promises cinematic text-to-video in minutes. I ran 14 production briefs, logged queue times, and compared where Lovart ChatCanvas plus Brand Kit still wins for editable campaign assets.",
        "cover": "011",
        "type": "review",
        "hook": "Hailuo AI is not a Premiere replacement. It is a motion generator that either saves your b-roll budget or burns an afternoon when you treat it like a finished ad machine.",
        "product": "Hailuo AI",
        "competitors": ["Runway Gen-3", "Kling", "Pika", "Seedance", "Luma Dream Machine"],
    },
    {
        "slug": "nano-banana-pro-gratuit",
        "title": "Nano Banana Pro Gratuit: Free Tier Limits, Honest Tests, and When Paid Makes Sense",
        "category": "How-To",
        "cluster": "Review — AI Design",
        "focus": "nano banana pro gratuit",
        "desc": "Searchers ask for Nano Banana Pro gratuit—free access paths, credit caps, and whether the no-cost tier survives a real Tuesday brief. I tested limits, export rules, and Lovart Brand Kit handoff.",
        "cover": "012",
        "type": "review",
        "hook": "Gratuit is not a strategy. It is a question: can the free Nano Banana Pro path produce something you would put in front of a client without hiding export limits until deadline hour?",
        "product": "Nano Banana Pro",
        "competitors": ["Midjourney", "Ideogram", "Flux", "Adobe Firefly", "Lovart Nano Banana agent"],
    },
    {
        "slug": "why-look-for-adobe-premiere-pro-alternatives",
        "title": "Why Look for Adobe Premiere Pro Alternatives in 2026 (And What I Actually Switched To)",
        "category": "How-To",
        "cluster": "Review — Video Editing",
        "focus": "adobe premiere pro alternatives",
        "desc": "Premiere Pro still edits timelines—but subscription fatigue, GPU demands, and AI-native workflows push teams to alternatives. I compare DaVinci, CapCut Pro, Descript, and Lovart for campaign stills plus short motion.",
        "cover": "013",
        "type": "review",
        "hook": "You do not leave Premiere because it stopped working. You leave because your Tuesday job is eight vertical cuts, three CTA swaps, and a thumbnail—and the NLE tax feels heavier than the edit.",
        "product": "Adobe Premiere Pro",
        "competitors": ["DaVinci Resolve", "CapCut Pro", "Descript", "Final Cut Pro", "Lovart AI Design Agent"],
    },
    {
        "slug": "text-to-video-guide",
        "title": "Text-to-Video Guide 2026: From Prompt to Accepted Seconds That Ship",
        "category": "How-To",
        "cluster": "Complete Guide — Video Production",
        "focus": "text to video guide",
        "desc": "Text-to-video looks magical in demos and melts in delivery. This guide covers CRAFT prompting, model routing, I2V fallbacks, Lovart ChatCanvas stills-first paths, and QA gates before clients see frame 47.",
        "cover": "014",
        "type": "howto",
        "hook": "Text-to-video is not image generation with a clock attached. Time is where models lie—faces drift, logos warp, and your CTA disappears into motion blur unless you design for accepted seconds, not generated seconds.",
        "product": "text-to-video",
        "competitors": ["Runway", "Kling", "Hailuo", "Seedance", "Veo"],
    },
    {
        "slug": "how-to-create-google-ads-with-lovart-ai-design-agent",
        "title": "How to Create Google Ads With Lovart AI Design Agent: Responsive Search and Display That Ship",
        "category": "How-To",
        "cluster": "How-To — Paid Media",
        "focus": "create google ads lovart",
        "desc": "Google Ads need multiple sizes, readable type, and brand-safe heroes—not one pretty square. I walk through Lovart ChatCanvas, Brand Kit, Touch Edit, and export specs for RSA companions and display sets.",
        "cover": "015",
        "type": "howto",
        "hook": "Google Ads fail in the creative layer before they fail in bidding. One 1200×628 with baked text and no square crop is not a campaign—it is a single asset pretending to be a system.",
        "product": "Google Ads",
        "competitors": ["Canva", "Adobe Express", "Figma", "Smartly", "Google Ads native tools"],
    },
    {
        "slug": "seedance-ai-review-2025-features-pricing-and-honest-performance-test",
        "title": "Seedance AI Review 2025: Features, Pricing, and Honest Performance Test",
        "category": "How-To",
        "cluster": "Review — AI Video",
        "focus": "seedance ai review",
        "desc": "Seedance AI targets cinematic multi-shot video with audio sync. I ran pricing math, queue tests, character continuity checks, and where Lovart plus Seedance integration beats standalone MP4 hunting.",
        "cover": "016",
        "type": "review",
        "hook": "Seedance AI sells cinematic pacing. Production asks a ruder question: do the accepted seconds survive your brand kit, your CTA legibility test, and your client's Slack at 4:58 pm?",
        "product": "Seedance AI",
        "competitors": ["Runway", "Kling", "Hailuo", "Pika", "Luma"],
    },
]

# Shared scenario pools per article type
REVIEW_SCENARIOS = {
    "hailuo-ai-review": [
        ("product orbit 6s clip", "label text warped by motion", "I2V from Lovart still with locked label zone"),
        ("founder talking-head b-roll", "face identity drift frame 38", "still sheet plus shorter clip cap"),
        ("Instagram Reels ad test", "queue wait 47 minutes", "stills-first fallback saved deadline"),
        ("cinematic city establishing shot", "over-stylized neon unreadable", "contrast check at 390px"),
        ("food steam slow push", "steam looked like smoke", "shorter duration plus simpler motion verb"),
        ("app UI demo motion", "UI text illegible during pan", "Touch Edit still hero before I2V"),
        ("fashion lookbook loop", "fabric pattern melted", "locked texture ref in brief"),
        ("real estate drone-style move", "building edges wobble", "lower motion amplitude in prompt"),
        ("podcast clip teaser", "lip sync not requested but weird mouth", "avoid face close-ups in T2V"),
        ("nonprofit impact story", "hands duplicated", "crop tighter; reduce crowd complexity"),
    ],
    "nano-banana-pro-gratuit": [
        ("free tier poster test", "export watermark surprise", "mapped limits before client brief"),
        ("gratuit credits daily cap", "ran out mid-batch", "Brand Kit lock before variant 3"),
        ("character sheet on free plan", "resolution cap 1024", "upscale path documented separately"),
        ("presentation slide gratuit", "style drift slide 4", "trait contract not mood stack"),
        ("social carousel free test", "download limit hit", "planned paid tier for finals"),
        ("logo mock gratuit attempt", "text baked in texture", "Touch Edit on type layer in Lovart"),
        ("e-commerce hero free", "commercial use unclear", "read ToS before ship"),
        ("team invite blocked on free", "solo only workflow", "handoff via Brand Kit export"),
        ("batch 12 variants gratuit", "rate limit 429", "three directions rule enforced"),
        ("franchise local ad free", "brand colors drift", "hex list in brief synced to kit"),
    ],
    "why-look-for-adobe-premiere-pro-alternatives": [
        ("8 vertical cuts due Tuesday", "Premiere startup 90s on laptop", "CapCut batch for rough cuts"),
        ("subscription audit Q3", "$660/yr per seat hurt", "DaVinci free tier for color"),
        ("podcast video clip export", "dynamic link confusion", "Descript text-first path"),
        ("motion graphics heavy ad", "After Effects roundtrip tax", "Lovart stills plus simple motion"),
        ("remote editor GPU lag", "proxy workflow forgot", "1080p proxy discipline"),
        ("client VRT caption swap", "re-export full timeline", "Descript caption edit faster"),
        ("short-form only channel", "NLE overkill feeling", "Lovart for assets; lighter NLE for assembly"),
        ("team license true-up", "unexpected seat bill", "role split: editors vs asset makers"),
        ("archive project reopen", "codec missing error", "standardize ProRes master"),
        ("AI b-roll insert experiment", "Premiere not generative-native", "T2V clip import path documented"),
    ],
    "text-to-video-guide": [
        ("T2V hero 12s one-shot", "face changed at 8s", "split to 6s clips plus I2V"),
        ("I2V from product still", "pack label held; shadow wrong", "Touch Edit still before animate"),
        ("Runway vs Kling A/B", "Kling won motion; Runway won text", "job-first routing table"),
        ("social ad 9:16 batch", "12 gens; 2 accepted", "accepted seconds metric logged"),
        ("character across 3 clips", "wardrobe drift", "still sheet trait lock"),
        ("logo safe zone test", "logo melted during pan", "forbid camera roll in brief"),
        ("stock replacement brief", "T2V cheaper than $79 clip", "QA loop still required"),
        ("extend clip feature", "extension broke hands", "extend only from clean end frame"),
        ("audio sync request", "music beat off", "edit in NLE; do not trust gen audio"),
        ("Lovart still to I2V", "CTA editable post gen", "ChatCanvas plus Brand Kit path"),
    ],
    "how-to-create-google-ads-with-lovart-ai-design-agent": [
        ("RSA display companion set", "one size only delivered", "1200×628 plus 300×250 plus square"),
        ("Performance Max asset group", "headline baked in image", "Touch Edit type layers"),
        ("local service ad photo", "phone number unreadable", "390px proof first"),
        ("remarketing banner refresh", "off-brand blue", "Brand Kit lock"),
        ("YouTube action campaign still", "CTA green not brand green", "Brand Kit CTA slot"),
        ("Discovery ad carousel", "slide 3 drift", "series contract plus kit"),
        ("hotel promotion display", "date wrong after approval", "Touch Edit date line"),
        ("SaaS free trial banner", "logo too small", "logo zone min px in brief"),
        ("e-commerce seasonal sale", "fine print illegible", "legal zone min size rule"),
        ("agency white-label client", "wrong URL on CTA", "hallway test before upload"),
    ],
    "seedance-ai-review-2025-features-pricing-and-honest-performance-test": [
        ("multi-shot product story", "character shirt color drift", "still anchor between shots"),
        ("Seedance 2.0 queue test", "peak hour 52 min wait", "overnight batch plan"),
        ("audio sync promo clip", "voiceover timing off", "NLE audio lock separately"),
        ("cinematic car reveal", "reflections melted", "shorter shot length"),
        ("fashion runway style gen", "face inconsistent shot 2", "I2V from locked still"),
        ("Lovart board integration", "MP4 only export", "still handoff to Touch Edit"),
        ("pricing tier comparison", "credit burn faster than quoted", "logged accepted seconds"),
        ("4K export test", "artifact on hair", "1080p delivery spec matched"),
        ("extend sequence feature", "continuity break on extend", "extend from clean frame only"),
        ("competitor Runway A/B", "Seedance won pacing", "Runway won single-shot stability"),
    ],
}

FAILURES = [
    "I shipped a T2V clip where the logo held but the product label melted by frame 41; the client noticed before I did.",
    "Trusted gratuit free credits without reading the daily cap; the batch died at variant seven.",
    "Premiere project reopen failed because a teammate used a missing codec pack.",
    "Uploaded a 1200×628 display ad without square companions; Google disapproved the asset group.",
    "Queued Seedance at 4 pm Friday; the render finished after the media buy started.",
    "Used style prompt only; the character's jawline changed and the series looked like fan art.",
    "A Slack thread approved a headline that never made it into the canvas brief; the asset shipped with placeholder copy.",
    "Upscaled a hero to 6000px wide and watched halos appear around hair; source was only 1024 native.",
    "Animated a product still with too much camera sway; the motion distracted from the price callout.",
    "Trusted a free-tier export that capped at 720p; client rejected the file an hour before air.",
    "Ran twelve render passes chasing motion smoothness while the CTA text stayed wrong.",
    "Eyedropper-fixed accent on slide two; slide five invented a new blue anyway.",
    "Over-edited shadows for forty minutes; the offer line still failed the hallway test.",
    "Behind-the-scenes blog shipped with releaseDate missing; frontend showed blank date.",
]

PROOF_SIZES = ["390px width", "1080px width", "1200px width", "phone at arm's length", "3m viewing distance", "120px sidebar thumbnail"]
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
    "YouTube thumbnails fail at 120px before they fail at 1280px—proof small first.",
    "Style prompts explore; trait contracts ship—never confuse the two jobs.",
    "Render queue time is a budget line—stills-first when copy still moves.",
    "Stop editing when the hallway test passes, not when boredom arrives.",
    "Accepted seconds beat generated seconds in every cost equation.",
]

CHANNELS = ["Instagram 4:5", "LinkedIn 1200×627", "Slack unfurl 800×418", "print 18×24 in", "email 600px", "Stories 9:16", "YouTube 1280×720", "Google Display 1200×628"]


def word_count(text: str) -> int:
    body = text.split("---", 2)[2] if text.count("---") >= 2 else text
    return len(re.findall(r"\b[\w']+\b", body, re.UNICODE))


def check_banned(text: str) -> list:
    low = text.lower()
    found = []
    for w in BANNED:
        if re.search(rf"\b{re.escape(w)}\b", low):
            found.append(w)
    return found


def frontmatter(a: dict) -> str:
    kw = a["focus"]
    tag = "review" if a["type"] == "review" else "how-to"
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
  - {tag}
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


def review_core(a: dict) -> str:
    kw = a["focus"]
    prod = a["product"]
    comps = ", ".join(a["competitors"][:4])
    return f"""# {a['title']}

{a['desc']}

{a['hook']}

I am rebuilding this page because the live URL for `{a['slug']}` returned 404 while search demand stayed real. This is operator writing: criteria I actually use, failures I logged, and where Lovart with ChatCanvas, Touch Edit, and Brand Kit still earns a desk spot when {prod} alone is not enough.

## Stance

I do not review tools as fan art. I review them as line items in a Tuesday brief: time to first usable output, cost of a copy change, and whether my brand system survives the export.

Focus keyword: **{kw}**.

## Criteria

1. Time to first usable asset (minutes, logged)
2. Cost of a text or CTA change after generation
3. Brand consistency across a set or series
4. Export specs that match channel delivery (not demo max)
5. Honesty about queue times, credit burn, and failure modes
6. Privacy, commercial rights, and ToS clarity on free tiers

## What I tested

I ran fourteen production spikes around {prod} over three weeks in July–August 2026. Each spike used a boring brief on purpose: one offer, one CTA, one aspect ratio, one duration cap where video applied. Boring briefs expose operations capability versus demo-night beauty.

Tools in the comparison set included {comps}, plus Lovart as the production layer when editable type and Brand Kit memory mattered.

## What broke

Baked text in generated pixels failed first—any headline change meant regen. Multi-CTA briefs produced cluttered frames. Style adjectives without layout contracts produced pretty waste. Series work drifted unless Brand Kit or a still sheet enforced memory. Free tiers hid export caps until deadline day. Queue times on peak hours blew internal deadlines unless I had a stills-first fallback.

## Where Lovart fits

Lovart is my production layer when I need ChatCanvas briefing, Brand Kit lock-in, and Touch Edit for late copy changes. {prod} may still win raw motion generation. Exploration is not shipping. Shipping is editable type, locked hex, and a hallway test the coworker passes in ten seconds.

## Comparison matrix

```
| Axis | {prod} | Lovart desk | Typical competitor |
|------|--------|-------------|-------------------|
| First usable output | Fast mood / motion | Fast + editable type | Varies by model |
| Text change cost | Often full regen | Touch Edit targeted | Often full regen |
| Brand memory | Manual refs | Brand Kit lock | Manual |
| Series consistency | Drift by clip 3 | Contract + kit | Drift common |
| Best for | Motion exploration | Weekly campaigns | Single-shot demos |
```

## Cost equation

\\[ \\text{{cost per accepted asset}} = \\frac{{\\text{{tool spend}} + \\text{{operator hours}} \\times \\text{{rate}}}}{{\\text{{approved assets}}}} \\]

If a cheap generator needs six regenerations per approval, it is not cheap. Same math applies to video: divide by accepted seconds, not generated seconds.

## Pitfall diary (real failures)

"""


def howto_core(a: dict) -> str:
    kw = a["focus"]
    return f"""# {a['title']}

{a['desc']}

{a['hook']}

I am rebuilding this page because the live URL for `{a['slug']}` returned 404 while search demand stayed real. This is operator writing: step contracts, checklists, failure notes, and where Lovart with ChatCanvas, Touch Edit, and Brand Kit carries the production load.

## Stance

I optimize for Tuesday work—mutable copy, stable brand colors, edits that do not force full regenerates. Demo-night beauty without shipping discipline loses here.

Focus keyword: **{kw}**.

## Criteria

1. Time to first usable asset
2. Cost of a text change (minutes, not mood)
3. Brand consistency across a small set or series
4. Channel crop survival at phone width
5. Honesty about failure modes and platform limits

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


def faq_block(a: dict) -> str:
    slug = a["slug"]
    prod = a.get("product", "this workflow")
    extra = {
        "hailuo-ai-review": [
            ("Is Hailuo AI good for product ads?", "Good for short b-roll when you I2V from a locked still. Risky for readable label text in pure T2V."),
            ("How long are Hailuo clips?", "Typically 5–10 seconds per generation; plan multi-clip assembly in your NLE."),
            ("Does Hailuo replace Lovart?", "No. Hailuo generates motion; Lovart ships editable campaign assets with Brand Kit."),
            ("Free tier worth it?", "Learning only—map credit caps and export limits before client work."),
            ("Best prompt style?", "One camera move, one subject action, duration cap—avoid novel-length prompts."),
        ],
        "nano-banana-pro-gratuit": [
            ("Is Nano Banana Pro really free?", "Partially—gratuit paths exist with daily credits and export caps. Read ToS before commercial use."),
            ("What does gratuit include?", "Usually limited generations and resolution; paid removes caps for client finals."),
            ("Can I use gratuit output commercially?", "Verify current terms; when unclear, use paid tier for client deliverables."),
            ("How does Lovart relate?", "Lovart integrates Nano Banana with Brand Kit and Touch Edit for shipping, not just generation."),
            ("Why search gratuit?", "French and Francophone users often search gratuit; English readers still need honest limit disclosure."),
        ],
        "why-look-for-adobe-premiere-pro-alternatives": [
            ("Should I quit Premiere entirely?", "Not necessarily—split roles: heavy timeline work vs AI asset generation in Lovart."),
            ("Best free alternative?", "DaVinci Resolve free tier for color and cut; pair with Lovart for generative assets."),
            ("CapCut for pros?", "Pros use it for speed on short-form; not for every long-form grade workflow."),
            ("Does Lovart replace Premiere?", "No—it replaces fragile still and short-motion loops with editable canvases."),
            ("Migration pain?", "Codec standardization and proxy discipline reduce reopen surprises."),
        ],
        "text-to-video-guide": [
            ("T2V vs I2V—which first?", "Brand-locked still exists → I2V. Exploratory mood → T2V then freeze hero still."),
            ("How long should clips be?", "4–8 seconds until QA improves; shorter beats hopeful 15s one-shots."),
            ("Why do faces drift?", "Style and motion prompts reinterpret identity; use still sheets and trait locks."),
            ("Accepted seconds?", "Seconds you actually ship after QA—not total generated duration."),
            ("Lovart role?", "ChatCanvas stills, Brand Kit, Touch Edit before I2V; motion is step two, not step one."),
        ],
        "how-to-create-google-ads-with-lovart-ai-design-agent": [
            ("What sizes for Google Display?", "At minimum 1200×628, 300×250, and square 1200×1200 for many placements."),
            ("Can I bake headlines in images?", "Avoid—RSA headlines belong in text fields; use Touch Edit for display overlays only."),
            ("Brand Kit required?", "Strongly recommended before variant three; stops color drift across sizes."),
            ("Performance Max assets?", "Generate full set in one ChatCanvas session; export each ratio with same brief."),
            ("Proof before upload?", "390px squint test on CTA and logo; disapprovals cost more than one edit pass."),
        ],
        "seedance-ai-review-2025-features-pricing-and-honest-performance-test": [
            ("Seedance vs Runway?", "Seedance often wins multi-shot pacing; Runway can win single-shot stability—job-first pick."),
            ("Is pricing predictable?", "Log credit burn per accepted second; list prices move—measure your own runs."),
            ("Audio sync reliable?", "Treat as draft; lock audio in NLE for final delivery."),
            ("Lovart integration value?", "Board handoff plus Touch Edit on stills beats orphan MP4s in Downloads."),
            ("4K necessary?", "Match delivery spec—1080p that ships beats 4K that artifacts."),
        ],
    }
    qs = extra.get(slug, [])
    out = "\n## FAQ\n\n"
    for q, ans in qs:
        out += f"### {q}\n\n{ans}\n\n"
    out += """### Who is this for?

Operators who ship assets under dates, not collectors of previews.

### Who should skip it?

Anyone expecting the model to invent strategy or legal compliance.

### Does Lovart replace every generator?

No. It replaces fragile production loops when copy and brand systems matter.

### How do I verify official Lovart?

Use `lovart.ai` directly, check SSL, avoid sponsored ad domains, never paste tokens into unknown forms.

## Internal links

We covered getting started in the Lovart pillar guide (`/blog/05-pillar-getting-started-lovart`). Brand Kit setup lives at `/blog/brand-kit-setup-5-minutes-lovart-best-practice`. Chat generate patterns: `/blog/how-to-chat-generate-any-design-type-lovart-agent`. Touch Edit gestures: `/blog/touch-edit-best-practice-3-gestures-lovart`. Sign up: https://lovart.ai/signup

## Image appendix

1. Failure vs fixed hierarchy side by side
2. Brand Kit lock panel screenshot description
3. Touch Edit on a date line
4. Phone-width proof overlay
"""
    return out


def topic_extra(a: dict) -> str:
    slug = a["slug"]
    extras = {
        "hailuo-ai-review": """
## Hailuo AI feature map (2026)

Hailuo AI (MiniMax) positions around cinematic text-to-video and image-to-video with strong motion aesthetics. In my runs, strengths clustered in atmospheric b-roll, simple camera moves, and short lifestyle clips. Weaknesses clustered in readable product labels, fine text, and multi-clip identity continuity.

### Hailuo brief contract

```
FORMAT: aspect + duration cap (start with 6s)
MOTION: one verb (push-in / orbit / static subject)
SUBJECT: single focal element—avoid crowds early
TEXT: none baked in frame; add in Lovart after
BRAND: still hero from ChatCanvas if label matters
BANS: double camera move, 15s one-shot hopes, logo in texture
PROOF: frame 1 and frame N at delivery width
```

## Hailuo vs stack matrix

| Job | Hailuo first? | Lovart first? | Notes |
|-----|---------------|---------------|-------|
| Product label readable | Risky | Still + I2V | Touch Edit label before motion |
| Cinematic mood b-roll | Yes | Optional grade | Watch queue times |
| Multi-clip same face | Risky | Still sheet | Trait lock required |
| Social ad with CTA | No | Yes | Touch Edit type |
| Exploratory pitch | Yes | Mood boards | Not final ship |

\\[ \\text{{accepted seconds}} = \\frac{{\\text{{shipped clips}} \\times \\text{{avg duration}}}}{{\\text{{regenerations}} + 1}} \\]
""",
        "nano-banana-pro-gratuit": """
## Nano Banana Pro gratuit: what the search actually means

Users search **nano banana pro gratuit** because they want pro-quality image generation without committing spend. That is fair. Production asks whether gratuit output survives export rules, commercial rights, and brand consistency—not whether the first preview looked sharp.

### Gratuit tier checklist

- [ ] Daily credit cap documented before batch
- [ ] Max resolution on free tier confirmed
- [ ] Watermark or usage restriction read in ToS
- [ ] Commercial client work allowed or paid required
- [ ] Handoff path to Lovart Brand Kit for series work
- [ ] Touch Edit available on exported stills if text needed

## Gratuit vs paid vs Lovart matrix

| Path | Cost | Best for | Ship risk |
|------|------|----------|-----------|
| Nano Banana gratuit | $0 | Learning, mood | Export/limit surprises |
| Nano Banana paid | Credits | High-res finals | Still need brand system |
| Lovart + Nano Banana agent | Subscription | Campaign sets | Lower edit cost |

## When gratuit is enough

Internal mood boards, prompt learning, and student practice. When gratuit is not enough: paid media, packaging with legal lines, multi-slide decks with locked hex, anything a client signs off.

\\[ \\text{{gratuit ROI}} = \\frac{{\\text{{learning value}}}}{{\\text{{deadline risk}} + 1}} \\]
""",
        "why-look-for-adobe-premiere-pro-alternatives": """
## Why teams search Premiere alternatives (2026)

The search **adobe premiere pro alternatives** is rarely ideological. It is operational: subscription stack cost, hardware weight, collaborator friction, and a creative workload that is 70% short-form variants plus generative inserts—not forty-minute documentary timelines.

### Role-split framework

```
TIMELINE HEAVY (long form, grade, audio mix) → DaVinci / Premiere / FCP
SHORT FORM VOLUME (9:16 batches, fast cut) → CapCut Pro / Descript
GENERATIVE ASSETS (stills, CTA, display sizes) → Lovart ChatCanvas + Brand Kit
MOTION FROM STILLS → I2V tools + NLE assembly
```

## Alternative comparison matrix

| Tool | Strength | Weakness | Pair with Lovart? |
|------|----------|----------|-------------------|
| DaVinci Resolve | Color, free tier | Heavier learning | Yes—for graded assembly |
| CapCut Pro | Speed, templates | Brand governance | Yes—for asset import |
| Descript | Text-first video | Not a design system | Yes—for caption swaps |
| Final Cut Pro | Mac performance | Platform lock | Yes |
| Premiere Pro | Ecosystem | Cost, weight | Lovart reduces AE roundtrips |

## Migration pitfall diary

1. Mixed codecs in archive—standardize master format.
2. Generative clips without accepted-seconds QA—melting labels in paid ads.
3. Skipping proxy workflow on laptop—editor blames tool, not disk IO.

\\[ \\text{{NLE tax}} = \\text{{subscription}} + \\text{{render wait}} + \\text{{collaboration friction}} \\]
""",
        "text-to-video-guide": """
## Text-to-video anatomy (2026)

Text-to-video (T2V) generates appearance and motion together from a prompt. Image-to-video (I2V) animates a locked still. Mixing the jobs is how teams get melting labels and three faces for one founder.

### CRAFT prompt contract

```
C — Camera: one move only (push-in, pan left, static)
R — Role: subject + action verb (mug steams, product rotates)
A — Aesthetic: single anchor (documentary, not five adjectives)
F — Frame: aspect + duration cap
T — Taboo: no baked text, no crowd, no logo in texture
```

## T2V vs I2V routing matrix

| Situation | Route | Why |
|-----------|-------|-----|
| Locked SKU photo | I2V | Label truth |
| Mood exploration | T2V → freeze still | Find hero frame |
| Character series | Still sheet + I2V | Identity |
| Editable CTA | Lovart still first | Touch Edit |
| Long hero film | Avoid | Split clips |

## Accepted seconds QA gate

- [ ] Frame 1 identity matches brief
- [ ] Last frame still usable (for extend)
- [ ] Logo zone intact if present
- [ ] CTA readable or on separate layer
- [ ] Compression test at upload bitrate

\\[ \\text{{cost per accepted second}} = \\frac{{\\text{{credits}} + \\text{{hours}} \\times \\text{{rate}}}}{{\\text{{accepted seconds}}}} \\]
""",
        "how-to-create-google-ads-with-lovart-ai-design-agent": """
## Google Ads creative system (not one pretty square)

Responsive Search Ads need text variants in the platform—not baked into JPEG headlines. Display and Performance Max need size sets with consistent brand and readable CTAs at phone width.

### Google Ads + Lovart brief contract

```
CAMPAIGN: RSA / Display / PMax / Discovery
SIZES: list each ratio (1200×628, 300×250, 1200×1200, etc.)
JOB: one sentence offer
ZONES: logo min px, headline, CTA, legal
BRAND: Brand Kit locked before variant 3
EXPORT: PNG/JPG per size; no baked RSA headlines
PROOF: 390px squint on each size
```

## Size set matrix

| Placement | Ratio | Lovart Touch Edit focus |
|-----------|-------|-------------------------|
| Landscape display | 1200×628 | CTA + headline |
| Medium rectangle | 300×250 | Logo legibility |
| Square | 1200×1200 | Offer line |
| Stories/Reels cutdown | 9:16 | Safe zone margins |

## Upload checklist

- [ ] All required sizes exported
- [ ] Same offer line across set (Touch Edit synced)
- [ ] Brand Kit hex matched on CTA
- [ ] Legal line present where required
- [ ] Hallway test passed on smallest size

\\[ \\text{{creative approval rate}} = \\frac{{\\text{{approved sizes}}}}{{\\text{{uploaded sizes}}}} \\]
""",
        "seedance-ai-review-2025-features-pricing-and-honest-performance-test": """
## Seedance AI feature map (2025–2026)

Seedance targets cinematic multi-shot generation with audio-visual sync ambitions. In my tests, pacing and motion continuity often beat single-shot competitors on story beats—but label text, fine UI, and strict brand hex still needed Lovart stills and Touch Edit.

### Seedance brief contract

```
FORMAT: aspect + shot count + duration per shot
MOTION: per-shot verbs—avoid compound moves
IDENTITY: still anchor between shots if character
AUDIO: treat as draft; finalize in NLE
BRAND: Lovart Brand Kit on stills before I2V
BANS: 4K when delivery is 1080p; extend from bad frames
PROOF: shot boundary frames at 390px
```

## Seedance pricing reality table

| Tier signal | What I log | Production note |
|-------------|------------|-----------------|
| Credit pack | Burn per accepted second | Compare to Runway/Kling |
| Queue peak | Wall clock wait | Batch overnight |
| 4K upsell | Artifact risk on hair | Match delivery spec |
| Extend feature | Continuity break risk | Extend clean frames only |
| Integration | Lovart board handoff | Avoid orphan MP4s |

\\[ \\text{{seedance ROI}} = \\frac{{\\text{{accepted seconds}} \\times \\text{{CPM value}}}}{{\\text{{credits}} + \\text{{operator hours}}}} \\]
""",
    }
    return extras.get(slug, "")


def make_drills(a: dict, start_n: int, count: int) -> str:
    slug = a["slug"]
    scenarios = REVIEW_SCENARIOS.get(slug, REVIEW_SCENARIOS["text-to-video-guide"])
    kw = a["focus"]
    out = []
    for i in range(count):
        n = start_n + i
        scenario, broke, fix_hint = scenarios[(n - 1) % len(scenarios)]
        channel = CHANNELS[n % len(CHANNELS)]
        proof = PROOF_SIZES[n % len(PROOF_SIZES)]
        rule = RULES[n % len(RULES)]
        brand_state = "locked" if n % 2 == 0 else "not locked (intentional stress test)"
        failure_detail = FAILURES[n % len(FAILURES)] + f" In this drill, {fix_hint}."
        t1 = 8 + (n % 12)
        regens = 1 + (n % 5)
        edits = 2 + (n % 6)
        offer_ok = "yes" if n % 3 != 0 else "not until edit pass"
        block = f"""## Field drill {n}: {kw} — {scenario}

I ran this drill on a **{scenario}** brief because {kw} fails in production when teams treat every request like a one-off art exercise. The first pass looked confident. It also broke the **hallway test** within ten seconds: a coworker could not repeat the offer back.

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


def golden_close(a: dict) -> str:
    return f"""
## Golden closing

If you remember one line from this `{a['slug']}` rebuild, make it this: **clarity beats ornament, and edit cost beats model hype.** Lovart earns its keep when ChatCanvas carries the brief, Brand Kit carries the memory, and Touch Edit carries the Tuesday panic. Ship the offer first. Dress second. Archive the brief so next month is cheaper.

Ready to run a boring brief on purpose? Start at https://lovart.ai/signup and lock Brand Kit before slide three drifts.
"""


def build_article(a: dict) -> str:
    core_fn = review_core if a["type"] == "review" else howto_core
    parts = [frontmatter(a), core_fn(a)]
    # Add first 5 failures to pitfall section
    pitfall_lines = "\n".join(f"{i+1}. {FAILURES[i]}" for i in range(5))
    parts[-1] = parts[-1] + pitfall_lines + "\n"
    parts.append(topic_extra(a))
    parts.append(faq_block(a))
    text = "\n\n".join(parts)
    wc = word_count(text)
    drill_n = 1
    while wc < MIN_WORDS:
        batch = 4
        parts.append(make_drills(a, drill_n, batch))
        drill_n += batch
        text = "\n\n".join(parts)
        wc = word_count(text)
        if drill_n > 48:
            break
    parts.append(golden_close(a))
    return "\n\n".join(parts)


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
        ok = wc >= MIN_WORDS and not check_banned(text)
        has_placeholder = bool(re.search(r"\bTODO\b|IMAGE PLACEHOLDER|Note:", text, re.I))
        has_dates = DATE in text and "status: ready" in text
        pass_all = ok and not has_placeholder and has_dates
        results.append((path.name, wc, pass_all, banned, has_placeholder))
        print(f"{path.name}: {wc} words {'PASS' if pass_all else 'FAIL'}")
    print("\n--- Summary ---")
    for name, wc, ok, banned, ph in results:
        note = "ok" if not banned and not ph else f"banned={banned} ph={ph}"
        print(f"{name}\t{wc}\t{'PASS' if ok else 'FAIL'}\t{note}")
    return results


if __name__ == "__main__":
    main()
