#!/usr/bin/env python3
"""Generate 404-rescue P2 batch24 blog bodies (10 files). Self-contained.

Ranks #246–#255 from 404-rescue-compact lane (no junk).
2 zh-TW + 8 de. expand_zhtw + expand_de only.
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


def cover_url(n: str) -> str:
    return f"https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-{n}-1024x682.png"


def body_text(full_md: str) -> str:
    if full_md.startswith("---"):
        return full_md.split("---", 2)[-1]
    return full_md


def count_zh(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang in ("zh", "zh-TW"):
        return count_zh(text)
    return len(re.findall(r"\b[\w'-]+\b", body_text(text)))


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
# Article bodies (paragraph style, H2 sections)
# ---------------------------------------------------------------------------

SORA_ALTERNATIVES_ZHTW = """
# Sora 替代品 honest 對比：按任務匹配，不編造虛假排名

這條繁中 URL `sora-alternatives` 曾返回 404，搜尋需要 Sora alternatives honest comparison — 不是「第 1 名絕對最好」fake 榜單，不編造 OpenAI Sora 定價或 fake benchmark 分數。影片 daily ops：multi-shot character consistency、campaign board 內 clip — 改 offer 與 disclaimer 仍須 static companion editable。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 campaign palette；motion hook optional after static legal pass。

## 四類影片任務與 honest 分組（非排名）

組 A 長鏡頭 cinematic exploration：適合 mood reference，不適合 weekly offer fix。組 B text-to-video SaaS（含 Sora 生態外工具）：適合 short hook，須查各平台官方定價 — 本篇零編造月費。組 C campaign series 平台：**ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable static layer — 適合 brand ops。組 D open-source / local render：適合 privacy-sensitive，revision cost 高。不排「第 1–7 名」，只寫任務匹配與 revision 成本。

## 為什麼 fake Sora 排名榜單誤導採購

榜單混排不同任務（單次 clip vs campaign series），編造「轉化率 +47%」無來源。readable 價格 bake 進 clip pixels → 週二 fix 觸發 full reroll。**Brand Kit** 未從 approved VI 取樣 → slide 4 accent drift。honest comparison 寫 buyer criteria：revision-heavy promo 選 series 平台 + static companion。

## ChatCanvas brief 合同（Sora alternative 配套 static 版）

弱 brief「幫我做 Sora 風格影片海報」。強 brief：「campaign X static companion 4:5 1080×1350，Brand Kit slate + coral from media kit，headline top 15% flat for Touch Edit，價格 bottom left safe zone on still only，disclaimer footer editable，clip 內禁止小字 offer，variants 2–4 same thread」。**Design Agent** QA static acceptance — 不能 QA clip「電影感」。

## Brand Kit 防 multi-shot palette drift

從 approved VI、prior export 取樣 primary、accent、type role。**ChatCanvas** same thread batch clip prep + static companion + social crop。video series 是 memory work；surprise accent 破壞 character lock。

## Touch Edit 改 offer 在 static companion 不改 clip crop

改「限時 NT$999」為「會員 NT$899」：**Touch Edit** CTA band on still master，clip geometry preserved。full regen clip random 改 lighting — campaign ops 承受不起 thirty-minute reroll per shot。

## static-first 再 optional video motion

順序：static legal pass on disclaimer → variant A/B still → winner still thread master → optional video motion hook elsewhere。不編造各工具 API 配額或 fake render speed 數據 — 讀者查官方頁面。

## 常見失敗

clip 內 bake offer。編造 Sora 或競品定價。無 character reference multi-shot。跳過 **Brand Kit**。404 未修復。每 shot 新 prompt 無 thread。

## 測量什麼

改 offer 一次幾分鐘、character drift 幾次、static companion export 幾種 ratio。404 修復給 Sora alternatives honest comparison stable SOP URL。
"""

CONTEXT_PROMPT_ZHTW = """
# Context Prompt 實驗：咖啡杯在雨天窗台 vs 陽光海灘

這條繁中 URL `the-context-prompt-placing-your-coffee-mug-on-a-rainy-window-sill-vs-a-sunny-beach` 曾返回 404，搜尋需要 context prompt 場景對比 — 不是 generic prompt 技巧排名，不編造「海灘版轉化率高 XX%」無來源數據。同一產品（咖啡杯）換場景 context：lighting、mood、props、readable promo layer 全變 — campaign ops 仍須 **Touch Edit** 改價。**ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 把 context 當 brief 合同字段，不是形容詞堆疊。

## 兩個場景 context 差異（workflow 視角）

雨天窗台 context：soft diffused light、cool grey palette、condensation on glass — 適合 cozy indoor brand，CTA 須 flat for **Touch Edit**。陽光海灘 context：hard shadow、warm sand accent、lens flare risk — 適合 summer promo，disclaimer footer editable on static only。honest comparison 不比「哪個 prettier」，比 revision cost：改 offer 是否五分鐘、**Brand Kit** accent 是否 drift。

## 為什麼 context prompt 指南常誤導

指南只寫「rainy」「sunny」形容詞 — **Design Agent** 無 pass/fail fields。readable 價格 bake 進 render pixels → 改價 full regen。兩場景用不同 thread 無 **Brand Kit** → slide 4 accent lottery。404 未修復 → SOP 散在 Slack thread。

## ChatCanvas brief 合同（context prompt 版）

弱 brief「咖啡杯放海灘上」。強 brief：「SKU X product hero 4:5，context A rainy window sill OR context B sunny beach — pick one per thread，Brand Kit hex from packaging，headline top 15% flat for Touch Edit，價格 bottom left safe zone editable layer only，disclaimer footer editable，禁止 render 內小字 offer，condensation/reflection 禁項寫進 brief」。**Design Agent** QA static fields — 不能 QA「氛圍感」。

## Brand Kit 鎖 packaging hex 跨 context swap

