#!/usr/bin/env python3
"""Generate PRODUCTION-PLAN rows 44-84 (How-To, Branding, Insight)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.howto_batch_builder import build_howto_body, build_longform_body  # noqa: E402
from lib.howto_batch_common import faq_schema, howto_schema, write_draft

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "PRODUCTION-PLAN.md"


def steps_for(topic: str, channel: str) -> list[tuple[str, str, str]]:
    return [
        (
            "Lock Brand Kit and canvas specs",
            f"Open **ChatCanvas** and load **Brand Kit** for your brand. Create an artboard at the native {channel} dimensions. Write a one-line outcome: audience, offer, and CTA. This prevents margin drift when you generate variants later.",
            f'Apply Brand Kit "[Brand]". Artboard for {channel}. Outcome: [audience] sees [offer] and taps [CTA]. Photography mood: [mood]. No off-palette accents.',
        ),
        (
            "Generate the hero layout",
            f"Use **Thinking Mode** when the brief includes compliance, localization, or multi-slide narrative. Generate the hero frame first—headline zone, subject, and CTA placement—before derivative sizes.",
            f'Hero {topic}: headline "[Headline]", subhead "[Subhead]", subject [describe], background [describe], Brand Kit colors, readable type, safe margins for {channel} UI overlays.',
        ),
        (
            "Refine with semantic edits",
            f"Use **Touch Edit** on the subject or product and **Text Edit** on headlines. If you need to swap a background or badge layer, try **Edit Elements** before regenerating the entire layout.",
            'Touch Edit: [object] — [change]. Text Edit: replace headline with "[New headline]" keeping font style. Preserve Brand Kit margins.',
        ),
        (
            "Produce size and copy variants",
            f"From the approved hero, prompt for companion sizes and alternate headlines. Keep **Identity Lock** on logos or products when testing offers.",
            'Match hero grid and Brand Kit. Generate [list sizes]. Variant B headline: "[Alt headline]". Same product geometry.',
        ),
        (
            "Export and publish checklist",
            f"Export PNG at 2x if the platform allows retina sharpness. Name files with campaign ID. Run squint-test on mobile before scheduling.",
            f"Export PNG sRGB at native width. Filename: [campaign]-[channel]-v1.png. Document approved version in project notes.",
        ),
    ]


def h(
    plan: int,
    filename: str,
    slug: str,
    title: str,
    kw: str,
    date: str,
    cluster: str,
    channel: str,
    specs: str,
    topic: str,
    tool: str = "ChatCanvas, Brand Kit, Touch Edit, Text Edit, Nano Banana 2",
    extra: list[tuple[str, str]] | None = None,
) -> dict:
    return {
        "plan": plan,
        "filename": filename,
        "slug": slug,
        "title": title,
        "focus_keyword": kw,
        "date": date,
        "category": "How-To",
        "content_cluster": cluster,
        "description": f"Step-by-step {topic} with Lovart's AI Design Agent—Brand Kit, ChatCanvas, and semantic edits for on-brand {channel} assets.",
        "seo_title": title[:58] + ("…" if len(title) > 58 else ""),
        "seo_description": f"{topic} on Lovart ChatCanvas—on-brand specs, prompts, and export checklist. Start free at lovart.ai/signup.",
        "tool": tool,
        "topic": topic,
        "channel": channel,
        "specs": specs,
        "steps": steps_for(topic, channel),
        "extra_links": extra or [],
        "internal_note": f"Plan #{plan} | How-To | target 1800+ words",
    }


HOW_TOS = [
    h(44, "how-to-twitter-x-image-posts-ai-engagement.md", "twitter-x-image-posts-ai-engagement",
       "How to Create Twitter/X Image Posts for Maximum Engagement", "twitter x image posts ai engagement",
       "2026-06-14", "Social Media How-To", "Twitter/X",
       "Single images: 1600×900 (16:9) or 1200×675; keep critical type inside center safe zone for crop on mobile.",
       "Twitter/X image posts", extra=[("composition rules", "/blog/composition-rules-design-rule-of-thirds-golden-ratio")]),
    h(45, "how-to-discord-telegram-community-graphics-ai.md", "discord-telegram-community-graphics-ai",
       "How to Design Discord and Telegram Community Graphics", "discord telegram community graphics ai",
       "2026-06-14", "Social Media How-To", "Discord / Telegram",
       "Discord server icon 512×512; banner 960×540; Telegram channel photo 640×360; emoji-safe simple shapes at small sizes.",
       "Discord and Telegram community graphics"),
    h(46, "how-to-shopify-product-images-ai.md", "shopify-product-images-ai",
       "How to Create Shopify Product Images with AI", "shopify product images ai",
       "2026-06-15", "E-Commerce How-To", "Shopify",
       "Product hero 2048×2048 or 3000×3000 square; lifestyle 4:5 optional; white-background SKU shots with consistent shadow.",
       "Shopify product images", tool="ChatCanvas, Brand Kit, Identity Lock, Touch Edit",
       extra=[("ecommerce sellers guide", "/blog/best-ai-design-agent-ecommerce-sellers")]),
    h(47, "how-to-etsy-listing-photos-ai.md", "etsy-listing-photos-ai",
       "How to Design Etsy Listing Photos That Stand Out", "etsy listing photos ai",
       "2026-06-15", "E-Commerce How-To", "Etsy",
       "Listing images 2000×2000 px (1:1); first image thumbnail must read at ~300px; lifestyle + scale + detail sequence.",
       "Etsy listing photos", extra=[("packaging design", "/blog/create-packaging-design-with-ai")]),
    h(48, "how-to-amazon-a-plus-content-ai.md", "amazon-a-plus-content-ai",
       "How to Create Amazon A+ Content with AI", "amazon a plus content ai",
       "2026-06-16", "E-Commerce How-To", "Amazon A+",
       "Modules vary; common hero 970×600; comparison charts and icon rows need legible type at mobile zoom.",
       "Amazon A+ content", extra=[("ecommerce sellers guide", "/blog/best-ai-design-agent-ecommerce-sellers")]),
    h(49, "how-to-product-detail-page-pdp-design-ai.md", "product-detail-page-pdp-design-ai",
       "How to Design Product Detail Pages (PDP) with AI", "product detail page pdp design ai",
       "2026-06-16", "E-Commerce How-To", "PDP",
       "Hero gallery 1:1 or 4:5; feature icons 64–128px; lifestyle banners 16:9; keep CTA color consistent with Brand Kit.",
       "product detail page (PDP) design", tool="ChatCanvas, Brand Kit, Edit Elements, Nano Banana Pro"),
    h(50, "how-to-size-chart-comparison-table-ai.md", "size-chart-comparison-table-ai",
       "How to Create Size Charts and Comparison Tables with AI", "size chart comparison table ai",
       "2026-06-17", "E-Commerce How-To", "size charts",
       "Tables as crisp PNG or SVG export; minimum 12px body type at mobile; high contrast grid lines.",
       "size charts and comparison tables", extra=[("create infographics", "/blog/create-infographics-with-ai")]),
    h(51, "how-to-batch-edit-product-colors-ai.md", "batch-edit-product-colors-ai",
       "How to Batch-Edit Product Colors — Same Product, Multiple Variants", "batch edit product colors ai",
       "2026-06-17", "E-Commerce How-To", "product variants",
       "Keep product geometry locked; swap colorways via Touch Edit / Identity Lock; export square SKUs per variant.",
       "batch product color variants", tool="ChatCanvas, Identity Lock, Touch Edit, Brand Kit"),
    h(52, "how-to-flyer-brochure-design-ai.md", "flyer-brochure-design-ai",
       "How to Design Flyers and Brochures with AI", "flyer brochure design ai",
       "2026-06-18", "Print & Physical How-To", "flyers / brochures",
       "US Letter 8.5×11 with 0.125 in bleed; tri-fold panels planned in ChatCanvas artboards; 300 DPI export for print.",
       "flyers and brochures", extra=[("design business cards", "/blog/design-business-cards-with-ai")]),
    h(53, "how-to-sticker-label-design-ai.md", "sticker-label-design-ai",
       "How to Create Stickers and Labels with AI", "sticker label design ai",
       "2026-06-18", "Print & Physical How-To", "stickers / labels",
       "Die-cut stickers: design with bleed; labels include barcode quiet zone; vector-friendly simple shapes.",
       "stickers and labels"),
    h(54, "how-to-t-shirt-apparel-graphics-ai.md", "t-shirt-apparel-graphics-ai",
       "How to Design T-Shirt and Apparel Graphics with AI", "t shirt apparel graphics ai",
       "2026-06-19", "Print & Physical How-To", "apparel",
       "Print area ~12×16 in at 300 DPI; limit fine lines that break on fabric; mock up on Smart Mockups.",
       "T-shirt and apparel graphics", tool="ChatCanvas, Brand Kit, Smart Mockups"),
    h(55, "how-to-event-banner-signage-design-ai.md", "event-banner-signage-design-ai",
       "How to Create Event Banners and Signage with AI", "event banner signage design ai",
       "2026-06-19", "Print & Physical How-To", "event signage",
       "Retractable banners 33×80 in; wayfinding 24×36 in; high contrast type readable at 10+ feet.",
       "event banners and signage"),
    h(56, "how-to-book-cover-design-ai.md", "book-cover-design-ai",
       "How to Design a Book Cover with AI", "book cover design ai",
       "2026-06-20", "Print & Physical How-To", "book covers",
       "Print cover: trim + spine + bleed per KDP/Ingram specs; thumbnail test at 150px height for Amazon grid.",
       "book covers", extra=[("typography 101", "/blog/typography-101-font-pairing-rules-non-designers")]),
    h(57, "how-to-magazine-layout-editorial-design-ai.md", "magazine-layout-editorial-design-ai",
       "How to Create Magazine Layouts and Editorial Design with AI", "magazine layout editorial design ai",
       "2026-06-20", "Print & Physical How-To", "editorial layouts",
       "Grid-based spreads; consistent baseline; export PDF spreads for print or long-scroll web features.",
       "magazine layouts and editorial design"),
    h(58, "how-to-trade-show-booth-exhibition-design-ai.md", "trade-show-booth-exhibition-design-ai",
       "How to Design Trade Show Booths and Exhibition Graphics", "trade show booth exhibition design ai",
       "2026-06-21", "Print & Physical How-To", "trade show booths",
       "Large-format 150+ DPI at final size; simplify logos; test readability from 15 feet.",
       "trade show booth graphics"),
    h(59, "how-to-custom-wall-art-prints-ai.md", "custom-wall-art-prints-ai",
       "How to Create Custom Wall Art and Prints with AI", "custom wall art prints ai",
       "2026-06-21", "Print & Physical How-To", "wall art",
       "Common ratios 2:3, 3:4; upscale before print; avoid fine noise that moirés on canvas.",
       "custom wall art and prints"),
    h(60, "how-to-cinematic-camera-movements-ai.md", "cinematic-camera-movements-ai",
       "How to Create Cinematic Camera Movements with AI", "cinematic camera movements ai",
       "2026-06-22", "Video How-To", "cinematic video",
       "Export 16:9 or 9:16 per channel; plan story beats before motion; use Seedance 2.0 / Veo 3 on ChatCanvas.",
       "cinematic camera movements", tool="ChatCanvas, Seedance 2.0, Veo 3, Brand Kit",
       extra=[("Veo 3 vs Lovart", "/blog/veo-3-vs-lovart-video-generation-comparison")]),
    h(61, "how-to-before-after-transformation-videos-ai.md", "before-after-transformation-videos-ai",
       "How to Create Before/After Transformation Videos with AI", "before after transformation videos ai",
       "2026-06-22", "Video How-To", "before/after video",
       "Match lighting and camera angle between states; disclose illustrative results where regulated.",
       "before/after transformation videos", tool="ChatCanvas, Seedance 2.0, Touch Edit",
       extra=[("product videos", "/blog/how-to-create-product-videos-with-ai")]),
    h(62, "how-to-ai-explainer-videos.md", "ai-explainer-videos",
       "How to Make AI-Generated Explainer Videos", "ai explainer videos",
       "2026-06-23", "Video How-To", "explainer video",
       "Script beats → scene boards on ChatCanvas → motion per scene; captions safe zone bottom 20%.",
       "AI explainer videos", tool="ChatCanvas, Seedance 2.0, Veo 3, Text Edit"),
    h(63, "how-to-multi-scene-brand-videos-character-consistency.md", "multi-scene-brand-videos-character-consistency",
       "How to Create Multi-Scene Brand Videos with Character Consistency", "multi scene brand videos character consistency",
       "2026-06-23", "Video How-To", "multi-scene brand video",
       "Use Identity Lock on hero character; storyboard all scenes before generating motion.",
       "multi-scene brand videos", tool="ChatCanvas, Identity Lock, Seedance 2.0, Veo 3",
       extra=[("AI shorts generator", "/blog/ai-shorts-generator-viral-short-form-video")]),
    h(64, "how-to-add-sound-music-ai-video.md", "add-sound-music-ai-video",
       "How to Add Sound and Music to AI-Generated Video", "add sound music ai video",
       "2026-06-24", "Video How-To", "video + audio",
       "Export silent master from Lovart; finalize audio in your NLE; respect platform loudness standards.",
       "sound and music for AI video", tool="ChatCanvas, Seedance 2.0",
       extra=[("lip sync guide", "/blog/ai-lip-sync-characters-speak-any-language")]),
    h(65, "how-to-brand-mascot-design-ai.md", "brand-mascot-design-ai",
       "How to Design a Brand Mascot with AI", "brand mascot design ai",
       "2026-06-24", "Logo & Brand How-To", "brand mascot",
       "Vector-friendly shapes; test at 32px favicon and large mural; lock with Identity Lock across campaigns.",
       "brand mascot design", extra=[("build brand kit", "/blog/build-complete-brand-kit-from-scratch-ai")]),
    h(66, "how-to-brand-color-palette-ai.md", "brand-color-palette-ai",
       "How to Create a Brand Color Palette with AI", "brand color palette ai",
       "2026-06-25", "Logo & Brand How-To", "color palette",
       "Define primary, secondary, neutrals, semantic colors (success/warn); document hex in Brand Kit.",
       "brand color palette", extra=[("color psychology", "/blog/color-psychology-brand-design-complete-guide")]),
    h(67, "how-to-brand-pattern-system-ai.md", "brand-pattern-system-ai",
       "How to Design a Brand Pattern System with AI", "brand pattern system ai",
       "2026-06-25", "Logo & Brand How-To", "pattern system",
       "Seamless tiles at power-of-two dimensions; test repeat at large backgrounds.",
       "brand pattern system"),
    h(68, "how-to-brand-guidelines-ai.md", "brand-guidelines-ai",
       "How to Create Brand Guidelines That Actually Get Used", "brand guidelines ai",
       "2026-06-26", "Logo & Brand How-To", "brand guidelines",
       "One-page quick reference plus detailed PDF; export samples from live Brand Kit.",
       "brand guidelines", extra=[("create brand style guide", "/blog/create-brand-style-guide-with-ai")]),
    h(69, "how-to-ab-test-ad-creatives-ai.md", "ab-test-ad-creatives-ai",
       "How to A/B Test Ad Creatives with AI", "ab test ad creatives ai",
       "2026-06-26", "Ad Creative How-To", "ad A/B tests",
       "Change one variable per variant; keep product locked with Identity Lock; log variant IDs in filenames.",
       "A/B test ad creatives", extra=[("Google Ads guide", "/blog/create-google-ads-with-ai-2026")]),
    h(70, "how-to-programmatic-display-ads-ai.md", "programmatic-display-ads-ai",
       "How to Create Programmatic Display Ads at Scale", "programmatic display ads ai",
       "2026-06-27", "Ad Creative How-To", "programmatic display",
       "Standard IAB sizes: 300×250, 728×90, 160×600, 300×600; weight limits per DSP.",
       "programmatic display ads at scale", extra=[("Google Ads guide", "/blog/create-google-ads-with-ai-2026")]),
    h(71, "how-to-retargeting-ad-visuals-ai.md", "retargeting-ad-visuals-ai",
       "How to Design Retargeting Ad Visuals That Convert", "retargeting ad visuals ai",
       "2026-06-27", "Ad Creative How-To", "retargeting ads",
       "Strong product recall; offer clarity; frequency-capped creative sets with consistent Brand Kit.",
       "retargeting ad visuals"),
]


def branding_article(
    plan: int, filename: str, slug: str, title: str, kw: str, date: str, cluster: str, thesis: str, sections: list
) -> dict:
    return {
        "plan": plan,
        "filename": filename,
        "slug": slug,
        "title": title,
        "focus_keyword": kw,
        "date": date,
        "category": "Branding",
        "content_cluster": cluster,
        "description": thesis[:280],
        "seo_title": (title[:57] + "…") if len(title) > 60 else title,
        "seo_description": f"{kw} for AI creators using Lovart—practical principles and workflows. Explore lovart.ai.",
        "tool": "ChatCanvas, Brand Kit",
        "thesis": thesis,
        "sections": sections,
        "internal_note": f"Plan #{plan} | Branding | target 3000+ words",
        "keywords": [kw, "lovart branding", "ai design education", "design fundamentals", "brand kit"],
        "tags": ["branding", "design education", "lovart"],
        "seo_schema": "FAQ",
    }


def insight_article(
    plan: int, filename: str, slug: str, title: str, kw: str, date: str, cluster: str, thesis: str, sections: list
) -> dict:
    return {
        "plan": plan,
        "filename": filename,
        "slug": slug,
        "title": title,
        "focus_keyword": kw,
        "date": date,
        "category": "Insight & Trend",
        "content_cluster": cluster,
        "description": thesis[:280],
        "seo_title": (title[:57] + "…") if len(title) > 60 else title,
        "seo_description": f"{kw}—Lovart research perspective on AI design agents. Read more at lovart.ai.",
        "tool": "ChatCanvas, MCoT",
        "thesis": thesis,
        "sections": sections,
        "internal_note": f"Plan #{plan} | Insight | target 3000+ words",
        "keywords": [kw, "ai design agent", "lovart insight", "generative ai trends", "design industry 2026"],
        "tags": ["insight", "trend", "lovart", "ai design agent"],
        "seo_schema": "FAQ",
        "extra_links": [
            ("AI design agent vs image generator", "/blog/insight-ai-design-agent-vs-image-generator-paradigm"),
        ],
    }


def _long_sections(topic: str) -> list[tuple[str, list[str]]]:
    """Generate deep sections for branding/insight (3000+ word target)."""
    return [
        (
            "The problem teams actually face",
            [
                f"Most teams approaching {topic} already produce content—they produce it inconsistently. The pain is not ignorance of best practices; it is **throughput pressure** without a governed system. Tools that emit one beautiful image accelerate the wrong metric if brand, compliance, and channel specs are recreated from scratch each time.",
                "Lovart's **Design Agent** model assumes marketing is a pipeline: brief, plan, generate, semantically edit, export. That pipeline is how agencies stayed solvent for decades—expressed now as **ChatCanvas** plus **Brand Kit** instead of folder sprawl.",
                "When every coordinator interprets 'on brand' differently, you get margin drift, competing blues, and headlines that fight photography. The organization does not need more inspiration—it needs a **Design Context Core** that travels with every export.",
            ],
        ),
        (
            "Principles that survive automation",
            [
                "Automation should encode decisions humans already made: palette, type roles, logo rules, photography mood, and CTA hierarchy. Anything still ambiguous after Brand Kit setup should be resolved in **Thinking Mode**, not by longer prompts.",
                "Semantic editing (**Touch Edit**, **Text Edit**, **Edit Elements**) exists because the last 10% of quality is object-level, not prompt-level. Teams that regenerate entire layouts for one word pay a latency tax that shows up in missed publishing windows.",
                "Inference agnosticism matters: model APIs change pricing and capability quarterly. Platforms that route across image and video models protect teams from vendor shock without forcing a re-learn of editing semantics.",
                "Accessibility and conversion are not opposites. Contrast minimums, type size, and clear hierarchy help both compliance and performance—especially on mobile feeds where thumbs cover corners.",
            ],
        ),
        (
            "How Lovart implements the practice",
            [
                "**MCoT (Mind Chain of Thought)** externalizes planning so stakeholders can correct direction before pixels render. **Identity Lock** protects heroes—products, mascots, spokespeople—across sizes and motion. Integrated video models (**Seedance 2.0**, **Veo 3**, **Kling**) reduce handoffs when channels demand motion from the same campaign brain.",
                "For operators, the shift is from mastering five single-purpose apps to directing one agent with persistent context—see [how to chat and generate any design type](/blog/how-to-chat-generate-any-design-type-lovart-agent).",
                "**Brand Kit** is not a mood board—it is executable rules the agent applies on every artboard. **ChatCanvas** is not a gallery—it is where variants stay comparable. **Edit Elements** is not a gimmick—it is how marketers get layer discipline without learning Photoshop.",
                "Hybrid stacks remain normal: stock libraries, DAMs, and specialist tools coexist. Lovart wins on campaign velocity after identity exists—not on replacing every legacy asset.",
            ],
        ),
        (
            "Operating model for marketing and creative leads",
            [
                "Assign one ChatCanvas project per campaign or quarter. All sizes and languages live there. Reviewers approve a contact sheet PDF, not scattered PNGs in chat.",
                "Monday: brief and constraints. Tuesday: hero approval with Brand Kit locked. Wednesday: variant explosion (sizes, headlines). Thursday: optional motion. Friday: QA export pack with filenames legal can archive.",
                "Measure revision rounds per asset, not images generated. A team generating 200 images with twelve rounds loses to a team generating forty images with two rounds.",
                "Train coordinators on Text Edit and Touch Edit before advanced video. Semantic edits compound; prompt roulette does not.",
            ],
        ),
        (
            "Industry patterns we see in production",
            [
                "Ecommerce teams use Identity Lock on pack shots, then explode marketplaces and ads from one hero. Agencies keep client Brand Kits per account to stop associate drift. Vertical SaaS ships feature launches with the same illustration grammar quarter after quarter.",
                "Regulated categories (health, finance, legal) add human QA gates but still cut production time when layouts are consistent. Education and nonprofits stretch budgets by batching social from one brief.",
                f"Across segments, the teams winning on {topic} treat AI as **production infrastructure**, not a slot machine for pretty frames.",
            ],
        ),
        (
            "Failure modes and how to avoid them",
            [
                "**Prompt inflation:** Novel-length prompts without Brand Kit confuse models. Fix with structured briefs and Thinking Mode.",
                "**Tool sprawl:** Hero in one app, type fix in another, video in a third—context loss guaranteed. Fix with ChatCanvas as system of record.",
                "**Unbounded variants:** Testing headline, color, product, and layout simultaneously teaches nothing. Fix with one-variable rules.",
                "**Rights ambiguity:** Uploading unlicensed references or client assets without contracts. Fix with documented sources and legal review on claims.",
            ],
        ),
        (
            "Checklist before you scale volume",
            [
                "1) Brand Kit documented with hex, type roles, and logo clear space. 2) One approved hero per campaign on ChatCanvas. 3) Variant rules: what may change (headline, offer) vs locked (product, margins). 4) Export naming convention. 5) Human QA for claims, accessibility contrast, and rights.",
                "Teams ignoring step five discover the **hallucination tax**—rework, brand incidents, and eroded trust—faster than teams ignoring step one.",
                "Publish internal 'approved prompt patterns' linked to Brand Kit—not a free-form prompt graveyard in a wiki.",
            ],
        ),
    ]


BRANDING = [
    branding_article(
        72, "better-design-accessible-design-inclusive-content-ai.md", "accessible-design-inclusive-content-ai",
        "Accessibility in Design: Making Content Inclusive with AI",
        "accessible design inclusive content ai", "2026-06-28", "Better Design — Accessibility",
        "Accessibility is not a filter applied at publish time—it is contrast, hierarchy, and alt text decided when layouts are generated. Lovart teams can encode contrast minimums in Brand Kit notes and QA exports before they ship.",
        _long_sections("accessible inclusive design"),
    ),
    branding_article(
        73, "better-design-ai-copyright-creators-guide-2026.md", "ai-copyright-creators-guide-2026",
        "AI and Copyright: What Creators Need to Know in 2026",
        "ai copyright creators guide 2026", "2026-06-28", "Better Design — Legal & Ethics",
        "Copyright in 2026 is a workflow question: what you generate, what you upload, what you publish, and what your client contract allows. Lovart does not replace counsel—but it centralizes assets so provenance and approvals are traceable.",
        _long_sections("AI copyright for creators"),
    ),
    branding_article(
        74, "better-design-print-design-basics-bleed-dpi-cmyk.md", "print-design-basics-bleed-dpi-cmyk",
        "Print Design Basics: Bleed, DPI, and CMYK Explained for AI Creators",
        "print design basics bleed dpi cmyk", "2026-06-29", "Better Design — Print",
        "AI creators hit print shops with RGB PNGs and wonder why colors shift. Bleed, DPI, and CMYK are not academic—they are the contract between your ChatCanvas export and a vendor who will not fix margins for free.",
        _long_sections("print bleed DPI CMYK"),
    ),
    branding_article(
        75, "better-design-responsive-design-aspect-ratios-guide.md", "responsive-design-aspect-ratios-guide",
        "Responsive Design: How to Think About Aspect Ratios",
        "responsive design aspect ratios guide", "2026-06-29", "Better Design — Layout",
        "Responsive design for marketers means planning artboards per channel—not stretching one hero until type breaks. Lovart multiplies formats from one governed brief instead of one accidental crop.",
        _long_sections("responsive aspect ratios"),
    ),
    branding_article(
        76, "better-design-design-psychology-visuals-convert.md", "design-psychology-visuals-convert",
        "Design Psychology: Why Some Visuals Convert and Others Don't",
        "design psychology visuals convert", "2026-06-30", "Better Design — Psychology",
        "Conversion is attention × clarity × trust. Psychology principles (contrast, gaze direction, scarcity cues) only work when brand governance keeps tests honest—same product, same claim evidence, one variable at a time.",
        _long_sections("design psychology and conversion"),
    ),
    branding_article(
        77, "better-design-design-styles-history-ai-prompting.md", "design-styles-history-ai-prompting",
        "The History of Design Styles — and How to Prompt AI for Each",
        "design styles history ai prompting", "2026-06-30", "Better Design — History",
        "Style references fail when prompts name eras without structure. Pair historical vocabulary with layout constraints in Brand Kit—Swiss grid, Art Deco symmetry, Y2K chrome—and let the agent execute consistently.",
        _long_sections("design styles and prompting"),
    ),
    branding_article(
        78, "better-design-visual-hierarchy-design-principle.md", "visual-hierarchy-design-principle",
        "Visual Hierarchy: The One Principle That Fixes 90% of Bad Design",
        "visual hierarchy design principle", "2026-07-01", "Better Design — Fundamentals",
        "Visual hierarchy is the ordering of what viewers see first, second, and third. Most 'bad AI design' is equal-weight chaos: headlines, badges, and backgrounds competing at the same volume.",
        _long_sections("visual hierarchy"),
    ),
]

INSIGHTS = [
    insight_article(
        79, "insight-death-static-impression-2026-motion.md", "death-static-impression-2026-motion",
        "The Death of the Static Impression: Why 2026 Demands Motion",
        "death static impression 2026 motion", "2026-07-01", "Insight & Trend — Motion",
        "Feeds in 2026 reward motion literacy, not still-image novelty alone. The winning teams pair governed stills on ChatCanvas with short motion cutdowns from the same Brand Kit—without rebuilding context in a separate video app.",
        _long_sections("static vs motion in 2026"),
    ),
    insight_article(
        80, "insight-ai-design-agent-vs-image-generator-paradigm.md", "ai-design-agent-vs-image-generator-paradigm",
        "AI Design Agent vs AI Image Generator: The Paradigm Shift",
        "ai design agent vs image generator paradigm", "2026-07-02", "Insight & Trend — Paradigm",
        "Image generators answer: 'make a picture.' Design agents answer: 'ship this campaign under these brand rules.' Lovart's bet is that marketing throughput needs the second question.",
        _long_sections("design agent vs image generator"),
    ),
    insight_article(
        81, "insight-model-loyalty-dead-inference-agnosticism.md", "model-loyalty-dead-inference-agnosticism",
        "Model Loyalty is Dead: The Rise of Inference Agnosticism",
        "model loyalty dead inference agnosticism", "2026-07-02", "Insight & Trend — Models",
        "Teams locked to one model vendor inherit that vendor's outages, price changes, and capability gaps. Agent platforms that route across models—image and video—optimize for outcomes, not logos on a slide.",
        _long_sections("inference agnosticism"),
    ),
    insight_article(
        82, "insight-hallucination-tax-agencies-fear-generative-ai.md", "hallucination-tax-agencies-fear-generative-ai",
        "The Hallucination Tax: Why Agencies Fear Generative AI",
        "hallucination tax agencies fear generative ai", "2026-07-03", "Insight & Trend — Agencies",
        "Agencies do not fear creativity—they fear unbillable rework: wrong logos, invented claims, off-brand colors, and client escalations. The hallucination tax is measured in Slack threads, not GPU seconds.",
        _long_sections("hallucination tax in agencies"),
    ),
    insight_article(
        83, "insight-specialist-to-generalist-ai-10x-designer.md", "specialist-to-generalist-ai-10x-designer",
        "From Specialist to Generalist: How AI Is Creating the 10x Designer",
        "specialist to generalist ai 10x designer", "2026-07-03", "Insight & Trend — Roles",
        "The 10x designer in 2026 is not faster at every craft—they are faster at orchestration: brief clarity, brand systems, semantic edits, and export discipline across channels.",
        _long_sections("10x designer generalist"),
    ),
    insight_article(
        84, "insight-ai-design-2027-predictions.md", "ai-design-2027-predictions",
        "AI Design in 2027: Predictions from the Lovart Research Team",
        "ai design 2027 predictions", "2026-07-04", "Insight & Trend — Forecast",
        "2027 rewards teams that treated 2025–2026 as systems building: Brand Kits, agent workflows, and QA—not prompt collections. Motion, governance, and cross-model routing compound from that foundation.",
        _long_sections("AI design 2027 predictions"),
    ),
]


def meta_from_howto(a: dict) -> dict:
    kw = [
        a["focus_keyword"],
        "lovart how to",
        "ai design agent",
        a["slug"].replace("-", " "),
        "brand kit",
        "chatcanvas",
    ]
    tags = [a["channel"].lower().split()[0], "how-to", "lovart"]
    return {
        **a,
        "keywords": kw,
        "tags": tags,
        "seo_schema": "HowTo",
    }


def update_plan(plan_num: int, wc: int):
    text = PLAN.read_text(encoding="utf-8")
    pat = rf"^\| {plan_num} \|"
    for i, line in enumerate(text.splitlines()):
        if re.match(pat, line):
            new = re.sub(r"\| (pending|draft-exists|\*\*draft-done\*\*[^|]*)\|", f"| **draft-done** (~{wc}w) |", line)
            lines = text.splitlines()
            lines[i] = new
            PLAN.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return


def main():
    results = []
    for a in HOW_TOS:
        m = meta_from_howto(a)
        body = f"# {m['title']}\n\n" + build_howto_body(m)
        steps = [s[0] for s in m["steps"]]
        structured = howto_schema(m["title"], m["description"], m.get("cover_url", ""), steps)
        if not m.get("cover_url"):
            from lib.howto_batch_common import pick_cover_url

            m["cover_url"] = pick_cover_url(m["slug"])
            structured = howto_schema(m["title"], m["description"], m["cover_url"], steps)
        wc = write_draft(m["filename"], m, body, structured)
        update_plan(m["plan"], wc)
        results.append((m["plan"], m["filename"], wc))

    for a in BRANDING + INSIGHTS:
        body = f"# {a['title']}\n\n" + build_longform_body(a)
        pairs = a.get("faq") or [
            ("Who is this for?", "Marketers, founders, and designers adopting Lovart for governed production."),
            ("Does Lovart replace legal advice?", "No. Copyright and compliance articles are educational—not legal counsel."),
        ]
        structured = faq_schema(pairs)
        from lib.howto_batch_common import pick_cover_url

        a["cover_url"] = pick_cover_url(a["slug"])
        wc = write_draft(a["filename"], a, body, structured)
        update_plan(a["plan"], wc)
        results.append((a["plan"], a["filename"], wc))

    print("Generated", len(results), "articles")
    for r in results:
        print(f"  #{r[0]} {r[1]}: {r[2]} words")


if __name__ == "__main__":
    main()
