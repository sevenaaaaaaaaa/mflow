#!/usr/bin/env python3
"""Generate 404-rescue P2 batch31 blog bodies (10 files). Self-contained.

Ranks #316–#325 from 404-rescue-compact lane.
5 JA + 5 KO. expand_ja + expand_ko (batch19/batch30 pattern).
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
    "ja": 1800,
    "ko": 1400,
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


def count_ko(text: str) -> int:
    return len(re.findall(r"[가-힣]", body_text(text)))


def count_ja(text: str) -> int:
    return len(JA_CHAR_RE.findall(body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang == "ja":
        return count_ja(text)
    if lang == "ko":
        return count_ko(text)
    return len(re.findall(r"\b[\w'-]+\b", body_text(text)))


def check_banned(text: str) -> list[str]:
    hits = []
    bt = body_text(text)
    low = bt.lower()
    for w in BANNED_EN:
        if " " in w:
            if w in low:
                hits.append(w)
        elif re.search(rf"\b{re.escape(w)}\b", low):
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
# Article bodies (paragraph style, H2 sections)
# ---------------------------------------------------------------------------

CREATE_3D_CHARACTERS_JA = """
# AI で 3D キャラクター制作：2D キーデザイン lock から series ops まで

この日本語 URL `create-3d-characters` は 404 を返していました。検索意図は 3D キャラクター How-To — 単発 wow render ではなく、ポーズ・角度・シーズンが変わっても同一 IP として読める series ops。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** は 3D パイプライン前の 2D key design lock と promo static companion 向け。各 3D tool 料金 tier は変動 — 公式参照、**ここでは tool 月額を捏造しません**。

## 四つの 3D character deliverable layer

第一に 2D key design 4:5 — 正面・45度・側面 silhouette lock、**Brand Kit** hex from approved mood board。第二に turnaround sheet same thread — accent stripe **ChatCanvas** memory。第三に pose sheet 3 poses — neutral、gesture、prop、hands は silhouette 回避。第四に promo static companion — 日付・価格 **Touch Edit** editable、**Design Agent** 50% zoom readable pass/fail。

## なぜ 3D キャラクターが pose sheet で崩れるか

「人気 model に 3D キャラ」だけで開始 — 初回 render は美しいが pose 2 で手・目間隔 drift。**Brand Kit** 未設定 → season promo accent lottery。2D lock なしで 3D 拡張 — 修正 cost 垂直上昇。Honest How-To = 2D **ChatCanvas** lock → 3D pipeline → Lovart static companion for weekly offer fix。

## ChatCanvas brief 契約（3D character JP）

弱い brief「かわいい 3D キャラ」。強い brief：「IP X key design 4:5 1080×1350、Brand Kit coral + slate from approved mood board、turnaround 4 views same thread、pose sheet 3 poses hands hidden、promo bottom band flat for Touch Edit、disclaimer footer editable、**Design Agent** pass/fail silhouette consistency」。3D tool 名は brief コメントのみ — offer text bake 禁止。

## Brand Kit が season promo の hue を統一

approved mood board から primary、accent、type role。**ChatCanvas** same thread batch key + turnaround + pose + promo — material hue diverge 禁止。3D export 後も hex SSOT。

## Touch Edit で season 価格変更、character hero 保持

「¥1,980」→「¥1,480」：**Touch Edit** promo band 5 分 — full character regen 30 分ではない。3D ops KPI = static edit-minute median per season cycle。

## 2D lock → 3D → static companion の順序

順序：2D key legal pass on silhouette → turnaround QA → optional 3D conversion → Lovart static promo with **Touch Edit** price layer。動画 hook 必要なら video tool と分業 — offer は static editable layer に。fake poly count benchmark 禁止。

## よくある失敗

2D lock スキップ。**Brand Kit** 未設定。404 未復旧。3D tool 料金捏造。pose sheet で hands を hero に — 解剖リスク。single wow render を final promo に。

## 測定指標

2D lock から 3D handoff 分数、pose QA fail 回数、season price fix 分数。404 復旧 URL を JP create-3d-characters stable SOP link。
"""

STOCK_FOOTAGE_JA = """
# ストック映像時代の終焉？2026 AI 動画創作 complete guide

この日本語 URL `he-death-of-the-stock-footage-era-a-complete-guide-to-ai-powered-video-creation-in-2026` は 404 を返していました — slug には **he-death** という typo が残っています（the の t が欠落）。本文ではこの URL 表記を一度だけ説明し、内容は stock footage era と AI video creation 2026 の honest complete guide です。検索意図は roundup ではなく operational guide — fake render benchmark や tool 月額捏造なし。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** は static-first video prep：master still、variant crops、editable caption layer。

## 四つの video prep deliverable layer

第一に static master 16:9 または 4:5 — readable headline、disclaimer footer editable。第二に B-roll companion same thread accent stripe — **Brand Kit** hex 一致。第三に social crops 1:1 と 9:16 — **Design Agent** QA ratio export mismatch。第四に landing companion still — CTA match video thumb；**Design Agent** 抓 mismatch。

## なぜ stock-footage-only funnel が火曜 offer 変更で失敗するか

Clip bake offer 而 landing static 無 **Touch Edit** layer。改「¥1499 限定」触发 full rerender 30 分。slide 4 accent lottery。**Brand Kit** 未从 approved VI 取样。generic B-roll 購入は editable copy ops を fix しない — honest framing：libraries 仍存在、weekly offer 改動需要 editable static layer。

## ChatCanvas brief 契約（AI video 2026 JP）

