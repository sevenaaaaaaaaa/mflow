#!/usr/bin/env python3
"""tmp_pull_sections.py — 拉取全站页面所有 section 类型与图片来源位 → sections-ledger.json

产出：
  stats:  每个 section type 的页面数 / 图片位总数
  detail: 逐 type 的字段路径、每页平均图数
"""
import json, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

PROJ, DS = "o11tm2qe", "production"
PAGE = 40
OUT = Path(__file__).resolve().parent / "sections-ledger.json"

def token():
    return json.loads((Path.home() / ".config" / "sanity" / "config.json").read_text()).get("authToken", "")

def q(query, params=None, timeout=180):
    url = f"https://{PROJ}.api.sanity.io/v2024-01-01/data/query/{DS}"
    body = {"query": query}
    if params:
        body["params"] = params
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {token()}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read()).get("result")

def find_media_paths(node, prefix, out):
    """递归找出所有带 src 的 media 对象及字符串形式的图片 URL"""
    if isinstance(node, dict):
        if isinstance(node.get("src"), str) and node["src"].startswith("http"):
            out.append(prefix + ".src")
        if isinstance(node.get("img"), str) and node["img"].startswith("http"):
            out.append(prefix + ".img")
        if isinstance(node.get("image_url"), str) and node["image_url"].startswith("http"):
            out.append(prefix + ".image_url")
        for k, v in node.items():
            if k in ("src", "img", "image_url"):
                continue
            find_media_paths(v, f"{prefix}.{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            find_media_paths(v, f"{prefix}[{i}]", out)

def main():
    total = q('count(*[_type=="compositePage" && !(_id in path("drafts.**"))])')
    print(f"compositePage 总数: {total}", flush=True)

    sec_pages = Counter()          # type -> 出现该 type 的页面数
    sec_imgs = Counter()           # type -> 图片位总数
    sec_field = defaultdict(Counter)   # type -> 字段路径计数
    sec_pageset = defaultdict(set)     # type -> 页面（slug）集合
    sec_imgset = defaultdict(set)      # type -> 去重后 URL 集合
    after, n = "", 0

    while True:
        docs = q('*[_type=="compositePage" && !(_id in path("drafts.**")) && _id > $after]'
                 ' | order(_id asc)[0...$n]{_id,"slug":slug.current,"bj":bodyJson}',
                 {"after": after, "n": PAGE})
        if not docs:
            break
        for d in docs:
            after = d["_id"]
            n += 1
            try:
                arr = json.loads(d["bj"])
            except Exception:
                continue
            if not isinstance(arr, list):
                continue
            for s in arr:
                if not isinstance(s, dict):
                    continue
                t = s.get("type") or "(no-type)"
                paths = []
                find_media_paths(s, t, paths)
                if paths:
                    sec_pages[t] += 1
                    sec_pageset[t].add(d["slug"] or d["_id"])
                    sec_imgs[t] += len(paths)
                    for p in paths:
                        key = p.split("[")[0] if "[" not in p else p.split("[")[0]
                        sec_field[t][key] += 1
                        # 记录 URL 去重
                        cur = s
                        for tok in p.split("."):
                            pass
                else:
                    sec_pagesettmp = None
                    sec_pages.setdefault(t, sec_pages.get(t, 0))
        print(f"  {n}/{total}", flush=True)
        if n >= total:
            break

    out = {
        "totalDocs": total,
        "byType": {t: {"pages": sec_pages[t], "images": sec_imgs[t],
                       "fields": dict(sec_field[t].most_common(8))}
                   for t in sorted(sec_imgs, key=lambda x: -sec_imgs[x])},
        "noImageTypes": sorted({t for t in sec_pages if t not in sec_imgs}),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n写入 {OUT.name}")

if __name__ == "__main__":
    main()
