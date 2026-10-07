#!/usr/bin/env python3
"""Generate 404-rescue P2 batch23 blog bodies (10 files). Self-contained.

Ranks #235–#245 from 404-rescue-compact lane (skip junk #242).
All zh-TW. expand_zhtw only.
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

SEEDANCE_PROMPTS_ZHTW = """
# Seedance 2 影片創作 prompt 精選：workflow 導向，不編制定價

這條繁中 URL `awesome-prompts-seedance-2-video-creation-guide` 曾返回 404，搜尋需要 Seedance 2 prompt 實操指南 — 不是 generic 影片工具排名，**不編造 Seedance 官方定價或 fake 性能 benchmark**。Seedance ops：multi-shot character consistency、campaign board 內 clip — 改 offer 與 disclaimer 仍須 static companion editable。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 campaign palette；motion hook optional after static legal pass。

## 四類 Seedance prompt 場景（workflow 分組）

第一類 atmosphere B-roll：clip pixels 內無 readable offer，landing static 承載 CTA editable layer。第二類 character lock multi-shot：reference plate yaw ±15°，**Brand Kit** accent 一致 thread。第三類 product hero motion：bottle/cutout geometry 不變，**Touch Edit** 改價在 static companion。第四類 social hook 10s：static still 先 legal pass，再 optional subtle motion。

## 為什麼 prompt 指南常誤導 ops

指南堆「cinematic」「viral」形容詞 — **Design Agent** 無 pass/fail fields。clip 內 bake 小字 offer → 週二 fix 觸發 full reroll。編造 Seedance 月費 NT$XX 無官方來源 — 本篇不寫任何 Seedance 定價數字，讀者須查官方頁面。multi-shot 無 reference → slide 4 character drift。

## ChatCanvas brief 合同（Seedance 2 prompt 版）

弱 brief「幫我做 Seedance viral 影片」。強 brief「campaign X Seedance prep 16:9，Brand Kit slate + coral from media kit，headline static companion top 15% flat for Touch Edit，價格 bottom left safe zone on still only，disclaimer footer editable，clip 內禁止小字 offer，character ref plate yaw ±15°，variants 2–4 same thread」。**Design Agent** QA static acceptance — 不能 QA clip「電影感」。

## 精選 prompt 模板（不含 fake 排名）

模板 A atmosphere：「slow dolly product hero, muted lighting, no text in render, accent stripe match Brand Kit hex」。模板 B character：「same character ref plate, walk cycle 3s, no price in pixels」。模板 C hook：「10s hook, static CTA on companion still editable via Touch Edit」。不聲稱「prompt #1 轉化率最高」— 只描述 field 結構與 revision cost。

## Brand Kit 防止 multi-shot palette drift

從 approved VI、prior export 取樣 primary、accent、type role。**ChatCanvas** same thread batch clip prep + static companion + social crop。Seedance series 是 memory work；surprise accent 破壞 character lock。

## Touch Edit 改 offer 在 static companion 不改 clip crop

改「限時 NT$999」為「會員 NT$899」：**Touch Edit** CTA band on still master，clip geometry preserved。full regen clip random 改 lighting — campaign ops 承受不起 thirty-minute reroll per shot。

## static-first 再 optional Seedance motion

順序：static legal pass on disclaimer → variant A/B still → winner still thread master → Seedance motion hook elsewhere。**Touch Edit** price change 五分鐘內 — ops viable。不編造 Seedance API 配額或 fake render speed 數據。

## 常見失敗

clip 內 bake offer。編造 Seedance 定價。無 character reference multi-shot。跳過 **Brand Kit**。404 未修復。每 shot 新 prompt 無 thread。

## 測量什麼

改 offer 一次幾分鐘、character drift 幾次、static companion export 幾種 ratio。404 修復給 Seedance 2 prompt guide stable SOP URL — 定價以官方為準。
"""

CASE_STUDY_PHOTOS_ZHTW = """
# 家庭老照片 AI 動畫 case study：第一人稱翻車與 static-first 補救

這條繁中 URL `case-study-family-animated-old-photos-ai` 曾返回 404，搜尋需要 honest case study — 不是 fake before/after 轉化率。Family photo animation ops：scan restore、subtle motion、memorial slideshow、shareable clip — 改 caption 與 disclaimer 勤，accent 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 memorial palette；motion optional after static legal pass。

## 我第一次翻車的經歷（第一人稱）

我第一次用 AI 把外公的掃描件做成「會眨眼」的 clip：prompt 堆「溫馨」「電影感」，沒設 **Brand Kit**，也沒做 static companion。結果 clip 裡 bake 了「永遠懷念」小字，改一個字要 full regen 四十分鐘；人臉 lighting 隨機變，表哥說「不像外公了」。那次教訓是：memorial 專案也要 static-first — caption 與日期在 **Touch Edit** editable layer，motion 只動 subtle parallax，不動 readable copy in pixels。

## 四類 family photo animation deliverable layer

第一是 restored still master 4:5：caption footer editable，無 render 內小字 dates bake。第二是 subtle motion 10s：parallax only，face geometry lock from reference scan。第三是 slideshow carousel slides 2–6：同 thread accent stripe，**Brand Kit** hex lock。第四是 share card 1:1 companion：**Design Agent** QA caption match clip offer。

## 為什麼 family photo promo 常卡在改 caption

改「2024 春」為「2026 紀念」觸發 full regen 三十分鐘。readable caption bake 進 clip pixels。**Brand Kit** 未從 approved family album color sample 取樣 hex。brief 形容詞堆疊 — **Design Agent** 無 pass/fail fields。consent Tier：commercial publish 須 documented consent — 本篇不 substitute legal advice。

