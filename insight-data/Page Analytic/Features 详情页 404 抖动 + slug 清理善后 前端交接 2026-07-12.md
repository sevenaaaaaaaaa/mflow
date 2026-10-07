---
type: engineering-issue
owner: lovart.ai 前端（Next.js）
created: 2026-07-12
status: open
severity: P1（Issue A，影响收录与用户体验） / P2（Issue B，善后）
related: /features 聚合页 404 排查、compositePage 数据卫生修复
---

# Features 详情页 404 抖动 + slug 清理善后 — 前端交接

> 面向 lovart.ai 前端仓库负责人。本文两件事：
> **Issue A** = `/features/[slug]` 间歇性 404 的根因与修复（本体，未修，需前端改）。
> **Issue B** = 2026-07-12 一批 Sanity slug 清理产生的 301 重定向需求（善后）。
> Sanity 侧数据已修复完毕；下面两项**只能在前端/基础设施层解决**。

---

## Issue A — `/features/[slug]` 间歇性 404（P1）

### 结论
详情页在**并发/突发流量**下会间歇性返回 404，同一个 URL 重试基本都能 200。这不是内容问题（Sanity 里页面已发布、有正文、`noIndex=false`），而是**详情页 SSR 实时取数在负载下失败后回落到 `notFound()`**。对用户是偶发 404，对 Googlebot 是间歇 404 → **实质性伤害收录**。

### 证据（2026-07-12 实测）
1. 同一 URL 结果不稳定：`ai-affiliate-ads-generator` 批量扫描时 404，单独重试连续 5 次全 200。
2. 单 URL 顺序请求 40 次 → 全部 200。
3. **并发 20 请求 60 个不同页面 → 18/60（30%）返回 404，外加 1 个连接失败（`000`）**；且每轮 404 命中的 slug 都不同（`bakery-menu-design`、`ai-poster-design-agent-nano-banana` 等"正常页"在并发下也会 404）。→ 与具体 slug 无关，纯随机、随负载出现。
4. 响应头：`cache-control: private, no-cache, no-store, must-revalidate` + `cf-cache-status: DYNAMIC`。**每次点击都穿透 CDN、实时 SSR、实时查 Sanity，无任何缓存兜底**——这是抖动被放大的根本原因。

### 复现命令
```bash
# 并发压测，观察 404 率
head -60 slugs.txt | xargs -P 20 -I{} sh -c \
  'echo "$(curl -s -o /dev/null -w "%{http_code}" "https://www.lovart.ai/features/{}") {}"' \
  | grep -v "^200 "
```

### 修复建议（按优先级）
1. **给详情页加缓存（最关键）**：改用 ISR —— `export const revalidate = 300`，或 `fetch(..., { next: { revalidate: 300 } })`，让成功响应可被 CDN/边缘缓存。绝大多数点击命中缓存后不再实时查 Sanity，抖动直接消失。
2. **区分"没查到"和"查失败"**：详情查询 **超时/抛错 → 返回 5xx（可重试）**；只有确认 `doc === null` 时才 `notFound()`（404）。当前把 fetch 失败也当 404，是最致命的一点——Google 会把可用页判为死链。
3. **Sanity 客户端走 CDN + 韧性**：`useCdn: true`（`apicdn.sanity.io`），取数加 3 次重试 + 超时兜底。
4. 修复后用上面的并发压测复跑，404 率应降到 ~0。

---

## Issue B — slug 清理产生的 301 重定向需求（P2 善后）

2026-07-12 在 Sanity 完成一批 compositePage 数据卫生修复，导致部分旧 URL 失效，需前端加 301：

### B1. restaurant 下划线合并
- 旧（已下线，将 404）：`/features/restaurant_menu_design`
- 新（现役）：`/features/restaurant-menu-design`
- **加 301：`/features/restaurant_menu_design` → `/features/restaurant-menu-design`**

### B2. ai-video-generator 重复拆分
- `/features/ai-video-generator` 仍有效（保留 v1，无需处理）。
- 新增 `/features/ai-video-generator-for-ads`（原 v2，已换 slug 上线）。无旧 URL 失效，无需 301。
- 小残留（可选）：`zh` 的 `ai-video-generator` 目前指向 v2(ads) 内容，与 en 的 v1 定位不一致，跨语言统一属另议。

### B3. draft- 前缀实验页全部下线（430 个）
- 路径分布：`/scenarios/draft-*`（418）、`/features/draft-*`（8）、`/tools/draft-*`（4）。
- 这些是今天才导入的半成品版式实验，**未进 sitemap、基本未收录、无流量**，下线后 404，SEO 风险低。
- 处理：**无需逐条 301**；确保它们从任何内部链接/聚合列表中移除即可（下线后聚合查询自然不再列出）。如担心零星外链，可对 `/scenarios/draft-*` 统一 410 Gone。

---

## 备注
- Sanity 侧全部改动遵守铁律：未删除任何 production 文档（改名走 patch、清理走 unpublish→草稿，430 页均可恢复）。
- Issue A 与 B 无依赖，可并行处理。Issue A 优先级更高（持续影响收录）。
