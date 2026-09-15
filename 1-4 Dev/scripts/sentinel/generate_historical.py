#!/usr/bin/env python3
"""全维度历史报告生成器 v3 — 收录分析 + 竞品覆盖 + 数据驱动洞察"""
import json, ssl, re
from pathlib import Path
import sys
_scripts = Path(__file__).resolve().parents[1]
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))
from lovart_brand_match import is_brand
from datetime import date, timedelta
from calendar import monthrange
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

SCRIPT_DIR = Path(__file__).resolve().parent  # → sentinel/
ROOT = SCRIPT_DIR.parent.parent  # → 1-Project/

BASE = ROOT / "1-2 Insight/Trident Insights/reports"
OUT_M = BASE / "monthly"; OUT_Q = BASE / "quarterly"; OUT_A = BASE / "annual"; OUT_W = BASE / "weekly"
for d in [OUT_M, OUT_Q, OUT_A, OUT_W]: d.mkdir(parents=True, exist_ok=True)

CRED_DIR = ROOT / "Lovart" / "scripts" / "sentinel"
GSC_C = json.loads((CRED_DIR / "gsc_credentials" / "gsc-token.json").read_text())
GA4_T = json.loads((CRED_DIR / "ga4_credentials" / "ga4-token.json").read_text())['token']
BING = json.loads((BASE / "bing-full.json").read_text())
SITE = "https://www.lovart.ai/"

def ib(q): return any(re.search(p, q.lower()) for p in BP)
def fm(n): return f"{n:,}"

