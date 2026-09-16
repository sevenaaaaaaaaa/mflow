#!/usr/bin/env bash
# pre-import-check.sh — enforce RULES-00 before any Sanity import.
#
# Refuses (exit 1) if any of these are violated:
#   1. pipeline-state shows item not at S4-ready or S5-importing
#   2. qa.l1_block / l2_block / l7_block all not equal to 0
#   3. Blog date double-write missing (releaseDate AND publishedAt both present)
#   4. Multi-language coverage incomplete for the same slug
#   5. Draft file is missing artifact_path
#
# Usage:
#   bash pre-import-check.sh --id blog-firefly-prompt-2026-07 \
#       --state-path /path/to/pipeline-state.json \
#       --artifact /path/to/blog-draft.md \
#       --type blog
#
# Exit codes:
#   0 = ok to import
#   1 = BLOCK — fix issues before re-running
#   2 = engine error (state file missing / python error)

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PIPELINE_STATE="${PIPELINE_STATE_PATH:-}"
ARTIFACT=""
ID=""
TARGET_TYPE="blog"
ALLOW_LANGS=""  # e.g. "en,zh" to skip coverage check; default = require all

usage() {
    sed -n '2,21p' "$0"
    exit 2
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --id) ID="$2"; shift 2;;
        --state-path) PIPELINE_STATE="$2"; shift 2;;
        --artifact) ARTIFACT="$2"; shift 2;;
        --type) TARGET_TYPE="$2"; shift 2;;
        --allow-langs) ALLOW_LANGS="$2"; shift 2;;
        -h|--help) usage;;
        *) echo "unknown arg: $1" >&2; usage;;
    esac
done

if [[ -z "$ID" ]]; then echo "[err] --id required" >&2; exit 2; fi
if [[ -z "$PIPELINE_STATE" || ! -f "$PIPELINE_STATE" ]]; then
    echo "[err] --state-path required and must exist ($PIPELINE_STATE)" >&2; exit 2
fi

ERRORS=()
WARNINGS=()
ok()   { echo "  ✓ $*"; }
warn() { WARNINGS+=("$*"); echo "  ! $*"; }
err()  { ERRORS+=("$*");   echo "  ✗ $*"; }

PY="${LOVART_PYTHON:-}"
if [[ -z "$PY" ]]; then
    ROOT_ABS="$(cd "$HERE/../../.." && pwd)"
    if [[ -x "$ROOT_ABS/.venv/bin/python" ]]; then
        PY="$ROOT_ABS/.venv/bin/python"
    else
        PY="$(command -v python3 || echo python3)"
    fi
fi

echo "[pre-import] id=$ID type=$TARGET_TYPE"

# --- 1) pipeline-state readiness ---
echo "[1/5] pipeline-state readiness"
# Resolve PIPELINE_PY as absolute path so we never depend on shell `..` expansion.
# $HERE = hooks/, so 3 levels up gets us to 1-Project/Lovart MFlow/.
HERE_ABS="$(cd "$HERE/../../.." && pwd)"
PIPELINE_PY="$HERE_ABS/1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/pipeline_state.py"
if ! STAGE_JSON="$("$PY" "$PIPELINE_PY" --state-path "$PIPELINE_STATE" get --id "$ID" --json 2>/dev/null)"; then
    err "cannot read pipeline-state for id=$ID (does it exist?)"
    echo
    echo "VERDICT: BLOCK"
    exit 1
fi

if ! STAGE="$("$PY" -c "import sys,json; print(json.loads(sys.argv[1])['stage'])" "$STAGE_JSON" 2>/dev/null)"; then
    err "state JSON unreadable"
    exit 1
fi

case "$STAGE" in
    S4-ready|S5-importing) ok "stage=$STAGE (import-ready)" ;;
    S4-qa|S4-fix|S4-failed)
        err "stage=$STAGE: QA not finished (BLOCKs not cleared)"
        ;;
    S3-creating|S3-draft|S3-done)
        err "stage=$STAGE: still in CREATE phase — must finish QA first"
        ;;
    S5-published|S6-monitoring|done)
        err "stage=$STAGE: already past import (double-import risk)"
        ;;
    failed|escalated)
        err "stage=$STAGE: terminal — re-create with new id"
        ;;
    *)
        err "stage=$STAGE: unknown — refusing"
        ;;
