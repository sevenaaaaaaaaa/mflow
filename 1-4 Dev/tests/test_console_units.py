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
import time
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


class TestLandingPublisher(unittest.TestCase):
    """T1 落地页：md→版块、结构校验、composite 文档构造。"""

    MD_OK = """---
title: AI Video Generator
slug: ai-video-generator-2026
description: Turn one line into a short video
---
# AI Video Generator

One line to a publish-ready short video.

## Built for teams that ship daily

Teams ship 20 short videos a month; editing costs $300 each, up 42% in 2025.

## Style control without an editor

Pick from 12 styles; average brief to export is 3 minutes.

## FAQ

### Can I use the videos commercially?

Yes — paid plans include commercial rights.
"""

    def setUp(self):
        self.pub = C.SANITY_PUB
        self.assertTrue(self.pub, "sanity_publisher 应已加载")

    def test_md_to_sections_minimal_valid(self):
        secs = self.pub.md_to_sections(self.MD_OK, "AI Video Generator", "One line to short video",
                                       "https://cdn.example.com/a.png", "cover")
        types_ = [x["type"] for x in secs]
        self.assertIn("hero-split", types_)
        self.assertIn("cta-default", types_)
        self.assertTrue(any(t == "feature-detail" for t in types_))
        self.assertEqual(self.pub.validate_sections(secs), [])

    def test_validate_rejects_thin_content(self):
        secs = [{"type": "hero-split", "title": "T", "description": "d", "media": {"src": "u", "alt": "a"}},
                {"type": "cta-default", "title": "c", "description": "d"}]
        errs = self.pub.validate_sections(secs)
        self.assertTrue(any("内容版块不足" in e for e in errs))

    def test_validate_rejects_missing_hero_and_alt(self):
        secs = [{"type": "feature-detail", "title": "t", "description": "d", "items": []},
                {"type": "feature-detail", "title": "t2", "description": "d2", "items": []},
                {"type": "cta-default", "title": "c", "description": "d"}]
        errs = self.pub.validate_sections(secs)
        self.assertTrue(any("hero" in e for e in errs), errs)

    def test_build_composite_doc_shape(self):
        import tempfile, pathlib
        p = pathlib.Path(tempfile.mkdtemp()) / "landing.md"
        p.write_text(self.MD_OK)
        doc = self.pub.build_composite_doc(md_path=str(p), page_type="tool", lang="en")
        self.assertEqual(doc["_type"], "compositePage")
        self.assertEqual(doc["pageType"], "tool")
        self.assertEqual(doc["language"], "en")
        self.assertEqual(doc["schemaVersion"], "composite-v2")
        self.assertIn("bodyJson", doc)
        self.assertGreater(len(__import__("json").loads(doc["bodyJson"])), 2)
        self.assertFalse(self.pub.validate_sections(__import__("json").loads(doc["bodyJson"])))

    def test_build_rejects_bad_page_type(self):
        # page_type 校验先于读文件 → 不应因文件不存在而抛 FileNotFoundError
        with self.assertRaises(RuntimeError) as ctx:
            self.pub.build_composite_doc(md_path="", slug="s", page_type="nonsense")
        self.assertIn("page_type", str(ctx.exception))


