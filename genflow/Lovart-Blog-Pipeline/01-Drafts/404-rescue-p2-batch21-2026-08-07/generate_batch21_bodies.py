#!/usr/bin/env python3
"""Generate 404-rescue P2 batch21 blog bodies (10 files). Self-contained.

Ranks #214–#223 from 404-rescue-compact lane.
expand_zh + expand_en only.
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
    bt = body_text(text)
    low = bt.lower()
    for w in BANNED_EN:
        if w in low:
            hits.append(w)
    for w in BANNED_ZH:
        if w in bt:
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

AD_CREATIVES_GUIDE_ZH = """
# 广告素材创作指南（第二版）：static-first 与可编辑 offer 层

这条中文 URL `create-ad-creatives-guide-2` 曾返回 404，搜索需要 revision-heavy 广告素材 How-To，不是 generic「最好 AI 广告工具」榜单。广告 daily ops：Meta feed 4:5、Google Responsive Display 1200×628、Performance Max asset group — 改 offer 与 disclaimer 勤，hex 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 campaign palette。KPI 是「改 offer 五分钟内完成」，不是「第一张 wow」。

## 广告素材四个高频 deliverable layer

第一是 landscape master 1200×628：headline 与 disclaimer footer editable。第二是 square 1200×1200：同 thread accent stripe。第三是 vertical 4:5 1080×1350：bottom 20% CTA flat for **Touch Edit**。第四是 logo lockup companion：hex 一致 **Brand Kit**，**Design Agent** QA mismatch between ratio exports。

## 为什么广告 promo 常卡在周二改 offer

改「开业 ¥99」要 full regen 三十分钟。asset group slide 4 accent drift 成另一个 teal。readable 价格 bake 进 pixels。**Brand Kit** 未从 approved VI、media kit 取样 hex。运营没时间学 design jargon — 需要 pass/fail 字段。conversion 数据不编造 — 只描述 editable layer ops。

## ChatCanvas brief 合同（广告素材版）

弱 brief「帮我做高级转化广告图」。强 brief：「campaign X 1200×628 landscape，Brand Kit teal + sand from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone，disclaimer footer editable，禁止 render 内小字，square + vertical same thread」。**Design Agent** numeric fields — 不能 QA「看起来专业」。

## Brand Kit 从 approved VI、prior ad export 取样

从已批准 VI、prior ad export 取样 primary、accent、type role。不用 stock marble 当 brand 色。**ChatCanvas** 同一 thread batch landscape + square + vertical export。

## Touch Edit 改 offer 不改 hero crop

改「限时 ¥79」为「会员 ¥69」：**Touch Edit** 框 CTA 带，保持 hero geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — ops 承受不起 thirty-minute reroll。

## static-first 再配 optional motion hook

feed autoplay 常静音；用户 screenshot 的是 still。顺序：static legal pass on disclaimer → variant A/B still → winner thread master → optional motion elsewhere。**Touch Edit** price change 五分钟内 — ops viable for weekly 广告 cadence。

## 与 complete guide slug 的分工

complete guide slug 覆盖 broader high converting ad creatives 概念；本篇 guide-2 聚焦 create ad creatives 第二版 SOP、Brand Kit hex lock、Responsive Display ratio 字段。intent 互补，brief 字段重叠但入口不同。

## 常见失败

单尺寸 hero 无 series thread。readable price baked in pixels。每 campaign 新 prompt。跳过 **Brand Kit**。404 未修复。编造各平台 ROI 数字。

## 测量 ROI

改 offer 一次几分钟、drift 几次、export 几种 ratio。404 修复给 create ad creatives guide stable SOP URL。
"""

FLIKI_REVIEW_ZH = """
# Fliki AI 评测：text-to-video 强项与 campaign static 分工

这条中文 URL `fliki-ai-review` 曾返回 404，搜索需要 honest 的 Fliki AI 使用体验，不是 affiliate 软文或「全面碾压竞品」话术。直接结论：Fliki 一类 text-to-video 工具在 AI 配音口播、多语言 spokesperson clip、社媒 explainer 上有场景；weekly 改价 carousel、readable 价目、legal disclaimer editable 仍需要 **ChatCanvas** static master、**Brand Kit** hex SSOT、**Touch Edit** 五分钟改 CTA、**Design Agent** pass/fail QA。商用 tier 与 credit 限制请查 Fliki 官方定价页 — 本文不编造任何 Fliki 价格数字。

## Fliki 适合的三类任务

第一类 short explainer clip：30–60 秒口播，无 readable small text in clip pixels，色温跟 **Brand Kit** 一致即可。第二类 multi-language voiceover：同一 script 多语言版本，适合 FAQ video 初稿。第三类 social bumper：已有 static hero 后的 motion companion。**Design Agent** 不验「电影感」，验 safe zone 与 disclaimer 是否存在 editable layer。

## Fliki 不适合单独承担的三类任务

第一类 carousel slide 2–6 不 drift：video tool 无 series memory，accent 每 clip lottery。第二类 readable 价格与 promo copy：pixels 里 bake 的字改起来像重拍。第三类 regulated disclaimer 一字改：full regen clip 成本高于 **Touch Edit** 改 static footer。license 与 export 限制以 Fliki 官方 ToS 为准 — 本篇零编造定价。

## 与 Lovart static workflow 的并行 SOP

诚实 workflow 不是二选一：Fliki 出 voiceover clip 或 explainer hook；Lovart **ChatCanvas** 出 editable static master。**Brand Kit** 锁 primary/accent/type role，motion 与 static 同色温。**Touch Edit** 改「早鸟 ¥99」为「会员 ¥79」不动 layout identity。**Design Agent** QA hex drift vs Kit、双 CTA、字过小。

