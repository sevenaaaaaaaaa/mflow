#!/usr/bin/env python3
"""月报扩展：OKR、年均对比、分区 mini 报告、关键词多维分层、章节洞察。"""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
from typing import Any

from lovart_brand_match import is_brand
from lovart_seo_geo_metrics import (
    NEW_VS_ALL_PAY_FOOTNOTE,
    DAILY_SUM_FOOTNOTE,
    GA4_DATAWORK_FOOTNOTE,
    OKR_NATURAL_FOOTNOTE,
    channel_metrics,
    dau_share_pct,
    merge_natural_dedup,
    natural_pay_metrics,
)

# OKR 2026-05 版（与 AGENTS.md A4 一致）
OKR = {
    "O1": {"organic_uv_month": 960_000, "reg_month": 360_000, "pay_month": 22_800,
           "reg_rate": 0.375, "pay_rate": 0.063},
    "O3": {"referral_uv_month": 360_000, "reg_month": 42_000, "pay_month": 3_000,
           "ref_reg_rate": 0.117, "ref_pay_rate": 0.071},
}

TRIDENT_REPORTS = Path(__file__).resolve().parents[2] / "1-2 Insight" / "Trident Insights" / "reports"


def pct_str(actual: float, target: float) -> str:
    if not target:
        return "—"
    return f"{round(actual / target * 100, 1)}%"


def annual_note(hist: dict, metric: str, curr: float, *, digits: int = 0) -> str:
    """节末年均对比备注。hist: {2025_avg, 2026_ytd_avg, 2026_months, 2025_months}"""
    a25 = hist.get("avg_2025", {}).get(metric)
    a26 = hist.get("avg_2026_ytd", {}).get(metric)
    m25 = hist.get("months_2025", 0)
    m26 = hist.get("months_2026", 0)
    if digits:
        s25 = f"{a25:,.{digits}f}" if a25 is not None else "—"
        s26 = f"{a26:,.{digits}f}" if a26 is not None else "—"
        sc = f"{curr:,.{digits}f}"
    else:
        s25 = f"{a25:,.0f}" if a25 is not None else "—"
        s26 = f"{a26:,.0f}" if a26 is not None else "—"
        sc = f"{curr:,.0f}"
    return (
        f"> 📊 **年均对比** — 当月 {sc} ｜ "
        f"2026 YTD 月均 ({m26}个月) {s26} ｜ 2025 月均 ({m25}个月) {s25}"
    )


def load_metrics_history(metrics_dir: Path, out_dir: Path, report_ym: str) -> dict:
    """从 .metrics 与 gsc-5k 缓存聚合 2025/2026 月均。"""
    y, m = map(int, report_ym.split("-"))

    def load_one(ym: str) -> dict | None:
        p = metrics_dir / f"{ym}.json"
        if p.exists():
            return json.loads(p.read_text())
        gp = out_dir / f"gsc-5k-{ym}.json"
        if not gp.exists():
            return None
        d = json.loads(gp.read_text())
        t = d.get("tiers", {})
        return {
            "gsc_clicks": t.get("_total_clicks", 0),
            "gsc_impr": t.get("_total_impr", 0),
            "brand_share": t.get("品牌词", {}).get("share", 0),
            "nb_share": t.get("非品牌词", {}).get("share", 0),
        }

    def avg_for_year(year: int, through_month: int | None = None) -> tuple[dict, int]:
        acc: dict[str, list] = defaultdict(list)
        n = 0
        max_m = through_month if through_month else 12
        for mm in range(1, max_m + 1):
            ym = f"{year}-{mm:02d}"
            row = load_one(ym)
            if not row:
                continue
            n += 1
            for k, v in row.items():
                try:
                    acc[k].append(float(v))
                except (TypeError, ValueError):
                    pass
        avg = {k: round(sum(v) / len(v), 1) if v else None for k, v in acc.items()}
        return avg, n

    avg_2026, m26 = avg_for_year(y, m if y == 2026 else None)
    avg_2025, m25 = avg_for_year(2025)
    return {
        "avg_2025": avg_2025,
        "avg_2026_ytd": avg_2026,
        "months_2025": m25,
        "months_2026": m26,
    }


def save_metrics_snapshot(
    metrics_dir: Path,
    report_ym: str,
    g_curr: dict,
    ga4_curr: dict,
    comp_curr: dict,
    pdirs_curr: dict,
) -> None:
    metrics_dir.mkdir(parents=True, exist_ok=True)
    home = pdirs_curr.get("首页", {"clicks": 0, "impr": 0})
    tools = pdirs_curr.get("tools", {"clicks": 0})
    snap = {
        "report_ym": report_ym,
        "gsc_clicks": g_curr["total_clicks"],
        "gsc_impr": g_curr["total_impr"],
        "gsc_ctr": g_curr["avg_ctr"],
        "brand_share": g_curr["tiers"]["品牌词"]["share"],
        "nb_share": g_curr["tiers"]["非品牌词"]["share"],
        "ga4_sessions": ga4_curr["sessions"],
        "ga4_users": ga4_curr["users"],
        "ga4_new_users": ga4_curr["new_users"],
        "ga4_bounce": ga4_curr["bounce"],
        "comp_core_rate": comp_curr["core_rate"],
        "homepage_clicks": home["clicks"],
        "tools_clicks": tools["clicks"],
        "pages_with_traffic": g_curr.get("pages_with_traffic", g_curr.get("index_pages", 0)),
        "index_rate": g_curr.get("index_rate", g_curr.get("index_rate_primary", 0)),
        "indexing_corpus_total": g_curr.get("indexing_corpus_total", 20_000),
    }
    (metrics_dir / f"{report_ym}.json").write_text(json.dumps(snap, indent=2, ensure_ascii=False))


def build_region_pages(cq_page_rows: list, country_group_fn) -> dict:
    buckets = defaultdict(lambda: defaultdict(lambda: {"clicks": 0, "impr": 0}))
    for rw in cq_page_rows:
        g = country_group_fn(rw["keys"][0])
        u = rw["keys"][1]
        buckets[g][u]["clicks"] += rw["clicks"]
        buckets[g][u]["impr"] += rw["impressions"]
    out = {}
    for g, pages in buckets.items():
        rows = []
        for u, v in pages.items():
            ctr = round(v["clicks"] / v["impr"] * 100, 1) if v["impr"] else 0
            rows.append({"url": u, **v, "ctr": ctr})
        out[g] = sorted(rows, key=lambda x: x["clicks"], reverse=True)[:15]
    return out


def keyword_movers(g_prev: dict, g_curr: dict, n: int = 15) -> tuple[list, list, list]:
    pm = {k["q"].lower(): k for k in g_prev["keywords"]}
    cm = {k["q"].lower(): k for k in g_curr["keywords"]}
    keys = set(pm) | set(cm)
    movers = []
    for q in keys:
        label = pm.get(q, cm.get(q, {"q": q})).get("q", q)
        if is_brand(label):
            continue
        a, b = pm.get(q, {"clicks": 0, "impr": 0, "ctr": 0, "q": q}), cm.get(q, {"clicks": 0, "impr": 0, "ctr": 0, "q": q})
        dc = b["clicks"] - a["clicks"]
        di = b["impr"] - a["impr"]
        movers.append({"q": b.get("q") or a.get("q"), "dc": dc, "di": di, "clicks": b["clicks"], "impr": b["impr"],
                       "ctr": b.get("ctr", 0), "ctr_delta": round(b.get("ctr", 0) - a.get("ctr", 0), 1)})
    by_click = sorted(movers, key=lambda x: x["dc"], reverse=True)[:n]
    by_click_down = sorted(movers, key=lambda x: x["dc"])[:n]
    by_impr = sorted(movers, key=lambda x: x["di"], reverse=True)[:n]
    return by_click, by_click_down, by_impr


def tiers_table_full(t_prev, t_curr, tier_names, pl, cl, chg_str, chg_f) -> str:
    lines = []
    for n in tier_names:
        ta, tb = t_prev[f"Top{n}"], t_curr[f"Top{n}"]
        lines.append(
            f"| Top {n} | {ta['count']} | {ta['clicks']:,} | {ta['impr']:,} | {ta['share']}% | {ta['ctr']}% | → | "
            f"{tb['count']} | {tb['clicks']:,} | {tb['impr']:,} | {tb['share']}% | {tb['ctr']}% | "
            f"{chg_str(ta['clicks'], tb['clicks'])} | {chg_str(ta['impr'], tb['impr'])} | {chg_f(ta['ctr'], tb['ctr'])} |"
        )
    return "\n".join(lines)


def top_by_impression(keywords: list, n: int = 15) -> list:
    return sorted(keywords, key=lambda x: x["impr"], reverse=True)[:n]


def _product_metric_row(label: str, prev_m: dict, curr_m: dict, key: str, chg_str, *, fmt: str = "int") -> str:
    a, b = prev_m.get(key, 0), curr_m.get(key, 0)
    if fmt == "money":
        av, bv = f"¥{round(a):,.0f}", f"¥{round(b):,.0f}"
        return f"| {label} | {av} | {bv} | {chg_str(round(a), round(b))} |"
    elif fmt == "pct":
        av, bv = f"{a:.2f}%", f"{b:.2f}%"
        d = round(b - a, 2)
        chg = f"{d:+.2f}pp" if a or b else "—"
        return f"| {label} | {av} | {bv} | {chg} |"
    elif fmt == "arppu":
        av, bv = f"¥{a:,.2f}", f"¥{b:,.2f}"
    else:
        av, bv = f"{int(a):,}", f"{int(b):,}"
    return f"| {label} | {av} | {bv} | {chg_str(a, b)} |"


def render_dau_share_card(sgeo_prev: dict | None, sgeo_curr: dict | None, pl: str, cl: str, chg_str) -> str:
    """SEO Dashboard 卡 A：全渠道 DAU 比例（DataWorks 日均）。"""
    share_prev = dau_share_pct(sgeo_prev)
    share_curr = dau_share_pct(sgeo_curr)
    if not share_curr:
        return ""
    rows = [
        "#### A. 全渠道 DAU 比例（DataWorks 日均）",
        "",
        f"| 渠道 | {pl} | {cl} | 环比 |",
        "|------|-----:|-----:|------|",
        _product_metric_row(
            "SEO+GEO 合计（`seo_geo_dau_share`）",
            share_prev, share_curr, "seo_geo_combined_pct", chg_str, fmt="pct",
        ),
        _product_metric_row("SEO", share_prev, share_curr, "seo_pct", chg_str, fmt="pct"),
        _product_metric_row("GEO", share_prev, share_curr, "geo_pct", chg_str, fmt="pct"),
        "",
        "> SEO / GEO 拆分占比 = 当日各渠道 UV ÷ `total_dau_uv` 的日均；合计行与底表 `seo_geo_dau_share` 对齐。",
        "",
    ]
    return "\n".join(rows)


def render_product_overview_card(sgeo_prev: dict | None, sgeo_curr: dict | None, pl: str, cl: str, chg_str) -> str:
    """SEO Dashboard 卡 B：自然搜索用户大盘数据（DataWorks 综合，SEO+GEO）。"""
    if not sgeo_curr:
        return (
            "#### B. 自然搜索用户大盘数据（DataWorks）\n\n> ⚠️ 未找到 DataWorks 文件："
            f"`1-2 Insight/From Datawork/{{YYYY-MM}} SEO GEO.xlsx`（见 AGENTS.md A0i）\n\n"
        )
    prev_nat, curr_nat = merge_natural_dedup(sgeo_prev, sgeo_curr)
    if not curr_nat.get("all_uv"):
        return "#### B. 自然搜索用户大盘数据（DataWorks）\n\n> ⚠️ DataWorks 日明细无有效 UV 行，请检查 xlsx 导出。\n\n"

    src = "月去重" if sgeo_curr.get("data_source") == "monthly_dedup" else "日明细加总"
    uv_label = "访问 UV（去重）" if sgeo_curr.get("has_monthly_dedup") else "访问 UV*"
    metric_rows = [
        _product_metric_row(uv_label, prev_nat, curr_nat, "all_uv", chg_str),
        _product_metric_row("新增注册 UV（new_uv）", prev_nat, curr_nat, "new_uv", chg_str),
        _product_metric_row("新增付费 UV（new_pay_uv）", prev_nat, curr_nat, "new_pay_uv", chg_str),
        _product_metric_row("新增付费金额（new_pay_amount）", prev_nat, curr_nat, "new_pay_amount", chg_str, fmt="money"),
        _product_metric_row("新增客单价（new_arppu）", prev_nat, curr_nat, "new_arppu", chg_str, fmt="arppu"),
        _product_metric_row("新增注册→付费转化率", prev_nat, curr_nat, "new_pay_rate", chg_str, fmt="pct"),
        _product_metric_row("累计付费 UV（all_pay_uv）", prev_nat, curr_nat, "all_pay_uv", chg_str),
        _product_metric_row("累计付费金额", prev_nat, curr_nat, "all_pay_amount", chg_str, fmt="money"),
        _product_metric_row("累计订单数", prev_nat, curr_nat, "all_order_cnt", chg_str),
        _product_metric_row("累计客单价 ARPPU", prev_nat, curr_nat, "all_arppu", chg_str, fmt="arppu"),
        _product_metric_row("访问→付费率（累计口径）", prev_nat, curr_nat, "all_pay_rate", chg_str, fmt="pct"),
        _product_metric_row("对话 UV（活跃）", prev_nat, curr_nat, "all_dialog_uv", chg_str),
        _product_metric_row("生成 UV（活跃）", prev_nat, curr_nat, "all_generate_uv", chg_str),
        _product_metric_row("导出 UV（活跃）", prev_nat, curr_nat, "all_export_uv", chg_str),
        _product_metric_row("对话渗透率", prev_nat, curr_nat, "all_dialog_rate", chg_str, fmt="pct"),
        _product_metric_row("D7 留存 UV", prev_nat, curr_nat, "all_retain_d7_uv", chg_str),
    ]
    lines = [
        f"#### B. 自然搜索用户大盘数据（DataWorks · {src}）",
        "",
        OKR_NATURAL_FOOTNOTE,
        "",
        NEW_VS_ALL_PAY_FOOTNOTE,
        "",
        f"| 指标（自然搜索 = SEO + GEO） | {pl} | {cl} | 环比 |",
        "|------|-----:|-----:|------|",
        "\n".join(metric_rows),
        "",
    ]
    if not sgeo_curr.get("has_monthly_dedup"):
        lines.append(DAILY_SUM_FOOTNOTE + "\n")
    lines.append(GA4_DATAWORK_FOOTNOTE + "\n")
    return "\n".join(lines)