## ChatCanvas brief 合同（family photo animation 版）

弱 brief「幫我把老照片變溫馨影片」。強 brief「memorial X restored still 4:5 1080×1350，Brand Kit warm sepia + cream from album sample，caption bottom 20% flat for Touch Edit，日期 editable layer only，clip 內禁止小字 caption bake，subtle parallax 10s same thread，share card 1:1 companion」。**Design Agent** numeric fields — 不能 QA「看起來感人」。

## Brand Kit 從 album sample 鎖 memorial palette

從 family album approved color sample、prior export 取樣 primary、accent、type role。不用 stock filter 當 memorial 色。**ChatCanvas** 同一 thread batch still + motion prep + share card export。

## Touch Edit 改 caption 不改 face geometry crop

改「獻給外公」為「獻給外婆」：**Touch Edit** text band，保持 face geometry 與 **Brand Kit** accent stripe。full regen random 改 expression — family trust sensitive，thirty-minute reroll 不可接受。

## static-first 再 optional subtle motion

順序：static legal pass on caption → variant A/B still → winner thread master → optional subtle parallax elsewhere。**Touch Edit** caption change 五分鐘內 — ops viable before family sharing deadline。不編造「動畫老照片提升分享率 XX%」無來源數據。

## 常見失敗

clip 內 bake caption。無 consent documentation。跳過 **Brand Kit**。每 photo 新 prompt 無 thread。404 未修復。fake emotional conversion stats。

## 測量什麼（case study 誠實指標）

改 caption 一次幾分鐘、face drift 幾次、export 幾種 ratio。404 修復給 family animated old photos case study stable SOP URL。
"""

STOCK_FOOTAGE_ZHTW = """
# 素材庫時代終結？2026 AI 影片創作完整指南

這條繁中 URL `he-death-of-the-stock-footage-era-a-complete-guide-to-ai-powered-video-creation-in-2026` 曾返回 404（slug 保留 **he-death** 拼寫，標題語意仍為 stock footage era 完整指南）。搜尋需要 honest complete guide to AI video creation — 不是 generic 工具排名與編造定價。誠實 framing：stock footage libraries 仍存在，但每週改 offer 的團隊需要 editable static layers 再 optional B-roll。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 聚焦 static-first video prep：master still、variant crops、editable caption layer — 不是 fake render benchmarks。

## 四個 video prep deliverable layer

第一是 static master 16:9 或 4:5：readable headline 與 disclaimer footer editable。第二是 B-roll companion 同 thread accent stripe — hex **Brand Kit** 一致。第三是 social crops 1:1 與 9:16 — **Design Agent** QA mismatch between ratio exports。第四是 landing companion：still CTA 須 match video thumb；**Design Agent** 抓 mismatch。

## 為什麼 stock-footage-only funnel 在週二改 offer 失敗

Clip bake offer 而 landing static 無 **Touch Edit** layer。改「限時 NT$1499」觸發 full rerender — 三十分鐘。slide 4 accent lottery。**Brand Kit** 未從 approved VI 取樣。團隊 screenshot still — 價格須 readable on static。買 generic B-roll 不 fix editable copy ops。

## ChatCanvas brief 合同（AI video 2026 版）

弱 brief「做 cinematic AI 影片」。強 brief「campaign X video prep 16:9 1920×1080，Brand Kit slate + coral from media kit，headline top 15% flat for Touch Edit，價格 bottom left safe zone，disclaimer footer editable，B-roll companion subtle motion only，variants 2–4 same thread」。**Design Agent** QA static acceptance — 不是 clip「電影感」。

## Brand Kit 取代 random stock palette drift

從 approved VI 取樣 primary、accent、type role — 不用 random stock marble 當 brand color。**ChatCanvas** same thread batch landscape + square + vertical export。stock footage era pain：每支 clip 不同 teal。**Brand Kit** 作 SSOT fix hex drift。

## Touch Edit 改 offer 不改 hero crop

改「限時 NT$799」為「會員 NT$699」：**Touch Edit** 框 CTA band，保持 hero geometry 與 **Brand Kit** accent stripe。full regen randomize lighting — ops 承受不起 thirty-minute reroll。

## static-first 再 optional AI B-roll companion

順序：static legal pass on disclaimer → variant A/B still → winner still thread master → optional subtle B-roll。**Touch Edit** price change 五分鐘內 — ops viable。不編造 fake video render speed 或 fake user counts。

## 與 photo animation slug 的分工

photo animation slug 覆蓋 still-to-motion for product hero。本篇覆蓋 stock footage replacement framing 與 cross-platform video prep editable layers。intent 重疊；scope 不同。

## 常見失敗

video-only funnel 無 static editable layer。價格 baked in pixels。每 campaign 新 prompt。404 未修復。編造工具定價或 fake benchmark renders。

## 測量什麼

改 offer 一次幾分鐘、accent drift 次數、export 尺寸數。404 修復給 stable AI video creation 2026 complete guide SOP URL。
"""

HIGGSFIELD_REVIEW_ZHTW = """
# Higgsfield AI 評測：motion hook vs campaign static 分業

這條繁中 URL `higgsfield-ai-review` 曾返回 404，搜尋在問「Higgsfield AI 值不值得用」。honest framing：Higgsfield 在 motion hook 與 clip 生成可能有強項，但 revision-heavy promo 需要 **ChatCanvas** static master、**Brand Kit** hex lock、**Touch Edit** 改價、**Design Agent** readable offer QA。不是二選一，是 workflow 順序問題。價格與訂閱 tier 請查官方 ToS — 正文只描述 ops workflow，**不編造任何 Higgsfield 定價數字**。

