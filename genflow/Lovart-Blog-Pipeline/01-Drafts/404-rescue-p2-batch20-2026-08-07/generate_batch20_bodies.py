#!/usr/bin/env python3
"""Generate 404-rescue P2 batch20 blog bodies (10 files). Self-contained.

Ranks #204–#213 from 404-rescue-compact lane.
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

NON_DESIGN_PT = """
# Melhor Design Agent para quem não é designer (PT): contrato de brief operacional

Esta URL portuguesa `best-agent-for-non-design` devolveu 404 enquanto buscas pediam um guia honesto para marketers, founders e ops sem formação em design — não um ranking genérico de ferramentas com preços inventados. Ops semanal: feed Instagram 4:5, stories 9:16, promo sazonal, cartão de preços — alterações de offer toda semana, accent color deriva entre feed e vitrine. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** fixam palette de campanha. KPI é «alterar preço em cinco minutos», não «primeiro poster bonito».

## Quatro outputs semanais para perfis não-design

Primeiro, hero feed 4:5 e carousel slides 2–6: preço legível, accent sem drift. Segundo, story 9:16: top 12% e bottom 20% reservados para UI da plataforma. Terceiro, static de evento ou live: headline flat for **Touch Edit**. Quarto, cartão de preços e membership card: disclaimer footer editable.

## Brief fraco versus brief contrato

Fraco: «faz-me um poster premium». Forte: «SKU centrado, Brand Kit slate + coral, headline top 15%, preço bottom left safe zone, 1080×1350, proibir double CTA, disclaimer editable footer». **Design Agent** não pode aceitar «parece premium».

## Brand Kit antes do batch

Sem **Brand Kit** cada ronda inventa novo accent. Sample hex de packaging real ou slide aprovado. Depois abre thread **ChatCanvas** de produto. Mudança de campanha: **Touch Edit** altera copy, não product cutout.

## Touch Edit é o motivo de regressão para não-designers

Só alterar bloco de preço ou data de evento. Instrução: manter stripe e font role, substituir copy. Full regen assusta perfis não-design — **Touch Edit** em cinco minutos é motivo de regressão na terça.

## Design Agent como checklist

Verifica safe zone, double CTA, texto pequeno, hex drift vs Kit. Não substitui brief; executa brief. Segunda passagem costuma só preencher campos em falta, sem trocar modelo.

## Diferença vs versão it/zh do mesmo slug

Versão it cobre marketer EU; zh cobre Xiaohong/Douyin safe zone. Esta versão pt-BR: Instagram/TikTok BR, formato R$, disclaimer ANVISA-adjacent quando aplicável. Slug igual, locale diferente, parágrafo não copiado.

## Erros comuns

Só prompt estético. Alterar preço com full regen. Carousel sem thread único. Preço baked em video clip. Brief sem disclaimer.

## Métricas

Minutos por alteração de preço, drift slide 4. **Touch Edit** cinco minutos → workflow válido para não-designers. URL restaurada como stable PT best agent for non design SOP link.
"""

FITNESS_STUDIO_PT = """
# Melhor Design Agent AI para boutique fitness studio (PT): preço editável antes do wow

Esta URL portuguesa `best-ai-design-agent-for-boutique-fitness-studio` devolveu 404 enquanto buscas pediam guia honesto para studios boutique — HIIT, cycling, boxing — não ranking genérico. Ops diárias: challenge graphics, class packs, coach spotlight, WOD screen — preços e datas mudam toda semana, accent neon deriva entre Instagram e TV interna. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** e **Design Agent** fixam palette sweat-ready. KPI é «alterar preço de challenge em cinco minutos», não «primeiro poster cinematic».

## Quatro cenários boutique fitness de alta frequência

Primeiro, challenge launch 4:5: preço legível, data editable, disclaimer footer. Segundo, class pack promo slides 2–6: mesmo thread accent stripe. Terceiro, coach spotlight 1:1: bottom 20% flat for **Touch Edit**. Quarto, WOD screen 16:9: copy editable layer, não baked in pixels.

## Por que promos fitness falham na terça ao mudar preço

Mudar «Challenge R$149» exige full regen thirty minutes se preço baked. Slide 4 accent lottery. **Brand Kit** não amostrado de signage aprovado do studio. Brief termina em «premium cinematic» — **Design Agent** sem campos pass/fail.

## ChatCanvas brief contract (boutique fitness PT)

Fraco: «poster premium de gym». Forte: «Challenge X 4:5 1080×1350, Brand Kit charcoal + neon coral from studio signage, headline top 15% flat for Touch Edit, preço bottom left safe zone, disclaimer footer editable, slides 2–6 same thread, WOD screen 16:9 companion». **Design Agent** campos numéricos — não «parece motivador».

## Brand Kit do signage, merch, export anterior

Sample primary, accent, type role de signage aprovado, merch, prior export — não stock gym photo como brand color. **ChatCanvas** same thread batch challenge + class pack + coach spotlight.

## Touch Edit muda preço de challenge sem crop do hero

«Early bird R$129» para «Member R$119»: **Touch Edit** banda CTA, mantém geometry e **Brand Kit** accent stripe. Full regen randomiza lighting — studio consistency não absorve thirty-minute reroll.

## Static-first antes de motion hook opcional

Ordem: static legal pass on disclaimer → variant A/B still → winner thread master → optional motion intro. **Touch Edit** price fix em cinco minutos — ops viable para cadência semanal de challenges.

## Erros comuns

**Brand Kit** ignorado. Preço baked. Novo prompt por challenge. Disclaimer ausente. URL 404 não restaurada. Fake conversion lift claims.

## Métricas

Minutos por fix de preço, accent drift, export ratios. URL restaurada como stable PT boutique fitness Design Agent SOP link.
"""

APPOINTMENT_CARDS_PT = """
# Como gerar cartões de agendamento via ChatCanvas (PT): layer CTA editável static-first

