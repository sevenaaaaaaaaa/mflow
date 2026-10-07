# noqa: D100
"""Fifteen Lovart 101 article definitions."""

from __future__ import annotations

from lib.lovart_101_common import faq_schema, howto_schema, pick_cover_url
from lib.lovart_101_content.builder import build_body
from lib.lovart_101_content.expand import bullets_to_paragraphs


def _subs(title_bullets: list[tuple[str, list[str], list[str]]]) -> list[tuple[str, list[str]]]:
    return [(t, bullets_to_paragraphs(b, c)) for t, b, c in title_bullets]


def _steps(step_data: list[tuple[str, list[str], list[str]]]) -> list[tuple[str, list[str]]]:
    return [(t, bullets_to_paragraphs(b, c)) for t, b, c in step_data]


def _spec(
    num: int,
    meta: dict,
    h1: str,
    hook: str,
    image1: str,
    p1_title: str,
    p1: list[tuple[str, list[str], list[str]]],
    p2_title: str,
    p2: list[tuple[str, list[str], list[str]]],
    p3_title: str,
    steps: list[tuple[str, list[str], list[str]]],
    cluster: str,
    derivative: list[str],
    faq: list[tuple[str, str]],
    step_names_for_schema: list[str],
    cover_override: str | None = None,
) -> dict:
    if cover_override:
        meta = {**meta, "cover_url": cover_override}
    body = build_body(
        h1,
        hook,
        image1,
        p1_title,
        _subs(p1),
        p2_title,
        _subs(p2),
        p3_title,
        _steps(steps),
        cluster,
        derivative,
        faq,
    )

    def structured() -> str:
        cover = meta.get("cover_url") or pick_cover_url(meta["slug"])
        if meta["seo_schema"] == "FAQ":
            return faq_schema(faq)
        return howto_schema(
            meta["seo_title"],
            meta["seo_description"],
            cover,
            meta["slug"],
            step_names_for_schema,
        )

    meta.setdefault("internal_note", f"Batch 3 101-{num} | Lovart 101 | auto-generated")
    return {
        "filename": f"lovart-101-{meta['slug']}.md",
        "meta": meta,
        "body_builder": lambda b=body: b,
        "structured": structured,
    }


# --- Shared bullet banks (unique per article via contexts) ---

