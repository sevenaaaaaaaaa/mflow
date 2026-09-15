---
type: storyline
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-creation"
tools: [opencode, claude, cursor]
status: active
path: 1-1 Harness/08-storyline/STORYLINE-BY-DIRECTION.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# 落地页模块与故事线一览

> **上线依据**：[README.md](./README.md) 字段说明 + [preview-data.json](./preview-data.json) 示例 JSON。  
> 本文回答：**有几类页面 → 每类用哪些 section → 对应哪个 `type` → 干什么用**。

---

## 一、总览

### 1.1 六大页面类型

| 页面类型 | URL 路径 | Sanity `category` | 故事线 | section 数 | 页面定位 |
|----------|----------|-------------------|--------|------------|----------|
| **Features** | `/features/{slug}` | `feature` | 4 条 | 13 | 单功能/能力介绍，讲清价值 → 试用 → 证言/定价 → 转化 |
| **Tools** | `/tools/{slug}` | `tool` | 6 条 | 12～13 | 工具页，强调试用、步骤、案例内容 |
| **Product** | `/product/{slug}` | `product` | 4 条 | 12～13 | 产品线总览，偏 Tab + 网格，含证言、定价、FAQ、底部 CTA |
| **Scenarios** | `/scenarios/{slug}` | `scenario` | 2 条 | 11 | 行业/场景叙事，Tab 有两种布局方案 |
| **Solution** | `/solution/{slug}` | `solution` | 1 条 | 12 | 方案包售卖，模块最全之一 |
|| **Landing Page** | 待定 | 待定 | 2 条 | 12 | 最全 demo 页，模块覆盖最广 |
|| **Topic** | `/topic/{slug}` | `topic` | 6 条 | 12～14 | 复合型内容聚合枢纽，以话题为中心分发 Blog + Tools 内容 |

**故事线** = 同一页面类型下，`bodyJson` 里 section 的组合方案。  
规则：**每个分叉、每个变体都单独计为一条新故事线**（不合并为"扩展"说明）。

### 1.2 两个层级（别混）

| 层级 | 是什么 | 数量 | 举例 |
|------|--------|------|------|
| **本体** | 页面里一段 section 的**职责**（产品语言） | 17 种 | 「首屏」「能力 Tab」「步骤教程」 |
| **JSON 模块** | `bodyJson` 里 `"type"` 字段的**具体组件** | 33 种 | `hero-split`、`capability-tabs` |

**关系：** 每个本体在上线时选 **1 个** JSON `type`（若该本体对应多种组件，则从中择一 = **变体**）。

### 1.3 数字速查

| 项目 | 数量 |
|------|------|
| 页面类型 | **7** |
| 页面本体（section 职责） | **17**（每类页面只用其中一部分） |
| 可上线 JSON 模块 | **33**（见 §二；示例见 `preview-data.json`） |
| 故事线合计 | **25 条** |

---

## 二、JSON 模块字典（33 种）

每种模块：`type` 字符串 = 上线 JSON 里的 `"type"`。示例字段见 `preview-data.json` 同名条目。

### Hero 首屏（5 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `hero-split` | 左文右图，tag + 双行标题 + 按钮 + 4:3 大图 | 功能/工具页默认首屏，信息密度适中 |
| `hero-cinematic` | 居中标题 + 全宽剧院大图 | 品牌感强、视觉主导的 Product / Landing |
| `hero-journey` | 居中标题 + 横向 step 卡片条 | 强调「用户旅程 / 多步骤路径」 |
| `hero-mosaic` | 居中标题 + 不规则拼贴瓦片 | 多能力并列、修复/组合类叙事 |
| `hero-gallery` | 居中标题 + 6 宫格工具入口 | 产品矩阵、多工具入口总览 |

### 网格 / Bento / 信息簇（5 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `bento-2` | 两栏等大特性卡 | 两个核心卖点并列 |
| `bento-4` | 2×2 不规则四宫格 | 四个能力点，视觉有主次 |
| `bento-6` | 六卡 bento 布局 | 六个能力/场景，信息量大 |
| `feature-grid` | 2/3/4 列对称特性网格 | 均匀罗列功能点（`preview-data` 暂无示例，见 README） |
| `cluster-block-dense` | 3 列 icon 小卡墙 | 痛点列表、能力清单、内容簇 |

