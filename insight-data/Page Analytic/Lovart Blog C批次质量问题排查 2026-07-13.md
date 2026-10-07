---
type: audit-report
scope: sanity-blog-c-batch
date: 2026-07-13
status: reviewed
project: lovart
dataset: production
---

# Lovart Blog C批次质量问题排查 2026-07-13

## 结论

本轮按 `C_long_tail_low_value_review` 队列全量复扫，共核验 `130` 篇英文 published Blog。

- 正文字符数 `=0`：`0`
- 正文字符数 `<2000`：`0`
- 正文字符数 `<4000`：`0`
- 存在占位符或禁用词命中：`10`
- 存在可见占位符（本轮全部出现在 description）：`7`
- 缺少 signal refresh 强制结构块：`70`
- 脏标题 / 异常 slug：`2`
- 去重后需处理问题文档总数：`71`

结论很明确：`C` 批次现在**不是空壳问题**，而是以**结构块缺失**为主，辅以少量 **PLACEHOLDER 描述残留**、**禁用词残留** 与 **个别标题/slug 异常**。

## 主问题分组

### 1. 缺结构块

共 `70` 篇。

- 其中 `57` 篇缺：
  - `Derivative Scenarios`
  - `E-E-A-T Notes`
  - `Internal Links`
  - `Image Appendix`

- 其中 `13` 篇缺：
  - `Derivative Scenarios`
  - `E-E-A-T Notes`
  - `Image Appendix`

这类最适合批量修复，因为问题模式高度一致。

### 2. 可见占位符（description）

共 `7` 篇，全部是 `description` 中残留 `PLACEHOLDER`：

- `case-study-ecommerce-upscaled-product-images-ai`
- `ai-avatar-tools-compared`
- `ai-face-swap-tools-compared`
- `case-study-novelist-consistent-character-ai`
- `case-study-real-estate-ai-interior-staging`
- `case-study-video-producer-ai-model-selection`
- `year-in-review-design-templates`

### 3. 正文禁用词残留

共 `5` 篇：

- `case-study-ecommerce-upscaled-product-images-ai` → `unlock`, `leverage`
- `complete-guide-ai-video-model-selection-2026` → `leverage`
- `year-in-review-design-templates` → `unlock`
- `shutterstock-ai-vs-lovart` → `seamless`
- `https-www-lovart-ai-zh-blog-human-ai-cocreation-lovart-canvas-solopreneur-design` → `empower`

### 4. 脏标题 / 异常 slug

共 `2` 篇：

- `best-ai-image-generator-for-photorealism-2026`
  - 标题：`Best Ai Image Generator: AI-Powered Creation Tool 2026 | Lov`
  - 问题：明显截断

- `https-www-lovart-ai-zh-blog-human-ai-cocreation-lovart-canvas-solopreneur-design`
  - 标题：`Ai Cocreation Lovart Canvas Solopreneur Design`
  - 问题：slug 异常，像 URL 转写残留

## 建议修复顺序

建议按下面 3 组批量推进：

### 第一组：结构块批量补齐

目标：`70` 篇  
动作：统一补 `Derivative Scenarios` / `E-E-A-T Notes` / `Internal Links` / `Image Appendix`，并保留现有正文主体。

### 第二组：PLACEHOLDER + 禁用词清洗

目标：`10` 篇  
动作：

- 改写 `description`
- 清理正文内 `unlock` / `leverage` / `seamless` / `empower`

### 第三组：脏标题 / 异常 slug 单独修

目标：`2` 篇  
动作：

- 修标题
- 对异常 slug 文档单独判断是否只修标题，还是要另做 canonical URL/slug 善后

## 过程产物

- 审计缓存：`tmp/c-batch-problem-audit.json`
- 长度快照：`tmp/c-batch-current-lengths.json`
