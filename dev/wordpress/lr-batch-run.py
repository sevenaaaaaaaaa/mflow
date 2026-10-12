#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lr-batch-run.py — LR Native 批量建页产线 v2（自建通道，不依赖 LPagery tier）。

背景：LPagery free 版占位符上限 3 列（get_placeholder_counts），126 列契约走不通；
改走 snippet 39 的 lr_batch_page：本地按 CSV 行替换 {col} → 上传 batch/<slug>.json
→ 服务端拉取建页（绕 WAF）。

用法：
  python3 -u lr-batch-run.py --run            # 全部行建 draft 页
  python3 -u lr-batch-run.py --run --limit 1  # 只跑前 N 行
  python3 -u lr-batch-run.py --publish        # 发布（--slugs 缺省全部）
  python3 -u lr-batch-run.py --clean <slug>…  # 彻底删除指定页
"""
import argparse
import csv
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import importlib.util
_spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dm)

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "native-modules" / "lp-lr-native-v1-sample.csv"
SEED = ROOT / "native-modules" / "lp-lr-native-v1-pro.json"
BATCH_DIR = "/www/wwwroot/nownexts_com/lr-assets/batch"
BATCH_URL = "https://nownexts.com/lr-assets/batch"


def admin_ajax_post(op, fields, timeout=300):
    body = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(dm.BASE + "/wp-admin/admin-ajax.php", data=body)
    return json.loads(op.open(req, timeout=timeout).read().decode())


def rest_pages(op, nonce, method, path, payload=None):
    req = urllib.request.Request(
        dm.BASE + path, method=method,
        data=json.dumps(payload).encode() if payload else None,
        headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
    r = op.open(req, timeout=120)
    body = r.read().decode()
    return json.loads(body) if body.strip() else {}


def substitute(obj, row):
    """递归替换 {col} 占位符（只动字符串叶子；逐列 replace，一处占位符多 section 共用）。"""
    if isinstance(obj, str):
        for k, v in row.items():
            obj = obj.replace("{%s}" % k, v)
        return obj
    if isinstance(obj, list):
        return [substitute(x, row) for x in obj]
    if isinstance(obj, dict):
        return {k: substitute(v, row) for k, v in obj.items()}
    return obj


def leftover_tokens(obj):
    import re
    found = set()

    def walk(o):
        if isinstance(o, str):
            found.update(re.findall(r"\{[a-z0-9_]+\}", o))
        elif isinstance(o, list):
            for x in o:
                walk(x)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
    walk(obj)
    return sorted(found)


def run(op, nonce, limit):
    seed = json.load(io.open(SEED, encoding="utf-8"))
    with io.open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if limit:
        rows = rows[:limit]

    ok = True
    for row in rows:
        slug = row["slug"]
        payload = {
            "slug": slug,
            "title": row["page_title"],
            "status": "draft",
            "elementor": {"version": seed["version"],
                          "data": substitute(seed["data"], row)},
            "seo": {"rank_math_title": row.get("seo_title", ""),
                    "rank_math_description": row.get("meta_description", ""),
                    "rank_math_canonical": row.get("canonical_url", "")},
        }
        left = leftover_tokens(payload["elementor"]["data"])
        if left:
            print(f"  ✗ {slug}: 替换后仍有 {len(left)} 个残留占位符 {left[:6]}")
            ok = False
            continue
        local = ROOT / "native-modules" / "batch" / f"{slug}.json"
        local.parent.mkdir(parents=True, exist_ok=True)
        with io.open(local, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)

        subprocess_up(slug, local)

        r = admin_ajax_post(op, {"action": "lr_batch_page", "secret": dm.SECRET,
                                 "url": f"{BATCH_URL}/{slug}.json"})
        if isinstance(r, dict) and r.get("success"):
            d = r["data"]
            print(f"  ✓ {slug} → id={d['page']} created={d['created']} elements={d['elements']}")
        else:
            print(f"  ✗ {slug} → {json.dumps(r, ensure_ascii=False)[:200]}")
            ok = False
        time.sleep(1)
    return ok


def subprocess_up(slug, local):
    import subprocess
    subprocess.run(
        ["ssh", "-p", dm.ASSETS_PORT, f"root@{dm.ASSETS_HOST}",
         "mkdir", "-p", BATCH_DIR], check=True)
    subprocess.run(
        ["scp", "-P", dm.ASSETS_PORT, str(local),
         f"root@{dm.ASSETS_HOST}:{BATCH_DIR}/{slug}.json"],
        check=True, cwd=ROOT)


def publish(op, nonce, slugs):
    for slug in slugs:
        r = rest_pages(op, nonce, "GET",
                       f"/wp-json/wp/v2/pages?slug={slug}&status=draft,publish,pending&_fields=id,status")
        if not r:
            print(f"  ✗ {slug}: 无页面")
            continue
        pid = r[0]["id"]
        rest_pages(op, nonce, "POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "publish"})
        print(f"  ✓ {slug} (id={pid}) → publish")


def clean(op, nonce, slugs):
    for slug in slugs:
        r = rest_pages(op, nonce, "GET",
                       f"/wp-json/wp/v2/pages?slug={slug}&status=draft,publish,pending&_fields=id")
        if not r:
            print(f"  ↷ {slug}: 无页面")
            continue
        rest_pages(op, nonce, "DELETE", f"/wp-json/wp/v2/pages/{r[0]['id']}?force=true")
        print(f"  ✗ 已删除 {slug} (id={r[0]['id']})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--clean", nargs="*", default=None)
    ap.add_argument("--slugs", default="")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    op = dm.build_opener()
    dm.login(op)
    nonce = dm.rest_nonce(op)

    if args.clean is not None:
        slugs = args.clean if args.clean else []
        if not slugs:
            with io.open(CSV_PATH, encoding="utf-8") as f:
                slugs = [r["slug"] for r in csv.DictReader(f)]
        clean(op, nonce, slugs)
    if args.run:
        if not run(op, nonce, args.limit):
            sys.exit("\n✗ 存在失败行，先解决再 publish")
        print("\nrun 完成。下一步: 验证渲染 → --publish")
    if args.publish:
        slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
        if not slugs:
            with io.open(CSV_PATH, encoding="utf-8") as f:
                slugs = [r["slug"] for r in csv.DictReader(f)]
        publish(op, nonce, slugs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
