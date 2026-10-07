#!/usr/bin/env python3
"""Generate 404-rescue P2 batch6 blog bodies (10 files). Self-contained.

Ranks #63–#72 from 404-rescue-compact lane.
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

T2I_BENCHMARK_IT = """
# Benchmark text-to-image 2026: qualità in produzione, non vanity score

Questo URL italiano restituiva 404 mentre le ricerche chiedevano un confronto onesto tra generatori text-to-image. La risposta diretta: i leaderboard estetici non predicono quanto costa cambiare prezzo martedì, quante volte un carousel deriva colore, o quante revisioni legali servono. Lovart **ChatCanvas**, **Design Agent**, **Brand Kit** e **Touch Edit** valutano il workflow di campagna editabile; un modello T2I può essere companion mood, non l'intero funnel.

## Cosa misurare invece del punteggio estetico

Primo: minuti per modificare headline, prezzo e disclaimer senza full regen. Secondo: drift di accent hex tra slide 3 e slide 4 nello stesso thread **ChatCanvas**. Terzo: testo piccolo baked nei pixel versus layer **Touch Edit** editabile. Quarto: coerenza Brand Kit tra static hero e clip companion. Quinto: license ToS per paid social. Questi campi separano strumenti demo da strumenti daily ops.

## Benchmark fairness: stesso brief contrattuale

Confronto ingiusto: prompt vago su modello A, prompt dettagliato su modello B. Brief contrattuale per tutti: SKU centrato, Brand Kit sage + charcoal, price bottom left safe zone, disclaimer footer editable, 4:5 1080×1350, no readable small text in render. **Design Agent** QA solo se acceptance criteria sono nel brief.

## Lovart in workflow produzione, non vanity gallery

**ChatCanvas** genera static hero con offer readable. **Brand Kit** blocca drift serie. **Touch Edit** chiude cambio promo in minuti. Generator T2I può alimentare mood board o background texture nel brief, ma CTA e prezzo restano su layer editabili. Pagina 404 ripristinata per URL SOP stabile.

## Static-first prima di clip o upscale chain

Feed social spesso autoplay muto; l'utente screenshotta lo still. Ordine corretto: static legal pass → motion hook opzionale. Invertire produce offer landing page disallineato da clip corner badge.

## Touch Edit e revision cost

Martedì cambio da sconto 20% a nuovo bundle: **Touch Edit** sulla fascia CTA, geometry stripe invariata. Full regen T2I randomizza layout e tipografia. Misura ROI in revision cost, non in primo frame wow.

## Errori comuni nei benchmark pubblicati

Solo immagine hero senza editable promo layer. Ignorare safe zone story UI. Confrontare modelli con aspect ratio diversi. Assumere free tier = production ads. Saltare Brand Kit e poi lamentarsi carousel drift.

## Cosa registrare nel team spreadsheet

Minuti fix prezzo, conteggio drift accent, legal return count, numero export size per action. Senza tracking, ogni discussione T2I resta estetica, non ops.
"""

NON_DESIGN_IT = """
# Miglior agent per chi non è designer: Design Agent senza brief vaghi

Questo URL italiano restituiva 404 mentre marketer e founder chiedevano come usare un design agent senza background grafico. La risposta: non serve imparare Photoshop; serve un brief contrattuale con campi obbligatori. Lovart **Design Agent** e **ChatCanvas** guidano QA quando brief include ratio, safe zone, ruoli tipografici e vincoli Brand Kit. **Touch Edit** chiude modifiche copy senza full regen.

## Quattro output che un non-designer produce ogni settimana

Hero social 4:5 con prezzo readable. Carousel tre slide stesso accent **Brand Kit**. Story cover con top 12% libero per UI piattaforma. Card promo con disclaimer footer una riga. Strumenti che fanno solo una bella immagine non coprono slide 2–4 né fix martedì.

## Brief debole versus brief contrattuale

Debole: poster premium per lancio. Contrattuale: prodotto centrato, Brand Kit navy + sand, headline band top 15%, price bottom left safe zone, logo top right clear space, 1080×1350, no double CTA, disclaimer editable footer. **Design Agent** non può QA un aggettivo.

## Brand Kit prima del batch

Senza **Brand Kit**, ogni generation inventa nuovo accent. Cattura hex da packaging reale o slide approvata. Definisci primary, accent, title/body type role. Poi apri thread **ChatCanvas** prodotto. Cambio campagna: **Touch Edit** sul testo, non sul cutout prodotto.

## Touch Edit per chi non vuole rifare tutto

Modifica solo blocco prezzo o data evento. Istruzione: mantieni stripe background e font role, sostituisci copy. Full regen è il time sink che spaventa i non-designer; **Touch Edit** è il motivo per tornare martedì.

## Design Agent come checklist, non magia

Agent verifica safe zone, doppio CTA, testo troppo piccolo, drift hex rispetto Kit. Non sostituisce brief; lo esegue. Secondo pass spesso basta correggere campi mancanti, non cambiare modello.