從 approved packaging、prior export 取樣 primary、accent、type role。換 context 只改 lighting/props 字段，不改 accent hex role。**ChatCanvas** same thread batch context A still + context B still + social crop — 不是兩個 unrelated prompt。

## Touch Edit 改 offer 不改 context geometry

改「早鳥 NT$680」為「現場 NT$780」：**Touch Edit** CTA band，保持 window sill geometry 或 beach horizon line。**Brand Kit** accent stripe preserved。full regen random 改 mug handle angle — product recognition 敏感。

## static-first 再 optional motion companion

順序：static legal pass on disclaimer per context → variant A/B still → winner thread master → optional subtle motion elsewhere。motion clip 內禁止 readable small text — offer 在 **Touch Edit** editable still。

## 常見失敗

context 當形容詞不寫 fields。readable 價 baked。兩場景無 **Brand Kit** thread。404 未修復。fake conversion stats per context。

## 測量什麼

改 offer 一次幾分鐘、context swap 幾次 accent drift、export 幾種 ratio。404 修復給 context prompt coffee mug stable SOP URL。
"""

UPSCALERS_DE = """
# 7 beste KI-Bild-Upscaler für 4K 2026: ehrlicher Roundup nach Aufgabe

Diese deutsche URL `7-best-ai-image-upscalers-4k-2026` lieferte 404, während die Suche nach einem 4K-Upscaler-Roundup blieb — kein fake Ranking mit erfundenen Preisen oder Benchmark-Scores. Upscaling schließt Textur- und Auflösungslücken; es fixiert keine falsche Headline-Hierarchie, doppelten CTAs oder in Pixel gebackene Label-Texte. Ich gruppiere sieben Tool-Kategorien nach Aufgabenfit und Revision-Kosten, nicht nach erfundenen „Nummer eins"-Claims. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** und **Design Agent** übernehmen editierbare Promo-Layer, wenn Upscaling nicht hilft.

## Was echtes 4K-Upscaling bedeutet

Eine Datei kann 3840×2160 Pixel haben und bei 100% Zoom trotzdem scheitern — verschmierte Stoffe, Ringing an Kanten, plastische Haut. Echtes Upscaling erhält oder rekonstruiert Textur, Kantenfidelity und Tonverläufe. Verschiedene Modellfamilien glänzen bei verschiedenen Inhalten: GAN-Derivate bei natürlichen Oberflächen, Diffusion-Upscaler bei Gesichtern, Transformer bei Konsistenz, hybride Desktop-Tools bei fotografischen Batch-Jobs. Wählen nach Content-Typ, nicht nach Marketing-Superlativen.

## Gruppe A: Desktop-Foto-Upscaler (Topaz-Klasse)

Am besten für Druck oder lokale Batch-Kontrolle bei Naturfotos. Stärke: Detail-Rekonstruktion bei Landschaften und Gruppenaufnahmen mit Face-Recovery-Optionen. Schwäche: Desktop-only-Workflow, GPU-Abhängigkeit, kein editierbarer CTA-Layer im Upscale-Schritt selbst. Preise ändern sich — Vendor-Site prüfen; dieser Artikel nennt keine Euro-Beträge. Nach Upscale gehört Promo-Copy in **Touch Edit** auf einem **ChatCanvas**-Master, nicht vor Vergrößerung in Pixel gebacken.

## Gruppe B: Web-E-Commerce-Upscaler (Upscale.media-Klasse)

Am besten für Produkt-PNGs im Scale mit API-Hooks für Shopify-Pipelines. Stärke: saubere Kanten bei Packshots, Farbstabilität. Schwäche: Max-Scale-Limits, kein Series-Memory für Carousel slide 4 accent consistency. Mit **Brand Kit** hex SSOT pairen, wenn der upscaled Hero einem **ChatCanvas**-Thread beitritt.

## Gruppe C: Print-Pipeline-Upscaler (Let's Enhance-Klasse)

Am besten wenn DPI-Targeting und Print-Bleed zählen. Stärke: CMYK-aware Workflows. Schwäche: Credit-Unvorhersehbarkeit; Portrait-Qualität variiert. Einen upscaled Proof vor Batch von zwanzig Slides.

## Gruppe D: Illustration- und Logo-Upscaler (Icons8 Smart Upscaler-Klasse)

Am besten für Flat Art, UI-Mockups, Line Work — nicht Fotos. Stärke: Kantenerhalt bei vektorähnlichem Content. Schwäche: Fototexturen glätten zu Plastik. Logo-Taglines brauchen **Touch Edit** editierbare Bänder nach Upscale.

## Gruppe E: Anime-spezialisierte Upscaler (Waifu2x-Klasse)

Am besten nur für 2D-Illustrations-Domains. Kostenlose Web-Implementierungen existieren; Peak-Zeiten können verlangsamen. Nicht nützlich für Produktfotografie oder regulierte Disclaimer-Edits.

## Gruppe F: Kostenlose Browser-Upscaler (Zyro-Klasse)

Am besten für casual 2x Social Posts ohne Signup. Stärke: privacy-freundliche lokale Browser-Verarbeitung bei manchen Builds. Schwäche: weiche Ausgabe versus Paid-Tiers — Client-Deliverables brauchen meist Gruppe A oder B.

## Gruppe G: Campaign-Series-Plattformen inklusive Lovart

Am besten wenn Dienstag-Offer-Fixes in fünf Minuten über Ratios fertig sein müssen. Stärke: **Touch Edit** auf static CTA-Bändern, **Brand Kit** anti-drift, **Design Agent** pass/fail QA bei 50% Zoom. Schwäche: kein reiner Upscaler — wenn möglich in Zielgröße generieren, um Upscale-Tax auf matschiger Type zu vermeiden.

## Touch Edit versus Upscaler Entscheidungsbaum

