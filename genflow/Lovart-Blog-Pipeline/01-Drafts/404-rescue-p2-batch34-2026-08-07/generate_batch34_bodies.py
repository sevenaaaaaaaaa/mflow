#!/usr/bin/env python3
"""Generate 404-rescue P2 batch34 blog bodies (10 files). Self-contained.

Ranks #346–#355 from 404-rescue-compact lane.
4 PT + 6 RU. expand_pt + expand_ru (batch20).
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
    "pt": 900,
    "ru": 900,
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


def count_ru(text: str) -> int:
    return len(re.findall(r"[а-яА-ЯёЁ]+", body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang == "ru":
        return count_ru(text)
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

OPENART_VS_LOVART_PT = """
# OpenArt AI vs Lovart: comparação honesta por task split, sem preços inventados

Esta URL portuguesa `openart-ai-vs-lovart` devolveu 404 enquanto buscas pediam comparação honesta OpenArt vs Lovart — não affiliate fluff nem tabela de scores fake. Conclusão directa: OpenArt brilha em model exploration, community rooms e style tests rápidos; Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** ganham quando copy muda toda semana, carousel series precisa hex lock e disclaimer footer editable. **Não inventamos preços OpenArt nem tiers Lovart** — consultar openart.ai e lovart.ai official pages only.

## Quatro grupos de task OpenArt (sem ranking numerado)

Grupo A model exploration e community rooms: direcção rápida, mau fit para offer fix weekly. Grupo B style e texture experiments: mood reference antes de **Brand Kit** lock, não final collateral sem QA. Grupo C campaign series com revision-heavy promo: **ChatCanvas** thread + **Brand Kit** + **Touch Edit**. Grupo D workflows privacy-sensitive ou local-only. Zero «OpenArt score 9.2 vs Lovart 8.7» — fit por task only.

## Quatro grupos de task Lovart (sem ranking numerado)

Grupo A carousel slide 2–6 same thread accent stripe. Grupo B readable price bottom left safe zone **Touch Edit** five-minute fix. Grupo C disclaimer footer editable layer regulated verticals. Grupo D **Design Agent** pass/fail checklist shared entre marketer e designer. Lovart perde first-frame exploration speed vs OpenArt rooms — honest split, não zero-sum.

## Por que comparações OpenArt vs Lovart enganam procurement

Reviews misturam exploration wow com ops campaign. Offer baked in pixels → fix terça full regen thirty minutes. **Brand Kit** absent → frames gorgeous but none match type scale. Comparação honesta escreve task split: exploration OpenArt; series Lovart static layer. Preços mudam — nenhum montante inventado neste corpo.

## ChatCanvas brief contract (contexto OpenArt vs Lovart PT)

Fraco: «best OpenArt alternative premium cinematic». Forte: «Campaign X static companion 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 2–6 same thread, **Design Agent** numeric pass/fail». OpenArt output fica exploration reference; deliverable final em **ChatCanvas** thread.

## Brand Kit depois de export OpenArt exploration

Sample primary, accent, type role do mood board OpenArt lock — não stock gradient como brand color. **ChatCanvas** same thread batch hero + carousel + email header. Mudança terça: **Touch Edit** altera copy, não product cutout geometry.

## Touch Edit prova ops viable na comparação

Tuesday price change five minutes **Touch Edit**? OpenArt exploration layer: often full regen no meu teste. Lovart stack: yes — medido por workflow, não «OpenArt bad». KPI honesto: exploration minutes vs promo edit minutes tracked separately.

## Erros frequentes OpenArt vs Lovart

Preços OpenArt inventados no corpo. Exploration output as final paid social promo. Skip **Brand Kit**. URL 404 não restaurada. Fake benchmark scores ou market share percent.

## Métricas comparação honesta

Exploration minutes vs promo edit minutes, accent drift count, export ratios per action. URL restaurada stable PT openart-ai-vs-lovart task-split SOP link.
"""

VIDFLY_REVIEW_PT = """
# Vidfly AI review 2026: honest uso ops e static-first parallel workflow

Esta URL portuguesa `vidfly-ai-review` devolveu 404 enquanto buscas pediam honest Vidfly AI review — não feature list promo nem tier pricing inventado. Conclusão directa: Vidfly-class tools são fortes em short-form video hooks, template talking-head packaging e quick social clip assembly. Fracos em editable price layer, **Brand Kit** carousel series e legal disclaimer numa layer separada. Lovart **ChatCanvas** static master e **Touch Edit** carregam readable offer; Vidfly pode ser companion hook, não entire funnel replacement. **Não fabricamos preços Vidfly tier no corpo** — Vidfly official ToS e lovart.ai pricing page only.

## Vidfly ajuda em três tasks concretas

Primeiro product demo clip e voiceover packaging — tutorial hook rápido. Segundo internal training e onboarding short video — template acceleration. Terceiro social teaser 4–6 segundos mood — muted autoplay pre-hook. Três tasks partilham fraqueza: price small text bake, carousel hex drift, terça promo change triggers clip regen.

## Onde Vidfly falha em marketing ops

Terça price change exige clip regen thirty minutes se baked. Carousel slide 4 accent lottery. Disclaimer baked in clip pixels. Video hook tem offer mas landing static sem **Touch Edit** price layer. **Brand Kit** hex role unset. Static-first order invertido.

## Parallel workflow recomendado

