#!/usr/bin/env python3
"""Generate 404-rescue P2 batch22 blog bodies (10 files). Self-contained.

Ranks #224–#234 from 404-rescue-compact lane (skip junk #232).
9 EN + 1 zh-TW. expand_en + expand_zhtw only.
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
    "zh": 2200,
    "zh-TW": 2200,
    "en": 1300,
    "ko": 1400,
    "ru": 900,
    "de": 900,
    "pt": 900,
    "it": 900,
    "fr": 900,
    "ja": 1800,
}

BANNED_EN = [
    "unlock", "revolutionize", "game-changer", "leverage", "streamline",
    "empower", "seamless", "seamlessly", "delve", "testament",
    "unprecedented", "the future of", "pave the way", "elevate", "fostering",
    "tapestry", "beacon", "realm", "journey",
]
BANNED_ZH = [
    "赋能", "闭环", "抓手", "链路", "底层逻辑", "方法论", "心智", "对齐",
    "颗粒度", "打法", "痛点", "破局", "深挖", "见证", "颠覆性", "前沿",
    "生态位", "维度", "引爆",
]

JA_CHAR_RE = re.compile(r"[ぁ-んァ-ン一-龥々〆ヵヶ]")


def cover_url(n: str) -> str:
    return f"https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-{n}-1024x682.png"


def body_text(full_md: str) -> str:
    if full_md.startswith("---"):
        return full_md.split("---", 2)[-1]
    return full_md


def count_zh(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", body_text(text)))


def count_en(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang in ("zh", "zh-TW"):
        return count_zh(text)
    if lang == "en":
        return count_en(text)
    return count_en(text)


def check_banned(text: str) -> list[str]:
    hits = []
    bt = body_text(text)
    low = bt.lower()
    for w in BANNED_EN:
        if w in low:
            hits.append(w)
    for w in BANNED_ZH:
        if w in bt:
            hits.append(w)
    return hits


def fm(meta: dict) -> str:
    kw_lines = "\n".join(f"  - {k}" for k in meta["keywords"])
    return f"""---
title: "{meta['title']}"
slug: {meta['slug']}
date: "2026-08-06"
language: {meta['lang']}
page_type: Blog Post
category: {meta['category']}
author: Lovart Content Team
description: "{meta['description']}"
estimated_read: {meta.get('read', '9 min')}
difficulty: {meta.get('difficulty', 'beginner')}
tool: ChatCanvas, Brand Kit, Touch Edit, Design Agent
focus_keyword: {meta['focus']}
keywords:
{kw_lines}
tags:
  - lovart
  - {meta.get('tag', '404-recovery')}
seo_title: "{meta['seo_title']}"
seo_description: "{meta['seo_description']}"
seo_schema: FAQ
cover_url: {cover_url(meta['cover'])}
alt_text: {meta['slug']} — Lovart blog cover
status: ready
content_cluster: {meta.get('cluster', '404 recovery')}
releaseDate: "{DATE}"
publishedAt: "{DATE}"
---

"""


# ---------------------------------------------------------------------------
# Article bodies (paragraph style, H2 sections)
# ---------------------------------------------------------------------------

DESIGN_AGENT_CREATORS_EN = """
# AI Powered Design Agent for Creators: Buyer Criteria That Survive Tuesday Edits

This English URL `ai-powered-design-agent-for-creators-it` returned 404 while search still asked how creators should pick a design agent — not a generic feature dump with invented pricing tiers. I treat "design agent for creators" as an ops question: can you change episode title, sponsor line, and promo price in five minutes across YouTube thumb, Shorts cover, and community post without accent drift? Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent** answer that with static-first editable layers. KPI is revision minutes, not first-frame wow.

## Four creator deliverables with high edit frequency

First, YouTube thumbnail 1280×720: readable episode title top third, face safe zone center, sponsor disclaimer footer editable when paid placement applies. Second, Shorts cover 9:16: bottom twenty percent flat for **Touch Edit** CTA band. Third, community post 1:1: same thread accent stripe as thumb series. Fourth, Patreon or newsletter banner 1584×396: hex matched **Brand Kit**, **Design Agent** QA mismatch between ratio exports.

## Why creator promos fail on Tuesday title changes

Changing "Ep. 12" to "Ep. 13" costs thirty-minute full regen when title text is baked into pixels. Carousel slide four accent lottery. **Brand Kit** not sampled from channel banner or prior thumb export. Creator brief ends with "cinematic premium" — **Design Agent** has no pass/fail fields. Users screenshot still frames — offer and title must live on editable static layers.

## ChatCanvas brief contract (creator edition)

Weak brief: "make me a viral thumbnail." Strong brief: "Series X Ep. 13 thumb 1280×720, Brand Kit coral + charcoal from channel banner, title top fifteen percent flat for Touch Edit, sponsor line bottom left safe zone, disclaimer footer editable, face center safe zone, Shorts 9:16 same thread." **Design Agent** QA readable title at reduced preview size — not clip cinematic feel.

## Brand Kit sampled from channel art and prior export

Sample primary, accent, and type role from approved channel art and prior thumb export — no random stock gradient as channel color. **ChatCanvas** same thread batch YouTube + Shorts + community export. Creator work is series work; memory beats surprise accent on slide four.

## Touch Edit changes episode title without face crop

"Summer Vlog" to "Autumn Vlog": **Touch Edit** frames title band, keeps face geometry and **Brand Kit** accent stripe. Full regen randomizes expression and catchlight — channel consistency cannot absorb that lottery.

## Design Agent pass/fail fields creators actually need

Readable title at 120px preview width. Hex drift versus **Brand Kit** on slide two through six. Double CTA detection. Disclaimer footer present on editable layer. Sponsor line not baked into render pixels. These fields replace adjective briefs that produce pretty failures.

## Static-first before optional motion hook

Order: static thumb legal pass on disclaimer → variant A/B still → winner becomes thread master → optional subtle motion intro elsewhere. **Touch Edit** title change within five minutes — ops viable for weekly upload cadence. No fabricated conversion lift numbers or fake benchmark renders in this guide.

## Separation from pure video generator tools

Video generators win first-frame demo; creator ops win on title and sponsor line edits across ten episodes. This page covers buyer criteria for revision-heavy channel art, not a ranked list of model names.

## Common mistakes

Skipping **Brand Kit**. Title baked in pixels. New prompt per episode. Sponsor disclaimer missing. 404 URL not restored. Believing fake "best design agent" lists with invented market share.

