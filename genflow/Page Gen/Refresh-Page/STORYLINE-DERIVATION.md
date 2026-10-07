# 故事线派生规则与清单

> ⚠️ **已过时**：文中「PDF 变体号」不是上线选型依据。请以 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) + [README-MODULE-VARIANTS.md](./README-MODULE-VARIANTS.md) 为准。

---

## 1. 我理解的规则（与你确认一致）

```
大方向（PDF 列） → 决定「这页用哪些本体、按什么顺序」
模块本体（PDF 行） → 每页里的一段 section
变体 → 同一本体的不同设计稿编号

派生规则：
  ① PDF 单元格只有一个数字     → 该方向「基准故事线」里该本体用此变体
  ② PDF 单元格有两个数字       → 派生两条故事线（其余本体相同，仅该本体变体不同）
  ③ PDF 有缩略图但无数字（✓*） → 不当作变体 1；该本体有未编号变体 → 每条派生一条故事线
  ④ PDF 空白 / ❎               → 该方向不出现此本体
  ⑤ Hero Banner                 → PDF 均标 1，但顶部要求「Hero 区分」→ 另维度派生（见 §5）
```

**一条故事线** = 某个大方向下，按 PDF **行序**排列的 `(本体 → 变体)` 列表（只含该方向启用的本体）。

---

## 2. 优先：六种大方向（PDF 列）

| 代号 | 大方向 | PDF 优先级 | 启用本体数（约） |
|------|--------|------------|------------------|
| **DIR-P** | Product | 今晚找 R（首屏） | 10（含 3 个无号派生） |
| **DIR-F** | Features | 标准功能页 | 12 |
| **DIR-SC** | Scenarios | **黄色高亮** | 11 |
| **DIR-SL** | Solution | **黄色高亮**，今晚找 R | 12 |
| **DIR-T** | Tools | 工具页 | 13 |
| **DIR-LP** | Landing Page | 最全 demo 候选 | 12（含 1 个无号派生） |

---

## 3. 优先：十七种模块本体（PDF 行序 = section 顺序）

| 序 | 本体 ID | PDF 名称 | 说明 |
|----|---------|----------|------|
| M01 | `hero` | Hero Banner | 首屏 |
| M02 | `multi` | Multi columns | 多栏 |
| M03 | `tab` | Tab Card | Tab 卡 |
| M04 | `cardgrid` | Card Grid | 卡片网格 |
| M05 | `featurecard` | Feature Card | 特性大卡 |
| M06 | `gallery` | Gallery | 图库 |
| M07 | `tryprompt` | Try Prompt | 试用输入 |
| M08 | `photoloop` | Photo loop | 图片/Logo 条 |
| M09 | `cta` | CTA | 页内 CTA |
| M10 | `howtos` | How-tos | 步骤教程 |
| M11 | `vstable` | vs table | 对比 |
| M12 | `cluster` | Content Cluster | 内容簇 |
| M13 | `dynamic` | Dynamic Content | 动态图文 |
| M14 | `testimonial` | Testimonial | 证言 |
| M15 | `pricing` | Pricing Table | 定价 |
| M16 | `faq` | FAQ | 问答 |
| M17 | `bottomcta` | Bottom CTA | 底部 CTA |

---

## 4. 各方向 · 基准故事线 + 派生故事线

写法：`本体【变体号】`；`本体【派生-XX】` = PDF 有图无号，**禁止写变体 1**。

### DIR-F · Features（1 条，无派生）

**F-基准**

| 序 | 本体 | 变体 |
|----|------|------|
| M01 | hero | 1 |
| M02 | multi | 3 |
| M03 | tab | 2 |
| M05 | featurecard | 4 |
| M10 | howtos | 4 |
| M11 | vstable | 7 |
| M12 | cluster | 5 |
| M13 | dynamic | 6 |
| M14 | testimonial | 8 |
| M15 | pricing | 9 |
| M16 | faq | 11 |
| M17 | bottomcta | 12 |

---

### DIR-SC · Scenarios（1 基准 + 1 派生 = **2 条**）

**差异点：** M03 Tab — PDF 同时给出 **3** 与 **9** → **两条故事线**，不是同一页叠两个 Tab。

| 故事线 ID | M03 tab 变体 | 其余与基准相同 |
|-----------|--------------|----------------|
| **SC-基准** | 3 | ✓ |
| **SC-派生-tab9** | **9** | ✓ |

**SC-基准 / SC-派生-tab9 共用段（除 tab 外）：**

M01 hero【1】→ M02 multi【2】→ M03 tab【3 或 9】→ M05 featurecard【6】→ M10 howtos【4】→ M11 vstable【6】→ M12 cluster【5】→ M13 dynamic【8】→ M14 testimonial【8】→ M16 faq【10】→ M17 bottomcta【11】

---

### DIR-SL · Solution（1 条）

**SL-基准：** M01【1】→ M02【2】→ M03【3】→ M05【3】→ M10【5】→ M11【9】→ M12【4】→ M13【10】→ M14【7】→ M15【11】→ M16【9】→ M17【10】

---

### DIR-T · Tools（1 基准 + 1 派生 = **2 条**）

**差异点：** M12 Content Cluster — PDF **4** 与 **12** → **两条故事线**。

| 故事线 ID | M12 cluster 变体 |
|-----------|------------------|
| **T-基准** | 4 |
| **T-派生-cluster12** | **12** |

**T-基准 / T-派生-cluster12 共用段（除 cluster 外）：**

M01【1】→ M02【2】→ M05【3】→ M07【6】→ M08【7】→ M09【8】→ M10【4】→ M11【3】→ M12【4 或 12】→ M13【11】→ M16【13】→ M17【14】

