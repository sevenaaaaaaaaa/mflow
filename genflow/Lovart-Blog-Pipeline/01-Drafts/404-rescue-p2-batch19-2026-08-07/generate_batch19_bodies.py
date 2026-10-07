#!/usr/bin/env python3
"""Generate 404-rescue P2 batch19 blog bodies (10 files). Self-contained.

Ranks #194–#203 from 404-rescue-compact lane.
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
    "zh": 2200,
    "zh-TW": 2200,
    "en": 1300,
    "ko": 1400,
    "ru": 900,
    "de": 900,
    "pt": 900,
    "it": 900,
    "fr": 900,
    "ja": 1800,
}

BANNED_EN = [
    "unlock", "revolutionize", "game-changer", "leverage", "streamline",
    "empower", "seamless", "seamlessly", "delve", "testament",
    "unprecedented", "the future of", "pave the way", "elevate", "fostering",
    "tapestry", "beacon", "realm", "journey",
]
BANNED_ZH = [
    "赋能", "闭环", "抓手", "链路", "底层逻辑", "方法论", "心智", "对齐",
    "颗粒度", "打法", "痛点", "破局", "深挖", "见证", "颠覆性", "前沿",
    "生态位", "维度", "引爆",
]

JA_CHAR_RE = re.compile(r"[ぁ-んァ-ン一-龥々〆ヵヶ]")


def cover_url(n: str) -> str:
    return f"https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-{n}-1024x682.png"


def body_text(full_md: str) -> str:
    if full_md.startswith("---"):
        return full_md.split("---", 2)[-1]
    return full_md


def count_zh(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", body_text(text)))


def count_en(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", body_text(text)))


def count_ko(text: str) -> int:
    return len(re.findall(r"[가-힣]", body_text(text)))


def count_ru(text: str) -> int:
    return len(re.findall(r"[а-яА-ЯёЁ]+", body_text(text)))


def count_ja(text: str) -> int:
    return len(JA_CHAR_RE.findall(body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang in ("zh", "zh-TW"):
        return count_zh(text)
    if lang == "en":
        return count_en(text)
    if lang == "ko":
        return count_ko(text)
    if lang == "ru":
        return count_ru(text)
    if lang == "ja":
        return count_ja(text)
    return count_en(text)


def check_banned(text: str) -> list[str]:
    hits = []
    low = text.lower()
    for w in BANNED_EN:
        if w in low:
            hits.append(w)
    for w in BANNED_ZH:
        if w in text:
            hits.append(w)
    return hits


def fm(meta: dict) -> str:
    kw_lines = "\n".join(f"  - {k}" for k in meta["keywords"])
    return f"""---
title: "{meta['title']}"
slug: {meta['slug']}
date: "2026-08-06"
language: {meta['lang']}
page_type: Blog Post
category: {meta['category']}
author: Lovart Content Team
description: "{meta['description']}"
estimated_read: {meta.get('read', '9 min')}
difficulty: {meta.get('difficulty', 'beginner')}
tool: ChatCanvas, Brand Kit, Touch Edit, Design Agent
focus_keyword: {meta['focus']}
keywords:
{kw_lines}
tags:
  - lovart
  - {meta.get('tag', '404-recovery')}
seo_title: "{meta['seo_title']}"
seo_description: "{meta['seo_description']}"
seo_schema: FAQ
cover_url: {cover_url(meta['cover'])}
alt_text: {meta['slug']} — Lovart blog cover
status: ready
content_cluster: {meta.get('cluster', '404 recovery')}
releaseDate: "{DATE}"
publishedAt: "{DATE}"
---

"""


# ---------------------------------------------------------------------------
# Article bodies (paragraph style, no bullet lists in main sections)
# ---------------------------------------------------------------------------

PET_GROOMER_RU = """
# Brand Kit для груминг-салона: editable price card и compliance disclaimer (RU)

Русская страница `brand-kit-pet-groomer-lovart` отдавала 404, хотя запросы искали operational **Brand Kit** guide для pet groomer segment — не generic ranking «лучший AI дизайн». Груминг daily ops: price card стрижка/SPA для собак, Instagram carousel before/after, визитка записи, seasonal promo — цены и disclaimer про аллергию меняются часто, calm pet-friendly accent drift между feed и POP. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** и **Design Agent** фиксируют trust-heavy palette. KPI — «изменить цену за пять минут», не «первый wow poster».

## Четыре сценария pet groomer с высокой частотой

Первый — price card 4:5: readable стрижка/SPA цифры, disclaimer footer editable про аллергию и условия записи. Второй — before/after carousel slides 2–6: accent stripe того же thread, **Brand Kit** hex lock. Третий — визитка и booking card: bottom 20% CTA flat for **Touch Edit**. Четвёртый — seasonal promo «летний SPA»: дата и цена editable layer, не baked in pixels.

## Почему groomer promo ломается во вторник при смене цены

Смена «Стрижка ₽890» требует full regen thirty minutes, если цена baked в pixels. Slide 4 accent lottery в carousel. **Brand Kit** не sample из approved signage или prior export. Disclaimer про аллергию меняют одно слово — full regen вместо **Touch Edit** text band. Владелец салона не учит design jargon — нужны pass/fail fields у **Design Agent**.

## ChatCanvas brief contract (pet groomer Brand Kit RU)

Слабый brief: «сделай premium poster для грумера». Сильный: «Season promo 4:5 1080×1350, Brand Kit sage + cream from approved signage, headline top 15% flat for Touch Edit, цена bottom left safe zone, disclaimer footer editable про аллергию, запрет мелкого текста в render, slides 2–6 same thread, booking card 1:1 companion». **Design Agent** numeric fields — не clip «cinematic feel».

## Brand Kit из approved signage, визитки, prior export

Sample primary, accent, type role из approved signage, визитки, prior price card export — не stock marble как brand color. **ChatCanvas** same thread batch price card + carousel + booking export. Pet groomer — series work; memory beats surprise.

## Touch Edit меняет цену без crop pet hero

«SPA ₽1290» → «Member ₽1190»: **Touch Edit** CTA band, pet geometry и **Brand Kit** accent stripe сохранены. Full regen randomizes fur lighting — salon consistency cannot absorb thirty-minute reroll.

## Отличие от generic vet clinic Brand Kit slug

Vet slug покрывает clinical blue и medical disclaimer; groomer slug покрывает pet-friendly sage/cream, grooming price tiers, аллергия disclaimer. Оба regulated-adjacent, brief fields разные.

## Типичные ошибки

**Brand Kit** skipped. Цена baked. Новый prompt per promo. Disclaimer не editable. 404 не восстановлен. Fake «100% conversion lift» claims.

## Метрики

Минуты на price fix, accent drift count, export ratios per action. Восстановленный URL — stable RU pet groomer Brand Kit SOP link.
"""

SPA_BRAND_KIT_ZH = """
# 水疗会所 Brand Kit：疗程价目、预约 card 与合规 disclaimer 可编辑视觉

