#!/usr/bin/env bash
# warmup.sh — 开工预热（真实只读 / dry-run）。详见 docs/warmup.md
#
#   bash "1-4 Dev/scripts/warmup.sh"                 # 全量
#   bash "1-4 Dev/scripts/warmup.sh" --only A,B      # 只跑部分板块
#   bash "1-4 Dev/scripts/warmup.sh" --sync-library  # 含内容库全量同步
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

PY="${LOVART_PYTHON:-}"
if [[ -z "$PY" && -x "$ROOT/.venv/bin/python" ]]; then PY="$ROOT/.venv/bin/python"; fi
PY="${PY:-python3}"
exec "$PY" "1-4 Dev/scripts/warmup.py" "$@"
