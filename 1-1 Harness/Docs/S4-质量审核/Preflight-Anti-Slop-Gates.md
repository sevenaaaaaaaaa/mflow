# Preflight Anti-Slop Gates — 自动门禁映射

> 用途：把 [Content-Quality-Rubric](./Content-Quality-Rubric.md) 与 [Content-Production-Ledger](./Content-Production-Ledger.md) 中可自动检测项，映射到 preflight 错误码与严重级。  
> 上游：Rubric、Ledger、Anti-Slop  
> 实现：`1-1 Harness/Skills/lovart-content-quality-gates/scripts/anti-slop-preflight.js`  
> 目标合并：`1-4 Dev/lovart.sanity.studio/scripts/preflight-content.js`

---

## 1. 分层

| 层 | 工具 | 时机 |
|---|---|---|
| **L1 结构** | `preflight-content.js` | slug、i18n、JSON、SEO 长度、URL |
| **L1b Anti-Slop** | `anti-slop-preflight.js` | 占位符、空泛词、薄 H2、缩水、FAQ/CTA |
| **L3 深度** | `lovart-content-audit` | 合规、文化、可读性、TF-IDF |

L1b 不替代 L3；它挡住最明显的 AI slop 与结构缩水，再交人工/Rubric 细评。

---

## 2. 错误码表

### 2.1 已有（preflight-content.js）

| 码 | 严重级 | 检测 |
|---|---|---|
| `I18N_MARKER` | BLOCK | `(section_xx)` |
| `MD_LINK` | BLOCK | `/博客文章/`、`/cluster/`、`.md)`、`](#)`、`](/)` |
| `UX_PLACEHOLDER` | BLOCK/WARN | 正文 placeholder |
| `UX_FAQ` | BLOCK | FAQ < 3 |
| `UX_CTA` | BLOCK | 无 CTA |
| `UX_BRAND` | WARN | MCoT / ChatCanvas 拼写 |

### 2.2 新增（anti-slop-preflight.js）

| 码 | 严重级 | Rubric/Ledger 来源 | 检测逻辑 |
|---|---|---|---|
| `AS_BANNED_PHRASE` | WARN | Anti-slop 语言 | 命中 1–2 个空泛词 |
| `AS_BANNED_DENSITY` | WARN / BLOCK (`--strict`) | Anti-slop 语言 | 空泛词 ≥3（Blog）或 ≥4（Page） |
| `AS_GENERIC_H2` | WARN | Blog Rubric | H2 为 Benefits/总结/Part N |
| `AS_THIN_H2` | WARN | Ledger H2 密度 | H2 下 < 80 词 |
| `AS_LOW_DENSITY_H2` | WARN | Ledger 五项 | 长段但密度分 < 2 |
| `AS_H2_COUNT` | WARN | 结构 | 长文 H2 < 3 |
| `AS_SHRINKAGE` | WARN / BLOCK (`--strict`) | Ledger 30/40/30 | 后 30% 密度低于前 30% |
|| `AS_HERO_IO` | WARN | Landing Rubric | Tool 页 hero 未体现输入/输出 |
|| **`BODY_NOT_PORTABLE_TEXT`** | **BLOCK** | AB-LP22 | Blog `body` 非 Portable Text 数组（为 Markdown 字符串）。检测：`body[0]._type == null`。GROQ 查询：`count(*[_type=="blog" && length(body) > 0 && body[0]._type == null])`。**修复**：解析 Markdown 后生成 Portable Text 结构（`##`→h2，`###`→h3，段落→normal，列表→listItem）并 patch。**不修复不可发布**——前端 Portable Text 渲染器遇到字符串直接报 `Unknown block type "undefined"`，正文完全不可见。 |
|| **`SD_EMPTY_JSON`** | **BLOCK** | AB-LP23 | Blog 或 compositePage 的 `seo.structuredData.json` 为 null 或空字符串。全站扫描：`count(*[seo.structuredData.json==null || seo.structuredData.json==""])`。 |
|| **`SD_WRONG_TYPE`** | **BLOCK** | AB-LP23 | Blog `seo.structuredData.json` 内 `@type` 不为 `Article`/`BlogPosting`（当前全站为 `WebPage`，导致 Google 不展示 Article rich results）。compositePage tool/feature @type 建议 `WebPage`+`mainEntity.SoftwareApplication`。 |
|| **`SD_MISSING_FIELDS`** | **BLOCK** | AB-LP23 | Blog Article 必缺字段：`headline`（非 `name`）、`author`、`datePublished`、`image`。 |
|| **`SD_TEMPLATE_LEAK`** | **WARN** | AB-LP23 | compositePage description 跨页面模板串用（如 nano-banana 出现 avatar 描述）。 |

`[待考证]`：WARN，不 BLOCK（允许显式标注未核实事实）。

---

