# Blog Signal Writer 质检（本地+线上）— 2026-08-05

> 谁会读：内容 / 发布  
> 为什么现在读：落地页语种清完后，Blog 须按 signal-writer 标准另线验收  
> 读完改变什么：READY/线上前排 FAIL 有明确队列；不与落地页 GT/vault 管道混用  
> 下一步：先啃线上 EN top100 词数不足 + 非 EN 前排 EN 壳；本地只盯 ready/published

## 标准

SSOT：`lovart-blog-signal-writer`（全分类英文 ≥7,500 词；分类/封面/禁用词/Anti-Slop；body Portable Text）。

## 结论

1. **线上 EN 前 100**（按 `releaseDate`）：**41** 篇未过 signal-writer 硬门槛，主因英文词数 <7500（35）与缺封面（8）。
2. **线上非 EN 各语前 30**：合计 **75** 篇 FAIL；主因正文 EN 壳/语种可疑（67）与缺 category（10）。重灾：IT/DE/PT/FR。
3. **本地**：宽扫 MD 噪声大（日历/半成品）；可行动子集（`status=ready|published` 或 Drafts/Published 路径）仅 **22** 篇，主因词数不足（21）。

修复走 signal-writer 重写，**不走落地页 GT 管道**。

## 机器文件

- 全量扫描：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-signal-writer-qa-2026-08-05.json`
- 可行动 FAIL 队列：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-signal-writer-fail-queue-2026-08-05.json`

## 建议顺序

1. 线上 EN top100：`EN_WORDS_BELOW_7500` → column-writer multi-turn 扩写至 ≥7500  
2. 线上非 EN 前排：`LANG_BODY` EN 壳 → 按语言重写（非机翻终稿）  
3. 本地 ready/published 22 篇清掉再进发布
