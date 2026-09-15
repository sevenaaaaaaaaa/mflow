# tableBlock FAQ/附录/related 空壳删除 — Pilot（2026-08-05）

## 结论

七语 pilot 已跑完：只删 **FAQ / 附录 / related** 上下文中的空 `tableBlock`（无 `rows`），不删文档、不碰有 rows 的表、CTA/`block` 指纹门禁通过。

**合计删除 67 个空壳**（设计上限每语 ≤10；IT 可分类的只有 7）。

| 语 | 删壳 | 文档数 | 类型 | 剩余 docs / nodes |
|---|---:|---:|---|---|
| DE | 10 | 8 | faq 9 + related 1 | 148 / 190 |
| FR | 10 | 10 | faq 10 | 163 / 224 |
| ES | 10 | 10 | faq 9 + related 1 | 46 / 64 |
| PT | 10 | 10 | faq 10 | 119 / 151 |
| RU | 10 | 10 | faq 10 | 108 / 155 |
| IT | 7 | 6 | faq 5 + appendix 2 | 24 / 41 |
| KO | 10 | 10 | faq 10 | 61 / 75 |

机器源：`~/Documents/Lovart Local Dev/Output/QA-Memo/tableblock-faq-appendix-delete-pilot-2026-08-05.json`

## 规则（pilot 已执行）

1. 前后文分类为 faq / appendix / related 才删  
2. 拉完整 `body`，只去掉目标下标空壳  
3. 其余节点 JSON 指纹不变；有 rows 的 table 数量不变；CTA link / block 数不回退  

## 未做

- 未扩全量  
- 未删 `other` / 无源内容槽（如 flora Core Feature、E-E-A-T 旁空壳）  
- 未重建 Image Appendix 表  

## 下一轮

分类器扫全量 → 同规则批量删 FAQ/附录/related；`content-candidate` 仍走 MD 补 rows。