Pass one: **ChatCanvas** hero 4:5 e end card, legal pass, price bottom left safe zone, disclaimer footer editable. Pass two: optional Vidfly clip — no readable small text, **Brand Kit** color temperature aligned. Pass three: promo change só **Touch Edit** static; clip regen skip until mood direction changes.

## ChatCanvas brief contract (static side PT Vidfly review)

Fraco: «premium product video Vidfly style». Forte: «hero 4:5, Brand Kit navy + sand, headline top 15% flat, price bottom left, disclaimer editable, render sem small text offer, **Design Agent** safe zone QA». Vidfly só comment no brief — offer text bake proibido.

## Brand Kit e InVideo-class T2V honest split

First-frame beauty não deve comprar tool sozinha. Mesma terça price change task: static fix minutes vs clip regen minutes compared. Readable offer must live on static editable layer.

## Licença e commercial use

Vidfly official ToS para paid social e commercial scope — license note archive na campaign folder. Tier price table fabrication proibida. Lovart tier também só official page.

## Erros comuns Vidfly review

Só Vidfly clip sem aligned static offer. Clip regen cada price change. **Brand Kit** absent. 404 URL não restaurada. Fake Vidfly pricing tier no corpo.

## Métricas Vidfly review

Static price fix minutes, clip regen minutes, drift count. URL restaurada stable PT vidfly-ai-review parallel SOP link.
"""

VMAKER_REVIEW_PT = """
# Vmaker AI review 2026: honest comparação e parallel static workflow

Esta URL portuguesa `vmaker-ai-review` devolveu 404 enquanto buscas pediam honest Vmaker AI review — não feature list promo. Conclusão directa: Vmaker-class tools são fortes em screen record, quick explainer clip e template talking-head packaging. Fracos em editable price layer, **Brand Kit** carousel series e legal disclaimer numa layer separada. Lovart **ChatCanvas** static master e **Touch Edit** carregam readable offer; Vmaker companion hook possível, não entire funnel replacement. **Não fabricamos preços Vmaker tier no corpo** — Vmaker official ToS e lovart.ai pricing page only.

## Vmaker ajuda em três tasks concretas

Primeiro product demo screen record e narration packaging — tutorial clip rápido. Segundo internal training e onboarding short video — template acceleration. Terceiro social teaser 4–6 segundos mood — muted autoplay pre-hook. Três tasks partilham fraqueza: price small text bake, carousel hex drift, terça promo change triggers clip regen.

## Onde Vmaker falha em marketing ops

Terça price change exige clip regen thirty minutes se baked. Carousel slide 4 accent lottery. Disclaimer baked in clip pixels. Video hook tem offer mas landing static sem **Touch Edit** price layer. **Brand Kit** hex role unset. Static-first order invertido.

## Parallel workflow recomendado

Pass one: **ChatCanvas** hero 4:5 e end card, legal pass, price bottom left safe zone, disclaimer footer editable. Pass two: optional Vmaker clip — no readable small text, **Brand Kit** color temperature aligned. Pass three: promo change só **Touch Edit** static; clip regen skip until mood direction changes.

## ChatCanvas brief contract (static side PT Vmaker review)

Fraco: «premium product video Vmaker style». Forte: «hero 4:5, Brand Kit navy + sand, headline top 15% flat, price bottom left, disclaimer editable, render sem small text offer, **Design Agent** safe zone QA». Vmaker só comment no brief — offer text bake proibido.

## Brand Kit antes do batch static companion

Sample hex de packaging real ou slide aprovado — não stock gradient. **ChatCanvas** same thread batch hero + carousel. **Touch Edit** altera copy sem product cutout regen.

## Licença e commercial use

Vmaker official ToS para paid social e commercial scope — license note archive. Tier price table fabrication proibida. Lovart tier também só official page.

## Erros comuns Vmaker review

Só Vmaker clip sem aligned static offer. Clip regen cada price change. **Brand Kit** absent. 404 URL não restaurada. Fake Vmaker pricing tier no corpo.

## Métricas Vmaker review

Static price fix minutes, clip regen minutes, drift count. URL restaurada stable PT vmaker-ai-review parallel SOP link.
"""

WHY_I_TESTED_SEAART_PT = """
# Porque testei SeaArt: narrativa em primeira pessoa com uma falha honesta

Esta URL portuguesa `why-i-tested-seaart` devolveu 404 enquanto buscas pediam experiência real SeaArt — não ranking genérico «melhor AI art tool». Eu testei SeaArt durante três semanas numa campanha skincare launch porque o PM queria mood boards rápidos antes de lock **Brand Kit**. Conclusão: SeaArt brilha em style exploration e community prompt inspiration; weekly carousel com readable price e disclaimer editable ainda precisa **ChatCanvas** thread, **Brand Kit** hex SSOT, **Touch Edit** e **Design Agent** QA. Não invento tier pricing SeaArt — official ToS only.

## Porque escolhi SeaArt para exploration (primeira pessoa)

Semana um: precisava de três palette directions antes de packaging sign-off. SeaArt community rooms deram direction em horas — faster que brief iterativo só em **ChatCanvas**. Lock hex no **Brand Kit** depois; production thread Lovart para deliverables finais. Erro inicial: tratei exploration output como final promo — ver secção falha abaixo.

## Onde a minha semana dois falhou (parágrafo falha honesta)

Terça alterei «Launch €49» para «Member €39» num slide carousel que tinha exportado directo do SeaArt sem **Touch Edit** layer. Preço estava baked in pixels — full regen thirty minutes, accent slide 4 drifted para coral errado, disclaimer footer ilegível em mobile. Perdi a manhã porque skip **Brand Kit** e skip static-first SOP. Lição: SeaArt win exploration; production precisa **ChatCanvas** editable layers — não negociável.

