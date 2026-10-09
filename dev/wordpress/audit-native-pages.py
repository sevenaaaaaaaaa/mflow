#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit LR Native Elementor artifacts before deployment."""
from __future__ import print_function

import glob
import io
import json
import os
import re
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
NATIVE_DIR = os.path.join(ROOT, "elem-native")
TEMPLATE_DIR = os.path.join(ROOT, "elem-native-templates")
MODULE_DIR = os.path.join(ROOT, "native-modules")
ALLOWED_WIDGETS = {"heading", "text-editor", "button", "image", "video", "accordion"}


def load(path):
    return json.load(io.open(path, encoding="utf-8"))


def walk(nodes):
    for node in nodes:
        yield node
        for child in walk(node.get("elements", []) or []):
            yield child


def classes(node):
    settings = node.get("settings", {}) or {}
    return settings.get("css_classes", "") or settings.get("_css_classes", "")


def audit():
    errors = []
    documents = native_sections = fallback_sections = 0
    widget_types = set()

    for path in sorted(glob.glob(os.path.join(NATIVE_DIR, "*.json"))):
        if path.endswith("conversion-report.json"):
            continue
        documents += 1
        doc = load(path)
        if not isinstance(doc.get("data"), list) or not doc["data"]:
            errors.append("%s: empty Elementor data" % os.path.basename(path))
            continue
        for root in doc["data"]:
            root_classes = classes(root).split()
            nodes = list(walk([root]))
            html_count = sum(
                1 for node in nodes if node.get("widgetType") == "html")
            if "lr-native" in root_classes:
                native_sections += 1
                if "lr" not in root_classes or "dark" not in root_classes:
                    errors.append("%s/%s: missing scope classes" % (
                        os.path.basename(path), root.get("id")))
                if html_count:
                    errors.append("%s/%s: native section contains HTML widget" % (
                        os.path.basename(path), root.get("id")))
                for node in nodes:
                    kind = node.get("widgetType")
                    if kind:
                        widget_types.add(kind)
                        if kind not in ALLOWED_WIDGETS:
                            errors.append("%s/%s: unsupported widget %s" % (
                                os.path.basename(path), node.get("id"), kind))
            else:
                fallback_sections += 1
                if html_count != 1:
                    errors.append("%s/%s: fallback HTML count=%d" % (
                        os.path.basename(path), root.get("id"), html_count))

    manifest = load(os.path.join(TEMPLATE_DIR, "manifest.json"))
    if len(manifest) != 86:
        errors.append("template manifest: expected 86, got %d" % len(manifest))
    for item in manifest:
        target = os.path.join(TEMPLATE_DIR, item["file"])
        if not os.path.isfile(target):
            errors.append("missing template: %s" % item["file"])

    for name in ("lp-lr-native-v1-free.json", "lp-lr-native-v1-pro.json"):
        seed = load(os.path.join(MODULE_DIR, name))
        roots = seed.get("data", [])
        if len(roots) != 7:
            errors.append("%s: expected 7 roots, got %d" % (name, len(roots)))
        for root in roots:
            if "lr-native" not in classes(root).split():
                errors.append("%s/%s: missing lr-native class" % (
                    name, root.get("id")))
            if any(node.get("widgetType") == "html" for node in walk([root])):
                errors.append("%s/%s: HTML widget found" % (
                    name, root.get("id")))

    fixtures = glob.glob(os.path.join(
        MODULE_DIR, "lp-lr-native-v1-free-samples", "*.json"))
    if len(fixtures) != 3:
        errors.append("LPagery fixtures: expected 3, got %d" % len(fixtures))
    for path in fixtures:
        raw = io.open(path, encoding="utf-8").read()
        if re.search(r"\{[a-z_]+\}", raw):
            errors.append("%s: unresolved placeholder" % os.path.basename(path))

    summary = {
        "documents": documents,
        "native_sections": native_sections,
        "fallback_sections": fallback_sections,
        "templates": len(manifest),
        "lpagery_fixtures": len(fixtures),
        "widget_types": sorted(widget_types),
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(audit())