这条中文 URL `brand-kit-spa-lovart` 曾返回 404，搜索需要 spa segment 的 **Brand Kit** operational 指南，不是 generic「最好 AI 设计工具」榜单。水疗会所 daily ops：面部/身体疗程价目、会员 card、小红书/点评 cover、院内 POP — 改疗程价与 wellness disclaimer 勤，calm neutral accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 trust-heavy palette，KPI 是「改价 five 分钟」不是「第一张 wow」。

## 水疗会所四个高频场景

第一是疗程价目 card：面部、身体、套餐数字改得勤，手机 readable。第二是会员 card 与预约 cover：bottom 20% CTA flat for **Touch Edit**。第三是社媒 cover 4:5：headline 不挡 spa hero，wellness disclaimer footer editable。第四是季节 promo：日期与疗程价 editable layer，禁止 render 内小字。

## 为什么 spa promo 常卡在改价

改「面部 ¥599」要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 sage green。readable 价格 bake 进 pixels。**Brand Kit** 未从 approved VI、价目册取样 hex。wellness disclaimer 改一字触发 full regen — legal return 成本高。

## ChatCanvas brief 合同（水疗 Brand Kit 版）

弱 brief「帮我做高级 spa 海报」。强 brief：「季节 promo 4:5 1080×1350，Brand Kit sage + sand from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone，wellness disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread，会员 card 1:1 companion」。**Design Agent** numeric fields — 不能 QA「看起来高级」。

## Brand Kit 从 approved VI、价目册、prior export 取样

从已批准 VI、价目册、prior spa export 取样 primary、accent、type role。不用 stock marble 当会所色。**ChatCanvas** 同一 thread batch 多疗程 export。

## Touch Edit 改疗程价不改 spa hero crop

改「限时 ¥499」为「会员 ¥449」：**Touch Edit** 框 CTA 带，保持 spa geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — 会所承受不起 thirty-minute 重出。

## 与 pet groomer Brand Kit slug 的分工

pet groomer slug 覆盖宠物美容价目与过敏 disclaimer；本篇覆盖 spa 疗程价目、wellness disclaimer、calm neutral palette。segment 同属 service retail，品类字段不同。

## 常见失败

跳过 **Brand Kit**。价格 baked。每活动新 prompt。404 未修复。wellness disclaimer 未设 editable layer。编造疗效数据。

## 测量 ROI

改价一次几分钟、drift 几次、export 几种 ratio。404 修复给 spa ops stable Brand Kit SOP URL。
"""

GOOGLE_ADS_CHAT_ZH = """
# 如何用 ChatCanvas 对话生成 Google Ads 视觉：static-first 可编辑 CTA layer

这条中文 URL `how-to-chat-generate-google-ads-lovart` 曾返回 404，搜索需要 chat generate Google Ads 的 How-To，不是 generic「最好 AI 广告工具」榜单。Google Ads daily ops：Responsive Display、Performance Max asset、1200×628 与 1:1 square — 改 offer 与 disclaimer 勤，hex 易 drift。Lovart **ChatCanvas** 对话 brief、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 campaign palette，KPI 是「改 offer five 分钟」不是「第一张 wow」。本篇强调 static-first：CTA 与 disclaimer 在 editable layer，不在 render pixels 内 bake。

## Google Ads 四个高频 static asset layer

第一是 1200×628 landscape master：headline 与 disclaimer footer editable，CTA bottom 20% flat for **Touch Edit**。第二是 1:1 square 1200×1200：同 thread accent stripe。第三是 4:5 vertical 1080×1350：价格 bottom left safe zone readable。第四是 logo lockup companion：hex 一致 **Brand Kit**，**Design Agent** QA mismatch between ratio exports。

## 为什么 chat generate Google Ads 常卡在改 offer

对话 brief 停在「帮我做高级 Google 广告图」— **Design Agent** 无 pass/fail fields。改「开业 ¥99」要 full regen 三十分钟。asset group 4 accent drift。**Brand Kit** 未从 approved VI 取样。CTA baked in pixels — Tuesday price fix 触发整图重出。

## ChatCanvas 对话 brief 合同（Google Ads 版）

弱 brief「对话生成一张 Google 广告」。强 brief：「campaign X 1200×628 landscape，Brand Kit teal + sand from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone，disclaimer footer editable，禁止 render 内小字，square + vertical same thread，static-first CTA layer only」。**Design Agent** numeric fields — 不能 QA「看起来专业」。

## Brand Kit 从 approved VI、Google Ads asset library 取样

从已批准 VI、prior Google Ads export 取样 primary、accent、type role。**ChatCanvas** 同一 thread 对话迭代 brief，batch landscape + square + vertical export。不编造 Google Ads 定价或 fake performance 数据。

## Touch Edit 改 offer 不改 hero crop

改「限时 ¥79」为「会员 ¥69」：**Touch Edit** 框 CTA 带，保持 hero geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — 运营承受不起 thirty-minute 重出。static-first 意味着 clip 内无 baked 小字 offer。

## static-first CTA layer 与 Responsive Display spec

Google Responsive Display 要求多种 ratio；**Brand Kit** 作为 SSOT 保证 hex 一致。**Design Agent** 验 safe zone、readable price、hex drift vs Kit、disclaimer present。对话生成后先 static legal pass，再 optional motion companion elsewhere。

## 与 Brand Kit-only Google Ads slug 的分工

brand-kit Google Ads slug 重 Kit 取样 SOP；本篇重 **ChatCanvas** 对话 brief 迭代与 static-first CTA editable layer。intent 互补，brief 字段重叠但入口不同。

## 常见失败

对话 brief 形容词堆叠。跳过 **Brand Kit**。价格 baked。每 campaign 新 thread。404 未修复。编造 Google Ads ROI 数字。

## 测量 ROI

改 offer 一次几分钟、drift 几次、export 几种 ratio。404 修复给 chat generate Google Ads SOP stable URL。
"""

LEGAL_MARKETING_ZH = """
# 2027 法律营销视觉设计：ethical visuals 与可编辑 disclaimer SOP

这条中文 URL `legal-marketing-design-ethical-visuals-2027` 曾返回 404，搜索需要 legal marketing design ethical visuals 的 operational 指南，不是 generic「AI 替律师写广告」榜单。法律营销 daily ops：律所 promo、seminar flyer、LinkedIn/公众号 cover、合规 disclaimer — 改活动日期与执业领域 disclaimer 勤，trust-heavy navy/gold accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 professional palette。本篇强调 ethical visuals：不编造胜诉率、不 fake 客户 testimonial、disclaimer editable static layer。不构成法律意见 — 合规文案须律所 legal team 确认后 paste 到 **Touch Edit** text band。

