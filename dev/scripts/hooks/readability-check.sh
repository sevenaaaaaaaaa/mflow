#!/usr/bin/env bash
# readability-check.sh — Flesch Reading Ease 评分（EN 内容）
# Exit: 0=ok / 1=BLOCK / 2=engine error
set -euo pipefail
FILE=""; LANG_ARG="en"
while [[ $# -gt 0 ]]; do case "$1" in --file) FILE="$2"; shift 2;; --lang) LANG_ARG="$2"; shift 2;; *) shift;; esac; done
[[ -z "$FILE" || ! -f "$FILE" ]] && { echo "[err] --file required"; exit 2; }
if [[ "$LANG_ARG" != "en" ]]; then echo "[readability] skip (lang=$LANG_ARG, only EN scored)"; echo "VERDICT: PASS (0 warnings)"; exit 0; fi
python3 - "$FILE" << 'PY'
import re, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except: pass
text = open(sys.argv[1], encoding="utf-8").read()
# 去掉 frontmatter / headings / code
if text.startswith("---"): text = text.split("---",2)[-1] if text.count("---")>=2 else text
text = re.sub(r"^#+ .*", "", text, flags=re.M)
text = re.sub(r"```[\s\S]*?```", "", text)
sentences = re.split(r"[.!?]+", text)
sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
words = re.findall(r"[A-Za-z]+", text)
syllables = sum(max(1, len(re.findall(r"[aeiouAEIOU]", w))) for w in words)
if not sentences or not words:
    print("VERDICT: PASS (0 warnings)"); exit(0)
flesch = 206.835 - 1.015 * (len(words)/len(sentences)) - 1.455 * (syllables/len(words))
print(f"  Flesch Reading Ease: {flesch:.1f}")
if flesch > 12:
    print("  ✗ Flesch grade level > 12 — 内容过复杂，AI 引擎不偏好")
    print(f"\nVERDICT: BLOCK (1 errors, 0 warnings)"); exit(1)
else:
    print(f"  ✓ Flesch={flesch:.1f} ≤ 12 (target ≤12)")
    print("\nVERDICT: PASS (0 warnings)")
PY
