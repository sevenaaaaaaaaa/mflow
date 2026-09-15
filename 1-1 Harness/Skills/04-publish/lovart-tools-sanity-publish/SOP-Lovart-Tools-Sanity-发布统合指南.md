# Lovart Tools → Sanity 发布统合指南

> **单一事实来源（SSOT）**：本地 Tools 页面 JSON 同步到 Sanity `production` 的完整流程、安全规则、脚本与排障。  
> 统合自：`SOP-PageJSON导入指南.md`、`lovart-sanity-publish`、`lovart-sanity-content-pipeline.mdc`、`lovart-landing-page`、`convert-features.js` 及线上实践经验。  
> **本文件位置**：`1-Project/1-1 Harness/Skills/lovart-tools-sanity-publish/`（与 `SKILL.md` 同目录）。镜像副本：`1-4 Dev/lovart.sanity.studio/SOP-Lovart-Tools-Sanity-发布统合指南.md`。

---

## 1. 文档地图

| 用途 | 文件 | 关系 |
|------|------|------|
| **三条管道总索引** | `1-4 Dev/lovart.sanity.studio/SOP-Lovart-Sanity-内容发布总指南.md` | Blog / Features / Tools 入口 |
| **本指南（Tools 主文档）** | `Skills/lovart-tools-sanity-publish/SOP-Lovart-Tools-Sanity-发布统合指南.md` | 执行 Tools 发布时只读这一份 |
| **Features 兄弟管道** | `Skills/lovart-features-sanity-publish/SOP-Lovart-Features-Sanity-发布统合指南.md` | 功能页专用 |
| Agent Skill | `Skills/lovart-tools-sanity-publish/SKILL.md` | 触发词 + 门禁，与本指南同目录 |
| 镜像副本 | `1-4 Dev/lovart.sanity.studio/SOP-Lovart-Tools-Sanity-发布统合指南.md` | 与 skills 版内容同步 |
| 批量转换 | `1-4 Dev/lovart.sanity.studio/scripts/convert-tools.js` | 薄封装 → `lib/feature-to-composite-page.js` |
| 单篇导入 | `1-4 Dev/lovart.sanity.studio/scripts/import-page.js` | Tools/Features 自动识别路径 + `_index.json` |
| 共享转换库 | `scripts/lib/feature-to-composite-page.js` | bodyJson + section 双格式 |
| Features 转换 | `scripts/convert-features.js` | 同库，勿混用目录 |
| Blog 发布（另一条管道） | `Skills/lovart-sanity-publish/` | **不要**对 Tools 跑 `convert.js` |
| 页面 JSON 简版 SOP | `1-4 Dev/lovart.sanity.studio/SOP-PageJSON导入指南.md` | 已并入本指南 §4–§8 |
| 内容管道红线 | `1-4 Dev/.cursor/rules/lovart-sanity-content-pipeline.mdc` | 全局安全规则 |
| Blog 同步 SOP | `1-4 Dev/lovart.sanity.studio/SOP-Sanity同步指南.md` | 仅 Markdown → `blog` |
| 生成 Tools JSON | `Skills/02-creation/lovart-landing-page/SKILL.md` | Step 3 `tool-page` |
| Studio 结构说明 | `1-4 Dev/lovart.sanity.studio/AGENTS.md` | schema、desk、GROQ |

---

## 2. 心智模型与双 Studio 目录

### 2.1 两条内容管道

```
管道 A — Blog     Sanity Blog/**/*.md → convert.js → _type: blog
管道 B — Tools    Page Gen/Pages/Tools/*.json (composite-v2) → convert-tools.js → compositePage
```

**2026-05-29**：线上 **528/528** Tools 均为 composite-v2（6 篇 `draft-*` 仅 noIndex）。**正式源**：`Page Gen/Pages/Tools/`（编辑区）；**真相源**：production。**定期** `export-composite-production` → `sync-tools-from-production` 把线上拉回本地，避免迁移漂移。`pages-legacy/Tools/` **已弃用**。

**关键结论**：这是 **内容同步**（`dataset import --missing`），不是 **`sanity deploy`**。

### 2.2 当前 Studio 工程与 legacy 目录名（勿混淆）

| 目录 | 用途 | 注意 |
|------|------|------|
| **`1-4 Dev/lovart.sanity.studio`** | 当前唯一 Studio 工程；schema、convert、import 脚本都在此 | **Content → Tools**（`category == "tool"`） |
| 历史 `sanity-studio/` | 旧 SOP 中的内容运营目录名 | 当前按 legacy 处理，执行命令时映射到上一行 |