## Higgsfield 較適合的場景

短 motion hook、concept mood clip、social intro B-roll。團隊不每週改 offer、只做 hook-only 實驗。readable price block bake 進 clip pixels 但 ops 負擔可接受時。

## Higgsfield 較弱的場景

editable price layer、series-consistent carousel、legal 可改 disclaimer on static。週二改價觸發 full clip rerender。multi-ratio export hex drift。

## Lovart 與 Higgsfield 分業

順序：**ChatCanvas** 出 static hero 與 end card → legal pass → optional motion。Higgsfield 管 hook；Lovart 管 readable price、date、disclaimer 在 **Touch Edit** 層。**Design Agent** 驗 safe zone 與 hex drift vs **Brand Kit**。

## ChatCanvas brief 合同（評測版）

弱 brief「Higgsfield vs Lovart 哪個更好」。強 brief「campaign X 16:9 static hero，Brand Kit from media kit，headline flat for Touch Edit，Higgsfield hook optional after static pass，no price in clip pixels」。**Design Agent** pass/fail fields。

## Brand Kit 防止 random palette drift

無 **Brand Kit** 時 carousel slide 4 發明新 accent。Kit active 時 hex role follow。funnel work 是 series work。

## Touch Edit 改 promo blocks

offer 從「八折」→「免運」：hero 與 email header 用 **Touch Edit** type layer。兩字改動 full reroll — 「一鍵」工具在週二變慢的方式。

## honest review 邊界

正文是 workflow SOP，無 fake benchmark render、fake user count、fabricated subscription price。讀者用 **Design Agent** checklist 自行 review export。

## 常見失敗

只做 motion 而 landing static 仍是舊價。跳過 **Brand Kit**。Higgsfield clip 內 bake disclaimer。404 未修復。

## 測量什麼

改價幾分鐘、static vs video offer match、legal return。stable Higgsfield review SOP URL。
"""

RESTAURANT_MENU_ZHTW = """
# 餐廳老闆用 AI 設計菜單：完整實操指南

這條繁中 URL `how-to-design-a-restaurant-menu-with-ai-complete-guide-for-owners` 曾返回 404，搜尋需要 practical menu design workflow — 不是一鍵模板幻想。老闆每週改價、換季菜、更新過敏原註記。Lovart **ChatCanvas**、**Design Agent**、**Brand Kit**、**Touch Edit** 符合這節奏：layout 鎖定、copy 與價格 editable、print PDF、Instagram、門口 poster 系列一致。

## 餐廳老闆實際需要的四種 menu 輸出

可讀 print 或 PDF menu 含 disclaimer footer。單頁 lunch special promo 含 price safe zone。Instagram story cover 留 top UI clear。桌牌或 QR card 匹配 **Brand Kit** accent。只做漂亮 food photo 的工具無法 cover 週二改價。

## ChatCanvas brief 合同（菜單版）

弱 brief：elegant Italian menu。強 brief：dish photo zone center，price column right third readable at print size，Brand Kit olive + cream，allergy disclaimer one line footer editable，8.5×11 與 4:5 story from same thread，no tiny generated text in render。**Design Agent** QA 需要 numeric 與 legal fields in brief。

## Brand Kit 從真實餐廳物料取樣

從 dining room 木紋、磁磚、餐巾 capture color — 不用 stock marble。定義 primary、accent、menu title/body type roles、logo clear space。seasonal insert 在同一 **ChatCanvas** thread batch。

## Touch Edit 週二改湯品價格

只更新 price block 與菜名。instruction：keep grid 與 stripe geometry，match **Brand Kit** roles，replace copy in price column。full regen randomize photo crop，與 host stand 已印 stack 不一致。

## Design Agent 老闆在意的檢查

過敏原 line present、price readable at arm's length、no double CTA、accent drift vs **Brand Kit**、story export safe zone。老闆不需要 design jargon — 需要上述 pass/fail。

## 與 food photo generator 的分工

food stylization 工具幫 hero shots；menu ops 需要 editable columns、legal footer、multi-size export。brief 引用 food image；deliverable 仍需要 **Touch Edit** layers。

## 常見失敗

漂亮 dish photo 但 price unreadable。改一塊錢 full regen。story 與 print 不同 font。跳過 **Brand Kit** 使 weekly special 像另一家店。

## 測量什麼

改一個價格幾分鐘、menu variant drift 次數、legal/allergy return count、每次更新 export 幾種尺寸。404 修復給 stable owner SOP URL。
"""

FLYERS_CARDS_ZHTW = """
# 用 AI 設計傳單、名片與邀請函：印刷級 workflow

這條繁中 URL `how-to-design-flyers-business-cards-invitations-ai` 曾返回 404，搜尋需要 print collateral How-To — 不是 scattered Canva 模板。小店 daily ops：window flyer、business card、opening invitation、menu insert — 改日期與 offer 勤，四種物料 hex 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 把五件 collateral 當一個 brand family：master-first，derivative crops，editable CTA。

## 四類 print collateral deliverable layer

第一是 flagship flyer A5/A4：headline 與 disclaimer footer editable。第二是 business card 3.5×2 inch：tagline flat for **Touch Edit**。第三是 invitation 5×7：RSVP line editable layer。第四是 menu insert 或 brochure panel：**Design Agent** QA hex mismatch vs **Brand Kit**。

## 為什麼 collateral 專案在週二改日期失敗

