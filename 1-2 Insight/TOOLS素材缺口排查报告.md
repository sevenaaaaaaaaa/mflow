# TOOLS 素材缺口排查报告

> **排查日期**: 2026-06-15
> **数据源**: Sanity CMS `o11tm2qe/production` · `_type == "compositePage"`
> **排查范围**: tool / feature / solution / product 四个分类

---

## 一、全站总览

| Category | 页面数 | bodyJson | 状态 |
|----------|--------|----------|------|
| **tool** | 917 | 917 (100%) | ⚠️ 42% 无图片 |
| **feature** | 2,222 | 2,222 (100%) | ✅ 99.9% 有图 |
| **solution** | 10 | 10 (100%) | ✅ 全部高质量 |
| **product** | 2 | 2 (100%) | ✅ 全部高质量 |
| scenario | 70 | 70 (100%) | 未排查 |
| topic | 48 | 48 (100%) | 未排查 |
| landing | 3 | 3 (100%) | 未排查 |

---

## 二、TOOLS 详细分析

### 2.1 分层概览

TOOLS 共 **443 个唯一 slug**（917 页含多语言变体），按素材状态分为三层：

```
┌─────────────────────────────────────────────────────────┐
│  TOOLS 443 slug / 917 页面                              │
├─────────────────────────────────────────────────────────┤
│  P0 骨架页:  339 slug (76%) ← 批量生成的空壳页          │
│  P1 框架页:   45 slug (10%) ← 结构完整但无图            │
│  有图页面:    59 slug (13%) ← 已上线，但同质化严重      │
└─────────────────────────────────────────────────────────┘
```

### 2.2 P0 骨架页 — 339 slug（核心缺口）

**症状**：批量生成的框架页，4-6 个 section，完全没有图片

**统一结构**：
```
hero-split (media.src = "")
  → feature-grid (features[n] 只有 title + description，无图片字段)
    → faq
      → cta-default
```

**根本原因**：这批页面按 SEO 批量生成，只搭了文字骨架，没有按生产标准注入素材和故事线。

**多语言覆盖**：391/443 slug 仅有英文 1 个语言版本，说明尚未进入本地化流程。

**涉及品类分布**（24 个品类）：

| 品类 | slug 数 | 代表页面 |
|------|---------|----------|
| video | 42 | ai-animation-generator, ai-cinematic-video, ai-video-editor |
| design-tool-generic | 38 | ai-design-platform, ai-creative-suite, ai-design-studio |
| usp-value | 31 | easy-ai-design, fast-ai-design-tool, free-ai-design-tool |
| ai-capability | 31 | ai-3d-texture, ai-consistent-character, ai-image-to-image |
| print-design | 29 | ai-poster-maker, ai-flyer-maker, ai-business-card-maker |
| platform-feature | 27 | ai-api-access, ai-batch-processing, ai-workflow-automation |
| social-media | 26 | ai-instagram-post, ai-tiktok-branding, ai-youtube-branding |
| marketing | 24 | ai-advertising-design, ai-banner-maker, ai-email-template |
| brand-identity | 22 | ai-logo-creator-free, ai-brand-kit, ai-brand-identity |
| platform-specific | 18 | ai-app-design, mobile-ai-design, browser-design-tool |
| photo-editing | 17 | ai-photo-editor, ai-background-blur, ai-face-retouch |
| product-ecommerce | 16 | ai-product-photo, ai-mockup-scene, ai-etsy-listing |
| content-creation | 15 | ai-meme-generator, ai-thumbnail-maker, ai-content-calendar |
| misc-creative | 13 | ai-baby-announcement, ai-pet-portrait, ai-wallpaper-generator |
| persona-audience | 14 | ai-design-for-marketers, ai-design-for-agencies |
| document | 13 | ai-ebook-maker, ai-whitepaper, ai-report-maker |
| alternative-comparison | 12 | kling-ai, sora-2, veo-3, alternative-to-figma |
| data-visualization | 9 | ai-infographic-creator, ai-flowchart, ai-mind-map |
| industry-vertical | 10 | ai-restaurant-branding, ai-fashion-design, ai-room-planner |
| education | 6 | ai-flashcard-maker, ai-worksheet-maker, ai-lesson-plan |
| presentation | 5 | ai-pitch-deck-maker, ai-presentation-maker |
| typography-design | 4 | ai-color-palette, ai-font-pairing |
| interior-space | 3 | ai-interior-design, ai-room-planner, ai-virtual-staging |
| other | 15 | ai-agent-platform, ai-company-profile 等 |

