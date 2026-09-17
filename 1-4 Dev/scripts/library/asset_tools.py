#!/usr/bin/env python3
"""asset_tools.py — 落地页/Blog 图片物料台账与批量替换（Sanity compositePage + blog）。

物料位置：
  - cover      : {_type:"imageSource", sourceType:"external", url, alt}
  - bodyJson   : 版块数组（字符串字段），版块内 media={src, alt}；部分版块另有 image/backgroundImage

能力：
  scan   → 生成物料台账 run/library/{site}/assets.json（页面 → 物料；URL → 使用方反查）
  plan   → 依据匹配规则（exact/prefix/regex/url-map）与过滤（section/lang/pageType/slug）生成替换计划
  apply  → 执行计划（默认 dry-run；真实写入用 ifRevisionID 防并发覆盖，逐批审计）

安全：dry-run 默认；真实写入需 --yes；每批 ≤50 个 patch；写前重取 _rev。
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB_ROOT = ROOT / "run" / "library"
SITES_DIR = ROOT / "run" / "sites"
SECRETS = ROOT / "run" / "secrets" / "sanity.json"
PAGE = 100
BATCH = 50


def token():
    import os
    if os.environ.get("SANITY_TOKEN"):
        return os.environ["SANITY_TOKEN"]
    if SECRETS.exists():
        return json.loads(SECRETS.read_text()).get("token", "")
    mac = Path.home() / ".config" / "sanity" / "config.json"
    return json.loads(mac.read_text()).get("authToken", "") if mac.exists() else ""


def site_of(site):
    return json.loads((SITES_DIR / f"{site}.json").read_text())


def query(proj, ds, q, tok, timeout=180):
    url = f"https://{proj}.api.sanity.io/v2024-01-01/data/query/{ds}"
    req = urllib.request.Request(url, data=json.dumps({"query": q}).encode(),
                                 headers={"Authorization": f"Bearer {tok}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read()).get("result")


def mutate(proj, ds, mutations, tok, dry_run=True, timeout=180):
    url = f"https://{proj}.api.sanity.io/v2024-01-01/data/mutate/{ds}"
    payload = {"mutations": mutations, "dryRun": bool(dry_run)}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {tok}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


# ─────────────────────────── scan ───────────────────────────
def scan(site, sections="", max_n=0):
    """扫描物料 → run/library/{site}/assets.json"""
    prof = site_of(site)
    proj, ds = prof["source"]["project"], prof["source"]["dataset"]
    tok = token()
    want = [s.strip() for s in sections.split(",") if s.strip()]
    secs = [s for s in prof["sections"] if (not want or s["key"] in want) and s.get("docType") in ("compositePage", "blog")]
    pages, urls = {}, {}

    def add_url(u, doc_id, role, alt):
        if not u:
            return
        e = urls.setdefault(u, {"n": 0, "roles": {}, "pages": [], "alt": alt})
        e["n"] += 1
        e["roles"][role] = e["roles"].get(role, 0) + 1
        if doc_id not in e["pages"]:
            e["pages"].append(doc_id)

    for sec in secs:
        where = f'_type=="{sec["docType"]}"'
        if sec.get("pageType"):
            where += f' && pageType=="{sec["pageType"]}"'
        where += ' && !(_id in path("drafts.**"))'
        total = query(proj, ds, f"count(*[{where}])", tok) or 0
        limit = total if max_n <= 0 else min(total, max_n)
        for start in range(0, limit, PAGE):
            q = (f'*[{where}] | order(_id) [{start}...{start+PAGE}]'
                 f'{{_id,_rev,title,slug,language,pageType,cover,bodyJson,coverUrl}}')
            try:
                docs = query(proj, ds, q, tok) or []
            except Exception as e:
                print(f"  批次 {start} 失败: {str(e)[:120]}", file=sys.stderr)
                continue
            for d in docs[: max(0, limit - start)]:
                did = d["_id"]
                slug = (d.get("slug") or {}).get("current") if isinstance(d.get("slug"), dict) else d.get("slug")
                lang = d.get("language") or prof.get("default_lang", "en")
                rec = {"slug": slug or did, "lang": lang, "pageType": d.get("pageType") or sec["docType"],
                       "section": sec["key"], "title": d.get("title", ""), "rev": d.get("_rev", ""),
                       "cover": None, "media": []}
                cov = d.get("cover") or {}
                if cov.get("url"):
                    rec["cover"] = {"url": cov["url"], "alt": cov.get("alt", "")}
                    add_url(cov["url"], did, "cover", cov.get("alt", ""))
                if d.get("coverUrl"):
                    rec["cover"] = rec["cover"] or {"url": d["coverUrl"], "alt": ""}
                    add_url(d["coverUrl"], did, "cover", "")
                if d.get("bodyJson"):
                    try:
                        arr = json.loads(d["bodyJson"])
                    except Exception:
                        arr = []
                    for i, s in enumerate(arr if isinstance(arr, list) else []):
                        if not isinstance(s, dict):
                            continue
                        for key in ("media", "image", "backgroundImage"):
                            m = s.get(key)
                            if isinstance(m, dict) and m.get("src"):
                                rec["media"].append({"idx": i, "sect": s.get("type", ""), "field": key,
                                                     "src": m["src"], "alt": m.get("alt", "")})
                                add_url(m["src"], did, "media", m.get("alt", ""))
                            elif isinstance(m, str) and m.startswith("http"):
                                rec["media"].append({"idx": i, "sect": s.get("type", ""), "field": key,
                                                     "src": m, "alt": ""})
                                add_url(m, did, "media", "")
                pages[did] = rec
            print(f"  {sec['key']}: {min(start+PAGE, limit)}/{limit}", flush=True)

    out = {"site": site, "domain": prof.get("domain"), "synced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "pages": pages, "urls": urls,
           "stats": {"pages": len(pages), "urls": len(urls),
                     "with_cover": sum(1 for p in pages.values() if p["cover"]),
                     "with_media": sum(1 for p in pages.values() if p["media"])}}
    dst = LIB_ROOT / site / "assets.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False))
    print(json.dumps(out["stats"], ensure_ascii=False, indent=1))
    return out


# ─────────────────────────── plan ───────────────────────────
def _match(u, mode, pat, url_map):
    if url_map:
        return url_map.get(u)
    if mode == "exact":
        return None if u != pat else u
    if mode == "prefix":
        return None if not u.startswith(pat) else u
    if mode == "regex":
        return None if not re.search(pat, u) else u
    return None


def plan(site, mode="prefix", match="", url_map_path="", new_url="", new_alt="",
         section="", lang="", page_type="", slugs=""):
    inv = json.loads((LIB_ROOT / site / "assets.json").read_text())
    url_map = json.loads(Path(url_map_path).read_text()) if url_map_path else {}
    if url_map:
        mode, match = "url-map", "(file)"
    slug_set = {s.strip() for s in slugs.split(",") if s.strip()}
    items = []
    for did, p in inv["pages"].items():
        if section and p.get("section") != section:
            continue
        if lang and p.get("lang") != lang:
            continue
        if page_type and p.get("pageType") != page_type:
            continue
        if slug_set and p.get("slug") not in slug_set:
            continue
        if p.get("cover") and _match(p["cover"]["url"], mode, match, url_map):
            items.append({"doc_id": did, "kind": "cover", "idx": None,
                          "old": p["cover"]["url"], "alt": p["cover"]["alt"], "slug": p["slug"]})
        for m in p["media"]:
            if _match(m["src"], mode, match, url_map):
                items.append({"doc_id": did, "kind": "media", "idx": m["idx"], "field": m["field"],
                              "old": m["src"], "alt": m["alt"], "slug": p["slug"]})
    out = {"site": site, "mode": mode, "match": match, "new_url": new_url, "new_alt": new_alt,
           "filter": {"section": section, "lang": lang, "pageType": page_type, "slugs": sorted(slug_set)},
           "count": len(items), "docs": len({i["doc_id"] for i in items}), "items": items[:2000]}
    dst = LIB_ROOT / site / "replace-plan.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps({k: out[k] for k in ("mode", "match", "new_url", "count", "docs")}, ensure_ascii=False, indent=1))
    print(f"计划已写 {dst}")
    return out


# ─────────────────────────── apply ───────────────────────────
def apply(site, plan_path, dry_run=True, max_docs=500):
    prof = site_of(site)
    proj, ds = prof["source"]["project"], prof["source"]["dataset"]
    tok = token()
    pl = json.loads(Path(plan_path).read_text())
    new_url = pl.get("new_url") or ""
    new_alt = pl.get("new_alt") or ""
    by_doc = {}
    for it in pl["items"]:
        by_doc.setdefault(it["doc_id"], []).append(it)
    doc_ids = list(by_doc)[:max_docs]
    mutations, changed = [], 0
    for did in doc_ids:
        # 重取最新版本（防并发覆盖）
        fresh = query(proj, ds, f'*[_id=="{did}"][0]{{_id,_rev,cover,bodyJson,coverUrl}}', tok)
        if not fresh:
            continue
        items = by_doc[did]
        sets = {}
        if any(i["kind"] == "cover" for i in items):
            for i in items:
                if i["kind"] != "cover":
                    continue
                nu = new_url or i["old"]
                if "cover" in fresh and fresh["cover"]:
                    sets["cover.url"] = nu
                    if new_alt:
                        sets["cover.alt"] = new_alt
                else:
                    sets["coverUrl"] = nu
        media_items = [i for i in items if i["kind"] == "media"]
        if media_items and fresh.get("bodyJson"):
            try:
                arr = json.loads(fresh["bodyJson"])
                idx_map = {}
                for it in media_items:
                    idx_map.setdefault(it["idx"], []).append(it)
                for i, s in enumerate(arr):
                    for it in idx_map.get(i, []):
                        fld = it.get("field", "media")
                        m = s.get(fld)
                        if isinstance(m, dict) and m.get("src") == it["old"]:
                            m["src"] = new_url or it["old"]
                            if new_alt:
                                m["alt"] = new_alt
                        elif isinstance(m, str) and m == it["old"]:
                            s[fld] = new_url or it["old"]
                sets["bodyJson"] = json.dumps(arr, ensure_ascii=False)
            except Exception as e:
                print(f"  bodyJson 解析失败 {did}: {str(e)[:80]}", file=sys.stderr)
                continue
        if sets:
            mutations.append({"patch": {"id": did, "ifRevisionID": fresh.get("_rev"), "set": sets}})
        if len(mutations) >= BATCH:
            r = mutate(proj, ds, mutations, tok, dry_run=dry_run)
            changed += len(mutations)
            print(f"  提交 {len(mutations)} 个 patch（dry_run={dry_run}）: {json.dumps(r)[:160]}", flush=True)
            mutations = []
    if mutations:
        r = mutate(proj, ds, mutations, tok, dry_run=dry_run)
        changed += len(mutations)
        print(f"  提交 {len(mutations)} 个 patch（dry_run={dry_run}）: {json.dumps(r)[:160]}", flush=True)
    if not dry_run and changed:
        with open(ROOT / "run" / "approvals.log", "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} ASSET-PATCH site={site} docs={changed} "
                    f"match={pl.get('match')} new={new_url[:80]} plan={plan_path}\n")
    print(json.dumps({"ok": True, "dry_run": dry_run, "docs_patched": changed}, ensure_ascii=False))
    return {"ok": True, "dry_run": dry_run, "docs_patched": changed}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("scan")
    s1.add_argument("--site", default="lovart-global"); s1.add_argument("--sections", default="")
    s1.add_argument("--max", type=int, default=0)
    s2 = sub.add_parser("plan")
    s2.add_argument("--site", default="lovart-global"); s2.add_argument("--mode", default="prefix", choices=["exact", "prefix", "regex"])
    s2.add_argument("--match", default=""); s2.add_argument("--url-map", default="")
    s2.add_argument("--new-url", default=""); s2.add_argument("--new-alt", default="")
    s2.add_argument("--section", default=""); s2.add_argument("--lang", default="")
    s2.add_argument("--page-type", default=""); s2.add_argument("--slugs", default="")
    s3 = sub.add_parser("apply")
    s3.add_argument("--site", default="lovart-global"); s3.add_argument("--plan", required=True)
    s3.add_argument("--yes", action="store_true"); s3.add_argument("--max-docs", type=int, default=500)
    a = ap.parse_args()
    if a.cmd == "scan":
        scan(a.site, a.sections, a.max)
    elif a.cmd == "plan":
        plan(a.site, a.mode, a.match, a.url_map, a.new_url, a.new_alt, a.section, a.lang, a.page_type, a.slugs)
    else:
        apply(a.site, a.plan, dry_run=not a.yes, max_docs=a.max_docs)
