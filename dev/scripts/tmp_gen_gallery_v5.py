#!/usr/bin/env python3
"""tmp_gen_gallery_v5.py — D 模块 gallery 按真实结构重做（v5）

真实结构（来自 gallery-ledger.json 台账）：
  12 瓦 · gallery   · 行业维度 · 18 个品类 × 12 个行业 = 216 张瓦片 + 18 张 media 主图
   6 瓦 · toolTiles · 工具维度 · 4 套 × 6 = 24 张
   4 瓦 · toolTiles · 工具维度 · 1 套 × 4 = 4 张（11 语言共用同一套）

关键工艺约束：
  - 海报/菜单/简历/PPT/封面等本身含文字 → 必须用「抽象灰色条块代替字形」表达排版层级，
    绝不出现可读字符（否则生成必乱码）
  - 12 瓦必须 12 种不同机位，且每个行业有独立配色/材质/气质，避免 12 格雷同
"""
import json
from pathlib import Path

OUT = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")

# ── 12 个行业维度：配色 + 材质 + 气质 + 纹样 ──
INDUSTRIES = [
    ("商旅出行", "business-travel",
     "cool slate-blue and pale stone grey", "clean matte surfaces and soft brushed metal",
     "precise, calm, forward-motion", "subtle route lines and boarding-pass-like grid marks"),
    ("国潮插画", "chinese-chic-illustration",
     "vermilion and antique gold on warm off-white", "ink-wash texture with carved seal red",
     "traditional yet modern, ornate restraint", "cloud-scroll and lattice motifs used sparingly"),
    ("极简商务", "minimal-business",
     "a restrained mono-tone warm grey with one ink accent", "smooth uncoated paper and hairline ink",
     "quiet, exact, generous white space", "thin rules and vast margins"),
    ("食品餐饮", "food-beverage",
     "terracotta, cream and deep olive", "appetizing organic texture with crumb and steam hints",
     "warm, tactile, appetizing", "rounded organic shapes and drip marks"),
    ("科技数码", "tech-digital",
     "deep navy with electric cyan and cool white", "crisp matte composite with fine mesh grid",
     "precise, engineered, forward", "faint grid overlays and machined edges"),
    ("时尚美妆", "fashion-beauty",
     "blush nude and soft charcoal", "soft satin and pearl-sheen surfaces",
     "editorial elegance, confident poise", "elongated silhouettes and couture curves"),
    ("教育培训", "education-training",
     "friendly teal and soft sand", "clean matte card with rounded corners",
     "clear, encouraging, structured", "modular blocks and friendly rounded geometry"),
    ("医疗健康", "medical-health",
     "clean mint and clinical white", "soft-touch matte with rounded soft forms",
     "calm, trustworthy, precise", "gentle arcs and clear breathing space"),
    ("房地产", "real-estate",
     "warm stone and deep forest green", "concrete-grain texture with architectural paper",
     "structural, solid, aspirational", "architectural elevation lines and plan grids"),
    ("电商零售", "ecommerce-retail",
     "vivid coral with clean white and charcoal", "glossy print finish with crisp edges",
     "punchy, price-forward, high energy", "burst badges and bold price-block shapes"),
    ("文化创意", "culture-creative",
     "muted plum with ochre and bone", "textured art paper with layered collage edges",
     "artistic, layered, expressive", "hand-torn edges and overlapping planes"),
    ("金融保险", "finance-insurance",
     "deep forest green with restrained gold", "fine engraved texture and ruled paper",
     "authoritative, precise, enduring", "guilloche rules and columnar grids"),
]

# ── 全部 12 行业定义（B 端 4 个 + 主力 6 个 + 剩余 2 个）──
EXTRA_INDUSTRIES = [
    ("房地产", "real-estate",
     "warm stone and deep forest green", "concrete-grain texture with architectural paper",
     "structural, solid, aspirational", "architectural elevation lines and plan grids"),
    ("教育培训", "education-training",
     "friendly teal and soft sand", "clean matte card with rounded corners",
     "clear, encouraging, structured", "modular blocks and friendly rounded geometry"),
    ("医疗健康", "medical-health",
     "clean mint and clinical white", "soft-touch matte with rounded soft forms",
     "calm, trustworthy, precise", "gentle arcs and clear breathing space"),
    ("金融保险", "finance-insurance",
     "deep forest green with restrained gold", "fine engraved texture and ruled paper",
     "authoritative, precise, enduring", "guilloche rules and columnar grids"),
    ("商旅出行", "business-travel",
     "cool slate-blue and pale stone grey", "clean matte surfaces and soft brushed metal",
     "precise, calm, forward-motion", "subtle route lines and boarding-pass-like grid marks"),
    ("文化创意", "culture-creative",
     "muted plum with ochre and bone", "textured art paper with layered collage edges",
     "artistic, layered, expressive", "hand-torn edges and overlapping planes"),
]
# ── 主力 6 行业（v6 分批口径：覆盖广 + 视觉区分度强）──
BG_TONE = {'business-travel': 'pale stone grey', 'chinese-chic-illustration': 'warm off-white', 'minimal-business': 'warm grey', 'food-beverage': 'cream', 'tech-digital': 'deep navy', 'fashion-beauty': 'blush nude', 'education-training': 'soft sand', 'medical-health': 'clinical white', 'real-estate': 'warm stone', 'ecommerce-retail': 'clean white', 'culture-creative': 'bone', 'finance-insurance': 'deep forest green'}