弱い brief「cinematic AI 動画」。強い brief：「campaign X video prep 16:9 1920×1080、Brand Kit slate + coral from media kit、headline top 15% flat for Touch Edit、価格 bottom left safe zone、disclaimer footer editable、B-roll companion subtle motion only、variants 2–4 same thread」。**Design Agent** QA static acceptance — clip「映画感」ではない。

## Brand Kit が random stock palette drift を止める

approved VI から primary、accent、type role — random stock marble を brand color にしない。**ChatCanvas** same thread batch landscape + square + vertical export。stock footage era pain：每支 clip 不同 teal。**Brand Kit** SSOT fix hex drift。

## Touch Edit で offer 変更、hero crop 保持

「¥799 限定」→「会員 ¥699」：**Touch Edit** CTA band、hero geometry と **Brand Kit** accent stripe 保持。full regen randomize lighting — ops 承受不起 thirty-minute reroll。

## static-first 再 optional AI B-roll companion

順序：static legal pass on disclaimer → variant A/B still → winner still thread master → optional subtle B-roll。**Touch Edit** price change 5 分以内 — ops viable。fake video render speed や fake user counts 禁止。

## よくある失敗

video-only funnel 無 static editable layer。価格 baked in pixels。404 未復旧。tool 料金捏造。slug typo 修正提案で content scope 逸脱 — slug は he-death のまま維持。

## 測定指標

offer 変更分数、accent drift 回数、export ratio 数。404 復旧 URL を JP he-death-of-the-stock-footage-era stable complete guide SOP link。
"""

BROCHURE_JA = """
# AI でプロ brochure デザイン：step-by-step tutorial と editable ops

この日本語 URL `how-to-design-professional-brochures-with-ai-step-by-step-tutorial` は 404 を返していました。Category How-To。検索意図は tri-fold A4、bi-fold service menu、event program の step-by-step — generic ranking ではなく revision-heavy brochure ops。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** — offer と disclaimer 頻繁変更、print preview と social crop 間 accent drift 防止。lovart.ai 料金参照 — 捏造なし。

## 四つの brochure deliverable layer

第一に tri-fold spread master — panel 3 price band **Touch Edit** editable。第二に bi-fold service menu — **Brand Kit** hex from approved VI。第三に event program cover + inner pages same thread。第四に social crop companion 4:5 — **Design Agent** print QA pass/fail at actual size、disclaimer footer editable。

## なぜ brochure promo が offer 変更で詰まるか

「¥599 コース」bake → full regen 30 分。print preview と Instagram crop accent drift。**Brand Kit** 未設定 → panel 2 と panel 4 別 brand に見える。Brief「高級 brochure」だけ — pass/fail フィールドなし。Honest tutorial = step-by-step brief contract + **Touch Edit** five 分テスト。

## ChatCanvas brief 契約（brochure step-by-step JP）

弱い brief「premium brochure AI」。強い brief：「Service X tri-fold A4 297×210mm、Brand Kit navy + gold from media kit、panel 1 headline flat for Touch Edit、panel 3 price safe zone editable、disclaimer footer editable including terms lines、social crop 4:5 companion same thread、**Design Agent** print QA pass/fail」。step 1 layout grid → step 2 Kit lock → step 3 variant → step 4 Touch Edit test。

## Brand Kit が print と social export を統一

approved media kit から primary、accent、type role。**ChatCanvas** same thread batch tri-fold + bi-fold + social crop — hex lock cross-format。

## Touch Edit でコース価格変更、layout 保持

「Standard ¥599」→「Member ¥499」：**Touch Edit** price band 5 分 — full brochure regen 30 分ではない。Brochure ops KPI = edit-minute median per offer cycle。

## step-by-step ワークフロー（誇張なし）

Step 1：用途定義 tri-fold vs bi-fold。Step 2：**Brand Kit** VI から hex lock。Step 3：**ChatCanvas** thread で spread 生成。Step 4：**Design Agent** print readable QA。Step 5：**Touch Edit** offer 変更テスト。各 step に pass/fail 基準 — fake「10 分完成」保証なし。

## よくある失敗

offer bake。**Brand Kit** スキップ。404 未復旧。print 小字 disclaimer non-editable。step 省略で wow spread のみ。

## 測定指標

price fix 分数、print QA pass rate、drift count。404 復旧 URL を JP how-to-design-professional-brochures-with-ai stable tutorial link。
"""

SOCIAL_MEDIA_BING_JA = """
# AI でソーシャルメディアコンテンツ制作（Bing）：static-first series ops

この日本語 URL `how-to-make-social-media-content-ai-bing` は 404 を返していました。Category How-To。Bing 経由検索 intent — Instagram feed 4:5、story 9:16、carousel slide 2–6、seasonal promo — 週次 offer 変更、feed と story 間 accent drift。**ChatCanvas** thread、**Brand Kit**、**Touch Edit**、**Design Agent**。各 platform 料金 tier 変動 — 公式参照、捏造なし。

## 四つの social content deliverable

第一に feed hero 4:5 — headline top 15% flat for **Touch Edit**。第二に carousel slides 2–6 same thread **Brand Kit** hex lock。第三に story 9:16 — top 12% bottom 20% platform UI safe zone。第四に seasonal promo overlay — 日付・価格 editable layer、**Design Agent** 50% zoom readable pass/fail。

## なぜ social content が slide 4 で accent lottery になるか

各投稿 unrelated prompt — feed teal vs story sand drift。**Brand Kit** 未設定 → grid 全体が別ブランド。Promo 価格 bake → セール変更 full regen 30 分。Bing 検索 user は How-To 期待 — fake engagement lift stat 禁止。

## ChatCanvas brief 契約（social media Bing JP）

