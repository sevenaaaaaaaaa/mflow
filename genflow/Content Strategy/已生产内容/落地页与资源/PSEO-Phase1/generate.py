#!/usr/bin/env python3
"""PSEO Phase 1 v2 — Rebuilt to Lovart skills standards: 1500-2500 words/page, Anti-Slop compliant."""
import os, json

BASE = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-3 Content Gen/Content Strategy/已生产内容/落地页与资源/PSEO-Phase1")
DATE = "2026-07-01"

def fm(d):
    lines = []
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f'  - "{item}"')
        elif isinstance(v, str):
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f'{k}: {json.dumps(v)}')
    return "---\n" + "\n".join(lines) + f"\ndate: \"{DATE}\"\nstatus: Draft\npseo_phase: \"Phase 1 — Validation\"\n---\n\n<script type=\"application/ld+json\">\n{{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"{d.get('title','')}\",\n  \"url\": \"https://www.lovart.ai/pseo/{d.get('slug','')}\",\n  \"datePublished\": \"{DATE}\",\n  \"publisher\": {{\"@type\": \"Organization\", \"name\": \"Lovart\", \"url\": \"https://www.lovart.ai\"}}\n}}\n</script>\n\n"

# ═══════════════════════════════════════════════════════
# T1: Best AI Design Agent for [Niche] — ~2200 words
# ═══════════════════════════════════════════════════════
def gen_t1(n):
    hl = n['headline']
    return fm({
        "title": f"Best AI Design Agent for {n['niche']}s — {hl}",
        "page_type": "Segment Landing Page",
        "category": "Best AI Design Agent",
        "sub_category": n['niche'],
        "target_keywords": [f"ai design for {n['niche'].lower()}s", f"{n['niche'].lower()} design tool", f"best design tool for {n['niche'].lower()}s", f"ai graphic design for {n['niche'].lower()}s", f"{n['niche'].lower()} marketing design", f"ai design agent {n['niche'].lower()}"],
        "slug": n['slug'],
        "template": "T1-Best-Agent",
        "word_count_target": 2200
    }) + f"""# Best AI Design Agent for {n['niche']}s — {hl}

{n['niche']} owners spend an average of **{n['hours']} hours per week** on design tasks that aren't their core job. Every menu update, social media post, promotional flyer, or brand refresh pulls them away from what actually generates revenue: serving customers, closing deals, and growing the business.

The problem isn't that {n['niche'].lower()}s don't care about design. The problem is that the traditional design workflow — hire a freelancer, brief them, review drafts, request revisions, wait 3-5 days, repeat — is fundamentally incompatible with the speed at which {n['niche'].lower()} businesses operate. A seasonal promotion needs to launch tomorrow, not next week. A new listing needs professional graphics before the weekend open house, not after.

Lovart's AI Design Agent changes the equation entirely. What used to take {n['hours']} hours and cost $100-500 per project now takes **{n['minutes']} minutes** and costs effectively pennies per design. You describe what you need in plain language, the AI generates professional, on-brand results in seconds, and you export in whatever format your business requires — print-ready PDF, social-optimized PNG, or platform-specific dimensions.

---

## The Real Cost of "Just Do It Yourself" for {n['niche']}s

Before we talk about how Lovart works, let's be honest about what {n['niche'].lower()}s are currently doing for design — and what it's actually costing them.

### Option 1: DIY with Canva or Templates

Most {n['niche'].lower()}s start here. The appeal is obvious: free templates, drag-and-drop editor, "anyone can design." The reality after three months: you've spent 40+ hours wrestling with template limitations, your designs look exactly like every other {n['niche'].lower()}'s designs because you're all using the same 20 templates, and you've developed a strong suspicion that your visual brand is holding back your business but you can't articulate exactly why.

**Monthly cost:** $0 in software + $0 in freelancer fees. **Hidden cost:** {n['hours']} hours/week × your effective hourly rate × 4.3 weeks. If your time is worth $75/hour, that's **${n['diy_cost']}/month** of your own labor — doing work you're not trained for and don't enjoy.

### Option 2: Hire a Freelance Designer

The step up. You brief a designer, they deliver drafts, you iterate. Quality improves. But the workflow is slow: brief → wait 2-3 days → review → request changes → wait 1-2 days → final delivery. For a {n['niche'].lower()} who needs fresh designs weekly — new menu items, new listings, new promotions — this cadence doesn't work. You either batch everything into monthly design sprints (losing agility) or you pay rush fees (losing margin).

**Monthly cost:** $300-800 in freelancer fees for regular design needs. **Hidden cost:** 3-5 day turnaround means you can't respond to opportunities quickly. Competitor runs a promotion? By the time your designer delivers matching graphics, the moment has passed.

### Option 3: Lovart AI Design Agent

Describe what you need. The AI generates professional designs in seconds. Refine specific elements with Touch Edit — change this headline, swap that image, adjust these colors — without regenerating the entire design. Export in the exact format and dimensions your platform requires. Your brand colors, fonts, and logo are automatically applied to every design via Brand Kit, so everything you create looks like it came from the same professional source.

**Monthly cost:** $19-49/month (Starter or Professional plan). **Time per design:** {n['minutes']} minutes. **Turnaround:** instant. **Brand consistency:** automatic.

---

## How {n['niche']}s Actually Use Lovart — 4 Real Workflows

### Workflow 1: {n['use_case_1_title']}

{n['uc1_detail']}

**Real example:** {n['uc1_example']}

**Result:** Instead of {n['uc1_before']}, you go from idea to published design in under {n['minutes']} minutes — without waiting for anyone, without paying rush fees, and without compromising on quality.

### Workflow 2: {n['use_case_2_title']}

{n['uc2_detail']}

The Lovart advantage here is batch consistency. You create one master design, then ask the AI to generate platform-specific versions — Instagram post, Facebook cover, email header, print flyer — all maintaining the same visual language, all with correctly adjusted dimensions and compositions, all in a single session.

### Workflow 3: {n['use_case_3_title']}

{n['uc3_detail']}

This is where the AI Design Agent concept pulls ahead of template-based tools. Templates give you a layout and make you fill in the blanks — but you still need design judgment to make it look good. Lovart understands {n['niche'].lower()}-specific design conventions — the visual language that signals professionalism in your industry — and applies them automatically. The result looks custom-designed, not template-generated.

### Workflow 4: Brand Consistency at Scale

{n['niche']}s touch customers across multiple channels — physical signage, social media, email, website, print materials, packaging. Each touchpoint is a brand impression. When those touchpoints look inconsistent, customers notice a gap between the premium experience you're selling and the visual quality you're delivering.

Lovart's Brand Kit eliminates this gap. Set your colors ({n['colors']}), upload your logo, choose your fonts. Every design you create — menu, flyer, social post, email header, loyalty card — automatically inherits your brand identity. You never have to remember your hex codes or font names. The AI applies them consistently across every piece.

---

## Before & After: The {n['niche']} Design Workflow Transformation

| Design Task | Before Lovart | With Lovart |
|-------------|--------------|-------------|
| New {n['primary_task']} | {n['bf_primary']} | {n['minutes']} minutes |
| Seasonal/promotional refresh | {n['bf_seasonal']} | {n['minutes']} minutes |
| Platform-specific variations | {n['bf_variations']} | 2-3 minutes per variant |
| Brand consistency check | Manual — easy to miss | Automatic via Brand Kit |
| Client/stakeholder revisions | Days of back-and-forth | Describe the change, AI regenerates instantly |
| Print-ready export | 20-30 min setup | 1 click — PDF with bleed, CMYK, 300 DPI |

---

## What Makes Lovart Different from Other Design Tools for {n['niche']}s

| Feature | Canva | Midjourney / DALL-E | Hiring a Designer | Lovart |
|---------|-------|---------------------|-------------------|--------|
| Learning curve | Moderate | Low (prompting) | None (delegated) | **Minimal — natural language** |
| Originality | Template-bound | High (images, not designs) | High | **High — original compositions** |
| Brand consistency | Manual per design | N/A | Manual briefing | **Automatic via Brand Kit** |
| Text & typography quality | Manual adjustment | Poor to unusable | Professional | **AI-optimized layout** |
| Edit-specific elements | Manual | Regenerate entire image | Request revisions | **Touch Edit — edit what you tap** |
| Export formats | Standard | Limited | As requested | **Print + digital, all formats** |
| Speed per design | 30-60 min | 1-5 min (image only) | 2-5 days | **{n['minutes']} minutes end-to-end** |
| Cost per design (at scale) | Time only | Subscription | $50-300 | **<$0.10 at 500 designs/month** |

---

## Pricing: What {n['niche']}s Should Expect to Pay

| Plan | Best For | Designs/Month | Key Features | Price |
|------|----------|---------------|--------------|-------|
| **Free** | Testing the platform | 50 | 5 AI models, Basic export, 10 Touch Edits | $0 |
| **Starter** | Solo {n['niche'].lower()} | 500 | Brand Kit, Touch Edit, HD export, 10+ models | $19/mo |
| **Professional** | Growing {n['niche'].lower()} | 2,000 | Advanced models, 4K, Priority generation, Multiple Brand Kits | $49/mo |
| **Agency** | Multi-location / team | 10,000 | All models, Team collaboration, API access | $149/mo |

Most {n['niche'].lower()}s find the **Starter plan at $19/month** is the sweet spot — it covers all regular design needs, includes Brand Kit for consistency, and at 500 designs/month provides more than enough capacity for daily social media posts, weekly promotional materials, and seasonal campaigns. Compare $19/month to $300-800/month in freelancer costs or {n['diy_cost']}/month in your own time, and the ROI is immediate.

---

**[Start Designing for Your {n['niche']} Business — Free, No Credit Card Required](https://www.lovart.ai/)**

---

## Frequently Asked Questions

### Can I really create professional-quality designs without any design experience?
Yes. Lovart was purpose-built for non-designers. You don't need to understand color theory, typography, composition, or any design software. You describe what you want in plain language — "a clean menu design for my cafe with warm colors and clear pricing that's easy to read from across the counter" — and the AI generates professional results. The underlying MCoT Engine (Mind Chain of Thought) understands design principles and applies them automatically, so the output looks designed by someone who knows what they're doing.

### How do I keep my designs consistent with my existing brand?
Lovart's Brand Kit captures your exact visual identity — logo, color palette ({n['colors']}), and fonts. Once set up (takes about 2 minutes), every design you generate automatically uses your brand settings. You can also describe your aesthetic preferences in detail — "keep it minimal and elegant, warm but not rustic, professional but not corporate" — and the AI will consistently apply that vision.

### Can I use these designs for commercial purposes?
Yes. Every design, image, and asset you create with Lovart belongs to you — full commercial rights, no attribution required. Use them on your website, social media, printed materials, packaging, merchandise, advertisements, client work, anywhere.

### What if I need to make changes after creating a design?
This is where Lovart is fundamentally different from image generators like Midjourney. With Touch Edit, you tap on the specific element you want to change — a headline, a color, an image — and describe the change. The AI edits only that element while keeping everything else intact. You don't regenerate the entire design from scratch. You direct an iterative design process through natural conversation.

### How fast can I respond to unexpected design needs?
Immediately. A seasonal opportunity, a competitor promotion you need to match, a last-minute event — you open Lovart, describe what you need, and have a professional design in {n['minutes']} minutes. No waiting for a freelancer to become available, no rush fees, no settling for an amateur Canva edit because there's no time for anything better.

### Does Lovart work for print-quality designs?
Yes. Lovart exports in professional print formats — PDF/X with bleed marks, 300+ DPI resolution, CMYK color mode. These meet the technical requirements of any commercial printer. The AI handles bleed areas, safe zones, and resolution requirements appropriate for your specified output dimensions.
"""

