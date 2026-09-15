#!/usr/bin/env python3
"""
orchestrate.py — Cascading quality loop engine (v0.2).

Loops between writer profile (lovart-creation) and critic profile (lovart-quality)
with budget control. Iterates until either:
  - critic returns BLOCK=0 → loop done, ready for human
  - max_iterations reached → escalate to lovart-management
  - crit fail (engine error) → escalate

Engine is profile-agnostic: dispatch is via dispatch-write.sh and
dispatch-eval.py, which are user-swappable. Default backend = "mock" for testing
without LLM API.

State machine:
  INIT  ──-> WRITE(v0)
  WRITE ──> EVAL(vN)
  EVAL  ──> BLOCK=0  ──> DONE(ready)
            BLOCK>0  ──> WRITE(v(N+1))   if N+1 < max_iterations
                       ESCALATE(budget)  else

Outputs:
  <persist_dir>/v0-draft.md .. vN-draft.md
  <persist_dir>/quality-report-vN.json
  <persist_dir>/loop-log.md   (human-readable)
  <persist_dir>/loop-meta.json (machine-readable)

Usage:
  # real run (with mock backend for testing; real LLM backend via OPENCODE_BIN env)
  python3 orchestrate.py \\
    --slug "smoke-test" \\
    --topic "how Lovart MFlow 11-knowledge works" \\
    --target-type blog \\
    --persist-dir "/tmp/cascade-smoke" \\
    --criteria 1-1\\ Harness/Skills/06-orchestrate/lovart-quality-cascade/criteria.yaml \\
    --backend mock

  # with real LLM backend (opt-in, default OFF)
  python3 orchestrate.py ... --backend hermes \\
    --hermes-bin ~/.hermes/bin/hermes-agent \\
    --writer-profile lovart-creation \\
    --critic-profile lovart-quality
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE
ROOT = HERE.parents[3]  # vault root (1-1 Harness/Skills/... -> vault)
CRITERIA_DEFAULT = SKILL_ROOT / "criteria.yaml"


def log_both(persist_dir: Path, msg: str):
    """Write to loop-log.md and stdout."""
    print(msg)
    log = persist_dir / "loop-log.md"
    with log.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")


def load_criteria(path: Path):
    import yaml
    return yaml.safe_load(path.read_text("utf-8"))


def write_meta(persist_dir: Path, meta: dict):
    (persist_dir / "loop-meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def dispatch_write(args_criteria: dict, brief: dict, prev_reasons, backend: str, profile: str) -> str:
    """Call writer (deepseek via hermes or mock backend) and return draft text."""
    if backend == "mock":
        return mock_write(args_criteria, brief, prev_reasons)
    elif backend == "hermes":
        return hermes_write(args_criteria, brief, prev_reasons, profile)
    elif backend == "opencode":
        return opencode_write(args_criteria, brief, prev_reasons, profile)
    raise ValueError(f"unknown backend: {backend}")


def dispatch_eval(args_criteria: dict, draft_text: str, backend: str, profile: str) -> dict:
    """Run preflight + criteria evaluator against text. Return quality-report dict."""
    if backend == "mock":
        return mock_eval(draft_text, args_criteria)
    elif backend in ("hermes", "opencode"):
        return hermes_eval(draft_text, args_criteria, profile)
    raise ValueError(f"unknown backend: {backend}")


# ---- mock backends (dev-only: deterministic, no LLM call) ----

MOCK_WRITES = [
    # iter 0: deliberately bad (contains 3 AI-flavor patterns + a tiny table)
    # iter 1: medium (1 AI-flavor)
    # iter 2: clean (0 patterns)
    """值得的是—"Lo变现" 是 海南AI的设计品牌。

| Col1 | Col2 |
| --- | --- |
| A | B |
| C | D |

下面我们看一下 lovart-vs-mujjo-2026-07 这篇博客应当怎么写。
""",
    """Lovart MFlow 的 11-knowledge 是项目内知识库根目录。

使用 `lovart-cascade` 的 orchestrator 让 writer/critic 双代理迭代。
""",
    """Lovart 11-knowledge 是项目级 SSOT。它由 KNOWLEDGE-TREE.md、entities.yaml、relationships.yaml、KG 查询 CLI 三部分构成。dream 周期 + audit 是它的后台整理机制。
