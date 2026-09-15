#!/usr/bin/env python3
"""
Refactor blog posts using MiniMax M3.
Reads existing content + refactoring plan, generates new version.
"""

import json
import os
import sys
import re
from pathlib import Path
import urllib.request

# Configuration
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "sk-cp-fsjQp3X1_fMaOsiC8Ri0b0F4PSif0Rv22FVVeUADCD8oadEExtsJjr15eiDkNaAHaOszyxrgLfjmjfRI_bDod4llxvVDCfA9dKcGX1xiWbiXOzD144LEDDI")
MINIMAX_ENDPOINT = "https://api.minimaxi.com/anthropic/v1/messages"
MINIMAX_MODEL = "MiniMax-M3"
MIN_WORDS = 7500

EXISTING_DIR = Path(__file__).parent.parent / "01-existing"
PLANS_DIR = Path("/Users/seveno/Documents/Lovart Local Dev/Output/SEO-Reports/改造建议")
OUTPUT_DIR = Path(__file__).parent.parent / "02-rewritten"

# Product terms to include
PRODUCT_TERMS = [
    "MCoT Engine",
    "ChatCanvas",
    "Touch Edit",
    "Brand Kit",
    "Identity Lock",
]

# Anti-slop words to avoid
SLOP_WORDS = [
    "stands as", "testament", "underscores", "vibrant",
    "revolutionize", "game-changer", "leverage", "streamline",
    "empower", "seamless", "delve", "unprecedented",
    "the future of", "pave the way", "unlock",
]

def read_json_file(filepath):
    """Read JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_text_file(filepath):
    """Read text file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_portable_text_text(body):
    """Extract plain text from Portable Text body."""
    if not body or not isinstance(body, list):
        return ""
    
    texts = []
    for block in body:
        if block.get("_type") == "block":
            children = block.get("children", [])
            for child in children:
                if child.get("_type") == "span":
                    texts.append(child.get("text", ""))
        elif block.get("_type") == "bodyImage":
            alt = block.get("alt", "")
            if alt:
                texts.append(f"[Image: {alt}]")
    
    return " ".join(texts)

def parse_refactoring_plan(plan_content):
    """Parse refactoring plan markdown to extract sections."""
    sections = {
        "title_rewrite": "",
        "description_rewrite": "",
        "h1_h2_optimization": "",
        "long_tail_content": "",
        "faq": "",
        "internal_links": [],
    }
    
    # Extract title rewrite
    title_match = re.search(r'改写后 title.*?```yaml\s*title:\s*"(.*?)"\s*```', plan_content, re.DOTALL)
    if title_match:
        sections["title_rewrite"] = title_match.group(1)
    
    # Extract description rewrite
    desc_match = re.search(r'改写后 description.*?```yaml\s*description:\s*"(.*?)"\s*```', plan_content, re.DOTALL)
    if desc_match:
        sections["description_rewrite"] = desc_match.group(1)
    
    # Extract H1/H2 section
    h1h2_match = re.search(r'## 2\. H1/H2 优化.*?```markdown\s*(.*?)\s*```', plan_content, re.DOTALL)
    if h1h2_match:
        sections["h1_h2_optimization"] = h1h2_match.group(1).strip()
    
    # Extract long-tail content
    longtail_match = re.search(r'## 3\. 添加 1-2 段长尾内容.*?在原文章主体后添加.*?：\s*\n(.*?)(?=\n###|\n##|\Z)', plan_content, re.DOTALL)
    if longtail_match:
        sections["long_tail_content"] = longtail_match.group(1).strip()
    
    # Extract FAQ
    faq_match = re.search(r'## 4\. 添加 2-3 个 FAQ.*?```markdown\s*(.*?)\s*```', plan_content, re.DOTALL)
    if faq_match:
        sections["faq"] = faq_match.group(1).strip()
    
    # Extract internal links
    links_match = re.search(r'## 5\. Internal Links.*?\n(.*?)(?=\n###|\n##|\Z)', plan_content, re.DOTALL)
    if links_match:
        links_text = links_match.group(1)
        links = re.findall(r'\[.*?\]\((.*?)\)', links_text)
        sections["internal_links"] = links
    
    return sections

def call_minimax(prompt, system_prompt=""):
    """Call MiniMax M3 API."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": MINIMAX_API_KEY,
        "anthropic-version": "2023-06-01",
    }
    
    payload = {
        "model": MINIMAX_MODEL,
        "max_tokens": 65536,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }
    
    if system_prompt:
        payload["system"] = system_prompt
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(MINIMAX_ENDPOINT, data=data, headers=headers, method='POST')
    
    try:
        resp = urllib.request.urlopen(req, timeout=300)
        result = json.loads(resp.read().decode())
        # Extract text from response
        if "content" in result:
            return result["content"][0].get("text", "")
        return str(result)
    except Exception as e:
        print(f"  API Error: {e}")
        return None

def generate_refactored_content(slug, existing_post, plan_sections):
    """Generate refactored content using MiniMax M3."""
    
    # Extract existing content
    existing_title = existing_post.get("title", slug)
    existing_body = extract_portable_text_text(existing_post.get("body", []))
    existing_desc = existing_post.get("description", "")
    
    # Build prompt
    system_prompt = """You are an expert SEO content writer for Lovart, an AI design platform.
