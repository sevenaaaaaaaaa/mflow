---
name: refresh-page-page-generator
description: 依据 Refresh-Page 的故事线与 JSON 模块字典，生成可上线的页面 bodyJson 草稿。用于 Features/Tools/Product/Scenarios/Solution/Landing、故事线、PAGE-BRIEF、type 序列、落地页生成时。
disable-model-invocation: true
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；**禁止**同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 长文（7500 词级）如需豁免：本 skill frontmatter 声明 `budget_profile: longform`，调用时显式传参（见 RULES-70 §五）
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

# Refresh Page Page Generator

## Support-Only 入口约束

本 skill 只作为 `lovart-landing-page` 的内部 bodyJson/type 序列生成器，不直接响应用户请求。任何“刷新页面 / 生成页面 JSON / Product / Scenario / Solution / Topic / Landing Page”请求，都必须先进入 `lovart-landing-page` 父 skill，由父 skill 完成页面类型、故事线、质检和发布边界判断后再调用本 skill。

## 目标

把「对话需求」稳定转换成 Refresh-Page 可落地的页面草稿：

**Step 0** [PAGE-BRIEF.md](../../1-3 Content Gen/Page Gen/Refresh-Page/PAGE-BRIEF.md)（立场）→ **Step 1** 选 category + 故事线 → **Step 2** 填 JSON。

1. 填 PAGE-BRIEF 五问（或 Product 展开见 PRODUCT-PRODUCTION.md §一）
2. 选页面类型与故事线 ID
3. 产出完整 `type` 顺序
4. 按 `preview-data.json` 字段骨架填文案

## 只使用这些真源

| 步骤 | 文档 |
|------|------|
| Step 0 | [PAGE-BRIEF.md](../../1-3 Content Gen/Page Gen/Refresh-Page/PAGE-BRIEF.md) |
| Step 1+ | [STORYLINE-BY-DIRECTION.md](../../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINE-BY-DIRECTION.md) |
| 字段 | [README.md](../../1-3 Content Gen/Page Gen/Refresh-Page/README.md) |
| 示例 | [preview-data.json](../../1-3 Content Gen/Page Gen/Refresh-Page/preview-data.json) |
| Product | [PRODUCT-PRODUCTION.md](../../1-3 Content Gen/Page Gen/Refresh-Page/PRODUCT-PRODUCTION.md) + `Pages/Products/en/` 案例 |

勿跳过 Brief 直接从 §4 复制 type 序列。

## 对话执行流程（必须按序）

### 第零步：Brief 确认单（Step 0）

若用户未给全，先补 PAGE-BRIEF 五问：流量目的、读者问题、内容主次、表达难度、与相邻页分工。

Product 页额外确认：官网 SEO vs 投放、能力/特色/功能主次、与 Scenario/Solution 边界。

### 第一步：确认输入

1. 页面类型（六选一）
2. 故事线 ID
3. 语言
4. Brief 摘要（来自 Step 0）
5. CTA 目标
6. 是否先只出 type 序列

### 第二步：故事线确认单

返回：页面类型、故事线 ID、完整 type 顺序、section 数、分叉点。

### 第三步：生成 JSON

- 顶层 `bodyJson` 数组（或 compositePage 整文档，含 `category`、`storyline`、`schemaVersion: composite-v2`）
- 字段名严格来自 README + preview-data
- Product 参考：`chatcanvas-en.json`（能力+标准）、`brand-kit-en.json`（特色+含社会证明）

### 第四步：自检

- type 顺序与故事线一致
- Product 禁用模块未出现（`prompt-launcher` 等）
- FAQ/定价/证言按故事线包含
- `seo.noIndex: true` 直到用户授权 SEO 上线

## 发布（Product）

生成后走 **`lovart-product-sanity-publish`** Skill：`preflight` → `import-page.js --dry-run` → `--import`。

## 强约束

- 每个分叉/变体 = 独立故事线
- 不发明 README 不存在的 `type`
- 先 Brief + 故事线确认，再写 JSON
