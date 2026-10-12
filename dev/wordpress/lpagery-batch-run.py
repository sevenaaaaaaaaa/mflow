#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lpagery-batch-run.py — 【已弃用】LPagery 直驱通道（保留作历史记录）。

弃用原因（2026-10-13 线上实测）：LPagery free 版占位符列数上限 = 3
（InputParamProvider::lpagery_get_input_params_without_images 的
get_placeholder_counts() 熔断，超出列直接 break 丢弃），126 列契约只有前 3 列
（page_title/slug/industry）进替换引擎，meta 里其余占位符全部残留。
且 free 版 slug 由模板页标题派生（get_slug 读 template_post->post_title），
process config 的 slug 模式是 premium 路径。

替代：lr-batch-run.py（snippet 29 lr_batch_page 自建通道）。

用法（如仍要试 LPagery）：
  python3 -u lpagery-batch-run.py --setup        # 建/复位模板页 + 推种子 JSON + 抓 nonce 自检
  python3 -u lpagery-batch-run.py --run          # 按样本 CSV 建 draft 页
  python3 -u lpagery-batch-run.py --publish      # 验证通过后发布（--slugs 逗号分隔，缺省全部）
"""
import argparse
import csv
import io
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

import importlib.util
_spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dm)

BASE = dm.BASE
SECRET = dm.SECRET
ASSETS_HOST = dm.ASSETS_HOST
ASSETS_PORT = dm.ASSETS_PORT
ROOT = Path(__file__).resolve().parent
SEED_SLUG = "lp-lr-native-v1"
CSV_PATH = ROOT / "native-modules" / "lp-lr-native-v1-sample.csv"


def admin_ajax_post(op, fields, timeout=300):
    body = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(BASE + "/wp-admin/admin-ajax.php", data=body)
    return json.loads(op.open(req, timeout=timeout).read().decode())


def rest_pages(op, nonce, method, path, payload=None):
    req = urllib.request.Request(
        BASE + path, method=method,
        data=json.dumps(payload).encode() if payload else None,
        headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
    return json.loads(op.open(req, timeout=120).read().decode())


def setup_template(op, nonce):
    """建/复位种子模板页并推入 pro JSON。"""
    # 1) 页面（复用已存在的）。线上 17 复刻页口径 = elementor_header_footer
    r = rest_pages(op, nonce, "GET",
                   f"/wp-json/wp/v2/pages?slug={SEED_SLUG}&status=draft,publish,pending&_fields=id,status,link")
    if r:
        pid, status = r[0]["id"], r[0]["status"]
        print(f"模板页已存在 id={pid} status={status}")
        rest_pages(op, nonce, "POST", f"/wp-json/wp/v2/pages/{pid}",
                   {"status": "draft", "template": "elementor_header_footer"})
    else:
        r = rest_pages(op, nonce, "POST", "/wp-json/wp/v2/pages", {
            "title": "LPagery LR Native Seed", "slug": SEED_SLUG,
            "status": "draft", "template": "elementor_header_footer"})
        pid = r["id"]
        print(f"模板页新建 id={pid}")
    # template 字段回读确认
    chk = rest_pages(op, nonce, "GET",
                     f"/wp-json/wp/v2/pages/{pid}?_fields=id,template,status")
    print("回读:", chk)

    # 2) 种子 JSON 上资产服务器（seed/ 子目录）
    seed_file = ROOT / "native-modules" / "lp-lr-native-v1-pro.json"
    subprocess.run(
        ["ssh", "-p", ASSETS_PORT, f"root@{ASSETS_HOST}",
         "mkdir", "-p", "/www/wwwroot/nownexts_com/lr-assets/elem/seed"],
        check=True)
    subprocess.run(
        ["scp", "-P", ASSETS_PORT, str(seed_file),
         f"root@{ASSETS_HOST}:/www/wwwroot/nownexts_com/lr-assets/elem/seed/lp-lr-native-v1-pro.json"],
        check=True, cwd=ROOT)
    seed_url = "https://nownexts.com/lr-assets/elem/seed/lp-lr-native-v1-pro.json"

    # 3) bridge 导入（写 _elementor_data + _lr_replica）
    r = admin_ajax_post(op, {"action": "lr_elem_import", "page_id": pid,
                             "url": seed_url, "secret": SECRET})
    if isinstance(r, dict) and r.get("success"):
        print("种子导入 ✓", r.get("data"))
    else:
        sys.exit(f"✗ 种子导入失败: {json.dumps(r, ensure_ascii=False)[:300]}")
    return pid


def get_lpagery_nonce(op):
    """经 lr-elem-bridge 的 lr_lpagery_nonce action 生成 lpagery_ajax nonce
    （dashboard 页面 HTML 里没有该 nonce，只能服务端生成）。"""
    r = admin_ajax_post(op, {"action": "lr_lpagery_nonce", "secret": SECRET})
    if not (isinstance(r, dict) and r.get("success")):
        sys.exit(f"✗ lr_lpagery_nonce 失败: {json.dumps(r, ensure_ascii=False)[:200]}")
    n = r["data"]["nonce"]
    print("nonce:", n)
    return n


def run_batch(op, nonce, tpl_pid, limit=None):
    n = get_lpagery_nonce(op)
    # 1) upsert process（复用同名）
    search = admin_ajax_post(op, {
        "action": "lpagery_search_processes", "_wpnonce": n, "search": ""})
    existing = [p for p in (search if isinstance(search, list) else search.get("data", []))
                if isinstance(p, dict) and p.get("post_id") == tpl_pid]
    if existing:
        process_id = existing[0]["id"]
        print(f"复用 Page Set id={process_id}")
    else:
        up = admin_ajax_post(op, {
            "action": "lpagery_upsert_process", "_wpnonce": n,
            "post_id": tpl_pid, "purpose": "LR Native 投放页",
            "data[slug]": "{slug}", "data[parent_path]": "0",
            "data[status]": "draft"})
        if not up.get("success"):
            sys.exit(f"✗ upsert_process 失败: {json.dumps(up, ensure_ascii=False)[:300]}")
        process_id = up["process_id"]
        print(f"Page Set 新建 id={process_id}")

    # 2) 逐行建页
    with io.open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if limit:
        rows = rows[:limit]
    creation_id = uuid.uuid4().hex[:12]
    results = []
    for i, row in enumerate(rows):
        r = admin_ajax_post(op, {
            "action": "lpagery_create_posts", "_wpnonce": n,
            "process_id": process_id, "creation_id": creation_id,
            "index": i, "is_last_page": "true" if i == len(rows) - 1 else "false",
            "data": json.dumps(row, ensure_ascii=False),
            "client_generated_slug": row["slug"], "status": "draft",
            "existing_page_update_action": "create",
            "force_update_content": "false", "overwrite_manual_changes": "false"},
            timeout=300)
        ok = isinstance(r, dict) and r.get("success")
        results.append((row["slug"], r.get("mode"), ok, r))
        print(f"  [{'✓' if ok else '✗'}] {row['slug']} → mode={r.get('mode')} "
              f"{'' if ok else json.dumps(r, ensure_ascii=False)[:200]}")
        time.sleep(2)
    bad = [s for s, _, ok, _ in results if not ok]
    if bad:
        sys.exit(f"✗ 失败行: {bad}")
    print(f"\n{len(results)} 行全部处理完成（Page Set {process_id}）。")


def publish(op, nonce, slugs):
    for slug in slugs:
        r = rest_pages(op, nonce, "GET",
                       f"/wp-json/wp/v2/pages?slug={slug}&status=draft,publish,pending&_fields=id,status")
        if not r:
            print(f"  ✗ {slug}: 无页面"); continue
        pid = r[0]["id"]
        rest_pages(op, nonce, "POST", f"/wp-json/wp/v2/pages/{pid}",
                   {"status": "publish"})
        print(f"  ✓ {slug} (id={pid}) → publish")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--setup", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--slugs", default="")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    op = dm.build_opener()
    dm.login(op)
    nonce = dm.rest_nonce(op)

    if args.setup:
        setup_template(op, nonce)
        get_lpagery_nonce(op)  # 自检 nonce 可抓
        print("\nsetup 完成。下一步: --run")
    if args.run:
        tpl = rest_pages(op, nonce, "GET",
                         f"/wp-json/wp/v2/pages?slug={SEED_SLUG}&status=draft,publish,pending&_fields=id")
        run_batch(op, nonce, tpl[0]["id"], limit=args.limit)
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
