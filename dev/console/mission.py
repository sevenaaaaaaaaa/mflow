"""任务全景（Mission Control）—— 新人 30 秒看懂系统在干什么。

痛点（2026-10-12 用户原话）：一个人进到系统里，无法很快上手——看不懂正在执行的任务、
对应的过程进程，也没有最终产出物的预览和 URL 汇总；不知道为什么这么做、会执行多久、
收益是什么、QA 反馈如何、流量反馈如何。

根因：同一件事被拆在 Run 画布 / 批量任务 / Loop / QA / 分发 / 报告 多个页面，
每页只讲自己那一段。本模块把三种执行入口（Run、批量、Loop）统一成一种「工作卡」，
每张卡回答同样 7 个问题：为什么 · 在做什么 · 过程 · 多久 · 产出 · QA · 流量。

设计约束：
- 只读、零副作用、零网络（不调 Sanity / LLM），整页一次请求 < 300ms 量级
- 不往 console.py 堆代码：console 只做路由，把自己的 globals 交给 build(G, proj)
- 流量数据只用本地已落盘的 GSC 快照，覆盖不到的页面显示「暂无数据」而不是 0
"""
import csv
import io
import json
import os
import re
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

# ───────────────────────── 类型字典：机器类型 → 人话 ─────────────────────────
# what=在做什么；why=默认动机（拿不到具体触发原因时兜底）；benefit=预期收益；
# per_item_sec=没有历史样本时的单条耗时估计（秒）
TYPE_INFO = {
    "field_patch": {"label": "字段修补", "what": "批量补/改 SEO 字段（seoTitle、description 等），不动正文",
                    "why": "搜索结果里标题/摘要缺失或被截断，会直接拉低点击率",
                    "benefit": "搜索结果展示完整 → 提升 CTR；字段级改动、可回滚", "per_item_sec": 6},
    "asset_replace": {"label": "图片物料替换", "what": "把占位图/坏图/缺 alt 的图片换成正式物料",
                      "why": "占位图和缺 alt 会伤页面质量分与图片搜索",
                      "benefit": "页面质量与图片搜索收录提升；视觉一致", "per_item_sec": 5},
    "gen": {"label": "新写内容", "what": "按选题调用 LLM 生成新稿，过四道质量门禁",
            "why": "有搜索需求但站内没有对应页面（内容缺口）",
            "benefit": "覆盖新关键词 → 新增自然流量与 AI 引用机会", "per_item_sec": 90},
    "rewrite": {"label": "改写已有内容", "what": "读取线上旧稿，按新规范重写并过门禁",
                "why": "老页面排名/流量衰减，或质量不达标",
                "benefit": "挽回衰减流量，提升排名与可引用性", "per_item_sec": 90},
    "landing_refresh": {"label": "落地页改稿", "what": "按落地页结构（H1 / 卖点 / FAQ / CTA）重写并做结构校验",
                        "why": "落地页文案结构不完整或转化弱",
                        "benefit": "落地页排名与转化提升", "per_item_sec": 120},
    "publish_sanity": {"label": "发布上线", "what": "把已过门禁的稿件写入 CMS，前台可访问",
                       "why": "稿件已通过质检，需要上线才开始产生流量",
                       "benefit": "页面上线，开始获取搜索流量（通常 3–14 天出数据）", "per_item_sec": 8},
    "internal_link": {"label": "内链建议", "what": "为页面生成站内相关页面链接建议",
                      "why": "孤立页面收录慢、权重传不过去",
                      "benefit": "提升收录速度与权重传递", "per_item_sec": 4},
    "qa": {"label": "质量扫描", "what": "扫描线上/草稿内容，产出问题清单（findings）",
           "why": "先量化问题再决定修什么",
           "benefit": "发现问题并可一键生成修复任务", "per_item_sec": 3},
    "loop": {"label": "Loop 自动创作", "what": "生成 → 质检 → 带反馈重写，直到通过或达到轮数上限",
             "why": "选题已定，交给系统自治完成草稿",
             "benefit": "产出可审阅草稿，进入发布前审核", "per_item_sec": 60},
    "run": {"label": "多步执行", "what": "多个步骤串联的执行（Agent 规划或自动化剧本）",
            "why": "一个目标需要多步完成", "benefit": "见各步骤", "per_item_sec": 30},
}

STATUS_TEXT = {
    "running": "执行中", "queued": "排队中", "done": "已完成", "failed": "失败待处理",
    "waiting": "预演完成·待授权", "paused": "已暂停", "cancelled": "已取消", "tripped": "熔断停止",
    "blocked": "被门禁拦截",
}

