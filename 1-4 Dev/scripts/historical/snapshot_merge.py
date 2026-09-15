#!/usr/bin/env python3
"""合并多月 GSC/GA4/Bing 快照为双月窗 bundle（供 generate_report 使用）。"""
from __future__ import annotations

import json
from collections import defaultdict
from copy import deepcopy


def _merge_kw_rows(*row_groups: list[dict]) -> list[dict]:
    by_q: dict[str, dict] = {}
    for rows in row_groups:
        for k in rows or []:
            q = k["q"]
            if q not in by_q:
                by_q[q] = {"q": q, "clicks": 0, "impr": 0, "_pos_w": 0.0}
            by_q[q]["clicks"] += int(k.get("clicks") or 0)
            by_q[q]["impr"] += int(k.get("impr") or 0)
            by_q[q]["_pos_w"] += float(k.get("pos") or 0) * int(k.get("impr") or 0)
    out: list[dict] = []
    for v in by_q.values():
        impr = v["impr"]
        clicks = v["clicks"]
        ctr = round(clicks / impr * 100, 1) if impr else 0
        pos = round(v["_pos_w"] / impr, 1) if impr else 0
        out.append({"q": v["q"], "clicks": clicks, "impr": impr, "ctr": ctr, "pos": pos})
    return sorted(out, key=lambda x: x["clicks"], reverse=True)


def _merge_countries(*country_groups: list[dict]) -> list[dict]:
    by_c: dict[str, dict] = {}
    for rows in country_groups:
        for c in rows or []:
            code = c.get("country") or c.get("q") or ""
            if code not in by_c:
                by_c[code] = {"country": code, "clicks": 0, "impr": 0, "_pos_w": 0.0}
            by_c[code]["clicks"] += int(c.get("clicks") or 0)
            by_c[code]["impr"] += int(c.get("impr") or 0)
            by_c[code]["_pos_w"] += float(c.get("pos") or 0) * int(c.get("impr") or 0)
    out: list[dict] = []
    for v in by_c.values():
        impr = v["impr"]
        clicks = v["clicks"]
        out.append(
            {
                "country": v["country"],
                "clicks": clicks,
                "impr": impr,
                "ctr": round(clicks / impr * 100, 1) if impr else 0,
                "pos": round(v["_pos_w"] / impr, 1) if impr else 0,
            }
        )
    return sorted(out, key=lambda x: x["clicks"], reverse=True)


def _merge_pages(*page_groups: list[dict]) -> list[dict]:
    by_u: dict[str, dict] = {}
    for pages in page_groups:
        for p in pages or []:
            u = p.get("url") or p.get("page") or ""
            if not u:
                continue
            if u not in by_u:
                by_u[u] = {"url": u, "clicks": 0, "impr": 0, "_pos_w": 0.0}
            by_u[u]["clicks"] += int(p.get("clicks") or 0)
            by_u[u]["impr"] += int(p.get("impr") or 0)
            by_u[u]["_pos_w"] += float(p.get("pos") or 0) * int(p.get("impr") or 0)
    out = list(by_u.values())
    for p in out:
        impr = p["impr"]
        p["ctr"] = round(p["clicks"] / impr * 100, 1) if impr else 0
        p["pos"] = round(p["_pos_w"] / impr, 1) if impr else 0
        p.pop("_pos_w", None)
    return sorted(out, key=lambda x: x["clicks"], reverse=True)[:5000]


def _merge_region_stats(*stats_list: list[dict]) -> dict:
    out: dict = {}
    for stats in stats_list:
        for grp, v in (stats or {}).items():
            if grp not in out:
                out[grp] = {
                    "clicks": 0,
                    "impr": 0,
                    "brand": {"clicks": 0, "impr": 0},
                    "nonbrand": {"clicks": 0, "impr": 0},
                }
            for key in ("clicks", "impr"):
                out[grp][key] += int(v.get(key) or 0)
            for sub in ("brand", "nonbrand"):
                for key in ("clicks", "impr"):
                    out[grp][sub][key] += int((v.get(sub) or {}).get(key) or 0)
    return out


