#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-elementor-faithful.py — 忠实转换 POC：原始 HTML → Elementor 结构树。

原则（区别于 build-elementor-native.py 的自造样式）：
  - 原始 DOM 的每个块级节点 → Elementor container，保留原始 class
  - 标题/段落/图片 → 原生微件（heading/text-editor/image），保留原始 class
  - 其余（svg/button/a/canvas 等）→ HTML 微件原样保留
  - 不写任何自造样式：排版/间距/字号/行距全部由 lovart-replica.css 的原始规则渲染

用法：python3 build-elementor-faithful.py --src elem-src/xxx.json --sections 1,4 --out native-faithful/poc.json
"""
import argparse
import importlib.util
import io
import json
import os
import re

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "lr_native", os.path.join(ROOT, "build-elementor-native.py"))
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)

CONTAINER_TAGS = {"div", "section", "header", "footer", "nav", "ul", "ol",
                  "li", "form", "figure", "article", "aside", "main",
                  "fieldset", "table", "thead", "tbody", "dl", "dt", "dd",
                  "picture"}
MEDIA_TAGS = {"svg", "canvas", "iframe", "video", "button", "input",
              "select", "textarea", "marquee", "blockquote", "a", "span"}

# 交互区块：内部靠 lovart-replica.js 以 data-lp-section / aria-* / data-state /
# role 等语义属性驱动（对比滑块、FAQ 手风琴、tabs/轮播、对话、锚点）。
# 拆成容器树会丢这些属性、JS 找不到目标 → 全部失效。故此类区块在忠实模式下
# 保持整区块单个 HTML 微件（原样 DOM + 全属性），不做容器化。
INTERACTIVE_SECTIONS = {
    "comparison-before-after",   # 对比滑块（拖动）
    "faq",                       # FAQ 手风琴
    "capability-tabs",           # 多 tab 切换/轮播
    "workflow-vertical",         # howto/workflow 折叠展开
    "workflow-horizontal",
    "comparison-table",          # 对比表（含折叠/高亮）
    "prompt-launcher",           # 对话式启动器（可互动输入）
    "hero-cinematic",            # 含对话面板/轮播
    "hero-journey",              # 含步骤轮播
    "media-marquee",             # 跑马灯（拖动/自动）
    "showcase-stacked",          # 层叠轮播
    "showcase-horizontal",       # 横向轮播（拖拽）
    "canvas-wall",               # 画布墙（拖拽）
    "logo-loop",                 # logo 循环（自动轮播）
    "testimonial",               # 评价轮播
    "pricing-block",             # 价格区（月/年切换）
}


def is_interactive_section(html):
    m = re.search(r'data-lp-section="([^"]+)"', html or "")
    return (m.group(1) in INTERACTIVE_SECTIONS) if m else False


def classes_of(node):
    return " ".join(node.get("class", []))


def inner_html(node):
    return node.decode_contents().strip()


def convert_tag(node, ids, depth=0):
    """单个标签 → 0/1/n 个 Elementor 元素。"""
    if not isinstance(node, Tag):
        return []
    name = node.name.lower()
    classes = classes_of(node)

    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        # 忠实模式：heading 微件把 css_classes 放到包装层而非标题元素上，
        # 工具类字号/字距会失效。标题一律 HTML 回退，保持原始 DOM 与类名。
        return [N.widget(ids, "html", {"html": str(node)},
                         "Heading (html)")]
    if name == "img":
        img_classes = classes
        # 带定位/尺寸工具类的 img（absolute/inset-/h-full 等）必须保持原始 <img>，
        # image 微件不把这些类写到 img 上，会导致 absolute 填充失效。
        if re.search(r"\b(absolute|fixed|inset-|h-full|w-full|self-|object-)", img_classes):
            return [N.widget(ids, "html", {"html": str(node)}, "Image (html)")]
        settings = {
            "image": {"url": node.get("src", ""), "id": "",
                      "alt": node.get("alt", "")},
            "image_size": "full", "caption_source": "none",
        }
        if img_classes:
            settings["css_classes"] = img_classes
        return [N.widget(ids, "image", settings, "Image")]
    if name == "p":
        settings = {"editor": str(node)}
        if classes:
            settings["css_classes"] = classes
        return [N.widget(ids, "text-editor", settings, "Text")]
    if name in CONTAINER_TAGS:
        children = []
        for child in node.children:
            if isinstance(child, NavigableString):
                text = child.strip()
                if text:
                    settings = {"editor": "<p>%s</p>" % text}
                    if classes:
                        settings["css_classes"] = classes
                    children.append(N.widget(ids, "text-editor", settings,
                                             "Text"))
            else:
                children.extend(convert_tag(child, ids, depth + 1))
        # 忠实模式：不写 content_width/flex_direction/gap 等任何布局设置，
        # 只保留原始 class + lr-faithful 标记，让 lovart-replica.css 的原始规则
        # 和 lovart-faithful-mirror.css 的未分层镜像完全接管。
        marker = "lr-faithful"
        settings = {"content_width": "full", "css_classes": marker}
        if classes:
            settings["css_classes"] = marker + " " + classes
        container = {
            "id": ids.next(), "elType": "container", "settings": settings,
            "elements": children, "isInner": depth > 0,
        }
        return [container]
    # 其余标签（span/a/button/svg/canvas/marquee...）→ HTML 原样回退
    return [N.widget(ids, "html", {"html": str(node)}, "HTML fallback")]


def convert_section(html, ids):
    """区块 HTML → 根容器（携带 .lr.dark 环境层类）。

    交互区块（data-lp-section ∈ INTERACTIVE_SECTIONS）整区块保留为 HTML 微件，
    完整保留 data-lp-section/aria-*/data-state/role 等语义属性，让
    lovart-replica.js 能正常初始化；外层仅套一个 .lr-faithful 根容器承接镜像 CSS。
    结构区块照常容器化（像素级排版），因其不依赖 JS 属性。
    """
    if is_interactive_section(html):
        root_settings = {"content_width": "full", "css_classes": "lr-faithful"}
        widget = N.widget(ids, "html", {"html": html}, "Interactive section")
        return {
            "id": ids.next(), "elType": "container", "settings": root_settings,
            "elements": [widget], "isInner": False,
        }
    soup = BeautifulSoup(html, "html.parser")
    wrapper = soup.find(True)
    root_classes = classes_of(wrapper)
    children = []
    for child in wrapper.children:
        if isinstance(child, NavigableString):
            if child.strip():
                children.append(N.widget(ids, "text-editor", {
                    "editor": "<p>%s</p>" % child.strip()}, "Text"))
        else:
            children.extend(convert_tag(child, ids, 1))
    settings = {"content_width": "full"}
    if root_classes:
        settings["css_classes"] = "lr-faithful " + root_classes
    return {
        "id": ids.next(), "elType": "container", "settings": settings,
        "elements": children, "isInner": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--sections", required=True, help="如 1,4,11")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    doc = json.load(io.open(args.src, encoding="utf-8"))
    sections_html = []
    for c in doc["data"]:
        for w in c.get("elements", []):
            if w.get("widgetType") == "html":
                sections_html.append(w["settings"]["html"])
    want = list(range(len(sections_html))) if args.sections.strip().lower() == "all" \
        else [int(x) for x in args.sections.split(",")]
    ids = N.IdFactory("lr-faithful")
    data = [convert_section(sections_html[i], ids) for i in want]
    out = {"version": "3.35.7", "data": data}
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with io.open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)

    def stats(nodes):
        n_cont = n_widget = 0
        kinds = {}
        for x in nodes:
            if x.get("elType") == "container":
                n_cont += 1
                a, b, kinds2 = stats(x.get("elements", []))
                n_cont += a
                n_widget += b
                for k, v in kinds2.items():
                    kinds[k] = kinds.get(k, 0) + v
            else:
                n_widget += 1
                kinds[x.get("widgetType")] = kinds.get(x.get("widgetType"), 0) + 1
        return n_cont, n_widget, kinds

    for i, root in zip(want, data):
        nc, nw, kinds = stats([root])
        print("section %d: containers=%d widgets=%d %s" % (i, nc, nw, kinds))


if __name__ == "__main__":
    main()
