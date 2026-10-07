# Skill: Sitemap & AI Search Optimization for Multi-Language Websites

> **适用场景**：Next.js SPA 多语言站点，需要生成完整 sitemap、优化 AI 搜索（Perplexity / ChatGPT / Gemini / Kimi / DeepSeek 等）、生成 Schema.org 结构化数据。

---

## 一、整体流程

```
1. 爬取分页列表页 → 提取真实 slug
2. 拉取服务器已有 sitemap → 获取额外 URL（profile/doc 等）
3. 合并去重 × 语言维度展开 → 生成 URL 全集
4. 分板块 + 分语言 → 生成子 sitemap + sitemap-index.xml
5. 按 AI 平台差异化 → 生成 robots.txt
6. 按 llms.txt 标准 → 生成分层知识索引
7. 按 Google 规范 → 生成 Schema.org JSON-LD
8. 部署到网站根目录
```

---

## 二、Step 1: 爬取分页列表页提取 slug

### 2.1 背景

Next.js SPA 的列表页，HTML 源码中的 `<a href>` 标签在服务端渲染（SSR）时已经包含链接，不需要等待 JS 执行。但 API 端点通常有 403 保护，所以走分页爬取。

### 2.2 脚本

```python
import urllib.request, re, time, ssl

BASE = "https://www.example.com"
H = {"User-Agent": "Mozilla/5.0 (compatible; SitemapCrawler/1.0)"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE  # 如有 SSL 波动

def crawl_section(section, max_pages=200):
    slugs = set()
    for page in range(1, max_pages + 1):
        url = f"{BASE}/{section}?page={page}"
        html = None
        for retry in range(3):  # 失败重试
            try:
                req = urllib.request.Request(url, headers=H)
                with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                    html = r.read().decode("utf-8", errors="replace")
                break
            except:
                time.sleep(2)
        
        if html is None:
            break
        
        # 从 <a href="/section/slug"> 提取 slug
        new = set(re.findall(rf'href="/{section}/([^"#?\s<>]+)"', html))
        slugs.update(new)
        
        if not new and empty_streak >= 3:
            break
        
        time.sleep(0.8)  # 限速，避免触发 Cloudflare 限制
    
    return sorted(slugs)

# 分板块爬取
for section in ["blog", "news", "tools", "features"]:
    slugs = crawl_section(section)
    print(f"{section}: {len(slugs)} slugs")
```

### 2.3 注意事项

- **SSL 波动**：Cloudflare 可能在连续请求后触发 SSL EOF。解决：`ssl.CERT_NONE` + 重试 + 限速
- **分页停止条件**：连续 3 页无新 slug → 停止
- **爬取速度**：0.5-1s/page，800 页约 10 分钟

---

## 三、Step 2: 拉取服务器已有 sitemap

### 3.1 发现 sitemap 列表

从 `robots.txt` 获取 sitemap 列表（服务器已有的）：

```python
SITEMAPS = [
    "sitemap.xml",
    "sitemap-profile.xml",
    "sitemap-blog.xml",
    "sitemap-blog-plus.xml",
    "sitemap-features.xml",
    "sitemap-features-plus.xml",
    "sitemap-tools.xml",
    "sitemap-tools-plus.xml",
    "sitemap-news.xml",
    "sitemap-doc.xml",
]

server_urls = set()
for sm in SITEMAPS:
    content = fetch(f"{BASE}/{sm}")
    locs = re.findall(r'<loc>(https?://[^<]+)</loc>', content)
    server_urls.update(locs)
```

### 3.2 用途

服务器 sitemap 通常包含：
- Profile 页面（用户生成内容，爬虫无法列表页发现）
- 文档页面（/docs/）
- 不同语言版本的已有 URL

---

## 四、Step 3: 合并去重 × 语言展开

### 4.1 语言前缀

从 HTML 的 `hreflang` 标签确认语言列表：

```python
LANGS = ["", "/zh", "/zh-TW", "/ja", "/ko", "/de", "/fr", "/pt", "/ru", "/it"]
LANG_CODES = ["en", "zh", "zh-TW", "ja", "ko", "de", "fr", "pt", "ru", "it"]
```

### 4.2 URL 生成

