#!/usr/bin/env python3
"""tmp_gen_module_docs.py — 按 section 模块生成独立提示词文档（modules/*.md）"""
import json
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
MO = D / "modules"
MO.mkdir(exist_ok=True)

L1 = ("High-end commercial photograph, 85mm shallow depth of field, soft key light "
      "from the upper left with a gentle contact shadow")
L3 = ("Soft-body 3D render in matte ceramic materials, warm-grey palette with one coral "
      "accent, macro 50mm look, soft key light with gentle contact shadows")
L4 = ("Editorial flat-graphic composition on a Swiss grid, paper grain texture with "
      "riso-print ink edges, flat layout with no photographic perspective, flat even lighting")
TAIL = "no text, no letters, no watermark, no screens, no UI windows"


def mk(lane, scene, ratio, fill, extra=""):
    p = f"{lane}, {scene}, the subject fills about {fill}% of frame, {ratio}"
    if extra:
        p += f", {extra}"
    return f"{p}, edges safe for rounded-corner crop, {TAIL}"


# ══════════════════════════════════════════════════════════
MODULES = []

# 1. bento-2
MODULES.append(dict(
    file="01-bento-2.md", stype="bento-2", name="bento-2 · 两栏特性卡",
    field="`features[].media.src`", size="1600 × 1000", ratio="16:10",
    per_instance=2, pages=6383,
    definition="2 等宽大卡，每卡 title + description + 大图；桌面端左右并排，移动端上下堆叠。",
    usage="用于「两个最重要能力 / 两个转化任务」的平行对比。",
    discipline=[
        "两卡必须视觉同构（同布光、同背景色系、同机位高度），否则并排会歪",
        "每卡只表达 1 个能力，不要塞多个元素",
        "卡片下方有 title + description 文字区，图片下半 20% 保持简洁",
    ],
    items=[
        ("电商转化", L1, "a single product on a clean podium with a soft contact shadow"),
        ("品牌一致性", L1, "one brand mark applied across a printed card and a small packaging box"),
        ("批量产出", L1, "a fan of five printed pieces in identical format laid in a row"),
        ("素材复用", L1, "one hero print shown twice at different sizes side by side"),
        ("交付速度", L1, "a clean desk with one finished print and a single pen"),
        ("商用授权", L1, "a printed certificate card with an abstract seal beside a framed artwork"),
        ("多模型协同", L3, "two matte ceramic objects of the same subject in different treatments"),
        ("团队协同", L1, "two copies of the same print on a shared table"),
    ]))

# 2. bento-4
MODULES.append(dict(
    file="02-bento-4.md", stype="bento-4", name="bento-4 · 2×2 不规则四宫格",
    field="`features[].media.src`", size="1600 × 1200", ratio="4:3",
    per_instance=4, pages=1730,
    definition="上排两等宽，下排左小右大（4:8），共 4 个特性卡。",
    usage="用于「四条能力线」或「四步价值主张」。",
    discipline=[
        "4 张必须同族：同背景色、同光向、同后期；否则拼贴会散",
        "下排右侧大卡尺寸更大，主体构图可稍宽（留更多呼吸）",
        "避免 4 张都用「居中正对」，至少 2 张用侧角或俯视",
    ],
    items=[
        ("图片生成", L1, "one vivid painted artwork standing on a small wooden easel"),
        ("视频生成", L1, "a short film strip with three consecutive frames of the same scene"),
        ("精准编辑", L1, "a printed photo with a clean vertical tear revealing a crisper version behind"),
        ("多格式导出", L1, "one design printed at three different aspect ratios laid side by side"),
        ("角色一致性", L3, "the same matte clay character shown on four small cards"),
        ("风格迁移", L1, "a cityscape print with painterly texture flowing across one half"),
        ("背景移除", L1, "a product cutout on pure white lifted slightly off a textured backdrop"),
        ("批量扩图", L1, "one small print expanding into a large print via layered paper steps"),
    ]))

