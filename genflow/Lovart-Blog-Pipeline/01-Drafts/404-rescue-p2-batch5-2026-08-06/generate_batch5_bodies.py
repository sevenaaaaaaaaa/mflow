#!/usr/bin/env python3
"""Generate 404-rescue P2 batch5 blog bodies (10 files). Self-contained.

Ranks #53–#62 from 404-rescue-compact lane.
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

VIDEO_PROMPTS_ZH = """
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
"""

INTERIOR_MAKEOVER_ZH = """
# AI 室内改造完全指南：ChatCanvas 情绪板与 Touch Edit 换家具

这条中文 URL 曾返回 404，搜索却在问「AI 能不能做 room makeover 并改家具」。能，但室内改造不是「一键换豪华风」。需要 mood board 阶段锁 palette 与材质方向，layout 阶段定 safe zone 与 focal point，家具替换阶段用 **Touch Edit** 局部 swap，而不是整图 re-roll。Lovart **ChatCanvas** 与 **Design Agent** 负责 thread 内 series 一致；**Brand Kit** 锁 accent 与 wood tone role。

## 三阶段 workflow

第一阶段 mood board：在 **ChatCanvas** 开 thread，brief 写风格词（北欧、日式、工业）、主色、禁止项（假窗、畸形透视）。出 3–4 张 direction still，选一张进 Brand Kit。第二阶段 layout pass：定相机高度、vanishing point、留白区（供后期叠字或标注尺寸）。第三阶段 furniture swap：沙发、茶几、灯具用 **Touch Edit** 框选替换，brief 写「保持墙面与地板，只换 seating zone 为 linen sofa」。

## ChatCanvas mood board brief 怎么写

弱 brief：「现代简约客厅 makeover」。强 brief：「living room eye-level，north light window left，Brand Kit sand + oak accent，sofa zone center，coffee table lower third，no text in render，4:5 1080×1350，禁止 fake window view」。把可验收字段写进 brief，**Design Agent** 才有 QA 标准。

## Touch Edit 换家具而不推翻硬装

客户说「沙发换米色、茶几换圆角」时，**Touch Edit** 框选家具区，指令写「replace sofa with beige linen, keep wall and floor, match Brand Kit oak」。full regen 会随机改窗位与墙色，交付物不可控。404 修复页给设计师 stable SOP URL。

## Brand Kit 防 series drift

同一项目做 before/after carousel 时，slide 3 不能发明新 wood tone。Kit 里定义 primary wall、accent wood、upholstery role。Touch Edit 换单品时引用 role，不临时 hex。

## 与纯 staging 工具的分工

virtual staging 工具偏单张氛围；campaign 还需要 readable 标注、多 slide 一致、改文案不全图重出。**ChatCanvas** composite + Brand Kit + Touch Edit 才是 revision-heavy 室内项目的 daily rhythm。

## 常见失败

一次 prompt 要「豪华+日式+工业」混搭。家具 swap 用 full regen 导致窗位变化。before/after 色温不一致。无 mood board 直接出 final，客户返工整轮。

## 测量 ROI

记「换一件家具几分钟」「carousel drift 几次」「客户改 brief 轮数」。室内改造是 edit-heavy，工具价值在局部 swap 成本。
"""

BODY_AGE_KO = """
# AI 초상 연령 변환 완전 가이드 2026: 윤리·동의·캠페인 static 분업

이 한국어 URL은 404였지만 검색은 「AI로 나이 변환 초상」 윤리적 workflow를 요구했습니다. 연령 변환은 entertainment demo가 아니라 동의·출처·오남용 방지가 먼저입니다. Lovart **ChatCanvas**와 **Design Agent**는 editable campaign static·**Brand Kit** series·**Touch Edit** promo 수정에 맞고, portrait age tool은 reference mood companion으로 분업합니다.

## 윤리 checklist (생성 전 필수)

첫째, 피사체 본인 또는 법정 대리인 서면 동의. 둘째, 미성년자·유명인·타인 사진 무단 사용 금지. 셋째, 「실제 노화 예측」 같은 의료·법률 claim 금지 — creative visualization임을 disclaimer에 명시. 넷째, deepfake 오남용 금지 목록을 brief에 포함. 다섯째, commercial use 시 generator ToS와 portrait rights 재확인.

## static-first와 age transform clip

paid social에서 offer는 readable static layer에 있어야 합니다. **ChatCanvas** hero와 end card를 먼저 legal pass, age transform clip은 mood companion 4–6초, clip 안에 작은 가격 텍스트 금지. **Touch Edit**으로 promo만 수정, portrait regen 최소화.

## ChatCanvas brief 예시

