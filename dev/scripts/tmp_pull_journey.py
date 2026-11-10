#!/usr/bin/env python3
"""tmp_pull_journey.py — 拉取全部 hero-journey 页面的 steps 与 media → journey-ledger.json"""
import json, urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "journey-ledger.json"

def token():
    return json.loads((Path.home() / ".config/sanity/config.json").read_text()).get("authToken", "")

def q(query, params=None):
    url = "https://o11tm2qe.api.sanity.io/v2024-01-01/data/query/production"
    body = {"query": query}
    if params:
        body["params"] = params
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {token()}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())["result"]

def main():
    total = q('count(*[_type=="compositePage" && !(_id in path("drafts.**")) && bodyJson match $p])',
              {"p": "hero-journey"})
    print(f"含 hero-journey 文档: {total}")
    rows, seen, after = [], set(), ""
    while True:
        docs = q('*[_type=="compositePage" && !(_id in path("drafts.**")) && bodyJson match $p '
                 '&& _id > $after] | order(_id asc)[0...8]{_id,"slug":slug.current,"lang":language,'
                 '"pt":pageType,"bj":bodyJson}', {"p": "hero-journey", "after": after})
        if not docs:
            break
        for d in docs:
            after = d["_id"]
            try:
                arr = json.loads(d["bj"])
            except Exception:
                continue
            for sec in arr:
                if not (isinstance(sec, dict) and sec.get("type") == "hero-journey"):
                    continue
                key = (d["slug"], d["lang"])
                if key in seen:
                    break
                seen.add(key)
                steps = sec.get("steps") or sec.get("journeyCards") or []
                m = sec.get("media") or {}
                rows.append({
                    "_id": d["_id"], "slug": d["slug"], "lang": d["lang"], "pageType": d["pt"],
                    "title": (sec.get("title") or "")[:80],
                    "step_count": len(steps),
                    "steps": [{"title": s.get("title", ""), "icon": s.get("icon", "")} for s in steps],
                    "has_media": bool(m.get("src")),
                    "media": m.get("src", ""),
                    "media_alt": m.get("alt", ""),
                })
                break
        print(f"  {len(rows)} 页", flush=True)
        if len(rows) >= total:
            break
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n写入 {len(rows)} 条 → {OUT.name}")

if __name__ == "__main__":
    main()
