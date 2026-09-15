"""
Lovart Sentinel - i18n Keyword Intelligence

Turns daily GSC query exports into locale-specific content production signals.
This is intentionally separate from the English-first SEO workflow so localized
content gets its own demand evidence before translation or net-new page work.
"""
from __future__ import annotations

import csv
import glob
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

from ._common import banner

GSC_DIR = Path(__file__).resolve().parents[4] / "1-2 Insight" / "Keywords Research" / "Daily Raw Data"

TARGET_LOCALES = ("zh", "zh-TW", "ja", "ko", "de", "fr", "ru", "pt", "it")

LOCALE_NAMES = {
    "zh": "简中",
    "zh-TW": "繁中",
    "ja": "日语",
    "ko": "韩语",
    "de": "德语",
    "fr": "法语",
    "ru": "俄语",
    "pt": "葡语",
    "it": "意语",
}

LOCALE_PATTERNS = {
    "ja": re.compile(r"[\u3040-\u30ff]"),
    "ko": re.compile(r"[\uac00-\ud7af]"),
    "ru": re.compile(r"[\u0400-\u04ff]"),
    "zh": re.compile(r"[\u4e00-\u9fff]"),
}

LOCALE_TERMS = {
    "zh": ("中文", "简体", "官网", "生成器", "设计", "视频", "图片", "海报", "字幕", "剪辑"),
    "zh-TW": ("繁體", "台灣", "臺灣", "設計", "影片", "圖片", "海報", "字幕", "剪輯"),
    "de": (" ki ", "künstliche intelligenz", "bildgenerator", "bearbeiten", "plakat", "entfernen"),
    "fr": (" ia ", "vidéo", "générateur", "modifier", "affiche", "supprimer"),
    "pt": (" ia ", "vídeo", "imagem", "gerador", "editar", "cartaz", "remover"),
    "it": (" ia ", "immagine", "generatore", "modifica", "rimuovere"),
}

LANG_PAGE_HINTS = {
    "zh": ("/zh/", "-zh"),
    "zh-TW": ("/zh-tw/", "/zh-TW/", "-zh-TW"),
    "ja": ("/ja/", "-ja"),
    "ko": ("/ko/", "-ko"),
    "de": ("/de/", "-de"),
    "fr": ("/fr/", "-fr"),
    "ru": ("/ru/", "-ru"),
    "pt": ("/pt/", "-pt"),
    "it": ("/it/", "-it"),
}


def _latest_csv(pattern: str) -> Path | None:
    files = sorted(glob.glob(str(GSC_DIR / pattern)))
    return Path(files[-1]) if files else None


def _read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _metric(row: dict, names: tuple[str, ...], default: float = 0.0) -> float:
    for name in names:
        raw = row.get(name)
        if raw in (None, ""):
            continue
        try:
            return float(str(raw).replace(",", "").replace("%", "").strip())
        except ValueError:
            continue
    return default


def _query_text(row: dict) -> str:
    for key in ("热门查询", "搜索查询", "查询", "query", "Query"):
        if row.get(key):
            return str(row[key]).strip()
    return ""


def detect_locale(query: str) -> str | None:
    text = query.strip().lower()
    if not text:
        return None
    if "繁體" in query or "台灣" in query or "臺灣" in query:
        return "zh-TW"
    if LOCALE_PATTERNS["ja"].search(query):
        return "ja"
    if LOCALE_PATTERNS["ko"].search(query):
        return "ko"
    if LOCALE_PATTERNS["ru"].search(query):
        return "ru"
    if LOCALE_PATTERNS["zh"].search(query):
        return "zh"
    padded = f" {text} "
    for locale, terms in LOCALE_TERMS.items():
        if any(term in padded for term in terms):
            return locale
    return None


def infer_locale_from_page(url: str) -> str | None:
    text = str(url)
    for locale, hints in LANG_PAGE_HINTS.items():
        if any(hint in text for hint in hints):
            return locale
    return None