# 3. bento-6
MODULES.append(dict(
    file="03-bento-6.md", stype="bento-6", name="bento-6 · 六卡 bento",
    field="`features[].media.src`", size="1400 × 1050", ratio="4:3",
    per_instance=6, pages=5063,
    definition="左大 + 右上下 + 底排三等分，共 6 个特性卡。",
    usage="用于「六大能力」综合展示，是站内使用量最大的 bento 变体。",
    discipline=[
        "6 张必须同族（同背景、同光向）；第 1 张（大卡）可略复杂，其余 5 张保持简洁",
        "6 张之间靠「对象」区分，不靠「风格」区分",
        "底排 3 卡在移动端会挤成单列，构图勿依赖横向关系",
    ],
    items=[
        ("图文一致", L1, "one poster beside the product it advertises, a visual echo between them"),
        ("批量变体", L1, "six small cards of the same template with different color treatments"),
        ("团队协作", L1, "three open notebooks showing the same page spread"),
        ("素材库", L1, "a tidy drawer of printed swatch cards fanned open"),
        ("品牌套件", L1, "a compact kit box open to reveal cards, a swatch and a mark card"),
        ("发布就绪", L1, "a finished print standing upright under a focused desk lamp"),
        ("A/B 测试", L1, "two poster variants side by side, one warmer one cooler"),
        ("本地化", L1, "the same layout printed three times with different visual treatments"),
        ("版权合规", L1, "a clean signed card resting on a stack of blank release forms"),
        ("4K 输出", L1, "a fine print under a loupe revealing crisp micro detail"),
        ("流程自动化", L1, "three connected paper cards falling in sequence"),
        ("资产归档", L1, "labeled archive boxes with one printed card peeking out"),
    ]))

# 4. feature-detail
MODULES.append(dict(
    file="04-feature-detail.md", stype="feature-detail", name="feature-detail · 图文左右交错",
    field="`items[].media.src`", size="1600 × 1200", ratio="4:3",
    per_instance=4, pages=7303,
    definition="N 个图文块左右交错：第 0 条图在右，`reverse: true` 让图在左。站内覆盖面最大的模块。",
    usage="用于「逐条展开能力」，每条一个图 + 标题 + 描述 + bullets + CTA。",
    discipline=[
        "**构图必须为文字留位**：图在右时主体偏左，图在左时主体偏右（交错排版的呼吸感）",
        "同页 4 条要形成节奏：机位高度、主体大小交替变化，不能 4 张一模一样",
        "每条配 3 个 bullet，图片需能承载「具体可指认」的对象（可被 bullet 描述）",
    ],
    items=[
        ("从 brief 开始", L1, "one index card with a folded corner resting on a worktable beside a pen"),
        ("多模型生成", L1, "a row of finished artworks of the same subject in four different styles"),
        ("精准控制", L1, "a printed photo with a small measuring rule laid across it"),
        ("图层编辑", L1, "layered paper sheets fanned to reveal separate printed planes"),
        ("工作流串联", L1, "three connected cards linked by a thin paper strip"),
        ("交付与导出", L1, "three printed formats stacked neatly ready to hand off"),
        ("品牌资产", L1, "a folder opened to show brand cards, a swatch and a mark card"),
        ("团队协作", L1, "two copies of the same print on a shared table, aligned"),
    ]))

