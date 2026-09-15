#!/usr/bin/env python3
"""MFlow Console v2 — content-ops workbench for the Lovart GEO workflow.

v3 adds the production core: LLM provider config (OpenAI-compatible), generation
  entry for blog + 6 landing types, Agent mode (Loop: generate->QA->feedback, max 3
  rounds, mirrors lovart-quality-cascade), node mode (per-step pipeline execution),
  Harness rules + Skills inventory with runtime re-sync.

stdlib + `markdown` package only. Publishing stays display-only (iron rule).
Auth: MFLOW_CONSOLE_PASSWORD from env; fail-closed when unset.
"""
import importlib.util
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import time
import urllib.parse
from datetime import datetime
from http import cookies as http_cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import markdown as md_lib

PROJECT = Path(__file__).resolve().parents[2]
CONSOLE_DIR = Path(__file__).resolve().parent
RUN_DIR = PROJECT / "run"
STATE_FILE = PROJECT / "1-3 GenFlow" / ".pipeline" / "pipeline-state.json"
EVENTS_FILE = PROJECT / "1-3 GenFlow" / ".pipeline" / "events.jsonl"
TASKS_FILE = RUN_DIR / "tasks.json"
DAILY_LOG = RUN_DIR / "logs" / "daily.out.log"
DAILY_PID = RUN_DIR / "logs" / "daily.pid"
KB_ROOT = PROJECT / "1-2 Insight" / "Knowledge Base"
LLM_FILE = RUN_DIR / "llm.json"
LOOPS_FILE = RUN_DIR / "loops.json"
GEN_DIR = PROJECT / "1-3 GenFlow" / "Console-Gen"
HARNESS_DIR = PROJECT / "1-1 Harness"
LOOP_LOCK = threading.Lock()
LOOP_THREADS = {}
PORT = int(os.environ.get("MFLOW_CONSOLE_PORT", "8088"))
PASSWORD = os.environ.get("MFLOW_CONSOLE_PASSWORD", "")

PS_PATH = PROJECT / "1-1 Harness" / "Skills" / "06-orchestrate" / "lovart-pipeline-state" / "pipeline_state.py"
ROUTER_PATH = PROJECT / "1-1 Harness" / "Skills" / "06-orchestrate" / "lovart-router" / "router.py"
HOOKS = ["pre-write-check.sh", "post-write-check.sh", "pre-import-check.sh", "post-generation-check.sh"]
READABLE_EXT = {".md", ".txt", ".json", ".csv", ".html", ".yaml", ".yml"}

# 报告中心目录映射（label -> (dir, glob)）
REPORT_CATS = [
    ("SEO 月报", "1-2 Insight/Trident Insights/reports/monthly", "*.md"),
    ("SEO 周报", "1-2 Insight/Trident Insights/reports/weekly", "*.md"),
    ("SEO 季报/年报", "1-2 Insight/Trident Insights/reports", "*.md"),
    ("舆情日报", "1-2 Insight/Lovart ORM", "Lovart-Sentinel-*-daily.md"),
    ("舆情周月报", "1-2 Insight/Lovart ORM/monthly", "*.md"),
    ("质量审计", "1-2 Insight/审计报告", "*.md"),
    ("页面分析/404", "1-2 Insight/Page Analytic", "*.md"),
    ("QA 记录", "1-2 Insight/QA", "*.md"),
    ("SEO 报告杂项", "1-2 Insight/SEO Reports", "*.md"),
    ("会话日志", "1-1 Harness/11-knowledge/sessions", "2026-*.md"),
]

SESSIONS = set()

# ── LLM 引擎（OpenAI 兼容）────────────────────────────────────────────
DEFAULT_LLM = {
    "providers": {
        "deepseek": {"base": "https://api.deepseek.com", "key": ""},
        "openai": {"base": "https://api.openai.com/v1", "key": ""},
        "custom": {"base": "", "key": ""}
    },
    "profiles": {
        "lovart-creation": {"provider": "deepseek", "model": "deepseek-chat"},
        "lovart-quality": {"provider": "deepseek", "model": "deepseek-chat"},
        "default": {"provider": "deepseek", "model": "deepseek-chat"}
    }
}


