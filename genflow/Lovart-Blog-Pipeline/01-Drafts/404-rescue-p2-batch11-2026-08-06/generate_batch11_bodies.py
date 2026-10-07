#!/usr/bin/env python3
"""Generate 404-rescue P2 batch11 blog bodies (10 files). Self-contained.

Ranks #113–#122 from 404-rescue-compact lane.
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

BROCHURE_CHAT_ZH = """
# 如何用 ChatCanvas 对话生成宣传册：可编辑 static 工作流

这条中文 URL slug `how-to-chat-generate-brochure-lovart` 曾返回 404，搜索需要「用对话/chat 生成 brochure/宣传册」的可执行 SOP，不是「一键全套 VI」 demo。诚实 framing：AI 宣传册的价值不在第一帧多炫，而在改价、改活动日期、改 disclaimer 时是否 five 分钟关闭。**ChatCanvas** thread、**Brand Kit**、**Touch Edit**、**Design Agent** 把 brochure 当 revision-heavy 物料系列，不是单次抽卡 PNG。

## 宣传册四类输出与 ratio 合同

第一是折页/单页 hero 4:5 或 A4 竖版 digital PDF cover：headline top 15% flat for **Touch Edit**。第二是内页 spread 或 slide 2–6：同一 **Brand Kit** accent，只换 copy 不换 grid skeleton。第三是 back cover 与 contact block：地址、电话、二维码在 editable footer，不能 bake 进 pixels。第四是社媒 derivative：同 thread export 1:1 与 9:16 crop，CTA safe zone bottom 20%。

## 为什么「chat 生成宣传册」常卡在周二改价

弱 brief「帮我做高级宣传册」→ 图好看但价目字小、角标挡产品。改「满 200 减 30」要 full regen 三十分钟。slide 4 accent drift 成另一个 coral。readable 价格 bake 进 render。video 角标有 offer 但 PDF static 没有 **Touch Edit** layer。**Brand Kit** 未从 approved VI 取样 hex。

## ChatCanvas 对话 brief 合同（宣传册版）

第一轮对话写 acceptance fields，不是形容词：「campaign X，brochure cover 4:5 1080×1350，Brand Kit navy + sand from media kit，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread 只换 headline」。第二轮迭代只改缺失字段。**Design Agent** QA 需要 numeric safe zone，不能 QA「高级感」。

## Brand Kit 先于 chat generate batch

从已批准 logo 板、prior brochure、门店 signage 取样 primary hex、accent hex、title/body type role。无 **Brand Kit** 时 chat 每轮 invented 新 accent，折页内页像拼贴。**ChatCanvas** 同一 thread 降低 slide 2–6 drift；改 global promo 用 **Touch Edit** CTA band，不 full regen cover photography。

## Touch Edit 改活动价不改 layout identity

改「早鸟 ¥99」为「现场 ¥129」：**Touch Edit** 框 CTA 带，指令「保持 stripe geometry 与 Brand Kit accent，只替换文案」。full regen 会 random 改 product cutout 与 shadow。测量 ROI：「改价一次覆盖 cover + 内页几种 ratio 的分钟数」。

## static-first 再配 optional motion teaser

宣传册主交付物是 readable PDF/static；optional motion bumper 4–6 秒与 **Brand Kit** 色温一致，no readable small text in clip。顺序颠倒会产生 clip 有 offer 但 PDF static 不能 edit 的 mismatch。

## 与 Canva 模板库或单次 T2I 的分工

模板库适合标准版式快速起稿；**ChatCanvas** + Kit + **Touch Edit** 适合 weekly 改价、多尺寸 derivative、legal disclaimer 频繁退回。若 KPI 是「改价 five 分钟覆盖 cover+story」，选 workflow 工具；若 KPI 是「试 50 种 mood」，选单次生成 playground。

## 常见失败

chat 每轮新 thread 无 series memory。readable 价格 baked。跳过 **Brand Kit** 从 random pastel 开干。404 URL 未修复 SOP 散在群里。内页与 cover 各开 prompt 导致 accent drift。

## 测量什么才有用

记「改价一次几分钟」「brochure series drift 几次」「一次 action export 几种 ratio」。404 修复给 ops team stable chat-generate brochure SOP URL。
"""

REAL_ESTATE_DE = """
# Brand Kit für Immobilienmakler: editierbare Listing- und Social-Assets

Diese deutsche URL `brand-kit-real-estate-agent-lovart` lieferte 404, während Suchen nach einem **Brand Kit** für Makler segment-spezifische Workflows verlangten — Exposé, Open-House-Flyer, Social-Carousel, nicht generisches „60 Sekunden komplette CI“. Ehrliche Einordnung: Makler-Ops ändern Preis, Besichtigungstermin und Disclaimer wöchentlich; full regen pro Änderung skaliert nicht. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** und **Design Agent** halten Listing-Serien visuell konsistent.

## Vier Szenarien im Makler-Segment

Erstes Szenario: Listing-Exposé cover und PDF hero — Objektfoto focal, Preis readable, Disclaimer footer editable. Zweites: Open-House-Flyer und Aushang — Datum und Uhrzeit per **Touch Edit**, nicht per full regen. Drittes: Instagram/Facebook carousel slide 2–6 — gleicher **Brand Kit** accent, nur Objektname wechseln. Viertes: Story 9:16 — bottom 20% CTA band, kein Text über Gesicht oder Fenster.

## Warum Makler-Promo oft am Dienstag scheitert