### Tab / 矩阵 / 博客 / 图文（5 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `capability-tabs` | 左 Tab 列表 + 右大图内容区 | 多功能切换讲解（Features / Solution / Scenarios 核心模块） |
| `tool-grid` | 工具卡 3 列网格（icon、标签、评分） | Tools 页、Landing 的工具矩阵、Product 卡片网格 |
| `blog-grid` | 博客/文章 3 列卡片 | 内容营销、案例文章聚合（Tools 内容簇方案 B） |
| `feature-detail` | 多条图文左右交错 | 深度讲一个能力、Dynamic 动态说明段 |
| `canvas-wall` | 10 卡 bento 画布墙（作者/likes） | 作品墙、Gallery 展示段 |

### Portrait / Showcase（4 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `portrait-grid-3` | 3 列 1:1 方卡 | 三类资产/三类场景 |
| `portrait-grid-4` | 4 列 3:4 竖卡 | 四象限场景、四类产品形态 |
| `showcase-stacked` | 垂直堆叠大图叙事 | 流程/前后阶段展示（Dynamic 段） |
| `showcase-horizontal` | 横向滚动大图叙事 | 多案例横滑浏览 |

### 互动 / 跑马灯（3 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `prompt-launcher` | 居中输入框 + prompt 标签 | **Tools 专属**：让用户立刻试工具 |
| `logo-loop` | 品牌 logo 循环条 | 社会证明、客户列表（Product Photo 段） |
| `media-marquee` | 作品图横向跑马灯 | 视觉案例流、创意范围展示 |

### CTA / 流程（3 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `cta-default` | 居中渐变 CTA 横幅 + 双按钮 | 页内中段转化或**底部收口**（同一组件，文案不同） |
| `workflow-horizontal` | 横向简短 N 步 | 「3 步搞定」类 How-to |
| `workflow-vertical` | 纵向带图 N 步 | 需要配图详解的步骤教程 |

### 对比（2 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `comparison-table` | 多列功能对比表 | Lovart vs 竞品 / 旧工作流 |
| `comparison-before-after` | 单图前后对比滑块 | 效果类工具、视觉改善证明 |

### 证言 / 评价（3 变体）

| `type` | 作用 | 适用场景 |
|--------|------|----------|
| `testimonial` | 客户引言轮播/卡片 | 单条或多条引言，偏叙事 |
| `review-grid-3col` | 3 列评价卡 | 中等数量用户故事 |
| `review-grid-4col` | 4 列评价卡 | 更多评价、偏社交证明墙 |

### 数据 / 信任 / 定价 / FAQ（4 变体）

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

---

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

---

### 4.2 Tools（6 条故事线 · 12～13 个本体）

**叙事：** 工具价值 → 特性（可加 Tab）→ **立刻试用** → 社会证明 → 页内转化 → 步骤 → 对比 → **内容簇（分叉）** → 深度说明 → FAQ → 底 CTA。

| 序 | 本体 | 故事线 A | 故事线 B | 可选变体 | 用途 |
|----|------|----------|----------|----------|------|
| 1 | 首屏 | `hero-split` | 同左 | hero-* | 工具名 + 一句话价值 |
| 2 | 多栏特性区 | `bento-4` | 同左 | bento-*, feature-grid | 工具能做什么 |
| 3 | 特性大卡 | `bento-2` | 同左 | bento-*, feature-detail | 核心能力 2 卡 |
| 4 | 试用输入 | `prompt-launcher` | 同左 | — | **Tools 关键模块** |
| 5 | Logo 滚动条 | `logo-loop` | 同左 | logo-loop, media-marquee | 谁在用 / 案例图 |
| 6 | 页内 CTA | `cta-default` | 同左 | — | 试用中段拦截 |
| 7 | 步骤教程 | `workflow-horizontal` | 同左 | workflow-* | 操作步骤 |
| 8 | 对比 | `comparison-table` | 同左 | comparison-* | vs 同类工具 |
| 9 | 内容簇 | `cluster-block-dense` | **`blog-grid`** | cluster, blog-grid | **唯一分叉**：能力卡墙 vs 文章网格 |
| 10 | 动态图文 | `feature-detail` | 同左 | feature-detail, showcase-* | 案例深讲 |
| 11 | FAQ | `faq` | 同左 | — | 工具使用问答 |
| 12 | 底部 CTA | `cta-default` | 同左 | — | 最终转化 |

**Tools 故事线（每个分叉/变体单独计线）：**

