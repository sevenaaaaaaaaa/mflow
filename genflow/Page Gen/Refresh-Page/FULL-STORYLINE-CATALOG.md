# 全槽位故事线清单

> ⚠️ **本文基于 Refresh-Page README 推导，已不是故事线权威来源。**  
> 请以 **[PAGE-MODULE-MATRIX.md](./PAGE-MODULE-MATRIX.md)**（官网改版 PDF）为准。

> 修订：2026-05-31  
> **唯一依据**：[README.md](./README.md) 的组件分组与 Variants 面板说明。  
> 本文**不**改 JSON、**不**改现网页面。

---

## 0. 先前错在哪里（说明）

之前把 README 里的结构搞混了，主要错误：

1. **自创了 S01–S20「槽位」**，与原始文档的「组件大类 / 33 种 type」对不上。  
2. **让人以为每个模块都有 5 个变体**——实际上 README 里**只有 2 个组件大类是 5 变体**（Hero、Bento/网格/Cluster），其余大多是**独立模块（只有 1 种 type）**，或 2–3 变体。

以下全部按 README 原文整理。

---

## 1. README 里的两种概念（必读）

| 概念 | README 怎么说 | 一页里怎么用 |
|------|---------------|--------------|
| **33 种 `type`** | 组件清单共 33 种，每种有固定字段 | 预览页 **Show all** 时 33 段全展开（给开发验收用） |
| **组件大类 + 变体** | Variants 面板 **One each**：**每个大类只显示 1 个变体** | 真实落地页：每个**有多变体的大类**选 1 个 type；**无变体的模块**固定 1 种 type |

**故事线**在落地页语境下指：

```
选哪些模块（大类）→ 有变体的大类选哪个 type → 按哪种营销叙事顺序排列
```

---

## 2. 组件大类与变体（严格摘自 README）

README `# 组件清单（33 种）` 按 `##` 分组如下。**「变体」仅指同一 `##` 标题下互斥、择一使用的 type。**

| README 分组 | 变体数 | 可选 `type`（择一或固定） |
|-------------|--------|---------------------------|
| **Hero 区（5 种）** | **5** | `hero-split` · `hero-cinematic` · `hero-journey` · `hero-mosaic` · `hero-gallery` |
| **Bento / 网格 / Cluster（5 种）** | **5** | `bento-2` · `bento-4` · `bento-6` · `feature-grid` · `cluster-block-dense` |
| **Tabs / Tool / Blog / 详情** | 各 **1** | `capability-tabs` · `tool-grid` · `blog-grid` · `feature-detail` · `canvas-wall`（5 个**独立模块**，不是彼此的变体） |
| **Portrait Grid（2 种）** | **2** | `portrait-grid-3` · `portrait-grid-4` |
| **Showcase（2 种）** | **2** | `showcase-stacked` · `showcase-horizontal` |
| **跑马灯 / 输入 / Logo（3 种）** | 各 **1** | `media-marquee` · `prompt-launcher` · `logo-loop`（3 个**独立模块**） |
| **CTA / 流程（3 种）** | 混合 | `cta-default`（1 种）· `workflow-horizontal` / `workflow-vertical`（流程 **2 变体，择一**） |
| **对比（2 种）** | **2** | `comparison-table` · `comparison-before-after` |
| **证言 / 评价（3 种）** | **3** | `testimonial` · `review-grid-3col` · `review-grid-4col` |
| **数据 / 信任 / 价格 / FAQ（4 种）** | 各 **1** | `stats` · `proof-block` · `pricing-block` · `faq` |

### 2.1 小结：谁有变体、谁没有

**有多变体、需择一的大类（共 7 组）：**

| 大类 | 变体数 |
|------|--------|
| Hero | 5 |
| Bento / 网格 / Cluster | 5 |
| Portrait Grid | 2 |
| Showcase | 2 |
| 流程（workflow） | 2 |
| 对比 | 2 |
| 证言 / 评价 | 3 |

**无变体、type 固定的大类（共 13 个模块）：**  
`capability-tabs` · `tool-grid` · `blog-grid` · `feature-detail` · `canvas-wall` · `media-marquee` · `prompt-launcher` · `logo-loop` · `cta-default` · `stats` · `proof-block` · `pricing-block` · `faq`

### 2.2 「满配页」有多少段？

按 Variants **One each** 逻辑（每个大类出现一次）：

```
7 个有变体的大类（各出 1 段）+ 13 个固定模块 = 20 段 section
```

不是 33 段同时出现在同一页——33 是 **Show all 预览** 用的总数（含同一大类下的多个变体同时展示）。

---

## 3. 变体组合有多少种

只有上面 **7 组**参与相乘，其余 13 个模块 type 固定：

```
5 × 5 × 2 × 2 × 2 × 2 × 3 = 1,200 种变体组合
```

编号 **V0001 … V1200**（见 [FULL-STORYLINE-VARIANTS.md](./FULL-STORYLINE-VARIANTS.md)，仅列这 7 列择一结果）。

---

## 4. 叙事顺序

**不再使用**此前自拟的 O01–O10（来自 STORYLINES 短链）。

叙事顺序**仅**摘自 README 原文，见 **[FULL-STORYLINE-ORDERS.md](./FULL-STORYLINE-ORDERS.md)**：

| 编号 | 名称 | README 依据 |
|------|------|-------------|
| **O1** | 预览默认顺序 | `preview-data.json` + Variants 面板（README L19–29） |
| **O2** | 组件清单文档顺序 | `# 组件清单` 各 `##` 标题顺序（L94–669） |
| **O3** | 产品流程叙事 | Showcase 章节「"产品流程"叙事」（L395）+ 流程组件 |
| **O4** | 落地页收口语序 | `hero-journey` journeyCards step 02 + `faq`→`cta-default` 收口 |

故事线编号：`F-O1-V0042` = Feature · 叙事 O1 · 变体 V0042。

**故事线总数：**

| | 数量 |
|--|------|
| 叙事 O | **4** |
| 变体 V | 1,200 |
| Feature | **4,800** |
| Tool | **4,800** |
| **合计** | **9,600** |

---

## 5. 故事线怎么选

- **O**： [FULL-STORYLINE-ORDERS.md](./FULL-STORYLINE-ORDERS.md) 选 O1–O4  
- **V**： [FULL-STORYLINE-VARIANTS.md](./FULL-STORYLINE-VARIANTS.md) 选 V0001–V1200  
- 把 O 序列中的 `hero*` 等替换为 V 中具体 `type` → 完整 `bodyJson` type 顺序

---

## 6. 勾选表（你来填）

| ☐ | 编号 | 说明 |
|---|------|------|
| ☐ | | |
| ☐ | | |
| ☐ | | |

---

## 7. 下一步

1. 确认 **O1–O4** 是否覆盖你需要的叙事；README 若补充新说明，在 [FULL-STORYLINE-ORDERS.md](./FULL-STORYLINE-ORDERS.md) 追加 O5…  
2. **O2（文档顺序）** 中 `cta-default` 在 `faq` 前，与常见落地页不同——是否保留仅作对照？  
3. 确认后，可指定 `F-O1-V0001` 等，逐条展开完整 `type` 序列（只写 Markdown）。
