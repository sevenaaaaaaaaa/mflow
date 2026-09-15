#!/usr/bin/env python3
"""
benchmark_fetch_0508.py — 为「Lovart 海外增长 Benchmark」补齐曝光侧数据。

与 trident/ 下其它脚本的区别：拉**固定历史区间的日粒度**，不是滚动 7/30 天窗口。
并且刻意绕开三个 API 的「默认只返回一部分」行为：

  GSC : rowLimit 默认 1000（已设 25000 + startRow 翻页到底）
        type 默认 web（已循环 web/image/video/news/discover/googleNews）
        dataState 默认 final（已设 all）
        query 维度有匿名化阈值 → 自动核算覆盖率并写进 notes
  GA4 : limit 默认 10000（已按 rowCount 用 offset 翻页到底）
        高基数维度会被折叠成 "(other)" → 自动检测并告警
        抽样 metadata.samplingMetadatas → 自动检测并告警
        账号接了多个站 → 默认按 hostName 锁定 lovart.ai，另出审计文件
  Bing: GetQueryStats 每周只给 top-N → 站点总量改用 GetRankAndTrafficStats

只读，不写任何线上系统。
用法（本机原生终端，不要在 Cowork VM 里跑）：
    python3 benchmark_fetch_0508.py                          # 默认 2026-05-01~08-31
    python3 benchmark_fetch_0508.py 2026-01-01 2026-08-31
    python3 benchmark_fetch_0508.py --only gsc|ga4|bing
    python3 benchmark_fetch_0508.py --audit-only             # 只跑 §审计，不拉大数据
    python3 benchmark_fetch_0508.py --notes-only             # 只按已落盘文件重算 _RUN-NOTES.md
依赖: google-auth google-auth-oauthlib google-api-python-client requests
"""
import csv, json, os, sys, time
from pathlib import Path
from datetime import date, timedelta

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
OUT = PROJECT / "1-2 Insight" / "From Datawork" / "benchmark-2026-05-08"
OUT.mkdir(parents=True, exist_ok=True)

SITE_DOMAIN   = "lovart.ai"                     # hostName / 属性归属的判定依据
GSC_SITE      = "https://www.lovart.ai/"        # 兜底；实际属性由 sites().list() 决定
GA4_PROPERTY  = "properties/403618427"
GA4_STREAM    = "10524753059"
NOTES = []                                       # 收集数据质量标记

def note(msg, level="INFO"):
    line = f"[{level}] {msg}"
    NOTES.append(line)
    print(("  ! " if level != "INFO" else "    ") + msg, flush=True)

CRED_DIRS = [
    Path(os.environ["LOVART_TRIDENT_CREDENTIALS_DIR"]).expanduser() if os.environ.get("LOVART_TRIDENT_CREDENTIALS_DIR") else None,
    Path("~/Library/Application Support/Lovart/credentials/trident").expanduser(),
    PROJECT / "1-1 Harness" / "Skills" / "01-strategy" / "lovart-trident-data-engine" / "credentials",
    PROJECT / "1-1 Harness" / "Skills" / "lovart-trident-data-engine" / "credentials",
    HERE.parent / "sentinel" / "gsc_credentials",
    HERE.parent / "sentinel" / "ga4_credentials",
    HERE.parent / "sentinel" / "bing_credentials",
    HERE,
]
def cred(fn):
    for d in CRED_DIRS:
        if d and (d / fn).exists(): return d / fn
    raise FileNotFoundError(f"找不到 {fn}，检查过:\n  " + "\n  ".join(str(d) for d in CRED_DIRS if d))

PRODUCED = []          # 本次运行真正写出的文件，供 §5 的覆盖区间体检

def write_csv(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    print(f"  ✓ {name:<40} {len(rows):>8,} 行", flush=True)
    if name not in PRODUCED: PRODUCED.append(name)
    return len(rows)

def months_in(s, e):
    cur = s
    while cur <= e:
        nxt = (cur.replace(day=28) + timedelta(days=4)).replace(day=1)
        yield cur, min(nxt - timedelta(days=1), e)
        cur = nxt

def daterange(s, e):
    d = s
    while d <= e:
        yield d.isoformat()
        d += timedelta(days=1)

def _norm_date(v):
    """GA4 返回 20260101，GSC/Bing 返回 2026-01-01；统一成 YYYY-MM-DD 再比。"""
    v = str(v or "").strip()
    return f"{v[:4]}-{v[4:6]}-{v[6:]}" if len(v) == 8 and v.isdigit() else v

# 这些源只给「每周快照」，不是日粒度 —— 不能按缺天报
WEEKLY_SNAPSHOT_FILES = {"bing_query_stats.csv", "bing_page_stats.csv"}

def _err(ex, limit=900):
    """把异常连同 HTTP 响应体一起取出来 —— §5 要求失败时保留原始报错，不许只留类名。"""
    body = ""
    content = getattr(ex, "content", None) or getattr(ex, "text", None)
    if content:
        try:
            body = " | " + (content.decode("utf-8", "replace") if isinstance(content, bytes) else str(content))
        except Exception:
            pass
    return (f"{ex.__class__.__name__}: {ex}{body}").replace("\n", " ")[:limit]

def retry(fn, what, n=4):
    last = None
    for i in range(n):
        try: return fn()
        except Exception as ex:
            last = ex
            if i == n - 1: raise
            note(f"{what} 重试 {i+1}/{n}: {_err(ex, 200)}", "WARN")
            time.sleep(2 ** i)

# ═══════════════════════════════════════════════════════════ GSC
GSC_TYPES = ["web", "image", "video", "news", "discover", "googleNews"]
GSC_ROWLIMIT = 25000          # API 上限；默认值是 1000
GSC_STARTROW_MAX = 100000     # API 对 startRow 的硬上限
GSC_USABLE_PERMISSIONS = {"siteOwner", "siteFullUser", "siteRestrictedUser"}  # siteUnverifiedUser 会 403

def gsc_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    tok = json.loads(cred("gsc-token.json").read_text())
    creds = Credentials.from_authorized_user_info(tok, ["https://www.googleapis.com/auth/webmasters.readonly"])
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)

