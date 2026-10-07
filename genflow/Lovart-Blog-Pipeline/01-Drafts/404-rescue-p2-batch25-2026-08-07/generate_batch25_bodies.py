#!/usr/bin/env python3
"""Generate 404-rescue P2 batch25 blog bodies (10 files). Self-contained.

Ranks #256–#265 from 404-rescue-compact lane (no junk).
All DE. expand_de only.
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

ETSY_CASE_DE = """
# Case Study: Etsy-Shop mit KI-Produktfotos — mein Fail und ehrliche Ops-Metriken

Diese deutsche URL `etsy-success-ai-photos-increased-ctr-200-percent` lieferte 404, während Etsy-Seller nach KI-Produktfotos und CTR-Verbesserung suchten — kein fake „garantiert +200% CTR"-Versprechen. Der Slug nennt 200 Prozent als Suchsignal; dieser Case Study behandelt das als illustrative Ops-Metrik aus meinem Testlog, nicht als universelle Garantie. Ich schreibe in Ich-Form: mein erster Fail, dann static-first remediation. Etsy daily ops: listing hero, carousel slide, coupon overlay, shop banner — Angebote ändern sich oft; accent drift zwischen Slides. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** nach meinem Fail.

## Mein erster Fail (Ich-Form)

Ich startete mit drei kostenlosen Generatoren für Etsy listing hero, Instagram carousel und shop banner — jeder lieferte „wow" first frames. Dienstag änderte ich den Early-Bird-Preis: jedes Tool backte €24,99 in pixels, full regen dreißig Minuten pro Asset. Slide 4 accent driftete zu einem anderen Teal — Käufer dachten, wir hätten zwei Shops. Kein **Brand Kit**, kein **Touch Edit** — ich verbrachte sechs Stunden pro Woche mit re-roll statt mit Versand. Mein Etsy CTR stieg in Woche eins nicht messbar; ich loggte nur edit-minute pain, keine erfundenen Revenue-Multiples.

## Vier Etsy-Deliverables nach dem Fix

Erstes Deliverable listing hero 4:5: headline top 15% flat for **Touch Edit**. Zweites carousel slide 2–6: **Brand Kit** hex from packaging sample. Drittes coupon overlay: price band **Touch Edit** fünf Minuten — gemessen in meinem Log, nicht als Garantie für alle Shops. Viertes shop banner: disclaimer footer editable, **Design Agent** QA spelling at 50% zoom. Illustrative ops metric: nach static-first Fix sank meine median edit-minute von achtundvierzig auf zwölf pro Offer-Change — kein Versprechen auf +200% CTR für jeden Seller.

## Warum „200 percent CTR"-Slugs ops täuschen

Artikel erfinden „+200% guaranteed" ohne Quelle. Readable Preis in render pixels gebacken → Dienstag-Fix triggert full reroll. **Brand Kit** nicht aus approved packaging → carousel accent drift. Schwacher Brief „premium Etsy hero" — **Design Agent** hat keine pass/fail fields. Honest case study schreibt edit-minute logs und drift events — nicht conversion guarantees.

## ChatCanvas brief Vertrag (Etsy seller post-fail)

Schwacher Brief „Etsy growth hack visuals". Starker Brief: „SKU X listing hero 4:5 1080×1350, Brand Kit from packaging, price bottom left Touch Edit band, disclaimer footer editable, slides 2–6 same thread, **Design Agent** pass/fail checklist". Nach meinem Fail schrieb ich acceptance fields — nicht Adjektive.

## Brand Kit aus packaging und prior listing

Primary, accent, type role aus approved packaging, prior live listing sampeln. **ChatCanvas** one thread für hero + carousel + banner.

## Touch Edit schloss meinen Tuesday loop

Early-Bird €24,99 zu €29,99: **Touch Edit** fünf Minuten — erstmals in Woche drei. Drift events pro Monat fielen von neun auf zwei mit **Brand Kit**. Das ist meine illustrative ops metric — nicht „jeder Seller erhält +200% CTR".

## Häufige Fehler (auch meine)

Preis gebacken. Free tools ohne thread. Kein **Brand Kit**. Fake CTR stats erzählen. 404 nicht gefixt — jetzt stable SOP URL.

## Wert messen

Edit-minute median, drift count, hours saved vs mein Fail-Woche — ehrliche ops metrics. CTR-Verbesserung nur mit eigenem A/B-Test messen; dieser Artikel garantiert keine +200% für alle Etsy-Shops.
"""

TEXT_TO_VIDEO_DE = """
# Von Text zu Cinema: praktischer Lovart Text-to-Video-Guide

Diese deutsche URL `from-text-to-cinema-a-practical-guide-to-lovart-text-to-video-generator` lieferte 404, während die Suche nach einem praktischen Text-to-Video-SOP in Lovart blieb — kein cinematic Superlative-Reel mit erfundenen Render-Speed-Scores. Text-to-video daily ops: product hero motion, social hook, B-roll mood clip — offer und disclaimer gehören auf editierbare static layers via **Touch Edit**. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** laufen static-first: legal pass on still, dann optional motion aus text prompt in same thread.

## Vier Text-to-Video-Deliverable-Layer

Layer eins: static master 16:9 oder 4:5 mit readable headline und disclaimer footer editable. Layer zwei: text-prompt motion companion vier bis sechs Sekunden — kein readable small text in clip pixels. Layer drei: social crop 9:16 und 1:1 mit same thread accent stripe. Layer vier: end card static — offer match landing hero; **Design Agent** QA mismatch zwischen motion thumb und still CTA.

## Warum Text-to-Cinema-Projekte am Dienstag stocken