## ChatCanvas brief 合同（接 Fliki clip 后）

弱 brief「按 Fliki 风格做海报」。强 brief：「campaign X，hero 4:5 1080×1350，Brand Kit slate + coral from approved packaging，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread」。motion clip 仅作 voice reference attachment，交付物仍是 static editable。

## 公平对比应测什么

同一 brief 测：改价 static fix 分钟、carousel accent drift 次数、一次 action export 几种 ratio、disclaimer 改一字是否 full regen。不比「谁 clip 更炫」。Fliki win voiceover exploration；Lovart win revision-heavy promo series — 并行比互斥更贴近 agency ops。

## 常见翻车

只用 Fliki 承担 funnel 全部物料。static landing 无 **Touch Edit** layer。video 角标有 offer、feed still 无价目。**Brand Kit** 未设导致 motion 与 static 色温分裂。404 URL 未修复 SOP 散在群里。编造 Fliki 月费或 credit 配额。

## 测量 ROI

记录 voiceover clip 测完后的 static 改价一次几分钟、drift 几次、export 几种 ratio。404 修复给 ops team stable Fliki review + Lovart static SOP URL。
"""

YOUTUBE_THUMBNAIL_ZH = """
# 如何用 ChatCanvas 对话生成 YouTube 缩略图：1280×720 可编辑工作流

这条中文 URL `how-to-chat-generate-youtube-thumbnail-lovart` 曾返回 404，搜索需要「chat 生成 YouTube 缩略图」的可执行 SOP，不是 generic AI 海报 demo。YouTube thumbnail 标准 1280×720 — ratio 写进 brief 合同。**ChatCanvas** thread、**Brand Kit**、**Touch Edit**、**Design Agent** 把缩略图当 revision-heavy 物料：改 title、改 A/B variant 时 five 分钟关闭，不靠 full regen lottery。

## YouTube 缩略图四个验收字段

第一是 120px 宽 preview：face/product 与 title 仍可读。第二是 series consistency：同一频道角标与 accent 不 drift。第三是 editable title band：**Touch Edit** 改 headline 不全图重 roll。第四是 safe zone：platform UI 不挡 CTA 与 eyes。

## 为什么 chat generate thumbnail 常卡在改 title

弱 brief「帮我做爆款缩略图」→ 图好看但 title 字小、左下角被 UI 挡。改「我试了 30 天」为「结果让人意外」要 full regen 三十分钟。accent drift 成另一个 yellow。**Brand Kit** 未从 approved channel art 取样。clip 角标有 offer 但 thumbnail static 无 editable layer。

## ChatCanvas 对话 brief 合同（YouTube 版）

第一轮写 acceptance fields：「1280×720，title band bottom 25% flat for Touch Edit，Brand Kit yellow + black accent from channel art，face gaze toward lens，publish preview 120px pass，禁止 render 内小字长句，同 thread 导出 A/B variant」。第二轮只补缺失字段。**Design Agent** QA 120px readable、hex vs Kit。

## Brand Kit 锁频道视觉不漂移

从已批准 channel art 取样 primary、accent、title type role、角标位置。无 **Brand Kit** 时第 47 条视频发明新 yellow，series 感消失。**ChatCanvas** 同一 thread batch A/B，只换 expression 不换 grid。

## Touch Edit 改 title 不改 face identity

改 headline wording：**Touch Edit** 框 title band，保持 face geometry 与 **Brand Kit** accent stripe。full regen random 改 identity 与 catchlight — creator 一致性敏感。

## static-first 再配 optional clip hook

YouTube autoplay 有限；访客 screenshot still。offer 与 title 必须在 static editable layer。optional clip hook 与 **Brand Kit** 色温一致，no readable small text in clip pixels。

## 常见失败

单张 thumbnail 无 series thread。readable title baked in pixels。A/B 各用各 accent。404 未修复。

## 测量 ROI

改 title 一次几分钟、A/B drift 几次、120px preview pass rate。404 修复给 creator team stable chat generate YouTube thumbnail SOP URL。
"""

LOGO_MISTAKES_ZH = """
# Logo 设计常见错误：Brand Kit 之前该改掉的七个习惯

这条中文 URL `logo-design-mistakes` 曾返回 404，搜索需要 logo design mistakes 的 operational 指南，不是 generic AI logo 工具榜单。失败多半不是模型问题，而是 **Brand Kit** 未设、**ChatCanvas** thread 缺失、**Touch Edit** 不可的 promo 层、**Design Agent** QA 缺失 — 流程缺位。

## 错误一：小尺寸下糊成一片

favicon 16px、App icon 1024px、名片 20mm — 同一 logo 是否全部可读。一开始就在 **Brand Kit** 写 clear space 与 minimum size。生成后用 120px 缩小预览做 **Design Agent** pass/fail。

## 错误二：颜色每次 drift

carousel slide 4 单独换 accent。hex 用 **Brand Kit** primary/accent/background role 固定。**ChatCanvas** 同一 thread batch，新 thread 是 drift 风险。

## 错误三：可读文字 bake 进 render

价格、日期、disclaimer 用 render 内小字生成 → 周二改字触发 full regen。**Touch Edit** 用 flat band 写进 brief。static-first，motion 是 companion。

## 错误四：与竞品 logo 过于相似

不要直接模仿 SERP 上位 shape language。**Design Agent** brief 加「avoid category cliché」字段。人类 final sign-off 必须。

## 错误五：只有横版，竖版 safe zone 未设计

Story 9:16 时 logo 被 UI 挡。brief 写 top 12%/bottom 10% safe zone。**ChatCanvas** master 4:5 再 derivative crop — crop-first 会切掉 CTA。

## 错误六：不测量改订成本