## 法律营销四个高频 deliverable layer

第一是 seminar flyer 4:5：readable 活动主题，disclaimer footer editable 含「不构成法律意见」句。第二是 LinkedIn/公众号 cover：headline 不挡 professional hero，执业领域 disclaimer editable。第三是 email header 600×300：CTA flat for **Touch Edit**。第四是 landing companion static：offer 与 seminar 日期 match；**Design Agent** QA mismatch。禁止 render 内小字 compliance 句 — 须 editable layer。

## 为什么 legal marketing promo 常卡在 compliance 改字

改 disclaimer 一字触发 full regen 三十分钟。readable 执业领域说明 bake 进 pixels。**Brand Kit** 未从 approved VI、律所 media kit 取样 hex。团队用「高级律所风」形容词 brief — **Design Agent** 无 pass/fail fields。ethical visuals 要求：不暗示 guaranteed outcome，不 fake case result 数据。

## ChatCanvas brief 合同（legal marketing ethical visuals 版）

弱 brief「帮我做高级律所海报」。强 brief：「seminar X flyer 4:5 1080×1350，Brand Kit navy + gold from media kit，headline top 15% flat for Touch Edit，日期 bottom left safe zone，disclaimer footer editable 含 legal team approved 句，禁止 render 内小字，禁止 fake 胜诉率 claim，slide 2–4 same thread」。**Design Agent** numeric fields — 不能 QA「看起来权威」。

## Brand Kit 从 approved VI、律所 media kit 取样

从已批准 VI、律所 media kit、prior seminar export 取样 primary、accent、type role。不用 stock marble 当律所色。**ChatCanvas** 同一 thread batch flyer + cover + email header export。

## Touch Edit 改 disclaimer 不改 professional hero crop

改 seminar 日期或 disclaimer wording：**Touch Edit** text band，保持 professional geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — 律所 brand consistency sensitive。disclaimer 句须 legal team 原文 paste — 不 AI 编造 compliance 语言。

## ethical visuals 边界：什么不能做

不编造胜诉率、不 fake client count、不 unauthorized competitor 贬低、不 implied guaranteed outcome visual（如 gavel + 「100% win」）。visual 可以 professional 与 readable，不能 substitute legal advice。reader 须 consult qualified counsel for jurisdiction-specific rules。

## 与 generic law firm Brand Kit slug 的分工

generic slug 覆盖 VI 取样；本篇覆盖 2027 ethical visuals discipline、disclaimer editable layer、no fake legal claims。compliance 是 ops 字段，不是 decoration。

## 常见失败

disclaimer baked in pixels。AI 编造 compliance 句。fake 胜诉率 visual。跳过 **Brand Kit**。404 未修复。每活动新 prompt。

## 测量什么

disclaimer edit 一次几分钟、legal return count、accent drift 次数。404 修复给 legal marketing ethical visuals SOP stable URL。
"""

BATCH_CREATE_EN = """
# How to Batch Create Designs with AI (Bing): Static-First Campaign Series SOP

This English URL `how-to-batch-create-designs-ai-bing` returned 404 while searches wanted a practical guide to batch create designs with AI for Bing Ads and Microsoft Advertising — not a generic tool ranking with fabricated pricing. Batch ops mean ten asset variants share one **ChatCanvas** thread, one **Brand Kit** hex lock, and **Touch Edit** editable CTA layers — not ten unrelated prompts. Lovart **Design Agent** QA readable price, disclaimer present, accent drift vs Kit. KPI is «change offer in five minutes», not «first wow image».

## Four batch deliverable layers for Bing Ads

First, 1200×628 landscape master: headline and disclaimer footer editable, CTA bottom 20% flat for **Touch Edit**. Second, 1:1 square 1200×1200: same thread accent stripe. Third, 4:5 vertical 1080×1350: price bottom left safe zone readable on mobile. Fourth, logo lockup companion: hex matched **Brand Kit**, **Design Agent** catches mismatch between ratio exports in the batch.

## Why batch create workflows fail on Tuesday price changes

Ten variants generated with ten separate prompts — slide 4 accent lottery across the batch. Offer baked in pixels; changing «Launch $49» triggers full regen thirty minutes per asset. **Brand Kit** not sampled from approved VI or prior Bing export. Teams treat batch as speed demo, not series discipline.

## ChatCanvas brief contract (batch create Bing edition)

Weak brief: «batch create ten Bing ad designs». Strong brief: «Campaign X batch 1200×628 landscape, Brand Kit slate + coral from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, no small text in render, variants 2–10 same thread accent stripe, square + vertical companions same ChatCanvas thread». **Design Agent** numeric pass/fail fields — not «looks professional».

## Brand Kit as batch SSOT against hex drift

Sample primary, accent, type role from approved VI and prior Microsoft Advertising export — not random stock gradient as brand color. One **ChatCanvas** thread batches landscape + square + vertical export. Batch create is series work; memory beats surprise.

## Touch Edit changes offer without hero crop across the batch

«Limited $79» to «Member $69»: **Touch Edit** CTA band on each static master, hero geometry and **Brand Kit** accent stripe preserved. Full regen per variant randomizes lighting — batch ops cannot absorb ten thirty-minute rerolls.

## Static-first before optional motion companion

Order: static legal pass on disclaimer → variant A/B still → winner still becomes thread master for remaining batch slots → optional subtle motion elsewhere. **Touch Edit** price change within five minutes — ops viable for weekly Bing cadence. No fabricated Microsoft Advertising ROI numbers.

## Distinction from single-asset AI poster demos

Single-asset demos win first-frame wow; batch ops win on Tuesday price fix and multi-ratio hex consistency across ten slots. This guide covers buyer criteria for revision-heavy Microsoft Advertising promo.

## Common failures

Ten unrelated prompts. **Brand Kit** skipped. Price baked. New thread per variant. 404 URL not restored. Fake Bing performance benchmarks.

## Metrics

Minutes per offer fix across batch, accent drift count, export ratios per action. Restored URL as stable EN batch create designs AI Bing SOP link.
"""

BAKERY_ZHTW = """
# 手工烘焙坊 Design Agent 選型：改開幕價比第一張 wow 更重要

這條繁中 URL `ai-design-agent-for-artisan-bakery-branding` 曾 404，搜尋需要 artisan bakery segment 的 **Design Agent** 選型指南，不是 generic「最好 AI 設計工具」榜單。手工烘焙 daily ops：季節口味 promo、外送平台 cover、門市 POP、會員 card — 改口味價與過敏 disclaimer 勤，warm pastry accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 appetite-forward palette，KPI 是「改價 five 分鐘」不是「第一張 wow」。

## 手工烘焙四個高頻場景

