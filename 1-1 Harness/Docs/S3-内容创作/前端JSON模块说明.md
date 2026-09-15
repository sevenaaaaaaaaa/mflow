---
type: stage-sop/s3
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-creation"
tools: [opencode, claude]
status: active
path: 1-1 Harness/Docs/S3-内容创作/前端JSON模块说明.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# 前端 JSON 模块说明

> **文档定位**：前端 JSON 模块的详细说明  
> **更新日期**：2026-06-04  
> **适用范围**：Lovart 项目前端 JSON 模块开发和维护相关人员

---

## 一、概述

本文档为前端 JSON 模块提供详细的说明，涵盖 33 种 JSON 模块的定义、字段结构、使用示例和最佳实践。

### 1.1 JSON 模块概述

**JSON 模块** = `bodyJson` 里 `"type"` 字段的**具体组件**。

**模块统计：**
- 页面类型：**6**
- 页面本体（section 职责）：**17**（每类页面只用其中一部分）
- 可上线 JSON 模块：**33**
- 故事线合计：**19 条**

### 1.2 两个层级（别混）

| 层级 | 是什么 | 数量 | 举例 |
|------|--------|------|------|
| **本体** | 页面里一段 section 的**职责**（产品语言） | 17 种 | 「首屏」「能力 Tab」「步骤教程」 |
| **JSON 模块** | `bodyJson` 里 `"type"` 字段的**具体组件** | 33 种 | `hero-split`、`capability-tabs` |

**关系：** 每个本体在上线时选 **1 个** JSON `type`（若该本体对应多种组件，则从中择一 = **变体**）。

---

## 二、JSON 模块字典（33 种）

每种模块：`type` 字符串 = 上线 JSON 里的 `"type"`。示例字段见 `preview-data.json` 同名条目。

### 2.1 Hero 首屏（5 变体）

#### `hero-split`

**作用：** 左文右图，tag + 双行标题 + 按钮 + 4:3 大图

**适用场景：** 功能/工具页默认首屏，信息密度适中

**字段结构：**
```json
{
  "type": "hero-split",
  "tag": "string",
  "title": "string",
  "subtitle": "string",
  "button_text": "string",
  "button_url": "string",
  "hero_image": "string",
  "hero_image_alt": "string"
}
```

**使用示例：**
```json
{
  "type": "hero-split",
  "tag": "AI Design Tool",
  "title": "Create Stunning Designs with AI",
  "subtitle": "Lovart's MCoT-powered AI Creative Director understands your design needs",
  "button_text": "Start Designing",
  "button_url": "/ai-design-tool#start",
  "hero_image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
  "hero_image_alt": "Lovart AI creating a professional design"
}
```

#### `hero-cinematic`

**作用：** 居中标题 + 全宽剧院大图

**适用场景：** 品牌感强、视觉主导的 Product / Landing

**字段结构：**
```json
{
  "type": "hero-cinematic",
  "title": "string",
  "subtitle": "string",
  "button_text": "string",
  "button_url": "string",
  "hero_image": "string",
  "hero_image_alt": "string"
}
```

**使用示例：**
```json
{
  "type": "hero-cinematic",
  "title": "The Future of Design",
  "subtitle": "Powered by Lovart's AI Creative Director",
  "button_text": "Explore Now",
  "button_url": "/explore",
  "hero_image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
  "hero_image_alt": "Lovart AI design showcase"
}
```

#### `hero-journey`

**作用：** 居中标题 + 横向 step 卡片条

**适用场景：** 强调「用户旅程 / 多步骤路径」

**字段结构：**
```json
{
  "type": "hero-journey",
  "title": "string",
  "subtitle": "string",
  "steps": [
    {
      "title": "string",
      "description": "string",
      "icon": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "hero-journey",
  "title": "Your Design Journey",
  "subtitle": "From idea to masterpiece in 3 steps",
  "steps": [
    {
      "title": "Describe",
      "description": "Tell Lovart what you want to create",
      "icon": "pencil"
    },
    {
      "title": "Generate",
      "description": "AI creates multiple design options",
      "icon": "magic"
    },
    {
      "title": "Refine",
      "description": "Perfect your design with AI assistance",
      "icon": "edit"
    }
  ]
}
```

#### `hero-mosaic`

**作用：** 居中标题 + 不规则拼贴瓦片

