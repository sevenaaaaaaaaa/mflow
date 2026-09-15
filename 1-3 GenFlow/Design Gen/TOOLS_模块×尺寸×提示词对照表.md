# Tools 模块 × 尺寸 × 提示词 对照表

> 基于 Sanity 14-section 框架 + 24 品类 | 用于批量素材生成

---

## 一、5 种素材槽位 → 尺寸 → 生成提示词模板

每页需要 5 类图，每类对应固定的尺寸和提示词结构：

| 槽位                  | 尺寸       | 每页数量 | 特点        | 提示词模板  |
| ------------------- | -------- | ---- | --------- | ------ |
| **hero-split**      | 1200×630 | 1 张  | 大横图，产品主视觉 | 见 §1.1 |
| **bento-4**         | 600×400  | 4 张  | 方形功能卡片    | 见 §1.2 |
| **bento-2**         | 800×500  | 2 张  | 横版对比展示    | 见 §1.3 |
| **capability-tabs** | 800×500  | 4 张  | 横版能力展示    | 见 §1.4 |
| **feature-detail**  | 800×500  | 4 张  | 横版深度功能    | 见 §1.5 |

### 1.1 hero-split 提示词 (1200×630)

```
A professional hero-style banner image (1200x630) for a [品类名] tool landing page.
[风格描述]. Clean composition, modern SaaS aesthetic, subtle gradient background,
professional lighting. No text overlay — image only. 3D render style with soft shadows.
```

**按品类变体 (15种提示词)**：

| #   | 品类                 | 风格描述                                                                                                     |
| --- | ------------------ | -------------------------------------------------------------------------------------------------------- |
| 1   | video              | video editing timeline interface with playhead, clips, and waveform; cinematic color grading; dark theme |
| 2   | social-media       | phone mockup displaying Instagram-style grid of posts; vibrant colors; modern influencer aesthetic       |
| 3   | marketing          | digital ad dashboard with banner previews; conversion metrics; clean SaaS interface                      |
| 4   | brand-identity     | brand style guide spread with logo variations, color swatches, and typography samples; minimalist        |
| 5   | print-design       | physical printed materials (poster, flyer, business card) arranged on a desk; professional lighting      |
| 6   | ai-capability      | split-screen showing input (rough sketch/text) → output (polished AI result); futuristic tech aesthetic  |
| 7   | photo-editing      | before/after comparison of photo retouching; split-screen format; clean studio background                |
| 8   | design-tool        | AI design platform interface with canvas, toolbars, and generated designs; modern UI                     |
| 9   | product-ecommerce  | product photography setup with white background, softbox lighting, and product pedestal                  |
| 10  | document           | professional document mockups (ebook, report, whitepaper) spread on a minimalist desk                    |
| 11  | presentation       | slide deck preview on laptop screen with modern design; conference room background                       |
| 12  | education          | educational worksheet and flashcard designs spread on a teacher's desk; colorful and clean               |
| 13  | data-visualization | infographic and chart designs displayed on a large monitor; data storytelling aesthetic                  |
| 14  | interior-space     | AI-generated room visualization; split-screen showing empty room → furnished design                      |
| 15  | typography-design  | font specimen sheet with multiple typefaces, color palette swatches; designer's workspace                |

### 1.2 bento-4 提示词 (600×400) — 每页4张

```
A compact feature illustration (600x400, square-ish) showing [功能描述].
Flat illustration style with soft gradients, [品类] theme colors.
Clean white/light background. Icon-like composition with subtle depth.
No text in the image.
```

**功能类提示词模板池 (8种通用，按页轮换)**：

| #   | 功能描述                                                                                                   | 适用品类 |
| --- | ------------------------------------------------------------------------------------------------------ | ---- |
| F1  | AI generation engine creating content from text input — sparks and creative elements emerging          | 全部   |
| F2  | touch-edit interface with hand adjusting design elements — intuitive gesture interaction               | 全部   |
| F3  | brand kit integration — colors, fonts, logo auto-applying to multiple designs simultaneously           | 全部   |
| F4  | multi-format export — designs converting to PNG, JPEG, SVG, PDF, PSD file icons                        | 全部   |
| F5  | batch processing — multiple files being processed simultaneously in a queue interface                  | 全部   |
| F6  | collaboration workspace — multiple cursors editing a shared canvas in real-time                        | 全部   |
| F7  | template-free original creation — unique designs emerging from blank canvas, no cookie-cutter patterns | 全部   |
| F8  | version history timeline — design iterations stacked chronologically with rollback arrows              | 全部   |

### 1.3 bento-2 提示词 (800×500) — 每页2张

```
A wide illustration (800x500) contrasting two approaches to [品类].
Left side: [方式A]. Right side: [方式B] with an arrow or transition between them.
Modern infographic style, clean layout, [品类] theme colors.
No dense text — visual storytelling only.
```

**每种品类1个提示词 (15种)**：