def gsc_pick_properties(svc):
    """列出全部可访问属性，优先 sc-domain:（URL 前缀属性会漏掉非 www 和子域）。

    关键：只有 permissionLevel ∈ {siteOwner, siteFullUser, siteRestrictedUser} 的属性
    才能调 searchanalytics；siteUnverifiedUser（如 docs./blogs.lovart.ai）会返回
    403 "User does not have sufficient permission for site"，必须在此剔除。
    另外 URL 前缀属性只认 www.lovart.ai / lovart.ai 本体，子域（docs./blogs.）不算同一口径。
    """
    from urllib.parse import urlparse
    sites = svc.sites().list().execute().get("siteEntry", [])
    note("GSC 可访问属性: " + ", ".join(f"{s['siteUrl']}({s.get('permissionLevel')})" for s in sites))

    usable, blocked = [], []
    for s in sites:
        (usable if (s.get("permissionLevel") or "") in GSC_USABLE_PERMISSIONS else blocked).append(s)
    for s in blocked:
        note(f"GSC 属性 {s['siteUrl']} 权限 {s.get('permissionLevel')} 不足（searchanalytics 会 403），不参与口径选择", "WARN")

    dom = [s["siteUrl"] for s in usable
           if s["siteUrl"].startswith("sc-domain:") and s["siteUrl"].split(":", 1)[1].lower() == SITE_DOMAIN]
    pre_all = [s["siteUrl"] for s in usable if not s["siteUrl"].startswith("sc-domain:")]
    pre_exact = [u for u in pre_all
                 if urlparse(u).netloc.lower().rstrip("/") in {SITE_DOMAIN, "www." + SITE_DOMAIN}]
    sub = [u for u in pre_all if u not in pre_exact]
    if sub:
        note(f"GSC 另有子域/它站 URL 前缀属性 {sub} —— 与 {SITE_DOMAIN} 网站口径不同，不并入", "WARN")

    picks = []
    if dom: picks.append((dom[0], "scdomain"))
    if pre_exact: picks.append((pre_exact[0], "urlprefix"))
    if not picks:
        note(f"未找到可用的 {SITE_DOMAIN} 属性，回退到写死值 {GSC_SITE}", "WARN")
        picks = [(GSC_SITE, "urlprefix")]
    if not dom:
        note(f"账号下不存在 sc-domain:{SITE_DOMAIN} 域名属性，只有 URL 前缀口径，"
             f"非 www 与子域的曝光量不在其中（这是 §3.3 差异的一个独立解释）", "WARN")
    if len(picks) == 2:
        note("两种属性口径都会拉，文件名后缀区分；对比二者即可判断 URL 前缀属性漏了多少量。")
    return picks

def gsc_query(svc, site, dims, s, e, stype="web"):
    rows, start_row, truncated = [], 0, False
    while True:
        body = {"startDate": s.isoformat(), "endDate": e.isoformat(), "dimensions": dims,
                "rowLimit": GSC_ROWLIMIT, "startRow": start_row,
                "type": stype, "dataState": "all"}
        resp = retry(lambda: svc.searchanalytics().query(siteUrl=site, body=body).execute(),
                     f"GSC {dims} {stype} {s}")
        batch = resp.get("rows", [])
        # discover / googleNews 的行**没有 position 字段**，统一补空，避免下游 KeyError
        for x in batch:
            rows.append({"keys": x.get("keys", []), "clicks": x.get("clicks", 0),
                         "impressions": x.get("impressions", 0), "ctr": x.get("ctr", ""),
                         "position": x.get("position", "")})
        if len(batch) < GSC_ROWLIMIT: break
        start_row += GSC_ROWLIMIT
        if start_row >= GSC_STARTROW_MAX:
            truncated = True
            note(f"GSC {site} {dims} {stype} {s:%Y-%m} 触到 startRow 上限 {GSC_STARTROW_MAX}，数据被截断", "WARN")
            break
    return rows, truncated