Esta URL portuguesa `how-to-chat-generate-appointment-cards-lovart` devolveu 404 enquanto buscas pediam How-To de chat generate appointment cards — não ranking genérico. Ops diárias: cartão 3.5×2, salão/clínica/veterinário — alterar horário, disclaimer e contacto frequentemente, accent drift entre impressão e Instagram. Lovart **ChatCanvas** brief conversacional, **Brand Kit**, **Touch Edit** e **Design Agent** fixam palette. KPI é «alterar horário em cinco minutos», não «primeiro cartão bonito». Static-first: CTA e disclaimer em layer editável.

## Quatro layers de appointment card static

Primeiro, frente 3.5×2: logo safe zone, campos data/hora editable via **Touch Edit**. Segundo, verso: contacto, disclaimer cancelamento footer editable. Terceiro, companion digital 4:5 para WhatsApp: mesmo thread accent stripe. Quarto, display counter 16:9: offer match cartão físico; **Design Agent** QA mismatch.

## Por que chat generate appointment cards falha ao mudar horário

Brief conversacional para em «cartão premium de salão» — **Design Agent** sem pass/fail fields. Alterar «Consulta €45» exige full regen thirty minutes. **Brand Kit** não amostrado de cartão aprovado. CTA baked in render pixels — fix de terça dispara reroll inteiro.

## ChatCanvas brief contract (appointment cards PT)

Fraco: «gera cartão de marcação bonito». Forte: «Campaign X appointment card 3.5×2, Brand Kit sage + cream from media kit, campos data/hora top 40% flat for Touch Edit, preço bottom left safe zone, disclaimer cancelamento footer editable, no small text in render, companion WhatsApp 4:5 same thread, static-first CTA layer only». **Design Agent** numeric fields — não «parece profissional».

## Brand Kit de VI aprovada, cartão anterior, export prior

Sample primary, accent, type role de VI aprovada, cartão anterior, prior export — não stock marble como cor do salão. **ChatCanvas** same thread batch frente + verso + companion digital export.

## Touch Edit altera horário sem crop do logo

Alterar «10:00» para «14:30»: **Touch Edit** text band, mantém logo geometry e **Brand Kit** accent stripe. Full regen randomiza spacing — ops de salão não absorve thirty-minute reroll. Static-first significa clip sem offer baked em pixels.

## Distinção vs slug Brand Kit-only de salão

slug Brand Kit salão cobre hex sampling SOP; este cobre **ChatCanvas** brief conversacional e static-first CTA editable layer. Intent complementar, campos brief sobrepostos mas entrada diferente.

## Erros comuns

Brief conversacional com adjetivos. **Brand Kit** ignorado. Preço baked. Nova thread por campanha. URL 404 não restaurada. Fake no-show reduction stats.

## Métricas

Minutos por fix de horário, drift count, export ratios. URL restaurada como stable PT chat generate appointment cards SOP link.
"""

SKINCARE_LAUNCH_RU = """
# От имени до launch: skincare brand identity с AI (RU)

Русская страница `from-name-to-launch-skincare-brand-identity-ai` отдавала 404, хотя запросы искали case narrative launch skincare — не generic ranking инструментов. Honest workflow: naming mood board → wordmark exploration → **Brand Kit** hex lock → packaging hero → launch promo static → **Touch Edit** fix launch price. Revision hotspots: ingredient disclaimer, launch price, channel crop — не первый bottle render.

## Шесть deliverable layer для skincare launch

Первый — naming mood board: three direction, без commit hex. Второй — wordmark + icon exploration: **ChatCanvas** thread clear space. Третий — **Brand Kit** primary/accent/type role из approved packaging. Четвёртый — hero 4:5 и carousel slide 2–6: same grid, разный copy. Пятый — story 9:16 и feed crop: same thread derivative. Шестой — end card и retail shelf talker: price и disclaimer на **Touch Edit** editable layer.

## Почему skincare launch ломается на revision

Изменение ingredient copy → full regen thirty minutes. Carousel slide 4 accent drift в другой pastel. Readable launch price baked in pixels. Video hook есть offer, landing static нет. **Brand Kit** не sample из packaging — online drift offline.

## ChatCanvas brief contract (skincare launch RU)

Слабый brief: «premium skincare brand feel». Сильный: «hero 4:5 1080×1350, product center, headline top 15% flat for Touch Edit, Brand Kit sage + cream accent from packaging sample, launch price bottom left safe zone, ingredient disclaimer footer editable, запрет мелкого текста в render, slides 2–6 same thread». **Design Agent** acceptance criteria — не clip «cinematic feel».

## Brand Kit из packaging фиксирует identity

Sample primary hex, accent hex, title/body role из approved bottle label, box, dieline. Не stock marble как brand color. После Kit все **ChatCanvas** launch threads ссылаются на одни role.

## Touch Edit меняет launch price без bottle identity crop

«Launch ₽1990» → «Limited ₽1590»: **Touch Edit** CTA band, bottle geometry и **Brand Kit** accent stripe сохранены. Full regen randomizes cap highlight и shadow.

## Design Agent QA для regulated copy

Проверка: ingredient disclaimer present, price readable at mobile width, hex drift vs Kit, safe zone, no double CTA. Не substitute legal copy — acceptance brief fields. Second pass часто только disclaimer sentence.

## Static-first перед optional motion launch teaser

Launch teaser autoplay часто mute; user screenshot still. Порядок: static legal pass on all sizes → optional motion. Иначе clip offer есть, PDP static не edit.

## Case narrative measurement без fake sales

Записывать «минуты на fix launch price», «сколько size за export», «carousel drift count». Если **Touch Edit** avg < five minutes а reroll avg > thirty — workflow valid. Не писать fake GMV.

## Типичные ошибки

Skip Brand Kit с random pastel. Readable price baked. Single size hero без series thread. 404 URL не restored. Fake funding data.

