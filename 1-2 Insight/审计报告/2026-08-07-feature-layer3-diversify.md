# Feature Layer3 分桶改写（feature-detail / comparison / cluster / cta）（2026-08-07）

## 结论

对同质 `feature-detail` 条目、`comparison-table` 行、`cluster-block-dense` 卡片、`cta-default` 描述按 slug MD5 分 **8 桶**，本地 JSON + Sanity `createOrReplace`。失败 = 0。

首轮在 **it≈150** 处进程中断；断点续跑 it/pt/ru 后清零。

## 数量（结果文件口径）

| 语言 | scanned | changed | skipped | fails |
|------|--------:|--------:|--------:|------:|
| en | 134 | 134 | 0 | 0 |
| zh | 231 | 223 | 8 | 0 |
| zh-TW | 73 | 73 | 0 | 0 |
| ja | 489 | 489 | 0 | 0 |
| ko | 507 | 507 | 0 | 0 |
| de | 523 | 523 | 0 | 0 |
| fr | 528 | 528 | 0 | 0 |
| it | 527 | 392(+首轮≈150) | 135 | 0 |
| pt | 522 | 522 | 0 | 0 |
| ru | 524 | 524 | 0 | 0 |

有效覆盖约 **~4050** 页（it 首轮+续跑；pack0 标题与 HOMO 指纹重合会导致检测仍显示少量「需改」，实为已改写的桶 0）。

## 效果

各语种 feature-detail item0 unique ≈ **8**。

## 缓存

`~/Documents/Lovart Local Dev/Output/QA-Memo/feature-layer3-diversify-2026-08-07/`