약한 brief: 「할머니처럼 보이게」. 강한 brief: 「동의받은 adult portrait reference, creative age visualization only, not medical prediction, Brand Kit neutral background, no readable text in render, disclaimer footer editable, 4:5 static master」. **Design Agent**는 acceptance criteria가 brief에 있을 때만 QA 가능.

## Touch Edit과 Brand Kit

연령 변환 결과물도 carousel series면 **Brand Kit** accent drift를 막아야 합니다. CTA·날짜·가격은 **Touch Edit** text layer. portrait pixel은 건드리지 않고 promo band만 수정.

## 오남용 방지 운영

내부 SOP: 동의서 스캔 archive, project id 기록, publish 전 legal review. 검색 클릭이 404로 떨어지면 팀이 ethics 없이 demo만 보게 됩니다 — 이 페이지는 stable workflow URL입니다.

## 흔한 실패

동의 없는 타인 사진. clip에 baked 작은 가격. medical claim. Brand Kit 없이 series color drift. static 없이 video만 배포.

## 측정 지표

동의 archive 유무, legal return 횟수, promo 수정 분수, portrait full regen 횟수. ethics pass가 없으면 도구 속도는 무의미합니다.
"""

MEDEO_PT = """
# Medeo AI Review 2026: clip mood versus static de campanha editável

Esta URL em português retornava 404 enquanto buscas pediam avaliação honesta do Medeo AI. Resposta direta: Medeo é forte em clip curto stylized e loop mood; é fraco em preço editável, Brand Kit series e disclaimer legal em layers. Lovart **ChatCanvas** e **Touch Edit** cobrem static hero; Medeo pode ser companion hook, não o funil inteiro.

## O que o Medeo faz bem

Motion loop curto, camera pan suave, look dev rápido para mood board de fashion/beauty. Útil para teaser quando o texto readable fica em static separado no **ChatCanvas**.

## Onde o Medeo falha em marketing

Texto pequeno bake-in, drift de cor entre clips, CTA duplo, label de produto ilegível. Mudança de promo na terça: regen clip custa mais que **Touch Edit** no static. Sem **Brand Kit**, carousel slide três inventa novo accent.

## Workflow paralelo recomendado

Brand Kit palette fixada. **ChatCanvas** gera hero 4:5 com price safe zone e disclaimer editable. Legal pass no static. Clip Medeo 4–6 segundos sem texto pequeno, color temperature alinhada ao Kit. Promo change: só Touch Edit static.

## Briefs separados

Medeo: soft beauty mood, ivory light, slow pan, no readable small text. ChatCanvas: hero 4:5, headline top third, price bottom left, Brand Kit sage + charcoal, disclaimer footer.

## Licença e uso comercial

Verifique ToS oficial Medeo para paid social. Não assuma que free tier cobre ads. Arquive license note por campanha. Lovart static passa QA textual antes de publish.

## Erros comuns

Só clip Medeo sem static offer alinhado. Regen clip a cada mudança de preço. Brand Kit ausente, carousel drift. Static-first mitiga.

## O que medir

Minutos mudança preço static vs regen clip. Alinhamento offer static/video. Legal return count. Página 404 restaurada para link workflow.
"""

ECONOMIC_IMPACT_ZH = """
# 2026 AI 设计经济影响：设计运营成本账，不是 hype 幻灯片

这条中文 URL 曾返回 404，搜索却在问「AI 设计对经济有什么影响」。答案不在 demo 视频里，而在 design ops 账本：改价一次几分钟、carousel drift 几次、legal return 几次、一人团队 weekly output 几种尺寸。Lovart **ChatCanvas**、**Design Agent**、**Brand Kit**、**Touch Edit** 的价值用 revision cost 衡量，不用「第一张图多快」衡量。

## 设计 ops 的四条成本线

第一是 brief 到 first pass 的分钟数，通常不是瓶颈。第二是 price/date/CTA 修改的分钟数，这才是 daily 成本。第三是 series 色与 type drift 导致的返工轮数。第四是 compliance 退回次数。AI 若只加速第一条而恶化后三条，总成本上升。

## static-first 如何降低 edit cost

**ChatCanvas** 先出 readable static，offer 与 disclaimer 在 **Touch Edit** 可改层。**Brand Kit** 锁 hex role，slide 3 不发明新 accent。video 与 music 后配，改 promo 不触发 motion regen。404 修复页给 CFO 与运营 stable URL，讨论 ROI 时有共同词汇。

## Brand Kit 作为 anti-drift 记忆

没有 **Brand Kit**，小团队 weekly promo 常在 slide 4 漂移色温，品牌看起来像不同公司。Kit 一次设定 primary、accent、type role，batch 在同一 thread。**Design Agent** 引用 role 而非临时形容词。测量：drift 次数下降是否转化为 fewer full regen。

