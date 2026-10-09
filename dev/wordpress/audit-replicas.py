#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit-replicas.py — blogs.lovart.ai 复刻页审计（Elementor 原生架构版）。

背景架构（Round 35 起）：
  复刻页 = 真正的 Elementor 文档：_elementor_data（每 section 一个 container + HTML 微件），
  模板 elementor_header_footer（主题在渲染链上），作用域资产由 Code Snippets
  在 _lr_replica 标记页 enqueue（CSS v2 / JS defer+data-cfasync）。
  post_content 保留 Round 34 共享格式仅作 SEO/数据源，不参与前端渲染。

审计项：
  A. 复刻页（18 页）公开 HTML 深检：
     - template=elementor_header_footer；data-elementor-type="wp-page"；
       elementor-widget-html 微件 ≥2；.lr 包裹；lovart-replica.css?v=2；
       lr-replica-js 带 data-cfasync；lr-replica-page body class；单 doctype。
  B. 历史页零泄漏（全量 500+ 页，8 线程并发）：不加载复刻资产、无 .lr 包裹、
     无 lr-replica-page body class。
  C. 旧渲染通道已无依赖：无页面使用 lovart-replica-template。

全部走公开请求（REST 搜索 + 页面 GET），无需登录态。
用法：python3 audit-replicas.py [--out report.md] [--workers N]
"""
import argparse
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://blogs.lovart.ai"
ASSET_MARK = "lr-assets/lovart-replica"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")


def get_json(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def get_html(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def paged(fmt):
    out, pageno = [], 1
    while True:
        batch = get_json(fmt.replace("{P}", str(pageno)))
        out.extend(batch)
        if len(batch) < 100:
            return out
        pageno += 1


def check_replica(p):
    """A 节单页检查，返回 (slug, id, ok, detail)。"""
    fails = []
    if (p.get("template") or "") != "elementor_header_footer":
        fails.append("template=%s" % (p.get("template") or "default"))
    try:
        h = get_html(p["link"])
    except Exception as e:
        return p["slug"], p["id"], False, "FAIL 拉取异常 %s" % e
    if 'data-elementor-type="wp-page"' not in h:
        fails.append("非 Elementor 原生渲染")
    n_widgets = len(re.findall(r'class="[^"]*elementor-widget elementor-widget-html"', h))
    if n_widgets < 2:
        fails.append("HTML微件=%d" % n_widgets)
    if not re.search(r'class="lr(?: dark)?"', h):
        fails.append("缺 .lr 包裹")
    if "lovart-replica.css?v=2" not in h:
        fails.append("缺作用域 CSS v2")
    if not re.search(r'<script[^>]*lr-replica[^>]*data-cfasync="false"', h):
        fails.append("JS 缺 data-cfasync")
    if "lr-replica-page" not in h:
        fails.append("缺 lr-replica-page body class")
    if len(re.findall(r"<!doctype", h, re.I)) != 1:
        fails.append("doctype 异常")
    return p["slug"], p["id"], not fails, (
        "%s（%d 字节，%d 微件）" % ("OK" if not fails else "FAIL " + "、".join(fails), len(h), n_widgets))


def check_historical(p):
    """B 节单页检查，返回 (slug, id, status, detail)。status: ok/leak/error。"""
    try:
        h = get_html(p["link"])
    except Exception as e:
        return p["slug"], p["id"], "error", "拉取异常 %s（跳过）" % e
    fails = []
    if "lovart-replica.css" in h or "lovart-replica.js" in h:
        fails.append("加载了复刻资产")
    if re.search(r'class="lr(?: dark)?"', h):
        fails.append(".lr 包裹泄漏")
    if "lr-replica-page" in h:
        fails.append("lr-replica-page body class 泄漏")
    return p["slug"], p["id"], "leak" if fails else "ok", "、".join(fails)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="-")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    print("listing pages ...", flush=True)
    allp = paged(BASE + "/wp-json/wp/v2/pages?per_page=100&page={P}&_fields=id,slug,link,template")
    shared = paged(BASE + "/wp-json/wp/v2/pages?per_page=100&search=%s&page={P}&_fields=id,slug"
                   % urllib.parse.quote(ASSET_MARK))
    shared_ids = {p["id"] for p in shared}
    # search 只索引 post_content——若 Elementor 接管后 content 变化导致漏检，按已知 slug 集合兜底
    known = [p for p in allp if p["slug"].startswith(("replica-", "composite-replica-"))]
    for p in known:
        shared_ids.add(p["id"])
    replicas = [p for p in allp if p["id"] in shared_ids]
    historical = [p for p in allp if p["id"] not in shared_ids]

    lines = ["# blogs.lovart.ai 复刻页审计报告（Elementor 原生架构）", ""]
    lines.append("共 %d 页：Elementor 复刻 %d / 历史页 %d" % (len(allp), len(replicas), len(historical)))
    lines.append("")

    problems = 0
    lines.append("## A. 复刻页深检（公开渲染输出）")
    print("A: %d replica pages, workers=%d" % (len(replicas), args.workers), flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for slug, pid, ok, detail in ex.map(check_replica, replicas):
            if not ok:
                problems += 1
            lines.append("- `%s` (id=%s): %s" % (slug, pid, detail))
    lines.append("")

    lines.append("## B. 历史页零泄漏")
    print("B: %d historical pages ..." % len(historical), flush=True)
    done = leaks = errors = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for slug, pid, status, detail in ex.map(check_historical, historical):
            done += 1
            if done % 100 == 0:
                print("B progress: %d/%d" % (done, len(historical)), flush=True)
            if status == "leak":
                leaks += 1
                problems += 1
                lines.append("- `%s` (id=%s): FAIL %s" % (slug, pid, detail))
            elif status == "error":
                errors += 1
                lines.append("- `%s` (id=%s): %s" % (slug, pid, detail))
    lines.append("- 其余 %d 页 OK（无复刻资产加载、无 .lr 包裹、无 lr-replica-page）"
                 % (done - leaks - errors))
    lines.append("")

    lines.append("## C. 旧渲染通道依赖")
    old_tpl = [p for p in allp if (p.get("template") or "") == "lovart-replica-template"]
    if old_tpl:
        problems += len(old_tpl)
        for p in old_tpl:
            lines.append("- `%s` (id=%s): 仍使用 lovart-replica-template" % (p["slug"], p["id"]))
    else:
        lines.append("- 无页面使用旧渲染模板（Renderer 已无依赖）")
    lines.append("")

    lines.append("**结论：%s（问题数 %d）**" % ("通过" if problems == 0 else "存在问题", problems))
    report = "\n".join(lines)
    if args.out == "-":
        print(report)
    else:
        io.open(args.out, "w", encoding="utf-8").write(report)
        print(report)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())