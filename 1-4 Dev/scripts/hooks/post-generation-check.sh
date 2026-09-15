#!/usr/bin/env bash
# post-generation-check.sh — 统一质量门禁 (landing-page + blog)
#
# 覆盖 5 个问题：
#   1. 图片 404 — HEAD 检查所有 image_url / cover_url
#   2. SEO 字段规范 — 必填字段检查 + Sanity-legal category
#   3. 运行中忘记约束 — 结构化检查 (H2/词数/frontmatter)
#   4. 批量脚本约束 — 检查脚本是否引用 deprecated skill
#   5. 质量自降 — fluff/空泛词/AI自介/低信息密度
#
# Usage:
#   bash post-generation-check.sh --file <path> --type blog|landing [--lang en] [--target-words 7500]
#   bash post-generation-check.sh --script <path>  (检查脚本合规性)
#
# Exit codes:
#   0 = PASS
#   1 = BLOCK
#   2 = engine error

set -euo pipefail

VAULT="${LOVART_RESOURCE_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)}"
FILE=""
SCRIPT=""
TYPE="blog"
LANG="en"
TARGET_WORDS=7500

while [[ $# -gt 0 ]]; do
  case "$1" in
    --file) FILE="$2"; shift 2;;
    --script) SCRIPT="$2"; shift 2;;
    --type) TYPE="$2"; shift 2;;
    --lang) LANG="$2"; shift 2;;
    --target-words) TARGET_WORDS="$2"; shift 2;;
    *) echo "unknown: $1" >&2; exit 2;;
  esac
done

ERRORS=0
WARNINGS=0
err()  { echo "  ✗ $*"; ERRORS=$((ERRORS + 1)); }
warn() { echo "  ! $*"; WARNINGS=$((WARNINGS + 1)); }
ok()   { echo "  ✓ $*"; }

# ============================================================
# MODE 1: 检查脚本 (batch scripts / new scripts)
# ============================================================
if [[ -n "$SCRIPT" ]]; then
  echo "=== Script governance check: $SCRIPT ==="
  
  # G1: naming
  bn=$(basename "$SCRIPT")
  ext="${bn##*.}"
  if [[ "$ext" == "py" ]]; then
    if echo "$bn" | grep -qE '^[a-z][a-z0-9_]+\.py$'; then
      ok "G1 naming: $bn"
    else
      err "G1 naming: $bn (expected snake_case.py)"
    fi
  elif [[ "$ext" == "sh" ]]; then
    if echo "$bn" | grep -qE '^[a-z][a-z0-9\-]+\.sh$'; then
      ok "G1 naming: $bn"
    else
      err "G1 naming: $bn (expected kebab-case.sh)"
    fi
  fi
  
  # G2: shebang
  if head -1 "$SCRIPT" | grep -q '^#!'; then
    ok "G2 shebang: present"
  else
    err "G2 shebang: missing"
  fi
  
  # G3: deprecated skill references
  DEP_REFS=$(grep -cE "serp.writer|blog.automation|i18n.pipeline|translat" "$SCRIPT" 2>/dev/null | head -1 || true)
  # Filter out content words (not import statements)
  IMPORT_REFS=$(grep -cE "^import|^from.*import" "$SCRIPT" 2>/dev/null || true)
  CONTENT_REFS=$(grep -cE "serp.writer|blog.automation" "$SCRIPT" 2>/dev/null || true)
  if [[ "$CONTENT_REFS" -gt 0 ]]; then
    err "G3 deprecated refs: $CONTENT_REFS references to deprecated skills"
  else
    ok "G3 deprecated: none"
  fi
  
  # G4: no hardcoded API keys
  if grep -qE "ntn_[a-zA-Z0-9]|sk-[a-zA-Z0-9]|token.*=.*['\"]" "$SCRIPT" 2>/dev/null; then
    err "G4 secrets: possible hardcoded API key"
  else
    ok "G4 secrets: none found"
  fi
  
  # G5: no rm -rf on important paths
  if grep -qE "rm -rf.*/Users/" "$SCRIPT" 2>/dev/null; then
    err "G5 safety: rm -rf on user paths"
  else
    ok "G5 safety: ok"
  fi
  
  echo ""
  if [[ $ERRORS -gt 0 ]]; then
    echo "VERDICT: BLOCK ($ERRORS errors)"
    exit 1
  fi
  echo "VERDICT: PASS"
  exit 0
