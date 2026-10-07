# 情景 × 组件组合菜谱

> 修订：2026-05-31  
> **短链示例**（F1/T1…）见下文。  
> **故事线权威来源**：[PAGE-MODULE-MATRIX.md](./PAGE-MODULE-MATRIX.md)（官网改版 PDF）。  
> 短链示例（F1/T1…）见下文。README 组件字典见 [README.md](./README.md)；旧版升级见 [LEGACY-MIGRATION.md](./LEGACY-MIGRATION.md)。

---

## 一、按页面类目

### A1. Feature（`category: feature`）

| 编号 | 情景 | 叙事 | 模块序列 |
|------|------|------|----------|
| **F1** | 标准 AI 功能（现网约 69% 五段式） | 试用 → 三步 → 能力 → 信任 → FAQ | `prompt-launcher` → `workflow-horizontal` → `feature-grid` → `testimonial` → `faq` → `cta-default` |
| **F2** | 品牌感强的模型页 | 震撼 → 试用 → 深度 | `hero-cinematic` → `prompt-launcher` → `capability-tabs` → `comparison-table` → `faq` → `cta-default` |
| **F3** | 视频 / 多模态 | 结果 → 流程 → 场景 | `hero-split` → `showcase-horizontal` → `workflow-vertical` → `media-marquee` → `faq` |
| **F4** | 编辑 / 修图类 | 前后对比 → 操作 → 案例 | `hero-split` → `comparison-before-after` → `feature-detail` → `canvas-wall` → `faq` |
| **F5** | 行业垂直（餐饮、房产等） | 痛点 → 产出物 → 案例 | `hero-journey` → `portrait-grid-3` → `showcase-stacked` → `review-grid-3col` → `faq` |
| **F6** | 工具矩阵 / Nano 系 | 多入口 → Agent | `hero-gallery` → `tool-grid` → `proof-block` → `faq` |
| **F7** | Agent 全链路 | 旅程 → 细节 → 数据 | `hero-journey` → `feature-detail` → `workflow-vertical` → `stats` → `cta-default` |

### A2. Tool（`category: tool`）

| 编号 | 情景 | 叙事 | 模块序列 |
|------|------|------|----------|
| **T1** | 标准工具（现网长链 7–9 段） | 即用 → 说明 → 步骤 → 图文 → 证言 | `prompt-launcher` → `bento-2` → `workflow-horizontal` → `feature-detail` → `testimonial` → `faq` → `cta-default` |
| **T2** | 单点效用、步骤少 | 快懂快用 | `hero-split` → `comparison-before-after` → `workflow-horizontal` → `faq` |
| **T3** | 工具合集 / 目录 | 选型 | `hero-cinematic` → `tool-grid` → `comparison-table` → `cta-default` |
| **T4** | 竞品对比 | 决策 | `hero-split` → `comparison-table` → `proof-block` → `review-grid-4col` → `faq` |
| **T5** | 重 SEO、轻交互 | 阅读型 | `hero-cinematic` → `feature-grid` → `blog-grid` → `faq` |
| **T-long** | 线上 reflow 扩展链（≥12 sections） | 全漏斗长页 | 以 production 为准；本地 `sync-tools-from-production` 自动标注 |

### A3. Product（`category: product`）

| 编号 | 模块序列 |
|------|----------|
| **P1** | `hero-split` → `showcase-stacked` → `portrait-grid-4` → `stats` → `pricing-block` → `faq` |
| **P2** | `hero-cinematic` → `bento-4` → `capability-tabs` → `logo-loop` → `cta-default` |
| **P3** | `hero-gallery` → `canvas-wall` → `tool-grid` → `cta-default` |

### A4. Solution（`category: solution` · 6 条 · 各 12 段）

> 权威序列见 [solution-storylines.json](./solution-storylines.json) 与 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.5。