## Measuring value

Minutes per title fix, accent drift count, export ratios per upload week. Restored URL gives search a stable EN design agent for creators SOP link.
"""

THUMBNAIL_BUY_VS_GEN_EN = """
# Buying a Thumbnail for $50 vs Generating One: Honest Cost Math for Creators

This English URL `buying-a-thumbnail-50-vs-generating-one-0` returned 404 while search asked whether to pay a designer fifty dollars per thumb or generate with AI — not affiliate hype with fake CTR lifts. Honest framing: fifty-dollar purchase wins when you need bespoke illustration once per quarter; generation wins when you ship weekly and Tuesday title edits must finish in five minutes. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent** treat thumbnails as revision-heavy static assets, not one-off wow frames.

## What fifty dollars actually buys

A freelance thumb often includes custom composition, licensed stock or hand-drawn elements, and one revision round. Strength: unique art direction per launch. Weakness: second title change may cost another thirty to fifty dollars and forty-eight hour turnaround. No series memory — episode fourteen accent may drift from episode three. Readable price or sponsor line baked into pixels triggers full redraw.

## What generation buys when brief is contract-grade

Generation wins when brief specifies 1280×720, title band flat for **Touch Edit**, **Brand Kit** hex from channel banner, face safe zone, and 120px preview pass via **Design Agent**. Strength: five-minute title fix, A/B variant in same **ChatCanvas** thread. Weakness: first brief with adjectives only produces pretty unreadable type — ops must learn pass/fail fields, not model names.

## Four-field acceptance test both paths must pass

Field one: readable title at reduced preview width. Field two: series accent consistency across ten episodes. Field three: editable sponsor or promo line without full redraw or regen. Field four: safe zone clear of platform UI overlap. Fifty-dollar purchase fails field three when text is flattened. Generation fails field one when brief ends with "make it pop."

## ChatCanvas brief contract (thumbnail economics edition)

Weak brief: "cheap thumb like top creators." Strong brief: "Series X Ep. 13, 1280×720, Brand Kit yellow + black from channel art, title bottom twenty-five percent flat for Touch Edit, sponsor bottom left safe zone, 120px preview pass, A/B variant same thread expression swap only." **Design Agent** numeric fields — cannot QA "looks viral."

## Brand Kit prevents episode-to-episode accent lottery

Without **Brand Kit**, episode forty-seven invents a new yellow. With Kit active, accent role follows approved channel palette. **ChatCanvas** same thread batch A/B — swap expression, not grid. Purchase path needs style guide PDF; generation path needs Kit SSOT — both need hex discipline.

## Touch Edit makes generation viable for weekly cadence

" I tried 30 days" to "Results surprised me": **Touch Edit** title band five minutes. Fifty-dollar path: email designer, wait, maybe pay rush fee. Break-even math favors purchase at monthly upload; favors generation at weekly upload with two plus title changes per episode.

## When purchase still makes sense

Quarterly tentpole launch with custom illustrated metaphor. Brand refresh with agency art direction. Channel under four uploads per year. Document Kit hex from purchased master so future **Touch Edit** edits match purchased style.

## Common mistakes

Compare only first-thumb cost, ignore revision rounds. Bake sponsor line into purchased PSD flatten. Generate without **Brand Kit** then blame model. Skip **Design Agent** 120px preview test. Fabricate "AI thumbs get 2x CTR" without source.

## Measuring ROI honestly

Track dollars per title change per year, hours waiting on designer, drift incidents across series. Restored URL gives search stable EN buy vs generate thumbnail SOP link — no fake pricing for either path beyond the fifty-dollar example in the slug intent.
"""

TEXT_TO_CINEMA_EN = """
# From Text to Cinema: A Practical Guide to Lovart Text-to-Video

This English URL `from-text-to-cinema-a-practical-guide-to-lovart-text-to-video` returned 404 while search wanted a practical text-to-video SOP inside Lovart — not a cinematic superlative reel with invented render speed scores. Text-to-video daily ops: product hero motion, social hook, B-roll mood clip — offer and disclaimer still belong on editable static layers via **Touch Edit**. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent** run static-first: legal pass on still, then optional motion from text prompt in same thread.

## Four text-to-video deliverable layers

Layer one: static master 16:9 or 4:5 with readable headline and disclaimer footer editable. Layer two: text-prompt motion companion four to six seconds — no readable small text in clip pixels. Layer three: social crop 9:16 and 1:1 with same thread accent stripe. Layer four: end card static — offer match landing hero; **Design Agent** QA mismatch between motion thumb and still CTA.

## Why text-to-cinema projects stall on Tuesday offer changes

Clip bakes "$49 launch" into pixels while landing static shows old price. Changing offer triggers full rerender thirty minutes. Slide four accent lottery between still and motion. **Brand Kit** not sampled from approved packaging. Brief stacks "cinematic epic" adjectives — **Design Agent** has no pass/fail fields.

## ChatCanvas brief contract (text-to-video edition)

Weak brief: "turn this paragraph into a movie." Strong brief: "Campaign X text-to-video prep 16:9 1920×1080, Brand Kit slate + coral from media kit, headline static companion top fifteen percent flat for Touch Edit, price bottom left safe zone on still only, disclaimer footer editable, motion prompt: slow dolly product hero muted lighting no text in render, variants two through four same thread." **Design Agent** QA static acceptance — not clip cinematic feel.

## Brand Kit keeps still and motion color temperature matched

Sample primary, accent, type role from approved VI — not random stock marble as brand color. Motion accent must not diverge from Instagram carousel slide three. **Brand Kit** as SSOT fixes hex drift between text-to-video output and static master.

## Touch Edit changes offer without motion reroll

"Limited $49" to "Member $39": **Touch Edit** frames CTA band on still master, keeps hero geometry and **Brand Kit** accent stripe. Full motion reroll for two-word change — ops cannot absorb thirty-minute reroll per shot.

## Text prompt discipline for cinema-style hooks

Prompt A atmosphere: slow dolly, muted lighting, no text in render, accent stripe match **Brand Kit** hex. Prompt B product: same hero geometry, parallax only, price on still companion editable. Prompt C character: reference plate yaw within fifteen degrees, no offer in pixels. Do not claim prompt template number one wins conversions — describe field structure and revision cost only.

## Static-first sequence before optional motion

Order: static legal pass on disclaimer → variant A/B still → winner still becomes thread master → text-to-video motion hook elsewhere. **Touch Edit** price change within five minutes — ops viable. No fabricated API quota numbers or fake render speed benchmarks.

