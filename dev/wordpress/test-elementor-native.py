#!/usr/bin/env python3
"""Structural tests for generated native Elementor documents/templates."""
import glob
import json
import os
import re


ROOT = os.path.dirname(os.path.abspath(__file__))


def walk(elements):
    for element in elements or []:
        yield element
        for child in walk(element.get("elements", [])):
            yield child


def main():
    source = sorted(glob.glob(os.path.join(ROOT, "elem-src", "*.json")))
    native = sorted(glob.glob(os.path.join(ROOT, "elem-native", "*.json")))
    native = [x for x in native if not x.endswith("conversion-report.json")]
    assert len(source) == 18, len(source)
    assert len(native) == 18, len(native)

    total_native = 0
    for src_path, native_path in zip(source, native):
        assert os.path.basename(src_path) == os.path.basename(native_path)
        src = json.load(open(src_path))
        doc = json.load(open(native_path))
        assert len(src["data"]) == len(doc["data"])
        assert doc["version"] == src["version"]
        for root in doc["data"]:
            settings = root.get("settings") or {}
            classes = settings.get("css_classes", "") or settings.get("_css_classes", "")
            if "lr-native" not in classes.split():
                continue
            total_native += 1
            widgets = [x for x in walk([root]) if x.get("elType") == "widget"]
            assert widgets
            assert not any(x.get("widgetType") == "html" for x in widgets)
            assert any(x.get("widgetType") in {
                "heading", "text-editor", "image", "video", "button", "accordion"
            } for x in widgets)
    assert total_native == 68, total_native

    manifest = json.load(open(os.path.join(
        ROOT, "elem-native-templates", "manifest.json")))
    assert len(manifest) == 86
    assert len({x["slug"] for x in manifest}) == len(manifest)
    assert sum(x["type"] == "page" for x in manifest) == 18
    assert sum(x.get("mode") == "native" for x in manifest) == 68
    for item in manifest:
        assert re.match(r"^lr-native-[a-z0-9-]+$", item["slug"])
        assert os.path.exists(os.path.join(
            ROOT, "elem-native-templates", item["file"]))
    print("OK: 18 documents, 68 native sections, 86 templates")


if __name__ == "__main__":
    main()
