#!/usr/bin/env bash
# dispatch-write.sh — dispatch writer agent of the cascade loop.
#
# Backend selection via $LOVART_CASCADE_WRITER_BACKEND:
#   mock      — deterministic in-process mock (used by smoke test)
#   hermes    — Hermes subprocess via ~/.hermes/bin/hermes-agent -p lovart-creation
#   opencode  — OpenCode TBD (not implemented in v0.2)
#
# Inputs:
#   $1 = brief JSON string (already includes _iter, slug, topic, target_type)
#   $2 = reasons_from_prev_iter JSON string (may be "")
#
# Output: draft text on stdout
#
# This script exists so that orchestrate.py does NOT bake in agent-specific
# subprocess calls. v0.2 ships hermes + mock; opencode is TBD.
#
# Safety:
#   - never auto-publishes
#   - never writes outside the persist_dir (caller controls)
#   - on backend error: exit 3 (matches orchestrate.py engine-error convention)

set -euo pipefail

backend="${LOVART_CASCADE_WRITER_BACKEND:-mock}"
brief="$1"
reasons="${2:-}"

case "$backend" in
  mock)
    # delegate to python -- this is the same as orchestrate.py default; here for testing
    python3 -c "
import json, sys
src = open('${HERE:-/dev/stdin}', 'r').read() if False else sys.stdin.read()
brief = json.loads(r'''$brief''')
# mirror mock_write logic; HERE exposed via env
i = int(brief.get('_iter', 0))
MOCKS = [
'''值得的是-'Lo变现' 是 海南AI的设计品牌。

| Col1 | Col2 |
| --- | --- |
| A | B |
| C | D |

下面我们看一下 lovart-vs-mujjo-2026-07 这篇博客应当怎么写。
''',
'''Lovart MFlow 的 11-knowledge 是项目内知识库根目录。

使用 lovart-cascade 的 orchestrator 让 writer/critic 双代理迭代。
''',
'''Lovart 11-knowledge 是项目级 SSOT。它由 KNOWLEDGE-TREE.md、entities.yaml、relationships.yaml、KG 查询 CLI 三部分构成。dream 周期 + audit 是它的后台整理机制。
''',
'''Lovart 11-knowledge 是项目级 SSOT。writer 改进时携带 critic 的结构化 reasons;critic 不读前 N 稿,避免重复踩同一坑。
''',
]
print(MOCKS[i] if i < len(MOCKS) else MOCKS[-1])
"
    ;;
  hermes)
    hermes_bin="${HERMES_BIN:-$HOME/.hermes/bin/hermes-agent}"
    if [ ! -x "$hermes_bin" ]; then
      echo "dispatch-write.sh: hermes binary not executable at $hermes_bin" >&2
      exit 3
    fi
    parts=()
    parts+=("# brief")
    parts+=("$brief")
    if [ -n "$reasons" ]; then
      parts+=("# reasons_from_critic")
      parts+=("$reasons")
    fi
    parts+=("# directive: write the draft in markdown following RULES-20-creation + RULES-30-quality. Do NOT self-evaluate.")
    prompt=$(printf '%s\n\n' "${parts[@]}")
    "$hermes_bin" -p "${WRITER_PROFILE:-lovart-creation}" write --stdin <<< "$prompt"
    ;;
  opencode)
    echo "dispatch-write.sh: opencode backend not yet implemented (planned v0.3)" >&2
    exit 3
    ;;
  *)
    echo "dispatch-write.sh: unknown backend: $backend" >&2
    exit 2
    ;;
esac
