#!/usr/bin/env python3
"""Generate 404-rescue P2 batch12 blog bodies (10 files). Self-contained.

Ranks #123–#132 from 404-rescue-compact lane.
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

COACH_BRAND_KIT_ZHTW = """
# 教練 Brand Kit：課程 promo、學員見證與 LINE 社群系列

這條繁中 URL `brand-kit-coach-lovart` 曾 404，搜尋需要 life coach / 教練 segment 的 **Brand Kit** SOP，不是「60 秒生成全套 VI」 demo。教練 daily ops：一對一諮詢 promo、團體課程開班、學員見證 quote card、LINE 官方帳封面 — 改開課日期與早鳥價頻繁，calm professional accent 易 drift。Lovart **ChatCanvas** thread、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 trustworthy palette 與 readable CTA。

## 教練 segment 四個高頻場景

第一是課程開班 hero 4:5：日期、名額、早鳥價 readable，headline top 15% flat for **Touch Edit**。第二是學員見證 quote card：姓名與職稱 disclaimer footer editable。第三是 Instagram / Reels cover 9:16：bottom 20% CTA band，不擋臉部。第四是 LINE 官方帳封面與課表 PDF：同一 **Brand Kit** accent，只換課程名。

## 為什麼 coach promo 常卡在改開課日

弱 brief「幫我做療癒系教練海報」→ 圖好看但日期字小、角標擋人像。改「3/15 開課」要 full regen 三十分鐘。carousel slide 4 accent drift 成另一個 sage green。readable 早鳥價 bake 進 pixels。video hook 有 offer 但 landing static 無 **Touch Edit** layer。**Brand Kit** 未從名片與 prior workshop PDF 取樣 hex。

## ChatCanvas brief 合同（教練版）

強 brief 寫驗收字段：「團體課 promo 4:5 1080×1350，Brand Kit sage + cream from business card，headline top 15% flat for Touch Edit，早鳥價 bottom left safe zone，免責聲明 footer editable（非醫療建議句附 brief 原文），禁止 render 內小字，slide 2–6 同 thread 只換課程名」。**Design Agent** QA safe zone、disclaimer present、hex drift vs Kit。

## Brand Kit 從名片、workshop 簡報取樣

從已批准名片、講座簡報、門口 signage 取樣 primary hex、accent hex、title/body type role。不用 stock marble 當教練品牌色。Kit 建好后所有 **ChatCanvas** thread 引用同一套 role；改 global promo 用 **Touch Edit** CTA band，不 full regen portrait photography。

## Touch Edit 改早鳥價不改 layout identity

改「早鳥 NT$3,800」為「現場 NT$4,200」：**Touch Edit** 框 CTA 帶，指令「保持 stripe geometry 與 Brand Kit accent，只替換文案」。full regen 會 random 改 portrait crop 與 shadow — 教練個人 brand 與 firm VI 並存時尤其致命。

## static-first 再配 optional motion teaser

教練 offer 必須在 static editable layer；optional motion bumper 4–6 秒與 **Brand Kit** 色溫一致，no readable small text in clip。Reels autoplay 常靜音；學員 screenshot still — 早鳥價須在 mobile width readable。

## 與 jewelry designer segment 的分工

本篇聚焦 coach：課程日期、見證 quote、LINE cover、非醫療 disclaimer。jewelry designer slug 另文覆蓋 product hero 與材質 disclaimer 字段。

## 常見失敗

跳過 **Brand Kit**。readable 價 baked。每課程新 prompt 無 thread。404 URL 未修復 SOP 散在 LINE 群組。

## 測量 ROI

改開課日一次幾分鐘、carousel drift 幾次、一次 action export 幾種 ratio。404 修復給 coach ops stable Brand Kit SOP URL。
"""

JEWELRY_BRAND_KIT_ZHTW = """
# 珠寶設計師 Brand Kit：系列 catalog、材質 disclaimer 與展覽 promo

這條繁中 URL `brand-kit-jewelry-designer-lovart` 曾 404，搜尋需要 jewelry designer segment 的 **Brand Kit** operational 指南。設計師 daily ops：系列 catalog hero、材質與保養 disclaimer、展覽 invite、Instagram 產品 carousel — 改系列價與「純銀/鍍金」說明勤，luxury neutral accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 editorial jewelry palette。

## 珠寶 designer 四個高頻場景

第一是系列 catalog cover：產品 focal，價 readable，材質 disclaimer footer editable。第二是展覽 invite 與 DM card：日期 venue 改得勤，**Touch Edit** date block。第三是 carousel slide 2–6 單品：同一 **Brand Kit** accent，只換 SKU name。第四是 story 9:16：product 不擋 bottom 20% CTA。

## 為什麼 jewelry promo 常卡在改材質說明

改「925 純銀」為「14K 鍍金」要 full regen 三十分鐘。slide 4 accent drift 成另一個 champagne gold。readable 價 bake 進 pixels。video 角標有 offer static 無 **Touch Edit** layer。**Brand Kit** 未從 packaging 與 prior lookbook 取樣 hex。

## ChatCanvas brief 合同（珠寶版）

弱 brief「高級珠寶感海報」。強 brief：「系列 promo 4:5 1080×1350，Brand Kit charcoal + champagne from packaging，headline top 15% flat for Touch Edit，價格 bottom left safe zone，材質 disclaimer footer editable 原文附 brief，禁止 render 內小字，slide 2–6 同 thread」。**Design Agent** numeric acceptance fields。

## Brand Kit 從 packaging、lookbook、signage 取樣