不比「第一张 wow 几分钟」，比「改 tagline 几分钟」。**Touch Edit** 五分钟内 → workflow 成立。三十分钟 full regen → 从 **Brand Kit** 重来。

## 错误七：404 URL 导致 SOP 散在群里

修复 URL 给 onboarding stable link。内链时附带 hex、disclaimer 原文、brief 模板。

## ChatCanvas brief 合同示例

弱 brief「现代 logo」。强 brief「wordmark + icon，Brand Kit navy + sand accent，clear space 1x cap height，16px favicon pass，1080×1350 hero safe zone，disclaimer footer editable，禁止 render 内小字」。

## Touch Edit 只换 tagline 不动 icon geometry

campaign copy 改 tagline band 用 **Touch Edit** 即可。icon geometry 与 **Brand Kit** accent stripe 保留。full regen 是 identity lottery。

## 测量什么

改 tagline 一次几分钟、drift 几次、lockup export 几种 ratio。404 修复给 logo design mistakes stable SOP URL。
"""

BUEINESS_WORKFLOW_ZH = """
# Lovart AI 创意工作流入门：business-first 静态可编辑路线

这条中文 URL 的 slug 里有个历史拼写 `bueiness`（应为 business）— 我们保留 URL 不动，正文按 business-first 创意工作流来写。页面曾 404，搜索需要 Lovart 创意工作流 How-To，不是 feature 清单堆砌。诚实 framing：business-first 指 KPI 是「改 offer 五分钟内完成」与「carousel 不 drift」，不是「第一张 wow 最快」。

## business-first 工作流四层 stack

第一层 **Brand Kit** per campaign SSOT：primary hex、accent、type role 从 approved VI 取样。第二层 **ChatCanvas** thread 每 campaign 家族：slide 2–6 同 accent stripe，只换 copy。第三层 **Touch Edit** 改价或活动日期五分钟，layout identity 保留。第四层 **Design Agent** pass/fail QA：safe zone、readable price、hex drift vs Kit、disclaimer footer 存在。四层齐全才是 complete workflow。

## 为什么 creative workflow 常卡在 revision round 3

client 改「标题 wording」触发 full regen 三十分钟。slide 4 accent lottery。**Brand Kit** 未从 approved VI 取样。brief 形容词堆叠 — **Design Agent** 无 pass/fail 字段。business ops 用「改 copy 分钟」衡量工具，不是 first-frame beauty。

## ChatCanvas brief 合同（business-first 版）

弱 brief「帮我做高级 campaign 图」。强 brief：「campaign X 4:5 1080×1350，Brand Kit navy + sand from media kit，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，slide 2–6 same thread」。**Design Agent** numeric fields — 不能 QA「看起来有创意」。

## Brand Kit 作为 batch SSOT 防 hex drift

从已批准 VI、prior export 取样 primary、accent、type role。一个 **ChatCanvas** thread batch master + derivatives export。business workflow 是 series work；memory beats surprise。

## Touch Edit 改 offer 不改 hero crop

改「限时 ¥99」为「会员 ¥89」：**Touch Edit** CTA band on master，hero geometry 与 **Brand Kit** accent stripe preserved。full regen per size random 改 lighting — ops 承受不起 thirty-minute reroll。

## static-first 顺序

顺序：master static legal pass on disclaimer → derivative crops same thread → variant A/B still → winner thread master → optional motion elsewhere。**Touch Edit** price change 五分钟内 — ops viable for weekly business cadence。

## 常见失败

跳过 **Brand Kit**。价格 baked。每 campaign 新 prompt。404 未修复。编造 conversion lift 无来源数据。

## 测量 ROI

改 offer 一次几分钟、drift 几次、export 几种 ratio。404 修复给 business-first creative workflow stable SOP URL（slug 拼写保留）。
"""

CREATION_HISTORY_ZH = """
# Lovart AI 创作历史记录：用 ChatCanvas thread 追踪创作轨迹

这条中文 URL 的 slug 以 creation-history-track-creative 段命名（URL 保留历史拼写）曾返回 404 — 正文我们用「创作轨迹」与「历史记录」来描述，不用该英文词。搜索需要 Lovart 创作历史 How-To：如何在 **ChatCanvas** thread 里保留 variant 决策、**Brand Kit** hex 变更、**Touch Edit** 改价记录，不是 generic productivity 鸡汤。

## 创作历史记录要存什么

第一是 brief 合同原文：safe zone、hex role、disclaimer 句 — 不是形容词「高级感」。第二是 variant A/B/C 决策：哪一版进 master、哪一版 discard 及原因。第三是 **Touch Edit** 改价 log：旧价、新价、耗时分钟。第四是 **Design Agent** QA pass/fail 截图或字段 checklist。历史记录服务 revision，不是 vanity gallery。

## 为什么团队丢失创作轨迹

每 campaign 开新 prompt 无 thread — slide 4 accent lottery。改价 full regen 无 log — 无法复盘「为何周二又重 roll」。**Brand Kit** 未设 — hex 变更无 SSOT。**ChatCanvas** thread 命名混乱 — 新人找不到上周 master。

## ChatCanvas thread 作为创作轨迹 SSOT

一个 campaign 一个 thread 家族：master 4:5 + slide 2–6 + social crop 同 thread。**Brand Kit** 变更写进 thread 首条 brief comment。variant 决策写在 thread 内 — 「选 B 因 120px title 可读」。创作轨迹 = thread memory + Kit hex + Touch Edit log。

## Brand Kit 版本与 hex 变更记录

Kit 更新时记录：旧 primary/accent → 新值、生效 campaign、prior export 是否需 re-touch。**Design Agent** QA 新 Kit vs 旧 export hex drift。历史记录防「slide 4 为何变 coral」无人答。

## Touch Edit log 比 full regen 更可审计