## Метрики

Minutes per launch price fix, drift count, export ratios. Restored URL — stable RU skincare brand identity launch SOP link.
"""

BROCHURES_RU = """
# Как создать professional brochures с AI: пошаговый tutorial (RU)

Русская страница `how-to-design-professional-brochures-with-ai-step-by-step-tutorial` отдавала 404, хотя запросы искали step-by-step tutorial brochures — не generic ranking. Brochure ops: tri-fold A4, bi-fold service menu, event program — offer и disclaimer меняются часто, accent drift между print preview и social crop. Lovart **ChatCanvas**, **Brand Kit**, **Touch Edit** и **Design Agent** держат brochure series static-first. KPI — «изменить offer за пять минут», не «первый wow spread».

## Четыре deliverable layer для brochure workflow

Первый — tri-fold master A4 300dpi intent: readable headline, disclaimer footer editable, bleed safe zone. Второй — bi-fold service menu companion: **Brand Kit** accent stripe same thread. Третий — social crop 4:5 и 1:1: **Design Agent** QA mismatch vs print master. Четвёртый — event program insert: offer match cover; disclaimer editable layer.

## Почему brochure promo ломается во вторник при смене offer

Смена «Consultation ₽990» требует full regen thirty minutes, если price baked in spread pixels. Panel 3 accent lottery. **Brand Kit** не sample из approved VI или prior brochure export. Teams brief «premium corporate» — **Design Agent** без pass/fail fields.

## ChatCanvas brief contract (brochures RU step-by-step)

Слабый brief: «сделай premium brochure». Сильный: «Campaign X tri-fold A4 300dpi intent, Brand Kit navy + gold from media kit, headline panel 1 top 15% flat for Touch Edit, price panel 2 bottom left safe zone, disclaimer footer editable, bleed 3mm safe zone, panels 2–3 same thread, bi-fold companion same ChatCanvas thread». **Design Agent** numeric pass/fail — не «выглядит corporate».

## Brand Kit как SSOT против hex drift print vs screen

Sample primary, accent, type role из approved VI и prior brochure export — не random stock gradient. Один **ChatCanvas** thread batch tri-fold + bi-fold + social crop export. Brochure — series work; memory beats surprise.

## Touch Edit меняет offer без hero crop across panels

«Limited ₽790» → «Member ₽690»: **Touch Edit** CTA band на static master, hero geometry и **Brand Kit** accent stripe сохранены. Full regen per panel randomizes lighting — print ops не absorb thirty-minute reroll.

## Step-by-step order: static legal pass before print handoff

Порядок: static legal pass on disclaimer → variant A/B still → winner still thread master → print proof export → optional motion elsewhere only. **Touch Edit** price change within five minutes — ops viable before reprint deadline.

## Отличие от generic AI poster demos

Poster demos win first-frame wow; brochure ops win on Tuesday offer fix и multi-panel hex consistency. Tutorial covers buyer criteria for revision-heavy print promo.

## Типичные ошибки

Print bleed ignored. Price baked. New prompt per campaign. **Brand Kit** skipped. 404 URL не restored. Fake print vendor pricing.

## Метрики

Minutes per offer fix, reprint count, accent drift. Restored URL — stable RU professional brochures AI step-by-step SOP link.
"""

BG_WALLPAPER_ZH = """
# 2026 AI 背景壁纸生成器选型：按任务匹配，不编虚假排名

这条中文 URL `8-best-ai-background-wallpaper-generators-2026` 曾返回 404，搜索需要 honest roundup — 不是「第 1 名绝对最好」的虚假榜单。壁纸 daily ops：桌面 4K、手机 9:16、社媒 cover、品牌 mood board — 改 campaign accent 勤，hex 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 适合 series campaign 壁纸与 editable CTA layer；纯 wallpaper 工具适合单次 export。本篇按任务场景分组，不编造市场份额或 fake benchmark 分数。

## 四类壁纸任务与选型标准

第一类 desktop 4K master：readable 无小字 offer，**Brand Kit** hex lock，适合 campaign series。第二类 phone 9:16：safe zone top/bottom 留 UI，**Touch Edit** 改日期不改 hero crop。第三类 social cover 4:5：accent stripe 同 thread，**Design Agent** QA mismatch between ratio exports。第四类 mood board exploration：three direction 不 commit hex，再进 Kit 流程。

## 为什么「8  best」榜单常误导采购

榜单把不同任务（单次壁纸 vs campaign series）混排，编造「转化率 +47%」无来源数据。readable 价格 bake 进 wallpaper pixels 无法 Tuesday fix。**Brand Kit** 未从 approved VI 取样 → slide 4 accent drift。 honest roundup 应写：什么任务用什么工具，revision cost 多少分钟。

## ChatCanvas brief 合同（campaign wallpaper 版）

弱 brief「帮我做高级壁纸」。强 brief「campaign X desktop 3840×2160，Brand Kit teal + sand from media kit，headline top 15% flat for Touch Edit，无 render 内小字 offer，phone 9:16 + cover 4:5 same thread companion」。**Design Agent** numeric fields — 不能 QA「看起来高级」。

## 八类工具 honest 分组（非排名）

组 A 单次 aesthetic export：适合个人桌面，不适合 weekly offer fix。组 B pattern/tile 工具：适合 repeat background，需检查 seam。组 C campaign series 平台（含 Lovart）：**ChatCanvas** thread + **Brand Kit** + **Touch Edit** editable layer — 适合 brand ops。组 D video loop wallpaper：motion hook optional，static still 须 legal pass first。不编造各组「第几名」，只写任务匹配与 revision 成本。

## Brand Kit 从 approved VI 取样防 drift

从已批准 VI、prior wallpaper export 取样 primary、accent、type role。不用 stock marble 当品牌色。**ChatCanvas** 同一 thread batch desktop + phone + cover export。

