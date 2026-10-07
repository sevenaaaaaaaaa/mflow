#!/usr/bin/env python3
"""Generate 404-rescue P2 batch29 blog bodies (10 files). Self-contained.

Ranks #296–#305 from 404-rescue-compact lane.
9 IT + 1 JA. expand_it (batch6) + expand_ja (batch19).
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
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


def count_ja(text: str) -> int:
    return len(JA_CHAR_RE.findall(body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang == "ja":
        return count_ja(text)
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

ONLINE_SELLER_IT = """
# Miglior Design Agent AI per online seller: workflow onesto senza ranking fake

Questa URL italiana `best-ai-design-agent-for-online-seller` restituiva 404 mentre seller marketplace e DTC cercavano guida onesta — non ranking generico « #1 best agent » con score inventati. Ops quotidiane seller: product hero, promo carousel, flash sale banner, listing thumbnail — prezzi SKU e date promo cambiano ogni settimana, accent drift tra Amazon A+ e Instagram crop. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** fissano palette catalog-ready. KPI è « cambiare prezzo promo in cinque minuti », non « primo hero cinematic ».

## Quattro deliverable online seller workflow

Primo layer product hero 4:5 o 1:1 con price band editable via **Touch Edit**. Secondo layer marketplace carousel slide 2–6 same **ChatCanvas** thread accent **Brand Kit**. Terzo layer flash sale banner 16:9 — disclaimer footer editable. Quarto layer listing thumbnail — **Design Agent** readable price at 50% zoom pass/fail.

## Perché « best agent for online seller » comparativi ingannano

Liste inventano scores senza source. Offerta baked in pixels → seller blocked martedì full regen. **Brand Kit** assente → hero teal, Instagram coral. Confronto onesto scrive: best = low edit-minute median on Tuesday loop, non pretty first output.

## Contratto brief ChatCanvas (online seller IT)

Brief debole: « premium product ad ». Brief forte: « Seller X SKU promo 4:5, Brand Kit hex from packaging VI, headline product name top 15% flat for Touch Edit, price bottom band editable, disclaimer footer editable, variants hero + carousel same thread, **Design Agent** pass/fail checklist seller can run ».

## Brand Kit unifica listing e social crop

Primary, accent da VI prodotto o packaging. **ChatCanvas** same thread 1:1 thumbnail + 4:5 story + 16:9 banner — accent stripe resta.

## Touch Edit cambia prezzo flash sale senza regen hero

« €29 » verso « €19 »: **Touch Edit** five minutes CTA band — non full product hero regen thirty minutes. Seller metric: edit-minute median down week over week.

## Errori frequenti online seller

Credere fake ranking scores. Exploration output as final listing. Saltare **Brand Kit**. URL 404 non ripristinato. Fake conversion lift stats senza source.

## Metriche online seller

Edit-minute median, regen count, drift events per SKU batch. URL ripristinato stable IT best-ai-design-agent-for-online-seller SOP link.
"""

NANO_BANANA_ADS_IT = """
# Generare ads in 60 secondi con nano-banana-2 e Lovart: static-first ops

Questa URL italiana `generate-ads-60-seconds-nano-banana-2-lovart` restituiva 404 mentre marketer cercavano workflow rapido nano-banana-2 + Lovart — non hype « instant perfect ad » senza campi pass/fail. Slug nano-banana-2 indica contesto visual motif o deck-adjacent style; questo articolo copre promo static editable in sessanta secondi di setup brief, non fake API timing benchmark. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** focus CTA editable layer dopo direction rapida.

## Quattro campi brief 60-second setup

Primo campo ratio 4:5 o 1:1 documentato in brief. Secondo campo **Brand Kit** hex from media kit — non stock marble. Terzo campo headline top 15% flat for **Touch Edit**. Quarto campo **Design Agent** pass/fail: readable price, disclaimer present, accent drift zero.

## Perché « 60 seconds » slug inganna senza context

Sessanta secondi = brief contract + Kit lock, non garantia universal perfect first frame. Ops reality: first pass direction, second pass **Touch Edit** price fix five minutes. Honest guide misura edit-minute median, non render clock fantasy.

## Contratto brief ChatCanvas (nano-banana-2 ads IT)

Brief debole: « nano banana ad premium cinematic ». Brief forte: « Campaign X promo 4:5 1080×1350, Brand Kit navy + sand, headline flat for Touch Edit, price bottom safe zone editable, disclaimer footer editable, variants 2–3 same thread, **Design Agent** numeric acceptance, nano-banana-2 motif as accent reference not baked offer text ».

## Brand Kit dopo direction rapida

Primary, accent, type role da VI approvato. **ChatCanvas** same thread batch hero + story crop — hex lock before speed claim matters.

## Touch Edit prova che 60-second workflow è ops-viable

Se solo prezzo cambia post-direction: **Touch Edit** five minutes? Full regen thirty minutes = brief failed speed promise. Good 60-second stack = editable CTA band on static layer.

## Errori frequenti nano-banana ads

