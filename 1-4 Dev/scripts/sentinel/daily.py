#!/usr/bin/env python3
"""
Lovart Sentinel - Daily Agent Workflow
======================================
这是 opencode agent 每日运行的入口脚本。
它结合本地数据读取 + webfetch 远程采集，生成完整舆情报告。

agent 每日运行流程：
  1. 读取本地 GSC CSV / SEO报告 / 邮件复盘
  2. webfetch 调用各社媒/搜索API
  3. 运行 report.py 生成舆情日报
  4. 输出到 1-2 Insight/Lovart ORM/
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SENTINEL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SENTINEL_DIR.parents[2]


def main():
    print("=" * 60)
    print("  Lovart Sentinel - Daily Agent Workflow")
    print("=" * 60)

    # Step 1: 运行本地数据采集
    print("\n[1/4] 采集本地数据源...")
    try:
        subprocess.run(
            [sys.executable, str(SENTINEL_DIR / "collect.py"), "--source", "all"],
            check=False, cwd=str(PROJECT_ROOT)
        )
    except Exception as e:
        print(f"  [WARN] collect.py failed: {e}")

    # Step 2: 生成报告
    print("\n[2/4] 生成舆情报告...")
    try:
        subprocess.run(
            [sys.executable, str(SENTINEL_DIR / "report.py")],
            check=False, cwd=str(PROJECT_ROOT)
        )
    except Exception as e:
        print(f"  [WARN] report.py failed: {e}")

    print("\n[3/4] Agent 待采集 (webfetch)...")
    print("  ⬜ Bing SERP (5条查询)")
    print("  ⬜ X/Twitter API")
    print("  ⬜ LinkedIn 公司页")
    print("  ⬜ Product Hunt")
    print("  ⬜ Reddit 搜索")
    print("  ⬜ 小红书搜索")
    print("  ⬜ YouTube/TikTok/Instagram")

    print("\n[4/4] 产出文件...")
    reports = sorted((PROJECT_ROOT / "1-2 Insight" / "Lovart ORM").glob("Lovart-Sentinel-*.md"))
    if reports:
        print(f"  最新报告: {reports[-1].name}")
    raw_dir = PROJECT_ROOT / "1-2 Insight" / "Lovart ORM" / "raw"
    if raw_dir.exists():
        snapshots = sorted(raw_dir.glob("*"))
        if snapshots:
            print(f"  最新数据快照: {snapshots[-1].name}")

    print("\n" + "=" * 60)
    print("  本地采集完成。")
    print("  请继续使用 webfetch 采集远程数据源，")
    print("  然后重新运行 report.py 生成最终报告。")
    print("=" * 60)


if __name__ == "__main__":
    main()
