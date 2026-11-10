#!/usr/bin/env python3
"""tmp_gen_per_entry_md.py — 每条 brief 生成一个独立 .md 文件

输出：
  briefs/<分组>/<ID>.md         ← 397 条，每条一份
  briefs/00-INDEX.md            ← 全量索引
"""
import json, re
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
ROOT = D / "briefs"
if ROOT.exists():
    import shutil
    shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)


def load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def slug(s):
    return re.sub(r"[^-a-z0-9]+", "-", s.lower()).strip("-") or "item"


GROUPS = []


def add_group(dirname, title, records, meta_fn):
    GROUPS.append(dict(dir=dirname, title=title, recs=records, meta=meta_fn))


# ── 1 hero-split ──
A = load(D / "module-A-split.jsonl")
A.sort(key=lambda r: (0 if r["priority"] == "P0" else 1, -r.get("pages", 0)))
add_group("01-hero-split", "hero-split · 左文右图（20 张）", A, lambda r: {
    "variant": "hero-split", "size": "2160 × 1620", "ratio": "4:3",
    "field": "段首 `media.src`",
    "rules": ["视觉重心落在中右 60%（左侧是页面文案栏）",
              "主体完整，四边 ≥5% 裁切余量（圆角卡片渲染）",
              "主视觉 ×1 + 支撑元素 ≤2 + 背景处理 ×1；禁止画任何界面"],
})

# ── 2 hero-cinematic ──
B = load(D / "module-B-cinematic.jsonl")
add_group("02-hero-cinematic", "hero-cinematic · 全宽剧院图（5 张）", B, lambda r: {
    "variant": "hero-cinematic", "size": "2400 × 1500", "ratio": "16:10",
    "field": "段首 `media.src`",
    "rules": ["三层深度（前 / 中 / 后），每层最多 1 个主元素",
              "上下各 8% 渐隐过渡，与页面背景衔接",
              "文字全在图外；图内不烧录任何文案"],
})

# ── 3 hero-mosaic ──
C = load(D / "module-C-mosaic.jsonl")
add_group("03-hero-mosaic", "hero-mosaic · 4 瓦拼贴（8 张 / 2 套）", C, lambda r: {
    "variant": "hero-mosaic", "size": "1200 × 900", "ratio": "4:3",
    "field": "`mosaicTiles[].media.src`",
    "rules": ["4 瓦 = 同一主体的 4 个连续状态（时间轴叙事）",
              "每瓦下方 30% 保持低细节供标题叠加",
              "**同一会话连续生成 + 锁 seed + 同风格参考**"],
})

# ── 4 gallery media ──
Dm = load(D / "batches" / "D1-media.jsonl")
add_group("04-gallery-media", "gallery · 品类总览主图（18 张）", Dm, lambda r: {
    "variant": "hero-gallery", "size": "2160 × 1350", "ratio": "16:10",
    "field": "`media.src`（页面主图，非瓦片）",
    "rules": ["每品类一张总览，建立该品类的视觉基调",
              "主体 + 少量辅件，为整个品类的瓦片定调"],
})

# ── 5 gallery tiles (主力 6 行业) ──
tiles = load(D / "module-D-gallery.jsonl")
tiles = [r for r in tiles if r["field"] == "gallery"]
add_group("05-gallery-tiles", "gallery · 行业瓦片 · 6 主力行业（108 张）", tiles, lambda r: {
    "variant": "hero-gallery", "size": "1200 × 1200", "ratio": "1:1",
    "field": "`gallery[].img`",
    "rules": ["每瓦 = 单对象，底部 25% 留 label 遮罩",
              "同品类 6 张必须同会话 + 锁 seed + 同背景色，只换行业",
              "机位按瓦片序号互斥：正视 / 侧角 / 微距 / 俯拍 / 低角度 / 侧轮廓"],
})

# ── 6 gallery tools ──
tools = load(D / "batches" / "D3-tools.jsonl")
add_group("06-gallery-tools", "gallery · 工具瓦片（28 张）", tools, lambda r: {
    "variant": "hero-gallery", "size": "1200 × 1200", "ratio": "1:1",
    "field": "`toolTiles[].media.src`",
    "rules": ["6 瓦套 ×4 + 4 瓦套 ×1（后者 11 语言共用同一套图）",
              "每套同会话 + 锁 seed"],
})

# ── 7 b2b industries ──
b2b = [r for r in load(D / "module-D-gallery-b2b4.jsonl") if r["field"] == "gallery"]
add_group("07-b2b-industries", "gallery · 行业瓦片 · 4 个 B 端行业（72 张）", b2b, lambda r: {
    "variant": "hero-gallery", "size": "1200 × 1200", "ratio": "1:1",
    "field": "`gallery[].img`",
    "rules": ["行业：房地产 / 教育培训 / 医疗健康 / 金融保险",
              "**必须紧接同品类的 05 批在同会话内跑完**，否则同品类会分裂成两套视觉语言",
              "每瓦 = 单对象，底部 25% 留 label 遮罩"],
})