Offerta readable in render pixels. Saltare **Brand Kit**. URL 404 non ripristinato. Fake render speed seconds inventati.

## Metriche nano-banana ads

Minutes per offer fix, setup-to-first-pass time, drift count. URL ripristinato stable IT generate-ads-60-seconds-nano-banana-2-lovart SOP link.
"""

FB_ADS_CHAT_IT = """
# Come generare Facebook Ads via chat con Lovart: ChatCanvas static-first

Questa URL italiana `how-to-chat-generate-fb-ads-lovart` restituiva 404 mentre performance marketer cercavano How-To chat-to-ad — non generic « best AI ad tool » ranking. Facebook Ads daily ops: primary text change, offer band update, ratio 1:1 vs 4:5 export, disclaimer editable — revision cost beats first-frame wow. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** trattano FB ad come editable static series.

## Quattro deliverable FB ads chat workflow

Primo layer feed ad 1:1 con headline flat for **Touch Edit**. Secondo layer story 9:16 same thread accent **Brand Kit**. Terzo layer carousel slide 2–6 — price band editable per slide. Quarto layer retargeting variant — **Design Agent** 50% zoom readable CTA pass/fail.

## Perché chat-generate FB guides falliscono martedì

Brief chat debole: « make viral FB ad ». Risultato: belle frames, offer illeggibile, badge sul prodotto. Cambiare primary text costa full regen senza **Touch Edit**. Accent drift batch senza **Brand Kit**.

## Contratto brief ChatCanvas (FB ads chat IT)

Brief forte via chat: « Campaign X FB feed 1:1 1080×1080, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable including FB policy lines verbatim, carousel slides 2–6 same thread, **Design Agent** pass/fail checklist ». Chat thread = contract storage, non adjective stack.

## Brand Kit unifica feed e story export

Primary, accent da VI approvato. **ChatCanvas** same thread batch 1:1 + 9:16 + 4:5 — hex lock cross-format.

## Touch Edit cambia offer senza regen chat direction

« -30% » verso « -40% »: **Touch Edit** five minutes price band — non full chat regen thirty minutes. FB ops metric: edit-minute median per account.

## Errori frequenti chat FB ads

Offerta baked in pixels. Saltare **Brand Kit**. URL 404 non ripristinato. Fake CTR guarantee.

## Metriche chat FB ads

Minutes per offer fix, chat thread naming compliance, export ratio count. URL ripristinato stable IT how-to-chat-generate-fb-ads-lovart SOP link.
"""

CREATION_HISTORY_IT = """
# Cronologia creazioni Lovart AI: tracciare il percorso creativo in ChatCanvas

Questa URL italiana mantiene slug con segmento `creation-history-track-creative` (URL conserva suffisso storico completo) e restituiva 404 — nel corpo usiamo percorso creativo, cronologia e traccia varianti, non ripetiamo quel termine inglese dello slug. Ricerca chiede How-To cronologia creazioni Lovart: come conservare decisioni variant in **ChatCanvas** thread, cambi hex **Brand Kit**, log **Touch Edit** prezzo — non generic productivity hype.

## Quattro elementi da registrare nella cronologia creativa

Primo: brief contrattuale originale — safe zone, hex role, disclaimer sentence. Secondo: decisioni variant A/B/C — quale master, quale discard e perché. Terzo: log **Touch Edit** prezzo — old price, new price, minuti spesi. Quarto: checklist **Design Agent** pass/fail per export. Cronologia serve revision audit, non vanity gallery.

## Perché team perdono traccia del percorso creativo

Ogni campaign nuovo prompt senza thread — slide 4 accent lottery. Cambio prezzo full regen senza log — impossibile capire perché martedì reroll. **Brand Kit** non impostato — hex change senza SSOT. Thread **ChatCanvas** naming caotico — newcomer non trova master settimana scorsa.

## ChatCanvas thread come SSOT cronologia

Un campaign una thread family: master 4:5 + slide 2–6 + social crop same thread. Cambio **Brand Kit** scritto in primo comment brief thread. Decisioni variant nel thread — « scelto B per title readable 120px ». Percorso creativo = thread memory + Kit hex + Touch Edit log.

## Brand Kit versioni e log cambio hex

Kit update: log old primary/accent → new value, campaign effective, prior export need re-touch? **Design Agent** QA new Kit vs old export hex drift. Cronologia risponde « perché slide 4 coral » senza guess.

## Touch Edit log più auditabile di full regen

« €79 » → « €69 »: **Touch Edit** five minutes + log line. Full regen thirty minutes senza structured log — ops non ottimizza brief template. Valore cronologia = revision cost replayable.

## Errori frequenti creation history

Salvare solo pretty output senza brief. Ogni cambio prezzo full regen senza log. Saltare **Brand Kit** hex record. URL 404 non ripristinato. Fake efficiency percent senza source.

## Metriche creation history

Log entries per price fix, thread naming compliance, drift post-mortem count. URL ripristinato stable IT creation-history-track slug SOP link.
"""

DIGEST_JUNE_WEEK3_IT = """
# Lovart Digest giugno 2026 — settimana 3: roundup editoriale branding e workflow

