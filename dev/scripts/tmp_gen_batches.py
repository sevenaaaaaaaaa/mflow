#!/usr/bin/env python3
"""tmp_gen_batches.py — 按品类拆分 D 模块为独立投喂文件 + 生成分批总表

输出：
  batches/D1-media.jsonl             18 张总览主图
  batches/D2-{01..18}-{cat}.jsonl    每品类 6 张行业瓦片（每批可单独跑）
  batches/D3-tools.jsonl             28 张工具瓦片
  BATCH-PLAN.md                      分批总表与执行说明
"""
import json
from collections import Counter
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
B = D / "batches"
B.mkdir(exist_ok=True)

recs = [json.loads(l) for l in (D / "module-D-gallery.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
media = [r for r in recs if r["field"] == "media"]
tiles = [r for r in recs if r["field"] == "gallery"]
tools = [r for r in recs if r["field"] == "toolTiles"]

# 含排版语义的品类（生成风险最高，建议后排）
TYPE_CATS = {"poster", "banner", "menu", "brochure", "packaging", "video-thumbnail",
             "social-media", "product-detail", "ppt", "resume", "data-story"}

# 品类分批顺序：先跑无排版风险 + 覆盖广的，再跑含排版的
CAT_ORDER = [
    "logo", "ecommerce-main", "business-card", "cover", "brand-identity", "font",
    "illustration", "menu", "brochure", "packaging", "poster", "banner",
    "social-media", "video-thumbnail", "product-detail", "ppt", "resume", "data-story",
]

def dump(path, rows):
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

# D1
dump(B / "D1-media.jsonl", media)

# D2 按品类
by_cat = {}
for cat in CAT_ORDER:
    grp = sorted([r for r in tiles if r["theme"] == cat], key=lambda r: r["tile"])
    if not grp:
        continue
    idx = CAT_ORDER.index(cat) + 1
    by_cat[cat] = grp
    dump(B / f"D2-{idx:02d}-{cat}.jsonl", grp)

# D3
dump(B / "D3-tools.jsonl", tools)

# ── BATCH-PLAN.md ──
L = []
L.append("# D 模块分批投喂计划（6 主力行业 · 154 张）\n")
L.append("> 目录：`batches/`，每个文件可独立投喂，跑完再开下一个。")
L.append("> 行业维度（6 个主力）：电商零售 / 食品餐饮 / 科技数码 / 时尚美妆 / 极简商务 / 国潮插画\n")

INDS = ["电商零售", "食品餐饮", "科技数码", "时尚美妆", "极简商务", "国潮插画"]

L.append("## 一览\n")
L.append("| 批次 | 文件 | 张数 | 规格 | 说明 |")
L.append("|---|---|---:|---|---|")
L.append(f"| D1 | `D1-media.jsonl` | {len(media)} | 2160×1350 · 16:10 | 18 品类总览主图 |")
for i, cat in enumerate([c for c in CAT_ORDER if c in by_cat], 1):
    grp = by_cat[cat]
    risk = "⚠ 含排版" if cat in TYPE_CATS else "—"
    L.append(f"| D2-{i:02d} | `D2-{i:02d}-{cat}.jsonl` | {len(grp)} | 1200×1200 · 1:1 | {grp[0].get('theme_label', cat)}　{risk} |")
L.append(f"| D3 | `D3-tools.jsonl` | {len(tools)} | 1200×1200 · 1:1 | 6 瓦套 ×4 + 4 瓦套 ×1 |")
L.append(f"| **合计** | | **{len(media)+len(tiles)+len(tools)}** | | |")

L.append("\n## 执行顺序建议\n")
L.append("1. **D1 先跑**（18 张）—— 这 18 张是每品类的总览图，跑完能一眼看出 18 个品类是否都成立，成本最低的验证。")
L.append("2. **D2 按序号跑**，先跑前 6 批（logo / ecommerce-main / business-card / cover / brand-identity / font，共 36 张），这 6 个品类不含排版语义，生成最稳。")
L.append("3. **中间 5 批**（illustration / menu / brochure / packaging / poster，30 张）开始引入排版。")
L.append("4. **最后 7 批**（banner / social-media / video-thumbnail / product-detail / ppt / resume / data-story，42 张）全部含排版，用前面验证过的「抽象条块」手法。")
L.append("5. **D3 最后跑**（28 张）—— 工具瓦片有明确 toolTiles label 参照，风险最低。\n")

L.append("## 每批操作纪律\n")
L.append("| 项 | 要求 |")
L.append("|---|---|")
L.append("| 同批同会话 | 一个品类的 6 张必须同一会话连续生成 |")
L.append("| 锁 seed | 同批 6 张共用同一 seed + 同一风格参考图 |")
L.append("| 机位互斥 | 6 张自动分配不同机位（正视/侧角/微距/俯拍/低角度/侧轮廓） |")
L.append("| 背景一致 | 同批 6 张背景为同一 flat 色 |")
L.append("| 只换行业 | 6 张之间只变行业配色/材质/气质，不变构图语言 |")
L.append("| 排版品类 | 图内不得出现可读字符；排版层级用抽象灰色条块表达 |")
L.append("| 命名 | `hero-gallery-{cat}-{industry}-v1.png` |")

L.append("\n## 6 行业视觉参数速查\n")
L.append("| 行业 | 配色 | 材质 | 气质 |")
L.append("|---|---|---|---|")
L.append("| 电商零售 | vivid coral + clean white + charcoal | 光泽印面、锐利边 | punchy、价格前置、高能量 |")
L.append("| 食品餐饮 | terracotta + cream + deep olive | 有机肌理、碎屑与蒸汽感 | 温暖、可触、诱人 |")
L.append("| 科技数码 | deep navy + electric cyan + cool white | 哑光复合材质、细网格 | 精准、工程感、前倾 |")
L.append("| 时尚美妆 | blush nude + soft charcoal | 缎面、珠光 | 编辑部式优雅、从容 |")
L.append("| 极简商务 | mono-tone warm grey + one ink | 无涂布纸、发丝线 | 安静、精确、大留白 |")
L.append("| 国潮插画 | vermilion + antique gold + warm off-white | 水墨肌理、印章红 | 传统而现代、克制的华丽 |")

L.append("\n## 批次进度追踪\n")
L.append("| 批次 | 状态 | 备注 |")
L.append("|---|---|---|")
L.append(f"| D1 media | ☐ 待生成 | |")
for i, cat in enumerate([c for c in CAT_ORDER if c in by_cat], 1):
    L.append(f"| D2-{i:02d} {cat} | ☐ 待生成 | |")
L.append("| D3 tools | ☐ 待生成 | |")

(D / "BATCH-PLAN.md").write_text("\n".join(L) + "\n", encoding="utf-8")

print(f"batches/ 目录：")
for f in sorted(B.iterdir()):
    n = len([1 for l in f.read_text(encoding='utf-8').splitlines() if l.strip()])
    print(f"  {f.name:<32} {n:>3} 条")
print(f"\nBATCH-PLAN.md 已生成")
