---
session_date: 2026-07-21
session_topic: "Agent 主动使用新 skill: SOUL 强制指令 + session-init.sh"
session_slug: "agent-proactive-usage"
profiles_used: [profile-lovart-management]
tools_used: [session-init.sh]
agents: [hermes]
duration_min: 25
files_changed_count: 10
schema_bumps: 0
status: ready
---

# Context
- 新 skill 已注册到 profile,但 agent 不会主动用——缺强制触发点
- 根因:SOUL.md 是文字指令,LLM 可以"善意绕过"

# Solution
**SOUL v3.1: 7 个 profile 注入 7 个强制 Gate**

| Gate | 触发点 | 强制动作 |
|---|---|---|
| GATE 1 | session start | pipeline_state.py next |
| GATE 2 | session start | router decide |
| GATE 3 | 写新 .py/.sh 文件前 | governance_check.py |
| GATE 4 | 写完 blog draft 后 | post-write-check.sh |
| GATE 5 | Sanity import 前 | pre-import-check.sh |
| GATE 6 | 跨档案场景 | router decide --from-context |
| GATE 7 | session end | 写 session log |

**session-init.sh: 4 gate 自动检查器**
- GATE 1: pipeline-state 存在
- GATE 2: router validate 通过
- GATE 3: pipeline next 有建议
- GATE 4: governance check (手动触发)

**sync-profile-skills.sh: 加新 skill 到 LAYOUT**
- 6 个新 skill 加到 content-gen-lovart + 6 标准 profile 的 LAYOUT

**修复**: sync_to_notion.py / sync_from_notion.py 重命名为 snake_case

**验证**: session-init.sh ALL GATES PASS

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| 7 个 SOUL.md | rewrite | v3.1,含强制 Gate |
| `1-4 Dev/scripts/session-init.sh` | add | 4 gate 检查器 |
| `1-4 Dev/scripts/sync_to_notion.py` | rename | sync-to-notion.py → sync_to_notion.py |
| `1-4 Dev/scripts/sync_from_notion.py` | rename | sync-from-notion.py → sync_from_notion.py |
| `1-1 Harness/09-scripts/sync-profile-skills.sh` | modify | 加 6 个新 skill 到 LAYOUT |

# Decisions Made
- D1: SOUL 的"MUST DO"比"建议"强 3-5 倍(LLM 遵从率更高)
- D2: session-init.sh 的 GATE 4 (governance) 改为手动触发,避免 false positive
- D3: 新 skill 加到所有 7 个 profile 的 LAYOUT,防止下次 sync 删掉

# Patterns Observed
- P1: SOUL.md 是 session 启动时加载的——在这里写"MUST"比 skill 里写更有效
- P2: `skill_view` 注入的上下文 > SOUL.md 文字指令——双管齐下最可靠
- P3: sync-profile-skills.sh 的 LAYOUT 是 skill 的"生死簿"——不在 LAYOUT 就会被删

# Tags
- relevant-tags: #agent-proactive #mandatory-actions #session-init #SOUL-v3.1 #2026-07