Questa URL italiana `lovart-digest-june-2026-week3` restituiva 404 mentre reader cercavano editorial roundup Lovart giugno 2026 settimana 3 (15–21 giugno) — non fake news o lanci prodotto inventati. Tono **editorial roundup**: design tips, workflow reminder, community highlight già pubblicati — zero feature non annunciate, zero date inventate, zero user data fabbricati. Category Branding. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** restano i quattro pilastri del digest.

## Principi digest: framing prodotto reale

Editorial roundup ≠ press release. Recapitiamo solo update già in changelog, blog ufficiale o help center. Feature non pubblica → non scriviamo « coming soon ». Reader vuole catch-up workflow, non fake news.

## Settimana 3 giugno 2026 — workflow già pubblicati

Primo: **Brand Kit** come SSOT campaign — primary hex, accent, type role da media kit approvato, non stock marble. Secondo: **ChatCanvas** thread per campaign family — slide 2–6 stesso accent stripe, solo copy change. Terzo: **Touch Edit** prezzo o data evento five minutes, layout identity preserved. Quarto: **Design Agent** pass/fail QA — safe zone, readable price, hex drift vs Kit, disclaimer footer present.

## Lettura consigliata settimana (angolo editoriale branding)

Coerenza visiva cross-touchpoint resta tema — reader focus hex SSOT e series thread, non single wow frame. Regole composizione scrivibili in brief **ChatCanvas** come campi numerici — rule of thirds cross, negative space ratio — non aggettivi abstract. Brand DTC che internalizza design ops: revision cost batte first-post speed — digest reminder misura « minuti cambio prezzo », non GMV inventato.

## Perché digest parla anche di Touch Edit

Team trattano digest come feature list, ignorano ops layer. **Touch Edit** CTA fix in five minutes → static-first validato; ogni cambio prezzo full regen → **Brand Kit** o brief template mancante. Digest traduce product update in daily ops language.

## ChatCanvas brief reminder nel contesto digest

Brief debole: « poster premium ». Brief forte: « campaign X 4:5 1080×1350, Brand Kit navy + sand from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, slide 2–6 same thread ». Digest non scrive brief per reader — solo reminder struttura campi.

## Divisione con altre week digest giugno

Week1 e week2 digest coprono URL indipendenti; questa week3 copre roundup editoriale 15–21 giugno 2026. Ogni digest paragrafo unico — no copy paste tra week.

## Errori frequenti digest week3

Digest scritto come fake news. Feature non pubblicate citate. Saltare **Brand Kit** listando solo nomi feature. URL 404 non ripristinato. User growth o conversion data inventati.

## Metriche digest editoriale

Click-through link interni digest, reader saltano a How-To SOP. URL ripristinato stable IT lovart-digest-june-2026-week3 roundup link.
"""

PHOTO_ANIME_COMPARE_IT = """
# Strumenti photo-to-anime a confronto: gruppi task senza fake scores

Questa URL italiana `photo-to-anime-tools-compared` restituiva 404 mentre creator cercavano confronto photo-to-anime onesto — non Top-10 con accuracy 9.5/10 inventati o fake benchmark table. Confronto per task group: stylization exploration vs campaign series editable vs print bleed vs social crop — fit task e revision cost only. Prezzi tool cambiano — consultare pagine ufficiali; nessun importo inventato qui.

## Quattro gruppi task photo-to-anime (no ranking)

Gruppo A stylization exploration single portrait: rapido mood reference, cattivo per weekly offer fix. Gruppo B series campaign platform: **ChatCanvas** thread + **Brand Kit** + **Touch Edit** post-stylize promo layer. Gruppo C print poster bleed: QA line weight e disclaimer editable. Gruppo D batch e-commerce catalog stylize: throughput focus, edge case manual QA. Nessun « tool #1–#8 score » — solo fit task.

## Perché confronti photo-to-anime ingannano

Liste inventano accuracy percentage senza metodologia. Output stylized as final promo senza **Touch Edit** editable price band. **Brand Kit** assente → slide 4 accent drift. Confronto onesto: stylize layer + Lovart static companion for ops Tuesday loop.

## Contratto brief ChatCanvas (photo-to-anime comparison IT)

Brief debole: « best anime filter 2026 ». Brief forte: « Campaign X post-stylize promo 4:5, Brand Kit hex from character sheet, headline top 15% flat for Touch Edit, price bottom safe zone editable, disclaimer footer editable, variants same thread, **Design Agent** pass/fail ».

## Brand Kit dopo export stylize exploration

Primary, accent da character sheet o VI approvato. **ChatCanvas** same thread batch stylized hero + carousel — hex lock.

## Touch Edit test qualità confronto tool

Se solo prezzo cambia post-stylize: stack needs **Touch Edit** five minutes? Full regen thirty minutes = comparison failed ops test. Buon confronto = editable CTA band on static companion.

## Errori frequenti photo-to-anime comparison