def fetch_gsc(start, end, audit_only=False):
    print("GSC ...", flush=True)
    svc = gsc_service()
    picks = gsc_pick_properties(svc)
    for site, tag in picks:
        sfx = "" if len(picks) == 1 else ("_scdomain" if tag == "scdomain" else "_urlprefix")
        note(f"GSC 正式口径 = {site}（sfx='{sfx}'）")
        # 1) 日 × searchType —— 默认只有 web，这里全类型都拉
        allrows, per_type_clicks = [], {}
        for st in GSC_TYPES:
            try:
                r, _ = gsc_query(svc, site, ["date"], start, end, st)
            except Exception as ex:
                note(f"GSC [{site}] searchType={st} 不可用，跳过：{_err(ex)}", "WARN"); continue
            per_type_clicks[st] = sum(x["clicks"] for x in r)
            allrows += [[x["keys"][0], st, x["clicks"], x["impressions"], x["ctr"], x["position"]] for x in r]
        write_csv(f"gsc_daily_by_type{sfx}.csv", ["date","search_type","clicks","impressions","ctr","position"],
                  sorted(allrows, key=lambda z: (z[0], z[1])))
        note(f"GSC{sfx} 各 searchType 点击: " + ", ".join(f"{k}={v:,}" for k, v in per_type_clicks.items()))
        web_share = per_type_clicks.get("web", 0) / max(sum(per_type_clicks.values()), 1)
        if web_share < 0.97:
            note(f"GSC{sfx} web 只占总点击 {web_share:.1%}，若只拉默认 type=web 会漏 {1-web_share:.1%}", "WARN")
        # web-only 单独一份，方便和历史报告对齐
        web = [r for r in allrows if r[1] == "web"]
        write_csv(f"gsc_daily{sfx}.csv", ["date","clicks","impressions","ctr","position"],
                  [[r[0], r[2], r[3], r[4], r[5]] for r in web])
        if audit_only: continue
        # 2) 日 × device / country（web）
        for dim in ("device", "country"):
            try:
                r, _ = gsc_query(svc, site, ["date", dim], start, end)
            except Exception as ex:
                note(f"GSC [{site}] date×{dim} 失败，该文件缺失：{_err(ex)}", "WARN"); continue
            write_csv(f"gsc_daily_by_{dim}{sfx}.csv", ["date",dim,"clicks","impressions","ctr","position"],
                      [[x["keys"][0], x["keys"][1], x["clicks"], x["impressions"], x["ctr"], x["position"]] for x in r])
        # 3) 月 × query —— 按月而非按日，匿名化阈值下按月覆盖率更高
        try:
            sys.path.insert(0, str(HERE.parent))
            from lovart_brand_match import is_brand      # 项目 SSOT，不要另写规则
            brandfn = is_brand
            note("品牌词判定使用 SSOT lovart_brand_match.is_brand()")
        except Exception as ex:
            brandfn = None
            note(f"无法导入 lovart_brand_match.is_brand，is_brand 列留空：{_err(ex)}", "WARN")
        qrows, cov, qfail = [], [], []
        web_by_month = {}
        for r in web: web_by_month[r[0][:7]] = web_by_month.get(r[0][:7], 0) + r[2]
        for ms, me in months_in(start, end):
            try:
                r, trunc = gsc_query(svc, site, ["query"], ms, me)
            except Exception as ex:
                qfail.append(ms.strftime("%Y-%m"))
                note(f"GSC [{site}] {ms:%Y-%m} query 维度失败：{_err(ex)}", "WARN"); continue
            qc = sum(x["clicks"] for x in r)
            tot = web_by_month.get(ms.strftime("%Y-%m"), 0)
            cov.append((ms.strftime("%Y-%m"), len(r), qc, tot, qc / tot if tot else None))
            qrows += [[ms.strftime("%Y-%m"), x["keys"][0],
                       ("" if brandfn is None else int(bool(brandfn(x["keys"][0])))),
                       x["clicks"], x["impressions"], x["ctr"], x["position"]] for x in r]
            print(f"    {ms:%Y-%m}: {len(r):,} queries, 覆盖点击 {qc:,}/{tot:,}"
                  + (f" = {qc/tot:.1%}" if tot else ""), flush=True)
        write_csv(f"gsc_monthly_query{sfx}.csv",
                  ["month","query","is_brand","clicks","impressions","ctr","position"], qrows)
        write_csv(f"gsc_query_coverage{sfx}.csv",
                  ["month","query_rows","clicks_in_query_rows","total_web_clicks","coverage"], cov)
        if qfail:
            note(f"GSC{sfx} 以下月份 query 维度完全未取到，覆盖率表里缺行：{', '.join(qfail)}", "WARN")
        worst = min((c[4] for c in cov if c[4] is not None), default=1)
        if worst < 0.7:
            note(f"GSC{sfx} query 维度最低月覆盖率仅 {worst:.1%}——其余点击被匿名化阈值隐藏，"
                 f"品牌词/非品牌词占比只能在这个覆盖范围内解读", "WARN")
        # 4) 月 × page
        prows = []
        for ms, me in months_in(start, end):
            try:
                r, _ = gsc_query(svc, site, ["page"], ms, me)
            except Exception as ex:
                note(f"GSC [{site}] {ms:%Y-%m} page 维度失败：{_err(ex)}", "WARN"); continue
            prows += [[ms.strftime("%Y-%m"), x["keys"][0], x["clicks"], x["impressions"], x["ctr"], x["position"]] for x in r]
        write_csv(f"gsc_monthly_page{sfx}.csv", ["month","page","clicks","impressions","ctr","position"], prows)

