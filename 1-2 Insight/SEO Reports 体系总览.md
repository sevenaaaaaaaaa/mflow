# Lovart SEO 报告体系总览

> **生成日期**: 2026-07-14
> **Profile**: `lovart-reports`
> **规则 SSOT**: `1-1 Harness/02-rules/RULES-00-iron.md` + `RULES-10-reports.md`

---

## 一、Skills 索引（8 个核心 Skills）

### 1.1 lovart-seo-reporting（SEO 报告生成工作流）— 主入口
- **路径**: `lovart/lovart-seo-reporting`
- **定位**: 报告执行手册，周报/月报/复盘周报的模板、数据源、洞察格式、OKR 表达规范
- **触发词**: SEO报告、周报、月报、复盘周报、增长日报
- **子 Skills**:
  - `lovart-seo-weekly-brief`（极简版周报）
  - `lovart-seo-weekly-detail`（明细报告）
- **引用文件**: `references/` 含 15 个工作流文档 + 4 个参考文件
- **核心规范**:
  - 报告模板忠实度（不可自创格式）
  - 洞察段落强制格式：`> 💡 **{节名}** — **问题**：… **根源/积极信号**：… **缓解**：…`
  - 复盘周时间窗口：上周三→本周二（7天）
  - 极简版时间窗口：上周二→本周一（7天）
  - GSC 2天延迟，必须标注缺口，使用日均值
  - 品牌词判定：`lovart_brand_match.is_brand()` 5层规则
  - 地区分组：GSC 3-letter country code → 大区
- **数据源**:
  - DataWorks CSV: `1-2 Insight/From Datawork/seo_geo_daily_report_YYYYMMDD.csv`
  - GSC 快照: `Output/Data Ingestion/monthly-snapshots/gsc-YYYY-MM.json`
  - GA4 快照: 同上
  - Bing Webmaster API: `1-4 Dev/scripts/sentinel/bing_credentials/api_key`
  - 竞品词库: `1-2 Insight/Keywords Research/竞品核心非品牌词/`
  - OKR 文件: `1-1 Harness/07-okr/`

### 1.2 lovart-seo-report-pipeline（SEO 报告完整管线）
- **路径**: `lovart/lovart-seo-report-pipeline`
- **定位**: 数据采集管线 — GSC/GA4/Bing 三引擎采集 → 品牌词分类 → 日均化 → 地区分组 → 周报/月报/复盘周报生成 → OKR 追踪
- **执行命令**:
  ```bash
  # 月报（render-only 模式）
  python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month 2026-06 --render-only
  # 自然周报
  python3 "1-4 Dev/scripts/weekly_review_v3.py" --type natural
  # 复盘周报
  python3 "1-4 Dev/scripts/weekly_review_v3.py"
  ```
- **执行前检查清单**: 5 项（快照目录、Python 环境、GA4 结构转换、GSC 5K 取样陷阱、render-only 前置条件）
- **GSC 全维度拉取**: query / country / page / country×query / country×page / device（6维度×2窗口=8+次API调用）
- **地区映射陷阱**: GSC 原始 API 使用 3-letter country code（`ind`, `bra`, `usa`），不是 2-letter

### 1.3 lovart-seo-weekly-brief（复盘周极简版生成器）
- **路径**: `lovart/lovart-seo-weekly-brief`
- **Parent**: `lovart-seo-reporting`
- **触发词**: 极简版周报、brief weekly report、复盘周极简版
- **时间窗口**: 上周二→本周一 vs 上上周二→上周一
- **8 章节固定结构**:
  1. 执行摘要（好的方面 + 需要关注的）
  2. 核心指标（GSC + Bing + DataWorks 注册/付费）
  3. 关键词结构（品牌/非品牌 + Top5 + 排名区间 + Bing）
  4. 渠道分析（DataWorks + GA4 全渠道）
  5. 地区表现（GA4 Top8 国家 + GSC 大区）
  6. 页面品类（首页/Blog/Tools/Features/AI + Top10）
  7. OKR 达成情况
  8. 本周建议（P0/P1/P2）
- **DataWorks 严格模式**: `pt` 必须等于文件名日期
- **强制步骤**: Bing 数据必须先刷新（运行 `bing_fetch.py`），不可直接读缓存

### 1.4 lovart-seo-weekly-detail（周报四项明细报告）
- **路径**: `lovart/lovart-seo-weekly-detail`
- **Parent**: `lovart-seo-weekly-brief`
- **触发条件**: 极简版周报完成后询问用户
- **四项明细**:
  1. Top 100 页面环比明细（含点击/曝光/CTR 环比）
  2. Top 100 关键词品牌/竞品分类明细
  3. 本周更新/优化页面追踪（异常检测）
  4. 上周优化页面本周表现（session_search 交叉对比）