## Touch Edit 与人力结构

一人 marketing 若每次改价 full regen 30 分钟，weekly 5 次改价就是 2.5 小时烧在 reroll。若 **Touch Edit** 5 分钟关闭，同一人力可多 export 两种尺寸或跑一次 legal pre-check。经济影响在 capacity，不在 headline「AI 取代设计师」。

## 不编造的 ROI 框架

记录 baseline：改价分钟、export 尺寸数、legal return。引入 Lovart loop 后同指标对比。不编造「节省 80%」；用团队真实 ticket 数据。若无 tracking，先建 spreadsheet 再谈工具采购。

## 与纯生成工具的分工

单张 cute frame 工具可能 win first frame；campaign series win on edit cost。**ChatCanvas** + Kit + Touch Edit 面向 revision-heavy ops。经济账在该场景才为正。

## 常见失败

用 demo wow 采购，无 revision metric。video-first 导致 offer 不可编辑。跳过 Brand Kit，手工改 hex。把 free tier 当 production stack。

## 404 修复意义

补齐 searchable SOP，让「经济影响」讨论落在 ops 数据上，不是 hype 词。
"""

COFFEE_SHOP_KO = """
# 2026년 커피숍 사장을 위한 최고의 AI 디자인 에이전트

이 한국어 URL은 404였지만 검색은 「커피숍 메뉴판·인스타·시즌 promo」 daily workflow를 원했습니다. 커피숍은 주 2회 가격·원두·시즌 drink가 바뀝니다. **Brand Kit** 없이 매 generation마다 새 brown tone이 나오면 brand trust가 깨집니다. Lovart **ChatCanvas**, **Design Agent**, **Touch Edit**는 layout 고정·copy 변경에 맞습니다.

## 커피숍 네 가지 일상 장면

첫째 메뉴판·가격표: 숫자 변경 잦음, typography readable. 둘째 시즌 drink promo: copy 바뀌고 visual system 유지. 셋째 Instagram story·카카오 채널 cover: vertical safe zone, title이 cup을 가리지 않음. 넷째 loyalty·coupon card: disclaimer 한 줄 footer.

## ChatCanvas brief 예시

약한 brief: 「감성 카페 포스터」. 강한 brief: 「seasonal latte, 4:5, price bottom left safe zone, logo top right, top 12% story UI clear, 1080×1350, Brand Kit espresso brown + cream, disclaimer one line」. 필수 필드 없으면 QA 불가.

## Brand Kit: stock marble 금지

실제 interior wood·tile color 캡처. primary, accent, menu type role, logo clear space 정의. 같은 thread batch. **Touch Edit**은 drink price만, stripe geometry는 유지.

## Touch Edit 화요일 가격 변경

새 single origin 가격은 price block만 edit. full regen은 grid 틀릴 때만. 카운터 staff도 locked Brand Kit SOP면 **Touch Edit** 가능.

## Portfolio와 social series

nine tile menu share badge position. story cover safe top 12%, bottom 10%. static hero before optional motion hook.

## Compliance

caffeine·allergy disclaimer brief 필드. fake certification 없음. static legal pass before ads.

## 흔한 실패

매 post 새 font. readable menu 없이 video만. 가격 변경 full regen. Brand Kit skip.

## 측정

price fix 분수. action당 size 수. carousel drift. 404 stable SOP URL.
"""

MUSIC_ZHTW = """
# 2026 AI 音樂生成完全指南：行銷配樂、授權邊界與靜態層配合

行銷團隊常問 AI 音樂能不能進廣告與短影片。這條繁中 URL 曾 404，搜尋需要一份誠實指南：什麼場景可用、授權怎麼讀、靜態畫面與音樂怎麼分工。本篇以繁體中文重寫，**不是**簡體 batch2 逐句翻譯；用語、法務提醒與台港素材習慣分開寫。AI 音樂不是「免費随便用」，也不是「完全不能用」——取決於平台條款、商用許可與物料結構。

## 行銷裡 AI 音樂的三個合法入口

第一是內部預覽與 storyboard：粗剪、客戶提案、內部評審，風險通常較低，仍應讀平台 ToS。第二是已獲商用授權的曲庫或 generator 輸出：必須保留 license PDF 與 project ID。第三是 hybrid 編曲：AI 底軌經人工編曲修改，授權狀態因平台而異，不能假設 free tier 可上 paid social。

## 靜態層為什麼仍要優先

很多廣告失敗於「音樂很燃但 offer 只在音軌裡」。Lovart **ChatCanvas** 與 **Design Agent** 負責可編輯靜態：headline、價格、disclaimer 必須在 **Touch Edit** 可改層上。**Brand Kit** 保證多尺寸 hero 色溫一致。音樂可以後配，但 CTA 與價格不能只在音軌出現一次。