CHATCANVAS = _spec(
    1,
    {
        "title": "Lovart ChatCanvas 101: The Complete Getting Started Guide",
        "slug": "lovart-chatcanvas-101-complete-getting-started-guide",
        "date": "2026-06-02",
        "tool": "ChatCanvas, Design Agent, Thinking Mode, Fast Mode, Brand Kit",
        "focus_keyword": "lovart tutorial getting started chatcanvas",
        "keywords": [
            "lovart tutorial getting started chatcanvas",
            "lovart chatcanvas guide",
            "ai design agent tutorial",
            "lovart workspace setup",
            "chatcanvas infinite canvas",
        ],
        "tags": ["lovart 101", "chatcanvas", "getting started", "tutorial"],
        "description": "Master Lovart ChatCanvas from first login to export: spatial workspace, Thinking vs Fast Mode, Brand Kit hooks, Touch Edit, and a repeatable getting-started workflow for teams.",
        "seo_title": "Lovart ChatCanvas 101: Complete Getting Started Guide",
        "seo_description": "Learn Lovart ChatCanvas step by step—workspace, modes, Brand Kit, and exports. Start free at lovart.ai/signup.",
        "seo_schema": "HowTo",
        "content_cluster": "Lovart 101 — Platform Foundations",
    },
    "Lovart ChatCanvas 101: The Complete Getting Started Guide",
    "You signed up for Lovart because a static image generator could not carry your campaign. "
    "Five minutes later you are staring at an infinite canvas, a chat thread, and a toolbar that "
    "expects you to think like a creative director—not a prompt gambler. **ChatCanvas** is "
    "Lovart's spatial collaboration surface: one place where the **Design Agent** plans, generates, "
    "edits, and exports without kicking you into separate apps.",
    "[IMAGE 1 PLACEHOLDER — Wide shot of Lovart ChatCanvas: infinite canvas with hero ad, product mockup, and video storyboard frames linked to a chat thread and Brand Kit panel]",
    "Part 1: Why ChatCanvas Exists (First Principles)",
    [
        (
            "The cost of scattered creative tools",
            [
                "Most teams still route a single campaign through four tabs: one for images, one for mockups, one for video, one for brand PDFs nobody opens",
                "Each handoff drops metadata—hex codes become screenshots, logo SVGs become flattened PNGs, and video briefs lose the product angle that marketing approved on Tuesday",
                "ChatCanvas collapses those handoffs into one persistent surface where assets stay spatially related to the conversation that produced them",
                "When feedback arrives ('move the headline, warm the background, export 4:5'), contributors edit in context instead of re-uploading files into a new thread",
            ],
            [
                "Creative ops leaders describe this as 'folder archaeology'—searching Slack for the approved green instead of editing the approved file",
                "Spatial layout mirrors how art directors pin references on a wall: relationships between hero, cutdown, and mockup remain visible",
                "That visibility reduces duplicate work when a founder asks for 'the same vibe as last launch' without naming files",
            ],
        ),
        (
            "Chat vs canvas: two lenses, one brain",
            [
                "Traditional AI art tools treat chat as a log and the gallery as a graveyard of one-off thumbnails",
                "Lovart binds chat to canvas nodes so the Design Agent can reference what you already approved when generating the next format",
                "You can branch explorations—version A and version B side by side—without losing the reasoning trail in the thread",
                "Thinking Mode exposes intermediate reasoning; Fast Mode skips visible planning when you already know the exact output spec",
            ],
            [
                "Product teams compare this to Figma comments attached to frames—except the commenter can also render, relight, and re-export",
                "Agencies use branches for client rounds: three directions on canvas, one thread documenting decisions",
            ],
        ),
        (
            "Who ChatCanvas is built for",
            [
                "Solo founders shipping launch creative without a retained studio",
                "Marketing teams producing weekly paid social without a full-time designer",
                "Agencies running parallel client boards with strict brand separation",
                "Creators who need stills, shorts, and thumbnails that share the same identity lock",
            ],
            [
                "Education customers start in ChatCanvas even when they later adopt advanced Edit Elements workflows",
                "Enterprise pilots often begin with one Brand Kit and one canvas per business unit before expanding seats",
            ],
        ),
        (
            "Onboarding mistakes to avoid in week one",
            [
                "Generating hero art before Brand Kit exists—fixes drift later at 3× credit cost",
                "Treating ChatCanvas like a single-image Discord bot instead of a campaign surface",
                "Exporting without naming conventions, then losing which prompt produced winners",
                "Skipping Thinking Mode on regulated categories because Fast Mode feels faster",
            ],
            [
                "Week-one discipline determines whether Lovart feels magical or like another random generator",
            ],
        ),
    ],
    "Part 2: ChatCanvas Architecture You Should Understand",
    [
        (
            "Infinite canvas mechanics",
            [
                "Pan and zoom across a boundless plane—frames are not trapped in a single artboard size",
                "Group related outputs: PDP stills left, paid social center, motion storyboard right",
                "Link exports back to the generating prompt so you can iterate without reconstructing the brief from memory",
            ],
            [
                "Operators running Black Friday sprints pin performance winners next to challengers to see what Brand Kit enforced consistently",
                "Interior mockup clients keep material swatches on-canvas while hero renders update live",
            ],
        ),
        (
            "Design Agent + MCoT on canvas",
            [
                "Every substantial request passes through **MCoT (Mind Chain of Thought)**—the agent decomposes goals, checks conflicts, then routes models",
                "You see planning in Thinking Mode; Fast Mode keeps the same routing with less visible narration",
                "Model routing might send type-heavy work to **Nano Banana 2** and photoreal packs to **Nano Banana Pro** without you micromanaging endpoints",
            ],
            [
                "This is the difference between typing 'make it pop' into a black box and briefing a collaborator who asks clarifying questions once",
                "See also the dedicated [MCoT 101](/blog/mcot-101-lovart-mind-chain-of-thought) walkthrough when you want reasoning internals",
            ],
        ),
        (
            "Editing layer on top of generation",
            [
                "**Touch Edit** targets objects semantically—click the bottle, describe the label change",
                "**Text Edit** fixes on-image type without rerolling the entire scene",
                "**Edit Elements** splits layers when you need Photoshop-like control without leaving canvas",
                "**Smart Mockups** wrap products with perspective-aware lighting for shelf-ready shots",
            ],
            [
                "Post-generation editing is why ChatCanvas behaves like a design environment—not a slot machine",
                "Teams migrating from Canva templates often adopt Touch Edit first, then Brand Kit for scale",
            ],
        ),
        (
            "Credits, plans, and commercial use",
            [
                "Free tiers are ideal for portfolio exploration; paid tiers unlock commercial rights for client work",
                "Thinking Mode and video exports consume more credits than a single Fast Mode still",
                "Upscale and batch variant runs should be budgeted like media spend, not ignored until invoice day",
                "Compare seats and credit bundles on Lovart pricing before committing a whole team",
            ],
            [
                "Finance leads appreciate when creative ops maps one approved hero to twelve formats instead of twelve unrelated gens",
            ],
        ),
    ],
    "Part 3: Getting Started on ChatCanvas (Numbered Workflow)",
    [
        (
            "Create your workspace and first project",
            [
                "Sign up at lovart.ai/signup and confirm you are on the plan that matches commercial needs—paid tiers unlock full commercial rights",
                "Open a new ChatCanvas project and name it after the campaign or client so history stays searchable",
                "Skim the default toolbar: generation, edit modes, upscale, export, and model selectors live here—not buried in settings",
            ],
            [
                "Invite collaborators if your plan includes seats; agencies often use one canvas per client to avoid cross-brand leakage",
            ],
        ),
        (
            "Configure Brand Kit before the first hero",
            [
                "Upload logo SVG or PNG, primary and secondary palettes, and two to three reference boards that express tone—not just logos",
                "Set typography preferences if available; if not, state type rules in the first brief ('headlines: geometric sans, body: humanist')",
                "Run a micro-test: generate a simple social tile and confirm colors match kit—not 'close enough' green",
            ],
            [
                "Follow [Brand Kit setup in five minutes](/blog/brand-kit-setup-5-minutes-lovart-best-practice) if you want a checklist",
            ],
        ),
        (
            "Write briefs the Design Agent can execute",
            [
                "Lead with outcome and channel: 'Meta static ad, 4:5, product hero, promo code readable at mobile size'",
                "Specify constraints: legal disclaimers, forbidden colors, mandatory logo placement",
                "Attach references on-canvas; the agent weights visual anchors higher than adjectives like 'premium'",
            ],
            [
                "Avoid novel-length prompts—see [over-prompting trap](/blog/over-prompting-trap-novel-length-prompts-confuse-generative-ai) for why brevity with structure wins",
            ],
        ),
        (
            "Generate, branch, and compare",
            [
                "Start in Thinking Mode for new categories; switch to Fast Mode when repeating a proven layout with new copy",
                "Place variants side by side; star or annotate winners in-chat so the thread documents approval",
                "Use Identity Lock when a character or SKU must remain identical across formats",
            ],
            [
                "Nano Banana family details live in the [Nano Banana complete guide](/blog/nano-banana-ai-complete-guide-lovart-image-model)",
            ],
        ),
        (
            "Edit semantically, then export",
            [
                "Touch Edit packaging claims before legal review instead of rerolling entire scenes",
                "Text Edit fixes sale percentages on-image when commerce updates pricing hourly",
                "Export PNG for paid social, SVG when you need vector logos, MP4 for motion cuts—Upscale when print or OOH requires 4K+",
            ],
            [
                "Compare [raster vs vector guidance](/blog/raster-png-vs-vector-svg-when-to-use-which) before handing files to print vendors",
            ],
        ),
        (
            "Document and reuse",
            [
                "Save successful prompts as snippets in the thread—not external docs that drift",
                "Duplicate the canvas for next week's drop; Brand Kit carries forward automatically",
                "Schedule a monthly kit review when seasonal palettes shift",
            ],
            [
                "Teams publishing daily social pair ChatCanvas with [batch social generation](/blog/batch-generate-30-days-social-media-content-ai) playbooks",
            ],
        ),
        (
            "Collaborate without brand bleed",
            [
                "Invite reviewers with view or comment permissions according to your plan",
                "Keep client canvases separate; never share one Brand Kit across competing accounts",
                "Use in-thread approvals so media buyers inherit context, not just files",
                "Archive completed canvases instead of deleting—history becomes your playbook",
            ],
            [
                "Agencies document why a direction won directly on the canvas node that exported",
            ],
        ),
    ],
    "Lovart 101 — Platform Foundations",
    [
        "Launch a DTC drop: hero PDP, three ads, and a 9:16 storyboard on one canvas with one Brand Kit",
        "Agency pitch boards: three visual territories for the same brief without duplicating threads",
        "Event marketing: poster, slide cover, and wayfinding icons sharing typography rules",
        "Creator launch: thumbnail, channel banner, and merch mockup with Identity Lock on the mascot",
        "Rebrand migration: old vs new logo applications side by side for stakeholder sign-off",
    ],
    [
        (
            "Is ChatCanvas the same as Lovart?",
            "ChatCanvas is the workspace surface; Lovart is the platform including the Design Agent, models, Brand Kit, and exports. You always create on ChatCanvas when producing inside Lovart.",
        ),
        (
            "Do I need design software experience?",
            "No—briefs in plain language work. Design literacy helps for typography and hierarchy, but Touch Edit and Text Edit reduce traditional tool learning curves.",
        ),
        (
            "Thinking Mode vs Fast Mode—which default?",
            "Use Thinking Mode for new products, categories, or legal-sensitive layouts. Use Fast Mode when repeating proven formats with new copy or SKUs.",
        ),
        (
            "Can teams share one canvas?",
            "Yes on plans with collaboration. Agencies typically separate canvases per client to keep Brand Kit and assets isolated.",
        ),
        (
            "What file types export from ChatCanvas?",
            "PNG, JPG, SVG, PSD, PDF, and MP4 depending on asset type; Upscale supports high-resolution stills for print.",
        ),
        (
            "Where do credits go?",
            "Complex video, upscale, and multi-step Thinking Mode runs consume more credits than a single Fast Mode still. Monitor usage on [Lovart pricing](https://lovart.ai/pricing).",
        ),
    ],
    [
        "Create workspace and first ChatCanvas project",
        "Configure Brand Kit and run color verification",
        "Write structured channel-specific briefs",
        "Generate variants in Thinking or Fast Mode",
        "Apply Touch Edit, Text Edit, and export deliverables",
        "Document prompts and duplicate canvas for reuse",
    ],
)

