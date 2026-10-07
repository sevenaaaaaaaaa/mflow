# 落地页模块与故事线一览

> **上线依据**：[README.md](./README.md) 字段说明 + [preview-data.json](./preview-data.json) 示例 JSON。  
> 本文回答：**有几类页面 → 每类用哪些 section → 对应哪个 `type` → 干什么用**。

---

## 〇、故事线为总纲（页面生成第一原则）

页面生成以**故事线**为总纲。选定故事线后，六个维度全部**从这一条故事线派生**，不各写一套：

| 维度 | 从故事线派生的来源 | 落点 |
|------|--------------------|------|
| **文案** | 故事线 copy 绑定 | `copy`/`copyDefault`（landing/solution/scenarios JSON）、`page-copy-bindings.json`（feature/tool/product/topic） |
| **模块** | 故事线 `sections` | 本文各 §四 的完整 `type` 顺序 |
| **个性化** | 故事线 `audience` + `intent` | Persona Matrix（`lovart-landing-page/SKILL.md`） |
| **配图** | 故事线 `sections` + card title | `image_pool`（选图范围被该故事线的模块集界定） |
| **CRO** | 故事线 `intent` + `ctaStyle` | 流量阶段 / CTA 文案 / 紧迫感 |
| **质检** | 故事线绑定 | `COPY-PREFLIGHT.md`（storyline-driven）+ 质量门禁 |

**顺序**：`PAGE-BRIEF → 选故事线 → 读全维度绑定 → 生成 → COPY-PREFLIGHT`。  
**迭代**：改哪个维度就改故事线的对应字段，不在别处另写一套（防漂移）。  
机器约定见 [`page-copy-bindings.json`](./page-copy-bindings.json) 的 `governedDimensions`；统一说明见 [`STORYLINE-COPY-UNIFICATION-2026-07-05.md`](./STORYLINE-COPY-UNIFICATION-2026-07-05.md)。

---

## 一、总览

### 1.1 六大页面类型

| 页面类型 | URL 路径 | Sanity `category` | 故事线 | section 数 | 页面定位 |
|----------|----------|-------------------|--------|------------|----------|
| **Features** | `/features/{slug}` | `feature` | 4 条 | 13 | 单功能/能力介绍，讲清价值 → 试用 → 证言/定价 → 转化 |
| **Tools** | `/tools/{slug}` | `tool` | 6 条 | 12～13 | 工具页，强调试用、步骤、案例内容 |
| **Product** | `/product/{slug}` | `product` | 4 条 | 12～13 | 产品线总览，偏 Tab + 网格，含证言、定价、FAQ、底部 CTA |
| **Scenarios** | `/scenarios/{slug}` | `scenario` | 14 条 | 11 | 行业/场景叙事，8 个分叉位可选变体（见 §4.4） |
| **Solution** | `/solution/{slug}` | `solution` | 6 条 | 12 | 方案包售卖；按人群/行业选 Hero、步骤、案例与证言变体 |
| **Landing Page** | 待定 | 待定 | 2 条 | 12 | 最全 demo 页，模块覆盖最广 |

**故事线** = 同一页面类型下，`bodyJson` 里 section 的组合方案。  
规则：**每个分叉、每个变体都单独计为一条新故事线**（不合并为“扩展”说明）。

### 1.2 两个层级（别混）

| 层级 | 是什么 | 数量 | 举例 |
|------|--------|------|------|
| **本体** | 页面里一段 section 的**职责**（产品语言） | 17 种 | 「首屏」「能力 Tab」「步骤教程」 |
| **JSON 模块** | `bodyJson` 里 `"type"` 字段的**具体组件** | 33 种 | `hero-split`、`capability-tabs` |

**关系：** 每个本体在上线时选 **1 个** JSON `type`（若该本体对应多种组件，则从中择一 = **变体**）。

### 1.3 数字速查

| 项目 | 数量 |
|------|------|
| 页面类型 | **6** |
| 页面本体（section 职责） | **17**（每类页面只用其中一部分） |
| 可上线 JSON 模块 | **33**（见 §二；示例见 `preview-data.json`） |
| 故事线合计 | **36 条** |

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

### 4.4 Scenarios（14 条故事线 · 11 个本体）

