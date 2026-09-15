---
tags:
  - workflow
  - seo
  - opencode
  - wordpress
  - obsidian
  - sop
created: 2026-05-17
---

# Obsidian + opencode WordPress SEO 快速起量工作流

> 核心理念：**Obsidian 是内容工厂，opencode 是 AI 引擎，WordPress 是发布终端。三位一体，批量化生产 SEO 内容。**

---

## 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    Keyword Research Layer                    │
│   GSC Data → opencode 关键词分析 → 关键词矩阵（Pillar +     │
│   Cluster + Long-tail + Programmatic）                       │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Content Brief Layer                        │
│   opencode 生成 Content Brief（标题/大纲/关键词/FAQ/内链）   │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Content Creation Layer                     │
│   Obsidian 模板 + opencode 写作 → Markdown 文章              │
│   ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│   │ 标准博客文章 │  │ 程序化SEO页面 │  │ 旧文翻新/刷新   │   │
│   │ (seo-blog)  │  │ (programmatic)│  │ (content-refresh)│   │
│   └─────────────┘  └──────────────┘  └──────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Optimization Layer                         │
│   标题优化 / Meta Description / FAQ Schema / 内链 / E-E-A-T │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Publishing Layer                           │
│   obsidian-wordpress → XML-RPC → WordPress (publish/draft)  │
│   NowX: nownexts.com (default)                               │
│   Lovart Blogs: blogs.lovart.ai                             │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Analytics Loop                             │
│   GSC 排名追踪 → opencode 分析 → 找出下降/可提升文章         │
│   → 触发 Content Refresh 工作流 → 重新发布                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: 关键词研究

### 输入源
- Google Search Console (GSC) — 已有的查询数据
- Ahrefs / Semrush (如有)
- 竞品博客 sitemap 反查
- People Also Ask (PAA) 抓取
- Google Trends

### opencode 操作

```
打开 Obsidian，读取 GSC 导出数据或已有关键词库，使用「关键词研究」prompt：
→ 1-Project/opencode-WP-SEO/prompts/opencode-seo-prompts.md #3   <!-- TODO: opencode-WP-SEO 在重构中已删除，如仍需请确认新落点 -->
```

输出：
- `Keywords Research/{topic}_关键词矩阵_{date}.md` — Pillar + Cluster + Long-tail
- `Keywords Research/{topic}_内容缺口分析_{date}.md` — 竞品在写你没写的

### 优先级排序
用 ICE 打分模型（Impact × Confidence × Ease）
- Impact（搜索量 + 商业价值）
- Confidence（你有能力排名吗）
- Ease（写这篇文章要多久）

---

## Phase 2: Content Brief 生成

### opencode 操作

```
读完关键词矩阵，选取 Top 5 高优先级关键词，每条用「Content Brief」prompt：
→ prompts/opencode-seo-prompts.md #1
```

输出：
- 每篇一个 Obsidian 笔记，包含完整大纲
- 放到 `Content Briefs/` 文件夹

---

## Phase 3-4: 文章写作 + 优化

### 方式 A：标准博客文章（How-to / Listicle / Pillar）

**Step 1 — 创建新笔记：**
1. Obsidian 中 Ctrl/Cmd+N 新建笔记
2. Templater: Insert Template → `seo-blog-post`
3. 按光标提示填入：标题 → slug → 分类 → 标签 → meta description → 主关键词

**Step 2 — opencode 写作：**
```
打开刚才创建的笔记模板，读取 Content Brief，使用「Write Article」prompt：
→ prompts/opencode-seo-prompts.md #2

让 opencode 直接填充完整的 Markdown 内容，包括所有 H2/H3、FAQ、内链表、E-E-A-T 表。
```

**Step 3 — 人工审核：**
- 检查事实准确性
- 调整品牌语气
- 补充真实截图/图片链接
- 确认内链指向正确

### 方式 B：程序化 SEO 页面

**Step 1 — 准备垂直列表：**
在 Obsidian 新建一个表格笔记，列出目标垂直：`{industry_name}, {slug}, {target_keyword}`

