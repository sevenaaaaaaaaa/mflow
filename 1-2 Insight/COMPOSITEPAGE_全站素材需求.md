# 全站 compositePage 素材需求清单

> 更新日期: 2026-06-15
> 数据源: Sanity CMS o11tm2qe/production
> 状态: 框架已全部升级至生产标准，等待素材填充

---

## 一、框架状态总览

| 分类 | Slug | 页面数 | 框架 | 平均section | 缺槽位 |
|------|------|--------|------|------------|--------|
| TOOL | 443 | 917 | 14-section | 13.2 | 4,909 |
| FEATURE | 246 | 2,222 | 12-section | 12.7 | 551 |
| TOPIC | 48 | 48 | 12-section | 12.1 | 577 |
| SCENARIO | 70 | 70 | 11-section | 11.0 | 125 |
| SOLUTION | 10 | 10 | 12-section | 12.0 | 33 |
| PRODUCT | 2 | 2 | 12-section | 12.5 | 10 |
| LANDING | 3 | 3 | 9-section | 9.0 | 0 |
| **合计** | **822** | **3,272** | — | — | **6,190** |

## 二、素材预算

| 指标 | 数值 |
|------|------|
| 全站 media 槽位 | 11,476 |
| 已填充（有URL） | 4,286 |
| 去重URL数 | 206 |
| 需新素材 | ~7,190 |
| URL复用比 | 55:1 (4,286 / 206) |

## 三、TOOL 标准框架 (14-section)

```
hero-split        → 1 张 hero 大图
bento-4           → 4 张 feature 图
bento-2           → 2 张 feature 图
capability-tabs   → 4 张 tab 图
prompt-launcher
logo-loop
cta-default
workflow-horizontal
comparison-table
cluster-block-dense
feature-detail    → 4 张 item 图
proof-block       → 3 个 icon 卡片
faq
cta-default
```

每页 15 个 media 槽位（443 slug × 15 ≈ 6,645 个槽位仅 TOOL 分类）。

## 四、FEATURE 框架 (12-section)

每页 ~14 个 media 槽位，246 slug ≈ 3,444 个槽位。已有 3,041 个填充（仅 146 去重 URL）。

## 五、其他分类

| 分类 | 槽位/页 | 总槽位 | 已填充 |
|------|---------|--------|--------|
| SCENARIO | ~12 | 820 | 695 |
| TOPIC | ~21 | 987 | 410 |
| SOLUTION | ~17 | 173 | 140 |
| PRODUCT | ~15 | 30 | 20 |
| LANDING | ~19 | 57 | 72 |

## 六、执行建议

1. **TOOL P0** (339 slug) — 刚升级框架，所有 media 槽位共享 9 个 URL → 需大幅填充
2. **TOOL 有图** (104 slug) — 图片复用严重 → 需差异化替换
3. **FEATURE** (246 slug) — 146 URL 支撑 3,592 槽位 → 需增加多样性
4. **TOPIC** (48 slug) — 577 个槽位空白 → 优先级高
5. **SCENARIO** (70 slug) — 125 个空位 → 相对较小

## 七、相关文件

| 文件 | 路径 |
|------|------|
| Tools 审计原始数据 | `tools_asset_gap_audit.json` |
| Tools 品类标签清单 | `tools_P0_P1_categorized.json` |
| Tools 执行清单 CSV | `tools_P0_P1_execution_list.csv` |
| Tools 素材匹配计划 | `tools_asset_matching_plan.json` |
| P1 排查报告 | `TOOLS素材缺口排查报告.md` |
| 全站需求清单(本文件) | `COMPOSITEPAGE_全站素材需求.md` |

> 所有文件位于 `~/Documents/Lovart Local Dev/`
