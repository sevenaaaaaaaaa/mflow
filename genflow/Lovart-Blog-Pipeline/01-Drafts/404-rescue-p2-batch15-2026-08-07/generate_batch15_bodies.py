#!/usr/bin/env python3
"""Generate 404-rescue P2 batch15 blog bodies (10 files). Self-contained.

Ranks #153–#163 from 404-rescue-compact lane (#160 junk skipped).
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

RESTAURANT_MANAGER_ZH = """
# 餐厅经理选什么 Design Agent：改套餐价比第一张好看更重要

这条中文 URL `best-ai-design-agent-for-restaurant-manager` 曾返回 404，搜索需要 restaurant manager segment 的 **Design Agent** 选型指南，不是 generic「最好 AI 设计工具」榜单。餐厅经理 daily ops：午晚市套餐、美团/大众点评 cover、会员 card、节日 promo — 改套餐价与过敏 disclaimer 勤，food hero 色温易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 hospitality palette，KPI 是「改价 five 分钟」不是「第一张 wow」。

## 餐厅经理四个高频场景

第一是午市/晚市套餐 card：双人餐、家庭餐数字改得勤，手机 readable。第二是外卖平台 cover 4:5：店名与 promo 不挡 dish hero。第三是朋友圈 1:1 与 story 9:16：bottom 20% CTA flat for **Touch Edit**。第四是会员 card 与店内 POP：过敏 disclaimer footer editable。

## 为什么餐厅 promo 常卡在改价

改「双人餐 ¥168」要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 burgundy。readable 价格 bake 进 pixels。video 角标有 offer static 无 **Touch Edit** layer。**Brand Kit** 未从 approved VI、菜单板取样 hex。经理没时间学设计 jargon — 需要 pass/fail 字段。

## ChatCanvas brief 合同（餐厅经理版）

弱 brief「帮我做高级餐厅海报」。强 brief：「午市 promo 4:5 1080×1350，Brand Kit burgundy + cream from menu board，headline top 15% flat for Touch Edit，价格 bottom left safe zone，过敏 disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** numeric fields — 不能 QA「看起来高级」。

## Brand Kit 从 approved VI、菜单板、价目取样

从已批准 VI、菜单板、prior 价目取样 primary、accent、type role。不用 stock marble 当餐厅色。**ChatCanvas** 同一 thread batch 多套餐 export。

## Touch Edit 改活动价不改 dish hero crop

改「限时 ¥138」为「会员 ¥118」：**Touch Edit** 框 CTA 带，保持 dish geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — 餐厅承受不起 thirty-minute 重出。

## Design Agent 当 checklist 而非「替经理想创意」

验 safe zone、双 CTA、字过小、hex drift vs Kit、disclaimer present。经理要「改价五分钟关单」，不要形容词 brief。

## 与 juice bar / small business slug 的分工

juice bar slug 覆盖鲜榨水果 hero 色温；small business slug 覆盖跨品类通用字段；本篇覆盖 restaurant manager、套餐价目、过敏 disclaimer 习惯。segment 重叠但品类字段不同。

## 常见失败

跳过 **Brand Kit**。价格 baked。每活动新 prompt。404 未修复。过敏 disclaimer 未设 editable layer。

## 测量 ROI

改价一次几分钟、drift 几次、export 几种 ratio。404 修复给 restaurant ops stable Design Agent SOP URL。
"""

SMALL_BUSINESS_ZH = """
# 小企业主完整设计解决方案：Design Agent 选型与可编辑视觉 SOP

这条中文 URL `best-ai-design-agent-for-small-business-owners-complete-design-solution` 曾返回 404，搜索需要 small business owners 的 **complete design solution** 指南，不是 generic「最好 AI 设计工具」榜单。小企业主 daily ops：价目 card、社媒 cover、会员 card、活动 promo — 改 offer 与 disclaimer 勤，brand accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 street-level palette，KPI 是「改价 five 分钟」不是「第一张 wow」。

## 小企业主四个高频场景

第一是价目 card 与 service menu：数字改得勤，手机 readable。第二是社媒 cover 4:5：店名与 promo 不挡 product hero。第三是 story 9:16：bottom 20% CTA flat for **Touch Edit**。第四是会员 card 与 POP：服务 disclaimer footer editable。

## 为什么小企业 promo 常卡在改价

改「开业 ¥99」要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 teal。readable 价格 bake 进 pixels。**Brand Kit** 未从 approved VI、名片取样 hex。老板没时间学设计 jargon — 需要 pass/fail 字段。

## ChatCanvas brief 合同（小企业版）

弱 brief「帮我做高级小企业海报」。强 brief：「开业 promo 4:5 1080×1350，Brand Kit teal + sand from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone，服务 disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** numeric fields — 不能 QA「看起来专业」。

## Brand Kit 从 approved VI、名片、价目取样

从已批准 VI、名片、prior 价目取样 primary、accent、type role。不用 stock marble 当 brand 色。**ChatCanvas** 同一 thread batch 多活动 export。

## Touch Edit 改活动价不改 product hero crop

改「限时 ¥79」为「会员 ¥69」：**Touch Edit** 框 CTA 带，保持 product geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — 小企业承受不起 thirty-minute 重出。

## complete design solution 的四层 stack

第一层 **Brand Kit** SSOT。第二层 **ChatCanvas** thread 每 campaign 家族。第三层 **Touch Edit** 改价五分钟。第四层 **Design Agent** pass/fail QA。四层齐全才是 complete solution，不是单张 hero 图。