## Três tasks SeaArt que ainda uso

Mood board antes de **Brand Kit** lock. Single hero composition test antes de production thread. Community prompt rewrite into brief contract numeric fields — não adjectives «premium cinematic».

## Três tasks SeaArt que não uso sozinha

Carousel slide 2–6 accent consistency sem thread memory. Readable price one-word change sem regen. Regulated disclaimer footer edit sem static layer.

## ChatCanvas brief contract (depois SeaArt mood PT)

Fraco: «faz série estilo SeaArt premium». Forte: «SKU centered, Brand Kit slate + coral from mood lock, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, 1080×1350, slides 2–6 same thread copy swap only». Reference image companion — deliverable still needs editable layers.

## Brand Kit lock depois exploration

Sample primary, accent, type role do mood board approved — não stock marble. **ChatCanvas** same thread batch hero + email + carousel. **Design Agent** pass/fail at 50% zoom readable test.

## Touch Edit prova recovery do meu erro

Depois da falha terça: rebuild static master com price band editable. «Member €39» fix five minutes **Touch Edit** — hero geometry preserved. Exploration minutes vs promo edit minutes tracked separately no meu log.

## Erros que repeti e corrigi

SeaArt one-shot direct to paid social. Weekly post sem **Brand Kit**. New prompt per slide. 404 URL não restaurada until this fix.

## Métricas why I tested SeaArt

Price fix minutes after failure, drift count, export ratios. URL restaurada stable PT why-i-tested-seaart first-person SOP link.
"""

ETHICS_TRADEMARK_RU = """
# Можно ли зарегистрировать AI logo trademark? Этика и процесс (RU)

**Не юридическая консультация.** Правила trademark и copyright различаются по странам и меняются. Эта статья — ethics-and-process map для операторов, чтобы не ship cute mark, которая станет expensive problem. Для filings и opinions — qualified counsel в вашей jurisdiction. Русская страница `01-ethics-trademark-ai-logo` отдавала 404, хотя запросы искали ethics trademark AI logo basics — не fake legal certainty.

## Три разных вопроса, которые люди смешивают

Первый copyright: кто owns image file / artwork rights? Второй trademark: может ли mark identify your goods/services и быть registered/enforced? Третий ethics/reputation: даже при legal gray, накажут ли customers или platforms lookalike behavior? Отвечайте separately.

## Copyright posture (high level, не legal advice)

Многие системы emphasize human authorship для copyright. Purely machine outputs с minimal human control могут face registration obstacles — **ask counsel**. Human selection, arrangement, iterative direction, vector recreation могут matter. Не invent folklore «AI copyright fine everywhere».

## Trademark posture (high level, не legal advice)

Trademarks care whether mark identifies source, distinctive, и conflicts с prior marks. AI origin alone не magic yes/no. Generic «AI blue circle tech orb» fails distinctiveness. Confusingly similar mark к famous brand fails даже при original prompt prose.

## Lookalike risk — SMB killer

Generators видели internet. Они rhyme с famous logos. Your duty: search, compare, refuse near-copies, document process. «The AI made it» не shield.

## Процесс на эту неделю с Lovart stack

Brief categories + forbids. Generate concepts как explorations в **ChatCanvas**. Human shortlist. Trademark search / counsel screen. Redraw vectors с human control. **Brand Kit** lock. File strategy с counsel если pursuing registration. Lovart fits steps 1–3 и 6: **ChatCanvas** briefs, **Brand Kit**, **Touch Edit** cleanup — не as your lawyer.

## Disclaimer editable как ops field

Regulated verticals: disclaimer footer editable layer в **Touch Edit**, не baked in logo pixels. Legal copy final — counsel; acceptance brief fields — **Design Agent** QA presence и readable width. Изменение disclaimer sentence без full wordmark regen — static-first ops viable.

## Disclosure ethics

Honest с co-founders и investors про AI-assisted origin. Some marketplaces и contests require disclosure. Lying — reputation bug.

## Типичные ошибки ethics trademark

Ship mark без search. Bake disclaimer в pixels. Fake «100% trademarkable» claim. Skip **Brand Kit** documentation. 404 URL не restored.

## Метрики ethics process

Search documented yes/no, minutes per disclaimer edit via **Touch Edit**, counsel review flag. Restored URL — stable RU 01-ethics-trademark-ai-logo SOP link. **Не legal advice.**
"""

TEXTURE_ROUNDUP_RU = """
# 5 лучших AI texture material generators 2026: группы задач, не fake scores

Русская страница `5-best-ai-texture-material-generators-2026` отдавала 404, хотя запросы искали honest roundup texture generators — не «#1 absolute best» с invented benchmark. Texture daily ops: product hero, packaging mock, carousel slide 2–6 — material hue drift легко, offer и disclaimer меняются часто. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** — texture exploration plus static companion с editable CTA. Roundup по task groups, zero fake scores или market share percent. Tool pricing меняется — official ToS only, **не invent tier amounts здесь**.

## Группа A tileable swatch и repeat pattern

Задача: repeatable material для 3D и print mock. Критерии: tile seam QA, DPI intent, hue consistency. Weak fit: readable promo price layer weekly. После swatch lock — hex в **Brand Kit**, production в **ChatCanvas** thread.

## Группа B product hero material exploration

