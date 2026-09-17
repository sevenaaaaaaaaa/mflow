---
name: lovart-101
description: End-to-end Lovart 101 / Getting Started (入门与枢纽指南) content production sub-skill. Translates foundational AI design concepts, prompting parameters, and 
---

# lovart-101 — Introductory & Hub-Page Content Production Sub-Skill

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/scripts/optimize_complete_guides.py` |
| 本 Skill | `1-1 Harness/Skills/02-creation/lovart-101/SKILL.md` |

End-to-end Lovart 101 / Getting Started (入门与枢纽指南) content production sub-skill. Translates foundational AI design concepts, prompting parameters, and terminology into highly readable, high-retention hub pages designed for broad search traffic and Topic Cluster building.

先加载 `lovart-core`、`lovart-blog`、`lovart-content-quality-gates`，并遵守：
`1-1 Harness/Skills/02-creation/references-blog-subskill-governance.md`

## Triggers

- "write a 101 guide about {topic}"
- "write an introductory guide / getting started guide"
- "写 101 教程 / 入门指南"
- "prompting 101"
- "getting started with {tool/concept}"

---

## Core DNA (Pillar 101 Design Guidelines)

Unlike expert Complete Guides, a "Lovart 101" article is designed to **demystify complexity** and act as a **structural router (Topic Cluster Hub)**. It must follow a strict **8-part layout** of **≥7,500 words** (universal blog floor 2026-07-17) with high readability scores (Flesch-Kincaid ≤8th-grade level).

### Banned AI-Slop Words (Strict BLOCK)
- **NEVER use**: `unlock`, `revolutionize`, `seamless` (use *frictionless*, *smooth*, *organic*, or *natural*), `empower`, `game-changer`, `cutting-edge`, `leverage` (use *scale*, *value*, or *impact*), `"in today's fast-paced"`, `"the future of"`.
- **ZH Banned**: `赋能`, `闭环`, `颠覆性`, `一站式解决方案`, `在当今快节奏`, `解锁.*潜力`, `无缝衔接`, `未来可期`.

---

## 4 Core Content Frameworks (Must Integrate)

### 1. The 3-Part Structured Prompt Formula
Teach beginners to write prompts using a rigorous, logical structure instead of listing loose keywords:
- **Part 1: The Subject**: Who or what is the main focus? Define age, clothing, pose, and expression specifically (e.g., `"A professional headshot of a female executive in her late thirties wearing a navy blazer, looking directly at the camera with a confident smile"`).
- **Part 2: The Context/Environment**: Where is the subject sitting or standing? Define the background clearly to prevent random AI artifacts (e.g., `"standing in a soft-blurred, sun-drenched modern office corridor"`).
- **Part 3: Style & Photographic Parameters**: Define the lighting setup, camera choice, lens focal length, and color grading (e.g., `"three-point studio softbox setup, shot on Fujifilm with a 50mm lens, f/1.8 shallow depth of field, warm color grading"`).

### 2. Photographic Parameters as Styling Levers
Demystify technical camera variables, showing readers how to use them as direct inputs for style control:
- **Focal Lengths (焦距)**:
  - `18mm - 24mm`: Wide-angle landscapes and immersive perspective distortion.
  - `50mm`: The "standard lens" — matches natural human sight, zero distortion, perfect for portraits.
  - `85mm - 135mm`: Telephoto compression — flattens features and creates beautiful blurry backgrounds (bokeh).
- **Specialist Lenses**:
  - `Fisheye`: 180° curved bubble distortion.
  - `Tilt-Shift`: Miniature model city effect.
  - `Lensbaby`: Dreamy, soft-focus selective blur.
- **Aperture (光圈)**:
  - `Wide (f/1.4 - f/2.8)`: Blurs the background, putting a spotlight on the subject.
  - `Narrow (f/11 - f/22)`: Sharp focus everywhere, perfect for vast landscapes or architecture.
- **Shutter Speed (快门速度)**:
  - `Fast (1/1000s)`: Freezes fast-moving actions (splashes, sports, athletic sprints).
  - `Slow (1/2s - 2s)`: Captures movement over time, creating silky water or light trails.

### 3. Terminology Demystification Glossary
Every 101 guide must feature a Markdown-table Glossary early in the article, defining complex concepts in simple terms:
- **Flat JPEGs vs. Layered PSDs**: A flat JPEG is a single, merged image where any edit forces a complete re-roll. A layered PSD separates backgrounds, subjects, and text onto individual, editable layers.
- **Rerolls vs. Surgical Inpainting (Touch Edit)**: A reroll regenerates the entire image, losing your preferred composition. Surgical inpainting patches only the specific area you select.
- **Scaleable Vectors (SVG) vs. Raster Pixels (PNG)**: A PNG is made of pixels that blur when stretched. An SVG is made of math (Bézier curves) that scales infinitely with perfect sharpness.

### 4. Topic Cluster Hub-and-Spoke Routing
As a 101 Hub Page, the article's job is to capture broad search intent and route traffic deeper into relevant articles.
- Include a dedicated `"Next Steps: Deeper Guides"` section before the FAQ.
- Anchor text must use exact keyword strings (e.g., `"[Complete Guide to AI Art Platform Selection 2026](/blog/complete-guide-ai-art-platform-selection-2026)"`).

---

## 8-Chapter Standardized 101 大纲 (Heading Hierarchy)

Every 101 guide must follow this unified大纲 structure exactly:

```markdown
# [Title: Introductory Keyword + Qualifier + Value Proposition (2026)]

