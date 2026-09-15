---
name: lovart-product-sanity-publish
description: 将本地 Product 页面 JSON（composite-v2，category product）安全同步到 Sanity production。用于用户提到 Product 发布、Products/en、chatcanvas、brand-kit、import-page、compositePage product 时。
disable-model-invocation: true
---

# Lovart Product → Sanity 发布

> Support-only：本 skill 只作为 `lovart-sanity-publish` 的内部 Product 执行管道，不直接响应用户发布请求。用户提到发布/同步/import Product 时，先进入 `lovart-sanity-publish` 父入口。

## 铁律（与 Blog/Features/Tools 一致）

- 只用 **`import --missing`**（单篇经 `import-page.js --import`）
- ❌ 不 `sanity deploy`、不改 schema、不 `--replace`、不删文档
- projectId **`o11tm2qe`** · dataset **`production`**

## SSOT

执行细节只读同目录：**[`SOP-Lovart-Product-Sanity-发布统合指南.md`](./SOP-Lovart-Product-Sanity-发布统合指南.md)**

内容生产 SSOT：**[`PRODUCT-PRODUCTION.md`](../../../../1-3 Content Gen/Page Gen/Refresh-Page/PRODUCT-PRODUCTION.md)** · Step 0 **[`PAGE-BRIEF.md`](../../../../1-3 Content Gen/Page Gen/Refresh-Page/PAGE-BRIEF.md)**

## 快速流程

```bash
cd "1-4 Dev/lovart.sanity.studio"
PRODUCTS="../../1-3 Content Gen/Page Gen/Pages/Products/en"

# 1. 结构 + 内容预检
node scripts/preflight-content.js --type composite-v2 --dir "$PRODUCTS"

# 2. 单篇 dry-run（不写线上）
node scripts/import-page.js "$PRODUCTS/chatcanvas-en.json" --dry-run
node scripts/import-page.js "$PRODUCTS/brand-kit-en.json" --dry-run

# 3. 用户确认后导入（--missing）
node scripts/import-page.js "$PRODUCTS/chatcanvas-en.json" --import
node scripts/import-page.js "$PRODUCTS/brand-kit-en.json" --import
```

## 门禁话术

与 Blog 发布协议一致：先输出 dry-run 摘要 → 等用户 **`import confirmed`** → 再 `--import`。

## 参考案例

| 文件 | 故事线 | `_id` 预期 |
|------|--------|------------|
| `chatcanvas-en.json` | `product-标准` | `chatcanvas-en` |
| `brand-kit-en.json` | `product-含社会证明` | `brand-kit-en` |

两篇默认 **`seo.noIndex: true`**（参考稿）；正式 SEO 上线前在 Studio 改 `false`，勿在未授权时用 `--replace` 覆盖已编辑文档。
