---
type: kb-doc
version: 1.0
schema_version: 1.0
kb_slug: kb-lovart-model-select-guide-preferences-for-flux-veo-3-tripo
origin: official-hand-curated-legacy
authority: 2
fetched_at: 2026-07-05
source_quality: legacy-archive
crawl_status: hand-placed
audited: False
path: insight-data/Knowledge Base/Lovart Docs Archive/Agent/Lovart Model Select Guide Preferences for Flux, Veo 3 & Tripo.md
topics:
  - agent
  - image
  - video
  - pricing
  - knowledge
capabilities:
  - Nano Banana Pro
  - Flux 2
  - Sora 2
  - Veo 3
  - Kling
  - Knowledge Base
source_urls:
  - https://www.lovart.ai/docs/agent/model-select
  - https://cdn.sanity.io/images/o11tm2qe/production/831a2192ac4eb19dacf6f6a50017b6c8fb60e05b-2160x1350.jpg
  - https://cdn.sanity.io/images/o11tm2qe/production/831a2192ac4eb19dacf6f6a50017b6c8fb60e05b-2160x1350.jpg
  - https://cdn.sanity.io/images/o11tm2qe/production/831a2192ac4eb19dacf6f6a50017b6c8fb60e05b-2160x1350.jpg
related_docs:
claims:
---

ℹ️ Please login

Agent

## Model Select

Master Lovart's Model Select panel. Learn how Auto On/Off logic works and how to set preferences for top models like Flux Context, Gemini Veo 3, and Tripo.

![Lovart Model Select Guide: Preferences for Flux, Veo 3 & Tripo](https://cdn.sanity.io/images/o11tm2qe/production/831a2192ac4eb19dacf6f6a50017b6c8fb60e05b-2160x1350.jpg)

Lovart Model Select Guide: Preferences for Flux, Veo 3 & Tripo

  
The **Model Select** panel on the right sets your **model preferences** for this task, rather than hard-locking specific models.

### How it works

- With **Auto** on, the system chooses suitable models based on your task, using your selections as **priority candidates**, not exclusive choices.
- With **Auto** off, the models you tick are **preferred and prioritized**, but the system may still smartly route within similar models to balance quality, speed, and stability.

### Image / Video / 3D

- **Image**: Select one or more image models to indicate which ones you prefer to generate the current visuals.
- **Video**: Pick preferred video models (for example, models with audio) for this script or storyboard.
- **3D**: Select Tripo when you prefer to generate 3D assets from text or reference images.

### Note on preference logic

- Model Select is **preference-based**, not a strict “only use this model” switch.
### Understanding Auto Mode

**Auto Mode ON:**
- System intelligently selects models based on task requirements
- Your selected models serve as priority candidates
- Best for: Unknown requirements, experimental work, general tasks

**Auto Mode OFF:**
- System respects your selections more strictly
- Still allows smart routing within model families
- Best for: Specific requirements, comparison testing, workflow optimization

### Model Categories Explained

**Image Models:**
| Model | Best For | Characteristics |
|-------|----------|-----------------|
| Nano Banana Pro | General purpose, brand visuals | Balanced quality and speed |
| Flux 2 Pro | Photorealistic outputs | High detail, professional quality |
| Flux 2 Max | Complex compositions | Maximum detail, premium results |
| GPT Image | Creative, artistic styles | Unique artistic interpretations |

**Video Models:**
| Model | Best For | Characteristics |
|-------|----------|-----------------|
| Sora 2 | Cinematic quality | Premium, professional productions |
| Veo 3 | Fast turnaround | Quality with speed balance |
| Kling 2.6 | Versatile content | Wide range of styles |
| Hailuo | Motion variety | Dynamic movement options |

**3D Models:**
| Model | Best For | Characteristics |
|-------|----------|-----------------|
| Tripo | Product visualization | Realistic 3D renders |
| Tripo Text-to-3D | Concept exploration | Quick 3D from descriptions |

### Practical Model Selection Strategies

**Strategy 1: Speed-First Approach**
- Select multiple fast models (Veo 3 Fast, Kling Turbo)
- Enable Auto mode
- Good for: Iterations, drafts, social media content

**Strategy 2: Quality-First Approach**
- Select premium models (Sora 2 Pro, Flux 2 Max)
- Disable Auto mode
- Good for: Final deliverables, client presentations

**Strategy 3: Balanced Approach**
- Select 2-3 models from different tiers
- Enable Auto mode
- Good for: General workflows, unknown requirements

### FAQ

**Q: Should I select multiple models or just one?**
A: Selecting multiple gives the system flexibility. Single selection is more consistent but less adaptive.

**Q: Does Auto mode ever use models I haven't selected?**
A: In Auto ON mode, unselected models may be used if selected models aren't optimal for the task.

**Q: What's the difference between Model Select and @ mention?**
A: Model Select is a preference (soft). @ mention is a hard override that guarantees specific model usage.

**Q: Can I save model preferences for different project types?**
A: Update preferences as needed based on project requirements. Preferences are session-based.