**适用场景：** 多能力并列、修复/组合类叙事

**字段结构：**
```json
{
  "type": "hero-mosaic",
  "title": "string",
  "subtitle": "string",
  "tiles": [
    {
      "image": "string",
      "alt": "string",
      "label": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "hero-mosaic",
  "title": "All-in-One Design Platform",
  "subtitle": "Every tool you need in one place",
  "tiles": [
    {
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo Design",
      "label": "Logo Design"
    },
    {
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Poster Design",
      "label": "Poster Design"
    },
    {
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Social Media",
      "label": "Social Media"
    }
  ]
}
```

#### `hero-gallery`

**作用：** 居中标题 + 6 宫格工具入口

**适用场景：** 产品矩阵、多工具入口总览

**字段结构：**
```json
{
  "type": "hero-gallery",
  "title": "string",
  "subtitle": "string",
  "tools": [
    {
      "name": "string",
      "description": "string",
      "icon": "string",
      "url": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "hero-gallery",
  "title": "Design Tools",
  "subtitle": "Professional design tools powered by AI",
  "tools": [
    {
      "name": "Logo Maker",
      "description": "Create professional logos",
      "icon": "logo",
      "url": "/tools/logo-maker"
    },
    {
      "name": "Poster Designer",
      "description": "Design stunning posters",
      "icon": "poster",
      "url": "/tools/poster-designer"
    },
    {
      "name": "Social Media Kit",
      "description": "Complete social media designs",
      "icon": "social",
      "url": "/tools/social-media-kit"
    }
  ]
}
```

### 2.2 网格 / Bento / 信息簇（5 变体）

#### `bento-2`

**作用：** 两栏等大特性卡

**适用场景：** 两个核心卖点并列

**字段结构：**
```json
{
  "type": "bento-2",
  "cards": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "bento-2",
  "cards": [
    {
      "title": "AI-Powered",
      "description": "Advanced AI understands your design intent",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "AI Design"
    },
    {
      "title": "Professional Quality",
      "description": "Output meets professional standards",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Professional Design"
    }
  ]
}
```

#### `bento-4`

**作用：** 2×2 不规则四宫格

**适用场景：** 四个能力点，视觉有主次

**字段结构：**
```json
{
  "type": "bento-4",
  "cards": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string",
      "size": "large|small"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "bento-4",
  "cards": [
    {
      "title": "Logo Design",
      "description": "Create professional logos in minutes",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo Design",
      "size": "large"
    },
    {
      "title": "Poster Design",
      "description": "Design stunning posters",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Poster Design",
      "size": "small"
    },
    {
      "title": "Social Media",
      "description": "Complete social media kits",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Social Media",
      "size": "small"
    },
    {
      "title": "Brand Kit",
      "description": "Complete brand identity",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Brand Kit",
      "size": "large"
    }
  ]
}
```

#### `bento-6`

**作用：** 六卡 bento 布局

**适用场景：** 六个能力/场景，信息量大

**字段结构：**
```json
{
  "type": "bento-6",
  "cards": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "bento-6",
  "cards": [
    {
      "title": "Logo Design",
      "description": "Professional logos",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo Design"
    },
    {
      "title": "Poster Design",
      "description": "Stunning posters",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Poster Design"
    },
    {
      "title": "Social Media",
      "description": "Social media kits",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Social Media"
    },
    {
      "title": "Brand Kit",
      "description": "Brand identity",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Brand Kit"
    },
    {
      "title": "Website Design",
      "description": "Website layouts",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Website Design"
    },
    {
      "title": "App Design",
      "description": "Mobile app designs",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "App Design"
    }
  ]
}
```

#### `feature-grid`

**作用：** 2/3/4 列对称特性网格

**适用场景：** 均匀罗列功能点

**字段结构：**
```json
{
  "type": "feature-grid",
  "columns": 3,
  "features": [
    {
      "title": "string",
      "description": "string",
      "icon": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "feature-grid",
  "columns": 3,
  "features": [
    {
      "title": "AI-Powered",
      "description": "Advanced AI understands your design intent",
      "icon": "magic"
    },
    {
      "title": "Professional Quality",
      "description": "Output meets professional standards",
      "icon": "star"
    },
    {
      "title": "Fast & Easy",
      "description": "Create designs in minutes",
      "icon": "lightning"
    }
  ]
}
```

#### `cluster-block-dense`

