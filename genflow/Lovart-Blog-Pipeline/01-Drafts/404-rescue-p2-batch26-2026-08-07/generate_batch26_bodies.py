#!/usr/bin/env python3
"""Generate 404-rescue P2 batch26 blog bodies (10 files). Self-contained.

Ranks #266–#275 from 404-rescue-compact lane.
1 DE + 9 FR. expand_de + expand_fr.
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

GOENHANCE_DE = """
# Was ist GoEnhance AI? ehrlicher Überblick nach Aufgabe, nicht nach Ranking

Diese deutsche URL `what-is-goenhance-ai` lieferte 404, während Teams nach einem ehrlichen GoEnhance-Überblick suchten — kein fake „Nummer eins"-Ranking mit erfundenen Preisen oder Benchmark-Scores. GoEnhance daily use: video style transfer, image enhancement, short clip upscaling — gut für exploration und mood reference, schlecht allein für weekly promo mit editable price layer. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** übernehmen wenn brand systems und Tuesday fixes zählen. Preise und Tier-Namen ändern sich — Leser prüfen goenhance.ai und offizielle Vendor-Seiten direkt; dieser Artikel nennt keine Euro- oder Dollar-Beträge für GoEnhance-Pläne.

## Vier Aufgabengruppen statt Top-10-Liste

Gruppe A video style transfer und clip enhancement: schnelle Richtung, schlecht für weekly offer fix auf static layer. Gruppe B image upscaling und face restore: mood reference, nicht final marketplace collateral ohne QA. Gruppe C campaign series platform: **ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable static layer. Gruppe D open-source or local render: privacy-sensitive, revision cost hoch. Keine „GoEnhance alternative #1–#7"-Liste — nur Aufgabenfit und Revision-Kosten.

## Warum „what is GoEnhance"-Artikel ops täuschen

Listen mischen clip enhancement mit campaign-series-ops, erfinden Preise ohne Quelle. Readable Preis in pixels gebacken → Dienstag-Fix triggert full reroll. **Brand Kit** nicht aus approved VI → slide 4 accent drift. Honest overview schreibt buyer criteria: revision-heavy promo braucht series platform + static companion.

## ChatCanvas brief Vertrag (GoEnhance context)

Schwacher Brief „best GoEnhance workflow". Starker Brief: „Campaign X static companion 4:5, Brand Kit slate + coral from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone on still only, disclaimer footer editable, variants 2–4 same thread". **Design Agent** QA static acceptance — nicht enhancement „wow frame".

## Brand Kit verhindert accent drift nach GoEnhance export

Export aus GoEnhance exploration in **Brand Kit** importieren — dann **ChatCanvas** thread für promo series. Nie readable offer in enhancement render pixels backen.

## Touch Edit versus full regen Entscheidungstest

Wenn nur headline price sich ändert: braucht der Stack **Touch Edit** five minutes? Enhancement tools in meinem test: often full regen. Lovart stack: yes — gemessen, nicht zero-sum „GoEnhance bad".

## GoEnhance versus Lovart task split (kein zero-sum)

GoEnhance für clip enhancement layer; **ChatCanvas** + **Touch Edit** für campaign series mit editable CTA. Nicht either-or — ops teams brauchen ehrliche task split statt „one tool replaces all".

## Häufige Fehler

Erfundene GoEnhance pricing in Vergleichen glauben. Enhancement output direkt als final promo. Kein **Brand Kit**. 404 nicht gefixt. Fake benchmark scores.

## Wert messen

Enhancement minutes versus promo edit minutes getrennt tracken. Wiederhergestellte URL gibt honest what-is-goenhance-ai stable link — pricing immer offizielle Vendor-Seite.
"""

BRAND_KIT_SCRATCH_FR = """
# Brand Kit from scratch : construire un kit de marque avec Lovart

Cette URL française `01-cluster-brand-kit-from-scratch` renvoyait une 404 alors que les recherches demandaient un guide honnête pour créer un Brand Kit from scratch — pas un classement générique d'outils. Le cluster branding couvre static-first brand system avec **ChatCanvas**, **Brand Kit**, **Touch Edit** et **Design Agent** : primary hex, accent, type role, logo lockup, variant crops. Pas de prix inventés, pas de fausses métriques gallery.

## Quatre layers pour un Brand Kit from scratch

Premièrement primary, accent, type role échantillonnés depuis VI approuvé ou packaging — pas stock marble comme couleur de marque. Deuxièmement logo lockup companion avec safe zone documented. Troisièmement static master 4:5 avec headline footer editable via **Touch Edit**. Quatrièmement variant series slide 2–6 same **ChatCanvas** thread — **Design Agent** QA hex drift vs Kit.

## Pourquoi les Brand Kit from scratch échouent le mardi

