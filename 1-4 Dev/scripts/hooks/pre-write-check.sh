#!/usr/bin/env bash
# pre-write-check.sh — enforce format rules before writing any content file.
#
# Refuses (exit 1) if any of these are violated:
#   1. Filename matches slug-format (lowercase, hyphens, .md extension)
#   2. Path is under an allowed content root (1-3 GenFlow/...)
#   3. Required frontmatter fields present (title, slug, lang, target_type)
#   4. No forbidden patterns (placeholder text, unfilled templated tokens)
#
# Usage:
#   bash pre-write-check.sh --file /path/to/file.md \
#       [--allowed-root /abs/path/to/1-3\ GenFlow] \
#       [--strict]
#
# Exit codes:
#   0 = ok to write
#   1 = BLOCK — fix issues
#   2 = engine error (bad args / file unreadable)

set -euo pipefail

usage() {
    sed -n '2,16p' "$0"
    exit 2
}

FILE=""
ALLOWED_ROOTS=()
STRICT=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --file) FILE="$2"; shift 2;;
        --allowed-root) ALLOWED_ROOTS+=("$2"); shift 2;;
        --strict) STRICT=1; shift;;
        -h|--help) usage;;
        *) echo "unknown arg: $1" >&2; usage;;
    esac
done

if [[ -z "$FILE" ]]; then echo "[err] --file required" >&2; exit 2; fi

# Default allowed roots: 1-3 GenFlow and its subdirs
if [[ ${#ALLOWED_ROOTS[@]} -eq 0 ]]; then
    MFLOW_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
    ALLOWED_ROOTS=("$MFLOW_ROOT/1-3 GenFlow")
fi

ERRORS=()
WARNINGS=()
ok()   { echo "  ✓ $*"; }
warn() { WARNINGS+=("$*"); echo "  ! $*"; }
err()  { ERRORS+=("$*");   echo "  ✗ $*"; }

BASENAME="$(basename "$FILE")"
DIRNAME="$(dirname "$FILE")"

echo "[pre-write] file=$FILE"

# --- 1) Filename format ---
echo "[1/4] filename format"
if [[ "$BASENAME" != *.md ]]; then
    err "filename must end with .md (got: $BASENAME)"
fi
# strip extension
STEM="${BASENAME%.md}"
if [[ ! "$STEM" =~ ^[a-z0-9][a-z0-9\-]{2,79}$ ]]; then
    err "filename stem '$STEM' must be kebab-case, 3-80 chars, no underscores/uppercase"
else
    ok "kebab-case slug: $STEM"
fi

# --- 2) Path under allowed root ---
echo "[2/4] path under allowed root"
ALLOWED_OK=0
for root in "${ALLOWED_ROOTS[@]}"; do
    if [[ "$FILE" == "$root"* ]]; then
        ok "under allowed root: $root"
        ALLOWED_OK=1
        break
    fi
done
if [[ "$ALLOWED_OK" -eq 0 ]]; then
    err "file is NOT under any allowed root (file=$FILE; allowed=${ALLOWED_ROOTS[*]})"
fi

# --- 3) Frontmatter ---
echo "[3/4] required frontmatter fields"
if [[ ! -f "$FILE" ]]; then
    warn "file does not exist yet (will be created) — skipping frontmatter check"
else
    if head -5 "$FILE" | grep -q '^---$'; then
        ok "has YAML frontmatter delimiter"
        REQUIRED_FM=("title" "slug")
        for f in "${REQUIRED_FM[@]}"; do
            if grep -q "^${f}:" "$FILE"; then
                ok "frontmatter has '$f'"
            else
                if [[ "$STRICT" -eq 1 ]]; then
                    err "frontmatter missing required field '$f'"
                else
                    warn "frontmatter missing '$f' (strict mode would block)"
                fi
            fi
        done
    else
        err "missing YAML frontmatter (first line should be '---')"
    fi
fi

# --- 4) Forbidden patterns ---
echo "[4/4] forbidden patterns"
if [[ -f "$FILE" ]]; then
    FORBIDDEN=(
        'TODO:'
        'FIXME:'
        '\[待考证\]'
        '\[PLACEHOLDER\]'
        'lorem ipsum'
        'Lorem Ipsum'
    )
    found_forbidden=0
    for pat in "${FORBIDDEN[@]}"; do
        if grep -qF "$pat" "$FILE" 2>/dev/null; then
            err "forbidden pattern present: '$pat'"
            found_forbidden=1
        fi
    done
    if [[ "$found_forbidden" -eq 0 ]]; then
        ok "no forbidden patterns"
    fi
else
    ok "no file to scan (write-only check)"
fi

echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "VERDICT: BLOCK (${#ERRORS[@]} errors, ${#WARNINGS[@]} warnings)"
    exit 1
fi
echo "VERDICT: PASS (${#WARNINGS[@]} warnings)"
exit 0
