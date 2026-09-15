#!/usr/bin/env bash
# smoketest.sh — verify orchestrate.py state machine + criteria evaluator end-to-end.
#
# Run from anywhere; uses /tmp/cascade-smoke by default.
#
# Expected outcome (mock backend):
#   - state machine: WRITE → EVAL → WRITE → EVAL → DONE in ≤3 iter
#   - evaluator: catches AI-flavor keywords + table-row count, BLOCK≥threshold
#   - artifacts: v{0..N}-draft.md + quality-report-v{0..N}.json + loop-log.md + loop-meta.json

set -euo pipefail

VAULT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
SKILL="$VAULT/1-1 Harness/Skills/06-orchestrate/lovart-quality-cascade"
TD="${CASCADE_SMOKE_DIR:-/tmp/cascade-smoke-$$}"
rm -rf "$TD" && mkdir -p "$TD"
echo "==[smoke] start. td=$TD"

run_case() {
  local slug="$1"
  local topic="$2"
  python3 "$SKILL/orchestrate.py" \
    --slug "$slug" \
    --topic "$topic" \
    --target-type blog \
    --persist-dir "$TD/$slug" \
    --backend mock
}

echo ""
echo "--- case 1: should reach READY in ≤3 iterations (mock text improves per iter)"
set +e
run_case "smoke-pass" "11-knowledge overview" > "$TD/case1.log" 2>&1
rc1=$?
set -e
echo "rc1=$rc1"

echo ""
echo "--- case 2: max-iterations=1 forces ESCALATE (no improvement room)"
set +e
python3 "$SKILL/orchestrate.py" \
  --slug "smoke-escalate" \
  --topic "any topic" \
  --target-type blog \
  --persist-dir "$TD/smoke-escalate" \
  --max-iterations 1 \
  --backend mock > "$TD/case2.log" 2>&1
rc2=$?
set -e
echo "rc2=$rc2 (expect 2 = ESCALATE)"

echo ""
echo "=== summary ==="
TD="$TD" python3 - <<'PY'
import json, os, pathlib
T = pathlib.Path(os.environ["TD"])
expected_rc_pass = 0
expected_rc_escalate = 2
results = {}
for s in ["smoke-pass", "smoke-escalate"]:
    p = T / s / "loop-meta.json"
    if not p.exists():
        print(f"  [fail] {s}: no meta")
        results[s] = "MISSING"
        continue
    d = json.loads(p.read_text("utf-8"))
    iters = d['iterations']
    print(f"  [{s}] rc={d['return_code']} state={d['final_state']} iters={len(iters)}")
    for i in iters:
        print(f"    v{i['iter']}: BLOCK={i['BLOCK']} blocks={i['block_count']} dt_w/i={i['write_dt_s']}/{i['eval_dt_s']}s")
    if s == "smoke-pass":
        results[s] = "OK" if d['return_code'] == expected_rc_pass and d['final_state'] == "DONE" else "WRONG_RC"
    else:
        results[s] = "OK" if d['return_code'] == expected_rc_escalate else "WRONG_RC"
print()
verdict = "PASS" if all(v == "OK" for v in results.values()) else "FAIL"
print("VERDICT:", verdict, results)
PY
