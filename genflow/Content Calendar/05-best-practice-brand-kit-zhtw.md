---
slug: 05-best-practice-brand-kit

title: "【繁體】 最佳 Practice: Set Up Your 品牌 Kit in 5 Minutes"
page_type: "Guide / Best Practice"
category: "Product Tutorial"
target_keywords:
  - "brand kit setup"
  - "ai brand kit"
  - "lovart brand kit"
  - "brand consistency ai"
  - "setup brand kit"
status: "Published"
date: "2026-05-W4"
author: "Lovart Content Team"
estimated_read: "6 min"
language: zh-TW
---

# Best Practice: Set Up Your Brand Kit in 5 Minutes

[IMAGE 1 PLACEHOLDER — Persona Scenario]

## The Feature That Pays for Itself Every Time You Generate

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

Here's a claim that sounds like marketing fluff but is actually true: once you set up your Brand Kit in Lovart, you never have to think about brand consistency again. No more copy-pasting hex codes into prompts. No more "did I use the right blue on that last batch?" anxiety. No more exporting a design and realising — too late — that the logo is slightly cut off.

Lovart's Brand Kit automates brand enforcement at the generation level. The MCoT (Mind Chain of Thought) engine considers your brand parameters *during* the design reasoning phase, which means every image, carousel, ad, and presentation that comes out of Lovart is on-brand by default — not because you manually chased consistency, but because the system never had the option to be off-brand.

Five minutes. That's all the setup takes. Let's walk through it.

---

## Step 1: Upload Your Logo (SVG Is Best)

**What you need:** Your logo file. Ideally SVG — vector format preserves crisp rendering at any size. PNG works too if you don't have SVG; just make sure it's high resolution (at least 1000px on the longest edge).

**How to do it:**

1. Open Lovart and navigate to **Settings → Brand Kit**.
2. Click **Upload Logo** and select your file.
3. Lovart automatically detects the logo's transparent areas and preserves them.
4. (Optional) Upload a **dark-mode variant** of your logo if you have one — white or light-coloured version for dark backgrounds.

**One thing to check:** After upload, generate a test image with a dark background and one with a light background. Make sure your logo is visible on both. If you have both light and dark variants uploaded, Lovart will automatically select the appropriate one based on the generated design's background.

**Pro tip:** If your logo includes a tagline or subtitle, upload a version without it as well. You may want the simplified version for small placements (social media profile pictures, favicons) and the full version for hero images and presentations.

---

## Step 2: Set Your Brand Colour Palette (3-5 Colours)

**What you need:** Your brand's hex colour codes. If you don't have these, grab them from your website, your logo, or your existing marketing materials — any colour picker tool will give you the hex values.

**How to do it:**

1. In the Brand Kit panel, go to **Colours**.
2. Click **Add Colour** and enter a hex code (e.g., `#1A1A2E`).
3. Label each colour by its role — Primary, Secondary, Accent, Background, Text.
4. Repeat for 3-5 colours total. More than 5 tends to dilute the brand recognition.

**A solid default palette structure:**

- **Primary (1):** Your main brand colour — the one people associate with your company. Used for headlines, CTAs, key visual elements.
- **Secondary (1):** A complementary colour for supporting elements — subheadings, icons, secondary buttons.
- **Accent (1):** A contrasting colour for emphasis — sale badges, highlights, notification dots.
- **Background (1):** Usually white or near-white (`#FFFFFF` or `#F8F9FA`).
- **Text (1):** Usually dark grey or black (`#1A1A2E` or `#333333`).

Lovart applies these intelligently — it understands colour roles, not just "these five colours exist." The Primary colour shows up on CTAs and headlines. The Background colour governs the overall canvas. The Text colour controls body copy. You don't need to specify roles; Lovart's MCoT engine figures it out based on standard design conventions.

---

## Step 3: Choose Your Brand Fonts

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

**What you need:** Your brand's primary typeface names. If you use Google Fonts or Adobe Fonts, Lovart has access to the full library. If you use a custom licensed font, you may need to upload it (check your Lovart plan for custom font support).

**How to do it:**

