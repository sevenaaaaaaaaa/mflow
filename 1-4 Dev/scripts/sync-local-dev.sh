#!/usr/bin/env bash
# sync-local-dev.sh — bidirectional sync between Lovart Local Dev and Obsidian vault
#
# Problem: Two folders (Obsidian vault + Lovart Local Dev) hold overlapping content.
#          Files drift apart. No one knows which is latest.
#
# Solution: One-directional SSOT sync with clear rules:
#   - Obsidian vault = SSOT for rules/skills/knowledge/strategies
#   - Local Dev = SSOT for runtime data (sanity dumps, API outputs, caches)
#   - This script syncs NEW files from Local Dev → Obsidian
#   - And archives STALE files from Obsidian → Local Dev/Backup
#
# Usage:
#   bash sync-local-dev.sh              # dry-run (show what would happen)
#   bash sync-local-dev.sh --apply      # actually move files
#   bash sync-local-dev.sh --archive    # archive stale Obsidian files to Local Dev
#
# Cron: weekly (Sunday 03:00) via launchd or Hermes cron

set -euo pipefail

# --- Configuration ---
LOCAL_DEV="${LOVART_LOCAL_DEV_ROOT:-$HOME/Documents/Lovart Local Dev}"
VAULT="${LOVART_RESOURCE_ROOT:-$(cd "${BASH_SOURCE[0]%/*}/../../../.." && pwd)}"
MFLOW="$VAULT/1-Project/Lovart MFlow"

# Mapping: Local Dev path → Obsidian target path
# Format: "local_dev_subdir:obsidian_subdir:file_pattern"
SYNC_MAP=(
  # Root .md files → 1-2 Insight/ (strategies/reports)
  "root_md:1-2 Insight:*.md"
  # Output/SEO-Reports → 1-2 Insight/SEO Reports/
  "Output/SEO-Reports:1-2 Insight/SEO Reports:*"
  # Output/Knowledge Base → 1-2 Insight/Knowledge Base/
  "Output/Knowledge Base:1-2 Insight/Knowledge Base:*"
  # Output/Lovart-Blog-Pipeline → 1-3 GenFlow/Lovart-Blog-Pipeline/
  "Output/Lovart-Blog-Pipeline:1-3 GenFlow/Lovart-Blog-Pipeline:*"
  # Output/Content Calendar → 1-3 GenFlow/Content Calendar/
  "Output/Content Calendar:1-3 GenFlow/Content Calendar:*"
  # Output/Page Gen → 1-3 GenFlow/Page Gen/
  "Output/Page Gen:1-3 GenFlow/Page Gen:*"
  # features/*.json → 1-3 GenFlow/Page Gen/features/
  "features:1-3 GenFlow/Page Gen/features:*.json"
  # tools/*.py → 1-4 Dev/tools/
  "tools:1-4 Dev/tools:*"
  # seo-documents → 1-2 Insight/SEO Reports/sitemap/
  "seo-documents:1-2 Insight/SEO Reports/sitemap:*"
)

# Directories to NEVER sync (runtime data, caches, credentials)
SKIP_DIRS=(".hermes" ".openharness" "Logs" "Temp" "Backup" ".git" "__pycache__" "node_modules")
SKIP_PATTERNS=(".env" ".token_*" "*.pyc" ".DS_Store" "credentials*" "*_credentials*")

# --- Parse args ---
MODE="dry-run"
ARCHIVE_MODE=0
for arg in "$@"; do
  case "$arg" in
    --apply) MODE="apply" ;;
    --archive) ARCHIVE_MODE=1 ;;
    --help|-h)
      echo "Usage: sync-local-dev.sh [--apply] [--archive]"
      echo "  (no args)  dry-run: show what would happen"
      echo "  --apply    actually copy/move files"
      echo "  --archive  archive stale Obsidian files to Local Dev/Backup"
      exit 0
      ;;
  esac
done

# --- Helpers ---
log() { echo "[sync] $*"; }
is_skip_dir() {
  local name="$1"
  for skip in "${SKIP_DIRS[@]}"; do
    [[ "$name" == "$skip" ]] && return 0
  done
  return 1
}
is_skip_file() {
  local name="$1"
  for pat in "${SKIP_PATTERNS[@]}"; do
    # Simple glob match
    case "$name" in
      $pat) return 0 ;;
    esac
  done
  return 1
}

# --- Main ---
log "Mode: $MODE"
log "Local Dev: $LOCAL_DEV"
log "Vault: $VAULT"
log ""

if [[ ! -d "$LOCAL_DEV" ]]; then
  log "ERROR: Local Dev not found at $LOCAL_DEV"
  exit 2
fi
if [[ ! -d "$MFLOW" ]]; then
  log "ERROR: Lovart MFlow not found at $MFLOW"
  exit 2
fi

SYNCED=0
SKIPPED=0
CONFLICTS=0

if [[ "$ARCHIVE_MODE" -eq 1 ]]; then
  # --- Archive mode: move stale Obsidian files to Local Dev/Backup ---
  log "=== Archive mode: moving stale files from Obsidian → Local Dev/Backup ==="
  BACKUP_DIR="$LOCAL_DEV/Backup/$(date +%Y-%m-%d)"
  mkdir -p "$BACKUP_DIR"

  # Find .md files in Obsidian 1-2 Insight/ and 1-3 GenFlow/ that are older than 30 days
  find "$MFLOW/1-2 Insight" "$MFLOW/1-3 GenFlow" -name "*.md" -mtime +30 -type f 2>/dev/null | while read -r f; do
    rel="${f#$MFLOW/}"
    # Don't archive SSOT files (rules, skills, knowledge)
    case "$rel" in
      1-1-Harness/*|AGENTS.md|entities.*|mempalace.*) continue ;;
    esac
    # Don't archive files that also exist in Local Dev (they're the source)
    bn=$(basename "$f")
    if find "$LOCAL_DEV" -name "$bn" -type f 2>/dev/null | head -1 | grep -q .; then
      continue
    fi
    target="$BACKUP_DIR/$(dirname "$rel")"
    mkdir -p "$target"
    if [[ "$MODE" == "apply" ]]; then
      mv "$f" "$target/"
      log "  archived: $rel"
    else
      log "  would archive: $rel"
    fi
    SYNCED=$((SYNCED + 1))
  done
else
  # --- Sync mode: copy new files from Local Dev → Obsidian ---
  log "=== Sync mode: copying new files from Local Dev → Obsidian ==="

  # 1) Root .md files → 1-2 Insight/
  log "--- Root .md → 1-2 Insight/ ---"
  for f in "$LOCAL_DEV"/*.md; do
    [[ -f "$f" ]] || continue
    bn=$(basename "$f")
    is_skip_file "$bn" && { SKIPPED=$((SKIPPED + 1)); continue; }
    target="$MFLOW/1-2 Insight/$bn"
    if [[ -f "$target" ]]; then
      # Compare modification time
      if [[ "$f" -nt "$target" ]]; then
        log "  newer: $bn (Local Dev is newer)"
        if [[ "$MODE" == "apply" ]]; then
          cp "$f" "$target"
          log "  updated: $bn"
        else
          log "  would update: $bn"
        fi
        SYNCED=$((SYNCED + 1))
      else
        SKIPPED=$((SKIPPED + 1))
      fi
    else
      log "  new: $bn"
      if [[ "$MODE" == "apply" ]]; then
        cp "$f" "$target"
        log "  copied: $bn"
      else
        log "  would copy: $bn"
      fi
      SYNCED=$((SYNCED + 1))
    fi
  done

  # 2) features/*.json → 1-3 GenFlow/Page Gen/features/
  log "--- features/ → Page Gen/features/ ---"
  FEATURES_TARGET="$MFLOW/1-3 GenFlow/Page Gen/features"
  mkdir -p "$FEATURES_TARGET"
  for f in "$LOCAL_DEV"/features/*.json; do
    [[ -f "$f" ]] || continue
    bn=$(basename "$f")
    target="$FEATURES_TARGET/$bn"
    if [[ -f "$target" ]]; then
      SKIPPED=$((SKIPPED + 1))
    else
      log "  new: $bn"
      if [[ "$MODE" == "apply" ]]; then
        cp "$f" "$target"
      fi
      SYNCED=$((SYNCED + 1))
    fi
  done

  # 3) tools/*.py → 1-4 Dev/tools/
  log "--- tools/ → Dev/tools/ ---"
  TOOLS_TARGET="$MFLOW/1-4 Dev/tools"
  mkdir -p "$TOOLS_TARGET"
  for f in "$LOCAL_DEV"/tools/*.py; do
    [[ -f "$f" ]] || continue
    bn=$(basename "$f")
    target="$TOOLS_TARGET/$bn"
    if [[ -f "$target" ]]; then
      SKIPPED=$((SKIPPED + 1))
    else
      log "  new: $bn"
      if [[ "$MODE" == "apply" ]]; then
        cp "$f" "$target"
      fi
      SYNCED=$((SYNCED + 1))
    fi
  done

  # 4) Output/ subdirectories → corresponding Obsidian paths
  log "--- Output/ subdirectories ---"
  for subdir in "Output/SEO-Reports" "Output/Knowledge Base" "Output/Lovart-Blog-Pipeline" "Output/Content Calendar" "Output/Page Gen"; do
    src="$LOCAL_DEV/$subdir"
    [[ -d "$src" ]] || continue
    # Map to Obsidian target
    case "$subdir" in
      "Output/SEO-Reports") dst="$MFLOW/1-2 Insight/SEO Reports" ;;
      "Output/Knowledge Base") dst="$MFLOW/1-2 Insight/Knowledge Base" ;;
      "Output/Lovart-Blog-Pipeline") dst="$MFLOW/1-3 GenFlow/Lovart-Blog-Pipeline" ;;
      "Output/Content Calendar") dst="$MFLOW/1-3 GenFlow/Content Calendar" ;;
      "Output/Page Gen") dst="$MFLOW/1-3 GenFlow/Page Gen" ;;
    esac
    mkdir -p "$dst"
    count=0
    find "$src" -type f -not -name ".DS_Store" -not -name "*.pyc" 2>/dev/null | while read -r f; do
      fn=$(basename "$f")
      target="$dst/$fn"
      if [[ ! -f "$target" ]]; then
        if [[ "$MODE" == "apply" ]]; then
          cp "$f" "$target"
        fi
        count=$((count + 1))
      fi
    done
    log "  $subdir → $(basename "$dst"): $count new files"
    SYNCED=$((SYNCED + count))
  done

  # 5) seo-documents/sitemap → 1-2 Insight/SEO Reports/sitemap/
  log "--- seo-documents/sitemap → SEO Reports/sitemap/ ---"
  SITEMAP_SRC="$LOCAL_DEV/seo-documents/sitemap-latest"
  SITEMAP_DST="$MFLOW/1-2 Insight/SEO Reports/sitemap"
  if [[ -d "$SITEMAP_SRC" ]]; then
    mkdir -p "$SITEMAP_DST"
    count=0
    find "$SITEMAP_SRC" -type f -not -name ".DS_Store" 2>/dev/null | while read -r f; do
      fn=$(basename "$f")
      target="$SITEMAP_DST/$fn"
      if [[ ! -f "$target" ]]; then
        if [[ "$MODE" == "apply" ]]; then
          cp "$f" "$target"
        fi
        count=$((count + 1))
      fi
    done
    log "  sitemap-latest → sitemap: $count new files"
    SYNCED=$((SYNCED + count))
  fi
fi

log ""
log "=== Summary ==="
log "  synced: $SYNCED"
log "  skipped (already exists): $SKIPPED"
log "  mode: $MODE"
if [[ "$MODE" == "dry-run" ]]; then
  log "  (dry-run: no files were changed)"
  log "  Run with --apply to execute"
fi