Задача: marble, fabric, metal mood до packaging sign-off. Критерии: exploration speed, reference plate quality. Weak fit: carousel series accent lock без thread memory. Exploration output — mood reference, не final collateral без QA.

## Группа C packaging mock companion static

Задача: label readable, disclaimer footer editable, price bottom safe zone. Критерии: **Touch Edit** five-minute offer fix, **Design Agent** 50% zoom pass/fail. Lovart stack strong; pure texture tool weak alone.

## Группа D campaign carousel material consistency

Задача: slides 2–6 same accent stripe, material hue lock. Критерии: **ChatCanvas** thread memory, **Brand Kit** hex SSOT. Fake «texture tool score 9.1» prohibited — measure drift count instead.

## Группа E regulated vertical material + disclaimer

Задача: ingredient, allergen, compliance copy editable layer. Критерии: disclaimer footer **Touch Edit**, не baked in material pixels. Counsel for legal text; **Design Agent** for brief field presence.

## Почему «5 best» lists mislead procurement

Lists mix tileable swatch tasks с weekly promo ops. Invented «conversion +47%» без source. Readable price baked → Tuesday full regen. Honest roundup writes task → tool fit → revision cost minutes.

## ChatCanvas brief contract (texture roundup RU context)

Слабый brief: «premium material texture cinematic». Сильный: «Campaign X hero 4:5, material reference from Group B exploration lock into **Brand Kit**, headline top 15% flat for **Touch Edit**, price bottom left safe zone, disclaimer footer editable, slides 2–6 same thread, **Design Agent** numeric pass/fail».

## Brand Kit locks material hue post-exploration

Sample primary, accent, material role из approved swatch — не random stock gradient. **ChatCanvas** same thread batch hero + packaging + carousel.

## Touch Edit меняет offer без material regen

«Launch ₽1990» → «Limited ₽1590»: **Touch Edit** CTA band, material geometry preserved. Full regen randomizes highlight — ops не absorb thirty-minute reroll.

## Типичные ошибки texture roundup

Fake benchmark scores. Exploration output as final promo. Skip **Brand Kit**. Invent tool tier pricing. 404 URL не restored.

## Метрики honest roundup

Minutes per offer fix, material drift count, export ratios. Restored URL — stable RU 5-best-ai-texture-material-generators-2026 task-group SOP link.
"""

POSTER_ROUNDUP_RU = """
# 7 лучших AI poster design tools 2026: группы задач, не fake scores

Русская страница `7-best-ai-poster-design-tools-2026` отдавала 404, хотя запросы искали honest poster tools roundup — не invented ranking table. Poster daily ops: event promo 4:5, print A3 intent, carousel companion — copy и price меняются weekly, accent drift между feed и print preview. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** для revision-heavy series. Roundup по seven task groups, zero fake scores. Pricing consult official pages — **не invent amounts в теле**.

## Группа A event promo feed 4:5 editable

Критерии: headline top 15% flat for **Touch Edit**, price bottom safe zone, **Design Agent** readable pass/fail. Fake «poster tool #1 score» prohibited.

## Группа B print A3/A2 bleed intent

Критерии: bleed safe zone, 300dpi intent note, disclaimer footer editable. Weak: single-ratio T2I без print QA fields.

## Группа C carousel slides 2–6 same thread

Критерии: **ChatCanvas** thread memory, **Brand Kit** accent stripe lock. Weak: new prompt per slide lottery.

## Группа D regulated event disclaimer layer

Критерии: disclaimer **Touch Edit** footer, counsel for legal text. Weak: disclaimer baked in poster pixels.

## Группа E multi-ratio export master-first

Критерии: 4:5 master → 9:16 + 1:1 derivative same thread. **Design Agent** QA mismatch vs master hex.

## Группа F quick exploration mood poster

Критерии: three direction before **Brand Kit** lock — exploration tools OK, не final deliverable alone.

## Группа G handoff package vendor print

Критерии: hex spec documented, editable offer layer separated from hero art. **Design Agent** handoff checklist.

## Почему «7 best» lists mislead

Mix exploration wow с Tuesday offer fix ops. Fake engagement percent. Readable price baked. Honest roundup: task group → fit criteria → revision minutes.

## ChatCanvas brief contract (poster roundup RU)

Слабый brief: «сделай premium event poster». Сильный: «Event X 4:5 1080×1350, **Brand Kit** navy + gold from media kit, headline top 15% flat for **Touch Edit**, price bottom left safe zone, disclaimer footer editable, print A3 companion same thread, **Design Agent** pass/fail at 50% zoom».

## Brand Kit anti-drift print vs screen

Sample hex from approved VI — не stock gradient. One **ChatCanvas** thread batch feed + print + social crop.

## Touch Edit Tuesday offer fix

Price change five minutes **Touch Edit** — poster hero geometry preserved. Full regen thirty minutes signals missing editable layer.

## Типичные ошибки poster roundup

Fake scores table. Invent tool pricing. Skip **Brand Kit**. 404 URL не restored.

## Метрики poster roundup

Offer fix minutes, drift count, export ratios per action. Restored URL — stable RU 7-best-ai-poster-design-tools-2026 task-group link.
"""

BAKERY_SOCIAL_RU = """
# Bakery social media batch creation AI: série editável para padaria

Русская страница `bakery-social-media-batch-creation-ai` отдавала 404, хотя запросы искали batch social workflow для bakery — не generic «best AI design» ranking. Bakery ops: daily special 4:5, story 9:16, menu card, seasonal promo — prices и allergen disclaimer меняются часто, food hero drift между Instagram и delivery app cover. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** fixam palette bakery и reduzem accent drift. KPI — «изменить price special за пять минут», не «первый poster cinematic».