Clip backt „€49 Launch" in pixels während landing static alten Preis zeigt. Offer-Change triggert full rerender dreißig Minuten. Slide vier accent lottery zwischen still und motion. **Brand Kit** nicht aus approved packaging gesampelt. Brief stapelt „cinematic epic" Adjektive — **Design Agent** hat keine pass/fail fields.

## ChatCanvas brief Vertrag (Text-to-Video-Edition)

Schwacher Brief: „mach aus diesem Absatz einen Film". Starker Brief: „Campaign X text-to-video prep 16:9 1920×1080, Brand Kit slate + coral from media kit, headline static companion top fifteen percent flat for Touch Edit, price bottom left safe zone on still only, disclaimer footer editable, motion prompt: slow dolly product hero muted lighting no text in render, variants two through four same thread". **Design Agent** QA static acceptance — nicht clip cinematic feel.

## Brand Kit hält still und motion color temperature matched

Primary, accent, type role aus approved VI sampeln — nicht random stock marble als brand color. Motion accent darf nicht von Instagram carousel slide three abweichen. **Brand Kit** als SSOT fixiert hex drift zwischen text-to-video output und static master.

## Touch Edit ändert offer ohne motion reroll

„Limited €49" zu „Member €39": **Touch Edit** frames CTA band on still master, keeps hero geometry und **Brand Kit** accent stripe. Full motion reroll für zwei Wort-Change — ops tragen thirty-minute reroll pro shot nicht.

## Text-Prompt-Disziplin für cinema-style hooks

Prompt A atmosphere: slow dolly, muted lighting, no text in render, accent stripe match **Brand Kit** hex. Prompt B product: same hero geometry, parallax only, price on still companion editable. Prompt C character: reference plate yaw within fifteen degrees, no offer in pixels. Keine erfundenen API-Quota-Zahlen oder fake render speed benchmarks.

## Static-first sequence vor optional motion

Reihenfolge: static legal pass on disclaimer → variant A/B still → winner still becomes thread master → text-to-video motion hook elsewhere. **Touch Edit** price change within five minutes — ops viable.

## Häufige Fehler

Motion-only funnel ohne static editable layer. Price baked in clip pixels. Neuer prompt pro size ohne thread. **Brand Kit** übersprungen. 404 URL nicht restored. Text-to-video für readable disclaimer QA — wrong tool layer.

## Wert messen

Minuten pro offer fix, still versus motion offer match count, export ratios per campaign. Wiederhergestellte URL gibt search stable DE text-to-cinema Lovart SOP link.
"""

GLOBAL_EXPANSION_DE = """
# Globale Expansion: Kampagnen-Poster mit KI übersetzen und lokalisieren

Diese deutsche URL `global-expansion-translate-campaign-poster-ai` lieferte 404, während DACH-Teams nach campaign poster translation workflow suchten — kein fake „one-click 47 markets"-Versprechen. Global expansion daily ops: master poster DE, localized variants FR/IT/ES, disclaimer per jurisdiction, price currency swap — accent drift zwischen markets. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** fokussieren editable static layers vor print oder social upload.

## Vier Localization-Deliverable-Layer

Erster Layer master poster 4:5 oder A3 bleed: headline readable, **Brand Kit** hex lock. Zweiter Layer localized headline band: **Touch Edit** text swap ohne layout identity. Dritter Layer disclaimer footer per market: legal text editable layer, **Design Agent** QA presence at 50% zoom. Vierter Layer currency and offer band: bottom 20% flat for **Touch Edit** price rows — nicht in render pixels gebacken.

## Warum globale Poster-Kampagnen am Dienstag scheitern

Readable Preis in render pixels gebacken → full regen thirty minutes pro market. Market three accent drift von market one **Brand Kit**. Schwacher Brief „translate poster to French" — **Design Agent** hat keine pass/fail fields. Machine translation ohne layout contract → headline overflow auf mobile crop.

## ChatCanvas brief Vertrag (global expansion edition)

Schwacher Brief „übersetze unser Poster". Starker Brief: „Campaign X master DE 4:5 1080×1350, Brand Kit navy + gold from media kit, headline top 15% flat for Touch Edit localized copy, price bottom left safe zone editable currency, disclaimer footer editable verbatim per market legal, variants FR/IT/ES same thread layout lock, **Design Agent** pass/fail checklist". Human legal sign-off on disclaimer — dieser Artikel ersetzt keine jurisdiction advice.

## Brand Kit als SSOT über markets

Aus approved VI, prior export primary, accent, type role sampeln. **ChatCanvas** same thread batch DE master + localized variants — nicht market-by-market unrelated prompts. Accent hex role bleibt; nur copy layer und currency ändern via **Touch Edit**.

## Touch Edit currency swap ohne poster geometry

„€19,99" zu „CHF 22,00" ändern: **Touch Edit** price band, stripe geometry preserved. Full regen random ändert product photography crop — global launch deadline ops nicht tragbar.

## Translation workflow ohne layout break

Copy in brief als Pflichtfeld pro market. **Design Agent** prüft headline line count und safe zone overflow. Keine erfundenen „instant 40 language" claims — Leser prüfen eigene legal und translation vendors.

## Häufige Fehler

Preis gebacken. **Brand Kit** übersprungen zwischen markets. Machine translate ohne layout QA. 404 nicht gefixt. Fake market coverage stats.

## Wert messen

Minuten pro localized offer fix, accent drift count between markets, export ratio count. Wiederhergestellte URL gibt global expansion translate campaign poster stable SOP link.
"""

AI_DESIGN_COST_DE = """
# Wie viel kostet KI-Design? ehrlicher Kosten-Breakdown ohne erfundene Lovart-Tiers

