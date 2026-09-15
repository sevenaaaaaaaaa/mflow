# Lovart Product → Sanity 发布统合指南

> **单一事实来源（SSOT）**：本地 Product 页面 JSON（composite-v2）同步到 Sanity `production`。  
> **Skills 目录副本**：`1-1 Harness/Skills/lovart-product-sanity-publish/SOP-Lovart-Product-Sanity-发布统合指南.md`  
> **内容生产**：[`PRODUCT-PRODUCTION.md`](../../../../1-3 Content Gen/Page Gen/Refresh-Page/PRODUCT-PRODUCTION.md)

---

## 1. 文档地图

| 用途 | 文件 |
|------|------|
| 三条+管道总索引 | `lovart-sanity-content-publish/SOP-Lovart-Sanity-内容发布总指南.md` |
| **本指南（Product SSOT）** | 本文 |
| Agent Skill | 同目录 `SKILL.md` |
| 参考 JSON | `1-3 Content Gen/Page Gen/Pages/Products/en/` |
| 单篇导入 | `sanity-studio/scripts/import-page.js` |
| 批量（未来） | `convert-products.js`（待建；当前用单篇 `import-page.js`） |
| 全局红线 | `.cursor/rules/lovart-sanity-content-pipeline.mdc` |

---

## 2. 心智模型

- **Schema 真源**：`lovart.sanity.studio`（`compositePage` + `category`）
- **内容 cwd**：`1-4 Dev/lovart.sanity.studio/`
- **Studio 导航**：Content → **Products**，`category == "product"`
- **URL**：`https://www.lovart.ai/product/{slug}`（en）；`/{lang}/product/{slug}`（i18n）
- **格式**：`schemaVersion: composite-v2`，`bodyJson` 字符串 + `section[]` 镜像

Product **不走** legacy `convert-tools.js` / 五段式 Features 转换；本地 JSON 已是 Refresh-Page 33 种 `type`。

---

## 3. 安全红线

| ❌ 禁止 | ✅ 允许 |
|--------|--------|
| `sanity deploy` | `preflight` → `import-page.js --dry-run` → `--import` |
| 改 schema / config | GROQ 验证 + Studio 抽查 |
| `--replace`（无明确授权） | **`--missing` only** |
| 删 production 文档 | 新增 `_id` 不存在的 Product 页 |

**参考稿默认 `seo.noIndex: true`** — 同步到线上不会立刻被收录；SEO 正式版在 Studio 改 `noIndex: false`。

---

## 4. 端到端流程

### Gate 0 — 环境

```bash
cd "1-4 Dev/lovart.sanity.studio"
grep -E "SANITY_STUDIO_PROJECT|SANITY_STUDIO_DATASET" .env
# o11tm2qe / production
npx sanity debug --secrets
git status   # 无 schema 误改
```

### Gate 1 — 本地 JSON checklist

- [ ] 路径 `Pages/Products/{lang}/{slug}-{lang}.json`
- [ ] `category: "product"` · `schemaVersion: "composite-v2"`
- [ ] `storyline` 与 section `type` 序列一致（见 `PRODUCT-PRODUCTION.md` §4.1）
- [ ] 图片 URL 优先 `https://assets-persist.lovart.ai/`
- [ ] `_id` 策略：`{slug}-{lang}`（如 `chatcanvas-en`）

### Gate 2 — 预检

```bash
PRODUCTS="../../1-3 Content Gen/Page Gen/Pages/Products/en"

node scripts/preflight-content.js --type composite-v2 --dir "$PRODUCTS"
```

### Gate 3 — dry-run

```bash
node scripts/import-page.js "$PRODUCTS/chatcanvas-en.json" --dry-run
node scripts/import-page.js "$PRODUCTS/brand-kit-en.json" --dry-run
```

审查输出：`_id`、slug、`category`、section 数、是否 **create**（非 replace）。

用户输入 **`import confirmed`** 后再导入。

### Gate 4 — 导入

```bash
node scripts/import-page.js "$PRODUCTS/chatcanvas-en.json" --import
node scripts/import-page.js "$PRODUCTS/brand-kit-en.json" --import
```

`--import` 内部使用 **`--missing`**；已存在同 `_id` 则跳过，不覆盖 Studio 手改内容。

### Gate 5 — GROQ 验证

```groq
*[_type == "compositePage" && category == "product" && slug.current in ["chatcanvas", "brand-kit"]]{
  _id, language, title, storyline, "sections": count(string::split(bodyJson, "\"type\"")) - 1, "noIndex": seo.noIndex
}
```

### Gate 6 — Studio 抽查

https://lovart.sanity.studio → Content → Products → 检查 Hero / Tab / pricing / FAQ 渲染字段。

---

## 5. 起步案例（英文 SSOT）

| 文件 | 故事线 | 主维度 | section 数 |
|------|--------|--------|------------|
| `chatcanvas-en.json` | `product-标准` | 产品能力 | 12 |
| `brand-kit-en.json` | `product-含社会证明` | 产品特色 | 13 |

重新生成本地 JSON：

```bash
node "1-3 Content Gen/Page Gen/Pages/Products/en/_build-examples.js"
```

---

## 6. 与 Features / Tools 的差异

| 维度 | Product | Features | Tools |
|------|---------|----------|-------|
| 导入方式 | **`import-page.js`**（composite-v2 直写） | `convert-features.js` 或 `import-page.js` | `convert-tools.js` |
| 故事线 | `product-标准` 等 4 条 | `features-*` | `tools-*` |
| 禁用模块 | `prompt-launcher`、页内 CTA、`canvas-wall` | — | 证言/定价（多数） |
| Step 0 | **PAGE-BRIEF** 五问 | 同 | 同 |

---

## 7. 更新已存在文档

线上已有同 `_id` 且需改 `bodyJson`：

1. **首选**：Studio 手改（安全）
2. **批量 patch**：`patch-composite-bodyjson-batch.js` + manifest（须用户授权，勿默认 `--replace`）
3. **`--replace`**：仅用户明确授权 + 先 `dataset export` 备份

---

## 8. 相关文档

| 文档 | 用途 |
|------|------|
| [PAGE-BRIEF.md](../../../../1-3 Content Gen/Page Gen/Refresh-Page/PAGE-BRIEF.md) | Step 0 立场 |
| [PRODUCT-PRODUCTION.md](../../../../1-3 Content Gen/Page Gen/Refresh-Page/PRODUCT-PRODUCTION.md) | 选型 + 案例 |
| [STORYLINE-BY-DIRECTION.md](../../../../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINE-BY-DIRECTION.md) §4.3 | 故事线 SSOT |
