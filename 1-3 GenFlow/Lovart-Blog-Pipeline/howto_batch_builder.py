"""Build How-To, Branding, and Insight article bodies."""

from __future__ import annotations

from .howto_batch_common import closing_blocks


def _para(*lines: str) -> str:
    return "\n\n".join(lines)


def build_howto_body(a: dict) -> str:
    topic = a["topic"]
    channel = a["channel"]
    specs = a["specs"]
    tool = a.get("tool", "ChatCanvas, Brand Kit, Touch Edit, Text Edit")
    steps = a["steps"]
    extra = a.get("extra_links", [])

    step_blocks = []
    for i, (title, detail, prompt) in enumerate(steps, 1):
        step_blocks.append(
            _para(
                f"### Step {i}: {title}",
                detail,
                f"> **Prompt on ChatCanvas:** {prompt}",
            )
        )
    steps_md = "\n\n".join(step_blocks)
    step_names = [s[0] for s in steps]

    body = _para(
        f"[IMAGE 1 PLACEHOLDER — Finished {channel} creative mockup with on-brand typography and clear CTA]",
        f"You opened {channel} analytics and the same problem appeared again: the asset that performed last month was a one-off. This week's post looks like a different company. {topic} is not a talent problem—it is a **systems** problem. Single-image generators optimize for one beautiful frame. Marketing teams need repeatable layouts, governed color, and copy-safe type at the exact dimensions {channel} expects.",
        f"Lovart's **AI Design Agent** on **ChatCanvas** treats {topic.lower()} as a production workflow: brief → **MCoT (Mind Chain of Thought)** planning → generation → semantic refinement → multi-format export. **Brand Kit** locks palette and typography so every variant looks like the same brand, not the same prompt lottery.",
        "---",
        f"## Why {topic} Breaks on Generic AI Tools",
        f"### Platform specs punish guesswork",
        specs,
        f"### Consistency beats novelty for performance",
        f"Algorithms reward recognition. When headline position, margin rhythm, and accent color drift between posts, completion rate drops—even if each image is individually pretty. The fix is not \"prompt harder.\" It is **design context**: one canvas, one Brand Kit, explicit slide or frame roles, and surgical edits via **Touch Edit** (click object, describe change) and **Text Edit** (fix type on-image) instead of full regenerations.",
        f"### Speed without governance creates brand debt",
        f"Marketing coordinators can publish ten variants by Friday—but legal, product, and leadership may each have a different \"approved\" version in email threads. Lovart centralizes iterations on **ChatCanvas** so the approved export is obvious. For foundational brand rules, start with the [Brand Kit guide for every industry](/blog/complete-guide-brand-kit-every-industry-lovart).",
        "---",
        f"## How Lovart Approaches {topic}",
        f"### Agentic planning before pixels",
        f"Enable **Thinking Mode** when the brief includes audience, offer, constraints, or compliance notes. Example: *\"{steps[0][2][:120]}...\"* The agent breaks deliverables into artboards or scenes, chooses aspect ratios, and sequences copy hierarchy—reducing the over-prompting trap described in our [over-prompting guide](/blog/over-prompting-trap-novel-length-prompts-confuse-generative-ai).",
        f"### Semantic last-mile editing",
        f"**Edit Elements** splits foreground, subject, and background when you need last-minute swaps—offer badges, product cutouts, or background replacements—without rebuilding the layout. Pair with **Identity Lock** when a product, mascot, or speaker must stay identical across sizes (see [Nano Banana consistent results](/blog/nano-banana-consistent-results-lovart-best-practice)).",
        f"### Tooling for this workflow",
        f"Primary tools: **{tool}**. Video cutdowns can use **Seedance 2.0** or **Veo 3** from the same canvas when motion is part of the campaign ([image to video](/blog/image-to-video-ai-static-designs-into-motion)).",
        "---",
        f"## Step-by-Step: {topic} on ChatCanvas",
        steps_md,
        "---",
        f"## Pro Tips and QA Checklist",
        f"### Squint-test legibility",
        f"Shrink the artboard to thumbnail size. If the headline disappears, increase contrast or reduce background noise—do not rely on platform auto-crop to save you.",
        f"### Version naming and rollback",
        f"Export `campaign-channel-vNN.png`. When a test wins, duplicate the artboard in ChatCanvas rather than overwriting—rollback is free.",
        f"### Batch from one brief",
        f"After the hero works, prompt: *\"Generate remaining sizes using the same Brand Kit and grid; preserve headline zone.\"* See [batch 30 days of social content](/blog/batch-generate-30-days-social-media-content-ai) for calendar-scale patterns.",
        f"### Common mistakes",
        f"- Mixing RGB exports with print vendors without bleed or CMYK conversation.\n- Regenerating entire layouts for one word change—use **Text Edit**.\n- Ignoring safe zones for UI overlays (link stickers, profile avatars, play buttons).\n- Publishing AI copy claims without human review where regulations apply.",
        "---",
        f"## Real-World {channel} Examples",
        f"### Example A: Product launch",
        f"**Brief:** New SKU, two-week {channel} push, English only. **Lovart flow:** Brand Kit → hero with Identity Lock on pack shot → three headline variants via Text Edit → export sizes from one canvas. **Why it works:** Variable isolation—only the offer line changes, so performance data stays interpretable.",
        f"### Example B: Evergreen education",
        f"**Brief:** Teach a concept without dated UI chrome. **Lovart flow:** Thinking Mode for slide roles → numbered steps with consistent icon style → PDF export for email capture. **Why it works:** Narrative structure prevents \"random tip\" carousels that drop off on slide two.",
        f"### Example C: Community or support",
        f"**Brief:** Policy update or event reminder. **Lovart flow:** High-contrast type, minimal photography, CTA button zone reserved. **Touch Edit** brightens background if contrast fails mobile squint test. **Why it works:** Clarity beats decoration for operational posts.",
        "---",
        "## Troubleshooting",
        "### Type looks blurry after export",
        "Regenerate at native width; avoid upscaling small exports. Prefer Nano Banana 2 for type-heavy layouts. Check that headline sits on flat or blurred regions—not busy texture.",
        "### Colors drift between variants",
        "Re-apply Brand Kit on the artboard before batching sizes. Remove descriptive color adjectives from prompts when hex codes exist in Brand Kit.",
        "### Stakeholder wants \"just one more version\"",
        "Duplicate artboard, label v2/v3, change only the approved variable. Do not fork projects across tools mid-campaign.",
        "### Video handoff from stills",
        "Export hero as PNG reference, then prompt Seedance or Veo with Identity Lock on subject. Keep lower-third safe zones consistent with still templates.",
    )

    derivative = a.get(
        "derivative",
        [
            f"Repurpose the hero {channel} asset to email header and web banner from the same Brand Kit.",
            f"Animate key frames with Seedance 2.0 for short-form video without a separate video tool.",
            f"Localize headlines with Text Edit for secondary markets.",
            f"Build a paid ads variant set at 1:1 and 9:16 using Identity Lock on the product.",
            f"Export a PDF proof sheet for stakeholder sign-off before publishing.",
        ],
    )
    faq = a.get(
        "faq",
        [
            (
                f"What size should I design {channel} assets in Lovart?",
                f"Design at native export dimensions noted in this guide ({specs.split('.')[0]}). Generate companion sizes from the same Brand Kit rather than resizing in a separate tool.",
            ),
            (
                "Can non-designers run this workflow?",
                "Yes. Conversational briefs plus Brand Kit reduce tool complexity. Start with one channel until QA rhythm is stable.",
            ),
            (
                "Which Lovart model works best for text-heavy layouts?",
                "Nano Banana 2 excels at sharp type and fast iteration; use Nano Banana Pro for photoreal subjects with Identity Lock.",
            ),
            (
                "How do I fix one element without redoing everything?",
                "Use Touch Edit for objects and Text Edit for type. Edit Elements helps when you need layer-like control without Photoshop.",
            ),
            (
                "Does Lovart replace my existing templates?",
                "Not necessarily. Many teams keep legacy templates for legal-approved shells and use Lovart for net-new campaigns and variant explosion.",
            ),
        ],
    )

    return body + closing_blocks(a["content_cluster"], derivative, faq, extra)