| 故事线 ID | 相对基线的变更 | 说明 |
|-----------|------------------|------|
| `tools-A` | 内容簇 = `cluster-block-dense` | 基准线 A |
| `tools-B` | 内容簇 = `blog-grid` | 分叉线 B |
| `tools-tab-A` | 在序 3 后插入 `capability-tabs`（布局 A） | Tab 变体单独成线 |
| `tools-tab-B` | 在序 3 后插入 `capability-tabs`（布局 B） | Tab 变体单独成线 |
| `tools-grid-feature` | 序 2 改为 `feature-grid` | 网格变体单独成线 |
| `tools-grid-bento6` | 序 2 改为 `bento-6` | 网格变体单独成线 |

> 含 `tools-tab-*` 的故事线本体数为 13，其余为 12。

**Tools 全量故事线（逐条完整呈现）：**

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `tools-A` | `hero-split → bento-4 → bento-2 → prompt-launcher → logo-loop → cta-default → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `tools-B` | `hero-split → bento-4 → bento-2 → prompt-launcher → logo-loop → cta-default → workflow-horizontal → comparison-table → blog-grid → feature-detail → faq → cta-default` |
| `tools-tab-A` | `hero-split → bento-4 → bento-2 → capability-tabs(布局A) → prompt-launcher → logo-loop → cta-default → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `tools-tab-B` | `hero-split → bento-4 → bento-2 → capability-tabs(布局B) → prompt-launcher → logo-loop → cta-default → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `tools-grid-feature` | `hero-split → feature-grid → bento-2 → prompt-launcher → logo-loop → cta-default → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `tools-grid-bento6` | `hero-split → bento-6 → bento-2 → prompt-launcher → logo-loop → cta-default → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |

**不用的本体（4）：** 卡片网格、图库展示、证言、定价

---

### 4.3 Product（4 条故事线 · 12～13 个本体）

**叙事：** 产品线总览 → 多栏 → Tab 分产品 → 工具/能力网格 → 步骤 → 对比 → 内容簇 → 动态说明 → 证言 → 定价 → FAQ → 底部 CTA（可加 Logo 条做社会证明）。

| 序 | 本体 | 基准线 | 含 Logo 线 | 视觉扩展线 A | 视觉扩展线 B | JSON 推荐 |
|----|------|--------|------------|---------------|---------------|-----------|
| 1 | 首屏 | `hero-cinematic` | 同左 | `hero-gallery` | `hero-split` | `hero-cinematic` 或 `hero-gallery` |
| 2 | 多栏特性区 | `bento-4` | 同左 | `portrait-grid-3` | `bento-6` | `bento-4` / `portrait-grid-3` |
| 3 | 能力 Tab | `capability-tabs` | 同左 | 同左 | 同左 | `capability-tabs` |
| 4 | 卡片网格 | `tool-grid` | 同左 | 同左 | 同左 | `tool-grid` |
| 5 | 步骤教程 | `workflow-vertical` | 同左 | `workflow-horizontal` | 同左 | `workflow-vertical` |
| 6 | 对比 | `comparison-table` | 同左 | 同左 | `comparison-before-after` | `comparison-table` |
| 7 | 内容簇 | `cluster-block-dense` | 同左 | `blog-grid` | 同左 | `cluster-block-dense` |
| 8 | 动态图文 | `showcase-stacked` | 同左 | `feature-detail` | `showcase-horizontal` | `showcase-stacked` |
| 9 | Logo 滚动条 | — | `logo-loop` | `logo-loop` | `logo-loop` | `logo-loop` |
| 10 | 证言 | `testimonial` | `testimonial` | `review-grid-3col` | `review-grid-4col` | `testimonial` |
| 11 | 定价 | `pricing-block` | `pricing-block` | `pricing-block` | `pricing-block` | `pricing-block` |
| 12 | FAQ | `faq` | `faq` | `faq` | `faq` | `faq` |
| 13 | 底部 CTA | `cta-default` | `cta-default` | `cta-default` | `cta-default` | `cta-default` |

**四条故事线：**

| ID | 包含 section | 说明 |
|----|--------------|------|
| `product-标准` | 序 1～8、10～13 | 标准产品线页（含证言/定价/FAQ/底 CTA） |
| `product-含社会证明` | `product-标准` + 序 9 Logo | 在标准线基础上加客户/案例滚动 |
| `product-视觉扩展-A` | `product-含社会证明`，并切换序 1/2/5/7/8/10 的变体 | 保留全链路模块，换更偏内容化视觉 |
| `product-视觉扩展-B` | `product-含社会证明`，并切换序 1/6/8/10 的变体 | 保留全链路模块，换更偏对比/展示视觉 |

**Product 全量故事线（逐条完整呈现）：**

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `product-标准` | `hero-cinematic → bento-4 → capability-tabs → tool-grid → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` |
| `product-含社会证明` | `hero-cinematic → bento-4 → capability-tabs → tool-grid → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → logo-loop → testimonial → pricing-block → faq → cta-default` |
| `product-视觉扩展-A` | `hero-gallery → portrait-grid-3 → capability-tabs → tool-grid → workflow-horizontal → comparison-table → blog-grid → feature-detail → logo-loop → review-grid-3col → pricing-block → faq → cta-default` |
| `product-视觉扩展-B` | `hero-split → bento-4 → capability-tabs → tool-grid → workflow-vertical → comparison-before-after → cluster-block-dense → showcase-horizontal → logo-loop → review-grid-4col → pricing-block → faq → cta-default` |

**明确不用：** 特性大卡（产品规则禁用）、图库展示、试用输入、页内 CTA

---

### 4.4 Scenarios（2 条故事线 · 11 个本体）

**叙事：** 场景痛点 → 能力概览 → **Tab 讲场景方案（两种布局）** → 特性 → 步骤 → 对比 → 内容 → 深度 → 证言 → FAQ → 转化。

| 序 | 本体 | 故事线 A | 故事线 B | 用途 |
|----|------|----------|----------|------|
| 1 | 首屏 | `hero-split` | 同左 | 场景名 + 痛点 |
| 2 | 多栏特性区 | `cluster-block-dense` | 同左 | 场景下 6 个能力点 |
| 3 | 能力 Tab | `capability-tabs`（布局 A） | `capability-tabs`（布局 B） | **分叉**：Tab 视觉/信息架构两套方案 |
| 4 | 特性大卡 | `bento-4` | 同左 | 场景核心能力 |
| 5 | 步骤教程 | `workflow-horizontal` | 同左 | 场景落地步骤 |
| 6 | 对比 | `comparison-table` | 同左 | vs 传统做法 |
| 7 | 内容簇 | `cluster-block-dense` | 同左 | 子场景/案例 |
| 8 | 动态图文 | `feature-detail` | 同左 | 场景故事长文 |
| 9 | 证言 | `review-grid-3col` | 同左 | 该场景客户评价 |
| 10 | FAQ | `faq` | 同左 | 场景相关问答 |
| 11 | 底部 CTA | `cta-default` | 同左 | 转化 |

**Scenarios 全量故事线（逐条完整呈现）：**

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `scenarios-A` | `hero-split → cluster-block-dense → capability-tabs(布局A) → bento-4 → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → review-grid-3col → faq → cta-default` |
| `scenarios-B` | `hero-split → cluster-block-dense → capability-tabs(布局B) → bento-4 → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → review-grid-3col → faq → cta-default` |

**不用（6）：** 卡片网格、图库展示、试用输入、Logo 滚动条、页内 CTA、定价

---

### 4.5 Solution（1 条故事线 · 12 个本体）

**叙事：** 与 Features 类似，但更偏「整套方案」售卖，含 Tab、定价，模块更全。

| 序 | 本体 | JSON `type`（推荐） | 可选变体 | 用途 |
|----|------|---------------------|----------|------|
| 1 | 首屏 | `hero-cinematic` | hero-* | 方案名 + 整体价值 |
| 2 | 多栏特性区 | `bento-4` | bento-*, cluster | 方案包含什么 |
| 3 | 能力 Tab | `capability-tabs` | — | 方案模块切换 |
| 4 | 特性大卡 | `bento-2` | bento-*, feature-detail | 核心交付物 |
| 5 | 步骤教程 | `workflow-vertical` | workflow-* | 实施/使用路径 |
| 6 | 对比 | `comparison-table` | comparison-* | vs 自建/外包 |
| 7 | 内容簇 | `cluster-block-dense` | blog-grid | 适用行业/案例 |
| 8 | 动态图文 | `showcase-stacked` | feature-detail, showcase-* | 方案效果展示 |
| 9 | 证言 | `testimonial` | review-grid-* | 方案客户故事 |
| 10 | 定价 | `pricing-block` | — | 方案套餐 |
| 11 | FAQ | `faq` | — | 采购/实施问答 |
| 12 | 底部 CTA | `cta-default` | — | 预约/购买 |

**不用（5）：** 卡片网格、图库展示、试用输入、Logo 滚动条、页内 CTA

---

### 4.6 Landing Page（2 条故事线 · 12 个本体）

**叙事：** 最全模块 demo，覆盖 Hero、Tab、网格、Gallery、对比、FAQ 等，用于「一屏看全组件能力」。

| 序 | 本体 | 故事线 A | 故事线 B | JSON 推荐 |
|----|------|----------|----------|-----------|
| 1 | 首屏 | `hero-gallery` | 同左 | 多入口总览 |
| 2 | 多栏特性区 | `bento-6` | 同左 | 六能力 bento |
| 3 | 能力 Tab | `capability-tabs` | 同左 | 能力切换 |
| 4 | 卡片网格 | `tool-grid` | 同左 | 工具矩阵 |
| 5 | 特性大卡 | `bento-4` | 同左 | 重点能力 |
| 6 | 图库展示 | `canvas-wall` | 同左 | 作品墙 |
| 7 | 步骤教程 | `workflow-horizontal` | 同左 | 流程 |
| 8 | 对比 | `comparison-table` | 同左 | 对比 |
| 9 | 内容簇 | `cluster-block-dense` | 同左 | 信息簇 |
| 10 | 动态图文 | `feature-detail` | **`showcase-horizontal`** | **分叉**：交错图文 vs 横滑叙事 |
| 11 | FAQ | `faq` | 同左 | FAQ |
| 12 | 底部 CTA | `cta-default` | 同左 | 收口 |

**Landing Page 全量故事线（逐条完整呈现）：**

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `landing-A` | `hero-gallery → bento-6 → capability-tabs → tool-grid → bento-4 → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `landing-B` | `hero-gallery → bento-6 → capability-tabs → tool-grid → bento-4 → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → showcase-horizontal → faq → cta-default` |