# 5. capability-tabs
MODULES.append(dict(
    file="05-capability-tabs.md", stype="capability-tabs", name="capability-tabs · Tab 切换大内容区",
    field="`tabs[].content.media.src`", size="1760 × 1100", ratio="16:10",
    per_instance=4, pages=6592,
    definition="左 4 列 tab list（label + icon），右 8 列内容区（图 + 标题 + 描述 + bullets + CTA），可自动轮播。",
    usage="用于「同一能力的多个维度」或「多个工具切换演示」。",
    discipline=[
        "**4 张必须同一视觉世界**：同材质、同打光、同背景色 —— 因为它们是同一个内容区轮播",
        "切换时只换「对象」，不换「风格」；否则轮播会闪",
        "图片右侧留 8 列文字位，主体重心偏左",
    ],
    items=[
        ("Image to Video", L3, "a framed landscape photo with one corner lifting into a soft motion trail"),
        ("Text to Video", L3, "a tiny open book with a miniature scene rising from its pages"),
        ("Product Video", L3, "a product on a small turntable with a circular motion trail"),
        ("Social Clips", L3, "a vertical phone-shaped frame holding a bold scene"),
        ("Style Reference", L3, "a style swatch card laid over a photo print with matching textures"),
        ("Consistent Character", L3, "the same matte clay figure photographed from four angles"),
    ]))

# 6. canvas-wall
MODULES.append(dict(
    file="06-canvas-wall.md", stype="canvas-wall", name="canvas-wall · 10 卡画布墙",
    field="`items[].media.src`", ratio="16:10 (大卡) / 1:1 (9 小卡)",
    size="1600 × 1000（大卡）/ 1000 × 1000（小卡）",
    per_instance=10, pages=1374,
    definition="左上 1 大卡 + 右上 5 小卡 + 底排 4 卡，每卡可显示作者 / likes / caption。",
    usage="用于「作品集展示」与「创作多样性」证明。",
    discipline=[
        "**10 张必须是 10 个不同品类**（海报/包装/名片/画册…），这是「能力广度」的唯一证明",
        "统一背景色与光向，视觉上像「同一面展示墙」",
        "每卡右下角有 caption 遮罩，主体避开右下 25%",
    ],
    items=[
        ("大卡 · 主视觉", L1, "one large framed artwork on a soft backdrop, gallery presentation", "16:10"),
        ("小卡 1 · 海报", L1, "a single printed poster with one corner curling", "1:1"),
        ("小卡 2 · 包装", L1, "a small packaging box with a printed sleeve", "1:1"),
        ("小卡 3 · 名片", L1, "a pair of business cards overlapping at an angle", "1:1"),
        ("小卡 4 · 画册", L1, "a folded brochure showing one open spread", "1:1"),
        ("小卡 5 · 社媒", L1, "a square social post card with a bold central shape", "1:1"),
        ("底排 1 · 菜单", L1, "a menu page standing open at a slight angle", "1:1"),
        ("底排 2 · 封面", L1, "a book cover standing upright", "1:1"),
        ("底排 3 · 横幅", L1, "a wide promotional banner sample laid flat", "1:1"),
        ("底排 4 · 标签", L1, "a product label wrapped around a small bottle", "1:1"),
    ]))

# 7. workflow-horizontal
MODULES.append(dict(
    file="07-workflow-horizontal.md", stype="workflow-horizontal", name="workflow-horizontal · 横向 N 步流程",
    field="`steps[].media.src`", size="1200 × 900", ratio="4:3",
    per_instance=3, pages=6557,
    definition="横向一排 step 卡（编号 + 标题 + 描述），每卡一张图。",
    usage="用于「3 步搞定」类流程叙事，覆盖页数极高。",
    discipline=[
        "**必须是同一主体的 3 个连续状态**（时间轴），不是 3 个不同对象",
        "3 张同背景、同光向、同机位高度；只让「状态」递进",
        "每卡下方 30% 留编号与描述位，保持低细节",
    ],
    items=[
        ("输入", L3, "a card being dropped toward a small shallow tray"),
        ("生成", L3, "a short row of small finished pieces standing on the same worktable"),
        ("精修", L3, "a finished print with a small tool resting beside it"),
        ("导出", L3, "three finished formats stacked neatly on the same table"),
    ]))

