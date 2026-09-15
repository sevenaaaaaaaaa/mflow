# Lovart Features → Sanity 发布统合指南

> **单一事实来源（SSOT）**：本地 Features 页面 JSON 同步到 Sanity `production` 的完整流程、安全规则、脚本与排障。  
> 统合自：`SOP-PageJSON导入指南.md`、`SOP-Sanity同步指南.md`、`lovart-sanity-content-pipeline.mdc`、`lovart-landing-page`、Features Page Generator v2.3.0、`convert-features.js` / `import-page.js` / `translate-features.py` 及线上实践经验。  
> **本文件位置**：`1-Project/1-1 Harness/Skills/lovart-features-sanity-publish/`（与 `SKILL.md` 同目录）。镜像副本：`1-4 Dev/lovart.sanity.studio/SOP-Lovart-Features-Sanity-发布统合指南.md`。

---

## 1. 文档地图

| 用途 | 文件 | 关系 |
|------|------|------|
| **本指南（Features 主文档）** | `Skills/lovart-features-sanity-publish/SOP-Lovart-Features-Sanity-发布统合指南.md` | 执行 Features 发布时只读这一份 |
| Agent Skill | `Skills/lovart-features-sanity-publish/SKILL.md` | 触发词 + 门禁 |
| 镜像副本 | `1-4 Dev/lovart.sanity.studio/SOP-Lovart-Features-Sanity-发布统合指南.md` | 与 skills 版内容同步 |
| **三条管道总索引** | `1-4 Dev/lovart.sanity.studio/SOP-Lovart-Sanity-内容发布总指南.md` | Blog / Features / Tools 入口 |
| 共享转换库 | `scripts/lib/feature-to-composite-page.js` | bodyJson + section 双格式 |
| 批量转换 | `scripts/convert-features.js` | 全量 / 按语言 NDJSON |
| 单篇导入 | `scripts/import-page.js` | 一篇 JSON → NDJSON → 可选 `--import` |
| 缺失翻译 | `scripts/translate-features.py` | en → 8 种语言，输出 missing NDJSON |
| Tools 发布（兄弟管道） | `Skills/lovart-tools-sanity-publish/` | **勿**对 Features 跑 `convert-tools.js` |
| Blog 发布（另一条管道） | `SOP-Sanity同步指南.md` + `convert.js` | **勿**对 Features 跑 `convert.js` |
| 内容管道红线 | `.cursor/rules/lovart-sanity-content-pipeline.mdc` | 全局安全规则 |
| 生成 Features JSON | `Skills/02-creation/lovart-landing-page/SKILL.md` | Step 3 `feature-page` |
| 5 组件架构规范 | `Skills/lovart-blog-automation/references/lovart-skills-and-norms-summary.md` | § Features Page |

---

## 2. 心智模型：三条管道

```
┌──────────────────────────────────────────────────────────────────┐
│ 管道 A — Blog（文章）                                               │
│   Sanity Blog/**/*.md → convert.js → _type: blog                  │
│   文档：SOP-Sanity同步指南.md                                       │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ 管道 B — Features（功能页）← 本指南                                 │
│   Pages/Features/{lang}/*.json → convert-features.js → NDJSON     │
│   _type: compositePage, category: feature, sourceType: features   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ 管道 C — Tools（工具页）                                            │
│   Page Gen/Pages/Tools/{lang}/*.json (v2) → convert-tools.js      │
│   文档：SOP-Lovart-Tools-Sanity-发布统合指南.md                      │
└──────────────────────────────────────────────────────────────────┘
```

**关键结论**

- 三条管道都是 **内容同步**，**不是** `sanity deploy`。
- **Schema 真源**：`1-4 Dev/lovart.sanity.studio/schemaTypes/compositePageType.ts`（已注册 6 类 `category`）。
- **历史 `sanity-studio/`** 是旧 SOP 中的内容运营目录名；当前执行 convert / import 时映射到 `1-4 Dev/lovart.sanity.studio/`。
- **线上 Studio 导航**：**Content → Features**，筛选 `category == "feature"`（**不是** `sourceType`）。
- **`sourceType: "features"`**：legacy 数据集字段，导入时仍可写入，供旧 desk / 历史 GROQ。

### 2.1 当前 Studio 工程与 legacy 目录名

| 目录 | 角色 |
|------|------|
| `1-4 Dev/lovart.sanity.studio/` | 当前唯一 Studio 工程；schema、`convert-features.js`、`import-page.js`、`import --missing` 都在此 |
| 历史 `sanity-studio/` | 旧 SOP 中的内容运营目录名；不作为当前执行 cwd |

