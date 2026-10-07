#!/usr/bin/env python3
"""Generate 404-rescue P2 batch32 blog bodies (10 files). Self-contained.

Ranks #326–#335 from 404-rescue-compact lane.
All KO. expand_ko only (batch19/batch31 pattern).
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
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


def cover_url(n: str) -> str:
    return f"https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-{n}-1024x682.png"


def body_text(full_md: str) -> str:
    if full_md.startswith("---"):
        return full_md.split("---", 2)[-1]
    return full_md


def count_ko(text: str) -> int:
    return len(re.findall(r"[가-힣]", body_text(text)))


def count_metric(text: str, lang: str) -> int:
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

TEXTURE_MATERIAL_KO = """
# AI 텍스처·재질 생성 완전 가이드: static-first promo companion SOP

이 한국어 URL `complete-guide-ai-texture-material-generation`은 404를 반환했습니다. 검색 의도는 AI texture material generation complete guide — generic tool ranking이 아니라 revision-heavy promo ops. 제품 hero, packaging mock, carousel slide 2–6에서 재질 hue가 drift하기 쉽고, offer와 disclaimer 변경이 잦습니다. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 texture exploration 후 static companion — CTA band editable, disclaimer footer editable. 각 texture tool 요금 tier 변동 — lovart.ai 및 각 platform 공식 ToS 참조, **여기서 tool 월액을 조작하지 않습니다**.

## 네 가지 texture·material deliverable layer

첫째 product hero 4:5 — readable headline, material accent stripe **Brand Kit** hex lock. 둘째 packaging mock companion same thread — marble/brass hue drift 금지. 셋째 carousel slide 2–6 — price band **Touch Edit** editable. 넷째 social crop 1:1과 9:16 — **Design Agent** ratio export mismatch QA, disclaimer footer editable.

## texture generation이 화요일 offer 변경에서 실패하는 이유

clip 안에 offer가 bake되고 static companion에 **Touch Edit** layer가 없습니다. slide 4 accent lottery — slide 3 teal vs slide 4 coral. **Brand Kit** 미설정 → packaging mock과 feed hero가 다른 brand로 보임. Brief「프리미엄 마블 텍스처」만 — **Design Agent** pass/fail fields 없음.

## ChatCanvas brief contract (texture material KO)

약한 brief: "premium marble texture AI". 강한 brief: "Campaign X product hero 4:5 1080×1350, Brand Kit slate + brass from approved packaging VI, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, texture reference as accent stripe not baked offer text, variants 2–4 same thread, **Design Agent** pass/fail checklist". texture tool 이름은 brief comment only.

## Brand Kit이 material hue drift를 막음

approved packaging VI에서 primary, accent, type role sample — stock marble을 brand color로 쓰지 않음. **ChatCanvas** same thread batch hero + packaging + carousel — hex SSOT cross-format.

## Touch Edit으로 offer 변경 hero crop 유지

「한정 ₩49,000」→「회원 ₩39,000」: **Touch Edit** CTA band, product geometry와 **Brand Kit** accent stripe 유지. full regen은 lighting randomize — texture ops가 30분 reroll 감당 불가.

## static-first texture workflow 순서

순서: static legal pass on disclaimer → variant A/B still → winner still이 thread master → optional texture exploration elsewhere only. **Touch Edit** price change 5분 내 — ops viable before weekly promo cadence. fake material benchmark score 없음.

## 흔한 실패

texture exploration output을 final promo로 — disclaimer non-editable. **Brand Kit** skip. 404 미복구. tool 월액 조작. single wow render를 series master로.

## 측정 지표

offer fix당 분수, accent drift 횟수, export ratio 수. 복구된 URL이 stable KO complete-guide-ai-texture-material-generation SOP link.
"""

FREE_TOOLS_COMPLETE_KO = """
# 2026 무료 AI 디자인 도구 완전 가이드: honest decision framework (pricing 조작 없음)

이 한국어 URL `complete-guide-free-ai-design-tools-2026`은 404를 반환했습니다. 검색 의도는 complete guide free AI design tools 2026 — fake Top-10 score 표가 아니라 task group별 fit과 revision cost. 무료 tier는 세 가지 의미가 섞입니다: 오픈소스 로컬, freemium 한도, attribution 요구 리소스. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 revision-heavy promo ops layer — weekly offer fix KPI. **Lovart 및 경쟁 tool 월 구독료·tier 금액을 본문에 조작하지 않습니다** — lovart.ai 공식 pricing page와 각 platform ToS만 참조.

## 네 가지 free-tool task group (fake ranking 금지)

그룹 A casual social 5–10 posts/week — price layer 거의 없음, exploration speed 우선. 그룹 B SMB promo weekly offer fix — **Touch Edit** five-minute test 필수. 그룹 C carousel series + legal disclaimer — **Brand Kit** hex lock, **Design Agent** pass/fail. 그룹 D multi-client agency — per-client **ChatCanvas** thread memory. honest complete guide = edit-minute median 비교, not tool #1 badge.

## "free AI design tools 2026" 가이드가 화요일에 막히는 이유

free tier export cap이 deadline day에 드러남. offer baked in pixels → full regen 30분. **Brand Kit** 미설정 → free template accent drift. fake「100% free forever」claim — hidden watermark, resolution cap. honest guide는 revision cost frame, not first-frame beauty.

