---
language: en

title: "Ugly to Lovely — We Took a Bad MS Paint Drawing and Let AI Fix It"
date: 2026-05-10
category: "The Journey"
keywords: ["fix bad design ai", "ai design makeover", "before after ai design"]
slug: "ugly-to-lovely-ms-paint-to-ai-makeover"
author: "Lovart Content Team"
description: "A case study: we drew a deliberately terrible product concept in MS Paint, fed it to Lovart as a reference, and watched AI transform it into professional marketing material in 3 steps."
image: "/images/blog/ugly-to-lovely-hero.jpg"
reading_time: "9 min"
---

This article begins with a confession: the drawing at the top of this section was made in MS Paint in approximately 90 seconds. It depicts a hypothetical smart water bottle. The bottle is a lopsided rectangle with a crooked triangle for a lid. There is a jagged blue line that is supposed to represent water. The "screen" on the bottle showing hydration stats is a gray rectangle with unreadable scribbles inside. A yellow circle in the top-right corner is meant to be a sun — the "outdoor hydration" visual cue.

It is, objectively, a very bad drawing. It is also exactly the kind of starting point that a lot of founders and product managers have in their heads: a clear concept with zero visual execution ability.

Here's what happened when we fed this drawing into Lovart as a reference image and asked it to produce professional, campaign-ready creative from it.

---

## Step 1: Reference Upload — "Here's My Idea"

[IMAGE 1 PLACEHOLDER — Persona Scenario]

We uploaded the MS Paint file into Lovart's Style Picker as a reference image. The system doesn't need a polished sketch — stick figures, rough shapes, and color blobs all communicate visual intent. The prompt:

> *"Use this rough sketch as a composition reference. The rectangle in the center is a futuristic smart water bottle. The blue line is water volume indicator. The gray square is a small LED screen. The yellow circle in the corner is sunlight. Translate this into a photorealistic product render on a clean white background. Studio lighting. Keep the composition — bottle centered, screen visible, water line visible, sunlight feel."*

Lovart processed the reference and generated a first draft. The result was not photorealistic — it was an intermediate render, somewhere between illustration and 3D mockup. The bottle had correct proportions. The LED screen was legible (showing hydration percentage). The lighting was directional, matching the "sunlight" reference from the original sketch. Progress: from MS Paint to concept render in 45 seconds.

---

## Step 2: Material Refinement — "Make It Real"

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

The concept render was compositionally correct but materially wrong. The bottle looked like matte plastic, but the product positioning required premium materials — brushed steel with silicone grip accents. The water inside looked like flat blue paint rather than a translucent liquid.

We used Touch Edit. Clicked the bottle body → *"Change material to brushed stainless steel, vertical grain. Add a matte black silicone grip band around the middle section."* Clicked the water → *"Make the water translucent with realistic refraction — visible light distortion through the liquid."* Clicked the LED screen → *"Display text: 'Hydration: 78%' in a clean digital typeface with a soft blue glow."*

Thirty seconds per edit. After three Touch Edit operations (roughly 90 seconds), the bottle looked like a product that could appear in a DTC brand's hero image. The steel had proper specular highlights. The water refracted light. The screen glowed.

---

## Step 3: Scene Composition — "Put It in Context"

A product on white is good for an Amazon listing. A product in context is good for social media and ads. We added scene context with a new prompt:

> *"Keep this exact product render unchanged. Place it into a scene: a morning hiking trail, soft golden light filtering through trees. The water bottle is in the foreground, resting on a smooth rock. A hiking backpack is visible out of focus in the background. The scene should feel aspirational but authentic — not a stock photo. Keep the bottle as the clear focal point. Leave the top 25% for a headline."*

Lovart composited the product render into the hiking scene without altering the bottle itself. The lighting on the bottle updated to match the scene's golden-hour direction. Shadows fell correctly on the rock surface. The LED screen remained legible, faintly glowing against the warm forest backdrop.

---

## Step 4: Brand Treatment — "Make It Ours"

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

Final pass: we added the brand identity. Using Lovart's Brand Kit, we placed the fictional brand's logo ("Hydro") in the top-left corner. Added a headline in the reserved top space: "Know Your Hydration." Added a subtle tagline below: "The smart bottle that tracks what matters."

Export. Total time from MS Paint sketch to market-ready creative: 5 minutes and 12 seconds. The before-and-after comparison is almost absurd — a childlike drawing on one side, a premium product ad on the other.

---

## What This Demonstrates

The journey from "terrible sketch" to "professional visual" is not about AI generating good things from nothing. It's about AI acting as a multi-step translation engine: sketch → concept render → material refinement → scene compositing → brand finishing. Each step is small and specific. No single step requires design expertise. The expertise is in knowing the steps and the order to apply them.

This workflow also proves something counterintuitive: a bad drawing is often a better starting point than a detailed text prompt. The drawing communicates spatial relationships — what's on the left, what's in the center, how big things are relative to each other — that would take paragraphs to describe. A stick figure and a rectangle, placed correctly, are worth 500 words of spatial description.

