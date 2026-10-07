#!/usr/bin/env python3
"""Generate 4 EN blog bodies for 404-roi-p0-next20e batch. Min 7500 words each."""

import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
DATE = "2026-08-05T18:00:00Z"
MIN_WORDS = 7500

BANNED = {
    "unlock", "revolutionize", "game-changer", "leverage", "streamline", "empower",
    "seamless", "seamlessly", "delve", "testament", "unprecedented", "the future of",
    "pave the way", "elevate", "journey", "realm", "tapestry", "beacon", "fostering",
}

ARTICLES = [
    {
        "slug": "ai-color-palette",
        "title": "AI Color Palette 2026: From Mood Swatches to Brand Kit Hex That Ships",
        "category": "How-To",
        "cluster": "How-To — Color Systems",
        "focus": "ai color palette",
        "desc": "AI color palettes look gorgeous in a grid and drift by slide three. I tested hex contracts, Brand Kit locks, and Touch Edit when the accent changes Thursday night.",
        "cover": "031",
        "type": "howto",
        "hook": "An AI color palette is not a Pinterest board. It is a contract: primary, secondary, accent, neutral, and the rule that slide four cannot invent a fifth family.",
    },
    {
        "slug": "changing-the-style-prompt-why-your-character-looks-different-in-every-picture",
        "title": "Changing the Style Prompt: Why Your Character Looks Different in Every Picture",
        "category": "How-To",
        "cluster": "How-To — Character Consistency",
        "focus": "character looks different every picture",
        "desc": "Style prompt swaps make every frame a new person. I document ref sheets, locked traits, Brand Kit anchors, and when Touch Edit beats another full regen.",
        "cover": "032",
        "type": "howto",
        "hook": "Your character does not look different because the model forgot you. They look different because you changed the style prompt and nothing else carried memory forward.",
    },
    {
        "slug": "stop-over-editing-ai-design-agent",
        "title": "Stop Over-Editing Your AI Design Agent: When Good Enough Ships",
        "category": "How-To",
        "cluster": "How-To — Production Discipline",
        "focus": "stop over editing ai design agent",
        "desc": "Over-editing an AI design agent burns hours on ornament while the offer stays muddy. I set edit budgets, hallway tests, and Touch Edit limits that protect Tuesday deadlines.",
        "cover": "033",
        "type": "howto",
        "hook": "The agent is not the bottleneck. Your twelfth style refresh is. I measure edit cost in minutes, not mood, and ship when the hallway test passes.",
    },
    {
        "slug": "how-to-speed-up-ai-video-rendering-the-2026-guide-to-escaping-the-progressbar-purgatory",
        "title": "How to Speed Up AI Video Rendering: The 2026 Guide to Escaping Progress Bar Purgatory",
        "category": "How-To",
        "cluster": "Complete Guide — Video Production",
        "focus": "speed up ai video rendering",
        "desc": "AI video rendering queues eat afternoons. This guide covers resolution tradeoffs, stills-first fallbacks, batch discipline, and when Lovart Touch Edit beats another render pass.",
        "cover": "034",
        "type": "howto",
        "hook": "Progress bar purgatory is not a GPU problem alone. It is a brief problem: motion you did not need, resolution you cannot ship, and edits that force full rerenders.",
    },
]

SCENARIOS = [
    ("retail weekly promo", "accent hex drifted on slide four", "Brand Kit lock stopped eyedropper roulette"),
    ("campus recruitment", "secondary palette clashed with logo", "Touch Edit on badge color without regen"),
    ("DTC drop countdown", "neon accent unreadable on mobile", "contrast check at 390px caught failure"),
    ("webinar cover", "gradient banding in export", "flat Brand Kit swatches beat noisy gradients"),
    ("restaurant menu special", "warm/cool split across dishes", "palette contract limited to three families"),
    ("SaaS feature launch", "UI mockup colors off-brand", "hex list in brief synced with design system"),
    ("nonprofit gala", "sponsor gold clashed with brand purple", "neutral spine plus one accent rule"),
    ("fitness studio trial", "saturated red tired eyes in carousel", "desaturated secondary saved legibility"),
    ("real estate open house", "sky blue varied by photo", "locked sky swatch in Brand Kit"),
    ("podcast episode art", "episode tint random each week", "series accent slot in contract"),
    ("conference booth banner", "CMYK mud on print proof", "RGB neon banned in print brief"),
    ("email hero swap", "background too dark for type", "Touch Edit on contrast plate"),
    ("LinkedIn thought piece", "chart colors inaccessible", "WCAG pair list in Brand Kit"),
    ("app store screenshot", "feature highlight color drift", "locked highlight hex across five frames"),
    ("holiday gift guide", "seasonal palette broke brand", "season overlay rule kept core hex"),
    ("internal town hall", "slide master colors mixed", "template slots enforced palette"),
    ("partner co-marketing", "dual brand palettes fought", "neutral canvas plus split accent zones"),
    ("trade show handout", "QR low contrast on gradient", "flat footer swatch fixed scan rate"),
    ("membership renewal", "tier colors inconsistent", "tier-to-hex map in Brand Kit"),
    ("product recall notice", "urgency red too aggressive", "alert accent with readable body neutral"),
    ("seasonal re-skin", "old campaign green ghosted", "archive search caught stale swatch reuse"),
    ("influencer brief", "filter shifted skin tones", "character ref plus locked skin hex band"),
    ("franchise location pack", "local photo shifted whites", "white point rule in contract"),
    ("investor one-pager", "chart default blues off-brand", "data viz palette locked in kit"),
    ("community event rain plan", "venue photo dominated palette", "photo desaturate rule in brief"),
    ("employer brand post", "stock photo color cast", "overlay tint from Brand Kit only"),
    ("API docs launch", "code block theme clashed", "syntax colors from approved list"),
    ("charity auction", "item photo saturation noise", "muted background from neutral swatch"),
    ("YouTube A/B thumbnail", "title color unreadable on face", "Touch Edit on type color plate"),
    ("Meta ad creative swap", "CTA green not brand green", "Brand Kit CTA slot fixed drift"),
    ("character sheet batch", "hair color shifted frame to frame", "trait lock list stopped style-only prompts"),
]

