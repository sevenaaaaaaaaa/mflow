#!/usr/bin/env python3
"""示例数据源插件 — 演示 source 类型插件的最小实现。
collect() 返回 dict，由调度管线写入 Data Ingestion（结构与其它源一致）。"""
import json, os, urllib.request
from datetime import date

def collect(cfg=None):
    cfg = cfg or {}
    url = cfg.get("url")
    items = []
    if url:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read())
        items = data if isinstance(data, list) else data.get("items", [])
    return {"source": "sample-source", "date": date.today().isoformat(), "count": len(items), "items": items[:50]}

if __name__ == "__main__":
    print(json.dumps(collect(), ensure_ascii=False)[:500])
