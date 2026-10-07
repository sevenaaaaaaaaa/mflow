"""wp_blocks — MFlow 适配器：IR → WordPress（Gutenberg lovart/{type} 区块）。"""
import json
import os
import re
IR_VERSION = "1.0"  # 与 replication_core.IR_VERSION 同步


def sanitize_type(t):
    return re.sub(r"[^a-z0-9-]", "", t.lower())


def ir_to_theme_blocks(ir, theme_dir):
    """IR → 主题区块产物。

    每个 section 生成 blocks/{type}/：block.json + render.php（section.html 直出）。
    同时写 assets/lovart-site.css（IR design.css）与 assets/lovart-tokens.json。
    返回 {blocks: [type], cssBytes, themeDir}。
    """
    blocks_dir = os.path.join(theme_dir, "blocks")
    assets_dir = os.path.join(theme_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    types = []
    for s in ir["sections"]:
        typ = sanitize_type(s["type"])
        d = os.path.join(blocks_dir, typ)
        os.makedirs(d, exist_ok=True)
        # 真实 SSR HTML 直出（render.php 从文件读，主题激活后即时生效）
        open(os.path.join(d, "section.html"), "w",
             encoding="utf-8").write(s["html"])
        meta = {
            "$schema": "https://schemas.wp.org/trunk/block.json",
            "apiVersion": 3, "name": f"lovart/{typ}", "version": IR_VERSION,
            "title": f"Lovart {typ}", "category": "lovart", "icon": "layout",
            "description": f"1:1 replica of source {typ} section.",
            "supports": {"align": ["full", "wide"], "html": False},
        }
        json.dump(meta, open(os.path.join(d, "block.json"), "w"),
                  ensure_ascii=False, indent=1)
        open(os.path.join(d, "render.php"), "w", encoding="utf-8").write(
            "<?php\n/** Lovart %s — 1:1 SSR replica (replication-core %s). */\n"
            "$h = file_get_contents(get_theme_file_path('blocks/%s/section.html'));\n"
            "echo $h;\n" % (typ, IR_VERSION, typ))
        types.append(typ)
    open(os.path.join(assets_dir, "lovart-site.css"), "w",
         encoding="utf-8").write(ir["design"]["css"])
    json.dump(ir["design"].get("tokens", {}),
              open(os.path.join(assets_dir, "lovart-tokens.json"), "w"),
              ensure_ascii=False, indent=1)
    return {"blocks": types, "cssBytes": len(ir["design"]["css"]), "themeDir": theme_dir}


def ir_to_page_content(ir):
    """IR → 页面内容（Gutenberg 注释 × sections 顺序）。"""
    return "\n".join(f"<!-- wp:lovart/{sanitize_type(s['type'])} /-->"
                     for s in ir["sections"]) + "\n"


def dark_class_filter_snippet(page_slugs):
    """复刻页深色模式 body_class 片段（class-based dark 源站适用）。"""
    slugs = ", ".join(f"'{s}'" for s in page_slugs)
    return ("add_filter('body_class', function ($classes) {\n"
            "    if (is_page([%s])) { $classes[] = 'dark'; }\n"
            "    return $classes;\n});\n" % slugs)
