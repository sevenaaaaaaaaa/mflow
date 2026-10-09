#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-faithful-mirror.py — 忠实模式工具类镜像生成器。

背景：lovart-replica.css 的 Tailwind 工具类都在 `@layer utilities/components` 内，
而 Elementor e-con 的 chrome 规则（width: var(--width)=100%,
border-radius: var(--border-radius)=0, gap: var(--row-gap) var(--column-gap)=20px,
flex-wrap: var(--flex-wrap-mobile)=wrap 等）是未分层规则。
CSS 级联规定：未分层声明恒压过分层声明（与特异性和顺序无关）。
因此凡转成 e-con 的忠实容器，身上的 display/gap/width/rounded/padding 等
工具类全部失效——这是排版全乱的根因。

修法：把 @layer utilities/components 里的规则机械镜像一份**未分层**副本，
选择器由 `.lr .X` 变为 `.lr .e-con.lr-faithful.X`（只作用于忠实容器，
不影响原版复刻页与 LR Native 页）。加载顺序在 replica.css 之后，
未分层 + 更高特异性 → 稳定覆盖 e-con chrome。

用法：python3 build-faithful-mirror.py --src assets-src/lovart-replica.css \
  --out assets-src/lovart-faithful-mirror.css
"""
import argparse
import io
import os
import re

PREFIX = ".lr .e-con.lr-faithful"


def transform_selector(sel):
    """`.lr .X` → `.lr .e-con.lr-faithful.X`（保留伪类/后代/媒体变体结构）。"""
    sel = sel.strip()
    if sel.startswith(".lr "):
        # .lr 后紧跟的第一个复合选择器挂上 e-con.lr-faithful
        rest = sel[4:]
        return ".lr .e-con.lr-faithful" + rest
    # 非 .lr 开头（理论上 layer 内都是作用域化的），原样返回不镜像
    return None


def transform_rule_block(css_text, out):
    """解析一层内的规则（含嵌套 @media），变换后写入 out。"""
    i, n = 0, len(css_text)
    buf = ""

    def flush_selector_chunk(chunk):
        chunk = chunk.strip()
        if not chunk:
            return
        parts = [p for p in chunk.split(",")]
        mirrored = []
        for p in parts:
            t = transform_selector(p)
            if t is not None:
                mirrored.append(t)
        if mirrored:
            out.append(",".join(mirrored) + "{")

    # 简单状态机：selector { body } / @media { ... } / 注释跳过
    while i < n:
        ch = css_text[i]
        if ch == "/":
            j = css_text.find("*/", i + 2)
            i = (j + 2) if j != -1 else n
            continue
        if ch == "}":
            out.append("}")
            i += 1
            continue
        # 收集 selector 直到 {
        j = css_text.find("{", i)
        if j == -1:
            buf += css_text[i:].strip()
            i = n
            if buf:
                out.append("/* 尾部残片: %s */" % buf[:80])
            break
        selector = css_text[i:j].strip()
        if selector.startswith("@"):
            # at-rule（如 @media / @supports）：保留条件，递归处理内部
            depth = 1
            k = j + 1
            while k < n and depth:
                if css_text[k] == "{":
                    depth += 1
                elif css_text[k] == "}":
                    depth -= 1
                k += 1
            out.append(selector + "{")
            transform_rule_block(css_text[j + 1:k - 1], out)
            out.append("}")
            i = k
            continue
        # 找匹配的 }
        depth = 1
        k = j + 1
        while k < n and depth:
            if css_text[k] == "{":
                depth += 1
            elif css_text[k] == "}":
                depth -= 1
            k += 1
        body = css_text[j + 1:k - 1]
        # 普通声明（不含嵌套 {）
        if "{" not in body:
            mirrored = transform_selector(selector)
            if mirrored:
                out.append(mirrored + "{" + body.rstrip().rstrip(";") + "}")
        else:
            # 嵌套体（Tailwind v4 把 @media/:hover 写在规则体内）：保留结构原样，
            # 只镜像外层选择器，内层条件不变
            mirrored = transform_selector(selector)
            if mirrored:
                out.append(mirrored + "{" + body + "}")
        i = k


def extract_layers(src):
    """抽取 @layer components/utilities 的内容（去重后合并）。"""
    text = io.open(src, encoding="utf-8").read()
    lines = text.split("\n")
    chunks = []
    i = 0
    while i < len(lines):
        m = re.match(r"\s*@layer (components|utilities) \{", lines[i])
        if m:
            depth = 0
            j = i
            while j < len(lines):
                depth += lines[j].count("{") - lines[j].count("}")
                if depth == 0:
                    break
                j += 1
            chunks.append("\n".join(lines[i + 1:j]))  # 去掉 @layer 行与收尾 }
            i = j + 1
            continue
        i += 1
    # 去重：两组 layer 内容相同，按块级文本去重后直接拼接
    # （块内规则保持完整含收尾大括号，交给 transform_rule_block 解析）
    seen = set()
    merged = []
    for chunk in chunks:
        key = chunk.strip()
        if key and key not in seen:
            seen.add(key)
            merged.append(chunk)
    return "\n".join(merged) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    css = extract_layers(args.src)
    header = (
        "/* lovart-faithful-mirror.css — 由 build-faithful-mirror.py 生成，勿手改。\n"
        "   未分层镜像 @layer utilities/components 的工具类，仅作用于忠实容器\n"
        "   (.lr .e-con.lr-faithful)，用于压过 Elementor e-con chrome 的未分层规则。 */\n"
    )
    out_lines = []
    transform_rule_block(css, out_lines)
    body = "\n".join(out_lines)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with io.open(args.out, "w", encoding="utf-8") as f:
        f.write(header + body + "\n")
    print("生成 %s: %d 字节, %d 行" % (args.out, len(header + body), body.count("\n") + 1))


if __name__ == "__main__":
    main()
