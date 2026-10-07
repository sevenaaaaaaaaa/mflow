# /r/ Short Link TDK 优化方案

> **目标**：解决 Google 将 `/r/` 短链接页面误判为 noindex/duplicate 的问题  
> **影响范围**：Lovart.ai 全站 `/r/` 路径  
> **优先级**：P1（影响 SEO 收录）  

---

## 问题描述

`/r/xxx` 短链接是真实的功能页面，用户通过它们跳转到目标内容。但目前所有 `/r/xxx` 页面共用了 **同一套 TDK**（title、description、keywords），导致 Google 将大量 `/r/` 页面判定为"低质量重复内容"，触发了多类问题：
- 被标记为 `noindex`（搜索引擎暂不收录）
- 被标记为 `copycat`（重复页面）
- 被标记为 `plan b`（备用页面）

`/profile/` 已有独立 TDK 不在此方案范围内。

---

## 修改方案

### 方案 A：服务端动态 TDK（推荐）

在 Next.js 服务端渲染 `/r/:code` 页面时，动态生成 `<title>` 和 `<meta description>`：

```tsx
// app/(web)/[lang]/r/[code]/page.tsx (示意)

export async function generateMetadata({ params }) {
  const target = await fetchShortLink(params.code);
  
  return {
    title: target 
      ? `${target.title} - Lovart Short Link` 
      : `Short Link - Lovart AI Design Agent`,
    description: target?.description 
      ?? 'Discover AI-powered design tools, brand kits, and creative workflows on Lovart.',
    robots: { index: true, follow: true },
  };
}
```

### 方案 B：静态唯一标识符（最小改动）

如果方案 A 的后端查询成本过高，至少给每个 `/r/` 页面加唯一 `<title>`：

```tsx
title: `Short Link #${params.code} - Lovart`
```

---

## 额外需要加的标签

每个 `/r/:code` 页面 `<head>` 中确保存在：

```html
<link rel="canonical" href="https://www.lovart.ai/r/{code}">
<meta name="robots" content="index, follow">
```

---

## 预期效果

| 指标 | 修改前 | 修改后 |
|------|--------|--------|
| Google noindex 标记 | 大量 `/r/` 页面 | 消除 |
| Google copycat 标记 | 大量 | 消除 |
| canonical 引用 | 缺失 | 每个页面唯一 |

---

## 验证方式

1. 部署后，对任意 `/r/xxx` 页面右键查看源代码，确认 `<title>` 为唯一值
2. 在 Google Search Console 中提交 sitemap，观察 noindex 数量变化
3. 用 Bing SEO 报告跟踪 `/r/` 路径的 impressions 是否恢复
