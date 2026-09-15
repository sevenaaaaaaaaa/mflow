# Feature Layer4 分桶改写（prompt-launcher / testimonial）（2026-08-07）

## 结论

对同质 `prompt-launcher` 描述/三组 prompt/CTA，以及 `testimonial` 句式与作者，按 slug MD5 分 **8 桶**，本地 JSON + Sanity `createOrReplace`。失败 = 0。

## 数量

| 语言 | scanned | changed | skipped | fails |
|------|--------:|--------:|--------:|------:|
| en | 134 | 134 | 0 | 0 |
| zh | 231 | 139 | 92 | 0 |
| zh-TW | 73 | 73 | 0 | 0 |
| ja | 489 | 489 | 0 | 0 |
| ko | 507 | 507 | 0 | 0 |
| de | 523 | 523 | 0 | 0 |
| fr | 528 | 528 | 0 | 0 |
| it | 527 | 527 | 0 | 0 |
| pt | 522 | 522 | 0 | 0 |
| ru | 524 | 524 | 0 | 0 |

合计 changed = **3966**。zh skipped=92 为已非同质指纹。

## 效果口径

prompt-launcher description unique ≈ **8**/语种（zh 因存量已有部分差异 → unique 更高）。

## 缓存

`~/Documents/Lovart Local Dev/Output/QA-Memo/feature-layer4-diversify-2026-08-07/`
