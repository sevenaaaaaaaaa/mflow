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
#
# 2026-10-09 用户裁定增量（Moodio/Lovart 共用）：
#   GATE6 增补两条：开场模板轮换（6.7，openers.log 连续同型 ready 拦截）+ 证据类型多样性（6.8）
#   前因：场景冷开场连续复用=新模板 AI 味（Lovart/Moodio 生成侧都出现过）

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
READY=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --file) FILE="$2"; shift 2;;
        --type) TARGET_TYPE="$2"; shift 2;;
        --lang) LANG="$2"; shift 2;;
        --target-words) TARGET_WORDS="$2"; shift 2;;
        --strict) STRICT=1; shift;;
        --ready) READY=1; shift;;
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
# Phase 2 fix (2026-09-15): wc -w splits on whitespace only, so CJK long-form text
# was undercounted (680 汉字 → 21 words). Word-equivalent = ASCII words + CJK/2.
WORD_COUNT="$(perl -CSD -ne '
    $c += () = /\p{Han}|\p{Hiragana}|\p{Katakana}|\p{Hangul}/g;
    $w += () = /[A-Za-z0-9]+/g;
    END { print $w + int(($c + 1) / 2) }
' "$FILE" 2>/dev/null || wc -w < "$FILE" | tr -d ' ')"
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
echo "[5/6] unfilled template tokens"
TEMPLATED="$(grep -cE '\{\{[A-Z_]+\}\}|<[A-Z_]+>' "$FILE" || true)"
if [[ "$TEMPLATED" -gt 0 ]]; then
    err "unfilled template tokens present ($TEMPLATED occurrences)"
else
    ok "no unfilled tokens"
fi

# --- 6) Positive quality markers (RULES-30 §四 12 项机检) ---
# 分级：默认（loop/批量中稿）= WARN 提示，不触发重试烧 token；
#       --ready（ready 前终检）= ERROR，缺任一项不可标 ready。
echo "[6/6] positive quality markers (draft=warn, --ready=block)"
LONG_DOC=$(( WORD_COUNT >= 4000 ? 1 : 0 ))
quant() { # ok? marker text  → --ready 缺失=BLOCK / 草稿缺失=WARN
    if [[ "$READY" -eq 1 && "$1" -eq 0 ]]; then err "$3"; return; fi
    if [[ "$1" -eq 0 ]]; then warn "$3 (ready 终检将拦截)"; return; fi
    ok "$3"
}

# 6.1 首人称真实视角（必须，RULES-30 #4）
if [[ "$LANG" == "en" ]]; then
    FP="$(grep -cE '\b(I|my|mine|we)\b' "$FILE" 2>/dev/null || true)"
else
    FP="$(grep -cE '我|亲身|实测|我们' "$FILE" 2>/dev/null || true)"
fi
FP_OK=$([[ "$FP" -ge 1 ]] && echo 1 || echo 0)
quant "$FP_OK" "first-person" "first-person presence (hits=$FP)"

# 6.2 翻车/踩坑段落（必须，RULES-30 #4）
FAILN="$(grep -cE '踩坑|翻车|教训|血泪|掉坑|差点|复盘|failure mode|pitfall|lesson|got burned|misstep|mistakes I' "$FILE" 2>/dev/null || true)"
FAIL_OK=$([[ "$FAILN" -ge 1 ]] && echo 1 || echo 0)
quant "$FAIL_OK" "pitfall" "pitfall/lesson section (hits=$FAILN)"

# 6.3 金句（可引用观点句 proxy：反共识对照句式）
QUOTE="$(grep -cE '而不是|不是.{0,20}[，。]?而是|真正的|别再|认清|not just [a-z ]+, but|isn.t [a-z ]+.*it.s|it.s not [a-z ]+, it.s|what actually matters' "$FILE" 2>/dev/null || true)"
QUOTE_OK=$([[ "$QUOTE" -ge 1 ]] && echo 1 || echo 0)
quant "$QUOTE_OK" "quote" "quotable insight line proxy (hits=$QUOTE)"

# 6.4 数据点密度：含数字行 ≥ 每 1000 词当量 1 处（RULES-70）
if [[ "$WORD_COUNT" -ge 1000 ]]; then
    NEED=$(( WORD_COUNT / 1000 ))
    DATAN="$(grep -cE '[0-9]' "$FILE" 2>/dev/null || true)"
    if [[ "$DATAN" -ge "$NEED" ]]; then
        ok "data-point density ($DATAN numeric lines >= need $NEED)"
    else
        DROW="data-point density low ($DATAN < need $NEED)"
        if [[ "$READY" -eq 1 ]]; then err "$DROW"; else warn "$DROW (ready 终检将拦截)"; fi
    fi
fi