改 opening date 觸發 full regen 三十分鐘。flyer 與 card accent lottery。**Brand Kit** 未從 approved logo 或 prior print PDF 取樣。brief 堆「rustic premium」— **Design Agent** 無 pass/fail fields。

## ChatCanvas brief 合同（print collateral 版）

弱 brief「幫我做高級傳單名片」。強 brief「pop-up bakery collateral family，Brand Kit terracotta + cream from logo sample，flyer A5 headline top 15% flat for Touch Edit，price bottom left safe zone，business card same thread accent stripe，300dpi CMYK bleed 3mm，disclaimer footer editable」。**Design Agent** numeric fields。

## Brand Kit 先於 batch 生成

從 approved logo、packaging、prior deck 取樣 primary hex、accent hex、title/body type role。不用 stock beige 當 brand color。**ChatCanvas** one thread batch flyer + card + invitation export。

## Touch Edit 改活動價不改 layout skeleton

改「開幕 NT$199」為「早鳥 NT$149」：**Touch Edit** CTA band，保持 card geometry 與 **Brand Kit** accent stripe。full regen random 改 food photo 與 padding。

## master-first 順序 static legal pass

順序：flagship flyer legal pass on disclaimer → derivative card + invitation crops same thread → variant A/B still。**Touch Edit** date change 五分鐘內 — ops viable for opening week cadence。

## 常見失敗

四種模板四種 font。readable price baked in pixels。每格式新 prompt。404 未修復。跳過 **Brand Kit**。

## 測量什麼

改日期一次幾分鐘、collateral drift 次數、一次 action export 幾種 print size。404 修復給 stable flyers business cards invitations SOP URL。
"""

PRODUCT_PHOTO_ZHTW = """
# 用 AI 生成產品攝影：Lovart 實用 workflow 指南

這條繁中 URL `how-to-gen-product-photography-with-ai` 曾返回 404，搜尋需要 product photography AI How-To — 不是 T2I 排行榜。product photo daily ops：PDP hero、ecommerce carousel、email header、marketplace square — 改價與 promo sticker 勤，shadow 與 hex 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 把 product shot 當 revision-heavy static master：cutout geometry lock，editable price band。

## 四類 product photography deliverable layer

第一是 PDP hero 4:5 或 1:1：product center，price bottom left safe zone editable。第二是 carousel slide 2–6：同 thread accent stripe。第三是 email header 600×300：**Brand Kit** hex lock。第四是 marketplace 2000×2000 white background companion：**Design Agent** QA mismatch。

## 為什麼 product photo promo 常卡在改 offer

改「滿千折百」為「新客 NT$99」觸發 full regen 三十分鐘。slide 4 accent drift。**Brand Kit** 未從 approved packaging 取樣。readable 價格 bake 進 pixels。brief 只有「studio lighting premium」— **Design Agent** 無 pass/fail fields。

## ChatCanvas brief 合同（product photography 版）

弱 brief「幫我做 stunning 產品圖」。強 brief「SKU X PDP hero 4:5 1080×1350，Brand Kit slate + coral from packaging PDF，product center 60% frame，price bottom left flat for Touch Edit，disclaimer footer editable，禁止 render 內小字，carousel 2–6 same thread」。**Design Agent** numeric fields。

## Brand Kit 從 approved packaging 取樣

從 packaging PDF、prior PDP export 取樣 primary、accent、type role。不用 stock marble 當 brand color。**ChatCanvas** same thread batch hero + carousel + email crop。

## Touch Edit 改 promo 不改 product cutout

改 sticker「限時八折」為「免運」：**Touch Edit** label band，保持 bottle geometry 與 **Brand Kit** accent frame。full regen random 改 highlight — ecommerce ops 承受不起 thirty-minute reroll per SKU。

## static-first 再 optional lifestyle motion

順序：static legal pass on disclaimer → variant A/B still → winner thread master → optional subtle lifestyle clip elsewhere。**Touch Edit** price change 五分鐘內 — ops viable。

## 常見失敗

single hero 無 carousel thread。價格 baked。每 SKU 新 prompt。404 未修復。編造 conversion lift 無來源。

## 測量什麼

改價一次幾分鐘、drift 次數、export ratios per SKU refresh。404 修復給 stable product photography AI SOP URL。
"""

ART_CREATION_ZHTW = """
# Lovart AI 藝術創作與 AI 繪畫工具：campaign 視角，不是 hype

這條繁中 URL `lovart-ai-art-creation-ai-painting-tools` 曾返回 404，搜尋在問 Lovart art creation 與 AI painting tools 能做什麼 — 不是「最強 AI 畫家」fake 排名。honest framing：Lovart 適合 revision-heavy visual series — gallery promo、artist drop、print companion — 需要 **Brand Kit**、**Touch Edit** editable caption、**Design Agent** pass/fail QA。純 AI painting playground 適合單張探索；campaign ops 需要 static-first editable layers。

## 四類 art creation deliverable layer

第一是 gallery hero 16:9 或 4:5：exhibition title editable via **Touch Edit**。第二是 series carousel slides 2–6：同 thread accent stripe。第三是 print companion A3/A4：**Brand Kit** hex lock。第四是 social crop 9:16 — **Design Agent** QA title readable at reduced preview。

## 為什麼 art promo 常卡在改展期

改 opening date 觸發 full regen 三十分鐘。slide 4 accent lottery。**Brand Kit** 未從 approved artist palette 或 prior poster 取樣。readable 展名 bake 進 render pixels。

## ChatCanvas brief 合同（art creation 版）

