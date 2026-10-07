---
title: "【繁體】 Prompting for Repairs — What Words Actually Work When Asking AI to Fix a Mistake"
date: 2026-05-10
category: "Best Practice"
keywords: ["ai fix prompt", "correct ai design mistakes", "ai repair words"]
slug: "prompting-for-repairs-words-to-fix-ai-mistakes"
author: "Lovart Content Team"
description: "A field-tested vocabulary of repair prompts — the exact words and phrases that reliably get AI design tools to fix specific mistakes instead of introducing new ones."
image: "/images/blog/prompting-for-repairs-hero.jpg"
reading_time: "9 min"
language: zh-TW
---

You see the problem. The product is floating a few pixels above the surface. The text is slightly garbled — one letter is morphing into the next. The shadow is casting in the wrong direction. The lighting on the character's face doesn't match the scene.

You know what's wrong. But when you type "fix the lighting," the model changes the lighting — and also the background, the character's posture, and the color of the CTA button. The repair created three new problems. You wanted a patch; you got a renovation.

This is the repair vocabulary problem. Certain words and phrases are interpreted by AI models in ways that produce targeted fixes. Other words — common, natural-sounding words — produce cascade changes. Here's the vocabulary that works, organised by problem type.

---

## The Repair Vocabulary, by Problem Type

[IMAGE 1 PLACEHOLDER — Persona Scenario]

### Lighting Fixes

| Problem | Wrong Prompt | Right Prompt | Why It Works |
|---------|-------------|-------------|--------------|
| Scene too dark | "Make it brighter" | "Increase exposure by 1 stop. Keep color temperature and contrast unchanged." | "Brighter" is ambiguous — it could mean exposure, saturation, or adding light sources. "Exposure" is precise. |
| Harsh shadows | "Soften the shadows" | "Reduce shadow opacity by 50%. Maintain shadow position and direction. Do not alter lighting on the main subject." | "Soften" can mean blur, reduce opacity, or change light source size. Quantitative direction ("by 50%") removes ambiguity. |
| Wrong light direction | "Fix the lighting" | "The light source should come from the upper right, not the left. Adjust all shadows and highlights to match a single light source at 2 o'clock position. Keep scene composition and subject unchanged." | "Fix the lighting" is a rewrite invitation. Specifying direction, position, and what to preserve produces a targeted adjustment. |
| Color cast on subject | "Make the skin tone natural" | "Remove the blue color cast on the subject's face. Restore natural warm skin tones while keeping the cool-toned background intact. Only adjust the subject's skin — do not alter the scene lighting." | "Natural" is subjective. Describing the cast color (blue) and specifying what should and shouldn't change produces a surgical edit. |

The pattern: quantify when possible ("by 50%," "1 stop," "2 o'clock position"), and always include what should remain unchanged ("keep scene composition," "do not alter the background").

---

### Object and Subject Fixes

| Problem | Wrong Prompt | Right Prompt | Why It Works |
|---------|-------------|-------------|--------------|
| Floating product | "Make the product sit on the table" | "Lower the product by approximately 2% of the frame height so it rests naturally on the table surface. Add a subtle contact shadow where the product meets the table. Keep product angle, lighting, and reflections unchanged." | "Sit on the table" doesn't specify the fix mechanism. The model might scale the product, move the table, or zoom the scene. Incremental positioning ("2% of frame height") + contact shadow instruction produces the right result. |
| Extra fingers | "Remove the extra finger" | "The right hand shows 6 fingers. Reduce to 5 fingers with natural proportions. Preserve hand position and gesture. Keep the rest of the character unchanged." | AI models sometimes generate extra digits. The specific number (6 → 5) gives the model a measurable target. "Preserve hand position" prevents the model from replacing the entire hand with a new one. |
| Distorted face | "Fix the face" | "The left eye is asymmetrical — lower than the right by a noticeable margin. Align the left eye to match the right eye's horizontal axis. Keep the expression, skin texture, and rest of the face unchanged." | "Fix the face" triggers a full facial regeneration that loses the specific expression and character. Naming the specific asymmetry and defining the target alignment preserves what's working. |
| Object blending into background | "Make the object stand out" | "Increase contrast between the product and the background by 15%. Add a subtle rim light to the product's top edge to separate it from the background. Keep product color and texture identical. Only adjust contrast and edge lighting." | "Stand out" is vague — the model might change the product color, blur the background, or resize the product. Specifying the separation mechanism (contrast + rim light) and the exact adjustment amount gives the model a recipe, not a vibe. |

---

### Color Fixes

