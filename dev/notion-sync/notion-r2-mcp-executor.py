#!/usr/bin/env python3
"""R2 batch MCP executor: props-only create + content updates + batch record."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SYNC = Path(__file__).parent
BATCH_DIR = SYNC / ".batch-out"
PROGRESS = SYNC / "sync-pushed.jsonl"
STATE = SYNC / ".mcp-r2-exec-state.json"
NEXT_OP = Path("/tmp/r2-next-mcp-op.json")
DS = "235b9609-b155-491e-9801-b1504abe99c2"
CHUNK = 12000
REPLACE_MAX = 25000

# R2-001 pages created props-only before content fill
PRE_CREATED = {
    "insight-data/Keywords Research/SEO Report/annual/Clawx_Lovart_SEO_深度分析报告_20260508.md": "379fc0c7-1bd5-81e4-acd9-f67289f70a97",
    "insight-data/Keywords Research/SEO Report/annual/Google_vs_Bing_搜索对比分析_20260514.md": "379fc0c7-1bd5-8195-ad62-fb11e2b70f71",
    "insight-data/Keywords Research/SEO Report/annual/Lovart 关键词终极洞察.md": "379fc0c7-1bd5-8135-840e-ea8d4b0565c8",
}


def done_paths() -> set[str]:
    done: set[str] = set()
    if PROGRESS.exists():
        for line in PROGRESS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["rel_path"])
    return done


def pending_batches() -> list[Path]:
    done = done_paths()
    out: list[Path] = []
    for path in sorted(BATCH_DIR.glob("R2-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if any(r not in done for r in data["rel_paths"]):
            out.append(path)
    return out


def content_ops(batch_file: Path, page_ids: list[str]) -> list[dict]:
    raw = subprocess.check_output(
        [sys.executable, str(SYNC / "notion-r2-batch-helper.py"), "content", str(batch_file), *page_ids],
        text=True,
        encoding="utf-8",
    )
    return json.loads(raw)


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"batch_idx": 0, "phase": "create", "page_idx": 0, "content_idx": 0, "page_ids": [], "failures": []}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def counts() -> dict:
    done = done_paths()
    total = synced = 0
    for line in (SYNC / "sync-queue.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e["batch"] != "R2":
            continue
        total += 1
        if e["rel_path"] in done:
            synced += 1
    by_batch: dict[str, dict[str, int]] = {}
    for path in sorted(BATCH_DIR.glob("R2-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        name = f"R2-{data['index']:03d}"
        t = data["count"]
        s = sum(1 for r in data["rel_paths"] if r in done)
        by_batch[name] = {"total": t, "synced": s, "pushed": s}
    return {"R2": {"total": total, "synced": synced, "remaining": total - synced}, "by_batch": by_batch}


def next_op() -> dict | None:
    st = load_state()
    batches = pending_batches()
    if not batches:
        return None

    bidx = min(st.get("batch_idx", 0), len(batches) - 1)
    batch_file = batches[bidx]
    data = json.loads(batch_file.read_text(encoding="utf-8"))
    phase = st.get("phase", "create")
    page_idx = st.get("page_idx", 0)
    rel_paths = data["rel_paths"]
    pages = data["mcp"]["pages"]

    if phase == "create":
        props_pages = [{"properties": p["properties"]} for p in pages]
        # R2-001: pages already exist
        if batch_file.name == "R2-001.json" and all(r in PRE_CREATED for r in rel_paths):
            st["page_ids"] = [PRE_CREATED[r] for r in rel_paths]
            st["phase"] = "content"
            st["content_idx"] = 0
            save_state(st)
            return next_op()
        op = {
            "tool": "notion-create-pages",
            "args": {"parent": {"data_source_id": DS, "type": "data_source_id"}, "pages": props_pages},
        }
        meta = {"batch": batch_file.name, "phase": "create", "pages": len(props_pages), "rel_paths": rel_paths}
        save_state({**st, "phase": "await_ids"})
        return {"op": op, "meta": meta}

    if phase == "await_ids":
        return {"error": "need page_ids", "meta": {"batch": batch_file.name, "expected": len(pages)}}

    if phase == "content":
        page_ids = st.get("page_ids", [])
        if len(page_ids) != len(pages):
            return {"error": "page_ids length mismatch", "meta": {"batch": batch_file.name}}
        done = done_paths()
        pid_to_rel = {pid: rel for pid, rel in zip(page_ids, rel_paths)}
        ops = [
            op
            for op in content_ops(batch_file, page_ids)
            if pid_to_rel.get(op["page_id"], "") not in done
        ]
        cidx = st.get("content_idx", 0)
        if cidx >= len(ops):
            st["phase"] = "apply"
            save_state(st)
            return next_op()
        item = ops[cidx]
        args = {"page_id": item["page_id"], "command": item["command"]}
        if item["command"] == "replace_content":
            args["new_str"] = item["new_str"]
        else:
            args["content"] = item["content"]
            args["position"] = item["position"]
        st["content_idx"] = cidx + 1
        save_state(st)
        return {
            "op": {"tool": "notion-update-page", "args": args},
            "meta": {
                "batch": batch_file.name,
                "phase": "content",
                "op_idx": cidx,
                "total_ops": len(ops),
                "name": item.get("name", ""),
            },
        }

    if phase == "apply":
        subprocess.check_call([sys.executable, str(SYNC / "notion-apply-batch.py"), str(batch_file)])
        st = {
            "batch_idx": bidx + 1,
            "phase": "create",
            "page_idx": 0,
            "content_idx": 0,
            "page_ids": [],
            "failures": st.get("failures", []),
        }
        save_state(st)
        return next_op()

    return None


def set_page_ids(ids: list[str]) -> None:
    st = load_state()
    st["page_ids"] = ids
    st["phase"] = "content"
    st["content_idx"] = 0
    save_state(st)


def advance(page_ids: list[str] | None = None, error: str | None = None) -> dict:
    st = load_state()
    if error:
        st.setdefault("failures", []).append(error)
        save_state(st)
    if page_ids:
        set_page_ids(page_ids)
    return {"state": load_state(), "counts": counts()}


def emit_next_file() -> dict:
    item = next_op()
    if item is None:
        out = {"done": True, "counts": counts()}
    else:
        out = item
    NEXT_OP.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        print(json.dumps({"state": load_state(), "counts": counts(), "pending_batches": [p.name for p in pending_batches()]}, ensure_ascii=False))
    elif cmd == "next":
        print(json.dumps(emit_next_file(), ensure_ascii=False))
    elif cmd == "set-ids":
        set_page_ids(sys.argv[2:])
        print(json.dumps({"state": load_state()}, ensure_ascii=False))
    elif cmd == "reset":
        STATE.unlink(missing_ok=True)
        print(json.dumps({"reset": True}, ensure_ascii=False))
    else:
        raise SystemExit(f"unknown: {cmd}")


if __name__ == "__main__":
    main()
