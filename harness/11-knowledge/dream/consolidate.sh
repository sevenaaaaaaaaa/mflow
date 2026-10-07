#!/usr/bin/env bash
# dream/consolidate.sh — night-time memory consolidation
#
# Pipeline:
#   1. Regenerate entities.jsonl + relationships.jsonl from YAML SSOT
#   2. Refresh tree.yaml header (version/generator fields)
#   3. Touch MEMORY-PROJECT.md + bump version if any entity changed
#   4. Emit a 7-day diff summary → audit/reports/dream-consolidate-{YYYY-MM-DD}.md
#   5. (Optional) pull rules from .claude/skills/ into .cursor/skills/ via sync-skills.sh
#   6. Reflect: scan sessions/*.md, extract recurring patterns, write weekly report
#
# Invocation:
#   bash dream/consolidate.sh                          # full run
#   bash dream/consolidate.sh --emit-only              # only JSONL refresh
#   bash dream/consolidate.sh --no-touch               # do NOT touch MEMORY-PROJECT.md
#   bash dream/consolidate.sh --audit-only             # only run audit.sh
#   bash dream/consolidate.sh --reflect-only           # only run reflect
#
# Logs:
#   audit/reports/dream-consolidate-{YYYY-MM-DD}.md
#   dream/recurring-patterns/{YYYY-WW}.md
#   ~/.hermes/logs/dream-consolidate.log  (cron side)
#
# Exit codes:
#   0 OK
#   1 audit mismatch (will NOT auto-fix; user must review)
#   2 hard error (python not found, broken YAML, etc.)

set -euo pipefail
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KNOWLEDGE_ROOT="$(cd "$SELF/.." && pwd)"
VAULT_ROOT="$(cd "$KNOWLEDGE_ROOT/../.." && pwd)"  # 1-Project/Lovart MFlow
TODAY="$(date +%F)"
LOG_DIR="$KNOWLEDGE_ROOT/audit/reports"
LOG_PREFIX="$SELF/.run-log"
LOG="$LOG_PREFIX.log"

mkdir -p "$LOG_DIR"

emit_only=0
no_touch=0
audit_only=0
reflect_only=0
for arg in "$@"; do
  case $arg in
    --emit-only)    emit_only=1 ;;
    --no-touch)     no_touch=1 ;;
    --audit-only)   audit_only=1 ;;
    --reflect-only) reflect_only=1 ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

acquire_lock() {
  LOOM_DREAM_LOCK="$SELF/.lock"
  if [ -e "$LOOM_DREAM_LOCK" ] && kill -0 "$(cat "$LOOM_DREAM_LOCK")" 2>/dev/null; then
    echo "consolidate.sh: another instance running (pid=$(cat "$LOOM_DREAM_LOCK"))" >&2
    exit 3
  fi
  echo $$ > "$LOOM_DREAM_LOCK"
  trap 'rm -f "$LOOM_DREAM_LOCK"' EXIT
}

acquire_lock

echo "[$(date +%FT%T)] consolidate.sh start (emit=$emit_only, audit=$audit_only)" >> "$LOG"

# ---- 1. JSONL refresh
if [ "$audit_only" -eq 0 ]; then
  if ! python3 "$KNOWLEDGE_ROOT/scripts/kg-emit-jsonl.py" >> "$LOG" 2>&1; then
    echo "consolidate.sh: kg-emit-jsonl failed" | tee -a "$LOG" >&2
    exit 2
  fi
  echo "[$(date +%FT%T)] JSONL refreshed" >> "$LOG"
fi

# ---- 2. Frontmatter check
if [ "$emit_only" -eq 0 ]; then
  python3 "$KNOWLEDGE_ROOT/scripts/fm-check.py" > "$LOG_DIR/fm-check-$TODAY.txt" 2>&1 || true
fi

# ---- 3. Touch MEMORY-PROJECT.md (only if entities.yaml mtime > MEMORY-PROJECT.md mtime)
if [ "$emit_only" -eq 0 ] && [ "$audit_only" -eq 0 ] && [ "$no_touch" -eq 0 ]; then
  if [ -f "$KNOWLEDGE_ROOT/entities.yaml" ] && \
     [ "$KNOWLEDGE_ROOT/entities.yaml" -nt "$KNOWLEDGE_ROOT/MEMORY-PROJECT.md" ]; then
    python3 - <<EOF >> "$LOG"
import datetime, pathlib
p = pathlib.Path("$KNOWLEDGE_ROOT/MEMORY-PROJECT.md")
text = p.read_text("utf-8")
# bump last_consolidated field
new_line = f"last_consolidated: {datetime.date.today().isoformat()}\n"
import re
text2 = re.sub(r"last_consolidated:\s*\d{4}-\d{2}-\d{2}", new_line.rstrip(), text, count=1)
if text2 == text and "last_consolidated" not in text:
    # insert after version:
    text2 = re.sub(r"(version:\s*\S+\n)", r"\1" + new_line, text, count=1)
p.write_text(text2, encoding="utf-8")
print("[consolidate] bumped MEMORY-PROJECT.md last_consolidated")
EOF
  fi
fi

# ---- 4. Hermes MEMORY.md sync (push MEMORY-PROJECT.md project slice)
if [ "$emit_only" -eq 0 ] && [ "$audit_only" -eq 0 ]; then
  echo "[$(date +%FT%T)] sync Hermes MEMORY.md" >> "$LOG"
  sync_rc=0
  python3 "$KNOWLEDGE_ROOT/scripts/sync-to-hermes-memory.py" --root "$VAULT_ROOT" >> "$LOG" 2>&1 || sync_rc=$?
  case $sync_rc in
    0)  echo "[$(date +%FT%T)] Hermes sync: facts written"          >> "$LOG" ;;
    2)  echo "[$(date +%FT%T)] Hermes sync: noop (already bridged)"  >> "$LOG" ;;
    *)  echo "[$(date +%FT%T)] Hermes sync: FAILED (USER.md not touched; will retry next cycle)" >> "$LOG" ;;
  esac
fi

# ---- 5. audit
if [ "$emit_only" -eq 0 ] && [ "$reflect_only" -eq 0 ]; then
  bash "$SELF/audit.sh" --no-write-today || rc=$?
  rc=${rc:-0}
  if [ "$rc" -ne 0 ]; then
    echo "[$(date +%FT%T)] audit reported issues (rc=$rc)" >> "$LOG"
    exit "$rc"
  fi
fi

# ---- 6. reflect (Layer 2: scan sessions/*.md, extract recurring patterns)
if [ "$emit_only" -eq 0 ] && [ "$audit_only" -eq 0 ]; then
  echo "[$(date +%FT%T)] reflect (Layer 2)" >> "$LOG"
  if python3 "$SELF/reflect.py" --root "$VAULT_ROOT" >> "$LOG" 2>&1; then
    echo "[$(date +%FT%T)] reflect done" >> "$LOG"
  else
    echo "[$(date +%FT%T)] reflect FAILED (continuing)" >> "$LOG"
  fi
fi

echo "[$(date +%FT%T)] consolidate.sh done" >> "$LOG"
echo "consolidate.sh: OK"