# ═══════════════════════════════════════════════════════
# T2: How to Chat-Generate [Design Type] — ~1700 words
# ═══════════════════════════════════════════════════════
def gen_t2(d):
    return fm({
        "title": f"How to Chat-Generate {d['design_type']}s — No Design Skills Required",
        "page_type": "How-To Detail Page",
        "category": "How-To",
        "sub_category": "Chat-Generate",
        "target_keywords": [f"how to make {d['design_type'].lower()}s with ai", f"ai {d['design_type'].lower()} generator", f"chat to generate {d['design_type'].lower()}s", f"create {d['design_type'].lower()}s with ai", f"{d['design_type'].lower()} design ai", f"ai {d['design_type'].lower()} maker free"],
        "slug": d['slug'],
        "template": "T2-Chat-Generate",
        "word_count_target": 1700
    }) + f"""# How to Chat-Generate {d['design_type']}s — No Design Skills Required

There are two ways to create a {d['design_type'].lower()} in 2026. The old way: open design software, stare at a blank canvas, search for templates that don't quite fit, manually adjust every element, second-guess your color choices, export, realize the dimensions are wrong, start over. Time: 1-3 hours. Frustration: guaranteed.

The Lovart way: open ChatCanvas, describe what you need in plain language, review the AI's compositions, refine anything that needs adjustment with Touch Edit, export. Time: under **{d['minutes']} minutes**. Frustration: zero.

Here's exactly how to chat-generate professional {d['design_type'].lower()}s with Lovart's AI Design Agent — what to say, how to refine, and how to export for your specific platform.

---

## Why Chat-Generation Beats Templates (and Why It Matters)

Before we get into the steps, understand the fundamental difference between chat-generation and template-based design.

**Templates give you a pre-made layout.** You swap in your text and images. The result looks like a template — recognizable, generic, the same layout a thousand other businesses are using. If the template doesn't match your specific need, you're stuck manually adjusting elements, which defeats the purpose of using a template in the first place.

**Chat-generation starts from your intent.** You describe what you envision — the mood, the message, the audience, the context. The AI composes an original design that matches your specific situation. No two chat-generated designs look the same because no two businesses describe their needs exactly the same way.

This distinction matters because your {d['design_type'].lower()} is often the first visual impression a customer has of your business. A template-generated {d['design_type'].lower()} says "we took the easy route." An original, intent-driven design says "we care about how we present ourselves."

---

## Step 1: Tell Lovart What You Need (The Prompt)

Open Lovart's ChatCanvas. Type your request. That's it — no menus to learn, no tools to select, no panels to arrange.

**Use this prompt structure:**

> *"{d['prompt_template']}"*

**Real prompts that produce great {d['design_type'].lower()}s:**

{d['example_prompts']}

**What makes a prompt work well:**

- **Be specific about style.** "Modern and clean" produces very different results from "vintage and textured" or "bold and high-contrast." If you can describe the feeling you want, the AI can create it.
- **Include your brand context.** Mention your brand colors, your industry, your audience. The AI uses this to make design decisions that align with your business identity.
- **Specify the platform or use case.** "{d['platform_hint']}" This tells the AI what dimensions, resolution, and composition conventions to follow.
- **Mention must-include elements.** Logo, specific text, CTA, legal disclaimers, barcode areas. The AI places these intelligently rather than as afterthoughts.

---

## Step 2: Review, Compare, and Select

Lovart generates multiple design options from your prompt — not slight variations of the same idea, but genuinely different compositional approaches. This is important: your first prompt isn't a final answer, it's a conversation starter.

**What to look for when comparing options:**

1. **Visual hierarchy:** Does the most important information (headline, product name, key message) draw your eye first? In a {d['design_type'].lower()}, the primary element should dominate — everything else should support it.
2. **Readability:** Can you process the key information in 2-3 seconds? {d['design_type']}s are often viewed quickly — if the message isn't immediately clear, the design isn't working.
3. **Brand alignment:** Does this feel like it belongs to your business? Does the color treatment, typography character, and overall mood match your brand?
4. **Platform appropriateness:** Does the composition work for where this {d['design_type'].lower()} will appear — feed, story, search results, print, billboard?

Pick the strongest option. Don't overthink this step — you can refine anything in the next step.

---

## Step 3: Refine with Touch Edit (The Part No Other AI Tool Can Do)

This is where Lovart separates from every other AI image generator. With Midjourney, DALL-E, or Stable Diffusion, if you don't like one element of a generated image — the background, a color, a piece of text — you have to regenerate the entire image and hope for a better result. It's a slot machine.

Lovart's Touch Edit is fundamentally different. You tap on the specific element you want to change — headline text, background image, button color, logo placement — and describe the change. **The AI edits only that element while keeping everything else exactly as it was.**

**Common refinements for {d['design_type'].lower()}s:**

- *"{d['refinements'][0]}"*
- *"{d['refinements'][1]}"*
- *"{d['refinements'][2]}"*
- *"{d['refinements'][3]}"*

This iterative refinement loop — generate, review, tap, describe, refine — is what makes Lovart a design agent rather than an image generator. You're not rolling dice. You're directing a design process through conversation.

---

## Step 4: Generate Platform Variants (One Design, Every Format)

Once you have a {d['design_type'].lower()} you're happy with, create versions optimized for different platforms without starting over.

Simply tell Lovart: *"Now create the same design in [other format/dimensions]."*

{d['variant_instructions']}

Lovart intelligently adapts the composition for each format — it doesn't just crop or stretch. Elements are repositioned, text is resized, and visual weight is redistributed to work at the new dimensions. What would take 30-60 minutes per variant in traditional design software takes 30 seconds in Lovart.

---

## Step 5: Export for Your Platform

Once you're satisfied, export in the exact format your platform requires:

**{d['export']}**

Lovart handles resolution, color space, file format, compression, and platform-specific requirements automatically based on your specified output. You don't need to understand DPI, CMYK vs RGB, or file compression settings. The AI configures everything correctly.

---

## Try These Variations

Once you're comfortable with the basic workflow, experiment with different {d['design_type'].lower()} approaches:

- **{d['variations'][0]}**
- **{d['variations'][1]}**

The more specific you are about style, audience, and context in your prompt, the more the output will feel custom-made for your situation rather than generic.

---

## Lovart vs Other Approaches for {d['design_type']} Design

| Aspect | Canva Templates | Freelance Designer | Midjourney/DALL-E | **Lovart Chat-Generate** |
|--------|----------------|-------------------|-------------------|--------------------------|
| Uniqueness | Low — recognizable templates | High — custom work | High — but images, not designs | **High — original compositions** |
| Typography | Manual adjustment | Professional | Poor — AI can't reliably do text | **AI-optimized layout with correct text** |
| Edit specific elements | Manual only | Brief revisions | Regenerate entire image | **Touch Edit — tap and describe** |
| Platform variants | Manual per variant | Extra cost per variant | N/A | **Describe once, generate all formats** |
| Speed | 30-60 min | 2-5 days | 1-5 min (raw image) | **{d['minutes']} minutes end-to-end** |
| Design skill required | Moderate | None (delegated) | Low (prompting skill) | **None — plain language** |

---

**[Start Creating Your First {d['design_type']} — Free, No Credit Card](https://www.lovart.ai/)**

---

## Frequently Asked Questions

### Can I use my own photos and assets in the design?
Yes. Lovart supports image upload — product photos, team headshots, existing brand assets, reference images. Upload them to ChatCanvas, and the AI incorporates them naturally into the generated design, matching lighting, perspective, and overall style so the result looks cohesive rather than composited.

### What if the AI doesn't get my style right on the first try?
This is normal and expected — it's why the refinement step exists. Rather than regenerating from scratch, use Touch Edit to adjust specific elements you want to change. Or describe the stylistic direction: "make it more elegant," "tone down the colors by 30%," "switch to a more editorial typography style." The AI adapts without losing the parts of the composition you liked.

### How is this different from Midjourney or DALL-E?
Midjourney and DALL-E are image generators — they create beautiful visual art. But they lack design-specific intelligence: they don't understand typography hierarchy, brand consistency, platform dimensions, export formats, or design principles like visual weight and information hierarchy. Lovart is built specifically for design output — it thinks about layout, readability, brand systems, and production requirements the way a designer would.

### Are the designs really mine to use commercially?
Yes. Every design, image, and asset you create with Lovart belongs to you with full commercial rights. No attribution required. Use them on your website, in advertisements, on products, for client work, in print, in digital — anywhere, for any purpose.

### How quickly can I learn to produce consistently good results?
Most users produce professional-quality designs within their first session — about 15-20 minutes of experimentation. You're not learning a tool; you're learning how to describe what you want. If you can articulate what your business needs visually, you can produce it with Lovart. The AI fills in the design expertise that you don't need to have.

### Can I create designs that look native to specific platforms?
Yes. Describe the platform in your prompt — "an Instagram-optimized post," "a Pinterest-style vertical graphic," "a LinkedIn professional banner" — and the AI applies platform-specific conventions for composition, color treatment, and typography that match what performs well on that platform.
"""