- **竞品词库**: `1-2 Insight/Keywords Research/竞品核心非品牌词/`
- **评价标准**: 🚀 点击+50% / ✅ 正向 / ➡️ 持平 / ❌ 恶化

### 1.5 lovart-trident-data-engine（三引擎 SEO 数据采集与 OKR 对标）
- **路径**: `lovart/lovart-trident-data-engine`
- **定位**: 所有报告（日/周/月/季/年）统一 7 板块结构 + OKR 预测系统
- **环比总则（所有频次适用）**:
  | 频次 | 环比基准 |
  |------|----------|
  | 日报 | 前日 |
  | 自然周报 | 上上周同期（周一〜周日）|
  | 复盘周报 | 上上周三〜上周二 |
  | 极简版 | 上上周二〜上周一 |
  | 月报 | 上一自然月 |
  | 季报 | 上一自然季 |
  | 年报 | 上一自然年 |
- **7 大板块架构**: 核心洞察 + 关键词 + GA4 + 竞品词 + 页面 + 地区 + TODO
- **GSC 拉取维度**: query(5000) + country + country×query + page + country×page + device
- **收录主口径**: 有曝光 URL / 语料库 20,000（**不是** sitemap 提交量÷1000）
- **OKR 目标（2026-05 版）**:
  | OKR | 指标 | 月目标 |
  |-----|------|:-----:|
  | O1 | Organic UV | 960,000 |
  | O1 | 注册（估） | 360,000 |
  | O1 | 付费（估） | 22,800 |
  | O3 | Referral UV | 360,000 |
- **地区分组**: 北美(USA+CAN+GBR+AUS+NZL)、大中华(CHN+HKG+TWN+MAC)、日本(JPN)、南亚(IND+PAK+IDN+BGD)、拉美(BRA+MEX+ARG+COL)、中东非(IRN+EGY+DZA+SAU)

### 1.6 seo-report-analysis（SEO 周报/月报生成 — 旧版）
- **路径**: `lovart/lovart-seo-report-analysis`
- **定位**: 旧版 SEO 报告生成（转化优先视角），含完整 pitfalls 和 OKR 模板
- **核心偏好**: 转化优先 (Conversion > UV > Keywords)
- **DataWorks 字段语义**: `all_*` = 累计所有时间，`new_*` = 当月新增
- **Bing 数据状态**: 已配置 API Key，但 `bing-full.json` 缓存可能过期
- **含 17 个 references**: OKR 基线计算、CRO 方法论、竞品 URL 注册表、多语言内链等

### 1.7 lovart-content-opportunity-scorer（内容机会评分器）
- **路径**: `lovart/lovart-content-opportunity-scorer`
- **定位**: 桥接「分析→创作」闭环 — Trident 三引擎数据自动评分
- **四维评分模型**:
  1. 流量潜力（GSC，权重 0.35）
  2. 竞品缺口（Bing/SERP，权重 0.25）
  3. 商业价值（GA4，权重 0.20）
  4. 实现成本（权重 0.20）
- **品牌词过滤**: `is_brand()` 过滤，品牌词得分 ×0.3
- **输出路由**: MindRe `1-2 Insight/PM/内容机会-YYYY-MM-DD.md`

### 1.8 lovart-sentinel-report（Sentinel 品牌舆情监控）
- **路径**: `lovart/lovart-sentinel-report`
- **与 SEO 报告明确分界**（不含 OKR 看板、关键词分层等 SEO 专属指标）
- **8 大板块**: 关键指标 + 摘要核心发现 + 搜索舆情 + 社媒数据 + 品牌形象 + 用户画像 + 风险机遇 + SWOT+监测阈值 + 行动清单
- **数据源覆盖**: 搜索引擎(5) + 社交媒体(7) + 评价平台(4) + 中国平台(13) + 品牌安全(6) + 内部数据(4) + 竞品(8+)
- **Sentinel 采集三部曲**: `collect.py` → 数据质量审计(Phase 3.5) → `report.py`

---

## 二、Harness 规则体系

### 2.1 RULES-00-iron.md（全局铁律）
- 路径: `1-1 Harness/02-rules/RULES-00-iron.md`
- 范围: 所有 Profile 通用
- 核心条款:
  - **Sanity 管道铁律**: 禁止 `sanity deploy`、`--replace`、修改 `schemaTypes/`、删除 production 文档
  - **产出路由铁律**: 写入文件前必须回答四问（人类 vs 机器、长期 vs 临时、结论 vs 中间、需回溯 vs 不需）
  - **行为铁律**: 不问就干、结论在前、存量改造优先
  - **SEO 报告通用铁律**: 所有维度必须有环比、天数不等用日均值、每节必须有 💡 洞察（问题/根源/缓解）
  - **品牌词分类**: `lovart_brand_match.is_brand()` 精确分类
  - **地区分组**: 南亚(IN+PK+ID)、拉美(BR+MX)、中东非(IR+EG+DZ)
  - **竞品词库**: 265 全量 / 36 核心

