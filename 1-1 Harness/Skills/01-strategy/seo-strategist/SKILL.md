---
name: seo-strategist
description: >-
  SEO 策略师（L0 策略层，先行）。SEO 策略 = 在搜索战场上，用有限的内容产能赢下"能赢的查询"的系统。
  产出机读策略 strategy/seo-strategy.json（词群地图/意图-形态映射/空档/黑名单/GEO 查询），是生成层的上游契约。
  Use for 「SEO 策略」「词群规划」「关键词战略」「搜索战场」「竞品词库」「SEO 空档」「GEO 策略」。
---

## SEO 策略的定义（先想清楚再动手）

SEO 策略不是关键词列表。它是四个决策的系统：

1. **战场**——我们打哪些查询？（按 意图 × 竞争度 × 商业价值 把查询分区，只宣布打得动的）
2. **武器**——每类查询用什么内容形态承接？（query → contentType → ownerSkill 映射，一 query 一形态）
3. **顺序**——先打哪个？（空档词群 > 长尾 > 品类 > 大词；ICE 排序）
4. **胜负**——怎么算赢？（每个词群定义里程碑：收录 → 排名区间 → 流量 → GEO 提及）

没有这四个决策就开工生成 = 把预算撒进随机查询——这就是"生成很傻"的根因。


## 历史资产承接（不另起炉灶）

- **KR 式结构**继承 `01-project/Lovart-SEO-Q3-Tactical-Plan-2026.md`（数据基线诊断 → O/KR → 12 周执行日历 → 预期效果模拟 → 风险应对）——本技能的策略文件保留 baseline/krs/timeline/projection/risks 字段
- **数据摄入**不重建：GSC/GA4 刷新走 `trident-data-engine`，词表摄入走 `keywords-intake`——本技能只做"摄入之后的战略加工"
- **竞品实测范式**继承 Moodio 侧竞品调研方法论（SimilarWeb/Semrush 实测 → 分层战场 → 空档词群）
- GEO 探针复用 console 既有 geo_scheduler/citations.jsonl 设施，策略文件只声明目标查询

## 方法论（五阶段，产出自 `1-3 GenFlow/Content Strategy/`）

### Phase 1 · 市场测绘（实测，不拍脑袋）
对每个候选战场做 SERP 实测：谁能排、凭什么样态排（工具页/榜单/教程/文档）→ 竞品词库交叉（Semrush/Sentinel 实测数据）→ 竞争烈度分级。参考 Lovart 影视竞品实测范式：工作台层是正面战场、模型层只借力不硬打、实测空档词群最值钱。

### Phase 2 · 词群地图（clusters）
聚词成群（同一意图的查询组），每群一条记录：

```json
{"id": "cluster-storyboard", "queries": ["ai storyboard generator", "..."],
 "intent": "informational|commercial|transactional|navigation",
 "contentType": "blog-howto|landing-tools|hub-directory|hub-best-of|guide|glossary",
 "ownerSkill": "blog-writer|landing-writer|hub-writer",
 "competition": "open|contested|monopolized", "priority": "P0|P1|P2",
 "gapFlag": true, "milestone": "收录→Top20→Top10→GEO 提及"}
```

### Phase 3 · 空档识别（⭐ 最值钱的一步）
我方产能 ∩ 查询有真实需求 ∩ 竞品未占 = 空档词群，标 `gapFlag: true`、P0 优先。竞品已垄断的词（如 ai video generator 大词）进**黑名单**（`bannedQueries`），写出为什么不碰（有实测依据更佳）。

### Phase 4 · 技术底座（策略的地基）
内链拓扑规划（hub-spoke 归属：每词群声明它的 hub 在哪）、收录方案（sitemap/IndexNow）、结构化数据要求（FAQ/HowTo/ItemList）。拓扑与词群必须一一对应——词群没 hub 就先建 hub（触发 hub-writer）。

### Phase 5 · GEO / AI 搜索可见性
目标查询集（10-15 条用户会问 AI 的问题）→ 每日探针 → 缺口查询回流 Phase 2 成新词群。AI 引擎的引用偏好（定义式开头/统计/来源）作为内容约束传给生成层。

## 产出契约（下游怎么消费你）

写入 `1-3 GenFlow/Content Strategy/seo-strategy.json`（schema 见目录 README）。消费方：
- **blog-writer**：选题必须 trace 到某个 cluster.id（写进 frontmatter `content_cluster`）
- **landing-writer**：页面主词必须来自某 cluster；投放页词再过 paid-strategy 白名单
- **hub-writer**：hub 选址 = 词群的拓扑入口声明
- **optimization-loop**：milestone 是刷新判定的基准

## 工作纪律

- 每季度全量复核词群（市场会变）；每月用 GEO 探针 + GSC 滚动修订
- 策略文件是 SSOT：改策略 = 改 json + 版本号递增，不改生成技能
- 没有实测数据支撑的词群判断标 `[假设]`，验证后转正
