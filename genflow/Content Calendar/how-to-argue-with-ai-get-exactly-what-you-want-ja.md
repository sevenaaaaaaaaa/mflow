---
title: "【日本語】 The Iteration Loop: 方法 Politely Argue with AI to Get Exactly What You Want"
date: 2026-05-10
category: "The Field Guide"
keywords: ["ai prompt iteration", "fix ai design", "ai refinement tips"]
slug: "how-to-argue-with-ai-get-exactly-what-you-want"
author: "Lovart Content Team"
description: "Master the art of iterative refinement with AI design tools. Learn the specific language patterns that fix what's wrong without starting over from scratch."
image: "/images/blog/argue-with-ai-hero.jpg"
reading_time: "9 min"
language: ja
---

Here's a scene that happens every day in Lovart's usage data: someone writes a prompt, gets a result that's 70% right, and deletes the whole thing to start over. They type a fresh prompt from scratch, hoping word choice will fix what instinct didn't.

The prompt is fine. The instinct is right. What's missing isn't a better first prompt — it's a better second prompt. The iteration loop — the back-and-forth of targeted corrections — is where the work actually happens. Here's how to get good at it.

---

## The "Don't Start Over" Rule

[IMAGE 1 PLACEHOLDER — Persona Scenario]

Before we get into specific techniques, one rule: never clear the canvas and start over unless the entire composition is wrong. Starting over discards information. The AI model already knows what you're trying to build — it just got some details wrong. Treat it like a junior designer who handed you a draft: you wouldn't fire them and hire someone new. You'd give revision notes.

Every time you start fresh, you lose the shared context of the previous generation. The model forgets the good parts along with the bad ones. Iterative refinement preserves the 70% that worked while targeting the 30% that didn't.

---

## Technique 1: The Specificity Sandwich

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

The most common iteration mistake is vague criticism. "Make it better" tells the model nothing. "It looks weird" doesn't identify what's weird.

The specificity sandwich works in three layers:

1. **Identify the element** — click it with Touch Edit, or name it explicitly: "the headline font," "the lighting on the product," "the background color"
2. **Diagnose what's wrong** — not "bad" but "too small," "too dark," "too formal," "clashing with the brand blue"
3. **Prescribe the fix** — "increase to 48pt," "warm the color temperature," "switch to a rounded sans-serif"

Bad iteration prompt: *"The ad doesn't look professional."*

Good iteration prompt: *"The product shadow is too harsh — soften the drop shadow under the bottle by 50% and add a subtle rim light on the top edge. Keep everything else identical."*

The phrase "keep everything else identical" is a signal that belongs in almost every iteration prompt. It tells the model: this is a surgical edit, not a redesign.

---

## Technique 2: Negative Space Instructions

Sometimes saying what you *don't* want is more effective than saying what you *do* want. Negative instructions work because they shrink the probability space. You're eliminating options rather than prescribing one.

Pattern: *"Regenerate the background, but — no gradients, no abstract shapes, no stock-photo office. Use a solid warm color or a real photographed texture."*

Each exclusion narrows the output. Three exclusions plus one positive direction is often more precise than a long positive description.

---

## Technique 3: The Reference Anchor

When words fail, use an image. Lovart's Style Picker lets you upload a reference image that captures the aesthetic you're aiming for. The model extracts style properties — color palette, composition patterns, typographic weight — and applies them to your existing canvas without replacing your content.

Prompt pattern: *"Apply the visual style from this reference image to my current canvas. Keep my layout and text placement. Only change: background treatment, color grading, and font styling."*

This technique is especially useful when you know something feels off but can't name it. The reference image does the naming for you.

---

## Technique 4: Component Isolation

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

Lovart's Touch Edit lets you click individual elements on the canvas and modify them independently. The power of this feature isn't just convenience — it's that isolated edits don't disturb the rest of the composition.

Click the CTA button → "Make this a rounded pill button, same green but 20% darker."

The model will change the button. The headline stays. The background stays. The character stays. The layout stays.

This is the closest thing to Photoshop layers that exists in AI-native design. Use it heavily. The more you isolate edits, the fewer things can randomly change.

---

## Technique 5: The Incremental Drift Check

After 4-5 iterations, pause and compare your current canvas to your original generation. Sometimes you drift. Each small fix makes sense individually, but the cumulative effect pulls the design in a direction you didn't intend.

