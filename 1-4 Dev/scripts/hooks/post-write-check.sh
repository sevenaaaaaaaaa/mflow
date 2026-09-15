#!/usr/bin/env bash
# post-write-check.sh — Anti-Slop hard checks run AFTER a draft is written.
#
# Detects (returns exit 1 = BLOCK if any triggered):
#   1. H2 density too low (< 4 H2s in 5000+ char doc = no structure)
#   2. Word-count shrinkage vs target (e.g. EN blog < 7500 words)
#   3. Empty/marketing fluff phrases (Anti-Slop L1)
#   4. Mid-section "as an AI" disclaimers (Anti-Slop L3)
#
# Usage:
#   bash post-write-check.sh --file /path/to/file.md \
#       --type blog --lang en --target-words 7500
#
# Exit codes:
#   0 = ok
#   1 = BLOCK (must fix before publish)
#   2 = engine error

set -euo pipefail

usage() {
    sed -n '2,15p' "$0"
    exit 2
}

FILE=""
TARGET_TYPE="blog"
LANG="en"
TARGET_WORDS=7500
STRICT=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --file) FILE="$2"; shift 2;;
        --type) TARGET_TYPE="$2"; shift 2;;
        --lang) LANG="$2"; shift 2;;
        --target-words) TARGET_WORDS="$2"; shift 2;;
        --strict) STRICT=1; shift;;
        -h|--help) usage;;
        *) echo "unknown arg: $1" >&2; usage;;
    esac
done

if [[ -z "$FILE" || ! -f "$FILE" ]]; then
    echo "[err] --file required and must exist ($FILE)" >&2; exit 2
fi

ERRORS=()
WARNINGS=()
ok()   { echo "  ✓ $*"; }
warn() { WARNINGS+=("$*"); echo "  ! $*"; }
err()  { ERRORS+=("$*");   echo "  ✗ $*"; }

echo "[post-write] file=$FILE type=$TARGET_TYPE lang=$LANG target=${TARGET_WORDS}w"

# --- 1) H2 density ---
echo "[1/4] H2 density (need >= 4 H2 sections)"
H2_COUNT="$(grep -cE '^## ' "$FILE" || true)"
H3_COUNT="$(grep -cE '^### ' "$FILE" || true)"
CHAR_COUNT="$(wc -c < "$FILE" | tr -d ' ')"
WORD_COUNT="$(wc -w < "$FILE" | tr -d ' ')"
echo "    stats: $CHAR_COUNT chars, $WORD_COUNT words, $H2_COUNT H2, $H3_COUNT H3"

# Min H2 thresholds scaled by length
if [[ "$CHAR_COUNT" -lt 1000 ]]; then
    MIN_H2=2
elif [[ "$CHAR_COUNT" -lt 5000 ]]; then
    MIN_H2=3
else
    MIN_H2=4
fi

if [[ "$H2_COUNT" -ge "$MIN_H2" ]]; then
    ok "H2=$H2_COUNT >= required $MIN_H2 (length=$CHAR_COUNT)"
else
    err "H2=$H2_COUNT < required $MIN_H2 — restructure with more H2 sections"
fi

# --- 2) Word-count vs target (10% tolerance) ---
echo "[2/4] word count vs target"
MIN_WORDS=$((TARGET_WORDS * 90 / 100))
if [[ "$WORD_COUNT" -lt "$MIN_WORDS" ]]; then
    err "words=$WORD_COUNT < min=$MIN_WORDS (90% of target=$TARGET_WORDS) — content shrink"
else
    ok "words=$WORD_COUNT >= min=$MIN_WORDS"
fi

# --- 3) Empty / marketing fluff (Anti-Slop L1) ---
echo "[3/4] empty/marketing fluff"
# Patterns that signal low-quality content. Heuristic — false positives allowed.
# Note: we don't grep for any single word like "revolutionize" since that breaks
# legitimate usage; we count how many appear and block if > threshold.
FLUFF_PATTERNS=(
    "revolutionize"
    "game-changer"
    "game changer"
    "cutting-edge"
    "cutting edge"
    "in today's fast-paced"
    "in today's digital"
    "world of [a-z]+,?"
    "unlock the power"
    "unleash the power"
    "embark on a journey"
    "navigate the [a-z]+ landscape"
    "delve into"
    "dive deep into"
    "seamless(ly)?"
    "next-level"
    "elevate your"
    "transform your"
)

# Heuristic thresholds: 3+ distinct fluff hits = block; 1-2 = warn
HITS=0
HIT_DETAILS=()
for pat in "${FLUFF_PATTERNS[@]}"; do
    n="$(grep -ciE "$pat" "$FILE" || true)"
    if [[ "$n" -gt 0 ]]; then
        HITS=$((HITS + 1))
        HIT_DETAILS+=("$pat ($n)")
    fi
done
if [[ "$HITS" -eq 0 ]]; then
    ok "no fluff phrases detected"
elif [[ "$HITS" -le 2 ]]; then
    warn "$HITS fluff phrase(s) — review: ${HIT_DETAILS[*]}"
else
    err "$HITS fluff phrases — content reads as marketing copy: ${HIT_DETAILS[*]}"
fi

# --- 4) AI disclaimers (Anti-Slop L3) ---
echo "[4/4] AI disclaimers / meta commentary"
DISCLAIMER_PATTERNS=(
    "as an AI (language model|assistant)"
    "as a large language model"
    "I cannot (provide|guarantee)"
    "I don't have access to"
    "please consult a professional"
    "this is not professional advice"
)
DISC_HITS=0
for pat in "${DISCLAIMER_PATTERNS[@]}"; do
    if grep -qiE "$pat" "$FILE" 2>/dev/null; then
        err "AI disclaimer found: '$pat' — strip from publishable content"
        DISC_HITS=$((DISC_HITS + 1))
    fi
done
if [[ "$DISC_HITS" -eq 0 ]]; then
    ok "no AI disclaimers"
fi

# --- 5) Block-style placeholder tokens (e.g. <PLACEHOLDER> / {{VAR}}) ---
echo "[5/5] unfilled template tokens"
TEMPLATED="$(grep -cE '\{\{[A-Z_]+\}\}|<[A-Z_]+>' "$FILE" || true)"
if [[ "$TEMPLATED" -gt 0 ]]; then
    err "unfilled template tokens present ($TEMPLATED occurrences)"
else
    ok "no unfilled tokens"
fi

echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "VERDICT: BLOCK (${#ERRORS[@]} errors, ${#WARNINGS[@]} warnings)"
    exit 1
fi
echo "VERDICT: PASS (${#WARNINGS[@]} warnings)"
exit 0