def llm_config():
    cfg = read_json(LLM_FILE, {})
    merged = json.loads(json.dumps(DEFAULT_LLM))
    merged.update(cfg)
    return merged


def llm_chat(messages, profile="default", max_tokens=4000, timeout=180):
    cfg = llm_config()
    pr = cfg["profiles"].get(profile) or cfg["profiles"]["default"]
    prov = cfg["providers"].get(pr["provider"], {})
    base, key, model = (prov.get("base") or "").rstrip("/"), prov.get("key", ""), pr.get("model", "")
    if not base or not key:
        raise RuntimeError(f"LLM 未配置：provider={pr['provider']} 缺 base/key（去 设置 页填写）")
    req = json.dumps({"model": model, "messages": messages,
                      "temperature": 0.7, "max_tokens": max_tokens}).encode()
    import urllib.request
    r = urllib.request.Request(base + "/chat/completions", data=req,
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + key})
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


# ── 生成模板（signal-writer 精华浓缩版；长文全景仍走本地 signal-writer 流程）──
GEN_TYPES = {
    "blog": "Blog 文章",
    "landing-tools": "落地页 · Tools",
    "landing-features": "落地页 · Features",
    "landing-product": "落地页 · Product",
    "landing-scenario": "落地页 · Scenario",
    "landing-solution": "落地页 · Solution",
    "landing-topic": "落地页 · Topic",
}
LANGS = ["zh", "en", "ja", "ko", "de", "fr", "pt", "ru", "it", "zh-TW"]

ANTI_SLOP = """硬性写作规则（违反任何一条即为废稿）：
- 每一段必须回答：谁会读 / 为什么现在读 / 读完改变什么 / 下一步是什么
- 禁止以下 AI 套话：In today's fast-paced world、game-changer、cutting-edge、unlock the power、seamlessly integrate、delve into、elevate your workflow、革命性、赋能、闭环（作修饰语时）
- 不可验证的数字一律标注 [待考证]，禁止编造产品数据
- 段落长度由语义完整性决定，不写零碎小段
- 面向真实用户的具体场景，不写空泛综述"""


def gen_prompt(ctype, lang, topic, brief, feedback=""):
    lang_name = {"zh": "简体中文", "zh-TW": "繁体中文", "en": "English", "ja": "日本語", "ko": "한국어",
                 "de": "Deutsch", "fr": "Français", "pt": "Português", "ru": "Русский", "it": "Italiano"}.get(lang, lang)
    if ctype == "blog":
        spec = f"""用{lang_name}写一篇 Blog 文章，主题：{topic}。
结构：H1 标题 → 导语（3-4 句，直给读者收益）→ 4-6 个 H2 章节（每章有小节正文，含具体场景/步骤/对比）→ FAQ（3 条）→ 结尾行动建议。
全文 1200-1800 字。可直接提及 Lovart（AI 设计工作台）作为相关工具推荐，但不通篇吹捧。"""
    else:
        page = ctype.split("-")[1]
        spec = f"""用{lang_name}写一个 {page.upper()} 类落地页的完整文案，主题：{topic}。
结构：Hero（大标题 + 副标题一句 + CTA 按钮文案）→ 3 个 Benefit 块（小标题 + 2-3 句说明）→ 使用场景 2 条 → FAQ（3 条）→ 底部 CTA。
 Lovart 相关功能描述基于公开常识，不编造参数。"""
    fb = (f"\n\n上一轮质检未通过，反馈如下，务必针对性修正：\n{feedback}") if feedback else ""
    return f"""{spec}

{brief}

{ANTI_SLOP}{fb}

直接输出 Markdown 正文，不要任何解释性开场白。"""


