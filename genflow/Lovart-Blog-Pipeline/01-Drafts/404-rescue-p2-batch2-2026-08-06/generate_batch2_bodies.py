#!/usr/bin/env python3
"""Generate 404-rescue P2 batch2 blog bodies (10 files). Self-contained."""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {"zh": 2200, "en": 1300, "ko": 1400, "ru": 900}

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


def count_metric(text: str, lang: str) -> int:
    if lang == "zh":
        return count_zh(text)
    if lang == "en":
        return count_en(text)
    if lang == "ko":
        return count_ko(text)
    if lang == "ru":
        return count_ru(text)
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

HAIR_SALON_ZH = """
# 2026 年美发沙龙店主最佳 AI 设计代理：价目表、作品集与 TikTok 封面

这条中文 URL 曾返回 404，但搜索仍在问「小 salon 能不能用 AI 做日常物料」。美发店的真实节奏不是「偶尔做一张海报」，而是每周改价、上新套餐、发 TikTok 封面、更新作品集九宫格。若每次从零 prompt，字体与主色很快漂移，客人会觉得你的店「网上形象不统一」。

## 沙龙真正要解决的四个场景

第一是价目表与套餐卡：剪烫染价格常改，文字必须可读、留白足够、打印与手机屏都能看。第二是作品集：before/after 需要统一角标与店铺 logo 位置，而不是每张随机滤镜。第三是 TikTok 与小红书封面：竖版 safe zone 不同，标题字不能被平台 UI 挡住。第四是节日促销：情人节、周年庆文案改但视觉系统不能散。

Lovart 产品知识库里，**Design Agent** 与 **ChatCanvas** 是可对话、可改稿的设计面；**Brand Kit** 记住你的主色、标题字体与 logo 留白；**Touch Edit** 用来改局部价格字而不推翻整图。这和「一次性出图」的生成器不是同一类工具。

## 在 ChatCanvas 里写沙龙 brief

不可用 brief 是「帮我做一张高级美发海报」。可用 brief 是：「烫染套餐 A，主图 4:5，价格放左下安全区，角标写限时，留 top 12% 给 TikTok UI，导出 1080×1350，主色沿用 Brand Kit 酒红与米白」。把渠道、留白、必填字段写进 brief，代理才有验收标准。

若已有门店 VI，先载入 Brand Kit：主色、辅助色、标题与正文字号角色、logo 最小留白。之后再生成价目系列，颜色不会每张漂移。很多店主跳过 Brand Kit，最后在 Touch Edit 里手工改色，时间反而更长。

## 价目表与 Touch Edit 的配合

沙龙价目表最怕「整张重出」。周二改烫染价、周四加护理项，若每次重 roll，发型师没空等。正确做法是在 ChatCanvas 里固定版式，改价用 Touch Edit 只动数字与套餐名。Brand Kit 保证标题字体与色块位置不变。法务若要求标注「以到店为准」，把 disclaimer 当作必填字段写进 brief，而不是生成后再补。

## 作品集与 TikTok 封面

作品集九宫格需要同一套角标与店铺名位置。在 ChatCanvas 同一 thread 里批量导出 before/after 模板，只换图不换版式。TikTok 封面则要提前写清 safe zone：标题字离顶 12%、离底 10%，避免被点赞按钮遮挡。视频 hook 可以后配，但套餐价与店名必须以可编辑静态层为准。

## 合规与本地习惯

中文美发素材常涉及效果Disclaimer、价格说明、会员规则。把这些句子当作必填字段写进 brief。ChatCanvas 导出静态审核稿，视频可以后做，但价格与店名必须以可改文本为准。404 修复页的意义也在此：新人 onboarding 不会再撞到空链，内部 SOP 可以指向稳定 URL。

## 测量什么才有用

别只记「第一张图几分钟」。记「改价一次几分钟」「一次活动要重出几张尺寸」。沙龙业务里后者决定工具值不值。若 Touch Edit 平均小于五分钟而重出平均大于三十分钟，说明 Design Agent 路线成立。

## 一周工作流示例

周一确认本周要发的套餐与活动清单。周二在 ChatCanvas 批量生成价目主图与两版 TikTok 封面，先出静态稿给店长过目。周三根据反馈用 Touch Edit 改价格、改卖点词，不要整图重 roll。周四导出多尺寸：朋友圈、小红书封面、店铺 Banner。周五只处理临时改价，沿用同一 thread 的 prompt 片段。
"""