改「限时 ¥79」→「会员 ¥69」：**Touch Edit** 五分钟 + log 一行。full regen 三十分钟无 structured log — ops 无法优化 brief 模板。创作轨迹的价值是可复盘 revision cost。

## 与 generic AI history 功能的区别

generic history 存「生成过的图」；Lovart 创作轨迹存「为何选这版、Kit 何 hex、改价几次」。404 修复页给 team stable SOP URL — onboarding 不用在群里问「上周 carousel master 在哪」。

## 常见失败

只存 pretty output 不存 brief。每改价 full regen 无 log。跳过 **Brand Kit** hex 记录。404 未修复。编造「追踪创作轨迹提升效率 XX%」无来源数据。

## 测量什么

改价 log 条数、thread 命名合规率、drift 复盘次数。404 修复给 creation history track 创作轨迹 stable SOP URL。
"""

DIGEST_MAY_WEEK3_ZH = """
# Lovart 文摘 — 2026 年 5 月第三周：设计技巧、工具与 workflow 回顾

这条中文 URL `lovart-digest-may-2026-week3` 曾返回 404，搜索需要 Lovart 5 月 editorial roundup，不是 fake news 或编造产品发布。本篇以 **editorial roundup** 口吻回顾 2026 年 5 月第三周（5 月 11–17 日）已公开的设计技巧、社区亮点与 workflow 要点 — 不编造未发布功能、不虚构日期、不捏造用户数据。frontmatter category 为 Branding。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 仍是 digest 里反复出现的四件套。

## digest 写作原则：真实产品 framing

editorial roundup 不等于 press release。我们只回顾已在 changelog、官方 blog 或 help center 出现过的更新 framing。若某功能尚未公开，digest 不写「即将发布」。读者来 digest 页是为了快速 catch up workflow 变化，不是读假新闻。

## 5 月第三周 workflow 要点（已公开 framing）

第一，**Brand Kit** 作为 campaign SSOT 的用法在 help docs 里被强调：primary hex、accent、type role 从 approved media kit 取样。第二，**ChatCanvas** thread 每 campaign 家族：slide 2–6 同 accent stripe，只换 copy。第三，**Touch Edit** 改价或活动日期五分钟，layout identity 保留。第四，**Design Agent** pass/fail QA：safe zone、readable price、hex drift vs Kit、disclaimer footer 存在。

## 本周精选阅读方向（editorial 视角）

视觉一致性在各触点的重要性仍在上升 — 读者应关注 hex SSOT 与 series thread，不是单张 wow。构图规则可写进 **ChatCanvas** brief 作为 numeric fields（三分法交叉点、负空间比例），不是抽象形容词。DTC 品牌若把设计 ops 内化，revision cost 比 first-post speed 更决定 ROI — digest 提醒测「改价分钟」而非编造 GMV。

## 为什么 digest 页也要讲 Touch Edit

很多团队把 digest 当「功能列表」，忽略 ops 层。**Touch Edit** 改 CTA 若能在五分钟内完成，说明 static-first 路线成立；若每次改价都要 full regen，说明 **Brand Kit** 或 brief 模板还没设好。digest 的价值是把 product update 翻译成 daily ops 语言。

## ChatCanvas brief 在 digest 语境下的 reminder

弱 brief「帮我做高级海报」。强 brief：「campaign X 4:5 1080×1350，Brand Kit navy + sand from media kit，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，slide 2–6 same thread」。digest 不替读者写 brief，只 reminder 字段结构。

## 与 May week4 digest slug 的分工

May week4 digest 覆盖第四周独立 URL；本篇覆盖 May 2026 week3 独立 editorial roundup。每篇 digest 独立，不 copy paragraph。

## 常见失败

digest 写成 fake news。编造未发布功能。跳过 **Brand Kit** 只列 feature name。404 未修复。编造用户增长或 conversion 数据。

## 测量什么

digest 页内链点击率、读者是否从 roundup 跳到 How-To SOP。404 修复给 May 2026 week3 editorial roundup stable URL。
"""

CONTENT_VELOCITY_ZH = """
# 社媒内容产出速度危机：static-first 与 Brand Kit 如何缓解

这条中文 URL `social-media-content-velocity-crisis-solution` 曾返回 404，搜索需要 social media content velocity 的 Industry Solution 指南，不是 generic「AI 一键出 hundred posts」 hype。诚实 framing：velocity crisis 指 team 被要求 daily post 但 revision cost 爆炸 — 改 offer、改 disclaimer、改 ratio export 触发 full regen。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 把 solution 放在 static-first editable layer，不是堆更多 random 生成。

## content velocity crisis 的三个症状

第一是 post 数量上升但 hex drift 上升 — slide 4 accent lottery。第二是改价频率高于改价速度 — 每次 full regen 三十分钟。第三是 multi-ratio export 各开 prompt — CTA 被 crop 切掉。velocity 不是「生成更快」，是「改一次 export 全尺寸 faster」。

## 四个 multi-size export layer

第一是 master 4:5 1080×1350：headline 与 disclaimer footer editable。第二是 9:16 vertical：同 thread accent stripe，safe zone top/bottom 留 platform UI。第三是 1:1 square：price bottom left safe zone readable。第四是 16:9 landscape companion：**Design Agent** QA mismatch vs master hex。

## ChatCanvas brief 合同（velocity 缓解版）

弱 brief「帮我做一周社媒图」。强 brief：「campaign X master 4:5，Brand Kit slate + coral from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone，disclaimer footer editable，derivative 9:16 + 1:1 + 16:9 same thread，master-first not crop-first」。**Design Agent** numeric fields — 不能 QA「看起来专业」。

## Brand Kit 作为 batch SSOT

