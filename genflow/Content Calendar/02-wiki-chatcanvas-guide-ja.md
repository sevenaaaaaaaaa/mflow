---
slug: 02-wiki-chatcanvas-guide

title: "【日本語】 ChatCanvas 完全 Operation ガイド: Master Conversational AI デザイン"
page_type: Wiki / Documentation
category: Product Guide
keywords: chatcanvas guide, how to use chatcanvas, lovart chatcanvas tutorial, conversational design ai, ai design chat interface
date: 2027-02-24
status: Draft
language: ja
---

# ChatCanvas Complete Operation Guide: Master Conversational AI Design

[IMAGE 1 PLACEHOLDER — Persona Scenario]

ChatCanvas is Lovart's conversational design interface — the place where natural language meets visual creation. Instead of clicking through toolbars, dragging elements, and manually adjusting properties, you describe what you want in plain English (or any of our supported languages), and the AI generates, iterates, and refines your design through ongoing conversation.

This guide covers everything from basic operation to advanced techniques that most users never discover. Whether you are on day one or month twelve, there is something here for you.

---

## The Core Concept: Conversation as Interface

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

Traditional design tools are imperative — you tell the computer what to do step by step. "Create a rectangle. Make it red. Add text. Center it." ChatCanvas is declarative — you describe the outcome you want, and the AI figures out the steps.

This shift from imperative to declarative interaction is the single most important concept to internalize. When you open ChatCanvas, do not think about what tools to use. Think about what you want to see on the canvas. Then describe it.

**Instead of:** "Insert a text box, type 'Summer Sale', make it 48pt, change the font to Montserrat Bold, make it red, center it horizontally."

**Say:** "Add a bold headline that says 'Summer Sale' in red, centered at the top."

The AI handles the implementation details. Your job is creative direction.

## Basic Operations

### Starting a New Design

There are three ways to begin:

1. **Describe from scratch:** "Create a square Instagram post for a summer sale at a boutique clothing store. It is 50% off everything. The brand is feminine and modern."

2. **Start from a template:** Browse the template library, select one that is close to what you need, and open it in ChatCanvas. Then modify it conversationally: "Change this to promote a winter sale instead."

3. **Upload an image for modification:** Upload a photo, screenshot, or existing design and describe what you want to change: "Remove the background from this product photo and place it on a clean white background with subtle shadow."

### Iterating Through Conversation

After the AI generates an initial design, you refine it through natural conversation. This is where ChatCanvas is fundamentally different from other AI design tools. You do not start over when the first result is not perfect — you talk through the improvements.

**Effective iteration patterns:**

- **Specific, directional feedback:** "Make the headline 20% larger and change the color to navy blue."
- **Comparative feedback:** "I like the second version better — can you take that one and add a border around the image?"
- **Mood-based feedback:** "This feels too corporate. Can you make it more playful and friendly?"
- **Structural feedback:** "The layout is good but I want the image on the left and the text on the right instead."

**Ineffective iteration patterns:**

- **Vague feedback:** "Make it better." (The AI cannot read your mind — be specific about what "better" means.)
- **Contradictory feedback:** Saying "make it bolder" and then "make it more subtle" in successive messages without clarifying the conflict.
- **Starting over unnecessarily:** If 80% of the design is working, iterate on the 20% that is not. Do not scrap everything and demand a fresh start unless the fundamental direction is wrong.

### Using References

ChatCanvas can reference external design inspiration. There are three ways to provide references:

1. **Upload reference images:** "Here is a design I like. Create something with a similar feel but for my brand."

2. **Describe a known reference:** "Make it look like an Apple product page — clean, lots of white space, one hero product image, minimal text."

3. **Reference a previous ChatCanvas design:** "Use the same layout as the 'Spring Collection' post we made last week, but update the colors and text for our Summer Collection."

The AI will capture the essence of the reference — layout structure, color treatment, typographic style — without copying it directly.

## Advanced Techniques

### Multi-Step Design Reasoning

ChatCanvas uses MCoT (Multi-modal Chain of Thought) to think through complex design requests. You can leverage this explicitly by chunking your request into logical phases:

