# P1 批次质检报告 · 2026-11-03

> 对象：`p1-batch.jsonl`（B-cinematic 5 张 + C-mosaic 8 张，共 13 张）
> 工具：`dev/scripts/tmp_brief_qc.py`（10 项自动规则：JSONL 结构 / 变体规格 / no-text 约束 / v2 禁词 / 高风险 UI 词 / 航道一致性 / 复杂度信号 / cinematic 三层结构 / mosaic 序列结构 / alt 合规）
> 结果：**BLOCK 0 / WARN 0 → 通过（可投喂）**

## 逐张结果

| ID | 航道 | 检查结论 |
|---|---|---|
| C-PLA | L3 柔体三维 | PASS：三层深度（卡片/成品列/空背景）+ 8% 渐隐；无光轨、无 UI |
| C-IMG | L1 商业摄影 | PASS：三层（画笔筒/画架/窗光）；点睛色仅存在于画内 |
| C-ECO | L1 商业摄影 | PASS：三层（瓶身特写/展台产品/白底卡）；"半实拍半 listing"叙事 |
| C-LOG | L5 材质静物 | PASS：三层（卡角/卡组/深灰空间）；无 typography 风险词 |
| C-IND | L1 商业摄影 | PASS：模板化背景可换装已注明；实物展板替代屏幕 |
| M-PLA-1~4 | L3 柔体三维 | PASS ×4：同一 console 四状态（待投→进行中→首件成品→全套交付）；locked seed 声明、lower 30% 留白齐全 |
| M-IND-1~4 | L1 商业摄影 | PASS ×4：同一包装四状态（坯+brief→新套封→批量列→上架）；群组主体已标注 |

## 过程修复记录（交付前已修）

1. **S-SOC（P0 复检）**：`surrounded by three cutouts` 触发复杂度信号 → 改为 `beside it three cutouts`，主从关系明确，WARN 归零。
2. **C-IND**：初稿 `frosted-glass board` 有玻璃拟态联想风险 → 改为 `matte standing board`。
3. **M-PLA-3**：初稿 `slot emitting a soft matte glow` 与负面词 `neon glow` 边界模糊 → 改为 `slot lit with a soft coral tint`。
4. **S-VID / C-PLA / C-IMG**：补齐 `no screens` 声明（含 desk/studio 场景的词表要求）。

## P0 v2 复检（回填）

`p0-batch-v2.jsonl` 6 张：BLOCK 0 / WARN 0（修复 S-SOC 后全 PASS）。**P0 v2 与 P1 均处于可投喂状态。**

## 已知残余风险（QC 无法覆盖，生成时需人工一眼确认）

- 风格"美丑"本身无法文本质检——已用航道 token + style reference 工作流（见 prompt-v2-style-system.md §5）对冲；
- mosaic 4 瓦同族性依赖生成时真的同 seed/同会话，prompt 只能声明、无法强制；
- C-IND 模板化换装效果需首个行业验证后再放量。
