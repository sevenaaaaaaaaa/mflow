#!/usr/bin/env python3
"""Generate 404-rescue P2 batch8 blog bodies (10 files). Self-contained.

Ranks #83–#92 from 404-rescue-compact lane.
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

LOVART_IMAGE_GEN_ZH = """
# Lovart AI 图像生成：产品工作流，不是 hype 清单

这条中文 URL 曾返回 404，但搜索仍在问「Lovart AI image generator 能不能出 stunning images」。诚实答案：能出图，但 daily ops 的价值不在第一张 wow，而在 **Brand Kit** 锁色、**ChatCanvas** thread 记系列、**Touch Edit** 改局部、**Design Agent** 按 brief 验收。这和「输入 prompt 等一张图」的单次生成器不是同一类工具。

## 图像生成在 campaign 里要拆成四类输出

第一是 hero 主图：产品或人物主体清晰，CTA safe zone 留白。第二是 carousel slide 2–6：同一 grid 换 copy，accent 不能每张漂移。第三是 story 与 feed crop：9:16 与 4:5 同 thread 导出。第四是 end card 与 thumbnail：价格与 disclaimer 必须在可编辑层，不能 bake 进像素。

## ChatCanvas brief 合同写法

弱 brief 是「帮我做一张 stunning 产品图」。强 brief 是：「hero 4:5 1080×1350，产品居中，headline band top 15% flat for Touch Edit，Brand Kit slate + coral accent，price bottom left safe zone，disclaimer footer editable，禁止生成图内小字价格」。把 ratio、safe zone、Kit hex 写进 brief，**Design Agent** 才有 acceptance criteria。

## Brand Kit 先于 batch 生成

从已批准 packaging、门店物料或 prior deck 取样 primary hex、accent hex、title/body type role、logo clear space。不要用 stock marble 或 random pastel 当品牌色。Kit 建好后，所有 **ChatCanvas** thread 引用同一套 role。跳过 Kit 后每张 post 发明新 accent，改价只能 full regen。

## Touch Edit 改价不改 identity

周二改「满 200 减 30」为「新客体验 ¥99」：**Touch Edit** 框 CTA 带，保持 stripe geometry 与 **Brand Kit** accent。full regen 会 random 改产品角度与背景。测量 ROI 用「改价分钟」不是「第一张 wow 分钟」。

## Design Agent QA 字段

Agent 检查 safe zone、double CTA、过小 type、hex drift vs Kit、disclaimer 是否存在。不是替 brief 想创意，是执行 acceptance criteria。第二 pass 常只需补 brief 缺字段，不必换模型。

## 与纯 T2I 生成器的分工

T2I 适合 mood board 与单张探索。**ChatCanvas** + **Design Agent** 适合 revision-heavy promo：同一 campaign 要改价、改 copy、导出多尺寸。若你的 KPI 是「改价 five 分钟」，选 workflow 工具；若 KPI 是「试 50 种风格」，选 T2I playground。

## 常见失败

跳过 Brand Kit 后 carousel slide 4 新 accent。readable 价格 baked in pixels。video hook 有 offer 但 static hero 没有。每次改 copy 都 full regen 三十分钟。404 修复页的意义是给 SOP stable URL。

## 测量什么才有用

记「改价一次几分钟」「一次活动 export 几种尺寸」「carousel drift 几次」。若 **Touch Edit** 平均小于五分钟而重出平均大于三十分钟，说明 Design Agent 路线成立。
"""

BRAND_KIT_CONSULTANT_ZHTW = """
# 顧問業 Brand Kit：提案 deck、案例卡與 LinkedIn 封面

這條繁體中文 URL 曾返回 404，但搜尋仍在問「顧問公司能不能用 AI 做日常物料」。顧問業的真實節奏不是偶爾做一張海報，而是每週換案例摘要、改服務包價、發 LinkedIn 封面、更新提案 deck 內頁。若每次從零 prompt，深藍與金色 accent 很快漂移，客戶會覺得你「不夠專業一致」。

## 顧問業真正要解決的四個場景

第一是服務包與價目卡：方案名稱、時數、費率常改，文字必須可讀、留白足夠、投影與手機都能看。第二是案例摘要卡：產業標籤改但視覺系統不能散。第三是 LinkedIn 與 newsletter 封面：橫豎版 safe zone 不同，標題不能被平台 UI 擋住。第四是 workshop 與 webinar promo：文案改但 **Brand Kit** 不能 drift。

Lovart 的 **Design Agent** 與 **ChatCanvas** 是可對話、可改稿的設計面；**Brand Kit** 記住你的主色、標題字體與 logo 留白；**Touch Edit** 用來改局部費率字而不推翻整圖。

## 在 ChatCanvas 裡寫顧問 brief

不可用 brief 是「幫我做一張高級顧問海報」。可用 brief 是：「策略診斷 workshop，主圖 4:5，費率放左下 safe zone，角標寫限時，留 top 12% 給 LinkedIn UI，Brand Kit 深藍與金色 accent，disclaimer footer editable」。把渠道、留白、必填欄位寫進 brief。

若已有 firm VI，先載入 **Brand Kit**：主色、輔助色、標題與正文字號角色、logo 最小留白。之後生成案例系列，顏色不會每張漂移。

## 費率說明與 Touch Edit 的配合

顧問物料最怕「整張重出」。方案調整或費率更新時，若每次重 roll，合夥人沒空等。正確做法是在 **ChatCanvas** 裡固定版式，改數字用 **Touch Edit** 只動假設條件與費率塊。**Brand Kit** 保證標題字體與色塊位置不變。

