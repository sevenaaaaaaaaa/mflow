#!/usr/bin/env python3
"""GA4 日本市场全量深挖 — 2025-01-01 ~ 2026-07-31（逐月拉取防超时）。

维度/指标：
  1. JP 全渠道日度: date × sessions/users/newUsers/engaged/时长/页次/跳出/事件数
  2. JP 渠道月度:   sessionDefaultChannelGroup × date
  3. JP 设备月度:   deviceCategory × date
  4. JP 新老用户:   newVsReturning × date
  5. JP 事件 Top:   eventName × eventCount（逐月聚合）
  6. JP 来源介质:   sessionSourceMedium × sessions（逐月聚合）
  7. JP 着陆页全渠道: landingPage（全窗口）
  8. JP 城市:       city（全窗口）
  9. 全球对照:      date × sessions（全渠道, 全窗口）+ 全球 engagement 汇总
输出: /tmp/jp_pull/ga4_jp_deep.json
"""
import json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from credential_paths import credential_file

OUT = Path("/tmp/jp_pull"); OUT.mkdir(parents=True, exist_ok=True)
PROPERTY = "properties/403618427"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
MONTHS = [f"{y}-{m:02d}" for y in (2025, 2026) for m in range(1, 13)][:19]


def month_bounds(mo):
    y, m = int(mo[:4]), int(mo[5:7])
    last = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return f"{mo}-01", f"{mo}-{last:02d}"


def jp_filter():
    return {"filter": {"fieldName": "country", "stringFilter": {
        "matchType": "CONTAINS", "value": "Japan"}}}


def run(svc, start, end, dims, metrics, extra_filter=None, limit=100000):
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "dimensions": [{"name": d} for d in dims],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
    }
    if extra_filter:
        body["dimensionFilter"] = extra_filter
    resp = svc.properties().runReport(property=PROPERTY, body=body).execute()
    rows = []
    for r in resp.get("rows", []):
        row = {"dims": [v["value"] for v in r["dimensionValues"]],
               "metrics": [v["value"] for v in r["metricValues"]]}
        rows.append(row)
    return rows


