# For Landing Page 制作人

> **文档定位**：面向落地页制作人员的操作指南  
> **更新日期**：2026-06-07  
> **适用范围**：Lovart 项目所有落地页制作相关人员

---

## 一、概述

本文档为 Landing Page 制作人提供完整的操作指南，涵盖页面类型、故事线选择、JSON 模块使用、制作流程等核心内容。

### 1.1 六大页面类型

| 页面类型 | URL 路径 | Sanity `category` | 故事线 | section 数 | 页面定位 |
|----------|----------|-------------------|--------|------------|----------|
| **Features** | `/features/{slug}` | `feature` | 4 条 | 13 | 单功能/能力介绍，讲清价值 → 试用 → 证言/定价 → 转化 |
| **Tools** | `/tools/{slug}` | `tool` | 6 条 | 12～13 | 工具页，强调试用、步骤、案例内容 |
| **Product** | `/product/{slug}` | `product` | 4 条 | 12～13 | 产品线总览，偏 Tab + 网格，含证言、定价、FAQ、底部 CTA |
| **Scenarios** | `/scenarios/{slug}` | `scenario` | 2 条 | 11 | 行业/场景叙事，Tab 有两种布局方案 |
| **Solution** | `/solution/{slug}` | `solution` | 1 条 | 12 | 方案包售卖，模块最全之一 |
| **Landing Page** | `/topic/{slug}`（待定） | `topic` 等 | **7 条**（6 投放 + 1 demo） | **12～15** | 投放向落地页，按意图选型；`landing-full` 仅 QA |

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

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `hero-split` | 左文右图，tag + 双行标题 + 按钮 + 4:3 大图 | 功能/工具页默认首屏，信息密度适中 |
| `hero-cinematic` | 居中标题 + 全宽剧院大图 | 品牌感强、视觉主导的 Product / Landing |
| `hero-journey` | 居中标题 + 横向 step 卡片条 | 强调「用户旅程 / 多步骤路径」 |
| `hero-mosaic` | 居中标题 + 不规则拼贴瓦片 | 多能力并列、修复/组合类叙事 |
| `hero-gallery` | 居中标题 + 6 宫格工具入口 | 产品矩阵、多工具入口总览 |

### 2.2 网格 / Bento / 信息簇（5 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `bento-2` | 两栏等大特性卡 | 两个核心卖点并列 |
| `bento-4` | 2×2 不规则四宫格 | 四个能力点，视觉有主次 |
| `bento-6` | 六卡 bento 布局 | 六个能力/场景，信息量大 |
| `feature-grid` | 2/3/4 列对称特性网格 | 均匀罗列功能点（`preview-data` 暂无示例，见 README） |
| `cluster-block-dense` | 3 列 icon 小卡墙 | 痛点列表、能力清单、内容簇 |

### 2.3 Tab / 矩阵 / 博客 / 图文（5 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `capability-tabs` | 左 Tab 列表 + 右大图内容区 | 多功能切换讲解（Features / Solution / Scenarios 核心模块） |
| `tool-grid` | 工具卡 3 列网格（icon、标签、评分） | Tools 页、Landing 的工具矩阵、Product 卡片网格 |
| `blog-grid` | 博客/文章 3 列卡片 | 内容营销、案例文章聚合（Tools 内容簇方案 B） |
| `feature-detail` | 多条图文左右交错 | 深度讲一个能力、Dynamic 动态说明段 |
| `canvas-wall` | 10 卡 bento 画布墙（作者/likes） | 作品墙、Gallery 展示段 |

### 2.4 Portrait / Showcase（4 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `portrait-grid-3` | 3 列 1:1 方卡 | 三类资产/三类场景 |
| `portrait-grid-4` | 4 列 3:4 竖卡 | 四象限场景、四类产品形态 |
| `showcase-stacked` | 垂直堆叠大图叙事 | 流程/前后阶段展示（Dynamic 段） |
| `showcase-horizontal` | 横向滚动大图叙事 | 多案例横滑浏览 |

### 2.5 互动 / 跑马灯（3 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `prompt-launcher` | 居中输入框 + prompt 标签 | **Tools 专属**：让用户立刻试工具 |
| `logo-loop` | 品牌 logo 循环条 | 社会证明、客户列表（Product Photo 段） |
| `media-marquee` | 作品图横向跑马灯 | 视觉案例流、创意范围展示 |

