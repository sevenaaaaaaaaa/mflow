#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix-main-content.py — 主站内容机械修复与重写队列生成（dry-run 默认，发布停 ready）。

输入：audit-main-content.py 产出的 JSON（默认取最新 main-audit-*.json）。
配置：dev/automation/quality-cadence.json → mainContentFix.autoFix / queueRewrite。

产出（全部落盘，默认不写 Sanity）：
  1) fix-plan.md            —— 修复计划（按 issue 类别计数 + 每页动作）
  2) safe-fixes.ndjson      —— 可安全机械修复的 Sanity patch（seo-fill-from-title /
                               cover-og-fallback），等人审授权后由 lovart-sanity-publish 导入
  3) rewrite-queue.ndjson   —— 需 signal-writer lane 重写的队列（thin/slop/untranslated/
                               lang-garbage/seq-template），带 lane 分级
用法：
  python3 fix-main-content.py --audit /tmp/main-audit-weekly-2026-10-09.json
  python3 fix-main-content.py --audit ... --write-patch   # 生成 NDJSON patch（仍不落库）
禁止：本脚本绝不直接 mutate production；导入必须走 lovart-sanity-publish 人审流程。
"""
from __future__ import annotations
import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT = "o11tm2qe"
DATASET = "production"
API = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/query/{DATASET}"
CADENCE = Path(__file__).resolve().parents[1] / "automation" / "quality-cadence.json"


def sanity_token():
    """token 取数：env SANITY_TOKEN → run/secrets/sanity.json（服务器）→ /tmp/sanitytoken.txt（开发机）。"""
    tok = os.environ.get("SANITY_TOKEN", "").strip()
    if tok:
        return tok
    sec = Path(__file__).resolve().parents[2] / "run" / "secrets" / "sanity.json"
    if sec.exists():
        try:
            return json.loads(sec.read_text()).get("token", "").strip()
        except Exception:
            pass
    return Path("/tmp/sanitytoken.txt").read_text().strip()


def q_one(query, token, tries=3):
    u = API + "?query=" + urllib.parse.quote(query)
    last = None
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(
                u, headers={"Authorization": f"Bearer {token}"}), timeout=120)
            return json.loads(r.read().decode()).get("result")
        except Exception as e:
            last = e
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"GROQ failed: {last}")


def latest_audit(explicit=None):
    if explicit:
        return Path(explicit)
    cands = sorted(glob.glob("/tmp/main-audit-*.json") + glob.glob("/tmp/main-audit.json"),
                   key=lambda p: Path(p).stat().st_mtime, reverse=True)
    if not cands:
        raise SystemExit("找不到审计 JSON，请先跑 audit-main-content.py 或 --audit 指定")
    return Path(cands[0])


BOILERPLATE = re.compile(
    r"Template-based tools like (Canva|Adobe)|Start (free|creating)|no design skill required|"
    r"In today's (fast-paced|digital)|landscape, (creators|businesses)|"
    r"look no further|In the ever-evolving|game-changer that|revolutioniz", re.I)


def safe_seo_title(title):
    """截到 ≤70 字符，词边界断句（禁止断词截断如 '...2026 G'）。"""
    t = re.sub(r"\s+", " ", (title or "").strip()).rstrip(" ,;:—-")
    if len(t) <= 70:
        return t or None
    cut = t[:70]
    if not cut.endswith((" ",)) and len(t) > 70:
        # 回退到最后一个词边界
        sp = cut.rfind(" ")
        if sp > 35:
            cut = cut[:sp]
    return cut.rstrip(" ,;:—-") or None


def safe_seo_desc(text):
    """从正文取 1-2 句拼 description（≤160 字符）。模板句/营销腔句子直接剔除；
    剔完不足 40 字符返回 None（该页改道重写队列，不机械 patch）。"""
    t = re.sub(r"\s+", " ", text or "").strip()
    if not t:
        return None
    sents = re.split(r"(?<=[.!?。！？])\s+", t)
    keep = []
    for s in sents:
        s = s.strip()
        if not s or BOILERPLATE.search(s):
            continue
        keep.append(s)
        if sum(len(x) for x in keep) > 200:
            break
    out = ""
    for s in keep:
        if out and len(out) + len(s) + 1 > 160:
            break
        out = (out + " " + s).strip() if out else s
    out = out[:160].rstrip()
    if len(out) < 40 or BOILERPLATE.search(out):
        return None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", default=None)
    ap.add_argument("--outdir", default=None, help="默认 insight-data/Page Analytic/fix-<date>/")
    ap.add_argument("--write-patch", action="store_true", help="额外生成 sanity patch ndjson（仍不落库）")
    ap.add_argument("--lang-filter", default="", help="仅处理这些语言（逗号分隔），空=全部")
    args = ap.parse_args()

    cfg = json.loads(CADENCE.read_text())
    fix_cfg = cfg.get("mainContentFix", {})
    auto = set(fix_cfg.get("autoFix", []))
    queue_classes = set(fix_cfg.get("queueRewrite", []))
    token = sanity_token()

    audit_path = latest_audit(args.audit)
    A = json.loads(audit_path.read_text())
    stamp = time.strftime("%Y-%m-%d")
    outdir = Path(args.outdir) if args.outdir else (
        Path(__file__).resolve().parents[2] / "insight-data" / "Page Analytic" / f"fix-{stamp}")
    outdir.mkdir(parents=True, exist_ok=True)
    lang_f = {x.strip() for x in args.lang_filter.split(",") if x.strip()}

    plan, patches, queue = [], [], []

    def want(row):
        return (not lang_f) or (row.get("lang") in lang_f)

    # 1) blog 机械修复候选
    for row in A.get("blog_issues", []):
        if row.get("lang") != "en" or not want(row):
            continue
        iss = set(row.get("issues", []))
        doc_id = row["_id"]
        acts = []
        if "seo-missing" in iss and "seo-fill-from-title" in auto:
            acts.append("seo-fill-from-title")
        if "no-image" in iss and "cover-og-fallback" in auto:
            acts.append("cover-og-fallback")
        for a in acts:
            plan.append({"kind": "blog", "id": doc_id, "slug": row.get("slug"), "action": a})
        rw = sorted(k for k in ("thin", "slop") if any(i.startswith(k) for i in iss))
        if rw and set(rw) & queue_classes:
            queue.append({"kind": "blog", "id": doc_id, "lang": row.get("lang"),
                          "slug": row.get("slug"), "title": row.get("title"),
                          "words": row.get("words"), "issues": rw})

    # 2) 重写队列（全语言）
    for row in A.get("comp_issues", []):
        if not want(row):
            continue
        iss = set(row.get("issues", []))
        rw = sorted(k for k in ("thin", "slop", "no-faq", "no-cta", "sections-empty", "bodyJson-broken")
                    if any(i == k or i.startswith(k + ":") for i in iss))
        if rw and (set(rw) & queue_classes or (row.get("lang") == "en")):
            queue.append({"kind": row.get("pageType"), "id": row["_id"], "lang": row.get("lang"),
                          "slug": row.get("slug"), "title": row.get("title"),
                          "words": row.get("words"), "issues": rw})
    for g in A.get("untranslated", []):
        if "untranslated" in queue_classes:
            queue.append({"kind": g["kind"], "id": g["id"], "lang": g["lang"], "slug": g["slug"],
                          "title": "", "words": None, "issues": ["untranslated"]})
    for g in A.get("lang_garbage", []):
        if "lang-garbage" in queue_classes:
            queue.append({"kind": g["kind"], "id": g["id"], "lang": g["lang"], "slug": g["slug"],
                          "title": "", "words": None, "issues": ["lang-garbage"]})
    # 同序列模板化组
    if "seq-template" in queue_classes:
        for key, v in (A.get("seq_templates") or {}).items():
            for slug in v.get("slugs", []):
                queue.append({"kind": key.split("|")[0], "id": None, "lang": key.split("|")[1],
                              "slug": slug, "title": "", "words": None, "issues": ["seq-template"]})

    # 3) 生成 safe patch 内容（需再拉一次目标文档的字段）
    seo_ids = [p["id"] for p in plan if p["action"] == "seo-fill-from-title"]
    cov_ids = [p["id"] for p in plan if p["action"] == "cover-og-fallback"]
    need_ids = list(dict.fromkeys(seo_ids + cov_ids))[:500]
    docs = {}
    if need_ids and args.write_patch:
        print(f"pulling {len(need_ids)} docs for patch material ...", file=sys.stderr)
        for i in range(0, len(need_ids), 40):
            chunk = need_ids[i:i + 40]
            ids = json.dumps(chunk)
            got = q_one(f'*[_id in {ids}]{{_id,title,language,"text":pt::text(body),"og":coalesce(seo.ogImage.url,""),"ogAlt":coalesce(seo.ogImage.alt,"")}}', token)
            for d in got or []:
                docs[d["_id"]] = d
            time.sleep(1)
    for p in plan:
        d = docs.get(p["id"])
        if not d:
            continue
        if p["action"] == "seo-fill-from-title":
            st, sd = safe_seo_title(d.get("title")), safe_seo_desc(d.get("text"))
            sets = {}
            if st:
                sets["seo.title"] = st
            if sd:
                sets["seo.description"] = sd
            if sets:
                patches.append({"id": p["id"], "patch": {"set": sets}})
        elif p["action"] == "cover-og-fallback":
            if d.get("og"):
                patches.append({"id": p["id"], "patch": {"set": {
                    "coverImage": {"_type": "image", "alt": d.get("ogAlt") or safe_seo_title(d.get("title")) or "",
                                   "url": d["og"]}}}})
    dedup = {}
    for p in patches:
        if p["id"] in dedup:
            dedup[p["id"]]["patch"]["set"].update(p["patch"]["set"])
        else:
            dedup[p["id"]] = p
    patches = list(dedup.values())

    # 4) 落盘
    plan_path = outdir / "fix-plan.md"
    L = ["# 主站内容修复计划", f"- 来源审计：{audit_path}", f"- 生成：{stamp}",
         f"- 模式：{'dry-run（未生成 patch）' if not args.write_patch else 'patch 已生成，待人审导入'}",
         f"- 发布闸：{fix_cfg.get('publishGate', 'ready-await-human')}", ""]
    counts = {}
    for p in plan:
        counts[p["action"]] = counts.get(p["action"], 0) + 1
    L.append(f"机械修复候选 {len(plan)} 项：" + ", ".join(f"{k} {v}" for k, v in counts.items()))
    for p in plan[:40]:
        L.append(f"- {p['action']} → {p['kind']}:{p['slug']} ({p['id']})")
    L.append("")
    L.append(f"重写队列 {len(queue)} 项（含 seq-template 展开页）。")
    qn = {}
    for q in queue:
        for k in q["issues"]:
            qn[k] = qn.get(k, 0) + 1
    L.append("分类计数：" + ", ".join(f"{k} {v}" for k, v in sorted(qn.items(), key=lambda x: -x[1])))
    plan_path.write_text("\n".join(L))
    print("plan ->", plan_path, file=sys.stderr)

    qpath = outdir / "rewrite-queue.ndjson"
    qpath.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in queue))
    print("queue ->", qpath, f"({len(queue)} 条)", file=sys.stderr)

    if args.write_patch and patches:
        ppath = outdir / "safe-fixes.ndjson"
        ppath.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in patches))
        print(f"patch -> {ppath} ({len(patches)} 条，待人审导入 lovart-sanity-publish)", file=sys.stderr)
    print(f"DONE. 机械修复候选 {len(plan)}，重写队列 {len(queue)}，patch {len(patches) if args.write_patch else 0}。",
          file=sys.stderr)


if __name__ == "__main__":
    main()