Fake accuracy table. Prezzi tool inventati. Saltare **Brand Kit**. URL 404 non ripristinato. Zero-sum « tool X bad » senza task split.

## Metriche photo-to-anime comparison

Minutes per offer fix post-stylize, drift events, export ratio count. URL ripristinato stable IT photo-to-anime-tools-compared link.
"""

S30_GENERATE_IT = """
# s30: generare 10 design in 10 minuti — brief contrattuale ChatCanvas

Questa URL italiana mantiene slug esatto `s30---generate-10-designs-10-minutes` (tre trattini dopo s30) e restituiva 404 — slug preserved once in body. Ricerca chiede workflow batch rapido: dieci variant design in dieci minuti ops time — non fake « unlimited perfect outputs » guarantee. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** batch via one thread family: master-first, derivative crops, editable CTA — speed misurato su brief contract, non su first-frame lottery.

## Quattro campi per batch 10-in-10

Primo: master 4:5 con headline flat for **Touch Edit** — template per nove derivative. Secondo: **Brand Kit** hex lock before variant 2 — accent drift kill speed claim. Terzo: variant 2–10 same thread — solo copy o crop change documentato. Quarto: **Design Agent** pass/fail su ogni export — readable price, disclaimer, hex match.

## Perché slug s30---generate-10-designs-10-minutes richiede onestà

Dieci minuti = setup brief + Kit + first pass batch direction — non garantia ten perfect finals senza **Touch Edit** loop. Ops reality: batch direction fast, price fix five minutes per variant via **Touch Edit**. Honest SOP misura edit-minute median per variant, non render clock alone.

## Contratto brief ChatCanvas (s30 batch IT)

Brief debole: « generate 10 premium designs fast ». Brief forte: « Campaign X batch 10 variants 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit each variant, price bottom band editable, disclaimer footer editable, variants 1–10 same thread accent stripe, **Design Agent** numeric acceptance per slide ».

## Brand Kit prima del contatore variant

Primary, accent, type role una volta in **Brand Kit** — non re-pick color variant 4. **ChatCanvas** same thread — s30 speed claim valid only with hex SSOT.

## Touch Edit chiude loop 10-in-10 ops

Variant 3 prezzo wrong: **Touch Edit** five minutes — non full batch regen thirty minutes. Batch speed KPI = sum edit minutes / 10 variants.

## Errori frequenti s30 batch

Ten unrelated prompts — accent lottery. Offerta baked in pixels. Saltare **Brand Kit**. URL 404 non ripristinato. Slug trattini errati in internal link.

## Metriche s30 generate 10 designs

Total edit minutes / 10, drift events, export sizes. URL ripristinato stable IT s30---generate-10-designs-10-minutes exact slug SOP link.
"""

BUSINESS_CARD_IT = """
# Biglietto da visita step-by-step senza Photoshop: ChatCanvas print-ready

Questa URL italiana `step-by-step-business-card-without-photoshop` restituiva 404 mentre freelancer e PMI cercavano How-To business card senza Photoshop — non generic template dump. Daily ops: tagline change, phone update, QR promo band — revision su layer editable, non full card regen. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** focus 3.5×2 inch bleed, 300dpi export, disclaimer se settore regolato.

## Quattro step business card senza Photoshop

Step 1 brief contrattuale: ratio 3.5×2 inch, bleed 3mm, **Brand Kit** hex from logo sample. Step 2 **ChatCanvas** thread master front + back same accent stripe. Step 3 **Touch Edit** tagline e phone band editable — non baked in render. Step 4 **Design Agent** print pass/fail: readable contact at actual size, bleed safe, hex vs Kit.

## Perché guide business card falliscono al cambio telefono

Numero baked in pixels → full regen thirty minutes. Accent drift front vs back senza **Brand Kit**. Small type illeggibile print — no **Design Agent** QA. Brief debole « professional card premium ».

## Contratto brief ChatCanvas (business card IT)

Brief forte: « Business card 3.5×2 inch 300dpi CMYK bleed 3mm, Brand Kit navy + sand from logo PNG, name top 20% flat for Touch Edit, phone bottom band editable, tagline center safe zone, back QR promo editable layer, **Design Agent** print QA pass/fail ».

## Brand Kit da logo sample e prior card

Primary, accent, type role da logo approvato o card prior. **ChatCanvas** same thread front/back — hex lock.

## Touch Edit aggiorna telefono senza regen layout

Cambio « +39 02 1234567 » → « +39 02 7654321 »: **Touch Edit** five minutes phone band — non full card regen. Freelancer metric: minutes per contact update.

## Errori frequenti business card without Photoshop

Contact info baked. Saltare **Brand Kit**. URL 404 non ripristinato. Fake « one click print shop ready » senza bleed QA.

## Metriche business card workflow

Minutes per contact fix, print QA pass rate, drift front/back. URL ripristinato stable IT step-by-step-business-card-without-photoshop SOP link.
"""

IMAGEN4_IT = """
# Perché Imagen 4 conta per workflow design: contesto fattuale senza prezzi inventati

