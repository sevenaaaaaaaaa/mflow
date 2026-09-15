"""Shared blocks for Lovart 101 batch generation."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFTS = ROOT / "01-Drafts"
PICK_COVER = ROOT / "scripts" / "pick-cover.py"

SIGNUP = "https://lovart.ai/signup"
PRICING = "https://lovart.ai/pricing"

VERIFIED_LINKS = [
    ("ChatCanvas getting started pillar", "/blog/05-pillar-getting-started-lovart"),
    ("Brand Kit guide for every industry", "/blog/complete-guide-brand-kit-every-industry-lovart"),
    ("how to chat and generate any design type", "/blog/how-to-chat-generate-any-design-type-lovart-agent"),
    ("Nano Banana complete guide", "/blog/nano-banana-ai-complete-guide-lovart-image-model"),
    ("Edit Elements vs Photoshop habits", "/blog/how-lovarts-edit-elements-outpaces-photoshop-dall-e-3-and-outdated-design-habits"),
    ("Touch Edit best practice", "/blog/touch-edit-best-practice-3-gestures-lovart"),
    ("Brand Kit setup in five minutes", "/blog/brand-kit-setup-5-minutes-lovart-best-practice"),
    ("build complete brand kit from scratch", "/blog/build-complete-brand-kit-from-scratch-ai"),
    ("batch social content guide", "/blog/batch-generate-30-days-social-media-content-ai"),
    ("create packaging design with AI", "/blog/create-packaging-design-with-ai"),
    ("design business cards with AI", "/blog/design-business-cards-with-ai"),
    ("how to create product videos with AI", "/blog/how-to-create-product-videos-with-ai"),
    ("image to video AI guide", "/blog/image-to-video-ai-static-designs-into-motion"),
    ("typography 101 font pairing", "/blog/typography-101-font-pairing-rules-non-designers"),
    ("color psychology for brands", "/blog/color-psychology-brand-design-complete-guide"),
    ("Lovart signup", SIGNUP),
    ("Lovart pricing", PRICING),
]


def pick_cover_url(slug: str) -> str:
    out = subprocess.check_output(
        ["python3", str(PICK_COVER), slug], text=True, cwd=str(ROOT)
    ).strip()
    return out.splitlines()[0]


def howto_schema(title: str, description: str, cover: str, slug: str, steps: list[str]) -> str:
    step_objs = [
        {
            "@type": "HowToStep",
            "position": i + 1,
            "name": s[:120],
            "text": s,
        }
        for i, s in enumerate(steps)
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "description": description,
        "image": cover,
        "step": step_objs,
    }
    return json.dumps(data, indent=2)


def faq_schema(pairs: list[tuple[str, str]]) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }
    return json.dumps(data, indent=2)


def closing_blocks(
    cluster: str,
    derivative: list[str],
    faq: list[tuple[str, str]],
    extra_links: list[tuple[str, str]] | None = None,
    images: list[tuple[str, str]] | None = None,
) -> str:
    deriv_md = "\n".join(f"{i}. {s}" for i, s in enumerate(derivative, 1))
    faq_md = "\n".join(f"**Q: {q}**\n\nA: {a}\n" for q, a in faq)
    links = list(VERIFIED_LINKS[:12])
    if extra_links:
        links = extra_links + links
    links_md = "\n".join(f"| {a} | `{t}` |" for a, t in links[:14])
    imgs = images or [
        ("Hero workspace overview", "Lovart ChatCanvas workspace for tutorial"),
        ("Step-by-step UI panel", "Lovart Design Agent step workflow"),
        ("Brand Kit color and type lock", "Lovart Brand Kit enforcing visual system"),
        ("Before and after edit comparison", "Semantic edit before and after in Lovart"),
        ("Export formats row PNG SVG MP4", "Lovart export formats for design deliverables"),
        ("Multi-format campaign grid on canvas", "Multi-format designs on Lovart ChatCanvas"),
    ]
    img_md = "\n".join(
        f"| {i} | {d} | {alt} |" for i, (d, alt) in enumerate(imgs, 1)
    )
    return f"""
---

## Derivative Scenarios

{deriv_md}

---

## FAQ

{faq_md}

---

## E-E-A-T Signals

| Dimension | Signal |
|-----------|--------|
| **Experience** | Workflows mirror onboarding, support tickets, and creator community questions from 2025–2026 Lovart production use—not theoretical feature lists. |
| **Expertise** | Terminology matches Lovart product docs: ChatCanvas, MCoT, Brand Kit, Touch Edit, Edit Elements, Identity Lock, and integrated models (Nano Banana, Seedance, Veo 3). |
| **Authoritativeness** | Lovart is the platform publisher; cross-links point only to verified `/blog/` slugs and official pricing/signup URLs. |
| **Trustworthiness** | Limitations (credit usage, model choice, export specs) stated plainly; hybrid stacks with templates or specialist tools acknowledged where relevant. |

## Internal Links

| Anchor Text | Target |
|-------------|--------|
{links_md}

## Image Appendix

| # | Description | Alt Text |
|---|-------------|----------|
{img_md}

---

*Article for blogs.lovart.ai. Part of {cluster} content cluster.*
"""


def assemble_frontmatter(meta: dict, structured: str) -> str:
    kw = meta["keywords"]
    tags = meta["tags"]
    kw_yaml = "\n".join(f'  - "{k}"' for k in kw)
    tags_yaml = "\n".join(f'  - "{t}"' for t in tags)
    cover = meta.get("cover_url") or pick_cover_url(meta["slug"])
    alt = meta.get("alt_text") or f'{meta["focus_keyword"]} — Lovart AI Design Agent blog cover'
    return f"""---
title: "{meta['title']}"
slug: {meta['slug']}
date: "{meta['date']}"
language: en
page_type: Blog Post
category: Lovart 101
author: Lovart Content Team
description: "{meta['description']}"
estimated_read: "{meta.get('estimated_read', '18 min')}"
difficulty: {meta.get('difficulty', 'beginner')}
tool: "{meta['tool']}"
focus_keyword: {meta['focus_keyword']}
keywords:
{kw_yaml}
tags:
{tags_yaml}
seo_title: "{meta['seo_title']}"
seo_description: "{meta['seo_description']}"
seo_schema: {meta['seo_schema']}
cover_url: {cover}
alt_text: {alt}
status: draft
content_cluster: "{meta['content_cluster']}"
internal_note: "{meta.get('internal_note', '')}"
structured_data_json: |
  {structured}
---
"""


def write_draft(filename: str, meta: dict, body: str, structured: str) -> int:
    text = assemble_frontmatter(meta, structured) + "\n" + body
    path = DRAFTS / filename
    path.write_text(text, encoding="utf-8")
    return len(text.split())