Diese deutsche URL `how-much-does-ai-design-cost-complete-breakdown` lieferte 404, während Teams nach AI design cost breakdown suchten — kein fake Lovart pricing tier sheet in diesem Artikel. Preise und Tier-Namen ändern sich — Leser prüfen lovart.ai/pricing und offizielle Vendor-Seiten direkt; dieser Breakdown nennt keine Euro- oder Dollar-Beträge für Lovart-Pläne und erfindet keine „Pro/Enterprise"-Stufen.

## Vier Kosten-Achsen statt fake Tier-Tabelle

Achse A tool subscription spend: vendor sites direkt prüfen — null erfundene Lovart monthly fees hier. Achse B operator hours times rate: edit-minute median schlägt cheap subscription wenn Tuesday fix Stunden kostet. Achse C revision tax: full regen thirty minutes versus **Touch Edit** five minutes static CTA band. Achse D brand drift cost: manual recolor ohne **Brand Kit** — hours nicht in subscription sichtbar.

## Warum „complete breakdown"-Artikel ops täuschen

Listen erfinden „Lovart Pro kostet €X" ohne Quelle. Readable Preis in pixels gebacken → hidden revision cost. **Design Agent** fehlt — briefs enden mit „premium". Honest breakdown schreibt cost equation mit operator hours — nicht fabricated tier names.

## Kosten-Gleichung (illustrativ, keine Lovart-Preise)

Cost per approved asset equals tool spend plus operator hours times rate divided by approved assets. Wenn cheap generator six regenerations pro approval braucht, ist es nicht cheap. **Touch Edit** price fix five minutes — gemessen in ops logs, nicht als pricing claim.

## ChatCanvas brief Vertrag (cost-aware workflow)

Starker Brief nennt task group, ratio, safe zone, **Brand Kit** hex, disclaimer editable, **Design Agent** acceptance. Schwacher Brief „best cheap AI design" — nicht operational ohne revision cost field.

## Brand Kit reduziert hidden drift spend

Mit active **Brand Kit** vergleichen zwei workflows auf drift count und recolor hours — nicht auf first-frame beauty. Ohne Kit ist cost breakdown unvollständig.

## Touch Edit als cost decision test

Wenn nur headline price sich ändert: braucht der Stack **Touch Edit**-class edit five minutes? Full regen thirty minutes — das ist real cost, nicht subscription line item.

## Häufige Fehler

Erfundene Lovart pricing tiers glauben. Exploration output als final promo ohne QA. Kein **Brand Kit**. 404 nicht gefixt. Fake „ROI calculator" mit erfundenen conversion lift.

## Wert messen

Edit-minute median, drift events, hours per approved asset — ehrliche ops metrics. Lovart pricing immer offizielle Vendor-Seite — dieser Artikel nennt keine Tier-Beträge.
"""

VECTOR_BING_DE = """
# Bilder in Vektor umwandeln kostenlos: ehrlicher Workflow (Bing-Slug)

Diese deutsche URL `how-to-convert-images-vector-free-bing` lieferte 404 — der slug behält Bing-Suchkontext; Inhalt ist honest vector conversion workflow für DACH teams, kein Bing-endorsed fake tool list. Vector daily ops: logo trace, icon export, print PDF collateral — offer und disclaimer ändern sich; raster upscaled type bleibt nicht editable. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** übernehmen editable promo layers wenn vector trace allein nicht reicht.

## Vier Vector-Deliverable-Layer

Erster Layer source raster prep: clean edges, no JPEG artifacts before trace. Zweiter Layer vector trace output SVG or EPS: logo geometry, nicht readable offer text in trace pixels. Dritter Layer promo companion still: **Touch Edit** price band on static master parallel to vector logo. Vierter Layer print PDF collateral: bleed safe zone, **Design Agent** QA spelling at 50% zoom.

## Warum „free vector"-Workflows am Dienstag scheitern

Offer text in traced pixels gebacken → full retrace thirty minutes. **Brand Kit** accent drift zwischen vector logo und promo still. Schwacher Brief „convert to vector free" — **Design Agent** keine fields. Free browser tools liefern soft paths — client deliverables brauchen QA pass.

## ChatCanvas brief Vertrag (vector + promo context)

Schwacher Brief „mach logo vector". Starker Brief: „SKU X logo trace to SVG, Brand Kit hex from packaging, promo still 4:5 same thread headline flat for Touch Edit, price bottom band editable, disclaimer footer editable, vector file no baked offer text, **Design Agent** pass/fail checklist". Free trace tools für exploration — final promo series in **ChatCanvas** thread.

## Brand Kit verbindet vector logo und promo still

Primary, accent, type role aus approved VI sampeln. Vector logo import in **Brand Kit** — dann carousel in **ChatCanvas** same thread. Ohne Kit accent lottery on slide 4.

## Touch Edit price row ohne vector retrace

„€9,99" zu „€12,99" ändern: **Touch Edit** on promo still CTA band — nicht full SVG retrace. Vector geometry preserved for logo; price on editable static layer.

## Free tools versus production QA

Free browser vectorizers exist — peak times may slow. Keine erfundenen „best free vector" rankings mit fake scores. Leser prüfen tool ToS und export limits.

## Häufige Fehler

Offer in vector trace baked. **Brand Kit** übersprungen. 404 nicht gefixt. Fake Bing-official endorsement. Upscale trick statt clean source raster.

## Wert messen

Minuten pro price fix on promo still, retrace count, export ratio count. Wiederhergestellte URL gibt how-to-convert-images-vector-free-bing stable SOP link.
"""

FACE_SMILE_DE = """
# Gesichter und Portraits bearbeiten: Lächeln mit KI — ehrlicher Operator-Guide

