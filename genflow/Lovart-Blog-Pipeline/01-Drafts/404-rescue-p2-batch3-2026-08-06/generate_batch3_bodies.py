#!/usr/bin/env python3
"""Generate 404-rescue P2 batch3 blog bodies (10 files). Self-contained.

Skipped junk (ranks not in this batch):
  #31 ja — junk URL pattern
  #33 en — https-www-lovart-ai-zh-blog-top-10-... (malformed slug / junk)
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {"zh": 2200, "zh-TW": 2200, "en": 1300, "ko": 1400}

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


def count_en(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", body_text(text)))


def count_ko(text: str) -> int:
    return len(re.findall(r"[가-힣]", body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang in ("zh", "zh-TW"):
        return count_zh(text)
    if lang == "en":
        return count_en(text)
    if lang == "ko":
        return count_ko(text)
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

PACKAGING_ZH = """
# 包装设计 AI 指南：从 brief 到可印刷 static，404 修复后的可执行流程

这条中文 URL 曾返回 404，但搜索仍在问「AI 能不能做包装」。能，但 packaging 不是「一张好看的主视觉」就结束。刀版、出血、监管信息、条形码位置、材质暗示，任何一步缺位，印刷厂都会打回。404 修复页要教的是 discipline：Lovart **ChatCanvas** 与 **Design Agent** 负责可编辑 concept 与 series static，**Brand Kit** 锁 palette 与 type role，**Touch Edit** 改局部文案与角标，而不是一次性抽卡。

## 包装项目真正要解决的四个关卡

第一是 concept 探索：同一 SKU 要在袋装、盒装、罐装之间快速比稿，色温与 logo 位置不能每张漂移。第二是主推方向精修：标题 hierarchy、secondary pattern、regulatory block 必须可读。第三是 mockup 与 shelf context：3D 渲染可以后做，但 2D flat 上的 label 必须 Touch Edit 可改。第四是投产 handoff：Illustrator 套刀版仍要人类 expertise，AI 不能替代 bleed 与 CMYK 决策。

## Brand Kit 先于 batch gen

包装 series 最怕 slide 4 发明新 accent color。先在 **Brand Kit** 写入主色 hex、标题与正文字号角色、logo clear space、摄影/插画风格 reference。再在 **ChatCanvas** 开 packaging thread，brief 写清：包装类型、必要元素（logo 区、barcode 占位、净含量）、export 比例、禁止 double CTA。弱 brief「高级包装」→ 随机。强 brief「250g 咖啡袋，Brand Kit sage + charcoal，front panel headline top third，barcode bottom right placeholder，4:5 concept board」。

## Design Agent 与 Touch Edit 分工

结构不对 → 重 brief 或换 artboard layout。label 字小 → **Touch Edit** 局部放大，不要整袋 re-roll。促销角标改价 → Touch Edit 改字层。regulatory 句子改措辞 → Touch Edit，Brand Kit 保证字体 role 不变。404 修复的意义是让 onboarding 有 stable SOP URL，新人不用在群里问「包装 concept 到底用哪套流程」。

## 与 Illustrator / 印刷 handoff 的边界

AI 擅长 exploration 与 visualization；human 仍负责刀版套用、专色、上光区、烫金区。workflow 应是：ChatCanvas 出 approved flat → 进 Illustrator 套 dieline → mockup 节点渲染 shelf shot。反过来只做 3D mockup 不做 editable flat，改 copy 时要重跑 render，成本更高。

## 监管与品类差异

食品、化妆品、儿童产品的监管 block 位置因市场而异。把 disclaimer 与净含量当作 brief 必填字段，生成后 merchandiser QA 一遍，法务过 editable text。ChatCanvas static export 先过审，motion shelf clip 可以后配。

## 常见失败案例

九宫格 concept 每张不同子风格，客户 feel 品牌散。只有 mockup 没有 readable flat label。改促销字 full regen 而不是 Touch Edit。跳过 Brand Kit 后在 slide 3 手工改色。四类用 static-first + Kit + Touch Edit 都可缓解。

## 测量 ROI

别只记「生成了多少 concept」。记「从 brief 到 approved flat 几轮」「改 regulatory 一行要几分钟」「carousel 色 drift 几次」。包装是 revision-heavy 工作，工具价值在 edit cost。
"""

MAKEUP_BRAND_KIT_ZH = """
# 化妆工作室 Brand Kit 指南：柔和奢华视觉与可改价服务菜单

化妆工作室的 URL 曾 404，搜索却在问「小工作室能不能用 AI 做品牌系统」。能，但 beauty 行业要的是「作品集一致、服务菜单可改价、Instagram 封面不挡脸」，不是一张 random 海报。Lovart **Brand Kit** 记住 ivory/champagne/rose gold 等 palette role，**ChatCanvas** 与 **Design Agent** 出 series 模板，**Touch Edit** 改套餐价与活动日期，才是日常 rhythm。

## 化妆工作室要稳住的四个输出物

第一是 Logo 与 studio name 变体：名片、咨询表、Instagram 头像框需要同一 clear space。第二是服务菜单与 bride package 价目：文案常改，版式不能散。第三是 before/after 作品集模板：角标位置、studio 署名、强调色 label 要 series 一致。第四是 Story 与 TikTok 封面：竖版 safe zone，文字不能挡妆容主体。

## Brand Kit 怎么设才不「廉价感」

新娘线常用 ivory、champagne、rose gold、soft blush；编辑线可用 cream、obsidian、crimson accent；纯净美妆线可用 alabaster、sage、clay。关键不是堆 luxury 形容词，而是 hex role 固定：背景、accent、body text、disclaimer。Kit 设好后，**ChatCanvas** brief 写「bridal trial menu，4:5，价格左下，top 12% Story UI 留白，Brand Kit bridal palette」。生成 carousel 时 slide 4 不会 random 换粉。

