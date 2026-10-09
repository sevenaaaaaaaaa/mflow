#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-elementor-pages.py — 把 lr-assets/pages/*.html 转成 Elementor 原生文档并迁移。

机制依据（WP/Elementor 渲染原理）：
  - Elementor 前端唯一事实来源 = _elementor_data（post meta）；
    _elementor_edit_mode=builder 时 the_content filter 渲染 Elementor 数据而非 post_content。
  - 每页拆成 N 个 section chunk，每 chunk = 一个 Elementor container + HTML 微件。
  - 作用域环境保真：chunk 包裹层复刻 .lr dark + 祖先环境类（scope 字体变量、
    main 的 bg/font 等，剔除 min-h-screen 这类逐 chunk 复刻会破坏布局的类）。
    环境类必须放在 .lr 的后代 div 上（作用域化 CSS 全是 .lr 后代选择器，
    变量类放包裹层自身不生效）。
  - chunk 只含平衡子树：同层 gap 内容并入相邻 chunk 的 pre/post（零丢失），
    跨层路径标签（main/scope 等开闭标签）不进 chunk，由 env 类承载。
  - 内容经 nownexts.com 服务器间传输写入（lr_elem_import），不碰 Aliyun WAF。
  - 页面模板切 elementor_header_footer：主题页头页尾保留（Hello Elementor）+ 全宽内容区。

sticky 页头：chunk 顶层是 <header> 站头的，用 Elementor Pro 容器 Sticky:Top
（拆分后原 position:sticky 只能在 chunk 容器内生效，会失效）。
嵌套在 section 内的 header 不处理——原页面它就在 section 内 sticky，行为天然一致。

用法（在 MFlow 服务器上）：
  python3 build-elementor-pages.py --stats
  python3 build-elementor-pages.py --only replica-homepage          # dry-run
  python3 build-elementor-pages.py --only replica-homepage --apply # 导入+切模板+验证
  python3 build-elementor-pages.py --all --apply
