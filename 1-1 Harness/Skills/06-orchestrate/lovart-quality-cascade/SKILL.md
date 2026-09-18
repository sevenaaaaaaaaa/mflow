---
description: 质量级联 skill。生成 → 质检 → BLOCK 反馈重写 ≤3 轮。
---
# lovart-quality-cascade — v0.2 runnable orchestrator

> 双代理 cascade 引擎正式版。状态机 + criteria 评估 + dispatch 抽象。
> **状态 v0.2**：mock backend 可 reproduce 验证；hermes backend 路径已写但未跑过（待真实环境调）。

---

## Explicit-Only 入口约束

本 skill 是实验性编排器，不参与默认 content creation / quality gates / review 路由。默认质检永远走 `lovart-content-quality-gates`；默认创作永远走对应父入口（Blog 或 Landing Page）。

只有用户明确要求 cascade / 双代理 / writer+critic / quality loop 时，才允许由 `lovart-pipeline-orchestrator` 或 `lovart-management` 显式调用本 skill。

## When this skill loads

加载条件：

- 用户说「cascade」、「双代理」、「writer+critic」、「quality loop」
- 用户显式接受额外成本与迭代时间

不加载：

- 单 agent 写一篇的简单任务
- 监控报告 / ORM / 数据类（不需要 loop）
- 与「发布」直接耦合的动作（cascade 永远停在 ready；手工走 import）

---

## Inputs

| 变量 | 类型 | 必填 | 例 |
|------|------|------|-----|
| `--slug` | str | 是 | `lovart-vs-mujjo-2026-07` |
| `--topic` | str | 是 | `why Lovart 11-knowledge matters` |
| `--target-type` | enum | 否 | `blog` / `landing-page`（v0.2 仅 blog 端到端验证） |
| `--persist-dir` | path | 是 | `1-3 GenFlow/Blog Pipeline/loops/{DATE}/{slug}/` |
| `--criteria` | path | 否 | 默认 `criteria.yaml` 同目录 |
| `--max-iterations` | int | 否 | override criteria.yaml 默认 3 |
| `--backend` | enum | 否 | `mock` (default) / `hermes` / `opencode` (TBD) |
| `--writer-profile` | str | 否 | `lovart-creation` |
| `--critic-profile` | str | 否 | `lovart-quality` |
| `--hermes-bin` | path | 否 | `~/.hermes/bin/hermes-agent` |

---

## Outputs (persist\_dir artifacts)

| 文件 | 内容 |
|------|------|
| `v{0,1,2}-draft.md` | 各 iter 草稿 |
| `quality-report-v{N}.json` | 各 iter 评审结果（BLOCK 计数 + reasons + 元数据） |
| `loop-log.md` | 时间戳 + state 转换的可读 log |
| `loop-meta.json` | 机器可读 run meta：rc / state / iterations 详情 |

返回码：
- `0` = READY（BLOCK=0 命中）
- `1` = ESCALATE（max-iterations 命中未达成 READY）
- `2` = ESCALATE 原因 max-iterations（亦 = 1，在本版本区分以方便 cron 区分）
- `3` = engine error（write/eval 子进程崩溃）

---

## Process — engine 内幕

状态机：
```
INIT ──> WRITE(v0) ──> EVAL(v0)
                        ├─ BLOCK=0 ──> DONE(rc=0)
                        └─ BLOCK>0 ──> WRITE(v1) ──> ... ──> WRITE(v(N+1))
                                                                └─ if N+1 == max_iters ──> ESCALATE(rc=1/2)
```

特征：

- writer 是 **lv-local-call** 的：dispatch-write.sh 调用 hermes/opencode 或 mock。
- critic 是 **stateful** 的：读 v(N) 草稿 + criteria.yaml；内存里**不**留前 N 稿状态。
- reasons 跨 iter 传递**仅结构化**（rule_id + span + matched text），不传整段 reviewer 反馈——这是为防止 context bleed（Ralph-style bug = reasons 越长越多 over many iter）。
- 全 run 边界：`--max-iterations=3` 默认保住 token budget，templated criteria.yaml v0.1 lock。

---

## Backend 接口

### Mock backend（默认，用于 dev + smoke test）

- 不调任何 LLM API
- MOCK_WRITES 4 段文本（人工编写，每 iter 比前 iter 干净）
- evaluator 按 criteria.yaml 的 block_if 规则做 regex 匹配
- 优势：CI 友好；劣势：criteria.yaml 任一改 → 跑 smoke test 重验

### Hermes backend（生产 path，v0.2 已写未跑）

```bash
# writer
hermes-agent -p lovart-creation write --stdin
# critic
hermes-agent -p lovart-quality evaluate --stdin
```

