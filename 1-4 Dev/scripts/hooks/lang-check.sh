#!/usr/bin/env bash
# lang-check.sh — RULES-80 多语言规范（硬门禁）
#
# 检查：① 简繁混用 ② 日文简体字混入 ③ 标点规范 ④ 语言残留（正文混其他语言常用词）
# Exit: 0=PASS / 1=BLOCK / 2=engine error
#
# Usage: bash lang-check.sh --file x.md --lang zh|zh-TW|ja|ko|de|fr|pt|ru|it|en
set -euo pipefail

FILE=""; LANG="zh"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --file) FILE="$2"; shift 2;;
    --lang) LANG="$2"; shift 2;;
    -h|--help) sed -n '2,10p' "$0"; exit 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[[ -z "$FILE" || ! -f "$FILE" ]] && { echo "[err] --file required" >&2; exit 2; }

PY3="${LOVART_PYTHON:-}"
if [[ -z "$PY3" ]]; then
  ROOT_ABS="$(cd "$(dirname "$0")/../../.." && pwd)"
  if [[ -x "$ROOT_ABS/.venv/bin/python" ]]; then PY3="$ROOT_ABS/.venv/bin/python"; else PY3="$(command -v python3 || echo python3)"; fi
fi

ERRORS=(); WARNINGS=()
ok()   { echo "  ✓ $*"; }
warn() { WARNINGS+=("$*"); echo "  ! $*"; }
err()  { ERRORS+=("$*");   echo "  ✗ $*"; }

echo "[lang-check] file=$FILE lang=$LANG"

# 只取正文（跳过 frontmatter 与代码块）
BODY="$("$PY3" - "$FILE" << 'PY'
import re,sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
t=open(sys.argv[1],encoding="utf-8").read()
if t.startswith("---"):
    p=t.split("---",2); t=p[2] if len(p)>=3 else t
t=re.sub(r"```[\s\S]*?```","",t)
print(t)
PY
)"

has() { printf '%s' "$BODY" | grep -qE "$1"; }
count() { printf '%s' "$BODY" | grep -oE "$1" | wc -l | tr -d ' ' || true; }

# ① 简体/繁体混用
echo "[1/4] 简繁/字形一致"
if [[ "$LANG" == "zh-TW" ]]; then
  SIMP=$(printf '%s' "$BODY" | grep -oE '(设|内|这|个|为|说|时|后|发|现|体|样|种|关|开|间|电|话|让|请|点|理|师|习|级|总|结|视|频|软|件|团|队|网|页|览|图|标|签|语|义|优|势|风|险|额|费|价|值|营|销|广|告|产|业|务)' | wc -l | tr -d ' ' || true)
  if [[ "$SIMP" -gt 0 ]]; then err "zh-TW 混入简体字 $SIMP 处（如含例外词请人工确认）"; else ok "未检出简体字"; fi
elif [[ "$LANG" == "zh" ]]; then
  TRAD=$(count '們|這|時|後|為|說|體|圖|標|籤|語|價|營|銷|廣|產|務|讓|請|點|習|級|總|結|視|頻|軟|團|隊|網|頁')
  if [[ "$TRAD" -gt 2 ]]; then warn "zh 中出现繁体字 $TRAD 处（可能混源）"; else ok "无繁体混用"; fi
else
  ok "非中文，跳过简繁检查"
fi

# ② 日文简体字混入（简体字形在日文里不存在或写法不同）
echo "[2/4] 语言专属字形"
if [[ "$LANG" == "ja" ]]; then
  CN=$(printf '%s' "$BODY" | grep -oE '(请|让|说|这|个|为|时|后|发|现|体|种|关|开|间|电|话|习|级|总|结|视|频|软|团|队|网|页|图|标|语|价|营|销|广|产|务)' | wc -l | tr -d ' ' || true)
  if [[ "$CN" -gt 0 ]]; then err "ja 正文混入简体中文字形 $CN 处"; else ok "未检出简体中文字形"; fi
fi
if [[ "$LANG" == "ru" ]]; then
  L=$(count '[A-Za-z]')
  if [[ "$L > 40" ]]; then warn "俄语正文含拉丁字母 $L 个（检查是否未本地化的英文残留）"; else ok "拉丁残留可控"; fi
fi

# ③ 标点规范
echo "[3/4] 标点规范"
if [[ "$LANG" == "zh" || "$LANG" == "zh-TW" || "$LANG" == "ja" || "$LANG" == "ko" ]]; then
  HALF=$(printf '%s' "$BODY" | grep -oE '[a-zA-Z0-9\u4e00-\u9fff],|[a-zA-Z0-9\u4e00-\u9fff]\.' | wc -l | tr -d ' ' || true)
  if [[ "$HALF" -gt 3 ]]; then warn "中日韩文本中疑似半角标点 $HALF 处"; else ok "标点规范"; fi
fi
if [[ "$LANG" == "en" ]]; then
  CJK_P=$(printf '%s' "$BODY" | grep -oE '[，。！？、；：]' | wc -l | tr -d ' ' || true)
  if [[ "$CJK_P" -gt 0 ]]; then err "英文正文含中文标点 $CJK_P 处"; else ok "英文标点规范"; fi
  CJK=$(printf '%s' "$BODY" | grep -oE '[\u4e00-\u9fff]' | wc -l | tr -d ' ' || true)
  if [[ "$CJK" -gt 20 ]]; then warn "英文正文含汉字 $CJK 个（疑似未翻译）"; else ok "无未翻译残留"; fi
fi

# ④ 语言残留（CJK 文档里出现整句英文以外的常见外文虚词）
echo "[4/4] 语言残留"
if [[ "$LANG" == "zh" || "$LANG" == "zh-TW" ]]; then
  EN_WORDS=$(printf '%s' "$BODY" | grep -oE '\b(the|and|with|your|from|that|this|for)\b' | wc -l | tr -d ' ' || true)
  if [[ "$EN_WORDS" -gt 5 ]]; then warn "中文正文含英文虚词 $EN_WORDS 处（检查未翻译片段）"; else ok "无未翻译片段"; fi
fi

echo ""
if [[ ${#ERRORS[@]} -gt 0 ]]; then echo "VERDICT: BLOCK (${#ERRORS[@]} errors, ${#WARNINGS[@]} warnings)"; exit 1; fi
echo "VERDICT: PASS (${#WARNINGS[@]} warnings)"; exit 0
