---
name: hub-writer
description: >-
  聚合页（Hub）生成唯一入口。策略性 SEO 页面：hero banner + 主题聚合部分（可多分块可单分块）+ 相关推荐，
  核心交付是详情页相互跳转的拓扑结构。基于大量现存 UGC/PGC 详情页的必然产物；不是落地页、大概率不是好的
  投放页；但要尽可能长得像长青页/专题页，增加页面 CRO 可能性。
  Use for 聚合页、目录页、榜单页、主题入口页、资源大全、Hub、best-of、"把详情页串起来"。
---

## 定位（先读这五条，决定你用什么心态写）

1. **是**：策略性 SEO 页面——当详情页（UGC/PGC）积累到一定规模，聚合页是**必然产物**，不是可选项。它吃类目词/榜单词/主题词，向详情页分发权重与点击。
2. **不是落地页**：不做广告投放承接，大概率不是优秀的投放页——不要写成转化漏斗。
3. **不是高级专题页**：它本质是聚合，但**外观要尽可能向长青页/专题页看齐**（观点导语、编辑判断、数字背书）——这是它与 doorway 垃圾页的区别，也是 CRO 可能性的来源。
4. **前置门槛**：≥8 个**已发布且可索引**的详情页。不足 → 先建详情页，hub 后置（hub 先行 = 空目录页，必被降权）。
5. **KPI**：类目词/榜单词排名 + 拓扑健康（出链/回链/收录/跳深）+ 分发点击。转化是加分项，不是目标。

## 与 landing-writer 的边界（别走错门）

| | landing-writer（转化页） | **hub-writer（本技能）** |
|---|---|---|
| 页面性质 | 投放承接、转化漏斗 | 策略性 SEO 聚合页 |
| 故事线 | `landing-storylines.json`（7 条转化向） | `references/hub-storylines.json`（4 条聚合向，本技能专属） |
| 核心逻辑 | 说服 → 转化 | 聚合 → 拓扑 → 分发 |
| CTA | 硬（trial/offer/compare） | 软（explore/start + 品牌收口） |
| 前置 | 无 | ≥8 可索引详情页 |
| 故障形态 | 转化低 | doorway 降权 / 空目录 / 死链 |

## 策略对齐

- hub 选址： 词群的 hub 字段（一集群一 hub 一主词，共享不另建）
- 集群结构规则： §Silo（spokes≥5 才建 hub）
- 前置门槛（≥8 可索引详情页）以 pipeline 实况为准；策略未声明该集群 → 先补 spokes，不建空 hub

## 四层决策

### 第一层 · 聚合故事线（4 条，选型 = 主词形态 × 详情页存量）

| 故事线 | 结构（aggregationBlocks） | 何时用 | 触发词 | 长青模式 |
|---|---|---|---|---|
| `hub-directory` | **单分块**：matrix | 全量目录："/tools/"、"all XX tools" | all / directory / everything / full list | strict |
| `hub-best-of` | ranked 主榜 + category 补充 | 榜单：best-of / top-N | best / top / recommended | hybrid（结构长青，榜单带年份则每年复核） |
| `hub-topic` | **多分块**：category ×2-3 + curated + recent | 主题入口：集群 hub、"everything about XX" | topic / guide to / start here / hub | strict |
| `hub-mixed` | curated 少而精 + matrix 兜底 | 合集：collection / roundup | collection / roundup / handpicked | strict |

完整骨架与字段见 `references/hub-storylines.json`（本技能专属 SSOT，独立于 landing 治理机器）。

### 第二层 · 分块类型（聚合块的 6 种形态）

| 形态 | 卡数 | 排序逻辑 | 用法 |
|---|---|---|---|
| `matrix` 全量矩阵 | 10-30（超 30 必分域分组） | 类目逻辑 | 目录页主体 |
| `ranked` 排名榜 | 5-12 | **编辑排序，有观点**（为什么第一是第一） | 榜单主体 |
| `curated` 精选注解 | 3-9 | 场景逻辑 | 专题化外观核心——每卡一句编辑判断 |
| `category` 类目分块 | 3-8/块，可复用多次 | 类目内权重 | 多分块聚合主体 |
| `recent` 最新 | 3-6 | 时间倒序 | 长青信号（证伪"死页"） |
| `cluster-link` 集群深链 | 3-8 | 拓扑关系 | 相关推荐位 + 拓扑收口 |

### 第三层 · 卡片与注解（防 doorway 的主战场）

