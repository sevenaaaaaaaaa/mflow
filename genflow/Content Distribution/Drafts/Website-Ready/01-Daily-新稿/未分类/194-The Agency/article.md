---
title: "The Agency：105k Star 的 AI Agent 专家库"
slug: agency-agents-expert-library
date: 2026-05-25
updated: 2026-05-29
tags: [agency-agents, AI Agent, 开源, 多角色, productivity]
categories: [AI工具]
summary: agency-agents（The Agency）收录 144+ 专业 Agent 人格，覆盖工程、设计、营销、销售等 12 事业部，一键安装到 Cursor、OpenCode、Claude Code 等 11 种 AI 工具。
focus_keyword: agency-agents
source: https://github.com/msitarzewski/agency-agents
author: msitarzewski
status: draft
---

# The Agency：105k Star 的 AI Agent 专家库

> 105k stars | MIT | 144 Agent | 12+ 事业部

## 这是什么

[agency-agents](https://github.com/msitarzewski/agency-agents) 是完整的 AI Agency 人格集合：每个 Agent 有**性格、流程、交付物、成功指标**，不是泛化 prompt。

设计哲学：强人格、明确交付、可衡量标准、成熟工作流、持续学习记忆。

枢纽文：[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 多角色任务（写稿+审代码+运营） | ✅ 推荐 | 按 @角色 切换 |
| opencode / Cursor / OpenClaw 用户 | ✅ 推荐 | 官方 install 脚本 |
| 只需单一通用助手 | ⚠️ 可选 | 角色过多可能选择困难 |
| 不愿维护本地 agent 目录 | ❌ 不推荐 | 需 clone + install |

## 安装与前置条件

```bash
git clone https://github.com/msitarzewski/agency-agents
cd agency-agents
./scripts/convert.sh
./scripts/install.sh                    # 交互检测已装工具
./scripts/install.sh --tool opencode --tool cursor --tool openclaw
```

| 工具 | 格式 | 路径 |
|------|------|------|
| Claude Code | .md | `~/.claude/agents/` |
| OpenCode | .md | `.opencode/agents/` |
| Cursor | .mdc | `.cursor/rules/` |
| OpenClaw | SOUL+AGENTS | `~/.openclaw/agency-agents/` |
| Copilot / Aider / Antigravity | 各异 | 见仓库 README |

## 核心用法

### 事业部概览（节选）

| 事业部 | Agent 数 | 典型角色 |
|--------|---------|----------|
| Engineering | 27 | Frontend、Backend、AI Engineer、SRE |
| Design | 8 | UI Designer、Brand Guardian |
| Marketing | 29 | 小红书、抖音、B站、公众号、SEO |
| Sales / Product / Testing / Game Dev 等 | … | 见仓库完整列表 |

### 使用示例

```
@frontend-developer 写一个 React 组件
@content-creator 写一篇公众号
@code-reviewer 审查这段代码
```

## 注意事项与风险

- **人格≠事实**：Agent 输出仍需人工核实，尤其法律、财务、医疗类角色。  
- **仓库体积与更新**：`convert.sh` 后文件较多，升级需重新 install。  
- **与 Codex 内置 agent**：外部库，与 IDE 内置互补（见生态枢纽文）。  
- **中文平台角色**：营销类 Agent 偏国内平台，海外场景需改 prompt。

## 与你现有工具的关系

你的 opencode、cursor、openclaw 均在支持列表。与 [[codex-ppt-skill：图片式 PPT 生成 Skill]]、[[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 组成写作→演示流水线。

## FAQ

### Q: 144 和 184 个 Agent 怎么理解？
A: 统计口径不同（角色数 vs 含变体/部门扩展），以 GitHub 当前 README 为准。

### Q: 能否只装 Marketing 部门？
A: 需查看 install 脚本是否支持筛选；默认全量安装。

### Q: 和 The Agency 品牌名关系？
A: 社区俗称 The Agency，仓库名 agency-agents。

## 相关链接

- GitHub：https://github.com/msitarzewski/agency-agents  
- 本库：[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]
