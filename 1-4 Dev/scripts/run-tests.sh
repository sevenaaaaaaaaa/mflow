#!/usr/bin/env bash
# run-tests.sh — MFlow 单元测试（离线，可进会话门禁）
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="${LOVART_PYTHON:-}"
if [[ -z "$PY" && -x "$ROOT/.venv/bin/python" ]]; then PY="$ROOT/.venv/bin/python"; fi
PY="${PY:-python3}"
cd "$ROOT"
exec "$PY" "1-4 Dev/tests/test_console_units.py" "$@"