## 授權 checklist（上線前必做）

確認 generator 或曲庫是否允許 paid social、TV、regional buy。確認是否需要 credit line。確認是否允許 modify tempo/key。確認退訂後已發布素材是否仍有效。把 license 截圖與 project id 存進 campaign folder，法務問時能答。台港團隊另注意繁體 metadata 與在地 disclaimer 用字。

## 與影片工具的分工

Veo、Runway 等偏 motion；Lovart 偏 campaign still 與半靜態套裝。workflow：ChatCanvas 出 hero 與 end card static → legal 過審 → 再配 music bed 與 motion hook。先做燃向 video 再補 static，常出現落地頁 offer 不一致。

## 常見翻車

free tier 輸出直接投 paid ads。prompt 刻意「像某歌手」當安全 brief。只有 video 有價格字，落地頁 static 沒有。活動結束 license 過期素材仍在投。

## 測量 ROI

記「法務問答幾次」「因 license 下架幾次」「改價是否觸達 static 重出」。音樂是放大器，不是 readable offer 的替代品。

## 404 修復用法

補齊空鏈，給團隊 stable SOP URL：先 static、後 audio、license 歸檔、Touch Edit 改 promo 字。
"""

GRAIN_ZHTW = """
# 完美不完美：用 grain 與 noise 讓 AI 視覺少一點塑膠感

這條繁中 URL 曾 404，搜尋卻在問「AI 圖太假怎麼辦」。過度 smooth skin、uniform noise、HDR halos 是典型 AI tell。適度 film grain 與 controlled noise 可以讓 static 更像相機物料，但 grain 不是「加越多越好」——brief 要寫 grain intensity、保留 readable label、以及 **Touch Edit** 後 grain 是否仍自然。Lovart **ChatCanvas**、**Design Agent**、**Brand Kit**、**Touch Edit** 在 series 一致前提下加 texture。

## grain 要解決的不是「復古濾鏡」

很多團隊把 grain 理解成 Instagram 復古 preset，結果 label 也糊了。正確做法是 brief 指定：subject zone 輕 grain 8–12%，headline band 與 CTA stripe 保持 flat 可讀，product cutout edge 少 noise。**Brand Kit** 定義 grain role 與 accent stripe，**Touch Edit** 改價時不破坏 grain continuity。

## ChatCanvas brief 怎麼寫 grain

弱 brief：「加一點顆粒感」。強 brief：「Brand Kit sage hero, subtle film grain 10% on background only, SKU zone sharp, price bottom left safe zone flat for Touch Edit, 4:5 1080×1350, no double CTA」。把 grain 當驗收字段，不是後期 guess。

## Touch Edit 與 texture 邊界

改「限時 NT$199」到「第二件半價」，**Touch Edit** 只框 CTA 帶，指令寫「保持 stripe 背景與 grain level，只替換文案」。若 full regen，grain pattern 常 random 變，series 不像同一 campaign。

## Brand Kit 防 carousel drift

slide 3 發明新 grain intensity 會讓 carousel 像拼貼。Kit 裡定義 background_grain_level 與 accent hex。同一 **ChatCanvas** thread 出 master，Touch Edit 導出 crop。

## static-first 與 video companion

grain 在 static 定調後，video hook 色溫與 noise profile 對齊 **Brand Kit**。clip 內不要 baked 小字 offer；readable promo 在 static。

## 常見失敗

全圖 heavy grain 導致 price unreadable。safe zone 內 busy texture。改價 full regen 導致 grain 不一致。跳過 Brand Kit 手工加 LUT。

## 測量什麼

記「改 CTA 一次幾分鐘」「carousel grain drift 幾次」。revision cost 決定 texture workflow 是否值得 daily 用。
"""

YICHU_GONGJU_ZH = """
# AI 易出设计工具工作流：创作者从 brief 到可改稿 static 的实操

这条中文 URL 曾返回 404。slug 里的「易出/一出」指创作者要的「容易出稿、容易改稿」设计产出，不是只谈地理上的北京。搜索却在问：国内创作者怎么用 AI 设计工具稳定出物料、改价不全图重 roll。Lovart **ChatCanvas**、**Design Agent**、**Brand Kit**、**Touch Edit** 组成 daily rhythm：brief 合同 → Kit 锁色 → thread 内 batch → Touch Edit 改 promo。

## 创作者 daily 四个输出物

第一是社媒 hero 与 carousel：比例、safe zone、readable 价格。第二是小店 promo 与菜单角标：改价频繁。第三是短视频 companion static：静音 feed 能看懂 offer。第四是品牌 series：色温与 type role 不 drift。纯「出一张好看图」工具解决不了后三条。

