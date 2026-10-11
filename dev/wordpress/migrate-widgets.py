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
import json
import re
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SENTINELS = {"t1": "__T1__", "c1": "__C1__", "t2": "__T2__", "c2": "__C2__"}


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
def find_path(obj, needle, path=()):
    """在嵌套结构里找到哨兵文本所在的完整路径。"""
    if isinstance(obj, str):
        return [path] if needle in obj else []
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out += find_path(v, needle, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += find_path(v, needle, path + (i,))
    return out


def load_sample(path):
    """读手搭样本 → 得到 {widget_type, settings 模板, repeater_key, title_key, content_key}。

    不依赖任何插件的键名约定，全靠哨兵反查。
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    data = raw.get("data", raw) if isinstance(raw, dict) else raw
    found = []
    walk_widgets(data if isinstance(data, list) else [data],
                 lambda n, p, i: found.append(n))
    if not found:
        raise SystemExit(f"✗ sample 里没有 widget 节点：{path}")
    # 取含哨兵的那个；没有就取第一个（--inspect 时方便看）
    w = next((x for x in found if SENTINELS["t1"] in json.dumps(x, ensure_ascii=False)), found[0])

    p_t1 = find_path(w, SENTINELS["t1"])
    p_c1 = find_path(w, SENTINELS["c1"])
    p_t2 = find_path(w, SENTINELS["t2"])
    if not (p_t1 and p_c1):
        raise SystemExit(
            "✗ sample 里找不到哨兵 __T1__ / __C1__。\n"
            "  请在编辑器里把第 1 行标题填 __T1__、正文填 __C1__，"
            "第 2 行填 __T2__ / __C2__，再导出。")

    t1, c1 = p_t1[0], p_c1[0]
    # 重复器：t1 路径里第一个 int 下标，它前面那一段就是 repeater 的 key 路径
    idx = next((i for i, seg in enumerate(t1) if isinstance(seg, int)), None)
    if idx is None:
        raise SystemExit("✗ 哨兵不在重复器里——这个微件可能不是 repeater 结构，需要单独适配。")
    rep_path, item_i = t1[:idx], t1[idx]
    title_key, content_key = t1[idx + 1:], c1[idx + 1:]
    if c1[:idx] != rep_path:
        raise SystemExit("✗ 标题与正文不在同一个重复器里，无法自动配对。")
    if not p_t2:
        print("  ! 警告：没找到 __T2__，无法确认这是重复器（只有一行也可能解析对）", file=sys.stderr)

    def dig(o, path):
        for s in path:
            o = o[s]
        return o

    return {
        "widget_type": w.get("widgetType"),
        "widget": w,
        "rep_path": list(rep_path),
        "item_tpl": json.loads(json.dumps(dig(w, list(rep_path))[item_i])),  # 深拷贝一行当模板
        "title_key": list(title_key),
        "content_key": list(content_key),
    }


def set_in(obj, path, value):
    for s in path[:-1]:
        obj = obj[s]
    obj[path[-1]] = value


def build_node(sample, items):
    """按 sample 的形状造一个新微件节点，重复器填 items=[(title, content), ...]。"""
    node = json.loads(json.dumps(sample["widget"]))
    node["id"] = eid()
    rows = []
    for title, content in items:
        row = json.loads(json.dumps(sample["item_tpl"]))
        if "_id" in row:
            row["_id"] = eid()
        set_in(row, sample["title_key"], title)
        set_in(row, sample["content_key"], content)
        rows.append(row)
    target = node
    for s in sample["rep_path"][:-1]:
        target = target[s]
    target[sample["rep_path"][-1]] = rows
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
    """FAQ：问题在 HTML 的 <h3> 里，答案在 replica.js 的 LR_FAQ_ANSWERS 里（按序配对）。

    实测 12 个页面问题数与答案数完全一致，故按顺序 zip 是安全的；
    数量不一致时直接报错，不做截断——宁可不迁移，也不产出错配内容。
    """
    qs = [strip_tags(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S)]
    qs = [q for q in qs if 10 < len(q) < 200]
    answers = _js_object("LR_FAQ_ANSWERS").get(slug_of(page_file), [])
    if not qs:
        return None, "HTML 里没抓到问题（<h3>）"
    if not answers:
        return None, f"LR_FAQ_ANSWERS 里没有 '{slug_of(page_file)}' 这一项"
    if len(qs) != len(answers):
        return None, f"问题 {len(qs)} 条 vs 答案 {len(answers)} 条，数量不一致——人工核对后再迁"
    return list(zip(qs, answers)), ""


MODULES = {
    # data-lp-section 的值 → 内容抽取函数
    "faq": extract_faq,
}


# ───────────────────────── 主流程 ─────────────────────────
def migrate(args):
    sample = load_sample(args.sample)
    if args.inspect:
        print("sample 解析结果：")
        print(f"  widgetType : {sample['widget_type']}")
        print(f"  重复器路径 : settings{''.join(repr([s]) for s in sample['rep_path'])}")
        print(f"  标题字段   : {'.'.join(map(str, sample['title_key']))}")
        print(f"  正文字段   : {'.'.join(map(str, sample['content_key']))}")
        print(f"  行模板键   : {list(sample['item_tpl'].keys())}")
        return 0

    extractor = MODULES.get(args.module)
    if not extractor:
        raise SystemExit(f"✗ 未支持的模块 '{args.module}'，已支持：{', '.join(MODULES)}")

    src = ROOT / args.src
    out = ROOT / args.out
    marker = f'data-lp-section="{args.module}"'
    report, totals = [], {"pages": 0, "replaced": 0, "skipped": 0}

    for f in sorted(src.glob("*.json")):
        raw = json.loads(f.read_text(encoding="utf-8"))
        data = raw.get("data") if isinstance(raw, dict) else raw
        if not isinstance(data, list):
            continue
        hits = []

        def visit(node, parent, i):
            if node.get("widgetType") != "html":
                return
            html = (node.get("settings") or {}).get("html", "")
            if marker in html:
                hits.append((node, parent, i, html))

        walk_widgets(data, visit)
        if not hits:
            continue
        totals["pages"] += 1
        changed = 0

        for node, parent, i, html in hits:
            items, why = extractor(html, f.name)
            if not items:
                totals["skipped"] += 1
                report.append((f.name, "skip", why, 0))
                continue
            parent[i] = build_node(sample, items)
            changed += 1
            totals["replaced"] += 1
            report.append((f.name, "ok", f"{len(items)} 条", len(items)))

        # 一块都没换成的页面不写出：保证「out 目录里的文件 = 已迁移的文件」
        if args.write and changed:
            out.mkdir(parents=True, exist_ok=True)
            (out / f.name).write_text(
                json.dumps(raw, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # ── 报告 ──
    print(f"\n模块 {args.module} → {sample['widget_type']}"
          f"{'' if args.write else '（预演，未写文件）'}")
    print(f"{'页面':<46} {'结果':<6} 说明")
    print("-" * 92)
    for name, st, why, _ in report:
        print(f"{name:<46} {'✓' if st == 'ok' else '—':<6} {why}")
    print("-" * 92)
    print(f"命中 {totals['pages']} 页 · 替换 {totals['replaced']} 块 · 跳过 {totals['skipped']} 块")

    md = ROOT / f"migration-report-{args.module}.md"
    md.write_text(
        f"# {args.module} 迁移报告\n\n"
        f"- 目标微件：`{sample['widget_type']}`\n"
        f"- 重复器：`{'.'.join(map(str, sample['rep_path']))}`，"
        f"标题 `{'.'.join(map(str, sample['title_key']))}`，"
        f"正文 `{'.'.join(map(str, sample['content_key']))}`\n"
        f"- 命中 {totals['pages']} 页 / 替换 {totals['replaced']} 块 / 跳过 {totals['skipped']} 块\n"
        f"- 模式：{'写出到 ' + args.out if args.write else '预演（未写文件）'}\n\n"
        "| 页面 | 结果 | 说明 |\n|---|:--:|---|\n"
        + "".join(f"| {n} | {'✓' if s == 'ok' else '—'} | {w} |\n" for n, s, w, _ in report)
        + f"\n## 替换成功后的收尾\n\n"
          f"导入验证无误后，删掉 `assets-src/lovart-replica.js` 里对应的运行时注入函数"
          f"（{args.module} → `init{args.module.capitalize()}Fill`），并 bump 版本号。\n"
          f"**replica.js 行数单调下降 = 这条路走对了。**\n",
        encoding="utf-8")
    print(f"报告：{md.relative_to(ROOT)}")

    if args.write and totals["replaced"]:
        bad = self_check(out, sample)
        if bad:
            print("\n✗ 自检未通过，产出不可用：")
            for b in bad:
                print("   ", b)
            return 1
        print(f"自检通过：{out.name} 下 {len(list(out.glob('*.json')))} 个文件，"
              f"无哨兵残留 / 无空行 / id 无重复 / 原 html 块已清除")

    if totals["skipped"]:
        print("\n跳过的块需要人工核对后再迁——脚本不做截断配对，避免产出错配内容。")
    return 0


def self_check(out_dir, sample, module="faq"):
    """产出自检。这些都是会静默毁掉一整批页面的错误，必须当场拦住。"""
    bad = []
    marker = f'data-lp-section="{module}"'
    for f in sorted(Path(out_dir).glob("*.json")):
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
        if any(v in blob for v in SENTINELS.values()):
            bad.append(f"{f.name}: 哨兵文本泄漏到产出里")
        if any(marker in h for h in html_blobs):
            bad.append(f"{f.name}: 原 widget-html 块没被清除")
        if len(ids) != len(set(ids)):
            bad.append(f"{f.name}: 微件 id 有重复（Elementor 会渲染异常）")
        for t in targets:
            rows = t
            for seg in sample["rep_path"]:
                rows = rows[seg]
            rid = [r.get("_id") for r in rows]
            if len(rid) != len(set(rid)):
                bad.append(f"{f.name}: 重复器行 _id 有重复")
            for r in rows:
                for key, label in ((sample["title_key"], "标题"), (sample["content_key"], "正文")):
                    v = r
                    for seg in key:
                        v = v.get(seg, "") if isinstance(v, dict) else ""
                    if not str(v).strip():
                        bad.append(f"{f.name}: 有空{label}行")
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
    return migrate(ap.parse_args())


if __name__ == "__main__":
    sys.exit(main())
