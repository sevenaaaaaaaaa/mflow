---
slug: 03-wiki-export-formats-guide

title: "【繁體】 Export Formats 完整 指南: Every File Format Lovart Supports and When to Use Each"
date: 2027-07-14
author: "Lovart Documentation Team"
category: "Wiki"
tags: ["export format guide", "file formats", "lovart export", "design export", "production formats"]
keywords: ["export format guide", "lovart export formats", "design file formats", "PNG vs SVG", "print export", "digital design export"]
description: "The definitive reference for Lovart's export formats. Learn which file format to use for web, print, social media, merchandise, and presentation — with technical specifications for every format."
image: "/assets/wiki/export-formats-guide-hero.jpg"
reading_time: "8 min"
word_count: 1500
language: zh-TW
---

# Export Formats Complete Guide

[IMAGE 1 PLACEHOLDER — Persona Scenario]

Choosing the wrong export format can ruin a design. A beautiful gradient exported as a GIF ends up banded. A crisp logo saved as JPEG develops compression artifacts around the edges. A print file submitted in RGB comes back with unexpected color shifts. Understanding export formats isn't glamorous — but it's the difference between designs that look professional and designs that look amateur.

This guide covers **every export format** supported by Lovart, with clear decision criteria for each use case.

---

## Export Format Decision Tree

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

Before diving into individual formats, use this quick reference:

```
Need transparency?
├── Yes → PNG or SVG (web), TIFF or EPS (print)
└── No → Continue

Is it a photograph or complex image?
├── Yes → JPEG (web/digital), TIFF (print)
└── No → Continue

Is it a logo, icon, or illustration?
├── Yes → SVG (web/digital), EPS (print)
└── No → Continue

Does it need to scale infinitely?
├── Yes → SVG (web), EPS or PDF (print)
└── No → Continue

Is it going to print?
├── Yes → TIFF, EPS, or PDF (CMYK, 300+ PPI)
└── No → JPEG, PNG, WebP, or SVG (RGB, 72-144 PPI)
```

---

## Raster Formats (Pixel-Based)

Raster formats store images as grids of pixels. They're resolution-dependent — enlarge them too much and you'll see pixelation.

### PNG (Portable Network Graphics)

