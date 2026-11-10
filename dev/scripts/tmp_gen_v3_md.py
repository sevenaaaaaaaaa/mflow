#!/usr/bin/env python3
"""tmp_gen_v3_md.py — 把 V3 全量 JSONL 渲染成 md（每条一份 + 分组索引）"""
import json, re, shutil
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
V3 = D / "v3"
ROOT = V3 / "md"
if ROOT.exists():
    shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)

ANCHOR_NOTE = ("**三层锚定**：材质真实（可触摸的表面肌理）· 单一焦点（只有 1 个视觉重心）· "
               "克制配色（低饱和底 + 至多 1 个点睛色）")


def load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def slug(s):
    return re.sub(r"[^-a-z0-9]+", "-", s.lower()).strip("-") or "item"


GROUPS = [
    ("01-split", "hero-split · 左文右图（20 条）", "A-split.jsonl", "hero-split",
     "2160 × 1620", "4:3", "段首 `media.src`",
     ["视觉重心落在中右 60%（左侧是页面文案栏）", "四边 ≥5% 裁切余量（圆角卡片渲染）",
      "主视觉 ×1 + 支撑元素 ≤2 + 背景 ×1；禁止画界面"]),
    ("02-cinematic", "hero-cinematic · 全宽剧院图（5 条）", "B-cinematic.jsonl", "hero-cinematic",
     "2400 × 1500", "16:10", "段首 `media.src`",
     ["三层深度（前 / 中 / 后），每层最多 1 个主元素", "上下各 8% 渐隐过渡",
      "文字全在图外"]),
    ("03-mosaic", "hero-mosaic · 4 瓦拼贴（8 条）", "C-mosaic.jsonl", "hero-mosaic",
     "1200 × 900", "4:3", "`mosaicTiles[].media.src`",
     ["4 瓦 = 同一主体的 4 个连续状态", "下方 30% 低细节供标题叠加",
      "**同一会话 + 锁 seed + 同风格参考**"]),
    ("04-gallery-media", "gallery · 品类总览主图（18 条）", "D-media.jsonl", "hero-gallery",
     "2160 × 1350", "16:10", "`media.src`",
     ["每品类一张总览，建立品类视觉基调", "三层锚定必须完整"]),
    ("05-gallery-tiles", "gallery · 行业瓦片（216 条 / 18 品类 × 12 行业）", "D-tiles.jsonl",
     "hero-gallery", "1200 × 1200", "1:1", "`gallery[].img`",
     ["每瓦 = 单对象，下方 25% 留 label 遮罩", "同品类 12 张同会话 + 锁 seed",
      "12 机位互斥", "材质 / 布光 / 场景 / 瞬间四层变量轮转"]),
    ("06-gallery-tools", "gallery · 工具瓦片（28 条）", "D-tools.jsonl", "hero-gallery",
     "1200 × 1200", "1:1", "`toolTiles[].media.src`",
     ["6 瓦套 ×4 + 4 瓦套 ×1", "每套同会话 + 锁 seed"]),
    ("07-journey", "hero-journey · 场景大图（7 条）", "E4-journey.jsonl", "hero-journey",
     "2160 × 1350", "16:10", "`media.src`",
     ["step 卡片图标由代码渲染，只做这张场景大图", "上下各 8% 渐隐"]),
    ("08-video", "hero-cinematic · 视频版（5 条）", "E5-video.jsonl", "hero-cinematic",
     "2400 × 1500", "16:10 · 8s", "`media.src`（type: video）",
     ["与静帧同构图，静帧作 poster", "8s 循环无音轨 ≤8MB"]),
    ("09-modules", "落地页模块配图（90 条）", "modules.jsonl", "多模块",
     "按模块", "按模块", "各模块自有字段",
     ["同页面同模块多张图必须同会话 + 锁 seed", "含排版模块用抽象灰色条块表达层级"]),
]