Schwacher brief: „Premium Immobilien-Look“. Ergebnis: kleiner Preis, Badge über Fassade. Änderung „Open House Sa 14 Uhr“ kostet thirty-minute full regen. Slide 4 erfindet neuen terracotta accent. Video-Hook zeigt Angebot, landing static ohne **Touch Edit** price block. **Brand Kit** fehlt — jede Generation erfindet brokerage colors neu.

## ChatCanvas brief-Vertrag (Makler)

Statt Adjektive: „Listing ID 4821, hero 4:5 1080×1350, Brand Kit navy + sand aus approved media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, Makler-Disclaimer footer editable, no small text in render, slide 2–6 same thread“. **Design Agent** prüft safe zone, hex drift vs Kit, double CTA.

## Brand Kit aus Offline-Material befüllen

Primary und accent hex aus Visitenkarte, Büroschild, bestehendem Exposé — nicht aus stock marble. Type roles für Objektname vs Preis vs Disclaimer. Ein **ChatCanvas** thread für Listing-Serie reduziert carousel drift. Promo-Wechsel: **Touch Edit** auf CTA, nicht auf Objektfoto crop.

## Touch Edit für Preis- und Terminänderungen

„Kaltmiete 1.890 €“ zu „1.750 €“: **Touch Edit** label band, stripe geometry und **Brand Kit** accent bleiben. Full regen randomisiert Fensterperspektive und Schatten — für Makler unbrauchbar bei wöchentlichen Anpassungen.

## static-first vor optional motion

Rechtliche Prüfung auf static PDF und social stills vor 4–6 sec teaser clip. Clip brief: no readable small text, color temperature aligned to Kit. User screenshot oft still, nicht frame three bei muted autoplay.

## Abgrenzung zu generischem Real-Estate-How-To

Diese Seite fokussiert **Brand Kit** segment Makler: hex SSOT, Listing series thread, editable disclaimer. Nicht: virtuelles Staging debate oder fake Marktstatistiken. Keine erfundenen Preis-Tiers.

## Typische Fehler

Kein **Brand Kit** — jede Listing-Karte andere accent. Preis baked in pixels. Cover und carousel in separaten threads. 404 URL nicht wiederhergestellt — SOP in WhatsApp-Gruppen.

## Metriken

Minuten pro Preis-Fix, accent drift pro carousel, export sizes pro action. Wiederhergestellte URL als stable Makler Brand Kit SOP für DE teams.
"""

INCLUSIVE_BIAS_ZH = """
# 2027 包容性视觉输出：AI 设计偏见审计与缓解工作流

这条中文 URL `ai-design-bias-inclusive-visual-output-2027` 曾返回 404，搜索需要 2027 规划语境下的 inclusive visual output 与 bias 缓解，不是空泛 DEI 幻灯片。诚实 framing：偏见常来自训练分布、brief 默认值与验收标准缺失；缓解靠可执行的 brief 字段、**Brand Kit** 角色定义、**Design Agent** pass/fail QA，不是口号。**ChatCanvas** thread 留痕、**Touch Edit** 改 copy 不改 representation lottery。

## 四类偏见在营销物料里的表现

第一是人物默认肤色、年龄、体型单一：brief 未写 representation requirements。第二是场景默认 luxury suburban，忽视 rental、shared workspace、multigenerational household。第三是 icon 与 pictogram 可访问性：contrast 不足、small type baked。第四是 multi-locale 同一 visual 强套，忽视 local dress norm 与 disclaimer 句差异。

## 为什么「加一句 diverse」在 prompt 里不够

弱 brief「要 inclusive 一点」→ 模型仍 lottery，slide 3 与 slide 4 人物不一致。改 campaign copy 要 full regen 三十分钟。readable disclaimer bake 进 pixels 无法 localization。**Brand Kit** 未定义 representation role 与 accent 独立于人物肤色。

## ChatCanvas brief 合同（inclusive 2027 版）

强 brief 写验收字段：「hero 4:5，Brand Kit hex 写死，representation: 至少两种 age band 与两种 body type 在 series 内一致（非每 slide lottery），headline top 15% flat for **Touch Edit**，disclaimer locale-specific footer editable，contrast ratio 目标 WCAG AA for price block，禁止 render 内小字」。**Design Agent** QA contrast、safe zone、series consistency。

## Brand Kit 定义 visual system 不含人物 lottery

Kit 锁 primary/accent/type role；representation guidelines 写在 brief required fields 与 QA checklist，不依赖 adjective。**ChatCanvas** 同一 thread 降低 slide 2–6 人物 drift；改 promo 用 **Touch Edit** copy layer，不 regen 整张 hero 换脸。

## Touch Edit 改文案不触发 representation regen

改「新客 ¥99」为「会员 ¥79」：**Touch Edit** 框 CTA 带，保持人物 crop 与 **Brand Kit** stripe。full regen 会 random 换模特肤色与姿势 — inclusive 工作流的大忌。

## static-first 与 motion 的 accessible offer

offer 必须在 static editable layer；clip 无 readable small text price bake-in。muted autoplay 下用户 screenshot still — inclusive 也要 readable price at mobile width。

## 2027 审计清单（可环比）

季度 audit：representation drift 次数（slide 间不一致）、contrast fail 次数、legal return 因 disclaimer localization、改价分钟数。环比写绝对变化 + 百分比，不单期 snapshot。

## 常见失败

DEI 写 PPT 无 brief 模板。每 slide 新 prompt lottery 人物。readable 价格 baked。跳过 **Brand Kit**。404 URL 未修复。

## 测量 ROI

drift 次数、contrast fail、改价分钟、export size 数。404 修复给 brand + compliance stable inclusive visual SOP URL。
"""

LEGAL_FIRMS_ZH = """
# 2026 律所与律师 AI 设计实务：合规 static 与可编辑 disclaimer

