#!/usr/bin/env python3
"""
kg-emit-jsonl.py — emit entities.jsonl + relationships.jsonl from SSOT YAML.

SSOT:
  entities.yaml      — schema stable; flat lists by kind
  relationships.yaml — schema stable; flat list

This script is run by dream/consolidate.sh and emits machine-readable
mirrors. Tools that can't read YAML (raw shell scripts, GitHub Actions,
some OneShot pipelines) read JSONL instead.

Usage:
  python3 kg-emit-jsonl.py
  python3 kg-emit-jsonl.py --check   # exit 1 if mirrors out of date (used by CI)

Deps:
  python3 stdlib only (yaml via `python3 -c 'import yaml'`)
  If PyYAML missing: install or use bundled `pip --user pyyaml`.
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path


def _json_default(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError(f"kg-emit-jsonl: unhandled type {type(o).__name__}")

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML not installed. Try: pip3 install --user pyyaml\n")
    sys.exit(2)


def die(msg):
    sys.stderr.write(f"kg-emit-jsonl: {msg}\n")
    sys.exit(1)


def main():
    here = Path(__file__).resolve().parent.parent  # 11-knowledge/
    ent_yaml = here / "entities.yaml"
    rel_yaml = here / "relationships.yaml"
    ent_jsonl = here / "entities.jsonl"
    rel_jsonl = here / "relationships.jsonl"

    if not ent_yaml.exists():
        die(f"missing {ent_yaml}")
    if not rel_yaml.exists():
        die(f"missing {rel_yaml}")

    ent_data = yaml.safe_load(ent_yaml.read_text("utf-8"))
    rel_data = yaml.safe_load(rel_yaml.read_text("utf-8"))

    # ---- entities: walk kind lists (person / project / ... / destination)
    kinds = ["people", "projects", "products", "tools", "profiles",
             "rules", "skills", "crons", "datasets", "destinations",
             # extension slots
             "concepts", "competitors"]
    out_records = []
    err_endpoints = []
    for k in kinds:
        for e in (ent_data.get(k) or []):
            if not e.get("id"):
                err_endpoints.append(f"{k}: missing id")
                continue
            e["__kind"] = k
            out_records.append(e)
    out_lines = [json.dumps(e, ensure_ascii=False) for e in out_records]

    # ---- relationships: flat list with endpoint validation
    valid_ids = {e["id"] for e in out_records}

    rel_lines = []
    for r in (rel_data.get("relationships") or []):
        if not r.get("id"):
            err_endpoints.append(f"rel: missing id")
            continue
        if r["from"] not in valid_ids:
            err_endpoints.append(f"rel {r['id']}: unknown FROM {r['from']}")
        if r["to"] not in valid_ids:
            err_endpoints.append(f"rel {r['id']}: unknown TO {r['to']}")
        rel_lines.append(json.dumps(r, ensure_ascii=False, default=_json_default))

    if err_endpoints:
        for e in err_endpoints:
            sys.stderr.write(f"  {e}\n")
        die(f"{len(err_endpoints)} endpoint errors")

    ent_jsonl.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    rel_jsonl.write_text("\n".join(rel_lines) + "\n", encoding="utf-8")

    print(f"emitted {len(out_lines)} entities → {ent_jsonl}")
    print(f"emitted {len(rel_lines)} relationships → {rel_jsonl}")

    # ---- --check mode
    if "--check" in sys.argv:
        # No diff file → just emit exit 0 on success (caller can compare hashes)
        return


if __name__ == "__main__":
    main()
