# Sanity Blog 发布统合指南

> **单一事实来源（SSOT）** — 统合自：SOP 同步指南、内容管道规则、AGENTS 规范、Sanity Publish Skill、批量导入方案、Skills 汇总。
>
> 适用项目：**lovart.ai** · Project ID `o11tm2qe` · Dataset `production` · Studio https://lovart.sanity.studio

---

## 0. 一句话总结

本地 Blog 发布 = **预检 MD → sync taxonomy → convert → 预检 NDJSON → import --missing → fix-category → link-translations → verify**。这是**内容管道**，不是 Studio/Schema 发布。

### 0.1 首次运行与增量（Agent 必守）

**SSOT**：[`references/first-run-and-incremental-policy.md`](./references/first-run-and-incremental-policy.md)

| 阶段 | 要求 |
|------|------|
| **首次** | `.env` + `npx sanity login` + `check-sanity-auth` → **`sync-blog-taxonomy`（拉线上 category/tag 到本地）** → 小批量 `--dry-run` 试跑 |
| **已有** | 本地有、线上已有同 `_id` → **不**全量重发该篇 |
| **日常** | 仅处理新增/变更 MD；`import` **只用 `--missing`** |
| **全量** | 仅当用户**明确要求**（含 `--replace`、无 `--lang` 扫全库 import） |

---

## 1. 心智模型

```
Sanity Blog/*.md
    ↓  gray-matter + marked + htmlToPortableText
import.ndjson
    ↓  npx sanity dataset import --missing
production 数据集（blog 文档）
    ↓  GROQ
lovart.ai 前端渲染
```

| 概念 | 说明 |
|------|------|
| **内容管道**（我们做的） | MD → NDJSON → 增量导入数据 |
| **Studio 发布**（前端做的） | `sanity deploy` 部署 Schema/插件 |
| **覆盖范围** | `--missing` 只新增 `_id` 不存在的 blog；UUID 文档、Page/Docs/News、Schema 均不受影响 |

### 所有权边界

```
前端团队维护 → sanity.config.ts / sanity.cli.ts / schemaTypes/ / components/
内容团队操作 → Sanity Blog/*.md → convert.js → import --missing
```

---

## 2. 项目速查

| 项 | 值 |
|---|---|
| Project ID | `o11tm2qe` |
| Dataset | `production`（当前无 staging，测试需单独创建） |
| Studio | https://lovart.sanity.studio |
| 本地代码 | `1-Project/1-4 Dev/lovart.sanity.studio/`（或 `~/lovart`） |
| MD 源目录 | `1-Project/1-4 Dev/lovart.sanity.studio/Sanity Blog/`（重构后从旧 `Lovart/Sanity Blog/` 迁移；如缺失需确认源稿落点） |
| 转换脚本 | `sanity-studio/convert.js` |
| NDJSON 输出 | `sanity-studio/import.ndjson` |
| 分类修复 | `sanity-studio/fix-category-refs.js` |
| 翻译关联 | `sanity-studio/link-translations.js` |
| 导入前预检 | `scripts/preflight-content.js` · Skill `lovart-content-quality-gates/` |
| 导入后验收 | `scripts/verify-blog-publish.js` |
| 分类 ID 缓存 | `scripts/sync-blog-taxonomy.js` → `scripts/lib/blog-taxonomy.json` |
| 环境模板 | `sanity-studio/.env.example` |

---

## 3. 环境准备

### 3.1 前置条件

- Node.js ≥ 18
- 已 `npm install` / `pnpm install`
- 已 `npx sanity login`（账号需被邀请进项目）

### 3.2 .env 必检项

```bash
grep SANITY_STUDIO .env
```

| 变量 | 期望值 |
|------|--------|
| `SANITY_STUDIO_PROJECT_ID` | `o11tm2qe` |
| `SANITY_STUDIO_DATASET` | `production` |
| `SANITY_STUDIO_API_TOKEN` | Editor 权限 Token（manage.sanity.io → API → Tokens） |

### 3.3 登录验证

```bash
npx sanity debug --secrets
```

### 3.4 执行前检查清单（按顺序）