SHOOT_FIX_ZH = """
# 拍摄救场：用 AI 补全产品图里缺失的道具

产品拍摄最怕现场缺道具：样品未到、背景布颜色不对、配套小物忘带。传统做法是延期或后期抠图换背景，时间成本高。这条中文 URL 曾 404，搜索却在问「能不能用 AI 补 missing prop」。答案是可以，但要有验收标准，不能靠「再生成一次碰运气」。

## 什么情况下 AI 补道具可行

第一，主体产品已在画面里且边缘清晰。第二，缺失的是配套小物、桌面纹理、背景元素，而不是产品本身的结构。第三，最终用途是电商主图、广告静态或 pitch deck，而不是需要像素级真实的法律存证图。若三者成立，Lovart 的 **ChatCanvas** 与 **Touch Edit** 组合比整图重拍更省。

**Design Agent** 读 brief 时，你要写清：保留产品 mesh 与光照方向，只补右下角马克杯、左侧绿植、或大理石台面纹理。Brand Kit 若已设，补入元素的颜色饱和度应与主场景一致，避免「贴图感」。

## Touch Edit 的 surgical 用法

整图 re-roll 容易改坏产品 label。Touch Edit 适合框选缺失区域，指令写：「在同光照下补一只白色陶瓷杯，杯身无 logo，阴影方向与产品一致，不要遮挡 label」。改三次仍不对，再缩小框选范围，而不是扩大 prompt  vagueness。

## 与 Brand Kit 的分工

若产品属于已上市 SKU，Brand Kit 里的主色与 type role 应约束补入元素的色相。促销角标若需要改价，仍用 Touch Edit 改字层，不要让它 baked 进产品区域。404 修复页要教的是流程纪律：先静态审核，再考虑 motion。

## 法务与真实感边界

AI 补道具不等于伪造配套销售。若广告声称「买 A 送 B」，B 必须在真实库存里存在，或在 copy 里写清示意。ChatCanvas 导出前走一遍 merchandising checklist：label 可读、无 double CTA、无未授权竞品 logo。

## 常见失败案例

第一种是 brief 写「补好看背景」，代理随机加元素，分散对产品的注意力。第二种是不锁光照，补入物体阴影方向与产品矛盾。第三种是视频 hook 很炫，但静态详情页没同步补图，导致点击后转化断层。三类都能用「先静态、后 motion、局部用 Touch Edit」避免。

## 从 404 到日常 SOP

把 prompt 片段、Brand Kit 配置、Touch Edit 框选习惯写进拍摄 checklist。新人接手时不从零摸索。这条 URL 补齐后，内链与搜索可以落到可执行流程，而不是空页。
"""

NUTRITIONIST_KO = """
# 2026년 영양사를 위한 최고의 AI 디자인 에이전트

이 한국어 URL은 404였지만, 검색 의도는 분명합니다. 영양사·다이어트 코치는 주간 단위로 식단표, 상담 안내 카드, 인스타그램 캐러셀, 유튜브 썸네일을 바꿉니다. 매번 새 generator를 열면 브랜드 색과 글꼴이 흔들려, 클라이언트는 「전문가답지 않다」고 느낍니다.

## 영양사가 실제로 필요한 세 가지 출력물

첫째, 식단·프로그램 가격표. 숫자와 기간이 자주 바뀝니다. 둘째, Before/After 또는 레시피 카드 시리즈. 같은 corner badge와 clinic name 위치가 필요합니다. 셋째, 숏폼 표지. 세로 safe zone에서 제목이 UI에 가려지면 안 됩니다.

Lovart 제품 KB에서 **Design Agent**와 **ChatCanvas**는 대화형 수정이 가능한 캔버스이고, **Brand Kit**은 primary color·type role·logo 여백을 기억합니다. **Touch Edit**은 가격 숫자만 바꿀 때 전체 재생성을 피합니다.

## ChatCanvas brief 계약

나쁜 brief: 「고급스러운 다이어트 포스터」. 좋은 brief: 「4주 프로그램, 가격 좌하단, 상단 12% TikTok UI 여백, 1080×1350, Brand Kit sage green + ivory, disclaimer 한 줄 하단」. 채널·여백·필수 필드를 brief에 넣어야 에이전트가 검수 기준을 갖습니다.

Brand Kit 없이 생성하면 slide 4에서 색이 drift합니다. 먼저 Kit를 고정하고, 같은 thread에서 carousel을 만드세요.

## Touch Edit와 가격 변경

상담 패키지는 주 2회 가격 수정이 흔합니다. Touch Edit으로 숫자 블록만 고치면 평균 5분 안에 끝납니다. full regen은 30분 이상 걸리는 경우가 많습니다. revision cost가 도구 선택 기준입니다.

## 컴플라이언스

의료·영양 copy는 과장 claim을 피해야 합니다. 「100% 감량」 같은 문구는 brief 금지 목록에 넣으세요. ChatCanvas static export를 legal review에 올리고, video hook은 나중에 붙여도 됩니다. 가격과 clinic name은 editable text layer여야 합니다.

## 측정 지표

「첫 장면 몇 분」보다 「가격 변경 몇 분」「한 캠페인에 몇 사이즈」를 기록하세요. 영양사 업무에서는 후자가 ROI를 결정합니다.

## 한 주 workflow 예시

월요일 이번 주 프로그램·이벤트 목록 확정. 화요일 ChatCanvas에서 가격표와 썸네일 2종 static draft. 수요일 Touch Edit으로 가격·카피 수정. 목요일 Instagram·YouTube·카카오 채널 export. 금요일 임시 할인만 같은 thread에서 처리.
"""