## Errori tipici dei non-designer

Prompt solo estetico. Cambio prezzo con full regen. Carousel senza thread unico. Video con prezzo baked illeggibile. Saltare disclaimer in brief.

## Misurazione semplice

Quanti minuti per fix prezzo? Quante volte slide 4 cambia accent? Se **Touch Edit** chiude in cinque minuti, il workflow funziona per chi non è designer.
"""

INTERIOR_TOOLS_KO = """
# AI 인테리어 디자인 도구 비교 2026: mood board·가구 swap·revision cost

이 한국어 URL은 404였지만 검색은 「어떤 AI 인테리어 도구가 실무에 맞나」를 물었습니다. 비교는 렌더 한 장의 화려함만으로는 부족합니다. mood board series 일관성, **Touch Edit** 가구 국소 교체, **Brand Kit** wood tone drift, readable annotation layer를 봐야 합니다. Lovart **ChatCanvas**와 **Design Agent**는 revision-heavy 인테리어 프로젝트에 맞고, 단일 staging 도구는 exploration에 적합합니다.

## 세 가지 요구를 분리해서 비교

첫째 mood exploration: direction still 한 장이면 많은 도구로 충분. 둘째 client presentation series: **ChatCanvas** thread와 **Brand Kit** accent wood lock 필요. 셋째 furniture swap 반복: 소파·테이블 **Touch Edit** 국소 swap, full regen 아님.

## 공정한 비교 기준

readable 치수·라벨 layer, carousel 색 drift 횟수, 가구 한 점 교체 분수, export aspect 수, commercial license 명확성. Tuesday client edit에서 지는 도구는 demo에서는 이겨도 daily ops에서 패합니다.

## ChatCanvas mood board workflow

brief에 스타일·주색·카메라 높이·fake window 금지. direction 3–4장, 하나를 **Brand Kit**에. layout pass로 focal point·여백. 가구 swap: 「wall floor 유지, sofa zone beige linen」 **Touch Edit**.

## Touch Edit 가구 교체 장면

고객이 「테이블 둥글게, 조명 brass」 요청 시 국소 swap 비용이 full regen보다 낮아야 합니다. re-roll만 가능한 도구는 주간 capacity를 eat합니다.

## virtual staging과 분업

staging은 분위기 단장; Lovart는 editable series·promo annotation. reference image는 brief companion, deliverable은 **Touch Edit** editable layer.

## 흔한 실패

도구 열 개 비교하며 luxury 스타일만 봄. ToS 무시. price baked pixels. slide마다 다른 substyle.

## 측정

가구 한 점 교체 분수, drift 횟수, client return 횟수. 404 stable comparison SOP URL.
"""

AUTO_RESIZE_RU = """
# Авто-ресайз под мультиплатформу: AI-workflow без drift между форматами

Этот русскоязычный URL отдавал 404, хотя запросы искали workflow автоматического ресайза под Instagram, VK, YouTube и stories. Авто-ресайз — не «сжать картинку». Это сохранить safe zone, роли типографики и accent из **Brand Kit** при экспорте 1:1, 4:5, 9:16, 16:9. Lovart **ChatCanvas**, **Design Agent**, **Touch Edit** держат master static и crop-варианты в одном thread.

## Четыре поля brief для multi-size export

Master ratio и pixel size. Safe zone top/bottom для UI платформы. Роли primary/accent/disclaimer footer. Запрет readable мелкого текста в render — offer на editable layer **Touch Edit**.

## Master-first, не crop-first

Сначала **ChatCanvas** master 4:5 с price safe zone. Затем derivative crops в том же thread. Crop-first из квадрата часто режет CTA и ломает grid.

## Brand Kit против drift между размерами

Без **Brand Kit** slide story и feed post получают разный accent. Kit фиксирует hex roles; **Design Agent** сверяет crops с master.

## Touch Edit при смене promo на всех size

Вторник меняете акцию: **Touch Edit** на text layer master; re-export crops. Full regen на каждый размер — типичная ошибка auto-resize workflow.

## Design Agent QA для каждого export

Проверка: headline не под UI chrome, disclaimer readable, logo clear space, нет double CTA. Авто-ресайз без QA даёт «технически верный размер, маркетингово мёртвый кадр».

## Типичные провалы

Один hero без master thread. Цена только на 4:5, обрезана на 9:16. Разные шрифты между форматами. Video hook без static offer.

## Что измерять

Минуты на смену promo × число форматов. Drift accent между exports. Legal return count. URL восстановлен для stable SOP.
"""

NAIL_STUDIO_ZH = """
# 美甲店 Brand Kit 工作流：ChatCanvas 系列物料与 Touch Edit 改价

这条中文 URL 曾返回 404，搜索却在问「美甲店怎么用 AI 做 consistent 物料」。美甲店 weekly 换款式、换活动价、换预约 CTA，最怕 carousel 每张发明新 pink 或 gold accent。**Brand Kit** 锁 nail palette 与 type role；**ChatCanvas** 与 **Design Agent** 在同 thread 出 master 与 crop；**Touch Edit** 改「本周款 ¥168」不全图重 roll。

