# Lovart SEO 自动化工具集 — 团队使用指南

> **作者**：SEO / 增长团队  
> **版本**：v1.0（2026-05-28）  
> **适用**：Lovart.ai 及同架构多语言站点  

---

## 目录

1. [这是什么](#1-这是什么)
2. [解决了什么问题](#2-解决了什么问题)
3. [Multi SEO 前置验证](#3-multi-seo-前置验证)
4. [快速开始（5 分钟上手）](#4-快速开始5-分钟上手)
5. [配置文件说明](#5-配置文件说明)
6. [脚本命令详解](#6-脚本命令详解)
7. [输出文件说明](#7-输出文件说明)
8. [部署指南](#8-部署指南)
9. [定时更新 & 维护](#9-定时更新--维护)
10. [为新站点适配](#10-为新站点适配)
11. [故障排查](#11-故障排查)
12. [技术原理简述](#12-技术原理简述)

---

## 1. 这是什么

一套自动化脚本工具，**从一个配置文件出发，自动生成一个多语言网站的全部 SEO 资产**：

```
                    ┌─────────────────────────────┐
                    │     config.json              │
                    │  (base_url, languages,       │
                    │   sections, org_info...)     │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │     generate-all.py          │
                    │                              │
                    │  ① 爬取分页列表页            │
                    │  ② 拉取服务器已有 sitemap    │
                    │  ③ 合并去重 × 语言展开       │
                    │  ④ 生成 sitemap XML          │
                    │  ⑤ 生成 robots.txt           │
                    │  ⑥ 生成 llms.txt 系列        │
                    │  ⑦ 生成 Schema.org JSON-LD   │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │       output/                │
                    │                              │
                    │  📂 21 个 sitemap XML 文件   │
                    │  📄 robots.txt               │
                    │  📄 llms.txt 系列（6 个）     │
                    │  📐 schema-snippets/         │
                    └──────────────────────────────┘
```

---

## 2. 解决了什么问题

### 之前的问题

| 问题 | 影响 |
|------|------|
| sitemap 只覆盖 EN + JA，缺 8 种语言 | Google 收不到其他语言页面 |
| 博客 855 篇，sitemap 里只列了 20+ 篇 | 大量优质内容不被索引 |
| robots.txt 对每个 bot 各写一遍规则 | 2500 行，维护噩梦 |
| 没有 llms.txt | ChatGPT、Perplexity 找不到内容 |
| 没有 Schema.org 结构化数据 | Google 知识面板、富结果缺失 |

### 现在的效果

| 指标 | 之前 | 现在 |
|------|------|------|
| sitemap 覆盖 URL | ~600 | **13,962** |
| 覆盖语言 | 2 | **10** |
| 博客收录 | ~20 / 855 | **855 / 855** |
| robots.txt 行数 | 2500 | **150** |
| AI 搜索优化（llms.txt） | 无 | **6 层索引** |
| Schema.org | 基础 | **组织/网站/应用/FAQ/文章 全类型** |

---

## 3. Multi SEO 前置验证

Multi SEO 已在 2026-06-07 收口：当前执行主线为 **Bing Webmaster + IndexNow**。Brave、国内搜索等渠道因 API 订阅、验证码、海外域名支持或站长平台限制，不进入近期执行范围。

当前结论文档：

- `multi-seo-closeout-2026-06-07.md`：最新收口总结，说明已打通内容、不再推进内容和维护动作。
- `multi-seo-access-status-2026-06-07.md`：Bing Webmaster、IndexNow、Sanity webhook 的接入状态。

历史验证文档：

- `multi-seo-feasibility-matrix.md`：渠道可达性、数据可得性、自动化等级、阻塞项和下一步。
- `multi-seo-feasibility-template.csv`：可直接填写的渠道验证模板。

后续若重新打开某个渠道，必须先确认：

- 搜索引擎或目标地区网络能访问 Lovart 重点页面。
- 该渠道的数据属于 `official`、`observed_sample`、`inferred` 还是 `unavailable`。
- SERP/AI 抽样数据不能和 GSC/Bing Webmaster/GA4/DataWorks 官方数据混算。
- 只有通过可行性验证的渠道才进入 Sentinel source、站长平台提交 SOP 或内容生产。

---

## 4. 快速开始（5 分钟上手）

### 前提

- Python 3.9+
- 网络能访问 lovart.ai

### 步骤

```bash
# 1. 进入 skills 目录
cd "Documents/skills"

# 2. 首次运行（需要联网爬取，约 10 分钟）
python3 generate-all.py config.example.json

# 3. 查看输出
ls output/
```

### 日常更新（无需重新爬取）

```bash
# 使用缓存的 slug 数据快速生成
python3 generate-all.py config.example.json --skip-crawl
```

### 完全离线（不联网）

```bash
python3 generate-all.py config.example.json --offline
```

---

## 5. 配置文件说明

配置文件 `config.example.json` 分为 6 个区块：

### 4.1 站点信息

```json
"site": {
    "name": "Lovart AI",
    "base_url": "https://www.lovart.ai",
    "tagline": "一句话描述这个网站"
}
```

### 4.2 语言配置

```json
"languages": {
    "prefixes": ["", "/zh", "/zh-TW", ...],    // URL 前缀
    "codes": ["en", "zh", "zh-TW", ...],        // 语言代码
    "names": { "en": "English", ... }            // 语言名称
}
```

> **重要**：`prefixes` 和 `codes` 的顺序必须一一对应。空字符串 `""` 表示默认语言。

### 4.3 板块配置

```json
"sections": {
    "listable": ["blog", "news", "tools", "features"],  // 有分页列表的板块
    "index_only": ["pricing", "r"]                      // 只有首页的板块
}
```

- `listable`：脚本会爬取 `{base}/{section}?page=1` 到 `?page=N`，提取所有子页面 slug
- `index_only`：只生成 `{base}/{section}` 这一个 URL

### 4.4 爬取参数

```json
"crawler": {
    "request_delay_s": 0.8,       // 每次请求间隔（秒）
    "timeout_s": 15,              // 单个请求超时
    "retry_count": 3,             // 失败重试次数
    "max_pages_per_section": 200, // 每个板块最多爬几页
    "empty_page_threshold": 3     // 连续 N 页无新内容则停止
}
```

### 4.5 组织信息（用于 Schema.org）

```json
"organization": {
    "founding_date": "2025",
    "founders": [...],
    "social": { ... },
    "price_range": {"low": "0", "high": "149", "currency": "USD"},
    "rating": {"value": "4.9", "count": "12"}
}
```

### 4.6 输出控制

```json
"output": {
    "dir": "./output",
    "generate_sitemaps": true,  // 是否生成 sitemap
    "generate_llms": true,      // 是否生成 llms.txt
    "generate_robots": true,    // 是否生成 robots.txt
    "generate_schema": true     // 是否生成 Schema.org
}
```

---

## 6. 脚本命令详解

```
python3 generate-all.py <配置文件> [选项]
```

| 选项 | 说明 | 耗时 |
|------|------|------|
| （无） | 完整运行：爬取 + 拉取 + 生成 | ~10 分钟 |
| `--skip-crawl` | 跳过爬取，用缓存 slug | ~30 秒 |
| `--skip-fetch` | 跳过拉取服务器 sitemap | — |
| `--offline` | 完全不联网 | ~2 秒 |
| `--only-sitemaps` | 只生成 sitemap | — |
| `--only-llms` | 只生成 llms.txt | — |
| `--only-robots` | 只生成 robots.txt | — |
| `--only-schema` | 只生成 Schema.org | — |

---

## 7. 输出文件说明

运行后 `output/` 目录结构：

```
output/
│
├── 🔗 搜索引擎提交用 ─────────────────────
│   ├── sitemap-index.xml           ← 提交这个给 Google Search Console
│   ├── sitemap-blog.xml            (8,870 URLs)
│   ├── sitemap-features.xml        (2,024 URLs)
│   ├── sitemap-tools.xml           (496 URLs)
│   ├── sitemap-news.xml            (96 URLs)
│   ├── sitemap-homepage.xml        (11 URLs)
│   ├── sitemap-pricing.xml         (10 URLs)
│   ├── sitemap-r.xml               (10 URLs)
│   ├── sitemap-profile.xml         (2,421 URLs)
│   ├── sitemap-docs.xml            (23 URLs)
│   ├── sitemap-lang-en.xml         (3,700 URLs)
│   ├── sitemap-lang-zh.xml         ...
│   ├── ... (10 个语言各一个)
│   └── robots.txt                  ← 放到网站根目录
│
├── 🧠 AI 搜索用 ─────────────────────────
│   ├── llms.txt                    ← AI 爬虫入口索引
│   ├── llms-blog.txt               (855 篇，按 11 个分类)
│   ├── llms-features.txt           (188 个功能)
│   ├── llms-tools.txt              (45 个工具)
│   ├── llms-news.txt               (8 条新闻)
│   └── llms-full.txt               (单文件全量，Perplexity 优先)
│
├── 📐 开发集成用 ────────────────────────
│   └── schema-snippets/
│       ├── homepage-schemas.html   (插入首页 <head>)
│       ├── breadcrumb-blog.html    (插入 /blog 页 <head>)
│       ├── breadcrumb-features.html
│       ├── breadcrumb-tools.html
│       ├── breadcrumb-pricing.html
│       ├── breadcrumb-news.html
│       └── breadcrumb-r.html
│
└── 📊 参考用 ────────────────────────────
    ├── all-urls.txt                (13,962 条完整 URL 列表)
    └── crawled_slugs.json          (爬取缓存，可重复使用)
```

---

## 8. 部署指南

### 7.1 部署到服务器

将 `output/` 中的以下文件上传到网站 **根目录**（和 `index.html` 同级）：

**必须上传：**
- `sitemap-index.xml`
- 所有 `sitemap-*.xml`（17 个）
- `robots.txt`
- `llms.txt`
- `llms-blog.txt`、`llms-features.txt`、`llms-tools.txt`、`llms-news.txt`
- `llms-full.txt`

**不需要上传（本地参考用）：**
- `all-urls.txt`
- `crawled_slugs.json`
- `schema-snippets/`（这些 HTML 片段需要开发者集成到页面代码中，不是独立文件）

**集成到页面代码的：**
- `homepage-schemas.html` → 把内容追加到首页 `<head>` 标签闭合前
- `breadcrumb-*.html` → 把内容追加到对应分页的 `<head>` 中

### 7.2 提交给搜索引擎

| 平台 | 操作 | 链接 |
|------|------|------|
| **Google** | 提交 `sitemap-index.xml` | [Search Console](https://search.google.com/search-console) |
| **Bing** | 提交 `sitemap-index.xml` | [Bing Webmaster](https://www.bing.com/webmasters) |
| **百度** | 提交 `sitemap-index.xml` | [百度站长平台](https://ziyuan.baidu.com) |
| **Yandex** | 提交 `sitemap-index.xml` | [Yandex Webmaster](https://webmaster.yandex.com) |

### 7.3 验证

部署后检查：

```bash
# 确认 sitemap 可访问
curl -I https://www.lovart.ai/sitemap-index.xml

# 确认 robots.txt 可访问
curl https://www.lovart.ai/robots.txt

# 确认 llms.txt 可访问
curl https://www.lovart.ai/llms.txt
```

用 Google Rich Results Test 验证 Schema：[https://search.google.com/test/rich-results](https://search.google.com/test/rich-results)

---

## 9. 定时更新 & 维护

### 8.1 Cron 定时任务

```bash
# 每周一凌晨 2 点自动运行（使用缓存数据，不重新爬取）
0 2 * * 1 cd /path/to/skills && python3 generate-all.py config.json --skip-crawl && rsync -avz output/ user@server:/var/www/lovart/public/
```

### 8.2 发布新博客/功能后

1. 手动运行一次完整爬取：`python3 generate-all.py config.json`
2. 部署新文件到服务器

### 8.3 新增语言后

1. 在 `config.json` 的 `languages` 中添加新语言
2. 运行：`python3 generate-all.py config.json --skip-crawl`
3. 部署新文件（所有 sitemap 和 llms 文件都已更新）

---

## 10. 为新站点适配

如果要在 Lovart 之外的其他站点使用这套工具：

### Step 1：复制配置

```bash
cp config.example.json my-site.json
```

### Step 2：修改配置

```json
{
  "site": {
    "name": "我的站点",
    "base_url": "https://www.my-site.com",
    "tagline": "一句话介绍"
  },
  "languages": {
    "prefixes": ["", "/en"],
    "codes": ["zh", "en"],
    "names": {"zh": "中文", "en": "English"}
  },
  "sections": {
    "listable": ["blog", "articles"],
    "index_only": ["about", "contact"]
  },
  "sitemap": {
    "server_files": ["sitemap.xml"]
  },
  "organization": {
    "founding_date": "2020",
    "founders": [{"name": "...", "title": "..."}],
    "social": {"twitter": "...", "linkedin": "..."},
    "price_range": {"low": "0", "high": "99", "currency": "CNY"}
  }
}
```

### Step 3：运行

```bash
python3 generate-all.py my-site.json
```

---

## 11. 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 脚本卡住不动 | 正在爬取分页（正常） | 等待，800 页约 10 分钟 |
| `SSL EOF occurred` | Cloudflare 限流 | 脚本会自动重试 3 次 + 间隔 |
| 某些板块爬不到数据 | 该板块不是 SSR 渲染 | 检查 HTML 源码中是否有 `<a href>` 标签 |
| `sitemap-blog-plus.xml: FAILED` | 服务器间歇不可用 | 使用 `--skip-fetch` 跳过 |
| 生成的 URL 少于预期 | 缓存文件过期 | 删除 `crawled_slugs.json` 重新爬取 |
| `ModuleNotFoundError` | Python 缺少依赖 | 脚本只用标准库，换 Python 3.9+ |

---

## 12. 技术原理简述

### 11.1 为什么能爬到 Next.js SPA 的内容

Lovart.ai 使用 Next.js，但 **服务端渲染（SSR）输出中已经包含 `<a href>` 链接**。爬虫不需要执行 JavaScript，直接解析 HTML 即可。

### 11.2 覆盖的 AI 搜索平台

| 平台 | 爬虫 Bot | 优化方式 |
|------|---------|---------|
| Google Gemini | Googlebot | sitemap + robots.txt + Schema.org |
| ChatGPT / SearchGPT | OAI-SearchBot | robots.txt + llms-full.txt |
| Perplexity | PerplexityBot | llms-full.txt（标准支持） |
| Claude | ClaudeBot | llms-knowledge.txt（深度文档） |
| Kimi（月之暗面） | MoonshotBot | robots.txt + llms-blog.txt |
| DeepSeek | DeepseekSpider | robots.txt + sitemap |
| 豆包（ByteDance） | Bytespider | robots.txt（crawl-delay:5） |
| 元宝（腾讯） | 无独立 Bot | 走 Bing 索引 |
| 搜狗 | Sogou web spider | robots.txt + sitemap |

### 11.3 文件之间的关系

```
robots.txt  →  Sitemap: https://.../sitemap-index.xml
                       │
sitemap-index.xml  →   17 个子 sitemap
                       │
                       ├── sitemap-blog.xml        (blog 板块所有 URL)
                       ├── sitemap-lang-zh.xml     (中文所有 URL)
                       └── ...

llms.txt  →  AI 爬虫从这里开始
              │
              ├── llms-blog.txt       (博客分类索引)
              ├── llms-features.txt   (功能列表)
              ├── llms-tools.txt      (工具列表)
              ├── llms-full.txt       (单文件全量)
              └── llms-knowledge.txt  (深度知识文档)
```

---

> **最后更新**：2026-05-28  
> **维护人**：SEO / 增长团队  
> **相关文件**：`generate-all.py` / `config.example.json` / `sitemap-seo-ai-search-optimization.md`