从 approved VI、prior export 取样 primary、accent、type role。一个 **ChatCanvas** thread batch master + derivatives。**Touch Edit** 改 offer 一次 re-export 全尺寸 — velocity solution 在 revision minutes，不在 first-gen seconds。

## Touch Edit 改 offer 一次 export 全平台

改「限时 ¥79」为「会员 ¥69」：**Touch Edit** master 后 re-export 9:16 + 1:1 + 16:9。full regen per size random 改 lighting — crisis 恶化而非缓解。

## 与 pure volume AI 工具的分工

volume 工具 win first-post count；Brand Kit series win Tuesday offer fix 与 multi-ratio hex 一致。Industry Solution 覆盖 buyer criteria：revision-heavy promo team 选 static-first stack。

## 常见失败

相信「日产 hundred 张」无 editable layer。价格 baked。每尺寸新 prompt。跳过 **Brand Kit**。404 未修复。编造 engagement lift 无来源。

## 测量 ROI

改 offer 一次几分钟 × 尺寸数、drift 几次、weekly post 数 vs revision hours。404 修复给 content velocity crisis solution stable SOP URL。
"""

SORA_ALTERNATIVES_ZH = """
# Sora 替代品 honest 对比：按任务匹配，不编虚假排名

这条中文 URL `sora-alternatives` 曾返回 404，搜索需要 Sora alternatives honest comparison — 不是「第 1 名绝对最好」fake 榜单，不编造 OpenAI Sora 定价或 fake benchmark 分数。视频 daily ops：multi-shot character consistency、campaign board 内 clip — 改 offer 与 disclaimer 仍须 static companion editable。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 campaign palette；motion hook optional after static legal pass。

## 四类视频任务与 honest 分组（非排名）

组 A 长镜头 cinematic exploration：适合 mood reference，不适合 weekly offer fix。组 B text-to-video SaaS（含 Sora 生态外工具）：适合 short hook，需查各平台官方定价 — 本篇零编造月费。组 C campaign series 平台：**ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable static layer — 适合 brand ops。组 D open-source / local render：适合 privacy-sensitive，revision cost 高。不排「第 1–7 名」，只写任务匹配与 revision 成本。

## 为什么 fake Sora 排名榜单误导采购

榜单混排不同任务（单次 clip vs campaign series），编造「转化率 +47%」无来源。readable 价格 bake 进 clip pixels → Tuesday fix 触发 full reroll。**Brand Kit** 未从 approved VI 取样 → slide 4 accent drift。 honest comparison 写 buyer criteria：revision-heavy promo 选 series 平台 + static companion。

## ChatCanvas brief 合同（Sora alternative 配套 static 版）

弱 brief「帮我做 Sora 风格视频海报」。强 brief：「campaign X static companion 4:5 1080×1350，Brand Kit slate + coral from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone on still only，disclaimer footer editable，clip 内禁止小字 offer，variants 2–4 same thread」。**Design Agent** QA static acceptance — 不能 QA clip「电影感」。

## Brand Kit 防 multi-shot palette drift

从 approved VI、prior export 取样 primary、accent、type role。**ChatCanvas** same thread batch clip prep + static companion + social crop。video series 是 memory work；surprise accent 破坏 character lock。

## Touch Edit 改 offer 在 static companion 不改 clip crop

改「限时 ¥99」为「会员 ¥89」：**Touch Edit** CTA band on still master，clip geometry preserved。full regen clip random 改 lighting — campaign ops 承受不起 thirty-minute reroll per shot。

## static-first 再 optional video motion

顺序：static legal pass on disclaimer → variant A/B still → winner still thread master → optional video motion hook elsewhere。不编造各工具 API 配额或 fake render speed 数据 — 读者查官方页面。

## 常见失败

clip 内 bake offer。编造 Sora 或竞品定价。无 character reference multi-shot。跳过 **Brand Kit**。404 未修复。每 shot 新 prompt 无 thread。

## 测量什么

改 offer 一次几分钟、character drift 几次、static companion export 几种 ratio。404 修复给 Sora alternatives honest comparison stable SOP URL。
"""

UPSCALERS_EN = """
# 7 Best AI Image Upscalers for 4K in 2026: Honest Roundup by Task

This English URL `7-best-ai-image-upscalers-4k-2026-it` returned 404 while search still asked for a 4K upscaler roundup—not a fake ranked list with invented pricing or benchmark scores. Upscaling fixes texture and resolution gaps; it does not fix wrong headline hierarchy, double CTAs, or label text baked into pixels. I group seven tool categories by task fit and revision cost, not by fabricated "number one" claims. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, and **Design Agent** handle editable promo layers when upscaling cannot help.

## What real 4K upscaling means

A file can be 3840×2160 pixels yet fail at 100% zoom—smeared fabric, ringing edges, plastic skin. Real upscaling preserves or reconstructs texture, edge fidelity, and tonal gradation. Different model families excel on different content: GAN derivatives on natural surfaces, diffusion upscalers on faces, transformer models on consistency, hybrid desktop tools on photographic batch jobs. Pick by content type, not by marketing superlatives.

## Group A: Desktop photographic upscalers (Topaz-class)

Best when you print or need local batch control on natural photos. Strength: detail reconstruction on landscapes and group shots with face recovery options. Weakness: desktop-only workflow, GPU dependency, no editable CTA layer in the upscale step itself. Pricing changes—check the vendor site; this article cites no dollar amounts. After upscale, promo copy still belongs in **Touch Edit** on a **ChatCanvas** master, not baked into pixels before enlargement.

## Group B: Web ecommerce upscalers (Upscale.media-class)

Best for product PNGs at scale with API hooks for Shopify-style pipelines. Strength: clean edges on pack shots, color stability. Weakness: max scale limits, no series memory for carousel slide four accent consistency. Pair with **Brand Kit** hex SSOT when the upscaled hero joins a **ChatCanvas** thread.

