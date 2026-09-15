#!/usr/bin/env python3
"""
Lovart Sentinel - 数据采集编排器 V4 (品牌配置化)
================================================
用法:
  python collect.py --brand lovart
  python collect.py --brand canva --mode competitor
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import yaml
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SENTINEL_ROOT = Path(__file__).resolve().parent
BRANDS_DIR = SENTINEL_ROOT / "brands"
RAW_OUT = PROJECT_ROOT / "1-2 Insight" / "Lovart ORM" / "raw"


def today_str() -> str:
    return datetime.date.today().isoformat()


def ensure_dirs() -> Path:
    d = RAW_OUT / today_str()
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_brand(name: str) -> Optional[dict]:
    path = BRANDS_DIR / f"{name}.yaml"
    if not path.exists():
        print(f"  [ERR] Brand config not found: {path}", file=sys.stderr)
        print(f"  Available: {[p.stem for p in BRANDS_DIR.glob('*.yaml') if p.stem != '_template']}", file=sys.stderr)
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def run_source(name: str, out_dir: Path, brand_config: Optional[dict] = None) -> Optional[Path]:
    mod_path = SENTINEL_ROOT / "sources" / f"{name}.py"
    if not mod_path.exists():
        print(f"  [SKIP] source not found: {name}", file=sys.stderr)
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"sources.{name}", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "collect"):
        print(f"  [SKIP] {name}.py missing collect()", file=sys.stderr)
        return None
    print(f"  [RUN ] {name} ...")
    try:
        import inspect
        sig = inspect.signature(mod.collect)
        if len(sig.parameters) > 0 and brand_config:
            data = mod.collect(brand_config=brand_config)
        else:
            data = mod.collect()
    except Exception as e:
        print(f"  [ERR ] {name}: {e}", file=sys.stderr)
        return None
    if data is None:
        print(f"  [NONE] {name} returned None", file=sys.stderr)
        return None
    out_path = out_dir / f"{name}.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"  [DONE] {name} -> {out_path}")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Lovart Sentinel Collector V4")
    parser.add_argument("--source", default="all", help="Source module name or 'all'")
    parser.add_argument("--brand", default="lovart", help="Brand config name (e.g., lovart, canva)")
    parser.add_argument("--mode", default="weekly", choices=["weekly", "daily", "competitor", "pulse"])
    args = parser.parse_args()

    brand_config = load_brand(args.brand)
    if not brand_config:
        return 1

    brand_name = brand_config["brand"]["name"]
    out_dir = ensure_dirs()
    print(f"[Sentinel] brand={args.brand} ({brand_name}), mode={args.mode}")

    with open(out_dir / "_brand.yaml", "w") as f:
        yaml.dump(brand_config, f, allow_unicode=True)

    ALL_SOURCES = [
        "gsc_daily", "gsc_weekly", "i18n_keyword_intelligence", "email_health", "content_production",
        "serp_bing", "serp_baidu", "serp_sogou",
        "social_x", "social_linkedin",
        "social_instagram", "social_tiktok", "social_youtube", "social_reddit",
        "china_shortvideo",
        "product_hunt", "ai_directories",
        "design_communities",
        "competitor_social",
        "media_polling",
        "propagation_tracker", "sentiment_quantifier",
    ]

    sources = ALL_SOURCES if args.source == "all" else [args.source]
    results = {}
    for s in sources:
        path = run_source(s, out_dir, brand_config)
        results[s] = str(path) if path else "FAILED"

    with open(out_dir / "_summary.json", "w") as f:
        json.dump({
            "date": today_str(), "brand": args.brand, "mode": args.mode,
            "sources": results,
            "success_count": sum(1 for v in results.values() if v != "FAILED"),
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[Sentinl] done. {sum(1 for v in results.values() if v != 'FAILED')}/{len(results)} OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
