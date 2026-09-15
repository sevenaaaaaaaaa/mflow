#!/usr/bin/env python3
"""
lovart-pipeline-state — single source of truth for content pipeline progress.

Problem this solves:
    S3 says "I'm done writing, next should be QA".
    S4 says "QA done, ready to publish".
    S5 says "imported".
    But without a shared state file, every agent re-derives this from scratch
    and gets it wrong: "should I run QA? or generate? I just ran QA, why
    is someone asking me to generate again?"

This script:
    1. Maintains `<state_path>/pipeline-state.json` with one record per item.
    2. Provides atomic write (tmp + rename) so concurrent agents don't corrupt.
    3. Exposes 7 subcommands (init/upsert/get/list/next/run/check/advance).
    4. Returns non-zero exit code on illegal transitions (so it's a hook, not a doc).

State machine (12 stages, 4 phase buckets):

    QUEUE  : S0-todo, S0-skip
    CREATE : S3-creating, S3-draft, S3-done
    REVIEW : S4-qa, S4-fix, S4-ready
    SHIP   : S5-importing, S5-published, S6-monitoring
    FINAL  : done, failed, escalated

Transitions enforced:
    S0-todo        → S3-creating | S0-skip
    S3-creating    → S3-draft    | S3-failed
    S3-draft       → S3-done     | S3-failed   (S3 must self-report done)
    S3-done        → S4-qa       | S3-failed   (QA must be requested)
    S4-qa          → S4-fix      | S4-ready    | S4-failed
    S4-fix         → S4-qa       (loop within REVIEW, max 3 fixes by default)
    S4-ready       → S5-importing | S4-failed
    S5-importing   → S5-published | S5-failed
    S5-published   → S6-monitoring | S5-failed
    S6-monitoring  → done | escalated
    Anything       → failed | escalated (terminal escape hatches)

Usage:
    pipeline_state.py init [--root PATH] [--state-path PATH]
    pipeline_state.py upsert --id ID [--category C] [--target-type T] [fields...]
    pipeline_state.py get --id ID
    pipeline_state.py list [--phase PHASE] [--stage STAGE] [--json]
    pipeline_state.py next [--phase PHASE]            # first item in QUEUE|REVIEW
    pipeline_state.py advance --id ID --to STAGE [--reason R]
    pipeline_state.py run --id ID [--qa-result JSON]  # QA result patch
    pipeline_state.py check --id ID                   # is it ready for next stage?
    pipeline_state.py summary                        # dashboard counters

Default state file: 1-3 GenFlow/.pipeline/pipeline-state.json
(This lives under the vault so it's git-tracked and dream-syncable.)

Audit trail: every advance/run writes an event to <state_path>/events.jsonl
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# SSOT paths (overridable via env or CLI)
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE
VAULT_ROOT = HERE.parents[3]   # Skills/06-orchestrate/<skill>/ → vault root
DEFAULT_STATE_DIR = VAULT_ROOT / "1-3 GenFlow" / ".pipeline"
DEFAULT_STATE_FILE = DEFAULT_STATE_DIR / "pipeline-state.json"
DEFAULT_EVENTS_FILE = DEFAULT_STATE_DIR / "events.jsonl"


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PHASES = ["QUEUE", "CREATE", "REVIEW", "SHIP", "FINAL"]

# All 12 legal stages (must match transition table above).
LEGAL_STAGES = {
    "S0-todo", "S0-skip",
    "S3-creating", "S3-draft", "S3-done", "S3-failed",
    "S4-qa", "S4-fix", "S4-ready", "S4-failed",
    "S5-importing", "S5-published",
    "S6-monitoring",
    "done", "failed", "escalated",
}

# Allowed forward transitions. Anything else raises TransitionError.
TRANSITIONS: dict[str, set[str]] = {
    "S0-todo":        {"S3-creating", "S0-skip", "failed", "escalated"},
    "S0-skip":        {"S3-creating", "failed", "escalated"},
    "S3-creating":    {"S3-draft", "S3-failed", "failed", "escalated"},
    "S3-draft":       {"S3-done", "S3-failed", "failed", "escalated"},
    "S3-done":        {"S4-qa", "S3-failed", "failed", "escalated"},
    "S4-qa":          {"S4-fix", "S4-ready", "S4-failed", "failed", "escalated"},
    "S4-fix":         {"S4-qa", "S4-failed", "failed", "escalated"},
    "S4-ready":       {"S5-importing", "S4-failed", "failed", "escalated"},
    "S5-importing":   {"S5-published", "S5-failed", "failed", "escalated"},
    "S5-published":   {"S6-monitoring", "S5-failed", "failed", "escalated"},
    "S6-monitoring":  {"done", "escalated", "failed"},
    # terminal stages
    "done":       set(),
    "failed":     set(),
    "escalated":  set(),
    "S3-failed":  {"S3-creating"},   # can retry by going back to creating
    "S4-failed":  {"S3-creating"},   # QA failed hard; re-create
    "S5-failed":  {"S4-qa"},         # import failed; re-QA
}

# Map stage → phase (for filtering)
STAGE_PHASE: dict[str, str] = {}
for s in ["S0-todo", "S0-skip"]:
    STAGE_PHASE[s] = "QUEUE"
for s in ["S3-creating", "S3-draft", "S3-done", "S3-failed"]:
    STAGE_PHASE[s] = "CREATE"
for s in ["S4-qa", "S4-fix", "S4-ready", "S4-failed"]:
    STAGE_PHASE[s] = "REVIEW"
for s in ["S5-importing", "S5-published", "S6-monitoring"]:
    STAGE_PHASE[s] = "SHIP"
for s in ["done", "failed", "escalated"]:
    STAGE_PHASE[s] = "FINAL"

# Default max fixes per item (anti Ralph-style bleed).
DEFAULT_MAX_FIXES = 3

# ID format: kebab-case only, 3-80 chars
ID_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{2,79}$")


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class StateError(Exception):
    """User-facing state error. Exit code 2."""

class TransitionError(StateError):
    """Illegal stage transition."""

class NotFoundError(StateError):
    """Item ID not in state file."""


# ---------------------------------------------------------------------------
# Atomic IO
# ---------------------------------------------------------------------------

def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _append_event(events_path: Path, event: dict) -> None:
    events_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, ensure_ascii=False)
    with events_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "items": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise StateError(f"state file corrupted: {path}: {e}") from e
    if not isinstance(data, dict) or "items" not in data:
        raise StateError(f"state file malformed (expected dict with 'items' key): {path}")
    return data


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_init(args) -> int:
    state_path = Path(args.state_path).expanduser()
    state_path.parent.mkdir(parents=True, exist_ok=True)
    if state_path.exists() and not args.force:
        print(f"[init] state already exists: {state_path}", file=sys.stderr)
        return 0
    _atomic_write_json(state_path, {"version": 1, "items": {}, "created_at": _now()})
    events_path = state_path.parent / "events.jsonl"
    if not events_path.exists():
        events_path.touch()
    print(f"[init] state created: {state_path}")
    print(f"[init] events log:   {events_path}")
    return 0


def cmd_upsert(args) -> int:
    state_path = Path(args.state_path).expanduser()
    state = _load_state(state_path)

    item_id = args.id
    if not ID_RE.match(item_id):
        raise StateError(f"invalid --id '{item_id}' (must match {ID_RE.pattern})")

    existing = state["items"].get(item_id)
    if existing is None:
        item: dict[str, Any] = {
            "id": item_id,
            "category": args.category or "blog",
            "target_type": args.target_type or "blog",
            "stage": "S0-todo",
            "phase": "QUEUE",
            "agent": None,
            "skill": None,
            "artifact_path": args.artifact_path or None,
            "qa": {"l1_block": None, "l2_block": None, "l7_block": None, "last_run": None, "fix_count": 0},
            "publish": {"sanity_id": None, "imported_at": None, "status": None},
            "fix_count": 0,
            "created_at": _now(),
            "updated_at": _now(),
            "history": [],
        }
    else:
        item = existing

    # Apply explicit field overrides
    for k in ("category", "target_type", "agent", "skill", "artifact_path"):
        v = getattr(args, k, None)
        if v is not None:
            item[k] = v
    item["updated_at"] = _now()

    state["items"][item_id] = item
    _atomic_write_json(state_path, state)

    _append_event(Path(args.events_path).expanduser(), {
        "ts": _now(),
        "event": "upsert",
        "id": item_id,
        "stage": item["stage"],
        "agent": item["agent"],
        "skill": item["skill"],
    })
    print(f"[upsert] {item_id} → stage={item['stage']} (exists={existing is not None})")
    return 0


def cmd_get(args) -> int:
    state = _load_state(Path(args.state_path).expanduser())
    item = state["items"].get(args.id)
    if item is None:
        raise NotFoundError(f"id not found: {args.id}")
    if args.json:
        print(json.dumps(item, indent=2, ensure_ascii=False))
    else:
        _print_item_human(item)
    return 0


def cmd_list(args) -> int:
    state = _load_state(Path(args.state_path).expanduser())
    items = list(state["items"].values())
    if args.phase:
        items = [i for i in items if i.get("phase") == args.phase.upper()]
    if args.stage:
        items = [i for i in items if i.get("stage") == args.stage]
    items.sort(key=lambda i: i.get("updated_at") or "")
    if args.json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
    else:
        if not items:
            print(f"[list] no items (filter: phase={args.phase}, stage={args.stage})")
            return 0
        print(f"[list] {len(items)} item(s)")
        for i in items:
            print(f"  - {i['id']:<48} stage={i['stage']:<14} phase={i['phase']:<6} agent={i.get('agent') or '-':<22} updates={i.get('fix_count', 0)}")
    return 0


def cmd_next(args) -> int:
    """Pick next item to work on: first item in QUEUE phase, else REVIEW phase."""
    state = _load_state(Path(args.state_path).expanduser())
    items = list(state["items"].values())
    if args.phase:
        items = [i for i in items if i.get("phase") == args.phase.upper()]
    # Priority: S0-todo first, then S3-creating? No — only Todo (never in-flight).
    queue_items = [i for i in items if i.get("stage") == "S0-todo"]
    queue_items.sort(key=lambda i: i.get("created_at") or "")
    if queue_items:
        if args.json:
            print(json.dumps(queue_items[0], indent=2, ensure_ascii=False))
        else:
            print(f"[next] id={queue_items[0]['id']} stage={queue_items[0]['stage']}")
        return 0
    review_items = [i for i in items if i.get("stage") in ("S3-done", "S4-fix")]
    review_items.sort(key=lambda i: i.get("updated_at") or "")
    if review_items:
        if args.json:
            print(json.dumps(review_items[0], indent=2, ensure_ascii=False))
        else:
            print(f"[next] id={review_items[0]['id']} stage={review_items[0]['stage']}")
        return 0
    print("[next] nothing to do (no S0-todo and no S3-done/S4-fix items)")
    return 0


def cmd_advance(args) -> int:
    state_path = Path(args.state_path).expanduser()
    state = _load_state(state_path)
    item = state["items"].get(args.id)
    if item is None:
        raise NotFoundError(f"id not found: {args.id}")
    cur = item["stage"]
    nxt = args.to
    if nxt not in LEGAL_STAGES:
        raise StateError(f"unknown target stage '{nxt}' (allowed: {sorted(LEGAL_STAGES)})")
    if nxt not in TRANSITIONS.get(cur, set()):
        raise TransitionError(
            f"illegal transition: {cur} → {nxt} for id={args.id}. "
            f"Allowed from {cur}: {sorted(TRANSITIONS.get(cur, set()))}"
        )

    # Anti-fix-bleed guard: cap fix_count to DEFAULT_MAX_FIXES unless --force.
    if nxt == "S4-fix":
        item["fix_count"] = item.get("fix_count", 0) + 1
        if item["fix_count"] > DEFAULT_MAX_FIXES and not args.force:
            raise StateError(
                f"fix_count={item['fix_count']} > {DEFAULT_MAX_FIXES}; "
                f"refusing to push to S4-fix again. Use --force to override."
            )

    # Update history
    item["history"].append({
        "ts": _now(),
        "from": cur,
        "to": nxt,
        "reason": args.reason or "",
        "agent": item.get("agent"),
    })
    item["stage"] = nxt
    item["phase"] = STAGE_PHASE[nxt]
    item["updated_at"] = _now()
    state["items"][args.id] = item

    _atomic_write_json(state_path, state)
    _append_event(Path(args.events_path).expanduser(), {
        "ts": _now(),
        "event": "advance",
        "id": args.id,
        "from": cur,
        "to": nxt,
        "reason": args.reason or "",
    })

    print(f"[advance] {args.id}: {cur} → {nxt}")
    return 0


def cmd_run(args) -> int:
    """Patch QA result onto an item. Format: --qa-result '{"l1_block":0,...}'"""
    state_path = Path(args.state_path).expanduser()
    state = _load_state(state_path)
    item = state["items"].get(args.id)
    if item is None:
        raise NotFoundError(f"id not found: {args.id}")
    if item["stage"] != "S4-qa":
        raise StateError(
            f"id={args.id} is at stage={item['stage']}; "
            f"qa-result only valid in S4-qa. Advance to S4-qa first."
        )
    try:
        qa = json.loads(args.qa_result)
    except json.JSONDecodeError as e:
        raise StateError(f"--qa-result not valid JSON: {e}") from e
    item["qa"] = {
        **item.get("qa", {}),
        **qa,
        "last_run": _now(),
    }
    item["updated_at"] = _now()
    state["items"][args.id] = item
    _atomic_write_json(state_path, state)
    _append_event(Path(args.events_path).expanduser(), {
        "ts": _now(),
        "event": "qa-run",
        "id": args.id,
        "qa": item["qa"],
    })
    print(f"[run] {args.id}: qa patched, last_run={item['qa']['last_run']}")
    return 0


def cmd_check(args) -> int:
    """Verify that the item is ready for the next legal advance."""
    state = _load_state(Path(args.state_path).expanduser())
    item = state["items"].get(args.id)
    if item is None:
        raise NotFoundError(f"id not found: {args.id}")
    stage = item["stage"]
    qa = item.get("qa", {})
    issues: list[str] = []

    # Per-stage pre-conditions
    if stage == "S3-done":
        if not item.get("artifact_path"):
            issues.append("artifact_path is empty (writer didn't record where the draft lives)")
    elif stage == "S4-qa":
        if not item.get("artifact_path"):
            issues.append("artifact_path missing — S4-qa needs a draft to check")
    elif stage == "S4-ready":
        # All three BLOCK fields must be 0 (or null, but ready implies checked)
        for k in ("l1_block", "l2_block", "l7_block"):
            v = qa.get(k)
            if v is None:
                issues.append(f"qa.{k} is null — QA must report a number, even 0")
            elif isinstance(v, (int, float)) and v > 0:
                issues.append(f"qa.{k}={v} > 0 — fix before advancing to S5")
    elif stage == "S5-importing":
        if not qa.get("last_run"):
            issues.append("qa.last_run is null — never been QA'd")
        for k in ("l1_block", "l2_block", "l7_block"):
            v = qa.get(k)
            if v is None:
                issues.append(f"qa.{k} is null — must be 0 to import")
            elif isinstance(v, (int, float)) and v > 0:
                issues.append(f"qa.{k}={v} > 0 — must clear BLOCKs before S5 import")
    elif stage == "S5-published":
        if not item.get("publish", {}).get("sanity_id"):
            issues.append("publish.sanity_id is null — import didn't record a Sanity ID")
    elif stage in ("S4-fix",):
        if item.get("fix_count", 0) > DEFAULT_MAX_FIXES:
            issues.append(f"fix_count={item['fix_count']} > {DEFAULT_MAX_FIXES}; escalate")
    elif stage in ("done", "failed", "escalated"):
        issues = []  # terminal states pass by definition

    if issues:
        print(f"[check] FAIL — id={args.id} stage={stage}")
        for it in issues:
            print(f"  - {it}")
        return 1  # non-zero = not ready (hook signal)
    print(f"[check] OK — id={args.id} stage={stage}")
    return 0


def cmd_summary(args) -> int:
    state = _load_state(Path(args.state_path).expanduser())
    by_phase: dict[str, int] = {p: 0 for p in PHASES}
    by_stage: dict[str, int] = {}
    for it in state["items"].values():
        ph = it.get("phase", "QUEUE")
        by_phase[ph] = by_phase.get(ph, 0) + 1
        st = it.get("stage", "S0-todo")
        by_stage[st] = by_stage.get(st, 0) + 1
    total = sum(by_phase.values())
    print(f"[summary] total items: {total}")
    print(f"  by phase: " + ", ".join(f"{p}={by_phase[p]}" for p in PHASES))
    if by_stage:
        print(f"  by stage:")
        for st, n in sorted(by_stage.items()):
            print(f"    {st:<16} {n}")
    return 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _print_item_human(item: dict) -> None:
    print(f"id:           {item['id']}")
    print(f"stage:        {item['stage']}")
    print(f"phase:        {item['phase']}")
    print(f"category:     {item.get('category')}")
    print(f"target_type:  {item.get('target_type')}")
    print(f"agent:        {item.get('agent')}")
    print(f"skill:        {item.get('skill')}")
    print(f"artifact:     {item.get('artifact_path')}")
    print(f"fix_count:    {item.get('fix_count', 0)}")
    qa = item.get("qa", {})
    print(f"qa.l1_block:  {qa.get('l1_block')}")
    print(f"qa.l2_block:  {qa.get('l2_block')}")
    print(f"qa.l7_block:  {qa.get('l7_block')}")
    print(f"qa.last_run:  {qa.get('last_run')}")
    pub = item.get("publish", {})
    print(f"sanity_id:    {pub.get('sanity_id')}")
    print(f"created_at:   {item.get('created_at')}")
    print(f"updated_at:   {item.get('updated_at')}")
    hist = item.get("history") or []
    if hist:
        print(f"history ({len(hist)}):")
        for h in hist[-5:]:
            print(f"  - [{h.get('ts')}] {h.get('from')} → {h.get('to')} ({h.get('reason', '')})")


# ---------------------------------------------------------------------------
# Argparse
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pipeline_state.py",
        description="Lovart MFlow pipeline state machine (single source of truth)",
    )
    p.add_argument("--state-path", default=str(DEFAULT_STATE_FILE),
                   help=f"path to pipeline-state.json (default: {DEFAULT_STATE_FILE})")
    p.add_argument("--events-path", default=str(DEFAULT_EVENTS_FILE),
                   help=f"path to events.jsonl (default: {DEFAULT_EVENTS_FILE})")

    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create empty state file")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("upsert", help="create or update a pipeline item")
    s.add_argument("--id", required=True)
    s.add_argument("--category")
    s.add_argument("--target-type")
    s.add_argument("--artifact-path")
    s.add_argument("--agent")
    s.add_argument("--skill")
    s.set_defaults(func=cmd_upsert)

    s = sub.add_parser("get", help="show one item")
    s.add_argument("--id", required=True)
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_get)

    s = sub.add_parser("list", help="list items")
    s.add_argument("--phase")
    s.add_argument("--stage")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("next", help="suggest the next item to work on")
    s.add_argument("--phase")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_next)

    s = sub.add_parser("advance", help="move an item to a new stage")
    s.add_argument("--id", required=True)
    s.add_argument("--to", required=True, help=f"target stage (one of: {sorted(LEGAL_STAGES)})")
    s.add_argument("--reason", default="")
    s.add_argument("--force", action="store_true", help="override fix_count guard")
    s.set_defaults(func=cmd_advance)

    s = sub.add_parser("run", help="record QA result for an item in S4-qa")
    s.add_argument("--id", required=True)
    s.add_argument("--qa-result", required=True, help='JSON: {"l1_block":0,"l2_block":0,"l7_block":0}')
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("check", help="verify an item is ready for its next advance")
    s.add_argument("--id", required=True)
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("summary", help="dashboard counters")
    s.set_defaults(func=cmd_summary)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except StateError as e:
        print(f"[err] {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
