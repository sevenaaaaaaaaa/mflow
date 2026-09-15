# Feature bento-6 + capability-tabs 分桶改写（2026-08-07）

## 结论

对同质 `bento-6` 条目与 `capability-tabs` 文案按 slug MD5 分 **8 桶**，本地 JSON + Sanity `createOrReplace` 同步。失败 = 0。首轮 ko/de 因指纹不一致 skipped，补指纹后二次清零。

## 数量

| 语言 | scanned | changed | fails |
|------|--------:|--------:|------:|
| en | 134 | 134 | 0 |
| zh | 231 | 222 | 0 |
| zh-TW | 73 | 73 | 0 |
| ja | 489 | 489 | 0 |
| ko | 507 | 507 | 0 |
| de | 523 | 523 | 0 |
| fr | 528 | 528 | 0 |
| it | 527 | 527 | 0 |
| pt | 522 | 522 | 0 |
| ru | 524 | 524 | 0 |

合计 changed = **4049**。

## 效果口径

改写后 bento item0 title unique ≈ **8**/语种（示例：en/fr/ja/ko/de）。ko 原指纹为「信息 위계를 명시」、de 为「Hierarchie klar machen」（非初版脚本假设），已写入 HOMO 集合。

## 缓存

`~/Documents/Lovart Local Dev/Output/QA-Memo/feature-bento-tabs-diversify-2026-08-07/`
