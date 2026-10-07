#!/usr/bin/env python3
"""稳定性 P0 单测（offline）：熔断 kill switch / 全局每日运行上限 / 分段 patch 计划 / loop token 预算。

背景（docs/CONTENT-SYSTEM-GUIDE.md §六 P0）：
- playbook runaway 事故（2026-09-20）→ 四个自动化触发器必须接全局熔断
- b20 hang（200+ block 整包 patch）→ 分段事务
运行：bash "1-4 Dev/scripts/run-tests.sh"
"""
import importlib.util
import json
import sys
import time
import types
import unittest
from pathlib import Path

import os

ROOT = Path(__file__).resolve().parents[2]
CONSOLE = ROOT / "1-4 Dev" / "console" / "console.py"
PUB = ROOT / "1-4 Dev" / "scripts" / "publish_adapters" / "sanity_publisher.py"


def _load(modpath, modname):
    spec = importlib.util.spec_from_file_location(modpath, modname)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _load_console():
    if "markdown" not in sys.modules:
        stub = types.ModuleType("markdown")
        stub.markdown = lambda *a, **k: ""
        sys.modules["markdown"] = stub
    return _load("mflow_console_stability", CONSOLE)


C = _load_console()


def _blocks(n):
    return [{"_type": "block", "_key": f"k{i}", "children": [{"_type": "span", "text": f"t{i}"}],
             "markDefs": [], "style": "normal"} for i in range(n)]


class TestBreakerKillSwitch(unittest.TestCase):
    """cooldown_min<=0 = 人工熔断：不自动复位（强制冷却期过后也保持）。"""

    def _trip(self, cooldown):
        st = C.breaker_trip("test", cooldown_min=cooldown)
        self.addCleanup(C.breaker_reset)
        return st

    def test_manual_never_auto_resets(self):
        self._trip(0)
        time.sleep(0.1)
        blocked, st = C.breaker_check()
        self.assertTrue(blocked)
        self.assertEqual(float(st.get("cooldown_min", 15)), 0)
        # 再过冷却逻辑时间（人为推后 ts）仍不复位
        C.BREAKER_FILE.write_text(json.dumps({**C.breaker_state(), "tripped_at_ts": time.time() - 10_000}))
        blocked, st = C.breaker_check()
        self.assertTrue(blocked, "cooldown_min=0 必须等人工 reset")

    def test_auto_resets_after_cooldown(self):
        self._trip(1)
        st = C.breaker_state()
        C.BREAKER_FILE.write_text(json.dumps({**st, "tripped_at_ts": time.time() - 3600}))
        blocked, _ = C.breaker_check()
        self.assertFalse(blocked, "cooldown>0 到期应自动复位")


class TestGlobalRunCap(unittest.TestCase):
    """全局每日运行总上限：跨剧本聚合计数 + 可通过 run/limits.json 调整。"""

    def test_sum_counts_all_playbooks_today(self):
        today = time.strftime("%Y-%m-%d")
        pbs = [{"id": "a", "day": today, "runs_today": 5},
               {"id": "b", "day": today, "runs_today": 3},
               {"id": "c", "day": "2000-01-01", "runs_today": 999},  # 非当日不计
               {"id": "d", "runs_today": 7}]                          # 无 day 字段不计（当天缺省行为）
        self.assertEqual(C._global_runs_today(pbs), 8)

    def test_limits_config_override(self):
        f = Path(C.GLOBAL_LIMITS_FILE)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps({"max_runs_per_day": 1}))
        self.addCleanup(f.unlink)
        self.assertEqual(C._global_limits()["max_runs_per_day"], 1)

    def test_blocks_when_cap_reached(self):
        today = time.strftime("%Y-%m-%d")
        f = Path(C.GLOBAL_LIMITS_FILE)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps({"max_runs_per_day": 2}))
        self.addCleanup(f.unlink)
        pb = {"id": "x", "name": "t", "steps": [{"type": "preset", "preset": "qa-scan"}],
              "day": today, "runs_today": 0}
        others = [{"id": "a", "day": today, "runs_today": 2}]
        ok, reason = C.playbook_limits_check({**pb, "limits": {}}) if False else (None, None)
        # 直接注入 playbooks_list 的返回（monkeypatch）
        orig = C.playbooks_list
        C.playbooks_list = lambda: others
        try:
            ok, reason = C.playbook_limits_check(pb)
        finally:
            C.playbooks_list = orig
        self.assertFalse(ok)
        self.assertIn("全局每日运行已达上限", reason)


class TestBodyChunking(unittest.TestCase):
    """b20 分段 patch 计划（纯函数）。"""

    def setUp(self):
        self.P = _load("mflow_pub_stability", PUB)

    def test_short_body_single_set(self):
        ch = self.P.split_body_chunks(_blocks(10))
        self.assertEqual(len(ch), 1)
        self.assertEqual(ch[0][0], "set_prefix")

    def test_long_body_set_then_inserts(self):
        ch = self.P.split_body_chunks(_blocks(95), chunk=40)
        self.assertEqual([k for k, _ in ch], ["set_prefix", "insert", "insert"])
        self.assertLessEqual(len(ch[0][1]), 40)
        self.assertEqual(sum(len(b) for _, b in ch), 95)

    def test_mutations_shape(self):
        ch = self.P.split_body_chunks(_blocks(85), chunk=40)
        muts = self.P._patch_mutations_for_patches(ch, "doc-1")
        self.assertEqual(muts[0]["patch"]["set"]["body"], ch[0][1])
        self.assertEqual(muts[1]["patch"]["insert"]["after"], "body[-1]")
        self.assertNotIn("ifRevisionID", muts[1]["patch"])
        self.assertEqual(len(muts[2]["patch"]["insert"]["items"]), 5)

    def test_empty_body(self):
        self.assertEqual(self.P.split_body_chunks([]), [])


class TestLoopTokenCap(unittest.TestCase):
    """loop token 预算超限 → blocked（人工接管），不让烧钱循环继续。"""

    def test_cap_from_env_consistent(self):
        self.assertGreater(C.LOOP_TOKEN_CAP, 0)


class TestDryRunSkipsLLM(unittest.TestCase):
    """gen/rewrite 的 dry_run = 预演不烧 LLM（token 质检 2026-10-07）。"""

    def test_gen_dry_run_skipped(self):
        r = C._bh_gen({"item_id": "x"}, {"dry_run": True}, "main")
        self.assertTrue(r.get("skipped"))
        self.assertIn("dry-run", r.get("reason", ""))

    def test_rewrite_dry_run_skipped(self):
        r = C._bh_rewrite({"item_id": "x"}, {"dry_run": True}, "main")
        self.assertTrue(r.get("skipped"))


if __name__ == "__main__":
    unittest.main()
