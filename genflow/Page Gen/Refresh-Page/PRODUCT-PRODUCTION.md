# Product 页面生产指南

> 依据 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.3 四条 Product 故事线。  
> **英文参考案例**：[`Pages/Products/en/`](../Pages/Products/en/)

---

## 一、动笔前先定三件事

Product 页不是「把功能说明书写长」——同一套 Lovart 能力，**流量目的、内容维度、叙事立场**不同，页型与模块权重就不同。

### 1.1 流量目的：官网 SEO vs 投放

| 维度 | **官网 / SEO 产品页** | **投放 / 高意图落地页** |
|------|----------------------|-------------------------|
| 主要目标 | 收录、品牌词/品类词排名、站内导航枢纽 | 转化、Quality Score、广告一致性 |
| 典型 URL | `/product/{slug}`，长期可索引 | 同上或 campaign slug；常 `noIndex` 测完再开 |
| 信息深度 | 完整 12～13 段：Tab、对比、FAQ、**定价** | 可压缩：强化首屏 + 前后对比 + 单 CTA；FAQ 精简 |
| 社会证明 | `logo-loop`、证言、评测格（含社会证明线） | 证言 / before-after 前置；Logo 条可选 |
| 故事线倾向 | `product-标准` / `product-含社会证明` | `product-视觉扩展-B`（`comparison-before-after`、`showcase-horizontal`） |
| SEO | 完整 `title` / `description` / `keywords` / 内链到 Features·Tools | 标题对齐广告组；可牺牲长尾 FAQ 数量 |

**规则：** 先写 **SEO  canonical 版**（案例 A/B 即此类），投放版从 canonical **删段、换序 1/6/8、加重对比**，不要反过来从投放页扩成 SEO 页。

### 1.2 内容维度：能力 · 特色 · 功能

同一 Product 页里，三类信息**都要出现**，但**主次因页而异**：

| 维度 | 是什么 | 典型例子 | 优先落在哪些 section |
|------|--------|----------|----------------------|
| **产品能力** | 平台级、跨场景的基础力 | ChatCanvas 空间工作流、Agent 规划、多模态生成 | `hero-cinematic`、`capability-tabs`、`workflow-vertical` |
| **产品特色** | 差异化、难被一句话替代的卖点 | Brand Kit 治理、Style Consistency、MCoT 推理 | `bento-4`、`comparison-table`、`cluster-block-dense` |
| **产品功能** | 可点名、可连到 Tools/Features 的入口 | Touch Edit、Mockup、Image Generator | `tool-grid`、`showcase-stacked` 内链 |

**写法：**

- **能力** → 讲「为什么需要这个产品形态」，偏叙事与步骤。
- **特色** → 讲「和旧工作流 / 竞品差在哪」，偏对比与证言。
- **功能** → 讲「点哪里、出什么」，偏网格与案例动图；链到 `/tools/`、`/features/`。

### 1.3 表达难度：直观 vs 需展开

| 类型 | 特征 | 模块策略 |
|------|------|----------|
| **直观型** | 一眼能懂（Touch Edit 点选、Mockup 贴图） | `showcase-stacked` / `showcase-horizontal` 大图优先；`bento-4` 短句；Tab 可少 |
| **需展开型** | 一两句说不清（Agent 上下文、Brand Kit 治理链、MCoT） | `capability-tabs` 分四层；`workflow-vertical` 分步；`comparison-table` 定锚；FAQ 加长 |

**同一页可混合：** 序 2 `bento-4` 放直观功能，序 3 `capability-tabs` 展开难讲清的能力链（案例 B Brand Kit 即此结构）。

---

## 二、与 Solution、Scenario 的边界

**题材可以重叠**（都在讲电商、都在讲品牌一致性），**页型不同 = 立场与叙事结构不同**：

