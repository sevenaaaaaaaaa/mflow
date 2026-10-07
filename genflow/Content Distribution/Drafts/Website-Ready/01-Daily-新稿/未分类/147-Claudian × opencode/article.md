---
title: "Claudian × opencode：免费模型接入 Obsidian 的三通道架构"
slug: claudian-opencode-obsidian-three-channels
date: 2026-05-25
updated: 2026-05-29
tags: [Claudian, opencode, Obsidian, OpenRouter, 免费模型]
categories: [AI工具]
summary: 在 Obsidian Claudian 中增加 opencode 第三通道，用 OpenRouter 免费 Ling-2.6-1T 处理翻译与杂活，Claude 写稿、Codex 编程、opencode 零成本分工。含 CC Switch 与常见坑点。
focus_keyword: Claudian opencode
source: https://x.com/alin_zone/status/2049482987402899559
author: 阿蔺A-Lin (@alin_zone)
status: draft
---

# Claudian × opencode：免费模型接入 Obsidian 的三通道架构

> 阿蔺A-Lin 系列第三篇 | 310 👍 | 124k 浏览

## 这是什么

在 Obsidian **Claudian** 插件里，为 Claude + Codex 之外增加**第三条免费通道 opencode**，挂载 OpenRouter 上的 **Ling-2.6-1T 免费模型**。

```
CLAUDE   → 写作/思考/复杂推理（已有订阅）
CODEX    → 编程/改 bug（ChatGPT 账号）
OPENCODE → 翻译/总结/日常杂活（免费，零成本）
```

完整 MiMo 配置见 [[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]（另一套国产免费方案）。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 已有 Claudian + Claude/Codex 的 Obsidian 用户 | ✅ 推荐 | 低成本分担杂活 |
| 愿折腾 CC Switch / opencode CLI | ✅ 推荐 | 约 12–15 分钟配置 |
| 从未用过 Obsidian | ❌ 先装 Obsidian + Claudian |
| 只要单一模型 | ❌ 三通道增加认知负担 |

## 安装与前置条件

1. **OpenRouter Key** → 搜 `inclusionai/ling-2.6-1t:free` → 复制模型 ID  
2. **opencode CLI**：`curl -fsSL https://opencode.ai/install | bash` → 运行一次 `opencode` 生成 `~/.config/opencode/`  
3. **CC Switch**（最新版，含 Opencode tab）  
4. **Claudian**（最新版，含 Opencode tab）

## 核心用法

### 技术链路（12–15 分钟）

1. OpenRouter Key + 模型 ID  
2. 安装 opencode CLI 并首次运行  
3. CC Switch → OpenCode 供应商 → 添加 OpenRouter → **删默认模型只留 Ling** → 启用  
4. `opencode` → `/models` → 选中 ling → 验证  
5. Claudian → Opencode tab → CLI Path → 清占位模型 → 勾选 ling  

### 关键坑点

- opencode CLI **必须先跑一次**，Claudian 才能读到 `/models`  
- Claudian / CC Switch 需**最新版**才有 Opencode tab  
- CC Switch **各 tab API Key 独立**，不跨 tab 同步  
- 模型列表默认行**全删**，只留自用模型  
- 三通道**对话历史完全隔离**

## 注意事项与风险

- **免费额度截止**：原文提及 Ling 免费至 2026-05-07，之后可能收费，需关注 OpenRouter。  
- **模型能力**：杂活可用，复杂推理仍建议 Claude 通道。  
- **配置漂移**：升级 Claudian/CC Switch 后检查 tab 是否仍在。

## 与你现有工具的关系

- 与 [[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 并列：OpenRouter Ling vs 小米 MiMo。  
- opencode 还可挂 [[../01-AI-Agent生态/The Agency：105k Star 的 AI Agent 专家库]]、[[../01-AI-Agent生态/codex-ppt-skill：图片式 PPT 生成 Skill]]。

## FAQ

### Q: 必须三个通道都开吗？
A: 否，但分工清晰时 token 成本最低。

### Q: opencode 路径填什么？
A: `which opencode` 结果，Claudian Opencode tab 中填写。

### Q: CC Switch 是什么？
A: 管理多供应商 API 与模型列表的桌面工具，本文用于配置 OpenRouter。

## 相关链接

- 原文：https://x.com/alin_zone/status/2049482987402899559  
- opencode：https://opencode.ai  
- 本库：[[../01-AI-Agent生态/给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]