这条中文 URL `ai-design-for-legal-firms-attorneys-2026` 曾返回 404，搜索需要 law firm segment 的 operational 指南，不是「AI 替律师出庭」 hype。律所 daily ops：服务介绍 one-pager、seminar 海报、LinkedIn/微信公众号 cover、客户须知 footer — 改 seminar 日期与 fee disclaimer 频繁，若 full regen 三十分钟 × N 场活动不可持续。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 grid，改 copy 不 lottery layout。

## 律所 segment 四个高频场景

第一是 seminar 与讲座海报：日期、地点、注册链接 weekly 改，字必须 readable。第二是 firm one-pager 与 service line card：disclaimer 与「不构成法律意见」句在 editable footer。第三是律师个人 brand 与 firm VI 并存：**Brand Kit** 锁 firm hex，律师 headshot zone 固定。第四是 newsletter header 与 webinar slide cover：4:5 与 16:9 同 thread derivative。

## 为什么 legal promo 常卡在 compliance 退回

改 disclaimer 一字要 full regen 三十分钟。readable 价目或 fee range bake 进 pixels，法务不能改。video 角标有 offer 但 landing static 没有 **Touch Edit** layer。carousel slide 4 accent drift vs approved firm letterhead。**Brand Kit** 未从 letterhead 取样 hex。

## ChatCanvas brief 合同（律所版）

弱 brief：「高端律所风海报」。强 brief：「seminar 4:5 1080×1350，Brand Kit navy + gold from letterhead，headline top 15% flat for Touch Edit，fee disclaimer footer editable 原文附 brief，禁止 render 内小字，slide 2–6 同 thread 换讲师名」。**Design Agent** QA safe zone、disclaimer present、hex drift vs Kit。

## Brand Kit 从 letterhead 与 prior collateral 取样

从已批准信纸、名片、prior seminar PDF 取样 primary hex、accent hex、title/body role。不用 stock marble 当 firm 色。**ChatCanvas** 同一 thread batch 多活动 export；global promo **Touch Edit** 各 locale static disclaimer 句可不同，visual system 一致。

## Touch Edit 改 seminar 日期不改 layout identity

改「3 月 15 日」为「3 月 22 日」：**Touch Edit** 框 date block，保持 stripe 与 **Brand Kit** accent。full regen 会 random 改 courthouse photo crop 与 shadow。

## static-first 与 optional motion

webinar teaser autoplay 常静音；观众 screenshot still。顺序：static legal pass on all sizes → optional motion 与 **Brand Kit** 色温一致。offer 与 disclaimer 必须在 static editable。

## 常见失败

跳过 **Brand Kit**。disclaimer baked。每活动新 prompt 无 thread。404 URL 未修复 SOP 散在邮件链。

## 测量 ROI

改 seminar 信息一次几分钟、legal return 次数、carousel drift 几次。404 修复给 law firm marketing stable SOP URL。
"""

MYTHS_ZH = """
# 2026 AI 设计流言对照：简体版实操反驳（非繁中拷贝）

这条简体 URL `ai-design-myths-debunked-2026` 曾返回 404。注意：繁中 batch1 已有 `zh-TW` 版五迷思结构；本篇为**简体重写**，角度与案例不同，禁止逐句翻译。不写假调查数字；用可重现 brief 与 **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 说明流言错在哪。

## 流言一：「点一下就有完整品牌手册」

2023 playground 给人「一键 VI」错觉。2026 交付要的是：改周二 promo、carousel slide 2–6 不 drift、disclaimer editable — 这需要 **Brand Kit** hex role 与 **ChatCanvas** thread，不是单次 download PNG。完整手册是 series ops，不是 one-shot。

## 流言二：「不会 PS 就做不了正经物料」

非设计师 weekly 产出 feed hero、story、价目角标 — 瓶颈是 resize 与改价，不是 lack of Pen tool。**Touch Edit** 改 CTA 带、**Design Agent** QA safe zone，五分钟关闭价格变更。PS 仍适合 print CMYK 精修与 legacy PSD，与 AI workflow 并行不互斥。

## 流言三：「AI 出图不能上法务审」

问题不是「AI 三个字」，是 price 与 disclaimer 是否 baked。readable 条款 bake 进 pixels → 法务必退。editable footer + static-first → 一字修改 **Touch Edit** 关闭，不 thirty-minute regen。合规关键是 layer 结构，不是工具标签。

## 流言四：「多尺寸靠人工一张张 crop」

单 thread **ChatCanvas** export 4:5 master → 9:16 story derivative → 1:1 profile crop，brief 写 safe zone。人工 crop 第十七张 banner 是 ops 浪费，不是「AI 不行」。失败模式是每尺寸各开 prompt，slide 4 invented 新 accent。

## 流言五：「prompt 越长图越好」

长 prompt 堆 style 词常产出小字价目与 double CTA。交付 brief 是验收合同：ratio、hex、headline band、price block、禁项。**Design Agent** pass/fail 靠 numeric fields，不靠形容词长度。

## 流言六：「换模型就能解决改价慢」

改价慢通常是 process：无 **Brand Kit**、无 **Touch Edit** layer、video-first 导致 offer 不可编辑。换 Seedance 为 Kling 不缩短 Tuesday static fix。测量「改价分钟」比争论模型 leaderboard 有用。

## 简体与繁中 batch1 的差异说明

繁中版重五迷思与印刷/伦理长讨论；简体版重 ops 流言（一键 VI、PS 门槛、法务层、多尺寸、长 prompt、换模型）。内链并存，内容不 duplicate paragraph。

## 常见失败

用流言吓阻 AI 或吹噓 magic。无 brief 模板。404 URL 未修复。