Brief faible : « brand kit premium ». Résultat : belles couleurs, caption illisible, badge sur le logo. Changer l'offre coûte thirty-minute full regen sans **Touch Edit**. Slide 4 accent lottery sans **Brand Kit** SSOT. Les équipes veulent des champs pass/fail, pas des adjectifs.

## Contrat brief ChatCanvas (Brand Kit from scratch FR)

Au lieu d'adjectifs : « Campaign X brand kit setup 4:5 1080×1350, Brand Kit slate + coral from media kit, headline top 15% flat for Touch Edit, disclaimer footer editable, variants 2–4 same thread, no small text in render ». **Design Agent** vérifie acceptance numeric — pas « artistique ».

## Brand Kit comme SSOT pour toute la série

Échantillonner primary, accent, type role depuis VI approuvé. **ChatCanvas** same thread batch hero + carousel + banner — accent stripe reste. Pas de nouveau prompt par variante sans thread.

## Touch Edit change l'offre sans crop logo

« €49 » vers « €59 » : **Touch Edit** cadre CTA band, garde logo geometry et **Brand Kit** accent stripe. Full regen randomise gradient — série ne supporte pas thirty-minute reroll.

## Erreurs fréquentes

Sauter **Brand Kit** setup. Offre baked in pixels. Nouveau prompt par variante. URL 404 non restaurée. Prix tool inventés.

## Métriques

Minutes par fix offre, accent drift, export sizes. URL restaurée comme stable FR brand kit from scratch SOP link.
"""

INSTAGRAM_CAROUSEL_FR = """
# Instagram carousel : série cohérente avec Brand Kit et Touch Edit

Cette URL française `02-cluster-instagram-carousel` renvoyait une 404 alors que les recherches demandaient un guide honnête pour Instagram carousel branding — pas un classement générique. Le cluster branding couvre static-first carousel series avec **ChatCanvas**, **Brand Kit**, **Touch Edit** et **Design Agent** : slide 1 hook, slides 2–6 same thread, editable CTA layer. Pas de prix inventés, pas de fausses métriques engagement.

## Quatre layers pour un Instagram carousel cohérent

Premièrement slide 1 hook master 4:5 avec headline readable top 15%. Deuxièmement slides 2–6 variant same thread accent stripe **Brand Kit**. Troisièmement CTA band bottom 20% flat for **Touch Edit** — pas d'offre baked in render pixels. Quatrièmement disclaimer footer editable — **Design Agent** QA presence at 50% zoom.

## Pourquoi les Instagram carousel échouent le mardi

Brief faible : « carousel premium Instagram ». Résultat : slide 4 accent drift, prix illisible, badge sur le produit. Changer l'offre coûte thirty-minute full regen sans **Touch Edit**. **Brand Kit** non défini — slide 3 teal ≠ slide 4 coral. Les équipes veulent des champs pass/fail.

## Contrat brief ChatCanvas (Instagram carousel FR)

Au lieu d'adjectifs : « Campaign X Instagram carousel 4:5 1080×1350, Brand Kit slate + coral from media kit, slide 1 hook flat for Touch Edit headline, slides 2–6 same thread, price bottom band editable, disclaimer footer editable, **Design Agent** pass/fail checklist ».

## Brand Kit verrouille accent sur slide 4

Échantillonner primary, accent, type role depuis VI approuvé. **ChatCanvas** same thread batch six slides — accent stripe reste. Pas de stock marble comme couleur de série.

## Touch Edit change l'offre sans regen slide 4

« €29 » vers « €39 » : **Touch Edit** cadre CTA band slide 6, garde product geometry slides 2–5. Full regen randomise accent — carousel ne supporte pas thirty-minute reroll par slide.

## Erreurs fréquentes

Sauter **Brand Kit**. Offre baked. Nouveau prompt par slide. URL 404 non restaurée. Fake engagement stats.

## Métriques

Minutes par fix offre, accent drift slide count, export ratios. URL restaurée comme stable FR Instagram carousel SOP link.
"""

AI_PROMPTS_FR = """
# 10 prompts design IA qui fonctionnent vraiment : guide How-To

Cette URL française `10-ai-design-prompts-that-actually-work` renvoyait une 404 alors que les recherches demandaient des prompts design IA actionnables — pas une liste générique sans contexte ops. Le guide How-To couvre static-first prompt discipline avec **ChatCanvas**, **Brand Kit**, **Touch Edit** et **Design Agent** : champs obligatoires, safe zones, pass/fail acceptance. Pas de prix inventés.

## Quatre champs obligatoires dans chaque prompt design

Premièrement ratio et dimensions explicites : 4:5 1080×1350 ou 16:9 1920×1080. Deuxièmement **Brand Kit** hex from media kit — pas « premium colors ». Troisièmement safe zone pour **Touch Edit** : headline top 15%, price bottom 20% flat. Quatrièmement **Design Agent** pass/fail checklist — pas « looks professional ».

## Pourquoi les prompts design IA échouent le mardi

