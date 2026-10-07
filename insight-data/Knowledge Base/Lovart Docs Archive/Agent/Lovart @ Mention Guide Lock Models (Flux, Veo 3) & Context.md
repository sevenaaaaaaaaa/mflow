---
type: kb-doc
version: 1.0
schema_version: 1.0
kb_slug: kb-lovart-mention-guide-lock-models-flux-veo-3-context
origin: official-hand-curated-legacy
authority: 2
fetched_at: 2026-07-05
source_quality: legacy-archive
crawl_status: hand-placed
audited: False
path: insight-data/Knowledge Base/Lovart Docs Archive/Agent/Lovart @ Mention Guide Lock Models (Flux, Veo 3) & Context.md
topics:
  - agent
  - tools
  - image
  - video
  - pricing
  - knowledge
capabilities:
  - Nano Banana Pro
  - Flux 2
  - Veo 3
  - Knowledge Base
source_urls:
  - https://www.lovart.ai/docs/agent/mention
  - https://cdn.sanity.io/images/o11tm2qe/production/691afd9bac814306db12eb29f238199adc18afcd-2160x1350.png
  - https://cdn.sanity.io/images/o11tm2qe/production/691afd9bac814306db12eb29f238199adc18afcd-2160x1350.png
  - https://cdn.sanity.io/images/o11tm2qe/production/691afd9bac814306db12eb29f238199adc18afcd-2160x1350.png
related_docs:
claims:
---

ℹ️ Please login

Agent

## Mention

Master the @ Mention panel in Lovart AI. Learn to strictly lock models like Nano Banana or Veo 3 and attach specific project resources. Understand the priority logic vs. Model Select.

![Lovart @ Mention Guide: Lock Models (Flux, Veo 3) & Context](https://cdn.sanity.io/images/o11tm2qe/production/691afd9bac814306db12eb29f238199adc18afcd-2160x1350.png)

Lovart @ Mention Guide: Lock Models (Flux, Veo 3) & Context

  
The **@ Mention** panel is used to **explicitly select** resources in the current conversation, so the agent strictly uses them as context when generating content.

### Core usage

- Type **@** in the input box to open a searchable list.
- Choose an **image, model, or project** from the list, and it will be attached to the current generation request.

### Selection logic

- When you **@ mention a model**, this is a **selection logic**: the system will execute with the exact model you call, not just treat it as a soft preference.
- Key difference: the Model Select panel defines **preferences**, while @-mentioning a model is a strong, high-priority instruction that overrides preferences.

\*Each conversation input can include a maximum of 10 elements combined (files, images, mentions, etc.).

### @ Mention Use Cases

**1. Locking Specific Models for Consistent Output**
When you need guaranteed model selection:
- "@ Flux 2 Pro" ensures this model is used regardless of auto-selection
- Perfect for projects requiring specific model characteristics (photorealism, artistic style, etc.)
- Useful when comparing results across specific models

**2. Attaching Project Resources**
Reference complete project assets:
- @ Project: Brand Assets → Uses entire brand guidelines as context
- @ Project: Campaign Materials → Applies campaign visual standards
- Ensures consistency across all generated content

**3. Image Reference Attachment**
Attach specific images for style/composition:
- @ Uploaded Image → AI analyzes this image for style matching
- Great for maintaining visual consistency with existing assets
- Enables "match this style" workflows

**4. Context Preservation**
Keep conversation context focused:
- Use @ to explicitly specify which resources matter for current request
- Reduces ambiguity when working with multiple assets
- Helps AI understand precise requirements

### Advanced @ Mention Patterns

**Combining Multiple Mentions:**
You can mention multiple resources in one prompt:
- "@ Veo 3 @ Brand Colors @ Product Photos" - Generates video using all three as strict context
- Useful for complex projects requiring multiple reference points

**Overriding Previous Selections:**
When your initial model choice isn't working:
- New @ mention automatically overrides previous selections
- Can specify new model mid-conversation without changing preferences
- Great for A/B testing and rapid iteration

**Priority Hierarchy:**
1. **@ Mention** (highest priority - explicit selection)
2. **Model Select panel** (medium priority - preferences)
3. **Auto selection** (lowest priority - system optimization)

### Practical Workflows

**Consistent Brand Video Production:**
1. "@ Veo 3" → Lock video model
2. "@ Brand Assets Project" → Apply brand guidelines
3. "Create promotional video for new product" → Generate with all context

**Style-Matched Character Design:**
1. "@ Flux 2 Max" → Use photorealistic model
2. "@ Reference Character Image" → Match style
3. "Design variations of this character in different poses" → Generate

**Campaign Asset Generation:**
1. "@ Nano Banana Pro" → Select image model
2. "@ Previous Campaign Assets" → Match visual style
3. "Create social media posts following this direction" → Consistent results

### FAQ

**Q: What's the difference between @ mention and Model Select?**
A: @ mention is a hard override - the AI MUST use that model. Model Select is a preference - the system may choose alternatives if better suited.

**Q: Can I @ mention files I've uploaded?**
A: Yes, uploaded files appear in the @ mention list. Attach them to give the AI explicit reference context.

**Q: What if I @ mention a model but it can't handle my request?**
A: The system will attempt to use the model but may suggest alternatives if technical constraints exist.

**Q: How many @ mentions can I use at once?**
A: Up to 10 elements total per message, including @ mentions, files, and images combined.