- **线上导航与 Presentation 预览**：只认 **`category: "tool"`**，不认 `sourceType`。
- **`sourceType: "tools"`**：导入脚本写入的 **legacy 数据集字段**，便于旧 desk / GROQ 排查；**不是** schema 字段，新 Studio 可忽略。
- **我们日常 cwd**：`1-4 Dev/lovart.sanity.studio/`（跑 convert / import）；未经授权**不要**改 `schemaTypes/` 或执行 `sanity deploy`。

### 2.3 Tools 字段速查（composite-v2）

| 项 | Tools |
|----|-------|
| **正式源路径** | `1-3 Content Gen/Page Gen/Pages/Tools/{lang}/{slug}-{lang}.json` |
| 故事线 SSOT | `1-3 Content Gen/Page Gen/Refresh-Page/STORYLINES.md`（T1–T5、N5） |
| 线上 → 本地 | **`pull-tools-from-production.sh`** 或 `node scripts/pull-tools-from-production.js`（**发布后 + 每周**） |
| draft 测试页 | 6 篇 `en` `draft-*`（noIndex）；sync 默认跳过，见 `DRAFT-TOOLS-PRODUCTION.md` |
| 索引 | `Pages/Tools/_index.json`（`id` + slug + language，迁移期保留现网 _id） |
| **schemaVersion** | **`composite-v2`**（必填） |
| **storylineTemplate** | **`T1`–`T5`、`N5` 或 `T-long`**（必填；`T-long` = 线上 12+ section reflow） |
| 线上 URL | 见总指南 compositePage URL 表（`/tools/` 或 `/en/tools/`） |
| Sanity `_type` | `compositePage` |
| **`category`** | **`tool`**（Studio / 前端 / GROQ 主键） |
| `sourceType` | `tools`（数据集 legacy 字段，导入脚本写入） |
| `_id` | `{id}-{lang}`（`id` 来自 JSON 或 `_index.json`） |
| Studio | https://lovart.sanity.studio → **Content → Tools** |
| Project / Dataset | `o11tm2qe` / `production` |

### 2.4 单篇导入 `import-page.js`

```bash
node scripts/import-page.js "../1-3 Content Gen/Page Gen/Pages/Tools/en/{slug}-en.json" --dry-run
node scripts/import-page.js "../1-3 Content Gen/Page Gen/Pages/Tools/en/{slug}-en.json" --import
```

**`_id` 要求**（满足其一即可）：

1. JSON 内 `"id": 292`（推荐）
2. `Pages/Tools/_index.json` 中存在对应 `slug` + `language` 的 `id`
3. 否则回退 `tools-{slug}-{lang}`，**可能与已有数字 _id 冲突**，`--missing` 会跳过

脚本根据路径自动加载 **Tools** 的 `_index.json`（不再误用 Features 索引）。

---

## 3. 安全红线（不可协商）

来源：`lovart-sanity-content-pipeline.mdc` + `lovart-sanity-publish` Incident 表。

| 规则 | 违反时 |
|------|--------|
| ❌ 不运行 `npx sanity deploy` | 拒绝 |
| ❌ 不改 `schemaTypes/`、`sanity.config.ts`、`sanity.cli.ts`、`components/` | 拒绝 |
| ❌ 不用 `--replace` 导入 | 只用 `--missing` |
| ❌ 不删 production 文档 | 拒绝 |
| ❌ 不改 `.env` 的 projectId / dataset | 拒绝 |
| ✅ Tools：`convert-tools.js` → `import --missing` | 允许 |
| ✅ Blog 才用 `fix-category-refs.js` | Tools 一般不需要 |

**所有权边界**

```
前端维护 → sanity.config.ts / schemaTypes/ / components/
我们操作 → Page Gen/Pages/Tools/*.json (v2) → convert-tools.js → import --missing
```

---

## 4. 端到端流程（含门禁）

### Gate 0 — 环境 + 首次运行

