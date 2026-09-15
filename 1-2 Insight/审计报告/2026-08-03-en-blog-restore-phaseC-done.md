# EN Blog Phase C 完成 — Local 清洗导入

> 日期：2026-08-03  
> 对象：overlap `BOTH_FULL` 21 + `LOCAL_FULL` 11 = 32  
> 脚本：`~/Documents/Lovart Local Dev/scripts/active/import_local_scrubbed_body.py`  
> 只改 `body`；SEO 字段不动

## 结论

**30/32 已 apply**（0 apply_error）。2 篇 scrub 后 <1800 词，进 Phase D 重写，不硬灌。

## 源选择

| 策略 | 篇数 | 说明 |
|---|---:|---|
| Local MD 清洗 | 29 | 剥 E-E-A-T / Related Resources / Image Appendix / Internal Links；未 verified `/blog/` 降级为纯文本 |
| History@07-20 | 1 | `nano-banana-2-vs-pro`（History 4220 > Local 3915） |
| signal-writer ready 稿 | 1（含在 Local） | `freepik-ai-image-generator-review` ← `01-Drafts/review-freepik-…md`（status: ready） |

## FAIL → Phase D

- `05-ai-design-freelance-pricing-guide-2026`（scrub 后 1722 词）
- `S14-ai-design-cost-calculator-comparison`（scrub 后 1726 词）

## 产物

- 报告：`Output/QA-Memo/en-restore-phaseC-20260803T072509Z.{json,csv}`
- 备份：`Output/QA-Memo/restore-backup-phaseC-20260803T072509Z/`

## 累计进度（A+B+C）

| Phase | applied |
|---|---:|
| A | 306 |
| B | 610 |
| C | 30 |
| **合计** | **946** |

剩余污染 → Phase D（REWRITE ~304 + EMPTY/THIN + B/C fail）。

## 同 slug 双文档补丁

Phase C 审计 `_id` 与线上 canonical 不完全一致，发现 2 组同 slug 双文档；已把恢复后的 body 复制到仍污染的 twin：

- `nano-banana-2-vs-pro`：`blog-nbvsp-en` → `blog-nano-banana-2-vs-pro-en`
- `pika-ai-review-2025-…`：短 id → `blog-pika-ai-review-2025-…-en`

**未删除**任何 production 文档（铁律）。后续需单独做 duplicate slug 治理（noindex/canonical），不在本阶段删库。

## 污染残留（C 后）

- EN 污染开场标记：~366（A 前 ~1300；B 后 397；C 后再降）
- h2=24+pad：~352
