# Feature Layer2 分桶改写（bento-2 / workflow / pricing / proof）（2026-08-07）

## 结论

对仍高度同质的 `bento-2`、`workflow-horizontal`、`pricing-block`、`proof-block` 按 slug MD5 分 **8 桶**，本地 JSON + Sanity `createOrReplace`。失败 = 0。

## 数量

| 语言 | scanned | changed | skipped | fails |
|------|--------:|--------:|--------:|------:|
| en | 134 | 134 | 0 | 0 |
| zh | 231 | 222 | 9 | 0 |
| zh-TW | 73 | 73 | 0 | 0 |
| ja | 489 | 489 | 0 | 0 |
| ko | 507 | 507 | 0 | 0 |
| de | 523 | 523 | 0 | 0 |
| fr | 528 | 528 | 0 | 0 |
| it | 527 | 527 | 0 | 0 |
| pt | 522 | 522 | 0 | 0 |
| ru | 524 | 524 | 0 | 0 |

合计 changed = **4049**。zh 跳过 9 页为已非同质指纹。

## 效果口径（抽检）

| 语种 | bento-2 unique | workflow unique |
|------|---------------:|----------------:|
| en | 20 | 26 |
| ja | 63 | 66 |
| ru | 64 | 75 |

（含 `{f}` 写入桶 → unique > 8。）

## 缓存

`~/Documents/Lovart Local Dev/Output/QA-Memo/feature-layer2-diversify-2026-08-07/`