**作用：** 3 列 icon 小卡墙

**适用场景：** 痛点列表、能力清单、内容簇

**字段结构：**
```json
{
  "type": "cluster-block-dense",
  "items": [
    {
      "title": "string",
      "description": "string",
      "icon": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "cluster-block-dense",
  "items": [
    {
      "title": "No Design Skills",
      "description": "AI handles the design for you",
      "icon": "user"
    },
    {
      "title": "Time Consuming",
      "description": "Create designs in minutes",
      "icon": "clock"
    },
    {
      "title": "Expensive",
      "description": "Professional results at low cost",
      "icon": "dollar"
    }
  ]
}
```

### 2.3 Tab / 矩阵 / 博客 / 图文（5 变体）

#### `capability-tabs`

**作用：** 左 Tab 列表 + 右大图内容区

**适用场景：** 多功能切换讲解（Features / Solution / Scenarios 核心模块）

**字段结构：**
```json
{
  "type": "capability-tabs",
  "tabs": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "capability-tabs",
  "tabs": [
    {
      "title": "Logo Design",
      "description": "Create professional logos with AI assistance",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo Design"
    },
    {
      "title": "Poster Design",
      "description": "Design stunning posters for any occasion",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Poster Design"
    },
    {
      "title": "Social Media",
      "description": "Complete social media design kits",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Social Media"
    }
  ]
}
```

#### `tool-grid`

**作用：** 工具卡 3 列网格（icon、标签、评分）

**适用场景：** Tools 页、Landing 的工具矩阵、Product 卡片网格

**字段结构：**
```json
{
  "type": "tool-grid",
  "tools": [
    {
      "name": "string",
      "description": "string",
      "icon": "string",
      "rating": 4.5,
      "url": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "tool-grid",
  "tools": [
    {
      "name": "Logo Maker",
      "description": "Create professional logos",
      "icon": "logo",
      "rating": 4.8,
      "url": "/tools/logo-maker"
    },
    {
      "name": "Poster Designer",
      "description": "Design stunning posters",
      "icon": "poster",
      "rating": 4.6,
      "url": "/tools/poster-designer"
    },
    {
      "name": "Social Media Kit",
      "description": "Complete social media designs",
      "icon": "social",
      "rating": 4.7,
      "url": "/tools/social-media-kit"
    }
  ]
}
```

#### `blog-grid`

**作用：** 博客/文章 3 列卡片

**适用场景：** 内容营销、案例文章聚合（Tools 内容簇方案 B）

**字段结构：**
```json
{
  "type": "blog-grid",
  "posts": [
    {
      "title": "string",
      "excerpt": "string",
      "image": "string",
      "alt": "string",
      "url": "string",
      "date": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "blog-grid",
  "posts": [
    {
      "title": "How to Create a Professional Logo",
      "excerpt": "Learn the step-by-step process...",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo Design Tutorial",
      "url": "/blog/how-to-create-logo",
      "date": "2026-05-15"
    },
    {
      "title": "Design Trends for 2026",
      "excerpt": "Discover the latest design trends...",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Design Trends",
      "url": "/blog/design-trends-2026",
      "date": "2026-05-10"
    }
  ]
}
```

#### `feature-detail`

**作用：** 多条图文左右交错

**适用场景：** 深度讲一个能力、Dynamic 动态说明段

**字段结构：**
```json
{
  "type": "feature-detail",
  "features": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string",
      "reverse": false
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "feature-detail",
  "features": [
    {
      "title": "AI-Powered Design",
      "description": "Our AI understands your design intent and creates professional results",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "AI Design",
      "reverse": false
    },
    {
      "title": "Professional Quality",
      "description": "Output meets professional standards for any use case",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Professional Quality",
      "reverse": true
    }
  ]
}
```

#### `canvas-wall`

**作用：** 10 卡 bento 画布墙（作者/likes）

**适用场景：** 作品墙、Gallery 展示段

**字段结构：**
```json
{
  "type": "canvas-wall",
  "items": [
    {
      "image": "string",
      "alt": "string",
      "author": "string",
      "likes": 100
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "canvas-wall",
  "items": [
    {
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo Design",
      "author": "John Doe",
      "likes": 150
    },
    {
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Poster Design",
      "author": "Jane Smith",
      "likes": 200
    }
  ]
}
```