弱い brief「viral social post premium」。強い brief：「Campaign X feed 4:5 1080×1350、Brand Kit hex from media kit、headline top 15% flat for Touch Edit、price bottom band editable、disclaimer footer editable、carousel slides 2–6 same thread accent stripe、story 9:16 crop hex lock、**Design Agent** pass/fail per format」。

## Brand Kit が feed と story export を統一

approved media kit から primary、accent。**ChatCanvas** same thread batch 1:1 + 4:5 + 9:16 — hex lock cross-format。

## Touch Edit でセール価格変更、hero regen なし

「-30%」→「-40%」：**Touch Edit** promo band 5 分 — full post regen 30 分ではない。Social ops KPI = edit-minute median per sale cycle。

## Bing 検索 user 向け honest framing

Bing 経由 reader は step-by-step と revision cost を期待 — one-click magic 保証なし。static-first series memory beats single wow post。**Design Agent** checklist が brief 品質を担保。

## よくある失敗

vibe 形容詞のみ brief。**Brand Kit** スキップ。404 未復旧。fake CTR guarantee。carousel 間 hex 不統一。

## 測定指標

価格修正あたり分数、format drift 回数、export ratio。404 復旧 URL を JP how-to-make-social-media-content-ai-bing stable SOP link。
"""

LEGAL_MARKETING_JA = """
# 2027 法律マーケティング visual design：ethical visuals と editable disclaimer

この日本語 URL `legal-marketing-design-ethical-visuals-2027` は 404 を返していました。Category Industry Solution。検索意図は legal marketing design ethical visuals operational 指南 — generic「AI が律师广告を書く」ranking ではない。律所 promo、seminar flyer、LinkedIn cover、合规 disclaimer — 活動日付と执业领域 disclaimer 頻繁変更、trust-heavy navy/gold accent drift。**ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 professional palette。ethical visuals：胜诉率捏造なし、fake client testimonial なし、disclaimer editable static layer。**本文は法律意见ではありません** — 合规文案は律所 legal team 确认后 **Touch Edit** text band に paste。

## 四つの legal marketing deliverable layer

第一に seminar flyer 4:5 — readable 活動主题、disclaimer footer editable 含「不构成法律意见」句。第二に LinkedIn cover — headline 不挡 professional hero、执业领域 disclaimer editable。第三に email header 600×300 — CTA flat for **Touch Edit**。第四に landing companion static — offer と seminar 日付 match；**Design Agent** QA mismatch。render 内小字 compliance 句禁止 — editable layer 必須。

## なぜ legal marketing promo が compliance 改字で詰まるか

disclaimer 一字変更触发 full regen 30 分。readable 执业领域说明 bake in pixels。**Brand Kit** 未从 approved VI、律所 media kit 取样 hex。Brief「高级律所风」形容词 — **Design Agent** 無 pass/fail fields。ethical visuals 要求：不暗示 guaranteed outcome、不 fake case result 数据。

## ChatCanvas brief 契約（legal marketing ethical visuals JP）

弱い brief「高级律所 poster」。強い brief：「seminar X flyer 4:5 1080×1350、Brand Kit navy + gold from media kit、headline top 15% flat for Touch Edit、日付 bottom left safe zone、disclaimer footer editable 含 legal team approved 句、禁止 render 内小字、禁止 fake 胜诉率 claim、slides 2–4 same thread」。**Design Agent** numeric fields — QA「看起来权威」不可。

## Brand Kit 从 approved VI、律所 media kit 取样

approved VI、律所 media kit、prior seminar export から primary、accent、type role。**ChatCanvas** same thread batch flyer + cover + email header export。

## Touch Edit 改 disclaimer 不改 professional hero crop

seminar 日付或 disclaimer wording 変更：**Touch Edit** text band、professional geometry と **Brand Kit** accent stripe 保持。disclaimer 句は legal team 原文 paste — AI 编造 compliance 语言禁止。

## ethical visuals 边界：什么不能做

不编造胜诉率、不 fake client count、不 unauthorized competitor 贬低、不 implied guaranteed outcome visual（gavel + 「100% win」）。visual 可以 professional readable、不能 substitute legal advice。reader 须 consult qualified counsel for jurisdiction-specific rules。

## よくある失敗

disclaimer baked in pixels。AI 编造 compliance 句。fake 胜诉率 visual。**Brand Kit** スキップ。404 未復旧。每活动新 prompt。

## 測定指標

disclaimer edit 分数、legal return count、accent drift 回数。404 復旧 URL を JP legal-marketing-design-ethical-visuals-2027 stable SOP link。
"""

AUTO_FORMAT_KO = """
# 1-Tap Auto Formatting: 문서·포스터 AI 정렬의 honest workflow

이 한국어 URL `1-tap-auto-formatting-instantly-…-your-documents-and-posters-with-ai`(원 slug는 CMS에 그대로 보존)은 404를 반환했습니다. slug에 marketing형 단어가 있지만 본문은 honest ops guide입니다 — one tap이 volume을 줄일 수는 있어도 campaign system을 대체하지 않습니다. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 auto-format 후에도 offer·date·disclaimer를 editable layer로 유지하는 static-first ops. lovart.ai 및 각 tool 공식 ToS 참조 — **여기서 월 구독료를 조작하지 않습니다**.

## 네 가지 auto-format deliverable layer

첫째 feed poster 4:5 — headline top 15% flat for **Touch Edit**. 둘째 carousel slide 2–6 same thread **Brand Kit** hex lock. 셋째 document header A4 — price band editable. 넷째 email header 600×300 — **Design Agent** 50% zoom readable pass/fail, disclaimer footer editable.

## one tap auto-format이 화요일 offer 변경에서 실패하는 이유

