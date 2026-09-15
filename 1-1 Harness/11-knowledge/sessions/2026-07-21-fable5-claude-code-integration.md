---
session_date: 2026-07-21
session_topic: "蒸馏 Fable 5 + Claude Code prompts → Hermes profile universal principles"
session_slug: "fable5-claude-code-integration"
profiles_used: [profile-lovart-management]
tools_used: [lovart-universal-prompt, lovart-session-recap, lovart-dream-memory]
agents: [hermes]
duration_min: 30
files_changed_count: 10
schema_bumps: 0
status: ready
---

# Context
- 用户不想手动作文本清洗和 Token 剪裁
- GitHub 社区已有两个成熟项目: KinetiNode/claude-fable-5-system-prompt-clean + Piebald-AI/claude-code-system-prompts
- 目标: 借助这些蒸馏成果改善 Hermes 使用体验

# Solution
**从两个仓库提炼 3 个可直接用的东西**:

**1. lovart-universal-prompt** (从 Fable 5 蒸馏):
- 6 条核心行为准则: Pre-Execution Mapping / High-Density Communication / Compliance Fidelity / Zero Placeholders / Constructive Pushback / Session Recap
- 34 行,~500 tokens, 所有 profile 共享
- 内嵌到每个 SOUL.md 的 "## Universal Principles" 段

**2. lovart-session-recap** (从 Piebald-AI away-summary-generation 蒸馏):
- ≤40 words, 1-2 sentences, no markdown
- 格式: goal + current task + next action
- 解决"用户回来时 agent 絮叨半天不说重点"

**3. lovart-dream-memory** (从 Piebald-AI dream-memory-consolidation 蒸馏):
- 5 phase 流程: Orient → Gather → Merge → Sync → Prune
- 适配 Lovart 的 11-knowledge/ 架构
- 解决"记忆不内化, session logs 白写"

**SOUL 重写**:
- 7 个 profile SOUL 全部重写为 v3.0
- 每个 45-59 行(含 universal principles)
- 规则全部改为 vault SSOT 文件引用

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-1 Harness/Skills/06-orchestrate/lovart-universal-prompt/SKILL.md` | add | Fable 5 distilled 6 principles |
| `1-1 Harness/Skills/06-orchestrate/lovart-session-recap/SKILL.md` | add | ≤40 word session recap |
| `1-1 Harness/Skills/06-orchestrate/lovart-dream-memory/SKILL.md` | add | 5-phase memory consolidation |
| `~/.hermes/profiles/content-gen-lovart/SOUL.md` | rewrite | v3.0, 56 lines |
| `~/.hermes/profiles/lovart-creation/SOUL.md` | rewrite | v3.0, 59 lines |
| `~/.hermes/profiles/lovart-quality/SOUL.md` | rewrite | v3.0, 52 lines |
| `~/.hermes/profiles/lovart-reports/SOUL.md` | rewrite | v3.0, 48 lines |
| `~/.hermes/profiles/lovart-ops/SOUL.md` | rewrite | v3.0, 49 lines |
| `~/.hermes/profiles/lovart-distribution/SOUL.md` | rewrite | v3.0, 45 lines |
| `~/.hermes/profiles/lovart-management/SOUL.md` | rewrite | v3.0, 48 lines |

# Decisions Made
- D1: Fable 5 的 6 条原则做 universal overlay(所有 profile 共享),不嵌入每个 SOUL
- D2: session-recap 用 ≤40 words 硬限制,比 Fable 5 原版的 "under 40 words" 更严格
- D3: dream-memory 适配 11-knowledge/ 架构(不是 Claude Code 的 memory/ 目录)
- D4: SOUL v3.0 全部 ≤60 行(含 universal),比 v2.0 的 45-66 行略短

# Patterns Observed
- P1: Fable 5 的核心是"6 条行为准则",不是"600 行规则"——蒸馏有效
- P2: Piebald-AI 的子 Agent 提示词 90% 是 Claude Code 专用(tools/workflows),只有 away-summary 和 dream-memory 可复用
- P3: universal prompt 做成 overlay 比嵌入更灵活——改一处生效所有 profile

# Tags
- relevant-tags: #fable5 #claude-code #prompt-distillation #universal-principles #2026-07
