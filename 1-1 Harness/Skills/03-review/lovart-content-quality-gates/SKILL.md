---
description: 内容质量门禁系统（三层 L1/L2/L3）。质检唯一父入口。
---
## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-content-quality-gates/SKILL.md` |

# Lovart 内容质量门禁（Quality Gates）

**发布策略（先于 preflight）**：[`first-run-and-incremental-policy.md`](../lovart-sanity-publish/references/first-run-and-incremental-policy.md) · **换设备**：[`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](../lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)

**执行脚本（可自动化）**：`1-4 Dev/lovart.sanity.studio/scripts/preflight-content.js`  
**认证检查**：`node scripts/check-publish-deps.js` → [`sanity-cli-setup.md`](../lovart-sanity-publish/references/sanity-cli-setup.md)  
**Taxonomy**：[`blog-taxonomy-sync.md`](../lovart-sanity-publish/references/blog-taxonomy-sync.md)  
**人工深度审计（Blog 长文）**：[`lovart-content-audit`](../lovart-content-audit/SKILL.md)  
**Blog 发布**：[`lovart-sanity-publish`](../lovart-sanity-publish/SKILL.md)  
**兼容别名**：[`lovart-sanity-preflight`](../lovart-sanity-preflight/SKILL.md)（已合并到本 Skill，勿重复维护命令表）

## Triggers

- 「质量检查」「preflight」「发布前验证」「SEO 检查」「URL 检查」
- 创建 / 翻译 / 更新 Tools、Features JSON 或 Blog MD 之后
- `dataset import` **之前**（与 convert dry-run 并列）

## 生命周期：何时跑哪一层

| 阶段 | 必跑 | 命令 / Skill |
|------|------|----------------|
| **FIRST-RUN** 本机首次 Sanity 发布 | 认证 + 拉线上参照 | [`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行`](../lovart-sanity-publish/references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md) + `check-publish-deps` |
| **CREATE** 生成 JSON/MD 后 | L1 结构 + i18n 文件名 | `preflight-content.js --type tools\|features\|blog-md` |
| **TRANSLATE** 翻译落盘后 | L1 + marker 清零 | 同上 + `grep section_` 为 0 |
| **UPDATE** 改 slug/SEO/链接后 | L1 + URL（可选） | `--check-urls` |
| **PRE-PUBLISH** convert 后 import 前 | L1 + NDJSON | `--ndjson "$HOME/Documents/Lovart Local Dev/Temp/lovart/import-*.ndjson"` |
| **POST-PUBLISH** import 后 | L2 落库抽查 + Studio | Blog：`verify-blog-publish.js`；compositePage：`verify-composite.js --sample 20` |
| **DEEP QA** Blog 长文上线前 | L3 全文审计 | `lovart-content-audit` |

**日常 import 默认**：`--missing` only；本地已有且线上已有同 `_id` → **不**全量重发（除非用户明确要求）。

```text
FIRST-RUN → CREATE → TRANSLATE → UPDATE → [preflight L1] → convert（限定范围）→ [preflight NDJSON] → import --missing → GROQ
```

---

## L1 — 自动化预检（preflight-content.js）

```bash
cd "…/1-4 Dev/lovart.sanity.studio"

# Tools（composite-v2 only，正式源 Page Gen/Pages/Tools）
node scripts/preflight-content.js --type tools --strict
node scripts/preflight-content.js --type features --lang en,ja

# Features v2 / 其他 composite 草稿目录
node scripts/preflight-content.js --type composite-v2 --dir "../Pages/drafts/composite-v2/Features/en"
node scripts/preflight-content.js --file "../1-3 Content Gen/Page Gen/Pages/Tools/en/{slug}-en.json"

# 单篇 Features（自动识别 legacy / v2）
node scripts/preflight-content.js --file "../Pages/Features/en/foo-en.json" --composite-v2

# Blog Markdown（Content Calendar）
node scripts/preflight-content.js --type blog-md

# import 前 NDJSON
node scripts/preflight-content.js --ndjson "$HOME/Documents/Lovart Local Dev/Temp/lovart/import-tools.ndjson"

# 随机 URL HTTP 抽查（推荐，默认抽 5 篇；不必每次全量）
node scripts/preflight-content.js --type tools --sample-urls 8

# 全量 URL（慢，仅大批量发布前偶尔使用）
node scripts/preflight-content.js --type tools --check-urls

# WARN 也视为失败（CI 严格模式）
node scripts/preflight-content.js --type tools --strict

# 机器可读报告（CI / Pipeline 汇总）
node scripts/preflight-content.js --type features --report "../../Output/Quality Reports/$(date +%Y-%m-%d)/preflight-features.json"
```

**退出码**：`0` 通过，`1` 有 BLOCK（`--strict` 时 WARN 也算失败），`2` 参数错误。

### language ↔ TDK 门禁（2026-08-04）

防回潮：`title` / `seo.title` / `description` / `seo.description` 必须与 `language` 对齐；拦截 EN 壳、`[IT]` 假本地化、合成模板句（如 `｜Lovart AI 设计工具`）。

```bash
# 推荐：Python 门禁（Studio 缺失时的可运行入口）
python3 "1-4 Dev/scripts/preflight_tdk_i18n.py" --file path/to/page-zh.json
python3 "1-4 Dev/scripts/preflight_tdk_i18n.py" --ndjson "$HOME/Documents/Lovart Local Dev/Temp/lovart/import.ndjson" --strict
python3 "1-4 Dev/scripts/preflight_tdk_i18n.py" --sanity --lang zh,ja,ko --limit 200

# Node：已挂入 anti-slop composite 检查
# lib: Skills/03-review/lovart-content-quality-gates/scripts/lib/tdk-i18n-gate.js
node "1-1 Harness/Skills/03-review/lovart-content-quality-gates/scripts/anti-slop-preflight.js" --file path/to/page.json --strict
```

BLOCK 码：`TDK_I18N_TITLE` / `TDK_I18N_DESC` / `TDK_I18N_EMPTY`。**import 前必须 BLOCK=0。**

### L1 检查维度（脚本已实现）

| 维度 | 代码 | BLOCK 示例 | WARN 示例 |
|------|------|------------|-----------|
| **i18n 语言** | `I18N_*` | `language` 非法；文件名 `-ja` 与 JSON 不一致 | `_index` 缺翻译语言 |
| **翻译 marker** | `I18N_MARKER` | body 含 `(section_de)` | — |
| **JSON 结构** | `JSON_*` | `bodyJson` 非数组、解析失败；`--strict` 下 v2 页含 legacy `type` | 未知 `type`；v2 页缺 `schemaVersion`；legacy 页混入 v2 `type` |
| **SEO 字段** | `SEO_*` | slug 含 `_`/空格/首尾 `/` | title/description 超长 |
| **UX 内容** | `UX_*` | 空 title/description/sections | 正文 placeholder；FAQ <3；无 CTA |
| **品牌词** | `UX_BRAND` | — | Lovart/MCoT/ChatCanvas 拼写错误 |
| **元数据** | `META_SOURCETYPE` | — | compositePage 缺/错 `sourceType` |
| **URL 契约** | `URL_*` | — | `url_path` 与 `lovart.ai/{lang}/tools/{slug}` 不一致 |
| **URL 可用性** | `URL_HTTP` | — | `--check-urls` 时 404（未发布可 WARN） |
| **资源 CDN** | `UX_CDN` | — | 图片非 `assets-persist.lovart.ai` |
| **MD 兼容** | `MD_*` | 无 frontmatter；坏内链模式 | 缺 `language` |

**Blog MD 坏链模式（BLOCK）**：`/博客文章/`、`/cluster/`、`.md)`、`](#)`、`](/)`

### slug 命名（Features / Tools / Blog）

- **必须 kebab-case**：`restaurant-menu-design` ✅ · `restaurant_menu_design` ❌ → `SEO_SLUG` BLOCK
- **文件名** `{slug}-{lang}.json` 与 JSON 内 `slug` 一致
- **Legacy 重复页**：若同主题已有 kebab slug，**删除**下划线版本地文件 + `_index` 条目，勿改 slug 留两篇；线上旧 URL 需 **301** 到 canonical（见 [`SOP-Lovart-Sanity-内容发布总指南` §4.5](../lovart-sanity-content-publish/SOP-Lovart-Sanity-内容发布总指南.md)）

```bash
rg '"slug": "[^"]*_[^"]*"' "../Pages/Features" "../1-3 Content Gen/Page Gen/Pages/Tools"
```

### compositePage bodyJson：legacy vs v2

| schema | 管道 | preflight |
|--------|------|-----------|
| **legacy** | 现网 Features 存量 | `--type features` |
| **v2（Tools 唯一）** | `Page Gen/Pages/Tools/` · `T-long` / T1–T5 / N5 | `--type tools --strict`（legacy → BLOCK） |
| **v2（Features 迁移中）** | `Pages/Features/` 或 drafts | `--type composite-v2` 或 `--composite-v2` |

- **Tools**：`convert-tools.js` 与 `--type tools` **仅 composite-v2**；legacy 须先 `legacy-to-composite.js` 迁移。
- 白名单 SSOT：`scripts/lib/legacy-to-composite.js` → `NEW_SECTION_TYPES`；故事线：`Refresh-Page/STORYLINES.md`。

---

## L2 — SEO 监测清单（人工 + 发布 Skill）

适用于 **Blog**（frontmatter）与 **compositePage**（`seo` 对象）。

| 字段 | Blog 建议 | compositePage 建议 | 严重级 |
|------|-----------|-------------------|--------|
| title / seo.title | ≤60–70 字，含主关键词 | ≤120 字 | BLOCK/WARN |
| description / seo.description | 150–170 字 | ≤300–500 字（schema excerpt ≤500） | WARN |
| keywords / seo.keywords | 3–8 个 | 同左 | WARN |
| ogImage | lovart CDN，1200×630 | 同左 | WARN |
| structuredData | 与页面类型一致 | FAQ 页用 FAQPage | WARN |
| noIndex | 生产环境应为 false | 同左 | WARN |
| slug | kebab-case，无 `/` 首尾 | 同左 | BLOCK |
| 多语言 | 同 slug + 不同 `_id`/`language` | `{id}-{lang}` | BLOCK |

**Blog 专项**（`lovart-sanity-publish`）：focus keyword 在 H1/前 100 词/H2；hreflang/canonical。

---

## L3 — 用户体验（UX）清单

| 检查项 | Tools/Features JSON | Blog MD |
|--------|---------------------|---------|
| Hero 有 CTA / button_link | `heroSection` / `contentSection`；`button_link` / `buttonLink` | 正文 CTA 链到 signup/pricing |
| FAQ ≥3 | `faqSection.faq` 或 v2 `faq.items`（preflight `UX_FAQ`） | ≥3 Q&A（preflight `UX_FAQ`） |
| 无空白 testimonial avatar | preflight `UX_AVATAR`（`avatar_url`） | — |
| suggestion 可读 | `label` 与 `value` 成对 | — |
| 可读性 | 段落长度、列表结构 | Flesch ≤12（audit） |
| 品牌词拼写 | preflight `UX_BRAND`（MCoT / ChatCanvas / Touch Edit） | 同左 |

---

## L3b — Anti-Slop（内容质量）

> 写作规范 SSOT：[1-1 GEO Readme/文档/04-质量治理/Anti-Slop.md](../../../1-1%20GEO%20Readme/文档/04-质量治理/Anti-Slop.md)

发布前自问：读者是谁、为什么现在读、读完改变什么、下一步是什么（四问）。

| 检查 | 工具 |
|------|------|
| 占位符 / 低信息密度 | `audit-content-quality.js`、`preflight` `UX_*` |
| EN 可读性 backlog | `en-readability-backlog.js` |
| Blog 深度审计 | `lovart-content-audit` |
| SERP 意图对齐 | `lovart-content-creation-orchestrator` Phase 0 SERP brief → Quality Gate BLOCK |

---

## L4 — URL 可用性（三类）

1. **契约 URL**（本地）：`url_path` 必须等于  
   `https://www.lovart.ai[/lang]/tools|features/{slug}` — L1 `URL_PATH`
2. **内链**（Blog）：`/blog/{slug}`，禁止旧路径 — L1 `MD_LINK` + `fix-blog-internal-links.py`
3. **线上 HTTP**（可选）：`--check-urls`；未发布草稿 404 记 **WARN** 而非 BLOCK

```bash
# Blog 内链修复（dry-run 优先）
python3 scripts/fix-blog-internal-links.py
```

---

## L5 — 多语言 / 本地化（创建·翻译·更新）

> 模块文档：[i18n-多语言.md](../../../1-1%20GEO%20Readme/文档/02-模块上手/i18n-多语言.md) · Studio：`npm run i18n:prepare|apply|verify|publish`

| 检查项 | 工具 |
|--------|------|
| 文件名 `{slug}-{lang}.json` 与 `language` 一致 | preflight `I18N_FILENAME` |
| 同 slug 各语言 `_id` 不同（`{id}-{lang}`） | convert 报告 duplicate _id |
| `_index.json` `missing_per_lang` | preflight `I18N_GAP` |
| 翻译后 section 数量一致 | `translate-features.py` 校验 |
| 禁止翻译字段未改 | `system_prompt`、`image_url`、`type` |
| pt/ru 批量同步 | `preflight-l0-pt-ru.sh` |
| 导入后 slug parity | GROQ（发布 Skill §5.2） |

**支持语言（Pages）**：`en de fr it ja ko pt ru zh-TW`  
**Blog 常见**：`en zh ja zh-TW` + 扩展 `pt ru`

---

## L6 — 代码 / 仓库健康（改脚本或 Studio 时）

| 检查 | 命令 |
|------|------|
| convert 脚本可运行 | `node scripts/convert-tools.js --dry-run` |
| 无 TS 语法进 .js | 勿在 `.js` 写 `Set<string>()` |
| NDJSON marker | `grep -c 'section_' "$HOME/Documents/Lovart Local Dev/Temp/lovart"/import-*.ndjson` → 0 |
| Studio schema 与数据集 | 唯一 SSOT：`1-4 Dev/lovart.sanity.studio` |
| Git 不误改 schema | `git status` 无 `schemaTypes/` |

---

## L7 — 合规与文化（深度）

**不重复实现** — 调用 [`lovart-content-audit`](../lovart-content-audit/SKILL.md) Dimension 3–4：

- GDPR / 广告法绝对化用语 / 地图领土 / 政治敏感
- `BLOCKED_PHRASES` 表

---

## 决策逻辑（与 Pipeline 对齐）

```text
IF preflight BLOCK > 0:
    → 停止 import；修复后重跑 preflight
IF preflight WARN only:
    → CONDITIONAL；用户确认后可 import
IF preflight OK AND lovart-content-audit PASS (Blog):
    → lovart-multi-platform-push / Sanity import
```

---

## 与各 Skill 的关系

| Skill | 质量职责 |
|-------|----------|
| **本 Skill** | L1 自动化 + 全维度清单索引 |
| `lovart-content-audit` | Blog 深度审计（合规/文化/可读性） |
| `lovart-landing-page` | 生成后 **必须** preflight |
| `lovart-tools/features-sanity-publish` | import 前 **必须** `--ndjson` preflight |
| `lovart-sanity-publish` | Blog NDJSON 字段 + CDN + 多语言 parity |
| `lovart-pipeline-orchestrator` | Step 3 后 L1；Step 4 audit；Step 5 前 NDJSON |

---

## 报告输出（建议）

```text
Output/Quality Reports/YYYY-MM-DD/
├── preflight-tools.txt        # tee stdout
├── preflight-features.json    # --report 机器可读
└── quality-summary.md         # BLOCK/WARN 汇总
```

保存方式：

```bash
node scripts/preflight-content.js --type tools 2>&1 | tee "../../Output/Quality Reports/$(date +%Y-%m-%d)/preflight-tools.txt"
node scripts/preflight-content.js --type features --report "../../Output/Quality Reports/$(date +%Y-%m-%d)/preflight-features.json"
```

---

## Anti-Bugs（禁止再犯）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md)

| ID | 本 Skill 门禁 |
|----|--------------|
| AB-P04 | marker `(section_xx)`：preflight WARN，勿手改 JSON；用 `repair-local-markers.js` |
| AB-P05 | category 规则只读 `scripts/lib/blog-taxonomy.js`，勿在 preflight 单独维护别名 |
| AB-S01 | `IMAGE PLACEHOLDER` 不进正文；convert 提取 `imageBriefs`（WARN 不 BLOCK 发布） |
| AB-S04 | `draft-*` 页跳过 preflight BLOCK / 生产验收 |
| AB-U01 | Features `url_path` / JSON-LD 须 `/features/`；preflight `URL_PATH` |
| AB-U02 | Blog 坏链 `/博客文章/`、`/cluster/` → `MD_LINK` BLOCK |
| AB-I01 | HTTP 404 替换用审计**精确 URL**；禁止 normalize `.png` 模糊匹配 |
| AB-I04/I05 | 大批发布后用 `audit-blog-covers.js` / `audit-composite-images-404.js` 复验 |
| AB-S06 | testimonial 空头像：`repair-testimonial-avatars.js`；默认 URL 须 HEAD 200 |
| AB-E05/E06 | 跑 preflight 前确认 `LOVART_ROOT` 与 Content Calendar / Pages 存在 |
| AB-U03 | 缺 slug 推断后发布前 GROQ 核对 `slug.current` |

**URL 探测**：日常用 `--sample-urls 8`；`--check-urls` 全量仅大批发布前偶尔使用（AB-A01：先小样本再扩大）。
