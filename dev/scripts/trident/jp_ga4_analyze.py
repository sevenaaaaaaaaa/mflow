#!/usr/bin/env python3
"""GA4 日本深挖分析 — 月度总量/渠道/设备/新老/质量/来源/事件/城市 + 全球对照。

产出: /tmp/jp_pull/jp_ga4_analysis.json + stdout 速览
"""
import json
from pathlib import Path
from collections import defaultdict

OUT = Path("/tmp/jp_pull")
D = json.loads((OUT / "ga4_jp_deep.json").read_text())
A = {}

def mk(datestr):
    s = datestr.replace("-", "")
    return f"{s[:4]}-{s[4:6]}"

# ───────────── 1. JP 月度总量（全渠道） ─────────────
daily = D["jp_daily"]
months = sorted({mk(r["d"]) for r in daily})
monthly = []
for mo in months:
    rows = [r for r in daily if mk(r["d"]) == mo]
    n = len(rows)
    tot = {k: 0 for k in ("sessions", "totalUsers", "newUsers", "engagedSessions", "eventCount", "screenPageViews")}
    for r in rows:
        for k in tot:
            tot[k] += r["m"][k]
    eng = sum(r["m"]["engagementRate"] * r["m"]["sessions"] for r in rows)
    bnc = sum(r["m"]["bounceRate"] * r["m"]["sessions"] for r in rows)
    dur = sum(r["m"]["averageSessionDuration"] * r["m"]["sessions"] for r in rows)
    pps = sum(r["m"]["screenPageViewsPerSession"] * r["m"]["sessions"] for r in rows)
    s = tot["sessions"]
    monthly.append({
        "mo": mo, "days": n,
        "sessions": s, "users": tot["totalUsers"], "new": tot["newUsers"],
        "engaged": tot["engagedSessions"],
        "engagement_rate": round(eng / s * 100, 1) if s else 0,
        "bounce": round(bnc / s * 100, 1) if s else 0,
        "dur_sec": round(dur / s) if s else 0,
        "pps": round(pps / s, 2) if s else 0,
        "events": tot["eventCount"], "pageviews": tot["screenPageViews"],
        "new_share": round(tot["newUsers"] / tot["totalUsers"] * 100, 1) if tot["totalUsers"] else 0,
    })
A["monthly"] = monthly

# 全球对照月度（全渠道）
wd = D["world_daily"]
w_months = sorted({mk(r["d"]) for r in wd})
world = []
for mo in w_months:
    rows = [r for r in wd if mk(r["d"]) == mo]
    s = sum(r["m"]["sessions"] for r in rows)
    u = sum(r["m"]["totalUsers"] for r in rows)
    eng = sum(r["m"]["engagementRate"] * r["m"]["sessions"] for r in rows)
    bnc = sum(r["m"]["bounceRate"] * r["m"]["sessions"] for r in rows)
    dur = sum(r["m"]["averageSessionDuration"] * r["m"]["sessions"] for r in rows)
    world.append({"mo": mo, "sessions": s, "users": u,
                  "engagement_rate": round(eng / s * 100, 1) if s else 0,
                  "bounce": round(bnc / s * 100, 1) if s else 0,
                  "dur_sec": round(dur / s) if s else 0})
A["world_monthly"] = world

# ───────────── 2. 渠道月度 ─────────────
ch_mo = defaultdict(lambda: defaultdict(int))
for mo, rows in D["channel_monthly"].items():
    for r in rows:
        ch_mo[mo][r["ch"]] += r["sessions"]
A["channels"] = {mo: dict(d) for mo, d in sorted(ch_mo.items())}

# ───────────── 3. 设备 ─────────────
dev_mo = defaultdict(lambda: defaultdict(int))
for mo, rows in D["device_monthly"].items():
    for r in rows:
        dev_mo[mo][r["dev"]] += r["sessions"]
A["devices"] = {mo: dict(d) for mo, d in sorted(dev_mo.items())}

# ───────────── 4. 新老 ─────────────
nvr_mo = defaultdict(lambda: defaultdict(int))
for mo, rows in D["nvr_monthly"].items():
    for r in rows:
        nvr_mo[mo][r["nvr"]] += r["sessions"]
A["nvr"] = {mo: dict(d) for mo, d in sorted(nvr_mo.items())}

# ───────────── 5. 事件 ─────────────
events = sorted(D["events"].items(), key=lambda x: -x[1]["count"])
A["events"] = [{"event": k, "count": v["count"], "users": v["users"]} for k, v in events]

# ───────────── 6. 来源介质 ─────────────
sm = sorted(D["source_medium"].items(), key=lambda x: -x[1]["sessions"])
A["source_medium"] = [{"sm": k, "sessions": v["sessions"], "users": v["users"]} for k, v in sm]

