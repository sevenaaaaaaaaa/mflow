"""
Lovart Sentinel - GSC Daily Data Source
Reads latest GSC CSV exports from 1-2 Insight/Keywords Research/Daily Raw Data/
"""
from __future__ import annotations

import csv
import glob
import os
from datetime import date, timedelta
from pathlib import Path

from ._common import banner

GSC_DIR = Path(__file__).resolve().parents[4] / "1-2 Insight" / "Keywords Research" / "Daily Raw Data"


def _find_latest_csv(pattern: str) -> Path | None:
    files = sorted(glob.glob(str(GSC_DIR / pattern)))
    return Path(files[-1]) if files else None


def _read_csv(path: Path) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def collect() -> dict:
    data = dict(banner("GSC Daily Overview"))
    data["date"] = date.today().isoformat()

    # 总览数据 - 找到 SearchPerformanceOverview CSV
    overview_csvs = sorted(glob.glob(str(GSC_DIR / "*SearchPerformanceOverview*.csv")))
    if overview_csvs:
        overview = Path(overview_csvs[-1])
        overview_rows = _read_csv(overview)
        data["overview"] = overview_rows[-7:] if len(overview_rows) >= 7 else overview_rows
        data["_overview_file"] = str(overview.name)

    # 查询关键词 - 找到 查询数.csv
    query_csvs = sorted(glob.glob(str(GSC_DIR / "GSC*" / "查询数.csv")))
    if query_csvs:
        queries_file = Path(query_csvs[-1])
        all_rows = _read_csv(queries_file)
        # sort by clicks descending
        sorted_rows = sorted(all_rows, key=lambda r: int(float(r.get("点击次数", "0").replace(",", ""))), reverse=True)
        data["top_queries"] = sorted_rows[:50]
        data["_queries_file"] = str(queries_file.parent.name) + "/" + queries_file.name

    # 国家/地区
    country_csvs = sorted(glob.glob(str(GSC_DIR / "GSC*" / "国家_地区.csv")))
    if country_csvs:
        country_file = Path(country_csvs[-1])
        country_rows = _read_csv(country_file)
        sorted_c = sorted(country_rows, key=lambda r: int(float(r.get("点击次数", "0").replace(",", ""))), reverse=True)
        data["top_countries"] = sorted_c[:20]

    # 页面
    page_csvs = sorted(glob.glob(str(GSC_DIR / "GSC*" / "网页.csv")))
    if page_csvs:
        page_file = Path(page_csvs[-1])
        page_rows = _read_csv(page_file)
        sorted_p = sorted(page_rows, key=lambda r: int(float(r.get("点击次数", "0").replace(",", ""))), reverse=True)
        data["top_pages"] = sorted_p[:20]

    # 设备
    device_csvs = sorted(glob.glob(str(GSC_DIR / "GSC*" / "设备.csv")))
    if device_csvs:
        data["devices"] = _read_csv(Path(device_csvs[-1]))

    return data