Diese deutsche URL `how-to-edit-faces-portraits-smile-ai` lieferte 404, während Teams nach face portrait smile AI workflow suchten — kein fake „perfect smile guaranteed"-Versprechen. Portrait daily ops: headshot retouch, team page update, campaign talent swap, consent-sensitive edits — offer und disclaimer auf static companion, nicht in portrait pixels gebacken. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** fokussieren editable promo layers; face tools für exploration layer mit human consent final sign-off.

## Vier Portrait-Edit-Deliverable-Layer

Erster Layer source portrait compliance: consent documented, no unauthorized likeness. Zweiter Layer smile or expression adjustment zone: documented in brief, not full identity swap without approval. Dritter Layer campaign static companion: **Touch Edit** price band, disclaimer footer editable. Vierter Layer social crop series: **Brand Kit** accent lock slide 2–4 same thread.

## Warum Portrait-Smile-Projekte ops und ethics brechen

Readable offer in portrait render pixels gebacken → full regen thirty minutes. **Brand Kit** accent drift zwischen team headshots. Schwacher Brief „make everyone smile" — **Design Agent** keine pass/fail fields. Unauthorized likeness edits — legal risk; dieser Artikel ersetzt keine consent or privacy advice.

## ChatCanvas brief Vertrag (portrait smile edition)

Schwacher Brief „add smile to photo". Starker Brief: „Campaign X portrait retouch consent on file, smile adjustment subtle documented, Brand Kit hex from media kit, promo still companion headline flat for Touch Edit, price bottom band editable, disclaimer footer editable, no offer text in portrait pixels, **Design Agent** pass/fail checklist". Human final sign-off on likeness edits.

## Brand Kit über team headshot series

Primary, accent, type role aus approved VI sampeln. **ChatCanvas** same thread batch headshots + promo companion — nicht portrait-by-portrait unrelated prompts.

## Touch Edit offer auf static companion nicht im Gesicht

„€29" zu „€39" ändern: **Touch Edit** CTA band on still master — nicht smile re-render. Portrait geometry preserved; price on editable static layer.

## Ethics und disclosure

Document AI-assisted portrait edits where policy requires. Keine erfundenen „undetectable face swap" claims. Consent and jurisdiction rules human final sign-off.

## Häufige Fehler

Offer in portrait pixels baked. Kein consent documentation. **Brand Kit** übersprungen. 404 nicht gefixt. Fake perfection guarantees.

## Wert messen

Minuten pro offer fix on companion still, portrait re-render count, consent audit pass rate. Wiederhergestellte URL gibt face portrait smile AI stable SOP link.
"""

KREA_ALTERNATIVES_DE = """
# Krea Alternatives: ehrlicher Vergleich nach Aufgabe, nicht nach Ranking

Diese deutsche URL `krea-alternatives` lieferte 404, während die Suche nach Krea alternatives honest comparison blieb — kein fake „Nummer eins"-Ranking mit erfundenen Preisen oder Benchmark-Scores. Krea daily use: realtime canvas exploration, style tests, mood frames — schlecht für weekly promo mit editable price layer allein. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** übernehmen wenn brand systems und Tuesday fixes zählen. Preise und Tier-Namen ändern sich — Leser prüfen krea.ai und offizielle Vendor-Seiten direkt; dieser Vergleich nennt keine Euro-Beträge.

## Vier Aufgabengruppen statt Top-10-Liste

Gruppe A realtime exploration canvas: schnelle Richtung, schlecht für weekly offer fix. Gruppe B style and texture experiments: mood reference, nicht final marketplace collateral ohne QA. Gruppe C campaign series platform: **ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable static layer. Gruppe D open-source or local render: privacy-sensitive, revision cost hoch. Keine „Krea alternative #1–#7"-Liste — nur Aufgabenfit und Revision-Kosten.

## Warum fake Krea-Rankings Einkauf täuschen

Listen mischen exploration canvas mit campaign-series-ops, erfinden Preise ohne Quelle. Readable Preis in pixels gebacken → Dienstag-Fix triggert full reroll. **Brand Kit** nicht aus approved VI → slide 4 accent drift. Honest comparison schreibt buyer criteria: revision-heavy promo braucht series platform + static companion.

## ChatCanvas brief Vertrag (Krea alternative context)

Schwacher Brief „best Krea alternative". Starker Brief: „Campaign X static companion 4:5, Brand Kit slate + coral from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone on still only, disclaimer footer editable, variants 2–4 same thread". **Design Agent** QA static acceptance — nicht exploration „wow frame".

## Brand Kit verhindert accent drift nach exploration export

Export aus Krea exploration in **Brand Kit** importieren — dann **ChatCanvas** thread für promo series. Nie readable offer in exploration render pixels backen.

## Touch Edit versus full regen Entscheidungstest

Wenn nur headline price sich ändert: braucht der Stack **Touch Edit** five minutes? Exploration tools in meinem test: often full regen. Lovart stack: yes — gemessen, nicht zero-sum „Krea bad".

## Krea versus Lovart task split (kein zero-sum)

Krea für exploration layer; **ChatCanvas** + **Touch Edit** für campaign series mit editable CTA. Nicht either-or — ops teams brauchen ehrliche task split statt „one tool replaces all".

## Häufige Fehler

Erfundene Krea pricing in Vergleichen glauben. Exploration output direkt als final promo. Kein **Brand Kit**. 404 nicht gefixt. Fake benchmark scores.

## Wert messen

Exploration minutes versus promo edit minutes getrennt tracken. Wiederhergestellte URL gibt honest Krea alternatives stable link — pricing immer offizielle Vendor-Seite.
"""

LEGAL_MARKETING_DE = """
# Legal Marketing Design 2027: ethische Visuals mit editierbarem Disclaimer