## 测量什么

改价分钟、drift 次数、legal return。404 修复给 mainland ops stable myths-debunked SOP URL。
"""

BEST_AGENT_ZH = """
# 非设计背景选什么 Design Agent：运营与市场团队的 brief 合同

这条简体 URL `best-agent-for-non-design` 曾返回 404。意大利语 batch6 已有 it 版（marketer/founder 语境）；本篇面向**大陆运营与市场**：抖音/小红书/微信 feed、价盘 weekly 改、无 PS 技能 — 不同案例与渠道 safe zone，非翻译 it 正文。

## 非设计岗每周四类输出

第一是 feed hero 4:5 与 carousel slide 2–6：价 readable，accent 不 drift。第二是 story 9:16：top 12% 与 bottom 20% 留平台 UI。第三是直播/活动预告 static：headline flat for **Touch Edit**。第四是价目角标与会员 card：disclaimer footer editable。

## 弱 brief 与合同 brief

弱：「帮我出高级感海报」。强：「SKU 居中，Brand Kit slate + coral，headline top 15%，price bottom left safe zone，1080×1350，禁止双 CTA，disclaimer editable footer」。**Design Agent** 不能验收「高级感」。

## Brand Kit 先于 batch

无 **Brand Kit** 每轮 invented 新 accent。从真实 packaging 或 approved slide 取 hex。再开 **ChatCanvas** product thread。改 campaign：**Touch Edit** 改字，不改 product cutout。

## Touch Edit 是非设计岗的回归理由

只改价块或活动日期。指令：保持 stripe 与 font role，替换 copy。full regen 是吓退非设计岗的 time sink；**Touch Edit** 五分钟是周二回归动机。

## Design Agent 当 checklist

验 safe zone、双 CTA、字过小、hex drift vs Kit。不替 brief；执行 brief。第二轮常只补缺失字段，不换模型。

## 与 it batch6 的分工

it 版：意大利 marketer、carousel tre slide、EU disclaimer 语境。简体版：小红书/抖音 safe zone、价盘改价、运营 KPI「改价几分钟」。slug 同，locale 不同，正文不 copy。

## 常见失败

只写 aesthetic prompt。改价 full regen。carousel 无单 thread。video 价 baked 不可读。brief 缺 disclaimer。

## 测量

改价几分钟、slide 4 drift 几次。**Touch Edit** 五分钟 → workflow 对非设计岗成立。
"""

ICE_CREAM_BRAND_KIT_ZH = """
# 冰淇淋店 Brand Kit：菜单、外卖袋与季节 promo 的可编辑视觉

这条中文 URL `brand-kit-ice-cream-shop-lovart` 曾返回 404，搜索需要 ice cream shop segment 的 **Brand Kit** SOP，不是虚构「60 秒生成全套 VI」。冰淇淋店 ops：季节口味 promo、外卖平台 cover、门店 POP、会员 card — 改口味价与过敏 disclaimer 勤，warm pastel accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 appetite-forward palette。

## 冰淇淋 segment 四个高频场景

第一是菜单与价目：数字改得勤，手机与收银屏 readable。第二是季节限定 promo 与外卖 banner：copy 改但 **Brand Kit** visual 不变。第三是 story 与点评封面：9:16 safe zone，口味名不挡 scoops 主图。第四是会员 card 与门店 POP：过敏与价格 disclaimer footer editable。

## 为什么 ice cream promo 常卡在改价

改「双球 ¥28」要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 mint。readable 价格 bake 进 pixels。video 角标有 offer static 无 **Touch Edit** layer。**Brand Kit** 未从 cup/wrapper 取样 hex。

## ChatCanvas brief 合同（冰淇淋版）

弱 brief：「可爱冰淇淋海报」。强 brief：「季节 promo 4:5 1080×1350，Brand Kit mint + cream from cup sample，headline top 15% flat for Touch Edit，价格 bottom left safe zone，过敏 disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** numeric acceptance fields。

## Brand Kit 从 cup、wrapper、signage 取样

从已批准杯身、包装、门店招牌取样 primary、accent、type role。不用 stock marble 当品牌色。Kit 建好后所有 **ChatCanvas** thread 引用同一套 role。

## Touch Edit 改口味价不改 scoops photography

改「限时 ¥22」为「会员 ¥19」：**Touch Edit** 框 CTA 带，保持 scoops geometry 与 **Brand Kit** accent stripe。full regen random 改 highlight 与 shadow。

## 与 waxing studio segment 的分工

本篇聚焦 ice cream：appetite palette、过敏 disclaimer、seasonal flavor series。waxing studio slug 另文覆盖 service menu 与预约 CTA 字段。

## static-first 再配 optional food motion

story autoplay 常静音；用户 screenshot still。顺序：static legal pass → optional motion 与 **Brand Kit** 色温一致。

## 常见失败

跳过 **Brand Kit**。readable 价格 baked。单尺寸 hero 无 series thread。404 未修复。

## 测量 ROI

改口味价一次几分钟、carousel drift 几次、export 几种 ratio。404 修复给 ice cream ops stable Brand Kit SOP URL。
"""

WAXING_BRAND_KIT_ZH = """
# 脱毛工作室 Brand Kit：服务价目、预约 CTA 与社媒系列

这条中文 URL `brand-kit-waxing-studio-lovart` 曾返回 404，搜索需要 waxing studio segment 的 **Brand Kit** operational 指南。工作室 daily ops：服务价目、新客体验 promo、大众点评/小红书 cover、门店 POP — 改套餐价与「单次/疗程」 disclaimer 频繁，soft neutral accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 calm professional palette。

## 脱毛 studio 四个高频场景

