# Hermes Agent

> Hermes 在 OpenCode 生态里对应 **`20-hermes`** Skills 组（飞书/Lark 集成）；通常作为 **消息/工作流 Agent**，不是 vault 文件调度器。

## 路径

| 项 | 路径 |
|----|------|
| Skills 组 | `~/.config/opencode/skills/20-hermes/` |
| 同步 | `1-Project/1-1 Harness/Skills/sync-skills.sh` |

## 配置要点

1. 安装 OpenCode + Hermes 插件（按你当前 Hermes 发行版文档）。
2. 飞书凭证：`1-1 Harness/Skills/lovart-trident-data-engine/credentials/feishu.json`（勿提交 git）。
3. 在 Hermes 中挂载与 OpenCode 相同的 **instructions**（见 [opencode.md](./opencode.md)）。

## 自动化边界

| 适合 Hermes | 不适合 Hermes |
|-------------|----------------|
| 飞书通知、审批、把报告推到群 | Tools production pull（改 iCloud 本地 JSON） |
| 触发「请 OpenCode/Cursor 跑 pipeline」 | 直接持有 Sanity write token 无人值守 |

## 推荐模式

```
Cursor Automation (cron)
    → bash pull-tools-from-production.sh
    → （可选）Hermes 发飞书摘要
```

Hermes 侧 **系统提示** 片段：

```
你是 Lovart 运维 Bot。收到「weekly ops」时：
1. 读取用户粘贴的 pull-tools-latest.json 或 health check 日志
2. 用中文 3 条 bullet 摘要；legacy>0 或 brokenUrls>0 时 @负责人
3. 不要自行执行 sanity import
```

## 定时

Hermes 自身 cron 取决于产品实现；**主时钟**仍建议 Cursor Automations 或 shell。
