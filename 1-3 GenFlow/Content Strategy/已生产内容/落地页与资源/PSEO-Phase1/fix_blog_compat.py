#!/usr/bin/env python3
"""Fix 158 PSEO/Tools pages for Blog LOCAL-SPEC compliance."""
import os, re, json, hashlib, glob

BASE = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-3 Content Gen/Content Strategy/已生产内容/落地页与资源/PSEO-Phase1")
AUTHOR = "Lovart Content Team"
DATE = "2026-07-15"

# ── Cover pool ──
POOL_PATH = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-6 Knowledge Base/Cover Url 随机调取.md")
with open(POOL_PATH) as f:
    pool_text = f.read()
COVER_POOL = list(set(re.findall(r'https://liblibai-online\.liblib\.cloud/blog-card-cover/\d+\.png', pool_text)))
print(f"Cover pool: {len(COVER_POOL)} URLs")

def pick_cover(slug):
    digest = hashlib.sha256(slug.encode()).hexdigest()
    return COVER_POOL[int(digest[:8], 16) % len(COVER_POOL)]

# ── Category mapping ──
# Sanity 12 legal categories:
# AI Image Tools, AI Video Tools, Best Practice, Branding, How-To,
# Insight & Trend, Lovart 101, Industry Solution, Customer Story, News, Pillar, Cluster
CAT_MAP = {
    "Best AI Design Agent": "Industry Solution",
    "Segment Landing Page": "Industry Solution",
    "How-To Detail Page": "How-To",
    "How-To": "How-To",
    "Tutorial Detail Page": "How-To",
    "Tutorial": "How-To",
    "Best Practice Detail Page": "Best Practice",
    "Best Practice": "Best Practice",
    "Brand Kit": "Branding",
    "Brand Identity": "Branding",
    "Tool Landing Page": "AI Image Tools",
    "Image Editing": "AI Image Tools",
    "Image Generation": "AI Image Tools",
    "AI Image Model": "AI Image Tools",
    "AI Video Model": "AI Video Tools",
    "Social Media": "How-To",
    "Content Creation": "How-To",
    "E-commerce": "Industry Solution",
    "Design Resources": "Best Practice",
    "Advertising & Marketing": "Industry Solution",
    "Print & Display": "How-To",
    "Food & Hospitality": "Industry Solution",
    "Data & Content": "How-To",
    "Mockup & Presentation": "AI Image Tools",
}

def map_category(cat):
    return CAT_MAP.get(cat, "How-To")  # default to How-To

# ── E-E-A-T signals block ──
EEAT_BLOCK = """

---

## Why Lovart's AI Design Agent Approach Matters

What separates Lovart from template-based tools and generic AI image generators is its underlying architecture. The **MCoT Engine (Mind Chain of Thought)** doesn't just generate images — it reasons about design context, audience intent, brand requirements, and production specifications before producing output. **ChatCanvas** turns the generation process into a collaborative conversation rather than a one-shot prompt. **Touch Edit** lets you refine specific elements without regenerating from scratch — the difference between directing a design process and gambling on image generation. And the **Brand Kit** ensures every output automatically inherits your brand colors, fonts, and logo — eliminating the consistency tax that makes most AI-generated content feel like it came from different sources.

These aren't feature bullet points. They're the architectural differences that make Lovart an AI Design Agent rather than an AI image generator. When you describe what you need, you're not prompting — you're directing. The AI doesn't just produce — it designs. This distinction is what makes professional, commercially usable output possible for the 94% of users who need design quality without design expertise.

"""

# ── Cluster footer ──
CLUSTER_FOOTER = """

---

## Explore More Lovart Resources

- **[How to Get Started with Lovart's AI Design Agent](https://www.lovart.ai/blog/lovart-getting-started)** — Your first design in under 5 minutes
- **[Lovart Pricing: Which Plan Is Right for You?](https://www.lovart.ai/pricing)** — Compare plans and features
- **[Lovart vs Canva vs Midjourney: Complete Comparison](https://www.lovart.ai/blog/lovart-vs-canva-vs-midjourney)** — Which tool fits your workflow?
"""

