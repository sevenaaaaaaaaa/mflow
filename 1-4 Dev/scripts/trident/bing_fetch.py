#!/usr/bin/env python3
"""Bing Webmaster 全维度拉取 — 关键词 + 页面（周→月聚合）+ 爬虫 + 流量

GetQueryStats / GetPageStats 返回 QueryStats 记录，含 Date（**每周**快照，每周约 top100
词/页），字段 Query(=词或URL)/Clicks/Impressions/AvgImpressionPosition。按 (月,词) 聚合
即得**月度**关键词/页面（含曝光加权排名、自算 CTR、可做环比）。键名与 GSC 对齐。
"""
import json, sys
from pathlib import Path
import requests
import xml.etree.ElementTree as ET
from credential_paths import credential_file
from trident_paths import DATA_INGESTION_DIR

KEY = credential_file("api_key", "LOVART_BING_API_KEY_FILE").read_text().strip()
SITE = "https://www.lovart.ai/"
NS = "http://schemas.datacontract.org/2004/07/Microsoft.Bing.Webmaster.Api"
URL = f"https://www.bing.com/webmasterapi/api.svc/soap?apikey={KEY}"

def call(action, body_xml):
    soap = f'<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>{body_xml}</soap:Body></soap:Envelope>'
    r = requests.post(URL, data=soap, headers={
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': f'"{NS}/IWebmasterApi/{action}"'
    }, timeout=30)
    return r.status_code, r.text


def _query_records(xml_text):
    root = ET.fromstring(xml_text)
    out = []
    for el in root.iter():
        if el.tag.split('}')[-1] == 'QueryStats':
            out.append({c.tag.split('}')[-1]: c.text for c in el})
    return out


def _aggregate_monthly(records, key_name):
    monthly = {}
    alltime = {}

    def acc(store, k, cl, im, pos):
        e = store.setdefault(k, {"clicks": 0, "impr": 0, "posw": 0.0, "wsum": 0})
        e["clicks"] += cl
        e["impr"] += im
        if pos > 0 and im > 0:
            e["posw"] += pos * im
            e["wsum"] += im

    for r in records:
        date = r.get("Date") or ""
        k = r.get("Query") or ""
        if not date or not k:
            continue
        cl = int(r.get("Clicks") or 0)
        im = int(r.get("Impressions") or 0)
        try:
            pos = float(r.get("AvgImpressionPosition") or 0)
        except ValueError:
            pos = 0.0
        acc(monthly.setdefault(date[:7], {}), k, cl, im, pos)
        acc(alltime, k, cl, im, pos)

    def finalize(store):
        rows = []
        for k, e in store.items():
            ctr = round(e["clicks"] / e["impr"] * 100, 1) if e["impr"] else 0.0
            pos = round(e["posw"] / e["wsum"], 1) if e["wsum"] else 0.0
            rows.append({key_name: k, "clicks": e["clicks"], "impr": e["impr"], "ctr": ctr, "pos": pos})
        rows.sort(key=lambda x: x["clicks"], reverse=True)
        return rows

    return {mo: finalize(d) for mo, d in monthly.items()}, finalize(alltime)


results = {"_site": SITE, "_source": "Bing Webmaster API"}

# 1. Keywords (query×week → monthly)
print("🔑 Bing Keywords...")
code, body = call('GetQueryStats', f'<GetQueryStats xmlns="{NS}"><siteUrl>{SITE}</siteUrl></GetQueryStats>')
kw_recs = _query_records(body)
kw_monthly, kw_all = _aggregate_monthly(kw_recs, "q")
results["keywords_monthly"] = kw_monthly
results["keywords"] = kw_all
if kw_monthly:
    lm = sorted(kw_monthly)[-1]
    print(f"  {len(kw_recs)} 周×词 → {len(kw_monthly)} 月；最新月 {lm}: {len(kw_monthly[lm])} 词")

# 2. Pages (page×week → monthly)
print("📄 Bing Pages...")
code, body = call('GetPageStats', f'<GetPageStats xmlns="{NS}"><siteUrl>{SITE}</siteUrl></GetPageStats>')
pg_recs = _query_records(body)
pg_monthly, pg_all = _aggregate_monthly(pg_recs, "url")
results["pages_monthly"] = pg_monthly
results["pages"] = pg_all
if pg_monthly:
    lm = sorted(pg_monthly)[-1]
    print(f"  {len(pg_recs)} 周×页 → {len(pg_monthly)} 月；最新月 {lm}: {len(pg_monthly[lm])} 页")

# 3. Crawl stats (last 7 days + latest)
print("🕷 Bing Crawl...")
body = f'<GetCrawlStats xmlns="{NS}"><siteUrl>{SITE}</siteUrl></GetCrawlStats>'
code, body = call('GetCrawlStats', body)
root = ET.fromstring(body)
crawl = {}
daily = []
for elem in root.iter(f'{{{NS}}}CrawlStats'):
    entry = {}
    for child in elem:
        tag = child.tag.split('}')[-1]
        text = child.text
        if text:
            try: entry[tag] = int(text)
            except: entry[tag] = text
    if entry: daily.append(entry)
results["crawl_daily"] = daily
latest = daily[-1] if daily else {}
print(f"  Latest: InIndex={latest.get('InIndex','?')}, CrawledPages={latest.get('CrawledPages','?')}, Errors={latest.get('CrawlErrors','?')}")

# 4. Rank & traffic — DAILY series (≈13 个月)，可按月聚合（关键词/页面接口无日期参数，仅此接口可按月拆分）
print("📈 Bing Traffic (daily)...")
body = f'<GetRankAndTrafficStats xmlns="{NS}"><siteUrl>{SITE}</siteUrl></GetRankAndTrafficStats>'
code, body = call('GetRankAndTrafficStats', body)
root = ET.fromstring(body)
traffic_daily = []
for elem in root.iter():
    if elem.tag.split('}')[-1] in ('TrafficStats', 'RankAndTrafficStats'):
        d = {c.tag.split('}')[-1]: c.text for c in elem}
        if 'Date' in d and d['Date']:
            traffic_daily.append({
                "date": d['Date'][:10],
                "clicks": int(d.get('Clicks', 0) or 0),
                "impressions": int(d.get('Impressions', 0) or 0),
            })
traffic_daily.sort(key=lambda x: x['date'])
monthly = {}
for r in traffic_daily:
    mo = r['date'][:7]
    m = monthly.setdefault(mo, {"clicks": 0, "impressions": 0})
    m['clicks'] += r['clicks']
    m['impressions'] += r['impressions']
for mo, m in monthly.items():
    m['ctr'] = round(m['clicks'] / m['impressions'] * 100, 2) if m['impressions'] else 0.0
results["traffic_daily"] = traffic_daily
results["traffic_monthly"] = monthly
if monthly:
    last_mo = sorted(monthly)[-1]
    print(f"  {len(traffic_daily)} 天 / {len(monthly)} 月；最新 {last_mo}: {monthly[last_mo]['clicks']:,} 点击")

# Output
out = DATA_INGESTION_DIR
out.mkdir(parents=True, exist_ok=True)
(out / "bing-full.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"\n📁 {out}/bing-full.json")
