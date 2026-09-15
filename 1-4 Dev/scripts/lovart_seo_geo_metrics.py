#!/usr/bin/env python3
"""
DataWorks SEO/GEO 产品漏斗数据 — SSOT

输入（每月）：
  1-2 Insight/From Datawork/{YYYY-MM} SEO GEO.xlsx
  或兼容旧版合并文件「2026 04 05 SEO GEO.xlsx」

Sheet：
  - 日明细（默认 DataWorks 导出表）：pt × organic_discovery_type × referer_platform_hint
  - monthly_dedup（可选）：月去重 UV；无则日明细加总（脚注说明）
"""
from __future__ import annotations

import json
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any

PROJECT = Path(
    str(Path(__file__).resolve().parents[2])
)
DATAWORK_DIR = PROJECT / "1-2 Insight" / "From Datawork"
SNAPSHOT_DIR = PROJECT / "1-4 Dev" / "Output" / "Data Ingestion" / "monthly-snapshots"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

DAILY_METRICS = (
    "all_uv", "new_uv", "all_paywall_uv", "all_click2pay_uv", "all_pay_uv",
    "all_pay_amount", "all_order_cnt", "all_dialog_uv", "all_generate_uv", "all_export_uv",
    "all_retain_d7_uv", "new_pay_uv", "new_pay_amount", "new_dialog_uv", "new_generate_uv",
)
DEDUP_METRICS = (
    "all_uv", "new_uv", "all_pay_uv", "new_pay_uv", "all_pay_amount", "new_pay_amount",
    "all_dialog_uv", "all_generate_uv", "all_paywall_uv", "all_retain_d7_uv",
)

GA4_DATAWORK_FOOTNOTE = (
    "> **GA4 Organic Sessions vs DataWorks** — GA4 为 **会话（Sessions）**；"
    "DataWorks 为 **自然搜索发现用户（SEO+GEO）** 的产品行为（访问/注册/付费/活跃）。"
    "受 stream 过滤、归因窗口影响，**Sessions 与 UV 不可直接对比绝对值**，应看趋势与转化率。"
)

DAILY_SUM_FOOTNOTE = (
    "> **DataWorks 汇总口径** — 访问/注册/活跃 UV 为当月 **日×平台加总**（同一用户跨平台/多日可能重复计数）；"
    "**付费金额、订单数为可加总实数**。月去重表就绪后将替换 UV 类指标。"
)

NEW_VS_ALL_PAY_FOOTNOTE = (
    "> **新增 vs 累计付费** — OKR 注册/付费达成率用 **`new_uv` / `new_pay_uv` / `new_pay_amount`**（当月新增，日×平台加总）；"
    "**`all_pay_uv` / `all_pay_amount` / `all_arppu`** 为累计存量，仅作对照，**不做相减**。"
)

# 兼容旧 import
CUMULATIVE_PAY_FOOTNOTE = NEW_VS_ALL_PAY_FOOTNOTE

OKR_NATURAL_FOOTNOTE = (
    "> **O1 自然搜索** — 访问 UV 以 DataWorks **`all_uv`**、注册/新增付费以 **`new_uv` / `new_pay_*`** 计（**自然搜索 = SEO + GEO**）；GA4 Sessions 仅渠道参考。"
)


def _float(v: Any) -> float:
    try:
        if v in ("", None, r"\N", "\\N"):
            return 0.0
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _ym_to_pt_prefix(ym: str) -> str:
    return ym.replace("-", "")