# Additional articles 2-15: compact definitions with rich unique bullets

def _mk(
    num: int,
    slug: str,
    title: str,
    focus: str,
    tool: str,
    desc: str,
    seo_title: str,
    seo_desc: str,
    h1: str,
    hook: str,
    img: str,
    p1t: str,
    p1: list,
    p2t: str,
    p2: list,
    p3t: str,
    steps: list,
    cluster: str,
    deriv: list,
    faq: list,
    schema_steps: list,
    schema: str = "HowTo",
    cover_override: str | None = None,
):
    meta = {
        "title": title,
        "slug": slug,
        "date": "2026-06-02",
        "tool": tool,
        "focus_keyword": focus,
        "keywords": [focus, "lovart 101", "ai design agent", "chatcanvas", slug.split("-")[0]],
        "tags": ["lovart 101", slug.split("-")[0], "tutorial"],
        "description": desc,
        "seo_title": seo_title,
        "seo_description": seo_desc,
        "seo_schema": schema,
        "content_cluster": cluster,
    }
    return _spec(num, meta, h1, hook, img, p1t, p1, p2t, p2, p3t, steps, cluster, deriv, faq, schema_steps, cover_override)


MCOT = _mk(
    2,
    "mcot-101-lovart-mind-chain-of-thought",
    "MCoT 101: How Lovart's Mind Chain of Thought Engine Thinks Before It Designs",
    "mcot engine lovart ai design reasoning",
    "MCoT, Thinking Mode, ChatCanvas, Design Agent",
    "Understand Lovart MCoT: decomposition, conflict detection, model routing, and how Thinking Mode turns reasoning into better images, video, and brand-safe layouts.",
    "MCoT 101: Lovart Mind Chain of Thought",
    "See how Lovart MCoT plans before pixels—decomposition, routing, and Thinking Mode. Try it free at lovart.ai/signup.",
    "MCoT 101: How Lovart's Mind Chain of Thought Engine Thinks Before It Designs",
    "You typed a perfect prompt. The image came back with two left hands, a misspelled headline, and lighting that contradicts the product photo you attached. "
    "The model did not 'fail creativity'—it skipped planning. **MCoT (Mind Chain of Thought)** is Lovart's reasoning layer that sits between your brief and every generator on **ChatCanvas**.",
    "[IMAGE 1 PLACEHOLDER — Diagram: user brief flowing through MCoT blocks (decompose, detect conflicts, route model) into Nano Banana, Seedream, Seedance outputs]",
    "Part 1: Why Reasoning Belongs Before Rendering",
    [
        (
            "Prompts are briefs, not spells",
            [
                "A prompt without structure forces the model to guess audience, medium, and legal constraints simultaneously",
                "Professional creative briefs separate objective, audience, mandatories, and references—MCoT automates that separation at machine speed",
                "Skipping decomposition is why 'minimal luxury skincare ad' returns chrome gradients one run and rustic wood the next",
                "Novel-length prompts confuse decomposition—structure beats volume",
                "References on canvas outweigh adjectives like 'premium' or 'playful' in MCoT weighting",
            ],
            ["Brand strategists already think in brief sections; MCoT encodes that habit for non-designers"],
        ),
        (
            "The hallucination tax",
            [
                "Every unplanned generation spends credits and attention; rework doubles calendar time",
                "Agencies call this the hallucination tax—pretty wrong outputs that still invoice hours",
                "Reasoning upfront reduces rerolls because conflicts surface before diffusion starts",
                "Client trust erodes when the third 'final final' still has the wrong offer code",
                "Operations teams should measure cost per approved asset, not cost per click on Generate",
            ],
            ["Finance teams track credits like media spend; MCoT is a cost-control layer, not a gimmick"],
        ),
        (
            "Reasoning vs raw speed",
            [
                "Fast Mode is not 'dumber'—it skips visible narration when the brief is already structured",
                "Thinking Mode is insurance on new categories, regulated claims, and multi-product compositions",
                "Teams that default to Fast Mode on day one often blame the model instead of the missing kit",
            ],
            ["Train contributors when to toggle modes; do not treat them as quality sliders only"],
        ),
    ],
    "Part 2: Inside the MCoT Pipeline",
    [
        (
            "Where MCoT shows up in the UI",
            [
                "Thinking Mode surfaces intermediate plans you can correct before spend",
                "Fast Mode still routes models but narrates less—ideal for repeating winning structures",
                "Failed outputs should be diagnosed against the plan, not only the final raster",
            ],
            ["Training contributors to read plans reduces 'random seed' superstition"],
        ),
        (
            "Decomposition",
            [
                "MCoT splits requests into sub-tasks: subject, environment, typography, camera, brand constraints",
                "Each sub-task gets success criteria—readable type at mobile scale, logo clear space, etc.",
            ],
            ["Ecommerce teams see decomposition separate product truth from lifestyle styling automatically"],
        ),
        (
            "Conflict detection",
            [
                "Contradictions ('minimal baroque', 'photoreal cartoon') trigger clarifications or safe defaults",
                "Conflicts between Brand Kit rules and ad-hoc prompts favor kit when enforcement is on",
            ],
            ["Legal prefers early flags on unsubstantiated claims before pixels exist"],
        ),
        (
            "Model routing",
            [
                "Type-heavy posters route toward **Nano Banana 2**; photoreal packs toward **Nano Banana Pro**",
                "Motion requests evaluate **Seedance 2.0**, **Veo 3**, or **Kling** based on style and sync needs",
                "Complex layouts with dense copy may route toward **Seedream** family models",
                "Routing logs help engineers explain why a still and a video in one campaign used different backends",
            ],
            ["Routing is why Lovart is inference-agnostic without making users maintain a spreadsheet of endpoints"],
        ),
        (
            "Brand Kit injection",
            [
                "Kit colors become hard constraints in sub-tasks unless you explicitly override with seasonal variants",
                "Typography rules attach to headline sub-tasks separate from body copy sub-tasks",
                "Identity Lock references propagate to character and product sub-tasks across stills and motion",
            ],
            ["When kit and prompt fight, fix the kit—ad-hoc prompts do not scale"],
        ),
    ],
    "Part 3: Working With MCoT in Production",
    [
        (
            "Enable Thinking Mode for discovery",
            [
                "Open ChatCanvas, toggle Thinking Mode, submit a structured brief with channel and mandatories",
                "Read the plan; correct misconceptions in-chat before approving generation",
                "Approve or edit sub-tasks individually when the UI exposes them",
                "Screenshot the approved plan in the thread so media and legal can align before spend",
            ],
            ["Discovery projects benefit from visible reasoning trails for stakeholder education"],
        ),
        (
            "Switch to Fast Mode for repetition",
            ["Once a layout wins, duplicate the canvas and run Fast Mode with swapped copy or SKUs", "Keep Brand Kit locked so routing still respects palette and type", "Log which sub-tasks changed—usually headline and CTA only"],
            ["Performance marketing teams live in Fast Mode during weekly creative refreshes"],
        ),
        (
            "Audit failures systematically",
            ["When output fails, screenshot the plan step that went wrong—not only the final raster", "Adjust Brand Kit or references before rewriting adjectives", "Escalate to Edit Elements if the plan was right but execution drifted on one layer"],
            ["Postmortems become actionable instead of 'try another random seed'"],
        ),
        (
            "Teach stakeholders to read plans",
            ["Export Thinking Mode summaries for legal and brand reviewers", "Highlight which sub-tasks carry mandatories like disclaimers and logo placement", "Celebrate catches before render as savings, not slowdowns"],
            ["Stakeholder education reduces last-minute rerolls after approval"],
        ),
        (
            "Instrument routing decisions",
            [
                "Note which model produced winners in the thread for repeat campaigns",
                "When typography fails, check whether Nano Banana 2 was routed for type-heavy sub-tasks",
                "When motion drifts, compare Seedance versus Veo plans before blaming the brief",
                "Share routing notes with new hires so they inherit taste, not superstition",
            ],
            ["Routing literacy separates power users from frustrated beginners"],
        ),
    ],
    "Lovart 101 — Platform Foundations",
    [
        "Regulated claims: MCoT flags superlatives before rendering supplement ads",
        "Character-driven serial ads: Identity Lock plus decomposition keeps wardrobe changes separate from face identity",
        "Multilingual posters: typography sub-task routes to models strong at glyph rendering",
        "Video pre-viz: motion sub-tasks storyboard shots before spending video credits",
    ],
    [
        ("What does MCoT stand for?", "Mind Chain of Thought—Lovart's proprietary reasoning engine before generation."),
        ("Is MCoT only in Thinking Mode?", "Thinking Mode shows more of the chain; Fast Mode still uses routing and checks with less narration."),
        ("Can I bypass MCoT?", "You cannot disable safety and routing entirely—doing so would recreate generic generator chaos."),
        ("Does MCoT cost extra credits?", "Visible planning may add steps; it usually saves net credits by reducing failed generations."),
        ("How does MCoT relate to Brand Kit?", "Brand Kit constraints inject into decomposition so sub-tasks inherit palette, type, and references."),
        (
            "How do I learn MCoT without engineering docs?",
            "Run real briefs in Thinking Mode, read plans before approving, and compare failures to sub-tasks. Pair with ChatCanvas 101 and Brand Kit setup guides linked in this article.",
        ),
    ],
    ["Enable Thinking Mode and submit a structured brief", "Review decomposition and resolve conflicts", "Approve generation with routed models", "Iterate in Fast Mode for variants", "Audit failures against plan steps"],
)