# 8. showcase
MODULES.append(dict(
    file="08-showcase.md", stype="showcase-stacked / showcase-horizontal",
    name="showcase · 前后堆叠 / 横向滚动展示",
    field="`items[].media.src`", size="1760 × 1100", ratio="16:10",
    per_instance=3, pages=149,
    definition="stacked：垂直堆叠 N 个图文块；horizontal：横向 carousel，每卡 16:10 大图 + 标题 + 描述 + CTA。",
    usage="用于「产品流程」深度叙事，视觉权重仅次于 hero。",
    discipline=[
        "**大图叙事，每张要有独立可读的完整场景**（不是缩略图放大）",
        "N 张之间是「流程先后」，需有递进关系",
        "横向 carousel 会左右裁切，主体避开左右各 8%",
    ],
    items=[
        ("产品图套件", L1, "one product shown as a clean cutout beside a fully styled scene"),
        ("广告素材", L1, "three ad formats of the same campaign laid side by side"),
        ("社交内容", L1, "a small stack of social post cards with the top one lifted"),
        ("品牌识别", L1, "a brand board with a mark, a swatch row and material samples"),
        ("包装设计", L1, "a package box and its printed sleeve separated on a table"),
        ("视频产出", L3, "a film strip unrolling from a spool with visible frames"),
    ]))

# 9. comparison-before-after
MODULES.append(dict(
    file="09-comparison-before-after.md", stype="comparison-before-after",
    name="comparison-before-after · 前后对比滑块",
    field="`before.media.src` + `after.media.src`", size="1600 × 900", ratio="16:9",
    per_instance=2, pages=614,
    definition="单图分左右两半（带可拖动竖杠），各贴 label；`aspect` 支持 1:1 / 4:3 / 3:4 / 9:16 / 16:9。",
    usage="用于「改造前 vs 改造后」的强对比证明。",
    discipline=[
        "**before 与 after 必须同主体、同构图、同机位**——只有「状态」不同，否则滑块会跳",
        "分割线在正中；两半的分辨率、亮度基线要一致",
        "这是唯一「拖拽交互」的模块，图片质量直接决定说服力",
    ],
    items=[
        ("草稿 vs 成品", L1, "a rough pencil sketch on the left half transforming into a polished printed artwork on the right half"),
        ("低清 vs 4K", L1, "one photo print with a blurred left half and a razor-sharp right half"),
        ("杂乱 vs 整洁", L1, "a cluttered work desk left half and a clean organized right half"),
        ("普通 vs 品牌化", L1, "the same layout left half without brand treatment and right half with a coherent brand system"),
        ("灰调 vs 调色", L1, "one photo with a flat desaturated left half and a richly graded right half"),
        ("空背景 vs 场景", L1, "a product on plain white left half and the same product in a styled scene right half"),
    ]))

# 10. media-marquee
MODULES.append(dict(
    file="10-media-marquee.md", stype="media-marquee", name="media-marquee · 媒体横向跑马灯",
    field="`items[].src`", size="1000 × 1000", ratio="1:1",
    per_instance=8, pages=0,
    definition="图片不停横向滚动，每张图含 caption + 作者 + 宽高。",
    usage="用于「创作多样性」快速证明，视觉上像作品瀑布。",
    discipline=[
        "**8 张必须是 8 个不同品类**，横滚时才有「广度」感",
        "统一背景与光向，横滚时画面不闪",
        "图片按 1:1 裁切，主体居中偏上（下方有 caption）",
    ],
    items=[
        ("海报", L1, "a poster standing against a plain backdrop"),
        ("包装", L1, "a small package box at a three-quarter angle"),
        ("名片", L1, "a pair of business cards overlapping"),
        ("社媒图", L1, "a square social card with a bold central shape"),
        ("封面", L1, "a book cover standing upright"),
        ("菜单", L1, "an open menu page at a slight angle"),
        ("横幅", L1, "a wide banner sample laid flat"),
        ("标签", L1, "a product label on a small bottle"),
    ]))