def resolve_xlsx_path(report_ym: str) -> Path | None:
    """优先单月文件，再回退合并导出。"""
    candidates = [
        DATAWORK_DIR / f"{report_ym} SEO GEO.xlsx",
        DATAWORK_DIR / f"{report_ym.replace('-', ' ')} SEO GEO.xlsx",
        DATAWORK_DIR / "2026 04 05 SEO GEO.xlsx",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def _col_to_idx(col: str) -> int:
    n = 0
    for c in col:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def _parse_cell_ref(ref: str) -> tuple[int, int]:
    m = re.match(r"([A-Z]+)(\d+)", ref)
    return _col_to_idx(m.group(1)), int(m.group(2)) - 1


def _read_xlsx_sheet(z: zipfile.ZipFile, sheet_path: str, max_row: int = 5000) -> list[dict]:
    ss_root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    strings = [
        "".join((t.text or "") for t in si.findall(".//m:t", NS))
        for si in ss_root.findall(".//m:si", NS)
    ]
    root = ET.fromstring(z.read(sheet_path))
    rows: dict[int, dict[int, str]] = {}
    for row in root.findall(".//m:sheetData/m:row", NS):
        ri = int(row.get("r")) - 1
        if ri > max_row:
            break
        for c in row.findall("m:c", NS):
            ci, _ = _parse_cell_ref(c.get("r"))
            v = c.find("m:v", NS)
            if v is None or v.text is None:
                val = ""
            elif c.get("t") == "s":
                val = strings[int(v.text)]
            else:
                val = v.text
            rows.setdefault(ri, {})[ci] = val
    if not rows:
        return []
    max_c = max(ci for r in rows for ci in rows[r])
    header = [rows[0].get(i, "") for i in range(max_c + 1)]
    out = []
    for r in range(1, max(rows) + 1):
        if r not in rows:
            continue
        if not any(str(rows[r].get(i, "")).strip() for i in rows[r]):
            continue
        rec = {header[i]: rows[r].get(i, "") for i in range(len(header)) if header[i]}
        if rec:
            out.append(rec)
    return out


def _sheet_paths(z: zipfile.ZipFile) -> dict[str, str]:
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {}
    for rel in rels:
        rid_to_target[rel.get("Id")] = rel.get("Target")
    mapping = {}
    for s in wb.findall(".//m:sheet", NS):
        name = s.get("name")
        rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rid_to_target.get(rid, "")
        if target.startswith("worksheets/"):
            mapping[name] = "xl/" + target
    return mapping


def _normalize_month(row: dict) -> str:
    for key in ("report_month", "report_ym", "ym", "pt_month", "month"):
        v = str(row.get(key, "")).strip()
        if not v:
            continue
        if len(v) == 6 and v.isdigit():
            return f"{v[:4]}-{v[4:6]}"
        if len(v) >= 7 and "-" in v:
            return v[:7]
    pt = str(row.get("pt", "")).strip()
    if len(pt) >= 6 and pt.isdigit():
        return f"{pt[:4]}-{pt[4:6]}"
    return ""


def _pick_daily_sheet(sheets: dict[str, str]) -> str | None:
    for name, path in sheets.items():
        if name.lower() in ("monthly_dedup", "月去重", "sheet1"):
            continue
        if "dataworks" in name.lower() or name.lower() == "sheet2":
            return path
    for name, path in sheets.items():
        if name.lower() not in ("monthly_dedup", "月去重", "sheet1"):
            return path
    return None


def _pick_dedup_sheet(sheets: dict[str, str]) -> str | None:
    for key in ("monthly_dedup", "月去重", "Monthly_Dedup"):
        if key in sheets:
            return sheets[key]
    return None


def load_xlsx_bundle(xlsx_path: Path) -> dict:
    with zipfile.ZipFile(xlsx_path) as z:
        sheets = _sheet_paths(z)
        daily_path = _pick_daily_sheet(sheets)
        dedup_path = _pick_dedup_sheet(sheets)
        daily = _read_xlsx_sheet(z, daily_path) if daily_path else []
        dedup = _read_xlsx_sheet(z, dedup_path, max_row=500) if dedup_path else []
    return {
        "source_file": str(xlsx_path),
        "daily": daily,
        "monthly_dedup": dedup,
        "has_monthly_dedup": bool(dedup),
    }


def _channel_totals_from_plat(plat: dict) -> dict[str, dict]:
    """按 seo/geo 加总日×平台行。"""
    raw: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for (ch, _p), vals in plat.items():
        for m in DAILY_METRICS:
            raw[ch][m] += vals[m]
    out = {}
    for ch, vals in raw.items():
        uv = vals["all_uv"]
        pay_uv = vals["all_pay_uv"]
        dlg = vals["all_dialog_uv"]
        new_pay = vals["new_pay_uv"]
        new_amt = vals["new_pay_amount"]
        out[ch] = {
            **dict(vals),
            "all_pay_rate": round(pay_uv / uv * 100, 2) if uv else 0,
            "all_dialog_rate": round(dlg / uv * 100, 2) if uv else 0,
            "all_generate_rate": round(vals["all_generate_uv"] / uv * 100, 2) if uv else 0,
            "all_export_rate": round(vals["all_export_uv"] / uv * 100, 2) if uv else 0,
            "all_arppu": round(vals["all_pay_amount"] / pay_uv, 2) if pay_uv else 0,
            "new_pay_rate": round(new_pay / vals["new_uv"] * 100, 2) if vals["new_uv"] else 0,
            "new_arppu": round(new_amt / new_pay, 2) if new_pay else 0,
        }
    if "seo" in out and "geo" in out:
        nat = defaultdict(float)
        for ch in ("seo", "geo"):
            for m in DAILY_METRICS:
                nat[m] += out[ch].get(m, 0)
        uv = nat["all_uv"]
        pay_uv = nat["all_pay_uv"]
        new_pay = nat["new_pay_uv"]
        out["natural"] = {
            **dict(nat),
            "all_pay_rate": round(pay_uv / uv * 100, 2) if uv else 0,
            "all_dialog_rate": round(nat["all_dialog_uv"] / uv * 100, 2) if uv else 0,
            "all_generate_rate": round(nat["all_generate_uv"] / uv * 100, 2) if uv else 0,
            "all_export_rate": round(nat["all_export_uv"] / uv * 100, 2) if uv else 0,
            "all_arppu": round(nat["all_pay_amount"] / pay_uv, 2) if pay_uv else 0,
            "new_pay_rate": round(new_pay / nat["new_uv"] * 100, 2) if nat["new_uv"] else 0,
            "new_arppu": round(nat["new_pay_amount"] / new_pay, 2) if new_pay else 0,
        }
    return out


def _dau_share_pct_from_rows(daily_rows: list[dict], report_ym: str) -> dict[str, float]:
    """按日汇总 SEO / GEO / SEO+GEO 占全渠道 DAU 比例（日均 %）。"""
    prefix = _ym_to_pt_prefix(report_ym)
    by_pt: dict[str, dict[str, float]] = {}
    for row in daily_rows:
        pt = str(row.get("pt", ""))
        if not pt.startswith(prefix):
            continue
        ch = str(row.get("organic_discovery_type", "")).strip().lower()
        if ch not in ("seo", "geo"):
            continue
        bucket = by_pt.setdefault(
            pt,
            {"total_dau": 0.0, "seo_geo_share": 0.0, "seo_uv": 0.0, "geo_uv": 0.0},
        )
        bucket["total_dau"] = max(bucket["total_dau"], _float(row.get("total_dau_uv")))
        sg = _float(row.get("seo_geo_dau_share"))
        if sg:
            bucket["seo_geo_share"] = sg
        bucket[f"{ch}_uv"] += _float(row.get("all_uv"))

    seo_ratios: list[float] = []
    geo_ratios: list[float] = []
    combined: list[float] = []
    for bucket in by_pt.values():
        t = bucket["total_dau"]
        if bucket["seo_geo_share"]:
            combined.append(bucket["seo_geo_share"])
        if t > 0:
            seo_ratios.append(bucket["seo_uv"] / t)
            geo_ratios.append(bucket["geo_uv"] / t)

    avg_combined = sum(combined) / len(combined) if combined else 0.0
    avg_seo = sum(seo_ratios) / len(seo_ratios) if seo_ratios else 0.0
    avg_geo = sum(geo_ratios) / len(geo_ratios) if geo_ratios else 0.0
    return {
        "seo_geo_combined_pct": round(avg_combined * 100, 2),
        "seo_pct": round(avg_seo * 100, 2),
        "geo_pct": round(avg_geo * 100, 2),
    }


def aggregate_daily(daily_rows: list[dict], report_ym: str) -> dict:
    """日×平台加总为月度产品指标（UV 类指标含重复计数，见 DAILY_SUM_FOOTNOTE）。"""
    prefix = _ym_to_pt_prefix(report_ym)
    plat: dict[tuple[str, str], dict[str, float]] = defaultdict(lambda: defaultdict(float))

    for row in daily_rows:
        pt = str(row.get("pt", ""))
        if not pt.startswith(prefix):
            continue
        ch = str(row.get("organic_discovery_type", "")).strip().lower()
        plat_key = str(row.get("referer_platform_hint", "")).strip() or "(unknown)"
        if ch not in ("seo", "geo"):
            continue
        key = (ch, plat_key)
        for m in DAILY_METRICS:
            plat[key][m] += _float(row.get(m))

    channel_dau_share_pct = _dau_share_pct_from_rows(daily_rows, report_ym)
    avg_share = channel_dau_share_pct.get("seo_geo_combined_pct", 0.0)

    by_channel: dict[str, dict] = {}
    for (ch, p), vals in plat.items():
        uv = vals.get("all_uv", 0)
        if uv <= 0:
            continue
        chd = by_channel.setdefault(ch, {"platforms": [], "row_sum_uv": 0.0})
        chd["row_sum_uv"] += uv
        pay = vals.get("all_pay_uv", 0)
        new_pay = vals.get("new_pay_uv", 0)
        new_amt = vals.get("new_pay_amount", 0)
        chd["platforms"].append({
            "platform": p,
            "all_uv": uv,
            "new_uv": vals.get("new_uv", 0),
            "new_pay_uv": new_pay,
            "new_pay_amount": new_amt,
            "new_arppu": round(new_amt / new_pay, 2) if new_pay else 0,
            "all_pay_uv": pay,
            "all_pay_amount": vals.get("all_pay_amount", 0),
            "all_order_cnt": vals.get("all_order_cnt", 0),
            "all_arppu": round(vals.get("all_pay_amount", 0) / pay, 2) if pay else 0,
            "all_dialog_uv": vals.get("all_dialog_uv", 0),
            "all_generate_uv": vals.get("all_generate_uv", 0),
            "all_export_uv": vals.get("all_export_uv", 0),
            "all_retain_d7_uv": vals.get("all_retain_d7_uv", 0),
            "pay_rate": round(pay / uv * 100, 2) if uv else 0,
            "new_pay_rate": round(new_pay / vals.get("new_uv", 0) * 100, 2) if vals.get("new_uv") else 0,
            "dialog_rate": round(vals.get("all_dialog_uv", 0) / uv * 100, 2) if uv else 0,
            "generate_rate": round(vals.get("all_generate_uv", 0) / uv * 100, 2) if uv else 0,
        })
    for ch in by_channel:
        by_channel[ch]["platforms"].sort(key=lambda x: x["all_uv"], reverse=True)

    plat_dict = dict(plat)
    channel_totals = _channel_totals_from_plat(plat_dict)

    return {
        "report_ym": report_ym,
        "avg_seo_geo_dau_share_pct": avg_share,
        "channel_dau_share_pct": channel_dau_share_pct,
        "by_channel": by_channel,
        "channel_totals": channel_totals,
        "data_source": "daily_row_sum",
    }


def parse_monthly_dedup(rows: list[dict], report_ym: str) -> dict:
    """月去重表：报告主指标。"""
    out: dict[str, dict] = {}
    for row in rows:
        ym = _normalize_month(row)
        if ym != report_ym:
            continue
        ch = str(row.get("organic_discovery_type", "")).strip().lower()
        if ch in ("", "all", "natural", "自然搜索"):
            ch = "natural"
        elif ch not in ("seo", "geo"):
            continue
        bucket = out.setdefault(ch, {})
        for m in DEDUP_METRICS:
            if m in row:
                bucket[m] = _float(row.get(m))
    return out


def build_month_snapshot(report_ym: str, bundle: dict | None = None) -> dict:
    path = resolve_xlsx_path(report_ym)
    if bundle is None:
        if not path:
            return {
                "report_ym": report_ym,
                "source_file": None,
                "has_monthly_dedup": False,
                "dedup": {},
                "daily": {},
                "natural": {},
            }
        bundle = load_xlsx_bundle(path)

    daily_agg = aggregate_daily(bundle["daily"], report_ym)
    dedup = parse_monthly_dedup(bundle["monthly_dedup"], report_ym)

    channel_totals = daily_agg.get("channel_totals") or {}
    natural = channel_totals.get("natural") or {}
    data_source = daily_agg.get("data_source", "daily_row_sum")

    if dedup:
        if "natural" in dedup:
            natural = _enrich_dedup_metrics(dedup["natural"])
        else:
            natural = {}
            for m in DEDUP_METRICS:
                natural[m] = sum(dedup.get(ch, {}).get(m, 0) for ch in ("seo", "geo"))
            natural = _enrich_dedup_metrics(natural)
        for ch in ("seo", "geo"):
            if ch in dedup:
                channel_totals[ch] = _enrich_dedup_metrics(dedup[ch])
        data_source = "monthly_dedup"

    return {
        "report_ym": report_ym,
        "source_file": bundle.get("source_file"),
        "has_monthly_dedup": bool(dedup),
        "data_source": data_source,
        "dedup": dedup,
        "daily": daily_agg,
        "channel_totals": channel_totals,
        "natural": natural,
        "dau_share_pct": daily_agg.get("channel_dau_share_pct") or {},
    }


def _enrich_dedup_metrics(d: dict) -> dict:
    uv = _float(d.get("all_uv"))
    pay_uv = _float(d.get("all_pay_uv"))
    dlg = _float(d.get("all_dialog_uv"))
    gen = _float(d.get("all_generate_uv"))
    exp = _float(d.get("all_export_uv"))
    new_uv = _float(d.get("new_uv"))
    new_pay = _float(d.get("new_pay_uv"))
    new_amt = _float(d.get("new_pay_amount"))
    amt = _float(d.get("all_pay_amount"))
    out = dict(d)
    out["all_pay_rate"] = round(pay_uv / uv * 100, 2) if uv else 0
    out["all_dialog_rate"] = round(dlg / uv * 100, 2) if uv else 0
    out["all_generate_rate"] = round(gen / uv * 100, 2) if uv else 0
    out["all_export_rate"] = round(exp / uv * 100, 2) if uv else 0
    out["all_arppu"] = round(amt / pay_uv, 2) if pay_uv else 0
    out["new_pay_rate"] = round(new_pay / new_uv * 100, 2) if new_uv else 0
    out["new_arppu"] = round(new_amt / new_pay, 2) if new_pay else 0
    return out


def save_seo_geo_snapshot(report_ym: str, data: dict) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    p = SNAPSHOT_DIR / f"seo-geo-{report_ym}.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def load_seo_geo_snapshot(report_ym: str) -> dict | None:
    p = SNAPSHOT_DIR / f"seo-geo-{report_ym}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def ingest_for_month(report_ym: str) -> dict:
    snap = build_month_snapshot(report_ym)
    save_seo_geo_snapshot(report_ym, snap)
    return snap


def _dedup_get(dedup: dict, ch: str, metric: str) -> float:
    return float(dedup.get(ch, {}).get(metric, 0))


def dau_share_pct(snap: dict | None) -> dict:
    if not snap:
        return {}
    return snap.get("dau_share_pct") or (snap.get("daily") or {}).get("channel_dau_share_pct") or {}


def natural_pay_metrics(sgeo_prev: dict | None, sgeo_curr: dict) -> dict[str, int]:
    """自然搜索付费：new_pay 用于 OKR，all_pay 仅展示累计。"""
    prev_nat, curr_nat = merge_natural_dedup(sgeo_prev, sgeo_curr)
    return {
        "new_pay_p": int(prev_nat.get("new_pay_uv", 0)),
        "new_pay_c": int(curr_nat.get("new_pay_uv", 0)),
        "new_pay_amt_p": int(round(prev_nat.get("new_pay_amount", 0))),
        "new_pay_amt_c": int(round(curr_nat.get("new_pay_amount", 0))),
        "all_pay_p": int(prev_nat.get("all_pay_uv", 0)),
        "all_pay_c": int(curr_nat.get("all_pay_uv", 0)),
        "reg_p": int(prev_nat.get("new_uv", 0)),
        "reg_c": int(curr_nat.get("new_uv", 0)),
    }


def cumulative_pay_delta(sgeo_prev: dict | None, sgeo_curr: dict) -> tuple[int, int, int]:
    """已废弃：请用 natural_pay_metrics。保留兼容返回 all_pay 双月与差值。"""
    m = natural_pay_metrics(sgeo_prev, sgeo_curr)
    return m["all_pay_p"], m["all_pay_c"], m["all_pay_c"] - m["all_pay_p"]


def channel_metrics(snap: dict | None, ch: str = "natural") -> dict:
    if not snap:
        return {}
    if snap.get("data_source") == "monthly_dedup" and ch == "natural":
        return snap.get("natural") or {}
    totals = snap.get("channel_totals") or {}
    return totals.get(ch) or snap.get("natural") or {}


def merge_natural_dedup(prev: dict | None, curr: dict) -> tuple[dict, dict]:
    """返回 (prev_natural, curr_natural) 用于环比。"""
    return channel_metrics(prev, "natural"), channel_metrics(curr, "natural")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest DataWorks SEO/GEO xlsx")
    parser.add_argument("--month", required=True, help="YYYY-MM")
    args = parser.parse_args()
    snap = ingest_for_month(args.month)
    nat = (snap.get("channel_totals") or {}).get("natural") or snap.get("natural") or {}
    print(json.dumps({
        "file": snap.get("source_file"),
        "data_source": snap.get("data_source"),
        "has_monthly_dedup": snap.get("has_monthly_dedup"),
        "natural_uv": int(nat.get("all_uv", 0)),
        "natural_new_pay_uv": int(nat.get("new_pay_uv", 0)),
        "natural_new_pay_amount": round(nat.get("new_pay_amount", 0), 2),
        "natural_all_pay_uv": int(nat.get("all_pay_uv", 0)),
    }, ensure_ascii=False, indent=2))