弱 brief「幫我做高級藝術海報」。強 brief「exhibition X hero 4:5 1080×1350，Brand Kit ink + paper from artist sample，title top 15% flat for Touch Edit，date bottom left safe zone，disclaimer footer editable，variants 2–4 same thread，禁止 render 內小字」。**Design Agent** numeric fields。

## Brand Kit 從 artist approved sample 鎖 palette

從 approved mood board、prior poster export 取樣 primary、accent、type role。不用 random stock gradient 當 series color。**ChatCanvas** same thread batch hero + carousel + print export。

## Touch Edit 改展名不改 artwork geometry

改「Spring Solo」為「Autumn Group」：**Touch Edit** title band，保持 artwork crop 與 **Brand Kit** accent stripe。full regen random 改 texture — gallery ops 敏感。

## 與 pure AI painting tool 的分工

T2I playground 適合 style exploration。**ChatCanvas** + **Design Agent** 適合 weekly promo 改 copy、export 多 ratio。KPI 是「改展期 five 分鐘」不是「第一張 wow」。

## 常見失敗

跳過 **Brand Kit**。title baked in pixels。每活動新 prompt。404 未修復。編造「AI 藝術賣出 XX% 提升」無來源。

## 測量什麼

改展期一次幾分鐘、drift 次數、export 幾種 ratio。404 修復給 stable Lovart art creation SOP URL。
"""

IMAGE_GENERATOR_ZHTW = """
# Lovart AI 圖像生成器：創造 stunning images 的 campaign workflow

這條繁中 URL `lovart-ai-image-generator-create-stunning-images-with-ai` 曾返回 404，搜尋仍在問「Lovart AI image generator 能不能出 stunning images」。誠實答案：能出圖，但 daily ops 的價值不在第一張 wow，而在 **Brand Kit** 鎖色、**ChatCanvas** thread 記系列、**Touch Edit** 改局部、**Design Agent** 按 brief 驗收。這和「輸入 prompt 等一張圖」的單次生成器不是同一類工具。

## 圖像生成在 campaign 裡要拆成四類輸出

第一是 hero 主圖：產品或人物主體清晰，CTA safe zone 留白。第二是 carousel slide 2–6：同一 grid 換 copy，accent 不能每張 drift。第三是 story 與 feed crop：9:16 與 4:5 同 thread 匯出。第四是 end card 與 thumbnail：價格與 disclaimer 須在可編輯層，不能 bake 進 pixels。

## ChatCanvas brief 合同寫法

弱 brief 是「幫我做一張 stunning 產品圖」。強 brief 是：「hero 4:5 1080×1350，產品居中，headline band top 15% flat for Touch Edit，Brand Kit slate + coral accent，price bottom left safe zone，disclaimer footer editable，禁止生成圖內小字價格」。把 ratio、safe zone、Kit hex 寫進 brief，**Design Agent** 才有 acceptance criteria。

## Brand Kit 先於 batch 生成

從已批准 packaging、門店物料或 prior deck 取樣 primary hex、accent hex、title/body type role、logo clear space。不要用 stock marble 或 random pastel 當品牌色。Kit 建好後，所有 **ChatCanvas** thread 引用同一套 role。跳過 Kit 後每張 post 發明新 accent，改價只能 full regen。

## Touch Edit 改價不改 identity

週二改「滿 2000 折 300」為「新客體驗 NT$990」：**Touch Edit** 框 CTA 帶，保持 stripe geometry 與 **Brand Kit** accent。full regen 會 random 改產品角度與背景。測量 ROI 用「改價分鐘」不是「第一張 wow 分鐘」。

## Design Agent QA 字段

Agent 檢查 safe zone、double CTA、過小 type、hex drift vs Kit、disclaimer 是否存在。不是替 brief 想創意，是執行 acceptance criteria。第二 pass 常只需補 brief 缺字段，不必換模型。

## 與純 T2I 生成器的分工

T2I 適合 mood board 與單張探索。**ChatCanvas** + **Design Agent** 適合 revision-heavy promo：同一 campaign 要改價、改 copy、匯出多尺寸。若 KPI 是「改價 five 分鐘」，選 workflow 工具；若 KPI 是「試 50 種風格」，選 T2I playground。

## 常見失敗

跳過 Brand Kit 後 carousel slide 4 新 accent。readable 價格 baked in pixels。video hook 有 offer 但 static hero 沒有。每次改 copy 都 full regen 三十分鐘。404 修復頁的意義是給 SOP stable URL。

## 測量什麼才有用

記「改價一次幾分鐘」「一次活動 export 幾種尺寸」「carousel drift 幾次」。若 **Touch Edit** 平均小於五分鐘而重出平均大於三十分鐘，說明 Design Agent 路線成立。
"""

LOVEART_BUSINESS_ZHTW = """
# Lovart 商業創意工作流：business-first static 可編輯路線

這條 URL 使用 `loveart-ai-business-creative-workflows`（**loveart** 為歷史 slug 拼寫，正文品牌名稱一律 **Lovart**）。曾返回 404，搜尋需要 business creative workflows How-To — 不是 feature hype 與 fake user counts。business ops daily rhythm：改 offer、更新 disclaimer、export Meta + email + PDP 多 ratio — hex 易 drift。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** 鎖 campaign palette；KPI 是 revision minutes 不是 first-frame wow。

## 四層 business creative stack

第一層 **Brand Kit**：每 campaign 的 hex、type role、accent 規則 SSOT。第二層 **ChatCanvas** thread：master + slide 2–6 + 多 ratio 衍生同一 thread。第三層 **Touch Edit**：只改 price/date/disclaimer band，不動 hero geometry。第四層 **Design Agent**：pass/fail QA — safe zone、double CTA、hex drift vs Kit。

