---
type: session-routing
version: 1.0
updated: 2026-07-05
scope: "all"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/SESSION-ROUTING.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart 会话路由指南

> 如何开正确的会话，做正确的事。一次会话只做一类事。

---

## 6 条工作线

| # | 工作线 | Profile | 启动命令 | 做什么 | 不做什么 |
|---|--------|---------|---------|--------|---------|
| 1 | 报告 | `lovart-reports` | `hermes -p lovart-reports` | SEO月报/周报、舆情日报、竞品分析、SERP调研、OKR看板 | 不写文章、不发布内容 |
| 2 | 创作 | `lovart-creation` | `hermes -p lovart-creation` | Blog/Tools/Features/Landing/Solution/Product/Scenario/Topic 页面 | 不跑SEO报告、不分发 |
| 3 | 质量 | `lovart-quality` | `hermes -p lovart-quality` | preflight、Anti-Slop检测、i18n审计、内容健康度 | 不写新内容、不调研 |
| 4 | 运维 | `lovart-ops` | `hermes -p lovart-ops` | Sitemap、IndexNow、CRO修复、图片素材替换 | 不改内容正文 |
| 5 | 分发 | `lovart-distribution` | `hermes -p lovart-distribution` | 国内(Wechatsync)/海外(DEV.to/GitHub/Blogger)分发 | 不创作原文 |
| 6 | 管理 | `lovart-management` | `hermes -p lovart-management` | 项目规划、工程优化、Skill维护、Profile调优 | 不执行内容操作 |

## 典型工作流

```
❌ 错误：一个会话里调研→分析→写文章→preflight→发布
✅ 正确：
  会话A (lovart-reports): "GSC数据分析，找出零点击但排名4-10的15篇Blog"
    → 产出改写清单 → 关闭

  会话B (lovart-creation): "按这份清单改写这15篇Blog"
    → 逐篇改写 → 关闭

  会话C (lovart-quality): "对今天改写的15篇做preflight + anti-slop"
    → 通过/打回 → 关闭

  会话D (lovart-creation): "preflight通过，import到Sanity"
    → 发布完成 → 关闭

  会话E (lovart-ops): "IndexNow通知搜索引擎"
    → 提交完成 → 关闭
```

## 快速入口

```
# 报告
hermes -p lovart-reports -s lovart-seo-reporting

# 创作 Blog
hermes -p lovart-creation -s lovart-blog-serp-writer,lovart-anti-slop

# 创作 Tools 页
hermes -p lovart-creation -s lovart-page-serp-writer,lovart-landing-page

# 质检
hermes -p lovart-quality -s lovart-content-quality-gates,lovart-anti-slop

# 运维
hermes -p lovart-ops -s lovart-sitemap-update,lovart-technical-seo

# 分发
hermes -p lovart-distribution -s lovart-content-distribution

# 管理
hermes -p lovart-management
```

## default 什么时候用

仅用于**不确定该走哪条线**的探索：如"帮我看看最近 SEO 有什么问题"→ 分析后告诉你应该去 lovart-reports 详细看。确定路线后立即切 Profile。

## 规则加载

| Profile | 加载的 RULES |
|---------|-------------|
| **全部** | `RULES-00-iron.md` |
| lovart-reports | + `RULES-10-reports.md` |
| lovart-creation | + `RULES-20-creation.md` |
| lovart-quality | + `RULES-30-quality.md` |
| lovart-ops | + `RULES-40-ops.md` |
| lovart-distribution | + `RULES-50-distribution.md` |
| lovart-management | + `RULES-60-management.md` |