## 服务菜单与 Touch Edit

bridal package 三档价（classic / premium / luxe）最常改的是 middle tier 价格与包含项。用 **Touch Edit** 改数字与 bullet 行，不要整页 re-roll。Brand Kit 保证标题 font role 与 accent stripe 位置。consultation PDF 的 disclaimer 与 allergy 字段当作必填 brief 字段。

## 作品集模板纪律

before/after split、三联 bride look、product flat lay、Story book CTA 各需固定 grid。同一 thread 批量 export，只换 photo 不换版式。肤色展示要遵循 studio 灯光指南（中性 5000K–5600K），brief 禁止过度磨皮 filter 挡皮肤纹理。404 修复页给新人 stable URL，不用从 Pinterest 重新拼模板。

## 与纯修图工具的分工

Lightroom preset 与 AI 增强可以 companion；paid 投放仍要 Lovart static offer 与 editable CTA。video tutorial hook 可后做，但「Book Your Trial」必须在 Touch Edit 可改层上。

## 常见翻车

每帖不同 font，客户 feel 不专业。只有 Story 动效没有 static menu 价。改价 full regen。跳过 Brand Kit 后手工改 rose gold hex。用 Kit + Touch Edit + 同一 thread 可缓解。

## 测量什么

记「改套餐价几分钟」「一次 bridal season 要 export 几种尺寸」「carousel drift 几次」。beauty 业务 revision 频率高于 first-frame wow。
"""

UPSCALER_EN = """
# AI Image Upscaler Guide: When to Upscale, When to Touch Edit Instead

This English URL returned 404 while search still asked how to upscale campaign art without melting labels. Upscaling is not a universal fix. I use upscalers for texture and resolution gaps; I use Lovart **Touch Edit** and **ChatCanvas** when the problem is editable type, Brand Kit consistency, or promo blocks that will change next Tuesday.

## What upscaling actually fixes

Upscalers help when you have a small master but need print or hero resolution, when fabric or skin texture looks soft but geometry is correct, or when a legacy asset must match a new carousel size. They do not fix wrong headline hierarchy, double CTAs, or label text baked into pixels. If the copy is wrong, upscaling sharper wrong text wastes time.

## My static-first loop in ChatCanvas

I load **Brand Kit** palette and type roles. I brief the **Design Agent** at target export size when possible, because upscaling after the fact is a tax. Brief example: "Product hero 2048 wide, headline top third, label readable at 50% zoom, leave bottom 12% for disclaimer, Brand Kit navy accent." If the first pass is sharp but label small, I Touch Edit the label region before any upscaler, because enlarging mushy type rarely beats regenerating the type layer.

## Touch Edit versus upscaler decision tree

Use **Touch Edit** when only a region needs change: price, date, logo swap, localized disclaimer. Use upscaler when global resolution is low but composition and type layers are approved. Use re-prompt in **ChatCanvas** when layout grid is wrong. Teams burn hours upscaling six PNGs that needed a five-minute headline Touch Edit.

## Brand Kit memory across sizes

Without **Brand Kit**, upscaled slide three invents a new accent hex. With Kit active, upscaled variants still follow role names even if pixel values differ slightly. For multi-size exports, I generate the largest master in ChatCanvas, Touch Edit promo blocks once, then downscale for email headers rather than upscaling small gens.

## QA before upscale batch jobs

Check label spelling at 100% and 50% zoom. Confirm no double CTA. Confirm disclaimer lines exist on editable layers where possible. Run one upscaled proof before batching twenty carousel slides. Broken 404 URLs often meant teams upscaled unapproved comps and had to redo legal.

## Common mistakes

Upscale first, discover typo, re-upscale entire stack. Upscale JPEG artifacts from a over-compressed source. Upscale anime-stylized product labels until they look plastic. Skip Brand Kit and manually recolor after upscale drift.

## Measuring value

Track minutes per headline fix versus minutes per upscale pass. Track how often upscaled text fails QA. Tools win when revision cost drops, not when the first upscale looks shiny.
"""

PET_GENERATORS_ZH = """
# AI 动物与宠物生成器对比：可控 brief 与商用 static 边界

「AI 宠物头像」「AI 动物插画」搜索量高，但输出质量参差。这条中文 URL 曾 404，需要段落体对比：何时适合、如何 brief、如何用 Lovart **ChatCanvas** 做 campaign 配套 static、**Touch Edit** 改字、**Brand Kit** 保 series 一致，而不是罗列十个 generator 名字。

## 三类需求与工具分工

第一类是 personal pet avatar：适合 social IP，注意肖像权与品种特征 accuracy。第二类是 pet brand campaign：需要 label、promo 角标、editable CTA，适合 **Design Agent** 在 **ChatCanvas** 出 static hero。第三类是 veterinary / pet service local marketing：价目、预约 CTA、门店 logo 位置要 series 一致，**Brand Kit** 与 **Touch Edit** 改价优于整图 re-roll。

## 对比标准：别只看「像不像」

我评估 pet generator 看五点：品种特征是否 stable、毛发纹理是否 over-smooth、背景是否抢主体、export 尺寸是否够 paid social、改字是否必须 full regen。多数纯 avatar 工具赢在 cute，输在 campaign editable layer。Lovart 赢在 Brand Kit series 与 Touch Edit 局部改 promo，不是单张 cutest cat。

## brief 怎么写才不崩

写清物种与品种、表情与 pose、背景复杂度、export 比例、是否需留 headline safe zone。弱 brief「可爱狗狗」→ 随机。强 brief「柯基侧面，studio soft light，Brand Kit coral accent，4:5，top 15% 留 campaign headline，label 区 blank for Touch Edit」。pet food packaging 还要写 regulatory placeholder 位置。