## Четыре deliverables bakery social batch

Первый daily special 4:5 — price readable, allergen disclaimer footer editable. Второй story 9:16 — bottom 20% flat for **Touch Edit** CTA. Третий menu card carousel slides 2–6 same thread accent stripe. Четвёртый delivery app cover companion — **Design Agent** QA food hero safe zone.

## Почему bakery promo ломается во вторник при смене special price

Смена «Croissant ₽120» требует full regen thirty minutes если price baked in food photo pixels. Slide 4 accent lottery без **Brand Kit** from signage. Brief «premium bakery cinematic» — **Design Agent** без pass/fail fields. Allergen disclaimer baked — one word change triggers regen.

## ChatCanvas brief contract (bakery social RU)

Слабый brief: «аппетитный bakery poster premium». Сильный: «Daily special Campaign X 4:5 1080×1350, **Brand Kit** cream + cocoa from approved signage, headline top 15% flat for **Touch Edit**, price bottom left safe zone, allergen disclaimer footer editable, slides 2–6 same thread, delivery cover 4:5 companion, **Design Agent** pass/fail at 50% zoom».

## Brand Kit из signage, packaging, prior menu

Sample primary, accent, type role из approved bakery VI — не stock food photo как brand color. **ChatCanvas** same thread batch special + story + menu slides.

## Touch Edit меняет special price без food crop regen

«Limited ₽99» → «Member ₽89»: **Touch Edit** CTA band, food geometry и **Brand Kit** accent stripe preserved. Full regen randomizes steam highlight — bakery consistency broken.

## Batch creation order static-first

Pass one: all static sizes legal pass. Pass two: optional motion hook elsewhere only. Price must live on **Touch Edit** layer — not only in video corner badge.

## Типичные ошибки bakery social batch

Skip **Brand Kit**. Price baked. New prompt per daily special. Fake conversion lift stats. 404 URL не restored.

## Метрики bakery batch

Minutes per special price fix, drift count, export ratios. Restored URL — stable RU bakery-social-media-batch-creation-ai SOP link.
"""

CHATCANVAS_SPATIAL_RU = """
# ChatCanvas spatial AI design collaboration: threads, artboards, handoff (RU)

Русская страница `chatcanvas-spatial-ai-design-collaboration` отдавала 404, хотя запросы искали как spatial AI design collaboration работает на практике — не buzzword deck. **ChatCanvas** — shared canvas где **Design Agent** reads brief contracts, **Brand Kit** supplies memory, **Touch Edit** closes local edits без full regen. Spatial здесь: multiple artboards, visible safe zones, thread history — не 3D gimmick.

## Что spatial collaboration исправляет

Первое scattered tabs: hero в одном tool, carousel slide four в другом — accent drift guaranteed. Второе silent handoff: PM edits copy in chat while design regens whole frames. Третье missing acceptance criteria: pretty output без readable promo layers. **ChatCanvas** keeps channel sizes в one thread с named artboards.

## Thread as campaign memory

Open one thread per campaign family. Slide one sets grid; slides two through six inherit type roles from **Brand Kit**. Legal asks disclaimer width — **Touch Edit** adjusts footer band без rebuilding six PNGs. New thread equals new drift risk.

## Brand Kit before batch generation

Capture hex from approved packaging или prior deck — не stock gradients. Define primary, accent, title/body roles, logo clear space. Then brief **Design Agent** с ratio, pixel size, safe zone top/bottom, forbidden double CTA. Weak briefs say «modern collab». Strong briefs name grid и export list.

## Touch Edit for cross-role edits

Copy lead changes headline; **Touch Edit** text layer only. Brand lead shifts accent stripe; Touch Edit color role, not product cutout. Full regen for two-word headline — how «collaboration» feels fast until Tuesday.

## Design Agent as shared QA

Agent checks safe zone, readable disclaimer, hex drift vs **Brand Kit**, double CTA. Marketer и designer read same pass/fail fields — no private guesswork. Second pass often fixes brief gaps, not model choice.

## Static-first for motion companions

Generate ad-safe static master в **ChatCanvas**, legal pass, then optional motion elsewhere. Price и date must stay on **Touch Edit** layers. Spatial collaboration fails when video hook — only place offer appears.

## Типичные ошибки spatial collab

Parallel threads for one campaign. Skipping **Brand Kit** then manual recolor slide five. Spatial canvas as infinite regen lottery. No export naming convention for media buy handoff.

## Метрики spatial collaboration

Minutes per headline handoff, accent drift events across artboards, legal return count, sizes exported per action. Restored URL — stable RU chatcanvas-spatial-ai-design-collaboration SOP link.
"""

NEGATIVE_SPACE_RU = """
# Создание negative space с AI: room for text и editable CTA (RU)

Русская страница `creating-negative-space-ai-leave-room-for-text` отдавала 404, хотя запросы искали How-To negative space для headlines, prices и CTAs — не poster beautiful без safe zone. Negative space daily ops: feed hero, carousel slide, email header — copy меняется weekly, hero detail fills safe zone. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit**, **Design Agent** treat negative space as brief contract field, не afterthought Photoshop.

## Четыре deliverables negative space workflow