# 6.7 开场模板轮换（2026-10-09 用户裁定：场景冷开场已成新模板 AI 味——Lovart/Moodio 都踩过，机器轮换制）
# 开场型指纹：scene-anecdote（"It was <时间>…" / "The <星期> I…" / "Last <季节>…"）
# 机制：run/openers.log 记录 (日期|文件|开场型)；--ready 时若最近 2 篇同型 → BLOCK；草稿档仅提示。
if [[ -n "${MFLOW_OPENERS_LOG:-}" ]]; then OPENER_LOG="$MFLOW_OPENERS_LOG"; else OPENER_LOG="openers.log"; fi
SCENE_OPEN="$( { head -c 400 "$FILE" 2>/dev/null | grep -iE '^(it was (on )?(a |an )?(monday|tuesday|wednesday|thursday|friday|saturday|sunday|summer|winter|night|morning)|the (monday|tuesday|wednesday|thursday|friday|saturday|sunday) i |last (summer|winter|year|month|week))' || true; } | wc -l | tr -d ' ')"
OPENER_CLASS="other"
[[ "$SCENE_OPEN" -ge 1 ]] && OPENER_CLASS="scene-anecdote"
RECENT="$( { tail -2 "$OPENER_LOG" 2>/dev/null | grep "|$OPENER_CLASS" || true; } | wc -l | tr -d ' ')"
if [[ "$OPENER_CLASS" == "scene-anecdote" && "$RECENT" -ge 2 && "$READY" -eq 1 ]]; then
    err "opening repeats the last 2 pieces (scene-anecdote cold open) — rotate opener class"
elif [[ "$OPENER_CLASS" == "scene-anecdote" ]]; then
    warn "scene cold-open detected — 若上一篇同款请换开场型（轮换制，用户裁定 2026-10-09）"
fi
echo "$(date +%F)|$(basename "$FILE")|$OPENER_CLASS" >> "$OPENER_LOG" 2>/dev/null || true

# 6.8 证据类型多样性（用户裁定：专栏声音 = 我实测 + 我听说/转述 + 产品侧发现 + 外部数据 的混合，不是永远第一人称场景）
REPORTED="$(grep -cE 'a DP I|a producer I|one of (our|the) (engineers|producers|editors)|I heard|colleague|friend|我听说|据.{0,8}(说|讲)|同事|业内朋友' "$FILE" 2>/dev/null || true)"
INSIDER="$(grep -cE 'when we built|our (team|product|engineers)|in our product|we shipped|我们做产品时|我们内部' "$FILE" 2>/dev/null || true)"
EV_OK=$([[ "$REPORTED" -ge 1 || "$INSIDER" -ge 1 ]] && echo 1 || echo 0)
quant "$EV_OK" "evidence-mix" "evidence-type mix: reported=${REPORTED} insider=${INSIDER} (只有第一人称场景=声音单一)"

# 6.9 图文并茂机检（2026-10-09 用户裁定：正文必须有可见图，briefs/附表不算图）
# 视为"有图"：Markdown 内联图 ![alt](https://...) 或 HTML <img src="https://...">
if [[ "$TARGET_TYPE" == "blog" && "$WORD_COUNT" -ge 1500 ]]; then
    INLINE_IMG="$(grep -cE '!\[[^]]*\]\(https://[^)]+\)|<img[^>]+src="https://' "$FILE" 2>/dev/null || true)"
    INLINE_IMG="${INLINE_IMG:-0}"
    if [[ "$INLINE_IMG" -eq 0 ]]; then
        IROW="no inline image in body (图文并茂：正文需≥1张可见图，仅 Image Appendix/briefs 不算)"
        if [[ "$READY" -eq 1 ]]; then err "$IROW"; else warn "$IROW (ready 终检将拦截)"; fi
    else
        ok "inline images present ($INLINE_IMG)"
    fi
fi
set +e
_URLS_RAW="$(grep -oE 'https://[a-zA-Z0-9.-]+[/A-Za-z0-9?=&._-]*' "$FILE" 2>/dev/null)"
if [[ -n "$_URLS_RAW" ]]; then
    EXT_URLS="$(echo "$_URLS_RAW" | grep -viE 'example\.com|localhost|127\.0\.0\.1|\.mflow\.|app\.moodio' | sort -u | wc -l | tr -d ' ')"
else
    EXT_URLS=0
fi
set -e 2>/dev/null || true
EXT_URLS="${EXT_URLS:-0}"
EXT_OK=$([[ "$EXT_URLS" -ge 2 ]] && echo 1 || echo 0)
quant "$EXT_OK" "external" "external citation URLs (unique=$EXT_URLS)"

# 6.6 FAQ 块（blog 长文必须；条目数由 content-quality-gates L3 复核）
if [[ "$TARGET_TYPE" == "blog" && "$LONG_DOC" -eq 1 ]]; then
    FAQ="$(grep -cE '^#+ .*(FAQ|常见问题|Frequently)' "$FILE" 2>/dev/null || true)"
    FAQ_OK=$([[ "$FAQ" -ge 1 ]] && echo 1 || echo 0)
    quant "$FAQ_OK" "faq-block" "FAQ section present (hits=$FAQ)"
fi

echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "VERDICT: BLOCK (${#ERRORS[@]} errors, ${#WARNINGS[@]} warnings)"
    exit 1
fi
echo "VERDICT: PASS (${#WARNINGS[@]} warnings)"
exit 0
