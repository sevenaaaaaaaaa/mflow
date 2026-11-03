#!/usr/bin/env python3
"""tmp_refine_v3.py — P2/P1 brief 精修 v3：构图多样性 + 布光/焦段补齐 + 调色板分散

修复项（对应 tmp_style_audit.py 报告）：
  R1  gallery 60 条：按 tile 序号注入机位变化 + 填充率变化（消除同构）
  R2  mosaic 8 条：4 瓦机位递进
  R3  L5 gallery（G-PRT/G-LOG）补 100mm 焦段
  R4  L4 gallery（G-SOC/G-DOC/G-ADS/G-CMP）补 flat 透视声明 + 均匀光
  R5  L4 调色板分散：G-DOC→ink blue，G-CMP→duotone，G-LOG copper→brass
  R6  G-CMP 六瓦句式变化（原来全用 "a split card — left/right"）
  R7  S-AVA/S-PED/S-IND/S-CRE/S-FAS 补布光
  R8  S-ADS/S-CMP/S-WEB/S-EDU 补焦段或 flat 声明
  R9  C-PLA 补等效焦段
  R10 G-VID 显式声明严格双色（teal-and-amber，无第三色）

用法：python3 tmp_refine_v3.py  → 重写 p2-batch.jsonl / p1-batch.jsonl
     然后 python3 tmp_gen_modules.py → 重新生成 module-*.jsonl 与 module-briefs.md
"""
import json
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")

# ── R1 机位 × 填充率（6 瓦） ──
CAM6 = [
    ("viewed straight on at eye level", 70),
    ("viewed at a slight three-quarter angle", 68),
    ("framed as a close macro on the material surface", 76),
    ("seen from directly above in a clean top-down", 66),
    ("seen from a low angle looking slightly upward", 72),
    ("viewed as a crisp side profile", 70),
]
# ── R2 机位（4 瓦） ──
CAM4 = [
    "at eye level, the console running left to right",
    "from a slight three-quarter angle, the console receding into depth",
    "in a closer macro, the slot filling most of the frame",
    "from a pulled-back wide angle showing the whole console",
]
# ── R5 调色板分散 ──
L4_PAL = {
    "G-SOC": "cream field with coral and charcoal accents",
    "G-DOC": "ivory field with ink-blue and charcoal accents",
    "G-ADS": "cream field with tangerine and charcoal accents",
    "G-CMP": "ivory surface split into muted grey on one side and coral on the other",
}
L5_PAL = {
    "G-PRT": "ivory and grey palette with one copper accent",
    "G-LOG": "ivory and charcoal palette with one brass accent",
}
L1_PAL = {
    "G-IMG": "warm neutral palette with one saturated accent",
    "G-ECO": "sand and cream palette with one deep-green accent",
}
# ── R6 G-CMP 六瓦句式 ──
CMP_SUBJECTS = [
    "one card split by a clean rule: left a dissolving stopwatch shape, right a queue of small clocks",
    "two cards side by side on the same surface: a tidy subscription card against a heap of coins",
    "one card torn in half: the left half crisp and sharp, the right half blurred",
    "one card showing a lone cursor on the left and a synced team of cursors on the right",
    "two stacked cards: a cleared-rights seal on top, a caution triangle below",
    "one wide card: a row of separate tool cards on the left, one unified canvas card on the right",
]

def build_gal(set_id, lane, bg, subject, tile):
    cam, fill = CAM6[tile - 1]
    if lane == "L4":
        head = (f"Editorial flat-graphic composition on a Swiss grid, paper grain texture with "
                f"riso-print ink edges, flat poster layout with no photographic perspective, "
                f"flat even lighting, {L4_PAL[set_id]}")
    elif lane == "L5":
        head = (f"Macro still-life photograph with raking side light revealing tactile texture, "
                f"100mm macro, {L5_PAL[set_id]}")
    elif lane == "L1":
        head = (f"High-end commercial photograph, 85mm shallow depth of field, soft key light, "
                f"{L1_PAL[set_id]}")
    elif lane == "L2":
        head = ("Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette "
                "with no additional accent color, soft volumetric light with subtle film grain")
    elif lane == "L3":
        head = ("Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral "
                "accent, macro 50mm look, soft key light with gentle contact shadows")
    else:
        raise ValueError(lane)
    return (f"{head}, one subject only: {subject}, {cam}, plain seamless backdrop in one flat "
            f"{bg} tone, hero fills about {fill}% of frame, bottom 25% clean for label scrim, "
            f"locked seed and style reference shared across all six tiles, 1:1, "
            f"no text, no letters, no watermark")

