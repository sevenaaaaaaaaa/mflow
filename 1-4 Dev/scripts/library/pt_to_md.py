#!/usr/bin/env python3
"""pt_to_md.py — Sanity Portable Text → Markdown（纯标准库）。

支持：block 样式（h1-h6/blockquote）、span marks（strong/em/code/underline/strike）、
链接（markDefs.link）、列表（bullet/number）、图片、代码块、表格（table 类型尽力而为）。
用途：把 Sanity 内容镜像成可读可搜的本地 Markdown（MFlow 内容库）。
"""
import json
import re


def _span_text(sp, markdefs):
    t = sp.get("text", "")
    marks = sp.get("marks") or []
    for m in marks:
        if m in ("strong", "b"):
            t = f"**{t}**"
        elif m in ("em", "i"):
            t = f"*{t}*"
        elif m == "code":
            t = f"`{t}`"
        elif m in ("underline", "strike-through"):
            t = t
        else:
            md = markdefs.get(m)
            if md and md.get("_type") == "link" and md.get("href"):
                t = f"[{t}]({md['href']})"
    return t


def _block_md(b):
    style = b.get("style", "normal")
    markdefs = {m.get("_key"): m for m in (b.get("markDefs") or []) if isinstance(m, dict)}
    text = "".join(_span_text(sp, markdefs) for sp in (b.get("children") or []))
    if style in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return f"{'#' * int(style[1])} {text}"
    if style == "blockquote":
        return "> " + text
    li = b.get("listItem")
    if li == "bullet":
        return f"- {text}"
    if li == "number":
        return f"1. {text}"
    return text


def portable_text_to_md(body):
    """body: list[dict] | JSON 字符串。返回 markdown 文本。"""
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            return body
    if not isinstance(body, list):
        return ""
    out = []
    for b in body:
        if not isinstance(b, dict):
            continue
        t = b.get("_type")
        if t == "block":
            out.append(_block_md(b))
        elif t == "image":
            alt = b.get("alt") or ""
            out.append(f"![{alt}]()")
        elif t == "code":
            lang = b.get("language") or ""
            out.append(f"```{lang}\n{b.get('code','')}\n```")
        elif t in ("table", "tableBlock"):
            rows = b.get("rows") or []
            for r in rows:
                cells = r.get("cells") if isinstance(r, dict) else r
                if isinstance(cells, list):
                    out.append("| " + " | ".join(str(c) for c in cells) + " |")
            if rows:
                out.append("")
        else:
            # 未知类型：尽力提取 text/caption
            if b.get("text"):
                out.append(str(b["text"]))
        out.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


# ── compositePage.bodyJson：从版块 JSON 里提取可读文本 ──
TEXT_KEYS = ("title", "heading", "subtitle", "subheading", "description", "desc", "text",
             "body", "label", "badge", "caption", "question", "answer", "name", "value",
             "summary", "quote", "faq", "cta", "buttonText")
SKIP_KEYS = ("href", "url", "src", "image", "icon", "color", "id", "_type", "_key", "style",
             "variant", "layout", "tag", "type")


def bodyjson_to_md(body_json):
    """compositePage 的 bodyJson（版块数组）→ 可读 markdown（标题/文案/按钮/问答）。"""
    if isinstance(body_json, str):
        try:
            body_json = json.loads(body_json)
        except Exception:
            return str(body_json)[:2000]
    lines = []

    def walk(node, depth=0):
        pad = "  " * min(depth, 4)
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    walk(v, depth + 1)
                elif isinstance(v, str) and v.strip() and k not in SKIP_KEYS:
                    if k in ("title", "heading", "h1", "h2"):
                        lines.append(f"\n{'#' * min(depth + 2, 6)} {v.strip()}")
                    elif k in ("question", "q"):
                        lines.append(f"\n**Q：{v.strip()}**")
                    elif k in ("answer", "a"):
                        lines.append(f"A：{v.strip()}")
                    elif k in TEXT_KEYS:
                        lines.append(f"{pad}{v.strip()}")
        elif isinstance(node, list):
            for it in node:
                if isinstance(it, str):
                    if it.strip():
                        lines.append(f"{pad}- {it.strip()}")
                else:
                    walk(it, depth + 1)

    walk(body_json, 1)
    text = "\n".join(l for l in lines if l.strip())
    return re.sub(r"\n{3,}", "\n\n", text).strip()
