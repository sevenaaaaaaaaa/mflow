---
title: Custom Skills in Lovart: automatizza i workflow di design
slug: 02-wiki-custom-skills-guide
date: 2026-08-05
language: it
page_type: Blog Post
category: Wiki
author: Lovart Content Team
description: Guida wiki IT: Custom Skills riutilizzabili, trigger, SDL e integrazione Brand Kit + Touch Edit.
focus_keyword: custom skills guide lovart
keywords:
  - custom skills
  - lovart automation
  - design workflow
  - skill builder
seo_title: Custom Skills in Lovart: automatizza i workflow di design
seo_description: Guida completa Custom Skills: dal primo skill Instagram resize al pipeline multi-step con MCoT.
cover_url: https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-053-1024x682.png
alt_text: 02 wiki custom skills guide — Lovart blog cover
status: ready
content_cluster: i18n 404 recovery
releaseDate: 2026-08-05T14:00:00Z
publishedAt: 2026-08-05T14:00:00Z
---

# Custom Skills in Lovart: automatizza i workflow di design

Ho riscritto `/it/blog/02-wiki-custom-skills-guide` perché l'URL restituiva 404. Non è un brochure: è la guida wiki che uso quando un team chiede «come evitiamo di ridimensionare manualmente 15 varianti ogni martedì».

## Posizione

Custom Skills sono macro riutilizzabili con intelligenza AI integrata. Un click o un comando naturale esegue una sequenza che altrimenti mangia mezza giornata.

Focus keyword: **custom skills guide lovart**.

## Anatomia di uno Skill

Ogni skill ha quattro componenti:

```
Skill: "Social Media Batch Generator"
├── Trigger: comando, pulsante, API, schedule
├── Input Schema: testo, immagini, Brand Kit
├── Operation Sequence: generate → resize → export
└── Output Configuration: formato, naming, cartella
```

## Skill Builder: Visual vs SDL

**Visual Builder:** blocchi collegati (Input → Resize → Export). Consigliato per chi parte da zero.

**Code Builder (SDL):** YAML con prompt embedded. Per pipeline complesse e version control.

### Esempio: Auto Resize Instagram

```
BLOCK 1: Input (image)
BLOCK 2: Resize 1080×1080 feed
BLOCK 3: Resize 1080×1920 story
BLOCK 4: Export PNG @2x → /Social/Instagram/
```

## Cinque trigger

1. **Command:** `/resize-instagram` in ChatCanvas
2. **Button:** nella toolbar del progetto
3. **API:** CI/CD o script esterni
4. **Schedule:** batch notturni
5. **Conditional:** se aspect ratio > 1.5 → story branch

## Dove ho visto fallire (onestà)

- Skill senza Brand Kit → drift al 3° output
- Due CTA nel brief → layout clutter
- Testo «cotto» nell'immagine → Touch Edit non salva
- Skill troppo generico → ogni campagna richiede patch manuali

## Lovart nel loop

Exploration resta umana; **shipping settimanale** passa da Skill + ChatCanvas + Brand Kit + Touch Edit. MCoT aiuta a spezzare carousel multi-size in artboard separati.

## Confronto rapido

| Bisogno | Manuale | Custom Skill |
| --- | --- | --- |
| 15 varianti social | 2–3 ore | 5–10 min |
| Coerenza brand | dipende da memoria | Brand Kit locked |
| Modifica data CTA | spesso regen | Touch Edit |

## Formula

\[ \text{risparmio} = \frac{\text{varianti} \times \text{frequenza}}{\text{minuti skill}} \]

## Link interni

| Ancora | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| Touch Edit | /blog/touch-edit-best-practice-3-gestures-lovart |
| Registrazione | https://lovart.ai/signup |

## FAQ

### Serve saper programmare?

No per Visual Builder; sì per SDL avanzato.

### Skill sostituisce il designer?

No. Automatizza ripetizione; la direzione creativa resta umana.

### Quanti skill per team?

3–5 solidi > 30 fragili.

### Versioning?

SDL in git; Visual export/import JSON.

### Commercial use?

Secondo licenza Lovart; asset brand sempre review umana.

## Drill operativo 1: batch Instagram 15 varianti

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: batch Instagram 15 varianti.


## Drill operativo 2: resize story 9:16

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: resize story 9:16.