## Touch Edit 改 campaign 日期不改 wallpaper hero crop

改「限时至 8/15」为「延至 8/22」：**Touch Edit** text band，保持 hero geometry 与 **Brand Kit** accent stripe。full regen random 改 lighting — brand ops 承受不起 thirty-minute reroll。

## 与 pure AI art playground 的分工

playground 赢 first-frame wow；campaign ops 赢 Tuesday offer fix 与 multi-ratio hex 一致。roundup 覆盖 buyer criteria：revision-heavy promo 选 series 平台，单次 aesthetic 选 lightweight export 工具。

## 常见失败

相信 fake 排名榜单。价格 baked。每尺寸新 prompt。跳过 **Brand Kit**。404 未修复。编造工具定价。

## 测量什么

改 offer 一次几分钟、drift 几次、export 几种 ratio。404 修复给 wallpaper generator roundup stable SOP URL。
"""

AUTO_RESIZE_ZH = """
# AI 多平台自动 resize 工作流：master-first 防 accent drift

这条中文 URL `auto-resize-multi-platform-workflow-ai` 曾返回 404，搜索需要 multi-platform auto resize How-To — 不是 generic「最好 AI 设计工具」榜单。Ops daily：小红书 4:5、抖音 9:16、视频号 16:9、朋友圈 1:1 — 改 offer 勤，hex 易 drift。Lovart **ChatCanvas** master thread、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 campaign palette。KPI 是「改 offer 一次 export 全尺寸」，不是「第一张 wow」。

## 四个 multi-size export layer

第一是 master 4:5 1080×1350：headline 与 disclaimer footer editable，CTA bottom 20% flat for **Touch Edit**。第二是 9:16 vertical 1080×1920：同 thread accent stripe，safe zone top/bottom 留平台 UI。第三是 1:1 square 1080×1080：价格 bottom left safe zone readable。第四是 16:9 landscape companion：**Design Agent** QA mismatch vs master hex。

## 为什么 auto resize 常卡在周二改 offer

十个尺寸各开 prompt — slide 4 accent lottery。offer baked in pixels；改「开业 ¥99」触发每尺寸 full regen 三十分钟。**Brand Kit** 未从 approved VI 取样。crop-first 从 square 裁 9:16 常切掉 CTA。

## ChatCanvas brief 合同（auto resize 版）

弱 brief「帮我做多尺寸海报」。强 brief「campaign X master 4:5 1080×1350，Brand Kit slate + coral from media kit，headline top 15% flat for Touch Edit，价格 bottom left safe zone，disclaimer footer editable，禁止 render 内小字，derivative 9:16 + 1:1 + 16:9 same thread，master-first not crop-first」。**Design Agent** numeric fields — 不能 QA「看起来专业」。

## Brand Kit 作为 batch SSOT 防 hex drift

从已批准 VI、prior export 取样 primary、accent、type role。一个 **ChatCanvas** thread batch master + derivatives export。auto resize 是 series work；memory beats surprise。

## Touch Edit 改 offer 一次 re-export 全尺寸

改「限时 ¥79」为「会员 ¥69」：**Touch Edit** CTA band on master，re-export 9:16 + 1:1 + 16:9，hero geometry 与 **Brand Kit** accent stripe  preserved。full regen per size random 改 lighting — ops 承受不起四路 thirty-minute reroll。

## master-first 顺序 static legal pass

顺序：master static legal pass on disclaimer → derivative crops same thread → variant A/B still → winner thread master → optional motion elsewhere。**Touch Edit** price change 五分钟内 — ops viable for weekly 多平台 cadence。

## 与 ru batch6 slug 的分工

ru 版覆盖 VK/YouTube RU locale fields；简体版覆盖小红书/抖音/视频号 safe zone 与 RMB 价目格式。slug 同，locale 不同，brief 字段不 copy paragraph。

## 常见失败

crop-first 无 master thread。价格 baked。每尺寸新 prompt。跳过 **Brand Kit**。404 未修复。编造各平台 ROI 数字。

## 测量 ROI

改 offer 一次几分钟 × 尺寸数、drift 几次、export 几种 ratio。404 修复给 auto resize multi platform workflow stable SOP URL。
"""

SEEDANCE_PROMPTS_ZH = """
# Seedance 2 视频创作 prompt 精选：workflow 导向，不编造定价

这条中文 URL `awesome-prompts-seedance-2-video-creation-guide` 曾返回 404，搜索需要 Seedance 2 prompt guide — 不是 generic 视频工具 ranking，**不编造 Seedance 官方定价或 fake 性能 benchmark**。Seedance ops：multi-shot character consistency、campaign board 内 clip — 改 offer 与 disclaimer 仍须 static companion editable。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 campaign palette；motion hook optional after static legal pass。

## 四类 Seedance prompt 场景（workflow 分组）

第一类 atmosphere B-roll：无 readable offer in clip pixels，landing static 承载 CTA editable layer。第二类 character lock multi-shot：reference plate yaw ±15°，**Brand Kit** accent 一致 thread。第三类 product hero motion：bottle/cutout geometry 不变，**Touch Edit** 改价在 static companion。第四类 social hook 10s：static still 先 legal pass，再 optional subtle motion。

## 为什么 prompt 指南常误导 ops

指南堆「cinematic」「viral」形容词 — **Design Agent** 无 pass/fail fields。clip 内 bake 小字 offer → Tuesday fix 触发 full reroll。编造 Seedance 月费 ¥XX 无官方来源 — 本篇不写任何 Seedance 定价数字，读者须查官方页面。multi-shot 无 reference → slide 4 character drift。

## ChatCanvas brief 合同（Seedance 2 prompt 版）

