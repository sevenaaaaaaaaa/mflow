---
title: "GEOFlow：开源自托管 AI 内容生产系统"
slug: geoflow
date: 2026-06-15
updated: 2026-06-16
tags: [GEO, 内容生产, 自托管, 多站点分发]
categories: [AI工具]
summary: "GEOFlow 是面向生成式引擎优化（GEO）的开源智能内容工程与多站点分发系统，集成知识库/RAG、多模型 AI 生成、审核发布、数据分析、WordPress 分发等功能，PHP/Laravel + PostgreSQL + Docker 部署，2.6k Stars，Apache-2.0 协议。"
focus_keyword: "GEOFlow"
source: https://github.com/yaojingang/GEOFlow
author: "yaojingang"
status: draft
---

# GEOFlow：开源自托管 AI 内容生产系统

> 知识库 → AI 生成 → 审核发布 → 多站点分发 → 数据分析，全链路闭环 | 2.6k Stars | Apache-2.0 | PHP/Laravel + PostgreSQL + Docker

## 这是什么

GEOFlow 是一套专门面向 GEO（Generative Engine Optimization，生成式引擎优化）的开源智能内容工程与多站点分发系统。它将知识库、素材库、提示词、AI 生成任务、审核发布、数据分析和多站点分发串联为一条可持续运营的工作链路，目标是帮助团队把可信资料沉淀为可管理、可发布、可追踪、可同步到多端的 GEO 内容资产。

系统架构基于 PHP/Laravel 8.2+，数据库使用 PostgreSQL（推荐 pgvector 扩展做向量检索），队列和缓存由 Redis 驱动，开发和生产环境均提供 Docker Compose 一键部署。关键能力包括：多模型 AI 内容生成（兼容 OpenAI 风格接口和 Gemini 原生接口）、知识库上传与 RAG 召回、语义切片规划、素材库集中管理（标题/关键词/图片/作者/提示词）、任务调度与队列执行、审核发布流程、以及 GEOFlow Agent / WordPress REST / 通用 HTTP API 三种渠道的目标站点分发。分发后可在目标站点生成静态首页、详情页、sitemap、TXT 地图和 llms.txt。

GEOFlow 2.0 版本重点更新了后台首页运营导航、Gemini 与 OpenAI-compatible 的完整接入、知识库语义切片规划、独立数据分析页、分销闭环、以及 6 种语言的完整后台翻译支持。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要建立独立 GEO 官网的内容团队 | ✅ 推荐 | 全链路内容生产与分发，适合做 AI 搜索友好型内容资产 |
| 需要管理多站点/多栏目的运营团队 | ✅ 推荐 | 支持多模板、多栏目、多域名，统一管理多个内容出口 |
| SEO 从业者转型 GEO 方向 | ✅ 推荐 | 内置 SEO 元信息、Schema、sitemap、llms.txt，覆盖传统 SEO 和 AI 搜索优化 |
| 希望通过知识库沉淀打造行业信源站的团队 | ✅ 推荐 | 知识库建设和 RAG 召回是核心设计，强调"先建知识库，再建自动化" |
| 需要私有化部署和自托管的团队 | ✅ 推荐 | Docker 一键部署，数据库和内容完全自主可控 |
| 个人博客或轻量内容需求 | ⚠️ 酌情 | 系统功能较重，个人用户可能用不到多站点分发和队列调度 |
| 不需要 AI 生成的纯静态站点 | ❌ 不推荐 | 系统核心价值在 AI 生成和自动化，纯手工写作的场景更适合静态站点生成器 |

## 安装与前置条件

- **PHP 8.2+**（Docker 镜像可为 8.4），启用 `pdo_pgsql`、`redis` 等扩展
- **PostgreSQL**（推荐 pgvector 镜像）
- **Redis**（队列/缓存）
- **Docker 20.10+**（推荐） 或 手动安装 Composer 2.x

```bash
# Docker 开发环境一键部署（推荐）
git clone https://github.com/yaojingang/GEOFlow.git
cd GEOFlow
cp .env.example .env
# 按需编辑 .env（数据库、Redis、APP_URL 等）
docker compose build
docker compose up -d

# 前台默认访问：http://localhost:18080
# 后台登录：http://localhost:18080/geo_admin/login
# 默认账号：admin / password（生产环境请设置 GEOFLOW_ADMIN_PASSWORD 环境变量）

# 生产环境 Docker 部署
cp .env.prod.example .env.prod
docker compose --env-file .env.prod -f docker-compose.prod.yml build
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d postgres redis
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d init
docker compose --env-file .env.prod -f docker-compose.prod.yml up -d app web queue scheduler reverb
```

## 核心用法

### 三步上手

