---
title: "Lovart API Complete Documentation Guide: Build Design Into Your Product"
date: 2027-10-15
week: W3
category: Wiki
tags: [lovart api documentation, lovart API, AI design API, REST API design, api reference, lovart developer]
seo_keywords: lovart api documentation, lovart API reference, AI design API, design generation API, REST API design tool, api integration guide, lovart developer docs
description: "Complete reference documentation for the Lovart API — authentication, endpoints, request formats, response handling, rate limits, webhooks, and SDK availability. Everything developers need to integrate AI design generation into their products."
author: Lovart Engineering
featured_image: /images/lovart-api-documentation.jpg
reading_time: 8 min
word_count: 1500
slug: wiki-api-documentation
platform: [Blog, Dev.to, GitHub]
status: published
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Lovart API Complete Documentation Guide: Build Design Into Your Product",
  "description": "--- title: "Lovart API Complete Documentation Guide: Build Design Into Your Product" date: 2027-10-15 week: W3 category: Wiki tags: lovart api documentatio",
  "url": "https://www.lovart.ai/01-wiki-api-documentation",
  "datePublished": "2026-05-12",
  "publisher": {
    "@type": "Organization",
    "name": "Lovart",
    "url": "https://www.lovart.ai"
  }
}
</script>

# Lovart API Complete Documentation Guide: Build Design Into Your Product

The Lovart API enables developers to integrate AI-powered design generation directly into their applications, workflows, and platforms. Whether you are building a social media scheduler that auto-generates post graphics, an e-commerce platform that creates product images on upload, or an internal tool that produces branded reports — the API gives you programmatic access to every Lovart capability available in the web interface.

This documentation covers everything you need to integrate: authentication, endpoint architecture, request/response formats, error handling, rate limits, webhooks, and available SDKs.

## Authentication

All API requests require authentication via API key. Generate your key in the Lovart Dashboard under **Settings → API**.

```
Authorization: Bearer lv_live_xxxxxxxxxxxxxxxxxxxxx
```

Two key types are available:

| Key Type | Prefix | Permissions | Rate Limit |
|----------|--------|-------------|------------|
| Test | `lv_test_` | Full API access, no design storage | 100 req/min |
| Live | `lv_live_` | Full API access with design storage | Varies by plan |

**Important:** Never expose your live API key in client-side code. Use server-side requests or a proxy endpoint. Test keys are safe for development and CI environments.

## Base URL

```
https://api.lovart.ai/v2
```

All requests use HTTPS. The API is versioned via URL path (`/v2/`). The current stable version is v2, released March 2027. v1 is deprecated and will be sunset on March 1, 2028.

## Core Endpoints

### Design Generation

**`POST /v2/designs/generate`**

Create a new design from a natural language prompt.

```json
{
  "prompt": "A minimalist product announcement banner for Instagram (1080x1080). Dark navy background, centered white product silhouette, subtle golden accent lines. Title: 'New Arrival' in sans-serif. CTA: 'Shop Now' bottom center.",
  "format": {
    "width": 1080,
    "height": 1080
  },
  "brand_kit_id": "bk_9a7b3c2d",
  "style_preset": "minimalist_corporate",
  "output_format": "png",
  "variations": 3
}
```

**Response:**

```json
{
  "id": "dsgn_x1y2z3a4",
  "status": "completed",
  "variations": [
    {
      "id": "var_a1",
      "url": "https://cdn.lovart.ai/designs/dsgn_x1y2z3a4/var_a1.png",
      "thumbnail_url": "https://cdn.lovart.ai/designs/dsgn_x1y2z3a4/var_a1_thumb.png"
    }
  ],
  "metadata": {
    "generation_time_ms": 2147,
    "prompt_tokens": 48,
    "model": "lovart-canvas-v3"
  }
}
```