### 2.4 Portrait / Showcase（4 变体）

#### `portrait-grid-3`

**作用：** 3 列 1:1 方卡

**适用场景：** 三类资产/三类场景

**字段结构：**
```json
{
  "type": "portrait-grid-3",
  "items": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "portrait-grid-3",
  "items": [
    {
      "title": "Business",
      "description": "Professional business designs",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Business Design"
    },
    {
      "title": "Creative",
      "description": "Artistic creative designs",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Creative Design"
    },
    {
      "title": "Social",
      "description": "Social media designs",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Social Design"
    }
  ]
}
```

#### `portrait-grid-4`

**作用：** 4 列 3:4 竖卡

**适用场景：** 四象限场景、四类产品形态

**字段结构：**
```json
{
  "type": "portrait-grid-4",
  "items": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "portrait-grid-4",
  "items": [
    {
      "title": "Logo",
      "description": "Professional logos",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo"
    },
    {
      "title": "Poster",
      "description": "Stunning posters",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Poster"
    },
    {
      "title": "Social",
      "description": "Social media",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Social"
    },
    {
      "title": "Brand",
      "description": "Brand identity",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Brand"
    }
  ]
}
```

#### `showcase-stacked`

**作用：** 垂直堆叠大图叙事

**适用场景：** 流程/前后阶段展示（Dynamic 段）

**字段结构：**
```json
{
  "type": "showcase-stacked",
  "items": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "showcase-stacked",
  "items": [
    {
      "title": "Step 1: Describe",
      "description": "Tell Lovart what you want to create",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Step 1"
    },
    {
      "title": "Step 2: Generate",
      "description": "AI creates multiple design options",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Step 2"
    },
    {
      "title": "Step 3: Refine",
      "description": "Perfect your design with AI assistance",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Step 3"
    }
  ]
}
```

#### `showcase-horizontal`

**作用：** 横向滚动大图叙事

**适用场景：** 多案例横滑浏览

**字段结构：**
```json
{
  "type": "showcase-horizontal",
  "items": [
    {
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "showcase-horizontal",
  "items": [
    {
      "title": "Logo Design",
      "description": "Professional logos",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Logo Design"
    },
    {
      "title": "Poster Design",
      "description": "Stunning posters",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Poster Design"
    },
    {
      "title": "Social Media",
      "description": "Social media kits",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Social Media"
    }
  ]
}
```

### 2.5 互动 / 跑马灯（3 变体）

#### `prompt-launcher`

**作用：** 居中输入框 + prompt 标签

**适用场景：** **Tools 专属**：让用户立刻试工具

**字段结构：**
```json
{
  "type": "prompt-launcher",
  "title": "string",
  "subtitle": "string",
  "placeholder": "string",
  "button_text": "string",
  "suggestions": ["string"]
}
```

**使用示例：**
```json
{
  "type": "prompt-launcher",
  "title": "Try Lovart Now",
  "subtitle": "Describe what you want to create",
  "placeholder": "e.g., A professional logo for a tech startup",
  "button_text": "Generate",
  "suggestions": ["Logo", "Poster", "Social Media"]
}
```

#### `logo-loop`

**作用：** 品牌 logo 循环条

**适用场景：** 社会证明、客户列表（Product Photo 段）

**字段结构：**
```json
{
  "type": "logo-loop",
  "logos": [
    {
      "name": "string",
      "logo": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "logo-loop",
  "logos": [
    {
      "name": "Company A",
      "logo": "https://cdn.lovart.ai/logos/company-a.png",
      "alt": "Company A"
    },
    {
      "name": "Company B",
      "logo": "https://cdn.lovart.ai/logos/company-b.png",
      "alt": "Company B"
    },
    {
      "name": "Company C",
      "logo": "https://cdn.lovart.ai/logos/company-c.png",
      "alt": "Company C"
    }
  ]
}
```

#### `media-marquee`

**作用：** 作品图横向跑马灯

**适用场景：** 视觉案例流、创意范围展示

**字段结构：**
```json
{
  "type": "media-marquee",
  "items": [
    {
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "media-marquee",
  "items": [
    {
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Design 1"
    },
    {
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Design 2"
    },
    {
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Design 3"
    }
  ]
}
```

### 2.6 CTA / 流程（3 变体）

#### `cta-default`

**作用：** 居中渐变 CTA 横幅 + 双按钮

