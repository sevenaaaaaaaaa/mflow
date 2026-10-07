#!/usr/bin/env bash
# geo-check.sh — GEO（生成式引擎优化）可引用性检查，在 post-write-check 之后运行。
#
# 依据：AI 引擎引用内容时偏好「可分块、含统计、有出处、自包含段落」的稿子
# （GEO 研究：statistics / quotations / citations 提升 AI 可见度）。
# 检查（默认宽松=warn 为主，--strict 全部升 BLOCK）：
#   1. 可分块结构：H2 密度 + 超长章节（>3500 字符无切分 = AI 难摘块）
#   2. 统计/数据点密度：数字-百分比/小数/年份 每 1000 字符 <1 → BLOCK（0 块），低 → WARN
#   3. 问答式块：`## / ### 标题含 ?` 或 FAQ 章节，0 个 → WARN（strict → BLOCK）
#   4. 来源标注：外部 http(s) 链接数，0 → WARN（strict → BLOCK）
#   5. 墙式段落：≥800 字符的段落占比 >25% → BLOCK，>10% → WARN
#
# Usage:
#   bash geo-check.sh --file /path/to/draft.md [--strict] [--lang zh]
#
# Exit codes:
#   0 = ok (PASS)
#   1 = BLOCK
#   2 = engine error

set -euo pipefail

usage() {
    sed -n '2,20p' "$0"
    exit 2
}

FILE=""
STRICT=0
LANG_ARG=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --file) FILE="$2"; shift 2;;
        --strict) STRICT=1; shift;;
        --lang) LANG_ARG="$2"; shift 2;;
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
# strict 模式把 warn 升级为 err
strict_warn() {
    if [[ "$STRICT" -eq 1 ]]; then err "$*"; else warn "$*"; fi
}

echo "[geo-check] file=$FILE strict=$STRICT"

CHAR_COUNT="$(wc -c < "$FILE" | tr -d ' ')"

# --- 1) 可分块结构 ---
echo "[1/5] chunkable structure (H2 density + section size)"
H2_COUNT="$(grep -cE '^## ' "$FILE" || true)"
if [[ "$CHAR_COUNT" -lt 1000 ]]; then
    MIN_H2=2
elif [[ "$CHAR_COUNT" -lt 5000 ]]; then
    MIN_H2=3
else
    MIN_H2=4
fi
if [[ "$H2_COUNT" -ge "$MIN_H2" ]]; then
    ok "H2=$H2_COUNT >= $MIN_H2"
else
    err "H2=$H2_COUNT < $MIN_H2 — AI 引擎按节分块，结构不足难被引用"
fi
# 超长章节：以 H2 分段后统计最大段字符数
LONGEST_SECTION="$(awk '
    /^## / { if (cur > max) max = cur; cur = 0; next }
    { cur += length($0) }
    END { if (cur > max) max = cur; print max + 0 }
' "$FILE")"
LONGEST_SECTION="${LONGEST_SECTION:-0}"
if [[ "$LONGEST_SECTION" -gt 3500 ]]; then
    strict_warn "最长章节 ${LONGEST_SECTION} 字符 > 3500 — 拆成可摘块（加 H3/列表/表格）"
else
    ok "章节块大小合理（max=${LONGEST_SECTION}）"
fi