### 2.2 RULES-10-reports.md（报告类规则）
- 路径: `1-1 Harness/02-rules/RULES-10-reports.md`
- 加载 Profile: `lovart-reports`
- 核心条款:
  - **环比总则**: 日报(D vs D-1)、周报(上周同期)、月报(上自然月)、季报(上自然季)、年报(上自然年)
  - **环比格式**: 绝对变化 + 百分比 + GSC 点击/曝光/CTR 三者环比
  - **SEO 月报 V2 强制结构**: 13 章节固定顺序（一核心洞察→二OKR看板→三Dashboard A-F→四关键词分层→五GA4→六DataWorks→七品牌vs非品牌→八竞品→九页面目录→十页面查询明细→十一分地区→十二TODO→十三Bing补充）
  - **收录主口径**: 有曝光 URL / 语料库 20,000
  - **代码 SSOT**: `seo_monthly_v2.py` + `lovart_brand_match.py`
  - **Sentinel 舆情**: 8 板块，与 SEO 报告明确分界
  - **GSC 数据量**: 月报 5000 词 / 周报 2000 词 / 日报 200 词

---

## 三、Harness 目录结构

```
1-1 Harness/
├── 02-rules/
│   ├── RULES-00-iron.md          ← 全局铁律（跨Profile）
│   ├── RULES-10-reports.md       ← 报告类规则
│   ├── RULES-20-creation.md      ← 创作类规则
│   ├── RULES-30-quality.md       ← 质量类规则
│   ├── RULES-40-ops.md           ← 运营类规则
│   ├── RULES-50-distribution.md  ← 分发类规则
│   ├── RULES-60-management.md    ← 管理类规则
│   └── SESSION-ROUTING.md        ← 会话路由规则
├── 05-skills/
│   ├── skills-usage.md
│   └── skill-entrypoint-governance.md
├── 07-okr/                       ← OKR 文件（当前6月: Lovart-OKR-2026-06-KR.md）
├── 10-config/
│   └── 产出路由规则.md
├── 11-knowledge/
│   └── scripts/
│       └── fm-fix.py
├── CLAUDE.md
├── Skills/                       ← Harness 级 Skills
│   ├── 02-creation/              （lovart-landing-page, lovart-complete-guide 等）
│   ├── 03-review/                （lovart-content-quality-gates, lovart-content-audit）
│   ├── 04-publish/               （lovart-tools-sanity-publish, lovart-sanity-content-publish 等）
│   └── 06-orchestrate/           （lovart-quality-cascade）
└── .claude/                      ← Claude 代理配置
    ├── agents/                   （lovart-blog, lovart-distributor, lovart-page, lovart-publisher）
    └── skills/                   （镜像 Skills 目录）
```

---

## 四、关键脚本路径（SSOT）

| 脚本 | 路径 |
|------|------|
| 月报生成器 | `1-4 Dev/scripts/seo_monthly_v2.py` |
| 周报复盘 | `1-4 Dev/scripts/weekly_review_v3.py` |
| 品牌词匹配 | `1-4 Dev/scripts/lovart_brand_match.py` |
| 报告标准 | `1-4 Dev/scripts/seo_report_standards.py` |
| GSC 拉取 | `1-4 Dev/scripts/trident/gsc_fetch.py` |
| GA4 拉取 | `1-4 Dev/scripts/trident/ga4_fetch.py` |
| Bing 拉取 | `1-4 Dev/scripts/sentinel/bing_credentials/bing_fetch.py` |
| Sentinel 采集 | `1-4 Dev/scripts/sentinel/collect.py` |
| Sentinel 报告 | `1-4 Dev/scripts/sentinel/report.py` |
| IndexNow 提交 | `1-4 Dev/scripts/multi_seo/indexnow_submit.py` |
| SEO/GEO 指标 | `1-4 Dev/scripts/lovart_seo_geo_metrics.py` |
| 凭证路径 | `1-4 Dev/scripts/trident/credential_paths.py` |

---

## 五、报告产出路径