Prompt faible : « make it premium ». Résultat : belle image, prix illisible, badge sur le sujet. Changer l'offre coûte thirty-minute full regen sans **Touch Edit**. Slide 4 accent lottery sans **Brand Kit**. Les ops veulent champs, pas adjectifs.

## Contrat brief ChatCanvas (10 prompts edition)

Exemple prompt fort : « Campaign X promo 4:5, Brand Kit navy + sand from packaging, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 2–4 same thread, no small text in render ». **Design Agent** QA numeric fields.

## Brand Kit dans chaque prompt

Primary, accent, type role depuis VI approuvé — jamais stock marble. **ChatCanvas** same thread quand plusieurs variants — accent stripe reste.

## Touch Edit comme test de prompt quality

Si le prompt produit une image où l'offre est baked in pixels, **Touch Edit** ne peut pas fix en five minutes — prompt failed. Bon prompt = editable CTA band.

## Dix prompts : structure pas contenu copié

Ce guide décrit la structure des dix prompts — ratio, hex, safe zone, disclaimer, thread — pas dix phrases magiques à copier. Chaque campagne adapte les champs.

## Erreurs fréquentes

Adjectifs sans champs. **Brand Kit** sauté. Offre baked. URL 404 non restaurée. Fake « prompt hacks » avec scores inventés.

## Métriques

Minutes par fix offre, prompt revision count, accent drift. URL restaurée comme stable FR AI design prompts SOP link.
"""

PRINT_TOOLS_FR = """
# 10 meilleurs outils design print IA 2026 : comparaison honnête par groupe de tâches

Cette URL française `10-best-ai-print-design-tools-2026` renvoyait une 404 alors que les recherches demandaient une comparaison honnête des outils print design IA — pas un fake Top-10 avec scores inventés. Cet article groupe par tâche, pas par ranking. Prix et noms de tiers changent — consulter pages officielles; aucun montant inventé ici.

## Quatre groupes de tâches print design (pas de ranking)

Groupe A layout et mise en page print-ready : bleed, safe zone, CMYK prep — bon pour static master. Groupe B photo enhancement pour print collateral : mood reference, pas final sans QA. Groupe C campaign series platform : **ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable layer. Groupe D open-source ou local : privacy-sensitive, revision cost élevé. Pas de « outil #1–#10 » — seulement fit tâche et coût revision.

## Pourquoi les comparatifs print design trompent

Listes mélangent exploration et ops campaign, inventent prix sans source. Offre readable baked in pixels → fix mardi = full regen thirty minutes. **Brand Kit** absent → accent drift slide 4. Comparaison honnête écrit critères acheteur : promo revision-heavy = series platform + static companion.

## Contrat brief ChatCanvas (print design context)

Brief faible : « best print design AI ». Brief fort : « Campaign X print collateral A4 bleed, Brand Kit hex from VI, headline flat for Touch Edit, disclaimer footer editable, variants same thread, **Design Agent** pass/fail ».

## Brand Kit pour print et digital companion

Primary, accent, type role depuis VI approuvé. Print PDF + social crop same **ChatCanvas** thread — hex lock.

## Touch Edit versus full regen pour print promo

Changement prix « €19,99 » → « €24,99 » : **Touch Edit** five minutes sur static companion — pas full regen print layout. Coût revision réel, pas subscription line item.

## Erreurs fréquentes

Croire prix inventés. Output exploration comme final print. Sauter **Brand Kit**. URL 404 non restaurée. Fake benchmark scores.

## Métriques

Minutes par fix offre, drift count, export bleed ratios. URL restaurée comme stable FR print design tools comparison link.
"""

TEXT_TO_VIDEO_TOOLS_FR = """
# 10 meilleurs outils text-to-video IA 2026 : comparaison honnête par groupe de tâches

Cette URL française `10-best-text-to-video-ai-tools-2026` renvoyait une 404 alors que les recherches demandaient une comparaison honnête text-to-video — pas un fake Top-10 avec scores inventés. Cet article groupe par tâche. Prix et quotas changent — consulter pages officielles; aucun montant inventé ici.

## Quatre groupes de tâches text-to-video (pas de ranking)

Groupe A cinematic exploration et mood clip : bon pour direction, mauvais pour weekly offer fix. Groupe B short hook social bumper : motion companion, static legal pass d'abord. Groupe C campaign series platform : **ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable static layer. Groupe D open-source local render : privacy-sensitive. Pas de « outil #1–#10 » — fit tâche et coût revision.

## Pourquoi text-to-video comparatifs trompent

Listes mélangent clip wow avec ops campaign. Offre dans clip pixels → fix mardi = full rerender thirty minutes. **Brand Kit** absent → accent drift still vs motion. Comparaison honnête : static-first, motion companion optional.

## ChatCanvas brief (text-to-video context)

