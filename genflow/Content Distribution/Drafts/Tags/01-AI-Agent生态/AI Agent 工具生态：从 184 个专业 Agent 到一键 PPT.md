---
title: "AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT"
slug: ai-agent-tools-ecosystem-pillar
date: 2026-05-24
updated: 2026-05-29
tags: [AI Agent, agency-agents, codex-ppt, OpenCode, 效率]
categories: [AI工具]
summary: 枢纽文：agency-agents 提供 184 个跨部门专业 Agent 人格，codex-ppt-skill 把文章一键转成图片式 PPT。配合 OpenCode 实现从写作到演示的 Agent 创作流水线。
focus_keyword: AI Agent 工具生态
source: https://github.com/msitarzewski/agency-agents
author: msitarzewski / ningzimu
status: draft
---

# AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT

> Pillar 文 | 串联 Tags 目录多工具笔记

## 这是什么

两篇核心能力组成「Agent 时代创作流水线」：

1. **[agency-agents](https://github.com/msitarzewski/agency-agents)** — 184 个专业 Agent 人格（⭐ 105k），12 大部门，强人格 + 交付物 + 成功指标。详见 [[The Agency：105k Star 的 AI Agent 专家库]]。  
2. **[codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill)** — 文章/报告一键转**图片式 PPT**。详见 [[codex-ppt-skill：图片式 PPT 生成 Skill]]。

在 **OpenCode + Obsidian** 中组合使用，见 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 内容创作者、运营、独立开发者 | ✅ 推荐 | 写作 + 演示一条龙 |
| 已用 opencode / Cursor 的用户 | ✅ 推荐 | 一键 `./scripts/install.sh` |
| 只需单次 Chat 对话 | ❌ 不推荐 | 安装与 @agent 学习成本 |
| 需要可编辑 PPT 母版 | ⚠️ 注意 | codex-ppt 为图片页，可编辑性弱 |

## 安装与前置条件

### agency-agents

```bash
./scripts/install.sh --tool opencode    # 或 cursor / claude-code
```

Agent 安装至 `.opencode/agents/` 等路径。

### codex-ppt-skill

```bash
npx skills add ningzimu/codex-ppt-skill --agent codex
# 或见 codex-ppt 笔记中的各 Agent 安装方式
```

## 核心用法

### agency-agents 部门示例

| 部门 | 代表角色 |
|------|----------|
| Engineering | Frontend/Backend/AI Engineer、Code Reviewer |
| Design | UI/UX Designer、Brand Guardian |
| Marketing | 小红书/公众号/B站/抖音/SEO 等 |
| Product / Sales / Testing | PM、Deal Strategist、Reality Checker |

使用：`@content-creator 写一篇公众号`、`@code-reviewer 审查代码`。

### codex-ppt 工作流

```
阅读内容 → 规划大纲 → 选风格 → 样张确认 → 逐页生成 → 组装 .pptx
```

9 种视觉风格；优先 Codex 内置生图，零 API key 可选。

### 组合最佳实践

1. **写文章** → OpenCode + `@content-creator`  
2. **转 PPT** → `请使用 codex-ppt skill 做成 10 页 PPT`  
3. **设计审校** → `@UI Designer`  
4. **发布前** → `@Reality Checker`  

## 注意事项与风险

- **184 vs 144**：不同统计口径（角色/事业部），以仓库 README 为准。  
- **与 Codex 内置 agent**：外部人格库，与 IDE 内置互补，非替代。  
- **PPT 版权与品牌**：生图内容需自行合规审核。  
- **模型成本**：长文 + 多页生图消耗 token/额度。

## 与你现有工具的关系

| 笔记 | 关系 |
|------|------|
| [[The Agency：105k Star 的 AI Agent 专家库]] | agency-agents 深度介绍 |
| [[codex-ppt-skill：图片式 PPT 生成 Skill]] | PPT skill 细节 |
| [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] | 运行环境 |
| [[../03-效率生产力/Claudian × opencode：免费模型接入 Obsidian 的三通道架构]] | 免费模型通道 |

## FAQ

### Q: agency-agents 和 The Agency 是一回事吗？
A: 是，同一仓库 `msitarzewski/agency-agents`。

### Q: 没有 Codex 能用 codex-ppt 吗？
A: 支持 Claude Code、OpenClaw、Hermes 等，多走 API fallback。

### Q: 安装到 Cursor 后怎么用？
A: `./scripts/install.sh --tool cursor`，规则进 `.cursor/rules/`。

## 相关链接

- agency-agents：https://github.com/msitarzewski/agency-agents  
- codex-ppt-skill：https://github.com/ningzimu/codex-ppt-skill  
- 子笔记：[[The Agency：105k Star 的 AI Agent 专家库]]、[[codex-ppt-skill：图片式 PPT 生成 Skill]]