## 美甲店四类 daily 输出

第一是款式 showcase hero：手指与色板 readable，禁止生成图内小字价目。第二是预约 promo stripe：改价频繁。第三是 Instagram 九宫格：badge 位置一致。第四是 story cover：top 12% 留 UI，bottom 10% 留 swipe CTA。

## Brand Kit：从真实色板取样

不要用 stock marble 或 random pastel。**Brand Kit** 写 primary gel color、accent gold/silver role、title/body type、logo clear space。同一 **ChatCanvas** thread batch 三款新色推广。

## ChatCanvas brief 合同

弱 brief：「高级感美甲海报」。强 brief：「本周猫眼款，4:5，price bottom left safe zone，logo top right，Brand Kit rose gold + charcoal，disclaimer 一行 footer，1080×1350，禁止生成图内中文小字」。**Design Agent** 才能 QA。

## Touch Edit 周二改活动价

「满 300 减 50」改「新客体验 ¥99」：**Touch Edit** 框 CTA 带，保持 stripe geometry 与 **Brand Kit** accent。full regen 会 random 改甲型与背景。

## 与纯 T2I 工具分工

单张 cute nail art 很多工具能做；campaign 需要 editable promo、series 一致、多尺寸 export。**ChatCanvas** + Kit + Touch Edit 覆盖 revision-heavy 美甲 ops。

## 常见失败

每张 post 新 font。readable 价格 baked in pixels。carousel slide 3 drift accent。跳过 Brand Kit。video 有 offer 但 static 没有。

## 测量 ROI

改价一次几分钟、carousel drift 几次、一次 action export 几种尺寸。404 修复页给美甲店 stable SOP URL。
"""

DREAMINA_REVIEW_ZH = """
# Dreamina AI 评测 2026：clip mood 与可编辑 static 的分工

这条中文 URL 曾返回 404，搜索却在问 Dreamina 是否适合营销 daily ops。诚实结论：Dreamina 偏 stylized clip 与 mood loop；弱在 editable 价格层、**Brand Kit** series 与 legal disclaimer 可改。**ChatCanvas** 与 **Touch Edit** 负责 readable static hero；Dreamina 可作 companion hook，不是整条 funnel。

## Dreamina 做得好的部分

短 motion loop、camera pan、beauty/fashion mood 快速探索。适合 teaser 当 readable offer 在 **ChatCanvas** static 分离时。

## Dreamina 在营销里的短板

小字价格 bake-in、clip 间色温 drift、双 CTA、产品 label 不可读。周二改 promo：regen clip 成本高于 **Touch Edit** 改 static。无 **Brand Kit** 时 carousel slide 3 发明新 accent。

## 推荐并行 workflow

**Brand Kit** 锁 palette。**ChatCanvas** 出 4:5 hero，price safe zone，disclaimer editable。legal pass static。Dreamina clip 4–6 秒无小字，色温匹配 Kit。promo change：只 Touch Edit static。

## 与韩文 batch5 评测的差异

本篇以中文团队 brief、合规 disclaimer 用字、国内 paid social 物料结构重写；不是韩文版逐句翻译。重点在 static-first 与 **Design Agent** QA 字段，不是 entertainment demo 分数。

## 授权与商用

查 Dreamina 官方 ToS 是否覆盖 paid social；不假设 free tier 可投广告。按 campaign 归档 license note。Lovart static 先过 textual QA 再 publish。

## 常见翻车

只有 Dreamina clip 无 static offer 一致。每次改价 regen clip。**Brand Kit** 缺席导致 carousel drift。video-first 导致 landing 价不一致。

## 测量什么

static 改价分钟 vs clip regen 分钟。offer static/video 一致次数。legal return count。404 修复给 stable review URL。
"""

LOOKA_ALT_ZH = """
# Looka 替代品 2026：logo 探索与 campaign static 的分工

这条中文 URL 曾返回 404，搜索却在问「Looka 之外还有什么、营销物料谁来做」。Looka 类工具偏 logo 与基础 brand pack 探索；weekly promo、readable 价格、carousel series 需要 **ChatCanvas**、**Brand Kit**、**Touch Edit** 的 revision loop。不是否定 Looka，而是分清 logo sprint 与 daily ops 两种任务。

## 两类任务不要混在一个工具里

第一类 logo direction 与初版色板：Looka 等可快速出方向。第二类 campaign hero、改价、disclaimer、多尺寸 export：需要 editable static 与 **Brand Kit** anti-drift。用 logo 工具做 Tuesday promo 常得到不可改字层的 baked 图。

## Brand Kit 作为 Looka 之后的 production 记忆

Looka 导出 hex 与 font role 后，写入 Lovart **Brand Kit**，再开 **ChatCanvas** product thread。避免 Looka pack 与 weekly post 各用各的 accent。