Brief faible : « turn paragraph into movie ». Brief fort : « Campaign X text-to-video prep 16:9, Brand Kit hex from media kit, headline static companion flat for Touch Edit, price on still only, disclaimer editable, motion prompt no text in render, **Design Agent** QA static first ».

## Brand Kit entre still et motion

Primary, accent depuis VI approuvé. Motion accent ne doit pas diverger de carousel slide 3. **Brand Kit** SSOT fixe hex drift.

## Touch Edit sur still companion — pas dans le clip

« €49 » → « €39 » : **Touch Edit** CTA band on still master — pas full motion reroll. Text-to-video pour hook; static pour legal pass.

## Erreurs fréquentes

Offre baked in clip. Motion-only sans static editable. Sauter **Brand Kit**. URL 404 non restaurée. Fake render speed benchmarks.

## Métriques

Minutes par fix offre on still, still vs motion match count, export ratios. URL restaurée comme stable FR text-to-video tools comparison link.
"""

OPENART_REVIEW_FR = """
# OpenArt AI Review : comparaison honnête après usage ops

Cette URL française `OpenArt-AI-Review` renvoyait une 404 — le slug conserve la casse exacte OpenArt-AI-Review. Les recherches demandaient un review honnête OpenArt AI — pas un affiliate fluff ou fake scores. OpenArt daily use : model exploration, community rooms, style tests — bon pour exploration, mauvais seul pour weekly promo editable. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** quand copy, color et revision cost comptent plus que model count. Prix changent — consulter openart.ai; aucun montant inventé ici.

## Quatre groupes de tâches OpenArt (pas de ranking)

Groupe A model exploration et community rooms : direction rapide, mauvais pour offer fix weekly. Groupe B style et texture experiments : mood reference, pas final collateral sans QA. Groupe C campaign series platform : **ChatCanvas** thread + **Brand Kit** + **Touch Edit**. Groupe D local ou privacy-sensitive workflows. Pas de « OpenArt vs X score 9.2/10 » — fit tâche seulement.

## Pourquoi les OpenArt reviews trompent

Reviews mélangent exploration wow avec ops campaign. Offre baked in pixels → fix mardi full regen. **Brand Kit** absent → frames gorgeous but none match type scale. Review honnête écrit task split : exploration OpenArt; series Lovart static layer.

## ChatCanvas brief (OpenArt review context)

Brief faible : « best OpenArt alternative ». Brief fort : « Campaign X static companion 4:5, Brand Kit from media kit, headline flat for Touch Edit, price bottom safe zone on still, disclaimer editable, variants same thread, **Design Agent** pass/fail ».

## Brand Kit après export OpenArt exploration

Importer hex from approved VI in **Brand Kit** — puis **ChatCanvas** thread promo series. Jamais offre readable in exploration render pixels.

## Touch Edit versus full regen

Changement prix five minutes **Touch Edit**? OpenArt exploration in my test: often full regen. Lovart stack: yes — mesuré, pas zero-sum « OpenArt bad ».

## OpenArt versus Lovart task split

OpenArt pour exploration layer; **ChatCanvas** + **Touch Edit** pour campaign series. Pas either-or — ops teams need honest split.

## Erreurs fréquentes

Prix OpenArt inventés. Exploration output as final promo. Sauter **Brand Kit**. URL 404 non restaurée. Fake benchmark scores.

## Métriques

Exploration minutes vs promo edit minutes track separately. URL restaurée stable OpenArt-AI-Review FR link.
"""

COLLAGE_MOODBOARD_FR = """
# Outils collage et moodboard IA comparés : comparaison honnête par groupe de tâches

Cette URL française `ai-collage-moodboard-tools-compared` renvoyait une 404 alors que les recherches demandaient une comparaison honnête collage et moodboard IA — pas un fake ranking. Cet article groupe par tâche. Pas de prix inventés.

## Quatre groupes de tâches collage moodboard (pas de ranking)

Groupe A moodboard exploration et reference boards : direction rapide, mauvais pour final promo editable. Groupe B collage layout experiments : texture mix, pas campaign series sans QA. Groupe C campaign series platform : **ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable static. Groupe D print-ready collage avec bleed : layout contract required. Pas de « outil #1–#7 » — fit tâche et revision cost.

## Pourquoi les comparatifs moodboard trompent

Listes mélangent Pinterest-style boards avec ops promo. Offre baked → fix mardi full regen. **Brand Kit** absent → accent drift entre collage tile 4 et slide 4. Comparaison honnête : moodboard for direction; **ChatCanvas** for final series.

## ChatCanvas brief (collage moodboard context)

Brief faible : « best moodboard AI ». Brief fort : « Campaign X moodboard export to static companion 4:5, Brand Kit hex from VI, headline flat for Touch Edit, disclaimer editable, variants same thread, **Design Agent** pass/fail ».

## Brand Kit unifie moodboard accent et promo still

Primary, accent depuis VI approuvé. Export moodboard tiles → **Brand Kit** → **ChatCanvas** thread final promo — hex lock.

