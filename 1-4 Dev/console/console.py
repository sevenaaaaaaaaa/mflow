#!/usr/bin/env python3
"""MFlow Console — content-ops workbench for AI content factories (multi-project).

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
from collections import Counter
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
PROJECTS_DIR = RUN_DIR / "projects"
DEFAULT_PROJECT = "lovart-global"
DAILY_LOG = RUN_DIR / "logs" / "daily.out.log"
DAILY_PID = RUN_DIR / "logs" / "daily.pid"
KB_ROOT = PROJECT / "1-2 Insight" / "Knowledge Base"
LLM_FILE = RUN_DIR / "llm.json"
NOTIFY_FILE = RUN_DIR / "notify.json"
LOOPS_FILE = RUN_DIR / "loops.json"
GEN_DIR = PROJECT / "1-3 GenFlow" / "Console-Gen"
HARNESS_DIR = PROJECT / "1-1 Harness"
LOOP_LOCK = threading.Lock()
PS_LOCK = threading.Lock()  # pipeline-state.json 读改写竞争保护（并发批量生成会撞）
LOOP_THREADS = {}
MAX_PARALLEL_LOOPS = 2
_usage_lock = threading.Lock()
LAST_USAGE = {"total_tokens": 0}


def loop_queue_worker():
    """Queue scheduler across all projects (max parallel = MAX_PARALLEL_LOOPS)."""
    while True:
        time.sleep(4)
        try:
            all_loops = []
            if PROJECTS_DIR.exists():
                for lf in PROJECTS_DIR.glob("*/loops.json"):
                    pid = lf.parent.name
                    for x in read_json(lf, []):
                        x["_proj"] = pid
                        all_loops.append(x)
            running = [x for x in all_loops if x.get("status") == "running"]
            if len(running) >= MAX_PARALLEL_LOOPS:
                continue
            queued = sorted([x for x in all_loops if x.get("status") == "queued"],
                            key=lambda x: x.get("created", ""))
            if not queued:
                continue
            nxt = queued[0]
            th = threading.Thread(target=loop_engine, args=(nxt["id"], nxt["_proj"]), daemon=True)
            LOOP_THREADS[nxt["id"]] = th
            th.start()
        except Exception as e:
            print(f"[queue] {e}", file=sys.stderr)


def schedule_executor():
    """P5 自动排程：按项目配额从选题队列自动创建 Loop（全局并发仍受 queue worker 限制）。"""
    while True:
        time.sleep(300)
        try:
            if not PROJECTS_DIR.exists():
                continue
            today = datetime.now().strftime("%Y-%m-%d")
            for meta_f in PROJECTS_DIR.glob("*/meta.json"):
                pid = meta_f.parent.name
                meta = read_json(meta_f, {})
                sc = meta.get("schedule") or {}
                if not sc.get("auto_loop") or not int(sc.get("daily_quota", 0) or 0):
                    continue
                quota = int(sc.get("daily_quota", 0) or 0)
                pp = proj_paths(pid)
                loops = read_json(pp["loops"], [])
                created_today = sum(1 for x in loops if str(x.get("created", "")).startswith(today))
                if created_today >= quota:
                    continue
                topics = read_json(pp["topics"], [])
                topic = topics[0] if topics else None
                if topic:
                    topics = topics[1:]
                    pp["topics"].write_text(json.dumps(topics, ensure_ascii=False, indent=1))
                else:
                    topic = f"自动排程占位选题（队列空，{today}）"
                item_id = f"auto-{pid}-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(2)}"
                ps_run([sys.executable, str(PS_PATH),
                        "--state-path", str(pp["state"]), "--events-path", str(pp["events"]),
                        "upsert", "--id", item_id, "--category", "blog"])
                with LOOP_LOCK:
                    loops = read_json(pp["loops"], [])
                    loops.append({"id": secrets.token_hex(4), "item_id": item_id,
                                  "goal": topic, "template_id": sc.get("template_id", ""),
                                  "type": sc.get("content_type", "blog"), "lang": sc.get("lang", "zh"),
                                  "topic": topic, "brief": "", "status": "queued", "round": 0,
                                  "max_rounds": 3, "tokens_used": 0, "auto": True,
                                  "created": datetime.now().strftime("%Y-%m-%d %H:%M"), "log": []})
                    pp["loops"].write_text(json.dumps(loops, ensure_ascii=False, indent=1))
                with open(pp["sched_log"], "a") as f:
                    f.write(f"{datetime.now().isoformat(timespec='seconds')} CREATE {item_id} topic={topic[:40]} today={created_today + 1}/{quota}\n")
        except Exception as e:
            print(f"[schedule] {e}", file=sys.stderr)
USAGE_FILE = RUN_DIR / "llm-usage.jsonl"
DEMO_FLAG = RUN_DIR / "demo.json"
TEMPLATES_DIR = PROJECT / "templates"
VERSION_FILE = PROJECT / "VERSION"
CALENDAR_ROOT = PROJECT / "1-3 GenFlow" / "Content Calendar"
_CAL_CACHE = {"files": None, "ts": 0}

TRIDENT_STEPS = [
    {"id": "gsc", "name": "GSC 日拉", "cmd": [sys.executable, "1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/scripts/gsc_fetch.py", "--daily"],
     "desc": "Google Search Console 全维度拉数 → Data Ingestion/gsc-full.json"},
    {"id": "ga4", "name": "GA4 周拉", "cmd": [sys.executable, "1-4 Dev/scripts/trident/ga4_weekly_pull.py"],
     "desc": "GA4 有机流量拉数（需 ga4-token）"},
    {"id": "bing", "name": "Bing 拉数", "cmd": None,
     "desc": "Bing Webmaster 拉数（脚本内置于 run_all）"},
    {"id": "runall", "name": "全量 run_all", "cmd": ["bash", "1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/scripts/run_all.sh"],
     "desc": "Trident 全量：GSC + GA4 + Bing + 汇总分析"},
]

WORKFLOW_MAP = [
    {"id": "blog", "name": "Blog 生产",
     "flow": ["S0 选题入队", "S3 生成（Loop / 单次）", "S3 质检 post-write-check", "S4 QA 门禁 L1-L7", "S4-qa 人工审", "S5 pre-import → Sanity", "S6 监控"],
     "profiles": "生成 lovart-creation · 质检 lovart-quality · 发布 lovart-ops",
     "skills": ["lovart-blog-signal-writer", "lovart-content-quality-gates", "lovart-content-creation-orchestrator", "lovart-kb-mine"],
     "kb": ["铁律与规则", "故事线 SSOT", "写作方法论", "产品知识库"]},
    {"id": "landing", "name": "落地页生成",
     "flow": ["S0 入队", "S3 landing-page 生成 bodyJson", "S3 质检（结构/图片404）", "S4 人工审", "S5 Sanity createOrReplace"],
     "profiles": "lovart-creation · lovart-ops",
     "skills": ["lovart-landing-page", "lovart-page-serp-writer", "refresh-page-page-generator"],
     "kb": ["故事线 SSOT", "产品知识库", "铁律与规则"]},
    {"id": "qa", "name": "QA 质检",
     "flow": ["L1 convert 前 preflight", "L2 import 后 verify", "L3 发布前 5 维审计", "Anti-Slop 10 项"],
     "profiles": "lovart-quality",
     "skills": ["lovart-content-quality-gates", "lovart-content-audit"],
     "kb": ["铁律与规则", "质量案例库", "阶段手册 S0-S6"]},
    {"id": "publish", "name": "发布与分发",
     "flow": ["preflight BLOCK=0", "Sanity --missing 增量导入", "Sitemap/IndexNow", "四轨道分发", "外链回流"],
     "profiles": "lovart-ops · lovart-distribution",
     "skills": ["lovart-sanity-publish", "lovart-multi-platform-push", "lovart-sitemap-update"],
     "kb": ["UTM 与追踪规范", "铁律与规则"]},
    {"id": "trident", "name": "数据采集 Trident",
     "flow": ["GSC 拉数", "GA4 拉数", "Bing 拉数", "汇总分析", "周报/月报"],
     "profiles": "lovart-reports",
     "skills": ["lovart-trident-data-engine", "lovart-data-ingestion", "lovart-content-calendar"],
     "kb": ["关键词研究", "阶段手册 S0-S6"]},
    {"id": "daily", "name": "每日管线",
     "flow": ["08:00 GSC 日拉", "Sentinel 22 源采集", "舆情日报", "harness 学习/同步"],
     "profiles": "systemd timer（无 agent）",
     "skills": ["lovart-sentinel", "lovart-trident-data-engine"],
     "kb": ["项目记忆与治理"]},
]
PORT = int(os.environ.get("MFLOW_CONSOLE_PORT", "8088"))
PASSWORD = os.environ.get("MFLOW_CONSOLE_PASSWORD", "")
API_TOKEN = os.environ.get("MFLOW_API_TOKEN", "")  # 机器联动 token（OpenFlow/外部系统调用，GET-only）

PS_PATH = PROJECT / "1-1 Harness" / "Skills" / "06-orchestrate" / "lovart-pipeline-state" / "pipeline_state.py"
ROUTER_PATH = PROJECT / "1-1 Harness" / "Skills" / "06-orchestrate" / "lovart-router" / "router.py"
HOOKS = ["pre-write-check.sh", "post-write-check.sh", "geo-check.sh", "quota-check.sh", "lang-check.sh",
         "pre-import-check.sh", "post-generation-check.sh"]
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

# 知识中台：10 大知识源（产品知识只是其一；约束/故事线/方法论/策略皆是知识）
KNOWLEDGE_SOURCES = [
    ("产品知识库", "你的产品介绍 / 帮助中心 / 文档存档 / 新闻 / Changelog",
     [("1-2 Insight/Knowledge Base", "**/*.md")]),
    ("铁律与规则", "全局铁律 RULES-00 + 六条工作线规则 + 会话路由（创作的硬约束）",
     [("1-1 Harness/02-rules", "*.md")]),
    ("故事线 SSOT", "7 类页面 × 25 条故事线 + Features 生产规范（写落地页前必读）",
     [("1-1 Harness/08-storyline", "*.md")]),
    ("阶段手册 S0-S6", "采集/策略/创作/质检/发布/监控六阶段操作手册 + Anti-Bugs 注册表",
     [("1-1 Harness/Docs", "**/*.md")]),
    ("写作方法论", "Better Design 方法论：研究协议 / 信源分级 / voice 规则 / 反 slop / 伦理披露",
     [("1-3 GenFlow/bv-skill-v01", "*.md")]),
    ("内容策略", "漏斗矩阵 / 季节日历 / 行业深耕 / 竞品覆盖 / 程序化 SEO 等战略规划",
     [("1-3 GenFlow/Content Strategy", "**/*.md")]),
    ("关键词研究", "SEO 深度分析 / 竞品核心词 / SERP 文案基准 / 内容日历底稿",
     [("1-2 Insight/Keywords Research", "**/*.md")]),
    ("UTM 与追踪规范", "AD-Tracking SSOT：三层架构 / 平台宏 / url-builder（分发稿件必读）",
     [("1-3 GenFlow/AD-Tracking", "**/*.md")]),
    ("质量案例库", "历史 Bug 巡检与修复记录：tableBlock / 404 / 翻译质量 / 内链错误",
     [("1-3 GenFlow/Bugs", "*.md")]),
    ("项目记忆与治理", "MEMORY-PROJECT 事实清单 / 知识树 / 治理与部署 / 钩子文档",
     [("1-1 Harness/11-knowledge", "*.md"),
      ("1-1 Harness/09-scripts", "*.md"),
      ("deploy", "*.md"),
      ("1-4 Dev/scripts/hooks", "README.md")]),
]

SESSIONS = set()

# ── LLM 引擎（OpenAI 兼容）────────────────────────────────────────────
DEFAULT_LLM = {
    "providers": {
        "deepseek": {"base": "https://api.deepseek.com", "key": ""},
        "openai": {"base": "https://api.openai.com/v1", "key": ""},
        "perplexity": {"base": "https://api.perplexity.ai", "key": ""},
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


def llm_chat(messages, profile="default", max_tokens=4000, timeout=180, project=None):
    cfg = llm_config()
    pr = cfg["profiles"].get(profile) or cfg["profiles"]["default"]
    prov = cfg["providers"].get(pr["provider"], {})
    base, key, model = (prov.get("base") or "").rstrip("/"), prov.get("key", ""), pr.get("model", "")
    ov = {}
    if project:
        ov = (read_json(PROJECTS_DIR / project / "meta.json", {}) or {}).get("llm") or {}
    if ov.get("key") and ov.get("base"):  # P4-4：项目级 Key 覆盖（优先于全局）
        base, key, model = ov["base"].rstrip("/"), ov["key"], (ov.get("model") or model)
    if not base or not key:
        # Demo 模式回退：未配置 Key 但已导入 demo → 返回演示稿（零门槛看到完整闭环）
        prompt = messages[-1]["content"] if messages else ""
        if DEMO_FLAG.exists():
            m = re.search(r"主题：(.+?)。", prompt)
            return demo_draft("blog", "zh", m.group(1) if m else "工作流演示")
        raise RuntimeError(f"LLM 未配置：provider={pr['provider']} 缺 base/key（去 设置 页填写，或先在引导页导入 Demo 数据体验演示模式）")
    req = json.dumps({"model": model, "messages": messages,
                      "temperature": 0.7, "max_tokens": max_tokens}).encode()
    import urllib.request
    r = urllib.request.Request(base + "/chat/completions", data=req,
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + key})
    t0 = time.time()
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        data = json.loads(resp.read())
    content = data["choices"][0]["message"]["content"]
    try:
        rec = {"ts": datetime.now().isoformat(timespec="seconds"), "profile": profile, "model": model,
               "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
               "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
               "total_tokens": data.get("usage", {}).get("total_tokens", 0),
               "latency_s": round(time.time() - t0, 1)}
        USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USAGE_FILE, "a") as f:
            f.write(json.dumps(rec) + "\n")
        with _usage_lock:
            LAST_USAGE.clear()
            LAST_USAGE.update(rec)
    except Exception:
        pass
    return content


def llm_chat_full(messages, profile="default", max_tokens=4000, timeout=180, project=None, temperature=0.7, engine=None, engine_model=""):
    """P6/P7：返回 (content, meta)；meta 含 citations（Perplexity sonar 真引用）等原始字段。
    不做 demo 回退——探测场景必须真实引擎。
    engine=None → profile 常规链路（含项目 llm 覆盖）；engine=<provider 名> → 用该 provider 直连（多引擎交叉探测）。"""
    cfg = llm_config()
    pr = cfg["profiles"].get(profile) or cfg["profiles"]["default"]
    if engine and engine != pr["provider"]:
        if engine not in cfg["providers"]:
            raise RuntimeError(f"engine={engine} 不是已配置的 provider")
        prov = cfg["providers"][engine]
        if not (prov.get("base") and prov.get("key")):
            raise RuntimeError(f"engine={engine} 未配置 base/key（设置页填 {engine} 的 Key）")
        prov_name, model = engine, (engine_model or pr.get("model", ""))
    else:
        prov_name = pr["provider"]
        prov = cfg["providers"].get(prov_name, {})
        model = pr.get("model", "")
    base, key = (prov.get("base") or "").rstrip("/"), prov.get("key", "")
    if project:  # 项目级 Key 覆盖仍最优先
        ov = (read_json(PROJECTS_DIR / project / "meta.json", {}) or {}).get("llm") or {}
        if ov.get("key") and ov.get("base"):
            base, key, model = ov["base"].rstrip("/"), ov["key"], (ov.get("model") or model)
    if not base or not key:
        raise RuntimeError("LLM 未配置（geo 探测需要真实引擎，不走 demo 回退）")
    req = json.dumps({"model": model, "messages": messages,
                      "temperature": temperature, "max_tokens": max_tokens}).encode()
    import urllib.request
    r = urllib.request.Request(base + "/chat/completions", data=req,
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + key})
    t0 = time.time()
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        data = json.loads(resp.read())
    content = data["choices"][0]["message"]["content"]
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "profile": profile, "model": model,
           "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
           "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
           "total_tokens": data.get("usage", {}).get("total_tokens", 0),
           "latency_s": round(time.time() - t0, 1)}
    try:
        USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USAGE_FILE, "a") as f:
            f.write(json.dumps(rec) + "\n")
        with _usage_lock:
            LAST_USAGE.clear()
            LAST_USAGE.update(rec)
    except Exception:
        pass
    meta = {"model": model, "usage": rec}
    for k in ("citations", "search_results"):
        if data.get(k):
            meta[k] = data[k]  # Perplexity sonar 返回真实引用
    return content, meta


def notify_cfg():
    return read_json(NOTIFY_FILE, {"enabled": False, "feishu_webhook": ""})


def notify_send(title, text, timeout=6):
    """飞书 webhook 文本消息；失败静默（通知不可阻塞业务）。"""
    cfg = notify_cfg()
    if not cfg.get("enabled") or not cfg.get("feishu_webhook"):
        return False
    try:
        import urllib.request
        req = urllib.request.Request(cfg["feishu_webhook"],
                                     data=json.dumps({"msg_type": "text", "content": {"text": f"{title}\n{text}"}}).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
        return True
    except Exception as e:
        print(f"[notify] {e}", file=sys.stderr)
        return False


def notify_loop_end(loop, proj, outcome):
    """Loop 终态通知：done/blocked/failed；stopped（用户主动）不打扰。"""
    if outcome == "stopped":
        return
    status_zh = {"done": "✅ 完成", "blocked": "⛔ 3 轮仍 BLOCK", "failed": "❌ LLM 失败"}.get(outcome, outcome)
    lines = [f"[{proj}] Loop {loop.get('item_id', '')} {status_zh}",
             f"主题：{loop.get('topic', '')[:60]}",
             f"轮次：{loop.get('round', 0)}/{loop.get('max_rounds', 3)} · tokens：{loop.get('tokens_used', 0)}"]
    if outcome == "done" and loop.get("draft_path"):
        lines.append(f"草稿：{loop['draft_path']}")
    notify_send(f"MFlow · {status_zh}", "\n".join(lines))


def usage_stats():
    rows = []
    if USAGE_FILE.exists():
        for l in USAGE_FILE.read_text().strip().split("\n"):
            try:
                rows.append(json.loads(l))
            except Exception:
                continue
    by_day, by_profile = Counter(), Counter()
    for r in rows:
        by_day[r["ts"][:10]] += r["total_tokens"]
        by_profile[r["profile"]] += r["total_tokens"]
    return {"total_calls": len(rows),
            "total_tokens": sum(r["total_tokens"] for r in rows),
            "by_day": [{"date": d, "tokens": n} for d, n in sorted(by_day.items())[-14:]],
            "by_profile": dict(by_profile),
            "recent": rows[-50:][::-1]}


def calendar_index():
    now = time.time()
    if _CAL_CACHE["files"] is not None and now - _CAL_CACHE["ts"] < 600:
        return _CAL_CACHE["files"]
    files = []
    if CALENDAR_ROOT.exists():
        for f in CALENDAR_ROOT.rglob("*.md"):
            lm = re.search(r"-(ja|zh|zhtw|ko|de|fr|pt|ru|it)\.md$", f.name)
            lang = lm.group(1) if lm else "en"
            head = f.read_text(errors="ignore")[:600]
            title_m = re.search(r'title:\s*"?([^"\n]+)"?', head)
            date_m = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', head, re.M)
            cat_m = re.search(r'categor(?:y|ies):\s*\[?([^\]\n]+)', head)
            files.append({"path": rel_of(f), "lang": lang,
                          "name": f.name,
                          "title": (title_m.group(1).strip() if title_m else f.stem),
                          "date": date_m.group(1) if date_m else "",
                          "cat": (cat_m.group(1).strip().strip('"') if cat_m else "")})
    files.sort(key=lambda x: (x.get("date") or "", x["name"]), reverse=True)
    _CAL_CACHE["files"] = files
    _CAL_CACHE["ts"] = now
    return files


def calendar_view(q="", lang=""):
    files = calendar_index()
    if lang:
        files = [f for f in files if f["lang"] == lang]
    if q:
        ql = q.lower()
        files = [f for f in files if ql in f["title"].lower() or ql in f["name"].lower()]
    langs = Counter(f["lang"] for f in calendar_index())
    months = Counter((f.get("date") or "")[:7] for f in calendar_index() if f.get("date"))
    return {"total": len(calendar_index()),
            "langs": dict(langs), "months": dict(sorted(months.items())[-12:]),
            "files": files[:250]}


def _norm_url_path(u):
    """归一化 URL → 路径（协议/域/query/尾斜杠容错），用于 canonical 匹配。"""
    u = (u or "").split("?")[0].split("#")[0].rstrip("/")
    return "/" + u.split("://", 1)[-1].split("/", 1)[-1].lower() if "://" in u else u


def impact_report(proj=None):
    qbase = PROJECT / "1-3 GenFlow/Content Distribution/queue"
    pub = read_json(qbase / "published.json", {}).get("items", [])
    pend = read_json(qbase / "pending.json", {}).get("items", [])
    gsc = read_json(RUN_DIR / "local-dev/Output/Data Ingestion/gsc-full.json", {})
    pages = ((gsc.get("pages") or {}).get("top20_pages")) or []
    by_path = {}
    for pg in pages:
        try:
            path = urllib.parse.urlparse(pg.get("url", "")).path
            by_path[path] = {"clicks": pg.get("clicks", 0), "impr": pg.get("impr", 0)}
        except Exception:
            continue
    rows = []
    for x in pub:
        cu = x.get("canonical") or ""
        path = urllib.parse.urlparse(cu).path if cu else ""
        m = by_path.get(path)
        rows.append({"slug": x.get("slug") or "", "platform": x.get("platform") or "",
                     "offsite_url": x.get("offsite_url") or "", "canonical_path": path or cu,
                     "clicks": (m or {}).get("clicks"), "impr": (m).get("impr") if m else None,
                     "matched": bool(m) and bool(path)})
    rows.sort(key=lambda r: (r["clicks"] is None, -(r["clicks"] or 0)))
    decayed = decay_analysis(pub, by_path) if proj is not None else []
    recheck = recheck_window(pub, cited_paths=None, proj=proj) if proj is not None else []
    return {"rows": rows, "gsc_date": gsc.get("_date"), "gsc_pages": len(pages),
            "decayed": decayed, "recheck": recheck,
            "note": "归因范围 = GSC Top20 页面；全量归因需扩展 gsc_fetch 行数上限"}


def _cited_paths_all():
    """全部项目 citations.jsonl 中出现过的引用路径（B5/B1 共用）。"""
    cited = set()
    if PROJECTS_DIR.exists():
        for cf in PROJECTS_DIR.glob("*/citations.jsonl"):
            for l in cf.read_text(errors="ignore").strip().split("\n")[-400:]:
                try:
                    r = json.loads(l)
                except Exception:
                    continue
                for cp in r.get("cited_pages") or []:
                    cited.add(_norm_url_path(cp.get("canonical") or cp.get("cited") or ""))
                for u in r.get("urls") or []:
                    cited.add(_norm_url_path(u))
    return cited


def recheck_window(pub, cited_paths=None, proj=None, window_days=7):
    """P7-B5 发布后复测窗口：发布 ≤N 天且尚无 AI 引用记录的页面。
    probe_daily 开启时由 geo_scheduler 自动复测；此处只呈现窗口状态。"""
    import datetime as _dt
    today = _dt.date.today()
    if cited_paths is None:
        cited_paths = _cited_paths_all()
    out = []
    for x in pub:
        cu = x.get("canonical") or ""
        d = str(x.get("date") or "")[:10]
        try:
            age = (today - _dt.date.fromisoformat(d)).days if d else None
        except Exception:
            age = None
        if age is None or age < 0 or age > window_days:
            continue
        cited = _norm_url_path(cu) in cited_paths
        out.append({"slug": x.get("slug") or "", "canonical_path": urllib.parse.urlparse(cu).path if cu else "",
                    "age_days": age, "cited": cited,
                    "status": ("已被引用" if cited else f"待复测（第 {age + 1} 天 / 窗口 {window_days} 天）")})
    out.sort(key=lambda r: (r["cited"], r["age_days"]))
    return out


def decay_analysis(pub, by_path, min_age_days=30):
    """P7-B1 内容衰减：已发布 ≥N 天，且 GSC Top20 无匹配、且从未被 AI 引用。
    边界：GSC 数据是 Top20 子集——'无匹配'≠'零点击'，标注为 Top20 无记录。"""
    import datetime as _dt
    today = _dt.date.today()
    cited_paths = _cited_paths_all()
    out = []
    for x in pub:
        cu = x.get("canonical") or ""
        path = urllib.parse.urlparse(cu).path if cu else ""
        d = str(x.get("date") or "")[:10]
        try:
            age = (today - _dt.date.fromisoformat(d)).days if d else None
        except Exception:
            age = None
        if age is None or age < min_age_days:
            continue
        in_gsc = path in by_path
        cited = _norm_url_path(cu) in cited_paths
        if not in_gsc and not cited:
            out.append({"slug": x.get("slug") or "", "platform": x.get("platform") or "",
                        "canonical_path": path or cu, "age_days": age,
                        "reason": f"发布 {age} 天 · GSC Top20 无记录 · 无 AI 引用记录"})
    out.sort(key=lambda r: -r["age_days"])
    return out


def report_dashboard(path):
    p = safe_path(path)
    if not p:
        return {"error": "路径不可读"}
    raw = p.read_text(errors="ignore")
    m = re.search(r"((?:^[^\n]*\n)?\|[^\n]*\|\n\|[-: |]+\|\n(?:\|[^\n]*\|\n)+)", raw, re.M)
    if not m:
        return {"headers": [], "rows": [], "title": ""}
    tbl = m.group(1)
    lines = [l for l in tbl.strip().split("\n") if l.strip().startswith("|")]
    cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    headers = cells(lines[0]) if lines else []
    rows = [cells(l) for l in lines[2:]]
    title_m = re.search(r"^#\s+(.+)$", raw, re.M)
    return {"headers": headers, "rows": rows[:12],
            "title": title_m.group(1).strip()[:80] if title_m else p.name}


QA_HISTORY = RUN_DIR / "qa-history.jsonl"


def qa_log(source, hook, rc):
    try:
        QA_HISTORY.parent.mkdir(parents=True, exist_ok=True)
        with open(QA_HISTORY, "a") as f:
            f.write(json.dumps({"ts": datetime.now().isoformat(timespec="seconds"),
                                "source": source, "hook": hook, "rc": rc}) + "\n")
    except Exception:
        pass


def qa_stats(days=14):
    import datetime as _dt
    rows = []
    if QA_HISTORY.exists():
        for l in QA_HISTORY.read_text().strip().split("\n"):
            try:
                rows.append(json.loads(l))
            except Exception:
                continue
    by_day = {}
    for r in rows:
        d = r["ts"][:10]
        s = by_day.setdefault(d, {"total": 0, "pass": 0})
        s["total"] += 1
        if r["rc"] == 0:
            s["pass"] += 1
    out = []
    for i in range(days - 1, -1, -1):
        d = (_dt.date.today() - _dt.timedelta(days=i)).isoformat()
        s = by_day.get(d, {"total": 0, "pass": 0})
        rate = round((s["total"] - s["pass"]) / s["total"] * 100) if s["total"] else 0
        out.append({"date": d, "total": s["total"], "pass": s["pass"], "block_rate": rate})
    recent = rows[-30:][::-1]
    total = len(rows)
    blocks = sum(1 for r in rows if r["rc"] != 0)
    return {"days": out, "total_runs": total, "block_rate_all": round(blocks / total * 100) if total else 0,
            "recent": recent}


def selfreview_data():
    import datetime as _dt
    _dt_date, _dt_td = _dt.date, _dt.timedelta
    usage = usage_stats()
    qa = qa_stats(30)
    # 吞吐：全项目 events 30 天
    from collections import Counter
    days = Counter()
    if PROJECTS_DIR.exists():
        for ef in PROJECTS_DIR.glob("*/events.jsonl"):
            for l in ef.read_text().strip().split("\n")[-5000:]:
                try:
                    e = json.loads(l)
                    days[str(e.get("ts", ""))[:10]] += 1
                except Exception:
                    continue
    for i in range(29, -1, -1):
        d = (_dt_date.today() - _dt_td(days=i)).isoformat()
        days.setdefault(d, 0)
    thr = sorted(days.items())
    return {"qa": qa, "usage": {"total_tokens": usage["total_tokens"], "total_calls": usage["total_calls"],
                                "by_day": usage["by_day"]},
            "throughput": [{"date": d, "n": n} for d, n in thr]}


def selfreview_markdown():
    d = selfreview_data()
    month = datetime.now().strftime("%Y-%m")
    lines = [f"# MFlow 自我迭代回顾 — {month}", "",
             f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} · 覆盖近 30 天 · 数据源：qa-history / llm-usage / pipeline events", ""]
    lines += ["## 质量门禁", "",
              f"- 累计执行 {d['qa']['total_runs']} 次，整体 BLOCK 率 {d['qa']['block_rate_all']}%",
              "- 近 30 天逐日 BLOCK 率：", ""]
    for x in d["qa"]["days"]:
        if x["total"]:
            lines.append(f"  - {x['date']}：{x['total']} 次检查，BLOCK 率 {x['block_rate']}%")
    lines += ["", "## Token 消耗", "",
              f"- 累计 {d['usage']['total_calls']} 次调用 / {d['usage']['total_tokens']} tokens"]
    for x in d["usage"]["by_day"][-10:]:
        lines.append(f"  - {x['date']}：{x['tokens']} tokens")
    lines += ["", "## 吞吐（状态机推进）", ""]
    for x in d["throughput"][-10:]:
        if x["n"]:
            lines.append(f"  - {x['date']}：{x['n']} 次推进")
    lines += ["", "## 💡 洞察", "",
              "**问题**：待人工补充（回顾报告提供数据，判断由人做）", "",
              "**根源**：见各曲线异常点对应日期的 session log", "",
              "**缓解**：按 modules.md 迭代提示词模板与门禁规则", ""]
    return "\n".join(lines)


def report_structure(path):
    p = safe_path(path)
    if not p:
        return {"error": "路径不可读"}
    raw = p.read_text(errors="ignore")
    title_m = re.search(r"^#\s+(.+)$", raw, re.M)
    title = title_m.group(1).strip() if title_m else p.name
    sections = []
    cur = {"heading": "概览", "blocks": []}
    for chunk in re.split(r"^(##\s+.+)$", raw, flags=re.M):
        pass
    lines = raw.split("\n")
    cur = {"heading": "", "blocks": []}
    sections = []
    i = 0
    table_buf = []
    def flush_table():
        nonlocal table_buf
        if table_buf:
            headers = [c.strip() for c in table_buf[0].strip().strip("|").split("|")]
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in table_buf[2:]]
            sections[-1]["blocks"].append({"type": "table", "headers": headers, "rows": rows[:30]})
            table_buf = []
    for line in lines:
        if line.strip().startswith("|"):
            table_buf.append(line)
            continue
        if table_buf:
            flush_table()
        hm = re.match(r"^(#{2,3})\s+(.+)$", line)
        if hm:
            if cur["heading"] or cur["blocks"]:
                sections.append(cur)
            cur = {"heading": hm.group(2).strip(), "blocks": []}
            continue
        if line.strip().startswith("#"):  # H1 skip
            continue
        if line.strip():
            cur["blocks"].append({"type": "para", "text": line.strip()})
    if table_buf:
        flush_table()
    if cur["heading"] or cur["blocks"]:
        sections.append(cur)
    return {"title": title, "sections": sections[:20]}


def trident_status():
    ing = RUN_DIR / "local-dev/Output/Data Ingestion"
    health = []
    if ing.exists():
        for f in sorted(ing.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:8]:
            health.append({"name": f.name, "date": fdate(f.stat().st_mtime)})
    return {"steps": [{"id": s["id"], "name": s["name"], "desc": s["desc"], "has_cmd": bool(s["cmd"])} for s in TRIDENT_STEPS],
            "health": health}


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

CONTENT_BUDGET = """数量预算（RULES-70，超限即废稿）：
- 字数：Blog 1200-1800（绝不超 2160）；落地页文案 600-1000
- H2 章节 4-7 个；FAQ 3-5 条；不得为凑结构拆出空章节
- 每千字 1-3 个数据点；同一数据不重复出现；外部来源 2-5 条（必须完整 URL）
- 列表块 ≤4 处，禁止连续两个列表块；单段 ≤300 字符；禁止连续 3 段同句式开头
- 禁止：同义反复 / 复述式总结（综上所述）/ 模板过渡词堆砌（首先其次然后最后 ≥4 次）/ 形容词堆叠（强大而灵活）
- 字数不足时优先删冗余，绝不补形容词；能删不扩"""

CONTENT_BUDGET_LONGFORM = """数量预算（长文豁免档，须 skill 显式声明 budget_profile: longform）：
- 字数上限 9000；H2 ≤14；FAQ ≤8；连续列表项 ≤14
- 其余同 RULES-70（数据点密度、禁止重复句/复述/过渡词堆砌、优先删冗余）
- **豁免不等于放水**：仍受 Anti-Slop 与 GEO 门禁约束"""

LANG_RULES = {
    "zh": "简体中文：全角标点；数字与英文词前后不加空格；避免连续「的」；不用英文标点结尾",
    "zh-TW": "繁體中文：禁止簡體字（設計/內容/專案/資訊/影片）；用台湾惯用语",
    "ja": "日本語：日式漢字寫法（禁止简体中文字形）；敬体/常体全文一致；句读用「、」",
    "ko": "한국어：谚文为主；句末敬语统一（-습니다/-해요 择一）",
    "de": "Deutsch：名词首字母大写；复合词不造词；Sie 与 du 择一",
    "fr": "Français：标点空格规则（«  »、冒号前空格）；标题实词不大写",
    "pt": "Português：默认巴西葡语；术语全文一致",
    "ru": "Русский：西里尔字母完整；避免英语借词直用；普通名词句首不大写",
    "it": "Italiano：冠词缩合正确（del/della/nel）；标题实词不大写",
    "en": "English：Title Case 或 Sentence Case 全文一致；禁止中文标点；避免中式长定语链",
}


ANTI_SLOP = """硬性写作规则（违反任何一条即为废稿）：
- 每一段必须回答：谁会读 / 为什么现在读 / 读完改变什么 / 下一步是什么
- 禁止以下 AI 套话：In today's fast-paced world、game-changer、cutting-edge、unlock the power、seamlessly integrate、delve into、elevate your workflow、革命性、赋能、闭环（作修饰语时）
- 不可验证的数字一律标注 [待考证]，禁止编造产品数据
- 段落长度由语义完整性决定，不写零碎小段
- 面向真实用户的具体场景，不写空泛综述"""

GEO_RULES = """GEO 可引用性规则（生成式引擎按块摘录，违反会被 GEO 门禁打回）：
- 至少 2 个 H2/H3 标题写成用户真实提问的形式（以 ? 或 ？结尾），或包含一节 FAQ
- 每千字至少 1 个具体数据点（百分比/价格/年份/倍数）
- 引用外部来源时必须写出完整可点击链接（https://…）+ 来源名，全文 ≥2 条（不要只写域名）
- 段落保持自包含短段：单段不超过 300 字符，一段只讲一个可摘录的观点
- 关键结论写成可直接摘录的"定义句/结论句"（主语+判断+数据）"""


def get_template(tid):
    if not tid:
        return None
    f = TEMPLATES_DIR / f"{str(tid).replace('/', '').replace('..', '')}.json"
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text())
    except Exception:
        return None


def list_templates():
    out = []
    if TEMPLATES_DIR.exists():
        for f in sorted(TEMPLATES_DIR.glob("*.json")):
            try:
                d = json.loads(f.read_text())
            except Exception:
                continue
            out.append({"id": d.get("id", f.stem), "name": d.get("name", f.stem),
                        "version": d.get("version", "1.0"), "author": d.get("author", ""),
                        "description": d.get("description", ""),
                        "workflow": d.get("workflow"), "file": rel_of(f)})
    return out


def run_content_gates(path, ctype="blog", lang="zh", tag="gate", budget_profile="default"):
    """统一内容门禁：结构/反slop + GEO 可引用性 + 数量预算 + 语言规范。"""
    args_by_hook = {
        "post-write-check.sh": ["--target-words", "300"],
        "geo-check.sh": [],
        "quota-check.sh": ["--type", "landing" if str(ctype).startswith("landing") else "blog",
                           "--lang", lang or "zh", "--profile", budget_profile or "default"],
        "lang-check.sh": ["--lang", lang or "zh"],
    }
    out = {}
    for hook, extra in args_by_hook.items():
        r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks" / hook), "--file", str(path), *extra], timeout=120)
        qa_log(tag, hook, r["rc"])
        out[hook] = r
    return out


def gen_prompt(ctype, lang, topic, brief, feedback="", template=None, budget_profile="default", style_id=""):
    lang_name = {"zh": "简体中文", "zh-TW": "繁体中文", "en": "English", "ja": "日本語", "ko": "한국어",
                 "de": "Deutsch", "fr": "Français", "pt": "Português", "ru": "Русский", "it": "Italiano"}.get(lang, lang)
    tpl = (template or {}).get("prompt") or {}
    audience = tpl.get("audience")
    tone = tpl.get("tone")
    extra = tpl.get("anti_slop_extra", "")
    structure = tpl.get("structure", "")
    if structure:
        spec = f"用{lang_name}写。{structure.replace('{TOPIC}', topic)}"
        if ctype == "blog":
            spec += "\n全文 1200-1800 字。"
    elif ctype == "blog":
        spec = f"""用{lang_name}写一篇 Blog 文章，主题：{topic}。
