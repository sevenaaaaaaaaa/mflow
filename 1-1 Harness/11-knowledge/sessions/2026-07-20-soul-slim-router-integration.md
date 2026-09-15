---
session_date: 2026-07-20
session_topic: "SOUL 瘦身 + router 集成 content-creation-orchestrator + --brief 模式"
session_slug: "soul-slim-router-integration"
profiles_used: [profile-lovart-management]
tools_used: [lovart-router, lovart-pipeline-state, lovart-content-creation-orchestrator, sync-profile-skills.sh, dryrun-blog-pipeline]
agents: [hermes]
duration_min: 40
files_changed_count: 5
schema_bumps: 0
status: ready
---

# Context
- 上一轮做了归档 2 个冗余档案 + 6 标准 profile SOUL 瘦身
- 本轮继续: 精简 content-gen-lovart SOUL + 把 router 集成到 content-creation-orchestrator + 加 router --brief 模式

# Solution
3 个改动:

**1. content-gen-lovart SOUL 精简**:
- 56 行中约 20 行是铁律全量快照嵌入 (RULES-00 + Anti-Slop + SEO 报告 + 行为偏好)
- 重写: identity / routing 指令 / rules 引用表 / project roots / hard rules 1 行
- 新 SOUL: 56 → 50 行,移除所有规则嵌入

**2. lovart-content-creation-orchestrator step 0**:
- 在 SKILL.md 的 Step 1 前加了 Step 0: "Resolve state and routing"
- 调用 `pipeline_state.py next` + `router decide`
- 三种返回 (reroute / execute_skill / info_only) 都有明确行为指引

**3. router --brief 模式**:
- 新增 `--brief` flag: 3 行 key=value 输出 (profile=... / action=... / skills=...)
- 用于 cron / script pipes / dream 调用,不需解析 JSON

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `~/.hermes/profiles/content-gen-lovart/SOUL.md` | modify | 56→50 行,移除规则嵌入 |
| `1-1 Harness/Skills/06-orchestrate/lovart-content-creation-orchestrator/SKILL.md` | modify | 加 Step 0 (router decide + pipeline_state next) |
| `1-1 Harness/Skills/06-orchestrate/lovart-router/router.py` | modify | 加 --brief flag + parser arg |
| `1-1 Harness/Skills/06-orchestrate/lovart-router/tests/smoketest.sh` | modify | 加 brief 模式测试 |
| `1-1 Harness/11-knowledge/sessions/2026-07-20-soul-slim-router-integration.md` | add | 本文件 |

# Decisions Made
- D1: content-gen-lovart 保留,不归档,但 SOUL 跟其他 6 个统一风格 (规则引用,不嵌入)
- D2: content-creation-orchestrator 的 Step 0 优先于 Step 1 (router 决策先于分类)
- D3: --brief 3 行格式 (profile/action/skills) 足够 cron 和脚本消费;不需要 --json-only

# Patterns Observed
- P1: 7 个 active profile SOUL 全部统一为相同结构 (identity → routing → what/not → rules table → roots → hard rules)
- P2: content-creation-orchestrator 作为"总入口"加 Step 0 后,任何创作任务自动经过 router 决策
- P3: --brief 模式比 --json 省 90% token,但保留了机器可解析性

# Cross-References
- entities: skill-lovart-router, skill-lovart-content-creation-orchestrator, profile-content-gen-lovart
- decisions: MEMORY-PROJECT.md § 6.6-6.7
- skills: lovart-router, lovart-pipeline-state, lovart-content-creation-orchestrator

# Tags
- relevant-tags: #router-integration #soul-unification #brief-mode #2026-07