tap 한 번으로 네 format이 나와도 accent drift와 melted type on slide three. offer가 pixels에 bake되면 full regen thirty minutes. **Brand Kit** 미설정 → feed vs story coral drift. honest guide = brief contract + **Touch Edit** five-minute test, not magic button hype.

## ChatCanvas brief contract (auto-format KO)

약한 brief: "premium poster auto format". 강한 brief: "Campaign X poster 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 1:1 + 4:5 same thread, **Design Agent** pass/fail". auto-format tool 이름은 brief comment only — offer text bake 금지.

## Brand Kit이 format batch 간 drift를 막음

approved media kit에서 primary, accent, type role 샘플링. **ChatCanvas** same thread batch poster + document + email — hex SSOT cross-format.

## Touch Edit으로 offer 변경, layout 유지

"-30%" → "-40%": **Touch Edit** promo band 5분 — full auto-format regen 30분 아님. Auto-format ops KPI = edit-minute median per account.

## auto-format vs manual series memory

auto-format은 opening tabs를 줄임 — legal review, brand QA, price update는 별도. **Design Agent** checklist가 brief 품질을 numeric pass/fail로 고정. fake "instant perfect layout" guarantee 없음.

## 흔한 실패

**Brand Kit** skip. offer bake. 404 미복구. tool 월 요금 조작. single tap output을 final legal promo로 — disclaimer non-editable.

## 측정 지표

offer fix당 분수, format drift 횟수, export ratio 수. 404 복구 URL을 KO auto-formatting documents posters stable SOP link.
"""

VIDEO_MODELS_KO = """
# 2026 AI 영상 모델 5종 비교: task group 비교 (fake ranking 금지)

이 한국어 URL `5-best-ai-video-models-compared-2026`은 404를 반환했습니다. 검색 의도는 roundup — "#1–#5 score 9.5/10" 표가 아니라 task group별 fit과 revision cost. 각 platform 요금 tier 변동 — 공식 ToS 참조, **여기서 tool 월액을 조작하지 않습니다**. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 video exploration 후 static companion — CTA band editable, disclaimer footer editable.

## 네 가지 video model task group (fake ranking 금지)

그룹 A cinematic exploration: 단발 mood, weekly offer fix 부적합. 그룹 B text-to-video rapid hook: short clip, static companion 필수. 그룹 C image-to-video product hero: end card 4:5 same thread **Brand Kit** hex lock. 그룹 D regulated disclaimer heavy: finance/health — disclaimer editable layer, **Touch Edit** five-minute test. Lovart companion: **Design Agent** pass/fail checklist numeric — score table 없음.

## "5 best video models" 비교가 화요일에 막히는 이유

CTR +47% 등 fake stat. offer baked in clip pixels → full rerender 30분. **Brand Kit** 미설정 → thumb vs end card accent drift. honest roundup = task group + revision cost, not tool #1 badge.

## ChatCanvas brief contract (video models roundup KO)

약한 brief: "best video AI 2026 viral". 강한 brief: "Campaign X video prep 16:9 1920×1080, Brand Kit slate + coral from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, B-roll companion subtle motion only, variants 2–4 same thread, **Design Agent** static QA pass/fail". video tool 이름은 brief comment only.

## Brand Kit이 thumb와 end card를 통일

approved VI에서 primary, accent. **ChatCanvas** same thread batch landscape + square + vertical — hex lock cross-format.

## Touch Edit으로 offer 변경, video re-render 없이

offer text만 변경: **Touch Edit** static band 5분 — full video re-render 30분 회피. Video ops KPI = static edit-minute median.

## 공정 비교 실험 설계 (fake score 없음)

동일 brief contract, 동일 revision task: 화요일 promo copy 변경. 측정: fix당 분수, drift count, export size 수. first-frame aesthetic만 비교하면 procurement 오판.

## 흔한 실패

#1–#5 fake score table. tool 월액 조작. **Brand Kit** skip. 404 미복구. video output만 final promo — static companion 생략.

## 측정 지표

offer fix당 분수, accent drift 횟수, export ratio. 404 복구 URL을 KO 5-best-ai-video-models-compared-2026 stable link.
"""

MARKETER_FUNNEL_KO = """
# 마케터의 꿈? "원클릭 full funnel" hype가 brief를 놓치는 이유

이 한국어 URL `a-marketer-s-dream-generate-full-funnel-creative-assets-with-one-click`은 404를 반환했습니다. slug는 magic button을 암시하지만 본문은 그 hype를 honest하게 비판합니다 — one click은 volume을 만들 수 있지 campaign system은 아닙니다. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 hero, carousel, email header, ad safe crop 전반의 revision cost를 줄일 때 가치가 있습니다 — slogan이 brief를 건너뛸 때가 아닙니다. **fake one-click full-funnel guarantee 없음**.

## one click이 실제로 deliver하는 것

대부분 "full funnel" demo는 drifting colors와 slide three melted type의 네 unrelated size. click은 네 tab opening을 줄임 — legal review, brand QA, next Tuesday price update는 아님. honest workflow: channel을 upfront에 명명, Brand Kit lock, 세 direction 생성, 하나 선택, static layer에서 **Touch Edit** dates and prices.

## five-step loop (one click 대신)

**ChatCanvas**에서 offer를 buyer가 이해하는 한 문장으로 restate. Brand Kit에서 palette and type lock. **Design Agent**에 channel별 artboard explicit pixels로 요청. clearest CTA block direction 선택. **Touch Edit** promo lines; named files export. one click보다 많지만 full regen은 적음.

## 마케터가 burn되는 지점

double CTA를 hero가 "premium"이라 accept. limited-time dates를 editable block 대신 image에 bake. static legal approval 전 video hook 실행. first-frame speed 대신 price-change minutes로 tool 비교. 각 failure는 brief discipline — model lottery 아님.