# ═══════════════════════════════════════════════════════════ GA4
GA4_LIMIT = 250000        # API 单次上限；默认值是 10000
GA4_METRICS = ["sessions","totalUsers","newUsers","activeUsers","engagedSessions",
               "averageSessionDuration","bounceRate","screenPageViews"]

def ga4_services():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    tok = json.loads(cred("ga4-token.json").read_text())
    creds = Credentials.from_authorized_user_info(tok, ["https://www.googleapis.com/auth/analytics.readonly"])
    data = build("analyticsdata", "v1beta", credentials=creds, cache_discovery=False)
    try:    admin = build("analyticsadmin", "v1beta", credentials=creds, cache_discovery=False)
    except Exception: admin = None
    return data, admin

def ga4_audit(admin):
    """账号接了多个站点时，确认 403618427 / stream / hostName 到底对应哪个站。"""
    if admin is None:
        note("Admin API 不可用，跳过属性/数据流审计", "WARN"); return
    try:
        summ = admin.accountSummaries().list(pageSize=200).execute().get("accountSummaries", [])
        lines = []
        for a in summ:
            for p in a.get("propertySummaries", []):
                lines.append(f"{p.get('property')} | {p.get('displayName')} | account={a.get('displayName')}")
        note(f"GA4 账号下共 {len(lines)} 个属性:\n      " + "\n      ".join(lines))
        (OUT / "ga4_property_inventory.txt").write_text("\n".join(lines), encoding="utf-8")
        hit = [l for l in lines if GA4_PROPERTY.split("/")[-1] in l]
        note(f"目标属性 {GA4_PROPERTY} → {hit[0] if hit else '未在清单中找到（权限或已删除）'}",
             "INFO" if hit else "WARN")
    except Exception as ex:
        note(f"accountSummaries 失败: {ex.__class__.__name__}: {ex}", "WARN")
    try:
        prop = admin.properties().get(name=GA4_PROPERTY).execute()
        note(f"属性时区 = {prop.get('timeZone')}，货币 = {prop.get('currencyCode')}"
             f"（日粒度与 DataWorks 大盘表对齐前必须确认时区一致，否则按天 join 会错位一天）")
    except Exception as ex:
        note(f"properties.get 失败: {ex.__class__.__name__}", "WARN")
    try:
        streams = admin.properties().dataStreams().list(parent=GA4_PROPERTY, pageSize=200).execute().get("dataStreams", [])
        lines = [f"{s.get('name','').split('/')[-1]} | {s.get('displayName')} | "
                 f"{s.get('webStreamData',{}).get('defaultUri','')}" for s in streams]
        note(f"GA4 属性 {GA4_PROPERTY} 下共 {len(streams)} 个数据流:\n      " + "\n      ".join(lines))
        (OUT / "ga4_stream_inventory.txt").write_text("\n".join(lines), encoding="utf-8")
        tgt = [l for l in lines if l.startswith(GA4_STREAM)]
        if tgt:
            note(f"写死的 stream {GA4_STREAM} → {tgt[0]}")
            if SITE_DOMAIN not in tgt[0]:
                note(f"该 stream 的 defaultUri 不含 {SITE_DOMAIN}，stream 过滤口径存疑", "WARN")
        else:
            note(f"写死的 stream {GA4_STREAM} 不在该属性的数据流清单里", "WARN")
        if len(streams) > 1:
            note(f"该属性有 {len(streams)} 个数据流，说明确实混了多个站/端 —— "
                 f"本脚本用 hostName 含 '{SITE_DOMAIN}' 作为正式口径", "WARN")
    except Exception as ex:
        note(f"dataStreams.list 失败: {ex.__class__.__name__}", "WARN")

def _host_filter():
    return {"filter": {"fieldName": "hostName",
                       "stringFilter": {"matchType": "CONTAINS", "value": SITE_DOMAIN, "caseSensitive": False}}}
def _stream_filter():
    return {"filter": {"fieldName": "streamId", "stringFilter": {"matchType": "EXACT", "value": GA4_STREAM}}}

