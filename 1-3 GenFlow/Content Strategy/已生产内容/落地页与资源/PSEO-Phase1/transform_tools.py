#!/usr/bin/env python3
"""KR2 Tools Phase 1: Transform existing Landing pages into /tools/ SEO format."""
import os, re, json

SRC = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-3 Content Gen/Content Strategy/已生产内容/落地页与资源/01-Core-Pages")
DST = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-3 Content Gen/Content Strategy/已生产内容/落地页与资源/PSEO-Phase1/Tools-Phase1")
os.makedirs(DST, exist_ok=True)

# ── Tool metadata: slug, tool name, category, comparison competitors ──
TOOLS = [
    {
        "file": "05-core-page-ai-mockup-generator.md",
        "slug": "ai-mockup-generator",
        "name": "AI Mockup Generator",
        "category": "Mockup & Presentation",
        "short_desc": "Place designs in photorealistic real-world scenes in seconds",
        "competitors": [
            ("Canva Smartmockups", "Template-based, limited scene library, manual placement", "AI-powered scene understanding, auto perspective/lights/shadows, unlimited custom scenes"),
            ("Placeit", "Good device mockups, fixed templates, repetitive look", "Any product category, dynamic scene generation, commercial 4K output"),
            ("Photoshop (manual compositing)", "Full control, steep learning curve, 30-90 min per mockup", "Describe scene in plain language, 15 seconds generation, Touch Edit to refine")
        ]
    },
    {
        "file": "04-core-page-ai-banner-maker.md",
        "slug": "ai-banner-maker",
        "name": "AI Banner Maker",
        "category": "Advertising & Marketing",
        "short_desc": "Generate platform-optimized banners for ads, web, and social",
        "competitors": [
            ("Canva Banner Templates", "Large template library, recognizable designs, manual resizing per platform", "Original AI-composed designs, auto-generate all platform variants, Brand Kit enforces consistency"),
            ("Adobe Express", "Professional tooling, Creative Cloud integration, moderate learning curve", "Natural language generation, Touch Edit for targeted refinement, zero learning curve"),
            ("BannerSnack / Creatopy", "Ad-specific features, limited AI capabilities, template-heavy output", "Full AI design agent, export in all ad platform specs, batch generation for campaigns")
        ]
    },
    {
        "file": "03-core-page-ai-poster-generator.md",
        "slug": "ai-poster-maker",
        "name": "AI Poster Maker",
        "category": "Print & Display",
        "short_desc": "Design print-ready posters and flyers with AI composition",
        "competitors": [
            ("Canva Poster Templates", "Extensive library, limited originality, print export requires manual CMYK setup", "AI-composed originals, automatic print-ready export (PDF/X, CMYK, bleed), any style on demand"),
            ("Adobe Illustrator/Photoshop", "Industry standard, full creative control, steep learning curve, 60-120 min per poster", "Natural language generation, 2-5 min per poster, professional print specs automatic"),
            ("PosterMyWall", "Poster-specific, template-heavy, limited AI features, lower design quality ceiling", "AI design agent with professional typography, batch event poster generation, brand consistency")
        ]
    },
    {
        "file": "01-core-page-ai-flyer-maker.md",
        "slug": "ai-flyer-maker",
        "name": "AI Flyer Maker",
        "category": "Print & Display",
        "short_desc": "Create event, promotion, and business flyers in minutes",
        "competitors": [
            ("Canva Flyer Templates", "Good for quick flyers, template recognition issue, manual text adjustment", "AI-designed originals, auto text hierarchy, print-ready with bleed marks in one click"),
            ("Adobe InDesign", "Professional print layout, steep learning curve, time-intensive per flyer", "Describe flyer purpose → AI generates in 2 min, edit with Touch Edit, export PDF/X instantly"),
            ("Vistaprint Design Studio", "Integrated with printing, limited design flexibility, template-dependent", "Professional design quality, export for any printer, Brand Kit auto-applied")
        ]
    },
    {
        "file": "02-core-page-ai-menu-design.md",
        "slug": "ai-menu-maker",
        "name": "AI Menu Maker",
        "category": "Food & Hospitality",
        "short_desc": "Generate restaurant menus, cafe boards, and QR digital menus",
        "competitors": [
            ("Canva Menu Templates", "Good starting layouts, recognizable as templates, manual update per menu change", "Original designs per cuisine type, daily update in 2 min via chat, print + digital dual export"),
            ("MustHaveMenus / iMenuPro", "Restaurant-specific features, dated design aesthetics, subscription cost", "Modern AI-designed menus, multi-cuisine style intelligence, free tier available"),
            ("Hiring a menu designer", "Professional, custom, $200-500 per menu, 1-2 week turnaround", "$19/month for unlimited menus, instant updates, seasonal menu variants in seconds")
        ]
    },
    {
        "file": "03-core-page-ai-business-card.md",
        "slug": "ai-business-card-maker",
        "name": "AI Business Card Maker",
        "category": "Brand Identity",
        "short_desc": "Design professional business cards with AI typography and layout",
        "competitors": [
            ("Canva Business Card Templates", "Many template options, standard quality, generic feel across users", "AI-designed unique compositions, industry-specific style intelligence, print-ready with bleed"),
            ("Vistaprint / Moo Designer", "Integrated with printing, templated designs, limited customization", "Full creative freedom via AI, export for any printer, Brand Kit auto-applied"),
            ("Adobe Illustrator", "Maximum design control, professional output, 45-90 min per card design", "2 min via natural language, Touch Edit for refinement, print specs automatic")
        ]
    },
    {
        "file": "03-core-page-ai-infographic.md",
        "slug": "ai-infographic-maker",
        "name": "AI Infographic Maker",
        "category": "Data & Content",
        "short_desc": "Turn data and ideas into visual infographics with AI layout",
        "competitors": [
            ("Canva Infographic Templates", "Good for simple infographics, limited data visualization, template recognition", "AI data-to-visual intelligence, custom visual style per topic, original compositions"),
            ("Piktochart / Venngage", "Infographic-focused, template-driven, moderate learning curve, subscription required", "Natural language → infographic in 2 min, data auto-visualized, free tier available"),
            ("PowerPoint / Google Slides (manual)", "Familiar tools, not designed for infographics, time-intensive layout work", "Purpose-built AI infographic engine, professional data visualization, export in all formats")
        ]
    },
    {
        "file": "S2-ai-photo-enhancer-core-page.md",
        "slug": "ai-photo-enhancer",
        "name": "AI Photo Enhancer",
        "category": "Image Editing",
        "short_desc": "Enhance photo quality, resolution, and clarity with one click",
        "competitors": [
            ("Let's Enhance / Topaz", "Good enhancement quality, separate tool subscription, batch processing limited", "Integrated in design workflow, enhance→edit→export in one platform, free tier available"),
            ("Adobe Photoshop (manual)", "Professional tools, time-intensive per photo, requires expertise", "One-click AI enhancement, batch process 100 photos, auto color/lighting correction"),
            ("Remini / AI enhancer apps", "Mobile-friendly, good for portraits, limited professional output control", "Professional 4K output, preserve original details, export in production formats")
        ]
    },
    {
        "file": "S3-image-upscaler-core-page.md",
        "slug": "ai-image-upscaler",
        "name": "AI Image Upscaler",
        "category": "Image Editing",
        "short_desc": "Upscale images to 4K/8K with AI detail preservation",
        "competitors": [
            ("Topaz Gigapixel", "Best-in-class upscaling quality, standalone tool, $99 one-time or subscription", "Integrated design workflow, upscale→edit in one platform, included in Lovart subscription"),
            ("Waifu2x / Real-ESRGAN", "Free open-source, good for anime/illustrations, requires technical setup", "One-click web-based, professional output, works on all image types including photos"),
            ("Adobe Photoshop Super Resolution", "Good quality, requires Camera Raw workflow, manual per-image process", "Batch upscale 100+ images, direct to 4K/8K export, integrated with design editing")
        ]
    },
    {
        "file": "03-core-page-ai-avatar-generator.md",
        "slug": "ai-avatar-generator",
        "name": "AI Avatar Generator",
        "category": "Image Generation",
        "short_desc": "Generate professional AI avatars and profile pictures",
        "competitors": [
            ("DALL-E / Midjourney (avatars)", "High-quality image generation, no avatar-specific optimization, requires prompt expertise", "Avatar-specific AI pipeline, consistent face identity, multiple style presets"),
            ("Avatar AI apps (Lensa, etc.)", "Good for stylized portraits, limited professional use cases, privacy concerns", "Professional avatar generation, business-appropriate styles, full commercial rights"),
            ("Hiring a photographer", "Highest quality, $200-500 per session, scheduling complexity", "Instant generation, unlimited variations, $19/month for unlimited avatars")
        ]
    },
]

