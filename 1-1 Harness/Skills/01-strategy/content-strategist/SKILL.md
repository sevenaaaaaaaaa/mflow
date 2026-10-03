---
name: content-strategist
description: >-
  内容营销策略师（L0 策略层，总协调）。内容营销策略 = 把"我们懂的"变成"受众搜的"，用内容资产网络在
  受众旅程里复利。产出机读策略 strategy/content-strategy.json（人群×漏斗配比/集群拓扑/复用链/日历节奏），
  统辖 blog/landing/hub 三大生成入口的选题来源。Use for 「内容策略」「选题规划」「主题集群」「内容配比」「内容日历」。
---

## 内容营销策略的定义

内容营销策略回答四个问题：

1. **给谁**——persona × 漏斗矩阵，每个格子配多少产能？（不是"都写"，是配比）
2. **造什么**——内容不是一篇篇文章，是**资产网络**：集群（cluster）→ pillar 长文 → spokes 教程/对比 → hub 聚合入口。每篇内容必须声明自己在网络里的位置。
3. **什么节奏**——产能 × 配比 → 周计划（content-calendar 的上游）；固发 > 爆发。
4. **怎么复利**——一鱼多吃链：长文 → 衍生稿 → 社媒 → newsletter；发布不是终点，是分发起点。

**与 SEO 策略的关系**：seo-strategist 决定"打哪些查询"（需求侧），content-strategist 决定"用什么资产网络承接并服务谁"（供给侧+人群侧）。两者共同约束生成层：**选题 = 词群 ∩ 人群格子 ∩ 集群位置**，三者缺一的选题不进队列。


## 历史资产承接（十份既有策略文档 = 本技能的维度来源）

`Content Strategy/00-09-*.md` 不是废弃品，是本策略的**分维度详情**，映射写死在 content-strategy.json 的 lineage 字段：
- 00-全景清单 → **Silo Structure**（页面类型体系/博客分类/内链路由）→ clusters.linkRule
- 01-漏斗矩阵 → **funnelMix**（四阶段覆盖度与 BOFU 缺口分析）
- 02-季节性日历 → axisPlans.seasonal　03-行业深度 → axisPlans.industries
- 04-职业工作流 → axisPlans.professions　05-企业级 → axisPlans.enterprise
- 06-复用分发 → reuseChains + 渠道优先级　07-伦理法律 → axisPlans.ethicsLegal
- 08-执行日历审计 / Docs/S2《内容复盘与缺口分析》→ 已升级为 `optimization-loop`
- **节奏执行**仍由 `content-calendar` 落地（本技能产出节奏，calendar 写日历——分工不变）

## 方法论

### Phase 1 · 人群-漏斗矩阵
persona（专业影视人/机构/新手…）× 漏斗（TOFU/MOFU/BOFU）= 9-12 格。每格：内容形态（TOFU=guide/insight；MOFU=howto/comparison；BOFU=case/vs 页/beta 页）+ 配比（如 40/40/20）+ 北极星。配比随阶段调（冷启动偏 TOFU 抢词，增长期偏 MOFU/BOFU 收割）。

### Phase 2 · 集群拓扑规划
每个主题集群一份拓扑定义：
```json
{"id": "cluster-storyboard", "pillar": "storyboard-guide（blog 长文）",
 "hub": "hub-topic:/topics/storyboard（hub-writer）",
 "spokes": ["howto-×3", "comparison-×2", "landing-tools-×1"],
 "linkRule": "spoke→pillar→hub 全互链；跨集群只经 hub"}
```
集群未满员（spokes < 5）不建 hub；hub 建成后 spoke 发布必须回链（拓扑健康归 optimization-loop 审计）。

### Phase 3 · 产能与节奏
月产能盘点（人/技能/门禁吞吐实测）→ 按矩阵配比切周计划 → 写入 content-calendar（执行工具）。节奏原则：每周固定配比产出 > 攒大招；每集群并行推进（pillar → spokes → hub 顺序）。

### Phase 4 · 复用链（一鱼多吃）
每篇 BOFU/MOFU 资产发布时声明衍生计划：长文 → 摘要稿（≤600）→ 社媒卡 → newsletter 段落。分发链复用 content-distribution / multi-platform-push；UTM 按 AD-Tracking SSOT。

### Phase 5 · 淘汰与升级
季度审计：无流量无转化的资产 → 301 合并或刷新（触发 optimization-loop）；达到 milestone 的 → 升级（加结构化数据/翻译扩语种/纳入投放白名单→触发 media-strategist）。

## 产出契约

写入 `1-3 GenFlow/Content Strategy/content-strategy.json`：personas×funnel 配比、clusters[]（拓扑）、reuseChains[]、cadence、quarterlyReview 日期。

消费方：**三大生成入口**（选题必须三重 trace：cluster.id + persona 格 + 网络位置，写入产出元数据）· **content-calendar**（节奏落地）· **optimization-loop**（淘汰/升级动作源）· **audience-ops**（persona 定义共享）。