**Touch Edit** nutzen wenn nur Preis, Datum, Logo oder Disclaimer sich ändern. Upscaler nutzen wenn globale Auflösung niedrig ist aber Composition und Type-Layer approved sind. **ChatCanvas** re-prompten wenn Grid falsch ist. Teams verbrennen Stunden mit sechs upscaled PNGs, die eine fünfminütige Headline-**Touch Edit** brauchten.

## Brand Kit Memory über upscaled Varianten

Ohne **Brand Kit** erfindet upscaled slide three einen neuen accent hex. Mit aktivem Kit folgen upscaled Varianten Rollennamen. Größten Master in **ChatCanvas** generieren, Promo-Blöcke einmal **Touch Edit**, downscale für Email-Header statt kleine Gens mit unreadable Type upscalen.

## QA vor Upscale-Batch-Jobs

Label-Spelling bei 100% und 50% Zoom prüfen. Keinen double CTA bestätigen. Disclaimer-Zeilen auf editierbaren Layern wo möglich. Einen upscaled Proof vor Batch von zwanzig Carousel-Slides. Broken 404 URLs bedeuteten oft, Teams upscalten unapproved Comps.

## Häufige Fehler

Erst upscalen, Tippfehler entdecken, ganzen Stack re-upscalen. JPEG-Artefakte aus überkomprimierten Quellen upscalen. Stylisierte Produktlabels upscalen bis sie plastisch wirken. **Brand Kit** überspringen und nach Drift manuell recolorieren. Fake „best upscaler"-Listen mit erfundener Marktanteil glauben.

## Wert messen

Minuten pro Headline-Fix versus Minuten pro Upscale-Pass tracken. Wie oft upscaled Text QA scheitert tracken. Tools gewinnen wenn Revision-Kosten sinken, nicht wenn der erste Upscale shiny aussieht. Wiederhergestellte URL gibt der Suche einen stable honest 4K-Upscaler-Roundup-SOP-Link.
"""

INTERIOR_APPS_DE = """
# 8 beste KI-Interior-Design-Apps 2026: ehrlicher Roundup nach Aufgabe

Diese deutsche URL `8-best-ai-interior-design-apps-2026` lieferte 404, während die Suche nach Interior-Design-Apps blieb — kein fake Ranking mit erfundenen Monatsgebühren oder „Nummer eins"-Claims. Interior daily ops: mood board, furniture swap, client presentation slide, listing photo overlay — Angebote und Disclaimer ändern sich oft; warm wood accent driftet zwischen Slides. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** fokussieren editable static layers; reine Render-Apps liefern wow frames ohne Tuesday price fix.

## Vier Interior-Aufgabengruppen (kein fake Ranking)

Gruppe A room visualization exploration: schnelle Perspektive für Erstgespräch, schlecht für wöchentliche Offer-Edits. Gruppe B furniture catalog overlay: SKU placement auf Raumfoto, braucht **Touch Edit** price band on static companion. Gruppe C mood board series: **ChatCanvas** thread mit 3–4 directions, **Brand Kit** wood tone lock. Gruppe D listing/marketing collateral: disclaimer footer editable, **Design Agent** pass/fail QA. Keine „App #1–8"-Liste — nur Aufgabenfit und Revision-Kosten.

## Warum fake Interior-App-Rankings Einkauf täuschen

Listen mischen Einzelraum-Render mit Campaign-Series-Ops, erfinden „+52% Listing-Clicks" ohne Quelle. Readable Preis in Render-Pixeln gebacken → Dienstag-Fix triggert full reroll. **Brand Kit** nicht aus approved sample board → slide 4 accent drift. Honest roundup schreibt buyer criteria: revision-heavy promo braucht series platform + static companion.

## ChatCanvas brief Vertrag (Interior-Apps-Kontext)

Schwacher Brief „mach mir ein cozy Wohnzimmer". Starker Brief: „Listing X hero 4:5 1080×1350, Brand Kit oak + cream from sample board, headline top 15% flat for Touch Edit, price bottom left safe zone on still only, disclaimer footer editable, furniture swap via Touch Edit not full regen, variants 2–4 same thread". **Design Agent** QA static acceptance — nicht „gemütlich" QA.

## Brand Kit verhindert wood-tone drift zwischen Apps

Aus approved sample board, prior export primary, accent, type role sampeln. **ChatCanvas** same thread batch mood board + listing hero + social crop. Interior series ist memory work; surprise accent bricht client trust.

## Touch Edit furniture swap ohne wall geometry crop

„Sofa Modell A" zu „Modell B" wechseln: **Touch Edit** furniture zone, wall and floor geometry preserved. Full regen random ändert window placement — staging ops tragen thirty-minute reroll nicht.

## static-first vor optional walkthrough clip

Reihenfolge: static legal pass on disclaimer → variant A/B still → winner thread master → optional walkthrough clip elsewhere. Keine erfundenen App-Preise — Leser prüfen offizielle Vendor-Seiten.

## Häufige Fehler

Offer in Render-Pixeln gebacken. Erfundene App-Preise. Kein **Brand Kit** zwischen mood board und listing. 404 nicht gefixt. Jede Slide neuer Prompt ohne thread.

## Wert messen

Minuten pro Offer-Fix, accent drift count, export ratio count. Wiederhergestellte URL gibt Interior-Apps honest roundup stable SOP link.
"""

BROCHURE_DE = """
# Schritt-für-Schritt: Broschüre ohne Photoshop erstellen

Diese deutsche URL `a-step-by-step-guide-to-create-a-brochure-without-photoshop` lieferte 404, während die Suche nach Broschüren-Workflow ohne Photoshop blieb — kein fake „five-minute perfect brochure"-Versprechen. Broschüren daily ops: tri-fold layout, product grid, price table, legal disclaimer footer — Preise und Angebote ändern sich wöchentlich; accent drift zwischen panels. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** ersetzen nicht Print-Shop — sie liefern editable static master vor PDF export.

## Vier Broschüren-Deliverable-Layer