def estimate_referral_uv(natural_uv: float, organic_sessions: float, referral_sessions: float) -> int:
    """Referral 无产品 UV：按 自然 UV × (Referral Sessions ÷ Organic Sessions) 估算。"""
    if not organic_sessions:
        return 0
    return round(natural_uv * referral_sessions / organic_sessions)


def okr_traffic_metrics(ga4_prev: dict, ga4_curr: dict, sgeo_prev: dict | None, sgeo_curr: dict | None) -> dict:
    """O1 访问 UV 用 DataWorks all_uv（自然 SEO+GEO）；O3 Referral UV 按 Sessions 比例估算。"""
    org_s, org_p = ga4_curr["sessions"], ga4_prev["sessions"]
    ref_s = ga4_curr["channels"].get("Referral", {}).get("sessions", 0)
    ref_p = ga4_prev["channels"].get("Referral", {}).get("sessions", 0)
    prev_nat, curr_nat = merge_natural_dedup(sgeo_prev, sgeo_curr) if sgeo_curr else ({}, {})
    uv_p = int(prev_nat.get("all_uv", 0)) or org_p
    uv_c = int(curr_nat.get("all_uv", 0)) or org_s
    return {
        "uv_p": uv_p, "uv_c": uv_c,
        "ref_uv_p": estimate_referral_uv(uv_p, org_p, ref_p),
        "ref_uv_c": estimate_referral_uv(uv_c, org_s, ref_s),
        "org_s": org_s, "org_p": org_p,
        "ref_s": ref_s, "ref_p": ref_p,
        "has_uv": bool(curr_nat.get("all_uv")),
    }


def render_okr_section(
    ga4_curr: dict,
    ga4_prev: dict,
    pl: str,
    cl: str,
    chg_str,
    sgeo_prev: dict | None = None,
    sgeo_curr: dict | None = None,
) -> str:
    org_s, org_p = ga4_curr["sessions"], ga4_prev["sessions"]
    o1 = OKR["O1"]
    o3 = OKR["O3"]
    tm = okr_traffic_metrics(ga4_prev, ga4_curr, sgeo_prev, sgeo_curr)
    uv_p, uv_c = tm["uv_p"], tm["uv_c"]
    ref_uv_p, ref_uv_c = tm["ref_uv_p"], tm["ref_uv_c"]
    ref_s, ref_p = tm["ref_s"], tm["ref_p"]
    rreg_p = round(ref_uv_p * o3["ref_reg_rate"])
    rreg_c = round(ref_uv_c * o3["ref_reg_rate"])
    if sgeo_curr:
        pm = natural_pay_metrics(sgeo_prev, sgeo_curr)
        reg_p, reg_c = pm["reg_p"], pm["reg_c"]
        new_pay_p, new_pay_c = pm["new_pay_p"], pm["new_pay_c"]
        all_pay_p, all_pay_c = pm["all_pay_p"], pm["all_pay_c"]
        reg_ach = pct_str(reg_c, o1["reg_month"])
        pay_ach = pct_str(new_pay_c, o1["pay_month"])
        reg_chg = chg_str(reg_p, reg_c)
        new_pay_chg = chg_str(new_pay_p, new_pay_c)
        all_pay_chg = chg_str(all_pay_p, all_pay_c)
        uv_label = "访问 UV（自然 SEO+GEO，all_uv）"
    else:
        reg_p, reg_c = round(org_p * o1["reg_rate"]), round(org_s * o1["reg_rate"])
        new_pay_p = new_pay_c = round(reg_c * o1["pay_rate"])
        all_pay_p = all_pay_c = 0
        reg_ach = pct_str(reg_c, o1["reg_month"])
        pay_ach = pct_str(new_pay_c, o1["pay_month"])
        reg_chg = chg_str(reg_p, reg_c)
        new_pay_chg = all_pay_chg = "—"
        uv_label = "访问 UV（GA4 Organic Sessions 代理）"
    base = f"""## 二、OKR 月达成看板

> O1 **访问 UV** 以 DataWorks 自然搜索（SEO+GEO）`all_uv` 计达成率与环比；GA4 Organic Sessions 仅作渠道参考。**新增注册 / 新增付费** 用 `new_uv` / `new_pay_uv`（产品大盘见 §三 Dashboard 卡 B）。O3 Referral 无产品 UV，按 **自然 UV × (Referral Sessions ÷ Organic Sessions)** 估算；分区浏览数据用 GA4 Sessions。

| OKR | 指标 | 月目标 | {pl} | {cl} | {cl}达成率 | 环比 |
|-----|------|:------:|-----:|-----:|:---------:|------|
| O1 | {uv_label} | {o1['organic_uv_month']:,} | {uv_p:,} | {uv_c:,} | {pct_str(uv_c, o1['organic_uv_month'])} | {chg_str(uv_p, uv_c)} |
| O1 | 新增注册 UV | {o1['reg_month']:,} | {reg_p:,} | {reg_c:,} | {reg_ach} | {reg_chg} |
| O1 | 新增付费 UV | {o1['pay_month']:,} | {new_pay_p:,} | {new_pay_c:,} | {pay_ach} | {new_pay_chg} |
| O1 | 累计付费 UV（对照） | — | {all_pay_p:,} | {all_pay_c:,} | — | {all_pay_chg} |
| O3 | Referral 访问 UV（估算） | {o3['referral_uv_month']:,} | {ref_uv_p:,} | {ref_uv_c:,} | {pct_str(ref_uv_c, o3['referral_uv_month'])} | {chg_str(ref_uv_p, ref_uv_c)} |
| O3 | 注册（估） | {o3['reg_month']:,} | {rreg_p:,} | {rreg_c:,} | {pct_str(rreg_c, o3['reg_month'])} | {chg_str(rreg_p, rreg_c)} |
| 参考 | GA4 Organic Sessions | — | {org_p:,} | {org_s:,} | — | {chg_str(org_p, org_s)} |
| 参考 | GA4 Referral Sessions | — | {ref_p:,} | {ref_s:,} | — | {chg_str(ref_p, ref_s)} |
| O2 | 全渠道质量 | — | 跳出 {ga4_prev['bounce']}% | 跳出 {ga4_curr['bounce']}% | 页/次 {ga4_curr['pages_per_session']} | {chg_str(ga4_prev['sessions'], org_s)} |

> 产品大盘（访问/注册/付费/活跃全量明细）见 §三 SEO Dashboard 卡 B。

"""
    return base


def share_pp_chg(prev_share: float, curr_share: float) -> str:
    d = round(curr_share - prev_share, 1)
    return f"{d:+.1f}pp"


def _kw_map_by_q(rows: list) -> dict:
    return {k["q"].lower(): k for k in rows}


def _dual_kw_rows(pl: str, cl: str, prev_list: list, curr_list: list, chg_str, n: int = 15) -> str:
    pm, cm = _kw_map_by_q(prev_list), _kw_map_by_q(curr_list)
    keys = sorted(set(cm) | set(pm), key=lambda q: cm.get(q, pm.get(q, {"clicks": 0}))["clicks"], reverse=True)[:n]
    lines = [
        f"| # | 关键词 | {pl} 点击 | {pl} 曝光 | {cl} 点击 | {cl} 曝光 | {cl} CTR | 点击环比 |",
        "|---|--------|----------|----------|----------|----------|---------|----------|",
    ]
    for i, qk in enumerate(keys):
        a = pm.get(qk, {"q": qk, "clicks": 0, "impr": 0, "ctr": 0})
        b = cm.get(qk, {"q": qk, "clicks": 0, "impr": 0, "ctr": 0})
        lines.append(
            f"| {i+1} | {(b.get('q') or a.get('q'))[:36]} | {a['clicks']:,} | {a['impr']:,} | "
            f"{b['clicks']:,} | {b['impr']:,} | {b.get('ctr', 0)}% | {chg_str(a['clicks'], b['clicks'])} |"
        )
    return "\n".join(lines) + "\n"


def render_executive_dashboards(
    g_prev, g_curr, ga4_prev, ga4_curr, comp_prev, comp_curr, pl, cl, chg_str, chg_f, b_prev, b_curr, nb_prev, nb_curr,
    sgeo_prev=None, sgeo_curr=None,
    bing_prev=None, bing_curr=None, bing_in_index: int | None = None,
) -> str:
    org_p = ga4_prev["channels"].get("Organic Search", {}).get("share", 0)
    org_c = ga4_curr["channels"].get("Organic Search", {}).get("share", 0)
    ix_note = (
        f"> 收录口径：有搜索曝光 URL / 语料库 {g_curr.get('indexing_corpus_total', 20000):,}（非 Sitemap 提交量÷1000）"
    )
    sm_idx = g_curr.get("sitemap_index_rate")
    sm_line = f" | Sitemap 索引率 {sm_idx}%" if sm_idx else ""
    dau_card = render_dau_share_card(sgeo_prev, sgeo_curr, pl, cl, chg_str)
    product_card = render_product_overview_card(sgeo_prev, sgeo_curr, pl, cl, chg_str)
    return f"""## 三、SEO Dashboard

{dau_card}
{product_card}
#### C. GSC 关键词全站

| 指标 | {pl} | {cl} | 环比 |
|------|-----|-----|------|
| 拉取词数 | {g_prev['keyword_count']:,} | {g_curr['keyword_count']:,} | — |
| 总曝光 | {g_prev['total_impr']:,} | {g_curr['total_impr']:,} | {chg_str(g_prev['total_impr'], g_curr['total_impr'])} |
| 总点击 | {g_prev['total_clicks']:,} | {g_curr['total_clicks']:,} | {chg_str(g_prev['total_clicks'], g_curr['total_clicks'])} |
| 整体 CTR | {g_prev['avg_ctr']}% | {g_curr['avg_ctr']}% | {chg_f(g_prev['avg_ctr'], g_curr['avg_ctr'])} |
| 平均排名 | {g_prev['avg_pos']:.1f} | {g_curr['avg_pos']:.1f} | {chg_f(g_prev['avg_pos'], g_curr['avg_pos'])} |

{render_bing_dashboard_cards(bing_prev, bing_curr, pl, cl, chg_str, chg_f, bing_in_index)}
#### D. Top 分层（点击 / 曝光 / CTR / 点击占比）

| 分层 | {pl} 点击 | {pl} 曝光 | {pl} CTR | {pl} 占比 | → | {cl} 点击 | {cl} 曝光 | {cl} CTR | {cl} 占比 | 点击环比 | 曝光环比 |
|------|----------|----------|---------|---------|---|----------|----------|---------|---------|----------|----------|
{tiers_table_full(g_prev['tiers'], g_curr['tiers'], [3, 10, 50], pl, cl, chg_str, chg_f)}

#### E. 品牌 vs 非品牌

| 指标 | {pl} | {cl} | 环比 |
|------|-----|-----|------|
| 品牌词数 | {b_prev['count']} | {b_curr['count']} | {chg_str(b_prev['count'], b_curr['count'])} |
| 品牌曝光 | {b_prev['impr']:,} | {b_curr['impr']:,} | {chg_str(b_prev['impr'], b_curr['impr'])} |
| 品牌点击 | {b_prev['clicks']:,} | {b_curr['clicks']:,} | {chg_str(b_prev['clicks'], b_curr['clicks'])} |
| 品牌 CTR | {b_prev['ctr']}% | {b_curr['ctr']}% | {chg_f(b_prev['ctr'], b_curr['ctr'])} |
| 品牌点击占比 | {b_prev['share']}% | {b_curr['share']}% | {share_pp_chg(b_prev['share'], b_curr['share'])} |
| 非品牌词数 | {nb_prev['count']} | {nb_curr['count']} | {chg_str(nb_prev['count'], nb_curr['count'])} |
| 非品牌曝光 | {nb_prev['impr']:,} | {nb_curr['impr']:,} | {chg_str(nb_prev['impr'], nb_curr['impr'])} |
| 非品牌点击 | {nb_prev['clicks']:,} | {nb_curr['clicks']:,} | {chg_str(nb_prev['clicks'], nb_curr['clicks'])} |
| 非品牌 CTR | {nb_prev['ctr']}% | {nb_curr['ctr']}% | {chg_f(nb_prev['ctr'], nb_curr['ctr'])} |
| 非品牌点击占比 | {nb_prev['share']}% | {nb_curr['share']}% | {share_pp_chg(nb_prev['share'], nb_curr['share'])} |

#### F. GA4 自然搜索 + 收录 + 竞品

| 指标 | {pl} | {cl} | 环比 |
|------|-----|-----|------|
| Sessions | {ga4_prev['sessions']:,} | {ga4_curr['sessions']:,} | {chg_str(ga4_prev['sessions'], ga4_curr['sessions'])} |
| Users | {ga4_prev['users']:,} | {ga4_curr['users']:,} | {chg_str(ga4_prev['users'], ga4_curr['users'])} |
| New Users | {ga4_prev['new_users']:,} | {ga4_curr['new_users']:,} | {chg_str(ga4_prev['new_users'], ga4_curr['new_users'])} |
| 跳出率 | {ga4_prev['bounce']}% | {ga4_curr['bounce']}% | {chg_f(ga4_prev['bounce'], ga4_curr['bounce'])} |
| 页/次 | {ga4_prev['pages_per_session']} | {ga4_curr['pages_per_session']} | {chg_f(ga4_prev['pages_per_session'], ga4_curr['pages_per_session'])} |
| Organic 渠道占比 | {org_p}% | {org_c}% | {share_pp_chg(org_p, org_c)} |
| 有曝光 URL 数 | {g_prev.get('pages_with_traffic', g_prev.get('index_pages', 0)):,} | {g_curr.get('pages_with_traffic', g_curr.get('index_pages', 0)):,} | {chg_str(g_prev.get('pages_with_traffic', 0), g_curr.get('pages_with_traffic', 0))} |
| 收录率（主口径） | {g_prev.get('index_rate', 0)}% | {g_curr.get('index_rate', 0)}% | {share_pp_chg(g_prev.get('index_rate', 0), g_curr.get('index_rate', 0))} |
| Core 竞品覆盖（Google） | {comp_prev['unique_core']}/{comp_prev['core_total']} ({comp_prev['core_rate']}%) | {comp_curr['unique_core']}/{comp_curr['core_total']} ({comp_curr['core_rate']}%) | {chg_str(comp_prev['unique_core'], comp_curr['unique_core'])} |
| Full 竞品覆盖（Google） | {comp_prev['unique_full']}/{comp_prev['comp_total']} ({comp_prev['full_rate']}%) | {comp_curr['unique_full']}/{comp_curr['comp_total']} ({comp_curr['full_rate']}%) | {chg_str(comp_prev['unique_full'], comp_curr['unique_full'])} |
| Core 竞品覆盖（Bing） | — | {((bing_curr or {}).get('comp') or {}).get('unique_core', 0)}/{((bing_curr or {}).get('comp') or {}).get('core_total', 0)} ({((bing_curr or {}).get('comp') or {}).get('core_rate', 0)}%) | — |
| Full 竞品覆盖（Bing） | — | {((bing_curr or {}).get('comp') or {}).get('unique_full', 0)}/{((bing_curr or {}).get('comp') or {}).get('comp_total', 0)} ({((bing_curr or {}).get('comp') or {}).get('full_rate', 0)}%) | — |

{ix_note}{sm_line}

"""