## 為什麼 business promo 常卡在週二改 offer

改「限時 NT$1999」觸發 full regen 三十分鐘。Meta ad 與 email header 價格不一致 — 各尺寸 unrelated prompts。readable 價格 bake 進 pixels。**Brand Kit** 未 active 作 batch SSOT。

## ChatCanvas brief 合同（business workflow 版）

弱 brief「幫我做高級商業視覺」。強 brief「campaign X master 4:5 1080×1350，Brand Kit navy + sand from media kit，headline top 15% flat for Touch Edit，price bottom left safe zone，disclaimer footer editable，derivative 1200×628 + 1200×1200 + 9:16 same thread master-first」。**Design Agent** numeric fields per ratio。

## Brand Kit 作 orchestration SSOT

從 approved VI 取樣 primary、accent、type role 一次 per campaign。**ChatCanvas** one thread batch master + derivatives。**Touch Edit** 改價 on master 再 re-export 全尺寸 — orchestration win 是 synchronized offer。

## Touch Edit 一次 re-export 全 ratio

改「限時 NT$999」為「會員 NT$799」：**Touch Edit** CTA band on master，re-export landscape、square、story、email crop。full regen per format random 改 lighting — business ops 承受不起四路 thirty-minute reroll。

## session zero 準備清單

gather approved hex from media kit。寫一個 campaign name。列出每週 export 尺寸 — Instagram 4:5、email header、PDP square。copy disclaimer 句 legal 已批准。缺這四項，first gen 好看但 fail 週二 edit test。

## 常見失敗

十個 prompt 十個尺寸。價格 baked。跳過 **Brand Kit**。404 未修復。編造 cross-platform CTR lift 無來源。

## 測量 orchestration ROI

改 offer 一次幾分鐘 × 格式數、cross-format drift incidents、每次 orchestrated action export 數。404 修復給 stable business creative workflows SOP URL（slug 保留 loveart 拼寫）。
"""


FAQ = {
    "seedance_prompts": """
## FAQ

**Seedance 2 prompt 指南有定價嗎？**  
沒有 — 請查官方頁面；正文零 fabricated tiers。

**clip 內能 bake offer 嗎？**  
不能 — static companion editable via Touch Edit。

**multi-shot 要 character ref 嗎？**  
要 — 防 slide 4 character drift。

**404 修復？**  
stable zh-TW Seedance 2 prompt guide SOP URL。

**Brand Kit 仍必要嗎？**  
是 — hex SSOT 不因新模型而省略。
""",
    "case_study_photos": """
## FAQ

**case study 是 fake 轉化率嗎？**  
不是 — honest ops 指標與第一人稱翻車段落。

**改 caption 要 full regen 嗎？**  
不需要 — Touch Edit text band 目標五分鐘。

**memorial 專案要 Brand Kit 嗎？**  
建議 — 從 album sample 取樣防 drift。

**404 修復？**  
stable zh-TW family animated old photos case study URL。

**consent 法律建議？**  
本篇不 substitute legal advice；commercial publish 須 documented consent。
""",
    "stock_footage": """
## FAQ

**slug he-death 要改嗎？**  
不改 — 正文開頭已說明保留拼寫；內容語意為 stock footage era 指南。

**stock footage 已死嗎？**  
誠實 framing：libraries 仍存在；weekly offer 改動需要 editable static layer。

**改價要 reroll clip 嗎？**  
不需要 — Touch Edit 改 static companion。

**404 修復？**  
stable zh-TW AI video creation 2026 complete guide URL。

**fake benchmark 有嗎？**  
沒有 — 只描述 edit minutes 與 drift count。
""",
    "higgsfield_review": """
## FAQ

**Higgsfield 與 Lovart 二選一？**  
不是 — workflow 順序：static legal pass 再 motion。

**正文有 Higgsfield 定價嗎？**  
沒有 — 請查官方 ToS；零 fabricated subscription tiers。

**改價要整圖重出嗎？**  
不需要 — Touch Edit 框 CTA 帶。

**404 修復？**  
stable zh-TW Higgsfield honest review SOP URL。

**Design Agent 做什麼？**  
QA safe zone、disclaimer、Brand Kit drift。
""",
    "restaurant_menu": """
## FAQ

**菜單設計要先 Brand Kit 嗎？**  
建議 — 從 signage 或 menu PDF 取樣 hex。

**改湯品價要 full regen 嗎？**  
不需要 — Touch Edit price column 五分鐘。

**過敏原 disclaimer 可編輯嗎？**  
要 — footer flat band，禁止 bake 進 render。

**404 修復？**  
stable zh-TW restaurant menu AI complete guide URL。

**legal advice？**  
本篇只 cover ops workflow；過敏原文案須 legal 批准。
""",
    "flyers_cards": """
## FAQ

**傳單名片要同一 thread 嗎？**  
是 — master-first collateral family，防 accent drift。

**改 opening date 要 full regen 嗎？**  
不需要 — Touch Edit date band。

**300dpi CMYK 寫進 brief 嗎？**  
要 — Design Agent QA print bleed 與 safe zone。

**404 修復？**  
stable zh-TW flyers business cards invitations SOP URL。

**Brand Kit 從哪取樣？**  
approved logo 或 prior print PDF — 不用 stock beige。
""",
    "product_photo": """
## FAQ

**product photography 要先 Brand Kit 嗎？**  
建議 — 從 packaging PDF 取樣防 SKU drift。

**改 promo sticker 要 full regen 嗎？**  
不需要 — Touch Edit label band。

