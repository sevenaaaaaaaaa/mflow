#!/usr/bin/env python3
"""tmp_pull_gallery.py — 拉取全部 hero-gallery 页面的真实瓦片结构 → gallery-ledger.json

关键：hero-gallery 有两种真实形态
  - toolTiles (6 瓦，工具维度)  → 英文 landing 页
  - gallery   (12 瓦，行业维度) → 中文 zh-topic 页
同时每段还带 media（单张主图）。
"""
import json, urllib.request
from pathlib import Path

PROJ, DS = "o11tm2qe", "production"
PAGE = 8
OUT = Path(__file__).resolve().parent / "gallery-ledger.json"


def token():
    mac = Path.home() / ".config" / "sanity" / "config.json"
    return json.loads(mac.read_text()).get("authToken", "")


def q(query, params=None, timeout=180):
    url = f"https://{PROJ}.api.sanity.io/v2024-01-01/data/query/{DS}"
    body = {"query": query}
    if params:
        body["params"] = params
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    tok = token()
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read()).get("result")


def main():
    total = q('count(*[_type=="compositePage" && !(_id in path("drafts.**")) '
              '&& bodyJson match $pat])', {"pat": "hero-gallery"})
    print(f"hero-gallery 文档总数: {total}", flush=True)

    rows, seen, after = [], set(), ""
    pages_fetched = 0
    while True:
        docs = q('*[_type=="compositePage" && !(_id in path("drafts.**")) '
                 '&& bodyJson match $pat && _id > $after] | order(_id asc) [0...$n]{'
                 '_id, "slug": slug.current, "lang": language, "pt": pageType, '
                 '"bj": bodyJson, "story": storylineTemplate}',
                 {"pat": "hero-gallery", "after": after, "n": PAGE})
        if not docs:
            break
        for d in docs:
            after = d["_id"]
            pages_fetched += 1
            try:
                arr = json.loads(d["bj"])
            except Exception:
                continue
            if not isinstance(arr, list):
                continue
            for sec in arr:
                if not (isinstance(sec, dict) and sec.get("type") == "hero-gallery"):
                    continue
                tt = sec.get("toolTiles") or []
                gal = sec.get("gallery") or []
                items = tt if tt else gal
                kind = "toolTiles" if tt else ("gallery" if gal else "none")
                key = (d["slug"], d["lang"])
                if key in seen:
                    break
                seen.add(key)
                rows.append({
                    "_id": d["_id"], "slug": d["slug"], "lang": d["lang"],
                    "pageType": d["pt"], "story": d["story"] or "",
                    "tile_field": kind, "tile_count": len(items),
                    "has_media": bool(sec.get("media")),
                    "media": (sec.get("media") or {}).get("src", ""),
                    "title": (sec.get("title") or "")[:70],
                    "tiles": [{"label": it.get("label", ""),
                               "sublabel": it.get("sublabel", ""),
                               "img": (it.get("media") or {}).get("src") or it.get("img", "")}
                              for it in items],
                })
                break
        print(f"  fetched {pages_fetched}/{total}", flush=True)
        if pages_fetched >= total:
            break

    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n写入 {len(rows)} 条 → {OUT.name}")


if __name__ == "__main__":
    main()