第一是季節口味 promo 4:5：readable 價格，過敏 disclaimer footer editable。第二是外送平台 cover：bottom 20% CTA flat for **Touch Edit**。第三是門市 POP 與會員 card：hex 一致 **Brand Kit**。第四是 Instagram carousel slides 2–6：同 thread accent stripe，**Design Agent** QA mismatch between ratio exports。

## 為什麼 bakery promo 常卡在改價

改「可頌 NT$85」要 full regen 三十分鐘。carousel slide 4 accent drift 成另一個 butter gold。readable 價格 bake 進 pixels。**Brand Kit** 未從 approved packaging、價目取樣 hex。過敏 disclaimer 改一字觸發 full regen。

## ChatCanvas brief 合同（artisan bakery 版）

弱 brief「幫我做高級烘焙海報」。強 brief：「season promo 4:5 1080×1350，Brand Kit butter gold + cream from packaging，headline top 15% flat for Touch Edit，價格 bottom left safe zone，過敏 disclaimer footer editable，禁止 render 內小字，slide 2–6 同 thread，外送 cover 1:1 companion」。**Design Agent** numeric fields — 不能 QA「看起來好吃」。

## Brand Kit 從 approved packaging、價目、prior export 取樣

從已批准 packaging、價目、prior bakery export 取樣 primary、accent、type role。不用 stock marble 當烘焙色。**ChatCanvas** 同一 thread batch promo + cover + POP export。

## Touch Edit 改口味價不改 pastry hero crop

改「限時 NT$79」為「會員 NT$69」：**Touch Edit** 框 CTA 帶，保持 pastry geometry 與 **Brand Kit** accent stripe。full regen random 改 lighting — 烘焙坊承受不起 thirty-minute 重出。

## 與 food stall Brand Kit slug 的分工

food stall slug 重夜市、外送 NT$ 價目；本篇重 artisan bakery branding、季節口味、過敏 disclaimer、warm pastry palette。segment 同属 F&B，brief 字段不同。

## 常見失敗

跳過 **Brand Kit**。價格 baked。每活動新 prompt。404 未修復。過敏 disclaimer 未設 editable layer。編造銷售數據。

## 測量 ROI

改價一次幾分鐘、drift 幾次、export 幾種 ratio。404 修復給 TW artisan bakery Design Agent SOP URL。
"""

TIKTOK_ADS_ZHTW = """
# 如何用 ChatCanvas 對話生成 TikTok 廣告視覺：static-first 可編輯 CTA layer

這條繁中 URL `how-to-chat-generate-tiktok-ads-lovart` 曾 404，搜尋需要 chat generate TikTok ads 的 How-To，不是 generic「最好 AI 短視頻工具」榜單。TikTok Ads daily ops：9:16 vertical、1:1 square companion、spark ads static cover — 改 offer 與 disclaimer 勤，hex 易 drift。Lovart **ChatCanvas** 對話 brief、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 campaign palette。本篇強調 static-first：CTA 與 disclaimer 在 editable layer，不在 clip pixels 內 bake。

## TikTok Ads 四個高頻 static asset layer

第一是 9:16 vertical 1080×1920 master：headline top third readable，bottom 20% CTA flat for **Touch Edit**。第二是 1:1 square 1080×1080：同 thread accent stripe。第三是 spark ads static cover companion：disclaimer footer editable。第四是 landing static hero：offer match vertical thumb；**Design Agent** QA mismatch。

## 為什麼 chat generate TikTok ads 常卡在改 offer

對話 brief 停在「幫我做 viral TikTok 廣告」— **Design Agent** 無 pass/fail fields。改「開幕 NT$999」要 full regen 三十分鐘。slide 4 accent drift。**Brand Kit** 未取樣。CTA baked in clip pixels — Tuesday price fix 觸發整段 reroll。

## ChatCanvas 對話 brief 合同（TikTok Ads 版）

弱 brief「對話生成 TikTok 廣告」。強 brief：「campaign X 9:16 1080×1920，Brand Kit coral + charcoal from media kit，headline top 15% flat for Touch Edit，價格 bottom left safe zone，disclaimer footer editable，禁止 render 內小字，square companion same thread，static-first CTA layer only」。**Design Agent** numeric fields — 不能 QA「看起來 viral」。

## Brand Kit 從 approved VI、prior TikTok export 取樣

從已批准 VI、prior TikTok export 取樣 primary、accent、type role。**ChatCanvas** 同一 thread 對話迭代 brief，batch vertical + square export。不編造 TikTok Ads 定價或 fake performance 數據。

## Touch Edit 改 offer 不改 vertical hero crop

改「限時 NT$799」為「早鳥 NT$699」：**Touch Edit** 框 CTA 帶，保持 hero geometry 與 **Brand Kit** accent stripe。full regen random 改 lighting — 運營承受不起 thirty-minute reroll。static-first 意味 clip 內無 baked 小字 offer。

## static-first 再 optional motion hook

順序：static legal pass on disclaimer → variant A/B still → winner still 成 thread master → optional subtle motion hook elsewhere。**Touch Edit** price change 五分鐘內 — ops viable for weekly TikTok cadence。

## 與 step-by-step TikTok ads slug 的分工

step-by-step slug 重無 Photoshop 入門；本篇重 **ChatCanvas** 對話 brief 迭代與 static-first CTA editable layer。intent 互補。

## 常見失敗

對話 brief 形容詞堆疊。跳過 **Brand Kit**。價格 baked。每 campaign 新 thread。404 未修復。編造 TikTok ROI 數字。

## 測量 ROI

改 offer 一次幾分鐘、drift 幾次、export 幾種 ratio。404 修復給 chat generate TikTok ads SOP stable URL。
"""

PODCASTER_DE = """
# Bester AI Design Agent für Podcaster (DE): Episode-Titel editierbar vor dem Wow

Diese deutsche URL `best-ai-design-agent-for-podcaster` lieferte 404, während Suchen nach einem ehrlichen Design-Agent-Guide für Podcaster kamen — nicht nach einem generic Tool-Ranking. Podcaster daily ops: Cover Art 3000×3000, YouTube thumb 1280×720, Shorts cover 9:16, Patreon banner — Episode-Titel und Sponsor-Disclaimer ändern sich oft, accent color drift zwischen Plattformen. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** und **Design Agent** fixieren channel palette. KPI ist „Episode-Titel in fünf Minuten ändern", nicht „erstes cinematic cover".

## Vier Podcaster-Deliverables mit hoher Frequenz

Erstens Cover Art 3000×3000: readable Show-Titel, face or logo safe zone. Zweitens YouTube thumb 1280×720: Episode-Titel top third flat for **Touch Edit**. Drittens Shorts cover 9:16: bottom 20% CTA flat. Viertens Patreon banner: disclaimer footer editable wenn Sponsor, **Brand Kit** hex lock.

## Warum Podcaster-Workflows am Dienstag bei Titel-Änderung scheitern

