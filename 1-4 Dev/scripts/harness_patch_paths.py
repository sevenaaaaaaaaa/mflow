#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit or patch legacy Lovart path aliases.

Default mode is audit-only. Use `--apply` to write replacements.
"""

import argparse
import os
import sys

# Define Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

REPLACEMENTS = {
    "1-4 Geo Dev": "1-4 Dev",
    "1-5 Harness": "1-1 Harness",
}

EXCLUDE_DIRS = {
    ".git",
    ".cursorignore",
    ".venv",
    "node_modules",
    "__pycache__",
    "raw",
    "daily",
    "reports"
}

EXCLUDE_PATH_PARTS = {
    os.path.normpath(".cursor/skills/lovart-core/SKILL.md"),
    os.path.normpath("1-4 Dev/scripts/harness_patch_paths.py"),
    os.path.normpath("1-4 Dev/notion-sync"),
    os.path.normpath("1-3 GenFlow/Page Gen/Pages/drafts"),
}

TEXT_SUFFIXES = (
    ".md", ".json", ".jsonc", ".sh", ".py", ".js", ".ts",
    ".mdc", ".plist", ".yaml", ".yml", ".txt", ".csv",
)

def patch_file(file_path, apply=False):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        matches = [old for old in REPLACEMENTS if old in content]
        if not matches:
            return False

        new_content = content
        for old in matches:
            new_content = new_content.replace(old, REPLACEMENTS[old])

        rel = os.path.relpath(file_path, PROJECT_ROOT)
        if apply:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✓ patched: {rel} ({', '.join(matches)})")
        else:
            print(f"would patch: {rel} ({', '.join(matches)})")
        return True
    except Exception as e:
        print(f"Error patching {file_path}: {e}", file=sys.stderr)
    return False

def should_skip_path(file_path):
    rel = os.path.normpath(os.path.relpath(file_path, PROJECT_ROOT))
    return any(rel == part or rel.startswith(part + os.sep) for part in EXCLUDE_PATH_PARTS)

def main():
    parser = argparse.ArgumentParser(description="Audit or patch legacy Lovart path aliases.")
    parser.add_argument("--apply", action="store_true", help="Write replacements. Default is audit-only.")
    args = parser.parse_args()

    print("==========================================")
    print("Lovart Harness Path Alias Auditor")
    print("==========================================")

    matched_count = 0
    total_scanned = 0

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if not file.endswith(TEXT_SUFFIXES):
                continue
            file_path = os.path.join(root, file)
            if should_skip_path(file_path):
                continue
            total_scanned += 1
            if patch_file(file_path, apply=args.apply):
                matched_count += 1

    print("==========================================")
    print("Path alias scan complete.")
    print(f"Mode: {'apply' if args.apply else 'audit-only'}")
    print(f"Scanned files: {total_scanned}")
    print(f"Matched files: {matched_count}")
    print("==========================================")

if __name__ == "__main__":
    main()
