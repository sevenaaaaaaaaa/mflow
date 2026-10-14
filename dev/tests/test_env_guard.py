#!/usr/bin/env python3
"""env_guard 单元测试（离线）：环境判定 / 写入守卫 / 传输层拦截。

每个用例都显式设置 MFLOW_ENV，结果与运行平台无关（Mac 开发机与 Linux 服务器上同样通过）。
运行：bash "dev/scripts/run-tests.sh"
"""
import http.client
import io
import json
import os
import smtplib
import subprocess
import sys
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "dev" / "scripts" / "library"
sys.path.insert(0, str(LIB))
import env_guard as G  # noqa: E402

G.install(force=True)  # patches are inert unless env() == development without opt-in

CLEAN = {"MFLOW_ENV": "", "APP_ENV": "", "MFLOW_ALLOW_LIVE_WRITES": "", "MFLOW_LIVE_WRITE_STRICT": "",
         "MFLOW_WRITE_GUARD_HOSTS": ""}


def _env(**kw):
    d = dict(CLEAN)
    d.update(kw)
    return mock.patch.dict(os.environ, d)


class _Recorder(urllib.request.BaseHandler):
    """Fake https/http handler: records what would hit the network, returns {"ok": true}."""

    handler_order = 100  # run before the real HTTP(S)Handler

    def __init__(self):
        self.calls = []

    def _open(self, req):
        self.calls.append((req.get_method(), req.full_url, req.data))
        resp = urllib.request.addinfourl(io.BytesIO(b'{"ok": true}'), http.client.HTTPMessage(),
                                         req.full_url, 200)
        resp.msg = "OK"
        return resp

    https_open = http_open = _open


class TestEnvDetection(unittest.TestCase):
    def test_platform_default(self):
        self.assertEqual(G.env({}, "linux"), "production")
        self.assertEqual(G.env({}, "darwin"), "development")
        self.assertEqual(G.env({}, "win32"), "development")

    def test_explicit_override(self):
        self.assertEqual(G.env({"MFLOW_ENV": "development"}, "linux"), "development")
        self.assertEqual(G.env({"MFLOW_ENV": "production"}, "darwin"), "production")
        self.assertEqual(G.env({"MFLOW_ENV": "prod"}, "darwin"), "production")
        self.assertEqual(G.env({"APP_ENV": "production"}, "darwin"), "production")
        self.assertEqual(G.env({"APP_ENV": "dev"}, "linux"), "development")

    def test_mflow_env_wins_over_app_env(self):
        self.assertEqual(G.env({"MFLOW_ENV": "dev", "APP_ENV": "production"}, "linux"), "development")

    def test_blank_falls_back_to_platform(self):
        self.assertEqual(G.env({"MFLOW_ENV": "  "}, "linux"), "production")


class TestRequireLiveWrite(unittest.TestCase):
    def test_dev_blocks(self):
        with _env(MFLOW_ENV="development"), mock.patch("sys.stderr", new=io.StringIO()) as err:
            self.assertFalse(G.require_live_write("test write"))
        self.assertIn("开发环境", err.getvalue())

    def test_dev_opt_in_env(self):
        with _env(MFLOW_ENV="development", MFLOW_ALLOW_LIVE_WRITES="1"):
            self.assertTrue(G.require_live_write("test write"))

    def test_dev_opt_in_cli_flag(self):
        with _env(MFLOW_ENV="development"), mock.patch.object(G, "_CLI_LIVE", True):
            self.assertTrue(G.require_live_write("test write"))

    def test_dev_allow_flag(self):
        with _env(MFLOW_ENV="development"):
            self.assertTrue(G.require_live_write("test write", allow_flag=True))

    def test_prod_passes(self):
        with _env(MFLOW_ENV="production"):
            self.assertTrue(G.require_live_write("test write"))

    def test_strict_raises(self):
        with _env(MFLOW_ENV="development"):
            with self.assertRaises(G.LiveWriteBlocked):
                G.require_live_write("test write", strict=True)
        with _env(MFLOW_ENV="development", MFLOW_LIVE_WRITE_STRICT="1"):
            with self.assertRaises(G.LiveWriteBlocked):
                G.require_live_write("test write")

    def test_skipped_result_shape(self):
        r = G.skipped_result("x", url="")
        self.assertEqual(r["skipped"], "development")
        self.assertTrue(r["ok"] and r["dry_run"])

    def test_decorator_downgrades_to_dry_run(self):
        @G.dry_run_in_development("demo")
        def write(doc, dry_run=True):
            return {"ok": True, "dry_run": dry_run}

        with _env(MFLOW_ENV="development"), mock.patch("sys.stderr", new=io.StringIO()):
            r = write({}, dry_run=False)
        self.assertTrue(r["dry_run"])
        self.assertEqual(r["skipped"], "development")
        with _env(MFLOW_ENV="production"):
            r = write({}, dry_run=False)
        self.assertFalse(r["dry_run"])
        self.assertNotIn("skipped", r)
        with _env(MFLOW_ENV="development", MFLOW_ALLOW_LIVE_WRITES="1"):
            self.assertFalse(write({}, False)["dry_run"])