def render_seo_geo_section(sgeo_prev: dict | None, sgeo_curr: dict | None, pl: str, cl: str, chg_str) -> str:
    if not sgeo_curr:
        return ""
    daily = sgeo_curr.get("daily") or {}
    by_ch = daily.get("by_channel") or {}
    if not by_ch:
        return ""

    out = f"""
---

## 六、自然搜索产品数据（DataWorks 平台拆解）

> `organic_discovery_type`：**seo** = 搜索引擎；**geo** = AI/对话式发现（ChatGPT、豆包等）。**O1 自然搜索**含 SEO+GEO（见 OKR 脚注）。

{GA4_DATAWORK_FOOTNOTE}

"""
    totals = sgeo_curr.get("channel_totals") or {}
    if totals:
        out += "### 6.1 渠道汇总（SEO / GEO / 合计）\n\n"
        out += (
            "| 渠道 | 访问 UV* | 新增注册 | 新增付费 UV | 新增付费额 | 累计付费 UV | 新增注册→付费 | 对话 |\n"
            "|------|-----:|-----:|--------:|--------:|--------:|--------:|-----:|\n"
        )
        for ch, title in (("seo", "SEO"), ("geo", "GEO"), ("natural", "合计")):
            cur = totals.get(ch) or {}
            if not cur.get("all_uv"):
                continue
            out += (
                f"| {title} | {cur['all_uv']:,.0f} | {cur.get('new_uv', 0):,.0f} | "
                f"{cur.get('new_pay_uv', 0):,.0f} | ¥{cur.get('new_pay_amount', 0):,.0f} | "
                f"{cur.get('all_pay_uv', 0):,.0f} | {cur.get('new_pay_rate', 0)}% | "
                f"{cur.get('all_dialog_uv', 0):,.0f} |\n"
            )
        out += "\n"
        if not sgeo_curr.get("has_monthly_dedup"):
            out += DAILY_SUM_FOOTNOTE + "\n\n"

    for ch, title in (("seo", "SEO 搜索引擎"), ("geo", "GEO / AI 发现")):
        chd = by_ch.get(ch)
        if not chd:
            continue
        out += f"### 6.{2 if ch=='seo' else 3} {title} — Top 平台（{cl}，日明细结构）\n\n"
        out += (
            f"| # | 平台 | UV* | 新增注册 | 新增付费 | 新增付费额 | 累计付费 | 新增→付费 | 对话 |\n"
            f"|---|------|-----:|-----:|--------:|--------:|--------:|--------:|-----:|\n"
        )
        for i, p in enumerate(chd.get("platforms", [])[:12], 1):
            out += (
                f"| {i} | {p['platform']} | {p['all_uv']:,.0f} | {p.get('new_uv', 0):,.0f} | "
                f"{p.get('new_pay_uv', 0):,.0f} | ¥{p.get('new_pay_amount', 0):,.0f} | "
                f"{p['all_pay_uv']:,.0f} | {p.get('new_pay_rate', 0)}% | "
                f"{p.get('all_dialog_uv', 0):,.0f} |\n"
            )
        out += "\n"

    seo_p = by_ch.get("seo", {}).get("platforms", [])
    geo_p = by_ch.get("geo", {}).get("platforms", [])

    # 6.4 引擎对比：Google vs Bing（Microsoft）全漏斗
    def _find(plats, name):
        return next((p for p in plats if p.get("platform") == name), {})
    prev_seo_p = ((sgeo_prev or {}).get("daily") or {}).get("by_channel", {}).get("seo", {}).get("platforms", []) if sgeo_prev else []
    g_c, b_c = _find(seo_p, "google"), _find(seo_p, "microsoft")
    g_p, b_p = _find(prev_seo_p, "google"), _find(prev_seo_p, "microsoft")
    if g_c and b_c:
        def cell(curr, prev, key, fmt):
            cv, pv = curr.get(key, 0) or 0, prev.get(key, 0) or 0
            if fmt == "money":
                return f"¥{cv:,.0f}（{chg_str(round(pv), round(cv))}）"
            if fmt == "arppu":
                d = cv - pv
                p = (d / pv * 100) if pv else 0
                arrow = "↑" if d > 0 else ("↓" if d < 0 else "→")
                return f"¥{cv:,.1f}（{arrow}{d:+.1f} / {p:+.1f}%）"
            return f"{cv:,.0f}（{chg_str(round(pv), round(cv))}）"
        rows = [
            ("访问 UV", "all_uv", "int"), ("新增访问 UV", "new_uv", "int"),
            ("新增付费 UV", "new_pay_uv", "int"), ("新增付费额", "new_pay_amount", "money"),
            ("新增客单价", "new_arppu", "arppu"), ("累计付费 UV", "all_pay_uv", "int"),
            ("累计付费额", "all_pay_amount", "money"), ("累计客单价", "all_arppu", "arppu"),
            ("对话 UV", "all_dialog_uv", "int"), ("生成 UV", "all_generate_uv", "int"),
        ]
        out += "### 6.4 引擎对比：Google vs Bing（Microsoft，DataWorks 全漏斗 · 环比）\n\n"
        out += "| 指标 | Google | Bing(Microsoft) | Google 占两者 |\n|------|-------|----------------|:----:|\n"
        for label, key, fmt in rows:
            gv, bv = g_c.get(key, 0) or 0, b_c.get(key, 0) or 0
            share = f"{gv/(gv+bv)*100:.0f}%" if (gv + bv) else "—"
            out += f"| {label} | {cell(g_c, g_p, key, fmt)} | {cell(b_c, b_p, key, fmt)} | {share} |\n"
        out += "\n"
        g_payrate = (g_c.get("new_pay_uv", 0) / g_c.get("new_uv", 1) * 100) if g_c.get("new_uv") else 0
        b_payrate = (b_c.get("new_pay_uv", 0) / b_c.get("new_uv", 1) * 100) if b_c.get("new_uv") else 0
        out += (
            f"> 💡 **引擎差异（产品转化）** — 访问体量 Google 约为 Bing 的 {g_c.get('all_uv',0)/max(b_c.get('all_uv',1),1):.1f}×，"
            f"但 Bing 新增付费转化率 **{b_payrate:.2f}%** vs Google **{g_payrate:.2f}%**、新增客单价 ¥{b_c.get('new_arppu',0):,.1f} vs ¥{g_c.get('new_arppu',0):,.1f}"
            f"（{'Bing 流量更小但变现效率更高 → 值得在 Bing 单独加大非品牌/内页投入' if b_payrate >= g_payrate else 'Google 变现效率更高'}）。\n\n"
        )

    if seo_p and geo_p:
        out += (
            f"> 💡 **SEO vs GEO** — SEO 体量集中在 {seo_p[0]['platform']}；"
            f"GEO 付费率通常高于 SEO（样本：{geo_p[0]['platform']} {geo_p[0].get('pay_rate', geo_p[0].get('new_pay_rate',0))}%）。"
            " 优化重点：高 UV 平台拉付费墙/对话转化；GEO 做品牌占位与深链。\n\n"
        )
    return out


def section_insight_ga4_with_product(
    ga4_curr: dict, ga4_prev: dict, chg_str, sgeo_curr: dict | None = None,
) -> str:
    base = section_insight_ga4(ga4_curr, ga4_prev, chg_str)
    if not sgeo_curr:
        return base
    nat = channel_metrics(sgeo_curr, "natural")
    if not nat.get("all_uv"):
        return base
    dlg = round(nat.get("all_dialog_uv", 0) / nat["all_uv"] * 100, 1) if nat.get("all_uv") else 0
    uv_note = "去重" if sgeo_curr.get("has_monthly_dedup") else "加总"
    return base + (
        f"\n> 📊 **产品实数（{uv_note}）** — 访问 {nat.get('all_uv', 0):,.0f}、新增注册 {nat.get('new_uv', 0):,.0f}、"
        f"**新增付费** {nat.get('new_pay_uv', 0):,.0f}（¥{nat.get('new_pay_amount', 0):,.0f}）、"
        f"累计付费 {nat.get('all_pay_uv', 0):,.0f}、新增注册→付费 {nat.get('new_pay_rate', 0)}%、对话渗透 {dlg}%（SEO+GEO）。\n"
    )