| 项 | Features |
|----|----------|
| 本地路径 | `1-3 Content Gen/Page Gen/Pages/Features/{lang}/{slug}-{lang}.json` |
| 索引 | `Pages/Features/_index.json` |
| 线上 URL | 总指南 §7 compositePage URL 表 |
| Sanity `_type` | `compositePage` |
| **`category`** | **`feature`** |
| `sourceType` | `features`（legacy） |
| `_id` | `{id}-{lang}` |
| 支持语言 | `en`, `de`, `fr`, `it`, `ja`, `ko`, `pt`, `ru`, `zh-TW` |
| Project / Dataset | `o11tm2qe` / `production` |
| Studio | **Content → Features** |

---

## 3. 安全红线（不可协商）

来源：`.cursor/rules/lovart-sanity-content-pipeline.mdc`。

| 规则 | 违反时 |
|------|--------|
| ❌ 不运行 `npx sanity deploy` | 拒绝 |
| ❌ 不改 `schemaTypes/`、`sanity.config.ts`、`sanity.cli.ts` | 拒绝 |
| ❌ 不用 `--replace` 导入 | 只用 `--missing` |
| ❌ 不删 production 文档 | 拒绝 |
| ❌ 不改 `.env` 的 projectId / dataset | 拒绝 |
| ✅ Features：`convert-features.js` 或 `import-page.js` → `import --missing` | 允许 |
| ✅ Blog 才用 `fix-category-refs.js` | Features 一般不需要 |

**所有权边界**

```
前端维护 → sanity.config.ts / schemaTypes/ / components/
我们操作 → Pages/Features/*.json → convert-*.js → import --missing
```

---

## 4. Features 页面结构（5 组件）

生成规范来自 **Features Page Generator v2.3.0**：

| 序号 | section `type` | 内容 | 数量 |
|------|----------------|------|------|
| 1 | `centeredInputSection` | 大标题、subtitle、system_prompt、input_placeholder、4 suggestions | 1 |
| 2 | `threeColumnSection` | 三步工作流（Input → Interact → Deliver） | 1 |
| 3 | `featureGridSection` | 6 个痛点 feature（icon_url + title + description） | 1 |
| 4 | `testimonialSection` | 3 个带业务数据的 testimonial | 1 |
| 5 | `faqSection` | FAQ（通常 9+ 个，可多个 faqSection 块） | 1+ |

**本地 JSON 两种等价格式**（转换脚本均支持）：

| 格式 | 字段 | 说明 |
|------|------|------|
| 新格式（当前主流） | `bodyJson` 字符串 | 已 Sanity 化的 section 数组 JSON.stringify |
| 旧格式 | `section[]` 数组 | 原始 section 对象数组 |

**必填字段**：`slug`、`language`、`title`、`description`、sections（`bodyJson` 或 `section`）

**可选但推荐**：`seo` 对象（含 `ogImage`、`structuredData`）、`keywords`

---

## 5. 字段映射（本地 JSON → compositePage）

```
本地 JSON                         → Sanity compositePage
────────────────────────────────────────────────────────────
id / uuid / _index.json 中的 id   → _id = "{id}-{lang}"
slug                              → slug.current（各语言相同）
language                          → language
category: "feature"               → category: "feature"
（固定）                          → sourceType: "features"
title                             → title
description                       → description（≤500 字）
bodyJson 或 section[]             → bodyJson（stringify 后）
seo { ... }                       → seo（原样合并，缺则自动生成）
seo.ogImage / section 首张图       → cover（imageSource, external）
releaseDate / create_time         → releaseDate
url_path                          → 不写入（schema 无字段）
_source                           → 不写入
```

**`_id` 策略（Incident：227 duplicate）**

- 同一数字 `id` **不得**跨语言共用 `_id`。
- 正确：`786-en`、`786-de`；错误：两个语言都用 `786`。
- 解析顺序：`uuid` → `id` → `_index.json` 查表 → 回退 `features-{slug}`。

---

## 6. 端到端流程（含门禁）

### Gate 0 — 环境 + 首次运行

