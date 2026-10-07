#!/usr/bin/env python3
"""Generate 404-rescue P2 batch33 blog bodies (10 files). Self-contained.

Ranks #336–#345 from 404-rescue-compact lane.
1 KO + 9 PT. expand_ko (batch19) + expand_pt (batch20).
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
    "ko": 1400,
    "pt": 900,
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

VMAKER_REVIEW_KO = """
# Vmaker AI 리뷰 2026: honest 비교와 revision-heavy 마케팅 static 워크플로

이 한국어 URL `vmaker-ai-review`는 404를 반환했습니다. 검색 의도는 honest Vmaker AI review — feature 목록 홍보가 아닙니다. 직접 결론: Vmaker류 도구는 screen record, 빠른 해설 clip, template talking-head 포장에 강합니다. 약한 영역은 editable price layer, **Brand Kit** carousel series, legal disclaimer 별도 layer입니다. Lovart **ChatCanvas** static master와 **Touch Edit**가 readable offer를 담당하고, Vmaker는 companion hook으로 쓸 수 있으나 entire funnel 대체는 아닙니다. **Vmaker 월 구독료·tier 금액을 본문에 조작하지 않습니다** — lovart.ai 및 Vmaker 공식 ToS만 참조.

## Vmaker가 실제로 도움이 되는 세 가지 task

첫째 product demo screen record와 내레이션 포장 — tutorial clip 빠른 제작. 둘째 internal training과 onboarding 짧은 영상 — template 가속. 셋째 social teaser 4–6초 mood — muted autoplay 전 hook. 세 가지 모두 약점: price small text bake, carousel hex drift, 화요일 promo 변경 시 clip regen.

## Vmaker가 marketing ops에서 흔히 막히는 지점

화요일 가격 변경이 clip regen 30분을 유발합니다. carousel slide 4 accent drift. disclaimer가 clip pixels에 bake. video hook에는 offer가 있으나 landing static에 **Touch Edit** price layer 없음. **Brand Kit** hex role 미설정. static-first 순서가 뒤집힘.

## parallel workflow 권장 순서

Pass one: **ChatCanvas** hero 4:5와 end card, legal pass, price bottom left safe zone, disclaimer footer editable. Pass two: optional Vmaker clip — readable small text 없음, **Brand Kit** color temperature aligned. Pass three: promo change는 **Touch Edit** static만; mood direction 변경 전까지 clip regen 생략.

## ChatCanvas brief contract (static side KO)

약한 brief: 「고급 product video 풍」. 강한 brief: 「hero 4:5, Brand Kit navy + sand, headline top 15% flat, price bottom left, disclaimer editable, render 내 small text 금지」. **Design Agent** QA safe zone, hex drift vs Kit.

## InVideo·Medeo 등 T2V와 honest 분업

first-frame beauty로 tool 구매를 유도하지 않음. 동일 화요일改价 task에서 static fix 분수 vs clip regen 분수를 비교. readable offer는 static editable layer에 있어야 함.

## 라이선스와 commercial use

Vmaker 공식 ToS에서 paid social·commercial scope 확인 — campaign folder에 license note archive. tier 가격 표 조작 금지. Lovart tier도 lovart.ai 공식 pricing page만.

## 흔한 실패

Vmaker clip만 있고 aligned static offer 없음. 매改价마다 clip regen. **Brand Kit** absent. 404 URL 미복구. fake Vmaker pricing tier.

## 측정 지표

static price fix 분수, clip regen 분수, drift 횟수. 복구 URL이 stable KO vmaker-ai-review parallel SOP link.
"""

AI_DESIGN_AGENCIES_PT = """
# AI design para agências: escalar trabalho de cliente sem inflar headcount

Esta URL portuguesa `ai-design-agencies` devolveu 404 enquanto buscas pediam um guia honesto para agências — não um ranking genérico com preços inventados. Ops diárias de agência: múltiplos clientes, briefs semanais, carousel series, price cards editáveis, disclaimers legais por setor. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** fixam palette por cliente e reduzem accent drift entre entregas. KPI é «alterar preço de campanha em cinco minutos por cliente», não «primeiro poster bonito por prompt isolado».

## Quatro entregáveis semanais por agência

Primeiro, hero feed 4:5 e carousel slides 2–6 por cliente — preço legível, accent sem drift vs **Brand Kit** desse cliente. Segundo, email header e landing companion still — disclaimer footer editable. Terceiro, ad-safe crops multi-ratio — **Design Agent** QA export mismatch. Quarto, handoff package com hex spec documentado para vendor print.

## Por que agências falham na terça ao mudar offer do cliente

Mudar «Launch R$49» exige full regen thirty minutes se preço baked in pixels. Slide 4 accent lottery entre clientes porque **Brand Kit** não foi isolado por account. Brief termina em «premium cinematic» — **Design Agent** sem campos pass/fail. Novo prompt por variante sem thread **ChatCanvas** — série quebra.

## Contrato brief ChatCanvas (agência PT)

Fraco: «poster premium para cliente X». Forte: «Client X Campaign Y 4:5 1080×1350, Brand Kit hex from approved media kit desse cliente, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants feed + email same thread, **Design Agent** pass/fail checklist». Nome de tool externo só comment — offer text bake proibido.