# ── Loop 引擎（Agent 模式：生成→质检→反馈迭代，≤3 轮，对应 quality-cascade）──
def _loop_save(loop):
    loops = read_json(LOOPS_FILE, [])
    loops = [x for x in loops if x.get("id") != loop["id"]]
    loops.append(loop)
    LOOPS_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOOPS_FILE.write_text(json.dumps(loops, ensure_ascii=False, indent=1))


def loop_engine(loop_id):
    def log(loop, msg):
        loop.setdefault("log", []).append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        _loop_save(loop)
    with LOOP_LOCK:
        loop = next((x for x in read_json(LOOPS_FILE, []) if x["id"] == loop_id), None)
    if not loop:
        return
    loop["status"] = "running"
    _loop_save(loop)
    log(loop, f"Loop 启动：{loop['goal']}")
    item = loop["item_id"]
    try:
        run_tool([sys.executable, str(PS_PATH), "advance", "--id", item, "--to", "S3-creating"])
    except Exception:
        pass
    feedback = ""
    for rnd in range(1, loop.get("max_rounds", 3) + 1):
        if loop.get("stop"):
            loop["status"] = "stopped"
            log(loop, "被用户停止")
            _loop_save(loop)
            return
        loop["round"] = rnd
        log(loop, f"第 {rnd} 轮：调用 LLM 生成（{loop['type']} / {loop['lang']}）")
        _loop_save(loop)
        try:
            draft = llm_chat([{"role": "user", "content": gen_prompt(
                loop["type"], loop["lang"], loop["topic"], loop["brief"], feedback)}],
                profile="lovart-creation", max_tokens=4000)
        except Exception as e:
            loop["status"] = "failed"
            log(loop, f"LLM 调用失败：{e}")
            _loop_save(loop)
            return
        draft_path = GEN_DIR / f"{item}.md"
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(draft)
        log(loop, f"草稿写入 {draft_path.relative_to(PROJECT)}（{len(draft)} 字符），跑质量门禁…")
        r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks/post-write-check.sh"),
                      "--file", str(draft_path), "--target-words", "300"], timeout=120)
        loop["last_hook_rc"] = r["rc"]
        if r["rc"] == 0:
            log(loop, "质检 PASS，推进状态机 S3-draft → S3-done → S4-qa")
            for stg in ("S3-draft", "S3-done", "S4-qa"):
                run_tool([sys.executable, str(PS_PATH), "advance", "--id", item, "--to", stg])
            loop["status"] = "done"
            loop["draft_path"] = rel_of(draft_path)
            log(loop, "Loop 完成：草稿已入 S4-qa，等待人工审阅/继续推进")
            _loop_save(loop)
            return
        feedback = r["out"][-1500:]
        log(loop, f"质检 BLOCK（exit {r['rc']}），反馈带入下一轮")
        _loop_save(loop)
    loop["status"] = "blocked"
    log(loop, f"达最大轮次仍 BLOCK。草稿在 {GEN_DIR / (item + '.md')}, 可人工修改后继续推进")
    _loop_save(loop)


def harness_inventory():
    rules = []
    rdir = HARNESS_DIR / "02-rules"
    if rdir.exists():
        for f in sorted(rdir.glob("RULES-*.md")) + sorted(rdir.glob("SESSION-ROUTING.md")):
            rules.append({"name": f.name, "path": rel_of(f),
                          "lines": len(f.read_text(errors="ignore").splitlines()),
                          "mtime": fdate(f.stat().st_mtime)})
    skills = []
    sk = HARNESS_DIR / "Skills"
    for f in sorted(sk.rglob("SKILL.md")):
        head = f.read_text(errors="ignore")[:400]
        m = re.search(r"description:\s*\n?\s*(.{5,120})", head)
        skills.append({"name": f.parent.name,
                       "group": str(f.parent.parent.relative_to(sk)),
                       "path": rel_of(f),
                       "desc": (m.group(1).replace("\n", " ").strip() if m else "")})
    return {"rules": rules, "skills": skills}

