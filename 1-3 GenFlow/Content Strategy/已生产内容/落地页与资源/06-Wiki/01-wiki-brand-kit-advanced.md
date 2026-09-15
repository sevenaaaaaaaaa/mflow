---
title: "Brand Kit Advanced Settings Guide: Mastering Lovart's Brand Management System"
date: 2027-07-14
author: "Lovart Documentation Team"
category: "Wiki"
tags: ["brand kit advanced", "brand kit settings", "lovart brand kit", "brand management", "advanced configuration"]
keywords: ["brand kit advanced", "brand kit tutorial", "lovart brand settings", "advanced brand configuration", "brand kit guide"]
description: "Unlock the full power of Lovart's Brand Kit with this advanced settings guide. Learn about variant management, conditional brand rules, AI brand memory, color accessibility profiles, and multi-brand workspace configuration."
image: "/assets/wiki/brand-kit-advanced-hero.jpg"
reading_time: "8 min"
word_count: 1500
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Brand Kit Advanced Settings Guide",
  "description": "--- title: "Brand Kit Advanced Settings Guide: Mastering Lovart's Brand Management System" date: 2027-07-14 author: "Lovart Documentation Team" category: "",
  "url": "https://www.lovart.ai/01-wiki-brand-kit-advanced",
  "datePublished": "2026-05-12",
  "publisher": {
    "@type": "Organization",
    "name": "Lovart",
    "url": "https://www.lovart.ai"
  }
}
</script>

# Brand Kit Advanced Settings Guide

The standard Brand Kit setup — upload a logo, pick some colors, choose fonts — gives you about 40% of what the system can do. This guide covers the advanced configuration layer that transforms Lovart's Brand Kit from a basic asset library into a **programmatic brand management engine**. If you manage multiple brands, serve clients, or need strict brand governance, these settings are essential.

---

## 1. Brand Variant Management

Most brands don't have one identity — they have core brand + several contextual variants. Lovart's Brand Variant system lets you define these as inheritable configurations.

### Creating Brand Variants

Navigate to **Brand Kit > [Your Brand] > Settings > Variants**. You can create:

- **Seasonal Variants** — Holiday color overrides, festive typography, seasonal logo lockups. Example: Your core brand with a winter holiday palette that automatically activates Nov 15 – Jan 5.
- **Campaign Variants** — Product launch-specific branding. Example: A limited-edition color palette and alternate logo mark for a summer collection launch.
- **Sub-Brand Variants** — Child brands that inherit 70% of the parent brand but differ in colors, logo mark, or tone. Example: "Acme Pro" (enterprise product line) vs. "Acme" (core brand).
- **Co-Branding Variants** — Partner brand integrations where both brands' identities must coexist. Example: A co-branded event with shared color space allocation rules.

### Inheritance Rules

Variants use a parent-child inheritance model:

```
Core Brand (100% rules)
├── Holiday Variant (overrides: colors, seasonal logo)
│   └── Inherits: fonts, spacing, tone, imagery style
├── Campaign Variant (overrides: colors, accent logo mark)
│   └── Inherits: fonts, primary logo, tone
└── Sub-Brand Variant (overrides: colors, fonts, logo)
    └── Inherits: spacing, imagery style, tone
```

Set which properties each variant inherits vs. overrides in the **Inheritance Map** panel.

**Pro Tip:** Create a "Safe Fallback" variant with no overrides. Use this as the base for testing — if a variant misbehaves, Lovart falls back to Safe Fallback rather than defaulting to system defaults.

---

## 2. Conditional Brand Rules

Conditional rules are the most powerful — and most underused — feature in the Brand Kit. They tell Lovart's AI to apply different brand behaviors based on context.

### Rule Types

**Content-Type Rules:**
Define how the brand behaves on different content formats.