| Problem | Wrong Prompt | Right Prompt | Why It Works |
|---------|-------------|-------------|--------------|
| Brand color is wrong | "Make the blue match the brand" | "Change the blue in the CTA button from #3B82F6 to #1E40AF. Recolor only the button element — do not affect any other blue elements in the design." | Hex codes are unambiguous. "Match the brand" requires the model to infer what your brand is, which it can't do unless you've configured Brand Kit. Even then, a hex code is more reliable than a brand name. |
| Background color clashing | "Change the background to something nicer" | "Replace the background color. Current: bright orange (#F97316). Target: warm cream (#F5F0E8). Keep the product lighting and shadows unchanged. Only the solid background color should change." | "Nicer" is subjective. Current color → target color with hex codes removes interpretation. The preservation clause ("keep product lighting unchanged") prevents the model from "fixing" the lighting to match the new background, which would create a cascade edit. |
| Color balance off | "Make the colors pop" | "Increase saturation globally by 10%. Then increase vibrance (selective saturation of muted colors) by an additional 5%. Do not clip highlights or crush shadows. Preserve the overall color temperature." | "Pop" is a vibe, not an instruction. Quantifying the saturation adjustment and separating saturation from vibrance (which are different operations) gives the model a recipe it can follow precisely. |

---

### Typography and Layout Fixes

| Problem | Wrong Prompt | Right Prompt | Why It Works |
|---------|-------------|-------------|--------------|
| Headline too small | "Make the headline bigger" | "Increase the headline font size by 12pt. Adjust the text zone boundaries to accommodate the larger text while maintaining the 40px margin from the edge of the canvas. Do not resize any other text elements." | "Bigger" could mean font size, bold weight, letter-spacing, or zone expansion. Specifying the unit (pt) and the spatial constraint (maintain margin) produces the intended change. |
| Text illegible over image | "Make the text readable" | "Add a semi-transparent dark overlay (black at 40% opacity) behind the entire text zone. Keep the overlay contained to the text area only — do not extend into the image. Text color remains white." | "Readable" is a symptom description, not a solution. The overlay bar is the specific fix mechanism. The containment instruction ("text area only") prevents the overlay from darkening the whole image. |
| Elements misaligned | "Align everything" | "The headline, subhead, and CTA button should share the same left alignment line. Adjust the subhead to align left with the headline. Keep all other positioning, sizing, and spacing unchanged." | "Align everything" might produce center-alignment when you wanted left. Naming the alignment shared-line (left alignment) and the specific element to adjust (subhead) prevents the model from adjusting elements that were already aligned. |

---

## The Meta-Pattern: The Four-Part Repair Prompt Structure

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

Every effective repair prompt follows the same four-part structure. You don't need to memorise every specific phrase above — you need to understand this structure:

1. **Identify:** Name the specific element that's wrong and what's wrong with it. Not "the image" — "the shadow under the product bottle." Not "looks weird" — "is casting in the opposite direction from the scene's light source."

2. **Prescribe:** Name the specific fix. Not "make it better" — "reverse the shadow direction to match the light source at 10 o'clock." Quantify when possible.

3. **Preserve:** List everything that should stay the same. Not "don't change anything else" — "keep product position, lighting intensity, color palette, and background unchanged." Be explicit about what matters.

4. **Constrain:** Add spatial or technical boundaries. Not "just fix that one thing" — "only the shadow element should change; do not regenerate the product, background, or text." The word "only" is the most powerful constraint word in repair prompts.

**Example — full four-part prompt:**

> *"[Identify] The drop shadow beneath the product is sharp and dark, inconsistent with the soft ambient lighting in the scene. [Prescribe] Reduce the shadow opacity by 60% and increase the shadow blur radius by 30px to match the ambient light softness. [Preserve] Keep the product, the surface it sits on, the scene lighting, and all other elements unchanged. [Constrain] Only the product's drop shadow should be modified — no other element in the image."*

---

## Words to Avoid in Repair Prompts

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

Some common words produce cascading changes because they're interpreted as holistic aesthetic instructions rather than surgical corrections:

- **"Better"** — the model interprets this as "regenerate with higher aesthetic quality score," which can change anything.
- **"Nicer"** — same problem; subjective aesthetic instruction triggers full regeneration.
- **"Fix"** — ambiguous. Fix what? The model guesses.
- **"Professional"** — triggers a different aesthetic mode entirely, potentially redesigning the composition.
- **"More modern"** — triggers a style shift, not a targeted adjustment.

Replace these with specific instructions. Not "make it better" — "increase contrast by 10% and sharpen the product focus." Not "make it more professional" — "add 20px of padding on all sides and increase the headline font size by 4pt."

---

## Image Appendix

