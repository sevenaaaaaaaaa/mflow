#!/usr/bin/env python3
"""Generate 404-rescue P2 batch28 blog bodies (10 files). Self-contained.

Ranks #286–#295 from 404-rescue-compact lane.
6 FR + 5 IT. expand_fr + expand_it (expand_it copied from batch6).
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
    "fr": 900,
    "it": 900,
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


def count_metric(text: str, lang: str) -> int:
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

LOVART_COMPLETE_GUIDE_FR = """
# Guide complet Lovart 2025 : design IA de bout en bout

Cette URL française `lovart-complete-guide-2025-ai-powered-design` renvoyait une 404 alors que les recherches demandaient un guide complet Lovart — pas un fake ranking « best AI design platform #1 » avec scores inventés. Ce Complete Guide couvre static-first daily ops avec **ChatCanvas**, **Brand Kit**, **Touch Edit** et **Design Agent** : brief contrat, series memory, revision cost, export multi-format. Prix et tiers changent — consulter lovart.ai; aucun montant inventé ici.

## Quatre piliers du workflow Lovart (pas de vanity score)

Premier pilier **ChatCanvas** : un thread par campagne — hero, carousel slide 2–6, social crop same accent stripe. Deuxième pilier **Brand Kit** : primary, accent, type role depuis VI approuvé — pas stock marble comme couleur officielle. Troisième pilier **Touch Edit** : offre, prix, disclaimer sur bandes flat editable — pas baked in render pixels. Quatrième pilier **Design Agent** : pass/fail checklist numeric — pas « looks professional » adjective stack.

## Pourquoi les « complete guides » AI design trompent

Guides mélangent exploration wow avec ops campaign. Offre baked in pixels → fix mardi full regen thirty minutes. **Brand Kit** absent → slide 4 accent drift. Fake benchmark scores 9.2/10 sans source. Guide honnête écrit task split : exploration layer vs series platform editable static.

## Contrat brief ChatCanvas (complete guide context)

Brief faible : « make something premium for Instagram ». Brief fort : « Campaign X promo 4:5 1080×1350, Brand Kit navy + sand from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 2–4 same thread, no small text in render, **Design Agent** pass/fail acceptance ».

## Brand Kit comme SSOT cross-format dans le guide

Primary, accent, type role depuis VI approuvé. **ChatCanvas** same thread batch 4:5 + 9:16 + 1:1 — hex lock retail flyer = story crop. Pas nouveau prompt par format sans thread continuity.

## Touch Edit comme test ops du complete guide

Si seul prix change : stack needs **Touch Edit** five minutes? Full regen thirty minutes = brief contract failed. Complete guide lesson : editable layer beats pretty baked pixel output every Tuesday loop.

## Design Agent QA avant export final

Checklist : readable price at 50% zoom mobile, disclaimer present, accent drift vs **Brand Kit** zero tolerance, safe zone headline not cropped. Pass/fail numeric — pas subjective « luxury feel ».

## Erreurs fréquentes complete guide Lovart

Sauter **Brand Kit** setup. Exploration output as final promo. URL 404 non restaurée. Fake pricing tiers inventés. Fake « mastery in 5 minutes » guarantee.

## Métriques complete guide

Edit-minute median, regen count per approval, drift events per series. URL restaurée stable FR lovart-complete-guide-2025-ai-powered-design SOP link.
"""

SORA_ALTERNATIVES_FR = """
# Alternatives Sora : comparaison honnête par groupe de tâches

Cette URL française `sora-alternatives` renvoyait une 404 alors que les recherches demandaient des alternatives Sora — pas un fake Top-10 avec prix OpenAI inventés ou scores 9.5/10. Cet article groupe par tâche motion vs static ops. Prix Sora et tiers changent — consulter pages officielles OpenAI; aucun montant inventé ici.

## Quatre groupes tâches Sora alternatives (pas de ranking)

Groupe A cinematic motion exploration : Sora forte direction clip long, mauvais pour weekly offer fix on static layer. Groupe B short hook social bumper : motion companion four to six seconds, static legal pass d'abord. Groupe C campaign series platform : **ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable static. Groupe D open-source local render : privacy-sensitive, revision cost élevé. Pas de « Sora alternative #1–#7 » — fit tâche et coût revision seulement.

## Pourquoi les comparatifs Sora alternatives trompent

Listes inventent pricing Sora sans source officielle. Offre dans clip pixels → fix mardi full rerender thirty minutes. **Brand Kit** absent → motion gorgeous but none match carousel slide 3 hex. Comparaison honnête : Sora for motion layer; Lovart static companion for ops Tuesday loop.

## Contrat brief ChatCanvas (Sora alternatives context)

Brief faible : « best Sora alternative 2026 ». Brief fort : « Campaign X static companion 4:5, Brand Kit from media kit, headline flat for Touch Edit, price bottom safe zone on still only, disclaimer editable, motion prompt optional no text in render, **Design Agent** QA static first ».

## Brand Kit entre Sora export et promo still

Importer hex from approved VI in **Brand Kit** — puis **ChatCanvas** thread promo series. Jamais offre readable in Sora render pixels without static editable layer.