def ga4_pages(data, dims, s, e, scope="host", extra=None, tag=""):
    """scope: host = 按 hostName 锁 lovart.ai（正式口径）| stream = 旧口径 | none = 全量审计

    逐页 yield，调用方自己决定是攒内存还是边写盘 —— referral 明细单月可达百万行，
    全攒内存会吃掉数 GB。
    """
    exprs = []
    if scope == "host":   exprs.append(_host_filter())
    elif scope == "stream": exprs.append(_stream_filter())
    if extra: exprs.append(extra)
    dimfilter = None
    if len(exprs) == 1: dimfilter = exprs[0]
    elif len(exprs) > 1: dimfilter = {"andGroup": {"expressions": exprs}}

    offset, flagged, seen_other, other_note, n = 0, False, False, False, 0
    while True:
        body = {"dateRanges": [{"startDate": s.isoformat(), "endDate": e.isoformat()}],
                "dimensions": [{"name": d} for d in dims],
                "metrics": [{"name": m} for m in GA4_METRICS],
                "limit": GA4_LIMIT, "offset": offset, "keepEmptyRows": True}
        if dimfilter: body["dimensionFilter"] = dimfilter
        resp = retry(lambda: data.properties().runReport(property=GA4_PROPERTY, body=body).execute(),
                     f"GA4 {dims} {s}")
        meta = resp.get("metadata", {}) or {}
        if meta.get("samplingMetadatas") and not flagged:
            sm = meta["samplingMetadatas"][0]
            note(f"GA4 {tag or dims} {s:%Y-%m} 被抽样: 读取 {sm.get('samplesReadCount')} / "
                 f"空间 {sm.get('samplingSpaceSize')}", "WARN"); flagged = True
        if meta.get("dataLossFromOtherRow") and not other_note:
            note(f"GA4 {tag or dims} {s:%Y-%m} 出现 (other) 行折叠（metadata.dataLossFromOtherRow），"
                 f"高基数维度尾部被聚合", "WARN"); other_note = True
        rows = resp.get("rows", [])
        page = [[*[v["value"] for v in r["dimensionValues"]], *[v["value"] for v in r["metricValues"]]]
                for r in rows]
        if dims and dims[0] == "date":          # GA4 原生 20260101 → 与 GSC/Bing 对齐成 2026-01-01
            for r in page: r[0] = _norm_date(r[0])
        if not seen_other and any("(other)" in str(p[:len(dims)]) for p in page):
            note(f"GA4 {tag or dims} 结果维度值里出现字面 '(other)'，该维度基数超限被折叠", "WARN")
            seen_other = True
        total = int(resp.get("rowCount", n + len(page)))
        offset += len(rows); n += len(page)
        yield page
        if not rows or offset >= total: break

def ga4_run(data, dims, s, e, scope="host", extra=None, tag=""):
    out = []
    for page in ga4_pages(data, dims, s, e, scope=scope, extra=extra, tag=tag):
        out += page
    return out

def ga4_write_stream(data, name, dims, start, end, scope="host", extra=None):
    """边翻页边落盘（referral 明细用），内存恒定。"""
    n = 0
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(dims + GA4_METRICS)
        for ms, me in months_in(start, end):
            for page in ga4_pages(data, dims, ms, me, scope=scope, extra=extra, tag=name):
                w.writerows(page); n += len(page)
            f.flush()
            print(f"    {name} {ms:%Y-%m} ok（累计 {n:,} 行）", flush=True)
    size = (OUT / name).stat().st_size / 1e6
    print(f"  ✓ {name:<40} {n:>8,} 行（{size:.1f} MB，流式写入）", flush=True)
    if name not in PRODUCED: PRODUCED.append(name)
    note(f"{name}: {n:,} 行 / {size:.1f} MB —— 已按日×来源全量落盘，未做任何 top-N 裁剪", "WARN")
    return n

def fetch_ga4(start, end, audit_only=False):
    print("GA4 ...", flush=True)
    data, admin = ga4_services()
    ga4_audit(admin)

    # §2.2 保留期：标准属性的事件数据默认只留 2 个月，先探测契约区间里到底有没有数据
    try:
        probe = ga4_run(data, ["date"], start, end, scope="host", tag="retention-probe")
        idx = 1 + GA4_METRICS.index("sessions")
        days = sorted(r[0] for r in probe if float(r[idx] or 0) > 0)
        fmt = lambda d: f"{d[:4]}-{d[4:6]}-{d[6:]}"
        if days:
            note(f"GA4 保留期探测：{start}~{end} 有数据 {len(days)} 天，最早 {fmt(days[0])}，最晚 {fmt(days[-1])}"
                 + ("" if days[0] <= start.strftime("%Y%m%d") else f" —— 契约区间前段（{start}~{fmt(days[0])}）取不到，"
                                                                     f"请按退让区间解读"), "WARN" if days[0] > start.strftime("%Y%m%d") else "INFO")
        else:
            note(f"GA4 保留期探测：{start}~{end} 全为 0，该属性没有可用历史（保留期限制）", "WARN")
    except Exception as ex:
        note(f"GA4 保留期探测失败: {_err(ex)}", "WARN")

    # A) hostName 审计：这个属性里到底有哪些站
    rows = []
    for ms, me in months_in(start, end):
        rows += ga4_run(data, ["hostName"], ms, me, scope="none", tag="hostname-audit")
    agg = {}
    for r in rows:
        agg[r[0]] = agg.get(r[0], 0) + int(float(r[1 + GA4_METRICS.index("sessions")]))
    write_csv("ga4_hostname_audit.csv", ["hostName","sessions_sum"],
              sorted(([k, v] for k, v in agg.items()), key=lambda z: -z[1]))
    tot = sum(agg.values()) or 1
    mine = sum(v for k, v in agg.items() if SITE_DOMAIN in k)
    note(f"GA4 属性内 hostName 共 {len(agg)} 个；{SITE_DOMAIN} 占会话 {mine/tot:.1%}"
         + ("（属性是干净的）" if mine/tot > 0.98 else " —— 属性确实混了别的站，必须按 hostName 过滤"),
         "INFO" if mine/tot > 0.98 else "WARN")

    # B) 口径对照：不过滤 / stream 过滤 / hostName 过滤，三份日粒度总量
    for scope, name in (("none","ga4_daily_nofilter.csv"), ("stream","ga4_daily_streamfilter.csv"),
                        ("host","ga4_daily.csv")):
        rows = []
        for ms, me in months_in(start, end):
            rows += ga4_run(data, ["date"], ms, me, scope=scope, tag=name)
        write_csv(name, ["date"] + GA4_METRICS, sorted(rows))
    if audit_only: return

    # C) 正式口径（hostName = lovart.ai）下的各维度明细
    for dims, name in ([["date","sessionDefaultChannelGroup","firstUserDefaultChannelGroup"], "ga4_daily_by_channel.csv"],
                       [["date","sessionSource","sessionMedium"], "ga4_daily_by_source_medium.csv"],
                       [["date","country"], "ga4_daily_by_country.csv"]):
        rows = []
        for ms, me in months_in(start, end):
            rows += ga4_run(data, dims, ms, me, scope="host", tag=name)
            print(f"    {name} {ms:%Y-%m} ok", flush=True)
        write_csv(name, dims + GA4_METRICS, rows)

    # D) Referral 明细 —— 拆「Referer 引荐」那 278 万未知 UV
    #    这两个文件是高基数明细（单月百万行级），必须流式落盘，不能攒内存
    ref = {"filter": {"fieldName": "sessionMedium",
                      "stringFilter": {"matchType": "EXACT", "value": "referral"}}}
    for dims, name in ((["date","sessionSource","pageReferrer"], "ga4_referral_detail.csv"),
                       (["date","sessionSource","landingPage"], "ga4_referral_landing.csv")):
        try:
            ga4_write_stream(data, name, dims, start, end, scope="host", extra=ref)
        except Exception as ex:
            note(f"{name} 失败（{dims[-1]} 可能不受支持）: {_err(ex)}", "WARN")

