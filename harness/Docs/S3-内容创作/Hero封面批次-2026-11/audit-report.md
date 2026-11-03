# 风格一致性与多样性审计报告 · 2026-11-04

> 对象：93 张 Hero brief（module-A/B/C/D）
> 工具：`dev/scripts/tmp_style_audit.py`（航道分布 / 模板疲劳 n-gram / 两两 Jaccard / 视觉参数分布 / 结构完整性）
> 修复：`tmp_refine_v3.py`（构图与参数补齐）+ `tmp_refine_v4.py`（L4 航道差异化）
> 结论：**四模块 QC 全绿；跨套同质对 13 → 0；结构缺口 0**

---

## 一、修复前后对比

| 指标 | 修复前 | 修复后 | 说明 |
|---|---:|---:|---|
| 跨套同质对（Jaccard ≥0.75） | 13 | **0** | 主要来自 L4 四套共用同一航道前缀 |
| 同质对总数 | 161 | 47 | 剩余 46 为同套内（设计意图：同族一致性） |
| 缺焦段 | 41 条 | **0** | L5 补 100mm，L4 声明 flat 透视（合法），split 补等效焦段 |
| 缺布光 | 31 条 | **0** | split 补 key light；L4 用 flat even lighting |
| 缺点睛色 | 7 条 | **0** | L2 显式声明"严格双色，无第三色" |
| 100mm 焦段使用 | 11 | 23 | L5 材质静物全部落到微距 |
| coral 点睛色占比 | 35/93 | 29/93 | L4 分散到 ink-blue / tangerine / duotone |
| charcoal 底色占比 | 24/93 | 18/93 | 同上 |

## 二、核心问题：构图同质（已修）

**问题**：60 条 gallery 原本共用同一句 `hero fills 70% of frame`，6 瓦之间只有主体名称不同——出图必然雷同。

**修复**：按 `tile` 序号注入**机位 × 填充率**矩阵，每套 6 瓦走一套不同机位：

| tile | 机位 | 填充率 |
|---:|---|---:|
| 1 | 正视平视（straight on, eye level） | 70% |
| 2 | 四分之三侧角 | 68% |
| 3 | 材质表面微距（close macro） | 76% |
| 4 | 正俯拍（top-down） | 66% |
| 5 | 低角度仰视 | 72% |
| 6 | 正侧profile | 70% |

mosaic 4 瓦同理：平视横排 → 侧角纵深 → 近距微距 → 拉远全景（递进叙事）。

## 三、L4 航道差异化（新增 v4）

L4 图形平面原有 24 瓦共用同一段 token，导致 G-SOC/G-DOC/G-ADS/G-CMP 四套瓦片长得像。改为**同一航道下的 4 个版式子型**：

| 套 | 版式子型 | 视觉特征 | 调色板 |
|---|---|---|---|
| G-DOC | editorial-grid | 严格瑞士网格、细线、大留白 | ivory + ink-blue + charcoal |
| G-SOC | bold-poster | 大色块、斜切、满版冲击 | cream + coral（大块）+ charcoal |
| G-ADS | badge-stack | 层叠错位卡片、印章徽章形 | cream + tangerine + charcoal |
| G-CMP | duotone-split | 硬中缝分割、镜像双色对撞 | 暖灰 ↔ 珊瑚 双色 |

每套内部再配 6 种版式机位（如 G-SOC：居中裁切 / 满版 / 对角切 / 下压 / 偏心 / 徽章居中）。

## 四、剩余高频短语（非缺陷，属模板固有）

| 频次 | 短语 | 判读 |
|---:|---|---|
| 68× | `locked seed and style reference shared across all…` | 操作纪律声明，需保留 |
| 60× | `bottom 25% clean for label scrim` | gallery 模块强制要求 |
| 24× | `riso-print ink edges flat poster layout` | L4 航道 token（4 套共用，但版式已分化） |

> 说明：n-gram 疲劳检测对"航道 token"和"安全区约束"必然报高，这类重复是设计所需；真正需警惕的是**主体描述与机位描述**的重复，已通过 v3/v4 消除。

## 五、航道分布现状

| 航道 | A | B | C | D | 合计 |
|---|---:|---:|---:|---:|---:|
| L1 商业摄影 | 9 | 3 | 4 | 12 | 28 |
| L4 图形平面 | 2 | 0 | 0 | 24 | 26 |
| L5 材质静物 | 4 | 1 | 0 | 12 | 17 |
| L3 柔体三维 | 2 | 1 | 4 | 6 | 13 |
| L2 电影剧照 | 1 | 0 | 0 | 6 | 7 |
| L6 纸艺 | 2 | 0 | 0 | 0 | 2 |

**观察**：L6 纸艺只覆盖 2 条（S-WEB / S-EDU），是全站最"另类"的航道。若上线后发现与站内其他 hero 气质割裂，建议将这两条改为 L1 或 L4 重出——已列入风险项。

## 六、残余风险（文本质检无法覆盖）

1. **风格美丑**仍依赖 Step 0 的 style sheet 定调（`NEXT-STEPS.md`），brief 只能保证"参数正确 + 不同构"。
2. **同套一致性**依赖生成时真的锁 seed / 同会话，prompt 只能声明、无法强制。
3. **L4 四套的气质分化**需首套（G-SOC）出图后与站内现有摄影风 hero 对比确认；若冲突，其余 L5→L4 需回调。
4. **L6 纸艺**是否保留，见第五章观察。

## 七、复跑命令

```bash
cd "mflow"
python3 dev/scripts/tmp_refine_v3.py      # 构图/布光/焦段/调色板修复
python3 dev/scripts/tmp_refine_v4.py      # L4 航道差异化
python3 dev/scripts/tmp_gen_modules.py    # 重建 module-*.jsonl + module-briefs.md
python3 dev/scripts/tmp_brief_qc.py "harness/Docs/S3-内容创作/Hero封面批次-2026-11/module-D-gallery.jsonl"
python3 dev/scripts/tmp_style_audit.py    # 一致性与多样性审计
```