# --- 2) 统计/数据点密度 ---
echo "[2/5] statistics density (GEO: data-rich content gets cited)"
STAT_HITS="$(grep -oE '[0-9]+(\.[0-9]+)?%|[0-9]+(\.[0-9]+)?x|\$[0-9][0-9,]*|20[0-9]{2}年?|[0-9]+/[0-9]+' "$FILE" | wc -l | tr -d ' ' || true)"
DENSITY_K=1
if [[ "$CHAR_COUNT" -ge 1000 ]]; then
    DENSITY="$(awk -v s="$STAT_HITS" -v c="$CHAR_COUNT" 'BEGIN { printf "%.2f", s / (c / 1000) }')"
    DENSITY_INT="${DENSITY%%.*}"
    if [[ "$STAT_HITS" -eq 0 ]]; then
        err "0 个数据点 — 无统计/百分比的稿子在 GEO 里几乎不被引用（补：数据、百分比、价格、年份）"
    elif [[ "$DENSITY_INT" -lt 1 ]]; then
        strict_warn "数据点密度 ${DENSITY}/千字符 偏低（hits=$STAT_HITS, chars=${CHAR_COUNT}）— 建议每千字 ≥1 个"
    else
        ok "数据点密度 ${DENSITY}/千字符（hits=${STAT_HITS}）"
    fi
else
    ok "短稿跳过密度检查（chars=${CHAR_COUNT}）"
fi

# --- 3) 问答式标题 / FAQ 块 ---
echo "[3/5] Q&A headings (AI engines love question-shaped chunks)"
Q_H2="$(grep -cE '^#{2,3} .*(\?|？)' "$FILE" || true)"
if grep -qiE '^#{1,3} *(FAQ|常见问题|よくある)' "$FILE" 2>/dev/null; then
    Q_H2=$((Q_H2 + 1))
    ok "发现 FAQ 节"
fi
if [[ "$Q_H2" -gt 0 ]]; then
    ok "问答式标题 $Q_H2 个"
else
    strict_warn "无问答式 H2/H3（加 2-3 个「…?」标题或 FAQ 节，对准用户真实提问）"
fi

# --- 4) 外部来源引用 ---
echo "[4/5] outbound sources (citations improve AI trust)"
LINKS="$(grep -oE 'https?://[a-zA-Z0-9./?=_%&#-]+' "$FILE" | grep -vcE 'example\.com|yourdomain|localhost|127\.0\.0\.1' || true)"
if [[ "$LINKS" -ge 2 ]]; then
    ok "外部来源链接 $LINKS 条"
elif [[ "$LINKS" -eq 1 ]]; then
    strict_warn "仅 1 条外部来源 — 权威出处 ≥2 条可提升 AI 采信"
else
    strict_warn "0 条外部来源标注 — GEO 共识：带 source 的内容更易被 AI 引用"
fi

# --- 5) 墙式段落（可摘录性）---
echo "[5/5] wall-of-text paragraphs (snippets live in short paragraphs)"
PARA_STATS="$(awk '
    BEGIN { total = 0; longp = 0; cur = 0 }
    /^$/ { if (cur >= 800) longp++; if (cur > 0) total++; cur = 0; next }
    /^#/ { if (cur >= 800) longp++; if (cur > 0) total++; cur = 0; next }
    { cur += length($0) + 1 }
    END { if (cur >= 800) longp++; if (cur > 0) total++; print total + 0, longp + 0 }
' "$FILE")"
TOTAL_PARA="$(echo "$PARA_STATS" | awk '{print $1}')"
LONG_PARA="$(echo "$PARA_STATS" | awk '{print $2}')"
if [[ "$TOTAL_PARA" -eq 0 ]]; then
    ok "无段落（纯结构稿）"
else
    PCT="$((LONG_PARA * 100 / TOTAL_PARA))"
    if [[ "$PCT" -gt 25 ]]; then
        err "墙式段落占比 ${PCT}%（$LONG_PARA/$TOTAL_PARA 段 ≥800 字符）— AI 摘录依赖自包含短段"
    elif [[ "$PCT" -gt 10 ]]; then
        strict_warn "墙式段落占比 ${PCT}% — 建议拆分长段落"
    else
        ok "段落可摘录性良好（长段占比 ${PCT}%）"
    fi
fi

echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then
    echo "VERDICT: BLOCK (${#ERRORS[@]} errors, ${#WARNINGS[@]} warnings)"
    exit 1
fi
echo "VERDICT: PASS (${#WARNINGS[@]} warnings)"
exit 0