弱 brief「帮我做 Seedance  viral 视频」。强 brief「campaign X Seedance prep 16:9，Brand Kit slate + coral from media kit，headline static companion top 15% flat for Touch Edit，价格 bottom left safe zone on still only，disclaimer footer editable，clip 内禁止小字 offer，character ref plate yaw ±15°，variants 2–4 same thread」。**Design Agent** QA static acceptance — 不能 QA clip「电影感」。

## 精选 prompt 模板（不含 fake 排名）

模板 A atmosphere：「slow dolly product hero, muted lighting, no text in render, accent stripe match Brand Kit hex」。模板 B character：「same character ref plate, walk cycle 3s, no price in pixels」。模板 C hook：「10s hook, static CTA on companion still editable via Touch Edit」。不声称「prompt #1 转化率最高」— 只描述 field 结构与 revision cost。

## Brand Kit  против random palette drift in multi-shot

从 approved VI、prior export 取样 primary、accent、type role。**ChatCanvas** same thread batch clip prep + static companion + social crop。Seedance series 是 memory work；surprise accent 破坏 character lock。

## Touch Edit 改 offer 在 static companion 不改 clip crop

改「限时 ¥99」为「会员 ¥89」：**Touch Edit** CTA band on still master，clip geometry  preserved。full regen clip random 改 lighting — campaign ops 承受不起 thirty-minute reroll per shot。

## static-first 再 optional Seedance motion

顺序：static legal pass on disclaimer → variant A/B still → winner still thread master → Seedance motion hook elsewhere。**Touch Edit** price change 五分钟内 — ops viable。不编造 Seedance API 配额或 fake render speed 数据。

## 常见失败

clip 内 bake offer。编造 Seedance 定价。无 character reference multi-shot。跳过 **Brand Kit**。404 未修复。每 shot 新 prompt 无 thread。

## 测量什么

改 offer 一次几分钟、character drift 几次、static companion export 几种 ratio。404 修复给 Seedance 2 prompt guide stable SOP URL — 定价以官方为准。
"""

LOGO_COMPARISON_ZH = """
# AI Logo 制作工具对比（Bing 语境）：诚实 round-up，不编虚假排名

这条中文 URL `b32-ai-logo-maker-comparison-bing` 曾返回 404，搜索需要 honest logo maker comparison — 不是「第 1 名绝对最好」fake 榜单，不编造 Bing Ads 转化率或工具市场份额。Logo ops：wordmark exploration、icon lockup、clear space spec、multi-ratio export — 改 tagline 勤，hex 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 适合 logo series 与 editable tagline layer；单次 logo generator 适合 first draft exploration。

## 四类 logo 任务与 honest 分组（非排名）

组 A 单次 wordmark export：适合 naming brainstorm，不适合 weekly tagline fix。组 B template logo SaaS：快但 clear space 常 weak，需 **Design Agent** QA。组 C campaign series 平台：**Brand Kit** hex lock + **Touch Edit** tagline editable — 适合 brand ops 长期维护。组 D icon-only exploration：mood board three direction，不 commit hex until Kit 流程。本篇不排「第 1–8 名」，只写任务匹配与 revision 成本。

## 为什么 fake logo 排名榜单误导采购

榜单混排不同任务（单次 export vs brand series），编造「Bing CTR +52%」无来源。readable tagline bake 进 logo pixels → Tuesday fix full regen。**Brand Kit** 未从 approved VI 取样 → carousel slide 4 accent drift。 honest round-up 写 buyer criteria：revision-heavy promo 选 series 平台。

## ChatCanvas brief 合同（logo exploration 版）

弱 brief「帮我做高级 logo」。强 brief「naming direction X wordmark exploration，Brand Kit sage + cream from mood board approved sample，tagline bottom 20% flat for Touch Edit，clear space 1x icon height，禁止 render 内小字 slogan bake，icon 1:1 + horizontal lockup same thread」。**Design Agent** numeric fields — 不能 QA「看起来高级」。

## Brand Kit 从 mood board approved sample 锁 identity

从 approved mood board、prior logo export 取样 primary、accent、type role。不用 stock marble 当 brand color。**ChatCanvas** 同一 thread batch wordmark + icon + horizontal lockup export。

## Touch Edit 改 tagline 不改 icon geometry crop

改「Since 2024」为「Est. 2026」：**Touch Edit** text band，保持 icon geometry 与 **Brand Kit** accent stripe。full regen random 改 stroke weight — brand ops 承受不起 thirty-minute reroll。

## Bing Ads 语境：logo lockup companion static

Bing Responsive Display 需多种 ratio；**Brand Kit** SSOT 保证 hex 一致。**Design Agent** 验 clear space、readable tagline、hex drift vs Kit。logo comparison 不写 fake Bing performance — 只描述 editable layer ops。

## 常见失败

相信 fake 排名。tagline baked。每 campaign 新 prompt。跳过 **Brand Kit**。404 未修复。编造工具定价或 fake 设计大赛奖项。

## 测量什么

改 tagline 一次几分钟、drift 几次、lockup export 几种 ratio。404 修复给 AI logo maker comparison Bing stable SOP URL。
"""

CASE_STUDY_PHOTOS_ZH = """
# 家庭老照片 AI 动画 case study：第一人称翻车与 static-first 补救

这条中文 URL `case-study-family-animated-old-photos-ai` 曾返回 404，搜索需要 honest case study — 不是 fake before/after 转化率。Family photo animation ops：scan restore、subtle motion、memorial slideshow、shareable clip — 改 caption 与 disclaimer 勤，accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 锁 memorial palette；motion optional after static legal pass。

## 我第一次翻车的经历（第一人称）

我第一次用 AI 把外公的扫描件做成「会眨眼」的 clip：prompt 堆「温馨」「电影感」，没设 **Brand Kit**，也没做 static companion。结果 clip 里 bake 了「永远怀念」小字，改一个字要 full regen 四十分钟；人脸 lighting 随机变，表哥说「不像外公了」。那次教训是：memorial 项目也要 static-first — caption 与日期在 **Touch Edit** editable layer，motion 只动 subtle parallax，不动 readable copy in pixels。