**叙事：** 场景入口 → 能力 Tab → 核心控制 → 落地步骤 → 对比证明 → 子场景/内容 → 案例深度 → 社会证明 → FAQ → 转化。  
**规则：** 每个分叉位单独成线；基准段其余位置不变。

| 序 | 本体 | 基准 `type` | 已开放变体 |
|----|------|-------------|------------|
| 1 | 首屏 | `hero-split` | `hero-journey`、`hero-cinematic` |
| 2 | 场景入口 | `cluster-block-dense` | `portrait-grid-3` |
| 3 | 能力 Tab | `capability-tabs` | 布局 A / 布局 B（独立故事线） |
| 4 | 核心控制 | `bento-4` | `bento-6`、`bento-2` |
| 5 | 步骤教程 | `workflow-horizontal` | `workflow-vertical` |
| 6 | 对比 | `comparison-table` | `comparison-before-after` |
| 7 | 子场景/内容 | `cluster-block-dense` | `blog-grid` |
| 8 | 案例深度 | `feature-detail` | `showcase-horizontal`、`showcase-stacked` |
| 9 | 社会证明 | `review-grid-3col` | `testimonial`、`review-grid-4col` |
| 10 | FAQ | `faq` | — |
| 11 | 底部 CTA | `cta-default` | — |

**故事线选型（职业/场景背景）：**

| 故事线 ID | 分叉说明 | 适用背景 |
|-----------|----------|----------|
| `scenarios-A` | Tab 布局 A | 通用基准 |
| `scenarios-B` | Tab 布局 B + autoplay | 社媒经理、输出优先团队 |
| `scenarios-journey` | 序 1 → `hero-journey` | 电商漏斗、社媒周循环、活动战役 |
| `scenarios-cinematic` | 序 1 → `hero-cinematic` | 品牌经理、高端 DTC、视觉主导 |
| `scenarios-portrait` | 序 2 → `portrait-grid-3` | 三大子场景/资产族/渠道三分法 |
| `scenarios-vertical` | 序 5 → `workflow-vertical` | 自由设计师交付、营销 playbook |
| `scenarios-bento6` | 序 4 → `bento-6` | 六触点全漏斗扫描 |
| `scenarios-bento2` | 序 4 → `bento-2` | 双成果聚焦、高意图简页 |
| `scenarios-before-after` | 序 6 → `comparison-before-after` | 产品图升级、品牌重塑 |
| `scenarios-blog` | 序 7 → `blog-grid` | 场景 hub、教育+案例 SEO 页 |
| `scenarios-showcase` | 序 8 → `showcase-horizontal` | 多子场景横滑 |
| `scenarios-stacked` | 序 8 → `showcase-stacked` | 阶段式纵叠案例 |
| `scenarios-testimonial` | 序 9 → `testimonial` | 长引言叙事、转型故事 |
| `scenarios-reviews4` | 序 9 → `review-grid-4col` | 高密度评价墙 |

**Scenarios 全量 type 顺序（14 条）：**

| 故事线 ID | 完整 `type` 顺序 |
|-----------|------------------|
| `scenarios-A` | `hero-split → cluster-block-dense → capability-tabs(A) → bento-4 → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → review-grid-3col → faq → cta-default` |
| `scenarios-B` | 同 A，序 3 为 `capability-tabs(B)` |
| `scenarios-journey` | 同 A，序 1 为 `hero-journey` |
| `scenarios-cinematic` | 同 A，序 1 为 `hero-cinematic` |
| `scenarios-portrait` | 同 A，序 2 为 `portrait-grid-3` |
| `scenarios-vertical` | 同 A，序 5 为 `workflow-vertical` |
| `scenarios-bento6` | 同 A，序 4 为 `bento-6` |
| `scenarios-bento2` | 同 A，序 4 为 `bento-2` |
| `scenarios-before-after` | 同 A，序 6 为 `comparison-before-after` |
| `scenarios-blog` | 同 A，序 7 为 `blog-grid` |
| `scenarios-showcase` | 同 A，序 8 为 `showcase-horizontal` |
| `scenarios-stacked` | 同 A，序 8 为 `showcase-stacked` |
| `scenarios-testimonial` | 同 A，序 9 为 `testimonial` |
| `scenarios-reviews4` | 同 A，序 9 为 `review-grid-4col` |

