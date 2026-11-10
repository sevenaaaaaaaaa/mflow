#!/usr/bin/env python3
"""tmp_gen_batches_e1.py — E1 批次：4 个 B 端行业 × 18 品类 = 72 张，按品类拆分"""
import json, os, subprocess, sys
from pathlib import Path
from collections import Counter

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
B = D / "batches"
B.mkdir(exist_ok=True)

src = D / "module-D-gallery-b2b4.jsonl"
recs = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
tiles = [r for r in recs if r["field"] == "gallery"]
print(f"B 端行业瓦片: {len(tiles)} 张（应为 72）")

CAT_ORDER = [
    "logo", "ecommerce-main", "business-card", "cover", "brand-identity", "font",
    "illustration", "menu", "brochure", "packaging", "poster", "banner",
    "social-media", "video-thumbnail", "product-detail", "ppt", "resume", "data-story",
]

def dump(path, rows):
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

count = 0
for cat in CAT_ORDER:
    grp = sorted([r for r in tiles if r["theme"] == cat], key=lambda r: r["tile"])
    if not grp:
        continue
    idx = CAT_ORDER.index(cat) + 1
    dump(B / f"E1-{idx:02d}-{cat}.jsonl", grp)
    count += len(grp)

print(f"已生成 {count} 张 → batches/E1-*.jsonl")
print("行业:", sorted({r["industry"] for r in tiles}))