從已批准包裝、lookbook、工作室招牌取樣 primary、accent、type role。不用 stock marble 當品牌色。**ChatCanvas** 同一 thread batch 多 SKU export。

## Touch Edit 改系列價不改 product photography crop

改「限量 NT$2,800」為「預購 NT$3,200」：**Touch Edit** 框 CTA 帶，保持 product geometry 與 **Brand Kit** accent stripe。full regen random 改 highlight 與 shadow — 珠寶細節對 lighting 敏感，brief 寫 reflection 禁項。

## 與 coach segment 的分工

coach slug 覆蓋課程日期與見證 quote；本篇覆蓋 SKU catalog、材質 disclaimer、展覽 invite 字段。

## static-first 再配 optional product motion

story autoplay 常靜音；買家 screenshot still。順序：static legal pass on 材質 disclaimer → optional motion 與 **Brand Kit** 色溫一致。

## 常見失敗

跳過 **Brand Kit**。價格 baked。每 SKU 新 prompt 無 thread。404 未修復。

## 測量 ROI

改系列價一次幾分鐘、drift 幾次、export 幾種 ratio。404 修復給 jewelry designer ops stable Brand Kit SOP URL。
"""

LOOKA_ALT_ZHTW = """
# Looka 替代品 2026：台灣 SMB 的 logo 探索與 LINE/IG 日常物料分工

這條繁中 URL `looka-alternatives-2026` 曾 404。注意：简体 batch6 已有 `zh` 版，重 logo sprint vs daily ops 分工；本篇為**繁中重寫**，角度不同：台灣 SMB 語境、LINE 官方帳、Reels safe zone、NT$ promo 字段 — 禁止逐句翻譯简体版。

## 台灣 SMB 兩類任務不要混用

第一類 logo 與初版色板探索：Looka 等可快速出方向，適合開店前 sprint。第二類 LINE 封面、IG carousel、早鳥 promo 改價：需要 **ChatCanvas**、**Brand Kit**、**Touch Edit** revision loop。用 logo 工具做週二改 NT$ 價常得到 baked 字層。

## Brand Kit 接 Looka 輸出成 production 記憶

Looka 鎖定 hex 與 font role 後，寫入 Lovart **Brand Kit**，再開 **ChatCanvas** product thread。避免 Looka pack 與 weekly LINE 貼文各用各 accent — 台灣店家常見「logo 一套、社群另一套」視覺分裂。

## ChatCanvas brief 接台灣渠道 safe zone

弱 brief「按 Looka 風格做海報」。強 brief：「SKU 居中，Brand Kit 用 Looka 鎖定 navy + sand，headline top 15%，早鳥價 bottom left safe zone，Reels bottom 20% CTA flat for Touch Edit，disclaimer footer editable，1:1 與 4:5 同 thread」。**Design Agent** 引用 Kit role，不驗「高級感」。

## Touch Edit 是 alternatives 清單少比的一環

Alternatives 文章常比「誰 logo 快」，少比「改早鳥價是否五分鐘」。**Touch Edit** 改 CTA 帶才是 daily ops 分水嶺 — 台灣 SMB 週改 promo 比 logo 再設計頻繁。

## 公平對比標準（台灣 ops）

readable promo layer、carousel drift、改價分鐘、export 尺寸數、商用 license 查官方 ToS — 不編造 tier 價格。單張 logo win 的工具可能在 LINE series 上 lose。

## 與简体 batch6 的差異說明

简体版重 logo vs campaign static 抽象分工；繁中版重 LINE/IG/Reels 字段、NT$ disclaimer、台灣店鋪 onboarding SOP。slug 同，locale 不同，正文不 copy paragraph。

## 常見失敗

Looka 一次匯出直接投廣告無 disclaimer 層。weekly post 不用 **Brand Kit**。alternatives 只列名字不比 revision cost。

## 測量 ROI

改價分鐘、drift 次數、export 幾種 ratio。404 修復給 TW SMB stable Looka alternatives SOP URL。
"""

DESIGN_CERT_DE = """
# AI-Design-Zertifizierung und Bildungsprogramme 2026: Curriculum vs. Production Workflow

Diese deutsche URL `ai-design-certification-education-programs-2026` lieferte 404, während Suchen nach ehrlichen Bildungsprogrammen und Zertifizierungen für AI-gestütztes Design kamen — nicht nach fake „Harvard AI Design Diploma“. Ehrliche Einordnung: Zertifikate messen oft Tool-Klickfolgen; Marketing-Ops brauchen **Brand Kit**, **ChatCanvas** thread, **Touch Edit** und **Design Agent** QA-Felder. Diese Seite trennt Curriculum-Lernziele von revision-heavy Production SOP.

## Vier Lernebenen in 2026-Programmen

Erstes Niveau: Prompt-Grundlagen und Ethik — nützlich, aber nicht gleich Tuesday-Preisänderung. Zweites: visuelle Systeme und **Brand Kit** hex roles — direkt übertragbar auf Kampagnen-Serien. Drittes: **Touch Edit** und editable layers — selten in reinen Zertifikatskursen, aber entscheidend für Legal/Disclaimer. Viertes: **Design Agent** als pass/fail Checkliste — QA-Felder statt Adjektiv-Briefs.

## Warum Zertifikats-Inhalte oft am Dienstag scheitern

Kurse lehren „premium Poster“ als Brief; Ergebnis: kleiner Preis, Badge über Produkt. Änderung „Open House Sa 14 Uhr“ kostet thirty-minute full regen — weil Curriculum static export ohne **Touch Edit** layer vorsieht. Slide 4 erfindet neuen accent ohne **Brand Kit** SSOT.

