# Card Title → Image 关键词映射规则（2026-06-24 更新）

> **43 张已验证图片 + 7 分类关键词映射**。落地页生成/批量替换/Blog 注入时按此规则自动选图。
> 完整 URL 列表见 [`verified-image-pool-2026-06.md`](./verified-image-pool-2026-06.md)。

## 核心原则

1. **图片 URL 必须从 `image-library.md` 或 `verified-image-pool-2026-06.md` 选取**，严禁编造
2. **匹配必须用词边界正则**（`\bword\b`）—— 子串匹配会产生 false positive
3. **CJK 关键词用精确子串**（中文/日文/韩文）不需要 `\b`
4. **优先级排序**：第一个匹配的规则胜出
5. **Section 共享**：capability-tabs / bento-2/4/6 / feature-detail 共用一套关键词

## 7 分类语义映射

| 分类 | 数量 | 用途关键词 |
|------|------|-----------|
| 🎬 video | 14 | storyboard / Seedance / Veo / Kling / motion / keyframe / camera / video / 動画 / 동영상 / 影片 |
| 👤 avatar | 7 | avatar / character / presenter / virtual actor / アバター / 캐릭터 / 角色 / 化身 |
| 🖼️ image_gen | 8 | image generator / text-to-image / Flux / anime / nano banana / illustration / 画像生成 / 图像生成 |
| 🎨 design | 6 | design agent / creative / sales deck / earbuds / style / brand consistency |
| ✏️ edit | 4 | text edit / touch edit / typography / a/b test / copy test / background / retouch / テキスト編集 |
| 📦 ecommerce | 3 | facebook ad / product image / mockup / 商品画像 / 产品图 / 목업 |
| 🔧 generic | 1 | 通用兜底（batch / generate / chatcanvas / cloud / agent） |

## 完整关键词规则（100+ 规则，按优先级排序）

