#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lovart Harness Auto-Optimizer Data Gatherer & Self-Optimizer (harness_auto_optimize.py)
-------------------------------------------------------------------------------------
This script runs daily to collect feedback and autonomously optimize Harness rules:
1. It analyzes git diffs of content files (.md, .json) over the last 24 hours to capture user manual edits.
2. It gathers recent preflight/linter warning logs.
3. It compiles these insights into a structured "Daily Learning Report" under `1-2 Insight/Harness-Learning/`.
4. It autonomously parses deleted text in git diffs to identify new potential AI-slop / banned phrases,
   automatically appends them to the master rules (RULES-30-quality.md), and triggers harness_sync.py.

Usage:
    python3 harness_auto_optimize.py                                    # daily gather mode
    python3 harness_auto_optimize.py --register-template-phrase "..."  # manual register (RULES-20 v1.1 §Banned Template-Phrase Registry)
    python3 harness_auto_optimize.py --register-template-phrase "..." --rules 20  # alternate target rule file
    python3 harness_auto_optimize.py --list-template-phrases             # list current registry
"""

import os
import subprocess
import sys
import re
from datetime import datetime

# Define Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
LEARNING_DIR = os.path.join(PROJECT_ROOT, "1-2 Insight/Harness-Learning")
QUALITY_RULES_PATH = os.path.join(PROJECT_ROOT, "1-1 Harness/02-rules/RULES-30-quality.md")
SYNC_SCRIPT_PATH = os.path.join(PROJECT_ROOT, "1-4 Dev/scripts/harness_sync.py")

os.makedirs(LEARNING_DIR, exist_ok=True)

def run_cmd(cmd, cwd=PROJECT_ROOT, warn=True):
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if warn:
            print(f"Warning running command {' '.join(cmd)}: {e.stderr}", file=sys.stderr)
        return ""

def is_git_repo():
    return run_cmd(["git", "rev-parse", "--is-inside-work-tree"], warn=False) == "true"

def get_recent_git_diffs():
    print("Analyzing recent git diffs for content changes...")
    modified_files = []

    if not is_git_repo():
        print("SKIP git diff learning: workspace is not a git repository.")
        return {}
    
    # Get list of modified files in the last 1 day
    files_str = run_cmd(["git", "log", "--since=1 day ago", "--name-only", "--oneline"], warn=False)
    if not files_str:
        # Fallback: check unstaged/staged changes or last commit
        files_str = run_cmd(["git", "diff", "--name-only", "HEAD~1"], warn=False)
        
    for line in files_str.split("\n"):
        parts = line.strip().split(" ")
        if len(parts) > 1 and len(parts[0]) == 7: # likely a short hash
            file_path = " ".join(parts[1:])
        else:
            file_path = line.strip()
            
        if not file_path:
            continue
            
        # Filter for content files
        if (file_path.endswith(".md") or file_path.endswith(".json")) and \
           ("Sanity Blog" in file_path or "GenFlow" in file_path or "Content Strategy" in file_path):
            if file_path not in modified_files and os.path.exists(os.path.join(PROJECT_ROOT, file_path)):
                modified_files.append(file_path)
                
    diffs = {}
    for f in modified_files:
        diff_content = run_cmd(["git", "diff", "HEAD~1", "--", f], warn=False)
        if not diff_content:
            diff_content = run_cmd(["git", "diff", "--", f], warn=False) # check unstaged
        if diff_content:
            diffs[f] = diff_content
            
    return diffs

def gather_preflight_logs():
    print("Gathering preflight/linter logs...")
    temp_log_path = os.path.expanduser("~/Documents/Lovart Local Dev/Temp/preflight-failures.log")
    if os.path.exists(temp_log_path):
        with open(temp_log_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "No preflight failures logged in the last 24 hours."

def extract_deleted_words(diffs):
    """
    Autonomously scan git diffs for words/phrases deleted by the user.
    If a word is deleted and replaced with a simpler word, it's a candidate for Banned Phrases.
    """
    deleted_candidates = set()
    # Simple regex to find deleted lines in diff starting with '-' but not '--'
    for file_path, diff in diffs.items():
        for line in diff.split("\n"):
            if line.startswith("-") and not line.startswith("---"):
                deleted_text = line[1:].strip()
                # Find common AI slop patterns (e.g., "delve into", "testament to", "revolutionize")
                # We can look for specific keywords or short phrases
                matches = re.findall(r'\b(delve|testament|revolutionize|streamline|leverage|unlock|empower|seamless|seamlessly|unprecedented|pave the way|foster|tapestry|beacon|realm|journey|赋能|闭环|抓手|链路|底层逻辑|方法论|心智|对齐|颗粒度|打法|痛点|破局|深挖|见证|颠覆性|前沿)\b', deleted_text, re.IGNORECASE)
                for m in matches:
                    deleted_candidates.add(m.lower())
    return sorted(list(deleted_candidates))

def autonomously_optimize_rules(new_banned_words):
    if not new_banned_words:
        print("No new banned phrases detected for auto-optimization.")
        return False
        
    print(f"Autonomously optimizing RULES-30-quality.md with new banned words: {new_banned_words}")
    
    if not os.path.exists(QUALITY_RULES_PATH):
        print(f"Error: Quality rules file not found at {QUALITY_RULES_PATH}", file=sys.stderr)
        return False
        
    with open(QUALITY_RULES_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    def append_to_block(text, start_marker, end_marker, words):
        start = text.find(start_marker)
        end = text.find(end_marker)
        if start == -1 or end == -1 or end < start:
            print(f"Warning: banned phrase block markers missing: {start_marker}", file=sys.stderr)
            return text, False

        block = text[start + len(start_marker):end]
        additions = []
        for word in words:
            if f"`{word}`" not in block:
                additions.append(f"- `{word}`")

        if not additions:
            return text, False

        new_block = block.rstrip() + "\n" + "\n".join(additions) + "\n"
        return text[:start + len(start_marker)] + new_block + text[end:], True

    new_content = content
    modified = False

    en_new = [w for w in new_banned_words if not re.match(r'[\u4e00-\u9fff]', w)]
    zh_new = [w for w in new_banned_words if re.match(r'[\u4e00-\u9fff]', w)]

    new_content, en_modified = append_to_block(
        new_content,
        "<!-- HARNESS_BANNED_EN_START -->",
        "<!-- HARNESS_BANNED_EN_END -->",
        en_new,
    )
    new_content, zh_modified = append_to_block(
        new_content,
        "<!-- HARNESS_BANNED_ZH_START -->",
        "<!-- HARNESS_BANNED_ZH_END -->",
        zh_new,
    )
    modified = en_modified or zh_modified

    if en_modified:
        print(f"✓ Autonomously appended English banned phrases: {en_new}")
    if zh_modified:
        print(f"✓ Autonomously appended Chinese banned phrases: {zh_new}")
                
    if modified:
        with open(QUALITY_RULES_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✓ Master quality rules updated autonomously.")
        
        # Trigger sync to propagate to all clients
        if os.path.exists(SYNC_SCRIPT_PATH):
            print("Triggering full-end synchronization...")
            run_cmd(["python3", SYNC_SCRIPT_PATH])
        return True
        
    return False

def register_template_phrase(phrase: str, rules_target: str = "20"):
    """Manually register a banned template phrase to RULES-{NN} (default 20)."""
    if not phrase or not phrase.strip():
        print("Error: phrase cannot be empty.", file=sys.stderr)
        sys.exit(2)

    rules_files = {
        "20": os.path.join(PROJECT_ROOT, "1-1 Harness/02-rules/RULES-20-creation.md"),
        "30": os.path.join(PROJECT_ROOT, "1-1 Harness/02-rules/RULES-30-quality.md"),
    }
    target_path = rules_files.get(rules_target)
    if not target_path or not os.path.exists(target_path):
        print(f"Error: rules file for {rules_target} not found at {target_path}", file=sys.stderr)
        sys.exit(2)

    start_marker = "<!-- HARNESS_BANNED_TEMPLATE_START -->"
    end_marker = "<!-- HARNESS_BANNED_TEMPLATE_END -->"

    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(start_marker)
    end = content.find(end_marker)
    if start == -1 or end == -1 or end < start:
        print(f"Error: HARNESS_BANNED_TEMPLATE markers not found in {target_path}", file=sys.stderr)
        sys.exit(2)

    block = content[start + len(start_marker):end]
    if f"`{phrase}`" in block:
        print(f"Phrase already in registry: `{phrase}`")
        return False

    additions = f"- `{phrase}`\n"
    new_block = block.rstrip() + "\n" + additions
    new_content = content[:start + len(start_marker)] + new_block + content[end:]

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Registered banned template phrase in RULES-{rules_target}.md: `{phrase}`")
    print(f"  ({len(block.splitlines())} existing + 1 new = {len(block.splitlines())+1} total)")
    return True


def list_template_phrases():
    """List the current registered banned template phrases."""
    rules_20_path = os.path.join(PROJECT_ROOT, "1-1 Harness/02-rules/RULES-20-creation.md")
    if not os.path.exists(rules_20_path):
        print(f"Error: RULES-20 not found at {rules_20_path}", file=sys.stderr)
        sys.exit(2)

    with open(rules_20_path, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find("<!-- HARNESS_BANNED_TEMPLATE_START -->")
    end = content.find("<!-- HARNESS_BANNED_TEMPLATE_END -->")
    if start == -1 or end == -1:
        print("Error: markers not found", file=sys.stderr)
        sys.exit(2)

    block = content[start:end]
    phrases = re.findall(r'^- `(.+)`$', block, re.MULTILINE)
    print(f"Current RULES-20 Banned Template-Phrase Registry ({len(phrases)} entries):")
    for i, p in enumerate(phrases, 1):
        print(f"  {i:2d}. {p}")
    return phrases


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Harness self-optimizer")
    parser.add_argument("--register-template-phrase", type=str, help="Manually register a banned template phrase")
    parser.add_argument("--rules", type=str, default="20", help="Target rule file (default: 20 for RULES-20)")
    parser.add_argument("--list-template-phrases", action="store_true", help="List current banned template phrases")
    args = parser.parse_args()

    if args.list_template_phrases:
        list_template_phrases()
        sys.exit(0)
    if args.register_template_phrase is not None:
        register_template_phrase(args.register_template_phrase, args.rules)
        sys.exit(0)

    # Default: daily gather mode
    stamp = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(LEARNING_DIR, f"daily-learning-{stamp}.md")
    
    print(f"Generating Daily Learning Report for {stamp}...")
    
    diffs = get_recent_git_diffs()
    preflight_logs = gather_preflight_logs()
    new_banned_words = extract_deleted_words(diffs)
    
    # Run autonomous optimization
    rules_optimized = autonomously_optimize_rules(new_banned_words)
    
    report_content = f"""# Lovart Harness Daily Learning Report — {stamp}