| Image | Description | Placement |
|-------|-------------|-----------|
| repair-before-after-lighting.jpg | Lighting fix: before (wrong direction) and after (corrected with specific prompt) | Lighting Fixes |
| repair-before-after-floating.jpg | Floating product fix: before and after with contact shadow added | Object Fixes |
| repair-before-after-color.jpg | Brand color fix: hex code correction example | Color Fixes |
| repair-before-after-typo.jpg | Typography fix: overlay bar for text legibility | Typography Fixes |
| four-part-structure-diagram.jpg | Visual diagram of the Identify-Prescribe-Preserve-Constrain structure | Meta-Pattern |
| wrong-words-cheatsheet.jpg | "Don't say this / Say this instead" quick reference card | Words to Avoid |

---

[IMAGE 4 PLACEHOLDER — Brand CTA]

## FAQ

**How do I know if a repair prompt will cause cascade changes or stay targeted?**
Test your prompt against the four-part structure. If your prompt includes the preserve and constrain sections explicitly, cascade risk is low. If your prompt is only the identify and prescribe sections ("fix the lighting"), cascade risk is high. The preserve section is the most commonly omitted and the most important for targeted repairs.

**What if I don't know the technical term for what's wrong?**
Describe the symptom in plain language, then add "keep everything else identical." For example: "The bottle looks like it's hovering above the surface instead of resting on it. Lower the bottle until it touches the surface. Keep everything else identical." You don't need to know "contact shadow" — you need to describe the visible problem. The model will infer the technical fix.

**Can I use the same repair vocabulary across different AI design tools?**
The vocabulary patterns described here are tested on Lovart's ChatCanvas and Touch Edit. Other AI design tools may interpret prompts differently — especially those with different model architectures. The four-part structure (Identify-Prescribe-Preserve-Constrain) is universally applicable. The specific phrase effectiveness varies by platform.

**Why does the model sometimes ignore the "keep everything else identical" instruction?**
Two reasons: (1) the primary instruction ("fix the lighting") is more ambiguous than the constraint is specific, so the model weights the ambiguous instruction over the specific one. Solution: make the repair instruction as specific as the constraint. (2) Some repairs inherently require cascade changes — fixing a shadow direction when the lighting source has been regenerated affects other shadows in the scene whether you want it to or not. Accept minor collateral changes for physically interdependent elements.

**How many repair attempts should I make before restarting from scratch?**
Follow the 3-strike rule: three attempted repairs. If the fix doesn't work after three targeted attempts, the underlying generation has issues that repair prompts can't address. Restart with a stronger initial prompt incorporating what you learned. See the over-editing guide for a fuller discussion of when to stop and restart.

**Can I save effective repair prompts as templates for future use?**
Yes. Lovart supports saving prompts. Create a personal library of repair prompts organised by problem type — lighting, color, typography, layout, objects. When you encounter a familiar problem, pull the relevant prompt template and adjust the specifics. Over time, your repair library makes you faster because you stop inventing repair language from scratch each time.

**Are repair prompts different for photorealistic vs. illustrated images?**
The vocabulary is the same, but the sensitivity to specific instructions differs. Photorealistic images are more sensitive to lighting and shadow precision because the audience's visual expectations are higher. Illustrated images are more tolerant of approximate fixes because the style itself communicates that the image is constructed rather than captured. In practice: be more precise with photorealistic repair prompts; illustrated images accept a wider margin of error.

---

## Internal Links

- [The Iteration Loop: How to Politely Argue with AI to Get Exactly What You Want](/blog/how-to-argue-with-ai-get-exactly-what-you-want/)
- [Over-Editing — How to Know When to Stop Tweaking and Export](/blog/over-editing-when-to-stop-tweaking-design/)
- [Eye Contact — How to Use Touch Edit to Make a Character Look at the Camera](/blog/eye-contact-touch-edit-character-look-at-camera/)
- [Creating Negative Space — How to Tell AI to Leave Room for Your Text](/blog/creating-negative-space-ai-leave-room-for-text/)

---

*Alex Novak is a prompt engineer and interaction designer who has been studying human-AI communication patterns since 2023. He has catalogued over 2,000 repair prompt attempts across multiple AI platforms, analysing which language patterns produce targeted corrections and which produce cascade changes. The four-part repair prompt structure and the avoided-word vocabulary in this article are based on his systematic testing — conducted originally for his own use and refined through collaboration with the Lovart team during their beta period.*

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A curated flat-lay photography scene showing design tools and outputs mentioned in Untitled — organized chaos, editorial product photography style

**Image 2 — The Conceptual Diagram**:
A hand-drawn ranking or scoring matrix showing the criteria used to evaluate options in Untitled — colorful markers, creative layout

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart template gallery or design showcase showing multiple completed designs]

**Image 4 — Brand CTA**:
Brand visual showing 'Best of' collection — multiple beautiful design outputs arranged in a grid, modern gallery aesthetic

