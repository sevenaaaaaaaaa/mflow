---
type: loop-engineering-proposal
status: draft
date: 2026-07-05
author: "lovart-management"
companion: 1-1 Harness/06-orchestrate/lovart-quality-cascade/
version: 1.0
updated: 2026-07-05
scope: profile-lovart-management
tools: [hermes, opencode, cursor, claude, codex]
path: 1-1 Harness/11-knowledge/dream/LOOP-ENGINEERING-PROPOSAL.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---

# Loop Engineering — Lovart MFlow 工程化建议

> **目标**：把现有手动版「writer 写、quality 检、fail 回 writer 改、retest」流程工程化，用 evaluable loop 替代。同时明确把哪些 loop **不要**上。

---

## 一、Loop 适用性矩阵（针对本项目）

| Loop 范式 | ROI | 上不上 | 上后的关键约束 |
|----------|-----|--------|--------------|
| A. Agent 自我反馈（plan-execute-evaluate） | 高 | **上** | 写一个明文 pass criteria |
| C. 对抗双代理（writer + critic）       | 高 | **上** | critic 必须严格读 preflight，不能只 inline 评分 |
| D. Eval-driven（前置准则）             | 中 | **先验证再加** | criteria 版本随 audit 报告冻结，防漂移 |
| B. Ralph 持续无人循环                  | 低 | **不上** | 直接违反项目 Sanity `publish` 前的"必人工授权" |
| (元) Agent 改自己 prompt               | 禁 | **不上** | 显式违禁，dream 阶段 audit 监控 |
| 多 model 对抗选优                      | 低 | **不上** | 增复杂度不增收益 |

> 评估基准：本项目当前最大痛点 = 内容批量产出的 AI 味道漂移、质检反复返工、跨工具状态漂移。Loop Engineering **主要治** 第二、第三个；第一个（写作深不够）由 profile 加 worker 深度，不在 loop 工程化范围。

---

## 二、Phase 1 ：质量级联 loop —— 设计（推荐先上）

### 目标

把当前手动的

```
pipeline-orchestrator → creation profile → quality profile (BLOCK) → 手动转发 → creation profile 改 → quality profile (重测) → 可能再 case → … → 人工最终授权 → import
```

工程化为：

```
orchestrator-skill (quality cascade loop, max N iterations)
  ├→ creation.profile writes draft v(N)
  └→ quality.profile evaluates draft v(N)
        ├ BLOCK = 0            → break loop, return "ready for human"
        └ BLOCK > 0 with reasons → re-call creation with hints, N += 1
                                       └ if N == MAX → return "loop-budget-exceeded" → human
```

### 设计要点

#### 1. Profile 边界严守

- **creation profile**：只写；不问"好/坏"
- **quality profile**：只评；不写正文
- **orchestrator（skill `lovart-quality-cascade`）**：调度两者、控制迭代上限、记录中间产物

> 这条强约束来源于 RULES-60 的「一条会话只做一类事」。Loop orchestrator 是 skill 不是 profile；它调用两个 profile，每个 profile 仍是一类事。

#### 2. Pass Criteria 形式化（eval-driven 内核）

```yaml
# 1-1 Harness/Skills/06-orchestrate/lovart-quality-cascade/criteria.yaml
criteria_version: 1.0
block_if:
  - kind: ai-flavor
    pattern: "(代词强~|总结式。|下面~|值得一提~)"
    threshold: 2   # 出现 2 次以上 BLOCK
  - kind: table-anti-human
    pattern: "^\\|.+\\|.+\\|$"
    threshold: 1
  - kind: i18n-translation
    region: '^(de|fr|it|ja|ko|pt|ru|zh|zh-TW)$'
    test: must_have_humanized_terminology
    threshold: 1
  - kind: schema-mismatch
    check: preflight
warn_if:
  - kind: redundancy
    threshold_pct: 0.30
  - kind: missing-link
    threshold_pct: 0.05
```

criteria 当作 **版本资产** 走 git/audit，不用 inline 逻辑。

#### 3. Loop Budget

| 资源 | 默认 | 配置点 |
|------|------|--------|
| 最大迭代次数 | 3 | `criteria.yaml.max_iterations` |
| 单次迭代 timeout | 600 s | `criteria.yaml.iter_timeout_s` |
| 累积 budget (tokens) | 20K | `criteria.yaml.token_budget` |
| Loop 失败行为 | 退回人工 | escalate_to: `lovart-management-workline` |

#### 4. 中间产物 —— 必存档（可"CTRL-Z"）

```
1-3 GenFlow/Blog Pipeline/loops/{YYYY-MM-DD}/{slug}/v0-draft.md
                                                       v1-draft.md
                                                       v2-draft.md
                                                       quality-report.json
                                                       loop-log.md
```

从 v0→v2 任何时间点可回退。

#### 5. 审计 / 可观察

每个 loop run 写一份 `audit/loop-engineering/{YYYY-MM-DD}-{run-id}.md`，含：
- 各 v 的 preflight BLOCK count
- reasons 摘要
- 最终落到 ready 还是 escalate
- 触发 criteria_version

### 受影响文件