需要的环境变量：
- `HERMES_BIN`：hermes-agent 绝对路径
- `WRITER_PROFILE`、`CRITIC_PROFILE`：profile 名（默认 lovart-creation / lovart-quality）

### OpenCode backend（v0.3）

未实现。在 opencode.jsonc 已为它预留：「cascade-write」「cascade-eval」命令 = 入口，下个版本接上 OpenCode 自定义 command 的实际 backend。

---

## Run 命令速查

```bash
# 1. smoke test (default in ~/.config/opencode)
bash 1-1\ Harness/Skills/06-orchestrate/lovart-quality-cascade/smoketest.sh

# 2. 真跑一篇 blog（hermes backend，需 hermes 已配）
bash 1-1\ Harness/Skills/06-orchestrate/lovart-quality-cascade/orchestrate.py \
  --slug "lovart-11-knowledge-explained" \
  --topic "what the 11-knowledge directory is for" \
  --persist-dir "1-3 GenFlow/Blog Pipeline/loops/2026-07-05/lovart-11-knowledge-explained/" \
  --backend hermes

# 3. 单步 writer（不走 cascade）
bash 1-1\ Harness/Skills/06-orchestrate/lovart-quality-cascade/dispatch-write.sh \
  '<brief-json>' '<reasons-json>'

# 4. 单步 critic（不走 cascade）
cat v0-draft.md | python3 1-1\ Harness/Skills/06-orchestrate/lovart-quality-cascade/dispatch-eval.py \
  --criteria 1-1\ Harness/Skills/06-orchestrate/lovart-quality-cascade/criteria.yaml
```

OpenCode 自定义命令（已加进 `opencode.jsonc`）：

- `/cascade-write <brief> [reasons]` — 单次 writer
- `/cascade-eval [criteria]` — 单次 critic（stdin 接 draft）
- `/cascade-run <slug> <topic> [persist-dir]` — 完整 loop run

---

## Smoke test（v0.2 已通过）

```
[smoke-pass]     rc=0 state=DONE        iters=2   v0 BLOCK=True blocks=6 → v1 BLOCK=False blocks=0
[smoke-escalate] rc=2 state=EVAL        iters=1   v0 BLOCK=True blocks=6 → max=1 hit → ESCALATE
VERDICT: PASS
```

Reproduce: `bash 1-1\ Harness/Skills/06-orchestrate/lovart-quality-cascade/smoketest.sh`

---

## 受 Profile 边界约束

- writer & critic 仍**两个独立 session**（RULES-60 精神）：cascade 是 orchestrator skill，不是 profile。
- 严禁把 critic feedback 完整文本传给 writer（防 Ralph-style bleed）。
- 严禁 criteria.yaml 在 engine 内自调 — 改 criteria = 提 PR → 版本 bump → CHANGELOG。
- 严禁自动 publish — rc=0 仅 = ready；最终 publish 仍走人工（受 RULES-00 iron 约束）。

---

## 不做什么 — 边界

| 不做 | 理由 |
|------|------|
| 不自动 publish | RULES-00 iron spirit |
| 不并发跑 writer/critic | 防 context bleed |
| 不缓存草稿跨 run | audit 透明 |
| 不改 criteria.yaml | 防 prompt drift |
| 不接 Ralph-style 不限 iter | 预算 fixed = 3 |
| 不让 writer 自己改 prompt | RULES-00 行为铁律 + DPRC (dream/audit 监控) |

---

## Failure modes（NEVER）

- 「criteria 全 BLOCK」→ escalate，**不**自动调宽松。
- 「cost > 20K tokens」→ escalate，**不**降 criteria。
- 「4+ iter 自动继续」 → 这是 budget trampling；明确禁止，已写 config。
- 「writer 自己说 '我没有问题'」 → 依然过 critic；writer 自评无效。

---

## Reference

- ADR：`1-1 Harness/11-knowledge/dream/LOOP-ENGINEERING-PROPOSAL.md`
- criteria：`1-1 Harness/Skills/06-orchestrate/lovart-quality-cascade/criteria.yaml` (v0.1 frozen)
- engine：`orchestrate.py`
- dispatchers：`dispatch-write.sh`（writer）/ `dispatch-eval.py`（critic）
- smoke test：`smoketest.sh`
- 安全 runtime：`max_iterations=3`、`iter_timeout_s=600`、`token_budget=20000`
- related：skill `lovart-content-creation-orchestrator`（single-pass）、skill `lovart-content-quality-gates`（single-pass criteria）、skill `lovart-anti-slop`（被 cascade criterion 通过 v0.2 取代）
- 改本 skill / criteria：提 PR 走 `git mv 1-1 Harness/Skills/06-orchestrate/lovart-quality-cascade/` → 1-1 Harness/.claude/skills/06-orchestrate/ 同路径同步。