1. 工作目录为正确的 `sanity-studio/`
2. `.env` 指向 `o11tm2qe` + `production`（不擅自修改）
3. `git status`：未误改 `sanity.config.ts`、`sanity.cli.ts`、`schemaTypes/`
4. 待发布 MD 已在 `Sanity Blog/` 下就绪
5. 导入前预览 `import.ndjson`（条数、`_type`、`_id`、语言、slug）
6. 优先使用 `--missing`，不用 `--replace`

---

## 4. Markdown 规范

### 4.1 文件目录

```
Sanity Blog/
├── Original/          ← 已发布（旧格式 📋 配置信息）
├── Lovart Fake/       ← 新文章
└── Content Calendar/  ← 新文章（推荐，按分类分子目录）
```

### 4.2 推荐格式（YAML frontmatter）

```markdown
---
title: "文章标题"
slug: "article-slug"
date: "2026-05-15"
author: "Seven"
category: "How-To"
language: "en"
description: "SEO 描述"
keywords: ["关键词1", "关键词2"]
tags: ["标签1", "标签2"]
cover_url: "https://assets-persist.lovart.ai/..."
---

# 正文标题

正文内容...
```

### 4.3 旧格式（Original/ 已发布文章）

文件末尾含 `📋 配置信息` 块：标题、slug、cover_url、author、language、category、tags、seo_title、seo_description、JSON-LD 等。`convert.js` 同样支持解析。

### 4.4 分类（12 选 1，category 字段必须精确匹配）

| 分类名 | 适用场景 |
|--------|----------|
| Lovart 101 | 产品介绍、教程 |
| How-To | 操作指南 |
| Best Practice | 工具评测、对比 |
| Insight & Trend | 行业洞察 |
| Better Design | 设计方法论 |
| Design | 设计技巧 |
| Branding | 品牌设计 |
| Video | 视频相关 |
| Topics | 话题讨论 |
| canvas | Canvas 功能 |
| AI Image Tools | AI 图片工具 |
| AI Video Tools | AI 视频工具 |

### 4.5 多语言

| 规则 | 说明 |
|------|------|
| 文件命名 | 英文 base + `-zh`/`-ja`/`-ko`/`-pt`/`-ru` 等后缀 |
| frontmatter | 加 `language: zh` 等 |
| slug | **各语言共享同一 slug**（URL 靠路径前缀区分） |
| 文档 `_id` | 英文 `my-slug`，中文 `my-slug-zh`（convert.js 自动处理） |
| 支持语言 | en（默认）、de、zh、zh-TW、ja、ko、fr、ru、pt、it |
| 团队规范 | 每篇至少 EN + CN 两个版本 |

**URL 规则：**

- EN: `www.lovart.ai/blog/{slug}`
- ZH: `www.lovart.ai/zh/blog/{slug}`
- JA: `www.lovart.ai/ja/blog/{slug}`

### 4.6 内链规范

- 站内链接：**`/blog/{slug}`**
- 禁止：`/博客文章/`、`/cluster/*`、`.md` 文件路径、`#` 占位
- pt/ru 翻译稿同步修内链；可复跑 `scripts/fix-blog-internal-links.py`

### 4.7 图片规范

- 封面/正文图 URL 必须以 **`https://assets-persist.lovart.ai/`** 开头
- 从 `image-library.md` 或 `URL_REGISTRY.md` 选取，**严禁编造 URL**
- 正文不得泄露 `[IMAGE PLACEHOLDER]`、`[REAL SCREENSHOT REQUIRED]` 等占位符

### 4.8 字段长度建议

| 字段 | 建议上限 |
|------|----------|
| title | 70 字符 |
| description | 170 字符 |
| seo.title | 60 字符 |
| seo.description | 160 字符 |
| slug | 仅 `a-z` `0-9` `-`，无空格/下划线，不以 `/` 开头 |

---

## 5. 标准发布流程

> **首次 / 增量**：[`references/first-run-and-incremental-policy.md`](./references/first-run-and-incremental-policy.md)

### 5.0 质量门控（导入前 / 导入后）

