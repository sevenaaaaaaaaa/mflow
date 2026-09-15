---
session_date: 2026-07-20
session_topic: "Pipeline state machine + hooks — 解 S0-S6 串不起来 + 铁律不遵守"
session_slug: "pipeline-state-and-hooks"
profiles_used: [profile-lovart-management]
tools_used: [lovart-pipeline-state, pre-write-check, post-write-check, pre-import-check]
agents: [hermes]
duration_min: 45
files_changed_count: 8
schema_bumps: 0
status: ready
---

# Context
- 用户反馈两个根问题：(1) 跑完 QA 该生成了,跑完生成该跑 QA——流程串不起来; (2) 做了那么多限制,Agent 还是会不遵守 skills
- 根因诊断:状态机缺失(每次 agent 重启从零猜该跑哪步)+ 铁律是文本(LLM 会"善意绕过")
- 解法分两层:状态机 SSOT + hooks 执行器(铁律→exit-code)

# Solution
两层交付,不动现有 skill,只在外部包约束:
1. **lovart-pipeline-state**: 12-stage state machine + 8 subcommand CLI,atomic write + transition guard + fix_count cap (3)
2. **3 hooks**: pre-write / post-write / pre-import,每个 exit-code 化 (0=pass / 1=BLOCK / 2=engine err)
3. **集成**: `pre-import-check` 内部调 `pipeline_state.py check`,两层自动串接
4. **测试**: pipeline-state 39/39 PASS + hooks 16/16 PASS,合计 55 个真实测试用例

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/pipeline_state.py` | add | 8 subcommand CLI, atomic write, 12-stage state machine |
| `1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/smoketest.sh` | add | 39 个状态机测试 (init/upsert/get/list/next/advance/run/check/summary) |
| `1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/SKILL.md` | add | 典型 session flow + safety guards + anti-patterns |
| `1-4 Dev/scripts/hooks/pre-write-check.sh` | add | 文件名/路径/frontmatter/占位符 (5 维) |
| `1-4 Dev/scripts/hooks/post-write-check.sh` | add | H2 密度/词数/fluff/AI 自介/模板残留 (5 维) |
| `1-4 Dev/scripts/hooks/pre-import-check.sh` | add | pipeline-state stage / qa BLOCKs / 日期双写 / 多语言 / artifact (5 维) |
| `1-4 Dev/scripts/hooks/README.md` | add | 调用方式 + 集成 + 与 pipeline-state 关系 |
| `1-4 Dev/scripts/hooks/tests/smoketest_hooks.sh` | add | 16 个 hook 测试 |
| `1-1 Harness/11-knowledge/MEMORY-PROJECT.md` | modify | 新增 § 6.5 记录本 session |

# Decisions Made
- D1: state 默认路径 `1-3 GenFlow/.pipeline/pipeline-state.json` (在 vault 内、可 git track、可 dream sync)
- D2: fix_count cap = 3 (与 quality-cascade 一致; 防止 fix-bleed Ralph-style bug)
- D3: hooks 不写文件只读 (exit-code 即结论,不引入 side effect)
- D4: pre-import-check 内部调 pipeline_state check (而非外部串联) — 减少 SOP 步骤
- D5: 路径 `$HERE/../../..` 用 `cd ... && pwd` 绝对化 (踩坑:相对 `..` 在含空格路径下 macOS Python 不展开)

# Patterns Observed
- P1: `expect_ok/fail` 函数吞了 hook 输出 → FAIL 时无法诊断 → 解决:函数内重跑一次捕获 stderr
- P2: bash 数组 `PS_ARGS=(...)` + `"${PS_ARGS[@]}"` 是处理"含空格路径"唯一正确方式
- P3: 测试 `mktemp -d` 不在 vault 内 → hook 拒 (设计正确) → 测试需用 vault 内 tmp
- P4: macOS 系统 Python 对 `..` 不展开 (但 bash 的 `cd $HERE/../..` 正确) — 永远用 `cd ... && pwd` 取绝对路径

# Open Questions
- Q1: 是否要把 `pipeline_state.py next` 写进 `lovart-content-creation-orchestrator` 的 step 1?
- Q2: Sentinel 触发新 Blog 时是否自动 `pipeline_state upsert` 进 S0-todo?
- Q3: dream/consolidate.sh 是否需要反向把 pipeline-state 同步到 Hermes MEMORY?
- Q4: hooks/README.md 写完后,要不要在 cron 加个每小时 dry-run 报告?

# Cross-References
- entities: skill-lovart-pipeline-state, skill-lovart-quality-cascade, concept-pipeline-state-machine
- decisions: MEMORY-PROJECT.md § 6.5
- skills: lovart-pipeline-state, lovart-content-quality-gates, lovart-sanity-publish

# Tags
- relevant-tags: #pipeline-orchestration #state-machine #hooks #engineering-quality #2026-07
