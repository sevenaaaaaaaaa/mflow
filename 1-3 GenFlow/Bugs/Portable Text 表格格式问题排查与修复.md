## 会话汇总：Portable Text 表格格式问题排查与修复

> **2026-08-03 纠偏**：上一轮「五层 tableCell」结论与已部署 schema 冲突。以下以 schema / 生产样本为准。

---

### 一、对应的质量问题

| # | 问题 | 严重级 | 根因 |
|---|------|:------:|------|
| Q1 | Blog 正文表格上传 Sanity 后前端渲染丢格式 | BLOCK | 转换器产出的 cells 形态与 schema 不符（object / tableCell / 缺 `_key`） |
| Q2 | 表格 block 缺 `_key`（table / tableRow） | BLOCK | 历史脚本未写 `_key` |
| Q3 | 多脚本内联错误转换函数 | BLOCK | 各写各的 `md_to_pt()`，与 SSOT 背离 |
| Q4 | 「五层 tableCell」误修 | BLOCK | 通用 Sanity 文档被当成 Lovart 规范；`o11tm2qe` **无** `tableCell` 类型 |

---

### 二、Schema 真相（SSOT）

已部署 schema：`tableRow.cells` = **`string[]`**。

合法形态：

```json
{
  "_type": "table",
  "_key": "...",
  "rows": [
    {"_type": "tableRow", "_key": "...", "cells": ["列1", "列2"]}
  ]
}
```

生产可渲染样本（pillar ja 等）全部是 string cells。仍存在历史 `cells: block` 对象污染。

---

### 三、修复手段（已落地）

1. **SSOT 纠正** — `~/Documents/Lovart Local Dev/scripts/md_to_portable_text.py`
   - 表格输出改为 string cells
   - 新增 `validate_portable_text_body` / `count_key_issues`
2. **门禁** — `validate_pt_body.py`（NDJSON / body JSON，BLOCK>0 停）
3. **脚本统一** — 内联转换器改为 import SSOT；batch 脚本 path 指向 Local Dev
4. **知识沉淀**
   - `lovart-blog-signal-writer/references/portable-text-table-syntax.md`
   - Pitfall #62（skill）
   - RULE 9 纠偏（`1-2 Insight/AGENTS.md`）
   - `TOOLS-REGISTRY.md` Blog PT 铁律
5. **审计报告** — `1-2 Insight/审计报告/2026-08-03-portable-text-table-audit.md`

---

### 四、残留风险

| 风险 | 说明 | 概率 |
|------|------|:----:|
| 生产存量 object-cell | ko/zh 等 review 文仍有 block cells | 高（待批量归一） |
| HAND_PT 散落脚本 | Temp/_patch_/gen_payloads 手拼 blocks，不含表格时风险较低 | 中 |
| CDN 缓存 | 修完后旧页需 revalidate | 中 |

---

### 五、还能做哪些

1. 生产存量 object-cell → string[] 批量 dry-run patch
2. pre-commit 阻断新增 `def md_to_pt`
3. CDN revalidate 提醒

**当前状态**：转换 SSOT + 门禁 + 规范已按 schema 纠正；生产存量 16 篇 object-cell 已于 2026-08-03 dry-run→apply 清零（`object_cell_docs=0`）。CDN revalidate 仍可选。



----

The full list is long (307 fixed). Let me give you the focused summary with the 16 broken URLs as hyperlinks, plus note the fixed count.

## 排查结果汇总

**线上审计范围**：323 篇含表格的 blog（Sanity 生产库全量扫描）

| 状态 | 数量 | 说明 |
|------|:----:|------|
| ✅ 已修复/结构合规 | 307 | cell `_type` 正确为 `tableCell`，五层 `_key` 完整 |
| ❌ 待修复 | 16 | cell `_type` 错误（用了 `block` 而非 `tableCell`），前端渲染丢格式 |

---

### ❌ 待修复（16 篇，需重新 patch body）

| # | URL |
|---|-----|
| 1 | https://www.lovart.ai/ko/blog/luma-dream-machine-review |
| 2 | https://www.lovart.ai/zh-TW/blog/stable-video-diffusion-review |
| 3 | https://www.lovart.ai/zh/blog/adobe-firefly-review |
| 4 | https://www.lovart.ai/ko/blog/adobe-firefly-review |
| 5 | https://www.lovart.ai/ko/blog/stable-video-diffusion-review |
| 6 | https://www.lovart.ai/de/blog/stable-video-diffusion-review |
| 7 | https://www.lovart.ai/es/blog/step-by-step-ai-design-replace-photoshop-25-types |
| 8 | https://www.lovart.ai/de/blog/luma-dream-machine-review |
| 9 | https://www.lovart.ai/ru/blog/adobe-firefly-review |
| 10 | https://blogs.lovart.ai/best-vidu-ai-alternatives |
| 11 | https://www.lovart.ai/ja/blog/best-vidu-ai-alternatives |
| 12 | https://www.lovart.ai/ko/blog/best-vidu-ai-alternatives |
| 13 | https://www.lovart.ai/zh/blog/best-vidu-ai-alternatives |
| 14 | https://www.lovart.ai/zh-TW/blog/best-vidu-ai-alternatives |
| 15 | https://www.lovart.ai/ja/blog/stable-video-diffusion-review |
| 16 | https://www.lovart.ai/ja/blog/luma-dream-machine-review |

---

### ✅ 已修复（307 篇，结构合规）

这 307 篇的表格结构已经正确（`tableCell` + 五层 `_key`）。完整 URL 列表已保存到 `/tmp/good_table_blogs.json`，需要我导出成文件或打印前 50 条吗？

---

**下一步建议**：对这 16 篇跑批量修复脚本（用修复后的 `md_to_portable_text` 重新转换其 markdown 源 → `createOrReplace`）。源文件在 `Output/Content Calendar/` 或 `Output/Lovart-Blog-Pipeline/` 下对应 slug。要我直接写修复脚本并跑这 16 篇吗？