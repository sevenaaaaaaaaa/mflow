> **本目录是合并交付包**：26 个 sitemap + `robots.txt` + 3 个 `llms*` + 统一验收脚本。
> 给前端的执行顺序见 `00-替换说明.md`；本文档是完整对账与来龙去脉。

# Sitemap 重建 — 2026-11-09（对齐 CMS 真值）

> 目标：把「已经修好、但谷歌看不到」的页面重新写进 sitemap，并交回 GSC。
> **文件已经重建并逐条实测；卡点在发布 —— 线上 sitemap 仍是 2026-07 的旧文件。**

## 1. 为什么必须重建

| 证据 | 数值 |
|---|---|
| CMS 真值（Sanity 有 slug 的可路由文档，不含 es） | 15,447 条 |
| 线上 sitemap 实际 URL 数 | 20,458 条（含 2,421 条 profile） |
| 线上 sitemap 抽样 60 条实测 | **32 条 404（53%）** |
| 服务器 11-05 那套覆盖 | 12,563 / 15,447（**漏 3,447 条**） |
| 线上文件 lastmod | 2026-07-09 |

症状：`sitemap-scenarios.xml` 的 700 条 `draft-*` 全是 404；`sitemap-features.xml` 只有 1,796 条，而 CMS 里有 5,829 条。

## 2. 本档怎么生成的

1. 直连 Sanity production，GROQ 分页拉 `compositePage` / `blog` / `news`（排除 `drafts.**`）。
2. 按 `language + category + slug` 拼规范 URL（en 无前缀，其余 `/{lang}/`）。
3. 对 15,375 条唯一 URL **逐条发 HTTP 请求**（并发 16，HEAD 失败回落 GET）。
4. 只保留 200/301/302：**15,354 条通过**；21 条 404/500 剔除（见 §6）。
5. `lastmod` 取文档 `_updatedAt`，不是抓取时间。

### 未纳入 es（635 条）

`/es/*` 虽返回 200，但只是 `<html lang="es">` 换壳，`<title>` 仍是英文（幽灵语言）。按 es 语言政策，前端补齐 es 内容/hreflang 前不进 sitemap。

## 3. 文件清单（26 个）

| 文件 | URL 数 | 说明 |
|---|---|---|
| sitemap-index.xml | — | 30 条子项 |
| sitemap-features.xml | 5,814 | 全语言 features |
| sitemap-tools.xml | 1,145 | 全语言 tools |
| sitemap-topics.xml | 318 | 全语言 topics |
| sitemap-solutions.xml | 66 | 全语言 solutions |
| sitemap-news.xml | 19 | news |
| sitemap-blog.xml | 1,509 | **英文** blog（沿用历史口径） |
| sitemap-blog-{de,fr,it,ja,ko,pt,ru,zh,zh-TW}.xml | 645–934 | 各语言 blog |
| sitemap-lang-{10 语言}.xml | 428–1,024 | 该语言全部 composite 页 |

不改动：`sitemap-homepage.xml`、`sitemap-pricing.xml`、`sitemap-profile.xml`、`sitemap-other.xml`、`sitemap-docs.xml`（非 CMS 产物）。

## 4. 与线上对比

| 项 | 数 |
|---|---|
| 新增（线上 sitemap 没有、页面实测 200） | **4,994** |
| 移除（线上有、新档没有） | 10,098 |
| — 其中 profile（仍保留在 sitemap-profile.xml） | 2,421 |
| — 其余（draft / 幽灵语言 / 错前缀 / 已删） | 7,677 |
| — 移除项抽样 36 条 | **29 条 404** |

## 5. 发布（唯一剩下的步骤）

把本目录 26 个 XML **覆盖**到前端 sitemap 目录（`apps/lovart` 现有管线落点），并**删除线上 `sitemap-scenarios.xml`**（scenario 文档已归零，留着就是 700 条 404）。

部署后跑 `bash deploy-check.sh`，期望：index 30 条 / features 5,814 / tools 1,145 / blog 1,509 / `draft-` 0 次。

## 6. 被剔除的 21 条（CMS 有文档，线上 404/500）

| URL | 状态 |
|---|---|
| /tools/ai-audio-voice-generator | 500 |
| /de/tools/veo3.1 | 404 |
| /fr/tools/veo3.1 | 404 |
| /topics/ai-design-generator-landing-agent-workflow | 500 |
| /topics/ai-banner-landing-agent-workflow | 404 |
| /de/features/seedream-4.5 | 404 |
| /fr/features/seedream-4.5 | 404 |
| /it/features/seedream-4.5 | 404 |
| /ja/features/seedream-4.5 | 404 |
| /ko/features/seedream-4.5 | 404 |
| /pt/features/seedream-4.5 | 404 |
| /ru/features/seedream-4.5 | 404 |
| /de/features/veo3.1 | 404 |
| /fr/features/veo3.1 | 404 |
| /it/features/veo3.1 | 404 |
| /ja/features/veo3.1 | 404 |
| /ko/features/veo3.1 | 404 |
| /pt/features/veo3.1 | 404 |
| /ru/features/veo3.1 | 404 |
| /zh/topics/dall-e-image-generation-landing-trial-now | 404 |
| /zh/topics/image-to-video-ai | 404 |

这些不是 sitemap 问题：`veo3.1` / `seedream-4.5` 这类带点 slug 前端路由解析不了；`ai-audio-voice-generator`、`ai-design-generator-landing-agent-workflow` 返回 500。修路由或下线，别继续躺在 sitemap 里。

## 7. 部署后提交给谷歌

```bash
python3 gsc-submit.py            # 预演
python3 gsc-submit.py --apply    # 真提交
```

会做：提交 index 里 30 条；删除 `all-urls.txt`（16,592 行文本清单）、`sitemap.xml`（旧 19 条）、`sitemap-scenarios.xml` 的登记。
## 8. 同一批交付的其它文件（2026-11-09 追加）

| 文件 | 作用 |
|---|---|
| `robots.txt` | 单条 `Sitemap:` 指向 index；删掉 crawl-delay；把 CF 块与自有块的冲突理顺（详见说明文档） |
| `llms.txt` | 站点概览 + 6 板块真实数量 + 10 语言入口 + 使用政策（AI 搜索可引用、训练禁止） |
| `llms-blog.txt` | 1,510 篇英文博客，按 10 个真实分类分组 |
| `llms-full.txt` | 15,426 个页面全量，语言 → 板块 → 分类三层 |
| `robots-llms-说明.md` | robots/llms 的逐条改动理由 + hreflang/JSON-LD 现状实测 |
| `给前端-替换说明.md` | 一页纸：按顺序覆盖哪些、删哪个、怎么验收 |

注意：`robots.txt` 里写的 Allow 不能覆盖 Cloudflare 层的 AI 爬虫拦截（Baiduspider / PetalBot / KimiBot 目前被 CF 挡着），需在 CF 后台同步调整。