def _merge_region_top(*tops: list[dict], n: int = 15) -> dict:
    merged: dict[str, list[dict]] = defaultdict(list)
    for top in tops:
        for grp, rows in (top or {}).items():
            merged[grp].extend(rows or [])
    return {g: _merge_kw_rows(v)[:n] for g, v in merged.items()}


def merge_gsc_snapshots(snaps: list[dict]) -> dict:
    if not snaps:
        raise ValueError("merge_gsc_snapshots: empty")
    snaps = [s for s in snaps if s]
    if not snaps:
        raise ValueError("merge_gsc_snapshots: no valid snapshots")

    keywords = _merge_kw_rows(*[s.get("keywords") or [] for s in snaps])
    countries = _merge_countries(*[s.get("countries") or [] for s in snaps])
    pages = _merge_pages(*[s.get("pages") or [] for s in snaps])
    total_cl = sum(k["clicks"] for k in keywords)
    total_impr = sum(k["impr"] for k in keywords)

    tail = snaps[-1]
    return {
        "_range": f"{snaps[0].get('_range', '')} + {tail.get('_range', '')}",
        "_label": f"{snaps[0].get('_label', '')}+{tail.get('_label', '')}",
        "keywords": keywords,
        "countries": countries,
        "pages": pages,
        "region_top_keywords": {
            g: sorted(v, key=lambda x: x["clicks"], reverse=True)[:5]
            for g, v in _merge_region_top(*[s.get("region_top_keywords") or {} for s in snaps], n=5).items()
        },
        "region_stats": _merge_region_stats(*[s.get("region_stats") or {} for s in snaps]),
        "region_brand_top": _merge_region_top(*[s.get("region_brand_top") or {} for s in snaps]),
        "region_nonbrand_top": _merge_region_top(*[s.get("region_nonbrand_top") or {} for s in snaps]),
        "region_pages": tail.get("region_pages") or {},
        "total_clicks": total_cl,
        "total_impr": total_impr,
        "avg_ctr": round(total_cl / total_impr * 100, 1) if total_impr else 0,
        "avg_pos": round(sum(k["pos"] for k in keywords) / len(keywords), 1) if keywords else 0,
        "keyword_count": len(keywords),
        "pages_with_traffic": max(int(s.get("pages_with_traffic") or 0) for s in snaps),
        "indexing_corpus_total": tail.get("indexing_corpus_total", 20_000),
        "index_rate_primary": tail.get("index_rate_primary", tail.get("index_rate", 0)),
        "sitemap_submitted": tail.get("sitemap_submitted"),
        "sitemap_indexed": tail.get("sitemap_indexed"),
        "sitemap_index_rate": tail.get("sitemap_index_rate"),
        "index_pages": tail.get("index_pages", tail.get("pages_with_traffic", 0)),
        "index_rate": tail.get("index_rate_primary", tail.get("index_rate", 0)),
    }


