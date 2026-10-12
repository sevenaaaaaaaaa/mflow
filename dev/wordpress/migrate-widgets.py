#!/usr/bin/env python3
"""migrate-widgets.py — 把 widget-html 整块替换成生态原生微件。

为什么要有这个脚本
------------------
实测：仓库里 1089 个微件实例，840 个是 `widget-html`（77%）。
widget-html 只有一个 `html` 字段装整块 DOM 字符串，不可寻址 → 不能批量改、
不能在编辑器里编辑、内容只能靠 replica.js 在运行时注入。
换成原生微件后，每个字段都是 settings 里的具名 key，CSV/脚本都能直接写。

零猜测原则
----------
本脚本**不猜任何插件的 settings key**。你在 Elementor 编辑器里手搭一个目标微件，
用哨兵文本填两行，导出那段 JSON 当 sample；脚本靠哨兵反查出真实 key。
这样它对 EA / HT Mega / ElementsKit / 任何第三方包都通用，且永远不会因为
我记错键名而生成废数据。

哨兵约定（手搭 sample 时照填）
------------------------------
    第 1 行标题 → __T1__      第 1 行正文 → __C1__
    第 2 行标题 → __T2__      第 2 行正文 → __C2__

用法
----
    # 1) 看 sample 被解析成什么（不产出文件）
    python3 migrate-widgets.py --module faq --sample samples/faq-sample.json --inspect

    # 2) 预演：报告将替换多少块、内容从哪来，不写文件
    python3 migrate-widgets.py --module faq --sample samples/faq-sample.json

    # 3) 真产出到新目录（不碰 elem-src，不碰线上）
    python3 migrate-widgets.py --module faq --sample samples/faq-sample.json --write

产出的 JSON 仍走你既有的 lr_elem_import 流程导入，本脚本不连任何站点。
"""
import argparse
import html as H
import json
import re
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 哨兵格式：__<组><行>_<列>__ ，例如 __A1_2__ = A 组第 1 行第 2 列。
# 一个微件最多两个重复器：A 和 B（例如月付/年付两套价格表，或表头/表体）。
SENTINEL_RE = re.compile(r"__([AB])(\d+)_(\d+)__")
# 旧 FAQ sample 的两列写法仍然可用
LEGACY_ALIAS = {"__T1__": "__A1_1__", "__C1__": "__A1_2__",
                "__T2__": "__A2_1__", "__C2__": "__A2_2__"}
SENTINELS = LEGACY_ALIAS  # 自检沿用：产出里不该出现任何哨兵


# ───────────────────────── 通用工具 ─────────────────────────
def eid():
    """Elementor 元素 id：7 位小写十六进制。"""
    return secrets.token_hex(4)[:7]


def walk_widgets(nodes, fn):
    """深度遍历 Elementor 树，对每个 widget 节点调 fn(node, parent_list, index)。"""
    for i, n in enumerate(nodes):
        if n.get("elType") == "widget":
            fn(n, nodes, i)
        walk_widgets(n.get("elements") or [], fn)


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


# ───────────────────────── sample 解析 ─────────────────────────
def collect_sentinels(obj, path=()):
    """遍历出所有哨兵的位置：{(组, 行, 列): 路径}。"""
    found = {}
    if isinstance(obj, str):
        txt = obj
        for legacy, canon in LEGACY_ALIAS.items():
            txt = txt.replace(legacy, canon)
        m = SENTINEL_RE.search(txt)
        if m:
            found[(m.group(1), int(m.group(2)), int(m.group(3)))] = path
    elif isinstance(obj, dict):
        for k, v in obj.items():
            found.update(collect_sentinels(v, path + (k,)))
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            found.update(collect_sentinels(v, path + (idx,)))
    return found


def dig(o, path):
    for seg in path:
        o = o[seg]
    return o