卡片四件套：**title（类目词/场景词，不与子页 H1 相同——防 cannibalization）+ 差异化一句（这页解决什么/适合谁）+ 标签或场景注解 + 链接（verified slug）**。
编辑感三律（"像专题页"的本质）：① 导语有观点（不是"本页收录了…"，而是"选型只看一个标准…"）② 分类/排序有逻辑且写明 ③ 每卡注解是判断不是复述。
hub 自有内容（导语+观点+FAQ）≥300 词——纯卡片堆砌页 doorway 必被降权。

### 第四层 · 拓扑与 SEO（本技能的核心交付）

**拓扑三律**：
1. **hub ↔ spoke 双向**：hub 链到每个被聚合详情页；每个详情页**必须回链** hub（面包屑或相关块）——单向链不建拓扑
2. **hub ↔ hub**：cluster-link 块互链同层 hub + 上级导航
3. **深度预算**：任意详情页 ≤3 跳达任意 hub
**硬指标**：出链 ≥8（全部 verified slug 或 production 存活，禁编造）；无死链。
**SEO**：H1 用类目词/榜单词（长青措辞优先："Best X for Y" 优于 "X in 2026"，带年份则每年复核）；结构化数据 **ItemList**（聚合实体清单）+ BreadcrumbList；卡片 desc 全页唯一；收录前置——被聚合子页必须已提交收录（sitemap/已索引）。

## 页面骨架（从故事线取，通例）

1. **hero banner**：主题价值主张 + 数字背书（"N 个工具 · M 篇指南"——真实存量数字）+ 软 CTA（Browse/Start where it matters）
2. **主题聚合部分**：按故事线的 aggregationBlocks——单分块（directory 的 matrix）或多分块（topic 的 category×2-3 + curated + recent）；块间有导语衔接
3. **相关推荐**：cluster-link（同层 hub + 上级）——这是拓扑的横向纬度
4. **收口**：faq-light（3-4 条：怎么选/从哪开始/商用/更新频率）+ proof（数字背书/案例墙引用）+ 品牌软 CTA

## CRO 专题化清单（"让它看起来像长青页"——每项都是转化可能性的来源）

- [ ] 导语 3-5 句带观点，非目录说明文
- [ ] 数字背书用真实存量（N 详情页 / 覆盖 M 场景）
- [ ] ≥1 个 curated 块（编辑判断是最强专题信号）
- [ ] recent 块在页尾（活页感）
- [ ] faq-light 回答"从哪开始"（把浏览者往详情页推一步 = 拓扑 + CRO 双赢）
- [ ] 收口软 CTA 指向核心产品入口（品牌在场的自然露出，非 hard-sell）
- [ ] 配图走图库（Lovart: `../landing-writer/references/landing-ssot/image_pool.py` 可复用选图逻辑），禁编造

## 输出格式

- **结构定义**：按故事线 sections 输出模块序列 + 每块卡片清单（title/注解/slug/标签）——人工写 markdown 或组装 composite-v2 JSON 均可
- **composite-v2 复用**：聚合模块直接用组件库 `tool-grid / blog-grid / canvas-wall / showcase-stacked / bento-* / cluster-block-dense`（33 组件库见 `genflow/Page Gen/Refresh-Page/README.md`）；**不要**挂 storylineTemplate=landing-*（那是转化向治理），hub 页 storylineTemplate 留空或 `hub-{type}`
- **Sanity 适配**：发布走 `sanity-publish`；pageType 按站点 schema（Lovart topics 类型或新增 hub 类型，由发布技能判定）
- **语言**：默认 EN 主建；多语言按需扩展（聚合页翻译成本低于详情页，后置）

## 自检清单（交付前逐项）

- [ ] 详情页存量 ≥8 且可索引（不足 → 中止，先建详情页）
- [ ] 出链 ≥8、零死链、零编造 slug
- [ ] 每个被聚合子页有回链本 hub 的方案（写进交付说明，交发布/详情页维护方落地）
- [ ] 卡片注解全页唯一且有编辑判断；hub 自有内容 ≥300 词
- [ ] H1/主词不与任何子页 H1 冲突
- [ ] ItemList + BreadcrumbList JSON-LD 就绪
- [ ] 长青措辞核查（strict 模式无年份依赖）
- [ ] 软 CTA ≤3 处（hero/页中/收口），无硬投放按钮
- [ ] 拓扑图（可选但推荐）：画出 hub↔spoke↔hub 关系，交内链维护

## 关键路径

```
本技能 references/hub-storylines.json        ← 聚合故事线 SSOT（4 条 + 6 分块形态 + 拓扑规则）
genflow/Page Gen/Refresh-Page/README.md  ← 33 组件库（聚合模块定义）
../landing-writer/references/landing-ssot/image_pool.py  ← 选图逻辑复用
dev/scripts/publish_adapters/            ← 发布适配（通用）
```