class TestChainAndPreset(unittest.TestCase):
    """T1 闭环：任务链只链通过门禁的产出；预设存在且参数正确。"""

    def test_preset_landing_loop_present(self):
        ps = {p["id"]: p for p in C.presets_list()}
        self.assertIn("landing-refresh-publish", ps)
        p = ps["landing-refresh-publish"]
        self.assertEqual(p["type"], "landing_refresh")
        self.assertEqual(p["params"]["chain"]["type"], "publish_sanity")
        self.assertTrue(p["params"]["chain"]["dry_run"], "链式发布必须默认 dry-run")

    def test_chain_skips_blocked_and_publishes_ready(self):
        task = {"id": "t1", "title": "T", "status": "done", "created_by": "tester", "dry_run": True,
                "params": {"chain": {"type": "publish_sanity", "dry_run": True}}, "log": [],
                "items": [
                    {"item_id": "a", "status": "done", "result": {"path": "p/a.md", "slug": "a", "page_type": "tool",
                                                                  "lang": "en", "gates_blocked": [], "struct_errors": []}},
                    {"item_id": "b", "status": "done", "result": {"path": "p/b.md", "slug": "b", "page_type": "tool",
                                                                  "lang": "en", "gates_blocked": ["quota-check.sh"], "struct_errors": []}},
                    {"item_id": "c", "status": "failed", "result": {}},
                ]}
        orig_create, orig_save = C.batch_create, C._batch_log
        created = {}

        def fake_create(btype, title, items, params=None, dry_run=True, by=""):
            created.update({"type": btype, "items": items, "dry_run": dry_run, "by": by})
            return {"id": "batch-x", "stats": {"total": len(items)}}
        C.batch_create = fake_create
        C._batch_log = lambda *a, **k: None
        try:
            nt = C.chain_next_task(task, C.DEFAULT_PROJECT)
        finally:
            C.batch_create, C._batch_log = orig_create, orig_save
        self.assertIsNotNone(nt)
        self.assertEqual(created["type"], "publish_sanity")
        self.assertEqual([i["item_id"] for i in created["items"]], ["a"], "只链通过门禁的项")
        self.assertTrue(created["dry_run"], "链式发布默认 dry-run")
        self.assertEqual(created["items"][0]["mode"], "patch")


class TestPlaybookBranchRetry(unittest.TestCase):
    """剧本分支（前向 goto）+ 步骤级重试/超时。"""

    def _steps(self):
        return [
            {"i": 0, "id": "scan", "name": "扫描", "type": "batch", "status": "done"},
            {"i": 1, "id": "has", "name": "条件", "type": "guard", "status": "pending",
             "expr": "findings>0", "on_true": "next", "on_false": "goto:verify"},
            {"i": 2, "id": "fix", "name": "修复", "type": "batch", "status": "pending"},
            {"i": 3, "id": "verify", "name": "验证", "type": "verify", "status": "pending"},
        ]

    def test_eval_guard(self):
        self.assertTrue(C._eval_guard("findings>0", {"findings": 3}))
        self.assertFalse(C._eval_guard("findings>0", {"findings": 0}))
        self.assertIsNone(C._eval_guard("rm -rf", {}))

    def test_parse_dest(self):
        self.assertEqual(C._parse_dest("continue"), ("next", None))
        self.assertEqual(C._parse_dest("stop"), ("stop", None))
        self.assertEqual(C._parse_dest("goto:verify"), ("goto", "verify"))
        self.assertEqual(C._parse_dest("verify"), ("goto", "verify"))

    def test_branch_false_skips_then(self):
        steps = self._steps()
        ok, detail = C._apply_branch(steps, 1, "goto:verify", "条件不成立")
        self.assertTrue(ok)
        self.assertEqual(steps[2]["status"], "skipped")
        self.assertEqual(steps[3]["status"], "pending")
        self.assertIn("跳到 验证", detail)

    def test_branch_stop_blocks_rest(self):
        steps = self._steps()
        ok, _ = C._apply_branch(steps, 1, "stop", "条件不成立")
        self.assertTrue(ok)
        self.assertEqual(steps[2]["status"], "blocked")
        self.assertEqual(steps[3]["status"], "blocked")

    def test_branch_reject_backjump(self):
        steps = self._steps()
        ok, detail = C._apply_branch(steps, 2, "goto:scan", "")
        self.assertFalse(ok)
        self.assertIn("回跳", detail)
        self.assertEqual(steps[3]["status"], "blocked")

    def test_branch_missing_target(self):
        steps = self._steps()
        ok, detail = C._apply_branch(steps, 1, "goto:nope", "")
        self.assertFalse(ok)
        self.assertIn("不存在", detail)

    def test_join_after_then(self):
        steps = self._steps()
        steps[2]["next"] = "goto:verify"
        steps.append({"i": 4, "id": "else", "name": "无需修复", "type": "note", "status": "pending"})
        # 把 else 插到 verify 前更符合真实 if/else；这里测完成后跳过中间
        steps[2]["status"] = "done"
        ok, _ = C._apply_branch(steps, 2, "goto:verify", "完成后走另一路")
        self.assertTrue(ok)
        self.assertEqual(steps[3]["status"], "pending")

    def test_retry_schedule_and_exhaust(self):
        st = {"status": "failed", "retry_max": 2, "retry_delay_sec": 10, "retries_used": 0}
        self.assertTrue(C._step_can_retry(st))
        C._schedule_step_retry(st)
        self.assertEqual(st["status"], "pending")
        self.assertEqual(st["retries_used"], 1)
        self.assertGreater(st["retry_after"], time.time())
        st["status"] = "failed"
        C._schedule_step_retry(st)
        st["status"] = "failed"
        self.assertFalse(C._step_can_retry(st))

    def test_timeout(self):
        now = time.time()
        st = {"status": "running", "timeout_min": 15, "started_ts": now - 16 * 60}
        self.assertTrue(C._step_timed_out(st, now))
        st["started_ts"] = now - 60
        self.assertFalse(C._step_timed_out(st, now))
        st["timeout_min"] = 0
        st["started_ts"] = now - 9999
        self.assertFalse(C._step_timed_out(st, now))

    def test_normalize_and_validate(self):
        steps = C.playbook_normalize_steps([
            {"name": "A", "type": "preset"},
            {"name": "B", "type": "guard", "on_false": "goto:s3"},
            {"name": "C", "type": "verify"},
        ])
        self.assertEqual([s["id"] for s in steps], ["s1", "s2", "s3"])
        self.assertEqual(C.playbook_validate_jumps(steps), "")
        steps[1]["on_false"] = "goto:ghost"
        self.assertIn("未知目标", C.playbook_validate_jumps(steps))

    def test_preview_skip_names(self):
        steps = C.playbook_normalize_steps([
            {"name": "扫", "id": "scan", "type": "preset"},
            {"name": "条件", "id": "has", "type": "guard", "on_false": "goto:verify"},
            {"name": "修", "id": "fix", "type": "preset"},
            {"name": "验", "id": "verify", "type": "verify"},
        ])
        self.assertEqual(C._preview_skip_names(steps, 1, "goto:verify"), ["修"])
        self.assertEqual(C._preview_skip_names(steps, 1, "stop"), ["修", "验"])