class TestClassify(unittest.TestCase):
    def test_reads_are_allowed(self):
        self.assertIsNone(G.classify_write("GET", "https://abc.api.sanity.io/v2024-01-01/data/mutate/production"))
        self.assertIsNone(G.classify_write("POST", "https://abc.api.sanity.io/v2024-01-01/data/query/production"))
        self.assertIsNone(G.classify_write("POST", "https://api.notion.com/v1/databases/x/query"))
        self.assertIsNone(G.classify_write(
            "POST", "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"))
        self.assertIsNone(G.classify_write("POST", "https://api.deepseek.com/chat/completions"))
        self.assertIsNone(G.classify_write("POST", "http://127.0.0.1:8088/api/x"))

    def test_writes_are_classified(self):
        self.assertEqual(G.classify_write("POST", "https://abc.api.sanity.io/v2024-01-01/data/mutate/production"),
                         "sanity-mutate")
        self.assertEqual(G.classify_write("POST", "https://blog.example.com/wp-json/wp/v2/posts"), "wordpress")
        self.assertEqual(G.classify_write("PATCH", "https://api.notion.com/v1/pages/x"), "notion")
        self.assertEqual(G.classify_write(
            "POST", "https://open.feishu.cn/open-apis/bitable/v1/apps/a/tables/t/records/batch_create"), "feishu")
        self.assertEqual(G.classify_write("POST", "https://open.feishu.cn/open-apis/bot/v2/hook/x"), "feishu")
        self.assertEqual(G.classify_write("POST", "https://api.cloudflare.com/client/v4/zones/z/purge_cache"),
                         "cloudflare")
        self.assertEqual(G.classify_write("POST", "https://api.indexnow.org/indexnow"), "indexnow")
        self.assertEqual(G.classify_write("POST", "https://hooks.slack.com/services/x"), "im")

    def test_extra_hosts(self):
        with _env(MFLOW_WRITE_GUARD_HOSTS="cms.example.org"):
            self.assertEqual(G.classify_write("PUT", "https://api.cms.example.org/x"), "custom")


