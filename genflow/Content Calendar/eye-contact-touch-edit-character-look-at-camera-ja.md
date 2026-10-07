---
title: "【日本語】 Eye Contact — 方法 Use Touch Edit to Make a Character Look at the Camera"
date: 2026-05-10
category: "Best Practice"
keywords: ["ai eye contact fix", "touch edit eyes", "character looking at camera ai"]
slug: "eye-contact-touch-edit-character-look-at-camera"
author: "Lovart Content Team"
description: "AI-generated characters often look slightly away from the camera. Learn the Touch Edit technique that redirects gaze direction — fixing one of the most common AI portrait flaws in seconds."
image: "/images/blog/eye-contact-hero.jpg"
reading_time: "7 min"
language: ja
---

You generate a portrait for your campaign. The lighting is perfect. The composition is balanced. The expression is warm and approachable. But something is slightly wrong, and you can't immediately name it. Then you realize: the character isn't looking at you. Their gaze is directed somewhere just above and to the left of the lens. It's the difference between a portrait that connects and a portrait that observes — and your audience will feel it even if they can't articulate it.

Eye contact — or the lack of it — is one of the most common flaws in AI-generated portraits. It's also one of the easiest to fix, once you know the technique.

---

## Why AI Characters Avoid Eye Contact

[IMAGE 1 PLACEHOLDER — Persona Scenario]

AI image models are trained on millions of photographs, and in those photographs, people rarely look directly at the camera. Candid shots, editorial photography, street photography — the subjects are looking at something else. The model learns that "person looking slightly away" is the statistical norm, and it reproduces that norm unless you explicitly override it.

Even when you prompt for eye contact — "a person looking directly at the camera" — the model sometimes approximates rather than achieves it. The eyes are directed at the viewer, but the angle is 5-10 degrees off. To the subconscious, this reads as avoidance. The character isn't connecting; they're looking past you.

---

## The Touch Edit Eye Fix

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

Lovart's Touch Edit lets you correct gaze direction without regenerating the entire image. Here's the technique:

**Step 1: Identify the deviation.**

Look at the character's eyes. Where are they looking? At the lens? Slightly above? To the left? To the right? The fix direction is the opposite of the deviation. If they're looking slightly up and left, you need to redirect the gaze down and right — toward the camera position.

**Step 2: Select the eyes.**

Click on the character's eyes using Touch Edit. The selection doesn't need to be pixel-perfect — a general selection around the eye area is sufficient. The system isolates the eyes, brow area, and immediate surrounding facial structure.

**Step 3: Issue the correction prompt.**

This is the specific language that works:

> *"Redirect the gaze directly at the camera — direct eye contact with the viewer. Pupils centered in the eyes, looking straight ahead. Adjust the iris position, pupil position, and eyelid angle to achieve a natural, engaged direct gaze. Keep everything else about the face identical — expression, lighting, skin tone, facial structure. Only the gaze direction changes."*

The key phrases are "pupils centered," "direct eye contact," and "keep everything else identical." The model understands these as precise gaze instructions, not general artistic direction.

**Step 4: Review and refine.**

After the edit, look at the result. Is the gaze now direct? Sometimes one eye corrects perfectly and the other drifts slightly. If that happens, Touch Edit the individual eye that's off — don't re-edit both. The specificity of one-eye correction prevents the model from changing things you already fixed.

Refinement prompt for one-eye correction:

> *"The right eye (camera-left) has perfect direct gaze. Only adjust the left eye (camera-right) to match — same pupil position, same engagement level, same catchlight. Bring the left iris to center, matching the right eye's gaze direction exactly."*

---

## The Catchlight Bonus

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

Eye contact alone isn't enough for a compelling portrait. The eyes need a catchlight — a small reflection of the light source visible in the iris. Catchlights make eyes look alive. Without them, even perfectly directed eyes look flat and doll-like.

If your generated portrait lacks catchlights, add them with Touch Edit:

> *"Add a subtle catchlight in both eyes — a small soft white reflection in the upper portion of each iris, consistent with the light source direction in the scene. The catchlight should be natural and realistic, not a bright studio flash. Match the size and placement to the ambient lighting."*

A portrait with direct eye contact AND catchlights has the visual psychology of a professional headshot. The viewer's brain registers the connection and the aliveness simultaneously.

---

## When to Avoid Direct Eye Contact

Direct eye contact is not always the right choice. In some design contexts, an averted gaze is more powerful:

- **Aspirational imagery:** A person looking upward and slightly away signals hope, ambition, future-focus. Direct eye contact keeps the viewer in the present.
- **Lifestyle photography:** A person engaged in an activity (cooking, reading, running) should look at what they're doing, not at the camera. Direct eye contact in an action scene breaks the illusion of candid reality.
- **Editorial and fashion:** Averted gaze is a convention of fashion photography that signals the subject is an object of aesthetic contemplation, not a person inviting interaction.
- **Mystery and intrigue:** A subject looking at something outside the frame creates narrative tension — what are they looking at? Direct eye contact resolves the tension.