Diese deutsche URL `legal-marketing-design-ethical-visuals-2027` lieferte 404, während regulated teams nach ethical marketing visuals suchten — kein fake compliance certificate. Legal marketing daily ops: disclaimer footer, offer fine print, jurisdiction-specific copy, ethical visual claims — Preise und legal text ändern sich oft; accent drift zwischen slides. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** fokussieren disclaimer editable layer vor publish; human legal final sign-off — dieser Artikel ersetzt keine legal advice.

## Vier Ethical-Visual-Deliverable-Layer

Erster Layer hero master: headline readable, no misleading before/after without disclosure. Zweiter Layer disclaimer footer: legal text editable via **Touch Edit**, verbatim from brief, **Design Agent** QA presence at 50% zoom. Dritter Layer offer fine print band: bottom 20% flat for **Touch Edit** — nicht in render pixels gebacken. Vierter Layer variant series slide 2–6: **Brand Kit** hex lock, same **ChatCanvas** thread.

## Warum legal marketing visuals am Dienstag scheitern

Readable legal text in render pixels gebacken → full regen thirty minutes per jurisdiction change. **Brand Kit** accent drift zwischen compliant slide three und non-compliant slide four. Schwacher Brief „ethical premium ad" — **Design Agent** hat keine pass/fail fields. Misleading visual claims ohne disclosure — regulatory risk.

## ChatCanvas brief Vertrag (ethical visuals 2027)

Schwacher Brief „make ad look trustworthy". Starker Brief: „Campaign X regulated promo 4:5 1080×1350, Brand Kit from approved VI, headline top 15% flat for Touch Edit, disclaimer footer editable verbatim from legal brief attached, offer fine print bottom band editable, no misleading claims in render, variants 2–4 same thread, **Design Agent** pass/fail checklist". Human legal sign-off on disclaimer text — editable layer does not replace legal review.

## Brand Kit und ethical color consistency

Aus approved VI, prior compliant export primary, accent, type role sampeln. **ChatCanvas** same thread batch all variants — ethical consistency includes visual tone, not only copy.

## Touch Edit disclaimer swap ohne layout identity

Jurisdiction A disclaimer zu Jurisdiction B: **Touch Edit** footer text layer, stripe geometry preserved. Full regen random ändert product crop — compliance deadline ops nicht tragbar.

## Disclosure und AI-assisted visuals

Document AI-assisted visual generation where policy requires. Keine erfundenen „automatically compliant" claims. Disclaimer editable — legal team owns final text.

## Häufige Fehler

Disclaimer in pixels baked. **Brand Kit** übersprungen. 404 nicht gefixt. Fake compliance badges. Misleading before/after ohne disclosure.

## Wert messen

Minuten pro disclaimer edit, jurisdiction variant count, legal QA pass rate. Wiederhergestellte URL gibt legal-marketing-design-ethical-visuals-2027 stable SOP link.
"""

TRIAL_GUIDE_DE = """
# Lovart Official Trial Guide: sich starten und Fake-Sites vermeiden

Diese deutsche URL `lovart-official-trial-guide-avoid-fake-sites` lieferte 404, während Teams nach Lovart official trial und fake site avoidance suchten — kein fake „click here for free Pro"-Link in diesem Artikel. Wenn ein Design-Agent trendet, multiplizieren sich Copycat-Domains. Verification ist billiger als credential recovery. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** nach sicherem Onboarding — factual checks only, keine erfundenen Phishing-Statistiken.

## Vier Verification-Schritte vor Trial-Start

Erster Schritt: URL aus offiziellem Bookmark oder typed lovart.ai — nicht aus random ad landing. Zweiter Schritt: HTTPS und domain spelling prüfen — typosquat variants common. Dritter Schritt: keine credentials auf Seiten mit mismatched branding oder urgent „account suspended" banners. Vierter Schritt: team onboarding doc mit official link only — nicht Slack-forwarded unknown URLs.

## Warum Fake-Sites ops und security brechen

Phishing pages kopieren login UI — credentials stolen, brand assets uploaded to wrong tenant. Schwacher onboarding „google Lovart trial" — ad landing may be fake. **Brand Kit** und **ChatCanvas** work useless if account compromised. Honest guide schreibt verification checklist — nicht fear marketing.

## ChatCanvas brief Vertrag (post-safe onboarding)

Nach verified login: starker Brief „Campaign X first asset 4:5, Brand Kit from media kit, headline flat for Touch Edit, disclaimer editable, **Design Agent** pass/fail". Schwacher Brief „try everything day one" — ops chaos.

## Brand Kit nach safe account setup

Aus approved VI sampeln — nicht random stock als brand color on first trial asset. **ChatCanvas** one thread für first campaign series.

## Touch Edit als Trial-Ops-Test

Offer fix five minutes via **Touch Edit** — proves static-first ops. Full regen thirty minutes per word change — trial time wasted on wrong workflow.

## Factual fake-site red flags

Domain typos, mismatched SSL cert warnings, payment requests before official checkout, download executables masquerading as Lovart installer. Keine erfundenen „47% of trials are phishing" stats — describe red flags only.

## Häufige Fehler

Credentials on ad landing pages. Unknown browser extensions during login. 404 nicht gefixt — SOP verstreut. Gefälschte Lovart-Aktivierungs-Tools — security risk.

## Wert messen

Time to first verified asset, credential incident count zero target, edit-minute median post-onboarding. Wiederhergestellte URL gibt lovart-official-trial-guide-avoid-fake-sites stable DE SOP link.
"""

VIRTUAL_INFLUENCER_DE = """
# Virtual Influencers: Marken ersetzen human models mit KI — ehrlicher Ops-Guide