**Phase 1: Strategy**
"First, help me think about the strategy. I need a landing page hero for a meditation app targeting stressed professionals. What visual direction would be most effective?"

The AI will reason through audience, emotional goals, competitive landscape, and design psychology before suggesting a direction. You discuss, agree on the approach, and then move to execution.

**Phase 2: Layout**
"Okay, I like the calm-but-modern direction. Now suggest a layout. I want it to communicate peace without looking boring."

**Phase 3: Detail Refinement**
"Great layout. Now let us refine — I want the headline typography to feel more editorial, the background color slightly warmer, and the CTA button to have more visual weight."

This phased approach produces better results than dumping all requirements in a single message because the AI can focus its reasoning on one problem at a time.

### Design System Commands

ChatCanvas understands design system concepts. You can use these directly:

- **"Establish a grid"** — The AI creates and maintains an underlying grid structure for alignment
- **"Apply visual hierarchy"** — The AI explicitly prioritizes elements by importance
- **"Use brand spacing"** — The AI references your Brand Kit's spacing tokens
- **"Maintain typographic scale"** — The AI ensures all text sizes follow a consistent proportional system
- **"Check accessibility"** — The AI reviews contrast ratios, text sizes, and touch targets

### Batch and Variant Generation

For high-volume needs, ChatCanvas supports batch operations:

**Variant generation:** "Generate 5 variations of this design — try different color schemes, photo placements, and typography treatments. I want to A/B test."

**Batch templating:** "I have 15 products. Take this template and create a version for each product. Here are the product names and images." (You can upload a CSV or paste a list.)

**Multi-format export:** "Export this design in all standard formats — Instagram square, Instagram Story, Facebook post, LinkedIn post, and email header. Adjust the layout as needed for each format."

### Touch Edit Integration

ChatCanvas integrates with Touch Edit for pixel-level refinements. When you need to modify a specific element within a generated design:

"Open this in Touch Edit. I want to remove the potted plant from the corner of this room photo." (Uses inpainting)

"Extend the background of this image by 200 pixels on the right side." (Uses outpainting)

"Change the color of the sofa in this image from beige to navy blue." (Uses selective color modification)

Touch Edit handles the image manipulation; ChatCanvas handles the overall design direction. Moving between them is seamless — your design state is preserved.

## Common Workflows

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

### Social Media Post Creation

**Typical session:**
1. "Create an Instagram post announcing our new product launch. The product is a sustainable water bottle. Our brand is eco-friendly and modern."
2. Review the generated post.
3. "I like the direction but the product photo needs to be larger — it should be the hero element."
4. "Add our logo in the top right corner at a subtle size."
5. "The background should be more natural — maybe a subtle leaf pattern or nature-inspired gradient."
6. "Perfect. Export as Instagram square and Story format."

**Time: 2-5 minutes.** (Traditional design: 30-60 minutes.)

### Marketing Campaign Suite

**Typical session:**
1. "I need a complete campaign suite for a Black Friday sale at our electronics store. I need: email header, Instagram post, Facebook ad, website hero banner, and a print flyer."
2. The AI generates the full suite with consistent visual language.
3. "The Facebook ad needs to be more conversion-focused — make the discount percentage the biggest element. The email header can be more brand-focused. Everything else looks great."
4. "Add our 'Free Shipping' badge to all versions."
5. "Export everything in correct platform dimensions."

**Time: 10-15 minutes.** (Traditional design: 4-8 hours across multiple tools.)

### Brand Identity Development

**Typical session:**
1. "I am starting a new brand called 'Morning Ritual' — a premium coffee subscription service. Target audience: design-conscious professionals who care about coffee quality. Brand personality: refined, warm, and slightly obsessive about craft. Help me develop the visual identity."
2. The AI proposes a complete brand direction — logo concepts, color palette, typography, and visual style.
3. Iterate: "The logo is close but feels too rustic — I want something more contemporary." "The color palette is beautiful but I want the accent color to be more distinctive."
4. "Now generate the full brand package — business card, packaging label concept, Instagram template set, and website hero."