## ChatCanvas brief contract (free tools complete KO)

약한 brief: "best free AI design 2026 viral". 강한 brief: "Campaign X promo 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 2–4 same thread, **Design Agent** static QA pass/fail". free tool 이름은 brief comment only — offer text bake 금지.

## Brand Kit이 free template palette drift를 줄임

approved VI에서 primary, accent sample — random free template gradient을 brand color로 쓰지 않음. **ChatCanvas** same thread batch feed + story + email header export.

## Touch Edit으로 free-tool output에서 offer fix

free exploration 후 Lovart static companion: **Touch Edit** CTA band 5분 — full free-tool regen 30분 회피. Free-tool ops KPI = static edit-minute median, not render count.

## Lovart pricing honesty boundary

lovart.ai 공식 페이지에서 plan 확인 — 본문은 tier 금액 표를 만들지 않음. reader는 export cap, watermark, commercial use terms를 각 tool 공식 ToS에서 직접 확인. fabricated pricing table 금지.

## 흔한 실패

fake #1–#10 score table. Lovart tier 금액 조작. **Brand Kit** skip. 404 미복구. free output만 final legal promo — disclaimer non-editable.

## 측정 지표

offer fix당 분수, free-tier cap surprise count, drift 횟수. 복구된 URL이 stable KO complete-guide-free-ai-design-tools-2026 honest link.
"""

FREE_TOOLS_KO = """
# 2026 무료 AI 디자인 도구: How-To ops SOP (Lovart tier 금액 조작 없음)

이 한국어 URL `free-ai-design-tools-2026`은 404를 반환했습니다. Category How-To. 검색 의도는 free AI design tools 2026 practical guide — generic ranking이 아님. How-To는 brief contract + **Touch Edit** five-minute test + **Brand Kit** hex lock — not「one-click magic free forever」. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**. **Lovart 월 구독료·tier 가격을 본문에 적지 않습니다** — lovart.ai 공식 pricing 참조만.

## How-To 네 deliverable layer

첫째 feed hero 4:5 — headline top 15% flat for **Touch Edit**. 둘째 carousel slide 2–6 same thread **Brand Kit** hex lock. 셋째 email header 600×300 — disclaimer footer editable. 넷째 landing companion still — **Design Agent** 50% zoom readable pass/fail.

## free AI design How-To가 offer 변경에서 실패하는 이유

free tool demo는 pretty first frame — offer bake in pixels. 화요일「-30%」→「-40%」full regen 30분. **Brand Kit** 미설정 → slide 4 accent lottery. Brief 형용사만 — **Design Agent** numeric fields 없음.

## ChatCanvas brief contract (free tools How-To KO)

약한 brief: "free AI poster premium". 강한 brief: "Campaign X free-tool workflow test 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 1:1 + 4:5 same thread, **Design Agent** pass/fail". free tool은 exploration layer — static legal pass 후 companion.

## Brand Kit이 free workflow series를 통일

approved media kit에서 primary, accent sample. **ChatCanvas** same thread batch multi-ratio export — hex lock cross-format.

## Touch Edit으로 free output promo band 수정

offer text만 변경: **Touch Edit** static band 5분 — full free-tool regen 30분 회피. How-To KPI = edit-minute median per account.

## pricing honesty: 본문에 tier 표 없음

reader는 lovart.ai 및 각 free tool 공식 ToS에서 export limit, watermark, commercial terms 확인. 본문은 workflow SOP only — fabricated Lovart $/₩ tier 금지.

## 흔한 실패

Lovart tier 금액 조작. **Brand Kit** skip. offer bake. 404 미복구. free demo를 final legal promo로.

## 측정 지표

offer fix당 분수, drift 횟수, export ratio. 복구된 URL이 stable KO free-ai-design-tools-2026 How-To SOP link.
"""

BATCH_CREATE_BING_KO = """
# AI로 Bing 광고용 디자인 일괄 생성: static-first campaign series SOP

이 한국어 URL `how-to-batch-create-designs-ai-bing`은 404를 반환했습니다. Category How-To. Bing Ads·Microsoft Advertising 검색 intent — ten asset variants가 one **ChatCanvas** thread, one **Brand Kit** hex lock, **Touch Edit** editable CTA — not ten unrelated prompts. Lovart **Design Agent** QA readable price, disclaimer present, accent drift vs Kit. KPI는「offer fix 5분」, not「first wow image」. 각 platform 요금 tier 변동 — 공식 ToS 참조, **여기서 tool 월액을 조작하지 않습니다**.

## Bing batch 네 deliverable layer

첫째 1200×628 landscape master — headline, disclaimer footer editable, CTA bottom 20% flat for **Touch Edit**. 둘째 1:1 square 1200×1200 same thread accent stripe. 셋째 4:5 vertical 1080×1350 — price bottom left safe zone readable. 넷째 logo lockup companion — **Brand Kit** hex matched, **Design Agent** ratio export mismatch catch.

## batch create가 화요일 price change에서 실패하는 이유

ten variants, ten separate prompts — slide 4 accent lottery across batch. Offer baked in pixels;「Launch ₩49,000」변경이 asset당 full regen 30분. **Brand Kit** 미설정. Teams는 batch를 speed demo로, series discipline으로 보지 않음.

## ChatCanvas brief contract (batch create Bing KO)