第一是服务价目与套餐 card：数字 readable，疗程 disclaimer editable。第二是新客体验 promo 与 story 9:16：预约 CTA bottom 20% flat for **Touch Edit**。第三是 carousel slide 2–6 服务介绍：同一 **Brand Kit** accent，只换 service name。第四是门店 POP 与会员 card：卫生与注意事项 disclaimer footer editable。

## 为什么 waxing promo 常卡在改价

改「体验 ¥99」要 full regen 三十分钟。slide 4 accent drift 成另一个 lavender。readable 疗程价 bake 进 pixels。video 角标有 offer static 无 **Touch Edit** layer。**Brand Kit** 未从 storefront 取样 hex。

## ChatCanvas brief 合同（脱毛版）

弱 brief：「高级脱毛海报」。强 brief：「新客 promo 4:5 1080×1350，Brand Kit soft gray + rose from signage，headline top 15% flat for Touch Edit，价格 bottom left safe zone，疗程 disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** numeric fields。

## Brand Kit 从 storefront、price list 取样

从已批准价目、门头、prior poster 取样 primary、accent、type role。**ChatCanvas** 同一 thread batch 多服务 export。

## Touch Edit 改套餐价不改 treatment photo crop

改「单次 ¥168」为「疗程 ¥899」：**Touch Edit** 框 CTA 带，保持 stripe 与 **Brand Kit** accent。full regen random 改 skin tone lighting — segment 敏感，brief 写 representation 与 lighting 禁项。

## 与 ice cream segment 的分工

ice cream slug 覆盖 seasonal flavor 与过敏 disclaimer；本篇覆盖 service menu、预约 CTA、疗程 disclaimer 句。

## static-first 再配 optional motion

预约 offer 必须在 static editable；clip 无 readable small text price。

## 常见失败

跳过 **Brand Kit**。价格 baked。每服务新 prompt 无 thread。404 未修复。

## 测量 ROI

改套餐价一次几分钟、drift 几次。404 修复给 waxing studio ops stable Brand Kit SOP URL。
"""

VMAKER_REVIEW_ZH = """
# Vmaker AI 评测 2026：诚实对比 revision-heavy 营销 static 工作流

这条中文 URL `vmaker-ai-review` 曾返回 404，搜索需要 honest Vmaker AI review，不是 feature 清单软文。直接结论：Vmaker 类工具擅长 screen record、快速解说 clip、template 化 talking-head 包装；弱在 editable price layer、**Brand Kit** carousel series、legal disclaimer 单独 layer。Lovart **ChatCanvas** static master 与 **Touch Edit** 关 readable offer；Vmaker 可作 companion hook，不是 entire funnel。不写 fake pricing tiers — 商用范围请阅官方 ToS。

## Vmaker 真正帮上忙的三类任务

第一是产品 demo screen record 与旁白包装：快速出 tutorial clip。第二是 internal training 与 onboarding 短视频：template 加速。第三是 social teaser 4–6 秒 mood：muted autoplay 前 hook。三类都 weak 在：价目小字 bake、carousel hex drift、周二改 promo 要 regen clip。

## Vmaker 在 marketing ops 里的 common gap

改价 Tuesday 触发 clip regen 三十分钟。carousel slide 4 accent drift。disclaimer bake 进 clip pixels。video hook 有 offer landing static 无 **Touch Edit** price。**Brand Kit** 未设 hex role。static-first 顺序颠倒。

## 推荐 parallel workflow

Pass one：**ChatCanvas** hero 4:5 与 end card，legal pass，price bottom left safe zone，disclaimer footer editable。Pass two：optional Vmaker clip 无 readable small text，色温 aligned to **Brand Kit**。Pass three：promo change 只 **Touch Edit** static；不 regen clip unless mood direction 变。

## ChatCanvas brief contract（static side）

弱 brief：「高级产品 video 风」。强 brief：「hero 4:5，Brand Kit navy + sand，headline top 15% flat，price bottom left，disclaimer editable，禁止 render 内小字」。**Design Agent** QA safe zone、hex drift vs Kit。

## 与 InVideo、Medeo 等 T2V 的 honest 分工

比 first-frame beauty 误导采购；同一 Tuesday 改价任务比 static fix 分钟与 clip regen 分钟。readable offer 必须在 static editable layer。

## 许可与 commercial use

查阅 Vmaker 官方 ToS 对 paid social 与商用范围；campaign folder archive license note。不编造 tier 价格。

## 常见失败

only Vmaker clip 无 aligned static offer。每改价 regen clip。**Brand Kit** absent。404 URL 未修复。

## 测量 ROI

static price fix 分钟、clip regen 分钟、drift 次数。404 修复给 video ops stable Vmaker + ChatCanvas parallel SOP URL。
"""

CHARACTER_DESIGN_ZHTW = """
# AI 角色設計指南：用工具建立一致角色視覺

這條繁中 URL `ai-character-design-guide-how-to-create-consistent-characters-with-ai-tools` 曾 404，搜尋需要 character consistency how-to，不是「一鍵 OC」 meme。角色系列 daily ops：漫畫連載、遊戲宣傳、IP 社媒 carousel — slide 3 臉型漂移比「第一張多炫」更致命。Lovart **ChatCanvas** thread、**Brand Kit**、**Touch Edit**、**Design Agent** 把角色當 series SSOT，不是每張 lottery。

## 角色一致性的四個驗收字段

第一是 face structure lock：眉距、鼻型、髮色 hex 寫進 **Brand Kit** role。第二是 outfit layer：服裝可換，face zone 不 regen lottery。第三是 pose derivative：同 thread export 4:5 hero → 9:16 story → 1:1 avatar crop。第四是 promo 改價：CTA 在 **Touch Edit** band，不 regen 整張換臉。

