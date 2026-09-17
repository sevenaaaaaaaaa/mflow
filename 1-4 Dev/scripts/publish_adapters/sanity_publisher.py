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
