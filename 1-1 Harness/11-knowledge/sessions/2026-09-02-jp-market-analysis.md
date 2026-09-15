---
type: session-log
session_date: 2026-09-02
session_slug: jp-market-analysis
status: ready
---

# Session 2026-09-02 — 日本市场 SEO 全窗口复盘（Google + Bing）

## Goal
梳理 2025-04 ~ 2026-07 日本市场在 Google（GSC）与 Bing 的整体 SEO 表现：关键词、页面、洞察结论。用户要求全量拉取，不得只查部分。

## What was done
- GATE1 已跑（pipeline 下一任务与本请求无关，用户直接指令优先）。
- 新建 `1-4 Dev/scripts/trident/jp_full_pull.py`（governance PASS）：GSC JP 逐月 query/page/date 三维度分页全量（19 个月）+ GA4 JP organic（sessionSource 逐月 / landingPage / country / organic daily）。
- 复用 `bing_fetch.py` 拉 Bing 全站 16 个月（无国家维度）。
- 新建 `jp_analyze.py`：品牌分类（is_brand SSOT）、日文词检测、页面分类、引擎拆分、movers。
- 原始数据 /tmp/jp_pull/*.json（gsc_jp / ga4_jp / bing-full / jp_analysis）。
- 报告：`1-2 Insight/Trident Insights/reports/Lovart-SEO-JP-2025-2026H1.md`。

## Key numbers
- GSC JP：2025-04-19 起有数据。日均点击 226(2025) → 568(2026H1) x2.51；曝光 x4.05；峰值 2026-03 26,580 点击 / 2026-04 168k 曝光；2026-07 11,185 点击（-58% vs 峰值）。CTR 59.5% → 10.5%，位 2.1 → 5.6。
- 品牌词 95.9% 点击；非品牌词全窗口仅 6,218 点击；日文词 8,404 个 / 18,790 点击。
- 唯一成规模本地化资产：学生証 cluster（学生証作成 メーカー 1,187 点击，位 2.5，CTR 30%）。
- GA4 JP organic：2025 月均 88k → 2026H1 月均 187k (x2.12)；引擎 Google 49.7% / Bing 24.6% / 中文引擎合计 24.8%（百度 16.4%）；JP 占全站 3.64%。
- Bing 全站：峰值 2026-03 276k 点击，/zh 占 62%；/ja 全窗口仅 4,296 点击（Bing 日本未开发）；Yahoo JP 份额 0.74%。

## Next actions
- 学生証 cluster 长尾扩张；/ja 大曝光工具页（video-generator 7.4 万曝光等）改写；模型词日文承接；Yahoo JP + Bing /ja 提交。

## Part 2 — GA4 日本流量深挖（同会话追加）
- 新建 `jp_ga4_deep.py`（governance PASS）：JP 全渠道 577 天日度 + 渠道/设备/新老/事件/来源逐月 + 着陆页(10万页) + 城市(1239) + 全球对照。踩坑：events 循环变量 `e` 遮蔽 end_date 导致 endDate 传对象（400 错误），已修复并加断点续跑。
- 新建 `jp_ga4_analyze.py`：月度聚合/渠道/设备/事件/来源/城市/汇总对比 → /tmp/jp_pull/jp_ga4_analysis.json。
- 报告：`1-2 Insight/Trident Insights/reports/Lovart-GA4-JP-2025-2026H1.md`。
- 核心数字：JP 全渠道日均 8,286(2025) → 29,236(2026H1) → 48,349(2026-07)；全球份额 2.43% → 10.71%；organic 占比 38.3% → 14.6%（绝对值 x4.6 仍涨）；TikTok 付费社交 0 → 32.7万/月；中文生态(百度/QQ/liblib/Antom/cn.bing)占 JP 流量 20-25%；东京23区 81.8%；form_start→form_submit 0.78%；GA4 无注册/付费埋点。
