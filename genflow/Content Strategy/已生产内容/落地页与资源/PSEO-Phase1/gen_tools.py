#!/usr/bin/env python3
"""Generate 19 new Tools pages in 3 batches."""
import os, json

DST = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-3 Content Gen/Content Strategy/已生产内容/落地页与资源/PSEO-Phase1/Tools-Phase1")
DATE = "2026-07-15"

def page(tool):
    """Build a tools page from tool dict. Content in triple-quoted raw strings."""
    slug, name, cat = tool["slug"], tool["name"], tool["category"]
    title, kw, intro = tool["title"], tool["keywords"], tool["intro"]
    steps, usecases, comps, faqs = tool["steps"], tool["use_cases"], tool["competitors"], tool["faq"]

    # Frontmatter
    kw_lines = "\n".join(f'  - "{k}"' for k in kw)
    fm = f"""---
title: "{title}"
page_type: "Tool Landing Page"
category: "{cat}"
tool_name: "{name}"
target_keywords:
{kw_lines}
slug: "{slug}"
word_count_target: 2000
date: "{DATE}"
status: Draft
---"""

    # FAQ JSON-LD
    faq_entities = []
    for q, a in tool["faq_json"]:
        a_clean = a.replace('"', '\\"').replace('\n', ' ')
        faq_entities.append('    {"@type": "Question", "name": "' + q + '", "acceptedAnswer": {"@type": "Answer", "text": "' + a_clean + '"}}')
    faq_json_ld = ",\n".join(faq_entities)

    schema = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{title}",
  "url": "https://www.lovart.ai/tools/{slug}",
  "datePublished": "{DATE}",
  "publisher": {{"@type": "Organization", "name": "Lovart", "url": "https://www.lovart.ai"}}
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_json_ld}
  ]
}}
</script>"""

    # Steps
    steps_text = ""
    for i, s in enumerate(steps):
        steps_text += f"\n\n### Step {i+1}: {s['title']}\n\n{s['body']}"

    # Use cases
    uc_text = ""
    for u in usecases:
        uc_text += f"\n\n### {u['title']}\n\n{u['body']}"

    # Comparison table
    comp_rows = ""
    for c in comps:
        comp_rows += f"\n| **{c[0]}** | {c[1]} | **{c[2]}** |"

    # FAQ
    faq_text = ""
    for q, a in faqs:
        faq_text += f"\n\n**Q: {q}**\nA: {a}"

    body = f"""

# {title}

{intro}

---

## Why {name} Matters for Your Workflow

Before diving into how {name} works, let's be clear about what problem it solves. Traditional approaches to {cat.lower().replace('ai ','').replace(' model','')} require either expensive specialized software, professional expertise, or significant time investment. {name} inside Lovart's AI Design Agent changes this: professional-quality output, zero learning curve, instant results — all within your existing Lovart workflow.

---

## How {name} Works
{steps_text}

---

## Real-World Use Cases

{name} isn't just a technical capability — it solves real problems for real users. Here are the most common ways Lovart users apply {name} in their daily work:
{uc_text}

---

## {name} Compared to Alternatives

Not all tools in this category are created equal. Here is how {name} inside Lovart compares to the alternatives you might be considering:

| Tool | Limitations | Lovart Advantage |
|------|------------|-----------------|{comp_rows}

**Bottom line:** {name} inside Lovart gives you professional-quality results integrated directly into your design workflow — no switching platforms, no separate subscriptions, no export-import hassles. Generate, refine with Touch Edit, apply your Brand Kit, and export in production formats — all in one place.

---

## Pricing: What {name} Costs

{name} is included in all Lovart plans. Here is what each tier offers for your design workflow:

| Plan | Designs/Month | Key Features | Price |
|------|---------------|--------------|-------|
| **Free** | 50 | 5 AI models, Standard export, 10 Touch Edits | $0 |
| **Starter** | 500 | HD export, Brand Kit, 10+ models, All design tools | $19/mo |
| **Professional** | 2,000 | 4K export, Multiple Brand Kits, Priority generation | $49/mo |
| **Agency** | 10,000 | All features, Team collaboration, API access | $149/mo |

For most individual users, the **Starter plan at $19/month** provides everything needed for professional {cat.lower().replace('ai ','')} work. Teams and agencies benefit from the Professional ($49/month) or Agency ($149/month) plans with higher limits, 4K resolution, and collaboration features.

---

**[Start Using {name} — Free, No Credit Card Required](https://www.lovart.ai/)**

---

## Frequently Asked Questions
{faq_text}

---

**[Try {name} Free — No Credit Card](https://www.lovart.ai/)**
"""
    return fm + schema + body


# Load tool data from JSON files to avoid escaping issues
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Read the companion data file
data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools_data.json")
if os.path.exists(data_file):
    with open(data_file) as f:
        all_tools = json.load(f)
    
    count = 0
    total = 0
    for tool in all_tools:
        path = os.path.join(DST, f"{tool['slug']}.md")
        content = page(tool)
        with open(path, 'w') as f:
            f.write(content)
        wc = len(content.split())
        total += wc
        count += 1
        print(f"  {tool['slug']}.md — {wc} words")
    
    print(f"\nDone: {count} pages, ~{total} words, avg ~{total//count} words/page")
else:
    print(f"Data file not found: {data_file}")
    print("Please create tools_data.json first")