```python
all_urls = set()

# 首页（10 语言）
for prefix in LANGS:
    all_urls.add(f"{BASE}{prefix}/")

# 板块首页（10 语言 × 板块）
for sec in ["features", "tools", "blog", "news", "pricing", "r"]:
    for prefix in LANGS:
        all_urls.add(f"{BASE}{prefix}/{sec}")

# 子页面 slug（10 语言 × slug）
for sec in ["blog", "news", "tools", "features"]:
    for slug in crawled_slugs[sec]:
        for prefix in LANGS:
            all_urls.add(f"{BASE}{prefix}/{sec}/{slug}")

# 服务器 sitemap 里的额外 URL
for u in server_urls:
    all_urls.add(u)
```

### 4.3 分类

```python
def get_section(url):
    parts = urlparse(url).path.strip("/").split("/")
    if not parts: return "homepage"
    # 处理语言前缀：/zh/blog/xxx → blog
    if parts[0] in LANG_CODES:
        return parts[1] if len(parts) > 1 else "homepage"
    return parts[0]

def get_lang(url):
    path = urlparse(url).path
    for i, prefix in enumerate(LANGS):
        if prefix and path.startswith(prefix + "/"):
            return LANG_CODES[i]
    return "en"
```

---

## 五、Step 4: 生成 sitemap XML

### 5.1 结构

```
sitemap-index.xml       ← Google Search Console 提交这个
├── sitemap-blog.xml
├── sitemap-features.xml
├── sitemap-tools.xml
├── sitemap-news.xml
├── sitemap-pricing.xml
├── sitemap-r.xml
├── sitemap-homepage.xml
├── sitemap-profile.xml
├── sitemap-docs.xml
├── sitemap-lang-en.xml
├── sitemap-lang-zh.xml
├── ... (每个语言一个)
```

### 5.2 sub-sitemap 格式

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/page</loc>
    <lastmod>2026-05-19</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

- **priority**：首页 1.0 → 板块首页 0.9 → 子页 0.8
- **changefreq**：首页 daily，其他 weekly

### 5.3 sitemap-index 格式

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.example.com/sitemap-blog.xml</loc>
    <lastmod>2026-05-19</lastmod>
  </sitemap>
  <!-- ... -->
</sitemapindex>
```

### 5.4 注意

- 子 sitemap 最多 50,000 URL / 50 MB，超过需拆分
- `lastmod` 更新为当天，Google 会对比旧版判断是否有变化
- `priority` 是相对值，Google 不保证遵守但会参考

---

## 六、Step 5: robots.txt — 分平台差异化

### 6.1 设计原则

```
Tier 1: 主流搜索引擎 → 全 Allow
Tier 2: AI 搜索 → Allow 搜索，Disallow 训练（用 Content-Signal）
Tier 3: 中文 AI → Allow（Kimi/DeepSeek/豆包特定 bot）
Tier 4: 社交媒体 → Allow（链接预览用）
Tier 5: SEO 爬虫 → Disallow（浪费预算）
```

### 6.2 关键规则

```txt
# 全局信号
User-agent: *
Content-Signal: search=yes,ai-input=yes,ai-train=no

# AI 搜索 bot（允许爬取）
User-agent: OAI-SearchBot
Allow: /

# AI 训练 bot（禁止）
User-agent: GPTBot
Disallow: /

# 中文 AI 平台
User-agent: Bytespider
Disallow: /
Crawl-delay: 5

User-agent: MoonshotBot
Allow: /
Crawl-delay: 3

