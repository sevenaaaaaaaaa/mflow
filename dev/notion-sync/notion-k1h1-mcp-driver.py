#!/usr/bin/env python3
"""Prepare next K1/H1 MCP batch args on disk for agent CallMcpTool."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
RUNNER = SYNC / "notion-push-mcp-runner.py"
OUT = Path("/tmp/current-k1h1-mcp-args.json")
META = Path("/tmp/current-k1h1-mcp-meta.json")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if cmd == "prepare":
        raw = subprocess.check_output([sys.executable, str(RUNNER), "emit-next"], text=True)
        data = json.loads(raw)
        if data.get("done"):
            print(json.dumps({"done": True, "counts": data.get("counts", {})}, ensure_ascii=False))
            return
        mcp = data["mcp"]
        OUT.write_text(json.dumps(mcp, ensure_ascii=False), encoding="utf-8")
        meta = {
            "file": data.get("file"),
            "batch": data.get("batch"),
            "rel_paths": data.get("rel_paths", []),
            "remaining_batches": data.get("remaining_batches"),
            "counts": data.get("counts"),
            "bytes": len(json.dumps(mcp, ensure_ascii=False)),
        }
        META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return
    if cmd == "meta":
        print(META.read_text(encoding="utf-8") if META.exists() else "{}")
        return
    raise SystemExit(f"unknown cmd: {cmd}")


if __name__ == "__main__":
    main()
