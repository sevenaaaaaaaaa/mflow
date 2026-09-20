#!/usr/bin/env bash
# run-tests.sh — MFlow 单元测试（离线，可进会话门禁）
#
# 隔离：测试导入 console.py 时会触发若干落盘动作（approvals.log / tasks / housekeeping）。
# 若不隔离，单测会把审计噪音写进生产 run/（2026-09-20 实测一天污染 92 条）。
# 故这里强制 MFLOW_RUN_DIR 指向临时目录，跑完即删。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="${LOVART_PYTHON:-}"
if [[ -z "$PY" && -x "$ROOT/.venv/bin/python" ]]; then PY="$ROOT/.venv/bin/python"; fi
PY="${PY:-python3}"
cd "$ROOT"

TEST_RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/mflow-test-run.XXXXXX")"
cleanup() { rm -rf "$TEST_RUN_DIR"; }
trap cleanup EXIT

# 只读种子：站点档案是预设展开所必需的，拷贝而非引用生产目录
mkdir -p "$TEST_RUN_DIR/sites"
[[ -d "$ROOT/run/sites" ]] && cp -a "$ROOT/run/sites/." "$TEST_RUN_DIR/sites/" 2>/dev/null || true

export MFLOW_RUN_DIR="$TEST_RUN_DIR"
exec "$PY" "1-4 Dev/tests/test_console_units.py" "$@"