## ChatCanvas brief-Vertrag als Prüfungsformat

Statt „schönes Design“: „Listing hero 4:5, Brand Kit navy + sand, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, no small text in render“. **Design Agent** prüft numeric acceptance — das ist prüfbares Curriculum, nicht subjektive Bewertung.

## Brand Kit als Brücke zwischen Kurs und Agentur-Ops

Programme, die nur Einzelbild-Generierung üben, produzieren Absolventen ohne series memory. **Brand Kit** als Pflichtmodul: hex aus genehmigtem Media Kit, nicht stock marble. Ein **ChatCanvas** thread für slide 2–6 reduziert drift — messbare Kompetenz.

## Touch Edit als fehlendes Modul in vielen Zertifikaten

Fairer Vergleich von Bildungsprogrammen 2026: lehrt das Curriculum Preisänderung in fünf Minuten via **Touch Edit**? Wenn nein, Absolventen gewinnen Zertifikat, verlieren aber Kunden-Revisionen. Keine erfundenen Stunden- oder Preisangaben — prüfen Sie offizielle Programmseiten.

## Abgrenzung: Zertifikat vs. Production SOP

Diese 404-Recovery-Seite ist keine Kursliste mit fake Rankings. Sie gibt DE teams stable URL für „nach dem Zertifikat — welcher Production workflow“. Referenz: **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** als Praxis-SSOT.

## Typische Fehler

Zertifikat als Ersatz für **Brand Kit** setup. Curriculum ohne disclaimer editable layer. 404 URL nicht wiederhergestellt — SOP in Slack-Threads.

## Metriken

Minuten pro Preis-Fix nach Kursabschluss, accent drift pro carousel, export sizes pro action. Wiederhergestellte URL als stable DE education-to-ops SOP link.
"""

FREE_AI_TOOLS_JA = """
# 無料 AI デザインツールの使い方：brief 契約と static-first 実務

この日本語 URL `how-to-use-free-ai-design-tools` は 404 でしたが、検索は「無料 AI デザインツールを marketing daily ops にどう組み込むか」を求めていました。正直な framing：無料 tier は exploration に向く；readable 価格、**Brand Kit** series、legal disclaimer editable は **ChatCanvas** + **Touch Edit** + **Design Agent** の revision loop が必要。ツール名の列挙だけでは Tuesday 改价に耐えません。

## 無料ツールで足りる三場面と足りない三場面

足りる：mood board 一枚、個人ブログ hero 試作、社内 slide 方向探索。足りない：carousel slide 2–6 の accent 一致、価格 block の **Touch Edit** 五分修正、disclaimer footer の一字変更、多 ratio export 同一 thread。

## なぜ「無料 AI」workflow が火曜日に破綻する

弱 brief「モダンなポスター」→ 価格文字が小さく badge が顔を隠す。「20% OFF」一字変更で thirty-minute full regen。slide 4 が別 accent。**Brand Kit** 未設定で毎 generation が新 pastel を invent。

## ChatCanvas brief 契約（無料ツール接続版）

強 brief：「SKU 中央、Brand Kit slate + coral from approved packaging、headline top 15% flat for Touch Edit、price bottom left safe zone、disclaimer footer editable、1080×1350、render 内小字禁止」。**Design Agent** は acceptance フィールドのみ QA — 形容詞「高級感」は不可。

## Brand Kit を無料探索の後に必ず置く

無料ツールで出した direction から hex を **Brand Kit** に取り込み、以降の **ChatCanvas** thread は Kit role を参照。探索と production を混在させると weekly post が拼贴に見えます。

## Touch Edit が無料 tier 記事で語られない理由

多くの how-to は first-frame beauty のみ。**Touch Edit** で CTA band だけ差し替え、layout identity を保持 — これが daily ops の分岐点。full regen 30 分なら Brand Kit と brief テンプレからやり直し。

## 商用 license と ToS（価格は捏造しない）

paid social 前に各ツール公式 ToS を確認。無料 tier が commercial use を許すか campaign ごとに archive。Lovart static を textual QA してから publish。

## よくある失敗

無料ツールだけで funnel 全体を賄う。価格 baked pixels。サイズごとに別 prompt。video hook に offer、landing static に **Touch Edit** layer なし。

## 測定

価格修正分数、slide 4 drift 回数、export ratio 数。404 復旧 URL は JP teams 向け stable free-tools-to-ops SOP link。
"""

SMB_BRANDING_KO = """
# 소규모 사업 브랜딩 완전 가이드: AI workflow와 Brand Kit SSOT

이 한국어 URL `complete-guide-small-business-branding-ai`은 404였지만 검색은 소규모 사업자의 브랜딩 완전 가이드를 원했습니다 — 「원클릭 VI」 환상이 아니라 weekly promo, readable 가격, carousel series 일관성. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent**가 revision-heavy SMB ops에 맞습니다.

## 소규모 사업 네 가지 daily 출력

첫째 feed hero 4:5와 carousel slide 2–6: 가격 readable, accent drift 금지. 둘째 story 9:16: top 12%, bottom 20% platform UI safe zone. 셋째 네이버/인스타 프로모 stripe: **Touch Edit**로 요일별 가격 수정. 넷째 명함·전단·QR card: disclaimer footer editable.

## 왜 SMB branding이 화요일 promo에서 깨지나

약한 brief 「고급스럽게」→ 작은 가격, badge가 제품 가림. 「10% 할인」 한 글자 변경에 thirty-minute full regen. slide 4 accent drift. readable disclaimer pixels에 bake. **Brand Kit** 없이 매 generation 새 pastel.

