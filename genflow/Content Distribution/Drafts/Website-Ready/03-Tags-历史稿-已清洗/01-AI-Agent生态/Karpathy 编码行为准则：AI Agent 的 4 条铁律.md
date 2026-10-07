---
title: "Karpathy 编码行为准则：AI Agent 的 4 条铁律"
slug: karpathy-agent-coding-guidelines
date: 2026-05-25
updated: 2026-05-29
tags: [Karpathy, AI Agent, 编码规范, 最佳实践, Cursor]
categories: [最佳实践]
summary: Andrej Karpathy 总结的 4 条 AI 编码铁律：先想再写、简洁优先、外科手术式修改、目标驱动执行。适用于 Cursor、Claude Code、Codex、OpenCode，可减少过度工程与无关 diff。
focus_keyword: Karpathy 编码准则
source: https://github.com/multica-ai/andrej-karpathy-skills
status: draft
---

# Karpathy 编码行为准则：AI Agent 的 4 条铁律

> 源自 Karpathy 对 LLM 编码陷阱的观察 | 原始推文：https://x.com/karpathy/status/2015883857489522876

## 这是什么

将 Andrej Karpathy 关于 LLM 写代码常见问题的观察，蒸馏为可放入 `CLAUDE.md`、`.cursor/rules/` 或 Agent skill 的 **4 条行为规范**。仓库：[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)。

**Karpathy 原话（节选）：**

> 模型会替你做错假设并一路执行；不管理困惑、不求澄清、不呈现权衡、该反驳时不反驳。
> 爱过度复杂化、堆抽象、不清理死代码……100 行能搞定却写 1000 行。
> 有时误改无关注释与代码。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 使用 Cursor / Codex / OpenCode 的开发者 | ✅ 强烈推荐 | 直接降低 PR 噪音 |
| 团队统一 Agent 规范 | ✅ 推荐 | 可写入共享 rules |
| 单行 typo、显而易见的小改 | ⚠️ 酌情简化 | 准则偏谨慎，非教条 |
| 非编码类 Agent（纯写作） | ⚠️ 部分适用 | 「外科手术式修改」等可改写为编辑规范 |

## 安装与前置条件

无需安装二进制。将准则合并到：

- 项目 `CLAUDE.md` / `AGENTS.md`
- `.cursor/rules/*.mdc`
- OpenCode / Claude Code skill 目录

本 vault 已在 `.cursor/rules/karpathy-guidelines.mdc` 应用类似内容。

## 核心用法

### 1. Think Before Coding（先想再写）

- 明确假设；不确定就问
- 多种解读时**全部呈现**，不默默选一个
- 有更简单方案就指出；该反驳就反驳
- 不清楚就停下来提问

### 2. Simplicity First（简洁优先）

- 不实现未要求的功能
- 不为单次使用抽象
- 不做未要求的「灵活性」
- 200 行能搞定别写 1000 行

**判据**：资深工程师会觉得过度复杂吗？

### 3. Surgical Changes（外科手术式修改）

- 不「顺手优化」相邻代码
- 不重构没坏的东西；匹配现有风格
- 无关死代码：提一嘴，不擅自删
- 只删**你这次改动**导致的孤儿 import/变量

### 4. Goal-Driven Execution（目标驱动执行）

| 别说 | 改说 |
|------|------|
| 加个校验 | 先写无效输入测试，再让它通过 |
| 修这个 bug | 先写复现测试，再修到通过 |
| 重构 X | 确保重构前后测试全过 |

多步骤任务：

```
1. [步骤] → 验证: [检查项]
2. [步骤] → 验证: [检查项]
```

### 如何判断生效

- diff 无关改动变少
- 因过度复杂而重写次数减少
- 澄清出现在实现之前
- PR 干净、最小化

## 注意事项与风险

- **速度 vs 谨慎**：非琐碎任务收益大；简单任务可 judgment 跳过完整流程。
- **不是银弹**：无法替代 code review 与测试。
- **与 Helio 等团队产品**：Multica 团队亦整理此准则，见 [[Helio：AI 即同事的团队工作空间]]。

## 与你现有工具的关系

适用于 **Cursor、Claude Code、Codex、Copilot、OpenCode** 等全部编码 Agent。与 [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 中的全权限配置配合时，准则尤其重要以防 Agent 越权大改。

## FAQ

### Q: 和一般「你是资深工程师」prompt 有何不同？
A: 强调可验证目标、显式权衡、禁止顺手重构，更可执行。

### Q: 能否只采用其中一条？
A: 可以，但四条互补：Think → Simplicity → Surgical → Goal-Driven。

### Q: 开源仓库在哪？
A: https://github.com/multica-ai/andrej-karpathy-skills

## 相关链接

- 原始推文：https://x.com/karpathy/status/2015883857489522876
- Skills 仓库：https://github.com/multica-ai/andrej-karpathy-skills
- 本库：`.cursor/rules/karpathy-guidelines.mdc`