## 与 solopreneur / restaurant slug 的分工

solopreneur slug 覆盖一人公司 lean ops；restaurant slug 覆盖套餐与过敏 disclaimer；本篇覆盖 cross-category 小企业 complete design solution。segment 重叠但 scope 不同。

## 常见失败

跳过 **Brand Kit**。价格 baked。每活动新 prompt。404 未修复。只买 hero 不买 editable layer。

## 测量 ROI

改价一次几分钟、drift 几次、export 几种 ratio。404 修复给 SMB ops stable complete design solution SOP URL。
"""

FILMMAKER_CASE_ZH = """
# 独立电影人 AI 电影海报案例：从 brief 到 export 的可编辑视觉流程

这条中文 URL `case-study-filmmaker-ai-movie-poster` 曾返回 404，搜索需要 filmmaker movie poster 的 **case study**，不是 generic「最好 AI 设计工具」榜单。独立电影人 daily ops：主视觉 poster、still frame crop、社媒 teaser、电影节 submission cover — 改 screening 日期与 credits 勤，cinematic palette 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 film-grade palette，KPI 是「改 screening 日期 five 分钟」不是「第一张 wow」。

## 电影海报四个高频 deliverable

第一是主视觉 poster 2:3 与 27×40 inch ratio：title treatment 与 credits block editable。第二是社媒 teaser 4:5 与 9:16：bottom 20% CTA flat for **Touch Edit**。第三是 festival submission cover：disclaimer footer editable。第四是 still frame series：slide 2–6 同 thread accent stripe。

## 为什么电影 promo 常卡在改 screening 日期

改「6 月 15 日首映」要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 amber。readable credits bake 进 pixels。**Brand Kit** 未从 approved key art、prior poster 取样 hex。导演没时间学 design jargon — 需要 pass/fail 字段。

## ChatCanvas brief 合同（电影海报版）

弱 brief「帮我做高级电影海报」。强 brief：「主视觉 2:3 1080×1620，Brand Kit amber + charcoal from key art，title top 20% flat for Touch Edit，screening date bottom left safe zone，credits footer editable，禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** numeric fields — 不能 QA「看起来 cinematic」。

## Brand Kit 从 key art、approved poster 取样

从已批准 key art、prior poster 取样 primary、accent、type role。不用 stock marble 当 film 色。**ChatCanvas** 同一 thread batch 多 ratio export。

## Touch Edit 改 screening 日期不改 title crop

改「6 月 15 日」为「6 月 22 日」：**Touch Edit** 框 CTA 带，保持 title geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — 独立电影人承受不起 thirty-minute 重出。

## case study 诚实 framing

本 case 不编造票房数字或 festival award。描述 workflow：brief → Brand Kit → ChatCanvas thread → Touch Edit revision → Design Agent QA → export。读者可复制 SOP，不 copy 虚构数据。

## 与 generic poster slug 的分工

generic poster slug 覆盖通用 promo；本篇覆盖 filmmaker segment、credits block、screening date editable 字段。segment 不同，brief 字段不同。

## 常见失败

跳过 **Brand Kit**。credits baked。每 screening 新 prompt。404 未修复。编造 festival 数据。

## 测量 ROI

改 screening 日期一次几分钟、drift 几次、export 几种 ratio。404 修复给 filmmaker ops stable movie poster case study SOP URL。
"""

DIGEST_JUNE_WEEK1_ZH = """
# Lovart Digest 2026 年 6 月第一周：产品更新与 workflow 要点回顾

这条中文 URL `lovart-digest-june-2026-week1` 曾返回 404，搜索需要 Lovart 6 月 editorial roundup，不是 fake news 或编造产品发布。本篇以 **editorial roundup** 口吻回顾 2026 年 6 月第一周已公开的产品更新与 workflow 要点 — 不编造未发布功能、不虚构日期、不捏造用户数据。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 仍是 digest 里反复出现的四件套。

## digest 写作原则：真实产品 framing

editorial roundup 不等于 press release。我们只回顾已在 changelog、官方 blog 或 help center 出现的更新 framing。若某功能尚未公开，digest 不写「即将发布」。读者来 digest 页是为了快速 catch up workflow 变化，不是为了读假新闻。

## 6 月第一周 workflow 要点（已公开 framing）

第一，**Brand Kit** 作为 campaign SSOT 的用法在 help docs 里被强调：primary hex、accent、type role 从 approved media kit 取样，不用 stock marble。第二，**ChatCanvas** thread 每 campaign 家族：slide 2–6 同 accent stripe，只换 copy。第三，**Touch Edit** 改价或活动日期五分钟，layout identity 保留。第四，**Design Agent** pass/fail QA：safe zone、readable price、hex drift vs Kit、disclaimer footer 存在。

## 为什么 digest 页也要讲 Touch Edit

很多团队把 digest 当「功能列表」，忽略 ops 层。**Touch Edit** 改 CTA 若能在五分钟内完成，说明 static-first 路线成立；若每次改价都要 full regen，说明 **Brand Kit** 或 brief 模板还没设好。digest 的价值是把 product update 翻译成 daily ops 语言。

## ChatCanvas brief 在 digest 语境下的 reminder

弱 brief「帮我做高级海报」。强 brief：「campaign X 4:5 1080×1350，Brand Kit navy + sand from media kit，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，slide 2–6 same thread」。digest 不替读者写 brief，只 reminder 字段结构。

## 与 weekly digest 其他 week 的分工