### 2.6 CTA / 流程（3 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `cta-default` | 居中渐变 CTA 横幅 + 双按钮 | 页内中段转化或**底部收口**（同一组件，文案不同） |
| `workflow-horizontal` | 横向简短 N 步 | 「3 步搞定」类 How-to |
| `workflow-vertical` | 纵向带图 N 步 | 需要配图详解的步骤教程 |

### 2.7 对比（2 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `comparison-table` | 多列功能对比表 | Lovart vs 竞品 / 旧工作流 |
| `comparison-before-after` | 单图前后对比滑块 | 效果类工具、视觉改善证明 |

### 2.8 证言 / 评价（3 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `testimonial` | 客户引言轮播/卡片 | 单条或多条引言，偏叙事 |
| `review-grid-3col` | 3 列评价卡 | 中等数量用户故事 |
| `review-grid-4col` | 4 列评价卡 | 更多评价、偏社交证明墙 |

### 2.9 数据 / 信任 / 定价 / FAQ（4 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `stats` | 大数字 + 标签条 | 关键指标（当前六类主线**未纳入**，可扩展） |
| `proof-block` | 2×2 信任证据卡 | 四大理由/保障（当前六类主线**未纳入**，可扩展） |
| `pricing-block` | 定价区（价格走后端） | Features / Solution 收口前定价 |
| `faq` | 手风琴 FAQ | 解答顾虑，SEO 长尾 |

---

## 三、十七种页面本体 → JSON 映射

**本体** = 六类页面编排用的 section 职责名。每个本体下列出**常用 JSON 模块**（择一上线）。

| # | 本体 | 一句话作用 | 常用 JSON `type` | 变体数 |
|---|------|------------|------------------|--------|
| 1 | **首屏** | 3 秒讲清是谁、解决什么、主按钮 | `hero-split` · `hero-cinematic` · `hero-journey` · `hero-mosaic` · `hero-gallery` | 5 |
| 2 | **多栏特性区** | 首屏下第一层：多个卖点/能力并列 | `bento-2/4/6` · `feature-grid` · `cluster-block-dense` · `portrait-grid-*` | 5～7 |
| 3 | **能力 Tab** | 多能力切换深讲 | `capability-tabs` | 1 |
| 4 | **卡片网格** | 工具/产品卡片矩阵 | `tool-grid` · `bento-4/6` | 2～3 |
| 5 | **特性大卡** | 少量重点能力大图讲解 | `bento-2/4` · `feature-detail` | 2～3 |
| 6 | **图库展示** | 作品墙、视觉案例聚合 | `canvas-wall` · `showcase-*` · `hero-gallery` | 3～4 |
| 7 | **试用输入** | 让用户立刻输入 prompt 试用 | `prompt-launcher` | 1 |
| 8 | **Logo / 滚动条** | 客户 logo 或案例图流动展示 | `logo-loop` · `media-marquee` | 2 |
| 9 | **页内 CTA** | 页面中段一次转化拦截 | `cta-default` | 1 |
| 10 | **步骤教程** | 怎么用、几步完成 | `workflow-horizontal` · `workflow-vertical` | 2 |
| 11 | **对比** | 和替代方案比差异 | `comparison-table` · `comparison-before-after` | 2 |
| 12 | **内容簇** | 案例/文章/能力密集聚合 | `cluster-block-dense` · `blog-grid` | 2 |
| 13 | **动态图文** | 深度展开某一主题、多段叙事 | `feature-detail` · `showcase-stacked` · `showcase-horizontal` | 3 |
| 14 | **证言** | 客户怎么说 | `testimonial` · `review-grid-3col` · `review-grid-4col` | 3 |
| 15 | **定价** | 套餐与购买 | `pricing-block` | 1 |
| 16 | **FAQ** | 常见问题 | `faq` | 1 |
| 17 | **底部 CTA** | 页面最后收口转化 | `cta-default` | 1 |

> **页内 CTA** 与 **底部 CTA** 同为 `cta-default`，靠文案与位置区分。

---

## 四、分页面类型：本体清单与推荐 JSON

表头：**序** = 页内从上到下；**故事线** 列只在有分叉时出现。