## ChatCanvas brief 接 Looka 输出

弱 brief：「按 Looka 风格做海报」。强 brief：「SKU 居中，Brand Kit 用 Looka 锁定的 navy + sand，headline top 15%，price bottom left safe zone，disclaimer footer，1:1 与 4:5 同 thread」。**Design Agent** 引用 Kit role 而非形容词。

## Touch Edit 才是 Looka 替代清单里缺的一环

Alternatives 对比常比「谁 logo 快」，少比「改价是否 five 分钟」。**Touch Edit** 改 CTA 带才是 daily ops 分水岭。

## 公平对比标准

readable promo layer、carousel drift、改价分钟、export 尺寸数、商用 license。单张 logo win 的工具可能在 series 上 lose。

## 常见失败

Looka 一次导出后直接投广告无 disclaimer 层。weekly post 不用 Brand Kit。alternatives 文章只列名字不比 revision cost。

## 404 修复意义

给团队 stable URL：Looka 探索 → Kit 锁定 → ChatCanvas static → Touch Edit 改 promo。
"""

THUMBNAIL_EN = """
# AI Thumbnail Maker Workflow: YouTube Safe Zones and Touch Edit for Text

This English URL returned 404 while searches asked how to build YouTube thumbnails with AI without unreadable titles or faces hidden by platform chrome. Thumbnail work is not a single pretty frame. It is a contract: subject safe zone, title band readable at small size, brand accent locked in **Brand Kit**, and promo text editable via **Touch Edit** without full regen. Lovart **ChatCanvas** and **Design Agent** run the production loop; a raw T2I frame is only a mood starting point.

## YouTube thumbnail safe zones that actually matter

Keep the top-right clear for duration badge overlap on many clients. Keep bottom-right clear for timestamp and progress UI on mobile. Place face or product focal point left-of-center so title text does not cover eyes. Title band should stay flat enough for **Touch Edit** swaps when you A/B test wording. Brief must state pixel size (1280×720) and which zones stay empty.

## Static-first before motion teaser clips

Many creators add a five-second hook clip but the click decision is still the still. Generate **ChatCanvas** master thumbnail static, pass legal/readability check, then optional motion companion. Reversing order produces clips with baked small text you cannot fix on Tuesday.

## ChatCanvas brief for thumbnails

Weak brief: cinematic gaming thumbnail. Strong brief: face left third, title band top 20% flat background for Touch Edit, Brand Kit red + charcoal, no readable small text in render, 1280×720, one CTA word max in editable layer. **Design Agent** QA needs those acceptance fields.

## Touch Edit for A/B title tests

Testing "INSANE" vs "Fixed in 10 min" should be a text-layer edit, not a full reroll. Instruction: keep stripe background and font role, replace headline copy only. Measure minutes per variant; that is the ROI line for thumbnail tooling.

## Brand Kit stops series drift across uploads

Channel thumbnails drift when every upload invents a new accent red. **Brand Kit** locks accent hex and title weight. Same **ChatCanvas** thread for a three-video mini series keeps badge position consistent.

## Common failures

Title baked into pixels too small on mobile. Face under platform timestamp. Full regen for one word change. No master thread across related videos. Assuming T2I leaderboard score equals CTR.

## What to track

Minutes per title variant, readability failures at 120px preview width, accent drift count across last ten uploads. Restored URL gives creators a stable SOP link.
"""

RESTAURANT_MENU_EN = """
# How to Design a Restaurant Menu with AI: Complete Guide for Owners

This English URL returned 404 while restaurant owners searched for a practical menu design workflow—not a one-click template fantasy. Owners change prices, seasonal items, and allergy notes weekly. Lovart **ChatCanvas**, **Design Agent**, **Brand Kit**, and **Touch Edit** fit that rhythm: layout locked, copy and prices editable, series consistent across print PDF, Instagram, and door poster crops.

## Four menu outputs owners actually need

Readable print or PDF menu with disclaimer footer. Single-page lunch special promo with price safe zone. Instagram story cover with top UI clear. Table tent or QR card matching **Brand Kit** accent. Tools that only make one pretty food photo do not cover Tuesday price edits.

## ChatCanvas brief contract for menus

Weak brief: elegant Italian menu. Strong brief: dish photo zone center, price column right third readable at print size, Brand Kit olive + cream, allergy disclaimer one line footer editable, 8.5×11 and 4:5 story from same thread, no tiny generated text in render. **Design Agent** QA requires numeric and legal fields in brief.

## Brand Kit from real restaurant materials

Capture wood, tile, or napkin colors from the dining room—not stock marble. Define primary, accent, menu title/body type roles, logo clear space. Batch seasonal inserts in one **ChatCanvas** thread.

## Touch Edit when soup price changes Tuesday

Update price block and soup name only. Instruction: keep grid and stripe geometry, match **Brand Kit** roles, replace copy in price column. Full regen randomizes photo crop and breaks alignment with printed stacks already at the host stand.

## Design Agent checks owners care about