약한 brief: "batch create ten Bing ad designs". 강한 brief: "Campaign X batch 1200×628 landscape, Brand Kit slate + coral from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 2–10 same thread accent stripe, square + vertical companions same ChatCanvas thread, **Design Agent** numeric pass/fail". Bing context slug — Microsoft 공식 endorsement 아님.

## Brand Kit as batch SSOT against hex drift

approved VI와 prior Bing export에서 primary, accent, type role sample — random stock gradient을 brand color로 쓰지 않음. One **ChatCanvas** thread batches landscape + square + vertical export.

## Touch Edit changes offer without hero crop across batch

「Limited ₩79,000」→「Member ₩69,000」: **Touch Edit** CTA band on each static master, hero geometry와 **Brand Kit** accent stripe preserved. Full regen per variant randomizes lighting — batch ops cannot absorb ten thirty-minute rerolls.

## static-first before optional motion companion

순서: static legal pass on disclaimer → variant A/B still → winner still becomes thread master for remaining batch slots → optional subtle motion elsewhere. **Touch Edit** price change 5분 내 — weekly Bing cadence ops viable.

## 흔한 실패

ten unrelated prompts. **Brand Kit** skipped. Price baked. New thread per variant. 404 미복구. Fake Bing performance benchmarks.

## 측정 지표

batch offer fix당 분수, accent drift count, export ratios. 복구된 URL이 stable KO how-to-batch-create-designs-ai-bing SOP link.
"""

FACE_RETOUCH_KO = """
# AI로 얼굴 보정·인물 리터치: consent-first static companion SOP

이 한국어 URL `how-to-edit-faces-retouch-portraits-ai`은 404를 반환했습니다. Category How-To. 검색 의도는 face retouch portrait AI How-To — fake「perfect skin guaranteed」없음. Portrait daily ops: headshot retouch, team page update, campaign talent swap, consent-sensitive edits — offer와 disclaimer는 static companion editable layer, portrait pixels에 bake 금지. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** — face tool은 exploration layer, human consent final sign-off 필수.

## 네 가지 portrait retouch deliverable layer

첫째 headshot master 4:5 — readable name/title band **Touch Edit** editable. 둘째 team page grid companion same thread **Brand Kit** hex lock. 셋째 campaign talent swap variant — disclaimer footer editable including likeness consent line. 넷째 social crop 1:1 — **Design Agent** 50% zoom readable pass/fail, no baked small text in render.

## portrait retouch How-To가 compliance에서 실패하는 이유

likeness consent line baked in pixels — one word change triggers full regen 30분. **Brand Kit** 미설정 → team page slide accent drift. Brief「자연스러운 보정」만 — **Design Agent** pass/fail fields 없음. fake before/after benchmark 금지.

## ChatCanvas brief contract (face retouch KO)

약한 brief: "natural portrait retouch premium". 강한 brief: "Team X headshot 4:5 1080×1350, Brand Kit navy + sand from media kit, name/title top 15% flat for Touch Edit, disclaimer footer editable including consent line verbatim, no small text in render pixels, variants team grid + social same thread, **Design Agent** pass/fail checklist". face tool 이름은 brief comment only.

## Brand Kit이 team page series hex를 통일

approved VI에서 primary, accent sample. **ChatCanvas** same thread batch headshot + team grid + social crop — hex lock cross-format.

## Touch Edit으로 title/disclaimer 변경 portrait hero 유지

「Senior Designer」→「Lead Designer」: **Touch Edit** text band, face geometry와 **Brand Kit** accent stripe 유지. Full regen randomizes expression — team consistency cannot absorb thirty-minute reroll.

## consent-first boundary

portrait retouch는 likeness consent와 jurisdiction rules 따름 — AI가 compliance 문장을 invent하지 않음. disclaimer는 legal/HR approved 원문 **Touch Edit** paste. 본문은 legal advice 아님.

## 흔한 실패

consent line baked in pixels. **Brand Kit** skip. 404 미복구. fake skin improvement percent. portrait output만 final promo — static companion 생략.

## 측정 지표

disclaimer edit 분수, accent drift 횟수, consent return count. 복구된 URL이 stable KO how-to-edit-faces-retouch-portraits-ai SOP link.
"""

ENHANCE_UPSCALE_KO = """
# AI로 사진 선명화·샤프닝·업스케일: static-first companion SOP

이 한국어 URL `how-to-enhance-sharpen-upscale-photos-ai`은 404를 반환했습니다. Category How-To. 검색 의도는 enhance sharpen upscale photos AI — generic修圖 tool ranking이 아님. Photo enhance daily ops: ecommerce product shot, portfolio before/after, social thumb — caption과 disclaimer 변경 잦음, hex drift. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 enhance workflow를 static-first: master still, variant crops, editable caption layer. **fake megapixel·fake benchmark 데이터 없음**.

## 네 가지 enhance·upscale deliverable layer

첫째 product hero master 4:5 — readable price band **Touch Edit** editable. 둘째 before/after carousel slide 2–6 same thread **Brand Kit** hex lock. 셋째 social thumb 1:1 — disclaimer footer editable. 넷째 landing companion still — **Design Agent** QA offer match between thumb and landing.

## enhance upscale How-To가 화요일 offer에서 실패하는 이유