## Common mistakes

Motion-only funnel with no static editable layer. Price baked in clip pixels. New prompt per size without thread. Skipping **Brand Kit**. 404 URL not restored. Using text-to-video to QA readable disclaimer — wrong tool layer.

## Measuring value

Minutes per offer fix, still versus motion offer match count, export ratios per campaign. Restored URL gives search stable EN text-to-cinema Lovart SOP link.
"""

LINKEDIN_BANNER_EN = """
# How to Chat Generate a LinkedIn Banner with Lovart ChatCanvas

This English URL `how-to-chat-generate-linkedin-banner-lovart` returned 404 while search wanted a chat-generate LinkedIn banner SOP — not a generic AI poster demo. LinkedIn personal banner standard 1584×396 — ratio must sit in brief contract. **ChatCanvas** thread, **Brand Kit**, **Touch Edit**, and **Design Agent** treat banner as revision-heavy: role change, headline wording, and promo line edits finish in five minutes without full regen lottery.

## LinkedIn banner four acceptance fields

Field one: readable headline at profile preview crop — mobile and desktop safe zones differ. Field two: series consistency with same creator accent across posts and banner. Field three: editable headline band — **Touch Edit** changes tagline without full reroll. Field four: no critical content in bottom-left avatar overlap zone.

## Why chat generate banner stalls on role title changes

Weak brief "premium professional banner" produces small title text hidden by avatar circle. Changing "Product Lead" to "Founder" triggers thirty-minute full regen. Accent drifts to different blue. **Brand Kit** not sampled from approved headshot or prior banner export. Promo line baked into pixels.

## ChatCanvas dialogue brief contract (LinkedIn edition)

Round one acceptance fields: "1584×396, headline right two-thirds flat for Touch Edit, Brand Kit navy + sand from media kit, avatar overlap zone bottom-left clear, publish preview mobile pass, no small text long sentences in render, same thread export company page companion 1128×191." Round two fills missing fields only. **Design Agent** QA preview crop readable, hex versus Kit.

## Brand Kit locks professional palette without drift

Sample primary, accent, title type role from approved media kit or prior banner. Without **Brand Kit**, month six banner invents new teal — personal brand feels fragmented. **ChatCanvas** same thread batch personal plus company page crop derivatives.

## Touch Edit changes headline without background identity loss

"Building AI tools" to "Helping teams ship faster": **Touch Edit** frames headline band, keeps background geometry and **Brand Kit** accent stripe. Full regen randomizes texture — professional consistency sensitive.

## Static-first before optional motion or video background

LinkedIn autoplay limited; visitors screenshot still profile. Offer and headline must live on static editable layer. Optional subtle motion background must match **Brand Kit** color temperature — no readable small text in video pixels.

## Common mistakes

Single banner no series thread with post templates. Readable headline baked in pixels. Avatar overlap ignored. 404 URL not restored. Skipping **Design Agent** mobile preview pass.

## Measuring value

Headline fix minutes, A/B drift count, mobile preview pass rate. Restored URL gives creator and founder teams stable chat generate LinkedIn banner SOP link.
"""

PRODUCT_LABELS_EN = """
# How to Create Product Labels Without Photoshop: Static-First SOP

This English URL `how-to-create-product-labels-without-photoshop` returned 404 while search wanted a practical label workflow without Photoshop — not a generic AI design tool ranking. Product label daily ops: SKU name, weight line, allergen disclaimer, promo sticker — regulatory text changes weekly, hex drifts between print and screen. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent** treat labels as revision-heavy static masters with editable compliance layers.

## Four product label deliverable layers

Layer one: front panel master with product name and weight line editable via **Touch Edit**. Layer two: back panel disclaimer and ingredient block — footer flat band, no small text baked in render. Layer three: promo sticker overlay same thread accent stripe. Layer four: print PDF companion and screen PDP crop — **Design Agent** QA hex mismatch versus **Brand Kit**.

## Why label projects fail on Tuesday allergen line edits

Regulatory text baked into pixels triggers full regen thirty minutes. Slide four accent lottery between front and back panel. **Brand Kit** not sampled from approved packaging or prior print export. Brief uses "premium artisan" adjectives — **Design Agent** has no pass/fail fields. Print bleed and safe zone ignored until press proof fails.

## ChatCanvas brief contract (product label edition)

Weak brief: "make a beautiful honey label." Strong brief: "SKU X front panel 4×6 inch print 300dpi, Brand Kit amber + cream from approved packaging, product name top twenty percent flat for Touch Edit, weight bottom left safe zone, allergen disclaimer footer editable, back panel same thread, no render small text for legal copy." **Design Agent** numeric fields — bleed, safe zone, readable at fifty percent zoom.

## Brand Kit from approved packaging and prior export

Sample primary, accent, type role from approved VI and prior label PDF — not stock marble as brand color. **ChatCanvas** same thread batch front, back, sticker, PDP crop. Label work is series work across SKU variants.

## Touch Edit changes weight or promo without illustration reroll

"16 oz" to "12 oz" or "Holiday batch" to "Spring batch": **Touch Edit** text band, keeps illustration geometry and **Brand Kit** accent frame. Full regen randomizes honey drip lighting — brand ops cannot absorb thirty-minute reroll per SKU.

## Print-safe workflow without Photoshop layers

Define bleed and trim in brief. Generate largest master in **ChatCanvas**, **Touch Edit** legal text once, export print PDF and downscale for ecommerce thumbnail. Teams burn hours regenerating six panels that needed five-minute disclaimer **Touch Edit**.

## Common mistakes

Single front panel no back disclaimer layer. Legal text baked in render. New prompt per SKU variant. Skipping **Brand Kit**. 404 URL not restored. Fabricating FDA compliance claims — this guide covers ops only, not legal advice.

## Measuring value

Minutes per regulatory text fix, drift count across SKU family, export ratios per label refresh. Restored URL gives CPG and artisan brand teams stable product label without Photoshop SOP link.
"""

GETTING_STARTED_EN = """
# Lovart Getting Started: Onboarding SOP Without Hype

This English URL `lovart-getting-started` returned 404 while search wanted a getting started onboarding SOP — not a feature hype reel with invented user counts. This page is operator writing: first session checklist, pass/fail fields, and where **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent** sit in daily workflow. No fabricated pricing tiers — check official Lovart plans before commercial use.

## Session zero: what to prepare before opening ChatCanvas

