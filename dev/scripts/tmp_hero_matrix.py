#!/usr/bin/env python3
"""tmp_hero_matrix.py — 主题族 × hero 变体 封面制作矩阵 v3（最终口径）"""
import json, re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
docs = [json.loads(l) for l in (HERE / "tmp_pages.jsonl").read_text().splitlines() if l.strip()]

THEME_RULES = [
    ("industry", "行业方案（zh-solution）", r"^zh-solution"),
    ("compare", "对比与替代", r"-vs-|vs-|alternative|better-than"),
    ("video", "视频生成与编辑", r"video|sora|veo|kling|seedance|hailuo|swap-to-video|short-video|cinematic|cinema|film-studio|animation|storyboard|gif|slideshow|explainer|commercial-generator|motion|webtoon|wan-"),
    ("avatar", "头像与人物", r"avatar|pfp|portrait|face-swap|face-enhancer|face-retouch|cartoon|baby-face|baby-name|gender-swap|hairstyle|makeup|caricature|pet-portrait|character|digital-human|virtual-actor|team-photo|aging-filter|image-to-cartoon|photo-to-cartoon|body-generator|filter"),
    ("fashion", "时尚服饰", r"fashion|lookbook|apparel|clothing|t-shirt|jewelry"),
    ("ads", "广告素材", r"ad-generator|ad-creator|ad-designer|ads-generator|-ad-|-ads-|display-ad|retargeting|advertis|promo|giveaway|sale-poster|discount|subscribe-ad|lead-generation"),
    ("creator-av", "创作者频道物料", r"youtube|twitch|discord|end-screen|overlay"),
    ("social", "社媒内容", r"social|instagram|tiktok|facebook|twitter|pinterest|linkedin|post-generator|post-maker|ugc|meme|carousel|story|wechat|xiaohongshu|weibo|bilibili|douyin|viral-content|seamless-carousel|hashtag|sticker|emoji|highlight-cover|webinar"),
    ("logo-brand", "Logo 与品牌", r"logo|brand|branding|style-guide|color-palette|font|typography|icon"),
    ("ecommerce", "电商与产品图", r"product|ecommerce|etsy|amazon|shopify|storefront|try-on|phone-case|earbuds|label-maker|nutrition-label|wine-label|catalog|retail|listing|mockup|packaging|display|photography"),
    ("3d", "3D 与模型", r"3d|model-generator"),
    ("interior", "室内与房产", r"interior|room-planner|virtual-staging|real-estate|property"),
    ("education", "教育物料", r"lesson-plan|worksheet|flashcard|course|textbook|quiz|classroom|education"),
    ("docs-deck", "文档与演示", r"presentation|pitch-deck|slides|infographic|report|proposal|whitepaper|invoice|resume|cv-template|roadmap|timeline|mind-map|flowchart|comparison-chart|org-chart|organizational|data-visualization|fact-sheet|company-profile|annual-report|tender|training|newsletter|email|medium-article|blog|chat-pdf|pdf|crisis|bdr|sales|investor"),
    ("audio", "音频与音乐", r"(^|-)voice|(^|-)audio|music|sound|podcast"),
    ("photo-edit", "照片编辑与增强", r"photo-editor|photo-enhancer|photo-retouch|photo-collage|image-enhancer|image-restorer|image-colorizer|image-resizer|image-extender|expand-tool|background-remover|background-generator|background-swap|object-remover|remove-object|watermark-remover|4k-upscaler|4k-resolution|image-upscaler|image-compressor|file-converter|pdf-converter|format-converter|screenshot-editor|style-transfer|upscaler|change-video-background|video-background|inpainting"),
    ("web-ui", "网站与 UI", r"landing-page|wireframe|app-design|website|web-banner|popup|web-app|browser"),
    ("image-gen", "图像生成", r"image-generator|text-to-image|image-to-image|picture-generator|photo-generator|gpt-image|flux|dreamshaper|sdxl|leonardo|nano-banana|nanobanana|seedream|stock-photo|stock-image|art-generator|artwork|concept-art|wallpaper|pattern|vector|svg|controlnet|chat-to-image|product-to-image|photoreal|anime|moodboard|mood-board|vision-board|illustration"),
    ("print", "印刷与品牌物料", r"poster|flyer|brochure|banner|business-card|invitation|greeting|birthday|announcement|thank-you|certificate|diploma|letterhead|envelope|menu|magazine|book-cover|album-cover|postcard|door-hanger|table-tent|gift-card|coupon|id-card|calendar|price-list|recipe-card|scrapbook|print|card-maker|card-design|qr-code|billboard"),
    ("platform", "平台与 Agent 能力", r"agent|agentic|chatcanvas|mcot|multi-model|model|workflow|batch|api|enterprise|collaboration|team-|approval|integration|copilot|canvas|magic-studio|creative-suite|design-platform|toolkit|all-in-one|assets-library|asset-library|template-library|studio|automation|safety|authenticity|compliance|privacy|gdpr|copyright|playground|productivity|community|free-trial|no-code|drag-and-drop|one-click|real-time|instant|fast-|easy-|effortless|simple-|save-time|no-experience|turn-ideas|stunning|professional-results|ready-to-publish|high-quality|customizable|subscription-fatigue|blank-canvas|pixel-pusher|overcome|natural-home|free-online-tool|graphic|design"),
]

