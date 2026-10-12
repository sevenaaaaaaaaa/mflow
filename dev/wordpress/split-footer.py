#!/usr/bin/env python3
"""split-footer.py — 把被 cta-default 块吞进去的站点页脚拆出来。

背景
----
实测：5 个页面（comparison-hub / content-hub / product-launch / showcase-gallery /
tool-directory）的 `data-lp-section="cta-default"` 块有 23.5KB，里面除 CTA 本身还整个
塞着站点页脚（Company / Resources / Social 三栏共 17 个链接 + 版权 + 主题语言切换器）。
抓取时块边界切错了。**直接把这块换成 CTA 微件，这 5 页的页脚会整个消失。**

页脚本来就不该是页面内容的一部分 —— 它该由 Elementor Pro 的 Theme Builder
做成全站模板。本脚本负责两件事：

1. 把页脚从这些 cta 块里**用解析器**摘掉（不能用字符串切：实测朴素切割会留下
   3 个不闭合的 `<div>`），产出干净的 CTA-only 块；
2. 导出页脚的内容规格（`footer-spec.md` + `footer-raw.html`），
   供 Theme Builder 照着搭，不用人肉重抄 17 个链接。

用法
----
    python3 split-footer.py                 # 预演
    python3 split-footer.py --write         # 写出到 elem-migrated/（与迁移脚本同一目录，可链式）

⚠ 拆完页脚**不等于**这 5 页就能迁 CTA 了 —— 它们的 CTA 文案仍是别页的
（Shopify 文案出现在工具目录页上）且链接是死链 `#`。那是 C2，需要人工定文案。
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("✗ 需要 beautifulsoup4：pip install beautifulsoup4")

ROOT = Path(__file__).resolve().parent
MARKER = 'data-lp-section="cta-default"'


def walk_widgets(nodes, fn):
    for i, n in enumerate(nodes):
        if n.get("elType") == "widget":
            fn(n, nodes, i)
        walk_widgets(n.get("elements") or [], fn)


def strip_footer(html):
    """用解析器摘掉 <footer>，返回 (干净 html, 页脚 html)。

    必须走解析器：页脚前后的 div 嵌套是跨越 <footer> 的，
    按 `html[:index]` 切会留下不闭合标签（实测差 3 个 </div>）。
    """
    soup = BeautifulSoup(html, "html.parser")
    foot = soup.find("footer")
    if not foot:
        return html, ""
    foot_html = str(foot)
    foot.decompose()
    return str(soup), foot_html


def footer_spec(foot_html):
    """从页脚 HTML 抽出内容规格：三栏标题 + 链接 + 版权。"""
    soup = BeautifulSoup(foot_html, "html.parser")
    cols, cur = [], None
    for el in soup.find_all(["p", "a"]):
        if el.name == "p":
            txt = el.get_text(strip=True)
            # 栏标题是 font-mono uppercase 的小字
            if txt and "font-mono" in " ".join(el.get("class") or []):
                cur = {"title": txt, "links": []}
                cols.append(cur)
        elif el.name == "a" and cur is not None:
            href = el.get("href", "")
            txt = el.get_text(strip=True)
            if href and txt:
                cur["links"].append({"text": txt, "url": href})
    copyright = ""
    for p in soup.find_all("p"):
        t = p.get_text(strip=True)
        if t.startswith("©"):
            copyright = t
            break
    switchers = [b.get_text(strip=True) for b in soup.find_all("button")]
    switchers = [x for x in switchers if x]
    return {"columns": cols, "copyright": copyright, "switchers": switchers}


def write_spec(spec, foot_html):
    lines = [
        "# 站点页脚内容规格（给 Elementor Theme Builder 用）",
        "",
        "> 由 `split-footer.py` 从 5 个页面共用的 cta-default 块里抽出。",
        "> 这 5 页的页脚 HTML **完全一致**（md5 相同），所以一份全站模板即可。",
        "",
        "## 栏目与链接",
        "",
    ]
    for c in spec["columns"]:
        lines.append(f"### {c['title']}")
        lines.append("")
        lines.append("| 文案 | 链接 |")
        lines.append("|---|---|")
        for l in c["links"]:
            lines.append(f"| {l['text']} | `{l['url']}` |")
        lines.append("")
    lines += [
        "## 版权",
        "",
        f"`{spec['copyright']}`",
        "",
        "## 主题 / 语言切换器",
        "",
        f"页脚里还有两个切换器按钮：{' · '.join(spec['switchers']) or '（无）'}。",
        "它们的行为在 `replica.js` 的 `initTheme` / `initLang` 里。",
        "**Theme Builder 版页脚要不要保留它们，需要你定** —— 若不保留，",
        "迁移后记得把 `initTheme` / `initLang` 一并删掉。",
        "",
        "## 搭建建议",
        "",
        "用 Elementor **核心免费微件**即可，不要依赖插件包（页脚是全站件，依赖越少越好）：",
        "",
        "- 容器（flex 横向，3 列）",
        "- 每列：Heading（栏标题）+ Icon List（链接，关掉图标）",
        "- 底部：Text Editor（版权）",
        "",
        "搭好后在 Theme Builder 里把显示条件设为「整站」，",
        "然后跑 `split-footer.py --write` 把这 5 页块里的页脚摘掉。",
        "",
        "原始 HTML 见 `footer-raw.html`（作视觉比对基准）。",
        "",
    ]
    (ROOT / "footer-spec.md").write_text("\n".join(lines), encoding="utf-8")
    (ROOT / "footer-raw.html").write_text(foot_html, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="把站点页脚从 cta-default 块里拆出来")
    ap.add_argument("--src", default="elem-src")
    ap.add_argument("--out", default="elem-migrated")
    ap.add_argument("--write", action="store_true", help="真写文件（默认预演）")
    args = ap.parse_args()

    src, out = ROOT / args.src, ROOT / args.out
    hits, foot_seen, spec_written = [], {}, None

    for f in sorted(src.glob("*.json")):
        cur = out / f.name
        f_read = cur if (cur.exists() and cur != f) else f
        raw = json.loads(f_read.read_text(encoding="utf-8"))
        data = raw.get("data") if isinstance(raw, dict) else raw
        if not isinstance(data, list):
            continue
        changed = 0

        def visit(node, parent, i):
            nonlocal changed, spec_written
            if node.get("widgetType") != "html":
                return
            html = (node.get("settings") or {}).get("html", "")
            if MARKER not in html or "<footer" not in html:
                return
            clean, foot = strip_footer(html)
            if not foot:
                return
            node["settings"]["html"] = clean
            changed += 1
            md5 = hashlib.md5(foot.encode()).hexdigest()[:10]
            foot_seen[md5] = foot_seen.get(md5, 0) + 1
            if spec_written is None:
                spec_written = foot

        walk_widgets(data, visit)
        if changed:
            hits.append((f.name, len(json.dumps(data)) // 1000))
            if args.write:
                out.mkdir(parents=True, exist_ok=True)
                (out / f.name).write_text(
                    json.dumps(raw, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    print(f"\n页脚拆分{'' if args.write else '（预演，未写文件）'}")
    print("-" * 70)
    for name, kb in hits:
        print(f"  ✓ {name:<46} 页脚已摘除")
    print("-" * 70)
    print(f"命中 {len(hits)} 页 · 页脚版本数 {len(foot_seen)}"
          f"（{'全部一致，一份模板即可' if len(foot_seen) == 1 else '有差异，需逐个核对'}）")

    if spec_written:
        spec = footer_spec(spec_written)
        n = sum(len(c["links"]) for c in spec["columns"])
        write_spec(spec, spec_written)
        print(f"规格：footer-spec.md（{len(spec['columns'])} 栏 / {n} 个链接）"
              f" + footer-raw.html（{len(spec_written)} 字符，作视觉基准）")

    print("\n⚠ 拆完页脚≠这 5 页能迁 CTA 了：它们的 CTA 文案仍是别页的（Shopify 文案）"
          "\n  且链接是死链 #。先定文案，migrate-widgets 的 C2 闸才会放行。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
