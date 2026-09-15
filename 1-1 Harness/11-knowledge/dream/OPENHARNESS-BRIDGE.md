---
type: dream-readme
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-management"
tools: [hermes, opencode, cursor, claude, codex]
status: active
path: 1-1 Harness/11-knowledge/dream/OPENHARNESS-BRIDGE.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# OpenHarness (HKUDS / `oh`) vs Lovart 梦境 — 架构桥接判断

> 日期：2026-07-05。
> 状态：决策草案 v1。本文件由 `lovart-dream-orchestrator` 启动时载入。

---

## TL;DR

**短期结论（未来 3 个月）**：两条路并存，不拉通。
**中期路径（>6 个月）** ：开第 3 条「合并快照」路。

---

## 两条工具与它们的目标 / 触发面

| 工具 | 来源 | 跑什么 | 触发面 | 输出位置 |
|------|------|--------|--------|---------|
| **OpenHarness HKUDS (`oh` v0.1.9)** | HKU Data Science Lab 插件层 | Claude Code 插件、team/swarm agent、subprocess | 用户主动 `oh -p "…"` | 程序化 stdout |
| **Lovart 梦境（dream/consolidate.sh）** | 项目内 SSOT | 文件刷新、记忆反推、一致性审计 | launchd 02:30 + 用户 `bash` + skill `lovart-dream-orchestrator` | `1-1 Harness/11-knowledge/audit/`, `~/.hermes/memories/MEMORY.md` |

**重叠面**：两者都"在用户不在线时让系统整理"。
**不重叠**：
- `oh` 主要管 Claude Code 插件（code-review、pr-review-toolkit、security-guidance、commit-commands、hookify、feature-dev）和 team/swarm。
- Dream 主要管 **本项目的内部一致性**（知识图 / 入口引用 / 跨工具 SSOT / 前置覆盖 / cron drift）。
- `oh` 现已配置为"日常不用、CC 插件/team 场景触发"（来自 Hermes MEMORY.md § OpenHarness 段）。

---

## 为什么不现在拉通？

1. **认证独立**：`oh setup` 配自己的 auth，不与 Hermes 共用。任何 SSO 都需要单独审批。开局接成本高、回滚难。
2. **作用域不同**：`oh` 的"团队泳道"面向 multi-agent 协作（含权限边界），Dream 是单 agent「文件 + 内部状态」整理。强行合一 = 双 token / 双管道 / 审计数据双源。
3. **触发面错位**：`oh` 是用户主动调用；Dream 是 02:30 自动 + 用户按需。同一事件既被 `oh` 主动拉又被 Dream 被动推，重复 + 状态漂移风险高。
4. **本项目当前定位**：AGENTS.md / CLAUDE.md / RULES-00 都不依赖 `oh`。「现在合并不补功能、只补复杂度」。

---

## 中期（>6 个月）该怎么做：合并快照

在 02:30 Dream 跑完 audit 后，加一步 **将 audit 关键 violations 推入 `oh` 的 team message queue**：

```
# 假装代码（仅设计参考，未实现）
bash dream/audit.sh --json | jq '.errors[]' | oh -p "auto-fix: $.message" --max-turns 1
```

但**触发规则必须严格**：
- 仅 ERROR 推进去；WARN 不推（避免噪音）
- `oh` 收到的任务是**写文件**，不是调网络
- 任务带明确的 fix patch（来自 audit 的检查项），不需要 `oh` 自己推理

实现条件：
- 内部 audit-output JSON schema 已稳定
- 用户明确同意把 `oh` 接进梦境边界（避免 agent 自动 entangled）
- 先做 mock run：Dream 把 `--json` 出的内容 dump 到临时文件 → 不真接入 `oh` → 由人 review

---

## 决策清单（本 file 的真正目的）

- 短期内 `oh` 调用显式**不**在 `consolidate.sh` 之内。
- 我**不**为 `oh` 在 `entities.yaml` 加 entity。原因：`oh` 是用户级工具，不属于项目内 SSOT；放项目层会让"项目级知识图"和"用户级插件图"接错位。
- 但用户可手写 **桥接事实** 进 `MEMORY-PROJECT.md § 10（跨项目记忆）** 第 N 条**。
- 长期如果合并，把这页提到 `1-4 Dev/` 或 `01-project/` 做正式 ADR。

---

## 边界记录（避免后续模式侵蚀）

- `~/.hermes/memories/MEMORY.md`：跨项目事实、用户纠正、OpenHarness 配置 — 仅人工编辑 + Dream 自动 sync。
- `1-1 Harness/11-knowledge/MEMORY-PROJECT.md`：Lovart 项目 SSOT 事实 — 人工 + Dream 自动。
- `~/.hermes/memories/USER.md`：用户偏好（不联动 / 不自动） — 仅人工。
- `1-1 Harness/11-knowledge/entities.yaml`：实体库（含工具 + 任务） — 人工。
- `oh` memory / RAG：不在 11-knowledge 范围内，**不要**反向写入项目 SSOT。

---

## 仍要继续拉通的触发面（不是合并、是「双向事实同步」）

只一条，且**仅写、不读**：

```
Dream 跑完 audit →
  IF error_count > 0 →
    push 一条到 oh's "team notes"（不挂 priority、仅 markup）
  END
```

实现节奏：先实现单向，再论双向。
