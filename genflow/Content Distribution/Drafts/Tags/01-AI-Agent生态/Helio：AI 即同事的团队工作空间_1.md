---
title: "Helio：AI 即同事的团队工作空间"
slug: helio-ai-teammate-workspace
date: 2026-05-25
updated: 2026-05-29
tags: [Helio, AI同事, 团队协作, SaaS, 工作空间]
categories: [AI工具]
summary: Helio 把 AI 放进与人类相同的频道、任务板和审批流，支持编码会话、AI 队友与即将推出的会议。适合要审计轨迹的团队，不适合只需个人侧边栏助手的用户。
focus_keyword: Helio
source: https://www.helio.im/
author: Helio / Multica
status: draft
---

# Helio：AI 即同事的团队工作空间

> "Your AI colleague that works beside you. Same channels, same tickets, same work."

## 这是什么

[Helio](https://www.helio.im/) 不是侧边栏插件，而是把 AI 作为**真实团队成员**：同一频道、同一任务、同一审计轨迹。人类与 AI 共享消息时间线，AI 在成员列表中与人类并列。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要 AI 操作可追溯的团队 | ✅ 推荐 | 审批卡 + 审计 |
| 工程/运营混合协作 | ✅ 推荐 | 任务 + 编码会话 |
| 个人单机开发者 | ❌ 过重 | 用 Cursor/opencode 即可 |
| 必须私有化部署且 Helio 未提供 | ⚠️ 联系厂商 | 以注册页政策为准 |

## 安装与前置条件

- 注册：https://app.helio.im  
- 客户端：macOS / Windows / Web  
- 编码会话：可接 Claude Code 或 Codex；JuiceFS 隔离文件系统  
- 定价：需注册或联系了解（未公开标准价）

## 核心用法

### 六大支柱（状态节选）

| 支柱 | 状态 | 要点 |
|------|------|------|
| Unified Channels | 已上线 | 人类+AI 同时间线 |
| Tasks | 已上线 | todo→in_progress→in_review→done，原子认领 |
| Coding Sessions | 已上线 | 真实终端、KMS、OpenFGA |
| AI Teammates | 已上线 | 角色记忆 `~/.brain/` |
| Email | 预览 | 真实邮箱 + 审批发出 |
| Meetings | 即将 | Zoom/Meet/Teams 转录→任务 |

### 互操作

- 聊天：Slack、Lark、Teams、Discord  
- 运行时：Claude Code、Codex、Custom MCP、Docker  
- 工具：Linear、GitHub、Vercel、Gmail/SES、Zoom 等  

### 审批机制

高风险操作（外发邮件、部署、代发消息）需人类批准或编辑。

### 梦境循环

夜间 AI 回顾决策写入 `~/.brain/soul.md`（自我进化叙事）。

## 注意事项与风险

- **SaaS 依赖**：数据与合规以 Helio 政策为准。  
- **成本**：企业定价不透明，上线前确认预算。  
- **AI 权限**：编码会话有真实 shell，审批策略需严格配置。  
- **预览功能**：Email/Meetings 可能变更。

## 与你现有工具的关系

- 同团队 **[Multica](https://github.com/multica-ai/multica)** 与 [[Karpathy 编码行为准则：AI Agent 的 4 条铁律]]。  
- 个人栈（Obsidian + opencode + Hermes）与 Helio **互补**：个人写作本地，团队执行上 Helio。

## FAQ

### Q: 和 Slack + ChatGPT 插件区别？
A: AI 是成员而非插件；任务、编码、审批一体化。

### Q: 支持自建模型吗？
A: AI Teammates 可配模型，细节见产品文档/注册后设置。

### Q: 编码会话用什么？
A: Claude Code 或 Codex，独立 workspace 文件系统。

## 相关链接

- 官网：https://www.helio.im  
- 应用：https://app.helio.im  
- Multica：https://github.com/multica-ai/multica
