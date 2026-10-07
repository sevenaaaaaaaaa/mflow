---
title: "awesome-openclaw-skills：5400+ OpenClaw 技能精选合集"
slug: awesome-openclaw-skills
date: 2026-06-16
updated: 2026-06-16
tags: [OpenClaw, Skills, 合集, Agent, 精选]
categories: [AI工具]
summary: "awesome-openclaw-skills 是由 VoltAgent 维护的 OpenClaw 技能精选合集，从官方技能注册表中筛选 5400+ 高质量技能，按类别组织。排除了 7215 个垃圾/重复/低质量/恶意技能。50.3k Stars，MIT 协议。"
focus_keyword: "awesome-openclaw-skills"
source: https://github.com/VoltAgent/awesome-openclaw-skills
status: draft
---

# awesome-openclaw-skills：5400+ OpenClaw 技能精选合集

> 从官方技能注册表筛选 5400+ 技能，排除 7215 个次品 | 50.3k Stars | MIT | 按类别组织 | 持续更新

## 这是什么

awesome-openclaw-skills 是 VoltAgent 维护的 OpenClaw（原名 Clawdbot）技能精选合集。OpenClaw 是一个运行在本地机器上的 AI 助手，Skills 是它的扩展机制，允许 AI 与外部服务交互、自动化工作流和执行专门任务。这个精选列表从 OpenClaw 的公共技能注册中心（ClawHub）中筛选出高质量技能，按类别组织以方便发现和安装使用。

该项目的核心价值在于**筛选和策展**。ClawHub 注册中心拥有大量社区提交的技能，但其中包含大量垃圾、重复、低质量和恶意技能。awesome-openclaw-skills 团队排除了以下内容：疑似垃圾/批量账号/机器人账户 4065 个、重复/相似名称 1040 个、低质量或非英文描述 851 个、加密货币/区块链/金融/交易相关 886 个、恶意（安全审计发现）373 个，总计排除 7215 个技能。最终精选 5400+ 个技能，分为 30 个类别。

技能分为以下大类：Git & GitHub（167 个）、Coding Agents & IDEs（1184 个）、Browser & Automation（323 个）、Web & Frontend Development（920 个）、DevOps & Cloud（393 个）、Image & Video Generation（170 个）、Speech & Transcription（46 个）、Notes & PKM（69 个）、Search & Research（345 个），以及 Apple Apps、Security、Gaming 等。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| OpenClaw 使用者 | ✅ 推荐 | 这是官方生态中最大的技能发现入口，必须收藏 |
| Claude Code / AI Agent 开发者 | ✅ 推荐 | 大量技能概念和实现可参考，开阔思路了解 Agent 能做什么 |
| 想找特定工作流自动化方案的用户 | ✅ 推荐 | 30 个分类覆盖几乎所有 AI Agent 应用场景 |
| 想贡献或发布个人技能到社区的开发者 | ✅ 推荐 | 提供清晰的技能发布和收录流程 |
| 不使用 OpenClaw/Claude Code 的用户 | ⚠️ 酌情 | 技能基于 OpenClaw 生态，但概念和思路可跨平台参考 |
| 需要安全审查的企业用户 | ⚠️ 酌情 | 合集仅策展不审计，技能可能被源作者随时修改。团队建议使用 Snyk Agent Scanner 自查 |

## 安装与前置条件

- **OpenClaw CLI** 或 **ClawHub CLI**（用于安装技能）

```bash
# OpenClaw CLI 安装技能
openclaw skills install <skill-slug>

# 或使用 ClawHub CLI
npx clawhub install <skill-slug>

# 也可将技能 GitHub 链接直接粘贴到 AI 对话中
# AI 助手会自动处理后台上设置
```

技能安装位置：
- 全局：`~/.openclaw/skills/`
- 工作区：`<project>/skills/`
- 优先级：Workspace > Local > Bundled

## 核心用法

### 浏览技能

