#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, gzip, urllib.request, urllib.parse, re
API = "https://o11tm2qe.api.sanity.io/v2024-01-01/data/query/production"
def groq(q):
    u = API + "?query=" + urllib.parse.quote(q)
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"Accept-Encoding": "gzip"}), timeout=60)
    raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip": raw = gzip.decompress(raw)
    return json.loads(raw.decode()).get("result")
comp = groq('*[_type=="compositePage"]{_id,"slug":slug.current,pageType,language,title}') or []
blog = groq('*[_type=="blog"]{_id,"slug":slug.current,language,title}') or []
def show(name, pat, pool, n=8):
    rx = re.compile(pat, re.I)
    hits = [d for d in pool if rx.search(d.get("slug") or "") or rx.search(d.get("title") or "")]
    print(f"-- {name}: {len(hits)}")
    for d in hits[:n]:
        print("   ", d.get("language"), "|", d.get("slug"), "|", (d.get("title") or "")[:60])
show("CINEMATIC", "cinematic", comp)
show("GRAPHIC DESIGN", r"graphic.design", comp)
show("LOGO DESIGN", r"logo.design", comp)
show("THUMBNAIL", "thumbnail", comp)
show("IMAGE TO VIDEO", r"image.to.video", comp)
show("MOCKUP", "mockup", comp)
show("DESIGN GEN", r"design.generator|design.agent", comp)
print("== ZH 平台/特点 ==")
zh = [d for d in comp + blog if (d.get("language") or "").startswith("zh") and ("平台" in (d.get("title") or "") or "特点" in (d.get("title") or ""))]
for d in zh[:8]:
    print("   ", d.get("language"), "|", d.get("slug"), "|", (d.get("title") or "")[:50])
show("LOVE", r"love", blog, 12)
show("BRANDING", r"branding", blog, 6)
show("PIKA", r"pika", blog, 6)
show("ARTIST", r"artist", blog, 8)