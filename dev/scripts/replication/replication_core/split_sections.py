"""split_sections — 结构切分：锚点切分 / 修边 / 平衡闭合 / 开标签补全。"""
import re
import os


def fix_opening_tag(html, tag="div"):
    """切分起点若截断了开标签（形如 'id=… class=…>' 开头），补回 <tag。"""
    m = re.match(rf"^(id=\"[^\"]*\" class=\"[^\"]*\">)", html)
    if m:
        return "<" + tag + " " + html
    return html


def strip_scripts(html):
    return re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S) \
        .replace(re.__class__ and "" or "", "")


def strip_all_scripts(html):
    """剥离 <script>（含裸 script 标签）——预览工具/水合 JS 不复刻。"""
    t = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)
    t = re.sub(r"<script\b[^>]*/>", "", t)
    return t


def balance_divs(html):
    """div 开闭平衡闭合（修边截断后调用）。"""
    opens = len(re.findall(r"<div\b", html))
    closes = len(re.findall(r"</div>", html))
    if opens > closes:
        html += "</div>" * (opens - closes)
    return html


def trim_after(html, marker):
    """截掉 marker（含）之后的全部内容（页尾脚本/预览工具等杂物）。"""
    i = html.find(marker)
    return html[:i] if i > 0 else html


def cut_before(html, marker):
    """截掉 marker（含）之前的全部内容。"""
    i = html.find(marker)
    return html[i:] if i > 0 else html


def split_sections(html, anchor_re=r'id="internal-section-\d+"[^>]*>'
                   r'<div class="contents" data-lp-section="([a-z0-9-]+)"',
                   fix_tag="div"):
    """按锚点正则切分组件片段。

    返回 [{order, type, html}]；html 为锚点起点 → 下一锚点前（原样，未修边）。
    实战依据：lovart.ai composite-page-all 33 组件按此锚点切分全部成功。
    """
    marks = [(m.start(), m.group(1))
             for m in re.finditer(anchor_re, html)]
    out = []
    for i, (pos, typ) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(html)
        out.append({"order": i, "type": typ, "html": html[pos:end]})
    return out


def trim_fragment(html, tail_markers=("<footer", "<script"), head_markers=(),
                  strip_scripts=True, balance=True, fix_tag=None):
    """单片段修边：掐头（head_markers 首现处）去尾（tail_markers 首现处）
    + 剥脚本 + div 平衡 + 开标签补全。"""
    for mk in head_markers:
        i = html.find(mk)
        if i > 0:
            html = html[i:]
            break
    for mk in tail_markers:
        i = html.find(mk)
        if i > 0:
            html = html[:i]
            break
    if strip_scripts:
        html = strip_all_scripts(html)
    if balance:
        html = balance_divs(html)
    if fix_tag:
        html = fix_opening_tag(html, fix_tag)
    return html


def remove_element(html, tag_open):
    """删除指定开标签的整个元素（非贪婪到对应闭标签；该元素内不应嵌套同名）。

    实战依据：composite-page-all 的 VARIANTS 预览面板 = <aside class="...fixed...">，
    需整体移除而非截断（截断会误伤宿主 section 的锚点与内容）。
    """
    pat = re.escape(tag_open) + r"[^>]*>.*?</" + tag_open[1:] + r">"
    return re.sub(pat, "", html, flags=re.S)


def strip_trailing_unclosed(html, max_iter=12):
    """移除尾部悬空的开标签（如 remove_element 后残留的空父容器 <div>）。

    悬空开标签会把后续内容（footer 等）吞进该容器——布局破坏风险。
    """
    pat = re.compile(r"<div(?:\s[^>]*)?>\s*$")
    for _ in range(max_iter):
        t2 = pat.sub("", html)
        if t2 == html:
            break
        html = t2
    return html


def strip_trailing_orphan_closes(html, tag="div", max_iter=12):
    """移除尾部多余的闭标签（remove_element 后父容器闭合残留）。

    多余闭合浏览器会忽略（无布局风险），但为保持与手工基准字节级一致而清理。
    """
    close = "</%s>" % tag
    pat = re.compile(r"\s*" + re.escape(close) + r"\s*$")
    opens = len(re.findall(r"<%s\b" % tag, html))
    closes = len(re.findall(r"</%s>" % tag, html))
    n = closes - opens
    for _ in range(min(n, max_iter)):
        if not pat.search(html):
            break
        html = pat.sub("", html)
    return html


def remove_empty_tail_container(html, max_iter=6):
    """remove_element 后若尾部残留空容器（<div...></div> 紧邻对），一并移除。

    实战：composite cta-default 移除 VARIANTS aside 后，其空父容器残留
    （11 字节差异，空 div 虽无布局影响，但保持产物与手工基准字节一致）。
    """
    pat = re.compile(r"<div(?:\s[^>]*)?>\s*</div>\s*$")
    for _ in range(max_iter):
        t2 = pat.sub("", html)
        if t2 == html:
            break
        html = t2
    return html