"""
import argparse
import http.cookiejar
import io
import json
import os
import random
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://blogs.lovart.ai"
PAGES_DIR = "/www/wwwroot/nownexts_com/lr-assets/pages"
ELEM_DIR = "/www/wwwroot/nownexts_com/lr-assets/elem"
ELEM_URL = "https://nownexts.com/lr-assets/elem"
SECRET = "lrb-2026-x7k9"
TPL = "elementor_header_footer"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")
ELEMENTOR_VERSION = "3.35.7"
ENV_CLASS_BLACKLIST = {"min-h-screen"}
SMALL_CHUNK_BYTES = 500
MAX_DESCEND = 5
DESCEND_RATIO = 0.75

TOKEN_RE = re.compile(
    r'<(/?)([a-zA-Z][a-zA-Z0-9:_-]*)((?:"[^"]*"|\'[^\']*\'|[^>])*?)(/?)>')
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr", "path", "circle", "rect",
        "line", "polyline", "polygon", "ellipse", "stop", "use", "animate",
        "animatetransform", "feGaussianBlur", "feOffset", "feMerge",
        "feMergeNode", "mask", "symbol", "clipPath"}


# ---------- HTML 结构化拆分 ----------

def tokenize(html):
    toks = []
    for m in TOKEN_RE.finditer(html):
        toks.append({"start": m.start(), "end": m.end(),
                     "close": m.group(1) == "/",
                     "tag": m.group(2).lower(),
                     "attrs": m.group(3) or "",
                     "selfclose": m.group(4) == "/"})
    return toks


def cls_of(attrs):
    m = re.search(r'class="([^"]*)"', attrs)
    if m:
        return m.group(1)
    m = re.search(r"class='([^']*)'", attrs)
    return m.group(1) if m else ""


def find_close(toks, open_idx):
    depth = 0
    for i in range(open_idx, len(toks)):
        t = toks[i]
        if t["tag"] in VOID or t["selfclose"]:
            continue
        if t["close"]:
            depth -= 1
            if depth == 0:
                return i
        else:
            depth += 1
    return None


def children_spans(toks, open_idx, close_idx):
    """元素的直接子元素 [(start, end, open_token_idx), ...]"""
    spans, depth, cur, cur_i = [], 0, None, None
    for i in range(open_idx + 1, close_idx):
        t = toks[i]
        if t["tag"] in VOID or t["selfclose"]:
            if depth == 0:
                spans.append((t["start"], t["end"], i))
            continue
        if not t["close"]:
            if depth == 0:
                cur, cur_i = t["start"], i
            depth += 1
        else:
            depth -= 1
            if depth == 0 and cur is not None:
                spans.append((cur, t["end"], cur_i))
                cur = None
    return spans


def ancestor_chain(toks, open_idx, target_idx):
    """从 open_idx 元素到 target_idx 元素（不含两端）的祖先路径 [(tag, cls), ...]"""
    chain, depth = [], 0
    for i in range(open_idx + 1, target_idx):
        t = toks[i]
        if t["tag"] in VOID or t["selfclose"]:
            continue
        if not t["close"]:
            if depth == 0:
                chain.append((t["tag"], cls_of(t["attrs"])))
            depth += 1
        else:
            if depth == 1:
                chain.pop()
            depth -= 1
    return chain


def env_str_of(chain):
    """祖先类列表 → 环境层 class 字符串（过滤黑名单）"""
    out = []
    for _, c in chain:
        kept = [x for x in c.split() if x not in ENV_CLASS_BLACKLIST]
        if kept:
            out.append(" ".join(kept))
    return " ".join(out)


def visible_text_len(seg):
    return len(re.sub(r"<[^>]+>", "", seg).strip())


def is_sticky_chunk(src):
    """chunk 顶层存在 <header> 站头 → 该 chunk 需要容器 Sticky。"""
    toks = tokenize(src)
    depth = 0
    for t in toks:
        if t["tag"] in VOID or t["selfclose"]:
            continue
        if not t["close"]:
            if depth == 0 and t["tag"] == "header":
                seg = src[t["start"]:t["start"] + 400]
                return "lovart-site-header" in seg or "sticky" in seg
            depth += 1
        else:
            depth -= 1
    return False


def _collect_chunks(toks, open_idx, close_idx, html, env_parts, depth):
    """递归收集平衡 chunk 子树 [(start, end), ...]（文档序）。

    下钻规则：最大非页头子元素占比 > 75% 且是 div/main（容器型）且无
    data-lp-section 时深入一层拆其子元素（下钻成功才把该层类记入 env_parts）。
    """
    kids = children_spans(toks, open_idx, close_idx)
    sub = []
    for k in kids:
        s, e, oi = k
        if (e - s) >= SMALL_CHUNK_BYTES or is_sticky_chunk(html[s:e]):
            sub.append(k)
    cand = [k for k in sub if not is_sticky_chunk(html[k[0]:k[1]])]
    if depth < MAX_DESCEND and cand:
        large = max(cand, key=lambda k: k[1] - k[0])
        total = sum(k[1] - k[0] for k in cand)
        lo = large[2]
        if (toks[lo]["tag"] in ("div", "main")
                and "data-lp-section" not in toks[lo]["attrs"]
                and (large[1] - large[0]) > DESCEND_RATIO * total):
            lc = find_close(toks, lo)
            if lc is not None:
                trial_env = list(env_parts)
                trial_env.append((toks[lo]["tag"], cls_of(toks[lo]["attrs"])))
                inner = _collect_chunks(toks, lo, lc, html, trial_env, depth + 1)
                if len(inner) >= 2:
                    env_parts[:] = trial_env
                    out = []
                    for k in sub:
                        if k[0] == large[0]:
                            out.extend(inner)
                        else:
                            out.append((k[0], k[1]))
                    return out
    return [(k[0], k[1]) for k in sub]


def balanced_prefix_end(html, toks, gap_start, gap_end):
    """gap 前缀里的平衡内容末尾（遇未闭合的开标签即停，其后属路径层）。"""
    depth = 0
    end = gap_start
    for t in toks:
        if t["start"] >= gap_end:
            break
        if t["start"] < gap_start:
            continue
        if t["tag"] in VOID or t["selfclose"]:
            if depth == 0:
                end = t["end"]
            continue
        if not t["close"]:
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = t["end"]
            if depth < 0:
                break
    return end


def balanced_suffix_start(html, toks, gap_start, gap_end):
    """gap 后缀里的平衡内容起点（跳过路径层闭标签之后的部分）。"""
    depth = 0
    last_neg_end = gap_start
    for t in toks:
        if t["start"] < gap_start or t["start"] >= gap_end:
            continue
        if t["tag"] in VOID or t["selfclose"]:
            continue
        if not t["close"]:
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                last_neg_end = t["end"]
                depth = 0
    return last_neg_end


def chunk_label(src, idx):
    m = re.search(r'data-lp-section="([^"]+)"', src)
    name = m.group(1) if m else ""
    return ("Section %02d%s" % (idx + 1, (" - " + name) if name else ""))


def split_page(html):
    """返回 (wrapper_classes, env_classes, chunks)

    chunks = [{"pre","html","post","sticky","label"}]，pre/post 为同层并入的平衡内容，
    html 为平衡子树——拼起来零内容丢失；路径层（main/scope 等开闭标签）不进 chunk。
    """
    toks = tokenize(html)
    w = None
    for i, t in enumerate(toks):
        if t["tag"] == "div" and not t["close"] and "lr" in cls_of(t["attrs"]).split():
            w = i
            break
    if w is None:
        raise RuntimeError("找不到 .lr 包裹层")
    wc = find_close(toks, w)
    wrapper_cls = cls_of(toks[w]["attrs"])
    inner_start, inner_end = toks[w]["end"], toks[wc]["start"]

    marker_idx = [i for i, t in enumerate(toks)
                  if w < i < wc and not t["close"] and "internal-section-" in t["attrs"]]

    if marker_idx:
        # 模式 A：internal-section 标记（6 模块页 + composite）
        ref = marker_idx[0]
        env = env_str_of(ancestor_chain(toks, w, ref))
        spans = []
        for mi in marker_idx:
            cl = find_close(toks, mi)
            if cl is not None:
                spans.append((toks[mi]["start"], toks[cl]["end"]))
    else:
        # 模式 B：递归下钻（homepage 的 main>scope>overflow 容器链、solution 的 scope 层）
        env_parts = []
        spans = _collect_chunks(toks, w, wc, html, env_parts, 0)
        env = env_str_of(env_parts)

    if not spans:
        spans = [(inner_start, inner_end)]
        env = ""

    chunks = []
    # 前导平衡内容 → 首 chunk 的 pre
    first_start = spans[0][0]
    pre_end = balanced_prefix_end(html, toks, inner_start, first_start)
    pre = html[inner_start:pre_end] if pre_end > inner_start else ""
    lost_head = html[pre_end:first_start]

    for i, (s, e) in enumerate(spans):
        src = html[s:e]
        chunks.append({"pre": pre if i == 0 else "",
                       "html": src,
                       "post": "",
                       "sticky": is_sticky_chunk(src)})
        pre = ""
        if i + 1 < len(spans):
            nxt = spans[i + 1][0]
            # 同层 gap：平衡尾部并入当前 chunk 的 post；其余（路径闭标签）丢弃
            ss = balanced_suffix_start(html, toks, e, nxt)
            if ss > e:
                chunks[-1]["post"] = html[ss:nxt]

    # 尾部平衡内容 → 末 chunk 的 post
    last_end = spans[-1][1]
    ts = balanced_suffix_start(html, toks, last_end, inner_end)
    if ts > last_end:
        chunks[-1]["post"] += html[ts:inner_end]

    for i, c in enumerate(chunks):
        c["label"] = chunk_label(c["html"], i)
    return wrapper_cls, env, chunks


# ---------- Elementor 文档生成 ----------

def rid():
    return "".join(random.choice("0123456789abcdef") for _ in range(7))


ZERO_BOX = {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}


def wrap_chunk(wrapper_cls, env, pre, src, post):
    out = '<div class="%s">' % wrapper_cls
    if env:
        out += '<div class="%s">' % env
    out += (pre or "") + src + (post or "")
    if env:
        out += "</div>"
    return out + "</div>"


def build_document(html):
    wrapper_cls, env, chunks = split_page(html)
    data = []
    for i, c in enumerate(chunks):
        chunk_html = wrap_chunk(wrapper_cls, env, c["pre"], c["html"], c["post"])
        settings = {
            "content_width": "full",
            "gap": "no",
            "padding": dict(ZERO_BOX),
            "margin": dict(ZERO_BOX),
        }
        if c["sticky"]:
            settings.update({
                "sticky": "top",
                "sticky_on": ["desktop", "tablet", "mobile"],
                "sticky_offset": {"unit": "px", "size": 0, "sizes": []},
                "sticky_effects_offset": {"unit": "px", "size": 0, "sizes": []},
                "sticky_parent": "",
                "z_index": 150,
            })
        data.append({
            "id": rid(),
            "elType": "container",
            "settings": settings,
            "elements": [{
                "id": rid(),
                "elType": "widget",
                "widgetType": "html",
                "settings": {"html": chunk_html, "_title": c["label"]},
                "elements": [],
            }],
            "isInner": False,
        })
    info = {
        "wrapper": wrapper_cls,
        "env": env,
        "chunks": [{"label": c["label"], "sticky": c["sticky"],
                    "bytes": len(c["html"]) + len(c["pre"]) + len(c["post"])}
                   for c in chunks],
    }
    return {"version": ELEMENTOR_VERSION, "data": data}, info


# ---------- WP 通道 ----------

def build_opener():
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    op.addheaders = [("User-Agent", UA)]
    return op


def login(op):
    lines = io.open("/tmp/.wp-auth.tmp", encoding="utf-8").read().strip().split("\n")
    op.open(BASE + "/wp-login.php", timeout=60)
    data = urllib.parse.urlencode({
        "log": lines[0], "pwd": lines[-1], "wp-submit": "Log In",
        "redirect_to": BASE + "/wp-admin/", "testcookie": "1"}).encode()
    op.open(urllib.request.Request(BASE + "/wp-login.php", data=data), timeout=60)


def rest_nonce(op):
    return op.open(BASE + "/wp-admin/admin-ajax.php?action=rest-nonce",
                   timeout=60).read().decode().strip()


def get_json(op, url):
    return json.loads(op.open(url, timeout=120).read().decode())


def wp_pages(op):
    out, page = [], 1
    while True:
        batch = get_json(op, "%s/wp-json/wp/v2/pages?per_page=100&page=%d&_fields=id,slug,link,template"
                         % (BASE, page))
        out.extend(batch)
        if len(batch) < 100:
            return out
        page += 1


def admin_ajax(op, fields):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(BASE + "/wp-admin/admin-ajax.php", data=data)
    return json.loads(op.open(req, timeout=300).read().decode())


def set_template(op, nonce, pid, tpl):
    body = json.dumps({"template": tpl}).encode()
    req = urllib.request.Request(BASE + "/wp-json/wp/v2/pages/%d" % pid, data=body,
                                 method="POST",
                                 headers={"Content-Type": "application/json",
                                          "X-WP-Nonce": nonce})
    try:
        op.open(req, timeout=120)
        return True
    except urllib.error.HTTPError as e:
        print("  模板切换 HTTP %s" % e.code)
        return False


def verify_page(op, link):
    h = op.open(link, timeout=180).read().decode("utf-8", "replace")
    m = re.search(r"<script[^>]*lovart-replica\.js[^>]*>", h)
    checks = {
        "elem_type": 'data-elementor-type="wp-page"' in h,
        "widget_html": "elementor-widget-html" in h,
        "lr_wrapper": re.search(r'class="lr[ "]', h) is not None,
        "lr_body_class": "lr-replica-page" in h,
        "css_v2": "lovart-replica.css?v=2" in h,
        "js_tag": m.group(0) if m else "",
        "single_doctype": len(re.findall(r"<!doctype", h, re.I)) == 1,
        "containers": len(re.findall(r'class="[^"]*\be-con\b', h)),
        "bytes": len(h),
    }
    title = re.search(r"<title>(.*?)</title>", h, re.S)
    checks["title"] = title.group(1)[:80] if title else "?"
    return checks


# ---------- 主流程 ----------

def load_html(slug):
    path = os.path.join(PAGES_DIR, slug + ".html")
    if not os.path.exists(path):
        return None
    return io.open(path, encoding="utf-8").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true", help="只看拆分统计")
    ap.add_argument("--only", help="只处理该 slug")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true", help="导入 WP + 切模板 + 验证")
    args = ap.parse_args()

    slugs = []
    for f in sorted(os.listdir(PAGES_DIR)):
        if f.endswith(".html"):
            slugs.append(f[:-5])
    if args.only:
        slugs = [s for s in slugs if s == args.only]
    if not slugs:
        print("无可处理页面")
        return 1

    os.makedirs(ELEM_DIR, exist_ok=True)
    built = {}
    for slug in slugs:
        html = load_html(slug)
        if html is None:
            print("!! 缺文件 %s" % slug)
            continue
        doc, info = build_document(html)
        built[slug] = doc
        print("[%s] chunks=%d wrapper=%r env=%r" % (
            slug, len(info["chunks"]), info["wrapper"], info["env"][:60]))
        for c in info["chunks"]:
            print("   %-38s %7d bytes %s" % (c["label"], c["bytes"],
                                             "[STICKY]" if c["sticky"] else ""))
        out = os.path.join(ELEM_DIR, slug + ".json")
        with io.open(out, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False)
        print("   -> %s (%d bytes)" % (out, os.path.getsize(out)))
    if args.stats or not args.apply:
        print("dry-run 完成（未导入）")
        return 0

    op = build_opener()
    login(op)
    nonce = rest_nonce(op)
    pages = {p["slug"]: p for p in wp_pages(op)}
    ok = fail = 0
    for slug, doc in built.items():
        p = pages.get(slug)
        if not p:
            print("!! WP 无此 slug：%s" % slug)
            fail += 1
            continue
        url = "%s/%s.json" % (ELEM_URL, urllib.parse.quote(slug))
        r = admin_ajax(op, {"action": "lr_elem_import", "page_id": p["id"],
                            "url": url, "secret": SECRET})
        print("[%s] import: %s" % (slug, json.dumps(r)[:160]))
        if not (isinstance(r, dict) and r.get("success")):
            fail += 1
            continue
        ok_tpl = set_template(op, nonce, p["id"], TPL)
        checks = verify_page(op, p["link"])
        good = (checks["elem_type"] and checks["widget_html"] and checks["lr_wrapper"]
                and checks["css_v2"] and checks["single_doctype"] and checks["lr_body_class"])
        print("   tpl=%s elem_type=%s widget=%s lr=%s css=%s doctype=%s cons=%s"
              % (ok_tpl, checks["elem_type"], checks["widget_html"], checks["lr_wrapper"],
                 checks["css_v2"], checks["single_doctype"], checks["containers"]))
        print("   js_tag: %s" % checks["js_tag"][:120])
        print("   title: %s" % checks["title"])
        if good and ok_tpl:
            ok += 1
        else:
            fail += 1
    print("done: ok=%d fail=%d" % (ok, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())