def merge_ga4_snapshots(snaps: list[dict]) -> dict:
    if not snaps:
        raise ValueError("merge_ga4_snapshots: empty")
    snaps = [s for s in snaps if s]
    if not snaps:
        raise ValueError("merge_ga4_snapshots: no valid snapshots")

    sessions = sum(int(s.get("sessions") or 0) for s in snaps)
    users = sum(int(s.get("users") or 0) for s in snaps)
    new_users = sum(int(s.get("new_users") or 0) for s in snaps)
    return_users = sum(int(s.get("return_users") or users - new_users) for s in snaps)

    def _wavg(field: str) -> float:
        w = sum(int(s.get("sessions") or 0) for s in snaps)
        if not w:
            return 0
        return round(sum(float(s.get(field) or 0) * int(s.get("sessions") or 0) for s in snaps) / w, 1)

    channels: dict[str, dict] = {}
    for s in snaps:
        for ch, v in (s.get("channels") or {}).items():
            if ch not in channels:
                channels[ch] = {"sessions": 0, "users": 0, "bounce": 0, "share": 0}
            channels[ch]["sessions"] += int(v.get("sessions") or 0)
            channels[ch]["users"] += int(v.get("users") or 0)
    for ch, v in channels.items():
        v["share"] = round(v["sessions"] / sessions * 100, 1) if sessions else 0

    segments: dict[str, dict] = {}
    for s in snaps:
        for seg, v in (s.get("segments") or {}).items():
            if seg not in segments:
                segments[seg] = {"sessions": 0, "dur": 0, "pages": 0, "bounce": 0, "_w": 0}
            w = int(v.get("sessions") or 0)
            segments[seg]["sessions"] += w
            segments[seg]["dur"] += float(v.get("dur") or 0) * w
            segments[seg]["pages"] += float(v.get("pages") or 0) * w
            segments[seg]["bounce"] += float(v.get("bounce") or 0) * w
            segments[seg]["_w"] += w
    for seg, v in segments.items():
        w = v.pop("_w") or 1
        v["dur"] = round(v["dur"] / w)
        v["pages"] = round(v["pages"] / w, 1)
        v["bounce"] = round(v["bounce"] / w, 1)

    geo_by_c: dict[str, dict] = {}
    for s in snaps:
        for g in s.get("geo") or []:
            c = g.get("country") or ""
            if c not in geo_by_c:
                geo_by_c[c] = {"country": c, "sessions": 0, "users": 0, "new_users": 0}
            geo_by_c[c]["sessions"] += int(g.get("sessions") or 0)
            geo_by_c[c]["users"] += int(g.get("users") or 0)
            geo_by_c[c]["new_users"] += int(g.get("new_users") or 0)

    tail = snaps[-1]
    return {
        "_label": "+".join(s.get("_label", "") for s in snaps),
        "sessions": sessions,
        "users": users,
        "new_users": new_users,
        "return_users": return_users,
        "new_user_pct": round(new_users / users * 100, 1) if users else 0,
        "avg_dur": _wavg("avg_dur"),
        "pages_per_session": _wavg("pages_per_session"),
        "bounce": _wavg("bounce"),
        "channels": channels,
        "segments": segments,
        "geo": sorted(geo_by_c.values(), key=lambda x: x["sessions"], reverse=True),
        "organic_sources": tail.get("organic_sources"),
        "bing_region_ga4": tail.get("bing_region_ga4"),
    }


def merge_sgeo_snapshots(snaps: list[dict]) -> dict:
    snaps = [s for s in snaps if s]
    if not snaps:
        return {"source_file": None, "has_monthly_dedup": False, "natural": {}}

    def _sum_nat(key: str) -> float:
        return sum(float((s.get("natural") or {}).get(key) or 0) for s in snaps)

    nat = deepcopy(snaps[-1].get("natural") or {})
    for m in ("all_uv", "new_uv", "new_pay_uv", "new_pay_amount", "all_pay_uv", "all_pay_amount"):
        if any((s.get("natural") or {}).get(m) for s in snaps):
            nat[m] = _sum_nat(m)

    return {
        "report_ym": snaps[-1].get("report_ym"),
        "source_file": " + ".join(filter(None, [s.get("source_file") for s in snaps])) or None,
        "has_monthly_dedup": all(s.get("has_monthly_dedup") for s in snaps),
        "natural": nat,
        "channel_totals": snaps[-1].get("channel_totals") or {},
    }


def merge_bing_months(bing_data: dict, months: list[str], *, build_bundle) -> dict | None:
    """build_bundle(bing_data, ym) -> dict；多月 keyword/page 合并后再走同构加工。"""
    kms: list[dict] = []
    pms: list[dict] = []
    for ym in months:
        kms.extend(bing_data.get("keywords_monthly", {}).get(ym) or [])
        pms.extend(bing_data.get("pages_monthly", {}).get(ym) or [])
    if not kms and not pms:
        return None
    synthetic = {
        "keywords_monthly": {"_merged": _merge_kw_rows(kms)},
        "pages_monthly": {"_merged": _merge_pages(pms)},
        "traffic_monthly": {},
    }
    return build_bundle(synthetic, "_merged")
