#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p2-verify.py — 回读 Elementor kit 的 system_colors/system_fonts 确认 token 落地。"""
import importlib.util
import json
import re
import subprocess
import urllib.request

spec = importlib.util.spec_from_file_location("dm", "deploy-migrated.py")
dm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dm)

op = dm.build_opener()
dm.login(op)
nonce = dm.rest_nonce(op)

php = """<?php
$kit_id = get_option( 'elementor_active_kit' );
$meta = get_post_meta( $kit_id, '_elementor_page_settings', true );
$out = [ 'kit' => $kit_id ];
if ( isset( $meta['system_colors'] ) ) {
    $out['system_colors'] = array_map( function ( $c ) { return $c['_id'] . '=' . $c['color']; }, (array) $meta['system_colors'] );
}
if ( isset( $meta['custom_colors'] ) ) {
    $out['custom_count'] = count( (array) $meta['custom_colors'] );
    $out['custom_ids'] = array_map( function ( $c ) { return $c['_id']; }, (array) $meta['custom_colors'] );
}
if ( isset( $meta['system_fonts'] ) ) {
    $out['fonts'] = array_map( function ( $f ) { return $f['_id'] . '=' . $f['font']; }, (array) $meta['system_fonts'] );
}
echo '<div style="display:none" id="lr-token-verify">' . json_encode( $out ) . '</div>';
"""

body = json.dumps({"title": "LR temp - verify tokens (auto)", "code": php, "scope": "global",
                   "active": True}).encode()
req = urllib.request.Request(dm.BASE + "/wp-json/code-snippets/v1/snippets", data=body, method="POST",
                             headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"})
snip = json.loads(op.open(req, timeout=120).read().decode())
sid = snip.get("id")
print("verify snippet id:", sid)

html = op.open(dm.BASE + "/replica-comparison-hub", timeout=120).read().decode("utf-8", "ignore")

# 删 snippet
req = urllib.request.Request(dm.BASE + f"/wp-json/code-snippets/v1/snippets/{sid}", method="DELETE",
                             headers={"X-WP-Nonce": nonce})
op.open(req, timeout=120).read()
print("已删临时 snippet")

m = re.search(r'id="lr-token-verify">(.*?)</div>', html)
if m:
    data = json.loads(m.group(1))
    print("kit id:", data.get("kit"))
    print("system_colors:", data.get("system_colors"))
    print("custom colors:", data.get("custom_count"), data.get("custom_ids"))
    print("fonts:", data.get("fonts"))
else:
    print("✗ 未捕获验证输出（snippet 未执行或读取失败）")
    print(html[html.find("lr-token-verify")-100:html.find("lr-token-verify")+300] if "lr-token-verify" in html else "无标记")
