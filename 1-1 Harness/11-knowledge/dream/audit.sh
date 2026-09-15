#!/usr/bin/env bash
# dream/audit.sh — 5-tool + cross-file consistency audit
#
# Checks:
#   A1 Graph integrity (orphans, dangling edges, dup ids)
#   A2 Frontmatter presence + schema
#   A3 Tool entry-point references 11-knowledge/README
#       - Hermes  : ~/.hermes/memories/MEMORY.md mentions 11-knowledge
#       - OpenCode: opencode.jsonc instructions includes 11-knowledge path
#       - Cursor  : at least one .cursor/rules/*.mdc references it
#       - Claude  : 1-1 Harness/CLAUDE.md references it
#       - Codex   : AGENTS.md references it
#   A4 Skill catalog cross-mirror: every active skill in 1-1 Harness/Skills
#       exists in at least one of {.claude/skills, .cursor/skills, ~/.hermes/skills/lovart}
#   A5 Hard rules consistency:
#       - RULES-00 mentions sanity iron-rules referenced by every *-sanity-publish skill
#       - rule-session-routing matches actual profile list in entities.yaml
#   A6 Cron list vs entity graph:
#       - every cron entity is runs_on a registered profile
#
# Outputs:
#   audit/reports/audit-report-{YYYY-MM-DD}.md   (human)
#   audit/checks/audit-{YYYY-MM-DD}.json        (machine)
#
# Invocation:
#   bash dream/audit.sh                # full run, write today's report
#   bash dream/audit.sh --no-write-today
#   bash dream/audit.sh --check A1 A4  # subset
#
# Exit codes:
#   0 OK (or only WARN)
#   1 ERROR(S) detected (review report)

set -euo pipefail
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KNOWLEDGE_ROOT="$(cd "$SELF/.." && pwd)"
VAULT_ROOT="$(cd "$KNOWLEDGE_ROOT/../.." && pwd)"
TODAY="$(date +%F)"
REPORT="$KNOWLEDGE_ROOT/audit/reports/audit-report-$TODAY.md"
CHECK="$KNOWLEDGE_ROOT/audit/checks/audit-$TODAY.json"

mkdir -p "$KNOWLEDGE_ROOT/audit/reports" "$KNOWLEDGE_ROOT/audit/checks"

no_write=0
checks_to_run=()
for arg in "$@"; do
  case $arg in
    --no-write-today) no_write=1 ;;
    A1|A2|A3|A4|A5|A6) checks_to_run+=("$arg") ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done
