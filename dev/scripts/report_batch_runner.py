#!/usr/bin/env python3
"""历史 SEO 报告批处理入口（避免 iCloud 锁 scripts/ 导入路径）。"""
from __future__ import annotations

import os
import subprocess
import sys

_HISTORICAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historical")
_RUNNER = os.path.join(_HISTORICAL_DIR, "report_batch_runner.py")
env = os.environ.copy()
env["PYTHONPATH"] = _HISTORICAL_DIR
raise SystemExit(
    subprocess.call(
        [sys.executable, _RUNNER, *sys.argv[1:]],
        cwd=_HISTORICAL_DIR,
        env=env,
    )
)
