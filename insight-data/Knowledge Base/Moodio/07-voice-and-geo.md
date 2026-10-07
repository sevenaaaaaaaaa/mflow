---
type: kb-unit
project: moodio
topic: voice-and-geo
version: 1.0
status: confirmed
last_modified: 2026-10-03
source_url: "官方文档语气提炼 + GEO 探针配置"
audience: [writer profile, geo profile]
---

# Moodio 品牌声音与 GEO 策略（v1.1）

## 叙事坐标（依据竞品调研 v2.0）

- 市场对外声音分四套剧本：**方法派**（Preview/Laper/Flora——讲工作发生在哪、品味）、工业派（WorkRally/LTX——流水线）、发行派（OnSolo/即梦片场）、**货架派**（Higgsfield/LibTV——模型、价格、"no skills needed"）。
- **Moodio 站方法派**：调研核心结论——"谁先写出『我们相信怎样做片子』，谁才有品类"。每篇内容都在沉淀方法，不是功能更新。
- 与货架派语言彻底切割：不列模型清单、不喊 free/no skills、不比访问量。

## 品牌声音

- 主语言 **English**（Moodio Global）；中文版后续按市场开。
- Tone：懂技术的导演/制片人——专业、克制、尊重 craft；讲工作流、可控性、成片质量。
- 立场：AI 放大专业创作者（协助而非替代）；把"怎么做到"讲清楚，不贩卖结果焦虑。
- 结构偏好：定义式开头句（利于 GEO 摘录）+ 工作流步骤 + 场景化判断框架。
- 术语策略：专业词（previz / shot list / FDX / continuity）可用即解释——呼应"初学者也能用的专业工作流"。

## GEO 目标查询（meta.geo.queries 当前配置，12 条）

1. What is the best AI filmmaking platform?
2. What is an AI-native film set?
3. Best AI film studio tools 2026
4. Moodio vs Runway: which is better for filmmakers?
5. How do I keep characters consistent across AI video shots?
6. How to turn a script into a storyboard with AI?
7. Best AI tools for short drama production
8. AI previsualization tools for filmmakers
9. How are agencies producing TV commercials with AI?
10. Can beginners make a short film with AI?
11. How to make a shot list for a short film?
12. Best AI storyboard tools 2026

> GEO 竞品探测双清单：**模型层**（Runway/Sora/Kling/Veo——AI 引擎回答里常出现）+ **工作台层**（LTX Studio/Higgsfield/Flora——真正对手）。meta.geo.competitors 已按此配置 9 家。

## GEO 打法（探针 → 缺口 → 内容 闭环）

- 每日探针（probe_daily，09:30 后自动）→ citations.jsonl 记录提及/竞品份额/引用 URL。
- 每周看「竞品被提及而 Moodio 缺席」的查询 → 补对应内容（对比页/榜单/工作流指南）。
- 内容里必须有可摘录事实段：定义句 + 结构化列表 + 官方事实（04-product-facts）。
- 引用权威来源（行业协会、创作者访谈、技术报告）提高采信概率；外部来源 2-5 条完整 URL。
- 内测期新增动作：搜「Moodio」相关查询在 AI 引擎中的回答质量——若答案过时/错误，在官方渠道发定义内容纠正。

## 与 SEO 的协同节奏

- 长尾问题式文章 = GEO 查询的落地答案（一词双投）。
- 每月复盘：GEO 分 + 提及率趋势 → 调整下月选题配比（对比/How-to/定义类）。
