---
type: kb-doc
version: 1.0
schema_version: 1.0
kb_slug: kb-ai-transformation
origin: official-hand-curated-doc
authority: 5
fetched_at: 2026-07-05
source_quality: hand-curated-official
crawl_status: hand-placed
audited: False
path: insight-data/Knowledge Base/Lovart New Help Center/Edit Your Design/AI Transformation.md
topics:
  - agent
  - canvas
  - tools
  - image
  - video
  - brand
  - pricing
  - knowledge
capabilities:
  - Shape
  - Frame
  - Image Generator
  - Brand Kit
  - Knowledge Base
source_urls:
  - https://www.lovart.ai/docs/edit-your-design/ai-transformation
  - https://www.lovart.ai/docs/edit-your-design/ai-transformation#63cf102480ef
  - https://www.lovart.ai/docs/edit-your-design/advanced-ai-editing#6ae82b6e027d
  - https://www.lovart.ai/docs/edit-your-design/advanced-ai-editing#a325d3865db9
  - https://www.lovart.ai/docs/how-to-prompt/adding-references#828020ecba5b
  - https://www.lovart.ai/docs/edit-your-design/basic-ai-editing#31d1b4d59068
  - https://www.lovart.ai/docs/how-to-prompt/adding-references#828020ecba5b
  - https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#8e6f4472cf04
  - https://www.lovart.ai/docs/edit-your-design/basic-ai-editing#5939657f2e1f
  - https://www.lovart.ai/docs/how-to-prompt/agent-skills#aa9126e0113d
related_docs:
claims:
---

https://www.lovart.ai/docs/edit-your-design/ai-transformation
### Multi-Angles

> Generate images of the same subject from new angles.

**What It Does**

Multi-Angles takes one image and produces variants of the same subject from different viewpoints. Instead of prompting, you drag or adjust parameters in a panel. Use it for product listings, character sheets, video storyboards, and any image set that needs to show a subject from multiple angles.

Multi-Angles has two modes:

- **Subject Mode:** Rotate, tilt, or scale the subject within the frame.
- **Camera Mode:** Rotate, tilt, or scale the virtual camera around the subject.

**How to Use**

1. **Open Multi-Angles.**
    - Select an image on the Canvas, then click Multi-Angles in the top bar to open the control panel.
2. **Pick a mode.**
    - Choose Subject Mode for direct subject control or Camera Mode for virtual-camera control.
3. **Set the angle.**
    - **Drag:** Drag the subject (Subject Mode) or the camera (Camera Mode) until the preview matches the angle you want.
    - **Or use parameters:** Set Rotate, Tilt, and Scale parameters numerically.
4. **Generate.**
    - Click Run. The new angle lands on the Canvas as a fresh image alongside the original.

**Quick Tips**

- Combining Rotate, Tilt, and Scale gives you 8 × 4 × 3 = 96 possible angles. Change one parameter at a time to see the effect, then combine.

**Related Features**

- [Move Object](https://www.lovart.ai/docs/edit-your-design/ai-transformation#63cf102480ef): Move an object to a new position inside an image.

### Move Object

> Move an object to a new position within an image, with optional prompt edits.

**What It Does**

Move Object moves one object in an image to a new position while preserving the original background. Select the object with the Rectangle or Lasso tool, then drag it to the desired location. Lovart generates a coherent new image with the original location filled in.

**How to Use**

1. **Open Move Object.**
    - Select an image on the Canvas, then click Move Object from the top bar.
2. **Select the target.**
    - Drag a rectangle or lasso around the object you want to move.
3. **Drag to a new position.**
    - Move the object to its new location in the frame.
4. **Generate.**
    - Lovart produces a new image with the object in its new spot and the original location filled in to match the surrounding scene.

**Quick Tips**

- Tighten your selection box around the target. A loose box can confuse object detection in busy scenes.

**Related Features**

- [Mark / Touch Edit](https://www.lovart.ai/docs/edit-your-design/advanced-ai-editing#6ae82b6e027d): Describe a change in natural language instead of dragging.
- [Edit Elements](https://www.lovart.ai/docs/edit-your-design/advanced-ai-editing#a325d3865db9): Separate an image into layers for multi-object rearrangement instead of moving one object at a time.

### Vectorize

> Convert a raster image (PNG, JPG) into a scalable SVG in one click.

**What It Does**

Vectorize turns a raster image into an SVG by tracing its contours and shapes as multi-path vector geometry. Use it when you need a logo, icon, or illustration that stays crisp at any size and exports cleanly to design or print tools.

**How to Use**

1. **Run Vectorize.**
    - Select an image on the Canvas, then click Vectorize from the top bar.
    - Lovart analyzes the image and generates an SVG.
2. **Export SVG.**
    - The SVG lands on the Canvas as a new asset. Download and import it into Illustrator, Figma, or another design tool to edit.

**Quick Tips**

- Remove the background first for a cleaner trace, especially for logo work.
- For brand assets, vectorize once and save the SVG to your [Brand Kit](https://www.lovart.ai/docs/how-to-prompt/adding-references#828020ecba5b) so you can drop the same crisp logo into any future project.

**Limitations**

- Lovart does not yet support previewing or editing vectors directly on the Canvas. To edit paths, download the SVG and open it in a vector editor like Illustrator or Figma.

**Related Features**

- [Remove Background](https://www.lovart.ai/docs/edit-your-design/basic-ai-editing#31d1b4d59068): Clean the subject before vectorizing for sharper traces.
- [Brand Kit](https://www.lovart.ai/docs/how-to-prompt/adding-references#828020ecba5b): Store the resulting SVG as a reusable brand asset.

### Mockup

> Place your design onto real-world objects like printed materials, packaging, or apparel.

**What It Does**

Mockup shows a flat design on a real-world object. Start from a photo of the object you want to mock — a poster, box, T-shirt — then place and position your design on it. Use it to present logos, labels, posters, or UI screens in context.

**How to Use**

1. **Select the image.**
    - Click the image on the Canvas that contains the real-world object you want your design to appear on.
2. **Open Mockup.**
    - Click Mockup in the top bar. Lovart detects the object surface that should receive the design.
3. **Add your design.**
    - Upload the design you want to apply.
    - Drag it around on the detected surface to place it.
4. **Lock and export.**
    - When the placement looks right, click Rasterize to bake the design onto the object.
    - Download as PNG or JPEG.

**Quick Tips**

- Don't have a scene yet? Generate one with [Image Generator](https://www.lovart.ai/docs/how-to-prompt/selecting-ai-models#8e6f4472cf04) and use it as the Mockup base.
- [Upscale](https://www.lovart.ai/docs/edit-your-design/basic-ai-editing#5939657f2e1f) the rasterized result before export.
- You can also bring a design and ask the Agent for any custom mockup scene ("place this logo on a coffee cup in a café setting"). The Agent generates the scene and applies the mockup in one pass.
- Try [Lovart Skills](https://www.lovart.ai/docs/how-to-prompt/agent-skills#aa9126e0113d) for mockup presets, especially under E-Commerce and Branding.

**Related Features**

- [Remove Background](https://www.lovart.ai/docs/edit-your-design/basic-ai-editing#31d1b4d59068): Isolate objects and designs.
- [Lovart Skills](https://www.lovart.ai/docs/how-to-prompt/agent-skills#aa9126e0113d): Use mockup-focused Skills for common e-commerce and brand presentation presets.