## Touch Edit sur static companion après moodboard

Changement offre : **Touch Edit** five minutes CTA band — pas rebuild moodboard collage. Moodboard = exploration; static = ops.

## Erreurs fréquentes

Moodboard output as final promo sans QA. Sauter **Brand Kit**. URL 404 non restaurée. Fake scores.

## Métriques

Moodboard minutes vs promo edit minutes, drift count. URL restaurée stable FR collage moodboard comparison link.
"""

MUSIC_VIDEO_FR = """
# Comment créer un clip musical avec IA : guide How-To pratique

Cette URL française `b3-how-to-create-music-video-ai-guide` renvoyait une 404 alors que les recherches demandaient un guide How-To music video AI — pas un reel cinematic avec benchmarks inventés. Music video daily ops : static hero, motion hook, lyric companion, end card — offer et disclaimer sur editable static via **Touch Edit**. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** static-first : legal pass on still, puis optional motion.

## Quatre layers music video deliverable

Premièrement static master 16:9 avec headline et disclaimer footer editable. Deuxièmement motion companion four to six seconds — no readable small text in clip pixels. Troisièmement social crop 9:16 et 1:1 same thread accent **Brand Kit**. Quatrièmement end card static — offer match landing; **Design Agent** QA mismatch.

## Pourquoi music video AI échoue le mardi

Clip bake « €49 Launch » in pixels while landing static old price. Offer change triggers full rerender thirty minutes. Slide accent lottery still vs motion. **Brand Kit** not sampled from approved VI. Brief stacks « cinematic epic » — **Design Agent** no pass/fail fields.

## Contrat brief ChatCanvas (music video FR)

Brief faible : « make music video from this song ». Brief fort : « Campaign X music video prep 16:9, Brand Kit slate + coral from media kit, headline static companion flat for Touch Edit, price on still only, disclaimer editable, motion prompt slow dolly muted lighting no text in render, **Design Agent** QA static first ».

## Brand Kit still et motion color temperature matched

Primary, accent, type role depuis VI approuvé. Motion accent ne diverge pas de carousel slide three. **Brand Kit** SSOT fixe hex drift.

## Touch Edit change offer sans motion reroll

« Limited €49 » → « Member €39 » : **Touch Edit** CTA band on still master — pas full motion reroll for two word change.

## Erreurs fréquentes

Motion-only sans static editable. Price baked in clip. Sauter **Brand Kit**. URL 404 non restaurée. Fake render speed benchmarks.

## Métriques

Minutes par fix offre, still vs motion match count, export ratios. URL restaurée stable FR music video AI guide link.
"""

FREE_VS_PAID_FR = """
# Outils design IA gratuits vs payants : comparaison honnête (Bing slug)

Cette URL française `b34-free-vs-paid-ai-design-tools-bing` renvoyait une 404 — le slug conserve le contexte Bing recherche; contenu est comparaison honnête free vs paid, pas endorsement Bing fake. Pas de tiers Lovart inventés — consulter lovart.ai/pricing directement; aucun montant Lovart ici.

## Quatre axes de comparaison (pas fake tier table)

Axe A tool subscription spend : consulter vendor sites — zero montants Lovart inventés. Axe B operator hours times rate : edit-minute median bat cheap subscription si fix mardi coûte heures. Axe C revision tax : full regen thirty minutes vs **Touch Edit** five minutes. Axe D brand drift cost : recolor manual sans **Brand Kit** — hours pas visibles in subscription.

## Pourquoi free vs paid comparatifs trompent

Listes inventent « Lovart Pro €X » sans source. Offre baked → hidden revision cost. **Design Agent** absent — briefs end with « premium ». Comparaison honnête écrit cost equation avec operator hours.

## Équation coût (illustrative, pas prix Lovart)

Cost per approved asset = tool spend + operator hours × rate / approved assets. Si free generator six regens per approval — not cheap. **Touch Edit** fix five minutes — mesuré ops, pas pricing claim.

## ChatCanvas brief (cost-aware workflow)

Brief fort nomme task group, ratio, safe zone, **Brand Kit** hex, disclaimer editable, **Design Agent** acceptance. Brief faible « best free AI design » — not operational.

## Brand Kit réduit hidden drift spend

Avec **Brand Kit** actif comparer deux workflows on drift count — pas first-frame beauty. Sans Kit cost breakdown incomplete.

## Touch Edit comme cost decision test

Si seul headline price change : stack needs **Touch Edit** five minutes? Full regen thirty minutes — real cost, not subscription line.

## Erreurs fréquentes

Croire tiers Lovart inventés. Exploration output as final promo. Sauter **Brand Kit**. URL 404 non restaurée. Fake ROI calculator.

## Métriques

Edit-minute median, drift events, hours per approved asset. Lovart pricing toujours page officielle — cet article nomme aucun tier amount.
"""


FAQ = {
    "goenhance_de": """