---

## When This Workflow Makes Sense

- You have a product concept you can picture but can't render.
- You're pitching an idea to stakeholders and need a visual that's beyond your drawing ability.
- You want to explore what a physical product could look like before hiring an industrial designer.
- You need marketing assets for a product that doesn't physically exist yet (pre-launch, crowdfunding).

---

## Image Appendix

| Image | Description | Placement |
|-------|-------------|-----------|
| ms-paint-original.png | The original MS Paint sketch — intentionally bad, 90 seconds of work | Introduction |
| step1-concept-render.jpg | First AI pass: intermediate render translating the sketch | Step 1 |
| step2-material-refinement.jpg | After Touch Edit: steel material, translucent water, glowing screen | Step 2 |
| step3-scene-composition.jpg | Final composite: bottle in hiking scene with golden light | Step 3 |
| step4-branded-final.jpg | Complete ad with logo, headline, tagline | Step 4 |
| before-after-comparison.jpg | Side-by-side: MS Paint original vs. final branded ad | Conclusion |

---

[IMAGE 4 PLACEHOLDER — Brand CTA]

## FAQ

**Does the quality of the reference sketch matter?**
No, within reason. A sketch that clearly communicates spatial relationships (what goes where) and basic proportions (how big each element is) will produce good results. A sketch that's complete visual noise with no discernible structure will confuse the model. The bar is low — stick figures and labeled rectangles work. Random scribbles don't.

**Can I use a photograph as a reference instead of a sketch?**
Yes. Upload a photo of a rough physical prototype (clay model, paper mockup, competitor's product for composition reference) and Lovart will translate it into the visual style you describe in the prompt. Photo-to-sketch-to-render is a valid pipeline when you have a physical reference but not a digital one.

**What if the AI misinterprets my sketch entirely?**
Simplify the reference. If your sketch has 12 labeled elements and the model is confused, reduce to 3–4 key elements. Focus on the essential spatial relationships — what's the focal point and where is it relative to other elements. You can add detail in the prompt text, which the model processes in parallel with the reference image.

**Is this workflow useful for digital products (apps, dashboards) or only physical products?**
Both. For digital products, sketch the UI layout — where the nav bar is, where the main content area is, where the data visualization goes. The AI will translate your wireframe into a polished UI mockup. This works for app screenshots, dashboard concepts, and landing page hero sections.

**How do I handle text elements in my sketch?**
Don't try to draw text — the AI won't read handwritten scribbles. Draw a labeled placeholder box (a rectangle with "HEADLINE" written inside) and specify the actual copy in your prompt. The AI will recognize the placeholder as a text zone and render it appropriately in the final image.

**Does this process work for complex multi-object scenes?**
Yes, but with diminishing returns as scene complexity increases. A single product with a simple background (workflow described above) is the sweet spot. A scene with 10 distinct objects at different depths requires more iterative refinement and may take 15–20 minutes instead of 5. The approach scales — it just takes more cycles.

**Can I use this for client presentations and pitch decks?**
Absolutely. This is actually one of the highest-ROI use cases. Instead of presenting a wireframe or a stick-figure sketch to a client, present the AI-assisted concept render. The jump in perceived professionalism is significant, and the client can give feedback on something that looks close to real rather than trying to imagine what your sketch is supposed to become.

---

## Internal Links

- [The Style Picker — How to Borrow Professional Aesthetics Without Knowing Design Theory](/blog/style-picker-borrow-professional-aesthetics-ai/)
- [Saving the Shoot — How We Fixed a Missing Prop in a Product Photo Without Reshooting](/blog/saving-the-shoot-fix-missing-prop-product-photo-ai/)
- [The Iteration Loop: How to Politely Argue with AI to Get Exactly What You Want](/blog/how-to-argue-with-ai-get-exactly-what-you-want/)
- [Remix Culture — Why Editable AI Assets Are the New Stock Photography](/blog/remix-culture-editable-ai-assets-new-stock-photography/)

---

*Chris Noland is a product designer who spent five years in hardware startups, where the gap between a founder's vision (a napkin sketch) and investor-ready visuals (a 3D render costing $2,000) was a constant source of friction. He has been experimenting with AI-assisted concept visualization since 2024 and has helped three pre-launch hardware companies produce funding-round materials using Lovart's reference-image workflow. The MS Paint smart water bottle in this case study is his creation — drawn with a trackpad during a flight delay.*

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
The persona from the case study in their real work environment — authentic, candid moment showing the transformation described in Untitled — natural light, documentary photography style

**Image 2 — The Conceptual Diagram**:
A simple data visualization sketch showing before/after metrics mentioned in the case study — hand-drawn bar charts and arrows, clean infographic style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart interface showing a completed project similar to the case study — with visible results]

**Image 4 — Brand CTA**:
Brand visual showing the success transformation — the 'after' state described in Untitled — inspiring, cinematic, warm tones

