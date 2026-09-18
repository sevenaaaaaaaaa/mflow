#!/usr/bin/env python3
"""sanity_publisher.py — 服务端 Sanity 发布器（纯标准库，无需 Node）。

凭证解析优先级：
  1) 环境变量 SANITY_TOKEN / SANITY_PROJECT / SANITY_DATASET（systemd env.sh 注入）
  2) run/secrets/sanity.json  （600，git-ignore）
  3) ~/.config/sanity/config.json 的 authToken（仅本机开发用）

安全设计：
  - 默认 dry_run=True（Sanity mutate API 原生 dryRun，不落库）
  - 写操作用 createIfNotExists（不覆盖既有文档），status 一律 "draft"（发布到前台仍需人工在 Sanity 侧确认）
  - 只读探测 ping() 用于验证凭证与数据集连通

用法（CLI）：
  python3 sanity_publisher.py ping
  python3 sanity_publisher.py dry-run --file draft.md --slug my-slug --lang zh --category How-To
  python3 sanity_publisher.py publish  --file draft.md --slug my-slug --lang zh --category How-To --yes
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from md_to_portable_text import md_to_portable_text as md_to_pt
except Exception as e:  # pragma: no cover
    md_to_pt = None
    _PT_ERR = str(e)

DEFAULT_PROJECT = "o11tm2qe"
DEFAULT_DATASET = "production"
API_VERSION = "2024-01-01"

# 分类引用（Lovart production 既有 taxonomy；未知分类回落到 How-To）
CAT_REF = {
    "How-To": "9d3210aa-e6e1-4391-b1fd-a634147de088",
    "Best Practice": "a5d8df07-3ab1-4411-a7b0-5b7fad3adf82",
    "Industry Solution": "247a9752-888d-44d1-b113-5f75edb5b96c",
    "Comparison": "9d3210aa-e6e1-4391-b1fd-a634147de088",
    "Branding": "5a9df9bb-d0b6-4ef9-8257-af3b470db780",
}
SCHEMA_MAP = {"How-To": "HowTo", "Comparison": "HowTo", "Best Practice": "HowTo",
              "Industry Solution": "Article", "Branding": "Article"}

RUN_SECRETS = Path(__file__).resolve().parents[3] / "run" / "secrets" / "sanity.json"


def sanity_cfg():
    """返回 {project, dataset, token, source}；token 为空表示未配置。"""
    tok = os.environ.get("SANITY_TOKEN", "").strip()
    proj = os.environ.get("SANITY_PROJECT", "").strip() or DEFAULT_PROJECT
    ds = os.environ.get("SANITY_DATASET", "").strip() or DEFAULT_DATASET
    if tok:
        return {"project": proj, "dataset": ds, "token": tok, "source": "env"}
    if RUN_SECRETS.exists():
        try:
            d = json.loads(RUN_SECRETS.read_text())
            if d.get("token"):
                return {"project": d.get("project", proj), "dataset": d.get("dataset", ds),
                        "token": d["token"], "source": str(RUN_SECRETS)}
        except Exception:
            pass
    mac = Path.home() / ".config" / "sanity" / "config.json"
    if mac.exists():
        try:
            d = json.loads(mac.read_text())
            if d.get("authToken"):
                return {"project": proj, "dataset": ds, "token": d["authToken"], "source": "sanity-cli"}
        except Exception:
            pass
    return {"project": proj, "dataset": ds, "token": "", "source": "none"}


def _api(cfg, path):
    return f"https://{cfg['project']}.api.sanity.io/v{API_VERSION}/data/{path}/{cfg['dataset']}"


def _req(cfg, path, payload=None, method="POST", timeout=60):
    url = _api(cfg, path)
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data,
                                 headers={"Authorization": f"Bearer {cfg['token']}",
                                          "Content-Type": "application/json"},
                                 method=method)
    return urllib.request.urlopen(req, timeout=timeout)


def ping():
    """只读连通性探测：返回 blog 文档数与最近更新时间。"""
    cfg = sanity_cfg()
    if not cfg["token"]:
        return {"ok": False, "error": "未配置 SANITY_TOKEN（run/secrets/sanity.json 或环境变量）"}
    q = ('{ "n": count(*[_type=="blog"]), '
         '"latest": *[_type=="blog"] | order(_updatedAt desc)[0]{_id,_updatedAt,language,status} }')
    try:
        with _req(cfg, "query", payload={"query": q}, method="POST", timeout=30) as r:
            d = json.loads(r.read())
        res = d.get("result", {})
        return {"ok": True, "project": cfg["project"], "dataset": cfg["dataset"],
                "source": cfg["source"], "blogs": res.get("n"), "latest": res.get("latest")}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if k == "keywords":
            try:
                v = json.loads(v.replace("'", '"'))
            except Exception:
                v = [x.strip().strip("\"'") for x in v.strip("[]").split(",")] if v.startswith("[") else [v]
        fm[k] = v
    return fm


def build_blog_doc(md_path, slug="", lang="", category="", title="", description="",
                   keywords=None, cover_url="", cluster="", author=""):
    """把本地 md 草稿转成 Sanity blog 文档（status=draft，不覆盖既有 _id）。"""
    if md_to_pt is None:
        raise RuntimeError(f"md_to_portable_text 不可用：{_PT_ERR}")
    p = Path(md_path)
    text = p.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    body_md = parts[2].strip() if len(parts) >= 3 else text
    fm = parse_frontmatter(text)
    slug = slug or fm.get("slug") or p.stem
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff-]", "-", str(slug)).strip("-").lower()
    lang = lang or fm.get("language") or fm.get("lang") or "zh"
    category = category or fm.get("category") or "How-To"
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    body_blocks = md_to_pt(body_md)
    structured = json.dumps({
        "@context": "https://schema.org", "@type": SCHEMA_MAP.get(category, "Article"),
        "headline": title or fm.get("title", ""),
        "author": {"@type": "Organization", "name": author or "Lovart"},
        "datePublished": now,
    }, ensure_ascii=False)
    return {
        "_id": slug,
        "_type": "blog",
        "title": (title or fm.get("title") or "")[:200],
        "slug": {"_type": "slug", "current": slug},
        "language": lang,
        "category": {"_type": "reference", "_ref": CAT_REF.get(category, CAT_REF["How-To"])},
        "description": (description or fm.get("description") or "")[:200],
        "keywords": keywords or fm.get("keywords") or [],
        "seoTitle": (fm.get("seo_title") or "")[:70],
        "seoDescription": (fm.get("seo_description") or "")[:160],
        "coverUrl": cover_url or fm.get("cover_url") or "",
        "altText": fm.get("alt_text", ""),
        "status": "draft",
        "noIndex": False,
        "contentCluster": cluster or fm.get("content_cluster") or "MFlow-GEO",
        "releaseDate": now,
        "publishedAt": now,
        "seo": {"structuredData": {"_type": "structuredData", "enabled": True, "json": structured}},
        "body": body_blocks,
    }


def upsert(doc, dry_run=True, mode="createIfNotExists"):
    """写库。dry_run=True 走 Sanity 原生 dryRun（返回 transactionId，不落库）。"""
    cfg = sanity_cfg()
    if not cfg["token"]:
        return {"ok": False, "error": "未配置 SANITY_TOKEN"}
    payload = {"mutations": [{mode: doc}], "dryRun": bool(dry_run)}
    try:
        with _req(cfg, "mutate", payload=payload, timeout=120) as r:
            d = json.loads(r.read())
        return {"ok": True, "dry_run": bool(dry_run), "result": d, "blocks": len(doc.get("body", []))}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:400]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:300]}


def publish_file(md_path, **kw):
    dry = kw.pop("dry_run", True)
    doc = build_blog_doc(md_path, **kw)
    return {"doc_id": doc["_id"], **upsert(doc, dry_run=dry)}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="MFlow Sanity 发布器")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ping")
    for name in ("dry-run", "publish"):
        s = sub.add_parser(name)
        s.add_argument("--file", required=True)
        s.add_argument("--slug", default="")
        s.add_argument("--lang", default="")
        s.add_argument("--category", default="")
        s.add_argument("--title", default="")
        s.add_argument("--cluster", default="")
        if name == "publish":
            s.add_argument("--yes", action="store_true", help="确认真实写库（默认 dry-run）")
    a = ap.parse_args()
    if a.cmd == "ping":
        print(json.dumps(ping(), ensure_ascii=False, indent=1))
    elif a.cmd == "dry-run":
        print(json.dumps(publish_file(a.file, slug=a.slug, lang=a.lang, category=a.category,
                                      title=a.title, cluster=a.cluster, dry_run=True),
                         ensure_ascii=False, indent=1))
    else:
        dry = not a.yes
        print(json.dumps(publish_file(a.file, slug=a.slug, lang=a.lang, category=a.category,
                                      title=a.title, cluster=a.cluster, dry_run=dry),
                         ensure_ascii=False, indent=1))


# ===================== 落地页（compositePage）支持 =====================
# 注意：compositePage 无 status 字段 → **写入即前台可见**（无草稿态）。
# 因此：默认 dry-run；create 需显式确认；更新优先用 patch 模式（带 ifRevisionID，只改指定字段）。
PAGE_TYPES = {"feature", "tool", "topic", "scenario", "solution", "product", "landing"}
CONTENT_SECTION_TYPES = {"feature-detail", "capability-tabs", "bento-2", "bento-3", "bento-4", "bento-6",
                         "comparison-table", "workflow-horizontal", "cluster-block-dense", "canvas-wall",
                         "proof-block", "testimonial", "pricing-block", "prompt-launcher", "comparison"}


def md_to_sections(md_text, title="", description="", cover_url="", cover_alt="", cta_href="https://www.lovart.ai/canvas"):
    """把落地页草稿（md）转成 composite-v2 最小合法版块数组。
    结构：hero-split → feature-detail(按 H2 归组) → (proof-block 如有数据点) → faq → cta-default"""
    body = md_text
    if body.startswith("---"):
        parts = body.split("---", 2)
        body = parts[2] if len(parts) >= 3 else body
    lines = [l.rstrip() for l in body.split("\n")]
    h2s, cur = [], None
    faq_items = []
    plain = []
    in_faq_container = False
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("## "):
            head = s[3:].strip()
            if re.match(r"^(FAQ|常见问题|よくある|자주 묻는)", head, re.I):
                in_faq_container = True
                cur = None
                continue
            in_faq_container = False
            if head.endswith(("?", "？")):
                cur = {"q": head.rstrip("?？"), "a": ""}
                faq_items.append(cur)
            else:
                cur = {"title": head, "desc": []}
                h2s.append(cur)
        elif s.startswith("### ") and (in_faq_container or s[4:].strip().endswith(("?", "？"))):
            head = s[4:].strip()
            cur = {"q": head.rstrip("?？"), "a": ""}
            faq_items.append(cur)
        elif cur is not None:
            if s.startswith("#"):
                continue
            if s:
                if "q" in cur:
                    if not cur["a"]:
                        cur["a"] = s[:400]
                else:
                    cur["desc"].append(s)
        elif s and not s.startswith("#"):
            plain.append(s)
    desc_text = (description or (plain[0] if plain else ""))[:400]
    first_sentence = re.split(r"[。.!?？]", desc_text)[0][:60] if desc_text else ""
    sections = [{
        "type": "hero-split", "badge": "", "title": title,
        "highlightedText": first_sentence,
        "description": desc_text,
        "buttons": [{"text": "Start free", "href": cta_href, "variant": "primary"},
                    {"text": "See examples", "href": cta_href, "variant": "secondary"}],
        "media": {"src": cover_url, "alt": cover_alt or title},
    }]
    for h in h2s[:4]:
        d = " ".join(h["desc"]).strip()
        if d:
            sections.append({"type": "feature-detail", "title": "", "description": "",
                             "items": [{"title": h["title"][:80], "description": d[:400],
                                        "media": {"src": cover_url}}]})
    # proof-block：正文里能找到 ≥2 个含数字的短句才生成
    nums = [s for s in (plain + [x for h in h2s for x in h["desc"]]) if len(s) < 120 and any(c.isdigit() for c in s)][:3]
    if len(nums) >= 2:
        sections.append({"type": "proof-block", "title": "Why teams choose this",
                         "stats": [{"value": (re.findall(r"[\d.,]+", n) or ["—"])[0], "label": re.sub(r"[\d.,]+", "", n).strip(" ，。()")[:40] or "metric"}
                                   for n in nums]})
    if faq_items:
        sections.append({"type": "faq", "title": "FAQ",
                         "items": [[q["q"][:120], (q["a"] or "")[:400]] for q in faq_items[:6]]})
    sections.append({"type": "cta-default", "title": f"Ready to try {title[:50]}?" if title else "Get started",
                     "description": "Start free — no design skill required.",
                     "buttons": [{"text": "Start free", "href": cta_href, "variant": "primary"}]})
    return sections


def _section_text_len(sec):
    """词当量（与 quota-check 同口径）：CJK 字符 + 拉丁词数 ×1.5。英文页面不再被原始字符数误伤。"""
    cjk = words = 0

    def walk(v):
        nonlocal cjk, words
        if isinstance(v, str):
            cjk += len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", v))
            words += len(re.findall(r"[A-Za-z0-9]+", v))
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(sec)
    return int(cjk + words * 1.5)


def validate_sections(sections):
    """落地页版块校验：结构合法性 + 数量预算（RULES-70）。返回错误列表（空=通过）。"""
    errs = []
    if not isinstance(sections, list) or not sections:
        return ["sections 必须是非空数组"]
    types_ = [s.get("type") for s in sections if isinstance(s, dict)]
    if not any(t in ("hero-split", "hero-cinematic") for t in types_):
        errs.append("缺 hero 版块（hero-split / hero-cinematic）")
    n_content = sum(1 for t in types_ if t in CONTENT_SECTION_TYPES)
    if n_content < 2:
        errs.append(f"内容版块不足（需 ≥2，当前 {n_content}）")
    faqs = [s for s in sections if isinstance(s, dict) and s.get("type") == "faq"]
    if faqs:
        items = faqs[0].get("items") or []
        if len(items) > 8:
            errs.append(f"FAQ 超过 8 条（当前 {len(items)}）")
    if not any(t == "cta-default" for t in types_):
        errs.append("缺 cta-default 结尾版块")
    total = sum(_section_text_len(s) for s in sections)
    if total > 1200:
        errs.append(f"文案词当量 {total} > 1200（RULES-70 落地页上限，压缩冗余）")
    if total < 200:
        errs.append(f"文案总长 {total} < 200（内容过薄）")
    for i, s in enumerate(sections):
        if not isinstance(s, dict) or not s.get("type"):
            errs.append(f"sections[{i}] 缺 type")
            continue
        if s["type"] == "hero-split":
            if not (s.get("title") or "").strip():
                errs.append("hero-split 缺 title")
            m = s.get("media") or {}
            if m.get("src") and not (m.get("alt") or "").strip():
                errs.append("hero media 缺 alt（GEO/可访问性）")
    return errs


def build_composite_doc(md_path="", slug="", lang="en", page_type="tool", title="", description="",
                        cover_url="", cover_alt="", storyline_template="T-long", cta_href="",
                        sections=None, sections_path=""):
    """构造 compositePage 文档（bodyJson 为字符串）。"""
    source_text, fm = "", {}
    if md_path:
        p = Path(md_path)
        source_text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(source_text)
        slug = slug or fm.get("slug") or p.stem
    if sections_path:
        try:
            sections = json.loads(Path(sections_path).read_text())
        except Exception as e:
            raise RuntimeError(f"sections 文件解析失败：{e}")
    if page_type not in PAGE_TYPES:
        raise RuntimeError(f"page_type 非法：{page_type}（可选 {sorted(PAGE_TYPES)}）")
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff-]", "-", str(slug)).strip("-").lower()
    if not slug:
        raise RuntimeError("slug 不能为空")
    if not title:
        title = fm.get("title") or ""
        if not title:
            for l in source_text.split("\n"):
                ls = l.strip()
                if ls.startswith("# "):
                    title = ls[2:].strip()
                    break
                elif ls and not ls.startswith(("-", "|", ">")):
                    title = ls[:100]
                    break
    title = title or slug
    description = description or fm.get("description") or ""
    cover_url = cover_url or fm.get("cover_url") or ""
    cover_alt = cover_alt or fm.get("alt_text") or title
    cta_href = cta_href or fm.get("cta_href") or "https://www.lovart.ai/canvas"
    if sections is None:
        sections = md_to_sections(source_text, title, description, cover_url, cover_alt, cta_href)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    structured = json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                             "name": title, "description": description[:160],
                             "publisher": {"@type": "Organization", "name": "Lovart"}}, ensure_ascii=False)
    return {
        "_id": slug, "_type": "compositePage", "pageType": page_type, "category": page_type,
        "language": lang, "slug": {"_type": "slug", "current": slug},
        "title": title[:200], "description": description[:300],
        "cover": {"_type": "imageSource", "sourceType": "external", "url": cover_url, "alt": cover_alt[:200]},
        "bodyJson": json.dumps(sections, ensure_ascii=False),
        "schemaVersion": "composite-v2", "storylineTemplate": storyline_template,
        "releaseDate": now, "publishedAt": now,
        "seo": {"description": description[:160],
                "structuredData": {"_type": "structuredData", "enabled": True, "json": structured}},
    }


def publish_composite(doc, dry_run=True, mode="create"):
    """写入 compositePage。mode=create → createIfNotExists；mode=patch → 只更新指定字段（ifRevisionID）。
    注意：compositePage 无草稿态 → 真实写入即前台可见。"""
    cfg = sanity_cfg()
    if not cfg["token"]:
        return {"ok": False, "error": "未配置 SANITY_TOKEN"}
    if mode == "patch":
        try:
            with _req(cfg, "query", {"query": f'*[_id=="{doc["_id"]}"][0]{{_id,_rev}}'}, timeout=30) as r:
                cur = json.loads(r.read()).get("result")
        except Exception as e:
            return {"ok": False, "error": f"读取现有文档失败：{str(e)[:120]}"}
        if not cur:
            return {"ok": False, "error": f"patch 模式要求文档已存在：{doc['_id']}（新建请用 mode=create）"}
        sets = {k: v for k, v in doc.items() if not k.startswith("_")}
        mutations = [{"patch": {"id": doc["_id"], "ifRevisionID": cur.get("_rev"), "set": sets}}]
    else:
        mutations = [{"createIfNotExists": doc}]
    try:
        with _req(cfg, "mutate", {"mutations": mutations, "dryRun": bool(dry_run)}, timeout=120) as r:
            d = json.loads(r.read())
        return {"ok": True, "dry_run": bool(dry_run), "mode": mode, "doctype": "compositePage",
                "result": d, "sections": len(json.loads(doc["bodyJson"]))}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:400]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:300]}


def publish_landing(md_path, dry_run=True, mode="create", **kw):
    doc = build_composite_doc(md_path=md_path, **kw)
    errs = validate_sections(json.loads(doc["bodyJson"]))
    if errs:
        return {"ok": False, "doc_id": doc["_id"], "validation_errors": errs,
                "error": "落地页结构校验未通过：" + "；".join(errs[:3])}
    out = publish_composite(doc, dry_run=dry_run, mode=mode)
    out["doc_id"] = doc["_id"]
    return out
