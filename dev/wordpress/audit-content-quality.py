#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit-content-quality.py — blogs.lovart.ai Blog + 落地页内容质量/模板化审计。

范围：全站 published pages + posts（REST 公开拉取，8 线程）。
审计项：
  A. 薄内容：正文词数（页面 <300 / 文章 <800 标 WARN）
  B. Slop：BANNED_EN 短语命中（anti-slop 规则）
  C. 占位/模板残留：IMAGE PLACEHOLDER / [TODO] / lorem ipsum 等
  D. 跨页重复度（模板化）：5 词 shingle 倒排索引，同组页面相似度
  E. 坏图：content 内图片 URL 采样 HEAD 检查
分组：replica（18 复刻页）/ lpagery（种子模板生成落地页）/ blog（posts）/ other
输出：--out JSON + --md Markdown 摘要（纯文字段落，无表格）
"""
import argparse
import json
import re
import sys
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

BASE = "https://blogs.lovart.ai"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")

BANNED_EN = [
    (r"\bunlock(?:ing|ed)?\b", "unlock"),
    (r"\brevolutionize\b", "revolutionize"),
    (r"\bgame[- ]?changer\b", "game-changer"),
    (r"\bseamless(?:ly)?\b", "seamless(ly)"),
    (r"\bdelve[ds]?\b", "delve"),
    (r"\bunprecedented\b", "unprecedented"),
    (r"\bin today'?s fast[- ]paced\b", "in today's fast-paced"),
    (r"\bcutting[- ]edge\b", "cutting-edge"),
    (r"\bAI[- ]powered platform\b", "AI-powered platform"),
    (r"\btransform(?:s|ing|ed)? your (?:workflow|business)\b", "transform your workflow/business"),
    (r"\btapestry\b", "tapestry"),
    (r"\bbeacon\b", "beacon"),
    (r"\brealm\b", "realm"),
    (r"\bstands as\b", "stands as"),
    (r"\bunderscores?\b", "underscores"),
    (r"\bvibrant\b", "vibrant"),
    (r"\belevate\b", "elevate"),
]
PLACEHOLDER_PATTERNS = [
    (r"IMAGE PLACEHOLDER", "IMAGE PLACEHOLDER"),
    (r"\[TODO\]", "[TODO]"),
    (r"\[TBD\]", "[TBD]"),
    (r"\[待补充\]", "[待补充]"),
    (r"lorem ipsum", "lorem ipsum"),
    (r"\{[a-z_0-9]+\}", "LPagery 占位符未替换"),
    (r"\(section_\w+\)", "(section_xx)"),
]
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
IMG_RE = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)
LINK_RE = re.compile(r"<a[^>]+href=[\"']([^\"']+)[\"']", re.I)


def get_json(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def get_html(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def paged(fmt):
    out, pageno = [], 1
    while True:
        try:
            batch = get_json(fmt.replace("{P}", str(pageno)))
        except Exception as e:
            if "404" in str(e):
                return out
            raise
        out.extend(batch)
        if len(batch) < 100:
            return out
        pageno += 1


def strip_html(html):
    html = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", html)
    text = TAG_RE.sub(" ", html)
    text = text.replace("&amp;", "&").replace("&#8217;", "'").replace("&nbsp;", " ")
    text = re.sub(r"&#\d+;", " ", text)
    return WS_RE.sub(" ", text).strip()


def word_count(text):
    # 拉丁词 + CJK 单字计数
    latin = len(re.findall(r"[A-Za-z0-9']+", text))
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    return latin + cjk


def shingles(text, k=5, cap=3000):
    words = re.findall(r"[a-z0-9]+", text.lower())
    if len(words) < k:
        return set()
    hs = set()
    for i in range(0, len(words) - k + 1):
        hs.add(hash(" ".join(words[i:i + k])))
        if len(hs) >= cap:
            break
    return hs


def classify(p, is_post):
    link = p.get("link", "")
    slug = p.get("slug", "")
    tmpl = p.get("template") or ""
    if not is_post and (slug.startswith("replica-") or slug == "composite-replica-all"):
        return "replica"
    if "lpagery" in (p.get("yoast_head_json", {}) or {}).get("title", "").lower():
        return "lpagery"
    if is_post:
        return "blog"
    return "other"


def fetch_one(p, is_post):
    pid, slug = p["id"], p.get("slug", "")
    link = p.get("link", "")
    try:
        html = p.get("content", {}).get("rendered", "") or ""
        text = strip_html(html)
        wc = word_count(text)
        slop_hits = defaultdict(int)
        for pat, name in BANNED_EN:
            n = len(re.findall(pat, text, re.IGNORECASE))
            if n:
                slop_hits[name] += n
        ph_hits = []
        for pat, name in PLACEHOLDER_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                ph_hits.append(name)
        h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.I | re.S)
        imgs = list(dict.fromkeys(IMG_RE.findall(html)))
        links = list(dict.fromkeys(LINK_RE.findall(html)))
        return {
            "id": pid, "slug": slug, "link": link,
            "title": (p.get("title") or {}).get("rendered", ""),
            "type": "post" if is_post else "page",
            "template": p.get("template") or "default",
            "date": p.get("date"),
            "words": wc, "h2": len(h2s),
            "slop": dict(slop_hits), "placeholders": ph_hits,
            "n_imgs": len(imgs), "n_links": len(links),
            "_text": text[:20000],
            "_imgs": imgs[:40],
        }
    except Exception as e:
        return {"id": pid, "slug": slug, "link": link, "error": str(e)}


def dup_index(pages):
    """shingle 倒排 → 组内相似对。boilerplate（出现在 >60 页）排除。"""
    inv = defaultdict(set)
    valid = [p for p in pages if not p.get("error") and p["words"] > 120]
    for idx, p in enumerate(valid):
        for h in shingles(p["_text"]):
            inv[h].add(idx)
    pair = defaultdict(int)
    for h, owners in inv.items():
        if len(owners) < 2 or len(owners) > 60:
            continue
        owners = sorted(owners)
        for i in range(len(owners)):
            for j in range(i + 1, len(owners)):
                pair[(owners[i], owners[j])] += 1
    out = []
    for (i, j), shared in pair.items():
        a, b = valid[i], valid[j]
        denom = min(len(shingles(a["_text"])), len(shingles(b["_text"]))) or 1
        sim = shared / denom
        if sim >= 0.55:
            out.append({"a": [a["type"], a["slug"]], "b": [b["type"], b["slug"]],
                        "sim": round(sim, 2)})
    return out


def check_imgs(items, sample=300, workers=8):
    urls = []
    for p in items:
        if p.get("error"):
            continue
        urls.extend(p["_imgs"])
    urls = list(dict.fromkeys(urls))
    if len(urls) > sample:
        # 内链域全查，外域采样
        internal = [u for u in urls if "lovart" in u or u.startswith("/")]
        external = [u for u in urls if u not in internal]
        urls = internal + external[:sample - len(internal)]

    def head(u):
        if u.startswith("/"):
            u = BASE + u
        if not u.startswith("http"):
            return (u, "skip")
        req = urllib.request.Request(u, headers={"User-Agent": UA}, method="HEAD")
        try:
            r = urllib.request.urlopen(req, timeout=15)
            return (u, r.status)
        except Exception as e:
            code = getattr(e, "code", None)
            if code is None:
                return (u, "ERR")
            return (u, code)

    with ThreadPoolExecutor(workers) as ex:
        res = list(ex.map(head, urls))
    return {"checked": len(res), "bad": [(u, s) for u, s in res if s not in (200, 301, 302, 405, "skip")][:50]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/content-quality.json")
    ap.add_argument("--md", default="/tmp/content-quality.md")
    ap.add_argument("--skip-imgs", action="store_true")
    args = ap.parse_args()

    print("listing pages/posts ...", file=sys.stderr)
    pages = paged(BASE + "/wp-json/wp/v2/pages?per_page=100&page={P}"
                  "&_fields=id,slug,link,title,template,date,content")
    posts = paged(BASE + "/wp-json/wp/v2/posts?per_page=100&page={P}"
                  "&_fields=id,slug,link,title,date,content")
    print(f"pages={len(pages)} posts={len(posts)}", file=sys.stderr)

    items = []
    with ThreadPoolExecutor(8) as ex:
        futs = [(p, True) for p in pages] + [(p, False) for p in posts]
        for r in ex.map(lambda t: fetch_one(t[0], t[1]), futs):
            items.append(r)
    for it in items:
        it["group"] = classify(it, it["type"] == "page")

    # 结构阈值
    for it in items:
        if it.get("error"):
            continue
        warns = []
        g = it["group"]
        floor = 800 if g == "blog" else 300
        if it["words"] < floor:
            warns.append(f"thin:{it['words']}<{floor}")
        if g == "blog" and it["h2"] < 3:
            warns.append(f"h2:{it['h2']}<3")
        if it["slop"]:
            top = sorted(it["slop"].items(), key=lambda x: -x[1])[:3]
            warns.append("slop:" + ",".join(f"{k}x{n}" for k, n in top))
        for ph in it["placeholders"]:
            warns.append("ph:" + ph)
        it["issues"] = warns

    print("computing duplication ...", file=sys.stderr)
    dup = dup_index(items)

    print("checking images ...", file=sys.stderr)
    imgs = {} if args.skip_imgs else check_imgs(items)

    report = {
        "base": BASE,
        "total": len(items),
        "by_group": {},
        "items": [{k: v for k, v in it.items() if not k.startswith("_")} for it in items],
        "duplicates": dup,
        "images": imgs,
    }
    for it in items:
        g = it.get("group", "?")
        s = report["by_group"].setdefault(g, {"n": 0, "issue": 0, "thin": 0, "slop": 0, "ph": 0, "words_avg": 0, "_wsum": 0})
        s["n"] += 1
        if it.get("error"):
            continue
        s["_wsum"] += it["words"]
        if it["issues"]:
            s["issue"] += 1
        for w in it["issues"]:
            if w.startswith("thin:"):
                s["thin"] += 1
            elif w.startswith("slop:"):
                s["slop"] += 1
            elif w.startswith("ph:"):
                s["ph"] += 1
    for g, s in report["by_group"].items():
        s["words_avg"] = s.pop("_wsum") // max(s["n"], 1)

    json.dump(report, open(args.out, "w"), ensure_ascii=False, indent=1)
    print("json ->", args.out, file=sys.stderr)

    # Markdown 摘要（纯文字，无表格）
    L = [f"# blogs.lovart.ai 内容质量/模板化审计", ""]
    L.append(f"共 {report['total']} 页。")
    for g, s in report["by_group"].items():
        L.append(f"- {g}: {s['n']} 页，平均词数 {s['words_avg']}，问题页 {s['issue']}（薄内容 {s['thin']} / slop {s['slop']} / 占位残留 {s['ph']}）")
    L.append("")
    L.append(f"## 跨页高度重复（sim>=0.55，{len(dup)} 对）")
    for d in dup[:40]:
        L.append(f"- {d['a'][0]}:{d['a'][1]} ≈ {d['b'][0]}:{d['b'][1]}（相似度 {d['sim']}）")
    L.append("")
    if imgs:
        L.append(f"## 图片抽查 {imgs['checked']} 个，异常 {len(imgs['bad'])} 个")
        for u, s in imgs["bad"][:20]:
            L.append(f"- {s} {u}")
    L.append("")
    L.append("## 问题页明细（每组前 25）")
    for g in ["replica", "lpagery", "blog", "other"]:
        rows = [it for it in items if it.get("group") == g and it.get("issues")]
        if not rows:
            continue
        L.append(f"### {g}（{len(rows)} 页有问题）")
        for it in rows[:25]:
            L.append(f"- {it['slug']}（{it['words']} 词）: " + "; ".join(it["issues"]))
        if len(rows) > 25:
            L.append(f"- ... 其余 {len(rows) - 25} 页见 JSON")
    open(args.md, "w").write("\n".join(L))
    print("md ->", args.md, file=sys.stderr)


if __name__ == "__main__":
    main()