def add_comparison_section(content, tool):
    """Add 'Lovart vs Alternatives' comparison table before FAQ section."""
    comp_rows = "\n".join([
        f"| **{comp[0]}** | {comp[1]} | **{comp[2]}** |"
        for comp in tool['competitors']
    ])
    
    comparison_block = f"""---

## Lovart vs Alternatives for {tool['category']}

Not all design tools are built the same. Here's how Lovart's {tool['name']} compares to the alternatives you might be considering:

| Tool | Limitations | Lovart Advantage |
|------|------------|-----------------|
{comp_rows}

**Bottom line:** Lovart is purpose-built for speed — describe what you need in plain language, and the AI generates professional, on-brand results in seconds. No templates. No learning curve. No waiting for a freelancer. And every design you create belongs to you with full commercial rights.

"""

    # Insert before FAQ section (find the last ## FAQ or ## Frequently Asked Questions)
    faq_patterns = [
        r'\n## Frequently Asked Questions\n',
        r'\n## FAQ\n',
        r'\n---\n\n## Frequently Asked Questions\n',
    ]
    
    for pattern in faq_patterns:
        match = re.search(pattern, content)
        if match:
            return content[:match.start()] + comparison_block + content[match.start():]
    
    # If no FAQ section found, append at end
    return content + "\n" + comparison_block

