"""历史批处理路径 SSOT（historical/ 包内统一引用）。"""
from __future__ import annotations

from pathlib import Path

_HISTORICAL = Path(__file__).resolve().parent
_SCRIPTS = _HISTORICAL.parent
_GEO_DEV = _SCRIPTS.parent
PROJECT = _GEO_DEV.parent  # 1-Project

GEO_DEV = PROJECT / "1-4 Dev"
OUT_DIR = GEO_DEV / "Output/Data Ingestion"
SNAPSHOT_DIR = OUT_DIR / "monthly-snapshots"
DATAWORK_DIR = PROJECT / "1-2 Insight/From Datawork"
TRIDENT = PROJECT / "1-2 Insight/Trident Insights"
REPORTS = TRIDENT / "reports"
MONTHLY_DIR = REPORTS / "monthly"
INVENTORY_DIR = REPORTS / "_inventory"
QUARTERLY_DIR = REPORTS / "quarterly"
BIMONTHLY_DIR = REPORTS / "bimonthly"
ANNUAL_DIR = REPORTS / "annual"
LIFETIME_DIR = REPORTS / "lifetime"
TOPICS_DIR = REPORTS / "topics"
DAILY_DIR = REPORTS / "daily"
BING_FULL = REPORTS / "bing-full.json"
