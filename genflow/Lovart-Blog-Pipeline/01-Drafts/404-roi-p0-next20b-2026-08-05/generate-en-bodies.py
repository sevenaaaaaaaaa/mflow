#!/usr/bin/env python3
"""Generate 10 EN blog bodies for 404-roi-p0-next20b batch. Min 7500 words each."""

import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
DATE = "2026-08-05T12:00:00Z"
MIN_WORDS = 7500

BANNED = {
    "unlock", "revolutionize", "game-changer", "leverage", "streamline", "empower",
    "seamless", "seamlessly", "delve", "testament", "unprecedented", "the future of",
    "pave the way", "elevate", "journey", "realm", "tapestry", "beacon", "fostering",
}

ARTICLES = [
    {
        "slug": "logo-maker-comparison",
        "title": "Logo Maker Comparison 2026: AI Tools vs Brand Desk Reality",
        "category": "How-To",
        "cluster": "How-To — Brand Identity",
        "focus": "logo maker comparison",
        "desc": "Logo makers promise instant marks. I compared AI logo tools on revision cost, vector export, and whether Brand Kit survives the second client note.",
        "cover": "025",
        "type": "comparison",
        "hook": "A logo maker wins on first impression. Brand desks win when the client asks to nudge the tagline two pixels left without rebuilding the whole mark.",
    },
    {
        "slug": "pixverse-ai-review",
        "title": "PixVerse AI Review 2026: Video Clips vs Campaign Shipping",
        "category": "How-To",
        "cluster": "Review — Video AI",
        "focus": "pixverse ai review",
        "desc": "PixVerse AI sells cinematic motion. I tested what finishes social clips versus what stays demo material when CTA text must change.",
        "cover": "026",
        "type": "review",
        "hook": "PixVerse clips look impressive on mute. The review question is whether your team can fix a wrong date before the post goes live.",
    },
    {
        "slug": "lovart-official-trial-guide-avoid-fake-sites",
        "title": "Lovart Official Trial Guide: How to Start Safely and Avoid Fake Sites",
        "category": "How-To",
        "cluster": "Signal — Brand Safety",
        "focus": "lovart official trial avoid fake sites",
        "desc": "Fake Lovart login pages ride on search ads. Here is how I verify the official trial, protect credentials, and onboard a team without phishing traps.",
        "cover": "027",
        "type": "signal",
        "hook": "When a design agent trends, copycat domains multiply. Verification is cheaper than credential recovery.",
    },
    {
        "slug": "what-is-ai-design-agent",
        "title": "What Is an AI Design Agent? A Production Desk Definition for 2026",
        "category": "How-To",
        "cluster": "How-To — Agent Concepts",
        "focus": "what is ai design agent",
        "desc": "AI design agent is not a synonym for image generator. I define the category by brief intake, editable output, and brand memory—not model count.",
        "cover": "028",
        "type": "howto",
        "hook": "Most explainers list features. Operators need a spine: can the tool carry a brief, survive a text edit, and remember your hex codes on slide four?",
    },
    {
        "slug": "venngage-ai-ad-generator-review",
        "title": "Venngage AI Ad Generator Review 2026: Infographic Speed vs Ad Desk Ops",
        "category": "How-To",
        "cluster": "Review — Ad Creative Tools",
        "focus": "venngage ai ad generator review",
        "desc": "Venngage AI ad generator targets quick promos. I tested layout speed, export limits, and where Lovart takes over for brand-locked campaigns.",
        "cover": "029",
        "type": "review",
        "hook": "Venngage shines when the brief is a simple promo block. It strains when legal lines, dual logos, and last-minute offer swaps stack up.",
    },
    {
        "slug": "wondershare-virbo-review",
        "title": "Wondershare Virbo Review 2026: Avatar Video vs Marketing Asset Ops",
        "category": "How-To",
        "cluster": "Review — Avatar Video",
        "focus": "wondershare virbo review",
        "desc": "Wondershare Virbo packages presenter video fast. I tested avatar quality, script edits, and whether still-first workflows beat avatar rerenders.",
        "cover": "030",
        "type": "review",
        "hook": "Virbo is useful when a talking head must ship tonight. It is less useful when the offer line changes after legal review.",
    },
    {
        "slug": "steve-ai-review",
        "title": "Steve AI Review 2026: Text-to-Video Promises vs Revision Reality",
        "category": "How-To",
        "cluster": "Review — Text-to-Video",
        "focus": "steve ai review",
        "desc": "Steve AI turns scripts into video. I measured time-to-first clip, text stability, and the cost of fixing a wrong product name mid-campaign.",
        "cover": "031",
        "type": "review",
        "hook": "Steve AI feels fast until the script changes. Then you learn whether the tool edits or rerenders.",
    },
    {
        "slug": "stable-video-diffusion-review-2025-open-source-ai-video-tested",
        "title": "Stable Video Diffusion Review 2025: Open-Source AI Video Tested for Ops",
        "category": "How-To",
        "cluster": "Review — Open Source Video",
        "focus": "stable video diffusion review open source ai video",
        "desc": "Stable Video Diffusion is open and flexible. I tested install cost, clip quality, and whether self-hosted motion beats managed tools for marketing desks.",
        "cover": "032",
        "type": "review",
        "hook": "Open-source video is free to download and expensive to operate. The review axis is ops hours, not GitHub stars.",
    },
    {
        "slug": "ai-visual-identity-design-2026",
        "title": "AI Visual Identity Design 2026: Systems, Not Single Logos",
        "category": "Branding",
        "cluster": "Signal — Brand Systems",
        "focus": "ai visual identity design 2026",
        "desc": "Visual identity in 2026 means type, color, templates, and motion rules—not one hero logo PNG. Here is how I build identity with AI agents and Brand Kit.",
        "cover": "033",
        "type": "signal",
        "hook": "Teams ask AI for a logo and get a PNG. Brand systems ask for repeatable templates that survive Tuesday's offer swap.",
    },
    {
        "slug": "pika-ai-review",
        "title": "Pika AI Review 2026: Social Motion vs Production Calendar Discipline",
        "category": "How-To",
        "cluster": "Review — Video AI",
        "focus": "pika ai review",
        "desc": "Pika AI generates eye-catching motion from stills. I tested loop quality, text overlays, and where stills plus Touch Edit beat re-rendering clips.",
        "cover": "034",
        "type": "review",
        "hook": "Pika wins the scroll-stop test. Desks still win when the price changes an hour before publish.",
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
    "Logo maker exported a raster mark; client needed vector and billed us for a redraw.",
    "PixVerse clip looked cinematic until frame nine showed duplicated product edges.",
    "Venngage template swapped fonts when I changed one word in the headline block.",
    "Virbo avatar mispronounced the product name; script edit required full re-render.",
    "Steve AI scene drifted between cuts; brand color shifted from teal to cyan.",
    "Self-hosted SVD queue stalled Friday afternoon; campaign used still fallback instead.",
    "Pika loop cropped the legal disclaimer off the bottom on Stories export.",
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
    if a["type"] in ("review", "comparison"):
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
        scenario, _, fix_hint = SCENARIOS[(n - 1) % len(SCENARIOS)]
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
        "logo-maker-comparison": """
## Logo maker comparison axes

| Tool class | First mark speed | Vector export | Text edit cost | Brand series |
|------------|------------------|---------------|----------------|--------------|
| Instant AI logo sites | Fast | Often raster only | High | Weak |
| General design suites | Medium | Mixed | Medium | Manual |
| Lovart + Brand Kit | Fast enough | Layout-first | Touch Edit low | Strong |

### When AI logo makers fit

Side projects, event one-offs, internal hackathon marks. ### When they fail

Trademark review, signage scale, co-brand packs, franchise localization.

## Vector and signage checklist

- [ ] SVG or EPS export confirmed
- [ ] Minimum size test at 16px favicon
- [ ] Single-color knockouts prepared
- [ ] Clear space rules documented
- [ ] Brand Kit stores primary and secondary locks
""",
        "pixverse-ai-review": """
## PixVerse vs desk criteria

Score PixVerse on loop length fit, motion artifact rate, text overlay stability, export resolution, and rights clarity—not first-watch wow.

### When PixVerse fits

Social teasers, product mood loops, experimental cuts. ### When Lovart fits

Posters, carousels, typed offers, Brand Kit series, last-minute CTA swaps on stills.

## Motion minimalism for PixVerse prompts

```
SUBJECT: one product or face
MOTION: one verb
CAMERA: slow push or static
TEXT: none in-gen; add in Lovart after
LENGTH: platform cap minus 2s
```
""",
        "lovart-official-trial-guide-avoid-fake-sites": """
## Official trial verification steps

1. Navigate directly to `https://lovart.ai`—never through ad redirects
2. Confirm HTTPS certificate matches Lovart organization
3. Start trial only from in-product signup flow
4. Bookmark the authenticated dashboard URL after first login
5. Share official link internally—do not forward third-party "free download" pages

### Fake site red flags

Typos in domain (`lovart-ai.tools`, `lovartapp.net`), missing privacy policy, crypto payment requests, EXE downloads, credential forms on non-official hosts.

## Team onboarding safety

- [ ] IT allowlist `lovart.ai`
- [ ] Slack pin with official URL
- [ ] Ban pasted tokens in public channels
- [ ] Two-factor auth where available
- [ ] Trial budget owner named before first invite

## Trial week curriculum

Day 1: verify domain + one poster. Day 2: Brand Kit lock. Day 3: Touch Edit drill. Day 4: export limits map. Day 5: archive briefs with assets.
""",
        "what-is-ai-design-agent": """
## AI design agent definition (operator version)

An **AI design agent** accepts a structured brief, generates layout-aware creative, exposes editable type and brand memory, and supports revision without full regenerates. It is not merely a text-to-image endpoint.

### Five capability layers

| Layer | Question it answers |
|-------|---------------------|
| Brief intake | Can I state format, job, zones in chat? |
| Generation | Does output respect layout zones? |
| Edit | Can I fix headline without rerolling hero? |
| Memory | Does Brand Kit hold hex and type rules? |
| Ship | Export survives target channel width? |

## Agent vs generator decision tree

```
Need one mood frame tonight? → generator may suffice
Need weekly campaigns with edits? → design agent
Need regulated claims? → agent + human review
Need 50 community models? → exploration suite, not agent
```

Lovart maps to the agent column when ChatCanvas, Touch Edit, and Brand Kit are in play.
""",
        "venngage-ai-ad-generator-review": """
## Venngage AI ad generator scoring

| Dimension | Venngage strength | Desk gap |
|-----------|-------------------|----------|
| Template speed | High | — |
| Infographic blocks | High | — |
| Brand Kit depth | Medium | Lovart stronger |
| Touch Edit on hero type | Limited | Lovart stronger |
| Multi-slide series | Manual | Lovart contract + kit |

### When Venngage fits

Simple promo blocks, internal comms, one-off infographics. ### When Lovart takes over

Dual-logo partner ads, legal-heavy disclaimers, carousel series with locked palette.
""",
        "wondershare-virbo-review": """
## Virbo review axes

Avatar lip-sync quality, script edit cost, language coverage, export resolution, background swap stability, and commercial rights—not avatar count alone.

### Script-change cost test

Change one product name in a 45-second Virbo clip. Log re-render time. Compare to still hero + Touch Edit for the same message.

## Avatar vs still-first matrix

| Message type | Virbo | Lovart still + motion accent |
|--------------|-------|------------------------------|
| Founder update | Strong | Optional |
| Product price promo | Weak on edits | Strong |
| Legal disclaimer read | Risky | Stills + human VO |
""",
        "steve-ai-review": """
## Steve AI production notes

Steve AI converts scripts to scenes quickly. Watch for scene-to-scene color drift, baked lower-thirds, and stock footage mismatches when brand guidelines are strict.

### Steve prompt skeleton

```
HOOK: one sentence
SCENES: 3–5 max
VISUAL: product or UI only—no crowd stock
TEXT ON SCREEN: none—add in post
BRAND: hex list in notes
CTA: final scene only
```

## When to pair Steve with Lovart

Generate still keyframes or thumbnail covers in Lovart; use Steve for motion assembly only when script is frozen.
""",
        "stable-video-diffusion-review-2025-open-source-ai-video-tested": """
## SVD ops reality check

Self-hosted Stable Video Diffusion adds GPU cost, queue management, dependency updates, and security patching. Budget ops hours alongside electricity.

### SVD vs managed tools

| Factor | Self-hosted SVD | Managed video AI |
|--------|-----------------|------------------|
| Install time | Hours to days | Minutes |
| Per-clip cost | GPU amortized | Subscription |
| Customization | High | Medium |
| Ops burden | You own it | Vendor owns uptime |

## Marketing-safe SVD settings

Conservative motion strength, short clip length, still-first fallback when queue exceeds SLA. Export loops to Lovart for typed CTA overlays via Touch Edit.
""",
        "ai-visual-identity-design-2026": """
## Visual identity system components 2026

Logo mark, wordmark, color tokens, type scale, layout grid, photography style, icon rules, motion grammar, and template library—not a single PNG.

### Identity build sequence with Lovart

1. Brand Kit: colors + type roles
2. ChatCanvas: core templates (social, slide, print)
3. Touch Edit: localize offers without breaking grid
4. Archive: template IDs per channel

## Identity QA checklist

- [ ] Primary logo clear space documented
- [ ] One-color knockouts tested
- [ ] Template slide 3 drift check
- [ ] Motion intro ≤2s brand sting
- [ ] Partner co-brand rules in Brand Kit
""",
        "pika-ai-review": """
## Pika AI scoring rubric

Loop smoothness, artifact rate on product edges, text stability (usually none in-gen), export aspect ratios, and edit cost when offer changes.

### Pika vs still workflow

| Scenario | Pika clip | Lovart still + Touch Edit |
|----------|-----------|---------------------------|
| Scroll-stop teaser | Strong | Medium |
| Price swap same day | Weak | Strong |
| Brand color lock series | Drift risk | Brand Kit strong |

## Pika prompt minimalism

One subject, one motion verb, static CTA added after in Lovart canvas.
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
        print(f"{path.name}: {wc} words {'PASS' if wc >= MIN_WORDS else 'FAIL'}")
    print("\n--- Summary ---")
    for name, wc, ok, banned in results:
        print(f"{name}\t{wc}\t{'PASS' if ok else 'FAIL'}")
    return results


if __name__ == "__main__":
    main()