CREATED_BY_TEXT = {
    "qa-recheck": "QA 修复后自动复检", "selfheal": "系统自愈", "warmup": "开工预热脚本",
    "scheduler": "定时调度", "chain": "上一个任务完成后自动链出", "": "未记录发起人",
}

_TRAFFIC_CACHE = {"key": None, "data": None}


# ───────────────────────── 小工具 ─────────────────────────
def _parse_ts(s):
    if not s:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s[:19], fmt).timestamp()
        except Exception:
            continue
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def _fmt_dur(sec):
    if sec is None:
        return "—"
    sec = int(max(0, sec))
    if sec < 60:
        return f"{sec} 秒"
    if sec < 3600:
        return f"{sec // 60} 分钟"
    if sec < 86400:
        h, m = divmod(sec // 60, 60)
        return f"{h} 小时" + (f" {m} 分" if m else "")
    return f"{sec // 86400} 天"


def _path_key(url):
    """URL → 匹配键（去协议/去 www/去尾斜杠/小写）。"""
    if not url:
        return ""
    try:
        u = urllib.parse.urlparse(url if "://" in url else "https://x" + url)
        host = (u.netloc or "").lower().replace("www.", "")
        path = (u.path or "/").rstrip("/") or "/"
        return host + path.lower()
    except Exception:
        return ""


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text(errors="ignore"))
    except Exception:
        return default