def load_sample(path):
    """读手搭样本 → 每个重复器组的 {重复器路径, 行模板, 各列字段路径}。

    完全靠哨兵反查，不依赖任何插件的键名约定。
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    data = raw.get("data", raw) if isinstance(raw, dict) else raw
    widgets = []
    walk_widgets(data if isinstance(data, list) else [data],
                 lambda n, p, i: widgets.append(n))
    if not widgets:
        raise SystemExit(f"✗ sample 里没有 widget 节点：{path}")

    w = next((x for x in widgets
              if collect_sentinels(x)), None)
    if w is None:
        raise SystemExit(
            "✗ sample 里找不到哨兵。请在编辑器里按 __A1_1__ / __A1_2__ … 的格式填写\n"
            "  （A=第一个重复器，数字依次是 行_列），第 2 行填 __A2_1__ …，再导出。")

    marks = collect_sentinels(w)
    reps = {}
    for grp in sorted({g for g, _, _ in marks}):
        cells = {(r, c): pth for (g, r, c), pth in marks.items() if g == grp}
        # 行下标 = 路径里第一个 int；它之前是重复器路径，之后是字段路径
        # 路径里没有 int 下标 = 平铺字段（CTA 这类一块只有一组字段的微件），不是重复器
        if not any(isinstance(seg, int) for pth in cells.values() for seg in pth):
            rows = {r for (r, _) in cells}
            if rows != {1}:
                raise SystemExit(f"✗ {grp} 组是平铺字段，只能有第 1 行，实际有 {sorted(rows)}")
            cols = sorted(c for (_, c) in cells)
            if cols != list(range(1, len(cols) + 1)):
                raise SystemExit(f"✗ {grp} 组列号不连续：{cols}（应为 1,2,3…）")
            reps[grp] = {"flat": True, "rep_path": [], "item_tpl": None,
                         "field_paths": [list(cells[(1, c)]) for c in cols]}
            continue

        rep_paths, rows_seen = set(), {}
        for (r, c), pth in cells.items():
            k = next((ix for ix, seg in enumerate(pth) if isinstance(seg, int)), None)
            if k is None:
                raise SystemExit(
                    f"✗ {grp} 组的哨兵一部分在重复器里、一部分不在，无法判定结构。")
            rep_paths.add(pth[:k])
            rows_seen.setdefault(r, pth[k])
        if len(rep_paths) != 1:
            raise SystemExit(f"✗ {grp} 组的哨兵分散在多个重复器里，无法自动配对。")
        rep_path = rep_paths.pop()
        first_row = min(rows_seen)
        cols = sorted({c for (r, c) in cells if r == first_row})
        if cols != list(range(1, len(cols) + 1)):
            raise SystemExit(f"✗ {grp} 组第 {first_row} 行的列号不连续：{cols}（应为 1,2,3…）")
        field_paths = [list(cells[(first_row, c)][len(rep_path) + 1:]) for c in cols]
        reps[grp] = {
            "flat": False,
            "rep_path": list(rep_path),
            "item_tpl": json.loads(json.dumps(dig(w, list(rep_path))[rows_seen[first_row]])),
            "field_paths": field_paths,
        }

    return {"widget_type": w.get("widgetType"), "widget": w, "reps": reps}


def set_in(obj, path, value):
    for seg in path[:-1]:
        obj = obj[seg]
    obj[path[-1]] = value


def build_node(sample, payload, allow_truncate=False):
    """按 sample 的形状造新微件节点。payload = {"A": [[列1,列2,…], …], "B": […]}"""
    node = json.loads(json.dumps(sample["widget"]))
    node["id"] = eid()
    for grp, rows in payload.items():
        rep = sample["reps"].get(grp)
        if not rep:
            raise ValueError(
                f"sample 里没有 {grp} 组重复器，但抽取器产出了 {grp} 组数据。"
                f"（sample 现有：{', '.join(sample['reps']) or '无'}；"
                f"若目标微件确实只有一个重复器，用 --only-group 指定要迁的那一组）")
        slots = len(rep["field_paths"])
        if rep.get("flat"):
            if len(rows) != 1:
                raise ValueError(f"{grp} 组是平铺字段，只接受 1 行，抽取器给了 {len(rows)} 行")
            row = rows[0]
            if len(row) > slots and not allow_truncate:
                raise ValueError(
                    f"{grp} 组：抽取器给了 {len(row)} 列，sample 只有 {slots} 个字段槽。"
                    f"在 sample 里多填几个哨兵（__{grp}1_{slots + 1}__ …），"
                    f"或加 --allow-truncate 明确接受丢列。")
            for ix, path in enumerate(rep["field_paths"]):
                set_in(node, path, row[ix] if ix < len(row) else "")
            continue
        out = []
        for row in rows:
            if len(row) > slots and not allow_truncate:
                raise ValueError(
                    f"{grp} 组：抽取器给了 {len(row)} 列，sample 只有 {slots} 个字段槽。"
                    f"在 sample 里多填几个哨兵（__{grp}1_{slots + 1}__ …），"
                    f"或加 --allow-truncate 明确接受丢列。")
            item = json.loads(json.dumps(rep["item_tpl"]))
            if "_id" in item:
                item["_id"] = eid()
            for ix, path in enumerate(rep["field_paths"]):
                set_in(item, path, row[ix] if ix < len(row) else "")
            out.append(item)
        target = node
        for seg in rep["rep_path"][:-1]:
            target = target[seg]
        target[rep["rep_path"][-1]] = out
    return node


# ───────────────────────── 内容抽取器（按模块） ─────────────────────────
def _js_blob():
    return (ROOT / "assets-src" / "lovart-replica.js").read_text(encoding="utf-8")


def _js_object(var):
    """从 replica.js 里把一个 JS 对象字面量捞出来转成 dict（仅支持纯 JSON 子集）。"""
    js = _js_blob()
    m = re.search(r"(?:window\.)?%s\s*=\s*(\{)" % re.escape(var), js)
    if not m:
        return {}
    i = m.start(1)
    depth, j, instr, esc = 0, i, False, False
    while j < len(js):
        ch = js[j]
        if instr:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                instr = False
        else:
            if ch == '"':
                instr = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
        j += 1
    try:
        return json.loads(js[i:j + 1])
    except Exception as e:
        print(f"  ! {var} 解析失败：{e}", file=sys.stderr)
        return {}


def slug_of(page_file):
    """elem-src 文件名 → LR_FAQ_ANSWERS 的 key（与 replica.js 的 pageSlug 同口径）。"""
    s = Path(page_file).stem
    for pre in ("replica-solution-", "replica-", "lr-demo-native-", "lr-demo-faithful-"):
        if s.startswith(pre):
            s = s[len(pre):]
            break
    return s


def extract_faq(html, page_file):
    """FAQ：问题在 HTML 的 <h3> 里，答案在 LR_FAQ_ANSWERS 里，按序配对。

    实测 12 页问题数与答案数完全一致，故按序 zip 安全；不一致直接跳过，不截断。
    """
    qs = [strip_tags(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S)]
    qs = [q for q in qs if 10 < len(q) < 200]
    slug = slug_of(page_file)
    answers = _js_object("LR_FAQ_ANSWERS").get(slug, [])
    if not qs:
        return None, "HTML 里没抓到问题（<h3>）"
    if not answers:
        return None, f"LR_FAQ_ANSWERS 里没有 '{slug}' 这一项"
    if len(qs) != len(answers):
        return None, f"问题 {len(qs)} 条 vs 答案 {len(answers)} 条，数量不一致——人工核对后再迁"
    return {"reps": {"A": [[q, a] for q, a in zip(qs, answers)]},
            "labels": {"A": ["问题", "答案"]}}, ""


C4_COMPARE_ROWS = {
    # C4（2026-10-12 定稿）：3 页对比表线上就是空壳（LR_COMPARE 无条目）。
    # 按各页主题写全 5 行 × 4 列；comparison-hub / composite 的块内 h2 也是
    # 跑题 Shopify 残留，一并覆盖（prepend 时用覆盖后的 h2）。
    "comparison-hub": {
        "h2": "Lovart vs common ways to produce product creative",
        "rows": [
            ["Turn one brief into a full asset set", "One image per prompt, no system", "Briefs, revisions, and handoffs per asset", "Full campaign set generated from one product brief"],
            ["Keep every visual on brand", "Restyles with each generation", "Depends on who touches the file", "Brand Kit applied to every generation"],
            ["Cover every channel and format", "Manual resizing, one canvas at a time", "Per-format fees and slow turnaround", "Social, ads, email, and PDP from one concept"],
            ["Iterate on what performs", "Regenerate from scratch", "New round, new invoice", "Touch Edit the winner in place"],
            ["Ship at launch speed", "Hours of prompting", "Weeks of lead time", "Launch-ready set in minutes"],
        ],
    },
    "composite-replica-all": {
        "h2": "Lovart vs common ways to produce product creative",
        "rows": [
            ["Turn one brief into a full asset set", "One image per prompt, no system", "Briefs, revisions, and handoffs per asset", "Full campaign set generated from one product brief"],
            ["Keep every visual on brand", "Restyles with each generation", "Depends on who touches the file", "Brand Kit applied to every generation"],
            ["Cover every channel and format", "Manual resizing, one canvas at a time", "Per-format fees and slow turnaround", "Social, ads, email, and PDP from one concept"],
            ["Iterate on what performs", "Regenerate from scratch", "New round, new invoice", "Touch Edit the winner in place"],
            ["Ship at launch speed", "Hours of prompting", "Weeks of lead time", "Launch-ready set in minutes"],
        ],
    },
    "ai-design-for-small-business-hub": {
        # h2 不跑题（"Lovart vs typical local business marketing"），沿用原块
        "rows": [
            ["Look professional on every platform", "Generic templates, same as everyone", "Print-only, dated layouts", "Studio-quality designs in your brand style"],
            ["Keep brand consistent", "Colors and fonts drift per design", "Whatever the shop's template allows", "Brand Kit locked into every asset"],
            ["Update promos fast", "Redo it yourself each time", "New order, new wait", "Touch Edit when the special changes"],
            ["Cover print and digital", "Export sizes get fiddly", "Print comes first, digital is an afterthought", "Social posts, flyers, and signage from one design"],
            ["Affordable ongoing creative", "Hours you don't have", "Per-run pricing adds up", "Flat subscription, unlimited designs"],
        ],
    },
}


def _head_prepend(html, h2_override=None):
    """把对比表块内的 h2 + 副标题原样抽成独立 html 微件（prepend 用）。

    h2/sub 是 tailwind 类排版，留在 html 微件里 replica.css 继续生效，
    视觉零漂移；h2_override 时只换文字、保留原标签与类。
    块内没有 h2 时返回 []。
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return []
    soup = BeautifulSoup(html, "html.parser")
    h2 = soup.find("h2")
    if not h2:
        return []
    if h2_override:
        h2.string = h2_override
    parts = [str(h2)]
    sub = h2.find_next_sibling("p")
    if sub is not None:
        parts.append(str(sub))
    wrap = f'<div class="lr-keep-head">{"".join(parts)}</div>'
    return [{"elType": "widget", "widgetType": "html",
             "settings": {"html": wrap}, "elements": [], "isInner": False}]