def render_region_executive_summary(
    region_order: list,
    reg_prev: dict,
    reg_curr: dict,
    rs_prev: dict,
    rs_curr: dict,
    reg_ga4_prev: dict,
    reg_ga4_curr: dict,
    pl: str,
    cl: str,
    chg_str,
    *,
    brief: bool = False,
) -> str:
    rows = []
    for grp in region_order:
        a = reg_prev.get(grp, {"clicks": 0, "impr": 1})
        b = reg_curr.get(grp, {"clicks": 0, "impr": 1})
        if b["clicks"] + a["clicks"] == 0:
            continue
        dc = b["clicks"] - a["clicks"]
        pct = round(dc / a["clicks"] * 100, 1) if a["clicks"] else 0
        sp = rs_prev.get(grp, {"brand": {"clicks": 0}, "nonbrand": {"clicks": 0}})
        sc = rs_curr.get(grp, {"brand": {"clicks": 0}, "nonbrand": {"clicks": 0}})
        bshare = round(sc["brand"]["clicks"] / b["clicks"] * 100, 1) if b["clicks"] else 0
        ga_gap = reg_ga4_curr.get(grp, {}).get("sessions", 0) - b["clicks"]
        rows.append({"grp": grp, "dc": dc, "pct": pct, "bshare": bshare, "ga_gap": ga_gap, "clicks": b["clicks"]})

    if not rows:
        return ""
    rows.sort(key=lambda x: x["pct"], reverse=True)
    best = [r for r in rows if r["pct"] > 2][:3]
    flat = [r for r in rows if -2 <= r["pct"] <= 2][:3]
    worst = sorted([r for r in rows if r["pct"] < -2], key=lambda x: x["pct"])[:3]

    def fmt(lst, label):
        if not lst:
            return f"- **{label}**：无显著变化\n"
        return "- **" + label + "**：" + "；".join(
            f"{r['grp']}（{chg_str((reg_prev.get(r['grp']) or {}).get('clicks', 0), (reg_curr.get(r['grp']) or {}).get('clicks', 0))}, 品牌占比{r['bshare']}%）" for r in lst
        ) + "\n"

    body = f"""{fmt(best, '表现最好')}{fmt(flat, '基本持平')}{fmt(worst, '表现最差')}
> 💡 **大区策略** — 优先在「表现最差」大区复制「表现最好」区的非品牌词 landing 模板；GA4 与 GSC 缺口大的区（如大中华）单独排查渠道与品牌词污染。
"""
    if brief:
        return body.strip() + "\n"
    return f"""
### 11.0 大区表现总览（{pl} vs {cl}）

{body}
"""


def region_mini_block(
    grp: str,
    pl: str,
    cl: str,
    reg_prev: dict,
    reg_curr: dict,
    rs_prev: dict,
    rs_curr: dict,
    ga4_prev: dict,
    ga4_curr: dict,
    brand_top: list,
    nb_top: list,
    brand_top_prev: list,
    nb_top_prev: list,
    pages: list,
    pages_prev: list,
    total_cl_prev: float,
    total_cl_curr: float,
    total_im_prev: float,
    total_im_curr: float,
    chg_str,
    chg_f,
    format_page_path,
) -> str:
    a = reg_prev.get(grp, {"clicks": 0, "impr": 1})
    b = reg_curr.get(grp, {"clicks": 0, "impr": 1})
    sp = rs_prev.get(grp, {"brand": {"clicks": 0, "impr": 0}, "nonbrand": {"clicks": 0, "impr": 0}})
    sc = rs_curr.get(grp, {"brand": {"clicks": 0, "impr": 0}, "nonbrand": {"clicks": 0, "impr": 0}})
    ga = ga4_prev.get(grp, {"sessions": 0, "users": 0})
    gb = ga4_curr.get(grp, {"sessions": 0, "users": 0})
    a_ctr = round(a["clicks"] / a["impr"] * 100, 1) if a["impr"] else 0
    b_ctr = round(b["clicks"] / b["impr"] * 100, 1) if b["impr"] else 0
    a_cl_share = round(a["clicks"] / total_cl_prev * 100, 1) if total_cl_prev else 0
    b_cl_share = round(b["clicks"] / total_cl_curr * 100, 1) if total_cl_curr else 0
    a_im_share = round(a["impr"] / total_im_prev * 100, 1) if total_im_prev else 0
    b_im_share = round(b["impr"] / total_im_curr * 100, 1) if total_im_curr else 0
    sp_b_ctr = round(sp["brand"]["clicks"] / sp["brand"]["impr"] * 100, 1) if sp["brand"]["impr"] else 0
    sc_b_ctr = round(sc["brand"]["clicks"] / sc["brand"]["impr"] * 100, 1) if sc["brand"]["impr"] else 0
    sp_nb_ctr = round(sp["nonbrand"]["clicks"] / sp["nonbrand"]["impr"] * 100, 1) if sp["nonbrand"]["impr"] else 0
    sc_nb_ctr = round(sc["nonbrand"]["clicks"] / sc["nonbrand"]["impr"] * 100, 1) if sc["nonbrand"]["impr"] else 0

    block = f"""
### 11.x {grp} — 分区月报（{pl} vs {cl}）

#### GSC 汇总

| 指标 | {pl} | {cl} | 环比 |
|------|-----|-----|------|
| 点击 | {a['clicks']:,} | {b['clicks']:,} | {chg_str(a['clicks'], b['clicks'])} |
| 曝光 | {a['impr']:,} | {b['impr']:,} | {chg_str(a['impr'], b['impr'])} |
| CTR | {a_ctr}% | {b_ctr}% | {chg_f(a_ctr, b_ctr)} |
| 点击占比 | {a_cl_share}% | {b_cl_share}% | {share_pp_chg(a_cl_share, b_cl_share)} |
| 曝光占比 | {a_im_share}% | {b_im_share}% | {share_pp_chg(a_im_share, b_im_share)} |

#### 品牌 vs 非品牌

| 类型 | {pl} 点击 | {pl} 曝光 | {pl} CTR | {cl} 点击 | {cl} 曝光 | {cl} CTR | 点击环比 | 曝光环比 |
|------|----------|----------|---------|----------|----------|---------|----------|----------|
| 品牌 | {sp['brand']['clicks']:,} | {sp['brand']['impr']:,} | {sp_b_ctr}% | {sc['brand']['clicks']:,} | {sc['brand']['impr']:,} | {sc_b_ctr}% | {chg_str(sp['brand']['clicks'], sc['brand']['clicks'])} | {chg_str(sp['brand']['impr'], sc['brand']['impr'])} |
| 非品牌 | {sp['nonbrand']['clicks']:,} | {sp['nonbrand']['impr']:,} | {sp_nb_ctr}% | {sc['nonbrand']['clicks']:,} | {sc['nonbrand']['impr']:,} | {sc_nb_ctr}% | {chg_str(sp['nonbrand']['clicks'], sc['nonbrand']['clicks'])} | {chg_str(sp['nonbrand']['impr'], sc['nonbrand']['impr'])} |

#### Top 15 品牌词（双月）

"""
    block += _dual_kw_rows(pl, cl, brand_top_prev, brand_top, chg_str)
    block += "#### Top 15 非品牌词（双月）\n\n"
    block += _dual_kw_rows(pl, cl, nb_top_prev, nb_top, chg_str)
    block += f"""
#### GA4 Organic

| 指标 | {pl} | {cl} | 环比 |
|------|-----|-----|------|
| Sessions | {ga['sessions']:,} | {gb['sessions']:,} | {chg_str(ga['sessions'], gb['sessions'])} |
| Users | {ga['users']:,} | {gb['users']:,} | {chg_str(ga['users'], gb['users'])} |

#### Top 10 页面（GSC，双月点击）

| # | URL | {pl} 点击 | {cl} 点击 | 点击环比 |
|---|-----|----------|----------|----------|
"""
    pp = {format_page_path(p["url"]): p for p in pages_prev}
    for i, p in enumerate(pages[:10]):
        u = format_page_path(p["url"])
        prev_p = pp.get(u, {"clicks": 0})
        block += f"| {i+1} | {u[:45]} | {prev_p['clicks']:,} | {p['clicks']:,} | {chg_str(prev_p['clicks'], p['clicks'])} |\n"
    sc = rs_curr.get(grp, {"brand": {"clicks": 0, "impr": 0}, "nonbrand": {"clicks": 0, "impr": 0}})
    block += section_insight_region(grp, b, sc, gb)
    return block


def section_insight_region(grp, reg_totals: dict, reg_split: dict, ga4_curr: dict) -> str:
    b = reg_totals
    sc = reg_split
    brand_share = round(sc["brand"]["clicks"] / b["clicks"] * 100, 1) if b.get("clicks") else 0
    return f"""
> 💡 **{grp}** — 品牌点击占比 {brand_share}%。**问题**：非品牌词布局不足时增长靠品牌拉动。**积极信号**：GA4 sessions {ga4_curr.get('sessions', 0):,} 可对照 GSC 点击排查渠道差异。**缓解**：优先在该区 Top15 非品牌词上建/优化 landing page，并用首页内链导流。
"""


def enrich_core_ctx_with_product(
    ctx: dict,
    sgeo_prev: dict | None,
    sgeo_curr: dict | None,
    chg_str,
) -> dict:
    """注入 DataWorks 自然搜索（SEO+GEO）产品指标与转化率，供核心洞察（一）（三）使用。"""
    prev_nat, curr_nat = merge_natural_dedup(sgeo_prev, sgeo_curr)
    pm = natural_pay_metrics(sgeo_prev, sgeo_curr or {})
    uv_p, uv_c = int(prev_nat.get("all_uv", 0)), int(curr_nat.get("all_uv", 0))
    reg_p, reg_c = pm["reg_p"], pm["reg_c"]
    new_pay_p, new_pay_c = pm["new_pay_p"], pm["new_pay_c"]
    all_pay_p, all_pay_c = pm["all_pay_p"], pm["all_pay_c"]
    new_amt_p, new_amt_c = pm["new_pay_amt_p"], pm["new_pay_amt_c"]

    def reg_conv(nat: dict) -> float:
        uv = nat.get("all_uv", 0)
        return round(nat.get("new_uv", 0) / uv * 100, 2) if uv else 0.0

    rc_prev, rc_curr = reg_conv(prev_nat), reg_conv(curr_nat)
    npr_prev = prev_nat.get("new_pay_rate", 0)
    npr_curr = curr_nat.get("new_pay_rate", 0)
    reg_to_pay_str = f"{npr_prev}%→{npr_curr}%（{share_pp_chg(npr_prev, npr_curr)}，new_pay_uv/new_uv）"

    seo_c = channel_metrics(sgeo_curr, "seo") if sgeo_curr else {}
    geo_c = channel_metrics(sgeo_curr, "geo") if sgeo_curr else {}
    share_c = dau_share_pct(sgeo_curr)
    ctx.update({
        "has_product": bool(curr_nat.get("all_uv")),
        "uv_p": uv_p, "uv_c": uv_c,
        "uv_chg": chg_str(uv_p, uv_c),
        "reg_p": reg_p, "reg_c": reg_c,
        "reg_chg": chg_str(reg_p, reg_c),
        "new_pay_p": new_pay_p, "new_pay_c": new_pay_c,
        "new_pay_chg": chg_str(new_pay_p, new_pay_c),
        "all_pay_p": all_pay_p, "all_pay_c": all_pay_c,
        "all_pay_chg": chg_str(all_pay_p, all_pay_c),
        "new_amt_p": new_amt_p, "new_amt_c": new_amt_c,
        "new_amt_chg": chg_str(new_amt_p, new_amt_c),
        "reg_conv_prev": rc_prev,
        "reg_conv_curr": rc_curr,
        "reg_conv_pp": share_pp_chg(rc_prev, rc_curr),
        "new_pay_rate_prev": npr_prev,
        "new_pay_rate_curr": npr_curr,
        "new_pay_rate_pp": share_pp_chg(npr_prev, npr_curr),
        "pay_rate_prev": prev_nat.get("all_pay_rate", 0),
        "pay_rate_curr": curr_nat.get("all_pay_rate", 0),
        "pay_rate_pp": share_pp_chg(prev_nat.get("all_pay_rate", 0), curr_nat.get("all_pay_rate", 0)),
        "reg_to_pay_str": reg_to_pay_str,
        "seo_uv": int(seo_c.get("all_uv", 0)),
        "geo_uv": int(geo_c.get("all_uv", 0)),
        "seo_dau_pct": share_c.get("seo_pct", 0),
        "geo_dau_pct": share_c.get("geo_pct", 0),
        "seo_geo_dau_pct": share_c.get("seo_geo_combined_pct", 0),
        "okr_reg_pct": pct_str(reg_c, OKR["O1"]["reg_month"]),
        "okr_pay_pct": pct_str(new_pay_c, OKR["O1"]["pay_month"]),
        "dialog_chg": chg_str(int(prev_nat.get("all_dialog_uv", 0)), int(curr_nat.get("all_dialog_uv", 0))),
    })
    return ctx


def load_content_inventory() -> dict:
    p = TRIDENT_REPORTS / "content-inventory.json"
    if p.exists():
        return json.loads(p.read_text())
    return {"blog": 0, "features": 0, "tools": 0}


def enrich_core_ctx_with_platforms(ctx: dict, sgeo_curr: dict | None) -> dict:
    """GEO vs SEO 平台新增注册→付费率，供 §一 全链路叙事。"""
    by = ((sgeo_curr or {}).get("daily") or {}).get("by_channel") or {}
    geo_labels = {"doubao": "豆包", "chatgpt": "ChatGPT", "baidu": "百度"}
    seo_labels = {"google": "Google", "microsoft": "Microsoft", "baidu": "百度"}
    geo_rates, geo_parts = [], []
    for p in (by.get("geo") or {}).get("platforms") or []:
        name = p.get("platform", "")
        if name in geo_labels and (p.get("new_uv") or 0) >= 10:
            rate = float(p.get("new_pay_rate") or 0)
            geo_rates.append(rate)
            geo_parts.append(f"{geo_labels[name]} **{rate}%**")
    seo_parts = []
    for p in (by.get("seo") or {}).get("platforms") or []:
        name = p.get("platform", "")
        if name in seo_labels and (p.get("new_uv") or 0) >= 100:
            seo_parts.append(f"{seo_labels[name]} **{float(p.get('new_pay_rate') or 0)}%**")
    seo_top3 = "、".join(seo_parts[:3]) if seo_parts else "—"
    geo_top = "、".join(geo_parts[:3]) if geo_parts else "—"
    geo_avg = round(sum(geo_rates) / len(geo_rates), 1) if geo_rates else 0
    ctx.update({
        "geo_pay_avg": geo_avg,
        "geo_pay_platforms": geo_top,
        "seo_pay_platforms": seo_top3,
    })
    return ctx