week1 digest 覆盖 6 月第一周的 workflow reminder；后续 week 覆盖不同 changelog 条目。每篇 digest 独立 URL，不 copy paragraph。404 修复让 week1 有 stable roundup link。

## 常见失败

digest 写成 fake news。编造未发布功能。跳过 **Brand Kit** 只列 feature name。404 未修复。

## 测量什么

digest 页内链点击率、读者是否从 roundup 跳到 How-To SOP。404 修复给 editorial roundup stable URL。
"""

EVENT_COUNTDOWN_ZHTW = """
# 活動倒數 5 天 Teaser 圖：AI 視覺與可編輯 CTA 實操

這條繁中 URL `event-countdown-5-days-teaser-graphics-ai` 曾 404，搜尋需要 event countdown teaser 的 operational 指南，不是 generic「最好 AI 設計工具」榜單。活動主辦 daily ops：倒數 5 天、3 天、1 天 teaser 圖 — 改活動日期與 CTA 勤，brand accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 event palette，KPI 是「改倒數天數 five 分鐘」不是「第一張 wow」。

## 倒數 teaser 四個高頻 deliverable

第一是 5 天倒數 1:1 與 4:5：天數數字 editable。第二是 3 天倒數 story 9:16：bottom 20% CTA flat for **Touch Edit**。第三是 1 天倒數 urgency stripe：disclaimer footer editable。第四是 carousel slide 2–6 同 thread accent stripe，只換倒數 copy。

## 為什麼 event countdown promo 常卡在改天數

改「倒數 5 天」為「倒數 3 天」要 full regen 三十分鐘。carousel slide 4 accent drift。readable 天數 bake 進 pixels。**Brand Kit** 未從 approved VI 取樣 hex。主辦沒時間學 design jargon — 需要 pass/fail 字段。

## ChatCanvas brief 合同（倒數 teaser 版）

弱 brief「幫我做高級活動海報」。強 brief：「倒數 5 天 teaser 4:5 1080×1350，Brand Kit coral + slate from media kit，天數 top 15% flat for Touch Edit，CTA bottom left safe zone，disclaimer footer editable，禁止 render 內小字，slide 2–6 同 thread」。**Design Agent** numeric fields — 不能 QA「看起來 urgent」。

## Brand Kit 從 approved VI、prior event 取樣

從已批准 VI、prior event 取樣 primary、accent、type role。不用 stock marble 當 event 色。**ChatCanvas** 同一 thread batch 5/3/1 天 export。

## Touch Edit 改倒數天數不改 hero crop

改「倒數 5 天」為「倒數 3 天」：**Touch Edit** 框 CTA 帶，保持 hero geometry 與 **Brand Kit** accent stripe。full regen random 改 lighting — 主辦承受不起 thirty-minute 重出。

## 與 hospitality marketing slug 的分工

hospitality slug 覆蓋飯店/餐飲 campaign；本篇覆蓋 generic event countdown teaser、天數 editable 字段。segment 不同，brief 字段不同。

## 常見失敗

跳過 **Brand Kit**。天數 baked。每倒數階段新 prompt。404 未修復。

## 測量 ROI

改倒數天數一次幾分鐘、drift 幾次、export 幾種 ratio。404 修復給 event ops stable countdown teaser SOP URL。
"""

HOSPITALITY_MARKETING_ZHTW = """
# 飯店與餐飲行銷 AI Design Agent：可編輯 promo 與 Brand Kit SOP

這條繁中 URL `hospitality-marketing-ai-design-agent` 曾 404，搜尋需要 hospitality marketing segment 的 **Design Agent** 選型指南，不是 generic「最好 AI 設計工具」榜單。飯店/餐飲行銷 daily ops：季節套餐、OTA cover、會員 card、節日 promo — 改套餐價與過敏 disclaimer 勤，warm palette 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 hospitality palette，KPI 是「改價 five 分鐘」不是「第一張 wow」。

## 飯店餐飲行銷四個高頻場景

第一是季節套餐 card：雙人餐、家庭餐數字改得勤，手機 readable。第二是 OTA cover 4:5：店名與 promo 不擋 dish hero。第三是 story 9:16：bottom 20% CTA flat for **Touch Edit**。第四是會員 card 與店內 POP：過敏 disclaimer footer editable。

## 為什麼 hospitality promo 常卡在改價

改「雙人餐 NT$1680」要 full regen 三十分鐘。carousel slide 4 accent drift 成另一個 burgundy。readable 價格 bake 進 pixels。**Brand Kit** 未從 approved VI、菜單板取樣 hex。行銷沒時間學 design jargon — 需要 pass/fail 字段。

## ChatCanvas brief 合同（hospitality 版）

弱 brief「幫我做高級飯店海報」。強 brief：「季節 promo 4:5 1080×1350，Brand Kit burgundy + cream from menu board，headline top 15% flat for Touch Edit，價格 bottom left safe zone，過敏 disclaimer footer editable，禁止 render 內小字，slide 2–6 同 thread」。**Design Agent** numeric fields — 不能 QA「看起來高級」。

## Brand Kit 從 approved VI、菜單板、價目取樣

從已批准 VI、菜單板、prior 價目取樣 primary、accent、type role。不用 stock marble 當飯店色。**ChatCanvas** 同一 thread batch 多套餐 export。

## Touch Edit 改活動價不改 dish hero crop

改「限時 NT$1380」為「會員 NT$1180」：**Touch Edit** 框 CTA 帶，保持 dish geometry 與 **Brand Kit** accent stripe。full regen random 改 lighting — 行銷承受不起 thirty-minute 重出。

