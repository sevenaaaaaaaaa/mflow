#!/usr/bin/env python3
"""tmp_gen_queue.py — 汇总三批 brief → 按执行顺序输出 generate-queue.jsonl + NEXT-STEPS.md"""
import json
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")

def load(name):
    p = D / name
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

p0 = load("p0-batch-v2.jsonl")
p1 = load("p1-batch.jsonl")
p2 = load("p2-batch.jsonl")

# ── 执行顺序 ──
GAL_ORDER = ["G-PRT", "G-SOC", "G-ECO", "G-LOG", "G-VID",
             "G-IMG", "G-DOC", "G-ADS", "G-CMP", "G-PLA"]

split_p2 = [r for r in p2 if r["variant"] == "hero-split"]
gal_p2 = [r for r in p2 if r["variant"] == "hero-gallery"]
cine = [r for r in p1 if r["variant"] == "hero-cinematic"]
mos = [r for r in p1 if r["variant"] == "hero-mosaic"]

def gal_set_key(r):
    return r["id"].rsplit("-", 1)[0]

queue = []
def add(recs, step, step_name, note=""):
    for r in recs:
        q = dict(r)
        q["step"] = step
        q["step_name"] = step_name
        q["order"] = len(queue) + 1
        if note:
            q["step_note"] = note
        queue.append(q)

add(p0, 1, "P0 止血", "上线后替换 83c980ae.jpg 死链引用")
add(cine, 2, "P1 品牌旗舰 cinematic", "lovart-2-0 / landing-full / 行业方案首屏")
add(mos, 3, "P1 分步叙事 mosaic", "每套 4 瓦同一会话连出 + 锁 seed")
add(split_p2, 4, "P2 其余主题族 split")
for sid in GAL_ORDER:
    grp = [r for r in gal_p2 if gal_set_key(r) == sid]
    add(grp, 5, f"P2 gallery · {sid}", "同套 6 瓦同一会话 + 锁 seed + 同背景色")

