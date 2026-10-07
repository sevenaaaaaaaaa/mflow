## tableBlock 压扁表解压 — 2026-08-05

### 结论
高置信度 **色板压扁表**（`Color Role | Hex | Usage` 单行塞 `\n`）已全量解压为多行矩形表。严格口径剩余 **0**。

### 本批结果
| 语 | 表数 | 状态 |
|---|---|---|
| DE | 27 | OK |
| FR | 17 | OK |
| ES | 29 | OK |
| PT | 14 | OK |
| RU | ~24 | mutate 读超时，抽查已写入 |
| KO | 4 | OK |
| IT | 0 | 无匹配色板压扁 |

脚本：`~/Documents/Lovart Local Dev/scripts/active/unflat_tableblock_color.py`  
Memo：`tableblock-*-unflat-color-2026-08-05.json`

### 仍未动（压扁残留主体）
- **Image Appendix 型**（Image / Description / Alt Text）— 多数压扁；解压价值低，前端多当附录
- **对比/定价等内容表** — 列数易误判（2↔3↔4），需更严校验或 MD 对齐后再解

### 与空壳关系
空壳（无 rows）仍在；压扁是「有 rows 但结构坏」。两件事分开处理。