def add_faqpage_schema(content, tool):
    """Add FAQPage JSON-LD structured data after frontmatter."""
    # Extract FAQ questions from content
    faq_qa = re.findall(r'### (.*?)\n\n(.*?)(?=\n### |\n---\n|\n\[|\n$)', content, re.DOTALL)
    
    if not faq_qa:
        faq_qa = re.findall(r'\*\*(.*?)\*\*\n\n(.*?)(?=\n\*\*|\n---|\n$)', content, re.DOTALL)
    
    if not faq_qa or len(faq_qa) < 3:
        # Fallback: use generic FAQ
        faq_qa = [
            ("Can I use the designs commercially?", "Yes. Every design, image, and asset you create with Lovart belongs to you with full commercial rights. Use them on your website, in ads, on products, for client work — no attribution required."),
            ("Do I need design experience to use this?", f"No. Lovart is built for non-designers. Describe what you want in plain language, and the AI Design Agent handles composition, typography, color selection, and export settings automatically."),
            (f"How is Lovart's {tool['name']} different from other tools?", f"Unlike Canva (template-based), Midjourney (image-only, no design editing), or hiring a freelancer (slow, expensive), Lovart is an AI Design Agent — it creates original designs from your description, lets you edit specific elements with Touch Edit, maintains brand consistency via Brand Kit, and exports in professional formats."),
            ("Can I try it for free?", "Yes. Lovart's Free plan gives you 50 designs per month across 5 AI models. No credit card required. Upgrade to Starter ($19/month) for 500 designs, HD export, and Brand Kit."),
            ("What formats can I export to?", "Lovart exports in PNG, JPEG, SVG, PDF (with bleed, CMYK, 300 DPI for print), PSD, and platform-specific optimized formats for social media, web, and advertising platforms."),
        ]
    
    # Build FAQPage JSON-LD
    entities = []
    for q, a in faq_qa[:6]:  # Max 6 FAQ items
        q_clean = q.strip().rstrip('?').strip()
        if not q_clean or len(q_clean) < 5:
            continue
        a_clean = a.strip()[:500]  # Google limit ~500 chars per answer
        # Remove markdown formatting
        a_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', a_clean)
        a_clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', a_clean)
        entities.append({
            "@type": "Question",
            "name": q_clean + "?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a_clean
            }
        })
    
    if len(entities) < 3:
        return content  # Not enough FAQ to warrant Schema
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    
    faqpage_ld = f"""<script type="application/ld+json">
{json.dumps(schema, indent=2, ensure_ascii=False)}
</script>

"""
    
    # Insert after first </script> (which should be the WebPage Schema)
    first_script_end = content.find('</script>')
    if first_script_end >= 0:
        insert_at = first_script_end + len('</script>') + 1
        return content[:insert_at] + "\n" + faqpage_ld + content[insert_at:]
    
    # Fallback: insert after frontmatter
    fm_end = content.find('---', 3)
    if fm_end >= 0:
        return content[:fm_end+3] + "\n" + faqpage_ld + "\n" + content[fm_end+3:]
    
    return faqpage_ld + content