> **策略 SSOT**：[`Skills/lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](../../Skills/lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)

**首次**（本机未做过 Sanity 发布）：先完成下列步骤，**再**大批量 convert/import。

| 步骤 | 命令 |
|------|------|
| 认证 | `npx sanity login` |
| 检查 | `node scripts/check-sanity-auth.js` |
| 拉线上参照 | `node scripts/convert-features.js --dry-run` → 读 `~/lovart/import-features-report.json`（看缺失语言 / 重复 _id） |
| 试跑 | `import-page.js` 单篇 `--dry-run` 或小范围 `--lang` |

**日常**（默认）：只处理**新增或明确变更**的 JSON → `import --missing`。**本地已有且线上已有同 `_id` 的篇目，不要全量重发**，除非用户明确要求。

```bash
cd "…/1-4 Dev/lovart.sanity.studio"
grep -E "SANITY_STUDIO_PROJECT|SANITY_STUDIO_DATASET" .env
# 期望：o11tm2qe / production

npx sanity debug --secrets
# 已登录 sevena@lovart.ai

git status
# 确认未误改 schemaTypes/、sanity.config.ts
```

### Gate 1 — 确认本地 JSON

- [ ] 文件在 `Pages/Features/{lang}/`，命名 `{slug}-{lang}.json`
- [ ] **`slug` 必须为 kebab-case**（禁止 `_`、空格）— preflight `SEO_SLUG` BLOCK
- [ ] **`_index.json` 中同一主题无重复 slug**（legacy 下划线页 vs 新 kebab 页）
- [ ] 5 组件齐全；`type` 字段名勿改
- [ ] 多语言：**同一 slug**，**不同 `_id`**
- [ ] 图片 URL 优先 `https://assets-persist.lovart.ai/`
- [ ] 发布前：`node scripts/preflight-content.js --type features [--lang en,ja]`

### Gate 2 — 转换 NDJSON

**单篇（推荐试跑）**

```bash
# 预览 compositePage 文档，不写文件
node scripts/import-page.js "../Pages/Features/en/graphic-design-en.json" --dry-run

# 生成 NDJSON
node scripts/import-page.js "../Pages/Features/en/graphic-design-en.json"

# 生成并导入
node scripts/import-page.js "../Pages/Features/en/graphic-design-en.json" --import
```

**批量**

```bash
# 预检（不写 NDJSON）
node scripts/convert-features.js --dry-run

# 查看报告
cat ~/lovart/import-features-report.json | head -80

# 正式生成
node scripts/convert-features.js

# 只处理部分语言
node scripts/convert-features.js --lang en,de,ja
```

**输出**

| 文件 | 说明 |
|------|------|
| `~/lovart/import-features.ndjson` | 批量导入用 |
| `~/lovart/import-features-report.json` | 条数、重复 _id、marker、缺失语言、sourceFormat |
| `~/lovart/import-page-{slug}-{lang}.ndjson` | 单篇导入用 |

**导入前检查**

```bash
wc -l ~/lovart/import-features.ndjson
grep -c 'section_' ~/lovart/import-features.ndjson   # 期望 0（无翻译 marker 残留）
```

用户明确确认后再执行导入（与 Blog / Tools 发布协议一致）。

### Gate 3 — 导入 production

```bash
npx sanity dataset import ~/lovart/import-features.ndjson --dataset production --missing
```

- `--missing`：仅新增缺失 `_id`，**不覆盖** Studio 内已编辑文档。

### Gate 4 — 落库校验（推荐随机抽查）

```bash
npx sanity exec scripts/verify-composite.js --with-user-token -- \
  --ndjson ~/lovart/import-features.ndjson --sample 20
```

GROQ 手工抽查：

```groq
// 按语言统计
count(*[_type == "compositePage" && sourceType == "features" && language == "en"])

// 某 slug 多语言是否齐全
*[_type == "compositePage" && category == "feature" && slug.current == "graphic-design"]{
  _id, language, title, _updatedAt
}

// 最近导入
*[_type == "compositePage" && sourceType == "features"] | order(_updatedAt desc)[0...5]{
  title, "slug": slug.current, language, _id
}
```

### Gate 5 — Studio 抽查

打开 https://lovart.sanity.studio → **Content → Features**（`category == "feature"`），检查模块、SEO、封面。

---

## 7. 缺失翻译（translate-features.py）

当 `_index.json` 或报告提示某 slug 缺少 `de`/`ja`/… 版本时：

```bash
python3 scripts/translate-features.py --target de,ja,ko
python3 scripts/translate-features.py --concurrency 2 --limit 5    # 试跑
python3 scripts/translate-features.py --force                      # 重翻已完成项
```

**策略要点**

| 项 | 说明 |
|----|------|
| 输入 | `Pages/Features/en/{slug}-en.json` |
| 输出 NDJSON | `~/lovart/import-features-missing.ndjson` |
| 模型 | MiniMax-CN（`MiniMax-M2.7`），配置 `~/.mavis/config.yaml` |
| **禁止翻译** | `system_prompt`、`suggestion.value`、`type`、`image_url`、`icon_url` |
| 源 section | 从 `section[]` 或 `bodyJson` 解析（与 convert 一致） |
| 断点续传 | `~/lovart/features-translate-progress.json` |
| 边译边写 | 进程被杀不丢已译条目 |

**导入翻译补全**

```bash
npx sanity dataset import ~/lovart/import-features-missing.ndjson --dataset production --missing
```

---

## 8. Marker 清洗

非 en 翻译可能残留 `(section_de)` 等标记。转换库 `deepCleanMarkers()` 在 stringify 前递归清洗。

```javascript
const MARKER_PATTERN = /\s*\(section_[a-z]{2}(?:-[A-Z]{2})?\)\s*/g
```

验证：`grep -c 'section_' ~/lovart/import-features.ndjson` → **0**

---

## 9. 命令速查

```bash
export STUDIO="…/1-4 Dev/lovart.sanity.studio"
cd "$STUDIO"

# ── 单篇 ──
node scripts/import-page.js "../Pages/Features/en/{slug}-en.json" --dry-run
node scripts/import-page.js "../Pages/Features/en/{slug}-en.json" --import

# ── 批量 Features ──
node scripts/convert-features.js --dry-run
node scripts/convert-features.js
npx sanity dataset import ~/lovart/import-features.ndjson --dataset production --missing

# ── 翻译补全 ──
python3 scripts/translate-features.py --target it,pt,ru
npx sanity dataset import ~/lovart/import-features-missing.ndjson --dataset production --missing

# ── 兄弟管道（勿混用）──
node scripts/convert-tools.js          # Tools
node convert.js                        # Blog
```

---

## 10. 常见坑与修复

| 现象 | 原因 | 修复 |
|------|------|------|
| bodyJson 为空 `[]` | 旧脚本只读 `section`，忽略 `bodyJson` | 已修复：用 `feature-to-composite-page.js` |
| Studio Feature Content 为空 | 缺 `sourceType: "features"` | convert 已写入；旧数据需 patch |
| duplicate `_id`（227 篇） | 跨语言共用 id | `_id = "{id}-{lang}"` |
| `section_de` 出现在正文 | 翻译 marker 未清 | `deepCleanMarkers()` |
| `_id` 变成 `features-slug-en-en` | translate 回退 id 含 lang | 已修复 translate-features.py |
| import 全跳过 | `_id` 已存在 | 正常（`--missing`）；更新请 Studio 手改 |
| 误用 `convert-tools.js` | Tools / Features 脚本不同 | Features 只用 `convert-features.js` |
| 误用 `convert.js` | Blog 管道 | Features 不走 Markdown 转换 |
| `<think>` 污染 JSON | MiniMax 推理输出 | translate 脚本正则剥离 |
| `quota exhausted` | API 配额耗尽 | 换 provider 或稍后重试 |
| compositePage Studio 不可见 | 未注册 schema 类型 | 数据在 dataset，前端 GROQ 可读；Feature Content 列表按 sourceType 筛 |
| **`SEO_SLUG` 含下划线** | 历史 admin 导出或重复页 | 用 kebab-case；删 legacy 重复 JSON + `_index` 条目；线上旧 URL 配 301（见总指南 §4.5） |
| 同主题两篇（如 menu design） | 迁移未合并 | 保留 canonical slug（kebab）；删 `_` 版；production `81-*` 勿删，仅 301 |

---

## 11. 与内容生产管线的关系

```
lovart-content-calendar
  → lovart-landing-page (feature-page)
  → Pages/Features/{lang}/*.json
  → lovart-content-audit
  → 【本指南】convert-features.js / import-page.js → import --missing
  → （可选）translate-features.py → import --missing
  → lovart-sitemap-update
```

**Pipeline Orchestrator** Step 3 路由：`feature-page` → `lovart-landing-page` → 本指南发布步骤。

---

## 12. Agent / 人工触发词

| 说法 | 动作 |
|------|------|
| 「同步 Features 到 Sanity」「发布功能页」「import features」 | 读本指南 + `lovart-features-sanity-publish` Skill |
| 「单篇功能页导入」 | `import-page.js --dry-run` → 确认 → `--import` |
| 「Sanity push」「发布博客」 | 走 `SOP-Sanity同步指南.md`（管道 A） |
| 「同步 Tools」 | 走 Tools 统合指南（管道 C） |

---

## 13. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-29 | 初版统合；新增 `feature-to-composite-page.js`、`import-page.js`；bodyJson 双格式支持；写入 `sourceType: features` |
| 2026-05-29 | Gate 1 slug 规范；清理 legacy `restaurant_menu_design`（保留 `restaurant-menu-design` id 163） |
| 2026-05-29 | Gate 0 首次认证+拉线上参照 vs 日常增量 |
