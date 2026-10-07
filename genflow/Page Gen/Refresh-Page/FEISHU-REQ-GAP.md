# 飞书 / PDF 原始需求 ↔ 当前交付 对照

> **权威来源**：[PAGE-MODULE-MATRIX.md](./PAGE-MODULE-MATRIX.md)（来自 `官网改版各类新增页面模块对照一览表.pdf`）  
> 飞书链接：https://resonate.feishu.cn/wiki/ZCEGwtD4ziXBxQk12lDco5k8nsh

---

## 对照结论（2026-05-31）

| 需求（PDF） | 当前本地文档 | 对齐？ |
|-------------|--------------|--------|
| 6 种页面：Product / Features / Scenarios / Solution / Tools / Landing Page | `FULL-STORYLINE-*` 按 Feature/Tool + O1–O4 | ❌ 框架错误 |
| 17 种模块本体，行序 = section 顺序 | 20 段 README One-each | ❌ 模块集不同 |
| 单元格数字 = **设计变体号** | V0001–V1200 笛卡尔积 | ❌ 变体体系错误 |
| 空白 / ❎ = 该场景不用此模块 | 满配 20 段全用 | ❌ |
| 按场景做最全落地页 + JSON + demo | 15 篇短链 F1/T1 草稿 | ⚠️ 部分完成，结构不对 |
| Hero 区分、模块备注 | 未 sistematize | ⏳ |
| Product/Solution 首屏找 R 老师 | — | 待人工 |

---

## 应以 PDF 为准的下一步

1. 以 **PAGE-MODULE-MATRIX.md §4** 为 6 条主故事线。  
2. 做 **1 条最全 demo JSON**（建议 Landing Page 或合并各列模块）。  
3. 与前端确认 **§5 映射表**（PDF 模块 → `bodyJson` type）。  
4. 废弃或标注过时：`FULL-STORYLINE-ORDERS.md`、`FULL-STORYLINE-VARIANTS.md` 的编号体系。

---

## 飞书 §A（原文摘录）

见 [PAGE-MODULE-MATRIX.md](./PAGE-MODULE-MATRIX.md) 全文。
