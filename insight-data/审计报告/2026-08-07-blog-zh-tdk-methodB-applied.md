# Blog 简中 TDK Method B — 已 apply（2026-08-07）

## 结论

方式 B（打断 Title 回声）已写入 production：**183/183 OK**，fail=0。范围是 GSC 曝光≥20 且描述仍以 seoTitle（或标题头）开头的简中 Blog。覆盖曝光合计约 **31,770**，其中曝光≥100 共 48 篇。

`preflight_tdk_i18n --strict`：PASS 183 / BLOCK 0。抽查字段 `description` 与 `seo.description` 均匹配；本批 patched 文档线上仍回声 = 0。

## 改了什么

只改 `description` / `seo.description`。标题与 keywords 不动（留给方式 C）。描述首句改为检索意图句（按 guide/review/versus/persona/howto 分流），主题用短 hint 挂在中间，禁止再以标题开篇。

## 残量

主批 183 之后又补清同 slug 重复文档（Pollo / Artlist 等，共 5 条 mutate）。曝光≥20 的 Title 回声档已清完；剩余回声主要是低曝光或零曝光页，ROI 低于方式 C。

## 证据

- 本地包：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-zh-tdk-methodB-2026-08-07/`
- apply 报告：`methodB-apply-report.json`
- 人审 diff：`methodB-diff.csv`

## 下一刀

方式 C：关键词去灌水（通用词堆叠 → 页级具体词），优先高曝光页。
