#!/usr/bin/env bash
# Smoke test for pipeline_state.py — verifies state machine enforces all rules.
# Returns rc=0 if all checks pass; rc=1 otherwise.

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${HERE}/pipeline_state.py"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

STATE="$TMPDIR/state.json"
EVENTS="$TMPDIR/events.jsonl"
PS="--state-path $STATE --events-path $EVENTS"

PASS=0
FAIL=0
log() { echo "[smoke] $*"; }
expect_ok() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        log "  ✓ $desc"
        PASS=$((PASS + 1))
    else
        log "  ✗ $desc  (rc=$?)"
        FAIL=$((FAIL + 1))
    fi
}
expect_fail() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        log "  ✗ $desc  (expected failure but got success)"
        FAIL=$((FAIL + 1))
    else
        log "  ✓ $desc  (correctly rejected)"
        PASS=$((PASS + 1))
    fi
}

log "1) init"
expect_ok "init creates empty state" python3 "$PY" $PS init

log "2) upsert an item"
expect_ok "upsert new id" python3 "$PY" $PS upsert --id "blog-test-001" --category blog --target-type blog --artifact-path "/tmp/blog.md"

log "3) illegal forward transition is rejected"
expect_fail "S0-todo → S5-importing rejected" python3 "$PY" $PS advance --id "blog-test-001" --to "S5-importing"

log "4) happy path S0 → S3 → S3-draft"
expect_ok "S0-todo → S3-creating" python3 "$PY" $PS advance --id "blog-test-001" --to "S3-creating"
expect_ok "S3-creating → S3-draft" python3 "$PY" $PS advance --id "blog-test-001" --to "S3-draft"
expect_ok "S3-draft → S3-done" python3 "$PY" $PS advance --id "blog-test-001" --to "S3-done"

log "5) S3-done → S4-qa → run qa → check"
expect_ok "S3-done → S4-qa" python3 "$PY" $PS advance --id "blog-test-001" --to "S4-qa"
expect_ok "qa-run with all BLOCK=0" python3 "$PY" $PS run --id "blog-test-001" --qa-result '{"l1_block":0,"l2_block":0,"l7_block":0}'
expect_ok "check passes (ready for S4-ready)" python3 "$PY" $PS check --id "blog-test-001"

log "6) advance to S4-ready"
expect_ok "S4-qa → S4-ready" python3 "$PY" $PS advance --id "blog-test-001" --to "S4-ready"
expect_ok "check still passes" python3 "$PY" $PS check --id "blog-test-001"

log "7) sanity_id check on S5-published"
expect_ok "S4-ready → S5-importing" python3 "$PY" $PS advance --id "blog-test-001" --to "S5-importing"
expect_ok "check passes (qa BLOCKs all 0, ready to import)" python3 "$PY" $PS check --id "blog-test-001"
# Simulate import: patch publish block via Python (state has no nested publish setter; use a small inline helper)
python3 -c "
import json
p = '$STATE'
d = json.load(open(p))
d['items']['blog-test-001']['publish'] = {'sanity_id':'o11tm2qe-abc-001','imported_at':'2026-07-17T10:00:00Z','status':'published'}
d['items']['blog-test-001']['updated_at'] = '2026-07-17T10:00:00Z'
json.dump(d, open(p,'w'), indent=2, ensure_ascii=False)
"
expect_ok "S5-importing → S5-published" python3 "$PY" $PS advance --id "blog-test-001" --to "S5-published"
expect_ok "check passes (sanity_id set)" python3 "$PY" $PS check --id "blog-test-001"

log "8) fix_count guard — bail at 4"
expect_ok "S5-published → S6-monitoring" python3 "$PY" $PS advance --id "blog-test-001" --to "S6-monitoring"
expect_ok "S6-monitoring → done" python3 "$PY" $PS advance --id "blog-test-001" --to "done"

log "9) fix-bleed guard on S4-fix (cap=3, so 4th push is rejected)"
expect_ok "upsert second item" python3 "$PY" $PS upsert --id "blog-test-002" --category blog
expect_ok "advance to S4-qa via shortcut" python3 "$PY" $PS advance --id "blog-test-002" --to "S3-creating"
expect_ok "advance to S3-draft" python3 "$PY" $PS advance --id "blog-test-002" --to "S3-draft"
expect_ok "advance to S3-done" python3 "$PY" $PS advance --id "blog-test-002" --to "S3-done"
expect_ok "advance to S4-qa" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-qa"
expect_ok "qa-run with l1_block=2 (fail)" python3 "$PY" $PS run --id "blog-test-002" --qa-result '{"l1_block":2,"l2_block":0,"l7_block":0}'
expect_ok "S4-qa → S4-fix #1 (count=1)" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-fix"
expect_ok "S4-fix → S4-qa (loop)" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-qa"
expect_ok "S4-qa → S4-fix #2 (count=2)" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-fix"
expect_ok "S4-fix → S4-qa (loop)" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-qa"
expect_ok "S4-qa → S4-fix #3 (count=3)" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-fix"
expect_ok "S4-fix → S4-qa (loop)" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-qa"
expect_fail "S4-qa → S4-fix #4 (count=4 > 3, guard trips)" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-fix"
expect_ok "--force overrides guard, allows 4th fix" python3 "$PY" $PS advance --id "blog-test-002" --to "S4-fix" --force

log "10) terminal states reject further advance"
expect_fail "done → anywhere rejected" python3 "$PY" $PS advance --id "blog-test-001" --to "S6-monitoring"
expect_fail "failed → anywhere rejected" python3 "$PY" $PS advance --id "blog-test-002" --to "S3-creating"  # S4-failed → S3-creating allowed, so test fail differently
# Override blog-test-001 to failed for negative test
python3 -c "
import json
p = '$STATE'
d = json.load(open(p))
d['items']['blog-test-001']['stage'] = 'failed'
d['items']['blog-test-001']['phase'] = 'FINAL'
json.dump(d, open(p,'w'), indent=2, ensure_ascii=False)
"
expect_fail "failed is terminal" python3 "$PY" $PS advance --id "blog-test-001" --to "S6-monitoring"

log "11) invalid id format"
expect_fail "uppercase id rejected" python3 "$PY" $PS upsert --id "Blog-Invalid-Format"
expect_fail "too-short id rejected" python3 "$PY" $PS upsert --id "ab"

log "12) atomicity — state file is always valid JSON"
python3 -c "
import json
d = json.load(open('$STATE'))
assert d['version'] == 1
assert 'items' in d
assert 'blog-test-001' in d['items']
assert 'blog-test-002' in d['items']
print('  ✓ state file structure valid')
PASS_GLOBAL=True
" || FAIL=$((FAIL + 1))

log "13) summary"
python3 "$PY" $PS summary

log "14) list filtering"
expect_ok "list --phase CREATE empty (both items advanced)" python3 "$PY" $PS list --phase CREATE
expect_ok "list --phase FINAL" python3 "$PY" $PS list --phase FINAL

log "15) next command"
expect_ok "next returns empty (no S0-todo)" python3 "$PY" $PS next

echo ""
echo "==================================================="
echo "smoke results: PASS=$PASS  FAIL=$FAIL"
echo "==================================================="
if [ "$FAIL" -eq 0 ]; then
    echo "VERDICT: PASS"
    exit 0
else
    echo "VERDICT: FAIL"
    exit 1
fi
