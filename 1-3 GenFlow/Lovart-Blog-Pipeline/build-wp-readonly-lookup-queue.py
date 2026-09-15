#!/usr/bin/env python3
"""Build a local, read-only WordPress metadata lookup queue.

This script does not call WordPress, read credentials, publish, move, or edit
posts. It only combines the existing reconciliation CSV with local Published
Markdown frontmatter so the remaining online verification can be done
deliberately.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_DIR = ROOT / "03-Published"
DEFAULT_INPUT = ROOT / "wordpress-id-reconciliation-2026-06.csv"
DEFAULT_CSV = ROOT / "wordpress-readonly-lookup-queue-2026-06.csv"
DEFAULT_JSON = ROOT / "wordpress-readonly-lookup-queue-2026-06.json"
DEFAULT_MD = ROOT / "WORDPRESS_READONLY_LOOKUP_QUEUE.md"


def read_frontmatter(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    raw = text[4:end]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def lookup_fields(file_name: str) -> dict[str, str]:
    if not file_name:
        return {}
    path = PUBLISHED_DIR / file_name
    fm = read_frontmatter(path)
    return {
        "local_exists": "yes" if path.is_file() else "no",
        "local_status": fm.get("status", ""),
        "local_wp_status": fm.get("wp_status", ""),
        "local_wp_id": fm.get("wp_id", ""),
        "local_wp_post_id": fm.get("wp_post_id", ""),
        "local_wp_link": fm.get("wp_link", ""),
        "local_publish_date": fm.get("publish_date", ""),
    }


def classify(row: dict[str, str]) -> str:
    if row["kind"] == "possible-old-new-pair":
        return "verify-old-new-pair"
    if row["old_wp_link"]:
        return "lookup-by-link-then-id"
    if row["old_slug"]:
        return "lookup-by-slug"
    return "manual-review"


def build_rows(input_csv: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with input_csv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            old_local = lookup_fields(row.get("old_file", ""))
            new_local = lookup_fields(row.get("new_file", ""))
            out = {
                "kind": row.get("kind", ""),
                "lookup_priority": "",
                "lookup_mode": "",
                "old_file": row.get("old_file", ""),
                "old_slug": row.get("old_slug", ""),
                "old_wp_id": row.get("old_wp_id", ""),
                "old_wp_link": row.get("old_wp_link", ""),
                "old_local_exists": old_local.get("local_exists", ""),
                "old_local_status": old_local.get("local_status", ""),
                "old_local_wp_status": old_local.get("local_wp_status", ""),
                "old_local_wp_post_id": old_local.get("local_wp_post_id", ""),
                "new_file": row.get("new_file", ""),
                "new_slug": row.get("new_slug", ""),
                "new_wp_post_id": row.get("new_wp_post_id", ""),
                "new_wp_link": row.get("new_wp_link", ""),
                "new_local_exists": new_local.get("local_exists", ""),
                "new_local_status": new_local.get("local_status", ""),
                "new_local_wp_status": new_local.get("local_wp_status", ""),
                "match_score": row.get("match_score", ""),
                "safe_next_action": row.get("recommended_action", ""),
            }
            out["lookup_mode"] = classify(row)
            out["lookup_priority"] = "P0" if row.get("kind") == "possible-old-new-pair" else "P1"
            rows.append(out)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["lookup_mode"]] = counts.get(row["lookup_mode"], 0) + 1

    lines = [
        "# WordPress Readonly Lookup Queue",
        "",
        "> Generated from `wordpress-id-reconciliation-2026-06.csv`.",
        "> No network calls, no credentials, no publishing, no file moves.",
        "",
        "## Summary",
        "",
        f"- Total rows: {len(rows)}",
    ]
    for key in sorted(counts):
        lines.append(f"- {key}: {counts[key]}")

    lines.extend(
        [
            "",
            "## Queue",
            "",
            "| priority | mode | old file | old wp id | rewrite file | rewrite post id | action |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        action = re.sub(r"\s+", " ", row["safe_next_action"]).strip()
        lines.append(
            "| {lookup_priority} | {lookup_mode} | `{old_file}` | {old_wp_id} | `{new_file}` | {new_wp_post_id} | {action} |".format(
                action=action,
                **row,
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    rows = build_rows(args.input)
    write_csv(args.csv, rows)
    args.json.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_md(args.md, rows)
    print(f"Rows: {len(rows)}")
    print(f"CSV: {args.csv}")
    print(f"JSON: {args.json}")
    print(f"Markdown: {args.md}")


if __name__ == "__main__":
    main()
