# Blog 简中正文 Phase 1 — 404 模板腔清洗（已 apply）

## 结论

正文层已开刀，第一波针对 `blog-404fix-*-zh`（120 篇）。目标不是全文重写，而是先去掉读者一进文就撞上的运营腔与英文模板词。

已写入 production：

- 波次 A：116 篇 glossary + 去「这条中文 URL」句（保留 Brand Kit / ChatCanvas / Touch Edit / Design Agent）
- 波次 B：误伤回滚后，改为逐 span 谨慎删除「曾返回 404 / 曾 404」等
- 波次 C：25 篇跨 span 的「这篇补 /zh/blog/...404」整句清除 → 残量 0

精确残量（Python 全文检索，非 GROQ 模糊 match）：

- `这条中文 URL` = 0
- `曾返回 404` = 0
- `这篇补` = 0
- `brief 合同` = 0
- `改稿-heavy` = 0

## 读者能感到的变化

开篇不再解释「这条 URL 曾 404 / 这篇补 404」。部分 `daily ops / revision cost / editable / readable / disclaimer` 等模板英文已换成中文说法。产品名未翻译。

## 诚实边界

这仍是**清洗**，不是**重写**。正文里仍有不少中英混排与运营腔（如 series、carousel、accent、honest roundup）。部分开篇删句后会留下 slug 碎片或语气略跳，需要在 Phase 2 用高曝光全文重写消化。

机械替换有过一版误伤（跨 span 拼句），已用波次 A 备份回滚后改谨慎策略；当前线上以回滚后的清洗态为准。

## 证据包

`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-zh-body-404-scrub-2026-08-07/`

## Phase 2（下一刀）

按 GSC 曝光优先，对 404 批次 Top10–20 做**开篇+关键 H2 人工级重写**（不是再跑 glossary）。并行拉 2026-07-22 heavy_en_mix 清单与曝光交叉，排非 404 存量队列。