def extract_comparison(html, page_file):
    """对比表：**表头在 HTML 的 <th> 里，表体在 LR_COMPARE / C4 覆盖表里**。

    A 组 = 表头（每行一列），B 组 = 表体（每行 N 列）。
    目标微件若把表头也做成重复器（EA Advanced Data Table 就是），两组都能填；
    若表头是普通字段，sample 里只填 B 组哨兵，再用 --only-group B。
    块内 h2/sub 通过 payload["prepend"] 原样保留（见 _head_prepend）。
    """
    heads = [strip_tags(x) for x in re.findall(r"<th[^>]*>(.*?)</th>", html, re.S)]
    heads = [h for h in heads if h]
    slug = slug_of(page_file)
    over = C4_COMPARE_ROWS.get(slug)
    if over:
        rows = over["rows"]
        prepend = _head_prepend(html, over.get("h2"))  # 有 h2 覆盖值才换文字
    else:
        rows = (_js_object("LR_COMPARE").get(slug) or {}).get("rows") or []
        prepend = _head_prepend(html)
    if not rows:
        return None, f"LR_COMPARE / C4 覆盖表里都没有 '{slug}'（该页对比表是空壳，需先补数据）"
    width = len(rows[0])
    if any(len(r) != width for r in rows):
        return None, f"表体各行列数不一致：{[len(r) for r in rows]}"
    if heads and len(heads) != width:
        return None, f"表头 {len(heads)} 列 vs 表体 {width} 列，不一致——人工核对后再迁"
    # EA Advanced Data Table 免费层的 static 数据源是**单 HTML 字符串槽**
    # （ea_adv_data_table_static_html，模板自带 <table> 外壳，槽内只放 thead+tbody）。
    # 多行列 → 单 HTML blob，无法按列寻址——LPagery 契约里这一模块按 blob 处理。
    if not heads:
        heads = [f"第{k + 1}列" for k in range(width)]
    thead = "<thead><tr>" + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead>"
    tbody = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody>"
    return {"reps": {"A": [[thead + tbody]]},
            "labels": {"A": ["表格 HTML（thead+tbody）"]},
            "prepend": prepend}, ""


def _money(v):
    return f"${v}" if isinstance(v, (int, float)) else str(v or "")


