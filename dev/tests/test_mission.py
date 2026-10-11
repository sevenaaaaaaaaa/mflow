#!/usr/bin/env python3
"""任务全景（mission.py）单元测试：离线、只用临时 RUN_DIR 里的合成数据。

运行：bash "dev/scripts/run-tests.sh"（会强制 MFLOW_RUN_DIR 指向临时目录）
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
CONSOLE = ROOT / "dev" / "console" / "console.py"

if not os.environ.get("MFLOW_RUN_DIR"):  # 单独运行时也绝不碰生产 run/
    os.environ["MFLOW_RUN_DIR"] = tempfile.mkdtemp(prefix="mflow-mission-test-")


def _load_console():
    if "markdown" not in sys.modules:
        stub = types.ModuleType("markdown")
        stub.markdown = lambda *a, **k: ""
        sys.modules["markdown"] = stub
    spec = importlib.util.spec_from_file_location("mflow_console_mission_test", CONSOLE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _load_console()
M = C.MISSION
G = vars(C)


def _w(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False))


class MissionBase(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(M, "mission.py 未加载")
        self.saved = {k: G[k] for k in ("RUN_DIR", "BATCH_DIR", "RUNS_DIR", "PROJECTS_DIR")}
        self.tmp = Path(tempfile.mkdtemp(prefix="mflow-mission-"))
        G["RUN_DIR"] = self.tmp
        G["BATCH_DIR"] = self.tmp / "batch"
        G["RUNS_DIR"] = self.tmp / "runs"
        G["PROJECTS_DIR"] = self.tmp / "projects"
        M._TRAFFIC_CACHE.update(key=None, data=None)

    def tearDown(self):
        G.update(self.saved)
        M._TRAFFIC_CACHE.update(key=None, data=None)

    def batch(self, tid, **kw):
        t = {"id": tid, "type": "field_patch", "title": "测试批量", "status": "done", "dry_run": False,
             "created": "2026-10-10 10:00", "started": "2026-10-10 10:00", "finished": "2026-10-10 10:10",
             "created_by": "seven", "stats": {"total": 2, "done": 2, "failed": 0, "skipped": 0},
             "items": [{"i": 0, "status": "done", "title": "页 A",
                        "result": {"url": "https://test.example/a/", "hook_rc": 0}},
                       {"i": 1, "status": "done", "title": "页 B",
                        "result": {"url": "https://test.example/b", "hook_rc": 1}}]}
        t.update(kw)
        _w(G["BATCH_DIR"] / f"{tid}.json", t)
        return t


class TestMissionBuild(MissionBase):
    def test_empty_is_safe(self):
        d = M.build(G, "main")
        self.assertEqual(d["cards"], [])
        self.assertEqual(len(d["chain"]), 6)
        self.assertTrue(d["notes"])
        for k in ("running", "queued", "failed", "waiting", "outputs"):
            self.assertIn(k, d["kpi"])

    def test_batch_card_answers_seven_questions(self):
        self.batch("batch-1")
        c = M.build(G, "main")["cards"][0]
        for k in ("why", "what", "progress", "timing", "benefit", "outputs", "qa", "traffic"):
            self.assertIn(k, c)
        self.assertEqual(c["status"], "done")
        self.assertIn("seven", c["why"]["trigger"])
        self.assertTrue(c["why"]["reason"])          # 拿不到具体原因时用类型兜底
        self.assertEqual(c["qa"]["pass"], 1)
        self.assertEqual(c["qa"]["fail"], 1)
        self.assertEqual(c["outputs"][0]["state"], "已上线/已写库")

    def test_dry_run_done_means_waiting_for_approval(self):
        self.batch("batch-dry", dry_run=True)
        c = M.build(G, "main")["cards"][0]
        self.assertEqual(c["status"], "waiting")
        self.assertIn("待授权", c["status_text"])
        self.assertTrue(c["benefit"]["note"])
        self.assertIn("预演", c["traffic"]["line"])

    def test_run_absorbs_child_batch_and_keeps_user_message(self):
        self.batch("batch-child")
        _w(G["RUNS_DIR"] / "run-x.json",
           {"id": "run-x", "title": "补 SEO 字段", "status": "done", "kind": "agent", "by": "seven",
            "message": "60 篇缺 seoTitle，补齐", "created": "2026-10-10 10:00:00", "started_ts": time.time() - 600,
            "steps": [{"i": 0, "name": "补字段", "type": "batch", "status": "done", "task_id": "batch-child"}]})
        cards = M.build(G, "main")["cards"]
        self.assertEqual([c["id"] for c in cards], ["run-x"])   # 子批量不重复出卡
        self.assertEqual(cards[0]["why"]["reason"], "60 篇缺 seoTitle，补齐")
        self.assertEqual(cards[0]["outputs_total"], 2)

    def test_running_batch_has_eta_and_sorts_first(self):
        self.batch("batch-old")
        self.batch("batch-run", status="running", finished=None,
                   started=time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() - 120)),
                   stats={"total": 10, "done": 2, "failed": 0, "skipped": 0})
        cards = M.build(G, "main")["cards"]
        self.assertEqual(cards[0]["id"], "batch-run")
        self.assertIsNotNone(cards[0]["timing"]["eta_sec"])
        self.assertGreater(cards[0]["timing"]["eta_sec"], 0)

    def test_loop_card_has_draft_and_gates(self):
        _w(G["PROJECTS_DIR"] / "main" / "loops.json",
           [{"id": "lp1", "goal": "写一篇召回文", "brief": "来自旅程断点信号", "status": "done", "round": 1,
             "max_rounds": 3, "created": "2026-10-10 10:00", "log": ["[10:00:30] Loop 完成"],
             "last_hook_rc": 0, "last_geo_rc": 0, "draft_path": "run/projects/main/content/x.md"}])
        c = M.build(G, "main")["cards"][0]
        self.assertEqual(c["kind"], "loop")
        self.assertEqual(c["why"]["reason"], "来自旅程断点信号")
        self.assertEqual(c["outputs"][0]["qa"], "pass")
        self.assertEqual(c["timing"]["elapsed_sec"], 30)

    def test_traffic_matched_by_path_not_exact_string(self):
        _w(self.tmp / "local-dev/Output/Data Ingestion/gsc-5k-2026-09.json",
           {"pages": [{"url": "https://www.test.example/a", "clicks": 42, "impr": 900, "ctr": 4.7, "pos": 6.1}]})
        self.batch("batch-t")
        c = M.build(G, "main")["cards"][0]
        a = next(o for o in c["outputs"] if o["url"].endswith("/a/"))
        b = next(o for o in c["outputs"] if o["url"].endswith("/b"))
        self.assertEqual(a["traffic"]["clicks"], 42)   # www / 尾斜杠差异仍能匹配
        self.assertIsNone(b["traffic"])                 # 不在快照 = 暂无，而不是 0
        self.assertEqual(c["traffic"]["matched"], 1)

    def test_corrupt_files_do_not_break_page(self):
        (G["RUNS_DIR"]).mkdir(parents=True, exist_ok=True)
        (G["RUNS_DIR"] / "run-bad.json").write_text("{not json")
        _w(G["RUNS_DIR"] / "run-weird.json", {"id": "run-weird", "steps": "oops"})
        self.batch("batch-ok")
        ids = [c["id"] for c in M.build(G, "main")["cards"]]
        self.assertIn("batch-ok", ids)

    def test_build_has_no_side_effects(self):
        self.batch("batch-ro")
        before = sorted(str(p) for p in self.tmp.rglob("*"))
        M.build(G, "main")
        self.assertEqual(before, sorted(str(p) for p in self.tmp.rglob("*")))

    def test_csv_export(self):
        self.batch("batch-csv")
        s = M.outputs_csv(M.build(G, "main"))
        self.assertTrue(s.startswith("﻿标题,URL"))
        self.assertIn("https://test.example/a/", s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