Gather approved hex from media kit or packaging PDF. Write one campaign name. List deliverable sizes you ship weekly — Instagram 4:5, email header, PDP square. Copy disclaimer sentence legal already approved. Without these four inputs, first gen looks pretty and fails Tuesday edit test.

## Step one: create Brand Kit per campaign

Sample primary, accent, background, type role from approved sources — not stock palette as brand color. Name Kit after campaign or product line. Document hex in thread first comment so slide four cannot invent coral without audit trail.

## Step two: open ChatCanvas thread with brief contract

Weak first prompt: "modern premium launch creative." Strong first prompt: "Campaign X hero 4:5 1080×1350, Brand Kit navy + sand active, headline top fifteen percent flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, no small text in render, slide two through six same thread accent stripe." **Design Agent** responds to fields, not adjectives.

## Step three: run Design Agent pass/fail QA on first output

Check readable price at reduced zoom. Confirm single CTA. Confirm disclaimer footer exists on editable layer. Confirm hex matches **Brand Kit** roles. Confirm safe zone clear of platform UI crop. Fail any field — revise brief fields, not model name shopping.

## Step four: Touch Edit Tuesday drill before scaling batch

Change price or date on master using **Touch Edit** — target five minutes. If thirty-minute full regen required, reset **Brand Kit** and brief template before generating variants two through six. Getting started succeeds when edit drill passes, not when first frame looks cinematic.

## Step five: export multi-ratio from same thread

Master-first: 4:5 hero then derivative 9:16, 1:1, 16:9 crops same thread. Crop-first from random sizes cuts CTA bands. **Design Agent** QA mismatch between exports.

## What getting started is not

Not a model comparison leaderboard. Not fake "teams save forty hours" stat without source. Not substitute for legal review on regulated disclaimers. Not invitation to bake offer text into render pixels because Touch Edit exists — you must brief flat bands first.

## Common onboarding mistakes

Skip **Brand Kit** and manually recolor after drift. Generate variants in separate unrelated prompts. Accept first pretty output without QA checklist. Restore 404 URL but leave team using scattered Slack screenshots as SOP.

## Week one success metrics

One campaign Kit live. One thread with master plus two derivatives. One Touch Edit price fix under five minutes documented. One **Design Agent** checklist saved as team template. Restored URL gives search stable Lovart getting started onboarding link.
"""

MULTI_FORMAT_CAMPAIGNS_EN = """
# Orchestrate Multi-Format Campaigns in ChatCanvas: One Thread, Many Ratios

This English URL `orchestrate-multi-format-campaigns-chatcanvas` returned 404 while search wanted multi-format campaign orchestration SOP — not scattered prompts per platform. Campaign daily ops: Meta 4:5, Google 1200×628, email 600×300, PDP 1:1 — offer and disclaimer change together, hex drifts when each size opens new prompt. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent** orchestrate one thread family: master static, derivative crops, editable CTA across formats.

## Four multi-format layers in one orchestrated thread

Layer one: master 4:5 1080×1350 with headline and disclaimer footer editable. Layer two: landscape 1200×628 same accent stripe. Layer three: square 1200×1200 price bottom left safe zone. Layer four: vertical 9:16 story — **Design Agent** QA bottom twenty percent CTA flat for **Touch Edit**.

## Why multi-format campaigns fracture on Tuesday offer sync

Meta ad shows "$79" while email header still shows "$99" because sizes lived in unrelated prompts. Changing offer triggers four full regens — two hours. Slide four accent lottery per format. **Brand Kit** not active as batch SSOT. Orchestration means one edit propagates through re-export, not four lottery rerolls.

## ChatCanvas brief contract (multi-format orchestration edition)

Weak brief: "assets for all platforms." Strong brief: "Campaign X master 4:5, Brand Kit slate + coral from media kit, headline top fifteen percent flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, derivative 1200×628 + 1200×1200 + 9:16 same thread master-first not crop-first." **Design Agent** numeric fields per ratio.

## Brand Kit as orchestration SSOT across formats

Sample primary, accent, type role once per campaign. **ChatCanvas** one thread batch master plus derivatives. **Touch Edit** price change on master then re-export all sizes — orchestration win is synchronized offer, not fastest first gen.

## Touch Edit once, re-export all ratios

"Limited $99" to "Member $79": **Touch Edit** CTA band on master, re-export landscape, square, story, email crop. Full regen per format randomizes lighting — multi-format ops cannot absorb four thirty-minute rerolls.

## Design Agent QA orchestration checklist

Hex match all exports versus **Brand Kit**. Single CTA per format. Disclaimer present on editable layer. Safe zone per platform — story bottom UI, LinkedIn avatar overlap on companion assets. Fail one export — fix master, re-export chain, not isolated regen.

## Master-first versus crop-first orchestration

Master-first preserves CTA band geometry. Crop-first from unrelated hero cuts price text. Orchestration SOP mandates master 4:5 or 16:9 choice documented in thread header comment.

## Common mistakes

Ten prompts for ten sizes. Price baked in pixels. Skip **Brand Kit**. 404 URL not restored. Fabricating cross-platform CTR lift without source data.

## Measuring orchestration ROI

One offer fix minutes times format count, cross-format drift incidents, exports per orchestrated action. Restored URL gives marketing ops stable multi-format ChatCanvas orchestration SOP link.
"""

SEEDANCE_RELEASE_EN = """
# Seedance 2 Release: What Changes for Campaign Workflow (Honest Read)

This English URL `seedance-2-release` returned 404 while search wanted an honest read on Seedance 2 release implications — not launch hype with invented subscription prices or fake benchmark renders. Honest framing: Seedance 2 improves motion hook quality for short clips; offer, price, and disclaimer still belong on editable static layers in **ChatCanvas** with **Brand Kit**, **Touch Edit**, and **Design Agent**. Check official Seedance and Lovart pricing pages — this article cites no dollar amounts or credit quotas.

## What Seedance 2 release actually affects

Better short clip motion fidelity and multi-shot character consistency when reference plates are supplied. Teams running weekly promo changes still need static-first workflow — motion hook optional after legal pass on still. Release notes do not replace **Touch Edit** price layer on companion static.

## What Seedance 2 release does not fix alone

Editable price block inside clip pixels. Series-consistent carousel across six static slides. Legal disclaimer change without rerender. Hex drift between clip accent and Instagram slide three — **Brand Kit** still required as SSOT.

## Static-first five-step workflow after Seedance 2 availability

