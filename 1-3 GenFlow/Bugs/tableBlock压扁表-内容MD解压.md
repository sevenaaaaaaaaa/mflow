## tableBlock 内容压扁表解压（MD 对齐）— 2026-08-06

### 结论
对比/定价等内容压扁表，用 Content Calendar EN MD 作列数/行数 oracle，**531/531 OK**。

### 门禁
- 跳过 Image Appendix（alt text / suggested visual / figure）
- 跳过已处理色板（Color+Hex）
- 解压后：列数=MD、行数=MD、表头相似度 ≥0.5、score≥10
- 只改目标 `tableBlock.rows`；CTA / 其他节点 fingerprint 门禁

### 结果
| 语 | 表数 |
|---|---|
| DE | 74 |
| FR | 70 |
| ES | 128 |
| PT | 70 |
| RU | 60 |
| IT | 32 |
| KO | 97 |
| **合计** | **531** |

脚本：`~/Documents/Lovart Local Dev/scripts/active/unflat_tableblock_content_md.py`  
Memo：`tableblock-*-unflat-content-2026-08-06.json`

### Image Appendix
按计划**未动**（约 681 节点）。解压收益低；若前端当附录渲染，保持现状。

### 残留压扁
- appendix ~681
- other ~1182（无 MD / 对齐失败 / 非矩形可解）
- color 余量个位数（表头变体，非标准 Color Role/Hex）