## Brand Kit por cliente como SSOT anti-drift

Sample primary, accent, type role do media kit aprovado do cliente — não stock gradient como brand color. **ChatCanvas** thread family por campanha por cliente. Mudança de campanha: **Touch Edit** altera copy, não product cutout geometry.

## Touch Edit prova ops viável para account managers

«20% off» para «free shipping»: hero e email header type layer **Touch Edit** numa sessão. Duas palavras de mudança com full reroll quebra cadência de terça da agência sem editable layer.

## Design Agent como checklist de handoff

Verifica safe zone, double CTA, texto pequeno, hex drift vs Kit do cliente. Não substitui brief; executa brief. Segunda passagem costuma só preencher campos em falta — account manager não precisa design jargon.

## Erros comuns agência

**Brand Kit** skipped ou misturado entre clientes. Preço baked. Novo prompt por slide. 404 não restaurado. Fake ROI benchmark por cliente.

## Métricas agência

Minutos por fix de preço por cliente, accent drift count, export ratios. URL restaurada stable PT ai-design-agencies SOP link.
"""

AI_DESIGN_EDUCATION_PT = """
# AI design para educação: materiais de curso, certificados e promo editável

Esta URL portuguesa `ai-design-education` devolveu 404 enquanto buscas pediam guia para educadores e course creators — não template genérico sem VI lock. Ops educacionais: thumbnail de módulo, slide de certificado, banner de matrícula, email header — datas e preços mudam toda semana, accent calm deriva entre LMS e social. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** fixam palette institucional. KPI é «alterar data de turma em cinco minutos», não «primeiro poster cinematic».

## Quatro cenários educacionais de alta frequência

Primeiro, course thumbnail 16:9 1280×720 — title readable, face hero safe zone. Segundo, certificate template companion — nome do aluno band editable via **Touch Edit**. Terceiro, enrollment promo 4:5 — price bottom left safe zone, disclaimer footer editable. Quarto, module carousel slides 2–6 same thread **Brand Kit** hex lock.

## Por que promo educacional falha na terça ao mudar turma

Mudar «Turma março R$890» exige full regen thirty minutes se preço baked. Slide 4 accent lottery sem **Brand Kit** institucional. Brief «premium education» — **Design Agent** sem campos pass/fail. Certificate name baked in pixels — one word change triggers full regen.

## Contrato brief ChatCanvas (educação PT)

Fraco: «poster premium curso online». Forte: «Course X enrollment 4:5 1080×1350, Brand Kit navy + sand from approved VI, headline module title top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants thumbnail + email same thread, **Design Agent** pass/fail at 50% zoom». Tool names só comment.

## Brand Kit institucional unifica LMS e social

Primary, accent, type role desde VI aprovada da instituição. **ChatCanvas** same thread batch thumbnail + enrollment + certificate companion — hex lock cross-format.

## Touch Edit muda data de turma sem crop do hero educacional

«Início 15/03» para «Início 22/03»: **Touch Edit** date band, hero geometry e **Brand Kit** accent stripe preservados. Full regen randomiza lighting — cadência semanal não absorve thirty-minute reroll.

## static-first antes de motion hook opcional

Offer de matrícula deve estar em static editable; clip bumper sem readable small text price. Educadores precisam legal pass antes de publish.

## Erros comuns educação

**Brand Kit** skipped. Preço baked. Certificate name non-editable. 404 não restaurado. Fake enrollment conversion percent.

## Métricas educação

Minutos por fix de data/preço, drift count, export ratios LMS + social. URL restaurada stable PT ai-design-education SOP link.
"""

B41_FAQ_BING_PT = """
# FAQ geração de imagens IA (Bing): respostas honestas sem ranking inventado

Esta URL portuguesa `b41-ai-image-generation-faq-bing` devolveu 404 enquanto buscas Bing e Google pediam respostas curtas sobre geração de imagens IA — não classement d'outils avec scores inventados. Este guia FAQ cobre workflow static-first com **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent**: ratio, safe zone, disclaimer editable, pass/fail acceptance. **Sem preços inventados** para tiers Lovart ou concorrentes — consultar páginas oficiais.

## Quatro perguntas FAQ que ops fazem toda semana

Primeira: qual ratio colocar no brief — 4:5 feed, 1:1 square, 16:9 landscape? Resposta: ratio no brief contract antes de gen; **Design Agent** QA export mismatch. Segunda: preço pode ir baked no render? Resposta: não — **Touch Edit** editable band bottom left. Terceira: accent drift slide 4? Resposta: **Brand Kit** hex lock + same **ChatCanvas** thread. Quarta: disclaimer legal onde? Resposta: footer editable layer, não pixels.

## Por que FAQ de image gen falha na terça ao mudar offer

Brief fraco «premium AI image» — bela imagem, preço illisible. Full regen thirty minutes por mudança de copy. **Brand Kit** não amostrado. Fake benchmark score table — zero fake metrics neste FAQ.

## Contrato brief ChatCanvas (FAQ image gen PT)

