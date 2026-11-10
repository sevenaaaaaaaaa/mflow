# Sanity Blog — `es`（西班牙语）语言策略

> **Canonical**：Blog / preflight / convert 语言集合不一致时的 SSOT。  
> 关联：[`SOP-品牌方-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](./SOP-品牌方-Sanity-Blog-Features-Tools-换设备交接与首次运行.md) §12

---

## 现状（2026-05 production）

| 层 | `es` 状态 |
|----|-----------|
| **线上 dataset** | 约 **859** 篇 `blog` 文档 `language: es` |
| **Studio Blog schema** | 未在 `i18n/locales.ts` 正式声明 |
| **`preflight-content.js`** | `VALID_LANGS` **不含** `es` → 新 MD 写 `language: es` 会 **BLOCK** |
| **`convert.js`** | `LANG_PRIORITY` 含 `es`（仅排序）；会 convert 已有 es MD |
| **Features / Tools** | `VALID_LANGS` **不含** `es` |

---

## 决策（内容管道 Agent 必守）

**新稿默认禁止 `es`**，直到产品明确将西班牙语纳入主站 i18n 并完成：

1. `品牌.sanity.studio` schema / locales 增加 `es`  
2. `preflight-content.js` `VALID_LANGS` 增加 `es`  
3. 前端 `apps/品牌` 路由与 hreflang 支持 `es`  
4. 与存量 859 篇 slug / metadata 对齐方案

---

## 接手人勿做什么

| ❌ 禁止 | 原因 |
|--------|------|
| 因线上有 859 篇 es 而全量重导 | 存量债，用增量 + patch 脚本处理 |
| 批量删 production `language: es` 文档 | 需业务 + 前端确认 |
| 在 preflight 未改前发布 `language: es` 新 MD | 会被 BLOCK；即使强行 import 前端可能 404 |

---

## 若业务决定正式支持 `es`

按顺序：

1. 前端 + schema 团队添加 locale  
2. 更新本仓库 `VALID_LANGS`（preflight、Features/Tools convert）  
3. 更新 [`Sanity-Blog-发布统合指南.md`](../Sanity-Blog-发布统合指南.md) 语言表  
4. 跑 `link-translations.js` 将 es 纳入 `translation.metadata`  
5. 小批量 `--missing` 试跑 + verify

---

## GROQ 抽查

```bash
npx sanity documents query 'count(*[_type == "blog" && language == "es"])' --dataset production
```

---

## 决策更新（2026-11-05）：**业务已拍板——正式接入 es**

| 步骤 | 状态 | 责任方 |
|---|---|---|
| 1. Studio schema `i18n/locales.ts` + 前端 es 路由/hreflang | **待实施（研发）** | schema 团队 + 前端（Studio repo 与 apps/lovart 均不在内容侧仓库） |
| 2. 仓库 VALID_LANGS（preflight / Features/Tools convert）加 es | 待实施（Studio repo 侧脚本；本服务器无 Studio 工具链） | 内容侧（需 Studio repo 路径） |
| 3. 发布指南语言表更新 | ✅ 已更新（2026-11-05，见 §语言表 es 行） | 内容侧 |
| 4. link-translations.js 纳入 es | 待实施（Studio repo） | 内容侧（同上） |
| 5. 小批量 --missing 试跑 + verify | 待实施（依赖 1/2） | 内容侧 |
| 6. 存量 631 篇 es blog 内容治理 | 已部分完成：author/structuredData ✅；**534 篇英文正文待翻译（优先级已提升）**；76 封面待补 | 内容侧（翻译批次队列） |

**硬依赖**：步骤 1（前端 es 路由 + schema locale）是先决——在此之前不向 es 发布新内容
（否则重演"英文标题+日语正文"式页面）。