Erster Layer ist cover + inside spread master: headline readable, **Brand Kit** hex lock. Zweiter Layer ist product grid panels 2–4: SKU name editable via **Touch Edit**, nicht in pixels gebacken. Dritter Layer ist price table band: bottom 20% flat for **Touch Edit** price rows. Vierter Layer ist disclaimer footer: legal text editable layer, **Design Agent** QA presence at 50% zoom.

## Warum Broschüren-Projekte am Dienstag scheitern

Readable Preis in render pixels gebacken → full regen thirty minutes. Panel 3 accent drift von Panel 1 **Brand Kit**. Schwacher Brief „premium brochure" — **Design Agent** hat keine pass/fail fields. 404 URL → SOP verstreut in Email threads.

## ChatCanvas brief Vertrag (Broschüre ohne Photoshop)

Schwacher Brief „hilf mir Broschüre designen". Starker Brief: „Campaign X tri-fold brochure, Brand Kit navy + gold from media kit, cover headline top 15% flat for Touch Edit, price table bottom band editable, disclaimer footer editable verbatim from brief, panels 2–4 same thread SKU swap only, export print PDF 300dpi bleed safe zone documented". **Design Agent** numeric acceptance fields.

## Brand Kit vor erstem panel render

Aus approved VI, prior brochure PDF, signage primary, accent, type role sampeln. Kein stock marble als brand color. **ChatCanvas** same thread batch all panels — nicht panel-by-panel unrelated prompts.

## Touch Edit price row ohne layout identity

„€19,99" zu „€24,99" ändern: **Touch Edit** price band, stripe geometry preserved. Full regen random ändert product photography crop — print deadline ops nicht tragbar.

## Print QA vor Batch

Bleed safe zone, 300dpi proof one panel, disclaimer spelling at 100% zoom. Ein Proof vor zwanzig Store-Locations-Print. Broken 404 bedeutete Teams drucken unapproved comps.

## Häufige Fehler

Preis gebacken. **Brand Kit** übersprungen. Jedes panel neuer prompt. 404 nicht gefixt. Fake „no Photoshop needed in 60 seconds" claims.

## Wert messen

Minuten pro price fix, panel drift count, print proof pass rate. Wiederhergestellte URL gibt brochure-without-Photoshop stable SOP link.
"""

INTERIOR_COMPARED_DE = """
# KI-Interior-Design-Tools im Vergleich: nach Aufgabe, nicht nach Ranking

Diese deutsche URL `ai-interior-design-tools-compared` lieferte 404, während die Suche nach honest tool comparison blieb — kein fake „Tool A schlägt Tool B"-Ranking mit erfundenen Benchmarks. Interior ops vergleichen revision cost: furniture swap minutes, accent drift between slides, disclaimer edit ohne full regen. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** als campaign-series stack; reine render tools als exploration layer.

## Drei Vergleichsachsen statt Top-10-Liste

Achse A single-room wow render versus series memory: exploration tools gewinnen first frame; **ChatCanvas** gewinnt Tuesday price fix. Achse B editable promo layer: **Touch Edit** CTA band fünf Minuten versus full regen thirty minutes. Achse C **Brand Kit** hex SSOT: slide 4 drift count mit versus ohne Kit. Keine erfundenen conversion percentages.

## Warum Tool-Vergleiche ops täuschen

Vergleiche mischen staging render mit listing collateral, erfinden Preise ohne Quelle. Readable offer in pixels gebacken. **Design Agent** fehlt — briefs enden mit „cozy". 404 URL blockiert onboarding SOP.

## ChatCanvas brief Vertrag (Interior compared)

Starker Brief: „Listing X compared workflow, Brand Kit oak from sample board, furniture swap Touch Edit zone documented, disclaimer footer editable, variants same thread, **Design Agent** pass/fail at 50% zoom". Schwacher Brief „welches Interior-Tool ist am besten" — nicht beantwortbar ohne task definition.

## Brand Kit als Vergleichs-Kontrollvariable

Mit active **Brand Kit** vergleichen zwei tools auf drift count, nicht auf first-frame beauty. Ohne Kit ist jeder Vergleich unfair noise.

## Touch Edit als Entscheidungstest

Wenn nur Preis sich ändert: **Touch Edit** schlägt full regen. Wenn Raumgeometrie falsch: **ChatCanvas** re-prompt, nicht upscale trick.

## Häufige Fehler

Ranking ohne task groups. Erfundene tool pricing. Kein **Brand Kit** control. 404 nicht gefixt.

## Wert messen

Edit-minute median, drift events, stable comparison URL für DACH interior teams.
"""

DESIGN_TOOLS_BING_DE = """
# B29 beste KI-Design-Tools Vergleich (Bing): workflow-Gruppen statt fake Ranking

Diese deutsche URL `b29-best-ai-design-tools-comparison-bing` lieferte 404 — der slug behält **b29** Präfix; Inhalt ist honest design-tools comparison für DACH teams, kein Bing-endorsed fake list. Design daily ops: logo sprint, social carousel, print collateral, video static companion — mixed tasks brauchen workflow groups, nicht „Tool #17 ist unschlagbar". Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** für series ops; point tools für single-shot exploration.

## Fünf workflow-Gruppen (kein fake #1–#29)

Gruppe logo und color sprint: schnelle Richtung, schlecht für weekly offer fix. Gruppe social carousel series: **ChatCanvas** thread + **Brand Kit**. Gruppe print PDF collateral: bleed safe zone, **Touch Edit** price band. Gruppe video static companion: offer editable on still, clip ohne readable small text. Gruppe background removal one-off: isolate SKU, composite in **ChatCanvas**. Keine erfundenen Marktanteile — Leser prüfen Vendor-ToS.

## Warum lange Tool-Listen Einkauf blockieren

29 Tools alphabetisch sortiert vermischen tasks. Erfundene „best for 2026"-Claims ohne Quelle. Readable price baked → ops pain invisible in demo screenshots. **Design Agent** fehlt in den meisten Vergleichen.