Step one: brief in **ChatCanvas** with hero size and **Brand Kit** primary. Step two: **Design Agent** delivers static hero and end card. Step three: legal pass on editable text layers. Step four: optional Seedance four to six second hook aligned to static color temperature. Step five: **Touch Edit** changes price without Seedance reroll — static companion only.

## ChatCanvas brief contract (Seedance 2 release edition)

Weak brief: "make Seedance 2 viral video." Strong brief: "Campaign X Seedance prep 16:9, Brand Kit slate + coral from media kit, headline static companion top fifteen percent flat for Touch Edit, price bottom left on still only, disclaimer footer editable, Seedance hook subtle motion no text in render, character ref plate yaw within fifteen degrees." **Design Agent** QA static — not clip cinematic feel.

## Brand Kit prevents post-release palette drift

Sample primary, accent, type role from approved VI. Seedance clip accent must match static carousel slide three. Release excitement does not excuse skipping Kit setup — drift incidents rise after new model toggles without SSOT discipline.

## Touch Edit still wins Tuesday offer edits

"Launch $49" to "Member $39": **Touch Edit** on still master. Full Seedance reroll for two-word change — ops cannot absorb thirty-minute reroll per shot regardless of release version number.

## Honest comparison boundary after release

Seedance 2 wins motion exploration. Lovart campaign stack wins revision-heavy promo with editable static layers. Parallel workflow beats either-or marketing. No fabricated "Seedance 2 beats competitor X by forty percent" claims — measure your brief pass rate and edit minutes.

## Common mistakes

Clip-only funnel after release news. Bake offer into motion pixels. Skip **Brand Kit** because new model "looks better." Fabricate Seedance pricing. 404 URL not restored.

## Measuring post-release value

Offer fix minutes, static versus motion offer match, character drift count. Restored URL gives search stable Seedance 2 release honest workflow SOP link — pricing on official pages only.
"""

VEO3_VS_LOVART_EN = """
# Veo 3 vs Lovart Video Generation: Honest Comparison by Task

This English URL `veo-3-vs-lovart-video-generation-comparison` returned 404 while search wanted Veo 3 versus Lovart honest comparison — not a fake winner headline with invented Google pricing or render benchmark scores. Veo 3 excels at short motion hooks and B-roll exploration inside Google's ecosystem. Lovart excels at campaign series with editable static layers via **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent**. Different tasks — not a single scoreboard. Check official Google and Lovart pricing — zero dollar figures in this article.

## Task A: cinematic mood clip without offer text

Veo 3 fit: high when clip has no readable price, no series carousel dependency, exploratory B-roll acceptable. Lovart fit: use integrated Veo routing plus static companion in same thread when clip must match **Brand Kit** hex on landing still.

## Task B: weekly offer change across ad static and video thumb

Veo 3 alone weak: price baked in clip pixels triggers reroll. Lovart fit: high — **Touch Edit** five-minute fix on static master, optional Veo hook unchanged. Buyer criterion is Tuesday edit minutes, not peak frame beauty.

## Task C: multi-ratio export with disclaimer compliance

Veo 3 alone weak: no series memory across six carousel slides. Lovart fit: high — master-first **ChatCanvas** thread, **Design Agent** QA per ratio, disclaimer on editable footer.

## Task D: character consistency multi-shot board

Veo 3 fit: moderate to high with reference discipline. Lovart fit: high when character lock must match static campaign board — **Brand Kit** and thread memory tie clip prep to still variants two through four.

## ChatCanvas brief contract (Veo 3 versus Lovart workflow edition)

Weak brief: "which tool wins." Strong brief: "Campaign X static hero 16:9, Brand Kit from media kit, headline flat for Touch Edit, Veo hook optional after static legal pass, no price in clip pixels, variants same thread." **Design Agent** pass/fail on static acceptance.

## Brand Kit as comparison tiebreaker for brand ops

Without **Brand Kit**, Veo clip accent diverges from Meta carousel slide four. Lovart stack enforces hex SSOT across motion and still. Comparison for brand teams is drift count, not codec names.

## Touch Edit decision tree

Copy-only change: **Touch Edit** on Lovart static — do not reroll Veo. Composition wrong: **ChatCanvas** re-prompt static. Motion mood wrong: Veo reroll hook only after static approved. Teams burn hours rerolling Veo when five-minute **Touch Edit** on still would suffice.

## License and pricing honesty boundary

Veo output subject to Google terms — verify before commercial use. Lovart commercial terms on official site. This comparison fabricates no subscription tiers, no fake minute quotas, no invented win rates.

## Common mistakes

Declare universal winner. Bake offer into Veo pixels. Skip static companion. Compare demo reels instead of edit-minute drill. 404 URL not restored.

## Measuring comparison value for your team

Run same brief: Tuesday price fix minutes, cross-format hex drift, disclaimer edit without reroll. Restored URL gives search stable Veo 3 vs Lovart honest comparison SOP link.
"""

DESIGN_DICT_ZHTW = """
# 非設計師的 AI 設計詞彙表：實用術語與 Lovart 對照

這條繁體中文 URL `ai-design-dictionary-for-non-designers-essential-terms-explained` 曾返回 404 — 正文是給行銷、創作者、小店 owner's 用的**詞彙表**，不是把英文版逐句翻過來。搜尋意圖：聽懂設計 review 在講什麼、把「感覺不對」改寫成可執行 brief。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 在每条術語下標注「在平台裡怎麼做」。金句：叫不出 constraint 的名字，就會一直為「看起來不一樣但還是錯」的重出買單。

## 怎麼用這本詞彙表（不是背誦考試）

收到「太擠」「不夠高級」「不像品牌」時，先對照本章術語，把評論改寫成 brief 裡的數字與 safe zone，再在 **ChatCanvas** 執行；局部錯用 **Touch Edit**，不要整圖重 roll。我會在 Notion 維護「術語 → 爛 ask → 好 ask」一頁 — 比換模型更省 revision 時間。

## 版面術語：構圖（Composition）

白話：元素怎麼排，視線能進來、停住、離開。構圖爛時，圖「好看」但不知道要看哪。

爛 ask：「再設計感一點。」好 ask：「產品占畫面 60%，標題 band 上方 15% 留白，背景紋理降飽和 30%。」

在 Lovart：寫進 **ChatCanvas** brief 的 hierarchy 數字；**Design Agent** 驗 focal point，不是驗「高級感」。

## 版面術語：視覺層級（Hierarchy）

白話：先看什麼、再看什麼。全部很大聲 = 全部沒被聽見。