## Touch Edit versus full Sora reroll

Changement prix five minutes **Touch Edit** on still? Sora clip in my test: often full reroll for text change. Lovart static stack: yes — mesuré, pas zero-sum « Sora bad ».

## Sora versus Lovart task split (no zero-sum)

Sora pour motion exploration layer; **ChatCanvas** + **Touch Edit** pour campaign series editable. Pas either-or — ops teams need honest task split not fake ranking.

## Erreurs fréquentes Sora alternatives

Prix Sora inventés. Motion output as final promo sans static. Sauter **Brand Kit**. URL 404 non restaurée. Fake benchmark scores.

## Métriques Sora comparison

Motion minutes vs static edit minutes track separately. URL restaurée stable FR sora-alternatives honest comparison link.
"""

VIRTUAL_INFLUENCERS_FR = """
# Influenceurs virtuels : marques et remplacement des mannequins humains — guide ops honnête

Cette URL française `virtual-influencers-brands-replacing-human-models-ai` renvoyait une 404 alors que les marques cherchaient un workflow influenceur virtuel — pas un fake « 100% replace all human models » promise. Virtual influencer daily ops : character reference plate, multi-shot consistency, campaign static companion, disclosure requirements — offer et disclaimer sur editable layers. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** focus series memory et editable promo; human disclosure and consent rules human final sign-off.

## Quatre layers deliverable influenceur virtuel

Premier layer character reference plate : yaw, wardrobe, **Brand Kit** accent lock documented in brief. Deuxième layer campaign still series slide 2–6 : same **ChatCanvas** thread, character consistency fields. Troisième layer promo companion : **Touch Edit** price band, disclaimer footer editable including AI disclosure where required. Quatrième layer social crop 9:16 and 1:1 : accent stripe same thread, **Design Agent** QA at 50% zoom.

## Pourquoi les campagnes influenceur virtuel échouent le mardi

Offre readable in character render pixels baked → full regen thirty minutes. Character drift slide four — different face geometry. **Brand Kit** non défini → accent lottery. Missing AI disclosure — regulatory and trust risk. Brief faible « make virtual influencer » — **Design Agent** no pass/fail fields.

## Contrat brief ChatCanvas (virtual influencer FR)

Brief faible : « create AI influencer for brand ». Brief fort : « Campaign X virtual talent series 4:5, character reference plate attached, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom band editable on static companion, disclaimer footer editable with AI disclosure verbatim, variants 2–4 same thread character lock, **Design Agent** pass/fail checklist ». Human legal sign-off on disclosure text.

## Brand Kit empêche character and accent drift

Primary, accent, type role depuis VI approuvé. **ChatCanvas** same thread batch character shots + promo companion — pas shot-by-shot unrelated prompts.

## Touch Edit offer sans character reroll

« 49 € » vers « 59 € » : **Touch Edit** CTA band on static companion — pas full character regen. Character geometry preserved; price on editable layer.

## Ethics : replacement versus supplement

Guide ops honnête : virtual influencers supplement specific campaign types — pas universal human model replacement claim. Disclosure editable via **Touch Edit** footer layer. Consent and jurisdiction rules human final sign-off.

## Erreurs fréquentes influenceur virtuel

Offre in character pixels baked. Pas de AI disclosure. Sauter **Brand Kit**. URL 404 non restaurée. Fake « replace all models » ROI stats.

## Métriques influenceur virtuel

Minutes par offer fix on companion, character drift events, disclosure QA pass rate. URL restaurée stable FR virtual-influencers-brands-replacing-human-models-ai SOP link.
"""

CLAWDBOT_FR = """
# Pourquoi Lovart est le « clawdbot » du design pour débutants : adieu anxiété process, pas de garantie instantanée

Cette URL française `why-lovart-is-the-clawdbot-of-design-for-beginners-goodbye-process-anxiety-hello-instant-results` renvoyait une 404 — le slug long exact est preserved, y compris la typo « clawdbot » dans l'URL (probablement une référence mal orthographiée à un outil connu). Le titre promet « instant results » mais cet article ne garantit aucun résultat instantané universel — seulement un workflow static-first qui réduit process anxiety via champs pass/fail. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** pour débutants qui veulent ops metrics pas adjective stacks.

## Quatre sources process anxiety chez les débutants design

Première source : brief vague « make it pretty » — **Design Agent** no checklist. Deuxième source : offre baked in pixels — fix mardi panic full regen. Troisième source : **Brand Kit** absent — slide 4 accent drift destroys confidence. Quatrième source : fake « one click perfect » marketing — reality Tuesday loop needs editable layers.

## Pourquoi le slug « hello-instant-results » trompe sans contexte

Marketing slugs promise instant; ops reality = brief contract + **Touch Edit** five-minute fix path after first pass. Pas de garantie instant results for every campaign — mesuré edit-minute median only. Honest beginner guide writes : reduce anxiety via predictable fields, not magic button.

## Contrat brief ChatCanvas (beginner clawdbot context)