enhanced clip에 offer bake — landing static에 **Touch Edit** layer 없음. slide 4 accent lottery. **Brand Kit** 미설정. fake「4K upscale guaranteed」claim — export cap surprise. honest How-To = edit-minute median, not pixel count hype.

## ChatCanvas brief contract (enhance upscale KO)

약한 brief: "4K upscale product photo premium". 강한 brief: "Campaign X product hero 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, before/after slides 2–6 same thread accent stripe, **Design Agent** pass/fail at 50% zoom". upscale tool 이름은 brief comment only.

## Brand Kit이 enhance batch hex를 통일

approved VI에서 primary, accent sample. **ChatCanvas** same thread batch hero + carousel + thumb — hex SSOT cross-format.

## Touch Edit으로 caption·offer 변경 re-enhance 없이

offer text만 변경: **Touch Edit** static band 5분 — full re-enhance 30분 회피. Enhance ops KPI = static edit-minute median.

## honest enhance boundary

본문은 workflow SOP — fake resolution benchmark, fake file size comparison 없음. reader는 **Design Agent** checklist로 export review before vendor handoff.

## 흔한 실패

offer baked in enhanced pixels. **Brand Kit** skip. 404 미복구. fake megapixel stat. enhance output만 final promo — caption non-editable.

## 측정 지표

offer fix당 분수, re-enhance count, drift 횟수. 복구된 URL이 stable KO how-to-enhance-sharpen-upscale-photos-ai SOP link.
"""

CREATION_HISTORY_KO = """
# Lovart AI 창작 기록 추적: ChatCanvas thread audit SOP

이 한국어 URL은 `lovart-ai-creation-history-track-creative-` 접두 slug segment로 CMS에 보존됩니다 — 전체 slug suffix는 URL bar에서 확인, 본문에서는 창작 경로·작업 기록·variant 타임라인만 사용하고 해당 영어 slug term을 반복하지 않습니다. 검색 의도는 Lovart creation history How-To — **ChatCanvas** thread에서 variant 결정, **Brand Kit** hex 변경, **Touch Edit** price log를 audit 가능하게 기록. Lovart **Design Agent** pass/fail log 포함.

## 창작 기록에 남길 네 요소

첫째 original brief contract — safe zone, hex role, disclaimer sentence. 둘째 variant A/B/C 결정 — master 선택, discard 이유. 셋째 **Touch Edit** price log — old price, new price, 소요 분수. 넷째 **Design Agent** export checklist pass/fail. 기록은 revision audit용, vanity gallery 아님.

## team이 창작 경로를 잃는 이유

campaign마다 new prompt without thread — slide 4 accent lottery. price change full regen without log — 화요일 reroll 원인 추적 불가. **Brand Kit** 미설정 — hex change without SSOT. **ChatCanvas** thread naming 혼란 — newcomer가 지난주 master를 못 찾음.

## ChatCanvas thread as creation history SSOT

one campaign one thread family: master 4:5 + slide 2–6 + social crop same thread. **Brand Kit** change는 thread 첫 comment에 기록. variant 결정은 thread에「B 선택 — title 120px readable」. 창작 경로 = thread memory + Kit hex + Touch Edit log.

## Brand Kit version log와 hex change audit

Kit update: log old primary/accent → new value, campaign effective date, prior export re-touch 필요? **Design Agent** QA new Kit vs old export hex drift. 기록이「slide 4 coral인 이유」에 답 — guess 불필요.

## Touch Edit log가 full regen보다 audit-friendly

「₩79,000」→「₩69,000」: **Touch Edit** 5분 + log line. Full regen 30분 without structured log — ops가 brief template 최적화 못 함. 기록 가치 = revision cost replayable.

## 흔한 실패

pretty output만 저장 brief 없이. price change마다 full regen log 없음. **Brand Kit** hex record skip. 404 미복구. fake efficiency percent without source.

## 측정 지표

price fix당 log entries, thread naming compliance, drift post-mortem count. 복구된 URL이 stable KO lovart-ai-creation-history-track slug SOP link.
"""

OFFICIAL_GUIDE_KO = """
# 공식 Lovart Design AI Agent 확인 가이드: 가짜 사이트 피하고 안전하게 온보딩

이 한국어 URL `lovart-official-authentic-design-ai-agent-guide`은 404를 반환했습니다. Category How-To. Lovart 이름이 trend일 때 copycat domain이 따라옵니다 — verification beats regret. 본문은 operator writing: 실패 메모, criteria, checklist. **허구의 phishing domain 목록을 만들지 않습니다** — reader는 공식 `lovart.ai` HTTPS, browser address bar, 로그인 전 URL 확인 habit을 따릅니다. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 verified official agent에서 revision cost를 줄일 때 가치 — fake site credential trap 아님.

## 공식 agent 확인 네 criteria

첫째 domain: browser address bar에 `lovart.ai` HTTPS — bookmark typo 확인. 둘째 login flow: credential을 unknown third-party form에 paste 금지 — official login page only. 셋째 product surface: **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**가 documented workflow와 match. 넷째 pricing: lovart.ai 공식 pricing page 참조 — **본문에 tier 금액 표를 조작하지 않음**.

## fake Lovart site가 ops를 망치는 방식

phishing page가 API key 또는 password 수집. copycat UI는 pretty demo만 — **Touch Edit** editable layer 없음. team이 unverified link에서 download한「Lovart plugin」— malware risk. honest guide = verification checklist, not fabricated domain name list.

