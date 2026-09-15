#!/bin/bash
# sync-profile-skills.sh — 将 canonical (~/.hermes/skills/lovart/) 的 skills
# 同步到全部活跃 lovart-* profile 的副本 (~/.hermes/profiles/<name>/skills/lovart/)
#
# 解决的问题: profile skills 是物理副本（非软链），单次 patch 只更新一个档案。
# 修改 canonical 后必须跑此脚本，否则其他 profile 看不到改动。
#
# 用法:
#   bash sync-profile-skills.sh                 # 同步全部 8 个 lovart-* profile
#   bash sync-profile-skills.sh lovart-ops      # 只同步指定 profile
#
# 维护: 增删 profile 时改 ACTIVE_PROFILES 数组；同步规则改 LAYOUT。
#
# 2026-07-20 变更: 归档 qa-of-lovart / seo-opt-lovart → ~/.hermes/profiles/.archive/2026-07-20/
#   理由: 三个"超级档案" (content-gen-lovart / qa-of-lovart / seo-opt-lovart) 38/39
#   顶层 skill 完全相同。归档两个冗余档案,保留 content-gen-lovart 作为日常用。
#   新 active 档案: content-gen-lovart + 6 标准 (creation/quality/reports/ops/distribution/management)
#   legacy: lovart-content / lovart-seo (cron 兼容保留)
#   路由决策:lovart-router skill 替代人工判断
#   详见: ~/.hermes/profiles/.archive/2026-07-20/INDEX.md

set -e

GLOBAL_SKILLS="$HOME/.hermes/skills/lovart"
MINDSCRIPT_DIR="/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/MindRe/1-Project/Lovart MFlow/1-1 Harness/09-scripts"

# 活跃 lovart-* profile 清单（libtv-* 历史遗留不动）
# 2026-07-21: 7 active (从 9 缩到 7: 归档 lovart-content / lovart-seo)
ACTIVE_PROFILES=(
  "lovart-ops"
  "lovart-quality"
  "lovart-creation"
  "lovart-distribution"
  "lovart-management"
  "lovart-reports"
  "content-gen-lovart"
)

# 工作线 → skills 分配（SSOT 在此文件，新加 profile/skill 时改这里）
# 格式: profile1|skill1 skill2 ...\nprofile2|skill1 skill2 ...
LAYOUT='
lovart-ops|lovart-project-architecture lovart-output-routing lovart-external-tool-integration lovart-sanity-content-publish lovart-sanity-publish lovart-sanity-preflight lovart-sanity-cms-production lovart-sitemap-update lovart-features-sanity-publish lovart-product-sanity-publish lovart-tools-sanity-publish lovart-scenarios-sanity-publish sanity-cms-operations sanity-cms-batch-ops sanity-cms-bulk-ops sanity-cms-asset-management lovart-content-health-audit lovart-post-publish-verify lovart-pipeline-state lovart-router lovart-universal-prompt lovart-session-recap lovart-landing-page lovart-blog-signal-writer
lovart-creation|lovart-project-architecture lovart-output-routing lovart-content-creation-orchestrator lovart-blog-serp-writer lovart-blog-signal-writer lovart-page-serp-writer lovart-composite-page-design lovart-blog-automation lovart-blog-content-ops lovart-landing-page lovart-refresh-page-generator lovart-image-generation lovart-i18n-pipeline lovart-sanity-content-publish lovart-sanity-publish lovart-sanity-preflight lovart-anti-slop lovart-article-quality-template lovart-pipeline-state lovart-router lovart-universal-prompt lovart-session-recap
lovart-distribution|lovart-project-architecture lovart-output-routing lovart-content-distribution lovart-multi-platform-push lovart-content-creation-orchestrator lovart-blog-automation lovart-page-serp-writer lovart-sanity-content-publish lovart-post-publish-verify lovart-sitemap-update lovart-pipeline-state lovart-router lovart-universal-prompt lovart-session-recap lovart-landing-page lovart-blog-signal-writer
lovart-management|lovart-project-architecture lovart-output-routing lovart-content-calendar lovart-pipeline-orchestrator lovart-content-creation-orchestrator lovart-content-workflow lovart-content-opportunity-scorer lovart-post-publish-verify lovart-pipeline-state lovart-router lovart-universal-prompt lovart-session-recap lovart-landing-page lovart-blog-signal-writer
lovart-quality|lovart-project-architecture lovart-output-routing lovart-anti-slop lovart-article-quality-template lovart-content-audit lovart-content-health-audit lovart-content-quality-gates lovart-i18n-pipeline lovart-landing-image-audit lovart-sanity-preflight lovart-post-publish-verify lovart-pipeline-state lovart-router lovart-universal-prompt lovart-session-recap lovart-landing-page lovart-blog-signal-writer
lovart-reports|lovart-project-architecture lovart-output-routing lovart-trident-data-engine lovart-data-ingestion lovart-sentinel lovart-sentinel-orm lovart-sentinel-report lovart-seo-reporting lovart-seo-report-analysis lovart-seo-report-pipeline lovart-seo-content-ops lovart-seo-internal-linking lovart-content-opportunity-scorer lovart-pipeline-state lovart-router lovart-universal-prompt lovart-session-recap lovart-landing-page lovart-blog-signal-writer
content-gen-lovart|lovart-project-architecture lovart-output-routing lovart-content-creation-orchestrator lovart-content-workflow lovart-blog-serp-writer lovart-blog-signal-writer lovart-page-serp-writer lovart-composite-page-design lovart-blog-automation lovart-blog-content-ops lovart-landing-page lovart-refresh-page-generator lovart-landing-image-audit lovart-i18n-pipeline lovart-it-blog-translation lovart-image-generation lovart-content-calendar lovart-sanity-content-publish lovart-sanity-publish lovart-sanity-preflight lovart-post-publish-verify lovart-anti-slop lovart-article-quality-template lovart-content-quality-gates lovart-pipeline-state lovart-router lovart-new-tool-governance lovart-universal-prompt lovart-session-recap lovart-dream-memory
|'