| 页型 | 读者立场 | 叙事主轴 | 你卖的是什么 | 典型禁用/慎用 |
|------|----------|----------|--------------|---------------|
| **Product** | 「这个产品是什么、值不值得买」 | 产品线总览 → 能力 Tab → 工具矩阵 → **定价** | **Lovart 某一产品/模块**（ChatCanvas、Brand Kit） | 少讲「你的行业一周怎么过」；不用 `prompt-launcher` |
| **Scenario** | 「我这种工作场景能不能用」 | 场景痛点 → 子场景 Tab → 落地步骤 → 案例 | **某职业/流程下的用法**（电商运营、社媒经理） | 无 `pricing-block`、无 `tool-grid` |
| **Solution** | 「整套方案能不能替我们团队」 | 方案包 → 保障/对比 → 人群或行业轴 | **组合售卖 / 组织级方案**（Shopify 增长包、代理工作流） | 同 Product 可有定价，但 Hero 讲「方案结果」非单点功能 |

**何时仍用 Product 而非 Scenario/Solution：**

- 要讲 **Lovart 产品名本身**（ChatCanvas、Brand Kit、Thinking Mode）→ Product  
- 要讲 **某角色的一周**（freelance designer、ecommerce operator）→ Scenario  
- 要讲 **按行业/团队打包的采购理由**（Shopify 全漏斗、agency 多客户）→ Solution  

若内容偏场景但 URL 必须在 `/product/`，则 **立场仍保持产品说明书**：场景只出现在 `cluster-block-dense` / `showcase-*` 作例证，Hero 不写成「电商运营指南」。

---

## 三、选型决策树（制作人用）

```
1) 流量目的？
   ├─ 官网 SEO / 站内枢纽 → 12～13 段 + 完整 FAQ + pricing-block
   └─ 投放 / 广告落地 → 视觉扩展 B 或删段；首屏+对比+底 CTA 加权

2) 主维度？
   ├─ 能力型（平台/工作流）→ workflow-vertical + capability-tabs 加重
   ├─ 特色型（差异化治理/Agent）→ comparison-table + testimonial + logo-loop
   └─ 功能型（可连 Tools）→ tool-grid + showcase-stacked 加重

3) 表达难度？
   ├─ 直观为主 → showcase-* / bento-4 前置，Tab 2～3 个即可
   └─ 需展开 → capability-tabs 4 层 + workflow-vertical + FAQ 6+ 条

4) 与 Scenario/Solution 是否撞题？
   └─ 撞题但立场是「产品名」→ 保留 Product；场景改为例证块，Hero 写产品价值
```

---

## 四、故事线与模块权重

### 4.1 四条故事线（section 顺序）

| 故事线 ID | 完整 `type` 顺序 | 适用 |
|-----------|------------------|------|
| `product-标准` | `hero-cinematic → bento-4 → capability-tabs → tool-grid → workflow-vertical → comparison-table → cluster-block-dense → showcase-stacked → testimonial → pricing-block → faq → cta-default` | **SEO 基准**；能力+功能均衡 |
| `product-含社会证明` | 同上，在 `showcase-stacked` 与 `testimonial` 之间加 **`logo-loop`** | 特色型、需信任背书（Brand Kit、Team） |
| `product-视觉扩展-A` | `hero-gallery → portrait-grid-3 → … → blog-grid → feature-detail → logo-loop → review-grid-3col → …` | 功能入口多、偏内容化 SEO |
| `product-视觉扩展-B` | `hero-split → … → comparison-before-after → showcase-horizontal → logo-loop → review-grid-4col → …` | **投放向**、直观 before/after |

**Product 禁用：** `prompt-launcher`、页内 mid-page `cta-default`（仅保留底部）、`canvas-wall`；标准线禁用 `feature-detail`（扩展 A 除外）。

### 4.2 按流量目的调权重（不改 type 顺序时）

| Section | SEO 官网 | 投放落地 |
|---------|----------|----------|
| Hero | 品类词 + 产品名 + 长期价值句 | 广告组同款 headline + 单 CTA |
| `bento-4` | 能力/特色/功能各 1 格 | 只保留 2～4 个最强卖点 |
| `comparison-table` | vs 旧工作流 / 竞品 | vs 「不用 Lovart」或单点工具 |
| `faq` | 6～8 条，覆盖 SEO 长尾问 | 3～4 条，消异议 |
| `pricing-block` | 保留 | 可简化为一句 + 链到定价页 |

---

## 五、两条起步案例（对照表）

