#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Select list-copy audit candidates: first 30 in listing UNION top 30 by traffic.

Inputs are exports, not live CMS credentials:
  pages.jsonl: one JSON object per page with id/_id, page_type/pageType/category,
               language, slug, title, description, and listing_rank/listRank.
  traffic.csv: doc_id plus impressions and optional clicks. If doc_id is absent,
               page_type, language and slug are used as a composite key.

Outputs:
  candidates.jsonl  -- one record per selected page, with selection source and flags
  summary.json      -- counts by page type and language
"""
from __future__ import print_function

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict


def text(value):
    return str(value or "").strip()


def page_id(row):
    return text(row.get("doc_id") or row.get("_id") or row.get("id"))


def page_type(row):
    return text(row.get("page_type") or row.get("pageType") or row.get("category") or "unknown")


def language(row):
    return text(row.get("language") or "en")


def slug(row):
    value = row.get("slug")
    if isinstance(value, dict):
        value = value.get("current")
    return text(value)


def composite_key(row):
    return "|".join([page_type(row), language(row), slug(row)])


def number(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def rank(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 10 ** 12


def is_cjk(value):
    return bool(re.search(u"[\u3040-\u30ff\u3400-\u9fff\ua960-\ua97f\uac00-\ud7af]", value))


def normalize(value):
    value = text(value).lower()
    return re.sub(r"[^a-z0-9\u3040-\u30ff\u3400-\u9fff\ua960-\ua97f\uac00-\ud7af]+", "", value)


def quality_flags(row, selected_group):
    title = text(row.get("title"))
    description = text(row.get("description") or row.get("seoDescription"))
    flags = []
    if row.get("listing_rank") is not None and not text(row.get("listing_card_text")):
        flags.append("LIST_CARD_TEXT_MISSING_OR_UNVERIFIED")
    if not title:
        flags.append("LIST_TITLE_MISSING")
    if not description:
        flags.append("LIST_DESCRIPTION_MISSING")
    title_norm = normalize(title)
    desc_norm = normalize(description)
    slug_norm = normalize(slug(row).replace("-", " "))
    if title_norm and slug_norm and title_norm == slug_norm:
        flags.append("LIST_TITLE_MAY_BE_BARE_KEYWORD")
    if title_norm and desc_norm and (desc_norm == title_norm or desc_norm.startswith(title_norm)):
        flags.append("LIST_DESCRIPTION_REPEATS_TITLE")
    if title:
        if is_cjk(title) and len(title) > 35:
            flags.append("LIST_TITLE_REVIEW_FOR_TRUNCATION")
        elif not is_cjk(title) and len(title) > 70:
            flags.append("LIST_TITLE_REVIEW_FOR_TRUNCATION")
    if description:
        if is_cjk(description) and len(description) < 20:
            flags.append("LIST_DESCRIPTION_MAY_BE_TOO_THIN")
        elif not is_cjk(description) and len(description) < 45:
            flags.append("LIST_DESCRIPTION_MAY_BE_TOO_THIN")
        if is_cjk(description) and len(description) > 90:
            flags.append("LIST_DESCRIPTION_REVIEW_FOR_TRUNCATION")
        elif not is_cjk(description) and len(description) > 180:
            flags.append("LIST_DESCRIPTION_REVIEW_FOR_TRUNCATION")

    title_counts = defaultdict(int)
    desc_counts = defaultdict(int)
    for item in selected_group:
        item_title = normalize(item.get("title"))
        item_desc = normalize(item.get("description") or item.get("seoDescription"))
        if item_title:
            title_counts[item_title] += 1
        if item_desc:
            desc_counts[item_desc] += 1
    if title_norm and title_counts[title_norm] > 1:
        flags.append("LIST_TITLE_DUPLICATE_IN_COHORT")
    if desc_norm and desc_counts[desc_norm] > 1:
        flags.append("LIST_DESCRIPTION_DUPLICATE_IN_COHORT")
    return flags


def read_pages(path):
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError as exc:
                raise ValueError("Invalid JSONL at line {0}: {1}".format(line_number, exc))
            if not page_id(row):
                raise ValueError("Missing id/_id/doc_id at pages line {0}".format(line_number))
            rows.append(row)
    return rows


def read_traffic(path):
    by_id = {}
    by_key = {}
    if not path:
        return by_id, by_key
    with open(path, "r", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            payload = {
                "impressions": number(row.get("impressions")),
                "clicks": number(row.get("clicks")),
            }
            if text(row.get("doc_id")):
                by_id[text(row.get("doc_id"))] = payload
            elif text(row.get("page_type")) and text(row.get("language")) and text(row.get("slug")):
                by_key["|".join([text(row["page_type"]), text(row["language"]), text(row["slug"])])] = payload
    return by_id, by_key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", required=True, help="Full CMS page export in JSONL")
    parser.add_argument("--traffic", required=True, help="Traffic export CSV: doc_id,impressions,clicks")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--limit", type=int, default=30, help="Top N per type/language/source")
    args = parser.parse_args()

    pages = read_pages(args.pages)
    traffic_by_id, traffic_by_key = read_traffic(args.traffic)
    groups = defaultdict(list)
    for row in pages:
        metrics = traffic_by_id.get(page_id(row), traffic_by_key.get(composite_key(row), {}))
        item = dict(row)
        item["_page_id"] = page_id(row)
        item["_page_type"] = page_type(row)
        item["_language"] = language(row)
        item["_slug"] = slug(row)
        item["_listing_rank"] = rank(row.get("listing_rank") or row.get("listRank"))
        item["_impressions"] = number(metrics.get("impressions"))
        item["_clicks"] = number(metrics.get("clicks"))
        groups[(item["_page_type"], item["_language"])].append(item)

    os.makedirs(args.out_dir, exist_ok=True)
    candidates = []
    summary = {"limit": args.limit, "groups": []}
    for (kind, lang), rows in sorted(groups.items()):
        # Missing rank means this document was not matched to a public list card.
        # It must never be silently promoted into the "list top" cohort merely
        # because its sentinel rank sorts after real cards.
        listed = sorted(
            (row for row in rows if row["_listing_rank"] < 10 ** 12),
            key=lambda x: (x["_listing_rank"], x["_page_id"]),
        )[:args.limit]
        trafficked = sorted(rows, key=lambda x: (-x["_impressions"], -x["_clicks"], x["_page_id"]))[:args.limit]
        selected = {}
        for item in listed:
            selected.setdefault(item["_page_id"], {"item": item, "sources": []})["sources"].append("list_top")
        for item in trafficked:
            selected.setdefault(item["_page_id"], {"item": item, "sources": []})["sources"].append("traffic_top")
        group_selected = [entry["item"] for entry in selected.values()]
        flagged = 0
        for entry in selected.values():
            item = entry["item"]
            flags = quality_flags(item, group_selected)
            if flags:
                flagged += 1
            candidates.append({
                "doc_id": item["_page_id"],
                "page_type": kind,
                "language": lang,
                "slug": item["_slug"],
                "title": text(item.get("title")),
                "description": text(item.get("description") or item.get("seoDescription")),
                "listing_rank": None if item["_listing_rank"] >= 10 ** 12 else item["_listing_rank"],
                "listing_card_text": text(item.get("listing_card_text")),
                "impressions": item["_impressions"],
                "clicks": item["_clicks"],
                "selected_by": sorted(entry["sources"]),
                "structural_flags": flags,
                "manual_review": "pending"
            })
        summary["groups"].append({
            "page_type": kind,
            "language": lang,
            "pages_available": len(rows),
            "list_top_count": len(listed),
            "traffic_top_count": len(trafficked),
            "union_count": len(selected),
            "flagged_count": flagged
        })

    candidates.sort(key=lambda x: (x["page_type"], x["language"], x["listing_rank"] is None,
                                    x["listing_rank"] or 10 ** 12, -x["impressions"], x["slug"]))
    with open(os.path.join(args.out_dir, "candidates.jsonl"), "w", encoding="utf-8") as handle:
        for item in candidates:
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
    summary["candidate_count"] = len(candidates)
    with open(os.path.join(args.out_dir, "summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print("Selected {0} candidates across {1} type/language groups.".format(
        len(candidates), len(summary["groups"])))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ERROR: {0}".format(exc), file=sys.stderr)
        sys.exit(2)