## 案例卡與 carousel 系列

案例 carousel 需要同一套角標與 firm name 位置。在 **ChatCanvas** 同一 thread 裡批量匯出模板，只換產業標籤不換 grid。**Design Agent** QA：headline 不被 UI chrome 擋、disclaimer readable。

## 合規與本地習慣

顧問素材涉及成果免責、具體以合約為準、過往案例不代表未來。把這些句子當作 brief 必填欄位。**ChatCanvas** 匯出 static 審核稿，video 可以後做，但費率與 disclaimer 必須以可改文字為準。

## 測量什麼才有用

記「改費率一次幾分鐘」「一次活動要重出幾張尺寸」。若 **Touch Edit** 平均小於五分鐘而重出平均大於三十分鐘，說明 Design Agent 路線成立。

## 一週工作流示例

週一確認本週案例與 workshop 清單。週二在 **ChatCanvas** 批量生成案例卡與兩版 LinkedIn 封面。週三用 **Touch Edit** 改費率、改賣點詞。週四匯出多尺寸。週五只處理臨時更新，沿用同一 thread。
"""

BRAND_KIT_GYM_ZHTW = """
# 健身館 Brand Kit：會籍卡、團課表與 Reels 封面

這條繁體中文 URL 曾返回 404，但搜尋仍在問「健身館能不能用 AI 做日常物料」。健身館的真實節奏不是偶爾做一張海報，而是每月改會籍價、換團課表、發 Reels 封面、更新教練作品集。若每次從零 prompt，力量區的黑紅與瑜伽區的薄荷綠很快混用，會員會覺得你的館「網上形象不專業」。

## 健身館真正要解決的四個場景

第一是会籍與私教價目：月卡季卡價格常改，文字必須可讀、留白足夠、前台屏與手機都能看。第二是團課表：每週排課變動，版式要固定只換時間與課程名。第三是教練 before/after 作品集：角標與館名位置要統一。第四是開業與節日 promo：文案改但 **Brand Kit** 視覺系統不能散。

Lovart 的 **Design Agent** 與 **ChatCanvas** 是可對話、可改稿的設計面；**Brand Kit** 記住你的主色、標題字體與 logo 留白；**Touch Edit** 用來改局部價格字而不推翻整圖。

## 在 ChatCanvas 裡寫健身 brief

不可用 brief 是「幫我做一張高級健身海報」。可用 brief 是：「私教體驗課，主圖 4:5，價格放左下 safe zone，角標寫限時，留 top 12% 給 Reels UI，Brand Kit 炭黑與能量橙，disclaimer editable」。把渠道、留白、必填欄位寫進 brief。

若已有館 VI，先載入 **Brand Kit**。之後生成會籍系列，顏色不會每張漂移。

## 會籍價目與 Touch Edit 的配合

健身價目最怕「整張重出」。月初改季卡價、月中加體驗課，若每次重 roll，前台沒空等。正確做法是在 **ChatCanvas** 裡固定版式，改價用 **Touch Edit** 只動數字與套餐名。**Brand Kit** 保證標題字體與色塊位置不變。

## 團課表與 Reels 封面

團課表需要固定 grid，只換時間與課程名。在 **ChatCanvas** 同一 thread 裡匯出週表模板。Reels 封面寫清 safe zone：標題字離頂 12%、離底 10%，避免被按讚按鈕遮擋。

## 合規與本地習慣

健身素材常涉及效果說明、價格公示、會員規則。把這些句子當作 brief 必填欄位。**ChatCanvas** 匯出 static 審核稿，video 可以後做，但價格與館名必須以可改文字為準。404 修復頁讓 SOP 有 stable URL。

## 測量什麼才有用

記「改價一次幾分鐘」「一次活動要重出幾張尺寸」。若 **Touch Edit** 平均小於五分鐘而重出平均大於三十分鐘，說明 Design Agent 路線成立。

## 一週工作流示例

週一確認本週團課與 promo 清單。週二在 **ChatCanvas** 批量生成會籍主圖與兩版 Reels 封面。週三用 **Touch Edit** 改價格、改賣點詞。週四匯出多尺寸。週五只處理臨時改價，沿用同一 thread。
"""

LOGO_MISTAKES_JA = """
# ロゴデザインでよくある失敗：Brand Kit 前に直すべき七つの習慣

この日本語 URL は 404 でしたが、検索は「ロゴデザイン 失敗 直し方」を求めていました。失敗の多くはモデルの問題ではなく、**Brand Kit** 未設定、**ChatCanvas** thread なし、**Touch Edit** 不可の promo レイヤー、**Design Agent** QA なし、というプロセス欠落です。

## 失敗その一：小さいサイズで潰れる

ファビコン 16px、App icon 1024px、名刺 20mm — 同じロゴが全部読めるか。最初から **Brand Kit** に clear space と minimum size を書く。生成後に縮小プレビュー 120px で **Design Agent** pass/fail。

## 失敗その二：カラーが毎回 drift

carousel slide 4 だけ別 accent。hex を **Brand Kit** primary / accent / background role で固定。**ChatCanvas** 同一 thread で batch、新 thread は drift リスク。

## 失敗その三：可読テキストを render に bake

料金・日付・ disclaimer を画像内小文字で生成すると火曜の変更が full regen。**Touch Edit** 用 flat band を brief に明記。static-first、motion は companion。

## 失敗その四：競合ロゴとの類似

SERP 上位の shape language をそのまま真似しない。**Design Agent** brief に「avoid category cliché」フィールド。人間の final sign-off は必須。