**适用场景：** 页内中段转化或**底部收口**（同一组件，文案不同）

**字段结构：**
```json
{
  "type": "cta-default",
  "title": "string",
  "subtitle": "string",
  "primary_button": {
    "text": "string",
    "url": "string"
  },
  "secondary_button": {
    "text": "string",
    "url": "string"
  }
}
```

**使用示例：**
```json
{
  "type": "cta-default",
  "title": "Ready to Start?",
  "subtitle": "Join thousands of creators using Lovart",
  "primary_button": {
    "text": "Get Started Free",
    "url": "/signup"
  },
  "secondary_button": {
    "text": "View Pricing",
    "url": "/pricing"
  }
}
```

#### `workflow-horizontal`

**作用：** 横向简短 N 步

**适用场景：** 「3 步搞定」类 How-to

**字段结构：**
```json
{
  "type": "workflow-horizontal",
  "title": "string",
  "steps": [
    {
      "number": 1,
      "title": "string",
      "description": "string",
      "icon": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "workflow-horizontal",
  "title": "How It Works",
  "steps": [
    {
      "number": 1,
      "title": "Describe",
      "description": "Tell us what you want",
      "icon": "pencil"
    },
    {
      "number": 2,
      "title": "Generate",
      "description": "AI creates designs",
      "icon": "magic"
    },
    {
      "number": 3,
      "title": "Download",
      "description": "Get your design",
      "icon": "download"
    }
  ]
}
```

#### `workflow-vertical`

**作用：** 纵向带图 N 步

**适用场景：** 需要配图详解的步骤教程

**字段结构：**
```json
{
  "type": "workflow-vertical",
  "title": "string",
  "steps": [
    {
      "number": 1,
      "title": "string",
      "description": "string",
      "image": "string",
      "alt": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "workflow-vertical",
  "title": "Step-by-Step Guide",
  "steps": [
    {
      "number": 1,
      "title": "Describe Your Design",
      "description": "Tell Lovart what you want to create",
      "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
      "alt": "Step 1"
    },
    {
      "number": 2,
      "title": "AI Generates Options",
      "description": "AI creates multiple design options",
      "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
      "alt": "Step 2"
    },
    {
      "number": 3,
      "title": "Refine & Download",
      "description": "Perfect your design and download",
      "image": "https://cdn.lovart.ai/images/agents/da4b4705.png",
      "alt": "Step 3"
    }
  ]
}
```

### 2.7 对比（2 变体）

#### `comparison-table`

**作用：** 多列功能对比表

**适用场景：** Lovart vs 竞品 / 旧工作流

**字段结构：**
```json
{
  "type": "comparison-table",
  "title": "string",
  "headers": ["string"],
  "rows": [
    {
      "feature": "string",
      "values": ["string"]
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "comparison-table",
  "title": "Lovart vs Traditional Design",
  "headers": ["Feature", "Lovart", "Traditional"],
  "rows": [
    {
      "feature": "Time",
      "values": ["5 minutes", "2 hours"]
    },
    {
      "feature": "Cost",
      "values": ["$0", "$50+"]
    },
    {
      "feature": "Skill Required",
      "values": ["None", "Professional"]
    }
  ]
}
```

#### `comparison-before-after`

**作用：** 单图前后对比滑块

**适用场景：** 效果类工具、视觉改善证明

**字段结构：**
```json
{
  "type": "comparison-before-after",
  "title": "string",
  "before": {
    "image": "string",
    "alt": "string",
    "label": "string"
  },
  "after": {
    "image": "string",
    "alt": "string",
    "label": "string"
  }
}
```

**使用示例：**
```json
{
  "type": "comparison-before-after",
  "title": "See the Difference",
  "before": {
    "image": "https://cdn.lovart.ai/images/agents/8f3f2384.png",
    "alt": "Before",
    "label": "Before"
  },
  "after": {
    "image": "https://cdn.lovart.ai/images/agents/98800dc8.png",
    "alt": "After",
    "label": "After"
  }
}
```

### 2.8 证言 / 评价（3 变体）

#### `testimonial`

**作用：** 客户引言轮播/卡片

**适用场景：** 单条或多条引言，偏叙事