def extract_pricing(html, page_file):
    """定价：**整份数据都在 LR_PRICING 里**（源 HTML 是 animate-pulse 骨架，一个价格数字都没有）。

    目标微件：HT Mega `htmega-2026-pricing`（Flip Switcher Pricing Table，免费层可用）。
    **单重复器 plan_items、每档一行、双价列**（price_monthly / price_annual，渲染层
    用 `htm25-pricing--annual` class 切换显示）——所以 LR_PRICING 的月/年两组不是
    两个重复器，而是**同一行的两列**（build_node 的 A/B 组共享 rep_path 会互相
    覆盖，必须在这里合并成单组 12 列）。

    每行 12 列：档名 / 货币 / 月价 / 年价 / 计价周期 / tagline / 功能清单 / 推荐 / 徽章 / 按钮文案 / 按钮链接 / 按钮样式
    微件没有「划线原价 / 折扣 / 计费说明」字段：划线价 + 省钱钩子进 tagline
    （wp_kses_post 允许 <s>），年付计费说明进功能清单首行（默认态=annual，与真站一致）。
    """
    P = _js_object("LR_PRICING")
    M, Y = P.get("monthly") or [], P.get("yearly") or []
    if not M or not Y:
        return None, "LR_PRICING 缺 monthly/yearly 组（replica.js 结构变了？）"
    ymap = {y.get("name"): y for y in Y}
    rows = []
    for x in M:
        y = ymap.get(x.get("name"))
        if not y:
            return None, f"monthly/yearly 档名不齐：{x.get('name')}"
        # tagline = 划线原价 + 月付折扣 + 年付省钱钩子（月年共用一个槽）
        bits = []
        if x.get("original") and x["original"] != x["price"]:
            bits.append(f"<s>${x['original']}</s>" + (f" {x['off']}" if x.get("off") else ""))
        if y.get("save"):
            bits.append(y["save"])
        tagline = " · ".join(bits)
        feats = list(y.get("feats") or x.get("feats") or [])
        if y.get("bill"):
            feats.insert(0, y["bill"])   # 功能清单首行 = 年付计费说明（默认态）
        hot = bool(x.get("hot"))
        rows.append([
            str(x.get("name", "")),
            "$",
            str(x.get("price", "")),
            str(y.get("price", "")),
            "/month",
            tagline,
            "\n".join(feats),
            "yes" if hot else "",
            "Most popular" if hot else "",
            "Get started",
            "https://www.lovart.ai/canvas",
            "primary",
        ])
    labels = ["档名", "货币", "月价", "年价", "计价周期", "tagline(划线/省钱)",
              "功能清单(首行计费说明)", "推荐", "徽章", "按钮文案", "按钮链接", "按钮样式"]
    return {"reps": {"A": rows}, "labels": {"A": labels},
            "prepend": _head_prepend(html),
            "note": "定价全站共用一份（LR_PRICING），12 页填同样内容；月年切换由微件原生支持"}, ""


def _js_const(name, default=""):
    m = re.search(r"var\s+%s\s*=\s*\"([^\"]*)\"" % re.escape(name), _js_blob())
    return m.group(1) if m else default


def _fix_href(raw):
    """复刻 replica.js 的链接处理：重定向表 + 清掉 ?cb= 缓存参数。

    迁移后那段 JS 要删掉，所以必须在这里把它做过的事固化进数据，
    否则链接会退回成抓取时的旧值。
    """
    raw = (raw or "").strip()
    red = _js_object("LR_LINK_REDIRECT")
    if raw in red:
        return red[raw]
    return re.sub(r"[?&]cb=\d+", "", raw)


CTA_OVERRIDES = {
    # C2 按页覆盖表（2026-10-12 定稿）：7 页的 cta 块被同一份跑题 Shopify 文案污染
    # 且链接全为死链 #。按各页 hero 主题重写；主按钮 → canvas（同 solution 页惯例），
    # 次链接 → 站内真实页面（不用 #，迁移后没有 JS 死链兜底）。
    "comparison-hub": {
        "title": "Ready to turn one brief into every comparison your buyers search for?",
        "primary": ("Start your comparison", "https://www.lovart.ai/canvas"),
        "secondary": ("See pricing", "https://www.lovart.ai/pricing"),
    },
    "content-hub": {
        "title": "Ready to design every step from click to repeat purchase?",
        "primary": ("Start creating free", "https://www.lovart.ai/canvas"),
        "secondary": ("Explore the docs", "https://www.lovart.ai/docs"),
    },
    "product-launch": {
        "title": "Ready to take your next drop from idea to profitable launch?",
        "primary": ("Start your launch", "https://www.lovart.ai/canvas"),
        "secondary": ("See pricing", "https://www.lovart.ai/pricing"),
    },
    "showcase-gallery": {
        "title": "Ready to start anywhere in the stack?",
        "primary": ("Open the canvas", "https://www.lovart.ai/canvas"),
        "secondary": ("See pricing", "https://www.lovart.ai/pricing"),
    },
    "tool-directory": {
        "title": "Ready to fix your creative leaks for good?",
        "primary": ("Start fixing today", "https://www.lovart.ai/canvas"),
        "secondary": ("Browse the docs", "https://www.lovart.ai/docs"),
    },
    "people-reviews": {
        "title": "Ready to write your own five-star story?",
        "primary": ("Start your free trial", "https://www.lovart.ai/canvas"),
        "secondary": ("See pricing", "https://www.lovart.ai/pricing"),
    },
    "composite": {
        "title": "Ready to design at the speed of thought?",
        "primary": ("Start creating now", "https://www.lovart.ai/canvas"),
        "secondary": ("See pricing", "https://www.lovart.ai/pricing"),
    },
}


