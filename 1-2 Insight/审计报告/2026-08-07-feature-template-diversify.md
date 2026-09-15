# Feature 模板同质分桶改写（2026-08-07）

## 结论

对同质 hero highlight（各语种几乎 1 条）按 slug 稳定哈希分 **8 桶**，改写 `highlightedText` + FAQ 6 题，并 `createOrReplace` 回写 Sanity。失败 = 0。

## 数量

| 语言 | scanned | changed |
|------|--------:|--------:|
| en | 134 | 134 |
| zh | 231 | 139 |
| zh-TW | 73 | 73 |
| ja | 489 | 489 |
| ko | 507 | 507 |
| de | 523 | 523 |
| fr | 528 | 528 |
| it | 527 | 527 |
| pt | 522 | 522 |
| ru | 524 | 524 |

合计 changed ≈ **3966**。FR 顺带清掉残留 `Pas de d'image` typo 前缀。

## 效果口径（本地复测）

改写后 unique highlight 远高于 8（因 `{f}` 写入部分桶）：例如 ja 1→245、fr 1→269、en 1→67；单条 top 从约 500 降至约 70。FR typo 残留 = 0。

## 缓存

`~/Documents/Lovart Local Dev/Output/QA-Memo/feature-template-diversify-2026-08-07/`