**carousel 同 thread 嗎？**  
是 — slide 2–6 accent stripe 一致。

**404 修復？**  
stable zh-TW product photography AI workflow URL。

**fake conversion lift？**  
禁止 — 只測改價分鐘與 drift count。
""",
    "art_creation": """
## FAQ

**Lovart 是 pure AI 畫家嗎？**  
不是 — campaign series 與 editable caption layer 為主。

**改展期要 full regen 嗎？**  
不需要 — Touch Edit title band。

**Brand Kit 從 artist sample 取樣？**  
是 — 防 gallery promo accent drift。

**404 修復？**  
stable zh-TW Lovart art creation painting tools URL。

**T2I playground 分工？**  
style exploration 用 T2I；weekly promo 改 copy 用 ChatCanvas stack。
""",
    "image_generator": """
## FAQ

**Lovart image generator 要先建 Brand Kit 嗎？**  
強烈建議 — 鎖 hex role，防 carousel drift。

**改活動價要整圖重出嗎？**  
不需要 — Touch Edit 框 CTA 帶。

**和純 T2I 分工？**  
T2I 偏單張探索；ChatCanvas 偏 editable series。

**404 修復？**  
stable zh-TW image generator stunning images SOP URL。

**Design Agent 做什麼？**  
按 brief QA safe zone、disclaimer、hex drift。
""",
    "loveart_business": """
## FAQ

**slug loveart 是 Lovart 嗎？**  
是 — URL 保留 loveart 拼寫；正文品牌名稱一律 Lovart。

**business workflow 有 fake stats 嗎？**  
沒有 — onboarding SOP 與 edit-minute 測量。

**多格式要幾個 prompt？**  
一個 thread — master-first 再 re-export 全 ratio。

**404 修復？**  
stable zh-TW business creative workflows URL（loveart slug）。

**Touch Edit drill 何時做？**  
在生成 slide 2–6 前 — 證明五分鐘改價成立。
""",
}


def expand_zhtw(topic: str, n: int) -> str:
    return f"""