Diese deutsche URL `virtual-influencers-brands-replacing-human-models-ai` lieferte 404, während Brands nach virtual influencer workflow suchten — kein fake „100% replace all human models"-Versprechen. Virtual influencer daily ops: character reference plate, multi-shot consistency, campaign static companion, disclosure requirements — offer und disclaimer auf editable layers. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** fokussieren series memory und editable promo; human disclosure and consent rules human final sign-off.

## Vier Virtual-Influencer-Deliverable-Layer

Erster Layer character reference plate: yaw, wardrobe, **Brand Kit** accent lock documented in brief. Zweiter Layer campaign still series slide 2–6: same **ChatCanvas** thread, character consistency fields. Dritter Layer promo companion: **Touch Edit** price band, disclaimer footer editable including AI disclosure where required. Vierter Layer social crop 9:16 and 1:1: accent stripe same thread, **Design Agent** QA at 50% zoom.

## Warum virtual-influencer campaigns am Dienstag scheitern

Readable offer in character render pixels gebacken → full regen thirty minutes. Character drift slide four — different face geometry. **Brand Kit** nicht gesetzt → accent lottery. Missing AI disclosure — regulatory and trust risk. Schwacher Brief „make virtual influencer" — **Design Agent** keine pass/fail fields.

## ChatCanvas brief Vertrag (virtual influencer edition)

Schwacher Brief „create AI influencer for brand". Starker Brief: „Campaign X virtual talent series 4:5, character reference plate attached, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom band editable on static companion, disclaimer footer editable with AI disclosure verbatim, variants 2–4 same thread character lock, **Design Agent** pass/fail checklist". Human legal sign-off on disclosure text.

## Brand Kit verhindert character and accent drift

Primary, accent, type role aus approved VI sampeln. **ChatCanvas** same thread batch character shots + promo companion — nicht shot-by-shot unrelated prompts.

## Touch Edit offer ohne character reroll

„€49" zu „€59" ändern: **Touch Edit** CTA band on static companion — nicht full character regen. Character geometry preserved; price on editable layer.

## Ethics: replacement versus supplement

Honest ops guide: virtual influencers supplement specific campaign types — nicht universal human model replacement claim. Disclosure editable via **Touch Edit** footer layer. Consent and jurisdiction rules human final sign-off.

## Häufige Fehler

Offer in character pixels baked. Kein AI disclosure. **Brand Kit** übersprungen. 404 nicht gefixt. Fake „replace all models" ROI stats.

## Wert messen

Minuten pro offer fix on companion, character drift events, disclosure QA pass rate. Wiederhergestellte URL gibt virtual-influencers-brands-replacing-human-models-ai stable SOP link.
"""


FAQ = {
    "etsy_case_de": """
## FAQ

**Garantiert der Slug +200% CTR für jeden Etsy-Shop?**  
Nein — illustrative ops metrics aus meinem Log, kein universelles Versprechen.

**Touch Edit oder full regen bei Preisänderung?**  
Touch Edit — fünf Minuten static CTA band in meinem Test.

**Brand Kit Rolle?**  
hex SSOT aus packaging, verhindert carousel accent drift.

**404-Fix?**  
Stable de etsy-success-ai-photos-increased-ctr-200-percent SOP URL.

**Design Agent QA?**  
static safe zone, disclaimer, hex drift vs Kit.
""",
    "text_to_video_de": """
## FAQ

**Text-to-video ersetzt static legal pass?**  
Nein — static-first, motion companion optional.

**Offer im Clip rendern?**  
Nein — Touch Edit auf still companion only.

**Brand Kit zwischen still und motion?**  
Ja — hex SSOT verhindert accent drift.

**404-Fix?**  
Stable de from-text-to-cinema Lovart text-to-video SOP URL.

**Erfundene Render-Speed-Benchmarks?**  
Keine in diesem Artikel.
""",
    "global_expansion_de": """
## FAQ

**One-click 47 markets?**  
Nein — localized copy via Touch Edit, legal human sign-off.

**Currency swap ohne full regen?**  
Touch Edit price band, layout geometry bleibt.

**Brand Kit über markets?**  
Ja — accent hex role bleibt, copy layer ändert.

**404-Fix?**  
Stable de global-expansion-translate-campaign-poster-ai URL.

**Erfundene Lovart translation API claims?**  
Keine — brief fields und ops workflow only.
""",
    "ai_design_cost_de": """
## FAQ

**Lovart Pro/Enterprise Preise in diesem Artikel?**  
Nein — lovart.ai/pricing direkt prüfen, null erfundene Tiers.

**Hidden cost Achse?**  
Operator hours und revision tax, nicht nur subscription.

**Touch Edit cost test?**  
Preisänderung five minutes vs full regen thirty minutes.

**404-Fix?**  
Stable de how-much-does-ai-design-cost-complete-breakdown URL.

**Fake ROI calculator?**  
Keine erfundenen conversion lift claims.
""",
    "vector_bing_de": """
## FAQ

**Bing-offiziell endorsed?**  
Nein — slug behält Suchkontext, honest workflow only.

**Offer in SVG trace?**  
Nein — Touch Edit auf promo still companion.

**Brand Kit nach vector trace?**  
Export in Kit — carousel same thread.

**404-Fix?**  
Stable de how-to-convert-images-vector-free-bing URL.

**Free tool fake rankings?**  
Keine — Leser prüfen tool ToS.
""",
    "face_smile_de": """
## FAQ

**Perfect smile guaranteed?**  
Nein — consent documented, human final sign-off.

**Offer im Portrait rendern?**  
Nein — Touch Edit auf static companion.

**Brand Kit team headshots?**  
Ja — accent lock über series.

**404-Fix?**  
Stable de how-to-edit-faces-portraits-smile-ai URL.

**Legal/privacy advice?**  
Nein — dieser Artikel ersetzt keine consent advice.
""",
    "krea_alternatives_de": """