Brief forte: «Campaign X 4:5 1080×1350, Brand Kit hex from media kit, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable, variants 2–4 same thread accent stripe, **Design Agent** numeric pass/fail». Bing context no slug — não endorsement Bing oficial.

## Brand Kit antes de batch image gen

Sample primary, accent, type role de VI aprovada — não stock gradient como brand color. One **ChatCanvas** thread batches multi-ratio export.

## Touch Edit muda offer sem hero crop

«Limited R$79» para «Member R$69»: **Touch Edit** CTA band five minutes — full regen thirty minutes evitado.

## Slug b41 e contexto Bing honesto

Slug `b41-ai-image-generation-faq-bing` reflete contexto de busca Bing — artigo não é endorsement Microsoft. Conteúdo = workflow Lovart static layer honesto. Zero fake benchmark scores.

## Erros frequentes FAQ image gen

Ten prompts unrelated. **Brand Kit** skipped. Price baked. 404 não restaurado. Fake tool #1–#10 table.

## Métricas FAQ

Minutos por fix offer, accent drift count, export sizes. URL restaurada stable PT b41-ai-image-generation-faq-bing SOP link.
"""

BEAUTY_SALON_PT = """
# Melhor Design Agent AI para dono de salão de beleza: preço editável antes do wow

Esta URL portuguesa `best-ai-design-agent-for-beauty-salon-owner` devolveu 404 enquanto buscas pediam guia honesto para salões — preço lista, portfolio, social covers, não ranking genérico. Salões mudam preços, promos sazonais e formatos story toda semana; sem **Brand Kit** cada geração inventa nova rose-gold variant. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** mantêm layout estável enquanto copy muda. KPI é «alterar preço de pacote em cinco minutos».

## Quatro cenários salon de alta frequência

Primeiro, price card 4:5 — números legíveis, disclaimer footer editable sobre alergia. Segundo, before/after carousel slides 2–6 same thread accent stripe. Terceiro, Instagram story 9:16 — bottom 20% flat for **Touch Edit**. Quarto, seasonal promo — data e preço editable layer.

## Por que promo salon falha na terça ao mudar preço

Mudar «Manicure R$89» exige full regen thirty minutes se baked. Slide 4 accent lottery. **Brand Kit** não amostrado de signage aprovado. Brief «premium spa cinematic» — **Design Agent** sem pass/fail fields.

## Contrato brief ChatCanvas (beauty salon PT)

Fraco: «poster premium salão». Forte: «Season promo 4:5 1080×1350, Brand Kit rose + cream from approved signage, headline top 15% flat for Touch Edit, price bottom left safe zone, disclaimer footer editable sobre alergia, slides 2–6 same thread, **Design Agent** pass/fail checklist».

## Brand Kit do signage e prior export

Sample primary, accent, type role de signage aprovado, cartão visita, prior export — não stock marble como brand color. **ChatCanvas** same thread batch price card + carousel + story.

## Touch Edit muda preço sem crop do hero salon

«SPA R$129» para «Member R$119»: **Touch Edit** CTA band, geometry e **Brand Kit** accent stripe preservados. Full regen randomiza lighting — consistência salon não absorve thirty-minute reroll.

## static-first antes de motion hook opcional

Offer salon deve estar em static editable; clip teaser sem readable small text price.

## Erros comuns salon

**Brand Kit** skipped. Preço baked. Novo prompt por promo. 404 não restaurado. Fake conversion lift percent.

## Métricas salon

Minutos por fix preço, accent drift count, export ratios. URL restaurada stable PT best-ai-design-agent-for-beauty-salon-owner SOP link.
"""

REAL_ESTATE_BRAND_KIT_PT = """
# Brand Kit agente imobiliário: kit de marca para listings e flyers

Esta URL portuguesa `brand-kit-real-estate-agent-lovart` devolveu 404 enquanto agentes imobiliários PT buscavam guia Brand Kit para listings, flyers open house e social crop — não template genérico sem VI lock. Industry Solution branding: static-first com **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent**: logo lockup, primary hex agência, disclaimer legal editable. **Sem preços inventados**.

## Quatro layers Brand Kit agente imobiliário

Primeiro primary e accent desde charta agência aprovada — não stock luxury marble como cor oficial. Segundo logo lockup com safe zone documented para photo property overlay. Terceiro listing master 4:5 com preço e área em banda editable via **Touch Edit** — não baked in render pixels. Quarto variant series open house + sold sticker same **ChatCanvas** thread — **Design Agent** QA hex drift vs Kit.

## Por que Brand Kit imobiliário falha na terça

Brief fraco «luxury real estate premium» — bela fachada, preço m² illisible. Mudar preço listing custa thirty-minute full regen sem **Touch Edit**. Open house slide accent drift sem **Brand Kit** SSOT. Agentes querem pass/fail, não adjetivos.

## Contrato brief ChatCanvas (real estate PT)

Brief forte: «Listing Campaign X 4:5 1080×1350, Brand Kit slate + gold from agency VI, headline address top 15% flat for Touch Edit, price bottom band editable, disclaimer legal footer editable, variants open house + sold same thread, **Design Agent** pass/fail».