„Ep. 12" zu „Ep. 13" ändern kostet full regen thirty minutes, wenn Titel in pixels baked. Carousel slide 4 accent lottery. **Brand Kit** nicht aus channel banner oder prior cover export gesampelt. Creator brief endet mit „premium cinematic" — **Design Agent** hat keine pass/fail fields.

## ChatCanvas brief-Vertrag (Podcaster DE)

Schwach: „make me a viral podcast cover". Stark: „Series X Ep. 13 cover 3000×3000, Brand Kit coral + charcoal from channel banner, title top 15% flat for Touch Edit, sponsor line bottom left safe zone, disclaimer footer editable, YouTube 1280×720 same thread". **Design Agent** QA readable title at reduced size — nicht clip „cinematic feel".

## Brand Kit aus channel banner und prior export sampeln

Sample primary, accent, type role aus approved channel art, prior cover export — kein random stock gradient als channel color. **ChatCanvas** same thread batch cover + YouTube + Shorts export.

## Touch Edit ändert Episode-Titel ohne face crop

„Summer Special" zu „Autumn Special": **Touch Edit** rahmt title band, hält face geometry und **Brand Kit** accent stripe. Full regen randomisiert expression — channel consistency cannot absorb that.

## Static-first vor optional motion hook

Reihenfolge: static cover legal pass → variant A/B → winner becomes thread master → optional subtle motion intro elsewhere. **Touch Edit** title change within five minutes — ops viable for weekly upload cadence.

## Abgrenzung zu pure audio-only tools

Audio tools win recording; podcaster ops win on title and sponsor line edits across ten episodes. This guide covers buyer criteria for revision-heavy channel art.

## Typische Fehler

**Brand Kit** überspringen. Titel baked in pixels. Neuer prompt pro Episode. Sponsor disclaimer fehlt. 404 URL nicht wiederhergestellt.

## Metriken

Minuten pro Titel-Fix, accent drift count, export ratios per upload week. Wiederhergestellte URL als stable DE podcaster Design Agent SOP link.
"""

COURSE_CREATOR_JA = """
# コースクリエイター向け最適 AI Design Agent：早割価格を5分で直す

この日本語 URL `best-ai-design-agent-for-course-creator` は 404 でしたが、検索意図は course creator segment の **Design Agent** 選定ガイドです。generic「最高 AI デザインツール」ランキングではありません。コース運営 daily ops：サムネイル、募集チラシ、live カバー、早割カウントダウン — 開講日と価格変更が頻繁で、accent color が slide 4 で drift しやすい。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** で campaign palette を固定。KPI は「価格変更 5 分以内」であり「最初の wow 画像」ではありません。

## コースクリエイター四つの高頻度 deliverable

第一に募集チラシ 4:5：readable 価格、disclaimer footer editable。第二に YouTube/Zoom live カバー 16:9：headline top 15% flat for **Touch Edit**。第三にサムネイル grid 1280×720：同 thread accent stripe。第四に早割カウントダウン static：日付と価格 editable layer、pixels に bake 禁止。

## 火曜の価格変更で失敗する理由

「早割 ¥29,800」変更が full regen 30 分。carousel slide 4 accent lottery。**Brand Kit** 未設定。readable 価格が pixels baked。creator brief が「モダンで高級」で終わる — **Design Agent** に pass/fail フィールドなし。

## ChatCanvas brief 契約（course creator JP 版）

弱い brief：「高級コース募集ポスター」。強い brief：「cohort X 募集 4:5 1080×1350、Brand Kit navy + sand from media kit、headline top 15% flat for Touch Edit、価格 bottom left safe zone、disclaimer footer editable、render 内小文字禁止、slide 2–6 same thread、live カバー 16:9 companion」。**Design Agent** numeric fields — clip「シネマティック」ではない。

## Brand Kit を approved VI、prior export から sample

approved VI、prior cohort export から primary、accent、type role を sample。stock marble を brand color にしない。**ChatCanvas** same thread batch チラシ + live + サムネ export。

## Touch Edit で早割価格変更、hero crop 維持

「早割 ¥29,800」→「最終 ¥34,800」：**Touch Edit** CTA band、hero geometry と **Brand Kit** accent stripe 維持。full regen は lighting randomize — 週次 upload cadence に 30 分 reroll は不可。

## static-first 後 optional motion companion

順序：static legal pass on disclaimer → variant A/B still → winner thread master → optional subtle motion elsewhere。**Touch Edit** price change 5 分以内 — ops viable。

## zh Brand Kit course creator slug との分工

zh slug は Brand Kit SOP 中心。本篇は JP locale の **Design Agent** 選定、早割 editable layer、live カバー fields。locale 別 rewrite、逐句翻訳禁止。

## 典型ミス

**Brand Kit** skip。価格 baked。campaign ごと new prompt。404 未復旧。fake 受講者数 claim。

## 測定指標

価格 fix 何分、accent drift 回数、export ratio 数。復旧 URL は stable JP course creator Design Agent SOP link。
"""

POSTER_PRINTING_KO = """
# AI 포스터 디자인·인쇄 완전 가이드: static-first print-ready SOP

이 한국어 URL `complete-guide-ai-poster-design-printing`은 404였지만, 검색은 complete guide ai poster design printing을 원합니다 — generic AI poster tool ranking이 아닙니다. 포스터·인쇄 daily ops：A2/A3 promo、매장 POP、행사 현수막 — offer와 disclaimer 변경이 잦고, print CMYK와 screen hex가 conflict하기 쉽습니다. Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent**는 poster series를 static-first로：master artwork, bleed-safe variant, editable price layer. KPI는 「offer fix 5분」이지 「첫 wow poster」가 아닙니다.

## 포스터·인쇄 네 deliverable layer

첫째, static master A2/A3 300dpi intent — readable headline, disclaimer footer editable, bleed safe zone marked. 둘째, 매장 POP 4:5 companion — **Brand Kit** accent stripe 동일 thread. 셋째, social crop 1:1과 9:16 — **Design Agent** ratio export mismatch QA. 넷째, print proof companion — still CTA와 POP offer 일치 필수.

## 화요일 offer 변경에서 실패하는 이유

clip 안에 offer가 bake되고 print static에 **Touch Edit** layer가 없습니다. 「한정 ₩49,000」 변경이 full rerender — 30분. slide 4 accent lottery. **Brand Kit** 미설정. print CMYK preview와 screen hex drift — reprint cost.

## ChatCanvas brief 계약（poster printing KO）

약한 brief: 「멋진 인쇄 포스터」. 강한 brief: 「campaign X poster A2 300dpi intent, Brand Kit slate + coral from media kit, headline top 15% flat for Touch Edit, 가격 bottom left safe zone, disclaimer footer editable, bleed 3mm safe zone, variants 2–4 same thread, POP 4:5 companion」. **Design Agent** static acceptance QA — clip 「영화같은 느낌」 아님.