1. In the Brand Kit panel, go to **Typography**.
2. Set your **Heading Font** — this is what headlines, titles, and large display text will use.
3. Set your **Body Font** — this is what paragraphs, descriptions, and small text will use.
4. (Optional) Set a **Display Font** if your brand uses a third typeface for special occasions (hero text, quotes, numbers in infographics).

**If you're not sure what to pick:**
- Heading: Something with character — Inter, Montserrat, Playfair Display.
- Body: Something readable — Inter (yes, works for both), Source Sans Pro, Lora.
- Keep the pairing simple. One sans-serif for headings and one serif for body is a classic combination; two sans-serifs with different weights also works well.

Lovart automatically applies appropriate font sizes, weights, and line heights based on the element type. You don't need to specify "36pt bold for H1" — the system handles typographic hierarchy.

---

## Step 4: Save and Apply

**How to do it:**

1. Hit **Save** in the Brand Kit panel. (Yes, it's that simple.)
2. Go back to the main canvas and generate something — anything — with a prompt that doesn't mention your brand at all. "Social media post for a product launch" works fine.
3. Notice that the output uses your colours, your fonts, and your logo placement — automatically.

**What's happening under the hood:** Lovart's MCoT engine now has your Brand Kit parameters as part of its reasoning context. Every time you generate, the system thinks through your business context *and* your visual identity simultaneously. The brand guidelines aren't a filter applied after generation — they're part of the creative direction from the start.

---

## Verification: Check Your Brand Kit Is Working

Before you trust the system with a hundred assets, do a quick sanity check:

1. **Generate 5 different types of designs** — a social media post, an ad banner, a presentation slide, a LinkedIn carousel, and an infographic.
2. **Check colour consistency** — are your primary and secondary colours showing up across all assets? They should feel like they came from the same brand, even if the designs are completely different.
3. **Check logo placement** — is your logo present in appropriate positions? (Usually bottom-right on social graphics, top-left on presentations.)
4. **Check typography** — are headlines using your heading font and body text using your body font?

If something's off, go back to the Brand Kit settings and adjust. It's easier to catch a colour misalignment on a test batch of 5 than on a production batch of 50.

---

## Advanced: Multi-Brand Management (Team Plan and Above)

If you're an agency, a freelancer with multiple clients, or a company with sub-brands, Lovart's Team Plan supports multiple Brand Kits in a single workspace.

**How to set it up:**

1. Go to **Settings → Brand Kits** and click **Add Brand Kit**.
2. Repeat Steps 1-3 for your second brand.
3. When generating, select which Brand Kit to apply from a dropdown — or set a default for each project folder.

**Use case:** Monday morning you're designing for Client A (healthcare SaaS, blue palette, clean sans-serif fonts). Tuesday afternoon you switch to Client B (DTC skincare, warm earth tones, elegant serif type). One click switches the entire brand context. No reconfiguration. No colour mix-ups.

---

## Why This Matters More Than You Think

Brand inconsistency is expensive in ways that don't show up on a balance sheet. When a potential customer sees your Instagram post in one style, clicks through to your website (different style), then gets your email newsletter (third style), their brain registers the inconsistency — even if they can't articulate it. The result is lower trust, weaker recall, and a brand that feels amateurish even if the individual assets are well-designed.

[IMAGE 4 PLACEHOLDER — Brand CTA]

Lovart's Brand Kit eliminates the human error from brand enforcement. Not by giving you checklists and guidelines to follow (those exist already, and you still forget), but by making on-brand output the only kind of output the system can produce.

Five minutes of setup. Brand consistency forever. That's a trade worth making.

---

**[Set Up Your Brand Kit in Lovart — Free →]**

Five minutes. Upload your logo, pick your colours, choose your fonts. That's it. Everything you generate from now on will be on-brand by default.

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create a design — warm natural lighting, candid documentary style

**Image 2 — The Conceptual Diagram**:
A hand-drawn sketch diagram showing the step-by-step workflow for creating designs with AI — clean line art on grid paper, arrows connecting each step, minimalist style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]

**Image 4 — Brand CTA**:
Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in Best Practice: Set Up Your Brand Kit in 5 Minutes — modern, aspirational, cinematic lighting

