#!/usr/bin/env bash
set -euo pipefail

# Build lightweight Hermes profiles for the brand.
# Each profile gets only the skills needed for its work line, plus a small
# shared base set. Existing profile skill folders are backed up before rewrite.

HERMES_ROOT="${HERMES_ROOT:-$HOME/.hermes}"
SOURCE_SKILLS="${SOURCE_SKILLS:-$HERMES_ROOT/skills}"
PROFILES_ROOT="${PROFILES_ROOT:-$HERMES_ROOT/profiles}"
BACKUP_ROOT="${BACKUP_ROOT:-$HERMES_ROOT/profile-skill-backups}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MFLOW_PROJECT_ROOT="${MFLOW_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
MFLOW_RULES_ROOT="$MFLOW_PROJECT_ROOT/1-1 Harness/02-rules"

if [[ ! -d "$SOURCE_SKILLS" ]]; then
  echo "Missing source skills directory: $SOURCE_SKILLS" >&2
  exit 1
fi

mkdir -p "$PROFILES_ROOT" "$BACKUP_ROOT"

COMMON_SKILLS=(
  "markdown-viewer"
  "computer-use"
  "note-taking/obsidian"
  "mflow/mflow-project-architecture"
)

profile_model() {
  case "$1" in
    mflow-creation|mflow-content) echo "deepseek-v4-pro" ;;
    *) echo "deepseek-chat" ;;
  esac
}

profile_rules() {
  case "$1" in
    mflow-reports) echo "RULES-00-iron.md RULES-10-reports.md" ;;
    mflow-creation|mflow-content) echo "RULES-00-iron.md RULES-20-creation.md" ;;
    mflow-quality) echo "RULES-00-iron.md RULES-30-quality.md" ;;
    mflow-ops|mflow-seo) echo "RULES-00-iron.md RULES-40-ops.md" ;;
    mflow-distribution) echo "RULES-00-iron.md RULES-50-distribution.md" ;;
    mflow-management) echo "RULES-00-iron.md RULES-60-management.md" ;;
    *) echo "RULES-00-iron.md" ;;
  esac
}

profile_skills() {
  case "$1" in
    mflow-reports)
      printf '%s\n' \
        "mflow/data-ingestion" \
        "mflow/trident-data-engine" \
        "mflow/mflow-sentinel" \
        "mflow/mflow-sentinel-orm" \
        "mflow/mflow-sentinel-report" \
        "mflow/mflow-seo-reporting" \
        "mflow/mflow-seo-report-pipeline" \
        "mflow/mflow-seo-report-analysis" \
        "mflow/mflow-seo-content-ops" \
        "mflow/mflow-seo-internal-linking"
      ;;
    mflow-creation|mflow-content)
      printf '%s\n' \
        "apikey-image-gen" \
        "mflow-existing-page-rewriting" \
        "mflow/content-calendar" \
        "mflow/content-creation-orchestrator" \
        "mflow/blog-automation" \
        "mflow/blog-signal-writer" \
        "mflow/mflow-blog-content-ops" \
        "mflow/page-serp-writer" \
        "mflow/landing-page" \
        "mflow/mflow-composite-page-design" \
        "mflow/mflow-refresh-page-generator" \
        "mflow/image-generation" \
        "mflow/mflow-i18n-pipeline"
      ;;
    mflow-quality)
      printf '%s\n' \
        "mflow-existing-page-rewriting" \
        "mflow/mflow-anti-slop" \
        "mflow/mflow-article-quality-template" \
        "mflow/content-audit" \
        "mflow/mflow-content-health-audit" \
        "mflow/content-quality-gates" \
        "mflow/mflow-landing-image-audit" \
        "mflow/mflow-i18n-pipeline" \
        "mflow/sanity-preflight"
      ;;
    mflow-ops|mflow-seo)
      printf '%s\n' \
        "mflow/sitemap-update" \
        "mflow/mflow-sanity-cms-production" \
        "mflow/sanity-content-publish" \
        "mflow/sanity-preflight" \
        "mflow/sanity-publish" \
        "mflow/features-sanity-publish" \
        "mflow/tools-sanity-publish" \
        "mflow/product-sanity-publish" \
        "mflow/scenarios-sanity-publish" \
        "mflow/sanity-cms-asset-management" \
        "mflow/sanity-cms-operations" \
        "mflow/sanity-cms-batch-ops" \
        "mflow/sanity-cms-bulk-ops" \
        "seo/mflow-seo-technical" \
        "seo/mflow-technical-seo"
      ;;
    mflow-distribution)
      printf '%s\n' \
        "mflow/multi-platform-push" \
        "creative/ai-self-media-article" \
        "social-media/xurl" \
        "productivity/notion"
      ;;
    mflow-management)
      printf '%s\n' \
        "mflow/pipeline-orchestrator" \
        "mflow/content-creation-orchestrator" \
        "mflow/content-calendar" \
        "devops/kanban-orchestrator" \
        "devops/kanban-worker" \
        "hermes-agent/external-skills-catalog" \
        "hermes/external-skills" \
        "autonomous-ai-agents/hermes-agent"
      ;;
  esac
}

