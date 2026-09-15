#!/usr/bin/env python3
"""render-status.py — MFlow status page generator.

Reads pipeline state / sentinel / audit artifacts from the project tree and
renders a static status page to <project>/run/status/ (index.html + status.json).
Served by the mflow Apache vhost (port 8088 on the server).

Usage:
    python3 render-status.py            # render to run/status/
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
OUT = PROJECT / "run" / "status"


def pipeline_summary():
    f = PROJECT / "1-3 GenFlow" / ".pipeline" / "pipeline-state.json"
    if not f.exists():
        return {"total": 0, "by_phase": {}, "note": "state file missing"}
    d = json.loads(f.read_text())
    items = d.get("items", {})
    phases = {}
    for it in items.values():
        ph = it.get("phase", "?")
        phases[ph] = phases.get(ph, 0) + 1
    return {"total": len(items), "by_phase": phases}


def latest(pattern, base):
    files = sorted(base.glob(pattern), reverse=True)
    return files[0] if files else None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M %Z").strip()

    sent = latest("Lovart-Sentinel-*-daily.md", PROJECT / "1-2 Insight" / "Lovart ORM")
    sent_date = None
    if sent:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", sent.name)
        sent_date = m.group(1) if m else sent.stat().st_mtime

    audit = latest("fm-check-*.txt", PROJECT / "1-1 Harness" / "11-knowledge" / "audit" / "reports")

    data = {
        "generated_at": now,
        "host": "server (/var/www/mflow)",
        "pipeline": pipeline_summary(),
        "sentinel_latest_daily": str(sent.name) if sent else None,
        "sentinel_latest_date": sent_date,
        "fm_check_latest": audit.name if audit else None,
    }
    (OUT / "status.json").write_text(json.dumps(data, ensure_ascii=False, indent=2))

    rows = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>"
        for k, v in [
            ("生成时间", now),
            ("管线 items", f"{data['pipeline']['total']}"),
            ("阶段分布", json.dumps(data["pipeline"]["by_phase"], ensure_ascii=False)),
            ("舆情日报", str(sent_date or "—")),
            ("fm-check", audit.name if audit else "—"),
        ]
    )
    html = f"""<!doctype html><html lang="zh"><meta charset="utf-8">
<title>MFlow Status</title>
<style>body{{font-family:-apple-system,sans-serif;max-width:640px;margin:48px auto;padding:0 16px;color:#222}}
h1{{font-size:20px}} table{{border-collapse:collapse;width:100%}} td{{border-bottom:1px solid #eee;padding:8px 4px}}
td:first-child{{color:#666;width:130px}} .ok{{color:#0a7d38;font-weight:600}}</style>
<h1>MFlow 状态页 <span class="ok">●</span></h1>
<p>Lovart GEO 内容工作流 · 独立实例（与 XMP/OpenFlow 隔离）</p>
<table>{rows}</table>
<p style="color:#999;font-size:12px">pipeline.json: /status.json · 刷新: mflow-status.timer (30min) · 数据源: pipeline-state / Sentinel / fm-check</p>"""
    (OUT / "index.html").write_text(html)
    print(f"status rendered -> {OUT}/index.html")


if __name__ == "__main__":
    sys.exit(main())
