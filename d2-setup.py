#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主站 SEO 2日冲刺 D2 批次预置（2026-10-14 晚，无需本地次日发号施令）：
1) R1 geo修复重写批（2 项，草稿为源，先跑）
2) D2 重写批 A5-A8 / C1-C4（rewrite，只产草稿；composite 正文发布留人工审）
3) PT1-PT3 TDK field_patch 上线批（composite+blog，只改 title/description/seo.*，ifRevisionID+审计）
B3 长尾建页不预置（变体选词需人工定）；composite/blog 正文整体发布不预置（拍平/fm 保真风险）。
"""
import json, re, time, secrets, os, urllib.parse, urllib.request, gzip, pathlib, datetime

API = "https://o11tm2qe.api.sanity.io/v2024-01-01/data/query/production"
ROOT = pathlib.Path("/www/wwwroot/mflow")
BATCH_DIR = ROOT / "run/batch"
SRC = ROOT / "run/projects/main/content/src"
DRAFTS = ROOT / "run/projects/main/content"

def groq(q, params=None, tries=3):
    u = API + "?query=" + urllib.parse.quote(q)
    if params:
        u += "&" + urllib.parse.urlencode({("$" + k): json.dumps(v) for k, v in params.items()})
    last = None
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"Accept-Encoding": "gzip"}), timeout=120)
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip": raw = gzip.decompress(raw)
            return json.loads(raw.decode()).get("result")
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise RuntimeError(f"GROQ failed: {last}")

def comp_text(sections):
    parts = []
    def walk(o):
        if isinstance(o, str): parts.append(o); return
        if isinstance(o, dict):
            for k in ("title", "description", "body", "answer", "question", "label", "quote", "name", "subtitle"):
                v = o.get(k)
                if isinstance(v, str): parts.append(v)
                elif isinstance(v, list):
                    for x in v: walk(x)
            for v in o.values():
                if isinstance(v, (dict, list)): walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(sections); return re.sub(r"\s+", " ", " ".join(parts)).strip()

# ---------- 1) 站点索引 ----------
comp_idx = groq('*[_type=="compositePage"]{_id,"slug":slug.current,pageType,language,title}') or []
blog_idx = groq('*[_type=="blog"]{_id,"slug":slug.current,language,title,"cover":coverUrl,"cat":category._ref,"pub":publishedAt,"desc":description}') or []
comp_by_key = {}
for c in comp_idx:
    if c.get("slug"): comp_by_key[(c["slug"], c.get("language") or "en")] = c
blog_by_key = {}
for b in blog_idx:
    if b.get("slug"): blog_by_key[(b["slug"], b.get("language") or "en")] = b
print(f"[1] index: composite={len(comp_idx)} blog={len(blog_idx)}")

def find_comp(lang, slug):
    return comp_by_key.get((slug, lang))
def find_blog(lang, slug):
    return blog_by_key.get((slug, lang))

def doc_from_url(url):
    """https://www.lovart.ai/{lang}/features/xxx → doc（语言/别名回退）"""
    m = re.match(r"https://www\.lovart\.ai/(.+)", url or "")
    if not m: return None, None
    segs = [s for s in m.group(1).strip("/").split("/") if s]
    lang = "en"
    if segs and segs[0] in ("zh", "pt", "ru", "fr", "ja", "ko", "de", "es", "it", "zh-TW"):
        lang = segs[0]; segs = segs[1:]
    if not segs: return None, None
    kind, slug = segs[0], "/".join(segs[1:])
    if kind == "blog":
        d = find_blog(lang, slug) or next((b for (s2, l2), b in blog_by_key.items() if s2 == slug), None)
        return (d, "blog") if d else (None, None)
    pt = {"features": "feature", "tools": "tool", "topics": "topic", "solutions": "solution",
          "product": "product", "scenario": "scenario", "landing": "landing"}.get(kind)
    if pt:
        d = find_comp(lang, slug) or next((c for (s2, l2), c in comp_by_key.items() if s2 == slug), None)
        if d: return d, ("comp", d.get("pageType") or pt)
    return None, None

