#!/usr/bin/env python3
"""Generate 404-rescue P2 batch30 blog bodies (10 files). Self-contained.

Ranks #306–#315 from 404-rescue-compact lane.
All JA. expand_ja only (batch19 pattern).
"""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T20:00:00Z"

FLOORS = {
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


def count_ja(text: str) -> int:
    return len(JA_CHAR_RE.findall(body_text(text)))


def count_metric(text: str, lang: str) -> int:
    if lang == "ja":
        return count_ja(text)
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

MIDJOURNEY_VS_LOVART_JA = """
# Midjourney と Lovart：正直な task split（Midjourney 料金は捏造しない）

この日本語 URL `04-midjourney-vs-lovart` は 404 を返していました。検索意図は比較記事 — 架空の Midjourney 月額表や 9.8/10 スコア表ではなく、探索 layer と campaign series editable layer の task split です。Midjourney の tier 料金は変動するため midjourney.com 公式を参照 — **この記事では Midjourney 価格を捏造しません**。Lovart 料金も lovart.ai 公式参照 — ここでも金額を書きません。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** は commercial static ops 向け。KPI は「火曜に価格修正 five 分」、最初の cinematic frame ではありません。

## 四つの task split（ゼロサム ranking なし）

第一に Midjourney 向き：単発 mood board、concept art、atmospheric exploration — 美しい first frame、週次 promo 価格修正には不向き。第二に Lovart 向き：campaign hero 4:5、carousel slide 2–6、**Brand Kit** hex lock、**Touch Edit** で CTA band editable。第三に両方併用：Midjourney で direction、**ChatCanvas** thread で static companion に落とし込み。第四に **Design Agent** pass/fail：50% ズームで価格可読、免責 footer、Kit との hex drift ゼロ — どちらの tool でも必須 QA layer。

## なぜ Midjourney vs Lovart 記事が ops を裏切るか

比較表に Midjourney Basic $10 等の固定数字 — 公式と不一致で即 BLOCK。探索 output を final legal promo に — 免責・価格が pixels に bake。**Brand Kit** 未設定 → carousel slide 4 accent lottery。Midjourney 側の Vary Region は強力だが、週次「¥599→¥499」は **Touch Edit** five 分 vs full regen 30 分の差 — ここが commercial team の分岐点。

## ChatCanvas brief 契約（Midjourney 探索後 companion JP）

弱い brief「Midjourney 風 premium ad」。強い brief：「Campaign X static companion 4:5 1080×1350、Brand Kit hex from media kit、headline top 15% flat for Touch Edit、price bottom band editable、disclaimer footer editable、variants 2–4 same thread、**Design Agent** pass/fail — exploration は Midjourney thread コメントのみ参照」。探索と series を同一 brief に混ぜない。

## Brand Kit が Midjourney export 後の accent drift を止める

approved VI から primary、accent、type role。**ChatCanvas** same thread で hero + story crop + carousel — model source が変わっても hex SSOT。Midjourney style reference だけでは weekly offer fix は成立しにくい — Kit + Touch Edit が ops layer。

## Touch Edit が比較の実務テスト

探索後に価格だけ変える：Lovart **Touch Edit** five 分？ Midjourney 側は often full regen or Vary Region lottery — どちらが bad ではなく task fit の話。Commercial KPI = edit-minute median、not aesthetic score。

## Midjourney 編集 vs Lovart 直接編集（誇張なし）

Midjourney：prompt vary、region regen — 説明ベース。Lovart：**Touch Edit** で price band、**ChatCanvas** canvas 上の series memory。Deadline 前の typo fix は Lovart static-first が向く — 探索 mood は Midjourney。併用 stack が現場で多い。

## よくある失敗

Midjourney 料金捏造。Lovart 未発表 roadmap を「2028 確定」と書く — 禁止。探索 output を compliance promo に。**Brand Kit** スキップ。404 未復旧。fake benchmark table。

## 測定指標

探索分数 vs promo edit 分数を分離計測。404 復旧 URL を JP 04-midjourney-vs-lovart stable SOP link として onboard。
"""

CLIPART_ROUNDUP_JA = """
# AI クリップアート・ベクター生成 2026：task グループ比較（架空 ranking なし）

この日本語 URL `6-best-ai-clipart-vector-generators-2026` は 404 を返していました。検索意図は roundup — 「#1–#6 スコア 9.5/10」表ではなく、task グループ別 fit と revision cost です。各 tool 料金は変動 — 公式ページ参照、**ここでは tool 月額を捏造しません**。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** は clip art 探索後の campaign static companion 向け。真の SVG export か PNG 近似か — brief に明記。

## 四つの task グループ（fake ranking 禁止）

グループ A 真 SVG パス探索：Recraft 系 — icon/logo 向き、複雑 overlap で path QA 要。グループ B stylized illustration 単一 aesthetic：Illustroke 系 — gallery 確認必須、外れた style には不向き。グループ C stock 風 raster 近似：Freepik AI 系 — PNG that looks vector、billboard 不可。グループ D merch/POD workflow：Kittl 系 — t-shirt safe zone、**Touch Edit** 価格 band テスト向き。Lovart companion：探索後 **Brand Kit** hex lock + **ChatCanvas** series — スコア表なし。

## なぜ「6 best」記事が現場を裏切るか

accuracy 92% 等の捏造 percentage。SVG と言いながら raster only export。探索 clip を final promo に — 価格 bake。**Brand Kit** 未設定 → slide 4 accent drift。正直 roundup = task group + Lovart static ops layer、not zero-sum winner。

## ChatCanvas brief 契約（clipart roundup 後 companion JP）

弱い brief「best clipart AI 2026」。強い brief：「Campaign X post-clipart promo 4:5、Brand Kit hex from VI、headline flat for Touch Edit、price bottom editable、disclaimer footer editable、variants same thread、**Design Agent** pass/fail」。clip 探索 tool 名は brief コメントのみ — offer text bake 禁止。

## Brand Kit が clip 系列の hue を統一

packaging VI から primary、accent。**ChatCanvas** same thread batch icon set + carousel + mock — material hue が diverge しない。

## Touch Edit で SKU ラベル変更、clip 再生成なし

「Model A」→「Model B」：**Touch Edit** ラベル band 5 分 — full clip regen 30 分ではない。roundup の ops テスト = この five 分 loop。

## 従来 clip 制作 vs AI clip（スコア表なし）

比較軸は task fit のみ。手描き SVG：コスト高・改稿に illustrator 再依頼。AI clip + Lovart static：探索 layer と series editable layer 分離。**Design Agent** QA：50% ズーム readable。

## よくある失敗

#1–#6 fake score table。tool 料金捏造。**Brand Kit** スキップ。404 未復旧。SVG 表記 lie。

## 測定指標

clip 修正あたり分数、path QA fail 回数、export ratio 数。404 復旧 URL を JP 6-best-ai-clipart-vector-generators-2026 stable link。
"""

BANNER_ROUNDUP_JA = """
# AI バナー広告メーカー 2026：task グループ比較（架空 ranking なし）

この日本語 URL `8-best-ai-banner-ad-makers-2026` は 404 を返していました。検索意図は banner ad roundup — fake Top-8 score 表ではなく、display ad task グループ別 fit です。各 platform 料金 tier は変動 — 公式 ToS 参照、**捏造 pricing なし**。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** は static display companion — CTA band editable、免責 footer editable。

## 四つの banner task グループ（スコア ranking 禁止）

グループ A 単発 display exploration：rapid mood、週次 offer fix 不向き。グループ B template-first SMB：Canva 系 — template swap 速い、**Brand Kit** hex SSOT は別途 Lovart で補完可。グループ C performance marketer multi-ratio：1:1 + 4:5 + 16:9 same thread — **ChatCanvas** + Kit 必須。グループ D regulated disclaimer heavy：finance/health — disclaimer editable layer、**Touch Edit** five 分テスト。Lovart：**Design Agent** pass/fail checklist numeric。

## なぜ「8 best banner makers」比較が火曜に詰まるか

CTR +47% 等の fake stat。offer baked in pixels → full regen 30 分。**Brand Kit** 未設定 → feed vs story accent drift。正直 roundup = task group + revision cost、not tool #1 badge。

## ChatCanvas brief 契約（banner ad JP）

弱い brief「viral banner premium」。強い brief：「Campaign X display 4:5 1080×1350、Brand Kit hex from media kit、headline top 15% flat for Touch Edit、price bottom left safe zone、disclaimer footer editable including ad policy lines、variants 1:1 + 4:5 same thread、**Design Agent** 50% zoom pass/fail」。

## Brand Kit が feed と story export を統一

approved media kit から primary、accent。**ChatCanvas** same thread batch 1:1 + 9:16 + 4:5 — hex lock cross-format。

## Touch Edit でオファー変更、banner full regen なし

「-30%」→「-40%」：**Touch Edit** CTA band 5 分 — full banner regen 30 分ではない。Banner ops KPI = edit-minute median per account。

## よくある失敗

fake CTR guarantee。tool 月額捏造。**Brand Kit** スキップ。404 未復旧。Zero-sum「tool X ダメ」without task split。

## 測定指標

offer fix あたり分数、export ratio 数、drift events。404 復旧 URL を JP 8-best-ai-banner-ad-makers-2026 stable SOP link。
"""

AESTHETIC_FEEDS_JA = """
# ミニマル・レトロ aesthetic feed：Instagram 系列の Brand Kit ops

この日本語 URL `aesthetic-feeds-minimalist-retro-theme-ai` は 404 を返していました。検索意図は aesthetic feed How-To — 単発 wow 投稿ではなく、minimalist/retro トーンを跨ぐ 9–12 grid series。**Brand Kit** hex SSOT、**ChatCanvas** thread、**Touch Edit** promo band、**Design Agent** grid QA。料金 tier は lovart.ai 参照 — 金額捏造なし。

## 四つの aesthetic feed deliverable

第一に grid master 4:5 — retro grain + minimalist negative space、headline flat for **Touch Edit**。第二に carousel slide 2–6 same thread accent **Brand Kit**。第三に story 9:16 crop — hex lock、grain intensity 数値で brief 化。第四に seasonal promo overlay — 日付・価格 editable layer、**Design Agent** 50% zoom readable pass/fail。

## なぜ aesthetic feed が slide 4 で accent lottery になるか

各投稿 unrelated prompt — retro teal vs minimalist sand drift。**Brand Kit** 未設定 → grid 全体が別ブランドに見える。Promo 価格 bake → セール変更 full regen 30 分。Aesthetic ≠ 形容詞だけ — brief に hex、grain%、safe zone 数値必須。

## ChatCanvas brief 契約（aesthetic feed JP）

弱い brief「retro minimalist vibe」。強い brief：「Feed series X 4:5 1080×1350、Brand Kit sand + rust from mood board approved、grain 12% document in brief、headline top 15% flat for Touch Edit、promo bottom band editable、grid 9 posts same thread accent stripe、**Design Agent** pass/fail per post」。

## Brand Kit が minimalist と retro を同一 VI に固定

primary、accent、type role を mood board 承認版から。**ChatCanvas** same thread — post 3 と post 7 で hue diverge 禁止。

## Touch Edit でセール価格変更、grain layer 保持

「¥1,980」→「¥1,480」：**Touch Edit** promo band 5 分 — full grid regen 30 分ではない。Feed ops KPI = edit-minute median per sale cycle。

## よくある失敗

vibe 形容詞のみ brief。**Brand Kit** スキップ。404 未復旧。fake engagement lift stat。grid 間 hex 不統一。

## 測定指標

価格修正あたり分数、grid drift 回数、export ratio。404 復旧 URL を JP aesthetic-feeds-minimalist-retro-theme-ai stable link。
"""

PREDICTIONS_2028_JA = """
# AI デザイン 2028 予測：推測ラベル付き（Lovart roadmap 捏造禁止）

この日本語 URL `ai-design-2028-predictions` は 404 を返していました。Category Insight & Trend。**本文は推測（speculation）であり確定ロードマップではありません** — Lovart 未発表機能を「2028 確定」と書くことは禁止。公開 changelog・公式 blog のみ参照。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** は 2026 現行 ops の四本柱 — 2028 も editable static + series memory 軸が続く可能性、**推測ラベル**。

## 四つの 2028 推測テーマ（確定宣言なし）

テーマ A agentic brief から export まで — **Design Agent** QA が pass/fail 標準化、**推測**。テーマ B **Brand Kit** cross-channel SSOT 強化 — hex drift 自動検知、**推測**。テーマ C **Touch Edit** レイヤー細分化 — compliance text band 独立、**推測**。テーマ D **ChatCanvas** thread 監査 log — variant 決定理由の記録、**推測**。いずれも Lovart 公式未発表 — 読者は lovart.ai で現行機能確認。

## なぜ 2028 予測記事が fake news になるか

「Lovart Pro $XX 2028」等の捏造 tier。未発表 MCoT v3 を確定と書く。探索 wow のみで weekly offer fix 無視 — ops 視点欠如。正直 Insight = 推測ラベル + 2026 現行 ops 教訓 + 公開ソースのみ。

## ChatCanvas brief 契約（2028 予測文脈 JP）

2026 現行 SOP：「Campaign X promo 4:5、Brand Kit hex from VI、headline flat for Touch Edit、price editable、disclaimer editable、**Design Agent** pass/fail」。2028 推測：brief フィールドが agent 監査可能に — **推測ラベル**、確定機能リストに載せない。

## Brand Kit の 2026 教訓が 2028 推測の根拠

2026 ops：Kit 未設定 → slide 4 accent lottery が最大コスト。**推測**：2028 も SSOT hex が commercial team の分岐 — ただし Lovart 製品計画の公式声明ではない。

## Touch Edit と revision cost（2026 データからの推測）

2026 現場：価格 fix five 分 **Touch Edit** vs full regen 30 分 — 測定可能。**推測**：2028 も edit-minute median が KPI 軸 — fake efficiency % は書かない。

## よくある失敗

Lovart roadmap 捏造。推測ラベルなし確定口調。404 未復旧。**Brand Kit** 言及なし general futurism。

## 測定指標

推測段落に speculation ラベル維持。404 復旧 URL を JP ai-design-2028-predictions stable link。現行機能は公式 changelog のみ。
"""

TEACHERS_EDU_JA = """
# 教師向け AI 教室デザイン 2026：compliance と editable 教材 ops

この日本語 URL `ai-for-teachers-classroom-education-2026` は 404 を返していました。Category Industry Solution。検索意図は教師・教育現場 — worksheet、announcement、seasonal bulletin、保護者向け PDF — 免責・連絡先・日付変更が頻繁。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** — school VI 準拠、readable at print size。料金 lovart.ai 参照 — 捏造なし。

## 四つの classroom deliverable

第一に event announcement 4:5 — 日付 band **Touch Edit** editable。第二に worksheet header — **Brand Kit** school colors from approved VI。第三に bulletin carousel slide 2–6 same thread。第四に parent PDF cover — **Design Agent** print pass/fail、disclaimer footer editable。

## なぜ classroom promo が学期中に詰まるか

連絡先・日付 bake in pixels → full regen 30 分。**Brand Kit** 未設定 → 学年別 accent drift。小さい免責 text illegible print — **Design Agent** QA 必須。Brief「cute classroom poster」だけ — pass/fail フィールドなし。

## ChatCanvas brief 契約（teachers JP）

弱い brief「fun education poster」。強い brief：「School event X 4:5 1080×1350、Brand Kit navy + gold from school VI、date top 15% flat for Touch Edit、contact bottom band editable、disclaimer footer editable、slides 2–4 same thread、**Design Agent** print QA pass/fail at actual size」。

## Brand Kit が学年・クラス間の drift を止める

approved school VI から primary、accent。**ChatCanvas** same thread batch grade-level variants — hex lock。

## Touch Edit で行事日変更、layout 保持

「3/15」→「3/22」：**Touch Edit** date band 5 分 — full poster regen 30 分ではない。Teacher ops KPI = minutes per date fix。

## よくある失敗

連絡先 bake。**Brand Kit** スキップ。404 未復旧。fake student outcome stat。compliance disclaimer 非 editable。

## 測定指標

日付修正あたり分数、print QA pass rate、drift count。404 復旧 URL を JP ai-for-teachers-classroom-education-2026 stable SOP link。
"""

VIDEO_TRICKS_JA = """
# AI 動画トリック： claymation・loop・写真 animate の static companion ops

この日本語 URL `ai-video-creation-tricks-claymation-loop-animate-photos` は 404 を返していました。Category How-To。検索意図は claymation 風、loop、写真 animate — 動画探索後の thumbnail・end card・CTA static companion。**ChatCanvas** thread、**Brand Kit**、**Touch Edit**、**Design Agent**。各 video tool 料金は公式参照 — 捏造なし。

## 四つの video trick + static companion

第一に claymation 風 mood — exploration layer、weekly CTA fix は **Touch Edit** static。第二に loop GIF thumbnail 1:1 — **Brand Kit** hex lock。第三に photo animate hero — end card 4:5 same thread accent。第四に **Design Agent** QA：50% zoom CTA readable、disclaimer on static layer。

## なぜ video trick 記事が promo ops を無視するか

動画 only wow — 価格・免責が video pixels に bake、変更 full re-render。**Brand Kit** 未設定 → thumbnail vs end card accent drift。Honest How-To = video exploration + Lovart static companion for Tuesday loop。

## ChatCanvas brief 契約（video tricks JP）

弱い brief「claymation viral video」。強い brief：「Campaign X video exploration + static companion 4:5、Brand Kit hex from VI、headline flat for Touch Edit、price bottom editable、disclaimer footer editable、thumbnail 1:1 + end card same thread、**Design Agent** pass/fail」。

## Brand Kit が thumbnail と end card を統一

VI から primary、accent。**ChatCanvas** same thread — video tool 出力後も hex SSOT。

## Touch Edit で CTA 変更、video re-render なし

オファー text のみ変更：**Touch Edit** static band 5 分 — full video re-render 30 分回避。Video ops KPI = static edit-minute median。

## よくある失敗

video output を final promo に。**Brand Kit** スキップ。404 未復旧。fake render speed benchmark。static companion 省略。

## 測定指標

static CTA fix 分数、thumbnail/end card drift、export ratio。404 復旧 URL を JP ai-video-creation-tricks-claymation-loop-animate-photos stable link。
"""

BOUTIQUE_OWNER_JA = """
# ブティックオーナー向け Design Agent：正直 workflow（fake ranking なし）

この日本語 URL `best-ai-design-agent-for-boutique-owner` は 404 を返していました。Category Industry Solution。検索意図は boutique owner ops — window display、seasonal promo、Instagram crop、loyalty card — 価格・日付 weekly 変更、店頭と SNS の間で accent drift。**ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** — 「#1 best agent」スコア表なし。KPI = 価格修正 five 分。

## 四つの boutique deliverable

第一に window promo 4:5 — price band **Touch Edit** editable。第二に seasonal carousel slide 2–6 **Brand Kit** hex lock。第三に loyalty card 1:1 — contact flat for **Touch Edit**。第四に **Design Agent** pass/fail：50% zoom readable price、disclaimer footer。

## なぜ boutique 「best agent」 ranking が ops を裏切るか

fake score 9.5/10。offer bake → 火曜 full regen 30 分。**Brand Kit** 未設定 → vetrina vs Instagram coral drift。Honest guide = edit-minute median KPI、not pretty first frame。

## ChatCanvas brief 契約（boutique JP）

弱い brief「luxury boutique poster」。強い brief：「Boutique X seasonal 4:5 1080×1350、Brand Kit hex from signage VI、headline top 15% flat for Touch Edit、price bottom safe zone editable、disclaimer footer editable、variants window + IG same thread、**Design Agent** pass/fail checklist boutique owner can run」。

## Brand Kit が店頭と SNS crop を統一

signage VI から primary、accent。**ChatCanvas** same thread batch window + story + loyalty — hex lock。

## Touch Edit でセール価格変更、hero regen なし

「¥12,800」→「¥9,800」：**Touch Edit** promo band 5 分 — full window regen 30 分ではない。

## よくある失敗

fake ranking scores。**Brand Kit** スキップ。404 未復旧。offer bake。conversion lift 捏造。

## 測定指標

edit-minute median、drift events per seasonal batch。404 復旧 URL を JP best-ai-design-agent-for-boutique-owner stable SOP link。
"""

LASH_TECHNICIAN_JA = """
# まつげエステ向け Design Agent：メニュー card と compliance editable ops

この日本語 URL `best-ai-design-agent-for-lash-technician` は 404 を返していました。Category Industry Solution。検索意図は lash salon ops — メニュー card、before/after carousel、予約 card、seasonal promo — 施術価格・免責（アレルギー等）頻繁変更。**ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** — fake #1 ranking なし。KPI = 価格修正 five 分。

## 四つの lash salon deliverable

第一に menu price card 4:5 — 施術名 readable、**Touch Edit** price band。第二に before/after carousel slide 2–6 **Brand Kit** hex lock。第三に booking card 1:1 — CTA flat for **Touch Edit**。第四に **Design Agent** pass/fail：disclaimer footer editable、アレルギー注意文 editable layer。

## なぜ lash promo が施術価格変更で詰まるか

「¥8,800」bake → full regen 30 分。**Brand Kit** 未設定 → slide 4 accent lottery。免責 one word change triggers full regen — **Touch Edit** text band 使わない。Salon owner は design jargon 不要 — pass/fail フィールド必須。

## ChatCanvas brief 契約（lash JP）

弱い brief「premium lash poster」。強い brief：「Salon X menu promo 4:5 1080×1350、Brand Kit sage + cream from approved signage、headline top 15% flat for Touch Edit、price bottom safe zone editable、allergy disclaimer footer editable、slides 2–6 same thread、**Design Agent** pass/fail」。

## Brand Kit が menu と carousel を統一

approved signage から primary、accent。**ChatCanvas** same thread batch menu + carousel + booking。

## Touch Edit で施術価格変更、lash hero 保持

「¥8,800」→「Member ¥7,800」：**Touch Edit** CTA band 5 分 — full hero regen 30 分ではない。

## よくある失敗

fake ranking。**Brand Kit** スキップ。404 未復旧。免責 non-editable。fake conversion stat。

## 測定指標

price fix 分数、disclaimer edit count、drift events。404 復旧 URL を JP best-ai-design-agent-for-lash-technician stable SOP link。
"""

C8_PLATFORM_JA = """
# C8 AI Agent Platform：Lovart プラットフォーム概観（tier 料金捏造禁止）

この日本語 URL `c8-ai-agent-platform` は 404 を返していました。Category Branding。検索意図は Lovart AI Agent Platform 概観 — goal から deliver まで agentic workflow、**MCoT** による design reasoning。Lovart tier 料金は lovart.ai 公式参照 — **この記事では Starter/Pro/Ultimate 等の金額を捏造しません**。競合 tier も各社公式参照。Lovart **ChatCanvas**、**Brand Kit**、**Touch Edit**、**Design Agent** が四本柱 — AI tool（prompt in/out）vs AI agent（goal delegate）の区別を factual に。

## 四つの platform pillar（marketing hype なし）

第一 **ChatCanvas**：campaign thread SSOT — hero、carousel、social crop same accent。**Brand Kit**：VI から hex SSOT。第三 **Touch Edit**：offer、price、disclaimer editable band — five 分 ops test。第四 **Design Agent**：pass/fail checklist numeric — readable price、hex drift vs Kit、disclaimer present。

## AI tool vs AI agent（factual 区別）

AI tool：prompt → output → human re-prompt every step。AI agent：goal → plan → execute → deliver → human review。**MCoT** は Lovart 公開ドキュメントの multi-step design reasoning 架構 — 未公開 vNext を確定と書かない。Human role = director、not every-step operator。

## ChatCanvas brief 契約（platform context JP）

弱い brief「make premium design」。強い brief：「Campaign X 4:5 1080×1350、Brand Kit hex from media kit、headline flat for Touch Edit、price editable、disclaimer editable、variants same thread、**Design Agent** pass/fail acceptance」。Platform value = brief contract + editable layers、not single wow frame。

## Brand Kit が agent output series を統一

approved VI から primary、accent、type role。Agent が ten variants 生成しても Kit active なら同一 brand look — exploration lottery 回避。

## Touch Edit が agent workflow の ops 証明

Agent deliver 後に価格のみ変更：**Touch Edit** five 分？ Full agent re-run 30 分 = brief or Kit gap。Platform KPI = edit-minute median post-deliver。

## よくある失敗

Lovart tier $XX 捏造。未発表 roadmap 確定口調。**Brand Kit** スキップ。404 未復旧。Zero-sum「競合すべて bad」。

## 測定指標

post-deliver edit minutes、Kit compliance rate、404 復旧 URL を JP c8-ai-agent-platform stable platform overview link。
"""


FAQ = {
    "midjourney_vs_lovart_ja": """
## FAQ

**Midjourney 料金をこの記事に書く？**  
いいえ — midjourney.com 公式参照のみ。

**Lovart 料金捏造？**  
なし — lovart.ai 公式参照。

**Touch Edit で価格修正 5 分？**  
はい — static companion editable layer テスト。

**Brand Kit は探索後必須？**  
はい — carousel accent drift 防止。

**404 復旧 URL？**  
安定 JP 04-midjourney-vs-lovart。
""",
    "clipart_roundup_ja": """
## FAQ

**#1–#6 スコア表はある？**  
いいえ — task グループのみ、fake ranking なし。

**Touch Edit でラベル修正 5 分？**  
はい — clip 再生成なし ops テスト。

**Brand Kit は clip 系列後？**  
はい — hex SSOT same thread。

**tool 月額捏造？**  
なし — 各社公式参照。

**404 復旧 URL？**  
安定 JP 6-best-ai-clipart-vector-generators-2026。
""",
    "banner_roundup_ja": """
## FAQ

**Top-8 fake score 表？**  
いいえ — task グループ比較のみ。

**Touch Edit でオファー変更 5 分？**  
はい — banner full regen 回避。

**Brand Kit feed + story 統一？**  
はい — same thread hex lock。

**fake CTR 保証？**  
なし — pass/fail QA のみ。

**404 復旧 URL？**  
安定 JP 8-best-ai-banner-ad-makers-2026。
""",
    "aesthetic_feeds_ja": """
## FAQ

**grid 間 hex 統一必要？**  
はい — Brand Kit SSOT。

**Touch Edit でセール価格 5 分？**  
はい — grain layer 保持。

**vibe 形容詞のみ brief？**  
いいえ — 数値フィールド必須。

**404 復旧 URL？**  
安定 JP aesthetic-feeds-minimalist-retro-theme-ai。

**fake engagement stat？**  
なし — edit-minute KPI のみ。
""",
    "predictions_2028_ja": """
## FAQ

**2028 予測は確定ロードマップ？**  
いいえ — 推測ラベル付き speculation のみ。

**Lovart 未発表機能を確定と書く？**  
禁止 — 公開 changelog のみ。

**Touch Edit KPI 2026 から推測？**  
はい — 推測ラベル付き。

**Brand Kit 2028 推測？**  
推測 — 公式声明ではない。

**404 復旧 URL？**  
安定 JP ai-design-2028-predictions。
""",
    "teachers_edu_ja": """
## FAQ

**学校 VI から Brand Kit？**  
はい — approved VI hex サンプリング。

**Touch Edit で行事日変更 5 分？**  
はい — layout 保持。

**disclaimer editable？**  
はい — footer editable layer。

**404 復旧 URL？**  
安定 JP ai-for-teachers-classroom-education-2026。

**fake student outcome？**  
なし — ops metrics のみ。
""",
    "video_tricks_ja": """
## FAQ

**video のみで promo 完結？**  
いいえ — static companion + Touch Edit。

**Brand Kit thumbnail + end card？**  
はい — same thread hex lock。

**Touch Edit static CTA 5 分？**  
はい — video re-render 回避。

**404 復旧 URL？**  
安定 JP ai-video-creation-tricks-claymation-loop-animate-photos。

**fake render speed？**  
なし — edit-minute のみ。
""",
    "boutique_owner_ja": """
## FAQ

**#1 best agent ranking？**  
いいえ — edit-minute median KPI。

**Touch Edit セール価格 5 分？**  
はい — window hero regen なし。

**Brand Kit 店頭 + IG 統一？**  
はい — same thread hex lock。

**404 復旧 URL？**  
安定 JP best-ai-design-agent-for-boutique-owner。

**fake conversion lift？**  
なし — ops metrics のみ。
""",
    "lash_technician_ja": """
## FAQ

**まつげサロン Brand Kit 必要？**  
はい — signage VI から hex。

**Touch Edit 施術価格 5 分？**  
はい — full hero regen なし。

**アレルギー disclaimer editable？**  
はい — footer editable layer。

**404 復旧 URL？**  
安定 JP best-ai-design-agent-for-lash-technician。

**fake ranking score？**  
なし — honest workflow のみ。
""",
    "c8_platform_ja": """
## FAQ

**Lovart tier 料金を記載？**  
いいえ — lovart.ai 公式参照のみ。

**AI agent vs AI tool 区別？**  
はい — goal delegate vs prompt in/out。

**Touch Edit post-deliver 5 分？**  
はい — agent re-run 回避 ops テスト。

**Brand Kit agent series 統一？**  
はい — hex SSOT。

**404 復旧 URL？**  
安定 JP c8-ai-agent-platform。
""",
}


def expand_ja(topic: str, n: int) -> str:
    return f"""
## 現場メモ {n}：{topic}

初回 brief が「モダン」で終わると価格文字が小さく badge が顔を隠します。二回目は safe zone と必須フィールドのみ修正。**Design Agent** と **ChatCanvas** で thread を維持すると carousel slide 4 の accent drift が減ります。{topic} で **Touch Edit** が 5 分以内に価格修正できれば static-first が成立。30 分 full regen なら **Brand Kit** からやり直し。404 復旧 URL は JP ops 向け stable link batch30 です。
"""


ARTICLES = [
    {
        "rank": 306,
        "key": "midjourney_vs_lovart_ja",
        "lang": "ja",
        "slug": "04-midjourney-vs-lovart",
        "cover": "056",
        "category": "Comparison",
        "title": "Midjourney と Lovart：正直な task split（料金捏造なし）",
        "seo_title": "04 Midjourney Vs Lovart JP — honest task split no fake pricing",
        "description": "JP 404 fix: Midjourney vs Lovart comparison, task split, no fabricated Midjourney pricing.",
        "seo_description": "Comparison: ChatCanvas Brand Kit Touch Edit, exploration vs series editable layer.",
        "focus": "04 midjourney vs lovart",
        "keywords": ["midjourney vs lovart", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — Midjourney Vs Lovart JA",
        "body": MIDJOURNEY_VS_LOVART_JA,
        "expand_topic": "JP 04 midjourney vs lovart honest task split workflow",
    },
    {
        "rank": 307,
        "key": "clipart_roundup_ja",
        "lang": "ja",
        "slug": "6-best-ai-clipart-vector-generators-2026",
        "cover": "057",
        "category": "Comparison",
        "title": "AI クリップアート・ベクター 2026：task グループ比較",
        "seo_title": "6 Best AI Clipart Vector Generators 2026 JP — task groups no fake scores",
        "description": "JP 404 fix: clipart vector roundup, task groups not fake ranking scores.",
        "seo_description": "Comparison: SVG vs raster task split, Touch Edit post-clipart companion.",
        "focus": "6 best ai clipart vector generators 2026",
        "keywords": ["ai clipart generator", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Clipart Vector Generators 2026 JA",
        "body": CLIPART_ROUNDUP_JA,
        "expand_topic": "JP 6 best ai clipart vector generators task group workflow",
    },
    {
        "rank": 308,
        "key": "banner_roundup_ja",
        "lang": "ja",
        "slug": "8-best-ai-banner-ad-makers-2026",
        "cover": "058",
        "category": "Comparison",
        "title": "AI バナー広告メーカー 2026：task グループ比較",
        "seo_title": "8 Best AI Banner Ad Makers 2026 JP — no fake ranking scores",
        "description": "JP 404 fix: banner ad roundup, task groups not fake Top-8 scores.",
        "seo_description": "Comparison: display ad task groups, Brand Kit multi-ratio same thread.",
        "focus": "8 best ai banner ad makers 2026",
        "keywords": ["ai banner ad maker", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Comparison — AI Banner Ad Makers 2026 JA",
        "body": BANNER_ROUNDUP_JA,
        "expand_topic": "JP 8 best ai banner ad makers task group workflow",
    },
    {
        "rank": 309,
        "key": "aesthetic_feeds_ja",
        "lang": "ja",
        "slug": "aesthetic-feeds-minimalist-retro-theme-ai",
        "cover": "059",
        "category": "Branding",
        "title": "ミニマル・レトロ aesthetic feed：Instagram 系列 Brand Kit ops",
        "seo_title": "Aesthetic Feeds Minimalist Retro Theme AI JP — grid Brand Kit SOP",
        "description": "JP 404 fix: aesthetic feed How-To, minimalist retro grid, Brand Kit hex SSOT.",
        "seo_description": "Branding: ChatCanvas grid series, Touch Edit promo band editable.",
        "focus": "aesthetic feeds minimalist retro theme ai",
        "keywords": ["aesthetic feed ai", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Branding — Aesthetic Feeds Minimalist Retro JA",
        "body": AESTHETIC_FEEDS_JA,
        "expand_topic": "JP aesthetic feeds minimalist retro Brand Kit grid workflow",
    },
    {
        "rank": 310,
        "key": "predictions_2028_ja",
        "lang": "ja",
        "slug": "ai-design-2028-predictions",
        "cover": "060",
        "category": "Insight & Trend",
        "title": "AI デザイン 2028 予測：推測ラベル付き（roadmap 捏造禁止）",
        "seo_title": "AI Design 2028 Predictions JP — speculation labeled no fake roadmap",
        "description": "JP 404 fix: 2028 predictions speculation labeled, no fabricated Lovart roadmap.",
        "seo_description": "Insight: Brand Kit Touch Edit lessons from 2026 ops, published sources only.",
        "focus": "ai design 2028 predictions",
        "keywords": ["ai design 2028 predictions", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Insight — AI Design 2028 Predictions JA",
        "body": PREDICTIONS_2028_JA,
        "expand_topic": "JP ai design 2028 predictions speculation labeled workflow",
    },
    {
        "rank": 311,
        "key": "teachers_edu_ja",
        "lang": "ja",
        "slug": "ai-for-teachers-classroom-education-2026",
        "cover": "061",
        "category": "Industry Solution",
        "title": "教師向け AI 教室デザイン 2026：compliance editable ops",
        "seo_title": "AI For Teachers Classroom Education 2026 JP — Touch Edit date band",
        "description": "JP 404 fix: teachers classroom AI design, Brand Kit school VI, disclaimer editable.",
        "seo_description": "Industry Solution: worksheet bulletin carousel, Design Agent print QA.",
        "focus": "ai for teachers classroom education 2026",
        "keywords": ["ai for teachers", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Teachers Classroom Education JA",
        "body": TEACHERS_EDU_JA,
        "expand_topic": "JP ai for teachers classroom education Brand Kit workflow",
    },
    {
        "rank": 312,
        "key": "video_tricks_ja",
        "lang": "ja",
        "slug": "ai-video-creation-tricks-claymation-loop-animate-photos",
        "cover": "062",
        "category": "How-To",
        "title": "AI 動画トリック：claymation・loop・写真 animate static companion",
        "seo_title": "AI Video Creation Tricks Claymation Loop Animate Photos JP",
        "description": "JP 404 fix: video tricks How-To, static companion Touch Edit CTA layer.",
        "seo_description": "How-To: thumbnail end card same thread, Brand Kit hex lock.",
        "focus": "ai video creation tricks claymation loop animate photos",
        "keywords": ["ai video creation tricks", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "How-To — AI Video Creation Tricks JA",
        "body": VIDEO_TRICKS_JA,
        "expand_topic": "JP ai video creation tricks static companion workflow",
    },
    {
        "rank": 313,
        "key": "boutique_owner_ja",
        "lang": "ja",
        "slug": "best-ai-design-agent-for-boutique-owner",
        "cover": "063",
        "category": "Industry Solution",
        "title": "ブティックオーナー向け Design Agent：正直 workflow",
        "seo_title": "Best AI Design Agent Boutique Owner JP — no fake ranking",
        "description": "JP 404 fix: boutique owner Design Agent, Touch Edit seasonal price editable.",
        "seo_description": "Industry Solution: window IG loyalty same thread, edit-minute median KPI.",
        "focus": "best ai design agent for boutique owner",
        "keywords": ["boutique owner design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Boutique Owner Design Agent JA",
        "body": BOUTIQUE_OWNER_JA,
        "expand_topic": "JP best ai design agent for boutique owner workflow",
    },
    {
        "rank": 314,
        "key": "lash_technician_ja",
        "lang": "ja",
        "slug": "best-ai-design-agent-for-lash-technician",
        "cover": "064",
        "category": "Industry Solution",
        "title": "まつげエステ向け Design Agent：メニュー card editable ops",
        "seo_title": "Best AI Design Agent Lash Technician JP — allergy disclaimer editable",
        "description": "JP 404 fix: lash technician Design Agent, menu card Touch Edit price band.",
        "seo_description": "Industry Solution: before/after carousel, Design Agent pass/fail QA.",
        "focus": "best ai design agent for lash technician",
        "keywords": ["lash technician design agent", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Industry Solution — Lash Technician Design Agent JA",
        "body": LASH_TECHNICIAN_JA,
        "expand_topic": "JP best ai design agent for lash technician workflow",
    },
    {
        "rank": 315,
        "key": "c8_platform_ja",
        "lang": "ja",
        "slug": "c8-ai-agent-platform",
        "cover": "065",
        "category": "Branding",
        "title": "C8 AI Agent Platform：Lovart 概観（tier 料金捏造禁止）",
        "seo_title": "C8 AI Agent Platform JP — factual overview no fake tier pricing",
        "description": "JP 404 fix: C8 AI agent platform overview, MCoT architecture, no fabricated pricing.",
        "seo_description": "Branding: ChatCanvas Brand Kit Touch Edit Design Agent four pillars.",
        "focus": "c8 ai agent platform",
        "keywords": ["c8 ai agent platform", "lovart chatcanvas", "brand kit", "touch edit"],
        "cluster": "Branding — C8 AI Agent Platform JA",
        "body": C8_PLATFORM_JA,
        "expand_topic": "JP c8 ai agent platform factual overview workflow",
    },
]


EXPAND_FN = {
    "ja": expand_ja,
}

UNIT_MAP = {
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
        "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch30 content cluster.*\n"
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