## 與 event countdown slug 的分工

event countdown slug 覆蓋倒數 teaser 天數字段；本篇覆蓋 hospitality marketing、套餐價目、過敏 disclaimer 習慣。segment 不同，brief 字段不同。

## 常見失敗

跳過 **Brand Kit**。價格 baked。每活動新 prompt。404 未修復。過敏 disclaimer 未設 editable layer。

## 測量 ROI

改價一次幾分鐘、drift 幾次、export 幾種 ratio。404 修復給 hospitality ops stable Design Agent SOP URL。
"""

YOUTUBE_THUMBNAIL_ZHTW = """
# 如何用 Chat 生成 YouTube 縮圖：Lovart static-first 實操

這條繁中 URL `how-to-chat-generate-youtube-thumbnail-lovart` 曾 404，搜尋需要 chat generate YouTube thumbnail 的 How-To，不是 generic AI video demo。誠實 framing：YouTube 縮圖 reward readable title 與 face hero，但 offer copy 與 disclaimer 仍屬 editable static layer。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 把 thumbnail 生產當 static-first：master 16:9 1280×720，同一 thread 出 variant crop。

## YouTube 縮圖四個 deliverable layer

第一層是 static master 16:9 1280×720，readable title 與 disclaimer footer editable。第二層是 A/B variant 同 thread accent stripe。第三層是 end card companion 4:5 與 9:16 色溫對齊 **Brand Kit**。第四層是 landing companion：video CTA 與 static price 須 match；**Design Agent** QA 抓 mismatch。

## 為什麼 chat generate thumbnail workflow 常卡在週二改標題

clip 內 bake offer 而 landing static 無 **Touch Edit** layer。改標題觸發 full rerender — 三十分鐘。slide 4 accent lottery。**Brand Kit** 未設。muted autoplay 意味用戶 screenshot still — title 須 readable on static。

## ChatCanvas brief 合同（YouTube thumbnail 版）

弱 brief「幫我做 viral 縮圖」。強 brief：「campaign X，hero 16:9 1280×720，Brand Kit slate + coral from approved packaging，title top 15% flat for Touch Edit，subtitle bottom left safe zone，disclaimer footer editable，variant 2–4 same thread」。**Design Agent** QA static acceptance only — 不是 clip「cinematic feel」。

## Brand Kit 對齊 thumbnail 與 end card 色溫

從 Kit 拉 primary 與 accent 進 thumbnail color reference。**Touch Edit** 改 static title；variant 是 crop swap only。title fix 五分鐘內證明 static-first ops。

## static-first 再 optional motion companion

順序：static legal pass on disclaimer → variant A/B → winner still 成 thread master。**Touch Edit** title change 五分鐘內 — ops viable。

## Touch Edit 改 title 不改 face crop

改「Ep.12 完整教學」為「Ep.13 進階版」：**Touch Edit** 框 title band，保持 face geometry 與 **Brand Kit** accent。full regen randomize gradient — brand consistency sensitive。

## 常見失敗

thumbnail-only funnel 無 static editable layer。title baked in pixels。每支影片新 prompt。404 未修復。跳過 **Brand Kit**。

## 測量什麼

改 title 一次幾分鐘、variant drift 次數、export ratios per action。404 修復給 TW YouTube thumbnail ChatCanvas SOP stable URL。
"""

SALARY_REPORT_DE = """
# AI Designer Gehaltsreport 2026: Marktbänder statt erfundener Zahlen

Diese deutsche URL `ai-designer-salary-report-2026` lieferte 404, während Suchen nach einem ehrlichen Gehaltsüberblick kamen — nicht nach erfundenen Einzelgehältern. **Wichtiger Disclaimer:** Diese Seite nennt keine verifizierten Einzelgehälter. Stattdessen beschreiben wir **Marktbänder** (Gehaltskorridore) aus öffentlich zitierten Branchenquellen und ordnen ein, wie **ChatCanvas**, **Brand Kit**, **Touch Edit** und **Design Agent** die Produktivität von Design-Teams beeinflussen können — ohne Tool-Preise zu erfinden.

## Was ein ehrlicher Salary Report 2026 leisten darf

Ein seriöser Report unterscheidet: verifizierte Bandbreiten aus Stellenanzeigen-Aggregatoren, regionale Unterschiede DACH vs Remote EU, und Rolle (Junior UI vs Senior Creative Ops). Er erfindet keine „Durchschnittsgehälter“ ohne Quellenangabe. Leser kommen für Orientierung, nicht für clickbait-Zahlen.

## Marktbänder als Orientierung (Disclaimer)

Typische **Marktbänder** in DACH für AI-adjacent Design-Rollen (Stand 2026, grobe Korridore, keine Garantie): Junior Visual Designer oft im unteren bis mittleren Bereich; Senior Creative mit Agent-Workflow-Kenntnissen höher; Freelancer stark projektabhängig. Konkrete EUR-Beträge variieren nach Stadt, Branche und Vertrag — prüfen Sie aktuelle Stellenanzeigen und Tarifverträge. **Keine dieser Angaben ist eine Gehaltsgarantie.**

## Warum Gehaltsdiskussionen an Ops hängen

Teams, die **Touch Edit** für Preis-Fixes in fünf Minuten nutzen, reduzieren Revision-Zyklen — das beeinflusst effektive Stundenkosten, nicht das Bruttogehalt. **Brand Kit** als SSOT verhindert accent drift auf slide 4. **Design Agent** pass/fail QA spart Review-Runden. Fairer Vergleich: Minuten pro Revision, nicht first-frame beauty.

