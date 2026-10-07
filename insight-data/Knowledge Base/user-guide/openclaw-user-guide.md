---
type: knowledge/user-guide
source: https://lovart.notion.site/Lovart-OpenClaw-User-Guide-33da46b16a0f80f6a7fff8e4896b9fca
updated: 2026-09-18
category: product-docs
---

# Lovart OpenClaw User Guide（产品用户指南）

## 产品定位

Lovart 是一个**协作式 AI 工作空间**——用户通过 agent 对话描述视觉需求，Lovart 生成并交付设计。

## Agent 集成方式

| Agent Host | 说明 | 适用人群 |
|------------|------|---------|
| **OpenClaw Desktop** | 本地运行，最强大 | 个人创作者 |
| **Discord / Telegram** | 团队集成 | 团队协作 |
| **Slack Agent** | 专业工作区 | 企业用户 |

## 安装

1. **CLI**：`npx skills add lovartai/lovart-skills`
2. **下载**：lovart-skill.zip (16.6 KiB)

## 认证

需要 `access_key` + `secret_key`（从 Lovart.ai Settings 获取）：
```
LOVART_ACCESS_KEY="ak_xxx"
LOVART_SECRET_KEY="sk_xxx"
```

## 使用方式

认证后，用户通过对话描述愿景即可开始创作。
- **推荐模型**：GPT-5.4 / Claude 4.6 / Gemini 3.1（复杂 Skill 逻辑）
- **参考文件**：可上传图片/视频作为 style/structure reference

## 对 MFlow 的启示（写内容时可引用的事实）

1. Lovart Skill 系统是**公开可编程的**——不是黑盒 API
2. 支持多种 agent host（桌面/Discord/Telegram/Slack）→ 可覆盖这些场景写内容
3. 用户需要先获得 API Key → onboarding 内容可描述此流程
4. "describe your vision" 是核心交互模式 → 内容应围绕"如何描述设计需求"
5. 参考文件（图片/视频）是关键 feature → 可写 "how to use reference images" 类内容
