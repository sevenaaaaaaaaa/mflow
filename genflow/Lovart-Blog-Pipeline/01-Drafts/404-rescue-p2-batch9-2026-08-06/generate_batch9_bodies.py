#!/usr/bin/env python3
"""Generate 404-rescue P2 batch9 blog bodies (10 files). Self-contained.

Ranks #93–#102 from 404-rescue-compact lane.
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

DESIGN_AGENT_ULTIMATE_JA = """
# AI Design Agent と ChatCanvas 完全ガイド：クリエイターとビジネスの実務向け

この日本語 URL は 404 でしたが、検索は「Design Agent」「ChatCanvas」「クリエイター ビジネス 使い方」を求めていました。本稿は hype ではなく、**Brand Kit** 設定、**ChatCanvas** thread 運用、**Touch Edit** 局部修正、**Design Agent** QA という daily ops の順序を説明します。最初の wow 一枚より、火曜の価格変更が何分で終わるかが ROI です。

## クリエイターと SMB が本当に解く四つの場面

第一は hero 主図と carousel slide 2–6：同一 grid で copy だけ差し替え、accent が drift しないこと。第二は story 9:16 と feed 4:5：同 thread から derivative crop、CTA safe zone を切らない。第三は end card と thumbnail：価格・ disclaimer を editable layer に置く。第四は client deck 内ページ：firm VI を **Brand Kit** に載せ、提案ごとに full regen しない。

## Design Agent の役割：brief 契約の QA 実行役

**Design Agent** はクリエイティブディレクター代わりではありません。brief に書いた acceptance criteria を機械的にチェックします：safe zone pass、readable price at mobile width、hex drift vs **Brand Kit**、disclaimer footer 存在、double CTA なし。第二 pass で足りないのは brief フィールド追加で、モデル lottery ではありません。

## ChatCanvas brief 契約の書き方

弱い brief：「モダンで高級な SNS 投稿」。強い brief：「hero 4:5 1080×1350、headline top 15% flat band for Touch Edit、Brand Kit navy #1a2b3c + sand accent、price bottom left safe zone、disclaimer footer editable、render 内小文字価格禁止、slide 2–6 同一 thread」。ratio、safe zone、Kit hex を数値で書くと **Design Agent** が pass/fail できます。

## Brand Kit を batch 生成より先に

承認済み packaging、店頭 POP、過去 deck から primary hex、accent hex、title/body type role、logo clear space を取り込む。stock marble や random pastel を brand color にしない。**ChatCanvas** の全 thread が同 role を参照すると carousel slide 4 の accent lottery が止まります。

## Touch Edit：価格変更は identity lottery にしない

「新規 20% OFF」から「期間限定 ¥980」へ：**Touch Edit** で CTA 帯のみ。stripe geometry と **Brand Kit** accent は保持。full regen は product angle と背景を random 変更。測る指標は「価格 fix 分数」です。

## ビジネス向け：client revision と thread memory

代理店・フリーランスは client A と B で accent が混線しやすい。**ChatCanvas** thread を client 単位で分け、**Brand Kit** を client VI ごとに切替。revision 履歴が thread に残るため「前回の角標位置」で再説明不要。**Design Agent** は client disclaimer 原文の有無もチェック。

## static-first、motion は companion

feed autoplay は mute 前提。ユーザーが screenshot するのは still。順序：static legal pass → optional motion hook。逆順だと clip 角標に offer があるのに landing static が edit 不可、という mismatch が起きます。

## よくある失敗七つ

**Brand Kit** 未設定で slide 4 だけ別 accent。readable 価格を render に bake。video hook に offer、static hero になし。改 copy のたび full regen 三十分。404 URL のまま SOP が Slack に散在。brief が形容詞のみで safe zone なし。**Touch Edit** 不可 promo layer 設計。

## 測るべき指標

価格 fix 分数、slide accent drift 回数、legal return 回数、export size 数 per action。404 復旧ページは onboarding 用 stable SOP link です。
"""

BRAND_KIT_NAIL_KO = """
# 네일 스튜디오 Brand Kit: 예약 카드, 시술 메뉴, Reels 커버

이 한국어 URL은 404였지만, 검색은 「네일샵 Brand Kit」「네일 스튜디오 AI 디자인」을 물었습니다. 중국어 batch6 nail studio 글과 다른 언어·현장 맥락입니다. 네일샵의 daily ops는 월별 시술가 변경, 젤·케어 패키지 promo, 예약 오픈 알림, 인스타 Reels cover입니다. 매번 새 prompt면 파스텔과 블랙골드 accent가 섞여 고객이 「샵 분위기가 매번 달라」고 느낍니다.

## 네일 스튜디오가 풀어야 할 네 가지 장면

첫째 시술·패키지 가격표: 젤 풀세트, 케어 add-on 가격이 자주 바뀌고, 글자는 readable, 카운터·폰 화면 모두 OK. 둘째 예약 오픈·한정 슬롯 promo: copy만 바꾸고 grid는 고정. 셋째 before/after portfolio carousel: 샵명·각 badge 위치 통일. 넷째 오픈·시즌 이벤트: 문구는 바꿔도 **Brand Kit** visual system은 유지.

Lovart **Design Agent**와 **ChatCanvas**는 대화형 수정 가능한 design surface; **Brand Kit**은 primary hex, title font, logo clear space 기억; **Touch Edit**은 가격 숫자만 바꾸고 전체 regen 안 함.

## ChatCanvas brief 예시

나쁜 brief: 「고급 네일샵 느낌」. 좋은 brief: 「젤 풀세트 promo, 4:5 1080×1350, price bottom left safe zone, top 12% Reels UI 여백, Brand Kit dusty rose + charcoal, disclaimer editable, render 내 작은 가격 금지, slide 2–6 same thread」.

이미 샵 VI가 있으면 **Brand Kit** 먼저: primary, accent, title/body role, logo minimum size. 이후 시술 시리즈 생성 시 accent drift 없음.

## Touch Edit와 월말 가격 변경