MAIN_INDUSTRIES = [
    "ecommerce-retail",      # 电商零售 —— 覆盖最广
    "food-beverage",         # 食品餐饮 —— 高频场景
    "tech-digital",          # 科技数码 —— B 端主力
    "fashion-beauty",        # 时尚美妆 —— 视觉标杆
    "minimal-business",      # 极简商务 —— 通用兜底
    "chinese-chic-illustration",  # 国潮插画 —— 中国市场特色
]

# 行业池：由环境变量 INDUSTRY_SET 决定用哪批
import os as _os
_SET = _os.environ.get("INDUSTRY_SET", "main6")
if _SET == "b2b4":
    INDUSTRIES = [i for i in EXTRA_INDUSTRIES if i[1] in
                  ("real-estate", "education-training", "medical-health", "finance-insurance")]
elif _SET == "rest2":
    INDUSTRIES = [i for i in EXTRA_INDUSTRIES if i[1] in ("business-travel", "culture-creative")]
elif _SET == "all12":
    pass  # 原始 12 条即全集
else:
    INDUSTRIES = [i for i in INDUSTRIES if i[1] in MAIN_INDUSTRIES]


# ── 18 个品类：主体 + 是否含排版（含则必须用抽象条块） + 航道 ──
CATEGORIES = [
    ("logo", "logo", "L4",
     "a logo mark suite: one geometric primary mark plus a compact lockup arrangement, marks standing as flat shapes",
     False, "logo design"),
    ("poster", "poster", "L4",
     "a poster layout with a strong abstract focal shape and a bold typographic hierarchy",
     True, "poster design"),
    ("banner", "banner", "L4",
     "a wide promotional banner layout with one prominent focal shape and a confident typographic rhythm",
     True, "banner design"),
    ("menu", "menu", "L5",
     "an open printed menu page with a small dish illustration and a clean list structure",
     True, "menu design"),
    ("brochure", "brochure", "L5",
     "a tri-fold brochure with one open spread showing an image panel and a text panel",
     True, "brochure design"),
    ("business-card", "business-card", "L5",
     "a pair of business cards, one face up and one angled behind, with an embossed abstract mark",
     False, "business card design"),
    ("packaging", "packaging", "L1",
     "a product packaging box photographed at a flattering angle with a label panel and a subtle foil detail",
     True, "packaging design"),
    ("cover", "cover", "L5",
     "a printed cover with an embossed abstract artwork field and a foil edge catching the light",
     False, "cover design"),
    ("video-thumbnail", "video-thumbnail", "L4",
     "a video thumbnail composition with one dominant focal subject and a strong corner-to-corner diagonal",
     True, "video thumbnail design"),
    ("social-media", "social-media", "L4",
     "a set of social post cards of one hero card plus two supporting cards",
     True, "social media design"),
    ("ecommerce-main", "ecommerce-main", "L1",
     "a single product hero image on a clean studio podium with a soft contact shadow",
     False, "ecommerce main image"),
    ("product-detail", "product-detail", "L4",
     "a product detail page module with an image block and a feature block",
     True, "product detail page design"),
    ("ppt", "ppt", "L4",
     "a presentation slide with one dominant layout block and a clean supporting data-shape arrangement",
     True, "presentation slide design"),
    ("resume", "resume", "L4",
     "a resume layout with a clear column structure, an abstract avatar block and ruled content lines",
     True, "resume design"),
    ("font", "font", "L5",
     "a type specimen sheet showing large abstract glyph forms with fine rule lines and generous margins",
     False, "type specimen design"),
    ("illustration", "illustration", "L4",
     "an illustration set of three related flat artwork panels sharing one motif",
     False, "illustration design"),
    ("infographic", "data-story", "L4",
     "a data-story layout with abstract shapes, connected flow blocks and a clear visual hierarchy",
     True, "infographic design"),
    ("brand-identity", "brand-identity", "L5",
     "a brand identity system board with the mark, a color chip row and material sample squares",
     False, "brand identity system"),
]