**试点主题（3）：** `ecommerce-operator`、`social-media-manager`、`freelance-designer`  
**草稿规模：** 3 主题 × 14 故事线 = **42 篇**（`draft-*`，`noIndex`）

**明确不用：** `prompt-launcher`、`tool-grid`、`logo-loop`、页内 CTA、`pricing-block`、`hero-mosaic`、`hero-gallery`

---

### 4.5 Solution（6 条故事线 · 12 个本体）

**叙事：** 整套方案售卖，含 Tab、定价、FAQ。Solution 同时服务**人群**（团队、代理、个体）与**行业**（电商、公益等），故在 12 段骨架上按受众切换 Hero、步骤、案例与证言模块。

**两条选型轴：**

| 轴 | 举例 | 优先看的信号 |
|----|------|--------------|
| **人群** | 营销团队、代理商、自由职业、大企业 | 组织规模、采购角色、是否多客户 |
| **行业** | 电商/DTC、非营利、小商家 | SKU/漏斗、筹款/影响力、个人生意 |

机器可读 SSOT：[`solution-storylines.json`](./solution-storylines.json)

#### 4.5.1 本体 × 六条故事线（分叉表）

| 序 | 本体 | team | ecommerce | agency | enterprise | solo | mission |
|----|------|------|-----------|--------|------------|------|---------|
| 1 | 首屏 | `hero-cinematic` | `hero-journey` | `hero-mosaic` | `hero-cinematic` | `hero-split` | `hero-journey` |
| 2 | 多栏特性区 | `bento-4` | `bento-4` | `bento-4` | `bento-6` | `bento-4` | `bento-4` |
| 3 | 能力 Tab | `capability-tabs` | 同左 | 同左 | 同左 | 同左 | 同左 |
| 4 | 特性大卡 | `bento-2` | `bento-2` | `feature-detail` | `feature-detail` | `bento-2` | `bento-2` |
| 5 | 步骤教程 | `workflow-vertical` | 同左 | `workflow-horizontal` | 同左 | `workflow-horizontal` | 同左 |
| 6 | 对比 | `comparison-table` | 同左 | 同左 | 同左 | `comparison-before-after` | 同左 |
| 7 | 内容簇 | `cluster-block-dense` | 同左 | 同左 | 同左 | 同左 | 同左 |
| 8 | 动态图文 | `showcase-stacked` | 同左 | `canvas-wall` | `showcase-horizontal` | 同左 | 同左 |
| 9 | 证言 | `testimonial` | `review-grid-3col` | `review-grid-4col` | `review-grid-3col` | `testimonial` | `testimonial` |
| 10 | 定价 | `pricing-block` | 同左 | 同左 | 同左 | 同左 | 同左 |
| 11 | FAQ | `faq` | 同左 | 同左 | 同左 | 同左 | 同左 |
| 12 | 底部 CTA | `cta-default` | 同左 | 同左 | 同左 | 同左 | 同左 |

#### 4.5.2 故事线 ID 与适用场景

| 故事线 ID | 编号 | 主轴 | 适用受众 / 行业 | 叙事侧重 |
|-----------|------|------|-----------------|----------|
| `solution-team` | S1 | 人群 | 营销团队、创业公司、增长团队 | 团队扩产、分布式生产、采购决策 |
| `solution-ecommerce` | S2 | 行业 | Shopify、DTC、电商运营 | 买家旅程、全漏斗素材、转化测试 |
| `solution-agency` | S3 | 人群 | 代理商、创意工作室 | 多客户、作品墙、交付加速与利润率 |
| `solution-enterprise` | S4 | 人群 | 大企业、全球品牌团队 | 治理、规模化、多区域品牌一致性 |
| `solution-solo` | S5 | 人群 | 自由职业、个体户、小商家 | 个人生产力、前后对比、低门槛 |
| `solution-mission` | S6 | 行业 | 非营利、NGO、使命驱动组织 | 影响力旅程、筹款活动、有限资源 |

#### 4.5.3 自动分配信号（写 JSON 前）

| 内容信号 | 选用故事线 |
|----------|------------|
| Shopify / DTC / PDP / SKU / 转化漏斗 | `solution-ecommerce` |
| 代理商 / 工作室 / 多客户 / pitch / 作品集 | `solution-agency` |
| 大企业 / 全球 / SSO / 治理 / 多区域 | `solution-enterprise` |
| 自由职业 / 个体户 / 一人公司 / 小商家 | `solution-solo` |
| 非营利 / 公益 / 筹款 / 影响力 | `solution-mission` |
| 营销团队 / 创业公司 / 增长团队（默认） | `solution-team` |

