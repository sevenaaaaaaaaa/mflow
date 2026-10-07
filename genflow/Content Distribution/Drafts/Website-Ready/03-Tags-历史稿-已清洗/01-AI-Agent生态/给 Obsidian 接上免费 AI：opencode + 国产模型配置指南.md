---
title: "给 Obsidian 接上免费 AI：opencode + 国产模型配置指南"
slug: obsidian-opencode-free-ai-guide
date: 2026-05-24
updated: 2026-05-29
tags: [Obsidian, OpenCode, AI, 国产模型, 配置]
categories: [AI工具]
summary: Claude 封号不稳？用小米 MiMo 等国产免费模型 + opencode，在 Obsidian 内获得 1M 上下文、全权限 AI 通道。含完整 JSON 配置、agency-agents 与 codex-ppt 组合工作流。
focus_keyword: Obsidian opencode
source: https://x.com/alin_zone/status/2049482987402899559
status: draft
---

# 给 Obsidian 接上免费 AI：opencode + 国产模型配置指南

> 1M context | 国产节点 | 零订阅成本

## 这是什么

在 Obsidian 中通过 **opencode** 接入国产大模型（如小米 MiMo），替代不稳定的海外的 Claude 订阅通道。参考 [@alin_zone](https://x.com/alin_zone) 的 Claudian × opencode 方案：用免费/低成本模型完成翻译、总结、写作与工具调用。

另见三通道架构：[[../03-效率生产力/Claudian × opencode：免费模型接入 Obsidian 的三通道架构]]。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| Obsidian 重度用户、需本地知识库 + AI | ✅ 推荐 | 全程在 vault 内完成 |
| 受 Claude 封号/订阅困扰的用户 | ✅ 推荐 | 国内节点更稳 |
| 只需单次 ChatGPT 网页对话 | ❌ 不推荐 | 配置成本偏高 |
| 企业合规禁止第三方 API | ⚠️ 需自评 | 确认 MiMo 等服务条款 |

## 安装与前置条件

- 已安装 **Obsidian** 与 **opencode**（及可选 Claudian 插件）
- 获取小米 MiMo 或兼容 OpenAI API 的 Key
- 可选：`~/.mavis/skills`、MCP（cdp-bridge、Sanity 等）

## 核心用法

### 模型配置

```json
{
"model": "xiaomi/mimo-v2.5-pro",
"small_model": "xiaomi/mimo-v2.5-pro",
"provider": {
"xiaomi": {
"npm": "@ai-sdk/openai-compatible",
"options": {
"baseURL": "https://token-plan-cn.xiaomimimo.com/v1"
},
"models": {
"mimo-v2.5-pro": {
"name": "MiMo-V2.5-Pro",
"options": { "include_reasoning": false },
"limit": { "context": 1048576, "output": 131072 }
}
}
}
}
}
```

| 配置项 | 值 | 说明 |
|--------|-----|------|
| 模型 | `xiaomi/mimo-v2.5-pro` | 免费国产模型 |
| Context | **1,048,576 tokens** | 可吞下整本书 |
| 输出 | **131,072 tokens** | 单次长文 |
| API | `token-plan-cn.xiaomimimo.com` | 国内低延迟 |
| 推理模式 | 关闭 | 省 token |

### 权限配置（全开示例）

```json
{
"permission": {
"*": "allow",
"question": "deny"
}
}
```

### Skills 与 MCP

- Skills：`~/.mavis/skills`、`~/.mavis/agents/main/skills`、`~/.mavis/.builtin-skills`
- MCP：cdp-bridge、Sanity 等远程 MCP

### 已安装的增强组件

- **184 个专业 Agent**（agency-agents）：`@content-creator 写一篇公众号` — 见 [[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]
- **codex-ppt-skill**：文章转 PPT — 见 [[codex-ppt-skill：图片式 PPT 生成 Skill]]
- **Scrapling**：opencode 内 Python 抓取

### 工作流示例

```
Obsidian 打开 opencode →
"@content-creator 根据这篇笔记写公众号" →
初稿 →
"请使用 codex-ppt skill 转成分享 PPT" →
获得 PPTX
```

## 注意事项与风险

- **权限全开**：`"*": "allow"` 方便但风险高，生产环境建议收紧文件/网络权限。
- **模型可用性**：免费额度与政策可能变化，需关注厂商公告。
- **三通道隔离**：Claude / Codex / opencode 对话历史互不共享，见 [[../03-效率生产力/Claudian × opencode：免费模型接入 Obsidian 的三通道架构]]。
- **API Key 安全**：勿将含 Key 的配置提交到公开仓库。

## 与你现有工具的关系

- 与 **Claudian + CC Switch + OpenRouter Ling** 方案互补，可并存多通道。
- 发布流水线见 vault 内 `opencode-WP-SEO`：Obsidian 写稿 → 优化 → WordPress。
- Tags 目录其他工具笔记（x-cli、GBrain、LLM Wiki）可作为 opencode 的 skill/知识来源。

## FAQ

### Q: 为什么选国产模型？
A: 免费额度、国内节点稳定、大上下文、减少封号焦虑。

### Q: agency-agents 和 Codex 内置 agent 区别？
A: agency-agents 是外部人格库；Codex 内置为另一套，见 [[The Agency：105k Star 的 AI Agent 专家库]]。

### Q: 1M context 实际够用吗？
A: 适合整库笔记摘要；极长对话仍建议分块与索引。

## 相关链接

- 参考文章：https://x.com/alin_zone/status/2049482987402899559
- 本库笔记：[[../03-效率生产力/Claudian × opencode：免费模型接入 Obsidian 的三通道架构]]、[[AI Agent 工具生态：从 184 个专业 Agent 到一键 PPT]]
