"""Shared helpers for How-To / Branding / Insight batch generation."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFTS = ROOT / "01-Drafts"
PICK_COVER = ROOT / "scripts" / "pick-cover.py"

SIGNUP = "https://lovart.ai/signup"
PRICING = "https://lovart.ai/pricing"

STANDARD_LINKS = [
    ("ChatCanvas getting started", "/blog/05-pillar-getting-started-lovart"),
    ("Brand Kit guide for every industry", "/blog/complete-guide-brand-kit-every-industry-lovart"),
    ("how to chat and generate any design type", "/blog/how-to-chat-generate-any-design-type-lovart-agent"),
    ("Brand Kit setup in five minutes", "/blog/brand-kit-setup-5-minutes-lovart-best-practice"),
    ("Lovart signup", SIGNUP),
    ("Lovart pricing", PRICING),
]


def pick_cover_url(slug: str) -> str:
    lines = subprocess.check_output(
        ["python3", str(PICK_COVER), slug], text=True, cwd=str(ROOT)
    ).strip().splitlines()
    return [ln for ln in lines if ln.startswith("http")][0]


def howto_schema(title: str, description: str, cover: str, steps: list[str]) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "description": description,
        "image": cover,
        "step": [
            {"@type": "HowToStep", "position": i + 1, "name": s[:100], "text": s}
            for i, s in enumerate(steps)
        ],
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
) -> str:
    deriv_md = "\n".join(f"{i}. {s}" for i, s in enumerate(derivative, 1))
    faq_md = "\n".join(f"**Q: {q}**\n\nA: {a}\n" for q, a in faq)
    links = list(extra_links or []) + STANDARD_LINKS
    seen = set()
    uniq: list[tuple[str, str]] = []
    for a, t in links:
        if t in seen:
            continue
        seen.add(t)
        uniq.append((a, t))
    links_md = "\n".join(f"| {a} | `{t}` |" for a, t in uniq[:16])
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
| **Experience** | Workflow reflects production teams shipping real campaigns on Lovart—not generic AI art tips. |
| **Expertise** | Uses Lovart product vocabulary: ChatCanvas, Brand Kit, MCoT, Touch Edit, Text Edit, Edit Elements, Identity Lock. |
| **Authoritativeness** | Published by Lovart; internal links limited to verified `/blog/` slugs. |
| **Trustworthiness** | States export specs, platform rules, and when human QA or legal review is required. |

## Internal Links

| Anchor Text | Target |
|-------------|--------|
{links_md}

## Image Appendix

| # | Description | Alt Text |
|---|-------------|----------|
| 1 | Hero mockup of finished deliverable on device | Lovart how-to hero mockup for channel deliverable |
| 2 | ChatCanvas workspace with Brand Kit panel | Lovart ChatCanvas Brand Kit applied to project |
| 3 | Step workflow with prompt and output | Lovart Design Agent prompt to output workflow |
| 4 | Touch Edit or Text Edit refinement UI | Semantic edit refinement in Lovart |
| 5 | Multi-format export grid same brand | Multi-format export from one Lovart brief |
| 6 | Before and after quality fix | Before and after Lovart design correction |

---

*Article for blogs.lovart.ai. Part of {cluster} content cluster.*
"""


def assemble_frontmatter(meta: dict, structured: str) -> str:
    kw_yaml = "\n".join(f'  - "{k}"' for k in meta["keywords"])
    tags_yaml = "\n".join(f'  - "{t}"' for t in meta["tags"])
    cover = meta.get("cover_url") or pick_cover_url(meta["slug"])
    return f"""---
title: "{meta['title']}"
slug: {meta['slug']}
date: "{meta['date']}"
language: en
page_type: Blog Post
category: {meta['category']}
author: Lovart Content Team
description: "{meta['description']}"
estimated_read: "{meta.get('estimated_read', '11 min')}"
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
alt_text: {meta.get('alt_text', meta['focus_keyword'] + ' — Lovart AI Design Agent blog cover')}
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