> 详细命令见 Skill **`lovart-content-quality-gates/`**

```bash
cd sanity-studio

# A. 写作/翻译完成后 — 检查 MD（SEO、分类、内链、i18n parity）
node scripts/preflight-content.js --type blog-md
node scripts/preflight-content.js --type blog-i18n          # 同 slug 缺 EN/zh
node scripts/preflight-content.js --type blog-md --check-urls  # 内链 HTTP 抽检

# B. convert 后、import 前 — 检查 NDJSON
node scripts/preflight-content.js --type blog-ndjson

# C. import 后 — GROQ 验收 + 翻译 metadata
npx sanity exec scripts/verify-blog-publish.js --with-user-token --since-minutes 60
npx sanity exec link-translations.js --with-user-token --dry-run
npx sanity exec link-translations.js --with-user-token
```

| 阶段 | 脚本 | 检查项 |
|------|------|--------|
| MD | `preflight-content.js --type blog-md` | frontmatter、category、CDN、内链、占位符 |
| i18n | `--type blog-i18n` | 同 slug 缺 EN/zh、文件名后缀 vs language |
| NDJSON | `--type blog-ndjson` | `_type`、slug、body、seo 长度、cover |
| 线上 | `verify-blog-publish.js` | category、body、CDN、translation.metadata |
| 翻译组 | `link-translations.js` | 同 slug 多语言 → `translation.metadata` |

`lovart-content-audit` 负责写作质量/合规；`lovart-content-quality-gates` 负责 **Sanity 技术字段与 i18n**。

### 5.1 标准命令

```bash
cd sanity-studio

# ① 同步分类/标签 _id（首次或 Studio 分类变更后）
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token

# ② MD → NDJSON（含 category / tags / seo.keywords；按语言分批）
node convert.js --lang en,zh,zh-TW

# ③ 增量导入（按 import-blog-manifest.json 逐批）
npx sanity dataset import ~/lovart/import-blog-en-batch01.ndjson --dataset production --missing

# ④ 补分类（convert 未映射到的文章）
npx sanity exec fix-category-refs.js --with-user-token
```

### 5.2 转换链路

```
MD (YAML frontmatter 或 📋 配置信息)
  → gray-matter 提取元数据
  → marked 转 HTML
  → htmlToPortableText 转 Sanity Portable Text
     · h1-h6 → block.style
     · **bold** → marks: ["strong"]
     · [link](url) → marks + markDefs
     · ![](url) → bodyImage 块
     · |table| → table 块（@sanity/table，非 tableBlock）
```

### 5.2.1 convert.js 字段写入（导入前须知）

**首次或分类变更后**：`npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token`

| 项 | 行为 |
|----|------|
| `category` | 写入 `reference`（需 `scripts/lib/blog-taxonomy.json`）；未映射可再跑 `fix-category-refs.js` |
| `tags` | 写入 `reference[]`；NDJSON 先写 `tag-{slug}` 文档，再写 blog |
| `seo.keywords` | 写入字符串数组（无则 `[]`） |
| `seo.structuredData.json` | 默认空字符串 |
| 无 `cover_url` | liblib CDN 池轮询（**优先** MD 内 `assets-persist.lovart.ai`） |
| 输出路径 | `~/lovart/import-blog-{lang}-batch*.ndjson` + manifest |

### 5.2.3 convert.js 分批（避免 OOM）

与 [`1-4 Dev/lovart.sanity.studio/Sanity-Blog-发布统合指南.md`](../../1-4 Dev/lovart.sanity.studio/Sanity-Blog-发布统合指南.md) §5.2.3 同步（`--lang`、`--batch-size 100`、`--dry-run`、`import-blog-manifest.json`）。

### 5.2.4 PT/RU 批次专用流程（与全量 convert.js 不同）

```
convert-subset.js --all  →  import --missing  →  fix-category-all.js  →  verify-all.js
```

详见 `OPENCODE-L0-PT-RU-SYNC.md`、`OPENCODE-PT-RU-ALL.md`。此路径**不跑**根目录 `convert.js` / `fix-category-refs.js`。