**不用（5）：** 试用输入、Logo 滚动条、页内 CTA、证言、定价

---

### 4.7 Topic（6 条故事线 · 12～14 本体）

> **定位**：与其他 6 类不同，Topic 页面不是交易/转化页，而是**复合型内容聚合枢纽**。核心目标是：把分散的 Blog、Tools 页面、产品能力、外部话题信号整合到一个高信息密度页面中，成为用户在某个话题上的"一站式信息终点"。
>
> **数据驱动**：Topic 候选从 GSC 非品牌词、ORM 社交监听、竞品关键词矩阵、产品 KB 中提取。不同于 Scenarios（稳定使用场景）和 Solutions（行业方案），Topics 具有**时效性**和**动态性**。
>
> **叙事差异**：Features/Tools 走「试用→信任→转化」，Topic 走「**话题引子→内容聚合→产品映射→深度分发→分流**」。`blog-grid` 和 `tool-grid` 是核心模块（不可省略），因为 Topic 页面的价值就是内容分发。

#### Topic 五大类型与故事线映射

| 类型 | 故事线 ID | 叙事风格 | 典型话题 | 模块数 |
|------|----------|----------|----------|--------|
| T1 模型聚焦 | `topic-model` | 模型介绍→内容聚合→产品实操→FAQ | "Veo 3.1 on Lovart: What Changed" | 14 |
| T2 趋势热点 | `topic-trend` | 趋势起因→案例展示→产品实现→FAQ | "AI Product Photography Replacing Studios" | 12 |
| T3 产品深度 | `topic-product` | 概念定义→能力展开→内容分发→FAQ | "MCoT Engine Deep Dive" | 13 |
| T4 社群争议 | `topic-community` | 争议背景→各方观点→产品立场→FAQ | "Is AI Design Killing Creativity?" | 12 |
| T5 知识枢纽 | `topic-hub` | 全景总览→多维对比→深度分发→FAQ | "AI Video Models Complete Guide 2026" | 14 |