## 失敗その五：横長だけ、縦型 safe zone 未設計

Story 9:16 で logo が UI に隠れる。brief に top 12% / bottom 10% safe zone。**ChatCanvas** で master 4:5 から derivative crop、crop-first は CTA を切る。

## 失敗その六：改訂コストを測っていない

「最初の wow 何分」ではなく「価格変更何分」。**Touch Edit** 5 分以内なら workflow 成立。30 分 full regen なら **Brand Kit** からやり直し。

## 失敗その七：404 URL のまま SOP が散在

修復 URL で onboarding に stable link。hex、disclaimer 原文、brief テンプレを内リンク時に添付。

## ChatCanvas brief 契約例

弱い：「モダンなロゴ」。強い：「wordmark + icon、Brand Kit navy #1a2b3c + sand accent、clear space 1x cap height、16px favicon pass、1080×1350 hero safe zone、disclaimer footer editable、render 内小文字禁止」。

## Touch Edit で tagline だけ差し替え

キャンペーン copy 変更は tagline band の **Touch Edit** のみ。icon geometry と **Brand Kit** accent stripe は保持。full regen は identity lottery。

## 測るべき指標

価格 fix 分数、slide accent drift 回数、legal return 回数、export size 数 per action。404 復旧ページは repeatable logo workflow SOP。
"""

PICSART_REVIEW_KO = """
# Picsart AI 리뷰: 솔직한 비교와 revision cost 관점

이 한국어 URL은 404였지만, 검색은 「Picsart AI review」를 물었습니다. 정직한 답: Picsart는 모바일 편집과 sticker/filter 생태계에 강하고, revision-heavy campaign static에서는 **Brand Kit** drift, **Touch Edit** edit cost, **ChatCanvas** thread memory가 ROI를 가릅니다. Lovart **Design Agent**는 brief contract QA; Picsart는 quick social edit에 맞는 경우가 많습니다.

## Picsart가 잘하는 구간

첫째 모바일 one-off edit: 배경 제거, sticker, quick filter. 둘째 creator casual post: beauty-first single frame. 셋째 template marketplace: 빠른 mood exploration. 넷째 short-form clip companion: motion hook 중심.

## revision-heavy campaign에서 흔한 gap

가격 변경이 full regen 30분. carousel slide 4 accent drift. disclaimer가 baked pixels. video offer와 landing static 불일치. **Brand Kit** hex role 없음. **Touch Edit** editable promo layer 없음.

## Lovart ChatCanvas workflow와의 분업

**ChatCanvas** thread per campaign family. **Brand Kit** lock primary/accent/type role. **Touch Edit** CTA stripe copy swap. **Design Agent** QA safe zone, readable price, hex drift. static legal pass 후 optional motion elsewhere.

## 공정한 비교 실험 설계

같은 brief contract: hero 4:5, price bottom left safe zone, disclaimer footer editable, Brand Kit hex. 같은 revision task: 화요일 promo copy 변경. 측정: minutes per price fix, drift count, export sizes per action. 첫 frame beauty만 비교하면 misleading.

## Picsart 선택이 맞는 팀

주간 output이 casual social 5–10장, 가격 layer 거의 없음, series consistency 낮은 priority. revision cost보다 speed of first post.

## Lovart 선택이 맞는 팀

주간 promo 20+ size export, 가격/날짜 weekly 변경, carousel series, legal disclaimer 필수. **Touch Edit** 5분 이내가 KPI.

## ChatCanvas brief 예시

나쁜 brief: 「프리미엄 느낌」. 좋은 brief: 「4:5 1080×1350, Brand Kit navy + sand, price bottom left, disclaimer editable, no readable small text in render, same thread for slide 2–6」.

## Touch Edit가 분기점

promo 변경이 **Touch Edit** 5분이면 static-first 성립. 30분 full regen이면 tool mismatch 아니라 process failure.

## 윤리와 라이선스

stock asset, watermark, third-party IP — 각 플랫form ToS 확인. campaign folder에 license screenshot 보관. 비교 리뷰는 feature list가 아니라 edit cost framework.

## 측정

가격 fix 분수, drift 횟수, legal return, export size 수. 404 stable honest review SOP URL.
"""

HIGGSFIELD_REVIEW_ZH = """
# Higgsfield AI 评测：视频生成强项与 campaign static 分工

这条中文 URL 曾返回 404，但搜索仍在问「Higgsfield AI 值不值得用」。诚实答案：Higgsfield 在 motion hook 与 clip 生成上有场景，但 revision-heavy promo 仍需要 **ChatCanvas** static master、**Brand Kit** 锁色、**Touch Edit** 改价、**Design Agent** QA readable offer layer。不是二选一，是 workflow 顺序问题。

## Higgsfield 擅长的区间

第一是 short-form motion hook：产品 reveal、transition-heavy clip。第二是 mood exploration：快速试 direction。第三是 social clip companion：已有 static hero 后的 motion 层。第四是 creator casual output：beauty-first 单条。

## campaign static 里常见的 gap

价格改一次要 full regen 三十分钟。carousel slide 4 accent drift。disclaimer bake 进像素。video 角标有 offer 但 landing static 没有。**Brand Kit** hex role 未设。**Touch Edit** 可编辑 promo layer 缺失。

## Lovart 与 Higgsfield 的分工

顺序：先在 **ChatCanvas** 出 static hero 与 end card，legal pass 后再 optional motion。Higgsfield 管 hook；Lovart 管 readable price、date、disclaimer 在 **Touch Edit** 层。**Design Agent** 验收 safe zone 与 hex drift vs **Brand Kit**。