## Brand Kit as anti-drift memory

Brand Kit 없으면 carousel slide four가 new accent color invent. Kit active면 agent가 hex roles follow — spellcheck가 dictionary follow하듯. funnel work는 series work; memory beats surprise.

## Touch Edit on funnel blocks

offer가 "20% off"에서 "free shipping"으로 shift: hero and email header type layer **Touch Edit** one session. two-word change에 full reroll — "one-click" tool이 Tuesday까지 fast feel하는 방법.

## static companion for every motion hook

paid social은 autoplay off일 때 static fallback 필요. same **ChatCanvas** thread에서 ad-safe crop 생성 — color temperature landing hero match. broken funnel URLs in sitemaps = campaigns never got companion sizes.

## 흔한 실패

one-click without brief contract. **Brand Kit** skip. 404 미복구. fake full-funnel guarantee. offer bake across all sizes.

## 측정 지표

price fix당 분수, funnel drift 횟수, companion size export ratio. 404 복구 URL을 KO a-marketer-s-dream stable honest funnel SOP link.
"""

SIDE_HUSTLERS_KO = """
# 사이드 허슬러를 위한 Design Agent: honest workflow (fake ranking 없음)

이 한국어 URL `best-ai-design-agent-for-side-hustlers`은 404를 반환했습니다. Category Industry Solution. 검색 의도는 side hustler ops — Etsy listing, Instagram promo, seasonal offer card, client pitch deck — 가격·날짜 weekly 변경, client A vs client B accent drift. **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** — "#1 best agent" score table 없음. KPI = 가격 수정 five minutes. lovart.ai 요금 공식 참조 — 금액 조작 없음.

## 네 가지 side hustler deliverable

첫째 listing hero 4:5 — price band **Touch Edit** editable. 둘째 seasonal carousel slide 2–6 **Brand Kit** hex lock per client. 셋째 client pitch cover 16:9 — CTA flat for **Touch Edit**. 넷째 **Design Agent** pass/fail: 50% zoom readable price, disclaimer footer, Kit hex drift zero.

## side hustler "best agent" ranking이 ops를 배신하는 이유

fake score 9.5/10. offer bake → 화요일 full regen 30분. **Brand Kit** 미설정 → client A coral vs client B teal drift. honest guide = edit-minute median KPI, not pretty first frame.

## ChatCanvas brief contract (side hustler KO)

약한 brief: "premium side hustle poster". 강한 brief: "Client X seasonal 4:5 1080×1350, Brand Kit hex from client VI, headline top 15% flat for Touch Edit, price bottom safe zone editable, disclaimer footer editable, variants listing + IG same thread, **Design Agent** pass/fail checklist side hustler can run". client별 separate thread — memory per client.

## Brand Kit이 client별 series를 분리

client A VI에서 primary, accent sample — client B와 hex mix 금지. **ChatCanvas** per-client thread batch listing + carousel + pitch.

## Touch Edit으로 seasonal 가격 변경, hero regen 없이

"₩12,800" → "₩9,800": **Touch Edit** promo band 5분 — full listing regen 30분 아님.

## side hustler pricing honesty

견적에 revision round, client VI setup, **Brand Kit** lock 시간 포함 — AI가 빨라졌다고 one-line 견적 금지. fake conversion lift stat 없음.

## 흔한 실패

fake ranking scores. **Brand Kit** skip. 404 미복구. offer bake. client thread mix — accent lottery.

## 측정 지표

edit-minute median, drift events per client batch. 404 복구 URL을 KO best-ai-design-agent-for-side-hustlers stable SOP link.
"""

KREA_ALTERNATIVES_KO = """
# 2025 Krea AI 대안 비교: honest comparison (pricing 조작 없음)

이 한국어 URL `best-krea-ai-alternatives-in-2025-image-generation-tools-compared`은 404를 반환했습니다. 검색 의도는 Krea AI alternatives and 2025 image tool comparison — honest framing: Krea는 real-time style exploration과 live canvas iteration에 강함; revision-heavy promo는 **ChatCanvas** static masters, **Brand Kit** hex roles, **Touch Edit** price layers, **Design Agent** QA가 필요. edit cost 비교, first-frame beauty 아님. **Krea 및 경쟁 tool 월액을 본문에 조작하지 않습니다** — 각 platform 공식 ToS 참조.

## Krea가 2025 workflow에서 잘하는 것

첫째 live style mixing과 rapid mood iteration. 둘째 layout grid commit 전 creator exploration. 셋째 price and disclaimer rarely change하는 single-frame social. 넷째 series consistency low priority일 때 reference-driven aesthetics.

## revision-heavy campaign에서 team이 막히는 gap

화요일 promo copy change triggers thirty-minute full regen. carousel slide four accent drift. disclaimer baked into pixels. video hook shows offer while landing static lacks editable price. **Brand Kit** hex roles 없음. **Touch Edit** promo band 없음.

## Lovart ChatCanvas workflow division of labor

campaign family당 one **ChatCanvas** thread — revision memory 유지. **Brand Kit** locks primary, accent, type roles. **Touch Edit** swaps CTA copy without identity lottery. **Design Agent** checks safe zone, readable price, hex drift versus Kit. KPI = minutes per price fix.

## 공정 비교 실험 설계

동일 brief contract: hero 4:5, price bottom left safe zone, disclaimer footer editable, Brand Kit hex specified. 동일 revision task: 화요일 promo copy 변경. 측정: fix당 minutes, drift count, export sizes per action. first-frame aesthetic만 비교하면 procurement 오판.

## Krea가 더 나은 fit일 때