## 1. Quick Overview (TL;DR)
[3-5 highly readable Bullet Points defining what this is and who it is for]

## 2. What Is [Concept/Tool] 101?
[Simple, non-technical explanation. Introduces the core definition and historical context]
### The Evolving Role of the Creator
[How the user shifts from a manual pixel-level drafter to a structural Creative Director]

## 3. Terminology Demystification Glossary
[Markdown table comparing concepts: Flat vs. Layered, PNG vs. SVG, Reroll vs. Touch Edit]

## 4. The 3-Part Prompt Formula
[Detailed walkthrough of Subject, Context, and Style/Parameters]
### Photographic Parameters as Direct Styling Levers
[Paragraphs explaining focal lengths, apertures, shutter speeds, and special lenses]

## 5. Practical Prompt Templates You Can Use Right Now
### Template 1: [e.g., Professional Headshot]
[Detailed, copy-paste prompt template with bracketed placeholders]
### Template 2: [e.g., Product Showcase]
[Detailed, copy-paste prompt template with bracketed placeholders]
### Template 3: [e.g., Creative Atmosphere]
[Detailed, copy-paste prompt template with bracketed placeholders]

## 6. Common Beginner Mistakes and How to Avoid Them
### Mistake 1: [e.g., Listing Random Keywords]
[Why it confuses the AI model and the structural fix]
### Mistake 2: [e.g., Overcomplicating Details]
[Why it leads to prompt compression and the structural fix]
### Mistake 3: [e.g., Over-reliance on Flat JPEGs]
[The layer-isolation fix using Lovart's separate vector layer system]

## 7. Next Steps: Deeper Guides
[A clean bullet list routing readers to deeper, relevant complete guides with exact anchors]

## 8. FAQ
[5-8 clean, helpful Q&As answering beginner objections, commercial safety, and cost queries]
```

---

## Workflow Checklist (Before Publish)

- [ ] **Preflight**: Run `node anti-slop-preflight.js --file path/to/article.md --pro`
- [ ] **Slop Check**: Ensure 0 occurrences of `leverage`, `seamless`, or `unlock`.
- [ ] **Word Count**: Verify final word count is ≥7,500 words.
- [ ] **Hierarchy**: Ensure H2 headings match the 8-chapter 101 format exactly.
- [ ] **FAQ Check**: Ensure the H2 is `"FAQ"` exactly to satisfy preflight checks.

## References

Read [references/benchmark-seed-v1.md](references/benchmark-seed-v1.md) for the first 101 benchmark base and five core beginner topic lanes.

Read [references/benchmark-seed-v2.md](references/benchmark-seed-v2.md) to extend coverage into branding basics, team-friendly prompting basics, and on-brand generation basics.

Read [references/benchmark-seed-v3.md](references/benchmark-seed-v3.md) to improve tone range, system-bridge teaching, and beginner-to-advanced learning transitions.

Read [references/lovart-101-playbook.md](references/lovart-101-playbook.md) for the hub-page writing rules, next-step routing logic, and anti-patterns.

Read [references/lovart-101-review-checklist.md](references/lovart-101-review-checklist.md) before approving a draft.