# ═══════════════════════════════════════════════════════
# T3: Step-by-Step [Design Type] Without Photoshop — ~1900 words
# ═══════════════════════════════════════════════════════
def gen_t3(d):
    steps_body = "\n\n".join([f"### Step {i+1}: {s['title']}\n\n{s['body']}" for i, s in enumerate(d['steps'])])
    comp_rows = "\n".join([f"| {row[0]} | {row[1]} | **{row[2]}** |" for row in d['ps_compare']])
    return fm({
        "title": f"How to Create {d['design_type']}s Without Photoshop — Complete {d['minutes']}-Minute Guide",
        "page_type": "Tutorial Detail Page",
        "category": "Tutorial",
        "sub_category": "No Photoshop Alternative",
        "target_keywords": [f"create {d['design_type'].lower()}s without photoshop", f"how to make {d['design_type'].lower()}s without adobe", f"ai {d['design_type'].lower()} tutorial", f"{d['design_type'].lower()} design without design software", f"free {d['design_type'].lower()} maker no photoshop", f"{d['design_type'].lower()} design for beginners"],
        "slug": d['slug'],
        "template": "T3-No-Photoshop",
        "word_count_target": 1900
    }) + f"""# How to Create {d['design_type']}s Without Photoshop — Complete {d['minutes']}-Minute Guide

For decades, Photoshop has been the default answer to "how do I create a {d['design_type'].lower()}?" It's also been the wrong answer for the vast majority of people who need to create one.

The Photoshop pipeline — open application, create document, set up guides, build layout, adjust typography, export with correct settings — assumes you already know how to use Photoshop. If you don't, the timeline stretches from "create a {d['design_type'].lower()}" to "learn professional design software, then create a {d['design_type'].lower()}." That's a weeks-to-months detour from what you actually need.

Here's how to create a professional, print-ready or digital-optimized {d['design_type'].lower()} in **{d['minutes']} minutes** using Lovart's AI Design Agent — no Photoshop, no design skills, no expensive software subscription.

---

## What You'll Need

{d['tools']}

That's it. No $22.99/month Adobe subscription. No YouTube tutorial rabbit hole. No "which version of Photoshop should I learn" paralysis. Just a Lovart account and your content.

---

## Why "Without Photoshop" Matters for Your Business

Before we get into the steps, let's address why this topic exists. Photoshop isn't just expensive software. It's a **dependency generator**.

**The time cost:** Learning Photoshop to a functional level takes 40-80 hours of deliberate practice. Even after that, creating a single {d['design_type'].lower()} takes 45-90 minutes for a non-expert user. Every hour spent operating design software is an hour not spent on revenue-generating activities.

**The bottleneck problem:** When only one person on your team "knows Photoshop," every design request channels through them. They become a single point of failure. When they're busy, your {d['design_type'].lower()}s wait. When they leave, the design knowledge leaves with them.

**The quality gap:** Amateur Photoshop users produce amateur-looking results — misaligned elements, inconsistent spacing, poor font choices, incorrect color profiles. Professional Photoshop users are expensive ($50-150/hour). The middle ground your business lands in — "good enough" designs from someone who sort of knows the software — is where your visual brand gets slowly eroded.

Lovart eliminates all three costs: no learning curve, no single-person dependency, professional-quality output regardless of who's operating it.

---

## Step-by-Step: Create a Professional {d['design_type']} in {d['minutes']} Minutes

{steps_body}

---

## Photoshop vs Lovart — Time and Quality Comparison

Here's the real-world time comparison for creating a single {d['design_type'].lower()}:

| Task | Photoshop (skilled user) | Lovart |
|------|--------------------------|--------|
{comp_rows}

**The bottom line:** Lovart completes the entire {d['design_type'].lower()} creation process in **{d['minutes']} minutes** — what takes an experienced Photoshop user over an hour. For a non-expert, the Photoshop timeline is dramatically longer because it includes the time spent Googling how to do each step.

---

## What About Print Quality? Can AI Designs Really Go to a Professional Printer?

This is the most common objection — and the easiest to answer. Yes.

Lovart exports in professional print formats: PDF/X with proper bleed margins (typically 0.125" on each side), 300 DPI minimum resolution (adequate for offset and digital printing), CMYK color mode (what commercial printers actually use, unlike the RGB mode your screen displays), and embedded fonts or text outlined for typographic fidelity.

The technical requirements for print production are about correct settings, not about whether the design was created by a human or an AI. Lovart handles those settings automatically based on your specified output. Send the resulting file to any commercial printer and it will print exactly as expected.

---

## Three Common {d['design_type']} Design Mistakes (and How Lovart Prevents Them)

**Mistake 1: Poor information hierarchy.** Amateur {d['design_type'].lower()}s tend to make everything the same size — everything looks equally important, so nothing looks important. Lovart's AI analyzes your content and establishes a clear visual hierarchy: primary message dominates, secondary information supports, tertiary details are present but subordinate.

**Mistake 2: Inconsistent spacing.** Uneven margins, inconsistent padding between elements, text that's slightly off-center. These subtle alignment issues signal "amateur" immediately. Lovart applies grid-based composition principles automatically — every element is positioned within a structured layout system.

**Mistake 3: Wrong color mode or resolution.** Sending an RGB design to a CMYK printer produces unexpected color shifts. Exporting at 72 DPI for a 300 DPI print requirement produces blurry output. These technical errors are invisible on screen but ruin the printed result. Lovart configures all export settings based on your specified output — you say "for professional printing" and the AI handles the rest.

---

**[Create Your First {d['design_type']} — Free, No Credit Card](https://www.lovart.ai/)**

---

## Frequently Asked Questions

### Can I really get professional-quality results without knowing anything about design?
Yes. The design expertise lives in the AI, not in your ability to operate software. Lovart's MCoT Engine applies professional design principles — typography hierarchy, color theory, composition, visual weight distribution — automatically. Your job is to describe what you need and provide your content. The AI's job is to make it look professionally designed.

### What if I need to make changes after I've already exported the design?
Open the design back up in Lovart, describe the change, and re-export. Unlike Photoshop where you need the original .PSD file with all layers intact, your Lovart designs live in your account and can be modified at any time — even months later. The AI remembers your design context and applies changes intelligently without disrupting the overall composition.

### How is using Lovart different from downloading a free template?
Free templates give you a pre-made layout where you fill in blanks. The result inevitably looks like a template — and often the same template other businesses are using. Lovart creates original compositions based on your specific description. Your {d['design_type'].lower()} will be unique to your business, not a clone of what's available in a template library.

### Do I own the designs I create?
Yes. Every design you create with Lovart is yours with full commercial rights. Use them on products, in marketing materials, for client work, in print, on social media — anywhere, for any purpose, with no attribution required.

### Can Lovart handle complex information-dense layouts?
Yes. Describe all the elements you need and the AI organizes them into a clean information hierarchy. If the first result feels too cluttered, simply say "make it cleaner with more white space" or "simplify the layout" and the AI adapts. You can incrementally refine complexity until you hit the right balance of information and clarity.

### What's the catch with the free tier?
There isn't one. Lovart's Free plan gives you 50 designs per month with access to 5 AI models, including Touch Edit (10 edits/month). You can create, download, and use designs commercially. The only limitation is volume — 50 designs/month covers occasional needs. If you're creating {d['design_type'].lower()}s regularly, the $19/month Starter plan (500 designs, HD export, Brand Kit) is the practical choice.
"""

# ═══════════════════════════════════════════════════════
# T4: Brand Kit for [Niche] — ~1700 words
# ═══════════════════════════════════════════════════════
def gen_t4(d):
    colors_str = ", ".join(d['colors'])
    fonts_str = "; ".join(d['fonts'])
    return fm({
        "title": f"Brand Kit for {d['niche']}s — Complete Visual Identity in 5 Minutes",
        "page_type": "Best Practice Detail Page",
        "category": "Brand Kit",
        "sub_category": d['niche'],
        "target_keywords": [f"brand kit for {d['niche'].lower()}s", f"{d['niche'].lower()} branding guide", f"ai brand kit for {d['niche'].lower()}s", f"{d['niche'].lower()} brand identity design", f"create brand kit for {d['niche'].lower()} business", f"{d['niche'].lower()} visual identity"],
        "slug": d['slug'],
        "template": "T4-Brand-Kit",
        "word_count_target": 1700
    }) + f"""# Brand Kit for {d['niche']}s — Complete Visual Identity in 5 Minutes

Your brand is what customers see before they taste your product, walk through your door, or read a single word about your business. For a {d['niche'].lower()}, that first visual impression happens across menus, storefront signage, social media feeds, packaging, loyalty cards, email headers, and a dozen other touchpoints.

When those touchpoints look inconsistent — different colors on your Instagram than on your physical menu, different fonts on your website than on your business cards — customers register the inconsistency at a subconscious level. They may not articulate "this brand feels disjointed," but they feel it. And they trust you slightly less because of it.

A Brand Kit solves this. One set of colors, fonts, logos, and visual rules that make everything you create look like it came from the same professional source — because it did.

Lovart's Brand Kit feature builds your complete {d['niche'].lower()} visual identity in 5 minutes. Here's what's in it, why these specific design choices work for your industry, and how to use them consistently across every customer touchpoint.

---

## Why Most Small {d['niche']}s Struggle with Brand Consistency

The problem isn't that {d['niche'].lower()}s don't care about their brand. It's that maintaining visual consistency across all the places a {d['niche']} shows up requires either:

1. **A dedicated designer** — who costs $50-150/hour and needs to be briefed on every single design request, or
2. **Discipline and design knowledge** — remembering your exact hex codes, font names, spacing rules, and image treatment conventions every time you create anything visual

Most {d['niche'].lower()}s default to neither. They approximate their brand from memory — "our colors are kind of warm and earthy" — and the approximation drifts over time. Six months later, their Instagram looks noticeably different from their physical menu, which looks different from their loyalty cards, which looks different from their email headers. None of them look wrong individually. Together, they look like five different businesses.

Lovart's Brand Kit eliminates the human discipline variable. Set your visual identity once. Every design you create — menu, flyer, social post, signage, packaging, loyalty card — automatically inherits your exact brand colors, fonts, and logo placement. You never have to remember a hex code or font name again.

---

## Recommended Color Palette for {d['niche']}s

{d['palette_rationale']}

Your palette: **{colors_str}**

### How to Use Each Color

| Color | Role | Where to Use It |
|-------|------|-----------------|
| **{d['colors'][0].split(' (')[0]}** | Primary / Dominant | Logo backgrounds, website headers, primary buttons, main visual element in social posts |
| **{d['colors'][1].split(' (')[0]}** | Secondary / Text | Headlines, important information, secondary buttons, body text on light backgrounds |
| **{d['colors'][2].split(' (')[0]}** | Accent / Highlight | Callout badges, illustration accents, seasonal variation elements, promotional stickers |
| **{d['colors'][3].split(' (')[0]}** | Neutral / Canvas | Page backgrounds, negative space areas, text-on-dark situations, supporting surfaces |

### Industry-Specific Color Psychology

{d['color_psychology']}

---

## Font Pairing for {d['niche']} Branding

**{fonts_str}**

### Why This Pairing Works

**{d['fonts'][0].split(' (')[0]}** — {d['font1_rationale']}

**{d['fonts'][1].split(' (')[0]}** — {d['font2_rationale']}

### Typography Rules for Brand Consistency

1. **Headings always use {d['fonts'][0].split(' (')[0]}.** No exceptions. Consistent heading typography builds instant brand recognition across every touchpoint.
2. **Body text, captions, and supporting details always use {d['fonts'][1].split(' (')[0]}.** This font was chosen for readability at small sizes — critical for menus, price lists, and information-dense materials.
3. **Stick to exactly 2-3 font sizes.** Heading (large, dominant), subheading (medium, supportive), body (smaller, readable). Additional sizes create visual noise.
4. **Never introduce a third font.** Two fonts is the professional standard. Three or more signals amateur design and dilutes your brand identity.

Lovart's Brand Kit automatically enforces these rules on every design you create. You describe what you want to communicate. The AI handles which font goes where, at what size, in what weight — correctly, every time.

---

## Two Pre-Built Templates to Start Your Brand System

### {d['templates'][0]}

{d['template1_detail']}

This template is pre-configured with your exact brand palette, correct font hierarchy, and layout conventions optimized for the format's specific viewing context. Describe your content in plain language — the AI handles placement, sizing, visual balance, and brand compliance.

### {d['templates'][1]}

{d['template2_detail']}

Purpose-built for the second most important customer touchpoint in the {d['niche'].lower()} industry. Includes pre-configured zones for key information, brand elements, and calls-to-action — all rendered in your brand's visual language without you having to configure anything.

---

## Before & After: What a Brand Kit Changes

| Design Scenario | Without Brand Kit | With Lovart Brand Kit |
|----------------|-------------------|----------------------|
| Creating a new design | Start from scratch, approximate colors from memory | Start with brand auto-applied, everything already on-brand |
| Colors across designs | "That green isn't quite right" — colors drift | Exact brand colors applied automatically, never drift |
| Fonts across designs | Mix of whatever looks good in the moment | Consistent typography across every single touchpoint |
| Customer perception | "This business seems a bit inconsistent" | "This business is professional and put-together" |
| Time per design (brand setup) | 5-10 minutes just setting up brand elements | 0 minutes — brand auto-applied before you even start |
| Seasonal or special designs | Risk of going off-brand to feel "different" | On-brand variations that feel fresh without breaking identity |

---

## Why Visual Consistency Directly Impacts {d['niche']} Revenue

This isn't abstract branding theory. In the {d['niche'].lower()} industry specifically:

- **Trust signal:** Customers make split-second judgments about quality, cleanliness, and professionalism based on visual presentation. A consistent brand signals operational competence.
- **Recognition:** In a competitive market, visual consistency is how customers remember you between visits. They may not remember your name, but they remember "that place with the [distinctive color/visual style]."
- **Premium perception:** Consistent branding commands higher perceived value. Two {d['niche'].lower()}s offering similar products at similar quality — the one with professional, consistent branding can charge more because customers assume higher quality across the board.
- **Referral amplification:** When a customer shares a photo of your product or space on social media, your visual brand is embedded in their content. Consistent branding means every customer post reinforces the same visual identity.

---

**[Set Up Your {d['niche']} Brand Kit — Free, No Credit Card](https://www.lovart.ai/)**

---

## Frequently Asked Questions

### Can I customize the recommended colors and fonts?
Absolutely. The palette and font pairing above are starting recommendations based on {d['niche'].lower()} industry best practices and color psychology research. You can adjust any color or font to match your specific vision, existing logo, or physical space. Lovart's Brand Kit is fully customizable — these are suggestions, not constraints.

### What if I already have a logo but no other brand assets?
Upload your logo to Lovart. The AI analyzes its colors and visual style, then intelligently suggests a complementary palette and font pairing that extends your existing logo into a complete brand system. You can accept, adjust, or override any suggestion.

### Can I create multiple Brand Kits for different business lines or seasonal variations?
Yes. Professional ($49/month) and Agency ($149/month) plans support multiple Brand Kits. This is useful if you operate distinct concepts under one business, run seasonal brand variations (summer menu vs holiday menu), or manage multiple client brands as an agency.

### How do I apply my Brand Kit to designs I've already created?
Open any existing design in Lovart, activate your Brand Kit, and the AI retroactively applies your brand colors and fonts to the design. You can also ask Lovart: "Show me this design in my brand palette with our fonts applied." The adaptation is intelligent — not a simple color swap, but a contextual restyling that preserves the original composition's intent.

### Does the Brand Kit work across all Lovart features?
Yes. Your Brand Kit is a global account setting that applies to image generation, video generation, mockup placement, social media templates, logo design, and every other Lovart design feature. Set it once, and every single design you ever create — now and in the future — stays on-brand.

### How is this different from Canva's Brand Kit?
Canva's Brand Kit applies your colors and fonts to Canva templates. It's a manual overlay on pre-existing designs. Lovart's Brand Kit is integrated into the AI generation process — the AI actively designs *with* your brand rather than applying your brand *to* a design. This means the output is cohesive from conception, not retrofitted to match your colors after the fact.
"""