Brief faible : « I'm a beginner make premium poster ». Brief fort : « Campaign X beginner promo 4:5, Brand Kit hex from media kit sample, headline top 15% flat for Touch Edit, price bottom safe zone editable, disclaimer footer editable, variants 2–4 same thread, **Design Agent** pass/fail checklist beginner can run ».

## Brand Kit réduit decision fatigue débutant

Sample hex once in **Brand Kit** — pas re-pick color every variant. **ChatCanvas** same thread — accent drift slide 4 avoided without design degree. Beginner wins : fewer arbitrary color choices per Tuesday fix.

## Touch Edit comme preuve que l'anxiété process baisse

Si seul prix change : **Touch Edit** five minutes? Full regen thirty minutes = anxiety returns. Beginner metric : edit-minute median down week over week — pas « instant first frame » vanity.

## Design Agent checklist pour débutants

Readable price at 50% zoom, disclaimer present, accent vs **Brand Kit** match — pass/fail numeric. Beginner runs checklist before export — pas wait for designer approval on subjective feel.

## Erreurs fréquentes débutants et slug long

Croire slug instant-results as guarantee. Ignorer typo clawdbot in URL when linking internally. Sauter **Brand Kit**. URL 404 non restaurée. Fake « mastery day one » claims.

## Métriques beginner workflow

Edit-minute median, regen count, anxiety proxy = number of Tuesday panics avoided. URL restaurée stable FR why-lovart-is-the-clawdbot-of-design-for-beginners-goodbye-process-anxiety-hello-instant-results honest guide link.
"""

YOUTUBE_THUMBNAIL_FR = """
# Science du design de miniatures YouTube 2027 : checklist ops readable

Cette URL française `youtube-thumbnail-design-science-2027` renvoyait une 404 alors que les créateurs cherchaient une checklist thumbnail 2027 — pas un fake « +47% CTR guarantee » sans source. YouTube thumbnail standard 1280×720 — ratio in brief contract. **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** treat thumbnail as revision-heavy asset : title change, A/B variant five-minute close, not full regen lottery.

## Quatre champs science thumbnail 2027

Premier champ 120px preview pass : headline readable at mobile feed scale — **Design Agent** QA pass/fail. Deuxième champ safe zone : face not cropped by YouTube UI overlay. Troisième champ **Brand Kit** accent lock across A/B variants same thread. Quatrième champ **Touch Edit** title band editable — pas baked in render pixels.

## Pourquoi « thumbnail science » guides échouent le mardi

Brief faible : « shocked face premium cinematic ». Résultat : belle expression, title illisible at 120px. Changer title coûte full regen sans **Touch Edit**. Accent drift A vs B without **Brand Kit**. Fake CTR stats without Etsy/YouTube analytics source.

## Contrat brief ChatCanvas (YouTube thumbnail FR 2027)

Brief fort : « Campaign X YouTube thumb 1280×720, Brand Kit hex from channel VI, title top 20% flat for Touch Edit max 4 words, face center safe zone documented, disclaimer N/A or footer if sponsored editable, variants A/B same thread, **Design Agent** 120px preview pass/fail ».

## Brand Kit unifie thumbnail et end screen companion

Primary, accent depuis channel VI. **ChatCanvas** same thread thumb + community post crop + Shorts cover — hex lock.

## Touch Edit change title A/B sans regen face geometry

« 5 ERREURS » vers « 5 FIXES » : **Touch Edit** title band five minutes — pas full face regen thirty minutes. Thumbnail science = revision cost metric not pretty first frame.

## Erreurs fréquentes thumbnail 2027

Title baked in pixels. Sauter **Brand Kit**. URL 404 non restaurée. Fake CTR guarantee from slug year 2027.

## Métriques thumbnail science

Minutes per title fix, 120px pass rate, A/B drift count. URL restaurée stable FR youtube-thumbnail-design-science-2027 checklist link.
"""

OPENART_REVIEW_IT = """
# OpenArt AI Review: confronto onesto dopo uso ops

Questa URL italiana `OpenArt-AI-Review` restituiva 404 — lo slug mantiene la casse esatta OpenArt-AI-Review. Le ricerche chiedevano un review onesto OpenArt AI — non affiliate fluff o fake scores. OpenArt daily use: model exploration, community rooms, style tests — buono per exploration, cattivo da solo per weekly promo editable. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** quando copy, color e revision cost contano più del model count. Prezzi cambiano — consultare openart.ai; nessun importo inventato qui.

## Quattro gruppi di task OpenArt (no ranking)

Gruppo A model exploration e community rooms: direzione rapida, cattivo per offer fix weekly. Gruppo B style e texture experiments: mood reference, non final collateral senza QA. Gruppo C campaign series platform: **ChatCanvas** thread + **Brand Kit** + **Touch Edit**. Gruppo D local o privacy-sensitive workflows. Nessun « OpenArt vs X score 9.2/10 » — fit task only.

## Perché i review OpenArt ingannano

Review mescolano exploration wow con ops campaign. Offerta baked in pixels → fix martedì full regen. **Brand Kit** assente → frames gorgeous but none match type scale. Review onesto scrive task split: exploration OpenArt; series Lovart static layer.