| 编号 | 故事线 ID | 主轴 | 适用 | 完整 `type` 序列 |
|------|-----------|------|------|------------------|
| **S1** | `solution-team` | 人群 | 营销团队、创业公司 | `hero-cinematic → bento-4 → capability-tabs → bento-2 → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` |
| **S2** | `solution-ecommerce` | 行业 | Shopify、DTC、电商 | `hero-journey → bento-4 → capability-tabs → bento-2 → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → review-grid-3col → pricing-block → faq → cta-default` |
| **S3** | `solution-agency` | 人群 | 代理商、工作室 | `hero-mosaic → bento-4 → capability-tabs → feature-detail → workflow-horizontal → comparison-table → cluster-block-dense → canvas-wall → review-grid-4col → pricing-block → faq → cta-default` |
| **S4** | `solution-enterprise` | 人群 | 大企业、全球团队 | `hero-cinematic → bento-6 → capability-tabs → feature-detail → workflow-vertical → comparison-table → cluster-block-dense → showcase-horizontal → review-grid-3col → pricing-block → faq → cta-default` |
| **S5** | `solution-solo` | 人群 | 自由职业、个体户、小商家 | `hero-split → bento-4 → capability-tabs → bento-2 → workflow-horizontal → comparison-before-after → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` |
| **S6** | `solution-mission` | 行业 | 非营利、使命驱动 | `hero-journey → bento-4 → capability-tabs → bento-2 → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` |

### A5. Scenario（`category: scenario`）

| 编号 | 模块序列 |
|------|----------|
| **C1** | `hero-journey` → `showcase-horizontal` → `feature-detail` → `faq` |
| **C2** | `hero-cinematic` → `portrait-grid-4` → `cluster-block-dense` → `blog-grid` |
| **C3** | `hero-split` → `media-marquee` → `bento-6` → `cta-default` |

### A6. Topic（`category: topic`）

| 编号 | 模块序列 |
|------|----------|
| **K1** | `hero-cinematic` → `blog-grid` → `tool-grid` → `faq` |
| **K2** | `hero-split` → `workflow-vertical` → `capability-tabs` → `blog-grid` |

---

## 二、按营销叙事（跨类目）

| 编号 | 叙事 | 模块序列 |
|------|------|----------|
| **N1** | AIDA | `hero-*` → `proof-block` / `stats` → `feature-detail` → `cta-default` |
| **N2** | 问题 - 方案 - 证明 | `cluster-block-dense` → `capability-tabs` → `testimonial` → `faq` |
| **N3** | 前后对比 | `hero-split` → `comparison-before-after` → `showcase-stacked` → `cta-default` |
| **N4** | 社会证明 | `logo-loop` → `review-grid-4col` → `media-marquee` → `cta-default` |
| **N5** | 价格转化 | `hero-split` → `pricing-block` → `comparison-table` → `faq` → `cta-default` |
| **N6** | 内容 + 转化 | `blog-grid` → `prompt-launcher` → `cta-default` |

---

## 三、首屏 Hero 怎么选

| 首屏目标 | 首选 | 常配第二屏 |
|----------|------|------------|
| 立即试用 / 输入 | `prompt-launcher`（或 `hero-split` + launcher） | `workflow-horizontal` |
| 品牌 / 电影感 | `hero-cinematic` | `logo-loop` |
| 多步骤旅程 | `hero-journey` | `workflow-vertical` |
| 多能力拼贴 | `hero-mosaic` | `feature-detail` |
| 多工具入口 | `hero-gallery` | `tool-grid` |

---

## 四、现网骨架 → 默认升级模板

| 现网序列（抽样统计） | 默认菜谱 |
|----------------------|----------|
| Features：`centeredInput → threeColumn → featureGrid → testimonial → faq` | **F1** |
| Tools：`hero → content → threeColumn → textImage × N → faq` | **T1**；多段 textImage 可考虑 **T2** + `comparison-before-after` |
| 末尾含 `ctaSection` | 统一加 **`cta-default`** |

---

## 五、实战记录（使用时填写）

| 日期 | 情景编号 | slug | 采用 / 调整 | 备注 |
|------|----------|------|-------------|------|
| 2026-06-07 | S2 | `ai-design-solution-for-shopify` | `solution-ecommerce` | 电商行业范例 |
| 2026-06-07 | S1 | `ai-design-solution-for-marketing-teams` | `solution-team` | 团队型人群范例 |
| 2026-06-07 | S3 | `ai-design-solution-for-agencies` | `solution-agency` | 代理商范例 |
