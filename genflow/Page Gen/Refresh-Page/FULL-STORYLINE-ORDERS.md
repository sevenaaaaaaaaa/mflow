# 叙事顺序（摘自 README 原文）

> 修订：2026-05-31  
> **依据文件**：[README.md](./README.md)、[preview-data.json](./preview-data.json)（README L13–14、L19–20 引用的预览数据源）  
> **不引用** [STORYLINES.md](./STORYLINES.md) 中的 F1/N1 等（那是短链示例，不是 README 原文）。

---

## 1. README 里关于「顺序」写了什么

| README 位置 | 原文要点 | 对叙事顺序的含义 |
|-------------|----------|------------------|
| L22–29 Variants 面板 | **One each**：每个组件大类只显示 1 个变体；**Show all**：33 段全展开；移动端「全部 section **顺序铺开**」 | 落地页顺序以预览数据源为准，不是随意排列 |
| L13–14、L19–20 | 示例与预览来自 **`preview-data.json`** | 这是 README 认可的**默认 section 顺序** |
| L94–669 `# 组件清单` | 各 `##` 标题按固定顺序介绍组件 | 文档阅读顺序（与 preview-data **不完全相同**） |
| L98 | Hero 区「**页面首屏用**」 | Hero 大类始终在第一位 |
| L395 | Showcase「**"产品流程"叙事**」 | 命名了一种叙事：展示 + 流程成组 |
| L499–514 | `workflow-horizontal`「3 步搞定」；`workflow-vertical`「**详细叙述**」 | 流程模块跟在产品/步骤叙事后 |
| L636–642 | `proof-block`「Why use …」 | 信任/理由块，属证明段 |
| preview-data `hero-journey` | journeyCards step 02：Landing page 含「**Hero, proof, comparison, FAQ and CTA**」 | 落地页收口语序的原文描述 |
| preview-data 末两段 | `faq` → `cta-default` | 收口：FAQ 在 CTA 前 |

README **没有**写「O01 试用优先」「O04 对比决策」等命名；此前 §4 那 10 条来自 STORYLINES，**已作废**。

---

## 2. 四种叙事顺序（当前能从 README 推出的全部）

每种顺序都是 **20 个模块大类** 各出现一次（Variants **One each**）。  
表中用 **模块大类名** 表示；`*` 表示该大类需从变体中择一（见 [FULL-STORYLINE-VARIANTS.md](./FULL-STORYLINE-VARIANTS.md)）。

### O1 · 预览默认顺序

| 项目 | 内容 |
|------|------|
| **README 依据** | `preview-data.json` 数组顺序；README L19–20、L22–29 |
| **含义** | 前端预览页 **One each** 模式下，各大类**第一次出现**的先后 |

**20 段顺序：**

```
hero* → logo-loop → bento* → capability-tabs → tool-grid → blog-grid → feature-detail → canvas-wall → portrait* → showcase* → media-marquee → prompt-launcher → workflow* → comparison* → testimonial* → stats → proof-block → pricing-block → faq → cta-default
```

---

### O2 · 组件清单文档顺序

| 项目 | 内容 |
|------|------|
| **README 依据** | `# 组件清单（33 种）` 各 `##` 标题顺序（L94–669） |
| **含义** | 与 README 文档结构一致，便于对照字段说明 |

**20 段顺序：**

```
hero* → bento* → capability-tabs → tool-grid → blog-grid → feature-detail → canvas-wall → portrait* → showcase* → media-marquee → prompt-launcher → logo-loop → cta-default → workflow* → comparison* → testimonial* → stats → proof-block → pricing-block → faq
```

> 注意：O2 里 `cta-default` 出现在 `faq` **之前**（因 README 把 CTA 写在「CTA / 流程」、`faq` 写在后面的「数据 / 信任 / 价格 / FAQ」）。**真实落地页收口通常仍用 O1 的 `faq → cta-default`**。O2 仅作文档对照，是否采用需你确认。

---

### O3 · 产品流程叙事

| 项目 | 内容 |
|------|------|
| **README 依据** | L395 Showcase 章节标题 **「"产品流程"叙事」**；L468–514 流程组件 |
| **含义** | 先讲「产出/案例展示」，再讲「步骤流程」，再展开其余模块 |

**相对 O1 的调整：** 首屏后立刻插入 `showcase*` + `workflow*`，其余模块保持 O1 中的相对先后（未在 O3 点名的，按 O1 顺序接在后面）。

**20 段顺序：**

```
hero* → showcase* → workflow* → logo-loop → bento* → capability-tabs → tool-grid → blog-grid → feature-detail → canvas-wall → portrait* → media-marquee → prompt-launcher → comparison* → testimonial* → stats → proof-block → pricing-block → faq → cta-default
```

---

### O4 · 落地页收口语序（买家旅程）

| 项目 | 内容 |
|------|------|
| **README 依据** | preview-data 中 `hero-journey` 的 journeyCards **step 02**（Landing page）；`proof-block`、`comparison-*`、`faq`、`cta-default` 字段说明 |
| **含义** | 中段模块仍服务「讲清楚产品」；**结尾**按 journey 原文收成「证明 → 对比 → FAQ → CTA」 |

**相对 O1 的调整：** 前段（hero 至 pricing-block 之前）与 O1 相同；**末段**固定为：

```
… → proof-block → comparison* → faq → cta-default
```

（`testimonial*`、`stats`、`pricing-block` 仍在 `proof-block` 之前，顺序同 O1。）

**20 段顺序：**

```
hero* → logo-loop → bento* → capability-tabs → tool-grid → blog-grid → feature-detail → canvas-wall → portrait* → showcase* → media-marquee → prompt-launcher → workflow* → testimonial* → stats → pricing-block → proof-block → comparison* → faq → cta-default
```

---

## 3. 故事线编号

```
F-O1-V0042   =  Feature · 叙事 O1（预览默认）· 变体 V0042
T-O3-V0001   =  Tool · 叙事 O3（产品流程）· 变体 V0001
```

| 叙事 O | 条数（× V0001–V1200） |
|--------|------------------------|
| O1 | 1,200 |
| O2 | 1,200 |
| O3 | 1,200 |
| O4 | 1,200 |
| **Feature 小计** | **4,800** |
| **Tool 小计** | **4,800** |
| **合计** | **9,600** |

---

## 4. README 尚未定义、故未列入的顺序

以下在 **STORYLINES.md** 或旧讨论里出现过，但 **README 原文未给出**对应的全页排法，**暂不自动生成**：

- 「试用优先 PLG」「对比决策」「SEO 引流」等命名叙事  
- 首屏 Hero 变体与第二屏的配对表（在 STORYLINES §三，不在 README）  
- 任意 20 段全排列

若前端团队在 README 或 `preview-data.json` 中**补充**新的叙事说明，在此文件追加 **O5、O6…** 并注明行号即可。

---

## 5. 与 [FULL-STORYLINE-CATALOG.md](./FULL-STORYLINE-CATALOG.md) 的关系

- **变体、大类、满配 20 段** → 见 CATALOG §2–§3  
- **叙事顺序** → 仅本文 O1–O4  
- 选定 `F-O?_-V____` 后，将 O 的模块序列中的 `hero*` 等替换为 V 中的具体 `type`，即完整故事线