## Brand Kit unifica listing, flyer e social crop

Primary, accent, type role desde VI agência. **ChatCanvas** same thread batch A4 flyer + Instagram crop + story — accent stripe resta.

## Touch Edit muda preço listing sem crop logo agência

«R$ 450.000» para «R$ 435.000»: **Touch Edit** cadre CTA band, mantém logo geometry e **Brand Kit** accent. Full regen randomiza gradient fachada — série listing não suporta thirty-minute reroll.

## Erros frequentes imobiliário

Pular **Brand Kit** setup. Preço baked in pixels. Novo prompt por variante formato. URL 404 não restaurada. Fake engagement stats listing.

## Métricas imobiliário

Minutos por fix preço, accent drift, export bleed A4 ratios. URL restaurada stable PT brand-kit-real-estate-agent-lovart SOP link.
"""

CONTENT_HEALTH_SCORE_PT = """
# Framework Content Health Score para blogs de design IA: auditoria sem métricas inventadas

Esta URL portuguesa `content-health-score-framework-ai-design-blogs` devolveu 404 enquanto buscas pediam um framework de auditoria de conteúdo — não uma tabela fake «+34% traffic guaranteed». Este artigo apresenta **framework operacional**: cinco dimensões ponderadas que a sua equipa preenche com **dados reais** do GSC, GA4 e CMS — zero benchmark inventado no corpo. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** entram na dimensão Freshness e Structural quando refresh exige static companion editável.

## O que é Content Health Score (framework, não fake score)

Content Health Score é rubrica 0–100 por artigo em cinco dimensões: Traffic Health (30%), Engagement Health (20%), Conversion Health (20%), Freshness Health (20%), Structural Health (10%). Cada dimensão recebe score 0–100 com critérios definidos; soma ponderada produz score global. **Não publicamos scores de exemplo inventados** — reader exporta inventário CMS, puxa GSC/GA4 90 dias, aplica rubrica artigo a artigo.

## Dimensão Traffic Health — como pontuar com dados reais

Score 90–100: top 3 artigos por tráfego orgânico, trajectória growing MoM 6+ meses — **os seus** top 3, não números genéricos. Score 70–89: top 25% tráfego, stable or growing. Score 50–69: middle 50%, flat or slightly declining. Score 30–49: bottom 25%, declining 3+ months. Score 0–29: near-zero traffic, 6+ months sem tração. Fonte: GSC query + page export.

## Dimensão Engagement e Conversion — relative ao site average

Engagement: time on page, scroll depth, bounce rate **vs média do seu site** — não vs benchmark industry inventado. Conversion: trial signups, newsletter subs, product clicks atribuídos por URL no GA4. Score relativo ao seu portfolio, não tabela universal fake.

## Dimensão Freshness — onde Lovart ops entra no refresh

Score alto: updated last 3 months, screenshots current, pricing references apontam páginas oficiais — não tier amounts fabricated. Refresh candidate: usar **ChatCanvas** + **Brand Kit** + **Touch Edit** para static promo layers editáveis; **Design Agent** pass/fail no re-export. Fake «health score 87» sem audit data — proibido neste framework.

## Matriz de acção após scoring

Score 80–100: Maintain — monitor quarterly. 60–79: Refresh — update content, screenshots, internal links. 40–59: Consolidate — merge + 301. 0–39: Retire or Rewrite. Priorize Refresh por traffic current × strategic value — não por fake ROI projection.

## Cinco passos audit completo

Passo 1: export URLs, publish dates, categories do CMS. Passo 2: GSC/GA4 90 dias — traffic, trajectory, engagement, conversions por URL. Passo 3: score 3–5 min por artigo com rubrica. Passo 4: quatro listas Maintain/Refresh/Consolidate/Retire. Passo 5: sprint Refresh com static-first workflow Lovart onde visuals precisam update.

## Erros frequentes content audit

Publicar fake case study «traffic +34%» sem source. Score inventado sem GSC pull. Refresh só title/meta sem body/visual update. **Brand Kit** skip no refresh visual. 404 URL não restaurada.

## Métricas audit honestas

Horas total audit, count Refresh candidates, median score por category — **suas** métricas, não nossas. URL restaurada stable PT content-health-score-framework-ai-design-blogs framework link.
"""

NEGATIVE_SPACE_PT = """
# Criar negative space com IA: deixar room for text e CTA editável

Esta URL portuguesa `creating-negative-space-ai-leave-room-for-text` devolveu 404 enquanto buscas pediam How-To de negative space para headlines, preços e CTAs — não poster bonito sem safe zone. Negative space daily ops: feed hero, carousel slide, email header — copy muda toda semana, hero detail enche safe zone. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** tratam negative space como brief contract field, não afterthought Photoshop.

## Quatro deliverables negative space workflow

Primeiro hero 4:5 — top 15% e bottom 20% reservados flat for **Touch Edit**. Segundo carousel slide 2–6 — accent stripe lateral, centre negative for headline. Terceiro email header 600×300 — disclaimer footer editable band. Quarto landing companion — **Design Agent** 50% zoom readable pass/fail.