# Due to length, articles 3-15 use dense subsection templates
REST = []

_b = lambda t, bl, ctx: (t, bl, ctx)

def _article3():
    p1 = [
        _b("Brand systems fail at scale without memory", [
            "Style guides become PDF graveyards while social teams improvise hex codes in Canva",
            "Freelancers inherit outdated logos from Google Drive links labeled 'FINAL_v7'",
            "Without persistent rules, each campaign whispers a slightly different brand personality",
        ], ["Brand Kit is Lovart's answer: rules the Design Agent consults every session"]),
        _b("What Brand Kit stores", [
            "Palette with roles—primary, secondary, accent, neutrals—not just swatches",
            "Typography families, weights, and hierarchy notes for headlines vs body",
            "Logo variants, clear space, and misuse examples when you upload references",
            "Character or product Identity Lock references for serial storytelling",
        ], ["The Design Context Core propagates these fields into MCoT decomposition"]),
    ]
    p2 = [
        _b("Governance without bottlenecks", [
            "Brand owners approve kit changes; contributors cannot silently drift palette",
            "Seasonal campaigns get temporary accent colors as kit variants, not one-off prompts",
            "Agencies clone kits per client instead of remixing the same defaults",
        ], ["Governance pairs with ChatCanvas permissions on team plans"]),
        _b("Scaling outputs", [
            "One kit powers PDP, paid social, OOH, and motion when models route correctly",
            "Smart Mockups read kit lighting preferences for consistent shelf photography",
            "Batch workflows import SKU lists while kit enforces brand",
        ], ["See [complete Brand Kit guide](/blog/complete-guide-brand-kit-every-industry-lovart) for industry patterns"]),
    ]
    steps = [
        _b("Audit existing brand assets", ["Collect SVG logos, official hex values, type licenses, and three campaign references that feel on-brand", "Reject moodboards that contradict sold products—kit should reflect reality", "Document mandatory legal lines and logo placements"], []),
        _b("Create kit in Lovart", ["Open Brand Kit from ChatCanvas, name by business unit or client", "Enter colors with roles; upload references per role", "Set typography and upload Identity Lock anchors for mascots or spokespeople"], []),
        _b("Validate with torture tests", ["Generate ads with promo codes, long headlines, and small logos", "Test dark-mode social backgrounds and print-oriented whites", "Touch Edit failures indicate kit gaps, not model randomness"], []),
        _b("Roll out to contributors", ["Publish a one-page 'how we brief' doc linking to [five-minute setup](/blog/brand-kit-setup-5-minutes-lovart-best-practice)", "Duplicate canvas templates with kit locked", "Review monthly for seasonal updates"], []),
        _b("Maintain and version kits", ["Archive retired palettes instead of deleting history", "Document kit version in export filenames for compliance trails", "Run quarterly audits comparing live ads to kit rules"], []),
    ]
    p1.append(_b("When PDF guides fail", [
        "PDFs cannot stop a tired contractor from using last year's neon accent",
        "Version control on PDFs is human-dependent; kits enforce at generation time",
        "Global teams need machine-readable rules, not 80-page decks nobody scrolls",
        "Stakeholder decks rarely include negative space rules for social safe zones",
        "Retail partners enforce their own photography standards—kits encode your side of the contract",
    ], ["Brand Kit is the operational layer; PDFs remain useful for narrative and storytelling"]))
    p1.append(_b("First principles for kit design", [
        "Assign color roles, not just swatches—primary, secondary, accent, neutral",
        "Typography hierarchy matters more than font enthusiasm",
        "Identity Lock references beat verbal descriptions of mascots and founders",
        "Seasonal accents should be variants, not rogue prompts",
    ], ["Principles align with the ChatCanvas 101 workflow for briefing and export"]))
    p2.append(_b("Failure modes to eliminate", [
        "Duplicating kits per contributor instead of per brand—creates drift",
        "Uploading low-res logos—forces the model to invent edges",
        "Skipping torture tests on promo codes and disclaimers",
        "Deleting retired palettes instead of archiving—loses audit trails",
    ], ["Cross-read [common prompting mistakes](/blog/common-ai-prompting-mistakes-design-results-how-to-fix) when outputs feel random"]))
    steps.extend([
        _b("Cross-train teams", [
            "Run a 30-minute lab: brief, generate, Touch Edit a logo clear-space issue",
            "Publish three approved prompt snippets per channel in your wiki",
            "Pair marketers and designers on one canvas to align vocabulary",
        ], []),
        _b("Launch and retrospective", [
            "Export with kit version in filenames for compliance",
            "Log performance feedback beside winning canvas nodes",
            "Schedule kit updates when campaigns reveal gaps",
        ], []),
    ])
    return _mk(3, "brand-kit-101-visual-systems-scale", "Lovart Brand Kit 101: Building Visual Systems That Scale",
        "lovart brand kit tutorial visual systems", "Brand Kit, Design Context Core, ChatCanvas, Identity Lock",
        "Build a Lovart Brand Kit that scales: palette roles, typography, Identity Lock, governance, and validation workflows for teams and agencies.",
        "Brand Kit 101: Visual Systems That Scale", "Lovart Brand Kit 101—scale colors, type, and identity across ChatCanvas. Start at lovart.ai/signup.",
        "Lovart Brand Kit 101: Building Visual Systems That Scale",
        "Your brand guidelines are beautiful. Your Instagram grid is chaos. The gap is not 'more discipline'—it is **memory**. **Brand Kit** gives Lovart's Design Agent persistent rules so every generation on **ChatCanvas** inherits the same visual contract.",
        "[IMAGE 1 PLACEHOLDER — Brand Kit panel beside canvas ads showing synchronized palette and typography]",
        "Part 1: Why Visual Systems Collapse", p1, "Part 2: Brand Kit as Infrastructure", p2,
        "Part 3: Build and Scale Your Kit", steps, "Lovart 101 — Brand Systems",
        ["Rebrand: kit v1 vs v2 canvases for leadership sign-off", "Franchisee marketing: locked kit with local copy fields", "Marketplace sellers: kit per sub-brand on one Lovart account", "Beauty line extensions: accent colors as kit variants", "Nonprofit chapters: shared kit, localized photography references"],
        [("How is Brand Kit different from a PDF guide?", "Kit is machine-enforced; PDFs rely on human memory."), ("Can I run multiple kits?", "Yes—typical for agencies and multi-brand portfolios."), ("Does Brand Kit affect video?", "Yes—motion outputs inherit palette and identity constraints when configured."), ("What if my logo is wrong in generations?", "Upload vector SVG, specify clear space in brief, and verify Touch Edit on logo layer."), ("Do free plans include Brand Kit?", "Check current [pricing](https://lovart.ai/pricing) for kit limits on free vs paid tiers.")],
        ["Audit brand assets", "Create Brand Kit with roles", "Run torture-test generations", "Roll out contributor brief standards"],
    )

