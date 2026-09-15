#!/usr/bin/env python3
"""
历史 SEO 报告批处理编排器。

子命令：
  inventory          扫描数据覆盖 → history-coverage.json
  backfill-snapshots 按月拉 GSC/GA4 快照（调用 seo_monthly_v2）
  render-monthly     生成月报（draft/full）+ Draft 后处理
  render-weekly      批量复盘周/自然周
  render-quarterly   季报（聚合月快照）
  render-bimonthly   双月报（连续两月 vs 上两月）
  render-annual      年报（聚合月快照）
  render-topics      维度专题报告
  render-daily       日报（默认近 90 天）
  finalize-monthly   DataWorks 补齐后升 Final
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPTS = _SCRIPT_DIR.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from path_constants import BING_FULL, SNAPSHOT_DIR, TRIDENT
from week_dates_local import iter_natural_weeks, iter_review_weeks, month_range
from seo_report_tier import DATA_TIER_DRAFT, DATA_TIER_FULL

PYTHON = sys.executable
MONTHLY_SCRIPT = _SCRIPTS / "seo_monthly_v2.py"
MONTHLY_TIER_SCRIPT = _SCRIPT_DIR / "monthly_with_tier.py"
WEEKLY_SCRIPT = _SCRIPTS / "weekly_review_v3.py"


def _run(cmd: list[str], **kw) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=str(_SCRIPTS), **kw)


def cmd_inventory(args: argparse.Namespace) -> None:
    from report_inventory import main as inventory_main

    to_ym = args.to or date.today().strftime("%Y-%m")
    inventory_main(args.from_ym, to_ym)


def cmd_backfill_snapshots(args: argparse.Namespace) -> None:
    for ym in month_range(args.from_ym, args.to):
        gsc = SNAPSHOT_DIR / f"gsc-{ym}.json"
        if gsc.is_file() and not args.force:
            print(f"  skip {ym} (gsc snapshot exists)")
            continue
        extra = ["--resume", "--snapshots-only"]
        if args.refresh_indexing:
            extra.append("--refresh-indexing")
        _run([PYTHON, str(MONTHLY_SCRIPT), "--month", ym] + extra)
        _extract_bing_month(ym)


def _extract_bing_month(ym: str) -> None:
    """从 bing-full.json 写出 bing-YYYY-MM.json 月切片。"""
    if not BING_FULL.is_file():
        return
    try:
        data = json.loads(BING_FULL.read_text())
    except Exception:
        return
    out = {
        "month": ym,
        "keywords_monthly": (data.get("keywords_monthly") or {}).get(ym),
        "pages_monthly": (data.get("pages_monthly") or {}).get(ym),
        "traffic_monthly": (data.get("traffic_monthly") or {}).get(ym),
    }
    if not any(out[k] for k in ("keywords_monthly", "pages_monthly", "traffic_monthly")):
        return
    p = SNAPSHOT_DIR / f"bing-{ym}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"  bing snapshot {p.name}")


def cmd_render_monthly(args: argparse.Namespace) -> None:
    tier = args.tier
    for ym in month_range(args.from_ym, args.to):
        ro = ["--render-only"] if args.render_only else []
        resume = ["--resume"] if args.resume and not args.render_only else []
        cmd = [
            PYTHON,
            str(MONTHLY_TIER_SCRIPT),
            "--month",
            ym,
            "--data-tier",
            tier,
        ] + ro + resume
        try:
            subprocess.run(cmd, check=True, cwd=str(_SCRIPT_DIR))
        except subprocess.CalledProcessError:
            if args.skip_errors:
                print(f"  ⚠️ skip failed month {ym}")
                continue
            raise


def cmd_render_weekly(args: argparse.Namespace) -> None:
    start = date.fromisoformat(args.from_date)
    end = date.fromisoformat(args.to_date)
    weeks = iter_review_weeks(start, end) if args.type == "review" else iter_natural_weeks(start, end)
    for ws, we in weeks:
        anchor = we
        out = TRIDENT / "reports" / "weekly"
        if args.type == "review":
            fname = f"Lovart-SEO-review-{ws}-{we}.md"
        else:
            fname = f"Lovart-SEO-Week_{ws}_{we}.md"
        if (out / fname).is_file() and not args.force:
            print(f"  skip {fname}")
            continue
        try:
            if args.type == "natural":
                from weekly_helpers import run_natural_week
                run_natural_week(anchor)
            else:
                _run([PYTHON, str(WEEKLY_SCRIPT), "--week", anchor])
        except subprocess.CalledProcessError:
            if args.skip_errors:
                print(f"  ⚠️ skip week {ws}~{we}")
                continue
            raise


def cmd_render_bimonthly(args: argparse.Namespace) -> None:
    from bimonth_with_tier import run as run_bimonth_tier
    from seo_bimonthly import iter_bimonths

    for y, b in iter_bimonths(args.from_ym, args.to):
        try:
            run_bimonth_tier(y, b, data_tier=args.tier, render_only=True)
        except Exception as e:
            if args.skip_errors:
                print(f"  ⚠️ {y}-B{b}: {e}")
            else:
                raise


def cmd_render_quarterly(args: argparse.Namespace) -> None:
    from seo_quarterly import render_quarter

    fy, fq = _parse_quarter_arg(args.from_ym)
    ty, tq = _parse_quarter_arg(args.to)
    y, q = fy, fq
    while (y, q) <= (ty, tq):
        try:
            render_quarter(y, q, tier=args.tier)
        except Exception as e:
            if args.skip_errors:
                print(f"  ⚠️ {y}-Q{q}: {e}")
            else:
                raise
        q += 1
        if q > 4:
            q, y = 1, y + 1


def _parse_quarter_arg(s: str) -> tuple[int, int]:
    if "-Q" in s.upper():
        y, q = s.upper().split("-Q", 1)
        return int(y), int(q)
    y, m = s.split("-")
    return int(y), (int(m) - 1) // 3 + 1


def cmd_render_annual(args: argparse.Namespace) -> None:
    from seo_annual import render_year

    for y in range(args.from_year, args.to_year + 1):
        try:
            render_year(y, tier=args.tier)
        except Exception as e:
            if args.skip_errors:
                print(f"  ⚠️ {y}: {e}")
            else:
                raise


def cmd_render_topics(args: argparse.Namespace) -> None:
    from seo_topic_render import render_all_topics

    for ym in month_range(args.from_ym, args.to):
        try:
            render_all_topics(ym)
        except Exception as e:
            if args.skip_errors:
                print(f"  ⚠️ topics {ym}: {e}")
            else:
                raise


def cmd_render_daily(args: argparse.Namespace) -> None:
    from seo_daily import render_daily_range

    end = date.fromisoformat(args.to_date) if args.to_date else date.today()
    start = end - timedelta(days=args.days - 1)
    render_daily_range(start, end, skip_existing=not args.force)


def cmd_finalize_monthly(args: argparse.Namespace) -> None:
    from finalize_monthly import finalize_month

    for ym in month_range(args.from_ym, args.to):
        try:
            finalize_month(ym, render_only=args.render_only)
        except Exception as e:
            if args.skip_errors:
                print(f"  ⚠️ finalize {ym}: {e}")
            else:
                raise


def default_16mo_from() -> str:
    d = date.today().replace(day=1) - timedelta(days=16 * 31)
    return d.strftime("%Y-%m")


def main() -> None:
    p = argparse.ArgumentParser(description="Lovart 历史 SEO 报告批处理")
    sub = p.add_subparsers(dest="cmd", required=True)

    inv = sub.add_parser("inventory")
    inv.add_argument("--from", dest="from_ym", default=default_16mo_from())
    inv.add_argument("--to", default=None)
    inv.set_defaults(func=cmd_inventory)

    bf = sub.add_parser("backfill-snapshots")
    bf.add_argument("--from", dest="from_ym", default=default_16mo_from())
    bf.add_argument("--to", default=date.today().strftime("%Y-%m"))
    bf.add_argument("--force", action="store_true")
    bf.add_argument("--refresh-indexing", action="store_true")
    bf.set_defaults(func=cmd_backfill_snapshots)

    rm = sub.add_parser("render-monthly")
    rm.add_argument("--from", dest="from_ym", default=default_16mo_from())
    rm.add_argument("--to", default=date.today().strftime("%Y-%m"))
    rm.add_argument("--tier", default=DATA_TIER_DRAFT, choices=[DATA_TIER_DRAFT, DATA_TIER_FULL])
    rm.add_argument("--render-only", action="store_true")
    rm.add_argument("--resume", action="store_true", default=True)
    rm.add_argument("--skip-errors", action="store_true")
    rm.set_defaults(func=cmd_render_monthly)

    rw = sub.add_parser("render-weekly")
    rw.add_argument("--type", choices=["review", "natural"], default="review")
    rw.add_argument("--from-date", default=(date.today() - timedelta(days=120)).isoformat())
    rw.add_argument("--to-date", default=date.today().isoformat())
    rw.add_argument("--force", action="store_true")
    rw.add_argument("--skip-errors", action="store_true")
    rw.set_defaults(func=cmd_render_weekly)

    rq = sub.add_parser("render-quarterly")
    rq.add_argument("--from", dest="from_ym", default="2025-Q1")
    cq = (date.today().month - 1) // 3 + 1
    rq.add_argument("--to", default=f"{date.today().year}-Q{cq}")
    rq.add_argument("--tier", default=DATA_TIER_DRAFT)
    rq.add_argument("--skip-errors", action="store_true")
    rq.set_defaults(func=cmd_render_quarterly)

    rb = sub.add_parser("render-bimonthly")
    rb.add_argument("--from", dest="from_ym", default="2025-B1")
    rb.add_argument("--to", default=f"{date.today().year}-B{(date.today().month + 1) // 2}")
    rb.add_argument("--tier", default=DATA_TIER_DRAFT)
    rb.add_argument("--skip-errors", action="store_true")
    rb.set_defaults(func=cmd_render_bimonthly)

    ra = sub.add_parser("render-annual")
    ra.add_argument("--from-year", type=int, default=date.today().year - 1)
    ra.add_argument("--to-year", type=int, default=date.today().year)
    ra.add_argument("--tier", default=DATA_TIER_DRAFT)
    ra.add_argument("--skip-errors", action="store_true")
    ra.set_defaults(func=cmd_render_annual)

    rt = sub.add_parser("render-topics")
    rt.add_argument("--from", dest="from_ym", default=default_16mo_from())
    rt.add_argument("--to", default=date.today().strftime("%Y-%m"))
    rt.add_argument("--skip-errors", action="store_true")
    rt.set_defaults(func=cmd_render_topics)

    rd = sub.add_parser("render-daily")
    rd.add_argument("--days", type=int, default=90)
    rd.add_argument("--to-date", default=None)
    rd.add_argument("--force", action="store_true")
    rd.set_defaults(func=cmd_render_daily)

    fin = sub.add_parser("finalize-monthly")
    fin.add_argument("--from", dest="from_ym", default=default_16mo_from())
    fin.add_argument("--to", default=date.today().strftime("%Y-%m"))
    fin.add_argument("--render-only", action="store_true", default=True)
    fin.add_argument("--skip-errors", action="store_true")
    fin.set_defaults(func=cmd_finalize_monthly)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
