#!/usr/bin/env python3
"""Export one S1 batch as per-page MCP arg files + manifest on stdout."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
THRESHOLD = 12000  # use props-only above this content len for speed


def main() -> None:
    out = subprocess.check_output(
        [sys.executable, str(SYNC / "notion-push-next.py"), "S1", "3"], text=True
    )
    d = json.loads(out)
    if d["count"] == 0:
        print(json.dumps({"done": True}))
        return
    parent = d["parent"]
    manifest = {"rel_paths": d["rel_paths"], "pages": []}
    for i, p in enumerate(d["pages"]):
        clen = len(p.get("content", ""))
        full = {"parent": parent, "pages": [p]}
        props = {"parent": parent, "pages": [{"properties": p["properties"]}]}
        use = "full" if clen <= THRESHOLD else "props"
        path = Path(f"/tmp/s1-mcp-export-{i}.json")
        payload = full if use == "full" else props
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        manifest["pages"].append(
            {
                "i": i,
                "name": p["properties"]["Name"],
                "content_len": clen,
                "use": use,
                "file": str(path),
                "page_id_for_update": None,
            }
        )
    Path("/tmp/s1-mcp-export-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
