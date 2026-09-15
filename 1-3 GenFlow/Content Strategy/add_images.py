#!/usr/bin/env python3
"""批量补全博客文章的 Image Placeholder + Image Appendix"""

import os, re

# TODO: 重构后 "已生产内容/博客文章" 子目录已不存在；如需运行请确认博客文章新落点
BASE = "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/Content Marketing/Content Calendar/已生产内容/博客文章"

def extract_title(content):
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else "Untitled"

def extract_article_type(content):
    """Determine topic from filename and content for prompt generation"""
    text = content[:2000].lower()
    if 'how to' in text or 'step-by-step' in text or 'guide' in text:
        return 'howto'
    if 'vs ' in text or 'comparison' in text or 'compared' in text:
        return 'comparison'
    if 'case study' in text or 'saved' in text or 'transformed' in text:
        return 'case'
    if 'best ' in text or 'top ' in text or 'list' in text:
        return 'listicle'
    if 'trend' in text or 'insight' in text or 'prediction' in text:
        return 'insight'
    if 'brand kit' in text or 'color' in text or 'palette' in text:
        return 'brand'
    if 'digest' in text or 'newsletter' in text:
        return 'digest'
    return 'general'

def generate_prompts(title, atype):
    """Generate 4 image prompts based on article type and title"""
    title_short = title[:80]
    
    prompts = {
        'howto': [
            f"A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create {title_short.split('How to ')[-1] if 'How to ' in title_short else 'a design'} — warm natural lighting, candid documentary style",
            f"A hand-drawn sketch diagram showing the step-by-step workflow for {title_short.split('How to ')[-1] if 'How to ' in title_short else 'creating designs'} with AI — clean line art on grid paper, arrows connecting each step, minimalist style",
            f"[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]",
            f"Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in {title_short[:50]} — modern, aspirational, cinematic lighting"
        ],
        'comparison': [
            f"A split-screen scene showing two workspaces side by side: one cluttered with multiple tools and tabs (traditional), the other clean with a single Lovart ChatCanvas — contrasting lighting, editorial style",
            f"A hand-drawn comparison matrix sketch comparing features across tools mentioned in {title_short[:60]} — markers and sticky notes, creative brainstorming aesthetic",
            f"[REAL SCREENSHOT REQUIRED: Lovart comparison view or multi-model selector interface showing different AI models available]",
            f"Professional brand visual showing the Lovart logo and key differentiators highlighted in {title_short[:50]} — clean, bold typography, modern tech aesthetic"
        ],
        'case': [
            f"The persona from the case study in their real work environment — authentic, candid moment showing the transformation described in {title_short[:60]} — natural light, documentary photography style",
            f"A simple data visualization sketch showing before/after metrics mentioned in the case study — hand-drawn bar charts and arrows, clean infographic style",
            f"[REAL SCREENSHOT REQUIRED: Lovart interface showing a completed project similar to the case study — with visible results]",
            f"Brand visual showing the success transformation — the 'after' state described in {title_short[:50]} — inspiring, cinematic, warm tones"
        ],
        'listicle': [
            f"A curated flat-lay photography scene showing design tools and outputs mentioned in {title_short[:50]} — organized chaos, editorial product photography style",
            f"A hand-drawn ranking or scoring matrix showing the criteria used to evaluate options in {title_short[:50]} — colorful markers, creative layout",
            f"[REAL SCREENSHOT REQUIRED: Lovart template gallery or design showcase showing multiple completed designs]",
            f"Brand visual showing 'Best of' collection — multiple beautiful design outputs arranged in a grid, modern gallery aesthetic"
        ],
        'insight': [
            f"A forward-looking scene depicting the future described in {title_short[:60]} — conceptual, artistic, cinematic — a person confidently creating with AI in an innovative workspace",
            f"A hand-drawn trend map or timeline showing the evolution described in {title_short[:50]} — arrows, nodes, annotated predictions — creative consulting aesthetic",
            f"[REAL SCREENSHOT REQUIRED: Lovart feature that exemplifies the trend or insight discussed — with contextual caption]",
            f"Brand visual representing Lovart's vision for the future of AI design — aspirational, forward-looking, professional"
        ],
        'brand': [
            f"A beautifully arranged brand identity flat-lay showing color swatches, font specimens, and design elements matching the niche in {title_short[:60]} — warm, editorial style",
            f"A hand-drawn brand wheel or identity framework sketch — color circles, font pairings, and application examples — creative branding consultant style",
            f"[REAL SCREENSHOT REQUIRED: Lovart Brand Kit interface showing color palette and font selection for a brand setup]",
            f"Brand visual showing a complete brand identity package — logo, business card, social post, and packaging all in consistent style — professional, cohesive"
        ],
    }
    
    return prompts.get(atype, [
        f"A relatable professional scene depicting the core problem discussed in {title_short[:60]} — authentic, natural lighting, documentary style",
        f"A hand-drawn conceptual diagram illustrating the main idea of {title_short[:50]} — clean sketch style, creative brainstorming aesthetic",
        f"[REAL SCREENSHOT REQUIRED: Lovart interface showing a relevant feature or completed design related to this article]",
        f"Professional brand visual for Lovart AI Design Agent — modern, aspirational, showing the value promised in {title_short[:50]}"
    ])

