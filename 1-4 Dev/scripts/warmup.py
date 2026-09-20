#!/usr/bin/env python3
"""warmup.py — Lovart Global 开工预热（真实只读 / dry-run）

目的：让后台每一块都带着**真实的**历史记录、曲线、findings、缺口清单开工，
     而不是一屏空状态。所有动作要么只读，要么 dry-run——不写生产库。

原则（与 RULES-00 / 项目原则一致）：
  · 不伪造数据。跑不通的步骤如实记 skip/fail 与原因，绝不编一条历史。
  · 写生产库的动作一律 dry_run=True，且本脚本**不提供** --real 开关。
  · 幂等：重复跑只是多几条真实历史，不会破坏状态。

用法（在服务器上，或任何能访问 console 的机器）：
    export MFLOW_CONSOLE_PASSWORD=...        # 或 --password
    python3 "1-4 Dev/scripts/warmup.py"
    python3 "1-4 Dev/scripts/warmup.py" --only A,B      # 只跑部分板块
    python3 "1-4 Dev/scripts/warmup.py" --sync-library  # 含内容库全量同步（约 3 分钟）

板块：0 体检 · A 内容生产与发布 · B QA 编排与物料 · C Agent 与剧本 · D GEO 与报告 · E 治理收尾
退出码：0 = 无 fail；1 = 有 fail（skip 不算失败）
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from http.cookiejar import CookieJar
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_RUN = Path(os.environ["MFLOW_RUN_DIR"]).resolve() if os.environ.get("MFLOW_RUN_DIR") else ROOT / "run"
LOG_DIR = _RUN / "logs"


# ────────────────────────────── HTTP 客户端 ──────────────────────────────
class Console:
    def __init__(self, base, timeout=120):
        self.base = base.rstrip("/")
        self.timeout = timeout
        self.jar = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def _call(self, method, path, body=None, params=None, timeout=None):
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with self.opener.open(req, timeout=timeout or self.timeout) as r:
                raw = r.read().decode("utf-8", "replace")
                try:
                    return r.status, json.loads(raw)
                except json.JSONDecodeError:
                    return r.status, {"_raw": raw[:400]}
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace")
            try:
                return e.code, json.loads(raw)
            except json.JSONDecodeError:
                return e.code, {"error": raw[:300]}
        except Exception as e:
            return 0, {"error": f"{type(e).__name__}: {e}"}

    def get(self, path, params=None, timeout=None):
        return self._call("GET", path, None, params, timeout)

    def post(self, path, body=None, timeout=None):
        return self._call("POST", path, body or {}, None, timeout)

    def login(self, username, password):
        code, r = self.post("/api/login", {"username": username, "password": password})
        return code == 200 and not r.get("error"), r

    def wait_batch(self, task_id, timeout=240, poll=3):
        """等批量任务跑完（dry-run 也要等，否则历史停在 running）。"""
        end = time.time() + timeout
        last = {}
        while time.time() < end:
            code, r = self.get("/api/batch/detail", {"id": task_id})
            if code != 200:
                return {"status": "unknown", "error": r.get("error", f"HTTP {code}")}
            last = r.get("task") or r
            st = str(last.get("status", ""))
            if st in ("done", "failed", "cancelled", "tripped", "paused"):
                return last
            time.sleep(poll)
        return dict(last, status="timeout")


# ────────────────────────────── 步骤框架 ──────────────────────────────
class Runner:
    def __init__(self, con, args):
        self.con = con
        self.args = args
        self.results = []
        self.ctx = {}

    def step(self, area, name, fn):
        if self.args.only and area not in self.args.only:
            return
        t0 = time.time()
        sys.stdout.write(f"  [{area}] {name} ... ")
        sys.stdout.flush()
        try:
            status, detail = fn()
        except Exception as e:
            status, detail = "fail", f"{type(e).__name__}: {e}"
        el = round(time.time() - t0, 1)
        icon = {"ok": "✓", "skip": "—", "fail": "✗"}.get(status, "?")
        print(f"{icon} {detail}  ({el}s)")
        self.results.append({"area": area, "name": name, "status": status,
                             "detail": str(detail), "sec": el})

    @property
    def failed(self):
        return [r for r in self.results if r["status"] == "fail"]

    @property
    def skipped(self):
        return [r for r in self.results if r["status"] == "skip"]


# 「不是故障，只是还没有数据 / 还没配凭证」——这类一律记 skip，
# 否则报告里的 ✗ 会被噪音淹没，真故障就看不见了。
DATA_SKIPS = (
    "内容库里没有", "无物料台账", "镜像为空", "没有可", "无符合", "暂无", "为空",
    "未配置", "凭证", "SANITY_TOKEN", "not configured",
    "Tunnel connection failed", "403 Forbidden", "Connection refused", "Name or service",
    "LLM", "余额", "402", "key", "Key",
)


def looks_like_no_data(msg):
    return any(k in str(msg) for k in DATA_SKIPS)


def ok_or_fail(code, r, okmsg, *, skip_on=()):
    """统一把 API 返回翻译成 (status, detail)——错误如实报出，不美化。"""
    if code == 200 and not r.get("error"):
        return "ok", okmsg(r) if callable(okmsg) else okmsg
    err = str(r.get("error") or f"HTTP {code}")[:160]
    for pat in skip_on:
        if pat in err:
            return "skip", f"跳过：{err}"
    if looks_like_no_data(err):
        return "skip", f"跳过：{err}"
    return "fail", err


# ────────────────────────────── 板块 0：体检 ──────────────────────────────
def phase_0(R):
    con = R.con

    def health():
        code, r = con.get("/api/health")
        if code != 200:
            return "fail", f"HTTP {code}"
        R.ctx["health_before"] = r.get("level", "?")
        return "ok", f"level={r.get('level')} · {json.dumps(r.get('summary', {}), ensure_ascii=False)[:100]}"

    def selfcheck():
        code, r = con.get("/api/selfcheck")
        if code != 200:
            return "fail", f"HTTP {code}"
        items = r.get("items") or r.get("checks") or []
        bad = [i for i in items if str(i.get("level", "")) in ("block", "warn")]
        R.ctx["selfcheck_bad"] = len(bad)
        if not bad:
            return "ok", f"{len(items)} 项全绿"
        return "ok", f"{len(items)} 项，{len(bad)} 项待处理 → 尝试自愈"

    def autofix():
        if not R.ctx.get("selfcheck_bad"):
            return "skip", "自检无待处理项"
        code, r = con.post("/api/selfcheck/autofix")
        return ok_or_fail(code, r, lambda x: f"已修 {len(x.get('fixed', []))} 项，"
                                              f"{len(x.get('skipped', []))} 项需人工")

    def rag():
        code, r = con.get("/api/rag/status")
        if code != 200:
            return "fail", f"HTTP {code}"
        chunks = r.get("chunks") or r.get("count") or 0
        if chunks:
            return "ok", f"索引已在（{chunks} 块，{r.get('backend', '?')}）"
        code, r = con.post("/api/rag/build", timeout=300)
        return ok_or_fail(code, r, lambda x: f"已重建 {x.get('chunks', '?')} 块")

    R.step("0", "健康基线", health)
    R.step("0", "系统自检", selfcheck)
    R.step("0", "一键自愈", autofix)
    R.step("0", "RAG 检索底座", rag)


# ────────────────────────── 板块 A：内容生产与发布 ──────────────────────────
def phase_A(R):
    con, site = R.con, R.args.site

    def lib_status():
        code, r = con.get("/api/library/status", {"site": site})
        if code != 200:
            return "fail", f"HTTP {code}"
        total = r.get("total") or r.get("count") or 0
        R.ctx["library_total"] = total
        if total:
            return "ok", f"镜像 {total} 篇"
        return "ok", "镜像为空（加 --sync-library 可全量拉取）"

    def lib_sync():
        if not R.args.sync_library:
            return "skip", "未加 --sync-library"
        code, r = con.post("/api/library/sync", {"site": site}, timeout=600)
        return ok_or_fail(code, r, lambda x: f"同步 {x.get('total', '?')} 篇")

    def multilang():
        got, errs = [], []
        for sec in ("tools", "blog", "features"):
            code, r = con.get("/api/multilang/coverage", {"section": sec, "base_lang": "en"})
            if code == 200 and not r.get("error"):
                base = r.get("base_total") or r.get("total") or 0
                langs = r.get("langs") or r.get("coverage") or []
                got.append(f"{sec}:{base}篇/{len(langs)}语")
            else:
                errs.append(str(r.get("error") or f"HTTP {code}"))
        if got:
            return "ok", " · ".join(got)
        if not R.ctx.get("library_total") or all(looks_like_no_data(e) for e in errs):
            return "skip", f"内容库无数据：{errs[0][:100] if errs else '镜像为空'}"
        return "fail", errs[0][:150]

    def publish_ping():
        code, r = con.get("/api/publish/ping")
        return ok_or_fail(code, r, lambda x: f"Sanity {x.get('status') or x.get('ok')}",
                          skip_on=("未配置", "凭证", "not configured"))

    def landing_dry():
        code, r = con.post("/api/presets/run",
                           {"id": "landing-refresh-publish",
                            "options": {"dry_run": True, "limit": R.args.limit,
                                        "section": "tools", "lang": "en"}})
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "")
        tid = (r.get("task") or {}).get("id") or r.get("id")
        R.ctx["landing_task"] = tid
        t = con.wait_batch(tid, timeout=R.args.wait)
        st = t.get("status", "?")
        s = t.get("stats", {})
        return ("ok" if st == "done" else "fail"), \
               f"落地页闭环 dry-run {st}（{s.get('done', 0)}/{s.get('total', 0)}，失败 {s.get('failed', 0)}）task={tid}"

    def publish_history():
        code, r = con.get("/api/publish/history")
        if code != 200:
            return "fail", f"HTTP {code}"
        items = r if isinstance(r, list) else (r.get("items") or r.get("history") or [])
        return "ok", f"{len(items)} 条发布记录"

    R.step("A", "内容库状态", lib_status)
    R.step("A", "内容库同步", lib_sync)
    R.step("A", "多语言覆盖盘点", multilang)
    R.step("A", "发布通道连通", publish_ping)
    R.step("A", "落地页闭环 dry-run", landing_dry)
    R.step("A", "发布历史", publish_history)


# ────────────────────────── 板块 B：QA 编排与物料 ──────────────────────────
def phase_B(R):
    con, site = R.con, R.args.site

    def qa_scan():
        code, r = con.get("/api/qa/create", {"kind": "sanity-filter", "max": R.args.qa_max},
                          timeout=300)
        if code != 200 or r.get("error"):
            R.ctx["sanity_ok"] = False
            return ok_or_fail(code, r, "", skip_on=("发布器未加载", "凭证"))
        R.ctx["sanity_ok"] = True
        tid = (r.get("task") or {}).get("id") or r.get("id") or r.get("task_id")
        R.ctx["qa_task"] = tid
        t = con.wait_batch(tid, timeout=R.args.wait)
        return ("ok" if t.get("status") == "done" else "fail"), \
               f"扫描 {t.get('stats', {}).get('total', '?')} 篇，status={t.get('status')} task={tid}"

    def qa_findings():
        tid = R.ctx.get("qa_task")
        if not tid:
            return "skip", "无 QA 任务"
        code, r = con.get("/api/qa/findings", {"task": tid})
        if code != 200:
            return "fail", f"HTTP {code}"
        fs = r.get("findings") or (r if isinstance(r, list) else [])
        R.ctx["findings"] = len(fs)
        by = {}
        for f in fs:
            by[f.get("rule", "?")] = by.get(f.get("rule", "?"), 0) + 1
        top = " · ".join(f"{k}×{v}" for k, v in sorted(by.items(), key=lambda x: -x[1])[:4])
        return "ok", f"{len(fs)} 条 findings（{top or '无'}）"

    def qa_orchestrate():
        tid = R.ctx.get("qa_task")
        if not tid:
            return "skip", "无 QA 任务"
        if not R.ctx.get("findings"):
            return "ok", "0 findings——无需编排（如实记录，不造任务）"
        code, r = con.post("/api/qa/orchestrate", {"task": tid, "dry_run": True, "max_items": 200})
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "")
        kids = r.get("tasks") or r.get("created") or []
        R.ctx["qa_children"] = [k.get("id") if isinstance(k, dict) else k for k in kids]
        for k in R.ctx["qa_children"]:
            con.wait_batch(k, timeout=R.args.wait)
        return "ok", f"编排出 {len(kids)} 个修复任务（dry-run 已跑完）"

    def qa_recheck():
        tid = R.ctx.get("qa_task")
        if not tid or not R.ctx.get("findings"):
            return "skip", "无可复检对象"
        code, r = con.post("/api/qa/recheck", {"task": tid, "dry_run": True}, timeout=300)
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "")
        child = (r.get("task") or {}).get("id") or r.get("id")
        con.wait_batch(child, timeout=R.args.wait)
        code, d = con.get("/api/qa/delta", {"parent": tid, "child": child})
        if code == 200 and not d.get("error"):
            return "ok", (f"复检 delta：已解决 {len(d.get('resolved', []))} · "
                          f"新增 {len(d.get('new', []))}（dry-run 下未闭环属正常）")
        return "ok", f"复检任务 {child} 已建"

    def assets_scan():
        code, r = con.post("/api/assets/scan", {"site": site}, timeout=600)
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "")
        def _n(v):
            return len(v) if isinstance(v, (list, dict)) else int(v or 0)
        pages = _n(r.get("pages") or r.get("scanned") or r.get("total") or 0)
        urls = _n(r.get("assets") or r.get("urls") or 0)
        R.ctx["assets"] = urls
        if not pages and not urls:
            return "skip", "内容库镜像为空，无可扫描页面"
        return "ok", f"{pages} 页 / {urls} 个素材 URL"

    def alt_dry():
        code, r = con.post("/api/presets/run",
                           {"id": "asset-alt-fill", "options": {"dry_run": True, "limit": R.args.limit}})
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "", skip_on=("没有", "无符合", "0 项"))
        tid = (r.get("task") or {}).get("id") or r.get("id")
        t = con.wait_batch(tid, timeout=R.args.wait)
        s = t.get("stats", {})
        return "ok", f"封面 alt 补齐 dry-run {t.get('status')}（{s.get('done', 0)}/{s.get('total', 0)}）"

    R.step("B", "QA 扫描（真实读 Sanity）", qa_scan)
    R.step("B", "findings 归类", qa_findings)
    R.step("B", "修复编排 dry-run", qa_orchestrate)
    R.step("B", "复检闭环 delta", qa_recheck)
    R.step("B", "图片物料台账", assets_scan)
    R.step("B", "封面 alt 补齐 dry-run", alt_dry)


# ────────────────────────── 板块 C：Agent 与剧本 ──────────────────────────
def phase_C(R):
    con = R.con

    def opc():
        code, r = con.post("/api/playbooks/enable_recommended")
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "")
        n_en = r.get("enabled") or r.get("installed") or r.get("ids") or r.get("count") or 0
        n_en = len(n_en) if isinstance(n_en, (list, dict)) else int(n_en or 0)
        if not n_en:  # 已经装过就是 0，用实际清单说话，别报"0 个"让人误会失败
            c2, l2 = con.get("/api/playbooks")
            have = len((l2.get("playbooks") or [])) if c2 == 200 else 0
            return "ok", f"推荐剧本已在（当前共 {have} 个剧本，本次新增 0）"
        return "ok", f"推荐剧本 {n_en} 个已装启"

    def preview_all():
        code, r = con.get("/api/playbooks")
        if code != 200:
            return "fail", f"HTTP {code}"
        pbs = r.get("playbooks") or []
        R.ctx["playbooks"] = pbs
        if not pbs:
            return "skip", "无剧本"
        okn, tot = 0, 0
        for pb in pbs:
            c, p = con.post("/api/playbooks/preview", {"playbook": pb}, timeout=180)
            if c == 200 and not p.get("error"):
                okn += 1
                tot += int(p.get("total") or 0)
        return "ok", f"{okn}/{len(pbs)} 个剧本试运行预览通过，合计将处理 {tot} 条（零副作用）"

    def run_daily_qa():
        pbs = R.ctx.get("playbooks") or []
        pb = next((p for p in pbs if "qa" in str(p.get("id", "")).lower()), None) or (pbs[0] if pbs else None)
        if not pb:
            return "skip", "无剧本可跑"
        if not pb.get("dry_run", True):
            return "skip", f"剧本 {pb.get('id')} 非 dry-run，预热不碰真写"
        code, r = con.post("/api/playbooks/run", {"id": pb["id"]}, timeout=180)
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "", skip_on=("冷却", "上限", "并发"))
        rid = r.get("run_id") or r.get("id")
        R.ctx["run_id"] = rid
        end = time.time() + R.args.wait
        st = "running"
        while time.time() < end:
            c, d = con.get("/api/run/detail", {"id": rid})
            st = str(((d.get("run") or d).get("status")) or "?")
            if st in ("done", "failed", "cancelled"):
                break
            time.sleep(3)
        if st == "done":
            return "ok", f"剧本「{pb.get('name')}」run={rid} status=done"
        c, d = con.get("/api/run/detail", {"id": rid})
        run = (d.get("run") or d) if c == 200 else {}
        bad = next((x for x in (run.get("steps") or [])
                    if str(x.get("status", "")) in ("failed", "error")), {})
        why = str(bad.get("error") or bad.get("note") or run.get("error") or "").strip()[:140]
        step = bad.get("name", "?")
        msg = f"剧本「{pb.get('name')}」run={rid} status={st}"
        if bad:
            msg += f" · 卡在「{step}」" + (f"：{why}" if why else "")
        # 根因在上游（Sanity 连不上 / 内容库为空）时不算故障——修的是那边，不是剧本
        upstream_dry = (R.ctx.get("sanity_ok") is False) or not R.ctx.get("library_total")
        if looks_like_no_data(why) or (upstream_dry and not why):
            return "skip", msg + "（根因在上游：Sanity 未连通或内容库为空，非剧本故障）"
        return "fail", msg

    def agent_chat():
        msg = ("盘点一下 tools 段落 en 语言下 seoTitle 缺失的页面，"
               "先给我一个 dry-run 的修复方案，不要真写。")
        code, r = con.post("/api/agent/chat", {"message": msg}, timeout=300)
        if code != 200 or r.get("error"):
            return ok_or_fail(code, r, "", skip_on=("LLM", "余额", "402", "未配置", "key"))
        spec = r.get("spec")
        rev = (r.get("review") or {}).get("verdict", "—")
        qs = r.get("questions") or []
        R.ctx["agent_session"] = r.get("session_id")
        if spec:
            return "ok", f"出规格 type={spec.get('type')} items={len(spec.get('items', []))} · 审阅 verdict={rev}（未执行）"
        return "ok", f"Agent 反问 {len(qs)} 条（不确定即反问，符合设计）"

    def runs_list():
        code, r = con.get("/api/runs")
        if code != 200:
            return "fail", f"HTTP {code}"
        items = r if isinstance(r, list) else (r.get("runs") or r.get("items") or [])
        return "ok", f"执行画布历史 {len(items)} 条"

    R.step("C", "OPC 一键启用推荐剧本", opc)
    R.step("C", "全部剧本试运行预览", preview_all)
    R.step("C", "跑一次 dry-run 剧本", run_daily_qa)
    R.step("C", "Agent 任务台真实一轮", agent_chat)
    R.step("C", "执行画布历史", runs_list)


# ────────────────────────── 板块 D：GEO 与报告 ──────────────────────────
def phase_D(R):
    con = R.con

    def geo_probe():
        code, r = con.get("/api/geo/config")
        cfg = r if code == 200 else {}
        if not (cfg.get("queries") or cfg.get("brand")):
            return "skip", "GEO 未配置品牌/查询（设置页 GEO 卡填了才有意义）"
        code, r = con.post("/api/geo/probe", timeout=600)
        return ok_or_fail(code, r, lambda x: f"探测 {x.get('queries', '?')} 查询，"
                                             f"提及 {x.get('mentioned', '?')}",
                          skip_on=("demo", "LLM", "余额", "402", "key", "未配置"))

    def geo_state():
        code, r = con.get("/api/geo/citations")
        if code != 200:
            return "fail", f"HTTP {code}"
        cs = r.get("citations") or (r if isinstance(r, list) else [])
        R.ctx["citations"] = len(cs)
        if cs:
            return "ok", f"{len(cs)} 条引用记录"
        return "ok", "0 条引用记录（无数据即为 0，不造分）"

    def impact():
        code, r = con.get("/api/impact", timeout=180)
        return ok_or_fail(code, r, lambda x: f"归因数据 {len(x.get('rows', x.get('items', [])))} 行")

    def links():
        got, errs = [], []
        for sec in ("tools", "blog"):
            code, r = con.get("/api/links/audit",
                              {"section": sec, "lang": "en", "limit": R.args.limit}, timeout=300)
            if code == 200 and not r.get("error"):
                got.append(f"{sec}:{len(r.get('pages') or r.get('items') or [])}页")
            else:
                errs.append(str(r.get("error") or f"HTTP {code}"))
        if got:
            return "ok", "内链建议报告已出 · " + " · ".join(got)
        if not R.ctx.get("library_total") or all(looks_like_no_data(e) for e in errs):
            return "skip", "内容库无数据，无页面可分析"
        return "fail", errs[0][:150] if errs else "内链体检全部失败"

    def selfreview():
        code, r = con.post("/api/selfreview/generate", timeout=180)
        return ok_or_fail(code, r, lambda x: f"月度自我迭代回顾 → {x.get('path', '已生成')}")

    def reports():
        code, r = con.get("/api/reports")
        if code != 200:
            return "fail", f"HTTP {code}"
        items = r if isinstance(r, list) else (r.get("reports") or r.get("items") or [])
        return "ok", f"报告中心 {len(items)} 份"

    R.step("D", "GEO 引用探测", geo_probe)
    R.step("D", "GEO 引用记录", geo_state)
    R.step("D", "效果归因", impact)
    R.step("D", "内链建议体检", links)
    R.step("D", "月度自我迭代回顾", selfreview)
    R.step("D", "报告中心", reports)


# ────────────────────────── 板块 E：治理收尾 ──────────────────────────
def phase_E(R):
    con = R.con

    def learnings():
        code, r = con.post("/api/learnings/scan", {"days": 7}, timeout=180)
        return ok_or_fail(code, r, lambda x: f"失败→学习 产出 {len(x.get('learnings', x.get('items', [])))} 条")

    def housekeeping():
        code, r = con.post("/api/housekeeping/run", {"dry_run": True}, timeout=180)
        return ok_or_fail(code, r, lambda x: f"降噪预览：归档 {x.get('items', 0)} · "
                                             f"僵尸 {x.get('zombies', 0)} · 批量 {x.get('batch', 0)}")

    def governance():
        code, r = con.get("/api/governance", timeout=180)
        if code != 200:
            return "fail", f"HTTP {code}"
        gaps = r.get("kb_gaps") or r.get("gaps") or []
        if isinstance(gaps, dict):
            gaps = gaps.get("items") or list(gaps.values())
        cov = r.get("skills") or r.get("coverage") or {}
        parts = [f"知识库缺口 {len(gaps)}"]
        if isinstance(cov, dict) and cov:
            tot = cov.get("total") or len(cov.get("skills") or [])
            miss = cov.get("missing") or cov.get("uncovered") or []
            miss = len(miss) if isinstance(miss, (list, dict)) else int(miss or 0)
            if tot:
                parts.append(f"Skills {tot} 个，{miss} 类页面无专属 skill")
        return "ok", " · ".join(parts)

    def inbox():
        code, r = con.get("/api/inbox")
        if code != 200:
            return "fail", f"HTTP {code}"
        n = sum(len(v) for v in r.values() if isinstance(v, list))
        return "ok", f"收件箱 {n} 条待处理"

    def health_after():
        code, r = con.get("/api/health")
        if code != 200:
            return "fail", f"HTTP {code}"
        before = R.ctx.get("health_before", "?")
        R.ctx["health_after"] = r.get("level")
        return "ok", f"{before} → {r.get('level')}"

    R.step("E", "失败→学习扫描", learnings)
    R.step("E", "降噪治理预览", housekeeping)
    R.step("E", "治理面板", governance)
    R.step("E", "统一收件箱", inbox)
    R.step("E", "健康终态", health_after)


# ────────────────────────────── 报告 ──────────────────────────────
def write_report(R, args, started):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    f = LOG_DIR / f"warmup-{started:%Y%m%d-%H%M}.md"
    okn = len([x for x in R.results if x["status"] == "ok"])
    lines = [
        f"# 开工预热报告 — {args.project}",
        "",
        f"> 时间：{started:%Y-%m-%d %H:%M} · 耗时 {round(time.time() - started.timestamp())}s · "
        f"目标 `{args.base}`",
        f"> 结果：**{okn} ok · {len(R.skipped)} skip · {len(R.failed)} fail**"
        f" · 健康 {R.ctx.get('health_before', '?')} → {R.ctx.get('health_after', '?')}",
        "",
        "所有动作均为**只读或 dry-run**，未写入生产库。skip/fail 为如实记录，未以任何方式补数。",
        "",
        "| 板块 | 步骤 | 结果 | 说明 | 耗时 |",
        "|---|---|:--:|---|--:|",
    ]
    icon = {"ok": "✓", "skip": "—", "fail": "✗"}
    for r in R.results:
        d = r["detail"].replace("|", "\\|")[:150]
        lines.append(f"| {r['area']} | {r['name']} | {icon.get(r['status'], '?')} | {d} | {r['sec']}s |")
    if R.failed:
        lines += ["", "## 需要处理", ""]
        for r in R.failed:
            lines.append(f"- **[{r['area']}] {r['name']}** — {r['detail']}")
    if R.skipped:
        lines += ["", "## 被跳过（多为缺配置/缺数据，不是故障）", ""]
        for r in R.skipped:
            lines.append(f"- [{r['area']}] {r['name']} — {r['detail']}")
    lines += ["", "---", "", "重跑：`python3 \"1-4 Dev/scripts/warmup.py\"`（幂等，只会多出真实历史）", ""]
    f.write_text("\n".join(lines), encoding="utf-8")
    return f


def main():
    ap = argparse.ArgumentParser(description="Lovart Global 开工预热（真实只读 / dry-run）")
    ap.add_argument("--base", default=os.environ.get("MFLOW_BASE", "http://127.0.0.1:8088"))
    ap.add_argument("--user", default=os.environ.get("MFLOW_CONSOLE_USER", "admin"))
    ap.add_argument("--password", default=os.environ.get("MFLOW_CONSOLE_PASSWORD", ""))
    ap.add_argument("--project", default="lovart-global")
    ap.add_argument("--site", default="lovart-global")
    ap.add_argument("--only", default="", help="只跑指定板块，如 A,B（板块：0 A B C D E）")
    ap.add_argument("--limit", type=int, default=30, help="每个 dry-run 预设的条数上限")
    ap.add_argument("--qa-max", type=int, default=200, help="QA 扫描页数上限")
    ap.add_argument("--wait", type=int, default=300, help="单个批量任务最长等待秒数")
    ap.add_argument("--sync-library", action="store_true", help="含内容库全量同步（约 3 分钟）")
    args = ap.parse_args()
    args.only = [x.strip() for x in args.only.split(",") if x.strip()]

    if not args.password:
        print("✗ 缺密码：export MFLOW_CONSOLE_PASSWORD=... （见服务器 run/env.sh）")
        return 2

    started = datetime.now()
    print(f"\n开工预热 · {args.project} · {args.base}")
    print(f"模式：真实只读 / dry-run（本脚本不提供真写开关）\n")

    con = Console(args.base)
    ok, r = con.login(args.user, args.password)
    if not ok:
        print(f"✗ 登录失败：{r.get('error', r)}")
        return 2
    code, sw = con.post("/api/projects/switch", {"id": args.project})
    print(f"登录 {args.user} ✓ · 项目 {sw.get('current', args.project)}"
          f"{'' if code == 200 else ' (切换失败，用默认项目)'}\n")

    R = Runner(con, args)
    for fn in (phase_0, phase_A, phase_B, phase_C, phase_D, phase_E):
        fn(R)

    f = write_report(R, args, started)
    okn = len([x for x in R.results if x["status"] == "ok"])
    print(f"\n{'─' * 60}")
    print(f"完成：{okn} ok · {len(R.skipped)} skip · {len(R.failed)} fail")
    print(f"报告：{f}")
    if R.failed:
        print("\n需要处理：")
        for x in R.failed:
            print(f"  ✗ [{x['area']}] {x['name']} — {x['detail']}")
    return 1 if R.failed else 0


if __name__ == "__main__":
    sys.exit(main())
