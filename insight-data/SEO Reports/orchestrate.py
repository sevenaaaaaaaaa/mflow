#!/usr/bin/env python3
"""
Main orchestration script for batch blog refactoring.
Coordinates: pull → refactor → patch pipeline.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent
EXISTING_DIR = BASE_DIR / "01-existing"
REWRITTEN_DIR = BASE_DIR / "02-rewritten"
PATCHED_DIR = BASE_DIR / "03-patched"

def run_script(script_name, args=None):
    """Run a script and return success status."""
    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path)] + (args or [])
    
    print(f"\n{'='*60}")
    print(f"Running: {script_name} {' '.join(args or [])}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def generate_report():
    """Generate final report of all processed posts."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_posts": 0,
            "successful": 0,
            "failed": 0,
            "total_words": 0,
        },
        "posts": []
    }
    
    # Read all patched manifests
    for manifest_file in sorted(PATCHED_DIR.glob("manifest-batch-*.json")):
        with open(manifest_file, 'r') as f:
            batch_data = json.load(f)
        
        for item in batch_data:
            report["summary"]["total_posts"] += 1
            if item.get("status") == "ok":
                report["summary"]["successful"] += 1
                report["summary"]["total_words"] += item.get("verified_count", 0)
            else:
                report["summary"]["failed"] += 1
            
            report["posts"].append(item)
    
    # Save report
    report_file = BASE_DIR / "REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Batch Refactoring Report\n\n")
        f.write(f"Generated: {report['timestamp']}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Total posts: {report['summary']['total_posts']}\n")
        f.write(f"- Successful: {report['summary']['successful']}\n")
        f.write(f"- Failed: {report['summary']['failed']}\n")
        f.write(f"- Total words: {report['summary']['total_words']:,}\n")
        f.write(f"- Average words: {report['summary']['total_words'] // max(report['summary']['successful'], 1):,}\n\n")
        
        f.write("## Posts\n\n")
        f.write("| Slug | Status | Words | Verified |\n")
        f.write("|------|--------|-------|----------|\n")
        for post in report["posts"]:
            status = "✓" if post.get("status") == "ok" else "✗"
            words = post.get("word_count", 0)
            verified = post.get("verified_count", 0)
            f.write(f"| {post['slug']} | {status} | {words:,} | {verified:,} |\n")
    
    print(f"\nReport saved to: {report_file}")
    return report

def main():
    """Main entry point."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    
    print("="*60)
    print("BATCH BLOG REFACTORING PIPELINE")
    print(f"Mode: {mode}")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*60)
    
    if mode == "test":
        # Test mode: process 3 posts
        print("\n[TEST MODE] Processing 3 posts...")
        
        # Step 1: Pull existing posts
        if not run_script("pull-existing.py", ["0", "3"]):
            print("Failed to pull existing posts")
            return
        
        # Step 2: Refactor content
        if not run_script("refactor.py", ["0", "3"]):
            print("Failed to refactor content")
            return
        
        # Step 3: Patch to Sanity (dry run first)
        print("\n[DRY RUN] Testing patch...")
        if not run_script("patch-sanity.py", ["0", "3", "--dry-run"]):
            print("Dry run failed")
            return
        
        print("\n✓ Dry run successful. Ready for actual patch.")
        print("Run with: python orchestrate.py patch-test")
    
    elif mode == "patch-test":
        # Actually patch the test batch
        print("\n[PATCH TEST] Patching 3 posts...")
        if not run_script("patch-sanity.py", ["0", "3"]):
            print("Failed to patch posts")
            return
        
        print("\n✓ Test batch patched successfully")
        generate_report()
    
    elif mode == "batch":
        # Full batch processing
        batch_num = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        batch_size = 10
        
        print(f"\n[BATCH {batch_num}] Processing posts {batch_num*batch_size} to {(batch_num+1)*batch_size-1}...")
        
        # Step 1: Pull existing posts
        start = batch_num * batch_size
        if not run_script("pull-existing.py", [str(start), str(batch_size)]):
            print("Failed to pull existing posts")
            return
        
        # Step 2: Refactor content
        if not run_script("refactor.py", [str(start), str(batch_size)]):
            print("Failed to refactor content")
            return
        
        # Step 3: Patch to Sanity
        if not run_script("patch-sanity.py", [str(start), str(batch_size)]):
            print("Failed to patch posts")
            return
        
        generate_report()
    
    elif mode == "report":
        # Generate report only
        generate_report()
    
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python orchestrate.py [test|patch-test|batch <num>|report]")

if __name__ == "__main__":
    main()