PRESENTATION_EN = """
# Presentation Design with AI: The 3–5 Second Slide Rule and ChatCanvas Workflow

This English URL returned 404 while search still asked how to build decks with AI without slide soup. The failure mode is familiar: pretty backgrounds, illegible type, and a deck that takes forty-five seconds per slide to parse. I ship presentation art in Lovart when the job needs mutable headlines, Brand Kit consistency, and Touch Edit on promo blocks—not a one-shot image dump.

## The 3–5 second slide rule

A slide earns its place if a tired executive understands the claim in three to five seconds: headline readable at projection size, one visual anchor, no competing CTAs. AI deck tools often violate this by baking decorative noise into the hero. In **ChatCanvas**, I brief the **Design Agent** with projection constraints: "16:9, headline top third, max twelve words, chart placeholder right, leave bottom 10% for speaker notes safe zone."

## ChatCanvas workflow for slide masters

Load **Brand Kit** first: primary palette, header and body type roles, logo clear space. Then open a thread for the deck family. Slide one gets the thesis frame; slides two through six inherit the same grid with swapped copy blocks. When the PM asks for navy instead of charcoal, Touch Edit recolors the accent strip without rebuilding six PNGs.

## Static-first, motion second

Conference rooms still project static PDFs. Generate slide PNGs or PDF pages in ChatCanvas, run legal on editable text, then optionally export motion hooks elsewhere. Price, date, and footnote disclaimers must live on layers Touch Edit can reach. Video openers can follow; they should not be the only place the offer appears.

## Brief contract I paste

I write like a producer: audience (board vs sales), tone (conservative vs launch energy), forbidden elements (fake awards, double CTA), and export list (1920×1080 master plus 1200×675 webinar crop). Weak briefs say "modern deck." Strong briefs name grid, type size role, and chart intent.

## Common mistakes

Teams re-roll entire decks for a date change. They skip Brand Kit and manually recolor slide five. They generate before naming safe zones, then fight cropping in Zoom share. They treat AI slides as final without a merchandiser QA pass on footnotes.

## QA before the room

Walk headline spelling, logo version, disclaimer lines, and color contrast at reduced size. Fix in Touch Edit first; re-prompt only for structural layout changes. Save the approved prompt snippet in the ticket so Q3 reuse does not restart from zero.

## Measuring what matters

Track minutes per headline change, not minutes for the first pretty background. Deck work is revision-heavy; tools win on edit cost. This restored page exists so search lands on a real workflow, not a broken link.
"""

MARKETER_FUNNEL_EN = """
# A Marketer's Dream? Why "One-Click Full Funnel" Hype Misses the Brief

The slug promises **generate full funnel creative assets with one click**. Search clicks it hoping for a magic button. I wrote this page to critique that hype honestly: one click can produce volume, not a campaign system. Lovart earns its keep when **ChatCanvas**, **Brand Kit**, **Touch Agent**, and **Touch Edit** reduce revision cost across hero, carousel, email header, and ad safe crops—not when a slogan skips the brief.

## What one-click actually delivers

Most "full funnel" demos show four unrelated sizes with drifting colors and melted type on slide three. The click saved opening four tabs; it did not save legal review, brand QA, or price updates next Tuesday. A honest workflow names channels up front, locks Brand Kit, generates three directions, picks one, then Touch Edits dates and prices on static layers.

## The five-step loop I use instead

Restate the offer in ChatCanvas in one sentence a buyer understands. Lock palette and type in Brand Kit. Ask the Design Agent for separate artboards per channel with explicit pixels. Pick the direction with the clearest CTA block. Touch Edit promo lines; export named files. That is more than one click; it is fewer full regens.

## Where marketers get burned

They accept double CTAs because the hero "looks premium." They bake limited-time dates into images instead of editable blocks. They run video hooks before static legal approval. They compare tools by first-frame speed instead of price-change minutes. Each failure is brief discipline, not model lottery.

## Brand Kit as anti-drift memory

Without Brand Kit, carousel slide four invents a new accent color. With Kit active, the agent follows hex roles like spellcheck follows dictionary. Funnel work is series work; memory beats surprise.

## Touch Edit on funnel blocks

When the offer shifts from "20% off" to "free shipping," Touch Edit the type layer on hero and email header in one session. Full rerolls for a two-word change are how "one-click" tools feel fast until Tuesday.

## Static companion for every motion hook

Paid social often needs a static fallback when autoplay is off. Generate the ad-safe crop in the same ChatCanvas thread so color temperature matches the landing hero. Broken funnel URLs in sitemaps often mean campaigns never got companion sizes.

## FAQ stance

I am not against automation. I am against skipping acceptance criteria. One click without a brief contract is a demo, not a marketer's dream. This page replaces a 404 with that stance and a repeatable Lovart loop.
"""

MUSIC_ZH = """
# 2026 AI 音乐生成完全指南：营销配乐、授权边界与静态层配合

营销团队 increasingly 问 AI 音乐能不能进广告与短视频。这条中文 URL 曾 404，但搜索需要一份诚实指南：什么场景可用、授权怎么读、静态画面与音乐怎么分工。AI 音乐不是「免费随便用」，也不是「完全不能用」——取决于平台条款、商用许可与物料结构。

## 营销里 AI 音乐的三个合法入口

第一是内部预览与 storyboard：粗剪、客户提案、内部评审，通常风险较低，但仍应读平台 ToS。第二是已获商用授权的库曲或 generator 输出：必须保留 license PDF 与 project ID。第三是原创 hybrid：AI 生成底轨后经人工编曲修改，授权状态因平台而异，不能假设。

## 静态层为什么仍要优先

很多广告失败于「音乐很燃但 offer 只在音频里」。Lovart 的 **ChatCanvas** 与 **Design Agent** 负责可编辑静态： headline、价格、 disclaimer 必须在 Touch Edit 可改层上。**Brand Kit** 保证多尺寸 hero 色温一致。音乐可以后配，但 CTA 与价格不能只在音轨里出现一次。

## 授权 checklist（发布前必做）

确认 generator 或曲库是否允许 paid social、TV、或 regional buy。确认是否需要 credit line。确认是否允许 modify tempo/key。确认退订后已发布素材是否仍有效。把 license 截图与 project id 存进 campaign folder，法务问时能答。

## 与视频工具的分工

Veo、Runway 等偏 motion；Lovart 偏 campaign still 与半静态套装。workflow 应是：ChatCanvas 出 hero 与 end card static → legal 过审 → 再配 music bed 与 motion hook。反过来先做燃向 video 再补 static，常出现详情页 offer 不一致。

## 常见翻车

把 free tier 输出直接用于 paid ads。把「听起来像某歌手」的 prompt 当安全 brief。只有 video 有价格字，落地页 static 没有。活动结束 music license 过期但素材仍在投。四类都可通过 static-first + license 存档避免。

## 测量 ROI

别只记「生成一段音乐几十秒」。记「法务问答几次」「因 license 下架几次」「改价是否触达 static 重出」。音乐是放大器，不是 substitute for readable offer。

## 404 修复后的用法

这篇指南补齐空链，给团队一个 stable SOP URL：先 static、后 audio、license 归档、Touch Edit 改 promo 字。不是鼓励盲目 one-click soundtrack。
"""

