#!/usr/bin/env bash
# sync.sh — MFlow 一键发布：测试 → 提交 → 推送 → 服务器同步 → 重启 → 验证 → 刷新 CF 缓存
#
# Usage:
#   bash deploy/sync.sh                  # 全流程（测试→提交→推送→同步→重启→验证→CF）
#   bash deploy/sync.sh --msg "说明"     # 指定本次提交说明
#   bash deploy/sync.sh --no-push        # 不同步到 GitHub（仅本地测试+服务器）
#   bash deploy/sync.sh --no-commit      # 有未提交改动则中止（不自动提交）
#   bash deploy/sync.sh --dry-run        # 只跑测试与校验，不推送不同步
#   bash deploy/sync.sh --skip-tests     # 跳过本地测试（紧急热修，不推荐）
#
# 前置：
#   - SSH 免密可达 root@172.96.253.73:28766
#   - CF 刷新（可选）：deploy/cf.env 填 CF_API_TOKEN / CF_ZONE_ID / CF_DOMAIN
#     （模板见 cf.env.example；无此文件则自动跳过 CF 步骤并提示）
#
# Exit: 0 = 全部成功；非 0 = 失败步骤号 ×10（如 30 = 同步失败）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

# ── 配置 ──
REMOTE_HOST="${MFLOW_REMOTE_HOST:-172.96.253.73}"
REMOTE_PORT="${MFLOW_REMOTE_PORT:-28766}"
REMOTE_ROOT="/www/wwwroot/mflow"
REMOTE="root@${REMOTE_HOST}"
SSH_OPTS=(-p "$REMOTE_PORT")
CONSOLE_SVC="mflow-console"
SITE_URL="${MFLOW_SITE_URL:-https://nownexts.com/mflow/}"

MSG=""
DO_COMMIT=1
DO_PUSH=1
DO_TESTS=1
DRY_RUN=0
CF_PURGE_ALL=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --msg) MSG="$2"; shift 2;;
        --no-push) DO_PUSH=0; shift;;
        --no-commit) DO_COMMIT=0; shift;;
        --skip-tests) DO_TESTS=0; shift;;
        --dry-run) DRY_RUN=1; shift;;
        --cf-purge-all) CF_PURGE_ALL=1; shift;;
        -h|--help) sed -n '2,20p' "$0"; exit 0;;
        *) echo "未知参数: $1" >&2; exit 20;;
    esac
done

say()  { echo "[sync] $*"; }
fail() { echo "[sync] ✗ $* (exit $1×10)" >&2; exit $(( $1 * 10 )); }

say "=== MFlow sync · $(date '+%F %T') ==="

# ── 1) 本地测试 ─────────────────────────────────────────────
if [[ "$DO_TESTS" -eq 1 ]]; then
    say "① 本地测试：session-init（含 GATE5 语法门禁）"
    bash "1-4 Dev/scripts/session-init.sh" >/dev/null 2>&1 \
        || fail 1 "session-init 门禁未过——先修再发布"

    say "    hook smoketest（16 断言）"
    bash "1-4 Dev/scripts/hooks/tests/smoketest_hooks.sh" >/dev/null 2>&1 \
        || fail 1 "hook smoketest 未过"
    say "  ✓ 测试全绿"
else
    say "① 跳过本地测试（--skip-tests）"
fi

# ── 2) 提交 ─────────────────────────────────────────────
if [[ "$DO_COMMIT" -eq 1 ]]; then
    if [[ -n "$(git status --porcelain)" ]]; then
        if [[ "$DRY_RUN" -eq 1 ]]; then
            say "② [dry-run] 有未提交改动，提交内容如下："
            git status --short
        else
            DEFAULT_MSG="sync: auto-deploy $(date '+%F %H:%M')"
            git add -A
            git commit -m "${MSG:-$DEFAULT_MSG}" --quiet || fail 2 "git commit 失败"
            say "  ✓ 已提交：${MSG:-$DEFAULT_MSG}"
        fi
    else
        say "② 工作区干净，无需提交"
    fi
else
    if [[ -n "$(git status --porcelain)" ]]; then
        say "⚠ 未提交改动被保留（--no-commit）："
        git status --short
    fi
fi

# ── 3) 推送 GitHub ────────────────────────────────────────
if [[ "$DRY_RUN" -eq 1 ]]; then
    say "③ [dry-run] 跳过推送与同步"
    echo "[sync] dry-run 结束"
    exit 0
fi
if [[ "$DO_PUSH" -eq 1 ]]; then
    if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
        LOCAL_SHA=$(git rev-parse HEAD)
        ORIGIN_SHA=$(git rev-parse origin/main 2>/dev/null || echo "")
        if [[ "$LOCAL_SHA" != "$ORIGIN_SHA" ]]; then
            git push origin main >/dev/null 2>&1 || fail 3 "git push 失败"
            say "  ✓ 已推送 GitHub"
        else
            say "③ GitHub 已是最新"
        fi
    else
        say "⚠ 无 upstream，跳过推送"
    fi