# ───────────────────────── 流量：本地 GSC 快照索引 ─────────────────────────
def traffic_index(project_dir, run_dir):
    """合并本地所有 GSC 页面级快照为 {path_key: metrics}。按文件 mtime 缓存。

    数据源（按新鲜度覆盖）：gsc-5k-YYYY-MM.json（1000 页/月）、gsc-full.json（Top20）。
    """
    project_dir, run_dir = Path(project_dir), Path(run_dir)
    cands = []
    for d in (run_dir / "local-dev/Output/Data Ingestion", project_dir / "dev/Output/Data Ingestion",
              project_dir / "insight-data/Trident Insights/reports"):
        if d.exists():
            cands += [p for p in d.glob("gsc-5k-*.json")] + [p for p in d.glob("gsc-full.json")]
    cands = [p for p in cands if p.is_file()]
    key = tuple(sorted((str(p), p.stat().st_mtime) for p in cands))
    if _TRAFFIC_CACHE["key"] == key and _TRAFFIC_CACHE["data"] is not None:
        return _TRAFFIC_CACHE["data"]
    idx, sources = {}, []

    def label_of(p, d):
        m = re.search(r"(\d{4}-\d{2})", p.name)
        return (d.get("_date") if isinstance(d, dict) else None) or (m.group(1) if m else
                datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d"))

    for p in sorted(cands, key=lambda x: x.stat().st_mtime):  # 旧 → 新，新的覆盖旧的
        d = _read_json(p, {})
        if not isinstance(d, dict):
            continue
        pages = d.get("pages")
        if isinstance(pages, dict):
            pages = pages.get("top20_pages") or []
        if not isinstance(pages, list):
            continue
        lab = label_of(p, d)
        n = 0
        for pg in pages:
            k = _path_key((pg or {}).get("url", ""))
            if not k:
                continue
            idx[k] = {"clicks": pg.get("clicks"), "impr": pg.get("impr", pg.get("impressions")),
                      "ctr": pg.get("ctr"), "pos": pg.get("pos", pg.get("position")), "period": lab}
            n += 1
        sources.append({"file": p.name, "period": lab, "pages": n})
    data = {"idx": idx, "sources": sources[-6:], "pages": len(idx),
            "latest": sources[-1]["period"] if sources else None}
    _TRAFFIC_CACHE.update(key=key, data=data)
    return data


def _traffic_for(url, tidx):
    m = tidx["idx"].get(_path_key(url)) if url else None
    return dict(m) if m else None


# ───────────────────────── 耗时：同类历史基线 ─────────────────────────
def duration_baseline(batches):
    """按类型统计已完成批量任务的单条耗时中位数（秒/条）。"""
    by = {}
    for t in batches:
        if t.get("status") != "done":
            continue
        a, b = _parse_ts(t.get("started") or t.get("created")), _parse_ts(t.get("finished"))
        n = int((t.get("stats") or {}).get("total") or 0)
        if a and b and b > a and n:
            by.setdefault(t.get("type"), []).append((b - a) / n)
    out = {}
    for k, arr in by.items():
        arr.sort()
        out[k] = {"per_item_sec": round(arr[len(arr) // 2], 1), "samples": len(arr)}
    return out


# ───────────────────────── 单条目 → 产出 / QA ─────────────────────────
def _item_gates(r):
    g = {}
    for k, label in (("hook_rc", "写后质检"), ("geo_rc", "GEO 可引用性"), ("quota_rc", "配额"), ("lang_rc", "语言")):
        if k in r and r.get(k) is not None:
            g[label] = "pass" if r.get(k) == 0 else "fail"
    if "ready_to_publish" in r:
        g["落地页结构"] = "pass" if r.get("ready_to_publish") else "fail"
    if r.get("block"):
        g["QA 阻断"] = "fail"
    if r.get("warn"):
        g["QA 告警"] = "warn"
    return g


def _outputs_of_batch(t, G, site, tidx):
    outs = []
    for it in (t.get("items") or []):
        r = it.get("result") or {}
        st = it.get("status")
        title = (it.get("title") or r.get("title") or it.get("slug") or r.get("slug")
                 or it.get("doc_id") or f"条目 {int(it.get('i', 0)) + 1}")
        url = r.get("url") or ""
        if not url:
            slug = it.get("slug") or r.get("slug")
            if slug:
                try:
                    url = G["_site_url"](site, it.get("page_type") or r.get("page_type"),
                                         it.get("lang") or r.get("lang"), slug)
                except Exception:
                    url = ""
        draft = r.get("path") or ""
        if not url and not draft:
            continue
        gates = _item_gates(r)
        qa = "fail" if "fail" in gates.values() else ("warn" if "warn" in gates.values() else ("pass" if gates else ""))
        if st == "failed":
            qa = "fail"
        live = bool(url) and not t.get("dry_run") and st == "done" and t.get("type") in ("publish_sanity", "field_patch",
                                                                                        "asset_replace")
        outs.append({"title": str(title)[:120], "url": url, "draft": draft, "status": st,
                     "state": ("已上线/已写库" if live else ("预演（未写库）" if t.get("dry_run") else
                               ("草稿" if draft and not url else ("失败" if st == "failed" else "前台页面")))),
                     "qa": qa, "gates": gates, "error": str(it.get("error") or "")[:160],
                     "traffic": _traffic_for(url, tidx), "task_id": t.get("id"), "task_title": t.get("title")})
    return outs


def _qa_summary(outs, failed_items, blocked_reasons):
    n = len(outs)
    p = sum(1 for o in outs if o["qa"] == "pass")
    w = sum(1 for o in outs if o["qa"] == "warn")
    f = sum(1 for o in outs if o["qa"] == "fail")
    checked = p + w + f
    if not checked and not failed_items:
        line = "本任务不经过质量门禁，或尚未产出"
    else:
        line = f"门禁通过 {p} · 告警 {w} · 未过 {f}" + (f"（共 {n} 个产出）" if n else "")
        if failed_items:
            line += f"；另有 {failed_items} 条执行失败"
    return {"pass": p, "warn": w, "fail": f, "checked": checked, "line": line,
            "top_issues": blocked_reasons[:4]}


def _traffic_summary(outs, dry_run, tidx):
    urls = [o for o in outs if o.get("url")]
    matched = [o for o in urls if o.get("traffic")]
    clicks = sum(int(o["traffic"].get("clicks") or 0) for o in matched)
    impr = sum(int(o["traffic"].get("impr") or 0) for o in matched)
    if dry_run:
        line = "预演任务，未上线，暂不产生流量"
    elif not urls:
        line = "无前台页面产出（草稿/扫描类任务）"
    elif not matched:
        line = f"{len(urls)} 个页面暂未进入 GSC 快照（新页通常 3–14 天出数据；快照 {tidx.get('latest') or '无'}）"
    else:
        line = f"{len(matched)}/{len(urls)} 个页面有 GSC 数据：点击 {clicks:,} · 展示 {impr:,}"
    return {"urls": len(urls), "matched": len(matched), "clicks": clicks, "impr": impr, "line": line,
            "period": tidx.get("latest")}


def _why_of_batch(t, G):
    title = t.get("title") or ""
    by = t.get("created_by") or ""
    params = t.get("params") or {}
    trig = []
    if params.get("from_qa"):
        trig.append(f"QA 扫描 {params['from_qa']} 发现问题后自动生成")
    m = re.search(r"源\s*(batch-[\w-]+)", title)
    if m and not params.get("from_qa"):
        trig.append(f"由任务 {m.group(1)} 的结果派生")
    if by.startswith("playbook"):
        trig.append("自动化剧本触发：" + by.split(":", 1)[-1])
    elif by in CREATED_BY_TEXT and by:
        trig.append(CREATED_BY_TEXT[by])
    elif by:
        trig.append(f"{by} 手动发起")
    reason = params.get("reason") or params.get("goal") or params.get("why") or ""
    info = TYPE_INFO.get(t.get("type"), {})
    return {"trigger": "；".join(trig) or "未记录触发来源", "reason": reason or info.get("why", ""),
            "parent": (m.group(1) if m else params.get("from_qa") or "")}


# ───────────────────────── 三种入口 → 统一工作卡 ─────────────────────────
def _norm_status(raw, dry_run=False):
    if raw in ("done",) and dry_run:
        return "waiting"
    if raw in ("warn",):
        return "done"
    if raw in ("replanned", "skipped"):
        return "done"
    return raw if raw in STATUS_TEXT else (raw or "queued")


def card_from_batch(t, G, site, tidx, base, now=None):
    now = now or time.time()
    info = TYPE_INFO.get(t.get("type"), {"label": t.get("type"), "what": "", "benefit": "", "per_item_sec": 30})
    stats = t.get("stats") or {}
    total = int(stats.get("total") or 0)
    done_n = int(stats.get("done") or 0) + int(stats.get("skipped") or 0)
    fail_n = int(stats.get("failed") or 0)
    status = _norm_status(t.get("status"), bool(t.get("dry_run")))
    t0 = _parse_ts(t.get("started")) or _parse_ts(t.get("created"))
    t1 = _parse_ts(t.get("finished"))
    hb = float(t.get("heartbeat_ts") or 0)
    if status in ("running", "queued"):
        elapsed = (now - t0) if t0 else None
    else:
        elapsed = ((t1 or hb or 0) - t0) if t0 and (t1 or hb) else None
    per = (base.get(t.get("type")) or {}).get("per_item_sec") or info.get("per_item_sec", 30)
    remain = max(0, total - done_n - fail_n)
    eta = None
    if status in ("running", "queued") and remain:
        rate = (done_n + fail_n) / elapsed if elapsed and (done_n + fail_n) else 0
        eta = int(remain / rate) if rate > 0 else int(remain * per / max(1, int(t.get("concurrency") or 1)))
    outs = _outputs_of_batch(t, G, site, tidx)
    blocked = []
    try:
        fd = G["failure_digest"](t) or {}
        for c in (fd.get("categories") or [])[:4]:
            blocked.append(f"{c.get('label')}（{c.get('count')} 条）→ {c.get('hint', '')}")
    except Exception:
        for it in (t.get("items") or []):
            if it.get("status") == "failed" and it.get("error"):
                blocked.append(str(it["error"])[:80])
    log = [str(x) for x in (t.get("log") or [])[-8:]]
    return {
        "id": t.get("id"), "kind": "batch", "kind_text": "批量任务", "type": t.get("type"),
        "type_text": info.get("label"), "title": t.get("title") or info.get("label"),
        "status": status, "status_text": STATUS_TEXT.get(status, status), "dry_run": bool(t.get("dry_run")),
        "created": t.get("created"), "updated_ts": hb or t1 or t0,
        "why": _why_of_batch(t, G),
        "what": info.get("what", ""),
        "progress": {"done": done_n, "failed": fail_n, "total": total,
                     "pct": int(round(100 * (done_n + fail_n) / max(1, total))) if total else (100 if status == "done" else 0)},
        "steps": [], "log": log,
        "timing": {"elapsed_sec": int(elapsed) if elapsed else None, "eta_sec": eta,
                   "elapsed_text": _fmt_dur(elapsed) if elapsed else "—",
                   "eta_text": (_fmt_dur(eta) if eta else ("即将完成" if status == "running" else "—")),
                   "typical_text": f"同类约 {_fmt_dur(per * max(1, total) / max(1, int(t.get('concurrency') or 1)))}"
                                   + (f"（{base[t.get('type')]['samples']} 次历史）" if t.get("type") in base else "（经验值）")},
        "benefit": {"expected": info.get("benefit", ""),
                    "note": "预演只校验不写库——确认结果后到「批量任务」关掉 dry-run 再跑一遍才会生效" if t.get("dry_run") else ""},
        "outputs": outs[:60], "outputs_total": len(outs),
        "qa": _qa_summary(outs, fail_n, blocked),
        "traffic": _traffic_summary(outs, bool(t.get("dry_run")), tidx),
        "drill": {"tab": "batch", "id": t.get("id"), "text": "批量任务详情"},
    }


def card_from_run(r, G, site, tidx, base, batches_by_id, now=None):
    now = now or time.time()
    steps = r.get("steps") or []
    child = [batches_by_id[s["task_id"]] for s in steps if s.get("task_id") in batches_by_id]
    st_done = sum(1 for s in steps if s.get("status") in ("done", "warn", "skipped", "replanned"))
    st_fail = sum(1 for s in steps if s.get("status") in ("failed", "blocked"))
    status = _norm_status(r.get("status"))
    if status == "done" and child and all(c.get("dry_run") for c in child):
        status = "waiting"
    t0 = float(r.get("started_ts") or 0) or _parse_ts(r.get("created"))
    t_end = _parse_ts(r.get("ended") or r.get("finished"))
    if not t_end and status not in ("running", "queued"):
        ends = [_parse_ts(c.get("finished")) for c in child if c.get("finished")]
        t_end = max([e for e in ends if e] or [0]) or None
    elapsed = ((now if status in ("running", "queued") else (t_end or 0)) - t0) if t0 and (
        status in ("running", "queued") or t_end) else None
    items_total = sum(int((c.get("stats") or {}).get("total") or 0) for c in child)
    items_done = sum(int((c.get("stats") or {}).get("done") or 0) + int((c.get("stats") or {}).get("skipped") or 0)
                     + int((c.get("stats") or {}).get("failed") or 0) for c in child)
    eta = None
    if status == "running":
        if items_total and items_done and elapsed:
            eta = int((items_total - items_done) / (items_done / elapsed)) if items_total > items_done else 0
        else:
            rest = len(steps) - st_done - st_fail
            eta = rest * 60 if rest > 0 else None
    outs, blocked = [], []
    for c in child:
        outs += _outputs_of_batch(c, G, site, tidx)
        for it in (c.get("items") or []):
            if it.get("status") == "failed" and it.get("error"):
                blocked.append(str(it["error"])[:80])
    for s in steps:
        if s.get("status") in ("failed", "blocked") and s.get("detail"):
            blocked.insert(0, f"{s.get('name')}：{str(s.get('detail'))[:80]}")
    for u in (s.get("urls") or [] for s in steps):
        for x in u:
            if isinstance(x, str) and x.startswith("http") and not any(o["url"] == x for o in outs):
                outs.append({"title": x, "url": x, "draft": "", "status": "done", "state": "验证页面", "qa": "",
                             "gates": {}, "error": "", "traffic": _traffic_for(x, tidx),
                             "task_id": r.get("id"), "task_title": r.get("title")})
    pb = r.get("playbook") or ""
    pb_desc = ""
    if pb:
        try:
            for x in (G["playbooks_list"]() or []):
                if x.get("id") == pb or x.get("name") == pb:
                    pb_desc = x.get("desc") or ""
                    pb = x.get("name") or pb
                    break
        except Exception:
            pass
    trig = ("自动化剧本「%s」" % pb) if pb else ({"agent": "Agent 任务台对话下达", "playbook": "自动化剧本"}.get(
        r.get("kind"), r.get("kind") or "手动")) + (f"（{r['by']}）" if r.get("by") else "")
    types = [c.get("type") for c in child]
    benefit = "；".join(dict.fromkeys(TYPE_INFO.get(x, {}).get("benefit", "") for x in types if x)) or TYPE_INFO["run"]["benefit"]
    whats = " → ".join(dict.fromkeys(TYPE_INFO.get(x, {}).get("label", x) for x in types if x))
    dry = bool(child) and all(c.get("dry_run") for c in child)
    return {
        "id": r.get("id"), "kind": "run", "kind_text": "多步执行", "type": "run",
        "type_text": whats or "多步执行", "title": r.get("title") or "未命名执行",
        "status": status, "status_text": STATUS_TEXT.get(status, status), "dry_run": dry,
        "created": r.get("created"), "updated_ts": t_end or t0,
        "why": {"trigger": trig, "reason": r.get("message") or pb_desc or r.get("replan_reason") or "", "parent": ""},
        "what": (f"{len(steps)} 个步骤：" + " → ".join(str(s.get("name")) for s in steps[:6])
                 + (" …" if len(steps) > 6 else "")),
        "progress": {"done": st_done, "failed": st_fail, "total": len(steps),
                     "pct": int(round(100 * (st_done + st_fail) / max(1, len(steps)))),
                     "items_done": items_done, "items_total": items_total},
        "steps": [{"name": s.get("name"), "status": s.get("status"), "detail": str(s.get("detail") or "")[:160],
                   "type": s.get("type"), "progress": s.get("progress"), "task_id": s.get("task_id") or "",
                   "started": s.get("started") or "", "ended": s.get("ended") or ""} for s in steps],
        "log": [],
        "timing": {"elapsed_sec": int(elapsed) if elapsed else None, "eta_sec": eta,
                   "elapsed_text": _fmt_dur(elapsed) if elapsed else "—",
                   "eta_text": _fmt_dur(eta) if eta else ("—" if status != "running" else "估算中"),
                   "typical_text": f"含 {items_total} 个条目" if items_total else f"{len(steps)} 步"},
        "benefit": {"expected": benefit,
                    "note": "整条执行都是预演（dry-run），尚未写库" if dry else ""},
        "outputs": outs[:60], "outputs_total": len(outs),
        "qa": _qa_summary(outs, st_fail, blocked),
        "traffic": _traffic_summary(outs, dry, tidx),
        "drill": {"tab": "run", "id": r.get("id"), "text": "执行画布"},
        "children": [c.get("id") for c in child],
    }


def card_from_loop(lp, proj, tidx, now=None):
    now = now or time.time()
    status = {"done": "done", "running": "running", "failed": "failed", "stopped": "cancelled",
              "tripped": "tripped", "queued": "queued"}.get(lp.get("status"), lp.get("status") or "queued")
    gates = {}
    for k, label in (("last_hook_rc", "写后质检"), ("last_geo_rc", "GEO 可引用性"),
                     ("last_quota_rc", "配额"), ("last_lang_rc", "语言")):
        if lp.get(k) is not None:
            gates[label] = "pass" if lp.get(k) == 0 else "fail"
    qa = "fail" if "fail" in gates.values() else ("pass" if gates else "")
    outs = []
    if lp.get("draft_path"):
        outs.append({"title": lp.get("topic") or lp.get("goal") or lp.get("item_id"), "url": "",
                     "draft": lp["draft_path"], "status": lp.get("status"), "state": "草稿（待人工审阅）",
                     "qa": qa, "gates": gates, "error": "", "traffic": None,
                     "task_id": lp.get("id"), "task_title": lp.get("goal")})
    t0 = _parse_ts(lp.get("created"))
    log = [str(x) for x in (lp.get("log") or [])]
    t_last = None
    if log:
        m = re.match(r"\[(\d{2}:\d{2}:\d{2})\]", log[-1])
        if m and lp.get("created"):
            t_last = _parse_ts(str(lp["created"])[:10] + " " + m.group(1))
    elapsed = ((now if status == "running" else (t_last or 0)) - t0) if t0 and (status == "running" or t_last) else None
    rnd, mx = int(lp.get("round") or 0), int(lp.get("max_rounds") or 3)
    eta = (mx - rnd) * TYPE_INFO["loop"]["per_item_sec"] if status == "running" else None
    return {
        "id": "loop-" + str(lp.get("id")), "kind": "loop", "kind_text": "Loop 创作", "type": "loop",
        "type_text": f"{lp.get('type') or '内容'} · {lp.get('lang') or ''}", "title": lp.get("goal") or lp.get("topic") or "Loop",
        "status": status, "status_text": STATUS_TEXT.get(status, status), "dry_run": False,
        "created": lp.get("created"), "updated_ts": t_last or t0, "proj": proj,
        "why": {"trigger": "Loop 自治模式" + (f"（模板 {lp['template_id']}）" if lp.get("template_id") else ""),
                "reason": lp.get("brief") or TYPE_INFO["loop"]["why"], "parent": ""},
        "what": TYPE_INFO["loop"]["what"],
        "progress": {"done": rnd, "failed": 0, "total": mx,
                     "pct": 100 if status in ("done", "failed") else int(100 * rnd / max(1, mx))},
        "steps": [], "log": log[-8:],
        "timing": {"elapsed_sec": int(elapsed) if elapsed else None, "eta_sec": eta,
                   "elapsed_text": _fmt_dur(elapsed) if elapsed else "—",
                   "eta_text": _fmt_dur(eta) if eta else "—",
                   "typical_text": f"第 {rnd}/{mx} 轮 · 消耗 {int(lp.get('tokens_used') or 0):,} token"},
        "benefit": {"expected": TYPE_INFO["loop"]["benefit"],
                    "note": "草稿在 S4 质检阶段，需要人工审阅后才进入发布" if status == "done" else ""},
        "outputs": outs, "outputs_total": len(outs),
        "qa": _qa_summary(outs, 1 if status == "failed" else 0, [log[-1]] if status == "failed" and log else []),
        "traffic": _traffic_summary(outs, False, tidx),
        "drill": {"tab": "loops", "id": lp.get("id"), "text": "Loop 详情"},
    }


# ───────────────────────── 链路 6 环 ─────────────────────────
def _chain(G, proj, cards, tidx):
    def safe(fn, d=None):
        try:
            return fn()
        except Exception:
            return d
    run_dir = Path(G["RUN_DIR"])
    pp = safe(lambda: G["proj_paths"](proj), {}) or {}
    topics = safe(lambda: _read_json(pp.get("topics"), []), []) or []
    pbs = safe(lambda: [x for x in (G["playbooks_list"]() or []) if x.get("enabled")], []) or []
    qa = safe(lambda: G["qa_stats"](14), {}) or {}
    active = [c for c in cards if c["status"] in ("running", "queued")]
    outs = [o for c in cards for o in c["outputs"]]
    live = [o for o in outs if o["state"] == "已上线/已写库"]
    pub_log = 0
    ap = run_dir / "approvals.log"
    if ap.exists():
        try:
            pub_log = sum(1 for l in ap.read_text(errors="ignore").splitlines()[-3000:]
                          if "PUBLISH" in l and "dry_run=True" not in l)
        except Exception:
            pass
    return [
        {"k": "intel", "name": "情报采集", "desc": "GSC / GA4 / Bing / 22 源舆情，知道用户在搜什么",
         "stat": f"GSC 快照 {tidx.get('latest') or '无'} · {tidx.get('pages', 0)} 页", "tab": "trident"},
        {"k": "decide", "name": "分析决策", "desc": "从数据里挑选题、找内容缺口、决定改哪批页面",
         "stat": f"选题 {len(topics)} · 启用剧本 {len(pbs)}", "tab": "auto"},
        {"k": "make", "name": "内容生产", "desc": "新写 / 改写 / 落地页 / 字段修补，10 语言",
         "stat": f"进行中 {len(active)}", "tab": "batch"},
        {"k": "gate", "name": "质量门禁", "desc": "四道门禁 + Anti-Slop，不过就不许发布",
         "stat": f"近 14 天拦截率 {qa.get('block_rate_all', 0)}% · {qa.get('total_runs', 0)} 次", "tab": "qa"},
        {"k": "publish", "name": "发布上线", "desc": "人工授权后才真写 CMS（Sanity / WordPress）",
         "stat": f"已写库产出 {len(live)} · 发布记录 {pub_log}", "tab": "dist"},
        {"k": "measure", "name": "效果回测", "desc": "GSC 点击/展示回流到每个页面，决定下一轮",
         "stat": f"有流量数据的产出 {sum(1 for o in outs if o.get('traffic'))}", "tab": "rdash"},
    ]


# ───────────────────────── 入口 ─────────────────────────
def build(G, proj=None, limit=60):
    """G = console.py 的 globals()。返回整页所需全部数据。"""
    now = time.time()
    proj = proj or G.get("DEFAULT_PROJECT", "main")
    run_dir, project_dir = Path(G["RUN_DIR"]), Path(G["PROJECT"])
    tidx = traffic_index(project_dir, run_dir)
    try:
        site = G["site_of"](proj)
    except Exception:
        site = proj
    batch_dir = Path(G["BATCH_DIR"])
    batches = []
    if batch_dir.exists():
        for f in sorted(batch_dir.glob("batch-*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:150]:
            t = _read_json(f, None)
            if isinstance(t, dict) and t.get("id"):
                batches.append(t)
    by_id = {t["id"]: t for t in batches}
    base = duration_baseline(batches)

    cards, used = [], set()
    runs_dir = Path(G["RUNS_DIR"])
    if runs_dir.exists():
        for f in sorted(runs_dir.glob("run-*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:40]:
            r = _read_json(f, None)
            if not isinstance(r, dict):
                continue
            try:
                c = card_from_run(r, G, site, tidx, base, by_id, now)
            except Exception:  # 单条坏数据不拖垮整页
                continue
            used.update(c.get("children") or [])
            cards.append(c)
    for t in batches:
        if t["id"] in used:
            continue
        try:
            cards.append(card_from_batch(t, G, site, tidx, base, now))
        except Exception:
            continue
    projects_dir = Path(G["PROJECTS_DIR"])
    if projects_dir.exists():
        for lf in projects_dir.glob("*/loops.json"):
            if lf.parent.name.startswith("_"):
                continue
            arr = _read_json(lf, [])
            for lp in (arr if isinstance(arr, list) else [])[-30:]:
                try:
                    cards.append(card_from_loop(lp, lf.parent.name, tidx, now))
                except Exception:
                    continue

    order = {"running": 0, "queued": 1, "failed": 2, "blocked": 2, "tripped": 2, "waiting": 3, "paused": 4}
    cards.sort(key=lambda c: (order.get(c.get("status"), 5), -(c.get("updated_ts") or _parse_ts(c.get("created")) or 0)))
    cards = cards[:limit]

    outputs = []
    for c in cards:
        for o in c.get("outputs") or []:
            outputs.append(o)
    seen, flat = set(), []
    for o in outputs:
        k = o.get("url") or o.get("draft")
        if k in seen:
            continue
        seen.add(k)
        flat.append(o)

    day0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    try:
        alive, idle = G["worker_alive"]()
    except Exception:
        alive, idle = False, None
    try:
        brk, bst = G["breaker_check"]()
    except Exception:
        brk, bst = False, {}
    kpi = {
        "running": sum(1 for c in cards if c["status"] == "running"),
        "queued": sum(1 for c in cards if c["status"] == "queued"),
        "failed": sum(1 for c in cards if c["status"] in ("failed", "blocked", "tripped")),
        "waiting": sum(1 for c in cards if c["status"] == "waiting"),
        "done_today": sum(1 for c in cards if c["status"] in ("done", "waiting") and (c.get("updated_ts") or 0) >= day0),
        "outputs": len(flat), "urls": sum(1 for o in flat if o.get("url")),
        "live": sum(1 for o in flat if o["state"] == "已上线/已写库"),
        "qa_pass": sum(1 for o in flat if o["qa"] == "pass"), "qa_checked": sum(1 for o in flat if o["qa"]),
        "with_traffic": sum(1 for o in flat if o.get("traffic")),
        "clicks": sum(int((o.get("traffic") or {}).get("clicks") or 0) for o in flat),
    }
    return {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "proj": proj, "site": site,
        "worker": {"alive": bool(alive), "idle_sec": idle,
                   "text": "执行器在线" if alive else (
                       "后台执行器未运行——排队中的任务不会推进（到「调度与日志」检查服务）"
                       if not idle or idle > 86400 else
                       f"后台执行器 {_fmt_dur(idle)}没有心跳——任务可能卡住（到「调度与日志」检查服务）")},
        "breaker": {"on": bool(brk), "reason": (bst or {}).get("reason", "") if isinstance(bst, dict) else ""},
        "kpi": kpi, "chain": _chain(G, proj, cards, tidx), "cards": cards, "outputs": flat[:500],
        "traffic_sources": tidx.get("sources"),
        "notes": [
            "流量来自本地 GSC 页面快照（最新 %s，覆盖 %d 页）；不在快照里的页面显示「暂无」，不代表 0 流量。"
            % (tidx.get("latest") or "无", tidx.get("pages", 0)),
            "「预演完成·待授权」= dry-run 跑通，没写生产库；要生效需人工关掉 dry-run 再跑一次（发布人工授权不可协商）。",
            "预计剩余时间 = 按当前速度外推；还没开始的任务用同类历史中位数估算。",
        ],
    }


def outputs_csv(data):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["标题", "URL", "草稿", "状态", "QA", "点击", "展示", "CTR", "排名", "流量期间", "来源任务", "任务ID"])
    for o in data.get("outputs") or []:
        tr = o.get("traffic") or {}
        w.writerow([o.get("title"), o.get("url"), o.get("draft"), o.get("state"), o.get("qa"),
                    tr.get("clicks", ""), tr.get("impr", ""), tr.get("ctr", ""), tr.get("pos", ""), tr.get("period", ""),
                    o.get("task_title"), o.get("task_id")])
    return "﻿" + buf.getvalue()
