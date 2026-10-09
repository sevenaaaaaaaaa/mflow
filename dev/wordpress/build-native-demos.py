#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-native-demos.py — 生成 4 个 LR Native 能力演示页的 Elementor JSON。

产物（outdir，默认 native-demos/）：
  demo-homepage.json          复刻主页（现有混合文档直接复用）
  demo-landing-ecommerce.json LPagery 种子物化的 E-commerce 原生落地页
  demo-landing-composite.json 混合模块落地页（10 原生 + 23 HTML 回退）
  demo-blog-article.json      纯原生微件拼装的博客文章页 demo

用法：python3 build-native-demos.py [--out native-demos]
"""
import argparse
import importlib.util
import io
import json
import os
import shutil


ROOT = os.path.dirname(os.path.abspath(__file__))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


N = load_module("lr_native", os.path.join(ROOT, "build-elementor-native.py"))
S = load_module("lr_seed", os.path.join(ROOT, "build-lpagery-native-seed.py"))


def dump(doc, path):
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False)


def materialize(doc, values):
    """把种子里的 {token} 全部替换为具体值（LPagery Free 物化同款逻辑）。"""
    text = json.dumps(doc, ensure_ascii=False)
    for field, value in values.items():
        text = text.replace("{%s}" % field, str(value))
    return json.loads(text)


def build_blog_article():
    """博客文章页 demo：标题区 + 正文 + 数据 + 相关阅读 + FAQ + CTA。"""
    ids = N.IdFactory("lr-demo-blog")
    img = "https://www.lovart.ai/assets/use-cases/social-media/how-to.png"

    hero = N.native_root(ids, "article-hero", [
        N.container(ids, [
            N.text(ids, "DESIGN SCIENCE", "Article eyebrow"),
            N.heading(ids, "How to Design a Thumbnail That Gets Clicks",
                      "h1", "Article title"),
            N.text(ids, "By Lovart Team · 8 min read · Oct 9, 2026",
                   "Article meta"),
            N.text(ids,
                   "A practical breakdown of the contrast, faces, and text "
                   "rules that separate clicked thumbnails from ignored ones "
                   "— rebuilt as native Elementor modules.",
                   "Article deck"),
            N.image(ids, img, "Thumbnail design science", "Article hero image"),
        ], "lr-native-copy"),
    ], "Blog Hero")

    body = N.native_root(ids, "article-body", [
        N.container(ids, [
            N.heading(ids, "Start with contrast, not decoration", "h2",
                      "Section heading"),
            N.text(ids,
                   "Thumbnails are judged at 120 pixels wide. At that size "
                   "only two things survive: a strong value contrast between "
                   "subject and background, and at most three words of text. "
                   "Everything else is noise the feed will swallow.",
                   "Paragraph"),
            N.heading(ids, "Faces beat objects — most of the time", "h2",
                      "Section heading"),
            N.text(ids,
                   "A cropped, expressive face consistently outperforms static "
                   "product shots on CTR. But the face must earn its place: "
                   "one emotion, exaggerated, lit against a background it "
                   "contrasts with. Two competing faces halve the signal.",
                   "Paragraph"),
            N.text(ids,
                   "Test the silhouette: blur the design until only shapes "
                   "remain. If the composition still reads — one subject, one "
                   "focal accent — it will survive the feed. If it turns to "
                   "mush, no amount of detail will save it.",
                   "Paragraph"),
            N.heading(ids, "The three-word rule", "h2", "Section heading"),
            N.text(ids,
                   "On-thumbnail text is a hook, not a headline. Pick the "
                   "three words that create the open loop, set them in one "
                   "weight, and let the title in the feed do the explaining.",
                   "Paragraph"),
        ], "lr-native-article-flow"),
    ], "Blog Body")

    stats = N.native_root(ids, "stats", [
        N.container(ids, [
            N.container(ids, [
                N.heading(ids, "38%", "div", "Stat 1 value"),
                N.text(ids, "average CTR lift from a single-face crop",
                       "Stat 1 label"),
            ], "lr-native-card lr-native-stat"),
            N.container(ids, [
                N.heading(ids, "3", "div", "Stat 2 value"),
                N.text(ids, "words maximum on the thumbnail", "Stat 2 label"),
            ], "lr-native-card lr-native-stat"),
            N.container(ids, [
                N.heading(ids, "120px", "div", "Stat 3 value"),
                N.text(ids, "the only width that matters in the feed",
                       "Stat 3 label"),
            ], "lr-native-card lr-native-stat"),
        ], "lr-native-grid lr-native-grid-4", "row"),
    ], "Blog Stats")

    related_cards = []
    for i in range(1, 4):
        related_cards.append(N.container(ids, [
            N.image(ids, img, "Related article %d" % i, "Related image"),
            N.heading(ids, "Workflow %d: from brief to published set" % i,
                      "h3", "Related title"),
            N.text(ids, "Native Elementor card, fully editable.",
                   "Related body"),
        ], "lr-native-card"))
    related = N.native_root(ids, "portrait-grid-3", [
        N.heading(ids, "Keep reading", "h2", "Related heading"),
        N.container(ids, related_cards, "lr-native-grid lr-native-grid-4",
                    "row"),
    ], "Blog Related")

    tabs = []
    faqs = [
        ("Do these modules work in the free Elementor?", "Yes — every demo "
         "widget here ships with Elementor Free and the WordPress core."),
        ("Can I edit the text after generation?", "All copy lives in native "
         "heading and text-editor widgets, so it stays editable forever."),
        ("How do I reuse this layout?", "Save it as an Elementor template "
         "and combine it with LPagery CSV rows for bulk generation."),
    ]
    for i, (q, a) in enumerate(faqs, 1):
        tabs.append({"_id": ids.next(), "tab_title": q,
                     "tab_content": "<p>%s</p>" % a})
    faq = N.native_root(ids, "faq", [
        N.heading(ids, "Frequently asked questions", "h2", "FAQ title"),
        N.widget(ids, "accordion", {
            "tabs": tabs,
            "selected_icon": {"value": "fas fa-chevron-down",
                              "library": "fa-solid"},
            "title_html_tag": "h3",
        }, "FAQ accordion"),
    ], "Blog FAQ")

    cta = N.native_root(ids, "cta-default", [
        N.container(ids, [
            N.heading(ids, "Design your next thumbnail with Lovart", "h2",
                      "CTA title"),
            N.text(ids, "One brief in, a complete campaign out.",
                   "CTA body"),
            N.button(ids, "Try Lovart free", "https://www.lovart.ai/",
                     "CTA button", "primary"),
        ], "lr-native-cta-card"),
    ], "Blog CTA")

    return {"version": "3.35.7",
            "data": [hero, body, stats, related, faq, cta]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="native-demos")
    args = ap.parse_args()
    out = os.path.join(ROOT, args.out)
    if not os.path.isdir(out):
        os.makedirs(out)

    # 1) 主页 demo：现有复刻主页混合文档直接复用
    shutil.copyfile(os.path.join(ROOT, "elem-native", "replica-homepage.json"),
                    os.path.join(out, "demo-homepage.json"))

    # 2) E-commerce 原生落地页：LPagery 种子按行物化
    row = S.row("E-commerce", "online store owners", "lr-demo-ecommerce")
    dump(materialize(S.build_seed(), row),
         os.path.join(out, "demo-landing-ecommerce.json"))

    # 3) 混合模块落地页：composite 文档（10 原生 + 23 HTML 回退）
    shutil.copyfile(
        os.path.join(ROOT, "elem-native", "composite-replica-all.json"),
        os.path.join(out, "demo-landing-composite.json"))

    # 4) 博客文章页 demo：纯原生微件拼装
    dump(build_blog_article(), os.path.join(out, "demo-blog-article.json"))

    for name in sorted(os.listdir(out)):
        print(name, os.path.getsize(os.path.join(out, name)))


if __name__ == "__main__":
    main()
