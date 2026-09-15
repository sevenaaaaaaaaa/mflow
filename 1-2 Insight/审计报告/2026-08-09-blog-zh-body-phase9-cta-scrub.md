# Blog 简中正文 Phase 9 — CTA/Related/占位符清洗（已 apply）

## 结论

Phase 8 严格英壳清零后，本刀清简中正文批量 CTA 壳与 Related 英链。

已写入 production：**75/75 OK**，fail=0。

应用后残量：CTA 壳约 **0**；图片占位约 **0**。
删除块类型：{'cta': 75, 'related': 75, 'placeholder': 56, 'en_related_title': 5}。

## 策略

按 Portable Text 整块删除 CTA 壳、`Related:` 相关链、图片占位符、明显英文章节标题链。保留中文教程正文。

## 证据

`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-zh-body-phase9-cta-scrub-2026-08-09/`

## 下一刀建议

高曝光中英混排中段（Amazon 白底图等）截断英尾并中文补齐；或加厚 Phase4–8 高曝光短文。