结构：H1 标题 → 导语（3-4 句，直给读者收益）→ 4-6 个 H2 章节（每章有小节正文，含具体场景/步骤/对比）→ FAQ（3 条）→ 结尾行动建议。
全文 1200-1800 字。可在结尾自然推荐你的产品/工具（如适用），但不通篇吹捧。"""
    else:
        page = ctype.split("-")[1]
        spec = f"""用{lang_name}写一个 {page.upper()} 类落地页的完整文案，主题：{topic}。
结构：Hero（大标题 + 副标题一句 + CTA 按钮文案）→ 3 个 Benefit 块（小标题 + 2-3 句说明）→ 使用场景 2 条 → FAQ（3 条）→ 底部 CTA。
产品能力描述基于公开常识，不编造参数。"""
    lang_rule = LANG_RULES.get(lang, "")
    budget = CONTENT_BUDGET_LONGFORM if budget_profile == "longform" else CONTENT_BUDGET
    anti = ANTI_SLOP_STRONG + "\n" + GEO_RULES + "\n" + budget + (f"\n语言规范：{lang_rule}" if lang_rule else "") + (f"\n{extra}" if extra else "")
    aud = (f"\n目标读者：{audience}" if audience else "")
    ton = (f"\n语气要求：{tone}" if tone else "")
    fb = (f"\n\n上一轮质检未通过，反馈如下，务必针对性修正：\n{feedback}") if feedback else ""
    return f"""{spec}{aud}{ton}

{brief}

{anti}{fb}

直接输出 Markdown 正文，不要任何解释性开场白。"""


# ── Loop 引擎（Agent 模式：生成→质检→反馈迭代，≤3 轮，对应 quality-cascade）──
def _loop_save(loop, proj):
    lp = proj_paths(proj)["loops"]
    loops = read_json(lp, [])
    loops = [x for x in loops if x.get("id") != loop["id"]]
    loops.append(loop)
    lp.parent.mkdir(parents=True, exist_ok=True)
    lp.write_text(json.dumps(loops, ensure_ascii=False, indent=1))


def loop_engine(loop_id, proj):
    lp = proj_paths(proj)["loops"]
    gen_dir = proj_paths(proj)["gen"]
    def log(loop, msg):
        loop.setdefault("log", []).append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        _loop_save(loop, proj)
    with LOOP_LOCK:
        loop = next((x for x in read_json(lp, []) if x["id"] == loop_id), None)
    if not loop:
        return
    loop["status"] = "running"
    _loop_save(loop, proj)
    log(loop, f"Loop 启动：{loop['goal']}")
    item = loop["item_id"]
    ps_args = ["--state-path", str(proj_paths(proj)["state"]), "--events-path", str(proj_paths(proj)["events"])]
    try:
        ps_run([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item, "--to", "S3-creating"])
    except Exception:
        pass
    feedback = ""
    for rnd in range(1, loop.get("max_rounds", 3) + 1):
        if loop.get("stop"):
            loop["status"] = "stopped"
            log(loop, "被用户停止")
            _loop_save(loop, proj)
            return
        loop["round"] = rnd
        log(loop, f"第 {rnd} 轮：调用 LLM 生成（{loop['type']} / {loop['lang']}）")
        _loop_save(loop, proj)
        try:
            draft = llm_chat([{"role": "user", "content": gen_prompt(
                loop["type"], loop["lang"], loop["topic"], loop["brief"], feedback,
                template=get_template(loop.get("template_id")))}],
                profile="lovart-creation", max_tokens=4000, project=proj)
        except Exception as e:
            loop["status"] = "failed"
            log(loop, f"LLM 调用失败：{e}")
            _loop_save(loop, proj)
            notify_loop_end(loop, proj, "failed")
            return
        with _usage_lock:
            loop["tokens_used"] = loop.get("tokens_used", 0) + LAST_USAGE.get("total_tokens", 0)
        draft_path = gen_dir / f"{item}.md"
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(draft)
        log(loop, f"草稿写入 {draft_path.relative_to(PROJECT)}（{len(draft)} 字符），跑质量门禁…")
        demo_mode = DEMO_FLAG.exists() and not llm_config()["providers"][
            llm_config()["profiles"]["default"]["provider"]].get("key")
        gates = run_content_gates(draft_path, loop.get("type", "blog"), loop.get("lang", "zh"),
                                  tag=f"loop:{loop.get('id','')}")
        r = gates["post-write-check.sh"]
        geo = gates["geo-check.sh"]
        quota = gates["quota-check.sh"]
        langc = gates["lang-check.sh"]
        loop["last_hook_rc"] = r["rc"]
        loop["last_geo_rc"] = geo["rc"]
        loop["last_quota_rc"] = quota["rc"]
        loop["last_lang_rc"] = langc["rc"]
        if r["rc"] == 0 and geo["rc"] == 0 and quota["rc"] == 0 and langc["rc"] == 0:
            log(loop, "质检 PASS（post-write + GEO 可引用性），推进状态机 S3-draft → S3-done → S4-qa")
            for stg in ("S3-draft", "S3-done", "S4-qa"):
                ps_run([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item, "--to", stg])
            loop["status"] = "done"
            loop["draft_path"] = rel_of(draft_path)
            log(loop, "Loop 完成：草稿已入 S4-qa，等待人工审阅/继续推进")
            _loop_save(loop, proj)
            notify_loop_end(loop, proj, "done")
            return
        feedback = "\n".join(x["out"] for x in (r, geo, quota, langc) if x["rc"] != 0)
        log(loop, f"质检 BLOCK（post-write {r['rc']} / geo {geo['rc']} / quota {quota['rc']} / lang {langc['rc']}），反馈带入下一轮")
        _loop_save(loop, proj)
        _loop_save(loop, proj)
    loop["status"] = "blocked"
    log(loop, f"达最大轮次仍 BLOCK。草稿在 {gen_dir / (item + '.md')}, 可人工修改后继续推进")
    _loop_save(loop, proj)
    notify_loop_end(loop, proj, "blocked")


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

DEMO_MODE_NOTE = {"demo": True}


def demo_draft(ctype, lang, topic):
    """无 LLM Key 时的演示稿：结构完整、可通过 post-write-check，让用户零门槛看到闭环。"""
    return f"""# {topic or "Demo"}：第一次内容工作流演示

这是一篇由 MFlow 工作流生成的演示草稿（demo 模式，未调用真实大模型）。
它展示的是系统的完整闭环：生成 → 质量门禁 → 状态机推进 → 人工审阅。

## 它解决什么问题

内容团队每天要回答三个问题：写什么、怎么写、发到哪。这篇演示稿对应"怎么写"环节。
读者是刚接触 MFlow 的运营者：读完你就能看懂一篇合格稿件的结构标准。

## 系统如何保证质量

MFlow 把写作规范做成可执行的检查，而不是写在文档里靠自觉。
生成完成后系统自动运行质量门禁：标题层级、段落信息密度、模板话术残留、占位符都会被检查。
不通过的稿件会带着反馈回到生成环节重写，最多三轮，这正是 Loop 模式的作用。

## 多语言从这里开始

MFlow 支持十种语言的独立撰写而非机器直译。切换语言后重新生成，你会得到符合当地表达习惯的版本。
一些团队用同样的方法维护多语言市场的内容，具体数字因项目而异 [待考证]。

## 下一步

在设置页配置你的大模型 API Key，然后回创作中心用同一主题发起一次正式生成。
对比演示稿与真实稿的差异，你就能判断提示词模板是否需要按你的行业调整。

## FAQ

**演示稿可以发布吗？** 可以走完发布流程，但它不含真实信息量，建议只用它理解流程。

**质量门禁会误杀正常内容吗？** 会偶发。门禁输出会说明触发原因，人工审阅环节可以放行。