# ---------- 2) CTR 缺口映射 + GSC 补拉 ----------
gap = json.loads((ROOT / "run/main-audit/ctr-gap-pages.json").read_text(encoding="utf-8"))

GSC_EXTRA = ["image to video", "text to image", "background remover", "cinematic video",
             "ai thumbnail maker", "graphic design", "logo design", "motion control",
             "ai design generator", "ai mockup generator", "luma dream machine",
             "i love art", "love arts", "love ai", "branding ai", "pika", "freepik",
             "civitai red"]
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    TOK = ROOT / "dev/scripts/sentinel/gsc_credentials/gsc-token.json"
    _creds = Credentials.from_authorized_user_info(json.loads(TOK.read_text()),
                                                   ["https://www.googleapis.com/auth/webmasters.readonly"])
    _svc = build("searchconsole", "v1", credentials=_creds)
    n_rows = 0
    for q in GSC_EXTRA:
        try:
            _res = _svc.searchanalytics().query(siteUrl="https://www.lovart.ai/", body={
                "startDate": "2026-09-16", "endDate": "2026-10-14",
                "dimensions": ["query", "page"], "rowLimit": 50,
                "dimensionFilterGroups": [{"filters": [{"dimension": "query", "operator": "EQUALS",
                                                         "expression": q}]}]}).execute()
        except Exception:
            continue
        for row in (_res.get("rows") or []):
            keys = row.get("keys") or []
            if len(keys) < 2: continue
            page = keys[1]
            gap.setdefault(q, []).append({"page": page, "clicks": row.get("clicks", 0),
                                          "impr": row.get("impressions", 0), "pos": round(row.get("position", 0), 1)})
            n_rows += 1
        time.sleep(0.3)
    print(f"[2] GSC 补拉 ok（{n_rows} 行）")
except Exception as e:
    print(f"[2] GSC 补拉失败（回退 regex）: {str(e)[:120]}")

def best_page(key, exclude_slugs=()):
    """该查询的映射页列表（按曝光降序）"""
    rows = sorted(gap.get(key, []), key=lambda e: -(e.get("impr") or 0))
    return [e for e in rows if (e.get("page") or "").rstrip("/").rsplit("/", 1)[-1] not in exclude_slugs]

def resolve_query(key, exclude_slugs=(), fb_fn=None, fb_kind=None, fb_stats=None, prefer_lang=None):
    """GSC 映射优先（按曝光降序逐个尝试落档）；prefer_lang 时优先该语言承接页；fb_fn 回退"""
    langs = ("zh", "pt", "ru", "fr", "ja", "ko", "de", "es", "it", "zh-TW")
    def url_lang(u):
        m = re.match(r"https://www\.lovart\.ai/([^/]+)/", u or "")
        return m.group(1) if (m and m.group(1) in langs) else "en"
    rows = best_page(key, exclude_slugs)
    if prefer_lang:
        rows = sorted(rows, key=lambda e: 0 if url_lang(e.get("page")) == prefer_lang else 1)
    for e in rows:
        d, kind = doc_from_url(e.get("page"))
        if d:
            if prefer_lang and (d.get("language") or "en") != prefer_lang:
                continue
            return {"doc": d, "kind": kind, "entry": e}
    if fb_fn:
        d = fb_fn()
        if d:
            return {"doc": d, "kind": fb_kind or ("comp", comp_type_of(d)), "entry": fb_stats or {"page": "", "impr": "", "pos": ""}}
    return None

# ---------- 3) D2 车道定义 ----------
TODAY_IDS = {  # 今天 A1-A4/B1 已改的文档（分层：以草稿为源继续深化）
    "features-ai-image-generator-en", "features-remove-video-background-en",
    "ai-promotion-landing-page-generator-en", "zh-topic-video-thumbnail",
    "features-ai-video-generator-en", "features-text-to-video-ai-en",
    "21dd4b6c-e23a-4440-ae85-b234c9ca57ac", "features-ai-lip-sync-en",
    "tool-ai-ai-shorts-en", "features-ai-ugc-generator-en",
    "features-ai-commercial-photography-en",
    "freepik-ai-image-generator-review", "blog-artlist-ai-review-en",
    "blog-what-is-civitai-red-en", "5D7P1Ms8gETxHN6XPxtZwP",
    "blog-flora-ai-review-en", "f03e85f7-01fe-4459-b558-884e8c0a019c", "media-io-review",
}