def optimize_frontmatter(content, tool):
    """Update frontmatter with Tools-optimized TDK and slug."""
    # Update title to tools format: "Free AI [Tool] — [Value Proposition] | Lovart"
    new_title = f"Free {tool['name']} — {tool['short_desc']} | Lovart"
    
    # Update keywords
    new_keywords = f"free {tool['slug'].replace('-',' ')}, {tool['name'].lower()}, ai {tool['category'].lower().replace('&','').replace('  ',' ')} tool, online {tool['slug'].replace('-',' ')}, {tool['slug'].replace('-',' ')} free"
    
    # Update slug to /tools/ format
    new_slug = tool['slug']
    
    # Update page_type
    new_page_type = "Tool Landing Page"
    
    # Update category
    new_category = tool['category']
    
    content = re.sub(r'title: ".*?"', f'title: "{new_title}"', content)
    content = re.sub(r'slug: ".*?"', f'slug: "{new_slug}"', content)
    content = re.sub(r'page_type: ".*?"', f'page_type: "{new_page_type}"', content)
    content = re.sub(r'category: ".*?"', f'category: "{new_category}"', content)
    
    # Update or add target_keywords
    if 'target_keywords:' in content:
        content = re.sub(r'target_keywords: ".*?"', f'target_keywords: "{new_keywords}"', content)
    else:
        # Add after category line
        content = content.replace(
            f'category: "{new_category}"',
            f'category: "{new_category}"\ntarget_keywords: "{new_keywords}"'
        )
    
    # Add tool metadata to frontmatter
    if 'tool_name:' not in content:
        content = content.replace(
            f'category: "{new_category}"',
            f'category: "{new_category}"\ntool_name: "{tool["name"]}"'
        )
    
    return content

def update_url_in_schema(content, tool):
    """Update the WebPage Schema URL to /tools/ path."""
    new_url = f"https://www.lovart.ai/tools/{tool['slug']}"
    content = re.sub(
        r'"url": "https://www\.lovart\.ai/[^"]*"',
        f'"url": "{new_url}"',
        content
    )
    return content

# ── Main ──
count = 0
for tool in TOOLS:
    src_path = os.path.join(SRC, tool['file'])
    
    # Handle missing file (avatar generator)
    if not os.path.exists(src_path):
        # Try alternative paths
        alt_paths = [
            os.path.join(SRC, tool['file'].replace('.md', '-lp.md')),
            os.path.join(SRC, f"b9-{tool['file']}"),
        ]
        found = False
        for ap in alt_paths:
            if os.path.exists(ap):
                src_path = ap
                found = True
                break
        if not found:
            print(f"  ⚠️  SKIP: {tool['file']} — file not found, need to create from scratch")
            continue
    
    with open(src_path) as f:
        content = f.read()
    
    orig_words = len(content.split())
    
    # Apply transformations
    content = optimize_frontmatter(content, tool)
    content = update_url_in_schema(content, tool)
    content = add_faqpage_schema(content, tool)
    content = add_comparison_section(content, tool)
    
    new_words = len(content.split())
    
    dst_path = os.path.join(DST, f"{tool['slug']}.md")
    with open(dst_path, 'w') as f:
        f.write(content)
    
    count += 1
    print(f"  ✅ {tool['slug']}.md — {orig_words} → {new_words} words (+{new_words-orig_words})")

print(f"\n✅ {count} tools pages transformed")
print(f"   Output: {DST}/")
