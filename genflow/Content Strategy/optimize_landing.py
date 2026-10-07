#!/usr/bin/env python3
"""批量优化落地页：补全 FAQ + JSON-LD + CTA 标准化"""

import os, re, json

BASE = "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/Content Marketing/Content Calendar/已生产内容/落地页与资源"

def extract_title(content):
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else "Untitled"

def extract_slug(fp):
    return os.path.basename(fp).replace('.md', '')

def generate_faq(title, content_text):
    """Generate 5-7 FAQ based on page topic and existing content"""
    text = content_text.lower()
    title_lower = title.lower()
    
    faqs = []
    
    # Generic questions all landing pages should answer
    if 'pricing' not in text.lower() and 'plan' not in text.lower():
        faqs.append(("How much does it cost?", 
            f"Lovart offers a Free plan to get started with {title.split(' — ')[0] if ' — ' in title else 'this tool'}. Paid plans start at $19/month (Starter), $49/month (Basic), $99/month (Pro), and $149/month (Ultimate). All plans include full access to Lovart's AI design agent capabilities."))
    
    faqs.append(("Can I use the designs commercially?",
        "Yes. Every design, image, and video you create with Lovart is yours to use commercially — for ads, products, client work, social media, print, or anything else. No attribution required."))
    
    faqs.append(("Do I need design experience to use this?",
        "No. Lovart is built for non-designers. You describe what you want in plain language, and the AI design agent handles the rest. The Touch Edit feature lets you refine results by tapping, not by learning complex software."))
    
    # Topic-specific questions
    if 'video' in title_lower or 'video' in text[:500]:
        faqs.append(("How long can my AI-generated videos be?",
            "Lovart supports videos from 2 seconds to 2 minutes. For longer content, use the batch generation system (Seedance 2.0) to create multiple scenes and stitch them together."))
    elif 'image' in title_lower or 'photo' in title_lower or 'picture' in title_lower:
        faqs.append(("What resolution are the generated images?",
            "Standard resolution is up to 2048×2048 pixels. High-res output (up to 4096×4096) is available on Basic plan and above. Vector SVG export is available for infinitely scalable graphics."))
    elif 'logo' in title_lower or 'brand' in title_lower:
        faqs.append(("Can I trademark an AI-generated logo?",
            "Yes, but it depends on how you use it. AI-generated logos that you modify and use as part of your brand identity can be trademarked. The key is making the logo distinctively yours through customization. Read our full copyright guide for details."))
    elif 'template' in title_lower:
        faqs.append(("Are the templates customizable?",
            "Yes. Every template is fully customizable. You can change colors, fonts, images, layout, and text. Your Brand Kit settings are automatically applied to any template you use."))
    
    faqs.append(("How is Lovart different from other AI design tools?",
        "Unlike Midjourney, DALL-E, or Canva — which generate images or use templates — Lovart is an AI Design Agent. It understands your business context through MCoT (Mind Chain of Thought), lets you edit specific parts without regenerating (Touch Edit), keeps your brand consistent automatically (Brand Kit), and exports in professional formats (PSD, SVG, PDF)."))
    
    faqs.append(("Can I try it for free?",
        "Yes. Lovart's Free plan gives you 50 image generations per month, access to 5 AI models, Touch Edit (10 edits/month), and Brand Kit setup. No credit card required."))
    
    # Build FAQ markdown
    faq_md = "\n## Frequently Asked Questions\n\n"
    for q, a in faqs[:7]:
        faq_md += f"### {q}\n{a}\n\n"
    
    return faq_md

def generate_jsonld(title, desc, slug, date="2026-05-12"):
    """Generate JSON-LD structured data"""
    return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{title}",
  "description": "{desc}",
  "url": "https://www.lovart.ai/{slug}",
  "datePublished": "{date}",
  "publisher": {{
    "@type": "Organization",
    "name": "Lovart",
    "url": "https://www.lovart.ai"
  }}
}}
</script>
"""

def optimize_page(fp):
    with open(fp, 'r') as f:
        content = f.read()
    
    title = extract_title(content)
    slug = extract_slug(fp)
    original = content
    
    # 1. Add FAQ if missing
    if '## Frequently Asked Questions' not in content and '## FAQ' not in content:
        faq = generate_faq(title, content)
        # Insert before any existing appendix or at end
        if '### Appendix' in content:
            content = content.replace('### Appendix', faq + '\n### Appendix')
        elif '---' in content[content.rfind('## '):]:
            # Insert before last separator
            last_sep = content.rfind('\n---\n')
            if last_sep > 0:
                content = content[:last_sep] + '\n' + faq + '\n---\n' + content[last_sep+5:]
            else:
                content = content.rstrip() + '\n' + faq
        else:
            content = content.rstrip() + '\n' + faq
    
    # 2. Add JSON-LD if missing
    if 'application/ld+json' not in content:
        # Extract first 155 chars for description
        text_only = re.sub(r'[#*\[\]\(\)\n]', ' ', content[:500])
        text_only = re.sub(r'\s+', ' ', text_only).strip()[:155]
        jsonld = generate_jsonld(title, text_only, slug)
        # Insert after YAML frontmatter or at top
        if content.startswith('---'):
            end_fm = content.find('---', 3)
            if end_fm > 0:
                content = content[:end_fm+3] + '\n' + jsonld + content[end_fm+3:]
        else:
            content = jsonld + '\n' + content
    
    # 3. Standardize CTA (add if missing, enhance if weak)
    cta_patterns = [
        r'\[Start.*Free.*\]\(.*\)',
        r'\[Try.*Free.*\]\(.*\)',
        r'\[Get Started.*\]\(.*\)',
        r'\[Create.*Free.*\]\(.*\)',
    ]
    has_cta = any(re.search(p, content) for p in cta_patterns)
    if not has_cta:
        cta = f"\n**[Start Creating Free — No Credit Card Required](https://www.lovart.ai/)**\n"
        # Add before FAQ if exists, otherwise at end
        if '## Frequently Asked Questions' in content:
            content = content.replace('## Frequently Asked Questions', cta + '\n## Frequently Asked Questions')
        elif '## FAQ' in content:
            content = content.replace('## FAQ', cta + '\n## FAQ')
        else:
            content = content.rstrip() + '\n' + cta
    
    if content != original:
        with open(fp, 'w') as f:
            f.write(content)
        return True
    return False

if __name__ == '__main__':
    optimized = 0
    skipped = 0
    
    for cat in sorted(os.listdir(BASE)):
        dp = os.path.join(BASE, cat)
        if not os.path.isdir(dp): continue
        for fn in os.listdir(dp):
            if not fn.endswith('.md'): continue
            fp = os.path.join(dp, fn)
            if optimize_page(fp):
                optimized += 1
                if optimized % 20 == 0:
                    print(f"  Processed {optimized}... ({cat})")
            else:
                skipped += 1
    
    print(f"\nDone. Optimized {optimized} pages, skipped {skipped} (already complete).")
    print(f"Added: FAQ sections, JSON-LD structured data, CTA standardization.")