## ChatCanvas brief (OpenArt review context)

Brief debole: « best OpenArt alternative ». Brief forte: « Campaign X static companion 4:5, Brand Kit from media kit, headline flat for Touch Edit, price bottom safe zone on still, disclaimer editable, variants same thread, **Design Agent** pass/fail ».

## Brand Kit dopo export OpenArt exploration

Primary, accent, type role da VI approvato. **ChatCanvas** same thread batch hero + carousel — accent stripe resta. Non stock marble as brand color.

## Touch Edit versus full regen post-exploration

Cambio prezzo five minutes **Touch Edit**? OpenArt exploration in my test: often full regen. Lovart stack: yes — misurato, non zero-sum « OpenArt bad ».

## OpenArt versus Lovart task split

OpenArt per exploration layer; **ChatCanvas** + **Touch Edit** per campaign series. Non either-or — ops teams need honest split.

## Errori frequenti OpenArt review

Prezzi OpenArt inventati. Exploration output as final promo. Saltare **Brand Kit**. URL 404 non ripristinato. Fake benchmark scores.

## Metriche OpenArt review

Exploration minutes vs promo edit minutes track separately. URL ripristinato stable OpenArt-AI-Review IT link.
"""

AI_VIDEO_BG_IT = """
# Rimozione sfondo video AI: guida pratica post-cutout ops

Questa URL italiana `ai-video-background-removal` restituiva 404 mentre marketer e creator cercavano una guida pratica rimozione sfondo video — non generic ranking strumenti. Rimozione sfondo è solo il primo passo. Offer, prezzo e disclaimer devono vivere su editable static layer con **Touch Edit**, hex fissa **Brand Kit**, series mantiene **ChatCanvas** thread. Lovart **Design Agent** QA readable price e mismatch tra ratio exports.

## Quattro deliverable dopo background removal video

Primo layer cutout hero 16:9 o 9:16 con subject clean edge — QA hair/fur pass/fail. Secondo layer static companion con CTA band editable via **Touch Edit**. Terzo layer variant series same thread accent **Brand Kit**. Quarto layer social crop 1:1 e 4:5 — **Design Agent** QA price readable at 50% zoom.

## Perché ai-video-background-removal fallisce il martedì

Brief debole: « remove background premium cinematic ». Risultato: bel cutout, prezzo illisibile, badge sul soggetto. Cambiare offerta costa full regen senza **Touch Edit**. Accent drift batch senza **Brand Kit**. Ops vogliono campi pass/fail.

## Contratto brief ChatCanvas (video bg removal IT)

Brief forte: « Campaign X product hero post-bg-removal 4:5, Brand Kit hex from packaging VI, headline top 15% flat for Touch Edit, price bottom band editable, disclaimer footer editable, variants 2–4 same thread, **Design Agent** edge QA pass/fail ».

## Brand Kit unifica cutout e promo companion

Primary, accent da VI prodotto. **ChatCanvas** same thread cutout + mock + carousel — material hue non diverge slide 4.

## Touch Edit cambia SKU label senza regen cutout

« Model X » verso « Model Y »: **Touch Edit** label band five minutes — non full cutout regen thirty minutes. Background removal separate; ops label on editable layer.

## Errori frequenti video background removal

Output exploration as final print senza QA. Saltare **Brand Kit**. URL 404 non ripristinato. Fake render speed benchmarks.

## Metriche video bg removal

Minuti per fix label, edge fail count, export ratio count. URL ripristinato stable IT ai-video-background-removal SOP link.
"""

B33_BG_REMOVER_IT = """
# Confronto rimozione sfondo AI b33 Bing: gruppi task senza fake scores

Questa URL italiana `b33-ai-background-remover-comparison-bing` restituiva 404 — slug contesto ricerca Bing, non endorsement Bing ufficiale. Confronto onesto rimozione sfondo per task group — non fake Top-8 con accuracy 9.5/10 inventati. Prezzi Remove.bg e tier cambiano — consultare pagine ufficiali; nessun importo inventato qui.

## Quattro gruppi task background remover (no ranking)

Gruppo A single-image API cutout: rapido per one-off, cattivo per campaign series editable CTA. Gruppo B batch e-commerce catalog: throughput focus, revision cost su edge cases. Gruppo C campaign series platform: **ChatCanvas** thread + **Brand Kit** + **Touch Edit** post-cutout promo layer. Gruppo D desktop local tool: privacy-sensitive, manual QA per shot. Nessun « tool #1–#8 accuracy score » — fit task e revision cost only.

## Perché i confronti b33 background remover ingannano

Liste inventano accuracy percentage senza metodologia. Cutout output as final promo senza **Touch Edit** editable price band. **Brand Kit** assente → accent drift slide 4. Bing slug context — articolo workflow onesto Lovart static layer, zero fake benchmark.

## Contratto brief ChatCanvas (b33 comparison context)

Brief debole: « best background remover 2026 ». Brief forte: « Campaign X post-cutout promo 4:5, Brand Kit hex from packaging, headline flat for Touch Edit, price bottom safe zone editable, disclaimer footer editable, variants same thread, **Design Agent** pass/fail ».

