# Blog 简中 TDK Method C — 已 apply（2026-08-07）

## 结论

方式 C（关键词去灌水）已写入 production：**785/785 OK**，fail=0。覆盖 766 个唯一 slug（含同 slug 重复文档），曝光合计约 **107,348**。

线上抽查：`创作者实操` 残量 **0**，`创作者工具横评` 残量 **0**（全库 884 篇有 keywords 的简中 Blog 已扫完）。高曝光抽查 Freepik / CivitAI Red / Runway 替代 / 视频生成器 的 `seo.keywords` 均已换成页级词。

## 改了什么

只改 `seo.keywords`。Title / Description 不动。

清掉的灌水壳主要包括：

- `AI设计工具` + `设计工作流` + `创作者实操`（原约 484 篇）
- `AI工具评测` + `创作者工具横评` +「X评测/怎么样/替代」三联
- Brand Kit 壳：`品牌套件` + `价目视觉` + `预约海报`
- Agent 壳：`DesignAgent怎么选` / `可编辑AI设计` / `改价改图工具`

新词按 slug 类型生成（评测 / 替代 / 是什么 / 品牌套件 / how-to / 案例等），并按哈希打散尾词，避免再形成同一套三联。

## 证据

- 本地包：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-zh-tdk-methodC-2026-08-07/`
- apply 报告：`methodC-apply-report.json`
- 人审 diff：`methodC-diff.csv`

## 三修法收束

A 去公式句 → B 打断 Title 回声 → C 关键词去灌水，简中 Blog TDK 批量痕迹主战场已清完。后续若要更高质量，应转到正文层（404 模板腔 / heavy_en_mix），而不是继续批量刷 TDK。