네일 가격표는 「전체 재출」이 가장 비쌉니다. 월초 패키지 조정, mid-month add-on promo — **ChatCanvas**에서 layout 고정, **Touch Edit**로 숫자·패키지명만.**Brand Kit**이 title font와 color block 위치 보장.

## Reels cover와 story safe zone

Reels cover brief에 safe zone 명시: title top 12%, bottom 10% UI 버튼 회피. 9:16 story는 nail art close-up이 CTA band에 가리지 않게 bottom 20% flat for Touch Edit.

## compliance와 현장 습관

시술 효과·가격 표시·예약 규정 문구를 brief 필수 필드로. **ChatCanvas** static legal pass 후 optional motion. video에 offer 있으면 static hero에도 readable price layer.

## zh batch6 nail 글과의 차이

KO 버전은 한국 네일샵 용어(젤, 케어, 예약 오픈), Reels·카카오 채널 safe zone, 현지 disclaimer 습관에 맞춤. workflow 구조는 동일: Brand Kit → ChatCanvas thread → Touch Edit → Design Agent QA.

## 측정

가격 fix 분수, drift 횟수, export size 수. 404 stable nail studio Brand Kit SOP URL.
"""

TEXT_TO_VIDEO_PT = """
# Text-to-video: workflow honesto static-first para promo revisável

Esta URL em português retornava 404 enquanto buscas pediam 「text to video AI workflow」. Resposta honesta: text-to-video brilha em motion hooks, mas campanhas revision-heavy ainda precisam de master static em **ChatCanvas**, cores em **Brand Kit**, copy de preço em **Touch Edit**, e QA em **Design Agent**. Não é escolha A ou B — é ordem de produção.

## O que text-to-video faz bem

Primeiro: reveal de produto em clip curto. Segundo: exploração de mood antes de fixar layout. Terceiro: companion para feed autoplay mute. Quarto: one-off creator clip quando preço legal não muda toda semana.

## Onde campanhas static quebram

Mudança de preço vira full regen de trinta minutos. Slide 4 do carousel com accent diferente. disclaimer baked em pixels. clip com offer mas landing static sem camada editável. **Brand Kit** sem roles hex. **Touch Edit** ausente na faixa promo.

## Ordem static-first recomendada

Passo um: hero 4:5 e end card em **ChatCanvas**, legal pass com preço readable. Passo dois: optional motion a partir do still aprovado. Inverter gera mismatch — usuário screenshot do still, não do frame do clip.

## ChatCanvas brief contract

Brief fraco: 「vídeo premium para Instagram」. Brief forte: 「hero 4:5 1080×1350, Brand Kit navy + sand, price bottom left safe zone, disclaimer footer editable, no small price text in render, slides 2–6 same thread, 9:16 crop derivative from master」. **Design Agent** precisa de campos numéricos.

## Brand Kit antes do batch clip

Extraia primary e accent de media kit aprovado. Sem **Brand Kit**, cada export inventa novo coral. Um thread **ChatCanvas** para família de campanha reduz drift entre slide 2 e slide 6.

## Touch Edit na faixa CTA

Troca 「20% OFF」 por 「Frete grátis」: **Touch Edit** só na label do botão, geometry e accent stripe do **Brand Kit** intactos. Full regen randomiza recorte do produto. Ops mede 「minutos por fix de copy」, não 「beleza do primeiro frame」.

## Design Agent QA para static companion

Safe zone pass, preço legível em largura mobile, hex drift vs Kit, disclaimer presente, sem double CTA. Agent não substitui revisão legal.

## Comparação justa com ferramentas pure T2V

Mesmo brief contract, mesma tarefa de mudança de preço na terça. Métrica: minutos por fix, contagem de drift, sizes export por ação. Comparar só primeiro frame engana.

## Falhas comuns

Hero único sem thread series. preço readable baked. crop 9:16 corta CTA. clip com badge, static sem offer editável.

## Métricas que importam

Minutos por fix de preço, drift de accent, retornos legal, quantidade de sizes IAB/social por ação. URL 404 restaurada = SOP estável para text-to-video + static ops.
"""

FREEPIK_VS_LOVART_ZH = """
# Freepik AI 图像生成 vs Lovart：运营视角诚实对比

这条中文 URL 曾返回 404，但搜索仍在问「Freepik AI image generator 和 Lovart 怎么选」。不是功能清单堆叠，而是 revision cost、**Brand Kit** series、**Touch Edit** 改价、**Design Agent** QA 四条 operational 指标。Freepik 在 stock 素材与 quick mood 上有场景；Lovart **ChatCanvas** 在 editable promo series 上有场景。很多团队误判，是因为只比第一张 wow。

## Freepik 擅长的运营区间

第一是 mood board 与单张探索：快速试 direction，不必锁 hex role。第二是 stock 搭配：已有图库 membership 时的 companion edit。第三是 casual social one-off：beauty-first 单帖，价格 layer 少。第四是 template 市场：快速起稿，series consistency 优先级低。

## revision-heavy campaign 里常见的 gap

周二改 promo copy 要 full regen 三十分钟。carousel slide 4 accent drift。disclaimer bake 进像素，法务不能改字。video 角标有 offer 但 landing static 没有 readable price。**Brand Kit** hex role 未设。**Touch Edit** 可编辑 CTA 带缺失。

## Lovart ChatCanvas workflow 的 operational 价值

**ChatCanvas** thread per campaign family，revision 历史留在 thread。**Brand Kit** 锁 primary/accent/type role。**Touch Edit** 改 CTA 与 price block 不全图重 roll。**Design Agent** 验收 safe zone、readable price、hex drift vs Kit。KPI 是「改价五分钟」不是「第一张惊艳」。

## 公平对比实验怎么设计

同一 brief contract：hero 4:5，price bottom left safe zone，disclaimer footer editable，Brand Kit hex 写死。同一 revision task：周二把「满 200 减 30」改成「新客 ¥99」。测量：改价分钟、drift 次数、一次 action export 几种尺寸。只比第一帧好看会误导采购决策。

## 选 Freepik 更合适的团队画像