> **策略 SSOT**：[`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](../lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)

**首次 / 换设备**：`sanity login` → `check-sanity-auth` → `export-composite-production.js` → `sync-tools-from-production.js` → `convert-tools.js --dry-run`。  
**日常 push**：改正式源 JSON → preflight → convert → **`import --missing`**；已有 `_id` 勿全量重发。  
**日常 pull（防漂移）**：`bash "1-4 Dev/automation/tools-pull/pull-tools-from-production.sh"` — 每次 Tools import 成功后，或每周/Sprint 初；有本地未提交编辑时先提交或备份再 pull。

```bash
cd "…/1-4 Dev/lovart.sanity.studio"
grep -E "SANITY_STUDIO_PROJECT|SANITY_STUDIO_DATASET" .env
# 期望：o11tm2qe / production

npx sanity debug --secrets
# 已登录 sevena@lovart.ai
```

### Gate 1 — 确认本地 JSON（composite-v2）

- [ ] 文件在 `1-3 Content Gen/Page Gen/Pages/Tools/{lang}/`，命名 `{slug}-{lang}.json`
- [ ] 必填：`schemaVersion: "composite-v2"`、`storylineTemplate`（T1–T5 / N5）、`slug`、`language`、`title`、`bodyJson`
- [ ] `category` 为 `tool`；图片优先 `media.src` → `https://assets-persist.lovart.ai/`
- [ ] 多语言：**同一 slug**，**不同 `_id`**（`{id}-{lang}`）
- [ ] **非** `draft-*` / `draftStatus: local-only`（定稿后再进正式源）

**Tools v2 section 示例**（见 STORYLINES.md）：  
`prompt-launcher`、`hero-split`、`bento-2`、`workflow-horizontal`、`feature-detail`、`comparison-table`、`testimonial`、`faq`、`cta-default` 等（共 33 种 Refresh-Page type）。

**禁止** legacy：`heroSection`、`contentSection`、`threeColumnSection`、`textImageSection`、`testimonialSection`、`faqSection`。

**Features 对比**（勿混用脚本）：Features 仍用 `convert-features.js` + `Pages/Features/`。

### Gate 1.5 — 质量预检（必跑）

```bash
cd "…/1-4 Dev/lovart.sanity.studio"
node scripts/preflight-content.js --type tools --strict
# 或单篇：--file "../1-3 Content Gen/Page Gen/Pages/Tools/en/{slug}-en.json"
```

Skill：[`lovart-content-quality-gates`](../../lovart-content-quality-gates/SKILL.md)。BLOCK > 0 则不得进入 convert/import。

### Gate 2 — 转换 NDJSON

```bash
cd "…/1-4 Dev/lovart.sanity.studio"

# 预检（不写 NDJSON）
node scripts/convert-tools.js --dry-run

# 查看报告
cat ~/lovart/import-tools-report.json | head -80

# 正式生成
node scripts/convert-tools.js

# 可选：只处理部分语言
node scripts/convert-tools.js --lang en,ja
```

**输出**

| 文件 | 说明 |
|------|------|
| `~/lovart/import-tools.ndjson` | 导入用 |
| `~/lovart/import-tools-report.json` | 条数、重复 _id、marker、缺失语言 |

**导入前检查**

```bash
wc -l ~/lovart/import-tools.ndjson
grep -c 'section_' ~/lovart/import-tools.ndjson   # 期望 0（无翻译 marker 残留）
```

用户明确输入 **`import confirmed`** 后再执行导入（与 Blog 发布协议一致）。

```bash
node scripts/preflight-content.js --ndjson ~/lovart/import-tools.ndjson --strict
```

### Gate 3 — 导入 production

```bash
npx sanity dataset import ~/lovart/import-tools.ndjson --dataset production --missing
```

- `--missing`：仅新增缺失 `_id`，**不覆盖** Studio 内已编辑文档。
- 已存在且需更新：在 Studio 手改，或用户明确授权 patch / `--replace`（极少使用）。

### Gate 4 — 落库校验（推荐随机抽查）

```bash
# 随机抽查 NDJSON 中 20 条是否已写入（秒级；全量去掉 --sample）
npx sanity exec scripts/verify-composite.js --with-user-token -- \
  --ndjson ~/lovart/import-tools.ndjson --sample 20
```

GROQ 手工抽查：

```groq
// 按语言统计
count(*[_type == "compositePage" && sourceType == "tools" && language == "en"])

// 某 slug 多语言是否齐全
*[_type == "compositePage" && category == "tool" && slug.current == "ai-logo-generator"]{
  _id, language, title, _updatedAt
}

// 最近导入
*[_type == "compositePage" && sourceType == "tools"] | order(_updatedAt desc)[0...5]{
  title, "slug": slug.current, language, _id
}
```

### Gate 5 — Studio 抽查

打开 https://lovart.sanity.studio → **Content → Tools**（`category == "tool"`），检查模块、SEO、封面。

### 可选 — 补缺失翻译

`python3 scripts/translate-tools.py`（与 Features 共用 `scripts/lib/translate_composite_missing.py`）。

- 前置：`node scripts/convert-tools.js --dry-run` → `~/lovart/import-tools-report.json`
- 模型：MiniMax-CN（`~/.mavis/config.yaml`）
- **禁止翻译**：`system_prompt`、`suggestion.value`、`type`、`image_url`、`icon_url`
- 剥离 `<think>...</think>`
- 边译边 append NDJSON；断点续传

```bash
npx sanity dataset import ~/lovart/import-tools-missing.ndjson --dataset production --missing
```

---

## 5. 字段映射（本地 JSON → compositePage）

```
本地 JSON                    → Sanity compositePage
────────────────────────────────────────────────────
id（或 _index.json 中的 id）  → _id = "{id}-{lang}"
slug                         → slug.current（各语言相同）
language                     → language
category: "tool"             → category: "tool"
（固定）                     → sourceType: "tools"
title                        → title
description                  → description（≤500 字）
bodyJson 或 section[]        → bodyJson（stringify 后）
seo { ... }                  → seo（原样合并，缺则自动生成）
首张 image_url / 子 section   → cover（imageSource, external）
create_time / releaseDate    → releaseDate
url_path                     → 不写入（schema 无字段）
```

**`_id` 策略（Incident：227 duplicate）**  
同一数字 `id` 不得跨语言共用；必须为 `{id}-{lang}`。

---

## 6. 命令速查

```bash
export STUDIO="…/1-4 Dev/lovart.sanity.studio"
cd "$STUDIO"

# 全流程
node scripts/convert-tools.js --dry-run
node scripts/convert-tools.js
npx sanity dataset import ~/lovart/import-tools.ndjson --dataset production --missing

# Features（非 Tools）
node scripts/convert-features.js
npx sanity dataset import ~/lovart/import-features.ndjson --dataset production --missing

# Blog（非 Tools）
node convert.js
npx sanity dataset import import.ndjson --dataset production --missing
npx sanity exec fix-category-refs.js --with-user-token
```

---

## 7. 常见坑与修复

| 现象 | 原因 | 修复 |
|------|------|------|
| Studio 列表为空 | 缺 `sourceType: "tools"` | `convert-tools.js` 已写入；旧数据需 patch |
| duplicate `_id` | 跨语言共用 id | `{id}-{lang}` |
| `section_de` 出现在正文 | 翻译 marker 未清 | `deepCleanMarkers()`；`grep section_` 为 0 |
| import 全跳过 | `_id` 已存在 | 正常（`--missing`）；要更新请 Studio 编辑 |
| import 失败 | 字段与线上 schema 不一致 | `npx sanity schema fetch`；联系前端同步 schema |
| `convert-features` 对 Tools 无效 | 读 `section` 而非 `bodyJson` | 必须用 `convert-tools.js` |
| 封面缺失 | 图在 `contentSection.sections[]` | `extractCover` 已递归子 section |
| 与 Blog 混跑 | 误用 `convert.js` | Tools 只走本指南管道 |

---

## 8. 与内容生产管线的关系

```
lovart-content-calendar → lovart-landing-page (tool-page)
       → Pages/Tools/{lang}/*.json
       → lovart-content-audit
       → 【本指南】convert-tools.js → import --missing
       → lovart-multi-platform-push（Sanity 部分偏 Blog，Tools 以本指南为准）
```

---

## 9. Agent / 人工触发词

| 说法 | 动作 |
|------|------|
| 「同步 Tools 到 Sanity」「发布工具页」「import tools」 | 读本指南 + `lovart-tools-sanity-publish` Skill |
| 「Sanity push」「发布博客」 | 走 `lovart-sanity-publish`（管道 A） |
| `preflight` / `import confirmed` / `cancel` | Blog 发布门禁；Tools 建议同样人工确认后再 import |

---

## 10. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-29 | 初版统合；新增 `convert-tools.js` |
| 2026-05-29 | 复制至 `Skills/lovart-tools-sanity-publish/` |
| 2026-05-29 | Gate 0 首次认证+拉线上参照 vs 日常增量 |