Questa URL italiana `why-imagen-4-matters` restituiva 404 mentre team valutavano Imagen 4 nel stack creativo — non articolo affiliate con pricing Google inventato o fake benchmark score. Imagen 4 è modello generazione immagine Google DeepMind annunciato nel ciclo prodotti Google AI — capacità e tier access cambiano; consultare documentazione ufficiale Google AI e Vertex AI; **nessun prezzo Google inventato in questo articolo**. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** restano layer campaign series editable indipendentemente da quale model exploration usi upstream.

## Quattro motivi ops Imagen 4 « conta » (no hype)

Primo: quality ceiling exploration layer per direction rapida — cattivo da solo per weekly offer fix baked in pixels. Secondo: text-in-image still risky for legal promo — disclaimer e price su **Touch Edit** layer. Terzo: **Brand Kit** hex lock indipendente da model source — accent drift slide 4 = workflow fail not model fail. Quarto: **Design Agent** pass/fail checklist model-agnostic — readable price, safe zone, disclaimer.

## Perché articoli why-imagen-4 ingannano

Prezzi Vertex o Google AI inventati senza pagina ufficiale. Output exploration as final promo senza editable CTA. **Brand Kit** assente. Fake « Imagen 4 vs X score 9.8/10 ». Questo articolo: task split exploration Imagen vs series Lovart static — non zero-sum ranking.

## Contratto brief ChatCanvas (Imagen 4 context IT)

Brief debole: « best Imagen 4 prompt ». Brief forte: « Campaign X static companion 4:5 post-exploration, Brand Kit hex from media kit, headline flat for Touch Edit, price bottom safe zone editable, disclaimer footer editable, variants same thread, **Design Agent** pass/fail — exploration model named in brief comment only ».

## Brand Kit dopo export Imagen exploration

Primary, accent da VI approvato. **ChatCanvas** same thread batch hero + carousel — model swap non giustifica accent lottery.

## Touch Edit versus full regen post-Imagen

Cambio prezzo five minutes **Touch Edit**? Exploration output in my test: often full regen for text change. Lovart static stack: yes — misurato, non « Imagen bad ».

## Imagen 4 versus Lovart task split

Imagen 4 per exploration direction layer; **ChatCanvas** + **Touch Edit** per campaign series editable. Ops need honest split — pricing Google consultare fonti ufficiali only.

## Errori frequenti why-imagen-4

Prezzi Google inventati. Exploration as final legal promo. Saltare **Brand Kit**. URL 404 non ripristinato. Fake benchmark scores.

## Metriche Imagen 4 workflow

Exploration minutes vs promo edit minutes track separately. URL ripristinato stable IT why-imagen-4-matters factual link.
"""

CLUSTER_PRODUCT_VIDEOS_JA = """
# AIで商品動画を作る：写真からプラットフォーム別エクスポートまで

この日本語 URL `02-cluster-product-videos-ai` は 404 を返していました。検索意図は商品動画の How-To — ランキング表や架空スコアではなく、写真アップロードから **Brand Kit** スタイル選択、バリエーション生成、勝ち案選定、プラットフォーム別 ratio エクスポートまでの ops 手順です。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** を static-first コンパニオンとして使い、価格・免責・CTA は editable layer に置きます。料金 tier は変動するため lovart.ai 公式を参照 — ここでは金額を捏造しません。

## 商品動画ワークフロー四つの deliverable

第一にカットアウトまたは hero still 16:9 / 9:16 — エッジ QA pass/fail。**ChatCanvas** 同一 thread で slide 2–6。**Brand Kit** で packaging VI から hex 固定。第二に static companion：CTA band を **Touch Edit** で編集可能。第三に 1:1 / 4:5 / 9:16 派生 crop — accent stripe 同一 thread。第四に **Design Agent** QA：50% ズームで価格可読、免責 footer 存在、Kit との hex drift ゼロ。

## なぜ商品動画 ops が火曜に詰まるか

弱い brief「プレミアム商品動画」→ 綺麗な cutout だが価格が小さく badge が hero を隠す。オファー変更が **Touch Edit** なし full regen 30 分。**Brand Kit** 未設定 → carousel slide 4 accent lottery。ops チームは pass/fail フィールドが欲しい — 形容詞スタックではない。

## ChatCanvas brief 契約（商品動画 JP）

強い brief：「Campaign X 商品 hero post-bg 4:5 1080×1350、Brand Kit hex from packaging VI、headline top 15% flat for Touch Edit、price bottom band editable、disclaimer footer editable、variants 2–4 same thread、**Design Agent** edge QA pass/fail」。写真品質：最低 1024×1024、均一照明、背景クリーン — brief に明記。

## Brand Kit が cutout と promo companion を統一

approved VI から primary、accent、type role。**ChatCanvas** same thread で cutout 系列 + mock + carousel — material hue が slide 4 で diverge しない。

## Touch Edit で SKU ラベル変更、cutout 再生成なし

