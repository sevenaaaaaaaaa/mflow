---
session_date: 2026-07-20
session_topic: "档案盘点 + lovart-router skill + Blog 闭环验证 — 解上下文分片悖论"
session_slug: "profile-router-rollout"
profiles_used: [profile-lovart-management]
tools_used: [lovart-pipeline-state, lovart-router, pre-write-check, post-write-check, pre-import-check, dryrun-blog-pipeline]
agents: [hermes]
duration_min: 75
files_changed_count: 9
schema_bumps: 0
status: ready
---

# Context
- 用户反馈上下文分片悖论:为省 token 拆档案 → 跨档场景时硬处理 → 档案污染 → 加 skill 覆盖 → 档案膨胀 → 失去专业意义
- 拆 3 个并行任务执行: (1) 盘点 8 档案 (2) 枚举交叉场景 + 设计 router skill (3) 跑真实 Blog 验证

# Solution
**两轮交付 + 一次真实数据验证**:

第 1 轮 (前一会话): pipeline-state + 3 hooks — 解决"流程串不起来 + 铁律不遵守"
第 2 轮 (本会话): lovart-router — 解决"上下文分片悖论"

**lovart-router 架构**:
- 6 个 active profile 的 registry (model / work_line / owns_stages / key_skills)
- 23 个决策 (stage, scenario) → (action, profile_target, skills_to_load)
- 6 subcommand CLI: decide / matrix / profile / profiles / validate
- 5 subcommand 之外的"suggest_next_item" 自动从 pipeline-state 找下一个该做的

**真实验证 (magnific-vs-lovart blog, 10021 词)**:
- A 单档案全装: 1,864,500 tokens, 0% 步骤漏失, 19 会话
- B router 提醒不切档: 67,900 tokens, **27.8% 步骤漏失**, 0 会话
- **C router + 切档: 248,600 tokens, 0% 步骤漏失, 4 会话 ← 推荐**
- C 比 A 省 **86.7%** token 同时保持 0 漏步骤

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-1 Harness/Skills/06-orchestrate/lovart-router/router.py` | add | 6 subcommand CLI + 23 decisions + 6 profile registry |
| `1-1 Harness/Skills/06-orchestrate/lovart-router/SKILL.md` | add | 决策表 + 典型 session flow |
| `1-1 Harness/Skills/06-orchestrate/lovart-router/tests/dryrun-blog-pipeline.py` | add | 模拟 3 种策略跑 18 个 stage |
| `1-1 Harness/Skills/06-orchestrate/lovart-router/tests/smoketest.sh` | add | 15 router 测试 |
| `1-1 Harness/11-knowledge/sessions/2026-07-20-profile-router-rollout.md` | add | 本文件 |

# Decisions Made
- D1: 6 active profile + 23 decisions + 11 stages (QUEUE/CREATE/REVIEW/SHIP/FINAL)
- D2: scenario 默认 `default` → 缺失 scenario 时按 stage 兜底
- D3: `decide --from-context` 启发式识别 10 种 scenario (l1_fluff / preflight_fail / sanity_id_exists / i18n / ranking_drop 等)
- D4: `info_only` action 给"用户问状态/问 skill" — 不污染 profile
- D5: 4 个 step-loss 验证 (C vs A) — 真实数字支持,不靠 narrative

# Patterns Observed
- P1: 8 个 profile 中 3 个 (`content-gen-lovart` / `qa-of-lovart` / `seo-opt-lovart`) 顶层 skill 完全相同 (38/39) — 冗余档案
- P2: 6 个标准 profile 的 SOUL 仍偏长 (186-232 行) — 规则全量快照塞进去 → token 浪费
- P3: 跨档场景 13 个最常见 — 5 个会导致严重步骤漏失 (C1/C2/C4/C6/C12)
- P4: dryrun 显示策略 B 最省 token 但漏 5 步 — 印证"加 router 不切档"是反 pattern
- P5: dryrun C 跑 4 个 profile = 248k tokens (vs 1 单档案 1.86M) — 切换开销 < 装全集

# Open Questions
- Q1: 是否合并 `content-gen-lovart` + `qa-of-lovart` + `seo-opt-lovart` 这 3 个冗余档案?
- Q2: 是否给 6 标准 profile 的 SOUL 做瘦身 (190-230 → 80-120 行),只留路由表?
- Q3: 是否在 cron 里加 `router decide` 作为梦境的 step 1?
- Q4: 是否把 `lovart-content-creation-orchestrator` 的 step 1 替换成 `router decide`?
- Q5: i18n audit fail 路由回 creation 是正确吗? 还是应回 quality 然后跳 ops?(当前决策未覆盖此路径)

# Cross-References
- entities: skill-lovart-router, skill-lovart-pipeline-state, concept-cross-profile-routing
- decisions: MEMORY-PROJECT.md § 6.5 (上轮) + 本 session log
- skills: lovart-router, lovart-pipeline-state, post-write-check, pre-import-check
- verification: 70 smoke tests pass (39 + 16 + 15)

# Tags
- relevant-tags: #profile-router #cross-profile #state-machine #token-optimization #dryrun-validation #2026-07