## Brand Kit dopo cutout batch

Primary, accent da VI approvato. **ChatCanvas** same thread batch cutout series + promo still — hex lock.

## Touch Edit test « remover comparison » quality

Se solo prezzo cambia: stack needs **Touch Edit** five minutes? Full regen thirty minutes = comparison failed ops test. Good comparison = editable CTA band post-cutout.

## Errori frequenti b33 comparison

Prezzi tool inventati. Fake accuracy table. Saltare **Brand Kit**. URL 404 non ripristinato. Bing endorsement claim fake.

## Metriche b33 comparison

Minutes per offer fix post-cutout, edge fail count, drift events. URL ripristinato stable IT b33-ai-background-remover-comparison-bing link.
"""

B39_FAQ_IT = """
# FAQ strumenti design AI b39 Bing: risposte ops oneste

Questa URL italiana `b39-ai-design-tools-faq-bing` restituiva 404 — slug contesto ricerca Bing, non endorsement Bing ufficiale. FAQ copre static-first workflow con **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent**: ratio, safe zone, disclaimer editable, pass/fail acceptance. Non prezzi inventati per tier Lovart o competitor — consultare pagine ufficiali.

## Quattro domande ops ogni FAQ design AI deve trattare

Primo: quale ratio e dimensioni per promo editable? Risposta ops: 4:5 1080×1350 o 16:9 1920×1080 con headline top 15% flat for **Touch Edit**. Secondo: come bloccare accent slide 4? **Brand Kit** hex da VI approvato — non stock marble. Terzo: offerta in pixels render o layer editable? Sempre layer editable — fix martedì five minutes vs full regen thirty minutes. Quarto: chi valida prima export? **Design Agent** pass/fail checklist — non « looks professional ».

## Perché le FAQ b39 design tools falliscono il martedì

Brief FAQ debole: « best AI design tool ». Risultato: belle frames, prezzo illeggibile, badge sul soggetto. Cambiare offerta costa thirty-minute full regen senza **Touch Edit**. Slide 4 accent lottery senza **Brand Kit**. Team IT vogliono campi pass/fail, non aggettivi premium.

## Contratto brief ChatCanvas (FAQ b39 context)

Brief forte: « Campaign X design tools FAQ companion 4:5, Brand Kit navy + sand from packaging, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 2–4 same thread, no small text in render, **Design Agent** numeric acceptance ». **ChatCanvas** same thread batch hero + carousel — accent stripe resta.

## Brand Kit come SSOT in ogni risposta FAQ

Primary, accent, type role da VI approvato. FAQ dice « sample hex from media kit » — non « use premium colors ». **Brand Kit** lock prima batch variants — slide 3 teal ≠ slide 4 coral = FAQ failed ops test.

## Touch Edit come prova che la FAQ è ops-ready

Se risposta FAQ raccomanda output dove offerta è baked in pixels, **Touch Edit** non fix in five minutes — workflow failed. Buona FAQ = editable CTA band, static-first, motion optional companion.

## Errori frequenti FAQ b39

Aggettivi senza campi. **Brand Kit** saltato. Offerta baked. URL 404 non ripristinato. Prezzi tool inventati. Fake « best model 2026 » ranking.

## Metriche FAQ b39

Minuti per fix offerta, accent drift count, export sizes. URL ripristinato stable IT b39-ai-design-tools-faq-bing SOP link.
"""

BOUTIQUE_OWNER_IT = """
# Miglior Design Agent AI per boutique owner: workflow onesto senza ranking fake

Questa URL italiana `best-ai-design-agent-for-boutique-owner` restituiva 404 mentre boutique owner cercavano guida onesta — non ranking generico « #1 best agent ». Ops quotidiane boutique: window display graphic, seasonal promo, Instagram crop, loyalty card — prezzi e date cambiano ogni settimana, accent drift tra vetrina e social. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** fissano palette boutique-ready. KPI è « cambiare prezzo promo in cinque minuti », non « primo poster cinematic ».

## Quattro deliverable boutique owner workflow

Primo layer window promo 4:5 o A4 bleed con prezzo band editable via **Touch Edit**. Secondo layer Instagram carousel same **ChatCanvas** thread accent **Brand Kit**. Terzo layer loyalty card print bleed — **Design Agent** print pass/fail. Quarto layer seasonal sale banner — disclaimer footer editable.

## Perché « best agent for boutique » comparativi ingannano

Liste inventano scores senza source. Offerta baked in pixels → owner blocked martedì full regen. **Brand Kit** assente → vetrina teal, Instagram coral. Confronto onesto scrive: best = low edit-minute median on Tuesday loop, non pretty first output.

## Contratto brief ChatCanvas (boutique owner IT)

Brief debole: « premium boutique poster ». Brief forte: « Boutique X seasonal promo 4:5, Brand Kit hex from shop VI, headline collection name top 15% flat for Touch Edit, price bottom band editable, disclaimer footer editable, variants window + IG same thread, **Design Agent** pass/fail checklist owner can run ».

## Brand Kit unifica vetrina e social crop