User-agent: DeepseekSpider
Allow: /
Crawl-delay: 3
```

### 6.3 各平台 Bot 清单

| 平台 | 搜索 Bot | 训练 Bot |
|------|---------|---------|
| Google | Googlebot | Google-Extended |
| ChatGPT | OAI-SearchBot | GPTBot |
| Perplexity | PerplexityBot | — |
| Claude | ClaudeBot | ClaudeBot |
| Kimi (月之暗面) | MoonshotBot | — |
| DeepSeek | DeepseekSpider | — |
| 豆包 (ByteDance) | Bytespider | — |
| 元宝 (腾讯) | 无独立 bot，走 Bing | — |
| 千问 (阿里) | 无公开 bot | — |

---

## 七、Step 6: llms.txt — AI 搜索知识索引

### 7.1 标准来源

llms.txt 由 Jeremy Howard (answer.ai) 提出，是一个面向 AI 爬虫的 Markdown 文件，放在网站根目录。

### 7.2 分层策略

| 文件 | 用途 | 平台偏好 |
|------|------|---------|
| `llms.txt` | 入口索引，指向子文件 | 全部 |
| `llms-blog.txt` | 全部博客按分类 + 链接 | ChatGPT, Kimi |
| `llms-features.txt` | 全部功能页 + 链接 | ChatGPT |
| `llms-tools.txt` | 全部工具页 + 链接 | ChatGPT |
| `llms-full.txt` | **单文件全量**（所有 slug + 链接） | **Perplexity 优先** |
| `llms-knowledge.txt` | 深度知识库（产品/技术/Prompt/竞品） | Claude, Gemini |

### 7.3 llms.txt 格式示例

```markdown
# Example Site — LLMs.txt

> Brief description of what this website is.
> https://www.example.com

## Core Pages

- [Home](https://www.example.com/): Homepage description
- [Blog](https://www.example.com/blog): 855 articles

## AI Search Knowledge Base

| File | Contents | Pages |
|------|----------|-------|
| [llms-blog.txt](.../llms-blog.txt) | All blog articles | 855 |
| ... |
```

### 7.4 slug → title 转换

```python
def slug_to_title(slug):
    slug = slug.replace("-", " ")
    words = slug.split()
    result = []
    for w in words:
        if w.upper() in {"AI","UI","SVG","SEO","B2B","3D","4K","SaaS"}:
            result.append(w.upper())
        else:
            result.append(w[0].upper() + w[1:] if w else w)
    return " ".join(result)
```

### 7.5 博客分类启发式

```python
def guess_category(slug):
    s = slug.lower()
    if any(k in s for k in ["review","alternative","vs","comparison"]):
        return "AI Tool Reviews & Comparisons"
    if any(k in s for k in ["how-to","guide","tutorial","workflow"]):
        return "Guides & Tutorials"
    if any(k in s for k in ["logo","brand","branding"]):
        return "Branding & Logo Design"
    # ... more categories
    return "General & Tips"
```

---

## 八、Step 7: Schema.org JSON-LD 结构化数据

### 8.1 首页需要的 Schema

首页 `<head>` 中嵌入以下 4 个 schema：

| Schema | @type | Google 富结果 |
|--------|-------|:--:|
| 1 | `Organization` | 品牌知识面板 |
| 2 | `WebSite` + `SearchAction` | 站点搜索框 |
| 3 | `SoftareApplication` | 应用详情 |
| 4 | `BreadcrumbList` | 面包屑导航 |

### 8.2 Organization 关键字段

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://www.example.com",
  "logo": "https://www.example.com/favicon.ico",
  "sameAs": [
    "https://twitter.com/...",
    "https://www.instagram.com/...",
    "https://www.linkedin.com/company/...",
    "https://www.youtube.com/@..."
  ],
  "foundingDate": "2025",
  "founders": [
    {"@type": "Person", "name": "...", "jobTitle": "Co-Founder & CEO"}
  ],
  "areaServed": [
    {"@type": "Country", "name": "United States"},
    {"@type": "Country", "name": "China"}
  ]
}
```

### 8.3 博客页 Schema

每篇 `/blog/{slug}` 页面嵌入：

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{ARTICLE_TITLE}}",
  "description": "{{ARTICLE_DESCRIPTION}}",
  "datePublished": "{{DATE}}",
  "dateModified": "{{DATE}}",
  "author": {"@type": "Organization", "name": "..."},
  "publisher": {"@type": "Organization", "name": "...", "logo": {...}}
}
```

### 8.4 定价页 FAQ Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do credits work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "..."
      }
    }
  ]
}
```

### 8.5 其他模板

- `HowTo` — 教程类博客（step 列表）
- `NewsArticle` — 新闻页
- `BreadcrumbList` — 每个分页自己的面包屑

### 8.6 验证

部署后用 Google 的 Rich Results Test 验证：
https://search.google.com/test/rich-results

---

## 九、部署清单

