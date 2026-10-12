#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""upgrade-htmega7.py — 上传 zip 后点确认链接（overwrite=update-plugin）完成替换。"""
import importlib.util
import re
import urllib.request
import uuid

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
ZIP = "/tmp/ht-mega-3.2.7.zip"

# 1) 上传 zip（overwrite=replace-plugin 触发确认页）
up_html = op.open(dm.BASE + "/wp-admin/plugin-install.php?tab=upload", timeout=120).read().decode("utf-8", "ignore")
nonce = re.search(r'name="_wpnonce" value="([a-f0-9]+)"', up_html).group(1)

boundary = "----" + uuid.uuid4().hex


def field(name, value):
    return (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n").encode()


with open(ZIP, "rb") as f:
    data = f.read()
body = (field("action", "upload-plugin") + field("_wpnonce", nonce) + field("overwrite", "replace-plugin")
        + (f"--{boundary}\r\nContent-Disposition: form-data; name=\"pluginzip\"; filename=\"ht-mega-3.2.7.zip\"\r\n"
           f"Content-Type: application/zip\r\n\r\n").encode() + data
        + f"\r\n--{boundary}--\r\n".encode())
req = urllib.request.Request(dm.BASE + "/wp-admin/update.php?action=upload-plugin&overwrite=replace-plugin",
                             data=body, method="POST",
                             headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
res_body = op.open(req, timeout=900).read().decode("utf-8", "ignore")

# 2) 抓确认链接并 GET
m = re.search(r'href=[\'"]update\.php\?action=upload-plugin&(?:amp;)?package=(\d+)&(?:amp;)?overwrite=update-plugin&(?:amp;)?_wpnonce=([a-f0-9]+)[\'"]', res_body)
assert m, "未找到替换确认链接"
confirm = (f"{dm.BASE}/wp-admin/update.php?action=upload-plugin&package={m.group(1)}"
           f"&overwrite=update-plugin&_wpnonce={m.group(2)}")
print("提交替换…")
res_body = op.open(confirm, timeout=900).read().decode("utf-8", "ignore")
open("/tmp/htmega-final-res.html", "w").write(res_body)
plain = re.sub(r"<script.*?</script>", "", res_body, flags=re.S)
for pat in ["替换", "成功", "激活", "失败", "错误", "已升级"]:
    for mm in re.finditer(pat, plain):
        s = max(0, mm.start()-120); e = min(len(plain), mm.end()+200)
        frag = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", plain[s:e]).strip())[:220]
        print(f"[{pat}] {frag}")
        break

# 3) 验证
html = op.open(dm.BASE + "/replica-solution-ai-design-solution-for-shopify", timeout=60).read().decode("utf-8", "ignore")
print("资产 ver:", sorted(set(re.findall(r'ht-mega[^"\']*ver=([\d.]+)', html))))
print("pricing 类:", sorted(set(re.findall(r'htm25-pricing[a-z_-]*', html)))[:8])
print("testimonial 类:", sorted(set(re.findall(r'htm25-testimonials[a-z_-]*', html)))[:8])
print("timeline 类:", sorted(set(re.findall(r'htmega-vert[a-z_-]*', html)))[:4])
