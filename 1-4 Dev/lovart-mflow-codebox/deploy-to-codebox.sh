#!/usr/bin/env bash
# deploy-to-codebox.sh — 一键部署 Lovart MFlow 到 codebox
#
# Usage:
#   export CODEBOX_API_KEY="codebox_api_key_xxxxxxxx"
#   bash deploy-to-codebox.sh
#
# Prerequisites:
#   - 内网访问 http://172.16.16.203:8080
#   - 飞书账号已登录 codebox 一次
#   - API Key 已生成

set -euo pipefail

CODEBOX="${CODEBOX:-http://172.16.16.203:8080}"
PROJECT="lovart-mflow"
HERE="$(cd "$(dirname "$0")" && pwd)"
H="Authorization: Bearer ${CODEBOX_API_KEY:?Set CODEBOX_API_KEY}"

log() { echo "[deploy] $*"; }

# ============================================================
# Step 1: 创建项目
# ============================================================
log "Step 1: Creating project..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "$H" -X POST "$CODEBOX/api/projects" -d "{\"name\":\"$PROJECT\"}" 2>/dev/null || echo "000")
if [[ "$HTTP_CODE" == "200" ]]; then
  log "  ✓ Project created"
elif [[ "$HTTP_CODE" == "409" ]]; then
  log "  - Project already exists (ok)"
else
  log "  ✗ Failed to create project (HTTP $HTTP_CODE)"
  exit 1
fi

# ============================================================
# Step 2: 创建目录结构
# ============================================================
log "Step 2: Creating directory structure..."
curl -s -H "$H" -X POST "$CODEBOX/api/projects/$PROJECT/exec" \
  -d '{"cmd":"mkdir -p cmd/server internal/api internal/store internal/engine scripts hooks skills config/rules config/profiles web/static logs run"}' >/dev/null
log "  ✓ Directories created"

# ============================================================
# Step 3: 上传 Go 源码
# ============================================================
log "Step 3: Uploading Go source..."

upload_file() {
  local src="$1" dst="$2"
  local content
  content=$(python3 -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" "$src")
  curl -s -H "$H" -X POST "$CODEBOX/api/projects/$PROJECT/exec" \
    -d "{\"cmd\":\"cat > $dst <<'GOEOF'\\n${content:1:-1}\\nGOEOF\"}" >/dev/null
}

upload_file "$HERE/go.mod" "go.mod"
upload_file "$HERE/start.sh" "start.sh"
upload_file "$HERE/cmd/server/main.go" "cmd/server/main.go"
log "  ✓ Go source uploaded"

# ============================================================
# Step 4: 上传 Python 脚本 (从 scripts/ 复制)
# ============================================================
log "Step 4: Uploading Python scripts..."

VAULT="$HOME/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow"

for script in pipeline_state.py router.py governance_check.py; do
  src="$VAULT/1-1 Harness/Skills/06-orchestrate"
  case "$script" in
    pipeline_state.py) src="$src/lovart-pipeline-state/$script" ;;
    router.py) src="$src/lovart-router/$script" ;;
    governance_check.py) src="$src/lovart-new-tool-governance/$script" ;;
  esac
  if [[ -f "$src" ]]; then
    upload_file "$src" "scripts/$script"
    log "  ✓ $script"
  else
    log "  - $src not found (skip)"
  fi
done

# ============================================================
# Step 5: 上传 Hooks
# ============================================================
log "Step 5: Uploading hooks..."

for hook in pre-write-check.sh post-write-check.sh pre-import-check.sh post-generation-check.sh; do
  src="$VAULT/1-4 Dev/scripts/hooks/$hook"
  if [[ -f "$src" ]]; then
    upload_file "$src" "hooks/$hook"
    log "  ✓ $hook"
  else
    log "  - $hook not found (skip)"
  fi
done

# ============================================================
# Step 6: 上传 Skills (51 个 SKILL.md)
# ============================================================
log "Step 6: Uploading skills..."

SKILL_DIR="$HOME/.hermes/skills/lovart"
COUNT=0
for skill in $(ls "$SKILL_DIR" 2>/dev/null); do
  src="$SKILL_DIR/$skill/SKILL.md"
  if [[ -f "$src" ]]; then
    curl -s -H "$H" -X POST "$CODEBOX/api/projects/$PROJECT/exec" \
      -d "{\"cmd\":\"mkdir -p skills/$skill\"}" >/dev/null
    upload_file "$src" "skills/$skill/SKILL.md"
    COUNT=$((COUNT + 1))
  fi
done
log "  ✓ $COUNT skills uploaded"

# ============================================================
# Step 7: 启动
# ============================================================
log "Step 7: Starting project..."
curl -s -H "$H" -X POST "$CODEBOX/api/projects/$PROJECT/start" >/dev/null
sleep 2

# 验证
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "$H" "$CODEBOX/p/$PROJECT/health" 2>/dev/null || echo "000")
if [[ "$HTTP_CODE" == "200" ]]; then
  log "  ✓ Health check passed (HTTP 200)"
else
  log "  ✗ Health check failed (HTTP $HTTP_CODE)"
  log "  Check logs: curl -H '$H' -X POST '$CODEBOX/api/projects/$PROJECT/exec' -d '{\"cmd\":\"tail -20 logs/server.log\"}'"
  exit 1
fi

# ============================================================
# Done
# ============================================================
log ""
log "=== DONE ==="
log "Dashboard: $CODEBOX/p/$PROJECT/"
log "API:       $CODEBOX/p/$PROJECT/health"
log "Pipeline:  $CODEBOX/p/$PROJECT/api/pipeline/summary"
log "Router:    $CODEBOX/p/$PROJECT/api/router/matrix"