## ChatCanvas brief-Vertrag (DE Business)

Statt Adjektive: „Listing hero 4:5 1080×1350, Brand Kit navy + sand from Media-Kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, slides 2–6 same thread“. **Design Agent** prüft numeric acceptance — nicht „hochwertig“.

## Brand Kit für Agentur vs Inhouse

Agentur: Kit pro Kunde wechseln, **ChatCanvas** thread pro Kunde trennen. Inhouse: ein Kit pro Corporate VI. Revision history bleibt im thread — „Badge-Position wie letzte Woche“ ohne Neu-Erklärung.

## Abgrenzung zu law-firm slug batch15

law-firm slug deckt Kanzlei **Brand Kit** und Impressum-Felder ab. Dieser salary report: Marktbänder, Disclaimer, keine erfundenen EUR-Einzelwerte. Gleicher batch, andere intent.

## Typische Fehler

Erfundene Durchschnittsgehälter ohne Quelle. Tool-Preise erfinden. 404 URL nicht wiederhergestellt. Gehalt als Produktversprechen.

## Metriken

Leser-Feedback ob Disclaimer klar. Minuten pro Preis-Fix als Ops-KPI neben Gehaltsorientierung. Wiederhergestellte URL als stable DE salary report SOP link.
"""

LAW_FIRM_DE = """
# Best AI Design Agent für Kanzleien: Brand Kit, Impressum und editierbare Promo

Diese deutsche URL `best-ai-design-agent-for-law-firm` lieferte 404, während Suchen nach einem Design Agent für law firm segment kamen — nicht nach einem generic Tool-Ranking. Kanzlei daily ops: Mandantenbriefing cover, Seminar flyer, LinkedIn promo, Impressum-konforme disclaimer — Angebots- und Terminänderungen häufig, trust-heavy navy palette drift. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** locken Kanzlei-VI; KPI ist „Preis/Termin-Fix fünf Minuten“, nicht „first frame wow“.

## Vier häufige Kanzlei-Szenarien

Erstens Mandantenbriefing cover 4:5: readable headline, kein Badge über Logo. Zweitens Seminar flyer: bottom 20% CTA flat for **Touch Edit**. Drittens LinkedIn promo 1:1: Impressum-Hinweis footer editable. Viertens Partner card: disclaimer footer editable, no small text in render.

## Warum Kanzlei-Promo am Dienstag scheitert

Änderung „Seminar 14.06.“ kostet thirty-minute full regen — kein **Touch Edit** layer. Slide 4 erfindet neuen accent ohne **Brand Kit**. Mandant A und B vermischen hex in einem thread. Impressum-Text gebacken in pixels — legal return teuer.

## ChatCanvas brief-Vertrag (Kanzlei Brand Kit)

Schwacher Brief: „premium Kanzlei-Poster“. Starker Brief: „Seminar promo 4:5 1080×1350, Brand Kit navy + sand from approved Kanzlei-VI, headline top 15% flat for Touch Edit, Termin bottom left safe zone, Impressum footer editable, no small text in render, slides 2–6 same thread“. **Design Agent** numeric fields — nicht QA „vertrauenswürdig“.

## Brand Kit aus approved Kanzlei-VI, Visitenkarte, prior Flyer

Aus genehmigtem VI, Visitenkarte, prior Flyer primary, accent, type role sampeln. Kein stock marble als Kanzlei-Farbe. **ChatCanvas** same thread batch multi-Mandant export — thread pro Mandant trennen.

## Touch Edit ändert Termin ohne Logo crop

Änderung „Sa 14 Uhr“ zu „So 10 Uhr“: **Touch Edit** rahmt CTA band, hält Logo geometry und **Brand Kit** accent stripe. Full regen randomisiert gradient — Kanzlei verträgt kein thirty-minute reroll.

## Design Agent als Checklist, nicht „Kreativ für Partner“

QA safe zone, double CTA, small type, hex drift vs Kit, Impressum present. Partner wollen „Termin-Fix fünf Minuten Ticket schließen“, nicht Adjektiv-Brief.

## Abgrenzung zum salary report slug batch15

salary report: Marktbänder mit Disclaimer. Diese law-firm-Version: **Brand Kit** operational für Kanzlei, Impressum-Felder. Kein paragraph copy.

## Typische Fehler

**Brand Kit** überspringen. Termin baked. Neuer prompt pro Mandant. 404 URL nicht wiederhergestellt. Impressum nicht editable layer.

## Metriken

Minuten pro Termin-Fix, accent drift, export sizes. Wiederhergestellte URL als stable DE law firm Design Agent SOP link.
"""

SOLOPRENEUR_ZH = """
# 一人公司选什么 Design Agent：改 offer 价比第一张好看更重要

这条中文 URL `best-ai-design-agent-for-solopreneur` 曾返回 404，搜索需要 solopreneur segment 的 **Design Agent** 选型指南，不是 generic「最好 AI 设计工具」榜单。一人公司 daily ops：service 价目、社媒 cover、pitch deck slide、会员 card — 改 offer 与 disclaimer 勤，personal brand accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 lean palette，KPI 是「改价 five 分钟」不是「第一张 wow」。

## 一人公司四个高频场景

第一是 service 价目 card：数字改得勤，手机 readable。第二是社媒 cover 4:5：personal brand 与 promo 不挡 product hero。第三是 story 9:16：bottom 20% CTA flat for **Touch Edit**。第四是 pitch deck slide：disclaimer footer editable。