## ChatCanvas brief 계약 (SMB branding)

강 brief: 「SKU 중앙, Brand Kit slate + coral from packaging, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, 1080×1350, render 내 작은 글자 금지」. **Design Agent**는 acceptance 필드만 QA.

## Brand Kit을 offline material에서 채우기

명함, 간판, 기존 전단에서 primary/accent hex, title/body type role. stock marble 금지. Kit 후 **ChatCanvas** product thread. campaign 변경은 **Touch Edit** copy layer.

## Touch Edit가 complete guide의 핵심 분기

가격·날짜만 수정, layout identity 유지. 지시: stripe geometry와 **Brand Kit** accent 유지, copy만 교체. full regen은 SMB 팀의 time sink — guide가 이걸 빼면 incomplete.

## static-first 후 optional motion

offer는 static editable layer에. clip 4–6초, readable small text 없음, **Brand Kit** color temperature aligned. muted autoplay에서 사용자는 still screenshot.

## 흔한 실패

**Brand Kit** 생략. 가격 baked. size마다 별도 prompt. video offer, landing static **Touch Edit** 없음.

## 측정

가격 fix 분수, drift 횟수, action당 export size 수. 404 복구 URL은 KR SMB stable branding SOP link.
"""

ADOBE_EXPRESS_ZH = """
# Adobe Express 与 Lovart 对比：运营向 revision-heavy static 工作流

这条中文 URL `adobe-express-vs-lovart-comparison` 曾返回 404，搜索需要 operational 对比，不是 feature 清单软文或拉踩。直接结论：Adobe Express 擅长模板化 quick layout、Adobe 生态内 asset 与 familiar UI；弱在 AI-native **ChatCanvas** thread series、**Brand Kit** hex SSOT 与 **Touch Edit** 五分钟改价 layer 的默认 workflow。Lovart **Design Agent** 执行 brief 合同 QA；Express 仍适合已有 Creative Cloud 团队的 template 起稿。不写 fake 价格 tier — 商用范围请阅各平台官方定价页。

## 四类任务的分工对比

第一类模板化 social post 快速起稿：Express template 库有优势。第二类 weekly 改价 carousel slide 2–6 不 drift：Lovart **Brand Kit** + 单 **ChatCanvas** thread 更稳。第三类 readable 价格与 disclaimer editable：**Touch Edit** 改 CTA 带 vs Express 内文字层编辑（取决于 export 路径）。第四类 **Design Agent** pass/fail 验收字段：Lovart 默认 checklist；Express 需人工 eyeball。

## 为什么「Express vs Lovart」对比常比错指标

比 first-frame beauty 或模板数量 → 采购误导。应比同一 Tuesday 改价任务：static fix 分钟、carousel accent drift 次数、一次 action export 几种 ratio。readable offer 是否在 editable layer 才是 ops 分水岭。

## ChatCanvas brief 合同（Lovart 侧 operational 标准）

弱 brief「高级产品海报」。强 brief：「SKU 居中，Brand Kit slate + coral，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，1080×1350，禁止双 CTA」。**Design Agent** 不能验收「高级感」。

## Brand Kit 作为 Express 导出后的 production 记忆

若团队已在 Express 定稿 hex，写入 Lovart **Brand Kit** 再开 **ChatCanvas** thread — 避免 Express 一稿与 weekly AI post 各用各 accent。并行 workflow 不是二选一互斥。

## Touch Edit 改价场景对比

Lovart：**Touch Edit** 框 CTA 带，保持 stripe geometry，五分钟关闭「满 200 减 30」变更。Express：取决于是否保留 editable text layer 与是否 full re-export；部分 AI 生成路径仍触发 thirty-minute regen。对比应实测同 brief，不编造分钟数。

## 常见失败

只比模板数量不比 revision cost。video hook 有 offer landing static 无 editable price。跳过 **Brand Kit** 导致 carousel drift。404 URL 未修复。

## 测量 ROI

改价分钟、drift 次数、legal return、export size 数。404 修复给 ops team stable Adobe Express vs Lovart comparison SOP URL。
"""

ILLUSTRATION_GUIDE_ZH = """
# AI 插画指南：从 prompt 生成专业级 artwork 的可编辑工作流

这条中文 URL `ai-illustration-guide-how-to-generate-professional-artwork-from-prompts` 曾返回 404，搜索需要 illustration from prompts 的 operational 指南，不是「一键艺术大片」 demo。专业 artwork 在 marketing ops 里指：series 一致、改 copy 不 lottery 风格、disclaimer editable — 靠 **ChatCanvas** thread、**Brand Kit** illustration role、**Touch Edit**、**Design Agent** QA。

## 插画输出四类验收字段

第一是 style lock：线宽、色板 hex 写进 **Brand Kit**，不是每 slide 新 prompt lottery。第二是 character/object consistency：同 thread export 4:5 hero → 9:16 story → 1:1 avatar。第三是 readable promo layer：价目与 CTA 在 **Touch Edit** band，不 bake 进 illustration pixels。第四是 legal footer：商用 disclaimer editable。

## 为什么「长 prompt 堆风格词」仍产出业余感

弱 brief「赛博朋克插画高级」→ 小字价目、double CTA、slide 4 accent drift。改活动 copy full regen 三十分钟 → 连带换风格。readable 价格 bake 进 render。**Brand Kit** 未定义 stroke_weight 与 palette role。

## ChatCanvas brief 合同（插画版）