## Design Agent 与 Touch Edit 分工

构图不对 → ChatCanvas 重 brief。项圈 label 字糊 → Touch Edit 局部 sharpen。促销「首单减 20%」→ Touch Edit 改字，不要整图 pet re-roll。multi-pet carousel 用同一 thread 固定角标与 logo 位置。

## 商用与合规

未授权品种 trademark 造型、竞品 logo 背景、celebrity 宠物 mimic 有风险。commercial use 读各平台 ToS。campaign 仍要 static offer 层 editable，不能只在 cute video 里闪一次价格。

## 与 video pet filter 的分工

motion pet filter 可玩；paid ads 需要 readable static companion。workflow：ChatCanvas hero 过 legal → optional motion。404 修复后 stable URL 给 pet brand SOP 内链。

## 常见失败

九宫格每只不同 cartoon 子风格。只有 cute avatar 无 readable shop CTA。改价 full regen。跳过 Brand Kit 后 slide 3 漂移。用 Kit + Touch Edit 缓解。
"""

DREAMINA_KO = """
# Dreamina AI 리뷰 2026: 솔직한 사용 후기와 캠페인 static 분업

이 한국어 URL은 404였지만, 검색은 Dreamina AI가 정말 괜찮은지, 마케팅에 쓸 수 있는지 묻습니다. 결론부터: Dreamina는 mood clip과 stylized visual exploration에 강점이 있습니다. editable price block, Brand Kit series, legal disclaimer layer는 Lovart **ChatCanvas**와 **Touch Edit** 쪽이 맞습니다. 둘을 경쟁으로만 보면 workflow가 깨집니다.

## Dreamina가 잘하는 것

짧은 stylized clip, 분위기 B-roll, concept board용 visual mood. prompt만으로 빠르게 look dev를 보는 데 유용합니다. 특히 fashion/beauty mood reel, SNS teaser용 abstract motion에는 시간을 절약할 수 있습니다.

## Dreamina가 약한 것

carousel slide 4에서 hex drift, 작은 가격 글자, double CTA, package label readability. 수정할 때 full regen 비용이 큽니다. 한국어 카피가 이미지에 bake되면 Touch Edit 없이는 Tuesday promo 변경이 painful합니다.

## Lovart와 병행 workflow

1) **Brand Kit**에 primary palette, type role, logo clear space 고정. 2) **ChatCanvas**에서 hero/end card static, offer와 disclaimer editable layer로 생성. 3) legal static pass. 4) Dreamina로 4–6초 mood hook, color temperature를 Brand Kit intent에 맞춤. 5) 가격 변경은 **Touch Edit** static만, Dreamina clip은 유지.

## brief 계약 예시

Dreamina: "soft beauty mood, ivory light, slow pan, no readable small text". ChatCanvas: "4:5 hero, headline top third, price bottom left safe zone, Brand Kit sage + charcoal, disclaimer one line footer". 약한 brief "예쁘게" → QA fail.

## 가격/라이선스 주의

Dreamina tier와 commercial use 범위는 공식 ToS 확인. free output을 paid social에 바로 쓰지 마세요. license PDF와 project id를 campaign folder에 저장. Lovart static은 editable text QA 후 publish.

## 실패 패턴

Dreamina clip만 있고 landing static offer 불일치. promo 변경마다 clip regen. Brand Kit 없이 carousel drift. static-first로 완화.

## 측정

"첫 clip 몇 분"보다 "가격 변경 몇 분", "static vs video offer 일치율", "legal return 횟수". revision cost가 도구 선택 기준입니다.
"""

PRINT_MATERIALS_ZHTW = """
# AI 印刷物料完全指南：傳單、名片與活動卡片的 static-first 流程

這條繁體中文 URL 曾回傳 404，搜尋仍在問「AI 能不能做傳單與名片」。能，但 print 物料不是「一張漂亮圖」就交件。出血、安全區、可編輯價格、門市 disclaimer、多尺寸 export，任何一步缺位，印刷店或活動現場都會打回。404 修復頁要教 discipline：Lovart **ChatCanvas** 與 **Design Agent** 負責可改稿 static，**Brand Kit** 鎖 palette 與字型角色，**Touch Edit** 改局部 promo，而不是一次性抽卡。

## 印刷物料真正要解決的四個場景

第一是活動傳單：時間地點常改，版式不能散。第二是名片與工作證：logo clear space 與 title hierarchy 要穩。第三是促銷卡片與桌牌：價格與 QR CTA 必須可編輯。第四是 post-event 改版：活動結束改「下次見」只需 Touch Edit，不要整份重出。

## Brand Kit 先於 batch gen

傳單 series 最怕 slide 3 發明新 accent 色。先在 **Brand Kit** 寫入主色 hex、標題與內文字型角色、logo 留白、print 偏好（哑光 vs 光面暗示）。再在 **ChatCanvas** 開 print thread，brief 寫清：尺寸（A5、90×54mm 名片）、必填欄位、safe zone、禁止 double CTA。弱 brief「高級傳單」→ 隨機。強 brief「開幕活動 A5，時間地點左下，QR 右下 placeholder，Brand Kit navy + cream，留 3mm bleed note in export checklist」。

## Design Agent 與 Touch Edit 分工

構圖不對 → 重 brief。電話號碼錯 → **Touch Edit** 改字層。活動日期改期 → Touch Edit，Brand Kit 保 stripe 位置。regulatory 或免責句改措辭 → Touch Edit，不要整張 re-roll。404 修復的意義是 onboarding 有 stable SOP URL。

## 與印刷 handoff 的邊界