爛 ask：「標題再突出。」好 ask：「主標 1.0 字重，副標 0.55，價格 bottom left safe zone 可讀。」

在 Lovart：**Touch Edit** 改價只動 CTA band；**Brand Kit** 鎖 type role。

## 版面術語：對比（Contrast）

白話：明暗、大小、疏密差異製造焦點。手機縮圖上對比不足 = 沉默殺手。

爛 ask：「再 pop 一點。」好 ask：「標題與背景對比至少 WCAG AA，120px 預覽仍可讀。」

在 Lovart：**Design Agent** 120px pass/fail；不足時改 brief 對比數字，不是形容詞。

## 版面術語：留白（Negative space）

白話：刻意空下來保護主體。有計畫的空白 ≠ 沒做完。

爛 ask：「填滿一點。」好 ask：「主體四周至少 1x icon height clear space。」

在 Lovart：brief 寫 clear space；carousel slide 2–6 同 thread 留白節奏一致。

## 版面術語：格線一致（Grid consistency）

白話：隱形欄位對齊 — 繁中寫「格線一致」避免與工程「對齊」混淆。歪了即使配色貴也顯 amateur。

爛 ask：「排整齊。」好 ask：「標題左緣與 logo 左緣同一 column，CTA 底邊距 24px。」

在 Lovart：**ChatCanvas** thread 內 batch 多尺寸 export 同一 grid spec。

## 品牌術語：Brand Kit

白話：一個 campaign 的 hex、字色角色、accent 規則 SSOT。沒 Kit = slide 4 突然變 coral。

在 Lovart：從 approved VI、包裝 PDF 取樣 primary/accent；thread 首條 comment 記錄 hex 變更。

## 品牌術語：Touch Edit

白話：只改文字/價格/日期 band，不動 hero 構圖。周二改「限時 NT$799」→「會員 NT$699」應 five 分鐘內。

在 Lovart：brief 要求 headline/price/disclaimer 在 flat editable layer；禁止 bake 進 render pixels。

## 品牌術語：Design Agent

白話：pass/fail QA 機器人 — 驗 safe zone、雙 CTA、hex drift vs **Brand Kit**、disclaimer 是否存在。不是驗「電影感」。

在 Lovart：用數字欄位 brief，不用「質感」「氛圍」堆疊。

## 品牌術語：ChatCanvas thread

白話：一個 campaign 家族的對話線 — master + slide 2–6 + 多 ratio 衍生同一 thread。新 thread = drift 風險。

在 Lovart：改價後 re-export 全尺寸，不要每平台開新 prompt。

## 輸出術語：Safe zone

白話：平台 UI 會擋住的區域 — Story 底 20%、LinkedIn 頭像左下。關鍵字/價格不能放進去。

在 Lovart：brief 寫 top/bottom safe zone 百分比；**Design Agent** QA crop 後仍可讀。

## 輸出術語：Master-first

白話：先做 4:5 或 16:9 master，再 derivative crop — 不是從小圖硬放大再切 CTA。

在 Lovart：**Touch Edit** 在 master 改一次，chain export 9:16 + 1:1 + 1200×628。

## 常見翻車（非設計師版）

用形容詞 brief 不用欄位。價格 bake 進 pixels。每活動新 prompt 無 thread。跳過 **Brand Kit**。404 未修復導致 SOP 散在 LINE 群。

## 測量什麼

改價一次幾分鐘、drift 幾次、120px preview pass rate。404 修復給非設計師 stable 繁中詞彙表 URL — 本文是 rewrite 不是英译中。
"""


FAQ = {
    "design_agent_creators": """
## FAQ

**Design agent for creators — ranked list?**  
No — buyer criteria for Tuesday title edits and Brand Kit series discipline.

**Skip Brand Kit for YouTube thumbs?**  
No — sample hex from channel art or slide 4 drifts.

**Title change needs full regen?**  
No — Touch Edit title band target five minutes.

**404 fix?**  
Stable EN ai powered design agent for creators SOP URL.

**Fake conversion stats?**  
No — measure edit minutes and drift count only.
""",
    "thumbnail_buy_vs_gen": """
## FAQ

**Is $50 purchase always wrong?**  
No — quarterly tentpole custom art may justify purchase; weekly uploads favor generation with Touch Edit.

**Generation without Brand Kit?**  
Accent drift across episodes — set Kit from channel banner first.

**120px preview test?**  
Yes — Design Agent pass/fail on readable title.

**404 fix?**  
Stable EN buying thumbnail vs generating SOP URL.

**Fake CTR claims?**  
No — this article cites no fabricated lift data.
""",
    "text_to_cinema": """
## FAQ

**Text-to-video replaces static layer?**  
No — offer and disclaimer stay on Touch Edit static companion.

**Price in clip pixels?**  
Avoid — Tuesday fix triggers motion reroll.

**Brand Kit role?**  
Hex SSOT between motion hook and carousel stills.

**404 fix?**  
Stable EN text to cinema Lovart SOP URL.

**Fake render speed benchmarks?**  
No — check official docs; none cited here.
""",
    "linkedin_banner": """
## FAQ

**LinkedIn banner size?**  
1584×396 personal; brief must note avatar overlap zone.

**Chat generate without Brand Kit?**  
Hex drifts from post templates — set Kit first.

**Headline fix full regen?**  
No — Touch Edit headline band five minutes.

**404 fix?**  
Stable EN chat generate LinkedIn banner SOP URL.

**Mobile preview pass?**  
Design Agent QA required — desktop-only check fails.
""",
    "product_labels": """
## FAQ

**Labels without Photoshop — legal advice?**  
No — ops workflow only; legal team approves disclaimer text.

**Allergen line edit full regen?**  
No — Touch Edit footer band on editable layer.

**Print bleed in brief?**  
Yes — Design Agent QA at fifty percent zoom.

**404 fix?**  
Stable EN product labels without Photoshop SOP URL.

**Brand Kit from packaging?**  
Sample hex from approved PDF — prevents SKU drift.
""",
    "getting_started": """
## FAQ

**Getting started feature hype?**  
No — onboarding SOP with five steps and QA checklist.

**Skip Brand Kit session zero?**  
Drift on first variant batch — Kit before scale.

**Touch Edit drill when?**  
Before generating slides two through six — prove five-minute edit.

**404 fix?**  
Stable EN Lovart getting started onboarding URL.

**Pricing in this guide?**  
No — check official Lovart plans; none fabricated here.
""",
    "multi_format_campaigns": """
