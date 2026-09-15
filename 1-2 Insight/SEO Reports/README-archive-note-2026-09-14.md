# SEO Reports 目录说明（2026-09-14 卫生轮）

本目录是 PATH-MAP 登记过的"路由违规区"，2026-09-14 做了第一次分流：

- **已归档到 Local Dev Backup**（29 个）：5 个临时调试脚本（_debug/_inspect/_generate_report）、
  17 个无引用 chart png、3 个空模板 CSV、3 个 A/B/C backup 产物、6 月月报 v1+v2。
  完整清单见 Backup/seo-reports-archive-2026-09-14/manifest.csv。
- **月报 SSOT 在** `../Trident Insights/reports/monthly/`，本目录不再产新月报。
- **sitemap/** 保留：是 sync-local-dev.sh 的映射目标（llms.txt/robots 快照）。
- 其余内容文件（wiki 批量、review 草稿、关键词清单、任务分配）为结论/工作资产，原地保留。

新规则：过程产物（脚本/中间 json/图表）不进 vault，走 `1-4 Dev/scripts/` 或 Local Dev Output。