```
IF content_type = "social_media_instagram_story"
THEN
  - Logo variant = "icon_mark_only"
  - Color dominance = "brand_secondary" (60%), "brand_primary" (35%), accent (5%)
  - Font scale = "mobile_compact"
  - Image style = "bold_typography_overlay"
```

```
IF content_type = "presentation_slide"
THEN
  - Logo variant = "horizontal_lockup" (position: bottom-right, size: 8% width)
  - Color dominance = "white" (70%), "brand_primary" (20%), accent (10%)
  - Font scale = "presentation_large"
  - Image style = "data_visualization_supporting"
```

**Audience Rules:**
Adjust branding based on the target audience.

```
IF audience = "B2B_enterprise"
THEN
  - Tone = "professional_formal"
  - Color saturation = -15% (muted)
  - Font weights = "medium_to_bold_range"
  - Image style = "corporate_editorial"

IF audience = "DTC_consumer"
THEN
  - Tone = "friendly_casual"
  - Color saturation = +10% (vibrant)
  - Font weights = "light_to_bold_range"
  - Image style = "lifestyle_authentic"
```

**Platform Rules:**
Optimize for where the content will live.

```
IF platform = "linkedin"
THEN
  - Aspect ratio = "1.91:1" OR "1:1"
  - Logo position = "top_center"
  - Copy length = "medium_professional"
  - CTA style = "text_link_primary"

IF platform = "tiktok"
THEN
  - Aspect ratio = "9:16"
  - Logo presence = "watermark_subtle_only"
  - Copy length = "minimal_overlay"
  - CTA style = "none" (native platform CTA preferred)
```

### Rule Priority & Conflict Resolution

When multiple conditions match (e.g., content is a TikTok post targeting B2B enterprise — rare but possible), Lovart resolves conflicts using:

1. **Content-Type Rules** (highest priority)
2. **Platform Rules**
3. **Audience Rules**
4. **Global Brand Defaults** (lowest priority)

You can customize this hierarchy in **Brand Kit > Settings > Rule Priority**.

---

## 3. AI Brand Memory

Lovart's AI Brand Memory is a machine learning layer that observes your manual edits and learns your unstated preferences over time.

### How It Works

Every time you manually adjust a Lovart-generated design — changing a font weight, repositioning the logo, adjusting spacing — the system captures:

- **The original AI output** (what Lovart generated)
- **Your edit** (what you changed it to)
- **Context metadata** (content type, platform, audience, time, campaign)

After approximately **20-30 manual corrections** on a specific pattern, Brand Memory starts automatically applying your preferences to new generations.

### Managing Brand Memory

Navigate to **Brand Kit > Settings > AI Memory** to:

- **View Learned Preferences** — See exactly what patterns Lovart has identified from your editing behavior
- **Override Learned Rules** — Delete incorrect generalizations. Example: If you manually resized a logo once because of a specific image, Lovart might incorrectly learn "logos should be 12% smaller" — override this.
- **Set Learning Sensitivity** — Low (requires 50+ corrections to learn), Medium (default: 20-30), High (learns from 10-15 corrections — but may overfit)
- **Pause Learning** — Temporarily freeze Brand Memory (useful during deliberate brand experiments where you don't want accidental patterns learned)
- **Reset to Baseline** — Clear all learned preferences and return to your original Brand Kit configuration

**Warning:** AI Brand Memory is plan-dependent. Professional plans retain 30 days of learning data. Business plans retain 90 days. Enterprise plans retain unlimited history with rollback capability.

---

## 4. Color Accessibility Profiles

Beyond basic contrast checking, Lovart's advanced accessibility system manages color use across different vision contexts.

### Profile Types

**Standard sRGB Profile:**
Default color rendering. WCAG 2.1 AA and AAA contrast compliance checked automatically.

**Deuteranopia Simulation (Red-Green):**
Simulates the most common form of color blindness (affects ~6% of males). Lovart automatically suggests palette adjustments:
- Avoid red-green status indicators → use red + blue, or add icon differentiation
- Flags problem color pairs in your palette
- Generates "safe alternative" palette that maintains brand feel while being distinguishable

**Protanopia & Tritanopia Profiles:**
Additional color vision deficiency simulations. Enterprise plan includes all CVD profiles with automatic remediation suggestions.

**High Contrast Mode:**
Optimizes for users with low vision or those using OS-level high contrast settings. Generates alternative designs that use:
- Solid backgrounds (no gradients)
- Thick borders on interactive elements
- Minimum 7:1 contrast ratio for all text
- No color-only information conveyance

**Grayscale Priority:**
For print-first brands concerned about B&W reproduction. Ensures designs maintain hierarchy and legibility when printed in grayscale.

### Setting Accessibility Defaults

Set your default accessibility profile in **Brand Kit > Settings > Accessibility**:

- **Check Mode:** Warn (flag issues but allow publication) vs. Block (prevent export until issues resolved)
- **Auto-Fix:** Lovart automatically corrects fixable accessibility issues (contrast, color dependencies) without requiring manual intervention
- **Report Generation:** Generate accessibility compliance reports for client deliverables (Professional+ plans)

---

## 5. Multi-Brand Workspace Configuration

For agencies, franchises, and companies managing multiple distinct brands, Lovart's multi-brand workspace prevents cross-contamination.

### Workspace Organization

```
Lovart Account
├── Workspace: "Client A — Tech Startup"
│   ├── Brand Kit: Core Brand
│   ├── Brand Kit: Product Line B
│   └── Brand Kit: Event Series C
├── Workspace: "Client B — DTC Fashion"
│   ├── Brand Kit: Main Label
│   └── Brand Kit: Diffusion Line
└── Workspace: "Internal — Agency Brand"
    └── Brand Kit: Agency Identity
```

### Workspace Settings

- **Brand Isolation:** AI generations within Workspace A can never accidentally reference Brand Kit elements from Workspace B
- **Team Permissions:** Assign designers to specific workspaces. Junior designers may only access Workspace A; creative directors access all.
- **Shared Asset Library:** Define which assets (stock images, icons, templates) are shared across workspaces vs. workspace-specific
- **Cross-Client Safety:** Lovart's safety layer prevents client-A brand colors from appearing in client-B deliverables

### Workspace Switching

Toggle between workspaces from the top-left workspace selector. Keyboard shortcut: `Cmd+Shift+W` (Mac) / `Ctrl+Shift+W` (Windows). Each workspace maintains its own generation history, draft library, and AI memory.

---

## 6. Export Profiles & Brand Governance

For brands with strict output requirements, Export Profiles enforce consistency at the file level.

### Profile Configuration

Define export profiles for different use cases:

**Web Export Profile:**
- Format: SVG (logos), WebP (images), PNG fallback
- Color space: sRGB
- Resolution: 72 PPI (2x and 3x retina variants)
- Metadata: Strip EXIF, embed copyright and brand contact info
- Naming convention: `brand_campaign_assetname_dimensions_date.ext`

**Print Export Profile:**
- Format: EPS (logos), TIFF (images), PDF (documents)
- Color space: CMYK (with specified ICC profile)
- Resolution: 300 PPI minimum
- Bleed: 3mm all sides (customizable)
- Naming convention: `BRAND_CAMPAIGN_ASSETNAME_CMYK_DATE.ext`

**Social Media Export Profile:**
- Format: JPEG (quality 85%), PNG (when transparency needed)
- Color space: sRGB
- Resolution: Platform-specific (1080x1080, 1080x1920, 1200x628, etc.)
- Auto-crop to platform specs
- Add platform-optimized alt text

### Governance Locks

For Enterprise plans, administrators can lock specific Brand Kit settings:

- **Lock Logo Usage:** Prevent any generation from modifying logo proportions, minimum size, or clear space
- **Lock Color Palette:** Prevent AI from generating non-approved colors (even as accents)
- **Lock Typography:** Restrict font usage to approved families only
- **Lock Tone of Voice:** Enforce brand voice guidelines through AI prompt injection at the system level

Locked settings appear with a lock icon and cannot be overridden without admin credentials.

---

## 7. API & Automation Integration

The Brand Kit's advanced settings are fully accessible through Lovart's API.

### Key API Endpoints

```
GET    /v2/brand-kits/{id}/variants          List all variants
POST   /v2/brand-kits/{id}/variants          Create variant
GET    /v2/brand-kits/{id}/rules             List conditional rules
PUT    /v2/brand-kits/{id}/rules/{rule_id}   Update rule
POST   /v2/brand-kits/{id}/memory/reset      Reset AI memory
GET    /v2/brand-kits/{id}/compliance        Run brand compliance check
POST   /v2/workspaces                        Create workspace
```

### Automation Examples

**CI/CD Brand Pipeline:**
```bash
# On every product launch, generate platform-specific assets using the campaign variant
curl -X POST https://api.lovart.ai/v2/generate \
  -H "Authorization: Bearer $LOVART_API_KEY" \
  -d '{
    "brand_kit_id": "bk_abc123",
    "variant": "product_launch_spring",
    "content_type": "social_media_instagram_post",
    "prompt": "New spring collection announcement"
  }'
```

**Scheduled Brand Audits:**
Set up automated weekly brand compliance checks across all client workspaces. Receive Slack notifications for any generation that deviated from brand rules.

---

## Quick Reference: Plan Feature Matrix

| Feature | Free | Starter ($19) | Pro ($49) | Business ($99) | Enterprise ($149) |
|---------|------|---------------|-----------|----------------|-------------------|
| Brand Variants | 1 | 3 | 10 | Unlimited | Unlimited |
| Conditional Rules | — | 5 | 25 | 100 | Unlimited |
| AI Brand Memory | — | 30 days | 30 days | 90 days | Unlimited + rollback |
| Accessibility Profiles | Basic | Basic | Full CVD | Full + Auto-fix | Full + Custom profiles |
| Multi-Brand Workspaces | 1 | 3 | 10 | 50 | Unlimited |
| Export Profiles | Default | 3 | 10 | 25 | Custom unlimited |
| Governance Locks | — | — | — | Partial | Full |
| API Access | — | Read | Read/Write | Full | Full + Webhooks |

**[Start Creating Free — No Credit Card Required](https://www.lovart.ai/)**

## Frequently Asked Questions

### Can I use the designs commercially?
Yes. Every design, image, and video you create with Lovart is yours to use commercially — for ads, products, client work, social media, print, or anything else. No attribution required.

### Do I need design experience to use this?
No. Lovart is built for non-designers. You describe what you want in plain language, and the AI design agent handles the rest. The Touch Edit feature lets you refine results by tapping, not by learning complex software.

### Can I trademark an AI-generated logo?
Yes, but it depends on how you use it. AI-generated logos that you modify and use as part of your brand identity can be trademarked. The key is making the logo distinctively yours through customization. Read our full copyright guide for details.

### How is Lovart different from other AI design tools?
Unlike Midjourney, DALL-E, or Canva — which generate images or use templates — Lovart is an AI Design Agent. It understands your business context through MCoT (Mind Chain of Thought), lets you edit specific parts without regenerating (Touch Edit), keeps your brand consistent automatically (Brand Kit), and exports in professional formats (PSD, SVG, PDF).

### Can I try it for free?
Yes. Lovart's Free plan gives you 50 image generations per month, access to 5 AI models, Touch Edit (10 edits/month), and Brand Kit setup. No credit card required.

---

*This documentation reflects Lovart Brand Kit v4.2 as of July 2027. Features and API endpoints are subject to change. For the latest version, visit docs.lovart.ai/brand-kit.*

---

**[Start Creating — Free, No Credit Card Required](https://www.lovart.ai/)**