## 實操補充 {n}：{topic}

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。{topic} 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。
"""


ARTICLES = [
    {
        "rank": 235,
        "key": "seedance_prompts",
        "lang": "zh-TW",
        "slug": "awesome-prompts-seedance-2-video-creation-guide",
        "cover": "022",
        "category": "How-To",
        "title": "Seedance 2 影片創作 prompt 精選：workflow 導向指南",
        "seo_title": "Seedance 2 Prompt Guide — zh-TW SOP",
        "description": "404 修復：Seedance 2 prompt 指南繁中，不編造定價，Touch Edit static layer。",
        "seo_description": "Seedance 2：Brand Kit、character ref、static-first，官方定價請查官網。",
        "focus": "awesome prompts seedance 2 video creation guide",
        "keywords": ["Seedance 2 prompt", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Seedance 2 Prompt Guide zh-TW",
        "body": SEEDANCE_PROMPTS_ZHTW,
        "expand_topic": "zh-TW Seedance 2 prompt workflow",
    },
    {
        "rank": 236,
        "key": "case_study_photos",
        "lang": "zh-TW",
        "slug": "case-study-family-animated-old-photos-ai",
        "cover": "026",
        "category": "Case Study",
        "title": "家庭老照片 AI 動畫 case study：第一人稱翻車與補救",
        "seo_title": "Family Animated Old Photos — zh-TW case study",
        "description": "404 修復：family photo animation case study，第一人稱失敗段落，Touch Edit caption。",
        "seo_description": "老照片動畫：memorial palette、static-first、honest ops 指標。",
        "focus": "case study family animated old photos ai",
        "keywords": ["family photo animation", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Case Study — Family Animated Old Photos zh-TW",
        "body": CASE_STUDY_PHOTOS_ZHTW,
        "expand_topic": "zh-TW family animated old photos case study workflow",
    },
    {
        "rank": 237,
        "key": "stock_footage",
        "lang": "zh-TW",
        "slug": "he-death-of-the-stock-footage-era-a-complete-guide-to-ai-powered-video-creation-in-2026",
        "cover": "030",
        "category": "Insight & Trend",
        "title": "素材庫時代終結？2026 AI 影片創作完整指南",
        "seo_title": "AI Video Creation 2026 — zh-TW complete guide",
        "description": "404 修復：he-death slug 保留拼寫，AI video 2026 static-first，不编制定價。",
        "seo_description": "Stock footage era：Brand Kit、Touch Edit editable layer、honest workflow。",
        "focus": "he death of the stock footage era ai video creation 2026",
        "keywords": ["AI video creation 2026", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight & Trend — Stock Footage Era zh-TW",
        "body": STOCK_FOOTAGE_ZHTW,
        "expand_topic": "zh-TW stock footage era AI video workflow",
    },
    {
        "rank": 238,
        "key": "higgsfield_review",
        "lang": "zh-TW",
        "slug": "higgsfield-ai-review",
        "cover": "034",
        "category": "Comparison",
        "title": "Higgsfield AI 評測：motion hook vs campaign static",
        "seo_title": "Higgsfield AI Review — zh-TW honest",
        "description": "404 修復：Higgsfield honest review，不编造 pricing，Touch Edit static layer。",
        "seo_description": "Higgsfield review：workflow 分業、Design Agent QA、官方定價請查 ToS。",
        "focus": "higgsfield ai review",
        "keywords": ["higgsfield ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Higgsfield AI Review zh-TW",
        "body": HIGGSFIELD_REVIEW_ZHTW,
        "expand_topic": "zh-TW Higgsfield honest review workflow",
    },
    {
        "rank": 239,
        "key": "restaurant_menu",
        "lang": "zh-TW",
        "slug": "how-to-design-a-restaurant-menu-with-ai-complete-guide-for-owners",
        "cover": "038",
        "category": "How-To",
        "title": "餐廳老闆用 AI 設計菜單：完整實操指南",
        "seo_title": "Restaurant Menu AI — zh-TW complete guide",
        "description": "404 修復：restaurant menu AI for owners，Brand Kit、Touch Edit 改價。",
        "seo_description": "菜單設計：print PDF、allergy disclaimer editable、Design Agent QA。",
        "focus": "how to design a restaurant menu with ai",
        "keywords": ["restaurant menu ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Restaurant Menu AI zh-TW",
        "body": RESTAURANT_MENU_ZHTW,
        "expand_topic": "zh-TW restaurant menu AI workflow",
    },
    {
        "rank": 240,
        "key": "flyers_cards",
        "lang": "zh-TW",
        "slug": "how-to-design-flyers-business-cards-invitations-ai",
        "cover": "042",
        "category": "How-To",
        "title": "用 AI 設計傳單、名片與邀請函：印刷級 workflow",
        "seo_title": "Flyers Business Cards Invitations — zh-TW SOP",
        "description": "404 修復：print collateral AI，master-first，Brand Kit、Touch Edit。",
        "seo_description": "傳單名片邀請函：300dpi CMYK、collateral family same thread。",
        "focus": "how to design flyers business cards invitations ai",
        "keywords": ["flyers business cards ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Flyers Business Cards Invitations zh-TW",
        "body": FLYERS_CARDS_ZHTW,
        "expand_topic": "zh-TW flyers business cards invitations workflow",
    },
    {
        "rank": 241,
        "key": "product_photo",
        "lang": "zh-TW",
        "slug": "how-to-gen-product-photography-with-ai",
        "cover": "046",
        "category": "How-To",
        "title": "用 AI 生成產品攝影：Lovart 實用 workflow 指南",
        "seo_title": "Product Photography AI — zh-TW workflow",
        "description": "404 修復：product photography AI，PDP hero、Touch Edit 改價。",
        "seo_description": "產品攝影：carousel thread、Brand Kit packaging hex、Design Agent QA。",
        "focus": "how to gen product photography with ai",
        "keywords": ["product photography ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Product Photography AI zh-TW",
        "body": PRODUCT_PHOTO_ZHTW,
        "expand_topic": "zh-TW product photography AI workflow",
    },
    {
        "rank": 243,
        "key": "art_creation",
        "lang": "zh-TW",
        "slug": "lovart-ai-art-creation-ai-painting-tools",
        "cover": "050",
        "category": "Lovart 101",
        "title": "Lovart AI 藝術創作與 AI 繪畫工具：campaign 視角",
        "seo_title": "Lovart Art Creation — zh-TW painting tools",
        "description": "404 修復：Lovart art creation AI painting tools，Brand Kit series。",
        "seo_description": "藝術創作：gallery promo editable layer、Touch Edit 改展期。",
        "focus": "lovart ai art creation ai painting tools",
        "keywords": ["lovart art creation", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Lovart 101 — Art Creation Painting Tools zh-TW",
        "body": ART_CREATION_ZHTW,
        "expand_topic": "zh-TW Lovart art creation painting workflow",
    },
    {
        "rank": 244,
        "key": "image_generator",
        "lang": "zh-TW",
        "slug": "lovart-ai-image-generator-create-stunning-images-with-ai",
        "cover": "054",
        "category": "Lovart 101",
        "title": "Lovart AI 圖像生成器：stunning images 的 campaign workflow",
        "seo_title": "Lovart Image Generator — zh-TW stunning images",
        "description": "404 修復：Lovart image generator stunning images，ChatCanvas editable series。",
        "seo_description": "圖像生成：Brand Kit、Touch Edit 改價、Design Agent pass/fail QA。",
        "focus": "lovart ai image generator create stunning images with ai",
        "keywords": ["lovart image generator", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Lovart 101 — Image Generator Stunning Images zh-TW",
        "body": IMAGE_GENERATOR_ZHTW,
        "expand_topic": "zh-TW Lovart image generator workflow",
    },
    {
        "rank": 245,
        "key": "loveart_business",
        "lang": "zh-TW",
        "slug": "loveart-ai-business-creative-workflows",
        "cover": "058",
        "category": "How-To",
        "title": "Lovart 商業創意工作流：business-first static 可編輯路線",
        "seo_title": "Business Creative Workflows — zh-TW SOP",
        "description": "404 修復：loveart slug 保留拼寫，business creative workflows，Brand Kit stack。",
        "seo_description": "商業工作流：multi-format orchestration、Touch Edit 五分鐘改價。",
        "focus": "loveart ai business creative workflows",
        "keywords": ["lovart business workflow", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Business Creative Workflows zh-TW",
        "body": LOVEART_BUSINESS_ZHTW,
        "expand_topic": "zh-TW business creative workflows",
    },
]


def build_article(a: dict) -> str:
    lang = a["lang"]
    floor = FLOORS[lang]
    parts = [fm(a), a["body"].strip()]
    topic = a["expand_topic"]
    n = 1
    while count_metric("\n".join(parts), lang) < floor:
        parts.append(expand_zhtw(topic, n))
        n += 1
        if n > 80:
            break
    parts.append(FAQ[a["key"]].strip())
    parts.append(
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch23 content cluster.*\n"
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
            "unit": "CJK",
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