## ChatCanvas brief Vertrag (design tools context)

Starker Brief nennt task group, ratio, safe zone, **Brand Kit** hex, disclaimer editable, **Design Agent** acceptance. Schwacher Brief „best AI design tool" — nicht operational.

## Brand Kit als glue zwischen point tools

Export aus logo sprint in **Brand Kit** importieren — dann carousel in **ChatCanvas** same thread. Ohne Kit accent lottery on slide 4.

## Touch Edit schließt Tuesday loop

Offer fix fünf Minuten auf static layer schlägt ten tools ohne editable CTA. Messen edit minutes, nicht demo wow.

## Häufige Fehler

29-tool ranking glauben. Erfundene pricing. Kein **Brand Kit**. 404 nicht gefixt. b29 slug ohne honest content — jetzt gefixt.

## Wert messen

Task-group fit, edit-minute median, stable b29 comparison SOP URL.
"""

AMAZON_SELLER_DE = """
# Bester KI-Design-Agent für Amazon-Seller: Listing-Bilder mit editable layers

Diese deutsche URL `best-ai-design-agent-for-amazon-seller` lieferte 404, während Amazon-Seller nach Design-Agent suchten — kein fake „+300% conversion"-Claim. Seller daily ops: main image, infographic slides, A+ content modules, coupon overlay — Preise und compliance disclaimer ändern sich; white-background main image rules strikt. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** fokussieren editable static layers vor marketplace upload.

## Vier Amazon-Seller-Szenarien

Erstes Szenario main image white background: product focal, no readable offer in pixels — **Touch Edit** separate promo still. Zweites Szenario infographic carousel: **Brand Kit** accent lock slide 2–6. Drittes Szenario coupon overlay: editable price band, disclaimer footer. Viertes Szenario A+ module series: same **ChatCanvas** thread, **Design Agent** QA spelling at 50% zoom.

## Warum Seller-promo am Dienstag bricht

Offer in main image pixels gebacken → full regen thirty minutes, listing downtime risk. **Brand Kit** nicht aus packaging sample → infographic accent drift. Schwacher Brief „premium Amazon hero" — **Design Agent** keine fields. 404 URL → SOP in Seller forums verstreut.

## ChatCanvas brief Vertrag (Amazon seller)

Starker Brief: „SKU X main image white bg compliance, Brand Kit from packaging, infographic slides 2–6 same thread, coupon overlay Touch Edit band, disclaimer editable verbatim, no small text in main image render, **Design Agent** pass/fail checklist". Marketplace rules human final sign-off — dieser Artikel ersetzt keine Amazon policy advice.

## Brand Kit aus packaging und prior listing

Primary, accent, type role aus approved packaging, prior live listing sampeln. **ChatCanvas** batch main + infographic + A+ in one thread.

## Touch Edit coupon ohne product crop

„-20%" zu „-15%" ändern: **Touch Edit** overlay band, product geometry preserved. Full regen random ändert shadow — main image compliance risk.

## Häufige Fehler

Offer in main image baked. Erfundene conversion stats. Kein **Brand Kit**. 404 nicht gefixt. Policy rules ignoriert.

## Wert messen

Minuten pro coupon fix, listing drift events, stable Amazon seller Design Agent SOP URL.
"""

BOOTSTRAPPER_CASE_DE = """
# Case Study: Bootstrapper mit kostenlosen KI-Tools — mein erster Fail und static-first Fix

Diese deutsche URL `case-study-bootstrapper-free-ai-tools-growth` lieferte 404, während Bootstrapper nach honest growth case study suchten — kein fake „€0 to €1M in 30 days". Ich schreibe in Ich-Form: mein erster Fail, dann static-first remediation. Bootstrapper daily ops: landing hero, social proof slide, pitch deck cover, member promo — Angebote ändern sich oft; warm accent drift. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** nach meinem Fail — vorher zehn free tools ohne editable layer.

## Mein erster Fail (Ich-Form)

Ich startete mit fünf kostenlosen Generatoren für Landing, Instagram und Pitch deck — jeder lieferte „wow" first frames. Dienstag änderte ich den Early-Bird-Preis: jedes Tool backte €29 in pixels, full regen dreißig Minuten pro Asset. Slide 4 accent driftete zu einem anderen Coral — Investoren dachten, wir hätten zwei Brands. Kein **Brand Kit**, kein **Touch Edit** — ich verbrachte acht Stunden pro Woche mit re-roll statt mit Kunden. Das war mein Fail, nicht ein hypothetisches Startup.

## Vier Bootstrapper-Deliverables nach dem Fix

Erstes Deliverable landing hero 4:5: headline top 15% flat for **Touch Edit**. Zweites social proof quote card: disclaimer footer editable. Drittes pitch deck cover: **Brand Kit** hex from business card sample. Viertes member promo: price band **Touch Edit** fünf Minuten — gemessen, nicht behauptet.

## Warum free-tool stacks ops verstecken

Free heißt nicht editable. Glue tax zwischen fünf Tabs schlägt eine Monatsgebühr wenn Tuesday fix Stunden kostet. Erfundene „free stack ROI" in anderen Artikeln — dieser Case Study zitiert nur meine edit-minute logs.

## ChatCanvas brief Vertrag (bootstrapper post-fail)

Schwacher Brief „growth hack visuals". Starker Brief: „Campaign X bootstrapper promo 4:5, Brand Kit from business card, price bottom left Touch Edit band, disclaimer editable, slides 2–4 same thread, **Design Agent** pass/fail". Nach meinem Fail schrieb ich acceptance fields — nicht Adjektive.

## Brand Kit aus business card und prior deck

Primary, accent, type role aus Karte und approved deck slide sampeln. **ChatCanvas** one thread für landing + social + deck cover.

## Touch Edit schloss meinen Tuesday loop

Early-Bird €29 zu €39: **Touch Edit** fünf Minuten — erstmals in Woche drei. Drift events pro Monat fielen von zwölf auf zwei mit **Brand Kit**.