# ── 12 种机位（瓦片间必须不同）──
CAMS = [
    "viewed straight on and perfectly centered",
    "seen from a slight three-quarter angle with a short throw shadow",
    "cropped tight into the main shape so it nearly fills the frame",
    "shown as a flat overhead top-down layout",
    "seen from a low angle looking slightly upward",
    "shown as a clean side profile against the backdrop",
    "placed off-center with generous negative space on one side",
    "overlapping a plain secondary sheet tucked behind it",
    "bled edge to edge so the composition runs off frame",
    "isolated small within a large calm field",
    "arranged on a bold diagonal axis",
    "layered with a soft foreground edge cutting the lower corner",
]

LANE_HEAD = {
    "L1": ("High-end commercial photograph, 85mm shallow depth of field, soft key light "
           "from the upper left with a gentle contact shadow"),
    "L4": ("Editorial flat-graphic composition on a Swiss grid, paper grain texture with "
           "riso-print ink edges, flat layout with no photographic perspective, flat even lighting"),
    "L5": ("Macro still-life photograph with raking side light revealing tactile texture, 100mm macro"),
    "L2": ("Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette "
           "with soft volumetric light and subtle film grain"),
}

TYPE_NOTE = ("all type is suggested only by abstract grey bars and shape blocks, never legible "
             "characters, no readable words anywhere, no screens, no UI windows")


def tile_prompt(cat, ind, tile_idx):
    slug, cid, lane, subject, has_type, _label = cat
    zh, iid, palette, material, mood, motif = ind
    assert tile_idx <= len(INDUSTRIES), (tile_idx, len(INDUSTRIES))
    cam = CAMS[tile_idx - 1]
    parts = [
        LANE_HEAD[lane],
        f"{palette} palette",
        material,
        f"{mood} mood",
        motif,
        f"one subject only: {subject}",
        cam,
        f"plain seamless backdrop in one flat {BG_TONE[iid]} tone",
        "hero fills about 70% of frame, bottom 25% clean for label scrim",
    ]
    if has_type:
        parts.append(TYPE_NOTE)
    parts += [f"locked seed and style reference shared across all {len(INDUSTRIES)} tiles",
              "1:1", "no text", "no letters", "no watermark"]
    return ", ".join(parts)


def media_prompt(cat):
    slug, cid, lane, subject, has_type, label = cat
    # 主图是品类总览：主体 + 少量辅件，16:10
    return (
        f"{LANE_HEAD[lane]}, a single confident composition introducing {label}: "
        f"{subject}, with two small supporting pieces arranged beside it for scale, "
        f"warm neutral palette with one saturated accent, camera at an equivalent 50mm "
        f"perspective, the arrangement fills about 65% of frame, 16:10, "
        + (f"{TYPE_NOTE}, " if has_type else "")
        + "top and bottom 8% fading to a neutral backdrop, "
          "no text, no letters, no watermark")