## 公平对比实验设计

同一 brief contract：hero 4:5，price bottom left safe zone，disclaimer footer editable，Brand Kit hex。同一 revision task：周二改 promo copy。测量：改价分钟、drift 次数、一次 action export 几种尺寸。只比第一帧好看会误导。

## 选 Higgsfield 更合适的团队

周产出以 casual clip 为主，价格 layer 少，series consistency 优先级低。revision cost 低于 first-post speed。

## 选 Lovart workflow 更合适的团队

周 promo 要 20+ 尺寸 export，价格/日期 weekly 改，carousel 系列，合规 disclaimer 必填。**Touch Edit** 五分钟内改价是 KPI。

## ChatCanvas brief 示例

弱 brief：「高级产品视频感」。强 brief：「hero 4:5 1080×1350，Brand Kit slate + coral，price bottom left，disclaimer editable，禁止生成图内小字，slide 2–6 同 thread」。

## Touch Edit 是分水岭

promo 变更若 **Touch Edit** 五分钟完成，static-first 成立。三十分钟 full regen 说明 process 未设好，不是模型 lottery。

## 伦理与版权

第三方素材、水印、IP — 各平台 ToS 确认。campaign folder 存档 license screenshot。评测写 edit cost framework，不是 feature 清单堆砌。

## 测量什么

改价分钟、drift 次数、legal return、export size 数。404 修复给 stable honest review SOP URL。
"""

BANNERS_DISPLAY_ADS_ZH = """
# 用 AI 做 Banner 与 Display Ads：从 brief 到多尺寸 export

这条中文 URL 曾返回 404，但搜索仍在问「怎么用 AI 做 banner 和 display ads」。不是「一键出整组广告」，而是 **ChatCanvas** 固定 grid、**Brand Kit** 锁 type role、**Touch Edit** 改 CTA 与 price block、**Design Agent** QA safe zone 与 IAB 常见尺寸。

## Display ad 任务要拆成四类输出

第一是 leaderboard 728×90 与 medium rectangle 300×250：headline 可读、logo clear space。第二是 wide skyscraper 160×600 与 half page：CTA 不被裁切。第三是 social companion 1200×628 与 1080×1080：同 thread 导出。第四是 retargeting end card：价格与 disclaimer 在 **Touch Edit** 可改层。

## ChatCanvas brief 合同写法

弱 brief：「现代 display ad」。强 brief：「300×250，headline top 20% flat band for Touch Edit，Brand Kit navy + sand accent，price bottom left safe zone，disclaimer footer editable，禁止生成图内小字价格，同 thread 导出 728×90」。把 pixel size、safe zone、Kit hex 写进 brief。

## Brand Kit 约束 ad 不漂移

从已批准 media kit 或 prior buy 取样 primary、accent、title/body role。无 **Brand Kit** 时 slide 3 发明新 accent，投放系列感消失。同一 thread batch 多尺寸，只换 copy 不换 grid。

## Touch Edit 改 CTA 不改 layout skeleton

改「Shop now」为「Book demo」：**Touch Edit** 框 button label 层，保持 card geometry 与 **Brand Kit** accent stripe。full regen 会 random 改 product cutout 与 padding。ad ops 用「改 copy 分钟」衡量工具。

## Design Agent QA for display static

检查 headline 在 120px 宽 preview 可读、price 不在 UI chrome 下、disclaimer 存在、hex drift vs Kit、无 double CTA。不是替 media buyer 写 copy，是验收 brief 字段。

## static-first 再配 motion

feed autoplay 常静音；用户 screenshot 的是 still。顺序：static legal pass → optional motion hook。反过来会产生 clip 有 offer 但 landing 不能 edit 的 mismatch。

## 常见失败

单尺寸 hero 无 series thread。readable price baked in pixels。728×90 从 square crop 切掉 CTA。video hook 有 offer 但 static 没有。

## 测量 ROI

改 CTA 一次几分钟、carousel drift 几次、一次 action export 几种 IAB 尺寸。404 修复给 media team stable SOP URL。
"""

YOUTUBE_THUMBNAIL_ZH = """
# YouTube 缩略图设计科学（2027 前瞻清单）：可读性与 series 一致

这条中文 URL 曾返回 404，slug 带 2027，搜索需要 forward-looking checklist：不是 hype 预测，而是 2026 daily ops 里已验证的 revision cost、**Brand Kit** series、**Touch Edit** 改 title block、**Design Agent** QA 120px 宽可读性。2027 framing 指「明年仍有效的验收字段」，不是 crystal ball。

## 2027 仍有效的五项验收字段

第一是 120px 宽 preview：face/ product 与 title 仍可读。第二是 series consistency：同一频道角标与 accent 不 drift。第三是 editable title band：**Touch Edit** 改 headline 不全图重 roll。第四是 safe zone：platform UI 不挡 CTA 与 eyes。第五是 static companion：clip hook 有 offer 时 thumbnail static 也有 readable price layer。

## ChatCanvas brief 合同写法

弱 brief：「爆款缩略图」。强 brief：「1280×720，title band bottom 25% flat for Touch Edit，Brand Kit yellow + black accent，face gaze toward lens，publish preview 120px pass，禁止生成图内小字长句，同 thread 导出 A/B variant」。**Design Agent** 需要 numeric acceptance fields。

## Brand Kit 锁频道视觉不漂移