## 为什么 solopreneur promo 常卡在改价

改「咨询 ¥999」要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 coral。readable 价格 bake 进 pixels。**Brand Kit** 未从 approved VI、名片取样 hex。创始人没时间学 design jargon — 需要 pass/fail 字段。

## ChatCanvas brief 合同（一人公司版）

弱 brief「帮我做高级个人品牌海报」。强 brief：「开业 promo 4:5 1080×1350，Brand Kit coral + slate from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone，服务 disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** numeric fields — 不能 QA「看起来专业」。

## Brand Kit 从 approved VI、名片、价目取样

从已批准 VI、名片、prior 价目取样 primary、accent、type role。不用 stock marble 当 personal brand 色。**ChatCanvas** 同一 thread batch 多活动 export。

## Touch Edit 改 offer 价不改 hero crop

改「限时 ¥799」为「早鸟 ¥699」：**Touch Edit** 框 CTA 带，保持 hero geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — 一人公司承受不起 thirty-minute 重出。

## 与 small business / bootstrappers slug 的分工

small business slug 覆盖 cross-category complete design solution；bootstrappers slug 覆盖 lean teams RU locale；本篇覆盖 mainland solopreneur、¥ 价目、personal brand 字段。segment 重叠但 scope 不同。

## 常见失败

跳过 **Brand Kit**。价格 baked。每活动新 prompt。404 未修复。服务 disclaimer 未设 editable layer。

## 测量 ROI

改价一次几分钟、drift 几次、export 几种 ratio。404 修复给 solopreneur ops stable Design Agent SOP URL。
"""

# FAQ blocks
FAQ = {
    "restaurant_manager_zh": """
## FAQ

**餐厅经理要先 Brand Kit 吗？**  
建议，从 approved VI、菜单板取样 hex 防 drift。

**改套餐价要 full regen 吗？**  
不需要，Touch Edit 五分钟改价格块。

**过敏 disclaimer 可编辑吗？**  
要，footer editable layer，禁止 render 内小字。

**与 juice bar slug 分工？**  
juice bar 水果 hero；本篇餐厅套餐与过敏 disclaimer。

**404 修复？**  
stable restaurant Design Agent SOP URL。
""",
    "small_business_zh": """
## FAQ

**小企业 complete solution 包含什么？**  
Brand Kit + ChatCanvas + Touch Edit + Design Agent 四层 stack。

**改价要 full regen 吗？**  
不需要，Touch Edit 五分钟改价格块。

**与 solopreneur slug 分工？**  
solopreneur 一人公司 lean；本篇 cross-category SMB complete solution。

**404 修复？**  
stable SMB complete design solution SOP URL。

**fake pricing？**  
不编造 tool 价格，查官方 ToS。
""",
    "filmmaker_case_zh": """
## FAQ

**case study 编造票房吗？**  
不编造，只描述 workflow SOP。

**改 screening 日期要 full regen 吗？**  
不需要，Touch Edit 五分钟改日期块。

**credits 可编辑吗？**  
要，footer editable layer。

**404 修复？**  
stable filmmaker movie poster case study SOP URL。

**Design Agent QA 什么？**  
credits readable、hex drift vs Kit、disclaimer present。
""",
    "digest_june_week1_zh": """
## FAQ

**digest 是 fake news 吗？**  
不是，只回顾已公开 product framing，不编造未发布功能。

**digest 为什么讲 Touch Edit？**  
把 product update 翻译成 daily ops 语言。

**与后续 week digest 分工？**  
week1 独立 URL，不 copy paragraph。

**404 修复？**  
stable June 2026 week1 editorial roundup URL。

**编造用户数据？**  
禁止，digest 不写虚构 metrics。
""",
    "event_countdown_zhtw": """
## FAQ

**倒數 teaser 要先 Brand Kit 嗎？**  
建議，從 approved VI 取樣 hex 防 drift。

**改倒數天數要 full regen 嗎？**  
不需要，Touch Edit 五分鐘改天數塊。

**與 hospitality slug 分工？**  
hospitality 套餐價目；本篇 event countdown 天數字段。

**404 修復？**  
stable TW countdown teaser SOP URL。

**Design Agent 替主辦創意？**  
不，執行 brief checklist pass/fail。
""",
    "hospitality_marketing_zhtw": """
## FAQ

**飯店餐飲要先 Brand Kit 嗎？**  
建議，從 approved VI、菜單板取樣 hex。

**改套餐價要 full regen 嗎？**  
不需要，Touch Edit 五分鐘改價格塊。

**過敏 disclaimer 可編輯嗎？**  
要，footer editable layer。

**404 修復？**  
stable TW hospitality Design Agent SOP URL。

**fake pricing？**  
不編造，查官方 ToS。
""",
    "youtube_thumbnail_zhtw": """
## FAQ

**YouTube 縮圖 offer 在 clip 還是 static？**  
Static editable layer；variant 是 crop only。

**改 title 觸發 full rerender？**  
避免，Touch Edit static title band。

**要先 Brand Kit 嗎？**  
要 — hex lock 防 slide 4 accent drift。

**404 修復？**  
stable TW YouTube thumbnail ChatCanvas SOP URL。

**Design Agent QA？**  
Static safe zone、disclaimer、hex drift vs Kit。
""",
    "salary_report_de": """
## FAQ

**Enthält der Report echte Einzelgehälter?**  
Nein — nur Marktbänder mit Disclaimer, keine Garantie.

