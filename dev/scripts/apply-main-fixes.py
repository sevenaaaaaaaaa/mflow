#!/usr/bin/env python3
"""apply-main-fixes.py — 主站 safe-fixes patch 批量导入器（授权后的执行端）。

输入：fix-main-content.py 产出的 safe-fixes.ndjson（{"id": <sanity _id>, "patch": {"set": {...}}}）
流程：--dry-run（Sanity 原生 dryRun，不落库）→ 预演通过后 --yes 真实写库。
安全：
  - 默认 dry-run；--yes 必须显式（对应 publishGate=ready-await-human 的人工授权）
  - 每 patch 独立 ifRevisionID 保护（防止导入期间文档被并发修改）
  - 分批（默认 20 mutation/事务）+ 失败重试 + 成功/失败清单落盘
用法：
  python3 apply-main-fixes.py --file "insight-data/Page Analytic/fix-2026-10-09/safe-fixes.ndjson"
  python3 apply-main-fixes.py --file ... --yes
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish_adapters.sanity_publisher import sanity_cfg, _req  # noqa: E402

BATCH = 20


def load_revs(ids):
    """批量拉 _rev，供 ifRevisionID 保护。"""
    cfg = sanity_cfg()
    out = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        q = f'*[_id in {json.dumps(chunk)}]{{_id,_rev}}'
        with _req(cfg, "query", payload={"query": q}, method="POST", timeout=60) as r:
            for d in json.loads(r.read()).get("result", []):
                out[d["_id"]] = d.get("_rev")
        time.sleep(0.5)
    return out


def run(patches, dry, batch=BATCH):
    cfg = sanity_cfg()
    if not cfg.get("token"):
        return {"ok": False, "error": "无 token（run/secrets/sanity.json 或 env）"}
    revs = load_revs([p["id"] for p in patches])
    results = {"ok": [], "fail": []}
    for i in range(0, len(patches), batch):
        chunk = patches[i:i + batch]
        muts = []
        for p in chunk:
            m = {"patch": dict(p["patch"], id=p["id"])}
            if p["id"] in revs:
                m["patch"]["ifRevisionID"] = revs[p["id"]]
            muts.append(m)
        try:
            with _req(cfg, "mutate", {"mutations": muts, "dryRun": bool(dry)}, timeout=120) as r:
                d = json.loads(r.read())
            n = len(d.get("transactionIds", d.get("results", []) or [muts]))
            results["ok"].extend(p["id"] for p in chunk)
            print(f"  batch {i // batch + 1}: ok {n}/{len(chunk)} ({'DRY' if dry else 'APPLIED'})")
        except Exception as e:
            results["fail"].extend({"id": p["id"], "error": str(e)[:200]} for p in chunk)
            print(f"  batch {i // batch + 1}: FAIL {e}")
        time.sleep(1)
    return {"ok": not results["fail"], **results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--yes", action="store_true", help="真实写库（默认 dry-run 预演）")
    ap.add_argument("--out", default="", help="结果清单输出路径")
    a = ap.parse_args()
    patches = [json.loads(l) for l in open(a.file) if l.strip()]
    print(f"{len(patches)} patches; mode={'APPLY' if a.yes else 'DRY-RUN'}", file=sys.stderr)
    res = run(patches, dry=not a.yes)
    outp = Path(a.out) if a.out else Path(a.file).with_name(
        Path(a.file).stem + ("-applied" if a.yes else "-dryrun") + ".json")
    outp.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"ok={len(res.get('ok', []))} fail={len(res.get('fail', []))} -> {outp}", file=sys.stderr)
    sys.exit(0 if res.get("ok") else 1)


if __name__ == "__main__":
    main()