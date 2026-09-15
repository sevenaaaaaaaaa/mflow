# Lovart 品牌词布局清单（还原自 lovart_brand_match.py SSOT）

> 来源：`/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/1-4 Dev/scripts/lovart_brand_match.py` · 每个候选词均经 `is_brand()` 实测验证 · 生成时间按需

## 一、品牌词全量清单（需要布局）

| 组 | 覆盖规则 | 品牌词（is_brand=True） | 验证 |
|---|---|---|---|
| A. 核心词族（canonical） | 规则 1-3：\blovart\b / \bloveart\b / \blovert\b + \blevert\b | lovart, loveart, lovert, levert, lovart.ai, lovartai, lovart ai | ✅ |
| B. 近拼写变体（单字符差/OCR 键盘误触） | 规则 19-51：lov[a-z0-9]*art* / lav* / luv* / 数字替换 | lovartia, lavorat, louvat, lavrt, l9vart, lorvat, lavort, lavart, lavard, lawat, lova, lovar, lovat, lovurt, lavrat, lvart, lavort, lav0rt, lavartai, lavartpro, lavardai, lavorat, louvar, louvard, luvart, luvat, livart, lowart, lavert, lavrt, volart, levart, loart, lovert | ✅ |
| C. 分词/空格变体（两 token 组合） | 规则 13-31 + _multi_token_brand pairs | lo art, lo ai, lo ia, lov art, lov ai, lov ia, love art, love ai, love ia, luv art, art love, art lov, art ai, art ia, ia art, levert ai, lovert ai, lavard ai, lawat ai, lovart ai, lovart ia, l o v a r t, l o v e a r t | ✅ |
| D. 组合品牌词（复合/产品名） | 规则 61-67 + roots：artlov / iloveart / nano banana 等 | artlov, artlove, iloveart, nano banana, nanobanana, chatcanvas, mcot, brand kit lovart, brandkit lovart | ✅ |
| E. 音译词（非拉丁字母市场） | 规则 55-60 + _TRANSLIT_FRAGMENTS（JA/KO/ZH/RU/AR） | ラブアート, ロバート, ラバート, らぶあーと, らばーと, らぶあー, ロバートai, ラバートai, 로바트, 로버트, 洛瓦特, 咯var, 咯var他, ловарт, лаварт, лов арт, لوفارت, لافارت, لووارت, لوآرت, لافرت, لافورت, لافارت | ✅ |
| F. 模糊匹配层（Levenshtein ≤ 2 于锚点） | _compact_form_brand / _fuzzy_lovart_token 的 levenshtein 分支 | lovort, lovars, lovartt, lovarts, lovarty, lovardi, lovartly, lovarta, loveartt, lovertz, lovartpro, lavorta, lavarti, louvat, luvart, luvarti, luvartai | ✅ |
| G. 品牌词根独立出现（短词） | _BRAND_ROOTS + _SHORT_ROOTS（与 art/ai/ia 组合或整句极短时） | lo, lov, love, lover, luv, lav, louv, lavort, lavart, lavard, lawat, lavrt, lavorat, louvat, lorvat, lovart, loveart, lovartai, lovar, lovat, lova, louart, lovurt, lavrat, lvart, l9vart, artlov, iloveart, volart, levart, levert, lovert, lova, lovu, luvi | ✅ |

## 二、非品牌排除词（不要布局）

以下词命中模糊规则但被 deny list 排除，`is_brand()` 返回 False，禁止作为品牌词布局：

- 正确排除（is_brand=False）：logo, logos, login, local, logic, load, loan, lock, loop, lose, lost, lone, lobe, logs, loid, lofi, lore, logo ai, local ai, art, ai art
- ⚠️ 反例（is_brand=True，需注意）：love, love ai

## 三、开放通配规则（无法穷举，按需布局）

| 规则 | 含义 | 布局建议 |
|---|---|---|
| `lov[a-z0-9]*art[a-z0-9]*` | lov…art 任意中缀/后缀 | 品牌词根 + 业务词缀：lovartai / lovartpro / lovartapp |
| `l[o0uv][vaeiou]*r?t`（4-10 字符） | 元音簇替换 | lovt / lovat / lovet / luvat / luvert |
| `lov[a-z0-9]*ard` | lov…ard | lovard / lovartd / lovars |
| `artlov[a-z]*` | art+lov 复合 | artlov / artlove / artlover |
| `lovart[\u4e00-\u9fff]+` | lovart+中文 | lovart中文工具 / lovart官网（中文布局） |

## 四、布局建议（按组落地）

- **A/B/D 组**：页面标题、H1、导航锚文本、站内链（必须优先覆盖 canonical + 高频误拼）。
- **C 组**：FAQ、长尾标题（"lov art" 类拼写错误的搜索意图承接页）。
- **E 组**：对应 hreflang 市场页面（ja/ko/zh/ru/ar），音译词放 title/alt。
- **F 组**：404 页、SERP 兜底、错误页（用户输错时也能命中品牌）。
- **二、非品牌词**：绝不布局；它们属于通用词，避免与品牌混淆。
