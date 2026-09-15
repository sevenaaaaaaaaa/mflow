#!/usr/bin/env bash
set -euo pipefail

# Build lightweight Hermes profiles for Lovart.
# Each profile gets only the skills needed for its work line, plus a small
# shared base set. Existing profile skill folders are backed up before rewrite.

HERMES_ROOT="${HERMES_ROOT:-$HOME/.hermes}"
SOURCE_SKILLS="${SOURCE_SKILLS:-$HERMES_ROOT/skills}"
PROFILES_ROOT="${PROFILES_ROOT:-$HERMES_ROOT/profiles}"
BACKUP_ROOT="${BACKUP_ROOT:-$HERMES_ROOT/profile-skill-backups}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOVART_PROJECT_ROOT="${LOVART_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
LOVART_RULES_ROOT="$LOVART_PROJECT_ROOT/1-1 Harness/02-rules"

if [[ ! -d "$SOURCE_SKILLS" ]]; then
  echo "Missing source skills directory: $SOURCE_SKILLS" >&2
  exit 1
fi

mkdir -p "$PROFILES_ROOT" "$BACKUP_ROOT"

COMMON_SKILLS=(
  "markdown-viewer"
  "computer-use"
  "note-taking/obsidian"
  "lovart/lovart-project-architecture"
)

profile_model() {
  case "$1" in
    lovart-creation|lovart-content) echo "deepseek-v4-pro" ;;
    *) echo "deepseek-chat" ;;
  esac
}

profile_rules() {
  case "$1" in
    lovart-reports) echo "RULES-00-iron.md RULES-10-reports.md" ;;
    lovart-creation|lovart-content) echo "RULES-00-iron.md RULES-20-creation.md" ;;
    lovart-quality) echo "RULES-00-iron.md RULES-30-quality.md" ;;
    lovart-ops|lovart-seo) echo "RULES-00-iron.md RULES-40-ops.md" ;;
    lovart-distribution) echo "RULES-00-iron.md RULES-50-distribution.md" ;;
    lovart-management) echo "RULES-00-iron.md RULES-60-management.md" ;;
    *) echo "RULES-00-iron.md" ;;
  esac
}

profile_skills() {
  case "$1" in
    lovart-reports)
      printf '%s\n' \
        "lovart/lovart-data-ingestion" \
        "lovart/lovart-trident-data-engine" \
        "lovart/lovart-sentinel" \
        "lovart/lovart-sentinel-orm" \
        "lovart/lovart-sentinel-report" \
        "lovart/lovart-seo-reporting" \
        "lovart/lovart-seo-report-pipeline" \
        "lovart/lovart-seo-report-analysis" \
        "lovart/lovart-seo-content-ops" \
        "lovart/lovart-seo-internal-linking"
      ;;
    lovart-creation|lovart-content)
      printf '%s\n' \
        "apikey-image-gen" \
        "lovart-existing-page-rewriting" \
        "lovart/lovart-content-calendar" \
        "lovart/lovart-content-creation-orchestrator" \
        "lovart/lovart-blog-automation" \
        "lovart/lovart-blog-signal-writer" \
        "lovart/lovart-blog-content-ops" \
        "lovart/lovart-page-serp-writer" \
        "lovart/lovart-landing-page" \
        "lovart/lovart-composite-page-design" \
        "lovart/lovart-refresh-page-generator" \
        "lovart/lovart-image-generation" \
        "lovart/lovart-i18n-pipeline"
      ;;
    lovart-quality)
      printf '%s\n' \
        "lovart-existing-page-rewriting" \
        "lovart/lovart-anti-slop" \
        "lovart/lovart-article-quality-template" \
        "lovart/lovart-content-audit" \
        "lovart/lovart-content-health-audit" \
        "lovart/lovart-content-quality-gates" \
        "lovart/lovart-landing-image-audit" \
        "lovart/lovart-i18n-pipeline" \
        "lovart/lovart-sanity-preflight"
      ;;
    lovart-ops|lovart-seo)
      printf '%s\n' \
        "lovart/lovart-sitemap-update" \
        "lovart/lovart-sanity-cms-production" \
        "lovart/lovart-sanity-content-publish" \
        "lovart/lovart-sanity-preflight" \
        "lovart/lovart-sanity-publish" \
        "lovart/lovart-features-sanity-publish" \
        "lovart/lovart-tools-sanity-publish" \
        "lovart/lovart-product-sanity-publish" \
        "lovart/lovart-scenarios-sanity-publish" \
        "lovart/sanity-cms-asset-management" \
        "lovart/sanity-cms-operations" \
        "lovart/sanity-cms-batch-ops" \
        "lovart/sanity-cms-bulk-ops" \
        "seo/lovart-seo-technical" \
        "seo/lovart-technical-seo"
      ;;
    lovart-distribution)
      printf '%s\n' \
        "lovart/lovart-multi-platform-push" \
        "creative/ai-self-media-article" \
        "social-media/xurl" \
        "productivity/notion"
      ;;
    lovart-management)
      printf '%s\n' \
        "lovart/lovart-pipeline-orchestrator" \
        "lovart/lovart-content-creation-orchestrator" \
        "lovart/lovart-content-calendar" \
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
    local path="$LOVART_RULES_ROOT/$rule"
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
You are Hermes Agent running the Lovart lightweight profile: $profile.

Mission: solve only this profile's Lovart work line with the smallest relevant skill set. If the task belongs to another work line, say which profile should handle it and stop after giving the routing advice.

Model target: $model

Mandatory Lovart rules to load mentally:
$(for r in $(profile_rules "$profile"); do echo "- $LOVART_RULES_ROOT/$r"; done)

Embedded rule body snapshot:
$(emit_profile_rules "$profile")

Project roots:
- Workspace root: $LOVART_PROJECT_ROOT
- Knowledge/control center: $LOVART_PROJECT_ROOT/1-1 Harness/
- Insight and reports: $LOVART_PROJECT_ROOT/1-2 Insight/
- Content generation and distribution: $LOVART_PROJECT_ROOT/1-3 GenFlow/
- Automation and local scripts: $LOVART_PROJECT_ROOT/1-4 Dev/

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
  lovart-reports
  lovart-creation
  lovart-quality
  lovart-ops
  lovart-distribution
  lovart-management
  lovart-seo
  lovart-content
)

for profile in "${profiles[@]}"; do
  install_profile "$profile"
done

echo "Done. Start with: hermes -p lovart-reports"