Save your intermediate generations. Lovart keeps a history, but naming and bookmarking key versions helps. If you drift, roll back to the last version that felt directionally correct and fork from there.

---

## The Psychology of Iterating with AI

There's an emotional pattern to using AI design tools that nobody talks about. Generation 1: excitement. Generation 2: mild disappointment. Generations 3-5: frustration as you can't quite articulate what's wrong. Generation 6: breakthrough, because you finally found the right three words that fixed everything.

This is normal. The tool isn't broken. You're not bad at prompting. The process is learning what your own taste actually means, translated into language another system can act on. It takes practice — the same way briefing a human designer takes practice, even though you speak the same language.

---

## Image Appendix

| Image | Description | Placement |
|-------|-------------|-----------|
| specificity-sandwich-diagram.jpg | Visual diagram of the 3-layer feedback structure | Technique 1 |
| before-after-iteration.jpg | Side-by-side: original 70% result → 3-iteration refined result | Technique 1 |
| negative-space-prompt-example.jpg | Screenshot of a negative instruction prompt and the cleaner result | Technique 2 |
| style-picker-reference.jpg | The Style Picker UI with a reference image loaded | Technique 3 |
| touch-edit-isolation.gif | Screen recording of Touch Edit modifying a single element | Technique 4 |
| drift-comparison.jpg | Four versions showing incremental drift vs. an anchor version | Technique 5 |

---

[IMAGE 4 PLACEHOLDER — Brand CTA]

## FAQ

**How many iterations should I expect before a design looks right?**
For simple social graphics, 1–3 iterations. For complex compositions with multiple elements (products, text, characters, backgrounds), 3–6 iterations is normal. If you exceed 8 iterations without getting close, the problem is usually your initial prompt, not your iteration technique — consider restarting with a more specific foundation.

**Does iterating cost more credits than generating new images?**
Touch Edit operations count as credit usage, but they typically use fewer credits than a full regeneration because they modify less. The exact ratio depends on your plan. The free tier includes Touch Edit functionality.

**Why does the model sometimes change things I didn't ask it to change?**
This is called "compositional drift" and it's a known characteristic of diffusion-based AI models. Asking the model to change one element sometimes nudges adjacent elements. Mitigation: use Touch Edit for surgical changes, and include "keep everything else identical" in your prompt.

**Can I iterate on text the same way I iterate on images?**
Yes, but text rendering in AI image models has inherent limitations. For best results with typed copy, use Lovart's dedicated text tool to place and style text after the visual is locked. Don't rely on the generative model for precise text rendering.

**What's the difference between Lovart's iteration and Midjourney's variations?**
Midjourney variations are random explorations of the prompt space — you get four new interpretations of the same description. Lovart's iteration is directed: you specify what to change, and the model targets that element. One is exploration. The other is refinement.

**How do I know when a design is "done" during iteration?**
When the remaining issues are things nobody but you would notice, and fixing them would take more time than the improvement is worth. If you're adjusting individual pixels of shadow opacity, you're in over-editing territory. See our guide on knowing when to stop.

---

## Internal Links

- [From Idea to Posted — A 5-Minute AI Design Workflow for Busy Founders](/blog/5-minute-workflow-busy-founders-ai-design/)
- [The Style Picker — How to Borrow Professional Aesthetics Without Knowing Design Theory](/blog/style-picker-borrow-professional-aesthetics-ai/)
- [Over-Editing — How to Know When to Stop Tweaking and Export](/blog/over-editing-when-to-stop-tweaking-design/)
- [Prompting for Repairs — What Words Actually Work When Asking AI to Fix a Mistake](/blog/prompting-for-repairs-words-to-fix-ai-mistakes/)

---

*Elena Vasquez spent six years as a creative director at a mid-size agency before moving into product. She now runs a design operations consultancy and has written extensively about human-AI collaboration workflows. She's been testing Lovart since its beta and contributed to the prompt engineering patterns described in this guide.*

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create a design — warm natural lighting, candid documentary style

**Image 2 — The Conceptual Diagram**:
A hand-drawn sketch diagram showing the step-by-step workflow for creating designs with AI — clean line art on grid paper, arrows connecting each step, minimalist style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]

**Image 4 — Brand CTA**:
Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in Untitled — modern, aspirational, cinematic lighting