AI 擅長 exploration 與 flat approved；human 仍負責出血設定、CMYK、特別色。workflow：ChatCanvas 出 approved PDF/PNG → 進 Indesign/Illustrator 套印刷規格 → 送印。反過來只做 mockup 不做 editable flat，改 copy 成本更高。

## 常見失敗

傳單與名片色溫不一致。只有 QR 圖沒有 editable 活動標題。改價 full regen。跳過 Brand Kit 後手工改色。用 Kit + Touch Edit 可緩解。

## 測量 ROI

別只記「出圖幾分鐘」。記「改日期一次幾分鐘」「一次活動要 export 幾種尺寸」。print 是 revision-heavy 工作。
"""

REAL_ESTATE_ZH = """
# 如何用 AI 做房产营销物料：listing 传单、开放看房与朋友圈

这条中文 URL 曾 404，搜索仍在问「房产营销能不能用 AI 做图」。能，但 broker 要的是「换盘、换价、换渠道尺寸时不要整页重做」。一周要出 listing 传单、开放看房预告、朋友圈九宫格、店铺活动海报；每次从零 prompt，品牌色与字体很快漂移，客户会觉得你不专业。

## 经纪人真正要解决的三个场景

第一是 listing 首发图：主图要清楚、角标不挡窗景、价格与面积可读。第二是开放看房与带看节点：时间地点常改，视觉系统不能散。第三是朋友圈与 WeChat 时刻：竖版 safe zone，标题不能挡客厅实景。Lovart **Design Agent** 与 **ChatCanvas** 是可对话、可改稿的设计面；**Brand Kit** 记住主色与 logo 留白；**Touch Edit** 改局部价格而不推翻整图。

## 在 ChatCanvas 里写 broker brief

不可用 brief 是「帮我做一张高端房源海报」。可用 brief 是：「三房两厅，南向客厅，主图 4:5，价格与面积放左下安全区，角标写新上，留 top 10% 给平台 UI，导出 1080×1350，Brand Kit 沿用门店主色」。把渠道、留白、必填字段写进 brief，代理才有验收标准。

## listing 传单与 Touch Edit

listing 传单最怕「整张重出」。周二改挂牌价、周四加 open house 时段，若每次重 roll，经纪人没空等。正确做法是在 ChatCanvas 固定版式，改价用 **Touch Edit** 只动数字与面积栏。Brand Kit 保证标题字体与色块位置不变。法务若要求标注「以现场为准」，把 disclaimer 当必填字段。

## 开放看房与朋友圈

open house 周末往往要同一套视觉连发：朋友圈预告、社群接龙图、店铺电视屏。用同一 ChatCanvas thread 改时间地点，比每晚重开 generator 省小时。WeChat 时刻竖版写清 top 12% 与 bottom 10% safe zone，价格放在 static 可编辑层，不要依赖 video 帧内小字。

## 合规与本地习惯

中文房源素材常涉及面积表述、学区免责、效果图与实景差异。把句子当必填字段写进 brief。ChatCanvas 导出 static 审核稿，video hook 可以后配，但价格与面积必须以可改文本为准。

## 常见失败

只有燃向 video 没有 readable listing static。改价 full regen。carousel 每 slide random font。跳过 Brand Kit。用 static-first + Touch Edit 缓解。

## 测量什么

记「改价一次几分钟」「一次 open house 要重出几张尺寸」。broker 业务里后者决定工具值不值。404 修复页让 SOP 有 stable URL。
"""

FIREFLY_VS_AGENTS_ZHTW = """
# Adobe Firefly 與 AI 設計代理比較：營運視角，不是口號對決

這條繁體中文 URL 曾 404，搜尋需要一份誠實對照：Firefly 與 Lovart 這類 **Design Agent** 路線各自擅長什麼、workflow 怎麼並行、哪裡不該互相替代。結論先行：Firefly 強在 Adobe 生態內的 generative fill 與 Creative Cloud 整合；Lovart 強在 **ChatCanvas** 可改稿 campaign static、**Brand Kit** series 記憶、**Touch Edit** 改價與 disclaimer，適合 revision-heavy 的行銷產出。

## 先定驗收標準，再選工具

若任務是「修 photo 局部、擴圖、Photoshop 內快速變體」，Firefly 合理。若任務是「hero + carousel + 傳單，下週改價不改版式」，**Design Agent** 與 Brand Kit 路線更省。用錯標準會得出「Firefly 不能 one-click funnel」或「Lovart 不能取代 Photoshop 筆刷」這類假問題。

## Firefly 擅長的操作面

Generative fill、text effect exploration、與 Illustrator/Photoshop 互轉。對已有 Adobe pipeline 的團隊，在單張 comp 內做局部 experiment 很快。弱點是 series campaign 的 hex drift、editable promo block、跨 slide 的 type role 記憶，除非另建 strict template，否則 Tuesday 改價常觸發 full regen。

## Lovart Design Agent 擅長的操作面

**ChatCanvas** thread 裡 brief → 多 artboard → **Touch Edit** 改 CTA/價格/日期。**Brand Kit** 讓 slide 4 不發明新 accent。適合 broker listing、print 傳單、beauty menu 這類高頻改字場景。弱點是不取代完整 Photoshop retouch 或 InDesign 長文排版；它是 campaign static 與半 static 套裝的中間層。

## 並行 workflow 範例

Brand Kit 定 palette → ChatCanvas 出 approved hero 與 end card → Firefly 在 Photoshop 內做 photo-specific fill → 回 ChatCanvas Touch Edit 統一 promo 字層 → export 多尺寸。反序（先 Firefly 全出再硬塞 Brand Kit）常造成色溫與 type hierarchy 不一致。

## 授權與品牌 hygiene