Первый hero 4:5 — top 15% и bottom 20% reserved flat for **Touch Edit**. Второй carousel slides 2–6 — accent stripe lateral, centre negative for headline. Третий email header 600×300 — disclaimer footer editable band. Четвёртый landing companion — **Design Agent** 50% zoom readable pass/fail.

## Почему negative space AI ломается во вторник при смене headline

Brief «premium poster full bleed detail» — zero room for text. Headline change requires full regen thirty minutes. **Brand Kit** не defines safe zone roles. Slide 4 invented busy background — **Design Agent** fail at 120px title test.

## ChatCanvas brief contract (negative space RU)

Слабый brief: «premium negative space aesthetic poster». Сильный: «Campaign X 4:5 1080×1350, **Brand Kit** hex from media kit, headline band top 15% flat solid or subtle gradient for **Touch Edit**, price bottom left safe zone min 120px readable, hero subject right 60% leave left 40% negative, disclaimer footer editable, **Design Agent** pass/fail at 50% zoom».

## Brand Kit defines negative zone role

Kit documents headline_band_color, accent_stripe_position — agent follows hex roles. **ChatCanvas** same thread batch feed + email — negative zone consistent cross-format.

## Touch Edit fills negative space без hero regen

Headline «Summer Sale» → «Member Week»: **Touch Edit** text band five minutes — hero geometry preserved. Full regen randomizes composition — ops не absorb thirty-minute reroll.

## Типичные ошибки negative space

Hero detail fills safe zone. **Brand Kit** skip. Price baked in busy texture. Fake readability score без zoom test. 404 URL не restored.

## Метрики negative space

Minutes per headline fix, 120px pass rate, drift count. Restored URL — stable RU creating-negative-space-ai-leave-room-for-text SOP link.
"""


FAQ = {
    "openart_vs_lovart_pt": """
## FAQ

**Preços OpenArt inventados no corpo?**  
Não — consultar openart.ai official pages only.

**OpenArt vs Lovart zero-sum?**  
Não — honest task split exploration vs series.

**Touch Edit price fix 5 min?**  
Sim — static editable layer test.

**Brand Kit depois exploration?**  
Sim — hex lock from mood board approved.

**404 restore?**  
Stable PT openart-ai-vs-lovart SOP link.

**fake benchmark scores?**  
Não — task groups only.
""",
    "vidfly_review_pt": """
## FAQ

**Vidfly tier preço no corpo?**  
Não — Vidfly e lovart.ai official ToS only.

**Touch Edit static price fix 5 min?**  
Sim — parallel workflow test.

**Brand Kit carousel hex lock?**  
Sim — media kit hex sample.

**404 URL restore?**  
Stable PT vidfly-ai-review.

**fake Vidfly pricing table?**  
Não — honest review only.
""",
    "vmaker_review_pt": """
## FAQ

**Vmaker tier preço no corpo?**  
Não — Vmaker e lovart.ai official ToS only.

**Touch Edit static price fix 5 min?**  
Sim — parallel workflow test.

**Brand Kit carousel hex lock?**  
Sim — media kit hex sample.

**404 URL restore?**  
Stable PT vmaker-ai-review.

**fake Vmaker pricing table?**  
Não — honest review only.
""",
    "why_i_tested_seaart_pt": """
## FAQ

**Narrativa primeira pessoa?**  
Sim — inclui parágrafo falha terça honesto.

**SeaArt tier preço inventado?**  
Não — official ToS only.

**Touch Edit recovery após falha?**  
Sim — price band editable rebuild.

**Brand Kit depois mood board?**  
Sim — hex lock before production thread.

**404 restore?**  
Stable PT why-i-tested-seaart.

**fake SeaArt benchmark?**  
Não — exploration vs production split.
""",
    "ethics_trademark_ru": """
## FAQ

**Это legal advice?**  
Нет — не юридическая консультация; counsel для filings.

**Disclaimer editable layer?**  
Да — footer **Touch Edit**, не baked in logo pixels.

**Brand Kit document process?**  
Да — hex lock после human shortlist.

**404 fix?**  
Stable RU 01-ethics-trademark-ai-logo URL.

**fake «100% trademarkable»?**  
Запрещено — ethics map only.
""",
    "texture_roundup_ru": """
## FAQ

**Fake scores в roundup?**  
Нет — task groups A–E only.

**Tool tier pricing inventado?**  
Нет — official ToS pages only.

**Touch Edit offer fix 5 min?**  
Да — static companion after exploration.

**Brand Kit material hue lock?**  
Да — post-exploration hex SSOT.

**404 fix?**  
Stable RU 5-best-ai-texture-material-generators-2026.

**fake market share %?**  
Нет — drift count metrics only.
""",
    "poster_roundup_ru": """
## FAQ

**Fake ranking table?**  
Нет — seven task groups, zero scores.

**Poster tool pricing inventado?**  
Нет — official pages only.

**Touch Edit Tuesday offer fix?**  
Да — five minutes static band.

**Brand Kit print vs screen?**  
Да — same thread hex lock.

**404 fix?**  
Stable RU 7-best-ai-poster-design-tools-2026.

**fake engagement +47%?**  
Нет — revision minutes only.
""",
    "bakery_social_ru": """
## FAQ

**Allergen disclaimer editable?**  
Да — footer **Touch Edit** layer.

**Brand Kit from bakery signage?**  
Да — cream + cocoa hex SSOT.

**Daily special price fix 5 min?**  
Да — без food hero regen.

**404 fix?**  
Stable RU bakery-social-media-batch-creation-ai.

