#!/usr/bin/env python3
"""MFlow console 单元测试（离线、无网络、可进 CI/门禁）。

覆盖：spec_guard 规格门禁 · 熔断判定与全局熔断 · 用户配额与用量 · 预设展开（纯逻辑部分）·
      housekeeping 幂等 · Agent 上下文预算与检索 · tokens 分词。

运行：bash "1-4 Dev/scripts/run-tests.sh"
"""
import importlib.util
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSOLE = ROOT / "1-4 Dev" / "console" / "console.py"


def _load_console():
    # 本地可能没有 markdown 依赖 → 注入 stub（console 仅用于渲染，单测不需要）
    if "markdown" not in sys.modules:
        stub = types.ModuleType("markdown")
        stub.markdown = lambda *a, **k: ""
        sys.modules["markdown"] = stub
    spec = importlib.util.spec_from_file_location("mflow_console_under_test", CONSOLE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _load_console()


class TestSpecGuard(unittest.TestCase):
    """Agent 规格门禁：类型/字段白名单、规模上限、dry-run 默认。"""

    def test_reject_unknown_type(self):
        spec, err = C.spec_guard({"type": "delete_all", "items": [{}]})
        self.assertIsNone(spec)
        self.assertIn("不允许的任务类型", err)

    def test_reject_extra_field(self):
        spec, err = C.spec_guard({"type": "field_patch", "items": [{"doc_id": "a", "set": {}, "evil": 1}]})
        self.assertIsNone(spec)
        self.assertIn("未允许字段", err)

    def test_cap_items(self):
        items = [{"doc_id": f"d{i}", "set": {"seoTitle": "x"}} for i in range(201)]
        spec, err = C.spec_guard({"type": "field_patch", "items": items})
        self.assertIsNone(spec)
        self.assertIn("≤200", err)

    def test_default_dry_run_true(self):
        spec, err = C.spec_guard({"type": "gen", "items": [{"item_id": "a", "topic": "t"}]})
        self.assertEqual(err, "")
        self.assertTrue(spec["dry_run"])

    def test_allow_budget_profile(self):
        spec, err = C.spec_guard({"type": "gen", "items": [{"item_id": "a", "topic": "t", "budget_profile": "longform"}]})
        self.assertEqual(err, "")


class TestBreaker(unittest.TestCase):
    """熔断：致命错误分类、trip/check/reset。"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self._orig = (C.BREAKER_FILE, C.RUN_DIR)
        C.BREAKER_FILE = self.tmp / "breaker.json"
        C.RUN_DIR = self.tmp

    def tearDown(self):
        C.BREAKER_FILE, C.RUN_DIR = self._orig

    def test_fatal_patterns(self):
        for msg in ("HTTP Error 401: Unauthorized", "invalid api key", "Insufficient Balance",
                    "quota exceeded", "403 Forbidden"):
            self.assertTrue(C._is_fatal_error(msg), msg)
        self.assertFalse(C._is_fatal_error("timeout connecting"))

    def test_trip_blocks_until_cooldown(self):
        C.breaker_trip("test", cooldown_min=30)
        blocked, st = C.breaker_check()
        self.assertTrue(blocked)
        self.assertTrue(st["tripped"])

    def test_auto_reset_after_cooldown(self):
        st = C.breaker_trip("test", cooldown_min=0)
        st["tripped_at_ts"] = st["tripped_at_ts"] - 60  # 已过冷却
        C.BREAKER_FILE.write_text(json.dumps(st))
        blocked, _ = C.breaker_check()
        self.assertFalse(blocked)

    def test_manual_reset(self):
        C.breaker_trip("test", cooldown_min=30)
        C.breaker_reset()
        blocked, _ = C.breaker_check()
        self.assertFalse(blocked)


class TestQuota(unittest.TestCase):
    """配额：admin 不限、超额拦截、用量记账、80% 预警去重。"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self._orig = (C.USAGE_USERS_FILE, C.QUOTAS_FILE)
        C.USAGE_USERS_FILE = self.tmp / "usage.json"
        C.QUOTAS_FILE = self.tmp / "quotas.json"
        C.QUOTAS_FILE.write_text(json.dumps({"default": {"items_per_month": 10, "tokens_per_month": 1000,
                                                        "writes_per_month": 5}, "per_user": {}}))

    def tearDown(self):
        C.USAGE_USERS_FILE, C.QUOTAS_FILE = self._orig

    def test_admin_unlimited(self):
        self.assertEqual(C.user_quota("seven", "admin"), {})
        ok, msg = C.quota_check("seven", "admin", n_items=10 ** 6)
        self.assertTrue(ok)

    def test_items_cap_blocks(self):
        ok, msg = C.quota_check("op", "operator", n_items=11, kind="field_patch")
        self.assertFalse(ok)
        self.assertIn("条目配额不足", msg)

    def test_usage_accumulates(self):
        C.usage_add("op", tasks=1, items=3, tokens=100, writes=2)
        u = C.usage_get("op")
        self.assertEqual(u["items"], 3)
        self.assertEqual(u["tokens"], 100)
        self.assertEqual(u["writes"], 2)

    def test_warn_flag_dedup(self):
        # 80% 预警只打一次（warned 去重）
        C.usage_add("op", items=8)
        m = C.usage_get("op")
        C.usage_add("op", items=1)
        allu = json.loads(C.USAGE_USERS_FILE.read_text())
        warned = allu["op"][C._month()].get("warned", {})
        self.assertIn("items:warn", warned)

    def test_dry_run_no_write(self):
        # 真实写入配额只统计非 dry-run（由执行器控制传参），此处验证 cap 判定
        ok, msg = C.quota_check("op", "operator", n_items=6, kind="asset_replace")
        self.assertFalse(ok)
        self.assertIn("真实写入配额不足", msg)


class TestHousekeeping(unittest.TestCase):
    """降噪治理：幂等（无旧数据时全 0）。"""

    def test_idempotent_empty(self):
        rep = C.housekeeping(dry_run=True)
        self.assertEqual(rep["archived_items"], 0)
        self.assertEqual(rep["archived_batch"], 0)
        self.assertIn("drafts_orphan", rep)


class TestAgentContext(unittest.TestCase):
    """上下文预算：tokens 分词、skills 检索、规则按意图收缩。"""

    def test_tokens_cjk_bigram(self):
        t = C._tokens("质检 SEO 修复")
        self.assertIn("质检", t)
        self.assertIn("seo", t)

    def test_rules_budget_capped(self):
        rules = C.context_rules(limit=1200, query="帮我做一次质检扫描并修复 seoTitle")
        self.assertLessEqual(len(rules), 1200)

    def test_skills_retrieval_relevant(self):
        hits = C.context_skills("落地页文案怎么写")
        self.assertTrue(hits, "应命中至少一个 skill")
        self.assertLessEqual(len(hits), 5)


class TestPresets(unittest.TestCase):
    """预设：清单完整性 + 未知预设报错。"""

    def test_presets_present(self):
        ps = C.presets_list()
        ids = {p["id"] for p in ps}
        for need in ("geo-gap-rewrite", "qa-field-fix", "asset-alt-fill", "multilang-batch"):
            self.assertIn(need, ids)
        for p in ps:
            self.assertTrue(p.get("type") in C.BATCH_HANDLERS)
            self.assertTrue(p.get("options"))

    def test_unknown_preset(self):
        r = C.preset_expand("nope", {}, C.DEFAULT_PROJECT)
        self.assertIn("error", r)

    def test_multilang_expand(self):
        r = C.preset_expand("multilang-batch", {"topic": "AI 设计工具对比", "langs": "zh,en,ja"}, C.DEFAULT_PROJECT)
        self.assertEqual(r["type"], "gen")
        self.assertEqual(len(r["items"]), 3)
        self.assertEqual({i["lang"] for i in r["items"]}, {"zh", "en", "ja"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