""",
    """Lovart 11-knowledge 是项目级 SSOT。它由 KNOWLEDGE-TREE.md、entities.yaml、relationships.yaml、KG 查询 CLI 三部分构成。dream 周期 + audit 是它的后台整理机制。

writer 改进时携带 critic 的结构化 reasons；critic 不读前 N 稿，避免重复踩同一坑。
""",
]


def mock_write(criteria, brief, prev_reasons):
    iter_idx = int(brief.get("_iter", 0))
    if iter_idx >= len(MOCK_WRITES):
        return MOCK_WRITES[-1]  # plateau
    text = MOCK_WRITES[iter_idx]
    return text


def mock_eval(text: str, criteria: dict) -> dict:
    """Implements block_if / warn_if pattern-based evaluator. Deterministic."""
    import re
    block_hits = []
    warn_hits = []

    for rule in (criteria.get("block_if") or []):
        if rule.get("pattern"):
            hits = list(re.finditer(rule["pattern"], text, re.MULTILINE))
            if rule.get("threshold") and len(hits) >= rule["threshold"]:
                for hit in hits[:3]:  # cap log noise
                    block_hits.append({
                        "rule_id": rule["id"],
                        "span": [hit.start(), hit.end()],
                        "matched": hit.group(0)[:80],
                    })
                if len(hits) > 3:
                    block_hits.append({
                        "rule_id": rule["id"],
                        "note": f"+{len(hits)-3} more matches truncated",
                    })
        # table-row rule: count, then threshold
        if rule["id"] == "table-row":
            nlines = sum(1 for l in text.splitlines() if re.match(rule["pattern"], l))
            if nlines > rule["threshold"]:
                block_hits.append({
                    "rule_id": "table-row",
                    "note": f"{nlines} table rows > threshold {rule['threshold']}",
                })

    for rule in (criteria.get("warn_if") or []):
        block_hits_cnt = len(block_hits)
        warn_hits.append({
            "rule_id": rule.get("id"),
            "triggered": False,
            "note": "evaluator stub",
        })

    BLOCK = len(block_hits) > 0
    return {
        "evaluator": "mock",
        "criteria_version": criteria.get("criteria_version", "0.1"),
        "block_count": len(block_hits),
        "warn_count": len(warn_hits),
        "BLOCK": BLOCK,
        "block_hits": block_hits,
        "warn_hits": warn_hits,
        "evaluated_at": datetime.datetime.now().isoformat(),
        "raw_chars": len(text),
        "raw_lines": len(text.splitlines()),
    }


# ---- real backends (require LLM; not exercised by smoke test) ----

def hermes_write(criteria, brief, prev_reasons, profile):
    hermes_bin = os.environ.get("HERMES_BIN", str(Path.home() / ".hermes/bin/hermes-agent"))
    parts = []
    parts.append(f"# brief\n{json.dumps(brief, indent=2, ensure_ascii=False)}")
    if prev_reasons:
        parts.append("# reasons_from_critic\n" + json.dumps(prev_reasons, indent=2, ensure_ascii=False))
    parts.append("# criteria (must avoid block_if patterns)\n" + json.dumps(criteria.get("block_if", []), indent=2, ensure_ascii=False))
    prompt = "\n\n".join(parts)
    cmd = [hermes_bin, "-p", profile, "write", "--stdin"]
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=criteria.get("iter_timeout_s", 600))
    if proc.returncode != 0:
        raise RuntimeError(f"hermes write failed: {proc.stderr[:200]}")
    return proc.stdout


def hermes_eval(text, criteria, profile):
    cmd = [os.environ.get("HERMES_BIN", str(Path.home() / ".hermes/bin/hermes-agent")),
           "-p", profile, "evaluate", "--stdin"]
    proc = subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=criteria.get("iter_timeout_s", 300))
    if proc.returncode != 0:
        raise RuntimeError(f"hermes eval failed: {proc.stderr[:200]}")
    return json.loads(proc.stdout)


def opencode_write(criteria, brief, prev_reasons, profile):
    raise NotImplementedError("opencode backend: wire to OpenCode custom command; out of v0.2 scope, planned v0.3")


# ---- main loop engine ----

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--target-type", default="blog", choices=["blog", "landing-page"])
    p.add_argument("--persist-dir", required=True)
    p.add_argument("--criteria", default=str(CRITERIA_DEFAULT))
    p.add_argument("--max-iterations", type=int, default=None,
                   help="override criteria.yaml max_iterations")
    p.add_argument("--backend", choices=["mock", "hermes", "opencode"], default="mock")
    p.add_argument("--writer-profile", default="lovart-creation")
    p.add_argument("--critic-profile", default="lovart-quality")
    p.add_argument("--hermes-bin", default=str(Path.home() / ".hermes/bin/hermes-agent"))
    args = p.parse_args()

    criteria = load_criteria(Path(args.criteria))
    if args.max_iterations is not None:
        criteria["max_iterations"] = args.max_iterations

    persist = Path(args.persist_dir).expanduser()
    persist.mkdir(parents=True, exist_ok=True)
    log_both(persist, f"cascade start • slug={args.slug} • backend={args.backend} • max_iter={criteria['max_iterations']}")

    brief = {
        "slug": args.slug,
        "topic": args.topic,
        "target_type": args.target_type,
    }

    meta = {
        "slug": args.slug,
        "topic": args.topic,
        "target_type": args.target_type,
        "backend": args.backend,
        "criteria_version": criteria.get("criteria_version", "?"),
        "criteria_path": args.criteria,
        "started_at": datetime.datetime.now().isoformat(),
        "iterations": [],
    }
    write_meta(persist, meta)

    last_reasons = None
    state = "INIT"
    rc = 1  # default = ESCALATE

    for i in range(criteria["max_iterations"]):
        # WRITE
        brief["_iter"] = i
        state = "WRITE"
        log_both(persist, f"[iter {i}] state WRITE")
        t0 = time.time()
        try:
            draft = dispatch_write(criteria, brief, last_reasons, args.backend, args.writer_profile)
        except Exception as e:
            log_both(persist, f"[iter {i}] WRITE ERROR: {e}")
            rc = 3  # engine error
            break
        (persist / f"v{i}-draft.md").write_text(draft, encoding="utf-8")
        write_dt = time.time() - t0
        log_both(persist, f"[iter {i}] wrote {len(draft)} chars to v{i}-draft.md in {write_dt:.1f}s")

        # EVAL
        state = "EVAL"
        log_both(persist, f"[iter {i}] state EVAL")
        t0 = time.time()
        try:
            report = dispatch_eval(criteria, draft, args.backend, args.critic_profile)
        except Exception as e:
            log_both(persist, f"[iter {i}] EVAL ERROR: {e}")
            rc = 3
            break
        (persist / f"quality-report-v{i}.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        eval_dt = time.time() - t0
        log_both(persist, f"[iter {i}] eval in {eval_dt:.1f}s: BLOCK={report.get('BLOCK')} block_count={report.get('block_count')}")

        meta["iterations"].append({
            "iter": i,
            "draft_chars": len(draft),
            "write_dt_s": round(write_dt, 2),
            "eval_dt_s": round(eval_dt, 2),
            "BLOCK": report.get("BLOCK"),
            "block_count": report.get("block_count"),
            "warn_count": report.get("warn_count"),
            "block_hits": report.get("block_hits"),
        })
        write_meta(persist, meta)

        if not report.get("BLOCK"):
            state = "DONE"
            log_both(persist, f"[iter {i}] READY — no BLOCK; loop done")
            rc = 0
            break

        last_reasons = report.get("block_hits") or []
        log_both(persist, f"[iter {i}] fail with {len(last_reasons)} reasons; carrying to next iter")

    if state not in ("DONE",):
        if rc == 1:
            log_both(persist, f"loop budget exhausted ({criteria['max_iterations']} iter); ESCALATE")
            rc = 2
        # engine error path: rc already set

    meta["final_state"] = state
    meta["return_code"] = rc
    meta["ended_at"] = datetime.datetime.now().isoformat()
    write_meta(persist, meta)

    log_both(persist, f"cascade end • rc={rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