```python
import re

PATTERNS = [
    # ── Priority 10: text_edit ──
    (re.compile(r"\btext\s+edit\b", re.I), "edit"),
    (re.compile(r"\btextbearbeitung\b", re.I), "edit"),
    (re.compile(r"\ba/b\s+test\b", re.I), "edit"),
    (re.compile(r"\bcopy\s+test\b", re.I), "edit"),
    (re.compile(r"\btypography\s+excellence\b", re.I), "edit"),
    (re.compile(r"\bflawless\s+typography\b", re.I), "edit"),
    (re.compile(r"\bperfect\s+typography\b", re.I), "edit"),
    (re.compile(r"\bedit\s+elements\b", re.I), "edit"),
    (re.compile(r"\belemente\s+bearbeiten\b", re.I), "edit"),
    (re.compile(r"\bedit\s+text\b", re.I), "edit"),
    (re.compile(r"\binfographic\b", re.I), "edit"),
    ("テキスト編集", "edit"), ("文字編輯", "edit"), ("文字编辑", "edit"),
    ("텍스트 편집", "edit"), ("タイポグラフィ", "edit"), ("要素の編集", "edit"),
    ("요소 편집", "edit"), ("编辑元素", "edit"), ("文字處理", "edit"),

    # ── Priority 9: touch ──
    (re.compile(r"\btouch\s+edit\b", re.I), "edit"),
    (re.compile(r"\bzero-shot\b", re.I), "edit"),
    (re.compile(r"\bpoint-and-talk\b", re.I), "edit"),
    (re.compile(r"\bclick-to-edit\b", re.I), "edit"),
    (re.compile(r"\bsemantic\s+click\b", re.I), "edit"),
    (re.compile(r"\bsubject\s+preservation\b", re.I), "edit"),
    (re.compile(r"\bretouch\b", re.I), "edit"),
    ("タッチ編集", "edit"), ("觸控編輯", "edit"), ("터치 편집", "edit"),
    ("语义级智能重绘", "edit"), ("微调", "edit"),

    # ── Priority 8: style ──
    (re.compile(r"\bstyle\s+reference\b", re.I), "design"),
    (re.compile(r"\bstyle\s+transfer\b", re.I), "design"),
    (re.compile(r"\bstyle\s+consistency\b", re.I), "design"),
    (re.compile(r"\bbrand\s+consistency\b", re.I), "design"),
    (re.compile(r"\bconsistent\s+branding\b", re.I), "design"),
    (re.compile(r"\bkonsistentes\s+branding\b", re.I), "design"),
    (re.compile(r"\bstay\s+on-brand\b", re.I), "design"),
    (re.compile(r"\bcharacter\s+consistency\b", re.I), "design"),
    (re.compile(r"\bbrand-consistent\b", re.I), "design"),
    (re.compile(r"\bremix\b", re.I), "design"),
    ("スタイル参照", "design"), ("風格參考", "design"), ("스타일 참조", "design"),
    ("品牌一致", "design"), ("ブランド一貫性", "design"),

    # ── Priority 7: video ──
    (re.compile(r"\bstoryboard\b", re.I), "video"),
    (re.compile(r"\bseedance\b", re.I), "video"),
    (re.compile(r"\bveo\b", re.I), "video"),
    (re.compile(r"\bkling\b", re.I), "video"),
    (re.compile(r"\bimage\s+to\s+video\b", re.I), "video"),
    (re.compile(r"\bimage-to-video\b", re.I), "video"),
    (re.compile(r"\bcamera\s+control\b", re.I), "video"),
    (re.compile(r"\bvideo\s+ads\b", re.I), "video"),
    (re.compile(r"\bkeyframe\b", re.I), "video"),
    (re.compile(r"\bmotion\s+control\b", re.I), "video"),
    (re.compile(r"\bmotion\s+graphics\b", re.I), "video"),
    (re.compile(r"\bdirector-level\b", re.I), "video"),
    (re.compile(r"\bnative\s+ad\b", re.I), "video"),
    ("ストーリーボード", "video"), ("故事板", "video"), ("動画", "video"),
    ("동영상", "video"), ("影片", "video"), ("영상", "video"),
    ("テキストから動画", "video"), ("動画広告", "video"),

    # ── Priority 6: avatar ──
    (re.compile(r"\bavatar\b", re.I), "avatar"),
    (re.compile(r"\bcharacter\b", re.I), "avatar"),
    (re.compile(r"\bvirtual\s+actor\b", re.I), "avatar"),
    (re.compile(r"\bip\s+avatar\b", re.I), "avatar"),
    (re.compile(r"\bpresenter\b", re.I), "avatar"),
    ("アバター", "avatar"), ("캐릭터", "avatar"), ("角色", "avatar"), ("化身", "avatar"),

    # ── Priority 5: image_gen ──
    (re.compile(r"\bimage\s+generator\b", re.I), "image_gen"),
    (re.compile(r"\btext\s+to\s+image\b", re.I), "image_gen"),
    (re.compile(r"\btext-to-image\b", re.I), "image_gen"),
    (re.compile(r"\bai\s+art\b", re.I), "image_gen"),
    (re.compile(r"\billustration\b", re.I), "image_gen"),
    (re.compile(r"\banime\b", re.I), "image_gen"),
    (re.compile(r"\bnano\s+banana\b", re.I), "image_gen"),
    (re.compile(r"\bflux\b", re.I), "image_gen"),
    ("画像生成", "image_gen"), ("이미지 생성", "image_gen"), ("图像生成", "image_gen"),

    # ── Priority 4: ecommerce ──
    (re.compile(r"\bfacebook\s+ad\b", re.I), "ecommerce"),
    (re.compile(r"\bad\s+creator\b", re.I), "ecommerce"),
    (re.compile(r"\bproduct\s+image\b", re.I), "ecommerce"),
    (re.compile(r"\bmockup\b", re.I), "ecommerce"),
    ("商品画像", "ecommerce"), ("产品图", "ecommerce"), ("목업", "ecommerce"),

    # ── Priority 3: expand ──
    (re.compile(r"\bexpand\s*/\s*resize\b", re.I), "design"),
    (re.compile(r"\bsmart\s+resize\b", re.I), "design"),
    (re.compile(r"\bsmart\s+expand\b", re.I), "design"),
    (re.compile(r"\bmulti-.*resize\b", re.I), "design"),
    (re.compile(r"\baspect\s+ratio\b", re.I), "design"),
    (re.compile(r"\bresizing\b", re.I), "design"),
    (re.compile(r"\bexpand\b", re.I), "design"),
    (re.compile(r"\bresize\b", re.I), "design"),
    ("サイズ変更", "design"), ("智慧尺寸調整", "design"),

    # ── Priority 2: export ──
    (re.compile(r"\bupscale\s+to\s+4k\b", re.I), "edit"),
    (re.compile(r"\b4k\s+upscaling\b", re.I), "edit"),
    (re.compile(r"\bcommercial\s+rights\b", re.I), "edit"),
    (re.compile(r"\bkommerzielle\s+rechte\b", re.I), "edit"),
    (re.compile(r"\bcommercial\b", re.I), "edit"),
    (re.compile(r"\bvector\s+export\b", re.I), "edit"),
    (re.compile(r"\bvectorize\b", re.I), "edit"),
    (re.compile(r"\bprint-ready\b", re.I), "edit"),
    (re.compile(r"\bupscale\b", re.I), "edit"),
    (re.compile(r"\bexport\b", re.I), "edit"),
    ("エクスポート", "edit"), ("导出", "edit"), ("升頻", "edit"),
    ("商用権利", "edit"), ("商业权利", "edit"),

    # ── Priority 1: reference ──
    (re.compile(r"\bfrom\s+reference\b", re.I), "image_gen"),
    (re.compile(r"\breference\b", re.I), "image_gen"),
    (re.compile(r"\bmultimodal\b", re.I), "image_gen"),
    (re.compile(r"\bupload\b", re.I), "image_gen"),
    ("リファレンス", "image_gen"), ("マルチモーダル", "image_gen"),
    ("アップロード", "image_gen"), ("上传", "image_gen"),

    # ── Priority 0: brand_kit ──
    (re.compile(r"\bbrand\s+kit\b", re.I), "design"),
    (re.compile(r"\bbrandkit\b", re.I), "design"),
    (re.compile(r"\bmockups?\b", re.I), "design"),
    ("ブランドキット", "design"), ("品牌套件", "design"),

    # ── Priority 0: audience ──
    (re.compile(r"\bappetite\b", re.I), "ecommerce"),
    (re.compile(r"\bcontent-driven\b", re.I), "ecommerce"),
    (re.compile(r"\bindustry-specific\b", re.I), "ecommerce"),
    (re.compile(r"\baudience\b", re.I), "ecommerce"),
    ("食欲", "ecommerce"), ("ターゲット", "ecommerce"), ("受众", "ecommerce"),

    # ── Priority 0: generic ──
    (re.compile(r"\bunlimited\s+variations?\b", re.I), "generic"),
    (re.compile(r"\bunbegrenzte\s+variationen\b", re.I), "generic"),
    (re.compile(r"\bvariations?\b", re.I), "generic"),
    (re.compile(r"\bbatch\s+generation\b", re.I), "generic"),
    (re.compile(r"\bbatch\b", re.I), "generic"),
    (re.compile(r"\bgenerate\b", re.I), "generic"),
    (re.compile(r"\binfinite\s+chatcanvas\b", re.I), "generic"),
    (re.compile(r"\bchatcanvas\b", re.I), "generic"),
    (re.compile(r"\bremove\s+background\b", re.I), "generic"),
    (re.compile(r"\bagent\b", re.I), "generic"),
    (re.compile(r"\bcanvas\b", re.I), "generic"),
    ("バリエーション", "generic"), ("变体", "generic"), ("バッチ", "generic"),
    ("批量", "generic"), ("生成", "generic"), ("背景除去", "generic"),
]
```