1. **配置 API**：至少添加一个可用 chat 模型；如需 RAG 召回，再添加 embedding 模型，并选择知识库切片策略
2. **配置素材库**：准备知识库、标题库、关键词库、图片库和作者。知识库建议先用真实、可验证的业务资料
3. **新建任务**：选择标题库、素材、模型、生成数量、发布频率和发布范围，先让文章进入草稿或审核流程，再逐步开启自动发布与多站点分发

### 核心功能模块

| 模块 | 功能 |
|------|------|
| AI 模型配置 | OpenAI 兼容接口 + Gemini 原生接口，支持 chat/embedding 模型，智能切换与重试 |
| 知识库与 RAG | 上传知识库 → 结构化规则切片 / 可选 LLM 语义规划 → 向量召回 → 文章上下文注入 |
| 素材与提示词库 | 标题库、关键词库、图片库、作者库、正文提示词、特殊提示词集中管理 |
| 任务自动化 | 生成数量、草稿池、审核开关、发布节奏、队列执行、失败重试 |
| 审核与文章管理 | 草稿/审核/发布/回收站流程，SEO 字段和任务来源统一管理 |
| 多站点分发 | GEOFlow Agent / WordPress REST / HTTP API 三种渠道，密钥管理、站点包下载 |
| 数据分析 | 系统总览、单站运营、多站分发、访问日志、Top 内容、AI 爬虫趋势 |
| SEO 输出 | SEO 元信息、Open Graph、Schema、GFM Markdown、独立 CSS、sitemap、llms.txt、TXT 地图 |

### 调用链路

```
后台管理页面
    ↓
AI 配置 / 素材库 / 提示词 / 任务配置
    ↓
调度器 / 队列 / Worker 执行 AI 生成
    ↓
草稿 / 审核 / 发布
    ↓
本地前台文章与 SEO 页面
    ↓
分发队列 / 目标站点 Agent
    ↓
远端静态首页、详情页、sitemap、TXT 地图与 llms.txt
```

## 注意事项与风险

- **知识库质量决定内容质量**：如果知识库本身不真实、不完整，AI 生成的内容只会放大噪音。文档反复强调"先建知识库，再建自动化"
- **管理员登录锁定**：连续 5 次登录失败自动锁定，可用 `php artisan geoflow:admin-unlock <username>` 解锁
- **生产环境安全**：务必修改默认管理员密码，设置环境变量 `GEOFLOW_ADMIN_PASSWORD`；使用 Nginx+PHP-FPM 方案（`docker-compose.prod.yml`），不要暴露 `php artisan serve` 到公网
- **向量检索依赖 pgvector**：知识库 RAG 功能需要 PostgreSQL 安装 pgvector 扩展，Docker Compose 默认包含 pgvector 镜像
- **升级流程**：`git pull → docker compose build → docker compose up -d`，注意备份 `.env` 和 storage 目录

## 与你现有工具的关系

- GEOFlow 生成的内容可经由 [[../01-AI-Agent生态/Claude Code Humanizer：用 Claude Code Humanizer 提升文章可读性]] 做 AI 去痕润色后发布
- 与 [[../02-内容创作媒体/Toonflow：开源 AI 短剧生成工具]] 互补：GEOFlow 负责图文内容，Toonflow 负责短剧视频内容
- [[../01-AI-Agent生态/Claude Code 自动化剪辑：基于 Claude Code 的自动化剪辑工作流]] 可作为视频内容生产端，素材由 GEOFlow 管理

## FAQ

### Q: GEO 和 SEO 有什么区别？
A: SEO 优化搜索引擎排名，GEO 优化生成式 AI（如 ChatGPT、Gemini、Perplexity）对你内容的引用和推荐。GEOFlow 同时兼顾两者的输出（sitemap + llms.txt + Schema）。

### Q: 免费吗？可以商用吗？
A: Apache-2.0 协议，允许个人和企业自由使用、修改、分发和商用，需保留版权声明和许可证文本。

### Q: 支持哪些 AI 模型？
A: 兼容 OpenAI 风格接口（GPT-5、Claude、DeepSeek、智谱、MiniMax、通义千问、xAI 等）和 Gemini 原生接口。支持 chat 和 embedding 两种模型类型。

### Q: 需要多少服务器资源？
A: 最小配置：2GB 内存 + 双核 CPU 即可运行。PostgreSQL + Redis + PHP-FPM 是主要资源消耗点。大批量 AI 生成任务可能需要更多的队列 Worker 和 API 调用预算。

### Q: 学习成本高吗？
A: 如果熟悉 Docker 和 Laravel 生态，上手很快（三步引导即可跑通）。对非技术人员，建议有运维支持或使用 Docker 一键部署方案。

## 相关链接

- 来源：https://www.ahhhhfs.com/80289/
- GitHub：https://github.com/yaojingang/GEOFlow
- 部署脚本：https://raw.githubusercontent.com/yaojingang/GEOFlow/main/deploy-scripts/geoflow-docker-deploy.sh