# ── 8 extra industries ──
ex = [r for r in load(D / "module-D-gallery-rest2.jsonl") if r["field"] == "gallery"]
add_group("08-extra-industries", "gallery · 行业瓦片 · 剩余 2 行业（36 张）", ex, lambda r: {
    "variant": "hero-gallery", "size": "1200 × 1200", "ratio": "1:1",
    "field": "`gallery[].img`",
    "rules": ["行业：商旅出行 / 文化创意",
              "接在同品类的 07 批之后同会话跑完",
              "每瓦 = 单对象，底部 25% 留 label 遮罩"],
})

# ── 9 journey media ──
jm = load(D / "batches" / "E4-journey-media.jsonl")
add_group("09-journey-media", "hero-journey · 场景大图（7 张）", jm, lambda r: {
    "variant": "hero-journey", "size": "2160 × 1350", "ratio": "16:10",
    "field": "`media.src`",
    "rules": ["step 卡片图标由代码渲染，无需出图；只需这张场景大图",
              "13 个 journey 页面按语义去重为 7 个场景",
              "上下各 8% 渐隐"],
})

# ── 10 cinematic video ──
vid = load(D / "E5-cinematic-video.jsonl")
add_group("10-cinematic-video", "hero-cinematic · 视频版（5 条）", vid, lambda r: {
    "variant": "hero-cinematic", "size": "2400 × 1500", "ratio": "16:10 · 8s 循环",
    "field": "`media.src`（type: video）",
    "rules": ["与 02 批对应静帧**同构图**，静帧作 poster",
              "8 秒、循环、无音轨、≤8MB",
              "iOS 自动播放必须静音"],
})

# ── 11-22 modules ──
MOD_TYPES = {
    "bento-2": ("11-bento-2", "bento-2 · 两栏特性卡"),
    "bento-4": ("12-bento-4", "bento-4 · 2×2 四宫格"),
    "bento-6": ("13-bento-6", "bento-6 · 六卡 bento"),
    "feature-detail": ("14-feature-detail", "feature-detail · 图文左右交错"),
    "capability-tabs": ("15-capability-tabs", "capability-tabs · Tab 大内容区"),
    "canvas-wall": ("16-canvas-wall", "canvas-wall · 10 卡画布墙"),
    "workflow-horizontal": ("17-workflow-horizontal", "workflow-horizontal · 横向 N 步流程"),
    "showcase-stacked": ("18-showcase", "showcase · 前後堆叠 / 横向滚动"),
    "comparison-before-after": ("19-comparison-before-after", "comparison-before-after · 前后对比"),
    "media-marquee": ("20-media-marquee", "media-marquee · 媒体跑马灯"),
    "portrait-grid": ("21-portrait-grid", "portrait-grid · 方形 / 竖版卡"),
    "tool-grid": ("22-tool-grid-blog-grid", "tool-grid / blog-grid · 工具卡与文章网格"),
}
modrecs = load(D / "modules" / "module-prompts.jsonl")
by_type = {}
for r in modrecs:
    key = r["stype"].split(" / ")[0]
    if key == "showcase-stacked":
        key = "showcase-stacked"
    if key == "portrait-grid-3":
        key = "portrait-grid"
    by_type.setdefault(key, []).append(r)

for key, (dname, title) in MOD_TYPES.items():
    rows = by_type.get(key, [])
    if not rows:
        continue
    add_group(dname, f"{title}（{len(rows)} 条）", rows, lambda r: {
        "variant": r["stype"], "size": r.get("ratio", ""), "ratio": r.get("ratio", ""),
        "field": r.get("field", ""),
        "rules": ["同页面同模块的多张图必须同会话 + 锁 seed + 同风格参考，只换对象",
                  "图内零可读字符；如含排版，用抽象灰色条块表达层级"],
    })