**Best for:** Any web graphic requiring transparency, screenshots, UI elements, logos (when SVG isn't suitable), designs with text.

**Technical Specs:**
- **Compression:** Lossless (DEFLATE algorithm)
- **Color Depth:** 8-bit (256 colors, indexed) or 24-bit (16.7 million colors, truecolor) with 8-bit alpha channel
- **Transparency:** Full alpha channel support (variable opacity from 0-100%)
- **Animation:** APNG variant supported (animated PNG)

**When to Use PNG:**
- Social media graphics with transparency
- App screenshots and UI mockups
- Designs with text (lossless compression preserves sharp edges)
- Logos and icons for digital use when SVG is unavailable
- Email graphics (some email clients don't render SVG)

**When to Avoid PNG:**
- Large photographs (file sizes 5-10× larger than JPEG at same quality)
- Print production (not a print format — JPEG artifacts but lossless, still RGB)
- Complex gradients with many colors (24-bit PNG files become large)

**Lovart PNG Export Options:**
- **PNG-8:** 256 colors max. Smallest file size. Good for simple graphics with flat colors.
- **PNG-24:** Full color + alpha. Best quality. Default for most exports.
- **PNG-24 (Compressed):** Losslessly optimized with pngquant/zopfli. 20-40% smaller than standard PNG-24.
- **PNG @2x / @3x:** Retina-resolution variants for web development.

```bash
# Example: Export a social graphic as optimized PNG with 2x retina
Format: PNG-24 (Compressed)
Scale factors: 1x (1080x1080), 2x (2160x2160)
```

---

### JPEG (Joint Photographic Experts Group)

**Best for:** Photographs, complex images without transparency, web images where file size matters.

**Technical Specs:**
- **Compression:** Lossy (DCT-based). Quality sacrifice for file size reduction.
- **Color Depth:** 24-bit (16.7 million colors)
- **Transparency:** Not supported
- **Color Space:** RGB, CMYK (rare, not recommended)

**When to Use JPEG:**
- Photographs and photo-heavy designs
- Website hero images and blog post featured images
- Email marketing images (small file size = faster load)
- Social media posts where file size affects upload speed
- Digital ads (platforms often have file size limits)

**When to Avoid JPEG:**
- Logos or designs with text (compression artifacts create soft, muddy edges)
- Graphics with flat colors or sharp lines (blocky compression artifacts visible)
- Designs requiring transparency
- Designs that will be re-edited (each save degrades quality — generational loss)
- Print production (not a print format)

**Lovart JPEG Export Options:**
- **Quality 100 (Maximum):** Near-lossless. Large file. Use when quality is paramount.
- **Quality 85 (High, Default):** Recommended for most uses. Good balance.
- **Quality 60 (Medium):** Noticeable compression. Acceptable for thumbnails and email.
- **Quality 40 (Low):** Heavy compression artifacts. Only for placeholders or tiny thumbnails.
- **Progressive JPEG:** Loads in passes on web. Better perceived performance.

---

### WebP

**Best for:** Modern web performance. Replacing both PNG and JPEG for web delivery.

**Technical Specs:**
- **Compression:** Both lossy and lossless modes
- **Color Depth:** 24-bit with 8-bit alpha channel
- **Transparency:** Full alpha support (lossy and lossless)
- **Animation:** Supported (replacement for animated GIF)

**When to Use WebP:**
- Website images (25-35% smaller than JPEG at equivalent quality)
- Images with transparency (26% smaller than PNG on average)
- Any web-facing image where you control the tech stack

**When to Avoid WebP:**
- Email marketing (limited client support as of 2027)
- Social media uploads (platforms don't accept WebP uploads)
- Print production
- Apple ecosystem compatibility (Safari added WebP support in 2020, but older devices may not render)

**Lovart WebP Export Options:**
- **Lossy WebP (Quality 85):** Recommended for photos. ~30% smaller than JPEG at equivalent quality.
- **Lossless WebP:** For graphics requiring pixel-perfect reproduction. ~26% smaller than PNG.
- **WebP @2x:** Retina variants.

```html
<!-- Always provide fallbacks for WebP -->
<picture>
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero image">
</picture>
```

---

### TIFF (Tagged Image File Format)

**Best for:** Professional print production, archival-quality images.

**Technical Specs:**
- **Compression:** Lossless (LZW, ZIP) or uncompressed
- **Color Depth:** Up to 32-bit per channel
- **Transparency:** Alpha channel support
- **Color Space:** RGB, CMYK, LAB, Grayscale

**When to Use TIFF:**
- Print production (CMYK TIFF is the gold standard)
- Professional photography archiving
- High-quality scans
- Designs heading to offset printing or high-end digital presses

**When to Avoid TIFF:**
- Web use (files are massive — 10-100× larger than JPEG)
- Email (will bounce or be rejected by attachment limits)
- Social media
- Any digital-only use case

**Lovart TIFF Export Options:**
- **TIFF (RGB, LZW Compressed):** Smaller file for RGB workflows.
- **TIFF (CMYK, Uncompressed):** Print-ready, maximum quality, large file.
- **TIFF (CMYK, LZW Compressed):** Print-ready with manageable file size.
- **Include Layers:** Preserve layer structure for editing (increases file size significantly).

---

### GIF (Graphics Interchange Format)

**Best for:** Simple animations, reaction images, legacy compatibility.

**Technical Specs:**
- **Compression:** Lossless within 256-color limitation
- **Color Depth:** 8-bit (256 colors maximum)
- **Transparency:** 1-bit (fully transparent or fully opaque — no partial transparency)
- **Animation:** Yes (primary use case in 2027)

**When to Use GIF:**
- Short, simple animations (under 5 seconds)
- Legacy email client compatibility
- Reaction GIFs for social media

**When to Avoid GIF:**
- Photographs (256-color limit = terrible quality)
- Designs with gradients (banding artifacts)
- Any professional web use (use WebP or MP4 instead)
- Modern animated content (APNG or WebP are strictly superior)

**Lovart GIF Export Options:**
- **GIF (Dithered):** Simulates more colors through dithering patterns. Better gradients.
- **GIF (No Dither):** Flat color blocks only. Smaller file.
- **GIF (Optimized):** Removes duplicate frames, reduces palette. Smallest file.
- **Loop Count:** Infinite, once, or custom (1-999 loops).

---

## Vector Formats (Math-Based)

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

Vector formats store graphics as mathematical paths, shapes, and curves. They're resolution-independent — scale to any size without quality loss.

### SVG (Scalable Vector Graphics)

**Best for:** Logos, icons, illustrations, UI elements, data visualizations — any graphic that benefits from infinite scaling.

**Technical Specs:**
- **Format:** XML-based markup language
- **Scalability:** Infinite (resolution-independent)
- **Animation:** CSS animations and SMIL supported
- **Interactivity:** JavaScript event handling supported
- **Accessibility:** Title, desc, and ARIA attributes supported

**When to Use SVG:**
- Logos (primary export format — always)
- Icons and UI elements for web and apps
- Illustrations with flat colors and defined shapes
- Data visualizations and charts
- Responsive web design (SVG scales to any viewport)

**When to Avoid SVG:**
- Photographs (not representable as vectors)
- Complex images with gradients and textures (file size can exceed raster equivalents)
- Print production (convert to EPS or PDF instead)
- Email (limited SVG support in email clients)

**Lovart SVG Export Options:**
- **SVG (Standard):** Default export with inline styles.
- **SVG (Optimized):** Minified, stripped of editor metadata. 40-60% smaller.
- **SVG (Responsive):** No fixed width/height. Scales to container.
- **SVG (Inlined):** Ready to paste directly into HTML. No external dependencies.
- **SVG Sprite:** Multiple SVGs combined into a single file with `<symbol>` tags for icon systems.

---

### EPS (Encapsulated PostScript)

**Best for:** Legacy print workflows, professional printing, compatibility with older design software.

**Technical Specs:**
- **Format:** PostScript-based vector format
- **Scalability:** Infinite
- **Color Space:** CMYK, RGB, spot colors (Pantone)
- **Transparency:** Limited (PostScript Level 3 improved, but not full)

**When to Use EPS:**
- Logo files for print vendors (industry standard request format)
- Compatibility with older RIP (Raster Image Processor) systems
- Signage and large-format printing
- Embroidery and engraving machine file preparation

**When to Avoid EPS:**
- Web use (not a web format)
- Modern digital design workflows (PDF has largely superseded EPS)
- Designs with complex transparency (EPS transparency support is inconsistent)

**Lovart EPS Export Options:**
- **EPS (CMYK):** Print-ready. Convert text to outlines. Embed fonts.
- **EPS (RGB):** Digital-first vector with RGB color space.
- **EPS (Legacy, EPS 8.0):** Maximum compatibility with older systems.

---

### PDF (Portable Document Format)

**Best for:** Universal document sharing, print-ready files, presentations, multi-page layouts.

**Technical Specs:**
- **Format:** Page description language
- **Scalability:** Vector elements scale infinitely; raster elements are resolution-dependent
- **Color Space:** RGB, CMYK, spot colors, ICC profiles
- **Pages:** Multi-page support
- **Interactivity:** Forms, hyperlinks, bookmarks, buttons

**When to Use PDF:**
- Print-ready files (PDF/X-4 is the modern print standard)
- Client presentations and pitch decks
- Multi-page documents (brand guidelines, reports, proposals)
- Shareable design proofs and review packages
- Archival purposes (PDF/A for long-term preservation)

**When to Avoid PDF:**
- Web display (browsers can render PDF but it's a poor user experience)
- Social media (platforms don't accept PDF uploads)
- Single-image scenarios (use PNG or JPEG instead)

**Lovart PDF Export Options:**
- **PDF (Standard):** General-purpose, RGB, medium compression.
- **PDF (Print):** CMYK, 300 PPI, 3mm bleed, crop marks, PDF/X-4 compliant.
- **PDF (Press-Ready):** CMYK, 300 PPI, bleed, marks, fonts embedded, images at full resolution.
- **PDF (Web Optimized):** RGB, 150 PPI, linearized for fast web viewing.
- **PDF (Interactive):** Preserve hyperlinks, buttons, and form fields.

---

## 3D & Specialized Formats

### GLB / glTF

**Best for:** 3D product visualization for web and AR.

Lovart supports 3D export for product visualization designs. GLB (binary glTF) is the standard for web-based 3D.

**When to Use:**
- Product configurators on e-commerce sites
- AR product previews (Apple ARKit, Google ARCore)
- Interactive 3D presentations
- Social media 3D posts (supported by Facebook and compatible platforms)

**Export Options:**
- **GLB (Standard):** 512px textures, Draco mesh compression.
- **GLB (High Quality):** 2048px textures, uncompressed meshes.
- **USDZ:** Apple AR-compatible format for iOS Quick Look.

---

## Platform-Specific Export Presets

Lovart includes one-click export presets for common platforms:

### Social Media

| Platform | Format | Dimensions | Max File Size |
|----------|--------|-----------|---------------|
| Instagram Post | JPEG (Q85) | 1080x1080 | 8 MB |
| Instagram Story | JPEG (Q85) | 1080x1920 | 8 MB |
| Facebook Post | JPEG (Q85) | 1200x630 | 8 MB |
| LinkedIn Post | PNG-24 | 1200x627 | 8 MB |
| Twitter/X Post | JPEG (Q85) | 1200x675 | 5 MB |
| TikTok Video Cover | JPEG (Q85) | 1080x1920 | 8 MB |
| Pinterest Pin | JPEG (Q85) | 1000x1500 | 10 MB |
| YouTube Thumbnail | JPEG (Q90) | 1280x720 | 2 MB |

### E-commerce

| Platform | Format | Dimensions |
|----------|--------|-----------|
| Amazon Main Image | JPEG (Q100) | 2000x2000 (white bg) |
| Amazon A+ Content | PNG-24 or JPEG (Q100) | 970x600 (module varies) |
| Shopify Product | JPEG (Q85) + WebP | 2048x2048 |
| eBay Listing | JPEG (Q95) | 1600x1600 (min) |
| Etsy Listing | JPEG (Q95) | 2700x2025 (4:3) |

### Print

| Use Case | Format | Specs |
|----------|--------|-------|
| Business Card | PDF (Print) | 3.5"x2", 0.125" bleed, CMYK, 300 PPI |
| Poster (18x24") | PDF (Press-Ready) | 18"x24", 0.25" bleed, CMYK, 300 PPI |
| Billboard (48x14') | TIFF (CMYK) | 48'x14' at 30-50 PPI (viewing distance) |
| T-Shirt (DTG) | PNG-24 (RGB, Transparent) | 12"x16" at 300 PPI |
| Mug Wrap | PNG-24 (RGB) | Template-dependent, check vendor specs |

---

## Batch Export: Multi-Format Output

Lovart's batch export lets you generate multiple formats from a single design in one operation. This is available on Professional plans and above.

```json
{
  "design_id": "design_xyz123",
  "exports": [
    {"format": "png", "scale": 1, "profile": "social_instagram_post"},
    {"format": "png", "scale": 2, "profile": "social_instagram_post"},
    {"format": "webp", "quality": 85, "scale": 1},
    {"format": "jpg", "quality": 85, "scale": 1},
    {"format": "pdf", "profile": "print"},
    {"format": "svg", "profile": "optimized"}
  ]
}
```

## Export Quality Comparison Table

| Format | Best Use | Transparency | Lossless? | Scalable? | Print-Ready? |
|--------|----------|-------------|-----------|-----------|-------------|
| PNG-24 | Web graphics, UI | Full alpha | Yes | No | No |
| JPEG | Photos, web images | No | No | No | No |
| WebP | Modern web | Full alpha | Optional | No | No |
| GIF | Simple animations | Binary | Within 256 colors | No | No |

[IMAGE 4 PLACEHOLDER — Brand CTA]

| TIFF | Print, archival | Full alpha | Optional | No | Yes (CMYK) |
| SVG | Logos, icons, vectors | Full alpha (CSS) | N/A (vector) | Infinite | No |
| EPS | Print vectors, legacy | Limited | N/A (vector) | Infinite | Yes (CMYK) |
| PDF | Documents, print-ready | Optional | Mixed | Mixed | Yes |
| GLB | 3D visualization | N/A | N/A | Yes (3D) | No |

---

*Export format support and specifications are accurate as of Lovart v4.2 (July 2027). Platform file size and dimension requirements are updated quarterly to reflect changes in platform specifications. Always verify export requirements with your printer or platform before final production.*

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create a design — warm natural lighting, candid documentary style

**Image 2 — The Conceptual Diagram**:
A hand-drawn sketch diagram showing the step-by-step workflow for creating designs with AI — clean line art on grid paper, arrows connecting each step, minimalist style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]

**Image 4 — Brand CTA**:
Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in Export Formats Complete Guide — modern, aspirational, cinematic lighting

