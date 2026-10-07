# 官网改版 · 各类新增页面模块对照一览表

> **来源**：`/Users/seveno/Downloads/官网改版各类新增页面模块对照一览表.pdf`（飞书导出）  
> **修订**：2026-05-31  
> **地位**：**开发前**结构参考（六大类、槽位、顺序）。**不是**上线变体定义。  
> 格子里的 1、2、3… 为旧设计稿序号，**勿写入故事线或 JSON**。  
> 模块与变体以 [README-MODULE-VARIANTS.md](./README-MODULE-VARIANTS.md) 为准。

---

## 0. PDF 顶部说明（原文）

| 时间 | 要求 |
|------|------|
| 今天下午 | 按**具体场景**填内容；做**一个最全落地页** + JSON + **最全 demo**；**Hero 区分**；模块最好加备注 |
| 今晚 | **首屏**；**Product** 和 **Solution** 找 R 老师 |

**解读：**

- 「场景」= 下表 **6 种页面类型**（列），不是 Sanity 里另造的 O1–O4。
- 「最全落地页」= 模块行里**尽量都有对应变体**；各场景列决定**用哪几个模块、用第几号变体**。
- 单元格里的 **数字 = 该模块在该页面类型下的变体编号**（设计稿序号），**不是** section 在页内的排序号。
- **模块在页内的顺序 = 下表从上到下的行顺序**（有数字或缩略图则启用；空白或 ❎ 则该场景**不用**此模块）。

---

## 1. 六种页面类型（列）

| 列 | 页面类型 | 备注 |
|----|----------|------|
| C1 | **Product** | |
| C2 | **Features** | |
| C3 | **Scenarios** | PDF 表头**黄色高亮**（优先场景） |
| C4 | **Solution** | PDF 表头**黄色高亮**（优先场景） |
| C5 | **Tools** | |
| C6 | **Landing Page** | |

与 Sanity `category` 大致对应：`product` / `feature` / `scenario` / `solution` / `tool`；**Landing Page** 在 Sanity 侧需确认是否单独 category 或某类子型。

---

## 2. 十七种模块本体（行，固定顺序）

| 行序 | PDF 模块名 | 说明 |
|------|------------|------|
| 1 | **Hero Banner** | 首屏；各场景均用变体 **1**（PDF 仅展示 1 号，Hero 仍须在 demo 里**区分**多种 Hero 设计） |
| 2 | **Multi columns** | 多栏内容块 |
| 3 | **Tab Card** | Tab 切换卡 |
| 4 | **Card Grid** | 卡片网格 |
| 5 | **Feature Card** | 特性大卡 |
| 6 | **Gallery** | 图库 / 展示墙 |
| 7 | **Try Prompt** | 试用输入 |
| 8 | **Photo loop** | 图片/Logo 循环条 |
| 9 | **CTA** | 页内 CTA（非底部） |
| 10 | **How-tos** | 步骤 / 教程 |
| 11 | **vs table** | 对比表 / 前后对比 |
| 12 | **Content Cluster** | 内容簇 / 聚合块 |
| 13 | **Dynamic Content** | 动态内容 / 图文块 |
| 14 | **Testimonial** | 证言 |
| 15 | **Pricing Table** | 定价 |
| 16 | **FAQ** | 问答 |
| 17 | **Bottom CTA** | 底部收口 CTA |

**共 17 个模块槽位**（不是 README 的 33 种 `type`，也不是 20 段 One-each）。

---

## 3. 对照矩阵：各场景用哪号变体

**图例：** 数字 = 使用该模块的**变体编号**；`—` = 该场景**不出现**此模块；`❎` = 明确禁用。

| 行序 | 模块 | Product | Features | Scenarios | Solution | Tools | Landing Page |
|------|------|---------|----------|-----------|----------|-------|--------------|
| 1 | Hero Banner | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | Multi columns | 2 | 3 | 2 | 2 | 2 | 2 |
| 3 | Tab Card | 3 | 2 | **3、9** | — | — | 6 |
| 4 | Card Grid | 4 | — | — | — | — | 5 |
| 5 | Feature Card | ❎ | 4 | 6 | 3 | 3 | 8 |
| 6 | Gallery | — | — | — | — | — | 9 |
| 7 | Try Prompt | — | — | — | — | 6 | — |
| 8 | Photo loop | ✓* | — | — | — | 7 | — |
| 9 | CTA | — | — | — | — | 8 | — |
| 10 | How-tos | 5 | 4 | 4 | 5 | 4 | 4 |
| 11 | vs table | 6 | 7 | 6 | 9 | 3 | 10 |
| 12 | Content Cluster | 7 | 5 | 5 | 4 | **4、12** | 7 |
| 13 | Dynamic Content | 10 | 6 | 8 | 10 | 11 | ✓* |
| 14 | Testimonial | ✓* | 8 | 8 | 7 | — | — |
| 15 | Pricing Table | ✓* | 9 | — | 11 | — | — |
| 16 | FAQ | — | 11 | 10 | 9 | 13 | 12 |
| 17 | Bottom CTA | — | 12 | 11 | 10 | 14 | 13 |

\* **✓\***：PDF 该格**有缩略图但无数字** — 表示**有变体但未编号**。**禁止当作变体 1**；须按 [STORYLINE-DERIVATION.md](./STORYLINE-DERIVATION.md) **派生独立故事线**（如 Product 的 Photo loop / Testimonial / Pricing；Landing 的 Dynamic Content）。

**双数字 = 两条故事线（不是同一页叠两段）：**

- **Scenarios · Tab Card**：变体 **3** 与 **9** → `SC-基准` / `SC-派生-tab9`
- **Tools · Content Cluster**：变体 **4** 与 **12** → `T-基准` / `T-派生-cluster12`