# 11. portrait-grid
MODULES.append(dict(
    file="11-portrait-grid.md", stype="portrait-grid-3 / portrait-grid-4",
    name="portrait-grid · 方形 / 竖版卡网格",
    field="`items[].media.src`", ratio="1:1 (grid-3) / 3:4 (grid-4)",
    size="1000 × 1000 / 900 × 1200",
    per_instance=3, pages=41,
    definition="grid-3：3 张 1:1 卡，上图下文；grid-4：4 张 3:4 竖版卡（`aspect` 可改 1:1 / 9:16）。",
    usage="用于「角色/场景系列」或「人物案例」。",
    discipline=[
        "**必须是同一系列**：同材质、同光向、同景别；只换角色或场景",
        "每卡下方有 title + subtitle + CTA，主体避开下方 20%",
        "竖版 3:4 构图需给竖直方向留呼吸，主体不要顶天立地",
    ],
    items=[
        ("角色 A", L3, "a matte clay figurine portrait in three-quarter view"),
        ("角色 B", L3, "a different matte clay figurine portrait under identical lighting"),
        ("角色 C", L3, "a third matte clay figurine portrait from the same family style"),
        ("场景 A", L3, "a miniature set piece of a shopfront interior"),
        ("场景 B", L3, "a miniature set piece of a studio corner"),
        ("场景 C", L3, "a miniature set piece of an outdoor market stall"),
    ]))

# 12. tool-grid / blog-grid
MODULES.append(dict(
    file="12-tool-grid-blog-grid.md", stype="tool-grid / blog-grid",
    name="tool-grid / blog-grid · 工具卡与文章网格",
    field="`tools[].media.src` / `posts[].cover.src`", size="1600 × 1000", ratio="16:10",
    per_instance=6, pages=226,
    definition="tool-grid：3 列网格，每卡 icon + 名称 + 分类 + 描述 + tag + 评分；blog-grid：3 列卡片，封面图 + 标题 + 摘要 + 日期。",
    usage="tool-grid 用于「工具矩阵入口」；blog-grid 用于「内容聚合」。",
    discipline=[
        "tool-grid 图是「该工具产出的样张」，必须有辨识度（一眼能看出是 logo / 海报 / 包装）",
        "blog-grid 图是「文章配图」，可更泛化（场景/氛围），不要求具体品类",
        "两者都是小卡，主体须占 70% 以上，缩略后仍可辨",
    ],
    items=[
        ("工具卡 · Logo", L1, "a logo mark card standing upright"),
        ("工具卡 · 海报", L1, "a poster sample at a slight angle"),
        ("工具卡 · 视频", L1, "a short film strip with visible frames"),
        ("工具卡 · 包装", L1, "a packaging box with a printed sleeve"),
        ("工具卡 · 社媒", L1, "a square social card with a bold shape"),
        ("工具卡 · 名片", L1, "a pair of business cards fanned"),
        ("博客配图 · 教程", L1, "a designer's desk mid-process with a print and a tool"),
        ("博客配图 · 案例", L1, "a finished printed set ready for delivery"),
    ]))