| 文件 | 动作 |
|------|------|
| `1-1 Harness/Skills/06-orchestrate/lovart-quality-cascade/SKILL.md` | **新建** orchestrator skill |
| `1-1 Harness/Skills/06-orchestrate/lovart-quality-cascade/criteria.yaml` | **新建** pass criteria 库 |
| `1-1 Harness/.claude/skills/06-orchestrate/lovart-quality-cascade/SKILL.md` | **新建** Claude 复制副本 |
| `1-1 Harness/11-knowledge/entities.yaml` | 加 entity `skill-lovart-quality-cascade`，加边 `profile-lovart-creation uses skill-lovart-quality-cascade` 和反之 |
| `1-1 Harness/11-knowledge/relationships.yaml` | 同上补边 |
| `1-1 Harness/02-rules/RULES-30-quality.md` | 加一条 "Loop budget 默认 3，超出回人工" |
| `1-1 Harness/02-rules/RULES-20-creation.md` | 加一条 "creation profile 只写不评；遇批改指令走 orchestrator 不自评" |

### 不做什么（明确）

- 不让 writer profile 改自己 prompt。
- 不让 critic + writer 共享上下文（separate sessions）。
- 不做在线 token 优化（cost control = cap，不在 loop 内做）。
- 不自动 import 到 Sanity（受 RULES-00 强约束）。

---

## 三、Phase 2 ：梦境 audit → eval-driven 修复指引（次优先）

### 现状

`dream/audit.sh` 已经按 A1-A6 六个维度产 ERROR。但目前是写报告让人看。

### 升级

在 `11-knowledge/audit/auto-fix/recipes.yaml` 写一份「修复指引库」，每个 audit ERROR → 配对一段固定 SOP（或一段 kg query）：

```yaml
A3-error-no-11-knowledge-ref:
  recipe: |
    在文件 X 第一行加：
    <!-- bootstrap: 1-1 Harness/11-knowledge/README.md -->
    或编辑 opencode.jsonc instructions 列表。
  verify: "grep -c '11-knowledge' X > 0"
A6-error-cron-graph-drift:
  recipe: |
    bash 1-1 Harness/11-knowledge/scripts/kg related-to <cron-id> --direction out --type runs_on
    若空：去 1-1 Harness/06-cron/README.md 注册
```

每日 Dream 跑完 audit 后，把 errors + recipes 推到 1-4 Dev/Kanban 的"梦境待办"列（用 `kanban` CLI）。**梦境不自动执行 recipe**，由用户在 lovart-management workline 内手动调用。这条严格守住"梦境只标记不修"边界。

### 受影响文件

- `1-1 Harness/11-knowledge/audit/auto-fix/recipes.yaml`（新建）
- `1-1 Harness/11-knowledge/dream/consolidate.sh` 加一段 "after audit, if errors, emit kanban-payload.yaml"
- `1-4 Dev/Kanban/梦境待办/...`（不实现，只是渲染 shell 命令）

---

## 四、Phase 3：blog 创作四阶链

针对 `lovart-blog-signal-writer`：把当前单次 generate → ready 重写成：

1. **Research phase**：SERP top 10 + 站内 KB consolidate → 选题评分
2. **Outline phase**：钩、段、CTA placement → outline score (anti-slop early catch)
3. **Draft phase**：依 outline 写 → draft score
4. **Polish phase**：表格/lux 展示 polish → final score

每阶段有显式 pass criteria。**任一阶段 BLOCK，回退上一阶段重做，不跨阶段跳跃**。

这是当前不在 MVP 范围，仅在 docs 里记 theta 编号，让你知道边界。

---

## 五、上 Loop 的代价 vs 收益（一行总结）

- 月均 token 涨：估算 +20% （N=3 重写 + 中间产物存档）
- 月均人工 review 减：估算 -40% （loop 把"简单 slop"修掉，剩下"深 slop"才找人）
- 月均 preflight-block-rate：估算 50% → 12% → 8%（Phase 1 后）

数字是预计，待 Phase 1 单 run 后校准并写进 `1-2 Insight/OKR/`。

---

## 六、不上的理由记录

> 这一节是给后人看的 ADR 风格留痕：

- **不上 Ralph（持续无人循环）**：违反 RULES-00「publish 前必人工授权」精神。无人值守无限循环 = 静默发布风险。
- **不上 self-modifying prompt**：所有 prompt 在 RULES + skills 内手动维护，梦境 / audit 监控"prompt 漂移"。
- **不上多 model 对抗选优**：单 agent 看不到对方 profile 全局，盲选胜率低于"同 model 写两稿让 quality 选一"。
- **不上 inline token 优化**：cap = 预算；循环内做 opt = 引入 reward hacking 风险。
- **不直接上 eval-driven 全自动**：criteria 一旦自动调，会跟"SERPs 偏好"耦合 → criteria 漂移；先冻结版本，逐版本手动 review。

---

## 七、决策清单

| 决策 | 推荐 | 备注 |
|------|------|------|
| Phase 1 上不上？ | **上** | 先做 1 个车间（blog），不全面铺 |
| 默认 budget | iter=3 / 600s / 20K tokens | 校准后改 |
| 不上 Ralph？ | **不上** | 永久 ADR |
| criteria 版本化？ | **要**，lock 在 `criteria.yaml` v=1.0 起 |
| Loop 失败默认行为？ | escalate 人工，**不**自动跳过 |

---

## 参考

- 用户原文讨论：`记忆 § 0`
- 反向 cite：Reflexion paper (NeurIPS 2023)、Self-Refine (Meta 2023)、Constitutional AI (Anthropic 2022)、SWE-agent (Princeton 2024)
- 本项目内：openship 06-cron + RULES-30 + skill `lovart-content-quality-gates` 实现细节。
