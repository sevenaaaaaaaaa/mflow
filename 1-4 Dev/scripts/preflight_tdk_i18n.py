#!/usr/bin/env python3
"""preflight_tdk_i18n.py — language ↔ TDK gate for composite JSON / NDJSON / Sanity scan.

Usage:
  python3 preflight_tdk_i18n.py --file path/to/page-zh.json
  python3 preflight_tdk_i18n.py --dir "1-3 GenFlow/Page Gen" --glob "*-ja.json"
  python3 preflight_tdk_i18n.py --ndjson /tmp/import.ndjson --strict
  python3 preflight_tdk_i18n.py --sanity --lang zh,ja,ko --limit 500

Exit: 0 pass, 1 BLOCK, 2 usage error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HAN = re.compile(r"[\u4e00-\u9fff]")
JA = re.compile(r"[\u3040-\u30ff]")
KO = re.compile(r"[\uac00-\ud7af]")
RU = re.compile(r"[\u0400-\u04FF]")
LATIN = re.compile(r"[A-Za-z]")
LANG_TAG = re.compile(r"^\[(IT|PT|FR|DE|JA|KO|RU|ZH|EN)\]\s*", re.I)
# Full boiler: EN shell on non-English pages (keep aggressive).
EN_BOILER = re.compile(
    r"\b(Create professional|with Lovart'?s AI Design Agent|Professional Design Tool|"
    r"Design Tool \| Lovart|in seconds with|Free to Try|from Text)\b",
    re.I,
)
# EN pages: only true slug-dump / product-shell templates — not "from text" / "in seconds with".
EN_PAGE_BOILER = re.compile(
    r"\b(Create professional|Professional Design Tool|Design Tool \| Lovart)\b",
    re.I,
)
SLUG_TC = re.compile(r"^Ai [A-Z][a-z]+( [A-Za-z0-9/-]+){1,10}\s*\|\s*Lovart\s*$")
SYNTH_SHELL = re.compile(
    r"｜Lovart AI 设计工具\s*$|｜Lovart AI 設計工具\s*$|"
    r"^Lovartの.+｜AIでプロ品質|"
    r"\|\s*Lovart AI로 전문 디자인\s*$|"
    r"\sс ИИ \| Lovart\s*$|"
    r"用 Lovart AI 设计代理，为「|用 Lovart AI 設計代理，為「|"
    r"LovartのAIデザインエージェントで「|Lovart AI 디자인 에이전트로|"
    r"Создавайте профессиональные материалы для «|"
    r"Créez des résultats professionnels pour|"
    r"Crea risultati professionali per|"
    r"Crie resultados profissionais para|"
    r"Erstellen Sie mit Lovarts KI-Design-Agenten professionelle Ergebnisse"
)


def as_str(v) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return " ".join(str(x) for x in v if x)
    return ""


def title_reasons(lang: str, text: str) -> list[str]:
    t = as_str(text).strip()
    if not t:
        return ["empty"]
    reasons = []
    if LANG_TAG.search(t):
        reasons.append("lang_tag_prefix")
    if SYNTH_SHELL.search(t):
        reasons.append("synth_shell")
    has_han, has_ja, has_ko, has_ru = bool(HAN.search(t)), bool(JA.search(t)), bool(KO.search(t)), bool(RU.search(t))
    has_latin = bool(LATIN.search(t))
    en_boiler = bool(EN_BOILER.search(t) or t.lower().startswith("create professional"))
    if lang == "en":
        if has_han or has_ja or has_ko or has_ru:
            reasons.append("wrong_script")
        return reasons
    if lang in ("de", "fr", "it", "pt"):
        if has_han or has_ja or has_ko or has_ru:
            reasons.append("wrong_script")
        if en_boiler:
            reasons.append("en_boilerplate")
        if SLUG_TC.match(t):
            reasons.append("slug_title_case_en")
    elif lang == "ja":
        # Kanji-only titles are valid Japanese; require CJK or kana.
        if has_ko or has_ru:
            reasons.append("wrong_script")
        if not has_ja and not has_han and has_latin:
            reasons.append("latin_only")
    elif lang == "ko":
        if has_han or has_ja or has_ru:
            reasons.append("wrong_script")
        if not has_ko and has_latin:
            reasons.append("latin_only")
    elif lang == "ru":
        if has_han or has_ja or has_ko:
            reasons.append("wrong_script")
        if not has_ru and has_latin:
            reasons.append("no_cyrillic")
    elif lang in ("zh", "zh-TW"):
        if has_ja or has_ko or has_ru:
            reasons.append("wrong_script")
        if not has_han and has_latin:
            reasons.append("latin_only")
    return reasons


def desc_reasons(lang: str, text: str, allow_empty: bool = True) -> list[str]:
    t = as_str(text).strip()
    if not t:
        return [] if allow_empty else ["empty"]
    reasons = []
    # A script-aligned sentence can still be unusably thin. Keep a lower
    # information floor by writing system; this is a gate, not a word-count
    # target for padding.
    min_len = {
        "en": 120,
        "de": 120,
        "fr": 120,
        "it": 120,
        "pt": 120,
        "ru": 120,
        "ja": 90,
        "ko": 90,
        "zh": 80,
        "zh-TW": 80,
    }.get(lang, 120)
    if len(t) < min_len:
        reasons.append("too_short")
    if SYNTH_SHELL.search(t):
        reasons.append("synth_shell")
    has_han, has_ja, has_ko, has_ru = bool(HAN.search(t)), bool(JA.search(t)), bool(KO.search(t)), bool(RU.search(t))
    has_latin = bool(LATIN.search(t))
    if lang == "en":
        # EN pages: block slug-dump templates only (not legitimate "from text" copy).
        if EN_PAGE_BOILER.search(t) or t.lower().startswith("create professional"):
            reasons.append("en_boilerplate")
        if has_han or has_ja or has_ko or has_ru:
            reasons.append("wrong_script")
        return reasons
    if EN_BOILER.search(t) or t.lower().startswith("create professional"):
        reasons.append("en_boilerplate")
    if lang in ("de", "fr", "it", "pt"):
        if has_han or has_ja or has_ko or has_ru:
            reasons.append("wrong_script")
    elif lang == "ja":
        if has_ko or has_ru:
            reasons.append("wrong_script")
        if not has_ja and not has_han and has_latin and len(t) > 40:
            reasons.append("latin_only")
    elif lang == "ko":
        if has_han or has_ja or has_ru:
            reasons.append("wrong_script")
        if not has_ko and has_latin and len(t) > 40:
            reasons.append("latin_only")
    elif lang == "ru":
        if has_han or has_ja or has_ko:
            reasons.append("wrong_script")
        if not has_ru and has_latin and len(t) > 40:
            reasons.append("no_cyrillic")
    elif lang in ("zh", "zh-TW"):
        if has_ja or has_ko or has_ru:
            reasons.append("wrong_script")
        if not has_han and has_latin and len(t) > 40:
            reasons.append("latin_only")
    return reasons


def check_page(page: dict, strict: bool = False) -> list[dict]:
    lang = page.get("language") or "en"
    seo = page.get("seo") or {}
    issues = []
    checks = [
        ("title", page.get("title"), "title"),
        ("seo.title", seo.get("title"), "title"),
        ("description", page.get("description"), "desc"),
        ("seo.description", seo.get("description"), "desc"),
    ]
    for field, value, kind in checks:
        reasons = (
            title_reasons(lang, value)
            if kind == "title"
            else desc_reasons(lang, value, allow_empty=not strict)
        )
        if not reasons:
            continue
        code = "TDK_I18N_TITLE" if kind == "title" else ("TDK_I18N_EMPTY" if "empty" in reasons else "TDK_I18N_DESC")
        sev = "WARN" if ("empty" in reasons and not strict) else "BLOCK"
        issues.append(
            {
                "code": code,
                "severity": sev,
                "field": field,
                "language": lang,
                "reasons": reasons,
                "sample": as_str(value)[:100],
                "id": page.get("_id") or page.get("slug"),
            }
        )
    return issues


def iter_json_files(dir_path: Path, glob_pat: str):
    yield from sorted(dir_path.rglob(glob_pat))


def load_ndjson(path: Path):
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            yield i, json.loads(line)
        except json.JSONDecodeError as e:
            yield i, {"_parse_error": str(e), "language": "en"}


def sanity_scan(langs: list[str] | None, limit: int | None):
    cfg = json.loads((Path.home() / ".config/sanity/config.json").read_text())
    token = cfg["authToken"]
    lang_filter = f' && language in {json.dumps(langs)}' if langs else ""
    q = f'''*[_type=="compositePage" && defined(language) && !(_id in path("drafts.**")){lang_filter}]{{
      _id, language, title, description, "slug": slug.current,
      "seo": {{"title": seo.title, "description": seo.description}}
    }}'''
    if limit:
        q = q + f"[0...{int(limit)}]"
    url = f"https://o11tm2qe.api.sanity.io/v2024-01-01/data/query/production?query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode())["result"]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="language ↔ TDK preflight gate")
    ap.add_argument("--file")
    ap.add_argument("--dir")
    ap.add_argument("--glob", default="*.json")
    ap.add_argument("--ndjson")
    ap.add_argument("--sanity", action="store_true")
    ap.add_argument("--lang", default="", help="comma langs for --sanity")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--report")
    args = ap.parse_args(argv)

    pages: list[tuple[str, dict]] = []
    if args.file:
        p = Path(args.file)
        pages.append((str(p), json.loads(p.read_text(encoding="utf-8"))))
    elif args.dir:
        root = Path(args.dir)
        for f in iter_json_files(root, args.glob):
            try:
                pages.append((str(f), json.loads(f.read_text(encoding="utf-8"))))
            except Exception as e:
                pages.append((str(f), {"language": "en", "_parse_error": str(e)}))
    elif args.ndjson:
        for i, doc in load_ndjson(Path(args.ndjson)):
            pages.append((f"ndjson:{i}", doc))
    elif args.sanity:
        langs = [x.strip() for x in args.lang.split(",") if x.strip()] or None
        for doc in sanity_scan(langs, args.limit or None):
            pages.append((doc.get("_id") or "sanity", doc))
    else:
        ap.print_help()
        return 2

    all_issues = []
    for ctx, page in pages:
        if page.get("_parse_error"):
            all_issues.append(
                {"code": "JSON_PARSE", "severity": "BLOCK", "message": page["_parse_error"], "ctx": ctx}
            )
            continue
        for issue in check_page(page, strict=args.strict):
            issue["ctx"] = ctx
            all_issues.append(issue)

    blocks = [i for i in all_issues if i.get("severity") == "BLOCK"]
    warns = [i for i in all_issues if i.get("severity") == "WARN"]
    print(f"TDK_I18N pages={len(pages)} BLOCK={len(blocks)} WARN={len(warns)}")
    for i in blocks[:30]:
        print(f"  BLOCK {i.get('code')} {i.get('ctx')} {i.get('field')} {i.get('reasons')} :: {i.get('sample','')[:60]}")
    if len(blocks) > 30:
        print(f"  ... +{len(blocks)-30} more BLOCKs")
    if args.report:
        Path(args.report).write_text(
            json.dumps({"pages": len(pages), "blocks": len(blocks), "warns": len(warns), "issues": all_issues}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("report", args.report)
    return 1 if blocks else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