**字段结构：**
```json
{
  "type": "testimonial",
  "testimonials": [
    {
      "quote": "string",
      "author": "string",
      "role": "string",
      "company": "string",
      "avatar": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "testimonial",
  "testimonials": [
    {
      "quote": "Lovart transformed our design workflow",
      "author": "John Doe",
      "role": "Marketing Director",
      "company": "Tech Corp",
      "avatar": "https://cdn.lovart.ai/avatars/john.png"
    },
    {
      "quote": "Professional results in minutes",
      "author": "Jane Smith",
      "role": "Freelance Designer",
      "company": "Self-employed",
      "avatar": "https://cdn.lovart.ai/avatars/jane.png"
    }
  ]
}
```

#### `review-grid-3col`

**作用：** 3 列评价卡

**适用场景：** 中等数量用户故事

**字段结构：**
```json
{
  "type": "review-grid-3col",
  "reviews": [
    {
      "quote": "string",
      "author": "string",
      "role": "string",
      "rating": 5
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "review-grid-3col",
  "reviews": [
    {
      "quote": "Amazing tool!",
      "author": "John Doe",
      "role": "Designer",
      "rating": 5
    },
    {
      "quote": "Highly recommended",
      "author": "Jane Smith",
      "role": "Marketer",
      "rating": 5
    },
    {
      "quote": "Best design tool ever",
      "author": "Bob Johnson",
      "role": "Entrepreneur",
      "rating": 5
    }
  ]
}
```

#### `review-grid-4col`

**作用：** 4 列评价卡

**适用场景：** 更多评价、偏社交证明墙

**字段结构：**
```json
{
  "type": "review-grid-4col",
  "reviews": [
    {
      "quote": "string",
      "author": "string",
      "role": "string",
      "rating": 5
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "review-grid-4col",
  "reviews": [
    {
      "quote": "Amazing tool!",
      "author": "John Doe",
      "role": "Designer",
      "rating": 5
    },
    {
      "quote": "Highly recommended",
      "author": "Jane Smith",
      "role": "Marketer",
      "rating": 5
    },
    {
      "quote": "Best design tool ever",
      "author": "Bob Johnson",
      "role": "Entrepreneur",
      "rating": 5
    },
    {
      "quote": "Game changer!",
      "author": "Alice Brown",
      "role": "Content Creator",
      "rating": 5
    }
  ]
}
```

### 2.9 数据 / 信任 / 定价 / FAQ（4 变体）

#### `stats`

**作用：** 大数字 + 标签条

**适用场景：** 关键指标（当前六类主线**未纳入**，可扩展）

**字段结构：**
```json
{
  "type": "stats",
  "stats": [
    {
      "value": "string",
      "label": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "stats",
  "stats": [
    {
      "value": "1M+",
      "label": "Users"
    },
    {
      "value": "10M+",
      "label": "Designs Created"
    },
    {
      "value": "4.8",
      "label": "User Rating"
    }
  ]
}
```

#### `proof-block`

**作用：** 2×2 信任证据卡

**适用场景：** 四大理由/保障（当前六类主线**未纳入**，可扩展）

**字段结构：**
```json
{
  "type": "proof-block",
  "items": [
    {
      "title": "string",
      "description": "string",
      "icon": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "proof-block",
  "items": [
    {
      "title": "AI-Powered",
      "description": "Advanced AI understands your design intent",
      "icon": "magic"
    },
    {
      "title": "Professional Quality",
      "description": "Output meets professional standards",
      "icon": "star"
    },
    {
      "title": "Fast & Easy",
      "description": "Create designs in minutes",
      "icon": "lightning"
    },
    {
      "title": "Affordable",
      "description": "Professional results at low cost",
      "icon": "dollar"
    }
  ]
}
```

#### `pricing-block`

**作用：** 定价区（价格走后端）

**适用场景：** Features / Solution 收口前定价

**字段结构：**
```json
{
  "type": "pricing-block",
  "title": "string",
  "subtitle": "string",
  "plans": [
    {
      "name": "string",
      "price": "string",
      "period": "string",
      "features": ["string"],
      "button_text": "string",
      "button_url": "string",
      "popular": false
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "pricing-block",
  "title": "Simple Pricing",
  "subtitle": "Choose the plan that works for you",
  "plans": [
    {
      "name": "Free",
      "price": "$0",
      "period": "forever",
      "features": ["5 designs/day", "Basic quality", "Standard support"],
      "button_text": "Get Started",
      "button_url": "/signup",
      "popular": false
    },
    {
      "name": "Pro",
      "price": "$9.99",
      "period": "month",
      "features": ["Unlimited designs", "8K quality", "Priority support"],
      "button_text": "Upgrade to Pro",
      "button_url": "/upgrade",
      "popular": true
    }
  ]
}
```