### 4.1 Features（4 条故事线 · 13 个本体）

**叙事：** 价值主张 → 能力概览 → Tab 深讲 → 特性展开 → 深度说明 → 立刻试用 → 怎么用 → 对比竞品 → 内容补充 → 客户证言 → 定价 → FAQ → 转化。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 在本页的用途 |
|----|------|---------------------|----------|--------------|
| 1 | 首屏 | `hero-split` | 5 种 hero-* | 功能名 + 核心价值 + 主 CTA |
| 2 | 多栏特性区（网格位） | `cluster-block-dense` 或 `bento-4` | `bento-2/4/6`、`feature-grid`、`cluster-block-dense` | 3～6 个能力点速览 |
| 3 | 能力 Tab | `capability-tabs`（布局 A） | `capability-tabs`（布局 B） | 多功能切换详解（两种布局） |
| 4 | 特性大卡 | `bento-2` 或 `feature-detail` | bento-*, feature-detail | 2～4 个重点能力深讲 |
| 5 | 动态图文 | `feature-detail` | showcase-* | 某一能力的长图文说明 |
| 6 | 试用输入 | `prompt-launcher` | — | 让用户直接输入需求试用 |
| 7 | 步骤教程 | `workflow-horizontal` | workflow-vertical | 「几步上手此功能」 |
| 8 | 对比 | `comparison-table` | comparison-before-after | vs 通用 AI / 手工流程 |
| 9 | 内容簇 | `cluster-block-dense` | blog-grid | 相关场景/痛点聚合 |
| 10 | 证言 | `testimonial` | review-grid-* | 1～3 条客户引言 |
| 11 | 定价 | `pricing-block` | — | 套餐选择 |
| 12 | FAQ | `faq` | — | 功能相关问答 |
| 13 | 底部 CTA | `cta-default` | — | 注册 / 开始试用 |

**本类不用的本体（4）：** 卡片网格、图库展示、Logo 滚动条、页内 CTA

**Features 故事线（每个变体单独计线）：**

| 故事线 ID | 相对 `features-主线` 的变更 | 说明 |
|-----------|-------------------------------|------|
| `features-主线` | — | 基准线 |
| `features-tab-B` | 序 3（能力 Tab）改为布局 B | Tab 变体单独成线 |
| `features-grid-feature` | 序 2（网格位）改为 `feature-grid` | 网格变体单独成线 |
| `features-grid-bento6` | 序 2（网格位）改为 `bento-6` | 网格变体单独成线 |

**Features 全量故事线（逐条完整呈现）：**

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `features-主线` | `hero-split → cluster-block-dense → capability-tabs(布局A) → bento-2 → feature-detail → prompt-launcher → workflow-horizontal → comparison-table → cluster-block-dense → testimonial → pricing-block → faq → cta-default` |
| `features-tab-B` | `hero-split → cluster-block-dense → capability-tabs(布局B) → bento-2 → feature-detail → prompt-launcher → workflow-horizontal → comparison-table → cluster-block-dense → testimonial → pricing-block → faq → cta-default` |
| `features-grid-feature` | `hero-split → feature-grid → capability-tabs(布局A) → bento-2 → feature-detail → prompt-launcher → workflow-horizontal → comparison-table → cluster-block-dense → testimonial → pricing-block → faq → cta-default` |
| `features-grid-bento6` | `hero-split → bento-6 → capability-tabs(布局A) → bento-2 → feature-detail → prompt-launcher → workflow-horizontal → comparison-table → cluster-block-dense → testimonial → pricing-block → faq → cta-default` |

### 4.2 Tools（6 条故事线 · 12～13 个本体）

