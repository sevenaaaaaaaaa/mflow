# P2 批次质检报告 · 2026-11-03

> 对象：`p2-batch.jsonl`（A-split 14 张 + D-gallery 60 张，共 74 张；至此 93 张全批交付完毕）
> 生成方式：`dev/scripts/tmp_gen_p2.py`（结构化数据 + 航道前缀 + 模板后缀统一装配，消除手工笔误）
> 工具：`dev/scripts/tmp_brief_qc.py`（10 项自动规则）
> 结果：**BLOCK 0 / WARN 0 → 通过（可投喂）**

## 覆盖与结构

| 子批 | 数量 | 规格 | 内容 |
|---|---:|---|---|
| A-split | 14 | 2160×1620 · 4:3 | 剩余 14 个主题族（print/docs-deck/avatar/photo-edit/industry/ads/creator-av/compare/web-ui/audio/interior/education/3d/fashion） |
| D-gallery | 10 套 × 6 | 每瓦 1200×1200 · 1:1 | G-PLA / G-VID / G-PRT / G-IMG / G-SOC / G-ECO / G-DOC / G-LOG / G-ADS / G-CMP |

航道分配：platform/3d → L3 柔体三维；video → L2 电影剧照；image-gen/ecommerce/avatar/photo-edit/industry/creator-av/interior/fashion → L1 商业摄影；social/docs-deck/ads/compare → L4 图形平面；print/logo-brand/docs-deck(split)/audio → L5 材质静物；education/web-ui → L6 纸艺。

## 过程修复记录（交付前已修）

1. **G-PLA-3 / G-PLA-4 / G-PLA-5**：alt 与 platform 主题词关联弱 → alt 分别补入 brief / design 锚点。
2. **G-ECO-6**：prompt 缺 ecommerce 主题词 → `three connected cards` 改为 `three connected product cards`。
3. **G-PLA-3**：初稿 `dial surrounded by four chips` 触发复杂度信号 → 改为 `dial with four chips beside it`。
4. **G-CMP-2**：初稿 `scattered coins` 触发复杂度信号 → 改为 `a heap of coins`。
5. **S-AVA**：初稿 `flat graphic` 与 L4 冲突词 `flat-graphic` 边界模糊 → 改为 `flat poster`。
6. **S-WEB**：初稿 `button-shaped chip` 命中高风险词 `button` → 改为 `a rounded chip layer`。
7. **G-VID-5**：`timeline strip` 命中高风险词 → 改为 `a short film strip with trim notches and color tabs`。
8. **G-DOC-3/4**：`chart/infographic` 高风险词 → 统一改为 `abstract data shapes / data motifs`（label 保留 Infographic，不进 prompt）。
9. **G-ADS-6**：`snapshot feel` 与禁词 `snapshot look` 相邻 → 改为 `authentic candid feel`。

## 投喂操作要点（QC 无法强制、依赖执行）

1. **gallery 同族性**：每套 6 瓦必须同一会话连续生成 + 锁 seed + 同风格参考；同套背景色已在 prompt 统一（G-PLA warm grey / G-VID deep charcoal / G-PRT·G-DOC·G-CMP ivory / G-IMG warm beige / G-SOC·G-ADS cream / G-ECO sand / G-LOG warm grey）。
2. **zh 四套**（G-PRT/G-SOC/G-ECO/G-CMP）：prompt 英文生成，alt 已给中文；投放 zh 页面时 label 用 brief 表中的中文 label。
3. **S-IND** 与 C-IND 共用模板背景，换装逻辑一致。

## 全批状态（93/93）

| 批次 | 文件 | 数量 | QC |
|---|---|---:|---|
| P0 | `p0-batch-v2.jsonl` | 6 | BLOCK 0 / WARN 0 |
| P1 | `p1-batch.jsonl` | 13 | BLOCK 0 / WARN 0 |
| P2 | `p2-batch.jsonl` | 74 | BLOCK 0 / WARN 0 |

## 已知残余风险

- gallery 瓦片"单对象肖像"构图对 Lovart 的引导强度需首套（建议 G-PRT）验证后再放量其余 9 套；
- L4 图形平面航道（G-SOC/G-DOC/G-ADS/G-CMP 共 24 瓦）与站内现有摄影风 hero 的气质差异需上线前确认一次；
- 风格"美丑"本身仍依赖 style reference 工作流（prompt-v2-style-system.md §5）对冲。