## 在落地页生成中的调用流程

```python
from image_pool import POOL, match_title, get_image, assign_images_to_features

# Step 1: 给 bento-4 分配图片
bento4_features = [
    {"title": "Text Edit", "description": "..."},
    {"title": "Multi-Platform Resize", "description": "..."},
    {"title": "Commercial Rights", "description": "..."},
    {"title": "Batch Generation", "description": "..."},
]
assign_images_to_features(bento4_features)

# Step 2: 给 capability-tabs 分配图片
for tab in capability_tabs:
    tab["content"]["media"]["src"] = get_image(match_title(tab["label"]))

# Step 3: 给 feature-detail 分配图片
for item in feature_detail_items:
    item["media"]["src"] = get_image(match_title(item["title"]))
```

## 跨主题复用原则

**同一个落地页的所有 section + 所有语言版本共用同一套图片 URL**。如主题 B（AI Image Generator）使用 `c546fad234b6b0fe9b08223a9626b449...` 系列图，则该页面的：
- contentSection 图 1-3
- textImageSection 图
- threeColumnSection 图
- heroSection 图
- 10 种语言版本

**都从同一组图片池选**，不混用其他主题。

## ⚠️ 重要约束（重复强调）

1. ❌ **禁止截断 hash** — CDN 用 64 字符完整 hex，截断 12 字符 → 404
2. ✅ **必须 HTTP 200 + size > 100KB** 验证后才能使用
3. ✅ **匹配用 `\bword\b` 词边界** — 不要用 `"edit" in title.lower()` 子串匹配
4. ✅ **CJK 精确子串** — 中文/日文/韩文不需要 `\b`
5. ✅ **优先级顺序** — text_edit(10) > touch(9) > style(8) > video(7) > expand(6) > export(6) > ref(5) > brand(4) > aud(3) > gen_a(1)

## 验证清单

- [x] 16 个核心测试用例全通过
- [x] 43 张图片全部 HTTP 200
- [x] 8 语言关键词覆盖
- [x] 7 分类语义映射
- [x] 跨 5 个 section type 共享规则