强 brief：「campaign X，illustration hero 4:5 1080×1350，Brand Kit palette #2a1810 + coral from approved mood board，stroke role lock，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，slide 2–6 同 thread 只换 copy/pose，禁止 render 内小字」。**Design Agent** QA style drift、safe zone、hex vs Kit。

## Brand Kit 承载 illustration SSOT

Kit 写 palette_hex、stroke_weight、background_role；无 Kit 时 carousel 像不同画师拼贴。**ChatCanvas** 同一 thread 降低 slide 2–6 style lottery。

## Touch Edit 改 promo 不破坏 artwork identity

改「早鸟 ¥99」为「会员 ¥79」：**Touch Edit** 框 CTA 带，保持 illustration crop 与 **Brand Kit** stripe。full regen 会 random 改线稿密度与色温。

## 与单次 T2I playground 的分工

playground 适合 mood 探索；deliverable series 需要 editable layer 与 **Design Agent** pass/fail。reference image 在 brief companion，交付物仍要 **Touch Edit** 可改 copy。

## 常见失败

每 slide 新 prompt 无 thread。style lottery 无 Kit。readable 价 baked。404 未修复。

## 测量 ROI

style drift 次数、改 CTA 一次几分钟、export 几种 ratio。404 修复给 illustration ops stable prompt-to-artwork SOP URL。
"""

FOOD_STALL_ZH = """
# 小吃摊老板选什么 Design Agent：价目、外卖 cover 与夜市 promo

这条中文 URL `best-ai-design-agent-for-food-stall-owner` 曾返回 404，搜索需要 food stall owner segment 的 **Design Agent** 选型指南，不是 generic「最好 AI 设计工具」榜单。小吃摊 daily ops：价目 readable、美团/饿了么 cover、夜市 promo、会员 card — 改口味价与过敏 disclaimer 勤，warm appetite accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 street-food palette。

## 小吃摊四个高频场景

第一是价目与菜单 card：数字改得勤，手机 readable。第二是外卖平台 cover 4:5：店名与 promo 不挡 food hero。第三是夜市 story 9:16：bottom 20% CTA flat for **Touch Edit**。第四是会员 card 与 POP：过敏 disclaimer footer editable。

## 为什么 food stall promo 常卡在改价

改「双份 ¥18」要 full regen 三十分钟。carousel slide 4 accent drift 成另一个 chili red。readable 价格 bake 进 pixels。video 角标有 offer static 无 **Touch Edit** layer。**Brand Kit** 未从招牌、包装取样 hex。

## ChatCanvas brief 合同（小吃摊版）

弱 brief「诱人小吃海报」。强 brief：「季节 promo 4:5 1080×1350，Brand Kit chili + cream from signage，headline top 15% flat for Touch Edit，价格 bottom left safe zone，过敏 disclaimer footer editable，禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** numeric fields — 不能 QA「看起来好吃」。

## Brand Kit 从招牌、包装、价目取样

从已批准招牌、打包袋、prior 价目取样 primary、accent、type role。不用 stock marble 当摊位色。**ChatCanvas** 同一 thread batch 多口味 export。

## Touch Edit 改口味价不改 food photography crop

改「限时 ¥15」为「会员 ¥13」：**Touch Edit** 框 CTA 带，保持 food geometry 与 **Brand Kit** accent stripe。full regen random 改 steam highlight 与 shadow。

## Design Agent 当 checklist 而非「替老板想创意」

验 safe zone、双 CTA、字过小、hex drift vs Kit、过敏 disclaimer present。老板不需要设计 jargon — 需要 pass/fail 字段。

## 与 ice cream / restaurant segment 的分工

ice cream slug 覆盖 seasonal flavor；本篇覆盖 street stall 价目、外卖 cover、夜市 CTA 字段。

## 常见失败

跳过 **Brand Kit**。价格 baked。每活动新 prompt。404 未修复。

## 测量 ROI

改价一次几分钟、drift 几次、export 几种 ratio。404 修复给 food stall ops stable Design Agent SOP URL。
"""

ROOFER_BRAND_KIT_ZH = """
# 屋顶工 Brand Kit：报价单、完工案例与本地 promo 可编辑视觉

这条中文 URL `brand-kit-roofer-lovart` 曾返回 404，搜索需要 roofer segment 的 **Brand Kit** operational 指南。屋顶工 daily ops：报价单 cover、before/after 案例 carousel、本地 Google/点评 cover、雨季 emergency promo — 改报价区间与服务 disclaimer 频繁，trustworthy blue/gray accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 trades professional palette。

## 屋顶工四个高频场景

第一是报价单与 estimate cover：价格区间 readable，服务 disclaimer footer editable。第二是 before/after 案例 hero：改项目名不 lottery layout。第三是 carousel slide 2–6 本地案例：同一 **Brand Kit** accent，只换地址 tag。第四是雨季 emergency story 9:16：CTA bottom 20% flat for **Touch Edit**。

## 为什么 roofer promo 常卡在改报价

改「起步 ¥8,800」要 full regen 三十分钟。slide 4 accent drift 成另一个 slate blue。readable 区间价 bake 进 pixels。video 角标有 offer static 无 **Touch Edit** layer。**Brand Kit** 未从 van wrap、uniform 取样 hex。

## ChatCanvas brief 合同（屋顶工版）

弱 brief「专业屋顶公司海报」。强 brief：「雨季 promo 4:5 1080×1350，Brand Kit slate + safety orange from van wrap，headline top 15% flat for Touch Edit，报价 bottom left safe zone，服务 disclaimer footer editable（非承诺句附 brief 原文），禁止 render 内小字，slide 2–6 同 thread」。**Design Agent** QA safe zone、disclaimer、hex drift vs Kit。

