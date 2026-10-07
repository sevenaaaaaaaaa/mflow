#!/usr/bin/env bash
# warmup.sh — 开工预热（真实只读 / dry-run）。详见 docs/warmup.md
#
#   bash "dev/scripts/warmup.sh"                 # 全量
#   bash "dev/scripts/warmup.sh" --only A,B      # 只跑部分板块
#   bash "dev/scripts/warmup.sh" --sync-library  # 含内容库全量同步
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

# 密码来自服务器环境契约 run/env.sh（MFLOW_CONSOLE_PASSWORD）
if [[ -z "${MFLOW_CONSOLE_PASSWORD:-}" && -f "$ROOT/run/env.sh" ]]; then
    set +u; source "$ROOT/run/env.sh"; set -u
fi
if [[ -z "${MFLOW_CONSOLE_PASSWORD:-}" ]]; then
    echo "✗ 缺 MFLOW_CONSOLE_PASSWORD（见 run/env.sh）" >&2; exit 2
fi

PY="${MFLOW_PYTHON:-}"
if [[ -z "$PY" && -x "$ROOT/.venv/bin/python" ]]; then PY="$ROOT/.venv/bin/python"; fi
PY="${PY:-python3}"
exec "$PY" "dev/scripts/warmup.py" "$@"
