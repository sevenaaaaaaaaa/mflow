---
name: lovart-tools-sanity-publish
description: Publish Lovart Tools composite-v2 JSON (Page Gen/Pages/Tools) to Sanity production. Pull from production via pull-tools-from-production (project script or node). Use for "同步 Tools"、"发布工具页"、"import tools to Sanity"、"pull tools".
disable-model-invocation: true
---

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-tools-sanity-publish/SKILL.md` |

# Lovart Tools → Sanity Publish

> Support-only：本 skill 只作为 `lovart-sanity-publish` 的内部 Tools 执行管道，不直接响应用户发布请求。用户提到发布/同步/import Tools 时，先进入 `lovart-sanity-publish` 父入口。

**换设备 / 首次运行（Sanity Blog·Features·Tools）**：[`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](../lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)

**Canonical doc（必读，与本 Skill 同目录）**：

`SOP-Lovart-Tools-Sanity-发布统合指南.md`

**Scripts**：

| 场景 | 命令 |
|------|------|
| 线上→本地 | `bash "1-4 Dev/automation/tools-pull/pull-tools-from-production.sh"` 或 `node scripts/pull-tools-from-production.js` |
| 批量 | `node scripts/convert-tools.js`（→ `feature-to-composite-page.js`） |
| 单篇 | `node scripts/import-page.js "../1-3 Content Gen/Page Gen/Pages/Tools/{lang}/{slug}-{lang}.json" --import` |
| 补翻译 | `python3 scripts/translate-tools.py`（读 `import-tools-report.json`） |
| 导入后校验 | `npx sanity exec scripts/verify-composite.js --with-user-token -- --type tools --sample 20` |

**正式源**：`1-3 Content Gen/Page Gen/Pages/Tools/`（线上 528/528 v2）。对齐：**pull-tools-from-production**（见 `1-4 Dev/automation/tools-pull/README.md`）。`pages-legacy/Tools/` **已弃用**。

单篇 `_id`：JSON 内 `id` 或 `Pages/Tools/_index.json`；否则回退 `tools-{slug}-{lang}`（可能冲突）。

## Triggers

- 「同步 Tools 到 Sanity」/「发布工具页」/「import tools」
- Pipeline 中 `tool-page` 产出 JSON 后的发布步骤

## Do NOT use for

- Blog Markdown → [`lovart-sanity-publish`](../lovart-sanity-publish/SKILL.md) + `convert.js`
- Features 页 → `scripts/convert-features.js`
- Studio 部署 → 永不 `npx sanity deploy`

## Quick workflow

1. **首次**：`check-publish-deps` → login → `convert-tools --dry-run`；勿无范围全量 import  
2. **日常**：仅新增/变更 JSON → `import-page` 或限定范围 convert → **`import --missing`**  
3. **质量门禁**：[`lovart-content-quality-gates`](../lovart-content-quality-gates/SKILL.md) → `preflight-content.js --type tools --strict`  
4. 用户确认后 import；Studio：**Content → Tools**（`category == "tool"`）

## Safety (summary)

- ❌ 默认全量 convert + 全量 import 已上线内容 / `sanity deploy` / `--replace`
- ✅ 首次拉线上参照（dry-run report）· 日常 `--missing` only
- ✅ **`category: "tool"`** + `_id: "{id}-{lang}"`；`sourceType: "tools"` 为 legacy 可选

## Anti-Bugs（禁止再犯）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md)

| ID | 本 Skill 门禁 |
|----|--------------|
| AB-S04 | 跳过 `draft-*`；`page-publish-skip.js` 与 preflight 一致 |
| AB-U04 | 文件名 `{slug}-{lang}.json` 无空格；曾用 `fix-tools-filename-spaces.js` |
| AB-I05 | composite 图 404：`audit-composite-images-404.js` → `patch-composite-images-404.js` |
| AB-I02 | 替换图禁止 `bg-line.png` 等装饰 URL；须 `assets-persist` 或同页 sibling |
| AB-P02 | 日常 `--missing` only；pull 对齐后仅 push 变更 JSON |
| AB-A01 | import 前 `--ndjson` preflight + dry-run convert |


## 预算（RULES-70 强制）

本 skill 产出受 RULES-70 数量预算约束（字数/H2/FAQ/数据点/来源）。
