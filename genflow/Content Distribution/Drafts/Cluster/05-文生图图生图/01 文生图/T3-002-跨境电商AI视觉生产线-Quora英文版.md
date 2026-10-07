# I Built a One-Person AI Visual Production Line for Cross-Border E-Commerce — Here's How It Works

> **Type**: T3 · Workflow Deep-Dive  
> **Author**: A marketing veteran who's optimized visuals for 20+ cross-border sellers and nearly went bald dealing with platform image requirements  
> **Use Case**: Cross-border e-commerce · Batch product image processing · Multi-language listing visual adaptation  
> **Reading Time**: 12 minutes

---

## Who Is This For?

I come from a marketing background and started working with cross-border e-commerce in 2018 — Amazon, AliExpress, Shopee, TikTok Shop — I've created over 2,000 listing images for sellers. The visual demands of cross-border selling are insane: the same product needs a pure white background 2000×2000 main image for Amazon, an 800×800 lifestyle shot for Shopee, a short video cover for TikTok Shop, and yet another lifestyle scene for your independent store. One SKU means at least 20 images. Ten SKUs? That's 200. The traditional approach — outsourcing to designers at ¥100-500 per image — means a single store launch can eat thousands in profit just on visuals.

Over the past two years, I've been iterating on a question: **How do you build an AI-powered visual production line that takes a white-background product photo and outputs platform-ready listing visuals across every channel — all run by one person in a day?** This article is the answer.

---

## The Bottom Line Up Front

**The one-sentence version**: Chain together 5 tools — Rembg (background removal) + Real-ESRGAN (upscaling) + Liblib (style reference) + Lovart (branding) + LibTV (video) — and compress one SKU's full-platform visual production from 3 days to 2 hours, with costs dropping from thousands of yuan to pocket change.

**Here's the data:**

| Stage | Tool | Output | Time | Cost |
|-------|------|--------|------|------|
| ① Preprocessing | Rembg + Real-ESRGAN | High-res white-background product image | 5 min/SKU | Free |
| ② Style Direction | Liblib | Scene style references + reusable workflows | 10 min (one-time) | Free |
| ③ Branded Output | Lovart | White-background + lifestyle + multi-size images | 15 min/SKU | ¥99/mo |
| ④ Video Production | LibTV | Product showcase short video | 20 min/SKU | Free / pay-as-you-go |
| ⑤ Distribution | Cap + Postiz | Listing images + video publishing | 10 min | Free |
| **Total** | — | **Full-platform visual assets** | **< 60 min/SKU** | **≈ ¥99/mo** |

> 💡 Traditional approach per SKU: 2-3 days, ¥1,000-3,000 outsourcing. This AI workflow gives cross-border sellers a "one-person visual factory."

---

## The Big Picture: How the 5 Tools Connect

```
┌──────────────────────────────────────────────────────────────────────┐
│              Cross-Border E-Commerce AI Visual Production Line        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ① Preprocessing           ② Style Direction       ③ Branded Output  │
│  ┌──────────────┐         ┌───────────┐          ┌─────────────┐    │
│  │ Rembg        │         │ Liblib    │          │ Lovart      │    │
│  │ Remove BG    │────────▶│ Find scene │─────────▶│ Brand Kit   │    │
│  │ Real-ESRGAN  │         │ references│          │ Batch output │    │
│  │ Upscale      │         │ Build lib │          │ Multi-size   │    │
│  └──────────────┘         └───────────┘          └──────┬──────┘    │
│                                                          │           │
│                                                          ▼           │
│  ⑤ Distribution            ④ Video Production                       │
│  ┌──────────────┐         ┌─────────────┐                           │
│  │ Cap          │         │ LibTV       │                           │
│  │ Screen demos │◀────────│ Images→Video│                           │
│  │ Postiz       │         │ Product vid │                           │
│  │ Multi-channel│         └─────────────┘                           │
│  └──────────────┘                                                    │
│                                                                      │
│  Data Flow: Raw Photo → HD White BG → Styled Scene → Video → Multi-Platform │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step: Making Each Link Work

### Step ① Preprocessing: Rembg + Real-ESRGAN — From "Messy Raw Photo" to "HD White-Background Product Image"

#### The Pain Point

Every cross-border seller knows this nightmare: supplier photos are all over the place. Shot casually in a warehouse with messy backgrounds. 800×800 resolution when Amazon demands 2000×2000 minimum. Crooked, poorly exposed, color-shifted. Upload these directly to a listing and your conversion rate tanks — Amazon's A9 algorithm is sensitive to main image quality, and low-res images don't even get impressions.

#### The Solution

**Two-step preprocessing that turns any raw photo into a usable HD white-background product shot:**

**Step 1: Rembg batch background removal.**  
Rembg (github.com, 23.3K Stars) is an open-source AI background removal tool. Usage is dead simple:

```bash
# Single image
rembg i product_raw.jpg product_nobg.png