### 2.3 P1 框架页 — 45 slug（快速上线机会）

**症状**：结构已按生产标准搭建（7-10 section），但所有 media 字段为空

**典型结构**：
```
hero-split (media.src = "")
  → feature-grid (纯文字)
    → how-it-works-section
      → use-cases-section
        → comparison-section
          → pricing-section
            → faq
              → cta-default
```

**关键差异**：P1 比 P0 多了 `how-it-works`、`use-cases`、`comparison`、`pricing` 等生产级 section。**只需填充图片即可上线**。

**45 个 P1 slug 完整清单**：

| # | slug | sections |
|---|------|----------|
| 1 | ai-banner-creator | 7 |
| 2 | ai-birthday-card | 7 |
| 3 | ai-brand-kit | 8 |
| 4 | ai-brochure-maker | 8 |
| 5 | ai-business-card-maker | 7 |
| 6 | ai-certificate-maker | 8 |
| 7 | ai-clothing-mockup | 8 |
| 8 | ai-design-alternative | 7 |
| 9 | ai-design-for-creators | 8 |
| 10 | ai-ebook-cover-maker | 8 |
| 11 | ai-flyer-maker | 7 |
| 12 | ai-image-generator-free | 8 |
| 13 | ai-infographic-creator | 8 |
| 14 | ai-instagram-posts | 8 |
| 15 | ai-interior-design | 8 |
| 16 | ai-invitation-maker | 8 |
| 17 | ai-logo-design | 8 |
| 18 | ai-mockup-generator | 8 |
| 19 | ai-online-photo-editor | 8 |
| 20 | ai-pet-portrait | 7 |
| 21 | ai-photo-editor-online | 8 |
| 22 | ai-pitch-deck-maker | 8 |
| 23 | ai-poster-creator | 8 |
| 24 | ai-presentation-maker | 7 |
| 25 | ai-product-photography | 8 |
| 26 | ai-product-photography-free | 8 |
| 27 | ai-real-estate-flyer | 7 |
| 28 | ai-restaurant-menu | 8 |
| 29 | ai-resume-builder | 7 |
| 30 | ai-social-media-content | 8 |
| 31 | ai-stock-image-free | 8 |
| 32 | ai-stock-photo-creator | 8 |
| 33 | ai-t-shirt-design | 8 |
| 34 | ai-vector-generator | 8 |
| 35 | ai-video-generator-free | 8 |
| 36 | ai-vs-chatgpt-design | 7 |
| 37 | ai-wedding-invitation | 7 |
| 38 | ai-youtube-thumbnails | 8 |
| 39 | alternative-to-figma | 7 |
| 40 | better-than-ai-design | 7 |
| 41 | kling-ai | 7 |
| 42 | nano-banana | 7 |
| 43 | photo-to-cartoon-ai | 7 |
| 44 | sora-2 | 7 |
| 45 | veo-3 | 7 |

### 2.4 有图页面 — 59 slug（质量隐患）

**素材复用极度严重**：
- 仅 **71 个去重 URL** 支撑 59 个 slug（含多语言后 6,800+ 槽位）
- **34 个独占 URL** / **37 个共享 URL**
- 46/59 个 slug **零独占 URL** — 所有图片都与其他页面共享

**Section 覆盖率**：

| Section | 覆盖率 | 状态 |
|---------|--------|------|
| hero-split | 100% | ✅ |
| faq | 99% | ✅ |
| workflow-horizontal（故事线）| 93% | ✅ |
| comparison-table | 98% | ✅ |
| logo-loop | 98% | ✅ |
| prompt-launcher | 98% | ✅ |
| **testimonial（社会证明）** | **6%** | ❌ |
| **pricing** | **0.2%** | ❌ |
| how-it-works | 0% | ❌ |

---

## 三、FEATURES 分析

| 层级 | slug 数 | 说明 |
|------|---------|------|
| Full（完整故事线+互动+10+section）| 242 | ✅ 生产级 |
| New Template（centeredInputSection 精简模板）| ~194 | ⚠️ 不同设计方案 |
| 结构异常（bodyJson 为 dict）| 3 | ⚠️ 需修复 |

**URL 同质化**：
- 146 个去重 URL 支撑 2,222 页
- **2,191 页（98.6%）零独占 URL**
- 1 张图被 246 页同时使用

