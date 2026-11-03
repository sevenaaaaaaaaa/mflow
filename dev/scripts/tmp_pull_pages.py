#!/usr/bin/env python3
"""tmp_pull_pages.py — 拉取全部 compositePage 轻量字段 + 首段 hero 变体（一次性排查脚本）。

输出: dev/scripts/tmp_pages.jsonl  每行一个文档:
  {_id, pageType, lang, slug, story, hero, title}
hero = bodyJson 首段 type（服务端 string::split 提取）
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJ, DS = "o11tm2qe", "production"
PAGE_SIZE = 100
OUT = Path(__file__).resolve().parent / "tmp_pages.jsonl"

SEP1 = '"type": "'
SEP2 = '"'

Q = '''*[_type=="compositePage" && !(_id in path("drafts.**"))] | order(_id asc) [$start...$end]{
  _id, pageType, language, title,
  "slug": slug.current, "story": storylineTemplate,
  "h": coalesce(string::split(coalesce(string::split(bodyJson, $sep1)[1], ""), $sep2)[0], "NONE")
}'''


def token():
    if os.environ.get("SANITY_TOKEN"):
        return os.environ["SANITY_TOKEN"]
    sec = ROOT / "run" / "secrets" / "sanity.json"
    if sec.exists():
        return json.loads(sec.read_text()).get("token", "")
    mac = Path.home() / ".config" / "sanity" / "config.json"
    return json.loads(mac.read_text()).get("authToken", "") if mac.exists() else ""


def query(q, params, tok):
    url = f"https://{PROJ}.api.sanity.io/v2024-01-01/data/query/{DS}"
    body = {"query": q, "params": params}
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read()).get("result")


def main():
    tok = token()
    total = query('count(*[_type=="compositePage" && !(_id in path("drafts.**"))])', {}, tok)
    print(f"total compositePage: {total}", flush=True)
    out, start, n = [], 0, 0
    while start < total:
        docs = query(Q, {"start": start, "end": start + PAGE_SIZE,
                         "sep1": SEP1, "sep2": SEP2}, tok) or []
        for d in docs:
            out.append({"_id": d["_id"], "pageType": d.get("pageType") or "(none)",
                        "lang": d.get("language") or "", "slug": d.get("slug") or "",
                        "story": d.get("story") or "", "hero": d.get("h") or "NONE",
                        "title": (d.get("title") or "")[:90]})
        n += len(docs)
        start += PAGE_SIZE
        print(f"  {start}/{total}", flush=True)
        if not docs:
            break
    OUT.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in out))
    print(f"written {n} docs -> {OUT}")


if __name__ == "__main__":
    main()
