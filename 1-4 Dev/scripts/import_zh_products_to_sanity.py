#!/usr/bin/env python3
"""
Lovart 中文 Product Page → Sanity 导入脚本
读取 NDJSON → createIfNotExists → Sanity production
用法:
  python3 import_zh_products_to_sanity.py --ndjson zh-products-batch2.ndjson [--dry-run]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

SANITY_PROJECT = "o11tm2qe"
SANITY_DATASET = "production"
API_VERSION = "2024-01-01"
API_BASE = f"https://{SANITY_PROJECT}.api.sanity.io/v{API_VERSION}/data"


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
        if tokens:
            return tokens[0]
    raise RuntimeError("No Sanity token found")


def upsert(doc: dict, token: str, dry_run: bool = False) -> tuple:
    if dry_run:
        print(f"  [DRY-RUN] {doc.get('_id','?'):40s} → {doc.get('category','?')}")
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
        data = json.loads(resp.read())
        return 0, json.dumps(data)[:150]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return e.code, body[:500]


def main():
    parser = argparse.ArgumentParser(description="Import zh product pages to Sanity")
    parser.add_argument("--ndjson", required=True, help="NDJSON file path")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    token = find_token()

    records = []
    with open(args.ndjson, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    print(f"待导入: {len(records)} 篇 Product Page")
    ok = fail = 0
    for doc in records:
        rc, msg = upsert(doc, token, args.dry_run)
        if rc == 0:
            ok += 1
        else:
            print(f"  ERROR {doc.get('_id','?')}: HTTP {rc} {msg[:100]}")
            fail += 1

    mode = "DRY-RUN" if args.dry_run else "导入"
    print(f"\n{mode}: {ok} 篇成功 / {fail} 篇失败")


if __name__ == "__main__":
    main()
