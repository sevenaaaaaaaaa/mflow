---
name: lovart-complete-guide
description: End-to-end Lovart Complete & Ultimate Guide (完整与终极指南) content production: market research → writing → high-availability translation → publishing. Tran
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# lovart-complete-guide — Complete & Ultimate Guide Content Production

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Geo Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Geo Dev/scripts/` |
| 自动化 | `1-4 Dev/scripts/optimize_complete_guides.py` |
| 本 Skill | `1-1 Harness/Skills/02-creation/lovart-complete-guide/SKILL.md` |

End-to-end Lovart Complete & Ultimate Guide (完整与终极指南) content production: market research → writing → high-availability translation → publishing. Translates advanced prompting, high-fidelity models, and human-AI design frameworks into authoritative, long-form pillar content.

## Triggers

- "write a complete guide about {topic}"
- "ultimate guide about {topic}"
- "写完整指南 / 终极指南"
- "深度长文"
- "ultimate prompting guide"

---

## Core DNA (Pillar Guide Design Guidelines)

To match the "Industry Gold Standard" for Complete and Ultimate Guides, every post must be structured as a **10-Chapter Standardized H2 Book** of **≥7,500 words** with zero AI-slop words. It must replace generic advice with parameter-level mechanics and first-person case studies.

### Banned AI-Slop Words (Strict BLOCK)
- **NEVER use**: `unlock`, `revolutionize`, `seamless` (use *frictionless*, *smooth*, *organic*, or *natural*), `empower`, `game-changer`, `cutting-edge`, `leverage` (use *scale*, *value*, or *impact*), `"in today's fast-paced"`, `"the future of"`.
- **ZH Banned**: `赋能`, `闭环`, `颠覆性`, `一站式解决方案`, `在当今快节奏`, `解锁.*潜力`, `无缝衔接`, `未来可期`.

---

## 4 Core Content Frameworks

### 1. The CRAFT Prompt Framework (Multimodal Control)
When writing about multimodal video (such as Seedance 2.0 or Veo 3.1), instruct readers to use the **CRAFT** prompting system instead of random keywords:
- **C — Context (环境背景)**: Establish the location, period, ambient lighting, and style references (e.g., `@[Image 1] as environment reference`).
- **R — Reference (资产指定)**: Explicitly map `@` mentions to their exact functional role (e.g., `@[Image 2] for character face, @[Video 1] for walking motion`).
- **A — Action (动态编排)**: Chronologically describe physical subject movements and dynamics (e.g., `runs to the desk, studies the photo intensely`).
- **F — Framing (镜头编排)**: Define cinematic camera work, focal distance, and transitions (e.g., `dolly shot circling subject, tracking from behind, 24fps`).
- **T — Timing & Sync (时间与音轨同步)**: Manage progressive timeline cuts and audio-beat synchronization (e.g., `0-4 seconds: panning; at 5-second beat, cut on @[Audio 1] drop`).

### 2. Prompting like a Creative Director (High-Density Styling)
For image-generation guides (such as Nano Banana Pro), replace generic descriptors with specialized photographic and material terms:
- **Lighting Design**: Softbox setups (e.g., `three-point softbox setup`), high-contrast shadows (e.g., `Chiaroscuro lighting, harsh side light`), or gold accents (e.g., `golden hour backlighting`).
- **Camera & Lens Choice**: Specific hardware bodies (e.g., `shot on Fujifilm for authentic color science`, `GoPro fisheye lens for immersive action`, or `disposable camera for raw flash aesthetic`) and aperture values (e.g., `f/1.8 shallow depth of field`, `macro lens for fine crevices`).
- **Color Grading & Film Stock**: Authentic textures (e.g., `1980s color film grain, muted teal cinematic color grading`) over flat digital renders.
- **Materiality & Texture Detail**: Direct tactile specifications (e.g., `navy blue tweed fabric weave`, `polished chrome metal label with gold leaf engraving`, `matte ceramic coffee glaze`).

### 3. Advanced Multimodal Workflow Operations (Seedance & Nano Banana Pro)
Always include concrete step-by-step instructions for these high-leverage production workflows:
- **Video Extension & Continuity**: Chaining narrative continuation based on ending frame analysis, select exact extension seconds (e.g., 5-8 seconds) and define connecting movements.
- **Video Fusion**: Creating smooth bridging transitions to connect two distinct scenes or locations without harsh jump cuts.
- **Character Replacement**: Swapping actors in existing footage while holding camera pan and gesture geometry frame-by-frame.
- **Storyline Subversion**: Altering narrative plot points (e.g., turning a proposal into a high-stakes standoff) on identical setups to test creative variants.
- **Vector Tiling & Tracing**: Using Seamless Tiling coordinates to generate repeatable packaging backgrounds, and running Vector Trace to convert raster edges into sharp, scaleable SVG assets for print.

### 4. Human-AI Interface & Design Frameworks (PAIR, HAX, IBM Essentials)
For enterprise-level guides, explain how teams design human-centered AI products:
- **Explainability & Mental Models**: Making non-deterministic, probabilistic AI decisions transparent to users (e.g., using Google's Explainability Rubric).
- **Graceful Failures & Error Handling**: Designing feedback loops (like Lovart's Touch Edit or separate vector text layers) to easily fix spelling distortions, limb anomalies, or texture smoothing without re-rolling the entire image.

---

## 10-Chapter Standardized大纲 (Heading Hierarchy)

Every guide must adopt this unified hierarchy. Use H2 for main chapters and H3 for sub-sections to ensure perfect layout consolidation.

### H2 Structure

```markdown
# [Title: Core Keyword + Qualifier + Value Proposition (2026)]

