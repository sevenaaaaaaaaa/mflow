#!/usr/bin/env bash
# quota-check.sh — RULES-70 数量限制与防注水（硬门禁）
#
# 检查：① 字数上限 ② H2 数 ③ FAQ 数 ④ 重复句/段落 ⑤ 列表灌水 ⑥ 模板过渡词堆砌
# Exit: 0=PASS / 1=BLOCK / 2=engine error
#
# Usage: bash quota-check.sh --file x.md [--type blog|landing] [--lang zh]
set -euo pipefail

FILE=""; TYPE="blog"; LANG="zh"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --file) FILE="$2"; shift 2;;
    --type) TYPE="$2"; shift 2;;
    --lang) LANG="$2"; shift 2;;
    -h|--help) sed -n '2,10p' "$0"; exit 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[[ -z "$FILE" || ! -f "$FILE" ]] && { echo "[err] --file required" >&2; exit 2; }

ERRORS=(); WARNINGS=()
ok()   { echo "  ✓ $*"; }
warn() { WARNINGS+=("$*"); echo "  ! $*"; }
err()  { ERRORS+=("$*");   echo "  ✗ $*"; }

echo "[quota-check] file=$FILE type=$TYPE lang=$LANG"

# 中英混合计数：CJK 字符 + 英文词
CHARS=$(perl -CSD -ne '$c += () = /\p{Han}|\p{Hiragana}|\p{Katakana}|\p{Hangul}/g; $w += () = /[A-Za-z0-9]+/g; END { print int($c + $w * 1.5) }' "$FILE" 2>/dev/null || wc -c < "$FILE")
H2=$(grep -cE '^## ' "$FILE" || true)
FAQ=$(grep -cE '^#{2,3} *(FAQ|常见问题|よくある)' "$FILE" || true)
QH=$(grep -cE '^#{2,3} .*[?？]$' "$FILE" || true)

# ① 字数上限（RULES-70：Blog 1200-1800，上限 +20% → 2160；落地页 600-1000 → 1200）
echo "[1/6] 字数预算"
if [[ "$TYPE" == "landing" ]]; then MAXW=1200; else MAXW=2160; fi
if [[ "$CHARS" -gt "$MAXW" ]]; then
  err "字数 $CHARS > 上限 $MAXW（注水嫌疑：优先删冗余，勿扩写）"
else
  ok "字数 $CHARS ≤ $MAXW"
fi

# ② H2 数
echo "[2/6] H2 章节数"
if [[ "$H2" -gt 7 ]]; then err "H2=$H2 > 7（拆碎充结构）"; else ok "H2=$H2 ≤ 7"; fi

# ③ FAQ 数
echo "[3/6] FAQ 条数"
if [[ "$FAQ" -gt 0 && "$QH" -gt 5 ]]; then err "问答式标题 $QH > 5（FAQ 超量）"; else ok "问答式标题 $QH"; fi

# ④ 重复句/重复段落（去重后行数对比）
echo "[4/6] 重复句/段落"
DUP=$(python3 - "$FILE" << 'PY'
import re,sys
lines=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip() and not l.strip().startswith(("#","|","-","*",">"))]
seen={}; dup=0
for l in lines:
    k=re.sub(r"\s+","",l)[:60]
    if len(k)>=18:
        seen[k]=seen.get(k,0)+1
        if seen[k]==2: dup+=1
print(dup)
PY
)
if [[ "$DUP" -gt 2 ]]; then err "重复句/段 $DUP 处（同一观点写了两遍）"; elif [[ "$DUP" -gt 0 ]]; then warn "重复句/段 $DUP 处"; else ok "无重复句段"; fi

# ⑤ 列表灌水（连续列表块 / 列表总块）
echo "[5/6] 列表灌水"
LISTRUN=$(awk 'BEGIN{run=0;max=0} /^[-*] /{run++; if(run>max)max=run; next} {run=0} END{print max+0}' "$FILE")
if [[ "$LISTRUN" -gt 12 ]]; then err "连续列表项 $LISTRUN > 12（把段落改成清单充数）"; else ok "连续列表项 $LISTRUN"; fi

# ⑥ 模板过渡词 / 无信息量形容词堆叠
echo "[6/6] 模板过渡词与空话"
TRANS=$(grep -oE '(首先|其次|然后|最后|综上所述|由此可见|值得注意的是)' "$FILE" | wc -l | tr -d ' ' || true)
if [[ "$TRANS" -ge 6 ]]; then err "模板过渡词 $TRANS 次（≥6，注水）"; elif [[ "$TRANS" -ge 4 ]]; then warn "模板过渡词 $TRANS 次"; else ok "模板过渡词 $TRANS 次"; fi
FLUFF=$(grep -ciE '(强大而灵活|高效且智能|全面且专业|赋能|闭环|革命性)' "$FILE" || true)
[[ "$FLUFF" -gt 1 ]] && warn "无信息量修饰 $FLUFF 处" || ok "无信息量修饰"

echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then echo "VERDICT: BLOCK (${#ERRORS[@]} errors, ${#WARNINGS[@]} warnings)"; exit 1; fi
echo "VERDICT: PASS (${#WARNINGS[@]} warnings)"; exit 0