Key parameters:
- **`prompt`** (required): Natural language description of the desired design. Maximum 2,000 characters.
- **`format`**: Target dimensions in pixels. Defaults to 1080×1080. Maximum supported size: 8192×8192.
- **`brand_kit_id`**: Reference to a saved Brand Kit for automatic color, font, and logo application.
- **`style_preset`**: Optional style direction. Available presets: `minimalist_corporate`, `bold_editorial`, `playful_illustration`, `luxury_minimal`, `tech_gradient`, `retro_vintage`, `dark_mode_elegant`.
- **`variations`**: Number of design variations to generate (1–6). Each variation counts as one generation toward your plan limit.
- **`output_format`**: `png`, `jpg`, `pdf`, `svg`, or `mp4` (for animated designs).

### Template-Based Generation

**`POST /v2/designs/generate-from-template`**

Generate a design starting from a Lovart template.

```json
{
  "template_id": "tmpl_halloween_poster_01",
  "modifications": {
    "headline": "Harvest Night Market — Oct 28",
    "brand_kit_id": "bk_9a7b3c2d",
    "color_overrides": {
      "primary": "#1a1a2e",
      "accent": "#e94560"
    }
  },
  "output_format": "png"
}
```

### Design Editing

**`POST /v2/designs/{design_id}/edit`**

Apply edits to an existing design via natural language instructions.

```json
{
  "instructions": "Remove the subtitle text. Enlarge the headline by 20%. Change the background gradient from blue to dark teal. Add our logo to the top right corner.",
  "brand_kit_id": "bk_9a7b3c2d"
}
```

The edit endpoint preserves the original design and creates a new version. All previous versions remain accessible via `GET /v2/designs/{design_id}/versions`.

### Batch Generation

**`POST /v2/designs/batch`**

Generate multiple designs in a single request. Ideal for campaigns requiring multiple format sizes from one prompt.

```json
{
  "prompt": "A summer sale announcement with tropical gradient background, bold white headline, and 'Up to 50% Off' badge.",
  "formats": [
    { "width": 1080, "height": 1080, "label": "instagram_feed" },
    { "width": 1080, "height": 1920, "label": "instagram_story" },
    { "width": 1200, "height": 628, "label": "facebook_link" },
    { "width": 600, "height": 200, "label": "email_header" }
  ],
  "brand_kit_id": "bk_9a7b3c2d",
  "output_format": "png"
}
```

The batch endpoint processes all formats in parallel and returns an array of results. You are billed per format, not per batch request.

### Brand Kit Management

| Endpoint | Description |
|----------|-------------|
| `GET /v2/brand-kits` | List all brand kits |
| `GET /v2/brand-kits/{id}` | Get a specific brand kit |
| `POST /v2/brand-kits` | Create a new brand kit |
| `PUT /v2/brand-kits/{id}` | Update a brand kit |
| `DELETE /v2/brand-kits/{id}` | Delete a brand kit |

**Creating a brand kit:**

```json
{
  "name": "Acme Corp 2027",
  "colors": {
    "primary": "#2563eb",
    "secondary": "#7c3aed",
    "accent": "#f59e0b",
    "background": "#ffffff",
    "text": "#111827"
  },
  "fonts": {
    "heading": "Inter",
    "body": "Inter"
  },
  "logo_url": "https://acme.com/logo.png",
  "logo_position": "top-right"
}
```

### Design Management

| Endpoint | Description |
|----------|-------------|
| `GET /v2/designs` | List designs (paginated) |
| `GET /v2/designs/{id}` | Get design details and variations |
| `GET /v2/designs/{id}/export` | Download design in specified format |
| `DELETE /v2/designs/{id}` | Delete a design and all variations |

### Templates

| Endpoint | Description |
|----------|-------------|
| `GET /v2/templates` | List available templates |
| `GET /v2/templates/{id}` | Get template details and preview |
| `GET /v2/templates/categories` | List template categories |

## Rate Limits

Rate limits are applied per API key and vary by subscription tier:

| Plan | Requests per Minute | Generations per Month |
|------|---------------------|----------------------|
| Free | 10 | 50 |
| Pro ($19/mo) | 30 | 500 |
| Studio ($49/mo) | 60 | 2,000 |
| Agency ($99/mo) | 120 | 10,000 |
| Enterprise ($149/mo) | Custom | Custom |