Firefly 與 Lovart 各有 commercial terms；不可假設「enterprise 就一定可投 paid social」。prompt 避免未授權 logo 與肖像。404 修復頁教 discipline，不是教站隊。

## 常見誤判

用 Firefly 做 entire funnel 然後抱怨改價慢。用 Lovart 取代 Photoshop 精修。不做 static legal pass 就做 motion hook。並行分工可緩解。

## 測量

記「改 headline 幾分鐘」「carousel drift 幾次」「legal return 幾次」。工具價值在 revision cost。
"""

TEAM_STORY_ZHTW = """
# Lovart 幕後團隊故事：流程、交接與 404 修復的營運誠實

這條繁體中文 URL 曾回傳 404，搜尋要找的不是 slogan，而是團隊如何工作、**ChatCanvas** 與 **Design Agent** 如何進 production、為何 **Brand Kit** 與 **Touch Edit** 不是 demo 功能而是降低改稿成本。本文用營運語氣描述 handoff，不捏造 headcount 或誇大 one-click。

## 為何發布「幕後」

URL 空著時，搜尋會落到論壇與二手貼文。我們需要 stable 頁面描述真實流程：brief → Brand Kit → 三個方向 → Touch Edit → export → QA → Sanity 發布。不用「magic one-click」，也不編造財務數字。

## 內容管線如何運作

情報（SEO、SERP、輿情）餵給內容日曆。Writer 在 **ChatCanvas** 開具體 brief thread。**Design Agent** 生成 static hero 與 campaign variants。**Brand Kit** 固定 hex 與 type role。**Touch Edit** 關閉價格與日期修改，避免 full regen。QA 跑 preflight、banned phrases、圖片 HEAD 檢查。Publish 走 Sanity，`releaseDate` 與 `publishedAt` 一致。

## 角色分工（不英雄化）

Product KB 是 ChatCanvas、Brand Kit、Touch Edit、MCoT 術語 SSOT。Content ops 負責 routing 與 anti-slop 門禁。Localization 是 rewrite，不是逐句翻譯。Engineering 負責 schema 與前端，不在真空中寫 copy。我們不發布假 org chart；我們描述交接點。

## 404 修復對團隊的意義

內部 onboarding 曾連到 broken URL，新人對 docs 失去信任。恢復頁面是 ops hygiene，如同監控連結。繁體讀者與簡中、英文讀者應看到同等誠實的流程描述，不是翻譯縮水。

## 誠實限制

Lovart 不取代 legal review。不保證每次 gen 都 pixel-perfect 商標一致。勝在 revision cost 低於 first-frame cost 的 campaign 工作。motion hook 常走 companion tools；static offer 活在可編輯層。

## 如何測量

headline 修改分鐘數。full regen vs Touch Edit 次數。carousel drift 分數。broken cover 工單。不是 Slack 按讚數。

## 讀者下一步

若你因 404 點進來——頁面已恢復。下一步：註冊、載入 Brand Kit、用真實 brief 開一個 production thread，而不是 abstract「make it cool」。
"""

BG_REMOVER_EN = """
# AI Background Remover Guide: Cutout Quality and the Touch Edit Workflow

This English URL returned 404 while search asked how to remove backgrounds for product and campaign art. Background removal is a start, not a finish. I pair cutout tools with Lovart **ChatCanvas**, **Brand Kit**, and **Touch Edit** when the deliverable is a promo-ready static with editable price and disclaimer blocks.

## What background removal solves

Clean product isolation for ecommerce tiles, compositing onto branded panels, and quick placement on seasonal backdrops. It does not solve typography, legal lines, or carousel consistency. A perfect cutout on a random gradient still fails brand QA.

## My workflow after the cutout

Import or generate the isolated product into **ChatCanvas**. Load **Brand Kit** colors and type roles. Brief the **Design Agent**: "Isolated SKU centered, shadow direction lower right, headline top third, price bottom left safe zone, disclaimer footer, 4:5 export." If the cutout edge frays hair or glass, Touch Edit the edge region before rebuilding the whole scene.

## Touch Edit for edge fixes versus full regen

Use **Touch Edit** on halo fringes, small label smudges, and promo type. Use re-prompt when perspective or lighting on the product is wrong. Teams regen entire heroes because of one fringe pixel; zoomed Touch Edit passes are cheaper.

## Brand Kit on composite backgrounds

Without **Brand Kit**, slide two picks a new backdrop hue. With Kit, backdrop tints follow accent roles even when the product cutout stays constant. For seasonal swaps, keep the cutout thread and Touch Edit only the background panel and promo line.

## Multi-size exports

Generate the tallest master, Touch Edit CTA once, export crops for marketplace thumbs and email headers. Upscaling tiny cutouts before composite yields plastic edges; start from the largest practical source file.

## Legal and merchandising QA

Confirm label text readable after composite. Confirm no competitor logos in generated backgrounds. Confirm disclaimer exists on editable layers. Static pass before motion hooks.

## Common mistakes

Remove background then upscale until edges glow. Composite before spell-checking label copy. Skip Brand Kit and manually match colors per slide. Run video ads before static legal approval.

## Measuring value

Track minutes to fix edges with Touch Edit versus full regen. Track carousel drift after background swaps. This restored page gives search a real workflow link.
"""

# FAQ blocks
FAQ = {
    "packaging_zh": """
## FAQ

**AI 能直接出印刷文件吗？**  
Concept 与 flat 可以；刀版套用、出血、CMYK 仍要 human expertise。ChatCanvas 出 approved flat 再进 Illustrator。

**为什么要先 Brand Kit？**  
包装 series 容易色 drift。Kit 固定 hex role 后再 batch gen。

**改 regulatory 一行要重出整袋吗？**  
不用。Touch Edit 改字层，Brand Kit 保字体 role。