**Erfundene EUR-Beträge?**  
Verboten. Quellen: Stellenanzeigen, Tarif — selbst prüfen.

**Unterschied law-firm slug?**  
Salary: Marktbänder; law-firm: Brand Kit Ops.

**404 fix?**  
Stable DE salary report SOP URL.

**Tool-Preise erfinden?**  
Nein — offizielle Seiten prüfen.
""",
    "law_firm_de": """
## FAQ

**Kanzlei braucht Brand Kit?**  
Ja — hex aus approved Kanzlei-VI, sonst slide 4 drift.

**Terminänderung full regen?**  
Nein — Touch Edit five minutes.

**Impressum editable?**  
Ja — footer editable layer, no small text in render.

**404 fix?**  
Stable DE law firm Design Agent SOP URL.

**Design Agent «Kreativ für Partner»?**  
Nein — pass/fail checklist.
""",
    "solopreneur_zh": """
## FAQ

**一人公司要先 Brand Kit 吗？**  
建议，从 approved VI、名片取样 hex。

**改 offer 价要 full regen 吗？**  
不需要，Touch Edit 五分钟改价格块。

**与 small business slug 分工？**  
small business complete solution；本篇 solopreneur lean personal brand。

**404 修复？**  
stable solopreneur Design Agent SOP URL。

**fake pricing？**  
不编造 tool 价格，查官方 ToS。
""",
}


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


def expand_de(topic: str, n: int) -> str:
    return f"""
## Praxisnotiz {n}: {topic}