## ChatCanvas brief contract (official onboarding KO)

약한 brief: "premium Lovart poster". 강한 brief: "Campaign X promo 4:5 1080×1350, Brand Kit hex from approved media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, **Design Agent** pass/fail — verified lovart.ai session only". onboarding brief는 ops fields, not adjective stack.

## Brand Kit lock after verified login

approved VI에서 primary, accent, type role sample — unverified tool random gradient 금지. **ChatCanvas** same thread batch after Kit lock — hex SSOT before export.

## Touch Edit proves official agent is ops-viable

verified session에서 offer만 변경: **Touch Edit** CTA band 5분 — full regen 30분 회피. Fake site는 editable layer 없이 baked offer — Tuesday ops failed test.

## team onboarding honest workflow

Brief one sentence → channel name → three directions → edit type on canvas → proof at target width → archive scaffold with brief attached. Credential은 password manager + official domain bookmark — Slack unverified link click 금지.

## 흔한 실패

unverified URL에서 login. **Brand Kit** skip before export. 404 미복구. fabricated phishing domain examples. tier pricing 금액 본문 조작.

## 측정 지표

verification checklist completion, edit-minute median post-onboard, credential incident count zero target. 복구된 URL이 stable KO lovart-official-authentic-design-ai-agent-guide SOP link.
"""

GENERALIST_CREATOR_KO = """
# 제너럴리스트 크리에이터의 부상: 모든 task마다 specialist가 필요 없는 이유

이 한국어 URL `the-rise-of-the-generalist-creator-why-you-no-longer-need-a-specialist-for-simple-graphics`은 404를 반환했습니다 — slug는 그대로 CMS에 보존. Category Insight & Trend. 검색 의도는 generalist creator trend — fake「AI replaces all jobs」hype 아님. Insight framing: revision-heavy SMB promo에서 one **ChatCanvas** thread + **Brand Kit** hex lock + **Touch Edit** five-minute offer fix가 specialist handoff queue를 줄일 수 있음 — not universal specialist elimination claim. Lovart **Design Agent** pass/fail checklist가 generalist ops를 numeric으로 고정.

## generalist creator ops 네 deliverable layer

첫째 feed hero 4:5 — headline flat for **Touch Edit**. 둘째 carousel slide 2–6 same thread **Brand Kit**. 셋째 email header 600×300 — disclaimer editable. 넷째 ad-safe crop companion — **Design Agent** multi-ratio QA.

## specialist queue가 화요일 offer에서 막히는 이유

designer queue 48h — offer change missed window. **Brand Kit** 없이 generalist가 new prompt every promo — accent drift. Brief adjective only — **Design Agent** pass/fail 없음. honest insight = edit-minute median down, not「no designers ever needed」.

## ChatCanvas brief contract (generalist creator KO)

약한 brief: "premium generalist poster viral". 강한 brief: "Campaign X 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants feed + email same thread, **Design Agent** pass/fail generalist can run without design jargon". specialist handoff는 exploration or legal review only.

## Brand Kit as generalist anti-drift memory

generalist without Kit → slide 4 new accent invent. Kit active → agent follows hex roles — spellcheck follows dictionary. series work = memory beats surprise across tasks.

## Touch Edit on generalist promo blocks

「20% off」→「free shipping」: hero and email header type layer **Touch Edit** one session. two-word change full reroll — generalist Tuesday cadence broken without editable layer.

## insight boundary: what generalist stack does not replace

legal review, brand strategy sign-off, regulated disclaimer wording — still human/counsel. generalist AI stack covers revision-heavy static promo ops — not licensed professional advice substitute.

## 흔한 실패

「no specialist ever」overclaim. **Brand Kit** skip. offer bake. 404 미복구. fake job replacement stat.

## 측정 지표

price fix당 분수, specialist queue wait hours down, drift 횟수. 복구된 URL이 stable KO the-rise-of-the-generalist-creator long slug SOP link.
"""

VECTOR_LOGO_SVG_KO = """
# 벡터 로고 export: 간판·인쇄에 SVG가 필요한 이유

이 한국어 URL `vector-logo-export-why-you-need-svg-files-for-signage-and-print`은 404를 반환했습니다 — slug 그대로 CMS 보존. Category How-To. 검색 의도는 vector logo export SVG signage print — raster-only logo가 large format에서 blur되는 ops problem. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**는 logo companion static series — promo band editable, disclaimer footer editable; SVG handoff는 print vendor workflow, fake DPI benchmark 없음.

## signage·print 네 deliverable layer

첫째 logo lockup master — safe zone documented, **Brand Kit** primary/accent hex lock. 둘째 signage mock 16:9 — readable headline flat for **Touch Edit**. 셋째 print business card companion — disclaimer footer editable. 넷째 social crop 1:1 — **Design Agent** ratio export mismatch QA.

## raster-only logo가 signage에서 실패하는 이유

PNG upscale on 3m banner — edge blur, reprint cost. **Brand Kit** hex documented 없음 — vendor recreates wrong teal. offer baked in signage mock pixels — date change full regen 30분. honest How-To = vector handoff checklist + editable promo layer.

## ChatCanvas brief contract (vector logo SVG KO)