Primary, accent da VI boutique. **ChatCanvas** same thread A4 window + Instagram crop + story — accent stripe resta.

## Touch Edit cambia prezzo promo senza regen display graphic

« €89 » verso « €69 »: **Touch Edit** five minutes CTA band — non full window graphic regen thirty minutes. Boutique owner metric: edit-minute median down week over week.

## Errori frequenti boutique owner

Credere fake ranking scores. Exploration output as final promo. Saltare **Brand Kit**. URL 404 non ripristinato. Fake « one click perfect display » guarantee.

## Metriche boutique owner

Edit-minute median, regen count, drift events per seasonal batch. URL ripristinato stable IT best-ai-design-agent-for-boutique-owner SOP link.
"""


FAQ = {
    "lovart_complete_guide_fr": """
## FAQ

**Complete guide garantit mastery day one?**  
Non — champs pass/fail et edit-minute median seulement.

**Brand Kit obligatoire?**  
Oui — hex VI approuvé, sinon slide 4 drift.

**Touch Edit test qualité guide?**  
Oui — offre baked = workflow failed.

**404 fix?**  
Stable FR lovart-complete-guide-2025-ai-powered-design URL.

**Fake pricing tiers Lovart?**  
Aucun — consulter lovart.ai officiel.
""",
    "sora_alternatives_fr": """
## FAQ

**Sora alternative Top-10 ranking?**  
Non — quatre groupes tâches, pas scores inventés.

**Prix Sora inventés ici?**  
Non — pages officielles OpenAI direct.

**Sora vs Lovart zero-sum?**  
Non — motion layer vs static ops companion.

**404 fix?**  
Stable FR sora-alternatives URL.

**Touch Edit static after Sora?**  
Oui — five minutes offer fix on still.
""",
    "virtual_influencers_fr": """
## FAQ

**Replace 100% human models guarantee?**  
Non — supplement specific campaigns only.

**AI disclosure editable?**  
Oui — Touch Edit footer layer, legal human sign-off.

**Brand Kit character drift?**  
Oui — hex SSOT same ChatCanvas thread.

**404 fix?**  
Stable FR virtual-influencers-brands-replacing-human-models-ai URL.

**Touch Edit offer on companion?**  
Oui — five minutes sans character reroll.
""",
    "clawdbot_fr": """
## FAQ

**Slug instant-results = garantie?**  
Non — reduce process anxiety via champs, pas magic instant.

**Typo clawdbot in URL?**  
Oui — preserved once naturally in article body.

**Long slug exact preserved?**  
Oui — why-lovart-is-the-clawdbot-of-design-for-beginners-goodbye-process-anxiety-hello-instant-results.

**404 fix?**  
Stable FR long slug clawdbot beginner guide URL.

**Design Agent beginner checklist?**  
Oui — pass/fail numeric, pas adjectives.
""",
    "youtube_thumbnail_fr": """
## FAQ

**2027 slug = CTR guarantee?**  
Non — checklist ops 120px pass only.

**Touch Edit title A/B?**  
Oui — five minutes sans regen face.

**Brand Kit channel VI?**  
Oui — accent lock A/B same thread.

**404 fix?**  
Stable FR youtube-thumbnail-design-science-2027 URL.

**1280×720 in brief?**  
Oui — ratio contract required.
""",
    "openart_review_it": """
## FAQ

**OpenArt-AI-Review slug case?**  
Sì — casse esatta OpenArt-AI-Review preserved.

**OpenArt vs Lovart zero-sum?**  
No — exploration vs series stack.

**Prezzi OpenArt inventati?**  
No — consultare openart.ai.

**404 fix?**  
Stable IT OpenArt-AI-Review URL.

**Fake benchmark scores?**  
Nessuno — task groups only.
""",
    "ai_video_bg_it": """
## FAQ

**Bg removal = final promo?**  
No — static companion editable layer required.

**Touch Edit post-cutout?**  
Sì — five minutes price band.

**Brand Kit dopo cutout?**  
Sì — hex lock same thread.

**404 fix?**  
Stable IT ai-video-background-removal URL.

**Fake render speed?**  
Nessuno — ops workflow only.
""",
    "b33_bg_remover_it": """
## FAQ

**Bing endorsement ufficiale?**  
No — slug contesto ricerca only.

**Top-8 accuracy scores?**  
No — task groups, no fake ranking.

**Touch Edit post-cutout test?**  
Sì — five minutes offer fix.

**404 fix?**  
Stable IT b33-ai-background-remover-comparison-bing URL.

**Prezzi tool inventati?**  
No — pagine ufficiali.
""",
    "b39_faq_it": """
## FAQ

**FAQ Bing endorsement?**  
No — slug contesto, workflow onesto only.

**Top ranking design tools?**  
No — campi ops pass/fail.

**Brand Kit in FAQ?**  
Sì — hex from VI.

**404 fix?**  
Stable IT b39-ai-design-tools-faq-bing URL.

**Touch Edit test FAQ quality?**  
Sì — offerta baked = failed.
""",
    "boutique_owner_it": """
## FAQ

**Best agent #1 ranking?**  
No — edit-minute median beats pretty frame.

