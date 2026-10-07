#!/usr/bin/env python3
"""Expand all 19 new Tools pages with richer content sections to reach 1500-2000+ words."""
import os, re

DST = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-3 Content Gen/Content Strategy/已生产内容/落地页与资源/PSEO-Phase1/Tools-Phase1")

EXPANSIONS = {
    "nano-banana": {
        "why_section": """## Why Nano Banana Pro Changes the Design Economics

The traditional design workflow for a small business looks like this: identify a design need → brief a freelancer ($50-150) → wait 2-5 days → review drafts → request revisions ($25-75) → wait 1-2 more days → receive final files. Total cost per design: $75-225. Total time: 3-7 days. Total designs per month before budget runs out: 4-8.

With Nano Banana Pro inside Lovart: describe your design need in plain language → AI generates professional designs in seconds → refine with Touch Edit → export in production format. Total cost: effectively zero (included in $19/month). Total time: 2-5 minutes. Total designs per month: unlimited (500 on Starter, 2,000 on Professional).

This isn't incremental improvement. It's a step-change in design economics. When design becomes essentially free and instant, the question shifts from "which designs can I afford?" to "which designs will drive the most business value?" That's the real transformation Nano Banana Pro enables.""",
        "extra_use_case": """### Batch Content Production for Social Media

Social media managers and content creators face a constant content treadmill: you need fresh, on-brand visuals every single day across multiple platforms. Nano Banana Pro's batch generation capability lets you describe a week's or month's worth of content themes, and the AI produces coordinated visual sets — all consistent with your Brand Kit, all correctly sized for each platform, all ready to schedule. What used to consume 10-15 hours per week of manual design work now takes 30-45 minutes of describing and reviewing."""
    },
    "veo-3": {
        "why_section": """## Why Veo 3 Changes Video Production Economics

Traditional video production follows a well-known cost curve. A 15-second product video: $500-2,000. A 30-second social media ad: $1,000-5,000. A 60-second brand film: $5,000-25,000. These costs aren't arbitrary — they reflect real expenses: equipment, crew, location, editing, color grading, sound design, revisions.

Veo 3 inside Lovart doesn't just reduce these costs — it eliminates the cost barrier entirely. Describe your video in plain language. The AI generates it in minutes. Refine with Touch Edit. Export in platform-optimized format. All included in your Lovart subscription.

But the more important shift is creative velocity. When producing a video takes a week and costs $1,000, you produce one version and hope it converts. When producing a video takes 5 minutes and costs nothing incremental, you produce 10 versions and test which performs best. Your first version is rarely your best version — but without Veo 3, you never had the chance to find out.""",
        "extra_use_case": """### E-commerce Product Video at Scale

E-commerce sellers know that product videos increase conversion — Amazon reports up to 80% higher conversion on listings with video. But producing professional video for every SKU in a 100-product catalog is economically impossible with traditional production. Veo 3 changes this: generate platform-optimized product videos for your entire catalog from product descriptions and reference photos. A 15-second product rotation video for each SKU — consistent quality, consistent branding, zero per-SKU production cost."""
    },
    "sora-2": {
        "why_section": """## The Cinematic Quality Gap — and Why Sora 2 Closes It

Until recently, AI-generated video had a tell. Sometimes it was unnatural motion. Sometimes objects that appeared and disappeared between frames. Sometimes lighting that shifted for no reason. The output was impressive — but it looked AI-generated.

Sora 2 changes this. Its output is often indistinguishable from professionally shot footage. Shadows track with light sources. Reflections behave correctly. Objects maintain consistent appearance. Motion follows physics. For brands that need video that builds trust rather than raises questions about authenticity, Sora 2 represents a threshold moment — the point where AI video quality crosses into professional production territory.

Inside Lovart, Sora 2 gains the workflow capabilities it lacks as a standalone model. Touch Edit for targeted refinement. Brand Kit for visual consistency. Multi-format export for every platform. Timeline editing for clip combination. The result: cinematic-quality video, produced in minutes, branded and exported in one workflow.""",
        "extra_use_case": """### Establishing Shots and B-Roll for Brand Films

Brand films need atmosphere — sweeping drone shots of locations, establishing shots that set mood, B-roll that fills narrative gaps. Traditionally, this means location scouting, permitting, crew coordination, and expensive footage that may only appear for 3-5 seconds in the final edit. Sora 2 generates custom establishing shots and B-roll from text descriptions — no location costs, no permits, no crew. Describe the scene you need, and Sora 2 produces cinematic footage that integrates seamlessly with your existing video content."""
    },
    "kling-ai": {
        "why_section": """## Motion Quality: The Underrated Differentiator

Most people evaluating AI video models focus on image quality — how sharp, how detailed, how realistic each frame looks. But video isn't a sequence of still frames. Video is motion. And motion quality — how naturally things move, how physics-aware the animation is, how fluid the transitions feel — is where the real differences between models emerge.

Kling AI's motion quality is its defining advantage. Walking looks like walking, not gliding. Gestures feel natural, not robotic. Camera movements have motivation and weight. Objects interact with their environment rather than floating through it. For content that needs to feel alive — fitness demonstrations, fashion content, action sequences, lifestyle scenarios — motion quality is the difference between engaging and uncanny.

Having Kling AI alongside Veo 3 and Sora 2 in Lovart means you're never locked into one model's strengths and weaknesses. Cinematic establishing shot? Sora 2. Polished product showcase? Veo 3. High-energy social content? Kling AI. Three models, one platform, choose the right tool for every shot.""",
        "extra_use_case": """### Fashion and Lifestyle Content Creation

Fashion brands and lifestyle creators need content that moves — models walking, fabric flowing, accessories catching light, lifestyle scenarios that feel authentic. Kling AI's motion quality makes it particularly well-suited for fashion content, where unnatural movement immediately signals "AI-generated" and undermines brand credibility. Upload reference images of garments or accessories, describe the scene and motion, and Kling AI produces natural-feeling fashion content ready for social media and e-commerce."""
    }
}