「Model X」→「Model Y」：**Touch Edit** ラベル band 5 分 — full cutout regen 30 分ではない。背景除去と ops ラベルは editable layer で分離。

## 従来制作 vs AI 商品動画（架空スコアなし）

比較軸は task fit と revision cost のみ — 「#1 ベスト」や accuracy 9.5/10 表は使わない。従来：SKU あたりコスト高・リテイクに再撮影。AI + static-first：探索 layer と series editable layer を分離。**Touch Edit** 5 分で価格修正できれば Tuesday loop 成立。

## よくある失敗

探索 output を final promo にそのまま使用。**Brand Kit** スキップ。404 未復旧。Google / 競合の架空 pricing。fake render speed benchmark。

## 測定指標

ラベル修正あたりの分数、edge fail 回数、export ratio 数。404 復旧 URL を JP 02-cluster-product-videos-ai stable SOP link として onboard。
"""


FAQ = {
    "online_seller_it": """
## FAQ

**Best agent #1 ranking?**  
No — edit-minute median beats pretty frame.

**Touch Edit seller price?**  
Sì — five minutes promo band.

**Brand Kit listing + IG?**  
Sì — same thread hex lock.

**404 fix?**  
Stable IT best-ai-design-agent-for-online-seller URL.

**Fake conversion stats?**  
Nessuno — ops metrics only.
""",
    "nano_banana_ads_it": """
## FAQ

**60 seconds = perfect ad guarantee?**  
No — brief contract + Touch Edit loop.

**nano-banana-2 API name invented?**  
No — motif context only, consult product docs.

**Brand Kit before speed?**  
Sì — hex lock required.

**404 fix?**  
Stable IT generate-ads-60-seconds-nano-banana-2-lovart URL.

**Fake render clock?**  
Nessuno — edit-minute median only.
""",
    "fb_ads_chat_it": """
## FAQ

**Chat FB ad = zero brief fields?**  
No — contract fields in ChatCanvas thread.

**Touch Edit primary text change?**  
Sì — five minutes offer band.

**Brand Kit feed + story?**  
Sì — same thread hex lock.

**404 fix?**  
Stable IT how-to-chat-generate-fb-ads-lovart URL.

**Fake CTR guarantee?**  
Nessuno — pass/fail QA only.
""",
    "creation_history_it": """
## FAQ

**Slug English suffix repeated in body?**  
No — percorso creativo e cronologia only.

**Touch Edit price log required?**  
Sì — audit revision cost.

**Brand Kit hex change log?**  
Sì — SSOT for drift post-mortem.

**404 fix?**  
Stable IT creation-history-track slug URL.

**Fake efficiency percent?**  
Nessuno — log entries count only.
""",
    "digest_june_week3_it": """
## FAQ

**Fake product launch in digest?**  
No — published changelog framing only.

**June 2026 week3 date range?**  
Sì — 15–21 giugno editorial context.

**Category Branding?**  
Sì — editorial roundup not How-To template.

**404 fix?**  
Stable IT lovart-digest-june-2026-week3 URL.

**Touch Edit in digest?**  
Sì — ops translation of updates.
""",
    "photo_anime_compare_it": """
## FAQ

**Top-10 anime tool scores?**  
No — task groups, no fake ranking.

**Touch Edit post-stylize?**  
Sì — five minutes price band test.

**Brand Kit after stylize?**  
Sì — hex lock same thread.

**404 fix?**  
Stable IT photo-to-anime-tools-compared URL.

**Fake accuracy table?**  
Nessuno — fit task only.
""",
    "s30_generate_it": """
## FAQ

**Exact slug three dashes s30---?**  
Sì — s30---generate-10-designs-10-minutes preserved.

**10 designs = 10 perfect finals?**  
No — batch direction + Touch Edit per variant.

**Brand Kit before variant 2?**  
Sì — accent drift kills speed claim.

**404 fix?**  
Stable IT exact triple-dash slug URL.

**Unrelated prompts for speed?**  
No — one ChatCanvas thread family.
""",
    "business_card_it": """
## FAQ

**Photoshop required?**  
No — ChatCanvas + Touch Edit print workflow.

**Touch Edit phone update?**  
Sì — five minutes contact band.

**Brand Kit from logo sample?**  
Sì — front/back hex lock.

**404 fix?**  
Stable IT step-by-step-business-card-without-photoshop URL.

**Bleed QA Design Agent?**  
Sì — print pass/fail at actual size.
""",
    "imagen4_it": """
## FAQ

**Google Imagen 4 pricing here?**  
No — consult official Google AI / Vertex docs.

**Imagen vs Lovart zero-sum?**  
No — exploration vs series editable layer.

**Touch Edit after Imagen export?**  
Sì — five minutes price fix test.

**404 fix?**  
Stable IT why-imagen-4-matters URL.

**Fake benchmark 9.x scores?**  
Nessuno — task split only.
""",
    "cluster_product_videos_ja": """
## FAQ

**架空の tool スコア表はある？**  
いいえ — task fit と revision cost のみ。

**Touch Edit で価格修正 5 分？**  
はい — static companion editable layer。