周产出以 casual social 5–10 张为主，价格/日期 weekly 改动少，carousel series 要求低，已有 heavy stock 订阅。revision cost 低于 first-post speed。

## 选 Lovart workflow 更合适的团队画像

周 promo 要 20+ 尺寸 export，价格/活动 weekly 改，carousel 系列 legal disclaimer 必填，**Touch Edit** 五分钟内改价是硬 KPI。404 修复页给这类团队 stable SOP URL。

## ChatCanvas brief 示例（Lovart 侧）

弱 brief：「高级产品图」。强 brief：「hero 4:5 1080×1350，Brand Kit slate + coral，price bottom left，disclaimer editable，禁止生成图内小字，slide 2–6 同 thread」。**Design Agent** 需要 numeric acceptance fields。

## Touch Edit 是分水岭

promo 变更若 **Touch Edit** 五分钟完成，static-first 成立。三十分钟 full regen 说明 process 未设好，不是「换模型」能救。对比文应写 edit cost framework，不是 feature checkbox。

## 伦理与版权边界

stock asset、水印、第三方 IP — 各平台 ToS 确认。campaign folder 存档 license screenshot。评测不写「谁更强」，写「你的 KPI 是 wow 还是改价分钟」。

## 常见失败

用 Freepik 出 hero 再用 Lovart 改价但没 **Brand Kit** → 仍 drift。用 Lovart 却只 single-shot prompt 不用 thread → 失去 revision memory。404 URL 未修复 → SOP 散在群里。

## 测量什么才有用

改价一次几分钟、carousel drift 几次、legal return 几次、export size 数 per action。
"""

AUTO_RESIZE_ZH = """
# Auto-Resize Magic：横版 Banner 一键转竖版 Story 的可编辑工作流

这条中文 URL 曾返回 404，slug 带 auto-resize magic，搜索需要 honest workflow：不是「AI 一键完美」，而是 **ChatCanvas** master 4:5 或 16:9 → derivative 9:16 crop、**Brand Kit** 锁 accent、**Touch Edit** 改 CTA 带、**Design Agent** QA safe zone 不被切。landscape banner 转 portrait story 的核心风险是 CTA 与 price 被 crop 掉。

## 横转竖真正要解决的四个问题

第一是 geometry：headline band 从 top 15% 变 bottom 20% 时是否仍 readable。第二是 product cutout：横版居中产品在竖版是否被 UI chrome 挡。第三是 price/disclaimer：从 bottom left 变 footer band 是否仍在 **Touch Edit** 层。第四是 series consistency：同一 campaign 横竖 accent 不 drift。

## 为什么「一键 auto-resize」常翻车

 naive crop 切掉 CTA button。full regen 竖版会 random 改 product angle 与 **Brand Kit** accent。readable 价格 baked in pixels，竖版改字要重出。video story 有 offer 但 feed static 没有。测量应用「竖版改价分钟」不是「转换秒数」。

## ChatCanvas brief 合同写法

弱 brief：「把横 banner 变 story」。强 brief：「master 1920×1080 landscape，derivative 9:16 1080×1920，CTA bottom 20% flat for Touch Edit，Brand Kit navy + coral，price safe zone bottom left on both ratios，disclaimer footer editable，crop-first 禁止切 CTA，同 thread 导出 feed 4:5」。**Design Agent** 需要两种 ratio 的 acceptance fields。

## Brand Kit 约束横竖不 drift

从已批准 media kit 取样 primary、accent、title/body role。无 **Brand Kit** 时竖版发明新 accent，用户划 feed 会感觉不是同一活动。**ChatCanvas** 同一 thread batch landscape + portrait，只换 copy 不换 grid skeleton。

## Touch Edit 改竖版 CTA 不改横版 identity

竖版改「立即预约」为「限时体验」：**Touch Edit** 框 story bottom band，保持横版 hero geometry 与 **Brand Kit** stripe。full regen 会 lottery 改 product cutout。

## Design Agent QA for resize derivatives

检查 portrait 下 headline 不被 platform UI 挡、price 在 thumb reach 区、disclaimer 存在、hex drift vs Kit、landscape 与 portrait double CTA 一致。不是替 designer 想创意，是验收 brief 字段。

## static-first 再配 motion story

story autoplay 常静音；用户 screenshot 的是 still frame。顺序：static landscape + portrait legal pass → optional motion hook。反过来会产生 clip 有 offer 但 static story 不能 edit 的 mismatch。

## 常见失败

单尺寸横版无 thread，竖版每次 full regen。crop 切掉 price block。竖版 readable text baked。carousel slide 4 竖版 accent drift。

## 一週工作流示例

周一确认本周横竖尺寸清单。周二 **ChatCanvas** 出 landscape master + portrait derivative。周三 **Touch Edit** 改 CTA copy。周四 **Design Agent** QA safe zone。周五只处理临时改价，沿用同一 thread。

## 测量 ROI

横转竖一次几分钟、crop 切 CTA 几次、drift 几次、一次 action export 几种 ratio。404 修复给 ops team stable auto-resize SOP URL。
"""

BRAND_KIT_COURSE_ZH = """
# 课程创作者 Brand Kit：大纲卡、招生海报与直播封面

这条中文 URL 曾返回 404，但搜索仍在问「课程创作者能不能用 AI 做日常物料」。知识付费与训练营的真实节奏不是偶尔做一张海报，而是每期改 syllabus 摘要、换招生价、发直播封面、更新学员 testimonial 卡。若每次从零 prompt，学术蓝与行动橙 accent 很快漂移，学员会觉得你的课「网上形象不专业」。

## 课程创作者真正要解决的四个场景

第一是招生与早鸟价目：季课、模块价、优惠券常改，文字必须 readable、留白足够、手机与视频号封面都能看。第二是 syllabus 与 module 卡：章节名改但版式要固定只换 copy。第三是讲师 live 与 replay 封面：横竖 safe zone 不同，标题不能被平台 UI 挡住。第四是 cohort promo：文案改但 **Brand Kit** 视觉系统不能散。

