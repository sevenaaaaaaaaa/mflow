#!/usr/bin/env python3
"""sanity_publisher.py — 服务端 Sanity 发布器（纯标准库，无需 Node）。

凭证解析优先级：
  1) 环境变量 SANITY_TOKEN / SANITY_PROJECT / SANITY_DATASET（systemd env.sh 注入）
  2) run/secrets/sanity.json  （600，git-ignore）
  3) ~/.config/sanity/config.json 的 authToken（仅本机开发用）

安全设计：
  - 默认 dry_run=True（Sanity mutate API 原生 dryRun，不落库）
  - 写操作用 createIfNotExists（不覆盖既有文档）；blog status 默认 "draft"（发布到前台仍需人工确认）
  - 只读探测 ping() 用于验证凭证与数据集连通

内容模型（2026-09-30 起，对齐 PRD-Blog文章页面开发 §1.3/§4.3 与 Composite 手册 §2.2）：
  - 文档 _id = (type, slug, language) 唯一键：blog → `blog-{slug}-{lang}`，
    compositePage → `{page_type}-{slug}-{lang}`（同线上既有形态，如 tools-logo-maker-en）。
    旧行为（_id=slug）可用环境变量 MFLOW_LEGACY_DOC_ID=1 临时回退。
  - patch 定位按 slug+language GROQ 查询（手册 §2.4），与 _id 方案解耦，旧文档也可 patch。
  - 三时间：publishedAt（真实发布）/ displayedAt（对外显示，PRD C3）；createdAt 用系统 _createdAt 不写。
  - status 五态：draft / scheduled / published / unpublished / archived（PRD §1.3；MFlow 落显式字段）。

用法（CLI）：
  python3 sanity_publisher.py ping
  python3 sanity_publisher.py dry-run --file draft.md --slug my-slug --lang zh --category How-To
  python3 sanity_publisher.py publish  --file draft.md --slug my-slug --lang zh --category How-To --yes
  python3 sanity_publisher.py publish  --file draft.md --mode patch --status scheduled --yes
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
try:
    import section_registry as _REG
except Exception:  # pragma: no cover
    _REG = None
try:
    import storylines as _STORY
except Exception:  # pragma: no cover
    _STORY = None

DEFAULT_PROJECT = "your-project-id"
DEFAULT_DATASET = "production"
API_VERSION = "2024-01-01"

# 分类引用（品牌方 production 既有 taxonomy；未知分类回落到 How-To）
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


STATUS_ENUM = ("draft", "scheduled", "published", "unpublished", "archived")


def doc_id(doc_type, slug, lang):
    """（type, slug, language）唯一键 → 文档 _id（PRD I1 / 手册 §2.2）。
    MFLOW_LEGACY_DOC_ID=1 回退旧行为（_id=slug），仅供迁移期应急。"""
    if os.environ.get("MFLOW_LEGACY_DOC_ID"):
        return slug
    return f"{doc_type}-{slug}-{lang}"


def _iso(dt_text, fallback):
    """frontmatter 日期 → ISO（带时区）。接受 YYYY-MM-DD 或 ISO；空值回落 fallback。"""
    t = str(dt_text or "").strip()
    if not t:
        return fallback
    if re.match(r"^\d{4}-\d{2}-\d{2}$", t):
        return t + "T00:00:00+08:00"
    if re.match(r"^\d{4}-\d{2}-\d{2}[T ]", t) and "+" not in t and "Z" not in t:
        return t.replace(" ", "T") + "+08:00"
    return t


def build_blog_doc(md_path, slug="", lang="", category="", title="", description="",
                   keywords=None, cover_url="", cluster="", author="",
                   status="", published_at="", displayed_at="", legacy_id=None):
    """把本地 md 草稿转成 Sanity blog 文档（默认 status=draft，不覆盖既有 _id）。

    三时间映射（PRD C3）：frontmatter `published` → publishedAt（真实发布时间）；
    `date` → displayedAt（对外显示时间，缺省回落 publishedAt）；createdAt 用系统 _createdAt 不写。
    status 取 CLI 参数 > frontmatter `status` > "draft"，五态外回落 draft。
    """
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
    published = _iso(published_at or fm.get("published") or fm.get("published_at"), now)
    displayed = _iso(displayed_at or fm.get("displayed_at") or fm.get("date"), published)
    st = (status or fm.get("status") or "draft").strip().lower()
    if st not in STATUS_ENUM:
        st = "draft"
    no_index = str(fm.get("no_index", fm.get("noindex", ""))).strip().lower() in ("1", "true", "yes", "on")
    use_legacy = bool(os.environ.get("MFLOW_LEGACY_DOC_ID")) if legacy_id is None else bool(legacy_id)
    body_blocks = md_to_pt(body_md)
    # JSON-LD datePublished 用对外显示时间（PRD C5：datePublished=displayedAt）
    structured = json.dumps({
        "@context": "https://schema.org", "@type": SCHEMA_MAP.get(category, "Article"),
        "headline": title or fm.get("title", ""),
        "author": {"@type": "Organization", "name": author or "品牌方"},
        "datePublished": displayed,
    }, ensure_ascii=False)
    return {
        "_id": slug if use_legacy else doc_id("blog", slug, lang),
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
        "status": st,
        "noIndex": no_index,
        "contentCluster": cluster or fm.get("content_cluster") or "MFlow-GEO",
        "releaseDate": now,
        "publishedAt": published,
        "displayedAt": displayed,
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


def find_by_slug_lang(doc_type, slug, lang):
    """按（slug, language）查文档（手册 §2.4 的取数契约；与 _id 方案解耦）。返回 {_id,_rev} 或 None。"""
    cfg = sanity_cfg()
    if not cfg["token"]:
        return None
    q = f'*[_type=="{doc_type}" && slug.current==$slug && language==$lang][0]{{_id,_rev}}'
    try:
        with _req(cfg, "query", {"query": q, "params": {"slug": slug, "lang": lang}}, timeout=30) as r:
            return json.loads(r.read()).get("result")
    except Exception:
        return None


def publish_blog(doc, dry_run=True, mode="create"):
    """blog 写入。mode=create：同（slug,language）已存在则拒绝并提示（不再静默跳过/重复建号）；
    mode=patch：按 slug+language 定位，ifRevisionID 保护，仅更新内容字段（slug/_id 不动）。"""
    cfg = sanity_cfg()
    if not cfg["token"]:
        return {"ok": False, "error": "未配置 SANITY_TOKEN"}
    slug = doc["slug"]["current"]
    cur = find_by_slug_lang("blog", slug, doc.get("language", ""))
    if mode == "patch":
        if not cur:
            return {"ok": False, "error": f"patch 模式要求文档已存在：slug={slug} lang={doc.get('language')}（新建请用 --mode create）"}
        sets = {k: v for k, v in doc.items() if k not in ("_id", "_type", "slug")}
        mutations = [{"patch": {"id": cur["_id"], "ifRevisionID": cur.get("_rev"), "set": sets}}]
        op = "patch"
    else:
        if cur:
            return {"ok": False,
                    "error": f"同 slug+language 已存在（_id={cur['_id']}）：create 不覆盖既有文档，更新请用 --mode patch"}
        mutations = [{"createIfNotExists": doc}]
        op = "createIfNotExists"
    try:
        with _req(cfg, "mutate", {"mutations": mutations, "dryRun": bool(dry_run)}, timeout=120) as r:
            d = json.loads(r.read())
        return {"ok": True, "dry_run": bool(dry_run), "mode": op, "doctype": "blog",
                "result": d, "blocks": len(doc.get("body", []))}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:400]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:300]}


def publish_file(md_path, dry_run=True, mode="create", **kw):
    doc = build_blog_doc(md_path, **kw)
    return {"doc_id": doc["_id"], **publish_blog(doc, dry_run=dry_run, mode=mode)}


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
        s.add_argument("--status", default="", choices=("",) + STATUS_ENUM,
                       help="draft/scheduled/published/unpublished/archived（缺省读 frontmatter，再缺省 draft）")
        s.add_argument("--mode", default="create", choices=("create", "patch"),
                       help="create=新建（同 slug+language 已存在则拒绝）；patch=按 slug+language 定位更新")
        s.add_argument("--legacy-id", action="store_true", help="临时回退 _id=slug 旧行为（迁移期应急）")
        if name == "publish":
            s.add_argument("--yes", action="store_true", help="确认真实写库（默认 dry-run）")
    a = ap.parse_args()
    if a.cmd == "ping":
        print(json.dumps(ping(), ensure_ascii=False, indent=1))
    elif a.cmd == "dry-run":
        print(json.dumps(publish_file(a.file, slug=a.slug, lang=a.lang, category=a.category,
                                      title=a.title, cluster=a.cluster, status=a.status,
                                      mode=a.mode, legacy_id=a.legacy_id or None, dry_run=True),
                         ensure_ascii=False, indent=1))
    else:
        dry = not a.yes
        print(json.dumps(publish_file(a.file, slug=a.slug, lang=a.lang, category=a.category,
                                      title=a.title, cluster=a.cluster, status=a.status,
                                      mode=a.mode, legacy_id=a.legacy_id or None, dry_run=dry),
                         ensure_ascii=False, indent=1))


# ===================== 落地页（compositePage）支持 =====================
# 注意：compositePage 无 status 字段 → **写入即前台可见**（无草稿态）。
# 因此：默认 dry-run；create 需显式确认；更新优先用 patch 模式（带 ifRevisionID，只改指定字段）。
PAGE_TYPES = {"feature", "tool", "topic", "scenario", "solution", "product", "landing"}
CONTENT_SECTION_TYPES = {"feature-detail", "capability-tabs", "bento-2", "bento-3", "bento-4", "bento-6",
                         "comparison-table", "workflow-horizontal", "cluster-block-dense", "canvas-wall",
                         "proof-block", "testimonial", "pricing-block", "prompt-launcher", "comparison",
                         "stats", "feature-grid", "tool-grid", "blog-grid", "portrait-grid-3",
                         "portrait-grid-4", "showcase-stacked", "showcase-horizontal", "media-marquee",
                         "workflow-vertical", "review-grid-3col", "review-grid-4col"}


def md_to_sections(md_text, title="", description="", cover_url="", cover_alt="", cta_href="https://www.example.com/canvas"):
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
                                        "media": {"src": cover_url, "alt": h["title"][:60] or title}}]})
    # 数字证据段：value+label 数据天然是 stats 型（曾误写成 proof-block + stats 字段错配，前端渲染为空）
    nums = [s for s in (plain + [x for h in h2s for x in h["desc"]]) if len(s) < 120 and any(c.isdigit() for c in s)][:3]
    if len(nums) >= 2:
        sections.append({"type": "stats",
                         "stats": [{"value": (re.findall(r"[\d.,]+", n) or ["—"])[0],
                                    "label": re.sub(r"[\d.,]+", "", n).strip(" ，。()")[:40] or "metric"}
                                   for n in nums]})
    if faq_items:
        sections.append({"type": "faq", "title": "FAQ",
                         "items": [{"question": q["q"][:120], "answer": (q["a"] or "")[:400]}
                                   for q in faq_items[:6]]})
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


def validate_sections(sections, registry=True):
    """落地页版块校验：结构合法性 + 数量预算（RULES-70）+ 注册表逐型字段契约。
    返回 BLOCK 级错误列表（空=通过）；registry=False 或 MFLOW_SKIP_REGISTRY=1 可跳过注册表层。"""
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
    if registry and _REG is not None and not os.environ.get("MFLOW_SKIP_REGISTRY"):
        errs.extend(_REG.validate_sections(sections))
    return errs


def registry_warnings(sections):
    """注册表建议级（不拦发布）：alt 缺省、canvas-wall 条数不足等。"""
    if _REG is None or os.environ.get("MFLOW_SKIP_REGISTRY"):
        return []
    return _REG.validate_sections_full(sections)["warnings"]


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
                elif ls and not ls.startswith(("-", "|", ">", "#")):
                    title = ls[:100]
                    break
    title = title or slug
    description = description or fm.get("description") or ""
    cover_url = cover_url or fm.get("cover_url") or ""
    cover_alt = cover_alt or fm.get("alt_text") or title
    cta_href = cta_href or fm.get("cta_href") or "https://www.example.com/canvas"
    if sections is None:
        sections = md_to_sections(source_text, title, description, cover_url, cover_alt, cta_href)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    displayed = _iso(fm.get("displayed_at") or fm.get("date"), now)
    structured = json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                             "name": title, "description": description[:160],
                             "publisher": {"@type": "Organization", "name": "品牌方"}}, ensure_ascii=False)
    return {
        "_id": doc_id(page_type, slug, lang), "_type": "compositePage",
        "pageType": page_type, "category": page_type,
        "language": lang, "slug": {"_type": "slug", "current": slug},
        "title": title[:200], "description": description[:300],
        "cover": {"_type": "imageSource", "sourceType": "external", "url": cover_url, "alt": cover_alt[:200]},
        "bodyJson": json.dumps(sections, ensure_ascii=False),
        "schemaVersion": "composite-v2", "storylineTemplate": storyline_template,
        "releaseDate": now, "publishedAt": now, "displayedAt": displayed,
        "seo": {"description": description[:160],
                "structuredData": {"_type": "structuredData", "enabled": True, "json": structured}},
    }


def publish_composite(doc, dry_run=True, mode="create"):
    """写入 compositePage。mode=create → createIfNotExists；mode=patch → 只更新指定字段（ifRevisionID）。
    patch 定位按（slug, language）GROQ 查询（手册 §2.4），与 _id 方案解耦，旧 _id 文档也可 patch。
    注意：compositePage 无草稿态 → 真实写入即前台可见。"""
    cfg = sanity_cfg()
    if not cfg["token"]:
        return {"ok": False, "error": "未配置 SANITY_TOKEN"}
    if mode == "patch":
        cur = find_by_slug_lang("compositePage", doc["slug"]["current"], doc.get("language", ""))
        if cur is None:
            return {"ok": False, "error": (f"patch 模式要求文档已存在：slug={doc['slug']['current']} "
                                           f"lang={doc.get('language')}（新建请用 mode=create）")}
        # ⚠ patch 模式：保留既有 slug（覆盖会导致前台路由 404）
        sets = {k: v for k, v in doc.items() if not k.startswith("_") and k != "slug"}
        mutations = [{"patch": {"id": cur["_id"], "ifRevisionID": cur.get("_rev"), "set": sets}}]
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


def publish_landing(md_path, dry_run=True, mode="create", registry=True, **kw):
    """落地页发布：结构校验 + 注册表逐型字段校验 + 故事线顺序校验（known 故事线错位=BLOCK）。
    故事线 SSOT：1-3 GenFlow/Page Gen/Refresh-Page/；未注册故事线降级为 warning 不拦。"""
    doc = build_composite_doc(md_path=md_path, **kw)
    sections = json.loads(doc["bodyJson"])
    errs = validate_sections(sections, registry=registry)
    warns = registry_warnings(sections) if registry else []
    sid = kw.get("storyline_template") or ""
    if sid and _STORY is not None and not os.environ.get("MFLOW_SKIP_REGISTRY"):
        chk = _STORY.check_storyline([s.get("type") for s in sections], sid)
        if chk["known"] and chk["fixed"] and not chk["ok"]:
            errs.extend(chk["problems"])
        elif not chk["known"]:
            warns.append(f"故事线 {sid} 未注册（SSOT：1-3 GenFlow/Page Gen/Refresh-Page），跳过顺序校验")
    if errs:
        return {"ok": False, "doc_id": doc["_id"], "validation_errors": errs, "warnings": warns,
                "error": "落地页结构校验未通过：" + "；".join(errs[:3])}
    out = publish_composite(doc, dry_run=dry_run, mode=mode)
    out["doc_id"] = doc["_id"]
    out["warnings"] = warns
    return out