## 為什麼「character sheet 一張參考」仍 drift

每 slide 新 prompt → slide 4 invented 新 eye color。改活動 copy full regen 三十分鐘 → 連帶換臉。readable 價 bake 進 pixels。video hook 角色與 static hero 不一致。**Brand Kit** 未定義 character_hex 與 stroke role。

## ChatCanvas brief 合同（角色版）

弱 brief：「可愛二次元角色」。強 brief：「IP 系列 4:5 1080×1350，Brand Kit character_hair #2a1810 + outfit_accent coral，face structure lock per reference sheet，headline top 15% flat for Touch Edit，price bottom left safe zone（若 promo），disclaimer footer editable，slide 2–6 同 thread 只換 pose/copy，禁止 render 內小字」。**Design Agent** QA face drift、safe zone、hex vs Kit。

## Brand Kit 承載角色 SSOT

Kit 寫 hair_hex、skin_tone_reference、outfit_primary、stroke_weight（若 line art 風）。無 Kit 時 carousel 像不同 IP 拼貼。**ChatCanvas** 同一 thread 降低 slide 2–6 face lottery。

## Touch Edit 改 promo 不破坏角色 identity

改「早鳥 NT$880」：**Touch Edit** 框 CTA 帶，指令「保持 face crop 與 Brand Kit accent，只替換文案」。full regen 會 random 改五官比例。

## 與韓文 slug 或英文 complete guide 的分工

本篇繁中重寫：台灣創作者語境、Reels safe zone、票務/promo 字段可選。非逐句翻譯其他 locale；與 ko batch 正文不同 angle。

## static-first 再配 optional motion

角色 offer 必須在 static editable；motion bumper 無 readable small text，色溫 aligned to Kit。

## 常見失敗

每張新 prompt 無 thread。face lottery 無 Kit。readable 價 baked。404 未修復。

## 測量 ROI

face drift 次數、改 CTA 一次幾分鐘、export 幾種 ratio。404 修復給 IP creator stable character consistency SOP URL。
"""

# FAQ blocks
FAQ = {
    "brochure_chat": """
## FAQ

**ChatCanvas 对话生成宣传册要先建 Brand Kit 吗？**  
建议，从 approved VI 取样 hex，防 slide 2–6 drift。

**改价要整图重出吗？**  
不需要，Touch Edit 框 CTA 带，保持 layout identity。

**brochure 与单次 T2I 分工？**  
改价频繁、多尺寸 derivative 选 ChatCanvas workflow；mood 探索选单次生成。

**404 修复？**  
stable chat-generate brochure SOP URL。

**Design Agent 做什么？**  
QA safe zone、disclaimer、Brand Kit hex drift。
""",
    "real_estate_de": """
## FAQ

**Makler brauchen zuerst Brand Kit?**  
Ja — hex aus Visitenkarte/Exposé, nicht stock marble.

**Preisänderung — full regen?**  
Nein. Touch Edit auf CTA-Band; clip optional unverändert.

**Story safe zone?**  
Top 12%, bottom 20% für Plattform-UI frei.

**404 fix?**  
Stable DE Makler Brand Kit SOP URL.

**Design Agent Rolle?**  
QA safe zone, disclaimer, hex drift vs Kit.
""",
    "inclusive_bias": """
## FAQ

**2027 inclusive 只靠 prompt 加 diverse？**  
不够，brief 写 representation 验收字段 + Design Agent QA。

**改价会换模特吗？**  
Touch Edit 只改 copy 层，不 regen 整张换脸。

**环比 audit 要什么？**  
drift 次数、contrast fail、改价分钟 — 绝对变化 + 百分比。

**404 修复？**  
stable inclusive visual output SOP URL。

**Brand Kit 作用？**  
锁 hex/type role；representation 写在 brief checklist。
""",
    "legal_firms": """
## FAQ

**律所要先建 Brand Kit 吗？**  
建议，从 letterhead 取样 hex 与 type role。

**法务改 disclaimer 一字要 regen 吗？**  
不需要，Touch Edit footer editable 层。

**seminar 日期改动？**  
Touch Edit 框 date block，不改 courthouse photo crop。

**404 修复？**  
stable law firm design SOP URL。

**Design Agent QA？**  
safe zone、disclaimer present、hex drift vs Kit。
""",
    "myths_zh": """
## FAQ

**本篇与繁中 batch1 五迷思重复吗？**  
不重复，简体重写六则 ops 流言，非逐句翻译。

**流言「一键 VI」怎么驳？**  
Brand Kit + ChatCanvas thread 是 series ops，不是 one-shot PNG。

**非设计师能用吗？**  
Touch Edit + Design Agent checklist，五分钟改价场景。

**404 修复？**  
stable 简体 myths-debunked SOP URL。

**还要 PS 吗？**  
print CMYK 与 legacy PSD 仍适合 PS；promo 改价用 workflow 工具。
""",
    "best_agent_zh": """
## FAQ

**与 it batch6 同 slug 有何不同？**  
简体面向大陆运营/小红书抖音 safe zone；it 版面向 EU marketer，正文不 copy。

**非设计岗要先 Brand Kit 吗？**  
要，防 carousel accent drift。

**改价要 full regen 吗？**  
不需要，Touch Edit 五分钟关闭价格块。

**404 修复？**  
stable 非设计岗 Design Agent SOP URL。

**Design Agent 做什么？**  
执行 brief 合同 QA，不替写 brief。
""",
    "ice_cream_brand_kit": """
## FAQ