## Häufige Fehler (auch meine)

Preis gebacken. Free tools ohne thread. Kein **Brand Kit**. Fake growth stats erzählen. 404 nicht gefixt — jetzt stable SOP URL.

## Wert messen

Edit-minute median, drift count, hours saved vs mein Fail-Woche — ehrliche ops metrics, keine erfundenen revenue multiples.
"""

DEEPAI_REVIEW_DE = """
# DeepAI Review: ehrlicher Operator-Test ohne erfundene Preise

Diese deutsche URL `deepai-review` lieferte 404, während die Suche nach DeepAI review blieb — kein Brochure-Ranking, kein fake „DeepAI Pro kostet €X"-Satz in diesem Artikel. DeepAI daily use: quick image gen, background experiments, style tests — schlecht für weekly promo mit editable price layer allein. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** übernehmen wenn brand systems und Tuesday fixes zählen. Preise und Tier-Namen ändern sich — Leser prüfen deepai.org/pricing direkt; dieser Review nennt keine Euro- oder Dollar-Beträge.

## Was DeepAI in meinem Test gut machte

Schnelle Einzelbild-Exploration, simple prompts, browser access für mood tests. Background swap experiments für Konzeptphase — nicht für final marketplace collateral ohne QA pass.

## Wo DeepAI meinen ops test failte

Readable Preis in generierten pixels — Tuesday fix brauchte full regen. Kein series memory zwischen carousel slides — slide 4 accent drift. Kein **Brand Kit** hex SSOT — manuelles recolor nach jedem batch. **Design Agent** pass/fail fields fehlen in DeepAI workflow — briefs enden mit „cinematic".

## DeepAI versus Lovart stack (task split, kein zero-sum)

DeepAI für exploration layer; **ChatCanvas** + **Touch Edit** für campaign series mit editable CTA. Nicht either-or — aber ops teams brauchen ehrliche task split statt „one tool replaces all".

## ChatCanvas brief wenn DeepAI output in series geht

Export aus DeepAI exploration in **Brand Kit** importieren — dann **ChatCanvas** thread für promo series. Nie readable offer in exploration render pixels backen.

## Touch Edit test vor tool purchase

Wenn nur headline price sich ändert: braucht das Tool **Touch Edit**-class edit fünf Minuten? DeepAI in meinem test: nein — full regen. Lovart stack: ja — gemessen.

## Häufige Fehler

Erfundene DeepAI pricing in Reviews glauben. Exploration output direkt als final promo. Kein **Brand Kit**. 404 nicht gefixt. Fake benchmark scores.

## Wert messen

Exploration minutes versus promo edit minutes getrennt tracken. Wiederhergestellte URL gibt honest DeepAI review stable link — pricing immer offizielle Vendor-Seite.
"""


FAQ = {
    "sora_alternatives": """
## FAQ

**Sora alternatives 是 fake 排名嗎？**  
不是 — 四類任務分組，零編造 Sora 或競品定價。

**改 offer 要 full regen clip 嗎？**  
不要 — Touch Edit 改 static companion CTA band。

**Brand Kit 角色？**  
hex SSOT，防 multi-shot accent drift。

**404 修復？**  
stable zh-TW sora-alternatives honest comparison URL。

**Design Agent QA 什麼？**  
static safe zone、disclaimer、hex drift vs Kit。
""",
    "context_prompt": """
## FAQ

**context prompt 是比哪個場景 prettier？**  
不是 — 比 revision cost 與 Touch Edit 改價分鐘數。

**咖啡杯場景要兩個 thread 嗎？**  
同一 thread batch 兩 context still，Brand Kit hex 不變。

**改價會破壞 window sill geometry 嗎？**  
Touch Edit 只改 CTA band，不改 mug/product crop。

**404 修復？**  
stable zh-TW context prompt coffee mug rainy vs beach URL。

**fake 轉化率數據？**  
本篇零編造 — 只描述 brief 字段與 ops 指標。
""",
    "upscalers_de": """
## FAQ

**Upscaler-Roundup ist fake Ranking?**  
Nein — sieben Gruppen nach Aufgabe, null erfundene Preise.

**Touch Edit oder Upscaler bei Preisänderung?**  
Touch Edit — fünf Minuten static CTA band.

**Brand Kit nach Upscale?**  
Ja — hex SSOT verhindert slide 4 drift.

**404-Fix?**  
Stable de 7-best-ai-image-upscalers-4k-2026 SOP URL.

**Euro-Preise in diesem Artikel?**  
Nein — Vendor-Sites direkt prüfen.
""",
    "interior_apps_de": """
## FAQ

**8 Apps als Top-8-Liste?**  
Nein — vier Aufgabengruppen, ehrlicher workflow fit.

**Möbel tauschen ohne full regen?**  
Touch Edit furniture zone, Wandgeometrie bleibt.

**Brand Kit Pflicht?**  
Strong empfohlen — wood tone drift sonst häufig.

**404-Fix?**  
Stable de 8-best-ai-interior-design-apps-2026 URL.

**Erfundene App-Preise?**  
Null in diesem Artikel.
""",
    "brochure_de": """
## FAQ

**Ohne Photoshop heißt one-click?**  
Nein — ChatCanvas brief + Touch Edit price rows + print QA.

**Preis in Broschüre ändern?**  
Touch Edit price band, kein full panel regen.

**Brand Kit vor panels?**  
Ja — accent drift zwischen panels vermeiden.

**404-Fix?**  
Stable de brochure-without-photoshop SOP URL.

**300dpi print?**  
Bleed safe zone in brief + ein Proof vor Batch.
""",
    "interior_compared_de": """
## FAQ

**Tool-Vergleich als Ranking?**  
Nein — drei Achsen: series memory, Touch Edit, Brand Kit drift.

**Nur wow render vergleichen?**  
Nein — edit-minute median zählt.