| #   | 品类                 | 方式A                              | 方式B                                     |
| --- | ------------------ | -------------------------------- | --------------------------------------- |
| 1   | video              | typing text description          | finished video with effects             |
| 2   | social-media       | blank phone screen               | fully designed Instagram post grid      |
| 3   | marketing          | empty ad template                | high-converting ad with metrics         |
| 4   | brand-identity     | scattered logo sketches          | organized brand kit spread              |
| 5   | print-design       | blank paper/canvas               | printed poster with professional finish |
| 6   | ai-capability      | low-res/blurry input image       | AI-enhanced 4K output                   |
| 7   | photo-editing      | unedited raw photo               | professionally retouched portrait       |
| 8   | design-tool        | empty canvas with prompt box     | multiple AI-generated design variations |
| 9   | product-ecommerce  | product on plain background      | professional studio product shot        |
| 10  | document           | blank page with placeholder text | formatted ebook/whitepaper pages        |
| 11  | presentation       | empty slide with title only      | fully designed presentation deck        |
| 12  | education          | blank worksheet template         | filled colorful educational worksheet   |
| 13  | data-visualization | raw spreadsheet data             | polished infographic chart              |
| 14  | interior-space     | empty room photo                 | AI-staged room with furniture           |
| 15  | typography-design  | basic default text               | custom font specimen with pairings      |

### 1.4 capability-tabs 提示词 (800×500) — 每页4张

```
A feature demonstration image (800x500) for the '[能力名]' capability tab.
Showing [具体场景]. Clean SaaS UI aesthetic, [品类] theme, subtle depth.
Professional quality, no text overlay.
```

**通用4能力模板 (所有品类共享，每品类微调关键词)**：

| Tab | 能力名 | 具体场景 |
|-----|--------|---------|
| Design | AI Design Engine | AI interface with design canvas showing auto-generated [品类] layouts with composition grid overlay |
| Edit | Touch-Edit | hand/finger touching a [品类] element and adjusting it with real-time preview showing the change |
| Brand | Brand Kit | brand colors, fonts, and logo being applied to multiple [品类] variations simultaneously |
| Export | Multi-Format | a single [品类] design branching out into PNG, JPEG, SVG, PDF, PSD format icons |

### 1.5 feature-detail 提示词 (800×500) — 每页4张

```
A detailed feature showcase image (800x500) for '[功能名]'.
[场景描述]. Rich detail, soft lighting, [品类] theme colors.
Professional quality, cinematic depth of field. No text.
```

**通用4功能模板 (所有品类共享)**：

| 功能名 | 场景描述 |
|--------|---------|
| AI Design Engine | MCoT engine visualization — neural network patterns transforming text prompts into complete [品类] designs with design principle annotations |
| Smart Brand Automation | brand kit dashboard with one-click upload → auto-apply cascade across multiple [品类] variants |
| Batch Generation | factory/assembly line metaphor — multiple [品类] designs being generated simultaneously from a single input brief |
| Version Control | timeline interface showing design iterations with side-by-side comparison and rollback buttons |

---

## 二、提示词总量统计

### 2.1 按类型统计

| 类型 | 通用池 | 品类专属 | 合计提示词 |
|------|--------|---------|-----------|
| hero-split | 0 | 15 | **15** |
| bento-4 | 8 | 0 | **8** (每品类轮换) |
| bento-2 | 0 | 15 | **15** |
| capability-tabs | 4 | 0 | **4** (每品类微调关键词) |
| feature-detail | 4 | 0 | **4** (每品类微调关键词) |
| **合计** | **16** | **30** | **46 个独立提示词** |

### 2.2 按品类生成需求

| 品类 | 页数 | hero(1) | bento4(4) | bento2(2) | tabs(4) | detail(4) | 总图数 | 提示词数 |
|------|------|---------|-----------|-----------|----------|-----------|--------|----------|
| video | 42 | 42 | 168 | 84 | 168 | 168 | **630** | 1+8+1+4+4=18 |
| print-design | 29 | 29 | 116 | 58 | 116 | 116 | **435** | 18 |
| brand-identity | 22 | 22 | 88 | 44 | 88 | 88 | **330** | 18 |
| social-media | 26 | 26 | 104 | 52 | 104 | 104 | **390** | 18 |
| marketing | 24 | 24 | 96 | 48 | 96 | 96 | **360** | 18 |
| ai-capability | 31 | 31 | 124 | 62 | 124 | 124 | **465** | 18 |
| design-tool | 38 | 38 | 152 | 76 | 152 | 152 | **570** | 18 |
| photo-editing | 17 | 17 | 68 | 34 | 68 | 68 | **255** | 18 |
| 其余16品类 | 214 | 214 | 856 | 428 | 856 | 856 | **3,210** | 18/品类 |

---

## 三、批量生成工作流

### Step 1: 准备基础素材

为每个品类准备 1-3 张**参考图**或**风格种子**：
- 放置到品类对应的文件夹
- 用于 img2img 或 style reference

### Step 2: 按品类执行

```
for category in [video, print-design, brand-identity, ...]:
    1. 加载品类专属 hero 提示词 → 生成 1 张 hero
    2. 加载品类专属 bento2 提示词 → 生成 2 张 bento2
    3. 加载通用 bento4 提示词(8选4) → 生成 4 张 bento4
    4. 加载通用 tabs 提示词(×4) → 生成 4 张 tabs
    5. 加载通用 detail 提示词(×4) → 生成 4 张 detail
    6. 对同品类下每页轮换 bento4 的 4 张选择(从8张池中每页选不同组合)
```