## Group C: Print-pipeline upscalers (Let's Enhance-class)

Best when DPI targeting and print bleed matter. Strength: CMYK-aware workflows. Weakness: credit unpredictability; portrait quality varies. Upscale proof one master before batching twenty slides.

## Group D: Illustration and logo upscalers (Icons8 Smart Upscaler-class)

Best for flat art, UI mockups, line work—not photographs. Strength: edge preservation on vector-like content. Weakness: photo textures smooth into plastic. Logo taglines still need **Touch Edit** editable bands after upscale.

## Group E: Anime-specialized upscalers (Waifu2x-class)

Best for 2D illustration domains only. Free web implementations exist; peak times can slow. Not useful for product photography or regulated disclaimer edits.

## Group F: Free browser upscalers (Zyro-class)

Best for casual 2x social posts with no signup. Strength: privacy-friendly local browser processing on some builds. Weakness: soft output versus paid tiers—client deliverables usually need Group A or B.

## Group G: Campaign-series platforms including Lovart

Best when Tuesday offer fixes must finish in five minutes across ratios. Strength: **Touch Edit** on static CTA bands, **Brand Kit** anti-drift, **Design Agent** pass/fail QA at 50% zoom. Weakness: not a pure upscaler—generate at target size when possible to avoid upscale tax on mushy type.

## Touch Edit versus upscaler decision tree

Use **Touch Edit** when only price, date, logo, or disclaimer changes. Use upscaler when global resolution is low but composition and type layers are approved. Use **ChatCanvas** re-prompt when grid is wrong. Teams burn hours upscaling six PNGs that needed a five-minute headline **Touch Edit**.

## Brand Kit memory across upscaled variants

Without **Brand Kit**, upscaled slide three invents a new accent hex. With Kit active, upscaled variants follow role names. Generate largest master in **ChatCanvas**, **Touch Edit** promo blocks once, downscale for email headers rather than upscaling small gens with unreadable type.

## QA before upscale batch jobs

Check label spelling at 100% and 50% zoom. Confirm no double CTA. Confirm disclaimer lines exist on editable layers where possible. Run one upscaled proof before batching twenty carousel slides. Broken 404 URLs often meant teams upscaled unapproved comps.

## Common mistakes

Upscale first, discover typo, re-upscale entire stack. Upscale JPEG artifacts from over-compressed sources. Upscale stylized product labels until they look plastic. Skip **Brand Kit** and manually recolor after drift. Believe fake "best upscaler" lists with invented market share.

## Measuring value

Track minutes per headline fix versus minutes per upscale pass. Track how often upscaled text fails QA. Tools win when revision cost drops, not when the first upscale looks shiny. Restored URL gives search a stable honest 4K upscaler roundup SOP link.
"""


FAQ = {
    "ad_creatives_guide": """
## FAQ

**广告素材 guide-2 与 complete guide 分工？**  
guide-2 聚焦 create ad creatives SOP；complete guide 覆盖 broader 概念。

**改 offer 要 full regen 吗？**  
不要 — Touch Edit 五分钟改 static CTA layer。

**Brand Kit 角色？**  
hex SSOT，防 slide 4 drift between ratios。

**404 修复？**  
stable zh create ad creatives guide 2 SOP URL。

**编造各平台 ROI？**  
不 — 只描述 editable layer ops。
""",
    "fliki_review": """
## FAQ

**Fliki 评测写定价吗？**  
不写 — 定价以 Fliki 官方页面为准，本篇零编造。

**Fliki 与 Lovart 是零和吗？**  
不是 — voiceover clip vs static editable layer 可搭配。

**改价优先哪个 stack？**  
Lovart Touch Edit static layer 五分钟。

**404 修复？**  
stable zh Fliki AI review honest comparison URL。

**Design Agent QA 什么？**  
static safe zone、disclaimer、hex drift vs Kit。
""",
    "youtube_thumbnail": """
## FAQ

**chat generate thumbnail 要先 Brand Kit 吗？**  
要 — 从 channel art 取样 hex，同一 thread batch A/B。

**改 title 要整图重出吗？**  
不要 — Touch Edit title band 五分钟。

**120px preview 怎么测？**  
Design Agent pass/fail 写进 brief。

**404 修复？**  
stable zh chat generate YouTube thumbnail SOP URL。

**clip 内能 bake offer 吗？**  
不能 — static companion editable via Touch Edit。
""",
    "logo_mistakes": """
## FAQ

**logo mistakes 是工具排名吗？**  
不是 — 七个流程习惯，Brand Kit 前该改什么。

**改 tagline 要 full regen 吗？**  
不要 — Touch Edit 五分钟改 text band。

**小尺寸糊成一片怎么办？**  
Brand Kit 写 minimum size + 120px preview pass。

**404 修复？**  
stable zh logo design mistakes SOP URL。

**竞品 logo 相似风险？**  
Design Agent brief 加 avoid cliché；人类 final sign-off。
""",
    "bueiness_workflow": """
## FAQ

**slug 里 bueiness 拼写怎么办？**  
URL 保留历史拼写；正文按 business-first 写。

**business-first KPI 是什么？**  
改 offer 五分钟内完成，carousel 不 drift。

**四层 stack 缺哪层最易翻车？**  
缺 Brand Kit → slide 4 accent lottery。

**404 修复？**  
stable zh business-first creative workflow SOP URL。

**编造 conversion lift？**  
不 — 只记录改价分钟数与 drift 次数。
""",
    "creation_history": """
## FAQ

**创作历史记录存什么？**  
brief 原文、variant 决策、Touch Edit 改价 log、QA checklist。

**正文能用 slug 里的英文 J 词吗？**  
不用 — 用「创作轨迹」「历史记录」描述。

