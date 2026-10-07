---
title: "AI 视频 Prompt 结构指南：营销 static-first 配套"
slug: ai-video-prompts
date: "2026-08-06"
language: zh
page_type: Blog Post
category: How-To
author: Lovart Content Team
description: "404 修复：营销 video prompt 五段结构，ChatCanvas static-first，Brand Kit，Touch Edit 改价。"
estimated_read: 9 min
difficulty: beginner
tool: ChatCanvas, Brand Kit, Touch Edit, Design Agent
focus_keyword: ai video prompts 营销
keywords:
  - ai video prompts
  - chatcanvas
  - brand kit
  - touch edit
tags:
  - lovart
  - 404-recovery
seo_title: "AI 视频 Prompt — 营销 static-first 工作流"
seo_description: "video prompt 结构：Design Agent、Brand Kit、Touch Edit、static companion。"
seo_schema: FAQ
cover_url: https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-014-1024x682.png
alt_text: ai-video-prompts — Lovart blog cover
status: ready
content_cluster: How-To — Video Prompts
releaseDate: "2026-08-05T20:00:00Z"
publishedAt: "2026-08-05T20:00:00Z"
---



# AI 视频 Prompt 结构指南：营销场景的 static-first 配套

这条中文 URL 曾返回 404，搜索却在问「营销视频 prompt 怎么写才不出废片」。视频 prompt 不是越长越好，而是一套可验收的字段：镜头意图、主体、光线、时长、禁止项、以及 companion static 的 safe zone。Lovart **ChatCanvas** 与 **Design Agent** 负责先出可读 static hero；**Brand Kit** 锁色温与 type role；**Touch Edit** 改价与 CTA，避免每次改 offer 都重跑整条 video pipeline。

## 营销 video prompt 的五段结构

第一段写 campaign intent：这条 clip 服务哪个渠道、静音播放时用户能否看懂 offer。第二段写 subject 与 action：产品或人物做什么，禁止 vague「高级感」。第三段写 camera 与 light：slow pan、top-down、golden hour 等可执行词，不要堆形容词。第四段写 duration 与 aspect：4–6 秒 loop、9:16 story、16:9 pre-roll。第五段写 negative constraints：no readable small text、no double CTA、no logo drift from Brand Kit。

## static-first 为什么先于 video gen

信息流常静音 autoplay，用户截图的是 still，不是 BGM。正确顺序是 ChatCanvas 出 hero 与 end card static，legal 过审 offer 与 disclaimer，再配 video hook。反过来先做燃向 clip 再补 static，常出现详情页价格与视频角标不一致。404 修复页给运营 stable SOP URL。

## ChatCanvas brief 与 video prompt 一致

弱 brief：「做一条产品宣传 video」。强 brief：「SKU 居中，Brand Kit sage + charcoal，price bottom left safe zone，4:5 static master；video companion 5s slow pan，色温匹配 Kit，禁止 clip 内小字 offer」。static 与 motion 共用 **Brand Kit** hex role，Touch Edit 改 promo 时 static 与 end card 同步，video 可不变或只换 hook 段。

## Touch Edit 在 video 工作流里的位置

周二改「限时 ¥99」到「满减 200」，用 **Touch Edit** 改 static hero 与 end card 字层，不要为两个字重跑 video gen。若 clip 内 baked 了价格像素，改价成本会爆炸。brief 应要求 offer 只在 editable static 层，clip 只做 mood 与 product motion。

## Design Agent 与渠道 safe zone

抖音、小红书、朋友圈的 UI 遮挡不同。brief 分渠道写 top/bottom 百分比。video prompt 里写「leave top 12% clear for platform chrome」，static 同样遵守。同一 ChatCanvas thread 出 carousel 与 video still，角标位置不 drift。

## 常见失败

prompt 只有「cinematic luxury」无验收字段。clip 内小字价格 unreadable。改价 full regen video。跳过 Brand Kit 后 static 与 clip 色温分裂。无 end card static，落地页 offer 与 video 脱节。

## 测量什么

记「改价一次几分钟」「static 与 clip 色温一致几次失败」「legal return 几次」。revision cost 决定 video 工具是否值得 daily 用。


## 实操补充 1：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 2：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 3：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 4：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 5：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 6：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 7：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 8：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 9：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。



## 实操补充 10：营销 video 与 static 一致

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。营销 video 与 static 一致 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。


## FAQ

**营销 video prompt 最短要写什么？**  
campaign intent、subject、camera/light、duration/ratio、negative constraints 五段；offer 放 editable static，不在 clip 小字。

**改价要重跑 video 吗？**  
不用。Touch Edit 改 static hero 与 end card；clip 可不变。

**static-first 顺序？**  
ChatCanvas static legal pass → 再配 video hook。

**404 修复意义？**  
stable URL 给运营 video+static SOP。

**Brand Kit 作用？**  
static 与 clip 色温一致，防 carousel drift。



*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch5 content cluster.*