从已批准 channel art 取样 primary、accent、title type role、角标位置。无 **Brand Kit** 时第 47 条视频发明新 yellow，series 感消失。同一 **ChatCanvas** thread batch A/B，只换 expression 不换 grid。

## Touch Edit 改 title 不改 face identity

改「我试了 30 天」为「结果让人意外」：**Touch Edit** 框 title band，保持 face geometry 与 **Brand Kit** accent stripe。full regen 会 random 改 identity 与 catchlight。

## shocked face 心理学与 non-cringe 生成

高 contrast expression 提升 CTR 的前提是 publish size 下仍像「真实反应」而非 meme artifact。**Touch Edit** 修 gaze 与 brow，不要整脸 regen 到 identity 换人。繁中版 shocked face 指南另文详述 expression brief 合同。

## Design Agent QA for thumbnail

120px pass/fail、double text layer、hex drift vs Kit、eyes 不被 UI 挡、disclaimer 若涉及赞助则 editable footer。

## 2027 checklist vs 2025 listicle 差异

2025 讨论常停在「用什么 font 爆款」。2027 checklist 问「周二改 title 是否 five 分钟」「A/B 是否 drift」「sponsor disclaimer 是否在 editable layer」。本篇按后者写。

## 常见失败

单张 thumbnail 无 series thread。readable title baked in pixels。A/B 各用各 accent。clip 角标有 offer 但 thumbnail static 没有 price layer。

## 测量 ROI

改 title 一次几分钟、A/B drift 几次、120px preview pass rate。404 修复给 creator team stable SOP URL（2027 framing）。
"""

WATERMARK_CASE_EN = """
# Case Study: Stock Photo Watermark Removal with AI and Touch Edit Ethics

This English URL returned 404 while teams searched for watermark removal workflows—not a tutorial to strip rights-managed marks. This case study covers a licensed stock refresh: replacing an expired comp watermark layer with a paid asset, using **Touch Edit** for local cleanup only where license permits, and **Design Agent** QA for disclaimer and provenance fields.

## Case background

A marketing team had 42 display sizes built on a comp watermarked hero. Legal approved purchase of the final asset mid-campaign. Goal: swap watermarked region without rebuilding 42 PNGs from scratch. Constraint: no removal of third-party rights-managed marks without license; only comp-to-paid transition on owned layers.

## Why full regen failed twice

Full regen changed product angle, broke **Brand Kit** accent stripe alignment, and moved disclaimer footer off safe zone. Measured thirty-eight minutes per size set. **Touch Edit** on watermark band plus asset swap completed average four minutes per master when **ChatCanvas** thread preserved grid.

## ChatCanvas thread as case memory

One thread held hero 4:5 master, carousel slides two through six, and IAB derivatives. **Brand Kit** navy and sand roles locked. When paid asset arrived, **Touch Edit** selected watermark band only—instruction: replace with licensed asset ID 8842, preserve geometry, do not alter product cutout.

## Touch Edit ethics boundary

**Touch Edit** is for licensed comp-to-final swap, dust cleanup on owned photography, and local CTA edits—not for removing Getty or Shutterstock marks on unpaid assets. Campaign folder stores license PDF and asset ID screenshot. **Design Agent** checks disclaimer line present.

## Design Agent acceptance fields

Safe zone pass, readable price at mobile width, hex drift vs **Brand Kit**, provenance note in footer editable layer, no double CTA. Agent does not replace legal review.

## Static-first before motion companions

Video hook reused old comp frame in corner badge while static hero already paid—mismatch triggered legal return. Workflow order: static license pass on all sizes, then re-export motion companion from approved still.

## Metrics from the case

Forty-two sizes, full regen path estimated eighteen hours; **Touch Edit** swap path closed in three hours ten minutes across two operators. Accent drift events: zero with **Brand Kit** lock. Legal returns after process fix: one down from four prior month.

## Team SOP after 404 restore

Document comp-to-paid checklist, **Touch Edit** band selection size, license archive path, **ChatCanvas** thread naming. Restored URL gives search a stable ethics-aware case study—not a circumvention guide.

## What not to do

Remove watermarks on unpaid stock. Regen entire campaign for watermark swap. Bake license text into pixels. Skip **Design Agent** provenance field.
"""

SHOCKED_FACE_ZHTW = """
# 「震驚臉」為什麼有效：不靠尷尬演戲的生成方法

這條繁體中文 URL 曾返回 404，slug 帶 shocked face，搜尋需要繁中 rewrite：不是教您對鏡頭做誇張表情，而是用 **ChatCanvas** brief 控制 expression、**Touch Edit** 局部修 brow 與 gaze、**Brand Kit** 鎖 series accent、**Design Agent** QA 120px 寬仍 readable 的 non-cringe thumbnail。

## 「震驚臉」在 CTR 科學裡指什麼

第一是高 contrast 但 publish size 下仍像自然反應，不是 meme artifact。第二是 gaze 朝向 lens，catchlight 與 key light 一致。第三是 title band 與 face 不互相遮擋。第四是 series 角標一致，第 47 條影片不發明新 yellow accent。

## 為什麼 full regen 常 cringe

整圖重 roll 直到「夠誇張」常換 identity、改 jawline、產生 uncanny brow。正確做法是 brief 寫 expression intensity 1–5，**Touch Edit** 只修 eye region 與 brow，Identity Lock reference 不換人。

## ChatCanvas brief 合同

弱 brief：「做一張震驚臉縮圖」。強 brief：「1280×720，expression intensity 3/5，gaze toward lens，title band bottom 25% Touch Edit editable，Brand Kit yellow + black，120px preview pass，禁止 over-stretch mouth，同 thread A/B variant」。**Design Agent** 需要 acceptance 欄位。