def pt_of(comp_type):
    return {"feature": "lp-feature", "tool": "lp-tool", "topic": "lp-topic",
            "scenario": "lp-scenario", "solution": "lp-solution",
            "product": "lp-product", "landing": "lp-landing"}.get(comp_type, "lp-" + str(comp_type))

def comp_type_of(doc):
    return doc.get("pageType") or "tool"

# 重写指令模板
P0 = ("改页+内链：查询词「{kw}」流量增长中（{note}）——页面内容未完全承接词簇。"
      "按「对比表/使用步骤/FAQ」结构重写正文（保持 Lovart 产品事实），hub 内链 ≥3 条，"
      "seo.title/description 同步含关键词。")
RO = ("排名机会改页：查询词「{kw}」28天 {impr} 曝光、排名 {pos} 且点击快速增长（+{growth}%）——"
      "内容未完全承接词簇。按「对比表/使用步骤/FAQ」结构重写正文对准词簇（保持 Lovart 产品事实），"
      "hub 内链 ≥3 条，seo.title/description 含关键词。")
HW = ("整页改写（被竞品超越）：查询词「{kw}」当前排名 {pos}，被 {comp} 超越。全页重写："
      "与 {comp} 的诚实对比表（明确各自优劣）、使用步骤、FAQ，补 ≥6 个具体数据点与 3-5 条外部来源链接；"
      "Lovart 强项场景前置。不投放，只做自然排名。")
PU = ("推前改页：查询词「{kw}」28天 {impr} 曝光、排名 {pos}（目标进 Top5）。保持页面结构，"
      "重点：hub 内链 ≥3 条 + 内容刷新（补 2-3 个新数据点/案例），seo.title 微调含关键词。")
PR = ("保排名轻刷新：查询词「{kw}」自然排名 {pos}，对应投放已停、转自然承接。轻量刷新："
      "核实/补足内链 ≥2 条、补 1-2 个数据点，不改变整体结构与既有关键词布局。")
R1 = ("GEO 门禁修复重写：source 是上一轮改稿（未过 geo 门禁）。在其基础上修复："
      "1) 全文补数据点至 ≥6 个（百分比、价格、年份、统计——只用真实可查的产品数据，不编造）；"
      "2) 确保 ≥3 个非问句 H2 章节（超长章节拆为 H3/列表）；其余内容、结论与结构保留。")
LAYER = "\n\n注意：source 是上一轮改稿后的最新版（含已更新的标题/导语），在其基础上继续深化，不要回退已改进的部分。"

used = {}   # doc_id -> lane（去重）
lanes = []  # (lane_key, title, [item...])

def add_item(lane, doc, kind, kw, instr, lang=None, growth=None, impr=None, pos=None, note=""):
    did = doc["_id"]
    if did in used:
        print(f"    [dedupe] {kw} → {did} 已在 {used[did]}，跳过")
        return False
    used[did] = lane
    is_blog = (kind == "blog")
    ctype = "blog" if is_blog else pt_of(kind[1])
    lg = lang or doc.get("language") or "en"
    layered = did in TODAY_IDS
    if layered:
        src_path = f"run/projects/main/content/{did}.md"
        instr += LAYER
    else:
        src_path = None  # 稍后拉线上文
    item = {"item_id": did, "type": ctype, "lang": lg, "topic": kw,
            "instruction": instr, "source_path": src_path,
            "_src_path": src_path, "_layered": layered, "_doc": doc, "_kind": kind}
    lanes[-1][2].append(item)
    return True

def new_lane(key, title):
    lanes.append((key, title, []))

