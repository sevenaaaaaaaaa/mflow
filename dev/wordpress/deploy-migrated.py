#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deploy-migrated.py — 把 elem-migrated/ 里的迁移成果推到线上页面。

流程（每页）：
  1. lr_elem_read 备份当前 _elementor_data → native-rollout-backups/<批次>/<slug>.json
     （bridge 会直接覆盖 meta，没有这步就没有回滚）
  2. scp JSON 到资产服务器 lr-assets/elem/migrated/
  3. admin-ajax lr_elem_import page_id=<id>&url=<资产URL>

用法：
  python3 deploy-migrated.py            # 预演：只解析映射和备份，不上传不导入
  python3 deploy-migrated.py --write    # 真执行
"""
import argparse
import http.client
import http.cookiejar
import io
import json
import socket
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

BASE = "https://blogs.lovart.ai"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")
# 本地 DNS 与 DoH 各自返回不同边缘（30.100.x.x 是 Lovart 自有边缘，47.252.x 是阿里云），
# 可用性随时间漂移。启动时逐个探活（TLS 握手按域名校验证书），选第一个能用的。
CANDIDATE_IPS = ["30.100.1.151", "47.252.7.74"]
REAL_IP = CANDIDATE_IPS[0]
SECRET = "lrb-2026-x7k9"
ASSETS_HOST = "172.96.253.73"
ASSETS_PORT = "28766"
ASSETS_DIR = "/www/wwwroot/nownexts_com/lr-assets/elem/migrated"
ASSETS_URL = "https://nownexts.com/lr-assets/elem/migrated"
ROOT = Path(__file__).resolve().parent
BACKUP_DIR = ROOT / "native-rollout-backups" / ("pre-cta-faq-" + date.today().isoformat())


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """连接到钉扎 IP，但 SNI 与证书校验仍用原域名。"""

    def connect(self):
        conn = socket.create_connection((REAL_IP, 443), timeout=self.timeout)
        self.sock = self._context.wrap_socket(conn, server_hostname=self.host)


class _PinnedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_PinnedHTTPSConnection, req, context=self._context)


def build_opener():
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj), _PinnedHTTPSHandler())
    op.addheaders = [("User-Agent", UA)]
    return op


def login(op):
    lines = io.open("/tmp/.wp-auth.tmp", encoding="utf-8").read().strip().split("\n")
    op.open(BASE + "/wp-login.php", timeout=60)
    data = urllib.parse.urlencode({
        "log": lines[0], "pwd": lines[-1], "wp-submit": "Log In",
        "redirect_to": BASE + "/wp-admin/", "testcookie": "1",
    }).encode()
    op.open(urllib.request.Request(BASE + "/wp-login.php", data=data), timeout=60)


def rest_nonce(op):
    return op.open(BASE + "/wp-admin/admin-ajax.php?action=rest-nonce",
                   timeout=60).read().decode().strip()


def _retry(fn, tries=5):
    import time
    for i in range(tries):
        try:
            return fn()
        except Exception as e:
            if i == tries - 1:
                raise
            wait = 8 * (i + 1)
            print(f"  … 第{i + 1}次失败（{e}），{wait}s 后重试", flush=True)
            time.sleep(wait)


def api(op, nonce, path):
    req = urllib.request.Request(BASE + path, headers={"X-WP-Nonce": nonce})
    return _retry(lambda: json.loads(op.open(req, timeout=120).read().decode()))


def admin_ajax(op, params):
    body = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(BASE + "/wp-admin/admin-ajax.php", data=body)
    return _retry(
        lambda: json.loads(op.open(req, timeout=180).read().decode()))


def _pin_probe():
    """探活候选边缘：TLS 握手（证书按 blogs.lovart.ai 校验）+ 简单 GET。"""
    global REAL_IP
    for ip in CANDIDATE_IPS:
        try:
            conn = socket.create_connection((ip, 443), timeout=8)
            ctx = ssl.create_default_context()
            tls = ctx.wrap_socket(conn, server_hostname="blogs.lovart.ai")
            tls.sendall(b"GET / HTTP/1.1\r\nHost: blogs.lovart.ai\r\n"
                        b"User-Agent: probe\r\nConnection: close\r\n\r\n")
            status = tls.recv(64).decode(errors="ignore")
            tls.close()
            if status.startswith("HTTP/") and (" 200" in status or " 30" in status):
                REAL_IP = ip
                print(f"边缘探活：使用 {ip}", flush=True)
                return
        except Exception as e:
            print(f"  ✗ {ip} 不可用（{e}）", flush=True)
    sys.exit("✗ 所有候选边缘都不可用，稍后再试")


def main():
    _pin_probe()
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--batch", default="elem-migrated")
    ap.add_argument("--exclude", default="", help="逗号分隔的文件名，跳过不部署")
    args = ap.parse_args()

    files = sorted((ROOT / args.batch).glob("*.json"))
    if not files:
        sys.exit(f"✗ {args.batch}/ 里没有文件")
    excl = {e.strip() for e in args.exclude.split(",") if e.strip()}
    files = [f for f in files if f.name not in excl]
    slugs = [f.stem for f in files]

    op = build_opener()
    login(op)
    nonce = rest_nonce(op)

    # 1) slug → page_id（REST 按 slug 精确查）
    mapping, missing = {}, []
    for slug in slugs:
        r = api(op, nonce, f"/wp-json/wp/v2/pages?slug={slug}&_fields=id,link,status")
        if r:
            mapping[slug] = r[0]["id"]
        else:
            missing.append(slug)
    print(f"映射：{len(mapping)} 页有对应线上页面，{len(missing)} 页没有")
    for s in missing:
        print(f"  ✗ 无页面：{s}")
    if missing:
        sys.exit("✗ 存在无对应的页面，中止（先核对 slug 口径）")

    # 2) 备份（无论预演与否都做——备份是只读操作，且是回滚的唯一凭据）
    #    若同名备份已存在则跳过：那是迁移前的原始快照，重跑导入绝不能覆盖它
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for slug, pid in mapping.items():
        dst = BACKUP_DIR / f"{slug}.json"
        if dst.exists():
            print(f"  ↷ {slug}：已有迁移前备份，跳过", flush=True)
            continue
        r = admin_ajax(op, {"action": "lr_elem_read", "page_id": pid, "secret": SECRET})
        data = r.get("data") if isinstance(r, dict) else None
        if not data or not data.get("data"):
            print(f"  ⚠ {slug} (id={pid})：lr_elem_read 无数据，照常备份空值标记", flush=True)
        dst.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"备份完成 → {BACKUP_DIR.name}/（{len(mapping)} 页）", flush=True)

    if not args.write:
        print("\n（预演结束：未上传、未导入。加 --write 执行）")
        return 0

    # 3) 上传资产
    subprocess.run(
        ["ssh", "-p", ASSETS_PORT, f"root@{ASSETS_HOST}", "mkdir", "-p", ASSETS_DIR],
        check=True)
    subprocess.run(
        ["scp", "-P", ASSETS_PORT] + [str(f) for f in files] +
        [f"root@{ASSETS_HOST}:{ASSETS_DIR}/"], check=True, cwd=ROOT)
    print(f"已上传 {len(files)} 个 JSON → {ASSETS_URL}/")

    # 4) 逐页导入
    fails = []
    for slug, pid in mapping.items():
        r = admin_ajax(op, {
            "action": "lr_elem_import", "page_id": pid,
            "url": f"{ASSETS_URL}/{slug}.json", "secret": SECRET})
        if isinstance(r, dict) and r.get("success"):
            print(f"  ✓ {slug} (id={pid}) → elements={r['data']['elements']}")
        else:
            print(f"  ✗ {slug} (id={pid}) → {json.dumps(r, ensure_ascii=False)[:200]}")
            fails.append(slug)
    if fails:
        print(f"\n✗ {len(fails)} 页导入失败：{fails}")
        return 1
    print(f"\n全部 {len(mapping)} 页导入成功。下一步：验证渲染 → 删 replica.js 注入 → bump 版本。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
