"""replication CLI — 端到端复刻流水线。

用法：
  python cli.py probe --url https://www.lovart.ai/internal/composite-page-all
  python cli.py replicate --url <源页> --base <资源基准URL> --out <输出目录> \\
      [--anchor '<正则>'] [--dark class|prefers|none] [--trim-tail '<marker>']
      产出：ir.json + sections/*.html + report.md
  python cli.py to-wordpress --ir <ir.json> --theme-dir <主题目录> [--page-slug xxx]
      产出：主题 blocks/* + assets/* + 深色 body_class 片段
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replication_core import probe, extract_css, split_sections, ir, qa_compare  # noqa: E402
from adapters import wp_blocks  # noqa: E402


def cmd_probe(args):
    r = probe.probe_source(args.url)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


def cmd_replicate(args):
    from replication_core.extract_css import design_assets, absolutize
    from replication_core.split_sections import split_sections as split_html
    if args.html_file:
        html = open(args.html_file, encoding="utf-8", errors="ignore").read()
    else:
        html = probe.fetch(args.url, timeout=args.timeout)
    base = args.base or args.url
    # 环节 1：探测（有 html_file 时跳过网络探测，标注 offline）
    if args.html_file:
        p = {"url": args.url, "reachable": True, "ssr": True, "offline": True}
    else:
        p = probe.probe_source(args.url)
    # 环节 2：设计资产（离线模式支持 --css-file 注入）
    if args.css_file:
        css = open(args.css_file, encoding="utf-8", errors="ignore").read()
        design = {"css": css, "cssFiles": [{"file": args.css_file}],
                  "tokens": extract_css.extract_tokens(css),
                  "breakpoints": extract_css.extract_breakpoints(css),
                  "fonts": extract_css.extract_fonts(css)}
    else:
        design = extract_css.design_assets(html, base, timeout=args.timeout)
    # 环节 3：切分 + 修边
    sections = split_html(html, anchor_re=args.anchor)
    trimmed = []
    last_idx = len(sections) - 1
    for idx, s in enumerate(sections):
        h = s["html"]
        if args.trim_tail and idx == last_idx:
            h = split_sections.trim_after(h, args.trim_tail)
        if args.cut_before and idx == last_idx:
            h = split_sections.cut_before(h, args.cut_before)
        if args.remove_last and idx == last_idx:
            h = split_sections.remove_element(h, args.remove_last)
            h = split_sections.strip_trailing_unclosed(h)
            h = split_sections.remove_empty_tail_container(h)
            h = split_sections.balance_divs(h)
            h = split_sections.strip_trailing_orphan_closes(h)
        h = split_sections.trim_fragment(
            h, tail_markers=("<footer", "<script"), strip_scripts=True,
            balance=True, fix_tag=args.fix_tag)
        trimmed.append({**s, "html": h})
    # 环节 4：IR
    ir_doc = ir.build_ir(args.url, trimmed, design,
                         meta={"probed": p}, dark_mode=args.dark)
    ir_doc = ir.absolutize_ir(ir_doc, base)
    ok, errors = ir.validate_ir(ir_doc)
    os.makedirs(args.out, exist_ok=True)
    ir.save_ir(ir_doc, os.path.join(args.out, "ir.json"))
    for s in ir_doc["sections"]:
        d = os.path.join(args.out, "sections", s["type"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "section.html"), "w", encoding="utf-8").write(s["html"])
    # QA
    rendered_stub = "".join(s["html"] for s in ir_doc["sections"])
    qa = qa_compare.assert_sections(rendered_stub, [s["type"] for s in ir_doc["sections"]])
    open(os.path.join(args.out, "report.md"), "w", encoding="utf-8").write(
        "# replication report\n\nsource: %s\nIR validate: %s %s\nsections: %d\nQA: %s\n"
        % (args.url, ok, errors or "", len(ir_doc["sections"]),
           json.dumps(qa, ensure_ascii=False)))
    print(json.dumps({"out": args.out, "sections": len(ir_doc["sections"]),
                      "irValid": ok, "errors": errors, "qa": qa},
                     ensure_ascii=False))
    return 0 if ok and qa["pass"] else 1


def cmd_to_wordpress(args):
    ir_doc = ir.load_ir(args.ir)
    ok, errors = ir.validate_ir(ir_doc)
    if not ok:
        print("IR invalid:", errors)
        return 1
    r = wp_blocks.ir_to_theme_blocks(ir_doc, args.theme_dir)
    os.makedirs(os.path.join(args.theme_dir, "templates"), exist_ok=True)
    content = wp_blocks.ir_to_page_content(ir_doc)
    slug = args.page_slug or "composite-replica"
    tpl = _page_template(content, slug, r)
    open(os.path.join(args.theme_dir, "templates",
                      f"page-{slug}.html"), "w", encoding="utf-8").write(tpl)
    snippet = wp_blocks.dark_class_filter_snippet([slug])
    print(json.dumps({"blocks": r["blocks"], "pageSlug": slug,
                      "pageContentBytes": len(content),
                      "darkSnippetFile": "dark-class-filter.php（已输出到 theme 目录）"},
                     ensure_ascii=False))
    open(os.path.join(args.theme_dir, "dark-class-filter.php"), "w",
         encoding="utf-8").write("<?php\n" + snippet)
    return 0


def _page_template(content, slug, blocks_result):
    """全宽页面模板：真实 header/footer + 全宽 main + 内容占位。"""
    W = os.path.dirname(os.path.abspath(__file__))
    header_p = os.path.join(W, "..", "wordpress", "lovart-theme", "lovart-theme",
                            "assets", "site-header.html")
    footer_p = os.path.join(W, "..", "wordpress", "lovart-theme", "lovart-theme",
                            "assets", "site-footer.html")
    header = open(header_p, encoding="utf-8").read() if os.path.exists(header_p) else "<header></header>"
    footer = open(footer_p, encoding="utf-8").read() if os.path.exists(footer_p) else "<footer></footer>"
    return (header +
            '\n<!-- wp:group {"tagName":"main","layout":{"type":"constrained",'
            '"contentSize":"1480px","wideSize":"1480px"}} -->\n<main class="wp-block-group">\n'
            "<!-- wp:post-content {\"layout\":{\"type\":\"default\"}} /-->\n"
            "</main>\n<!-- /wp:group -->\n" + footer)


def main():
    ap = argparse.ArgumentParser(prog="replication")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("probe")
    p1.add_argument("--url", required=True)
    p1.set_defaults(func=cmd_probe)
    p2 = sub.add_parser("replicate")
    p2.add_argument("--url", required=True)
    p2.add_argument("--html-file", default=None, help="从已抓取的 HTML 文件复刻（离线模式，跳过源探测抓取）")
    p2.add_argument("--base", default=None, help="资源基准 URL（默认=源 URL）")
    p2.add_argument("--out", required=True)
    p2.add_argument("--anchor", default=r'id="internal-section-\d+"[^>]*>'
                                       r'<div class="contents" data-lp-section="([a-z0-9-]+)"')
    p2.add_argument("--dark", default="class")
    p2.add_argument("--trim-tail", default=None)
    p2.add_argument("--remove-last", default=None,
                    help="从最后片段移除整个元素（如 '<aside' 预览工具面板）")
    p2.add_argument("--cut-before", default=None,
                    help="截掉最后片段中该标记（含）之后的尾部杂物，如 '<aside'（预览工具面板）")
    p2.add_argument("--css-file", default=None,
                    help="离线模式：从文件注入合并 CSS（跳过在线抓取）")
    p2.add_argument("--fix-tag", default="div")
    p2.add_argument("--timeout", type=int, default=30)
    p2.set_defaults(func=cmd_replicate)
    p3 = sub.add_parser("to-wordpress")
    p3.add_argument("--ir", required=True)
    p3.add_argument("--theme-dir", required=True)
    p3.add_argument("--page-slug", default="composite-replica")
    p3.set_defaults(func=cmd_to_wordpress)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