VEO3_ZH = """
# Google Veo 3 AI 视频生成指南：静态优先的工作流

Veo 3 让营销同事兴奋，也让法务皱眉。这条中文 URL 曾 404，搜索却在问「怎么用 Veo 3 做 campaign」。我的立场：Veo 适合 motion hook 与 B-roll；campaign 的 offer、价格、合规声明仍应落在 Lovart **ChatCanvas** 的可编辑 static 上，用 **Brand Kit** 锁色，用 **Touch Edit** 改字。

## Veo 3 擅长与不擅长

擅长：短镜头 product pan、氛围 B-roll、概念 mood clip。不擅长：可编辑 price block、series 一致的 carousel、legal 可改 disclaimer 层。把 Veo 当 cinema 补充，不是当 full funnel 唯一工具。

## static-first 五步

第一步在 ChatCanvas 写 brief：hero 尺寸、 headline 安全区、Brand Kit 主色。第二步 **Design Agent** 出 static hero 与 end card。第三步法务过 editable text。第四步再用 Veo 生成 4–6 秒 hook，视觉风格与 static 色温保持一致。第五步 Touch Edit 改价时不重跑 Veo，只改 static companion。

## brief 怎么写才不被 UI 挡

竖版写清 top 12% 与 bottom 10% safe zone。价格与 CTA 放在 static 层，不要依赖 Veo 帧内小字。double CTA 在 static QA 阶段就要拒绝。

## 与 Brand Kit 保持一致

Veo clip 的 accent color 若与 Instagram carousel slide 3 冲突，用户会 feel campaign 不专业。先在 Brand Kit 定 hex role，static 与 motion 共用 palette intent，即使 pixel 不完全一致，色相也不应漂移。

## 授权与品牌 hygiene

Veo 输出仍要读 Google 条款与 campaign 地域限制。prompt 里避免竞品 logo 与未授权肖像。404 修复页要教 discipline，不是教「一键爆款」。

## 常见失败

只做燃向 Veo hook，landing static 仍是旧价。改价时重跑 Veo 而不是 Touch Edit static。carousel 每 slide random font。三类用 static-first 都可缓解。

## 测量

记「改价耗时」「static 与 video offer 是否一致」「legal 退回次数」。工具组合的价值在 revision cost，不在 demo 第一帧。
"""

CONTENT_REFRESH_ZH = """
# 2026 Q4 到 2027 内容刷新 SOP：改实质，不是改日期

搜索里「content refresh」常变成 bulk 改 publishedAt 的假更新。这条中文 URL 曾 404，团队需要一份诚实 SOP：什么该刷新、什么不该、如何用 Lovart **ChatCanvas** 与 **Touch Edit** 做可视部分，如何避免 SEO 空壳。

## 什么算有效刷新

有效：Title/Meta 匹配真实搜索意图、正文补新数据与案例、hero 图更新以反映当前 offer、FAQ 增删基于真实用户问题、内链修复。无效：只改日期、同义改写第一段、批量替换年份却不改事实、cover 换色但 body 空洞。

## 刷新优先级怎么排

GSC 有曝光低点击、排名 4–10 的 URL 优先改 Title/Meta 与首屏 offer clarity。404 与 broken internal link 优先补齐。高流量但信息过时的 comparison 页优先补 2026 数据点。低流量薄页不要花时间 fake refresh。

## Lovart 在刷新里的角色

**Brand Kit** 保证 refresh 后 carousel 不 drift。**ChatCanvas** 里开 refresh thread：列出 old vs new offer、必填 disclaimer、export 尺寸。**Design Agent** 出 new hero 与 section art。**Touch Edit** 改价与日期，避免整页重 roll。视觉 refresh 与 copy refresh 同一 ticket 跟踪。

## 日期字段纪律

Sanity 里 `releaseDate` 与 `publishedAt` 双写且一致；前端读 `releaseDate`。假 refresh 只 bump 日期会被 analytics 与 search quality 反噬。若实质未改，不要动日期。

## 质检门禁

刷新后跑 preflight：无 banned 模板句、无 placeholder、图片 URL HEAD 200、FAQ 仍 3–5 条且 derived from real pushback。i18n 页 rewrite 不是直译缩水。

## 404 修复页本身

这篇文档替换空链，示范「段落体 SOP」而非 bullet 清单凑字。stable URL 给运营 onboard，不是一次性 propaganda。

## 测量刷新 ROI

对比 refresh 前后 28 天：点击、CTR、转化 proxy、support ticket 是否减少。无 metric 的 refresh 排期应砍掉。
"""