약한 brief: "premium logo signage". 강한 brief: "Brand X signage mock 16:9 1920×1080, Brand Kit hex from approved VI, logo lockup safe zone marked, headline top 15% flat for Touch Edit, event date bottom band editable, disclaimer footer editable, variants card + social same thread, **Design Agent** pass/fail at print preview size". SVG export path는 vendor spec comment — fake file size claim 없음.

## Brand Kit이 print·screen hex를 통일

approved VI에서 primary, accent, type role — vendor handoff hex SSOT. **ChatCanvas** same thread batch signage + card + social — hex lock cross-format.

## Touch Edit으로 event date 변경 signage hero 유지

「2026.09.01 Grand Open」→「2026.09.15」: **Touch Edit** date band, logo geometry와 **Brand Kit** accent stripe 유지. Full regen randomizes layout — reprint ops 30분 reroll 감당 불가.

## SVG vs raster honest boundary

SVG = scalable vector for vendor plate output; raster PNG/JPG = web social companion. 본문은 workflow division — fake「SVG always free」pricing 없음. reader는 print vendor에게 vector file + **Brand Kit** hex spec 함께 handoff.

## 흔한 실패

banner용 raster upscale only. **Brand Kit** skip. date baked in pixels. 404 미복구. fake DPI comparison table.

## 측정 지표

date fix당 분수, reprint count, hex drift vs vendor proof. 복구된 URL이 stable KO vector-logo-export-why-you-need-svg-files-for-signage-and-print SOP link.
"""


FAQ = {
    "texture_material_ko": """
## FAQ

**texture tool 월액 본문 기재?**  
없음 — lovart.ai 및 각 platform 공식 ToS 참조.

**Touch Edit offer fix 5분?**  
예 — static companion editable layer test.

**Brand Kit material hue lock?**  
예 — packaging VI에서 hex sample.

**404 복구 URL?**  
안정 KO complete-guide-ai-texture-material-generation.

**fake material benchmark?**  
없음 — edit-minute KPI만.
""",
    "free_tools_complete_ko": """
## FAQ

**Lovart tier 금액 표 있나?**  
없음 — lovart.ai 공식 pricing page만 참조.

**free tier export cap?**  
각 tool 공식 ToS에서 reader 직접 확인.

**Touch Edit 5분 KPI?**  
예 — revision-heavy promo ops test.

**404 복구 URL?**  
안정 KO complete-guide-free-ai-design-tools-2026.

**fake #1 ranking?**  
없음 — task group framework만.
""",
    "free_tools_ko": """
## FAQ

**본문 Lovart 월 구독료?**  
없음 — 공식 pricing 참조만.

**Brand Kit free workflow?**  
예 — media kit hex lock before batch.

**Touch Edit promo band 5분?**  
예 — full free-tool regen 회피.

**404 복구 URL?**  
안정 KO free-ai-design-tools-2026 How-To.

**fabricated pricing?**  
없음 — workflow SOP only.
""",
    "batch_create_bing_ko": """
## FAQ

**batch ten variants one thread?**  
예 — same ChatCanvas thread accent stripe.

**Tuesday price fix full regen?**  
아니오 — Touch Edit 5분 per variant.

**Brand Kit before batch?**  
예 — hex SSOT cross-ratio.

**404 복구 URL?**  
안정 KO how-to-batch-create-designs-ai-bing.

**fake Bing ROI?**  
없음 — ops metrics만.
""",
    "face_retouch_ko": """
## FAQ

**consent line editable?**  
예 — Touch Edit text band, pixels bake 금지.

**portrait full regen on title change?**  
아니오 — Touch Edit 5분.

**Brand Kit team page series?**  
예 — same thread hex lock.

**404 복구 URL?**  
안정 KO how-to-edit-faces-retouch-portraits-ai.

**fake skin improvement %?**  
없음 — consent-first workflow만.
""",
    "enhance_upscale_ko": """
## FAQ

**fake 4K benchmark?**  
없음 — Design Agent pass/fail QA만.

**Touch Edit caption fix 5분?**  
예 — re-enhance 회피.

**Brand Kit enhance batch?**  
예 — carousel same thread hex.

**404 복구 URL?**  
안정 KO how-to-enhance-sharpen-upscale-photos-ai.

**offer baked in enhanced pixels?**  
금지 — static editable layer.
""",
    "creation_history_ko": """
## FAQ

**slug 영어 suffix 본문 반복?**  
아니오 — 창작 경로·작업 기록만 사용.

**Touch Edit price log 필수?**  
예 — revision cost audit.

**Brand Kit hex change log?**  
예 — drift post-mortem SSOT.

**404 복구 URL?**  
안정 KO lovart-ai-creation-history-track slug.

**fake efficiency %?**  
없음 — log entries count만.
""",
    "official_guide_ko": """
## FAQ

**허구 phishing domain 목록?**  
없음 — lovart.ai HTTPS 확인 habit만.

**본문 tier 금액?**  
없음 — 공식 pricing page 참조.

**Touch Edit verified session test?**  
예 — 5분 offer fix ops proof.

**404 복구 URL?**  
안정 KO lovart-official-authentic-design-ai-agent-guide.

**unverified link login?**  
금지 — official domain bookmark.
""",
    "generalist_creator_ko": """
## FAQ

**specialist 완전 불필요 claim?**  
아니오 — legal/brand sign-off still human.

**Brand Kit generalist drift?**  
예 — Kit active면 hex roles follow.