# ───────────── 7. 着陆页全渠道 Top ─────────────
lp = sorted(D["landing_all"], key=lambda x: -x["sessions"])
A["landing_top"] = lp[:50]

# ───────────── 8. 城市 ─────────────
cities = sorted(D["cities"], key=lambda x: -x["sessions"])
A["cities_top"] = cities[:20]

# ───────────── 9. 汇总对比 ─────────────
def sum_mo(sel):
    s = sum(m["sessions"] for m in monthly if m["mo"] in sel)
    u = sum(m["users"] for m in monthly if m["mo"] in sel)
    n = sum(m["new"] for m in monthly if m["mo"] in sel)
    days = sum(m["days"] for m in monthly if m["mo"] in sel)
    bnc = sum(m["bounce"] * m["sessions"] for m in monthly if m["mo"] in sel)
    eng = sum(m["engagement_rate"] * m["sessions"] for m in monthly if m["mo"] in sel)
    dur = sum(m["dur_sec"] * m["sessions"] for m in monthly if m["mo"] in sel)
    return {"sessions": s, "users": u, "new": n, "days": days,
            "daily_sessions": round(s / days), "bounce": round(bnc / s, 1) if s else 0,
            "engagement": round(eng / s, 1) if s else 0, "dur": round(dur / s) if s else 0}

A["y2025"] = sum_mo([f"2025-{m:02d}" for m in range(1, 13)])
A["y2026h1"] = sum_mo([f"2026-{m:02d}" for m in range(1, 7)])
A["jul26"] = sum_mo(["2026-07"])

(OUT / "jp_ga4_analysis.json").write_text(json.dumps(A, ensure_ascii=False, indent=1))

# ───────────── stdout ─────────────
print("== JP 全渠道月度 (sessions/users/新占比/跳出/时长/页次/事件) ==")
for m in monthly:
    print(f"{m['mo']}  sess={m['sessions']:>8,} users={m['users']:>8,} new={m['new_share']:5.1f}% "
          f"bounce={m['bounce']:5.1f}% dur={m['dur_sec']:>4}s pps={m['pps']:.2f} eng={m['engagement_rate']:5.1f}% events={m['events']:>10,}")
print("\n== 全球对照 ==")
for w in world:
    print(f"{w['mo']}  sess={w['sessions']:>10,} bounce={w['bounce']:5.1f}% dur={w['dur_sec']:>4}s eng={w['engagement_rate']:5.1f}%")

print("\n== 汇总对比 ==")
for k in ("y2025", "y2026h1", "jul26"):
    v = A[k]
    print(f"  {k:<9} sess={v['sessions']:>10,} 日均={v['daily_sessions']:>7,} users={v['users']:>9,} "
          f"bounce={v['bounce']}% eng={v['engagement']}% dur={v['dur']}s")

print("\n== 渠道占比 (2026-07 vs 2025-01) ==")
def ch_share(mo):
    d = ch_mo[mo]; t = sum(d.values())
    return {k: (v, round(v / t * 100, 1)) for k, v in d.items()}
for mo in ("2025-01", "2025-07", "2025-12", "2026-03", "2026-07"):
    d = ch_mo[mo]; t = sum(d.values())
    parts = ", ".join(f"{k}={v/t*100:.1f}%" for k, v in sorted(d.items(), key=lambda x: -x[1])[:5])
    print(f"  {mo}: {parts}")

print("\n== 设备占比 ==")
for mo in ("2025-01", "2026-01", "2026-07"):
    d = dev_mo[mo]; t = sum(d.values())
    parts = ", ".join(f"{k}={v/t*100:.1f}%" for k, v in sorted(d.items(), key=lambda x: -x[1]))
    print(f"  {mo}: {parts}")

print("\n== 事件 Top30 ==")
for e in A["events"][:30]:
    print(f"  {e['event'][:45]:<45} {e['count']:>10,}  users={e['users']:>9,}")

print("\n== 来源介质 Top15 ==")
for r in A["source_medium"][:15]:
    print(f"  {r['sm'][:40]:<40} {r['sessions']:>9,}  users={r['users']:>9,}")

print("\n== 着陆页全渠道 Top20 ==")
for r in lp[:20]:
    print(f"  {r['page'][:55]:<55} {r['sessions']:>9,} bounce={r['bounce']:5.1f}% dur={r['dur']:>4}s")

print("\n== 城市 Top15 ==")
for c in cities[:15]:
    print(f"  {c['city'][:25]:<25} {c['sessions']:>9,}  users={c['users']:>8,}")