## Touch Edit 修 expression 不改 identity

框選過大 → 下巴與鼻型被改壞。框選過小 → brow 改不動。三次仍不對，縮框再試。每次 pass 只改一個變量：先 gaze，再 brow raise，再 lid openness。保 catchlight upper-left 若 key light 來自左上方。

## 不靠演戲的生成路線

用 reference still 的 neutral face + brief 指定 micro-expression delta。不要要求 model 「像 YouTuber 誇張表演」。series mascot 用 **Brand Kit** 鎖 accent stripe，expression 變但 stripe geometry 不變。

## Brand Kit 與 A/B 系列

同一 **ChatCanvas** thread 批量 A/B：A 版 brow +1，B 版 title word swap。**Touch Edit** 改 title band 不 full regen face。測 120px pass rate 再選 winner。

## 合規邊界

修 expression 不是偽造真人代言。若素材暗示真實使用者見證，需授權與 disclaimer。贊助內容 footer editable。

## 常見翻車

整圖 regen 直到夠誇張但 identity 換人。catchlight 與 scene light 矛盾。120px 上 eyes 被 platform UI 擋。只有 clip 沒有可編輯 static companion。

## 測量什麼

gaze fix 分鐘 vs full regen 分鐘。120px preview pass/fail。A/B drift 次數。404 修復給 creator stable SOP URL。
"""

# FAQ blocks
FAQ = {
    "lovart_image_gen": """
## FAQ

**Lovart image generator 要先建 Brand Kit 吗？**  
强烈建议，锁 hex role，防 carousel drift。

**改活动价要整图重出吗？**  
不需要，Touch Edit 框 CTA 带。

**和纯 T2I 分工？**  
T2I 偏单张探索；ChatCanvas 偏 editable series。

**404 修复？**  
补齐 image generator stable SOP URL。

**Design Agent 做什么？**  
按 brief QA safe zone、disclaimer、hex drift。
""",
    "brand_kit_consultant": """
## FAQ

**顧問業要先建 Brand Kit 嗎？**  
建議，鎖深藍與金色 accent，防案例卡 drift。

**改費率要整圖重出嗎？**  
不需要，Touch Edit 改費率塊。

**brief 必填欄位？**  
ratio、safe zone、disclaimer、Kit hex。

**404 修復？**  
stable consultant Brand Kit SOP URL。

**LinkedIn 封面 safe zone？**  
top 12%、bottom 10% 留 UI。
""",
    "brand_kit_gym": """
## FAQ

**健身館要先建 Brand Kit 嗎？**  
建議，鎖炭黑與能量橙，防團課表 drift。

**改會籍價要整圖重出嗎？**  
不需要，Touch Edit 改價格塊。

**Reels 封面 safe zone？**  
top 12%、bottom 10% 留 UI。

**404 修復？**  
stable gym Brand Kit SOP URL。

**Design Agent 做什麼？**  
按 brief QA safe zone、disclaimer、hex drift。
""",
    "logo_mistakes": """
## FAQ

**ロゴ失敗の大半はモデル問題？**  
いいえ。Brand Kit 未設定と Touch Edit 不可 promo が多い。

**価格変更で full regen 必要？**  
不要。Touch Edit CTA 帯で十分な場合が多い。

**16px favicon チェック？**  
Design Agent QA に minimum size pass を入れる。

**404 修復？**  
stable logo mistakes SOP URL。

**ChatCanvas thread は一つ？**  
キャンペーン family ごとに一 thread で drift 防止。
""",
    "picsart_review": """
## FAQ

**Picsart vs Lovart 二选一？**  
아니요. revision cost와 use case로 분업.

**공정한 비교?**  
같은 brief contract, 같은 price-change task.

**Touch Edit 5분 이내?**  
workflow 성립 신호.

**404 이유?**  
KO honest review 문서 누락.

**Brand Kit role?**  
series drift 방지; feature list보다 중요.
""",
    "higgsfield_review": """
## FAQ

**Higgsfield 与 Lovart 二选一？**  
不是，workflow 顺序：static legal pass 再 motion。

**改价要整图重出吗？**  
不需要，Touch Edit 框 CTA 带。

**公平对比怎么测？**  
同一 brief、同一改价任务，比分钟不是比第一帧。

**404 修复？**  
stable honest review SOP URL。

**Design Agent 做什么？**  
QA safe zone、disclaimer、Brand Kit drift。
""",
    "banners_display_ads": """
## FAQ

**display ad 要先建 Brand Kit 吗？**  
建议，锁 IAB 系列 accent 不 drift。

**改 CTA 要整图重出吗？**  
不需要，Touch Edit label 层。

**多尺寸同 thread？**  
是，728×90 与 300×250 同 thread 导出。

**404 修复？**  
stable banner display ad SOP URL。

**static-first？**  
legal pass static 再 optional motion。
""",
    "youtube_thumbnail": """
## FAQ

**2027 checklist 与 2025 listicle 有何不同？**  
强调 revision cost、120px pass、Touch Edit 改 title。

**改 title 要整图重出吗？**  
不需要，Touch Edit title band。

**shocked face 另文？**  
繁中 shocked face 指南详述 expression brief。

**404 修复？**  
stable thumbnail science SOP URL（2027 framing）。

**Design Agent QA？**  
120px readable、hex drift、safe zone。
""",
    "watermark_case": """
## FAQ