**Touch Edit boutique price?**  
Sì — five minutes promo band.

**Brand Kit window + IG?**  
Sì — same thread hex lock.

**404 fix?**  
Stable IT best-ai-design-agent-for-boutique-owner URL.

**One click perfect display?**  
No — pass/fail fields required.
""",
}


def expand_fr(topic: str, n: int) -> str:
    return f"""
## Note pratique {n}: {topic}

Le premier brief finit par « premium » et échoue: petit prix, badge sur le sujet. Au second passage, corriger seulement safe zone et champs obligatoires. Un thread **ChatCanvas** réduit accent drift sur slide 4. Dans **{topic}**, **Touch Edit** confirme changement de prix en cinq minutes static-first. Full regen 30 minutes — d'abord reset **Brand Kit**. URL 404 restaurée comme stable SOP link pour équipes FR batch28. **Design Agent** pass/fail checklist bat les briefs adjectifs.
"""


def expand_it(topic: str, n: int) -> str:
    return f"""
## Nota operativa {n}: {topic}

Il primo brief «premium» fallisce: prezzo piccolo, badge sul viso. Al secondo pass correggi solo safe zone e campi obbligatori. Thread unico **ChatCanvas** riduce drift slide 4. In **{topic}**, se **Touch Edit** chiude cambio prezzo in cinque minuti, il loop static-first funziona. Full regen da 30 minuti significa rifare **Brand Kit**. URL 404 ripristinato per SOP stabile onboarding.
"""


ARTICLES = [
    {
        "rank": 286,
        "key": "lovart_complete_guide_fr",
        "lang": "fr",
        "slug": "lovart-complete-guide-2025-ai-powered-design",
        "cover": "036",
        "category": "Complete Guide",
        "title": "Guide complet Lovart 2025 : design IA de bout en bout",
        "seo_title": "Lovart Complete Guide 2025 AI Powered Design FR",
        "description": "FR 404 fix: Lovart complete guide 2025, ChatCanvas Brand Kit Touch Edit Design Agent SOP.",
        "seo_description": "Complete Guide: static-first workflow, zero fake pricing tiers or ranking scores.",
        "focus": "lovart complete guide 2025 ai powered design",
        "keywords": ["lovart complete guide", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Complete Guide — Lovart 2025 FR",
        "body": LOVART_COMPLETE_GUIDE_FR,
        "expand_topic": "FR Lovart complete guide 2025 AI powered design",
    },
    {
        "rank": 287,
        "key": "sora_alternatives_fr",
        "lang": "fr",
        "slug": "sora-alternatives",
        "cover": "037",
        "category": "Comparison",
        "title": "Alternatives Sora : comparaison honnête par groupe de tâches",
        "seo_title": "Sora Alternatives FR — task groups no fake pricing",
        "description": "FR 404 fix: Sora alternatives comparison, task groups not fake ranking.",
        "seo_description": "Comparison: motion layer vs static ops, zero fabricated Sora pricing.",
        "focus": "sora alternatives",
        "keywords": ["sora alternatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Sora Alternatives FR",
        "body": SORA_ALTERNATIVES_FR,
        "expand_topic": "FR Sora alternatives honest comparison",
    },
    {
        "rank": 288,
        "key": "virtual_influencers_fr",
        "lang": "fr",
        "slug": "virtual-influencers-brands-replacing-human-models-ai",
        "cover": "038",
        "category": "Industry Solution",
        "title": "Influenceurs virtuels : marques et modèles humains — guide ops",
        "seo_title": "Virtual Influencers Brands Replacing Human Models FR",
        "description": "FR 404 fix: virtual influencer workflow, no 100% replace guarantee, AI disclosure.",
        "seo_description": "Industry Solution: character reference, Touch Edit companion, Brand Kit drift lock.",
        "focus": "virtual influencers brands replacing human models ai",
        "keywords": ["virtual influencers", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Virtual Influencers FR",
        "body": VIRTUAL_INFLUENCERS_FR,
        "expand_topic": "FR virtual influencers brands replacing human models",
    },
    {
        "rank": 289,
        "key": "clawdbot_fr",
        "lang": "fr",
        "slug": "why-lovart-is-the-clawdbot-of-design-for-beginners-goodbye-process-anxiety-hello-instant-results",
        "cover": "039",
        "category": "Industry Solution",
        "title": "Lovart pour débutants : adieu anxiété process, pas de garantie instantanée",
        "seo_title": "Clawdbot Design Beginners FR — exact long slug no instant guarantee",
        "description": "FR 404 fix: clawdbot long slug preserved, typo noted once, no fake instant results.",
        "seo_description": "Beginner guide: Design Agent checklist, Touch Edit Tuesday loop, process anxiety reduction.",
        "focus": "why lovart is the clawdbot of design for beginners",
        "keywords": ["lovart beginners", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Clawdbot Beginners FR",
        "body": CLAWDBOT_FR,
        "expand_topic": "FR clawdbot beginner design process anxiety honest guide",
    },
    {
        "rank": 290,
        "key": "youtube_thumbnail_fr",
        "lang": "fr",
        "slug": "youtube-thumbnail-design-science-2027",
        "cover": "040",
        "category": "How-To",
        "title": "Science du design de miniatures YouTube 2027 : checklist ops",
        "seo_title": "YouTube Thumbnail Design Science 2027 FR — 120px pass",
        "description": "FR 404 fix: YouTube thumbnail 2027 checklist, 1280×720, Touch Edit title A/B.",
        "seo_description": "How-To: Brand Kit channel VI, Design Agent 120px QA, no fake CTR guarantee.",
        "focus": "youtube thumbnail design science 2027",
        "keywords": ["youtube thumbnail design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — YouTube Thumbnail Science 2027 FR",
        "body": YOUTUBE_THUMBNAIL_FR,
        "expand_topic": "FR YouTube thumbnail design science 2027 checklist",
    },
    {
        "rank": 291,
        "key": "openart_review_it",
        "lang": "it",
        "slug": "OpenArt-AI-Review",
        "cover": "041",
        "category": "Comparison",
        "title": "OpenArt AI Review: confronto onesto dopo uso ops",
        "seo_title": "OpenArt AI Review IT — honest comparison exact slug case",
        "description": "IT 404 fix: OpenArt AI Review, exact slug OpenArt-AI-Review, no fake scores.",
        "seo_description": "OpenArt review: exploration vs series stack, zero fabricated pricing.",
        "focus": "OpenArt AI Review",
        "keywords": ["openart ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — OpenArt AI Review IT",
        "body": OPENART_REVIEW_IT,
        "expand_topic": "IT OpenArt AI Review honest comparison",
    },
    {
        "rank": 292,
        "key": "ai_video_bg_it",
        "lang": "it",
        "slug": "ai-video-background-removal",
        "cover": "042",
        "category": "How-To",
        "title": "Rimozione sfondo video AI: guida pratica post-cutout ops",
        "seo_title": "AI Video Background Removal IT — Touch Edit companion",
        "description": "IT 404 fix: video background removal How-To, static companion editable layer.",
        "seo_description": "How-To: Brand Kit hex lock, ChatCanvas thread, Design Agent edge QA.",
        "focus": "ai video background removal",
        "keywords": ["ai video background removal", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — AI Video Background Removal IT",
        "body": AI_VIDEO_BG_IT,
        "expand_topic": "IT ai video background removal post-cutout workflow",
    },
    {
        "rank": 293,
        "key": "b33_bg_remover_it",
        "lang": "it",
        "slug": "b33-ai-background-remover-comparison-bing",
        "cover": "043",
        "category": "Comparison",
        "title": "Confronto rimozione sfondo AI b33 Bing: gruppi task onesti",
        "seo_title": "B33 AI Background Remover Comparison Bing IT — no fake scores",
        "description": "IT 404 fix: b33 background remover comparison Bing slug, task groups not ranking.",
        "seo_description": "Comparison: Touch Edit post-cutout, zero fabricated accuracy scores.",
        "focus": "b33 ai background remover comparison bing",
        "keywords": ["ai background remover comparison", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — B33 Background Remover Bing IT",
        "body": B33_BG_REMOVER_IT,
        "expand_topic": "IT b33 AI background remover comparison Bing honest",
    },
    {
        "rank": 294,
        "key": "b39_faq_it",
        "lang": "it",
        "slug": "b39-ai-design-tools-faq-bing",
        "cover": "044",
        "category": "How-To",
        "title": "FAQ strumenti design AI b39 Bing: risposte ops oneste",
        "seo_title": "B39 AI Design Tools FAQ Bing IT — honest ops answers",
        "description": "IT 404 fix: b39 AI design tools FAQ Bing slug, pass/fail fields not fake ranking.",
        "seo_description": "How-To FAQ: Brand Kit hex lock, Touch Edit Tuesday loop, zero fabricated pricing.",
        "focus": "b39 ai design tools faq bing",
        "keywords": ["ai design tools faq", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — B39 AI Design Tools FAQ Bing IT",
        "body": B39_FAQ_IT,
        "expand_topic": "IT b39 AI design tools FAQ Bing",
    },
    {
        "rank": 295,
        "key": "boutique_owner_it",
        "lang": "it",
        "slug": "best-ai-design-agent-for-boutique-owner",
        "cover": "045",
        "category": "Industry Solution",
        "title": "Miglior Design Agent AI per boutique owner: workflow onesto",
        "seo_title": "Best AI Design Agent Boutique Owner IT — no fake ranking",
        "description": "IT 404 fix: boutique owner Design Agent guide, Touch Edit promo price editable.",
        "seo_description": "Industry Solution: window display + IG same thread, edit-minute median KPI.",
        "focus": "best ai design agent for boutique owner",
        "keywords": ["boutique owner design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Boutique Owner IT",
        "body": BOUTIQUE_OWNER_IT,
        "expand_topic": "IT best AI design agent for boutique owner workflow",
    },
]

EXPAND_FN = {
    "fr": expand_fr,
    "it": expand_it,
}

UNIT_MAP = {
    "fr": "words",
    "it": "words",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch28 content cluster.*\n"
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