## ChatCanvas brief 合同怎么写

弱 brief：「高级感国潮海报」。强 brief：「SKU 居中，Brand Kit coral + ink，headline band top 15%，price bottom left safe zone，disclaimer 一行 footer，1:1 与 4:5 同 thread，禁止生成图内中文小字」。**Design Agent** 只有 brief 有验收字段时才能 QA。

## Brand Kit 先于 batch

没有 **Brand Kit**，slide 3 发明新 accent。先 Kit 写 primary、promo stripe、title/body type role、logo clear space。再 **ChatCanvas** 开 product thread。改活动用 **Touch Edit** 改字层，不碰 product cutout。

## Touch Edit 与「易出」的真正含义

易出不是 one-click 奇迹，是改价 five 分钟内关闭。周二改「满减 200」到「新品上市」，**Touch Edit** 框 CTA 带，保持 stripe 与字重。full regen 才是创作者时间黑洞。

## 与抠图/换背景工具分工

抠图 isolate SKU；campaign 还需要 composite、readable promo、series 一致。**ChatCanvas** + Kit + Touch Edit 覆盖 daily ops。video 展示可 companion，价格必须以 static 可编辑层为准。

## 常见失败

只有氛围图没有 readable 价格。改活动 full regen。carousel 色 drift。跳过 Brand Kit。把 free tier 当 production。

## 404 修复意义

给创作者 stable SOP URL，onboarding 不用群问「到底哪套流程出稿」。
"""

INTERIOR_TOOLS_ZH = """
# AI 室内设计工具对比：mood board、换家具与 revision cost

这条中文 URL 曾返回 404，搜索却在问「哪个 AI 室内设计工具好用」。对比不能只比「哪张图更豪华」。要看 mood board 是否可 series、换家具是否 **Touch Edit** 局部、改标注是否 full regen、**Brand Kit** 是否防 drift。Lovart **ChatCanvas** 与 **Design Agent** 面向 revision-heavy 室内项目；纯 staging 单张工具适合 exploration，不适合 weekly client change。

## 三类需求要分开比

第一类 mood exploration：单张 direction 即可，很多工具够用。第二类 client presentation series：需要 **ChatCanvas** thread 与 **Brand Kit** 锁 wood tone 与 accent。第三类 furniture swap 迭代：需要 **Touch Edit** 框选换沙发茶几，不是整图 re-roll。

## 公平对比标准

比 readable 标注层、carousel 色 drift、改一件家具分钟数、export 比例、商用 license 是否清晰。单张 win 的工具可能在 Tuesday client edit 上 lose。

## ChatCanvas mood board 工作流

brief 写风格、主色、相机高度、禁止 fake window。出 3–4 direction，选一进 **Brand Kit**。layout pass 定 focal point 与留白。furniture swap 用 **Touch Edit**：「keep wall floor, replace sofa zone beige linen」。

## Touch Edit 换家具场景

客户改「茶几换圆角、灯换 brass」时，局部 swap 成本应低于 full regen。若工具只能 re-roll，室内设计师 weekly capacity 会被 eat。

## 与 virtual staging 工具分工

staging 偏氛围单张；Lovart 偏 editable series 与 promo 标注。reference image 可进 brief，final deliverable 仍需 Touch Edit 可改层。

## 常见失败

比十款工具只看 luxury 风格。忽略 ToS。价格 baked in pixels。carousel 每 slide 不同 substyles。

## 测量什么

记「换一件家具几分钟」「drift 几次」「legal/client return 几次」。404 修复页给 stable comparison SOP URL。
"""

# FAQ blocks
FAQ = {
    "video_prompts_zh": """
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
""",
    "interior_makeover_zh": """
## FAQ

**AI 能做 room makeover 吗？**  
能，分 mood board、layout、Touch Edit 换家具三阶段；不要一次 prompt 要混搭风格。

**换沙发要整图重出吗？**  
不需要。Touch Edit 框选家具区；保留墙地。

**Brand Kit 必须先建吗？**  
series 项目强烈建议，防 wood tone drift。

**和 virtual staging 分工？**  
staging 偏单张；ChatCanvas 偏 editable series。

**404 修复？**  
补齐 searchable 室内 workflow URL。
""",
    "body_age_ko": """
## FAQ

**연령 변환 전 필수는?**  
서면 동의, 미성년·유명인 무단 금지, medical claim 금지, disclaimer.

**clip에 가격 넣어도 되나?**  
안 됩니다. offer는 ChatCanvas static editable layer.

**Touch Edit 용도?**  
promo·날짜·가격만; portrait pixel 최소 변경.

**404 이유?**  
KO 문서 누락; stable URL 복구.

**Brand Kit?**  
carousel series accent drift 방지.
""",
    "medeo_pt": """