---

### DIR-P · Product（1 基准 + 3 派生 = **4 条**）

**有图无号（禁止变体 1）：** M08 Photo loop、M14 Testimonial、M15 Pricing — 各 **派生一条故事线**。

| 故事线 ID | 派生说明 |
|-----------|----------|
| **P-基准** | 仅 PDF **有数字**的本体 |
| **P-派生-photoloop** | 在完整序中 M08 使用 **【派生-P8】**（待设计稿补号） |
| **P-派生-testimonial** | M14 使用 **【派生-P14】** |
| **P-派生-pricing** | M15 使用 **【派生-P15】** |

**P-基准（有号段）：**  
M01【1】→ M02【2】→ M03【3】→ M04【4】→ M10【5】→ M11【6】→ M12【7】→ M13【10】

**P-完整序（含无号本体，供派生线填入）：**  
M01【1】→ M02【2】→ M03【3】→ M04【4】→ M10【5】→ M11【6】→ M12【7】→ **M08【派生-P8】** → M13【10】→ **M14【派生-P14】** → **M15【派生-P15】**

- **P-派生-photoloop** = 完整序，且仅 M08 为派生位（P14/P15 若基准未定义可仍标派生待填）  
- **P-派生-testimonial** = 完整序，突出 M14【派生-P14】  
- **P-派生-pricing** = 完整序，突出 M15【派生-P15】  

（三条派生线 **互不合并**；设计稿补号后把 `派生-P8` 改成正式编号即可。）

---



> **2026-06-07 更新：** Landing Page 已扩展为 **7 条故事线**（6 投放 + 1 满配 demo）。  
> 本节 DIR-LP 的 2 条为早期 PDF 推导，**上线选型以 [`landing-storylines.json`](./landing-storylines.json) + STORYLINE-BY-DIRECTION §4.6 为准**。

### DIR-LP · Landing Page（1 基准 + 1 派生 = **2 条**）

**有图无号：** M13 Dynamic Content → **【派生-L13】**

| 故事线 ID | M13 dynamic |
|-----------|-------------|
| **LP-基准** | 其余有号；M13 暂不启用或待派生 |
| **LP-派生-dynamic** | **【派生-L13】** |

**LP-基准（M13 以外有号）：**  
M01【1】→ M02【2】→ M03【6】→ M04【5】→ M05【8】→ M06【9】→ M10【4】→ M11【10】→ M12【7】→ M16【12】→ M17【13】

**LP-派生-dynamic（完整序）：**  
同上，在 M12 与 M16 之间插入 M13【派生-L13】

---

## 5. 横切派生：Hero 区分（PDF 另要求）

PDF 矩阵里 Hero 均写 **1**，但 PDF 顶部要求 **Hero 区分**。  
Hero 不作为「变体 1」，而是 **每条故事线可再派生 Hero 变体**（与设计稿 H1–H5 对齐，待 R 老师 / 设计确认）。

| 派生维度 | 说明 |
|----------|------|
| **×H1…H5** | 任一条 `*-基准` 或 `*-派生-*` 均可复制 5 份，仅 M01 hero 换设计 |

**暂不展开 5 倍乘法**；你选定某条故事线后再挂 Hero 变体即可。

---

## 6. 故事线总览（当前可勾选）

| # | 故事线 ID | 大方向 | 类型 | 相对谁派生 |
|---|-----------|--------|------|------------|
| 1 | F-基准 | Features | 基准 | — |
| 2 | SC-基准 | Scenarios | 基准 | — |
| 3 | SC-派生-tab9 | Scenarios | 派生 | SC-基准，M03 tab 9 替 3 |
| 4 | SL-基准 | Solution | 基准 | — |
| 5 | T-基准 | Tools | 基准 | — |
| 6 | T-派生-cluster12 | Tools | 派生 | T-基准，M12 cluster 12 替 4 |
| 7 | P-基准 | Product | 基准（仅有号段） | — |
| 8 | P-派生-photoloop | Product | 派生 | M08【派生-P8】 |
| 9 | P-派生-testimonial | Product | 派生 | M14【派生-P14】 |
| 10 | P-派生-pricing | Product | 派生 | M15【派生-P15】 |
| 11 | LP-基准 | Landing Page | 基准 | — |
| 12 | LP-派生-dynamic | Landing Page | 派生 | M13【派生-L13】 |

**合计：12 条**（不含 Hero ×5 横切）。

后续若某本体在设计稿中新增变体编号，在对应方向 **再派生一条**，不覆盖已有 ID。

---

## 7. 勾选表

| ☐ | 故事线 ID | 备注 |
|---|-----------|------|
| ☐ | F-基准 | |
| ☐ | SC-基准 | |
| ☐ | SC-派生-tab9 | |
| ☐ | SL-基准 | |
| ☐ | T-基准 | |
| ☐ | T-派生-cluster12 | |
| ☐ | P-基准 | |
| ☐ | P-派生-photoloop | 待补设计变体号 |
| ☐ | P-派生-testimonial | 待补设计变体号 |
| ☐ | P-派生-pricing | 待补设计变体号 |
| ☐ | LP-基准 | |
| ☐ | LP-派生-dynamic | 待补设计变体号 |

---

## 8. 与 Refresh-Page 的关系

- **本体 / 变体 / 派生** → 以本文 + PDF 为准。  
- **`bodyJson` 的 `type` 字符串** → 仍查 [README.md](./README.md)；映射见 [PAGE-MODULE-MATRIX.md §5](./PAGE-MODULE-MATRIX.md)。  
- 选定故事线 ID 后，再生成 JSON / 物料清单（下一步，你确认勾选后做）。