class TestTransportGuard(unittest.TestCase):
    MUTATE = "https://abc.api.sanity.io/v2024-01-01/data/mutate/production"

    def setUp(self):
        self.rec = _Recorder()
        self.opener = urllib.request.build_opener(self.rec)

    def _post(self, url, payload):
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        return self.opener.open(req, timeout=5)

    def test_dev_skips_feishu_write(self):
        with _env(MFLOW_ENV="development"), mock.patch("sys.stderr", new=io.StringIO()):
            r = self._post("https://open.feishu.cn/open-apis/bot/v2/hook/x", {"msg_type": "text"})
            body = json.loads(r.read())
        self.assertEqual(self.rec.calls, [], "development 不应发出写请求")
        self.assertEqual(body["skipped"], "development")
        self.assertEqual(body["code"], 0)

    def test_dev_forces_sanity_native_dry_run(self):
        with _env(MFLOW_ENV="development"), mock.patch("sys.stderr", new=io.StringIO()):
            self._post(self.MUTATE, {"mutations": [{"patch": {"id": "a"}}], "dryRun": False})
        self.assertEqual(len(self.rec.calls), 1)
        method, url, data = self.rec.calls[0]
        self.assertIn("dryRun=true", url)
        self.assertIs(json.loads(data)["dryRun"], True)

    def test_dev_reads_pass_through(self):
        with _env(MFLOW_ENV="development"):
            self.opener.open("https://www.example.com/", timeout=5).read()
            self._post("https://abc.api.sanity.io/v2024-01-01/data/query/production", {"query": "*"})
        self.assertEqual(len(self.rec.calls), 2)

    def test_dev_opt_in_sends_unchanged(self):
        with _env(MFLOW_ENV="development", MFLOW_ALLOW_LIVE_WRITES="1"):
            self._post(self.MUTATE, {"mutations": [], "dryRun": False})
        self.assertIs(json.loads(self.rec.calls[0][2])["dryRun"], False)

    def test_prod_sends_unchanged(self):
        with _env(MFLOW_ENV="production"):
            self._post(self.MUTATE, {"mutations": [], "dryRun": False})
            self._post("https://open.feishu.cn/open-apis/bot/v2/hook/x", {})
        self.assertEqual(len(self.rec.calls), 2)
        self.assertNotIn("dryRun=true", self.rec.calls[0][1])

    def test_strict_raises(self):
        with _env(MFLOW_ENV="development", MFLOW_LIVE_WRITE_STRICT="1"):
            with self.assertRaises(G.LiveWriteBlocked):
                self._post("https://api.notion.com/v1/pages", {})

    def test_smtp_sendmail_skipped_in_dev(self):
        srv = smtplib.SMTP(local_hostname="localhost")  # no host → no connection, no FQDN lookup
        with _env(MFLOW_ENV="development"), mock.patch("sys.stderr", new=io.StringIO()):
            self.assertEqual(srv.sendmail("a@x", ["b@x"], "hi"), {})

    @unittest.skipUnless(__import__("importlib").util.find_spec("requests"), "requests 未安装")
    def test_requests_write_skipped_in_dev(self):
        import requests
        from requests.adapters import BaseAdapter

        sent = []

        class Fake(BaseAdapter):
            def send(self, request, **kw):
                sent.append(request)
                r = requests.models.Response()
                r.status_code, r._content, r.url, r.request = 200, b"{}", request.url, request
                return r

            def close(self):
                pass

        s = requests.Session()
        s.mount("https://", Fake())
        with _env(MFLOW_ENV="development"), mock.patch("sys.stderr", new=io.StringIO()):
            r = s.patch("https://api.notion.com/v1/pages/x", json={"properties": {}})
            self.assertEqual(r.json()["skipped"], "development")
            s.post(self.MUTATE, json={"mutations": [], "dryRun": False})
            s.get("https://api.notion.com/v1/pages/x")
        self.assertEqual(len(sent), 2)
        self.assertIn("dryRun=true", sent[0].url)
        self.assertIs(json.loads(sent[0].body)["dryRun"], True)


class TestCli(unittest.TestCase):
    def _run(self, *args, **envkw):
        e = {**os.environ, **CLEAN, **envkw}
        return subprocess.run([sys.executable, str(LIB / "env_guard.py"), *args],
                              capture_output=True, text=True, env=e, timeout=30)

    def test_env_and_check(self):
        self.assertEqual(self._run("env", MFLOW_ENV="production").stdout.strip(), "production")
        self.assertEqual(self._run("check", "x", MFLOW_ENV="production").returncode, 0)
        self.assertEqual(self._run("check", "x", MFLOW_ENV="development").returncode, G.EXIT_SKIPPED)
        self.assertEqual(self._run("check", "x", "--live", MFLOW_ENV="development").returncode, 0)
        self.assertEqual(self._run("check", "x", MFLOW_ENV="development",
                                   MFLOW_ALLOW_LIVE_WRITES="1").returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