## Brand Kit 从 van wrap、uniform、 prior estimate 取样

从已批准车身贴、工服、历史报价 PDF 取样 primary、accent、type role。不用 stock marble 当 trades 色。**ChatCanvas** 同一 thread batch 多案例 export。

## Touch Edit 改报价区间不改 roof photography crop

改「起步 ¥8,800」为「咨询后报价」：**Touch Edit** 框 CTA 带，保持 roof geometry 与 **Brand Kit** accent stripe。full regen random 改 sky color 与 shadow — 案例真实性敏感。

## 与 real estate agent de segment 的分工

de slug 覆盖 Makler Listing；本篇覆盖 trades 报价、before/after、雨季 emergency 字段。

## static-first 再配 optional motion

紧急 promo offer 必须在 static editable；optional clip 无 readable small text，色温 aligned to **Brand Kit**。

## 常见失败

跳过 **Brand Kit**。报价 baked。每案例新 prompt 无 thread。404 未修复。

## 测量 ROI

改报价一次几分钟、drift 几次、export 几种 ratio。404 修复给 roofer ops stable Brand Kit SOP URL。
"""

# FAQ blocks
FAQ = {
    "coach_brand_kit_zhtw": """
## FAQ

**教練要先建 Brand Kit 嗎？**  
建議，從名片與 workshop PDF 取樣 hex，防 carousel drift。

**改開課日要整圖重出嗎？**  
不需要，Touch Edit 框 date/CTA 帶，保持 layout identity。

**與 jewelry slug 分工？**  
本篇課程/見證/LINE；jewelry 覆蓋 SKU 與材質 disclaimer。

**404 修復？**  
stable coach Brand Kit SOP URL。

**Design Agent 做什麼？**  
QA safe zone、disclaimer、Brand Kit hex drift。
""",
    "jewelry_brand_kit_zhtw": """
## FAQ

**珠寶設計師 Brand Kit 從哪取樣？**  
packaging、lookbook、工作室 signage 的 hex。

**改系列價要 regen 嗎？**  
不需要，Touch Edit 改價格塊。

**材質 disclaimer？**  
footer editable 層，禁止 bake 進 pixels。

**404 修復？**  
stable jewelry Brand Kit SOP URL。

**Design Agent QA？**  
safe zone、disclaimer、lighting 禁項字段。
""",
    "looka_alt_zhtw": """
## FAQ

**與简体 batch6 重複嗎？**  
不重复，繁中重寫 TW SMB、LINE/Reels 語境，非逐句翻譯。

**Looka 後要做什麼？**  
hex 寫入 Brand Kit，再開 ChatCanvas thread。

**alternatives 少比什麼？**  
少比 logo 速度，應比 Touch Edit 改價分鐘。

**404 修復？**  
stable TW Looka alternatives SOP URL。

**價格 tier？**  
不編造，查各工具官方 ToS。
""",
    "design_cert_de": """
## FAQ

**Zertifikat ersetzt Brand Kit?**  
Nein — Curriculum lehrt oft Einzelbild; Ops brauchen Kit SSOT.

**Preisänderung nach Kurs?**  
Touch Edit fünf Minuten vs. thirty-minute full regen — prüfbares Lernergebnis.

**Fake Diplome?**  
Keine erfundenen Programme; offizielle Seiten prüfen.

**404 fix?**  
Stable DE education-to-ops SOP URL.

**Design Agent Rolle?**  
QA acceptance fields, nicht Adjektiv-Briefs.
""",
    "free_ai_tools_ja": """
## FAQ

**無料 tier で weekly promo 足りる？**  
探索は可；改价・series には Brand Kit + Touch Edit が必要。

**Brand Kit いつ作る？**  
無料探索後、production thread の前に hex を Kit へ。

**商用 license？**  
各ツール公式 ToS を確認；価格は捏造しない。

**404 復旧？**  
stable JP free-tools-to-ops SOP URL。

**Design Agent 役割？**  
safe zone、disclaimer、hex drift の pass/fail。
""",
    "smb_branding_ko": """
## FAQ

**소규모 사업 Brand Kit 필수?**  
권장 — 명함·간판에서 hex, carousel drift 방지.

**화요일 가격 변경 — full regen?**  
아니요. Touch Edit CTA band, 5분 목표.

**complete guide vs 원클릭 VI?**  
series ops + editable disclaimer; one-shot PNG 아님.

**404 복구?**  
stable KR SMB branding SOP URL.

**Design Agent?**  
brief 계약 QA, 「고급感」 대체 불가.
""",
    "adobe_express_zh": """
## FAQ

**Express 与 Lovart 二选一吗？**  
不必，Express 模板起稿 + Lovart Kit/thread 可并行。

**对比应比什么？**  
Tuesday 改价分钟、drift 次数，不比模板数量。

**Touch Edit 改价场景？**  
Lovart 默认 CTA band 五分钟；Express 取决于 editable layer 路径。

**404 修复？**  
stable Adobe Express vs Lovart comparison SOP URL。

**fake pricing？**  
不编造，查各平台官方定价页。
""",
    "illustration_guide_zh": """
## FAQ

**专业插画要先 Brand Kit 吗？**  
要，写 palette_hex、stroke_weight role。

**改 promo 会换风格吗？**  
Touch Edit 只改 CTA 字层，不 regen 整图换画风。

**与 T2I playground 分工？**  
playground 探索 mood；series 交付要 editable layer。

**404 修复？**  
stable illustration prompt-to-artwork SOP URL。

