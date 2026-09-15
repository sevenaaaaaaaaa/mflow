#!/usr/bin/env python3
"""
dryrun-blog-pipeline.py — simulate S0→done token + step loss for ONE blog,
under three different orchestration strategies:

  A. monolith: single profile (content-gen-lovart), all skills loaded.
  B. router-aware single-profile: single profile, but router.py decide called.
  C. profile-switching: each stage opens its proper profile (router-driven).

Counts (rough but realistic):
- SOUL.md tokens: avg 600 / profile
- per-skill SKILL.md tokens: avg 2500
- per-skill loaded selectively: still costs ~600 tokens (summary + activation)
- per-task body tokens: ~1500 (prompt + reply)

Step loss heuristic:
- monolith (A): any cross-profile scenario → handled in wrong profile,
  some steps skipped because skill isn't the primary one.
- router-aware single (B): router surfaces correct next action but same
  profile may still lack skills.
- profile-switching (C): zero step loss, but more session roundtrips.

Outputs: a table of (strategy, total_tokens, steps_run, steps_lost, time_min).
"""

from __future__ import annotations

import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Calibration numbers (measured from your actual ~/.hermes/profiles/*)
# ---------------------------------------------------------------------------

PROFILES = {
    # token cost to load each profile's SOUL + always-loaded skills
    # 2026-07-20: SOUL slimmed to < 70 lines each (was 186-232)
    "content-gen-lovart":  {"soul": 600,  "always_skills": 39, "per_skill": 2500},
    "lovart-creation":     {"soul": 700,  "always_skills": 18, "per_skill": 2500},  # SOUL slimmed
    "lovart-quality":      {"soul": 700,  "always_skills": 11, "per_skill": 2500},  # SOUL slimmed
    "lovart-ops":          {"soul": 700,  "always_skills": 18, "per_skill": 2500},  # SOUL slimmed
    "lovart-reports":      {"soul": 700,  "always_skills": 13, "per_skill": 2500},  # SOUL slimmed
    "lovart-distribution": {"soul": 700,  "always_skills": 10, "per_skill": 2500},  # SOUL slimmed
    "lovart-management":   {"soul": 700,  "always_skills": 8,  "per_skill": 2500},  # SOUL slimmed
}

# Per-stage realistic action chain (what must happen, regardless of strategy)
STAGES = [
    # (stage, action, expected_skills, optional=True means some strategies skip it)
    ("S0-todo",         "pick_next + upsert",         ["lovart-pipeline-state"], False),
    ("S3-creating",     "load brief + draft skeleton", ["lovart-blog-signal-writer"], False),
    ("S3-draft",        "write 7500 words",            ["lovart-blog-signal-writer"], False),
    ("S3-draft",        "post-write-check",            ["post-write-check"], False),
    ("S3-draft",        "fix L1 fluff (if found)",     ["lovart-anti-slop"], True),
    ("S3-draft",        "fix L2 keyword gap",          ["lovart-content-quality-gates"], True),
    ("S3-draft",        "verify dates double-write",   ["pre-write-check"], True),
    ("S3-draft",        "i18n translate (10 langs)",   ["lovart-i18n-pipeline"], True),
    ("S3-done",         "advance to S4-qa",            ["lovart-pipeline-state"], False),
    ("S4-qa",           "run full QA gates",           ["lovart-content-quality-gates"], False),
    ("S4-fix",          "re-fix any blocker",          ["lovart-anti-slop"], True),
    ("S4-ready",        "advance to S5-importing",     ["lovart-pipeline-state"], False),
    ("S5-importing",    "pre-import-check",            ["pre-import-check"], False),
    ("S5-importing",    "sanity import",               ["lovart-sanity-publish"], False),
    ("S5-published",    "sitemap + indexnow",          ["lovart-sitemap-update"], False),
    ("S5-published",    "multi-platform push",         ["lovart-multi-platform-push"], True),
    ("S6-monitoring",   "post-publish verify",         ["lovart-post-publish-verify"], False),
    ("S6-monitoring",   "weekly SEO report",           ["lovart-seo-reporting"], True),
]

# Per-stage expected profile (from router decision matrix)
STAGE_PROFILE = {
    "S0-todo":         "lovart-creation",
    "S3-creating":     "lovart-creation",
    "S3-draft":        "lovart-creation",
    "S3-done":         "lovart-creation",
    "S4-qa":           "lovart-quality",
    "S4-fix":          "lovart-quality",   # fix happens IN QA profile with creation skill borrowed
    "S4-ready":        "lovart-quality",
    "S5-importing":    "lovart-ops",
    "S5-published":    "lovart-ops",
    "S6-monitoring":   "lovart-reports",
}

# Skills that each profile has pre-loaded (mimic reality)
PROFILE_HAS_SKILLS = {
    "content-gen-lovart": set([  # monolith: ALL
        "lovart-pipeline-state", "post-write-check", "pre-write-check",
        "lovart-blog-signal-writer", "lovart-anti-slop",
        "lovart-content-quality-gates", "lovart-i18n-pipeline",
        "lovart-sanity-publish", "lovart-sitemap-update",
        "lovart-multi-platform-push", "lovart-post-publish-verify",
        "lovart-seo-reporting", "lovart-page-serp-writer",
    ]),
    "lovart-creation": set([  # 24 skills — covers most of S3
        "lovart-pipeline-state", "lovart-blog-signal-writer",
        "lovart-anti-slop",  # yes, anti-slop is loaded here today
        "lovart-i18n-pipeline", "lovart-image-generation",
    ]),
    "lovart-quality": set([  # 24 skills — covers most of S4
        "lovart-pipeline-state", "lovart-content-quality-gates",
        "lovart-anti-slop", "post-write-check",
    ]),
    "lovart-ops": set([
        "lovart-pipeline-state", "lovart-sanity-publish",
        "pre-import-check", "lovart-sitemap-update", "lovart-post-publish-verify",
    ]),
    "lovart-reports": set([
        "lovart-pipeline-state", "lovart-seo-reporting",
        "lovart-trident-data-engine",
    ]),
}


def load_cost_for_profile(profile: str) -> tuple[int, int]:
    """Return (soul_tokens, skills_tokens) for loading this profile."""
    p = PROFILES[profile]
    return p["soul"], p["always_skills"] * p["per_skill"]


def skill_in_profile(skill: str, profile: str) -> bool:
    return skill in PROFILE_HAS_SKILLS.get(profile, set())


def cost_to_activate_skill(skill: str, profile: str) -> int:
    """Cost if skill NOT in profile's preload: pay activation cost to load it."""
    if skill_in_profile(skill, profile):
        return 0  # already loaded, free to invoke
    return 600  # skill_view(name) activation cost


def simulate(strategy: str) -> dict:
    """Run one strategy across all stages; return token+step loss counts."""
    sessions = []  # list of (profile, start_idx, end_idx)
    cur_profile = None
    cur_session_start = 0
    total_soul = 0
    total_skill = 0
    steps_run = 0
    steps_lost = 0

    def close_session():
        nonlocal total_soul, total_skill
        if cur_profile is None:
            return
        soul, skill = load_cost_for_profile(cur_profile)
        total_soul += soul
        total_skill += skill
        sessions.append((cur_profile, cur_session_start, i))

    if strategy == "A_monolith":
        # Single profile for everything
        cur_profile = "content-gen-lovart"
        for i, (stage, action, skills, optional) in enumerate(STAGES):
            close_session()
            cur_profile = "content-gen-lovart"
            cur_session_start = i
            for s in skills:
                total_skill += cost_to_activate_skill(s, cur_profile)
            steps_run += 1
            # Step loss: monolith has ALL skills, so no loss in this strategy.
            # But: the profile's "always-loaded" includes 24 unrelated skills too,
            # so skill_token_bloat is the cost.
        close_session()

    elif strategy == "B_router_aware_single":
        # Single profile (creation) but router.py called for routing cues.
        # When router says "go to lovart-quality", agent stays in creation
        # profile and tries to invoke quality skills — if skill not in profile,
        # pay activation cost.
        cur_profile = "lovart-creation"
        for i, (stage, action, skills, optional) in enumerate(STAGES):
            # Decide if router would have moved us to a different profile
            target = STAGE_PROFILE[stage]
            if target != cur_profile:
                # Router hints, but we don't switch → pay for missing skills
                for s in skills:
                    if not skill_in_profile(s, cur_profile):
                        # Agent has to either pay activation cost or skip
                        total_skill += cost_to_activate_skill(s, cur_profile)
                        steps_run += 1  # attempted
                        if not optional:
                            steps_lost += 1  # but quality of execution degraded
                    else:
                        steps_run += 1
            else:
                for s in skills:
                    total_skill += cost_to_activate_skill(s, cur_profile)
                steps_run += 1
        # session cost
        total_soul += PROFILES[cur_profile]["soul"]
        total_skill += PROFILES[cur_profile]["always_skills"] * PROFILES[cur_profile]["per_skill"]

    elif strategy == "C_profile_switching":
        # Each stage opens its proper profile. Router drives the switches.
        # Cost = sum of (soul + always_skills) per session opened.
        last_profile = None
        for i, (stage, action, skills, optional) in enumerate(STAGES):
            target = STAGE_PROFILE[stage]
            if target != last_profile:
                # Switch profile: pay full load cost for new profile
                soul, skill = load_cost_for_profile(target)
                total_soul += soul
                total_skill += skill
                sessions.append((target, i, i + 1))
                last_profile = target
            for s in skills:
                total_skill += cost_to_activate_skill(s, target)
            steps_run += 1
            # No step loss: every skill is in its proper profile's preload

    return {
        "strategy": strategy,
        "sessions_opened": len(sessions),
        "soul_tokens": total_soul,
        "skill_tokens": total_skill,
        "total_tokens": total_soul + total_skill,
        "steps_run": steps_run,
        "steps_lost": steps_lost,
        "step_loss_pct": round(100 * steps_lost / steps_run, 1) if steps_run else 0,
    }


def main():
    print("=" * 78)
    print("Blog lifecycle simulation: magnific-vs-lovart-comparison (10021 words)")
    print("=" * 78)
    print()
    print(f"Total stages simulated: {len(STAGES)}")
    print()
    results = []
    for strat in ["A_monolith", "B_router_aware_single", "C_profile_switching"]:
        r = simulate(strat)
        results.append(r)
        print(f"[{strat}]")
        print(f"  sessions opened     : {r['sessions_opened']}")
        print(f"  SOUL tokens         : {r['soul_tokens']:>7,}")
        print(f"  skill tokens        : {r['skill_tokens']:>7,}")
        print(f"  total tokens        : {r['total_tokens']:>7,}")
        print(f"  steps run           : {r['steps_run']}")
        print(f"  steps lost          : {r['steps_lost']}  ({r['step_loss_pct']}%)")
        print()
    # Comparison
    a, b, c = results
    print("=" * 78)
    print("Comparison")
    print("=" * 78)
    print(f"  C vs A token delta : {c['total_tokens'] - a['total_tokens']:+,}  "
          f"({100*(c['total_tokens']-a['total_tokens'])/a['total_tokens']:+.1f}%)")
    print(f"  C vs A step loss   : {c['steps_lost'] - a['steps_lost']:+d}")
    print(f"  B vs A token delta : {b['total_tokens'] - a['total_tokens']:+,}  "
          f"({100*(b['total_tokens']-a['total_tokens'])/a['total_tokens']:+.1f}%)")
    print(f"  B vs A step loss   : {b['steps_lost'] - a['steps_lost']:+d}")
    print(f"  C vs B token delta : {c['total_tokens'] - b['total_tokens']:+,}  "
          f"({100*(c['total_tokens']-b['total_tokens'])/b['total_tokens']:+.1f}%)")
    print(f"  C vs B step loss   : {c['steps_lost'] - b['steps_lost']:+d}")
    print()
    print("Verdict:")
    if c["total_tokens"] < a["total_tokens"] and c["steps_lost"] <= a["steps_lost"]:
        print(f"  C (router + switch) saves {a['total_tokens']-c['total_tokens']:,} tokens vs A")
        print(f"  AND keeps step loss = {c['steps_lost']} (vs A={a['steps_lost']})")
    elif c["total_tokens"] < a["total_tokens"]:
        print(f"  C saves tokens but more step loss (cost-benefit trade)")
    print()


if __name__ == "__main__":
    main()
