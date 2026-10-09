#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit-main-content.py — www.lovart.ai 主站（Sanity production）内容质量审计。

范围：blog 全部语言 + compositePage（feature/tool/topic/scenario/solution）全部语言。
审计维度（对应用户问题清单）：
  bug      缺封面/缺 og 图/缺 SEO 字段/坏链接模式/未来日期/空 sections/legacy section 类型
  质量     薄内容(词数)/slop 短语/占位残留/标题与描述长度
  模板化   同 pageType+语言 内完全相同的 section-type 序列 / 5 词 shingle 近重复对
  翻译垃圾 非 EN 文本英文残留率过高 / 与 EN 原文完全一致(未翻译) / 翻译标记
  图片错配 封面 URL 被 N 个不同主题页面复用(批量复用) / composite hero 媒体跨页复用
用法：
  python3 audit-main-content.py --out /tmp/main-audit.json --md /tmp/main-audit.md \
      [--langs en,zh,ja,...] [--max-offset 20000] [--no-shingle]
数据：Sanity HTTP GROQ 分页（token 读 /tmp/sanitytoken.txt）。
输出：JSON + Markdown 摘要（纯文字无表格）。
"""
from __future__ import annotations
import argparse
import collections
import gzip
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT = "o11tm2qe"
DATASET = "production"
API = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/query/{DATASET}"
EXPORT = f"https://{PROJECT}.api.sanity.io/v1/data/export/{DATASET}"

BANNED_EN = [
    (r"\bunlock(?:ing|ed)?\b", "unlock"), (r"\brevolutionize\b", "revolutionize"),
    (r"\bgame[- ]?changer\b", "game-changer"), (r"\bseamless(?:ly)?\b", "seamless"),
    (r"\bdelve[ds]?\b", "delve"), (r"\bunprecedented\b", "unprecedented"),
    (r"\bin today'?s fast[- ]paced\b", "fast-paced opener"), (r"\bcutting[- ]edge\b", "cutting-edge"),
    (r"\bAI[- ]powered platform\b", "AI-powered platform"), (r"\btapestry\b", "tapestry"),
    (r"\bbeacon\b", "beacon"), (r"\brealm\b", "realm"), (r"\bstands as\b", "stands as"),
    (r"\bunderscores?\b", "underscores"), (r"\bvibrant\b", "vibrant"), (r"\belevate\b", "elevate"),
    (r"\btransform(?:s|ing|ed)? your (?:workflow|business)\b", "transform your workflow"),
]
BANNED_ZH = [("赋能", "赋能"), ("无缝", "无缝"), ("革命性", "革命性"), ("颠覆性", "颠覆性"), ("引领未来", "引领未来")]
BANNED_JA = [("シームレス", "シームレス"), ("革命的", "革命的")]
BAD_LINK_PATTERNS = [
    (r"\(/博客文章/", "/博客文章/ link"), (r"\(/cluster/", "/cluster/ link"),
    (r"\.md\)", ".md link"), (r"\]\(#\)", "](#) anchor"), (r"\]\(/\)", "](/) root link"),
]
PLACEHOLDER_PATTERNS = [
    (r"\{[a-z_]{2,}\}", "花括号占位符"), (r"\[TODO\]", "[TODO]"), (r"\[TBD\]", "[TBD]"),
    (r"lorem ipsum", "lorem ipsum"), (r"IMAGE PLACEHOLDER", "IMAGE PLACEHOLDER"),
    (r"\[待补充\]", "[待补充]"), (r"\[待考证\]", "[待考证]"),
]
EN_FUNC = re.compile(r"\b(the|and|of|to|in|for|with|your|that|this|are|is)\b", re.I)

BLOG_FIELDS = """_id, language, "slug": slug.current, title,
  "seoTitle": seo.title, "seoDesc": seo.description,
  "cover": coalesce(coverImage.url, coverImage.asset->url, ""),
  "coverAlt": coalesce(coverImage.alt, ""),
  "og": coalesce(seo.ogImage.url, ""),
  "ogAlt": coalesce(seo.ogImage.alt, ""),
  releaseDate, publishedAt, "category": category->title,
  "text": pt::text(body)"""
COMP_FIELDS = """_id, language, pageType, "slug": slug.current, title,
  "seoTitle": seo.title, "seoDesc": seo.description, bodyJson"""


def q_all(query, token, tries=3):
    u = API + "?query=" + urllib.parse.quote(query)
    hdr = {"Authorization": f"Bearer {token}", "Accept-Encoding": "gzip"}
    last = None
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=hdr), timeout=180)
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return json.loads(raw.decode()).get("result", [])
        except Exception as e:
            last = e
            time.sleep(6 * (i + 1))
    raise RuntimeError(f"GROQ failed: {last}")


def pull_paged(base_query, page, token, label):
    out, off = [], 0
    while True:
        batch = q_all(base_query.replace("$O", str(off)), token)
        out.extend(batch)
        print(f"  [{label}] offset {off} -> {len(batch)} (cum {len(out)})", file=sys.stderr)
        if len(batch) < page or off > 20000:
            return out
        off += page
        time.sleep(1)


def strip_md(s):
    return re.sub(r"\s+", " ", s or "").strip()


def words(text):
    return len(re.findall(r"[A-Za-z0-9']+", text)) + len(re.findall(r"[\u4e00-\u9fff]", text))


def shingles(text, k=5, cap=4000):
    w = re.findall(r"[a-z0-9]+", text.lower())
    if len(w) < k:
        return set()
    hs = set()
    for i in range(min(len(w) - k + 1, cap)):
        hs.add(hash(" ".join(w[i:i + k])))
    return hs


def audit_blog(b, stats):
    issues = []
    text = b.get("text") or ""
    slug, lang = b.get("slug") or "?", b.get("language") or "?"
    n = words(text)
    stats["words_min"] = min(stats["words_min"], n) if stats["words_min"] else n
    if b.get("language") == "en" and n < 800:
        issues.append(f"thin:{n}")
    if not b.get("cover") and not b.get("og"):
        issues.append("no-image")
    if not b.get("seoTitle") or not b.get("seoDesc"):
        issues.append("seo-missing")
    if (b.get("seoDesc") or "") and len(b["seoDesc"]) > 170:
        issues.append("seoDesc-long")
    for pat, name in BAD_LINK_PATTERNS:
        if re.search(pat, text):
            issues.append(f"bad-link:{name}")
    for pat, name in PLACEHOLDER_PATTERNS:
        if re.search(pat, text, re.I):
            issues.append(f"ph:{name}")
    banned = BANNED_EN if lang == "en" else (BANNED_ZH if lang.startswith("zh") else BANNED_JA if lang == "ja" else [])
    for pat, name in banned:
        hits = len(re.findall(pat, text, re.I))
        if hits:
            issues.append(f"slop:{name}x{hits}")
    if b.get("releaseDate") and b["releaseDate"] > time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z":
        issues.append("future-date")
    return issues


def comp_sections(cj):
    try:
        return json.loads(cj)
    except Exception:
        return None


def comp_text(sections):
    parts = []

    def walk(o):
        if isinstance(o, dict):
            for k in ("title", "description", "body", "answer", "question", "label", "quote", "name", "subtitle"):
                v = o.get(k)
                if isinstance(v, str):
                    parts.append(v)
                elif isinstance(v, list):
                    for x in v:
                        walk(x)
            for v in o.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(sections)
    return strip_md(" ".join(parts))


def comp_images(sections):
    urls = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and v.startswith(("http", "/")) and re.search(r"\.(png|jpe?g|webp|gif|svg)(\?|$)", v, re.I):
                    urls.append(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(sections)
    return list(dict.fromkeys(urls))


def audit_comp(c, stats):
    issues = []
    sections = comp_sections(c.get("bodyJson") or "")
    lang, pt, slug = c.get("language") or "?", c.get("pageType") or "?", c.get("slug") or "?"
    if sections is None:
        return ["bodyJson-broken"], "", [], []
    if not sections:
        issues.append("sections-empty")
    text = comp_text(sections)
    n = words(text)
    if lang == "en" and n < 300:
        issues.append(f"thin:{n}")
    for pat, name in BAD_LINK_PATTERNS:
        if re.search(pat, text):
            issues.append(f"bad-link:{name}")
    for pat, name in PLACEHOLDER_PATTERNS:
        if re.search(pat, text, re.I):
            issues.append(f"ph:{name}")
    banned = BANNED_EN if lang == "en" else (BANNED_ZH if lang.startswith("zh") else BANNED_JA if lang == "ja" else [])
    for pat, name in banned:
        hits = len(re.findall(pat, text, re.I))
        if hits:
            issues.append(f"slop:{name}x{hits}")
    if not c.get("seoTitle") or not c.get("seoDesc"):
        issues.append("seo-missing")
    # FAQ/CTA 完备性（EN 才强制）
    if lang == "en":
        types = [s.get("type") for s in sections]
        if "faq" not in types:
            issues.append("no-faq")
        if not any(t and t.startswith("cta") for t in types):
            issues.append("no-cta")
    if not (c.get("cover") if "cover" in c else True):
        issues.append("no-cover")
    return issues, text, [s.get("type") for s in sections], comp_images(sections)


def lang_ratio_flags(text, lang):
    """翻译垃圾启发式：非 EN 页文本中英文残留率过高。"""
    if lang == "en" or not text or len(text) < 300:
        return None
    n = len(text)
    if lang.startswith("zh"):
        cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
        if cjk / max(n, 1) < 0.18:
            return "zh- mostly ASCII (疑似未翻译)"
    elif lang == "ja":
        cjk = len(re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]", text))
        if cjk / max(n, 1) < 0.15:
            return "ja- mostly ASCII (疑似未翻译)"
    elif lang == "ko":
        kor = len(re.findall(r"[\uac00-\ud7af]", text))
        if kor / max(n, 1) < 0.12:
            return "ko- mostly ASCII (疑似未翻译)"
    elif lang == "ru":
        cyr = len(re.findall(r"[\u0400-\u04ff]", text))
        if cyr / max(n, 1) < 0.30:
            return "ru- mostly ASCII (疑似未翻译)"
    else:  # de/fr/it/pt/es
        en_func = len(EN_FUNC.findall(text))
        total = len(re.findall(r"[A-Za-z]+", text))
        if total and en_func / total > 0.18:
            return f"{lang}- English function-word ratio {en_func/total:.0%} (疑似未翻译)"
    return None


def near_dup(items, key_fn, min_words=200):
    inv = collections.defaultdict(set)
    valid = [it for it in items if it["words"] >= min_words]
    for idx, it in enumerate(valid):
        for h in it["sh"]:
            inv[h].add(idx)
    pair = collections.defaultdict(int)
    for h, owners in inv.items():
        if 2 <= len(owners) <= 60:
            owners = sorted(owners)
            for i in range(len(owners)):
                for j in range(i + 1, len(owners)):
                    pair[(owners[i], owners[j])] += 1
    out = []
    for (i, j), shared in pair.items():
        a, b = valid[i], valid[j]
        denom = min(len(a["sh"]), len(b["sh"])) or 1
        sim = shared / denom
        if sim >= 0.6:
            out.append({"a": key_fn(a), "b": key_fn(b), "sim": round(sim, 2)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/main-audit.json")
    ap.add_argument("--md", default="/tmp/main-audit.md")
    ap.add_argument("--langs", default="", help="逗号分隔语言过滤，空=全部")
    ap.add_argument("--no-shingle", action="store_true", help="跳过跨页近重复（省时）")
    args = ap.parse_args()
    token = Path("/tmp/sanitytoken.txt").read_text().strip()
    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    lang_f = f' && language in {json.dumps(langs)}' if langs else ""

    print("== pulling blog ==", file=sys.stderr)
    blogs = pull_paged(f'*[_type=="blog"{lang_f}] | order(_id) [$O...$O+300] {{{BLOG_FIELDS}}}', 300, token, "blog")
    print("== pulling compositePage ==", file=sys.stderr)
    comps = pull_paged(f'*[_type=="compositePage"{lang_f}] | order(_id) [$O...$O+100] {{{COMP_FIELDS}}}', 100, token, "comp")
    print(f"blog={len(blogs)} comp={len(comps)}", file=sys.stderr)

    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "counts": {"blog": len(blogs), "compositePage": len(comps)},
              "blog_issues": [], "comp_issues": [], "dup_pairs": [],
              "seq_templates": {}, "cover_reuse": {}, "hero_reuse": {},
              "lang_garbage": [], "untranslated": []}

    # --- blog ---
    stats = {"words_min": None}
    blog_rows = []
    en_text_by_slug = {}
    for b in blogs:
        text = strip_md(b.get("text") or "")
        issues = audit_blog(b, stats)
        row = {"_id": b["_id"], "lang": b.get("language"), "slug": b.get("slug"),
               "title": strip_md(b.get("title") or ""), "words": words(text), "issues": issues}
        report["blog_issues"].append(row)
        if b.get("language") == "en" and b.get("slug"):
            en_text_by_slug[b["slug"]] = text[:6000]
        g = lang_ratio_flags(text, b.get("language") or "en")
        if g:
            report["lang_garbage"].append({"kind": "blog", "id": b["_id"], "lang": b.get("language"), "slug": b.get("slug"), "why": g})
        if b.get("language") and b["language"] != "en" and b.get("slug") and b["slug"] in en_text_by_slug:
            if text[:4000] == en_text_by_slug[b["slug"]][:4000] and len(text) > 500:
                report["untranslated"].append({"kind": "blog", "id": b["_id"], "lang": b["language"], "slug": b["slug"]})
        blog_rows.append(row)

    # --- composite ---
    comp_rows = []
    seq_counter = collections.defaultdict(list)
    en_comp_text = {}
    hero_seen = collections.defaultdict(set)
    for c in comps:
        issues, text, types, imgs = audit_comp(c, stats)
        row = {"_id": c["_id"], "lang": c.get("language"), "pageType": c.get("pageType"),
               "slug": c.get("slug"), "title": strip_md(c.get("title") or ""),
               "words": words(text), "seq": types, "issues": issues}
        report["comp_issues"].append(row)
        if types:
            seq_counter[(c.get("pageType"), c.get("language"), tuple(types))].append(row)
        if c.get("language") == "en" and c.get("slug"):
            en_comp_text[c["slug"]] = text[:6000]
        g = lang_ratio_flags(text, c.get("language") or "en")
        if g:
            report["lang_garbage"].append({"kind": c.get("pageType"), "id": c["_id"], "lang": c.get("language"), "slug": c.get("slug"), "why": g})
        if c.get("language") and c["language"] != "en" and c.get("slug") and c["slug"] in en_comp_text:
            if text[:4000] == en_comp_text[c["slug"]][:4000] and len(text) > 300:
                report["untranslated"].append({"kind": c.get("pageType"), "id": c["_id"], "lang": c["language"], "slug": c["slug"]})
        # hero 媒体跨页复用（同语言同类型不同 slug 用同一 URL）
        if imgs:
            hero_seen[(c.get("language"), c.get("pageType"), imgs[0])].add(c.get("slug"))
        comp_rows.append(row)
    report["seq_templates"] = {
        f"{k[0]}|{k[1]}": {"n": len(v), "slugs": [r["slug"] for r in v[:30]]}
        for k, v in seq_counter.items() if len(v) >= 5}
    report["hero_reuse"] = {f"{k[0]}|{k[1]}|{k[2].split('/')[-1][:60]}": {"n": len(v), "slugs": sorted(v)[:20]}
                            for k, v in hero_seen.items() if len(v) >= 5}

    # --- 封面跨主题复用（blog） ---
    cover_seen = collections.defaultdict(list)
    for b in blogs:
        u = b.get("cover") or b.get("og")
        if u:
            cover_seen[u.split("?")[0]].append(f"{b.get('language')}:{b.get('slug')}")
    report["cover_reuse"] = {u: {"n": len(sl), "pages": sl[:15]} for u, sl in cover_seen.items() if len(sl) >= 5}

    # --- EN 近重复 ---
    if not args.no_shingle:
        print("== shingle near-dup (EN) ==", file=sys.stderr)
        blog_en = [{"slug": b.get("slug"), "lang": b.get("language"), "type": "blog",
                    "words": words(strip_md(b.get("text") or "")),
                    "sh": shingles(strip_md(b.get("text") or ""))} for b in blogs if b.get("language") == "en"]
        report["dup_pairs"].extend(near_dup(blog_en, lambda r: ("blog", r.get("slug"))))
        comp_en = []
        for c in comps:
            if c.get("language") != "en":
                continue
            sections = comp_sections(c.get("bodyJson") or "")
            text = comp_text(sections) if sections else ""
            comp_en.append({"slug": c.get("slug"), "lang": "en", "type": c.get("pageType"),
                            "words": words(text), "sh": shingles(text)})
        report["dup_pairs"].extend(near_dup(comp_en, lambda r: (r.get("type"), r.get("slug"))))

    json.dump(report, open(args.out, "w"), ensure_ascii=False, indent=1)
    print("json ->", args.out, file=sys.stderr)

    # --- Markdown 摘要（无表格） ---
    L = ["# www.lovart.ai 主站内容审计（Sanity production）", "",
         f"blog {report['counts']['blog']} 篇，compositePage {report['counts']['compositePage']} 页。"]
    for kind, rows in [("blog", report["blog_issues"]), ("compositePage", report["comp_issues"])]:
        bad = [r for r in rows if r["issues"]]
        L.append("")
        L.append(f"## {kind}：{len(bad)}/{len(rows)} 页有问题")
        by_code = collections.Counter(i.split(":")[0] for r in bad for i in r["issues"])
        for k, n in by_code.most_common(12):
            L.append(f"- {k}: {n}")
        for r in bad[:20]:
            L.append(f"  - [{r.get('lang')}|{r.get('pageType') or 'blog'}:{r['slug']}] {'; '.join(r['issues'][:4])}（{r['words']} 词）")
        if len(bad) > 20:
            L.append(f"  - ... 其余 {len(bad) - 20} 页见 JSON")
    L.append("")
    L.append(f"## 同序列模板化（≥5 页完全相同 section 序列，{len(report['seq_templates'])} 组）")
    for k, v in list(report["seq_templates"].items())[:12]:
        L.append(f"- {k}: {v['n']} 页，如 {', '.join(v['slugs'][:5])}")
    L.append("")
    L.append(f"## 跨页近重复（EN，sim≥0.6，{len(report['dup_pairs'])} 对）")
    for d in report["dup_pairs"][:25]:
        L.append(f"- {d['a'][0]}:{d['a'][1]} ≈ {d['b'][0]}:{d['b'][1]}（{d['sim']}）")
    L.append("")
    L.append(f"## 翻译垃圾嫌疑（{len(report['lang_garbage'])}）")
    for g in report["lang_garbage"][:20]:
        L.append(f"- [{g['lang']}] {g['kind']}:{g['slug']} — {g['why']}")
    if len(report["lang_garbage"]) > 20:
        L.append(f"- ... 其余 {len(report['lang_garbage']) - 20} 条见 JSON")
    L.append("")
    L.append(f"## 疑似未翻译（正文与 EN 完全一致，{len(report['untranslated'])}）")
    for g in report["untranslated"][:20]:
        L.append(f"- [{g['lang']}] {g['kind']}:{g['slug']}")
    L.append("")
    L.append(f"## 封面跨主题复用（≥5 页同一封面，{len(report['cover_reuse'])} 个封面）")
    for u, v in list(report["cover_reuse"].items())[:12]:
        L.append(f"- {u.split('/')[-1][:70]} × {v['n']} 页，如 {', '.join(v['pages'][:5])}")
    L.append("")
    L.append(f"## Hero 媒体跨页复用（≥5 页，{len(report['hero_reuse'])} 个）")
    for k, v in list(report["hero_reuse"].items())[:12]:
        L.append(f"- {k} × {v['n']} 页，如 {', '.join(v['slugs'][:5])}")
    open(args.md, "w").write("\n".join(L))
    print("md ->", args.md, file=sys.stderr)


if __name__ == "__main__":
    main()