def extract_cta(html, page_file):
    """CTA：内容在 HTML 里，但**主按钮没有 href** —— 目标由 replica.js 给（LR_CANVAS）。

    5 列：标题 / 主按钮文案 / 主按钮链接 / 次链接文案 / 次链接链接

    两道跳过闸（实测出来的真实问题，不是防御性编程）：
    1. 5 个页面的 cta 块把整个站点页脚吞进去了（19 个链接含 Pricing/Docs/Terms/社交）。
       直接换成 CTA 微件会让这些页的页脚消失 —— 页脚该用 Theme Builder 单独做。
    2. composite / people-reviews 两页的 CTA 全是死链 #，文案还是别页的
       （Shopify 文案出现在人物评价页上）。需人工定文案后再迁。

    C2 解法（2026-10-12）：上面 7 页的文案在 CTA_OVERRIDES 按页定稿。
    命中覆盖表的页面不再看闸 —— 覆盖文案就是人工定稿，直接产出。
    跑题的 Shopify 文案留在 elem-src 原样不动（不污染源）。
    """
    # C1 已由 split-footer.py 拆页脚；但若块仍吞页脚（源未拆），照旧拦
    links = [(u, strip_tags(t)) for u, t in
             re.findall(r"<a[^>]*href=\"([^\"]*)\"[^>]*>(.*?)</a>", html, re.S)]
    links = [(u, t) for u, t in links if t]

    slug = re.sub(r"\.json$", "", page_file or "")
    slug = re.sub(r"^lr-demo-(native|faithful)-", "", slug)
    slug = re.sub(r"^replica-", "", slug)
    slug = re.sub(r"^composite-replica-all$", "composite", slug)
    ov = CTA_OVERRIDES.get(slug)
    if ov is not None:
        canvas = _js_const("LR_CANVAS", "https://www.lovart.ai/canvas")
        prim_t, prim_u = ov["primary"]
        sec_t, sec_u = ov["secondary"]
        if prim_u == "__CANVAS__":
            prim_u = canvas
        if sec_u == "__CANVAS__":
            sec_u = canvas
        return {"reps": {"A": [[ov["title"], prim_t, prim_u, sec_t, sec_u]]},
                "labels": {"A": ["标题", "主按钮文案", "主按钮链接", "次链接文案", "次链接链接"]},
                "page_note": "C2 覆盖文案（跑题 Shopify 文案已弃用）"}, ""

    if "statement/privacy-policy" in html or len(links) > 4:
        return None, (f"该页 CTA 块吞进了站点页脚（{len(links)} 个链接）——"
                      f"换成微件会让页脚消失。页脚请用 Elementor Theme Builder 单独做，拆出来后再迁")

    heads = [strip_tags(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)]
    heads = [h for h in heads if h]
    if not heads:
        return None, "没抓到标题（<h2>）"

    btns = [strip_tags(x) for x in re.findall(r"<button[^>]*>(.*?)</button>", html, re.S)]
    btns = [b for b in btns if 3 < len(b) < 60]
    if not btns and all((u or "#") in ("#", "") for u, _ in links):
        return None, ("CTA 全是死链 #，且文案疑似跑错主题（见交接文档 §零）——"
                      "需人工确认文案与目标后再迁")

    canvas = _js_const("LR_CANVAS", "https://www.lovart.ai/canvas")
    if btns:
        # 主按钮无 href，线上靠 JS 跳 canvas；迁移后 JS 会删，所以这里写死目标
        prim_t, prim_u = btns[0], canvas
        sec_t, sec_u = (links[0][1], _fix_href(links[0][0])) if links else ("", "")
    else:
        prim_t, prim_u = links[0][1], _fix_href(links[0][0])
        sec_t, sec_u = (links[1][1], _fix_href(links[1][0])) if len(links) > 1 else ("", "")

    note = ""
    if sec_t and sec_u in ("#", ""):   # 本来就没有次链接时不该报警
        note = f"次链接「{sec_t}」原本是死链 #，迁移后需补目标"
        sec_u = ""
    return {"reps": {"A": [[heads[0], prim_t, prim_u, sec_t, sec_u]]},
            "labels": {"A": ["标题", "主按钮文案", "主按钮链接", "次链接文案", "次链接链接"]},
            "page_note": note}, ""


def extract_workflow(html, page_file):
    """Workflow：步骤（序号/标题/描述）就在 HTML 里；横向纵向都按步骤序列抽。

    目标微件：HT Mega Vertical Timeline（htmega-verticletimeline-addons），
    重复器 custom_content_list，三列 = content_date（步骤号）/ content_title / content_text。

    两道闸与一个如实原则：
    1. 跑题闸：tool-directory / composite 横向块整段是 Shopify 通用 how-to 文案
       （C2 同类问题），如实迁移会把错文案固化进微件，拦下等人工定稿。
    2. 描述缺失不算错配：源站 hydration 缺失导致 9 个块的步骤 2/3 没有描述，
       但**线上现状渲染出来也是空的**——如实迁移留空，不劣化（C5 补内容后再编辑）。
    """
    joined = re.sub(r"\s+", " ", html)
    if "How-to workflow" in joined or "merchants who want" in joined:
        return None, ("该块是跑题的 Shopify 通用 how-to 文案（C2 同类）——"
                      "如实迁移会固化错文案，需人工定稿后再迁")

    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "|", html))
    parts = [p.strip() for p in plain.split("|") if p.strip()]
    steps, cur = [], None
    for p in parts:
        if re.fullmatch(r"[1-9]", p):
            cur = [p, "", ""]
            steps.append(cur)
        elif cur is not None:
            if not cur[1]:
                cur[1] = p
            else:
                cur[2] = (cur[2] + " " + p).strip()
    if not steps:
        return None, "没抽到步骤（HTML 里没有 1/2/3 序号标记）"
    for s in steps:
        s[2] = re.sub(r"&#x27;", "'", s[2]).replace("&amp;", "&")
        s[1] = s[1].replace("&amp;", "&")
    empty_desc = sum(1 for s in steps if not s[2])
    note = (f"{empty_desc}/{len(steps)} 个步骤描述缺失（源站 hydration 缺失，现状渲染同样为空，C5 补）"
            if empty_desc else "")
    rows = [s[:] for s in steps]
    return {"reps": {"A": rows},
            "labels": {"A": ["步骤号", "步骤标题", "步骤描述"]},
            "page_note": note}, ""