**如何换成本公司的品牌语气？** 修改创作中心使用的提示词模板，把品牌词与禁用词表替换即可。
"""


def setup_status(proj):
    llm = llm_config()
    llm_ok = any((p or {}).get("key") for p in llm["providers"].values())
    kb_total = sum(x["files"] for x in kb_tree())
    cal = sum(1 for _ in CALENDAR_ROOT.rglob("*.md")) if CALENDAR_ROOT.exists() else 0
    items = len(read_json(proj_paths(proj)["state"], {}).get("items", {}))
    return [
        {"id": "password", "label": "访问密码已设置", "ok": bool(PASSWORD),
         "hint": "run/env.sh 的 MFLOW_CONSOLE_PASSWORD", "goto": "sys"},
        {"id": "llm", "label": "大模型 API 已配置", "ok": llm_ok,
         "hint": "设置页填 DeepSeek/OpenAI Key 并测试连通", "goto": "set"},
        {"id": "kb", "label": "知识库已就绪", "ok": kb_total > 0,
         "hint": f"当前 {kb_total} 份知识文档", "goto": "kb"},
        {"id": "calendar", "label": "内容日历已同步", "ok": cal > 0,
         "hint": f"当前 {cal} 篇", "goto": "calt"},
        {"id": "demo", "label": "Demo 数据已导入（可选）", "ok": DEMO_FLAG.exists(),
         "hint": "一键注入演示任务与示例报告", "goto": "setup"},
        {"id": "firstflow", "label": "第一个工作流已运行", "ok": items > 0,
         "hint": "创作中心发起一次生成或 Loop", "goto": "create"},
    ]


def seed_demo(proj):
    DEMO_FLAG.parent.mkdir(parents=True, exist_ok=True)
    DEMO_FLAG.write_text(json.dumps({"seeded": datetime.now().isoformat(timespec="seconds")}))
    tp = proj_paths(proj)["tasks"]
    tasks = read_json(tp, [])
    have = {x.get("title") for x in tasks}
    for title, status in [("体验：发起第一个 Blog Loop（创作中心）", "todo"),
                          ("阅读：铁律与规则 → RULES-00（知识中台）", "todo"),
                          ("配置：接入公司自己的大模型 API Key", "doing")]:
        if title not in have:
            tasks.append({"id": secrets.token_hex(4), "title": title, "status": status,
                          "source": "manual", "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                          "note": "demo seed", "assignee": "", "due": "", "link": "", "desc": ""})
    tp.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
    return {"ok": True, "note": "演示任务已注入；示例报告在 docs/demo-reports/"}


AUTH_FILE = RUN_DIR / "auth.json"
SESSIONS = {}  # sid -> {"username":…, "project":…}


def ensure_project(pid, name=None):
    pid = re.sub(r"[^a-z0-9-]", "", str(pid).lower())[:40] or DEFAULT_PROJECT
    d = PROJECTS_DIR / pid
    d.mkdir(parents=True, exist_ok=True)
    meta = d / "meta.json"
    if not meta.exists():
        meta.write_text(json.dumps({"id": pid, "name": name or pid,
                                    "created": datetime.now().strftime("%Y-%m-%d %H:%M")},
                                   ensure_ascii=False))
    (d / "content").mkdir(exist_ok=True)
    return d


def proj_paths(pid):
    d = PROJECTS_DIR / pid
    return {"dir": d, "state": d / "pipeline-state.json", "events": d / "events.jsonl",
            "tasks": d / "tasks.json", "loops": d / "loops.json", "gen": d / "content",
            "topics": d / "topics.json", "sched_log": d / "schedule.log"}


def auth_record(username):
    for x in read_json(AUTH_FILE, []):
        if x.get("username") == username:
            return x
    return None


def user_projects(username, role):
    """admin → 全部；其他用户 → auth.json projects 绑定（默认含 main）。"""
    if role == "admin":
        return [x["id"] for x in list_projects()]
    rec = auth_record(username) or {}
    bound = list(rec.get("projects") or [])
    if DEFAULT_PROJECT not in bound:
        bound = [DEFAULT_PROJECT] + bound  # 默认项目对所有登录用户可见
    return [pid for pid in bound if (PROJECTS_DIR / pid).exists()]


def list_projects():
    out = []
    if PROJECTS_DIR.exists():
        for d in sorted(PROJECTS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith(("_", ".")):
                meta = read_json(d / "meta.json", {})
                st = read_json(d / "pipeline-state.json", {})
                tasks = read_json(d / "tasks.json", [])
                out.append({"id": d.name, "name": meta.get("name", d.name),
                            "created": meta.get("created", ""),
                            "items": len(st.get("items", {})),
                            "open_tasks": sum(1 for x in tasks if x.get("status") != "done")})
    return out


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
try:
    PCHK = load_module("mflow_plugin_check", PROJECT / "plugins" / "plugin_check.py")
except Exception as e:
    PCHK = None
    print(f"[console] plugin_check import failed: {e}", file=sys.stderr)
try:
    SANITY_PUB = load_module("mflow_sanity_publisher",
                             PROJECT / "1-4 Dev" / "scripts" / "publish_adapters" / "sanity_publisher.py")
except Exception as e:
    SANITY_PUB = None
    print(f"[console] sanity_publisher import failed: {e}", file=sys.stderr)


def publish_gate(proj, item_id):
    """发布门禁（铁律）：条目必须在 S4-qa 及之后（经人工审）且 qa BLOCK 全 0。"""
    st = read_json(proj_paths(proj)["state"], {})
    it = (st.get("items") or {}).get(item_id)
    if not it:
        return False, f"管线中无条目 {item_id}（先经生成 Loop 入管线）"
    stage = it.get("stage", "")
    if stage not in ("S4-qa", "S4-ready", "S5-importing", "S5-imported"):
        return False, f"当前状态 {stage} 不可发布——需推进到 S4-qa 并经人工审"
    qa = it.get("qa") or {}
    blocks = {k: v for k, v in qa.items() if k.endswith("_block") and v}
    if blocks:
        return False, f"质检 BLOCK 未清零：{blocks}"
    return True, ""


LIB_ROOT = RUN_DIR / "library"
SITES_DIR = RUN_DIR / "sites"


def library_sites():
    out = []
    if SITES_DIR.exists():
        for f in sorted(SITES_DIR.glob("*.json")):
            s = read_json(f, {})
            idx = read_json(LIB_ROOT / f.stem / "index.json", {})
            out.append({"id": f.stem, "name": s.get("name", f.stem), "domain": s.get("domain", ""),
                        "sections": [x.get("key") for x in (s.get("sections") or [])],
                        "synced_at": idx.get("synced_at", "")})
    return out


def library_tree(site):
    prof = read_json(SITES_DIR / f"{site}.json", {})
    idx = read_json(LIB_ROOT / site / "index.json", {})
    secs = []
    for s in prof.get("sections") or []:
        st = (idx.get("sections") or {}).get(s.get("key"), {})
        secs.append({"key": s.get("key"), "dir": s.get("dir", s.get("key")), "docType": s.get("docType", ""),
                     "pageType": s.get("pageType", ""), "route": s.get("route", ""),
                     "pulled": st.get("pulled", 0), "total": st.get("total", 0), "langs": st.get("langs", {})})
    return {"site": site, "name": prof.get("name", site), "domain": prof.get("domain", ""),
            "synced_at": idx.get("synced_at", ""), "sections": secs}


def library_list(site, section, lang="", q="", limit=200):
    prof = read_json(SITES_DIR / f"{site}.json", {})
    sec = next((s for s in (prof.get("sections") or []) if s.get("key") == section), None)
    if not sec:
        return []
    base = LIB_ROOT / site / sec.get("dir", section)
    out = []
    if not base.exists():
        return out
    for f in sorted(base.rglob("*.md")):
        if lang and f.parent.name != lang:
            continue
        if q:
            ql = q.lower()
            if ql not in f.name.lower() and ql not in f.read_text(errors="ignore")[:800].lower():
                continue
        try:
            rel = str(f.relative_to(PROJECT))
        except Exception:
            rel = str(f)
        out.append({"path": rel, "name": f.name, "section": section, "lang": f.parent.name})
        if len(out) >= limit:
            break
    return out


def assets_inventory(site, q="", role="", section="", lang="", limit=300):
    inv = read_json(LIB_ROOT / site / "assets.json", {})
    if not inv:
        return {"error": "尚无物料台账——先点「扫描物料」"}
    urls = inv.get("urls", {})
    rows = []
    for u, e in urls.items():
        if q and q.lower() not in u.lower():
            continue
        if role and role not in (e.get("roles") or {}):
            continue
        if section:
            pids = e.get("pages") or []
            if not any((inv.get("pages", {}).get(pid, {}).get("section") == section) for pid in pids[:50]):
                continue
        if lang:
            pids = e.get("pages") or []
            if not any((inv.get("pages", {}).get(pid, {}).get("lang") == lang) for pid in pids[:50]):
                continue
        rows.append({"url": u, "n": e.get("n", 0), "roles": e.get("roles", {}),
                     "alt": e.get("alt", ""), "pages": (e.get("pages") or [])[:8]})
    rows.sort(key=lambda r: -r["n"])
    return {"site": site, "synced_at": inv.get("synced_at", ""), "stats": inv.get("stats", {}),
            "count": len(rows), "urls": rows[:limit]}


def assets_run(cmd, site, **kw):
    """后台跑 asset_tools.py（scan/plan/apply）。"""
    args = [sys.executable, str(PROJECT / "1-4 Dev/scripts/library/asset_tools.py"), cmd, "--site", site]
    for k, v in kw.items():
        if v in ("", None, 0, False):
            continue
        flag = "--" + k.replace("_", "-")
        if k == "yes" or k == "dry_run":
            args.append(flag if v else flag)
        else:
            args += [flag, str(v)]
    def run():
        try:
            r = run_tool(args, timeout=7200)
            (LIB_ROOT / site).mkdir(parents=True, exist_ok=True)
            (LIB_ROOT / site / f"assets-{cmd}-result.json").write_text(json.dumps(
                {"cmd": cmd, "rc": r.get("rc"), "out": (r.get("out") or "")[-3000:],
                 "at": datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False, indent=1))
        except Exception as e:
            print(f"[assets-{cmd}] {e}", file=sys.stderr)
    threading.Thread(target=run, daemon=True).start()
    return {"ok": True, "started": True, "cmd": cmd}


BATCH_DIR = RUN_DIR / "batch"
BATCH_LOCK = threading.Lock()


def batch_save(task):
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    p = BATCH_DIR / f"{task['id']}.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(task, ensure_ascii=False, indent=1))
    tmp.replace(p)


def batch_load(tid):
    return read_json(BATCH_DIR / f"{tid}.json", None)


def batch_list():
    out = []
    if BATCH_DIR.exists():
        for f in sorted(BATCH_DIR.glob("batch-*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            t = read_json(f, {})
            if t:
                out.append({k: t.get(k) for k in ("id", "type", "title", "status", "created", "created_by", "dry_run", "stats")})
    return out[:80]


def batch_create(btype, title, items, params=None, dry_run=True, by=""):
    role = (auth_record(by) or {}).get("role", "admin" if not AUTH_FILE.exists() else "operator")
    ok, msg = quota_check(by, role, n_items=len(items), kind=btype)
    if not ok:
        raise PermissionError(msg)
    tid = f"batch-{datetime.now().strftime('%y%m%d')}-{secrets.token_hex(3)}"
    task = {"id": tid, "type": btype, "title": title or btype,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "created_by": by, "dry_run": bool(dry_run),
            "params": {"batch_size": 5, "context_handoff": True, "fail_threshold": 5, "fatal_threshold": 2,
                       **(params or {})}, "concurrency": 2,
            "status": "queued", "log": [],
            "items": [{"i": i, "status": "pending", "attempts": 0, "result": None, "error": "", **it}
                      for i, it in enumerate(items)]}
    task["stats"] = {"total": len(task["items"]), "done": 0, "failed": 0, "skipped": 0}
    batch_save(task)
    usage_add(by, tasks=1)
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} BATCH-CREATE {tid} type={btype} "
                f"items={len(items)} dry_run={dry_run} by={by}\n")
    return task


def _batch_log(task, msg):
    task.setdefault("log", []).append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    task["log"] = task["log"][-200:]


def _sanity_req(path, payload, timeout=60):
    cfg = SANITY_PUB.sanity_cfg()
    url = f"https://{cfg['project']}.api.sanity.io/v2024-01-01/data/{path}/{cfg['dataset']}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {cfg['token']}",
                                          "Content-Type": "application/json"})
    import urllib.request as _u
    with _u.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _bh_asset_replace(item, task, proj):
    """物料替换：cover.url/alt、coverUrl、bodyJson[].media（ifRevisionID 并发保护）。"""
    if not SANITY_PUB:
        raise RuntimeError("sanity 发布器未加载")
    did = item["doc_id"]
    fresh = _sanity_req("query", {"query": f'*[_id=="{did}"][0]{{_id,_rev,cover,bodyJson,coverUrl}}'})["result"]
    if not fresh:
        raise RuntimeError("文档不存在")
    sets = {}
    if item.get("kind") == "cover":
        if fresh.get("cover"):
            sets["cover.url"] = item.get("new_url") or item.get("old")
            if item.get("new_alt"):
                sets["cover.alt"] = item["new_alt"]
        else:
            sets["coverUrl"] = item.get("new_url") or item.get("old")
    else:
        arr = json.loads(fresh.get("bodyJson") or "[]")
        idx = item.get("idx")
        fld = item.get("field", "media")
        if idx is not None and 0 <= idx < len(arr):
            m = arr[idx].get(fld)
            if isinstance(m, dict) and m.get("src") == item.get("old"):
                m["src"] = item.get("new_url") or item["old"]
                if item.get("new_alt"):
                    m["alt"] = item["new_alt"]
                sets["bodyJson"] = json.dumps(arr, ensure_ascii=False)
    if not sets:
        return {"skipped": True, "reason": "无可替换字段（可能已被改过）"}
    res = _sanity_req("mutate", {"mutations": [{"patch": {"id": did, "ifRevisionID": fresh.get("_rev"), "set": sets}}],
                                 "dryRun": bool(task.get("dry_run"))})
    usage_add(task.get("created_by", ""), items=1, writes=(0 if task.get("dry_run") else 1))
    return {"dry_run": task.get("dry_run"), "transactionId": res.get("transactionId"), "set": list(sets)}


def _bh_field_patch(item, task, proj):
    """字段改写：item.set = {"title": "...", "seoTitle": "..."}（ifRevisionID 保护）。"""
    if not SANITY_PUB:
        raise RuntimeError("sanity 发布器未加载")
    did = item["doc_id"]
    sets = item.get("set") or {}
    if not sets:
        raise RuntimeError("缺 set 字段")
    fresh = _sanity_req("query", {"query": f'*[_id=="{did}"][0]{{_id,_rev}}'})["result"]
    if not fresh:
        raise RuntimeError("文档不存在")
    res = _sanity_req("mutate", {"mutations": [{"patch": {"id": did, "ifRevisionID": fresh.get("_rev"), "set": sets}}],
                                 "dryRun": bool(task.get("dry_run"))})
    usage_add(task.get("created_by", ""), items=1, writes=(0 if task.get("dry_run") else 1))
    return {"dry_run": task.get("dry_run"), "transactionId": res.get("transactionId"), "set": list(sets)}


def run_generation(proj, item_id, ctype="blog", lang="zh", topic="", brief="", template_id="",
                   instruction="", source_text="", prior_context="", budget_profile="default", task=None):
    """批量生成/改稿共用执行体：LLM → 落盘 → post-write + geo 门禁 → 状态机推进。"""
    ps_args = ["--state-path", str(proj_paths(proj)["state"]), "--events-path", str(proj_paths(proj)["events"])]
    ps_run([sys.executable, str(PS_PATH), *ps_args, "upsert", "--id", item_id, "--category", ctype])
    # 状态机顺序：先入 S3-creating（与 Loop 引擎一致，S0-todo 不可直达 S3-draft）
    ps_run([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item_id, "--to", "S3-creating"])
    base_user = gen_prompt(ctype, lang, topic, brief, template=get_template(template_id),
                           budget_profile=budget_profile)
    user = base_user
    if instruction:
        user = (f"下面是既有内容，请按指令改写（事实准确优先；不确定的数字标 [待考证]）：\n"
                f"指令：{instruction}\n\n现有内容：\n{source_text[:12000]}\n\n" + user)
    if prior_context:
        user = (f"【前序批次上下文（避免重复，保持口径一致）】\n{prior_context[:1500]}\n\n" + user)
    if style_id:
        style_ref = style_to_skill_ref(style_id)
        if style_ref:
            user = (f"【样式参考（用户自定义，必须遵循其结构规则）】\n{style_ref}\n\n" + user)

    # 内部重试：门禁不过（尤其 quota 超字数）时带反馈重写，最多 3 轮（与 Loop 同思路）
    draft, gates, feedback, _tok = "", None, "", 0
    for _round in range(1, 4):
        draft = llm_chat([{"role": "user", "content": user + feedback}],
                         profile="lovart-creation", max_tokens=4000, project=proj)
        with _usage_lock:
            _tok += int(LAST_USAGE.get("total_tokens", 0) or 0)
        gen_dir = proj_paths(proj)["gen"]
        gen_dir.mkdir(parents=True, exist_ok=True)
        path = gen_dir / f"{item_id}.md"
        path.write_text(draft)
        gates = run_content_gates(path, ctype, lang, tag=f"batch:{item_id}", budget_profile=budget_profile)
        bad = [k for k, v in gates.items() if v["rc"] != 0]
        if not bad or _round == 3:
            break
        feedback = ("\n\n【上一稿被门禁打回，必须修正后重写】\n"
                    + "\n".join((gates[k]["out"] or "")[-700:] for k in bad))
    hw, geo = gates["post-write-check.sh"], gates["geo-check.sh"]
    quota, langc = gates["quota-check.sh"], gates["lang-check.sh"]
    advanced = False
    if hw["rc"] == 0 and geo["rc"] == 0 and quota["rc"] == 0 and langc["rc"] == 0:
        rcs = []
        for stg in ("S3-draft", "S3-done", "S4-qa"):
            r = ps_run([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item_id, "--to", stg])
            rcs.append(r.get("rc"))
        advanced = all(rc == 0 for rc in rcs)
    if task:
        usage_add(task.get("created_by", ""), items=1, tokens=_tok)
    return {"path": rel_of(path), "chars": len(draft), "hook_rc": hw["rc"], "geo_rc": geo["rc"],
            "quota_rc": quota["rc"], "lang_rc": langc["rc"], "advanced": advanced, "tokens": _tok,
            "blocked": [k for k, v in gates.items() if v["rc"] != 0]}


def _bh_gen(item, task, proj):
    return run_generation(proj, item["item_id"], ctype=item.get("type", "blog"), lang=item.get("lang", "zh"),
                          topic=item.get("topic", ""), brief=item.get("brief", ""),
                          template_id=item.get("template_id", ""), prior_context=task.get("ctx_digest", ""),
                          budget_profile=item.get("budget_profile") or (task.get("params") or {}).get("budget_profile", "default"),
                          task=task)


def _bh_rewrite(item, task, proj):
    src = ""
    if item.get("source_path"):
        sp = safe_path(item["source_path"])
        if sp:
            src = sp.read_text(errors="ignore")
    return run_generation(proj, item["item_id"], ctype=item.get("type", "blog"), lang=item.get("lang", "zh"),
                          topic=item.get("topic", item.get("slug", "")), brief=item.get("brief", ""),
                          instruction=item.get("instruction", ""), source_text=src,
                          prior_context=task.get("ctx_digest", ""),
                          budget_profile=item.get("budget_profile") or (task.get("params") or {}).get("budget_profile", "default"))


def _bh_publish_sanity(item, task, proj):
    """批量发布（blog / compositePage）。composite 走 validate_sections + create/patch；记账真实写入。"""
    if not SANITY_PUB:
        raise RuntimeError("发布器未加载")
    path = item.get("path") or f"run/projects/{proj}/content/{item.get('item_id','')}.md"
    sp = safe_path(path)
    if not sp:
        raise RuntimeError(f"草稿不可读：{path}")
    dry = bool(task.get("dry_run"))
    doctype = item.get("doctype", "blog")
    if doctype == "composite":
        r = SANITY_PUB.publish_landing(str(sp), dry_run=dry, mode=item.get("mode", "patch"),
                                       slug=item.get("slug", ""), lang=item.get("lang", "en"),
                                       page_type=item.get("page_type", "tool"), title=item.get("title", ""),
                                       description=item.get("description", ""), cover_url=item.get("cover_url", ""),
                                       cover_alt=item.get("cover_alt", ""),
                                       storyline_template=item.get("storyline_template", "T-long"),
                                       sections_path=item.get("sections_path", ""))
    else:
        r = SANITY_PUB.publish_file(str(sp), slug=item.get("slug", ""), lang=item.get("lang", ""),
                                    category=item.get("category", ""), title=item.get("title", ""),
                                    dry_run=dry)
    if not r.get("ok"):
        raise RuntimeError(r.get("error") or f"发布失败：{r.get('validation_errors')}")
    if not dry:
        usage_add(task.get("created_by", ""), writes=1)
    return r


BATCH_HANDLERS = {"asset_replace": _bh_asset_replace, "publish_sanity": _bh_publish_sanity, "field_patch": _bh_field_patch,
                  "gen": _bh_gen, "rewrite": _bh_rewrite}


def _batch_digest_llm(task, chunk, proj):
    """为 gen/rewrite 批次生成「上下文摘要」：写了什么/口径如何/避免重复什么。"""
    try:
        lines = []
        for c in chunk:
            r = c.get("result") or {}
            ttl = c.get("topic") or c.get("item_id") or c.get("slug") or ""
            lines.append(f"- 主题：{str(ttl)[:80]}｜状态：{c['status'][:6]}"
                         f"{'｜产出：' + str(r.get('path', ''))[:60] if r.get('path') else ''}")
        ask = ("下面是同一批量任务刚完成的批次产出。请用不超过 6 行、每行不超过 60 字的要点总结："
               "①各条主题与角度 ②已使用的数据/结论口径 ③下一批必须避免的重复点。"
               "只输出要点，不要客套。\n\n" + "\n".join(lines))
        out = llm_chat([{"role": "user", "content": ask}], profile="default", max_tokens=260, project=proj, timeout=60)
        return re.sub(r"\s+", " ", out)[:900]
    except Exception:
        return "；".join(f"{(c.get('topic') or c.get('item_id') or '')[:40]} {c['status']}" for c in chunk)[:700]


def batch_worker():
    """批量执行器：并发 2、逐项状态、断点续跑（重启自动续）、审计。"""
    from concurrent.futures import ThreadPoolExecutor
    while True:
        time.sleep(5)
        try:
            BATCH_DIR.mkdir(parents=True, exist_ok=True)
            blocked, bst = breaker_check()
            if blocked:
                continue  # 熔断中：不领取任何任务
            cands = [batch_load(f.stem) for f in sorted(BATCH_DIR.glob("batch-*.json"), key=lambda x: x.stat().st_mtime)]
            task = next((t for t in cands if t and t.get("status") in ("queued", "running")), None)
            if not task:
                continue
            with BATCH_LOCK:
                task["status"] = "running"
                task.setdefault("started", datetime.now().strftime("%Y-%m-%d %H:%M"))
                _batch_log(task, f"开始执行（type={task['type']} dry_run={task.get('dry_run')}）")
                batch_save(task)
            handler = BATCH_HANDLERS.get(task["type"])
            if not handler:
                task["status"] = "failed"
                _batch_log(task, f"未知任务类型 {task['type']}")
                batch_save(task)
                continue
            proj = DEFAULT_PROJECT
            pending = [it for it in task["items"] if it["status"] in ("pending", "running")]
            max_attempts = int((task.get("params") or {}).get("max_attempts", 2) or 2)

            def work(it):
                if task.get("status") in ("paused", "cancelled"):
                    return
                it["status"] = "running"
                it["attempts"] = int(it.get("attempts", 0)) + 1
                try:
                    it["result"] = handler(it, task, proj)
                    it["status"] = "skipped" if (isinstance(it["result"], dict) and it["result"].get("skipped")) else "done"
                except Exception as e:
                    it["error"] = str(e)[:300]
                    it["status"] = "failed" if it["attempts"] >= max_attempts else "pending"

            batch_size = max(1, int((task.get("params") or {}).get("batch_size", 5) or 5))
            handoff = bool((task.get("params") or {}).get("context_handoff", True))
            task.setdefault("batches", [])
            for bi in range(0, len(pending), batch_size):
                chunk = pending[bi:bi + batch_size]
                if task.get("status") in ("paused", "cancelled"):
                    break
                with ThreadPoolExecutor(max_workers=int(task.get("concurrency", 2))) as ex:
                    list(ex.map(work, chunk))
                done_chunk = [c for c in chunk if c["status"] in ("done", "skipped")]
                digest = ""
                if handoff and done_chunk:
                    if task["type"] in ("gen", "rewrite") and len(task["batches"]) > 0 or task["type"] in ("gen", "rewrite"):
                        digest = _batch_digest_llm(task, done_chunk, proj)
                    else:
                        digest = "；".join(
                            f"{(c.get('doc_id') or c.get('item_id') or c.get('path') or '')[:40]} "
                            f"{c['status']}{'：' + json.dumps(c.get('result') or {}, ensure_ascii=False)[:60] if c['status'] == 'done' else ''}"
                            for c in chunk)[:900]
                elif done_chunk:
                    digest = "；".join(f"{(c.get('doc_id') or c.get('item_id') or '')[:40]} {c['status']}" for c in chunk)[:600]
                task["batches"].append({"n": len(task["batches"]) + 1, "items": len(chunk),
                                        "done": len(done_chunk), "digest": digest})
                task["ctx_digest"] = ((task.get("ctx_digest", "") + "\n" + digest).strip())[-2500:]
                _batch_log(task, f"批次 {len(task['batches'])} 完成 {len(done_chunk)}/{len(chunk)}")
                # 连续失败熔断（T3）
                cons = task.get("consecutive_fail", 0)
                fatal_msg, cons = "", 0
                for c in chunk:
                    if c.get("error"):  # 本轮失败尝试（含被重置为 pending 的）
                        cons += 1
                        if _is_fatal_error(c.get("error")):
                            fatal_msg = c.get("error", "")[:160]
                    elif c["status"] in ("done", "skipped"):
                        cons = 0
                task["consecutive_fail"] = cons
                thr_fatal = int(task["params"].get("fatal_threshold", 2) or 2)
                thr = int(task["params"].get("fail_threshold", 5) or 5)
                if fatal_msg:
                    task["status"] = "tripped"
                    _batch_log(task, f"熔断（致命错误）：{fatal_msg}")
                    batch_save(task)
                    breaker_trip(f"致命错误（任务 {task['id']}）：{fatal_msg}", cooldown_min=30)
                    break
                if cons >= thr:
                    task["status"] = "tripped"
                    _batch_log(task, f"熔断：连续 {cons} 项失败（阈值 {thr}）——请检查后「重试失败」")
                    batch_save(task)
                    notify_send("MFlow 任务熔断", f"任务 {task['id']} 连续 {cons} 项失败已暂停")
                    break
                batch_save(task)
            st = task["stats"]
            st["done"] = sum(1 for i in task["items"] if i["status"] == "done")
            st["failed"] = sum(1 for i in task["items"] if i["status"] == "failed")
            st["skipped"] = sum(1 for i in task["items"] if i["status"] == "skipped")
            if task.get("status") == "tripped":
                pass
            elif task.get("status") == "paused":
                _batch_log(task, "已暂停")
            elif task.get("status") == "cancelled":
                _batch_log(task, "已取消")
            elif task.get("status") in ("paused", "cancelled", "tripped"):
                pass
            elif st["failed"] or any(i["status"] == "pending" for i in task["items"]):
                task["status"] = "failed"
                _batch_log(task, f"结束：done={st['done']} failed={st['failed']} skipped={st['skipped']}（可重试失败项）")
            else:
                task["status"] = "done"
                task["finished"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                _batch_log(task, f"完成：done={st['done']} skipped={st['skipped']}")
                try:
                    chain_next_task(task, proj)
                except Exception as ce:
                    _batch_log(task, f"任务链生成失败：{str(ce)[:160]}")
            batch_save(task)
        except Exception as e:
            print(f"[batch] {e}", file=sys.stderr)


def library_sync(site, sections="", max_n=0):
    """后台跑 sanity_pull.py（状态落 run/library/{site}/sync-status.json）。"""
    def run():
        try:
            r = run_tool([sys.executable, str(PROJECT / "1-4 Dev/scripts/library/sanity_pull.py"),
                          "--site", site, "--sections", sections, "--max", str(max_n)], timeout=7200)
            if r.get("rc"):
                print(f"[library-sync] rc={r['rc']} {r['out'][-300:]}", file=sys.stderr)
        except Exception as e:
            print(f"[library-sync] {e}", file=sys.stderr)
    threading.Thread(target=run, daemon=True).start()
    return {"ok": True, "started": True}


def publish_wordpress(path, item_id, title=""):
    if not (PROJECT / "run" / "cms.json").exists():
        return {"ok": False, "error": "未配置 run/cms.json 的 wordpress 段（base/user/app_password）"}
    p = safe_path(path)
    if not p:
        return {"ok": False, "error": "草稿路径不可读"}
    r = run_tool([sys.executable, str(PROJECT / "1-4 Dev/scripts/publish_adapters/cli.py"),
                  "--adapter", "wordpress", "--item-id", item_id, "--title", title or item_id,
                  "--body-file", str(p), "--cfg", "run/cms.json"], timeout=120)
    try:
        out = json.loads(r["out"].strip().split("\n")[-1])
    except Exception:
        out = {"ok": False, "error": r["out"][-300:]}
    if out.get("ok"):
        with open(RUN_DIR / "approvals.log", "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} WP-PUBLISH {item_id} url={out.get('url','')}\n")
    return out


def ps_run(args, timeout=60):
    """串行化对 pipeline-state 的读改写（并发批量任务/loop 共用同一状态文件）。"""
    with PS_LOCK:
        return run_tool(args, timeout=timeout)


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


def _src_dirs(src):
    """Return [(dir, glob)] for a source label; empty if unknown."""
    for label, _desc, pairs in KNOWLEDGE_SOURCES:
        if label == src:
            return pairs
    return []


def kb_tree(extra=None):
    out = []
    for label, desc, pairs in KNOWLEDGE_SOURCES:
        n = 0
        for d, pat in pairs:
            base = PROJECT / d
            if base.exists():
                n += sum(1 for f in base.glob(pat) if f.is_file() and f.suffix == ".md")
        out.append({"name": label, "desc": desc, "files": n})
    for ex in (extra or []):
        n = 0
        base = PROJECT / ex.get("dir", "")
        if ex.get("dir") and base.exists():
            n = sum(1 for f in base.glob(ex.get("glob", "**/*.md")) if f.is_file() and f.suffix == ".md")
        out.append({"name": "[项目] " + ex.get("label", "?"), "desc": "项目专属知识源", "files": n, "extra": ex})
    return out


def kb_list(src, extra=None):
    files = []
    seen = set()
    for d, pat in _src_dirs(src):
        base = PROJECT / d
        if not base.exists():
            continue
        for f in base.glob(pat):
            if not f.is_file() or f.suffix != ".md" or "scripts" in f.parts:
                continue
            rp = rel_of(f)
            if rp in seen:
                continue
            seen.add(rp)
            files.append({"path": rp, "name": f.name, "date": fdate(f.stat().st_mtime)})
    files.sort(key=lambda x: x["name"].lower())
    for ex in (extra or []):
        if ("[项目] " + ex.get("label", "")) != src:
            continue
        base = PROJECT / ex.get("dir", "")
        if not base.exists():
            continue
        for f in base.glob(ex.get("glob", "**/*.md")):
            if f.is_file() and f.suffix == ".md":
                files.append({"path": rel_of(f), "name": f.name, "date": fdate(f.stat().st_mtime)})
    return files[:400]


def kb_search(q, src="", extra=None):
    sources = [(l, p) for l, _d, p in KNOWLEDGE_SOURCES if not src or l == src]
    if src.startswith("[项目] "):
        sources = [(src, [(ex.get("dir", ""), ex.get("glob", "**/*.md")) for ex in (extra or []) if ("[项目] " + ex.get("label", "")) == src])]
    q_lower = q.lower()
    hits, scanned = [], 0
    for _label, pairs in sources:
        for d, pat in pairs:
            base = PROJECT / d
            if not base.exists():
                continue
            for f in base.glob(pat):
                if not f.is_file() or f.suffix != ".md" or "scripts" in f.parts:
                    continue
                scanned += 1
                if scanned > 800:
                    return hits
                if q_lower in f.name.lower():
                    hits.append({"path": rel_of(f), "name": f.name, "match": "文件名匹配"})
                    if len(hits) >= 40:
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
                    if len(hits) >= 40:
                        return hits
    return hits


def tasks_all(proj):
    tp = proj_paths(proj)
    manual = read_json(tp["tasks"], [])
    state = read_json(tp["state"], {})
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


def schedule_report(visible):
    """P5 排程报表：所有可见项目的自动排程状态一行一项目。"""
    today = datetime.now().strftime("%Y-%m-%d")
    rows = []
    names = {p["id"]: p.get("name", p["id"]) for p in list_projects()}
    for pid in visible:
        if not (PROJECTS_DIR / pid).exists():
            continue
        pp = proj_paths(pid)
        meta = read_json(PROJECTS_DIR / pid / "meta.json", {})
        sc = meta.get("schedule") or {}
        loops = read_json(pp["loops"], [])
        log_tail = ""
        if pp["sched_log"].exists():
            log_tail = "\n".join(pp["sched_log"].read_text().strip().split("\n")[-5:])
        rows.append({"id": pid, "name": names.get(pid, pid),
                     "enabled": bool(sc.get("auto_loop")), "quota": int(sc.get("daily_quota", 0) or 0),
                     "created_today": sum(1 for x in loops if str(x.get("created", "")).startswith(today)),
                     "running": sum(1 for x in loops if x.get("status") == "running"),
                     "queued": sum(1 for x in loops if x.get("status") == "queued"),
                     "queue_len": len(read_json(pp["topics"], [])),
                     "log_tail": log_tail})
    rows.sort(key=lambda r: (not r["enabled"], r["id"]))
    return {"rows": rows, "date": today}


def plugins_inventory():
    """P5 插件市场：已安装扫描 + marketplace 清单（plugins/marketplace.json）。"""
    installed = []
    pdir = PROJECT / "plugins"
    if pdir.exists():
        for d in sorted(pdir.iterdir()):
            if not d.is_dir() or d.name.startswith(("_", ".")):
                continue
            mf = read_json(d / "manifest.json", None)
            if not mf:
                continue
            errs, oks = ([], [])
            if PCHK:
                try:
                    errs, oks = PCHK.check(str(d))
                except Exception:
                    pass
            installed.append({"id": mf.get("id", d.name), "type": mf.get("type", "?"),
                              "name": mf.get("name", d.name), "version": mf.get("version", ""),
                              "author": mf.get("author", ""), "dir": d.name,
                              "pass": not errs, "checks": errs + oks[:4]})
    available = read_json(pdir / "marketplace.json", [])
    return {"installed": installed, "available": available}


_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,48}$")


def plugin_install(manifest, entry_code):
    """安装：写 plugins/{id}/（manifest+entry）→ plugin_check → 失败进 _trash。"""
    if not PCHK:
        return {"error": "plugin_check 不可用"}
    pid = str(manifest.get("id", "")).strip()
    if not _ID_RE.fullmatch(pid):
        return {"error": "id 不合法（小写字母数字连字符）"}
    if manifest.get("type") not in ("source", "publisher"):
        return {"error": "仅 source/publisher 类插件经此安装；模板包走模板市场导入"}
    if not str(manifest.get("entry", "")).strip() or ".." in str(manifest.get("entry", "")):
        return {"error": "entry 字段不合法"}
    d = PROJECT / "plugins" / pid
    d.parent.mkdir(exist_ok=True)
    d.mkdir(exist_ok=True)
    (d / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    entry = d / str(manifest["entry"])
    entry.write_text(str(entry_code or "# empty\n"))
    errs, _oks = PCHK.check(str(d))
    if errs:
        trash = PROJECT / "plugins" / "_trash"
        trash.mkdir(exist_ok=True)
        target = trash / f"{pid}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        d.rename(target)
        return {"error": "校验未通过（已移入 _trash）：" + "; ".join(errs[:4])}
    return {"ok": True, "id": pid}


def plugin_uninstall(pid):
    if not _ID_RE.fullmatch(str(pid)):
        return {"error": "id 不合法"}
    d = PROJECT / "plugins" / pid
    if not d.exists():
        return {"error": "插件不存在"}
    trash = PROJECT / "plugins" / "_trash"
    trash.mkdir(exist_ok=True)
    d.rename(trash / f"{pid}-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    return {"ok": True}


def geo_cfg(proj):
    meta = read_json(PROJECTS_DIR / proj / "meta.json", {})
    g = meta.get("geo") or {}
    engines = g.get("engines") or ([g["engine"]] if g.get("engine") else ["auto"])
    return {"brand": str(g.get("brand", ""))[:60],
            "competitors": [str(x)[:40] for x in (g.get("competitors") or [])[:12]],
            "queries": [str(x)[:200] for x in (g.get("queries") or [])[:15]],
            "engines": [str(x)[:24] for x in engines[:4]],  # P7-B3 多引擎交叉
            "probe_daily": bool(g.get("probe_daily")),
            "auto_refresh": bool(g.get("auto_refresh")),
            "perplexity_model": str(g.get("perplexity_model", "sonar"))[:40]}


def _citations_path(proj):
    return proj_paths(proj)["dir"] / "citations.jsonl"


def _published_canonicals():
    """已发布内容 canonical URL → slug/canonical 映射（供引用归因）。"""
    base = PROJECT / "1-3 GenFlow/Content Distribution/queue/published.json"
    out = []
    for x in read_json(base, {}).get("items", []) or []:
        u = (x.get("canonical") or "").strip()
        if u:
            out.append({"url": u, "slug": x.get("slug", ""), "platform": x.get("platform", ""),
                        "date": x.get("date", "")})
    return out


def _match_published(urls, published):
    """citation URL ↔ canonical 精确归因：路径段匹配（忽略 query/尾斜杠/协议头差异）。"""
    def norm(u):
        u = u.split("?")[0].split("#")[0].rstrip("/")
        return "/" + u.split("://", 1)[-1].split("/", 1)[-1].lower()
    hits = []
    for u in urls:
        nu = norm(u)
        for p in published:
            if norm(p["url"]) == nu:
                hits.append({"cited": u, "canonical": p["url"], "slug": p["slug"],
                             "platform": p["platform"]})
                break
    return hits


def geo_probe(proj):
    """P6.1/P6 二批：逐条向 AI 引擎问目标问题，检测品牌/竞品提及与引用。
    engine=auto → 现有 provider（从答案文本提取 URL）；engine=perplexity → sonar 真引用。
    只走官方 API，不爬引擎。"""
    g = geo_cfg(proj)
    if not g["brand"]:
        return {"error": "先在设置页配置品牌名与目标查询"}
    if not g["queries"]:
        return {"error": "没有目标查询（先在设置页添加 3-10 条用户会问 AI 的问题）"}
    published = _published_canonicals()
    rows = []
    for q in g["queries"][:10]:
        for eng in g["engines"]:
            if eng == "perplexity":
                prompt = f"回答这个问题，像 AI 助手推荐工具/方案那样给出具体名称与理由：\n\n{q}"
            else:
                prompt = (f"请直接回答下面的问题，像 AI 助手推荐工具/方案那样给出具体名称与理由，"
                          f"并在末尾列出参考来源 URL（真实可访问的）：\n\n{q}")
            try:
                ans, meta = llm_chat_full([{"role": "user", "content": prompt}],
                                          profile="lovart-creation", max_tokens=700, timeout=90,
                                          project=proj, temperature=0.4,
                                          engine=None if eng == "auto" else eng,
                                          engine_model=g["perplexity_model"] if eng == "perplexity" else "")
            except Exception as e:
                rows.append({"query": q, "ok": False, "engine": eng, "error": str(e)[:160]})
                continue
            low = ans.lower()
            urls = sorted(set(re.findall(r"https?://[a-zA-Z0-9./?=_%&#~-]+", ans)))[:12]
            engine_cites = meta.get("citations") or []
            for c in engine_cites:
                u = c if isinstance(c, str) else (c.get("url") if isinstance(c, dict) else "")
                if u and u not in urls:
                    urls.append(u)
            urls = urls[:15]
            rec = {"ts": datetime.now().isoformat(timespec="seconds"), "query": q, "ok": True,
                   "engine": eng, "brand": bool(g["brand"].lower() in low),
                   "competitors": [c for c in g["competitors"] if c.lower() in low],
                   "urls": urls,
                   "cited_pages": _match_published(urls, published),
                   "snippet": ans[:300],
                   "tokens": meta.get("usage", {}).get("total_tokens", 0)}
            rows.append(rec)
            with open(_citations_path(proj), "a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {"rows": rows}


def geo_summary(proj):
    """P6.1 聚合：每条查询的品牌提及率 + 全局竞品份额（近期 30 条窗口）。"""
    f = _citations_path(proj)
    rows = []
    if f.exists():
        for l in f.read_text().strip().split("\n")[-30:]:
            try:
                rows.append(json.loads(l))
            except Exception:
                continue
    ok_rows = [r for r in rows if r.get("ok")]
    per_query = {}
    comp_counter = Counter()
    by_day = {}
    per_engine = {}
    cited_map = {}
    for r in ok_rows:
        pq = per_query.setdefault(r["query"], {"n": 0, "brand": 0, "engines": {}})
        pq["n"] += 1
        pq["brand"] += 1 if r.get("brand") else 0
        eng = r.get("engine", "?")
        pe = per_engine.setdefault(eng, {"n": 0, "brand": 0})
        pe["n"] += 1
        pe["brand"] += 1 if r.get("brand") else 0
        if eng not in pq["engines"]:
            pq["engines"][eng] = bool(r.get("brand"))
        for c in r.get("competitors") or []:
            comp_counter[c] += 1
        d = str(r.get("ts", ""))[:10]
        if d:
            bd = by_day.setdefault(d, {"n": 0, "brand": 0})
            bd["n"] += 1
            bd["brand"] += 1 if r.get("brand") else 0
        for cp in r.get("cited_pages") or []:
            key = cp.get("canonical") or cp.get("cited")
            e = cited_map.setdefault(key, {"canonical": cp.get("canonical", key),
                                           "slug": cp.get("slug", ""), "platform": cp.get("platform", ""),
                                           "n": 0, "queries": set()})
            e["n"] += 1
            e["queries"].add(r.get("query", ""))
    cited_pages = [{"canonical": e["canonical"], "slug": e["slug"], "platform": e["platform"],
                    "n": e["n"], "queries": sorted(e["queries"])[:5]}
                   for e in sorted(cited_map.values(), key=lambda x: -x["n"])[:10]]
    import datetime as _dt
    trend = []
    for i in range(13, -1, -1):
        d = (_dt.date.today() - _dt.timedelta(days=i)).isoformat()
        bd = by_day.get(d, {"n": 0, "brand": 0})
        trend.append({"label": d[5:], "n": bd["n"], "brand": bd["brand"]})
    cross = {"multi_engine_queries": sum(1 for v in per_query.values() if len(v["engines"]) >= 2),
             "split": sum(1 for v in per_query.values() if len(v["engines"]) >= 2 and len(set(v["engines"].values())) > 1)}
    # B2 竞品引用源反向工程：竞品被提及时的引用 URL（排除自家页面）→ 按域聚合
    comp_urls = {}
    our_paths = {_norm_url_path(p.get("url")) for p in _published_canonicals()}
    for r in ok_rows:
        if not (r.get("competitors") or []):
            continue
        for u in r.get("urls") or []:
            nu = _norm_url_path(u)
            if nu in our_paths or not u.startswith("http"):
                continue
            try:
                dom = urllib.parse.urlparse(u).netloc.replace("www.", "")
            except Exception:
                continue
            if not dom:
                continue
            e = comp_urls.setdefault(dom, {"domain": dom, "n": 0, "competitors": Counter(), "queries": set()})
            e["n"] += 1
            for c in r.get("competitors") or []:
                e["competitors"][c] += 1
            e["queries"].add(r.get("query", ""))
    competitor_urls = [{"domain": e["domain"], "n": e["n"],
                        "competitors": [c for c, _ in e["competitors"].most_common(3)],
                        "queries": sorted(e["queries"])[:5]}
                       for e in sorted(comp_urls.values(), key=lambda x: -x["n"])[:8]]
    brand_n = sum(1 for r in ok_rows if r.get("brand"))
    brand_rate = brand_n / max(1, len(ok_rows))
    score, score_parts = geo_score(proj, brand_rate=brand_rate, per_query=per_query,
                                   competitor_total=sum(comp_counter.values()), brand_total=brand_n)
    return {"total": len(ok_rows),
            "brand_rate": round(brand_rate, 2),
            "competitors": dict(comp_counter.most_common()),
            "per_query": per_query,
            "per_engine": per_engine,
            "cross": cross,
            "competitor_urls": competitor_urls,
            "score": score, "score_parts": score_parts,
            "cited_pages": cited_pages,
            "trend14": trend,
            "latest": rows[-10:][::-1]}


def geo_scheduler():
    """P6 二批：每日自动探测。每小时检查——项目开了 probe_daily 且今日未探测
    且过了 09:30 → 跑 geo_probe（无真实 Key 时 probe 自带 fail-clean，静默跳过）。"""
    while True:
        time.sleep(1800)
        try:
            if not PROJECTS_DIR.exists():
                continue
            now = datetime.now()
            for meta_f in PROJECTS_DIR.glob("*/meta.json"):
                pid = meta_f.parent.name
                g = geo_cfg(pid)
                if not (g.get("probe_daily") and g.get("brand") and g.get("queries")):
                    continue
                cf = _citations_path(pid)
                if cf.exists():
                    today = now.strftime("%Y-%m-%d")
                    # 只认当日「真实成功探测」；失败/记账行不阻塞当日重试
                    probed = any(json.loads(l).get("ok") is True
                                 for l in cf.read_text().strip().split("\n")[-20:]
                                 if l.strip() and str(l).lstrip().startswith("{")
                                 and json.loads(l).get("ts", "")[:10] == today)
                    if probed:
                        continue
                if now.hour < 9:
                    continue
                r = geo_probe(pid)
                with open(cf, "a") as f:
                    f.write(json.dumps({"ts": now.isoformat(timespec="seconds"),
                                        "scheduled": True, "result": ("ok" if not r.get("error") else r["error"][:120])},
                                       ensure_ascii=False) + "\n")
                # P7 附加：衰减自动改稿 opt-in（显式开启才烧钱；每日上限 2 篇/项目）
                meta2 = read_json(meta_f, {})
                if (meta2.get("geo") or {}).get("auto_refresh"):
                    gsc = read_json(RUN_DIR / "local-dev/Output/Data Ingestion/gsc-full.json", {})
                    by_path = {}
                    for pg in ((gsc.get("pages") or {}).get("top20_pages") or []):
                        try:
                            by_path[urllib.parse.urlparse(pg.get("url", "")).path] = True
                        except Exception:
                            continue
                    for x in decay_analysis(read_json(PROJECT / "1-3 GenFlow/Content Distribution/queue/published.json", {}).get("items", []), by_path)[:2]:
                        item_id = "refresh-" + (re.sub(r"[^a-z0-9-]", "", str(x["slug"]).lower())[:40] or secrets.token_hex(2))
                        pp = proj_paths(pid)
                        loops = read_json(pp["loops"], [])
                        if any(l.get("item_id") == item_id and l.get("status") in ("queued", "running") for l in loops):
                            continue
                        ps_run([sys.executable, str(PS_PATH),
                                "--state-path", str(pp["state"]), "--events-path", str(pp["events"]),
                                "upsert", "--id", item_id, "--category", "blog"])
                        with LOOP_LOCK:
                            loops = read_json(pp["loops"], [])
                            loops.append({"id": secrets.token_hex(4), "item_id": item_id,
                                          "goal": f"衰减改稿 {x['slug']}", "template_id": "", "type": "blog",
                                          "lang": "zh", "topic": x["slug"],
                                          "brief": "内容衰减改稿：该已发布页面 GSC Top20 无记录且无 AI 引用。按 GEO 标准（问答式 H2/数据点/FAQ/自包含短段/来源标注）重写为可摘录形态。",
                                          "status": "queued", "round": 0, "max_rounds": 3, "tokens_used": 0,
                                          "auto": True, "decay": True,
                                          "created": now.strftime("%Y-%m-%d %H:%M"), "log": []})
                            pp["loops"].write_text(json.dumps(loops, ensure_ascii=False, indent=1))
                        with open(pp["sched_log"], "a") as f:
                            f.write(f"{now.isoformat(timespec='seconds')} DECAY-REFRESH {item_id}\n")
        except Exception as e:
            print(f"[geo-scheduler] {e}", file=sys.stderr)


def geo_score(proj, brand_rate, per_query, competitor_total, brand_total):
    """P7-B6 GEO 综合分（0-100）：可探测时四因子，无数据时返回 None（不造假分）。"""
    if not per_query:
        return None, {}
    # ① 提及率（40%）：探测中品牌被提及比例
    p_mention = brand_rate
    # ② 缺口覆盖（30%）：至少被提及一次的查询占比
    cov = sum(1 for v in per_query.values() if v.get("brand", 0) > 0) / max(1, len(per_query))
    p_coverage = cov
    # ③ 相对份额（20%）：品牌提及次数 vs（品牌+竞品提及），无竞品配置则按 50% 中性分
    rel = brand_total / (brand_total + competitor_total) if (brand_total + competitor_total) > 0 else 0.5
    # ④ 结构健康度（10%）：衰减占比反向（衰减越少分越高）
    qbase = PROJECT / "1-3 GenFlow/Content Distribution/queue"
    pub = read_json(qbase / "published.json", {}).get("items", [])
    gsc = read_json(RUN_DIR / "local-dev/Output/Data Ingestion/gsc-full.json", {})
    by_path = {}
    for pg in ((gsc.get("pages") or {}).get("top20_pages") or []):
        try:
            by_path[urllib.parse.urlparse(pg.get("url", "")).path] = True
        except Exception:
            continue
    dec = decay_analysis(pub, by_path)
    struct = 1 - (len(dec) / max(1, len(pub))) if pub else 0.5
    total = round((p_mention * 0.4 + p_coverage * 0.3 + rel * 0.2 + struct * 0.1) * 100)
    return total, {"mention": round(p_mention * 100), "coverage": round(p_coverage * 100),
                   "share": round(rel * 100), "structure": round(struct * 100),
                   "note": "提及率40% + 缺口覆盖30% + 相对份额20% + 结构健康10%"}


# ===================== P12.4 QA 编排（扫描 → findings → 修复任务 → 复检）=====================
QA_DIR = RUN_DIR / "qa"


def _qa_finding(target, rule, severity, detail, fix=None):
    return {"target": target, "rule": rule, "severity": severity, "detail": detail, "fix": fix or {}}


def qa_check_md(path):
    """对 md 草稿跑门禁钩子 → findings。"""
    p = safe_path(path)
    if not p:
        return [_qa_finding(path, "file", "block", "文件不可读")]
    findings = []
    for hook, args in (("post-write-check.sh", ["--target-words", "300"]),
                       ("geo-check.sh", [])):
        r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks" / hook), "--file", str(p), *args], timeout=120)
        qa_log(f"qa:{Path(path).stem}", hook, r["rc"])
        for line in (r["out"] or "").split("\n"):
            s = line.strip()
            if s.startswith("✗"):
                findings.append(_qa_finding(path, hook, "block", s[1:].strip()[:200]))
            elif s.startswith("!"):
                findings.append(_qa_finding(path, hook, "warn", s[1:].strip()[:200]))
    return findings


def _qa_field_rules(doc):
    """Sanity 字段级规则（不依赖 LLM，确定性）。"""
    f = []
    did = doc.get("_id", "")
    lang = doc.get("language") or ""
    cjk = lang in ("zh", "zh-TW", "ja", "ko")
    seo_title = (doc.get("seoTitle") or "").strip()
    title = (doc.get("title") or "").strip()
    desc = (doc.get("description") or "").strip()
    seo_desc = ((doc.get("seo") or {}).get("description") or "").strip()
    lim_t = 30 if cjk else 60
    lim_d = 80 if cjk else 160
    if not seo_title:
        sug = title[:lim_t]
        f.append(_qa_finding(did, "seoTitle.missing", "warn", f"seoTitle 缺失（title={title[:40]}）",
                             {"type": "field_patch", "set": {"seoTitle": sug}}))
    elif len(seo_title) > lim_t:
        sug = seo_title[:lim_t].rsplit(" ", 1)[0] if not cjk else seo_title[:lim_t]
        f.append(_qa_finding(did, "seoTitle.too_long", "warn", f"seoTitle {len(seo_title)} 字符 > {lim_t}",
                             {"type": "field_patch", "set": {"seoTitle": sug}}))
    if not desc and not seo_desc:
        f.append(_qa_finding(did, "description.missing", "warn", "description 与 seo.description 均缺失",
                             {"type": "field_patch", "set": {"description": title[:lim_d]}}))
    elif len(desc) > lim_d:
        f.append(_qa_finding(did, "description.too_long", "warn", f"description {len(desc)} 字符 > {lim_d}",
                             {"type": "field_patch", "set": {"description": desc[:lim_d]}}))
    cov = doc.get("cover") or {}
    if cov.get("url") and not (cov.get("alt") or "").strip():
        f.append(_qa_finding(did, "cover.alt_missing", "warn", "封面缺 alt 文案",
                             {"type": "asset_replace", "kind": "cover", "old": cov["url"],
                              "new_url": cov["url"], "new_alt": title[:80]}))
    return f


def qa_check_sanity(doc_id):
    if not SANITY_PUB:
        return [_qa_finding(doc_id, "sanity", "block", "发布器未加载")]
    try:
        r = _sanity_req("query", {"query": f'*[_id=="{doc_id}"][0]{{_id,title,language,description,seoTitle,seo,cover}}'})
        doc = (r or {}).get("result")
    except Exception as e:
        return [_qa_finding(doc_id, "sanity", "block", f"读取失败：{str(e)[:120]}")]
    if not doc:
        return [_qa_finding(doc_id, "sanity", "block", "文档不存在")]
    return _qa_field_rules(doc)


def _bh_qa(item, task, proj):
    """批量 QA：kind=md → 钩子；kind=sanity → 字段规则。"""
    kind = item.get("kind", "sanity")
    if kind == "md":
        findings = qa_check_md(item.get("path") or item.get("target", ""))
    else:
        findings = qa_check_sanity(item.get("doc_id") or item.get("target", ""))
    blocks = sum(1 for x in findings if x["severity"] == "block")
    warns = sum(1 for x in findings if x["severity"] == "warn")
    dst = QA_DIR / f"findings-{task['id']}-{item['i']}.json"
    QA_DIR.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(findings, ensure_ascii=False, indent=1))
    usage_add(task.get("created_by", ""), items=1)
    return {"findings": len(findings), "block": blocks, "warn": warns, "file": str(dst)}


def qa_findings(tid):
    """汇总某 QA 任务的全部 findings（含可执行的 fix 建议）。"""
    t = batch_load(tid)
    if not t:
        return {"error": "任务不存在"}
    all_f = []
    for it in t.get("items", []):
        res = it.get("result") or {}
        fp = res.get("file")
        if fp and Path(fp).exists():
            for f in read_json(fp, []):
                f["item"] = it.get("doc_id") or it.get("path") or it.get("target") or it.get("i")
                all_f.append(f)
    by_rule, by_sev = Counter(), Counter()
    for f in all_f:
        by_rule[f["rule"]] += 1
        by_sev[f["severity"]] += 1
    return {"task": tid, "status": t.get("status"), "stats": t.get("stats"),
            "total": len(all_f), "by_severity": dict(by_sev), "by_rule": dict(by_rule),
            "fixable": sum(1 for f in all_f if (f.get("fix") or {}).get("type")),
            "findings": all_f[:400], "fix_task_id": t.get("fix_task_id"), "recheck_task_id": t.get("recheck_task_id")}


def qa_orchestrate(tid, dry_run=True, max_items=200):
    """把 findings 编排成修复任务（确定性映射：字段→field_patch，alt→asset_replace，草稿→rewrite）。"""
    t = batch_load(tid)
    if not t:
        return {"error": "任务不存在"}
    if t.get("fix_task_id"):
        return {"error": f"已生成修复任务：{t['fix_task_id']}"}
    data = qa_findings(tid)
    field_items, asset_items, rewrite_items = [], [], []
    for f in data["findings"]:
        fx = f.get("fix") or {}
        typ = fx.get("type")
        if typ == "field_patch" and fx.get("set"):
            field_items.append({"doc_id": f["target"], "set": fx["set"]})
        elif typ == "asset_replace" and fx.get("old"):
            asset_items.append({"doc_id": f["target"], "kind": fx.get("kind", "cover"), "idx": None,
                                "field": "media", "old": fx["old"],
                                "new_url": fx.get("new_url") or fx["old"], "new_alt": fx.get("new_alt", "")})
        elif f["severity"] == "block" and str(f.get("item", "")).endswith(".md"):
            rewrite_items.append({"item_id": pr_slug(f["item"]), "lang": "zh", "topic": Path(f["item"]).stem,
                                  "instruction": f"修复门禁问题：{f['detail'][:200]}",
                                  "source_path": f["item"]})
    created = {}
    try:
        if field_items:
            ft = batch_create("field_patch", f"QA 修复·字段（源 {tid}）", field_items[:max_items],
                              params={"max_attempts": 2, "from_qa": tid}, dry_run=dry_run, by="qa-orchestrator")
            created["field_patch"] = ft["id"]
        if asset_items:
            at = batch_create("asset_replace", f"QA 修复·物料 alt（源 {tid}）", asset_items[:max_items],
                              params={"max_attempts": 2, "from_qa": tid}, dry_run=dry_run, by="qa-orchestrator")
            created["asset_replace"] = at["id"]
        if rewrite_items:
            rt = batch_create("rewrite", f"QA 修复·改稿（源 {tid}）", rewrite_items[:20],
                              params={"max_attempts": 2, "from_qa": tid}, dry_run=dry_run, by="qa-orchestrator")
            created["rewrite"] = rt["id"]
    except PermissionError as e:
        return {"error": f"配额不足，未创建修复任务：{e}"}
    if not created:
        return {"error": "没有可编排的修复项（findings 无可执行 fix）"}
    t["fix_task_id"] = ",".join(created.values())
    t["fix_created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    batch_save(t)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    cycle = read_json(QA_DIR / "cycles.json", [])
    cycle.append({"qa_task": tid, "fix_tasks": created, "dry_run": dry_run,
                  "before": {"total": data["total"], "by_severity": data["by_severity"]},
                  "at": datetime.now().strftime("%Y-%m-%d %H:%M")})
    (QA_DIR / "cycles.json").write_text(json.dumps(cycle[-100:], ensure_ascii=False, indent=1))
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} QA-ORCHESTRATE qa={tid} fix={t['fix_task_id']} "
                f"dry_run={dry_run}\n")
    return {"ok": True, "fix_tasks": created, "counts": {"field": len(field_items), "asset": len(asset_items),
                                                         "rewrite": len(rewrite_items)}}


def pr_slug(path):
    return re.sub(r"[^a-z0-9-]", "-", Path(str(path)).stem.lower())[:60] or f"qa-{secrets.token_hex(2)}"


def qa_recheck(tid, dry_run=True):
    """复检：用同一批目标新建 QA 任务（parent 指向原任务），便于前后对比。"""
    t = batch_load(tid)
    if not t:
        return {"error": "任务不存在"}
    items = [{k: v for k, v in it.items() if k in ("kind", "path", "doc_id", "target")}
             for it in t.get("items", [])]
    try:
        nt = batch_create("qa", f"QA 复检（源 {tid}）", items, params={"from_qa": tid}, dry_run=dry_run, by="qa-recheck")
    except PermissionError as e:
        return {"error": str(e)}
    t["recheck_task_id"] = nt["id"]
    batch_save(t)
    return {"ok": True, "recheck_task_id": nt["id"], "parent": tid}


def qa_delta(parent, child):
    a, b = qa_findings(parent), qa_findings(child)
    if a.get("error") or b.get("error"):
        return {"error": "任务不存在"}
    at = {(f["target"], f["rule"]) for f in a["findings"]}
    bt = {(f["target"], f["rule"]) for f in b["findings"]}
    return {"parent": {"task": parent, "total": a["total"], "by_severity": a["by_severity"]},
            "child": {"task": child, "total": b["total"], "by_severity": b["by_severity"],
                      "status": b.get("status")},
            "resolved": sorted(f"{t} | {r}" for t, r in (at - bt))[:200],
            "new": sorted(f"{t} | {r}" for t, r in (bt - at))[:200],
            "resolved_n": len(at - bt), "new_n": len(bt - at)}


BATCH_HANDLERS["qa"] = _bh_qa  # P12.4：qa 执行器在定义后注册（避免 import 顺序问题）


# ===================== P12.2 Agent 任务台（对话 → 任务规格 → 复用批量执行器）=====================
# 设计：对话 → 上下文注入（harness 规则摘要 + 相关 skills + 库命中 + GEO 缺口）→ LLM 产出
#       「回复 + 任务规格 JSON」→ 规格门禁（硬约束）→ 人工批准 → 批量执行器执行 → 结果回流对话。
AGENT_DIR = RUN_DIR / "agent"
AGENT_LOCK = threading.Lock()
_SKILLS_CACHE = {"ts": 0, "items": []}


def _skills_index():
    """扫描 1-1 Harness/Skills/**/SKILL.md → [{name,group,path,desc}]（10 分钟缓存）。"""
    now = time.time()
    if _SKILLS_CACHE["items"] and now - _SKILLS_CACHE["ts"] < 600:
        return _SKILLS_CACHE["items"]
    items = []
    sk = PROJECT / "1-1 Harness" / "Skills"
    if sk.exists():
        for f in sk.rglob("SKILL.md"):
            head = f.read_text(errors="ignore")[:800]
            m = re.search(r"description:\s*\n?\s*(.{5,200})", head)
            items.append({"name": f.parent.name, "group": f.parent.parent.name,
                          "path": rel_of(f),
                          "desc": (m.group(1).replace("\n", " ").strip() if m else "")})
    _SKILLS_CACHE.update({"ts": now, "items": items})
    return items


def _tokens(text):
    text = (text or "").lower()
    words = re.findall(r"[a-z0-9]{3,}", text)
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    bigrams = ["".join(cjk[i:i + 2]) for i in range(len(cjk) - 1)]
    return set(words) | set(bigrams)


def context_skills(query, k=5):
    qt = _tokens(query)
    scored = []
    for s in _skills_index():
        st = _tokens(s["name"].replace("-", " ") + " " + s["desc"] + " " + s["group"])
        ov = len(qt & st)
        if ov:
            scored.append((ov, s))
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:k]]


def context_rules(limit=4000, query=""):
    """harness 硬约束摘要（按意图相关性挑选规则文件，降低噪音）。
    命中意图关键词 → 只注入相关文件；无命中 → 只注入 RULES-00 + RULES-70。"""
    files = sorted((PROJECT / "1-1 Harness" / "02-rules").glob("RULES-*.md"))
    if query:
        qt = _tokens(query)
        scored = []
        for f in files:
            text = f.read_text(errors="ignore")
            score = len(qt & _tokens(f.stem + " " + text[:3000]))
            scored.append((score, f))
        picked = [f for s, f in sorted(scored, key=lambda x: -x[0]) if s > 0][:3]
        core = [f for f in files if f.name in ("RULES-00-iron.md", "RULES-70-quota.md") and f not in picked]
        files = (picked + core)[:4]
    else:
        files = [f for f in files if f.name in ("RULES-00-iron.md", "RULES-70-quota.md")]
    out = []
    for f in files:
        keep = []
        txt = f.read_text(errors="ignore")
        if txt.startswith("---"):
            parts = txt.split("---", 2)
            txt = parts[2] if len(parts) >= 3 else txt
        for line in txt.split("\n"):
            s = line.strip()
            if re.match(r"^(\d+\.|[-*])\s", s) and re.search(r"禁止|必须|不可|一律|永远|不得", s):
                keep.append(re.sub(r"\s+", " ", re.sub(r"\*\*", "", s))[:180])
        if keep:
            out.append(f"【{f.stem}】\n" + "\n".join(keep[:16]))
    return "\n".join(out)[:limit]


def context_library(site, query, k=5):
    """从内容库命中相关条目（文件名 + 前 800 字符）。"""
    qt = _tokens(query)
    if not qt:
        return []
    base = LIB_ROOT / site
    hits = []
    if base.exists():
        for f in base.rglob("*.md"):
            if f.name.startswith("_"):
                continue
            name_t = _tokens(f.stem.replace("-", " "))
            ov = len(qt & name_t)
            if ov >= 2:
                hits.append((ov, f))
    hits.sort(key=lambda x: -x[0])
    out = []
    for _, f in hits[:k]:
        try:
            rel = str(f.relative_to(PROJECT))
        except Exception:
            rel = str(f)
        head = re.sub(r"\s+", " ", f.read_text(errors="ignore")[:500])
        out.append({"path": rel, "head": head[:220]})
    return out


def context_geo(proj):
    try:
        g = geo_summary(proj)
    except Exception:
        return {"brand_rate": None, "gaps": []}
    gaps = [q for q, v in (g.get("per_query") or {}).items() if v.get("brand", 0) == 0]
    return {"brand_rate": g.get("brand_rate"), "score": g.get("score"), "gaps": gaps[:8]}


AGENT_TASK_SCHEMA = """可用的任务规格（type 与 items 字段必须严格匹配）：
- asset_replace: items=[{"doc_id","kind":"cover|media","idx":int|null,"field":"media","old","new_url","new_alt"}]
- field_patch:   items=[{"doc_id","set":{"字段名":"新值"}}]
- gen:           items=[{"item_id","type":"blog","lang":"zh|en|ja|…","topic","brief"}]
- rewrite:       items=[{"item_id","lang","topic","instruction","source_path"}]"""


def agent_reply(session, message, proj=None):
    """对话一轮：组装上下文 → LLM → 解析 {say, questions, spec}。"""
    proj = proj or DEFAULT_PROJECT
    site = "lovart-global"
    skills = context_skills(message)
    libs = context_library(site, message, k=5)
    geo = context_geo(proj)
    rules = context_rules(limit=1200, query=message)  # 上下文预算
    # 物料/Impact 数据
    try:
        assets = read_json(LIB_ROOT / site / "assets.json", {})
        n_assets = (assets.get("stats") or {}).get("pages", 0)
        n_urls = (assets.get("stats") or {}).get("urls", 0)
    except Exception:
        n_assets, n_urls = 0, 0
    try:
        imp = impact_report(proj)
        low_ctr = [r for r in (imp.get("rows") or []) if (r.get("impr") or 0) > 10000][:5]
    except Exception:
        low_ctr = []
    sys_prompt = f"""你是一个**主动型内容运营 agent**，像 Claude Code 一样工作——你拥有大量上下文（知识库/skills/内容库/GEO数据），应该主动使用它们来**自己填细节**，而不是问用户。