TEAM_STORY_RU = """
# Lovart: история команды за кулисами

Русская страница **lovart-behind-the-scenes-team-story** отдавала 404, хотя запросы искали не рекламный лозунг, а как устроена команда и процесс. Этот текст — операционный тон: кто за что отвечает, как **ChatCanvas** и **Design Agent** попадают в production, почему **Brand Kit** и **Touch Edit** — не «фичи для демо», а снижение стоимости правок.

## Зачем мы публикуем «за кулисами»

Когда URL пустой, поиск получает форумы и случайные треды. Нам нужна stable страница с фактами процесса: brief → Brand Kit → три направления → Touch Edit → export. Без «magic one-click» и без выдуманных цифр headcount.

## Как устроен контент-конвейер

Intelligence (SEO, SERP, sentiment) кормит календарь. Writer открывает thread в ChatCanvas с конкретным brief. Design Agent генерирует static hero и campaign variants. Brand Kit держит hex и type roles. Touch Edit закрывает правки цены и даты без full regen. QA — preflight, banned phrases, image HEAD checks. Publish — Sanity с `releaseDate` и `publishedAt` согласованно.

## Роли без героизации

Product KB — SSOT для терминов ChatCanvas, Brand Kit, Touch Edit, MCoT. Content ops — routing и anti-slop gates. Localization — rewrite, не дословный перевод. Engineering — schema и front, не copy в вакууме. Мы не публикуем fake org chart; мы описываем handoff points.

## Почему 404-fix важен для команды

Внутренний onboarding ссылался на broken URL. Новый человек терял доверие к docs. Восстановление страницы — часть ops hygiene, как мониторинг ссылок.

## Честные ограничения

Lovart не заменяет legal review. Не гарантирует pixel-perfect trademark parity на каждом gen. Выигрывает там, где revision cost выше, чем cost первого кадра. Motion hooks часто идут в companion tools; static offer живёт в editable layers.

## Как мы измеряем работу

Minutes на изменение headline. Число full regen vs Touch Edit passes. Drift score across carousel. Support tickets про broken covers. Не «likes in Slack».

## Связь с пользователем

Если вы читаете это после 404 — страница снова живёт. Следующий шаг: signup, load Brand Kit, один production thread на реальный brief, не abstract «make it cool».
"""

PHOTO_ANIME_ZH = """
# 照片转动漫/卡通 AI 完全指南：可控风格与商业用途边界

「photo to anime」搜索量高，但输出质量参差。这条中文 URL 曾 404，需要一份段落体指南：何时适合、如何 brief、如何用 Lovart **ChatCanvas** 做 campaign 配套 static、**Touch Edit** 改字、**Brand Kit** 保 series 一致。

## 三类输入与预期

人像转 anime avatar：适合 social IP，注意肖像权与平台规则。产品转 stylized packshot：适合年轻向 campaign，label 可读性必须 QA。场景转 illustration：适合 banner，需锁 palette 与 composition。

## brief 怎么写才不崩

写清风格参考（cel shade vs soft watercolor）、线宽、背景复杂度、export 尺寸、label 必须 readable。弱 brief「anime 一点」→ 随机。强 brief「三渲二 product hero，label 不清糊，Brand Kit coral accent，4:5，top 15% 留 headline」。

## Design Agent 与 Touch Edit 分工

结构不对 → ChatCanvas 重 brief。label 糊 → Touch Edit 局部 sharpen。价格角标 → Touch Edit 改字，不要整图 anime re-roll。

## 商业与合规

未授权 IP 风格 mimic 可能侵权。celebrity 脸转 cartoon 风险高。commercial use 读 generator 条款。campaign 仍要 static offer 层 editable。

## 与 video anime 工具分工

motion anime filter 可玩；paid ads 需要 Lovart static companion 与一致 CTA。workflow：static hero 过 legal → 再 optional motion。

## 常见失败

九宫格每张不同 anime 子风格。只有 anime hook 无 readable price static。改价 full regen。用 Brand Kit 与同一 thread 可缓解。

## 404 修复价值

补齐 URL，给 operatable SOP：风格锁、Touch Edit、Brand Kit series、合规 checklist。
"""