#### 两类轻量变体（K1/K2 — 保留给简单话题）

轻量变体用于话题范围窄、不需要深度展开的场景（如单一工具对比、简单用例聚合）。不适用于 T1-T5 主体场景。

| 故事线 ID | 模块序列 | 适用 |
|-----------|----------|------|
| `topic-light-A`（原 K1） | `hero-cinematic → blog-grid → tool-grid → faq → cta-default` | 内容分发型轻话题 |
| `topic-light-B`（原 K2） | `hero-split → workflow-vertical → capability-tabs → blog-grid → cta-default` | 产品实操型轻话题 |

---

#### 4.7.1 基准线 `topic-model`（T1 模型聚焦 · 14 本体）

**叙事**：模型是什么 → 在 Lovart 能做什么 → 相关 Blog 深读 → 相关 Tools 入口 → 实操 → 对比 → FAQ → 分流。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 在本页的用途 |
|----|------|---------------------|----------|--------------|
| 1 | 首屏 | `hero-cinematic` | `hero-split` | 模型名 + Lovart 集成声明 + 主 CTA |
| 2 | 多栏特性区 | `bento-6` | `bento-4`、`feature-grid` | 6 个该模型在 Lovart 上的典型产出类型 |
| 3 | 内容簇（Blog 轨） | `blog-grid` | — | **核心模块**：引用 3-6 篇相关 Blog（模型测评/教程/对比） |
| 4 | 卡片网格（Tools 轨） | `tool-grid` | — | **核心模块**：相关 Tools 入口（如对应图像/视频工具） |
| 5 | 能力 Tab | `capability-tabs` | — | 4 种该模型使用模式（文生图/图生图/批量/局部重绘） |
| 6 | 试用输入 | `prompt-launcher` | — | 预填该模型最优 prompt 模板 |
| 7 | 图库展示 | `canvas-wall` | `showcase-horizontal` | 10 个 Lovart 上该模型的实际产出案例 |
| 8 | 步骤教程 | `workflow-horizontal` | `workflow-vertical` | "选择模型→输入 prompt→迭代优化"三步 |
| 9 | 对比 | `comparison-table` | — | 该模型 vs 同类模型 vs 传统方式 |
| 10 | 内容簇 | `cluster-block-dense` | — | 6 个该模型的常见限制 + Lovart 如何弥补 |
| 11 | 动态图文 | `feature-detail` | — | 3-4 个该模型在 Lovart 上的专属特性 |
| 12 | 页内 CTA | `cta-default` | — | "Try [Model] on Lovart" |
| 13 | FAQ | `faq` | — | "这个模型适合什么/不适合什么" |
| 14 | 底部 CTA | `cta-default` | — | 分流 CTA（"继续看 Blog 深读"或"直接试用"） |

