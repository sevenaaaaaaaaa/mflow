# Refresh-Page 适用范围

> 修订：2026-05-29

## 哪些内容用新组件（33 种 `type`）

| Sanity 类型 | 是否用 Refresh-Page |
|-------------|---------------------|
| `blog` | **否** — Markdown + `convert.js` |
| `news` | **否** |
| `docs` | **否** |
| `compositePage`（全部 `category`） | **是** |

### compositePage 六类（Studio 按 `category` 分栏）

| `category` | 公开 URL 段 | 本地 JSON（现状） |
|------------|-------------|-------------------|
| `feature` | `/features/` | `Pages/Features/` |
| `tool` | `/tools/` | `Pages/Tools/` |
| `product` | `/product/` | `Pages/Products/`（英文 2 篇参考案例，见 [PRODUCT-PRODUCTION.md](./PRODUCT-PRODUCTION.md)） |
| `solution` | `/solution/` | 待建 |
| `scenario` | `/scenario/` | 待建 |
| `topic` | `/topic/` | 待建 |

**规则：** 新写的 Products / Solutions / Scenarios / Topics 与迁移后的 Features / Tools 共用同一套 `bodyJson` 扁平格式（见 `README.md`）。`sourceType` 为 legacy 字段，导入时可有可无；**`category` 必须正确**。

## 相关文档

| 文件 | 内容 |
|------|------|
| [README.md](./README.md) | 33 种组件字段字典 |
| [STORYLINES.md](./STORYLINES.md) | 情景 × 组件组合菜谱 |
| [LEGACY-MIGRATION.md](./LEGACY-MIGRATION.md) | 旧版映射、改什么、怎么实现 |
| [preview-data.json](./preview-data.json) | 每种新组件一条完整示例 |

## 迁移脚本（骨架）

| 路径 | 说明 |
|------|------|
| `sanity-studio/scripts/lib/legacy-to-composite.js` | 单条 section 映射逻辑 |
| `sanity-studio/scripts/migrate-legacy-bodyjson.js` | CLI：批量 dry-run / 写 `-v2` 文件 |
| `sanity-studio/scripts/generate-composite-v2-drafts.js` | 本地 A/B 故事线草稿批量生成 |

## 本地 A/B 草稿（未同步 Sanity）

| 路径 | 说明 |
|------|------|
| `Pages/drafts/composite-v2/` | 故事线变体 JSON + `MANIFEST.md` |
| 预检 | `preflight-content.js --type composite-v2 --dir "../Pages/drafts/composite-v2/Features/en"` |