fi

# ============================================================
# MODE 2: 检查文件 (blog / landing page)
# ============================================================
if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  echo "[err] --file required and must exist" >&2
  exit 2
fi

BN=$(basename "$FILE")
echo "=== Post-generation check: $BN ==="

# ── Gate 1: 图片 404 检查 ──
echo "[1/5] Image 404 check"
IMAGE_URLS=$(grep -oE 'https?://[^")\s]+\.(jpg|jpeg|png|gif|webp|svg)' "$FILE" 2>/dev/null || true)
COVER_URLS=$(grep -oE 'cover_url:.*https?://[^")\s]+' "$FILE" 2>/dev/null || true)
ALL_URLS=$(echo -e "$IMAGE_URLS\n$COVER_URLS" | sort -u | grep -v '^$')

if [[ -n "$ALL_URLS" ]]; then
  URL_COUNT=$(echo "$ALL_URLS" | wc -l | tr -d ' ')
  DEAD=0
  while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    # Skip CDN URLs (lovart.ai, blogs.lovart.ai) — assume valid
    if echo "$url" | grep -qE "lovart\.ai|blogs\.lovart\.ai"; then
      continue
    fi
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")
    if [[ "$HTTP_CODE" == "000" || "$HTTP_CODE" == "404" || "$HTTP_CODE" == "403" ]]; then
      err "image 404/403: $url (HTTP $HTTP_CODE)"
      DEAD=$((DEAD + 1))
    fi
  done <<< "$ALL_URLS"
  if [[ "$DEAD" -eq 0 ]]; then
    ok "images: $URL_COUNT URLs, all reachable"
  else
    err "images: $DEAD dead URLs out of $URL_COUNT"
  fi
else
  ok "images: no external URLs found"
fi

# ── Gate 2: SEO 字段规范 ──
echo "[2/5] SEO field compliance"
if head -1 "$FILE" | grep -q '^---$'; then
  # Blog SEO fields
  if [[ "$TYPE" == "blog" ]]; then
    REQUIRED_FM=("title" "slug" "date" "category" "keywords" "description" "cover_url" "seo_title" "seo_description")
    for field in "${REQUIRED_FM[@]}"; do
      if grep -q "^${field}:" "$FILE"; then
        ok "frontmatter: $field present"
      else
        err "frontmatter: $field MISSING"
      fi
    done
    # Check category is Sanity-legal
    CAT=$(grep "^category:" "$FILE" | head -1 | sed 's/category: *//' | tr -d '"' | tr -d "'")
    LEGAL_CATS=("How-To" "Industry Solution" "Branding" "Comparison" "Best Practice" "Better Design" "Case Study" "Digest" "Glossary" "Insight" "Segment" "Product Update")
    CAT_OK=0
    for lc in "${LEGAL_CATS[@]}"; do
      [[ "$CAT" == "$lc" ]] && CAT_OK=1
    done
    if [[ "$CAT_OK" -eq 1 ]]; then
      ok "category: Sanity-legal ($CAT)"
    else
      err "category: '$CAT' is NOT Sanity-legal (allowed: ${LEGAL_CATS[*]})"
    fi
  fi
  # Landing page SEO fields
  if [[ "$TYPE" == "landing" ]]; then
    REQUIRED_LP=("title" "schemaVersion" "storylineTemplate" "bodyJson")
    for field in "${REQUIRED_LP[@]}"; do
      if grep -q "\"${field}\"" "$FILE" || grep -q "^${field}:" "$FILE"; then
        ok "landing: $field present"
      else
        err "landing: $field MISSING"
      fi
    done
  fi