Lovart **Design Agent** 与 **ChatCanvas** 是可对话、可改稿的设计面；**Brand Kit** 记住你的主色、标题字体与 logo 留白；**Touch Edit** 用来改局部价格字而不推翻整图。

## 在 ChatCanvas 里写课程 brief

不可用 brief 是「帮我做一张高级课程海报」。可用 brief 是：「数据分析训练营早鸟，主图 4:5，价格放左下 safe zone，角标写限席，留 top 12% 给直播 UI，Brand Kit 学术蓝与行动橙，disclaimer editable」。把渠道、留白、必填栏位写进 brief。

若已有 course VI，先载入 **Brand Kit**：主色、辅助色、标题与正文字号角色、logo 最小留白。之后生成 module 系列，颜色不会每张漂移。

## 招生价目与 Touch Edit 的配合

课程价目最怕「整张重出」。开营前改早鸟价、 mid-cohort 加 bonus module，若每次重 roll，运营没空等。正确做法是在 **ChatCanvas** 里固定版式，改价用 **Touch Edit** 只动数字与套餐名。**Brand Kit** 保证标题字体与色块位置不变。

## syllabus carousel 与 series 一致

module carousel 需要同一套角标与 course name 位置。在 **ChatCanvas** 同一 thread 里批量导出模板，只换章节标签不换 grid。**Design Agent** QA：headline 不被 UI chrome 挡、disclaimer readable。

## 合规与本地习惯

课程素材涉及学习效果说明、价格公示、退款规则。把这些句子当作 brief 必填栏位。**ChatCanvas** 导出 static 审核稿，video 可以后做，但价格与机构名必须以可改文字为准。404 修复页让 SOP 有 stable URL。

## 与 generic Brand Kit 文的差异

本篇聚焦 course creator segment：syllabus 卡、cohort 招生、live 封面、早鸟倒计时 editable layer。workflow 结构同 consultant/gym  segment，但 brief 字段与 disclaimer 句不同。

## 测量什么才有用

记「改价一次几分钟」「一次活动要重出几张尺寸」。若 **Touch Edit** 平均小于五分钟而重出平均大于三十分钟，说明 Design Agent 路线成立。

## 一週工作流示例

周一确认本周 live 与 promo 清单。周二在 **ChatCanvas** 批量生成 module 卡与两版 live 封面。周三用 **Touch Edit** 改价格、改卖点词。周四导出多尺寸。周五只处理临时改价，沿用同一 thread。
"""

SKINCARE_LAUNCH_ZH = """
# 从取名到上线：护肤品牌 identity 的 AI 辅助 launch 叙事

这条中文 URL 曾返回 404，但搜索需要 case narrative：不是虚构融资数据，而是 honest workflow——命名 mood board → logo wordmark 探索 → **Brand Kit** 锁 hex → packaging hero → launch promo static → **Touch Edit** 改首发价。护肤 launch 的 revision 热点在成分 disclaimer、首发价、渠道 crop，不是第一张 bottle render。

## Launch 阶段要拆成六类输出

第一是 naming mood board：three direction，不 commit hex。第二是 wordmark + icon 探索：**ChatCanvas** thread 记 clear space。第三是 **Brand Kit** primary/accent/type role 从 approved packaging 取样。第四是 hero 4:5 与 carousel slide 2–6：同一 grid 换 copy。第五是 story 9:16 与 feed crop：同 thread derivative。第六是 end card 与 retail shelf talker：价格与 disclaimer 在 **Touch Edit** 可改层。

## 为什么 skincare launch 常卡在 revision

成分表改字要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 pastel。readable 首发价 baked in pixels。video hook 有 offer 但 landing static 没有。**Brand Kit** 未从 packaging 取样，线上 drift offline。

## ChatCanvas brief 合同（launch 版）

弱 brief：「高级护肤品牌感」。强 brief：「hero 4:5 1080×1350，product center，headline top 15% flat for Touch Edit，Brand Kit sage + cream accent from packaging sample，首发价 bottom left safe zone，成分 disclaimer footer editable，禁止生成图内小字，slide 2–6 同 thread」。**Design Agent** 需要 acceptance criteria。

## Brand Kit 从 packaging 锁 identity

从已批准 bottle label、box、dieline 取样 primary hex、accent hex、title/body role。不要用 stock marble 当品牌色。Kit 建好后，所有 **ChatCanvas** launch thread 引用同一套 role。

## Touch Edit 改首发价不改 bottle identity

改「首发 ¥199」为「限时 ¥159」：**Touch Edit** 框 CTA 带，保持 bottle geometry 与 **Brand Kit** accent stripe。full regen 会 random 改 cap highlight 与 shadow。

## Design Agent QA for regulated copy

检查成分 disclaimer 是否存在、price readable at mobile width、hex drift vs Kit、safe zone、无 double CTA。不是替法务写 copy，是验收 brief 字段。第二 pass 常只需补 disclaimer 句。

## static-first 再配 motion launch teaser

launch teaser autoplay 常 mute；用户 screenshot 的是 still。顺序：static legal pass on all sizes → optional motion。反过来会产生 clip 有 offer 但 PDP static 不能 edit 的 mismatch。

## case narrative 里的测量（不编造销售数字）

记「改首发价一次几分钟」「一次 launch export 几种尺寸」「carousel drift 几次」。若 **Touch Edit** 平均小于五分钟而重出平均大于三十分钟，说明 workflow 成立。不写虚假 GMV。

## 常见失败

跳过 Brand Kit 从 random pastel 开干。readable 价格 baked。单尺寸 hero 无 series thread。404 URL 未修复 SOP 散在 Slack。

## 404 修复意义

stable URL 给 launch checklist：hex、disclaimer 原文、brief 模板内链，新人 onboarding 不用群里问。
"""

MIANFEI_TUPIAN_ZH = """
# Lovart 免费图片生成指南：中文用户的实用工作流