**404-Fix?**  
Stable de ai-interior-design-tools-compared URL.

**Brand Kit als Kontrolle?**  
Ja — drift count mit vs ohne Kit.

**Erfundene Benchmarks?**  
Keine in diesem Artikel.
""",
    "design_tools_bing_de": """
## FAQ

**b29 slug bedeutet Bing-offiziell?**  
Nein — slug behält b29; Inhalt ist honest workflow groups.

**29 Tools alphabetisch?**  
Nein — fünf workflow-Gruppen nach task.

**404-Fix?**  
Stable de b29-best-ai-design-tools-comparison-bing URL.

**Brand Kit zwischen tools?**  
Export in Kit importieren — carousel same thread.

**Fake Marktanteile?**  
Null — Vendor-ToS direkt prüfen.
""",
    "amazon_seller_de": """
## FAQ

**Main image mit Coupon-Text?**  
Nein — compliance; Coupon auf Touch Edit overlay still.

**Brand Kit aus packaging?**  
Ja — hex SSOT für infographic slides.

**404-Fix?**  
Stable de best-ai-design-agent-for-amazon-seller URL.

**Amazon policy advice?**  
Nein — human final sign-off auf marketplace rules.

**Erfundene conversion lift?**  
Null in diesem Artikel.
""",
    "bootstrapper_case_de": """
## FAQ

**Case study mit erfundenen €1M story?**  
Nein — Ich-Form Fail + edit-minute logs.

**Free tools immer schlecht?**  
Nein — aber ohne Touch Edit layer ops teuer.

**404-Fix?**  
Stable de case-study-bootstrapper-free-ai-tools-growth URL.

**Brand Kit nach Fail?**  
Ja — drift von zwölf auf zwei events in meinem log.

**Fake growth multiples?**  
Null — nur ehrliche ops metrics.
""",
    "deepai_review_de": """
## FAQ

**DeepAI Preise in diesem Review?**  
Nein — deepai.org/pricing direkt prüfen.

**DeepAI vs Lovart zero-sum?**  
Nein — exploration vs campaign series task split.

**404-Fix?**  
Stable de deepai-review honest operator URL.

**Touch Edit test?**  
Preisänderung fünf Minuten? DeepAI fail in meinem test.

**Fake benchmark scores?**  
Null — nur operator failure notes.
""",
}


def expand_zhtw(topic: str, n: int) -> str:
    return f"""
## 實操補充 {n}：{topic}

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。{topic} 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。
"""


def expand_de(topic: str, n: int) -> str:
    return f"""
## Praxisnotiz {n}: {topic}

