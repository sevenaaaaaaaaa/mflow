#!/usr/bin/env python3
"""Export one R2 content op args for MCP (used by agent loop)."""
import json, sys
from pathlib import Path

SYNC = Path(__file__).parent

def main():
    # Run executor next and export args
    import subprocess
    subprocess.run([sys.executable, str(SYNC / "notion-r2-mcp-executor.py"), "next"], check=True)
    d = json.loads(Path("/tmp/r2-next-mcp-op.json").read_text())
    if d.get("done"):
        print(json.dumps(d, ensure_ascii=False))
        return
    if d.get("error"):
        print(json.dumps(d, ensure_ascii=False))
        sys.exit(2)
    args = d["op"]["args"]
    Path("/tmp/r2-mcp-args.json").write_text(json.dumps(args, ensure_ascii=False), encoding="utf-8")
    meta = d.get("meta", {})
    sz = len(args.get("new_str", args.get("content", "")))
    print(json.dumps({"tool": d["op"]["tool"], "meta": meta, "page_id": args.get("page_id"), "command": args.get("command"), "size": sz, "position": args.get("position")}, ensure_ascii=False))

if __name__ == "__main__":
    main()