# --- A5 改页+内链（排名机会增长页，不在 CTR 映射里，按 slug/标题检索）---
new_lane("A5", "冲刺D2·A5 改页+内链（增长页 4）")
def find_by_regex(lang, pat, exclude=("video",), doc_type="comp", kw=""):
    rx = re.compile(pat, re.I)
    tokens = [t for t in re.split(r"[\s-]+", (kw or pat).lower()) if t]
    pool = comp_idx if doc_type == "comp" else blog_idx
    best, best_score = None, -1
    for d in pool:
        slug = (d.get("slug") or "").lower()
        if any(x in slug for x in exclude): continue
        if not (rx.search(slug) or rx.search(d.get("title") or "")): continue
        s = (2 if (d.get("language") or "en") == lang else 0)
        s += 4 * sum(1 for t in tokens if t in slug)
        s += (1 if rx.search(slug) else 0)
        s -= len(slug) * 0.01
        if s > best_score:
            best, best_score = d, s
    return best

A5_DEFS = [
    ("image to video", "+21.6%", r"image.to.video", ("text-to-video",), "comp"),
    ("text to image", "", r"text.to.image", (), "comp"),
    ("background remover", "", r"background.remover|remove.background", ("video",), "comp"),
    ("cinematic video", "", r"cinematic", (), "comp"),
]
for kw, g, pat, excl, dt in A5_DEFS:
    r = resolve_query(kw, prefer_lang="en", fb_fn=lambda p=pat, e2=excl, k2=kw: find_by_regex("en", p, e2, kw=k2),
                      fb_kind=("comp", "feature"), fb_stats={"impr": "", "pos": ""})
    if r:
        e = r["entry"]
        add_item("A5", r["doc"], r["kind"], kw, P0.format(kw=kw, note=g or "增长中"))
    else:
        print(f"    [unresolved] A5 {kw}")

# --- A6 排名机会① ---
new_lane("A6", "冲刺D2·A6 改页+内链（排名机会① 4）")
A6_DEFS = [("civitai red", "civitai", "+527"), ("freepik ai image generator", "freepik ai image generator", "+319"),
           ("freepik ai", "freepik ai", "+235"), ("artlist ai", "artlist ai", "+217")]
for kw, key, g in A6_DEFS:
    r = resolve_query(key)
    if r:
        e = r["entry"]
        add_item("A6", r["doc"], r["kind"], kw,
                 RO.format(kw=kw, impr=f"{e.get('impr')}", pos=f"{e.get('pos')}", growth=g), growth=g,
                 impr=e.get("impr"), pos=e.get("pos"))
    else:
        print(f"    [unresolved] A6 {kw}")

# --- A7 排名机会②（多语言） ---
new_lane("A7", "冲刺D2·A7 改页+内链（排名机会② 5）")
A7_DEFS = [("conversa com imagem", "conversa com imagem", "+141"),
           ("чат с изображениями", "чат с изображениями", "+125"),
           ("civitai.red", "civitai.red", "+102"), ("hedra ai", "hedra ai", "+82"), ("media io", "media io", "+50")]
for kw, key, g in A7_DEFS:
    r = resolve_query(key)
    if r:
        e = r["entry"]
        add_item("A7", r["doc"], r["kind"], kw,
                 RO.format(kw=kw, impr=f"{e.get('impr')}", pos=f"{e.get('pos')}", growth=g), growth=g,
                 impr=e.get("impr"), pos=e.get("pos"))
    else:
        print(f"    [unresolved] A7 {kw}")

# --- A8 被超越页整页改写① ---
new_lane("A8", "冲刺D2·A8 整页改写①（ai thumbnail maker）")
r8 = resolve_query("ai thumbnail maker", prefer_lang="en",
                   fb_fn=lambda: find_by_regex("en", r"thumbnail", (), kw="ai thumbnail maker"),
                   fb_kind=("comp", "feature"))
if r8:
    add_item("A8", r8["doc"], r8["kind"], "ai thumbnail maker",
             HW.format(kw="ai thumbnail maker", pos="24.3", comp="Canva"))
else:
    print("    [unresolved] A8 thumbnail")

# --- C1 推前 ---
new_lane("C1", "冲刺D2·C1 推前改页（4）")
C1_DEFS = [("Graphic Design", r"graphic.design", ()),
           ("Logo Design", r"logo.design", ()),
           ("Motion Control", r"motion.control", ()),
           ("AI Design Generator", r"design.generator|design.agent", ())]