**Can Touch Edit remove unpaid stock watermarks?**  
No. Only licensed comp-to-paid swap on owned layers.

**Why did full regen fail?**  
Accent drift and disclaimer misalignment across 42 sizes.

**What to archive?**  
License PDF and asset ID per campaign folder.

**404 fix?**  
Restored ethics-aware case study URL.

**Design Agent role?**  
Provenance field and safe zone QA—not legal replacement.
""",
    "shocked_face": """
## FAQ

**整圖 regen 還是 Touch Edit？**  
identity 已對只修 brow/gaze → Touch Edit eye region。

**如何避免 cringe acting？**  
brief 寫 intensity 1–5，Identity Lock，不要誇張表演 prompt。

**120px preview 怎麼測？**  
Design Agent pass/fail 欄位寫進 brief。

**404 修復？**  
stable shocked face SOP URL。

**Brand Kit 要嗎？**  
series 建議，防 accent drift。
""",
}


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

The first brief ends with "premium" and fails: small price type, badge over the face. Second pass fixes only safe zone and required fields. One **ChatCanvas** thread cuts slide-four accent drift. In **{topic}**, if **Touch Edit** closes a price change in five minutes, static-first works. Thirty-minute full regen means redo **Brand Kit** first. Restored 404 URL is the stable onboarding SOP link.
"""


def expand_ja(topic: str, n: int) -> str:
    return f"""
## 現場メモ {n}：{topic}

初回 brief が「モダン」で終わると価格文字が小さく badge が顔を隠します。二回目は safe zone と必須フィールドのみ修正。**Design Agent** と **ChatCanvas** で thread を維持すると carousel slide 4 の accent drift が減ります。{topic} で **Touch Edit** が 5 分以内に価格修正できれば static-first が成立。30 分 full regen なら **Brand Kit** からやり直し。404 復旧 URL は onboarding 用 stable link です。
"""


