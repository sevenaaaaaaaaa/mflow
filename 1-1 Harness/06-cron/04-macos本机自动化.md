---
type: cron
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-management"
tools: [hermes, claude]
status: active
path: 1-1 Harness/06-cron/04-macos本机自动化.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# macOS 本机自动化（launchd）

在 Mac 上无人值守跑定期任务，使用 **launchd**（系统级定时）。与 **Cursor Automation** 二选一，避免同一任务重复执行。

---

## 已提供的自动化

### 1. Tools Pull（每周一 07:00）

| 项 | 路径 |
|----|------|
| 脚本 | `1-4 Dev/automation/tools-pull/pull-tools-from-production.sh` |
| plist 模板 | `…/tools-pull/com.lovart.tools-pull-weekly.plist` |
| 安装 | `bash "…/tools-pull/install.sh"` |
| 卸载 | `launchctl unload ~/Library/LaunchAgents/com.lovart.tools-pull-weekly.plist` |
| 日志 | `~/Library/Logs/Lovart/tools-pull-weekly.log` |
| 手动跑 | `bash "…/pull-tools-from-production.sh"` |
| 状态 | `launchctl list \| grep com.lovart.tools-pull` |

**Cursor 替代方案**：见 [文档/06-自动化状态.md](../文档/06-自动化状态.md) 与 `.cursor/automations/lovart-tools-pull.workflow.json`（**周一 08:00**，需 Save + Run once）。

---

### 2. Sanity 内容健康检查（每周一 08:30）

在 Tools Pull 之后跑，覆盖 auth、未来日期、封面/composite 404、轻量 preflight。

| 项 | 路径 |
|----|------|
| 脚本 | `1-4 Dev/automation/content-health/weekly-health-check.sh` |
| plist 模板 | `…/content-health/com.lovart.content-health-weekly.plist` |
| 安装 | `bash "…/content-health/install.sh"` |
| 卸载 | `bash "…/content-health/uninstall.sh"` |
| 日志 | `~/Library/Logs/Lovart/content-health-weekly.log` |
| 错误日志 | `~/Library/Logs/Lovart/content-health-weekly.err` |
| 手动跑 | `bash "…/weekly-health-check.sh"` |
| 状态 | `launchctl list \| grep com.lovart.content-health` |

脚本非零退出时会在 stderr 写明哪一步失败；报告默认写入 `~/Documents/Lovart Local Dev/Temp/lovart/pull/` 与 `~/Documents/Lovart Local Dev/Output/quality-audits/`。

---

## 安装前提

| 要求 | 说明 |
|------|------|
| macOS 14+ | launchd `StartCalendarInterval` |
| Node.js | Studio `node_modules` 已安装 |
| Sanity 凭据 | `sanity login` 或 `SANITY_API_TOKEN` 在 studio `.env` |
| Mac 唤醒 | 合盖/睡眠时任务会推迟到下次唤醒 |

---

## launchd 通用操作

```bash
# 查看已加载的 Lovart 任务
launchctl list | grep com.lovart

# 立即触发一次（调试）
launchctl start com.lovart.content-health-weekly

# 修改 plist 后重载
launchctl unload ~/Library/LaunchAgents/com.lovart.content-health-weekly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.content-health-weekly.plist
```

---

## 日志目录

默认：`~/Library/Logs/Lovart/`（可通过环境变量 `LOVART_LOG_DIR` 覆盖，install.sh 会写入 plist）。

---

## 与 Cursor Automation 的分工

| 方式 | 适用 |
|------|------|
| **launchd** | 纯 shell、离线 Mac 唤醒后补跑、无 Agent 成本 |
| **Cursor Automation** | 需要 Agent 解读报告、发 Slack/摘要、复杂分支告警 |

**建议组合**：

- Tools Pull：**launchd** 或 **Cursor** 二选一
- 内容健康检查：**launchd**（本机脚本已足够）
- SEO 周报 / Sentinel：**手动** 或另建 plist（脚本在 `1-4 Dev/scripts/`）

---

## 相关文档

- [02-每周任务.md](./02-每周任务.md)
- [PRD-部署上线方案.md](../PRD-部署上线方案.md) §五 launchd 完整配置
- [WORKFLOW_CHAIN.md](../WORKFLOW_CHAIN.md) §五 定时任务调度表