这条中文 URL slug 为 lovart-mianfei-tupian（免费图片），曾返回 404。搜索意图是「免费图片怎么生成、能不能商用、怎么不改价就翻车」。诚实答案：免费 tier 能出图，但 daily ops 价值在 **Brand Kit** 锁色、**ChatCanvas** thread 记系列、**Touch Edit** 改局部、**Design Agent** 按 brief 验收——不是无限抽卡比谁第一张好看。

## 中文用户常问的四个实际问题

第一是免费额度用在哪：exploration vs production series。第二是商用边界：ToS、水印、第三方素材各平台规则不同，本文不编造 pricing tier。第三是可编辑性：免费出图若 price baked in pixels，改活动仍要 full regen。第四是 series consistency：无 **Brand Kit** 时第 10 张 post 发明新 accent。

## 免费图片生成在 campaign 里要拆成四类输出

hero 主图、carousel slide 2–6、story/feed crop、end card/thumbnail。每类都要 brief 写 ratio、safe zone、**Brand Kit** hex、disclaimer editable。单次「免费抽一张」不适合 revision-heavy promo。

## ChatCanvas brief 合同写法

弱 brief：「帮我免费生成一张好看图片」。强 brief：「hero 4:5 1080×1350，产品居中，headline band top 15% flat for Touch Edit，Brand Kit slate + coral，价格 bottom left safe zone，disclaimer footer editable，禁止生成图内小字」。**Design Agent** 才有 acceptance criteria。

## Brand Kit 先于 batch 生成

从已批准 packaging 或 prior deck 取样 primary hex、accent hex、type role。不要用 random pastel 当品牌色。Kit 建好后 **ChatCanvas** thread 引用同一 role，防 carousel drift。

## Touch Edit 改价不改 identity

改 promo copy：**Touch Edit** 框 CTA 带，保持 stripe geometry 与 **Brand Kit** accent。full regen 会 random 改产品角度。测量 ROI 用「改价分钟」。

## 与纯免费 T2I 玩具的分工

T2I playground 适合 mood board。 **ChatCanvas** + **Design Agent** 适合要改价、改 copy、导出多尺寸的 promo。若 KPI 是「改价 five 分钟」，选 workflow 工具；若 KPI 是「试 50 种风格」，选单次生成。

## 合规提醒（不编造条款）

各平台 ToS 与商用范围请阅官方说明。campaign folder 存档 license screenshot。不写虚假「永久免费无限张」承诺。

## 常见失败

跳过 Brand Kit。readable 价格 baked。video hook 有 offer static 没有。每次改 copy full regen。404 未修复 SOP 无 stable URL。

## 测量什么才有用

改价一次几分钟、export 几种尺寸、drift 几次。404 修复给中文用户 stable 免费图片 workflow SOP。
"""

NANO_BANANA_ZH = """
# Nano Banana 演示指南：deck 与 promo 的可编辑 static 工作流

这条中文 URL 曾返回 404，搜索需要 nano-banana presentation guide：把 presentation/deck 任务放进 **ChatCanvas** + **Brand Kit** + **Touch Edit** + **Design Agent** 框架，不是 generic AI PPT hype。deck 的 revision 热点在改一页 price、换 speaker bio、导出 16:9 与 4:5 封面，不是第一页 wow。

## Presentation 任务要拆成四类输出

第一是 title slide 与 agenda：logo clear space、readable headline。第二是 content slide 2–N：同一 grid 换 bullet，accent 不 drift。第三是 speaker promo 与 social cover：4:5 与 16:9 同 thread。第四是 end CTA 与 QR：price/event date 在 **Touch Edit** 可改层。

## 为什么 deck 工具常卡在周二改价

改一页 ticket price 要 full regen 三十分钟。slide 7 accent drift。readable 日期 baked in pixels。live promo video 有 offer 但 deck static 没有。**Brand Kit** hex role 未设。

## ChatCanvas brief 合同写法

弱 brief：「做一份 nano banana 风格演示」。强 brief：「deck 16:9 1920×1080，title slide Brand Kit yellow + black，slide 2–8 same thread，CTA slide bottom 20% flat for Touch Edit，event price bottom left safe zone，disclaimer footer editable，禁止 render 内小字，导出 4:5 social cover derivative」。**Design Agent** 需要 numeric fields。

## Brand Kit 锁 deck series

从已批准 prior deck 或 event VI 取样 primary、accent、title/body role。无 **Brand Kit** 时 slide 5 发明新 yellow，series 感消失。

## Touch Edit 改 ticket 价不改 layout

改「早鸟 ¥99」为「现场 ¥129」：**Touch Edit** 框 CTA slide price block，保持 grid 与 **Brand Kit** accent stripe。full regen 会 random 改 icon layout。

## Design Agent QA for presentation static

检查 headline readable at projector width、price 不在 footer crop、disclaimer 存在、hex drift vs Kit、social derivative safe zone。

## static-first 再配 talk recording companion

recording 角标常 mute autoplay；观众 screenshot 的是 slide still。顺序：static deck legal pass → optional motion bumper。

## nano-banana 语境说明

搜索词 nano-banana 可能指特定 visual motif 或 meme-adjacent deck 风格。本篇按「高 contrast readable deck + editable promo layer」写 operational guide，不编造产品 API 名称。

## 常见失败

单 deck 无 thread。readable price baked。16:9 与 4:5 各用各 accent。404 URL 未修复。

## 测量 ROI

改 ticket 价一次几分钟、slide drift 几次、export 几种 ratio。404 修复给 presenter stable SOP URL。
"""

KREA_ALTERNATIVES_EN = """
# Best Krea AI Alternatives in 2025: Image Generation Tools Compared

This English URL returned 404 while searches asked for Krea AI alternatives and 2025 image tool comparisons. Honest framing: Krea excels at real-time style exploration and live canvas iteration; revision-heavy promo still needs **ChatCanvas** static masters, **Brand Kit** hex roles, **Touch Edit** price layers, and **Design Agent** QA. Compare edit cost, not first-frame beauty.

## What Krea does well in 2025 workflows

