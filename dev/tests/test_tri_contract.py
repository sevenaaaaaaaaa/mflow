#!/usr/bin/env python3
"""三方契约 v1.1（InFlow × OpenFlow × MFlow）MFlow 侧单测（离线、无外网）。

覆盖：/api/item/upsert 来源字段落盘 + ok/id · advance 的 item_id 别名 · loop 记录 insight_id/source ·
      机器 token 写白名单（MFLOW_MACHINE_WRITE）· emit_to_insightflow 信封/签名/重试/死信 ·
      发布成功 → publish 回执 + 推进到 S5-published + 回流。

运行：bash "dev/scripts/run-tests.sh"（或直接 python3 本文件，会自动使用临时 MFLOW_RUN_DIR）
"""
import hashlib
import hmac
import http.server
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import threading
import types
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSOLE = ROOT / "dev" / "console" / "console.py"
_OWN_RUN = None
if not os.environ.get("MFLOW_RUN_DIR"):  # 直接运行时也绝不写生产 run/
    _OWN_RUN = tempfile.mkdtemp(prefix="mflow-tri-run.")
    os.environ["MFLOW_RUN_DIR"] = _OWN_RUN


def _load_console():
    if "markdown" not in sys.modules:
        stub = types.ModuleType("markdown")
        stub.markdown = lambda *a, **k: ""
        sys.modules["markdown"] = stub
    spec = importlib.util.spec_from_file_location("mflow_console_tri", CONSOLE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _load_console()


class _Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="mflow-tri."))
        self._saved = {k: getattr(C, k) for k in ("PROJECTS_DIR", "RUN_DIR", "WEBHOOK_LOG",
                                                  "INSFLOW_OUTBOX_FAILED", "_IF_BACKOFF", "API_TOKEN",
                                                  "emit_to_insightflow", "webhook_emit")}
        C.PROJECTS_DIR = self.tmp / "projects"
        C.RUN_DIR = self.tmp
        C.WEBHOOK_LOG = self.tmp / "webhooks.log"
        C.INSFLOW_OUTBOX_FAILED = self.tmp / "insightflow-outbox-failed.jsonl"
        C._IF_BACKOFF = (0, 0)
        self.proj = "main"
        (C.PROJECTS_DIR / self.proj).mkdir(parents=True)
        self._env = {k: os.environ.get(k) for k in ("INSFLOW_INGEST_URL", "INSFLOW_INGEST_SECRET",
                                                     "MFLOW_MACHINE_WRITE")}
        for k in self._env:
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._saved.items():
            setattr(C, k, v)
        for k, v in self._env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.tmp, ignore_errors=True)

    def item(self, iid):
        st = json.loads(C.proj_paths(self.proj)["state"].read_text())
        return st["items"].get(iid)


class TestItemAndLoopApi(_Base):
    def test_upsert_persists_origin_fields(self):
        code, r = C.api_item_upsert(self.proj, {
            "id": "if-ins-42-abc123", "category": "blog", "target_type": "blog",
            "topic": "AI 海报", "brief": "-以连字符开头的 brief", "source": "insightflow",
            "insight_id": "ins_42", "evidence": [{"k": "gsc", "v": 1}, "ref-2"],
            "keyword": "ai poster", "target_url": "https://x.test/p"})
        self.assertEqual(code, 200, r)
        self.assertTrue(r["ok"])
        self.assertEqual(r["id"], "if-ins-42-abc123")
        self.assertEqual(r["rc"], 0)
        self.assertIn("out", r)
        o = self.item("if-ins-42-abc123")["origin"]
        self.assertEqual(o["insight_id"], "ins_42")
        self.assertEqual(o["brief"], "-以连字符开头的 brief")
        self.assertEqual(o["evidence"], [{"k": "gsc", "v": 1}, "ref-2"])
        self.assertEqual(o["target_url"], "https://x.test/p")
        # 再次 upsert 只合并提供的字段，不抹掉已有来源
        C.api_item_upsert(self.proj, {"id": "if-ins-42-abc123", "evidence": "plain text"})
        o = self.item("if-ins-42-abc123")["origin"]
        self.assertEqual(o["evidence"], ["plain text"])
        self.assertEqual(o["keyword"], "ai poster")

    def test_upsert_rejects_bad_id(self):
        code, r = C.api_item_upsert(self.proj, {"id": "Bad_ID"})
        self.assertEqual(code, 400)
        self.assertFalse(r["ok"])
        self.assertEqual(r["id"], "Bad_ID")

    def test_upsert_legacy_item_without_origin(self):
        code, r = C.api_item_upsert(self.proj, {"id": "legacy-item"})
        self.assertTrue(r["ok"])
        self.assertNotIn("origin", self.item("legacy-item"))

    def test_advance_item_id_alias(self):
        C.api_item_upsert(self.proj, {"id": "adv-item"})
        code, r = C.api_item_advance(self.proj, {"item_id": "adv-item", "to": "S3-creating"})
        self.assertEqual(code, 200, r)
        self.assertTrue(r["ok"])
        self.assertEqual(r["id"], "adv-item")
        self.assertEqual(self.item("adv-item")["stage"], "S3-creating")
        code, r = C.api_item_advance(self.proj, {"id": "adv-item", "to": "done"})  # 非法转移
        self.assertEqual(code, 400)
        self.assertFalse(r["ok"])
        self.assertNotEqual(r["rc"], 0)

    def test_loop_create_persists_insight(self):
        code, r = C.api_loop_create(self.proj, {"item_id": "loop-item", "topic": "t", "goal": "g",
                                                "insight_id": "ins_7", "source": "insightflow"})
        self.assertEqual(code, 200, r)
        self.assertTrue(r["ok"])
        self.assertEqual(r["loop_id"], r["id"])
        loops = json.loads(C.proj_paths(self.proj)["loops"].read_text())
        lp = next(x for x in loops if x["id"] == r["loop_id"])
        self.assertEqual((lp["insight_id"], lp["source"], lp["goal"]), ("ins_7", "insightflow", "g"))
        self.assertEqual(self.item("loop-item")["origin"]["insight_id"], "ins_7")
        code, r = C.api_loop_create(self.proj, {"topic": "no item"})
        self.assertEqual(code, 400)
        self.assertFalse(r["ok"])