### Step 3: 上传到 assets-persist

生成后批量上传到 Lovart assets CDN，获得 URL。

### Step 4: 写入 Sanity

用已有的 Sanity mutation 管线按品类批量替换 bodyJson 中的 media.src。

---

## 四、提示词完整索引

### hero-split (15个品类专属)

| ID  | 品类                 | 提示词(精简版)                                                                                |
| --- | ------------------ | --------------------------------------------------------------------------------------- |
| H1  | video              | video editing timeline interface, cinematic color grading, dark theme, 1200x630         |
| H2  | social-media       | phone mockup with Instagram grid, vibrant colors, 1200x630                              |
| H3  | marketing          | digital ad dashboard with banner previews, conversion metrics, SaaS aesthetic, 1200x630 |
| H4  | brand-identity     | brand style guide spread with logo variations and color swatches, minimalist, 1200x630  |
| H5  | print-design       | printed materials (poster/flyer/card) on desk, professional lighting, 1200x630          |
| H6  | ai-capability      | split-screen input→output, futuristic tech aesthetic, 1200x630                          |
| H7  | photo-editing      | before/after photo comparison, split-screen, studio background, 1200x630                |
| H8  | design-tool        | AI design platform interface with canvas and toolbars, modern UI, 1200x630              |
| H9  | product-ecommerce  | product on white pedestal with softbox lighting, 1200x630                               |
| H10 | document           | document mockups (ebook/report) on minimalist desk, 1200x630                            |
| H11 | presentation       | slide deck on laptop, conference room background, 1200x630                              |
| H12 | education          | worksheets on teacher desk, colorful and clean, 1200x630                                |
| H13 | data-visualization | infographics on large monitor, data storytelling, 1200x630                              |
| H14 | interior-space     | empty room → furnished design split-screen, 1200x630                                    |
| H15 | typography-design  | font specimens and color swatches on designer workspace, 1200x630                       |

### bento-4 (8个通用，轮换使用)

| ID | 功能 | 提示词(精简版) |
|----|------|---------------|
| B1 | AI generation | sparks emerging from text input, creative elements, 600x400 |
| B2 | Touch-edit | hand adjusting design element, gesture interaction, 600x400 |
| B3 | Brand kit | colors/fonts/logo auto-applying to designs, 600x400 |
| B4 | Multi-format export | design converting to PNG/JPEG/SVG/PDF icons, 600x400 |
| B5 | Batch processing | files in queue being processed simultaneously, 600x400 |
| B6 | Collaboration | multiple cursors on shared canvas, 600x400 |
| B7 | Original creation | unique designs from blank canvas, no templates, 600x400 |
| B8 | Version history | iterations stacked with rollback arrows, 600x400 |

### bento-2 (15个品类专属)

| ID | 品类 | 提示词(精简版) |
|----|------|---------------|
| B2-1 | video | text description → finished video with effects, 800x500 |
| B2-2 | social-media | blank phone → designed Instagram grid, 800x500 |
| B2-3 | marketing | empty ad template → high-converting ad, 800x500 |
| B2-4 | brand-identity | scattered sketches → organized brand kit, 800x500 |
| B2-5 | print-design | blank canvas → printed poster, 800x500 |
| B2-6 | ai-capability | low-res input → AI-enhanced 4K output, 800x500 |
| B2-7 | photo-editing | unedited photo → retouched portrait, 800x500 |
| B2-8 | design-tool | empty canvas → AI-generated variations, 800x500 |
| B2-9 | product-ecommerce | plain background → studio product shot, 800x500 |
| B2-10 | document | blank page → formatted ebook pages, 800x500 |
| B2-11 | presentation | empty slide → designed presentation deck, 800x500 |
| B2-12 | education | blank worksheet → filled educational sheet, 800x500 |
| B2-13 | data-visualization | raw spreadsheet → polished infographic, 800x500 |
| B2-14 | interior-space | empty room → AI-staged room, 800x500 |
| B2-15 | typography-design | default text → custom font specimen, 800x500 |

### capability-tabs (4个通用)

| ID | Tab | 提示词(精简版) |
|----|-----|---------------|
| C1 | Design | AI interface with [品类] layouts and composition grid, 800x500 |
| C2 | Edit | hand touching [品类] element with real-time adjustment preview, 800x500 |
| C3 | Brand | brand kit applying to multiple [品类] variants, 800x500 |
| C4 | Export | single [品类] branching to format icons, 800x500 |

### feature-detail (4个通用)

| ID | 功能 | 提示词(精简版) |
|----|------|---------------|
| D1 | Design Engine | neural network → text to [品类], design principle annotations, 800x500 |
| D2 | Brand Automation | one-click upload → auto-apply cascade to [品类] variants, 800x500 |
| D3 | Batch Generation | assembly line of [品类] designs from single input, 800x500 |
| D4 | Version Control | timeline with side-by-side comparison and rollback, 800x500 |