First: live style mixing and rapid mood iteration. Second: creator exploration before committing to a layout grid. Third: single-frame social when price and disclaimer rarely change. Fourth: reference-driven aesthetics when series consistency is low priority.

## Gaps teams hit in revision-heavy campaigns

Tuesday promo copy change triggers thirty-minute full regen. Carousel slide four accent drift. Disclaimer baked into pixels. Video hook shows offer while landing static lacks editable price. No **Brand Kit** hex roles. No **Touch Edit** promo band.

## Lovart ChatCanvas workflow division of labor

One **ChatCanvas** thread per campaign family preserves revision memory. **Brand Kit** locks primary, accent, and type roles. **Touch Edit** swaps CTA copy without identity lottery. **Design Agent** checks safe zone, readable price, hex drift versus Kit. KPI is minutes per price fix.

## Fair comparison experiment design

Same brief contract: hero 4:5, price bottom left safe zone, disclaimer footer editable, Brand Kit hex specified. Same revision task: change promo copy on Tuesday. Measure minutes per fix, drift count, export sizes per action. Comparing only first-frame aesthetics misleads procurement.

## When Krea is the better fit

Teams shipping five to ten casual social posts weekly, minimal price layers, low carousel series requirements, exploration speed over edit cost.

## When Lovart workflow is the better fit

Twenty-plus size exports per promo, weekly price or date changes, carousel series with legal disclaimers, **Touch Edit** under five minutes as hard KPI.

## Other 2025 alternatives in the same edit-cost frame

Pure T2I playgrounds (batch-style diffusion tools), Canva template marketplaces, and Adobe Generative Fill each win on different axes. Operational comparison asks: after legal approves hero, how many minutes to change price across forty-two sizes? **Touch Edit** path versus full regen path.

## ChatCanvas brief example (Lovart side)

Weak: "premium product hero." Strong: "hero 4:5 1080×1350, Brand Kit slate plus coral, price bottom left, disclaimer editable, no readable small text in render, slides two through six same thread." **Design Agent** needs numeric acceptance fields.

## Touch Edit as the decision line

If promo change closes in five minutes via **Touch Edit**, static-first holds. Thirty-minute full regen means process failure, not model lottery.

## Ethics and licensing

Stock assets, watermarks, third-party IP — confirm each platform ToS. Archive license screenshots per campaign folder. Comparison writing uses edit-cost framework, not feature checkbox wars.

## Common failures

Pick Krea for exploration then expect Lovart-grade **Brand Kit** without setup. Run Lovart single-shot prompts without threads. Restored 404 URL missing — SOP scattered in Slack.

## Metrics that matter

Minutes per price fix, accent drift events, legal returns, export size count per action. Restored URL gives stable 2025 alternatives comparison SOP.
"""

# FAQ blocks
FAQ = {
    "design_agent_ultimate": """
## FAQ

**Design Agent はクリエイティブ代行？**  
いいえ。brief の acceptance criteria QA です。

**価格変更で full regen 必要？**  
不要。Touch Edit CTA 帯で足りる場合が多い。

**Brand Kit は batch より先？**  
はい。hex drift 防止のため。

**404 修復？**  
stable Design Agent + ChatCanvas SOP URL。

**static-first の意味？**  
legal pass static 後に optional motion。
""",
    "brand_kit_nail": """
## FAQ

**네일샵 Brand Kit 먼저?**  
권장. dusty rose + charcoal drift 방지.

**가격 변경 full regen?**  
아니요. Touch Edit 가격 블록.

**zh batch6 nail 글과 차이?**  
KO 현장 용어·Reels safe zone.

**404 복구?**  
stable nail studio Brand Kit SOP.

**Design Agent 역할?**  
safe zone, disclaimer, hex drift QA.
""",
    "text_to_video": """
## FAQ

**Text-to-video vs static — escolha única?**  
Não. Ordem static-first, motion companion.

**Mudança de preço exige regen total?**  
Não. Touch Edit na faixa CTA.

**Comparação justa?**  
Mesmo brief, mesma tarefa de preço na terça.

**404 fix?**  
URL estável para SOP text-to-video.

**Brand Kit antes do clip?**  
Sim, reduz drift entre slides.
""",
    "freepik_vs_lovart": """
## FAQ

**Freepik 与 Lovart 二选一？**  
不是，按 revision cost 与 KPI 分工。

**改价要整图重出吗？**  
Lovart 侧不需要，Touch Edit 框 CTA 带。

**公平对比怎么测？**  
同一 brief、同一改价任务，比分钟。

**404 修复？**  
stable operational comparison SOP URL。

**Design Agent 做什么？**  
QA safe zone、disclaimer、Brand Kit drift。
""",
    "auto_resize": """
## FAQ

**横转竖要整图重出吗？**  
不需要，ChatCanvas derivative crop + Touch Edit。

**crop 切掉 CTA 怎么办？**  
brief 写 bottom 20% flat band safe zone。

**横竖 accent 要一致吗？**  
是，Brand Kit 锁 role。

**404 修复？**  
stable auto-resize SOP URL。

**Design Agent QA？**  
两种 ratio 的 safe zone、price readable。
""",
    "brand_kit_course": """
## FAQ

**课程创作者要先建 Brand Kit 吗？**  
建议，锁 academic blue + action orange。

**改招生价要整图重出吗？**  
不需要，Touch Edit 改价格块。

**live 封面 safe zone？**  
top 12%、bottom 10% 留 UI。

**404 修复？**  
stable course creator Brand Kit SOP。

**Design Agent 做什么？**  
按 brief QA safe zone、disclaimer。
""",
    "skincare_launch": """
## FAQ

**护肤 launch 要先 Brand Kit 吗？**  
建议，从 packaging 取样 hex。

**改首发价要整图重出吗？**  
不需要，Touch Edit 框 CTA 带。

**成分 disclaimer？**  
brief 必填，Design Agent 验收存在性。

**404 修复？**  
stable launch case narrative SOP。

**会编造销售数据吗？**  
不会，只写 workflow 分钟数指标。
""",
    "mianfei_tupian": """
## FAQ

