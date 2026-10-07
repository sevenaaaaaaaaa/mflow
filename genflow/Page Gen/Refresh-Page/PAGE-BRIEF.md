# 落地页 Brief：先定立场，再选模块

> **SSOT**：所有 compositePage（Features / Tools / Product / Scenarios / Solution / Landing）动笔前的**统一 Step 0**。  
> 故事线与模块字典见 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md)；制作人手册见 [For-Landing-Page-制作人.md](../../1-1 GEO Readme/文档/03-角色手册/For-Landing-Page-制作人.md)。

---

## 为什么必须是前置步骤

模块和故事线是**表达手段**，不是**页面定义**。  
若跳过立场直接选 `hero-split` + `bento-4`，常见后果：

- 题材该做 Scenario，却写成 Product 说明书（或反过来）
- SEO 页缺 FAQ/定价，投放页却堆 13 段
- 能力、特色、功能混在一层，读者不知道「这页到底卖什么」

**顺序固定：Brief（立场）→ category + storyline（模块序列）→ 文案与素材。**

---

## Step 0：定立场（Brief 五问）

动笔前用下面五问填完（可写在任务卡 / Notion / PR 描述里）；**任一答不出，先不要选故事线**。

### 0.1 流量目的

| 目的 | 典型目标 | 对模块的影响 |
|------|----------|--------------|
| **官网 / SEO** | 收录、内链枢纽、长尾 FAQ | 完整故事线；FAQ、对比、定价（若该类型允许）保留 |
| **投放 / 高意图落地** | 转化、广告一致性 | 压缩段数；首屏 + 对比/before-after + 底 CTA 加权；FAQ 缩短 |
| **站内导航 / 教育** | 帮助用户选型 | 加强 tool-grid、内链、步骤；弱化硬销 |

### 0.2 读者在问什么（叙事立场）

| 读者核心问题 | 优先 `category` | 你卖的是什么 |
|--------------|-----------------|--------------|
| 「这个**工具/功能**怎么用、值不值？」 | `tool` / `feature` | 单点能力或生成器 |
| 「这个**产品/模块**是什么、要不要买？」 | `product` | Lovart 产品线（ChatCanvas、Brand Kit…） |
| 「**我这行/这场景**能不能用？」 | `scenario` | 职业或流程下的用法 |
| 「**整套方案**能不能替我们团队？」 | `solution` | 组合方案 / 组织采购 |
| 「Lovart **整体**是什么？」 | Landing（或首页） | 品牌 + 全栈概览 |

**撞题规则：** 题材可重叠（都讲电商），**category 由「Hero 主语」决定**——Hero 写产品名 → Product；写「电商运营的一周」→ Scenario；写「Shopify 增长方案」→ Solution。

### 0.3 内容主次（能力 / 特色 / 功能）

同一页可三者皆有，Brief 里标 **主 / 次 / 点缀**：

| 维度 | 含义 | 模块倾向 |
|------|------|----------|
| **能力** | 平台级、跨场景的基础力 | `capability-tabs`、`workflow-*` |
| **特色** | 差异化、难一句话讲清 | `comparison-table`、`testimonial`、`logo-loop` |
| **功能** | 可点名、可链 Tools/Features | `tool-grid`、`prompt-launcher`（Tools/Features）、`showcase-*` |

### 0.4 表达难度

| 类型 | 策略 |
|------|------|
| **直观**（点选编辑、前后对比） | `showcase-*`、`comparison-before-after`、短 `bento-*` |
| **需展开**（Agent、治理链、MCoT） | 多 Tab、`workflow-vertical`、长 FAQ |

### 0.5 与相邻页的分工

Brief 里写一句：**本页不做什么**（例如「不讲定价套餐细节，链到 Product」「不讲 Touch Edit 操作，链到 Feature」），避免站内 cannibalization。

---

## Step 1：选 category + 故事线

Brief 完成后，才查下表选 `category` 与故事线 ID（细节见 STORYLINE-BY-DIRECTION §4）。

| `category` | 默认故事线 | section 量级 | 定价 | 试用 `prompt-launcher` |
|------------|------------|--------------|------|-------------------------|
| `feature` | `features-main` 等 4 条 | 13 | ✅ | ✅ |
| `tool` | `tools-A` 等 6 条 | 12～13 | ❌ | ✅ |
| `product` | `product-标准` / `product-含社会证明` | 12～13 | ✅ | ❌ |
| `scenario` | `scenarios-A` 等 14 条 | 11 | ❌ | ❌ |
| `solution` | 见 `solution-storylines.json` | 12 | ✅ | 视稿 |
| Landing | 见 `landing-storylines.json`（6 投放线 + `landing-full`） | 12～15 | 仅 offer-close / full | trial-now + full |

**投放向：** 在对应类型中选「视觉扩展 / 对比 / 精简」故事线，或保留 type 顺序但删段、加重首屏与 `comparison-before-after`（Product 见 [PRODUCT-PRODUCTION.md](./PRODUCT-PRODUCTION.md) §4.2）。

---

## Step 2：模块权重（同一故事线内的调参）

故事线定的是 **type 顺序**；Brief 定的是 **每段写多深**：

| Brief 信号 | 加重 | 减轻 |
|------------|------|------|
| 特色型 | `comparison-table`、证言、Logo | 步骤段 |
| 能力型 | `capability-tabs`、`workflow-*` | tool-grid |
| 功能型 / 工具向 | `prompt-launcher`、`tool-grid`、showcase | 长 FAQ |
| 投放 | Hero、before-after、底 CTA | FAQ 条数、cluster |
| SEO | FAQ 长尾、内链、`pricing-block`（若允许） | — |

---

## 一页 Brief 模板（复制到任务）

```markdown
## 页面 Brief
- **slug / category**：
- **流量目的**：官网 SEO / 投放 / 站内教育
- **读者问题**：（一句话）
- **主语（Hero）**：产品名 / 场景 / 方案 / 工具名
- **内容主次**：能力 __ / 特色 __ / 功能 __（主/次/点缀）
- **表达难度**：直观 / 需展开 / 混合
- **不做什么**：（链到哪一页）
- **故事线 ID**：（Brief 填完后再选）
- **参考页**：（同类已上线或本地案例 JSON）
```

---

## 各类型 Brief 速查

| 类型 | Step 0 最关键的一问 | 常见误选 |
|------|---------------------|----------|
| **Features** | 是否只讲**一个**能力（而非整条产品线）？ | 写成 Product 总览 |
| **Tools** | 用户能否**立刻试**一个输入？ | 缺 `prompt-launcher` |
| **Product** | Hero 是否是 **Lovart 产品名**？ | 写成 Scenario 指南 |
| **Scenarios** | Hero 是否是 **场景/角色**？ | 加 pricing、tool-grid |
| **Solution** | 是否在卖 **组合/组织级** 理由？ | 写成单功能 Feature |
| **Landing** | 是否 **全栈品牌** 而非单点？ | 与 Product 重复 |

---

## 相关文档

| 文档 | 用途 |
|------|------|
| [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) | 六类故事线与 type 顺序 |
| [PRODUCT-PRODUCTION.md](./PRODUCT-PRODUCTION.md) | Product Brief 展开 + 案例 |
| [FEATURES-PRODUCTION.md](./FEATURES-PRODUCTION.md) | Features 流水线 |
| [SCOPE.md](./SCOPE.md) | 哪些内容走 compositePage |

**应用交叉引用补丁**（若各文档尚未链接 PAGE-BRIEF）：在项目根目录运行 `bash ".cursor/patches/apply-page-brief-crossrefs.sh"`