## Brand Kit으로 print·screen hex drift 방지

approved VI에서 primary, accent, type role sample — stock marble을 brand color로 쓰지 않음. **ChatCanvas** same thread batch poster + POP + social crop export. print vendor handoff前 **Design Agent** bleed check.

## Touch Edit으로 offer 변경 hero crop 유지

「한정 ₩79,000」→「회원 ₩69,000」: **Touch Edit** CTA band, hero geometry와 **Brand Kit** accent stripe 유지. full regen은 lighting randomize — reprint ops가 30분 reroll 감당 불가.

## static-first print proof workflow

순서: static legal pass on disclaimer → variant A/B still → winner still이 thread master → print proof export → optional motion elsewhere only. **Touch Edit** price change 5분 내 — ops viable before reprint deadline.

## fake print benchmark 없이 honest guide boundary

본문은 workflow SOP, fake vendor pricing, fake print quality benchmark 없음. reader는 **Design Agent** checklist로 자체 export review before vendor handoff.

## 흔한 실패

print bleed ignored. 가격 pixels baked. campaign마다 new prompt. **Brand Kit** skip. 404 미복구. CMYK preview skip.

## 측정 지표

offer fix 몇 분, reprint count, accent drift 횟수, export ratio 수. 복구된 URL이 stable KO complete guide ai poster design printing SOP link.
"""


# FAQ blocks — unique per article
FAQ = {
    "pet_groomer_ru": """
## FAQ

**Нужен Brand Kit для groomer?**  
Да — sample hex из signage и prior export, иначе slide 4 drift.

**Смена цены full regen?**  
Нет — Touch Edit five minutes на static price band.

**Disclaimer про аллергию editable?**  
Да — footer static layer, не baked in pixels.

**404 fix?**  
Stable RU pet groomer Brand Kit SOP URL.

**Fake conversion data?**  
Нет — только ops workflow.
""",
    "spa_brand_kit_zh": """
## FAQ

**水疗 Brand Kit 要先设吗？**  
要 — 从价目册与 approved VI 取样 hex，否则 slide 4 drift。

**改疗程价要 full regen 吗？**  
不要 — Touch Edit 五分钟改 static price band。

**wellness disclaimer 可编辑吗？**  
可以 — footer static layer，禁止 pixels baked。

**404 修复？**  
stable zh spa Brand Kit SOP URL。

**编造疗效数据？**  
不 — 本篇只讲 ops workflow。
""",
    "google_ads_chat_zh": """
## FAQ

**对话生成 Google Ads 要先 Brand Kit 吗？**  
要 — 从 media kit 取样 hex，同一 ChatCanvas thread batch 多 ratio。

**改 offer 要 full regen 吗？**  
不要 — Touch Edit 五分钟改 static CTA layer。

**CTA 可以 bake 在 render 里吗？**  
不可以 — static-first editable layer only。

**404 修复？**  
stable zh chat generate Google Ads SOP URL。

**编造 Google Ads ROI？**  
不 — 只描述 editable layer ops。
""",
    "legal_marketing_zh": """
## FAQ

**法律营销 visual 能 AI 写 disclaimer 吗？**  
不能 substitute legal advice — disclaimer 须 legal team 原文 paste 到 Touch Edit。

**能写胜诉率吗？**  
不能 — ethical visuals 禁止 fake outcome claim。

**改 disclaimer 要 full regen 吗？**  
不要 — Touch Edit text band 五分钟。

**404 修复？**  
stable zh legal marketing ethical visuals SOP URL。

**Brand Kit 角色？**  
hex SSOT，trust-heavy navy/gold palette。
""",
    "batch_create_en": """
## FAQ

**Batch create needs one ChatCanvas thread?**  
Yes — ten variants same thread accent stripe, not ten unrelated prompts.

**Tuesday price fix full regen?**  
No — Touch Edit five minutes on static CTA band per variant.

**Brand Kit before batch?**  
Yes — sample hex from media kit, prevents slide 4 drift across batch.

**404 fix?**  
Stable EN batch create designs AI Bing SOP URL.

**Fake Bing performance data?**  
No — ops workflow only.
""",
    "bakery_zhtw": """
## FAQ

**手工烘焙要先 Brand Kit 吗？**  
要 — 从 packaging 与价目取样 hex，否则 slide 4 drift。

**改口味价要 full regen 吗？**  
不要 — Touch Edit 五分钟改 static price band。

**过敏 disclaimer 可编辑吗？**  
可以 — footer static layer。

**404 修复？**  
stable zh-TW artisan bakery Design Agent SOP URL。

**编造销售数据？**  
不 — 本篇只讲 ops workflow。
""",
    "tiktok_ads_zhtw": """
## FAQ

**对话生成 TikTok ads 要先 Brand Kit 吗？**  
要 — 从 media kit 取样 hex，同一 ChatCanvas thread batch vertical + square。

**改 offer 要 full regen 吗？**  
不要 — Touch Edit 五分钟改 static CTA layer。

**CTA 可以 bake 在 clip 里吗？**  
不可以 — static-first editable layer only。

**404 修复？**  
stable zh-TW chat generate TikTok ads SOP URL。

**编造 TikTok ROI？**  
不 — 只描述 editable layer ops。
""",
    "podcaster_de": """
## FAQ

**Braucht Podcaster Brand Kit zuerst?**  
Ja — aus channel banner und prior cover export sampeln.

**Episode-Titel full regen?**  
Nein — Touch Edit title band in five minutes.

**Cover und YouTube same thread?**  
Ja — accent stripe und hex consistent.

**404 fix?**  
Stable DE podcaster Design Agent SOP URL.

**Sponsor disclaimer editable?**  
Ja — bottom safe zone als static layer.
""",
    "course_creator_ja": """
## FAQ

**コースクリエイターは Brand Kit 先？**  
はい — approved VI から hex sample、slide 4 drift 防止。

**早割価格変更 full regen？**  
いいえ — Touch Edit 5 分 static price band。

**live カバーとチラシ same thread？**  
はい — accent stripe 一致。

**404 復旧？**  
stable JP course creator Design Agent SOP URL。

**fake 受講者数？**  
いいえ — ops workflow のみ。
""",
    "poster_printing_ko": """
## FAQ

**포스터 인쇄前 Brand Kit 필요?**  
예 — approved VI에서 hex sample, print·screen drift 방지.

**offer 변경 full regen?**  
아니오 — Touch Edit 5분 static price band.

**bleed safe zone 필수?**  
예 — **Design Agent** print proof QA.

**404 복구?**  
stable KO complete guide ai poster design printing SOP URL.

**fake print benchmark?**  
아니오 — ops workflow만 설명.
""",
}


def expand_ru(topic: str, n: int) -> str:
    return f"""
## Полевая заметка {n}: {topic}