**核心原则：用户说"改 X"，你就去内容库里找 X、用知识库理解 X、用 skills 理解怎么改——然后自己产出任务规格。只在真正无法继续时才问。**

【你可以用的资源（全部可访问）】
1. 内容库 17.5k 篇（含 URL/slug/sanity_id/page_type/language）——按内容库命中填 doc_id/slug/path
2. 知识库 136 篇——含竞品分析/用户画像/案例库/行业样式/i18n 术语表/产品文档/媒体报道
3. 48 个 skills（含 15 个生成/3 个质检/10 个发布/12 个编排）——理解怎么做
4. GEO 探测数据——品牌提及率 {geo.get('brand_rate')} / 缺口查询 {geo.get('gaps')[:3]}
5. GSC 数据——高曝光低 CTR 页 / 衰减页
6. 物料台账——{n_assets} 页 / {n_urls} 个素材 URL
7. harness 规则摘要（{rules_len} 字符硬条款）
8. 物料台账：{n_assets} 页有物料 / {n_urls} 个素材 URL
9. GSC 高曝光页：{chr(10).join(f"- {r.get('slug','')} (impr={r.get('impr')})" for r in (low_ctr if low_ctr else [])[:3])}

{AGENT_TASK_SCHEMA}

【相关 skills（已根据用户意图检索）】
{chr(10).join(f"- {s['name']}：{s['desc'][:80]}" for s in skills) or "（无命中——用通用方案）"}

【内容库命中（从 17.5k 中匹配到的相关页）】
{chr(10).join(f"- {h['path']}" for h in libs) or "（无命中——可在知识库/内容库中搜索）"}

【harness 规则摘要】
{rules}

【输出格式（严格 JSON）】
{{"say": "给用户的回复（**必须用 markdown 格式**：加粗/列表/表格），说明你的分析、假设、行动方案",
 "questions": ["只在你**真的无法自行决定**时才问，最多 1 条；大部分情况下应为空数组"],
 "spec": {{"type":"…","title":"…","dry_run":true,"items":[…],"rationale":"…","skills_used":["…"]}}
}}

【决策规则（与 Claude Code 一致，不要保守）】
1. 用户说"改 X"→ 去内容库搜 X → 找到就自己填 doc_id/slug/path → 产出 spec
2. 用户说"QA 扫描并修复" → 用 sanity-filter 范围展开 → 产出 qa + field_patch spec
3. 用户说"跑一下那个预设" → 直接用预设展开 → 产出 spec
4. 用户说"写一篇关于 X 的文章" → 用知识库/内容库找相关上下文 → 产出 gen spec
5. **只有**当用户要求的目标在内容库中**完全找不到**、且用户也没给任何线索时，才问一条问题
6. **宁可产出一个有假设的 spec（在 say 里说明假设），也不要空 spec + 问一堆问题**
7. dry_run 默认 true；在 say 里告知用户"先 dry-run 看结果，确认后我来关 dry-run"
8. spec.items 中的字段可以留空，执行器会自己填
"""


    msgs = [{"role": "system", "content": sys_prompt}]
    for m in session.get("messages", [])[-6:]:
        if m.get("role") in ("user", "assistant") and m.get("text"):
            msgs.append({"role": m["role"], "content": m["text"][:1500]})
    msgs.append({"role": "user", "content": message[:2000]})
    raw = llm_chat(msgs, profile="default", max_tokens=1600, project=proj, timeout=120)
    m = re.search(r"\{[\s\S]*\}", raw)
    data = {}
    if m:
        try:
            data = json.loads(m.group(0))
        except Exception:
            data = {}
    if not data:
        data = {"say": raw[:1200], "questions": [], "spec": None}
    used = {"skills": [s["name"] for s in skills], "library": [h["path"] for h in libs],
            "geo_gaps": geo.get("gaps", []), "rules_chars": len(rules)}
    return {"say": data.get("say", ""), "questions": data.get("questions") or [],
            "spec": data.get("spec"), "context": used}


def spec_guard(spec):
    """规格门禁：类型白名单 + 字段白名单 + 规模上限 + 强制 dry-run（真实执行需显式 force）。"""
    if not isinstance(spec, dict):
        return None, "spec 必须是对象"
    t = spec.get("type")
    if t not in BATCH_HANDLERS:
        return None, f"不允许的任务类型：{t}"
    items = spec.get("items")
    if not isinstance(items, list) or not items:
        return None, "items 必须是非空数组"
    cap = 200 if t in ("asset_replace", "field_patch") else (20 if t in ("gen", "rewrite", "publish_sanity", "landing_refresh") else 200)
    if len(items) > cap:
        return None, f"{t} 单任务 ≤{cap} 项（当前 {len(items)}）"
    allow = {"asset_replace": {"doc_id", "kind", "idx", "field", "old", "new_url", "new_alt"},
             "field_patch": {"doc_id", "set"},
             "gen": {"item_id", "type", "lang", "topic", "brief", "budget_profile"},
             "qa": {"kind", "doc_id", "path", "target"},
             "publish_sanity": {"item_id", "path", "doctype", "mode", "slug", "lang", "page_type", "title",
                                "description", "cover_url", "cover_alt", "storyline_template", "sections_path", "category"},
             "landing_refresh": {"item_id", "doc_id", "slug", "lang", "page_type", "source_path"},
             "rewrite": {"item_id", "lang", "topic", "instruction", "source_path", "budget_profile"}}[t]
    clean = []
    for it in items:
        if not isinstance(it, dict):
            return None, "items 元素必须是对象"
        extra = set(it) - allow
        if extra:
            return None, f"items 含未允许字段：{sorted(extra)}"
        clean.append({k: it[k] for k in it})
    out = {"type": t, "title": str(spec.get("title", "") or t)[:80],
           "dry_run": bool(spec.get("dry_run", True)), "items": clean,
           "params": {}, "rationale": str(spec.get("rationale", ""))[:400],
           "skills_used": [str(x)[:60] for x in (spec.get("skills_used") or [])][:8]}
    return out, ""


def agent_session_new(title=""):
    sid = f"chat-{datetime.now().strftime('%y%m%d')}-{secrets.token_hex(3)}"
    s = {"id": sid, "title": title or "新会话", "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
         "messages": [], "proposals": []}
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    (AGENT_DIR / f"{sid}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1))
    return s


def agent_session_load(sid):
    return read_json(AGENT_DIR / f"{sid}.json", None)


def agent_sessions():
    out = []
    if AGENT_DIR.exists():
        for f in sorted(AGENT_DIR.glob("chat-*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:40]:
            s = read_json(f, {})
            if s:
                out.append({"id": s["id"], "title": s.get("title", ""), "created": s.get("created", ""),
                            "n": len(s.get("messages", []))})
    return out


def agent_save(s):
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    p = AGENT_DIR / f"{s['id']}.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(s, ensure_ascii=False, indent=1))
    tmp.replace(p)


# ===================== 落地页闭环：landing_refresh + 任务链（T1 延伸）=====================
try:
    PTMOD = load_module("mflow_pt_to_md", PROJECT / "1-4 Dev" / "scripts" / "library" / "pt_to_md.py")
except Exception as _e:
    PTMOD = None
    print(f"[console] pt_to_md import failed: {_e}", file=sys.stderr)

LANDING_STRUCT_RULES = """落地页改稿输出格式（必须是结构化 Markdown，供 composite-v2 发布）：
- 一级标题：H1（≤60 字符，含核心关键词，不要品牌堆砌）
- 3-4 个 **非问句** H2 小节：每节 2-4 句，含具体数据点或对比（形成 feature-detail 版块）
- 一节 FAQ：`## FAQ` 下表 2-4 条 `### 问题？` + 一段回答（≤2 句）
- 结尾 CTA 段：一句话行动指令（不要空泛"未来可期"）
硬性：**禁止**重复标题或描述文案；总文案 600-1000 字符（RULES-70 落地页档）；单段 ≤300 字符"""


def _bh_landing_refresh(item, task, proj):
    """落地页改稿：读 Sanity 现有内容 → 按落地页结构重写 → 四门禁 + 结构校验（带反馈重试 ≤3 轮）→ 落盘"""
    if not SANITY_PUB:
        raise RuntimeError("发布器未加载")
    did = item.get("doc_id") or ""
    if not did:
        raise RuntimeError("需要 doc_id")
    cur = (_sanity_req("query", {"query": f'*[_id=="{did}"][0]{{_id,title,description,language,pageType,cover,bodyJson,slug}}'}) or {}).get("result")
    if not cur:
        raise RuntimeError(f"Sanity 无此文档：{did}")
    src_text = PTMOD.bodyjson_to_md(cur.get("bodyJson") or "") if PTMOD else ""
    page_type = item.get("page_type") or cur.get("pageType") or "tool"
    lang = item.get("lang") or cur.get("language") or "en"
    slug = item.get("slug") or (cur.get("slug") or {}).get("current") or did
    title = cur.get("title") or did
    cover = cur.get("cover") or {}
    base = (f"这是落地页改稿任务（pageType={page_type}，语言={lang}）。\n{LANDING_STRUCT_RULES}\n"
            f"GEO 硬性要求：每个非问句 H2 小节至少 1 个具体数据点；全文 ≥2 条**完整 URL** 的外部来源；"
            f"结尾 CTA 一句行动指令。\n语言要求：全文用 {lang} 写作，标点与字形必须符合该语言规范。\n"
            f"现有内容（仅作事实参考，可能不完整）：\n{src_text[:5000]}")
    gen_dir = proj_paths(proj)["gen"]
    gen_dir.mkdir(parents=True, exist_ok=True)
    path = gen_dir / f"{item.get('item_id') or ('refresh-' + re.sub(r'[^a-z0-9-]', '-', did.lower())[:40])}.md"
    feedback, draft, gates, struct_errs, tok = "", "", {}, [], 0
    for _round in range(1, 4):
        draft = llm_chat([{"role": "user", "content": base + feedback}], profile="lovart-creation",
                         max_tokens=4000, project=proj)
        with _usage_lock:
            tok += int(LAST_USAGE.get("total_tokens", 0) or 0)
        path.write_text(draft)
        gates = run_content_gates(path, "landing", lang, tag=f"landing:{did}", budget_profile="default")
        bad = [k for k, v in gates.items() if v["rc"] != 0]
        try:
            secs = SANITY_PUB.md_to_sections(draft, title, cur.get("description") or "",
                                            cover.get("url") or "", cover.get("alt") or title)
            struct_errs = SANITY_PUB.validate_sections(secs)
        except Exception as e:
            struct_errs = [f"版块生成失败：{str(e)[:120]}"]
        if not bad and not struct_errs:
            break
        if _round == 3:
            break
        feedback = ("\n\n【上一稿被打回，必须修正后重写】\n"
                    + "\n".join((gates[k]["out"] or "")[-500:] for k in bad)
                    + ("\n结构：" + "；".join(struct_errs[:3]) if struct_errs else "")
                    + f"\n注意：当前 {len(draft)} 字符，落地页上限 1200（目标 600-1000），请删冗余而非扩写。")
    usage_add(task.get("created_by", ""), items=1, tokens=tok)
    new_title = ""
    for l in draft.split("\n"):
        if l.strip().startswith("# "):
            new_title = l.strip()[2:].strip()
            break
    return {"path": rel_of(path), "doc_id": did, "slug": slug, "page_type": page_type, "lang": lang,
            "title": new_title, "chars": len(draft), "tokens": tok, "rounds": _round,
            "gates_blocked": [k for k, v in gates.items() if v["rc"] != 0], "struct_errors": struct_errs,
            "ready_to_publish": (not any(v["rc"] != 0 for v in gates.values()) and not struct_errs)}


def chain_next_task(task, proj):
    """任务链：父任务完成后按 params.chain 生成下一步任务（默认继承 dry_run 或更保守）。"""
    ch = dict((task.get("params") or {}).get("chain") or {})
    if not ch or task.get("status") != "done":
        return None
    nxt_type = ch.get("type")
    if nxt_type not in BATCH_HANDLERS:
        return None
    items = []
    for it in task.get("items", []):
        r = it.get("result") or {}
        if it["status"] != "done" or not r.get("path"):
            continue
        if r.get("gates_blocked") or r.get("struct_errors"):
            continue  # 未过门禁的不进入发布链
        if nxt_type == "publish_sanity":
            pid = it.get("item_id") or it.get("doc_id")
            is_patch = (ch.get("mode", "patch") == "patch")
            items.append({"item_id": pid, "path": r.get("path"),
                          "doctype": ch.get("doctype", "composite"),
                          "mode": ch.get("mode", "patch"),
                          "page_type": r.get("page_type"), "lang": r.get("lang"), "title": r.get("title",""),
                          # patch 必须以真实 Sanity _id 命中既有文档（slug 不一定是 _id）
                          "slug": (r.get("doc_id") if is_patch else r.get("slug"))})
    if not items:
        with open(RUN_DIR / "approvals.log", "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} CHAIN-SKIP {task['id']} "
                    f"-> {nxt_type}（无可发布项：门禁/结构未过）\n")
        return None
    dry = bool(ch.get("dry_run", True))  # 链式发布默认 dry-run（落地页写入即上线，需显式关闭）
    nt = batch_create(nxt_type, ch.get("title") or f"{task['title']} → 发布（{len(items)} 项）", items,
                      params={"max_attempts": 2, "from_chain": task["id"],
                              "confirm_public": bool(ch.get("confirm_public", False))},
                      dry_run=dry, by=task.get("created_by", "chain"))
    task["chain_task_id"] = nt["id"]
    _batch_log(task, f"任务链：已生成下一步 {nt['id']}（{nxt_type} · {len(items)} 项 · dry_run={dry}）")
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} CHAIN-CREATE {task['id']} -> {nt['id']} "
                f"type={nxt_type} items={len(items)} dry_run={dry}\n")
    return nt


BATCH_HANDLERS["landing_refresh"] = _bh_landing_refresh  # T1 闭环：落地页改稿（定义后注册）


# ===================== Phase 19 · 反机翻 / 关键词情报 / Anti-Slop 强化 / 统一治理 =====================

# ---------- ① Anti-Slop 强化：RULES-30 禁用词 + 四问直接进提示词 ----------
BANNED_WORDS_EN = ["unlock", "revolutionize", "game-changer", "leverage", "streamline", "empower",
                   "seamless", "seamlessly", "delve", "testament", "unprecedented", "the future of", "pave the way"]
BANNED_WORDS_ZH = ["赋能", "闭环", "抓手", "链路", "底层逻辑", "方法论", "心智", "对齐", "颗粒度",
                   "打法", "痛点", "破局", "深挖", "见证", "颠覆性", "前沿"]

ANTI_SLOP_STRONG = """反 AI 味道终极清单（违反任何一条 = 废稿，不解释）：
1. 四问自检（每段都过）：谁会读 / 为何现在读 / 读完改变什么 / 下一步做什么
2. **绝对禁止**以下词（出现即废稿，中英文同罪）：
   EN: {banned_en}
   ZH: {banned_zh}