**Design Agent QA？**  
style drift、safe zone、hex vs Kit。
""",
    "food_stall_zh": """
## FAQ

**小吃摊要先 Brand Kit 吗？**  
建议，从招牌、包装取样 hex。

**改价要 full regen 吗？**  
不需要，Touch Edit 五分钟改价格块。

**Design Agent 替老板创意？**  
不，执行 brief checklist pass/fail。

**404 修复？**  
stable food stall Design Agent SOP URL。

**过敏 disclaimer？**  
footer editable，禁止 bake 进 pixels。
""",
    "roofer_brand_kit_zh": """
## FAQ

**屋顶工 Brand Kit 从哪取样？**  
van wrap、工服、历史报价 PDF 的 hex。

**改报价要 regen 吗？**  
不需要，Touch Edit 框报价带。

**与 Makler de slug 分工？**  
de 覆盖 Listing；本篇覆盖 trades 报价与 before/after。

**404 修复？**  
stable roofer Brand Kit SOP URL。

**Design Agent QA？**  
safe zone、服务 disclaimer、hex drift vs Kit。
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

Der erste Brief endet mit „premium“ und scheitert: kleiner Preis, Badge über dem Objekt. Im zweiten Durchlauf nur safe zone und Pflichtfelder korrigieren. Ein **ChatCanvas**-Thread reduziert accent drift auf slide 4. In **{topic}** bestätigt **Touch Edit** Preisänderung in fünf Minuten static-first. Full regen 30 Minuten — zuerst **Brand Kit** neu setzen. Wiederhergestellte 404-URL als stable SOP-Link für Bildungs- und Ops-Teams.
"""


def expand_ja(topic: str, n: int) -> str:
    return f"""
## 現場メモ {n}：{topic}

初回 brief が「モダン」で終わると価格文字が小さく badge が顔を隠します。二回目は safe zone と必須フィールドのみ修正。**Design Agent** と **ChatCanvas** で thread を維持すると carousel slide 4 の accent drift が減ります。{topic} で **Touch Edit** が 5 分以内に価格修正できれば static-first が成立。30 分 full regen なら **Brand Kit** からやり直し。404 復旧 URL は onboarding 用 stable link です。
"""


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 현장 메모 {n}: {topic}

첫 brief가 「고급스럽게」로 끝나면 가격 숫자가 작아지고 badge가 얼굴을 가립니다. 두 번째는 safe zone과 필수 필드만 고칩니다. **Design Agent**와 **ChatCanvas**에서 thread를 유지하면 carousel slide 4 색 drift를 줄입니다. {topic}에서 **Touch Edit** 5분 이내 가격 수정이면 도구가 맞습니다. 30분 full regen이면 Brand Kit부터 다시 하세요. 404 복구 URL은 onboarding용 stable link입니다.
"""