---

## 四、SOLUTIONS / PRODUCTS

**SOLUTIONS (10 slug)**：全部 12 section，story ≥ 2，engage = 1，51 个去重 URL。✅ 高质量无缺口。

**PRODUCTS (2 slug)**：brand-kit + chatcanvas，12-13 section，15 个去重 URL。✅ 高质量无缺口。

---

## 五、问题根因分析

### 5.1 P0 骨架页（339 slug）
**根因**：批量 SEO 页面生成时，只创建了文字骨架（hero + feature-grid + faq + cta），未按生产标准注入素材和故事线。feature-grid 的 features 项只有 `title + description`，没有 `media` 字段。

### 5.2 P1 框架页（45 slug）
**根因**：页面结构已按生产标准搭建（含 how-it-works、use-cases 等），但所有 media 字段留空。可能是在 CMS 中创建了结构但素材未到位。

### 5.3 有图页面同质化（59 slug）
**根因**：早期素材有限，同一批 URL 被大量复用。71 个去重 URL 覆盖 59 个 slug，导致视觉上千篇一律。

---

## 六、优先级排序

| 优先级 | 问题 | 影响面 | 工作量 | 建议动作 |
|--------|------|--------|--------|----------|
| **P0** | 339 个骨架页无内容无图片 | 76% tools 页面 | 大 | 注入素材 + 补充故事线 section |
| **P1** | 45 个框架页无图片 | 10% tools 页面 | 中 | 仅填充 hero 图即可上线 |
| **P2** | 57 个有图 slug 缺 testimonial | 社会证明缺失 | 小 | 补充 review/testimonial section |
| **P3** | 46 个有图 slug 零独占 URL | 视觉同质化 | 中 | 按品类替换差异化素材 |
| **P4** | Features 2,191 页零独占 URL | SEO 同质化风险 | 大 | 逐步替换为品类专属素材 |
| **P5** | Features 3 个结构异常页 | bodyJson 格式 | 小 | 修复为标准 array 格式 |

---

## 七、执行计划

### Phase 1：P1 框架页快速上线（45 slug × 10 语言 = 450+ 页）

**动作**：为 45 个 P1 slug 的 hero-split 填充图片
**素材需求**：45 张 hero 大图
**素材来源**：从 features 的 122 个独有 URL 中按品类匹配
**预期效果**：45 × 10 语言 = 450+ 页面从骨架升级为完整页面

### Phase 2：P0 高价值品类填充（124 slug）

覆盖 video (42) + social-media (26) + marketing (24) + brand-identity (22) + print-design (29) 五个品类

**动作**：
1. 为 hero-split 填充品类专属图片
2. 评估是否需要将 feature-grid 升级为 bento/capability-tabs（增加图片字段）
**素材需求**：~124 张 hero 图 + 可能的 feature 图

### Phase 3：P0 长尾品类覆盖（215 slug）

覆盖 design-tool / platform-feature / usp-value / ai-capability 等

**动作**：可用通用产品截图 + 界面截图批量覆盖
**素材需求**：~10 套通用素材模板

### Phase 4：有图页面质量提升

- 补充 testimonial section（57 slug）
- 替换共享 URL 为独占素材（46 slug）

---

## 八、素材缺口量化

| 维度 | 需求 | 可用 | 缺口 |
|------|------|------|------|
| hero 大图 | 384 张 | 7 个独占 URL + 122 features URL | ~255 张新图 |
| feature-grid 图 | P0 页面 feature-grid 无图片字段 | — | 需 schema 改造 |
| bento/capability 图 | P1 页面可选 | 25 + 27 个可用 URL | 可复用 |
| testimonial | 57 slug 需补充 | 0 | 57 组评价文案+头像 |

---

## 九、交付物清单

| 文件 | 路径 | 用途 |
|------|------|------|
| 审计原始数据 | `tools_asset_gap_audit.json` | P0/P1/有图三级分类详情 |
| 品类标签清单 | `tools_P0_P1_categorized.json` | 384 slug 带品类+section 详情 |
| 执行清单 CSV | `tools_P0_P1_execution_list.csv` | 可导入表格的执行列表 |
| 素材匹配计划 | `tools_asset_matching_plan.json` | 24 品类 × 素材需求 |
| 现有素材池 | `tools_asset_pool.json` | 49 个可用 URL 按 section 分组 |

> 所有文件位于 `~/Documents/Lovart Local Dev/`