| 类别 | 文件 | 路径 |
|------|------|------|
| Sitemap 索引 | `sitemap-index.xml` | 网站根目录 |
| 子 Sitemap | `sitemap-*.xml` (17 个) | 网站根目录 |
| AI 爬虫规则 | `robots.txt` | 网站根目录 |
| AI 知识索引 | `llms.txt` | 网站根目录 |
| AI 知识子索引 | `llms-*.txt` (5 个) | 网站根目录 |
| Schema 模板 | `schema-snippets/` | 开发参考目录 |
| URL 全集 | `all-urls.txt` | 参考用，不需部署 |

### Google Search Console

1. 提交 `sitemap-index.xml`
2. 检查覆盖率报告
3. 修复任何抓取错误

### Bing Webmaster（覆盖元宝）

1. 提交 `sitemap-index.xml`
2. 验证站点所有权

---

## 十、持续维护

### 10.1 新增博客 / 功能 / 工具时

1. 重新运行 Step 1 爬虫（或从 CMS API 获取新 slug）
2. 重新运行 Step 3-4 生成 sitemap
3. 更新 `llms-blog.txt` 等索引文件
4. 上传新文件

### 10.2 新增语言时

1. 在 LANGS 数组添加新语言前缀
2. 重新运行 Step 3-4 生成 sitemap
3. 更新所有 llms 文件
4. 在 robots.txt 的 sitemap 列表中无需修改（sitemap-index 已包含）

### 10.3 Schema 更新

当 Google 推出新 Schema 类型或字段时，修改 `structured-data.json` 并重新生成 HTML 片段。

---

## 十一、自动化脚本

### 11.1 一键生成

`generate-all.py` + `config.example.json` 放在 skills 目录下，使用方法：

```bash
# 完整运行（爬取 + 拉取 sitemap + 生成全部文件）
python3 generate-all.py config.json

# 跳过爬取（使用上次缓存的 slug）
python3 generate-all.py config.json --skip-crawl

# 完全离线（不联网，只用缓存数据）
python3 generate-all.py config.json --offline

# 只生成 sitemap
python3 generate-all.py config.json --only-sitemaps

# 只生成 robots.txt
python3 generate-all.py config.json --only-robots
```

### 11.2 配置文件

复制 `config.example.json` 为新项目配置，修改以下字段：

| 字段 | 说明 |
|------|------|
| `site.base_url` | 网站 URL |
| `site.name` | 品牌名 |
| `languages.prefixes` | URL 语言前缀列表 |
| `languages.codes` | 语言代码列表 |
| `sections.listable` | 可爬取分页列表的板块 |
| `sitemap.server_files` | 服务器已有 sitemap 列表 |
| `output.dir` | 输出目录 |

### 11.3 输出结构

```
output/
├── sitemap-index.xml          # 总索引
├── sitemap-{section}.xml      # 按板块
├── sitemap-lang-{lang}.xml    # 按语言
├── robots.txt                 # 分平台差异化规则
├── llms.txt                   # AI 搜索入口
├── llms-{blog,news,...}.txt   # 按板块索引
├── llms-full.txt              # 单文件全量
├── all-urls.txt               # 完整 URL 列表
├── crawled_slugs.json         # 爬取缓存
└── schema-snippets/           # Schema.org HTML 片段
```

### 11.4 定时更新

建议用 cron 每周自动运行：

```bash
0 2 * * 1 cd /path/to/skills && python3 generate-all.py config.json --skip-crawl >> logs/cron.log 2>&1
```

---

## 十二、常见问题

### Q: 爬虫在 SSL 上卡住了？

A: 使用 `ssl.CERT_NONE` + 重试 3 次 + 0.8s 间隔。Cloudflare 可能触发 SSL EOF。

### Q: 为什么搜索引擎不遵守 robots.txt 的优先级？

A: priority 是建议值，搜索引擎会自己对页面重要性建模。重点保证 sitemap 包含所有 URL。

### Q: llms.txt 真的有效吗？

A: Perplexity 已正式支持。OpenAI / Anthropic 在跟进。即使未被直接使用，它作为内部结构化索引也有价值。

### Q: 元宝 / 千问没有独立 bot 怎么办？

A: 元宝走 Bing 索引，在 Bing Webmaster 提交 sitemap 即可。千问通过标准网络爬取。
