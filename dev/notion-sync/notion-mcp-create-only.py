#!/usr/bin/env python3
"""Strip content from batch JSON for properties-only notion-create-pages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

BATCH = Path("/tmp/notion-r1-current-batch.json")


def main() -> None:
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    pages = [{"properties": p["properties"]} for p in payload["pages"]]
    out = {"parent": payload["parent"], "pages": pages, "count": len(pages)}
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
