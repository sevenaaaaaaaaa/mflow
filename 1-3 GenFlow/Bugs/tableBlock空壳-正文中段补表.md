## tableBlock 正文中段缺表 — 2026-08-05

### 结论
已补 **22** 个「正文中段 + Content Calendar 可对齐」空壳（目标语重写 `rows`，完整性门禁通过）。FAQ/附录/Related、错位标题槽位不补。

### 本批结果（OK=22）
- DE 2：`brand-kit-farmer-market` / `brand-kit-food-market` 排版表
- FR 7：comic/dog-trainer/farmer/food/hvac/wine/pet-supply 排版表
- ES 1：`how-to-create-sketches-doodles-ai` 翻车修复表
- PT 5：record/comic/pediatrician/pet-supply/wine 排版表
- RU 1：`how-to-turn-photo-into-anime-cartoon-ai` 风格要求表
- IT 3：batch-content 耗时对比 / shorts 产能 / virtual staging 成本
- KO 3：farmer 排版 + FB cover formula + collage 三工具对比

### 刻意跳过（错位）
- DE `step-by-step-ad-creatives@30`（标题讲速度，MD 是 CTA 变体）
- DE/RU `complete-guide-ai-avatar@45`（落在 FAQ/3D 问答区）

### Memo
`~/Documents/Lovart Local Dev/Output/QA-Memo/tableblock-*-expand-batch*-2026-08-05.json`（phase=`mid-content-fill`）

### 方法
1. 排除 FAQ / Image Appendix / Related
2. 标题语义对齐 EN MD（排版标题 ↔ Typography Recommendations；或单空壳+单 MD 表）
3. 目标语重写后只写目标 `tableBlock.rows`（整 body set + fingerprint 门禁）

---

## 兄弟语补齐批次（2026-08-05 续）

### 结论
同 slug「兄弟已填、本语中段仍空」**严格矩形表**可对齐极少（EN 几乎无 tableBlock；多数兄弟表被压成单行 appendix）。本批共补 **5**：

| 语 | slug | 来源 |
|---|---|---|
| FR | brand-kit-pediatric-dentist @13 | DE 排版表重写 |
| IT | 04-cluster-ai-logo-vs-human-designer @86 | EN 定价对比重写 |
| KO | brand-kit-jewelry-designer @9 | MD 色板（兄弟有压扁表可确认槽位） |
| FR | fall-collection-visual-strategy-2027 @28 | DE 色板解压+法语重写 |
| FR | logo-design-guide @29 | 兄弟色联想表解压+法语重写 |

### 瓶颈
- 中段空壳 ~510，其中排版/色板标题仅个位数
- 兄弟「已填」常为 Image/Alt Text 或 `\n` 压扁单行，不能直接抄
- 脚本：`~/Documents/Lovart Local Dev/scripts/active/fill_tableblock_sibling_mid.py`
- Memo：`tableblock-*-sibling-mid-2026-08-05.json`
