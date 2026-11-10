# robots.txt / llms.txt 改动说明 + hreflang / JSON-LD 现状

> 2026-11-09。所有数字都是当天线上实测或 CMS 真值，不是估算。

## 一、robots.txt：4 个问题，1 个必须修

| # | 现状（线上原文） | 影响 | 处理 |
|---|---|---|---|
| 1 | `Sitemap:` 逐条列了 **27 条**，却**没有 `sitemap-index.xml`**，还留着 `sitemap-scenarios.xml`（700 条 draft 全 404） | 谷歌按这 27 条逐个抓，其中一条整份是死链 | 改成**一条** `Sitemap: https://www.lovart.ai/sitemap-index.xml`（index 会带出全部 30 条） |
| 2 | 文件头是 Cloudflare 托管块，正文又有一份自有块；**Baiduspider 在 CF 块 `Disallow: /`，在自有块 `Allow: /`**；PetalBot、KimiBot 同样被 CF 封 | 中文搜索/AI 抓取被拦，且两份策略互相矛盾 | 自有块只保留一份策略；**CF 后台需同步关掉对应 AI 爬虫拦截**（只改文件不生效） |
| 3 | `Content-Signal` 出现两次且值不同：CF 是 `search=yes,ai-train=no,use=reference`，自有块是 `search=yes,ai-input=yes,ai-train=no` | 信号冲突 | 统一为 `search=yes,ai-input=yes,ai-train=no` |
| 4 | 大量 `Crawl-delay: 1/2/3` | Google 直接忽略；Bing 会据此降速 | 全部删除 |

**交付文件**：`robots.txt`（128 行）。

**需要 Cloudflare 侧配合的事**（文件改不动其中任何一条）：

- 若开启 *Managed robots.txt*，CF 会再注入一段，建议关掉，让这份文件成为唯一事实源。
- `Baiduspider`、`PetalBot`、`KimiBot` 目前在 CF 的 AI 爬虫拦截里，要放行得去 CF 后台「Security → Bots → 配置」调整。

## 二、llms.txt：三份文件互相打架

| 文件 | 线上生成日期 | 自报数量 | 真实值（本次对账） |
|---|---|---|---|
| llms.txt | 2026-07-09 | blog 1,547 / tools 617 / features 246 | blog 8,058（en 1,510）/ tools 1,145 / features 5,815 |
| llms-full.txt | **2026-05-31** | blog 1,089 / tools 47 / features 229 | 同上，且比 llms.txt 还旧 |
| llms-blog.txt | 2026-07-09 | 1,552 篇英文博客 | 1,510 篇（与 sitemap 同口径） |

三份文件三套数字，等于给 AI 三个不同的站点认知。本次按 sitemap 同一份真值重生成：

| 文件 | 大小 | 内容 |
|---|---|---|
| `llms.txt` | 2 KB | 站点是什么 + 6 个板块真实数量 + 10 个语言入口 + 使用政策（可引用、不可训练） |
| `llms-blog.txt` | 204 KB | 1,510 篇英文博客，按 10 个真实分类分组 |
| `llms-full.txt` | 2.2 MB | 15,426 个页面全量，按语言 → 板块 → 博客分类三层组织 |

> 2.2 MB 是「全量」的代价。如果嫌大，可以只保留 `llms.txt` + `llms-blog.txt`，`llms-full.txt` 改成按语言拆（`llms-full-en.txt` 等）。

## 三、hreflang：**没修**，问题原样在线上

实测 `/ja/blog/heygen-review`（2026-11-09）：

```html
<link rel="alternate" hrefLang="en" href="/blog/heygen-review"/>
... 共 12 条：11 语言 + x-default
<link rel="alternate" hrefLang="it" href="/it/blog/heygen-review"/>   ← 实测 404
<link rel="alternate" hrefLang="es" href="/es/blog/heygen-review"/>   ← 只有英文壳
```

- 仍是**无条件输出全语言**，不查该语言是否真有文档；抽样这一页 12 条里 `it` 直接 404。
- `es` 被列进去了，但 `/es/` 页面只是 `<html lang="es">` 换壳、`<title>` 还是英文。
- 属性名写成了 `hrefLang`（HTML 大小写不敏感，能解析，但不规范），href 用的是相对路径。
- 结论：`frontend-patch-pack-20261104.md` 的 **Patch 2 未落地**。

## 四、JSON-LD：数据层完成，渲染层只做了一半

以 `/blog/heygen-review`、`/ja/blog/heygen-review`、`/zh/features/ai-poster-creator` 实测：

| 检查项 | 结果 |
|---|---|
| Sanity 里 `seo.structuredData` 覆盖 | 100%（Article / WebPage 已回填） |
| 页面 payload 里的 schema 类型 | 有：BlogPosting / Article / Organization / WebSite / ImageObject / Person |
| 真实 `<script type="application/ld+json">` 标签数 | **0** |

也就是说：对象是有的，但它躺在 Next 的 RSC flight 数据里（`self.__next_s.push([0,{"type":"application/ld+json",...}])`），要等 JS 执行完才注入。
Googlebot 会渲染 JS，所以**大概率能读到**，但这不是可靠路径：Bing / 其他爬虫 / 富媒体测试的初始抓取都看不到。

修法还是 Patch 1 那 3 行 —— 把对象渲染成真正的 script 标签放进 `<head>`：

```tsx
{post?.seo?.structuredData?.enabled && (
  <script type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: post.seo.structuredData.json }} />
)}
```

验收：`curl -s https://www.lovart.ai/blog/heygen-review | grep -c '<script type="application/ld+json"'` 必须 ≥ 1（现在 0）。