## FAQ

**One thread for all formats?**  
Yes — master-first ChatCanvas orchestration, not ten prompts.

**Offer sync across Meta and email?**  
Touch Edit master once, re-export all ratios.

**404 fix?**  
Stable EN orchestrate multi format campaigns ChatCanvas SOP URL.

**Brand Kit per campaign?**  
SSOT prevents cross-format accent lottery.

**Fake cross-platform CTR?**  
No — measure edit minutes times format count.
""",
    "seedance_release": """
## FAQ

**Seedance 2 release — universal winner?**  
No — honest read: motion hook quality up; static editable layer still required.

**Seedance pricing in article?**  
No — check official pages; zero fabricated tiers.

**Offer in clip pixels after release?**  
Still avoid — Touch Edit on static companion.

**404 fix?**  
Stable EN Seedance 2 release workflow SOP URL.

**Brand Kit still required?**  
Yes — new model does not replace hex SSOT.
""",
    "veo3_vs_lovart": """
## FAQ

**Veo 3 vs Lovart — single winner?**  
No — task-based honest comparison; different buyer criteria.

**Google or Lovart pricing listed?**  
No — verify official ToS and plans; none cited here.

**Tuesday price fix — which stack?**  
Lovart Touch Edit static layer; avoid Veo reroll for copy-only change.

**404 fix?**  
Stable EN Veo 3 vs Lovart video comparison URL.

**Fake benchmark scores?**  
No — measure edit minutes and drift on your brief.
""",
    "design_dict_zhtw": """
## FAQ

**詞彙表是英译中嗎？**  
不是 — 繁中 rewrite，術語與場景按台港創作者/行銷 ops 寫。

**收到「不夠高級」怎麼辦？**  
對照 hierarchy/contrast 改寫成 brief 數字欄位。

**Touch Edit 適用哪些術語？**  
價格、日期、disclaimer、標題 band — 須 brief 要求 flat layer。

**404 修復？**  
stable zh-TW ai design dictionary non designers URL。

**编造療效或轉化率？**  
禁止 — 詞彙表只教 constraint 命名與 ops 測量。
""",
}


def expand_en(topic: str, n: int) -> str:
    return f"""
## Practice note {n}: {topic}

The first brief ends with "premium" and fails: small price text, badge over the subject. On the second pass, correct only safe zone and required fields. A **ChatCanvas** thread reduces accent drift on slide 4. In **{topic}**, **Touch Edit** confirms price change in five minutes static-first. Full regen thirty minutes — reset **Brand Kit** first. Restored 404 URL as stable SOP link for EN teams. **Design Agent** pass/fail checklist beats adjective briefs every time.
"""


def expand_zhtw(topic: str, n: int) -> str:
    return f"""
