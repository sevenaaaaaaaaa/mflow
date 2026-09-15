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
DEFAULT_PROJECT = "main"
DAILY_LOG = RUN_DIR / "logs" / "daily.out.log"
DAILY_PID = RUN_DIR / "logs" / "daily.pid"
KB_ROOT = PROJECT / "1-2 Insight" / "Knowledge Base"
LLM_FILE = RUN_DIR / "llm.json"
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


def impact_report():
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
    return {"rows": rows, "gsc_date": gsc.get("_date"), "gsc_pages": len(pages),
            "note": "归因范围 = GSC Top20 页面；全量归因需扩展 gsc_fetch 行数上限"}


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

ANTI_SLOP = """硬性写作规则（违反任何一条即为废稿）：
- 每一段必须回答：谁会读 / 为什么现在读 / 读完改变什么 / 下一步是什么
- 禁止以下 AI 套话：In today's fast-paced world、game-changer、cutting-edge、unlock the power、seamlessly integrate、delve into、elevate your workflow、革命性、赋能、闭环（作修饰语时）
- 不可验证的数字一律标注 [待考证]，禁止编造产品数据
- 段落长度由语义完整性决定，不写零碎小段
- 面向真实用户的具体场景，不写空泛综述"""


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
    anti = ANTI_SLOP + (f"\n{extra}" if extra else "")
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
                profile="lovart-creation", max_tokens=4000)
        except Exception as e:
            loop["status"] = "failed"
            log(loop, f"LLM 调用失败：{e}")
            _loop_save(loop, proj)
            return
        with _usage_lock:
            loop["tokens_used"] = loop.get("tokens_used", 0) + LAST_USAGE.get("total_tokens", 0)
        draft_path = gen_dir / f"{item}.md"
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(draft)
        log(loop, f"草稿写入 {draft_path.relative_to(PROJECT)}（{len(draft)} 字符），跑质量门禁…")
        demo_mode = DEMO_FLAG.exists() and not llm_config()["providers"][
            llm_config()["profiles"]["default"]["provider"]].get("key")
        r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks/post-write-check.sh"),
                      "--file", str(draft_path), "--target-words", "15" if demo_mode else "300"], timeout=120)
        qa_log(f"loop:{loop.get('id','')}", "post-write-check.sh", r["rc"])
        loop["last_hook_rc"] = r["rc"]
        if r["rc"] == 0:
            log(loop, "质检 PASS，推进状态机 S3-draft → S3-done → S4-qa")
            for stg in ("S3-draft", "S3-done", "S4-qa"):
                run_tool([sys.executable, str(PS_PATH), *ps_args, "advance", "--id", item, "--to", stg])
            loop["status"] = "done"
            loop["draft_path"] = rel_of(draft_path)
            log(loop, "Loop 完成：草稿已入 S4-qa，等待人工审阅/继续推进")
            _loop_save(loop, proj)
            return
        feedback = r["out"][-1500:]
        log(loop, f"质检 BLOCK（exit {r['rc']}），反馈带入下一轮")
        _loop_save(loop, proj)
    loop["status"] = "blocked"
    log(loop, f"达最大轮次仍 BLOCK。草稿在 {gen_dir / (item + '.md')}, 可人工修改后继续推进")
    _loop_save(loop, proj)


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
            "tasks": d / "tasks.json", "loops": d / "loops.json", "gen": d / "content"}


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


def kb_tree():
    out = []
    for label, desc, pairs in KNOWLEDGE_SOURCES:
        n = 0
        for d, pat in pairs:
            base = PROJECT / d
            if base.exists():
                n += sum(1 for f in base.glob(pat) if f.is_file() and f.suffix == ".md")
        out.append({"name": label, "desc": desc, "files": n})
    return out


def kb_list(src):
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
    return files[:400]


def kb_search(q, src=""):
    sources = [(l, p) for l, _d, p in KNOWLEDGE_SOURCES if not src or l == src]
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
    return {"items": items,
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
        return bool(self._me())

    def _me(self):
        sess = SESSIONS.get(self._sid(), "")
        return sess.get("username", "") if isinstance(sess, dict) else str(sess)

    def _role(self):
        me = self._me()
        for x in read_json(AUTH_FILE, []):
            if x.get("username") == me:
                return x.get("role", "operator")
        return "admin" if (PASSWORD and not AUTH_FILE.exists()) else "viewer"

    def _proj(self):
        sess = SESSIONS.get(self._sid(), {})
        pid = sess.get("project", DEFAULT_PROJECT) if isinstance(sess, dict) else DEFAULT_PROJECT
        pp = proj_paths(pid)
        if not pp["dir"].exists():
            ensure_project(pid)
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
                return self._send(200, overview(self._proj()))
            if parsed.path == "/api/state":
                return self._send(200, api_state(self._proj()))
            if parsed.path == "/api/tasks":
                return self._send(200, tasks_all(self._proj()))
            if parsed.path == "/api/reports":
                return self._send(200, list_reports())
            if parsed.path == "/api/kb/tree":
                return self._send(200, kb_tree())
            if parsed.path == "/api/kb/list":
                return self._send(200, kb_list(qs.get("src", [""])[0]))
            if parsed.path == "/api/kb/search":
                q = qs.get("q", [""])[0].strip()
                if len(q) < 2:
                    return self._send(400, {"error": "至少 2 个字符"})
                return self._send(200, kb_search(q, qs.get("src", [""])[0]))
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
                return self._send(200, {"projects": list_projects(), "current": self._proj()})
            if parsed.path == "/api/version":
                v = VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else "dev"
                return self._send(200, {"version": v, "started": time.strftime("%Y-%m-%d")})
            if parsed.path == "/api/daily/log":
                return self._send(200, daily_status())
            if parsed.path == "/api/usage":
                return self._send(200, usage_stats())
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
            if parsed.path == "/api/impact":
                return self._send(200, impact_report())
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
                                     "name": x.get("name", "")} for x in read_json(AUTH_FILE, [])])
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
                      "/api/trident/run", "/api/daily/run", "/api/tasks/del"}
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
                        profile="lovart-creation")
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
                return self._send(200, {"ok": True, "path": rel_of(path), "chars": len(draft),
                                        "hook_rc": hook["rc"], "hook_out": hook["out"][-2000:]})
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
                env.setdefault("LOVART_PYTHON", "/var/www/mflow/.venv/bin/python")
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
            if self.path == "/api/projects/create":
                name = str(body.get("name", "")).strip()[:60]
                if not name:
                    return self._send(400, {"error": "项目名必填"})
                pid = re.sub(r"[^a-z0-9-]", "", str(body.get("id") or name).lower())[:40] or f"proj-{secrets.token_hex(3)}"
                if (PROJECTS_DIR / pid).exists():
                    return self._send(409, {"error": f"项目 id 已存在：{pid}"})
                ensure_project(pid, name=name)
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
    ensure_project(DEFAULT_PROJECT, "默认项目")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    threading.Thread(target=loop_queue_worker, daemon=True).start()
    print(f"[console] MFlow Console on :{PORT} (loop queue worker started, max_parallel={MAX_PARALLEL_LOOPS})")
    server.serve_forever()


if __name__ == "__main__":
    main()
