#!/usr/bin/env bash
# Smoke test for lovart-router — verifies decision matrix + scenario detection.
# Returns rc=0 only if all checks pass.

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
ROUTER="$(cd "$HERE/.." && pwd)/router.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0
log() { echo "[smoke] $*"; }
expect_ok() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        log "  ✓ $desc"
        PASS=$((PASS + 1))
    else
        log "  ✗ $desc"
        FAIL=$((FAIL + 1))
    fi
}
expect_fail() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        log "  ✗ $desc  (expected failure)"
        FAIL=$((FAIL + 1))
    else
        log "  ✓ $desc"
        PASS=$((PASS + 1))
    fi
}
expect_eq() {
    local desc="$1" expected="$2" actual="$3"
    if [[ "$actual" == "$expected" ]]; then
        log "  ✓ $desc  (=$actual)"
        PASS=$((PASS + 1))
    else
        log "  ✗ $desc  expected=$expected actual=$actual"
        FAIL=$((FAIL + 1))
    fi
}

# Set up a real pipeline-state with items at various stages
STATE="$TMP/state.json"
EVENTS="$TMP/events.jsonl"
PS="$(cd "$HERE/../../lovart-pipeline-state" && pwd)/pipeline_state.py"
PS_ARGS=(--state-path "$STATE" --events-path "$EVENTS")
python3 "$PS" "${PS_ARGS[@]}" init >/dev/null

# Add 5 items at different stages
for id in item-s0 item-s3-creating item-s3-draft item-s4-fix item-s5-importing; do
    python3 "$PS" "${PS_ARGS[@]}" upsert --id "$id" --category blog --target-type blog >/dev/null
done
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s3-creating --to S3-creating >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s3-draft --to S3-creating >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s3-draft --to S3-draft >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s4-fix --to S3-creating >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s4-fix --to S3-draft >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s4-fix --to S3-done >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s4-fix --to S4-qa >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s4-fix --to S4-fix >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s5-importing --to S3-creating >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s5-importing --to S3-draft >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s5-importing --to S3-done >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s5-importing --to S4-qa >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s5-importing --to S4-ready >/dev/null
python3 "$PS" "${PS_ARGS[@]}" advance --id item-s5-importing --to S5-importing >/dev/null

ROUTER_ARGS=(--state-path "$STATE")

log "1) validate"
expect_ok "validate passes on clean decision table" python3 "$ROUTER" validate

log "2) profiles listed"
out=$(python3 "$ROUTER" profiles 2>&1)
n=$(echo "$out" | grep -c "^  lovart-")
expect_eq "exactly 6 profiles" "6" "$n"

log "3) decide picks S0-todo first"
out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "S0-todo → lovart-creation" "lovart-creation" "$target"

log "4) decide --id routes by stage"
out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s3-creating 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "S3-creating → lovart-creation" "lovart-creation" "$target"

out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s3-draft 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "S3-draft (default) → lovart-creation" "lovart-creation" "$target"

out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s4-fix 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "S4-fix → lovart-creation (back to write)" "lovart-creation" "$target"

out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s5-importing 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "S5-importing → lovart-ops" "lovart-ops" "$target"

log "5) decide --from-context detects scenarios"
# L1 fluff → lovart-quality
out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s3-draft --from-context "L1 fluff in section 3" 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "l1_fluff context → lovart-quality" "lovart-quality" "$target"

# preflight fail → lovart-quality
out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s5-importing --from-context "preflight failed BLOCK != 0" 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "preflight_fail context → lovart-quality" "lovart-quality" "$target"

# sanity_id_exists → lovart-ops
out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s5-importing --from-context "sanity_id already exists, can't import" 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "sanity_id_exists context → lovart-ops" "lovart-ops" "$target"

# i18n translation → stays in creation
out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s3-draft --from-context "need to translate to 10 languages" 2>&1)
target=$(echo "$out" | grep "→ profile:" | awk '{print $NF}')
expect_eq "i18n_translation context → lovart-creation" "lovart-creation" "$target"

log "6) decide --json has expected keys"
out=$(python3 "$ROUTER" "${ROUTER_ARGS[@]}" decide --id item-s3-draft --json 2>&1)
keys=$(echo "$out" | python3 -c "import sys,json; d=json.load(sys.stdin); print(' '.join(sorted(d.keys())))")
expect_eq "json has all expected keys" "decision id next_step_verb profile_target reason scenario skills_to_load stage" "$keys"

log "7) matrix has 23 decisions"
out=$(python3 "$ROUTER" matrix 2>&1)
n=$(echo "$out" | tail -n +4 | grep -v "^----" | grep -v "^\[matrix" | wc -l | tr -d ' ')
expect_eq "matrix shows 23 decisions" "23" "$n"

log "8) bad profile name rejected"
expect_fail "profile unknown_name rejected" python3 "$ROUTER" profile unknown_name

log "9) decide with missing state file AND no --id returns 2"
expect_fail "missing state, no --id → exit 2" python3 "$ROUTER" --state-path /nonexistent/state.json decide

echo ""
echo "==================================================="
echo "smoke results: PASS=$PASS  FAIL=$FAIL"
echo "==================================================="
[[ "$FAIL" -eq 0 ]] && echo "VERDICT: PASS" || echo "VERDICT: FAIL"
exit "$FAIL"
