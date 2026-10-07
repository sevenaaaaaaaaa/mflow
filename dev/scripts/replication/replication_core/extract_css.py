"""extract_css — 设计资产提取：编译 CSS 合并 / tokens / 字体栈 / 断点 / URL 绝对化。"""
import re
import urllib.request
from . import DEFAULT_UA


def _fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")


def absolutize(text, base_url):
    """相对资源引用 → 绝对 URL（src/href/poster/srcset/url()）。"""
    base = base_url.rstrip("/")
    text = re.sub(r'(src|href|poster|srcset)="(/(?!/))', rf'\1="{base}/', text)
    text = re.sub(r"(src|href|poster|srcset)='(/(?!/))", rf"\1='{base}/", text)
    text = re.sub(r'url\((?!["\']?https?:|data:)', f"url({base}/", text)
    return text


def extract_stylesheets(html, base_url, max_files=8, timeout=30):
    """抓取页面全部 <link stylesheet> 并合并；资源 URL 绝对化。

    实战依据：lovart.ai 4 个编译 CSS 合并 364KB 后，33 组件渲染与主站一致——
    CSS 全量直带是 1:1 复刻的基石（同 HTML 同 CSS → 同视觉）。
    """
    links = []
    seen = set()
    for m in re.finditer(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html):
        href = m.group(1)
        url = href if href.startswith("http") else base_url.rstrip("/") + href
        if url not in seen:
            seen.add(url)
            links.append(url)
    merged, files = [], []
    for url in links[:max_files]:
        try:
            css = _fetch(url, timeout)
            css = re.sub(r'url\((["\']?)/(?!/)', rf'url(\1{base_url}/', css)
            css = css.replace('url("./', f'url("{base_url}/')
            merged.append(css)
            files.append({"url": url, "bytes": len(css)})
        except Exception as e:
            files.append({"url": url, "error": repr(e)[:120]})
    return {"css": "\n".join(merged), "files": files}


def extract_tokens(css):
    """:root CSS 变量全量提取（实战：lovart.ai 381 项）。"""
    tokens = {}
    for block in re.findall(r":root[^{]*\{([^}]+)\}", css):
        for k, v in re.findall(r"(--[a-zA-Z0-9-]+)\s*:\s*([^;]+)", block):
            tokens.setdefault(k, v.strip())
    return tokens


def extract_breakpoints(css):
    """媒体查询断点清单（响应式适配的证明依据）。"""
    bps = {}
    for m in re.finditer(r"@media\s*\([^)]*width[^)]*\)", css):
        key = re.search(r"width\s*[:>]=?\s*([\d.]+(?:px|rem))", m.group(0))
        k = key.group(1) if key else m.group(0)[:40]
        bps[k] = bps.get(k, 0) + 1
    return bps


def extract_fonts(css):
    """字体家族栈。"""
    fams = {}
    for k, v in re.findall(r"(--[a-zA-Z0-9-]*font[a-zA-Z0-9-]*)\s*:\s*([^;]+)", css):
        fams.setdefault(k, v.strip())
    return fams


def design_assets(html, base_url, timeout=30):
    """一站式：合并 CSS + tokens + 断点 + 字体（环节 2 的对外接口）。"""
    ex = extract_stylesheets(html, base_url, timeout=timeout)
    tokens = extract_tokens(ex["css"])
    return {
        "css": ex["css"],
        "cssFiles": ex["files"],
        "tokens": tokens,
        "breakpoints": extract_breakpoints(ex["css"]),
        "fonts": extract_fonts(ex["css"]),
    }
