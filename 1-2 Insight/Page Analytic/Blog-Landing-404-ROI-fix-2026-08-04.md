# Blog + Landing 404 ROI 修复结论 — 2026-08-04

## 结论

- Landing **59**：产出 39 条 301（目标页全 200）+ 18 park + 2 drop；**前端未合入 redirects，from URL 仍 404**。
- Blog B1：10 条有稿仍 404，ISR 预热后 **10/10 = 200**。
- Blog B2 Top30：Class A 纠正语言标签并发布 **6** 篇（其中 HTTP 200=5）；Class B ready brief **22**（待 signal-writer 正文）；Class C 无源 **2**。
- 本轮重扫确认 Blog HTTP 200 新增 **13**；Blog 待修从 531 → **518**；Landing 待修仍 **59**（等前端）。

## 环比

- Blog 待修：531 → 518（Δ -13 / -2.4%）
- Landing 待修：59 → 59（Δ 0；301 未上线故基本不变）
- 合计开放 404（Blog+Landing+Docs）：594 → 581

## 💡 洞察

- 问题：CSV 404 里 Blog 主体是「缺语言文档」而非 CDN；少数是有稿未预热。
- 根源：i18n 只发了部分语言；EN 常缺。另有正文已是英文但挂在 zh-TW/ja 语言字段下。
- 缓解：Landing 先合 vercel redirects；Blog 继续按 triage P0 写 Class B；Class A 模式可复用于「latin body 错挂语言」。

## 交付物

- `Output/QA-Memo/landing-404-triage-2026-08-04.csv`
- `Output/QA-Memo/blog-404-triage-2026-08-04.csv`
- `Output/QA-Memo/landing-404-vercel-redirects-2026-08-04.json`
- `1-2 Insight/Page Analytic/Landing-404-301-map-2026-08-04.md`
- `Output/QA-Memo/blog-404-b1-rewarm-2026-08-04.csv`
- `Output/QA-Memo/blog-404-b2-top30-2026-08-04.csv`
- `1-3 GenFlow/Lovart-Blog-Pipeline/01-Drafts/404-roi-top30-2026-08-04/`
- `Output/QA-Memo/blog-404-parked-2026-08-04.md`

## 2026-08-05 续作：Class B 正文已写完（ready，待人审 import）

- 22/22 Class B bodies 写入 `1-3 GenFlow/Lovart-Blog-Pipeline/01-Drafts/404-roi-top30-2026-08-04/bodies/`
- EN 13 篇：正文词数均 ≥7,500；封面 blogcover 池 HEAD 抽检 200；Anti-Slop 禁用词/模板句 0 hit
- zh/zh-TW 6 篇：汉字 ≥12,000；ko/de/fr 各 1 篇：token ≥3,500
- 索引：`BODIES-READY-INDEX.md`；质检表：`Output/QA-Memo/blog-404-classB-bodies-qa-2026-08-05.csv`
- **未执行 Sanity import**（按计划停在 ready，等人审授权）

## 2026-08-05 授权发布

- Class B **22/22** `createIfNotExists` 入 Sanity production（`blog-404fix-{slug}-{lang}`）
- 预热后 HTTP **22/22 = 200**
- Blog 待修：约 496（相对发布前再降 22）
- 明细：`Output/QA-Memo/blog-404-classB-publish-2026-08-05.csv`

## 2026-08-05 P0 Next20 publish

- Published **20/20** (`createIfNotExists`) → HTTP **200** all
- CSV: `Output/QA-Memo/blog-404-p0-next20-publish-2026-08-05.csv`
- Blog pending after move: **473**; fixed cumulative tracked in 404-status
- Remaining P0 create queue still open beyond Next20

## 2026-08-05 P0 Next20b publish

- Published **20/20** → HTTP **200**
- CSV: `Output/QA-Memo/blog-404-p0-next20b-publish-2026-08-05.csv`
- Blog fixed **78** / pending **453**

## 2026-08-05 P0 Next20c publish

- Published **20/20** → HTTP **200**
- CSV: `Output/QA-Memo/blog-404-p0-next20c-publish-2026-08-05.csv`
- Blog fixed **98** / pending **433**

## 2026-08-05 P0 Next20d publish

- Published **20/20** → HTTP **200**
- CSV: `Output/QA-Memo/blog-404-p0-next20d-publish-2026-08-05.csv`
- Blog fixed **118** / pending **413**

## 2026-08-05 P0 Next20e publish

- Published **31/31** → HTTP **200** (final P0 create batch)
- CSV: `Output/QA-Memo/blog-404-p0-next20e-publish-2026-08-05.csv`
- Blog fixed **149** / pending **382**

## 2026-08-05 P1 batch publish

- Published **20/20** → HTTP **200** — P1 create cleared
- CSV: `Output/QA-Memo/blog-404-p1-publish-2026-08-05.csv`
- Blog fixed **169** / pending **362**