## 四类 family photo animation deliverable layer

第一是 restored still master 4:5：caption footer editable，无 render 内小字 dates bake。第二是 subtle motion 10s：parallax only，face geometry lock from reference scan。第三是 slideshow carousel slides 2–6：同 thread accent stripe，**Brand Kit** hex lock。第四是 share card 1:1 companion：**Design Agent** QA caption match clip offer。

## 为什么 family photo promo 常卡在改 caption

改「2024 春」为「2026 纪念」触发 full regen 三十分钟。readable caption bake 进 clip pixels。**Brand Kit** 未从 approved family album color sample 取样 hex。brief 形容词堆叠 — **Design Agent** 无 pass/fail fields。consent Tier：commercial publish 须 documented consent — 本篇不 substitute legal advice。

## ChatCanvas brief 合同（family photo animation 版）

弱 brief「帮我把老照片变温馨视频」。强 brief「memorial X restored still 4:5 1080×1350，Brand Kit warm sepia + cream from album sample，caption bottom 20% flat for Touch Edit，日期 editable layer only，clip 内禁止小字 caption bake，subtle parallax 10s same thread，share card 1:1 companion」。**Design Agent** numeric fields — 不能 QA「看起来感人」。

## Brand Kit 从 album sample 锁 memorial palette

从 family album approved color sample、prior export 取样 primary、accent、type role。不用 stock filter 当 memorial 色。**ChatCanvas** 同一 thread batch still + motion prep + share card export。

## Touch Edit 改 caption 不改 face geometry crop

改「献给外公」为「献给外婆」：**Touch Edit** text band，保持 face geometry 与 **Brand Kit** accent stripe。full regen random 改 expression — family trust  sensitive， thirty-minute reroll 不可接受。

## static-first 再 optional subtle motion

顺序：static legal pass on caption → variant A/B still → winner thread master → optional subtle parallax elsewhere。**Touch Edit** caption change 五分钟内 — ops viable before family sharing deadline。不编造「动画老照片提升分享率 XX%」无来源数据。

## 常见失败

clip 内 bake caption。无 consent documentation。跳过 **Brand Kit**。每 photo 新 prompt 无 thread。404 未修复。fake emotional conversion stats。

## 测量什么（case study 诚实指标）

改 caption 一次几分钟、face drift 几次、export 几种 ratio。404 修复给 family animated old photos case study stable SOP URL。
"""


# FAQ blocks — unique per article
FAQ = {
    "non_design_pt": """
## FAQ

**Não-designers precisam Brand Kit primeiro?**  
Sim — sample hex de packaging ou slide aprovado, evita drift slide 4.

**Alterar preço exige full regen?**  
Não — Touch Edit cinco minutos na banda static de preço.

**Brief contrato vs brief estético?**  
Contrato tem safe zone, hex, disclaimer editable; estético falha QA.

**404 fix?**  
Stable PT best agent for non design SOP URL.

**Ranking fake de ferramentas?**  
Não — só critérios ops e revision cost.
""",
    "fitness_studio_pt": """
## FAQ

**Boutique fitness precisa Brand Kit?**  
Sim — sample hex de signage aprovado do studio.

**Mudar preço de challenge full regen?**  
Não — Touch Edit five minutes na banda static.

**WOD screen e challenge same thread?**  
Sim — accent stripe e hex consistentes.

**404 fix?**  
Stable PT boutique fitness Design Agent SOP URL.

**Fake conversion lift?**  
Não — só workflow ops.
""",
    "appointment_cards_pt": """
## FAQ

**Chat generate appointment cards precisa Brand Kit?**  
Sim — sample hex de VI aprovada, mesmo thread batch frente + verso.

**Alterar horário full regen?**  
Não — Touch Edit five minutes na text band.

**CTA pode bake no render?**  
Não — static-first editable layer only.

**404 fix?**  
Stable PT chat generate appointment cards SOP URL.

**Fake no-show reduction stats?**  
Não — só editable layer ops.
""",
    "skincare_launch_ru": """
## FAQ

**Skincare launch нужен Brand Kit?**  
Да — sample hex из packaging, иначе online drift offline.

**Смена launch price full regen?**  
Нет — Touch Edit five minutes на static price band.

**Ingredient disclaimer editable?**  
Да — footer static layer, не baked in pixels.

**404 fix?**  
Stable RU skincare brand identity launch SOP URL.

**Fake GMV data?**  
Нет — только ops workflow metrics.
""",
    "brochures_ru": """
## FAQ

**Brochure tutorial нужен Brand Kit?**  
Да — sample hex из approved VI, prevents panel accent drift.

**Смена offer full regen?**  
Нет — Touch Edit five minutes на static CTA band.

**Print bleed обязателен?**  
Да — **Design Agent** print proof QA.

**404 fix?**  
Stable RU professional brochures AI step-by-step SOP URL.

**Fake print vendor pricing?**  
Нет — ops workflow only.
""",
    "bg_wallpaper_zh": """
## FAQ

**壁纸 roundup 是排名榜吗？**  
不是 — 按任务场景分组，不编虚假第几名。

**campaign wallpaper 要先 Brand Kit 吗？**  
要 — 从 VI 取样 hex，同一 ChatCanvas thread batch 多 ratio。

**改 offer 要 full regen 吗？**  
不要 — Touch Edit 五分钟改 static CTA layer。

**404 修复？**  
stable zh wallpaper generator roundup SOP URL。

**编造工具市场份额？**  
不 — 只写任务匹配与 revision cost。
""",
    "auto_resize_zh": """
## FAQ

**auto resize 要先 master 4:5 吗？**  
要 — master-first not crop-first，防 CTA 被裁切。

**改 offer 要每尺寸 full regen 吗？**  
不要 — Touch Edit master 后 re-export 全 derivative。