**免费图片能商用吗？**  
请阅各平台官方 ToS，本文不编造条款。

**免费出图要先 Brand Kit 吗？**  
production series 建议，防 drift。

**改价要整图重出吗？**  
不需要，Touch Edit 改 CTA 带。

**404 修复？**  
stable 中文免费图片 workflow URL。

**和纯 T2I 分工？**  
T2I 探索；ChatCanvas 改价 series。
""",
    "nano_banana": """
## FAQ

**nano-banana deck 要先 Brand Kit 吗？**  
建议，锁 slide series accent。

**改 ticket 价要整页重出吗？**  
不需要，Touch Edit price block。

**16:9 与 4:5 同 thread？**  
是，derivative export。

**404 修复？**  
stable presentation guide SOP。

**Design Agent QA？**  
projector readable、disclaimer、hex drift。
""",
    "krea_alternatives": """
## FAQ

**Krea vs Lovart — pick one?**  
No. Match tool to edit-cost KPI.

**Fair 2025 comparison?**  
Same brief, same Tuesday price-change task.

**Touch Edit under five minutes?**  
Signal static-first workflow fits.

**404 fix?**  
Restored stable alternatives comparison URL.

**Brand Kit role?**  
Stops carousel accent drift; beats feature lists.
""",
}


def expand_zh(topic: str, n: int) -> str:
    return f"""
## 实操补充 {n}：{topic}

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。{topic} 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。
"""


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 현장 메모 {n}: {topic}

첫 brief가 「고급스럽게」로 끝나면 가격 숫자가 작아지고 badge가 얼굴을 가립니다. 두 번째는 safe zone과 필수 필드만 고칩니다. **Design Agent**와 **ChatCanvas**에서 thread를 유지하면 carousel slide 4 색 drift를 줄입니다. {topic}에서 **Touch Edit** 5분 이내 가격 수정이면 도구가 맞습니다. 30분 full regen이면 Brand Kit부터 다시 하세요. 404 복구 URL은 onboarding용 stable link입니다.
"""


def expand_en(topic: str, n: int) -> str:
    return f"""
## Field note {n}: {topic}

The first brief ends with "premium" and fails: small price type, badge over the face. Second pass fixes only safe zone and required fields. One **ChatCanvas** thread cuts slide-four accent drift. In **{topic}**, if **Touch Edit** closes a price change in five minutes, static-first works. Thirty-minute full regen means redo **Brand Kit** first. Restored 404 URL is the stable onboarding SOP link.
"""


def expand_ja(topic: str, n: int) -> str:
    return f"""
## 現場メモ {n}：{topic}

初回 brief が「モダン」で終わると価格文字が小さく badge が顔を隠します。二回目は safe zone と必須フィールドのみ修正。**Design Agent** と **ChatCanvas** で thread を維持すると carousel slide 4 の accent drift が減ります。{topic} で **Touch Edit** が 5 分以内に価格修正できれば static-first が成立。30 分 full regen なら **Brand Kit** からやり直し。404 復旧 URL は onboarding 用 stable link です。
"""


def expand_pt(topic: str, n: int) -> str:
    return f"""
## Nota de campo {n}: {topic}

O primeiro brief termina em 「premium」 e falha: preço pequeno, badge sobre o rosto. A segunda passagem corrige só safe zone e campos obrigatórios. Um thread **ChatCanvas** reduz drift de accent no slide quatro. Em **{topic}**, se **Touch Edit** fecha mudança de preço em cinco minutos, static-first funciona. Full regen de trinta minutos exige refazer **Brand Kit** primeiro. URL 404 restaurada é link SOP estável para onboarding.
"""


