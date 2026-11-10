#!/usr/bin/env python3
"""tmp_gallery_plan.py — 基于真实台账重算 gallery 封面需求，输出制作计划"""
import json, re
from collections import Counter, defaultdict, OrderedDict
from pathlib import Path

LEDGER = Path(__file__).resolve().parent / "gallery-ledger.json"
rows = json.loads(LEDGER.read_text(encoding="utf-8"))

# ── 品类识别（从 slug 提取；zh-topic- 前缀）──
CAT_RULES = [
    ("logo", r"logo"),
    ("poster", r"poster"),
    ("banner", r"banner"),
    ("menu", r"menu"),
    ("brochure", r"brochure"),
    ("business-card", r"business-card"),
    ("packaging", r"packaging"),
    ("cover", r"^zh-topic-cover-design"),
    ("video-thumbnail", r"video-thumbnail"),
    ("social-media", r"social-media-design"),
    ("ecommerce-main", r"ecommerce-main-image"),
    ("product-detail", r"product-detail"),
    ("ppt", r"ppt"),
    ("resume", r"resume"),
    ("font", r"font"),
    ("illustration", r"illustration"),
    ("infographic", r"infographic"),
    ("brand-identity", r"brand-visual-identity"),
]

def cat_of(slug):
    s = slug.lower()
    for name, pat in CAT_RULES:
        if re.search(pat, s):
            return name
    return "other"

# ── 分组 ──
g12 = [r for r in rows if r["tile_field"] == "gallery" and r["tile_count"] == 12]
t6 = [r for r in rows if r["tile_field"] == "toolTiles" and r["tile_count"] == 6]
t4 = [r for r in rows if r["tile_field"] == "toolTiles" and r["tile_count"] == 4]

print("=" * 78)
print("A. gallery 真实形态分布（唯一页面）")
print(f"  12 瓦 · gallery  · 行业维度：{len(g12)} 页")
print(f"   6 瓦 · toolTiles · 工具维度：{len(t6)} 页")
print(f"   4 瓦 · toolTiles · 工具维度：{len(t4)} 页（同一页面 11 个语言版本）")
print(f"  合计唯一页面：{len(rows)}（Sanity 文档 87，多语言折叠后 69）")

print()
print("=" * 78)
print("B. 12 瓦组的品类拆分（每个品类各有独立 12 行业）")
bycat = defaultdict(list)
for r in g12:
    bycat[cat_of(r["slug"])].append(r["slug"])
print(f"{'品类':<16}{'页数':>6}  代表页")
for c, slugs in sorted(bycat.items(), key=lambda x: -len(x[1])):
    print(f"{c:<16}{len(slugs):>6}  {slugs[0]}")
print(f"{'合计':<16}{len(g12):>6}")

INDUSTRIES = [t["label"] for t in g12[0]["tiles"]] if g12 else []
print(f"\n12 个行业维度（50 页共用同一 label 组合）：{INDUSTRIES}")

print()
print("=" * 78)
print("C. 封面需求量重算")
n_cat = len(bycat)
tiles_12 = n_cat * 12
media_12 = n_cat
print(f"  12 瓦组：{n_cat} 品类 × 12 行业 = {tiles_12} 张瓦片")
print(f"           + {media_12} 张 media 主图（按品类）= {media_12} 张")
print(f"  6 瓦组：3 套工具维度独有 + 1 套（zh-comparison/zh-pain 5 页共用）= "
      f"{(len({r['slug'] for r in t6}) )} 套 × 6")
sets6 = {}
for r in t6:
    key = tuple(t["label"] for t in r["tiles"])
    sets6.setdefault(key, []).append(r["slug"])
print(f"          实际去重后 {len(sets6)} 套 × 6 = {len(sets6)*6} 张")
sets4 = {}
for r in t4:
    key = tuple(t["label"] for t in r["tiles"])
    sets4.setdefault(key, []).append(r["slug"])
print(f"  4 瓦组：{len(sets4)} 套 × 4 = {len(sets4)*4} 张")
total = tiles_12 + media_12 + len(sets6) * 6 + len(sets4) * 4
print(f"\n  ▶ D 模块真实需求 = {total} 张（原估 60 张，低估 {total-60} 张）")

print()
print("=" * 78)
print("D. 6/4 瓦组的真实 label 清单（需按页定制）")
for i, (labels, slugs) in enumerate(sets6.items(), 1):
    print(f"  6瓦套{i}（{len(slugs)} 页：{', '.join(sorted(set(slugs))[:3])}…）")
    print(f"     {list(labels)}")
for i, (labels, slugs) in enumerate(sets4.items(), 1):
    print(f"  4瓦套{i}（{len(slugs)} 页多语言）")
    print(f"     {list(labels)}")

print()
print("=" * 78)
print("E. 现状缺陷")
imgs = Counter()
for r in g12:
    for t in r["tiles"]:
        imgs[t["img"]] += 1
print(f"  50 个 12 瓦页面共用 {len(imgs)} 张图（每张被引用 {list(imgs.values())[0]} 次）")
print(f"  且这 {len(imgs)} 张是无关联的占位图（已验证：一个圆圈内数字 1 等）")
print(f"  → 全站 600 个行业瓦片位（50 页 × 12）实际只有 3 张图在轮转")

# ── 输出计划 JSON ──
plan = {
    "summary": {
        "pages_unique": len(rows),
        "docs_total": 87,
        "g12_pages": len(g12), "g12_categories": n_cat,
        "t6_sets": len(sets6), "t4_sets": len(sets4),
        "total_tiles_needed": tiles_12, "total_media_needed": media_12,
        "total_sets_6": len(sets6) * 6, "total_sets_4": len(sets4) * 4,
        "grand_total": total,
    },
    "industries": INDUSTRIES,
    "categories": {c: sorted(s) for c, s in bycat.items()},
    "tool_sets_6": [{"labels": list(k), "pages": sorted(set(v))} for k, v in sets6.items()],
    "tool_sets_4": [{"labels": list(k), "pages": sorted(set(v))} for k, v in sets4.items()],
}
(Path(__file__).resolve().parent / "gallery-plan.json").write_text(
    json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n计划已写入 gallery-plan.json")