def main():
    token = credential_file("ga4-token.json", "LOVART_GA4_TOKEN_FILE")
    creds = Credentials.from_authorized_user_info(json.loads(token.read_text()), SCOPES)
    svc = build("analyticsdata", "v1beta", credentials=creds)
    jpf = jp_filter()
    out = {"_window": "2025-01-01..2026-07-31", "_country": "Japan"}

    M_DAILY = ["sessions", "totalUsers", "newUsers", "engagedSessions",
               "engagementRate", "averageSessionDuration", "screenPageViewsPerSession",
               "bounceRate", "eventCount", "screenPageViews"]
    out["jp_daily"] = []
    out["channel_monthly"] = {}
    out["device_monthly"] = {}
    out["nvr_monthly"] = {}
    out["events"] = {}
    out["source_medium"] = {}
    if (OUT / "ga4_jp_deep.json").exists():
        existing = json.loads((OUT / "ga4_jp_deep.json").read_text())
        for k in ("jp_daily", "channel_monthly", "device_monthly", "nvr_monthly", "events", "source_medium"):
            out[k] = existing.get(k, out[k])
        print(f"  ♻ 续跑：已有 {len(out['channel_monthly'])} 个月，跳过…")

    for mo in MONTHS:
        if mo in out["channel_monthly"]:
            print(f"  ⏭ {mo}: 已存在，跳过")
            continue
        s, e = month_bounds(mo)
        # 1. 日度全渠道
        rows = run(svc, s, e, ["date"], M_DAILY, extra_filter=jpf)
        out["jp_daily"].extend([{"d": r["dims"][0],
                                 "m": {k: (float(v) if k in ("engagementRate", "averageSessionDuration", "screenPageViewsPerSession", "bounceRate") else int(v))
                                       for k, v in zip(M_DAILY, r["metrics"])}} for r in rows])
        # 2. 渠道
        rows = run(svc, s, e, ["sessionDefaultChannelGroup", "date"],
                   ["sessions", "totalUsers", "newUsers"], extra_filter=jpf)
        out["channel_monthly"][mo] = [{"ch": r["dims"][0], "d": r["dims"][1],
                                       "sessions": int(r["metrics"][0]), "users": int(r["metrics"][1]),
                                       "new": int(r["metrics"][2])} for r in rows]
        # 3. 设备
        rows = run(svc, s, e, ["deviceCategory", "date"],
                   ["sessions", "totalUsers"], extra_filter=jpf)
        out["device_monthly"][mo] = [{"dev": r["dims"][0], "d": r["dims"][1],
                                      "sessions": int(r["metrics"][0]), "users": int(r["metrics"][1])} for r in rows]
        # 4. 新老用户
        rows = run(svc, s, e, ["newVsReturning", "date"],
                   ["sessions", "totalUsers"], extra_filter=jpf)
        out["nvr_monthly"][mo] = [{"nvr": r["dims"][0], "d": r["dims"][1],
                                   "sessions": int(r["metrics"][0]), "users": int(r["metrics"][1])} for r in rows]
        # 5. 事件
        rows = run(svc, s, e, ["eventName"], ["eventCount", "totalUsers"], extra_filter=jpf, limit=400)
        for r in rows:
            e_name = r["dims"][0]
            ev = out["events"].setdefault(e_name, {"count": 0, "users": 0})
            ev["count"] += int(r["metrics"][0]); ev["users"] += int(r["metrics"][1])
        # 6. 来源介质
        rows = run(svc, s, e, ["sessionSourceMedium"], ["sessions", "totalUsers"],
                   extra_filter=jpf, limit=200)
        for r in rows:
            sm = r["dims"][0]
            sm_e = out["source_medium"].setdefault(sm, {"sessions": 0, "users": 0})
            sm_e["sessions"] += int(r["metrics"][0]); sm_e["users"] += int(r["metrics"][1])
        print(f"  {mo}: daily={len(out['jp_daily'])}行 渠道/设备/新老/事件/来源 完成")
        time.sleep(0.4)
        # 增量保存
        (OUT / "ga4_jp_deep.json").write_text(json.dumps(out, ensure_ascii=False))

    # 7. 着陆页（全渠道, 全窗口）
    try:
        rows = run(svc, "2025-01-01", "2026-07-31", ["landingPage"],
                   ["sessions", "totalUsers", "newUsers", "bounceRate", "averageSessionDuration"],
                   extra_filter=jpf, limit=100000)
        out["landing_all"] = [{"page": r["dims"][0], "sessions": int(r["metrics"][0]),
                               "users": int(r["metrics"][1]), "new": int(r["metrics"][2]),
                               "bounce": round(float(r["metrics"][3]) * 100, 1),
                               "dur": round(float(r["metrics"][4]))} for r in rows]
        print(f"  landingPage(all): {len(out['landing_all'])} 页")
    except Exception as e:
        print(f"  ⚠ landing 失败: {e}")

    # 8. 城市
    try:
        rows = run(svc, "2025-01-01", "2026-07-31", ["city"],
                   ["sessions", "totalUsers"], extra_filter=jpf, limit=10000)
        out["cities"] = [{"city": r["dims"][0], "sessions": int(r["metrics"][0]),
                          "users": int(r["metrics"][1])} for r in rows]
        print(f"  cities: {len(out['cities'])} 城市")
    except Exception as e:
        print(f"  ⚠ cities 失败: {e}")

    # 9. 全球对照：全渠道日度 + 汇总
    try:
        rows = run(svc, "2025-01-01", "2026-07-31", ["date"],
                   ["sessions", "totalUsers", "newUsers", "engagedSessions",
                    "engagementRate", "averageSessionDuration", "screenPageViewsPerSession",
                    "bounceRate"], limit=100000)
        out["world_daily"] = [{"d": r["dims"][0],
                               "m": {k: (float(v) if k in ("engagementRate", "averageSessionDuration", "screenPageViewsPerSession", "bounceRate") else int(v))
                                     for k, v in zip(["sessions", "totalUsers", "newUsers", "engagedSessions",
                                                      "engagementRate", "averageSessionDuration",
                                                      "screenPageViewsPerSession", "bounceRate"], r["metrics"])}}
                              for r in rows]
        print(f"  world_daily: {len(out['world_daily'])} 天")
    except Exception as e:
        print(f"  ⚠ world 失败: {e}")

    (OUT / "ga4_jp_deep.json").write_text(json.dumps(out, ensure_ascii=False))
    print(f"📁 {OUT}/ga4_jp_deep.json")


if __name__ == "__main__":
    main()