# ── 渲染 ──
index_rows = []
total = 0
for g in GROUPS:
    gd = ROOT / g["dir"]
    gd.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(g["recs"], 1):
        meta = g["meta"](r)
        rid = r["id"]
        fname = f"{i:03d}-{slug(rid)}.md"
        label = r.get("label") or r.get("theme_label") or r.get("theme") or ""
        ind = r.get("industry", "")
        lines = [f"# {rid}" + (f" · {label}" if label else "") + (f" · {ind}" if ind else "") + "\n"]
        lines.append("| 项 | 值 |")
        lines.append("|---|---|")
        lines.append(f"| ID | `{rid}` |")
        lines.append(f"| 分组 | {g['title']} |")
        lines.append(f"| section type | `{meta['variant']}` |")
        lines.append(f"| 来源字段 | {meta['field']} |")
        lines.append(f"| 尺寸 | {meta['size']} |")
        lines.append(f"| 比例 | {meta['ratio']} |")
        if label:
            lines.append(f"| 主题 / 品类 | {label} |")
        if ind:
            lines.append(f"| 行业 | {ind} |")
        if r.get("lane"):
            lines.append(f"| 风格航道 | `{r['lane']}` |")
        if r.get("priority"):
            lines.append(f"| 优先级 | {r['priority']} |")
        if r.get("pages"):
            lines.append(f"| 覆盖页面 | 约 {r['pages']} 页 |")
        if r.get("tile"):
            lines.append(f"| 瓦片序号 | {r['tile']} |")
        if r.get("duration_s"):
            lines.append(f"| 时长 | {r['duration_s']}s 循环 |")
        lines.append("")
        if r.get("notes"):
            lines.append(f"> {r['notes']}\n")
        lines.append("## Prompt\n")
        lines.append("```text")
        lines.append(r["prompt"])
        lines.append("```\n")
        lines.append("## Alt 文案\n")
        alt = r.get("alt") or f"Lovart {label} — {meta['variant']} visual"
        lines.append(f"`{alt}`\n")
        lines.append("## 本模块纪律\n")
        for rule in meta["rules"]:
            lines.append(f"- {rule}")
        lines.append("")
        lines.append("## 交付\n")
        lines.append("| 项 | 要求 |")
        lines.append("|---|---|")
        lines.append(f"| 命名 | `{slug(rid)}-v1.png` |")
        lines.append("| 体积 | ≤1.5MB（视频 ≤8MB） |")
        lines.append("| 图内文字 | 零。含可读字符即废稿 |")
        lines.append("| 安全区 | 四边 ≥5% 裁切余量 |")
        (gd / fname).write_text("\n".join(lines) + "\n", encoding="utf-8")
        total += 1
        index_rows.append((g["title"], g["dir"], fname, rid, label, ind, meta["ratio"]))

# 分组索引
for g in GROUPS:
    gd = ROOT / g["dir"]
    idx = [f"# {g['title']}\n", f"> 本组 {len(g['recs'])} 条，每条一个独立的 .md 文件。\n",
           "| # | 文件 | ID | 主题 / 品类 | 行业 |", "|---:|---|---|---|---|"]
    for i, r in enumerate(g["recs"], 1):
        label = r.get("label") or r.get("theme_label") or r.get("theme") or "—"
        ind = r.get("industry", "—")
        idx.append(f"| {i} | [{i:03d}-{slug(r['id'])}.md]({i:03d}-{slug(r['id'])}.md) | `{r['id']}` | {label} | {ind} |")
    (gd / "_INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")

# 总索引
o = ["# Brief 全集 · 每条一份 .md\n",
     f"> 共 **{total}** 条，每条 brief 一个独立 Markdown 文件。",
     "> 每个分组目录内另有 `_INDEX.md` 列出本组全部文件。\n",
     "| 分组 | 目录 | 条数 | section type |", "|---|---|---:|---|"]
seen = {}
for g in GROUPS:
    st = g["meta"](g["recs"][0])["variant"] if g["recs"] else "—"
    o.append(f"| {g['title']} | [`{g['dir']}/`]({g['dir']}/_INDEX.md) | {len(g['recs'])} | `{st}` |")
    seen[g["dir"]] = len(g["recs"])
o.append(f"| **合计** | | **{total}** | |")
o.append("")
o.append("## 通用交付规范\n")
o.append("| 项 | 要求 |")
o.append("|---|---|")
o.append("| 图内文字 | 零。含可读字符即废稿；含排版的模块用抽象灰色条块表达层级 |")
o.append("| 多语言 | 同页面 10–11 语言版本共用同一套图，按模块做、不按语言做 |")
o.append("| 安全区 | 四边 ≥5% 裁切余量 |")
o.append("| 体积 | JPG q85 或优化 PNG ≤1.5MB（视频 ≤8MB） |")
o.append("| 禁用元素 | 紫蓝渐变 / 玻璃拟态 / 悬浮 3D 球 / 等距插画 / 光轨 / floating chips |")
o.append("")
o.append("## 同批一致铁律\n")
o.append("1. 同品类 / 同模块的多张图**同一会话连续生成**")
o.append("2. **锁 seed + 同一风格参考图**")
o.append("3. `05-gallery-tiles` → `07-b2b-industries` → `08-extra-industries` **同品类连着跑**")
o.append("4. mosaic 每套 4 瓦、gallery 每套 6 瓦同理")
(ROOT / "00-INDEX.md").write_text("\n".join(o) + "\n", encoding="utf-8")

print(f"生成 {total} 个 .md 文件，{len(GROUPS)} 个分组目录")
for g in GROUPS:
    print(f"  {g['dir']:<28} {len(g['recs']):>3} 条")
