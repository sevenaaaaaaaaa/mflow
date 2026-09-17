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
                run_tool([sys.executable, str(PS_PATH),
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


def run_content_gates(path, ctype="blog", lang="zh", tag="gate"):
    """统一内容门禁：结构/反slop + GEO 可引用性 + 数量预算 + 语言规范。"""
    args_by_hook = {
        "post-write-check.sh": ["--target-words", "300"],
        "geo-check.sh": [],
        "quota-check.sh": ["--type", "landing" if str(ctype).startswith("landing") else "blog", "--lang", lang or "zh"],
        "lang-check.sh": ["--lang", lang or "zh"],
    }
    out = {}
    for hook, extra in args_by_hook.items():
        r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks" / hook), "--file", str(path), *extra], timeout=120)
        qa_log(tag, hook, r["rc"])
        out[hook] = r
    return out


def gen_prompt(ctype, lang, topic, brief, feedback="", template=None):
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
    anti = ANTI_SLOP + "\n" + GEO_RULES + "\n" + CONTENT_BUDGET + (f"\n语言规范：{lang_rule}" if lang_rule else "") + (f"\n{extra}" if extra else "")
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
        run_tool([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item, "--to", "S3-creating"])
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
                run_tool([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item, "--to", stg])
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
    tid = f"batch-{datetime.now().strftime('%y%m%d')}-{secrets.token_hex(3)}"
    task = {"id": tid, "type": btype, "title": title or btype,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "created_by": by, "dry_run": bool(dry_run),
            "params": {"batch_size": 5, "context_handoff": True, **(params or {})}, "concurrency": 2,
            "status": "queued", "log": [],
            "items": [{"i": i, "status": "pending", "attempts": 0, "result": None, "error": "", **it}
                      for i, it in enumerate(items)]}
    task["stats"] = {"total": len(task["items"]), "done": 0, "failed": 0, "skipped": 0}
    batch_save(task)
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
    return {"dry_run": task.get("dry_run"), "transactionId": res.get("transactionId"), "set": list(sets)}


def run_generation(proj, item_id, ctype="blog", lang="zh", topic="", brief="", template_id="",
                   instruction="", source_text="", prior_context=""):
    """批量生成/改稿共用执行体：LLM → 落盘 → post-write + geo 门禁 → 状态机推进。"""
    ps_args = ["--state-path", str(proj_paths(proj)["state"]), "--events-path", str(proj_paths(proj)["events"])]
    run_tool([sys.executable, str(PS_PATH), *ps_args, "upsert", "--id", item_id, "--category", ctype])
    # 状态机顺序：先入 S3-creating（与 Loop 引擎一致，S0-todo 不可直达 S3-draft）
    run_tool([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item_id, "--to", "S3-creating"])
    user = gen_prompt(ctype, lang, topic, brief, template=get_template(template_id))
    if instruction:
        user = (f"下面是既有内容，请按指令改写（事实准确优先；不确定的数字标 [待考证]）：\n"
                f"指令：{instruction}\n\n现有内容：\n{source_text[:12000]}\n\n" + user)
    if prior_context:
        user = (f"【前序批次上下文（避免重复，保持口径一致）】\n{prior_context[:1500]}\n\n" + user)
    draft = llm_chat([{"role": "user", "content": user}], profile="lovart-creation", max_tokens=4000, project=proj)
    gen_dir = proj_paths(proj)["gen"]
    gen_dir.mkdir(parents=True, exist_ok=True)
    path = gen_dir / f"{item_id}.md"
    path.write_text(draft)
    gates = run_content_gates(path, ctype, lang, tag=f"batch:{item_id}")
    hw, geo = gates["post-write-check.sh"], gates["geo-check.sh"]
    quota, langc = gates["quota-check.sh"], gates["lang-check.sh"]
    advanced = False
    if hw["rc"] == 0 and geo["rc"] == 0 and quota["rc"] == 0 and langc["rc"] == 0:
        rcs = []
        for stg in ("S3-draft", "S3-done", "S4-qa"):
            r = run_tool([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item_id, "--to", stg])
            rcs.append(r.get("rc"))
        advanced = all(rc == 0 for rc in rcs)
    return {"path": rel_of(path), "chars": len(draft), "hook_rc": hw["rc"], "geo_rc": geo["rc"],
            "quota_rc": quota["rc"], "lang_rc": langc["rc"], "advanced": advanced,
            "blocked": [k for k, v in gates.items() if v["rc"] != 0]}


def _bh_gen(item, task, proj):
    return run_generation(proj, item["item_id"], ctype=item.get("type", "blog"), lang=item.get("lang", "zh"),
                          topic=item.get("topic", ""), brief=item.get("brief", ""),
                          template_id=item.get("template_id", ""), prior_context=task.get("ctx_digest", ""))


def _bh_rewrite(item, task, proj):
    src = ""
    if item.get("source_path"):
        sp = safe_path(item["source_path"])
        if sp:
            src = sp.read_text(errors="ignore")
    return run_generation(proj, item["item_id"], ctype=item.get("type", "blog"), lang=item.get("lang", "zh"),
                          topic=item.get("topic", item.get("slug", "")), brief=item.get("brief", ""),
                          instruction=item.get("instruction", ""), source_text=src,
                          prior_context=task.get("ctx_digest", ""))


BATCH_HANDLERS = {"asset_replace": _bh_asset_replace, "field_patch": _bh_field_patch,
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
                batch_save(task)
            st = task["stats"]
            st["done"] = sum(1 for i in task["items"] if i["status"] == "done")
            st["failed"] = sum(1 for i in task["items"] if i["status"] == "failed")
            st["skipped"] = sum(1 for i in task["items"] if i["status"] == "skipped")
            if task.get("status") == "paused":
                _batch_log(task, "已暂停")
            elif task.get("status") == "cancelled":
                _batch_log(task, "已取消")
            elif st["failed"] or any(i["status"] == "pending" for i in task["items"]):
                task["status"] = "failed"
                _batch_log(task, f"结束：done={st['done']} failed={st['failed']} skipped={st['skipped']}（可重试失败项）")
            else:
                task["status"] = "done"
                task["finished"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                _batch_log(task, f"完成：done={st['done']} skipped={st['skipped']}")
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
                        run_tool([sys.executable, str(PS_PATH),
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
    nt = batch_create("qa", f"QA 复检（源 {tid}）", items, params={"from_qa": tid}, dry_run=dry_run, by="qa-recheck")
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


def context_rules(limit=4000):
    """harness 硬约束摘要：编号/项目符号列表中含「禁止/必须/不可/一律/永远/不得」的条款。"""
    out = []
    for f in sorted((PROJECT / "1-1 Harness" / "02-rules").glob("RULES-*.md")):
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
    libs = context_library(site, message)
    geo = context_geo(proj)
    rules = context_rules()
    sys_prompt = f"""你是 MFlow 的任务规划器（不是聊天机器人）。用户用自然语言提需求，你要产出**可执行的批量任务规格**。

【硬约束（不可违背，来自 harness 铁律）】
- 生产写入（Sanity/发布）默认 dry-run；真实写入必须由用户显式批准并留下审计
- 不得执行破坏性操作；不得绕过质检门禁；不得自动发布
- 单任务规模：asset_replace/field_patch ≤200 项；gen/rewrite ≤20 项
- 只允许下列任务类型与字段，不得发明新字段

{AGENT_TASK_SCHEMA}

【可用素材与状态】
站点：{site}（{site} 内容库 17.5k 篇；物料台账已建）
GEO：品牌提及率 {geo.get('brand_rate')}，综合分 {geo.get('score')}；缺口查询：{geo.get('gaps')}

【相关 skills（供你理解流程与规范）】
{chr(10).join(f"- {s['name']}（{s['group']}）：{s['desc'][:110]}" for s in skills) or "（无命中）"}

【内容库命中（可能是要改的对象或参考）】
{chr(10).join(f"- {h['path']}｜{h['head'][:120]}" for h in libs) or "（无命中）"}

【harness 规则摘要（执行时同样会被强制）】
{rules}

【输出格式（严格 JSON，不要多余文字）】
{{"say": "给用户的回复（中文，简洁，含你的判断与建议）",
 "questions": ["需要用户补充的信息，最多2条，没有就空数组"],
 "spec": null 或 {{"type":"…","title":"…","dry_run":true,"items":[…],"rationale":"为什么这样","skills_used":["…"]}}}}

规则：
1) 若信息不足（如目标对象不明、缺新值），先问 questions，spec 置 null
2) 若能形成方案，务必给出 spec（默认 dry_run=true）；items 必须具体可执行（doc_id/slug/path 要真实，可用库命中里的路径）
3) 不确定的数字/事实不要编造；宁可在 say 里说明限制
4) 讲清 dry-run 与真实执行的差别，建议先 dry-run"""
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
    cap = 200 if t in ("asset_replace", "field_patch") else 20
    if len(items) > cap:
        return None, f"{t} 单任务 ≤{cap} 项（当前 {len(items)}）"
    allow = {"asset_replace": {"doc_id", "kind", "idx", "field", "old", "new_url", "new_alt"},
             "field_patch": {"doc_id", "set"},
             "gen": {"item_id", "type", "lang", "topic", "brief"},
             "qa": {"kind", "doc_id", "path", "target"},
             "rewrite": {"item_id", "lang", "topic", "instruction", "source_path"}}[t]
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
                      "/api/qa/orchestrate", "/api/qa/recheck"}
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
                r = run_tool([sys.executable, str(PS_PATH),
                              "--state-path", str(self._st()), "--events-path", str(self._ev()),
                              "upsert", "--id", item_id,
                              "--category", str(body.get("category", "blog")),
                              "--target-type", str(body.get("target_type", "blog"))])
                return self._send(200 if r["rc"] == 0 else 400, r)
            if self.path == "/api/item/advance":
                r = run_tool([sys.executable, str(PS_PATH),
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
                t = batch_create(btype, str(body.get("title", "")), items,
                                 params=body.get("params") or {},
                                 dry_run=bool(body.get("dry_run", True)), by=self._me())
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
                t = batch_create(spec["type"], spec["title"], spec["items"],
                                 params={"max_attempts": 2, "from_agent": True, "rationale": spec.get("rationale", ""),
                                         "skills_used": spec.get("skills_used", [])},
                                 dry_run=spec["dry_run"], by=self._me())
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
                    run_tool([sys.executable, str(PS_PATH),
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
                gates = run_content_gates(path, str(body.get("type", "blog")), str(body.get("lang", "zh")), tag="generate")
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
                run_tool([sys.executable, str(PS_PATH),
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
    print(f"[console] MFlow Console on :{PORT} (loop queue + schedule + geo + pay verifier started, max_parallel={MAX_PARALLEL_LOOPS})")
    server.serve_forever()


if __name__ == "__main__":
    main()