else
    say "③ 跳过推送（--no-push）"
fi

# ── 4) rsync 同步（远端路径含空格必须引号——踩过两次的坑）───
say "④ rsync → ${REMOTE}:${REMOTE_ROOT}"
ssh -p "$REMOTE_PORT" "$REMOTE" "true" 2>/dev/null || fail 4 "SSH 连不上 ${REMOTE}:${REMOTE_PORT}"
SYNC_ITEMS=(
    "./1-4 Dev/console/|${REMOTE_ROOT}/1-4 Dev/console/"
    "./1-4 Dev/scripts/hooks/|${REMOTE_ROOT}/1-4 Dev/scripts/hooks/"
    "./1-4 Dev/scripts/session-init.sh|${REMOTE_ROOT}/1-4 Dev/scripts/session-init.sh"
    "./1-4 Dev/scripts/publish_adapters/|${REMOTE_ROOT}/1-4 Dev/scripts/publish_adapters/"
    "./1-4 Dev/scripts/trident/|${REMOTE_ROOT}/1-4 Dev/scripts/trident/"
    "./1-4 Dev/scripts/library/|${REMOTE_ROOT}/1-4 Dev/scripts/library/"
    "run/sites/|${REMOTE_ROOT}/run/sites/"
    "plugins/|${REMOTE_ROOT}/plugins/"
    "templates/|${REMOTE_ROOT}/templates/"
    "deploy/|${REMOTE_ROOT}/deploy/"
    "docs/|${REMOTE_ROOT}/docs/"
    "VERSION|${REMOTE_ROOT}/VERSION"
    "ROADMAP.md|${REMOTE_ROOT}/ROADMAP.md"
    "./1-1 Harness/11-knowledge/sessions/|${REMOTE_ROOT}/1-1 Harness/11-knowledge/sessions/"
)
for entry in "${SYNC_ITEMS[@]}"; do
    src="${entry%%|*}"; dst="${entry#*|}"
    # openrsync 规则：引号只能包 host: 之后的路径部分（包住 user@ 会被当非法用户名字符）
    spec="${REMOTE}:\"${dst}\""
    if ! rsync -az -e "ssh -p $REMOTE_PORT" "$src" "$spec" >/dev/null 2>&1; then
        fail 4 "rsync $src → $dst 失败"
    fi
done
say "  ✓ ${#SYNC_ITEMS[@]} 组已同步"

# ── 5) 重启 + 服务端门禁 ─────────────────────────────────
say "⑤ 重启 ${CONSOLE_SVC} + 服务端门禁"
ssh -p "$REMOTE_PORT" "$REMOTE" "systemctl restart ${CONSOLE_SVC} && sleep 2 && systemctl is-active --quiet ${CONSOLE_SVC}" \
    || fail 5 "服务重启失败"
ssh -p "$REMOTE_PORT" "$REMOTE" "bash '${REMOTE_ROOT}/1-4 Dev/scripts/session-init.sh'" >/dev/null 2>&1 \
    || fail 5 "服务端 session-init 门禁未过"
say "  ✓ 服务 active · 服务端门禁 5/5"

# ── 6) 外部验证 ─────────────────────────────────────────
say "⑥ 外部验证：${SITE_URL}"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL" || echo 000)
[[ "$HTTP" == "200" ]] || fail 6 "域名入口返回 $HTTP（预期 200）"
say "  ✓ 入口 200"

# ── 7) Cloudflare 缓存刷新（可选）────────────────────────
if [[ -f deploy/cf.env ]]; then
    # shellcheck disable=SC1091
    source deploy/cf.env
    if [[ -n "${CF_API_TOKEN:-}" && -n "${CF_ZONE_ID:-}" ]]; then
        if [[ "$CF_PURGE_ALL" -eq 1 ]]; then
            BODY='{"purge_everything":true}'
        else
            URLS=$(printf '"%s",' "$SITE_URL/" "$SITE_URL" | sed 's/,$//')
            BODY="{\"files\":[$URLS]}"
        fi
        R=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
            -H "Authorization: Bearer ${CF_API_TOKEN}" -H "Content-Type: application/json" --data "$BODY")
        if echo "$R" | grep -q '"success":true'; then
            say "⑦ ✓ CF 缓存已刷新$([[ $CF_PURGE_ALL -eq 1 ]] && echo '（全部）' || echo "（${SITE_URL}）")"
        else
            say "⚠ ⑦ CF 刷新失败：$(echo "$R" | head -c 200)——不影响发布，稍后可在 CF 面板手动 purge"
        fi
    else
        say "⑦ ⚠ deploy/cf.env 存在但缺 CF_API_TOKEN/CF_ZONE_ID——跳过 CF 刷新"
    fi
else
    say "⑦ ⚠ 无 deploy/cf.env——跳过 CF 刷新。配置方法："
    echo "     cp deploy/cf.env.example deploy/cf.env  # 填入 CF_API_TOKEN / CF_ZONE_ID"
fi

say "=== 全部完成 ==="