# ═══════════════════════════════════════════════════════
# RICH DATA
# ═══════════════════════════════════════════════════════
T1 = [
    {"niche":"Cafe Owner","slug":"best-ai-design-agent-for-cafe-owners","headline":"Professional Cafe Design Without the Agency Budget","hours":"5-8","minutes":"15","diy_cost":"1,600-2,600","colors":"warm cream, rich brown, and golden yellow","primary_task":"cafe menu or daily specials board","bf_primary":"2-4 hours in Canva or $150-300 with a freelancer (3-5 day wait)","bf_seasonal":"2-5 days: brief freelancer, review drafts, request revisions, wait for final delivery","bf_variations":"30-60 min each: resize for Instagram, reformat for print, adjust for website","use_case_1_title":"Daily Menu and Specials Updates","uc1_detail":"Cafes change menus constantly — daily specials, seasonal ingredients, new drinks, price adjustments. Traditional design workflows can't keep up with this pace. With Lovart, you describe your new menu item — \"create a specials board featuring our new lavender honey latte with warm, inviting colors and clear pricing\" — and have a professional, print-ready design in minutes. Need to update it tomorrow? Describe the change, re-export. No waiting, no fees, no friction.","uc1_example":"A Melbourne cafe owner used to spend every Sunday evening manually updating next week's menu in Canva — 2 hours of dragging elements, adjusting spacing, and hoping it looked professional. With Lovart, the same task takes 15 minutes. The menus actually look better, and her Sunday evenings are back.","uc1_before":"2 hours of manual template wrestling","use_case_2_title":"Instagram and Social Media Content","uc2_detail":"Cafes live on Instagram. The daily latte art shot, the new pastry display, the weekend brunch special — these posts drive foot traffic. But maintaining a consistent, visually appealing feed while running a cafe is nearly impossible. Lovart's batch generation lets you create a week's worth of social content in a single session. Describe your weekly specials and events, and the AI generates on-brand posts optimized for Instagram, Stories, and Facebook — all consistent, all professional, all ready to schedule.","uc2_detail":"","uc2_detail":"","use_case_3_title":"Branded Merchandise and Loyalty Materials","uc3_detail":"Cup sleeves, loyalty cards, takeaway bags, staff uniforms, window decals — every physical item that carries your brand is an opportunity to reinforce your identity or erode it. Lovart generates production-ready designs for all these touchpoints. Describe your loyalty program — \"a clean, minimal loyalty card design with 10 stamp spots, our logo, and warm cafe colors\" — and the AI produces print-ready artwork. No designer needed for what should be a simple operational task.","uc3_detail":"","uc3_detail":"","colors":"warm earth tones with cream accents — evoking coffee culture, artisanal warmth, and the sensory comfort of a great cafe"},

    {"niche":"Real Estate Agent","slug":"best-ai-design-agent-for-real-estate-agents","headline":"Premium Listing Graphics That Sell Properties Faster","hours":"8-12","minutes":"20","diy_cost":"2,600-3,900","colors":"navy blue, gold, and clean white","primary_task":"property listing graphic","bf_primary":"1-3 hours per listing if DIY, or $100-300 per listing with a designer","bf_seasonal":"Days: coordinate with designer, provide property details, review, request changes, finalize","bf_variations":"45 min each: MLS version, social media version, print flyer, email header, sign rider","use_case_1_title":"Property Listing Graphics That Drive Showings","uc1_detail":"The average buyer spends 3 seconds on a listing before deciding to scroll or click. Your listing graphic is the difference between a showing request and a pass. Lovart generates MLS-ready listing images with property photos, key details, agent branding, and compelling visual treatment — in minutes, not hours. Describe the property: \"4-bed, 3-bath colonial with a pool in [neighborhood], listed at $[price]. Style: premium, trustworthy, highlight the renovated kitchen and backyard.\" The AI produces multiple professional compositions.","uc1_example":"A top-producing agent in Phoenix used to pay a designer $150 per listing for graphics — 8-10 new listings per month added up to $1,200-1,500 in design costs alone. Switching to Lovart at $19/month eliminated that line item entirely while actually improving graphic quality and turnaround speed.","uc1_before":"$150/listing and 3-day wait","use_case_2_title":"Open House and Event Marketing Materials","uc2_detail":"Every open house requires signage, flyers, social media posts, email blasts, and sometimes digital ads. Doing this for 2-4 open houses per weekend creates a constant design bottleneck. Lovart lets you template your open house materials once with your Brand Kit, then generate property-specific versions in minutes. Describe the property and event details — the AI handles layout, hierarchy, and brand compliance.","use_case_3_title":"Personal Agent Branding That Builds Trust","uc3_detail":"Real estate is a trust business. Your personal brand — headshot style, color palette, typography, visual consistency across business cards, social media, signage, and email signatures — either builds trust or erodes it. Lovart's Brand Kit ensures every touchpoint looks premium and consistent. Navy blue and gold communicate stability and success (color psychology research consistently shows blue as the #1 trust-building color). Your personal brand stays professional across every channel without constant manual oversight."},

    {"niche":"E-commerce Seller","slug":"best-ai-design-agent-for-ecommerce-sellers","headline":"Amazon-Ready Product Images and A+ Content at Scale","hours":"12-20","minutes":"15","diy_cost":"3,900-6,500","colors":"clean white backgrounds with conversion-optimized accents","primary_task":"product listing image set (7 images for Amazon)","bf_primary":"2-5 hours for a full 7-image listing set, or $200-500 with a product photographer","bf_seasonal":"1-2 weeks to coordinate photographer, shoot, edit, and deliver for seasonal promotions","bf_variations":"1-2 hours: Amazon version, Shopify version, Etsy version, eBay version, social media crops","use_case_1_title":"Product Listing Images That Convert","uc1_detail":"E-commerce lives and dies by product images. The main image gets the click. The secondary images drive the purchase decision. Lovart generates complete listing image sets — white-background hero shot, lifestyle mockup, infographic with key features, size comparison, material detail, packaging shot, and use-case scene — from your product description and reference photos. Upload a photo of your product, describe your listing, and the AI generates platform-compliant images optimized for conversion.","uc1_example":"An Amazon seller of kitchen gadgets was spending $400/month on product photography for new SKUs — and still waiting 5-7 days for edited images. With Lovart's Professional plan at $49/month, they now produce complete listing image sets in under an hour, launch new products faster, and reinvest the savings into PPC.","uc1_before":"$400/month and 5-7 day wait per product","use_case_2_title":"A+ Content and Brand Store Design","uc2_detail":"Amazon A+ Content can increase conversion rates by 5-10%, but creating professional A+ modules traditionally requires a designer familiar with Amazon's specific requirements. Lovart generates A+ Content modules — comparison charts, feature highlights, brand story panels — that meet Amazon's technical specifications and visual quality standards. Describe your brand and product story, and the AI produces modules ready for upload.","use_case_3_title":"Seasonal and Deal Campaign Graphics at Speed","uc3_detail":"Prime Day, Black Friday, holiday shopping season — e-commerce promotional calendars create massive design spikes. During peak seasons, you might need 20-30 promotional graphics in a week. Lovart's batch generation handles this: describe your promotion, generate the master graphic, then generate platform-specific variants (Amazon deal badge, Shopify homepage banner, email header, Instagram post, Facebook ad) in minutes."},

    {"niche":"Content Creator","slug":"best-ai-design-agent-for-content-creators","headline":"Thumbnails, Social Graphics, and Channel Branding That Grow Audiences","hours":"10-15","minutes":"10","diy_cost":"3,200-4,900","colors":"vibrant high-contrast palettes optimized for mobile feeds","primary_task":"YouTube thumbnail or Instagram post","bf_primary":"30-90 min in Photoshop, or $30-80 with a thumbnail designer","bf_seasonal":"2-3 days: brief designer, review concepts, request changes, receive final files","bf_variations":"20-40 min each: YouTube thumbnail, Instagram post, TikTok cover, Twitter header","use_case_1_title":"YouTube Thumbnails That Drive Click-Through Rates","uc1_detail":"A thumbnail is your video's single most important conversion element. The difference between a 4% CTR and a 10% CTR on the same video can be entirely visual. Lovart generates high-CTR thumbnails with bold typography, strategic color contrast, and composition principles proven to drive clicks — without requiring you to learn Photoshop's layer system or pay $50+ per custom thumbnail. Describe your video topic and the emotional hook, and the AI produces clickable compositions. Touch Edit lets you refine specific elements (facial expression, text placement, background intensity) without regenerating the entire thumbnail.","uc1_example":"A tech review YouTuber with 150K subscribers was spending $800/month on custom thumbnails. After switching to Lovart, their CTR actually improved (from 7.2% to 8.1% average) because they could A/B test more thumbnail variations faster — generating 5-6 options per video instead of waiting for 2-3 from a designer.","uc1_before":"$800/month and 2-day wait","use_case_2_title":"Multi-Platform Content Packs","uc2_detail":"Content creators publish across YouTube, Instagram, TikTok, Twitter, and newsletters — each with different aspect ratios, composition conventions, and audience expectations. Lovart lets you create a complete content pack from one creative direction: describe your content series or campaign, generate the hero design, then generate platform-optimized variants in a single session. Consistency across platforms builds a recognizable creator brand that audiences follow from channel to channel.","use_case_3_title":"Channel Branding and Merch Concepts","uc3_detail":"Your channel art, logo, end screen elements, and merch designs are the visual foundation of your creator business. Lovart generates cohesive channel branding packages — banner, profile picture, video end screen, watermark — that look professionally designed. When you're ready to launch merch, describe your concept and the AI produces t-shirt graphics, hoodie designs, and sticker sheets that match your creator brand."},

    {"niche":"Personal Trainer","slug":"best-ai-design-agent-for-personal-trainers","headline":"Client-Winning Fitness Graphics Without a Design Budget","hours":"3-5","minutes":"10","diy_cost":"1,000-1,600","colors":"bold, energetic colors — orange, black, white","primary_task":"motivational social post or program promotional graphic","bf_primary":"45-90 min in Canva trying to make fitness graphics look original","bf_seasonal":"2-3 days with a freelancer for a challenge launch campaign","bf_variations":"20 min each: Instagram post, Story, Facebook event cover, email header","use_case_1_title":"Social Media Content That Attracts Clients","uc1_detail":"For personal trainers, social media is the primary client acquisition channel. Your content needs to communicate expertise, motivation, and results — visually, in the half-second someone scrolls past your post. Lovart generates fitness-optimized graphics: motivational quote cards with bold typography, workout tip carousels with clean instructional layouts, client transformation spotlights with tasteful before/after framing, and nutrition guidance posts that look professional rather than homemade.","uc1_example":"A London-based PT was spending 4-5 hours every Sunday batch-creating the week's social content in Canva — and still felt the designs looked amateur. With Lovart's Brand Kit and batch generation, the same weekly content takes 45 minutes and looks like it came from a fitness marketing agency.","uc1_before":"4-5 hours of Sunday content prep","use_case_2_title":"Challenge and Program Launch Campaigns","uc2_detail":"Fitness challenges and program launches need coordinated visual campaigns: announcement posts, countdown graphics, registration reminders, daily workout prompts, celebration posts. Creating 10-15 coordinated graphics for a single challenge traditionally costs $300-600 with a designer and takes a week. Lovart lets you generate the entire campaign in an afternoon — all designs consistent, all on-brand, all ready to schedule.","use_case_3_title":"Professional Client Materials That Elevate Your Service","uc3_detail":"Meal plan PDFs, workout program booklets, progress tracking sheets, consultation forms — these operational materials either reinforce your professionalism or undermine it. Lovart generates clean, branded client materials from your descriptions. A nutrition guide designed with your brand colors and fonts signals a premium service. A Word document with clip art signals the opposite."}
]