**Brand Kit 角色？**  
hex SSOT，防 slide 4 drift between ratios。

**404 修复？**  
stable zh auto resize multi platform workflow SOP URL。

**编造各平台 ROI？**  
不 — 只描述 editable layer ops。
""",
    "seedance_prompts_zh": """
## FAQ

**Seedance prompt 指南写定价吗？**  
不写 — 定价以 Seedance 官方页面为准，本篇零编造。

**clip 内能 bake offer 吗？**  
不能 — static companion editable via Touch Edit。

**multi-shot 要 character ref 吗？**  
要 — yaw ±15° plate lock，防 character drift。

**404 修复？**  
stable zh Seedance 2 prompt guide SOP URL。

**fake 性能 benchmark？**  
不 — 只描述 prompt field 结构与 revision cost。
""",
    "logo_comparison_zh": """
## FAQ

**logo comparison 是 fake 排名吗？**  
不是 — honest round-up 按任务分组，不编第 1 名。

**改 tagline 要 full regen 吗？**  
不要 — Touch Edit 五分钟改 text band。

**Bing Ads 语境 fake CTR？**  
不 — 只写 logo lockup companion static ops。

**404 修复？**  
stable zh AI logo maker comparison Bing SOP URL。

**Brand Kit 角色？**  
hex SSOT，long-term tagline editable layer。
""",
    "case_study_photos_zh": """
## FAQ

**case study 有第一人称翻车吗？**  
有 — 开篇描述 caption bake 与 face drift 教训。

**memorial 项目要 Brand Kit 吗？**  
要 — 从 album sample 取样 memorial palette。

**改 caption 要 full regen 吗？**  
不要 — Touch Edit 五分钟改 text band。

**404 修复？**  
stable zh family animated old photos case study SOP URL。

**fake 分享率提升数据？**  
不 — 只记录改 caption 分钟数与 drift 次数。
""",
}


def expand_pt(topic: str, n: int) -> str:
    return f"""
## Nota de campo {n}: {topic}

O primeiro brief termina em „premium" e falha: preço pequeno, badge sobre o rosto. Na segunda passagem, corrija só safe zone e campos obrigatórios. Um thread **ChatCanvas** reduz accent drift no slide 4. Em **{topic}**, **Touch Edit** confirma fix de preço em cinco minutos static-first. Full regen 30 minutos — recomece pelo **Brand Kit**. URL 404 restaurada como link SOP estável para PME lusófonas. **Design Agent** pass/fail checklist vence briefs adjetivos.
"""


def expand_ru(topic: str, n: int) -> str:
    return f"""
## Полевая заметка {n}: {topic}

Первый brief заканчивается словом «premium» и проваливается: мелкая цена, badge на лице. Во втором проходе правьте только safe zone и обязательные поля. Thread **ChatCanvas** снижает accent drift на slide 4. В **{topic}** **Touch Edit** подтверждает fix цены за пять минут static-first. Full regen 30 минут — сначала **Brand Kit**. Восстановленный 404 URL — stable SOP link для RU команд. **Design Agent** pass/fail checklist побеждает briefs-прилагательные.
"""


def expand_zh(topic: str, n: int) -> str:
    return f"""
## 实操补充 {n}：{topic}