# Generate articles 4-15 programmatically with topic-specific outlines
TOPICS = [
    (4, "edit-elements-101-semantic-layer-decomposition", "Edit Elements 101: Semantic Layer Decomposition Explained",
     "edit elements lovart layer decomposition", "Edit Elements, Touch Edit, Text Edit, ChatCanvas",
     "Master Lovart Edit Elements: semantic layer decomposition, when to split layers, and post-generation workflows faster than rerolling.",
     "Edit Elements 101: Semantic Layer Decomposition", "Edit Elements 101—decompose AI images into editable layers on Lovart. Try lovart.ai/signup.",
     "Edit Elements 101: Semantic Layer Decomposition Explained",
     "Photoshop trained you to think in layers. Generative AI trained you to think in prayers. **Edit Elements** restores layer logic by decomposing AI images into semantic objects you can adjust without destroying the whole scene.",
     "[IMAGE 1 PLACEHOLDER — Edit Elements panel showing separated product, shadow, background, and text layers on ChatCanvas]",
     "semantic editing", "layers vs reroll"),
    (5, "ai-design-ecommerce-101-product-images", "AI Design for E-Commerce 101: Product Images That Sell",
     "ai ecommerce design 101 product images", "ChatCanvas, Brand Kit, Smart Mockups, Nano Banana Pro, Touch Edit",
     "E-commerce AI design 101 on Lovart: PDP heroes, gallery consistency, colorways, Smart Mockups, and conversion-focused workflows.",
     "E-Commerce AI Design 101: Product Images", "Sell more with Lovart e-commerce AI design—PDP, mockups, colorways. Start at lovart.ai/signup.",
     "AI Design for E-Commerce 101: Product Images That Sell",
     "Shoppers do not buy prompts—they buy trust. Blurry specs, inconsistent colorways, and illegible promo codes erode conversion before copy ever gets read. Lovart treats ecommerce imagery as a system: **ChatCanvas** for production, **Brand Kit** for truth, **Smart Mockups** for shelf context.",
     "[IMAGE 1 PLACEHOLDER — PDP grid, colorway row, and Smart Mockup bottle on one ecommerce canvas]",
     "ecommerce conversion", "PDP trust"),
    (6, "ai-social-media-design-101-content-scale", "AI Social Media Design 101: Visual Content Creation at Scale",
     "ai social media design 101 content scale", "ChatCanvas, Brand Kit, batch workflows, Nano Banana 2",
     "Scale social visuals with Lovart: format matrices, Brand Kit governance, batch generation, and platform-native design on ChatCanvas.",
     "Social Media AI Design 101: Scale Content", "Scale social creatives with Lovart AI design 101—formats, batches, Brand Kit. lovart.ai/signup.",
     "AI Social Media Design 101: Visual Content Creation at Scale",
     "Your content calendar demands forty assets. Your team has Tuesday afternoon. Scaling social is not 'smaller templates'—it is **matrix thinking**: formats × messages × channels, governed by one **Brand Kit** on **ChatCanvas**.",
     "[IMAGE 1 PLACEHOLDER — 3x3 grid of social formats tied to one Brand Kit on ChatCanvas]",
     "social scale", "format matrix"),
    (7, "ai-brand-identity-101-logo-to-visual-system", "AI Brand Identity 101: From Logo to Full Visual System",
     "ai brand identity 101 visual system", "Brand Kit, ChatCanvas, Nano Banana Pro, Identity Lock",
     "Build brand identity with Lovart: logo exploration, visual system rules, Brand Kit, and launch assets from one agentic workflow.",
     "AI Brand Identity 101: Logo to System", "From logo to full visual system with Lovart Brand Kit and ChatCanvas—lovart.ai/signup.",
     "AI Brand Identity 101: From Logo to Full Visual System",
     "A logo without a system is a tattoo without a body. Brand identity work spans strategy, vocabulary, color, type, motion, and applications—too wide for a single prompt. Lovart connects exploratory **ChatCanvas** boards to durable **Brand Kit** memory.",
     "[IMAGE 1 PLACEHOLDER — Logo explorations evolving into business card, social, and OOH mockups]",
     "brand identity", "visual system"),
    (8, "ai-print-design-101-business-cards-billboards", "AI Print Design 101: Business Cards to Billboards",
     "ai print design 101", "ChatCanvas, Upscale, Brand Kit, export PDF",
     "Print-ready AI design on Lovart: bleed, DPI, CMYK-minded exports, large-format upscaling, and Brand Kit consistency from cards to billboards.",
     "AI Print Design 101: Cards to Billboards", "Print-ready AI design 101 on Lovart—bleed, upscale, exports. lovart.ai/signup.",
     "AI Print Design 101: Business Cards to Billboards",
     "Print punishes guesswork. RGB glow that looked great on screen dies on a business card. Lovart bridges screen generation with **Upscale**, vector exports, and **Brand Kit** discipline so a billboard whispers the same brand as your card.",
     "[IMAGE 1 PLACEHOLDER — Business card, flyer, and billboard mockups with bleed guides]",
     "print production", "bleed and DPI"),
    (9, "ai-packaging-design-101-concept-shelf-ready", "AI Packaging Design 101: From Concept to Shelf-Ready",
     "ai packaging design 101", "Smart Mockups, Brand Kit, Edit Elements, Nano Banana Pro",
     "Packaging design 101 with Lovart: dielines, shelf-ready mockups, regulatory copy edits, and Brand Kit consistency from concept to production handoff.",
     "AI Packaging Design 101: Shelf-Ready", "Packaging AI 101 on Lovart—mockups, edits, Brand Kit. lovart.ai/signup.",
     "AI Packaging Design 101: From Concept to Shelf-Ready",
     "Packaging is industrial design wearing marketing makeup. Structure, regulations, photography, and shelf context must align. Lovart combines generation with **Smart Mockups** and **Edit Elements** so you iterate claims before the factory phone rings.",
     "[IMAGE 1 PLACEHOLDER — Flat dieline, 3D mockup, and retail shelf scene on canvas]",
     "packaging", "shelf-ready"),
    (10, "ai-video-creation-101-text-to-motion", "AI Video Creation 101: Text to Motion — The Complete Beginner's Guide",
     "ai video creation 101 text to motion", "Seedance 2.0, Veo 3, Kling, ChatCanvas, Brand Kit",
     "AI video 101 on Lovart: storyboards on ChatCanvas, model choice (Seedance, Veo, Kling), brand consistency, and export for ads and social.",
     "AI Video Creation 101: Text to Motion", "Learn AI video on Lovart—Seedance, Veo 3, storyboards. lovart.ai/signup.",
     "AI Video Creation 101: Text to Motion — The Complete Beginner's Guide",
     "Still images got you meetings. Motion gets you budgets. Text-to-video is not one button—it is directing time: pacing, camera, audio sync, and brand persistence across shots. Lovart routes motion through integrated models while **ChatCanvas** keeps storyboards adjacent to stills.",
     "[IMAGE 1 PLACEHOLDER — Storyboard frames linked to MP4 export and waveform strip]",
     "motion design", "video models"),
    (11, "ai-design-non-designers-101-getting-started", "AI Design for Non-Designers 101: Everything You Need to Start",
     "ai design for non designers getting started", "ChatCanvas, Touch Edit, Brand Kit, Thinking Mode",
     "Non-designer's guide to Lovart: plain-language briefs, ChatCanvas basics, Touch Edit fixes, and confidence without Adobe certifications.",
     "AI Design for Non-Designers 101", "Start AI design without design school—Lovart 101 for beginners. lovart.ai/signup.",
     "AI Design for Non-Designers 101: Everything You Need to Start",
     "You do not need to know Bézier curves to ship credible creative. You need vocabulary for goals, constraints, and feedback. Lovart's **Design Agent** on **ChatCanvas** translates plain language into production—with **Touch Edit** when words almost work.",
     "[IMAGE 1 PLACEHOLDER — Non-designer user fixing headline with Text Edit on a social tile]",
     "beginner creative", "plain language"),
    (12, "ai-design-marketers-101-no-design-team", "AI Design for Marketers 101: Visuals Without a Design Team",
     "ai design for marketers no design team", "ChatCanvas, Brand Kit, batch workflows, Fast Mode",
     "Marketer's Lovart 101: campaign briefs, ad matrices, Brand Kit governance, and Fast Mode production without hiring a studio.",
     "AI Design for Marketers 101", "Ship campaign visuals without a design team—Lovart for marketers. lovart.ai/signup.",
     "AI Design for Marketers 101: Visuals Without a Design Team",
     "Marketing owns outcomes; design owns craft. When headcount is frozen, that split collapses on you. Lovart gives marketers an agentic studio—**ChatCanvas** for production, **Brand Kit** for guardrails, **Fast Mode** for weekly refreshes.",
     "[IMAGE 1 PLACEHOLDER — Marketer building Meta ad matrix from spreadsheet brief on ChatCanvas]",
     "marketing ops", "campaign velocity"),
    (13, "ai-design-small-business-101-professional-branding", "AI Design for Small Business 101: Professional Branding on a Budget",
     "ai design small business professional branding", "Brand Kit, ChatCanvas, Smart Mockups",
     "Small business AI design 101: credible branding, local marketing assets, and Lovart workflows that replace piecemeal freelancers.",
     "Small Business AI Design 101", "Professional branding on a budget with Lovart—101 guide. lovart.ai/signup.",
     "AI Design for Small Business 101: Professional Branding on a Budget",
     "Customers forgive small shops—they do not forgive sloppy trust signals. Professional branding used to mean agency retainers. Lovart compresses logo, menu, social, and signage into one **Brand Kit**-backed **ChatCanvas** workflow priced for local business reality.",
     "[IMAGE 1 PLACEHOLDER — Local café menu, storefront hours poster, and Instagram promo sharing one Brand Kit]",
     "local business", "budget branding"),
    (14, "ai-design-content-creators-101-idea-to-published", "AI Design for Content Creators 101: From Idea to Published",
     "ai design content creators 101", "ChatCanvas, Identity Lock, Nano Banana 2, video models",
     "Creator's Lovart 101: thumbnails, channel art, serial identity, shorts, and publishing pipelines from idea to posted content.",
     "AI Design for Content Creators 101", "From idea to published—creator AI design 101 on Lovart. lovart.ai/signup.",
     "AI Design for Content Creators 101: From Idea to Published",
     "Creators do not suffer from ideas—they suffer from throughput. Thumbnails, community posts, merch, and sponsor integrations each demand different specs with the same face. Lovart's **Identity Lock** and **ChatCanvas** keep you recognizable across formats.",
     "[IMAGE 1 PLACEHOLDER — Thumbnail trio, channel banner, and short-form storyboard with locked character]",
     "creator economy", "throughput"),
    (15, "ai-design-agencies-101-scaling-client-work", "AI Design for Agencies 101: Scaling Client Work Without Scaling Headcount",
     "ai design agencies 101 scaling", "ChatCanvas, Brand Kit, Edit Elements, collaboration",
     "Agency Lovart 101: multi-client Brand Kits, canvas separation, revision workflows, and margin-friendly scaling without hiring sprees.",
     "AI Design for Agencies 101: Scale Work", "Scale agency client work with Lovart—101 playbook. lovart.ai/signup.",
     "AI Design for Agencies 101: Scaling Client Work Without Scaling Headcount",
     "Agencies sell craft and margin. Hiring sprees eat margin; tool chaos eats craft. Lovart lets studios separate clients by **Brand Kit** and **ChatCanvas**, standardize revision via **Edit Elements**, and ship more rounds per strategist hour.",
     "[IMAGE 1 PLACEHOLDER — Multi-client canvas tabs with isolated Brand Kits and approval threads]",
     "agency operations", "client scale"),
]

