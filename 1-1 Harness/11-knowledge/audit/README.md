---
type: audit-architecture
version: 1.0
updated: 2026-07-05
scope: profile-lovart-management
tools: [hermes, opencode, cursor, claude, codex]
status: active
path: 1-1 Harness/11-knowledge/audit/README.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---

# Audit — 一致性审计维度

梦境每晚跑（含 launchd 02:30 + 手动触发）会产出两类产物：

```
audit/
├── README.md                  ← 本文件：维度清单
├── checks/audit-{DATE}.json   ← 机器可读
├── reports/audit-report-{DATE}.md   ← 人读报告
└── fm-check-{DATE}.txt         ← frontmatter 报告（来自 fm-check.py）
```

## 维度清单（A1-A6）

| ID | 名称 | 说明 | 何时新增 |
|----|------|------|----------|
| A1 | Graph integrity | 无 orphan、无 dangling 节点、id 唯一 | 永久 |
| A2 | Frontmatter | 02-rules / 06-cron / 08-storyline / 11-knowledge / CLAUDE.md 必带 frontmatter（type+version） | 覆盖后改 strict |
| A3 | Tool entry-point ref | 5 工具入口文件均引用 `11-knowledge` | 任何工具配置变化都重跑 |
| A4 | Skill catalog cross-mirror | SSOT => 副本至少一处一致 | skill 库变更后重跑 |
| A5 | Rules consistency | RULES-00 仍说禁 `deploy`/`--replace` + 用 `--missing` | 关键约束类 |
| A6 | Cron graph integrity | 所有 cron entity 有 runs_on 边；profile 都注册 | cron 改动后重跑 |

## 严重级

| 级别 | 后缀 | 含义 | 例 |
|------|------|------|-----|
| ERROR | `log_err` | 必须修复否则 5 工具会跑偏 | A3 entry-point 未引用、cron profile 未知 |
| WARN | `log_warn` | 数据不完整但不影响运行 | A1 待补 graph 边缘、A2 前置覆盖不完整 |

## 状态机

- `0` = 全部 OK / 仅 WARN
- `1` = 有 ERROR（audit 退出码 1，cron 侧发通知）

> 当前版本：A1 + A2 + A3 + A4 + A5 + A6。后续可加 A7 (凭证轮转)、A8 (sanity schema drift) 等。

## 报告格式

- 文件：`audit-report-{YYYY-MM-DD}.md`（人读）
- 结构：`summary` + `errors` + `warnings` + `artifacts` + `follow-up`
- 配对：`checks/audit-{YYYY-MM-DD}.json`（CI / 通知用）
- 固定名：最新报告 = `audit/reports/latest.md` 符号链接（由 audit 主脚本维护，下个阶段加）