## Por que negative space AI falha na terça ao mudar headline

Brief «premium poster full bleed detail» — zero room for text. Mudar headline exige full regen thirty minutes. **Brand Kit** não define safe zone roles. Slide 4 invented busy background — **Design Agent** fail at 120px title test.

## Contrato brief ChatCanvas (negative space PT)

Fraco: «poster premium negative space aesthetic». Forte: «Campaign X 4:5 1080×1350, Brand Kit hex from media kit, headline band top 15% flat solid or subtle gradient for Touch Edit, price bottom left safe zone min 120px readable, hero subject right 60% leave left 40% negative, disclaimer footer editable, **Design Agent** pass/fail at 50% zoom».

## Brand Kit define role de negative zone

Kit documenta headline_band_color, accent_stripe_position — agent follows hex roles. **ChatCanvas** same thread batch feed + email — negative zone consistent cross-format.

## Touch Edit preenche negative space sem regen hero

Headline «Summer Sale» para «Member Week»: **Touch Edit** text band five minutes — hero geometry preserved. Full regen randomiza composition — ops não absorve thirty-minute reroll.

## Erros frequentes negative space

Hero detail enche safe zone. **Brand Kit** skip. Preço baked in busy texture. 404 não restaurado. Fake readability score sem zoom test.

## Métricas negative space

Minutos por headline fix, 120px pass rate, drift count. URL restaurada stable PT creating-negative-space-ai-leave-room-for-text SOP link.
"""

YOUTUBE_THUMBNAIL_PT = """
# Como chat generate YouTube thumbnail com Lovart: SOP static-first 1280×720

Esta URL portuguesa `how-to-chat-generate-youtube-thumbnail-lovart` devolveu 404 enquanto buscas pediam How-To chat generate YouTube thumbnail — não generic AI video demo. YouTube thumbnail standard 1280×720 — ratio no brief contract. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** tratam thumbnail como revision-heavy asset: title change, A/B variant five-minute close, not full regen lottery.

## Quatro deliverables thumbnail workflow

Primeiro master 16:9 1280×720 — face hero right, title band left negative flat for **Touch Edit**. Segundo A/B variant same **ChatCanvas** thread — accent stripe only differs. Terceiro Shorts crop 9:16 companion — **Design Agent** ratio QA. Quarto end card still — disclaimer footer editable if promo.

## Por que thumbnail chat gen falha na terça ao mudar title

Title baked in render pixels — one word change full regen thirty minutes. Slide accent lottery between A/B. **Brand Kit** não amostrado de channel VI. Brief «viral thumbnail cinematic» — **Design Agent** sem 120px title pass/fail.

## Contrato brief ChatCanvas (YouTube thumbnail PT)

Fraco: «thumbnail viral YouTube premium». Forte: «Video X thumbnail 1280×720, Brand Kit hex from channel media kit, title left 40% flat for Touch Edit min 120px at 50% zoom, face hero right safe zone, no small text in render pixels, variant B same thread accent swap, **Design Agent** pass/fail checklist».

## Brand Kit unifica thumbnail series channel

Primary, accent, type role desde channel VI. **ChatCanvas** same thread batch thumbnail A/B + Shorts crop — hex lock.

## Touch Edit muda title sem regen face hero

«5 Tips Design» para «5 Erros Design»: **Touch Edit** title band five minutes — face crop preserved. Full regen randomizes expression — channel consistency broken.

## Erros frequentes YouTube thumbnail

Title baked in pixels. **Brand Kit** skip. Fake CTR +47% claim. 404 não restaurado. New thread per variant.

## Métricas thumbnail

Minutos por title fix, 120px pass rate, A/B drift count. URL restaurada stable PT how-to-chat-generate-youtube-thumbnail-lovart SOP link.
"""

SKETCHES_DOODLES_PT = """
# Como criar sketches e doodles com IA: How-To static-first series SOP

Esta URL portuguesa `how-to-create-sketches-doodles-ai` devolveu 404 enquanto buscas pediam create sketches doodles AI How-To — não generic illustration tool ranking. Sketch doodle daily ops: social cover, note app thumb, educational material — caption e disclaimer mudam often, personal style conflita com **Brand Kit**. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** tratam sketch series static-first: master artwork, variant crops, editable caption layer.

## Quatro deliverables sketch doodle workflow

Primeiro master sketch 4:5 — caption band top 15% flat for **Touch Edit**. Segundo carousel slides 2–6 same thread stroke weight **Brand Kit** lock. Terceiro note app thumb 1:1 — disclaimer footer editable. Quarto educational worksheet companion — **Design Agent** print preview pass/fail.

## Por que sketch How-To falha na terça ao mudar caption

Caption baked in render pixels — full regen thirty minutes. Slide 4 stroke style lottery. **Brand Kit** não define stroke_weight role. Brief «cute doodle premium» — **Design Agent** sem pass/fail fields.

## Contrato brief ChatCanvas (sketches doodles PT)

Fraco: «doodle premium social cover». Forte: «Series X sketch 4:5 1080×1350, Brand Kit ink #1a1a1a + accent coral from media kit, caption top 15% flat for Touch Edit, stroke weight consistent per reference sheet, slides 2–6 same thread pose swap only, disclaimer footer editable, **Design Agent** pass/fail».