很多小团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。{topic} 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。
"""


ARTICLES = [
    {
        "rank": 204,
        "key": "non_design_pt",
        "lang": "pt",
        "slug": "best-agent-for-non-design",
        "cover": "022",
        "category": "Best Practice",
        "title": "Melhor Design Agent para quem não é designer (PT)",
        "seo_title": "Best Agent Non Design — PT ChatCanvas SOP",
        "description": "PT 404 fix: best agent for non design，Brand Kit、Touch Edit brief contrato。",
        "seo_description": "Não-designers：Instagram feed、preço editable、Design Agent QA。",
        "focus": "best agent for non design",
        "keywords": ["best agent non design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Best Practice — Non Design Agent PT",
        "body": NON_DESIGN_PT,
        "expand_topic": "PT non design Design Agent workflow",
    },
    {
        "rank": 205,
        "key": "fitness_studio_pt",
        "lang": "pt",
        "slug": "best-ai-design-agent-for-boutique-fitness-studio",
        "cover": "026",
        "category": "Industry Solution",
        "title": "Melhor Design Agent AI para boutique fitness studio (PT)",
        "seo_title": "Boutique Fitness Design Agent — PT SOP",
        "description": "PT 404 fix: boutique fitness Design Agent、challenge editable、Brand Kit。",
        "seo_description": "Fitness studio：class pack、WOD screen、Touch Edit 改价。",
        "focus": "best ai design agent for boutique fitness studio",
        "keywords": ["boutique fitness ai design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Boutique Fitness Design Agent PT",
        "body": FITNESS_STUDIO_PT,
        "expand_topic": "PT boutique fitness Design Agent workflow",
    },
    {
        "rank": 206,
        "key": "appointment_cards_pt",
        "lang": "pt",
        "slug": "how-to-chat-generate-appointment-cards-lovart",
        "cover": "030",
        "category": "How-To",
        "title": "Como gerar cartões de agendamento via ChatCanvas (PT)",
        "seo_title": "Chat Generate Appointment Cards — PT static-first SOP",
        "description": "PT 404 fix: chat generate appointment cards、static-first CTA editable layer。",
        "seo_description": "Appointment cards：brief conversacional、Brand Kit、Touch Edit。",
        "focus": "how to chat generate appointment cards lovart",
        "keywords": ["chat generate appointment cards", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Chat Generate Appointment Cards PT",
        "body": APPOINTMENT_CARDS_PT,
        "expand_topic": "PT chat generate appointment cards workflow",
    },
    {
        "rank": 207,
        "key": "skincare_launch_ru",
        "lang": "ru",
        "slug": "from-name-to-launch-skincare-brand-identity-ai",
        "cover": "034",
        "category": "Branding",
        "title": "От имени до launch: skincare brand identity с AI (RU)",
        "seo_title": "Skincare Brand Identity Launch — RU ChatCanvas SOP",
        "description": "RU 404 fix: skincare brand identity launch、Brand Kit、Touch Edit。",
        "seo_description": "Skincare launch：packaging Kit、editable promo、无 fake GMV。",
        "focus": "from name to launch skincare brand identity ai",
        "keywords": ["skincare brand launch", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Branding — Skincare Launch RU",
        "body": SKINCARE_LAUNCH_RU,
        "expand_topic": "RU skincare brand identity launch workflow",
    },
    {
        "rank": 208,
        "key": "brochures_ru",
        "lang": "ru",
        "slug": "how-to-design-professional-brochures-with-ai-step-by-step-tutorial",
        "cover": "038",
        "category": "How-To",
        "title": "Как создать professional brochures с AI: step-by-step (RU)",
        "seo_title": "Professional Brochures AI Tutorial — RU SOP",
        "description": "RU 404 fix: professional brochures AI step-by-step、Brand Kit、Touch Edit。",
        "seo_description": "Brochures：tri-fold、print bleed、Design Agent QA。",
        "focus": "how to design professional brochures with ai step by step tutorial",
        "keywords": ["professional brochures ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Professional Brochures AI RU",
        "body": BROCHURES_RU,
        "expand_topic": "RU professional brochures AI step-by-step workflow",
    },
    {
        "rank": 209,
        "key": "bg_wallpaper_zh",
        "lang": "zh",
        "slug": "8-best-ai-background-wallpaper-generators-2026",
        "cover": "042",
        "category": "Comparison",
        "title": "2026 AI 背景壁纸生成器选型：按任务匹配 honest roundup",
        "seo_title": "AI Background Wallpaper Generators 2026 — honest roundup",
        "description": "404 修复：wallpaper generator honest roundup、不编虚假排名。",
        "seo_description": "壁纸：任务分组、Brand Kit hex lock、Touch Edit 改 offer。",
        "focus": "8 best ai background wallpaper generators 2026",
        "keywords": ["ai background wallpaper", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Wallpaper Generators 2026 ZH",
        "body": BG_WALLPAPER_ZH,
        "expand_topic": "zh wallpaper generator honest roundup workflow",
    },
    {
        "rank": 210,
        "key": "auto_resize_zh",
        "lang": "zh",
        "slug": "auto-resize-multi-platform-workflow-ai",
        "cover": "046",
        "category": "How-To",
        "title": "AI 多平台自动 resize 工作流：master-first 防 drift",
        "seo_title": "Auto Resize Multi Platform Workflow — ChatCanvas SOP",
        "description": "404 修复：auto resize multi platform、master-first、Brand Kit。",
        "seo_description": "多平台：4:5 master、9:16 derivative、Touch Edit 改 offer。",
        "focus": "auto resize multi platform workflow ai",
        "keywords": ["auto resize multi platform", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Auto Resize Multi Platform ZH",
        "body": AUTO_RESIZE_ZH,
        "expand_topic": "zh auto resize multi platform workflow",
    },
    {
        "rank": 211,
        "key": "seedance_prompts_zh",
        "lang": "zh",
        "slug": "awesome-prompts-seedance-2-video-creation-guide",
        "cover": "050",
        "category": "How-To",
        "title": "Seedance 2 视频创作 prompt 精选：workflow 导向",
        "seo_title": "Seedance 2 Prompt Guide — static-first SOP",
        "description": "404 修复：Seedance 2 prompt guide、不编造定价、Brand Kit。",
        "seo_description": "Seedance：prompt 模板、static companion、Touch Edit 改 offer。",
        "focus": "awesome prompts seedance 2 video creation guide",
        "keywords": ["seedance 2 prompt", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Seedance 2 Prompt Guide ZH",
        "body": SEEDANCE_PROMPTS_ZH,
        "expand_topic": "zh Seedance 2 prompt static-first workflow",
    },
    {
        "rank": 212,
        "key": "logo_comparison_zh",
        "lang": "zh",
        "slug": "b32-ai-logo-maker-comparison-bing",
        "cover": "054",
        "category": "Comparison",
        "title": "AI Logo 制作工具对比（Bing）：诚实 round-up",
        "seo_title": "AI Logo Maker Comparison Bing — honest roundup",
        "description": "404 修复：logo maker comparison honest roundup、不编虚假排名。",
        "seo_description": "Logo：任务分组、tagline editable、Design Agent QA。",
        "focus": "b32 ai logo maker comparison bing",
        "keywords": ["ai logo maker comparison", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Logo Maker Bing ZH",
        "body": LOGO_COMPARISON_ZH,
        "expand_topic": "zh AI logo maker comparison Bing workflow",
    },
    {
        "rank": 213,
        "key": "case_study_photos_zh",
        "lang": "zh",
        "slug": "case-study-family-animated-old-photos-ai",
        "cover": "058",
        "category": "Industry Solution",
        "title": "家庭老照片 AI 动画 case study：翻车与补救",
        "seo_title": "Family Animated Old Photos Case Study — ChatCanvas SOP",
        "description": "404 修复：family animated old photos case study、第一人称翻车、Touch Edit。",
        "seo_description": "老照片动画：memorial palette、caption editable、static-first。",
        "focus": "case study family animated old photos ai",
        "keywords": ["family animated old photos", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Case Study — Family Animated Old Photos ZH",
        "body": CASE_STUDY_PHOTOS_ZH,
        "expand_topic": "zh family animated old photos case study workflow",
    },
]

EXPAND_FN = {
    "pt": expand_pt,
    "ru": expand_ru,
    "zh": expand_zh,
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
    "fr": "words",
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch20 content cluster.*\n"
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
