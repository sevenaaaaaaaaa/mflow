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
# 品牌方 会话路由指南

> 如何开正确的会话，做正确的事。一次会话只做一类事。

---

## 6 条工作线

| # | 工作线 | Profile | 启动命令 | 做什么 | 不做什么 |
|---|--------|---------|---------|--------|---------|
| 1 | 报告 | `mflow-reports` | `hermes -p mflow-reports` | SEO月报/周报、舆情日报、竞品分析、SERP调研、OKR看板 | 不写文章、不发布内容 |
| 2 | 创作 | `mflow-creation` | `hermes -p mflow-creation` | Blog/Tools/Features/Landing/Solution/Product/Scenario/Topic 页面 | 不跑SEO报告、不分发 |
| 3 | 质量 | `mflow-quality` | `hermes -p mflow-quality` | preflight、Anti-Slop检测、i18n审计、内容健康度 | 不写新内容、不调研 |
| 4 | 运维 | `mflow-ops` | `hermes -p mflow-ops` | Sitemap、IndexNow、CRO修复、图片素材替换 | 不改内容正文 |
| 5 | 分发 | `mflow-distribution` | `hermes -p mflow-distribution` | 国内(Wechatsync)/海外(DEV.to/GitHub/Blogger)分发 | 不创作原文 |
| 6 | 管理 | `mflow-management` | `hermes -p mflow-management` | 项目规划、工程优化、Skill维护、Profile调优 | 不执行内容操作 |

## 典型工作流

```
❌ 错误：一个会话里调研→分析→写文章→preflight→发布
✅ 正确：
  会话A (mflow-reports): "GSC数据分析，找出零点击但排名4-10的15篇Blog"
    → 产出改写清单 → 关闭

  会话B (mflow-creation): "按这份清单改写这15篇Blog"
    → 逐篇改写 → 关闭

  会话C (mflow-quality): "对今天改写的15篇做preflight + anti-slop"
    → 通过/打回 → 关闭

  会话D (mflow-creation): "preflight通过，import到Sanity"
    → 发布完成 → 关闭

  会话E (mflow-ops): "IndexNow通知搜索引擎"
    → 提交完成 → 关闭
```

## 快速入口

```
# 报告
hermes -p mflow-reports -s mflow-seo-reporting

# 创作 Blog
hermes -p mflow-creation -s blog-writer,mflow-anti-slop

# 创作 Tools 页
hermes -p mflow-creation -s landing-writer,landing-writer

# 质检
hermes -p mflow-quality -s content-quality-gates,mflow-anti-slop

# 运维
hermes -p mflow-ops -s sitemap-update,mflow-technical-seo

# 分发
hermes -p mflow-distribution -s content-distribution

# 管理
hermes -p mflow-management
```

## default 什么时候用

仅用于**不确定该走哪条线**的探索：如"帮我看看最近 SEO 有什么问题"→ 分析后告诉你应该去 mflow-reports 详细看。确定路线后立即切 Profile。

## 规则加载

| Profile | 加载的 RULES |
|---------|-------------|
| **全部** | `RULES-00-iron.md` |
| mflow-reports | + `RULES-10-reports.md` |
| mflow-creation | + `RULES-20-creation.md` |
| mflow-quality | + `RULES-30-quality.md` |
| mflow-ops | + `RULES-40-ops.md` |
| mflow-distribution | + `RULES-50-distribution.md` |
| mflow-management | + `RULES-60-management.md` |
