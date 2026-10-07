#!/usr/bin/env python3
"""统一 CLI：python3 cli.py --adapter webhook --item-id x --title t --body-file f.md --cfg run/cms.json"""
import argparse, importlib, json, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--adapter", required=True)
ap.add_argument("--item-id", required=True)
ap.add_argument("--title", default="")
ap.add_argument("--body-file", required=True)
ap.add_argument("--cfg", default="run/cms.json")
ap.add_argument("--lang", default="en")
a = ap.parse_args()

adapter = importlib.import_module(a.adapter)
body = Path(a.body_file).read_text()
cfg = json.loads(Path(a.cfg).read_text()).get(a.adapter, {}) if Path(a.cfg).exists() else {}
item = {"id": a.item_id, "title": a.title or a.item_id, "body_md": body, "lang": a.lang, "meta": {}}
result = adapter.publish(item, cfg)
print(json.dumps(result, ensure_ascii=False))
sys.exit(0 if result.get("ok") else 1)