for kw, pat, excl in C1_DEFS:
    r = resolve_query(kw, prefer_lang="en", fb_fn=lambda p=pat, e2=excl, k2=kw: find_by_regex("en", p, e2, kw=k2),
                      fb_kind=("comp", "feature"), fb_stats={"impr": "1.1k", "pos": "4-20"})
    if r:
        e = r["entry"]
        add_item("C1", r["doc"], r["kind"], kw, PU.format(kw=kw, impr=e.get("impr") or "1.1k", pos=e.get("pos") or "4-20"))
    else:
        print(f"    [unresolved] C1 {kw}")

# --- C2 被超越页整页改写② ---
new_lane("C2", "冲刺D2·C2 整页改写②（ai mockup generator）")
r2m = resolve_query("ai mockup generator", prefer_lang="en",
                    fb_fn=lambda: find_by_regex("en", r"mockup", (), kw="ai mockup generator"),
                    fb_kind=("comp", "tool"))
if r2m:
    add_item("C2", r2m["doc"], r2m["kind"], "ai mockup generator",
             HW.format(kw="ai mockup generator", pos="24.3", comp="Kittl"))
else:
    print("    [unresolved] C2 mockup")

# --- C3 交给自然·保排名 ---
new_lane("C3", "冲刺D2·C3 保排名轻刷新（5）")
C3_DEFS = [("luma dream machine", r"luma|dream machine"), ("branding ai", r"branding"), ("pika", r"pika")]
for kw, pat in C3_DEFS:
    r = resolve_query(kw, fb_fn=lambda p=pat, k2=kw: find_by_regex("en", p, (), doc_type="blog", kw=k2),
                      fb_kind="blog", fb_stats={"impr": "", "pos": "3.7-14.3"})
    if r:
        e = r["entry"]
        add_item("C3", r["doc"], r["kind"], kw, PR.format(kw=kw, pos=e.get("pos") or "3.7-14.3"))
    else:
        print(f"    [unresolved] C3 {kw}")

# --- C4 排名机会尾巴 ---
new_lane("C4", "冲刺D2·C4 排名机会尾巴（5）")
C4_DEFS = [("heygen", "heygen", "+86"), ("artist", "artist", "+73"),
           ("爱设计的平台特点", "爱设计的平台特点", "+68"), ("flora ai", "flora ai", "+65"),
           ("fil de discussion avec image", "fil de discussion avec image", "+62")]
for kw, key, g in C4_DEFS:
    r = resolve_query(key)
    if r:
        e = r["entry"]
        add_item("C4", r["doc"], r["kind"], kw,
                 RO.format(kw=kw, impr=f"{e.get('impr')}", pos=f"{e.get('pos')}", growth=g), growth=g,
                 impr=e.get("impr"), pos=e.get("pos"))
    else:
        print(f"    [unresolved] C4 {kw} | 映射页: {[x.get('page') for x in gap.get(key, [])][:3]}")

# ---------- 4) 拉未分层项的线上源文 ----------
def fetch_body(doc, kind):
    if kind == "blog":
        r = groq(f'*[_id=="{doc["_id"]}"]{{"t": pt::text(body)}}') or [{}]
        return (r[0].get("t") or "").strip()
    r = groq(f'*[_id=="{doc["_id"]}"]{{bodyJson}}') or [{}]
    try:
        return comp_text(json.loads(r[0].get("bodyJson") or ""))
    except Exception:
        return ""

SRC.mkdir(parents=True, exist_ok=True)
src_sizes = {}
for key, title, items in lanes:
    for it in items:
        if it["_layered"]:
            p = ROOT / it["_src_path"]
            if not p.exists():  # 草稿缺失 → 拉线上文
                it["_src_path"] = it["source_path"] = None; it["_layered"] = False
            else:
                src_sizes[it["item_id"]] = p.stat().st_size
                continue
        txt = fetch_body(it["_doc"], it["_kind"])
        sp = SRC / f"{it['item_id']}.md"
        sp.write_text(txt, encoding="utf-8")
        it["_src_path"] = it["source_path"] = f"run/projects/main/content/src/{it['item_id']}.md"
        src_sizes[it["item_id"]] = len(txt)
        time.sleep(0.4)