class TestContentEditor(unittest.TestCase):
    """P2-1 正文编辑器：路径白名单 · 版本轮转 · diff。

    安全要点：editable_path 是唯一的写入闸门。它一旦放宽，UI 就能改规则/报告/代码，
    相当于给 RULES 开后门——所以这些用例是护栏，不是覆盖率。
    """

    def _mk(self, rel, text="# t\n\nbody\n"):
        p = C.PROJECTS_DIR / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    # ── 路径白名单 ──
    def test_rejects_non_md(self):
        self.assertIsNone(C.editable_path("run/projects/lovart-global/content/a.json"))

    def test_rejects_traversal(self):
        self.assertIsNone(C.editable_path("run/projects/../../etc/passwd.md"))
        self.assertIsNone(C.editable_path("../outside.md"))

    def test_rejects_rules_and_docs(self):
        # 规则与文档是 SSOT / 由脚本生成，UI 不许改
        self.assertIsNone(C.editable_path("1-1 Harness/02-rules/RULES-00-iron.md"))
        self.assertIsNone(C.editable_path("ROADMAP.md"))
        self.assertIsNone(C.editable_path("docs/warmup.md"))

    def test_accepts_project_content(self):
        p = self._mk("lovart-global/content/demo-edit.md")
        self.assertEqual(C.editable_path(str(p)), p.resolve())

    def test_save_refuses_non_editable(self):
        r = C.content_save("ROADMAP.md", "x", by="t")
        self.assertIn("error", r)
        # 且没有真的去动那个文件
        self.assertNotIn("ok", r)

    # ── 版本轮转 ──
    def test_snapshot_rotation_keeps_n(self):
        p = self._mk("lovart-global/content/rot.md", "v0\n")
        for i in range(C.VERSIONS_KEEP + 4):
            p.write_text(f"v{i}\n", encoding="utf-8")
            C.content_snapshot(p, by="t", note=f"n{i}")
        vs = C.content_versions(p)
        self.assertEqual(len(vs), C.VERSIONS_KEEP)
        self.assertTrue(all(v.get("by") == "t" for v in vs))

    def test_restore_roundtrip(self):
        p = self._mk("lovart-global/content/rt.md", "原始\n")
        ts = C.content_snapshot(p, by="t")
        p.write_text("改坏了\n", encoding="utf-8")
        r = C.content_restore(str(p), ts, by="t")
        self.assertTrue(r.get("ok"), r)
        self.assertEqual(p.read_text(), "原始\n")
        # 恢复前会把「改坏了」也存一版，不丢东西
        self.assertGreaterEqual(len(C.content_versions(p)), 2)

    # ── diff ──
    def test_diff_counts(self):
        d = C.content_diff("a\nb\nc\n", "a\nB\nc\nd\n")
        self.assertTrue(d["changed"])
        self.assertEqual(d["added"], 2)    # B + d
        self.assertEqual(d["removed"], 1)  # b

    def test_diff_identical(self):
        d = C.content_diff("same\ntext\n", "same\ntext\n")
        self.assertFalse(d["changed"])
        self.assertEqual((d["added"], d["removed"]), (0, 0))

    def test_diff_folds_long_unchanged_runs(self):
        old = "\n".join(f"line{i}" for i in range(60))
        new = old + "\nTAIL"
        d = C.content_diff(old, new, ctx=3)
        self.assertTrue(any(r["t"] == "gap" for r in d["rows"]), "长段未改动应折叠为 gap")
        # 折叠后行数远少于原文，否则 diff 视图会被无关内容淹没
        self.assertLess(len([r for r in d["rows"] if r["t"] == "ctx"]), 20)

    # ── 编辑门禁结论 → 发布硬拦 ──
    def test_gate_state_absent_by_default(self):
        """没编辑过的稿子必须没有门禁记录——否则会给存量内容引入回归。"""
        p = self._mk("lovart-global/content/never-edited.md")
        self.assertEqual(C.content_gate_state(p), {})

    def test_gate_state_roundtrip(self):
        p = self._mk("lovart-global/content/gated.md")
        C._ver_dir(p).mkdir(parents=True, exist_ok=True)
        C.write_json(C._ver_dir(p) / "last-gate.json",
                     {"ok": False, "rcs": {"lang-check.sh": 1, "quota-check.sh": 0}})
        g = C.content_gate_state(p)
        self.assertFalse(g.get("ok"))
        self.assertEqual(g["rcs"]["lang-check.sh"], 1)

    def test_diff_empty_side(self):
        d = C.content_diff("", "新建\n")
        self.assertTrue(d["changed"])
        self.assertEqual(d["removed"], 0)


