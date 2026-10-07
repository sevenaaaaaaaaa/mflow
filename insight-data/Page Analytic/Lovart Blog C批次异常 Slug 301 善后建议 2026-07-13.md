---
type: engineering-issue
owner: lovart.ai 前端（Next.js）
created: 2026-07-13
status: ready
severity: P3（低优先级善后）
related: Lovart Blog C批次异常 Slug 善后 2026-07-13
---

# Lovart Blog C批次异常 Slug 301 善后建议 2026-07-13

## 结论

建议前端**补一条单独的永久重定向**：

- 旧：`/blog/https-www-lovart-ai-zh-blog-human-ai-cocreation-lovart-canvas-solopreneur-design`
- 新：`/blog/human-ai-cocreation-lovart-canvas-solopreneur-design`

优先级判断：**值得做，但不高，属于低成本 SEO/UX 善后**。

## 为什么建议做

虽然本轮没有看到强信号，但这条 301 的成本非常低，收益明确：

1. 该旧 URL 曾经真实上线过，而不是纯本地草稿路径。
2. Sanity 内容侧已经把 slug 全量切到新路径，旧路径现在不再对应 published 文档。
3. 本地 GSC 缓存里**未命中旧 URL 页面信号**，说明它不是高流量页，也不是当前重点收录页。
4. 但“没有最近 28 天信号”不等于“从未被抓取/从未被分享”。对于这种曾上线过的异常 URL，补一条 301 通常比放任 404 更干净。

所以结论不是“必须紧急做”，而是：

- **如果前端 redirect 维护成本很低，就应该做。**
- **如果本周前端带宽很紧，这条可以排在更高优先级问题后面。**

## 不做会怎样

不做也不是灾难，原因是：

- 旧 URL 当前没有在本地 GSC 缓存中体现出页面流量/曝光；
- 内容主体已经迁移到新 URL；
- 这不是站内大规模 slug 迁移，只是单条异常 URL。

但不做的代价是：

- 任何旧分享、旧抓取、旧外链命中该 URL 时都会落到 404；
- 对用户来说是坏体验；
- 对搜索引擎来说会留下一个本可平滑迁移却没有迁移的历史死链。

## 推荐动作

### 方案 A：直接加一条 301（推荐）

如果 `lovart.ai` 前端支持集中 redirect 配置，直接加：

```ts
{
  source: "/blog/https-www-lovart-ai-zh-blog-human-ai-cocreation-lovart-canvas-solopreneur-design",
  destination: "/blog/human-ai-cocreation-lovart-canvas-solopreneur-design",
  permanent: true,
}
```

适用场景：

- Next.js `redirects()`
- CDN / edge redirect rule
- Nginx / Cloudflare redirect rule

### 方案 B：如果暂时不加 301

可以接受暂时保持 404，但前提是：

- 新 URL 已正常可访问；
- 站内所有内部链接、canonical、structured data、sitemap 都只指向新 URL；
- 后续有空时再补这条 301。

## 当前已确认的内容侧状态

- 旧 slug：`https-www-lovart-ai-zh-blog-human-ai-cocreation-lovart-canvas-solopreneur-design`
- 新 slug：`human-ai-cocreation-lovart-canvas-solopreneur-design`
- 旧 slug published 数：`0`
- 新 slug published 数：`8`
- 新 slug 已覆盖多语言 published 文档
- 内容侧 `title` / `seo` / `structuredData` 残留已同步清理

## 最终建议

一句话版本：

**建议补这 1 条 301，但优先级只算 P3。**

它不是必须立刻抢修的问题，但属于“花 2 分钟消灭一个历史脏 URL 尾巴”的高性价比动作。