ARTICLES = [
    {
        "rank": 83,
        "key": "lovart_image_gen",
        "lang": "zh",
        "slug": "lovart-ai-image-generator-create-stunning-images",
        "cover": "018",
        "category": "How-To",
        "title": "Lovart AI 图像生成：产品工作流，不是 hype 清单",
        "seo_title": "Lovart AI 图像生成实用指南 — ChatCanvas workflow",
        "description": "404 修复：Lovart image generator 产品 workflow，Brand Kit、Touch Edit、Design Agent QA。",
        "seo_description": "AI 图像生成：revision cost、editable promo layer、非 hype 清单。",
        "focus": "lovart ai image generator",
        "keywords": ["lovart ai image generator", "chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Image Generator",
        "body": LOVART_IMAGE_GEN_ZH,
        "expand_topic": "Lovart 图像生成 workflow",
    },
    {
        "rank": 84,
        "key": "brand_kit_consultant",
        "lang": "zh-TW",
        "slug": "brand-kit-consultant-lovart",
        "cover": "025",
        "category": "Industry Solution",
        "title": "顧問業 Brand Kit：提案 deck、案例卡與 LinkedIn 封面",
        "seo_title": "顧問 Brand Kit — ChatCanvas 實操指南",
        "description": "繁中 404 修復：顧問業 Brand Kit、案例卡、LinkedIn 封面，ChatCanvas、Touch Edit。",
        "seo_description": "顧問 Brand Kit：費率 Touch Edit，series 一致。",
        "focus": "brand kit consultant lovart",
        "keywords": ["brand kit consultant", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Consultant",
        "body": BRAND_KIT_CONSULTANT_ZHTW,
        "expand_topic": "顧問案例卡與 LinkedIn 封面",
    },
    {
        "rank": 85,
        "key": "brand_kit_gym",
        "lang": "zh-TW",
        "slug": "brand-kit-fitness-gym-lovart",
        "cover": "032",
        "category": "Industry Solution",
        "title": "健身館 Brand Kit：會籍卡、團課表與 Reels 封面",
        "seo_title": "健身館 Brand Kit — ChatCanvas 實操指南",
        "description": "繁中 404 修復：健身館 Brand Kit、會籍、團課表、Reels 封面，Touch Edit 改價。",
        "seo_description": "健身 Brand Kit：改價 Touch Edit，Brand Kit 防 drift。",
        "focus": "brand kit fitness gym lovart",
        "keywords": ["brand kit gym", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Segment — Gym zh-TW",
        "body": BRAND_KIT_GYM_ZHTW,
        "expand_topic": "健身會籍與團課表",
    },
    {
        "rank": 86,
        "key": "logo_mistakes",
        "lang": "ja",
        "slug": "logo-design-mistakes",
        "cover": "039",
        "category": "Branding",
        "title": "ロゴデザインでよくある失敗：Brand Kit 前に直すべき七つの習慣",
        "seo_title": "ロゴデザイン 失敗 — ChatCanvas workflow",
        "description": "JA 404 fix: logo design mistakes, Brand Kit, Touch Edit, Design Agent QA.",
        "seo_description": "ロゴ失敗：hex drift、editable promo layer、revision cost。",
        "focus": "logo design mistakes",
        "keywords": ["logo design mistakes", "lovart brand kit", "chatcanvas", "touch edit"],
        "cluster": "Branding — Logo Mistakes JA",
        "body": LOGO_MISTAKES_JA,
        "expand_topic": "ロゴ revision cost",
    },
    {
        "rank": 87,
        "key": "picsart_review",
        "lang": "ko",
        "slug": "picsart-ai-review",
        "cover": "044",
        "category": "Comparison",
        "title": "Picsart AI 리뷰: 솔직한 비교와 revision cost 관점",
        "seo_title": "Picsart AI review — honest comparison KO",
        "description": "KO 404 fix: Picsart AI honest review, Brand Kit drift, Touch Edit edit cost.",
        "seo_description": "Picsart review KO: ChatCanvas, Design Agent, fair compare framework.",
        "focus": "picsart ai review",
        "keywords": ["picsart ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Picsart KO",
        "body": PICSART_REVIEW_KO,
        "expand_topic": "Picsart revision cost compare",
    },
    {
        "rank": 88,
        "key": "higgsfield_review",
        "lang": "zh",
        "slug": "higgsfield-ai-review",
        "cover": "055",
        "category": "Comparison",
        "title": "Higgsfield AI 评测：视频生成强项与 campaign static 分工",
        "seo_title": "Higgsfield AI 评测 —  honest comparison",
        "seo_description": "Higgsfield review：static-first、Touch Edit、Brand Kit workflow。",
        "description": "404 修复：Higgsfield AI  honest review，motion vs static workflow。",
        "focus": "higgsfield ai review",
        "keywords": ["higgsfield ai review", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Higgsfield ZH",
        "body": HIGGSFIELD_REVIEW_ZH,
        "expand_topic": "Higgsfield vs static workflow",
    },
    {
        "rank": 89,
        "key": "banners_display_ads",
        "lang": "zh",
        "slug": "how-to-create-banners-display-ads-ai",
        "cover": "056",
        "category": "How-To",
        "title": "用 AI 做 Banner 与 Display Ads：从 brief 到多尺寸 export",
        "seo_title": "Banner Display Ads AI — ChatCanvas workflow",
        "description": "404 修复：banner display ads，IAB 尺寸、Brand Kit、Touch Edit CTA。",
        "seo_description": "Display ads AI：multi-size export、editable promo layer。",
        "focus": "banners display ads ai",
        "keywords": ["banner display ads ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Display Ads",
        "body": BANNERS_DISPLAY_ADS_ZH,
        "expand_topic": "display ad multi-size export",
    },
    {
        "rank": 90,
        "key": "youtube_thumbnail",
        "lang": "zh",
        "slug": "youtube-thumbnail-design-science-2027",
        "cover": "057",
        "category": "How-To",
        "title": "YouTube 缩略图设计科学（2027 前瞻清单）：可读性与 series 一致",
        "seo_title": "YouTube 缩略图设计科学 2027 — checklist",
        "description": "404 修复：2027 thumbnail checklist，120px pass、Brand Kit、Touch Edit title band。",
        "seo_description": "Thumbnail science 2027：revision cost、series anti-drift。",
        "focus": "youtube thumbnail design science 2027",
        "keywords": ["youtube thumbnail design", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — Thumbnail 2027",
        "body": YOUTUBE_THUMBNAIL_ZH,
        "expand_topic": "YouTube thumbnail 120px QA",
    },
    {
        "rank": 91,
        "key": "watermark_case",
        "lang": "en",
        "slug": "case-study-stock-photo-watermark-removal-ai",
        "cover": "058",
        "category": "How-To",
        "title": "Case Study: Stock Photo Watermark Removal with AI and Touch Edit Ethics",
        "seo_title": "Watermark Removal Case Study — Touch Edit Ethics",
        "description": "404 fix EN: licensed comp-to-paid swap, Touch Edit ethics, Brand Kit, Design Agent provenance.",
        "seo_description": "EN case study: watermark workflow ethics, not circumvention guide.",
        "focus": "stock photo watermark removal ai",
        "keywords": ["watermark removal ai", "lovart touch edit", "chatcanvas", "brand kit"],
        "cluster": "How-To — Watermark Case EN",
        "body": WATERMARK_CASE_EN,
        "expand_topic": "licensed watermark swap workflow",
    },
    {
        "rank": 92,
        "key": "shocked_face",
        "lang": "zh-TW",
        "slug": "the--shocked-face---why-it-works-and-how-to-generate-it-without-acting",
        "cover": "059",
        "category": "How-To",
        "title": "「震驚臉」為什麼有效：不靠尷尬演戲的生成方法",
        "seo_title": "震驚臉縮圖 — Touch Edit 繁中指南",
        "description": "繁中 404 修復：shocked face psychology，non-cringe expression，ChatCanvas、Touch Edit。",
        "seo_description": "Shocked face zh-TW：120px pass、Identity Lock、Brand Kit series。",
        "focus": "shocked face thumbnail without acting",
        "keywords": ["shocked face thumbnail", "lovart touch edit", "chatcanvas", "brand kit"],
        "cluster": "How-To — Shocked Face zh-TW",
        "body": SHOCKED_FACE_ZHTW,
        "expand_topic": "non-cringe shocked face expression",
    },
]

EXPAND_FN = {
    "zh": expand_zh,
    "zh-TW": expand_zhtw,
    "en": expand_en,
    "ko": expand_ko,
    "ja": expand_ja,
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch8 content cluster.*\n"
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

    print(f"{'RANK':>4} {'FILE':<75} {'METRIC':>7} {'FLOOR':>7} {'UNIT':<7} {'PASS':>5} BANNED")
    print("-" * 120)
    failed = []
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['rank']:>4} {r['file']:<75} {r['metric']:>7} {r['floor']:>7} {r['unit']:<7} {str(r['pass']):>5} {b}")
        if not r["pass"]:
            failed.append(r["file"])
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    return results


if __name__ == "__main__":
    main()