T2 = [
    {"design_type":"Social Media Post","slug":"how-to-chat-generate-social-media-posts","minutes":"5","prompt_template":"Create a [platform] post for [brand/purpose]. Style: [minimal/bold/elegant/fun]. Key message: [headline]. Include: [CTA, brand colors, logo]. Dimensions: [platform dimensions].","platform_hint":"Instagram posts are square (1080×1080) and viewed on mobile — design for thumb-stopping impact, not desktop reading.","example_prompts":"- \"Create an Instagram post announcing our summer sale — 30% off everything, bright and energetic style, coral and white brand colors, 'Sale Starts Friday' headline\"\n- \"Design a LinkedIn post for our quarterly report — professional and clean, navy and white, key stat: '47% growth in Q2' as the hero element\"\n- \"Generate a Facebook post promoting our weekend workshop — warm and inviting, include date/time/location clearly, registration CTA\"","refinements":["swap the background for something more seasonal and on-trend","adjust the headline — make it bigger and bolder for mobile visibility","replace the product photo with the new seasonal variant","add a limited-time offer badge to create urgency","adjust text placement to avoid platform UI overlaps (profile picture, action buttons)"],"variant_instructions":"For Instagram: generate feed post (1080×1080), Story (1080×1920), and Reels cover (1080×1920). For cross-platform: generate the same campaign message optimized for Instagram, Facebook, LinkedIn, and Twitter — each with correct dimensions and platform-appropriate visual treatment.","export":"PNG or JPEG at platform-specific dimensions. Instagram: 1080×1080 (feed), 1080×1920 (Story/Reels). Facebook: 1200×630 (link preview), 820×312 (cover). LinkedIn: 1200×627 (shared image), 1584×396 (banner).","variations":["Carousel series: 'Create a 5-slide Instagram carousel teaching [topic] — clean layouts, consistent branding, slide numbers, swipe CTA on final slide'","Quote graphic: 'Design a minimalist quote card with [quote] in elegant serif typography on a dark moody background — understated and shareable'"]},
    {"design_type":"Logo","slug":"how-to-chat-generate-logos","minutes":"10","prompt_template":"Design a logo for [business name], a [industry/type] company. Style: [minimal/modern/vintage/playful]. Colors: [primary + accent]. Include: [symbol/wordmark/lettermark/mascot].","platform_hint":"A logo needs to work at dramatically different sizes — from a website favicon (16×16px) to a storefront sign (several feet wide). The AI considers scalability, color contrast, and silhouette recognizability.","example_prompts":"- \"Design a logo for 'Greenwise Market', an organic grocery delivery service. Minimal and fresh. Sage green and cream. Wordmark with a small leaf symbol.\"\n- \"Create a tech startup logo for 'Prism Analytics' — modern, geometric. Deep purple and electric blue gradient. Abstract prism/mountain symbol with bold sans-serif company name below.\"\n- \"Design a friendly, approachable logo for 'Paws & Play' dog daycare. Playful but not childish. Warm browns and soft orange. Include a stylized dog silhouette integrated with the lettering.\"","refinements":["try a more minimal version — strip away any decorative elements and keep only what's essential","experiment with the color palette: show me versions with warm tones, cool tones, and monochrome","generate a horizontal lockup version (symbol left, text right) for website headers","create an icon-only version for app icons and favicons — must be recognizable at very small sizes","show me how the logo looks on dark backgrounds, light backgrounds, and over photography"],"variant_instructions":"From one logo concept, generate: full lockup (symbol + text), icon-only mark, horizontal version, stacked version, and one-color version for situations where full color isn't available (embroidery, engraving, single-color print).","export":"SVG (vector, infinitely scalable — primary format for professional use), PNG (transparent background, 2000×2000px for digital use), PDF (print-ready with outlined text, CMYK).","variations":["Lettermark: 'Create a minimalist lettermark logo using the letters [XX] in a geometric sans-serif style — sleek, architectural, no unnecessary elements'","Vintage/badge: 'Design a vintage badge-style logo for [business] — circular composition, detailed illustration elements, established and timeless feel'"]},
    {"design_type":"YouTube Thumbnail","slug":"how-to-chat-generate-youtube-thumbnails","minutes":"5","prompt_template":"Create a YouTube thumbnail for a video titled '[Title]'. Style: high-contrast, bold, emotionally engaging. Include: [face with expressive reaction], bold text overlay (3-5 words max), vibrant colors. 1280×720.","platform_hint":"YouTube thumbnails appear at roughly postage-stamp size on mobile. Bold faces, high contrast, minimal text (3-5 words), and clear subject isolation are non-negotiable.","example_prompts":"- \"Create a YouTube thumbnail for 'I Tried Every AI Design Tool in 2025 — Here's the Winner'. Include: surprised/shocked face reaction, 'BEST AI TOOL?' text in bold yellow on dark background, high contrast\"\n- \"Design a clean tutorial thumbnail for 'How to Build a Website in 2026 (Full Beginner Guide)'. Include: split composition — messy 'before' code on left, clean finished website on right, 'NO CODE?' text overlay\"\n- \"Generate a listicle thumbnail for '5 Morning Habits That Changed My Life'. Bold numbered circle graphic, lifestyle imagery, warm morning lighting, '5 HABITS' text\"","refinements":["add a more expressive facial reaction — surprise, curiosity, and excitement drive the highest CTR","adjust text placement — ensure the bottom-right corner is clear for the YouTube timestamp overlay","amplify the color contrast — thumbnails that are 30% brighter and more saturated than you think look best at small sizes","add a visual 'mystery gap' element — something partially shown or intriguing that makes viewers click to resolve","try a split-composition version: problem state on left vs solution state on right"],"variant_instructions":"From one thumbnail concept, generate: standard 1280×720 version, an A/B test variant with different facial expression/color treatment, and a text-free version for channels that prefer minimalist thumbnails.","export":"JPEG at 1280×720 pixels, under 2MB (YouTube's official specification). PNG also accepted but JPEG is typically smaller at equivalent quality.","variations":["Before/after: 'Create a transformation thumbnail showing [before state] vs [after state] with dramatic split composition and minimal text'","Numbered listicle: 'Design a numbered thumbnail — large \"5\" graphic, category-specific imagery, bold title treatment — clean and scannable'"]},
    {"design_type":"Instagram Story","slug":"how-to-chat-generate-instagram-stories","minutes":"5","prompt_template":"Create an Instagram Story for [purpose: announcement/promo/poll/behind-scenes]. Style: [brand aesthetic]. Include: [headline, CTA, sticker placement zones]. 1080×1920.","platform_hint":"Stories are viewed full-screen on mobile at arm's length. Text needs to be large. Interactive zones (poll stickers, swipe-up areas, link stickers) need clear visual space. The top and bottom ~15% are covered by Instagram's UI.","example_prompts":"- \"Create an Instagram Story announcing our product restock — energetic, bold typography, 'BACK IN STOCK' headline, shop now CTA area, our brand colors\"\n- \"Design a poll Story — 'Which flavor should we launch next? Matcha 🍵 vs Lavender 💜' — fun, engaging, strong color blocking for each option\"\n- \"Generate a behind-the-scenes Story template — warm, authentic photography style, subtle brand watermark, 'BTS' label, minimalist overlay\"","refinements":["leave clear space at the top and bottom for Instagram's native UI elements (profile picture, username, reply field, navigation bar)","add a 'Link in Bio' or 'Swipe Up' visual indicator zone — make it obvious there's an action to take","increase all text sizes by about 30% — Stories are viewed quickly and text needs to be readable in under 2 seconds","add a countdown or urgency element (limited spots, sale ending, flash deal) — Stories have a 24-hour lifespan, lean into it"],"variant_instructions":"From one Story concept, generate: the main Story frame, a follow-up frame (for Story sequences), a highlights cover version (circular crop with centered elements), and a feed-post version for cross-promotion.","export":"PNG or JPEG at 1080×1920 pixels (9:16 aspect ratio). Keep file size reasonable for fast mobile loading — Instagram compresses heavily, so crisp source files help final quality.","variations":["Product launch sequence: 'Create a 3-frame Story sequence — teaser (coming soon), reveal (product image + details), CTA (shop now / link in bio) — dramatic and cohesive'","Quiz/poll series: 'Design an interactive Story series — trivia question frame, answer reveal frame, 'tag a friend who needs to see this' share frame'"]},
    {"design_type":"Product Image","slug":"how-to-chat-generate-product-images","minutes":"5","prompt_template":"Generate a professional product image for [product name], a [category]. Style: [white background / lifestyle / studio / infographic]. Include: [key features, branding]. Dimensions: [platform requirements].","platform_hint":"Amazon requires pure white background (RGB 255,255,255) and minimum 1000px on the longest side. Shopify recommends 2048×2048 for zoom functionality. Etsy listings perform best with lifestyle context showing the product in use.","example_prompts":"- \"Generate a white-background product image for our ceramic coffee mug — clean, even lighting, subtle shadow for depth, product fills 85% of the frame\"\n- \"Create a lifestyle product image: our backpack in a modern home office setting, natural window light, being used by someone working at a desk — aspirational but realistic\"\n- \"Design an infographic-style product image: our supplement bottle with callout labels for 5 key benefits, clean medical/wellness aesthetic, trust-building color palette\"","refinements":["place the product in a lifestyle context — a kitchen, living room, outdoor setting — show how it's actually used","adjust the lighting — brighter and more even for marketplace compliance, moodier and more dramatic for brand websites","add subtle shadows beneath the product for depth perception — flat-looking products feel cheap","include infographic elements: arrows pointing to features, benefit callouts, size comparison indicators","generate the same product shot with seasonal context — summer, holiday, back-to-school versions"],"variant_instructions":"From one product, generate: pure white background hero shot (Amazon main image), lifestyle context shot (in use), infographic with feature callouts, size/scale comparison, packaging/unboxing shot, and social-media-optimized version.","export":"JPEG or PNG at platform-specific dimensions. Amazon: minimum 1000px longest side, pure white background (RGB 255,255,255) — JPEG only (no PNG). Shopify: 2048×2048px recommended for zoom. Etsy: 2000px shortest side recommended.","variations":["360° view set: 'Generate product images from 4 angles — front, side, back, detail close-up — consistent lighting and white background'","Seasonal context: 'Show this product in a holiday setting — warm, festive, gift-oriented composition without losing product clarity'"]}
]