class TestRunDirIsolation(unittest.TestCase):
    """RUN_DIR 隔离——踩过的坑：单测 import console 就往生产 run/approvals.log 写审计噪音。

    错误只犯一次：这条测试保证 MFLOW_RUN_DIR 始终被尊重，
    run-tests.sh 也必须设置它（否则本用例直接失败）。
    """

    def test_env_override_is_honored(self):
        self.assertTrue(
            os.environ.get("MFLOW_RUN_DIR"),
            "run-tests.sh 必须设置 MFLOW_RUN_DIR，否则单测会污染生产 run/",
        )
        self.assertEqual(
            C.RUN_DIR, Path(os.environ["MFLOW_RUN_DIR"]).resolve(),
            "console.RUN_DIR 未跟随 MFLOW_RUN_DIR——审计日志会写回生产目录",
        )

    def test_not_pointing_at_repo_run(self):
        self.assertNotEqual(C.RUN_DIR, ROOT / "run")

    def test_derived_paths_follow(self):
        # TASKS_FILE / PROJECTS_DIR 等派生路径必须一起搬走，否则隔离只做了一半
        self.assertTrue(str(C.TASKS_FILE).startswith(str(C.RUN_DIR)))
        self.assertTrue(str(C.PROJECTS_DIR).startswith(str(C.RUN_DIR)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