> This report is automatically generated to feed back into the Harness Self-Optimization Loop.
> It captures user manual edits (git diffs) and preflight quality gate failures from the last 24 hours.

---

## 1. User Style & Aesthetic Diffs (Git Diffs)

Below are the manual edits made by the user to AI-generated content. 
*Agent Instructions: Analyze these diffs. If the user consistently removes certain words, they should be added to the Banned Phrases list. If they expand sections or rewrite structures, update the writing playbooks accordingly.*

"""
    if not diffs:
        report_content += "No manual content edits detected in the last 24 hours.\n\n"
    else:
        for file_path, diff in diffs.items():
            report_content += f"### File: `{file_path}`\n\n"
            report_content += "```diff\n"
            report_content += diff + "\n"
            report_content += "```\n\n"
            
    report_content += f"""## 2. Preflight Quality Gate Failures

Below are the quality gate warnings or blocks triggered during content validation:

```text
{preflight_logs}
```

---

## 3. Autonomous Self-Optimization Actions Taken

- **New Banned Phrases Detected**: {new_banned_words if new_banned_words else "None"}
- **Harness Rules Auto-Updated & Synced**: {"Yes (RULES-30-quality.md updated & compiled to all clients)" if rules_optimized else "No (No new patterns to update or already exists)"}

---

## 4. Recommended Manual Optimization Actions for Agent

Based on the above data, the Agent should:
1. **Style Adjustments**: If the user manually corrected formatting, dates, or metadata, update `1-1 Harness/02-rules/RULES-20-creation.md` to prevent these configuration errors.
2. **Trigger Sync**: After making any manual adjustments to master rules, run `python3 "1-4 Dev/scripts/harness_sync.py"` to compile and propagate the changes to all clients (Cursor, Claude Code, Codex, Hermes).
"""
    
    write_file_success = False
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        write_file_success = True
        print(f"✓ Daily Learning Report written to: {os.path.relpath(report_path, PROJECT_ROOT)}")
    except Exception as e:
        print(f"Error writing learning report: {e}", file=sys.stderr)
        
    if write_file_success:
        print("🎉 Gatherer & Auto-Optimizer complete. Harness self-optimization feedback loop is active.")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