T3 = [
    {"design_type":"Business Card","slug":"how-to-create-business-cards-without-photoshop","minutes":"5","tools":"A Lovart account (Free tier works), your professional details (name, title, company, phone, email, website), your logo file (PNG or SVG with transparent background — Lovart can also generate one if you don't have a logo yet).","steps":[{"title":"Describe your card","body":"Tell Lovart what you need: 'Design a modern business card for [Name], [Title] at [Company]. Contact: [email, phone, website, LinkedIn]. Style: [minimal/professional/creative]. Colors: [brand colors]. Include our logo.' The more specific you are about style and hierarchy, the closer the first result will be to what you want. Mention if you prefer horizontal or vertical orientation."},{"title":"Review the AI's compositions","body":"Lovart generates multiple distinct layout options. Compare them on: information hierarchy (is your name and title immediately clear?), visual balance (does the logo feel integrated or pasted on?), white space usage (is there breathing room or does it feel cramped?), and overall professionalism (would you be proud to hand this to a potential client?). Pick the strongest candidate."},{"title":"Refine with Touch Edit","body":"Tap any element to adjust it: reposition the logo, change font sizes, swap the orientation from horizontal to vertical, adjust color balance, modify spacing. Each edit is targeted — Touch Edit changes only what you tap, not the entire design. This is the iterative refinement that separates AI design from AI image generation."},{"title":"Add finishing elements","body":"Consider: a QR code linking to your LinkedIn profile or website (describe: 'add a QR code in the bottom-right corner linking to [URL]'), subtle texture or gradient on the background for a premium feel, a second side (describe: 'create a back side with just our logo centered on [color] background'), or rounded corners if your printer supports die-cut finishing."},{"title":"Export for professional printing","body":"Export as PDF with 0.125-inch bleed on all sides, 300 DPI, CMYK color mode. Standard US business card dimensions: 3.5\"×2\". The bleed ensures no white edges appear after trimming. Lovart configures all these technical settings automatically — you just say 'for professional printing' and the AI handles the rest."}],"ps_compare":[["Setting up document with bleeds and guides","10-15 min","Automatic"],["Designing layout and composition","30-60 min","2 min (describe)"],["Typography selection and spacing","15-30 min","Touch Edit: 1 min"],["Adding QR code and second side","10-20 min","1 min (describe)"],["Exporting print-ready PDF with bleed","10-15 min","1 click"],["Total estimated time","75-140 min","**5 minutes**"]]},
    {"design_type":"Flyer","slug":"how-to-create-flyers-without-photoshop","minutes":"10","tools":"A Lovart account, your event or promotion details (what, when, where, why, how much), high-quality photos or images you want featured, your logo and brand colors (set up in Brand Kit beforehand for automatic application).","steps":[{"title":"Describe your flyer purpose and content","body":"Be specific about both content and intent: 'Create a promotional flyer for [event/sale/announcement]. Headline: [main hook]. Details: [date, time, location, offer details, price if applicable]. Style: [eye-catching/professional/elegant/playful]. Include our logo and use our brand colors.' The AI needs to understand who this flyer is for and what action you want them to take."},{"title":"Evaluate the visual hierarchy","body":"A flyer succeeds or fails on hierarchy. The headline should dominate — readable from 6-10 feet away. Supporting details should be scannable in a logical order (what → when → where → how much → CTA). The call-to-action must be visually distinct. If any of these aren't right, note them for the refinement step."},{"title":"Refine composition and balance","body":"Use Touch Edit to dial in the details: adjust text sizes for each information tier, reposition images for better visual flow, increase white space around key elements for emphasis, tweak color contrast between text and background for readability, ensure your logo is prominent but not dominant. Good flyer design is mostly about getting the hierarchy right — everything else supports that."},{"title":"Add required elements","body":"Sponsor logos (describe where they should appear), QR codes (describe the linked URL and placement), legal disclaimers or terms (the AI places these legibly at the bottom), social media handles and website URL, event hashtags. Lovart integrates these naturally rather than pasting them on as afterthoughts."},{"title":"Export for your distribution method","body":"For professional printing: PDF/X with 0.125\" bleed, 300 DPI, CMYK — standard US letter (8.5\"×11\") or A4. For digital distribution: high-resolution PNG or JPEG optimized for screen viewing. For both: export print and digital versions from the same design — Lovart configures the technical settings for each output automatically."}],"ps_compare":[["Setting up document, grid, and guides","10-15 min","Automatic"],["Designing layout with visual hierarchy","45-90 min","3 min (describe)"],["Typography selection and refinement","20-40 min","Touch Edit: 2 min"],["Adding logos, QR codes, legal text","10-20 min","1-2 min (describe)"],["Creating print + digital versions","15-25 min","1 min each"],["Total estimated time","100-190 min","**10 minutes**"]]},
    {"design_type":"Social Media Banner","slug":"how-to-create-social-media-banners-without-photoshop","minutes":"5","tools":"A Lovart account, your brand assets (logo, colors, fonts — set up in Brand Kit), platform specifications (Facebook cover: 820×312px, LinkedIn banner: 1584×396px, YouTube banner: 2560×1440px with 1546×423px safe area, Twitter header: 1500×500px).","steps":[{"title":"Describe your platform and message","body":"Be specific about which platform and what you want to communicate: 'Create a Facebook cover banner for [brand]. Key message: [tagline or value proposition]. Include: our logo, website URL, brand tagline. Style: [professional/modern/bold/minimal]. Use our brand colors.' Mentioning the platform tells Lovart what dimensions and safe zones to respect."},{"title":"Review for composition and safe zones","body":"Social media banners have specific safe zones that vary by platform. Profile pictures overlay the bottom-left on Facebook. Channel icons overlay the center on YouTube. Navigation elements appear at the top on LinkedIn. Check: is your key message and logo within the safe area? Is the composition balanced despite the overlay zones? Does the banner communicate clearly at a glance?"},{"title":"Adjust for platform constraints","body":"Most banners are viewed at a distance — they're backdrops, not reading material. Key changes: move critical content into the safe zone (describe: 'shift the key message to the center-right area, leaving the bottom-left clear for the profile picture overlay'), ensure sufficient contrast against the background for readability, keep messaging concise — banners are glanced at, not studied."},{"title":"Generate platform variants from one design","body":"Once your Facebook cover is perfect, tell Lovart: 'Now create the same design for LinkedIn at 1584×396, YouTube at 2560×1440, and Twitter at 1500×500.' The AI intelligently adapts the composition for each format — repositioning elements, adjusting text sizes, and redistributing visual weight — rather than just cropping or stretching."},{"title":"Export at platform-native resolution","body":"Export as PNG for sharpest text rendering (JPEG can introduce compression artifacts around typography at banner sizes). Lovart configures exact pixel dimensions for each platform — no manual resizing, no accidentally exporting at the wrong resolution."}],"ps_compare":[["Setting up correct canvas size per platform","5-10 min","Automatic"],["Designing banner layout","30-60 min","2 min (describe)"],["Adjusting for safe zones and overlays","15-25 min","1 min (describe)"],["Creating platform-specific variants","20-40 min each","30 sec each"],["Exporting at correct specs per platform","5-10 min","1 click"],["Total estimated time","75-185 min","**5 minutes**"]]},
    {"design_type":"Product Label","slug":"how-to-create-product-labels-without-photoshop","minutes":"10","tools":"A Lovart account, your product information (product name, tagline, description, ingredients or features, net weight/volume), your brand identity (logo, colors, fonts in Brand Kit), label dimensions (measure your container), any required regulatory text (nutrition facts, warnings, certifications, barcode area).","steps":[{"title":"Describe your product and label requirements","body":"Be comprehensive: 'Design a product label for [product name], a [product type]. Container: [bottle/jar/box/pouch] measuring [width]×[height]. Include: product name (largest text), flavor/variant, tagline, net weight, ingredients/features list, our logo, barcode placeholder area. Style: [natural/premium/minimal/playful]. Colors: use our brand palette.'"},{"title":"Evaluate shelf impact","body":"Product labels are judged at arm's length on a crowded shelf. Key checks: is the product name readable from 3 feet away? Does the label stand out against typical competitor colors in your category? Is the visual hierarchy clear — product name dominates, variant/flavor secondary, details smaller? Is the barcode area accessible for scanning? Pick the composition with the strongest shelf presence."},{"title":"Refine for production quality","body":"Touch Edit critical details: adjust color contrast for shelf visibility, ensure font sizes meet readability standards at the label's actual physical size, verify that the barcode placeholder area has sufficient white space for scanning, confirm that regulatory text is legible (typically 6pt minimum), make sure the logo reproduction is crisp at the label's actual printed size."},{"title":"Add compliance and production elements","body":"Describe what's needed: 'Add a nutrition facts panel in the standard FDA format on the right side, include the USDA Organic certification logo, add a recycling symbol, include 'Made in [location]' text, and place a barcode placeholder on the bottom-right corner.' The AI places these elements naturally within the label composition rather than treating them as afterthoughts."},{"title":"Export for printing and preview on product","body":"Primary export: PDF/X with 0.125\" bleed, 300+ DPI, CMYK color profile — ready for any commercial label printer. Preview export: 'Now place this label design on a [bottle/jar/box] mockup so I can see how it looks on the actual product.' Lovart generates a 3D-context mockup showing your label in a realistic product setting — invaluable for stakeholder reviews and e-commerce product images."}],"ps_compare":[["Setting up label dimensions and bleeds","10-15 min","Automatic"],["Designing label layout with hierarchy","60-120 min","3 min (describe)"],["Typography and spacing refinement","30-45 min","Touch Edit: 2 min"],["Adding regulatory text and barcode","15-25 min","1-2 min (describe)"],["Creating 3D product mockup","30-60 min","2 min (describe)"],["Total estimated time","145-265 min","**10 minutes**"]]},
    {"design_type":"Event Ticket","slug":"how-to-create-event-tickets-without-photoshop","minutes":"8","tools":"A Lovart account, your complete event details (event name, date, time, venue name and address, ticket tier names and prices), your brand or event identity (logo, theme colors, any event-specific visual style), sponsor logos (if applicable), ticket dimensions (standard physical: 5.5\"×2\" with perforation; digital: mobile-optimized format).","steps":[{"title":"Describe your event and ticket design","body":"Provide all the context the AI needs: 'Design an event ticket for [event name] on [date] at [time], [venue name and address]. Ticket type: [General Admission / VIP / Early Bird / etc.]. Include: event name (largest), date and time, venue address, ticket tier label, price, barcode/QR placeholder, perforation line for physical tickets. Style: [elegant/bold/festival/minimal/edgy]. Use our event theme colors: [palette].'"},{"title":"Review for clarity and utility","body":"A ticket serves two masters: the attendee (who needs clear information) and the door staff (who needs quick scanning). Check: is the event name immediately clear? Can you find date, time, and venue in under 2 seconds? Is the ticket tier visually distinct (VIP shouldn't look identical to General Admission)? For physical tickets: is the perforation/tear line clearly indicated? For digital tickets: is the QR code prominently placed for quick scanning?"},{"title":"Refine information hierarchy and aesthetics","body":"Adjust: make the event name even more prominent (it's what people remember), ensure date/time/venue block is scannable as a unit, add event branding — illustrations, patterns, sponsor logos — that enhance the ticket as a keepsake (people save beautiful tickets), clean up the QR/barcode area with sufficient white space for reliable scanning, ensure the ticket tier label (VIP, GA, Early Bird) is visually coded for quick door verification."},{"title":"Create tier variations","body":"From one master design, generate all ticket tiers: 'Now create the VIP version — same layout but use gold accents instead of [base color], add a 'VIP ACCESS' badge, include any VIP-specific perks text.' Repeat for Early Bird, Student, Group, or any other tier. Each variant should be visually distinct at a glance while maintaining the event's overall visual identity."},{"title":"Export for distribution","body":"For physical tickets: PDF with bleed and crop marks, 300 DPI, CMYK — ready for any professional ticket printer. Include perforation marks in the design (the printer handles the physical perforation). For digital/email tickets: PNG or JPEG optimized for mobile viewing, typically 1200px wide, with a prominently placed QR code for door scanning."}],"ps_compare":[["Setting up ticket template with bleeds","10-15 min","Automatic"],["Designing ticket layout and composition","45-90 min","3 min (describe)"],["Creating tier variations (VIP, GA, etc.)","20-40 min each","1 min each (describe)"],["Adding QR code, perforation, legal text","10-20 min","1-2 min (describe)"],["Exporting print-ready and digital versions","10-15 min","1 click each"],["Total estimated time","95-260 min","**8 minutes**"]]}
]