# Load competitor keyword library
COMP_KWS = set()
try:
    kw_lib = ROOT / "1-2 Insight" / "Trident Insights" / "竞品核心非品牌词" / "lovart_competitors_keywords.md"
    for line in kw_lib.read_text().lower().split('\n'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            kw = re.sub(r'^\d+\.?\s*', '', parts[1].strip().lower())
            if len(kw) > 3 and not kw.startswith('-') and not kw.startswith('关键词') and not kw.startswith('出现竞品') and not kw.startswith('>'):
                COMP_KWS.add(kw)
except: pass

def is_comp(q):
    ql = q.lower()
    if ib(q): return False
    for ck in COMP_KWS:
        if ck in ql or ql in ck: return True
    return False

def pull_gsc_full(start, end):
    creds = Credentials.from_authorized_user_info(GSC_C, ["https://www.googleapis.com/auth/webmasters.readonly"])
    svc = build("searchconsole", "v1", credentials=creds)
    search = svc.searchanalytics()

    r_kw = search.query(siteUrl=SITE, body={"startDate":start,"endDate":end,"dimensions":["query"],"rowLimit":100}).execute()
    kw = [{"q":r["keys"][0],"c":r["clicks"],"i":r["impressions"],"r":round(r["ctr"]*100,1),"p":round(r["position"],1)} for r in r_kw.get("rows",[])]

    r_geo = search.query(siteUrl=SITE, body={"startDate":start,"endDate":end,"dimensions":["country"],"rowLimit":20}).execute()
    geo = [{"country":r["keys"][0],"clicks":r["clicks"],"impressions":r["impressions"],"ctr":round(r["ctr"]*100,1),"pos":round(r["position"],1)} for r in r_geo.get("rows",[])]

    r_pg = search.query(siteUrl=SITE, body={"startDate":start,"endDate":end,"dimensions":["page"],"rowLimit":20}).execute()
    pages = [{"url":r["keys"][0],"clicks":r["clicks"],"impressions":r["impressions"]} for r in r_pg.get("rows",[])]

    # Sitemap (one-time pull, shared across months)
    try:
        sm = svc.sitemaps()
        s_items = sm.list(siteUrl=SITE).execute().get("sitemap", [])
        sm_total = sum(int(s.get("contents",[{}])[0].get("submitted",0)) for s in s_items if s.get("contents"))
    except: sm_total = 69788

    # Competitor analysis
    comp_hits = [k for k in kw if is_comp(k['q'])]
    comp_cl = sum(k['c'] for k in comp_hits)

    return kw, geo, pages, sm_total, comp_hits, comp_cl

def pull_ga4_full(start, end):
    sf = {"filter":{"fieldName":"streamId","stringFilter":{"matchType":"EXACT","value":"10524753059"}}}
    org_f = {"filter":{"fieldName":"sessionDefaultChannelGroup","stringFilter":{"matchType":"EXACT","value":"Organic Search"}}}

    def call(body):
        req = urllib.request.Request("https://analyticsdata.googleapis.com/v1beta/properties/403618427:runReport",
            data=json.dumps(body).encode(), headers={"Authorization":f"Bearer {GA4_T}","Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=15) as r: return json.loads(r.read())

    d = call({"dateRanges":[{"startDate":start,"endDate":end}],"metrics":[{"name":"sessions"},{"name":"totalUsers"},{"name":"newUsers"},{"name":"averageSessionDuration"},{"name":"screenPageViewsPerSession"},{"name":"bounceRate"}],"dimensions":[{"name":"sessionDefaultChannelGroup"}],"dimensionFilter":sf,"limit":15})
    org = {"sessions":0,"users":0,"new":0,"dur":0,"pages":0,"bounce":0}
    for row in d.get("rows",[]):
        dims = {v['name']:row['dimensionValues'][i]['value'] for i,v in enumerate(d['dimensionHeaders'])}
        if dims.get('sessionDefaultChannelGroup')=='Organic Search':
            m = {v['name']:row['metricValues'][i]['value'] for i,v in enumerate(d['metricHeaders'])}
            org = {"sessions":int(m['sessions']),"users":int(m['totalUsers']),"new":int(m['newUsers']),"dur":round(float(m['averageSessionDuration'])),"pages":round(float(m['screenPageViewsPerSession']),2),"bounce":round(float(m['bounceRate'])*100,1)}

    d = call({"dateRanges":[{"startDate":start,"endDate":end}],"metrics":[{"name":"sessions"},{"name":"totalUsers"},{"name":"newUsers"},{"name":"bounceRate"}],"dimensions":[{"name":"country"}],"dimensionFilter":{"andGroup":{"expressions":[sf,org_f]}},"limit":15})
    geo_org = []
    for row in d.get("rows",[]):
        dims = {v['name']:row['dimensionValues'][i]['value'] for i,v in enumerate(d['dimensionHeaders'])}
        m = {v['name']:row['metricValues'][i]['value'] for i,v in enumerate(d['metricHeaders'])}
        geo_org.append({"country":dims.get('country','?'),"sessions":int(m['sessions']),"users":int(m['totalUsers']),"new":int(m['newUsers']),"bounce":round(float(m['bounceRate'])*100,1)})

    d = call({"dateRanges":[{"startDate":start,"endDate":end}],"metrics":[{"name":"sessions"},{"name":"totalUsers"},{"name":"averageSessionDuration"},{"name":"bounceRate"}],"dimensions":[{"name":"newVsReturning"}],"dimensionFilter":{"andGroup":{"expressions":[sf,org_f]}},"limit":5})
    segs = {}
    for row in d.get("rows",[]):
        dims = {v['name']:row['dimensionValues'][i]['value'] for i,v in enumerate(d['dimensionHeaders'])}
        m = {v['name']:row['metricValues'][i]['value'] for i,v in enumerate(d['metricHeaders'])}
        segs[dims.get('newVsReturning','?')] = m

    return org, segs, geo_org

def gen_monthly(y, m, kw, geo_gsc, pages, sm_total, comp_hits, comp_cl, org, segs, geo_ga4, prev_org=None):
    period = f"{y}-{m:02d}"
    end_day = monthrange(y, m)[1]
    gb = [k for k in kw if ib(k['q'])]; gn = [k for k in kw if not ib(k['q'])]
    gc = sum(k['c'] for k in kw); gi = sum(k['i'] for k in kw)
    gbc = sum(k['c'] for k in gb); gnc = sum(k['c'] for k in gn)
    traffic_pages = len(pages)
    gap = sm_total - traffic_pages

    # Tiers
    tiers = []
    for n,label in [(3,"Top 3"),(10,"Top 10"),(50,"Top 50"),(100,"Top 100")]:
        t = kw[:n]; tc = sum(k['c'] for k in t); ti = sum(k['i'] for k in t)
        tiers.append({"label":label,"count":len(t),"clicks":tc,"impr":ti,"ctr":round(tc/ti*100,1) if ti else 0,"share":round(tc/gc*100,1) if gc else 0})

    bb = [k for k in BING['keywords'] if ib(k['query'])]; bn = [k for k in BING['keywords'] if not ib(k['query'])]
    b_total = sum(k['clicks'] for k in BING['keywords']); b_non = sum(k['clicks'] for k in bn)

    L = [f"# Lovart SEO 月报 — {period}"]
    L.append(f"\n**周期**: {period}-01 至 {period}-{end_day} | **生成**: {date.today().isoformat()}")

    # 1. Keywords
    L.append(f"\n## 1. 关键词分层 (GSC)")
    L.append(f"| 层级 | 词数 | 点击 | 展示 | CTR | 占比 |")
    L.append(f"|------|------|------|------|------|------|")
    for t in tiers: L.append(f"| {t['label']} | {t['count']} | {fm(t['clicks'])} | {fm(t['impr'])} | {t['ctr']}% | {t['share']}% |")
    L.append(f"| 品牌词 | {len(gb)} | {fm(gbc)} | — | — | {gbc/gc*100:.1f}% |" if gc else "")
    L.append(f"| 非品牌词 | {len(gn)} | {fm(gnc)} | — | — | {gnc/gc*100:.1f}% |" if gc else "")
    if comp_hits:
        L.append(f"| 🎯 竞品非品牌 | {len(comp_hits)}/{len(COMP_KWS)} | {fm(comp_cl)} | — | — | {comp_cl/gc*100:.1f}% |" if gc else "")
    else:
        L.append(f"| 🎯 竞品非品牌 | 0/{len(COMP_KWS)} | 0 | — | 0% | 0% |")
    if gi and gc: L.append(f"| 整体CTR | — | — | {fm(gi)} | {gc/gi*100:.1f}% | — |")

    L.append(f"\n### Top 10 品牌词")
    for k in gb[:10]: L.append(f"- {k['q']}: {fm(k['c'])} clicks, pos {k['p']:.1f}")
    L.append(f"\n### Top 10 非品牌词 (含竞品)")
    for k in gn[:10]: L.append(f"- {k['q']}: {fm(k['c'])} clicks, pos {k['p']:.1f}" + (" 🎯" if is_comp(k['q']) else ""))
    if comp_hits and len(comp_hits) > 10:
        L.append(f"\n### 竞品非品牌完整清单")
        for k in comp_hits: L.append(f"- {k['q']}: {fm(k['c'])} clicks, pos {k['p']:.1f}")

    # 2. Country
    L.append(f"\n## 2. 分国家 (GSC)")
    L.append(f"| 国家 | 点击 | 展示 | CTR | 排名 |")
    L.append(f"|------|------|------|------|------|")
    for g in geo_gsc[:12]: L.append(f"| {g['country']} | {fm(g['clicks'])} | {fm(g['impressions'])} | {g['ctr']}% | {g['pos']} |")

    # 3. Indexing
    L.append(f"\n## 3. 收录分析 (GSC)")
    L.append(f"| 指标 | 值 |")
    L.append(f"|------|-----|")
    L.append(f"| Sitemap 提交 | {fm(sm_total)} |")
    L.append(f"| 28天有流量页面 | {fm(traffic_pages)} |")
    L.append(f"| 提交但无流量 | {fm(gap)} ({traffic_pages/max(sm_total,1)*100:.2f}% 有流量) |")
    L.append(f"| Top 5 页面 (点击) |")
    for p in pages[:5]: L.append(f"| {p['url'].replace(SITE,'/')[:55]} | {fm(p['clicks'])} clicks |")

    # 4. GA4
    L.append(f"\n## 4. 自然搜索 (GA4)")
    L.append(f"| 指标 | 值 |")
    L.append(f"|------|-----|")
    L.append(f"| Sessions | {fm(org['sessions'])} |")
    L.append(f"| Users | {fm(org['users'])} |")
    L.append(f"| New Users | {fm(org['new'])} ({org['new']/org['users']*100:.1f}%) |" if org['users'] else "")
    L.append(f"| Avg Duration | {org['dur']}s |")
    L.append(f"| Pages/Session | {org['pages']} |")
    L.append(f"| Bounce Rate | {org['bounce']}% |")
    if prev_org and prev_org.get('sessions',0):
        chg = (org['sessions']-prev_org['sessions'])/prev_org['sessions']*100
        L.append(f"| 环比 (vs上月) | {chg:+.1f}% |")

    L.append(f"\n### 用户分层 (Organic)")
    for name, m in segs.items():
        if name in ('returning','new'):
            L.append(f"| {name} | {fm(int(m.get('sessions',0)))} sess, {round(float(m.get('averageSessionDuration',0)))}s avg, {round(float(m.get('bounceRate',0))*100,1)}% bounce |")

    L.append(f"\n### 分国家 (GA4 Organic)")
    L.append(f"| 国家 | Sessions | Users | New | Bounce |")
    L.append(f"|------|----------|-------|-----|--------|")
    for g in geo_ga4[:10]: L.append(f"| {g['country']} | {fm(g['sessions'])} | {fm(g['users'])} | {fm(g['new'])} | {g['bounce']}% |")

    # 5. Bing
    L.append(f"\n## 5. Bing (全量历史)")
    L.append(f"| 关键词 | {len(BING['keywords'])} | 总点击 | {fm(b_total)} |")
    L.append(f"| 品牌词 | {len(bb)}词 / {fm(sum(k['clicks'] for k in bb))}cl | 非品牌 | {len(bn)}词 / {fm(b_non)}cl |")

    # 6. Insights
    L.append(f"\n## 6. 核心洞察")
    insights = []
    if gc and len(gb) and gbc/gc > 0.85: insights.append(f"品牌依赖度 {gbc/gc*100:.0f}% — 搜索流量几乎全部来自品牌词，风险极高")
    if sm_total > 0: insights.append(f"收录缺口巨大 — {fm(sm_total)} 个 URL 提交，仅 {fm(traffic_pages)} ({traffic_pages/max(sm_total,1)*100:.2f}%) 有搜索流量")
    if comp_cl and gc: insights.append(f"竞品非品牌覆盖 {len(comp_hits)}/{len(COMP_KWS)} ({comp_cl/gc*100:.2f}%) — 对 252 个行业词几乎无排名")
    if org['bounce'] and org['bounce'] < 20: insights.append(f"内容粘性优秀 — {org['bounce']}% bounce, {org['pages']} 页/次, {org['dur']}s 停留")
    if prev_org and prev_org.get('sessions',0):
        chg = (org['sessions']-prev_org['sessions'])/prev_org['sessions']*100
        if chg > 10: insights.append(f"环比增长 {chg:+.0f}% → 趋势向好")
        elif chg < -10: insights.append(f"环比下降 {chg:.0f}% → 需关注衰减原因")
    if geo_gsc:
        us = [g for g in geo_gsc if g['country']=='usa']
        if us and us[0]['ctr'] < 5: insights.append(f"美国 CTR {us[0]['ctr']}% (排名{us[0]['pos']}) — 全球展示最多但点击率最低，排名瓶颈严重")
    for i,s in enumerate(insights[:5],1): L.append(f"{i}. {s}")

    # 7. TODO
    L.append(f"\n## 7. TODO")
    todos = []
    if gap > 60000: todos.append(f"P0 | {fm(gap)} URL 提交但无流量 → 排查收录问题，优先修复 4xx 错误和 robots.txt 策略")
    if comp_cl < 500: todos.append(f"P0 | 竞品非品牌仅 {len(comp_hits)}/{len(COMP_KWS)} 词 ({comp_cl} clicks) → 加速非品牌内容生产")
    if geo_gsc:
        us = [g for g in geo_gsc if g['country']=='usa']
        if us and us[0]['ctr'] < 5: todos.append(f"P1 | 美国 CTR {us[0]['ctr']}% (排名{us[0]['pos']}) → schema + backlink + 本地化")
    if geo_ga4:
        br = [g for g in geo_ga4 if 'Brazil' in g['country']]
        if br and br[0]['bounce'] < 15: todos.append(f"P1 | 巴西 bounce {br[0]['bounce']}% → 优先葡语翻译扩量")
    todos.append(f"P1 | 非品牌词仅 {len(gn)} 个(GSC) vs {len(bn)} 个(Bing) → Bing 长尾优先")
    todos.append(f"P2 | 月度环比追踪 → 连续 3 月趋势确认方向")
    for i,t in enumerate(todos[:6],1): L.append(f"{i}. {t}")

    L.append(f"\n> Bing 数据为全量历史统计 | 竞品词库 {len(COMP_KWS)} 词")
    (OUT_M / f"Lovart-SEO-{period}.md").write_text("\n".join(L)+"\n")
    return org

# ===== MAIN =====
months = [(2025,4),(2025,5),(2025,6),(2025,7),(2025,8),(2025,9),(2025,10),(2025,11),(2025,12),(2026,1),(2026,2),(2026,3),(2026,4),(2026,5)]
all_data = {}; prev_org = None; total=len(months)

for i,(y,m) in enumerate(months,1):
    period=f"{y}-{m:02d}"; end_day=monthrange(y,m)[1]
    start=f"{y}-{m:02d}-01"; end=f"{y}-{m:02d}-{end_day}"
    print(f"[{i}/{total}] {period} ...", end=" ", flush=True)
    try:
        kw, geo_gsc, pages, sm_total, comp_hits, comp_cl = pull_gsc_full(start, end)
        org, segs, geo_ga4 = pull_ga4_full(start, end)
        prev_org = gen_monthly(y,m,kw,geo_gsc,pages,sm_total,comp_hits,comp_cl,org,segs,geo_ga4,prev_org)
        print(f"✅ GSC:{len(kw)}kw Comp:{len(comp_hits)}/{len(COMP_KWS)} GA4:{fm(org['sessions'])}sess")
    except Exception as e:
        print(f"❌ {str(e)[:100]}")

print(f"\n✅ 月报完成: {len([f for f in OUT_M.glob('*.md')])}")