assert len(queue) == 93, len(queue)
(D / "generate-queue.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in queue) + "\n", encoding="utf-8")

# ── 风格定调小样（6 航道 × 3 候选）──
SHEETS = {
    "L1-photo-editorial": [
        ("A 柔和棚拍", "High-end commercial photograph of one matte ceramic cup on a sand-colored seamless surface, 85mm, soft key light from upper left with a gentle falloff shadow, warm sand and cream palette with one deep-green accent, calm and premium, 1:1, no text, no letters, no watermark"),
        ("B 硬光 editorial", "High-end editorial photograph of one matte ceramic cup on a bone-white surface, 85mm, single hard directional light creating a crisp long shadow, warm neutral palette with one saturated accent, confident and graphic, 1:1, no text, no letters, no watermark"),
        ("C 窗光生活方式", "High-end lifestyle photograph of one matte ceramic cup on a linen cloth by a window, 85mm, soft diffused daylight with natural falloff, warm neutral palette with one muted accent, quiet and human, 1:1, no text, no letters, no watermark"),
    ],
    "L2-cinematic-still": [
        ("A 暖调胶片", "Cinematic still of one glass bottle on a dark desk, shot on 35mm film, single warm volumetric light from a window with soft haze, teal-and-amber palette, shallow depth of field, subtle film grain, 1:1, no text, no letters, no watermark"),
        ("B 冷调夜戏", "Cinematic still of one glass bottle on a dark desk, shot on 35mm film, moonlit blue key with one practical amber rim light, desaturated cool palette, deep shadows, anamorphic feel, 1:1, no text, no letters, no watermark"),
        ("C 高反差单光源", "Cinematic still of one glass bottle on a dark desk, shot on 35mm film, one narrow hard light source from the side, near-monochrome with one warm highlight, dramatic contrast, 1:1, no text, no letters, no watermark"),
    ],
    "L3-soft-3d": [
        ("A 哑光陶土", "Soft-body 3D render of one matte clay cup on a warm-grey seamless backdrop, macro 50mm, soft key light with gentle contact shadow, warm-grey palette with one coral accent, tactile and calm, 1:1, no text, no letters, no watermark"),
        ("B 圆润塑料 + 大阴影", "Soft-body 3D render of one rounded matte plastic cup on a pale sand backdrop, macro 50mm, soft top light casting one large soft shadow, muted palette with one electric accent, playful and clean, 1:1, no text, no letters, no watermark"),
        ("C 纸感材质", "Soft-body 3D render of one paper-textured cup on an off-white backdrop, macro 50mm, gentle HDRI light with fine surface fibers visible, ivory palette with one ink accent, crafted and quiet, 1:1, no text, no letters, no watermark"),
    ],
    "L4-graphic-flat": [
        ("A 瑞士网格静物", "Editorial flat-graphic composition of one abstract cup silhouette on a cream field, Swiss grid alignment, paper grain texture with riso-print ink edges, cream and coral with charcoal accent, precise and restrained, 1:1, no text, no letters, no watermark"),
        ("B 大色块几何", "Editorial flat-graphic composition of one abstract cup shape built from two bold geometric blocks, cream field with a strong diagonal shadow shape, riso texture, 2-color palette, confident and poster-like, 1:1, no text, no letters, no watermark"),
        ("C 拼贴纸感", "Editorial flat-graphic collage of one abstract cup assembled from torn paper pieces, ivory field, visible fiber and deckle edges, muted palette with one saturated accent, handmade and editorial, 1:1, no text, no letters, no watermark"),
    ],
    "L5-material-still-life": [
        ("A 棉纸烫金", "Macro still-life photograph of one cotton-paper card with an embossed abstract shape and a foil edge, raking side light revealing texture, ivory and charcoal with one copper accent, precise cast shadow, 1:1, no text, no letters, no watermark"),
        ("B 黑胶哑面", "Macro still-life photograph of one vinyl record half out of a matte sleeve, raking side light on the groove, charcoal and ivory with one copper accent, deep shadows, 1:1, no text, no letters, no watermark"),
        ("C 陶土与铜", "Macro still-life photograph of one matte clay tile beside a copper strip on a stone surface, raking side light, warm grey and copper palette, tactile and quiet, 1:1, no text, no letters, no watermark"),
    ],
    "L6-paper-craft": [
        ("A 分层纸雕", "Layered paper-craft diorama of one simple house shape in three depth layers, hand-cut paper edges, soft daylight casting real shadows, cream and sage with one coral accent, 1:1, no text, no letters, no watermark"),
        ("B 白纸极简", "Layered paper-craft diorama of one simple house shape in white paper on a white background, hand-cut edges with soft real shadows, near-monochrome with one grey shadow accent, minimal and architectural, 1:1, no text, no letters, no watermark"),
        ("C 彩色手作", "Layered paper-craft diorama of one simple house shape in warm colored paper layers, hand-cut edges, playful daylight shadows, warm palette with one contrasting accent, cheerful and crafted, 1:1, no text, no letters, no watermark"),
    ],
}

lines = []
lines.append("# 生成队列（NEXT STEPS）· 99 个生成任务\n")
lines.append("> 投喂文件：`generate-queue.jsonl`（93 条，含 `order` / `step` / `step_name` 字段，按序执行）")
lines.append("> 单任务字段：id / step / order / variant / lane / w / h / ratio / prompt / alt")
lines.append("> 本文档只做执行说明与顺序，prompt 正文以 jsonl 为准。\n")
lines.append("---\n")

lines.append("## Step 0 · 风格定调（18 个候选，必做前置）\n")
lines.append("目的：为 6 条航道各选 1 张**风格参考图**并冻结。此后该航道所有生成都带这张参考图，风格决策与单张 prompt 解耦——这是解决\"丑/过时\"的关键动作。\n")
lines.append("做法：每条航道 3 个候选（A/B/C）各生成 1 次，统一 1:1 / 同一测试主体（一个哑光杯子），横向对比后选 1 张。**选定后把该图存为 `style/{lane}.png`，后续生成作为 style reference 附上。**\n")
for lane, cands in SHEETS.items():
    lines.append(f"### {lane}\n")
    for name, prompt in cands:
        lines.append(f"- **{name}**")
        lines.append(f"  `{prompt}`")
    lines.append("")

lines.append("---\n")
lines.append("## 正式生成（93 张，按 step 顺序）\n")

step_meta = {}
for r in queue:
    step_meta.setdefault((r["step"], r["step_name"]), []).append(r)

ORDER_NOTE = {
    1: ("P0 止血", "6 张 split。**上线优先级最高**：`83c980ae.jpg` 已在 CDN 404，65 处引用全坏。出图后立即替换。"),
    2: ("P1 品牌旗舰 cinematic", "5 张 16:10。用于 lovart-2-0、landing-full、zh-enterprise、行业方案等视觉权重最高的首屏。"),
    3: ("P1 分步叙事 mosaic", "8 张 4:3。两套各 4 瓦，必须同一会话连出 + 锁 seed。"),
    4: ("P2 其余主题族 split", "14 张 4:3。补齐除 6 大流量族外的全部主题族。"),
    5: ("P2 gallery 10 套", "60 张 1:1。按套跑，每套 6 瓦同一会话 + 锁 seed + 同背景色；套间顺序见下。"),
}

for (step, name), recs in sorted(step_meta.items()):
    note = ORDER_NOTE[step][1]
    lines.append(f"### Step {step} · {name}（{len(recs)} 张）\n")
    lines.append(f"{note}\n")
    if step == 5:
        cur = None
        for r in recs:
            sid = r["id"].rsplit("-", 1)[0]
            if sid != cur:
                cur = sid
                bg = r["prompt"].split("one flat ")[-1].split(" tone")[0] if "one flat " in r["prompt"] else "-"
                lines.append(f"- **{sid}**（{r['theme']}，背景 {bg}，覆盖 {r['pages']} 页）：{', '.join(x['label'] for x in recs if x['id'].startswith(sid + '-'))}")
    else:
        for r in recs:
            lines.append(f"- `{r['id']}` · {r['theme']} · {r['ratio']} · 覆盖 {r.get('pages', '-')} 页")
    lines.append("")

lines.append("---\n")
lines.append("## Gallery 套间建议顺序（为什么这么排）\n")
lines.append("1. **G-PRT** 先跑 —— 覆盖 58 个 zh-topic 页影响面最大，且 L5 材质静物最接近站内已有成功画风，风险最低、验证效果最好。")
lines.append("2. **G-SOC / G-ECO** —— 中文站点流量集中，且 L4/L1 已过 style sheet 验证。")
lines.append("3. **G-LOG / G-VID / G-IMG** —— 英文主力页，L5/L2/L1。")
lines.append("4. **G-DOC / G-ADS / G-CMP / G-PLA** —— L4 占比高，最后跑，便于统一调整 L4 航道参考图。\n")
lines.append("> 若 L4 首套（G-SOC）出图气质与站内摄影风 hero 差异过大，暂停其余 L4 四套，先调 style sheet 再继续。\n")

lines.append("## 交付与验收\n")
lines.append("| 项 | 要求 |")
lines.append("|---|---|")
lines.append("| 命名 | `hero-{variant}-{theme}-v1.{ext}`，瓦片加 `-t1…t6` |")
lines.append("| 尺寸 | split 2160×1620 · cinematic 2400×1500 · mosaic 瓦 1200×900 · gallery 瓦 1200×1200 |")
lines.append("| 体积 | ≤1.5MB（JPG q85 或 PNG 优化） |")
lines.append("| 图内文字 | 零。含乱码 UI 文字即废稿 |")
lines.append("| 安全区 | 四边 ≥5% 裁切余量；mosaic 下方 30% / gallery 下方 25% 保持低细节 |")
lines.append("| 同套一致 | gallery/mosaic 一套内背景色、光向、色彩完全一致 |")
lines.append("| 随图交付 | alt 文案（jsonl 已给）+ 中文页面用中文 alt |\n")

(D / "NEXT-STEPS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"generate-queue.jsonl: {len(queue)} 条")
print(f"NEXT-STEPS.md: {len(lines)} 行")
print("step 分布:", {k: len(v) for k, v in sorted(step_meta.items())})