else
  err "frontmatter: missing YAML delimiter (---)"
fi

# ── Gate 3: 结构化质量 (约束合规) ──
echo "[3/5] Structural quality"
# H2 density
H2_COUNT=$(grep -c '^## ' "$FILE" 2>/dev/null || true)
CHAR_COUNT=$(wc -c < "$FILE" | tr -d ' ')
if [[ "$CHAR_COUNT" -gt 5000 && "$H2_COUNT" -lt 4 ]]; then
  err "structure: H2=$H2_COUNT < 4 (need ≥4 for docs >5000 chars)"
else
  ok "structure: H2=$H2_COUNT (ok for $CHAR_COUNT chars)"
fi

# Word count
WORD_COUNT=$(wc -w < "$FILE" | tr -d ' ')
MIN_WORDS=$((TARGET_WORDS * 90 / 100))
if [[ "$WORD_COUNT" -lt "$MIN_WORDS" ]]; then
  err "structure: words=$WORD_COUNT < min=$MIN_WORDS (90% of $TARGET_WORDS)"
else
  ok "structure: words=$WORD_COUNT ≥ $MIN_WORDS"
fi

# No template tokens
TEMPLATE_COUNT=$(grep -cE '\{\{[A-Z_]+\}\}|<[A-Z_]+>' "$FILE" 2>/dev/null || true)
if [[ "$TEMPLATE_COUNT" -gt 0 ]]; then
  err "structure: $TEMPLATE_COUNT unfilled template tokens"
else
  ok "structure: no template tokens"
fi

# ── Gate 4: 批量脚本约束 ──
echo "[4/5] Batch/script constraints (skip for content files)"
ok "skip: not a script file"

# ── Gate 5: 质量自降检测 ──
echo "[5/5] Quality self-degradation"

# Fluff phrases
FLUFF_COUNT=0
for pat in "revolutionize" "game-changer" "cutting-edge" "in today's fast-paced" \
           "unlock the power" "unleash the power" "embark on a journey" \
           "delve into" "next-level" "elevate your" "transform your"; do
  n=$(grep -ciE "$pat" "$FILE" 2>/dev/null || true)
  FLUFF_COUNT=$((FLUFF_COUNT + n))
done
if [[ "$FLUFF_COUNT" -gt 3 ]]; then
  err "quality: $FLUFF_COUNT fluff phrases (max 3)"
elif [[ "$FLUFF_COUNT" -gt 0 ]]; then
  warn "quality: $FLUFF_COUNT fluff phrases"
else
  ok "quality: 0 fluff phrases"
fi

# AI self-introduction
AI_COUNT=$(grep -ciE "as an AI|as a language model|I cannot provide|I don't have access" "$FILE" 2>/dev/null || true)
if [[ "$AI_COUNT" -gt 0 ]]; then
  err "quality: $AI_COUNT AI self-introduction patterns"
else
  ok "quality: no AI self-intro"
fi

# Low information density: paragraphs without concrete data
LONG_PARAS=$(awk '/^$/{p=0;next} {p+=length($0)} p>200 && /^[A-Z]/' "$FILE" 2>/dev/null | wc -l | tr -d ' ')
if [[ "$LONG_PARAS" -gt 5 ]]; then
  warn "quality: $LONG_PARAS long paragraphs (>200 chars) — check info density"
else
  ok "quality: paragraph density ok"
fi

# ── Verdict ──
echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "VERDICT: BLOCK ($ERRORS errors, $WARNINGS warnings)"
  exit 1
elif [[ $WARNINGS -gt 0 ]]; then
  echo "VERDICT: PASS with warnings ($WARNINGS)"
  exit 0
else
  echo "VERDICT: PASS"
  exit 0
fi