**不用（3）：** Logo 滚动条、证言、定价

---

#### 4.7.2 `topic-trend`（T2 趋势热点 · 12 本体）

**叙事**：趋势是什么 → 为什么火 → 内容深读 → 产品实现 → FAQ → 分流。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 用途 |
|----|------|---------------------|----------|------|
| 1 | 首屏 | `hero-journey` | `hero-cinematic` | 趋势起源 + 时间线 |
| 2 | 多栏特性区 | `bento-4` | `bento-6` | 4 个该趋势的典型应用场景 |
| 3 | 内容簇（Blog 轨） | `blog-grid` | — | **核心**：引用相关趋势分析 Blog |
| 4 | Logo/滚动条 | `media-marquee` | `logo-loop` | 该趋势的视觉案例轮播 |
| 5 | 能力 Tab | `capability-tabs` | — | 4 种"如何在 Lovart 上实现该趋势" |
| 6 | 试用输入 | `prompt-launcher` | — | 预填趋势风格的 prompt |
| 7 | 图库展示 | `canvas-wall` | — | Lovart 生成的趋势风格作品 |
| 8 | 对比 | `comparison-before-after` | `comparison-table` | "传统方式 vs Lovart 一键实现" |
| 9 | 内容簇 | `cluster-block-dense` | — | 6 个"你该知道的趋势细节" |
| 10 | 证言 | `testimonial` | — | 引用真实用户/设计师评价 |
| 11 | FAQ | `faq` | — | "这个趋势会持续多久/适合什么行业" |
| 12 | 底部 CTA | `cta-default` | — | "Start Creating in [Trend Style]" |

**不用（5）：** 卡片网格、步骤教程、动态图文、页内 CTA、定价

---

#### 4.7.3 `topic-product`（T3 产品深度 · 13 本体）