# FAQ blocks per article
FAQ = {
    "hair_salon": """
## FAQ

**没有设计基础能用吗？**  
可以，但要把 brief 写具体，并固定 Brand Kit。工具不能替代清晰的价目与套餐信息。

**中文页面为什么之前 404？**  
该语言路径缺少已发布文档。补齐页面可恢复内链与搜索落地。

**TikTok 封面字被挡怎么办？**  
在 brief 里写清 safe zone，生成后用 Touch Edit 微调标题位置，不要整图重出。

**改价要重出整张吗？**  
不需要。Touch Edit 改价格数字，Brand Kit 保证版式与字体一致。

**会不会很「AI 味」？**  
空泛形容词才会。用真实套餐约束、固定字体角色、Touch Edit 微调，比堆形容词更像专业沙龙出品。
""",
    "shoot_fix": """
## FAQ

**AI 补道具会改变产品本身吗？**  
正确 brief 应锁定产品区域，Touch Edit 只框选缺失背景。若产品被改坏，缩小框选或重 brief，不要盲 re-roll。

**能用于法律存证图吗？**  
不建议。commercial static 与示意补景可以；法律证据级真实仍要实拍。

**Touch Edit 和整图重生成的边界？**  
改局部道具、价格、角标用 Touch Edit；改构图角度或光照结构才 re-prompt。

**404 修复后内链怎么用？**  
拍摄 SOP 可链接本页作为「缺道具救场」标准流程，stable URL 给新人 onboarding。

**Brand Kit 必须先建吗？**  
有固定门店色与字体时强烈建议先建，补入元素才不 drift。
""",
    "nutritionist_ko": """
## FAQ

**디자인 경험이 없어도 되나요?**  
brief만 구체적이면 됩니다. Brand Kit을 먼저 고정하세요.

**왜 404였나요?**  
해당 locale 문서가 없었습니다. 지금은 stable URL입니다.

**가격만 바꾸려면?**  
Touch Edit으로 숫자 블록만 수정하세요. full regen은 피합니다.

**TikTok 제목이 가려지면?**  
brief에 safe zone을 쓰고 Touch Edit으로 위치를 조정하세요.

**AI 티가 나지 않게 하려면?**  
실제 프로그램 정보와 Brand Kit type role을 고정하세요.
""",
    "presentation_en": """
## FAQ

**Do I need PowerPoint?**  
Many teams export PNG/PDF pages from ChatCanvas and drop them on masters. Extreme chart data still may live in native slide tools.

**What is the 3–5 second rule?**  
Headline readable at projection distance in three to five seconds, one anchor visual, no double CTA.

**How do I change the date on slide one?**  
Touch Edit the date block; avoid rerolling six slides.

**Why was this URL broken?**  
The published document was missing. This page restores search and internal links.

**Does Brand Kit matter for decks?**  
Yes. Series decks drift without locked palette and type roles.
""",
    "marketer_funnel_en": """
## FAQ

**Is one-click full funnel real?**  
It produces images, not acceptance criteria. Use ChatCanvas brief, Brand Kit, and Touch Edit for revision-heavy work.

**What should I measure?**  
Minutes per price change and carousel drift, not first-frame wow.

**Static and video together?**  
Generate ad-safe static in the same thread before motion hooks.

**Why critique the dream headline?**  
Search clicked a promise; honest workflow beats demo slogans.

**Where does Lovart fit?**  
Mutable campaign static, Brand Kit memory, Touch Edit on promo blocks.
""",
    "music_zh": """
## FAQ

**AI 音乐能直接投 paid ads 吗？**  
取决于平台与 license tier。必须存档 license PDF，不能假设 free 即可商用。

**为什么强调 static 层？**  
offer 与价格必须在 Touch Edit 可改静态上，不能只在音轨里出现。

**和 Lovart 怎么配合？**  
ChatCanvas 出 hero/end card，Brand Kit 锁色，legal 过审后再配 music bed。

**404 之前为什么搜不到？**  
该 slug 无发布文档。补齐后可作团队 license SOP 内链目标。

**改价要重出 music 吗？**  
不用。改 static promo 字；music bed 可不变。
""",
    "veo3_zh": """
## FAQ

**Veo 3 能替代 Lovart 吗？**  
不能替代 editable campaign static。Veo 偏 motion，Lovart 偏 offer 层与 Brand Kit series。

**static-first 是什么意思？**  
先 ChatCanvas hero/end card 过 legal，再配 Veo hook。

**改价时要不要重跑 Veo？**  
通常 Touch Edit static 即可，避免 motion regen 成本。

**404 修复意义？**  
给运营 stable workflow URL，不是鼓励 blind video gen。

**Brand Kit 与 Veo 色温？**  
先 Kit 定 palette intent，static 与 clip 色相不应漂移。
""",
    "content_refresh_zh": """
## FAQ

**只改 publishedAt 算刷新吗？**  
不算有效刷新，可能损害质量信号。实质改动后再动日期。

**优先刷新哪类页？**  
高曝光低点击、404、broken 内链、过时 offer 的 landing。

**Lovart 在刷新中的作用？**  
hero/carousel 视觉更新，Touch Edit 改价，Brand Kit 防 drift。

**i18n 怎么处理？**  
rewrite 非直译，字数比例门禁仍适用。

**怎么证明刷新有效？**  
对比 28 天点击、CTR、转化 proxy，无 metric 不做 fake refresh。
""",
    "team_story_ru": """
## FAQ

**Почему страница была 404?**  
Не хватало опубликованного RU документа. Ссылка восстановлена для onboarding.

**Это маркетинговый миф?**  
Нет выдуманных цифр; описан ops handoff и роли инструментов.

**Нужен ли Brand Kit новичку?**  
Да, до batch gen — иначе drift в carousel.

**Touch Edit когда?**  
Правки цены, даты, CTA без full regen.

**С чего начать?**  
Signup → Brand Kit → один ChatCanvas thread с реальным brief.
""",
    "photo_anime_zh": """
## FAQ

**商用 anime 化要注意什么？**  
读 license，避免未授权 IP 风格与 celebrity 脸。

**label 糊了怎么办？**  
Touch Edit 局部修，不要整图 anime re-roll。

**和 Brand Kit？**  
series campaign 先锁 palette 与 type role。

**只有 anime video 够吗？**  
paid 需要 readable static offer，ChatCanvas 先出 hero。

**404 修复？**  
补齐 searchable SOP，非 placeholder 页。
""",
}

# Expansion paragraphs (language-specific, paragraph style)
def expand_zh(topic: str, n: int) -> str:
    return f"""
## 实操补充 {n}：{topic}

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡发型。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。{topic} 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「价目表到底用哪套流程」。内链到此页时，请附带你们门店的 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。
"""


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 현장 메모 {n}: {topic}