# ── R7/R8 split 补丁（prompt 片段替换）──
SPLIT_PATCHES = {
    "S-AVA": [("85mm shallow depth of field, seamless paper backdrop",
               "85mm shallow depth of field, soft key light from the upper left with gentle shadows, seamless paper backdrop")],
    "S-PED": [("85mm shallow depth of field, 4:3",
               "85mm shallow depth of field, soft directional daylight from the left casting one crisp shadow along the tear, 4:3")],
    "S-IND": [("85mm shallow depth of field, the board fills",
               "85mm shallow depth of field, soft ambient studio light with a warm accent from the right, the board fills")],
    "S-CRE": [("85mm shallow depth of field, seamless paper backdrop",
               "85mm shallow depth of field, soft studio key light from the front-left with gentle shadows, seamless paper backdrop")],
    "S-FAS": [("85mm shallow depth of field, seamless paper backdrop",
               "85mm shallow depth of field, soft window light from the side casting gentle fabric shadows, seamless paper backdrop")],
    "S-ADS": [("precise alignment, the hero silhouette",
               "precise alignment, flat poster layout with no photographic perspective, the hero silhouette")],
    "S-CMP": [("2-3 color palette, hero contrast fills",
               "2-3 color palette, flat poster layout with no photographic perspective, hero contrast fills")],
    "S-WEB": [("soft daylight casting real paper shadows, cream and sage palette",
               "low macro angle, soft daylight casting real paper shadows, cream and sage palette")],
    "S-EDU": [("warm daylight, hero fills",
               "warm daylight, shot at a low macro angle, hero fills")],
}

def patch_p1():
    p = D / "p1-batch.jsonl"
    recs = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    n = 0
    for r in recs:
        # R9 C-PLA 等效焦段
        if r["id"] == "C-PLA":
            old = "macro-soft HDRI lighting with gentle contact shadows, 16:10"
            new = ("macro-soft HDRI lighting with gentle contact shadows, rendered at an "
                   "equivalent 50mm perspective, 16:10")
            assert old in r["prompt"]
            r["prompt"] = r["prompt"].replace(old, new); n += 1
        # R2 mosaic 机位递进
        if r["variant"] == "hero-mosaic" and "tile" in r:
            tile = r["tile"]
            old = "locked seed and style reference shared across all four tiles"
            new = f"{CAM4[tile-1]}, locked seed and style reference shared across all four tiles"
            if old in r["prompt"]:
                r["prompt"] = r["prompt"].replace(old, new); n += 1
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
    print(f"p1-batch.jsonl: {len(recs)} 条，修补 {n} 处")

def patch_p2():
    p = D / "p2-batch.jsonl"
    recs = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    n_split = n_gal = 0
    for r in recs:
        if r["variant"] == "hero-split" and r["id"] in SPLIT_PATCHES:
            for old, new in SPLIT_PATCHES[r["id"]]:
                if old in r["prompt"]:
                    r["prompt"] = r["prompt"].replace(old, new); n_split += 1
                else:
                    print(f"  ! 未命中 {r['id']}: {old[:40]}")
        if r["variant"] == "hero-gallery":
            sid = r["id"].rsplit("-", 1)[0]
            tile = r["tile"]
            lane = r["lane"].split("-")[0]
            bg = r["prompt"].split("one flat ")[-1].split(" tone")[0]
            # 主体：G-CMP 用新句式，其余取原 subject
            if sid == "G-CMP":
                subject = CMP_SUBJECTS[tile - 1]
            else:
                subject = r["prompt"].split("one subject only: ")[1].split(", plain seamless")[0]
            r["prompt"] = build_gal(sid, lane, bg, subject, tile)
            n_gal += 1
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
    print(f"p2-batch.jsonl: {len(recs)} 条，split 修补 {n_split} 处，gallery 重建 {n_gal} 条")

if __name__ == "__main__":
    patch_p1()
    patch_p2()