Первый brief заканчивается словом «premium» и проваливается: мелкая цена, badge на лице. Во втором проходе правьте только safe zone и обязательные поля. Thread **ChatCanvas** снижает accent drift на slide 4. В **{topic}** **Touch Edit** подтверждает fix цены за пять минут static-first. Full regen 30 минут — сначала **Brand Kit**. Восстановленный 404 URL — stable SOP link для RU pet groomer команд. **Design Agent** pass/fail checklist побеждает briefs-прилагательные.
"""


def expand_zh(topic: str, n: int) -> str:
    return f"""
## 实操补充 {n}：{topic}

很多小团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。{topic} 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。
"""


def expand_zhtw(topic: str, n: int) -> str:
    return f"""
## 實操補充 {n}：{topic}

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。{topic} 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。
"""


def expand_en(topic: str, n: int) -> str:
    return f"""
## Practice note {n}: {topic}

The first brief ends with "premium" and fails: small price text, badge over the subject. On the second pass, correct only safe zone and required fields. A **ChatCanvas** thread reduces accent drift on slide 4. In **{topic}**, **Touch Edit** confirms price change in five minutes static-first. Full regen thirty minutes — reset **Brand Kit** first. Restored 404 URL as stable SOP link for EN SMB and creator teams. **Design Agent** pass/fail checklist beats adjective briefs every time.
"""


def expand_de(topic: str, n: int) -> str:
    return f"""
## Praxisnotiz {n}: {topic}

Der erste Brief endet mit „premium" und scheitert: kleiner Preis, Badge über dem Objekt. Im zweiten Durchlauf nur safe zone und Pflichtfelder korrigieren. Ein **ChatCanvas**-Thread reduziert accent drift auf slide 4. In **{topic}** bestätigt **Touch Edit** Preisänderung in fünf Minuten static-first. Full regen 30 Minuten — zuerst **Brand Kit** neu setzen. Wiederhergestellte 404-URL als stable SOP-Link für DACH Podcaster-Teams. **Design Agent** pass/fail checklist schlägt Adjektiv-Briefs.
"""


def expand_ja(topic: str, n: int) -> str:
    return f"""
## 現場メモ {n}：{topic}

初回 brief が「モダン」で終わると価格文字が小さく badge が顔を隠します。二回目は safe zone と必須フィールドのみ修正。**Design Agent** と **ChatCanvas** で thread を維持すると carousel slide 4 の accent drift が減ります。{topic} で **Touch Edit** が 5 分以内に価格修正できれば static-first が成立。30 分 full regen なら **Brand Kit** からやり直し。404 復旧 URL は JP コースクリエイター ops 向け stable link です。
"""


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 실습 보충 {n}: {topic}

첫 brief가 형용사만 쌓이면 그림은 예쁘지만 가격 글자가 작고 배지가 hero를 가립니다. 두 번째는 safe zone과 필수 필드만 수정. **ChatCanvas** thread가 slide 4 accent drift를 줄입니다. **{topic}**에서 **Touch Edit** 가격 수정 5분이면 static-first 입증. full regen 30분이면 **Brand Kit**부터 재설정. 복구된 404 URL이 stable SOP link. **Design Agent** pass/fail checklist가 형용사 brief보다 낫습니다.
"""


