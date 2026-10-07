---
title: "AIMedia：全自动 AI 媒体创作与多平台发布"
slug: aimedia-auto-publish-ai-media
date: 2026-05-29
updated: 2026-05-29
tags: [AIMedia, 自媒体, Django, 热点, 自动发布]
categories: [AI工具]
summary: AIMedia 自动抓取抖音/微博等热点，AI 生成图文并发布头条、公众号、小红书等。Django 后端 + PySide6 桌面端，工程量大；轻量替代见 MediaFlow 与 AiMaster 爬虫插件。
focus_keyword: AIMedia
source: https://github.com/Anning01/AIMedia
author: Anning01
status: draft
---

# AIMedia：全自动 AI 媒体创作与多平台发布

> 2,195+ stars | Django 5 + PySide6 | 工程级重量项目

## 这是什么

[AIMedia](https://github.com/Anning01/AIMedia) 是**全自动托管 AI 媒体软件**：自动抓取热点 → AI 创作文章/配图 → 自动发布到**今日头条、企鹅号、微信公众号、百家号**等（README 亦提及小红书等能力演进）。

架构：

- **back/** — Django REST API、任务调度、热点抓取、AI 生成、发布管理  
- **pyside/** — PySide6 桌面客户端、配置与监控  

技术：Django 5、DRF、智谱 AI、Stable Diffusion、Selenium + Chrome。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 有 Django 部署经验、做多平台矩阵 | ⚠️ 可尝试 | 完整前后端，非开箱即用 |
| 只想轻量发文/插件爬虫 | ❌ 过重 | 官方推荐 [MediaFlow](https://mediaflow.daniu7.cn)、[AiMaster](https://github.com/Anning01/AiMaster) |
| 不愿配置微信支付/登录/数据库 | ❌ 不推荐 | 集成企业级组件 |
| 仅想学热点爬虫 | ✅ 另仓库 | [article-spider](https://github.com/Anning01/article-spider) |

## 安装与前置条件

**⚠️ 工程级部署**，README 明确不适合「下载即用」：

- 自行部署 Django（SQLite / PostgreSQL / MySQL）  
- 打包 PySide6 桌面端  
- 配置智谱 AI、SD、Selenium Chrome 驱动  
- 可选：微信支付、微信登录商户与回调  

轻量方向（作者说明）：

- 新版 **MediaFlow**：FastAPI + 浏览器插件 + 公众号 API — [官网](https://mediaflow.daniu7.cn/login?code=GAGWP9UK)  
- 插件爬虫：**AiMaster**  
- 仅爬虫：[article-spider](https://github.com/Anning01/article-spider)  

具体 `back/`、`pyside/` 步骤见仓库文档（需自行阅读当前 README 部署章节）。

## 核心用法

### 热点抓取（已支持节选）

抖音、网易、微博、澎湃、中国日报、搜狐等。

### AI 创作

- 基于热点自动生成文章  
- AI 配图（提升原创率）  
- 多平台内容适配  

### 发布与管理

- 头条、企鹅号、公众号、百家号等  
- Django Admin + 桌面端任务监控  
- 任务调度、配置面板  

## 注意事项与风险

- **合规**：自动抓取与批量发布可能违反平台规则，存在封号风险；需人工审核内容。  
- **维护重心**：作者表示本仓库偏**稳定性维护**，新功能在 MediaFlow / AiMaster。  
- **部署成本**：支付、登录、数据库、浏览器自动化运维门槛高。  
- **内容质量**：热点追风易同质化，需编辑把关与 [[Karpathy 编码行为准则：AI Agent 的 4 条铁律]] 式「目标与验证」流程（若接 Agent 改写）。  

## 与你现有工具的关系

- 写作源头可在 Obsidian + [[给 Obsidian 接上免费 AI：opencode + 国产模型配置指南]]；AIMedia 偏**全自动发布管线**。  
- 图文排版：[[html-anything：AI 时代的 HTML 编辑器]]（公众号 HTML）、[[codex-ppt-skill：图片式 PPT 生成 Skill]]（演示）。  
- SEO 发布：vault 内 `opencode-WP-SEO` 偏 WordPress；AIMedia 偏国内自媒体矩阵。

## FAQ

### Q: 和 MediaFlow 选哪个？
A: 要开箱轻量用 MediaFlow；要完整自建、可控全栈才考虑 AIMedia。

### Q: 只有爬虫需求怎么办？
A: 直接用 [article-spider](https://github.com/Anning01/article-spider) 或 AiMaster 插件版。

### Q: 支持小红书自动发吗？
A: README 功能列表以头条/公众号等为主；小红书以仓库最新说明与 MediaFlow 为准。

## 相关链接

- GitHub：https://github.com/Anning01/AIMedia  
- MediaFlow：https://mediaflow.daniu7.cn  
- AiMaster：https://github.com/Anning01/AiMaster  
- B 站介绍：https://www.bilibili.com/video/BV1Xkw1zMEP7