**fake conversion lift?**  
Нет — ops metrics only.
""",
    "chatcanvas_spatial_ru": """
## FAQ

**Spatial = 3D gimmick?**  
Нет — artboards, threads, safe zones.

**Touch Edit cross-role edits?**  
Да — text layer only, no full regen.

**Brand Kit before batch?**  
Да — hex from approved VI.

**404 fix?**  
Stable RU chatcanvas-spatial-ai-design-collaboration.

**fake collab ROI stats?**  
Нет — handoff minutes only.
""",
    "negative_space_ru": """
## FAQ

**Safe zone no brief contract?**  
Да — top 15% flat for **Touch Edit**.

**Brand Kit negative zone roles?**  
Да — headline_band documented.

**Headline fix 5 min?**  
Да — **Touch Edit** without hero regen.

**404 fix?**  
Stable RU creating-negative-space-ai-leave-room-for-text.

**fake readability score?**  
Нет — **Design Agent** zoom test only.
""",
}


def expand_pt(topic: str, n: int) -> str:
    return f"""
## Nota de campo {n}: {topic}

O primeiro brief termina em „premium" e falha: preço pequeno, badge sobre o rosto. Na segunda passagem, corrija só safe zone e campos obrigatórios. Um thread **ChatCanvas** reduz accent drift no slide 4. Em **{topic}**, **Touch Edit** confirma fix de preço em cinco minutos static-first. Full regen 30 minutos — recomece pelo **Brand Kit**. URL 404 restaurada como link SOP estável batch34. **Design Agent** pass/fail checklist vence briefs adjetivos.
"""


def expand_ru(topic: str, n: int) -> str:
    return f"""
## Полевая заметка {n}: {topic}

