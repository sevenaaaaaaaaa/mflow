#!/usr/bin/env python3
"""检测 iCloud 路径是否对当前终端可读可写。"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from path_constants import MONTHLY_DIR, SNAPSHOT_DIR, TRIDENT

CHECKS = [
    ("月报样例", MONTHLY_DIR / "Lovart-SEO-2026-05.md"),
    ("GSC 快照", SNAPSHOT_DIR / "gsc-2026-05.json"),
    ("主脚本", Path(__file__).resolve().parents[1] / "seo_monthly_v2.py"),
    ("盘点输出", TRIDENT / "reports" / "_inventory" / "history-coverage.json"),
]


def probe(label: str, path: Path) -> str:
    if not path.exists():
        return f"❌ {label}: 不存在 {path}"
    ro, wo = os.access(path, os.R_OK), os.access(path, os.W_OK)
    try:
        if path.is_file():
            path.read_bytes()[:1]
            read_ok = True
        else:
            next(path.iterdir(), None)
            read_ok = True
    except OSError as e:
        return f"❌ {label}: 读取失败 ({e})"
    if not read_ok:
        return f"❌ {label}: 读取失败"
    if path.is_file():
        try:
            with path.open("a"):
                pass
            write_ok = True
        except OSError as e:
            return f"⚠️ {label}: 可读不可写 ({e}) [R={ro} W={wo}]"
    else:
        write_ok = os.access(path, os.W_OK)
    status = "✅" if read_ok and (write_ok or path.is_dir()) else "⚠️"
    return f"{status} {label}: R={ro} W={wo} {path}"


def main() -> int:
    print("iCloud / TCC 访问探测\n")
    bad = 0
    for label, path in CHECKS:
        line = probe(label, path)
        print(line)
        if line.startswith("❌"):
            bad += 1
    print()
    if bad:
        print("仍有路径被系统拦截。请在 Finder 对相应文件「立即下载」，")
        print("并在 系统设置 → 隐私与安全性 → 完全磁盘访问权限 中授权 Terminal / Cursor。")
        print("或将仓库移出 iCloud Drive 到本地目录（如 ~/Projects/）。")
        return 1
    print("全部通过，可运行 ./report_batch_runner.sh render-monthly ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