def build_longform_body(a: dict) -> str:
    """Branding / Insight articles (3000+ word target)."""
    title = a["title"]
    thesis = a["thesis"]
    sections = a["sections"]  # list of (h2, list of paragraphs)
    extra = a.get("extra_links", [])

    parts = [
        f"[IMAGE 1 PLACEHOLDER — Editorial visual supporting: {title}]",
        thesis,
        "---",
    ]
    for h2, paras in sections:
        parts.append(f"## {h2}\n\n" + _para(*paras))
        parts.append("---")

    parts.append(
        _para(
            "## What Practitioners Should Do Next",
            "Pick one workflow you ship weekly—ads, packaging, social, or deck headers—and rebuild it on **ChatCanvas** with **Brand Kit** locked. Measure time-to-approved-export, not time-to-first-image. Add motion only after stills are governed.",
            "For platform depth, see [how to chat and generate any design type](/blog/how-to-chat-generate-any-design-type-lovart-agent) and the [ChatCanvas getting started](/blog/05-pillar-getting-started-lovart) pillar.",
        )
    )

    derivative = a.get(
        "derivative",
        [
            "Turn insight into a team workshop: audit last month's creatives for consistency failures.",
            "Publish internal Brand Kit rules sourced from this article's principles.",
            "Pair static campaigns with motion tests using Seedance 2.0 cutdowns.",
            "Run a small A/B on headline zones with Text Edit instead of full redesigns.",
            "Document approved prompt patterns in a shared ChatCanvas project.",
        ],
    )
    faq = a.get(
        "faq",
        [
            (
                "Is Lovart only for designers?",
                "No. Lovart targets marketers, founders, and operators who need governed production without mastering Adobe stacks.",
            ),
            (
                "How does this relate to single-model tools?",
                "Lovart orchestrates models and editing semantics as a Design Agent—not a single generator UI.",
            ),
            (
                "Where should teams start?",
                "Brand Kit + one high-frequency deliverable. Expand to video and multi-channel after QA discipline exists.",
            ),
            (
                "What about legal and brand risk?",
                "Human review remains essential for regulated claims. Lovart accelerates iteration; accountability stays with your team.",
            ),
        ],
    )

    return "\n\n".join(parts) + closing_blocks(a["content_cluster"], derivative, faq, extra)
