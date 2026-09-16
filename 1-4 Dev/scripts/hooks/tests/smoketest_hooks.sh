#!/usr/bin/env bash
# Smoke test for the 3 hook scripts.
# Verifies exit codes match expected for positive AND negative cases.
# Returns rc=0 only if all checks pass.

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
HOOKS_DIR="$(cd "$HERE/.." && pwd)"
PIPELINE_DIR="$(cd "$HERE/../../../../1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state" && pwd)"
# Use vault-internal temp dir so allowed-root checks pass for hooks.
# tests → hooks → scripts → 1-4 Dev → 项目根（4 级）
PROJECT_ROOT="$(cd "$HERE/../../../.." && pwd)"
# P6：无 LOVART_PYTHON 时自动用项目 venv（服务器 py3.6 不认 pipeline_state 的类型标注）
if [[ -z "${LOVART_PYTHON:-}" && -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
    export LOVART_PYTHON="$PROJECT_ROOT/.venv/bin/python"
fi
PY3="${LOVART_PYTHON:-python3}"
TMP="$HOOKS_DIR/tests/.tmp-smoke"
# Quote TMP everywhere to survive the space in "Lovart MFlow"
rm -rf "$TMP" && mkdir -p "$TMP"
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
        log "  ✓ $desc  (correctly rejected, rc=$?)"
        PASS=$((PASS + 1))
    fi
}

# Set up a clean pipeline-state for testing
STATE="$TMP/state.json"
EVENTS="$TMP/events.jsonl"
PS="$PIPELINE_DIR/pipeline_state.py"
PS_ARGS=(--state-path "$STATE" --events-path "$EVENTS")
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" init >/dev/null

# Add a "ready-to-import" item
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" upsert --id "blog-test-publish" --category blog --target-type blog --artifact-path "$TMP/draft.md" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-publish" --to "S3-creating" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-publish" --to "S3-draft" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-publish" --to "S3-done" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-publish" --to "S4-qa" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" run --id "blog-test-publish" --qa-result '{"l1_block":0,"l2_block":0,"l7_block":0}' >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-publish" --to "S4-ready" >/dev/null

# Create a clean blog draft (well-structured, well-sized, no fluff)
cat > "$TMP/draft.md" <<'EOF'
---
title: A Test Blog Post
slug: blog-test-publish
lang: en
target_type: blog
releaseDate: 2026-07-17
publishedAt: 2026-07-17
---

# Heading One

Intro paragraph that says something specific about the topic. The opening
orients the reader on what is changing and why.

## Section Two

Some content. We write in plain language, with concrete examples from real
workflows we have observed. We avoid generic advice and instead anchor each
recommendation in a specific scenario that someone might face.

## Section Three

More details. The structure here follows the standard anti-slop guidance:
each paragraph answers "who reads this, why now, what changes after reading,
what's the next step."

## Section Four

Practical examples. When we say "you should do X" we also say "here is what
X looks like in production" and "here is how to verify you did it right."

## Section Five

Wrap-up. The closing paragraph ties the sections together and explicitly
states the next action the reader should take.
EOF

# ============== pre-write-check.sh ==============
log "== pre-write-check.sh =="
# Smoke test files live in hooks/tests, so include both real content root
# AND tests dir as allowed (this mirrors how skill devs would use the hook).
ALLOWED=(--allowed-root "$PROJECT_ROOT/1-3 GenFlow"
         --allowed-root "$HOOKS_DIR/tests")
expect_ok "valid file passes"  bash "$HOOKS_DIR/pre-write-check.sh" --file "$TMP/draft.md" "${ALLOWED[@]}"
expect_fail "non-md extension blocked" bash "$HOOKS_DIR/pre-write-check.sh" --file "$TMP/draft.txt"
expect_fail "uppercase filename blocked" bash "$HOOKS_DIR/pre-write-check.sh" --file "$TMP/BlogTest.md"
expect_fail "underscore filename blocked" bash "$HOOKS_DIR/pre-write-check.sh" --file "$TMP/blog_test.md"
expect_fail "too-short slug blocked" bash "$HOOKS_DIR/pre-write-check.sh" --file "$TMP/ab.md"

# Create file with placeholder — pre-write on existing should catch
cat > "$TMP/bad-draft.md" <<'EOF'
# Bad Draft

Some content with [待考证] in it.

More text. lorem ipsum dolor sit amet.
EOF
expect_fail "placeholder detected in existing file" bash "$HOOKS_DIR/pre-write-check.sh" --file "$TMP/bad-draft.md"

# ============== post-write-check.sh ==============
log "== post-write-check.sh =="
expect_ok "clean 159-word draft passes target=150" bash "$HOOKS_DIR/post-write-check.sh" --file "$TMP/draft.md" --target-words 150

# Test word-count shrinkage
expect_fail "159-word draft fails target=7500" bash "$HOOKS_DIR/post-write-check.sh" --file "$TMP/draft.md" --target-words 7500

# Test fluff detection
cat > "$TMP/fluff-draft.md" <<'EOF'
# Cutting-Edge Solutions

In today's fast-paced world of innovation, we must revolutionize the way
teams collaborate. This cutting-edge approach is a game-changer that
allows you to unlock the power of seamless integration.

## Section Two

Some content here. Elevate your workflow with next-level automation.
Navigate the complex landscape of modern tools. Delve into the future.
Transform your business today.

## Section Three

Some content. Embrace the journey. Seamlessly integrate AI into your stack.
Unleash the power of data.

## Section Four

More. As an AI language model, I can help you navigate this landscape.
Please consult a professional before making decisions.

## Section Five

Final. Some more text to make this pass.
EOF
expect_fail "fluff draft blocked by fluff detector" bash "$HOOKS_DIR/post-write-check.sh" --file "$TMP/fluff-draft.md" --target-words 50

# Test low H2 density
cat > "$TMP/flat-draft.md" <<'EOF'
# Flat Document

This document has a lot of text but very few H2 sections. It just keeps
going with one paragraph after another without any clear structure. We
need structure to satisfy the H2 density requirement.

We need at least 4 H2 sections when the document is more than 5000
characters. So let's add more text to push it over the threshold.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
est laborum.

We keep going with more text. The point is to have a long document with
no structure so we can verify the H2 density check fires correctly.
EOF
expect_fail "low H2 density blocked (3000+ chars, 0 H2s)" bash "$HOOKS_DIR/post-write-check.sh" --file "$TMP/flat-draft.md" --target-words 50

# Test unfilled tokens
cat > "$TMP/templated-draft.md" <<'EOF'
# Templated Draft

This file has unfilled tokens like {{SOME_VAR}} and <PLACEHOLDER>.

## Section A

Some content. We have {{ANOTHER_VAR}} here too.

## Section B

More content. {{YET_ANOTHER}}.

## Section C

Final content.
EOF
expect_fail "unfilled tokens blocked" bash "$HOOKS_DIR/post-write-check.sh" --file "$TMP/templated-draft.md" --target-words 50

# ============== pre-import-check.sh ==============
log "== pre-import-check.sh =="
expect_ok "ready item + clean draft passes" bash "$HOOKS_DIR/pre-import-check.sh" --id "blog-test-publish" --state-path "$STATE" --artifact "$TMP/draft.md"

# Test draft missing date double-write
cat > "$TMP/no-dates.md" <<'EOF'
---
title: Missing Dates
slug: blog-no-dates
lang: en
target_type: blog
---

# Heading

Some content here.
EOF
# Reset item with this artifact and re-check
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" upsert --id "blog-test-no-dates" --category blog --target-type blog --artifact-path "$TMP/no-dates.md" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-no-dates" --to "S3-creating" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-no-dates" --to "S3-draft" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-no-dates" --to "S3-done" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-no-dates" --to "S4-qa" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" run --id "blog-test-no-dates" --qa-result '{"l1_block":0,"l2_block":0,"l7_block":0}' >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-no-dates" --to "S4-ready" >/dev/null
expect_fail "missing releaseDate+publishedAt blocked" bash "$HOOKS_DIR/pre-import-check.sh" --id "blog-test-no-dates" --state-path "$STATE" --artifact "$TMP/no-dates.md"

# Test item in wrong stage
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" upsert --id "blog-test-creating" --category blog --target-type blog --artifact-path "$TMP/draft.md" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-creating" --to "S3-creating" >/dev/null
expect_fail "item in S3-creating rejected" bash "$HOOKS_DIR/pre-import-check.sh" --id "blog-test-creating" --state-path "$STATE" --artifact "$TMP/draft.md"

# Test item with non-zero BLOCK
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" upsert --id "blog-test-qa-fail" --category blog --target-type blog --artifact-path "$TMP/draft.md" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-qa-fail" --to "S3-creating" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-qa-fail" --to "S3-draft" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-qa-fail" --to "S3-done" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-qa-fail" --to "S4-qa" >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" run --id "blog-test-qa-fail" --qa-result '{"l1_block":2,"l2_block":0,"l7_block":0}' >/dev/null
"${PY3:-python3}" "$PS" "${PS_ARGS[@]}" advance --id "blog-test-qa-fail" --to "S4-ready" >/dev/null  # force advance
expect_fail "qa l1_block=2 blocks import" bash "$HOOKS_DIR/pre-import-check.sh" --id "blog-test-qa-fail" --state-path "$STATE" --artifact "$TMP/draft.md"

# Test missing id
expect_fail "missing --id exits 2" bash "$HOOKS_DIR/pre-import-check.sh" --state-path "$STATE"

echo ""
echo "==================================================="
echo "smoke results: PASS=$PASS  FAIL=$FAIL"
echo "==================================================="
if [[ "$FAIL" -eq 0 ]]; then
    echo "VERDICT: PASS"
    exit 0
fi
echo "VERDICT: FAIL"
exit 1
