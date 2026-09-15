---
type: rule
version: 1.0
updated: 2026-07-05
scope: "profile-management-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-60-management.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 60 管理类（Management）

> 适用路线：项目管理、工程管理、知识管理、Hermes 优化
> 加载 Profile：`lovart-management`

---

## 三层目录架构

| 层 | 目录 | 定位 |
|---|------|------|
| 源码层 | `1-Project/Lovart MFlow/`（Obsidian vault） | 文档、脚本、SOP、Skills |
| 资源层 | `3-Resource/` | 大型数据集、Git object store |
| 运行层 | `$LOVART_LOCAL_DEV_ROOT`（`~/Documents/Lovart Local Dev/`） | 输出、缓存、拉取结果、日志 |

**规则**：源码不放大文件（>50MB 生成产物外置到运行层）。

## Profile 架构（6+2）

| Profile | 模型 | 用途 | 会话启动 |
|---------|------|------|---------|
| `lovart-reports` | deepseek-chat | SEO/舆情/竞品/SERP/OKR | `hermes -p lovart-reports` |
| `lovart-creation` | deepseek-v4-pro | Blog/Tools/Features/Landing 页 | `hermes -p lovart-creation` |
| `lovart-quality` | deepseek-chat | 质检/Anti-Slop/i18n 优化 | `hermes -p lovart-quality` |
| `lovart-ops` | deepseek-chat | Sitemap/IndexNow/CRO/素材 | `hermes -p lovart-ops` |
| `lovart-distribution` | deepseek-chat | 国内外内容分发 | `hermes -p lovart-distribution` |
| `lovart-management` | deepseek-chat | 项目/工程/知识/Hermes | `hermes -p lovart-management` |
| `lovart-seo` (legacy) | deepseek-chat | SEO 报告 cron | 保留 |
| `lovart-content` (legacy) | deepseek-v4-pro | 创作 cron | 保留 |

## 会话路由规则

1. **一条会话只做一类事**。不要在调研会话里执行发布，不要在创作会话里跑 SEO 报告。
2. **调研→清单→关闭→创作**。分析类工作产出结论/清单后关闭，创作类工作按清单执行。
3. **default 仅用于探索**。不确定该走哪条线时用 default，确定后切到对应 profile。

## Cron 自动化（12 任务）

| Cron | Profile | 周期 |
|------|---------|------|
| 每日舆情分析 | lovart-seo | 08:00 |
| 每日自媒体稿件 | lovart-content | 09:00 |
| 每天内容抽查 | lovart-seo | 14:00 |
| SEO 复盘周报 | lovart-seo | 周三 20:00 |
| 每周舆情报告 | lovart-seo | 周二 09:00 |
| 每周内容健康度 | lovart-seo | 周一 09:00 |
| 每周 Sitemap | lovart-seo | 周一 02:00 |
| 每周 i18n 缺口 | lovart-seo | 周五 10:00 |
| 每月 SEO 报告 | lovart-seo | 每月第一周三 |
| Tri 月度汇总 | lovart-seo | 每月 3 号 |
| SEO 季度汇总 | lovart-seo | 3/6/9/12月5号 |
| SEO 年度报告 | lovart-seo | 1月10号 |
| IndexNow 每日 | no-agent | 09:00 |
| 中国爬虫触发 | no-agent | 09:30 |

## 自动化层次

| 机制 | 执行者 | 适用 |
|------|--------|------|
| macOS launchd | launchctl | 纯脚本（数据采集、preflight） |
| Hermes cron | Hermes agent | 需要 LLM 分析的周期任务 |
| Kanban | dispatcher → worker profile | 批次任务流水线 |

## Hermes 优化原则

1. Skills 按需加载，不全量。创作会话只加载 creation 类 skill，报告会话只加载 reporting 类。
2. Memory 保持精简（<80%）。操作步骤放 skill pitfalls，不放 memory。
3. Skill Curator 7 天自动审计（已启用），闲置 30 天标记 stale。
4. Gateway 保持运行（当前 launchd PID 45625），12 cron deliver→origin。
5. delegate_task 仅用于独立推理子任务（<5 分钟）。铺量（50+ 篇）用主 agent Python 模板批量生成。

## 知识管理

- **SSOT**：Hermes Skills 是运行时真相，Obsidian 是分发包源。
- **新 Skill**：`skill_manage create` → `~/.hermes/skills/lovart/`
- **废弃文档**：移至 `1-8 Backup/archives/`，勿留 `_old`/`_v2` 后缀。
- **路径引用**：禁止硬编码，统一用 `$LOVART_RESOURCE_ROOT` / `$LOVART_LOCAL_DEV_ROOT`。
- **维护**：新增文档更新 `00-INDEX.md`。
