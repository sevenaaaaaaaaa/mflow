# Cursor

## 规则与上下文

| 文件 | 作用 |
|------|------|
| `1-Project/harness/AGENTS.md` | 运维规则（Harness） |
| `1-Project/1-1 GEO Readme/AGENTS.md` | GEO / Sanity 规则 |
| `1-Project/dev/.cursor/rules/mflow-sanity-content-pipeline.mdc` | Sanity 管道红线（alwaysApply） |

## Automations（定时）

草稿目录：`1-Project/.cursor/automations/`

| JSON | 状态 |
|------|------|
| `mflow-tools-pull.workflow.json` | **已保存** |
| `mflow-content-health-weekly.workflow.json` | 待 Save |
| `mflow-trident-weekly.workflow.json` | 待 Save |
| `mflow-seo-weekly.workflow.json` | 待 Save |
| `mflow-sentinel-daily.workflow.json` | 待 Save |

**工作区**：Automations 环境选 vault 根 `LifeOS Pro PARA Vault`，分支 `main`。

**创建**：Cursor → Automations → New；或 Agent 调用 `open_automation` + `prefillWorkflowData`（`name` + `workflow` 字段）。

## 手动触发词

| 意图 | 说法 |
|------|------|
| Tools pull | 「跑 Tools pull」/ 「pull tools from production」 |
| 健康检查 | 「weekly health check」/ 「preflight sanity」 |
| 完整 pipeline | 「运行完整 pipeline」（见 `MFLOW-AUTOMATION-WORKFLOW.md`） |

## 注意

- Cloud Agent 计费（Max Mode）；定时任务在 **Automations → Runs** 查看。
- 与 launchd 二选一；卸载：`bash dev/automation/unload-all-launchd.sh`