def render_monthly_executive_snapshot(c: dict) -> str:
    """§一 顶部速览：关键数字表 + P0 醒目框（飞书/高管扫读友好）。"""
    n_missing = len(c.get("missing_core", []))
    n_overlap = c.get("cross_engine_count", "—")
    index_push = min(c.get("index_gap", 0) // 10, 2000)
    uv_c = c.get("uv_c")
    pay_c = c.get("new_pay_c")
    g_cl = c.get("gsc_clicks_curr")
    b_cl = c.get("bing_site_clicks_curr")
    uv_cell = f"{uv_c:,}" if isinstance(uv_c, (int, float)) else "—"
    pay_cell = f"{pay_c:,}" if isinstance(pay_c, (int, float)) else "—"
    g_cell = f"{g_cl:,}" if isinstance(g_cl, (int, float)) else "—"
    b_cell = f"{b_cl:,}" if isinstance(b_cl, (int, float)) else "—"
    return f"""
### 本月 30 秒速览（双引擎）

| 信号 | 报告月 | 环比 | 详情 |
|------|--------|------|------|
| 自然搜索 UV | {uv_cell} | {c.get('uv_chg', '—')} | §三 卡 B |
| **新增付费 UV** | {pay_cell} | {c.get('new_pay_chg', '—')} | §三 卡 B |
| Google 点击（GSC） | {g_cell} | {c.get('gsc_clicks_chg', '—')} | §三 卡 C |
| Bing 站点点击 | {b_cell} | {c.get('bing_site_clicks_chg', '—')} | §三 卡 C-Bing |
| 品牌依赖 | Google **{c.get('b_share', '—')}%** / Bing **{c.get('bing_brand_share', '—')}%** | — | §七 |
| 竞品 Core 覆盖 | Google **{c.get('core_rate', '—')}%** / Bing **{c.get('bing_core_rate', '—')}%** | 缺 **{n_missing}** 词 | §八 |
| 收录率 | **{c.get('index_rate', '—')}%** | 缺口 **{c.get('index_gap', 0):,}** URL | §三 卡 F |

> **🔴 本月 P0（只干这三件）**  
> ① **Google 优先**：§4.7 跌幅词 + 收录推进约 **+{index_push:,}** 有曝光 URL  
> ② **Bing 优先**：§9.5 内页 + §4.16 共用词 landing（**{n_overlap}** 个 GSC∩Bing 高曝光词）  
> ③ **双引擎共用**：补 **{n_missing}** 个 missing core landing + 首页 hub 内链

"""


def render_core_insights(ctx: dict) -> str:
    """§一 核心洞察：飞书友好三段式结论 +（一）（二）展开；OKR 见 §二。"""
    c = ctx
    missing_str = "、".join(c["missing_core"][:5]) if c.get("missing_core") else "—"
    n_missing = len(c.get("missing_core", []))
    region_lines = c.get("region_summary", "见 §11.0 大区总览。")
    inv = c.get("content_inventory") or {}
    n_blog, n_feat, n_tools = inv.get("blog", 0), inv.get("features", 0), inv.get("tools", 0)
    inv_note = (
        f"**{n_blog}** 个 Blog、**{n_feat}** 个 Features、**{n_tools}** 个 Tools"
        if (n_blog or n_feat or n_tools) else "tools/features/blog 内容池"
    )

    if c.get("has_product"):
        uv_pct = c.get("uv_chg", "—").split("/")[-1].strip() if c.get("uv_chg") else "—"
        geo_note = ""
        if c.get("geo_pay_avg"):
            geo_note = (
                f"虽 GEO DAU 仅 **{c['geo_dau_pct']}%**，但 {c.get('geo_pay_platforms', 'GEO 平台')} "
                f"新增注册→付费均值约 **{c['geo_pay_avg']}%**，高于传统 SEO（{c.get('seo_pay_platforms', '—')}，见 **§六**）。"
            )
        else:
            geo_note = f"GEO DAU **{c['geo_dau_pct']}%**，须分开看 SEO/GEO 转化（见 **§六**）。"
        headline = f"""1. **全链路表现**：流量收缩（{uv_pct}），转化走弱（注册 **{c['reg_conv_pp']}**），GEO 值得关注；{geo_note}

2. **关键词层面**：收录数暴增（有曝光 URL **{c.get('pwt_prev', 0):,}→{c['pages_with_traffic']:,}**，收录率 **{c.get('index_rate_prev', '—')}%→{c['index_rate']}%**），但点击仍依赖品牌词（**{c['b_share']}%**{'（'+c['b_share_chg']+'）' if c.get('b_share_chg') else ''}）；增长突破口在非品牌曝光 **{c['nb_impr_chg']}**，以及 **{n_missing}** 个竞品核心非品牌词（{missing_str}…）与内容池 {inv_note}。详见 **§四 / §七 / §八 / §九**。

3. **执行层面**：**建 landing**（非品牌词页）｜**首页导流**（首页改造）｜**优化目录**（Footer）｜**扩收录**（404 页面）｜**保付费**（SEO+GEO 高付费意向词）｜**提注册**（Tools 页面改造）｜**补流量**（新增 Tools 页）；双引擎分工见 **§4.16 / §9.5 / §11.10**。
"""
        block1 = f"""### （一）自然搜索整体表现

1. **规模全面收缩** —— 访问/新增注册/新增付费三项齐跌，增长引擎降速；访问 UV {c['uv_chg']}、新增付费 {c['new_pay_chg']}（详见 **§三 卡 B**、**§二 OKR**）。
2. **转化效率走弱** —— 注册转化与付费率双降，漏斗在漏水；注册转化率 {c['reg_conv_prev']}%→{c['reg_conv_curr']}%（{c['reg_conv_pp']}）、新增注册→付费 {c['reg_to_pay_str'].split('（')[0]}。
3. **渠道结构** —— SEO 是绝对主力（**Google、Microsoft、百度** 为 SEO 前三入口）；**Google 与 Microsoft** 同时承载搜索与部分 AI 发现流量，**GEO**（豆包/ChatGPT 等）DAU 虽小但付费转化更高。SEO 占 DAU **{c['seo_dau_pct']}%**、GEO **{c['geo_dau_pct']}%**（**§三 卡 A**）；入口对照 Google 点击 {c['gsc_clicks_chg']}、Bing 站点 {c.get('bing_site_clicks_chg', '—')}（**§三 C/C-Bing**）。
"""
        block2 = f"""### （二）收录、关键词排名与页面表现

1. **收录绝对值和收录率都大幅提升** —— **{c['index_rate']}%** 有曝光（{c.get('index_rate_pp', '—')}）、缺口 **{c['index_gap']:,}** URL；不扩收录则长尾/非品牌词无从放量（**§三 卡 F**）。
2. **点击高度依赖头部品牌词** —— 集中度 **{c['b_share']}%**（{c.get('b_share_chg', '—')}），抗风险弱；非品牌曝光 **{c['nb_impr_chg']}** 是积极信号。最大缺口 **{n_missing}** 个竞品核心词零排名；解法→修跌幅词（**§4.7**）+ 补非品牌高曝光低 CTR 标题（**§4.5**）+ 双引擎 landing（**§4.16**）。
3. **流量过度集中首页、内页 discovery 弱** —— 首页占 GSC 点击 **{c['home_share']}%**；tools/features/blog 合计 **{c['content_clicks']:,}**（{c['content_clicks_chg']}）。解法→首页 hub 内链 + tools/features 目录 SEO（**§九**）；Bing 首页系 **{c.get('bing_home_share', '—')}%**（**§9.4–9.6**）。

{region_lines}
"""
    else:
        headline = f"""1. **全链路表现**：点击 {c['gsc_clicks_chg']}、收录 **{c['index_rate']}%**（GSC 代理，缺 DataWorks 产品表）。

2. **关键词层面**：品牌依赖 **{c['b_share']}%**；竞品缺口 **{n_missing}** 词。详见 **§四 / §八**。

3. **执行层面**：优先补齐 `From Datawork/{{YYYY-MM}} SEO GEO.xlsx` 后重做转化诊断。
"""
        block1 = f"""### （一）自然搜索整体表现

> ⚠️ 未接入 DataWorks 产品表。请放入 `1-2 Insight/From Datawork/{{YYYY-MM}} SEO GEO.xlsx`。

1. GSC 点击 {c['gsc_clicks_chg']}，曝光 {c['gsc_impr_chg']}，CTR {c['gsc_ctr_chg']}。
2. GA4 Sessions {c['ga4_sess_chg']}，Organic {c['org_share_prev']}%→{c['org_share_curr']}%。

"""
        block2 = f"""### （二）收录、关键词排名与页面表现

1. 收录 **{c['index_rate']}%**（{c['pages_with_traffic']:,}/{c['corpus']:,} URL）。
2. 品牌占比 **{c['b_share']}%**；非品牌曝光 {c['nb_impr_chg']}。
3. 首页占 **{c['home_share']}%**。

"""

    return f"""## 一、核心洞察

> 赶时间：**只读下方 1–3 段结论**；（一）（二）为展开；OKR 与大盘表见 **§二 / §三**。

{headline}

{block1}
{block2}
"""


def section_insight_keywords(g_prev, g_curr, chg_str, bing_curr=None) -> str:
    nb_impr = chg_str(g_prev["tiers"]["非品牌词"]["impr"], g_curr["tiers"]["非品牌词"]["impr"])
    b_note = ""
    if bing_curr and bing_curr.get("kw_count"):
        b_note = f" Bing 品牌占比 {bing_curr['tiers']['品牌词']['share']}%（§4.12–4.15）；跨引擎词见 §4.16。"
    return f"""
> 💡 **关键词** — **问题**：Top10 点击集中度仍高。**根源**：品牌词占主导。**积极信号**：Google 非品牌曝光 {nb_impr}。{b_note}**缓解**：Google §4.4–4.7；Bing §4.12–4.15；共用词 §4.16。
{annual_note_placeholder('keywords')}
"""


def section_insight_ga4(ga4_curr, ga4_prev, chg_str) -> str:
    return f"""
> 💡 **GA4** — **问题**：Sessions {chg_str(ga4_prev['sessions'], ga4_curr['sessions'])} 未达 O1。**积极信号**：{ga4_curr['pages_per_session']} 页/次、{ga4_curr['avg_dur']}s、跳出 {ga4_curr['bounce']}% — 质量优秀。**缓解**：扩非品牌入口而非仅优化落地页体验。
{annual_note_placeholder('ga4_sessions')}
"""


def section_insight_brand(b_prev, b_curr, nb_prev, nb_curr, bing_curr=None) -> str:
    b_extra = ""
    if bing_curr and bing_curr.get("kw_count"):
        b_extra = f" Bing 品牌占比 {bing_curr['tiers']['品牌词']['share']}%（§7B）。"
    return f"""
> 💡 **品牌/非品牌** — Google 品牌点击占比 {b_curr['share']}%。{b_extra}**缓解**：品牌守 SERP；非品牌 tools/features/blog + 双引擎 landing。
{annual_note_placeholder('brand_share')}
"""


def section_insight_comp(comp_curr, bing_curr=None) -> str:
    n = len(comp_curr["missing_core"])
    b_extra = ""
    if bing_curr and bing_curr.get("comp"):
        bc = bing_curr["comp"]
        b_extra = f" Bing Core {bc['core_rate']}%（§8.6–8.11），未覆盖 {len(bc['missing_core'])} 词。"
    return f"""
> 💡 **竞品** — Google {n} 个核心词零排名。{b_extra}**缓解**：missing core 建 landing（双引擎共用）；Full 词做长尾聚合页。
{annual_note_placeholder('comp_core_rate')}
"""


def section_insight_pages(pdirs_curr, total_pc, bing_curr=None) -> str:
    home = pdirs_curr.get("首页", {"clicks": 0})
    hs = round(home["clicks"] / total_pc * 100, 1) if total_pc else 0
    b_extra = ""
    if bing_curr and bing_curr.get("pdirs"):
        fam = sum(v["clicks"] for d, v in bing_curr["pdirs"].items() if d == "首页" or d.startswith("语言首页"))
        tot = sum(v["clicks"] for v in bing_curr["pdirs"].values()) or 1
        b_extra = f" Bing 首页系 {round(fam/tot*100,1)}%（§9.4–9.6）。"
    return f"""
> 💡 **页面目录** — Google 首页占 {hs}%。{b_extra}**缓解**：首页 hub 内链 + tools/features 目录 SEO + 多语言 i18n 内页。
{annual_note_placeholder('homepage_clicks')}
"""


def section_insight_region_summary() -> str:
    return """
> 💡 **地区总览** — 下文 §11.x 为各大区 mini 月报（GSC/品牌非品牌/GA4/Top 页面全维度）。**缓解**：按区 Top15 非品牌词建本地化 landing。
"""


def annual_note_placeholder(metric: str) -> str:
    """占位，generate_report 中 replace 为真实 annual_note。"""
    return f"<!--ANNUAL:{metric}-->"


def render_movers_section(
    g_prev, g_curr, pl, cl, chg_str, n=15,
    sections: tuple = (4.4, 4.5, 4.6, 4.7), label: str = "",
) -> str:
    tag = f"{label} " if label else ""
    up, down, impr_up = keyword_movers(g_prev, g_curr, n)
    s1, s2, s3, s4 = sections
    lines = [f"### {s1} {tag}点击增长 Top {n} movers\n",
             f"| # | 关键词 | {pl} 点击 | {cl} 点击 | 点击变化 | {cl} 曝光 | CTR |",
             "|---|--------|----------|----------|----------|----------|-----|"]
    for i, m in enumerate(up):
        if m["dc"] <= 0:
            break
        lines.append(f"| {i+1} | {m['q'][:35]} | — | {m['clicks']:,} | {m['dc']:+,} | {m['impr']:,} | {m['ctr']}% |")
    lines.append(f"\n### {s2} {tag}曝光增长 Top {n}\n")
    lines.append(f"| # | 关键词 | 曝光变化 | {cl} 曝光 | {cl} 点击 | CTR |")
    lines.append("|---|--------|----------|----------|----------|-----|")
    for i, m in enumerate(impr_up):
        if m["di"] <= 0:
            break
        lines.append(f"| {i+1} | {m['q'][:35]} | {m['di']:+,} | {m['impr']:,} | {m['clicks']:,} | {m['ctr']}% |")
    ctr_movers = sorted(keyword_movers(g_prev, g_curr, 5000)[0], key=lambda x: abs(x["ctr_delta"]), reverse=True)
    ctr_movers = [m for m in ctr_movers if m["impr"] >= 100][:n]
    lines.append(f"\n### {s3} {tag}CTR 变化 Top {n}（曝光≥100）\n")
    lines.append(f"| # | 关键词 | CTR 变化 | {cl} CTR | {cl} 曝光 | {cl} 点击 |")
    lines.append("|---|--------|----------|----------|----------|----------|")
    for i, m in enumerate(ctr_movers):
        lines.append(f"| {i+1} | {m['q'][:35]} | {m['ctr_delta']:+.1f}pp | {m['ctr']}% | {m['impr']:,} | {m['clicks']:,} |")
    lines.append(f"\n### {s4} {tag}点击下滑 Top {n}\n")
    lines.append(f"| # | 关键词 | 点击变化 | {cl} 点击 | {cl} 曝光 |")
    lines.append("|---|--------|----------|----------|----------|")
    for i, m in enumerate(down):
        if m["dc"] >= 0:
            break
        lines.append(f"| {i+1} | {m['q'][:35]} | {m['dc']:+,} | {m['clicks']:,} | {m['impr']:,} |")
    return "\n".join(lines) + "\n"


# ============================================================
# Bing 分渠道（与 GSC 并列）— 月度（周→月聚合，键名同 GSC: q/url/clicks/impr/ctr/pos）
# ============================================================
def _bing_path(url: str) -> str:
    if not url:
        return "/"
    for prefix in (
        "https://www.lovart.ai", "https://lovart.ai",
        "http://www.lovart.ai", "https://insight.lovart.ai",
    ):
        url = url.replace(prefix, "")
    return (url.strip() or "/")[:55]


def _lang_type_rollups(pdirs: dict) -> dict:
    roll = defaultdict(lambda: {"clicks": 0, "impr": 0})
    for d, v in pdirs.items():
        if d == "首页":
            roll["首页"]["clicks"] += v["clicks"]
            roll["首页"]["impr"] += v["impr"]
        elif d.startswith("语言首页-"):
            roll["语言首页合计"]["clicks"] += v["clicks"]
            roll["语言首页合计"]["impr"] += v["impr"]
            roll[d]["clicks"] += v["clicks"]
            roll[d]["impr"] += v["impr"]
        elif d.startswith("i18n内页-"):
            roll["i18n内页合计"]["clicks"] += v["clicks"]
            roll["i18n内页合计"]["impr"] += v["impr"]
    return dict(roll)


def render_cross_engine_keyword_overlap(g_curr, bc, pl, cl) -> str:
    if not bc or not bc.get("keywords"):
        return ""
    gm = {k["q"].lower(): k for k in g_curr["keywords"]}
    bm = {k["q"].lower(): k for k in bc["keywords"]}
    both = set(gm) & set(bm)
    g_only = set(gm) - set(bm)
    b_only = set(bm) - set(gm)

    def top_keys(keys, keymap, n=10):
        return sorted(keys, key=lambda q: keymap[q]["impr"], reverse=True)[:n]

    rows_both = []
    for q in top_keys(both, gm, 10):
        g, b = gm[q], bm[q]
        rows_both.append(
            f"| {g['q'][:28]} | {g['clicks']:,} | {g['impr']:,} | {b['clicks']:,} | {b['impr']:,} |"
        )
    rows_g = [f"| {gm[q]['q'][:32]} | {gm[q]['clicks']:,} | {gm[q]['impr']:,} |" for q in top_keys(g_only, gm, 8)]
    rows_b = [f"| {bm[q]['q'][:32]} | {bm[q]['clicks']:,} | {bm[q]['impr']:,} |" for q in top_keys(b_only, bm, 8)]
    return f"""
#### 4.16 跨引擎词重叠（GSC 5K ∩ Bing 月词 {len(both)} 个）

| 关键词 | Google 点击 | Google 曝光 | Bing 点击 | Bing 曝光 |
|--------|------------|------------|----------|----------|
""" + ("\n".join(rows_both) or "| — | — | — | — | — |") + f"""

#### 仅 Google 有高曝光（Top 8，Bing 周榜未覆盖）

| 关键词 | Google 点击 | Google 曝光 |
|--------|------------|------------|
""" + ("\n".join(rows_g) or "| — | — | — |") + f"""

#### 仅 Bing 有量（Top 8，GSC 5K 未收录）

| 关键词 | Bing 点击 | Bing 曝光 |
|--------|----------|----------|
""" + ("\n".join(rows_b) or "| — | — | — |") + f"""

> 💡 **跨引擎词策略** — 共同词 **{len(both)}** 个优先做双引擎 landing；仅 Google **{len(g_only)}** 个补 Bing 内链/提交；仅 Bing **{len(b_only)}** 个验证是否值得在 Google 侧扩量。
"""


def render_engine_overview(g_prev, g_curr, bp, bc, pl, cl, chg_str) -> str:
    """§四 顶部「整体（Google + Bing）」概览。Google=GSC 关键词合计；Bing=站点级 §13.1。"""
    if not bc:
        return ""
    gpc, gcc = g_prev["total_clicks"], g_curr["total_clicks"]
    gpi, gci = g_prev["total_impr"], g_curr["total_impr"]
    bpc = (bp or {}).get("site_clicks") or 0
    bcc = bc.get("site_clicks") or 0
    bpi = (bp or {}).get("site_impr") or 0
    bci = bc.get("site_impr") or 0
    tpc, tcc = gpc + bpc, gcc + bcc
    tpi, tci = gpi + bpi, gci + bci

    def ctr(c, i):
        return f"{round(c / i * 100, 1)}%" if i else "—"
    return f"""> **整体搜索（Google + Bing）** — 口径不同分行列示：Google 为 GSC 关键词合计（月度），Bing 为站点级流量（§13.1，月度）；关键词/页面**明细**层因覆盖词数不同不做混合合计，见下方各引擎分块。

| 引擎 | {pl} 点击 | {cl} 点击 | 点击环比 | {cl} 曝光 | {cl} CTR |
|------|----------|----------|----------|----------|---------|
| Google（GSC 关键词合计） | {gpc:,} | {gcc:,} | {chg_str(gpc, gcc)} | {gci:,} | {ctr(gcc, gci)} |
| Bing（站点级 §13.1） | {bpc:,} | {bcc:,} | {chg_str(bpc, bcc)} | {bci:,} | {ctr(bcc, bci)} |
| **合计** | {tpc:,} | {tcc:,} | {chg_str(tpc, tcc)} | {tci:,} | {ctr(tcc, tci)} |

#### Multi SEO 渠道全貌（收口监测）

> 口径：Google/GSC 与 Bing/Bing Webmaster 为 `official` 数据；DuckDuckGo、Yahoo Japan 等没有独立站长数据，按 Bing + IndexNow 的发现路径覆盖；Brave、国内搜索、Yandex 等仅保留历史可达性结论，不进入月度执行 KPI。详见 `1-1 Harness/Skills/multi-seo-closeout-2026-06-07.md`。

| 渠道/生态 | 当前接入状态 | 月报使用方式 | 后续动作 |
|-----------|--------------|--------------|----------|
| Google | GSC 已接入 | 主搜索引擎官方表现 | 按 GSC 关键词、页面、地区继续分析 |
| Bing / Microsoft | Bing Webmaster API 已接入 | 第二官方搜索引擎；同时服务部分 Bing 生态发现 | 每月拉取关键词、页面、流量、crawl 数据 |
| IndexNow 支持的网站 | Sanity -> `/api/indexnow` 已验证 `200 ok` | 作为 URL 主动通知覆盖层，不单独混算流量 | 发布后抽查 `IndexNow Notify` delivery |
| DuckDuckGo / Yahoo Japan | 无独立站长平台；主要依赖 Bing/IndexNow/自然抓取 | 作为生态覆盖说明，不做官方曝光 KPI | 必要时低频 SERP spot check |
| Naver | 暂不单独接入 Search Advisor | 仅保留韩国市场观察项 | 若韩国市场优先级提升再单开验证 |
| 百度 | 仅保留人工/资源平台可能性 | 不进入脚本化月报 KPI | 需要账号和人工验证时再开任务 |
| 360 / 神马 / 头条等国内搜索 | 不再推进 | 不纳入 Lovart 当前 Multi SEO 任务 | 无 |
| Brave / Yandex | Brave 无订阅且 429；Yandex 验证码阻塞 | 不进入近期执行范围 | 有 API/账号条件后再重启 |

"""


def render_bing_keyword_block(bp, bc, pl, cl, chg_str, chg_f) -> str:
    if not bc or bc.get("kw_count", 0) == 0:
        return "\n### 4.8 Bing 关键词（月度）\n\n> ⚠️ 本月无 Bing 关键词数据（检查 `bing-full.json` 的 `keywords_monthly`）。\n"
    out = ["### 4.8 Bing 关键词分层（月度 · 词位=曝光加权 AvgImpressionPosition）\n",
           f"> Bing 来自 Webmaster API 每周 top~100 词聚合为月度；当月 **{bc['kw_count']} 词**、关键词点击合计 **{bc['total_clicks']:,}**（口径与 GSC 5K 词不同，不可直接比绝对值；站点级点击见 §13.1）。\n",
           f"| 分层 | {pl} 词数 | {pl} 点击 | {pl} 曝光 | {pl} 占比 | {pl} CTR | → | {cl} 词数 | {cl} 点击 | {cl} 曝光 | {cl} 占比 | {cl} CTR | 点击环比 | 曝光环比 | CTR环比 |",
           "|------|----------|----------|----------|----------|---------|---|----------|----------|----------|----------|---------|----------|----------|---------|",
           tiers_table_full(bp["tiers"], bc["tiers"], [3, 5, 10, 30, 50, 100], pl, cl, chg_str, chg_f)]

    a_br = sorted((bp or {}).get("brand_kw", []), key=lambda x: x["clicks"], reverse=True)
    m_br = sorted(bc["brand_kw"], key=lambda x: x["clicks"], reverse=True)
    out.append(f"\n#### 4.9 Bing 品牌词 Top 10（双月）\n")
    out.append(f"| # | {pl} | {pl} 点击 | → | {cl} | {cl} 点击 | 环比变化 |")
    out.append("|---|-----|----------|---|-----|----------|----------|")
    for i in range(10):
        ak = a_br[i] if i < len(a_br) else {"q": "", "clicks": 0}
        mk = m_br[i] if i < len(m_br) else {"q": "", "clicks": 0}
        out.append(f"| {i+1} | {ak['q'][:22]} | {ak['clicks']:,} | → | {mk['q'][:22]} | {mk['clicks']:,} | {chg_str(ak['clicks'], mk['clicks'])} |")
    a_nb = sorted((bp or {}).get("nonbrand_kw", []), key=lambda x: x["clicks"], reverse=True)
    m_nb = sorted(bc["nonbrand_kw"], key=lambda x: x["clicks"], reverse=True)
    out.append(f"\n#### 4.10 Bing 非品牌词 Top 10（双月）\n")
    out.append(f"| # | {pl} | {pl} 点击 | → | {cl} | {cl} 点击 | 环比变化 |")
    out.append("|---|-----|----------|---|-----|----------|----------|")
    for i in range(10):
        ak = a_nb[i] if i < len(a_nb) else {"q": "", "clicks": 0}
        mk = m_nb[i] if i < len(m_nb) else {"q": "", "clicks": 0}
        out.append(f"| {i+1} | {ak['q'][:22]} | {ak['clicks']:,} | → | {mk['q'][:22]} | {mk['clicks']:,} | {chg_str(ak['clicks'], mk['clicks'])} |")
    if bp:
        out.append(render_movers_section(bp, bc, pl, cl, chg_str, 15, (4.12, 4.13, 4.14, 4.15), "Bing"))
    return "\n".join(out) + "\n"


def render_engine_compare_kw(g_curr, b_g_curr, bc) -> str:
    """§四 末：Google × Bing 关键词结构差异 💡。"""
    if not bc or bc.get("kw_count", 0) == 0:
        return ""
    g_top3 = g_curr["tiers"]["Top3"]["share"]
    g_brand = b_g_curr["share"]
    g_ctr = round(g_curr["total_clicks"] / g_curr["total_impr"] * 100, 1) if g_curr["total_impr"] else 0
    b_top3 = bc["tiers"]["Top3"]["share"]
    b_brand = bc["tiers"]["品牌词"]["share"]
    b_ctr = round(bc["total_clicks"] / bc["total_impr"] * 100, 1) if bc["total_impr"] else 0
    g_top = sorted(g_curr["keywords"], key=lambda x: x["clicks"], reverse=True)[0]["q"] if g_curr["keywords"] else "—"
    b_top = bc["keywords"][0]["q"] if bc["keywords"] else "—"
    verdict = "Bing 更依赖品牌词/首页，非品牌拓展空间更大" if b_brand >= g_brand else "Bing 非品牌结构相对更分散"
    return f"""
> 💡 **引擎差异（关键词）** — 头部集中度 Top3：Bing **{b_top3}%** vs Google **{g_top3}%**；品牌词点击占比：Bing **{b_brand}%** vs Google **{g_brand}%**；平均 CTR：Bing **{b_ctr}%** vs Google **{g_ctr}%**（Bing 通常更高，与品牌词占比/SERP 形态有关）；头部词 Bing「{b_top[:20]}」/ Google「{g_top[:20]}」。**结论**：{verdict}；非品牌放量优先复用两引擎共同高曝光词。
"""


def render_bing_brand_block(bp, bc, b_g_curr, nb_g_curr, pl, cl, chg_str, chg_f) -> str:
    """§七：Bing 品牌 vs 非品牌（与 §7A 同构）+ 引擎差异。"""
    if not bc or bc.get("kw_count", 0) == 0:
        return ""
    bcur = bc["tiers"]["品牌词"]
    ncur = bc["tiers"]["非品牌词"]
    bpre = bp["tiers"]["品牌词"] if bp else {"count": 0, "clicks": 0, "impr": 0, "share": 0, "ctr": 0}
    npre = bp["tiers"]["非品牌词"] if bp else {"count": 0, "clicks": 0, "impr": 0, "share": 0, "ctr": 0}
    g_brand = b_g_curr["share"]
    diff = round(bcur["share"] - g_brand, 1)
    return f"""
### 7B Bing 品牌词 vs 非品牌词（月度）

| 维度 | {pl} | {cl} | 环比变化 |
|------|-----|-----|----------|
| 品牌词数量 | {bpre['count']} | {bcur['count']} | {chg_str(bpre['count'], bcur['count'])} |
| 品牌词点击 | {bpre['clicks']:,} | {bcur['clicks']:,} | {chg_str(bpre['clicks'], bcur['clicks'])} |
| 品牌词曝光 | {bpre['impr']:,} | {bcur['impr']:,} | {chg_str(bpre['impr'], bcur['impr'])} |
| 非品牌词数量 | {npre['count']} | {ncur['count']} | {chg_str(npre['count'], ncur['count'])} |
| 非品牌词点击 | {npre['clicks']:,} | {ncur['clicks']:,} | {chg_str(npre['clicks'], ncur['clicks'])} |
| 非品牌词曝光 | {npre['impr']:,} | {ncur['impr']:,} | {chg_str(npre['impr'], ncur['impr'])} |
| 品牌词点击占比 | {bpre['share']}% | {bcur['share']}% | {bcur['share']-bpre['share']:+.1f}% |
| 非品牌词点击占比 | {npre['share']}% | {ncur['share']}% | {ncur['share']-npre['share']:+.1f}% |

> 💡 **引擎差异（品牌依赖）** — Bing 品牌词点击占比 **{bcur['share']}%**，Google **{g_brand}%**（差 {diff:+.1f}pp）。{'Bing 品牌依赖更重 → 非品牌内容在 Bing 的增量空间更大' if bcur['share'] >= g_brand else 'Bing 非品牌占比更高 → 已有一定非品牌承接'}。
"""


def render_bing_competitor_detail(bp, bc, pl, cl, chg_str) -> str:
    """§八：Bing 竞品明细 8.7–8.11（镜像 Google §8.1–8.5）。"""
    if not bc or not bc.get("comp"):
        return ""
    cp = (bp or {}).get("comp") or {}
    c = bc["comp"]
    out = f"""
### 8.7 Bing 竞品总览（{pl} vs {cl}）

| 指标 | {pl} | {cl} | 变化 |
|------|-----|-----|------|
| Full 匹配关键词 | {cp.get('full_match', 0)} | {c['full_match']} | {chg_str(cp.get('full_match', 0), c['full_match'])} |
| Full 唯一竞品词 | {cp.get('unique_full', 0)} | {c['unique_full']} | {chg_str(cp.get('unique_full', 0), c['unique_full'])} |
| Full 覆盖率 | {cp.get('full_rate', 0)}% | {c['full_rate']}% | {c['full_rate']-cp.get('full_rate', 0):+.1f}% |
| Core 匹配关键词 | {cp.get('core_match', 0)} | {c['core_match']} | {chg_str(cp.get('core_match', 0), c['core_match'])} |
| Core 唯一竞品词 | {cp.get('unique_core', 0)} | {c['unique_core']} | {chg_str(cp.get('unique_core', 0), c['unique_core'])} |
| Core 覆盖率 | {cp.get('core_rate', 0)}% | {c['core_rate']}% | {c['core_rate']-cp.get('core_rate', 0):+.1f}% |
| 竞品词点击占非品牌比 | {cp.get('click_share', 0)}% | {c['click_share']}% | {c['click_share']-cp.get('click_share', 0):+.1f}% |

### 8.8 Bing 分层表现 ({cl})

| 分层 | Full 命中词数 | Full Clicks | Core 命中词数 | Core Clicks | 竞品词去重数 |
|------|:-----------:|------------:|:-----------:|------------:|:----------:|
| Top 10 | {c['tier_full']['top10']['count']} | {c['tier_full']['top10']['clicks']:,} | {c['tier_core']['top10']['count']} | {c['tier_core']['top10']['clicks']:,} | {c['tier_full']['top10']['comps']} |
| Top 50 | {c['tier_full']['top50']['count']} | {c['tier_full']['top50']['clicks']:,} | {c['tier_core']['top50']['count']} | {c['tier_core']['top50']['clicks']:,} | {c['tier_full']['top50']['comps']} |
| Top 100 | {c['tier_full']['top100']['count']} | {c['tier_full']['top100']['clicks']:,} | {c['tier_core']['top100']['count']} | {c['tier_core']['top100']['clicks']:,} | {c['tier_full']['top100']['comps']} |

### 8.9 Bing 命中的核心竞品词明细 (Top 20)

| # | 竞品词 | 匹配的 Bing 关键词 | 点击 | 曝光 | CTR |
|---|--------|-----------------|------|------|-----|
"""
    core_seen = {}
    for m in c["matched_core_detail"]:
        for cc in m["comps"]:
            if cc not in core_seen or m["clicks"] > core_seen[cc]["clicks"]:
                core_seen[cc] = {"q": m["q"], "clicks": m["clicks"], "impr": m["impr"], "ctr": m["ctr"]}
    for i, (comp, d) in enumerate(sorted(core_seen.items(), key=lambda x: x[1]["clicks"], reverse=True)[:20]):
        out += f"| {i+1} | {comp} | {d['q'][:35]} | {d['clicks']:,} | {d['impr']:,} | {d['ctr']}% |\n"
    out += f"""
### 8.10 Bing Full 匹配 Top 20

| # | Bing 关键词 | 命中竞品词 | 点击 | 曝光 | CTR | 词位 |
|---|-----------|-----------|------|------|-----|------|
"""
    for i, m in enumerate(c["matched_full_detail"][:20]):
        cs = ", ".join(m["comps"][:4])
        out += f"| {i+1} | {m['q'][:30]} | {cs[:40]} | {m['clicks']:,} | {m['impr']:,} | {m['ctr']}% | {m['pos']} |\n"
    out += f"""
### 8.11 Bing 未覆盖的核心竞品词 ({len(c['missing_core'])} 个)

以下高优先级词在 Bing 月词中完全无排名:
"""
    for kw in c["missing_core"][:20]:
        out += f"- {kw}\n"
    return out


def render_bing_competitor_block(bc, comp_g_curr, chg_str) -> str:
    """§八：Bing 竞品覆盖 + 引擎差异。"""
    if not bc or not bc.get("comp"):
        return ""
    c = bc["comp"]
    g = comp_g_curr
    return f"""
### 8.6 Bing 竞品非品牌词覆盖（月度）

| 指标 | Bing 当月 | Google 当月 | 引擎差 |
|------|----------|------------|--------|
| Full 匹配关键词 | {c['full_match']} | {g['full_match']} | {c['full_match']-g['full_match']:+} |
| Full 覆盖率 | {c['full_rate']}% | {g['full_rate']}% | {c['full_rate']-g['full_rate']:+.1f}pp |
| Core 覆盖率 | {c['core_rate']}% | {g['core_rate']}% | {c['core_rate']-g['core_rate']:+.1f}pp |
| 竞品词点击占非品牌比 | {c['click_share']}% | {g['click_share']}% | {c['click_share']-g['click_share']:+.1f}pp |
| 未覆盖核心竞品词 | {len(c['missing_core'])} | {len(g['missing_core'])} | {len(c['missing_core'])-len(g['missing_core']):+} |

> 💡 **引擎差异（竞品）** — Bing Core 覆盖 **{c['core_rate']}%** vs Google **{g['core_rate']}%**。{'两引擎竞品缺口一致 → 内容结构性问题，建 landing 可同时补两端' if abs(c['core_rate']-g['core_rate']) < 15 else '两引擎竞品格局差异显著，需分别排查'}。Bing 当月命中竞品词 Top：{('、'.join(sorted({cc for m in c['matched_core_detail'][:6] for cc in m['comps']})[:5]) or '—')}。
"""


def render_bing_pages_block(bp, bc, pl, cl, chg_str) -> str:
    """§九：Bing 页面目录 9.4–9.6（镜像 §9.1–9.3）+ 引擎差异。"""
    if not bc or not bc.get("pdirs"):
        return ""
    pd_c = bc["pdirs"]
    pd_p = (bp or {}).get("pdirs", {})
    tot_c = sum(v["clicks"] for v in pd_c.values()) or 1
    tot_pi_c = sum(v["impr"] for v in pd_c.values()) or 1
    tot_p = sum(v["clicks"] for v in pd_p.values()) or 1
    tot_pi_p = sum(v["impr"] for v in pd_p.values()) or 1
    all_d = sorted(set(pd_c) | set(pd_p), key=lambda d: pd_c.get(d, {"clicks": 0})["clicks"], reverse=True)
    rows = []
    for d in all_d[:20]:
        pv = pd_p.get(d, {"clicks": 0, "impr": 0})
        cv = pd_c.get(d, {"clicks": 0, "impr": 0})
        rows.append(
            f"| {d} | {pv['clicks']:,} | {pv['impr']:,} | "
            f"{round(pv['clicks']/tot_p*100,1)}% | {round(pv['impr']/tot_pi_p*100,1)}% | → | "
            f"{cv['clicks']:,} | {cv['impr']:,} | "
            f"{round(cv['clicks']/tot_c*100,1)}% | {round(cv['impr']/tot_pi_c*100,1)}% | "
            f"{chg_str(pv['clicks'], cv['clicks'])} | {chg_str(pv['impr'], cv['impr'])} |"
        )
    target = ['features', 'tools', 'blog', 'news', 'docs', 'r', 'profile']
    core_rows = []
    for d in target:
        pv = pd_p.get(d, {"clicks": 0, "impr": 0})
        cv = pd_c.get(d, {"clicks": 0, "impr": 0})
        core_rows.append(
            f"| {d} | {pv['clicks']:,} | {pv['impr']:,} | {cv['clicks']:,} | {cv['impr']:,} | "
            f"{chg_str(pv['clicks'], cv['clicks'])} | {round(cv['impr']/tot_pi_c*100,1)}% |"
        )
    lang_prev = _lang_type_rollups(pd_p)
    lang_curr = _lang_type_rollups(pd_c)
    lang_types = ["首页", "语言首页合计", "i18n内页合计"]
    lang_types += sorted(k for k in lang_curr if k.startswith("语言首页-"))
    lang_rows = []
    seen = set()
    for t in lang_types:
        if t in seen:
            continue
        seen.add(t)
        pv = lang_prev.get(t, {"clicks": 0, "impr": 0})
        cv = lang_curr.get(t, {"clicks": 0, "impr": 0})
        lang_rows.append(
            f"| {t} | {pv['clicks']:,} | {pv['impr']:,} | {round(pv['clicks']/tot_p*100,1)}% | → | "
            f"{cv['clicks']:,} | {cv['impr']:,} | {round(cv['clicks']/tot_c*100,1)}% | "
            f"{chg_str(pv['clicks'], cv['clicks'])} |"
        )
    home_fam = sum(v["clicks"] for d, v in pd_c.items() if d == "首页" or d.startswith("语言首页"))
    home_share = round(home_fam / tot_c * 100, 1)
    inner_share = round(100 - home_share, 1)
    return f"""
### 9.4 Bing 页面目录流量（{pl} vs {cl}）

| 目录 | {pl} 点击 | {pl} 曝光 | {pl} 点击占比 | {pl} 曝光占比 | → | {cl} 点击 | {cl} 曝光 | {cl} 点击占比 | {cl} 曝光占比 | 点击环比 | 曝光环比 |
|------|----------|----------|--------------|--------------|---|----------|----------|--------------|--------------|----------|----------|
""" + "\n".join(rows) + f"""

### 9.5 Bing 核心内容目录

| 目录 | {pl} 点击 | {pl} 曝光 | {cl} 点击 | {cl} 曝光 | 点击环比 | 曝光占比({cl}) |
|------|----------|----------|----------|----------|----------|----------------|
""" + "\n".join(core_rows) + f"""

### 9.6 Bing 多语言页面类型占比

| 类型 | {pl} 点击 | {pl} 曝光 | {pl} 点击占比 | → | {cl} 点击 | {cl} 曝光 | {cl} 点击占比 | 点击环比 |
|------|----------|----------|--------------|---|----------|----------|--------------|----------|
""" + "\n".join(lang_rows) + f"""

> 💡 **引擎差异（页面）** — Bing 首页系（首页+各语言首页）点击占比高达 **{home_share}%**，内页仅 **{inner_share}%**（高度集中 `/zh` 与 `/`）。对比 §9.1 Google 目录分布，{'Bing 内页 discovery 明显更弱 → 工具/博客等内页在 Bing 几乎无承接，是结构性机会' if home_share >= 70 else 'Bing 已有一定内页承接'}。
"""


def render_ga4_engine_split(ga4_prev, ga4_curr, pl, cl, chg_str) -> str:
    """§5.4 Organic Search 按来源引擎拆分（GA4 sessionSource）。老快照无该字段时返回提示。"""
    cur = (ga4_curr or {}).get("organic_sources")
    if not cur:
        return "\n### 5.4 自然搜索引擎拆分（GA4 sessionSource）\n\n> ⚠️ 当前 GA4 快照未含 `sessionSource` 拆分，请重跑完整月报（非 --render-only）以补全 Google/Bing 引擎拆分。\n"
    prev = (ga4_prev or {}).get("organic_sources", {})
    order = ["google", "bing", "yahoo", "duckduckgo", "其他"]
    order = [e for e in order if e in cur] + [e for e in cur if e not in order]
    rows = []
    for e in order:
        c = cur[e]
        p = prev.get(e, {})
        rows.append(
            f"| {e} | {c['sessions']:,} | {c.get('share',0)}% | {c.get('new_users',0):,} | "
            f"{c.get('dur',0)}s | {c.get('bounce',0)}% | {chg_str(p.get('sessions',0), c['sessions'])} |"
        )
    g = cur.get("google", {}).get("sessions", 0)
    b = cur.get("bing", {}).get("sessions", 0)
    g_share = round(g / (g + b) * 100, 1) if (g + b) else 0
    return f"""
### 5.4 自然搜索引擎拆分（GA4 · Organic Search by sessionSource）

| 来源引擎 | {cl} Sessions | 占自然搜索 | 新用户 | 时长 | 跳出 | Sessions 环比 |
|----------|-------------:|----------:|------:|-----:|-----:|--------------|
""" + "\n".join(rows) + f"""

> 💡 **引擎差异（自然访问行为）** — 自然搜索 Sessions 中 Google 约 **{g_share}%**、Bing 约 **{round(100-g_share,1)}%**；行为指标见上表（Bing 与 Google 的停留/跳出差异反映流量质量）。该口径与 GSC 点击、DataWorks UV 各自独立，不可直接相加。
"""


def render_bing_top_pages(bp, bc, pl, cl, chg_str, n: int = 20) -> str:
    """§十：Bing 页面 Top N（双月）。"""
    if not bc or not bc.get("pages"):
        return ""
    pp = {_bing_path(p["url"]): p for p in (bp or {}).get("pages", [])}
    rows = []
    for i, p in enumerate(bc["pages"][:n]):
        u = _bing_path(p["url"])
        prev_p = pp.get(u, {"clicks": 0, "impr": 0})
        rows.append(
            f"| {i+1} | {u} | {prev_p['clicks']:,} | {p['clicks']:,} | {chg_str(prev_p['clicks'], p['clicks'])} | "
            f"{p['impr']:,} | {p['ctr']}% | {p['pos']} |"
        )
    return f"""
### 10B Bing 页面查询明细 (Top {n}，双月)

| # | URL | {pl} 点击 | {cl} 点击 | 点击环比 | {cl} 曝光 | CTR | 词位 |
|---|-----|----------|----------|----------|----------|-----|------|
""" + "\n".join(rows) + "\n"


def render_bing_dashboard_cards(bp, bc, pl, cl, chg_str, chg_f, bing_in_index: int | None = None) -> str:
    """§三 Dashboard：C-Bing / D-Bing / E-Bing 卡。"""
    if not bc or not bc.get("kw_count"):
        return ""
    bpre = bp or {}
    b_br = bpre.get("tiers", {}).get("品牌词", {"count": 0, "clicks": 0, "impr": 0, "share": 0, "ctr": 0})
    b_nb = bpre.get("tiers", {}).get("非品牌词", {"count": 0, "clicks": 0, "impr": 0, "share": 0, "ctr": 0})
    b_br_c = bc["tiers"]["品牌词"]
    b_nb_c = bc["tiers"]["非品牌词"]
    sc_p = bpre.get("site_clicks") or 0
    sc_c = bc.get("site_clicks") or 0
    si_p = bpre.get("site_impr") or 0
    si_c = bc.get("site_impr") or 0
    ctr_p = round(sc_p / si_p * 100, 1) if si_p else 0
    ctr_c = round(sc_c / si_c * 100, 1) if si_c else 0
    ix_line = f"\n| Bing 索引页数（参考） | — | {bing_in_index:,} | — |" if bing_in_index else ""
    return f"""
#### C-Bing. Bing 站点流量（§13.1 口径）

| 指标 | {pl} | {cl} | 环比 |
|------|-----|-----|------|
| 站点点击 | {sc_p:,} | {sc_c:,} | {chg_str(sc_p, sc_c)} |
| 站点曝光 | {si_p:,} | {si_c:,} | {chg_str(si_p, si_c)} |
| 站点 CTR | {ctr_p}% | {ctr_c}% | {chg_f(ctr_p, ctr_c)} |
| 月词数（周榜聚合） | {bpre.get('kw_count', 0):,} | {bc['kw_count']:,} | {chg_str(bpre.get('kw_count', 0), bc['kw_count'])} |{ix_line}

#### D-Bing. Top 分层（Bing 关键词）

| 分层 | {pl} 点击 | {pl} 曝光 | {pl} CTR | {pl} 占比 | → | {cl} 点击 | {cl} 曝光 | {cl} CTR | {cl} 占比 | 点击环比 | 曝光环比 |
|------|----------|----------|---------|---------|---|----------|----------|---------|---------|----------|----------|
{tiers_table_full(bpre.get('tiers', {}), bc['tiers'], [3, 10, 50], pl, cl, chg_str, chg_f)}

#### E-Bing. 品牌 vs 非品牌（Bing）

| 指标 | {pl} | {cl} | 环比 |
|------|-----|-----|------|
| 品牌词数 | {b_br['count']} | {b_br_c['count']} | {chg_str(b_br['count'], b_br_c['count'])} |
| 品牌曝光 | {b_br['impr']:,} | {b_br_c['impr']:,} | {chg_str(b_br['impr'], b_br_c['impr'])} |
| 品牌点击 | {b_br['clicks']:,} | {b_br_c['clicks']:,} | {chg_str(b_br['clicks'], b_br_c['clicks'])} |
| 品牌 CTR | {b_br['ctr']}% | {b_br_c['ctr']}% | {chg_f(b_br['ctr'], b_br_c['ctr'])} |
| 品牌点击占比 | {b_br['share']}% | {b_br_c['share']}% | {share_pp_chg(b_br['share'], b_br_c['share'])} |
| 非品牌词数 | {b_nb['count']} | {b_nb_c['count']} | {chg_str(b_nb['count'], b_nb_c['count'])} |
| 非品牌曝光 | {b_nb['impr']:,} | {b_nb_c['impr']:,} | {chg_str(b_nb['impr'], b_nb_c['impr'])} |
| 非品牌点击 | {b_nb['clicks']:,} | {b_nb_c['clicks']:,} | {chg_str(b_nb['clicks'], b_nb_c['clicks'])} |
| 非品牌 CTR | {b_nb['ctr']}% | {b_nb_c['ctr']}% | {chg_f(b_nb['ctr'], b_nb_c['ctr'])} |
| 非品牌点击占比 | {b_nb['share']}% | {b_nb_c['share']}% | {share_pp_chg(b_nb['share'], b_nb_c['share'])} |

"""


def enrich_core_ctx_with_bing(ctx: dict, bing_prev, bing_curr, ga4_curr, chg_str) -> dict:
    """注入 Bing 引擎字段供 §一 核心洞察双引擎叙事。"""
    if not bing_curr or not bing_curr.get("kw_count"):
        return ctx
    b_brand = bing_curr["tiers"]["品牌词"]["share"]
    home_fam = sum(
        v["clicks"] for d, v in bing_curr.get("pdirs", {}).items()
        if d == "首页" or d.startswith("语言首页")
    )
    tot_pc = sum(v["clicks"] for v in bing_curr.get("pdirs", {}).values()) or 1
    osrc = (ga4_curr or {}).get("organic_sources", {})
    g_sess = osrc.get("google", {}).get("sessions", 0)
    b_sess = osrc.get("bing", {}).get("sessions", 0)
    comp = bing_curr.get("comp") or {}
    ctx.update({
        "bing_site_clicks_chg": chg_str(bing_prev.get("site_clicks") or 0, bing_curr.get("site_clicks") or 0),
        "bing_site_clicks_curr": bing_curr.get("site_clicks") or 0,
        "bing_brand_share": b_brand,
        "bing_core_rate": comp.get("core_rate", 0),
        "bing_home_share": round(home_fam / tot_pc * 100, 1),
        "google_bing_session_ratio": round(g_sess / b_sess, 1) if b_sess else 0,
        "bing_kw_count": bing_curr["kw_count"],
        "bing_top3_share": bing_curr["tiers"]["Top3"]["share"],
    })
    return ctx


def render_bing_region_section(
    region_order: list,
    reg_bing_prev: dict,
    reg_bing_curr: dict,
    pl: str,
    cl: str,
    chg_str,
) -> str:
    """§11.10 Bing 分地区（GA4 country×sessionSource=bing 近似）。"""
    if not reg_bing_curr:
        return ""
    total_c = sum(v.get("sessions", 0) for v in reg_bing_curr.values()) or 1
    rows = []
    for grp in region_order:
        a = reg_bing_prev.get(grp, {"sessions": 0, "users": 0, "new_users": 0, "dur": 0, "bounce": 0})
        b = reg_bing_curr.get(grp, {"sessions": 0, "users": 0, "new_users": 0, "dur": 0, "bounce": 0})
        if b["sessions"] + a["sessions"] == 0:
            continue
        rows.append(
            f"| {grp} | {a['sessions']:,} | {b['sessions']:,} | {chg_str(a['sessions'], b['sessions'])} | "
            f"{round(b['sessions']/total_c*100,1)}% | {b.get('new_users',0):,} | {b.get('dur',0)}s | {b.get('bounce',0)}% |"
        )
    if not rows:
        return "\n> ⚠️ §11.10 无 Bing GA4 分地区数据（请重跑 GA4 拉取 `country×sessionSource`）。\n"
    return f"""
### 11.10 Bing 分地区（GA4 近似 · Organic Search × sessionSource=bing）

> ⚠️ **口径**：Bing Webmaster 无 country 维度；本节为 GA4 `country × sessionSource(bing)` 的 **Sessions 行为近似**，不代表 Bing 搜索词地区分布。与 §11.1–11.9 的 GSC 搜索词地区**不可直接对比**。

| 地区 | {pl} Sessions | {cl} Sessions | 环比 | {cl} 占比 | 新用户 | 时长 | 跳出 |
|------|-------------:|-------------:|------|--------:|------:|-----:|-----:|
""" + "\n".join(rows) + "\n"