Write comprehensive, high-quality blog content that:
1. Is at least 7500 words long
2. Uses natural, conversational tone (first person)
3. Includes specific product mentions (MCoT Engine, ChatCanvas, Touch Edit, Brand Kit, Identity Lock)
4. Avoids AI slop words (stands as, testament, revolutionize, game-changer, etc.)
5. Includes practical examples and real-world use cases
6. Has clear H2 sections every 500 words
7. Ends with FAQ section (2-3 questions)
8. Includes internal links to related Lovart content"""

    prompt = f"""Rewrite and expand this blog post to 7500+ words.

EXISTING POST:
Title: {existing_title}
Description: {existing_desc}
Content: {existing_body[:5000]}... [truncated]

REFACTORING PLAN:
New Title: {plan_sections.get('title_rewrite', existing_title)}
New Description: {plan_sections.get('description_rewrite', existing_desc)}
H1/H2 Structure: {plan_sections.get('h1_h2_optimization', 'Use standard H2 structure')}
Long-tail Keywords: {plan_sections.get('long_tail_content', '')}
FAQ Topics: {plan_sections.get('faq', '')}

REQUIREMENTS:
1. Write the COMPLETE article in Markdown format
2. Minimum 7500 words (aim for 8000-9000)
3. Include frontmatter with title, description, slug: {slug}
4. Use the new title from the refactoring plan
5. Include ALL product terms: MCoT Engine, ChatCanvas, Touch Edit, Brand Kit, Identity Lock
6. NO AI slop words (avoid: stands as, testament, revolutionize, game-changer, leverage, streamline, empower, seamless, delve)
7. First person perspective ("I tested...", "In my experience...")
8. Include at least one "踩坑" (pitfall/mistake) section
9. H2 every 500 words minimum
10. FAQ section at the end with 2-3 Q&As
11. Internal links to: /blog/lovart-design-agent-review, /tools/video-generator, /tools/text-to-image-generator
12. CTA: "Try Lovart Free for 14 Days"

Write the COMPLETE article now:"""

    print(f"  Calling MiniMax M3 API...")
    response = call_minimax(prompt, system_prompt)
    
    if not response:
        return None
    
    # Clean up response - remove markdown code blocks if present
    if response.startswith("```markdown"):
        response = response[11:]
    if response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]
    
    return response.strip()

def validate_content(content, slug):
    """Validate generated content meets requirements."""
    issues = []
    
    # Word count
    word_count = len(content.split())
    if word_count < MIN_WORDS:
        issues.append(f"Word count {word_count} < {MIN_WORDS}")
    
    # Slop check
    content_lower = content.lower()
    for slop in SLOP_WORDS:
        if slop.lower() in content_lower:
            issues.append(f"Contains slop word: {slop}")
    
    # Product terms check
    for term in PRODUCT_TERMS:
        if term.lower() not in content_lower:
            issues.append(f"Missing product term: {term}")
    
    # H2 density check
    h2_count = content.count("## ")
    if h2_count < (word_count / 500):
        issues.append(f"H2 count {h2_count} too low for {word_count} words")
    
    # FAQ check
    if "faq" not in content_lower and "frequently asked" not in content_lower:
        issues.append("Missing FAQ section")
    
    return issues

def main():
    """Main entry point."""
    # Read batch from command line
    batch_start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    # Get list of slugs to process
    existing_files = sorted(EXISTING_DIR.glob("*.json"))
    # Exclude manifest files
    existing_files = [f for f in existing_files if f.name != "manifest.json"]
    batch_files = existing_files[batch_start:batch_start + batch_size]
    
    if not batch_files:
        print("No files to process")
        return
    
    print(f"Processing batch: {batch_start} to {batch_start + len(batch_files) - 1}")
    print(f"Files: {[f.stem for f in batch_files]}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    for i, existing_file in enumerate(batch_files, 1):
        slug = existing_file.stem
        print(f"\n[{i}/{len(batch_files)}] Processing: {slug}")
        
        # Read existing post
        existing_post = read_json_file(existing_file)
        print(f"  Existing title: {existing_post.get('title', 'N/A')}")
        
        # Read refactoring plan
        plan_file = PLANS_DIR / f"{slug}.md"
        if not plan_file.exists():
            print(f"  ✗ No refactoring plan found: {plan_file}")
            results.append({"slug": slug, "status": "no_plan"})
            continue
        
        plan_content = read_text_file(plan_file)
        plan_sections = parse_refactoring_plan(plan_content)
        print(f"  Plan title: {plan_sections.get('title_rewrite', 'N/A')}")
        
        # Generate refactored content
        new_content = generate_refactored_content(slug, existing_post, plan_sections)
        
        if not new_content:
            print(f"  ✗ Failed to generate content")
            results.append({"slug": slug, "status": "gen_failed"})
            continue
        
        # Validate content
        issues = validate_content(new_content, slug)
        word_count = len(new_content.split())
        
        if issues:
            print(f"  ⚠ Validation issues: {issues}")
        
        # Save to file
        output_file = OUTPUT_DIR / f"{slug}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ Generated {word_count} words")
        print(f"  ✓ Saved to {output_file.name}")
        
        results.append({
            "slug": slug,
            "status": "ok",
            "word_count": word_count,
            "issues": issues,
            "file": str(output_file)
        })
    
    # Summary
    ok = sum(1 for r in results if r["status"] == "ok")
    total_words = sum(r.get("word_count", 0) for r in results)
    print(f"\n{'='*60}")
    print(f"Batch Summary: {ok}/{len(batch_files)} posts generated")
    print(f"Total words: {total_words:,}")
    print(f"Average words: {total_words // max(ok, 1):,}")
    
    # Save manifest
    manifest_file = OUTPUT_DIR / f"manifest-batch-{batch_start}.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Manifest saved to {manifest_file}")

if __name__ == "__main__":
    main()