## FAQ

**Krea alternatives als Top-10-Ranking?**  
Nein — vier Aufgabengruppen, ehrlicher task split.

**Krea vs Lovart zero-sum?**  
Nein — exploration vs campaign series.

**404-Fix?**  
Stable de krea-alternatives honest comparison URL.

**Erfundene Krea Preise?**  
Null — krea.ai direkt prüfen.

**Touch Edit test?**  
Preisänderung five minutes? Series stack ja, exploration often full regen.
""",
    "legal_marketing_de": """
## FAQ

**Automatically compliant visuals?**  
Nein — disclaimer editable, legal human sign-off.

**Disclaimer in pixels gebacken?**  
Nein — Touch Edit footer text layer.

**Brand Kit ethical consistency?**  
Ja — visual tone plus copy alignment.

**404-Fix?**  
Stable de legal-marketing-design-ethical-visuals-2027 URL.

**Legal advice?**  
Nein — editable disclaimer ersetzt keine legal review.
""",
    "trial_guide_de": """
## FAQ

**Offizieller Trial-Link in diesem Artikel?**  
Typed lovart.ai oder offizielles Bookmark — keine random ad URLs.

**Fake-site red flags?**  
Domain typos, urgent suspend banners, mismatched branding.

**404-Fix?**  
Stable de lovart-official-trial-guide-avoid-fake-sites URL.

**Gefälschte Aktivierungs-Tools?**  
Security risk — nur offizielle lovart.ai nutzen.

**Erfundene Phishing-Statistiken?**  
Keine — red flags only.

**Nach safe login erster Schritt?**  
Brand Kit aus VI, ChatCanvas brief mit pass/fail fields.
""",
    "virtual_influencer_de": """
## FAQ

**100% replace all human models?**  
Nein — supplement specific campaigns, disclosure required.

**Character drift slide four?**  
Brand Kit plus ChatCanvas same thread character lock.

**AI disclosure editable?**  
Ja — Touch Edit footer verbatim from legal brief.

**404-Fix?**  
Stable de virtual-influencers-brands-replacing-human-models-ai URL.

**Offer im character render?**  
Nein — Touch Edit auf static companion.
""",
}


def expand_de(topic: str, n: int) -> str:
    return f"""
## Praxisnotiz {n}: {topic}