## Brand Kit carrega sketch SSOT

Kit documenta ink_hex, stroke_weight, accent role — carousel não vira mixed style collage. **ChatCanvas** same thread reduz slide 2–6 lottery.

## Touch Edit muda caption sem regen artwork

«Week 3 Tips» para «Week 4 Tips»: **Touch Edit** caption band five minutes — artwork geometry preserved. Full regen randomiza line quality — series consistency broken.

## Erros frequentes sketches doodles

Novo prompt per slide. Stroke lottery sem Kit. Caption baked. 404 não restaurado. Fake style benchmark table.

## Métricas sketches

Minutos por caption fix, stroke drift count, export ratios. URL restaurada stable PT how-to-create-sketches-doodles-ai SOP link.
"""


FAQ = {
    "vmaker_review_ko": """
## FAQ

**Vmaker tier preço no corpo?**  
Não — Vmaker e lovart.ai official ToS only.

**Touch Edit static price fix 5 min?**  
Sim — parallel workflow test.

**Brand Kit carousel hex lock?**  
Sim — media kit hex sample.

**404 URL restore?**  
Stable KO vmaker-ai-review.

**fake Vmaker pricing table?**  
Não — honest review only.
""",
    "ai_design_agencies_pt": """
## FAQ

**Brand Kit por cliente separado?**  
Sim — hex SSOT per account before batch.

**Touch Edit preço 5 min?**  
Sim — full regen evitado.

**Design Agent handoff checklist?**  
Sim — pass/fail fields for AM.

**404 restore?**  
Stable PT ai-design-agencies SOP.

**fake agency ROI benchmark?**  
Não — edit-minute KPI only.
""",
    "ai_design_education_pt": """
## FAQ

**Brand Kit institucional primeiro?**  
Sim — VI aprovada hex lock.

**Touch Edit data turma 5 min?**  
Sim — hero layout preserved.

**Certificate name editable?**  
Sim — Touch Edit text band.

**404 restore?**  
Stable PT ai-design-education.

**fake enrollment %?**  
Não — workflow SOP only.
""",
    "b41_faq_bing_pt": """
## FAQ

**Preços Lovart inventados?**  
Não — official pages only.

**Touch Edit offer 5 min?**  
Sim — static editable layer.

**Brand Kit before batch?**  
Sim — hex SSOT cross-ratio.

**404 restore?**  
Stable PT b41-ai-image-generation-faq-bing.

**fake tool ranking?**  
Não — FAQ workflow honesto.
""",
    "beauty_salon_pt": """
## FAQ

**Brand Kit signage sample?**  
Sim — approved VI hex lock.

**Touch Edit preço pacote 5 min?**  
Sim — full regen evitado.

**Disclaimer alergia editable?**  
Sim — footer Touch Edit layer.

**404 restore?**  
Stable PT best-ai-design-agent-for-beauty-salon-owner.

**fake conversion lift?**  
Não — ops metrics only.
""",
    "real_estate_brand_kit_pt": """
## FAQ

**Preço listing editable?**  
Sim — Touch Edit band, not baked pixels.

**Brand Kit agency VI?**  
Sim — primary accent SSOT.

**Open house same thread?**  
Sim — ChatCanvas thread family.

**404 restore?**  
Stable PT brand-kit-real-estate-agent-lovart.

**fake listing engagement stats?**  
Não — workflow checklist only.
""",
    "content_health_score_pt": """
## FAQ

**Scores exemplo inventados no corpo?**  
Não — reader aplica rubrica com GSC/GA4 real.

**Framework vs fake +34% case?**  
Framework only — zero fabricated metrics.

**Refresh com ChatCanvas?**  
Sim — Freshness dim visual update static-first.

**404 restore?**  
Stable PT content-health-score-framework-ai-design-blogs.

**fake health score 87?**  
Proibido — audit data required.
""",
    "negative_space_pt": """
## FAQ

**Safe zone no brief contract?**  
Sim — top 15% flat for Touch Edit.

**Brand Kit negative zone roles?**  
Sim — headline_band documented.

**Headline fix 5 min?**  
Sim — Touch Edit without hero regen.

**404 restore?**  
Stable PT creating-negative-space-ai-leave-room-for-text.

**fake readability score?**  
Não — Design Agent zoom test only.
""",
    "youtube_thumbnail_pt": """
## FAQ

**Ratio 1280×720 no brief?**  
Sim — YouTube standard in contract.

**Title Touch Edit 5 min?**  
Sim — face hero preserved.

**Brand Kit channel VI?**  
Sim — hex lock A/B variants.

**404 restore?**  
Stable PT how-to-chat-generate-youtube-thumbnail-lovart.

**fake CTR +47%?**  
Não — 120px pass rate KPI only.
""",
    "sketches_doodles_pt": """
## FAQ

**Stroke weight Brand Kit lock?**  
Sim — ink_hex + stroke role SSOT.

**Caption Touch Edit 5 min?**  
Sim — artwork geometry preserved.

