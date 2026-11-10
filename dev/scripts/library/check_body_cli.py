#!/usr/bin/env python3
"""check_body_cli.py FILE LANG — body-language gate for markdown drafts.

Exit 0 = pass, 1 = block, 2 = usage/engine error.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from body_lang import check_body  # noqa: E402


def main():
    if len(sys.argv) < 3:
        print("[body-lang] usage: check_body_cli.py FILE LANG", file=sys.stderr)
        return 2
    path, lang = sys.argv[1], sys.argv[2]
    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        text = parts[2] if len(parts) >= 3 else text
    text = re.sub(r"```[\s\S]*?```", "", text)
    reasons = check_body(lang, [{"type": "body", "text": text}])
    if reasons:
        print("  x body-language reasons: " + ", ".join(reasons))
        return 1
    print("  + body language matches " + lang)
    return 0


if __name__ == "__main__":
    sys.exit(main())