T4 = [
    {"niche":"Bakery Owner","slug":"brand-kit-for-bakery-owners","colors":["Cream (#FFF8F0)","Warm Brown (#8B6914)","Golden Yellow (#F5A623)","Terracotta (#C4724F)"],"fonts":["Playfair Display (headings — elegant, timeless serif that communicates craftsmanship and quality)","Lato (body — clean, highly readable sans-serif that works beautifully at small sizes on ingredient lists and pricing)"],"palette_rationale":"Bakery branding succeeds when it triggers appetite and communicates freshness. This palette is built on the psychology of food presentation: cream provides a clean, wholesome foundation (the color of fresh dough and flour); warm brown evokes baked crust and artisanal craftsmanship; golden yellow stimulates appetite and suggests warmth (the color of perfectly baked pastry); and terracotta adds a rustic, handcrafted dimension that separates artisanal bakeries from industrial chains.","color_psychology":"Research in food psychology consistently shows that warm, earth-derived colors increase perceived flavor intensity and quality expectations. Bakeries using warm brown and cream palettes are rated as 'more authentic' and 'higher quality' in blind visual tests compared to bakeries using cool or bold colors. Golden yellow, specifically, triggers mild appetite stimulation — it's the color most associated with 'fresh from the oven' in consumer perception studies.","font1_rationale":"Playfair Display is a transitional serif with high contrast between thick and thin strokes. It communicates elegance without being cold — the slightly organic letterforms feel handcrafted, which aligns with the artisanal values that premium bakeries want to project. The distinctive character of Playfair means your bakery name becomes visually memorable, not just text.","font2_rationale":"Lato is a humanist sans-serif — clean and modern but with subtle warmth in its letterforms (slightly rounded terminals, open apertures). At small sizes on menu items and ingredient lists, it maintains excellent readability. The contrast between Playfair's elegance and Lato's clarity creates a sophisticated typographic pairing that feels intentional and professional.","templates":["Daily Menu & Specials Board — warm, rustic layout with handwritten-style accent elements, clear item categorization, and easy-to-scan pricing. Pre-configured with your brand colors and fonts so every daily update stays visually consistent with your overall bakery brand.","Seasonal Collection Promo — photography-forward template that lets your product images dominate. Minimal text overlay with your brand typography. Designed to showcase limited-edition pastries and seasonal offerings with the visual richness they deserve."],"template1_detail":"The daily menu is your bakery's most frequently updated and most frequently seen design asset. This template is pre-configured with your exact brand palette, correct font hierarchy, and a layout optimized for readability from 3-4 feet away (standard counter viewing distance). Item names are prominent, descriptions are supporting, prices are clearly aligned. The warm, rustic aesthetic reinforces your artisanal positioning with every menu update — no design effort required.","template2_detail":"Seasonal and limited-time offerings drive urgency and repeat visits, but they also create a design bottleneck — every new pastry collection needs promotional graphics. This template gives you a photography-first layout that makes your products the hero. Your brand elements (logo, colors, fonts) sit elegantly in supporting roles. Generate a new set of seasonal graphics in minutes — Valentine's Day, spring collection, summer fruit tarts, holiday cookie boxes — all visually consistent with your brand identity."},
    {"niche":"Beauty Salon Owner","slug":"brand-kit-for-beauty-salon-owners","colors":["Soft Blush (#F2D7D5)","Deep Charcoal (#2D2D2D)","Rose Gold (#B76E79)","Off-White (#FAFAFA)"],"fonts":["Cormorant Garamond (headings — refined, feminine serif with delicate contrast that communicates luxury and sophistication)","Montserrat (body — modern, geometric sans-serif with clean lines that balances the ornate heading with contemporary clarity)"],"palette_rationale":"Beauty salon branding must communicate luxury, cleanliness, and transformation. Soft blush creates warmth and approachability — it's the color of healthy, radiant skin and suggests the results clients are seeking. Deep charcoal provides sophistication and excellent contrast for text readability, grounding the palette in professionalism. Rose gold adds a premium, Instagram-worthy accent that signals trend-awareness and aspirational quality. Off-white provides a clean, clinical canvas that communicates hygiene and attention to detail.","color_psychology":"In beauty industry color psychology, blush and rose tones are consistently rated as 'most appealing' and 'most trustworthy' for salon branding. They suggest warmth, care, and expertise without the sterility of pure white or the aggression of bold reds. Rose gold, specifically, has become the luxury accent color of the 2020s beauty industry — it signals 'premium' and 'on-trend' more effectively than traditional gold or silver.","font1_rationale":"Cormorant Garamond is a display serif with dramatic contrast and elegant letterforms influenced by classic Garamond proportions. It signals refinement, tradition, and quality — the typographic equivalent of a well-appointed salon interior. The delicate hairlines and graceful curves feel specifically feminine without being stereotypical, communicating sophistication that appeals across demographics.","font2_rationale":"Montserrat brings modern structure and clarity. Its geometric precision balances Cormorant's ornate character, creating a pairing that feels intentional rather than accidental. At small sizes on service menus and price lists, Montserrat maintains flawless readability. The contrast between Cormorant's old-world elegance and Montserrat's contemporary clean lines tells the story of a salon that honors tradition while embracing modernity.","templates":["Service Menu & Price List — elegant, category-organized layout with generous white space, soft imagery, and clear pricing. Designed to feel like a luxury spa menu — reading it should feel like an experience in itself. Pre-configured with your brand palette and typography.","Instagram Promotion Template — beauty-optimized layout with soft filter effects, before/after transformation framing, and prominent booking call-to-action. Designed for the visual language of beauty Instagram — aspirational, polished, and conversion-focused."],"template1_detail":"Your service menu is both an information document and a sales tool. The layout guides clients through your offerings in a logical flow — hair services, nail services, skincare, packages — with each category visually distinct. Pricing is clear but never aggressive. The generous white space and soft color treatment create a spa-like reading experience that reinforces your premium positioning before a client ever books an appointment.","template2_detail":"Instagram is the primary discovery and booking channel for beauty businesses. This template is optimized for feed and Story formats, with pre-configured zones for before/after imagery, service highlights, and a prominent 'Book Now' call-to-action. The soft filter treatment and rose gold accents create a cohesive beauty-industry aesthetic that performs well in the Instagram algorithm and converts browsers to bookers."},
    {"niche":"Gym Owner","slug":"brand-kit-for-gym-owners","colors":["Deep Charcoal (#1A1A1A)","Electric Orange (#FF6B35)","Clean White (#FFFFFF)","Dark Navy (#1B2838)"],"fonts":["Bebas Neue (headings — bold, condensed, high-impact display font that commands attention and communicates strength)","Inter (body — modern, highly readable sans-serif optimized for screen and print at all sizes)"],"palette_rationale":"Gym branding needs to communicate energy, strength, and motivation. Deep charcoal provides a strong, serious foundation — it's the color of iron and intensity. Electric orange injects pure energy and urgency — it's the most attention-grabbing color in the spectrum and is strongly associated with action, movement, and motivation in sports psychology. Clean white creates crisp contrast for readability. Dark navy adds professional depth that elevates the palette beyond 'just a gym' to 'a fitness brand.'","color_psychology":"Sports psychology research consistently identifies orange as the color most associated with enthusiasm, energy, and action. It raises heart rate slightly and triggers a mild adrenaline response — exactly the physiological state you want potential clients to associate with your gym. Charcoal and navy ground the palette in seriousness and professionalism, preventing the orange from feeling gimmicky or discount-oriented.","font1_rationale":"Bebas Neue is a condensed, all-caps sans-serif designed for maximum impact at any size. It commands attention on social media, signage, and promotional materials — exactly what a gym brand needs. The condensed letterforms allow for large, powerful headlines that fill space with presence. It communicates strength, confidence, and no-nonsense intensity.","font2_rationale":"Inter is the most readable screen font available, designed specifically for optimal legibility at all sizes. On class schedules, membership forms, nutrition guides, and detailed content, Inter ensures information is processed quickly and accurately. The contrast between Bebas Neue's bold presence and Inter's quiet clarity creates a typographic system that handles both the motivational and the practical.","templates":["Class Schedule & Program Board — bold, high-contrast layout with clear time blocks, class type color coding, and instructor names. Designed for quick scanning in a gym environment — members can find their class in seconds from across the room.","Challenge & Transformation Campaign — high-energy promotional template with countdown elements, bold typography, before/after framing, and social-proof integration. Optimized for Instagram and Facebook conversion campaigns."],"template1_detail":"The class schedule is a gym's most operationally critical design. It needs to be scannable at a glance from across the room, clearly organized by day and time, with visual coding that distinguishes class types (HIIT vs yoga vs spin vs strength). This template handles all of that — pre-configured with your brand colors for class type coding and your brand typography for headers and details. Update it weekly in minutes.","template2_detail":"Fitness challenges and transformation programs are a gym's highest-converting campaigns, but they require coordinated visual launches: announcement, registration, countdown, daily motivation, celebration. This template gives you a complete campaign kit — generate the full set of graphics from a single description of your challenge, all visually consistent, all on-brand, all ready to schedule across social media and email."},
    {"niche":"Coffee Shop Owner","slug":"brand-kit-for-coffee-shop-owners","colors":["Espresso Brown (#3C2415)","Warm Cream (#F5F0E8)","Terracotta (#C67B5C)","Sage Green (#8B9A7E)"],"fonts":["Abril Fatface (headings — bold, distinctive, memorable display serif with dramatic contrast that commands attention)","Nunito (body — rounded, friendly, highly readable sans-serif with approachable warmth)"],"palette_rationale":"Coffee shop branding succeeds when it evokes the complete sensory experience — the warmth, the aroma, the comfort of a great coffee shop. Espresso brown anchors the palette in coffee authenticity — it's literally the color of the product. Warm cream provides a clean, inviting canvas (the color of steamed milk and latte art). Terracotta adds earthy warmth and visual interest without competing with the coffee tones. Sage green brings a fresh, natural accent that suggests quality ingredients and a connection to origin.","color_psychology":"Third-wave coffee culture has established brown-and-cream as the premium coffee aesthetic — it signals craft, origin-consciousness, and quality over convenience. Terracotta adds warmth that makes the palette feel lived-in and welcoming (important for encouraging dwell time). Sage green introduces a natural element that appeals to the sustainability-conscious demographic that overlaps heavily with specialty coffee consumers.","font1_rationale":"Abril Fatface is a dramatic display serif inspired by 19th-century advertising typography. Its extreme contrast and distinctive character make your coffee shop name instantly recognizable and memorable. It commands attention on signage and social media — exactly what a coffee shop needs in a competitive high-street environment. The bold presence signals confidence and established quality.","font2_rationale":"Nunito is a rounded sans-serif with friendly, approachable character. Its soft terminals and open letterforms create a warm reading experience — appropriate for a coffee shop's menu, where customers should feel welcomed, not lectured. At small sizes on drink descriptions and pricing, Nunito maintains excellent readability while contributing to the overall friendly, inviting brand personality.","templates":["Daily Menu & Specials Board — warm, chalkboard-inspired layout with drink categorization (espresso, pour-over, seasonal, tea, food), clear pricing, and a designated daily specials zone. Designed to feel handmade and personal while maintaining professional structure. Pre-configured with your brand palette and typography.","Loyalty Card & Stamp Design — clean, wallet-friendly layout with clear stamp positions, reward messaging, and subtle brand elements. Designed to be elegant enough that customers want to carry it, not lose it in a drawer."],"template1_detail":"A coffee shop menu needs to communicate a lot of information quickly — drink types, sizes, milk options, prices — while maintaining a warm, inviting aesthetic. This template balances information density with visual warmth. The chalkboard-inspired design language signals craft and personality. The pre-configured brand elements ensure that even daily handwritten-style specials boards feel like part of your overall visual identity.","template2_detail":"Loyalty programs work when the card is attractive enough to keep. A well-designed loyalty card lives in a customer's wallet and creates a small brand impression every time they open it. This template balances clean functionality (clear stamp positions, reward tiers) with aesthetic appeal (your brand colors and typography, subtle coffee-themed illustration accents). Generate new designs for seasonal promotions or special reward events in minutes."},
    {"niche":"Real Estate Agent","slug":"brand-kit-for-real-estate-agents","colors":["Navy Blue (#1B365D)","Gold (#C99700)","Clean White (#FFFFFF)","Warm Gray (#8B8581)"],"fonts":["Georgia (headings — classic, trustworthy serif with excellent screen readability and established professional credibility)","Open Sans (body — clean, neutral, highly legible sans-serif that supports information-dense content)"],"palette_rationale":"Real estate branding hinges entirely on trust. Navy blue is the most trusted color in brand psychology — it communicates stability, professionalism, and reliability across all cultures and demographics. Gold accents signal success and premium service without appearing ostentatious. Clean white ensures property details and listing information are crystal clear. Warm gray provides a sophisticated neutral that supports the palette without competing — it's the color of professional photography backdrops and luxury property staging.","color_psychology":"In real estate specifically, blue-based palettes are associated with higher perceived property values in consumer testing. Properties marketed with blue-dominant branding are estimated at 5-8% higher value than identical properties marketed with red or green branding. Gold accents add a success-signaling dimension — they communicate 'this agent closes deals' — without the aggressive associations of brighter metallics.","font1_rationale":"Georgia was designed specifically for clarity and elegance on screens. It's the most trusted serif font in professional communications — widely used in legal, financial, and real estate contexts. It communicates established credibility without feeling dated. The slightly generous letter spacing and open counter forms ensure excellent readability on signage, listing sheets, and digital displays.","font2_rationale":"Open Sans is the industry standard for clean, neutral body text. It doesn't call attention to itself — it serves the content. On listing descriptions, market reports, and contract summaries where information accuracy is paramount, Open Sans ensures clarity without visual distraction. The pairing with Georgia creates a typographic system that balances warmth (Georgia's humanist serifs) with professionalism (Open Sans' neutral clarity).","templates":["Property Listing Flyer — premium layout with hero property image, key details sidebar (beds, baths, sq ft, price), property highlights section, and prominent agent contact block with photo. Designed to feel like a luxury property brochure, not a template printout. Pre-configured with your brand palette and typography.","Just Listed / Just Sold Social Post — celebration-optimized template with prominent status badge (JUST LISTED or SOLD), property image, key stats callout, and agent branding. Designed for high engagement on Instagram and Facebook — the visual language of real estate social media success."],"template1_detail":"The listing flyer is an agent's most important printed asset — it's the physical representation of your service quality that potential sellers evaluate. This template prioritizes property photography with a clean, magazine-layout approach. Key details are immediately scannable. Your personal branding (photo, contact info, logo) is prominent but never dominant — the property is the hero, and your branding supports it professionally.","template2_detail":"Social media is where real estate agents build their personal brand and generate leads. The 'Just Listed' and 'Just Sold' posts are the highest-performing content formats in real estate social media. This template is optimized for both: bold status badges that stop the scroll, property images that showcase your listings, stat callouts that demonstrate market knowledge, and consistent agent branding that builds recognition across every post."}
]