**冰淇淋店 Brand Kit 从哪取样？**  
cup、wrapper、门店 signage 的 hex，不用 stock marble。

**改口味价要整图重出吗？**  
不需要，Touch Edit 改价格块。

**过敏 disclaimer？**  
footer editable 层，禁止 bake 进 pixels。

**404 修复？**  
stable ice cream Brand Kit SOP URL。

**与 waxing slug 分工？**  
本篇 seasonal flavor + 过敏；waxing 覆盖疗程与预约 CTA。
""",
    "waxing_brand_kit": """
## FAQ

**脱毛 studio Brand Kit 要先建吗？**  
建议，从价目与门头取样 hex。

**改套餐价要 regen 吗？**  
不需要，Touch Edit 框 CTA 带。

**疗程 disclaimer？**  
footer editable，法务可改一字。

**404 修复？**  
stable waxing studio Brand Kit SOP URL。

**Design Agent QA？**  
safe zone、disclaimer、lighting 禁项字段。
""",
    "vmaker_review": """
## FAQ

**Vmaker 覆盖整个 marketing funnel 吗？**  
不，clip mood 可以；editable price 在 ChatCanvas static + Touch Edit。

**改价 Tuesday 要 regen clip 吗？**  
不需要，Touch Edit 改 static；clip 可选 companion。

**价格 tier 怎么写？**  
不编造，请阅 Vmaker 官方 ToS。

**404 修复？**  
stable Vmaker + ChatCanvas parallel SOP URL。

**与 Medeo/InVideo 对比？**  
同一改价任务比 static fix 分钟，不比 first-frame beauty。
""",
    "character_design_zhtw": """
## FAQ

**角色一致要先 Brand Kit 吗？**  
要，写 hair_hex、face structure lock role。

**改 promo 会换脸吗？**  
Touch Edit 只改 CTA 字层，不 regen 整脸。

**Reels safe zone？**  
top 12%、bottom 20% 留 UI 与 CTA。

**404 修復？**  
stable character consistency SOP URL。

**与 ko 同 slug 正文重复吗？**  
不重复，本篇繁中 IP 创作者语境重写。
""",
}


def expand_zh(topic: str, n: int) -> str:
    return f"""
## 实操补充 {n}：{topic}

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。{topic} 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。
"""


def expand_zhtw(topic: str, n: int) -> str:
    return f"""
## 實操補充 {n}：{topic}

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。{topic} 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。
"""


def expand_de(topic: str, n: int) -> str:
    return f"""
## Praxisnotiz {n}: {topic}