## 3. 空泛词表（SSOT）

维护于 `scripts/lib/anti-slop-rules.js`：

**EN**：unlock, revolutionize, seamless, empower, game-changer, cutting-edge, leverage, AI-powered platform, in today's fast-paced, the future of …

**ZH**：赋能、闭环、颠覆性、革命性、一站式解决方案、在当今快节奏、解锁…潜力、无缝衔接、未来可期、综上所述

**JA**：革新的な、シームレス、ワンストップ、今後に期待

舆情/SEO 反馈后在此文件增删，勿在多处维护。

---

## 4. 缩水检测（30/40/30）

与 Ledger §6 对齐的启发式（非 LLM）：

1. 按字符将正文分为前 30% / 中 40% / 后 30%。
2. 每段密度分 0–3：数字、举例词、因果/机制词、长度。
3. **BLOCK/WARN 条件**（`--strict` 时 BLOCK）：
   - 后 30% 得分 < 2
   - 后 30% < 前 30%
   - 中段明显高于后段（中段 ≥2 且后段比中段低 2 分以上）

短文（< 2000 字符）跳过缩水检测；FAQ 尾段不参与后 30% 计分。

---

## 5. 命令

### 5.1 独立运行（Harness，立即可用）

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"

# 单篇 Blog
node anti-slop-preflight.js --file "../../../1-3 Content Gen/Content Calendar/01-How-To/example.md"

# 单篇 Tools JSON
node anti-slop-preflight.js --file "../../../1-3 Content Gen/Page Gen/Pages/Tools/en/example-en.json"

# 目录批量
node anti-slop-preflight.js --dir "../../../1-3 Content Gen/Content Calendar/01-How-To" --glob "*.md"

# CI 严格模式（WARN 也算失败）
node anti-slop-preflight.js --file article.md --strict --report "../../Output/Quality Reports/$(date +%Y-%m-%d)/anti-slop.json"
```

退出码：`0` 通过，`1` 失败，`2` 参数错误。

### 5.2 与 studio preflight 串联（推荐发布前）

```bash
cd "1-4 Dev/lovart.sanity.studio"

node scripts/preflight-content.js --type blog-md --strict
node ../1-5\ Harness/Skills/lovart-content-quality-gates/scripts/anti-slop-preflight.js \
  --dir "../../1-3 Content Gen/Content Calendar" --glob "*.md" --strict
```

### 5.3 合并到 preflight-content.js（待办）

在 `preflight-content.js` 的 Blog / composite 检查路径中：

```javascript
const antiSlop = require('../../1-1 Harness/Skills/lovart-content-quality-gates/scripts/lib/anti-slop-rules.js')

// Blog MD path
const r = antiSlop.checkBlogMarkdown(md, { strict: opts.strict, language })
for (const i of r.issues) {
  if (i.severity === 'BLOCK') block(i.code, i.message, rel)
  else warn(i.code, i.message, rel)
}

// composite JSON path
const r2 = antiSlop.checkCompositePage(page, { strict: opts.strict })
// same loop
```

合并后 `anti-slop-preflight.js` 仍保留，供 Content Calendar 快速抽检。

---

## 6. 生命周期

```text
SERP brief → Ledger → 撰写 → anti-slop-preflight (CREATE)
       → preflight-content (TRANSLATE / PRE-PUBLISH)
       → Rubric 人工/Agent 评分
       → lovart-content-audit (DEEP QA)
```

| 阶段 | 必跑 |
|---|---|
| CREATE 长文/Blog 成稿后 | `anti-slop-preflight.js` |
| TRANSLATE 后 | `preflight-content.js` + marker 检查 |
| PRE-PUBLISH | 两者 `--strict` |
| DEEP QA | Rubric + content-audit |

---

## 7. 与 Rubric BLOCK 的对应

| Rubric BLOCK | 自动码 |
|---|---|
| 可见占位符 | `UX_PLACEHOLDER` |
| 坏内链 | `MD_LINK` |
| FAQ 模板凑数 | 部分 `UX_FAQ`（仅数量） |
| 后 30% 缩水 | `AS_SHRINKAGE` |
| 空泛 AI 腔 | `AS_BANNED_*` |
| Tool 首屏无输入输出 | `AS_HERO_IO`（WARN，人工复核） |
| 编造事实 | 不自动 — 人工 / `[待考证]` |

---

## 8. 维护

- 空泛词：每月根据舆情 + SERP 样本更新 `anti-slop-rules.js`。
- 阈值：`AS_BANNED_DENSITY` 命中次数、H2 最小字数可在脚本顶部配置。
- 样本库：[Content-Sample-Library.md](./Content-Sample-Library.md) — 好稿/坏稿标注用于校准本表阈值。

```bash
cd "1-1 Harness/Skills/lovart-content-quality-gates/scripts"
node sample-library-cli.js calibrate
```
