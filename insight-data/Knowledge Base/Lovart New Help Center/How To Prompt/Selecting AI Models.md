---
type: kb-doc
version: 1.0
schema_version: 1.0
kb_slug: kb-selecting-ai-models
origin: official-hand-curated-doc
authority: 5
fetched_at: 2026-07-05
source_quality: hand-curated-official
crawl_status: hand-placed
audited: False
path: insight-data/Knowledge Base/Lovart New Help Center/How To Prompt/Selecting AI Models.md
topics:
  - agent
  - tools
  - image
  - video
  - pricing
  - knowledge
capabilities:
  - Frame
  - Image Generator
  - Video Generator
  - Knowledge Base
source_urls:
  - https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models
  - https://cdn.sanity.io/images/o11tm2qe/production/831a2192ac4eb19dacf6f6a50017b6c8fb60e05b-2160x1350.jpg?w=800&q=75&auto=format
  - https://www.lovart.ai/docs/how-to-prompt/chat-tools#386e71e4d01e
  - https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#8e6f4472cf04
  - https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#bc4f64975112
  - https://cdn.sanity.io/images/o11tm2qe/production/648105fa40f8fce24cfb9bf73449cab23a1f04c5-2160x1350.png?w=800&q=75&auto=format
  - https://www.lovart.ai/docs/reference/models-and-pricing
  - https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#bc4f64975112
  - https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#d3a9af644108
  - https://www.lovart.ai/docs/how-to-prompt/chat-tools#386e71e4d01e
related_docs:
claims:
---

https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models
### Select AI Models

> Set your AI model preferences for specific design tasks.

![](https://cdn.sanity.io/images/o11tm2qe/production/831a2192ac4eb19dacf6f6a50017b6c8fb60e05b-2160x1350.jpg?w=800&q=75&auto=format)

**What It Does**

Open the Models panel to set model preferences for the current task. Turn Auto On to let the Agent choose the most suitable model automatically. Turn Auto Off to manually select the image, video, or 3D models you want to prioritize. The Agent may still route between similar models to balance quality, speed, and stability.

**How to Use**

1. **Open the Models panel.**
    - Click the Models icon on the bottom-right corner of the input box.
2. **Configure Auto Mode.**
    - **Auto On:** The Agent automatically chooses suitable models based on your task.
    - **Auto Off:** Select your preferred and prioritized models.
3. **Set model preferences.**
    - **Image:** Select one or more image models to indicate which ones you prefer for generating visuals.
    - **Video:** Select one or more video models to indicate which ones you prefer for generating videos.
    - **3D:** Select Tripo as your preferred model.

**Quick Tips**

- Select AI Models sets a preference, not a strict lock. To lock a specific model, use @ Mention instead.

**Related Features**

- [Mention](https://www.lovart.ai/docs/how-to-prompt/chat-tools#386e71e4d01e): Strictly lock a specific model for a generation request by using `@` (this will override Select Model).
- [Image Generator](https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#8e6f4472cf04): Generate images with a specific model, bypassing the Agent.
- [Video Generator](https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#bc4f64975112): Generate videos with a specific model, bypassing the Agent.

### Image Generator

**Shortcut:** `A`

> Generate images directly with a chosen model, bypassing the Agent.

![](https://cdn.sanity.io/images/o11tm2qe/production/648105fa40f8fce24cfb9bf73449cab23a1f04c5-2160x1350.png?w=800&q=75&auto=format)

**What It Does**

Image Generator runs your prompt with an image model directly. Use it when you already know the model, resolution, and aspect ratio you want and don't want the Agent to pick for you.

**How to Use**

1. **Open Image Generator.**
    - Click the Image Generator icon in the Canvas toolbar or in the input box. Press `A` as a shortcut.
2. **Write your prompt.**
    - Describe the image in the input box.
3. **Configure settings.**
    - **Model:** Pick from the available image models. See [Models & Pricing](https://www.lovart.ai/docs/reference/models-and-pricing) for the current list.
    - **Set parameters:** Set the resolution, aspect ratio, and any other options the model accepts.
    - **Upload references (optional):** Upload a file or pick an image from the Canvas.
4. **Generate.**
    - Click Generate. The image lands on the Canvas, ready to edit.

**Quick Tips**

- Available parameters change with the model, so the panel will show only the controls the selected model supports.

**Related Features**

- [Video Generator](https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#bc4f64975112): Generate video directly with a chosen model.
- [Select AI Models](https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#d3a9af644108): Set a default model preference for the Agent instead of bypassing it.
- [Mention](https://www.lovart.ai/docs/how-to-prompt/chat-tools#386e71e4d01e): Lock a specific model in an Agent prompt with `@`.

### Video Generator

**Shortcut:** `S`

> Generate videos directly with a chosen model, bypassing the Agent.

![](https://cdn.sanity.io/images/o11tm2qe/production/61a8924a970025c550ef000b658c02b433e540b7-2160x1350.png?w=800&q=75&auto=format)

**What It Does**

Video Generator runs your prompt and input media through a video model directly to create engaging videos. Use it when you want fast, direct control over the model and settings.

**How to Use**

1. **Open Video Generator.**
    - Click the Video Generator icon in the Canvas toolbar or in the input box. Press `S` as a shortcut.
2. **Write your prompt.**
    - Describe the video in the input box.
3. **Configure settings.**
    - **Model:** Pick from the available video models. See [Models & Pricing](https://www.lovart.ai/docs/reference/models-and-pricing) for the current list.
    - **Set parameters:** Set the resolution, aspect ratio, length, and any other options the model accepts.
    - **Upload references (optional):** Upload reference images, videos, audio, or start and end frames, and any other modes of reference the model accepts.
4. **Generate.**
    - Click Generate. The video lands on the Canvas.

**Quick Tips**

- Available parameters change with the model, so the panel will show only the controls the selected model supports.

**Related Features**

- [Image Generator](https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#8e6f4472cf04): Generate stills directly with a chosen model, or as keyframes for video.
- [Select AI Models](https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#d3a9af644108): Set a default video model for the Agent.
- [Mention](https://www.lovart.ai/docs/how-to-prompt/chat-tools#386e71e4d01e): Lock a specific video model in an Agent prompt with `@`.