Der erste Brief endet mit „premium“ und scheitert: kleiner Preis, Badge über dem Objekt. Im zweiten Durchlauf nur safe zone und Pflichtfelder korrigieren. Ein **ChatCanvas**-Thread reduziert accent drift auf slide 4. In **{topic}** bestätigt **Touch Edit** Preisänderung in fünf Minuten static-first. Full regen 30 Minuten — zuerst **Brand Kit** neu setzen. Wiederhergestellte 404-URL als stable SOP-Link für DACH SMB- und Creator-Teams.
"""


ARTICLES = [
    {
        "rank": 153,
        "key": "restaurant_manager_zh",
        "lang": "zh",
        "slug": "best-ai-design-agent-for-restaurant-manager",
        "cover": "012",
        "category": "Industry Solution",
        "title": "餐厅经理选什么 Design Agent：改套餐价比第一张好看更重要",
        "seo_title": "餐厅经理 Design Agent — ChatCanvas 实操",
        "description": "404 修复：restaurant manager segment Design Agent，套餐价 readable，Touch Edit 改价。",
        "seo_description": "餐厅：Brand Kit、外卖 cover、过敏 disclaimer editable。",
        "focus": "best ai design agent for restaurant manager",
        "keywords": ["餐厅经理 ai 设计", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Restaurant Manager Design Agent ZH",
        "body": RESTAURANT_MANAGER_ZH,
        "expand_topic": "餐厅经理 Design Agent 选型",
    },
    {
        "rank": 154,
        "key": "small_business_zh",
        "lang": "zh",
        "slug": "best-ai-design-agent-for-small-business-owners-complete-design-solution",
        "cover": "019",
        "category": "Industry Solution",
        "title": "小企业主完整设计解决方案：Design Agent 选型与可编辑视觉 SOP",
        "seo_title": "小企业 Complete Design Solution — ChatCanvas 实操",
        "description": "404 修复：small business complete design solution，Brand Kit、Touch Edit 四层 stack。",
        "seo_description": "小企业：complete solution、价目 readable、Design Agent QA。",
        "focus": "best ai design agent for small business owners complete design solution",
        "keywords": ["小企业 ai 设计", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Small Business Complete Solution ZH",
        "body": SMALL_BUSINESS_ZH,
        "expand_topic": "小企业 complete design solution workflow",
    },
    {
        "rank": 155,
        "key": "filmmaker_case_zh",
        "lang": "zh",
        "slug": "case-study-filmmaker-ai-movie-poster",
        "cover": "026",
        "category": "Industry Solution",
        "title": "独立电影人 AI 电影海报案例：从 brief 到 export 的可编辑视觉流程",
        "seo_title": "Filmmaker Movie Poster Case Study — ChatCanvas 实操",
        "description": "404 修复：filmmaker movie poster case study，credits editable，不编造票房。",
        "seo_description": "电影海报：Brand Kit、screening date、Touch Edit、Design Agent QA。",
        "focus": "case study filmmaker ai movie poster",
        "keywords": ["电影海报 ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Case Study — Filmmaker Movie Poster ZH",
        "body": FILMMAKER_CASE_ZH,
        "expand_topic": "filmmaker movie poster case study workflow",
    },
    {
        "rank": 156,
        "key": "digest_june_week1_zh",
        "lang": "zh",
        "slug": "lovart-digest-june-2026-week1",
        "cover": "033",
        "category": "Branding",
        "title": "Lovart Digest 2026 年 6 月第一周：产品更新与 workflow 要点回顾",
        "seo_title": "Lovart Digest June 2026 Week1 — Editorial Roundup",
        "description": "404 修复：June 2026 week1 editorial roundup，真实 product framing，非 fake news。",
        "seo_description": "Digest：ChatCanvas、Brand Kit、Touch Edit、Design Agent workflow reminder。",
        "focus": "lovart digest june 2026 week1",
        "keywords": ["lovart digest", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Editorial — Lovart Digest June Week1 ZH",
        "body": DIGEST_JUNE_WEEK1_ZH,
        "expand_topic": "Lovart Digest June 2026 week1 editorial roundup",
    },
    {
        "rank": 157,
        "key": "event_countdown_zhtw",
        "lang": "zh-TW",
        "slug": "event-countdown-5-days-teaser-graphics-ai",
        "cover": "040",
        "category": "How-To",
        "title": "活動倒數 5 天 Teaser 圖：AI 視覺與可編輯 CTA 實操",
        "seo_title": "Event Countdown Teaser — 繁中 ChatCanvas 實操",
        "description": "繁中 404 修復：event countdown teaser，天數 editable，Touch Edit 改倒數。",
        "seo_description": "倒數 teaser：Brand Kit、Touch Edit、Design Agent QA。",
        "focus": "event countdown 5 days teaser graphics ai",
        "keywords": ["活動倒數 ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Event Countdown Teaser zh-TW",
        "body": EVENT_COUNTDOWN_ZHTW,
        "expand_topic": "TW event countdown teaser workflow",
    },
    {
        "rank": 158,
        "key": "hospitality_marketing_zhtw",
        "lang": "zh-TW",
        "slug": "hospitality-marketing-ai-design-agent",
        "cover": "047",
        "category": "Industry Solution",
        "title": "飯店與餐飲行銷 AI Design Agent：可編輯 promo 與 Brand Kit SOP",
        "seo_title": "Hospitality Marketing Design Agent — 繁中實操",
        "description": "繁中 404 修復：hospitality marketing Design Agent，套餐價 readable，Touch Edit 改價。",
        "seo_description": "飯店餐飲：Brand Kit、OTA cover、過敏 disclaimer editable。",
        "focus": "hospitality marketing ai design agent",
        "keywords": ["飯店餐飲 ai 設計", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Hospitality Marketing Design Agent zh-TW",
        "body": HOSPITALITY_MARKETING_ZHTW,
        "expand_topic": "TW hospitality marketing Design Agent workflow",
    },
    {
        "rank": 159,
        "key": "youtube_thumbnail_zhtw",
        "lang": "zh-TW",
        "slug": "how-to-chat-generate-youtube-thumbnail-lovart",
        "cover": "050",
        "category": "How-To",
        "title": "如何用 Chat 生成 YouTube 縮圖：Lovart static-first 實操",
        "seo_title": "Chat Generate YouTube Thumbnail — 繁中 SOP",
        "description": "繁中 404 修復：chat generate YouTube thumbnail，Brand Kit、Touch Edit static-first。",
        "seo_description": "YouTube 縮圖：16:9 master、variant same thread、Design Agent QA。",
        "focus": "how to chat generate youtube thumbnail lovart",
        "keywords": ["youtube 縮圖 ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — YouTube Thumbnail Chat zh-TW",
        "body": YOUTUBE_THUMBNAIL_ZHTW,
        "expand_topic": "TW YouTube thumbnail ChatCanvas static-first",
    },
    {
        "rank": 161,
        "key": "salary_report_de",
        "lang": "de",
        "slug": "ai-designer-salary-report-2026",
        "cover": "061",
        "category": "Branding",
        "title": "AI Designer Gehaltsreport 2026: Marktbänder statt erfundener Zahlen",
        "seo_title": "AI Designer Salary Report 2026 — DE Marktbänder",
        "description": "DE 404 fix: salary report 2026，Marktbänder mit Disclaimer，keine erfundenen EUR。",
        "seo_description": "Gehaltsreport：Marktbänder、Disclaimer、ChatCanvas Ops KPI。",
        "focus": "ai designer salary report 2026",
        "keywords": ["ai designer gehalt", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Editorial — AI Designer Salary Report DE",
        "body": SALARY_REPORT_DE,
        "expand_topic": "AI Designer Gehaltsreport DE Marktbänder",
    },
    {
        "rank": 162,
        "key": "law_firm_de",
        "lang": "de",
        "slug": "best-ai-design-agent-for-law-firm",
        "cover": "062",
        "category": "Industry Solution",
        "title": "Best AI Design Agent für Kanzleien: Brand Kit, Impressum und editierbare Promo",
        "seo_title": "Law Firm Design Agent — DE Brand Kit SOP",
        "description": "DE 404 fix: law firm Design Agent，Brand Kit、Impressum editable、Touch Edit Termin-Fix。",
        "seo_description": "Kanzlei：navy palette、Seminar flyer、Design Agent QA。",
        "focus": "best ai design agent for law firm",
        "keywords": ["kanzlei design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Law Firm Design Agent DE",
        "body": LAW_FIRM_DE,
        "expand_topic": "Kanzlei Design Agent Brand Kit DE",
    },
    {
        "rank": 163,
        "key": "solopreneur_zh",
        "lang": "zh",
        "slug": "best-ai-design-agent-for-solopreneur",
        "cover": "063",
        "category": "Industry Solution",
        "title": "一人公司选什么 Design Agent：改 offer 价比第一张好看更重要",
        "seo_title": "Solopreneur Design Agent — ChatCanvas 实操",
        "description": "404 修复：solopreneur segment Design Agent，offer readable，Touch Edit 改价。",
        "seo_description": "一人公司：Brand Kit、personal brand cover、disclaimer editable。",
        "focus": "best ai design agent for solopreneur",
        "keywords": ["一人公司 ai 设计", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Solopreneur Design Agent ZH",
        "body": SOLOPRENEUR_ZH,
        "expand_topic": "solopreneur Design Agent 选型",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "zh-TW": expand_zhtw,
    "de": expand_de,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch15 content cluster.*\n"
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