class TestMachineWrite(_Base):
    def setUp(self):
        super().setUp()
        C.API_TOKEN = "machine-tok"
        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), C.Handler)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.srv.server_address[1]}"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()
        super().tearDown()

    def post(self, path, body, token="machine-tok"):
        req = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", "X-MFlow-Token": token})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}")

    def test_default_read_only(self):
        code, _ = self.post("/api/item/upsert", {"id": "mw-item"})
        self.assertEqual(code, 403)

    def test_allowlist_when_enabled(self):
        os.environ["MFLOW_MACHINE_WRITE"] = "1"
        code, r = self.post("/api/item/upsert", {"id": "mw-item", "insight_id": "ins_1"})
        self.assertEqual(code, 200, r)
        self.assertTrue(r["ok"])
        code, r = self.post("/api/loop/create", {"item_id": "mw-item", "insight_id": "ins_1"})
        self.assertEqual(code, 200, r)
        self.assertTrue(r["loop_id"])
        code, r = self.post("/api/item/advance", {"item_id": "mw-item", "to": "S0-skip"})
        self.assertEqual(code, 200, r)
        # 白名单外的写接口仍 403；错 token 不放行
        code, _ = self.post("/api/tasks/del", {"id": "x"})
        self.assertEqual(code, 403)
        code, _ = self.post("/api/item/upsert", {"id": "mw-item2"}, token="wrong")
        self.assertIn(code, (401, 403))
        self.assertIsNone(self.item("mw-item2"))


class _Capture(http.server.BaseHTTPRequestHandler):
    hits = []
    fail_times = 0

    def log_message(self, *a):
        pass

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        _Capture.hits.append({"raw": raw, "headers": {k.lower(): v for k, v in self.headers.items()}})
        code = 500 if len(_Capture.hits) <= _Capture.fail_times else 200
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}')