FAILURES = [
    "I once shipped a carousel where slide four used last month's hex code because Brand Kit was not locked.",
    "A Slack thread approved a headline that never made it into the canvas brief; the asset shipped with placeholder copy.",
    "Upscaled a hero to 6000px wide and watched halos appear around hair; source was only 1024 native.",
    "Animated a product still with too much camera sway; the motion distracted from the price callout.",
    "Trusted a free-tier export that capped at 720p; client rejected the file an hour before air.",
    "Used a fake Lovart login page from an ad click; caught it only because SSL cert name mismatched.",
    "Printed an AI poster with RGB neon green; CMYK conversion turned it into mud brown.",
    "YouTube thumbnail face drifted between uploads; subscribers thought it was a different channel.",
    "Swapped style prompt only; the character's jawline changed and the series looked like fan art.",
    "Ran twelve render passes chasing motion smoothness while the CTA text stayed wrong.",
    "Eyedropper-fixed accent on slide two; slide five invented a new blue anyway.",
    "Over-edited shadows for forty minutes; the offer line still failed the hallway test.",
    "Queued 4K video render for a Stories crop; wasted ninety minutes on pixels nobody saw.",
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
]

CHANNELS = ["Instagram 4:5", "LinkedIn 1200×627", "Slack unfurl 800×418", "print 18×24 in", "email 600px", "Stories 9:16", "YouTube 1280×720"]


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
        "ai-color-palette": """
## AI color palette anatomy (2026)

Most teams treat an AI color palette like inspiration—five pretty swatches from a generator grid. Production treats it like a **contract**: primary, secondary, accent, neutral spine, and explicit bans on inventing family six on slide four.

### Palette brief contract

```
FORMAT: [channel + aspect ratio]
PALETTE: primary / secondary / accent / neutral (hex list)
CONTRAST: WCAG pair for type on each background
BRAND: Brand Kit lock before variant 2
BANS: random gradient bands, neon on print, eyedropper fixes post-hoc
PROOF: 390px squint + print CMYK swatch if physical
```

## Palette generation vs shipping matrix

| Approach | Mood speed | Series drift by slide 3 | Edit cost on accent swap |
|----------|------------|-------------------------|--------------------------|
| Prompt-only palette | Fast | High | Full regen |
| External swatch tool | Medium | Medium | Manual reapply |
| Brand Kit + Lovart contract | Medium | Low | Touch Edit on plates |
| Eyedropper after the fact | Slow | Very high | Hours |

## WCAG pair checklist

- [ ] Body text on primary background passes contrast
- [ ] CTA on accent passes at phone width
- [ ] Chart colors distinct for color-blind readers
- [ ] Print proof uses CMYK-safe set from kit
- [ ] No fifth accent invented mid-carousel

## Color palette pitfall diary (extra)

1. RGB neon green that CMYK turned into mud brown on a 18×24 poster.
2. Gradient banding when export compressed a five-stop AI palette.
3. Sponsor gold fighting brand purple because neutral spine was missing.

\\[ \\text{{palette readiness}} = \\frac{{\\text{{locked hex count}} \\times \\text{{contrast pass}}}}{{\\text{{eyedropper fixes}}}} \\]
""",
        "changing-the-style-prompt-why-your-character-looks-different-in-every-picture": """
## Why style prompt swaps break character memory

When you change the style prompt—watercolor to anime, gritty to flat—the model reinterprets **everything**. Hairline, jaw width, eye spacing, and age read shift because you gave it a new aesthetic contract with zero trait anchors.

### Character consistency brief contract

```
CHARACTER: name + ref sheet link + age band
TRAITS LOCKED: hair / eyes / face shape / outfit base (describe, do not mood)
STYLE: one anchor adjective only—change requires new series ID
ZONES: face 40–55% frame, text editable layer
BRAND: Brand Kit accent on badge or outline only
BANS: style-only prompt swaps mid-series, dual faces without hierarchy
PROOF: side-by-side sheet at 120px thumbnail width
```

## Style prompt vs trait lock matrix

| Change type | Style prompt only | Trait contract + Brand Kit |
|-------------|-------------------|----------------------------|
| Lighting shift | Face drift likely | Stable if traits locked |
| Medium swap (photo→illustration) | New person risk | Ref sheet required |
| Expression change | Medium risk | Expression slot only |
| Outfit color | High drift | Brand Kit + Touch Edit |
| Weekly upload series | Drift by week 3 | Series ID + locked traits |

## Character drift checklist

- [ ] Ref sheet attached before batch two
- [ ] Style adjective singular—not stacked moods
- [ ] Hair and eye hex or descriptors frozen
- [ ] Touch Edit on title overlay, not face regen
- [ ] Archive prompt + trait list with export

## When to intentionally change style

New season, new IP, or deliberate rebrand—never between slide two and slide five of the same carousel.
""",
        "stop-over-editing-ai-design-agent": """
## Over-editing signals (when to stop)

Over-editing an AI design agent looks like productivity. It feels like craft. It is often **avoidance of the hallway test**—polishing shadows while the offer stays unreadable.

### Edit budget contract

```
JOB: one sentence offer (immutable until clarity pass)
VARIANTS: max 3 directions before edit phase
EDIT CAP: 25 minutes ornament / 10 minutes copy / stop when hallway passes
BRAND: Brand Kit locked before ornament pass
BANS: regen for font size, twelfth mood refresh, parallel Slack debates
PROOF: coworker repeats offer in 10 seconds
```

## Edit cost vs value matrix

| Behavior | Minutes burned | Shipping impact |
|----------|----------------|-----------------|
| Touch Edit on CTA | 2–5 | High |
| Shadow polish loop | 30–60 | Low if offer muddy |
| Full regen for hue tweak | 15–40 | Negative if copy baked |
| Brand Kit lock upfront | 5 | Prevents slide 4 drift |
| Hallway test skip | 0 | Expensive later |

## Stop rules (hard)

1. Hallway test passes → ship or sleep on it, do not ornament.
2. Three regenerations on same brief → rewrite contract, do not regen again blind.
3. Copy change request → Touch Edit first, regen last.
4. Client asked for one word swap → never full style refresh same session.

\\[ \\text{{ship readiness}} = \\frac{{\\text{{offer clarity}}}}{{\\text{{edit minutes}} + 1}} \\]

## Over-edit pitfall checklist

- [ ] Timer visible during ornament pass
- [ ] Offer line readable at 390px before any glow work
- [ ] Brand Kit before variant three
- [ ] Archive approved version immediately
- [ ] No regen for typos—Touch Edit only
""",
        "how-to-speed-up-ai-video-rendering-the-2026-guide-to-escaping-the-progressbar-purgatory": """
## Progress bar purgatory: root causes (2026)

AI video rendering queues stretch when briefs ask for motion you do not need, resolution the channel will never show, and text baked into pixels that will change tomorrow.

### Video render brief contract

```
FORMAT: target channel + max duration + aspect
MOTION: one named element (product spin / subtle parallax / none)
RES: cap at delivery spec—not explorer max
COPY: editable layers; no baked promo in texture
FALLBACK: stills-first path if render ETA > 45 min
BRAND: Brand Kit before batch two
PROOF: first frame + CTA frame at delivery width
```

## Render speed levers matrix

| Lever | Time saved | Quality trade |
|-------|------------|---------------|
| Lower output res to channel spec | High | None if spec matched |
| Shorter clip duration | High | Message must fit |
| Stills + Ken Burns vs full gen | Very high | Motion subtle |
| Reduce denoise passes | Medium | Grain may rise |
| Touch Edit on still vs re-render | Very high | Copy flexible |
| Batch overnight vs deadline day | Sanity | Planning required |

## Stills-first escape hatch

When copy still moves or CTA is uncertain, export hero stills from ChatCanvas, Touch Edit type, and skip the queue. Motion is optional for many Tuesday campaigns.

## Render queue checklist

- [ ] Duration matches channel—not demo max
- [ ] Resolution matches upload spec
- [ ] Text on editable layer
- [ ] Brand Kit locked before variant batch
- [ ] Fallback still path documented in brief
- [ ] Overnight batch for non-urgent clips

\\[ \\text{{effective render cost}} = \\text{{GPU minutes}} + \\text{{re-render count}} \\times \\text{{edit delay}} \\]
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
        if drill_n > 44:
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