print(f"[4] sources: {len(src_sizes)}")

# ---------- 5) R1 geo修复批 ----------
geo_items = []
for did, ctype in [("tool-ai-ai-shorts-en", "lp-tool"), ("features-ai-ugc-generator-en", "lp-feature")]:
    dp = DRAFTS / f"{did}.md"
    geo_items.append({"item_id": did, "type": ctype, "lang": "en", "topic": did,
                      "instruction": R1, "source_path": f"run/projects/main/content/{did}.md"})
assert all((DRAFTS / (i["item_id"] + ".md")).exists() for i in geo_items), "R1 草稿缺失"
lanes.insert(0, ("R1", "冲刺D2·R1 geo修复重写（2）", geo_items))

# ---------- 6) 建批 ----------
def mk_batch(tid, ts, btype, title, items, params, concurrency=2):
    task = {"id": tid, "type": btype, "title": title,
            "created": ts, "created_by": "seveno", "dry_run": False, "important": True,
            "params": dict(params), "concurrency": concurrency, "status": "queued",
            "log": ["[setup] D2 预置批（2026-10-14 晚建，FIFO 自动执行）"],
            "items": [{"i": n, "status": "pending", "attempts": 0, "result": None, "error": "",
                       **{k: v for k, v in it.items() if not k.startswith("_")}}
                      for n, it in enumerate(items)],
            "stats": {"total": len(items), "done": 0, "failed": 0, "skipped": 0}}
    if os.environ.get("D2_DRYPLAN"):
        print(f"[DRYPLAN] would create {tid} | {title} | items={len(items)} | "
              + json.dumps([{k: it.get(k) for k in ("item_id", "type", "lang", "source_path")} for it in task["items"]],
                           ensure_ascii=False)[:400])
        return
    (BATCH_DIR / f"{tid}.json").write_text(json.dumps(task, ensure_ascii=False), encoding="utf-8")
    with open(ROOT / "run/approvals.log", "a") as f:
        f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} BATCH-CREATE {tid} type={btype} "
                f"items={len(items)} dry_run=False by=seveno sprint=D2\n")
    print(f"[6] created {tid} | {title} | items={len(items)}")

RP = {"batch_size": 5, "context_handoff": True, "fail_threshold": 5, "fatal_threshold": 2,
      "max_attempts": 2, "important": True}
ts_n = 0
def next_ts():
    global ts_n
    ts_n += 1
    return f"2026-10-14 22:{10 + ts_n:02d}"

exist = {json.loads(f.read_text(encoding="utf-8")).get("title", "")
         for f in BATCH_DIR.glob("batch-*.json") if f.stat().st_size < 200000}
for key, title, items in lanes:
    if not items:
        print(f"[6] skip {key}（无可用项）"); continue
    if title in exist:
        print(f"[6] skip {key}（已创建）"); continue
    # ≤5/批 拆分
    for bi in range(0, len(items), 5):
        chunk = items[bi:bi + 5]
        t = title if len(items) <= 5 else f"{title}·{bi // 5 + 1}"
        mk_batch(f"batch-261014-{secrets.token_hex(3)}", next_ts(), "rewrite", t, chunk, RP)

# ---------- 7) TDK field_patch 上线批 ----------
def clean(s, limit=None):
    s = re.sub(r"\[(待考证|TODO[^\]]*|FIXME|占位[^\]]*)\]", "", s or "").strip()
    if limit and len(s) > limit:
        cut = s[:limit]
        sp = cut.rfind(" ")
        if sp > limit * 0.6: cut = cut[:sp]
        s = cut.rstrip(" ,.:;、，。：；-—") 
    return s

def first_heading(md):
    for l in md.split("\n"):
        ls = l.strip()
        if ls.startswith("#"):
            return ls.lstrip("#").strip()
    return ""