**叙事：** 立刻试用 → 核心能力 → 怎么用 → 深度讲解 → 内容补充 → 社会证明 → FAQ → 转化。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 在本页的用途 |
|----|------|---------------------|----------|--------------|
| 1 | 首屏 | `hero-split` | 5 种 hero-* | 工具名 + 核心价值 + 主 CTA |
| 2 | 试用输入 | `prompt-launcher` | — | 让用户立刻试工具 |
| 3 | 多栏特性区 | `bento-2` | bento-4/6, feature-grid | 核心能力速览 |
| 4 | 步骤教程 | `workflow-horizontal` | workflow-vertical | 「几步搞定」 |
| 5 | 特性大卡 | `feature-detail` | bento-2/4 | 深度讲解重点能力 |
| 6 | 对比 | `comparison-table` | comparison-before-after | vs 竞品/旧方案 |
| 7 | 内容簇 | `cluster-block-dense` | blog-grid | 相关场景/案例 |
| 8 | 图库展示 | `canvas-wall` | showcase-* | 作品展示 |
| 9 | 证言 | `testimonial` | review-grid-* | 用户评价 |
| 10 | Logo 滚动条 | `logo-loop` | media-marquee | 客户 logo |
| 11 | FAQ | `faq` | — | 常见问题 |
| 12 | 底部 CTA | `cta-default` | — | 注册/开始使用 |

**Tools 故事线：**

| 故事线 ID | 变更说明 |
|-----------|----------|
| `tools-主线` | 基准线 |
| `tools-对比` | 序 6 改为 `comparison-before-after` |
| `tools-图库` | 序 8 改为 `showcase-horizontal` |
| `tools-内容B` | 序 7 改为 `blog-grid` |
| `tools-无对比` | 移除序 6（对比） |
| `tools-精简` | 移除序 8（图库）+ 序 9（证言） |

### 4.3 Product（4 条故事线 · 12～13 个本体）

**叙事：** 产品概览 → 核心能力 → 深度讲解 → 社会证明 → 定价 → FAQ → 转化。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 在本页的用途 |
|----|------|---------------------|----------|--------------|
| 1 | 首屏 | `hero-split` | hero-cinematic, hero-gallery | 产品名 + 核心价值 |
| 2 | 多栏特性区 | `bento-4` | bento-2/6, feature-grid | 核心能力速览 |
| 3 | 能力 Tab | `capability-tabs` | — | 多功能切换详解 |
| 4 | 特性大卡 | `feature-detail` | bento-2/4 | 深度讲解重点能力 |
| 5 | 图库展示 | `canvas-wall` | showcase-* | 作品展示 |
| 6 | Logo 滚动条 | `logo-loop` | media-marquee | 客户 logo |
| 7 | 证言 | `testimonial` | review-grid-* | 用户评价 |
| 8 | 定价 | `pricing-block` | — | 套餐选择 |
| 9 | FAQ | `faq` | — | 常见问题 |
| 10 | 底部 CTA | `cta-default` | — | 注册/开始使用 |

**Product 故事线：**

| 故事线 ID | 变更说明 |
|-----------|----------|
| `product-主线` | 基准线 |
| `product-影院` | 序 1 改为 `hero-cinematic` |
| `product-画廊` | 序 1 改为 `hero-gallery` |
| `product-无定价` | 移除序 8（定价） |

### 4.4 Scenarios（2 条故事线 · 11 个本体）

**叙事：** 场景概览 → 核心能力 → 深度讲解 → 案例展示 → 社会证明 → FAQ → 转化。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 在本页的用途 |
|----|------|---------------------|----------|--------------|
| 1 | 首屏 | `hero-journey` | hero-split | 场景名 + 核心价值 |
| 2 | 多栏特性区 | `portrait-grid-3` | portrait-grid-4 | 场景分类 |
| 3 | 能力 Tab | `capability-tabs` | — | 多能力切换详解 |
| 4 | 特性大卡 | `feature-detail` | bento-2/4 | 深度讲解重点能力 |
| 5 | 图库展示 | `showcase-stacked` | showcase-horizontal | 案例展示 |
| 6 | 证言 | `review-grid-3col` | testimonial | 用户评价 |
| 7 | FAQ | `faq` | — | 常见问题 |
| 8 | 底部 CTA | `cta-default` | — | 注册/开始使用 |

**Scenarios 故事线：**

| 故事线 ID | 变更说明 |
|-----------|----------|
| `scenarios-主线` | 基准线 |
| `scenarios-横向` | 序 5 改为 `showcase-horizontal` |

### 4.5 Solution（1 条故事线 · 12 个本体）

**叙事：** 方案概览 → 核心能力 → 深度讲解 → 社会证明 → 定价 → FAQ → 转化。

