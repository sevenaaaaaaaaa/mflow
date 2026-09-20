#!/usr/bin/env bash
# push.sh — 只做 git push，凭据优先用 deploy/gh.env（给无家目录访问权的环境用）
#
#   bash deploy/push.sh              # 推当前分支
#   bash deploy/push.sh --dry-run    # 只预演
#
# 与 deploy/sync.sh 的区别：sync.sh 是全流程（测试→提交→推送→服务器→CF），
# 需要 SSH 到服务器；push.sh 只碰 GitHub，任何能走 HTTPS 的环境都能跑。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DRY=""; [[ "${1:-}" == "--dry-run" ]] && DRY="--dry-run"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ -f "$ROOT/deploy/gh.env" ]]; then
    set +u; source "$ROOT/deploy/gh.env"; set -u
fi

if [[ -n "${GH_TOKEN:-}" ]]; then
    REMOTE_PATH="$(git remote get-url origin | sed -E 's#^https://([^@]*@)?github\.com/##')"
    # token 只在这一条命令的参数里，不写进 .git/config，不进 shell 历史文件
    git push $DRY "https://${GH_USER:-x-access-token}:${GH_TOKEN}@github.com/${REMOTE_PATH}" "$BRANCH" 2>&1 \
        | sed -E "s#//[^@]*@#//***@#g"
else
    echo "(未找到 deploy/gh.env，走默认凭据)"
    git push $DRY origin "$BRANCH"
fi