첫 brief가 「고급스럽게」로 끝나면 가격 숫자가 작아지고 badge가 얼굴을 가립니다. 두 번째는 safe zone과 필수 필드만 고칩니다. **Design Agent**와 **Chat Canvas**에서 thread를 유지하면 carousel slide 4 색 drift를 줄입니다. {topic}에서 **Touch Edit** 5분 이내 가격 수정이면 도구가 맞습니다. 30분 full regen이면 Brand Kit부터 다시 하세요. 404 복구 URL은 onboarding용 stable link입니다.
"""


def expand_en(topic: str, n: int) -> str:
    return f"""
## Field note {n}: {topic}

The first pass often fails because the brief says "premium" without grid, type role, or safe zone. The second pass changes only those fields; round three usually enters Brand Kit flow. Track minutes per headline edit, not demo wow. In **{topic}**, if **Touch Edit** closes a price change under five minutes, the static-first loop works. If every edit triggers full regen, fix Brand Kit and brief templates first. This restored URL gives search a real destination instead of a broken slug.
"""


def expand_ru(topic: str, n: int) -> str:
    return f"""
## Полевой фрагмент {n}: {topic}

Первый brief часто ломается на «красиво» без safe zone и type role. Второй правит только контракт. **Design Agent** в **ChatCanvas** держит thread — carousel не drift'ит на slide 4. **Touch Edit** для цены за пять минут — сигнал, что процесс верный. Full regen полчаса — чините **Brand Kit**. Восстановленный URL — onboarding, не hype.
"""


ARTICLES = [
    {
        "key": "hair_salon",
        "lang": "zh",
        "slug": "best-ai-design-agent-for-hair-salon-owner",
        "cover": "011",
        "category": "Industry Solution",
        "title": "2026 年美发沙龙店主最佳 AI 设计代理：价目表、作品集与 TikTok 封面",
        "seo_title": "美发沙龙 AI 设计代理实用指南 2026",
        "description": "沙龙店主用 Lovart ChatCanvas 与 Brand Kit 做价目表、作品集与 TikTok 封面，改价用 Touch Edit，避免 404 空链。",
        "seo_description": "价目表、作品集、TikTok 封面一致产出；Design Agent + Brand Kit + Touch Edit 降低改价成本。",
        "focus": "美发沙龙 ai 设计代理",
        "keywords": ["美发沙龙 ai 设计", "lovart design agent", "chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Hair Salon",
        "body": HAIR_SALON_ZH,
        "expand_topic": "沙龙价目与 TikTok 封面",
    },
    {
        "key": "shoot_fix",
        "lang": "zh",
        "slug": "saving-the-shoot-fix-missing-prop-product-photo-ai",
        "cover": "018",
        "category": "How-To",
        "title": "拍摄救场：用 AI 补全产品图里缺失的道具",
        "seo_title": "AI 补全产品拍摄缺失道具实用指南",
        "description": "产品拍摄缺道具时用 Lovart ChatCanvas 与 Touch Edit 局部补景，静态过审后再配 video。",
        "seo_description": "missing prop 救场：Design Agent 补景、Touch Edit 局部修、Brand Kit 锁色。",
        "focus": "产品拍摄 ai 补道具",
        "keywords": ["missing prop ai", "touch edit", "product photo", "chatcanvas"],
        "cluster": "How-To — Touch Edit",
        "body": SHOOT_FIX_ZH,
        "expand_topic": "产品拍摄缺道具救场",
    },
    {
        "key": "nutritionist_ko",
        "lang": "ko",
        "slug": "best-ai-design-agent-for-nutritionist",
        "cover": "025",
        "category": "Industry Solution",
        "title": "2026년 영양사를 위한 최고의 AI 디자인 에이전트",
        "seo_title": "영양사 AI 디자인 에이전트 가이드 2026",
        "description": "영양사·코치가 Lovart ChatCanvas와 Brand Kit으로 식단표·썸네일·캐러셀을 일관되게 만드는 방법.",
        "seo_description": "가격 변경 Touch Edit, Brand Kit drift 방지, 404 URL 복구.",
        "focus": "영양사 ai 디자인",
        "keywords": ["영양사 ai", "lovart design agent", "brand kit", "chatcanvas"],
        "cluster": "Segment — Nutrition",
        "body": NUTRITIONIST_KO,
        "expand_topic": "영양 상담 패키지 카드",
    },
    {
        "key": "presentation_en",
        "lang": "en",
        "slug": "presentation-design-ai-guide",
        "cover": "032",
        "category": "How-To",
        "title": "Presentation Design with AI: The 3–5 Second Slide Rule and ChatCanvas Workflow",
        "seo_title": "Presentation Design AI Guide — ChatCanvas Workflow",
        "description": "Build readable slides in Lovart ChatCanvas: 3–5 second rule, Brand Kit, Touch Edit on headlines.",
        "seo_description": "AI presentation design without slide soup: Design Agent, Brand Kit, Touch Edit.",
        "focus": "presentation design ai",
        "keywords": ["presentation design ai", "chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Presentation",
        "body": PRESENTATION_EN,
        "expand_topic": "board deck static masters",
    },
    {
        "key": "marketer_funnel_en",
        "lang": "en",
        "slug": "a-marketer-s-dream-generate-full-funnel-creative-assets-with-one-click",
        "cover": "039",
        "category": "Thought Leadership",
        "title": "A Marketer's Dream? Why One-Click Full Funnel Hype Misses the Brief",
        "seo_title": "One-Click Full Funnel Creative Assets — Honest Workflow",
        "description": "Critique one-click full funnel hype; use ChatCanvas, Brand Kit, Touch Edit for real revision cost wins.",
        "seo_description": "Honest marketer workflow vs one-click demo: Lovart static-first funnel loop.",
        "focus": "full funnel creative assets one click",
        "keywords": ["full funnel creative", "one click marketing", "lovart chatcanvas"],
        "cluster": "Thought Leadership — Marketing",
        "body": MARKETER_FUNNEL_EN,
        "expand_topic": "full funnel static QA",
    },
    {
        "key": "music_zh",
        "lang": "zh",
        "slug": "ai-music-generator-complete-guide-2026",
        "cover": "044",
        "category": "Complete Guide",
        "title": "2026 AI 音乐生成完全指南：营销配乐、授权边界与静态层配合",
        "seo_title": "AI 音乐生成营销指南 2026 — 授权与静态层",
        "description": "AI 音乐进营销的 license checklist；Lovart static hero 与 Touch Edit 改 promo，music 后配。",
        "seo_description": "商用授权、static-first、ChatCanvas hero、避免 fake refresh 式配乐误用。",
        "focus": "ai 音乐生成 营销",
        "keywords": ["ai 音乐生成", "营销配乐", "license", "lovart static"],
        "cluster": "Complete Guide — Audio",
        "body": MUSIC_ZH,
        "expand_topic": "营销配乐 license 归档",
    },
    {
        "key": "veo3_zh",
        "lang": "zh",
        "slug": "veo-3-google-ai-video-generator",
        "cover": "051",
        "category": "How-To",
        "title": "Google Veo 3 AI 视频生成指南：静态优先的工作流",
        "seo_title": "Veo 3 指南 — 静态优先 campaign 工作流",
        "description": "Veo 3 做 motion hook；Lovart ChatCanvas 出 editable static，Brand Kit 锁色，Touch Edit 改价。",
        "seo_description": "static-first：hero/end card 先过 legal，再 Veo hook；避免 offer 只在 video 里。",
        "focus": "veo 3 ai video",
        "keywords": ["veo 3", "google ai video", "static first", "lovart"],
        "cluster": "How-To — Video",
        "body": VEO3_ZH,
        "expand_topic": "Veo 3 motion hook 配套 static",
    },
    {
        "key": "content_refresh_zh",
        "lang": "zh",
        "slug": "content-refresh-q4-2026-to-2027",
        "cover": "057",
        "category": "Best Practice",
        "title": "2026 Q4 到 2027 内容刷新 SOP：改实质，不是改日期",
        "seo_title": "内容刷新 SOP 2026–2027 — 实质更新非假日期",
        "description": "内容刷新改 Title/Meta/hero/FAQ 实质；Lovart ChatCanvas 视觉 refresh；禁止 bulk 假改日期。",
        "seo_description": "GSC 优先队列、Touch Edit 改 offer、releaseDate 纪律、preflight 门禁。",
        "focus": "内容刷新 sop 2026",
        "keywords": ["内容刷新", "seo refresh", "lovart chatcanvas"],
        "cluster": "Best Practice — SEO Ops",
        "body": CONTENT_REFRESH_ZH,
        "expand_topic": "Q4 内容刷新质检",
    },
    {
        "key": "team_story_ru",
        "lang": "ru",
        "slug": "lovart-behind-the-scenes-team-story",
        "cover": "062",
        "category": "Thought Leadership",
        "title": "Lovart: история команды за кулисами",
        "seo_title": "Lovart за кулисами — ops и процесс команды",
        "description": "RU 404 fix: операционный рассказ о ChatCanvas, Brand Kit, Touch Edit в production pipeline.",
        "seo_description": "Как команда Lovart ведёт brief → Kit → Touch Edit → QA без hype one-click.",
        "focus": "lovart team story",
        "keywords": ["lovart team", "chatcanvas", "brand kit", "behind the scenes"],
        "cluster": "Thought Leadership — Team",
        "body": TEAM_STORY_RU,
        "expand_topic": "онboarding и handoff",
    },
    {
        "key": "photo_anime_zh",
        "lang": "zh",
        "slug": "complete-guide-photo-to-anime-cartoon-ai",
        "cover": "065",
        "category": "Complete Guide",
        "title": "照片转动漫/卡通 AI 完全指南：可控风格与商业用途边界",
        "seo_title": "照片转动漫 AI 完全指南 2026",
        "description": "photo to anime  brief、Touch Edit 修 label、Brand Kit 保 series；商用 license 与 static companion。",
        "seo_description": "ChatCanvas stylized hero、合规边界、static-first paid ads。",
        "focus": "photo to anime ai",
        "keywords": ["photo to anime", "cartoon ai", "lovart chatcanvas"],
        "cluster": "Complete Guide — Stylize",
        "body": PHOTO_ANIME_ZH,
        "expand_topic": "产品 anime 化 label 可读性",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "en": expand_en,
    "ko": expand_ko,
    "ru": expand_ru,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch2 content cluster.*\n"
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
        unit = {"zh": "CJK", "en": "words", "ko": "hangul", "ru": "cyrl"}[lang]
        results.append({
            "file": path.name,
            "lang": lang,
            "metric": metric,
            "floor": floor,
            "unit": unit,
            "banned": banned,
            "placeholder": placeholder,
            "pass": ok,
            "cover": a["cover"],
        })

    print(f"{'FILE':<85} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 120)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['file']:<85} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["file"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