for num, slug, title, focus, tool, desc, seo_t, seo_d, h1, hook, img, theme_a, theme_b in TOPICS:
    p1 = [
        _b(f"Why {theme_a} breaks traditional workflows", [
            f"Teams treating {theme_a} as one-off prompts burn credits without building reusable systems",
            "Handoffs between strategists, designers, and media buyers lose constraints at every step",
            "Without canvas memory, winners from last quarter cannot be found when the same brief returns",
            "Spreadsheet briefs detached from visuals cause media buyers to improvise crops that violate brand",
            "Single-tool generators cannot see your last approved hero when making today's story cutdown",
        ], [f"Lovart addresses {theme_a} with agentic planning on ChatCanvas, not isolated generators"]),
        _b(f"Stakeholders who feel {theme_b} pain first", [
            "Operators responsible for revenue metrics—not vanity likes—need accurate product representation",
            "Brand owners fear drift more than they fear blank pages",
            "Compliance and legal teams care about claims before aesthetics",
            "Founders wear brand hats at 11 p.m. and need guardrails, not another blank canvas",
            "Agency account leads need client-separated memory without five Figma teams",
        ], ["MCoT surfaces risky copy combinations before render when Thinking Mode is enabled"]),
        _b("First principles for durable production", [
            "Separate strategy (what must be true) from execution (how it looks)—MCoT encodes the split",
            "Treat references as contracts, not inspiration—upload what legal already approved",
            "Prefer semantic edits over rerolls when 80% of a frame is correct",
            "Build kits before volume—scaling noise is worse than scaling silence",
        ], ["These principles appear across Lovart 101 guides from ChatCanvas to Brand Kit"]),
    ]
    p2 = [
        _b("Lovart capabilities that matter here", [
            "Brand Kit enforces palette, type, and references for every format in the matrix",
            "Touch Edit and Text Edit fix localized failures without rerolling entire scenes",
            "Smart Mockups and Upscale bridge screen drafts to production realities",
            "Integrated video models connect stills to motion on the same canvas",
            "Identity Lock preserves faces, mascots, and hero SKUs across unrelated backgrounds",
            "Visual Insights helps diagnose weak hierarchy before spend goes live",
        ], ["Model routing sends each sub-task to Nano Banana, Seedream, Seedance, or Veo as appropriate"]),
        _b("Metrics that prove progress", [
            "Track reroll rate per campaign—reasoning should lower it week over week",
            "Measure time-to-first-approved-asset, not time-to-first-pixel",
            "Compare cost per approved deliverable against freelancer baselines",
            "Count brand-violation catches in review—should fall after kit hardening",
            "Monitor credit spend per channel to reallocate Thinking vs Fast Mode policies",
        ], ["Finance and creative ops can share one dashboard narrative"]),
        _b("Common failure modes to eliminate", [
            "Over-prompting: novels that confuse decomposition—keep structured brevity",
            "Under-specifying channel: missing aspect ratio or safe zones until export panic",
            "Skipping kit setup: beautiful one-offs that cannot repeat tomorrow",
            "Rerolling instead of Touch Editing: paying for full scenes when one object is wrong",
        ], ["Cross-read [common prompting mistakes](/blog/common-ai-prompting-mistakes-design-results-how-to-fix) when results feel random"]),
    ]
    steps = [
        _b("Define outcomes and constraints", [
            "Write a half-page brief: audience, channel, mandatories, forbidden elements, and success metric",
            "Attach on-canvas references; label them in-chat so MCoT weights them correctly",
            "Confirm Brand Kit is current—seasonal accents belong in kit variants, not stray prompts",
        ], []),
        _b("Produce the core asset", [
            "Use Thinking Mode for new categories; Fast Mode when repeating winning structures",
            "Generate a hero plus two alternates; place side by side for stakeholder review",
            "Apply Identity Lock when characters or SKUs must remain identical across outputs",
        ], []),
        _b("Refine semantically", [
            "Touch Edit object-level changes; Text Edit for on-image type; Edit Elements when layers need isolation",
            "Run Smart Mockups for physical context when the brief includes packaging or signage",
            "Upscale or export vector/PDF when print or OOH is in scope",
        ], []),
        _b("Scale and document", [
            "Duplicate canvas for the next drop; swap copy or SKUs while kit stays locked",
            "Export format matrix (1:1, 4:5, 9:16, 16:9) from the same approved hero",
            "Archive prompts and plan snippets in-thread for institutional memory",
        ], []),
        _b("Launch and retrospective", [
            "Publish or hand off exports with filenames that include channel and date",
            "Log performance feedback next to the winning canvas node for the next sprint",
            "Schedule kit and reference updates if the campaign revealed gaps",
            "Share signup and pricing links with stakeholders evaluating seat expansion",
        ], []),
        _b("Cross-train the team", [
            "Run a 30-minute lab: one brief, Thinking Mode plan review, one Touch Edit fix",
            "Document three approved prompt snippets per channel in your ops wiki",
            "Pair marketers and designers on the same canvas to align vocabulary",
        ], []),
    ]
    deriv = [
        f"Apply {theme_a} lessons to a launch sprint with three channels in one canvas",
        f"Pair {theme_b} governance with batch social generation for a month of posts",
        "Hand off print-ready exports to vendors after Upscale and bleed checks",
        "Combine stills and motion for a paid social story arc without leaving ChatCanvas",
        "Run agency-style client rounds with isolated Brand Kits per account",
    ]
    faq = [
        (f"Do I need prior experience with {theme_a}?", "No—structured briefs and Lovart editing tools cover most gaps; specialist review still helps for regulated industries."),
        ("Which Lovart plan fits high volume?", "Compare seats, credits, and commercial rights on Lovart pricing before committing to a campaign month."),
        ("Can I migrate assets from other tools?", "Upload references and logos into Brand Kit; rebuild active campaigns on ChatCanvas for agent memory."),
        ("How do I keep brand consistency?", "Brand Kit plus documented brief templates—see Brand Kit 101 for system setup."),
        ("What if generations fail legal review?", "Use Thinking Mode plans to adjust claims before render; Touch Edit for post-render hotfixes."),
    ]
    schema_steps = ["Define brief and Brand Kit", "Produce hero and alternates", "Semantic refine and mockup", "Scale formats and document"]
    cover = None
    if slug == "ai-design-marketers-101-no-design-team":
        cover = "https://liblibai-online.liblib.cloud/blog-card-cover/1772516937198.png"
    REST.append(
        _mk(num, slug, title, focus, tool, desc, seo_t, seo_d, h1, hook, img,
            f"Part 1: {theme_a.title()} — Root Causes", p1,
            f"Part 2: Lovart Strategy for {theme_b.title()}", p2,
            "Part 3: Step-by-Step on ChatCanvas", steps,
            f"Lovart 101 — {theme_a.title()}",
            deriv, faq, schema_steps, cover_override=cover)
    )

ALL_SPECS = [CHATCANVAS, MCOT, _article3(), *REST]