#### 4.5.4 全量故事线（逐条完整呈现）

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `solution-team` | `hero-cinematic → bento-4 → capability-tabs → bento-2 → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` |
| `solution-ecommerce` | `hero-journey → bento-4 → capability-tabs → bento-2 → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → review-grid-3col → pricing-block → faq → cta-default` |
| `solution-agency` | `hero-mosaic → bento-4 → capability-tabs → feature-detail → workflow-horizontal → comparison-table → cluster-block-dense → canvas-wall → review-grid-4col → pricing-block → faq → cta-default` |
| `solution-enterprise` | `hero-cinematic → bento-6 → capability-tabs → feature-detail → workflow-vertical → comparison-table → cluster-block-dense → showcase-horizontal → review-grid-3col → pricing-block → faq → cta-default` |
| `solution-solo` | `hero-split → bento-4 → capability-tabs → bento-2 → workflow-horizontal → comparison-before-after → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` |
| `solution-mission` | `hero-journey → bento-4 → capability-tabs → bento-2 → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` |

**不用（5）：** 卡片网格、试用输入、Logo 滚动条、页内 CTA、`prompt-launcher`

---

### 4.6 Landing Page（6 条投放故事线 + 1 条满配 demo · 12～15 段）

**定位：** 面向**投放人员**的 composite-v2 落地页。单页保持 12 段（投放友好）；**7 条线并集**覆盖尽量全的模块类型。

**选型轴：** 投放意图（认知 / 试用 / 信任 / 对比 / 收口 / 内部 demo）

机器可读 SSOT：[`landing-storylines.json`](./landing-storylines.json) · 制作指南：[LANDING-PRODUCTION-2026-06-07.md](./LANDING-PRODUCTION-2026-06-07.md)

#### 4.6.1 投放故事线（6 条 · 各 12 段）

| 故事线 ID | 投放意图 | 适用场景 | 叙事侧重 |
|-----------|----------|----------|----------|
| `landing-gallery-detail` | 广泛认知 | Meta/Google 广泛匹配、多工具入口 | 工具矩阵 + `feature-detail` 深讲 |
| `landing-gallery-funnel` | 漏斗教育 | 再营销、全链路教育型创意 | 工具矩阵 + `showcase-horizontal` 阶段叙事 |
| `landing-brand-trust` | 品牌 upper funnel | 品牌 campaign、信任建立 | `hero-cinematic` + `logo-loop` + `testimonial` |
| `landing-trial-now` | Search 试用转化 | 工具词、即时试用广告 | `hero-split` + `prompt-launcher` + 三步上手 |
| `landing-vs-competitor` | 竞品抢量 | 竞品词、vs/alternative 创意 | `comparison-before-after` + 痛点簇 |
| `landing-offer-close` | 再营销收口 | 促销、底部漏斗、限时 offer | `hero-journey` + `pricing-block` + `review-grid-3col` |

**别名（兼容旧 ID）：** `landing-A` → `landing-gallery-detail`；`landing-B` → `landing-gallery-funnel`

#### 4.6.2 满配 demo（1 条 · 15 段，非投放）

| 故事线 ID | 用途 | section 数 |
|-----------|------|------------|
| `landing-full` | 制作人 / 设计 QA / 模块验收 | **15** |

含：`prompt-launcher`、`logo-loop`、`testimonial`、`pricing-block` — **不建议**作为 Meta/Google 落地页模板。

#### 4.6.3 自动分配信号（写 JSON 前）

| 内容 / 创意信号 | 选用故事线 |
|----------------|------------|
| 竞品词 / alternative / vs 创意 | `landing-vs-competitor` |
| 工具试用 / Search 词 / try now | `landing-trial-now` |
| 品牌曝光 / upper funnel / 信任 | `landing-brand-trust` |
| 促销 / 再营销 / pricing offer | `landing-offer-close` |
| 漏斗阶段 / acquire→convert 叙事 | `landing-gallery-funnel` |
| 内部 demo / 模块验收 | `landing-full` |
| 多工具矩阵 / 广泛匹配（默认） | `landing-gallery-detail` |

