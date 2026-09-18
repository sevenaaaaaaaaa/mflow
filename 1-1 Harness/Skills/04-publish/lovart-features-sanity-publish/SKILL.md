---
name: lovart-features-sanity-publish
description: Publish local Lovart Features page JSON (Pages/Features) to Sanity production as compositePage. Safe incremental import only. Use for "同步 Features"、"发布功能页"、"import features to Sanity".
disable-model-invocation: true
---

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-features-sanity-publish/SKILL.md` |

# Lovart Features → Sanity Publish

> Support-only：本 skill 只作为 `lovart-sanity-publish` 的内部 Features 执行管道，不直接响应用户发布请求。用户提到发布/同步/import Features 时，先进入 `lovart-sanity-publish` 父入口。

**换设备 / 首次运行（Sanity Blog·Features·Tools）**：[`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](../lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)

**Canonical doc（必读，与本 Skill 同目录）**：

`SOP-Lovart-Features-Sanity-发布统合指南.md`

**Scripts**：

| 场景 | 脚本 |
|------|------|
| 单篇 | `1-4 Dev/lovart.sanity.studio/scripts/import-page.js` |
| 批量 | `1-4 Dev/lovart.sanity.studio/scripts/convert-features.js` |
| 翻译补全 | `1-4 Dev/lovart.sanity.studio/scripts/translate-features.py` |
| 导入后校验 | `npx sanity exec scripts/verify-composite.js --with-user-token -- --type features --sample 20` |
| 共享库 | `scripts/lib/feature-to-composite-page.js` |

## Triggers

- 「同步 Features 到 Sanity」/「发布功能页」/「import features」
- Pipeline 中 `feature-page` 产出 JSON 后的发布步骤

## Do NOT use for

- Blog Markdown → `SOP-Sanity同步指南.md` + `convert.js`
- Tools 页 → `Skills/lovart-tools-sanity-publish/` + `convert-tools.js`
- Studio 部署 → 永不 `npx sanity deploy`

## Quick workflow

1. **首次**：`check-publish-deps` → login → `convert-features --dry-run`（本地缺口报告）；勿无范围全量 import  
2. **日常**：仅新增/变更 JSON → convert / `import-page` → **`import --missing`**  
3. `cd "1-4 Dev/lovart.sanity.studio"` — `node scripts/check-sanity-auth.js`  
4. **质量门禁**：[`lovart-content-quality-gates`](../lovart-content-quality-gates/SKILL.md) → `preflight-content.js --type features`（可选 `--sample-urls 8`）  
5. **单篇**：`node scripts/import-page.js "../1-3 Content Gen/Page Gen/Pages/Features/en/{slug}-en.json" --dry-run`  
6. **批量**：`node scripts/convert-features.js --dry-run` — 读 `~/lovart/import-features-report.json`  
7. 用户确认后：convert / `import-page.js --import`  
8. **import 前**：`node scripts/preflight-content.js --ndjson ~/lovart/import-features.ndjson --strict`  
9. `npx sanity dataset import ~/lovart/import-features.ndjson --dataset production --missing`  
10. GROQ 验证 + Studio **Content → Features**（`category == "feature"`，见统合指南）

## Safety (summary)

- ❌ `sanity deploy` / `--replace` / 改 schema / 删文档
- ✅ `--missing` only
- ✅ `sourceType: "features"`, `category: "feature"`, `_id: "{id}-{lang}"`

## Anti-Bugs（禁止再犯）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md)

| ID | 本 Skill 门禁 |
|----|--------------|
| AB-U01 | JSON-LD / `url_path` 须 `lovart.ai/features/`；本地 convert 自动修，**线上**须 `patch-composite-seo-urls-env.js` |
| AB-P03 | 已发布文档不因 re-convert 自动变；差量走 patch 分批 `--dry-run` → `--apply` |
| AB-P04 | marker 用 `repair-local-markers.js --writeback`，勿 221 篇手改 |
| AB-S05 | convert 补 `sourceType`；preflight `META_SOURCETYPE` 归零 |
| AB-I05 | 发布后 `audit-composite-images-404.js`；404 用 `patch-composite-images-404.js` |
| AB-A01 | patch / import 必须先 dry-run 或 `--limit` pilot |


## 预算（RULES-70 强制）

本 skill 产出受 RULES-70 数量预算约束（字数/H2/FAQ/数据点/来源）。
