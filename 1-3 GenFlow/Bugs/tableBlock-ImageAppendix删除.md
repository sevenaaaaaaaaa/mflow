## Image Appendix 表删除 — 2026-08-06

### 结论
按用户要求：从文章中**去掉** Image Appendix / 图注清单表（含压扁 `Image|Description|Alt Text`、`Suggested Visual`、`Figure` 附录表）。**不删文档**，只删对应 `tableBlock`（若紧前是附录标题则一并删）。

### 结果
| 语 | 篇 | 表 | 抽样 |
|---|---|---|---|
| DE | 127 | 127 | 20/20 OK |
| FR | 113 | 113 | 20/20 OK |
| ES | 167 | 167 | 20/20 OK |
| PT | 94 | 94 | 20/20 OK |
| RU | 104 | 104 | 20/20 OK |
| IT | 210 | 210 | 20/20 OK |
| KO | 141 | 141 | 20/20 OK |
| **合计** | **956** | **956** | 抽样无 FAIL |

脚本：`~/Documents/Lovart Local Dev/scripts/active/delete_appendix_tableblocks.py`  
Memo：`tableblock-*-appendix-delete-2026-08-06.json`

### 分类规则（只删这些）
- 表头含 `Alt Text` / `Suggested Visual`
- 首列 `Image` / `Image ID` / `Image #` / `Figure` / `Bild` / `이미지` / `#` 且含 Description/Alt
- 压扁单行图注 dump（文件名 + alt）

正文对比/定价/色板表不在范围。