Rate limit headers are included in every response:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 27
X-RateLimit-Reset: 1697378400
```

When you exceed the rate limit, the API returns `429 Too Many Requests` with a `Retry-After` header indicating the number of seconds to wait.

## Webhooks

Lovart supports webhooks for asynchronous design generation events:

```
POST https://your-app.com/webhooks/lovart
```

Supported events:
- `design.completed` — Fired when a design generation finishes
- `design.failed` — Fired when a generation fails (includes error details)
- `batch.completed` — Fired when all designs in a batch are complete

Configure webhooks in the Lovart Dashboard under **Settings → API → Webhooks**. Each webhook delivery includes a `X-Lovart-Signature` header for verification (HMAC-SHA256 of the payload using your webhook secret).

## Error Handling

The API uses standard HTTP status codes:

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | — |
| 400 | Bad Request | Check request body format and required fields |
| 401 | Unauthorized | Verify your API key or regenerate |
| 402 | Payment Required | Upgrade your plan or add payment method |
| 429 | Rate Limited | Implement exponential backoff |
| 500 | Server Error | Retry with backoff; contact support if persistent |

All error responses follow this format:

```json
{
  "error": {
    "code": "invalid_prompt",
    "message": "Prompt exceeds maximum length of 2,000 characters.",
    "details": {
      "current_length": 2150,
      "max_length": 2000
    }
  }
}
```

## SDKs & Client Libraries

Official SDKs are available for:

- **Node.js / TypeScript:** `npm install @lovart/api` (v2.3.0, released September 2027)
- **Python:** `pip install lovart-api` (v2.1.0)
- **Ruby:** `gem install lovart-api` (v1.5.0)
- **PHP:** `composer require lovart/api` (v2.0.0)

Each SDK wraps the REST API with idiomatic methods, automatic retry with exponential backoff, webhook signature verification utilities, and TypeScript/Python type definitions.

Example (Node.js):

```javascript
import { Lovart } from '@lovart/api';

const lovart = new Lovart({ apiKey: process.env.LOVART_API_KEY });

const design = await lovart.designs.generate({
  prompt: 'A modern tech conference banner with...',
  format: { width: 1200, height: 628 },
  brandKitId: 'bk_9a7b3c2d',
  variations: 2
});

console.log(design.variations[0].url);
```

## Getting Started

1. [Create a Lovart account](https://lovart.ai/signup) if you do not have one
2. Generate an API key from the Dashboard
3. Read the [Quickstart Guide](https://docs.lovart.ai/quickstart) for a walkthrough of your first API call
4. Join the `#api-dev` channel in the [Lovart Community Discord](https://discord.gg/lovart) for real-time support
5. Report bugs and request features on the [Lovart API GitHub repository](https://github.com/lovart/api)

The Lovart API is the same engine that powers the ChatCanvas interface. Anything you can do in the app, you can automate through the API. Start building.

**[Start Creating Free — No Credit Card Required](https://www.lovart.ai/)**

## Frequently Asked Questions

### Can I use the designs commercially?
Yes. Every design, image, and video you create with Lovart is yours to use commercially — for ads, products, client work, social media, print, or anything else. No attribution required.

### Do I need design experience to use this?
No. Lovart is built for non-designers. You describe what you want in plain language, and the AI design agent handles the rest. The Touch Edit feature lets you refine results by tapping, not by learning complex software.

### How is Lovart different from other AI design tools?
Unlike Midjourney, DALL-E, or Canva — which generate images or use templates — Lovart is an AI Design Agent. It understands your business context through MCoT (Mind Chain of Thought), lets you edit specific parts without regenerating (Touch Edit), keeps your brand consistent automatically (Brand Kit), and exports in professional formats (PSD, SVG, PDF).

### Can I try it for free?
Yes. Lovart's Free plan gives you 50 image generations per month, access to 5 AI models, Touch Edit (10 edits/month), and Brand Kit setup. No credit card required.

---

**[Start Creating — Free, No Credit Card Required](https://www.lovart.ai/)**