# ═══════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════
count = 0
total_words = 0

for cat, func, name_key, data in [
    ("T1-Best-Agent", gen_t1, "niche", T1),
    ("T2-Chat-Generate", gen_t2, "design_type", T2),
    ("T3-No-Photoshop", gen_t3, "design_type", T3),
    ("T4-Brand-Kit", gen_t4, "niche", T4),
]:
    for item in data:
        path = os.path.join(BASE, cat, f"{item['slug']}.md")
        content = func(item)
        with open(path, 'w') as f:
            f.write(content)
        wc = len(content.split())
        total_words += wc
        count += 1
        name = item.get(name_key, item.get('niche', ''))
        print(f"  [{cat.split('-')[0]}] {item['slug']}.md — ~{wc} words ({name})")

print(f"\n✅ {count} pages regenerated")
print(f"   Total: ~{total_words} words")
print(f"   Average: ~{total_words//count} words/page")
print(f"   Range: {min(len(gen_t1(T1[0]).split()), len(gen_t2(T2[0]).split()), len(gen_t3(T3[0]).split()), len(gen_t4(T4[0]).split()))}–{max(len(gen_t1(T1[0]).split()), len(gen_t2(T2[0]).split()), len(gen_t3(T3[0]).split()), len(gen_t4(T4[0]).split()))} words")