def summarize_queries(rows: list[dict]) -> tuple[dict, list[dict]]:
    buckets: dict[str, dict] = {
        locale: {
            "locale": locale,
            "label": LOCALE_NAMES[locale],
            "query_count": 0,
            "clicks": 0,
            "impressions": 0,
            "top_queries": [],
            "opportunities": [],
        }
        for locale in TARGET_LOCALES
    }
    unmatched = []

    for row in rows:
        query = _query_text(row)
        locale = detect_locale(query)
        clicks = int(_metric(row, ("点击次数", "clicks", "Clicks")))
        impressions = int(_metric(row, ("展示", "展现次数", "印象数", "impressions", "Impressions")))
        ctr = _metric(row, ("点击率", "平均 点击率", "CTR", "ctr"))
        position = _metric(row, ("排名", "平均排名", "Position", "position"))
        entry = {
            "query": query,
            "clicks": clicks,
            "impressions": impressions,
            "ctr": ctr,
            "position": position,
        }
        if not locale:
            unmatched.append(entry)
            continue
        bucket = buckets[locale]
        bucket["query_count"] += 1
        bucket["clicks"] += clicks
        bucket["impressions"] += impressions
        bucket["top_queries"].append(entry)
        if impressions >= 50 and ctr < 3:
            bucket["opportunities"].append(entry)

    for bucket in buckets.values():
        bucket["top_queries"] = sorted(
            bucket["top_queries"], key=lambda item: (item["clicks"], item["impressions"]), reverse=True
        )[:10]
        bucket["opportunities"] = sorted(
            bucket["opportunities"], key=lambda item: item["impressions"], reverse=True
        )[:10]
        bucket["ctr"] = round((bucket["clicks"] / bucket["impressions"] * 100), 2) if bucket["impressions"] else 0
    return buckets, unmatched[:100]


def summarize_pages(rows: list[dict]) -> dict[str, dict]:
    pages = {
        locale: {"locale": locale, "label": LOCALE_NAMES[locale], "pages": 0, "clicks": 0, "impressions": 0}
        for locale in TARGET_LOCALES
    }
    for row in rows:
        url = row.get("网页") or row.get("page") or row.get("Page") or ""
        locale = infer_locale_from_page(url)
        if not locale:
            continue
        clicks = int(_metric(row, ("点击次数", "clicks", "Clicks")))
        impressions = int(_metric(row, ("展示", "展现次数", "印象数", "impressions", "Impressions")))
        pages[locale]["pages"] += 1
        pages[locale]["clicks"] += clicks
        pages[locale]["impressions"] += impressions
    for row in pages.values():
        row["ctr"] = round((row["clicks"] / row["impressions"] * 100), 2) if row["impressions"] else 0
    return pages


def build_content_tasks(query_summary: dict[str, dict], page_summary: dict[str, dict]) -> list[dict]:
    tasks = []
    for locale, bucket in query_summary.items():
        page_stats = page_summary.get(locale, {})
        if bucket["opportunities"]:
            top = bucket["opportunities"][0]
            tasks.append({
                "locale": locale,
                "label": bucket["label"],
                "priority": "P1",
                "task": f"补充 {bucket['label']} 查询意图页或翻译：{top['query']}",
                "evidence": f"{top['impressions']} impressions / CTR {top['ctr']}%",
            })
        elif bucket["query_count"] > 0 and page_stats.get("pages", 0) == 0:
            top = bucket["top_queries"][0]
            tasks.append({
                "locale": locale,
                "label": bucket["label"],
                "priority": "P2",
                "task": f"{bucket['label']} 有查询需求但缺少可识别本地化页面：{top['query']}",
                "evidence": f"{bucket['query_count']} queries / {bucket['impressions']} impressions",
            })
    return tasks[:20]


def collect() -> dict:
    data = dict(banner("i18n Keyword Intelligence"))
    data["date"] = date.today().isoformat()
    query_file = _latest_csv("GSC*/查询数.csv")
    page_file = _latest_csv("GSC*/网页.csv")

    query_rows = _read_csv(query_file) if query_file else []
    page_rows = _read_csv(page_file) if page_file else []
    query_summary, unmatched = summarize_queries(query_rows)
    page_summary = summarize_pages(page_rows)

    data["_queries_file"] = str(query_file.parent.name + "/" + query_file.name) if query_file else None
    data["_pages_file"] = str(page_file.parent.name + "/" + page_file.name) if page_file else None
    data["locales"] = query_summary
    data["localized_pages"] = page_summary
    data["content_tasks"] = build_content_tasks(query_summary, page_summary)
    data["unmatched_sample"] = unmatched
    data["requirements"] = [
        "日报必须按目标 locale 展示查询数、点击、曝光、CTR 与机会词。",
        "i18n 内容生产优先级不得只由英文主工作流决定，必须引用 locale 查询证据。",
        "高曝光低 CTR 的本地语言查询进入翻译/新建页面候选池。",
        "有本地语言查询但缺少可识别本地化页面时，标记为内容缺口。",
    ]
    return data
