# EN Blog Phase A+B 恢复完成

> 日期：2026-08-03  
> 锚点：`2026-07-20T00:00:00Z`  
> 只改 `body`，SEO 字段不动  
> 脚本：`~/Documents/Lovart Local Dev/scripts/active/restore_en_blog_body_from_history.py`

## 结论

History 可恢复池已基本清空：**916 篇 body 已从 07-20 锚点写回 production**。  
全库污染标记从 **~1300 → 397**；硬克隆（h2=24+pad）从 **~994 → 384**。

## 执行结果

| Phase | 标签 | 门槛 | applied | fail | 备注 |
|---|---|---:|---:|---:|---|
| A | HISTORY_OK + SCRUB | 1800 | **306** | 0 | 含 overlap HISTORY_OK |
| B | HISTORY_OK_WEAK | 1400 | **610** | 10 | fail 全为 below_floor，进 Phase D |
| **合计** | | | **916** | **10** | 0 apply_error |

## 污染残留

- EN 仍命中污染开场标记：**397** / 1314
- 其中 h2=24 + pad：**384**（Phase C/D 主战场）
- Phase B fail 10 篇（History <1400 词）并入 rewrite 队列

## 产物

- 报告 JSON/CSV：`Output/QA-Memo/en-restore-phaseA-20260803T06*.{json,csv}`
- 备份：`Output/QA-Memo/restore-backup-20260803T06*/`
- Phase A 明细：`2026-08-03-en-blog-restore-phaseA-done.md`

## 下一步

1. **Phase C**：overlap LOCAL_FULL / BOTH_FULL（~32）— 本地 scrub 后 patch body  
2. **Phase D**：剩余 ~350+ REWRITE / EMPTY / THIN + B-fail10 — `lovart-blog-signal-writer`  
3. Preflight：共享 24-H2 fingerprint / Canva 开场 → BLOCK