**Step 2 — opencode 批量生成：**
```
使用「Programmatic SEO Batch」prompt：
→ prompts/opencode-seo-prompts.md #5

一次性生成 N 个行业的品牌套件页面，每个一个 .md 文件。
```

### 方式 C：旧文翻新

**Step 1 — 找出待翻新文章：**
```
从 GSC 筛选：排名 8-20 位 + 展示量 > 100/月 + 文章 > 6 个月
从 GA4 筛选：跳出率 > 80% + 平均停留时间 < 1min
```

**Step 2 — opencode 翻新：**
```
使用「Content Refresh」prompt：
→ prompts/opencode-seo-prompts.md #4

自动翻新：更新年份 → 补充缺失段落 → 添加 FAQ → 刷新内链 → 增强 E-E-A-T
```

---

## Phase 5: 发布到 WordPress

### obsidian-wordpress 插件配置

两个配置文件已就绪：
- **NowX** (nownexts.com) — 默认发布站点
- **Lovart Blogs** (blogs.lovart.ai) — 第二站点

### 发布操作

1. 在 Obsidian 中打开要发布的文章
2. 左侧 Ribbon 点击 WordPress 图标，或 Cmd+P → `WordPress: Publish`
3. 选择 Profile → 确认分类 → 发布

插件会自动：
- 将 YAML frontmatter 的 tags 映射为 WP Tags
- 将 category 映射为 WP Categories
- 使用 meta_description 作为 SEO 插件描述字段
- 上传并替换本地图片链接

> 建议首次发布时选 `draft` 状态，在 WP 后台预览确认后再改为 `publish`。

---

## Phase 6: 数据复盘与迭代

### 每两周复盘

```
打开 GSC，导出最近 14 天查询数据。
在 opencode 中：
- 读入 GSC 数据
- 读入已发布的文章列表
- 分析：
  1. 哪些文章进入了 Top 10？（→ 加强内链支持）
  2. 哪些在 11-30 位？（→ 触发 Content Refresh）
  3. 哪些关键词有 impression 但无 click？（→ 优化标题和 Meta Description）
  4. 新发现的关键词机会（→ 加入下轮 Content Brief 队列）
```

---

## 效率基准

| 环节 | 传统方式 | opencode 方式 | 提效 |
|------|---------|--------------|------|
| 关键词研究（10 个主题） | 4-6 小时 | 30 分钟 | 8-12x |
| Content Brief（5 篇） | 3-4 小时 | 20 分钟 | 9-12x |
| 写一篇 1500 字文章 | 3-5 小时 | 15 分钟 + 30 分钟审核 | 6-10x |
| 旧文翻新（5 篇） | 2-3 小时/篇 | 10 分钟/篇 + 15 分钟审核 | 8-12x |
| 程序化 SEO（50 页） | 2-3 周 | 2-3 小时 | 20-40x |

---

## 文件索引

| 文件 | 路径 | 用途 |
|------|------|------|
| SEO 文章模板 | `模版/seo-blog-post.md` | 标准博客文章模板 |
| 程序化 SEO 模板 | `模版/programmatic-seo.md` | 批量行业页面模板 |
| opencode 提示词库 | `1-Project/opencode-WP-SEO/prompts/opencode-seo-prompts.md` | 6 类 SEO prompt（⚠️ 重构中已删除，待确认新落点） |
| Lovart SEO 策略 | `1-Project/Lovart Dev/Product Project Management/Lovart子站内容与SEO体系规划.md` | 参考：三站 SEO 体系 |
| 自动化工作流 | `0-Inbox/自动化舆情检测与SEO 内容生产工作流.md` | 参考：n8n 自动化管线 |
| 分析报表 SOP | `analytics-report-sop.md` | 参考：数据采集与分析 |

---

## 进阶方向

1. **opencode + n8n 集成**：让 opencode 的输出直接触发 n8n webhook → 自动发布
2. **AI 图片生成集成**：opencode 写文章 → 同时调用 Midjourney/DALL-E API → 图片自动插入
3. **多语言管道**：English 文章 → opencode 翻译 → 日语/中文/葡语版 → 多语言子目录发布
4. **GSC 自动监控**：定时 cron → GSC API → opencode 分析 → Obsidian 日报