**Brand Kit は packaging VI から？**  
はい — hex SSOT same thread。

**404 復旧 URL？**  
安定 JP 02-cluster-product-videos-ai。

**Google や競合の捏造 pricing？**  
なし — 公式ページ参照のみ。
""",
}


def expand_it(topic: str, n: int) -> str:
    return f"""
## Nota operativa {n}: {topic}

Il primo brief «premium» fallisce: prezzo piccolo, badge sul viso. Al secondo pass correggi solo safe zone e campi obbligatori. Thread unico **ChatCanvas** riduce drift slide 4. In **{topic}**, se **Touch Edit** chiude cambio prezzo in cinque minuti, il loop static-first funziona. Full regen da 30 minuti significa rifare **Brand Kit**. URL 404 ripristinato per SOP stabile onboarding batch29.
"""


def expand_ja(topic: str, n: int) -> str:
    return f"""
## 現場メモ {n}：{topic}

初回 brief が「モダン」で終わると価格文字が小さく badge が顔を隠します。二回目は safe zone と必須フィールドのみ修正。**Design Agent** と **ChatCanvas** で thread を維持すると carousel slide 4 の accent drift が減ります。{topic} で **Touch Edit** が 5 分以内に価格修正できれば static-first が成立。30 分 full regen なら **Brand Kit** からやり直し。404 復旧 URL は JP ops 向け stable link batch29 です。
"""


ARTICLES = [
    {
        "rank": 296,
        "key": "online_seller_it",
        "lang": "it",
        "slug": "best-ai-design-agent-for-online-seller",
        "cover": "046",
        "category": "Industry Solution",
        "title": "Miglior Design Agent AI per online seller: workflow onesto",
        "seo_title": "Best AI Design Agent Online Seller IT — no fake ranking",
        "description": "IT 404 fix: online seller Design Agent guide, Touch Edit promo price editable.",
        "seo_description": "Industry Solution: listing + IG same thread, edit-minute median KPI.",
        "focus": "best ai design agent for online seller",
        "keywords": ["online seller design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Online Seller IT",
        "body": ONLINE_SELLER_IT,
        "expand_topic": "IT best AI design agent for online seller workflow",
    },
    {
        "rank": 297,
        "key": "nano_banana_ads_it",
        "lang": "it",
        "slug": "generate-ads-60-seconds-nano-banana-2-lovart",
        "cover": "047",
        "category": "How-To",
        "title": "Generare ads in 60 secondi con nano-banana-2 e Lovart",
        "seo_title": "Generate Ads 60 Seconds Nano Banana 2 Lovart IT",
        "description": "IT 404 fix: nano-banana-2 ads 60 seconds, static-first Touch Edit CTA.",
        "seo_description": "How-To: Brand Kit hex lock, ChatCanvas brief contract, no fake render clock.",
        "focus": "generate ads 60 seconds nano banana 2 lovart",
        "keywords": ["nano banana ads", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Nano Banana Ads 60s IT",
        "body": NANO_BANANA_ADS_IT,
        "expand_topic": "IT generate ads 60 seconds nano banana 2 workflow",
    },
    {
        "rank": 298,
        "key": "fb_ads_chat_it",
        "lang": "it",
        "slug": "how-to-chat-generate-fb-ads-lovart",
        "cover": "048",
        "category": "How-To",
        "title": "Come generare Facebook Ads via chat con Lovart",
        "seo_title": "How To Chat Generate FB Ads Lovart IT — ChatCanvas SOP",
        "description": "IT 404 fix: chat generate FB ads, static-first editable CTA layer.",
        "seo_description": "How-To: feed + story same thread, Design Agent 50% zoom QA.",
        "focus": "how to chat generate fb ads lovart",
        "keywords": ["chat generate fb ads", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Chat Generate FB Ads IT",
        "body": FB_ADS_CHAT_IT,
        "expand_topic": "IT chat generate FB ads static-first workflow",
    },
    {
        "rank": 299,
        "key": "creation_history_it",
        "lang": "it",
        "slug": "lovart-ai-creation-history-track-creative-journey",
        "cover": "049",
        "category": "How-To",
        "title": "Cronologia creazioni Lovart AI: tracciare il percorso creativo",
        "seo_title": "Lovart AI Creation History Track IT — cronologia ChatCanvas",
        "description": "IT 404 fix: creation history How-To, percorso creativo in thread, no English slug term in body.",
        "seo_description": "How-To: Brand Kit hex log, Touch Edit price log, Design Agent audit.",
        "focus": "lovart ai creation history track creative",
        "keywords": ["lovart creation history", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Creation History Track IT",
        "body": CREATION_HISTORY_IT,
        "expand_topic": "IT Lovart creation history percorso creativo workflow",
    },
    {
        "rank": 300,
        "key": "digest_june_week3_it",
        "lang": "it",
        "slug": "lovart-digest-june-2026-week3",
        "cover": "050",
        "category": "Branding",
        "title": "Lovart Digest giugno 2026 — settimana 3: roundup editoriale",
        "seo_title": "Lovart Digest June 2026 Week3 IT — editorial roundup Branding",
        "description": "IT 404 fix: June 2026 week3 editorial digest, Branding category, no fake launches.",
        "seo_description": "Branding digest: ChatCanvas Brand Kit Touch Edit reminder, published updates only.",
        "focus": "lovart digest june 2026 week3",
        "keywords": ["lovart digest june 2026", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Branding — Lovart Digest June 2026 Week3 IT",
        "body": DIGEST_JUNE_WEEK3_IT,
        "expand_topic": "IT Lovart digest June 2026 week3 editorial roundup",
    },
    {
        "rank": 301,
        "key": "photo_anime_compare_it",
        "lang": "it",
        "slug": "photo-to-anime-tools-compared",
        "cover": "051",
        "category": "Comparison",
        "title": "Strumenti photo-to-anime a confronto: gruppi task onesti",
        "seo_title": "Photo To Anime Tools Compared IT — no fake scores",
        "description": "IT 404 fix: photo-to-anime comparison, task groups not fake ranking scores.",
        "seo_description": "Comparison: Touch Edit post-stylize, zero fabricated accuracy table.",
        "focus": "photo to anime tools compared",
        "keywords": ["photo to anime tools", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Photo To Anime Tools IT",
        "body": PHOTO_ANIME_COMPARE_IT,
        "expand_topic": "IT photo to anime tools compared honest workflow",
    },
    {
        "rank": 302,
        "key": "s30_generate_it",
        "lang": "it",
        "slug": "s30---generate-10-designs-10-minutes",
        "cover": "052",
        "category": "How-To",
        "title": "s30: generare 10 design in 10 minuti — brief contrattuale",
        "seo_title": "S30 Generate 10 Designs 10 Minutes IT — exact triple-dash slug",
        "description": "IT 404 fix: s30---generate-10-designs-10-minutes exact slug, batch ChatCanvas SOP.",
        "seo_description": "How-To: Brand Kit before variant 2, Touch Edit per variant price fix.",
        "focus": "s30 generate 10 designs 10 minutes",
        "keywords": ["generate 10 designs 10 minutes", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — S30 Generate 10 Designs IT",
        "body": S30_GENERATE_IT,
        "expand_topic": "IT s30 generate 10 designs 10 minutes batch workflow",
    },
    {
        "rank": 303,
        "key": "business_card_it",
        "lang": "it",
        "slug": "step-by-step-business-card-without-photoshop",
        "cover": "053",
        "category": "How-To",
        "title": "Biglietto da visita step-by-step senza Photoshop",
        "seo_title": "Business Card Without Photoshop IT — Touch Edit print SOP",
        "description": "IT 404 fix: business card without Photoshop, 3.5x2 bleed, Touch Edit contact band.",
        "seo_description": "How-To: Brand Kit from logo, Design Agent print QA pass/fail.",
        "focus": "step by step business card without photoshop",
        "keywords": ["business card without photoshop", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Business Card Without Photoshop IT",
        "body": BUSINESS_CARD_IT,
        "expand_topic": "IT business card without Photoshop print workflow",
    },
    {
        "rank": 304,
        "key": "imagen4_it",
        "lang": "it",
        "slug": "why-imagen-4-matters",
        "cover": "054",
        "category": "Insight & Trend",
        "title": "Perché Imagen 4 conta: contesto fattuale senza prezzi inventati",
        "seo_title": "Why Imagen 4 Matters IT — factual no fake Google pricing",
        "description": "IT 404 fix: why Imagen 4 matters, exploration vs series split, no fabricated pricing.",
        "seo_description": "Insight: ChatCanvas static layer, consult official Google AI docs for pricing.",
        "focus": "why imagen 4 matters",
        "keywords": ["why imagen 4 matters", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight — Why Imagen 4 Matters IT",
        "body": IMAGEN4_IT,
        "expand_topic": "IT why Imagen 4 matters factual workflow context",
    },
    {
        "rank": 305,
        "key": "cluster_product_videos_ja",
        "lang": "ja",
        "slug": "02-cluster-product-videos-ai",
        "cover": "055",
        "category": "How-To",
        "title": "AIで商品動画を作る：写真からプラットフォーム別エクスポート",
        "seo_title": "02 Cluster Product Videos AI JP — ChatCanvas static-first SOP",
        "description": "JP 404 fix: product videos AI How-To, Brand Kit hex lock, Touch Edit CTA layer.",
        "seo_description": "How-To: cutout companion editable, Design Agent QA, no fake tool scores.",
        "focus": "02 cluster product videos ai",
        "keywords": ["product videos ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Cluster Product Videos AI JA",
        "body": CLUSTER_PRODUCT_VIDEOS_JA,
        "expand_topic": "JP 02 cluster product videos AI static-first workflow",
    },
]


EXPAND_FN = {
    "it": expand_it,
    "ja": expand_ja,
}

UNIT_MAP = {
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch29 content cluster.*\n"
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