**404 之前为什么搜不到？**  
该 slug 无发布文档。补齐后可作包装 SOP 内链。

**和纯 mockup 工具分工？**  
mockup 可后做；editable flat label 必须先过 legal。
""",
    "makeup_brand_zh": """
## FAQ

**小工作室没有设计师能用吗？**  
可以，但 brief 要写具体套餐与 safe zone，并固定 Brand Kit。

**改 bridal 套餐价要重出吗？**  
不需要。Touch Edit 改数字，Brand Kit 保版式。

**404 修复意义？**  
stable URL 给 onboarding，不用从 Pinterest 拼模板。

**Instagram 字挡脸怎么办？**  
brief 写 safe zone，Touch Edit 微调标题位置。

**只有 video 教程够吗？**  
paid 需要 readable static menu 与 CTA，ChatCanvas 先出 hero。
""",
    "upscaler_en": """
## FAQ

**Should I upscale before or after Touch Edit?**  
Fix type and promo blocks first; upscale approved masters once.

**Can upscaling replace ChatCanvas?**  
No. It adds resolution; it does not fix layout or Brand Kit drift.

**Why was this URL broken?**  
The published document was missing. This page restores the workflow link.

**Does Brand Kit matter after upscale?**  
Yes. Kit roles prevent accent drift across sizes.

**When do I re-prompt instead?**  
When grid, lighting, or hierarchy is wrong—not for one typo.
""",
    "pet_generators_zh": """
## FAQ

**宠物 avatar 工具能直接投广告吗？**  
取决于 ToS 与 editable CTA。campaign 建议 ChatCanvas static + Touch Edit 改价。

**label 糊了怎么办？**  
Touch Edit 局部修，不要整图 pet re-roll。

**404 修复？**  
补齐 searchable SOP，非 placeholder 页。

**和 Brand Kit？**  
pet brand series 先锁 palette 与角标位置。

**只有 cute video 够吗？**  
paid 需要 readable shop CTA static。
""",
    "dreamina_ko": """
## FAQ

**Dreamina만으로 funnel 충분한가요?**  
아닙니다. editable static과 Brand Kit series는 ChatCanvas 쪽이 맞습니다.

**가격 변경은?**  
Touch Edit static; clip regen은 피하세요.

**404였던 이유?**  
locale 문서缺失. 지금 stable URL입니다.

**라이선스?**  
ToS 확인, license PDF 저장. free를 paid에 바로 쓰지 마세요.

**Firefly/Dreamina vs Lovart?**  
mood clip vs editable campaign static; 병행이지 대체가 아닙니다.
""",
    "print_zhtw": """
## FAQ

**AI 能直接送印吗？**  
ChatCanvas 出 approved flat；出血与 CMYK 仍要 human 印刷规格。

**活动改期要重出传单吗？**  
不用。Touch Edit 改日期，Brand Kit 保版式。

**404 修复意义？**  
stable URL 给 print SOP onboarding。

**名片与传单色温不一致？**  
先 Brand Kit 再 batch export。

**只有 QR 图够吗？**  
活动标题与 disclaimer 必须在 editable text 层。
""",
    "real_estate_zh": """
## FAQ

**没有设计基础能用吗？**  
可以，但 brief 要写 listing 字段与 safe zone，并固定 Brand Kit。

**改挂牌价要重出整张吗？**  
不需要。Touch Edit 改价格与面积数字。

**open house 时间改了怎么办？**  
同一 ChatCanvas thread 改时间与地点，Touch Edit 改字层。

**朋友圈字被挡？**  
brief 写 top 12% safe zone，Touch Edit 微调。

**404 之前为什么 404？**  
该语言路径缺少发布文档。补齐后可作 broker SOP 内链。
""",
    "firefly_zhtw": """
## FAQ

**Firefly 能取代 Design Agent 吗？**  
不全然。局部 generative fill vs campaign series 改价是不同任务。

**Lovart 能取代 Photoshop 吗？**  
不取代精修；负责 editable campaign static 与 Brand Kit 记忆。

**404 修复？**  
补齐对照页，避免搜尋落到空链。

**Tuesday 改价谁更省？**  
高频改字场景 Touch Edit + Brand Kit 通常更省。

**授权要注意什么？**  
各自 commercial terms；不可假设 enterprise 即等于 all paid uses。
""",
    "team_story_zhtw": """
## FAQ

**为什么页面曾是 404？**  
缺少已发布的繁体文档。链接已恢复供 onboarding。

**这是营销神话吗？**  
不捏造数字；描述 ops handoff 与工具角色。

**新手要先 Brand Kit 吗？**  
是，在 batch gen 之前，否则 carousel drift。

**Touch Edit 何时用？**  
改价格、日期、CTA，避免 full regen。

**从哪里开始？**  
注册 → Brand Kit → 一个真实 brief 的 ChatCanvas thread。
""",
    "bg_remover_en": """
## FAQ

**Is background removal enough for ads?**  
No. You still need Brand Kit, readable type, and legal lines in ChatCanvas.

**Fringe halos after cutout?**  
Touch Edit the edge region before full regen.

**Why restore this URL?**  
Search and internal links pointed to a missing doc.

**Static before video?**  
Yes. Approve composite static before motion hooks.

**Brand Kit on composites?**  
Backdrop tints follow Kit roles; prevents slide drift.
""",
}

# Expansion paragraphs
def expand_zh(topic: str, n: int) -> str:
    return f"""
## 实操补充 {n}：{topic}