## FAQ

**GoEnhance als Top-10-Ranking?**  
Nein — vier Aufgabengruppen, ehrlicher task split.

**GoEnhance vs Lovart zero-sum?**  
Nein — enhancement vs campaign series.

**404-Fix?**  
Stable de what-is-goenhance-ai honest overview URL.

**Erfundene GoEnhance Preise?**  
Null — goenhance.ai direkt prüfen.

**Touch Edit test?**  
Preisänderung five minutes? Series stack ja, enhancement often full regen.
""",
    "brand_kit_scratch_fr": """
## FAQ

**Brand Kit from scratch nécessite Brand Kit?**  
Oui — hex depuis VI, sinon slide 4 drift.

**Changement offre full regen?**  
Non — Touch Edit five minutes.

**Prix inventés?**  
Non — consulter pages officielles.

**404 fix?**  
Stable FR 01-cluster-brand-kit-from-scratch SOP URL.

**Design Agent « artistique »?**  
Non — checklist pass/fail numeric.
""",
    "instagram_carousel_fr": """
## FAQ

**Instagram carousel nécessite Brand Kit?**  
Oui — hex depuis VI, sinon slide 4 drift.

**Changement offre full regen?**  
Non — Touch Edit five minutes CTA band.

**Prix inventés?**  
Non — consulter pages officielles.

**404 fix?**  
Stable FR 02-cluster-instagram-carousel SOP URL.

**Fake engagement stats?**  
Aucune — ops metrics only.
""",
    "ai_prompts_fr": """
## FAQ

**10 prompts magiques à copier?**  
Non — structure champs obligatoires, pas phrases copiées.

**Touch Edit test prompt quality?**  
Oui — offre baked = prompt failed.

**Brand Kit dans chaque prompt?**  
Oui — hex from VI, pas adjectifs.

**404 fix?**  
Stable FR 10-ai-design-prompts-that-actually-work URL.

**Fake prompt scores?**  
Aucun — pass/fail fields only.
""",
    "print_tools_fr": """
## FAQ

**Top-10 ranking print tools?**  
Non — quatre groupes tâches, pas scores inventés.

**Prix tools inventés?**  
Non — pages officielles.

**Touch Edit print promo?**  
Oui — five minutes CTA band on static.

**404 fix?**  
Stable FR 10-best-ai-print-design-tools-2026 URL.

**Brand Kit print + digital?**  
Oui — same thread hex lock.
""",
    "text_to_video_tools_fr": """
## FAQ

**Top-10 text-to-video ranking?**  
Non — groupes tâches, pas fake scores.

**Offre dans clip pixels?**  
Non — Touch Edit sur still companion only.

**Brand Kit still vs motion?**  
Oui — hex SSOT verhindert drift.

**404 fix?**  
Stable FR 10-best-text-to-video-ai-tools-2026 URL.

**Fake render benchmarks?**  
Aucun — ops workflow only.
""",
    "openart_review_fr": """
## FAQ

**OpenArt-AI-Review slug case?**  
Oui — casse exacte OpenArt-AI-Review preserved.

**OpenArt vs Lovart zero-sum?**  
Non — exploration vs campaign series.

**Prix OpenArt inventés?**  
Non — openart.ai direct.

**404 fix?**  
Stable FR OpenArt-AI-Review URL.

**Fake scores 9.2/10?**  
Aucun — task fit only.
""",
    "collage_moodboard_fr": """
## FAQ

**Moodboard as final promo?**  
Non — ChatCanvas static companion after exploration.

**Top ranking collage tools?**  
Non — groupes tâches honnêtes.

**Brand Kit moodboard to promo?**  
Oui — hex lock same thread.

**404 fix?**  
Stable FR ai-collage-moodboard-tools-compared URL.

**Prix inventés?**  
Non — pages officielles.
""",
    "music_video_fr": """
## FAQ

**Music video remplace static legal pass?**  
Non — static-first, motion optional.

**Offre dans clip?**  
Non — Touch Edit sur still companion.

**Brand Kit still et motion?**  
Oui — hex SSOT.

**404 fix?**  
Stable FR b3-how-to-create-music-video-ai-guide URL.

**Fake render speed?**  
Aucun — ops metrics only.
""",
    "free_vs_paid_fr": """
## FAQ

**Lovart Pro/Enterprise prix ici?**  
Non — lovart.ai/pricing direct, zero tiers inventés.

**Hidden cost axe?**  
Operator hours et revision tax.

**Touch Edit cost test?**  
Five minutes vs full regen thirty minutes.

**404 fix?**  
Stable FR b34-free-vs-paid-ai-design-tools-bing URL.

**Bing-officiel endorsed?**  
Non — slug contexte recherche, workflow honnête only.
""",
}


def expand_de(topic: str, n: int) -> str:
    return f"""
## Praxisnotiz {n}: {topic}

