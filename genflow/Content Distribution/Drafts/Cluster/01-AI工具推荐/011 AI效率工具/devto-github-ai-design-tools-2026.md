---
track: native
platform: devto
language: en
offsite_title: "Four GitHub Projects That Turn AI Agents Into Design and Video Pipelines"
approved: false
content_id: github-ai-design-tools-2026-06-09__devto
tags: [ai, opensource, design, productivity]
---

# Four GitHub Projects That Turn AI Agents Into Design and Video Pipelines

If you still think of LLMs as chat widgets, 2026 GitHub trending repos will change your mind. The fastest-growing projects this year do not optimize for longer essays—they ship **artifacts**: runnable UI code, exportable decks, desktop prototypes, and short videos you can actually post.

I picked four open-source tools that are genuinely breaking skill barriers for developers, founders, and solo creators. Each section covers **the pain → how it works → a concrete scenario**. Every tool below is worth starring before you try it.

---

## 1. screenshot-to-code — design handoff as a compile step (72k+ stars)

**Repo**: https://github.com/abi/screenshot-to-code  
**Site**: https://screenshottocode.com

The classic bottleneck is not ideas—it is **Figma-to-code**. Engineers spend days matching pixels; every spacing tweak resets the clock. screenshot-to-code flattens that stack: drop a screenshot (or Figma export), pick React+Tailwind / Vue / HTML+CSS, get runnable code back.

Stack: React/Vite frontend, FastAPI backend, MIT license. Models include Gemini 3, Claude Opus 4.5, GPT-5.x. The experimental **screen-recording → prototype** path is underrated: record a competitor flow, get interactive code to fork.

It will not replace thoughtful component architecture, but it compresses **0→60% fidelity** from days to minutes. Always review generated code—that is engineering hygiene, not a product flaw.

**Scenario**: You spot a dashboard layout on Dribbble, screenshot it, generate a React shell, then let Cursor wire up your API mocks for a weekend demo.

---

## 2. Open Design — DESIGN.md + Skills as an agent-native design runtime (61k+ stars)

**Repo**: https://github.com/nexu-io/open-design  
**Site**: https://open-design.ai

Anthropic’s Claude Design proved LLMs can ship design deliverables. Open Design (Apache-2.0) is the **open, local-first** answer: BYOK, forkable, no cloud lock-in.

Core idea: portable **`DESIGN.md`** systems (150+ presets—Linear, Vercel, Stripe, Apple…) plus 100+ Skills (`saas-landing`, `dashboard`, `wireframe-sketch`, deck modes…). It does not bundle an agent—you bring Cursor, Claude Code, Codex, Copilot, Gemini CLI, OpenCode, Qwen, or 17+ other CLIs. Output renders in a sandboxed iframe and exports to **HTML / PDF / PPTX / MP4**, including HyperFrames motion.

For teams already living in coding agents, this turns “someone should mock a landing page” into a **scripted, repeatable** workflow instead of a Figma side quest.

**Scenario**: Pick the Vercel-style `DESIGN.md`, prompt Cursor CLI for a SaaS landing with pricing + FAQ, export HTML into your Next.js monorepo the same afternoon.

---

## 3. Open CoDesign — desktop streaming artifacts in under 90 seconds (6k stars)

**Repo**: https://github.com/OpenCoworkAI/open-codesign

Open Design is a platform; Open CoDesign is a **personal desktop loop**. MIT-licensed Electron app, local-first, BYOK across Claude, GPT, Gemini, DeepSeek, Kimi, GLM, Ollama, OpenRouter.

Import your Claude Code / Codex keys—or sign in with ChatGPT—and stream HTML/JSX into an on-device iframe preview. Interrupt generation mid-flight, export PDF for stakeholders or HTML for engineers. Think of it as the fastest way to **trial multiple models on the same brief** without standing up a full design system first.

**Scenario**: Hackathon eve: three landing variants from local Ollama, pick one at breakfast, ship copy tweaks before demo time.

---

## 4. libtv-skills — DAG video pipelines inside your agent toolchain (737+ stars)

**Repo**: https://github.com/libtv-labs/libtv-skills  
**Product**: https://www.liblib.tv/

Video agents usually fail on **control**. End-to-end models give you an MP4 black box. LibTV uses a **DAG of nodes** (script, image, video, audio); libtv-skills exposes that graph to OpenClaw / Claude Code.

You prompt in the terminal; the agent runs scripting, storyboards, subject-library face lock, and renders. You get a video **plus** an editable canvas URL—fix lighting on shot three without re-running the entire pipeline.

**Scenario**: Tell OpenClaw “30-second API gateway explainer, six shots, tech tone.” Five minutes later, tweak one node, publish.

---

## How to combine them

| Pain | Start here |
|------|------------|
| UI from pixels | screenshot-to-code |
| Systematic prototypes / decks | Open Design |
| Fast desktop drafts | Open CoDesign |
| Agent-driven video | libtv-skills |

These four cover **open-source 0→60%**. When you need brand-grade campaign consistency across image and video, layer a Design Agent such as [Lovart](https://www.lovart.ai?utm_source=devto&utm_medium=native&utm_campaign=github_ai_tools_2026) on top—not instead of—the stack above.

---

Which one are you shipping with? Drop your stack in the comments—I will update this list based on real deployments.