def main():
    recs = []

    # ── D1: 18 张 media 主图（每品类 1 张）──
    for cat in CATEGORIES:
        slug, cid, lane, subject, has_type, label = cat
        recs.append({
            "id": f"GM-{cid}", "priority": "P2", "series": "D-gallery-media",
            "theme": cid, "theme_label": label, "lane": LANE_HEAD[lane] and {
                "L1": "L1-photo-editorial", "L4": "L4-graphic-flat",
                "L5": "L5-material-still-life"}[lane],
            "variant": "hero-gallery", "field": "media",
            "w": 2160, "h": 1350, "ratio": "16:10",
            "prompt": media_prompt(cat),
            "alt": f"Lovart {label} — hero overview",
        })

    # ── D2: 216 张行业瓦片（18 品类 × 12 行业）──
    for cat in CATEGORIES:
        slug, cid, lane, subject, has_type, label = cat
        for i, ind in enumerate(INDUSTRIES, 1):
            zh, iid, palette, material, mood, motif = ind
            recs.append({
                "id": f"G-{cid}-{i:02d}{'-'+_SET if _SET!='main6' else ''}", "priority": "P2", "series": "D-gallery-tiles",
                "theme": cid, "theme_label": label, "industry": zh, "industry_id": iid,
                "lane": {"L1": "L1-photo-editorial", "L4": "L4-graphic-flat",
                         "L5": "L5-material-still-life"}[lane],
                "variant": "hero-gallery", "field": "gallery",
                "w": 1200, "h": 1200, "ratio": "1:1", "tile": i,
                "prompt": tile_prompt(cat, ind, i),
                "alt": f"Lovart {label} — {zh} visual style",
                "notes": "zh 页面 alt 用中文",
            })

    # ── D3: toolTiles 6 瓦 · 4 套 ──
    TOOL6 = [
        ("ai-ad-generator-landing-gallery-funnel", "ad-creative",
         ["product image set", "video ad", "paid creative", "brand kit", "social post", "email header"]),
        ("e_commerce", "ecommerce-tool",
         ["PDP image", "video ad", "paid creative", "brand kit", "packaging", "social post"]),
        ("marketers-preview", "marketer-tool",
         ["ad concept", "video hook", "social kit", "email header", "brand kit", "landing visual"]),
        ("zh-comparison-zh-pain", "zh-tool-matrix",
         ["poster", "logo", "cover", "main image", "video cover", "presentation slide"]),
    ]
    # 每套注入独立的材质/配色语汇，避免不同页面间 prompt 完全相同
    SET_FLAVOR = {
        "ad-creative": "glossy print finish, campaign energy, strong diagonal composition",
        "ecommerce-tool": "clean matte commerce finish, price-tag-like accent blocks",
        "marketer-tool": "soft uncoated paper finish, editorial restraint, generous margins",
        "zh-tool-matrix": "warm textured art paper, balanced contrast, moderate density",
    }
    for slug, cid, subjects in TOOL6:
        flavor = SET_FLAVOR[cid]
        for i, subj in enumerate(subjects, 1):
            recs.append({
                "id": f"GT-{cid}-{i}", "priority": "P2", "series": "D-gallery-tools",
                "theme": cid, "lane": "L4-graphic-flat", "variant": "hero-gallery",
                "field": "toolTiles", "w": 1200, "h": 1200, "ratio": "1:1", "tile": i,
                "label": subj,
                "prompt": (f"{LANE_HEAD['L4']}, {flavor}, warm neutral palette with one saturated accent, "
                           f"one subject only: a {subj} shown as a clean standalone design artifact, "
                           f"{CAMS[i-1]}, plain seamless backdrop in one flat warm grey tone, "
                           f"hero fills about 70% of frame, bottom 25% clean for label scrim, "
                           f"type suggested only by abstract grey bars, never legible characters, "
                           f"locked seed and style reference shared across all six tiles, 1:1, "
                           f"no text, no letters, no watermark"),
                "alt": f"Lovart {subj} — tool output example",
            })

    # ── D4: toolTiles 4 瓦 · 1 套（11 语言共用）──
    for i, (subj, lane) in enumerate([
        ("an image generation output", "L4"),
        ("a brand design artifact", "L5"),
        ("an editing adjustment result", "L1"),
        ("a video frame composition", "L2"),
    ], 1):
        head = LANE_HEAD[lane]
        recs.append({
            "id": f"GT-graphic-design-{i}", "priority": "P2", "series": "D-gallery-tools",
            "theme": "graphic-design-tools", "lane": {"L1": "L1-photo-editorial", "L2": "L2-cinematic-still",
                                                      "L4": "L4-graphic-flat", "L5": "L5-material-still-life"}[lane],
            "variant": "hero-gallery", "field": "toolTiles", "w": 1200, "h": 1200,
            "ratio": "1:1", "tile": i, "label": subj,
            "prompt": (f"{head}, warm neutral palette with one saturated accent, "
                       f"one subject only: {subj}, {CAMS[i-1]}, plain seamless backdrop in one flat "
                       f"warm grey tone, hero fills about 70% of frame, bottom 25% clean for label scrim, "
                       f"locked seed and style reference shared across all four tiles, 1:1, "
                       f"no text, no letters, no watermark"),
            "alt": f"Lovart {subj} — capability example",
            "notes": "11 个语言版本共用同一套图（label 已本地化，图不需本地化）",
        })

    p = OUT / f"module-D-gallery{('-'+_SET) if _SET!='main6' else ''}.jsonl"
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
    from collections import Counter
    print(f"module-D-gallery.jsonl: {len(recs)} 条")
    print("  按 series:", dict(Counter(r["series"] for r in recs)))
    print("  按 field :", dict(Counter(r["field"] for r in recs)))


if __name__ == "__main__":
    main()