C3_TABS_FILE = ROOT / "c3-tabs-content.json"


def extract_capability_tabs(html, page_file):
    """capability-tabs：源站 4 个 tab 只有面板 1 有内容（hydration 缺失），tab 点不动
    （无 role=tablist，replica.js 也无兜底）。内容表 c3-tabs-content.json 提供
    面板 1 原样 HTML（骨架脚本抽的，含图与 tailwind 类）+ 补写的面板 2/3/4。

    目标微件：EA Advanced Tabs（eael-adv-tabs），重复器 eael_adv_tabs_tab，
    4 列 = 标签 / 内容 HTML / tab_id / 默认激活。

    内容来源三层：标签——HTML 按钮（无按钮的页用内容表）；面板 1——HTML 原样
    （无原样的页用内容表）；面板 2/3/4——内容表（C3，2026-10-12 定稿）。
    """
    labels_src = [strip_tags(x) for x in
                  re.findall(r'<button[^>]*>(.*?)</button>', html, re.S)]
    labels_src = [H.unescape(x).strip() for x in labels_src]
    labels_src = [x for x in labels_src if x and len(x) < 60]

    h2m = re.search(r"<h2[^>]*>(.*?)</h2>", html, re.S)
    h2 = H.unescape(strip_tags(h2m.group(1))).strip() if h2m else ""
    prepend = [{"elType": "widget", "widgetType": "html",
                "settings": {"html": f'<div class="lr-keep-head"><h2>{h2}</h2></div>'},
                "elements": [], "isInner": False}] if h2 else []

    slug_key = (page_file or "").removesuffix(".json")
    table = (json.loads(C3_TABS_FILE.read_text(encoding="utf-8")).get(slug_key)
             if C3_TABS_FILE.exists() else None)
    if not table:
        return None, f"c3-tabs-content.json 里没有 '{slug_key}' 的内容（C3 未定稿）"

    labels = labels_src or table["labels"]
    if len(labels) != 4:
        return None, f"标签数 {len(labels)} ≠ 4（HTML 给 {len(labels_src)}，内容表给 {len(table['labels'])}）"

    # 面板 1：优先原样 HTML（保图与 tailwind 类），否则内容表
    panels = [table["panel1_html"] or table["panels_html"].get("0", "")]
    panels += [table["panels_html"].get(str(k), "") for k in range(1, 4)]
    if not all(panels):
        return None, "有面板内容为空——查 c3-tabs-content.json"

    short = slug_key.replace("replica-solution-", "").replace("replica-", "")[:18]
    rows = []
    for k in range(4):
        rows.append([
            labels[k],
            panels[k],
            f"eael-tab-{k + 1}-{short}",
            "active-default" if k == 0 else "inactive",
        ])
    return {"reps": {"A": rows},
            "labels": {"A": ["标签", "内容HTML", "tab_id", "默认激活"]},
            "prepend": prepend}, ""


C6_TM_FILE = ROOT / "c6-testimonials-content.json"


def extract_testimonial(html, page_file):
    """testimonial：轮播型引言块（大引文 + 作者行 + 圆点切换）。

    内容现状（2026-10-12 实测）：10 页里只有 4 条真实评价存活于源 HTML
    （composite/showcase 同一条 Maya Lin、small-business Kenji M.、nonprofits
    Erika Schroeder），其余全部是 hydration 缺失的空壳（引文空、名字空，
    线上现状渲染同样为空）。内容表 c6-testimonials-content.json 每页 3 条：
    真实条目嵌回，缺口按页主题补写（C6，2026-10-12 定稿）。

    目标微件：HT Mega `htmega-2026-testimonials`，重复器 testimonial_items，
    5 列 = 引文 / 评分 / 名字 / 头衔公司 / （空槽，author_company 一并放头衔列）。
    """
    def _long_ps(seg):
        cl = lambda x: H.unescape(re.sub(r"<[^>]+>", " ", x)).strip()
        return [re.sub(r"\s+", " ", cl(x)) for x in re.findall(r"<p[^>]*>(.*?)</p>", seg, re.S)]

    seg = html[html.find('data-lp-section="testimonial"'):] if 'data-lp-section="testimonial"' in html else html
    real = [t for t in _long_ps(seg) if 40 < len(t) < 400]

    slug_key = (page_file or "").removesuffix(".json")
    table = (json.loads(C6_TM_FILE.read_text(encoding="utf-8")).get(slug_key)
             if C6_TM_FILE.exists() else None)
    if not table:
        return None, f"c6-testimonials-content.json 里没有 '{slug_key}'（C6 未定稿）"

    # 真实存活条目只在内容表首条缺失时兜底（表首条即抄自真实条目，通常已覆盖）
    out = []
    for k, item in enumerate(table):
        q, n_, r_ = item["q"], item["n"], item["r"]
        if k == 0 and not table and real:
            q = real[0]
        out.append([q, "5", n_, r_, ""])
    return {"reps": {"A": out},
            "labels": {"A": ["引文", "评分", "名字", "头衔", "公司"]}}, ""


MODULES = {
    # data-lp-section 的值 → 内容抽取函数
    "faq": extract_faq,
    "comparison-table": extract_comparison,
    "pricing-block": extract_pricing,
    "cta-default": extract_cta,
    "workflow": extract_workflow,
    "capability-tabs": extract_capability_tabs,
    "testimonial": extract_testimonial,
}