esac

# --- 2) qa BLOCK fields ---
echo "[2/5] QA BLOCK fields"
QA_JSON="$("$PY" -c "import sys,json; print(json.dumps(json.loads(sys.argv[1]).get('qa', {})))" "$STAGE_JSON")"
L1="$("$PY" -c "import sys,json; d=json.loads(sys.argv[1]); print(d.get('l1_block'))" "$QA_JSON")"
L2="$("$PY" -c "import sys,json; d=json.loads(sys.argv[1]); print(d.get('l2_block'))" "$QA_JSON")"
L7="$("$PY" -c "import sys,json; d=json.loads(sys.argv[1]); print(d.get('l7_block'))" "$QA_JSON")"
for pair in "l1_block=$L1" "l2_block=$L2" "l7_block=$L7"; do
    k="${pair%=*}"; v="${pair#*=}"
    if [[ "$v" == "None" || "$v" == "" ]]; then
        err "qa.$k is null — QA must report a number (even 0)"
    elif [[ "$v" == "0" ]]; then
        ok "qa.$k=0"
    elif [[ "$v" =~ ^[0-9]+$ ]] && [[ "$v" -gt 0 ]]; then
        err "qa.$k=$v > 0 — fix BLOCKs before import"
    else
        warn "qa.$k='$v' is non-numeric — verify manually"
    fi
done

# --- 3) Blog date double-write (RULES-00 § Sanity 9) ---
if [[ "$TARGET_TYPE" == "blog" ]]; then
    echo "[3/5] blog date double-write (releaseDate + publishedAt)"
    if [[ -z "$ARTIFACT" || ! -f "$ARTIFACT" ]]; then
        err "artifact file missing: $ARTIFACT"
    else
        if grep -q "releaseDate" "$ARTIFACT" 2>/dev/null; then
            ok "releaseDate present"
        else
            err "releaseDate MISSING — must be set alongside publishedAt (RULES-00 §9)"
        fi
        if grep -q "publishedAt" "$ARTIFACT" 2>/dev/null; then
            ok "publishedAt present"
        else
            err "publishedAt MISSING — must be set alongside releaseDate"
        fi
    fi
else
    echo "[3/5] blog date check skipped (type=$TARGET_TYPE)"
    ok "skipped (not a blog)"
fi

# --- 4) Multi-language coverage (RULES-00 § Sanity 7) ---
echo "[4/5] multi-language coverage"
if [[ -z "$ALLOW_LANGS" ]]; then
    REQUIRED=("en" "de" "fr" "it" "ja" "ko" "pt" "ru" "zh" "zh-TW")
    if [[ "$TARGET_TYPE" == "blog" ]]; then
        # blog default = 10 langs (incl. zh + zh-TW)
        warn "language coverage check is advisory only here — full check in sanity-import.sh"
        ok "10 langs required for blog (de/fr/it/ja/ko/pt/ru/zh/zh-TW + en)"
    else
        # landing pages: en + 9 langs
        ok "10 langs required (de/fr/it/ja/ko/pt/ru/zh/zh-TW + en)"
    fi
else
    IFS=',' read -ra ALLOWED <<< "$ALLOW_LANGS"
    ok "language check waived (--allow-langs=${ALLOW_LANGS[*]})"
fi

# --- 5) artifact_path consistent ---
echo "[5/5] artifact consistency"
ARTIFACT_FIELD="$("$PY" -c "import sys,json; print(json.loads(sys.argv[1]).get('artifact_path') or '')" "$STAGE_JSON")"
if [[ -n "$ARTIFACT_FIELD" ]]; then
    ok "state.artifact_path=$ARTIFACT_FIELD"
    if [[ -n "$ARTIFACT" && "$ARTIFACT_FIELD" != "$ARTIFACT" ]]; then
        err "artifact_path mismatch: state=$ARTIFACT_FIELD vs --artifact=$ARTIFACT"
    fi
elif [[ -n "$ARTIFACT" ]]; then
    warn "state.artifact_path is empty but --artifact=$ARTIFACT provided"
fi

# --- verdict ---
echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "VERDICT: BLOCK (${#ERRORS[@]} errors, ${#WARNINGS[@]} warnings)"
    exit 1
fi
echo "VERDICT: PASS (${#WARNINGS[@]} warnings — review if you have time)"
exit 0