ZH_TITLE_RULES = [
    ("social", "社媒内容", r"社媒|小红书|抖音|微博|B站|公众号|朋友圈|贴文|内容日历|表情|贴纸|UP主|达人|MCN"),
    ("video", "视频生成与编辑", r"视频|影片|动画|图片转视频"),
    ("ecommerce", "电商与产品图", r"电商|商品|产品|详情页|主图|淘宝|京东|拼多多|跨境电商"),
    ("image-gen", "图像生成", r"图片|图像|插画"),
    ("logo-brand", "Logo 与品牌", r"品牌|logo|Logo|LOGO|视觉识别|VI"),
    ("docs-deck", "文档与演示", r"演示|PPT|简历|图表|报告|白皮书|信息图|思维导图"),
    ("print", "印刷与品牌物料", r"海报|传单|名片|菜单|画册|封面|贺卡|邀请|日历|证书|招牌|包装|横幅|字体"),
    ("platform", "平台与 Agent 能力", r"平台|智能体|工作流|协作|企业|安全|版权|定价|价格|评价|常见问题|指南|中国|替代|工具|效率|选择|修改|设计|落地页"),
]

def theme_of(slug, title=""):
    s = (slug or "").lower()
    if s.startswith("zh-"):
        for name, label, pat in ZH_TITLE_RULES:
            if re.search(pat, title or ""):
                return name, label
        return "misc", "未归类"
    for name, label, pat in THEME_RULES:
        if re.search(pat, s):
            return name, label
    return "misc", "未归类"

VARS = ["hero-split", "hero-cinematic", "hero-journey", "hero-mosaic", "hero-gallery",
        "centeredInputSection", "NONE"]
IMG_VARS = ["hero-split", "hero-cinematic", "hero-mosaic", "hero-gallery"]
TILES = {"hero-split": 1, "hero-cinematic": 1, "hero-mosaic": 4, "hero-gallery": 6}

slug_map = {}
for d in docs:
    if not d["slug"]:
        continue
    rec = slug_map.setdefault((d["pageType"], d["slug"]),
                              {"heros": Counter(), "langs": set(), "title": d["title"]})
    rec["heros"][d["hero"]] += 1
    rec["langs"].add(d["lang"])

MANUAL_FIX = {"ai-design-generator-landing-agent-workflow": "hero-split",
              "dall-e-image-generation-landing-trial-now": None,
              "image-to-video-ai": None}
for (pt, s), rec in slug_map.items():
    if s in MANUAL_FIX and "NONE" in rec["heros"]:
        fx = MANUAL_FIX[s]
        del rec["heros"]["NONE"]
        if fx:
            rec["heros"][fx] += 1

# ── A. 类型 × 变体 ──
print("=" * 80)
print("A. 类型 × 首段 hero 变体（slug 级；同 slug 多语言可能跨变体）")
cell = defaultdict(set)
for (pt, s), rec in slug_map.items():
    for h in rec["heros"]:
        cell[(pt, h)].add(s)