**Time: 30-60 minutes for full brand development.** (Traditional design: 2-4 weeks with an agency.)

## Keyboard Shortcuts and Power Features

ChatCanvas supports keyboard shortcuts for power users:

- **⌘ + Enter:** Send message / generate
- **⌘ + Z:** Undo last generation (reverts to previous design state)
- **⌘ + Shift + Z:** Redo
- **⌘ + E:** Export current design
- **⌘ + S:** Save to project
- **⌘ + B:** Toggle Brand Kit overlay (shows brand colors, fonts, and rules for reference)
- **⌘ + /:** Show command palette
- **Tab:** Autocomplete common design commands
- **↑ (in chat input):** Cycle through previous messages

**Power features:**

- **"/@brand"** — Explicitly invoke Brand Kit for the current message
- **"#template-name"** — Reference a saved template by name
- **Right-click any element** — Opens a contextual menu with element-specific actions (adjust, replace, remove, duplicate)
- **Drag and drop images** directly onto the canvas to add them to the current design
- **"Remember:"** prefix — Adds a persistent instruction that applies to all subsequent messages in this session (e.g., "Remember: always use our brand green for CTAs")

## Troubleshooting Common Issues

**"The AI is not understanding what I want."**
- Be more specific. Instead of "make it modern," try "use a minimal sans-serif font, lots of white space, and a limited color palette."
- Provide a reference image.
- Try the phased approach: strategy first, then layout, then details.

**"The design looks generic."**
- Provide more brand-specific detail. Generic prompts produce generic results.
- Use your Brand Kit if you have not already.
- Reference specific design styles or inspirations you admire.

**"The AI keeps making the same mistake."**
- Use "Remember:" to set a persistent instruction.
- Try rephrasing the feedback differently — sometimes a different description of the same issue produces better results.
- If it is a specific element that keeps being problematic, try: "Lock everything except [element] and only change that."

**"The text in my design has typos or weird formatting."**
- Explicitly spell out any text you want included: "The headline should read exactly: 'Summer Sale — 50% Off Everything'"
- Check text carefully. While AI text rendering has improved dramatically, it is not perfect. Always proofread.
- For critical text, consider adding it as a separate text layer after generation.

**"My design looks different when exported."**
- ChatCanvas previews are RGB. Print exports need CMYK conversion — always check the print preview before exporting for print.
- Screen brightness and calibration affect how colors appear. Trust the hex codes, not just your eyes.
- Export at the intended size and resolution for the target medium.

## Tips from Power Users

- **Start every session with context.** "I am designing for [brand name], a [industry] company. Our brand colors are [colors]. The audience is [audience]. The goal of this design is [goal]." The more context you give upfront, the better the first result.

[IMAGE 4 PLACEHOLDER — Brand CTA]

- **Build a ChatCanvas vocabulary.** Pay attention to which phrasings produce good results and which do not. Over time, you will develop an intuitive sense of how to describe design direction effectively.

- **Use the history panel.** Every ChatCanvas session preserves your full history. You can scroll back to any previous design state and branch from there. This is invaluable for exploring multiple directions without losing work.

- **Save successful designs as templates.** If you create a social media post that works well, save it. Next time, start from that template rather than from scratch.

- **Combine ChatCanvas with manual tools.** ChatCanvas is great for the 80% — structure, layout, color, and typography. For pixel-perfect final adjustments, export and fine-tune in your preferred design tool. The AI gets you to the finish line; the final sprint is yours.

ChatCanvas represents a fundamentally new way to create visual content. It rewards clear communication, creative direction, and iterative refinement. The more you use it, the more intuitive the conversation becomes — and the faster you will move from idea to finished design.

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create a design — warm natural lighting, candid documentary style

**Image 2 — The Conceptual Diagram**:
A hand-drawn sketch diagram showing the step-by-step workflow for creating designs with AI — clean line art on grid paper, arrows connecting each step, minimalist style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]

**Image 4 — Brand CTA**:
Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in ChatCanvas Complete Operation Guide: Master Conver — modern, aspirational, cinematic lighting