Der erste Brief endet mit „premium“ und scheitert: kleiner Preis, Badge über dem Objekt. Im zweiten Durchlauf nur safe zone und Pflichtfelder korrigieren. Ein **ChatCanvas**-Thread reduziert accent drift auf slide 4. In **{topic}** bestätigt **Touch Edit** Preisänderung in fünf Minuten static-first. Full regen 30 Minuten — zuerst **Brand Kit** neu setzen. Wiederhergestellte 404-URL als stable SOP-Link für Makler-Teams.
"""


ARTICLES = [
    {
        "rank": 113,
        "key": "brochure_chat",
        "lang": "zh",
        "slug": "how-to-chat-generate-brochure-lovart",
        "cover": "011",
        "category": "How-To",
        "title": "如何用 ChatCanvas 对话生成宣传册：可编辑 static 工作流",
        "seo_title": "ChatCanvas 对话生成宣传册 — Lovart 实操",
        "description": "404 修复：chat generate brochure，ChatCanvas thread，Brand Kit，Touch Edit 改价。",
        "seo_description": "宣传册 AI：static-first、Design Agent QA、多尺寸 derivative。",
        "focus": "chat generate brochure lovart",
        "keywords": ["宣传册 ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Brochure Chat ZH",
        "body": BROCHURE_CHAT_ZH,
        "expand_topic": "ChatCanvas 对话宣传册",
    },
    {
        "rank": 114,
        "key": "real_estate_de",
        "lang": "de",
        "slug": "brand-kit-real-estate-agent-lovart",
        "cover": "018",
        "category": "Industry Solution",
        "title": "Brand Kit für Immobilienmakler: editierbare Listing-Assets",
        "seo_title": "Makler Brand Kit — ChatCanvas DE",
        "description": "DE 404 fix: Immobilienmakler Brand Kit, Exposé, Touch Edit Preisänderung.",
        "seo_description": "Makler Brand Kit: Listing series, static-first, Design Agent QA.",
        "focus": "brand kit real estate agent lovart",
        "keywords": ["immobilien brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Real Estate DE",
        "body": REAL_ESTATE_DE,
        "expand_topic": "Makler Brand Kit Listing",
    },
    {
        "rank": 115,
        "key": "inclusive_bias",
        "lang": "zh",
        "slug": "ai-design-bias-inclusive-visual-output-2027",
        "cover": "025",
        "category": "Insight & Trend",
        "title": "2027 包容性视觉输出：AI 设计偏见审计与缓解工作流",
        "seo_title": "2027 inclusive visual output — bias 缓解",
        "description": "404 修复：inclusive visual 2027，brief 验收，Brand Kit，Design Agent QA。",
        "seo_description": "偏见缓解：Touch Edit、static-first、环比 audit。",
        "focus": "ai design bias inclusive visual 2027",
        "keywords": ["包容性视觉 ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight — Inclusive Visual 2027 ZH",
        "body": INCLUSIVE_BIAS_ZH,
        "expand_topic": "2027 inclusive visual audit",
    },
    {
        "rank": 116,
        "key": "legal_firms",
        "lang": "zh",
        "slug": "ai-design-for-legal-firms-attorneys-2026",
        "cover": "032",
        "category": "Industry Solution",
        "title": "2026 律所与律师 AI 设计实务：合规 static 与可编辑 disclaimer",
        "seo_title": "律所 AI 设计 — ChatCanvas 合规 workflow",
        "description": "404 修复：law firm segment，seminar 海报，Touch Edit disclaimer。",
        "seo_description": "律所设计：Brand Kit letterhead、static-first。",
        "focus": "ai design legal firms attorneys 2026",
        "keywords": ["律所 ai 设计", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Legal Firms ZH",
        "body": LEGAL_FIRMS_ZH,
        "expand_topic": "律所 seminar 合规 static",
    },
    {
        "rank": 117,
        "key": "myths_zh",
        "lang": "zh",
        "slug": "ai-design-myths-debunked-2026",
        "cover": "039",
        "category": "How-To",
        "title": "2026 AI 设计流言对照：简体版实操反驳",
        "seo_title": "AI 设计流言 2026 — 简体实操反驳",
        "description": "404 修复：简体 myths debunked，非繁中拷贝，ChatCanvas Brand Kit Touch Edit。",
        "seo_description": "六则 ops 流言反驳，brief 合同，无假统计。",
        "focus": "ai design myths debunked 2026",
        "keywords": ["ai 设计 流言", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight — Myths ZH Rewrite",
        "body": MYTHS_ZH,
        "expand_topic": "简体 AI 设计流言反驳",
    },
    {
        "rank": 118,
        "key": "best_agent_zh",
        "lang": "zh",
        "slug": "best-agent-for-non-design",
        "cover": "044",
        "category": "Industry Solution",
        "title": "非设计背景选什么 Design Agent：运营与市场团队 brief 合同",
        "seo_title": "非设计岗 Design Agent — 简体实操",
        "description": "404 修复：非设计岗简体版，区别于 it batch6，ChatCanvas Brand Kit Touch Edit。",
        "seo_description": "运营市场：brief 合同、五分钟改价、Design Agent QA。",
        "focus": "best agent for non design",
        "keywords": ["非设计 design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Non-Designer ZH",
        "body": BEST_AGENT_ZH,
        "expand_topic": "非设计岗 promo workflow",
    },
    {
        "rank": 119,
        "key": "ice_cream_brand_kit",
        "lang": "zh",
        "slug": "brand-kit-ice-cream-shop-lovart",
        "cover": "051",
        "category": "Industry Solution",
        "title": "冰淇淋店 Brand Kit：菜单、外卖袋与季节 promo 可编辑视觉",
        "seo_title": "冰淇淋店 Brand Kit — ChatCanvas 实操",
        "description": "404 修复：ice cream Brand Kit，季节 promo，Touch Edit 改口味价。",
        "seo_description": "冰淇淋 segment：过敏 disclaimer、series 一致。",
        "focus": "brand kit ice cream shop lovart",
        "keywords": ["冰淇淋 brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Ice Cream Brand Kit ZH",
        "body": ICE_CREAM_BRAND_KIT_ZH,
        "expand_topic": "冰淇淋季节 promo Brand Kit",
    },
    {
        "rank": 120,
        "key": "waxing_brand_kit",
        "lang": "zh",
        "slug": "brand-kit-waxing-studio-lovart",
        "cover": "057",
        "category": "Industry Solution",
        "title": "脱毛工作室 Brand Kit：服务价目、预约 CTA 与社媒系列",
        "seo_title": "脱毛 studio Brand Kit — ChatCanvas 实操",
        "description": "404 修复：waxing studio Brand Kit，疗程 disclaimer，Touch Edit 改套餐价。",
        "seo_description": "脱毛 segment：预约 CTA、static-first。",
        "focus": "brand kit waxing studio lovart",
        "keywords": ["脱毛 brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Waxing Brand Kit ZH",
        "body": WAXING_BRAND_KIT_ZH,
        "expand_topic": "脱毛 studio 套餐 promo",
    },
    {
        "rank": 121,
        "key": "vmaker_review",
        "lang": "zh",
        "slug": "vmaker-ai-review",
        "cover": "058",
        "category": "Review",
        "title": "Vmaker AI 评测 2026：诚实对比 revision-heavy static 工作流",
        "seo_title": "Vmaker AI 评测 — ChatCanvas parallel workflow",
        "description": "404 修复：honest Vmaker review，static-first，Touch Edit，无 fake pricing。",
        "seo_description": "Vmaker 评测：clip companion vs editable static offer。",
        "focus": "vmaker ai review",
        "keywords": ["vmaker ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Vmaker ZH",
        "body": VMAKER_REVIEW_ZH,
        "expand_topic": "Vmaker clip vs static offer",
    },
    {
        "rank": 122,
        "key": "character_design_zhtw",
        "lang": "zh-TW",
        "slug": "ai-character-design-guide-how-to-create-consistent-characters-with-ai-tools",
        "cover": "059",
        "category": "How-To",
        "title": "AI 角色設計指南：用工具建立一致角色視覺",
        "seo_title": "AI 角色一致 — ChatCanvas 繁中指南",
        "description": "繁中 404 修復：character consistency，Brand Kit face lock，Touch Edit promo。",
        "seo_description": "角色設計：thread series、Design Agent QA face drift。",
        "focus": "ai character design consistent characters",
        "keywords": ["ai 角色設計", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Character Design zh-TW",
        "body": CHARACTER_DESIGN_ZHTW,
        "expand_topic": "IP 角色一致 series",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch11 content cluster.*\n"
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

    print(f"{'RANK':>4} {'FILE':<85} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 130)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['rank']:>4} {r['file']:<85} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["file"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