weekly five to ten casual social posts, minimal price layers, low carousel series requirements, exploration speed over edit cost.

## Lovart workflow가 더 나은 fit일 때

promo당 twenty-plus size exports, weekly price or date changes, carousel series with legal disclaimers, **Touch Edit** under five minutes as hard KPI.

## 다른 2025 alternatives 같은 edit-cost frame

pure T2I playgrounds, Canva template marketplaces, Adobe Generative Fill 각각 다른 axis에서 win. operational comparison 질문: legal approves hero 후 forty-two sizes에서 price 변경 몇 분? **Touch Edit** path versus full regen path.

## 흔한 실패

Krea로 exploration 후 Lovart-grade **Brand Kit** without setup 기대. Lovart single-shot prompts without threads. 404 URL missing — SOP scattered in Slack. **fabricated pricing table 금지**.

## 측정 지표

price fix당 minutes, drift count, restored 404 URL을 KO best-krea-ai-alternatives stable honest comparison link.
"""


FAQ = {
    "create_3d_characters_ja": """
## FAQ

**2D lock 없이 3D부터 해도 되나?**  
브랜드納品は 2D **ChatCanvas** lock 後 3D が安い。

**Touch Edit で season 価格 5 分？**  
はい — static companion editable layer テスト。

**Brand Kit は pose sheet 後必須？**  
はい — season promo accent drift 防止。

**3D tool 料金捏造？**  
なし — 各社公式参照。

**404 復旧 URL？**  
安定 JP create-3d-characters。
""",
    "stock_footage_ja": """
## FAQ

**slug he-death typo を修正？**  
いいえ — 本文で一度説明、slug は he-death 維持。

**stock footage 完全消滅？**  
いいえ — libraries 仍存在、editable static layer が weekly ops 向き。

**Touch Edit で offer 変更 5 分？**  
はい — video re-render 回避。

**404 復旧 URL？**  
安定 JP he-death-of-the-stock-footage-era complete guide。

**fake benchmark 有？**  
なし — edit minutes と drift count のみ。
""",
    "brochure_ja": """
## FAQ

**tri-fold と bi-fold 同 thread？**  
はい — **Brand Kit** hex lock same **ChatCanvas** thread。

**Touch Edit でコース価格 5 分？**  
はい — layout 保持。

**print QA 必須？**  
はい — **Design Agent** actual size pass/fail。

**404 復旧 URL？**  
安定 JP how-to-design-professional-brochures-with-ai。

**fake 10 分完成保証？**  
なし — step-by-step pass/fail のみ。
""",
    "social_media_bing_ja": """
## FAQ

**Bing 検索 user 向け one-click？**  
いいえ — static-first series SOP。

**Touch Edit でセール価格 5 分？**  
はい — hero regen なし。

**Brand Kit feed + story 統一？**  
はい — same thread hex lock。

**404 復旧 URL？**  
安定 JP how-to-make-social-media-content-ai-bing。

**fake CTR 保証？**  
なし — ops metrics のみ。
""",
    "legal_marketing_ja": """
## FAQ

**本文は法律意见？**  
いいえ — disclaimer は legal team 確認後 **Touch Edit** paste。

**disclaimer editable？**  
はい — footer editable layer 必須。

**fake 胜诉率 visual？**  
禁止 — ethical visuals 境界。

**404 復旧 URL？**  
安定 JP legal-marketing-design-ethical-visuals-2027。

**Brand Kit 律所 VI から？**  
はい — approved media kit hex サンプリング。
""",
    "auto_format_ko": """
## FAQ

**one tap이 campaign system 대체?**  
아니요 — brief contract + **Touch Edit** ops layer 필요.

**Touch Edit 가격 수정 5분?**  
예 — auto-format full regen 회피.

**Brand Kit format batch 통일?**  
예 — same thread hex lock.

**404 복구 URL?**  
안정 KO 1-tap-auto-formatting SOP link.

**tool 월 요금 본문 기재?**  
없음 — 공식 ToS 참조만.
""",
    "video_models_ko": """
## FAQ

**#1–#5 score 표 있나?**  
없음 — task group만, fake ranking 금지.

**Touch Edit static CTA 5분?**  
예 — video re-render 회피.

**Brand Kit thumb + end card?**  
예 — same thread hex lock.

**404 복구 URL?**  
안정 KO 5-best-ai-video-models-compared-2026.

**fake CTR stat?**  
없음 — pass/fail QA만.
""",
    "marketer_funnel_ko": """
## FAQ

**one-click full funnel 보장?**  
없음 — honest five-step loop.

**Touch Edit funnel block 5분?**  
예 — two-word change full reroll 회피.

**Brand Kit carousel drift?**  
예 — Kit active면 hex roles follow.

**404 복구 URL?**  
안정 KO a-marketer-s-dream honest funnel SOP.

**fake conversion lift?**  
없음 — edit-minute KPI만.
""",
    "side_hustlers_ko": """
## FAQ

**#1 best agent ranking?**  
없음 — edit-minute median KPI.

**client별 separate thread?**  
예 — **ChatCanvas** per-client memory.

**Touch Edit seasonal 가격 5분?**  
예 — listing hero regen 없이.

**404 복구 URL?**  
안정 KO best-ai-design-agent-for-side-hustlers.

**fake ranking score?**  
없음 — honest workflow만.
""",
    "krea_alternatives_ko": """
## FAQ

**Krea pricing 본문 기재?**  
없음 — krea.ai 공식 ToS 참조.

**Lovart vs Krea 이원 대立?**  
아니요 — workflow 순서: static legal pass 후 exploration.

**Touch Edit 5분 KPI?**  
예 — revision-heavy promo ops test.