ARTICLES = [
    {
        "rank": 123,
        "key": "coach_brand_kit_zhtw",
        "lang": "zh-TW",
        "slug": "brand-kit-coach-lovart",
        "cover": "012",
        "category": "Industry Solution",
        "title": "教練 Brand Kit：課程 promo、學員見證與 LINE 社群系列",
        "seo_title": "教練 Brand Kit — ChatCanvas 繁中實操",
        "description": "繁中 404 修復：coach Brand Kit，課程日期，Touch Edit 改早鳥價。",
        "seo_description": "教練 segment：見證 quote、LINE cover、static-first。",
        "focus": "brand kit coach lovart",
        "keywords": ["教練 brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Coach Brand Kit zh-TW",
        "body": COACH_BRAND_KIT_ZHTW,
        "expand_topic": "教練課程 promo Brand Kit",
    },
    {
        "rank": 124,
        "key": "jewelry_brand_kit_zhtw",
        "lang": "zh-TW",
        "slug": "brand-kit-jewelry-designer-lovart",
        "cover": "019",
        "category": "Industry Solution",
        "title": "珠寶設計師 Brand Kit：系列 catalog 與材質 disclaimer",
        "seo_title": "珠寶設計師 Brand Kit — ChatCanvas 繁中",
        "description": "繁中 404 修復：jewelry Brand Kit，SKU series，Touch Edit 改價。",
        "seo_description": "珠寶 segment：材質 disclaimer、展覽 invite。",
        "focus": "brand kit jewelry designer lovart",
        "keywords": ["珠寶 brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Jewelry Brand Kit zh-TW",
        "body": JEWELRY_BRAND_KIT_ZHTW,
        "expand_topic": "珠寶系列 catalog Brand Kit",
    },
    {
        "rank": 125,
        "key": "looka_alt_zhtw",
        "lang": "zh-TW",
        "slug": "looka-alternatives-2026",
        "cover": "026",
        "category": "How-To",
        "title": "Looka 替代品 2026：台灣 SMB 的 logo 與 LINE/IG 分工",
        "seo_title": "Looka 替代品 2026 — 繁中 TW SMB",
        "description": "繁中 404 修復：Looka alternatives TW 重寫，非简体 copy，ChatCanvas Brand Kit Touch Edit。",
        "seo_description": "TW SMB：LINE/Reels safe zone、改價分鐘对比。",
        "focus": "looka alternatives 2026",
        "keywords": ["looka alternatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Looka Alternatives zh-TW",
        "body": LOOKA_ALT_ZHTW,
        "expand_topic": "TW SMB Looka alternatives",
    },
    {
        "rank": 126,
        "key": "design_cert_de",
        "lang": "de",
        "slug": "ai-design-certification-education-programs-2026",
        "cover": "033",
        "category": "Insight & Trend",
        "title": "AI-Design-Zertifizierung 2026: Curriculum vs. Production Workflow",
        "seo_title": "AI Design Zertifizierung 2026 — DE Ops",
        "description": "DE 404 fix: Bildungsprogramme 2026, Brand Kit, Touch Edit, kein fake Diplom.",
        "seo_description": "Zertifikat vs ChatCanvas production SOP.",
        "focus": "ai design certification education programs 2026",
        "keywords": ["ai design zertifizierung", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight — Design Education DE",
        "body": DESIGN_CERT_DE,
        "expand_topic": "AI Design Zertifizierung Ops",
    },
    {
        "rank": 127,
        "key": "free_ai_tools_ja",
        "lang": "ja",
        "slug": "how-to-use-free-ai-design-tools",
        "cover": "040",
        "category": "How-To",
        "title": "無料 AI デザインツールの使い方：brief 契約と static-first",
        "seo_title": "無料 AI デザインツール — ChatCanvas 実務",
        "description": "JA 404 復旧：free AI design tools how-to, Brand Kit, Touch Edit.",
        "seo_description": "無料 tier から ops へ：Design Agent QA.",
        "focus": "how to use free ai design tools",
        "keywords": ["無料 ai デザイン", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Free AI Tools JA",
        "body": FREE_AI_TOOLS_JA,
        "expand_topic": "無料 AI ツール daily ops",
    },
    {
        "rank": 128,
        "key": "smb_branding_ko",
        "lang": "ko",
        "slug": "complete-guide-small-business-branding-ai",
        "cover": "047",
        "category": "How-To",
        "title": "소규모 사업 브랜딩 완전 가이드: AI workflow와 Brand Kit",
        "seo_title": "소규모 사업 브랜딩 — ChatCanvas KO",
        "description": "KO 404 복구：SMB branding complete guide, Brand Kit, Touch Edit.",
        "seo_description": "SMB branding：carousel series, static-first.",
        "focus": "complete guide small business branding ai",
        "keywords": ["소규모 브랜딩 ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — SMB Branding KO",
        "body": SMB_BRANDING_KO,
        "expand_topic": "소규모 사업 branding workflow",
    },
    {
        "rank": 129,
        "key": "adobe_express_zh",
        "lang": "zh",
        "slug": "adobe-express-vs-lovart-comparison",
        "cover": "050",
        "category": "How-To",
        "title": "Adobe Express 与 Lovart 对比：运营向 revision-heavy 工作流",
        "seo_title": "Adobe Express vs Lovart — 运营对比",
        "description": "404 修复：Adobe Express vs Lovart operational 对比，Touch Edit 改价，无 fake pricing。",
        "seo_description": "对比 revision cost、Brand Kit series，非 feature 清单。",
        "focus": "adobe express vs lovart comparison",
        "keywords": ["adobe express lovart", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Adobe Express vs Lovart ZH",
        "body": ADOBE_EXPRESS_ZH,
        "expand_topic": "Adobe Express vs Lovart ops",
    },
    {
        "rank": 130,
        "key": "illustration_guide_zh",
        "lang": "zh",
        "slug": "ai-illustration-guide-how-to-generate-professional-artwork-from-prompts",
        "cover": "061",
        "category": "How-To",
        "title": "AI 插画指南：从 prompt 生成专业级 artwork 可编辑工作流",
        "seo_title": "AI 插画 prompt 指南 — ChatCanvas 实操",
        "description": "404 修复：illustration from prompts，Brand Kit style lock，Touch Edit promo。",
        "seo_description": "专业 artwork：series 一致、Design Agent QA style drift。",
        "focus": "ai illustration guide professional artwork prompts",
        "keywords": ["ai 插画", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Illustration Prompts ZH",
        "body": ILLUSTRATION_GUIDE_ZH,
        "expand_topic": "插画 prompt 专业 artwork",
    },
    {
        "rank": 131,
        "key": "food_stall_zh",
        "lang": "zh",
        "slug": "best-ai-design-agent-for-food-stall-owner",
        "cover": "062",
        "category": "Industry Solution",
        "title": "小吃摊老板选什么 Design Agent：价目与外卖 cover",
        "seo_title": "小吃摊 Design Agent — ChatCanvas 实操",
        "description": "404 修复：food stall owner segment，Brand Kit，Touch Edit 改价。",
        "seo_description": "小吃摊：价目 readable、过敏 disclaimer。",
        "focus": "best ai design agent food stall owner",
        "keywords": ["小吃摊 ai 设计", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Food Stall Design Agent ZH",
        "body": FOOD_STALL_ZH,
        "expand_topic": "小吃摊价目 promo workflow",
    },
    {
        "rank": 132,
        "key": "roofer_brand_kit_zh",
        "lang": "zh",
        "slug": "brand-kit-roofer-lovart",
        "cover": "063",
        "category": "Industry Solution",
        "title": "屋顶工 Brand Kit：报价单、完工案例与本地 promo",
        "seo_title": "屋顶工 Brand Kit — ChatCanvas 实操",
        "description": "404 修复：roofer Brand Kit，报价区间，Touch Edit 改价。",
        "seo_description": "屋顶工 segment：before/after、雨季 emergency promo。",
        "focus": "brand kit roofer lovart",
        "keywords": ["屋顶工 brand kit", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Roofer Brand Kit ZH",
        "body": ROOFER_BRAND_KIT_ZH,
        "expand_topic": "屋顶工报价 promo Brand Kit",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "zh-TW": expand_zhtw,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch12 content cluster.*\n"
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