| 报告类型 | 输出路径 |
|----------|----------|
| 月报 | `1-2 Insight/Trident Insights/reports/monthly/Lovart-SEO-YYYY-MM.md` |
| 自然周报 | `1-2 Insight/Trident Insights/reports/weekly/` |
| 复盘周极简版 | `1-2 Insight/Trident Insights/reports/weekly/Lovart-SEO-review-YYYY-MM-DD-YYYY-MM-DD-brief.md` |
| 复盘周明细 | `1-2 Insight/Trident Insights/reports/weekly/Lovart-SEO-detail-YYYY-MM-DD-YYYY-MM-DD.md` |
| Blog 盘点报告 | `1-2 Insight/Keywords Research/Lovart.ai 英文 Blog 全量盘点报告.md` |
| 内容机会 | `1-2 Insight/PM/内容机会-YYYY-MM-DD.md` |
| Sentinel 日报 | `1-2 Insight/Lovart ORM/daily/` |
| Sentinel 周报 | `1-2 Insight/Lovart ORM/weekly/` |
| Sentinel 月报 | `1-2 Insight/Lovart ORM/monthly/` |

---

## 六、各频次报告对比

| 维度 | 日报 | 自然周报 | 复盘周报 | 极简版 | 月报 | 季报 | 年报 |
|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| GSC 词量 | 200 | 2,000 | 2,000 | 2,000 | 5,000 | 5,000×3 | 5,000×12 |
| 板块数 | 7 | 7 | 7 | 8 | 13 | 7+季度专属 | 7+年度专属 |
| OKR 位置 | 开头 | 开头 | 开头 | §七 | §二 | 开头 | 开头 |
| 竞品词 | ✅ | ✅ | ✅ | 不单独列节 | ✅(§八) | ✅ | ✅ |
| Bing | — | — | — | 附在§三 | ✅(§十三) | ✅ | ✅ |
| 趋势表 | 7日迷你 | 4周 | 4周 | 4周 | 年月均 | 3月逐月 | 12月逐月 |
| 地区粒度 | 5区/Top5词 | 5区/Top5词+页面 | 同周报 | Top8国家+GSC大区 | 每区mini月报+Top15 | 逐月趋势 | 逐月趋势 |
| 洞察格式 | 简版💡 | 💡三要素 | 💡三要素 | 💡三要素 | 💡+📊年均 | 💡+📊年均 | 💡+📊年均 |

---

## 七、常见陷阱速查（P0 高发）

1. **DataWorks CSV 双日期陷阱** — 每个文件含当日+7天前两天的数据，`pt` 字段区分。未过滤+去重 → 绝对值 2 倍膨胀。修复：严格模式 `pt == 文件名日期`。
2. **Bing 缓存时效** — `bing-full.json` 可能早于报告窗口。修复：周报/月报前必须先运行 `bing_fetch.py`。
3. **Python 环境不兼容** — 系统 Python 3.9 与 cryptography 包不兼容。修复：用 `~/.local/bin/python3.11` 执行。
4. **GSC country 代码** — 原始 API 返回 3-letter（`ind`, `bra`, `usa`），不是 2-letter。用 2-letter 映射会导致所有国家落入「其他」。
5. **品牌分类不可用简单子串** — 必须用 `lovart_brand_match.is_brand()` 五层规则。`l o v a r t`（含空格）在 Bing 上也是品牌词。
6. **GSC 5K 取样 vs 原始 25K** — 快照仅含 Top 5K（~25% 全量），跨月环比可能扭曲。需在报告头部注明口径差异。
7. **天数不对等比绝对值** — 必须全部换算成日均值再对比。
8. **GA4 快照结构不匹配** — 原始快照 `channels: []`，脚本期望 `channels: {}`，需提前转换。
9. **all_pay_amount ≠ 当月新增** — `all_*` 是累计所有时间。当月新增用 `new_pay_amount`。
10. **收录率不能用 sitemap** — 主口径是有曝光 URL / 语料库 20,000，禁止用 page API 前 1000 ÷ sitemap submitted。

---

## 八、数据源总表

| 数据引擎 | 来源 | 频率 | 路径/API |
|----------|------|:--:|----------|
| GSC | Google Search Console API | 月/周/日 | `1-4 Dev/scripts/sentinel/gsc_credentials/gsc-token.json` |
| GA4 | Google Analytics 4 API | 月/周 | `1-4 Dev/scripts/sentinel/ga4_credentials/ga4-token.json`（Property: 403618427）|
| Bing | Bing Webmaster SOAP API | 月/周 | `1-4 Dev/scripts/sentinel/bing_credentials/api_key` |
| DataWorks | 产品日度 CSV | 日 | `1-2 Insight/From Datawork/seo_geo_daily_report_YYYYMMDD.csv` |
| 竞品词库 | 手工维护 | 静态 | `1-2 Insight/Keywords Research/竞品核心非品牌词/` |
| 品牌词匹配 | `lovart_brand_match.py` | 实时 | `1-4 Dev/scripts/lovart_brand_match.py` |
| Sanity CMS | Sanity API | 按需 | Project `o11tm2qe`, dataset `production` |
| OKR | Markdown 文件 | 月 | `1-1 Harness/07-okr/` |