## 1. Why This Matters in 2026
[Quick Overview / TL;DR (3-5 Bullet points)]
[Paragraphs with 2026 industry data (Adobe/McKinsey etc.) with specific percentages]

## 2. The Lovart Workflow Formula and Team Playbook
[Explanation of context, constraints, canvas, correction, and conversion]
### Best Workflow by Team Size and Budget
[Tailored strategies for solo operators, brand teams, and high-volume agencies]

## 3. Comparison Matrix and Platform Selection Guide
[Comparison of template-first, image-only, desktop design, and editable AI workflows]

## 4. Advanced Prompt Architecture and Steering Mechanics
[Explanation of prompt layering: Role, Assignment, Audience, Style, and Constraints]
[Separation of expansive generation prompts from surgical repair prompts]

## 5. Step-by-Step Walkthrough: [Custom Case Study Scene]
[First-person "I tested..." real-world case study with concrete numbers, timelines, and budgets]
### Managing Real-World Stakeholder Sign-offs
[Structuring approval criteria across internal clarity, stakeholder confidence, and production readiness]

## 6. Common Pitfalls and Parameter-Level Fixes
### Pitfall 1: [Specific Technical Pain Point]
[Specific parameters and tool settings to fix it inside Lovart]
### Pitfall 2: [Specific Technical Pain Point]
[Specific parameters and tool settings to fix it inside Lovart]
### Pitfall 3: [Specific Technical Pain Point]
[Specific parameters and tool settings to fix it inside Lovart]
### When Lovart Is Not the Best Fit
[Explicit anti-recommendations and when to stay in traditional desktop software]

## 7. Operational Playbook and 30-Day Rollout Strategy
[Establishing prompt structures, naming conventions, and team approval logic]
### The 30-Day Rollout and Implementation Calendar
[Detailed week-by-week plan: Week 1 Foundations, Week 2 Systems, Week 3 Revisions, Week 4 Handoff]
### Handoff Packages and Operational Continuity
[Documenting approved visual rules and repair vocabularies for seamless team transition]

## 8. Advanced Quality Control and Performance Metrics
[Composition, realism, channel fit, brand fit, and derivative resilience passes]
### Measuring Workflow Efficiency and ROI
[Tracking time-to-approval, derivative count, and downstream labor savings]
### Pre-Publish Verification Checklist
[5-step tactical pre-flight list before final asset export]

## 9. FAQ
[10-12 highly specific, defensive Q&As addressing cost, copyright, and custom parameters]

## 10. Key Takeaways and Final Word
[3-5 highly distilled action bullet points]
**[A bold, insightful, quotable closing sentence of ≤20 words]**
```

---

## Workflow (sequential)

### Phase 0: Market Research & SERP Scan
- Verify the slug doesn't already exist.
- Scan top 3-5 competitor pages on Google SERP. Record their word counts, H2 structure, and weak spots. Write to `{slug}-research.md`.

### Phase 1: Outline Planning
- Structure the article with H2s matching the Standardized 10-Chapter đại cương exactly.

### Phase 2: Writing & Anti-Slop Audit
- Write in high-density, first-person narrative. Split into sections if word count limits apply during generation.
- Run `lovart-quality-gates` / `anti-slop-preflight.js` to audit slop words.

### Phase 3: High-Availability Translation
- **DO NOT translate the whole file at once**. Use paragraph-by-paragraph translation engines (e.g. `translate_markdown_v3.py`) to prevent HTTP 500 errors.
- Rewrite for natural Chinese/target locale tone. Keep brand terms, code blocks, and markdown formatting intact.
- Translate and insert CTA blocks right before the `## FAQ` heading.

### Phase 4: Publishing & IndexNow
- Convert Markdown to Portable Text and patch to Sanity CMS. Verify online URL returns HTTP 200.
- Submit the updated URLs using `indexnow_submit.py` for immediate indexing.