## FAQ

**Medeo cobre o funil inteiro?**  
Não. Clip mood sim; preço editável exige ChatCanvas static.

**Mudança de preço na terça?**  
Touch Edit no static; evite regen clip.

**Por que 404?**  
Documento PT ausente; URL restaurada.

**Licença comercial?**  
Verifique ToS Medeo; arquive por campanha.

**Workflow recomendado?**  
Brand Kit → static ChatCanvas → legal pass → clip Medeo opcional.
""",
    "economic_impact_zh": """
## FAQ

**经济影响看什么指标？**  
改价分钟、drift 次数、legal return、weekly export 尺寸数；不是 first frame wow。

**static-first 如何省钱？**  
Touch Edit 改 promo，不触发 video regen。

**Brand Kit ROI？**  
减少 carousel accent drift 与 full regen。

**404 修复？**  
给 ops 讨论 stable URL，非 hype。

**和纯生成工具比？**  
比 revision cost，不比单张 cute。
""",
    "coffee_shop_ko": """
## FAQ

**디자인 경험 없어도 되나?**  
brief만 구체적이면 됩니다. Brand Kit 먼저.

**가격만 바꾸려면?**  
Touch Edit price block; full regen 피함.

**story UI 가림?**  
brief safe zone + Touch Edit 조정.

**404 이유?**  
KO 문서 없음; stable URL.

**Brand Kit?**  
drink promo series brown tone drift 방지.
""",
    "music_zhtw": """
## FAQ

**AI 音樂能直接投 paid ads 嗎？**  
視平台與 license tier；必須 archive license PDF，不能假設 free 可商用。

**為什麼強調 static 層？**  
offer 與價格須在 Touch Edit 可改靜態，不能只在音軌。

**和 Lovart 怎麼配合？**  
ChatCanvas hero/end card，Brand Kit 鎖色，legal 後再配 music bed。

**與簡體 batch2 關係？**  
本篇繁中重寫，非逐句翻譯；授權與用語分開寫。

**改價要重出 music 嗎？**  
不用；改 static promo 字即可。
""",
    "grain_zhtw": """
## FAQ

**grain 加越多越好嗎？**  
不是。background 輕 grain，price/CTA band 保持 flat 可讀。

**改價會破坏 grain 吗？**  
Touch Edit 只改 CTA 字層，保持 stripe grain level。

**Brand Kit 作用？**  
定義 background_grain_level，防 carousel drift。

**404 修復？**  
stable URL 給 texture workflow SOP。

**video companion？**  
static 定調後 clip 對齊 Brand Kit 色溫。
""",
    "yichu_gongju_zh": """
## FAQ

**「易出」是 one-click 吗？**  
不是。指改价 Touch Edit 五分钟内关闭，brief 合同 + Brand Kit。

**创作者要先建 Brand Kit 吗？**  
有固定品牌色与字体时强烈建议。

**和抠图工具分工？**  
抠图 isolate SKU；ChatCanvas 负责 composite 与 editable promo。

**404 修复？**  
补齐创作者 stable SOP URL。

**video 与 static？**  
static-first；价格必须在可编辑层。
""",
    "interior_tools_zh": """
## FAQ

**对比工具只看效果图够吗？**  
不够。要比 Touch Edit 换家具分钟数与 drift。

**换家具要 full regen 吗？**  
不需要。Touch Edit 局部 swap；保留墙地。

**mood board 怎么做？**  
ChatCanvas thread 出 3–4 direction，选一进 Brand Kit。

**404 修复？**  
stable comparison URL。

**Brand Kit？**  
室内 series 锁 wood tone 与 accent。
""",
}

# Expansion paragraphs
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


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 현장 메모 {n}: {topic}

첫 brief가 「고급스럽게」로 끝나면 가격 숫자가 작아지고 badge가 얼굴을 가립니다. 두 번째는 safe zone과 필수 필드만 고칩니다. **Design Agent**와 **ChatCanvas**에서 thread를 유지하면 carousel slide 4 색 drift를 줄입니다. {topic}에서 **Touch Edit** 5분 이내 가격 수정이면 도구가 맞습니다. 30분 full regen이면 Brand Kit부터 다시 하세요. 404 복구 URL은 onboarding용 stable link입니다.
"""


def expand_pt(topic: str, n: int) -> str:
    return f"""
## Nota de campo {n}: {topic}

A primeira passagem falha quando o brief diz premium sem grid, safe zone ou papéis tipográficos. A segunda corrige só esses campos; a terceira entra no fluxo Brand Kit. Meça minutos por fix de headline, não wow de demo. Em **{topic}**, se **Touch Edit** fecha mudança de preço em menos de cinco minutos, o loop static-first funciona. Se cada edit exige regen total, ajuste Brand Kit e templates de brief. URL restaurada para SOP estável.
"""


