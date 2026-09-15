#!/usr/bin/env python3
"""
lovart-router — state-aware profile router for Lovart content factory.

Problem:
    6+ Profile × 13+ cross-profile scenarios × N skills per profile = context
    bloat. Agents either (a) load every potentially-relevant skill (high token)
    or (b) miss critical steps when scenarios cross profile boundaries
    (e.g., QA bug discovered in creation profile).

Solution:
    Single decision table mapping (state, scenario) → (action, profile_target,
    skills_to_load). Every profile's first action is `lovart-router decide`
    which returns ONE precise next step.

Usage:
    # In any profile, at session start:
    python3 lovart-router/router.py decide [--state-path ...]

    # When bug discovered mid-session:
    python3 lovart-router/router.py decide --from-context "qa_l1_fluff"

    # List all decisions and which profile handles them:
    python3 lovart-router/router.py matrix
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PIPELINE_STATE_PY = HERE.parent / "lovart-pipeline-state" / "pipeline_state.py"


# ---------------------------------------------------------------------------
# Profile registry — only 8 active profiles. Add to this map to onboard new
# workflow lines; don't bloat existing profiles.
# ---------------------------------------------------------------------------

PROFILES = {
    "lovart-reports": {
        "model": "deepseek-chat",
        "work_line": "S1-data + S6-monitor",
        "owns_stages": ["S0-todo"],
        "key_skills": ["lovart-trident-data-engine", "lovart-sentinel",
                       "lovart-data-ingestion", "lovart-seo-reporting"],
        "token_budget_hint": 4500,
    },
    "lovart-creation": {
        "model": "deepseek-v4-pro",
        "work_line": "S3-content-production",
        "owns_stages": ["S3-creating", "S3-draft", "S3-done"],
        "key_skills": ["lovart-blog-signal-writer", "lovart-page-serp-writer",
                       "lovart-landing-page", "lovart-image-generation",
                       "lovart-i18n-pipeline"],
        "token_budget_hint": 4500,
    },
    "lovart-quality": {
        "model": "deepseek-chat",
        "work_line": "S4-review",
        "owns_stages": ["S4-qa", "S4-fix", "S4-ready"],
        "key_skills": ["lovart-content-quality-gates", "lovart-anti-slop",
                       "lovart-content-audit", "post-write-check"],
        "token_budget_hint": 3500,
    },
    "lovart-ops": {
        "model": "deepseek-chat",
        "work_line": "S5-publish",
        "owns_stages": ["S5-importing", "S5-published", "S6-monitoring"],
        "key_skills": ["lovart-sanity-publish", "lovart-sitemap-update",
                       "pre-import-check"],
        "token_budget_hint": 3500,
    },
    "lovart-distribution": {
        "model": "deepseek-chat",
        "work_line": "S5b-distribute",
        "owns_stages": [],  # distribution doesn't own a stage; operates on
                            # already-published items.
        "key_skills": ["lovart-multi-platform-push",
                       "lovart-content-distribution"],
        "token_budget_hint": 3500,
    },
    "lovart-management": {
        "model": "deepseek-chat",
        "work_line": "M0-meta",
        "owns_stages": [],
        "key_skills": ["lovart-pipeline-state", "lovart-router",
                       "lovart-project-architecture", "lovart-knowledge-graph-query"],
        "token_budget_hint": 4000,
    },
}


# ---------------------------------------------------------------------------
# Decision table — single source of routing truth.
# Format: (stage, scenario_key) → {action, profile, skills, reason}
# If stage matches but scenario is unknown → fall back to stage-only match.
# If neither matches → defaults to management (meta).
# ---------------------------------------------------------------------------

DECISIONS: list[dict[str, Any]] = [
    # ---- S0-todo: pick up new work ----
    {
        "stage": "S0-todo", "scenario": "default",
        "action": "upsert",
        "profile": "lovart-creation",
        "skills": ["lovart-pipeline-state", "lovart-blog-signal-writer"],
        "reason": "S0-todo → first creation step",
    },
    {
        "stage": "S0-todo", "scenario": "from_sentinel",
        "action": "upsert",
        "profile": "lovart-creation",
        "skills": ["lovart-pipeline-state", "lovart-blog-signal-writer"],
        "reason": "Sentinel-triggered creation",
    },

    # ---- S3 stages: creation work ----
    {
        "stage": "S3-creating", "scenario": "default",
        "action": "execute_skill",
        "profile": "lovart-creation",
        "skills": ["lovart-blog-signal-writer"],
        "reason": "Writing in progress",
    },
    {
        "stage": "S3-draft", "scenario": "default",
        "action": "run_hook_and_advance",
        "profile": "lovart-creation",
        "skills": ["post-write-check"],
        "reason": "Draft exists → run post-write-check before advancing to S3-done",
    },
    {
        "stage": "S3-draft", "scenario": "l1_fluff",
        "action": "reroute",
        "profile": "lovart-quality",
        "skills": ["lovart-anti-slop"],
        "reason": "L1 fluff → quality profile specializes in slop detection",
    },
    {
        "stage": "S3-draft", "scenario": "word_count_low",
        "action": "execute_skill",
        "profile": "lovart-creation",
        "skills": ["lovart-blog-signal-writer"],
        "reason": "Word count short → keep creation profile, extend draft",
    },
    {
        "stage": "S3-draft", "scenario": "missing_dates",
        "action": "patch_artifact",
        "profile": "lovart-creation",
        "skills": ["pre-write-check"],
        "reason": "Missing frontmatter dates → fix in same profile",
    },
    {
        "stage": "S3-draft", "scenario": "i18n_translation_needed",
        "action": "execute_skill",
        "profile": "lovart-creation",
        "skills": ["lovart-i18n-pipeline"],
        "reason": "Translation → stay in creation profile (i18n is a sub-mode)",
    },
    {
        "stage": "S3-done", "scenario": "default",
        "action": "advance_only",
        "profile": "lovart-creation",
        "skills": ["lovart-pipeline-state"],
        "reason": "S3 done → advance to S4-qa and close session",
    },

    # ---- S4 stages: QA work ----
    {
        "stage": "S4-qa", "scenario": "default",
        "action": "execute_skill",
        "profile": "lovart-quality",
        "skills": ["lovart-content-quality-gates"],
        "reason": "QA in progress",
    },
    {
        "stage": "S4-fix", "scenario": "default",
        "action": "reroute",
        "profile": "lovart-creation",
        "skills": ["lovart-blog-signal-writer"],
        "reason": "Fix → back to creation profile to edit artifact",
    },
    {
        "stage": "S4-fix", "scenario": "i18n_audit_fail",
        "action": "reroute",
        "profile": "lovart-creation",
        "skills": ["lovart-i18n-pipeline"],
        "reason": "i18n audit fail → creation profile (i18n sub-mode)",
    },
    {
        "stage": "S4-ready", "scenario": "default",
        "action": "advance_only",
        "profile": "lovart-quality",
        "skills": ["lovart-pipeline-state"],
        "reason": "QA done → close session; ops profile will pick up next",
    },

    # ---- S5 stages: publishing ----
    {
        "stage": "S5-importing", "scenario": "default",
        "action": "execute_skill",
        "profile": "lovart-ops",
        "skills": ["lovart-sanity-publish", "pre-import-check"],
        "reason": "Importing to Sanity",
    },
    {
        "stage": "S5-importing", "scenario": "preflight_fail",
        "action": "reroute",
        "profile": "lovart-quality",
        "skills": ["lovart-content-quality-gates"],
        "reason": "pre-import-check BLOCK → quality profile to fix BLOCKs",
    },
    {
        "stage": "S5-importing", "scenario": "sanity_id_exists",
        "action": "execute_skill",
        "profile": "lovart-ops",
        "skills": ["lovart-sanity-publish"],
        "reason": "Sanity ID exists → use patch (not --replace)",
    },
    {
        "stage": "S5-published", "scenario": "default",
        "action": "execute_skill",
        "profile": "lovart-ops",
        "skills": ["lovart-sitemap-update", "lovart-post-publish-verify"],
        "reason": "Notify engines + verify",
    },
    {
        "stage": "S5-published", "scenario": "needs_distribution",
        "action": "reroute",
        "profile": "lovart-distribution",
        "skills": ["lovart-multi-platform-push"],
        "reason": "Distribution needed for newly published item",
    },
    {
        "stage": "S6-monitoring", "scenario": "default",
        "action": "execute_skill",
        "profile": "lovart-reports",
        "skills": ["lovart-seo-reporting"],
        "reason": "Monitoring data lives in reports profile",
    },
    {
        "stage": "S6-monitoring", "scenario": "ranking_drop",
        "action": "execute_skill",
        "profile": "lovart-creation",
        "skills": ["lovart-existing-page-rewriting"],
        "reason": "Ranking drop → rewrite existing page (creation sub-mode)",
    },

    # ---- Cross-cutting queries (any stage) ----
    {
        "stage": "ANY", "scenario": "user_asks_state",
        "action": "info_only",
        "profile": None,  # use current profile
        "skills": ["lovart-pipeline-state"],
        "reason": "State query → use pipeline-state CLI directly",
    },
    {
        "stage": "ANY", "scenario": "user_asks_skill_list",
        "action": "info_only",
        "profile": None,
        "skills": [],
        "reason": "Skill list → just describe; no skill needed",
    },
    {
        "stage": "ANY", "scenario": "calendar_oversubscribed",
        "action": "reroute",
        "profile": "lovart-management",
        "skills": ["lovart-content-calendar"],
        "reason": "Calendar conflict → management escalates",
    },
]


# ---------------------------------------------------------------------------
# Decision engine
# ---------------------------------------------------------------------------

def _load_pipeline_state(state_path: str) -> dict[str, Any] | None:
    """Read pipeline-state.json (using the other skill's CLI to stay SSOT)."""
    if not os.path.exists(state_path):
        return None
    try:
        return json.loads(Path(state_path).read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _suggest_next_item(state: dict[str, Any]) -> dict[str, Any] | None:
    """Pick first S0-todo or first S3-done (highest priority)."""
    items = list(state.get("items", {}).values())
    queue = sorted(
        [i for i in items if i.get("stage") == "S0-todo"],
        key=lambda i: i.get("created_at") or "",
    )
    if queue:
        return queue[0]
    review = sorted(
        [i for i in items if i.get("stage") in ("S3-done", "S4-fix")],
        key=lambda i: i.get("updated_at") or "",
    )
    if review:
        return review[0]
    return None


def _match_decision(stage: str, scenario: str) -> dict[str, Any] | None:
    """Find decision by (stage, scenario) → fall back to (stage, default)."""
    for d in DECISIONS:
        if d["stage"] == stage and d["scenario"] == scenario:
            return d
    for d in DECISIONS:
        if d["stage"] == stage and d["scenario"] == "default":
            return d
    for d in DECISIONS:
        if d["stage"] == "ANY" and d["scenario"] == scenario:
            return d
    for d in DECISIONS:
        if d["stage"] == "ANY" and d["scenario"] == "default":
            return d
    return None


def _detect_scenario(args_text: str | None, item: dict[str, Any] | None) -> str:
    """Heuristic: detect scenario from --from-context text or qa block."""
    if not args_text:
        return "default"
    t = args_text.lower()
    if any(k in t for k in ("fluff", "slop", "marketing")):
        return "l1_fluff"
    if any(k in t for k in ("word", "length", "short")):
        return "word_count_low"
    if any(k in t for k in ("date", "releasedate", "publishedat")):
        return "missing_dates"
    if any(k in t for k in ("i18n", "translate", "translation", "lang")):
        return "i18n_translation_needed"
    if any(k in t for k in ("preflight", "pre-import", "block")):
        return "preflight_fail"
    if any(k in t for k in ("exists", "duplicate", "sanity id")):
        return "sanity_id_exists"
    if any(k in t for k in ("rank", "drop", "decline")):
        return "ranking_drop"
    if any(k in t for k in ("distribut", "publish elsewhere", "platform")):
        return "needs_distribution"
    if any(k in t for k in ("state", "where", "status")):
        return "user_asks_state"
    if any(k in t for k in ("calendar", "oversub", "schedule conflict")):
        return "calendar_oversubscribed"
    return "default"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_decide(args) -> int:
    """The single most important command: 'what should I do right now?'"""
    state_path = args.state_path
    state = _load_pipeline_state(state_path)
    if state is None and not args.id:
        print("[err] state file not found and --id not given", file=sys.stderr)
        return 2

    # Resolve target item: explicit --id, or auto-suggest from state
    item = None
    if args.id:
        item = state["items"].get(args.id) if state else None
    if item is None:
        item = _suggest_next_item(state or {"items": {}})

    if item is None:
        print("[decide] no items in queue and no --id given")
        return 0

    scenario = _detect_scenario(args.from_context, item)
    decision = _match_decision(item["stage"], scenario)
    if decision is None:
        print(f"[decide] no decision for stage={item['stage']} scenario={scenario}")
        return 1

    out = {
        "id": item["id"],
        "stage": item["stage"],
        "scenario": scenario,
        "decision": decision,
        "profile_target": decision["profile"],
        "skills_to_load": decision["skills"],
        "next_step_verb": decision["action"],
        "reason": decision["reason"],
    }

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    elif args.brief:
        # Machine-friendly: 3 lines, no decoration — ideal for cron / script pipes
        print(f"profile={decision['profile']}")
        print(f"action={decision['action']}")
        print(f"skills={','.join(decision['skills'])}")
    else:
        print(f"[decide] id={item['id']}  stage={item['stage']}  scenario={scenario}")
        print(f"  → profile: {decision['profile']}")
        print(f"  → action:  {decision['action']}")
        print(f"  → skills:  {', '.join(decision['skills']) or '(none)'}")
        print(f"  → reason:  {decision['reason']}")

    return 0


def cmd_matrix(args) -> int:
    """Print the entire decision table."""
    print(f"[matrix] {len(DECISIONS)} decisions, {len(PROFILES)} profiles")
    print()
    print(f"{'stage':<16} {'scenario':<28} {'profile':<22} {'action':<24}")
    print("-" * 92)
    for d in DECISIONS:
        print(f"{d['stage']:<16} {d['scenario']:<28} {(d['profile'] or 'current'):<22} {d['action']:<24}")
    return 0


def cmd_profile(args) -> int:
    """Print profile details."""
    p = PROFILES.get(args.name)
    if p is None:
        print(f"[err] unknown profile: {args.name}", file=sys.stderr)
        print(f"      known: {', '.join(sorted(PROFILES))}")
        return 1
    if args.json:
        print(json.dumps(p, indent=2, ensure_ascii=False))
    else:
        print(f"[profile] {args.name}")
        for k, v in p.items():
            print(f"  {k}: {v}")
    return 0


def cmd_validate(args) -> int:
    """Validate decision table: no orphan stages, no bad profile refs."""
    errors = []
    stages_seen = set()
    for d in DECISIONS:
        stages_seen.add(d["stage"])
        if d["profile"] and d["profile"] not in PROFILES:
            errors.append(f"decision stage={d['stage']} scenario={d['scenario']} "
                          f"references unknown profile: {d['profile']}")
        if d["action"] not in ("execute_skill", "reroute", "advance_only",
                                "upsert", "patch_artifact", "info_only",
                                "run_hook_and_advance"):
            errors.append(f"unknown action '{d['action']}' in "
                          f"stage={d['stage']} scenario={d['scenario']}")
    legal_stages = {"S0-todo", "S3-creating", "S3-draft", "S3-done",
                    "S4-qa", "S4-fix", "S4-ready",
                    "S5-importing", "S5-published", "S6-monitoring",
                    "ANY"}
    bad_stages = stages_seen - legal_stages
    if bad_stages:
        errors.append(f"unknown stages in decisions: {bad_stages}")

    if errors:
        for e in errors:
            print(f"  ✗ {e}")
        print(f"\nFAIL ({len(errors)} errors)")
        return 1
    print(f"OK — {len(DECISIONS)} decisions across {len(stages_seen)} stages, "
          f"{len(PROFILES)} profiles")
    return 0


def cmd_list_profiles(args) -> int:
    print(f"[profiles] {len(PROFILES)} active")
    for name, p in PROFILES.items():
        print(f"  {name:<22} ({p['work_line']:<22})  skills: {len(p['key_skills'])}")
    return 0


# ---------------------------------------------------------------------------
# Argparse
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="router.py",
        description="Lovart state-aware profile router",
    )
    p.add_argument("--state-path", default="1-3 GenFlow/.pipeline/pipeline-state.json")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("decide", help="decide next step for current state")
    s.add_argument("--id")
    s.add_argument("--from-context", help="free-text description of current bug/scenario")
    s.add_argument("--json", action="store_true")
    s.add_argument("--brief", action="store_true", help="compact key=value output for cron/pipes")
    s.set_defaults(func=cmd_decide)

    s = sub.add_parser("matrix", help="print decision table")
    s.set_defaults(func=cmd_matrix)

    s = sub.add_parser("profile", help="print profile details")
    s.add_argument("name")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_profile)

    s = sub.add_parser("profiles", help="list all profiles")
    s.set_defaults(func=cmd_list_profiles)

    s = sub.add_parser("validate", help="validate decision table integrity")
    s.set_defaults(func=cmd_validate)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