直接访问 [awesome-openclaw-skills README](https://github.com/VoltAgent/awesome-openclaw-skills) 按类别浏览，或访问 [clawskills.sh](https://clawskills.sh) 在线搜索。

### 主要分类概览

| 分类 | 技能数量 | 典型场景 |
|------|----------|----------|
| Coding Agents & IDEs | 1184 | 代码生成、调试、重构、测试自动化 |
| Web & Frontend | 920 | 网站搭建、前端组件生成、样式设计 |
| DevOps & Cloud | 393 | 部署、监控、CI/CD、容器管理 |
| Search & Research | 345 | 网页搜索、学术研究、数据采集 |
| Browser & Automation | 323 | 浏览器自动化、表单填写、数据抓取 |
| Productivity & Tasks | 206 | 任务管理、日程规划、习惯追踪 |
| CLI Utilities | 180 | 命令行工具、终端增强 |
| Image & Video | 170 | AI 图片/视频生成、编辑、处理 |
| Git & GitHub | 167 | PR 管理、代码审查、仓库操作 |
| Communication | 146 | 邮件、Slack、消息平台集成 |
| Notes & PKM | 69 | 笔记管理、知识库、Obsidian 集成 |
| Speech & Transcription | 46 | 语音合成、转写、播客生成 |

### 安全提醒

> Agent 技能可能包含提示注入、工具投毒、隐藏恶意载荷或不安全的数据处理模式。安装前务必审查源代码，自行判断使用风险。

推荐安全审查工具：
- [Snyk Skill Security Scanner](https://github.com/snyk/agent-scan)
- [Agent Trust Hub](https://ai.gendigital.com/agent-trust-hub)
- ClawHub 技能页面的 VirusTotal 报告

## 注意事项与风险

- **策展不等于审计**：技能可能被原作者随时更新、修改或替换。入选列表不代表安全审查通过
- **安全自查是必须的**：列表中明确提到已排除 373 个恶意技能，说明注册中心存在安全隐患
- **技能质量参差不齐**：即使通过了策展筛选，从 7200+ 中挑出的 5400+ 也意味着质量分布很广
- **生态锁定**：这些技能专为 OpenClaw 构建，如果迁移到其他 Agent 平台（如 Claude Code Skills），可能需要适配

## 与你现有工具的关系

- OpenClaw Skills 的概念与 Claude Code Skills（本 Tags 目录下多个笔记如 [[Claude Code Humanizer：用 Claude Code Humanizer 提升文章可读性]]、[[Claude Code 自动化剪辑：基于 Claude Code 的自动化剪辑工作流]]、[[axton-obsidian-visual-skills：Obsidian 可视化技能包]]）类似，但生态更大、技能数量更多
- 本合集可作为发现新工具和自动化思路的灵感来源，筛选后迁移到 Claude Code 生态

## FAQ

### Q: 和 Claude Code Skills 有什么区别？
A: OpenClaw Skills 是为 OpenClaw（原名 Clawdbot）设计的，Claude Code Skills 是为 Anthropic 的 Claude Code CLI 设计的。两者概念类似（基于 Markdown 的提示词扩展），但布局和调用方式有差异，不完全兼容。

### Q: 这个合集多久更新一次？
A: 项目有 406 次提交，持续活跃更新。数据通过 GitHub Actions 工作流从 ClawHub 注册中心自动同步。

### Q: 如何贡献技能？
A: 技能必须先发布到 [ClawHub](https://clawhub.ai) 注册中心。在 PR 中包含技能的 ClawHub 链接即可。不接受个人仓库或 Gist 的链接。

### Q: 合集可靠吗？
A: 策展筛选了大量垃圾内容，但 5400+ 技能的策展深度有限。建议对每个安装的技能做自主安全审查。

## 相关链接

- GitHub：https://github.com/VoltAgent/awesome-openclaw-skills
- 在线搜索：https://clawskills.sh
- ClawHub 注册中心：https://clawhub.ai
- OpenClaw 官方：https://github.com/VoltAgent/voltagent
- Discord 社区：https://s.voltagent.dev/discord