types = sorted({pt for (pt, _) in cell})
print(f"{'type':<10}" + "".join(f"{v.replace('hero-','')[:9]:>10}" for v in VARS) + "   slugs")
for pt in types:
    row = [len(cell.get((pt, v), set())) for v in VARS]
    tot = len({s for (p, v) in cell if p == pt for s in cell[(p, v)]})
    print(f"{pt:<10}" + "".join(f"{n:>10}" for n in row) + f"{tot:>7}")

# ── B. 主题族 × 变体 ──
theme_pages = {}
for (pt, s), rec in slug_map.items():
    t, label = theme_of(s, rec["title"])
    tp = theme_pages.setdefault(t, {"label": label, "slugs": set(), "heros": Counter(),
                                    "types": Counter(), "langs": set(), "cells": defaultdict(set)})
    tp["slugs"].add(s)
    for h, n in rec["heros"].items():
        tp["heros"][h] += n
    tp["types"][pt] += 1
    tp["langs"].update(rec["langs"])
    for h in rec["heros"]:
        tp["cells"][h].add(s)

print()
print("=" * 80)
print("B. 主题族 × 变体（slug 级页面数）")
print(f"{'主题族':<11}{'label':<14}" + "".join(f"{v.replace('hero-','')[:9]:>10}" for v in VARS) + f"{'slugs':>7}{'langs':>7}")
order = sorted(theme_pages, key=lambda t: -len(theme_pages[t]["slugs"]))
for t in order:
    tp = theme_pages[t]
    row = [len(tp["cells"].get(v, set())) for v in VARS]
    print(f"{t:<11}{tp['label']:<14}" + "".join(f"{n:>10}" for n in row)
          + f"{len(tp['slugs']):>7}{len(tp['langs']):>7}")

# ── C. 封面制作量 ──
print()
print("=" * 80)
print("C. 封面制作量（口径一：现状真实存在的 主题×变体 格子）")
print(f"{'主题族':<11}{'label':<14}" + "".join(f"{v.replace('hero-','')[:9]:>10}" for v in IMG_VARS) + f"{'小计':>6}")
total_cur, detail = 0, {}
for t in order:
    tp = theme_pages[t]
    nums, sub = {}, 0
    for v in IMG_VARS:
        n = TILES[v] if tp["cells"].get(v) else 0
        nums[v] = n
        sub += n
    if sub == 0:
        continue
    detail[t] = (tp["label"], nums, sub, len(tp["slugs"]))
    total_cur += sub
    print(f"{t:<11}{tp['label']:<14}" + "".join(f"{nums[v]:>10}" for v in IMG_VARS) + f"{sub:>6}")
print(f"{'合计':<25}" + " " * 40 + f"{total_cur:>6}")

n_th = len([t for t in order if theme_pages[t]["slugs"] and t != "misc"])
full = n_th * sum(TILES.values())
print()
print(f"口径二（全交叉补齐）：{n_th} 主题族 × (1 split + 1 cinematic + 4 mosaic + 6 gallery) = {full} 张")
n_s = sum(1 for t in detail if detail[t][1]["hero-split"])
n_c = sum(1 for t in detail if detail[t][1]["hero-cinematic"])
print(f"口径三（瓦片产品级共享）：split {n_s} + cinematic {n_c} + mosaic 4 + gallery 6 = {n_s + n_c + 10} 张")

# ── D. 明细 ──
print()
print("=" * 80)
print("D. 主题族明细")
for t in order:
    tp = theme_pages[t]
    slugs = sorted(tp["slugs"])
    sample = ", ".join(slugs[:7]) + (" …" if len(slugs) > 7 else "")
    print(f"{t} [{tp['label']}] {len(slugs)} slugs | {sample}")

misc = sorted({s for (pt, s) in slug_map if theme_of(s, slug_map[(pt, s)]["title"])[0] == "misc"})
print()
print(f"E. 未归类 misc（{len(misc)}）：", ", ".join(misc))
