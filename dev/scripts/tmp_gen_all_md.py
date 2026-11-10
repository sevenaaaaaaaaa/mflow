#!/usr/bin/env python3
"""tmp_gen_all_md.py — 把全部 JSONL brief 渲染成可读 Markdown（每个模块/批次一份 + 一份总览）

输出：
  md/00-总览.md
  md/A-split.md  md/B-cinematic.md  md/C-mosaic.md
  md/D1-media.md  md/D2-{cat}.md ×18  md/D3-tools.md
  md/E1-{cat}.md ×18  md/E3-{cat}.md ×18
  md/E4-journey.md  md/E5-video.md
"""
import json
from collections import Counter, OrderedDict
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
MD = D / "md"
MD.mkdir(exist_ok=True)
B = D / "batches"


def load(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


CAT_LABEL = {
    "logo": "Logo 设计", "poster": "海报设计", "banner": "Banner 设计",
    "menu": "菜单设计", "brochure": "宣传册设计", "business-card": "名片设计",
    "packaging": "包装设计", "cover": "封面设计", "video-thumbnail": "视频缩略图",
    "social-media": "社媒设计", "ecommerce-main": "电商主图",
    "product-detail": "商品详情页", "ppt": "演示文稿", "resume": "简历设计",
    "font": "字体设计", "illustration": "插画设计", "data-story": "信息图设计",
    "brand-identity": "品牌视觉识别",
}

TYPE_CATS = {"poster", "banner", "menu", "brochure", "packaging", "video-thumbnail",
             "social-media", "product-detail", "ppt", "resume", "data-story"}


def header(title, meta_lines):
    out = [f"# {title}\n"]
    out += [f"> {m}" for m in meta_lines]
    out.append("")
    return out


def render_record(r, show_fields=None):
    """单条 brief 渲染"""
    out = []
    rid = r["id"]
    label = r.get("label") or r.get("theme_label") or r.get("theme") or ""
    ind = r.get("industry", "")
    title = f"**{rid}**"
    extra = []
    if ind:
        extra.append(f"行业：{ind}")
    if label and label != r.get("theme"):
        extra.append(label)
    if r.get("lane"):
        extra.append(f"`{r['lane']}`")
    if r.get("step"):
        extra.append(f"步骤：{r['step']}")
    if r.get("tile"):
        extra.append(f"瓦片 {r['tile']}")
    if extra:
        title += "　·　" + "　·　".join(extra)
    if r.get("pages"):
        title += f"　·　覆盖 {r['pages']} 页"
    out.append(title)
    if r.get("notes"):
        out.append(f"> {r['notes']}")
    out.append(f"- **Prompt**")
    out.append("")
    out.append("```text")
    out.append(r["prompt"])
    out.append("```")
    out.append("")
    out.append(f"- **Alt**：`{r['alt']}`")
    out.append("")
    return out


def render_group(records, *, title, spec, discipline, group_key=None, group_title=None):
    out = header(title, [
        f"张数：**{len(records)}**",
        f"规格：{spec}",
    ] + discipline)
    out.append("---\n")
    if group_key:
        groups = OrderedDict()
        for r in records:
            groups.setdefault(r.get(group_key, "未分组"), []).append(r)
        for k, rs in groups.items():
            name = group_title(k, rs) if group_title else k
            out.append(f"## {name}（{len(rs)} 张）\n")
            for r in rs:
                out += render_record(r)
            out.append("---\n")
    else:
        for r in records:
            out += render_record(r)
    return out


def main():
    written = {}

    # ── A · split ──
    A = load(D / "module-A-split.jsonl")
    A.sort(key=lambda r: (0 if r["priority"] == "P0" else 1, -r.get("pages", 0)))
    out = render_group(
        A, title="模块 A · hero-split（左文右图）· 20 张",
        spec="2160×1620 · 4:3 · JPG/PNG ≤1.5MB",
        discipline=[
            "构图：左侧是页面文案栏，视觉重心须落在中右 60%；主体完整、四边 ≥5% 裁切余量",
            "预算：主视觉 ×1 + 支撑元素 ≤2 + 背景处理 ×1；禁止画任何界面",
            "命名：`hero-split-{theme}-v1.png`",
        ],
        group_key="priority",
        group_title=lambda k, rs: {"P0": "P0 · 止血六张（出图即替换 83c980ae.jpg 死链）",
                                   "P2": "P2 · 其余主题族"}.get(k, k),
    )
    (MD / "A-split.md").write_text("\n".join(out), encoding="utf-8")
    written["A-split"] = len(A)

    # ── B · cinematic ──
    Bc = load(D / "module-B-cinematic.jsonl")
    out = render_group(
        Bc, title="模块 B · hero-cinematic（居中标题 + 全宽剧院图）· 5 张",
        spec="2400×1500 · 16:10 · JPG/PNG ≤1.5MB",
        discipline=[
            "构图：三层深度（前/中/后），每层最多 1 个主元素",
            "上下各 8% 渐隐过渡，与页面背景衔接",
            "文字全在图外，图内不烧录任何文案",
            "命名：`hero-cinematic-{theme}-v1.png`",
        ],
    )
    (MD / "B-cinematic.md").write_text("\n".join(out), encoding="utf-8")
    written["B-cinematic"] = len(Bc)

    # ── C · mosaic ──
    C = load(D / "module-C-mosaic.jsonl")
    out = render_group(
        C, title="模块 C · hero-mosaic（4 瓦拼贴）· 8 张（2 套）",
        spec="每瓦 1200×900 · 4:3",
        discipline=[
            "4 瓦 = 同一主体的 4 个连续状态（时间轴叙事）",
            "每瓦下方 30% 保持低细节供标题叠加",
            "**每套 4 瓦必须同一会话连续生成 + 锁 seed + 同风格参考**",
            "命名：`hero-mosaic-{set}-t{n}.png`",
        ],
        group_key="id",
        group_title=lambda k, rs: f"{k.rsplit('-', 1)[0]} · {rs[0].get('theme','')}",
    )
    (MD / "C-mosaic.md").write_text("\n".join(out), encoding="utf-8")
    written["C-mosaic"] = len(C)

    # ── D1 media ──
    D1 = load(B / "D1-media.jsonl")
    out = render_group(
        D1, title="D1 · gallery media 主图 · 18 张",
        spec="2160×1350 · 16:10",
        discipline=[
            "每个品类一张总览主图，对应页面 `hero-gallery` 段的 `media` 字段",
            "主体 + 少量辅件，建立该品类的视觉基调",
            "命名：`hero-gallery-media-{cat}-v1.png`",
        ],
    )
    (MD / "D1-media.md").write_text("\n".join(out), encoding="utf-8")
    written["D1-media"] = len(D1)

    # ── D2 每品类 ──
    for f in sorted(B.glob("D2-*.jsonl")):
        recs = load(f)
        cat = recs[0]["theme"]
        risk = "（含排版语义：图内零可读字符，排版用抽象灰色条块表达）" if cat in TYPE_CATS else ""
        out = render_group(
            recs, title=f"D2 · {CAT_LABEL.get(cat, cat)} · 6 行业瓦片 {risk}",
            spec="1200×1200 · 1:1",
            discipline=[
                "每瓦 = 单对象，底部 25% 留 label 遮罩",
                "**6 张必须同一会话 + 锁 seed + 同背景色，只换行业**",
                "机位已按瓦片序号互斥分配：正视 / 侧角 / 微距 / 俯拍 / 低角度 / 侧轮廓",
                f"命名：`hero-gallery-{cat}-{{industry}}-v1.png`",
            ],
        )
        (MD / f"D2-{cat}.md").write_text("\n".join(out), encoding="utf-8")
        written[f"D2-{cat}"] = len(recs)

    # ── D3 tools ──
    D3 = load(B / "D3-tools.jsonl")
    out = render_group(
        D3, title="D3 · gallery 工具瓦片 · 28 张",
        spec="1200×1200 · 1:1",
        discipline=[
            "6 瓦套 ×4 + 4 瓦套 ×1（后者 11 个语言版本共用同一套图）",
            "每套同一会话 + 锁 seed",
            "命名：`hero-gallery-tools-{set}-t{n}.png`",
        ],
        group_key="theme",
    )
    (MD / "D3-tools.md").write_text("\n".join(out), encoding="utf-8")
    written["D3-tools"] = len(D3)

    # ── E1 / E3 每品类 ──
    for prefix, note in [("E1", "4 个 B 端行业（房地产 / 教育培训 / 医疗健康 / 金融保险）"),
                         ("E3", "剩余 2 行业（商旅出行 / 文化创意）")]:
        for f in sorted(B.glob(f"{prefix}-*.jsonl")):
            recs = load(f)
            cat = recs[0]["theme"]
            out = render_group(
                recs, title=f"{prefix} · {CAT_LABEL.get(cat, cat)} · {len(recs)} 行业瓦片",
                spec="1200×1200 · 1:1",
                discipline=[
                    f"行业范围：{note}",
                    "**必须紧接同品类的 D2 批在同会话内跑完**，否则同品类会分裂成两套视觉语言",
                    "命名：`hero-gallery-{cat}-{industry}-v1.png`",
                ],
            )
            (MD / f"{prefix}-{cat}.md").write_text("\n".join(out), encoding="utf-8")
            written[f"{prefix}-{cat}"] = len(recs)

    # ── E4 journey ──
    E4 = load(B / "E4-journey-media.jsonl")
    out = render_group(
        E4, title="E4 · hero-journey media 大图 · 7 张",
        spec="2160×1350 · 16:10",
        discipline=[
            "对应 `hero-journey` 段的 `media` 字段（step 卡片图标由代码渲染，无需出图）",
            "13 个 journey 页面按语义去重为 7 个场景",
            "命名：`hero-journey-media-{scene}-v1.png`",
        ],
    )
    (MD / "E4-journey.md").write_text("\n".join(out), encoding="utf-8")
    written["E4-journey"] = len(E4)

    # ── E5 video ──
    E5 = load(D / "E5-cinematic-video.jsonl")
    out = render_group(
        E5, title="E5 · cinematic 视频版 · 5 条",
        spec="2400×1500 · 16:10 · 8s 静音循环 MP4 ≤8MB",
        discipline=[
            "与对应 B 系列静帧**同构图**，用静帧作 poster",
            "8 秒、循环、无音轨",
            "命名：`hero-cinematic-{theme}-v1.mp4` + `-poster.jpg`",
        ],
    )
    (MD / "E5-video.md").write_text("\n".join(out), encoding="utf-8")
    written["E5-video"] = len(E5)

    # ── 总览 ──
    groups = [
        ("A · hero-split", "A-split.md", ["P0 止血 ×6", "其余主题族 ×14"], "2160×1620 · 4:3"),
        ("B · hero-cinematic", "B-cinematic.md", ["品牌旗舰页"], "2400×1500 · 16:10"),
        ("C · hero-mosaic", "C-mosaic.md", ["platform 4 瓦", "industry 4 瓦"], "每瓦 1200×900 · 4:3"),
        ("D1 · gallery media", "D1-media.md", ["18 品类总览"], "2160×1350 · 16:10"),
        ("D2 · gallery 瓦片×18", "D2-{cat}.md", ["18 品类 × 6 主力行业"], "1200×1200 · 1:1"),
        ("D3 · 工具瓦片", "D3-tools.md", ["6瓦×4套", "4瓦×1套"], "1200×1200 · 1:1"),
        ("E1 · B端行业×18", "E1-{cat}.md", ["18 品类 × 4 B端行业"], "1200×1200 · 1:1"),
        ("E3 · 剩余行业×18", "E3-{cat}.md", ["18 品类 × 2 剩余行业"], "1200×1200 · 1:1"),
        ("E4 · journey media", "E4-journey.md", ["7 场景"], "2160×1350 · 16:10"),
        ("E5 · 视频", "E5-video.md", ["5 条"], "2400×1500 · 8s"),
    ]
    o = ["# Hero 封面 Brief 全集 · 274 张\n",
         "> 全部 brief 的可读版。原始机器可读文件在 `batches/*.jsonl` 与 `module-*.jsonl`。",
         "> 风格体系见 `prompt-v2-style-system.md`；执行顺序见 `ALL-BATCHES.md`。\n",
         "| 模块 | 文档 | 内容 | 规格 | 张数 |", "|---|---|---|---|---:|"]
    for name, fname, contents, spec in groups:
        if "{cat}" in fname:
            n = sum(v for k, v in written.items() if k.startswith(name.split(" ")[0] + "-"))
        else:
            n = written.get(name.split(" · ")[0].replace("D1", "D1-media"), 0)
            if n == 0:
                n = written.get(fname.replace(".md", ""), 0)
        o.append(f"| {name} | `{fname}` | {' / '.join(contents)} | {spec} | {n or '—'} |")
    o.append(f"| **合计** | | | | **{sum(written.values())}** |")
    o.append("")
    o.append("## 通用规范（所有批次）\n")
    o.append("| 项 | 要求 |")
    o.append("|---|---|")
    o.append("| 图内文字 | 零。含可读字符即废稿；含排版品类用抽象灰色条块表达层级 |")
    o.append("| 多语言 | 同页面 10–11 语言版本共用同一套图，按主题做、不按语言做 |")
    o.append("| 安全区 | 四边 ≥5%；mosaic 下方 30% / gallery 下方 25% 低细节 |")
    o.append("| 体积 | JPG q85 或优化 PNG ≤1.5MB（视频 ≤8MB） |")
    o.append("| 禁用元素 | 紫蓝渐变、玻璃拟态、悬浮 3D 球、等距插画、光轨、floating chips |")
    o.append("")
    o.append("## 同批一致铁律\n")
    o.append("1. 一个品类的所有行业瓦片**同一会话连续生成**")
    o.append("2. **锁 seed + 同一风格参考图**")
    o.append("3. **D2 → E1 → E3 同品类连着跑**，不要先把 D2 全部跑完再回头补")
    o.append("4. mosaic 每套 4 瓦、gallery 每套 6 瓦同理")
    (MD / "00-总览.md").write_text("\n".join(o) + "\n", encoding="utf-8")

    print(f"md/ 目录已生成 {len(list(MD.glob('*.md')))} 个文档")
    print(f"brief 总条数: {sum(written.values())}")


if __name__ == "__main__":
    main()