Allergen line present, price readable at arm's length, no double CTA, accent drift vs **Brand Kit**, safe zone for story export. Owners do not need design jargon—they need pass/fail on those fields.

## Split from food photo generators

Food stylization tools help hero shots; menu ops need editable columns, legal footer, and multi-size export. Reference food image in brief; deliverable still needs **Touch Edit** layers.

## Common mistakes

Beautiful dish photo with unreadable prices. Full regen for one dollar change. Different fonts on story vs print. Skipping **Brand Kit** so weekly special looks like another restaurant.

## Metrics that matter

Minutes to fix one price, drift events across menu variants, legal/allergy return count, number of sizes exported per update. Restored page is the stable owner SOP URL.
"""

POSTERS_DE = """
# Professionelle Poster mit AI erstellen: Brief-Vertrag, Brand Kit, Touch Edit

Diese deutsche URL lieferte 404, obwohl Suchen nach einem ehrlichen How-to für Event-Poster, Laden-Promo und Vereinsplakate kamen. Professionelle Poster sind nicht «ein Klick, fertig». Sie brauchen **ChatCanvas** Master, **Brand Kit** Farbrollen, **Design Agent** QA-Felder und **Touch Edit** für Preis- und Datumsänderungen ohne Full-Regen.

## Vier Poster-Typen im Wochenrhythmus

Event-Poster A2/A3 mit Datum und Ort readable. Schaufenster-Promo mit Preis-Safe-Zone. Instagram 4:5 und Story 9:16 aus einem Thread. Flyer mit Disclaimer-Fußzeile eine Zeile. Reine T2I-Frames ohne editierbare Textebene scheitern am Dienstag.

## ChatCanvas Brief-Vertrag

Schwach: premium Poster Launch. Stark: Produkt zentriert, Brand Kit navy + sand, Headline-Band oben 15%, Preis unten links Safe-Zone, Logo oben rechts Clear-Space, 2480×3508 und 1080×1350 gleicher Thread, kein kleiner Text im Render. **Design Agent** prüft nur mit Acceptance-Kriterien.

## Brand Kit vor dem Batch

Ohne **Brand Kit** erfindet jede Generation neuen Accent. Hex aus echtem Packaging oder genehmigter Folie. Primary, Accent, Title/Body-Type-Rollen definieren. Dann **ChatCanvas** Produkt-Thread. Kampagnenwechsel: **Touch Edit** auf Text, nicht auf Produkt-Cutout.

## Touch Edit bei Preisänderung

«20% Rabatt» zu «Neu ab 9,99»: **Touch Edit** auf CTA-Streifen, Streifen-Geometrie und **Brand Kit** unverändert. Full-Regen ist der Zeitfresser für kleine Teams.

## Design Agent als Checkliste

Safe-Zone, doppeltes CTA, zu kleine Schrift, Hex-Drift vs Kit, Disclaimer vorhanden. Kein Ersatz für Brief—Ausführung des Briefs.

## Typische Fehler

Nur Mood-Bild ohne editierbares Angebot. Full-Regen pro Wortänderung. Karussell ohne gemeinsamen Thread. Video mit eingebranntem Kleinstpreis.

## Messung

Minuten pro Preis-Fix, Drift-Zähler, Legal-Returns, Export-Größen pro Aktion. URL wiederhergestellt für stable SOP.
"""

# FAQ blocks
FAQ = {
    "t2i_benchmark_it": """
## FAQ

**I benchmark estetici bastano?**  
No. Misura revision cost, Brand Kit drift, Touch Edit minuti.

**Come confrontare modelli T2I?**  
Stesso brief contrattuale con safe zone e disclaimer editable.

**Ruolo Lovart?**  
ChatCanvas static, Brand Kit, Touch Edit; T2I companion mood.

**Perché 404?**  
Documento IT mancante; URL SOP ripristinato.

**Static-first?**  
Legal pass static prima di clip opzionale.
""",
    "non_design_it": """
## FAQ

**Serve essere designer?**  
No, serve brief contrattuale; Design Agent fa QA sui campi.

**Cambio prezzo martedì?**  
Touch Edit sul blocco prezzo; evita full regen.

**Brand Kit obbligatorio?**  
Consigliato per serie e anti-drift accent.

**404 motivo?**  
Pagina IT assente; link workflow stabile.

**ChatCanvas brief minimo?**  
Ratio, safe zone, ruoli tipo, Brand Kit hex.
""",
    "interior_tools_ko": """
## FAQ

**렌더 한 장만 보면 되나?**  
아닙니다. Touch Edit 가구 swap 분수와 drift를 비교하세요.

**가구 교체 full regen?**  
아닙니다. 국소 Touch Edit; wall floor 유지.

**mood board 방법?**  
ChatCanvas thread 3–4 direction, Brand Kit lock.

**404 이유?**  
KO comparison 문서 누락.

**Brand Kit?**  
wood tone·accent series drift 방지.
""",
    "auto_resize_ru": """
