#!/usr/bin/env python3
"""tmp_rebuild_all.py — 一键重建 batches/ 与 md/（源文件正确后运行）"""
import json, subprocess, sys
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
B = D / "batches"

CAT = ["logo","ecommerce-main","business-card","cover","brand-identity","font",
       "illustration","menu","brochure","packaging","poster","banner",
       "social-media","video-thumbnail","product-detail","ppt","resume","data-story"]

def load(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

def dump(p, rows):
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

# 清理旧 D2/E1/E3 文件
for pat in ("D2-*.jsonl", "E1-*.jsonl", "E3-*.jsonl"):
    for f in B.glob(pat):
        f.unlink()

made = {}
# D 主批（6 主力行业）
recs = load(D / "module-D-gallery.jsonl")
dump(B / "D1-media.jsonl", [r for r in recs if r["field"] == "media"])
dump(B / "D3-tools.jsonl", [r for r in recs if r["field"] == "toolTiles"])
tiles = [r for r in recs if r["field"] == "gallery"]
for cat in CAT:
    g = sorted([r for r in tiles if r["theme"] == cat], key=lambda r: r["tile"])
    if g:
        dump(B / f"D2-{CAT.index(cat)+1:02d}-{cat}.jsonl", g)
        made[f"D2-{cat}"] = len(g)

# E1 / E3
for prefix, src in [("E1", "module-D-gallery-b2b4.jsonl"), ("E3", "module-D-gallery-rest2.jsonl")]:
    rs = [r for r in load(D / src) if r["field"] == "gallery"]
    for cat in CAT:
        g = sorted([r for r in rs if r["theme"] == cat], key=lambda r: r["tile"])
        if g:
            dump(B / f"{prefix}-{CAT.index(cat)+1:02d}-{cat}.jsonl", g)
            made[f"{prefix}-{cat}"] = len(g)

print(f"batches/ 重建完成：")
print(f"  D1-media: {len(load(B/'D1-media.jsonl'))}")
print(f"  D3-tools: {len(load(B/'D3-tools.jsonl'))}")
print(f"  D2 批次: {sum(v for k,v in made.items() if k.startswith('D2-'))} 张 ({len([k for k in made if k.startswith('D2-')])} 文件)")
print(f"  E1 批次: {sum(v for k,v in made.items() if k.startswith('E1-'))} 张 ({len([k for k in made if k.startswith('E1-')])} 文件)")
print(f"  E3 批次: {sum(v for k,v in made.items() if k.startswith('E3-'))} 张 ({len([k for k in made if k.startswith('E3-')])} 文件)")

# 重建 md
r = subprocess.run([sys.executable, "dev/scripts/tmp_gen_all_md.py"],
                   cwd="/Users/seveno/MFlow Dev/mflow", capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip())

# 全量 QC
files = sorted(B.glob("*.jsonl")) + [D / "E5-cinematic-video.jsonl"]
ok = bad = total = 0
for f in files:
    n = len([1 for l in f.read_text(encoding="utf-8").splitlines() if l.strip()])
    total += n
    r = subprocess.run([sys.executable, "dev/scripts/tmp_brief_qc.py", str(f)],
                       cwd="/Users/seveno/MFlow Dev/mflow", capture_output=True, text=True)
    if "通过" in r.stdout.splitlines()[-1]:
        ok += 1
    else:
        bad += 1
        print(f"  FAIL {f.name}")
print(f"\nQC: {ok} 通过 / {bad} 失败，共 {total} 张")