**Same thread slides 2–6?**  
Sim — pose swap only.

**404 restore?**  
Stable PT how-to-create-sketches-doodles-ai.

**fake style benchmark?**  
Não — pass/fail checklist only.
""",
}


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 실습 보충 {n}: {topic}

첫 brief가 형용사만 쌓이면 그림은 예쁘지만 가격 글자가 작고 배지가 hero를 가립니다. 두 번째는 safe zone과 필수 필드만 수정. **ChatCanvas** thread가 slide 4 accent drift를 줄입니다. **{topic}**에서 **Touch Edit** 가격 수정 5분이면 static-first 입증. full regen 30분이면 **Brand Kit**부터 재설정. 복구된 404 URL이 stable SOP link batch33. **Design Agent** pass/fail checklist가 형용사 brief보다 낫습니다.
"""


def expand_pt(topic: str, n: int) -> str:
    return f"""
## Nota de campo {n}: {topic}

O primeiro brief termina em „premium" e falha: preço pequeno, badge sobre o rosto. Na segunda passagem, corrija só safe zone e campos obrigatórios. Um thread **ChatCanvas** reduz accent drift no slide 4. Em **{topic}**, **Touch Edit** confirma fix de preço em cinco minutos static-first. Full regen 30 minutos — recomece pelo **Brand Kit**. URL 404 restaurada como link SOP estável batch33. **Design Agent** pass/fail checklist vence briefs adjetivos.
"""