| 序 | 本体 | JSON `type` | 在本页的用途 |
|----|------|-------------|--------------|
| 1 | 首屏 | `hero-cinematic` | 方案名 + 核心价值 |
| 2 | 多栏特性区 | `proof-block` | 四大理由/保障 |
| 3 | 对比 | `comparison-table` | vs 竞品/旧方案 |
| 4 | 步骤教程 | `workflow-vertical` | 怎么用 |
| 5 | 证言 | `review-grid-3col` | 用户评价 |
| 6 | 底部 CTA | `cta-default` | 注册/购买 |

### 4.6 Landing Page（6 条投放故事线 + 1 条满配 demo · 12～15 段）

**定位：** 面向**投放人员**的落地页类型。投放线各 **12 段**；满配 demo **15 段**（非投放）。

**叙事：** 按投放意图选型 → 核心能力 → 社会证明/对比 → FAQ → 转化。

机器可读 SSOT：[`landing-storylines.json`](../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/landing-storylines.json)  
制作指南：[LANDING-PRODUCTION-2026-06-07.md](../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/LANDING-PRODUCTION-2026-06-07.md)  
参考 JSON：[`landing-examples/en/`](../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/landing-examples/en/)

#### 投放故事线（6 条）

| 故事线 ID | 投放意图 | 关键模块差异 |
|-----------|----------|--------------|
| `landing-gallery-detail` | 广泛认知 / 多工具 | `hero-gallery` + `feature-detail` |
| `landing-gallery-funnel` | 漏斗教育 / 再营销 | `hero-gallery` + `showcase-horizontal` |
| `landing-brand-trust` | 品牌 upper funnel | `hero-cinematic` + `logo-loop` + `testimonial` |
| `landing-trial-now` | Search 试用转化 | `hero-split` + `prompt-launcher` |
| `landing-vs-competitor` | 竞品 / alternative | `comparison-before-after` |
| `landing-offer-close` | 促销 / 再营销收口 | `hero-journey` + `pricing-block` + `review-grid-3col` |

#### 满配 demo（1 条）

| 故事线 ID | 说明 |
|-----------|------|
| `landing-full` | 15 段，含试用/Logo/证言/定价 — **仅供 QA，勿投放** |

**别名：** `landing-A` → `landing-gallery-detail`；`landing-B` → `landing-gallery-funnel`

#### 自动分配信号

| 信号 | 故事线 |
|------|--------|
| 竞品 / vs / alternative | `landing-vs-competitor` |
| 试用 / try now / 工具 Search | `landing-trial-now` |
| 品牌曝光 / upper funnel | `landing-brand-trust` |
| 促销 / retarget / pricing | `landing-offer-close` |
| 漏斗阶段叙事 | `landing-gallery-funnel` |
| 内部 demo / 模块验收 | `landing-full` |
| 默认 / 多工具 gallery | `landing-gallery-detail` |

完整 type 顺序见 [`landing-storylines.json`](../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/landing-storylines.json) 或 STORYLINE-BY-DIRECTION §4.6.4。

---

## 五、页面制作流程

### 5.1 Features 页面制作流程

**做法 A：内容重排（推荐）**

把线上现存英文 Features 页（legacy 五段式）重排成新的 13 段故事线，复用原文案/图片，缺口派生或占位。全程本地，不触线上。

**流水线：**

在 `1-4 Dev/lovart.sanity.studio/` 下（输出落在工作区内，避免沙箱写 `~/lovart`）：

```bash
# _pull 已外置到运行层，通过 LOVART_PULL_DIR 环境变量引用
source "$(cd ../.. && pwd)/1-Project/Lovart MFlow/1-4 Dev/automation/local-dev-env.sh"
PULL="$LOVART_PULL_DIR"

# 1) 只读拉取线上全量英文 Features 页（含 bodyJson + seo）
LOVART_PULL_DIR="$PULL" node scripts/export-feature-pages.js --lang en

# 2) 全量重排为新 13 段故事线（本地草稿，noIndex，不导入）
LOVART_PULL_DIR="$PULL" node scripts/reflow-feature-pages.js
#   --limit 5            只跑前 5 篇
#   --slug ai-logo-maker 只跑某页
#   --storyline features-main  强制统一故事线
```