# Batch process an entire folder
rembg p ./raw_photos ./white_bg_photos
```

One command processes 200 product photos in a folder. For e-commerce hard-edged products (electronics, home goods, luggage), Rembg's accuracy is 90%+ — more than good enough. Soft-edged products (clothing, plush toys, jewelry) may need manual touch-ups, but you've still saved 80% of manual work.

**Step 2: Real-ESRGAN super-resolution upscaling.**  
Real-ESRGAN (github.com, 35K+ Stars) is Tencent ARC Lab's open-source super-resolution tool. Upscale the background-removed images to meet platform resolution requirements:

```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i white_bg_product.png -o product_4x.png
```

4× upscaling turns an 800px image into 3200px — more than enough for Amazon's 2000×2000 requirement. Real-ESRGAN's JPEG artifact restoration is particularly suited for e-commerce — those WhatsApp-compressed supplier photos come out with surprisingly good detail.

#### Key Details

- **Order matters**: Remove background first, then upscale. Don't waste compute upscaling with a background you're going to remove.
- **Use PNG format**: Output background-removed images as PNG to preserve the alpha channel — you'll need transparency for scene compositing later.
- **Batch script it**: Write a simple shell script chaining both steps. Drop in a folder, get out HD white-background images.
- **Cost**: Both tools are free, open-source, and run locally. Zero cost.

---

### Step ② Style Direction: Liblib — From "No Idea What Style" to "Style Plan Locked In"

#### The Pain Point

White-background images are done, but white-background-only listings feel bare — especially on Shopee and TikTok Shop, where lifestyle images with scenes convert 3-5× better than pure white-background shots. The question: what style? Nordic minimalism or American retro? Warm tones or cool? Coffee table or beach? Every style decision is a decision-paralysis nightmare.

#### The Solution

**Liblib is your "style advisor."**

Open Liblib's Inspiration Gallery (liblib.art) and search by product category:
- Home goods: "Nordic style scene home"
- Electronics: "tech desk product showcase"
- Apparel: "street style outfit lookbook"
- Beauty: "ins style skincare scene"

When you find visually compelling work, **don't just look — bookmark and tag**. Build a library of 10-20 style references per category. This becomes your "style template library." For each new product, pick 2-3 matching style directions from your library.

Even more advanced: **directly clone workflows from Liblib.** Many creators share complete ComfyUI/Stable Diffusion workflows — which models, LoRAs, and parameter combos reliably produce a given style. One-click clone to your ComfyUI, swap in your product image. If you don't use SD, extract the prompt structures and feed them to Lovart.

#### Key Details

- **Build style libraries by category**: 5-10 reference images per category. Reuse directly instead of starting from scratch every time.
- **Triple-keyword search**: Use "product + style + scene" — e.g., "Bluetooth earbuds tech desk."
- **Pay attention to trending styles**: Sort by popularity on Liblib. High-engagement work often represents broader aesthetic preferences — good for e-commerce.
- **Cost**: Completely free.

---

### Step ③ Branded Output: Lovart — From "Scattered Assets" to "Unified Brand Visuals"

#### The Pain Point

This is the core pain of cross-border visual work — **style consistency.** Designer A does one set of scene images today. Tomorrow, designer A is booked, you hire designer B, and the style is completely different. Six images on a listing with six different styles — buyers scroll through and think "unprofessional." Even worse: **multi-size adaptation.** Same hero visual needs to be 1:1 square for Amazon, 3:4 for Shopee's first image, 16:9 for your independent store banner, 2:3 for Pinterest. Manual cropping and recomposition for one SKU across platforms can eat half a day.

#### The Solution

**Lovart's Brand Kit solves brand consistency and multi-size adaptation in one shot.**

Here's the workflow:

**Step 1: Build your Brand Kit (one-time, 30 minutes).**  
In Lovart (lovart.ai), create your brand:
- Upload your logo (white-background and dark-background versions)
- Set your brand color palette (primary + secondary + accent + neutral)
- Choose font combinations (heading + body)
- Define visual style keywords (e.g., "clean, professional, warm lighting, lifestyle")

**Step 2: Drive batch output with Brand Kit.**  
Feed Step ①'s HD white-background product images + Step ②'s style references into Lovart:
- "Product white-background + Nordic scene = lifestyle product image"
- "Product white-background + Brand Kit = main image with brand watermark and standard layout"

Lovart's MCoT reasoning engine automatically adjusts output style based on your Brand Kit, ensuring every image aligns with brand guidelines.

**Step 3: One-click multi-size export.**  
Same visual concept, Lovart exports in one click:
- Amazon main image: 2000×2000
- Amazon A+ Content: 970×600 / 970×300
- Shopee cover: 800×800
- TikTok Shop: 9:16 vertical
- Independent store banner: 1920×600
- Pinterest: 1000×1500

No manual cropping, no recomposition. Lovart intelligently adjusts layout for each size.

#### Key Details

- **Brand Kit is your core asset.** Spend 30 minutes building it once and save 30 hours later. Every new SKU auto-applies it.
- **Optimize scene prompts**: Add category keywords when describing scenes in Lovart. "The product sits on a sunlit modern kitchen marble countertop, soft natural light streaming through windows" is far more accurate than "in a kitchen."
- **A/B test**: Generate 3 different style variants for the same product, run ad tests to see which CTR wins.
- **Cost**: Lovart Pro ¥99/month, Brand Kit + unlimited generations. One month might save you an entire SKU's outsourcing design fee.

---

### Step ④ Video Production: LibTV — From "Static Image" to "Product Video That Sells"

#### The Pain Point

In 2025 cross-border e-commerce, static listings aren't enough anymore. TikTok Shop and Reels short-video commerce have the highest conversion rates, and Amazon listings now support main image video. But making product videos has a much higher barrier than images — you need lighting and set design for shooting, Premiere skills for editing, and separate workflows for effects and subtitles. A 30-second product showcase video costs ¥500-2,000 to outsource. Ten SKUs? That's ¥10,000+.

#### The Solution

**LibTV uses node-based workflows to turn static product images into dynamic showcase videos — no shooting, no editing skills required.**

Here's the workflow:

**Step 1: Import branded visual assets.**  
Batch import Step ③'s Lovart-generated scene images, white-background shots, and detail close-ups into LibTV (liblib.tv).

**Step 2: Choose a node workflow template.**  
The LibTV community has tons of pre-built node workflows for e-commerce:
- "Product 360° Showcase": Image sequence + rotation camera movement
- "Feature Close-up": Local zoom + annotation animations
- "Scene Switch": Multiple scene dissolves
- "Unboxing Demo": Simulated unboxing process

Pick a template matching your category, swap in your assets.

**Step 3: Add subtitles and brand elements.**  
LibTV supports speech-to-subtitle — convert your product selling-point copy to TTS audio, auto-generate timed subtitles. Add brand logo watermark, end-screen CTA, and you've got a 30-second product video.

#### Key Details

- **Camera movement is everything**: For static product images, the Ken Burns effect (slow zoom + pan) is the safest choice — natural, not forced.
- **Keep it fast**: Cross-border product videos work best at 15-30 seconds. First 3 seconds must grab attention.
- **Batch production**: Build one product video workflow template. For each SKU, just swap assets. 10 SKUs done in a day.
- **Seamless Lovart handoff**: Lovart outputs images → LibTV turns them into video → complete production pipeline.
- **Cost**: Core features free. Heavy usage is pay-as-you-go but very cheap.

---

### Step ⑤ Distribution: Cap + Postiz — From "Upload One by One" to "One-Click Omnichannel"

#### The Pain Point

Assets are ready. Now comes the most painful part — uploading. Amazon Seller Central: 6 images, one by one. Then Shopee again. Then TikTok Shop again. Then Shopify for your independent store. Ten SKUs × four platforms = 40 upload operations. And each platform has different filename, format, and ordering requirements. Get one wrong and your listing gets rejected.

#### The Solution

**Daily communication with Cap, batch publishing with Postiz.**

**Cap** (github.com, 17.2K Stars) for quick recording and sharing:
- Record "this product photo isn't right, shoot it like this" demos for suppliers
- Record listing upload SOPs for your team
- Record product demo videos for customers

Record, get an instant share link. They click and watch — no download needed.

**Postiz** (github.com, 27K Stars) for social media distribution:
- Connect TikTok, Instagram, Pinterest, YouTube accounts
- Upload once, schedule publishing across platforms
- Fine-tune content per platform (different titles, descriptions, hashtags)

#### Key Details

- **Use Cap instead of WeChat video calls for supplier communication**: Async is more efficient, rewatchable, and leaves a record.
- **Schedule product video social posts with Postiz**: Research optimal posting times per platform, batch schedule.
- **Cost**: Both tools are free and open-source.

---

## Full Workflow Review

### Timeline Breakdown (Per SKU)

| Time | Step | Tool | Action | Output |
|------|------|------|--------|--------|
| T+0 min | Preprocessing | Rembg + Real-ESRGAN | Remove background + 4× upscale | HD white-background product image |
| T+5 min | Style Direction | Liblib | Select references from style library | 2-3 style directions |
| T+10 min | Branded Output | Lovart | Brand Kit batch generation | White-background + scene + multi-size images |
| T+25 min | Video Production | LibTV | Node workflow video generation | 30s product showcase video |
| T+45 min | Distribution | Postiz + Cap | Multi-platform scheduling + team sharing | All channels scheduled |

### Common Pain Points & Troubleshooting

| Pain Point | Cause | Solution |
|------------|-------|----------|
| Rembg rough edges | Soft edges / transparent materials on product | Use `isnet-general-use` model instead of default u2net |
| Real-ESRGAN out of VRAM | 4K large image direct upscaling | Add `--tile 400` flag for tiled processing |
| Lovart inconsistent scene styles | No Brand Kit in use | Build Brand Kit first, base all outputs on it |
| LibTV video drags | Individual image displayed too long | Shorten each image's camera movement time, keep total 15-30s |
| Platform image requirements differ | Different sizes/formats/naming per platform | Lovart multi-size export + establish platform naming conventions |

---

## Cost Comparison: Traditional vs. AI Workflow

| Dimension | Traditional | AI Workflow | Savings |
|-----------|-------------|-------------|---------|
| **Time per SKU** | 2-3 days | < 1 hour | ↓95% |
| **Cost per SKU** | ¥1,000-3,000 (outsourced design) | ≈ ¥5-10 (monthly tool fee amortized) | ↓98%+ |
| **Monthly SKU capacity (1 person)** | 5-8 | 30-50 | ↑5-6× |
| **White-background image cost** | ¥50-100/image (photography/retouching) | Free (Rembg batch processing) | ↓100% |
| **Scene image cost** | ¥200-500/image (designer compositing) | ≈ ¥2/image (Lovart generation) | ↓99% |
| **Video cost** | ¥500-2,000/video (outsourced) | ≈ ¥1-3/video (LibTV) | ↓99% |
| **Multi-platform distribution** | Upload one by one, 1-2h/session | Postiz scheduling, 5min/session | ↓95% |
| **Monthly tool fees** | Adobe suite ¥400+ | Lovart ¥99/month (rest free) | ↓75% |

> 📊 **The core economic insight**: A 30-SKU store costs ¥30,000-90,000 in visual production with the traditional approach. The AI workflow caps it at ¥99/month in tool fees. That's three orders of magnitude difference.

---

## Who This Is For (And Who It's Not)

### ✅ Perfect For

| Who | Why |
|-----|-----|
| **Cross-border sellers (10+ SKUs)** | Batch image demand is high enough for massive workflow ROI |
| **DTC brands** | Brand Kit ensures consistency; unified multi-platform asset output |
| **Shopee / Lazada / TikTok Shop sellers** | Southeast Asian platforms demand scene images; AI generation cost advantage is huge |
| **Independent store operators** | Product images, banners, social media assets — one workflow handles all |
| **Solopreneurs / small teams** | No need to hire designers. One person + one workflow = visual department |
| **FBA bulk-listing sellers** | Many SKUs, fast listing turnover — batch processing is a must |

### ⚠️ Needs Consideration

| Situation | Limitation |
|-----------|------------|
| **Ultra-luxury goods / jewelry** | AI-generated scene quality may not feel "luxurious" enough — need pro photography |
| **Products requiring extreme color accuracy** | AI processing introduces subtle noise — color-critical products need manual calibration |
| **Unusually shaped products** | Highly irregular shapes may challenge Rembg's background removal accuracy |

### ❌ Not Ideal For

| Situation | Why |
|-----------|-----|
| Sellers with only 1-2 SKUs | Workflow setup cost exceeds outsourcing cost |
| Images requiring guaranteed legal copyright | AI-generated image copyright issues still carry risk on some platforms (though Amazon now accepts AI-generated images) |

---

## Advanced Plays: Making the Production Line Smarter

1. **Competitor visual monitoring**: Periodically scrape competitor listing main images, analyze style trend shifts, adjust your own style library.
2. **A/B testing automation**: Generate 3 different style variants per product, run ad tests on CTR and conversion, let data pick the winner.
3. **Seasonal / holiday templates**: Build "Christmas edition," "Black Friday edition," "Summer edition" variants in Lovart Brand Kit — one-click switching.
4. **Multi-language localization**: Replace text elements in Lovart scene images per target market language. Find culturally-matched style prompts on Liblib.

---

## One-Sentence Summary

> **Rembg removes backgrounds, ESRGAN sharpens quality, Liblib defines style, Lovart outputs branded kits, LibTV makes videos, Cap handles sharing, Postiz distributes everywhere — seven tools, one pipeline. A one-person cross-border visual factory that runs faster than a design team.**

---

*If this article helped you, bookmark and share it. I'll be breaking down specialized visual workflows per category (3C electronics, home goods, apparel, beauty) — including ComfyUI node templates and Lovart Brand Kit configuration sharing.*

**#CrossBorderEcommerce #AIWorkflow #ListingOptimization #ProductPhotography #VisualContent #Automation #Solopreneur**