# ═══════════════════════════════════════════════════════════ Bing
# 注意：Bing Webmaster 的 SOAP 端点（api.svc/soap）目前对任何 body 都返回
#   HTTP 400 {"ErrorCode":2,"Message":"ERROR!!! UnknownError"}
# （2026-09-13 实测；与 SOAPAction 加不加引号、命名空间、Content-Type、带不带 apikey 都无关）。
# 可用的入口是同一服务的 JSON 端点：
#   GET https://www.bing.com/webmasterapi/api.svc/json/<Method>?apikey=...&siteUrl=...
BING_JSON = "https://www.bing.com/webmasterapi/api.svc/json"

def _bing_date(raw):
    """Bing 返回 '/Date(1747094400000)/'（UTC 毫秒）→ 'YYYY-MM-DD'。"""
    import re
    from datetime import datetime, timezone
    m = re.search(r"/Date\((-?\d+)", str(raw))
    if not m: return str(raw)[:10]
    return datetime.fromtimestamp(int(m.group(1)) / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

def _bing_int(v):
    try: return int(float(v or 0))
    except Exception: return 0

def fetch_bing(start, end, audit_only=False):
    import requests
    print("Bing ...", flush=True)
    key = cred("api_key").read_text().strip()
    sess = requests.Session()
    sess.headers.update({"Accept": "application/json", "User-Agent": "lovart-trident/benchmark_fetch_0508"})

    def jget(action, **params):
        params["apikey"] = key

        def go():
            r = sess.get(f"{BING_JSON}/{action}", params=params, timeout=90)
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
            return r.json().get("d", [])
        return retry(go, f"Bing {action} {params.get('siteUrl', '')}")

    # 审计：这个 Bing 账号下有哪些站，lovart.ai 的 siteUrl 到底写成什么
    site = GSC_SITE
    try:
        sites = jget("GetUserSites")
        lines = [f"{s.get('Url')} | verified={s.get('IsVerified')}" for s in sites]
        note("Bing 账号下站点: " + (", ".join(lines) if lines else "(空)"))
        (OUT / "bing_site_inventory.txt").write_text("\n".join(lines), encoding="utf-8")
        cand = [s for s in sites if SITE_DOMAIN in (s.get("Url") or "")]
        ver = [s for s in cand if s.get("IsVerified")]
        if ver: site = ver[0]["Url"]
        elif cand: site = cand[0]["Url"]
        if len(cand) > 1:
            note(f"匹配到多个 lovart 站点 {[s.get('Url') for s in cand]}，使用 {site}（优先已验证）", "WARN")
        if not cand:
            note(f"Bing 账号下没有 {SITE_DOMAIN}，回退 {GSC_SITE}", "WARN")
    except Exception as ex:
        note(f"GetUserSites 失败，回退 {GSC_SITE}：{_err(ex)}", "WARN")
    note(f"Bing 正式口径 = {site}")

    # 站点总量用 RankAndTrafficStats（QueryStats 每周只给 top-N，加总≠站点总量）
    try:
        recs = jget("GetRankAndTrafficStats", siteUrl=site)
        rows = sorted([[_bing_date(r.get("Date")), _bing_int(r.get("Impressions")), _bing_int(r.get("Clicks"))]
                       for r in recs if r.get("Date")])
        write_csv("bing_traffic_daily.csv", ["date", "impressions", "clicks"], rows)
        if rows:
            seen = {r[0] for r in rows}
            inrange = [r for r in rows if start.isoformat() <= r[0] <= end.isoformat()]
            note(f"Bing GetRankAndTrafficStats 无翻页参数即整段返回：窗口 {rows[0][0]} ~ {rows[-1][0]}，"
                 f"{len(rows)} 天（含契约区间外的历史，未裁剪）。契约区间 {start}~{end} 内 {len(inrange)} 天，"
                 f"点击 {sum(r[2] for r in inrange):,} / 曝光 {sum(r[1] for r in inrange):,}")
            gap = [d for d in daterange(start, end) if d not in seen]
            if gap:
                note(f"Bing 契约区间内缺失日期 {len(gap)} 天：{', '.join(gap)}", "WARN")
            else:
                note("Bing 契约区间内无缺失日期")
    except Exception as ex:
        note(f"GetRankAndTrafficStats 失败: {_err(ex)}", "WARN")
    if audit_only: return

    for action, name, lbl in (("GetQueryStats", "bing_query_stats.csv", "query"),
                              ("GetPageStats", "bing_page_stats.csv", "page")):
        try:
            recs = jget(action, siteUrl=site)
            rows = []
            for r in recs:
                d, q = _bing_date(r.get("Date")), r.get("Query")
                if not q or d.startswith("Date("): continue
                rows.append([d, q, _bing_int(r.get("Clicks")), _bing_int(r.get("Impressions")),
                             r.get("AvgImpressionPosition", "")])
            rows.sort(key=lambda z: (z[0], z[1]))
            write_csv(name, ["date", lbl, "clicks", "impressions", "avg_position"], rows)
            per_week = {}
            for r in rows: per_week[r[0]] = per_week.get(r[0], 0) + 1
            counts = sorted(per_week.values()) or [0]
            note(f"{name}: {len(rows):,} 行 / {len(per_week)} 个周快照 × 每周 "
                 f"中位 {counts[len(counts)//2]} 条（min {counts[0]} / max {counts[-1]}），"
                 f"窗口 {min(per_week, default='-')} ~ {max(per_week, default='-')}。"
                 f"该接口每周只给 top-N 且无翻页参数，不是全量 —— 占比分析必须用 "
                 f"bing_traffic_daily.csv 做分母", "WARN")
        except Exception as ex:
            note(f"{action} 失败: {_err(ex)}", "WARN")

# ═══════════════════════════════════════════════════════════ 品牌词规则快照
def write_brand_snapshot():
    """§4 要求：导出当前生效的品牌词规则快照，日后规则改动也能复现 is_brand 的口径。"""
    import hashlib
    try:
        sys.path.insert(0, str(HERE.parent))
        import lovart_brand_match as bm
    except Exception as ex:
        note(f"brand_rules_snapshot.json 生成失败：无法导入 lovart_brand_match（{_err(ex, 200)}）", "WARN")
        return
    p = Path(bm.__file__).resolve()
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    snap = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "module_path": str(p),
        "module_sha256": sha,
        "note": "is_brand() 的 SSOT 是 1-4 Dev/scripts/lovart_brand_match.py；本文件只是该规则的快照，不替代它。",
        "brand_patterns": list(bm.BRAND_PATTERNS),
        "translit_fragments": list(bm._TRANSLIT_FRAGMENTS),
        "brand_roots": sorted(bm._BRAND_ROOTS),
        "art_suffix_tokens": sorted(bm._ART_SUFFIX_TOKENS),
        "short_roots": sorted(bm._SHORT_ROOTS),
        "fuzzy_deny": sorted(bm._FUZZY_DENY),
        "samples": {q: bool(bm.is_brand(q)) for q in [
            "lovart", "lovart ai", "lovart登录", "ロバート", "art ai",
            "ai image generator", "logo", "login", "lovart.ai", "nano banana"]},
    }
    (OUT / "brand_rules_snapshot.json").write_text(
        json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ brand_rules_snapshot.json（lovart_brand_match.py sha256 {sha[:12]}…）", flush=True)
    note(f"品牌词规则快照已导出 brand_rules_snapshot.json（lovart_brand_match.py sha256 {sha[:16]}）")

# ═══════════════════════════════════════════════════════════ main
if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
    audit_only = "--audit-only" in sys.argv
    notes_only = "--notes-only" in sys.argv          # 只按已落盘文件重算 _RUN-NOTES.md，不再打 API
    s = date.fromisoformat(args[0]) if args else date(2026, 5, 1)
    e = date.fromisoformat(args[1]) if len(args) > 1 else date(2026, 8, 31)
    print(f"区间 {s} ~ {e}   输出 → {OUT}"
          + ("   [仅审计]" if audit_only else "") + ("   [仅重算 notes]" if notes_only else "") + "\n", flush=True)
    if notes_only:
        PRODUCED.extend(sorted(p.name for p in OUT.glob("*.csv")))
    write_brand_snapshot()
    note("口径提醒：GA4 原始 date 为 YYYYMMDD，本脚本已统一归一成 YYYY-MM-DD，与 GSC/Bing 可直接按天 join；"
         "Bing QueryStats/PageStats 的 date 是每周快照标记日（每周一条，非日粒度）")
    for nm, fn in (("gsc", fetch_gsc), ("ga4", fetch_ga4), ("bing", fetch_bing)):
        if notes_only or (only and only != nm): continue
        try: fn(s, e, audit_only)
        except Exception as ex:
            note(f"{nm} 整体失败: {_err(ex)}", "ERROR")
        print("", flush=True)

    # §5：每个产出文件的实际覆盖区间 + 缺失日期逐个列出（流式读，referral 明细可达千万行）
    cov_lines, other_note_lines = [], []
    for name in sorted(PRODUCED):
        nrows, n_other, other_cols = 0, 0, set()
        try:
            with open(OUT / name, newline="", encoding="utf-8") as f:
                rd = csv.DictReader(f)
                cols = rd.fieldnames or []
                dates, spans, per_type = set(), set(), {}
                for r in rd:
                    nrows += 1
                    if any(v == "(other)" for v in r.values()):
                        n_other += 1
                        other_cols.update(k for k, v in r.items() if v == "(other)")
                    if "date" in cols and r.get("date"):
                        dv = _norm_date(r["date"])
                        dates.add(dv)
                        if "search_type" in cols: per_type.setdefault(r["search_type"], set()).add(dv)
                    elif r.get("month"):
                        spans.add(r["month"])
        except Exception as ex:
            cov_lines.append(f"| `{name}` | 读取失败 {_err(ex, 120)} | | | |")
            continue
        other_cell = "0" if not n_other else f"{n_other:,}（列: {','.join(sorted(other_cols))}）"
        if n_other:
            other_note_lines.append(f"- `{name}` 含字面 '(other)' 行 {n_other:,} 行，出现在列 {sorted(other_cols)}")
        if dates:
            lo, hi = min(dates), max(dates)
            if name in WEEKLY_SNAPSHOT_FILES:
                wk = sorted(dates)
                miss_txt = (f"周粒度快照，非日粒度；{len(wk)} 个快照周 "
                            f"（{wk[0]} ~ {wk[-1]}），契约区间内 {len([d for d in wk if s.isoformat() <= d <= e.isoformat()])} 个")
            elif per_type:
                miss_txt = "; ".join(f"{k} 缺 {len([d for d in daterange(s, e) if d not in v])} 天"
                                     for k, v in sorted(per_type.items()))
            else:
                missing = [d for d in daterange(s, e) if d not in dates]
                miss_txt = "无" if not missing else f"缺 {len(missing)} 天: {', '.join(missing)}"
            cov_lines.append(f"| `{name}` | {lo} ~ {hi} | {nrows:,} 行 | {miss_txt} | {other_cell} |")
        elif spans:
            cov_lines.append(f"| `{name}` | {min(spans)} ~ {max(spans)}（月粒度） | {nrows:,} 行 | 不适用 | {other_cell} |")
        else:
            cov_lines.append(f"| `{name}` | —— | {nrows:,} 行 | 不适用 | {other_cell} |")
    if not cov_lines:
        cov_lines.append("| (无) | | | | |")
    if not other_note_lines:
        other_note_lines.append("- 全部产出文件里都没有字面 '(other)' 行（逐行核对）—— "
                                "即便 GA4 元数据报过 dataLossFromOtherRow，落到文件里的行都是真值")

    # --notes-only 模式下没有新的 NOTES：沿用上一版标记，并把本次新增的追加在后面（不覆盖）
    prev_block = ""
    if notes_only and (OUT / "_RUN-NOTES.md").exists():
        _t = (OUT / "_RUN-NOTES.md").read_text(encoding="utf-8")
        if "## 数据质量标记" in _t:
            prev_block = _t.split("## 数据质量标记", 1)[1].strip("\n")
    new_lines = [f"- {n}" for n in NOTES]
    if notes_only:
        have = set(prev_block.splitlines())
        add = [l for l in new_lines if l not in have]        # 幂等：重复跑不会叠加同样两行
        marker_block = "\n".join(x for x in (prev_block, "\n".join(add)) if x) or "- (无)"
    else:
        marker_block = "\n".join(new_lines) or "- (无)"

    (OUT / "_RUN-NOTES.md").write_text(
        f"# 补数运行记录\n\n"
        f"区间 {s} ~ {e}（契约区间）\n"
        f"运行时间 {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"脚本 {Path(__file__).name}\n\n"
        f"## 文件覆盖区间体检\n\n"
        f"| 文件 | 实际覆盖 | 行数 | 契约区间内缺失 | 字面 '(other)' 行 |\n|---|---|---|---|---|\n"
        + "\n".join(cov_lines) + "\n\n"
        f"## '(other)' 折叠核对（GA4 高基数维度）\n\n"
        + "\n".join(other_note_lines) + "\n\n"
        f"## 数据质量标记\n\n"
        + marker_block + "\n",
        encoding="utf-8")
    print(f"完成。数据 + _RUN-NOTES.md 都在 {OUT.name}/，整个目录交给 Claude 即可。")
