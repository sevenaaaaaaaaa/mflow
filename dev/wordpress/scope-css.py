#!/usr/bin/env python3
"""scope-css.py — 把复刻用全量序列化 CSS 作用域化到 .lr 包裹类下（tinycss2 版）。

解决的问题（复刻四毛病的根治层）：
1. 样式互踩：原 CSS 有 :root/html/body 顶层规则，内联进 WP 页面后全文档
   生效，与博客主题互相覆盖（254 条 html/body 规则实锤）。
2. 配色漂移：深色覆盖块 `:root, .dark{...}` 无条件挂 :root——收敛为
   `.lr.dark{...}`，由页面包裹类决定明暗，与主站 class-based dark 同构。

映射规则：
  :root / html / body          → .lr
  .dark / html.dark / body.dark → .lr.dark
  .dark <后代> / html.dark <后代> → .lr.dark <后代>
  :root <后代>（如 ":root :where(x)"）→ .lr <后代>
  其他选择器                    → .lr <选择器>
  @font-face/@keyframes/@property/@counter-style 原样保留
  @media/@supports/@container/@layer/@scope 递归处理

用法：
  python3 scope-css.py <in.css> <out.css> [--wrapper .lr]

依赖：tinycss2（pip install tinycss2）——手写解析器在 @layer 内引号嵌套
处会失步（实测 343KB utilities 层吞掉后续全部规则），必须用正经解析器。
"""
import argparse
import re
import sys

import tinycss2

NESTED_AT = {"media", "supports", "container", "layer", "scope"}
KEEP_AT = {"font-face", "keyframes", "-webkit-keyframes", "property", "counter-style", "import", "charset", "namespace", "page", "font-feature-values"}


def sel_text(selectors):
    return tinycss2.serialize(selectors).strip()


def scope_selector(sel, wrapper, dark_wrapper):
    """单个（逗号已拆分）选择器 → 作用域化。"""
    s = re.sub(r"\s+", " ", sel.strip())
    if s in (":root", "html", "body", "html.dark", "body.dark"):
        return wrapper
    if s in (".dark", ":root.dark", ":root .dark"):
        return dark_wrapper
    # :root <后代> → wrapper <后代>（WP block-library 常见写法 ":root :where(x)"）
    if s.startswith(":root "):
        rest = s[len(":root "):].strip()
        if rest in ("html", "body"):
            return wrapper
        return f"{wrapper} {rest}"
    # html.dark/body.dark 前缀复合
    m = re.match(r"^(?:html|body)\.dark[ .>+~]+(.*)$", s)
    if m:
        return f"{dark_wrapper} {m.group(1)}".strip()
    # .dark 前缀
    m = re.match(r"^\.dark[ .>+~]+(.*)$", s)
    if m:
        return f"{dark_wrapper} {m.group(1)}".strip()
    # 裸通配/伪元素/普通类等
    return f"{wrapper} {s}".strip()


def scope_prelude(prelude_tokens, wrapper, dark_wrapper):
    text = sel_text(prelude_tokens)
    if not text:
        return None
    # 按顶层逗号切分（括号感知）
    parts, buf, depth, in_str = [], "", 0, None
    for ch in text:
        if in_str:
            buf += ch
            if ch == in_str:
                in_str = None
            continue
        if ch in ("'", '"'):
            in_str = ch
            buf += ch
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(buf)
            buf = ""
            continue
        buf += ch
    parts.append(buf)
    sels = [p.strip() for p in parts if p.strip()]
    if not sels:
        return None
    norm = {re.sub(r"\s+", "", x) for x in sels}
    # 深色覆盖块整体形态：{:root, .dark} → 只挂 dark wrapper
    if norm in ({":root", ".dark"}, {":root", ":root.dark"}):
        return dark_wrapper
    return ", ".join(scope_selector(x, wrapper, dark_wrapper) for x in sels)


def process(nodes, wrapper, dark_wrapper, out):
    for node in nodes:
        if node.type in ("comment", "whitespace"):
            continue
        if node.type == "at-rule":
            at = (node.lower_at_keyword or "")
            if at in KEEP_AT:
                out.append(tinycss2.serialize([node]))
                continue
            if at in NESTED_AT:
                head = f"@{node.at_keyword}"
                pre = tinycss2.serialize(node.prelude).strip()
                inner = process(tinycss2.parse_rule_list(node.content), wrapper, dark_wrapper, [])
                out.append(f"{head} {pre} {{\n{inner}\n}}")
                continue
            # 未知 at-rule：整体保留（宁多勿失）
            out.append(tinycss2.serialize([node]))
            continue
        if node.type == "qualified-rule":
            scoped = scope_prelude(node.prelude, wrapper, dark_wrapper)
            if not scoped:
                out.append(tinycss2.serialize([node]))
                continue
            body = tinycss2.serialize(node.content).strip()
            out.append(f"{scoped} {{\n  {body}\n}}" if body else f"{scoped} {{ }}")
            continue
        # 其他（declaration 等异常顶层项）：原样
        out.append(tinycss2.serialize([node]))
    return "\n".join(x for x in out if x.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("outfile")
    ap.add_argument("--wrapper", default=".lr")
    args = ap.parse_args()
    css = open(args.infile, encoding="utf-8").read()
    nodes = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=False)
    dark_wrapper = args.wrapper + ".dark"
    scoped = process(nodes, args.wrapper, dark_wrapper, [])
    header = (
        "/* lovart-replica.css — 全量序列化 CSS 作用域化到 .lr（由 scope-css.py 生成，勿手改）\n"
        "   明色变量挂 .lr；深色变量/规则挂 .lr.dark；html/body/:root 规则全部收敛。\n"
        "   页面内容须包裹 <div class=\"lr dark\">…</div>（明色页去掉 dark）。*/\n"
    )
    open(args.outfile, "w", encoding="utf-8").write(header + scoped + "\n")
    # 自检：顶层不允许出现裸 :root/html/body 选择器
    bad = []
    for line in scoped.split("\n"):
        m = re.match(r"^([^,{]+)\{", line.strip())
        if m:
            for s in m.group(1).split(","):
                s = s.strip()
                if re.match(r"^(?::root|html|body)(?![\w.-])", s):
                    bad.append(s[:60])
    n = sum(1 for line in scoped.split("\n") if re.match(r"^\S.*\{$", line))
    print(f"scoped top lines: {n}; unscoped leftovers: {len(bad)}")
    for b in bad[:5]:
        print("  LEAK:", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())