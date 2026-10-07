#!/usr/bin/env python3
"""Print current pending MCP op summary and export args for agent CallMcpTool."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SYNC = Path(__file__).parent
NEXT = Path("/tmp/r2-next-mcp-op.json")
ARGS = Path("/tmp/r2-mcp-args.json")


def main() -> None:
    if not NEXT.exists():
        print(json.dumps({"error": "no /tmp/r2-next-mcp-op.json; run executor next first"}))
        sys.exit(1)
    d = json.loads(NEXT.read_text(encoding="utf-8"))
    if d.get("done"):
        print(json.dumps({"done": True, "counts": d.get("counts", {})}, ensure_ascii=False))
        return
    if d.get("error"):
        print(json.dumps(d, ensure_ascii=False))
        sys.exit(2)
    op = d["op"]
    args = op["args"]
    ARGS.write_text(json.dumps(args, ensure_ascii=False), encoding="utf-8")
    meta = d.get("meta", {})
    sz = len(args.get("new_str", args.get("content", "")))
    out = {
        "tool": op["tool"],
        "meta": meta,
        "args_file": str(ARGS),
        "args_size": len(json.dumps(args, ensure_ascii=False)),
        "content_len": sz,
        "page_id": args.get("page_id"),
        "command": args.get("command"),
        "pages": len(args.get("pages", [])),
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
