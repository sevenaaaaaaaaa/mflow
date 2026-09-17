#!/usr/bin/env python3
"""sanity_pull.py — 把 Sanity 内容镜像到 MFlow 内容库（按站点目录结构归档）。

站点档案驱动（这是"兼容不同网站目录结构"的关键）：
  run/sites/{site}.json → {domain, source, sections:[{key,docType,pageType,dir,route,...}]}

输出布局：
  run/library/{site}/{section}/{lang}/{slug}.md      （frontmatter + 正文）
  run/library/{site}/index.json                      （sections/lang 计数 + 同步时间）
  run/library/{site}/sync-status.json                （后台同步进度）

用法：
  python3 sanity_pull.py --site lovart-global --dry-run
  python3 sanity_pull.py --site lovart-global --sections blog --max 20      # 试跑
  python3 sanity_pull.py --site lovart-global --sections blog,features,tools,topic,scenario,solution,product
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pt_to_md import portable_text_to_md, bodyjson_to_md  # noqa: E402

ROOT = HERE.parents[2]                       # 仓库根
LIB_ROOT = ROOT / "run" / "library"
SITES_DIR = ROOT / "run" / "sites"
SECRETS = ROOT / "run" / "secrets" / "sanity.json"
PAGE = 100


def sanity_token():
    import os
    if os.environ.get("SANITY_TOKEN"):
        return os.environ["SANITY_TOKEN"]
    if SECRETS.exists():
        return json.loads(SECRETS.read_text()).get("token", "")
    mac = Path.home() / ".config" / "sanity" / "config.json"
    if mac.exists():
        return json.loads(mac.read_text()).get("authToken", "")
    return ""


def sanity_query(project, dataset, query, token, timeout=120):
    url = f"https://{project}.api.sanity.io/v2024-01-01/data/query/{dataset}"
    req = urllib.request.Request(url, data=json.dumps({"query": query}).encode(),
                                 headers={"Authorization": f"Bearer {token}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read()).get("result")


def load_site(site):
    p = SITES_DIR / f"{site}.json"
    if not p.exists():
        raise SystemExit(f"站点档案不存在：{p}")
    return json.loads(p.read_text())


def build_url(site, sec, lang, slug):
    route = sec.get("route", "/{lang}/{dir}/{slug}")
    r = route.replace("{lang}", lang).replace("{slug}", slug).replace("{dir}", sec.get("dir", sec["key"]))
    if lang == site.get("default_lang", "en") and "{lang}" in route:
        # 默认语言不带前缀（站点级配置；不同站点可设 default_lang 与 keep_prefix）
        r = route.replace("/{lang}", "").replace("{lang}", "").replace("{slug}", slug).replace("{dir}", sec.get("dir", sec["key"]))
    if not r.startswith("/"):
        r = "/" + r
    return f"https://{site.get('domain','')}{r}"


def md_escape(v):
    if isinstance(v, (dict, list)):
        v = json.dumps(v, ensure_ascii=False)
    return str(v or "").replace("\n", " ").strip()


def write_doc(site_id, site, sec, doc, dry=False):
    slug = (doc.get("slug") or {}).get("current") if isinstance(doc.get("slug"), dict) else doc.get("slug")
    slug = slug or re.sub(r"[^a-z0-9-]", "-", str(doc.get("_id", "")).lower())
    lang = doc.get("language") or site.get("default_lang", "en")
    if sec.get("engine") == "portable-text":
        body = portable_text_to_md(doc.get("body") or [])
    else:
        body = bodyjson_to_md(doc.get("bodyJson") or doc.get("body") or "")
    url = build_url(site, sec, lang, slug)
    fm = ["---",
          f"site: {site_id}",
          f"section: {sec['key']}",
          f"doc_type: {doc.get('_type','')}",
          f"language: {lang}",
          f"slug: {slug}",
          f"title: {json.dumps(md_escape(doc.get('title')), ensure_ascii=False)}",
          f"page_type: {md_escape(doc.get('pageType'))}",
          f"status: {md_escape(doc.get('status'))}",
          f"published_at: {md_escape(doc.get('publishedAt') or doc.get('releaseDate'))}",
          f"updated_at: {md_escape(doc.get('_updatedAt'))}",
          f"url: {url}",
          f"sanity_id: {doc.get('_id','')}",
          "---", ""]
    text = "\n".join(fm) + (doc.get("description") or doc.get("seo", {}).get("description") or "") + "\n\n" + body + "\n"
    rel = Path(site_id) / sec["dir"] / lang / f"{slug}.md"
    target = LIB_ROOT / rel
    if not dry:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return rel, len(text)


def pull_section(site_id, site, sec, token, max_n=0, dry=False, progress=None):
    src = site["source"]
    proj, ds = src["project"], src["dataset"]
    where = f'_type=="{sec["docType"]}"'
    if sec.get("pageType"):
        where += f' && pageType=="{sec["pageType"]}"'
    where += " && !(_id in path(\"drafts.**\"))"
    total = sanity_query(proj, ds, f'count(*[{where}])', token) or 0
    limit = total if max_n <= 0 else min(total, max_n)
    done, size, langs, errors = 0, 0, {}, 0
    fields = sec.get("fields") or "_id,_type,title,slug,language,status,pageType,publishedAt,releaseDate,_updatedAt,description,seo"
    if sec.get("engine") == "portable-text":
        fields += ",body"
    else:
        fields += ",bodyJson"
    for start in range(0, limit, PAGE):
        q = f'*[{where}] | order(_updatedAt desc) [{start}...{start+PAGE}]{{{fields}}}'
        try:
            docs = sanity_query(proj, ds, q, token) or []
        except Exception as e:
            errors += 1
            if progress:
                progress(f"  批次 {start} 失败：{str(e)[:120]}")
            continue
        for d in docs[: max(0, limit - done)]:
            try:
                rel, n = write_doc(site_id, site, sec, d, dry=dry)
                langs[d.get("language") or site.get("default_lang", "en")] = langs.get(d.get("language") or site.get("default_lang", "en"), 0) + 1
                size += n
                done += 1
            except Exception:
                errors += 1
        if progress:
            progress(f"  {sec['key']}: {done}/{limit}（{size//1024} KB）")
    return {"section": sec["key"], "dir": sec["dir"], "total": total, "pulled": done,
            "bytes": size, "langs": langs, "errors": errors}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="lovart-global")
    ap.add_argument("--sections", default="", help="逗号分隔 section key；空=全部")
    ap.add_argument("--max", type=int, default=0, help="每 section 上限（0=全部）")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    site = load_site(a.site)
    token = sanity_token()
    if not token:
        raise SystemExit("无 Sanity token（run/secrets/sanity.json 或 env SANITY_TOKEN）")
    wanted = [s.strip() for s in a.sections.split(",") if s.strip()]
    secs = [s for s in site["sections"] if not wanted or s["key"] in wanted]

    def log(msg):
        print(msg, flush=True)

    status_p = LIB_ROOT / a.site / "sync-status.json"
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def set_status(state, extra=None):
        if a.dry_run:
            return
        status_p.parent.mkdir(parents=True, exist_ok=True)
        payload = {"state": state, "site": a.site, "started": started,
                   "updated": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        payload.update(extra or {})
        status_p.write_text(json.dumps(payload, ensure_ascii=False, indent=1))

    set_status("running", {"sections": [s["key"] for s in secs]})
    log(f"[{a.site}] 站点：{site.get('name')} · 域名 {site.get('domain')} · 段落 {[s['key'] for s in secs]}")
    results = []
    for sec in secs:
        r = pull_section(a.site, site, sec, token, max_n=a.max, dry=a.dry_run, progress=log)
        results.append(r)
        set_status("running", {"done_sections": [x["section"] for x in results]})

    index = {"site": a.site, "name": site.get("name"), "domain": site.get("domain"),
             "synced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "dry_run": a.dry_run, "sections": {r["section"]: {"dir": r["dir"], "total": r["total"],
                                                              "pulled": r["pulled"], "bytes": r["bytes"],
                                                              "langs": r["langs"], "errors": r["errors"]}
                                                for r in results}}
    if not a.dry_run:
        (LIB_ROOT / a.site).mkdir(parents=True, exist_ok=True)
        (LIB_ROOT / a.site / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
        set_status("done", {"pulled": sum(r["pulled"] for r in results)})
    log(json.dumps(index, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