完整派生清单见 **[STORYLINE-DERIVATION.md](./STORYLINE-DERIVATION.md)**。

---

## 4. 各方向模块序列（概要）

**完整故事线（含基准 + 派生）见 [STORYLINE-DERIVATION.md](./STORYLINE-DERIVATION.md)。**  
下列仅为有号段的**骨架摘要**；双数字 / 无号格请打开派生文档。

### Product

`Hero¹ → Multi² → Tab³ → CardGrid⁴ → How⁵ → vs⁶ → Cluster⁷ → Dynamic¹⁰ → Testimonial* → Pricing* → …`  
（无 Feature Card、Gallery、Try Prompt、FAQ、Bottom CTA 等 — 以 PDF 空白为准）

### Features

`Hero¹ → Multi³ → Tab² → Feature⁴ → How⁴ → vs⁷ → Cluster⁵ → Dynamic⁶ → Testimonial⁸ → Pricing⁹ → FAQ¹¹ → BottomCTA¹²`

### Scenarios

- **SC-基准**：Tab【3】…（见 STORYLINE-DERIVATION）
- **SC-派生-tab9**：Tab【9】…（其余同基准）

### Solution

`Hero¹ → Multi² → Tab³ → Feature³ → How⁵ → vs⁹ → Cluster⁴ → Dynamic¹⁰ → Testimonial⁷ → Pricing¹¹ → FAQ⁹ → BottomCTA¹⁰`

### Tools

- **T-基准**：Cluster【4】…
- **T-派生-cluster12**：Cluster【12】…

### Landing Page

`Hero¹ → Multi² → Tab⁶ → CardGrid⁵ → Feature⁸ → Gallery⁹ → How⁴ → vs¹⁰ → Cluster⁷ → Dynamic* → FAQ¹² → BottomCTA¹³`

---

## 5. PDF 模块 ↔ Refresh-Page `type`（待前端确认）

| PDF 模块 | 可能对应的 v2 `type` | 备注 |
|----------|---------------------|------|
| Hero Banner | `hero-split` / `hero-cinematic` / …（5 种） | PDF 变体 1–N 与设计稿绑定，**不是** README 里 5 type 一一等于变体 1–5 |
| Multi columns | `bento-2` · `portrait-grid-*` · `feature-grid` | 待对照设计稿 |
| Tab Card | `capability-tabs` | |
| Card Grid | `tool-grid` · `bento-*` | |
| Feature Card | `bento-*` · `feature-detail` | |
| Gallery | `canvas-wall` · `showcase-*` · `hero-gallery` | |
| Try Prompt | `prompt-launcher` | |
| Photo loop | `logo-loop` · `media-marquee` | |
| CTA / Bottom CTA | `cta-default` | 页内 CTA 与 Bottom 可能同 type、不同文案 |
| How-tos | `workflow-horizontal` · `workflow-vertical` | |
| vs table | `comparison-table` · `comparison-before-after` | |
| Content Cluster | `cluster-block-dense` · `blog-grid` | |
| Dynamic Content | `feature-detail` · `showcase-*` | |
| Testimonial | `testimonial` · `review-grid-*` | |
| Pricing Table | `pricing-block` | |
| FAQ | `faq` | |

**结论：** Refresh-Page README 是 **JSON 字段字典**；本 PDF 是 **页面结构 + 设计变体编号**。两者必须通过上表 **join**，不能直接用 README 的 7 组变体 × 1200 组合替代 PDF。

---

## 6. 与此前本地文档的差异（必读）

| 项目 | 此前 `FULL-STORYLINE-*` | 本 PDF |
|------|-------------------------|--------|
| 模块集合 | README 33 type / 20 段 One-each | **17 模块本体** |
| 变体含义 | 同 `##` 标题下互斥 type | **设计稿变体编号 1–14+** |
| 变体数量 | 误算 1200 笛卡尔积 | **每模块每场景指定一个（或两个）编号** |
| 叙事 / 顺序 | 自拟 O1–O4 或 STORYLINES F1 | **6 场景列 + 行序** |
| 故事线总数 | 9,600（O×V） | **6 条主故事线** + 少量双变体格 + Hero/待确认格 |

---

## 7. 建议的后续（按 PDF 原文）

1. **做一个最全落地页 + JSON + demo**（今天下午要求）— 建议以 **Landing Page** 或模块最全的一列为主干。  
2. **Hero 区分** — 5 种 Hero 设计单独备注，不与 PDF 单元格「1」混为一谈。  
3. **Product / Solution 首屏** — 找 R 老师（今晚）。  
4. 在本地用 `F-Features-V{模块}-{变体号}` 或 `features-scenarios-tab3` 等命名生成 JSON，**对齐本表**，不再用 `F-O1-V0042` 体系。  
5. 完成映射后，再写「用途 + 物料 checklist」。

---

## 8. 相关文件

| 文件 | 状态 |
|------|------|
| [FEISHU-REQ-GAP.md](./FEISHU-REQ-GAP.md) | 已可对照 §3 更新 |
| [FULL-STORYLINE-CATALOG.md](./FULL-STORYLINE-CATALOG.md) | ⚠️ 基于 README，**应降级为 JSON 字典索引** |
| [FULL-STORYLINE-ORDERS.md](./FULL-STORYLINE-ORDERS.md) | ⚠️ O1–O4 **作废**，以本文 §4 为准 |
| [FULL-STORYLINE-VARIANTS.md](./FULL-STORYLINE-VARIANTS.md) | ⚠️ 1200 组合 **与 PDF 无关**，勿用于上线选型 |