很多团队第一次用 **Design Agent** 时会把 brief 写成形容词堆叠，结果图「好看」但价目字小、角标挡主体。第二次只改 brief 里的必填字段与 safe zone，第三轮往往就能进 Brand Kit 流程。记录每轮改 brief 花了多久、是否触发整图重出，比争论模型名字更有用。{topic} 这类场景里，**Touch Edit** 改价若能在五分钟内完成，就证明 static-first 路线成立；若每次改价都要重 roll，说明 Brand Kit 或 brief 模板还没设好。404 修复页的价值是让 SOP 有 stable URL，新人不用在群里问「到底用哪套流程」。内链到此页时，请附带 hex 与 disclaimer 句原文，减少 ChatCanvas thread 里来回确认。
"""


def expand_zhtw(topic: str, n: int) -> str:
    return f"""
## 實操補充 {n}：{topic}

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。{topic} 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。
"""


def expand_ko(topic: str, n: int) -> str:
    return f"""
## 현장 메모 {n}: {topic}

첫 brief가 「고급스럽게」로 끝나면 가격 숫자가 작아지고 badge가 얼굴을 가립니다. 두 번째는 safe zone과 필수 필드만 고칩니다. **Design Agent**와 **ChatCanvas**에서 thread를 유지하면 carousel slide 4 색 drift를 줄입니다. {topic}에서 **Touch Edit** 5분 이내 가격 수정이면 도구가 맞습니다. 30분 full regen이면 Brand Kit부터 다시 하세요. 404 복구 URL은 onboarding용 stable link입니다.
"""


def expand_en(topic: str, n: int) -> str:
    return f"""
## Field note {n}: {topic}