class TestEmitAndPublish(_Base):
    def setUp(self):
        super().setUp()
        _Capture.hits, _Capture.fail_times = [], 0
        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Capture)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        os.environ["INSFLOW_INGEST_URL"] = f"http://127.0.0.1:{self.srv.server_address[1]}/api/v1/ingest"
        os.environ["INSFLOW_INGEST_SECRET"] = "s3cret"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()
        super().tearDown()

    def test_disabled_without_env(self):
        os.environ.pop("INSFLOW_INGEST_URL")
        self.assertIsNone(C.emit_to_insightflow("content.published", {"item_id": "a"}, sync=True))
        self.assertEqual(_Capture.hits, [])

    def test_envelope_and_signature(self):
        ok = C.emit_to_insightflow("content.published", {"item_id": "pub-item", "url": "u"},
                                   epoch=1760256000, sync=True)
        self.assertTrue(ok)
        h = _Capture.hits[0]
        env = json.loads(h["raw"])
        self.assertEqual(env["schema_version"], "1.1")
        self.assertEqual(env["event"], "content.published")
        self.assertEqual(env["event_id"], "mflow-pub-pub-item-1760256000")
        self.assertEqual(env["occurred_at"], "2025-10-12T08:00:00Z")
        self.assertEqual(env["source"], "mflow")
        self.assertEqual(env["data"]["item_id"], "pub-item")
        want = hmac.new(b"s3cret", h["raw"], hashlib.sha256).hexdigest()
        self.assertEqual(h["headers"]["x-if-signature"], want)
        self.assertTrue(h["headers"]["x-if-timestamp"].isdigit())

    def test_retry_keeps_event_id_then_dead_letter(self):
        _Capture.fail_times = 2
        self.assertTrue(C.emit_to_insightflow("content.failed", {"item_id": "r-item"}, epoch=1, sync=True))
        ids = {json.loads(h["raw"])["event_id"] for h in _Capture.hits}
        self.assertEqual(len(_Capture.hits), 3)
        self.assertEqual(ids, {"mflow-fail-r-item-1"})
        _Capture.hits, _Capture.fail_times = [], 99
        self.assertFalse(C.emit_to_insightflow("content.failed", {"item_id": "r-item"}, epoch=2, sync=True))
        self.assertEqual(len(_Capture.hits), 3)
        dl = [json.loads(x) for x in C.INSFLOW_OUTBOX_FAILED.read_text().splitlines()]
        self.assertEqual(dl[-1]["envelope"]["event_id"], "mflow-fail-r-item-2")

    def _ready_item(self, iid, stage_path):
        C.api_item_upsert(self.proj, {"id": iid, "insight_id": "ins_9", "topic": "Topic 9"})
        for st in stage_path:
            code, r = C.api_item_advance(self.proj, {"id": iid, "to": st})
            self.assertEqual(code, 200, r)

    def test_publish_success_advances_and_emits(self):
        sent = []
        C.emit_to_insightflow = lambda ev, data, epoch=None, sync=False: sent.append((ev, data, epoch))
        C.webhook_emit = lambda ev, data: sent.append(("webhook:" + ev, data, None))
        self._ready_item("pub-item", ["S3-creating", "S3-draft", "S3-done", "S4-qa"])
        lid = C.api_loop_create(self.proj, {"item_id": "pub-item"})[1]["loop_id"]
        out = C.publish_record_success(self.proj, "pub-item", "sanity", external_id="blog-zh-x",
                                       url="https://www.lovart.ai/x", title="T", actor="tester")
        self.assertEqual(out["advanced"], ["S4-ready", "S5-importing", "S5-published"], out)
        it = self.item("pub-item")
        self.assertEqual(it["stage"], "S5-published")
        pub = it["publish"]
        self.assertEqual((pub["url"], pub["target"], pub["external_id"], pub["sanity_id"]),
                         ("https://www.lovart.ai/x", "sanity", "blog-zh-x", "blog-zh-x"))
        self.assertTrue(pub["imported_at"].endswith("Z"))
        evs = [e for e in sent if e[0] == "content.published"]
        self.assertEqual(len(evs), 1)
        d = evs[0][1]
        self.assertEqual((d["item_id"], d["loop_id"], d["insight_id"], d["target"]),
                         ("pub-item", lid, "ins_9", "sanity"))
        self.assertIn("webhook:content.published", [e[0] for e in sent])

    def test_publish_from_s5_importing_and_untracked(self):
        C.emit_to_insightflow = lambda *a, **k: None
        C.webhook_emit = lambda *a, **k: 0
        self._ready_item("imp-item", ["S3-creating", "S3-draft", "S3-done", "S4-qa", "S4-ready", "S5-importing"])
        out = C.publish_record_success(self.proj, "imp-item", "wordpress", external_id="77", url="https://wp/x")
        self.assertEqual(out["advanced"], ["S5-published"])
        self.assertEqual(self.item("imp-item")["publish"]["external_id"], "77")
        self.assertFalse(C.publish_record_success(self.proj, "not-in-pipeline", "sanity")["tracked"])

    def test_publish_failure_emits(self):
        sent = []
        C.emit_to_insightflow = lambda ev, data, epoch=None, sync=False: sent.append((ev, data))
        C.webhook_emit = lambda *a, **k: 0
        self._ready_item("fail-item", ["S3-creating"])
        self.assertTrue(C.publish_record_failure(self.proj, "fail-item", "sanity", "HTTP 500"))
        ev, d = sent[0]
        self.assertEqual(ev, "content.failed")
        self.assertEqual((d["item_id"], d["stage"], d["error"], d["insight_id"]),
                         ("fail-item", "S3-creating", "HTTP 500", "ins_9"))
        self.assertEqual(self.item("fail-item")["stage"], "S3-creating")


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        if _OWN_RUN:
            shutil.rmtree(_OWN_RUN, ignore_errors=True)