Use the gaze direction that serves the emotional purpose of the image. If the purpose is connection, engagement, and trust — direct eye contact. If the purpose is aspiration, candid reality, or aesthetic contemplation — let the gaze drift.

---

## Image Appendix

| Image | Description | Placement |
|-------|-------------|-----------|
| gaze-comparison.jpg | Side-by-side: portrait with averted gaze vs. same portrait with corrected direct gaze | Introduction |
| touch-edit-eyes-selection.jpg | Screenshot showing the eye area selected in Touch Edit | Step 2 |
| before-after-gaze-correction.jpg | Before (looking up-left) and after (direct eye contact) | Step 3–4 |
| catchlight-comparison.jpg | Eyes without catchlights vs. with catchlights — the "alive" difference | Catchlight |
| appropriate-averted-gaze.jpg | Three examples where averted gaze is the correct creative choice | When to Avoid |

---

[IMAGE 4 PLACEHOLDER — Brand CTA]

## FAQ

**Can I use this technique for animals or non-human characters?**
Yes. The gaze direction logic applies to any subject with eyes — animals, illustrated characters, mascots. The prompt language adjusts accordingly: "cat looking directly at camera," "illustrated character making eye contact with viewer." The Touch Edit selection works on any eye-like feature in the image.

**What if the character is in profile or three-quarter view?**
If the face is in profile, you can't create direct eye contact without rotating the head, which is a much larger edit. Touch Edit can adjust gaze direction within the existing head angle — a three-quarter view can be redirected from "looking past the camera" to "looking at the camera at a slight angle." Full profile to full frontal is a head rotation, not a gaze edit, and requires regenerating the entire portrait with a new prompt.

**Does Touch Edit affect the rest of the face when modifying eyes?**
In isolated form, no — the edit is localised to the selected area. However, the surrounding brow and upper cheek may shift slightly to accommodate the new gaze angle (the muscles around the eyes move when gaze direction changes). This subtle adjustment is usually appropriate and natural — real eye movement affects the whole eye region.

**How many attempts does it typically take to fix eye contact?**
One to two Touch Edit passes for most portraits. If the initial gaze deviation is severe (looking 30+ degrees off-camera), two passes may be needed: first to bring the gaze into the general camera direction, second to fine-tune to direct eye contact. If it takes more than three passes, the original head angle may not support direct gaze — consider regenerating with a stronger initial eye-contact prompt.

**Can I specify where the character is looking instead of just "at the camera"?**
Yes. Touch Edit supports directional gaze prompts: "looking at the product in their hand," "looking at another person off-frame to the right," "looking down at a phone screen." The gaze redirection technique works for any target direction, not just the camera lens. Describe what the character should be looking at, and the system adjusts pupil and iris position accordingly.

**Why does AI struggle with eye contact more than other facial features?**
Eye contact is a highly precise spatial relationship — both eyes must converge on the same point in 3D space, which is computationally complex. Slight asymmetries that are imperceptible in other facial features become very noticeable in gaze because humans are extraordinarily sensitive to eye direction. It's one of our most evolved social perception systems. The AI's approximation isn't worse than other features — we're just better at detecting its errors.

---

## Internal Links

- [The Iteration Loop: How to Politely Argue with AI to Get Exactly What You Want](/blog/how-to-argue-with-ai-get-exactly-what-you-want/)
- [Prompting for Repairs — What Words Actually Work When Asking AI to Fix a Mistake](/blog/prompting-for-repairs-words-to-fix-ai-mistakes/)
- [Saving the Shoot — How We Fixed a Missing Prop in a Product Photo Without Reshooting](/blog/saving-the-shoot-fix-missing-prop-product-photo-ai/)
- [Lovart Touch Edit: Select, Modify, Perfect — Element by Element](/features/touch-edit)

---

*Katherine Webb is a portrait photographer who spent ten years shooting editorial and commercial portraiture. She has photographed over 2,000 subjects and considers eye contact the single most important variable in portrait effectiveness. She began experimenting with AI-generated portraiture in 2025 and contributed the gaze-correction technique in this article, adapting her photographic understanding of eye direction to AI-native editing workflows.*

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create a design — warm natural lighting, candid documentary style

**Image 2 — The Conceptual Diagram**:
A hand-drawn sketch diagram showing the step-by-step workflow for creating designs with AI — clean line art on grid paper, arrows connecting each step, minimalist style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]

**Image 4 — Brand CTA**:
Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in Untitled — modern, aspirational, cinematic lighting