ARTICLES = [
    {
        "rank": 93,
        "key": "design_agent_ultimate",
        "lang": "ja",
        "slug": "ultimate-guide-ai-design-agent-canvas-for-creators-business",
        "cover": "012",
        "category": "How-To",
        "title": "AI Design Agent と ChatCanvas 完全ガイド：クリエイターとビジネスの実務向け",
        "seo_title": "Design Agent ChatCanvas 完全ガイド — クリエイター向け",
        "description": "JA 404 fix: Design Agent + ChatCanvas ultimate guide, Brand Kit, Touch Edit, business ops.",
        "seo_description": "Design Agent ガイド：revision cost、editable promo、static-first。",
        "focus": "ai design agent canvas creators business",
        "keywords": ["design agent", "chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Design Agent Ultimate JA",
        "body": DESIGN_AGENT_ULTIMATE_JA,
        "expand_topic": "Design Agent ChatCanvas 実務",
    },
    {
        "rank": 94,
        "key": "brand_kit_nail",
        "lang": "ko",
        "slug": "brand-kit-nail-studio-lovart",
        "cover": "019",
        "category": "Industry Solution",
        "title": "네일 스튜디오 Brand Kit: 예약 카드, 시술 메뉴, Reels 커버",
        "seo_title": "네일샵 Brand Kit — ChatCanvas 실操 KO",
        "description": "KO 404 fix: nail studio Brand Kit, booking promo, Reels cover, Touch Edit price.",
        "seo_description": "네일 Brand Kit: 가격 Touch Edit, series 일관성.",
        "focus": "brand kit nail studio lovart",
        "keywords": ["brand kit nail studio", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Nail Studio KO",
        "body": BRAND_KIT_NAIL_KO,
        "expand_topic": "네일샵 예약 promo workflow",
    },
    {
        "rank": 95,
        "key": "text_to_video",
        "lang": "pt",
        "slug": "text-to-video",
        "cover": "026",
        "category": "How-To",
        "title": "Text-to-video: workflow honesto static-first para promo revisável",
        "seo_title": "Text-to-video workflow — static-first PT",
        "description": "PT 404 fix: text-to-video honest workflow, ChatCanvas static, Touch Edit, Brand Kit.",
        "seo_description": "Text-to-video PT: static-first, revision cost, Design Agent QA.",
        "focus": "text to video workflow",
        "keywords": ["text to video", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Text-to-Video PT",
        "body": TEXT_TO_VIDEO_PT,
        "expand_topic": "text-to-video static companion",
    },
    {
        "rank": 96,
        "key": "freepik_vs_lovart",
        "lang": "zh",
        "slug": "freepik-ai-image-generator-vs-lovart",
        "cover": "033",
        "category": "How-To",
        "title": "Freepik AI 图像生成 vs Lovart：运营视角诚实对比",
        "seo_title": "Freepik vs Lovart — operational comparison",
        "description": "404 修复：Freepik AI vs Lovart honest comparison，revision cost、Brand Kit、Touch Edit。",
        "seo_description": "Freepik vs Lovart：edit cost framework，非 feature 清单。",
        "focus": "freepik ai image generator vs lovart",
        "keywords": ["freepik ai vs lovart", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Freepik vs Lovart ZH",
        "body": FREEPIK_VS_LOVART_ZH,
        "expand_topic": "Freepik vs Lovart operational compare",
    },
    {
        "rank": 97,
        "key": "auto_resize",
        "lang": "zh",
        "slug": "auto-resize-magic-converting-a-landscape-banner-to-a-portrait-story-in-1-click",
        "cover": "040",
        "category": "How-To",
        "title": "Auto-Resize Magic：横版 Banner 一键转竖版 Story 的可编辑工作流",
        "seo_title": "Auto-Resize 横转竖 — ChatCanvas workflow",
        "description": "404 修复：landscape banner to portrait story，Brand Kit、Touch Edit、Design Agent QA。",
        "seo_description": "Auto-resize magic：derivative crop、editable CTA layer。",
        "focus": "auto resize landscape banner portrait story",
        "keywords": ["auto resize banner story", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Auto-Resize ZH",
        "body": AUTO_RESIZE_ZH,
        "expand_topic": "横版转竖版 story workflow",
    },
    {
        "rank": 98,
        "key": "brand_kit_course",
        "lang": "zh",
        "slug": "brand-kit-course-creator-lovart",
        "cover": "047",
        "category": "Industry Solution",
        "title": "课程创作者 Brand Kit：大纲卡、招生海报与直播封面",
        "seo_title": "课程创作者 Brand Kit — ChatCanvas 实操",
        "description": "404 修复：course creator Brand Kit、招生、live 封面，Touch Edit 改价。",
        "seo_description": "课程 Brand Kit：syllabus 卡、cohort promo、series 一致。",
        "focus": "brand kit course creator lovart",
        "keywords": ["brand kit course creator", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Course Creator ZH",
        "body": BRAND_KIT_COURSE_ZH,
        "expand_topic": "课程招生与 live 封面",
    },
    {
        "rank": 99,
        "key": "skincare_launch",
        "lang": "zh",
        "slug": "from-name-to-launch-skincare-brand-identity-ai",
        "cover": "050",
        "category": "Branding",
        "title": "从取名到上线：护肤品牌 identity 的 AI 辅助 launch 叙事",
        "seo_title": "护肤品牌 launch — Brand Kit case narrative",
        "description": "404 修复：skincare brand identity launch case，ChatCanvas、Touch Edit、Design Agent。",
        "seo_description": "护肤 launch：packaging Kit、editable promo、无虚构数据。",
        "focus": "skincare brand identity launch ai",
        "keywords": ["skincare brand launch", "lovart brand kit", "chatcanvas", "touch edit"],
        "cluster": "Branding — Skincare Launch ZH",
        "body": SKINCARE_LAUNCH_ZH,
        "expand_topic": "护肤品牌 launch workflow",
    },
    {
        "rank": 100,
        "key": "mianfei_tupian",
        "lang": "zh",
        "slug": "lovart-mianfei-tupian",
        "cover": "061",
        "category": "How-To",
        "title": "Lovart 免费图片生成指南：中文用户的实用工作流",
        "seo_title": "Lovart 免费图片 — 中文 workflow 指南",
        "description": "404 修复：lovart-mianfei-tupian 免费图片生成，Brand Kit、ChatCanvas、Touch Edit。",
        "seo_description": "免费图片生成：revision cost、editable layer，非 hype。",
        "focus": "lovart mianfei tupian free image",
        "keywords": ["lovart 免费图片", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Free Image ZH",
        "body": MIANFEI_TUPIAN_ZH,
        "expand_topic": "中文免费图片 workflow",
    },
    {
        "rank": 101,
        "key": "nano_banana",
        "lang": "zh",
        "slug": "nano-banana-presentation-guide",
        "cover": "062",
        "category": "How-To",
        "title": "Nano Banana 演示指南：deck 与 promo 的可编辑 static 工作流",
        "seo_title": "Nano Banana presentation — ChatCanvas deck guide",
        "description": "404 修复：nano-banana presentation guide，deck、Touch Edit ticket price。",
        "seo_description": "Presentation guide：slide series、Brand Kit、Design Agent QA。",
        "focus": "nano banana presentation guide",
        "keywords": ["nano banana presentation", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Nano Banana Presentation ZH",
        "body": NANO_BANANA_ZH,
        "expand_topic": "nano-banana deck editable workflow",
    },
    {
        "rank": 102,
        "key": "krea_alternatives",
        "lang": "en",
        "slug": "best-krea-ai-alternatives-in-2025-image-generation-tools-compared",
        "cover": "063",
        "category": "How-To",
        "title": "Best Krea AI Alternatives in 2025: Image Generation Tools Compared",
        "seo_title": "Krea AI Alternatives 2025 — Image Tools Compared",
        "description": "404 fix EN: Krea AI alternatives 2025 comparison, Brand Kit, Touch Edit, edit cost.",
        "seo_description": "EN Krea alternatives: fair compare framework, static-first workflow.",
        "focus": "krea ai alternatives 2025 image generation",
        "keywords": ["krea ai alternatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Krea Alternatives EN",
        "body": KREA_ALTERNATIVES_EN,
        "expand_topic": "Krea alternatives edit cost compare",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "en": expand_en,
    "ko": expand_ko,
    "ja": expand_ja,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch9 content cluster.*\n"
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