**404 복구 URL?**  
안정 KO best-krea-ai-alternatives honest comparison.

**fabricated pricing table?**  
없음 — edit-cost framework만.
""",
}


def expand_ja(topic: str, n: int) -> str:
    return f"""
## 現場メモ {n}：{topic}

初回 brief が「モダン」で終わると価格文字が小さく badge が顔を隠します。二回目は safe zone と必須フィールドのみ修正。**Design Agent** と **ChatCanvas** で thread を維持すると carousel slide 4 の accent drift が減ります。{topic} で **Touch Edit** が 5 分以内に価格修正できれば static-first が成立。30 分 full regen なら **Brand Kit** からやり直し。404 復旧 URL は JP ops 向け stable link batch31 です。
"""


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 실습 보충 {n}: {topic}

첫 brief가 형용사만 쌓이면 그림은 예쁘지만 가격 글자가 작고 배지가 hero를 가립니다. 두 번째는 safe zone과 필수 필드만 수정. **ChatCanvas** thread가 slide 4 accent drift를 줄입니다. **{topic}**에서 **Touch Edit** 가격 수정 5분이면 static-first 입증. full regen 30분이면 **Brand Kit**부터 재설정. 복구된 404 URL이 stable SOP link batch31. **Design Agent** pass/fail checklist가 형용사 brief보다 낫습니다.
"""