### 5.3 导入模式选择

| 模式 | 命令 | 用途 |
|------|------|------|
| **增量新增**（默认） | `--missing` | 新文章、多语言新版本 |
| 全量替换 | `--replace` | ⚠️ 仅用户明确授权时使用，会覆盖同 `_id` 文档 |

### 5.4 多语言完整流程

```
1. 复制英文 MD → xxx-zh.md
2. frontmatter 加 language: zh，翻译标题/描述/正文/SEO
3. node scripts/preflight-content.js --type blog-md
4. npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token
5. node convert.js
6. node scripts/preflight-content.js --type blog-ndjson
7. npx sanity dataset import ~/lovart/import.ndjson --dataset production --missing
8. npx sanity exec fix-category-refs.js --with-user-token
9. npx sanity exec link-translations.js --with-user-token
10. npx sanity exec scripts/verify-blog-publish.js --with-user-token --slug {slug}
```

**link-translations.js**：按 `slug.current` 分组，创建/补全 `translation.metadata`（`@sanity/document-internationalization` v6 结构）。

```bash
npx sanity exec link-translations.js --with-user-token --dry-run
npx sanity exec link-translations.js --with-user-token --slug my-slug
```

OpenCode L0 pt/ru：先读 `OPENCODE-L0-PT-RU-SYNC.md`（preflight 门禁），译稿与内链在 import 前完成。

---

## 6. 安全发布协议（7 步门控）

> 来源：`lovart-sanity-publish` Skill v3.0 — 由 13 个真实 Incident 驱动，Cursor 中说「Sanity push」/「发布」触发。

| 步骤 | 动作 | 门控 |
|------|------|------|
| 1 Initiation | 扫描待导入 MD，输出安全协议摘要 | 等用户确认 |
| 2 Preflight | `.env` + **MD 预检**（`lovart-content-quality-gates`） | 输入 `preflight confirmed` |
| 3 Convert | sync-taxonomy → `convert.js` + **NDJSON 预检** | 输入 `import confirmed` |
| 4 Import | `import --missing` | — |
| 5 Validate | `verify-blog-publish.js` + `link-translations.js` | — |
| 6 Fix Refs | `fix-category-refs.js`（补漏） | `fix refs` |
| 7 Done | 更新日历、Studio 抽查 | `done` |

**快捷指令：** `preflight` → `preflight confirmed` → `import confirmed` → `fix refs` → `done` · 任意步骤 `cancel`

---

## 7. 安全规则（硬性）

### 7.1 绝对禁止

| 操作 | 原因 |
|------|------|
| `npx sanity deploy` | 覆盖线上 Schema 和插件配置 |
| 修改 `sanity.config.ts` / `sanity.cli.ts` / `schemaTypes/` / `components/` | Schema 归前端团队 |
| `import --replace`（无明确授权） | 覆盖管理员在 Studio 编辑过的内容 |
| 删除 `production` 文档 | 不可逆 |
| 修改 `.env` 的 projectId / dataset | 可能导入错误环境 |
| 批量写入 page / docs / news / category / tag | 只操作 blog |

### 7.2 允许

- 新增/修改 `Sanity Blog/` 下 Markdown
- `node convert.js` → `import.ndjson`
- `import --missing`
- `fix-category-refs.js` / `link-translations.js`
- `scripts/preflight-content.js` / `scripts/verify-blog-publish.js`
- 导入前备份或预览 NDJSON

---

## 8. 导入后验证

### 8.1 自动化验收

```bash
npx sanity exec scripts/verify-blog-publish.js --with-user-token
npx sanity exec scripts/verify-blog-publish.js --with-user-token --slug my-article
npx sanity exec scripts/verify-blog-publish.js --with-user-token --since-minutes 30
```

### 8.2 CLI 查询

```bash
# 总数
npx sanity documents query 'count(*[_type == "blog"])' --dataset production

# 最新 5 篇
npx sanity documents query '*[_type == "blog"] | order(_createdAt desc)[0...5]{title, "slug": slug.current, language}' --dataset production

# 按分类
npx sanity documents query '*[_type == "blog" && category->title=="How-To"]{title, slug}' --dataset production
```