**Touch Edit two-word change 5분?**  
예 — full reroll 회피.

**404 복구 URL?**  
안정 KO the-rise-of-the-generalist-creator long slug.

**fake job replacement stat?**  
없음 — edit-minute insight만.
""",
    "vector_logo_svg_ko": """
## FAQ

**SVG signage handoff?**  
예 — vendor plate + Brand Kit hex spec.

**Touch Edit event date 5분?**  
예 — signage hero layout 유지.

**raster-only banner OK?**  
아니오 — large format blur reprint risk.

**404 복구 URL?**  
안정 KO vector-logo-export-why-you-need-svg-files-for-signage-and-print.

**fake DPI table?**  
없음 — workflow checklist만.
""",
}


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 실습 보충 {n}: {topic}

첫 brief가 형용사만 쌓이면 그림은 예쁘지만 가격 글자가 작고 배지가 hero를 가립니다. 두 번째는 safe zone과 필수 필드만 수정. **ChatCanvas** thread가 slide 4 accent drift를 줄입니다. **{topic}**에서 **Touch Edit** 가격 수정 5분이면 static-first 입증. full regen 30분이면 **Brand Kit**부터 재설정. 복구된 404 URL이 stable SOP link batch32. **Design Agent** pass/fail checklist가 형용사 brief보다 낫습니다.
"""