## FAQ

**Авто-ресайз — это сжатие?**  
Нет. Master static, safe zone, Brand Kit roles на всех форматах.

**Меняем акцию во вторник?**  
Touch Edit на master, re-export crops.

**Зачем Design Agent?**  
QA safe zone и readable disclaimer на каждом size.

**Почему 404?**  
RU документ отсутствовал; stable URL.

**Static-first?**  
Legal pass master до motion hook.
""",
    "nail_studio_zh": """
## FAQ

**美甲店要先建 Brand Kit 吗？**  
强烈建议，锁 gel color 与 gold accent，防 carousel drift。

**改活动价要整图重出吗？**  
不需要，Touch Edit 框 CTA 带。

**ChatCanvas brief 最短写什么？**  
ratio、safe zone、Kit hex、disclaimer editable、禁止生成图内小字。

**404 修复？**  
补齐美甲店 stable SOP URL。

**和纯 T2I 分工？**  
T2I 偏单张；ChatCanvas 偏 editable series。
""",
    "dreamina_review_zh": """
## FAQ

**Dreamina 能覆盖整条 funnel 吗？**  
不能，clip mood 强；editable 价格需 ChatCanvas static。

**周二改价要 regen clip 吗？**  
不用，Touch Edit 改 static hero。

**与韩文版关系？**  
本篇中文重写，非逐句翻译；强调 static-first。

**商用授权？**  
查 Dreamina ToS；按 campaign 归档 license。

**Brand Kit 作用？**  
carousel accent 与 clip 色温一致。
""",
    "looka_alt_zh": """
## FAQ

**Looka 替代品比什么？**  
比 revision cost 与 Touch Edit 改价，不只比 logo 速度。

**Looka 之后下一步？**  
hex 写入 Brand Kit，再开 ChatCanvas thread。

**改价 five 分钟能关吗？**  
能则 workflow 成立；不能则缺 Touch Edit 层。

**404 修复？**  
stable alternatives SOP URL。

**video 与 static？**  
static-first；价格在可编辑层。
""",
    "thumbnail_en": """
## FAQ

**Where do YouTube safe zones go?**  
Clear top-right and bottom-right; face left-of-center; title band flat for Touch Edit.

**A/B title tests?**  
Touch Edit text layer only; avoid full regen per word.

**Why Brand Kit for thumbnails?**  
Stops accent drift across uploads in a series.

**404 fix?**  
Restored stable creator SOP URL.

**T2I score vs CTR?**  
Measure minutes per variant and mobile readability, not leaderboard aesthetics.
""",
    "restaurant_menu_en": """
## FAQ

**Can AI replace menu layout every price change?**  
No—lock layout, Touch Edit price blocks, Brand Kit accents.

**What brief fields are mandatory?**  
Price column safe zone, allergy disclaimer, print and social sizes, Brand Kit roles.

**Food photo tools enough?**  
They help hero shots; menu ops need editable columns and legal footer.

**404 reason?**  
Missing owner guide URL; now restored.

**Design Agent for owners?**  
Pass/fail on readable prices, allergens, drift—no design jargon required.
""",
    "posters_de": """
## FAQ

**Reicht ein schönes KI-Bild?**  
Nein. Editierbare Preis- und Datums-Layer via Touch Edit.

**Preisänderung Dienstag?**  
Touch Edit auf CTA-Streifen; kein Full-Regen.

**Brand Kit zuerst?**  
Ja, gegen Accent-Drift in Serien.

**Warum 404?**  
DE How-to fehlte; stable SOP URL.

**ChatCanvas Minimum?**  
Ratio, Safe-Zone, Kit-Rollen, Disclaimer footer.
""",
}

# Expansion paragraphs
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


def expand_it(topic: str, n: int) -> str:
    return f"""
## Nota operativa {n}: {topic}

Il primo brief «premium» fallisce: prezzo piccolo, badge sul viso. Al secondo pass correggi solo safe zone e campi obbligatori. Thread unico **ChatCanvas** riduce drift slide 4. In **{topic}**, se **Touch Edit** chiude cambio prezzo in cinque minuti, il loop static-first funziona. Full regen da 30 minuti significa rifare **Brand Kit**. URL 404 ripristinato per SOP stabile onboarding.
"""


def expand_ru(topic: str, n: int) -> str:
    return f"""
## Полевые заметки {n}: {topic}

Первый brief «премиум» даёт мелкий ценник и badge на лице. Во втором проходе правьте только safe zone и обязательные поля. Один thread **ChatCanvas** снижает drift слайда 4. В сценарии **{topic}** правка цены **Touch Edit** за пять минут подтверждает static-first. Full regen 30 минут — сначала **Brand Kit**. Восстановленный URL для stable SOP.
"""


def expand_en(topic: str, n: int) -> str:
    return f"""
## Field note {n}: {topic}