def find_insertion_points(content):
    """Find logical positions to insert IMAGE placeholders"""
    points = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        # After H1 (title)
        if stripped.startswith('# ') and not points:
            points.append(('IMAGE_1', i + 1))
        # After first H2 section
        elif stripped.startswith('## ') and len(points) < 2:
            points.append(('IMAGE_2', i + 2))
        # At roughly midpoint
        elif stripped.startswith('## ') and len(points) < 3 and i > len(lines) * 0.4:
            points.append(('IMAGE_3', i + 2))
    
    # IMAGE_4 near the end
    conclusion_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## ') and ('conclusion' in line.lower() or 'faq' in line.lower() or 'final' in line.lower() or 'verdict' in line.lower()):
            conclusion_idx = i
            break
    if not conclusion_idx:
        conclusion_idx = len(lines) - 10
    
    points.append(('IMAGE_4', conclusion_idx))
    
    return sorted(points, key=lambda x: x[1])

def build_appendix(prompts):
    return f"""
### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
{prompts[0]}

**Image 2 — The Conceptual Diagram**:
{prompts[1]}

**Image 3 — Real UI Screenshot**:
{prompts[2]}

**Image 4 — Brand CTA**:
{prompts[3]}
"""

def process_file(fp):
    with open(fp, 'r') as f:
        content = f.read()
    
    title = extract_title(content)
    atype = extract_article_type(content)
    prompts = generate_prompts(title, atype)
    appendix = build_appendix(prompts)
    
    # Remove existing appendix if present (to avoid duplicates)
    content = re.sub(r'\n*### Appendix: Image Prompts.*$', '', content, flags=re.DOTALL)
    content = content.rstrip() + '\n'
    
    # Find insertion points and insert placeholders (insert from end to preserve indices)
    points = find_insertion_points(content)
    lines = content.split('\n')
    
    placeholders = [
        '\n[IMAGE 1 PLACEHOLDER — Persona Scenario]\n',
        '\n[IMAGE 2 PLACEHOLDER — Conceptual Diagram]\n',
        '\n[IMAGE 3 PLACEHOLDER — Real UI Screenshot]\n',
        '\n[IMAGE 4 PLACEHOLDER — Brand CTA]\n',
    ]
    
    # Insert from bottom up to preserve indices
    for (label, pos), ph in zip(reversed(points), reversed(placeholders)):
        if pos < len(lines):
            lines.insert(pos, ph)
    
    content = '\n'.join(lines)
    
    # Remove any duplicate E-E-A-T or trailing whitespace before appendix
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Append the appendix
    content = content.rstrip() + '\n' + appendix + '\n'
    
    with open(fp, 'w') as f:
        f.write(content)
    
    return title, atype

# Main
if __name__ == '__main__':
    processed = 0
    skipped = 0
    
    for fn in sorted(os.listdir(BASE)):
        if not fn.endswith('.md'):
            continue
        fp = os.path.join(BASE, fn)
        with open(fp, 'r') as f:
            content = f.read()
        
        # Skip if already has both placeholders and appendix
        has_ph = 'IMAGE 1 PLACEHOLDER' in content or 'IMAGE 2 PLACEHOLDER' in content
        has_app = 'Image Appendix' in content or 'image appendix' in content.lower()
        
        if has_ph and has_app:
            skipped += 1
            continue
        
        title, atype = process_file(fp)
        processed += 1
        if processed % 50 == 0:
            print(f"  Processed {processed}... ({title[:60]} [{atype}])")
    
    print(f"\nDone. Added images to {processed} articles, skipped {skipped} (already complete).")
