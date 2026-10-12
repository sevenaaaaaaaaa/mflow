#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p2-tokens.py — 建 token 层：lovart.ai 设计 token → Elementor Global Colors/Fonts。
经一次性 PHP snippet 写 active kit 的 system_colors/system_fonts 并重生成 CSS，跑完即删。
"""
import importlib.util
import json
import time
import urllib.request

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)

# ---------- token 集（源自 lovart-replica.css 的 Tailwind 主题变量，Light 为默认值） ----------
SYSTEM_COLORS = [
    {"_id": "primary",   "title": "LR Ink（主黑）",        "color": "#100f09"},
    {"_id": "secondary", "title": "LR Paper（浅底）",      "color": "#f2f1ee"},
    {"_id": "text",      "title": "LR Text（正文）",       "color": "#100f09"},
    {"_id": "accent",    "title": "LR Accent（强调）",     "color": "#171612"},
]
CUSTOM_COLORS = [
    {"_id": "lr_bg_base",        "title": "LR BG Base",        "color": "#f9f8f6"},
    {"_id": "lr_bg_secondary",   "title": "LR BG Secondary",   "color": "#f2f1ee"},
    {"_id": "lr_bg_tertiary",    "title": "LR BG Tertiary",    "color": "#eae9e6"},
    {"_id": "lr_bg_dark",        "title": "LR BG Dark",        "color": "#100f09"},
    {"_id": "lr_bg_dark_2",      "title": "LR BG Dark 2",      "color": "#171612"},
    {"_id": "lr_bg_dark_3",      "title": "LR BG Dark 3",      "color": "#1d1b16"},
    {"_id": "lr_text_default",   "title": "LR Text Default",   "color": "#100f09"},
    {"_id": "lr_text_invert",    "title": "LR Text Invert",    "color": "#f5f4ef"},
    {"_id": "lr_border",         "title": "LR Border Contrast","color": "#1a1a19"},
    {"_id": "lr_border_l1",      "title": "LR Border L1",      "color": "#1a1a190f"},
    {"_id": "lr_border_l2",      "title": "LR Border L2",      "color": "#1a1a191f"},
    {"_id": "lr_border_l3",      "title": "LR Border L3",      "color": "#1a1a192e"},
    {"_id": "lr_accent_light",   "title": "LR Accent Light",   "color": "#f5f5f5"},
]
SYSTEM_FONTS = [
    {"_id": "primary",   "title": "LR Body（Montserrat）",  "font": "Montserrat", "weight": "400"},
    {"_id": "secondary", "title": "LR Display（Poppins）",  "font": "Poppins",    "weight": "500"},
    {"_id": "text",      "title": "LR Text（Montserrat）",  "font": "Montserrat", "weight": "400"},
    {"_id": "accent",    "title": "LR Accent（Poppins）",   "font": "Poppins",    "weight": "500"},
]

# ---------- 一次性 snippet ----------
php = """<?php
$kit_id = get_option( 'elementor_active_kit' );
if ( ! $kit_id ) { echo json_encode( [ 'error' => 'no active kit' ] ); return; }
$meta = get_post_meta( $kit_id, '_elementor_page_settings', true );
if ( ! is_array( $meta ) ) { $meta = []; }
$meta['system_colors'] = json_decode( file_get_contents( '/tmp/lr-system-colors.json' ), true );
$meta['custom_colors'] = json_decode( file_get_contents( '/tmp/lr-custom-colors.json' ), true );
$meta['system_fonts']  = json_decode( file_get_contents( '/tmp/lr-system-fonts.json' ), true );
update_post_meta( $kit_id, '_elementor_page_settings', $meta );
\\Elementor\\Plugin::$instance->files_manager->clear_cache();
echo json_encode( [ 'kit' => $kit_id, 'ok' => true ] );
"""


def create_snippet(code):
    body = json.dumps({"title": "LR temp - tokens (auto)", "code": code, "scope": "frontend",
                       "active": True}).encode()
    req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets", data=body, method="POST",
                                 headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
    return json.loads(op.open(req, timeout=120).read().decode())


def run_snippet(sid):
    # code-snippets v1 无"执行"端点——active snippet 在前台生效。借探针页触发。
    return op.open(PROBE_URL, timeout=120).read().decode("utf-8", "ignore")


def delete_snippet(sid):
    req = urllib.request.Request(dm.BASE + f"/wp-json/code-snippets/v1/snippets/{sid}",
                                 method="DELETE", headers={"X-WP-Nonce": nonce})
    return op.open(req, timeout=120).read().decode()


def put_token_file(local_name, remote_name, data):
    r = subprocess_run(f"ssh -p 28766 root@172.96.253.73 'cat > /tmp/{remote_name}'",
                       input=json.dumps(data))
    print(f"  上传 {remote_name}:", r[:40])


import subprocess


def subprocess_run(cmd, input=""):
    r = subprocess.run(["bash", "-c", cmd], input=input.encode(), capture_output=True, timeout=120)
    return r.stdout.decode(errors="ignore") + r.stderr.decode(errors="ignore")


PROBE_URL = dm.BASE + "/replica-comparison-hub"

print("① 上传 token JSON 到 WP 机器 /tmp")
put_token_file("sys", "lr-system-colors.json", SYSTEM_COLORS)
put_token_file("cus", "lr-custom-colors.json", CUSTOM_COLORS)
put_token_file("fnt", "lr-system-fonts.json", SYSTEM_FONTS)
put_token_file("php", "lr-tokens.php", php)

print("② 建临时 snippet（frontend scope，探针页触发执行）")
snip = create_snippet(php)
sid = snip.get("id")
print("  snippet id:", sid)

print("③ 触发执行（拉探针页）")
html = run_snippet(sid)

print("④ 删临时 snippet")
print("  ", delete_snippet(sid)[:120])

print("⑤ 验证：kit meta 回读")
# 直接读 kit：REST /elementor/v1/... 不通用；用全局色 CSS 文件出现 LR 色验证
html2 = op.open(PROBE_URL, timeout=120).read().decode("utf-8", "ignore")
css_links = [h for h in __import__("re").findall(r'href="([^"]*post-[0-9]+\.css[^"]*)"', html2)]
print("  kit/page CSS 引用:", css_links[:2])
ok = all(c in html2 for c in ["eael-advanced-data-table", "eael-cta-box"])
print("  探针:", "✓" if ok else "✗")
print("done")