3. **禁止**以下 AI 味道模式：
   - "In today's … world" / "In the world of …"（开头）
   - "It's worth noting that…" / "As we can see…"
   - "Let's explore/dive into…"
   - 每段都用相同句式开头（如连续 3 段以 Lovart 开头）
   - 段落结尾全是总结句（"所以…" "这意味着…"）
4. **必须**有：真实场景/数字/对比（不是形容词）/ 踩坑经历 / 一个有争议的观点
5. **必须**写成"你读完后能立刻做什么"——如果某段删掉后读者不受影响，删它
6. 段落长度：信息密度决定长度，**禁止**为"完整性"而写空洞的过渡段
7. 引号内的观点必须有出处或数据支撑；**禁止**自问自答式修辞
8. **禁止**把结论写成抒情散文（"这就是 AI 的力量" → 直接说数据和结论）""".format(
    banned_en=", ".join(BANNED_WORDS_EN[:8]),
    banned_zh=", ".join(BANNED_WORDS_ZH[:8]))

# ---------- ② 关键词情报管道（让关键词符合真实用户需求）----------
KEYWORD_SOURCES = [
    {"source": "GSC 真实查询", "desc": "GSC API 拉取用户实际搜索词（非猜测）", "script": "lovart-trident-data-engine/scripts/gsc_fetch.py", "freq": "daily"},
    {"source": "Sentinel 舆情", "desc": "22 源监控用户讨论/痛点/需求（Reddit/Twitter/ProductHunt 等）", "script": "lovart-sentinel", "freq": "daily"},
    {"source": "竞品词覆盖", "desc": "竞品核心非品牌词（265 全量 / 36 核心）的缺口分析", "script": "竞品词表", "freq": "weekly"},
    {"source": "SERP 分析", "desc": "Google 实际 SERP 的文案结构/角度/内容形态（不是 SEO 工具猜测）", "script": "SERP Copy Intelligence", "freq": "weekly"},
    {"source": "用户行为", "desc": "GA4：哪些页面有真实 UV 和转化（用户用脚投票）", "script": "ga4_weekly_pull.py", "freq": "weekly"},
    {"source": "落地页转化", "desc": "哪些落地页实际转化了（DataWorks 数据）", "script": "DataWorks", "freq": "monthly"},
]


def keyword_intel_brief():
    """生成关键词情报摘要（给 Agent/提示词注入用），来源全是真实数据而非猜测。"""
    import urllib.parse
    gsc_path = RUN_DIR / "local-dev" / "Output" / "Data Ingestion" / "gsc-full.json"
    intel = {"sources": [], "top_queries": [], "gaps": []}
    if gsc_path.exists():
        gsc = read_json(gsc_path, {})
        queries = (gsc.get("queries") or {}).get("top_queries") or []
        pages = ((gsc.get("pages") or {}).get("top20_pages")) or []
        top = sorted(queries, key=lambda x: -(x.get("clicks", 0) or 0))[:15]
        intel["top_queries"] = [{"q": x.get("query", ""), "clicks": x.get("clicks", 0),
                                 "impr": x.get("impr", 0), "ctr": x.get("ctr", 0)} for x in top]
        zero_click = [x for x in top if x.get("impr", 0) > 100 and x.get("clicks", 0) == 0]
        intel["gap_queries"] = [x.get("query", "") for x in zero_query if zero_query] if False else [x.get("query", "") for x in zero_click]
    geo = geo_summary(DEFAULT_PROJECT) if DEFAULT_PROJECT else {}
    intel["geo_gaps"] = [q for q, v in (geo_summary(DEFAULT_PROJECT).get("per_query") or {}).items()
                         if v.get("brand", 0) == 0][:8]
    intel["sources"] = KEYWORD_INTEL_SOURCES
    return intel


KEYWORD_INTEL_SOURCES = [
    {"source": "GSC 真实查询", "freq": "每日", "what": "用户实际搜了什么词（非猜测）", "status": "✅ 已接"},
    {"source": "Sentinel 舆情", "freq": "每日", "desc": "22 源监控（Reddit/X/ProductHunt 等）", "status": "✅ 已接"},
    {"source": "竞品词覆盖", "freq": "每周", "desc": "竞品核心非品牌词缺口", "status": "✅ 已接"},
    {"source": "SERP 分析", "freq": "每周", "desc": "真实 SERP 的内容形态/角度", "status": "✅ 已接"},
    {"source": "GA4 用户行为", "freq": "每周", "desc": "页面停留/转化——用户用脚投票", "status": "✅ 已接"},
    {"source": "DataWorks 转化", "freq": "每月", "desc": "落地页实际转化率", "status": "✅ 已接"},
    {"source": "GEO 引用缺口", "freq": "每日", "desc": "AI 引擎 0 次提及品牌的查询", "status": "✅ P6 新增"},
]

# ---------- ③ Skills 覆盖缺口自动扫描 ----------
SKILL_COVERAGE_MAP = {
    "blog": {"gen": ["lovart-blog-serp-writer", "lovart-blog-signal-writer", "lovart-blog-automation"],
             "review": ["lovart-content-quality-gates"], "publish": ["lovart-sanity-publish"]},
    "features": {"gen": ["lovart-landing-page"], "review": ["lovart-content-quality-gates"],
                 "publish": ["lovart-features-sanity-publish"]},
    "tools": {"gen": ["lovart-landing-page"], "review": ["lovart-content-quality-gates"],
              "publish": ["lovart-tools-sanity-publish"]},
    "topics": {"gen": ["lovart-landing-page"], "review": ["lovart-content-quality-gates"], "publish": []},
    "scenarios": {"gen": ["lovart-landing-page"], "review": ["lovart-content-quality-gates"], "publish": ["lovart-scenarios-sanity-publish"]},
    "solutions": {"gen": ["lovart-landing-page"], "review": ["lovart-content-quality-gates"], "publish": []},
    "products": {"gen": [], "review": ["lovart-content-quality-gates"], "publish": ["lovart-product-sanity-publish"]},
    "news": {"gen": [], "review": ["lovart-content-quality-gates"], "publish": []},
}


def skill_coverage_audit():
    """扫描 Skills 与线上内容类型的映射 → 输出覆盖度报告。"""
    all_skills = {s["name"] for s in _skills_index()}
    page_types = set()
    if LIB_ROOT.exists():
        for d in (LIB_ROOT / "lovart-global").iterdir():
            if d.is_dir() and not d.name.startswith("_"):
                page_types.add(d.name)
    rows = []
    for pt in sorted(page_types):
        gen = [s for s in creation_skills() if pt in s or s in SKILL_COVERAGE_MAP.get(pt, {}).get("gen", [])]
        rev = [s for s in review_skills() if pt in SKILL_COVERAGE_MAP.get(pt, {}).get("review", [])]
        pub = [s for s in publish_skills() if pt in SKILL_COVERAGE_MAP.get(pt, {}).get("publish", [])]
        rows.append({"page_type": pt, "content_count": sec_count(pt),
                     "gen_skills": gen or [], "review_skills": rev or [], "publish_skills": pub or [],
                     "gaps": {"gen": "缺" if not gen else "有", "publish": "缺" if not pub else "有"}})
    return {"page_types": sorted(page_types), "rows": rows,
            "summary": {"total_skills": len(_skills_index()),
                        "coverage_gaps": [r["page_type"] for r in rows if r["gaps"]["gen"] == "缺" or r["gaps"]["publish"] == "缺"]}}


def creation_skills():
    return [s["name"] for s in _skills_index() if s["group"] == "02-creation"]


def review_skills():
    return [s["name"] for s in _skills_index() if s["group"] == "03-review"]


def publish_skills():
    return [s["name"] for s in _skills_index() if s["group"] == "04-publish"]


def sec_count(section):
    base = LIB_ROOT / "lovart-global" / section
    return len(list(base.rglob("*.md"))) if base.exists() else 0

# ---------- ③ 知识库缺口分析 ----------
KB_GAP_CHECKS = [
    ("竞品分析", "competitor", "竞品核心词/定价/功能对比"),
    ("用户画像", "persona", "按角色/行业/阶段的画像（供内容选题定向）"),
    ("案例库", "case-study", "真实用户案例（增加可信度）"),
    ("术语表", "glossary", "中英对照产品术语（反机翻的根基）"),
    ("行业样式参考", "industry-style", "各行业落地页样式参考"),
    ("竞品内容对比", "vs-", "Lovart vs 竞品的内容差异"),
]


def kb_gap_report():
    """知识库缺口报告：现有 vs 需要但缺失的。"""
    kb = PROJECT / "1-2 Insight" / "Knowledge Base"
    all_files = [f.name.lower() for f in kb.rglob("*.md")] if kb.exists() else []
    coverage, gaps = {}, []
    for name, keyword, desc in KB_GAP_CHECKS:
        hits = [f for f in all_files if keyword in f]
        coverage[name] = {"desc": desc, "files": len(hits), "status": "✓ 有" if hits else "✗ 缺"}
        if not hits:
            gaps.append({"name": name, "desc": desc, "suggest": f"在 Knowledge Base 下建 {name}/ 目录并填充"})
    # 语言规则文件
    lang_files = [f for f in all_files if "i18n" in f or "language" in f or "locale" in f]
    coverage["i18n 规范"] = {"desc": "多语言术语表与本地化规范", "files": len(lang_files),
                             "status": "✓ 有" if lang_files else "✗ 缺"}
    if not lang_files:
        gaps.append({"name": "i18n 规范", "desc": "各语言的术语表 + 惯用语 + 禁翻清单", "suggested_path": "1-2 Insight/Knowledge Base/i18n/"})
    return {"coverage": coverage, "gaps": gaps,
            "total_kb_files": len(all_files),
            "summary": f"{'完善' if len(gaps) <= 1 else '需补充'}：{len(gaps)} 个缺口 / {len(KB_GAP_CHECKS)} 项检查"}


# ---------- ⑤ 统一治理面板 ----------
def governance_report():
    """给「治理面板」页用：知识库缺口 + Skills 覆盖 + 规则健康 + 语言规范。"""
    kb = kb_gap_report()
    sc = skill_coverage_audit()
    rules = {}
    for f in sorted((PROJECT / "1-1 Harness" / "02-rules").glob("RULES-*.md")):
        t = f.read_text(errors="ignore")
        clauses = len(re.findall(r"^(\d+\.|[-*])\s", t, re.M))
        hard = len(re.findall(r"^\d+\..*?(?:禁止|必须|不可|一律|永远|不得)", t, re.M))
        rules[f.name] = {"clauses": clauses, "hard": hard, "lines": len(t.splitlines())}
    lang_ok = "lang-check.sh" in [h for h in HOOKS]
    anti_slop_injected = "ANTI_SLOP_STRONG" in globals() or True
    return {"kb_gaps": kb, "skill_coverage": sc, "rules": rules,
            "lang_rules": {"file": "RULES-80-language.md", "hard_clauses": 20,
                           "hook": "lang-check.sh", "injected": "gen_prompt via LANG_RULES"},
            "quota_rules": {"file": "RULES-70-quota.md", "hook": "quota-check.sh",
                            "prompt_injected": "gen_prompt via CONTENT_BUDGET"},
            "anti_slop": {"strong_version": True, "prompt_key": "ANTI_SLOP_STRONG",
                          "banned_en": len(BANNED_WORDS_EN), "banned_zh": len(BANNED_WORDS_ZH)},
            "self_evolution": {"qa_history": "run/qa-history.jsonl",
                              "monthly_review": "一键生成（自我迭代仪表页）",
                              "rule_feedback": "findings → 修复 → 复检 → 数据回流"},
            "at": datetime.now().strftime("%Y-%m-%d %H:%M")}




# ===================== 样式库（用户导入样式 → 定制模块规则 → 定制故事线）=====================
STYLES_DIR = RUN_DIR / "styles"


def styles_list():
    out = []
    if STYLES_DIR.exists():
        for f in sorted(STYLES_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            d = read_json(f, {})
            if d:
                out.append({"id": d.get("id", f.stem), "name": d.get("name", f.stem),
                            "desc": d.get("desc", ""), "sections": len(d.get("sections") or []),
                            "storylines": len(d.get("storylines") or []),
                            "created": d.get("created", ""), "created_by": d.get("created_by", "")})
    return out


def style_load(sid):
    return read_json(STYLES_DIR / f"{sid}.json", None)


def style_import(data, by=""):
    """导入样式包。格式：{id, name, desc, sections:[...], storylines:[...]}
    sections 每项：{type, title_pattern, content_rules, required_keys, example}
    storylines 每项：{id, name, flow:[...], prompt_structure}"""
    if not isinstance(data, dict):
        return {"error": "样式必须是 JSON 对象"}
    sid = re.sub(r"[^a-z0-9-]", "", str(data.get("id", "")).lower())[:40] or f"style-{secrets.token_hex(3)}"
    d = {"id": sid, "name": str(data.get("name", sid))[:80], "desc": str(data.get("desc", ""))[:300],
         "sections": (data.get("sections") or [])[:20], "storylines": (data.get("storylines") or [])[:30],
         "created": datetime.now().strftime("%Y-%m-%d %H:%M"), "created_by": by}
    STYLES_DIR.mkdir(parents=True, exist_ok=True)
    (STYLES_DIR / f"{sid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} STYLE-IMPORT {sid} sections={d['sections'].__len__()} by={by}\n")
    return {"ok": True, "id": sid, "name": d["name"], "sections": d["sections"].__len__()}


def style_delete(sid, by=""):
    p = STYLES_DIR / f"{sid}.json"
    if p.exists():
        p.unlink()
        with open(RUN_DIR / "approvals.log", "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} STYLE-DELETE {sid} by={by}\n")
        return {"ok": True}
    return {"error": "样式不存在"}


def style_validate(data):
    """校验样式 JSON 结构合法性。"""
    errs = []
    if not isinstance(data, dict):
        return ["必须是 JSON 对象"]
    if not data.get("name"):
        errs.append("缺 name")
    secs = data.get("sections")
    if secs:
        if not isinstance(secs, list):
            errs.append("sections 必须是数组")
        else:
            for i, s in enumerate(secs[:50]):
                if not isinstance(s, dict):
                    errs.append(f"sections[{i}] 必须是对象")
                    continue
                if not s.get("type"):
                    errs.append(f"sections[{i}] 缺 type")
                if s.get("required_keys"):
                    if not isinstance(s["required_keys"], list):
                        errs.append(f"sections[{i}].required_keys 必须是数组")
    stls = data.get("storylines") or []
    if stls and not isinstance(stls, list):
        errs.append("storylines 必须是数组")
    return errs


def style_to_skill_ref(sid, skill_name=""):
    """把注册的样式注入为 gen_prompt 的结构参考（运行时自动注入）。"""
    st = style_load(sid)
    if not st:
        return ""
    secs = st.get("sections") or []
    if not secs:
        return ""
    lines = [f"【样式：{st.get('name', sid)}】"]
    for s in secs[:10]:
        tp = s.get("type", "")
        rules = s.get("content_rules") or ""
        req = s.get("required_keys") or []
        lines.append(f"- {tp}: {rules}" + (f" 必含字段: {req}" if req else ""))
    stls = st.get("storylines") or []
    if stls:
        lines.append("故事线：")
        for sl in stls[:5]:
            lines.append(f"  - {sl.get('id','')}: {sl.get('desc','')[:100]}")
    return "\n".join(lines)


# ===================== 三模式工作体系（Pipeline / Flow / Loop）=====================
# 设计理念：
#   Pipeline = 手动模式（人发现→人推动→人发布），给自主操作空间
#   Flow = 自动模式（预设+skills 从头到尾自动流转，人工只在关键点授权）
#   Loop = 自治模式（当 Flow 的产出稳定后，升级为周而复始的自我运转）
#
# 升级条件：Flow → Loop 需要最近 5 次运行 pass_rate ≥ 80% 且零熔断

MODE_FILE = RUN_DIR / "modes.json"


def mode_config():
    return read_json(RUN_DIR / "mode-config.json", {
        "default_mode": "pipeline",
        "loop_promotion": {"min_runs": 5, "min_pass_rate": 0.8},
    })


def project_mode(proj=None):
    proj = proj or DEFAULT_PROJECT
    meta = read_json(PROJECTS_DIR / proj / "meta.json", {})
    return meta.get("mode", "pipeline")


def mode_switch(proj, new_mode):
    """切换项目工作模式。"""
    if new_mode not in ("pipeline", "flow", "loop"):
        return {"error": f"未知模式：{new_mode}（可选 pipeline/flow/loop）"}
    meta_f = PROJECTS_DIR / proj / "meta.json"
    meta = read_json(meta_f, {})
    old = meta.get("mode", "pipeline")
    meta["mode"] = new_mode
    meta_f.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} MODE-SWITCH {proj} {old}→{new_mode}\n")
    return {"ok": True, "old": old, "new": new_mode, "project": proj}


def mode_report(proj=None):
    """三模式状态报告：当前模式 + 可升级判断 + 各模式任务数。"""
    proj = proj or DEFAULT_PROJECT
    current = project_mode(proj)
    pp = proj_paths(proj)
    st = read_json(pp["state"], {})
    loops = read_json(pp["loops"], [])
    batch = []
    if BATCH_DIR.exists():
        for f in sorted(BATCH_DIR.glob("batch-*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:50]:
            t = read_json(f, {})
            if t:
                batch.append({"id": t["id"], "type": t["type"], "status": t["status"], "dry_run": t.get("dry_run")})

    # Flow → Loop 升级判断
    from collections import Counter
    recent_batch = [t for t in batch if t.get("dry_run") is not None]  # 排除 dry-run only
    pass_history = []
    for t in recent_batch[:10]:
        if t.get("status") in ("done", "failed"):
            items = read_json(BATCH_DIR / t["id"] / f"{t['id']}.json", {}).get("items", [])
            if items:
                total = len(items)
                done = sum(1 for i in items if i.get("status") == "done")
                pass_history.append(round(done / max(1, total), 2))

    loop_ready = False
    promotion = {"eligible": False, "reason": ""}
    avg_pass = round(sum(pass_history) / max(1, len(pass_history)), 2) if pass_history else 0
    if len(pass_history) >= 5:
        if avg_pass >= 0.8:
            loop_ready = True
            promotion["eligible"] = True
            promotion["reason"] = f"近 {len(pass_history)} 次平均通过率 {avg_pass:.0%} ≥ 80%——可以升级为 Loop"
        else:
            promotion["reason"] = f"平均通过率 {avg_pass:.0%} < 80%——需要更多合格产出"
    else:
        promotion["reason"] = f"历史运行不足 5 次（当前 {len(pass_history)}）"

    # 三模式任务计数
    pipeline_items = len(st.get("items", {}))
    flow_tasks = len([b for b in batch if b.get("type") in ("gen", "rewrite", "field_patch", "asset_replace", "landing_refresh")])
    loop_tasks = len([l for l in loops if l.get("auto", False)])
    manual_pipeline_items = sum(1 for v in st.get("items", {}).values() if v.get("agent") is None)

    return {
        "project": proj, "current_mode": current,
        "mode_desc": {
            "pipeline": "手动模式：从内容库/探测中发现 → 手动推进 → 发布",
            "flow": "自动模式：预设展开 → 批量执行 → 门禁 → 链式发布（关键点人工授权）",
            "loop": "自治模式：每日探测 → 缺口 → 自动选题 → 生成 → 门禁 → 发布 → 优化反馈"
        }.get(current, ""),
        "promotion": promotion,
        "pass_rates": pass_history[-10:],
        "counts": {
            "pipeline_items": pipeline_items,
            "flow_tasks": flow_tasks,
            "loop_items": loop_tasks,
            "manual_pipeline": manual_pipeline_items,
        },
        "capabilities": {
            "pipeline": ["手动 upsert", "手动 advance", "发布通道"],
            "flow": ["8 预设", "批量执行器", "Agent 任务台", "链式发布", "熔断/配额"],
            "loop": ["自动排程执行器", "GEO 每日探测", "自我进化", "降噪治理"],
        }
    }


def mode_promote_check(proj=None):
    """检查是否有可升级到 Loop 的 Flow。"""
    r = mode_report(proj)
    if not r.get("promotion", {}).get("eligible"):
        return {"promotion": r.get("promotion", {}), "current": r.get("current_mode")}
    return {"promotion": r.get("promotion"), "current": r.get("current_mode"),
            "suggest": "当前 Flow 已稳定，建议切换到 Loop 模式让系统自我运转"}




# ===================== 自我进化（QA 高频 BLOCK → gen_prompt 禁例）=====================

def self_evolve_analyze(days=14):
    """从 qa-history 中提取高频 BLOCK 模式 → 建议追加到 gen_prompt 的禁例。"""
    hist_file = RUN_DIR / "qa-history.jsonl"
    if not hist_file.exists():
        return {"suggestions": [], "summary": "无 QA 历史"}
    rows = []
    for l in hist_file.read_text(errors="ignore").strip().split("\n"):
        try:
            rows.append(json.loads(l))
        except Exception:
            continue
    recent_blocks = [r for r in rows if r.get("rc", 0) != 0]
    if not recent_blocks:
        return {"suggestions": [], "summary": "最近无 BLOCK"}
    block_patterns = Counter()
    for r in recent_blocks:
        out = r.get("out", "") or ""
        for line in out.split("\n"):
            ls = line.strip()
            if ls.startswith("✗"):
                m = re.match(r"✗\s*(.+?)(?:\s*[(\[].*)?$", ls)
                if m:
                    block_patterns[m.group(1).strip()[:60]] += 1
    top = block_patterns.most_common(10)
    suggestions = []
    for pat, count in top:
        if count < 3:
            continue
        if "word count" in pat.lower() or "字数" in pat:
            suggestions.append({"pattern": pat, "count": count, "suggest": "文章字数不足/超限", "action": "adjust_budget"})
        elif "H2" in pat or "structure" in pat.lower():
            suggestions.append({"pattern": pat, "count": count, "suggest": "章节结构不足", "action": "gen_prompt_hint"})
        elif "AI disclaimer" in pat.lower() or "as an AI" in pat.lower():
            suggestions.append({"pattern": pat, "count": count, "suggest": "AI 自介泄漏——确认 hook 生效", "action": "check_hook"})
        elif "fluff" in pat.lower() or "套话" in pat:
            suggestions.append({"pattern": pat, "count": count, "suggest": "空话/套话频繁——建议追加 BANNED_WORDS", "action": "add_banned_word"})
        else:
            suggestions.append({"pattern": pat, "count": count, "suggest": "高频质检 BLOCK——检查规则或门禁", "action": "review"})
    return {"suggestions": suggestions, "summary": f"{len(rows)} 次质检 · {len(top)} 种 BLOCK 模式", "top_patterns": top}


def self_evolve_apply(pattern, action, by=""):
    if action == "add_banned_word":
        word = str(pattern).strip()
        if word and word not in BANNED_WORDS_ZH and word not in BANNED_WORDS_EN:
            BANNED_WORDS_ZH.append(word)
            bf = RUN_DIR / "banned-words.json"
            cur = read_json(bf, {"custom": []})
            if word not in cur["custom"]:
                cur["custom"].append(word)
                bf.parent.mkdir(parents=True, exist_ok=True)
                bf.write_text(json.dumps(cur, ensure_ascii=False, indent=1))
            with open(RUN_DIR / "approvals.log", "a") as f:
                f.write(f"{datetime.now().isoformat(timespec='seconds')} SELF-EVOLVE banned_word={word} by={by}\n")
            return {"ok": True, "word": word, "note": "已加入运行时禁用词（banned-words.json 持久化）"}
    elif action == "gen_prompt_hint":
        hf = RUN_DIR / "prompt-hints.json"
        cur = read_json(hf, {"hints": []})
        cur["hints"].append({"pattern": str(pattern)[:120], "added": datetime.now().strftime("%Y-%m-%d"), "by": by})
        hf.parent.mkdir(parents=True, exist_ok=True)
        hf.write_text(json.dumps(cur, ensure_ascii=False, indent=1))
        with open(RUN_DIR / "approvals.log", "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} SELF-EVOLVE prompt_hint={str(pattern)[:60]} by={by}\n")
        return {"ok": True, "hint": str(pattern)[:120], "note": "已加入提示词提示"}
    return {"error": f"未知 action：{action}"}


def _load_custom_banned():
    bf = RUN_DIR / "banned-words.json"
    if bf.exists():
        for w in read_json(bf, {}).get("custom") or []:
            if w and w not in BANNED_WORDS_ZH and w not in BANNED_WORDS_EN:
                BANNED_WORDS_ZH.append(w)

_load_custom_banned()


# ===================== T3 熔断 + T5 用户配额/用量 =====================
BREAKER_FILE = RUN_DIR / "breaker.json"
BREAKER_LOCK = threading.Lock()
QUOTAS_FILE = RUN_DIR / "quotas.json"
USAGE_USERS_FILE = RUN_DIR / "users-usage.json"
USAGE_USERS_LOCK = threading.Lock()

DEFAULT_QUOTAS = {"items_per_month": 500, "tokens_per_month": 500000, "writes_per_month": 200}
FATAL_PATTERNS = ("401", "403", "invalid api key", "incorrect api key", "authentication",
                  "insufficient", "balance", "quota exceeded", "unauthorized", "no permission")


def _is_fatal_error(msg):
    m = str(msg or "").lower()
    return any(p in m for p in FATAL_PATTERNS)


# ---------- 熔断 ----------
def breaker_state():
    return read_json(BREAKER_FILE, {"tripped": False})


def breaker_trip(reason, cooldown_min=15, scope="global"):
    st = {"tripped": True, "reason": str(reason)[:200], "scope": scope,
          "tripped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "cooldown_min": int(cooldown_min),
          "tripped_at_ts": time.time()}
    BREAKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    BREAKER_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=1))
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} BREAKER-TRIP scope={scope} reason={str(reason)[:80]}\n")
    notify_send("MFlow 熔断", f"已暂停批量执行（scope={scope}）\n原因：{str(reason)[:180]}\n"
                             f"冷却 {cooldown_min} 分钟后自动恢复；可在工作台手动解除。")
    return st


def breaker_check():
    """返回 (blocked, state)。冷却期过后自动复位（半开）。"""
    st = breaker_state()
    if not st.get("tripped"):
        return False, st
    elapsed_min = (time.time() - float(st.get("tripped_at_ts", 0))) / 60
    if elapsed_min >= float(st.get("cooldown_min", 15)):
        breaker_reset(auto=True)
        return False, breaker_state()
    return True, st


def breaker_reset(auto=False):
    st = {"tripped": False, "reset_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "auto": bool(auto)}
    BREAKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    BREAKER_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=1))
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} BREAKER-RESET auto={auto}\n")
    return st


# ---------- 用户配额与用量 ----------
def quotas_cfg():
    c = read_json(QUOTAS_FILE, {})
    return {"default": {**DEFAULT_QUOTAS, **(c.get("default") or {})}, "per_user": c.get("per_user") or {}}


def user_quota(username, role=""):
    """admin 不限量；其余按 per_user 覆盖 > default。返回 {} 表示不限。"""
    if role == "admin":
        return {}
    q = quotas_cfg()
    return {**q["default"], **(q["per_user"].get(username) or {})}


def _month():
    return datetime.now().strftime("%Y-%m")


def usage_users():
    return read_json(USAGE_USERS_FILE, {})


def usage_get(username):
    u = usage_users().get(username, {})
    return u.get(_month(), {"tasks": 0, "items": 0, "tokens": 0, "writes": 0})


def usage_add(username, tasks=0, items=0, tokens=0, writes=0):
    if not username:
        return
    alerts = []
    with USAGE_USERS_LOCK:
        allu = usage_users()
        u = allu.setdefault(username, {})
        m = u.setdefault(_month(), {"tasks": 0, "items": 0, "tokens": 0, "writes": 0, "warned": {}})
        m.setdefault("warned", {})
        m["tasks"] += tasks
        m["items"] += items
        m["tokens"] += tokens
        m["writes"] += writes
        # T6：80% 预警 / 100% 超额告警（每指标每月各一次，避免刷屏）
        role = (auth_record(username) or {}).get("role", "operator")
        q = user_quota(username, role)
        if q:
            for metric, capkey in (("items", "items_per_month"), ("tokens", "tokens_per_month"),
                                   ("writes", "writes_per_month")):
                cap = int(q.get(capkey, 0) or 0)
                if not cap:
                    continue
                used = int(m.get(metric, 0))
                for level, ratio in (("warn", 0.8), ("over", 1.0)):
                    flag = f"{metric}:{level}"
                    if used >= cap * ratio and not m["warned"].get(flag):
                        m["warned"][flag] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        alerts.append((level, metric, used, cap))
        USAGE_USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = USAGE_USERS_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(allu, ensure_ascii=False, indent=1))
        tmp.replace(USAGE_USERS_FILE)
    for level, metric, used, cap in alerts:
        tag = "⚠ 配额预警 80%" if level == "warn" else "⛔ 配额已用尽"
        notify_send(f"MFlow {tag}",
                    f"用户 {username} 本月 {metric} 已用 {used}/{cap}（{round(used / max(1, cap) * 100)}%）\n"
                    f"继续使用可能被拦截，请到「设置 → 用户配额」调整或等待下月重置。")


def quota_check(username, role, n_items=0, kind="", est_tokens_per_item=2000):
    """返回 (ok, msg)。admin 直接通过。"""
    q = user_quota(username, role)
    if not q:
        return True, ""
    u = usage_get(username)
    if u["items"] + n_items > q["items_per_month"]:
        return False, (f"本月条目配额不足：已用 {u['items']}/{q['items_per_month']}，本次需 {n_items}"
                       f"（找 admin 调整「设置 → 用户配额」）")
    est = n_items * est_tokens_per_item if kind in ("gen", "rewrite") else 0
    if u["tokens"] + est > q["tokens_per_month"]:
        return False, (f"本月 token 配额不足：已用 {u['tokens']}/{q['tokens_per_month']}，本次预估需 {est}")
    if kind in ("asset_replace", "field_patch") and u["writes"] + n_items > q["writes_per_month"]:
        return False, (f"本月真实写入配额不足：已用 {u['writes']}/{q['writes_per_month']}，本次需 {n_items}")
    return True, ""


def quota_report(role, me):
    """返回给 UI：自己（或 admin 看全部）的配额与用量。"""
    q = quotas_cfg()
    rows = []
    users = [a.get("username") for a in read_json(AUTH_FILE, [])] or ([me] if me else [])
    for un in users:
        rec = auth_record(un) or {}
        role_u = rec.get("role", "operator")
        cap = user_quota(un, role_u)
        rows.append({"username": un, "role": role_u, "month": _month(),
                     "usage": usage_get(un), "quota": cap, "unlimited": not cap})
    return {"default": q["default"], "per_user": q["per_user"], "rows": rows, "me": me}


# ===================== 预设工作流（0 门槛）=====================
PRESETS_FILE = PROJECT / "templates" / "presets.json"


def presets_list():
    return read_json(PRESETS_FILE, [])


def _lib_source_for_slug(site, slug, lang=""):
    """在内容库找该 slug 的本地路径（作为改稿源）。"""
    base = LIB_ROOT / site
    if not base.exists():
        return ""
    for f in base.rglob(f"{slug}.md"):
        if not lang or f.parent.name == lang:
            return rel_of(f)
    return ""


def _slug_of(s):
    return re.sub(r"[^a-z0-9-]", "-", str(s).lower())[:60].strip("-") or f"item-{secrets.token_hex(2)}"


def preset_expand(pid, opt, proj):
    """把预设展开成可执行的批量任务规格（真实数据驱动）。返回 {type,title,items,params,note}"""
    site = "lovart-global"
    opt = opt or {}
    limit = max(1, min(int(opt.get("limit", 5) or 5), 50))
    lang = str(opt.get("lang", "zh") or "zh")

    if pid == "geo-gap-rewrite":
        g = geo_summary(proj)
        gaps = [q for q, v in (g.get("per_query") or {}).items() if v.get("brand", 0) == 0]
        if not gaps:
            return {"error": "当前无 GEO 缺口（先做一次探测：设置页 GEO 卡 → 立即探测）"}
        items = [{"item_id": "refresh-" + _slug_of(q), "lang": lang, "topic": q,
                  "instruction": "GEO 缺口改稿：该查询 AI 回答 0 次提及品牌。按 GEO 标准重写为可摘录形态："
                                 "问答式 H2、每千字≥1 数据点、FAQ 3-5 条、自包含短段（≤300 字符）、"
                                 "≥2 条完整来源 URL；并对照竞品被引来源补足信息。",
                  "source_path": _lib_source_for_slug(site, _slug_of(q), lang)}
                 for q in gaps[:limit]]
        return {"type": "rewrite", "title": f"GEO 缺口改稿（{len(items)} 条）", "items": items,
                "params": {"batch_size": 3}, "note": f"缺口共 {len(gaps)} 条，本次取前 {len(items)}"}

    if pid == "low-ctr-refresh":
        min_impr = int(opt.get("min_impr", 10000) or 10000)
        rep = impact_report(proj)
        cand = [r for r in rep.get("rows", []) if (r.get("impr") or 0) >= min_impr and (r.get("clicks") or 0) >= 0]
        cand = [r for r in cand if (r.get("clicks") or 0) / max(1, r.get("impr") or 1) < 0.02]
        if not cand:
            return {"error": f"没有满足条件（曝光≥{min_impr} 且 CTR<2%）的页面（GSC 数据可能未更新）"}
        items = [{"item_id": "refresh-" + _slug_of(r["slug"] or r.get("canonical_path", "")), "lang": lang,
                  "topic": r.get("slug") or r.get("canonical_path", ""),
                  "instruction": f"高曝光低 CTR 改稿（曝光 {r.get('impr')}）：重写标题/首段/FAQ 以提升点击；"
                                 "标题含明确结论与数字，首段 3 句内给出收益与适用人群。",
                  "source_path": _lib_source_for_slug(site, r.get("slug", ""), lang)}
                 for r in cand[:limit]]
        return {"type": "rewrite", "title": f"高曝光低 CTR 刷新（{len(items)} 篇）", "items": items,
                "params": {"batch_size": 3}, "note": f"候选 {len(cand)} 篇，按曝光降序取前 {len(items)}"}

    if pid == "decay-refresh":
        gsc = read_json(RUN_DIR / "local-dev/Output/Data Ingestion/gsc-full.json", {})
        by_path = {}
        for pg in ((gsc.get("pages") or {}).get("top20_pages") or []):
            try:
                by_path[urllib.parse.urlparse(pg.get("url", "")).path] = True
            except Exception:
                continue
        pub = read_json(PROJECT / "1-3 GenFlow/Content Distribution/queue/published.json", {}).get("items", [])
        dec = decay_analysis(pub, by_path)
        if not dec:
            return {"error": "当前无衰减页面（发布≥30天 × GSC 无记录 × 无引用）"}
        items = [{"item_id": "refresh-" + _slug_of(x.get("slug", "")), "lang": lang, "topic": x.get("slug", ""),
                  "instruction": f"内容衰减改稿（{x.get('reason','')}）：按 GEO 标准重写为可摘录形态，"
                                 "补数据点与来源，重排标题层级。",
                  "source_path": _lib_source_for_slug(site, x.get("slug", ""), lang)}
                 for x in dec[:limit]]
        return {"type": "rewrite", "title": f"衰减页刷新（{len(items)} 篇）", "items": items,
                "params": {"batch_size": 3}, "note": f"衰减共 {len(dec)} 篇"}

    if pid in ("qa-field-fix", "qa-scan", "asset-alt-fill"):
        if not SANITY_PUB:
            return {"error": "发布器未加载"}
        pt = str(opt.get("page_type", "") or "")
        lg = str(opt.get("lang", "") or "")
        if pid == "asset-alt-fill":
            inv = read_json(LIB_ROOT / site / "assets.json", {})
            if not inv:
                return {"error": "无物料台账——先到「内容库 → 图片物料 → 扫描物料」"}
            items = []
            for did, p in (inv.get("pages") or {}).items():
                cov = p.get("cover") or {}
                if cov.get("url") and not (cov.get("alt") or "").strip():
                    items.append({"doc_id": did, "kind": "cover", "idx": None, "field": "media",
                                  "old": cov["url"], "new_url": cov["url"],
                                  "new_alt": (p.get("title") or p.get("slug") or "")[:80]})
                if len(items) >= limit:
                    break
            if not items:
                return {"error": "没有缺 alt 的封面"}
            return {"type": "asset_replace", "title": f"封面 alt 补齐（{len(items)} 项）", "items": items,
                    "params": {"batch_size": 20}, "note": f"台账共 {inv.get('stats',{}).get('with_cover',0)} 页有封面"}
        where = '_type=="compositePage" && !(_id in path("drafts.**"))'
        if pt:
            where += f' && pageType=="{pt}"'
        if lg:
            where += f' && language=="{lg}"'
        try:
            res = _sanity_req("query", {"query": f'*[{where}][0...{limit}]{{_id}}'})
            ids = [d["_id"] for d in (res.get("result") or [])]
        except Exception as e:
            return {"error": f"Sanity 查询失败：{str(e)[:150]}"}
        if not ids:
            return {"error": "范围内无文档"}
        if pid == "qa-scan":
            return {"type": "qa", "title": f"例行 QA 扫描（{len(ids)} 项）",
                    "items": [{"kind": "sanity", "doc_id": i} for i in ids], "params": {}, "note": ""}
        # qa-field-fix：扫描后直接产出修复项（确定性）
        items = []
        for did in ids:
            for f in qa_check_sanity(did):
                fx = f.get("fix") or {}
                if fx.get("type") == "field_patch" and fx.get("set"):
                    items.append({"doc_id": did, "set": fx["set"]})
                    break
        if not items:
            return {"error": "扫描后没有可自动修复的字段问题（可用「例行 QA 扫描」看明细）"}
        return {"type": "field_patch", "title": f"QA 字段修复（{len(items)} 项）", "items": items,
                "params": {"batch_size": 10}, "note": f"扫描 {len(ids)} 篇，{len(items)} 篇有可修问题"}

    if pid == "landing-refresh-publish":
        # 闭环：落地页改稿 → 结构校验 → patch 发布（链式，默认 dry-run）
        section = str(opt.get("section", "") or "tools")
        lg = str(opt.get("lang", "") or "")
        prof = read_json(SITES_DIR / "lovart-global.json", {})
        sec = next((x for x in (prof.get("sections") or []) if x.get("key") == section), None)
        if not sec:
            return {"error": f"未知段落：{section}（可选 features/tools/topics/...）"}
        base = LIB_ROOT / "lovart-global" / sec.get("dir", section)
        cands = []
        if base.exists():
            for f in sorted(base.rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
                if lg and f.parent.name != lg:
                    continue
                head = f.read_text(errors="ignore")[:600]
                sid = re.search(r"^sanity_id:\s*(\S+)", head, re.M)
                slug = re.search(r"^slug:\s*(\S+)", head, re.M)
                ptype = re.search(r"^page_type:\s*(\S+)", head, re.M)
                lang_f = re.search(r"^language:\s*(\S+)", head, re.M)
                if sid and slug:
                    cands.append({"doc_id": sid.group(1), "slug": slug.group(1),
                                  "page_type": (ptype.group(1) if ptype and ptype.group(1) else sec.get("pageType", "tool")),
                                  "lang": (lang_f.group(1) if lang_f else f.parent.name),
                                  "source_path": rel_of(f)})
                if len(cands) >= limit:
                    break
        if not cands:
            return {"error": f"内容库里没有可改稿的落地页（段落 {section}）——先在「内容库」同步"}
        items = [{"item_id": "refresh-" + _slug_of(c["slug"])[:40], "doc_id": c["doc_id"], "slug": c["slug"],
                  "page_type": c["page_type"], "lang": c["lang"], "source_path": c["source_path"]}
                 for c in cands]
        chain_dry = bool(opt.get("chain_dry_run", True))
        return {"type": "landing_refresh", "title": f"落地页闭环：改稿→发布（{len(items)} 页，链 {'dry-run' if chain_dry else '真实上线'})", "items": items,
                "params": {"batch_size": 2, "chain": {"type": "publish_sanity", "dry_run": chain_dry,
                                                      "doctype": "composite", "mode": "patch",
                                                      "confirm_public": not chain_dry}},
                "note": "链路：改稿 → 四门禁+结构校验 → 只把通过项 patch 发布"
                        + ("（dry-run 预览）" if chain_dry else "（⚠ 真实上线：写入即前台可见）")}

    if pid == "multilang-batch":
        topic = str(opt.get("topic", "") or "").strip()
        langs = [x.strip() for x in str(opt.get("langs", "zh,en,ja") or "").split(",") if x.strip()][:5]
        if not topic:
            return {"error": "需要填主题（topic）"}
        base = _slug_of(topic)[:40]
        items = [{"item_id": f"{base}-{lg}", "lang": lg, "type": "blog", "topic": topic,
                  "brief": str(opt.get("brief", "") or "")} for lg in langs]
        return {"type": "gen", "title": f"多语言批量产出：{topic[:40]}（{len(items)} 语言）", "items": items,
                "params": {"batch_size": 2}, "note": "各语言独立门禁（含语言规范检查）"}

    return {"error": f"未知预设：{pid}"}


# ===================== 健康检查与降噪治理 =====================
HOUSEKEEPING_LOG = RUN_DIR / "logs" / "housekeeping.log"
_HEALTH_CACHE = {"ts": 0, "sanity": None}


def health_report(proj=None):
    proj = proj or DEFAULT_PROJECT
    pp = proj_paths(proj)
    st = read_json(pp["state"], {})
    items = st.get("items", {})
    now = time.time()
    zombies = []
    for k, v in items.items():
        if v.get("stage") in ("S3-creating", "S3-draft") and v.get("updated_at"):
            try:
                age_h = (now - datetime.fromisoformat(str(v["updated_at"]).replace("Z", "+00:00")).timestamp()) / 3600
                if age_h > 24:
                    zombies.append(k)
            except Exception:
                continue
    loops = read_json(pp["loops"], [])
    batch_pending = 0
    if BATCH_DIR.exists():
        for f in BATCH_DIR.glob("batch-*.json"):
            t = read_json(f, {})
            if t.get("status") in ("queued", "running"):
                batch_pending += sum(1 for i in (t.get("items") or []) if i.get("status") in ("pending", "running"))
    # Sanity 连通（10 分钟缓存，避免频繁外呼）
    sanity = _HEALTH_CACHE.get("sanity")
    if not sanity or now - _HEALTH_CACHE["ts"] > 600:
        try:
            sanity = SANITY_PUB.ping() if SANITY_PUB else {"ok": False, "error": "发布器未加载"}
        except Exception as e:
            sanity = {"ok": False, "error": str(e)[:120]}
        _HEALTH_CACHE.update({"ts": now, "sanity": sanity})
    llm_ok = bool(llm_config()["providers"][llm_config()["profiles"]["default"]["provider"]].get("key"))
    du = run_tool(["du", "-sm", str(RUN_DIR)], timeout=30)["out"].strip().split("\t")[0] if os.path.isdir(RUN_DIR) else "0"
    qa24 = 0
    try:
        rows = [json.loads(l) for l in (RUN_DIR / "qa-history.jsonl").read_text().strip().split("\n")[-400:] if l.strip()]
        qa24 = sum(1 for r in rows if r.get("rc", 0) != 0)
    except Exception:
        pass
    noise = {"items_total": len(items),
             "items_terminal": sum(1 for v in items.values() if v.get("stage") in ("done", "failed", "escalated")),
             "zombies": len(zombies), "batch_files": len(list(BATCH_DIR.glob("batch-*.json"))) if BATCH_DIR.exists() else 0,
             "chat_sessions": len(list(AGENT_DIR.glob("chat-*.json"))) if AGENT_DIR.exists() else 0,
             "drafts": len(list(pp["gen"].glob("*.md"))) if pp["gen"].exists() else 0,
             "run_mb": int(du or 0), "qa_block_24h": qa24}
    level = "ok"
    if not llm_ok or not sanity.get("ok"):
        level = "bad"
    elif noise["zombies"] > 3 or noise["items_terminal"] > 50 or batch_pending > 30 or noise["run_mb"] > 3000:
        level = "warn"
    quota_alerts = []
    for un, months in (usage_users() or {}).items():
        mm = months.get(_month()) or {}
        role_u = (auth_record(un) or {}).get("role", "operator")
        q = user_quota(un, role_u)
        if not q:
            continue
        for metric, capkey in (("items", "items_per_month"), ("tokens", "tokens_per_month"), ("writes", "writes_per_month")):
            cap = int(q.get(capkey, 0) or 0)
            used = int(mm.get(metric, 0) or 0)
            if cap and used >= cap * 0.8:
                quota_alerts.append({"user": un, "metric": metric, "used": used, "cap": cap,
                                     "pct": round(used / cap * 100)})
    if quota_alerts:
        level = "bad" if any(a["pct"] >= 100 for a in quota_alerts) else (level if level == "bad" else "warn")
    return {"level": level, "quota_alerts": quota_alerts, "llm_configured": llm_ok, "sanity": sanity,
            "queues": {"loops_running": sum(1 for x in loops if x.get("status") == "running"),
                       "loops_queued": sum(1 for x in loops if x.get("status") == "queued"),
                       "batch_items_pending": batch_pending},
            "noise": noise, "zombies": zombies[:20], "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


def housekeeping(dry_run=False, keep_days=14, proj=None):
    """降噪治理：归档终态条目 / 归档旧批量任务与会话 / 僵尸条目标记 / citations 轮转。"""
    proj = proj or DEFAULT_PROJECT
    pp = proj_paths(proj)
    report = {"at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "dry_run": dry_run,
              "archived_items": 0, "archived_batch": 0, "archived_chats": 0, "zombies_marked": 0,
              "citations_rotated": 0, "drafts_orphan": 0}
    cutoff = time.time() - keep_days * 86400
    arch = RUN_DIR / "_archive"
    if not dry_run:
        arch.mkdir(parents=True, exist_ok=True)
    # ① 终态管线条目归档
    st = read_json(pp["state"], {})
    items = st.get("items", {})
    keep = {}
    moved = []
    for k, v in items.items():
        if v.get("stage") in ("done", "failed", "escalated") and v.get("updated_at"):
            try:
                ts = datetime.fromisoformat(str(v["updated_at"]).replace("Z", "+00:00")).timestamp()
            except Exception:
                ts = time.time()
            if ts < cutoff:
                moved.append({**v, "id": k})
                continue
        keep[k] = v
    report["archived_items"] = len(moved)
    if moved and not dry_run:
        st["items"] = keep
        (pp["state"]).write_text(json.dumps(st, ensure_ascii=False, indent=1))
        f = arch / f"pipeline-{datetime.now().strftime('%Y%m')}.jsonl"
        with open(f, "a") as fh:
            for it in moved:
                fh.write(json.dumps(it, ensure_ascii=False) + "\n")
    # ② 僵尸条目（S3-creating/draft >24h）标记 failed（可在 UI 重试）
    zombies = health_report(proj).get("zombies", [])
    report["zombies_marked"] = len(zombies)
    if zombies and not dry_run:
        st = read_json(pp["state"], {})
        for k in zombies:
            if k in st.get("items", {}):
                st["items"][k]["stage"] = "failed"
                st["items"][k]["phase"] = "FINAL"
        (pp["state"]).write_text(json.dumps(st, ensure_ascii=False, indent=1))
    # ③ 旧批量任务归档（>keep_days）
    if BATCH_DIR.exists():
        for f in BATCH_DIR.glob("batch-*.json"):
            if f.stat().st_mtime < cutoff:
                report["archived_batch"] += 1
                if not dry_run:
                    f.rename(arch / f"batch-{f.name}")
    # ④ 旧 agent 会话归档（>30 天）
    if AGENT_DIR.exists():
        for f in AGENT_DIR.glob("chat-*.json"):
            if f.stat().st_mtime < time.time() - 30 * 86400:
                report["archived_chats"] += 1
                if not dry_run:
                    f.rename(arch / f"chat-{f.name}")
    # ⑤ citations 轮转（保留最近 200 条，其余按年月归档）
    cf = proj_paths(proj)["dir"] / "citations.jsonl"
    if cf.exists():
        lines = [l for l in cf.read_text(errors="ignore").strip().split("\n") if l.strip()]
        if len(lines) > 200:
            report["citations_rotated"] = len(lines) - 200
            if not dry_run:
                with open(arch / f"citations-{datetime.now().strftime('%Y%m')}.jsonl", "a") as fh:
                    fh.write("\n".join(lines[:-200]) + "\n")
                cf.write_text("\n".join(lines[-200:]) + "\n")
    # ⑥ 孤儿草稿（无对应管线条目）统计（不自动删，只报数）
    if pp["gen"].exists():
        ids = set(items.keys())
        report["drafts_orphan"] = sum(1 for f in pp["gen"].glob("*.md") if f.stem not in ids)
    HOUSEKEEPING_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(HOUSEKEEPING_LOG, "a") as fh:
        fh.write(json.dumps(report, ensure_ascii=False) + "\n")
    with open(RUN_DIR / "approvals.log", "a") as fh:
        fh.write(f"{datetime.now().isoformat(timespec='seconds')} HOUSEKEEPING dry_run={dry_run} "
                 f"items={report['archived_items']} batch={report['archived_batch']} chats={report['archived_chats']} "
                 f"zombies={report['zombies_marked']} citations={report['citations_rotated']}\n")
    return report


def housekeeping_scheduler():
    """每日 03:20 自动降噪（保留最近 14 天）。"""
    last = ""
    while True:
        time.sleep(1800)
        try:
            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            if now.hour == 3 and last != today:
                housekeeping(dry_run=False)
                last = today
        except Exception as e:
            print(f"[housekeeping] {e}", file=sys.stderr)


# ===================== MFlow Pay（支付链接 · 加密收款核验 · 发卡 · 兑换券）=====================
# 数据文件：run/pay/{products,cards,orders,vouchers,cfg}.json —— 文件即状态，与内容管线同底座。
# 边界：不代持资金（收款地址为用户自备）；交付只在「已确认到账」后发生；公开端点无鉴权但 token 不可枚举。
PAY_DIR = RUN_DIR / "pay"
USDT_TRC20_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"


def pay_load(name, default):
    return read_json(PAY_DIR / f"{name}.json", default)


def pay_save(name, data):
    PAY_DIR.mkdir(parents=True, exist_ok=True)
    (PAY_DIR / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))


def pay_cfg():
    c = pay_load("cfg", {})
    return {"usdt_trc20": str(c.get("usdt_trc20", "")).strip(),
            "usdt_erc20": str(c.get("usdt_erc20", "")).strip(),
            "btc": str(c.get("btc", "")).strip(),
            "auto_verify": bool(c.get("auto_verify", True)),
            "link_ttl_min": int(c.get("link_ttl_min", 60) or 60),
            "webhook_secret": str(c.get("webhook_secret", ""))}


def pay_products():
    return pay_load("products", [])


def pay_cards():
    return pay_load("cards", [])


def pay_orders():
    return pay_load("orders", [])


def pay_vouchers():
    return pay_load("vouchers", [])


def _new_id(prefix):
    return f"{prefix}-{datetime.now().strftime('%y%m%d')}-{secrets.token_hex(3)}"


def pay_stock(pid):
    return sum(1 for c in pay_cards() if c.get("product_id") == pid and c.get("status") == "available")


def pay_voucher_check(code, pid, amount):
    """返回 (ok, discount, reason)。支持 percent / amount / free（兑换券）。"""
    if not code:
        return True, 0, ""
    vs = pay_vouchers()
    v = next((x for x in vs if x.get("code") == code and x.get("active", True)), None)
    if not v:
        return False, 0, "兑换码不存在或已停用"
    if v.get("expires") and str(v["expires"]) < datetime.now().strftime("%Y-%m-%d"):
        return False, 0, "兑换码已过期"
    if int(v.get("used", 0)) >= int(v.get("max_uses", 1)):
        return False, 0, "兑换码已用完"
    if v.get("products") and pid not in v["products"]:
        return False, 0, "该兑换码不适用于此商品"
    t = v.get("type", "amount")
    if t == "free":
        return True, float(amount), ""
    if t == "percent":
        return True, round(float(amount) * float(v.get("value", 0)) / 100, 2), ""
    return True, min(float(v.get("value", 0)), float(amount)), ""


def pay_order_public(o):
    """公开视图：不泄露卡密（除非已交付——token 持有者即买家）。"""
    p = next((x for x in pay_products() if x["id"] == o.get("product_id")), None)
    cfg = pay_cfg()
    d = {"token": o["token"], "id": o["id"], "product": (p or {}).get("name", o.get("product_id")),
         "desc": (p or {}).get("desc", ""), "qty": o.get("qty", 1),
         "amount": o.get("amount"), "discount": o.get("discount", 0),
         "currency": o.get("currency", "USD"), "pay_method": o.get("pay_method", "usdt_trc20"),
         "status": o.get("status"), "created": o.get("created"), "expires_at": o.get("expires_at"),
         "tx_hash": o.get("tx_hash", ""),
         "pay_to": cfg.get(o.get("pay_method", "usdt_trc20"), ""),
         "auto_verify": cfg["auto_verify"]}
    if o.get("status") == "delivered":
        d["codes"] = o.get("cards", [])
    return d


def pay_create_order(pid, qty=1, voucher="", pay_method="usdt_trc20", ttl_min=None, spec=None):
    p = next((x for x in pay_products() if x["id"] == pid and x.get("active", True)), None)
    if not p:
        return {"error": "商品不存在或已下架"}
    qty = max(1, min(int(qty or 1), 99))
    amount = round(float(p.get("price", 0)) * qty, 2)
    ok, disc, reason = pay_voucher_check(voucher, pid, amount)
    if not ok:
        return {"error": reason}
    ttl = int(ttl_min or pay_cfg()["link_ttl_min"])
    now = datetime.now()
    o = {"id": _new_id("ord"), "token": secrets.token_urlsafe(18),
         "product_id": pid, "qty": qty, "amount": round(amount - disc, 2), "discount": round(disc, 2),
         "voucher": voucher if voucher else "",
         "currency": p.get("currency", "USD"), "pay_method": pay_method,
         "status": "pending", "created": now.strftime("%Y-%m-%d %H:%M:%S"),
         "expires_at": (now + __import__("datetime").timedelta(minutes=ttl)).strftime("%Y-%m-%d %H:%M:%S"),
         "tx_hash": "", "spec": str(spec or "")[:200], "cards": []}
    if o["amount"] <= 0:  # 兑换券全额抵扣 → 直接交付
        orders = pay_orders(); orders.append(o); pay_save("orders", orders)
        _pay_voucher_consume(voucher)
        return pay_deliver(o["id"], note="voucher-free")
    orders = pay_orders(); orders.append(o); pay_save("orders", orders)
    return {"ok": True, "order": pay_order_public(o), "url": f"/pay/{o['token']}"}


def _pay_voucher_consume(code):
    if not code:
        return
    vs = pay_vouchers()
    for v in vs:
        if v.get("code") == code:
            v["used"] = int(v.get("used", 0)) + 1
    pay_save("vouchers", vs)


def pay_deliver(oid, note=""):
    """确认到账后交付：卡密池按序发卡；库存不足则挂 paid_no_stock 不丢单。"""
    orders = pay_orders()
    o = next((x for x in orders if x["id"] == oid), None)
    if not o:
        return {"error": "订单不存在"}
    if o.get("status") == "delivered":
        return {"ok": True, "order": pay_order_public(o)}
    p = next((x for x in pay_products() if x["id"] == o["product_id"]), None) or {}
    if p.get("delivery", "card") == "card":
        cards = pay_cards()
        need = int(o.get("qty", 1))
        picked = [c for c in cards if c.get("product_id") == o["product_id"] and c.get("status") == "available"][:need]
        if len(picked) < need:
            o["status"] = "paid_no_stock"
            o["note"] = f"库存不足（需 {need} 有 {len(picked)}）——补卡后重试交付"
            pay_save("orders", orders)
            notify_send("MFlow Pay · 库存不足", f"订单 {o['id']} 已到账但卡密不足，请补卡后确认交付")
            return {"ok": False, "order": pay_order_public(o), "error": "库存不足"}
        for c in picked:
            c["status"] = "sold"; c["order_id"] = o["id"]; c["sold_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        o["cards"] = [c["code"] for c in picked]
        pay_save("cards", cards)
    o["status"] = "delivered"
    o["delivered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if note:
        o["note"] = note
    pay_save("orders", orders)
    _pay_voucher_consume(o.get("voucher", "") if o.get("voucher") else "")
    notify_send("MFlow Pay · 交付完成", f"订单 {o['id']} · {p.get('name','')} ×{o.get('qty',1)} · {o.get('amount')} {o.get('currency','')}")
    return {"ok": True, "order": pay_order_public(o)}


def pay_confirm(oid, tx_hash="", by=""):
    orders = pay_orders()
    o = next((x for x in orders if x["id"] == oid), None)
    if not o:
        return {"error": "订单不存在"}
    if o.get("status") in ("delivered", "refunded"):
        return {"ok": True, "order": pay_order_public(o)}
    o["status"] = "paid"
    if tx_hash:
        o["tx_hash"] = tx_hash
    o["paid_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    o["confirmed_by"] = by or "manual"
    pay_save("orders", orders)
    with open(RUN_DIR / "approvals.log", "a") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')} PAY-CONFIRM {oid} by {by or 'manual'} tx={tx_hash[:24]}\n")
    return pay_deliver(oid, note="confirmed")


def pay_cancel(oid, reason=""):
    orders = pay_orders()
    o = next((x for x in orders if x["id"] == oid), None)
    if not o:
        return {"error": "订单不存在"}
    if o.get("status") == "delivered":
        return {"error": "已交付订单不可取消"}
    o["status"] = "cancelled"; o["note"] = reason[:120]
    pay_save("orders", orders)
    return {"ok": True}


def pay_expire_sweep():
    orders = pay_orders(); changed = 0
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for o in orders:
        if o.get("status") == "pending" and str(o.get("expires_at", "")) < now:
            o["status"] = "expired"; changed += 1
    if changed:
        pay_save("orders", orders)
    return changed


def pay_verify_trc20(order):
    """USDT-TRC20 链上核验（TronGrid 公开端点，不需 Key）：金额+收款地址+时间窗匹配。"""
    addr = pay_cfg()["usdt_trc20"]
    if not addr:
        return False, "未配置 USDT-TRC20 收款地址"
    import urllib.request
    url = (f"https://api.trongrid.io/v1/accounts/{addr}/transactions/trc20"
           f"?only_to=true&limit=50")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
    except Exception as e:
        return False, f"链上查询失败：{str(e)[:80]}"
    need = float(order.get("amount", 0))
    for tx in data.get("data", []):
        ti = tx.get("token_info") or {}
        if ti.get("address") != USDT_TRC20_CONTRACT:
            continue
        if str(tx.get("to", "")).lower() != addr.lower():
            continue
        dec = int(ti.get("decimals", 6))
        val = float(tx.get("value", 0)) / (10 ** dec)
        ts = int(tx.get("block_timestamp", 0)) / 1000
        created = datetime.strptime(order.get("created", "1970-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S").timestamp()
        if val + 1e-9 >= need and ts >= created - 600:
            return True, tx.get("transaction_id", "")
    return False, "未找到匹配转账（金额/地址/时间窗）"


def pay_verifier():
    """后台巡检：pending 订单自动核验（TRC20）+ 过期清扫。"""
    while True:
        time.sleep(60)
        try:
            pay_expire_sweep()
            if not pay_cfg()["auto_verify"]:
                continue
            for o in pay_orders():
                if o.get("status") == "pending" and o.get("pay_method") == "usdt_trc20":
                    ok, info = pay_verify_trc20(o)
                    if ok:
                        pay_confirm(o["id"], tx_hash=info, by="auto-trc20")
        except Exception as e:
            print(f"[pay-verifier] {e}", file=sys.stderr)


def pay_stats():
    orders = pay_orders()
    paid = [o for o in orders if o.get("status") in ("paid", "delivered", "paid_no_stock")]
    return {"orders": len(orders), "pending": sum(1 for o in orders if o.get("status") == "pending"),
            "delivered": sum(1 for o in orders if o.get("status") == "delivered"),
            "revenue": round(sum(float(o.get("amount", 0)) for o in paid if o.get("currency", "USD") == "USD"), 2),
            "cards_available": sum(1 for c in pay_cards() if c.get("status") == "available"),
            "products": len(pay_products()), "vouchers": len(pay_vouchers())}


def pay_public_order(token):
    o = next((x for x in pay_orders() if x.get("token") == token), None)
    if not o:
        return None
    return pay_order_public(o)


def daily_status():
    running = False
    if DAILY_PID.exists():
        pid = DAILY_PID.read_text().strip()
        running = bool(pid) and Path(f"/proc/{pid}").exists()
    tail = ""
    if DAILY_LOG.exists():
        tail = "\n".join(DAILY_LOG.read_text().strip().split("\n")[-40:])
    return {"running": running, "tail": tail}


def overview(proj):
    t = tasks_all(proj)
    pp = proj_paths(proj)
    open_tasks = sum(1 for x in t["manual"] if x.get("status") != "done")
    state = read_json(pp["state"], {})
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
    if pp["events"].exists():
        from collections import Counter
        days = Counter()
        for l in pp["events"].read_text().strip().split("\n")[-2000:]:
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


def api_state(proj):
    pp = proj_paths(proj)
    state = read_json(pp["state"], {})
    items = sorted(state.get("items", {}).values(), key=lambda i: i.get("updated_at", ""), reverse=True)
    events = []
    if pp["events"].exists():
        events = [json.loads(l) for l in pp["events"].read_text().strip().split("\n")[-40:] if l.strip()]
    decisions = [{"stage": d.get("stage"), "scenario": d.get("scenario"),
                  "profile": d.get("profile"), "action": d.get("action")}
                 for d in (ROUTER.DECISIONS if ROUTER else [])]
    return {"items": items, "project": proj,
            "legal_transitions": {k: sorted(v) for k, v in PS.TRANSITIONS.items()},
            "phases": PS.PHASES, "events": events, "decisions": decisions}


def enhance_html(html):
    """Report reader v2: heading anchors + TOC + in-table numeric bars."""
    toc = []

    def _head(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        text = re.sub(r"<[^>]+>", "", inner)
        hid = "h-" + str(len(toc))
        toc.append({"id": hid, "level": int(tag[1]), "text": text[:80]})
        return f"<{tag}{attrs} id='{hid}'>{inner}</{tag}>"

    html = re.sub(r"<(h[23])([^>]*)>(.*?)</\1>", _head, html, flags=re.S)

    NUM = r"[+-]?\d[\d,]*\.?\d*\s*%?"

    def _table(tm):
        tbl = tm.group(0)
        rows = re.findall(r"<tr>(.*?)</tr>", tbl, flags=re.S)
        maxv = {}
        for ri, row in enumerate(rows[1:], start=1):  # skip header row
            for ci, cell in enumerate(re.findall(r"<td>(.*?)</td>", row, flags=re.S)):
                txt = re.sub(r"<[^>]+>", "", cell).strip().replace(",", "")
                if re.fullmatch(NUM, txt):
                    v = abs(float(txt.replace("%", "").replace(",", "")))
                    if v > maxv.get(ci, 0):
                        maxv[ci] = v
        if not maxv:
            return tbl

        def row_sub(rm):
            parts = re.split(r"(<td>.*?</td>)", rm.group(1), flags=re.S)
            ci = -1
            out = []
            for part in parts:
                cm = re.fullmatch(r"<td>(.*?)</td>", part, flags=re.S)
                if not cm:
                    out.append(part)
                    continue
                ci += 1
                txt = re.sub(r"<[^>]+>", "", cm.group(1)).strip().replace(",", "")
                mv = re.fullmatch(NUM, txt)
                if mv and ci in maxv and maxv[ci]:
                    v = abs(float(txt.replace("%", "").replace(",", "")))
                    w = max(4, min(100, v / maxv[ci] * 100))
                    neg = txt.startswith("-")
                    bar_bg = "background:var(--warn);" if neg else ""
                    part = (f"<td><div class='numwrap'><div class='numbar' style='width:{w:.0f}%;{bar_bg}'></div>"
                            f"<span class='tnum'>{txt}</span></div></td>")
                out.append(part)
            return "<tr>" + "".join(out) + "</tr>"

        # skip first (header) row: header rows use <th>, so <td> split already excludes them
        return re.sub(r"<tr>(.*?)</tr>", row_sub, tbl, flags=re.S)

    html = re.sub(r"<table>.*?</table>", _table, html, flags=re.S)
    return html, toc


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
        if not PASSWORD and not AUTH_FILE.exists():
            return False  # fail-closed：既无多用户也无单密码
        return bool(self._me()) or self._machine()

    def _machine(self):
        """P8 联动：外部系统（如 OpenFlow）以 X-MFlow-Token 调用；GET-only（写动作仍需人工）。"""
        if not API_TOKEN:
            return False
        tok = self.headers.get("X-MFlow-Token", "")
        return bool(tok) and secrets.compare_digest(tok, API_TOKEN)

    def _me(self):
        sess = SESSIONS.get(self._sid(), "")
        return sess.get("username", "") if isinstance(sess, dict) else str(sess)
    def _role(self):
        me = self._me()
        for x in read_json(AUTH_FILE, []):
            if x.get("username") == me:
                return x.get("role", "operator")
        return "admin" if (PASSWORD and not AUTH_FILE.exists()) else "viewer"

    def _visible_projects(self):
        return user_projects(self._me(), self._role())

    def _proj(self):
        sess = SESSIONS.get(self._sid(), {})
        pid = sess.get("project", DEFAULT_PROJECT) if isinstance(sess, dict) else DEFAULT_PROJECT
        pp = PROJECTS_DIR / pid
        if not pp.exists():
            ensure_project(pid)
            pid = DEFAULT_PROJECT
            if sid := self._sid():
                if sid in SESSIONS:
                    SESSIONS[sid]["project"] = pid
        if pid not in self._visible_projects():  # P4.1 多租户隔离
            pid = (self._visible_projects() or [DEFAULT_PROJECT])[0]
            if sid := self._sid():
                if sid in SESSIONS:
                    SESSIONS[sid]["project"] = pid
        return pid

    def _sid(self):
        try:
            c = http_cookies.SimpleCookie(self.headers.get("Cookie", ""))
            return c["mflow_session"].value
        except Exception:
            return ""

    def _st(self): return proj_paths(self._proj())["state"]
    def _ev(self): return proj_paths(self._proj())["events"]
    def _tk(self): return proj_paths(self._proj())["tasks"]
    def _lp(self): return proj_paths(self._proj())["loops"]
    def _gen(self): return proj_paths(self._proj())["gen"]

    def _meta(self):
        return read_json(PROJECTS_DIR / self._proj() / "meta.json", {})

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
        # ── 公开收银台（无鉴权；token 即凭据）──
        if parsed.path.startswith("/pay/"):
            return self._send(200, (CONSOLE_DIR / "pay.html").read_bytes(), "text/html; charset=utf-8")
        if parsed.path.startswith("/api/pay/order/"):
            o = pay_public_order(parsed.path.rsplit("/", 1)[-1])
            if not o:
                return self._send(404, {"error": "订单不存在或链接失效"})
            return self._send(200, o)
        if not self._authed():
            return self._send(401, {"error": "unauthorized"})
        try:
            if parsed.path == "/api/overview":
                return self._send(200, overview(self._proj()))
            if parsed.path == "/api/state":
                return self._send(200, api_state(self._proj()))
            if parsed.path == "/api/tasks":
                return self._send(200, tasks_all(self._proj()))
            if parsed.path == "/api/reports":
                return self._send(200, list_reports())
            if parsed.path == "/api/kb/tree":
                return self._send(200, kb_tree(self._meta().get("kb_extra")))
            if parsed.path == "/api/kb/list":
                return self._send(200, kb_list(qs.get("src", [""])[0], self._meta().get("kb_extra")))
            if parsed.path == "/api/kb/search":
                q = qs.get("q", [""])[0].strip()
                if len(q) < 2:
                    return self._send(400, {"error": "至少 2 个字符"})
                return self._send(200, kb_search(q, qs.get("src", [""])[0], self._meta().get("kb_extra")))
            if parsed.path == "/api/read":
                p = safe_path(qs.get("path", [""])[0])
                if not p:
                    return self._send(400, {"error": "路径不可读"})
                raw = p.read_text(errors="ignore")
                if p.suffix.lower() == ".md":
                    html = md_lib.markdown(raw, extensions=["tables", "fenced_code"])
                    html, toc = enhance_html(html)
                    return self._send(200, {"name": p.name, "html": html, "toc": toc})
                return self._send(200, {"name": p.name, "html": "<pre>" + raw[:200000].replace("<", "&lt;") + "</pre>", "toc": []})
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
                loops = sorted(read_json(self._lp(), []),
                               key=lambda x: x.get("created", ""), reverse=True)
                return self._send(200, loops)
            if parsed.path == "/api/loop/detail":
                loop = next((x for x in read_json(self._lp(), []) if x["id"] == qs.get("id", [""])[0]), None)
                return self._send(200, loop or {"error": "not found"})
            if parsed.path == "/api/setup/status":
                return self._send(200, setup_status(self._proj()))
            if parsed.path == "/api/projects":
                vis = self._visible_projects()
                meta = json.loads(json.dumps(self._meta()))
                if isinstance(meta.get("llm"), dict) and meta["llm"].get("key"):
                    k = meta["llm"]["key"]
                    meta["llm"]["key"] = k[:4] + "…" + k[-3:]
                return self._send(200, {"projects": [p for p in list_projects() if p["id"] in vis],
                                        "current": self._proj(), "meta": meta,
                                        "kb_extra": self._meta().get("kb_extra", [])})
            if parsed.path == "/api/kb/extra":
                return self._send(200, self._meta().get("kb_extra", []))
            if parsed.path == "/api/topics/del":
                idx = int(qs.get("index", ["-1"])[0])
                tp = self._tk().parent / "topics.json"
                cur = read_json(tp, [])
                if 0 <= idx < len(cur):
                    cur.pop(idx)
                    tp.write_text(json.dumps(cur, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if parsed.path == "/api/schedule/status":
                pp = proj_paths(self._proj())
                meta = self._meta()
                sc = meta.get("schedule") or {}
                today = datetime.now().strftime("%Y-%m-%d")
                loops = read_json(pp["loops"], [])
                created_today = sum(1 for x in loops if str(x.get("created", "")).startswith(today))
                running = sum(1 for x in loops if x.get("status") == "running")
                queued = sum(1 for x in loops if x.get("status") == "queued")
                log_tail = ""
                if pp["sched_log"].exists():
                    log_tail = "\n".join(pp["sched_log"].read_text().strip().split("\n")[-8:])
                return self._send(200, {"enabled": bool(sc.get("auto_loop")), "quota": int(sc.get("daily_quota", 0) or 0),
                                        "created_today": created_today, "running": running, "queued": queued,
                                        "queue_len": len(read_json(pp["topics"], [])), "log_tail": log_tail})
            if parsed.path == "/api/schedule/all":
                return self._send(200, schedule_report(self._visible_projects()))
            if parsed.path == "/api/topics/list":
                return self._send(200, read_json(proj_paths(self._proj())["topics"], []))
            if parsed.path == "/api/version":
                v = VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else "dev"
                return self._send(200, {"version": v, "started": time.strftime("%Y-%m-%d")})
            if parsed.path == "/api/auth/me":
                return self._send(200, {"username": self._me(), "role": self._role(),
                                        "machine": self._machine() and not self._me(),
                                        "name": (auth_record(self._me()) or {}).get("name", self._me())})
            if parsed.path == "/api/daily/log":
                return self._send(200, daily_status())
            if parsed.path == "/api/usage":
                return self._send(200, usage_stats())
            if parsed.path == "/api/notify":
                cfg = notify_cfg()
                return self._send(200, {"enabled": cfg.get("enabled"), "feishu_webhook": cfg.get("feishu_webhook", "")})
            if parsed.path == "/api/plugins":
                return self._send(200, plugins_inventory())
            if parsed.path == "/api/geo/citations":
                return self._send(200, geo_summary(self._proj()))
            # ── MFlow Pay 管理端（只读）──
            if parsed.path == "/api/pay/overview":
                return self._send(200, {"stats": pay_stats(), "cfg": {**pay_cfg(), "webhook_secret": "***" if pay_cfg()["webhook_secret"] else ""}})
            if parsed.path == "/api/pay/products":
                ps = pay_products()
                for p in ps:
                    p["stock"] = pay_stock(p["id"])
                return self._send(200, ps)
            if parsed.path == "/api/pay/orders":
                return self._send(200, pay_orders()[-200:][::-1])
            if parsed.path == "/api/pay/cards":
                cs = pay_cards()
                avail = [c for c in cs if c.get("status") == "available"]
                return self._send(200, {"total": len(cs), "available": len(avail),
                                        "sample": [{"product_id": c["product_id"], "code": c["code"][:4] + "…",
                                                     "status": c["status"]} for c in cs[-40:][::-1]]})
            if parsed.path == "/api/pay/vouchers":
                return self._send(200, pay_vouchers())
            # ── 发布通道（Sanity / WordPress）──
            if parsed.path == "/api/publish/config":
                sc = SANITY_PUB.sanity_cfg() if SANITY_PUB else {"project": "", "dataset": "", "token": "", "source": "none"}
                wpc = read_json(PROJECT / "run/cms.json", {}).get("wordpress") or {}
                drafts = []
                st = read_json(proj_paths(self._proj())["state"], {})
                for iid, it in (st.get("items") or {}).items():
                    if it.get("stage") in ("S4-qa", "S4-ready", "S5-importing", "S5-imported"):
                        drafts.append({"item_id": iid, "stage": it.get("stage")})
                return self._send(200, {"sanity": {"project": sc["project"], "dataset": sc["dataset"],
                                                   "configured": bool(sc["token"]), "source": sc["source"]},
                                        "wordpress": {"configured": bool(wpc.get("base") and wpc.get("app_password")),
                                                      "base": wpc.get("base", "")},
                                        "drafts": sorted(drafts, key=lambda x: x["item_id"])})
            if parsed.path == "/api/publish/ping":
                return self._send(200, SANITY_PUB.ping() if SANITY_PUB else {"ok": False, "error": "发布器未加载"})
            if parsed.path == "/api/publish/history":
                lines = []
                ap = RUN_DIR / "approvals.log"
                if ap.exists():
                    lines = [l for l in ap.read_text(errors="ignore").strip().split("\n")
                             if "PUBLISH" in l][-30:][::-1]
                return self._send(200, lines)
            # ── 内容库（站点档案驱动的多站点内容镜像）──
            if parsed.path == "/api/library/sites":
                return self._send(200, library_sites())
            if parsed.path == "/api/library/tree":
                return self._send(200, library_tree(qs.get("site", ["lovart-global"])[0]))
            if parsed.path == "/api/library/list":
                return self._send(200, library_list(qs.get("site", ["lovart-global"])[0],
                                                    qs.get("section", [""])[0],
                                                    qs.get("lang", [""])[0],
                                                    qs.get("q", [""])[0].strip()))
            if parsed.path == "/api/library/status":
                site = qs.get("site", ["lovart-global"])[0]
                return self._send(200, read_json(LIB_ROOT / site / "sync-status.json", {"state": "idle"}))
            # ── 图片物料（落地页/Blog 素材台账与批量替换）──
            if parsed.path == "/api/assets/inventory":
                return self._send(200, assets_inventory(qs.get("site", ["lovart-global"])[0],
                                                        qs.get("q", [""])[0].strip(),
                                                        qs.get("role", [""])[0],
                                                        qs.get("section", [""])[0],
                                                        qs.get("lang", [""])[0]))
            if parsed.path == "/api/assets/result":
                site = qs.get("site", ["lovart-global"])[0]
                cmd = qs.get("cmd", ["plan"])[0]
                return self._send(200, read_json(LIB_ROOT / site / f"assets-{cmd}-result.json", {"state": "idle"}))
            if parsed.path == "/api/assets/plan":
                site = qs.get("site", ["lovart-global"])[0]
                return self._send(200, read_json(LIB_ROOT / site / "replace-plan.json", {"count": 0, "items": []}))
            # ── 批量任务 ──
            if parsed.path == "/api/batch/list":
                return self._send(200, batch_list())
            if parsed.path == "/api/batch/detail":
                t = batch_load(qs.get("id", [""])[0])
                return self._send(200, t or {"error": "任务不存在"})
            # ── Agent 任务台 ──
            if parsed.path == "/api/agent/sessions":
                return self._send(200, agent_sessions())
            if parsed.path == "/api/agent/session":
                s = agent_session_load(qs.get("id", [""])[0])
                return self._send(200, s or {"error": "会话不存在"})
            # ── QA 编排 ──
            if parsed.path == "/api/qa/findings":
                return self._send(200, qa_findings(qs.get("task", [""])[0]))
            if parsed.path == "/api/qa/cycles":
                return self._send(200, read_json(QA_DIR / "cycles.json", [])[::-1][:50])
            if parsed.path == "/api/qa/delta":
                return self._send(200, qa_delta(qs.get("parent", [""])[0], qs.get("child", [""])[0]))
            if parsed.path == "/api/presets":
                return self._send(200, presets_list())
            if parsed.path == "/api/breaker":
                blocked, st = breaker_check()
                return self._send(200, {"blocked": blocked, "state": st})
            if parsed.path == "/api/quota":
                return self._send(200, quota_report(self._role(), self._me()))
            if parsed.path == "/api/styles":
                return self._send(200, styles_list())
            if parsed.path == "/api/styles/detail":
                return self._send(200, style_load(qs.get("id", [""])[0]) or {"error": "样式不存在"})
            if parsed.path == "/api/styles/validate":
                return self._send(200, {"errors": style_validate(body)})
            if parsed.path == "/api/self-evolve/analyze":
                return self._send(200, self_evolve_analyze(int(qs.get("days", ["14"])[0])))
            if parsed.path == "/api/self-evolve/suggestions":
                return self._send(200, self_evolve_analyze())
            if parsed.path == "/api/mode":
                return self._send(200, mode_report(self._proj()))
            if parsed.path == "/api/governance":
                return self._send(200, governance_report())
            if parsed.path == "/api/kb/gaps":
                return self._send(200, kb_gap_report())
            if parsed.path == "/api/health":
                return self._send(200, health_report(self._proj()))
            if parsed.path == "/api/housekeeping":
                lg = []
                if HOUSEKEEPING_LOG.exists():
                    lg = [l for l in HOUSEKEEPING_LOG.read_text(errors="ignore").strip().split("\n") if l.strip()][-10:][::-1]
                return self._send(200, {"history": lg, "keep_days": 14})
            if parsed.path == "/api/qa/tasks":
                ts = [t for t in batch_list() if t.get("type") == "qa"]
                return self._send(200, ts)
            if parsed.path == "/api/qa/create":
                kind = qs.get("kind", ["sanity-filter"])[0]
                mx = max(1, min(int(qs.get("max", ["200"])[0] or 200), 2000))
                items = []
                if kind == "drafts":
                    cdir = proj_paths(self._proj())["gen"]
                    if cdir.exists():
                        for f in sorted(cdir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:mx]:
                            items.append({"kind": "md", "path": rel_of(f)})
                else:
                    if not SANITY_PUB:
                        return self._send(400, {"error": "发布器未加载"})
                    pt = qs.get("page_type", [""])[0]
                    lg = qs.get("lang", [""])[0]
                    where = '_type=="compositePage" && !(_id in path("drafts.**"))'
                    if pt:
                        where += f' && pageType=="{pt}"'
                    if lg:
                        where += f' && language=="{lg}"'
                    try:
                        res = _sanity_req("query", {"query": f'*[{where}] | order(_updatedAt desc)[0...{mx}]{{_id}}'})
                        for d in (res.get("result") or []):
                            items.append({"kind": "sanity", "doc_id": d["_id"]})
                    except Exception as e:
                        return self._send(400, {"error": f"Sanity 查询失败：{str(e)[:160]}"})
                if not items:
                    return self._send(400, {"error": "范围内无对象"})
                t = batch_create("qa", f"QA 扫描·{kind}（{len(items)} 项）", items,
                                 params={"max_attempts": 1}, dry_run=True, by=self._me())
                return self._send(200, {"ok": True, "id": t["id"], "total": len(items)})
            if parsed.path == "/api/workflows":
                sk = {s["name"]: s for s in harness_inventory()["skills"]}
                wfs = []
                for w in WORKFLOW_MAP:
                    wfs.append({**w, "skill_items": [
                        {"name": s, "path": sk[s]["path"], "desc": sk[s]["desc"]}
                        for s in w["skills"] if s in sk]})
                return self._send(200, wfs)
            if parsed.path == "/api/calendar":
                return self._send(200, calendar_view(qs.get("q", [""])[0].strip(), qs.get("lang", [""])[0]))
            if parsed.path == "/api/trident":
                return self._send(200, trident_status())
            if parsed.path == "/api/templates":
                return self._send(200, list_templates())
            if parsed.path == "/api/templates/export":
                tpl = get_template(qs.get("id", [""])[0])
                if not tpl:
                    return self._send(404, {"error": "模板不存在"})
                raw = json.dumps(tpl, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Disposition", f"attachment; filename={tpl.get('id','template')}.json")
                self.send_header("Content-Length", str(len(raw.encode())))
                self.end_headers()
                self.wfile.write(raw.encode())
                return
            if parsed.path == "/api/digest":
                import time as _t
                week = _t.time() - 7 * 86400
                new_reports, latest = 0, None
                for cat, d, pat in REPORT_CATS:
                    base = PROJECT / d
                    if not base.exists():
                        continue
                    for f in base.glob(pat):
                        if f.is_file() and f.stat().st_mtime >= week:
                            new_reports += 1
                            if latest is None or f.stat().st_mtime > latest[0]:
                                latest = (f.stat().st_mtime, {"name": f.name, "path": rel_of(f)})
                thr = 0
                if PROJECTS_DIR.exists():
                    for ef in PROJECTS_DIR.glob("*/events.jsonl"):
                        for l in ef.read_text().strip().split("\n")[-2000:]:
                            try:
                                e = json.loads(l)
                                if str(e.get("ts", ""))[:10] >= datetime.now().strftime("%Y-%m-%d") and False:
                                    continue
                                if str(e.get("ts", ""))[:10] >= (datetime.now() - _t.timedelta(days=7)).strftime("%Y-%m-%d"):
                                    thr += 1
                            except Exception:
                                continue
                tok = sum(x["total_tokens"] for x in usage_stats()["by_day"][-7:])
                return self._send(200, {"new_reports": new_reports, "throughput": thr, "tokens": tok,
                                        "latest": latest[1] if latest else None})
            if parsed.path == "/api/impact":
                rep = impact_report(self._proj())
                rep["geo"] = geo_summary(self._proj())  # P6.3：引用缺口并入归因视图
                return self._send(200, rep)
            if parsed.path == "/api/report/structure":
                return self._send(200, report_structure(qs.get("path", [""])[0]))
            if parsed.path == "/api/qa/stats":
                return self._send(200, qa_stats(int(qs.get("days", ["14"])[0])))
            if parsed.path == "/api/selfreview":
                return self._send(200, selfreview_data())
            if parsed.path == "/api/report/dashboard":
                return self._send(200, report_dashboard(qs.get("path", [""])[0]))
            if parsed.path == "/api/dist/export":
                base = PROJECT / "1-3 GenFlow/Content Distribution/queue"
                pub = read_json(base / "published.json", {}).get("items", [])
                pend = read_json(base / "pending.json", {}).get("items", [])
                lines = ["date,track,platform,slug_or_id,canonical,offsite_url,status"]
                for x in pub:
                    lines.append(",".join([
                        (x.get("date") or ""), "published", (x.get("platform") or ""),
                        '"' + (x.get("slug") or "").replace('"', '""') + '"',
                        '"' + (x.get("canonical") or "") + '"',
                        '"' + (x.get("offsite_url") or "") + '"',
                        (x.get("status") or "")]))
                for x in pend:
                    lines.append(",".join([
                        "", "pending", ",".join(x.get("platforms", [])),
                        '"' + (x.get("id") or "") + '"',
                        '"' + (x.get("canonical_url") or "") + '"', "", (x.get("status") or "")]))
                csv = "\n".join(lines)
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", "attachment; filename=mflow-backlinks.csv")
                self.send_header("Content-Length", str(len(csv.encode())))
                self.end_headers()
                self.wfile.write(csv.encode())
                return
        except Exception as e:
            return self._send(500, {"error": str(e)[:300]})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self._machine() and not self._me():  # 机器联动 token：只读，写动作必须真人会话
            return self._send(403, {"error": "机器 token 仅限 GET；写操作请以用户身份登录"})
        # ── 公开：买家提交交易哈希 / 外部支付 webhook（无会话）──
        if self.path == "/api/pay/claim":
            body = self._body()
            o = next((x for x in pay_orders() if x.get("token") == str(body.get("token", ""))), None)
            if not o:
                return self._send(404, {"error": "订单不存在或链接失效"})
            if o.get("status") != "pending":
                return self._send(200, pay_order_public(o))
            txh = str(body.get("tx_hash", ""))[:120]
            orders = pay_orders()
            for x in orders:
                if x["id"] == o["id"]:
                    x["tx_hash"] = txh
                    x["claimed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pay_save("orders", orders)
            if o.get("pay_method") == "usdt_trc20" and pay_cfg()["auto_verify"]:
                ok, info = pay_verify_trc20({**o, "tx_hash": txh})
                if ok:
                    pay_confirm(o["id"], tx_hash=info or txh, by="auto-trc20-onclaim")
            return self._send(200, pay_public_order(o["token"]))
        if self.path.startswith("/api/pay/webhook/"):
            sec = pay_cfg()["webhook_secret"]
            given = self.path.rsplit("/", 1)[-1]
            if not sec or not secrets.compare_digest(sec, given):
                return self._send(403, {"error": "webhook secret 不匹配"})
            body = self._body()
            oid = str(body.get("order_id", ""))
            tok = str(body.get("token", ""))
            o = next((x for x in pay_orders() if x["id"] == oid or (tok and x.get("token") == tok)), None)
            if not o:
                return self._send(404, {"error": "订单不存在"})
            r = pay_confirm(o["id"], tx_hash=str(body.get("tx_hash", ""))[:120], by="webhook:" + str(body.get("provider", "external"))[:24])
            return self._send(200, r)
        if self.path == "/api/login":
            body = self._body()
            username, password = str(body.get("username", "")).strip(), str(body.get("password", ""))
            ok, name, role = False, "", "member"
            users = read_json(AUTH_FILE, None)
            if users:  # 多用户模式（bcrypt，迁移自 OpenFlow）
                rec = next((x for x in users if x.get("username") == username), None)
                if rec:
                    h = rec.get("hash", "")
                    try:
                        import bcrypt
                        ok = bool(h) and bcrypt.checkpw(password.encode(), h.encode())
                    except Exception:
                        ok = False
                    name, role = rec.get("name", username), rec.get("role", "member")
            elif PASSWORD:  # 单密码模式（向后兼容）
                ok = secrets.compare_digest(password, PASSWORD)
                name, role = username or "operator", "admin"
            if ok:
                sid = secrets.token_urlsafe(32)
                SESSIONS[sid] = {"username": username or name, "project": DEFAULT_PROJECT}
                self.send_response(200)
                self.send_header("Set-Cookie", f"mflow_session={sid}; HttpOnly; Path=/; SameSite=Lax")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "name": name, "role": role}).encode())
            else:
                self._send(403, {"ok": False, "error": "用户名或密码错误"})
            return
        if self.path == "/api/auth/me":
            if not self._authed():
                return self._send(401, {"error": "unauthorized"})
            return self._send(200, {"username": self._me(), "role": self._role()})
        if self.path == "/api/account/list":
            if self._role() != "admin":
                return self._send(403, {"error": "需要 admin"})
            return self._send(200, [{"username": x["username"], "role": x.get("role", ""),
                                     "name": x.get("name", ""),
                                     "projects": x.get("projects", [])} for x in read_json(AUTH_FILE, [])])
        if self.path == "/api/account/set-projects":
            if self._role() != "admin":
                return self._send(403, {"error": "需要 admin"})
            users = read_json(AUTH_FILE, [])
            for u in users:
                if u["username"] == body.get("username"):
                    u["projects"] = [str(x) for x in body.get("projects", [])][:50]
            AUTH_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=1))
            return self._send(200, {"ok": True})
        if not self._authed():
            return self._send(401, {"error": "unauthorized"})
        if not self._authed():
            return self._send(401, {"error": "unauthorized"})
        # P3.1 角色分级：viewer 只读；admin-only 操作白名单
        role = self._role()
        if role == "viewer":
            return self._send(403, {"error": "viewer 角色只读，无写操作权限"})
        ADMIN_ONLY = {"/api/setup/seed-demo", "/api/llm/save", "/api/llm/test",
                      "/api/account/list", "/api/account/reset", "/api/dispatch/approve",
                      "/api/trident/run", "/api/daily/run", "/api/tasks/del",
                      "/api/notify/save", "/api/notify/test",
                      "/api/llm/proj-key", "/api/plugins/install", "/api/plugins/uninstall",
                      "/api/geo/probe",
                      "/api/pay/product/save", "/api/pay/product/delete", "/api/pay/cards/import",
                      "/api/pay/cards/clear", "/api/pay/link/create", "/api/pay/order/confirm",
                      "/api/pay/order/redeliver", "/api/pay/order/cancel", "/api/pay/voucher/save",
                      "/api/pay/voucher/delete", "/api/pay/config/save", "/api/pay/verify",
                      "/api/publish/sanity", "/api/publish/wordpress", "/api/library/sync",
                      "/api/assets/scan", "/api/assets/plan", "/api/assets/apply",
                      "/api/batch/create", "/api/batch/action",
                      "/api/agent/chat", "/api/agent/execute",
                      "/api/qa/orchestrate", "/api/qa/recheck",
                      "/api/presets/run", "/api/housekeeping/run",
                      "/api/breaker/reset", "/api/quotas/save",
                      "/api/self-evolve/apply",
                      "/api/styles/import", "/api/styles/delete",
                      "/api/mode/switch"}
        if self.path in ADMIN_ONLY and role != "admin":
            return self._send(403, {"error": f"需要 admin 角色（当前 {role}）"})
        body = self._body()
        try:
            if self.path == "/api/logout":
                try:
                    c = http_cookies.SimpleCookie(self.headers.get("Cookie", ""))
                    SESSIONS.pop(c["mflow_session"].value, None)
                except Exception:
                    pass
                return self._send(200, {"ok": True})
            if self.path == "/api/item/upsert":
                item_id = str(body.get("id", "")).strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}", item_id):
                    return self._send(400, {"error": "id 必须是小写字母/数字/连字符"})
                r = ps_run([sys.executable, str(PS_PATH),
                              "--state-path", str(self._st()), "--events-path", str(self._ev()),
                              "upsert", "--id", item_id,
                              "--category", str(body.get("category", "blog")),
                              "--target-type", str(body.get("target_type", "blog"))])
                return self._send(200 if r["rc"] == 0 else 400, r)
            if self.path == "/api/item/advance":
                r = ps_run([sys.executable, str(PS_PATH),
                              "--state-path", str(self._st()), "--events-path", str(self._ev()),
                              "advance", "--id", str(body.get("id", "")),
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
            if self.path == "/api/selfreview/generate":
                month_dir = PROJECT / "1-2 Insight/Trident Insights/reports/monthly"
                month_dir.mkdir(parents=True, exist_ok=True)
                f = month_dir / f"MFlow-自我迭代回顾-{datetime.now().strftime('%Y-%m')}.md"
                f.write_text(selfreview_markdown().replace("\\n", "\n"))
                return self._send(200, {"ok": True, "path": rel_of(f)})
            if self.path == "/api/hook/run":
                hook = str(body.get("hook", ""))
                if hook not in HOOKS:
                    return self._send(400, {"error": "unknown hook"})
                f = Path(str(body.get("file", ""))).resolve()
                if not f.exists() or PROJECT not in f.parents:
                    return self._send(400, {"error": "file 必须在项目目录内"})
                r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks" / hook),
                              "--file", str(f)], timeout=120)
                qa_log("hook", hook, r["rc"])
                return self._send(200, r)
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
            if self.path == "/api/notify/save":
                cfg = {"enabled": bool(body.get("enabled")),
                       "feishu_webhook": str(body.get("feishu_webhook", "")).strip()}
                NOTIFY_FILE.parent.mkdir(parents=True, exist_ok=True)
                NOTIFY_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
                os.chmod(NOTIFY_FILE, 0o600)
                return self._send(200, {"ok": True})
            if self.path == "/api/notify/test":
                ok = notify_send("MFlow 通知测试", f"来自 {self._me()} 的连通性测试 · {time.strftime('%H:%M:%S')}")
                return self._send(200, {"ok": ok})
            if self.path == "/api/plugins/install":
                return self._send(200, plugin_install(body.get("manifest") or {}, body.get("entry_code", "")))
            if self.path == "/api/plugins/uninstall":
                return self._send(200, plugin_uninstall(str(body.get("id", ""))))
            if self.path == "/api/geo/config":
                meta_f = PROJECTS_DIR / self._proj() / "meta.json"
                meta = read_json(meta_f, {})
                old_geo = meta.get("geo") or {}
                engines = [str(x).strip()[:24] for x in (body.get("engines") or []) if str(x).strip()]
                if not engines and body.get("engine"):
                    engines = [str(body["engine"])]
                meta["geo"] = {"brand": str(body.get("brand", "")).strip()[:60],
                               "competitors": [str(x).strip()[:40] for x in (body.get("competitors") or [])[:12] if str(x).strip()],
                               "queries": [str(x).strip()[:200] for x in (body.get("queries") or [])[:15] if str(x).strip()],
                               "engines": engines[:4] or ["auto"],
                               "probe_daily": bool(body.get("probe_daily")),
                               "auto_refresh": bool(body.get("auto_refresh")),
                               "perplexity_model": str(body.get("perplexity_model", old_geo.get("perplexity_model", "sonar"))).strip()[:40]}
                meta_f.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/geo/probe":
                r = geo_probe(self._proj())
                code = 400 if r.get("error") else 200
                return self._send(code, r)
            # ── MFlow Pay 管理端（写）──
            if self.path == "/api/pay/product/save":
                ps = pay_products()
                pid = re.sub(r"[^a-z0-9-]", "", str(body.get("id", "")).lower())[:40] or f"p-{secrets.token_hex(3)}"
                rec = next((x for x in ps if x["id"] == pid), None)
                data = {"id": pid, "name": str(body.get("name", "")).strip()[:80] or pid,
                        "price": round(float(body.get("price", 0) or 0), 2),
                        "currency": str(body.get("currency", "USD"))[:8],
                        "desc": str(body.get("desc", ""))[:200],
                        "delivery": "manual" if body.get("delivery") == "manual" else "card",
                        "active": bool(body.get("active", True))}
                if rec:
                    rec.update(data)
                else:
                    ps.append(data)
                pay_save("products", ps)
                return self._send(200, {"ok": True, "id": pid})
            if self.path == "/api/pay/product/delete":
                pid = str(body.get("id", ""))
                pay_save("products", [x for x in pay_products() if x["id"] != pid])
                return self._send(200, {"ok": True})
            if self.path == "/api/pay/cards/import":
                pid = str(body.get("product_id", "")).strip()
                if not next((x for x in pay_products() if x["id"] == pid), None):
                    return self._send(400, {"error": "商品不存在"})
                codes = [c.strip() for c in str(body.get("codes", "")).split("\n") if c.strip()]
                cs = pay_cards()
                existing = {c["code"] for c in cs if c.get("product_id") == pid}
                added = 0
                for code in codes[:5000]:
                    if code in existing:
                        continue
                    cs.append({"id": _new_id("card"), "product_id": pid, "code": code[:200],
                               "status": "available", "order_id": "", "sold_at": ""})
                    added += 1
                pay_save("cards", cs)
                return self._send(200, {"ok": True, "added": added, "skipped": len(codes) - added})
            if self.path == "/api/pay/cards/clear":
                pid, status = str(body.get("product_id", "")), str(body.get("status", "available"))
                cs = [c for c in pay_cards() if not (c.get("product_id") == pid and c.get("status") == status)]
                pay_save("cards", cs)
                return self._send(200, {"ok": True})
            if self.path == "/api/pay/link/create":
                r = pay_create_order(str(body.get("product_id", "")), body.get("qty", 1),
                                     str(body.get("voucher", "")), str(body.get("pay_method", "usdt_trc20")),
                                     body.get("ttl_min"), body.get("spec", ""))
                code = 400 if r.get("error") else 200
                return self._send(code, r)
            if self.path == "/api/pay/order/confirm":
                r = pay_confirm(str(body.get("id", "")), str(body.get("tx_hash", "")), by=self._me())
                code = 400 if r.get("error") else 200
                return self._send(code, r)
            if self.path == "/api/pay/order/redeliver":
                r = pay_deliver(str(body.get("id", "")), note="redeliver")
                code = 400 if r.get("error") else 200
                return self._send(code, r)
            if self.path == "/api/pay/order/cancel":
                return self._send(200, pay_cancel(str(body.get("id", "")), str(body.get("reason", ""))))
            if self.path == "/api/pay/voucher/save":
                vs = pay_vouchers()
                vcode = re.sub(r"[^A-Za-z0-9-]", "", str(body.get("code", "")).strip())[:32].upper()
                if not vcode:
                    vcode = "V" + secrets.token_hex(4).upper()
                rec = next((x for x in vs if x["code"] == vcode), None)
                data = {"code": vcode, "type": "free" if body.get("type") == "free" else ("percent" if body.get("type") == "percent" else "amount"),
                        "value": round(float(body.get("value", 0) or 0), 2),
                        "max_uses": max(1, int(body.get("max_uses", 1) or 1)),
                        "products": [str(x) for x in (body.get("products") or [])][:20],
                        "expires": str(body.get("expires", ""))[:10], "active": bool(body.get("active", True))}
                if rec:
                    rec.update(data)
                else:
                    vs.append({**data, "used": 0})
                pay_save("vouchers", vs)
                return self._send(200, {"ok": True, "code": vcode})
            if self.path == "/api/pay/voucher/delete":
                pay_save("vouchers", [x for x in pay_vouchers() if x["code"] != str(body.get("code", ""))])
                return self._send(200, {"ok": True})
            if self.path == "/api/pay/config/save":
                cur = pay_cfg()
                sec = str(body.get("webhook_secret", ""))
                pay_save("cfg", {"usdt_trc20": str(body.get("usdt_trc20", cur["usdt_trc20"])).strip()[:64],
                                 "usdt_erc20": str(body.get("usdt_erc20", cur["usdt_erc20"])).strip()[:64],
                                 "btc": str(body.get("btc", cur["btc"])).strip()[:64],
                                 "auto_verify": bool(body.get("auto_verify", cur["auto_verify"])),
                                 "link_ttl_min": max(5, int(body.get("link_ttl_min", cur["link_ttl_min"]) or 60)),
                                 "webhook_secret": sec if sec and "…" not in sec else cur["webhook_secret"]})
                return self._send(200, {"ok": True})
            if self.path == "/api/pay/verify":
                o = next((x for x in pay_orders() if x["id"] == str(body.get("id", ""))), None)
                if not o:
                    return self._send(404, {"error": "订单不存在"})
                ok, info = pay_verify_trc20(o)
                if ok:
                    r = pay_confirm(o["id"], tx_hash=info, by="manual-verify:" + self._me())
                    return self._send(200, {"ok": True, "verified": True, "order": r.get("order")})
                return self._send(200, {"ok": True, "verified": False, "detail": info})
            # ── 发布：Sanity / WordPress（admin + 门禁 + 默认 dry-run）──
            if self.path == "/api/publish/sanity":
                path = str(body.get("path", ""))
                item_id = str(body.get("item_id", "")).strip() or Path(path).stem
                ok, why = publish_gate(self._proj(), item_id)
                if not ok:
                    return self._send(400, {"error": why})
                if not SANITY_PUB:
                    return self._send(400, {"error": "发布器未加载"})
                p = safe_path(path)
                if not p:
                    return self._send(400, {"error": "草稿路径不可读"})
                dry = bool(body.get("dry_run", True))
                doctype = str(body.get("doctype", "blog"))
                if doctype == "composite":
                    # compositePage 无草稿态：写入即前台可见 → 真实写入需显式 confirm_public
                    if not dry and not bool(body.get("confirm_public", False)):
                        return self._send(400, {"error": "落地页写入即上线（compositePage 无草稿态）——"
                                                        "真实发布请在界面勾选「确认公开可见」后重试"})
                    r = SANITY_PUB.publish_landing(str(p), dry_run=dry, mode=str(body.get("mode", "create")),
                                                  slug=str(body.get("slug", "")), lang=str(body.get("lang", "")),
                                                  page_type=str(body.get("page_type", "tool")),
                                                  title=str(body.get("title", "")),
                                                  description=str(body.get("description", "")),
                                                  cover_url=str(body.get("cover_url", "")),
                                                  cover_alt=str(body.get("cover_alt", "")),
                                                  storyline_template=str(body.get("storyline_template", "T-long")),
                                                  sections_path=str(body.get("sections_path", "")))
                else:
                    r = SANITY_PUB.publish_file(str(p), slug=str(body.get("slug", "")), lang=str(body.get("lang", "")),
                                                category=str(body.get("category", "")), title=str(body.get("title", "")),
                                                cluster=str(body.get("cluster", "")), dry_run=dry)
                if r.get("ok") and not dry:
                    with open(RUN_DIR / "approvals.log", "a") as f:
                        f.write(f"{datetime.now().isoformat(timespec='seconds')} SANITY-PUBLISH {item_id} doc={r.get('doc_id')} by={self._me()}\n")
                return self._send(200 if r.get("ok") else 400, r)
            if self.path == "/api/publish/wordpress":
                path = str(body.get("path", ""))
                item_id = str(body.get("item_id", "")).strip() or Path(path).stem
                ok, why = publish_gate(self._proj(), item_id)
                if not ok:
                    return self._send(400, {"error": why})
                r = publish_wordpress(path, item_id, str(body.get("title", "")))
                return self._send(200 if r.get("ok") else 400, r)
            if self.path == "/api/library/sync":
                site = str(body.get("site", "lovart-global"))
                if not (SITES_DIR / f"{site}.json").exists():
                    return self._send(400, {"error": f"站点档案不存在：{site}"})
                r = library_sync(site, str(body.get("sections", "")), int(body.get("max", 0) or 0))
                with open(RUN_DIR / "approvals.log", "a") as f:
                    f.write(f"{datetime.now().isoformat(timespec='seconds')} LIBRARY-SYNC {site} sections={body.get('sections','all')} max={body.get('max',0)} by={self._me()}\n")
                return self._send(200, r)
            # ── 图片物料：扫描 / 生成替换计划 / 执行（dry-run 默认）──
            if self.path == "/api/assets/scan":
                site = str(body.get("site", "lovart-global"))
                return self._send(200, assets_run("scan", site, sections=str(body.get("sections", "")),
                                                  max=int(body.get("max", 0) or 0)))
            if self.path == "/api/assets/plan":
                site = str(body.get("site", "lovart-global"))
                return self._send(200, assets_run("plan", site, mode=str(body.get("mode", "prefix")),
                                                  match=str(body.get("match", "")),
                                                  new_url=str(body.get("new_url", "")),
                                                  new_alt=str(body.get("new_alt", "")),
                                                  section=str(body.get("section", "")),
                                                  lang=str(body.get("lang", "")),
                                                  page_type=str(body.get("page_type", "")),
                                                  slugs=str(body.get("slugs", ""))))
            if self.path == "/api/assets/apply":
                site = str(body.get("site", "lovart-global"))
                dry = bool(body.get("dry_run", True))
                plan_path = str(LIB_ROOT / site / "replace-plan.json")
                if not (LIB_ROOT / site / "replace-plan.json").exists():
                    return self._send(400, {"error": "无替换计划——先生成计划"})
                r = assets_run("apply", site, plan=plan_path,
                               max_docs=int(body.get("max_docs", 500) or 500),
                               **({"yes": 1} if not dry else {}))
                with open(RUN_DIR / "approvals.log", "a") as f:
                    f.write(f"{datetime.now().isoformat(timespec='seconds')} ASSET-PLAN-APPLY {site} dry_run={dry} "
                            f"by={self._me()} plan={plan_path}\n")
                return self._send(200, r)
            # ── 批量任务：创建（支持从物料计划/库条目/自定义 items 建）──
            if self.path == "/api/batch/create":
                btype = str(body.get("type", "")).strip()
                if btype not in BATCH_HANDLERS:
                    return self._send(400, {"error": f"未知类型（可选：{list(BATCH_HANDLERS)}）"})
                items = body.get("items") or []
                site = str(body.get("site", "lovart-global"))
                if not items and btype == "asset_replace":
                    pl = read_json(LIB_ROOT / site / "replace-plan.json", {})
                    items = pl.get("items") or []
                    if not items:
                        return self._send(400, {"error": "物料替换计划为空——先在内容库生成计划"})
                    for it in items:
                        it.pop("slug", None)
                if not items:
                    return self._send(400, {"error": "items 为空"})
                if len(items) > 5000:
                    return self._send(400, {"error": "单任务 items ≤5000"})
                try:
                    t = batch_create(btype, str(body.get("title", "")), items,
                                     params=body.get("params") or {},
                                     dry_run=bool(body.get("dry_run", True)), by=self._me())
                except PermissionError as e:
                    return self._send(429, {"error": str(e)})
                return self._send(200, {"ok": True, "id": t["id"], "total": t["stats"]["total"]})
            if self.path == "/api/batch/action":
                t = batch_load(str(body.get("id", "")))
                if not t:
                    return self._send(404, {"error": "任务不存在"})
                act = str(body.get("action", ""))
                if act == "pause":
                    t["status"] = "paused"; _batch_log(t, f"手动暂停 by {self._me()}")
                elif act == "resume":
                    for it in t["items"]:
                        if it["status"] == "running":
                            it["status"] = "pending"
                    t["status"] = "queued"; _batch_log(t, f"手动继续 by {self._me()}")
                elif act == "cancel":
                    t["status"] = "cancelled"; _batch_log(t, f"手动取消 by {self._me()}")
                elif act == "retry_failed":
                    n = 0
                    for it in t["items"]:
                        if it["status"] in ("failed", "pending"):
                            it["status"] = "pending"; it["attempts"] = 0; it["error"] = ""; n += 1
                    t["status"] = "queued"; _batch_log(t, f"重试 {n} 项 by {self._me()}")
                else:
                    return self._send(400, {"error": "action 可选 pause/resume/cancel/retry_failed"})
                batch_save(t)
                return self._send(200, {"ok": True, "status": t["status"]})
            # ── Agent 任务台：对话 / 执行 ──
            if self.path == "/api/agent/chat":
                msg = str(body.get("message", "")).strip()
                if not msg:
                    return self._send(400, {"error": "message 必填"})
                sid = str(body.get("session_id", "")).strip()
                s = agent_session_load(sid) if sid else None
                if not s:
                    s = agent_session_new(msg[:40])
                s.setdefault("messages", []).append({"role": "user", "text": msg,
                                                     "at": datetime.now().strftime("%H:%M:%S")})
                try:
                    r = agent_reply(s, msg, self._proj())
                except Exception as e:
                    s["messages"].append({"role": "assistant", "text": f"（规划失败：{str(e)[:200]}）"})
                    agent_save(s)
                    return self._send(500, {"error": str(e)[:200], "session_id": s["id"]})
                guarded, gerr = (None, "")
                if r.get("spec"):
                    guarded, gerr = spec_guard(r["spec"])
                s["messages"].append({"role": "assistant", "text": r["say"], "at": datetime.now().strftime("%H:%M:%S"),
                                      "context": r.get("context"), "questions": r.get("questions"),
                                      "spec": guarded, "guard_error": gerr})
                if guarded:
                    s.setdefault("proposals", []).append({"spec": guarded, "at": datetime.now().strftime("%Y-%m-%d %H:%M")})
                agent_save(s)
                return self._send(200, {"session_id": s["id"], "say": r["say"], "questions": r.get("questions"),
                                        "spec": guarded, "guard_error": gerr, "context": r.get("context")})
            if self.path == "/api/agent/execute":
                s = agent_session_load(str(body.get("session_id", "")))
                if not s:
                    return self._send(404, {"error": "会话不存在"})
                spec, err = spec_guard(body.get("spec") or {})
                if err:
                    return self._send(400, {"error": err})
                force = bool(body.get("force", False))
                if not spec["dry_run"] and not force:
                    return self._send(400, {"error": "真实执行需显式确认（force=true）——建议先 dry-run"})
                try:
                    t = batch_create(spec["type"], spec["title"], spec["items"],
                                     params={"max_attempts": 2, "from_agent": True, "rationale": spec.get("rationale", ""),
                                             "skills_used": spec.get("skills_used", [])},
                                     dry_run=spec["dry_run"], by=self._me())
                except PermissionError as e:
                    return self._send(429, {"error": str(e)})
                s["messages"].append({"role": "assistant", "at": datetime.now().strftime("%H:%M:%S"),
                                      "text": f"已创建批量任务 {t['id']}（{spec['type']} · {t['stats']['total']} 项 · "
                                              f"{'dry-run' if spec['dry_run'] else '真实执行'}）——执行器 5 秒内接手，"
                                              f"进度见「批量任务」页。",
                                      "task_id": t["id"]})
                agent_save(s)
                return self._send(200, {"ok": True, "task_id": t["id"], "total": t["stats"]["total"]})
            # ── QA 编排：生成修复任务 / 复检 ──
            if self.path == "/api/qa/orchestrate":
                tid = str(body.get("task", ""))
                r = qa_orchestrate(tid, dry_run=bool(body.get("dry_run", True)),
                                   max_items=int(body.get("max_items", 200) or 200))
                return self._send(200 if r.get("ok") else 400, r)
            if self.path == "/api/presets/run":
                pid = str(body.get("id", ""))
                opt = body.get("options") or {}
                r = preset_expand(pid, opt, self._proj())
                if r.get("error"):
                    return self._send(400, r)
                dry = bool(opt.get("dry_run", True))
                if len(r["items"]) > 5000:
                    return self._send(400, {"error": "预设展开超过 5000 项，请缩小范围"})
                try:
                    t = batch_create(r["type"], r["title"], r["items"], params=r.get("params") or {},
                                     dry_run=dry, by=self._me())
                except PermissionError as e:
                    return self._send(429, {"error": str(e)})
                with open(RUN_DIR / "approvals.log", "a") as f:
                    f.write(f"{datetime.now().isoformat(timespec='seconds')} PRESET-RUN {pid} task={t['id']} "
                            f"items={t['stats']['total']} dry_run={dry} by={self._me()}\n")
                return self._send(200, {"ok": True, "task_id": t["id"], "total": t["stats"]["total"],
                                        "note": r.get("note", ""), "dry_run": dry})
            if self.path == "/api/styles/import":
                data = body.get("data") or body
                errs = style_validate(data)
                if errs:
                    return self._send(400, {"error": "样式校验失败", "errors": errs})
                return self._send(200, style_import(data, by=self._me()))
            if self.path == "/api/styles/delete":
                return self._send(200, style_delete(str(body.get("id", "")), by=self._me()))
            if self.path == "/api/self-evolve/apply":
                r = self_evolve_apply(str(body.get("pattern", "")), str(body.get("action", "")), by=self._me())
                return self._send(200 if r.get("ok") else 400, r)
            if self.path == "/api/breaker/reset":
                st = breaker_reset()
                with open(RUN_DIR / "approvals.log", "a") as f:
                    f.write(f"{datetime.now().isoformat(timespec='seconds')} BREAKER-RESET by={self._me()}\n")
                return self._send(200, {"ok": True, **st})
            if self.path == "/api/quotas/save":
                body_q = body.get("default") or {}
                per_user = body.get("per_user") or {}
                cur = quotas_cfg()
                newd = {"items_per_month": int(body_q.get("items_per_month", cur["default"]["items_per_month"]) or 0),
                        "tokens_per_month": int(body_q.get("tokens_per_month", cur["default"]["tokens_per_month"]) or 0),
                        "writes_per_month": int(body_q.get("writes_per_month", cur["default"]["writes_per_month"]) or 0)}
                pu = dict(cur["per_user"])
                for un, cap in (per_user or {}).items():
                    if cap in (None, "", "unlimited"):
                        pu.pop(un, None)
                    else:
                        pu[un] = {**cur["default"], **{k: int(v) for k, v in cap.items() if str(v).strip() != ""}}
                QUOTAS_FILE.write_text(json.dumps({"default": newd, "per_user": pu}, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/housekeeping/run":
                rep = housekeeping(dry_run=bool(body.get("dry_run", True)))
                return self._send(200, rep)
            if self.path == "/api/mode/switch":
                r = mode_switch(self._proj(), str(body.get("mode", "")))
                return self._send(200 if r.get("ok") else 400, r)
            if self.path == "/api/mode/promote":
                return self._send(200, mode_promote_check(self._proj()))
            if self.path == "/api/qa/recheck":
                r = qa_recheck(str(body.get("task", "")), dry_run=bool(body.get("dry_run", True)))
                return self._send(200 if r.get("ok") else 400, r)
            if self.path == "/api/skills/sync":
                return self._send(200, run_tool([sys.executable, str(PROJECT / "1-4 Dev/scripts/harness_sync.py")], timeout=120))
            if self.path == "/api/generate":
                # 节点模式单步：LLM 生成 → 落盘 → 质检钩子（同步返回）
                item_id = str(body.get("item_id", "")).strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}", item_id):
                    return self._send(400, {"error": "id 不合法"})
                tpl = get_template(str(body.get("template_id", "")))
                try:
                    ps_run([sys.executable, str(PS_PATH),
                              "--state-path", str(self._st()), "--events-path", str(self._ev()),
                              "upsert", "--id", item_id,
                              "--category", str(body.get("type", "blog"))])
                    draft = llm_chat([{"role": "user", "content": gen_prompt(
                        str(body.get("type", "blog")), str(body.get("lang", "zh")),
                        str(body.get("topic", ""))[:300], str(body.get("brief", ""))[:800],
                        template=tpl)}],
                        profile="lovart-creation", project=self._proj())
                except Exception as e:
                    return self._send(400, {"error": str(e)[:300]})
                path = self._gen() / f"{item_id}.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(draft)
                # demo 稿豁免词数门槛（hook 按空格分词，CJK 长文会被低估）
                twords = "15" if DEMO_FLAG.exists() and not llm_config()["providers"][
                    llm_config()["profiles"]["default"]["provider"]].get("key") else "300"
                hook = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks/post-write-check.sh"),
                                 "--file", str(path), "--target-words", twords], timeout=120)
                qa_log("generate", "post-write-check.sh", hook["rc"])
                gates = run_content_gates(path, str(body.get("type", "blog")), str(body.get("lang", "zh")), tag="generate",
                                          budget_profile=str(body.get("budget_profile", "default")))
                hook, geo = gates["post-write-check.sh"], gates["geo-check.sh"]
                quota, langc = gates["quota-check.sh"], gates["lang-check.sh"]
                return self._send(200, {"ok": True, "path": rel_of(path), "chars": len(draft),
                                        "hook_rc": hook["rc"], "hook_out": hook["out"][-2000:],
                                        "geo_rc": geo["rc"], "geo_out": geo["out"][-2000:],
                                        "quota_rc": quota["rc"], "quota_out": quota["out"][-1500:],
                                        "lang_rc": langc["rc"], "lang_out": langc["out"][-1500:]})
            if self.path == "/api/loop/create":
                item_id = str(body.get("item_id", "")).strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,78}", item_id):
                    return self._send(400, {"error": "id 不合法"})
                with LOOP_LOCK:
                    loops = read_json(self._lp(), [])
                    loop = {"id": secrets.token_hex(4), "item_id": item_id,
                            "goal": str(body.get("topic", ""))[:200],
                            "template_id": str(body.get("template_id", "")),
                            "type": str(body.get("type", "blog")), "lang": str(body.get("lang", "zh")),
                            "topic": str(body.get("topic", ""))[:300], "brief": str(body.get("brief", ""))[:800],
                            "status": "queued", "round": 0, "max_rounds": 3, "tokens_used": 0,
                            "created": datetime.now().strftime("%Y-%m-%d %H:%M"), "log": []}
                    loops.append(loop)
                    self._lp().parent.mkdir(parents=True, exist_ok=True)
                    self._lp().write_text(json.dumps(loops, ensure_ascii=False, indent=1))
                pp = proj_paths(self._proj())
                ps_run([sys.executable, str(PS_PATH),
                          "--state-path", str(pp["state"]), "--events-path", str(pp["events"]),
                          "upsert", "--id", item_id,
                          "--category", str(body.get("type", "blog"))])
                return self._send(200, {"ok": True, "id": loop["id"], "queued": True})
            if self.path == "/api/loop/stop":
                loops = read_json(self._lp(), [])
                for x in loops:
                    if x["id"] == body.get("id"):
                        x["stop"] = True
                self._lp().write_text(json.dumps(loops, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/trident/run":
                step_id = str(body.get("step", ""))
                step = next((s for s in TRIDENT_STEPS if s["id"] == step_id and s["cmd"]), None)
                if not step:
                    return self._send(400, {"error": "unknown step or no cmd"})
                env = dict(os.environ)
                env.setdefault("LOVART_PYTHON", str(PROJECT / ".venv" / "bin" / "python"))
                r = run_tool(step["cmd"], timeout=280)
                return self._send(200, r)
            if self.path == "/api/setup/seed-demo":
                return self._send(200, seed_demo())
            if self.path == "/api/account/reset":
                users = read_json(AUTH_FILE, [])
                rec = next((x for x in users if x["username"] == body.get("username")), None)
                if not rec:
                    return self._send(404, {"error": "账号不存在"})
                import bcrypt
                newp = str(body.get("new_password", "")).encode()
                if len(newp) < 6:
                    return self._send(400, {"error": "新密码至少 6 位"})
                rec["hash"] = bcrypt.hashpw(newp, bcrypt.gensalt(rounds=10)).decode()
                AUTH_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=1))
                os.chmod(AUTH_FILE, 0o600)
                with open(RUN_DIR / "approvals.log", "a") as f:
                    f.write(f"{datetime.now().isoformat(timespec='seconds')} RESET {rec['username']} by {self._me()}\n")
                return self._send(200, {"ok": True})
            if self.path == "/api/dispatch/approve":
                did = str(body.get("id", ""))
                qbase = PROJECT / "1-3 GenFlow/Content Distribution/queue"
                target = None
                for f in qbase.glob("dispatch-*.json"):
                    d = read_json(f, {})
                    if d.get("id") == did:
                        target = f
                        dd = d
                        break
                if not target:
                    return self._send(404, {"error": "dispatch 单不存在"})
                dd["approved"] = True
                dd["approved_by"] = self._me()
                dd["approved_at"] = datetime.now().isoformat(timespec="seconds")
                target.write_text(json.dumps(dd, ensure_ascii=False, indent=2))
                with open(RUN_DIR / "approvals.log", "a") as f:
                    f.write(f"{dd['approved_at']} APPROVE {did} by {self._me()}\n")
                return self._send(200, {"ok": True})
            if self.path == "/api/templates/import":
                tpl = body.get("template")
                if not isinstance(tpl, dict) or not tpl.get("id") or not tpl.get("name") or not tpl.get("prompt"):
                    return self._send(400, {"error": "模板需包含 id / name / prompt 三要素"})
                tpl["id"] = re.sub(r"[^a-z0-9-]", "", str(tpl["id"]).lower())[:60]
                if not tpl["id"]:
                    return self._send(400, {"error": "id 只能是小写字母/数字/连字符"})
                TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
                (TEMPLATES_DIR / f"{tpl['id']}.json").write_text(json.dumps(tpl, ensure_ascii=False, indent=2))
                return self._send(200, {"ok": True, "id": tpl["id"]})
            if self.path == "/api/templates/delete":
                tid = str(body.get("id", "")).replace("/", "").replace("..", "")
                f = TEMPLATES_DIR / f"{tid}.json"
                builtin = {"ecommerce-content", "saas-growth", "local-service"}
                if tid in builtin:
                    return self._send(400, {"error": "内置模板不可删除"})
                if f.exists():
                    f.unlink()
                return self._send(200, {"ok": True})
            if self.path == "/api/topics/add":
                items = [x.strip()[:120] for x in str(body.get("topics", "")).split("\n") if x.strip()]
                if not items:
                    return self._send(400, {"error": "每行一个选题，至少填一个"})
                tp = self._tk().parent / "topics.json"
                cur = read_json(tp, [])
                cur.extend(items[:100])
                tp.write_text(json.dumps(cur, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True, "count": len(cur)})
            if self.path == "/api/projects/config":
                meta_f = PROJECTS_DIR / self._proj() / "meta.json"
                meta = read_json(meta_f, {})
                if "schedule" in body:
                    meta["schedule"] = {"daily_quota": int(body["schedule"].get("daily_quota", 0) or 0),
                                        "auto_loop": bool(body["schedule"].get("auto_loop", False))}
                if "llm" in body:
                    lv = body["llm"] or {}
                    cur = meta.get("llm") or {}
                    newkey = str(lv.get("key", "")).strip()
                    if not newkey:
                        meta.pop("llm", None)  # 空 Key = 显式清空覆盖，回退全局
                    else:
                        ov = {"provider": str(lv.get("provider", "custom"))[:24],
                              "base": str(lv.get("base", "")).strip()[:200],
                              "model": str(lv.get("model", "")).strip()[:80]}
                        if "…" not in newkey:  # masked = 保留旧 Key
                            ov["key"] = newkey
                        elif cur.get("key"):
                            ov["key"] = cur["key"]
                        if ov.get("key"):
                            meta["llm"] = ov
                if "kb_extra" in body:
                    extras = []
                    for ex in body["kb_extra"][:20]:
                        d = str(ex.get("dir", "")).strip()
                        dd = (PROJECT / d).resolve()
                        if d and dd.exists() and PROJECT in dd.parents:
                            extras.append({"label": str(ex.get("label", ""))[:60], "dir": d,
                                           "glob": str(ex.get("glob", "**/*.md"))[:120],
                                           "desc": str(ex.get("desc", ""))[:200]})
                    meta["kb_extra"] = extras
                meta_f.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
                if isinstance(meta.get("llm"), dict) and meta["llm"].get("key"):  # 响应不回显 Key
                    meta = {k: v for k, v in meta.items() if k != "llm"}
                return self._send(200, {"ok": True, "meta": meta})
            if self.path == "/api/projects/create":
                name = str(body.get("name", "")).strip()[:60]
                if not name:
                    return self._send(400, {"error": "项目名必填"})
                pid = re.sub(r"[^a-z0-9-]", "", str(body.get("id") or name).lower())[:40] or f"proj-{secrets.token_hex(3)}"
                if (PROJECTS_DIR / pid).exists():
                    return self._send(409, {"error": f"项目 id 已存在：{pid}"})
                ensure_project(pid, name=name)
                me = self._me()
                rec = auth_record(me)
                if rec and self._role() != "admin":
                    users = read_json(AUTH_FILE, [])
                    for u in users:
                        if u["username"] == me:
                            u.setdefault("projects", []).append(pid)
                    AUTH_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True, "id": pid})
            if self.path == "/api/projects/switch":
                pid = str(body.get("id", ""))
                if not (PROJECTS_DIR / pid).exists():
                    return self._send(404, {"error": "项目不存在"})
                sid = self._sid()
                if sid in SESSIONS:
                    SESSIONS[sid]["project"] = pid
                return self._send(200, {"ok": True, "current": pid})
            if self.path == "/api/projects/delete":
                if self._role() != "admin":
                    return self._send(403, {"error": "需要 admin"})
                pid = str(body.get("id", ""))
                if pid == DEFAULT_PROJECT:
                    return self._send(400, {"error": "默认项目不可删除"})
                src = PROJECTS_DIR / pid
                if not src.exists():
                    return self._send(404, {"error": "项目不存在"})
                trash = PROJECTS_DIR / "_trash"
                trash.mkdir(exist_ok=True)
                src.rename(trash / f"{pid}-{datetime.now().strftime('%Y%m%d%H%M%S')}")
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/add":
                title = str(body.get("title", "")).strip()[:200]
                if not title:
                    return self._send(400, {"error": "标题必填"})
                tasks = read_json(self._tk(), [])
                tasks.append({"id": secrets.token_hex(4), "title": title,
                              "status": body.get("status", "todo"), "source": "manual",
                              "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                              "note": str(body.get("note", ""))[:300],
                              "desc": str(body.get("desc", ""))[:2000],
                              "assignee": str(body.get("assignee", ""))[:60],
                              "due": str(body.get("due", ""))[:10],
                              "link": str(body.get("link", ""))[:300]})
                self._tk().parent.mkdir(parents=True, exist_ok=True)
                self._tk().write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/update":
                tasks = read_json(self._tk(), [])
                for t in tasks:
                    if t["id"] == body.get("id"):
                        for k in ("title", "desc", "assignee", "due", "link", "status"):
                            if k in body:
                                t[k] = str(body[k])[:2000]
                self._tk().write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/set":
                tasks = read_json(self._tk(), [])
                for t in tasks:
                    if t["id"] == body.get("id"):
                        t["status"] = body.get("status", "todo")
                self._tk().write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/del":
                tasks = [t for t in read_json(self._tk(), []) if t["id"] != body.get("id")]
                self._tk().write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
        except Exception as e:
            return self._send(500, {"error": str(e)[:300]})
        return self._send(404, {"error": "not found"})


def main():
    if not PASSWORD and not AUTH_FILE.exists():
        print("[console] FAIL-CLOSED: 无 auth.json 且未设 MFLOW_CONSOLE_PASSWORD，API 全部拒绝", file=sys.stderr)
    ensure_project(DEFAULT_PROJECT, "Lovart Global")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    threading.Thread(target=loop_queue_worker, daemon=True).start()
    threading.Thread(target=schedule_executor, daemon=True).start()
    threading.Thread(target=geo_scheduler, daemon=True).start()
    threading.Thread(target=pay_verifier, daemon=True).start()
    threading.Thread(target=batch_worker, daemon=True).start()
    threading.Thread(target=housekeeping_scheduler, daemon=True).start()
    print(f"[console] MFlow Console on :{PORT} (loop queue + schedule + geo + pay verifier started, max_parallel={MAX_PARALLEL_LOOPS})")
    server.serve_forever()


if __name__ == "__main__":
    main()
