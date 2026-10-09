#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert LR HTML-widget Elementor documents to editable native widgets.

Input is the existing elem-src JSON, so the converter is independent of the
remote HTML source and can be rerun deterministically. Supported section kinds
become native Elementor containers/widgets; unsupported sections are retained
unchanged as a lossless legacy fallback.
"""
from __future__ import print_function

import argparse
import copy
import glob
import hashlib
import io
import json
import os
import re

from bs4 import BeautifulSoup


PILOT_KINDS = {
    "hero-split", "stats", "proof-block", "review-grid-3col",
    "review-grid-4col", "testimonial", "cta-default", "portrait-grid-3",
    "portrait-grid-4", "faq",
}

ZERO_BOX = {
    "unit": "px", "top": "0", "right": "0", "bottom": "0",
    "left": "0", "isLinked": True,
}


class IdFactory(object):
    def __init__(self, seed):
        self.seed = seed
        self.n = 0

    def next(self):
        self.n += 1
        raw = ("%s:%d" % (self.seed, self.n)).encode("utf-8")
        return hashlib.sha1(raw).hexdigest()[:7]


def widget(ids, kind, settings, title):
    out = {
        "id": ids.next(), "elType": "widget", "widgetType": kind,
        "settings": settings, "elements": [],
    }
    out["settings"].setdefault("_title", title)
    return out


def container(ids, elements=None, classes="", direction="column", settings=None):
    base = {
        "content_width": "full",
        "flex_direction": direction,
        "gap": {"unit": "px", "size": 20, "sizes": []},
        "padding": copy.deepcopy(ZERO_BOX),
        "margin": copy.deepcopy(ZERO_BOX),
    }
    if classes:
        base["css_classes"] = classes
    if settings:
        base.update(settings)
    return {
        "id": ids.next(), "elType": "container", "settings": base,
        "elements": elements or [], "isInner": True,
    }


def heading(ids, text, level="h2", title="Heading"):
    return widget(ids, "heading", {
        "title": text, "header_size": level,
        "title_color": "#f7f6f2",
        "typography_typography": "custom",
        "typography_font_family": "Inter",
    }, title)


def text(ids, value, title="Text"):
    return widget(ids, "text-editor", {
        "editor": "<p>%s</p>" % value,
        "text_color": "#a6a49d",
        "typography_typography": "custom",
        "typography_font_family": "Inter",
    }, title)


def button(ids, label, url, title="Button", variant="primary"):
    settings = {
        "text": label, "link": {"url": url or "#", "is_external": False,
                                "nofollow": False},
        "size": "md", "align": "left",
        "button_text_color": "#100f09" if variant == "primary" else "#f7f6f2",
        "background_color": "#f7f6f2" if variant == "primary" else "#26251f",
        "border_radius": {"unit": "px", "top": "999", "right": "999",
                          "bottom": "999", "left": "999", "isLinked": True},
    }
    return widget(ids, "button", settings, title)


def image(ids, url, alt="", title="Image"):
    return widget(ids, "image", {
        "image": {"url": url, "id": "", "alt": alt},
        "image_size": "full", "caption_source": "none",
    }, title)


def video(ids, url, poster="", title="Video"):
    return widget(ids, "video", {
        "video_type": "hosted", "hosted_url": {"url": url},
        "autoplay": "yes", "loop": "yes", "mute": "yes",
        "play_on_mobile": "yes", "controls": "",
        "image_overlay": {"url": poster, "id": ""},
        "show_image_overlay": "yes" if poster else "",
    }, title)


def clean_text(node):
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()


def unique_texts(nodes):
    out = []
    seen = set()
    for node in nodes:
        value = clean_text(node)
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def section_kind(soup):
    marker = soup.select_one("[data-lp-section]")
    return marker.get("data-lp-section", "") if marker else ""


def links(soup):
    out = []
    seen = set()
    for a in soup.find_all("a"):
        label = clean_text(a)
        if not label:
            continue
        key = (label, a.get("href") or "#")
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def native_root(ids, kind, children, source_title):
    settings = {
        "content_width": "full",
        "flex_direction": "column",
        "gap": {"unit": "px", "size": 28, "sizes": []},
        "padding": {"unit": "px", "top": "80", "right": "40",
                    "bottom": "80", "left": "40", "isLinked": False},
        "margin": copy.deepcopy(ZERO_BOX),
        "background_background": "classic",
        "background_color": "#100f09",
        "css_classes": "lr dark lr-native lr-native-%s" % kind,
        "_title": "LR Native — %s" % source_title,
    }
    return {
        "id": ids.next(), "elType": "container", "settings": settings,
        "elements": children, "isInner": False,
    }


def build_hero(ids, soup):
    headings = unique_texts(soup.find_all(["h1", "h2"]))
    paragraphs = unique_texts(soup.find_all("p"))
    media = soup.find(["video", "img"])
    copy_children = []
    if paragraphs:
        copy_children.append(text(ids, paragraphs[0], "Eyebrow"))
    if headings:
        copy_children.append(heading(ids, headings[0], "h1", "Hero title"))
    for value in paragraphs[1:3]:
        copy_children.append(text(ids, value, "Hero copy"))
    btns = [button(ids, label, url, "Hero CTA %d" % (i + 1),
                   "primary" if i == 0 else "secondary")
            for i, (label, url) in enumerate(links(soup)[:2])]
    if btns:
        copy_children.append(container(ids, btns, "lr-native-buttons", "row"))
    columns = [container(ids, copy_children, "lr-native-copy")]
    if media:
        if media.name == "video":
            columns.append(container(ids, [video(
                ids, media.get("src", ""), media.get("poster", ""), "Hero media")],
                "lr-native-media"))
        else:
            columns.append(container(ids, [image(
                ids, media.get("src", ""), media.get("alt", ""), "Hero media")],
                "lr-native-media"))
    return native_root(ids, "hero-split", [
        container(ids, columns, "lr-native-columns", "row")
    ], "Hero Split")


def build_stats(ids, soup):
    texts = unique_texts(soup.find_all(["div", "span", "p"]))
    # Pick compact leaf text values and pair value/label in document order.
    leaves = []
    for node in soup.find_all(["div", "span", "p"]):
        if node.find(["div", "span", "p"]):
            continue
        value = clean_text(node)
        if value and len(value) < 80:
            leaves.append(value)
    pairs = []
    for i in range(0, min(len(leaves), 8), 2):
        if i + 1 < len(leaves):
            pairs.append((leaves[i], leaves[i + 1]))
    cards = []
    for i, (value, label) in enumerate(pairs[:4]):
        cards.append(container(ids, [
            heading(ids, value, "div", "Stat %d value" % (i + 1)),
            text(ids, label, "Stat %d label" % (i + 1)),
        ], "lr-native-card lr-native-stat"))
    return native_root(ids, "stats", [
        container(ids, cards, "lr-native-grid lr-native-grid-4", "row")
    ], "Stats")


def build_cta(ids, soup):
    headings = unique_texts(soup.find_all(["h1", "h2", "h3"]))
    paragraphs = unique_texts(soup.find_all("p"))
    children = []
    if headings:
        children.append(heading(ids, headings[0], "h2", "CTA title"))
    if paragraphs:
        children.append(text(ids, paragraphs[0], "CTA body"))
    btns = [button(ids, label, url, "CTA %d" % (i + 1),
                   "primary" if i == 0 else "secondary")
            for i, (label, url) in enumerate(links(soup)[:2])]
    if btns:
        children.append(container(ids, btns, "lr-native-buttons", "row"))
    return native_root(ids, "cta-default", [
        container(ids, children, "lr-native-cta-card")
    ], "CTA")


def build_faq(ids, soup):
    headings = unique_texts(soup.find_all(["h1", "h2"]))
    questions = unique_texts(soup.find_all(["h3", "h4"]))
    # The captured SSR source often omits collapsed answers. Ship a neutral
    # editable prompt instead of raw tokens — tokens are reserved for the
    # LPagery seed builder, which assembles its own tabs.
    tabs = []
    for i, question in enumerate(questions[:8]):
        tabs.append({
            "_id": ids.next(),
            "tab_title": question,
            "tab_content": "<p>Answer this question here — every word stays "
                           "editable in Elementor.</p>",
        })
    children = []
    if headings:
        children.append(heading(ids, headings[0], "h2", "FAQ title"))
    children.append(widget(ids, "accordion", {
        "tabs": tabs, "selected_icon": {"value": "fas fa-chevron-down",
                                         "library": "fa-solid"},
        "title_html_tag": "h3",
    }, "FAQ accordion"))
    return native_root(ids, "faq", children, "FAQ")


def build_cards(ids, soup, kind):
    headings = unique_texts(soup.find_all(["h1", "h2"]))
    card_heads = unique_texts(soup.find_all(["h3", "h4"]))
    paragraphs = unique_texts(soup.find_all(["p", "blockquote"]))
    media = soup.find_all(["img", "video"])
    children = []
    if headings:
        children.append(heading(ids, headings[0], "h2", "Section title"))
    cards = []
    count = min(max(len(card_heads), len(media), 3), 4)
    for i in range(count):
        parts = []
        if i < len(media):
            m = media[i]
            parts.append(video(ids, m.get("src", ""), m.get("poster", ""),
                               "Card %d video" % (i + 1)) if m.name == "video"
                         else image(ids, m.get("src", ""), m.get("alt", ""),
                                    "Card %d image" % (i + 1)))
        if i < len(card_heads):
            parts.append(heading(ids, card_heads[i], "h3",
                                 "Card %d title" % (i + 1)))
        if i < len(paragraphs):
            parts.append(text(ids, paragraphs[i], "Card %d body" % (i + 1)))
        if parts:
            cards.append(container(ids, parts, "lr-native-card"))
    children.append(container(ids, cards,
                              "lr-native-grid lr-native-grid-%d" % max(1, count),
                              "row"))
    return native_root(ids, kind, children, kind.replace("-", " ").title())


def convert_container(source, seed):
    current = source
    html_widget = None
    for child in current.get("elements", []):
        if child.get("widgetType") == "html":
            html_widget = child
            break
    if not html_widget:
        return copy.deepcopy(source), "unchanged", ""
    html = (html_widget.get("settings") or {}).get("html", "")
    soup = BeautifulSoup(html, "lxml")
    kind = section_kind(soup)
    if kind not in PILOT_KINDS:
        return copy.deepcopy(source), "fallback", kind
    ids = IdFactory(seed)
    if kind == "hero-split":
        root = build_hero(ids, soup)
    elif kind == "stats":
        root = build_stats(ids, soup)
    elif kind == "cta-default":
        root = build_cta(ids, soup)
    elif kind == "faq":
        root = build_faq(ids, soup)
    else:
        root = build_cards(ids, soup, kind)
    # Preserve sticky and z-index behavior from the source top-level container.
    for key in ("sticky", "sticky_on", "sticky_offset",
                "sticky_effects_offset", "sticky_parent", "z_index"):
        if key in source.get("settings", {}):
            root["settings"][key] = copy.deepcopy(source["settings"][key])
    return root, "native", kind


def convert_document(doc, slug):
    out = copy.deepcopy(doc)
    stats = {"native": 0, "fallback": 0, "unchanged": 0, "kinds": {}}
    converted = []
    for i, source in enumerate(doc.get("data", [])):
        result, status, kind = convert_container(source, "%s:%d" % (slug, i))
        converted.append(result)
        stats[status] += 1
        if kind:
            stats["kinds"][kind] = stats["kinds"].get(kind, 0) + 1
    out["data"] = converted
    return out, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="elem-src")
    ap.add_argument("--out", default="elem-native")
    args = ap.parse_args()
    if not os.path.isdir(args.out):
        os.makedirs(args.out)
    summary = {}
    for path in sorted(glob.glob(os.path.join(args.src, "*.json"))):
        slug = os.path.basename(path)[:-5]
        doc = json.load(io.open(path, encoding="utf-8"))
        native, stats = convert_document(doc, slug)
        target = os.path.join(args.out, slug + ".json")
        with io.open(target, "w", encoding="utf-8") as f:
            json.dump(native, f, ensure_ascii=False)
        summary[slug] = stats
        print("%s native=%d fallback=%d unchanged=%d" % (
            slug, stats["native"], stats["fallback"], stats["unchanged"]))
    with io.open(os.path.join(args.out, "conversion-report.json"),
                 "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)
    print("documents:", len(summary),
          "native sections:", sum(x["native"] for x in summary.values()),
          "fallback sections:", sum(x["fallback"] for x in summary.values()))


if __name__ == "__main__":
    main()
