---
name: optimization-loop
description: >-
  持续优化层（L2）：让内容资产随数据进化而不是发布即衰减。循环 = 测（信号采集）→ 诊（缺口/衰减/机会）
  → 方（动作：刷新/重写/新选题/策略修订）→ 行（进 pipeline S0）→ 复测。
  信号源：GSC（trident 刷新）· GEO 探针 citations.jsonl · Sentinel 舆情 · 用户之声（audience-ops）。
  Use for 「内容优化」「刷新旧文」「衰减改稿」「数据回流」「优化队列」。
---

## 持续优化的定义

内容资产的默认命运是发布 3 个月后开始衰减——持续优化层的工作就是对抗这件事：**每个资产带里程碑（来自 seo-strategy 词群），每周期用信号对照里程碑，偏差变动作**。它不是"再看一眼数据"，是一台把信号翻译成 pipeline 动作的机器。

## 信号 → 动作映射表（核心资产，逐条执行）

| 信号（来源） | 诊断 | 动作（进 pipeline S0） |
|---|---|---|
| GSC 高曝光低点击（impr↑ click≈0） | 标题/摘要不匹配意图 | 标题+meta 重写（不动正文） |
| GSC 排名 8–20 且曝光 >100 | 差一口气 | Content Refresh：补深度/更新数据/强化内链 |
| GSC 排名持续下滑（Top10→Top20） | 内容过时或竞品超车 | 衰减改稿 loop（复核事实/补新段落） |
| GEO 探针：竞品被提及而品牌缺席 | 答案缺口 | 新选题入队（对比页/答案文，trace 词群） |
| GEO 探针：品牌被提及但引用了旧页面 | 页面失焦 | 该页 GEO 结构化改稿（定义句/统计/来源） |
| Sentinel：竞品新动作/负面议题 | 话题机会或风险 | Comparison/Insight 选题（7 天内跟进） |
| topology 审计：hub 出链 <8 / spoke 未回链 | 拓扑破损 | 内链修补工单（不动文案） |
| 用户之声（audience-ops）：高频问题 | 内容缺口 | 新选题候选（进 content-strategist 评审） |
| 季度审计：零流量零转化资产 | 资产无效 | 301 合并 / 深度重写 / 下架建议 |

## 方法论（周循环）

1. **测**：每周一跑 trident（GSC/GA4 刷新）+ 读 GEO 周汇总 + Sentinel 周报 + 上周 pipeline 表现。
2. **诊**：信号过映射表，产出《优化工单》：每条 = 资产 + 信号证据 + 动作类型 + 优先级（ICE）。
3. **方**：动作分四类——刷新（翻新旧文）/ 重写（标题/meta 级）/ 新选题（进词群评审）/ 策略修订（反馈给 L0，改 strategy json 而不是硬改内容）。
4. **行**：刷新/重写走 blog-writer（Content Refresh 路径）进 pipeline；新选题过 content-strategist 三重 trace。
5. **复测**：动作后 14 天复核同一信号，写进工单闭环记录。

## 产出契约

`1-3 GenFlow/Content Strategy/optimization-log.jsonl`（周追加）：`{"week", "signal", "asset", "action", "priority", "owner", "closedAt", "result"}`。策略层修订建议汇总给对应 strategist（改策略文件，版本递增）。

## 边界

- 信号采集是 05-monitor（sentinel/sitemap/trident）的事；本技能是**诊断与动作**。
- 生成是 blog-writer 等的事；本技能只开工单，不动手写。
- 发布动作永远止步 ready，人工授权（同全站原则）。