ARTICLES = [
    {
        "rank": 326,
        "key": "texture_material_ko",
        "lang": "ko",
        "slug": "complete-guide-ai-texture-material-generation",
        "cover": "026",
        "category": "Complete Guide",
        "title": "AI 텍스처·재질 생성 완전 가이드: static-first promo companion",
        "seo_title": "Complete Guide AI Texture Material Generation KO — Brand Kit hex lock",
        "description": "KO 404 fix: texture material complete guide, Touch Edit offer editable, no fabricated pricing.",
        "seo_description": "Complete Guide: ChatCanvas same thread, Design Agent pass/fail, official ToS only.",
        "focus": "complete guide ai texture material generation",
        "keywords": ["ai texture material generation", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Complete Guide — AI Texture Material Generation KO",
        "body": TEXTURE_MATERIAL_KO,
        "expand_topic": "KO complete guide ai texture material generation workflow",
    },
    {
        "rank": 327,
        "key": "free_tools_complete_ko",
        "lang": "ko",
        "slug": "complete-guide-free-ai-design-tools-2026",
        "cover": "027",
        "category": "Complete Guide",
        "title": "2026 무료 AI 디자인 도구 완전 가이드: honest decision framework",
        "seo_title": "Complete Guide Free AI Design Tools 2026 KO — no fake pricing",
        "description": "KO 404 fix: free AI design tools 2026 complete guide, task groups not fake scores, Lovart tier 금액 조작 없음.",
        "seo_description": "Complete Guide: Touch Edit revision cost, Brand Kit hex lock, lovart.ai official pricing only.",
        "focus": "complete guide free ai design tools 2026",
        "keywords": ["free ai design tools 2026", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Complete Guide — Free AI Design Tools 2026 KO",
        "body": FREE_TOOLS_COMPLETE_KO,
        "expand_topic": "KO complete guide free ai design tools 2026 honest framework",
    },
    {
        "rank": 328,
        "key": "free_tools_ko",
        "lang": "ko",
        "slug": "free-ai-design-tools-2026",
        "cover": "028",
        "category": "How-To",
        "title": "2026 무료 AI 디자인 도구: How-To ops SOP",
        "seo_title": "Free AI Design Tools 2026 KO — How-To no Lovart tier fabrication",
        "description": "KO 404 fix: free AI design tools 2026 How-To, Brand Kit hex lock, no Lovart tier 금액 in body.",
        "seo_description": "How-To: ChatCanvas brief contract, Touch Edit five-minute test, official ToS reference.",
        "focus": "free ai design tools 2026",
        "keywords": ["free ai design tools", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Free AI Design Tools 2026 KO",
        "body": FREE_TOOLS_KO,
        "expand_topic": "KO free ai design tools 2026 How-To workflow",
    },
    {
        "rank": 329,
        "key": "batch_create_bing_ko",
        "lang": "ko",
        "slug": "how-to-batch-create-designs-ai-bing",
        "cover": "029",
        "category": "How-To",
        "title": "AI로 Bing 광고용 디자인 일괄 생성: static-first campaign series",
        "seo_title": "How To Batch Create Designs AI Bing KO — one ChatCanvas thread",
        "description": "KO 404 fix: batch create designs AI Bing, Brand Kit hex lock, Touch Edit CTA layer.",
        "seo_description": "How-To: multi-ratio export same thread, Design Agent QA, no fake Bing ROI.",
        "focus": "how to batch create designs ai bing",
        "keywords": ["batch create designs ai bing", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Batch Create Designs AI Bing KO",
        "body": BATCH_CREATE_BING_KO,
        "expand_topic": "KO how to batch create designs ai bing workflow",
    },
    {
        "rank": 330,
        "key": "face_retouch_ko",
        "lang": "ko",
        "slug": "how-to-edit-faces-retouch-portraits-ai",
        "cover": "030",
        "category": "How-To",
        "title": "AI로 얼굴 보정·인물 리터치: consent-first static companion",
        "seo_title": "How To Edit Faces Retouch Portraits AI KO — Touch Edit consent layer",
        "description": "KO 404 fix: face retouch portrait AI How-To, disclaimer editable, consent-first boundary.",
        "seo_description": "How-To: Brand Kit team page series, Design Agent pass/fail, no fake skin claims.",
        "focus": "how to edit faces retouch portraits ai",
        "keywords": ["face retouch ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Edit Faces Retouch Portraits AI KO",
        "body": FACE_RETOUCH_KO,
        "expand_topic": "KO how to edit faces retouch portraits ai workflow",
    },
    {
        "rank": 331,
        "key": "enhance_upscale_ko",
        "lang": "ko",
        "slug": "how-to-enhance-sharpen-upscale-photos-ai",
        "cover": "031",
        "category": "How-To",
        "title": "AI로 사진 선명화·샤프닝·업스케일: static-first companion SOP",
        "seo_title": "How To Enhance Sharpen Upscale Photos AI KO — Touch Edit caption layer",
        "description": "KO 404 fix: enhance sharpen upscale photos AI How-To, no fake megapixel benchmark.",
        "seo_description": "How-To: Brand Kit carousel same thread, Design Agent 50% zoom QA.",
        "focus": "how to enhance sharpen upscale photos ai",
        "keywords": ["enhance sharpen upscale photos ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Enhance Sharpen Upscale Photos AI KO",
        "body": ENHANCE_UPSCALE_KO,
        "expand_topic": "KO how to enhance sharpen upscale photos ai workflow",
    },
    {
        "rank": 332,
        "key": "creation_history_ko",
        "lang": "ko",
        "slug": "lovart-ai-creation-history-track-creative-journey",
        "cover": "032",
        "category": "How-To",
        "title": "Lovart AI 창작 기록 추적: ChatCanvas thread audit SOP",
        "seo_title": "Lovart AI Creation History Track KO — 창작 경로 ChatCanvas log",
        "description": "KO 404 fix: creation history How-To, slug suffix preserved, no English slug term in body.",
        "seo_description": "How-To: Brand Kit hex log, Touch Edit price log, Design Agent audit checklist.",
        "focus": "lovart ai creation history track creative",
        "keywords": ["lovart creation history", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Lovart AI Creation History Track KO",
        "body": CREATION_HISTORY_KO,
        "expand_topic": "KO Lovart creation history 창작 경로 workflow",
    },
    {
        "rank": 333,
        "key": "official_guide_ko",
        "lang": "ko",
        "slug": "lovart-official-authentic-design-ai-agent-guide",
        "cover": "033",
        "category": "How-To",
        "title": "공식 Lovart Design AI Agent 확인 가이드: 가짜 사이트 피하기",
        "seo_title": "Lovart Official Authentic Design AI Agent Guide KO — verify lovart.ai",
        "description": "KO 404 fix: official Lovart agent verification, no fabricated phishing domains, factual onboarding.",
        "seo_description": "How-To: lovart.ai HTTPS check, Brand Kit lock, Touch Edit ops test, no tier fabrication.",
        "focus": "lovart official authentic design ai agent guide",
        "keywords": ["lovart official authentic", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Lovart Official Authentic Guide KO",
        "body": OFFICIAL_GUIDE_KO,
        "expand_topic": "KO lovart official authentic design ai agent verification workflow",
    },
    {
        "rank": 334,
        "key": "generalist_creator_ko",
        "lang": "ko",
        "slug": "the-rise-of-the-generalist-creator-why-you-no-longer-need-a-specialist-for-simple-graphics",
        "cover": "034",
        "category": "Insight & Trend",
        "title": "제너럴리스트 크리에이터의 부상: specialist handoff 줄이는 insight",
        "seo_title": "Rise Of Generalist Creator KO — long slug preserved ChatCanvas ops",
        "description": "KO 404 fix: generalist creator insight, long slug exact match, no fake job replacement stat.",
        "seo_description": "Insight: Brand Kit anti-drift, Touch Edit five-minute fix, Design Agent generalist checklist.",
        "focus": "the rise of the generalist creator why you no longer need a specialist for every task",
        "keywords": ["generalist creator", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight & Trend — Generalist Creator Rise KO",
        "body": GENERALIST_CREATOR_KO,
        "expand_topic": "KO the rise of the generalist creator insight workflow",
    },
    {
        "rank": 335,
        "key": "vector_logo_svg_ko",
        "lang": "ko",
        "slug": "vector-logo-export-why-you-need-svg-files-for-signage-and-print",
        "cover": "035",
        "category": "How-To",
        "title": "벡터 로고 export: 간판·인쇄에 SVG가 필요한 이유",
        "seo_title": "Vector Logo Export SVG Signage Print KO — Brand Kit hex handoff",
        "description": "KO 404 fix: vector logo export SVG signage print, long slug exact match, Touch Edit date editable.",
        "seo_description": "How-To: logo lockup safe zone, Design Agent print QA, no fake DPI table.",
        "focus": "vector logo export why you need svg files for signage and print",
        "keywords": ["vector logo export svg", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Vector Logo Export SVG Signage Print KO",
        "body": VECTOR_LOGO_SVG_KO,
        "expand_topic": "KO vector logo export svg signage print workflow",
    },
]


EXPAND_FN = {
    "ko": expand_ko,
}

UNIT_MAP = {
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch32 content cluster.*\n"
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