ARTICLES = [
    {
        "rank": 194,
        "key": "pet_groomer_ru",
        "lang": "ru",
        "slug": "brand-kit-pet-groomer-lovart",
        "cover": "059",
        "category": "Best Practice",
        "title": "Brand Kit для груминг-салона: editable price card (RU)",
        "seo_title": "Pet Groomer Brand Kit — RU ChatCanvas SOP",
        "description": "RU 404 fix: pet groomer Brand Kit、Touch Edit 改价、disclaimer editable。",
        "seo_description": "Groomer：price card、carousel、аллергия disclaimer、Design Agent QA。",
        "focus": "brand kit pet groomer lovart",
        "keywords": ["pet groomer brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Pet Groomer Brand Kit RU",
        "body": PET_GROOMER_RU,
        "expand_topic": "RU pet groomer Brand Kit workflow",
    },
    {
        "rank": 195,
        "key": "spa_brand_kit_zh",
        "lang": "zh",
        "slug": "brand-kit-spa-lovart",
        "cover": "060",
        "category": "Best Practice",
        "title": "水疗会所 Brand Kit：疗程价目与合规 disclaimer 可编辑视觉",
        "seo_title": "Spa Brand Kit — ChatCanvas 水疗 SOP",
        "description": "404 修复：spa Brand Kit、疗程价目、wellness disclaimer editable。",
        "seo_description": "水疗：价目 card、会员 cover、Touch Edit 改价、Design Agent QA。",
        "focus": "brand kit spa lovart",
        "keywords": ["水疗 brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Spa Brand Kit ZH",
        "body": SPA_BRAND_KIT_ZH,
        "expand_topic": "spa Brand Kit mainland workflow",
    },
    {
        "rank": 196,
        "key": "google_ads_chat_zh",
        "lang": "zh",
        "slug": "how-to-chat-generate-google-ads-lovart",
        "cover": "061",
        "category": "How-To",
        "title": "如何用 ChatCanvas 对话生成 Google Ads 视觉",
        "seo_title": "Chat Generate Google Ads — ChatCanvas static-first SOP",
        "description": "404 修复：chat generate Google Ads、static-first CTA editable layer。",
        "seo_description": "Google Ads：对话 brief、Brand Kit hex lock、Touch Edit 改 offer。",
        "focus": "how to chat generate google ads lovart",
        "keywords": ["chat generate google ads", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Chat Generate Google Ads ZH",
        "body": GOOGLE_ADS_CHAT_ZH,
        "expand_topic": "chat generate Google Ads static-first workflow",
    },
    {
        "rank": 197,
        "key": "legal_marketing_zh",
        "lang": "zh",
        "slug": "legal-marketing-design-ethical-visuals-2027",
        "cover": "062",
        "category": "Industry Solution",
        "title": "2027 法律营销视觉设计：ethical visuals 与可编辑 disclaimer",
        "seo_title": "Legal Marketing Ethical Visuals 2027 — ChatCanvas SOP",
        "description": "404 修复：legal marketing ethical visuals、disclaimer editable、no fake legal claims。",
        "seo_description": "法律营销：ethical visuals、Touch Edit disclaimer、不构成法律意见。",
        "focus": "legal marketing design ethical visuals 2027",
        "keywords": ["法律营销视觉", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Legal Marketing Ethical Visuals 2027 ZH",
        "body": LEGAL_MARKETING_ZH,
        "expand_topic": "legal marketing ethical visuals 2027 workflow",
    },
    {
        "rank": 198,
        "key": "batch_create_en",
        "lang": "en",
        "slug": "how-to-batch-create-designs-ai-bing",
        "cover": "063",
        "category": "How-To",
        "title": "How to Batch Create Designs with AI (Bing): Static-First SOP",
        "seo_title": "Batch Create Designs AI Bing — ChatCanvas SOP",
        "description": "404 fix: batch create designs AI Bing, Brand Kit hex lock, Touch Edit CTA layer.",
        "seo_description": "Bing batch: one ChatCanvas thread, multi-ratio export, Design Agent QA.",
        "focus": "how to batch create designs ai bing",
        "keywords": ["batch create designs ai bing", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Batch Create Designs AI Bing EN",
        "body": BATCH_CREATE_EN,
        "expand_topic": "batch create designs AI Bing workflow",
    },
    {
        "rank": 199,
        "key": "bakery_zhtw",
        "lang": "zh-TW",
        "slug": "ai-design-agent-for-artisan-bakery-branding",
        "cover": "064",
        "category": "Industry Solution",
        "title": "手工烘焙坊 Design Agent 選型：改開幕價比 wow 更重要",
        "seo_title": "Artisan Bakery Design Agent — TW ChatCanvas SOP",
        "description": "404 修復：artisan bakery Design Agent、過敏 disclaimer、Touch Edit 改價。",
        "seo_description": "烘焙：季節 promo、外送 cover、Brand Kit hex lock。",
        "focus": "ai design agent for artisan bakery branding",
        "keywords": ["手工烘焙 design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Artisan Bakery Design Agent zh-TW",
        "body": BAKERY_ZHTW,
        "expand_topic": "TW artisan bakery Design Agent workflow",
    },
    {
        "rank": 200,
        "key": "tiktok_ads_zhtw",
        "lang": "zh-TW",
        "slug": "how-to-chat-generate-tiktok-ads-lovart",
        "cover": "065",
        "category": "How-To",
        "title": "如何用 ChatCanvas 對話生成 TikTok 廣告視覺",
        "seo_title": "Chat Generate TikTok Ads — TW static-first SOP",
        "description": "404 修復：chat generate TikTok ads、static-first CTA editable layer。",
        "seo_description": "TikTok Ads：對話 brief、Brand Kit、Touch Edit 改 offer。",
        "focus": "how to chat generate tiktok ads lovart",
        "keywords": ["chat generate tiktok ads", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Chat Generate TikTok Ads zh-TW",
        "body": TIKTOK_ADS_ZHTW,
        "expand_topic": "chat generate TikTok ads static-first workflow",
    },
    {
        "rank": 201,
        "key": "podcaster_de",
        "lang": "de",
        "slug": "best-ai-design-agent-for-podcaster",
        "cover": "011",
        "category": "Industry Solution",
        "title": "Bester AI Design Agent für Podcaster (DE)",
        "seo_title": "Podcaster Design Agent — DE ChatCanvas SOP",
        "description": "DE 404 fix: best AI design agent for podcaster，Cover Art、Touch Edit。",
        "seo_description": "Podcaster：Episode-Titel editable、Brand Kit、Design Agent QA。",
        "focus": "best ai design agent for podcaster",
        "keywords": ["podcaster ai design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Podcaster Design Agent DE",
        "body": PODCASTER_DE,
        "expand_topic": "DE podcaster Design Agent workflow",
    },
    {
        "rank": 202,
        "key": "course_creator_ja",
        "lang": "ja",
        "slug": "best-ai-design-agent-for-course-creator",
        "cover": "014",
        "category": "Industry Solution",
        "title": "コースクリエイター向け最適 AI Design Agent（JP）",
        "seo_title": "Course Creator Design Agent — JP ChatCanvas SOP",
        "description": "JP 404 fix: course creator Design Agent、早割 editable、Brand Kit。",
        "seo_description": "コース：募集チラシ、live カバー、Touch Edit 5分改价。",
        "focus": "best ai design agent for course creator",
        "keywords": ["course creator ai design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Course Creator Design Agent JA",
        "body": COURSE_CREATOR_JA,
        "expand_topic": "JP course creator Design Agent workflow",
    },
    {
        "rank": 203,
        "key": "poster_printing_ko",
        "lang": "ko",
        "slug": "complete-guide-ai-poster-design-printing",
        "cover": "018",
        "category": "Complete Guide",
        "title": "AI 포스터 디자인·인쇄 완전 가이드: static-first print SOP",
        "seo_title": "Complete Guide AI Poster Design Printing — KO SOP",
        "description": "KO 404 fix: complete guide ai poster design printing，Brand Kit、Touch Edit。",
        "seo_description": "포스터·인쇄：bleed safe zone、editable price layer、Design Agent QA。",
        "focus": "complete guide ai poster design printing",
        "keywords": ["ai poster design printing", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Complete Guide — AI Poster Design Printing KO",
        "body": POSTER_PRINTING_KO,
        "expand_topic": "KO ai poster design printing workflow",
    },
]

EXPAND_FN = {
    "ru": expand_ru,
    "zh": expand_zh,
    "zh-TW": expand_zhtw,
    "en": expand_en,
    "de": expand_de,
    "ja": expand_ja,
    "ko": expand_ko,
}

UNIT_MAP = {
    "zh": "CJK",
    "zh-TW": "CJK",
    "en": "words",
    "ko": "hangul",
    "ru": "cyrl",
    "de": "words",
    "pt": "words",
    "it": "words",
    "fr": "words",
    "ja": "chars",
}


def build_article(a: dict) -> str:
    lang = a["lang"]
    floor = FLOORS[lang]
    parts = [fm(a), a["body"].strip()]
    expand = EXPAND_FN[lang]
    topic = a["expand_topic"]
    n = 1
    while count_metric("\n".join(parts), lang) < floor:
        parts.append(expand(topic, n))
        n += 1
        if n > 80:
            break
    parts.append(FAQ[a["key"]].strip())
    parts.append(
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch19 content cluster.*\n"
    )
    return "\n\n".join(parts) + "\n"


def main():
    results = []
    for a in ARTICLES:
        text = build_article(a)
        lang = a["lang"]
        metric = count_metric(text, lang)
        floor = FLOORS[lang]
        banned = check_banned(text)
        placeholder = any(x in text for x in ("PLACEHOLDER", "TODO", "IMAGE PLACEHOLDER", "[REAL SCREENSHOT"))
        ok = metric >= floor and not banned and not placeholder
        path = OUT / f"{lang}-{a['slug']}.md"
        path.write_text(text, encoding="utf-8")
        results.append({
            "file": path.name,
            "lang": lang,
            "rank": a["rank"],
            "metric": metric,
            "floor": floor,
            "unit": UNIT_MAP[lang],
            "banned": banned,
            "placeholder": placeholder,
            "pass": ok,
            "cover": a["cover"],
        })

    print(f"{'RANK':>4} {'FILE':<90} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 135)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['rank']:>4} {r['file']:<90} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["file"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
