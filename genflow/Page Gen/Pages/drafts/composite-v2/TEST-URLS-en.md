# Composite v2 草稿 — 英文测试 URL 清单

> 修订：2026-05-31  
> **英语为默认语言：URL 无 `/en/` 前缀。**  
> 数据在 Sanity `production`（`language: "en"`）；**前端 v2 预览请用预发域名。**

## 域名

| 环境 | 基址 |
|------|------|
| **预发 / 前端测试（推荐）** | `https://www-pre.lovart.vip` |
| 生产 | `https://www.lovart.ai` |

| category | URL 模式（en） |
|----------|----------------|
| feature | `{基址}/features/{slug}` |
| tool | `{基址}/tools/{slug}` |

---

## 预发环境 — AI Logo Maker

### Features

| 故事线 | Slug | 预发 URL |
|--------|------|----------|
| **F1** | `draft-ai-logo-maker-f1` | https://www-pre.lovart.vip/features/draft-ai-logo-maker-f1 |
| **F2** | `draft-ai-logo-maker-f2` | https://www-pre.lovart.vip/features/draft-ai-logo-maker-f2 |
| **F4** | `draft-ai-logo-maker-f4` | https://www-pre.lovart.vip/features/draft-ai-logo-maker-f4 |
| **F5** | `draft-ai-logo-maker-f5` | https://www-pre.lovart.vip/features/draft-ai-logo-maker-f5 |
| **F6** | `draft-ai-logo-maker-f6` | https://www-pre.lovart.vip/features/draft-ai-logo-maker-f6 |

### Tools

| 故事线 | Slug | 预发 URL |
|--------|------|----------|
| **T1** | `draft-ai-logo-maker-t1` | https://www-pre.lovart.vip/tools/draft-ai-logo-maker-t1 |
| **T2** | `draft-ai-logo-maker-t2` | https://www-pre.lovart.vip/tools/draft-ai-logo-maker-t2 |
| **T4** | `draft-ai-logo-maker-t4` | https://www-pre.lovart.vip/tools/draft-ai-logo-maker-t4 |

---

## 预发环境 — AI Sales Deck PPT Generator

### Features

| 故事线 | Slug | 预发 URL |
|--------|------|----------|
| **F1** | `draft-ai-sales-deck-ppt-generator-f1` | https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-f1 |
| **F2** | `draft-ai-sales-deck-ppt-generator-f2` | https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-f2 |
| **F7** | `draft-ai-sales-deck-ppt-generator-f7` | https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-f7 |
| **S1** | `draft-ai-sales-deck-ppt-generator-s1` | https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-s1 |

### Tools

| 故事线 | Slug | 预发 URL |
|--------|------|----------|
| **N5** | `draft-ai-sales-deck-ppt-generator-n5` | https://www-pre.lovart.vip/tools/draft-ai-sales-deck-ppt-generator-n5 |
| **T1** | `draft-ai-sales-deck-ppt-generator-t1` | https://www-pre.lovart.vip/tools/draft-ai-sales-deck-ppt-generator-t1 |
| **T2** | `draft-ai-sales-deck-ppt-generator-t2` | https://www-pre.lovart.vip/tools/draft-ai-sales-deck-ppt-generator-t2 |

---

## 预发纯链接列表（复制给前端）

```
https://www-pre.lovart.vip/features/draft-ai-logo-maker-f1
https://www-pre.lovart.vip/features/draft-ai-logo-maker-f2
https://www-pre.lovart.vip/features/draft-ai-logo-maker-f4
https://www-pre.lovart.vip/features/draft-ai-logo-maker-f5
https://www-pre.lovart.vip/features/draft-ai-logo-maker-f6
https://www-pre.lovart.vip/tools/draft-ai-logo-maker-t1
https://www-pre.lovart.vip/tools/draft-ai-logo-maker-t2
https://www-pre.lovart.vip/tools/draft-ai-logo-maker-t4
https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-f1
https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-f2
https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-f7
https://www-pre.lovart.vip/features/draft-ai-sales-deck-ppt-generator-s1
https://www-pre.lovart.vip/tools/draft-ai-sales-deck-ppt-generator-n5
https://www-pre.lovart.vip/tools/draft-ai-sales-deck-ppt-generator-t1
https://www-pre.lovart.vip/tools/draft-ai-sales-deck-ppt-generator-t2
```

---

## Sanity 文档 _id（GROQ 抽查）

```groq
*[_type == "compositePage" && slug.current match "draft-ai-*" && language == "en"]{
  _id, category, "slug": slug.current, language
} | order(slug.current asc)
```

## 故事线说明

- **draft-ai-logo-maker-f1** (F1): Trial → workflow → feature grid → testimonial → FAQ
- **draft-ai-logo-maker-f2** (F2): Cinematic + capability tabs + comparison
- **draft-ai-logo-maker-f4** (F4): Before/after + canvas wall
- **draft-ai-logo-maker-f5** (F5): Hero journey + launch identity
- **draft-ai-logo-maker-f6** (F6): Tool matrix / ecosystem
- **draft-ai-logo-maker-t1** (T1): Standard tool page
- **draft-ai-logo-maker-t2** (T2): Quick utility
- **draft-ai-logo-maker-t4** (T4): Comparison / decision stage
- **draft-ai-sales-deck-ppt-generator-f1** (F1): Baseline sales deck feature
- **draft-ai-sales-deck-ppt-generator-f2** (F2): Cinematic enablement
- **draft-ai-sales-deck-ppt-generator-f7** (F7): Full agent workflow
- **draft-ai-sales-deck-ppt-generator-s1** (S1): Enterprise solution
- **draft-ai-sales-deck-ppt-generator-n5** (N5): Pricing / ROI
- **draft-ai-sales-deck-ppt-generator-t1** (T1): Standard tool
- **draft-ai-sales-deck-ppt-generator-t2** (T2): Quick generator