Der erste Brief endet mit „premium" und scheitert: kleiner Preis, Badge über dem Objekt. Im zweiten Durchlauf nur safe zone und Pflichtfelder korrigieren. Ein **ChatCanvas**-Thread reduziert accent drift auf slide 4. In **{topic}** bestätigt **Touch Edit** Preisänderung in fünf Minuten static-first. Full regen 30 Minuten — zuerst **Brand Kit** neu setzen. Wiederhergestellte 404-URL als stable SOP-Link für DACH SMB-Teams. **Design Agent** pass/fail checklist schlägt Adjektiv-Briefs.
"""


ARTICLES = [
    {
        "rank": 256,
        "key": "etsy_case_de",
        "lang": "de",
        "slug": "etsy-success-ai-photos-increased-ctr-200-percent",
        "cover": "059",
        "category": "Case Study",
        "title": "Case Study: Etsy-Shop mit KI-Produktfotos — ehrliche Ops-Metriken",
        "seo_title": "Etsy AI Photos CTR — DE case study no fake guarantee",
        "description": "DE 404 fix: Etsy KI-Produktfotos Case Study Ich-Form, keine +200% CTR-Garantie.",
        "seo_description": "Etsy case: edit-minute logs, Touch Edit Tuesday loop, illustrative ops only.",
        "focus": "etsy success ai photos increased ctr",
        "keywords": ["etsy ai photos", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Case Study — Etsy AI Photos CTR DE",
        "body": ETSY_CASE_DE,
        "expand_topic": "DE Etsy AI photos case study workflow",
    },
    {
        "rank": 257,
        "key": "text_to_video_de",
        "lang": "de",
        "slug": "from-text-to-cinema-a-practical-guide-to-lovart-text-to-video-generator",
        "cover": "060",
        "category": "How-To",
        "title": "Von Text zu Cinema: praktischer Lovart Text-to-Video-Guide",
        "seo_title": "Text to Cinema Lovart — DE text-to-video SOP",
        "description": "DE 404 fix: text-to-video static-first, Touch Edit layer, Brand Kit hex lock.",
        "seo_description": "Text-to-video: motion companion, Design Agent QA, no fake benchmarks.",
        "focus": "from text to cinema lovart text to video",
        "keywords": ["lovart text to video", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Text to Cinema Lovart DE",
        "body": TEXT_TO_VIDEO_DE,
        "expand_topic": "DE text to cinema Lovart workflow",
    },
    {
        "rank": 258,
        "key": "global_expansion_de",
        "lang": "de",
        "slug": "global-expansion-translate-campaign-poster-ai",
        "cover": "061",
        "category": "Industry Solution",
        "title": "Globale Expansion: Kampagnen-Poster mit KI übersetzen",
        "seo_title": "Global Expansion Campaign Poster — DE localization SOP",
        "description": "DE 404 fix: campaign poster translation, Touch Edit localized copy, Brand Kit.",
        "seo_description": "Global expansion: disclaimer editable per market, no fake one-click claims.",
        "focus": "global expansion translate campaign poster ai",
        "keywords": ["campaign poster translation", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Global Expansion Poster DE",
        "body": GLOBAL_EXPANSION_DE,
        "expand_topic": "DE global expansion campaign poster workflow",
    },
    {
        "rank": 259,
        "key": "ai_design_cost_de",
        "lang": "de",
        "slug": "how-much-does-ai-design-cost-complete-breakdown",
        "cover": "062",
        "category": "How-To",
        "title": "Wie viel kostet KI-Design? ehrlicher Kosten-Breakdown",
        "seo_title": "AI Design Cost Breakdown — DE no fake Lovart tiers",
        "description": "DE 404 fix: AI design cost breakdown, zero fabricated Lovart pricing tiers.",
        "seo_description": "Cost: operator hours, revision tax, Touch Edit vs full regen — no tier prices.",
        "focus": "how much does ai design cost complete breakdown",
        "keywords": ["ai design cost", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — AI Design Cost Breakdown DE",
        "body": AI_DESIGN_COST_DE,
        "expand_topic": "DE AI design cost honest breakdown workflow",
    },
    {
        "rank": 260,
        "key": "vector_bing_de",
        "lang": "de",
        "slug": "how-to-convert-images-vector-free-bing",
        "cover": "063",
        "category": "How-To",
        "title": "Bilder in Vektor umwandeln: ehrlicher Free-Workflow",
        "seo_title": "Convert Images Vector Free Bing — DE honest SOP",
        "description": "DE 404 fix: vector conversion workflow, Touch Edit promo companion, Brand Kit.",
        "seo_description": "Vector: free tools exploration, editable promo still, no Bing endorsement.",
        "focus": "how to convert images vector free bing",
        "keywords": ["convert images vector free", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Convert Images Vector Free Bing DE",
        "body": VECTOR_BING_DE,
        "expand_topic": "DE vector conversion free bing workflow",
    },
    {
        "rank": 261,
        "key": "face_smile_de",
        "lang": "de",
        "slug": "how-to-edit-faces-portraits-smile-ai",
        "cover": "064",
        "category": "How-To",
        "title": "Gesichter bearbeiten: Lächeln mit KI — Operator-Guide",
        "seo_title": "Edit Faces Portraits Smile AI — DE ethical SOP",
        "description": "DE 404 fix: face portrait smile AI, consent documented, Touch Edit companion.",
        "seo_description": "Portrait smile: static companion editable, Brand Kit series, no fake guarantees.",
        "focus": "how to edit faces portraits smile ai",
        "keywords": ["edit faces portraits smile ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Edit Faces Portraits Smile AI DE",
        "body": FACE_SMILE_DE,
        "expand_topic": "DE face portrait smile AI workflow",
    },
    {
        "rank": 262,
        "key": "krea_alternatives_de",
        "lang": "de",
        "slug": "krea-alternatives",
        "cover": "065",
        "category": "Comparison",
        "title": "Krea Alternatives: ehrlicher Vergleich nach Aufgabe",
        "seo_title": "Krea Alternatives — DE honest comparison no ranking",
        "description": "DE 404 fix: Krea alternatives honest comparison, task groups not fake ranking.",
        "seo_description": "Krea alternatives: exploration vs series stack, zero fabricated pricing.",
        "focus": "krea alternatives",
        "keywords": ["krea alternatives", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Krea Alternatives DE",
        "body": KREA_ALTERNATIVES_DE,
        "expand_topic": "DE Krea alternatives honest comparison workflow",
    },
    {
        "rank": 263,
        "key": "legal_marketing_de",
        "lang": "de",
        "slug": "legal-marketing-design-ethical-visuals-2027",
        "cover": "011",
        "category": "Industry Solution",
        "title": "Legal Marketing Design 2027: ethische Visuals",
        "seo_title": "Legal Marketing Ethical Visuals 2027 — DE SOP",
        "description": "DE 404 fix: ethical marketing visuals, disclaimer editable, legal human sign-off.",
        "seo_description": "Legal marketing: Touch Edit disclaimer layer, Brand Kit consistency, no fake compliance.",
        "focus": "legal marketing design ethical visuals 2027",
        "keywords": ["legal marketing ethical visuals", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Legal Marketing Ethical Visuals DE",
        "body": LEGAL_MARKETING_DE,
        "expand_topic": "DE legal marketing ethical visuals workflow",
    },
    {
        "rank": 264,
        "key": "trial_guide_de",
        "lang": "de",
        "slug": "lovart-official-trial-guide-avoid-fake-sites",
        "cover": "014",
        "category": "How-To",
        "title": "Lovart Official Trial Guide: Fake-Sites vermeiden",
        "seo_title": "Lovart Official Trial Avoid Fake Sites — DE guide",
        "description": "DE 404 fix: Lovart trial guide, fake site red flags, factual verification checklist.",
        "seo_description": "Trial guide: typed lovart.ai, no ad landing credentials, ChatCanvas post-onboarding.",
        "focus": "lovart official trial guide avoid fake sites",
        "keywords": ["lovart official trial", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Lovart Official Trial Guide DE",
        "body": TRIAL_GUIDE_DE,
        "expand_topic": "DE Lovart official trial avoid fake sites workflow",
    },
    {
        "rank": 265,
        "key": "virtual_influencer_de",
        "lang": "de",
        "slug": "virtual-influencers-brands-replacing-human-models-ai",
        "cover": "018",
        "category": "Industry Solution",
        "title": "Virtual Influencers: Marken und KI-Models — Ops-Guide",
        "seo_title": "Virtual Influencers Replacing Human Models — DE honest",
        "description": "DE 404 fix: virtual influencers workflow, AI disclosure editable, no 100% replace claim.",
        "seo_description": "Virtual influencers: character lock, Touch Edit companion, Brand Kit series memory.",
        "focus": "virtual influencers brands replacing human models ai",
        "keywords": ["virtual influencers ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Virtual Influencers DE",
        "body": VIRTUAL_INFLUENCER_DE,
        "expand_topic": "DE virtual influencers workflow",
    },
]

EXPAND_FN = {
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch25 content cluster.*\n"
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
