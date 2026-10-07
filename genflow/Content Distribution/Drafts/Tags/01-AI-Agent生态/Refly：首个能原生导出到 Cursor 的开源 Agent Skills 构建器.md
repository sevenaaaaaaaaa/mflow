---
title: "Refly：首个能原生导出到 Cursor 的开源 Agent Skills 构建器"
slug: refly
date: 2026-06-15
updated: 2026-06-15
tags: [Agent, Skills, Cursor]
categories: [AI工具]
summary: "Refly：首个能原生导出到 Cursor 的开源 Agent Skills 构建器。平台：Web/Docker。"
focus_keyword: "Refly"
source: https://github.com/refly-ai/refly
author: ""
status: draft
---

# Refly：首个能原生导出到 Cursor 的开源 Agent Skills 构建器

> Web/Docker | [7.4k Stars](https://github.com/refly-ai/refly/stargazers)

## 这是什么

Refly 是首个开源的 Agent Skills 构建平台，核心理念是"**Skills 不是 Prompt，是持久化基础设施**"。它通过可视化 IDE 让你将企业 SOP 和业务逻辑编译为**可版本控制、可复用的确定性 Agent Skill**，然后导出到 Claude Code、Cursor、Codex 等 AI 编程工具中作为可调用的工具使用。

与 n8n、Dify 等工作流工具不同：传统工作流是"触发即黑盒"，难以中途干预和跨环境复用；而 Refly 提供**可干预运行时**（Intervenable Runtime），允许你在执行过程中暂停、审计、修正 Agent 行为，确保 100% 的业务合规。与 LangChain 等框架不同：Refly 不需要手写 Python/TypeScript 样板代码，用自然语言描述意图后由 Copilot 编译为优化的 DSL，**3 分钟即可将静态 SOP 变成可执行 Skill**。

Refly 可以输出为多种形态：REST API（供 Lovable 等前端调用）、Webhook（接入飞书/Slack）、或原生导出到 Claude Code/Cursor 作为 Agent 工具。已集成 3000+ 原生工具（Stripe、Slack、Salesforce、GitHub 等），并完整支持 MCP 协议。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 不断重复相同 AI Agent 提示词的开发者/运维 | ✅ 推荐 | 将高频工作流固化为可复用 Skill，一次构建、到处运行，大幅降低 token 消耗 |
| 企业 IT 团队，需要将内部 SOP 转化为 AI Agent 可执行的操作 | ✅ 推荐 | 版本化 Skill 注册中心 + 可审计运行时，满足合规和团队协作需求 |
| 仅在 ChatGPT 网页端偶尔聊天的普通用户 | ⚠️ 酌情 | Refly 面向 Agent 工作流构建者，需要一定的工程思维，不适合轻量对话场景 |

## 安装

```bash
# 方式一：使用托管版（免部署）
# 直接访问 https://refly.ai/workspace 注册即可使用

# 方式二：Docker 自部署（推荐开发者）
# 详见 https://docs.refly.ai/community-version/self-deploy/

# 方式三：安装 Refly CLI（用于导出 Skills 到 Cursor/Claude Code）
npm install -g @powerformer/refly-cli

# 方式四：从源码构建
git clone https://github.com/refly-ai/refly
cd refly
pnpm install
pnpm dev
```

自部署默认访问 `http://localhost:5700`，首次登录需注册并配置模型提供商（OpenAI/Anthropic 等）。

## 核心用法

1. **创建工作流**：登录后点击"New Workflow"，可选择空白画布（拖拽节点）或 **Vibe 模式**（用自然语言描述需求，AI 自动生成工作流）
2. **配置节点**：添加"网页搜索"、"LLM 分析"、"输出格式"等节点，连接形成完整流程。支持 3000+ 原生工具集成
3. **测试调试**：点击 Run 执行工作流，在可干预运行时中查看每一步的中间结果，发现问题可中途暂停修正
4. **导出为 API**：在设置中生成 API Key，通过 REST 端点 (`POST /api/v1/workflows/{id}/execute`) 调用工作流
5. **导出为 Skill**：`refly skill publish <skill-id>` 将工作流发布为 Skill，在 Claude Code 或 Cursor 中通过 `npx skills add refly-ai/<skill-name>` 安装使用
6. **接入飞书/Slack**：配置 Webhook 触发器，当用户在飞书/Slack 中 @机器人 并发送消息时自动触发工作流并返回结果

## 注意事项与风险

- 自部署版本需要自行管理模型 API Key（OpenAI/Anthropic 等），token 成本由使用的模型决定
- 工作流的**确定性**取决于构建时的逻辑设计，自然语言描述的 Vibe 模式需要在测试中验证边界情况
- 开源许可为 ReflyAI Open Source License（Apache 2.0 + 附加限制），商用部署前请确认许可条款
- Refly Skills 生态仍在早期阶段，官方和社区 Skills 覆盖场景有限
- CLI 工具 (`@powerformer/refly-cli`) 当前功能主要为技能安装和发布，高级编排仍在完善中

## 与你现有工具的关系

- **与 Cursor/Claude Code**：Refly 不是替代品，而是增强层。你可以把在 Refly 中构建的企业工作流导出为 Cursor/Claude Code 可直接调用的 Skill，让编程 Agent 具备访问内部系统的能力
- **与 n8n/Dify**：Refly 在工作流编排上与 n8n/Dify 有重叠，但核心差异在于输出形态——n8n 侧重自动化触发，Refly 侧重将工作流作为可移植的 Agent Skill 分发到不同运行时
- **与 Lovart/LibTV**：Refly 的 API 导出能力可直接为 Lovable 类前端应用提供后端接口。如果你在用 Lovart 生成 App 界面，Refly 可以快速构建与之匹配的后端工作流 API

## 常见问题（FAQ）

**Q: Refly 和 n8n 最大的区别是什么？**
A: n8n 的本质是"可视化自动化触发器"，工作流绑定在实例上难以跨环境复用。Refly 将工作流编译为可移植的 Agent Skill，可以导出给 Claude Code、Cursor 或作为独立 API 调用。此外 Refly 支持运行时干预（中途暂停修正），n8n 是触发后全自动执行。

**Q: 自部署需要什么资源？**
A: 最低配置 2 核 CPU、4GB RAM，推荐 Docker 部署。Refly 本身不包含 LLM，需要自行配置 OpenAI/Anthropic API Key。工作流执行时的 token 消耗取决于复杂度，精简的 DSL 设计可降低 token 花费。

**Q: "Vibe 模式"生成的工作流可靠吗？**
A: Vibe 模式适合快速原型，能极大加速从 0 到 1 的过程。但对于生产级工作流，建议在 Vibe 生成的基础上进行节点级精细调整，并通过反复测试覆盖边界情况。Refly 提供了完整的测试和审计日志来支持这一流程。

## 相关链接

- 来源：https://www.ahhhhfs.com/79316/
- GitHub：https://github.com/refly-ai/refly