# ── Fix all pages ──
fixed = 0
for root, dirs, files in os.walk(BASE):
    for fname in files:
        if not fname.endswith('.md'): continue
        if any(s in fname for s in ['generate','gen_','transform','expand','CLAUDE','.py','.json']): continue
        
        path = os.path.join(root, fname)
        with open(path) as f:
            c = f.read()
        if len(c) < 300: continue
        
        slug = fname.replace('.md','')
        orig_wc = len(c.split())
        
        # ── 1. Fix frontmatter ──
        fm_end = c.find('---', 3)
        if fm_end < 0: continue
        old_fm = c[3:fm_end].strip()
        
        # Extract existing fields
        title_m = re.search(r'title:\s*"(.*?)"', old_fm)
        title = title_m.group(1) if title_m else slug
        old_cat = re.search(r'category:\s*"(.*?)"', old_fm)
        cat_raw = old_cat.group(1) if old_cat else "How-To"
        new_cat = map_category(cat_raw)
        
        # Extract keywords
        kw_section = re.search(r'target_keywords:(.*?)(?=\n\w+:|$)', old_fm, re.DOTALL)
        if kw_section:
            kws = re.findall(r'"([^"]+)"', kw_section.group(1))
        else:
            kws = [slug.replace('-',' ')]
        
        # Generate tags from keywords (first 4)
        tags = [w for w in kws[:4] if len(w) > 3]
        if not tags: tags = ["ai design", "lovart"]
        
        # Assign cover
        cover_url = pick_cover(slug)
        alt_text = f"{title[:100]} — Lovart AI Design Agent blog cover"
        
        # SEO title (first 60 chars of title)
        seo_title = title[:60] if len(title) > 60 else title
        
        # SEO description (from first 160 chars of intro)
        body_start = c.find('\n# ', fm_end)
        intro = c[body_start:body_start+300] if body_start > 0 else c[fm_end:fm_end+300]
        intro_clean = re.sub(r'[#*\[\]\(\)\n]', ' ', intro).strip()[:160]
        seo_desc = intro_clean[:157] + '...' if len(intro_clean) > 157 else intro_clean
        
        # Description/ excerpt
        desc = intro_clean[:280]
        
        # Build new frontmatter
        kw_yaml = "\n".join(f'  - "{w}"' for w in kws[:8])
        tag_yaml = "\n".join(f'  - "{t}"' for t in tags[:6])
        
        new_fm = f"""---
title: "{title}"
slug: {slug}
date: "{DATE}"
language: en
page_type: Blog Post
category: {new_cat}
author: {AUTHOR}
description: "{desc}"
focus_keyword: "{kws[0] if kws else slug.replace('-',' ')}"
keywords:
{kw_yaml}
tags:
{tag_yaml}
cover_url: {cover_url}
alt_text: "{alt_text}"
seo_title: "{seo_title}"
seo_description: "{seo_desc}"
status: draft
content_cluster: PSEO Programmatic SEO
internal_note: "PSEO auto-generated | Batch validation"
---"""
        
        # ── 2. Structured data ──
        # Remove old <script> FAQPage/WebPage blocks
        c = re.sub(r'<script type="application/ld\+json">\s*\{[^<]*"@type":\s*"FAQPage"[^<]*\}</script>', '', c, flags=re.DOTALL)
        c = re.sub(r'<script type="application/ld\+json">\s*\{[^<]*"@type":\s*"WebPage"[^<]*\}</script>', '', c, flags=re.DOTALL)
        
        # Use safe generic FAQ — avoids regex extraction bugs that eat body content
        safe_faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": "Can I use Lovart designs commercially?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Every design, image, and asset you create with Lovart belongs to you with full commercial rights. Use them on your website, in ads, on products, for client work, anywhere — no attribution required."}},
                {"@type": "Question", "name": "Do I need design experience to use Lovart?", "acceptedAnswer": {"@type": "Answer", "text": "No. Lovart is built for non-designers. You describe what you want in plain language, and the AI Design Agent handles composition, typography, color selection, and export settings automatically. The MCoT Engine applies professional design principles so you don't need to know them."}},
                {"@type": "Question", "name": "How is Lovart different from Canva or Midjourney?", "acceptedAnswer": {"@type": "Answer", "text": "Canva uses templates — your designs look like templates. Midjourney generates images but can't reliably do text or let you edit specific elements. Lovart is an AI Design Agent — it creates original designs from your description, lets you edit specific elements with Touch Edit, maintains brand consistency via Brand Kit, and exports in professional formats."}},
                {"@type": "Question", "name": "Can I try Lovart for free?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Lovart's Free plan gives you 50 designs per month across 5 AI models, including Touch Edit (10 edits/month). No credit card required. Upgrade to Starter ($19/month) for 500 designs, HD export, and Brand Kit."}},
                {"@type": "Question", "name": "What formats can I export to?", "acceptedAnswer": {"@type": "Answer", "text": "Lovart exports in PNG, JPEG, SVG, PDF (with bleed, CMYK, 300 DPI for professional printing), PSD (layered), and platform-specific optimized formats for social media, web, and advertising platforms."}},
            ]
        }
        faq_json = json.dumps(safe_faq, indent=2, ensure_ascii=False)
        sd_block = f"""structured_data_json: |
{chr(10).join('  ' + line for line in faq_json.split(chr(10)))}"""
        new_fm += f"\n{sd_block}"
        
        # Replace old frontmatter with new
        c = '---\n' + new_fm + '\n' + c[fm_end+3:]
        
        # ── 3. Add E-E-A-T signals if missing ──
        if 'MCoT' not in c and 'ChatCanvas' not in c:
            faq_match = re.search(r'\n## Frequently Asked Questions\n', c)
            if faq_match:
                c = c[:faq_match.start()] + EEAT_BLOCK + c[faq_match.start():]
        
        # ── 4. Add cluster footer if missing ──
        if 'Explore More' not in c and 'Related Articles' not in c:
            c = c.rstrip() + CLUSTER_FOOTER
        
        # ── 5. Clean up double-spacing ──
        c = re.sub(r'\n{4,}', '\n\n\n', c)
        
        with open(path, 'w') as f:
            f.write(c)
        
        fixed += 1
        new_wc = len(c.split())
        if fixed % 20 == 0:
            print(f"  {fixed} pages fixed... ({slug}: {orig_wc}→{new_wc}w)")

print(f"\nTotal fixed: {fixed} pages")