## Drill operativo 3: export client PDF

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: export client PDF.


## Drill operativo 4: Brand Kit drift fix

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Brand Kit drift fix.


## Drill operativo 5: Touch Edit data campagna

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Touch Edit data campagna.


## Drill operativo 6: multi-CTA clutter

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: multi-CTA clutter.


## Drill operativo 7: SDL version control

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: SDL version control.


## Drill operativo 8: schedule notturno batch

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: schedule notturno batch.


## Drill operativo 9: API trigger CI

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: API trigger CI.


## Drill operativo 10: carousel MCoT artboard

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: carousel MCoT artboard.


## Drill operativo 11: onboarding nuovo designer

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: onboarding nuovo designer.


## Drill operativo 12: audit skill mensile

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: audit skill mensile.


## Drill operativo 13: batch Instagram 15 varianti

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: batch Instagram 15 varianti.


## Drill operativo 14: resize story 9:16

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: resize story 9:16.


## Drill operativo 15: export client PDF

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: export client PDF.


## Drill operativo 16: Brand Kit drift fix

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Brand Kit drift fix.


## Drill operativo 17: Touch Edit data campagna

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Touch Edit data campagna.


## Drill operativo 18: multi-CTA clutter

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: multi-CTA clutter.


## Drill operativo 19: SDL version control

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: SDL version control.


## Drill operativo 20: schedule notturno batch

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: schedule notturno batch.


## Drill operativo 21: API trigger CI

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: API trigger CI.


## Drill operativo 22: carousel MCoT artboard

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: carousel MCoT artboard.


## Drill operativo 23: onboarding nuovo designer

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: onboarding nuovo designer.


## Drill operativo 24: audit skill mensile

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: audit skill mensile.


## Drill operativo 25: batch Instagram 15 varianti

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: batch Instagram 15 varianti.


## Drill operativo 26: resize story 9:16

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: resize story 9:16.


## Drill operativo 27: export client PDF

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: export client PDF.


## Drill operativo 28: Brand Kit drift fix

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Brand Kit drift fix.


## Drill operativo 29: Touch Edit data campagna

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Touch Edit data campagna.


## Drill operativo 30: multi-CTA clutter

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: multi-CTA clutter.


## Drill operativo 31: SDL version control

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: SDL version control.


## Drill operativo 32: schedule notturno batch

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: schedule notturno batch.


## Drill operativo 33: API trigger CI

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: API trigger CI.


## Drill operativo 34: carousel MCoT artboard

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: carousel MCoT artboard.


## Drill operativo 35: onboarding nuovo designer

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: onboarding nuovo designer.


## Drill operativo 36: audit skill mensile

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: audit skill mensile.


## Drill operativo 37: batch Instagram 15 varianti

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: batch Instagram 15 varianti.


## Drill operativo 38: resize story 9:16

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: resize story 9:16.


## Drill operativo 39: export client PDF

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: export client PDF.


## Drill operativo 40: Brand Kit drift fix

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Brand Kit drift fix.


## Drill operativo 41: Touch Edit data campagna

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: Touch Edit data campagna.


## Drill operativo 42: multi-CTA clutter

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: multi-CTA clutter.


## Drill operativo 43: SDL version control

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: SDL version control.


## Drill operativo 44: schedule notturno batch

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: schedule notturno batch.


## Drill operativo 45: API trigger CI

Ho iniziato volutamente con un brief sporco su custom skills lovart: due CTA, data vaga, canale non specificato. Il primo output era bello ma non diceva cosa doveva fare lo spettatore.

Dopo aver corretto solo la frase di lavoro, il secondo giro è stato nettamente più usabile. Il collo di bottiglia è spesso nel brief, non nel mito del modello.

### Cosa ho cambiato

Un solo CTA. Data leggibile. Divieto di loghi falsi. Crop canale esplicito. Testo modificabile dopo.

### Come ho chiuso in Lovart

Ho riformulato il brief in ChatCanvas, bloccato Brand Kit, generato tre direzioni, corretto data e pulsante con Touch Edit.

### Regola riutilizzabile

Se il collega elogia solo l'atmosfera ma non sa dire l'offerta, l'asset non è finito. Scenario del round: API trigger CI.


*Article for www.lovart.ai/blog 404 recovery. Part of i18n 404 recovery content cluster.*