# ══════════════════════════════════════════════════════════
def build(m):
    out = [f"# {m['name']}\n"]
    out.append(f"> **section type**：`{m['stype']}`  ")
    out.append(f"> **图片来源字段**：{m['field']}  ")
    out.append(f"> **尺寸 / 比例**：{m['size']} · {m['ratio']}  ")
    out.append(f"> **每实例图片数**：{m['per_instance']}  ")
    if m["pages"]:
        out.append(f"> **站内覆盖页面**：约 {m['pages']} 个文档")
    out.append("")
    out.append("## 模块形态\n")
    out.append(m["definition"])
    out.append("")
    out.append(f"**用途**：{m['usage']}\n")
    out.append("## 本模块专属纪律\n")
    for i, d in enumerate(m["discipline"], 1):
        out.append(f"{i}. {d}")
    out.append("")
    out.append("## 通用规范\n")
    out.append("| 项 | 要求 |")
    out.append("|---|---|")
    out.append("| 图内文字 | **零**。含可读字符即废稿；如模块自带排版，用抽象灰色条块表达层级 |")
    out.append("| 多语言 | 同页面 10–11 语言版本共用同一套图，按模块做、不按语言做 |")
    out.append("| 安全区 | 四边 ≥5% 裁切余量，主体不触边 |")
    out.append("| 体积 | JPG q85 或优化 PNG ≤1.5MB |")
    out.append("| 禁用元素 | 紫蓝渐变 / 玻璃拟态 / 悬浮 3D 球 / 等距插画 / 光轨 / floating chips / 多点拼贴 |")
    out.append("")
    out.append("---\n")
    out.append(f"## 提示词（{len(m['items'])} 条）\n")
    out.append("> 同一个页面里同模块的多张图**必须同会话 + 锁 seed + 同风格参考**，只换对象。\n")

    for i, item in enumerate(m["items"], 1):
        if len(item) == 3:
            lab, lane, scene = item
            ratio = m["ratio"].split(" ")[0]
        else:
            lab, lane, scene, ratio = item
        fill = 70
        prompt = mk(lane, scene, ratio, fill)
        out.append(f"### {i:02d} · {lab}\n")
        out.append("```text")
        out.append(prompt)
        out.append("```")
        out.append("")
        out.append(f"- **Alt**：`Lovart {lab} — {m['stype']} visual`")
        out.append(f"- **命名**：`{m['stype'].split(' / ')[0]}-{i:02d}-{slug(lab)}-v1.png`")
        out.append("")
    return "\n".join(out)


def slug(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "item"


def main():
    total = 0
    for m in MODULES:
        md = build(m)
        (MO / m["file"]).write_text(md, encoding="utf-8")
        total += len(m["items"])
        print(f"{m['file']:<36} {len(m['items']):>3} 条")

    # 总览
    o = ["# 落地页模块配图 · 提示词总览\n",
         "> 每个模块一份独立文档，位于 `modules/` 目录。",
         "> Hero 部分见上级目录的 `md/`（307 张）。\n",
         "| # | 模块 | section type | 图位/实例 | 覆盖页 | 提示词数 | 文档 |",
         "|---:|---|---|---:|---:|---:|---|"]
    for i, m in enumerate(MODULES, 1):
        o.append(f"| {i} | {m['name'].split(' · ')[1]} | `{m['stype']}` | {m['per_instance']} | "
                 f"{m['pages'] or '—'} | {len(m['items'])} | `{m['file']}` |")
    o.append(f"| | | | | | **{total}** | |")
    o.append("")
    o.append("## 无需配图的模块\n")
    o.append("以下模块为纯文字/图标/数字，**不需要图片素材**：\n")
    o.append("`faq` · `cta-default` · `stats` · `proof-block` · `pricing-table` · "
             "`comparison-table` · `logo-loop` · `testimonial` · `prompt-launcher` · "
             "`tabs` · `timeline` · `workflow-vertical` · `cluster-block-dense`（icon 渲染）")
    o.append("")
    o.append("## 生产顺序建议\n")
    o.append("按站内覆盖页数降序，先做影响面最大的：\n")
    o.append("1. `feature-detail`（7,303 页）—— 覆盖最广")
    o.append("2. `capability-tabs`（6,592 页）")
    o.append("3. `bento-2`（6,383 页）")
    o.append("4. `workflow-horizontal`（6,557 页）")
    o.append("5. `bento-6`（5,063 页）")
    o.append("6. `bento-4`（1,730 页）")
    o.append("7. `canvas-wall`（1,374 页）")
    o.append("8. `comparison-before-after`（614 页）")
    o.append("9. `showcase-*`（149 页）")
    o.append("10. `tool-grid` / `blog-grid`（226 页）")
    o.append("11. `portrait-grid-*`（41 页）")
    o.append("12. `media-marquee`（按需）")
    (MO / "00-总览.md").write_text("\n".join(o) + "\n", encoding="utf-8")
    print(f"\n00-总览.md 已生成，合计 {total} 条提示词")


if __name__ == "__main__":
    main()