# ───────────────────────── 主流程 ─────────────────────────
def _fmt_reps(sample):
    out = []
    for grp, rep in sample["reps"].items():
        kind = ("平铺字段" if rep.get("flat")
                else f"重复器 {''.join(repr([x]) for x in rep['rep_path'])}")
        out.append(f"  {grp} 组 · {kind} · {len(rep['field_paths'])} 个字段槽")
        for ix, fp in enumerate(rep["field_paths"], 1):
            out.append(f"      第{ix}列 → {'.'.join(map(str, fp))}")
    return "\n".join(out)


def migrate(args):
    sample = load_sample(args.sample)
    if args.inspect:
        print("sample 解析结果：")
        print(f"  widgetType : {sample['widget_type']}")
        print(_fmt_reps(sample))
        tpl = {g: (list(r["item_tpl"].keys()) if r.get("item_tpl") else "（平铺，无行模板）")
               for g, r in sample["reps"].items()}
        print(f"  行模板键   : {tpl}")
        return 0

    extractor = MODULES.get(args.module)
    if not extractor:
        raise SystemExit(f"✗ 未支持的模块 '{args.module}'，已支持：{', '.join(MODULES)}")

    src, out = ROOT / args.src, ROOT / args.out
    # 模块名允许带布局变体（如 workflow → workflow-vertical/horizontal）
    marker_re = re.compile(r'data-lp-section="%s(?:-[a-z0-9-]+)?"' % re.escape(args.module))
    report, totals = [], {"pages": 0, "replaced": 0, "skipped": 0, "rows": 0}
    preview, note, done = None, "", set()

    chained = 0
    for f in sorted(src.glob("*.json")):
        # 链式迁移：同一页已被上一个模块迁过就接着改它，否则从源读。
        # 不这么做，第二个模块会用源文件覆盖掉第一个模块的成果（静默丢工作）。
        cur = out / f.name
        if cur.exists() and cur != f:
            f_read, chained = cur, chained + 1
        else:
            f_read = f
        raw = json.loads(f_read.read_text(encoding="utf-8"))
        data = raw.get("data") if isinstance(raw, dict) else raw
        if not isinstance(data, list):
            continue
        hits = []

        def visit(node, parent, i):
            if node.get("widgetType") != "html":
                return
            html = (node.get("settings") or {}).get("html", "")
            if marker_re.search(html):
                hits.append((node, parent, i, html))

        walk_widgets(data, visit)
        if not hits:
            continue
        totals["pages"] += 1
        changed = 0

        for node, parent, i, html in hits:
            payload, why = extractor(html, f.name)
            if not payload:
                totals["skipped"] += 1
                report.append((f.name, "skip", why))
                continue
            reps = payload["reps"]
            if args.only_group:
                reps = {g: v for g, v in reps.items() if g in args.only_group}
                if not reps:
                    totals["skipped"] += 1
                    report.append((f.name, "skip", f"--only-group {args.only_group} 过滤后无数据"))
                    continue
            try:
                new_node = build_node(sample, reps, args.allow_truncate)
            except ValueError as e:
                totals["skipped"] += 1
                report.append((f.name, "skip", str(e)))
                continue
            # payload["prepend"]（如对比表的 h2/副标题）：原样保留成独立 html 微件，
            # 插在数据微件前——逆序 insert(i) 使其最终按原顺序排在 i、i+1、…
            pre = payload.get("prepend") or []
            for pn in reversed(pre):
                ins = json.loads(json.dumps(pn))
                ins["id"] = eid()
                parent.insert(i, ins)
            parent[i + len(pre)] = new_node
            n = sum(len(v) for v in reps.values())
            changed += 1
            totals["replaced"] += 1
            totals["rows"] += n
            msg = " + ".join(f"{g}组{len(v)}行" for g, v in reps.items())
            if payload.get("page_note"):
                msg += f" ⚠ {payload['page_note']}"
            report.append((f.name, "ok", msg))
            if preview is None:
                preview = (payload.get("labels") or {}, reps)
                note = payload.get("note", "")

        # 一块都没换成的页面不写出：保证「out 目录里的文件 = 已迁移的文件」
        if changed:
            done.add(f.name)
        if args.write and changed:
            out.mkdir(parents=True, exist_ok=True)
            (out / f.name).write_text(
                json.dumps(raw, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # ── 终端报告 ──
    print(f"\n模块 {args.module} → {sample['widget_type']}"
          f"{'' if args.write else '（预演，未写文件）'}")
    if note:
        print(f"注意：{note}")
    print(f"{'页面':<46} {'结果':<6} 说明")
    print("-" * 96)
    for name, st, why in report:
        print(f"{name:<46} {'✓' if st == 'ok' else '—':<6} {why}")
    print("-" * 96)
    print(f"命中 {totals['pages']} 页 · 替换 {totals['replaced']} 块 · "
          f"跳过 {totals['skipped']} 块 · 共 {totals['rows']} 行")
    if chained:
        print(f"（其中 {chained} 页接续了 {out.name}/ 里上一个模块的成果）")

    # ── 内容预览：N 列很容易错位，写盘前必须肉眼能核 ──
    if preview:
        labels, reps = preview
        print("\n首个成功页面的内容预览（核对列是否对齐）：")
        for grp, rows in reps.items():
            lab = labels.get(grp) or []
            print(f"  [{grp} 组]")
            for r in rows[:3]:
                for ix, v in enumerate(r):
                    name = lab[ix] if ix < len(lab) else f"第{ix + 1}列"
                    txt = str(v).replace("\n", " / ")
                    print(f"    {name:<10} {txt[:78]}{'…' if len(txt) > 78 else ''}")
                print()
            if len(rows) > 3:
                print(f"    （其余 {len(rows) - 3} 行略）\n")

    md = ROOT / f"migration-report-{args.module}.md"
    md.write_text(
        f"# {args.module} 迁移报告\n\n"
        f"- 目标微件：`{sample['widget_type']}`\n"
        f"- 字段映射：\n```\n{_fmt_reps(sample)}\n```\n"
        + (f"- 注意：{note}\n" if note else "")
        + f"- 命中 {totals['pages']} 页 / 替换 {totals['replaced']} 块 / "
          f"跳过 {totals['skipped']} 块 / 共 {totals['rows']} 行\n"
          f"- 模式：{'写出到 ' + args.out if args.write else '预演（未写文件）'}\n\n"
          "| 页面 | 结果 | 说明 |\n|---|:--:|---|\n"
        + "".join(f"| {n} | {'✓' if st == 'ok' else '—'} | {w} |\n" for n, st, w in report)
        + f"\n## 替换成功后的收尾\n\n"
          f"导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入"
          f"（faq → `initFaqFill`，comparison-table → `initCompareFill`，"
          f"pricing-block → `initPricingRender`）及其硬编码数据表"
          f"（`LR_FAQ_ANSWERS` / `LR_COMPARE` / `LR_PRICING`），并 bump 版本号。\n"
          f"**replica.js 行数单调下降 = 这条路走对了。**\n",
        encoding="utf-8")
    print(f"报告：{md.relative_to(ROOT)}")

    if args.write and totals["replaced"]:
        bad = self_check(out, sample, args.module, only=done)
        if bad:
            print("\n✗ 自检未通过，产出不可用：")
            for b in bad:
                print("   ", b)
            return 1
        print(f"自检通过：本轮 {len(done)} 个文件，"
              f"无哨兵残留 / 无空行 / id 无重复 / 原 html 块已清除")

    if totals["skipped"]:
        print("\n跳过的块需人工核对后再迁——脚本不做截断配对，避免产出错配内容。")
    return 0


def self_check(out_dir, sample, module="faq", only=None):
    """产出自检。这些都是会静默毁掉一整批页面的错误，必须当场拦住。

    only = 本轮真替换过的文件名集合。必须限定范围——链式迁移时 out 目录里还有
    上一轮迁的、本轮跳过的页面，它们当然还留着本模块的 html 块，全目录扫会误报。
    """
    bad = []
    marker_re = re.compile(r'data-lp-section="%s(?:-[a-z0-9-]+)?"' % re.escape(module))
    for f in sorted(Path(out_dir).glob("*.json")):
        if only is not None and f.name not in only:
            continue
        raw = json.loads(f.read_text(encoding="utf-8"))
        data = raw.get("data") if isinstance(raw, dict) else raw
        blob = json.dumps(data, ensure_ascii=False)
        ids, targets, html_blobs = [], [], []

        def visit(n, p, i):
            if n.get("elType") == "widget":
                ids.append(n.get("id"))
            if n.get("widgetType") == sample["widget_type"]:
                targets.append(n)
            # 必须查原始 html 字符串，不能查 json.dumps 的结果——
            # JSON 里引号会被转义成 \" ，用带引号的 marker 去匹配永远不中（曾静默漏报）
            if n.get("widgetType") == "html":
                html_blobs.append((n.get("settings") or {}).get("html", ""))

        walk_widgets(data, visit)
        if SENTINEL_RE.search(blob) or any(v in blob for v in LEGACY_ALIAS):
            bad.append(f"{f.name}: 哨兵文本泄漏到产出里")
        if not targets and any(marker_re.search(h) for h in html_blobs):
            # 一个该模块微件都没换成、却还留着原块 = 替换失败。
            # 注意不能按整页判：同页同模块多块时（如 composite 的横/纵两个 workflow），
            # 部分块被 C2 闸刻意跳过是预期状态，不算失败。
            bad.append(f"{f.name}: 原 widget-html 块没被清除")
        if len(ids) != len(set(ids)):
            bad.append(f"{f.name}: 微件 id 有重复（Elementor 会渲染异常）")
        for t in targets:
            for grp, rep in sample["reps"].items():
                if rep.get("flat"):
                    v = t
                    try:
                        v = dig(t, rep["field_paths"][0])
                    except Exception:
                        v = ""
                    if not str(v).strip():
                        bad.append(f"{f.name}: {grp} 组首个字段为空")
                    continue
                try:
                    rows = dig(t, rep["rep_path"])
                except Exception:
                    continue
                rid = [r.get("_id") for r in rows if isinstance(r, dict)]
                if rid and len(rid) != len(set(rid)):
                    bad.append(f"{f.name}: {grp} 组重复器行 _id 有重复")
                for r in rows:
                    first = rep["field_paths"][0]
                    v = r
                    for seg in first:
                        v = v.get(seg, "") if isinstance(v, dict) else ""
                    if not str(v).strip():
                        bad.append(f"{f.name}: {grp} 组有空的首列")
                        break
    return bad


def main():
    ap = argparse.ArgumentParser(description="widget-html → 原生微件 批量替换（预演优先）")
    ap.add_argument("--module", default="faq", help=f"要替换的模块：{', '.join(MODULES)}")
    ap.add_argument("--sample", required=True, help="手搭微件导出的 JSON（含哨兵）")
    ap.add_argument("--src", default="elem-src", help="源模板目录")
    ap.add_argument("--out", default="elem-migrated", help="产出目录（不覆盖源）")
    ap.add_argument("--write", action="store_true", help="真写文件（默认只预演）")
    ap.add_argument("--inspect", action="store_true", help="只解析 sample 并打印字段映射")
    ap.add_argument("--only-group", default="", metavar="A|B|AB",
                    help="只迁指定重复器组（目标微件只有一个重复器时用）")
    ap.add_argument("--allow-truncate", action="store_true",
                    help="抽取列数多于 sample 字段槽时，明确接受丢列")
    return migrate(ap.parse_args())


if __name__ == "__main__":
    sys.exit(main())