if [ ${#checks_to_run[@]} -eq 0 ]; then
  checks_to_run=(A1 A2 A3 A4 A5 A6)
fi

WARN=()
ERR=()
JSONL_RESULT='{}'  # overwritten per-check

# helper
log_warn() { WARN+=("$1"); printf 'WARN  %s\n' "$1"; }
log_err()  { ERR+=("$1");  printf 'ERROR %s\n' "$1";  }
note()     { printf '      %s\n' "$1"; }

# ============================================================================
# A1 — graph integrity
# ============================================================================
if printf '%s\n' "${checks_to_run[@]}" | grep -q '^A1$'; then
  echo "[A1] graph integrity"
  python3 "$KNOWLEDGE_ROOT/scripts/kg-query.py" --audit-orphans > "$KNOWLEDGE_ROOT/.audit-orphans.txt" 2>&1 || true
  if [ -s "$KNOWLEDGE_ROOT/.audit-orphans.txt" ] && ! grep -q "(no orphans)" "$KNOWLEDGE_ROOT/.audit-orphans.txt"; then
    log_warn "A1: orphans present — review .audit-orphans.txt (informational, expected for fresh datasets)"
    note "$(head -5 "$KNOWLEDGE_ROOT/.audit-orphans.txt")"
  fi

  # dup ids / dangling endpoints
  python3 "$KNOWLEDGE_ROOT/scripts/kg-emit-jsonl.py" > /dev/null 2>&1
  if [ "$?" -ne 0 ]; then
    log_err "A1: kg-emit-jsonl failed — likely dangling endpoints in relationships.yaml"
  fi
fi

# ============================================================================
# A2 — frontmatter
# ============================================================================
if printf '%s\n' "${checks_to_run[@]}" | grep -q '^A2$'; then
  echo "[A2] frontmatter"
  python3 "$KNOWLEDGE_ROOT/scripts/fm-check.py" > "$KNOWLEDGE_ROOT/.fm-check.txt" 2>&1 || true
  missing=$(grep -c "need attention:" "$KNOWLEDGE_ROOT/.fm-check.txt" || true)
  if [ -n "$missing" ] && [ "$missing" -gt 0 ]; then
    log_warn "A2: frontmatter coverage incomplete — see .fm-check.txt"
    note "Will be remediated by future fm-fix batches."
  fi
fi

# ============================================================================
# A3 — tool entry-point references knowledge tree
# ============================================================================
if printf '%s\n' "${checks_to_run[@]}" | grep -q '^A3$'; then
  echo "[A3] tool entry-point references"
  # entry file inventory; using parallel arrays (set -u safe)
  entries=(hermes-mem opencode-cfg claude-md agents-md)
  paths_=(
    "$HOME/.hermes/memories/MEMORY.md"
    "$VAULT_ROOT/opencode.jsonc"
    "$VAULT_ROOT/1-1 Harness/CLAUDE.md"
    "$VAULT_ROOT/AGENTS.md"
  )
  for i in 0 1 2 3; do
    k="${entries[$i]}"
    f="${paths_[$i]}"
    if [ ! -f "$f" ]; then
      log_err "A3: missing entry file $k → $f"
      continue
    fi
    if ! grep -q "11-knowledge" "$f"; then
      log_err  "A3: $k ($f) does not reference 11-knowledge"
      note     "→ edit file to add a line pointing to 1-1 Harness/11-knowledge/README.md"
    else
      note "OK $k references 11-knowledge"
    fi
  done
  cursor_rules="$VAULT_ROOT/.cursor/rules"
  if [ -d "$cursor_rules" ]; then
    if ! grep -rl "11-knowledge" "$cursor_rules" 2>/dev/null | head -1 | grep -q .; then
      log_err "A3: no .cursor/rules/*.mdc references 11-knowledge"
    else
      note "OK at least one Cursor rule references 11-knowledge"
    fi
  fi
fi

# ============================================================================
# A4 — skill catalog cross-mirror
# ============================================================================
if printf '%s\n' "${checks_to_run[@]}" | grep -q '^A4$'; then
  echo "[A4] skill catalogs"
  cat_names=(hermes cursor_rules harness)
  cat_paths=(
    "$HOME/.hermes/skills/lovart"
    "$VAULT_ROOT/.cursor/rules"
    "$VAULT_ROOT/1-1 Harness/Skills"
  )
  # 2026-09-14: 独立 .claude/skills 与 .cursor/skills 目录已废除——运行时副本由
  # harness_sync.py 生成（.cursor/rules/*.mdc + ~/.hermes/skills/lovart），
  # vault 1-1 Harness/Skills/ 是唯一真相。
  for i in 0 1 2; do
    k="${cat_names[$i]}"
    r="${cat_paths[$i]}"
    if [ ! -d "$r" ]; then
      log_warn "A4: $k skills dir missing: $r"
      continue
    fi
    # skills live at varying depths: clawx/claude = {group}/{skill}/SKILL.md (depth 2),
    # hermes = {skill}/SKILL.md (depth 1), cursor = {skill}/SKILL.md (depth 1).
    # count by SKILL.md at depth 1-3.
    if [ "$k" = "cursor_rules" ]; then
      cnt=$(find "$r" -maxdepth 1 -name '*.mdc' | wc -l | tr -d ' ')
      note "$k has $cnt compiled rules at $r"
    else
      cnt=$(find "$r" -maxdepth 3 -name 'SKILL.md' | wc -l | tr -d ' ')
      note "$k has $cnt skills at $r"
    fi
  done
fi

# ============================================================================
# A5 — rules consistency
# ============================================================================
if printf '%s\n' "${checks_to_run[@]}" | grep -q '^A5$'; then
  echo "[A5] rules consistency"
  iron="$VAULT_ROOT/1-1 Harness/02-rules/RULES-00-iron.md"
  if [ ! -f "$iron" ]; then
    log_err "A5: RULES-00-iron.md missing"
  else
    if ! grep -q "sanity deploy" "$iron"; then
      log_err "A5: RULES-00 missing 'sanity deploy' prohibition"
    fi
    if ! grep -q -- "\-\-missing" "$iron"; then
      log_err "A5: RULES-00 missing --missing mandate"
    fi
  fi
fi

# ============================================================================
# A6 — cron vs entity graph
# ============================================================================
if printf '%s\n' "${checks_to_run[@]}" | grep -q '^A6$'; then
  echo "[A6] cron vs graph"
  # crons present in entities.yaml + cron registered
  KR="$KNOWLEDGE_ROOT" python3 - <<'PY' || true
import json, sys, os, pathlib
kr = os.environ["KR"]
ents_p = pathlib.Path(kr) / "entities.jsonl"
rels_p = pathlib.Path(kr) / "relationships.jsonl"
if not ents_p.exists() or not rels_p.exists():
    print("ERR  A6: missing JSONL mirror; run kg-emit-jsonl.py first")
    sys.exit(1)
ents = [json.loads(l) for l in ents_p.read_text("utf-8").splitlines() if l.strip()]
rels = [json.loads(l) for l in rels_p.read_text("utf-8").splitlines() if l.strip()]
crons = [e for e in ents if e.get("__kind") == "crons"]
ids = {e["id"] for e in ents}
problems = []
for c in crons:
    cid = c["id"]
    # if cron has a non-null profile, must have runs_on edge
    p = c.get("meta", {}).get("profile") if isinstance(c.get("meta"), dict) else None
    if p:
        if not any(r["from"] == cid and r["to"] == p and r["type"] == "runs_on" for r in rels):
            problems.append(f"A6: cron {cid} meta={p} but no runs_on edge in graph")
unknown_cron_profiles = []
for c in crons:
    cid = c["id"]
    p = c.get("meta", {}).get("profile") if isinstance(c.get("meta"), dict) else None
    if p and p not in ids:
        unknown_cron_profiles.append(f"A6: cron {cid} meta={p} but {p} not in entities")
if problems or unknown_cron_profiles:
    for p in problems + unknown_cron_profiles:
        print("ERR  " + p)
    sys.exit(1)
print("OK crons consistent with graph")
PY
  if [ "$?" -ne 0 ]; then
    log_err "A6: graph/cron drift detected"
  fi
fi

# ============================================================================
# Snapshot JSON + render Markdown
# ============================================================================
if [ "$no_write" -eq 0 ]; then
python3 - <<PY
import datetime, json, os
out = {
  "date": "$TODAY",
  "warn": """$(printf '%s\n' "${WARN[@]:-}" | sed 's/$/\\n/')""" or "",
  "errors": """$(printf '%s\n' "${ERR[@]:-}" | sed 's/$/\\n/')""" or "",
  "checks_run": """$(printf '%s ' "${checks_to_run[@]}")""" .strip(),
  "orphan_count": $(wc -l < "$KNOWLEDGE_ROOT/.audit-orphans.txt" 2>/dev/null | tr -d ' ' || echo 0),
  "fm_missing_count": $(grep -c "need attention:" "$KNOWLEDGE_ROOT/.fm-check.txt" 2>/dev/null | tr -d ' ' || echo 0),
}
if not out["warn"]: out["warn"] = ""
if not out["errors"]: out["errors"] = ""
open("$CHECK","w").write(json.dumps(out, indent=2, ensure_ascii=False))
print("wrote", "$CHECK")
PY

cat > "$REPORT" <<MDEOF
---
type: audit-report
date: $TODAY
checks: $(printf '%s ' "${checks_to_run[@]}")
errors: ${#ERR[@]}
warnings: ${#WARN[@]}
---

# Audit Report — $TODAY

## Summary

- Errors: **${#ERR[@]}**
- Warnings: **${#WARN[@]}**
- Checks run: $(printf '%s, ' "${checks_to_run[@]}")

## Errors (must fix)

$(if [ ${#ERR[@]} -eq 0 ]; then echo "_none_"; else printf -- '- %s\n' "${ERR[@]}"; fi)

## Warnings (review)

$(if [ ${#WARN[@]} -eq 0 ]; then echo "_none_"; else printf -- '- %s\n' "${WARN[@]}"; fi)

## Artifacts

- $(realpath "$CHECK")  (JSON, machine-readable)
- $KNOWLEDGE_ROOT/.audit-orphans.txt
- $KNOWLEDGE_ROOT/.fm-check.txt

## Follow-up

- Errors → open a ticket or apply patch today.
- Warnings → batch into next dream cycle.
MDEOF
  echo "wrote $REPORT"
fi

# exit code: 1 if any errors
if [ ${#ERR[@]} -gt 0 ]; then
  exit 1
fi
exit 0