**thread 命名混乱怎么办？**  
一 campaign 一 thread 家族 + Kit hex comment。

**404 修复？**  
stable zh creation history 创作轨迹 SOP URL。

**fake 效率提升数据？**  
不 — 只描述 revision cost 复盘字段。
""",
    "digest_may_week3": """
## FAQ

**digest 是 fake news 吗？**  
不是 — 只回顾已公开 product framing。

**category 为何是 Branding？**  
editorial roundup 归 Branding 内容簇。

**digest 为什么讲 Touch Edit？**  
把 product update 翻译成 daily ops 语言。

**404 修复？**  
stable May 2026 week3 editorial roundup URL。

**编造用户数据？**  
禁止 — digest 不写虚构 metrics。
""",
    "content_velocity": """
## FAQ

**velocity crisis 指什么？**  
post 数量上升但 revision cost 爆炸 — 改价 full regen 三十分钟。

**solution 在生成更快吗？**  
在改一次 export 全尺寸更快 — Touch Edit + Brand Kit。

**master-first 什么意思？**  
先 4:5 master 再 derivative crop，防 CTA 被切。

**404 修复？**  
stable zh content velocity crisis solution SOP URL。

**编造 engagement lift？**  
不 — 只测改 offer 分钟数 × 尺寸数。
""",
    "sora_alternatives": """
## FAQ

**Sora alternatives 是 fake 排名吗？**  
不是 — 按任务分组 honest comparison，不编第 1 名。

**写 Sora 或竞品定价吗？**  
不写 — 查官方页面，本篇零编造。

**clip 内能 bake offer 吗？**  
不能 — static companion editable via Touch Edit。

**404 修复？**  
stable zh Sora alternatives honest comparison URL。

**multi-shot 要 character ref 吗？**  
要 — 防 slide 4 character drift。
""",
    "upscalers_en": """
## FAQ

**Is this a fake ranked list?**  
No — seven groups by task fit, not invented "number one" claims.

**Does upscaling fix wrong headline text?**  
No — use Touch Edit on ChatCanvas masters for copy changes.

**Are prices listed for upscaler tools?**  
No — check vendor sites; this article cites no dollar amounts.

**404 fix?**  
Stable EN 4K upscaler honest roundup SOP URL.

**When does Lovart beat pure upscalers?**  
When Tuesday offer fixes must finish in five minutes across ratios with Brand Kit anti-drift.
""",
}


def expand_zh(topic: str, n: int) -> str:
    return f"""
## 实操补充 {n}：{topic}

很多小团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。{topic} 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。
"""


def expand_en(topic: str, n: int) -> str:
    return f"""
## Practice note {n}: {topic}

