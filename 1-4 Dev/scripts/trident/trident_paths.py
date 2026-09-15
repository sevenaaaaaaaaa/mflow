#!/usr/bin/env python3
"""Local output paths for Lovart Trident data scripts."""
import os
from pathlib import Path


LOCAL_DEV_ROOT = Path(os.environ.get("LOVART_LOCAL_DEV_ROOT", Path.home() / "Documents" / "Lovart Local Dev"))
DATA_INGESTION_DIR = Path(os.environ.get("LOVART_TRIDENT_OUTPUT_DIR", LOCAL_DEV_ROOT / "Output" / "Data Ingestion"))
WAREHOUSE_DIR = Path(os.environ.get("LOVART_TRIDENT_WAREHOUSE_DIR", LOCAL_DEV_ROOT / "Output" / "Warehouse"))


def ensure_trident_dirs():
    DATA_INGESTION_DIR.mkdir(parents=True, exist_ok=True)
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

