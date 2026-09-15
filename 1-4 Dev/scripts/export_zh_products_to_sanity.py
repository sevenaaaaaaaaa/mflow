#!/usr/bin/env python3
"""
Lovart 中文 Product Page → Sanity NDJSON 导出脚本
===========================================
读取 Pages/Products/zh/*.json → 添加 Sanity import 字段 → 输出 NDJSON

用法:
  python3 export_zh_products_to_sanity.py --input-dir .../Pages/Products/zh --output zh-products.ndjson
  python3 export_zh_products_to_sanity.py --input-dir .../Pages/Products/zh --output zh-products.ndjson --dry-run
"""

import argparse
import glob
import hashlib
import json
import os
import sys

DEFAULT_OG_URL = "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d3e44c9edfb1a44f386973e9b3c23fcffddc8008.png"


def _extract_first_image(body_sections):
    for s in body_sections if isinstance(body_sections, list) else []:
        media = s.get("media", {})
        if isinstance(media, dict):
            src = media.get("src", "")
            if src:
                return src
        for key in ("cards", "items", "tabs", "logos", "testimonials"):
            for item in s.get(key, []) if isinstance(s.get(key), list) else []:
                img = item.get("media", item.get("image", {}))
                if isinstance(img, dict):
                    src = img.get("src", img.get("url", ""))
                    if src:
                        return src
                avatar = item.get("avatar", {})
                if isinstance(avatar, dict):
                    src = avatar.get("src", avatar.get("url", ""))
                    if src:
                        return src
    return DEFAULT_OG_URL


def _make_structured_data(title, description, slug):
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": title,
        "description": description or title,
        "url": f"https://www.lovart.ai/zh/{slug}",
        "publisher": {
            "@type": "Organization",
            "name": "Lovart",
            "url": "https://www.lovart.ai"
        }
    }
    return data


def export_product(input_path, output_path, dry_run=False):
    with open(input_path, "r", encoding="utf-8") as f:
        prod = json.load(f)

    slug = prod["slug"]
    title = prod.get("title", slug)
    description = prod.get("description", "")
    lang = prod.get("language", "zh")

    body = json.loads(prod["bodyJson"]) if isinstance(prod["bodyJson"], str) else prod["bodyJson"]

    og_url = _extract_first_image(body)

    # Extract base slug for urlPath (strip "zh-" prefix for clean URL)
    base_slug = slug
    if base_slug.startswith("zh-"):
        base_slug = base_slug[3:]

    record = {
        "_id": slug,
        "_type": "compositePage",
        "slug": {
            "_type": "slug",
            "current": slug
        },
        "category": "product",
        "language": lang,
        "schemaVersion": prod.get("schemaVersion", "composite-v2"),
        "storyline": prod.get("storyline", "product-标准"),
        "title": title,
        "description": description,
        "bodyJson": json.dumps(body, ensure_ascii=False),
        "seo": {
            "title": prod.get("seo", {}).get("title", title),
            "description": prod.get("seo", {}).get("description", description),
            "keywords": prod.get("seo", {}).get("keywords", []),
            "noIndex": prod.get("seo", {}).get("noIndex", False),
            "ogImage": {
                "_type": "imageSource",
                "alt": f"{title} — Lovart AI Design",
                "sourceType": "external",
                "url": og_url
            },
            "structuredData": {
                "_type": "structuredData",
                "enabled": True,
                "json": json.dumps(
                    _make_structured_data(title, description, slug),
                    ensure_ascii=False
                )
            }
        },
        "urlPath": f"https://www.lovart.ai/zh/{base_slug}"
    }

    line = json.dumps(record, ensure_ascii=False)
    if dry_run:
        print(f"  [DRY-RUN] {slug:40s} → /zh/{base_slug}")
        return True
    else:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"  {slug:40s} → /zh/{base_slug}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Export zh product page JSONs to Sanity NDJSON")
    parser.add_argument("--input-dir", required=True, help="Directory containing product JSON files")
    parser.add_argument("--output", required=True, help="Output NDJSON file path")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no write")
    args = parser.parse_args()

    files = sorted(glob.glob(os.path.join(args.input_dir, "*.json")))
    print(f"待导出: {len(files)} 篇 Product Page")

    if not args.dry_run:
        open(args.output, "w").close()

    ok = 0
    for fp in files:
        if export_product(fp, args.output, args.dry_run):
            ok += 1

    if not args.dry_run:
        size = os.path.getsize(args.output)
        print(f"\nNDJSON: {args.output}")
        print(f"   记录: {ok} 行 | 大小: {size/1024:.0f} KB")
    else:
        print(f"\nDRY-RUN: {ok}/{len(files)} 篇可导出")


if __name__ == "__main__":
    main()