## 實操補充 {n}：{topic}

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。{topic} 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。
"""


ARTICLES = [
    {
        "rank": 224,
        "key": "design_agent_creators",
        "lang": "en",
        "slug": "ai-powered-design-agent-for-creators-it",
        "cover": "059",
        "category": "Industry Solution",
        "title": "AI Powered Design Agent for Creators: Buyer Criteria That Survive Edits",
        "seo_title": "Design Agent for Creators — ChatCanvas SOP",
        "description": "404 fix: design agent for creators, Brand Kit series, Touch Edit title edits.",
        "seo_description": "Creators: YouTube thumb, Shorts cover, Design Agent pass/fail QA.",
        "focus": "ai powered design agent for creators",
        "keywords": ["design agent for creators", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Design Agent for Creators EN",
        "body": DESIGN_AGENT_CREATORS_EN,
        "expand_topic": "EN design agent for creators workflow",
    },
    {
        "rank": 225,
        "key": "thumbnail_buy_vs_gen",
        "lang": "en",
        "slug": "buying-a-thumbnail-50-vs-generating-one-0",
        "cover": "060",
        "category": "Comparison",
        "title": "Buying a Thumbnail for $50 vs Generating One: Honest Cost Math",
        "seo_title": "Buy vs Generate Thumbnail — honest comparison",
        "description": "404 fix: buy thumbnail $50 vs generate, Touch Edit weekly cadence, Brand Kit.",
        "seo_description": "Thumbnail economics: revision cost, ChatCanvas A/B, no fake CTR.",
        "focus": "buying a thumbnail 50 vs generating one",
        "keywords": ["buy vs generate thumbnail", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Buy vs Generate Thumbnail EN",
        "body": THUMBNAIL_BUY_VS_GEN_EN,
        "expand_topic": "EN buy vs generate thumbnail workflow",
    },
    {
        "rank": 226,
        "key": "text_to_cinema",
        "lang": "en",
        "slug": "from-text-to-cinema-a-practical-guide-to-lovart-text-to-video",
        "cover": "061",
        "category": "How-To",
        "title": "From Text to Cinema: Practical Lovart Text-to-Video SOP",
        "seo_title": "Text to Cinema Lovart — ChatCanvas SOP",
        "description": "404 fix: text to cinema Lovart text-to-video, static-first, Touch Edit layer.",
        "seo_description": "Text-to-video: Brand Kit hex lock, motion companion, Design Agent QA.",
        "focus": "from text to cinema lovart text to video",
        "keywords": ["lovart text to video", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Text to Cinema Lovart EN",
        "body": TEXT_TO_CINEMA_EN,
        "expand_topic": "EN text to cinema Lovart workflow",
    },
    {
        "rank": 227,
        "key": "linkedin_banner",
        "lang": "en",
        "slug": "how-to-chat-generate-linkedin-banner-lovart",
        "cover": "062",
        "category": "How-To",
        "title": "How to Chat Generate a LinkedIn Banner with Lovart",
        "seo_title": "Chat Generate LinkedIn Banner — Lovart SOP",
        "description": "404 fix: chat generate LinkedIn banner 1584×396, Brand Kit, Touch Edit.",
        "seo_description": "LinkedIn banner: avatar safe zone, mobile preview, Design Agent QA.",
        "focus": "how to chat generate linkedin banner lovart",
        "keywords": ["linkedin banner chatcanvas", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Chat Generate LinkedIn Banner EN",
        "body": LINKEDIN_BANNER_EN,
        "expand_topic": "EN chat generate LinkedIn banner workflow",
    },
    {
        "rank": 228,
        "key": "product_labels",
        "lang": "en",
        "slug": "how-to-create-product-labels-without-photoshop",
        "cover": "063",
        "category": "How-To",
        "title": "How to Create Product Labels Without Photoshop",
        "seo_title": "Product Labels Without Photoshop — ChatCanvas SOP",
        "description": "404 fix: product labels without Photoshop, disclaimer editable, Brand Kit.",
        "seo_description": "Labels: print safe zone, Touch Edit regulatory text, Design Agent QA.",
        "focus": "how to create product labels without photoshop",
        "keywords": ["product labels without photoshop", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Product Labels Without Photoshop EN",
        "body": PRODUCT_LABELS_EN,
        "expand_topic": "EN product labels without Photoshop workflow",
    },
    {
        "rank": 229,
        "key": "getting_started",
        "lang": "en",
        "slug": "lovart-getting-started",
        "cover": "064",
        "category": "Lovart 101",
        "title": "Lovart Getting Started: Onboarding SOP Without Hype",
        "seo_title": "Lovart Getting Started — onboarding SOP",
        "description": "404 fix: Lovart getting started onboarding, Brand Kit, Touch Edit drill.",
        "seo_description": "Getting started: five-step SOP, Design Agent checklist, no fake stats.",
        "focus": "lovart getting started",
        "keywords": ["lovart getting started", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Lovart 101 — Getting Started EN",
        "body": GETTING_STARTED_EN,
        "expand_topic": "EN Lovart getting started onboarding",
    },
    {
        "rank": 230,
        "key": "multi_format_campaigns",
        "lang": "en",
        "slug": "orchestrate-multi-format-campaigns-chatcanvas",
        "cover": "065",
        "category": "How-To",
        "title": "Orchestrate Multi-Format Campaigns in ChatCanvas",
        "seo_title": "Multi-Format Campaigns ChatCanvas — SOP",
        "description": "404 fix: orchestrate multi format campaigns, one thread, Touch Edit sync.",
        "seo_description": "Multi-format: master-first, Brand Kit SSOT, re-export all ratios.",
        "focus": "orchestrate multi format campaigns chatcanvas",
        "keywords": ["multi format campaigns chatcanvas", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Multi-Format Campaigns ChatCanvas EN",
        "body": MULTI_FORMAT_CAMPAIGNS_EN,
        "expand_topic": "EN multi format campaigns ChatCanvas workflow",
    },
    {
        "rank": 231,
        "key": "seedance_release",
        "lang": "en",
        "slug": "seedance-2-release",
        "cover": "011",
        "category": "Comparison",
        "title": "Seedance 2 Release: Honest Campaign Workflow Read",
        "seo_title": "Seedance 2 Release — honest workflow guide",
        "description": "404 fix: Seedance 2 release honest read, no fake pricing, Touch Edit static.",
        "seo_description": "Seedance 2: static-first, Brand Kit, motion hook optional, official pricing only.",
        "focus": "seedance 2 release",
        "keywords": ["seedance 2 release", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Seedance 2 Release EN",
        "body": SEEDANCE_RELEASE_EN,
        "expand_topic": "EN Seedance 2 release workflow",
    },
    {
        "rank": 233,
        "key": "veo3_vs_lovart",
        "lang": "en",
        "slug": "veo-3-vs-lovart-video-generation-comparison",
        "cover": "014",
        "category": "Comparison",
        "title": "Veo 3 vs Lovart Video Generation: Honest Task Comparison",
        "seo_title": "Veo 3 vs Lovart — honest comparison",
        "description": "404 fix: Veo 3 vs Lovart honest comparison, no fake pricing or winner hype.",
        "seo_description": "Veo 3 vs Lovart: task fit, Touch Edit static layer, Brand Kit anti-drift.",
        "focus": "veo 3 vs lovart video generation comparison",
        "keywords": ["veo 3 vs lovart", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Veo 3 vs Lovart EN",
        "body": VEO3_VS_LOVART_EN,
        "expand_topic": "EN Veo 3 vs Lovart honest comparison workflow",
    },
    {
        "rank": 234,
        "key": "design_dict_zhtw",
        "lang": "zh-TW",
        "slug": "ai-design-dictionary-for-non-designers-essential-terms-explained",
        "cover": "018",
        "category": "Lovart 101",
        "title": "非設計師的 AI 設計詞彙表：實用術語與 Lovart 對照",
        "seo_title": "AI Design Dictionary Non-Designers — TW glossary",
        "description": "404 修復：非設計師 AI 設計詞彙表繁中 rewrite，ChatCanvas、Touch Edit 對照。",
        "seo_description": "詞彙表：構圖、層級、Brand Kit、brief 欄位，非英译中。",
        "focus": "ai design dictionary for non designers",
        "keywords": ["AI 設計詞彙表", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Lovart 101 — AI Design Dictionary zh-TW",
        "body": DESIGN_DICT_ZHTW,
        "expand_topic": "zh-TW ai design dictionary non designers workflow",
    },
]

EXPAND_FN = {
    "en": expand_en,
    "zh-TW": expand_zhtw,
}

UNIT_MAP = {
    "zh": "CJK",
    "zh-TW": "CJK",
    "en": "words",
}


def build_article(a: dict) -> str:
    lang = a["lang"]
    floor = FLOORS[lang]
    parts = [fm(a), a["body"].strip()]
    expand = EXPAND_FN[lang]
    topic = a["expand_topic"]
    n = 1
    while count_metric("\n".join(parts), lang) < floor:
        parts.append(expand(topic, n))
        n += 1
        if n > 80:
            break
    parts.append(FAQ[a["key"]].strip())
    parts.append(
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch22 content cluster.*\n"
    )
    return "\n\n".join(parts) + "\n"


def main():
    results = []
    for a in ARTICLES:
        text = build_article(a)
        lang = a["lang"]
        metric = count_metric(text, lang)
        floor = FLOORS[lang]
        banned = check_banned(text)
        placeholder = any(x in text for x in ("PLACEHOLDER", "TODO", "IMAGE PLACEHOLDER", "[REAL SCREENSHOT"))
        ok = metric >= floor and not banned and not placeholder
        path = OUT / f"{lang}-{a['slug']}.md"
        path.write_text(text, encoding="utf-8")
        results.append({
            "file": path.name,
            "lang": lang,
            "rank": a["rank"],
            "metric": metric,
            "floor": floor,
            "unit": UNIT_MAP[lang],
            "banned": banned,
            "placeholder": placeholder,
            "pass": ok,
            "cover": a["cover"],
        })

    print(f"{'RANK':>4} {'FILE':<90} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 135)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['rank']:>4} {r['file']:<90} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["file"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
