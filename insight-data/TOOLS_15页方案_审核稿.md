# 15 个新增 Tools 页面方案

> 基于 Sanity 生产环境真实规范 | 只读分析, 待审核后执行

---

## 一、真实 Section 规范 (从 ai-avatar-generator 提取)

| # | Section type | 必须字段 | 子结构 |
|---|-------------|---------|--------|
| 1 | hero-split | badge, title, highlightedText, description, buttons, media | buttons: [{text, href, variant}], media: {src, alt} |
| 2 | bento-4 | title, description, columns, features[4] | features[n]: {title, description, media: {src, alt}} |
| 3 | bento-2 | title, description, columns, features[2] | 同上 |
| 4 | capability-tabs | title, tabs[4] | tabs[n]: {label, content: {title, description, media: {src, alt}}} |
| 5 | prompt-launcher | title, description, prompts[3], cta | prompts[n]: {label, prompt}, cta: {text} |
| 6 | logo-loop | text | — |
| 7 | cta-default | title, description, buttons | buttons: [{text, href, variant}] |
| 8 | workflow-horizontal | title, description, layout, steps[3] | steps[n]: {step, title, description} |
| 9 | comparison-table | title, description, headers[4], highlightColumn, rows[5] | rows[n]: {feature, values[3]} |
| 10 | cluster-block-dense | title, description, cards[6] | cards[n]: {icon, title, description} |
| 11 | feature-detail | title, description, items[4] | items[n]: {title, description, points[3], cta, media} |
| 12 | proof-block | title, description, cards[3] | cards[n]: {icon, title, description} |
| 13 | faq | title, items[5-7] | items[n]: {question, answer} |
| 14 | cta-default | (同 #7) | — |

**icon 可用值**: sparkle, refresh, brand, video, clock, flask, star, layout, download, zap, image, globe

---

## 二、15 页方案

### 页面选择原则
- 从已有的 443 slug 中选 15 个高价值品类
- 这些 slug 的框架已升级到 14-section，需要填充真实内容
- 优先覆盖高搜索量品类: poster, flyer, banner, ebook, certificate, invoice 等

### 15 页列表

| # | Slug | 品类 | 主关键词 | 模板 |
|---|------|------|---------|------|
| 1 | `ai-poster-maker` | 海报 | AI Poster Maker | A |
| 2 | `ai-flyer-maker` | 传单 | AI Flyer Maker | A |
| 3 | `ai-banner-maker` | 横幅 | AI Banner Maker | A |
| 4 | `ai-brochure-maker` | 手册 | AI Brochure Maker | A |
| 5 | `ai-business-card-maker` | 名片 | AI Business Card Maker | A |
| 6 | `ai-certificate-maker` | 证书 | AI Certificate Maker | A |
| 7 | `ai-ebook-cover-maker` | 电子书 | AI Ebook Cover Maker | A |
| 8 | `ai-invitation-maker` | 邀请函 | AI Invitation Maker | A |
| 9 | `ai-instagram-posts` | IG帖子 | AI Instagram Post Maker | C |
| 10 | `ai-social-media-content` | 社媒内容 | AI Social Media Content Creator | C |
| 11 | `ai-mockup-generator` | 样机 | AI Mockup Generator | B |
| 12 | `ai-product-photography` | 产品摄影 | AI Product Photography | B |
| 13 | `ai-infographic-creator` | 信息图 | AI Infographic Creator | B |
| 14 | `ai-presentation-maker` | 演示 | AI Presentation Maker | B |
| 15 | `ai-logo-design` | Logo | AI Logo Design Tool | B |

---

## 三、第 1 页完整内容方案: `ai-poster-maker`

### S1: hero-split

```json
{
  "type": "hero-split",
  "badge": "AI Poster Maker",
  "title": "AI Poster Maker — Create Professional Posters Instantly | Lovart",
  "highlightedText": "from text to print-ready in seconds",
  "description": "Generate stunning posters with AI. Create event posters, promotional posters, sale posters, and motivational posters — all from a simple text description. Professional layouts, print-ready export, and full brand control.",
  "buttons": [
    {"text": "Create a poster", "href": "/home", "variant": "primary"},
    {"text": "See poster examples", "href": "", "variant": "secondary"}
  ],
  "media": {"src": "[hero-url]", "alt": "AI Poster Maker"}
}
```

### S2: bento-4 — 4 种海报类型

```json
{
  "type": "bento-4",
  "title": "Four poster types Lovart creates",
  "description": "From event promotions to motivational prints, generate professional posters for every purpose.",
  "columns": 4,
  "features": [
    {
      "title": "Event posters",
      "description": "Concert, conference, festival, and party posters with eye-catching layouts and bold typography.",
      "media": {"src": "[url]", "alt": "Event poster design"}
    },
    {
      "title": "Promotional posters",
      "description": "Sale announcements, product launches and discount posters designed to drive action.",
      "media": {"src": "[url]", "alt": "Promotional poster design"}
    },
    {
      "title": "Business posters",
      "description": "Corporate posters, office signage and brand announcement posters with professional polish.",
      "media": {"src": "[url]", "alt": "Business poster design"}
    },
    {
      "title": "Motivational posters",
      "description": "Inspirational quote posters, team culture prints and decorative wall art for any space.",
      "media": {"src": "[url]", "alt": "Motivational poster design"}
    }
  ]
}
```

### S3: bento-2 — 2 种创作方式

```json
{
  "type": "bento-2",
  "title": "Two ways to create posters",
  "description": "Start from scratch with a text prompt or upload your own design assets.",
  "columns": 2,
  "features": [
    {
      "title": "Generate from text",
      "description": "Describe your poster idea — event name, style, colors — and Lovart creates multiple designs instantly.",
      "media": {"src": "[url]", "alt": "Generate poster from text"}
    },
    {
      "title": "Upload and enhance",
      "description": "Upload your logo, images or rough sketch and Lovart transforms them into a polished poster layout.",
      "media": {"src": "[url]", "alt": "Upload and enhance poster"}
    }
  ]
}
```

### S4: capability-tabs — 4 大能力

```json
{
  "type": "capability-tabs",
  "title": "Everything a poster maker should do",
  "tabs": [
    {
      "label": "Design",
      "content": {
        "title": "AI-powered poster design",
        "description": "Lovart's MCoT engine applies professional design principles — balance, hierarchy, contrast — to every poster automatically.",
        "media": {"src": "[url]", "alt": "AI poster design"}
      }
    },
    {
      "label": "Edit",
      "content": {
        "title": "Touch-edit any element",
        "description": "Tap to adjust colors, swap fonts, reposition text and resize elements without regenerating the entire poster.",
        "media": {"src": "[url]", "alt": "Touch edit poster"}
      }
    },
    {
      "label": "Brand",
      "content": {
        "title": "Auto-apply your brand kit",
        "description": "Upload your logo, colors and fonts once. Every poster automatically stays on-brand with zero manual adjustments.",
        "media": {"src": "[url]", "alt": "Brand kit poster"}
      }
    },
    {
      "label": "Export",
      "content": {
        "title": "Print-ready exports",
        "description": "Download posters as PNG, JPEG, SVG or PDF with CMYK color and bleed for professional printing.",
        "media": {"src": "[url]", "alt": "Export poster"}
      }
    }
  ]
}
```

### S5: prompt-launcher

```json
{
  "type": "prompt-launcher",
  "title": "Try the poster maker now",
  "description": "Describe what you want and let AI create it.",
  "prompts": [
    {"label": "Music festival poster", "prompt": "Create a bold music festival poster with neon colors, edgy typography, and a dramatic stage silhouette background"},
    {"label": "Sale promotion poster", "prompt": "Design a retail sale poster with big bold '50% OFF' text, clean layout and a vibrant red and white color scheme"},
    {"label": "Corporate event poster", "prompt": "Generate a professional corporate conference poster with minimalist design, blue accents and clear event details layout"}
  ],
  "cta": {"text": "Generate poster"}
}
```

### S6: logo-loop

```json
{"type": "logo-loop", "text": "Trusted by millions of creators worldwide"}
```

### S7: cta-default

```json
{
  "type": "cta-default",
  "title": "Start Creating Posters Free",
  "description": "No credit card. 50 free poster designs per month.",
  "buttons": [{"text": "Start Free", "href": "/home", "variant": "primary"}]
}
```

### S8: workflow-horizontal

```json
{
  "type": "workflow-horizontal",
  "title": "How the poster maker works",
  "description": "Three steps from idea to print-ready poster.",
  "layout": "horizontal",
  "steps": [
    {"step": "1", "title": "Describe your poster", "description": "Tell Lovart what kind of poster you need — event, sale, promotional — and pick a style."},
    {"step": "2", "title": "Generate and choose", "description": "The AI creates multiple poster variations. Pick your favorite or ask for more options."},
    {"step": "3", "title": "Refine and export", "description": "Touch-edit any element — colors, fonts, text — then download in PNG, JPEG, SVG or print-ready PDF."}
  ]
}
```

### S9: comparison-table

```json
{
  "type": "comparison-table",
  "title": "Poster maker: Lovart vs Canva vs Photoshop",
  "description": "See why creators switch to Lovart for poster design.",
  "headers": ["Need", "Canva", "Photoshop", "Lovart Poster Maker"],
  "highlightColumn": 3,
  "rows": [
    {"feature": "Creation speed", "values": ["30-60 minutes", "2-4 hours", "Seconds — just describe"]},
    {"feature": "Design skill required", "values": ["Basic design sense", "Professional training", "Zero — AI handles it"]},
    {"feature": "Unique designs", "values": ["Template-based, common", "Fully custom", "AI-generated, every time unique"]},
    {"feature": "Brand consistency", "values": ["Manual brand kit", "Manual", "Auto-apply brand kit"]},
    {"feature": "Print-ready export", "values": ["PDF only", "Multiple formats", "PNG, JPEG, SVG, PDF + CMYK bleed"]}
  ]
}
```

### S10: cluster-block-dense

```json
{
  "type": "cluster-block-dense",
  "title": "Why the AI poster maker matters",
  "description": "Six ways Lovart transforms how you create posters.",
  "cards": [
    {"icon": "clock", "title": "Create in seconds", "description": "What took hours in traditional tools now happens in seconds with AI."},
    {"icon": "sparkle", "title": "Professional quality", "description": "MCoT engine applies real design principles to every poster."},
    {"icon": "refresh", "title": "Unlimited variations", "description": "Generate dozens of poster designs from a single brief."},
    {"icon": "brand", "title": "Always on-brand", "description": "Your brand kit auto-applies — colors, fonts, logo — every time."},
    {"icon": "layout", "title": "Touch-edit control", "description": "Adjust any element without regenerating the entire design."},
    {"icon": "download", "title": "Print-ready export", "description": "PDF with CMYK bleed, PNG, JPEG, SVG — any format you need."}
  ]
}
```

### S11: feature-detail

```json
{
  "type": "feature-detail",
  "title": "Advanced poster maker features",
  "description": "Professional tools that make your posters stand out from the crowd.",
  "items": [
    {
      "title": "Smart layout engine",
      "description": "The AI analyzes your content and automatically applies the best layout — balanced hierarchy, proper whitespace, and eye-catching composition.",
      "points": ["Automatic text hierarchy based on content importance", "Smart image placement with proper margins and alignment", "Responsive layout adapts to any poster size or orientation"],
      "cta": {"text": "Create a poster", "href": "/home", "variant": "primary"},
      "media": {"src": "[url]", "alt": "Smart layout engine for posters"}
    },
    {
      "title": "Typography that commands attention",
      "description": "Access thousands of fonts and let the AI recommend the perfect type pairing for your poster's message and mood.",
      "points": ["AI-recommended font pairings based on poster style and mood", "Full control over weight, size, spacing, and color", "Upload custom fonts for complete brand consistency"],
      "cta": {"text": "Try typography", "href": "/home", "variant": "secondary"},
      "media": {"src": "[url]", "alt": "Poster typography"}
    },
    {
      "title": "Color palette intelligence",
      "description": "The AI generates color schemes optimized for your poster's purpose — bold for sales, elegant for events, professional for corporate.",
      "points": ["Industry-optimized color palettes for every poster type", "Extract colors from uploaded images for perfect harmony", "Accessibility-aware contrast for readable text"],
      "cta": {"text": "Explore colors", "href": "/home", "variant": "secondary"},
      "media": {"src": "[url]", "alt": "Poster color palette"}
    },
    {
      "title": "Multi-format export with bleed",
      "description": "Export your poster in any format with proper print specifications — CMYK color space, 3mm bleed, and 300 DPI resolution.",
      "points": ["Print-ready PDF with CMYK + 3mm bleed for professional printing", "Digital-optimized PNG and JPEG for social media and web", "Editable SVG for further customization in other tools"],
      "cta": {"text": "Start creating", "href": "/home", "variant": "primary"},
      "media": {"src": "[url]", "alt": "Export poster formats"}
    }
  ]
}
```

### S12: proof-block

```json
{
  "type": "proof-block",
  "title": "Why creators choose Lovart for poster design",
  "description": "Join millions of creators who switched from traditional tools.",
  "cards": [
    {"icon": "sparkle", "title": "10x faster than Canva or Photoshop", "description": "What takes 30-60 minutes in Canva or hours in Photoshop takes seconds with Lovart's AI poster maker."},
    {"icon": "refresh", "title": "No two posters look alike", "description": "Every poster is AI-generated fresh — your event poster won't look like anyone else's template."},
    {"icon": "brand", "title": "Brand-perfect every time", "description": "Upload your brand kit once and every poster automatically uses your colors, fonts, and logo."}
  ]
}
```

### S13: faq

```json
{
  "type": "faq",
  "title": "Frequently Asked Questions",
  "items": [
    {"question": "Is the AI poster maker free to use?", "answer": "Yes. Lovart's Free plan includes 50 poster designs per month with no credit card required. Upgrade to Starter ($19/month) for 500 designs, HD export, and Brand Kit features."},
    {"question": "Do I need design experience to create posters?", "answer": "No. Just describe the poster you want in plain language — event name, style preference, key information — and the AI handles layout, typography and composition automatically."},
    {"question": "Can I print the posters I create?", "answer": "Absolutely. Export your posters as print-ready PDF with CMYK color space and 3mm bleed for professional printing. Also available in PNG, JPEG, and SVG for digital use."},
    {"question": "How is Lovart different from Canva for posters?", "answer": "Canva requires you to manually arrange elements on templates. Lovart's AI generates complete, unique poster designs from your text description — no template hunting or manual layout work needed."},
    {"question": "Can I use my own images and logos in posters?", "answer": "Yes. Upload your photos, logos and brand assets. The AI incorporates them into the poster design while maintaining professional composition and brand consistency."},
    {"question": "What poster sizes are supported?", "answer": "Lovart supports all standard poster sizes including A3, A4, letter, tabloid, and custom dimensions. The layout automatically adapts to your chosen size."},
    {"question": "Do I own the commercial rights to my posters?", "answer": "Yes. Every poster you create with Lovart belongs to you with full commercial usage rights. No attribution required."}
  ]
}
```

### S14: cta-default

```json
{
  "type": "cta-default",
  "title": "Ready to create your poster?",
  "description": "Join millions of creators. Free 50 poster designs per month. No credit card.",
  "buttons": [{"text": "Start Creating Free", "href": "/home", "variant": "primary"}]
}
```

---

## 四、剩余 14 页差异化要点

### 页面 2: `ai-flyer-maker`
- **hero**: badge="AI Flyer Maker", title 含 "Flyer Maker"
- **bento-4**: 4 种传单类型 — Event flyers, Business flyers, Food menu flyers, Real estate flyers
- **comparison**: Lovart vs Canva vs InDesign
- **faq Q5**: "Can I create double-sided flyers?"

### 页面 3: `ai-banner-maker`
- **hero**: badge="AI Banner Maker", title 含 "Banner Maker"
- **bento-4**: 4 种横幅 — Web banners, Display ads, Social media banners, Email headers
- **bento-2**: 2 种尺寸 — Standard sizes vs Custom dimensions
- **comparison**: Lovart vs Canva vs Google Web Designer
- **faq Q4**: "What banner sizes are supported?"

### 页面 4: `ai-brochure-maker`
- **hero**: badge="AI Brochure Maker"
- **bento-4**: Bi-fold, Tri-fold, Product brochures, Company brochures
- **workflow** steps 含 "Choose brochure format" step
- **faq Q2**: "Can I create multi-page brochures?"

### 页面 5: `ai-business-card-maker`
- **hero**: badge="AI Business Card Maker"
- **bento-4**: Professional, Creative, Minimal, Industry-specific
- **comparison**: Lovart vs Vistaprint vs Canva
- **faq Q5**: "Can I order physical prints?"

### 页面 6: `ai-certificate-maker`
- **hero**: badge="AI Certificate Maker"
- **bento-4**: Completion, Achievement, Training, Gift certificates
- **faq Q3**: "Can I add signatures and seals?"

### 页面 7: `ai-ebook-cover-maker`
- **hero**: badge="AI Ebook Cover Maker"
- **bento-4**: Fiction, Non-fiction, Business, Educational
- **comparison**: Lovart vs Canva vs DIY designer
- **faq Q4**: "What formats for Kindle/KDP?"

### 页面 8: `ai-invitation-maker`
- **hero**: badge="AI Invitation Maker"
- **bento-4**: Wedding, Birthday, Corporate event, Party
- **faq Q3**: "Can I add RSVP details?"

### 页面 9: `ai-instagram-posts`
- **hero**: badge="AI Instagram Post Maker"
- **bento-4**: Feed posts, Stories, Reels covers, Carousel slides
- **bento-2**: Square (1:1) vs Portrait (4:5)
- **prompts**: 含 "Instagram feed post" "Story template" "Carousel post"
- **comparison**: Lovart vs Canva vs Later

### 页面 10: `ai-social-media-content`
- **hero**: badge="AI Social Media Content Creator"
- **bento-4**: Instagram, Facebook, LinkedIn, Twitter/X
- **faq Q5**: "Can I schedule posts directly?"

### 页面 11: `ai-mockup-generator`
- **hero**: badge="AI Mockup Generator"
- **bento-4**: Product, App screen, Print, Packaging
- **workflow**: Upload design → Choose scene → AI generates mockup → Export
- **comparison**: Lovart vs Placeit vs Smartmockups

### 页面 12: `ai-product-photography`
- **hero**: badge="AI Product Photography"
- **bento-4**: White background, Lifestyle, Studio, Ghost mannequin
- **comparison**: Lovart vs traditional photoshoot
- **faq Q2**: "Do I need a professional camera?"

### 页面 13: `ai-infographic-creator`
- **hero**: badge="AI Infographic Creator"
- **bento-4**: Data, Process, Timeline, Comparison
- **faq Q3**: "Can I import data from Excel/CSV?"

### 页面 14: `ai-presentation-maker`
- **hero**: badge="AI Presentation Maker"
- **bento-4**: Pitch decks, Training, Sales, Conference
- **comparison**: Lovart vs PowerPoint vs Google Slides vs Canva
- **faq Q4**: "Can I export to PowerPoint?"

### 页面 15: `ai-logo-design`
- **hero**: badge="AI Logo Design Tool" (note: 不是 maker, 是 design tool)
- **bento-4**: Wordmark, Icon-based, Lettermark, Combination
- **comparison**: Lovart vs Looka vs Canva vs 99designs
- **faq Q3**: "Will my logo be unique?"

---

## 五、不变的部分 (所有 15 页共享)

| Section | 是否定制 | 说明 |
|---------|---------|------|
| hero-split | 定制 ✓ | badge, title, description, buttons 按品类调整 |
| bento-4 | 定制 ✓ | features 按品类改写 |
| bento-2 | 定制 ✓ | 两种创建方式按品类改写 |
| capability-tabs | **共享** | Design/Edit/Brand/Export 四件套通用 |
| prompt-launcher | 定制 ✓ | 3 个 prompt 按品类改写 |
| logo-loop | **共享** | 固定文本 |
| cta-default | 定制 ✓ | title 含品类名 |
| workflow-horizontal | 定制 ✓ | 3 步流程按品类改写 |
| comparison-table | 定制 ✓ | 竞品按品类选择, 5 行数据按品类改写 |
| cluster-block-dense | **共享** | 6 个 card 通用 (仅调整描述中的品类名) |
| feature-detail | 定制 ✓ | 4 个 item 按品类深度改写 |
| proof-block | **共享** | 标准三件套 |
| faq | 定制 ✓ | 7 个 FAQ 按品类生成 |
| cta-default | 定制 ✓ | title 含品类名 |

---

## 六、执行策略

### Phase 1: 先做 1 页 (ai-poster-maker)
- 写入 Sanity, 在 staging/branch 环境验证
- 检查前端渲染效果
- 确认所有 section 正常显示

### Phase 2: 批量 14 页
- 基于 Phase 1 验证通过的模板复制 + 品类差异化
- 每页 14 个 section, 共 210 个 section 写入
- 图片先用现有 9 个 hero URL 占位

### Phase 3: 图片匹配
- 按品类匹配专属图片
- 替换占位 URL

### 安全保证
- ✅ 仅 UPDATE 已有 P0 骨架页的 bodyJson (不创建新文档)
- ✅ 使用 Sanity 原生 patch mutation (自动 revision)
- ✅ 仅修改 bodyJson 字段 (不碰 title/slug/seo/cover)
- ✅ 所有字段名和子结构均来自生产环境真实数据