SESSIONS = set()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PS = load_module("mflow_pipeline_state", PS_PATH)
try:
    ROUTER = load_module("mflow_router", ROUTER_PATH)
except Exception as e:
    ROUTER = None
    print(f"[console] router import failed: {e}", file=sys.stderr)


def run_tool(args, timeout=60):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT))
        return {"rc": r.returncode, "out": (r.stdout + r.stderr)[-4000:]}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "out": "timeout"}


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return default


def safe_path(rel):
    """Resolve rel under PROJECT; reject traversal & unreadable types."""
    p = (PROJECT / rel).resolve()
    if p != PROJECT and PROJECT not in p.parents:
        return None
    if not p.exists() or p.suffix.lower() not in READABLE_EXT:
        return None
    return p


def rel_of(p):
    return str(Path(p).resolve().relative_to(PROJECT))


def fdate(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def list_reports():
    out = {}
    for label, rel, pattern in REPORT_CATS:
        base = PROJECT / rel
        files = []
        if base.exists():
            matches = [f for f in base.glob(pattern) if f.is_file()]
            matches.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            for f in matches[:120]:
                files.append({"path": rel_of(f), "name": f.name, "date": fdate(f.stat().st_mtime)})
        out[label] = files
    return out


def kb_tree():
    dirs = []
    if KB_ROOT.exists():
        for d in sorted(KB_ROOT.iterdir()):
            if d.is_dir() and not d.name.startswith((".", "_")) and d.name != "scripts":
                n = sum(1 for _ in d.rglob("*") if _.is_file())
                dirs.append({"name": d.name, "files": n})
        roots = list(KB_ROOT.glob("*.md"))
        dirs.insert(0, {"name": "(根目录文档)", "files": len(roots)})
    return dirs


def kb_list(sub):
    base = (KB_ROOT / sub).resolve() if sub else KB_ROOT
    if not str(base).startswith(str(KB_ROOT)) or not base.exists():
        return []
    if base == KB_ROOT:
        entries = list(KB_ROOT.glob("*.md"))
    else:
        entries = list(base.iterdir())
    items = []
    for f in sorted(entries, key=lambda x: x.name.lower()):
        if f.name.startswith(".") or f.name == "scripts":
            continue
        if f.is_dir():
            items.append({"type": "dir", "name": f.name, "path": rel_of(f)})
        elif f.suffix.lower() in READABLE_EXT:
            items.append({"type": "file", "name": f.name, "path": rel_of(f),
                          "date": fdate(f.stat().st_mtime)})
    return items[:400]


def kb_search(q, sub=""):
    base = (KB_ROOT / sub).resolve() if sub else KB_ROOT
    if not str(base).startswith(str(KB_ROOT)):
        return []
    q_lower = q.lower()
    hits, scanned = [], 0
    for f in sorted(base.rglob("*"), key=lambda x: x.stat().st_mtime, reverse=True):
        if not f.is_file() or f.suffix.lower() not in {".md", ".txt"} or "scripts" in f.parts:
            continue
        scanned += 1
        if scanned > 400:
            break
        if q_lower in f.name.lower():
            hits.append({"path": rel_of(f), "name": f.name, "match": "文件名匹配"})
            if len(hits) >= 30:
                return hits
            continue
        try:
            text = f.read_text(errors="ignore")
        except Exception:
            continue
        idx = text.lower().find(q_lower)
        if idx >= 0:
            snippet = text[max(0, idx - 50): idx + 90].replace("\n", " ").strip()
            hits.append({"path": rel_of(f), "name": f.name, "match": f"…{snippet}…"})
            if len(hits) >= 30:
                break
    return hits


def tasks_all():
    manual = read_json(TASKS_FILE, [])
    state = read_json(STATE_FILE, {})
    pipeline = [{"id": i.get("id"), "stage": i.get("stage"), "phase": i.get("phase"),
                 "source": "pipeline"}
                for i in state.get("items", {}).values()
                if i.get("stage") not in ("done", "failed", "escalated")]
    dist = []
    q = read_json(PROJECT / "1-3 GenFlow/Content Distribution/queue/pending.json", {})
    for it in q.get("items", []):
        dist.append({"id": it.get("id"), "status": it.get("status"),
                     "score": it.get("score"), "platforms": ",".join(it.get("platforms", [])),
                     "source": "distribution"})
    return {"manual": manual, "pipeline": pipeline, "distribution": dist}


def daily_status():
    running = False
    if DAILY_PID.exists():
        pid = DAILY_PID.read_text().strip()
        running = bool(pid) and Path(f"/proc/{pid}").exists()
    tail = ""
    if DAILY_LOG.exists():
        tail = "\n".join(DAILY_LOG.read_text().strip().split("\n")[-40:])
    return {"running": running, "tail": tail}


def overview():
    t = tasks_all()
    open_tasks = sum(1 for x in t["manual"] if x.get("status") != "done")
    state = read_json(STATE_FILE, {})
    inflight = sum(1 for i in state.get("items", {}).values()
                   if i.get("stage") not in ("done", "failed", "escalated"))
    sent = sorted((PROJECT / "1-2 Insight/Lovart ORM").glob("Lovart-Sentinel-*-daily.md"),
                  key=lambda f: f.stat().st_mtime, reverse=True)
    sent_age = None
    if sent:
        sent_age = (time.time() - sent[0].stat().st_mtime) // 86400
    monthly = sorted((PROJECT / "1-2 Insight/Trident Insights/reports/monthly").glob("*.md"),
                     key=lambda f: f.stat().st_mtime, reverse=True)
    weekly = sorted((PROJECT / "1-2 Insight/Trident Insights/reports/weekly").glob("*.md"),
                    key=lambda f: f.stat().st_mtime, reverse=True)
    timers = run_tool(["systemctl", "list-timers", "mflow-*", "--no-pager"], timeout=15)["out"]
    chart7 = []
    if EVENTS_FILE.exists():
        from collections import Counter
        days = Counter()
        for l in EVENTS_FILE.read_text().strip().split("\n")[-2000:]:
            try:
                e = json.loads(l)
            except Exception:
                continue
            ts = str(e.get("ts", ""))[:10]
            if ts:
                days[ts] += 1
        import datetime as _dt
        for i in range(6, -1, -1):
            d = (_dt.date.today() - _dt.timedelta(days=i)).isoformat()
            chart7.append({"label": d[5:], "n": days.get(d, 0)})
    return {
        "chart7d": chart7,
        "open_tasks": open_tasks,
        "pipeline_inflight": inflight,
        "dist_open": len(t["distribution"]),
        "sentinel_latest": {"name": sent[0].name, "path": rel_of(sent[0]), "age_days": int(sent_age)} if sent else None,
        "seo_monthly": {"name": monthly[0].name, "path": rel_of(monthly[0])} if monthly else None,
        "seo_weekly": {"name": weekly[0].name, "path": rel_of(weekly[0])} if weekly else None,
        "timers": timers[-1200:],
        "daily": daily_status(),
    }


def api_state():
    state = read_json(STATE_FILE, {})
    items = sorted(state.get("items", {}).values(), key=lambda i: i.get("updated_at", ""), reverse=True)
    events = []
    if EVENTS_FILE.exists():
        events = [json.loads(l) for l in EVENTS_FILE.read_text().strip().split("\n")[-40:] if l.strip()]
    decisions = [{"stage": d.get("stage"), "scenario": d.get("scenario"),
                  "profile": d.get("profile"), "action": d.get("action")}
                 for d in (ROUTER.DECISIONS if ROUTER else [])]
    return {"items": items,
            "legal_transitions": {k: sorted(v) for k, v in PS.TRANSITIONS.items()},
            "phases": PS.PHASES, "events": events, "decisions": decisions}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _authed(self):
        if not PASSWORD:
            return False  # fail-closed
        try:
            c = http_cookies.SimpleCookie(self.headers.get("Cookie", ""))
            return c["mflow_session"].value in SESSIONS
        except Exception:
            return False

    def _body(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path in ("/", "/index.html"):
            if not self._authed():
                return self._send(200, (CONSOLE_DIR / "login.html").read_bytes(), "text/html; charset=utf-8")
            return self._send(200, (CONSOLE_DIR / "console.html").read_bytes(), "text/html; charset=utf-8")
        if not self._authed():
            return self._send(401, {"error": "unauthorized"})
        try:
            if parsed.path == "/api/overview":
                return self._send(200, overview())
            if parsed.path == "/api/state":
                return self._send(200, api_state())
            if parsed.path == "/api/tasks":
                return self._send(200, tasks_all())
            if parsed.path == "/api/reports":
                return self._send(200, list_reports())
            if parsed.path == "/api/kb/tree":
                return self._send(200, kb_tree())
            if parsed.path == "/api/kb/list":
                return self._send(200, kb_list(qs.get("dir", [""])[0]))
            if parsed.path == "/api/kb/search":
                q = qs.get("q", [""])[0].strip()
                if len(q) < 2:
                    return self._send(400, {"error": "至少 2 个字符"})
                return self._send(200, kb_search(q, qs.get("dir", [""])[0]))
            if parsed.path == "/api/read":
                p = safe_path(qs.get("path", [""])[0])
                if not p:
                    return self._send(400, {"error": "路径不可读"})
                raw = p.read_text(errors="ignore")
                if p.suffix.lower() == ".md":
                    html = md_lib.markdown(raw, extensions=["tables", "fenced_code"])
                    return self._send(200, {"name": p.name, "html": html})
                return self._send(200, {"name": p.name, "html": "<pre>" + raw[:200000].replace("<", "&lt;") + "</pre>"})
            if parsed.path == "/api/dist":
                base = PROJECT / "1-3 GenFlow/Content Distribution/queue"
                q = read_json(base / "pending.json", {})
                pub = read_json(base / "published.json", {})
                dispatches = []
                for f in sorted(base.glob("dispatch-*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:12]:
                    d = read_json(f, {})
                    dispatches.append({"id": d.get("id", f.stem), "approved": bool(d.get("approved")),
                                       "cn": len(d.get("cn", [])), "gl": len(d.get("global", []))})
                return self._send(200, {
                    "pending": q.get("items", []),
                    "published": (pub.get("items", []) or [])[-10:][::-1],
                    "restart": q.get("restart", {}),
                    "dispatches": dispatches})
            if parsed.path == "/api/llm":
                cfg = llm_config()
                masked = json.loads(json.dumps(cfg))
                for pv in masked["providers"].values():
                    if pv.get("key"):
                        pv["key"] = pv["key"][:6] + "…" + pv["key"][-4:]
                return self._send(200, masked)
            if parsed.path == "/api/harness":
                return self._send(200, harness_inventory())
            if parsed.path == "/api/loops":
                loops = sorted(read_json(LOOPS_FILE, []),
                               key=lambda x: x.get("created", ""), reverse=True)
                return self._send(200, loops)
            if parsed.path == "/api/loop/detail":
                loop = next((x for x in read_json(LOOPS_FILE, []) if x["id"] == qs.get("id", [""])[0]), None)
                return self._send(200, loop or {"error": "not found"})
            if parsed.path == "/api/daily/log":
                return self._send(200, daily_status())
        except Exception as e:
            return self._send(500, {"error": str(e)[:300]})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/api/login":
            body = self._body()
            if PASSWORD and secrets.compare_digest(str(body.get("password", "")), PASSWORD):
                sid = secrets.token_urlsafe(32)
                SESSIONS.add(sid)
                self.send_response(200)
                self.send_header("Set-Cookie", f"mflow_session={sid}; HttpOnly; Path=/; SameSite=Lax")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            else:
                self._send(403, {"ok": False, "error": "wrong password"})
            return
        if not self._authed():
            return self._send(401, {"error": "unauthorized"})
        body = self._body()
        try:
            if self.path == "/api/logout":
                try:
                    c = http_cookies.SimpleCookie(self.headers.get("Cookie", ""))
                    SESSIONS.discard(c["mflow_session"].value)
                except Exception:
                    pass
                return self._send(200, {"ok": True})
            if self.path == "/api/item/upsert":
                item_id = str(body.get("id", "")).strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}", item_id):
                    return self._send(400, {"error": "id 必须是小写字母/数字/连字符"})
                r = run_tool([sys.executable, str(PS_PATH), "upsert", "--id", item_id,
                              "--category", str(body.get("category", "blog")),
                              "--target-type", str(body.get("target_type", "blog"))])
                return self._send(200 if r["rc"] == 0 else 400, r)
            if self.path == "/api/item/advance":
                r = run_tool([sys.executable, str(PS_PATH), "advance", "--id", str(body.get("id", "")),
                              "--to", str(body.get("to", "")),
                              "--reason", str(body.get("reason", "console"))[:200]])
                return self._send(200 if r["rc"] == 0 else 400, r)
            if self.path == "/api/router/decide":
                if not ROUTER:
                    return self._send(500, {"error": "router unavailable"})
                d = ROUTER._match_decision(str(body.get("stage", "")), str(body.get("scenario", "default")))
                if not d:
                    return self._send(404, {"error": "无匹配决策"})
                return self._send(200, {"ok": True, "verdict": {
                    "stage": d.get("stage"), "scenario": d.get("scenario"),
                    "action": d.get("action"), "profile": d.get("profile"),
                    "skills": d.get("skills"), "reason": d.get("reason")}})
            if self.path == "/api/hook/run":
                hook = str(body.get("hook", ""))
                if hook not in HOOKS:
                    return self._send(400, {"error": "unknown hook"})
                f = Path(str(body.get("file", ""))).resolve()
                if not f.exists() or PROJECT not in f.parents:
                    return self._send(400, {"error": "file 必须在项目目录内"})
                return self._send(200, run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks" / hook),
                                                 "--file", str(f)], timeout=120))
            if self.path == "/api/daily/run":
                if daily_status()["running"]:
                    return self._send(409, {"error": "每日管线已在运行中"})
                log = open(DAILY_LOG, "a")
                proc = subprocess.Popen(["bash", str(PROJECT / "1-4 Dev/automation/run-daily-pipeline.sh")],
                                        stdout=log, stderr=subprocess.STDOUT, cwd=str(PROJECT))
                DAILY_PID.write_text(str(proc.pid))
                return self._send(200, {"ok": True, "pid": proc.pid})
            if self.path == "/api/llm/save":
                body_providers = body.get("providers")
                body_profiles = body.get("profiles")
                cfg = llm_config()
                if body_providers:
                    for name, pv in body_providers.items():
                        cur = cfg["providers"].setdefault(name, {})
                        newkey = str(pv.get("key", ""))
                        if newkey and "…" not in newkey:  # masked value = keep old
                            cur["key"] = newkey
                        if pv.get("base"):
                            cur["base"] = pv["base"]
                if body_profiles:
                    cfg["profiles"].update(body_profiles)
                LLM_FILE.parent.mkdir(parents=True, exist_ok=True)
                LLM_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
                os.chmod(LLM_FILE, 0o600)
                return self._send(200, {"ok": True})
            if self.path == "/api/llm/test":
                try:
                    out = llm_chat([{"role": "user", "content": "回复 OK 两个字母即可"}],
                                   profile=str(body.get("profile", "default")), max_tokens=8, timeout=30)
                    return self._send(200, {"ok": True, "reply": out[:50]})
                except Exception as e:
                    return self._send(400, {"ok": False, "error": str(e)[:300]})
            if self.path == "/api/skills/sync":
                return self._send(200, run_tool([sys.executable, str(PROJECT / "1-4 Dev/scripts/harness_sync.py")], timeout=120))
            if self.path == "/api/generate":
                # 节点模式单步：LLM 生成 → 落盘 → 质检钩子（同步返回）
                item_id = str(body.get("item_id", "")).strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}", item_id):
                    return self._send(400, {"error": "id 不合法"})
                try:
                    run_tool([sys.executable, str(PS_PATH), "upsert", "--id", item_id,
                              "--category", str(body.get("type", "blog"))])
                    draft = llm_chat([{"role": "user", "content": gen_prompt(
                        str(body.get("type", "blog")), str(body.get("lang", "zh")),
                        str(body.get("topic", ""))[:300], str(body.get("brief", ""))[:800])}],
                        profile="lovart-creation")
                except Exception as e:
                    return self._send(400, {"error": str(e)[:300]})
                path = GEN_DIR / f"{item_id}.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(draft)
                hook = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks/post-write-check.sh"),
                                 "--file", str(path), "--target-words", "300"], timeout=120)
                return self._send(200, {"ok": True, "path": rel_of(path), "chars": len(draft),
                                        "hook_rc": hook["rc"], "hook_out": hook["out"][-2000:]})
            if self.path == "/api/loop/create":
                item_id = str(body.get("item_id", "")).strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}", item_id):
                    return self._send(400, {"error": "id 不合法"})
                with LOOP_LOCK:
                    loops = read_json(LOOPS_FILE, [])
                    if any(x.get("status") == "running" for x in loops):
                        return self._send(409, {"error": "已有 Loop 在运行（同时只跑一个，防超支）"})
                    loop = {"id": secrets.token_hex(4), "item_id": item_id,
                            "goal": str(body.get("topic", ""))[:200],
                            "type": str(body.get("type", "blog")), "lang": str(body.get("lang", "zh")),
                            "topic": str(body.get("topic", ""))[:300], "brief": str(body.get("brief", ""))[:800],
                            "status": "queued", "round": 0, "max_rounds": 3,
                            "created": datetime.now().strftime("%Y-%m-%d %H:%M"), "log": []}
                    loops.append(loop)
                    LOOPS_FILE.parent.mkdir(parents=True, exist_ok=True)
                    LOOPS_FILE.write_text(json.dumps(loops, ensure_ascii=False, indent=1))
                run_tool([sys.executable, str(PS_PATH), "upsert", "--id", item_id,
                          "--category", str(body.get("type", "blog"))])
                th = threading.Thread(target=loop_engine, args=(loop["id"],), daemon=True)
                LOOP_THREADS[loop["id"]] = th
                th.start()
                return self._send(200, {"ok": True, "id": loop["id"]})
            if self.path == "/api/loop/stop":
                loops = read_json(LOOPS_FILE, [])
                for x in loops:
                    if x["id"] == body.get("id"):
                        x["stop"] = True
                LOOPS_FILE.write_text(json.dumps(loops, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/add":
                title = str(body.get("title", "")).strip()[:200]
                if not title:
                    return self._send(400, {"error": "标题必填"})
                tasks = read_json(TASKS_FILE, [])
                tasks.append({"id": secrets.token_hex(4), "title": title,
                              "status": "todo", "source": "manual",
                              "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                              "note": str(body.get("note", ""))[:300]})
                TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
                TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/set":
                tasks = read_json(TASKS_FILE, [])
                for t in tasks:
                    if t["id"] == body.get("id"):
                        t["status"] = body.get("status", "todo")
                TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/del":
                tasks = [t for t in read_json(TASKS_FILE, []) if t["id"] != body.get("id")]
                TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
        except Exception as e:
            return self._send(500, {"error": str(e)[:300]})
        return self._send(404, {"error": "not found"})


def main():
    if not PASSWORD:
        print("[console] FAIL-CLOSED: MFLOW_CONSOLE_PASSWORD 未设置，API 全部拒绝", file=sys.stderr)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[console] MFlow Console v3 on :{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