### 8.3 Studio 可视化

```bash
npx sanity dev   # http://localhost:3333
```

线上：https://lovart.sanity.studio — 抽查 1–2 篇封面、正文、SEO、分类。

### 8.4 验收检查项

- [ ] 文档数与预期一致
- [ ] `_type` 仅为 blog
- [ ] 分类不为空（空则重跑 fix-category-refs）
- [ ] 多语言 slug 对应正确
- [ ] 封面 CDN 合规、无占位符泄露
- [ ] 内链格式 `/blog/{slug}`
- [ ] `translation.metadata` 已关联（多语言稿跑 `link-translations.js`）

---

## 9. Blog Schema 字段对照

```typescript
{
  _id: string              // en: "my-slug", zh: "my-slug-zh"
  _type: "blog"
  title: string
  slug: { current: string }
  author: string
  description: string
  releaseDate: datetime
  language: string         // en/zh/ja/ko/es/fr/de/pt/...
  pinned: datetime         // 置顶时间（非 boolean featured）；有值则置顶，Studio 按 pinned desc 排序
  category: reference → category
  tags: reference[] → tag
  cover: imageSource       // { url, alt, sourceType: "external"|"upload" }
  body: blockContent[]     // Portable Text（见下方块类型）
  seo: {
    title: string
    description: string
    keywords: string[]
    noIndex: boolean
    ogImage: imageSource
    structuredData: { enabled: boolean, json: string }
  }
}
```

### Body 块类型（当前 schema，非 convert.js 全量产出）

Studio `blogType.ts` 支持 9 种 body 块：

| `_type` | 说明 | convert.js 是否产出 |
|---------|------|---------------------|
| `block` | 标准 Portable Text（h2/h3/blockquote、列表、link） | ✅ |
| `bodyImage` | 正文图片（imageSource） | ✅ |
| `table` | `@sanity/table` 插件表格 | ✅（非 tableBlock） |
| `mediaText` | 图文混排 | ❌ 仅 Studio 手编 |
| `videoEmbed` | 视频嵌入 | ❌ |
| `embed` | iframe 嵌入 | ❌ |
| `markdownBlock` | Markdown 块 | ❌ |
| `cta` | 行动号召 | ❌ |
| `faq` | FAQ 问答 | ❌ |

### 自定义对象类型

| 类型 | 用途 |
|------|------|
| `imageSource` | 封面/OG 图（外部 URL 或上传） |
| `structuredData` | JSON-LD |
| `table` | Sanity table 插件（**不是** `tableBlock`） |
| `bodyImage` | 正文图片 |

### 前端 GROQ 示例

```groq
// 取中文版
*[_type == "blog" && language == "zh" && slug.current == $slug][0]

// 取所有翻译版本
*[_type == "blog" && slug.current == $slug]{ language, title, description }

// 列表排序
*[_type == "blog" && language == $lang] | order(pinned desc, releaseDate desc)[0...20]
```

---

## 10. 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| slug 重复 / 导入跳过 | `_id` 已存在 | `--missing` 会跳过；改 slug 或确认是否重复发布 |
| 分类为空 | 导入后 reference 未关联 | `fix-category-refs.js` |
| convert.js 失败 | frontmatter YAML 错误 / 缺必填字段 | 检查 title、slug、language、UTF-8 编码 |
| 封面图挂了 | URL 无效或非 Lovart CDN | 换 `cover_url` 为 `assets-persist.lovart.ai` |
| 导入后格式不对 | Schema 字段变更 / convert 映射过期 | 联系前端同步 schema；Studio 手动改或修正 MD 后换 `_id` 重导 |
| Schema 不一致 | 本地 schemaTypes 过期 | Preflight 比对；不自行改 schema，联系前端 |
| API 超时 | 网络 | 稍后重试 |
| ID 含特殊字符 | slug 含 `&`、空格 | convert.js 自动清洗 |

---

## 11. Skills 与自动化索引

### 11.1 内容生产管线