#### `faq`

**作用：** 手风琴 FAQ

**适用场景：** 解答顾虑，SEO 长尾

**字段结构：**
```json
{
  "type": "faq",
  "title": "string",
  "faqs": [
    {
      "question": "string",
      "answer": "string"
    }
  ]
}
```

**使用示例：**
```json
{
  "type": "faq",
  "title": "Frequently Asked Questions",
  "faqs": [
    {
      "question": "What is Lovart?",
      "answer": "Lovart is an AI-powered design platform that helps you create professional designs in minutes."
    },
    {
      "question": "How does it work?",
      "answer": "Simply describe what you want to create, and our AI generates multiple design options for you to choose from."
    },
    {
      "question": "Is it free?",
      "answer": "Yes! Lovart offers a free plan with 5 designs per day. For more features, upgrade to Pro."
    }
  ]
}
```

---

## 三、JSON 模块最佳实践

### 3.1 模块选择建议

**首屏选择：**
- **功能/工具页**：使用 `hero-split`（信息密度适中）
- **品牌感强的页面**：使用 `hero-cinematic`（视觉主导）
- **多步骤流程**：使用 `hero-journey`（强调用户旅程）
- **多能力并列**：使用 `hero-mosaic`（不规则拼贴）
- **产品矩阵**：使用 `hero-gallery`（多工具入口）

**内容模块选择：**
- **核心能力速览**：使用 `bento-2/4/6` 或 `feature-grid`
- **多功能切换**：使用 `capability-tabs`
- **深度讲解**：使用 `feature-detail`
- **作品展示**：使用 `canvas-wall` 或 `showcase-*`

**转化模块选择：**
- **试用引导**：使用 `prompt-launcher`
- **社会证明**：使用 `testimonial` 或 `review-grid-*`
- **定价展示**：使用 `pricing-block`
- **常见问题**：使用 `faq`

### 3.2 模块组合建议

**Features 页面推荐组合：**
1. `hero-split` → 首屏
2. `cluster-block-dense` → 核心能力速览
3. `capability-tabs` → 多功能切换
4. `bento-2` → 重点能力深讲
5. `feature-detail` → 动态图文
6. `prompt-launcher` → 试用输入
7. `workflow-horizontal` → 步骤教程
8. `comparison-table` → 对比竞品
9. `cluster-block-dense` → 内容簇
10. `testimonial` → 证言
11. `pricing-block` → 定价
12. `faq` → FAQ
13. `cta-default` → 底部 CTA

**Tools 页面推荐组合：**
1. `hero-split` → 首屏
2. `prompt-launcher` → 试用输入
3. `bento-2` → 核心能力速览
4. `workflow-horizontal` → 步骤教程
5. `feature-detail` → 深度讲解
6. `comparison-table` → 对比竞品
7. `cluster-block-dense` → 内容簇
8. `canvas-wall` → 作品展示
9. `testimonial` → 证言
10. `logo-loop` → 客户 logo
11. `faq` → FAQ
12. `cta-default` → 底部 CTA

### 3.3 常见问题

**Q: 如何选择合适的 JSON 模块？**
A: 根据页面类型和内容特点选择。参考故事线文档中的推荐组合。

**Q: 如何修改 JSON 模块？**
A: 找到对应的 JSON 文件，修改 `type` 字段和内容结构。

**Q: 如何添加新模块？**
A: 在 `preview-data.json` 中添加示例，然后在页面中使用。

---

## 四、相关文档

- [STORYLINE-BY-DIRECTION.md](../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINE-BY-DIRECTION.md) - 权威故事线文档
- [FEATURES-PRODUCTION.md](../1-3 Content Gen/Page Gen/Refresh-Page/FEATURES-PRODUCTION.md) - Features 页面生产指南
- [STORYLINES.md](../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINES.md) - 情景×组件组合菜谱
- [For-Landing-Page-制作人.md](./For-Landing-Page-制作人.md) - Landing Page 制作人操作指南

---

> **维护者**：Lovart 团队  
> **最后更新**：2026-06-04  
> **版本**：V1.0