emit_profile_rules() {
  local profile="$1"
  local rule
  for rule in $(profile_rules "$profile"); do
    local path="$MFLOW_RULES_ROOT/$rule"
    echo ""
    echo "===== $rule ====="
    if [[ -f "$path" ]]; then
      sed 's/^/    /' "$path"
    else
      echo "    MISSING RULE FILE: $path"
    fi
  done
}

copy_skill() {
  local rel="$1"
  local profile_skills_dir="$2"
  local src="$SOURCE_SKILLS/$rel"
  local dest="$profile_skills_dir/$rel"
  if [[ ! -d "$src" ]]; then
    echo "WARN missing skill: $rel" >&2
    return 0
  fi
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  cp -R "$src" "$dest"
}

write_soul() {
  local profile="$1"
  local profile_dir="$2"
  local model
  model="$(profile_model "$profile")"
  cat > "$profile_dir/SOUL.md" <<EOF
You are Hermes Agent running the the brand lightweight profile: $profile.

Mission: solve only this profile's the brand work line with the smallest relevant skill set. If the task belongs to another work line, say which profile should handle it and stop after giving the routing advice.

Model target: $model

Mandatory the brand rules to load mentally:
$(for r in $(profile_rules "$profile"); do echo "- $MFLOW_RULES_ROOT/$r"; done)

Embedded rule body snapshot:
$(emit_profile_rules "$profile")

Project roots:
- Workspace root: $MFLOW_PROJECT_ROOT
- Knowledge/control center: $MFLOW_PROJECT_ROOT/1-1 Harness/
- Insight and reports: $MFLOW_PROJECT_ROOT/1-2 Insight/
- Content generation and distribution: $MFLOW_PROJECT_ROOT/1-3 GenFlow/
- Automation and local scripts: $MFLOW_PROJECT_ROOT/1-4 Dev/

Non-negotiables:
- Sanity: never deploy, never --replace, never edit schemaTypes, never delete production docs.
- Publishing work stops at ready/preflight unless the user explicitly authorizes publication.
- Reports require period comparison, daily averages for unequal windows, and clear issue/root/mitigation insight.
- Content must be anti-slop: no fake product data, no visible placeholders, no keyword stuffing.
- Multilingual pages are real requirements; rewrite locally rather than translating mechanically.
- Prefer existing data and local indexes. Do not ask the user for lists when the project can generate them.
- Respect skill entrypoint governance: use parent skills for user requests, and call support-only skills only from their parent workflows.
EOF
}

ensure_config() {
  local profile="$1"
  local profile_dir="$2"
  if [[ ! -f "$profile_dir/config.yaml" ]]; then
    cp "$HERMES_ROOT/config.yaml" "$profile_dir/config.yaml"
  fi
  mkdir -p "$profile_dir/memories" "$profile_dir/cron" "$profile_dir/sessions" "$profile_dir/logs"
  [[ -f "$profile_dir/processes.json" ]] || printf '{}\n' > "$profile_dir/processes.json"
}

install_profile() {
  local profile="$1"
  local profile_dir="$PROFILES_ROOT/$profile"
  local skills_dir="$profile_dir/skills"
  local stamp
  stamp="$(date +%Y%m%d-%H%M%S)"

  mkdir -p "$profile_dir"
  ensure_config "$profile" "$profile_dir"

  if [[ -d "$skills_dir" ]]; then
    mkdir -p "$BACKUP_ROOT/$profile"
    mv "$skills_dir" "$BACKUP_ROOT/$profile/skills-$stamp"
  fi
  mkdir -p "$skills_dir"

  for rel in "${COMMON_SKILLS[@]}"; do
    copy_skill "$rel" "$skills_dir"
  done
  while IFS= read -r rel; do
    [[ -n "$rel" ]] && copy_skill "$rel" "$skills_dir"
  done < <(profile_skills "$profile")

  cat > "$skills_dir/.webui-managed-skills.json" <<'EOF'
{}
EOF
  cat > "$skills_dir/.usage.json" <<'EOF'
{}
EOF

  write_soul "$profile" "$profile_dir"
  echo "Installed $profile: $(find "$skills_dir" -name SKILL.md | wc -l | tr -d ' ') skills"
}

profiles=(
  mflow-reports
  mflow-creation
  mflow-quality
  mflow-ops
  mflow-distribution
  mflow-management
  mflow-seo
  mflow-content
)

for profile in "${profiles[@]}"; do
  install_profile "$profile"
done

echo "Done. Start with: hermes -p mflow-reports"