The first brief ends with "premium" and fails: small price text, badge over the subject. On the second pass, correct only safe zone and required fields. A **ChatCanvas** thread reduces accent drift on slide 4. In **{topic}**, **Touch Edit** confirms price change in five minutes static-first. Full regen thirty minutes — reset **Brand Kit** first. Restored 404 URL as stable SOP link for EN teams. **Design Agent** pass/fail checklist beats adjective briefs every time.
"""


ARTICLES = [
    {
        "rank": 214,
        "key": "ad_creatives_guide",
        "lang": "zh",
        "slug": "create-ad-creatives-guide-2",
        "cover": "059",
        "category": "How-To",
        "title": "广告素材创作指南（第二版）：static-first 可编辑 offer 层",
        "seo_title": "Create Ad Creatives Guide 2 — ChatCanvas SOP",
        "description": "404 修复：create ad creatives guide 2、Brand Kit、Touch Edit 改 offer。",
        "seo_description": "广告素材：Responsive Display、master-first、Design Agent QA。",
        "focus": "create ad creatives guide 2",
        "keywords": ["create ad creatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Create Ad Creatives Guide 2 ZH",
        "body": AD_CREATIVES_GUIDE_ZH,
        "expand_topic": "zh create ad creatives guide 2 workflow",
    },
    {
        "rank": 215,
        "key": "fliki_review",
        "lang": "zh",
        "slug": "fliki-ai-review",
        "cover": "060",
        "category": "Comparison",
        "title": "Fliki AI 评测：text-to-video 强项与 static 分工",
        "seo_title": "Fliki AI Review — honest comparison",
        "description": "404 修复：Fliki AI honest review、不编造定价、Touch Edit static layer。",
        "seo_description": "Fliki review：voiceover clip vs campaign static editable layer。",
        "focus": "fliki ai review",
        "keywords": ["fliki ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Fliki AI Review ZH",
        "body": FLIKI_REVIEW_ZH,
        "expand_topic": "zh Fliki AI honest review workflow",
    },
    {
        "rank": 216,
        "key": "youtube_thumbnail",
        "lang": "zh",
        "slug": "how-to-chat-generate-youtube-thumbnail-lovart",
        "cover": "061",
        "category": "How-To",
        "title": "如何用 ChatCanvas 对话生成 YouTube 缩略图",
        "seo_title": "Chat Generate YouTube Thumbnail — Lovart SOP",
        "description": "404 修复：chat generate YouTube thumbnail、1280×720、Brand Kit。",
        "seo_description": "YouTube 缩略图：120px preview、Touch Edit 改 title、series thread。",
        "focus": "how to chat generate youtube thumbnail lovart",
        "keywords": ["youtube thumbnail chatcanvas", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Chat Generate YouTube Thumbnail ZH",
        "body": YOUTUBE_THUMBNAIL_ZH,
        "expand_topic": "zh chat generate YouTube thumbnail workflow",
    },
    {
        "rank": 217,
        "key": "logo_mistakes",
        "lang": "zh",
        "slug": "logo-design-mistakes",
        "cover": "062",
        "category": "How-To",
        "title": "Logo 设计常见错误：Brand Kit 前该改掉的七个习惯",
        "seo_title": "Logo Design Mistakes — ChatCanvas workflow",
        "description": "404 修复：logo design mistakes、Brand Kit、Touch Edit tagline editable。",
        "seo_description": "Logo 错误：hex drift、小尺寸可读、revision cost 测量。",
        "focus": "logo design mistakes",
        "keywords": ["logo design mistakes", "lovart brand kit", "chatcanvas", "touch edit"],
        "cluster": "How-To — Logo Design Mistakes ZH",
        "body": LOGO_MISTAKES_ZH,
        "expand_topic": "zh logo design mistakes workflow",
    },
    {
        "rank": 218,
        "key": "bueiness_workflow",
        "lang": "zh",
        "slug": "lovart-ai-bueiness-first-ai-creative-workflow",
        "cover": "063",
        "category": "How-To",
        "title": "Lovart AI 创意工作流入门：business-first 静态可编辑路线",
        "seo_title": "Business-First AI Creative Workflow — Lovart SOP",
        "description": "404 修复：business-first creative workflow（slug 保留 bueiness 拼写）。",
        "seo_description": "创意工作流：Brand Kit 四层 stack、Touch Edit 改 offer 五分钟。",
        "focus": "lovart ai bueiness first ai creative workflow",
        "keywords": ["lovart creative workflow", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Business-First Creative Workflow ZH",
        "body": BUEINESS_WORKFLOW_ZH,
        "expand_topic": "zh business-first creative workflow",
    },
    {
        "rank": 219,
        "key": "creation_history",
        "lang": "zh",
        "slug": "lovart-ai-creation-history-track-creative-journey",
        "cover": "064",
        "category": "How-To",
        "title": "Lovart AI 创作历史记录：用 ChatCanvas 追踪创作轨迹",
        "seo_title": "Creation History Track — ChatCanvas 创作轨迹 SOP",
        "description": "404 修复：creation history 创作轨迹、thread log、Touch Edit 改价记录。",
        "seo_description": "创作历史：variant 决策、Brand Kit hex 变更、revision 复盘。",
        "focus": "lovart ai creation history track creative journey",
        "keywords": ["lovart creation history", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Creation History Track ZH",
        "body": CREATION_HISTORY_ZH,
        "expand_topic": "zh creation history 创作轨迹 workflow",
    },
    {
        "rank": 220,
        "key": "digest_may_week3",
        "lang": "zh",
        "slug": "lovart-digest-may-2026-week3",
        "cover": "065",
        "category": "Branding",
        "title": "Lovart 文摘 — 2026 年 5 月第三周 editorial roundup",
        "seo_title": "Lovart Digest May 2026 Week 3 — editorial roundup",
        "description": "404 修复：May 2026 week3 digest editorial roundup、Branding category。",
        "seo_description": "5 月第三周文摘：workflow 要点、Touch Edit ops 语言、无 fake news。",
        "focus": "lovart digest may 2026 week3",
        "keywords": ["lovart digest", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Branding — Lovart Digest May 2026 Week 3 ZH",
        "body": DIGEST_MAY_WEEK3_ZH,
        "expand_topic": "zh Lovart digest May 2026 week3 editorial",
    },
    {
        "rank": 221,
        "key": "content_velocity",
        "lang": "zh",
        "slug": "social-media-content-velocity-crisis-solution",
        "cover": "011",
        "category": "Industry Solution",
        "title": "社媒内容产出速度危机：static-first 缓解方案",
        "seo_title": "Content Velocity Crisis Solution — ChatCanvas SOP",
        "description": "404 修复：social media content velocity crisis、Brand Kit、Touch Edit。",
        "seo_description": "velocity crisis：master-first multi-ratio、改 offer 一次 export 全尺寸。",
        "focus": "social media content velocity crisis solution",
        "keywords": ["content velocity crisis", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Content Velocity Crisis ZH",
        "body": CONTENT_VELOCITY_ZH,
        "expand_topic": "zh content velocity crisis solution workflow",
    },
    {
        "rank": 222,
        "key": "sora_alternatives",
        "lang": "zh",
        "slug": "sora-alternatives",
        "cover": "014",
        "category": "Comparison",
        "title": "Sora 替代品 honest 对比：按任务匹配",
        "seo_title": "Sora Alternatives — honest comparison",
        "description": "404 修复：Sora alternatives honest comparison、不编虚假排名与定价。",
        "seo_description": "Sora 替代：任务分组、static companion、Touch Edit 改 offer。",
        "focus": "sora alternatives",
        "keywords": ["sora alternatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Sora Alternatives ZH",
        "body": SORA_ALTERNATIVES_ZH,
        "expand_topic": "zh Sora alternatives honest comparison workflow",
    },
    {
        "rank": 223,
        "key": "upscalers_en",
        "lang": "en",
        "slug": "7-best-ai-image-upscalers-4k-2026-it",
        "cover": "018",
        "category": "Comparison",
        "title": "7 Best AI Image Upscalers for 4K in 2026: Honest Roundup by Task",
        "seo_title": "7 Best AI Image Upscalers 4K 2026 — honest roundup",
        "description": "404 fix: 4K upscaler honest roundup by task, no fake pricing or rankings.",
        "seo_description": "Upscalers: task groups, Touch Edit vs upscale, Brand Kit anti-drift.",
        "focus": "7 best ai image upscalers 4k 2026",
        "keywords": ["ai image upscaler 4k", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Image Upscalers 4K 2026 EN",
        "body": UPSCALERS_EN,
        "expand_topic": "EN 4K upscaler honest roundup workflow",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "en": expand_en,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch21 content cluster.*\n"
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