# 解析参数：可选指定单个 profile
TARGET_PROFILE="${1:-}"
if [ -n "$TARGET_PROFILE" ]; then
  echo "=== 单档案模式: $TARGET_PROFILE ==="
  PROFILES_TO_SYNC=("$TARGET_PROFILE")
else
  echo "=== 全量同步 ${#ACTIVE_PROFILES[@]} 个 profile ==="
  PROFILES_TO_SYNC=("${ACTIVE_PROFILES[@]}")
fi

# 主循环
sync_one() {
  local prof="$1"
  local skills_str
  skills_str=$(echo "$LAYOUT" | grep "^${prof}|" | head -1 | cut -d'|' -f2-)
  if [ -z "$skills_str" ]; then
    echo "  ⚠️  $prof 不在 LAYOUT，跳过（如需同步请先在 LAYOUT 加映射）"
    return 0
  fi

  IFS=' ' read -ra SKILLS <<< "$skills_str"
  local target="$HOME/.hermes/profiles/$prof/skills/lovart"
  mkdir -p "$target"

  # 清理不在新布局的 lovart-*/sanity-*
  local removed=0
  for d in "$target"/*/; do
    [ -d "$d" ] || continue
    local name=$(basename "$d")
    case "$name" in
      lovart-*|sanity-*) : ;;
      *) continue ;;
    esac
    local keep=0
    for s in "${SKILLS[@]}"; do
      [ "$name" = "$s" ] && keep=1
    done
    if [ $keep = 0 ]; then
      rm -rf "$d"
      removed=$((removed + 1))
    fi
  done

  # 复制/更新
  local added=0
  for s in "${SKILLS[@]}"; do
    if [ ! -f "$GLOBAL_SKILLS/$s/SKILL.md" ]; then
      echo "  ⚠️  canonical 缺少: $s（profile: $prof）"
      continue
    fi
    mkdir -p "$target/$s"
    cp "$GLOBAL_SKILLS/$s/SKILL.md" "$target/$s/SKILL.md"
    added=$((added + 1))
  done

  local cnt=$(ls "$target" 2>/dev/null | wc -l | tr -d ' ')
  echo "  ✅ $prof: $cnt 个 (同步 $added, 删除多余 $removed)"
}

for p in "${PROFILES_TO_SYNC[@]}"; do
  sync_one "$p"
done

# 双写 MindRe（备份当前脚本本身）
if [ -f "$MINDSCRIPT_DIR/sync-profile-skills.sh" ]; then
  cp "$0" "$MINDSCRIPT_DIR/sync-profile-skills.sh"
  echo ""
  echo "📌 已备份脚本到 MindRe: $MINDSCRIPT_DIR/sync-profile-skills.sh"
fi

echo ""
echo "=== DONE ==="
echo "💡 后续只需改 canonical (~/.hermes/skills/lovart/) 然后跑此脚本即可全量同步"