| | **案例 A** | **案例 B** |
|---|------------|------------|
| 文件 | [`chatcanvas-en.json`](../Pages/Products/en/chatcanvas-en.json) | [`brand-kit-en.json`](../Pages/Products/en/brand-kit-en.json) |
| 故事线 | `product-标准`（12 段） | `product-含社会证明`（13 段） |
| 流量目的 | **官网 SEO** 产品页 | **官网 SEO** + 信任背书 |
| 主维度 | **产品能力**（空间工作流 / Agent 画布） | **产品特色**（品牌治理 / Style Consistency） |
| 表达难度 | **需展开**（Tab 四层 + 竖向步骤） | **混合**（bento 直观 + Tab 讲治理链） |
| 与 Scenario 边界 | 场景只出现在 `cluster-block-dense` 例证 | 行业只作证言角色，Hero 仍是 Brand Kit 产品名 |
| 教制作人什么 | 能力型 + 标准线 + tool-grid 连 Tools | 特色型 + logo-loop + 对比表定锚 |

两篇均为 **`seo.noIndex: true`** 参考稿；上线 SEO 版时改 `false` 并补唯一配图。

**投放向改稿示例（从案例 B 出）：** 换 `product-视觉扩展-B`，Hero 改 `hero-split`，序 6 改 `comparison-before-after`，删 FAQ 至 4 条，保留底 CTA。

---

## 六、Product 与 Features / Tools 的区别

| 维度 | Product | Features | Tools |
|------|---------|----------|-------|
| `category` | `product` | `feature` | `tool` |
| URL | `/product/{slug}` | `/features/{slug}` | `/tools/{slug}` |
| 叙事 | 产品线 → Tab → 工具矩阵 → 步骤 → 对比 → **定价** | 单能力 → 试用 → 步骤 | 即用 → 步骤 → 长文 |
| 禁用 | `prompt-launcher`、页内 CTA、`canvas-wall`；标准线禁 `feature-detail` | — | 证言、定价 |

---

## 七、JSON 字段 checklist

```json
{
  "_type": "compositePage",
  "category": "product",
  "slug": "your-product-slug",
  "title": "Page title",
  "description": "Sanity list preview + meta fallback",
  "storyline": "product-标准",
  "bodyJson": "[{...}]",
  "seo": { "title": "...", "description": "...", "keywords": [], "noIndex": true, "ogImage": {...} },
  "language": "en",
  "schemaVersion": "composite-v2",
  "url_path": "/product/your-product-slug",
  "section": [{ "...same as bodyJson parsed..." }]
}
```

- **`storyline`** 必须与 section `type` 序列一致（§4.1）。
- **`bodyJson`** 与 **`section`** 内容相同。
- 组件字段见 [README.md](./README.md)；示例见 [preview-data.json](./preview-data.json)。

---

## 八、生产步骤

1. **定 §一 三件事** — 流量目的、主维度、表达难度；必要时对照 §二 确认不是 Scenario/Solution。
2. **选故事线** — SEO 默认 `product-标准` / `product-含社会证明`；投放见 §4.1 扩展 B。
3. **复制案例** — 能力型复制 A，特色型复制 B。
4. **改元数据** — `slug`、`title`、`description`、`url_path`、`storyline`、`seo`。
5. **按维度填 section** — 能力→Tab/步骤；特色→对比/证言；功能→tool-grid/showcase。
6. **换图** — 直观块用大动图/前后图；难讲块用分步示意图。
7. **预检** — `preflight-content.js --type composite-v2 --dir "../Pages/Products/en"`。
8. **导入** — Sanity `category: product`；SEO 版 `noIndex → false`。

---

## 九、本地目录

| 路径 | 说明 |
|------|------|
| `Pages/Products/en/` | 英文 SSOT |
| `Pages/Products/{lang}/` | 多语言（结构对齐 EN） |

```bash
node "1-3 Content Gen/Page Gen/Pages/Products/en/_build-examples.js"
```

---

## 十、相关文档

| 文件 | 内容 |
|------|------|
| [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.3–4.5 | Product / Scenario / Solution 故事线 |
| [FEATURES-PRODUCTION.md](./FEATURES-PRODUCTION.md) | Features 生产流水线 |
| [SCOPE.md](./SCOPE.md) | compositePage 六类范围 |
