#!/usr/bin/env python3
from pathlib import Path
"""DataWorks 四周聚合 — W1:7/14-20 W2:7/21-27 W3:7/28-8/3 W4:8/4-10

按 pt 过滤 + 去重。输出 /tmp/dataworks_4w.json:
  每窗口: seo_geo(整体)/seo/geo × {uv, dau, new_uv(注册), new_pay_uv, new_pay_amt}
"""
import csv, json, os
from collections import defaultdict

DATAWORK_DIR = str(Path(__file__).resolve().parents[3] / "1-2 Insight/From Datawork")
WINDOWS = {
    "W1": {f"202607{d:02d}" for d in range(14, 21)},
    "W2": {f"202607{d:02d}" for d in range(21, 28)},
    "W3": {f"202607{d:02d}" for d in range(28, 32)} | {"20260801", "20260802", "20260803"},
    "W4": {f"202608{d:02d}" for d in range(4, 11)},
}

def safe_float(v):
    try: return float(v) if v and str(v).strip() else 0.0
    except: return 0.0

def load_unique():
    seen, out = set(), []
    for fname in os.listdir(DATAWORK_DIR):
        if not (fname.startswith("seo_geo_daily_report_") and fname.endswith(".csv")):
            continue
        with open(os.path.join(DATAWORK_DIR, fname)) as f:
            for r in csv.DictReader(f):
                key = (r["pt"], r.get("organic_discovery_type", "").strip(), r.get("referer_platform_hint", "").strip())
                if key not in seen:
                    seen.add(key)
                    out.append(r)
    return out

def agg(rows, dates):
    daily = {}  # pt -> {"seo_geo": {...}, "seo": {...}, "geo": {...}}
    for r in rows:
        pt = r["pt"]
        if pt not in dates:
            continue
        od = r.get("organic_discovery_type", "").strip()
        if od not in ("seo", "geo"):
            continue
        if pt not in daily:
            daily[pt] = {"seo_geo": {"uv": 0.0, "new_uv": 0.0, "pay_uv": 0.0, "pay_amt": 0.0, "dau": 0.0},
                         "seo": {"uv": 0.0, "new_uv": 0.0, "pay_uv": 0.0, "pay_amt": 0.0},
                         "geo": {"uv": 0.0, "new_uv": 0.0, "pay_uv": 0.0, "pay_amt": 0.0}}
        d = daily[pt]
        sg = d["seo_geo"]
        tgt = d[od]
        uv = safe_float(r.get("all_uv", 0))
        nu = safe_float(r.get("new_uv", 0))
        pu = safe_float(r.get("new_pay_uv", 0))
        pa = safe_float(r.get("new_pay_amount", 0))
        for store in (sg, tgt):
            store["uv"] += uv
            store["new_uv"] += nu
            store["pay_uv"] += pu
            store["pay_amt"] += pa
        sg["dau"] = max(sg["dau"], safe_float(r.get("total_dau_uv", 0)))
    return daily

def main():
    rows = load_unique()
    print(f"去重后行数: {len(rows)}")
    out = {}
    for wname, dates in WINDOWS.items():
        daily = agg(rows, dates)
        have = set(daily.keys())
        missing = dates - have
        print(f"[{wname}] 日期数={len(have)} 缺失={missing or '无'}")
        w = {}
        for bucket in ("seo_geo", "seo", "geo"):
            tot = {"uv": 0.0, "new_uv": 0.0, "pay_uv": 0.0, "pay_amt": 0.0, "dau": 0.0}
            for d in daily.values():
                b = d[bucket]
                for k in tot:
                    tot[k] += b.get(k, 0.0)
            n = len(daily)
            w[bucket] = {"days": n,
                         "totals": {k: round(v, 2) for k, v in tot.items()},
                         "daily_avg": {k: round(v / n, 2) for k, v in tot.items()}}
        out[wname] = w
        s = w["seo_geo"]
        print(f"  SEO+GEO 日均: UV={s['daily_avg']['uv']:,.0f} 注册={s['daily_avg']['new_uv']:,.0f} 付费UV={s['daily_avg']['pay_uv']:,.1f} 付费${s['daily_avg']['pay_amt']:,.0f} DAU={s['daily_avg']['dau']:,.0f}")
        print(f"  SEO 日均: UV={w['seo']['daily_avg']['uv']:,.0f} 注册={w['seo']['daily_avg']['new_uv']:,.0f} 付费UV={w['seo']['daily_avg']['pay_uv']:,.1f}")
        print(f"  GEO 日均: UV={w['geo']['daily_avg']['uv']:,.0f} 注册={w['geo']['daily_avg']['new_uv']:,.0f} 付费UV={w['geo']['daily_avg']['pay_uv']:,.1f}")
    json.dump(out, open("/tmp/dataworks_4w.json", "w"), ensure_ascii=False, indent=1)
    print("\nSaved /tmp/dataworks_4w.json")

if __name__ == "__main__":
    main()