#### 4.6.4 全量故事线（逐条完整呈现）

| 故事线 ID | 完整 `type` 顺序（从上到下） |
|-----------|-------------------------------|
| `landing-gallery-detail` | `hero-gallery → bento-6 → capability-tabs → tool-grid → bento-4 → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `landing-gallery-funnel` | `hero-gallery → bento-6 → capability-tabs → tool-grid → bento-4 → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → showcase-horizontal → faq → cta-default` |
| `landing-brand-trust` | `hero-cinematic → bento-6 → capability-tabs → logo-loop → testimonial → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `landing-trial-now` | `hero-split → bento-4 → capability-tabs → prompt-launcher → bento-2 → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → faq → cta-default` |
| `landing-vs-competitor` | `hero-split → bento-6 → capability-tabs → tool-grid → bento-4 → canvas-wall → workflow-horizontal → comparison-before-after → cluster-block-dense → feature-detail → faq → cta-default` |
| `landing-offer-close` | `hero-journey → bento-4 → capability-tabs → tool-grid → pricing-block → canvas-wall → workflow-vertical → comparison-table → cluster-block-dense → review-grid-3col → faq → cta-default` |
| `landing-full` | `hero-cinematic → bento-6 → capability-tabs → tool-grid → canvas-wall → prompt-launcher → logo-loop → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → testimonial → pricing-block → faq → cta-default` |

**7 线模块并集覆盖：** Hero 变体 · 对比 2 种 · 动态图文 2 种 · 试用 · Logo · 证言 · 定价 · Gallery

**单页仍不用：** 页内 CTA（与底部 CTA 重复）

**参考案例 JSON：** [`landing-examples/en/`](./landing-examples/en/)

---

## 五、六类对照总表

| 页面类型 | 故事线 | 本体数 | 分叉 section | 含定价 | 含试用 | 含 Gallery |
|----------|--------|--------|--------------|--------|--------|------------|
| Features | 4 | 13 | Tab 布局、网格位 type | ✓ | ✓ | — |
| Tools | 6 | 12～13 | 内容簇、Tab 布局、网格位 type | — | ✓ | — |
| Product | 4 | 12～13 | 首屏/多栏/动态/证言视觉变体（可加 Logo） | ✓ | — | — |
| Scenarios | 2 | 11 | 能力 Tab | — | — | — |
| Solution | 6 | 12 | 首屏/多栏/大卡/步骤/对比/动态/证言 | ✓ | — | agency 含 `canvas-wall` |
| Landing Page | 7 | 12～15 | Hero / 卡片位 / 对比 / 动态 / 社会证明 / 定价 | 仅 `landing-full` + `landing-offer-close` | `landing-trial-now` + `landing-full` | ✓ |

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
| [landing-storylines.json](./landing-storylines.json) | Landing 7 条故事线 SSOT（**含 copy 文案绑定**） |
| [solution-storylines.json](./solution-storylines.json) | Solution 故事线 SSOT（含 `copyDefault`） |
| [scenarios-storylines.json](./scenarios-storylines.json) | Scenarios 故事线 SSOT（含 `copyDefault`） |
| [page-copy-bindings.json](./page-copy-bindings.json) | feature/tool/product/topic 文案绑定 + master intent 词汇 + intentCrosswalk |
| [COPY-PREFLIGHT.md](./COPY-PREFLIGHT.md) | 文案验收清单（从上面绑定 storyline-driven 派生） |
| [LANDING-PRODUCTION-2026-06-07.md](./LANDING-PRODUCTION-2026-06-07.md) | Landing Page 投放生产指南 + 参考案例 |
| [STORYLINES.md](./STORYLINES.md) | 早期短链示例（F1/T1）；topic K1/K2 结构仍以此为准 |
| FULL-STORYLINE-* | ⚠️ 已过时，勿用 |

> **结构 × 文案同源**：每条故事线既定义 section 顺序（结构），又通过 `copy` / `copyDefault` 绑定定义 intent / hero / proof / cta / faq / benchmark（文案）。文案写作意图见 [`landing-copy-constraints-ssot.md`](../../../1-1%20Harness/Skills/02-creation/lovart-landing-page/references/landing-copy-constraints-ssot.md)。