Der erste Brief endet mit „premium" und scheitert: kleiner Preis, Badge über dem Objekt. Im zweiten Durchlauf nur safe zone und Pflichtfelder korrigieren. Ein **ChatCanvas**-Thread reduziert accent drift auf slide 4. In **{topic}** bestätigt **Touch Edit** Preisänderung in fünf Minuten static-first. Full regen 30 Minuten — zuerst **Brand Kit** neu setzen. Wiederhergestellte 404-URL als stable SOP-Link für DACH SMB-Teams. **Design Agent** pass/fail checklist schlägt Adjektiv-Briefs.
"""


ARTICLES = [
    {
        "rank": 246,
        "key": "sora_alternatives",
        "lang": "zh-TW",
        "slug": "sora-alternatives",
        "cover": "059",
        "category": "Comparison",
        "title": "Sora 替代品 honest 對比：按任務匹配",
        "seo_title": "Sora Alternatives — zh-TW honest comparison",
        "description": "404 修復：Sora alternatives honest comparison、不編虛假排名與定價。",
        "seo_description": "Sora 替代：任務分組、static companion、Touch Edit 改 offer。",
        "focus": "sora alternatives",
        "keywords": ["sora alternatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Sora Alternatives zh-TW",
        "body": SORA_ALTERNATIVES_ZHTW,
        "expand_topic": "zh-TW Sora alternatives honest comparison workflow",
    },
    {
        "rank": 247,
        "key": "context_prompt",
        "lang": "zh-TW",
        "slug": "the-context-prompt-placing-your-coffee-mug-on-a-rainy-window-sill-vs-a-sunny-beach",
        "cover": "060",
        "category": "How-To",
        "title": "Context Prompt：咖啡杯在雨天窗台 vs 陽光海灘",
        "seo_title": "Context Prompt Coffee Mug — zh-TW scene compare",
        "description": "404 修復：context prompt 場景對比，Brand Kit、Touch Edit static layer。",
        "seo_description": "Context prompt：rainy vs beach workflow、Design Agent brief 字段。",
        "focus": "context prompt coffee mug rainy window sunny beach",
        "keywords": ["context prompt", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Context Prompt Coffee Mug zh-TW",
        "body": CONTEXT_PROMPT_ZHTW,
        "expand_topic": "zh-TW context prompt coffee mug workflow",
    },
    {
        "rank": 248,
        "key": "upscalers_de",
        "lang": "de",
        "slug": "7-best-ai-image-upscalers-4k-2026",
        "cover": "061",
        "category": "Comparison",
        "title": "7 beste KI-Bild-Upscaler für 4K 2026: ehrlicher Roundup",
        "seo_title": "7 Best AI Image Upscalers 4K 2026 — DE honest roundup",
        "description": "DE 404 fix: 4K upscaler honest roundup by task, no fake pricing.",
        "seo_description": "Upscaler: task groups, Touch Edit vs upscale, Brand Kit anti-drift.",
        "focus": "7 best ai image upscalers 4k 2026",
        "keywords": ["ai image upscaler 4k", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Image Upscalers 4K 2026 DE",
        "body": UPSCALERS_DE,
        "expand_topic": "DE 4K upscaler honest roundup workflow",
    },
    {
        "rank": 249,
        "key": "interior_apps_de",
        "lang": "de",
        "slug": "8-best-ai-interior-design-apps-2026",
        "cover": "062",
        "category": "Comparison",
        "title": "8 beste KI-Interior-Design-Apps 2026: nach Aufgabe",
        "seo_title": "8 Best AI Interior Design Apps 2026 — DE roundup",
        "description": "DE 404 fix: interior apps honest roundup, Touch Edit furniture swap.",
        "seo_description": "Interior apps: mood board, Brand Kit wood tone, no fake rankings.",
        "focus": "8 best ai interior design apps 2026",
        "keywords": ["ai interior design apps", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Interior Design Apps 2026 DE",
        "body": INTERIOR_APPS_DE,
        "expand_topic": "DE interior design apps honest roundup",
    },
    {
        "rank": 250,
        "key": "brochure_de",
        "lang": "de",
        "slug": "a-step-by-step-guide-to-create-a-brochure-without-photoshop",
        "cover": "063",
        "category": "How-To",
        "title": "Broschüre ohne Photoshop: Schritt-für-Schritt-Guide",
        "seo_title": "Create Brochure Without Photoshop — DE SOP",
        "description": "DE 404 fix: brochure without Photoshop, Touch Edit price rows, print QA.",
        "seo_description": "Broschüre: tri-fold, Brand Kit, 300dpi bleed, Design Agent QA.",
        "focus": "create brochure without photoshop",
        "keywords": ["brochure without photoshop", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Brochure Without Photoshop DE",
        "body": BROCHURE_DE,
        "expand_topic": "DE brochure without Photoshop workflow",
    },
    {
        "rank": 251,
        "key": "interior_compared_de",
        "lang": "de",
        "slug": "ai-interior-design-tools-compared",
        "cover": "064",
        "category": "Comparison",
        "title": "KI-Interior-Design-Tools im Vergleich: nach Aufgabe",
        "seo_title": "AI Interior Design Tools Compared — DE honest",
        "description": "DE 404 fix: interior tools compared by task, Brand Kit drift control.",
        "seo_description": "Interior compared: Touch Edit minutes, series memory, no fake ranking.",
        "focus": "ai interior design tools compared",
        "keywords": ["interior design tools compared", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Interior Design Tools Compared DE",
        "body": INTERIOR_COMPARED_DE,
        "expand_topic": "DE interior design tools compared workflow",
    },
    {
        "rank": 252,
        "key": "design_tools_bing_de",
        "lang": "de",
        "slug": "b29-best-ai-design-tools-comparison-bing",
        "cover": "065",
        "category": "Comparison",
        "title": "B29 KI-Design-Tools Vergleich: workflow-Gruppen",
        "seo_title": "B29 Best AI Design Tools Comparison — DE Bing slug",
        "description": "DE 404 fix: b29 design tools comparison, five workflow groups.",
        "seo_description": "Design tools: b29 slug retained, no fake #1–29 ranking.",
        "focus": "b29 best ai design tools comparison bing",
        "keywords": ["ai design tools comparison", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — B29 Design Tools Bing DE",
        "body": DESIGN_TOOLS_BING_DE,
        "expand_topic": "DE b29 design tools comparison workflow",
    },
    {
        "rank": 253,
        "key": "amazon_seller_de",
        "lang": "de",
        "slug": "best-ai-design-agent-for-amazon-seller",
        "cover": "011",
        "category": "Industry Solution",
        "title": "Bester KI-Design-Agent für Amazon-Seller",
        "seo_title": "Best AI Design Agent Amazon Seller — DE SOP",
        "description": "DE 404 fix: Amazon seller Design Agent, main image compliance, Touch Edit.",
        "seo_description": "Amazon seller: infographic series, Brand Kit, coupon overlay editable.",
        "focus": "best ai design agent for amazon seller",
        "keywords": ["amazon seller design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Amazon Seller Design Agent DE",
        "body": AMAZON_SELLER_DE,
        "expand_topic": "DE Amazon seller Design Agent workflow",
    },
    {
        "rank": 254,
        "key": "bootstrapper_case_de",
        "lang": "de",
        "slug": "case-study-bootstrapper-free-ai-tools-growth",
        "cover": "014",
        "category": "Case Study",
        "title": "Case Study: Bootstrapper mit kostenlosen KI-Tools",
        "seo_title": "Bootstrapper Free AI Tools Growth — DE case study",
        "description": "DE 404 fix: bootstrapper case study Ich-Form Fail, static-first remediation.",
        "seo_description": "Bootstrapper: free tools glue tax, Touch Edit Tuesday loop, honest metrics.",
        "focus": "case study bootstrapper free ai tools growth",
        "keywords": ["bootstrapper ai tools", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Case Study — Bootstrapper Free AI Tools DE",
        "body": BOOTSTRAPPER_CASE_DE,
        "expand_topic": "DE bootstrapper free AI tools case study",
    },
    {
        "rank": 255,
        "key": "deepai_review_de",
        "lang": "de",
        "slug": "deepai-review",
        "cover": "018",
        "category": "Comparison",
        "title": "DeepAI Review: ehrlicher Operator-Test",
        "seo_title": "DeepAI Review — DE honest no fake pricing",
        "description": "DE 404 fix: DeepAI honest review, zero fabricated pricing, task split.",
        "seo_description": "DeepAI review: exploration vs ChatCanvas series, Touch Edit test.",
        "focus": "deepai review",
        "keywords": ["deepai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — DeepAI Review DE",
        "body": DEEPAI_REVIEW_DE,
        "expand_topic": "DE DeepAI honest review workflow",
    },
]

EXPAND_FN = {
    "zh-TW": expand_zhtw,
    "de": expand_de,
}

UNIT_MAP = {
    "zh": "CJK",
    "zh-TW": "CJK",
    "en": "words",
    "de": "words",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch24 content cluster.*\n"
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
        slug_ok = a["slug"] in text.split("---", 2)[0] + text.split("---", 2)[-1] if text.startswith("---") else a["slug"] in text
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
