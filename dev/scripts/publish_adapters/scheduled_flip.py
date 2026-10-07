#!/usr/bin/env python3
"""scheduled_flip.py — 定时发布翻转（PRD §6：scheduled 态由任务在到点后翻转为 published）。

扫描 blog 文档中 status=="scheduled" 且 publishedAt<=now() 的，逐篇 patch status=published
（带 ifRevisionID，不覆盖并发改动）。compositePage 无 status 字段（写入即可见），不在扫描范围。

用法：
  python3 scheduled_flip.py            # dry-run：只列出将翻转的文档
  python3 scheduled_flip.py --yes      # 真实执行

接入调度（部署机 systemd timer 或 crontab，建议每 5-15 分钟一次）：
  */10 * * * * cd /path/to/mflow && python3 "dev/scripts/publish_adapters/scheduled_flip.py" --yes >> run/logs/flip.log 2>&1
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sanity_publisher import sanity_cfg, _req  # noqa: E402

QUERY = ('*[_type=="blog" && status=="scheduled" && defined(publishedAt) && publishedAt <= now()]'
         '{_id,_rev,slug,language,publishedAt}')


def flip(dry_run=True):
    cfg = sanity_cfg()
    if not cfg["token"]:
        return {"ok": False, "error": "未配置 SANITY_TOKEN"}
    try:
        with _req(cfg, "query", {"query": QUERY}, timeout=30) as r:
            due = json.loads(r.read()).get("result") or []
    except Exception as e:
        return {"ok": False, "error": f"查询失败：{str(e)[:200]}"}
    flipped = []
    mutations = []
    for d in due:
        if not isinstance(d, dict) or not d.get("_id"):
            continue
        mutations.append({"patch": {"id": d["_id"], "ifRevisionID": d.get("_rev"),
                                    "set": {"status": "published"}}})
        flipped.append({"id": d["_id"], "slug": (d.get("slug") or {}).get("current", ""),
                        "lang": d.get("language", ""), "publishedAt": d.get("publishedAt")})
    if mutations:
        try:
            with _req(cfg, "mutate", {"mutations": mutations, "dryRun": bool(dry_run)}, timeout=120) as r:
                res = json.loads(r.read())
        except Exception as e:
            return {"ok": False, "error": f"翻转写入失败：{str(e)[:200]}", "pending": flipped}
    else:
        res = None
    return {"ok": True, "dry_run": bool(dry_run), "flipped": len(flipped), "items": flipped,
            "result": res}


if __name__ == "__main__":
    print(json.dumps(flip(dry_run=not ("--yes" in sys.argv)), ensure_ascii=False, indent=1))
