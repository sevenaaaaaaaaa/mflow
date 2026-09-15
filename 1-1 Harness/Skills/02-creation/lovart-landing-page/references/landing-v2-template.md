# Landing Page composite-v2 模板（投放向）

> SSOT：[`landing-storylines.json`](../../../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/landing-storylines.json)  
> 制作指南：[`LANDING-PRODUCTION-2026-06-07.md`](../../../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/LANDING-PRODUCTION-2026-06-07.md)  
> 参考 JSON：[`landing-examples/en/`](../../../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/landing-examples/en/)

## 何时用 Landing Page（而非 Tools / Features）

用户明确说 **投放落地页 / Landing Page / paid media LP**，或 brief 要求 **12 段 composite-v2 + 投放意图选型**。

| 信号 | 故事线 ID |
|------|-----------|
| 广泛匹配 / 多工具矩阵 | `landing-gallery-detail` |
| 漏斗教育 / 再营销 | `landing-gallery-funnel` |
| 品牌 upper funnel | `landing-brand-trust` |
| Search 试用 / try now | `landing-trial-now` |
| 竞品 / vs / alternative | `landing-vs-competitor` |
| 促销 / retarget / pricing | `landing-offer-close` |
| 内部 QA / 模块验收 | `landing-full`（**15 段，勿投放**） |

别名：`landing-A` → `landing-gallery-detail`；`landing-B` → `landing-gallery-funnel`

## 输出契约

| 字段 | 值 |
|------|-----|
| `category` | `topic`（参考案例）；上线可映射 `product` / `solution` / `topic` |
| `schemaVersion` | `composite-v2` |
| `storylineId` | 上表之一 |
| `bodyJson` | 顶层 JSON 数组，**严格按** `landing-storylines.json` 中该线的 `sections` 顺序 |
| 输出路径 | `Page Gen/Refresh-Page/landing-examples/en/`（草稿）或用户指定 `topic` 目录 |
| `seo.noIndex` | 参考案例默认 `true` |

## 生成前检查

1. 从 `landing-storylines.json` 读取目标线的 `sections` 数组  
2. 从 [`preview-data.json`](../../../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/preview-data.json) 复制各 `type` 字段骨架  
3. 复制 [`landing-examples/en/`](../../../../1-3%20Content%20Gen/Page%20Gen/Refresh-Page/landing-examples/en/) 中最接近意图的参考稿改文案  
4. 跑结构预检（见 LANDING-PRODUCTION §3）

## 与 Tools 轨道的区别

| | Landing Page | Tools |
|--|--------------|-------|
| 故事线数 | 7（投放 6 + demo 1） | T1–T5、T-long 等 |
| 典型 Hero | gallery / cinematic / split / journey | 多为 `hero-split` |
| 投放选型 | 按创意意图（信任/试用/对比/收口） | 按工具任务 |
| 满配 demo | `landing-full` 15 段 | 无 |

## 一键生成（本地）

```bash
cd "1-4 Dev/lovart.sanity.studio"
node scripts/generate-landing-storyline-drafts.js
```