```
Daily Raw CSV
  → ① lovart-keywords-intake（P0/P1/P2 评分 → 更新日历）
  → ② lovart-content-writer（12 类型 × 11 框架 → 写作 + SEO + MD 导出）
  → ② lovart-content-writer → ③ lovart-content-quality-gates（MD/NDJSON 技术预检）
  → ④ lovart-sanity-publish（7 步安全发布协议）
```

| Skill | 版本 | 位置 |
|-------|------|------|
| Keywords Intake | 1.0.0 | `4-Archive/Skills/lovart-keywords-intake.md` |
| Content Writer | 4.0.0 | `4-Archive/Skills/lovart-content-writer.md` |
| Production Orchestrator | 1.0.0 | `4-Archive/Skills/lovart-production-orchestrator.md` |
| **Quality Gates** | 1.0.0 | `Skills/lovart-content-quality-gates/` |
| **Sanity Publish** | 3.0.0 | `Skills/lovart-sanity-publish/` |
| Multi-Platform Push | — | `Skills/lovart-multi-platform-push/SKILL.md` |
| Content Audit | — | `Skills/lovart-content-audit/`（写作/合规，与 Preflight 互补） |

### 11.2 Cursor 规则

| 规则 | 位置 | 作用 |
|------|------|------|
| 内容管道 | `Lovart/.cursor/rules/lovart-sanity-content-pipeline.mdc` | Agent 自动遵守的安全约束 |
| Karpathy 准则 | `.cursor/rules/karpathy-guidelines.mdc` | 全局编码/执行规范 |

### 11.3 Sanity 官方 Skill（通用）

| Skill | 用途 |
|-------|------|
| `sanity-best-practices` | Schema、GROQ、迁移、Portable Text、框架集成 |
| `content-modeling-best-practices` | 内容模型设计 |
| `seo-aeo-best-practices` | SEO / JSON-LD |

---

## 12. 从线上拉取 / 备份

```bash
# 全量导出
npx sanity dataset export production blog-backup.tar.gz

# 查询特定类型
npx sanity documents query "*[_type=='blog']" --dataset production > blogs.json
```

---

## 13. 开发相关（内容同学通常不需要）

| 操作 | 命令 | 注意 |
|------|------|------|
| 本地 Studio | `npx sanity dev` | 连接 production 数据集 |
| 部署 Studio | `npx sanity deploy` | ⚠️ 仅前端授权操作 |
| 创建 staging | `npx sanity dataset create staging` | 测试用独立数据集 |
| GROQ 调试 | Vision Tool | `localhost:3333/vision` |

---

## 14. 源文档索引（本指南统合来源）

| 文档 | 路径 | 状态 |
|------|------|------|
| **本指南（SSOT）** | `Skills/lovart-sanity-publish/Sanity-Blog-发布统合指南.md` | ✅ Skills 主副本 |
| 同内容镜像 | `1-4 Dev/lovart.sanity.studio/Sanity-Blog-发布统合指南.md` | ✅ sanity-studio 副本 |
| 原 SOP | `sanity-studio/SOP-Sanity同步指南.md` | 参考（部分内容重复） |
| 管道规则 | `Lovart/.cursor/rules/lovart-sanity-content-pipeline.mdc` | Cursor 自动加载 |
| Studio 开发规范 | `sanity-studio/AGENTS.md` | Schema/模块开发用 |
| 批量导入通用方案 | `Product Project Management/Sanity批量导入实操方案.md` | 通用 Sanity 导入参考 |
| Sanity Publish Skill | `Skills/lovart-sanity-publish/SKILL.md` | 7 步门控摘要 |
| Skills 汇总 | `Skills/lovart-blog-automation/references/lovart-skills-and-norms-summary.md` | 全管线索引 |
| pt/ru 批次 | `sanity-studio/OPENCODE-L0-PT-RU-SYNC.md` | 多语言专项 |

---

## 15. 快速上手卡片（可打印）