**叙事**：概念是什么 → 能力展开 → Blog 深读 → Tools 入口 → 实操 → FAQ → 分流。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 用途 |
|----|------|---------------------|----------|------|
| 1 | 首屏 | `hero-cinematic` | `hero-split` | 产品概念名 + 一句话定义 |
| 2 | 多栏特性区 | `bento-6` | `bento-4` | 6 个核心能力卡片 |
| 3 | 内容簇（Blog 轨） | `blog-grid` | — | **核心**：引用深度测评/教程 Blog |
| 4 | 卡片网格（Tools 轨） | `tool-grid` | — | **核心**：相关功能入口 |
| 5 | 能力 Tab | `capability-tabs` | — | 4 个实际使用模式 |
| 6 | 步骤教程 | `workflow-vertical` | `workflow-horizontal` | "输入→处理→输出"纵向流程 |
| 7 | 图库展示 | `canvas-wall` | — | 10 个产出案例 |
| 8 | 对比 | `comparison-table` | — | "有该能力 vs 没有该能力" |
| 9 | 动态图文 | `feature-detail` | — | 4 个深度技术特性 |
| 10 | 数据/信任 | `proof-block` | `stats` | 3 个信任信号/性能数据 |
| 11 | 页内 CTA | `cta-default` | — | "Try It Yourself" |
| 12 | FAQ | `faq` | — | 技术细节 Q&A |
| 13 | 底部 CTA | `cta-default` | — | 分流（"深入阅读"或"立即试用"） |

**不用（4）：** 试用输入、Logo 滚动条、证言、定价

---

#### 4.7.4 `topic-community`（T4 社群争议 · 12 本体）

**叙事**：争议是什么 → 各方观点 → Blog 深读 → 产品立场 → FAQ → 参与/分流。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 用途 |
|----|------|---------------------|----------|------|
| 1 | 首屏 | `hero-journey` | `hero-cinematic` | 争议时间线 + 各方观点简述 |
| 2 | 多栏特性区 | `bento-4` | `cluster-block-dense` | 4 个关键争论点 |
| 3 | 内容簇（Blog 轨） | `blog-grid` | — | **核心**：引用 Lovart Blog 深度分析 |
| 4 | 数据/信任 | `stats` | `proof-block` | 引用调查数据/投票/社区统计 |
| 5 | 证言 | `testimonial` | `review-grid-3col` | 引用真实设计师的公开观点（各方立场） |
| 6 | 对比 | `comparison-table` | — | "不同立场的设计师如何看待同一问题" |
| 7 | 图库展示 | `canvas-wall` | — | Lovart 在该争议领域的产出示例 |
| 8 | 内容簇 | `cluster-block-dense` | — | 6 个"无论你站哪边都需要知道的事实" |
| 9 | 动态图文 | `feature-detail` | — | Lovart 如何回应这个争议（产品层面） |
| 10 | 页内 CTA | `cta-default` | — | "Join the Conversation" 或 "Try Lovart's approach" |
| 11 | FAQ | `faq` | — | 社区常见疑问 |
| 12 | 底部 CTA | `cta-default` | — | 参与讨论 / 试用 |

**不用（5）：** 卡片网格、试用输入、Logo 滚动条、步骤教程、定价

---

#### 4.7.5 `topic-hub`（T5 知识枢纽 · 14 本体）

**叙事**：全景总览 → 子话题入口 → Blog 深读矩阵 → Tools 入口矩阵 → 多维对比 → 知识簇 → FAQ → 分流。这是 Topics 中信息密度最高的类型，模块数最多。

| 序 | 本体 | JSON `type`（主线） | 可选变体 | 用途 |
|----|------|---------------------|----------|------|
| 1 | 首屏 | `hero-cinematic` | `hero-gallery` | 话题全景 + "Everything you need to know" |
| 2 | 多栏特性区 | `bento-6` | `portrait-grid-3` | 6 个子话题入口 |
| 3 | 内容簇（Blog 轨） | `blog-grid` | — | **核心**：所有相关 Blog（按子话题分组，≥6 篇） |
| 4 | 卡片网格（Tools 轨） | `tool-grid` | — | **核心**：所有相关 Tools 页面 |
| 5 | 能力 Tab | `capability-tabs` | — | 按维度切换（模型/工具/工作流/案例） |
| 6 | 图库展示 | `canvas-wall` | `showcase-horizontal` | 各子话题的代表性产出 |
| 7 | 步骤教程 | `workflow-horizontal` | `workflow-vertical` | "从选择工具到产出成品的通用路径" |
| 8 | 对比 | `comparison-table` | — | 全品类横向对比（**核心模块**：枢纽页的灵魂） |
| 9 | 内容簇 | `cluster-block-dense` | — | 12 个关键知识点卡片（最高密度） |
| 10 | Logo/滚动条 | `media-marquee` | — | 案例轮播 |
| 11 | 动态图文 | `feature-detail` | — | 4 个深度对比展开 |
| 12 | 页内 CTA | `cta-default` | — | "想深入哪个方向？"分流 |
| 13 | FAQ | `faq` | — | 终极 FAQ |
| 14 | 底部 CTA | `cta-default` | — | 分流 CTA（多入口） |