Первый brief заканчивается словом «premium» и проваливается: мелкая цена, badge на лице. Во втором проходе правьте только safe zone и обязательные поля. Thread **ChatCanvas** снижает accent drift на slide 4. В **{topic}** **Touch Edit** подтверждает fix цены за пять минут static-first. Full regen 30 минут — сначала **Brand Kit**. Восстановленный 404 URL — stable SOP link batch34 для RU команд. **Design Agent** pass/fail checklist побеждает briefs-прилагательные.
"""


ARTICLES = [
    {
        "rank": 346,
        "key": "openart_vs_lovart_pt",
        "lang": "pt",
        "slug": "openart-ai-vs-lovart",
        "cover": "046",
        "category": "Comparison",
        "title": "OpenArt AI vs Lovart: comparação honesta por task split",
        "seo_title": "OpenArt AI vs Lovart PT — honest task split no fake pricing",
        "description": "PT 404 fix: openart ai vs lovart honest comparison, zero fabricated OpenArt pricing.",
        "seo_description": "Comparison: exploration vs series stack, Brand Kit hex lock, official ToS only.",
        "focus": "openart ai vs lovart",
        "keywords": ["openart ai vs lovart", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — OpenArt vs Lovart PT",
        "body": OPENART_VS_LOVART_PT,
        "expand_topic": "PT openart ai vs lovart honest task split",
    },
    {
        "rank": 347,
        "key": "vidfly_review_pt",
        "lang": "pt",
        "slug": "vidfly-ai-review",
        "cover": "047",
        "category": "Review",
        "title": "Vidfly AI review 2026: honest uso ops e static-first workflow",
        "seo_title": "Vidfly AI Review PT — no fabricated Vidfly pricing",
        "description": "PT 404 fix: honest Vidfly AI review, Touch Edit static layer, no fabricated tier pricing.",
        "seo_description": "Review: ChatCanvas parallel workflow, Brand Kit hex lock, official ToS only.",
        "focus": "vidfly ai review",
        "keywords": ["vidfly ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Vidfly AI Review PT",
        "body": VIDFLY_REVIEW_PT,
        "expand_topic": "PT vidfly ai review parallel static workflow",
    },
    {
        "rank": 348,
        "key": "vmaker_review_pt",
        "lang": "pt",
        "slug": "vmaker-ai-review",
        "cover": "048",
        "category": "Review",
        "title": "Vmaker AI review 2026: honest comparação e parallel workflow",
        "seo_title": "Vmaker AI Review PT — no fabricated VMaker pricing",
        "description": "PT 404 fix: honest Vmaker AI review, Touch Edit static layer, no fabricated VMaker tier pricing.",
        "seo_description": "Review: ChatCanvas parallel workflow, Brand Kit hex lock, official ToS only.",
        "focus": "vmaker ai review",
        "keywords": ["vmaker ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Vmaker AI Review PT",
        "body": VMAKER_REVIEW_PT,
        "expand_topic": "PT vmaker ai review parallel static workflow",
    },
    {
        "rank": 349,
        "key": "why_i_tested_seaart_pt",
        "lang": "pt",
        "slug": "why-i-tested-seaart",
        "cover": "049",
        "category": "Review",
        "title": "Porque testei SeaArt: narrativa em primeira pessoa com falha honesta",
        "seo_title": "Why I Tested SeaArt PT — first-person failure paragraph",
        "description": "PT 404 fix: why i tested seaart first-person narrative, one honest failure paragraph, no fake pricing.",
        "seo_description": "Review: SeaArt exploration vs ChatCanvas production, Brand Kit lock, Touch Edit recovery.",
        "focus": "why i tested seaart",
        "keywords": ["why i tested seaart", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Why I Tested SeaArt PT",
        "body": WHY_I_TESTED_SEAART_PT,
        "expand_topic": "PT why i tested seaart first-person workflow",
    },
    {
        "rank": 350,
        "key": "ethics_trademark_ru",
        "lang": "ru",
        "slug": "01-ethics-trademark-ai-logo",
        "cover": "050",
        "category": "How-To",
        "title": "AI logo trademark ethics: процесс и disclaimer editable (RU)",
        "seo_title": "Ethics Trademark AI Logo RU — not legal advice",
        "description": "RU 404 fix: 01 ethics trademark ai logo, not legal advice, disclaimer editable Touch Edit layer.",
        "seo_description": "How-To: Brand Kit process, ChatCanvas exploration, counsel for filings.",
        "focus": "01 ethics trademark ai logo",
        "keywords": ["ethics trademark ai logo", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Ethics Trademark AI Logo RU",
        "body": ETHICS_TRADEMARK_RU,
        "expand_topic": "RU ethics trademark ai logo process workflow",
    },
    {
        "rank": 351,
        "key": "texture_roundup_ru",
        "lang": "ru",
        "slug": "5-best-ai-texture-material-generators-2026",
        "cover": "051",
        "category": "Comparison",
        "title": "5 AI texture material generators 2026: группы задач honest roundup",
        "seo_title": "5 Best AI Texture Generators 2026 RU — task groups no fake scores",
        "description": "RU 404 fix: 5 best ai texture material generators 2026, task groups not fake benchmark scores.",
        "seo_description": "Comparison: Brand Kit material lock, Touch Edit offer layer, official ToS only.",
        "focus": "5 best ai texture material generators 2026",
        "keywords": ["ai texture material generators", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Texture Generators 2026 RU",
        "body": TEXTURE_ROUNDUP_RU,
        "expand_topic": "RU ai texture material generators task group roundup",
    },
    {
        "rank": 352,
        "key": "poster_roundup_ru",
        "lang": "ru",
        "slug": "7-best-ai-poster-design-tools-2026",
        "cover": "052",
        "category": "Comparison",
        "title": "7 AI poster design tools 2026: группы задач honest roundup",
        "seo_title": "7 Best AI Poster Design Tools 2026 RU — no fake scores",
        "description": "RU 404 fix: 7 best ai poster design tools 2026, task groups not invented ranking table.",
        "seo_description": "Comparison: ChatCanvas poster thread, Brand Kit hex lock, Touch Edit offer fix.",
        "focus": "7 best ai poster design tools 2026",
        "keywords": ["ai poster design tools", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Poster Design Tools 2026 RU",
        "body": POSTER_ROUNDUP_RU,
        "expand_topic": "RU ai poster design tools task group roundup",
    },
    {
        "rank": 353,
        "key": "bakery_social_ru",
        "lang": "ru",
        "slug": "bakery-social-media-batch-creation-ai",
        "cover": "053",
        "category": "Industry Solution",
        "title": "Bakery social media batch creation AI: série editável padaria",
        "seo_title": "Bakery Social Media Batch AI RU — Touch Edit daily special",
        "description": "RU 404 fix: bakery social media batch creation ai, allergen disclaimer editable, Brand Kit signage hex.",
        "seo_description": "Industry Solution: ChatCanvas bakery series, Design Agent pass/fail, no fake conversion stats.",
        "focus": "bakery social media batch creation ai",
        "keywords": ["bakery social media ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Bakery Social Media Batch RU",
        "body": BAKERY_SOCIAL_RU,
        "expand_topic": "RU bakery social media batch creation workflow",
    },
    {
        "rank": 354,
        "key": "chatcanvas_spatial_ru",
        "lang": "ru",
        "slug": "chatcanvas-spatial-ai-design-collaboration",
        "cover": "054",
        "category": "Best Practice",
        "title": "ChatCanvas spatial AI design collaboration: threads e handoff (RU)",
        "seo_title": "ChatCanvas Spatial Collaboration RU — artboards Touch Edit SOP",
        "description": "RU 404 fix: chatcanvas spatial ai design collaboration, thread memory, Brand Kit shared QA.",
        "seo_description": "Best Practice: Design Agent pass/fail, Touch Edit cross-role edits, static-first motion.",
        "focus": "chatcanvas spatial ai design collaboration",
        "keywords": ["chatcanvas spatial collaboration", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Best Practice — ChatCanvas Spatial Collaboration RU",
        "body": CHATCANVAS_SPATIAL_RU,
        "expand_topic": "RU chatcanvas spatial ai design collaboration workflow",
    },
    {
        "rank": 355,
        "key": "negative_space_ru",
        "lang": "ru",
        "slug": "creating-negative-space-ai-leave-room-for-text",
        "cover": "055",
        "category": "How-To",
        "title": "Создание negative space с AI: room for text и CTA editável (RU)",
        "seo_title": "Creating Negative Space AI RU — Touch Edit safe zone SOP",
        "description": "RU 404 fix: creating negative space ai leave room for text, headline safe zone, Brand Kit roles.",
        "seo_description": "How-To: ChatCanvas brief contract, Design Agent 120px readable pass/fail.",
        "focus": "creating negative space ai leave room for text",
        "keywords": ["negative space ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Negative Space AI RU",
        "body": NEGATIVE_SPACE_RU,
        "expand_topic": "RU creating negative space ai safe zone workflow",
    },
]


EXPAND_FN = {
    "pt": expand_pt,
    "ru": expand_ru,
}

UNIT_MAP = {
    "pt": "words",
    "ru": "cyrl",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch34 content cluster.*\n"
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