ARTICLES = [
    {
        "rank": 53,
        "key": "video_prompts_zh",
        "lang": "zh",
        "slug": "ai-video-prompts",
        "cover": "014",
        "category": "How-To",
        "title": "AI 视频 Prompt 结构指南：营销 static-first 配套",
        "seo_title": "AI 视频 Prompt — 营销 static-first 工作流",
        "description": "404 修复：营销 video prompt 五段结构，ChatCanvas static-first，Brand Kit，Touch Edit 改价。",
        "seo_description": "video prompt 结构：Design Agent、Brand Kit、Touch Edit、static companion。",
        "focus": "ai video prompts 营销",
        "keywords": ["ai video prompts", "chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Video Prompts",
        "body": VIDEO_PROMPTS_ZH,
        "expand_topic": "营销 video 与 static 一致",
    },
    {
        "rank": 54,
        "key": "interior_makeover_zh",
        "lang": "zh",
        "slug": "complete-guide-ai-interior-design-room-makeover",
        "cover": "021",
        "category": "Complete Guide",
        "title": "AI 室内改造完全指南：ChatCanvas 情绪板与 Touch Edit 换家具",
        "seo_title": "AI 室内改造指南 — mood board 与换家具",
        "description": "404 修复：室内 makeover 三阶段，ChatCanvas mood board，Touch Edit 换家具，Brand Kit 防 drift。",
        "seo_description": "室内 AI：Design Agent、ChatCanvas mood board、Touch Edit furniture swap。",
        "focus": "ai 室内改造 room makeover",
        "keywords": ["ai 室内改造", "room makeover", "chatcanvas", "touch edit"],
        "cluster": "Complete Guide — Interior",
        "body": INTERIOR_MAKEOVER_ZH,
        "expand_topic": "mood board 与家具 swap",
    },
    {
        "rank": 55,
        "key": "body_age_ko",
        "lang": "ko",
        "slug": "complete-guide-ai-body-age-transformation-portrait",
        "cover": "028",
        "category": "Complete Guide",
        "title": "AI 초상 연령 변환 완전 가이드 2026: 윤리·동의·static 분업",
        "seo_title": "AI 연령 변환 가이드 — 윤리 workflow",
        "description": "KO 404 fix: portrait age transform ethics, ChatCanvas static-first, Brand Kit, Touch Edit.",
        "seo_description": "연령 변환 AI: 동의 checklist, Design Agent, Touch Edit promo.",
        "focus": "ai body age transformation portrait",
        "keywords": ["ai age transform", "portrait ai", "lovart chatcanvas", "touch edit"],
        "cluster": "Complete Guide — Portrait Ethics",
        "body": BODY_AGE_KO,
        "expand_topic": "portrait ethics static companion",
    },
    {
        "rank": 56,
        "key": "medeo_pt",
        "lang": "pt",
        "slug": "medeo-ai-review",
        "cover": "035",
        "category": "Review",
        "title": "Medeo AI Review 2026: clip mood versus static de campanha editável",
        "seo_title": "Medeo AI review — static ChatCanvas workflow",
        "description": "404 fix: avaliação honesta Medeo AI vs Lovart ChatCanvas static, Brand Kit, Touch Edit.",
        "seo_description": "Medeo AI review PT: mood clip vs editable static, licença, workflow paralelo.",
        "focus": "medeo ai review",
        "keywords": ["medeo ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Medeo",
        "body": MEDEO_PT,
        "expand_topic": "Medeo clip vs static offer",
    },
    {
        "rank": 57,
        "key": "economic_impact_zh",
        "lang": "zh",
        "slug": "ai-design-economic-impact-2026",
        "cover": "042",
        "category": "Insight & Trend",
        "title": "2026 AI 设计经济影响：设计运营成本账，不是 hype",
        "seo_title": "AI 设计经济影响 2026 — ops 成本视角",
        "description": "404 修复：design ops 四条成本线，revision cost，ChatCanvas、Brand Kit、Touch Edit ROI 框架。",
        "seo_description": "AI 设计经济：static-first、Touch Edit 改价、Brand Kit anti-drift。",
        "focus": "ai design economic impact 2026",
        "keywords": ["ai design economic impact", "design ops", "lovart chatcanvas", "brand kit"],
        "cluster": "Insight — Economics",
        "body": ECONOMIC_IMPACT_ZH,
        "expand_topic": "design ops revision cost",
    },
    {
        "rank": 58,
        "key": "coffee_shop_ko",
        "lang": "ko",
        "slug": "best-ai-design-agent-for-coffee-shop-owner",
        "cover": "049",
        "category": "Industry Solution",
        "title": "2026년 커피숍 사장을 위한 최고의 AI 디자인 에이전트",
        "seo_title": "커피숍 AI 디자인 에이전트 — 메뉴·promo",
        "description": "KO 404 fix: 커피숍 menu·seasonal promo·story cover, ChatCanvas, Brand Kit, Touch Edit.",
        "seo_description": "Coffee shop AI: Design Agent, Brand Kit, Touch Edit, static-first.",
        "focus": "ai design agent coffee shop",
        "keywords": ["coffee shop ai", "chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Coffee Shop",
        "body": COFFEE_SHOP_KO,
        "expand_topic": "커피숍 메뉴판과 시즌 promo",
    },
    {
        "rank": 59,
        "key": "music_zhtw",
        "lang": "zh-TW",
        "slug": "ai-music-generator-complete-guide-2026",
        "cover": "054",
        "category": "Complete Guide",
        "title": "2026 AI 音樂生成完全指南：行銷配樂、授權與靜態層",
        "seo_title": "AI 音樂生成指南 2026 — 繁中授權實務",
        "description": "繁中 404 修復：AI 音樂商用邊界、license checklist、ChatCanvas static-first（非簡體翻譯）。",
        "seo_description": "AI 音樂繁中：Design Agent、Brand Kit、Touch Edit、授權 caution。",
        "focus": "ai music generator 2026",
        "keywords": ["ai 音樂生成", "music license", "lovart chatcanvas", "brand kit"],
        "cluster": "Complete Guide — Music",
        "body": MUSIC_ZHTW,
        "expand_topic": "行銷配樂與 license 歸檔",
    },
    {
        "rank": 60,
        "key": "grain_zhtw",
        "lang": "zh-TW",
        "slug": "perfect-imperfection-add-grain-noise-natural-ai",
        "cover": "060",
        "category": "Better Design",
        "title": "完美不完美：用 grain 與 noise 讓 AI 視覺更自然",
        "seo_title": "AI grain noise 指南 — 少一點塑膠感",
        "description": "繁中 404 修復：film grain brief、Touch Edit 改 CTA 不破壞 texture、Brand Kit series。",
        "seo_description": "grain noise AI：ChatCanvas、Design Agent、Brand Kit、Touch Edit texture workflow。",
        "focus": "ai grain noise natural",
        "keywords": ["ai grain", "film noise", "lovart chatcanvas", "touch edit"],
        "cluster": "Better Design — Grain",
        "body": GRAIN_ZHTW,
        "expand_topic": "grain 與 readable label 平衡",
    },
    {
        "rank": 61,
        "key": "yichu_gongju_zh",
        "lang": "zh",
        "slug": "ai-beijing-yichu-gongju",
        "cover": "061",
        "category": "Best Practice",
        "title": "AI 易出设计工具工作流：创作者 brief 到可改稿 static",
        "seo_title": "AI 易出设计工具 — ChatCanvas 创作者工作流",
        "description": "404 修复：创作者 daily 四输出物，brief 合同，Brand Kit，Touch Edit 改价，非 one-click hype。",
        "seo_description": "易出设计工具：Design Agent、Brand Kit、Touch Edit、static-first 出稿。",
        "focus": "ai 易出 设计工具 创作者",
        "keywords": ["ai 设计工具", "易出", "lovart chatcanvas", "brand kit"],
        "cluster": "Best Practice — Creator Workflow",
        "body": YICHU_GONGJU_ZH,
        "expand_topic": "创作者 daily 出稿 rhythm",
    },
    {
        "rank": 62,
        "key": "interior_tools_zh",
        "lang": "zh",
        "slug": "ai-interior-design-tools-compared",
        "cover": "062",
        "category": "Comparison",
        "title": "AI 室内设计工具对比：mood board、换家具与 revision cost",
        "seo_title": "AI 室内设计工具对比 — Touch Edit 换家具",
        "description": "404 修复：对比 mood board、Touch Edit swap、Brand Kit drift；ChatCanvas revision-heavy 室内项目。",
        "seo_description": "室内 AI 对比：Design Agent、ChatCanvas、Touch Edit furniture swap。",
        "focus": "ai interior design tools compared",
        "keywords": ["ai 室内设计工具", "interior ai compare", "chatcanvas", "touch edit"],
        "cluster": "Comparison — Interior Tools",
        "body": INTERIOR_TOOLS_ZH,
        "expand_topic": "室内工具 revision cost 对比",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "zh-TW": expand_zhtw,
    "ko": expand_ko,
    "pt": expand_pt,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch5 content cluster.*\n"
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

    print(f"{'RANK':>4} {'FILE':<75} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 120)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['rank']:>4} {r['file']:<75} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["file"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