**不用（3）：** 试用输入、证言、定价

---

#### 4.7.6 Topic 全量故事线（逐条完整呈现）

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `topic-model` | `hero-cinematic → bento-6 → blog-grid → tool-grid → capability-tabs → prompt-launcher → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → cta-default → faq → cta-default` |
| `topic-trend` | `hero-journey → bento-4 → blog-grid → media-marquee → capability-tabs → prompt-launcher → canvas-wall → comparison-before-after → cluster-block-dense → testimonial → faq → cta-default` |
| `topic-product` | `hero-cinematic → bento-6 → blog-grid → tool-grid → capability-tabs → workflow-vertical → canvas-wall → comparison-table → feature-detail → proof-block → cta-default → faq → cta-default` |
| `topic-community` | `hero-journey → bento-4 → blog-grid → stats → testimonial → comparison-table → canvas-wall → cluster-block-dense → feature-detail → cta-default → faq → cta-default` |
| `topic-hub` | `hero-cinematic → bento-6 → blog-grid → tool-grid → capability-tabs → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → media-marquee → feature-detail → cta-default → faq → cta-default` |
| `topic-light-A` | `hero-cinematic → blog-grid → tool-grid → faq → cta-default` |
| `topic-light-B` | `hero-split → workflow-vertical → capability-tabs → blog-grid → cta-default` |

> **轻量变体 `topic-light-A`/`topic-light-B`** 继承自旧 K1/K2，保留给话题范围窄、不需要深度展开的场景。T1-T5 主场景使用对应的 5 条完整故事线。

#### 4.7.7 Topic 故事线分叉规则

与 Features/Tools 不同，Topic 的变体不在模块 type 的选择上分叉（如"网格位用 bento-4 还是 feature-grid"），而在**整条故事线的叙事结构**上分叉。选线指南：

| 如果话题... | 选这条故事线 |
|------------|-------------|
| 围绕一个具体 AI 模型/工具，用户想了解"它是什么 + 在 Lovart 上怎么用" | `topic-model` |
| 围绕一个正在发酵的行业趋势/设计风格/热点事件 | `topic-trend` |
| 围绕 Lovart 自身的一个产品概念/能力深度解析 | `topic-product` |
| 围绕设计/AI 领域的一个争议性话题 | `topic-community` |
| 围绕一个品类的全维度知识聚合（横向对比多个模型/工具/方法） | `topic-hub` |
| 话题范围窄，仅需轻量内容分发 | `topic-light-A` 或 `topic-light-B` |

**不用（通用）：** 定价（Topic 页面不卖产品，只分发内容）

---

## 五、七类对照总表

| 页面类型 | 故事线 | 本体数 | 分叉 section | 含定价 | 含试用 | 含 Gallery |
|----------|--------|--------|--------------|--------|--------|------------|
| Features | 4 | 13 | Tab 布局、网格位 type | ✓ | ✓ | — |
| Tools | 6 | 12～13 | 内容簇、Tab 布局、网格位 type | — | ✓ | — |
| Product | 4 | 12～13 | 首屏/多栏/动态/证言视觉变体（可加 Logo） | ✓ | — | — |
| Scenarios | 2 | 11 | 能力 Tab | — | — | — |
| Solution | 1 | 12 | — | ✓ | — | — |
| Landing Page | 2 | 12 | 动态图文 | — | — | ✓ |
| **Topic** | **6** | **12～14** | **叙事结构分叉（5 种场景）** | — | ✓ | ✓ |

---

## 六、定稿与写 JSON

```
1. 选页面类型（如 Tools）
2. 选故事线（如 故事线 B = blog-grid 内容簇）
3. 按 §四表格顺序，列出每段 `type`
4. 从 preview-data.json 复制对应段落的字段骨架
5. 替换文案与 media URL → 写入 Sanity bodyJson
```

**勾选清单格式示例（Tools · 故事线 A）：**

```
hero-split → bento-4 → bento-2 → prompt-launcher → logo-loop → cta-default
→ workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default
```

---

## 七、相关文件

| 文件 | 用途 |
|------|------|
| [README.md](./README.md) | 每个 `type` 的字段说明 |
| [preview-data.json](./preview-data.json) | 每个 `type` 的可复制 JSON 示例 |
| [STORYLINES.md](./STORYLINES.md) | 早期短链示例（F1/T1），非满配故事线 |
| FULL-STORYLINE-* | ⚠️ 已过时，勿用 |
