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
DAILY_LOG = RUN_DIR / "logs" / "daily.out.log"
DAILY_PID = RUN_DIR / "logs" / "daily.pid"
KB_ROOT = PROJECT / "1-2 Insight" / "Knowledge Base"
LLM_FILE = RUN_DIR / "llm.json"
LOOPS_FILE = RUN_DIR / "loops.json"
GEN_DIR = PROJECT / "1-3 GenFlow" / "Console-Gen"
HARNESS_DIR = PROJECT / "1-1 Harness"
LOOP_LOCK = threading.Lock()
LOOP_THREADS = {}
USAGE_FILE = RUN_DIR / "llm-usage.jsonl"
DEMO_FLAG = RUN_DIR / "demo.json"
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
    ("产品知识库", "Lovart 产品介绍 / 帮助中心 / 文档存档 / 新闻 / Changelog",
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
        demo_mode = DEMO_FLAG.exists() and not llm_config()["providers"][
            llm_config()["profiles"]["default"]["provider"]].get("key")
        r = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks/post-write-check.sh"),
                      "--file", str(draft_path), "--target-words", "15" if demo_mode else "300"], timeout=120)
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
Lovart 团队用同样的方法维护八个语言市场的内容，具体数字因项目而异 [待考证]。

## 下一步

在设置页配置你的大模型 API Key，然后回创作中心用同一主题发起一次正式生成。
对比演示稿与真实稿的差异，你就能判断提示词模板是否需要按你的行业调整。

## FAQ

**演示稿可以发布吗？** 可以走完发布流程，但它不含真实信息量，建议只用它理解流程。

**质量门禁会误杀正常内容吗？** 会偶发。门禁输出会说明触发原因，人工审阅环节可以放行。

**如何换成本公司的品牌语气？** 修改创作中心使用的提示词模板，把品牌词与禁用词表替换即可。
"""


def setup_status():
    llm = llm_config()
    llm_ok = any((p or {}).get("key") for p in llm["providers"].values())
    kb_total = sum(x["files"] for x in kb_tree())
    cal = sum(1 for _ in CALENDAR_ROOT.rglob("*.md")) if CALENDAR_ROOT.exists() else 0
    items = len(read_json(STATE_FILE, {}).get("items", {}))
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


def seed_demo():
    DEMO_FLAG.parent.mkdir(parents=True, exist_ok=True)
    DEMO_FLAG.write_text(json.dumps({"seeded": datetime.now().isoformat(timespec="seconds")}))
    tasks = read_json(TASKS_FILE, [])
    have = {x.get("title") for x in tasks}
    for title, status in [("体验：发起第一个 Blog Loop（创作中心）", "todo"),
                          ("阅读：铁律与规则 → RULES-00（知识中台）", "todo"),
                          ("配置：接入公司自己的大模型 API Key", "doing")]:
        if title not in have:
            tasks.append({"id": secrets.token_hex(4), "title": title, "status": status,
                          "source": "manual", "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                          "note": "demo seed", "assignee": "", "due": "", "link": "", "desc": ""})
    TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
    return {"ok": True, "note": "演示任务已注入；示例报告在 docs/demo-reports/"}


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
                loops = sorted(read_json(LOOPS_FILE, []),
                               key=lambda x: x.get("created", ""), reverse=True)
                return self._send(200, loops)
            if parsed.path == "/api/loop/detail":
                loop = next((x for x in read_json(LOOPS_FILE, []) if x["id"] == qs.get("id", [""])[0]), None)
                return self._send(200, loop or {"error": "not found"})
            if parsed.path == "/api/setup/status":
                return self._send(200, setup_status())
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
                # demo 稿豁免词数门槛（hook 按空格分词，CJK 长文会被低估）
                twords = "15" if DEMO_FLAG.exists() and not llm_config()["providers"][
                    llm_config()["profiles"]["default"]["provider"]].get("key") else "300"
                hook = run_tool(["bash", str(PROJECT / "1-4 Dev/scripts/hooks/post-write-check.sh"),
                                 "--file", str(path), "--target-words", twords], timeout=120)
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
            if self.path == "/api/tasks/add":
                title = str(body.get("title", "")).strip()[:200]
                if not title:
                    return self._send(400, {"error": "标题必填"})
                tasks = read_json(TASKS_FILE, [])
                tasks.append({"id": secrets.token_hex(4), "title": title,
                              "status": body.get("status", "todo"), "source": "manual",
                              "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                              "note": str(body.get("note", ""))[:300],
                              "desc": str(body.get("desc", ""))[:2000],
                              "assignee": str(body.get("assignee", ""))[:60],
                              "due": str(body.get("due", ""))[:10],
                              "link": str(body.get("link", ""))[:300]})
                TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
                TASKS_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=1))
                return self._send(200, {"ok": True})
            if self.path == "/api/tasks/update":
                tasks = read_json(TASKS_FILE, [])
                for t in tasks:
                    if t["id"] == body.get("id"):
                        for k in ("title", "desc", "assignee", "due", "link", "status"):
                            if k in body:
                                t[k] = str(body[k])[:2000]
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