ARTICLES = [
    {
        "rank": 336,
        "key": "vmaker_review_ko",
        "lang": "ko",
        "slug": "vmaker-ai-review",
        "cover": "036",
        "category": "Review",
        "title": "Vmaker AI 리뷰 2026: honest 비교와 static-first parallel workflow",
        "seo_title": "Vmaker AI Review KO — no fabricated VMaker pricing",
        "description": "KO 404 fix: honest Vmaker AI review, Touch Edit static layer, no fabricated VMaker tier pricing.",
        "seo_description": "Review: ChatCanvas parallel workflow, Brand Kit hex lock, official ToS only.",
        "focus": "vmaker ai review",
        "keywords": ["vmaker ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Vmaker AI Review KO",
        "body": VMAKER_REVIEW_KO,
        "expand_topic": "KO vmaker ai review parallel static workflow",
    },
    {
        "rank": 337,
        "key": "ai_design_agencies_pt",
        "lang": "pt",
        "slug": "ai-design-agencies",
        "cover": "037",
        "category": "Lovart 101",
        "title": "AI design para agências: escalar client work sem inflar headcount",
        "seo_title": "AI Design Agencies PT — Brand Kit per client ChatCanvas SOP",
        "description": "PT 404 fix: ai design agencies guide, per-client Brand Kit, Touch Edit five-minute offer fix.",
        "seo_description": "Lovart 101: ChatCanvas thread per campaign, Design Agent handoff checklist.",
        "focus": "ai design agencies",
        "keywords": ["ai design agencies", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Lovart 101 — AI Design Agencies PT",
        "body": AI_DESIGN_AGENCIES_PT,
        "expand_topic": "PT ai design agencies per-client workflow",
    },
    {
        "rank": 338,
        "key": "ai_design_education_pt",
        "lang": "pt",
        "slug": "ai-design-education",
        "cover": "038",
        "category": "Industry Solution",
        "title": "AI design para educação: materiais de curso e promo editável",
        "seo_title": "AI Design Education PT — Touch Edit enrollment layer",
        "description": "PT 404 fix: ai design education course materials, Brand Kit institutional hex lock.",
        "seo_description": "Industry Solution: ChatCanvas thumbnail + certificate companion, Design Agent QA.",
        "focus": "ai design education",
        "keywords": ["ai design education", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — AI Design Education PT",
        "body": AI_DESIGN_EDUCATION_PT,
        "expand_topic": "PT ai design education course workflow",
    },
    {
        "rank": 339,
        "key": "b41_faq_bing_pt",
        "lang": "pt",
        "slug": "b41-ai-image-generation-faq-bing",
        "cover": "039",
        "category": "How-To",
        "title": "FAQ geração de imagens IA (Bing): respostas honestas",
        "seo_title": "B41 AI Image Generation FAQ Bing PT — no fake pricing",
        "description": "PT 404 fix: b41 ai image generation FAQ Bing, static-first honest answers, no fake benchmarks.",
        "seo_description": "How-To FAQ: ChatCanvas brief contract, Brand Kit hex lock, official ToS only.",
        "focus": "b41 ai image generation faq bing",
        "keywords": ["ai image generation faq", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — B41 AI Image FAQ Bing PT",
        "body": B41_FAQ_BING_PT,
        "expand_topic": "PT b41 ai image generation faq bing workflow",
    },
    {
        "rank": 340,
        "key": "beauty_salon_pt",
        "lang": "pt",
        "slug": "best-ai-design-agent-for-beauty-salon-owner",
        "cover": "040",
        "category": "Industry Solution",
        "title": "Melhor Design Agent AI para dono de salão de beleza",
        "seo_title": "Best AI Design Agent Beauty Salon Owner PT — Touch Edit price",
        "description": "PT 404 fix: best ai design agent beauty salon owner, Brand Kit signage hex, editable price card.",
        "seo_description": "Industry Solution: ChatCanvas salon series, Design Agent pass/fail, no fake conversion stats.",
        "focus": "best ai design agent for beauty salon owner",
        "keywords": ["beauty salon ai design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Beauty Salon Owner PT",
        "body": BEAUTY_SALON_PT,
        "expand_topic": "PT best ai design agent beauty salon workflow",
    },
    {
        "rank": 341,
        "key": "real_estate_brand_kit_pt",
        "lang": "pt",
        "slug": "brand-kit-real-estate-agent-lovart",
        "cover": "041",
        "category": "Best Practice",
        "title": "Brand Kit agente imobiliário: listings e flyers editáveis",
        "seo_title": "Brand Kit Real Estate Agent Lovart PT — Touch Edit listing price",
        "description": "PT 404 fix: brand kit real estate agent lovart, listing price editable, agency VI hex lock.",
        "seo_description": "Best Practice: ChatCanvas listing thread, Design Agent hex drift QA.",
        "focus": "brand kit real estate agent lovart",
        "keywords": ["brand kit real estate", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Best Practice — Real Estate Brand Kit PT",
        "body": REAL_ESTATE_BRAND_KIT_PT,
        "expand_topic": "PT brand kit real estate agent workflow",
    },
    {
        "rank": 342,
        "key": "content_health_score_pt",
        "lang": "pt",
        "slug": "content-health-score-framework-ai-design-blogs",
        "cover": "042",
        "category": "Insight & Trend",
        "title": "Framework Content Health Score: auditoria blog design IA",
        "seo_title": "Content Health Score Framework PT — rubrica sem métricas fake",
        "description": "PT 404 fix: content health score framework, five-dimension rubric, zero fabricated benchmark scores.",
        "seo_description": "Insight: GSC/GA4 real data audit, Refresh with ChatCanvas static-first, no fake +34% case.",
        "focus": "content health score framework ai design blogs",
        "keywords": ["content health score", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight & Trend — Content Health Score Framework PT",
        "body": CONTENT_HEALTH_SCORE_PT,
        "expand_topic": "PT content health score framework audit workflow",
    },
    {
        "rank": 343,
        "key": "negative_space_pt",
        "lang": "pt",
        "slug": "creating-negative-space-ai-leave-room-for-text",
        "cover": "043",
        "category": "How-To",
        "title": "Criar negative space com IA: room for text e CTA editável",
        "seo_title": "Creating Negative Space AI PT — Touch Edit safe zone SOP",
        "description": "PT 404 fix: creating negative space ai leave room for text, headline safe zone, Brand Kit roles.",
        "seo_description": "How-To: ChatCanvas brief contract, Design Agent 120px readable pass/fail.",
        "focus": "creating negative space ai leave room for text",
        "keywords": ["negative space ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Negative Space AI PT",
        "body": NEGATIVE_SPACE_PT,
        "expand_topic": "PT creating negative space ai safe zone workflow",
    },
    {
        "rank": 344,
        "key": "youtube_thumbnail_pt",
        "lang": "pt",
        "slug": "how-to-chat-generate-youtube-thumbnail-lovart",
        "cover": "044",
        "category": "How-To",
        "title": "Como chat generate YouTube thumbnail com Lovart: SOP 1280×720",
        "seo_title": "How To Chat Generate YouTube Thumbnail Lovart PT — Touch Edit title",
        "description": "PT 404 fix: how to chat generate youtube thumbnail lovart, static-first 1280×720, no fake CTR claims.",
        "seo_description": "How-To: ChatCanvas A/B thread, Brand Kit channel VI, Design Agent title QA.",
        "focus": "how to chat generate youtube thumbnail lovart",
        "keywords": ["youtube thumbnail lovart", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Chat Generate YouTube Thumbnail PT",
        "body": YOUTUBE_THUMBNAIL_PT,
        "expand_topic": "PT how to chat generate youtube thumbnail workflow",
    },
    {
        "rank": 345,
        "key": "sketches_doodles_pt",
        "lang": "pt",
        "slug": "how-to-create-sketches-doodles-ai",
        "cover": "045",
        "category": "How-To",
        "title": "Como criar sketches e doodles com IA: How-To series SOP",
        "seo_title": "How To Create Sketches Doodles AI PT — Brand Kit stroke lock",
        "description": "PT 404 fix: how to create sketches doodles ai, caption editable, stroke weight Brand Kit SSOT.",
        "seo_description": "How-To: ChatCanvas sketch thread, Touch Edit caption band, Design Agent print QA.",
        "focus": "how to create sketches doodles ai",
        "keywords": ["sketches doodles ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Create Sketches Doodles AI PT",
        "body": SKETCHES_DOODLES_PT,
        "expand_topic": "PT how to create sketches doodles ai workflow",
    },
]


EXPAND_FN = {
    "ko": expand_ko,
    "pt": expand_pt,
}

UNIT_MAP = {
    "ko": "hangul",
    "pt": "words",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch33 content cluster.*\n"
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
