---
title: "GBrain：AI Agent 的个人大脑层"
slug: gbrain-ai-agent-memory-brain
date: 2026-05-25
updated: 2026-05-29
tags: [GBrain, AI Agent, 知识图谱, MCP, Garry Tan]
categories: [AI工具]
summary: GBrain 是 Garry Tan 开源的 Agent 记忆层：自维护知识图谱、混合检索与 gbrain think 合成答案，支持 MCP 与 24/7 富化。可导入 Obsidian vault，与 LLM Wiki 互补。
focus_keyword: GBrain
source: https://github.com/garrytan/gbrain
author: Garry Tan
status: draft
---

# GBrain：AI Agent 的个人大脑层

> 18.9k stars | MIT | TypeScript + Bun + PGLite

## 这是什么

> "Search gives you raw pages. GBrain gives you the answer."

[GBrain](https://github.com/garrytan/gbrain) 不是搜索引擎，而是 **AI Agent 的记忆大脑**——自维护知识图谱 + 混合检索 + 合成层 + 可选 24/7 梦境循环。Garry Tan 为 OpenClaw / Hermes 部署：大规模页面、人物、公司实体跑在之上。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 多 Agent（Cursor/Claude/Hermes）需统一记忆 | ✅ 推荐 | 30+ MCP 工具 |
| 已有 Obsidian vault 想 Agent 化查询 | ✅ 推荐 | `gbrain import` |
| 只需手动笔记、无自动化 | ⚠️ 可选 | [[LLM Wiki：让 AI 替你维护个人知识库]] 更贴阅读流 |
| 不愿本地跑 Postgres/PGLite | ❌ 需评估 | `gbrain init --pglite` 较轻量 |

## 安装与前置条件

```bash
# Agent 引导安装
# "Retrieve and follow: https://raw.githubusercontent.com/garrytan/gbrain/master/INSTALL_FOR_AGENTS.md"

# 或 CLI
bun install -g github:garrytan/gbrain
gbrain init --pglite    # 约 2 秒，无需 Docker
gbrain doctor
gbrain import ~/notes/
gbrain think "最关键的问题是？"
```

需 Bun；团队大脑可用 Postgres + pgvector。

## 核心用法

### 两种查询

```bash
gbrain search "portfolio 里谁在搞 AI agent"   # 排名页面列表
gbrain think "portfolio 里谁在搞 AI agent"    # 合成答案 + 引用 + 缺口
```

`think` 会标明「大脑不知道什么」（如未见邮件/Slack）。

### 自布线知识图谱

写入时自动提取实体与类型化边（`works_at`、`invested_in` 等），**零 LLM**。评测：P@5 49.1%，R@5 97.9%，较纯向量 RAG +31.4 P@5。

### 摄入

```bash
gbrain capture "想法"
gbrain capture --file ./notes/today.md
gbrain import ~/vault/
```

Webhook：Zapier / Shortcuts / 邮件 / 日历等。

### Schema 与 Skills

- `gbrain schema detect/suggest/use` — 7 层优先级  
- **43 个内置 Skill**：摄入、富化、cron、报告、eval 等  

架构：PGLite（个人）/ Postgres（团队）；Git markdown 为源 → 同步 DB。

## 注意事项与风险

- **数据主权**：大脑内容敏感，备份与加密自行负责。  
- **LLM 成本**：`think`、富化、cron 消耗 API。  
- **与 Obsidian 同步**：import 后 Obsidian 仍为主编辑源时，注意双向一致性。  
- **规模**：146k+ 页级部署需规划硬件与 Postgres。

## 与你现有工具的关系

| Obsidian / LLM Wiki | GBrain |
|---------------------|--------|
| 手动知识管理 | Agent 自动化大脑 |
| 手动链接 | 自动实体边 |
| 搜索 → 页面 | search/think → 答案+缺口 |
| 静态 | 24/7 富化可选 |

`gbrain import ~/vault/` 后 Agent 经 MCP 查询。与 [[LLM Wiki：让 AI 替你维护个人知识库]]、[[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]] 形成「写→存→想」链路。

## FAQ

### Q: search 和 think 怎么选？
A: 要快、要列表用 search；要结论、要缺口分析用 think。

### Q: 必须用 Docker 吗？
A: 个人 `--pglite` 不需要；大规模用 Postgres。

### Q: 和 RAG 插件区别？
A: 图谱多跳 + 合成层 + 持续富化，非一次性检索。

## 相关链接

- GitHub：https://github.com/garrytan/gbrain  
- INSTALL_FOR_AGENTS：https://raw.githubusercontent.com/garrytan/gbrain/master/INSTALL_FOR_AGENTS.md
