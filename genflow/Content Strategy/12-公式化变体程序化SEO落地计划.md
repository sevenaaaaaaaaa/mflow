# 公式化变体落地计划：程序化 SEO 生成方案

> ~1050 条变体归为 4 种模板类型，通过模板+数据集批量生成落地页
> 先产 20 篇验证模板，再按优先级分批扩展

---

## 一、四种模板类型

| 模板 | 覆盖条目 | 页面类型 | 搜索意图 |
|------|---------|---------|---------|
| **T1: Best Agent for [Niche]** | ~320 条 | Segment Landing Page | "best ai design tool for [my business]" |
| **T2: Chat-Generate [Design Type]** | ~30 条 | How-To Detail Page | "how to make [design type] with ai" |
| **T3: Step-by-Step [Design Type] No Photoshop** | ~25 条 | Tutorial Detail Page | "create [design type] without photoshop" |
| **T4: Brand Kit for [Niche]** | ~100 条 | Best Practice Detail Page | "brand kit setup for [my industry]" |

---

## 二、模板设计

### T1: Best AI Design Agent for [Niche]

```markdown
---
title: "Best AI Design Agent for [Niche] — [Value Proposition]"
page_type: Segment Landing Page
keywords: [niche_kw_1], [niche_kw_2], ai design for [niche]
---

## Hero
[Niche] owners spend [X hours/week] on design. Lovart makes it [Y minutes].

## Why [Niche] Needs Different Design Tools
[2 paragraphs on niche-specific visual challenges]

## 3 Ways [Niche] Uses Lovart
1. **[Use Case 1]** — [specific scenario with niche context]
2. **[Use Case 2]** — [specific scenario with niche context]
3. **[Use Case 3]** — [specific scenario with niche context]

## Before & After
[描述该行业的改造前后对比]

## Templates Made for [Niche]
- [Template 1] — [use case]
- [Template 2] — [use case]

## Pricing
[Standard pricing table]

## FAQ
- Can I really design for [niche] without experience?
- What if my [niche] has specific brand requirements?
- [3 more niche-specific Q&A]

CTA: Start designing for your [niche] — free
```

**数据集字段**：
- niche_name (e.g., "Cafe Owner")
- niche_slug (e.g., "cafe-owner")
- hours_spent (e.g., "5-8")
- minutes_saved (e.g., "15")
- pain_1, pain_2, pain_3 (行业痛点)
- use_case_1, use_case_2, use_case_3 (场景)
- color_palette_suggestion
- template_1, template_2
- faq_questions (3 niche-specific)

### T2: How to Chat-Generate [Design Type] with Lovart

```markdown
---
title: "How to Chat-Generate [Design Type] — Lovart Agent Workflow"
page_type: How-To Detail Page
keywords: chat to generate [design_type], ai [design_type] generator
---

## 用对话生成[Design Type]，不需要设计技能

## Step 1: Tell Lovart What You Need
> "[Prompt Template]"

## Step 2: Review & Refine
[该设计类型的常见修改需求]

## Step 3: Export for [Platform/Use]
[该设计类型的导出格式和尺寸]

## Variations You Can Try
[2-3 prompt variations for different styles]

## FAQ
- How is this different from using Canva templates?
- Can I add my own photos?
- [3 more]

CTA: Chat-generate your first [design type] — free
```

**数据集字段**：design_type, prompt_template, platform, export_format, variations, common_refinements

### T3: Step-by-Step [Design Type] Without Photoshop

```markdown
---
title: "A Step-by-Step Guide to Create [Design Type] Without Photoshop"
page_type: Tutorial Detail Page
keywords: create [design_type] without photoshop, ai [design_type] tutorial
---

## Create [Design Type] in [X] Minutes — Zero Photoshop

## What You'll Need
- [工具前提]

## Step-by-Step
### Step 1: [action]
### Step 2: [action]
### Step 3: [action]
### Step 4: [action]
### Step 5: Export as [format]

## Photoshop vs Lovart for [Design Type]
| Task | Photoshop | Lovart |
|------|----------|--------|
| [task 1] | [time/cost] | [time/cost] |
| [task 2] | [time/cost] | [time/cost] |

## FAQ
CTA: Create your first [design type] — free
```

### T4: Brand Kit for [Niche]

```markdown
---
title: "How to Create a Brand Kit Instantly for [Niche] — Lovart Guide"
page_type: Best Practice Detail Page
keywords: brand kit for [niche], [niche] branding ai
---

## Set up your [niche] brand in 5 minutes

## Recommended Color Palette for [Niche]
[为什么这个色板适合该行业]

## Font Pairing for [Niche]
[字体推荐]

## 3 Templates to Start
1. [Template]
2. [Template]
3. [Template]

## FAQ
CTA: Set up your [niche] Brand Kit — free
```

---

## 三、数据集构建

### 优先级 P0：高搜索量 + 高转化（20 个 niche）

| 行业 | Niche | 搜索量预估 |
|------|-------|-----------|
| 餐饮 | Cafe Owner, Restaurant Owner, Bakery Owner, Coffee Shop Owner | 中-高 |
| 美容 | Beauty Salon Owner, Hair Salon Owner, Nail Studio, Makeup Studio | 中-高 |
| 健身 | Gym Owner, Personal Trainer, Yoga Studio | 中 |
| 电商 | E-commerce Seller, Shopify Merchant, Amazon Seller, DTC Founder | 高 |
| 房地产 | Real Estate Agent, Realtor | 中-高 |
| 创作者 | Content Creator, YouTuber, Influencer, Podcaster | 高 |

### 优先级 P1：中搜索量（40 个 niche）

扩展覆盖：Day Spa, Pilates Studio, Boutique Owner, Florists, Bookstores, Dropshippers, Handmade Sellers, Digital Agency, Social Media Manager, Consultant, Coach, Insurance Agent, Life Coach, Financial Advisor, Solopreneur, Freelancer, Course Creator, Digital Nomad, Indie Brand Owner, Side Hustler...

### 优先级 P2：长尾覆盖（其余 niche）

按需生成，每月扩充 10-20 个

---

## 四、执行计划

| 阶段 | 产出 | 数量 |
|------|------|------|
| **Phase 1: Template Validation** | 用 4 个模板各生成 5 篇（共 20 篇）验证模板效果 | 20 篇 |
| **Phase 2: P0 扩展** | 覆盖 20 个高价值 niche × 4 模板 = 80 篇 | 80 篇 |
| **Phase 3: P1 扩展** | 覆盖 40 个中价值 niche × 主要模板 = ~60 篇 | 60 篇 |
| **Phase 4: 持续维护** | 每月补充新 niche + 更新已有页面 | 持续 |

---

## 五、现在开始 Phase 1

先产 20 篇验证模板。四种模板各选 5 个代表性 niche。
