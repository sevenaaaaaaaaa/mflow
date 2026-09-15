#!/usr/bin/env python3
"""Import zh product blogs (Batch 2) to Sanity production."""

import glob
import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
import sys

_SSOT_DIR = str(Path.home() / "Documents/Lovart Local Dev/scripts")
if _SSOT_DIR not in sys.path:
    sys.path.insert(0, _SSOT_DIR)
from md_to_portable_text import md_to_portable_text as md_to_pt


SANITY_PROJECT = "o11tm2qe"
SANITY_DATASET = "production"
API_VERSION = "2024-01-01"
API_BASE = f"https://{SANITY_PROJECT}.api.sanity.io/v{API_VERSION}/data"

CAT_REF = {
    "How-To": "9d3210aa-e6e1-4391-b1fd-a634147de088",
    "Best Practice": "a5d8df07-3ab1-4411-a7b0-5b7fad3adf82",
    "Industry Solution": "247a9752-888d-44d1-b113-5f75edb5b96c",
    "Comparison": "9d3210aa-e6e1-4391-b1fd-a634147de088",
    "Branding": "5a9df9bb-d0b6-4ef9-8257-af3b470db780",
}
SCHEMA_MAP = {"How-To": "HowTo", "Comparison": "HowTo", "Best Practice": "HowTo", "Industry Solution": "Article", "Branding": "Article"}


def find_token():
    config = Path.home() / ".config" / "sanity" / "config.json"
    if config.exists():
        data = json.loads(config.read_text())
        tokens = []
        def walk(v):
            if isinstance(v, dict):
                for k, val in v.items():
                    if 'token' in k.lower() and isinstance(val, str) and len(val) > 20:
                        tokens.append(val)
                    walk(val)
            elif isinstance(v, list):
                for item in v:
                    walk(item)
        walk(data)
        if tokens: return tokens[0]
    raise RuntimeError("No Sanity token found")



def parse_fm(text: str) -> dict:
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m: return {}
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' not in line: continue
        k, v = line.split(':', 1);
        k, v = k.strip(), v.strip()
        if v.startswith('"') and v.endswith('"'): v = v[1:-1]
        if v.startswith("'") and v.endswith("'"): v = v[1:-1]
        if k == 'keywords':
            try: v = json.loads(v.replace("'", '"'))
            except: v = [x.strip().strip('"').strip("'") for x in v.strip('[]').split(',')] if v.startswith('[') else [v]
        fm[k] = v
    return fm


def build_doc(file_path: str) -> dict:
    text = Path(file_path).read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if len(parts) < 3: raise ValueError(f"Invalid frontmatter: {file_path}")
    fm = parse_fm(text)
    body_md = parts[2].strip().replace('\n\n\n', '\n\n')

    slug = fm.get('slug', Path(file_path).stem)
    blog_type = fm.get('category', 'How-To')
    cat_ref = CAT_REF.get(blog_type, CAT_REF['How-To'])
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

    body_blocks = md_to_pt(body_md)

    structured_json = json.dumps({
        "@context": "https://schema.org",
        "@type": SCHEMA_MAP.get(blog_type, "Article"),
        "headline": fm.get('title', ''),
        "author": {"@type": "Organization", "name": "Lovart"},
        "datePublished": now,
    }, ensure_ascii=False)

    doc = {
        "_id": slug,
        "_type": "blog",
        "title": fm.get('title', ''),
        "slug": {"_type": "slug", "current": slug},
        "language": "zh",
        "category": {"_type": "reference", "_ref": cat_ref},
        "description": (fm.get('description') or '')[:200],
        "keywords": fm.get('keywords', []),
        "seoTitle": (fm.get('seo_title') or '')[:70],
        "seoDescription": (fm.get('seo_description') or '')[:160],
        "coverUrl": fm.get('cover_url', ''),
        "altText": fm.get('alt_text', ''),
        "status": "draft",
        "noIndex": False,
        "contentCluster": fm.get('content_cluster', 'Zh-Batch2-Product'),
        "releaseDate": now,
        "publishedAt": now,
        "seo": {
            "structuredData": {
                "_type": "structuredData",
                "enabled": True,
                "json": structured_json
            }
        },
        "body": body_blocks,
    }
    return doc


def upsert(doc: dict, token: str, dry_run: bool = False) -> tuple:
    if dry_run:
        print(f"  [DRY-RUN] {doc['_id']:40s} | body={len(doc['body'])} blocks")
        return 0, "dry-run"
    url = f"{API_BASE}/mutate/{SANITY_DATASET}"
    mutation = {"mutations": [{"createIfNotExists": doc}]}
    req = urllib.request.Request(
        url, data=json.dumps(mutation).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        return 0, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--drafts-dir", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = find_token()
    drafts_dir = Path(args.drafts_dir)
    files = sorted(drafts_dir.glob("zh-*.md"))

    print(f"待导入: {len(files)} 篇 Blog")
    ok = fail = 0
    for fp in files:
        try:
            doc = build_doc(str(fp))
            rc, msg = upsert(doc, token, args.dry_run)
            if rc == 0:
                print(f"  {doc['_id']:40s} | body={len(doc['body'])} blocks")
                ok += 1
            else:
                print(f"  ERROR {doc['_id']}: HTTP {rc}")
                fail += 1
        except Exception as e:
            print(f"  ERROR {fp.name}: {str(e)[:100]}")
            fail += 1

    mode = "DRY-RUN" if args.dry_run else "导入"
    print(f"\n{mode}: {ok} 篇成功 / {fail} 篇失败")


if __name__ == "__main__":
    main()
