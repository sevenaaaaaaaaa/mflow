---
name: lovart-sanity-content-publish
description: Support-only Sanity 发布路由索引。请优先使用 lovart-sanity-publish 父入口。
disable-model-invocation: true
---

# Lovart Sanity 内容发布总指南

> Support-only：本 skill 只作为 `lovart-sanity-publish` 的内部路由索引，不直接响应用户发布请求。

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-sanity-content-publish/SKILL.md` |

> **三条管道的唯一入口索引**。各管道均有独立统合指南（SSOT），本文不重复细节，只做路由与全局规则汇总。  
> **本文件位置**：`1-Project/1-1 Harness/Skills/lovart-sanity-content-publish/`（与 `SKILL.md` 同目录）。镜像副本：`1-4 Dev/lovart.sanity.studio/SOP-Lovart-Sanity-内容发布总指南.md`。

---

## 1. 选哪条管道？

| 你要发布的内容          | 本地路径                           | Sanity 类型       | 统合指南（SSOT）                                                                                                       | Skill                                                                   |
| ---------------- | ------------------------------ | --------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Blog 博客**      | `Sanity Blog/**/*.md`          | `blog`          | [`Sanity-Blog-发布统合指南.md`](../lovart-sanity-publish/Sanity-Blog-发布统合指南.md)                                        | [`lovart-sanity-publish/`](../lovart-sanity-publish/)                   |
| **Features 功能页** | `Pages/Features/{lang}/*.json` | `compositePage` | [`SOP-Lovart-Features-Sanity-发布统合指南.md`](../lovart-features-sanity-publish/SOP-Lovart-Features-Sanity-发布统合指南.md) | [`lovart-features-sanity-publish/`](../lovart-features-sanity-publish/) |
| **Tools 工具页**    | `1-3 Content Gen/Page Gen/Pages/Tools/{lang}/*.json`（**composite-v2 only**） | `compositePage` | [`SOP-Lovart-Tools-Sanity-发布统合指南.md`](../lovart-tools-sanity-publish/SOP-Lovart-Tools-Sanity-发布统合指南.md)          | [`lovart-tools-sanity-publish/`](../lovart-tools-sanity-publish/)       |

**线上地址**

| 类型 | URL 模式 |
|------|----------|
| Blog | `https://www.lovart.ai/{lang}/blog/{slug}` |
| Features | `https://www.lovart.ai/{lang}/features/{slug}` |
| Tools | `https://www.lovart.ai/{lang}/tools/{slug}` |

---

## 2. 架构一览

```
                    ┌─────────────────────────────────┐
                    │  Lovart Sanity 内容发布          │
                    │  project: o11tm2qe              │
                    │  dataset: production            │
                    │  Studio: lovart.sanity.studio   │
                    └───────────────┬─────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
   │ 管道 A      │          │ 管道 B      │          │ 管道 C      │
   │ Blog        │          │ Features    │          │ Tools       │
   │ .md         │          │ .json       │          │ .json       │
   └──────┬──────┘          └──────┬──────┘          └──────┬──────┘
          │                        │                        │
   convert.js              convert-features.js       convert-tools.js
   import.ndjson           import-features.ndjson    import-tools.ndjson
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   ▼
              npx sanity dataset import … --dataset production --missing
```

**心智模型**：全部是 **内容同步**，不是 **Studio / schema 部署**。

---

## 3. 全局安全红线

来源：[`lovart-sanity-content-pipeline.mdc`](../../../1-4%20Geo%20Dev/.cursor/rules/lovart-sanity-content-pipeline.mdc)

| ❌ 禁止 | ✅ 允许 |
|--------|--------|
| `npx sanity deploy` | 本地内容文件 → convert → `import --missing` |
| 改 `schemaTypes/`、`sanity.config.ts` | GROQ 验证 + Studio 抽查 |
| `--replace` 导入（除非用户明确授权） | Blog 导入后 `fix-category-refs.js` |
| 删除 production 文档 | Features/Tools 单篇 `import-page.js` |
| 改 `.env` 的 projectId / dataset | |
| **默认全量** convert 全库 + 逐批 import 已上线内容 | **仅增量**（见 §3.1） |

### 3.1 首次运行 vs 日常增量（Agent 必守）

**一页速查**：[`Sanity-Blog-最小交接包.md`](../lovart-sanity-publish/references/Sanity-Blog-最小交接包.md)  
**换设备完整版**：[`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](../lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)  
**策略 SSOT**：[`first-run-and-incremental-policy.md`](../lovart-sanity-publish/references/first-run-and-incremental-policy.md)  
**P1**：[`sanity-es-language-policy.md`](../lovart-sanity-publish/references/sanity-es-language-policy.md) · [`sanity-frontend-apps-lovart.md`](../lovart-sanity-publish/references/sanity-frontend-apps-lovart.md)  
**GROQ**：[`groq-snippets-sanity-blog-features-tools.md`](../lovart-sanity-publish/references/groq-snippets-sanity-blog-features-tools.md)

| 阶段 | 要求 |
|------|------|
| **首次** | `check-publish-deps` → login → `.env` → sync-blog-taxonomy（Blog）→ dry-run 试跑 |
| **日常** | 只处理**本地新增或明确变更**；`import --missing` only |
| **已有** | 本地 + 线上同 `_id` → **不**全量重发 |
| **全量** | 仅用户**明确要求** |

### 3.2 双 Studio 目录（勿 deploy 错）

| 目录 | 用途 |
|------|------|
| `1-4 Dev/lovart.sanity.studio/` | 当前唯一 Studio 工程；Blog/Features/Tools **convert·import** 脚本也在此运行 |
| 历史 `sanity-studio/` | 旧 SOP 中的内容运营目录名；当前按 legacy 处理，执行前必须映射到上一行 |

内容 Agent **禁止**执行 `sanity deploy`（除非 schema 团队授权）。

---

## 4. 环境与公共前置

```bash
cd "…/1-4 Dev/lovart.sanity.studio"

node scripts/check-publish-deps.js
# 可选：export PROJECT_ROOT="/你的路径/1-Project"
# 旧脚本兼容：如单独覆盖内容根，可 export LOVART_ROOT="/你的路径/1-Project/1-3 Content Gen"

grep -E "SANITY_STUDIO_PROJECT|SANITY_STUDIO_DATASET" .env
# o11tm2qe / production

npx sanity debug --secrets
# 已登录的 Sanity 账号

git status
# 无 schema / config 误改

# 发布前质量门禁（三条管道通用）
node scripts/preflight-content.js --type features|tools|blog-md
# 详见 Skills/lovart-content-quality-gates/SKILL.md
```

---

## 4.5 发布前质量门禁（Quality Gates）

**Skill SSOT**：[`lovart-content-quality-gates/`](../lovart-content-quality-gates/SKILL.md)  
**脚本**：`1-4 Dev/lovart.sanity.studio/scripts/preflight-content.js`

| 阶段 | 命令 |
|------|------|
| 本地 JSON/MD 写完 | `--type features\|tools\|blog-md` |
| convert 后、import 前 | `--ndjson ~/lovart/import-*.ndjson` |
| import 后抽查 | Features/Tools：`verify-composite.js --sample 20`；Blog：`verify-blog-publish.js` |
| CI / 汇总报告 | `--report ../../Output/Quality Reports/YYYY-MM-DD/preflight.json` |

**决策**：`BLOCK > 0` → **停止 import**；仅 `WARN` → 人工确认后可继续（`--strict` 时 WARN 也算失败）。

### slug 命名规范（Features / Tools / Blog 通用）

| 规则 | 说明 | preflight 代码 |
|------|------|----------------|
| **kebab-case** | 小写 + 连字符，如 `restaurant-menu-design` | `SEO_SLUG` **BLOCK** |
| **禁止** | 下划线 `_`、空格、首尾 `/` | 同上 |
| **文件名** | `{slug}-{lang}.json` 与 JSON 内 `slug` 一致 | `I18N_FILENAME` WARN |
| **多语言** | 各语言 **同一 slug**，不同 `_id`（`{id}-{lang}`） | `I18N_GAP` / duplicate _id |

### Legacy slug 与重复页（2026-05-29 案例）

**现象**：preflight 报 `SEO_SLUG invalid slug: restaurant_menu_design`，且同主题存在两篇：

| slug | `_id` | 处置 |
|------|-------|------|
| `restaurant-menu-design` | 163 | ✅ **保留**（canonical） |
| `restaurant_menu_design` | 81 | ❌ **删除本地 JSON + `_index` 条目**（legacy 重复） |

**线上注意**（GSC 仍有 `/features/restaurant_menu_design` 流量）：

1. **不要**把 legacy slug 简单改成 kebab 而留两篇并存 — 先确认 `_index` 无重复 slug。
2. 本地清理后，production 上 `81-{lang}` 文档**勿直接删**（红线）；由前端/运维配置 **301** → `/features/restaurant-menu-design`（各语言路径同理）。
3. 重新生成 sitemap（`lovart-sitemap-update`）后再 ping 搜索引擎。
4. 新建页 **禁止** 下划线 slug；从 admin 导出的历史数据导入前先跑 preflight。

```bash
# 排查本地是否还有非法 slug
rg '"slug": "[^"]*_[^"]*"' "../Pages/Features" "../1-3 Content Gen/Page Gen/Pages/Tools"
node scripts/preflight-content.js --type features --lang en
```

---

## 5. 各管道一键命令

### Blog

```bash
node convert.js
npx sanity dataset import import.ndjson --dataset production --missing
npx sanity exec fix-category-refs.js --with-user-token
```

### Features

```bash
# 单篇
node scripts/import-page.js "../Pages/Features/en/{slug}-en.json" --import

# 批量
node scripts/convert-features.js --dry-run
node scripts/convert-features.js
npx sanity dataset import ~/lovart/import-features.ndjson --dataset production --missing
```

### Tools（composite-v2 · 正式源已启用）

正式源：`1-3 Content Gen/Page Gen/Pages/Tools/`（线上 526/528 已 v2）。换设备：`sync-tools-from-production.js`。

```bash
node scripts/export-composite-production.js
node scripts/sync-tools-from-production.js
node scripts/preflight-content.js --type tools --strict
node scripts/convert-tools.js --lang en --dry-run
npx sanity dataset import ~/lovart/import-tools.ndjson --dataset production --missing
```

---

## 6. compositePage 说明（六类落地页）

与 [`1-4 Dev/lovart.sanity.studio/SOP-Lovart-Sanity-内容发布总指南.md`](../../1-4 Dev/lovart.sanity.studio/SOP-Lovart-Sanity-内容发布总指南.md) **§7–§7.5** 同步（Studio 按 **`category`** 导航；`verify-composite.js`；Presentation 已知限制）。

---

## 7. 内容生产管线（Pipeline）

```
lovart-data-ingestion → lovart-content-calendar → lovart-landing-page
  ├─ sanity-blog    → 管道 A
  ├─ feature-page   → 管道 B
  └─ tool-page      → 管道 C
→ lovart-content-audit → 【本指南各管道 import】→ lovart-sitemap-update
```

编排 Skill：[`lovart-pipeline-orchestrator/SKILL.md`](../lovart-pipeline-orchestrator/SKILL.md)

---

## 8. 文档层级（避免重复阅读）

| 层级 | 文件 | 读什么 |
|------|------|--------|
| **L0 总索引** | 本文 | 选管道、全局规则 |
| **L1 管道 SSOT** | Features / Tools / Blog 统合指南 | 执行发布时的唯一详细文档 |
| **L2 简版 / 历史** | [`SOP-PageJSON导入指南.md`](../../1-4 Dev/lovart.sanity.studio/SOP-PageJSON导入指南.md) | 已并入 L1，仅作跳转 |
| **L3 Agent** | 各 `SKILL.md` | 触发词 + 快速门禁 |
| **L4 规则** | `lovart-sanity-content-pipeline.mdc` | Cursor 自动约束 |

---

## 9. 触发词路由

| 用户说法 | 读哪份 |
|----------|--------|
| 发布博客 / Sanity blog / convert.js | Blog 统合 / `lovart-sanity-publish` |
| 发布功能页 / Features / import features | [`lovart-features-sanity-publish`](../lovart-features-sanity-publish/) |
| 发布工具页 / Tools / import tools | [`lovart-tools-sanity-publish`](../lovart-tools-sanity-publish/) |
| 不确定发哪种 | **本文 §1** |

---

## 10. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-29 | 初版：统合 Blog / Features / Tools 三条管道索引 |
| 2026-06-06 | Tools 正式源 Page Gen/Pages/Tools；线上 v2 确认；弃用 pages-legacy；新增 sync-tools-from-production |
| 2026-05-29 | 迁入 `Skills/lovart-sanity-content-publish/` |
| 2026-05-29 | §4.5 质量门禁 + slug 规范；清理 legacy `restaurant_menu_design` 重复页 |
| 2026-05-29 | §3.1–§3.2 换设备 SOP + 双 Studio；`check-publish-deps`；`LOVART_ROOT` |
| 2026-06-05 | §11 Anti-Bugs：三条管道共用 B7 原则 |

---

## 11. Anti-Bugs（三条管道共用）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md) · [AGENTS.md Part B7](../../../1-1%20GEO%20Readme/AGENTS.md)

| 原则 | 管道 A Blog | 管道 B Features | 管道 C Tools |
|------|-------------|-----------------|--------------|
| 增量 `--missing` | AB-P02 | AB-P02 | AB-P02 |
| 线上 patch 差量 | fix-category-refs | patch-composite-seo-urls | patch-composite-images-404 |
| 发布前 auth | AB-E03 | AB-E03 | AB-E03 |
| 图片 404 仅修坏链 | AB-I04 | AB-I05 | AB-I05 |
| 禁止全量无授权 | AB-A01, AB-A03 | 同左 | 同左 |

各管道细节见对应 Skill 的 `Anti-Bugs` 小节；破坏面矩阵见 Registry **附录 B**。


## 预算（RULES-70 强制）

本 skill 产出受 RULES-70 数量预算约束（字数/H2/FAQ/数据点/来源）。