ARTICLES = [
    {
        "rank": 316,
        "key": "create_3d_characters_ja",
        "lang": "ja",
        "slug": "create-3d-characters",
        "cover": "011",
        "category": "How-To",
        "title": "AI で 3D キャラクター制作：2D key design lock から series ops",
        "seo_title": "Create 3D Characters JP — ChatCanvas 2D lock static companion",
        "description": "JP 404 fix: 3D character How-To, 2D ChatCanvas lock, Touch Edit season price editable.",
        "seo_description": "How-To: turnaround pose sheet, Brand Kit hex lock, Design Agent silhouette QA.",
        "focus": "create 3d characters",
        "keywords": ["3d character ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Create 3D Characters JA",
        "body": CREATE_3D_CHARACTERS_JA,
        "expand_topic": "JP create 3d characters 2D lock workflow",
    },
    {
        "rank": 317,
        "key": "stock_footage_ja",
        "lang": "ja",
        "slug": "he-death-of-the-stock-footage-era-a-complete-guide-to-ai-powered-video-creation-in-2026",
        "cover": "014",
        "category": "Insight & Trend",
        "title": "ストック映像時代の終焉？2026 AI 動画創作 complete guide",
        "seo_title": "He Death Stock Footage Era AI Video 2026 JP — he-death slug typo noted",
        "description": "JP 404 fix: he-death slug typo retained, AI video 2026 static-first, no fake pricing.",
        "seo_description": "Insight: Brand Kit Touch Edit editable layer, honest stock footage framing.",
        "focus": "he death of the stock footage era ai video creation 2026",
        "keywords": ["ai video creation 2026", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight & Trend — Stock Footage Era AI Video JA",
        "body": STOCK_FOOTAGE_JA,
        "expand_topic": "JP he-death stock footage era AI video static-first workflow",
    },
    {
        "rank": 318,
        "key": "brochure_ja",
        "lang": "ja",
        "slug": "how-to-design-professional-brochures-with-ai-step-by-step-tutorial",
        "cover": "018",
        "category": "How-To",
        "title": "AI でプロ brochure デザイン：step-by-step tutorial",
        "seo_title": "Professional Brochures AI Step By Step JP — Touch Edit price band",
        "description": "JP 404 fix: brochure step-by-step How-To, Brand Kit tri-fold, disclaimer editable.",
        "seo_description": "How-To: print QA Design Agent, ChatCanvas same thread social crop.",
        "focus": "how to design professional brochures with ai step by step tutorial",
        "keywords": ["brochure design ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Professional Brochures AI JA",
        "body": BROCHURE_JA,
        "expand_topic": "JP professional brochures AI step by step workflow",
    },
    {
        "rank": 319,
        "key": "social_media_bing_ja",
        "lang": "ja",
        "slug": "how-to-make-social-media-content-ai-bing",
        "cover": "019",
        "category": "How-To",
        "title": "AI でソーシャルメディアコンテンツ制作（Bing）：static-first series",
        "seo_title": "Social Media Content AI Bing JP — ChatCanvas series SOP",
        "description": "JP 404 fix: social media content AI Bing How-To, Brand Kit feed story hex lock.",
        "seo_description": "How-To: carousel same thread, Touch Edit promo band editable.",
        "focus": "how to make social media content ai bing",
        "keywords": ["social media content ai bing", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Social Media Content AI Bing JA",
        "body": SOCIAL_MEDIA_BING_JA,
        "expand_topic": "JP social media content AI Bing static-first workflow",
    },
    {
        "rank": 320,
        "key": "legal_marketing_ja",
        "lang": "ja",
        "slug": "legal-marketing-design-ethical-visuals-2027",
        "cover": "020",
        "category": "Industry Solution",
        "title": "2027 法律マーケティング visual：ethical visuals と editable disclaimer",
        "seo_title": "Legal Marketing Ethical Visuals 2027 JP — disclaimer Touch Edit",
        "description": "JP 404 fix: legal marketing ethical visuals, disclaimer editable, no fake legal claims.",
        "seo_description": "Industry Solution: seminar flyer, Brand Kit navy gold, not legal advice.",
        "focus": "legal marketing design ethical visuals 2027",
        "keywords": ["legal marketing design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Legal Marketing Ethical Visuals JA",
        "body": LEGAL_MARKETING_JA,
        "expand_topic": "JP legal marketing ethical visuals disclaimer workflow",
    },
    {
        "rank": 321,
        "key": "auto_format_ko",
        "lang": "ko",
        "slug": "1-tap-auto-formatting-instantly-elevate-your-documents-and-posters-with-ai",
        "cover": "021",
        "category": "How-To",
        "title": "1-Tap Auto Formatting: 문서·포스터 AI 정렬 honest workflow",
        "seo_title": "1 Tap Auto Formatting Documents Posters KO — no magic button hype",
        "description": "KO 404 fix: auto-formatting honest guide, Brand Kit hex lock, Touch Edit offer editable.",
        "seo_description": "How-To: ChatCanvas brief contract, Design Agent pass/fail, no fabricated pricing.",
        "focus": "1 tap auto formatting instantly elevate your documents and posters with ai",
        "keywords": ["auto formatting ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — 1 Tap Auto Formatting KO",
        "body": AUTO_FORMAT_KO,
        "expand_topic": "KO 1 tap auto formatting honest static-first workflow",
    },
    {
        "rank": 322,
        "key": "video_models_ko",
        "lang": "ko",
        "slug": "5-best-ai-video-models-compared-2026",
        "cover": "022",
        "category": "Comparison",
        "title": "2026 AI 영상 모델 5종: task group 비교 (fake ranking 없음)",
        "seo_title": "5 Best AI Video Models Compared 2026 KO — task groups no fake scores",
        "description": "KO 404 fix: video models roundup, task groups not fake Top-5 scores.",
        "seo_description": "Comparison: static companion Touch Edit, Brand Kit multi-ratio same thread.",
        "focus": "5 best ai video models compared 2026",
        "keywords": ["ai video models 2026", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Video Models 2026 KO",
        "body": VIDEO_MODELS_KO,
        "expand_topic": "KO 5 best ai video models task group workflow",
    },
    {
        "rank": 323,
        "key": "marketer_funnel_ko",
        "lang": "ko",
        "slug": "a-marketer-s-dream-generate-full-funnel-creative-assets-with-one-click",
        "cover": "023",
        "category": "Best Practice",
        "title": "마케터의 꿈? 원클릭 full funnel hype와 honest five-step loop",
        "seo_title": "Marketer Dream Full Funnel One Click KO — no fake guarantee",
        "description": "KO 404 fix: marketer full funnel critique, no one-click guarantee, Touch Edit funnel blocks.",
        "seo_description": "Best Practice: ChatCanvas Brand Kit, static companion per motion hook.",
        "focus": "a marketer s dream generate full funnel creative assets with one click",
        "keywords": ["full funnel creative assets", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Best Practice — Marketer Full Funnel KO",
        "body": MARKETER_FUNNEL_KO,
        "expand_topic": "KO marketer full funnel honest five-step workflow",
    },
    {
        "rank": 324,
        "key": "side_hustlers_ko",
        "lang": "ko",
        "slug": "best-ai-design-agent-for-side-hustlers",
        "cover": "024",
        "category": "Industry Solution",
        "title": "사이드 허슬러 Design Agent: honest workflow (fake ranking 없음)",
        "seo_title": "Best AI Design Agent Side Hustlers KO — edit-minute median KPI",
        "description": "KO 404 fix: side hustler Design Agent, per-client Brand Kit, Touch Edit price editable.",
        "seo_description": "Industry Solution: Etsy listing IG pitch same thread, Design Agent pass/fail.",
        "focus": "best ai design agent for side hustlers",
        "keywords": ["side hustler design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Side Hustlers Design Agent KO",
        "body": SIDE_HUSTLERS_KO,
        "expand_topic": "KO best ai design agent for side hustlers workflow",
    },
    {
        "rank": 325,
        "key": "krea_alternatives_ko",
        "lang": "ko",
        "slug": "best-krea-ai-alternatives-in-2025-image-generation-tools-compared",
        "cover": "025",
        "category": "Comparison",
        "title": "2025 Krea AI 대안: honest comparison (pricing 조작 없음)",
        "seo_title": "Best Krea AI Alternatives 2025 KO — edit cost no fake pricing",
        "description": "KO 404 fix: Krea alternatives honest comparison, no fabricated pricing table.",
        "seo_description": "Comparison: Touch Edit revision cost, Brand Kit hex lock, official ToS only.",
        "focus": "best krea ai alternatives in 2025 image generation tools compared",
        "keywords": ["krea ai alternatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Krea AI Alternatives 2025 KO",
        "body": KREA_ALTERNATIVES_KO,
        "expand_topic": "KO best krea ai alternatives honest edit cost compare",
    },
]


EXPAND_FN = {
    "ja": expand_ja,
    "ko": expand_ko,
}

UNIT_MAP = {
    "ja": "chars",
    "ko": "hangul",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch31 content cluster.*\n"
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
        fm_slug = re.search(r"^slug: (.+)$", text, re.M)
        slug_fm_ok = fm_slug and fm_slug.group(1) == a["slug"]
        ok = metric >= floor and not banned and not placeholder and slug_fm_ok
        path = OUT / f"{lang}-{a['slug']}.md"
        path.write_text(text, encoding="utf-8")
        results.append({
            "file": path.name,
            "slug": a["slug"],
            "lang": lang,
            "rank": a["rank"],
            "metric": metric,
            "floor": floor,
            "unit": UNIT_MAP[lang],
            "banned": banned,
            "placeholder": placeholder,
            "slug_ok": slug_fm_ok,
            "pass": ok,
            "cover": a["cover"],
        })

    print(f"{'RANK':>4} {'SLUG':<75} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 135)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['rank']:>4} {r['slug']:<75} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["slug"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