def bold_line(md):
    for l in md.split("\n"):
        ls = l.strip()
        if ls.startswith("**") and ls.endswith("**") and len(ls) > 6:
            return ls.strip("*").strip()
    return ""

def first_para(md):
    for l in md.split("\n"):
        ls = l.strip()
        if ls and not ls.startswith(("#", "*", "-", "|", ">", "[")) and not ls.startswith("**"):
            return ls
    return ""

def strip_fm(md):
    if md.startswith("---"):
        parts = md.split("---", 2)
        return parts[2] if len(parts) >= 3 else md
    return md

comp_tdk_items, blog_tdk_items = [], []
# composite TDK（今天 A1/A2 的复合页）
for did in ["features-ai-image-generator-en", "features-remove-video-background-en",
            "ai-promotion-landing-page-generator-en", "zh-topic-video-thumbnail"]:
    dp = DRAFTS / f"{did}.md"
    if not dp.exists(): print(f"    [tdk-skip] {did}（无草稿）"); continue
    md = strip_fm(dp.read_text(encoding="utf-8"))
    t = clean(first_heading(md), 80); d = clean(bold_line(md) or first_para(md), 300); sd = clean(d, 160)
    if not t or not d: print(f"    [tdk-skip] {did}（title/desc 解析失败）"); continue
    doc = next((c for c in comp_idx if c["_id"] == did), None)
    if not doc: print(f"    [tdk-skip] {did}（CMS 无此文档）"); continue
    comp_tdk_items.append({"item_id": did, "doc_id": did, "lang": doc.get("language") or "en",
                           "set": {"title": t, "description": d, "seo.description": sd}})
# blog TDK（今天 A2/A3 的博客）
BLOG_DRAFTS = ["freepik-ai-image-generator-review", "blog-artlist-ai-review-en",
               "blog-what-is-civitai-red-en", "5D7P1Ms8gETxHN6XPxtZwP",
               "blog-flora-ai-review-en", "f03e85f7-01fe-4459-b558-884e8c0a019c", "media-io-review"]
for did in BLOG_DRAFTS:
    dp = DRAFTS / f"{did}.md"
    if not dp.exists(): print(f"    [tdk-skip] {did}（无草稿）"); continue
    md = strip_fm(dp.read_text(encoding="utf-8"))
    t = clean(first_heading(md), 120); d = clean(bold_line(md) or first_para(md), 200)
    sd = clean(d, 160); st = clean(first_heading(md), 70)
    if not t or not d: print(f"    [tdk-skip] {did}（title/desc 解析失败）"); continue
    # 定位真实 blog 文档
    doc = next((b for b in blog_idx if b["_id"] == did), None)
    if not doc:
        slug_guess = re.sub(r"^-blog-|-en$", "", did.replace("blog-", ""))
        for cand in {slug_guess, did.replace("blog-", "")}:
            doc = blog_by_key.get((cand, "en"))
            if doc: break
    if not doc: print(f"    [tdk-skip] {did}（CMS 定位失败）"); continue
    blog_tdk_items.append({"item_id": did, "doc_id": doc["_id"], "lang": doc.get("language") or "en",
                           "set": {"title": t, "description": d, "seoTitle": st, "seoDescription": sd}})

FP = {"max_attempts": 2, "important": True}
def create_fp(title, items, ts):
    if not items: print(f"[7] skip {title}（空）"); return
    for bi in range(0, len(items), 5):
        chunk = items[bi:bi + 5]
        t = title if len(items) <= 5 else f"{title}·{bi // 5 + 1}"
        mk_batch(f"batch-261014-{secrets.token_hex(3)}", ts(), "field_patch", t, chunk, FP)

create_fp("冲刺D2·PT1 复合页TDK上线（4）", comp_tdk_items, next_ts)
create_fp("冲刺D2·PT2 博客TDK上线（7）", blog_tdk_items, next_ts)

print("\n=== D2 预置完成 ===")
print("src sizes:", json.dumps(src_sizes, ensure_ascii=False)[:600])
print("comp TDK:", len(comp_tdk_items), "| blog TDK:", len(blog_tdk_items))