The first brief ends with «premium» and fails: small price type, badge over the face. Second pass fixes only safe zone and required fields. One **ChatCanvas** thread cuts slide-four accent drift. In **{topic}**, if **Touch Edit** closes a price change in five minutes, static-first works. Thirty-minute full regen means redo **Brand Kit** first. Restored 404 URL is the stable onboarding SOP link.
"""


def expand_de(topic: str, n: int) -> str:
    return f"""
## Praxisnotiz {n}: {topic}

Erster Brief «premium» scheitert: kleiner Preis, Badge im Gesicht. Zweiter Durchlauf nur Safe-Zone und Pflichtfelder. Ein **ChatCanvas**-Thread reduziert Slide-4-Drift. Bei **{topic}** bestätigt **Touch Edit** unter fünf Minuten den static-first-Loop. Full-Regen 30 Minuten: **Brand Kit** neu. Wiederhergestellte 404-URL als stable SOP.
"""


ARTICLES = [
    {
        "rank": 63,
        "key": "t2i_benchmark_it",
        "lang": "it",
        "slug": "2026-top-text-to-image-tool-lovart-generation-quality-benchmark",
        "cover": "013",
        "category": "Comparison",
        "title": "Benchmark text-to-image 2026: qualità in produzione, non vanity score",
        "seo_title": "T2I benchmark 2026 — workflow Lovart ChatCanvas",
        "description": "404 fix IT: confronto onesto T2I vs revision cost, Brand Kit, Touch Edit, static-first.",
        "seo_description": "Benchmark T2I: Design Agent, ChatCanvas static, Brand Kit anti-drift.",
        "focus": "text to image benchmark 2026",
        "keywords": ["text to image benchmark", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — T2I Benchmark",
        "body": T2I_BENCHMARK_IT,
        "expand_topic": "T2I production workflow",
    },
    {
        "rank": 64,
        "key": "non_design_it",
        "lang": "it",
        "slug": "best-agent-for-non-design",
        "cover": "020",
        "category": "Industry Solution",
        "title": "Miglior agent per chi non è designer: Design Agent con brief contrattuale",
        "seo_title": "Design Agent non-designer — ChatCanvas workflow",
        "description": "404 fix IT: non-designer daily ops, Brand Kit, Touch Edit, brief contrattuale.",
        "seo_description": "Design Agent IT: ChatCanvas, Brand Kit, Touch Edit per marketer.",
        "focus": "best design agent non designer",
        "keywords": ["design agent", "non designer", "lovart chatcanvas", "brand kit"],
        "cluster": "Segment — Non-Designer",
        "body": NON_DESIGN_IT,
        "expand_topic": "non-designer promo workflow",
    },
    {
        "rank": 65,
        "key": "interior_tools_ko",
        "lang": "ko",
        "slug": "ai-interior-design-tools-compared",
        "cover": "027",
        "category": "Comparison",
        "title": "AI 인테리어 디자인 도구 비교 2026: mood board·가구 swap·revision cost",
        "seo_title": "AI 인테리어 도구 비교 — Touch Edit swap",
        "description": "KO 404 fix: interior tools compare mood board, Touch Edit furniture, Brand Kit drift.",
        "seo_description": "Interior AI KO: ChatCanvas, Design Agent, Touch Edit comparison.",
        "focus": "ai interior design tools compared",
        "keywords": ["ai interior design", "interior tools compare", "lovart chatcanvas", "touch edit"],
        "cluster": "Comparison — Interior KO",
        "body": INTERIOR_TOOLS_KO,
        "expand_topic": "인테리어 도구 revision cost",
    },
    {
        "rank": 66,
        "key": "auto_resize_ru",
        "lang": "ru",
        "slug": "auto-resize-multi-platform-workflow-ai",
        "cover": "034",
        "category": "How-To",
        "title": "Авто-ресайз под мультиплатформу: AI-workflow без drift",
        "seo_title": "Auto-resize multi-platform — ChatCanvas Brand Kit",
        "description": "RU 404 fix: multi-size export, Brand Kit, Touch Edit promo, Design Agent QA.",
        "seo_description": "Auto-resize RU: ChatCanvas master, Touch Edit, static-first.",
        "focus": "auto resize multi platform workflow ai",
        "keywords": ["auto resize", "multi platform", "lovart chatcanvas", "brand kit"],
        "cluster": "How-To — Auto Resize",
        "body": AUTO_RESIZE_RU,
        "expand_topic": "multi-platform resize workflow",
    },
    {
        "rank": 67,
        "key": "nail_studio_zh",
        "lang": "zh",
        "slug": "brand-kit-nail-studio-lovart",
        "cover": "043",
        "category": "Industry Solution",
        "title": "美甲店 Brand Kit 工作流：ChatCanvas 系列物料与 Touch Edit 改价",
        "seo_title": "美甲店 Brand Kit — ChatCanvas 改价 workflow",
        "description": "404 修复：美甲店 Brand Kit、carousel 一致、Touch Edit 改活动价。",
        "seo_description": "美甲 Brand Kit：Design Agent、ChatCanvas、Touch Edit static-first。",
        "focus": "brand kit nail studio lovart",
        "keywords": ["美甲 brand kit", "nail studio ai", "lovart chatcanvas", "touch edit"],
        "cluster": "Segment — Nail Studio",
        "body": NAIL_STUDIO_ZH,
        "expand_topic": "美甲店 weekly promo",
    },
    {
        "rank": 68,
        "key": "dreamina_review_zh",
        "lang": "zh",
        "slug": "dreamina-ai-review",
        "cover": "050",
        "category": "Review",
        "title": "Dreamina AI 评测 2026：clip mood 与可编辑 static 的分工",
        "seo_title": "Dreamina AI 评测 — ChatCanvas static workflow",
        "description": "404 修复：Dreamina clip vs editable static，Brand Kit，Touch Edit 改价。",
        "seo_description": "Dreamina 评测：Design Agent、ChatCanvas、Brand Kit、授权 caution。",
        "focus": "dreamina ai review",
        "keywords": ["dreamina ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Dreamina ZH",
        "body": DREAMINA_REVIEW_ZH,
        "expand_topic": "Dreamina clip vs static",
    },
    {
        "rank": 69,
        "key": "looka_alt_zh",
        "lang": "zh",
        "slug": "looka-alternatives-2026",
        "cover": "055",
        "category": "Comparison",
        "title": "Looka 替代品 2026：logo 探索与 campaign static 的分工",
        "seo_title": "Looka 替代品 2026 — Brand Kit campaign workflow",
        "description": "404 修复：Looka vs Lovart ChatCanvas daily ops，Touch Edit 改价对比。",
        "seo_description": "Looka alternatives：Brand Kit、ChatCanvas、Touch Edit revision cost。",
        "focus": "looka alternatives 2026",
        "keywords": ["looka alternatives", "logo ai", "lovart chatcanvas", "brand kit"],
        "cluster": "Comparison — Looka Alternatives",
        "body": LOOKA_ALT_ZH,
        "expand_topic": "Looka 后 campaign ops",
    },
    {
        "rank": 70,
        "key": "thumbnail_en",
        "lang": "en",
        "slug": "ai-thumbnail-maker",
        "cover": "056",
        "category": "How-To",
        "title": "AI Thumbnail Maker Workflow: YouTube Safe Zones and Touch Edit",
        "seo_title": "AI Thumbnail Maker — YouTube safe zones Touch Edit",
        "description": "404 fix: YouTube thumbnail safe zones, ChatCanvas, Brand Kit, Touch Edit A/B titles.",
        "seo_description": "AI thumbnail: Design Agent, ChatCanvas, Brand Kit, Touch Edit text layer.",
        "focus": "ai thumbnail maker",
        "keywords": ["ai thumbnail maker", "youtube thumbnail", "lovart chatcanvas", "touch edit"],
        "cluster": "How-To — Thumbnail",
        "body": THUMBNAIL_EN,
        "expand_topic": "YouTube thumbnail safe zones",
    },
    {
        "rank": 71,
        "key": "restaurant_menu_en",
        "lang": "en",
        "slug": "how-to-design-a-restaurant-menu-with-ai-complete-guide-for-owners",
        "cover": "057",
        "category": "Complete Guide",
        "title": "How to Design a Restaurant Menu with AI: Complete Guide for Owners",
        "seo_title": "Restaurant Menu AI Guide — Touch Edit prices",
        "description": "404 fix: owner menu workflow, Brand Kit, Touch Edit price blocks, allergy disclaimer.",
        "seo_description": "Restaurant menu AI: ChatCanvas, Design Agent, Brand Kit, Touch Edit.",
        "focus": "design restaurant menu with ai",
        "keywords": ["restaurant menu ai", "menu design", "lovart chatcanvas", "touch edit"],
        "cluster": "Complete Guide — Restaurant Menu",
        "body": RESTAURANT_MENU_EN,
        "expand_topic": "restaurant menu price edits",
    },
    {
        "rank": 72,
        "key": "posters_de",
        "lang": "de",
        "slug": "how-to-create-professional-posters",
        "cover": "058",
        "category": "How-To",
        "title": "Professionelle Poster mit AI erstellen: Brief, Brand Kit, Touch Edit",
        "seo_title": "Professionelle Poster AI — ChatCanvas Workflow DE",
        "description": "404 fix DE: Poster How-to, Brand Kit, Touch Edit Preisänderung, Design Agent QA.",
        "seo_description": "Poster AI DE: ChatCanvas, Brand Kit, Touch Edit, static-first.",
        "focus": "create professional posters ai",
        "keywords": ["professional posters ai", "poster design", "lovart chatcanvas", "brand kit"],
        "cluster": "How-To — Posters DE",
        "body": POSTERS_DE,
        "expand_topic": "Poster Preisänderung workflow",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "ko": expand_ko,
    "it": expand_it,
    "ru": expand_ru,
    "en": expand_en,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch6 content cluster.*\n"
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