index = []
total = 0
for dname, title, fname, stype, size, ratio, field, rules in GROUPS:
    src = V3 / fname
    if not src.exists():
        continue
    recs = load(src)
    gd = ROOT / dname
    gd.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(recs, 1):
        rid = r["id"]
        fn = f"{i:03d}-{slug(rid)}.md"
        label = r.get("label") or r.get("theme_label") or r.get("theme") or ""
        ind = r.get("industry", "")
        head = f"# {rid}"
        if label:
            head += f" · {label}"
        if ind:
            head += f" · {ind}"
        L = [head + "\n"]
        L += ["| 项 | 值 |", "|---|---|",
              f"| ID | `{rid}` |",
              f"| 分组 | {title} |",
              f"| section type | `{r.get('variant', stype)}` |",
              f"| 来源字段 | {field} |",
              f"| 尺寸 | {size} |",
              f"| 比例 | {ratio} |"]
        if label:
            L.append(f"| 主题 / 品类 | {label} |")
        if ind:
            L.append(f"| 行业 | {ind} |")
        if r.get("lane"):
            L.append(f"| 风格航道 | `{r['lane']}` |")
        if r.get("priority"):
            L.append(f"| 优先级 | {r['priority']} |")
        if r.get("pages"):
            L.append(f"| 覆盖页面 | 约 {r['pages']} 页 |")
        if r.get("tile"):
            L.append(f"| 瓦片序号 | {r['tile']} |")
        L.append("")
        if r.get("notes"):
            L.append(f"> {r['notes']}\n")
        L += ["## Prompt（V3）\n", "```text", r["prompt"], "```\n",
              "## Alt 文案\n",
              f"`{r.get('alt') or ('Lovart ' + str(label) + ' — visual')}`\n",
              "## 风格锚定\n", ANCHOR_NOTE + "\n",
              "## 本模块纪律\n"]
        L += [f"- {x}" for x in rules]
        L += ["", "## 交付\n", "| 项 | 要求 |", "|---|---|",
              f"| 命名 | `{slug(rid)}-v1.png` |",
              "| 体积 | ≤1.5MB（视频 ≤8MB） |",
              "| 图内文字 | 零。含可读字符即废稿 |",
              "| 安全区 | 四边 ≥5% 裁切余量 |", ""]
        (gd / fn).write_text("\n".join(L) + "\n", encoding="utf-8")
        total += 1
    # 分组索引
    idx = [f"# {title}\n", f"> 共 {len(recs)} 条，每条一个独立 .md\n",
           "| # | 文件 | ID | 标签 | 行业 |", "|---:|---|---|---|---|"]
    for i, r in enumerate(recs, 1):
        lab = r.get("label") or r.get("theme_label") or r.get("theme") or "—"
        idx.append(f"| {i} | [{i:03d}-{slug(r['id'])}.md]({i:03d}-{slug(r['id'])}.md) | "
                   f"`{r['id']}` | {lab} | {r.get('industry','—')} |")
    (gd / "_INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    index.append((title, dname, len(recs)))

# 总索引
o = ["# V3 Brief 全集 · 每条一份 md\n",
     f"> 共 **{total}** 条。体系见 [`prompt-v3-premium-agentic.md`](../prompt-v3-premium-agentic.md)",
     "> 与 V2 的差异：三层锚定 + 四层变量 + agent 物理隐喻\n",
     "| 分组 | 目录 | 条数 |", "|---|---|---:|"]
for t, d, n in index:
    o.append(f"| {t} | [`{d}/`]({d}/_INDEX.md) | {n} |")
o.append(f"| **合计** | | **{total}** |")
o += ["", "## V3 三层锚定（全站不变）\n",
      "| 锚点 | 定义 |", "|---|---|",
      "| A1 材质真实 | 必须有可见纤维 / 毛孔 / 磨损 / 厚度，禁止 CGI 塑料感 |",
      "| A2 单一焦点 | 只有 1 个视觉重心，其余元素降到 20% 权重以下 |",
      "| A3 克制配色 | 低饱和打底 + 至多 1 个点睛，点睛面积 <8% |",
      "", "## V3 四层变量（同组内放开）\n",
      "| 变量 | 取值 |", "|---|---|",
      "| V1 机位 | 正视 / 3-4 侧角 / 微距 / 正俯 / 低角度 / 侧剖面 / 偏心留白 / 出血 / 对角轴 / 前景切入 |",
      "| V2 叙事瞬间 | 静止陈列 / 成形中 / 半完成 / 刚交付 / 使用中 / 归档 |",
      "| V3 材质 | 水彩纸 / 亚麻 / 阳极氧化铝 / 陶土 / 大理石 / 绒面革 / 青铜 / 硫酸纸 / 丝网印 / 橡木 |",
      "| V4 场景 | 工作室 / 印刷工坊 / 档案抽屉 / 展柜 / 材料库 / 画廊墙 / 校样间 / 石膏墙 |",
      "", "## Agent 物理隐喻（不画 UI）\n",
      "| # | 隐喻 | 传达 |", "|---|---|---|",
      "| M1 | 一张 brief 卡 → 三种不同媒介的成品 | 统筹力 |",
      "| M2 | 同一物件呈现原始→半成→完成三态 | 从意图到交付 |",
      "| M3 | 物件正在自行完成（边缘翻起、封套合拢） | 自主性 |",
      "| M4 | 同一视觉语言出现在纸/布/陶/金属上 | 多模型协同 |",
      "| M5 | 草稿与最终版精确叠放 | 思考与迭代 |",
      "", f"> agent 隐喻全站覆盖 **148/397（37%）**；瓦片与模块为主，mosaic/media 因是单状态叙事不加。",
      ]
(ROOT / "00-INDEX.md").write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"V3 md 生成完毕：{total} 条，{len(index)} 个分组目录")