- 输入：`$LOVART_PULL_DIR/composite/features-full/*.json`
- 输出：`$LOVART_PULL_DIR/features-reflow/Features/en/<slug>-en.json` + `_manifest.json` + `_report.md`

> ⚠️ `_pull/` 已从 `1-3 GenFlow/Page Gen/Pages/drafts/` 迁移到 `~/Documents/Lovart Local Dev/Output/Page Gen/_pull/`。
> 所有脚本通过 `LOVART_PULL_DIR` 环境变量读取，默认值由 `local-dev-env.sh` 提供。

### 5.2 故事线分配（按页内容自动判定）

| 信号 | 选用故事线 |
|------|------------|
| 特性网格 ≥ 6 项 | `features-grid-bento6`（225 页） |
| 特性网格 3–5 项 | `features-grid-feature`（2 页） |
| 其它 | `features-main`（2 页） |

> `features-tab-b` 为纯布局变体，无内容信号，不自动分配；需要时用 `--storyline features-tab-b` 或逐页指定。

### 5.3 复用 vs 占位（13 段）

平均复用率约 **38%（5/13）**，复用的是真实 legacy 内容：

| 段 | 复用来源 | 占位逻辑 |
|----|----------|----------|
| 1. 首屏 | legacy hero | — |
| 2. 多栏特性区 | legacy featureGridSection | 派生自 legacy 3～6 项 |
| 3. 能力 Tab | legacy threeColumnSection | 派生自 legacy 3 列 |
| 4. 特性大卡 | — | 占位 |
| 5. 动态图文 | — | 占位 |
| 6. 试用输入 | legacy centeredInputSection | — |
| 7. 步骤教程 | — | 占位 |
| 8. 对比 | — | 占位 |
| 9. 内容簇 | — | 占位 |
| 10. 证言 | legacy testimonialSection | — |
| 11. 定价 | — | 占位 |
| 12. FAQ | legacy faqSection | — |
| 13. 底部 CTA | — | 占位 |

---

## 六、常见问题

### 6.1 如何选择故事线？

1. **确定页面类型**：根据 URL 路径和 Sanity category 确定是 Features、Tools、Product、Scenarios、Solution 还是 Landing Page
2. **分析内容特点**：根据页面内容特点选择对应的故事线
3. **参考信号**：如 Features 页面根据特性网格数量选择故事线

### 6.2 如何修改 JSON 模块？

1. **找到对应文件**：在 `$LOVART_PULL_DIR/features-reflow/` 目录下找到对应的 JSON 文件
2. **修改 type 字段**：将 `type` 字段修改为需要的 JSON 模块类型
3. **调整内容结构**：根据新模块的要求调整内容结构
4. **预览效果**：使用预览工具查看效果

### 6.3 如何添加新页面？

1. **确定页面类型**：根据页面内容确定使用哪种页面类型
2. **选择故事线**：从对应页面类型的故事线中选择合适的一个
3. **创建 JSON 文件**：基于故事线创建 JSON 文件
4. **填充内容**：填充实际内容
5. **导入 Sanity**：使用导入脚本将内容导入 Sanity

---

## 七、相关文档

- [STORYLINE-BY-DIRECTION.md](../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINE-BY-DIRECTION.md) - 权威故事线文档
- [LANDING-PRODUCTION-2026-06-07.md](../1-3 Content Gen/Page Gen/Refresh-Page/LANDING-PRODUCTION-2026-06-07.md) - Landing Page 7 条故事线生产指南
- [landing-storylines.json](../1-3 Content Gen/Page Gen/Refresh-Page/landing-storylines.json) - Landing Page 故事线 SSOT
- [landing-examples/MANIFEST.md](../1-3 Content Gen/Page Gen/Refresh-Page/landing-examples/MANIFEST.md) - 7 个参考案例清单
- [FEATURES-PRODUCTION.md](../1-3 Content Gen/Page Gen/Refresh-Page/FEATURES-PRODUCTION.md) - Features 页面生产指南
- [STORYLINES.md](../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINES.md) - 情景×组件组合菜谱
- [AGENTS.md](./AGENTS.md) - 项目规则和标准
- [WORKFLOWS.md](./WORKFLOWS.md) - 运维手册

---

> **维护者**：Lovart 团队  
> **最后更新**：2026-06-04  
> **版本**：V1.0
