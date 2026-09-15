#!/usr/bin/env python3
from pathlib import Path
"""DataWorks 双窗口聚合 — cur=2026-08-12..08-18 vs prev=2026-08-05..08-11

按 pt 过滤 + (pt, organic_discovery_type, referer_platform_hint) 去重。
输出: /tmp/dataworks_windows.json
"""
import csv, json, os
from collections import defaultdict

DATAWORK_DIR = str(Path(__file__).resolve().parents[3] / "1-2 Insight/From Datawork")
WINDOWS = {
    "cur": {"20260812", "20260813", "20260814", "20260815", "20260816", "20260817", "20260818"},
    "prev": {"20260805", "20260806", "20260807", "20260808", "20260809", "20260810", "20260811"},
}

def safe_float(v):
    try: return float(v) if v and str(v).strip() else 0.0
    except: return 0.0

def load():
    all_rows = []
    for fname in os.listdir(DATAWORK_DIR):
        if not (fname.startswith("seo_geo_daily_report_") and fname.endswith(".csv")):
            continue
        with open(os.path.join(DATAWORK_DIR, fname)) as f:
            for r in csv.DictReader(f):
                all_rows.append(r)
    # 去重
    seen = set()
    unique = []
    for r in all_rows:
        key = (r["pt"], r.get("organic_discovery_type", "").strip(), r.get("referer_platform_hint", "").strip())
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

def agg(rows, dates):
    daily = {}
    for r in rows:
        pt = r["pt"]
        if pt not in dates:
            continue
        od = r.get("organic_discovery_type", "").strip()
        ch = r.get("referer_platform_hint", "").strip() or "direct"
        if pt not in daily:
            daily[pt] = {"uv": 0.0, "dau": 0.0, "new_pay_uv": 0.0, "new_pay_amt": 0.0,
                         "new_uv": 0.0, "platform_new_uv": 0.0, "platform_dau": 0.0,
                         "channels": defaultdict(lambda: {"uv": 0.0, "new_pay_uv": 0.0, "new_pay_amt": 0.0, "new_uv": 0.0})}
        d = daily[pt]
        d["platform_new_uv"] = max(d["platform_new_uv"], safe_float(r.get("total_new_uv", 0)))
        d["platform_dau"] = max(d["platform_dau"], safe_float(r.get("total_dau_uv", 0)))
        uv = safe_float(r.get("all_uv", 0))
        new_uv = safe_float(r.get("new_uv", 0))
        pay_uv = safe_float(r.get("new_pay_uv", 0))
        pay_amt = safe_float(r.get("new_pay_amount", 0))
        dau = safe_float(r.get("total_dau_uv", 0))
        if od in ("seo", "geo"):
            d["uv"] += uv
            d["new_uv"] += new_uv
            d["new_pay_uv"] += pay_uv
            d["new_pay_amt"] += pay_amt
            d["dau"] = max(d["dau"], dau)  # total_dau_uv 是平台级字段，取 max
            c = d["channels"][ch]
            c["uv"] += uv
            c["new_uv"] += new_uv
            c["new_pay_uv"] += pay_uv
            c["new_pay_amt"] += pay_amt
    return daily

def summarize(daily, label):
    n = len(daily)
    tot = defaultdict(float)
    for d in daily.values():
        for k in ("uv", "dau", "new_uv", "new_pay_uv", "new_pay_amt", "platform_new_uv", "platform_dau"):
            tot[k] += d[k]
    return {"days": n, "totals": {k: round(v, 2) for k, v in tot.items()},
            "daily_avg": {k: round(v / n, 2) for k, v in tot.items()}}

def main():
    rows = load()
    print(f"去重后总行数: {len(rows)}")
    out = {}
    for wname, dates in WINDOWS.items():
        daily = agg(rows, dates)
        # 验证天数完整
        have = set(daily.keys())
        missing = dates - have
        print(f"[{wname}] 日期数={len(have)} 缺失={missing or '无'}")
        # 渠道聚合 (SEO+GEO)
        channels = defaultdict(lambda: {"uv": 0.0, "new_pay_uv": 0.0, "new_pay_amt": 0.0, "new_uv": 0.0})
        for d in daily.values():
            for ch, c in d["channels"].items():
                channels[ch]["uv"] += c["uv"]
                channels[ch]["new_pay_uv"] += c["new_pay_uv"]
                channels[ch]["new_pay_amt"] += c["new_pay_amt"]
                channels[ch]["new_uv"] += c["new_uv"]
        out[wname] = {"daily": daily, "summary": summarize(daily, wname),
                      "channels": {k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in sorted(channels.items(), key=lambda x: -x[1]["uv"])}}
        s = out[wname]["summary"]
        print(f"  日均 UV={s['daily_avg']['uv']:,.0f} DAU={s['daily_avg']['dau']:,.0f} new_uv={s['daily_avg']['new_uv']:,.0f} pay_uv={s['daily_avg']['new_pay_uv']:,.1f} pay_amt=${s['daily_avg']['new_pay_amt']:,.0f}")
    json.dump(out, open("/tmp/dataworks_windows.json", "w"), ensure_ascii=False, indent=1)
    print("\nSaved /tmp/dataworks_windows.json")

if __name__ == "__main__":
    main()