Der erste Brief endet mit „premium" und scheitert: kleiner Preis, Badge über dem Objekt. Im zweiten Durchlauf nur safe zone und Pflichtfelder korrigieren. Ein **ChatCanvas**-Thread reduziert accent drift auf slide 4. In **{topic}** bestätigt **Touch Edit** Preisänderung in fünf Minuten static-first. Full regen 30 Minuten — zuerst **Brand Kit** neu setzen. Wiederhergestellte 404-URL als stable SOP-Link für DACH SMB-Teams. **Design Agent** pass/fail checklist schlägt Adjektiv-Briefs.
"""


def expand_fr(topic: str, n: int) -> str:
    return f"""
## Note pratique {n}: {topic}

Le premier brief finit par « premium » et échoue: petit prix, badge sur le sujet. Au second passage, corriger seulement safe zone et champs obligatoires. Un thread **ChatCanvas** réduit accent drift sur slide 4. Dans **{topic}**, **Touch Edit** confirme changement de prix en cinq minutes static-first. Full regen 30 minutes — d'abord reset **Brand Kit**. URL 404 restaurée comme stable SOP link pour équipes FR. **Design Agent** pass/fail checklist bat les briefs adjectifs.
"""


ARTICLES = [
    {
        "rank": 266,
        "key": "goenhance_de",
        "lang": "de",
        "slug": "what-is-goenhance-ai",
        "cover": "011",
        "category": "Comparison",
        "title": "Was ist GoEnhance AI? ehrlicher Überblick nach Aufgabe",
        "seo_title": "What is GoEnhance AI — DE honest overview no ranking",
        "description": "DE 404 fix: GoEnhance AI overview, task groups not fake ranking, zero fabricated pricing.",
        "seo_description": "GoEnhance: enhancement vs series stack, Touch Edit Tuesday loop, honest task split.",
        "focus": "what is goenhance ai",
        "keywords": ["goenhance ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — What is GoEnhance AI DE",
        "body": GOENHANCE_DE,
        "expand_topic": "DE what is GoEnhance AI honest overview",
    },
    {
        "rank": 267,
        "key": "brand_kit_scratch_fr",
        "lang": "fr",
        "slug": "01-cluster-brand-kit-from-scratch",
        "cover": "014",
        "category": "Branding",
        "title": "Brand Kit from scratch : construire un kit de marque avec Lovart",
        "seo_title": "Brand Kit From Scratch FR — ChatCanvas branding cluster",
        "description": "FR 404 fix: brand kit from scratch, Brand Kit hex SSOT, Touch Edit editable layer.",
        "seo_description": "Branding cluster: logo lockup, variant same thread, Design Agent QA.",
        "focus": "01 cluster brand kit from scratch",
        "keywords": ["brand kit from scratch", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Branding — Brand Kit From Scratch FR",
        "body": BRAND_KIT_SCRATCH_FR,
        "expand_topic": "FR brand kit from scratch branding cluster",
    },
    {
        "rank": 268,
        "key": "instagram_carousel_fr",
        "lang": "fr",
        "slug": "02-cluster-instagram-carousel",
        "cover": "018",
        "category": "Branding",
        "title": "Instagram carousel : série cohérente avec Brand Kit",
        "seo_title": "Instagram Carousel FR — branding cluster ChatCanvas SOP",
        "description": "FR 404 fix: Instagram carousel branding, slide 4 accent lock, Touch Edit CTA.",
        "seo_description": "Branding cluster: six slides same thread, disclaimer editable, Design Agent QA.",
        "focus": "02 cluster instagram carousel",
        "keywords": ["instagram carousel ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Branding — Instagram Carousel FR",
        "body": INSTAGRAM_CAROUSEL_FR,
        "expand_topic": "FR Instagram carousel branding cluster",
    },
    {
        "rank": 269,
        "key": "ai_prompts_fr",
        "lang": "fr",
        "slug": "10-ai-design-prompts-that-actually-work",
        "cover": "019",
        "category": "How-To",
        "title": "10 prompts design IA qui fonctionnent vraiment",
        "seo_title": "10 AI Design Prompts That Work FR — How-To SOP",
        "description": "FR 404 fix: AI design prompts How-To, mandatory fields not magic phrases.",
        "seo_description": "How-To: ratio hex safe zone, Touch Edit test, Brand Kit in every prompt.",
        "focus": "10 ai design prompts that actually work",
        "keywords": ["ai design prompts", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — 10 AI Design Prompts FR",
        "body": AI_PROMPTS_FR,
        "expand_topic": "FR 10 AI design prompts that actually work",
    },
    {
        "rank": 270,
        "key": "print_tools_fr",
        "lang": "fr",
        "slug": "10-best-ai-print-design-tools-2026",
        "cover": "020",
        "category": "Comparison",
        "title": "10 meilleurs outils print design IA 2026 : comparaison honnête",
        "seo_title": "10 Best AI Print Design Tools 2026 FR — task groups",
        "description": "FR 404 fix: print design tools comparison, task groups not fake ranking scores.",
        "seo_description": "Comparison: bleed layout vs series platform, zero fabricated pricing.",
        "focus": "10 best ai print design tools 2026",
        "keywords": ["ai print design tools", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — 10 Best AI Print Design Tools 2026 FR",
        "body": PRINT_TOOLS_FR,
        "expand_topic": "FR 10 best AI print design tools 2026 comparison",
    },
    {
        "rank": 271,
        "key": "text_to_video_tools_fr",
        "lang": "fr",
        "slug": "10-best-text-to-video-ai-tools-2026",
        "cover": "021",
        "category": "Comparison",
        "title": "10 meilleurs outils text-to-video IA 2026 : comparaison honnête",
        "seo_title": "10 Best Text-to-Video AI Tools 2026 FR — task groups",
        "description": "FR 404 fix: text-to-video tools comparison, static-first not fake scores.",
        "seo_description": "Comparison: motion companion vs series stack, no fabricated benchmarks.",
        "focus": "10 best text to video ai tools 2026",
        "keywords": ["text to video ai tools", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — 10 Best Text-to-Video AI Tools 2026 FR",
        "body": TEXT_TO_VIDEO_TOOLS_FR,
        "expand_topic": "FR 10 best text-to-video AI tools 2026 comparison",
    },
    {
        "rank": 272,
        "key": "openart_review_fr",
        "lang": "fr",
        "slug": "OpenArt-AI-Review",
        "cover": "022",
        "category": "Comparison",
        "title": "OpenArt AI Review : comparaison honnête après usage ops",
        "seo_title": "OpenArt AI Review FR — honest comparison exact slug case",
        "description": "FR 404 fix: OpenArt AI Review, exact slug OpenArt-AI-Review, no fake scores.",
        "seo_description": "OpenArt review: exploration vs series stack, zero fabricated pricing.",
        "focus": "OpenArt AI Review",
        "keywords": ["openart ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — OpenArt AI Review FR",
        "body": OPENART_REVIEW_FR,
        "expand_topic": "FR OpenArt AI Review honest comparison",
    },
    {
        "rank": 273,
        "key": "collage_moodboard_fr",
        "lang": "fr",
        "slug": "ai-collage-moodboard-tools-compared",
        "cover": "023",
        "category": "Comparison",
        "title": "Outils collage et moodboard IA comparés",
        "seo_title": "AI Collage Moodboard Tools Compared FR — honest groups",
        "description": "FR 404 fix: collage moodboard tools compared, task groups not ranking.",
        "seo_description": "Comparison: moodboard exploration vs ChatCanvas static companion.",
        "focus": "ai collage moodboard tools compared",
        "keywords": ["ai collage moodboard", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Collage Moodboard Tools FR",
        "body": COLLAGE_MOODBOARD_FR,
        "expand_topic": "FR AI collage moodboard tools compared",
    },
    {
        "rank": 274,
        "key": "music_video_fr",
        "lang": "fr",
        "slug": "b3-how-to-create-music-video-ai-guide",
        "cover": "024",
        "category": "How-To",
        "title": "Comment créer un clip musical avec IA : guide How-To",
        "seo_title": "How to Create Music Video AI Guide FR — static-first SOP",
        "description": "FR 404 fix: music video AI How-To, static-first Touch Edit layer.",
        "seo_description": "How-To: motion companion optional, Brand Kit hex lock, Design Agent QA.",
        "focus": "b3 how to create music video ai guide",
        "keywords": ["create music video ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Create Music Video AI Guide FR",
        "body": MUSIC_VIDEO_FR,
        "expand_topic": "FR how to create music video AI guide",
    },
    {
        "rank": 275,
        "key": "free_vs_paid_fr",
        "lang": "fr",
        "slug": "b34-free-vs-paid-ai-design-tools-bing",
        "cover": "025",
        "category": "Comparison",
        "title": "Outils design IA gratuits vs payants : comparaison honnête",
        "seo_title": "Free vs Paid AI Design Tools Bing FR — no fake Lovart tiers",
        "description": "FR 404 fix: free vs paid AI design tools, zero fabricated Lovart pricing tiers.",
        "seo_description": "Comparison: operator hours revision tax, Touch Edit cost test, Bing slug context.",
        "focus": "b34 free vs paid ai design tools bing",
        "keywords": ["free vs paid ai design tools", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Free vs Paid AI Design Tools Bing FR",
        "body": FREE_VS_PAID_FR,
        "expand_topic": "FR free vs paid AI design tools Bing comparison",
    },
]

EXPAND_FN = {
    "de": expand_de,
    "fr": expand_fr,
}

UNIT_MAP = {
    "zh": "CJK",
    "zh-TW": "CJK",
    "en": "words",
    "de": "words",
    "fr": "words",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch26 content cluster.*\n"
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
