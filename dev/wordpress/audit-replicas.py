#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit-replicas.py — blogs.lovart.ai 全站复刻页审计（毛病四的解：页面多、发现不了不兼容）。

策略（避免下载旧页 2.7MB×N）：
  1. 轻量拉全站页面清单（不含 content）
  2. REST search 定位：lr-assets 引用集（新格式复刻页）、旧序列化标记集（待转换页）
  3. 只对「新格式页」逐页拉 content 深检（每页 ~140KB）
  4. 博客页泄漏 = lr-assets 引用集里出现非复刻页

检查项（新格式页）：CSS link、JS src、.lr 包裹类、无旧版内联 style、canvas 模板。
用法（在 MFlow 服务器上，凭据 /tmp/.wp-auth.tmp）：
  python3 audit-replicas.py [--out report.md]
"""
import argparse
import http.cookiejar
import io
import json
import re
import sys
import urllib.parse
import urllib.request

BASE = "https://blogs.lovart.ai"
ASSET = "lr-assets"
LEGACY_MARK = "sheet 0 ==="


def build_opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def login(op):
    lines = open("/tmp/.wp-auth.tmp", encoding="utf-8").read().strip().split("\n")
    USER, PASS = lines[0], lines[-1]
    op.open(BASE + "/wp-login.php")
    data = urllib.parse.urlencode({
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": BASE + "/wp-admin/", "testcookie": "1",
    }).encode()
    op.open(urllib.request.Request(BASE + "/wp-login.php", data=data))


def get_json(op, url, timeout=60):
    return json.loads(op.open(url, timeout=timeout).read().decode("utf-8"))


def paged(op, fmt, timeout=60):
    out, pageno = [], 1
    while True:
        batch = get_json(op, fmt.replace("{P}", str(pageno)), timeout)
        out.extend(batch)
        if len(batch) < 100:
            return out
        pageno += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="-")
    args = ap.parse_args()

    op = build_opener()
    login(op)

    # 1) 全站清单（轻）
    allp = paged(op, BASE + "/wp-json/wp/v2/pages?per_page=100&page={P}&_fields=id,slug,link,status,template")
    # 2) search 定位
    shared = paged(op, BASE + "/wp-json/wp/v2/pages?per_page=100&search=%s&page={P}&_fields=id,slug,template" % urllib.parse.quote(ASSET + "/lovart-replica"))
    legacy = paged(op, BASE + "/wp-json/wp/v2/pages?per_page=100&search=%s&page={P}&_fields=id,slug,template" % urllib.parse.quote(LEGACY_MARK))
    shared_ids = {p["id"] for p in shared}
    legacy_ids = {p["id"] for p in legacy} - shared_ids
    blog_pages = [p for p in allp if p["id"] not in shared_ids and p["id"] not in legacy_ids]

    lines = ["# blogs.lovart.ai 复刻页审计报告", ""]
    lines.append("共 %d 页：共享格式复刻 %d / 旧内联复刻 %d / 博客页 %d" % (
        len(allp), len(shared_ids), len(legacy_ids), len(blog_pages)))
    lines.append("")

    problems = 0
    lines.append("## 共享格式复刻页（新）深检")
    for p in shared:
        full = get_json(op, "%s/wp-json/wp/v2/pages/%d?_fields=slug,template,content" % (BASE, p["id"]))
        c = full["content"]["rendered"]
        fails = []
        if ASSET + "/lovart-replica.css" not in c:
            fails.append("缺 CSS link")
        if ASSET + "/lovart-replica.js" not in c:
            fails.append("缺 JS")
        if not re.search(r'class="lr(?: dark)?"', c):
            fails.append("缺 .lr 包裹")
        if LEGACY_MARK in c:
            fails.append("残留旧内联 style")
        if len(c) > 400000:
            fails.append("content 异常大 %d" % len(c))
        if (full.get("template") or "") != "elementor_canvas":
            fails.append("模板=%s" % full.get("template"))
        if fails:
            problems += 1
        lines.append("- `%s` (id=%s): %s（%d 字节）" % (
            p["slug"], p["id"], "OK" if not fails else "FAIL " + "、".join(fails), len(c)))
    lines.append("")

    lines.append("## 旧内联复刻页（待转换）")
    for p in allp:
        if p["id"] in legacy_ids:
            lines.append("- `%s` (id=%s): 旧 2.7MB 内联格式，建议用 build-payload.py --from-live 转换" % (p["slug"], p["id"]))
    lines.append("")

    lines.append("## 博客页泄漏检查")
    leaks = [p for p in shared if p["id"] not in shared_ids]
    # shared 集合里若混入非复刻页（search 命中但不是复刻页），上面推导保证 shared ⊂ 引用集；
    # 反向：博客页不应出现在 shared/legacy。上面 allp 分类已保证。
    # 额外确认：搜索 'class="lr' 独立命中
    lr_class_hits = paged(op, BASE + '/wp-json/wp/v2/pages?per_page=100&search=%s&page={P}&_fields=id,slug' % urllib.parse.quote('class="lr'))
    extra = [p for p in lr_class_hits if p["id"] not in shared_ids and p["id"] not in legacy_ids]
    if extra:
        problems += len(extra)
        for p in extra:
            lines.append("- `%s` (id=%s): 出现 .lr 包裹类泄漏" % (p["slug"], p["id"]))
    else:
        lines.append("无泄漏")
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