# Generic expansions for remaining 15 tools
GENERIC_EXPANSIONS = {
    "why_section": """## Why This Tool Changes Your Workflow

Every design tool promises to save time. But most tools simply shift where the time is spent — from one complex software to another, from one workflow bottleneck to another. Lovart's approach is fundamentally different: eliminate the bottleneck entirely.

Traditional workflow: open software, set up document, configure settings, build layout, adjust typography, export (hope settings are correct), realize something is wrong, start over. Time: 30-90 minutes. Skill required: moderate to high.

Lovart workflow: describe what you need in plain language, review AI-generated options, refine with Touch Edit, export in correct format. Time: 2-5 minutes. Skill required: none — you already know how to describe what you want.

This isn't about making design slightly faster. It's about making design accessible to the 94% of people who need professional visual output but aren't professional designers. When design stops being a specialized skill and becomes a capability anyone can access, the bottleneck isn't just reduced — it disappears.""",
    "extra_use_case": """### Team and Client Collaboration

For agencies, marketing teams, and businesses with multiple stakeholders, design projects typically involve rounds of feedback, revision requests, and version management. Lovart's approach transforms this process: instead of "send me the revised file," it becomes "let me show you the variation you described." Generate multiple versions in seconds. Refine based on feedback in real time. Export the approved version immediately. What used to be a multi-day revision cycle becomes a 5-minute collaborative session."""
}

def expand_page(filepath, slug):
    with open(filepath) as f:
        content = f.read()
    
    orig_words = len(content.split())
    exp = EXPANSIONS.get(slug, GENERIC_EXPANSIONS)
    
    # Find insertion point: after the intro paragraph(s), before ## How... or first ##
    # We want to insert the "Why" section after the intro text but before the first H2
    first_h2 = re.search(r'\n## ', content)
    if not first_h2:
        return orig_words
    
    insert_at = first_h2.start()
    
    # Insert the "Why" section
    why_block = f"\n{exp['why_section']}\n"
    content = content[:insert_at] + why_block + content[insert_at:]
    
    # Insert extra use case before the comparison table
    comp_match = re.search(r'\n## .*Compared to Alternatives\n', content)
    if not comp_match:
        comp_match = re.search(r'\n## .*vs Alternatives\n', content)
    if comp_match:
        uc_block = f"\n{exp['extra_use_case']}\n\n---\n"
        content = content[:comp_match.start()] + uc_block + content[comp_match.start():]
    
    new_words = len(content.split())
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return orig_words, new_words

count = 0
total_before = 0
total_after = 0

for fname in sorted(os.listdir(DST)):
    if not fname.endswith('.md'):
        continue
    slug = fname.replace('.md', '')
    filepath = os.path.join(DST, fname)
    before, after = expand_page(filepath, slug)
    total_before += before
    total_after += after
    count += 1
    print(f"  {slug}: {before} → {after} words (+{after-before})")

print(f"\nExpanded {count} pages: {total_before} → {total_after} words (+{total_after-total_before})")
print(f"Average: {total_before//count} → {total_after//count} words")
