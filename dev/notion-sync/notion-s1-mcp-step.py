#!/usr/bin/env python3
"""One step of S1 MCP push loop: emit batch JSON or record rel_paths."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
PUSH = SYNC / "notion-push-next.py"
RECORD = SYNC / "notion-record-push.py"


def emit(limit: int = 3) -> dict:
    out = subprocess.check_output([sys.executable, str(PUSH), "S1", str(limit)], text=True)
    return json.loads(out)


def record(paths: list[str]) -> None:
    if paths:
        subprocess.run([sys.executable, str(RECORD), *paths], check=True)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    if cmd == "next":
        d = emit(3)
        if d["count"] == 0:
            print(json.dumps({"done": True}))
            return
        payload = {"parent": d["parent"], "pages": d["pages"], "rel_paths": d["rel_paths"]}
        out = Path("/tmp/s1-mcp-step.json")
        out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        print(
            json.dumps(
                {
                    "count": d["count"],
                    "rel_paths": d["rel_paths"],
                    "file": str(out),
                    "size": len(json.dumps(payload, ensure_ascii=False)),
                },
                ensure_ascii=False,
            )
        )
    elif cmd == "split":
        step = Path("/tmp/s1-mcp-step.json")
        d = json.loads(step.read_text(encoding="utf-8"))
        parent = d["parent"]
        out = []
        for i, p in enumerate(d["pages"]):
            full = {"parent": parent, "pages": [p]}
            props = {"parent": parent, "pages": [{"properties": p["properties"]}]}
            full_path = Path(f"/tmp/s1-mcp-page-{i}.json")
            props_path = Path(f"/tmp/s1-mcp-props-{i}.json")
            full_path.write_text(json.dumps(full, ensure_ascii=False), encoding="utf-8")
            props_path.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
            clen = len(p.get("content", ""))
            out.append(
                {
                    "i": i,
                    "name": p["properties"]["Name"],
                    "content_len": clen,
                    "use": "full" if clen <= 7000 else "props",
                    "file": str(full_path if clen <= 7000 else props_path),
                }
            )
        print(json.dumps({"rel_paths": d["rel_paths"], "pages": out}, ensure_ascii=False))
    elif cmd == "record":
        record(sys.argv[2:])
        print("recorded", len(sys.argv) - 2)
    elif cmd == "status":
        done: set[str] = set()
        prog = SYNC / "sync-pushed.jsonl"
        if prog.exists():
            for line in prog.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    done.add(json.loads(line)["rel_path"])
        total = synced = 0
        for line in (SYNC / "sync-queue.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if e["batch"] != "S1":
                continue
            total += 1
            if e["rel_path"] in done:
                synced += 1
        print(json.dumps({"total": total, "synced": synced, "remaining": total - synced}, ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
