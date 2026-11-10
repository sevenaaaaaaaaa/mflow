#!/usr/bin/env python3
"""tmp_gen_queue.py — 汇总全部模块 → generate-queue.jsonl（执行顺序 + 分批）+ NEXT-STEPS.md"""
import json
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")

def load(name):
    return [json.loads(l) for l in (D / name).read_text(encoding="utf-8").splitlines() if l.strip()]

p0 = load("p0-batch-v2.jsonl")
p1 = load("p1-batch.jsonl")
A = load("module-A-split.jsonl")
B = load("module-B-cinematic.jsonl")
C = load("module-C-mosaic.jsonl")
Dg = load("module-D-gallery.jsonl")

# A 模块里 P0 六条与 p0-batch-v2 重复，以 module-A 为准
a_ids = {r["id"] for r in A}
p0 = [r for r in p0 if r["id"] not in a_ids] or p0

gallery_tiles = [r for r in Dg if r["field"] == "gallery"]
gallery_media = [r for r in Dg if r["field"] == "media"]
gallery_tools = [r for r in Dg if r["field"] == "toolTiles"]

# 品类顺序：先跑含排版风险最高的验证，再全量
CAT_ORDER = ["logo", "ecommerce-main", "business-card", "cover", "brand-identity", "font",
             "illustration", "menu", "brochure", "packaging", "poster", "banner",
             "social-media", "video-thumbnail", "product-detail", "ppt", "resume", "data-story"]
CAT_LABEL = {r["theme"]: r.get("theme_label", r["theme"]) for r in gallery_tiles}

queue = []
def add(recs, step, name, note=""):
    for r in recs:
        q = dict(r); q["step"] = step; q["step_name"] = name; q["order"] = len(queue) + 1
        if note: q["step_note"] = note
        queue.append(q)

# Step 1: P0 split
add([r for r in A if r["priority"] == "P0"], 1, "P0 止血",
    "出图即替换 83c980ae.jpg 死链（65 处引用）")
# Step 2: B cinematic
add(B, 2, "P1 品牌旗舰 cinematic", "lovart-2-0 / landing-full / 行业方案首屏")
# Step 3: C mosaic
add(C, 3, "P1 分步叙事 mosaic", "每套 4 瓦同一会话 + 锁 seed")
# Step 4: A 其余 split
add([r for r in A if r["priority"] != "P0"], 4, "P2 其余主题族 split")
# Step 5: D1 media 主图
add(gallery_media, 5, "P2 gallery · media 主图（18 张）",
    "每品类一张总览，16:10")
# Step 6: D2 行业瓦片（按品类跑，每品类 12 张一次会话）
for cat in CAT_ORDER:
    grp = sorted([r for r in gallery_tiles if r["theme"] == cat], key=lambda r: r["tile"])
    if not grp:
        continue
    add(grp, 6, f"P2 gallery · {cat}（{CAT_LABEL.get(cat, cat)}）",
        "6 主力行业同一会话 + 锁 seed；机位互斥；含排版品类用抽象条块代替文字")
# Step 7: D3/D4 工具瓦片
add(gallery_tools, 7, "P2 gallery · 工具瓦片（28 张）",
    "6 瓦套按页面分组跑；4 瓦套 11 语言共用")

(D / "generate-queue.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in queue) + "\n", encoding="utf-8")

from collections import Counter
steps = Counter((r["step"], r["step_name"]) for r in queue)
print(f"generate-queue.jsonl: {len(queue)} 条")
for (s, n), c in sorted(steps.items()):
    print(f"  Step {s} · {n}: {c}")
