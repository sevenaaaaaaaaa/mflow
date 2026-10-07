# Lovart Blog 自动化部署手册

> 适用站点：`blogs.lovart.ai`  
> 本地目录：`1-Project/1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/`  
> 前置要求：WordPress 管理员账号 + 服务器 SSH 访问
> 当前状态（2026-06-07）：`publish-to-wp.py` 已恢复到规范落点；生产发布前仍需 `--dry-run` 验证。Feishu wiki integration 仍为 `blocked-by-missing-source`。

---

## 目录

1. [本地环境准备](#1-本地环境准备)
2. [WordPress 插件安装](#2-wordpress-插件安装)
3. [Showcase CPT 注册与 ACF 字段](#3-showcase-cpt-注册与-acf-字段)
4. [Elementor 模板搭建](#4-elementor-模板搭建)
5. [Markdown 发布脚本](#5-markdown-发布脚本)
6. [CSV 导入 UGC 数据](#6-csv-导入-ugc-数据)
7. [SEO 配置（Rank Math）](#7-seo-配置rank-math)
8. [Blog ↔ Showcase 双向关联](#8-blog--showcase-双向关联)
9. [日常内容生产工作流](#9-日常内容生产工作流)
10. [故障排查](#10-故障排查)

---

## 1. 本地环境准备

### 1.1 目录结构

```
1-Project/1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/
├── 01-Drafts/                          ← 新文章撰写区
├── 03-Published/                       ← 已发布文章备份（含 wp_post_id）
├── LOVART-BLOG-LOCAL-SPEC.md           ← 写作规范（frontmatter、category 映射）
├── PRODUCTION-PLAN.md                  ← 内容日历（93 篇清单）
├── BATCH-WORKFLOW.md                   ← 批量生产规则
├── plugins/lovart-showcase/            ← Showcase CPT 插件
│   ├── lovart-showcase.php             ← 插件入口
│   ├── includes/cpt-taxonomy.php       ← CPT + Taxonomy 注册
│   ├── includes/shortcodes.php         ← [showcase_grid] 等短代码
│   ├── includes/rest-api.php           ← REST API 接口
│   ├── acf-json/showcase-fields.json   ← ACF 字段定义
│   ├── import/import-showcase.php      ← CSV 导入脚本
│   └── elementor-templates/            ← Elementor 模板指南
├── scripts/
│   └── pick-cover.py                   ← 封面 URL 分配
└── templates/
    └── frontmatter.example.yaml        ← frontmatter 模板

# 发布脚本规范落点（TODO/GAP 2026-06-03）
1-Project/1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/scripts/
└── publish-to-wp.py                    ← Markdown → WordPress 发布脚本
# 注：publish-to-wp.py 已恢复；发布前必须先 dry-run。
#     sync-wp-to-obsidian.py / sync-wp-xmlrpc.py 未在当前 Blog Pipeline 中恢复，如需请确认新落点。
```

### 1.2 Python 依赖

```bash
pip3 install pyyaml
# markdown 库可选（有则用 Python-Markdown 转换，无则用内置 fallback）
pip3 install markdown
```

### 1.3 服务器安装 wp-cli（用于 CSV 导入）

SSH 到 blogs.lovart.ai 服务器：

```bash
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp
wp --info   # 验证
```

---

## 2. WordPress 插件安装

在 `https://blogs.lovart.ai/wp-admin` 后台安装：

| 插件 | 用途 | 是否必需 |
|------|------|---------|
| **CPT UI** | 注册 Custom Post Type + Taxonomy | ✅ 必需 |
| **Advanced Custom Fields (ACF)** | 自定义字段（推荐语、作者名、浏览数等） | ✅ 必需 |
| **Rank Math SEO** | 面包屑、Schema、XML Sitemap | ✅ 必需 |
| **Elementor** | 已安装（Hello Elementor 主题自带） | ✅ 已存在 |
| **Elementor Pro**（可选）| Loop Grid 动态查询 | 🟡 有更好 |

---

## 3. Showcase CPT 注册与 ACF 字段

### 3.1 上传插件

将 `plugins/lovart-showcase/` 整个目录上传到服务器：

```bash
scp -r plugins/lovart-showcase user@server:/path/to/wp-content/plugins/
```

在 WordPress 后台 **Plugins → Lovart Community Showcase → Activate**。

### 3.2 导入 ACF 字段

1. 进入 **Custom Fields → Tools → Import**
2. 上传 `acf-json/showcase-fields.json`
3. 确认 7 个字段出现在 Field Groups 中：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `editor_recommendation` | WYSIWYG | 编辑推荐语 |
| `author_name` | Text | 原作者名 |
| `cover_url` | URL | 作品封面图 |
| `view_count` | Number | 浏览次数 |
| `like_count` | Number | 点赞次数 |
| `lovart_url` | URL | Lovart 原始链接 |
| `ai_workflow` | Text | AI 工作流类型 |

### 3.3 验证 CPT 注册

访问 `https://blogs.lovart.ai/wp-admin/edit.php?post_type=showcase` 确认 CPT 已注册。

URL 结构：
```
/showcase/                              → 列表页
/showcase/{category}/                   → 分类页
/showcase/{category}/{slug}/            → 详情页
/showcase/style/{style}/                → 风格标签页
/showcase/industry/{industry}/          → 行业标签页
```

---

## 4. Elementor 模板搭建

### 4.1 Single Showcase 模板

1. **Elementor → Theme Builder → Single Post → Add New**
2. 选中 **Showcase** 作为 Post Type
3. 模板名：`Showcase Detail Page`

**页面结构（从上到下）：**

```
┌─────────────────────────────────────────┐
│ 面包屑（Rank Math Breadcrumb 组件）        │
├─────────────────────────────────────────┤
│ 封面大图（ACF Dynamic Tag → cover_url）    │
├─────────────────────────────────────────┤
│ 编辑推荐语（ACF WYSIWYG → editor_recommendation）│
├─────────────────────────────────────────┤
│ 标题（Post Title） + 作者名 + 浏览/点赞数   │
├─────────────────────────────────────────┤
│ 标签（Post Info → Showcase Category/Style/Industry）│
├─────────────────────────────────────────┤
│ 相关作品（Loop Grid 或 Shortcode 组件）     │
├─────────────────────────────────────────┤
│ 相关博客（Posts 组件 / 按 taxonomy 筛选）   │
├─────────────────────────────────────────┤
│ 相关页面（手动关联 / REST API 加载）        │
├─────────────────────────────────────────┤
│ CTA 按钮 → 跳转到 Lovart 原始链接          │
└─────────────────────────────────────────┘
```

**Dynamic Tags 配置：**

| 组件 | Dynamic Tag 来源 |
|------|-----------------|
| 封面图 | ACF Field → `cover_url` |
| 作者名 | ACF Field → `author_name` |
| 浏览数 | ACF Field → `view_count` |
| 点赞数 | ACF Field → `like_count` |
| 推荐语 | ACF Field → `editor_recommendation` |

### 4.2 Archive Showcase 模板

1. **Elementor → Theme Builder → Archive → Add New**
2. 选中 **Showcase**
3. 模板名：`Showcase Archive`

使用 Loop Grid（Elementor Pro）或 Posts 组件，卡片展示：封面图 + 标题 + 作者 + 热度数据。

---

## 5. Markdown 发布脚本

### 5.1 配置脚本

凭证读取方式：设置 `WP_USER` / `WP_PASS` 环境变量，或复制 `scripts/wp-auth.local.env.example` 为 `scripts/wp-auth.local.env` 后填写。不要把真实凭证提交到 Git。

```bash
cp scripts/wp-auth.local.env.example scripts/wp-auth.local.env
```

认证方式：Cookie 登录（`wp-login.php`），非 Basic Auth。

### 5.2 使用方法

```bash
# 发布单篇
python3 scripts/publish-to-wp.py --file "canva-vs-lovart-comparison.md"

# 发布全部（从 01-Drafts/）
python3 scripts/publish-to-wp.py

# 预览模式（不实际发布）
python3 scripts/publish-to-wp.py --dry-run --limit 5
```

### 5.3 工作流

1. 文章写在 `01-Drafts/`，frontmatter 按 `writing-spec.md` 规范
2. 运行 `publish-to-wp.py`
3. 脚本自动：
   - 登录 WP 获取 Cookie
   - 创建/匹配 Category 和 Tags
   - 转换 Markdown 为 HTML
   - POST 到 WordPress REST API
   - 发布后文件移动到 `03-Published/`，追加 `wp_post_id`

### 5.4 WordPress API 调试

```bash
# 查询总文章数
curl -sI "https://blogs.lovart.ai/wp-json/wp/v2/posts?per_page=1" | grep X-WP-Total

# 按 slug 查重
curl -s "https://blogs.lovart.ai/wp-json/wp/v2/posts?slug=my-slug"

# 查看分类
curl -s "https://blogs.lovart.ai/wp-json/wp/v2/categories?per_page=30"
```

---

## 6. CSV 导入 UGC 数据

### 6.1 准备工作

1. 将 CSV 文件上传到服务器 WordPress 根目录
2. 确认 `lovart-showcase` 插件已激活
3. ACF 字段已导入

### 6.2 执行导入

```bash
cd /path/to/wordpress
wp eval-file wp-content/plugins/lovart-showcase/import/import-showcase.php
```

脚本自动完成：
- 解析 CSV 每行的 description，提取作者、分类、行业、关键词
- 根据关键词映射到 3 个 taxonomy（category / industry / style）
- 为每个 showcase 创建 CPT post
- 写入 ACF 字段（作者名、浏览数、点赞数等）
- 下载 cover_url 图片并设为 Featured Image
- 生成编辑推荐语（有 OpenAI Key 用 AI，无则用模板）

### 6.3 OpenAI 推荐语配置（可选）

在 `wp-config.php` 中添加：

```php
define('OPENAI_API_KEY', 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
```

不加则使用内置规则模板自动生成推荐语，质量仍然可用。

---

## 7. SEO 配置（Rank Math）

### 7.1 Showcase SEO

进入 **Rank Math → Titles & Meta → Post Types → Showcase**：

| 设置项 | 值 |
|--------|-----|
| Single Post Title | `%title% - Lovart Community Showcase` |
| Single Post Description | `%excerpt%` |
| Schema Type | `CreativeWork` |
| 面包屑 | 开启 |
| Sitemap | 开启 |

### 7.2 Blog SEO（已配置，确认项）

- 所有文章 schema 类型：`Article` 或 `FAQ`
- Sitemap 包含 posts + pages + showcase
- Canonical URL 自动生成

---

## 8. Blog ↔ Showcase 双向关联

### 8.1 在博客中嵌入 Showcase 网格

```
[showcase_grid category="poster" limit="6" columns="3" orderby="views"]
[showcase_author_works author="kyoma" limit="8"]
[showcase_stats]
```

### 8.2 Showcase 详情页推荐博客

通过 REST API 端点自动匹配：

```
GET /wp-json/lovart/v1/showcase/related?post_id=18001&type=blog&limit=4
```

按 showcase 的 category + industry + style 与博客 taxonomy 做交集匹配。

---

## 9. 日常内容生产工作流

### 写一篇新博客

```
1. 市场调研（Phase 0）
   ├── curl 查 slug 是否已存在 → 避免重复
   ├── 搜索竞品 SERP top 3-5 → 找内容缺口
   ├── 确认 PRODUCTION-PLAN.md 位置 → 避免主题冲突
   └── 选题角度决策 → Comparison / How-To / Better Design / Insight

2. 规划（Phase 1）
   ├── python3 scripts/pick-cover.py <slug> → 分配封面
   ├── 确认 category 映射（见 writing-spec.md）
   └── 设定目标字数

3. 撰写（Phase 2）
   ├── 按 frontmatter 模板填写元数据
   ├── 按结构写正文（H2 hook → 分析 → 方案 → FAQ → footer cluster）
   ├── 内链仅用已验证 slug + signup + pricing
   └── 保存到 01-Drafts/

4. 发布（Phase 3）
   └── python3 publish-to-wp.py --file "xxx.md"
```

### 写作快速参考

| 文章类型 | 最小字数 | Category 值 |
|---------|---------|------------|
| 竞品对比 | **7500**（全分类统一地板） | `How-To` |
| Lovart 101 | **7500** | `Lovart 101` |
| How-To | **7500** | `How-To` |
| Best Practice | **7500** | `Best Practice` |
| 行业方案 | 2800 | `Industry Solution` |

**每篇必含块**：Derivative Scenarios + FAQ + E-E-A-T 信号 + 内链 + 图片附录 + cluster footer

**品牌术语**：MCoT、ChatCanvas、Touch Edit、Edit Elements、Nano Banana、Brand Kit、Design Agent

---

## 10. 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `publish-to-wp.py` 返回 HTTP 401 | Cookie 过期 | 脚本会自动重新登录 |
| CSV 导入后无图片 | cover_url 链接过期或网络问题 | 检查 CDN 域名可访问性 |
| showcase URL 404 | rewrite rules 未刷新 | WP 后台 Settings → Permalinks → 点保存 |
| `[showcase_grid]` 无输出 | 插件未激活或 CPT 无数据 | 检查 Plugins → 激活；确认有 published showcase |
| 面包屑不显示 | Rank Math 未开启 CPT 面包屑 | Rank Math → General Settings → Breadcrumbs → 勾选 Showcase |