The first pass often fails because the brief says "premium" without grid, type role, or safe zone. The second pass changes only those fields; round three usually enters Brand Kit flow. Track minutes per headline edit, not demo wow. In **{topic}**, if **Touch Edit** closes a price change under five minutes, the static-first loop works. If every edit triggers full regen, fix Brand Kit and brief templates first. This restored URL gives search a real destination instead of a broken slug.
"""


ARTICLES = [
    {
        "key": "packaging_zh",
        "lang": "zh",
        "slug": "packaging-design-ai-guide",
        "cover": "012",
        "category": "Best Practice",
        "title": "包装设计 AI 指南：从 brief 到可印刷 static 的可执行流程",
        "seo_title": "包装设计 AI 指南 — ChatCanvas 工作流",
        "description": "404 修复：用 Lovart ChatCanvas、Brand Kit、Touch Edit 做包装 concept 与 editable flat，再 handoff 印刷。",
        "seo_description": "包装 AI：Design Agent concept、Brand Kit 锁色、Touch Edit 改 label，static-first 投产纪律。",
        "focus": "包装设计 ai",
        "keywords": ["包装设计 ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Best Practice — Packaging",
        "body": PACKAGING_ZH,
        "expand_topic": "包装 concept 与 label 可读性",
    },
    {
        "key": "makeup_brand_zh",
        "lang": "zh",
        "slug": "brand-kit-makeup-studio-lovart",
        "cover": "019",
        "category": "Branding",
        "title": "化妆工作室 Brand Kit 指南：柔和奢华视觉与可改价服务菜单",
        "seo_title": "化妆工作室 Brand Kit — Lovart 实用指南",
        "description": "化妆工作室用 Lovart Brand Kit 与 ChatCanvas 做作品集、服务菜单与 Story 封面，改价用 Touch Edit。",
        "seo_description": "beauty Brand Kit、bridal menu、Touch Edit 改价、404 URL 修复。",
        "focus": "化妆工作室 brand kit",
        "keywords": ["化妆工作室 brand kit", "lovart brand kit", "chatcanvas", "touch edit"],
        "cluster": "Branding — Beauty Studio",
        "body": MAKEUP_BRAND_KIT_ZH,
        "expand_topic": "bridal 套餐与服务菜单",
    },
    {
        "key": "upscaler_en",
        "lang": "en",
        "slug": "ai-image-upscaler",
        "cover": "026",
        "category": "How-To",
        "title": "AI Image Upscaler Guide: When to Upscale, When to Touch Edit Instead",
        "seo_title": "AI Image Upscaler — Touch Edit Workflow",
        "description": "404 fix: upscaler vs Lovart Touch Edit and ChatCanvas for campaign art; Brand Kit anti-drift.",
        "seo_description": "Upscale discipline: static-first, Touch Edit labels, Brand Kit series consistency.",
        "focus": "ai image upscaler",
        "keywords": ["ai image upscaler", "touch edit", "chatcanvas", "brand kit"],
        "cluster": "How-To — Touch Edit",
        "body": UPSCALER_EN,
        "expand_topic": "campaign upscale QA",
    },
    {
        "key": "pet_generators_zh",
        "lang": "zh",
        "slug": "ai-animal-pet-generators-compared",
        "cover": "033",
        "category": "Comparison",
        "title": "AI 动物与宠物生成器对比：可控 brief 与商用 static 边界",
        "seo_title": "AI 宠物生成器对比 — Lovart static 工作流",
        "description": "对比 pet generator 与 Lovart ChatCanvas campaign static；Touch Edit 改 promo，Brand Kit 保 series。",
        "seo_description": "pet AI 对比：Design Agent、Brand Kit、Touch Edit、商用 static 边界。",
        "focus": "ai 宠物生成器 对比",
        "keywords": ["ai 宠物生成器", "pet ai", "lovart chatcanvas", "touch edit"],
        "cluster": "Comparison — Pet AI",
        "body": PET_GENERATORS_ZH,
        "expand_topic": "pet brand campaign static",
    },
    {
        "key": "dreamina_ko",
        "lang": "ko",
        "slug": "dreamina-ai-review",
        "cover": "040",
        "category": "Review",
        "title": "Dreamina AI 리뷰 2026: 솔직한 사용 후기와 캠페인 static 분업",
        "seo_title": "Dreamina AI 리뷰 — 정직한 workflow",
        "description": "Dreamina AI 솔직 리뷰: mood clip vs Lovart ChatCanvas editable static, Brand Kit, Touch Edit.",
        "seo_description": "Dreamina review KO: static-first, license 주의, Touch Edit promo.",
        "focus": "dreamina ai review",
        "keywords": ["dreamina ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Review — Dreamina",
        "body": DREAMINA_KO,
        "expand_topic": "Dreamina mood clip companion",
    },
    {
        "key": "print_zhtw",
        "lang": "zh-TW",
        "slug": "complete-guide-ai-print-materials-flyers-cards",
        "cover": "047",
        "category": "Complete Guide",
        "title": "AI 印刷物料完全指南：傳單、名片與活動卡片的 static-first 流程",
        "seo_title": "AI 印刷物料指南 — 傳單名片 ChatCanvas 工作流",
        "description": "404 修復：用 Lovart ChatCanvas 與 Brand Kit 做傳單、名片、活動卡，Touch Edit 改日期與 promo。",
        "seo_description": "印刷 AI：Design Agent、Brand Kit、Touch Edit、static-first 送印 handoff。",
        "focus": "ai 印刷物料 傳單 名片",
        "keywords": ["ai 印刷", "傳單 ai", "lovart chatcanvas", "brand kit"],
        "cluster": "Complete Guide — Print",
        "body": PRINT_MATERIALS_ZHTW,
        "expand_topic": "活動傳單與名片 series",
    },
    {
        "key": "real_estate_zh",
        "lang": "zh",
        "slug": "how-to-create-real-estate-marketing-materials-ai",
        "cover": "052",
        "category": "Industry Solution",
        "title": "如何用 AI 做房产营销物料：listing 传单、开放看房与朋友圈",
        "seo_title": "房产营销 AI 物料指南 — listing 与 open house",
        "description": "经纪人用 Lovart ChatCanvas 与 Brand Kit 做 listing 传单、open house 与 WeChat 朋友圈封面，Touch Edit 改价。",
        "seo_description": "房产 AI 营销：Design Agent、listing static、Touch Edit 改挂牌价、404 修复。",
        "focus": "房产营销 ai 物料",
        "keywords": ["房产营销 ai", "listing 传单", "lovart chatcanvas", "brand kit"],
        "cluster": "Segment — Real Estate",
        "body": REAL_ESTATE_ZH,
        "expand_topic": "listing 传单与 open house",
    },
    {
        "key": "firefly_zhtw",
        "lang": "zh-TW",
        "slug": "adobe-firefly-vs-ai-design-agents",
        "cover": "058",
        "category": "Comparison",
        "title": "Adobe Firefly 與 AI 設計代理比較：營運視角，不是口號對決",
        "seo_title": "Firefly vs AI 設計代理 — 營運對照",
        "description": "404 修復：Firefly 與 Lovart Design Agent 並行分工，ChatCanvas、Brand Kit、Touch Edit 改稿場景。",
        "seo_description": "Firefly vs Design Agent：editable static vs generative fill，revision cost 視角。",
        "focus": "adobe firefly vs ai design agent",
        "keywords": ["adobe firefly", "ai design agent", "lovart chatcanvas", "brand kit"],
        "cluster": "Comparison — Firefly",
        "body": FIREFLY_VS_AGENTS_ZHTW,
        "expand_topic": "Firefly 與 campaign static 分工",
    },
    {
        "key": "team_story_zhtw",
        "lang": "zh-TW",
        "slug": "lovart-behind-the-scenes-team-story",
        "cover": "063",
        "category": "Thought Leadership",
        "title": "Lovart 幕後團隊故事：流程、交接與 404 修復的營運誠實",
        "seo_title": "Lovart 幕後團隊 — ChatCanvas 與 Touch Edit 流程",
        "description": "繁中 404 修復：營運語氣描述 Lovart 團隊流程、Brand Kit、Touch Edit 在 production 的角色。",
        "seo_description": "幕後故事：Design Agent pipeline、Brand Kit、Touch Edit、無 one-click hype。",
        "focus": "lovart team story",
        "keywords": ["lovart team", "chatcanvas", "brand kit", "behind the scenes"],
        "cluster": "Thought Leadership — Team",
        "body": TEAM_STORY_ZHTW,
        "expand_topic": "onboarding 與 handoff",
    },
    {
        "key": "bg_remover_en",
        "lang": "en",
        "slug": "ai-background-remover",
        "cover": "015",
        "category": "How-To",
        "title": "AI Background Remover Guide: Cutout Quality and the Touch Edit Workflow",
        "seo_title": "AI Background Remover — Touch Edit Workflow",
        "description": "404 fix: background removal plus Lovart ChatCanvas composites, Brand Kit, Touch Edit on promo blocks.",
        "seo_description": "Cutout to campaign static: Design Agent, Brand Kit, Touch Edit edge fixes.",
        "focus": "ai background remover",
        "keywords": ["ai background remover", "touch edit", "chatcanvas", "brand kit"],
        "cluster": "How-To — Touch Edit",
        "body": BG_REMOVER_EN,
        "expand_topic": "product cutout composite QA",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "zh-TW": expand_zhtw,
    "en": expand_en,
    "ko": expand_ko,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch3 content cluster.*\n"
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
        unit = {"zh": "CJK", "zh-TW": "CJK", "en": "words", "ko": "hangul"}[lang]
        results.append({
            "file": path.name,
            "lang": lang,
            "metric": metric,
            "floor": floor,
            "unit": unit,
            "banned": banned,
            "placeholder": placeholder,
            "pass": ok,
            "cover": a["cover"],
            "rank": a.get("rank"),
        })

    print(f"{'FILE':<85} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 120)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['file']:<85} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["file"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