```
┌─────────────────────────────────────────────────────────┐
│  Sanity Blog 发布 — 快速卡片 (v1.2)                       │
├─────────────────────────────────────────────────────────┤
│  ① .env → o11tm2qe / production（见 .env.example）      │
│  ② preflight MD → sync-blog-taxonomy → convert.js       │
│  ③ preflight NDJSON → import --missing                  │
│  ④ fix-category-refs → link-translations                │
│  ⑤ verify-blog-publish → Studio 抽查 → done              │
├─────────────────────────────────────────────────────────┤
│  ❌ deploy  ❌ --replace  ❌ 改 schema  ❌ 删文档          │
└─────────────────────────────────────────────────────────┘
```

---

*最后更新：2026-05-29 · 统合版本 v1.2（预检 + link-translations + verify）*

---

## 16. 代码库比对审计（2026-05-29）

> 对照 `lovart.sanity.studio/` + `sanity-studio/` schema/脚本 与 Skills 文档。前端 `apps/lovart` **不在本 vault**，以下前端部分来自 Studio 配置与 CLAUDE.md。

### 16.1 代码库双副本

| 目录 | 说明 |
|------|------|
| `1-4 Dev/lovart.sanity.studio/` | 内容管道主工作区（convert.js、fix-category-refs.js、scripts/） |
| `1-4 Dev/lovart.sanity.studio/` | Studio 源码镜像（schema、deskStructure、sanity.config） |

两者 schema 应保持一致；内容同步只在 `sanity-studio/` 执行。

### 16.2 Studio 侧边栏结构（deskStructure.ts）

```
Blog → News → Docs → Pages
Features / Tools / Products / Solutions / Scenarios / Topics（compositePage 按 category 分栏）
Content Library（People / Testimonials / Logos / Pricing）
Settings（Categories / Tags）
```

`compositePage` 在 production 使用但**未注册于本地 schemaTypes/** — Features/Tools 导入后数据可读、列表可见，Studio 表单可能不完整。

### 16.3 Skills 疏漏清单

| 优先级 | 疏漏 | 现状 | 建议 |
|--------|------|------|------|
| **P0** | `link-translations.js` | ✅ 已存在 | §5.4 |
| **P0** | `pinned` / `table` | ✅ | — |
| **P0** | multi-platform-push Sanity 段 | ✅ 已委托 lovart-sanity-publish | — |
| **P0** | page-generation blogPost | ✅ SKILL 为 `blog` | — |
| **P1** | Archive seoTitle/featuredImage | 未改 | BACKLOG |
| **P1** | convert 字段 + OOM | ✅ sync + 分批 | — |
| **P1** | liblib 默认封面 | 策略未改 | MD 写 cover_url |
| **P2** | 前端 / Presentation | 待办 | BACKLOG 阶段 4 |

排期：`1-4 Dev/lovart.sanity.studio/LOVART-SANITY-BACKLOG.md`

### 16.4 三条 Sanity 管道索引

| 管道 | Skill | 脚本 | 类型 |
|------|-------|------|------|
| Blog | `lovart-sanity-publish/` | `convert.js` | `blog` |
| Features | `lovart-features-sanity-publish/` | `convert-features.js` | `compositePage` |
| Tools | `lovart-tools-sanity-publish/` | `convert-tools.js` | `compositePage` |
| 总索引 | `lovart-sanity-content-publish/` | — | 路由三条管道 |

### 16.5 fix-category-refs.js 分类别名

除 12 个标准 display name 外，脚本自动映射：

- `BOFU` → `Best Practice`
- `TOFU` → `How-To`
- `MOFU` → `Insight & Trend`

### 16.6 前端集成（apps/lovart，vault 外）

| 模块 | 路径 |
|------|------|
| Sanity client | `src/request/sanity/client.ts` |
| Blog 查询 | `src/request/sanity/blog.ts` |
| compositePage | `src/request/sanity/compositePage.ts` |
| Portable Text | `src/components/sanity/PortableTextRenderer.tsx` |
| SEO | `SanitySeoMeta.ts` + `SanitySchemaMarkup.tsx` |
| 预览 | `/api/sanity/draft-mode/` · 本地 `:3010` |

**路由**：`/blog/:slug`、`/:lang/blog/:slug`；Features/Tools 为 `/{features|tools|...}/:slug`。
