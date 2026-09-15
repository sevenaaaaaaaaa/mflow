# For SEO 负责人

> **文档定位**：面向 SEO 负责人的操作指南  
> **更新日期**：2026-06-04  
> **适用范围**：Lovart 项目 SEO 报告生成和优化相关人员

---

## 一、概述

本文档为 SEO 负责人提供完整的操作指南，涵盖 SEO 报告标准、三引擎架构、报告生成流程、数据源和产出路径等核心内容。

### 1.1 三引擎架构

SEO 报告基于三引擎架构：

```
GSC API + GA4 API + 竞品词库（265+36词）
  ├── GSC: 关键词排名、点击、曝光、CTR
  ├── GA4: 用户行为、会话、转化
  └── 竞品词库: 竞品词覆盖分析、缺失分析
```

### 1.2 报告类型

| 报告类型 | 时间窗口 | 环比基准 | 数据量 |
|----------|----------|----------|--------|
| **日报** | 昨日 | 前日 | 200 词 |
| **自然周报** | 上周一～上周日 | 上上周同期 | 2,000 词 |
| **复盘周报** | 上周三～本周二 | 上上周三～上周二 | 2,000 词 |
| **月报** | 报告月全月 | 上一自然月 | 5,000 词 |
| **季报** | 报告季全季 | 上一自然季 | 5,000 词 |
| **年报** | 报告年全年 | 上一自然年 | 5,000 词 |

---

## 二、SEO 报告标准

### 2.1 环比总则（所有频次、所有维度）

**任何 SEO 报告、任何数据维度，都必须有环比。** 不允许只出当期 snapshot。

| 报告类型 | 当前周期（示例） | 环比基准（默认） |
|----------|------------------|------------------|
| **日报** | 昨日 YYYY-MM-DD | **前日** YYYY-MM-DD |
| **自然周报** | 上周一～上周日 | **上上周**同期（周一～周日） |
| **复盘周报** | 上周三～本周二 | **上上周三～上周二** |
| **月报** | 报告月全月（如 2026-05） | **上一自然月**全月（如 2026-04） |
| **季报** | 报告季全季（如 2026-Q2） | **上一自然季**（如 2026-Q1） |
| **年报** | 报告年全年（如 2026） | **上一自然年**（如 2025） |

**命名约定：** 用户说「5 月月报」→ 默认 **5 月 vs 4 月**；说「5 月周报」→ 默认该周 vs **紧邻上一同等长度周期**（常跨月落在 4 月末，合法）。

**环比列格式：** 绝对变化 + 百分比（如 `↓-218,884 / -27.9%`）。GSC 关键词相关必须 **点击环比 + 曝光环比 + CTR 环比** 三列齐全。

⚠️ GSC 有 2 天延迟；窗口末尾不可用时拉取至最后可用日，并在报告顶部标注；环比窗口须等长（如 5d vs 5d）。

### 2.2 OKR 目标（跑报告前须确认）

| 项 | 规则 |
|----|------|
| **当前生效版本** | **2026-05**（用户提供的 OKR 目标，见 A4 数值） |
| **Agent 跑报告前** | **必须询问用户**：OKR 目标是否要更新？未确认则沿用 A4 默认值 |
| **脚本默认** | `seo_report_standards.OKR_EFFECTIVE_MONTH = "2026-05"` |

### 2.3 关键词与细分统计（强制字段）

**凡与 GSC 关键词/查询相关的表格**（含 Top N、品牌/非品牌、竞品命中、地区 Top 词、页面 query）：

| 当期 | 环比 |
|------|------|
| 点击、曝光、CTR | 点击环比、曝光环比、CTR 环比 |

**凡细分统计**（Top N 分层、地区、目录、渠道占比、竞品分层等）：

| 必须含 |
|--------|
| **点击占比** + **曝光占比**（相对当期总量或父级合计） |

GA4 指标（Sessions、Users 等）同样须环比；渠道表须 Sessions 占比环比。

代码 SSOT：`1-4 Dev/scripts/seo_report_standards.py`（与本文 Part A 同步）。

### 2.4 月报 V2 强制结构

**生成命令：**

```bash
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month YYYY-MM          # 全量拉数
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month YYYY-MM --resume # 断点续跑（GSC/GA4 快照）
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month YYYY-MM --render-only  # 仅重渲染（须已有快照）
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month YYYY-MM --resume --refresh-indexing  # 重拉收录分页
```

**实现模块：** `seo_monthly_v2.py` + `seo_monthly_extras.py` + `lovart_brand_match.py` + `lovart_indexing_metrics.py`；快照目录 `1-4 Dev/Output/Data Ingestion/monthly-snapshots/`；收录缓存 `indexing-YYYY-MM.json`；年均缓存 `1-2 Insight/Trident Insights/reports/monthly/.metrics/`。

**固定章节顺序（大标题 + 子号；2026-06 起生效）：**

| 顺序 | 板块 | 强制内容 |
|:--:|------|----------|
| 一 | **核心洞察** | 置顶；**三层叙事**：（一）自然搜索产品 UV/注册/新增付费/累计付费/转化率（二）收录·关键词·页面（三）综合下一步+大区；DataWorks SEO+GEO；**顶部三层 TL;DR（流量/关键词/执行）+ 每要点首句加粗「一句话结论」**；正文仅核心数据+环比，其余「详见 §X」 |
| 二 | **OKR 月达成看板** | O1 访问 UV（DataWorks `all_uv`）/新增注册/新增付费、O3 Referral 访问 UV（估）/注册（估）、O2 质量、GA4 Sessions 参考行；含月目标、环比月、报告月、达成率、环比 |
| 三 | **SEO Dashboard** | 卡 **A** 全渠道 DAU 比例（DataWorks 日均）→ **B** 自然搜索用户大盘数据（DataWorks 综合）→ **C** GSC 关键词全站 → **D** Top 分层 → **E** 品牌 vs 非品牌 → **F** GA4+收录+竞品 |
| 四 | **关键词分层明细** | 4.1 Top N（3/5/10/30/50/100）：**点击+曝光+CTR+占比+点击/曝光/CTR 环比**；4.2/4.3 品牌/非品牌 Top10；**4.4 点击增长 Top15 movers**；**4.5 曝光增长 Top15**；**4.6 CTR 变化 Top15**（曝光≥100）；**4.7 点击下滑 Top15**；节末 **💡 + 📊 年均对比** |
| 五 | **自然搜索用户数据（GA4）** | 5.1~5.3 + 节末 **💡 + 年均对比** |
| 六 | **自然搜索产品数据（DataWorks 平台拆解）** | 6.1 渠道汇总（SEO/GEO/合计）+ 6.2 SEO 平台 + 6.3 GEO 平台 + GA4 口径脚注 |
| 七 | **品牌词 vs 非品牌词** | 点击/曝光/数量/占比 + 环比 + **💡 + 年均对比** |
| 八 | **竞品非品牌词覆盖** | 8.1~8.5 + missing core 列表 + **💡 + 年均对比** |
| 九 | **页面目录流量** | 9.1 双月+点击/曝光占比+环比；9.2 核心目录；9.3 多语言类型 + **💡 + 年均对比** |
| 十 | **页面查询明细** | Top 20 URL |
| 十一 | **分地区表现** | **11.0** 大区最好/持平/最差总览；11.1 GSC 汇总；11.1b 各区品牌/非品牌；**11.2–11.8 分区月报（双月）**（CTR/点击占比/曝光占比环比、Top15 词双月、Top10 页面双月、💡）；11.9 地区 GA4 |
| 十二 | TODO | P0/P1/P2 + 数据依据 |
| 十三 | Bing | 全量历史补充 |

**💡 洞察段落格式（每节末尾）：** `> 💡 **{节名}** — **问题**：… **根源/积极信号**：… **缓解**：…`（不可省略）。

**📊 年均对比（月报/季/年）：** `> 📊 **年均对比** — 当月 X ｜ 2026 YTD 月均 (N个月) Y ｜ 2025 月均 (M个月) Z`；无 2025 缓存时 Z 为 `—`，须补跑历史或写入 `.metrics/`。

**地区：** `REGION_ORDER` = 北美 / 大中华 / 日本 / 拉美 / 南亚 / 中东非洲 / 其他；GSC 须拉 `country×query`（大区品牌/非品牌）+ `country×page`（大区 Top 页面，失败可回退全站 Top10）。

**页面分类：** 与 `weekly_review_v3.py` 的 `classify_page()` 一致（首页、语言首页-xx、i18n内页、tools/features/blog 等），**禁止** 92% 落入 `other`。

---

## 三、报告质量标准

| # | 规则 | 说明 |
|---|------|------|
| 1 | **全部 7 板块** | 日/周/月/季/年报统一含：核心洞察 + 关键词 + GA4 + 竞品词 + 页面 + 地区 + TODO。不可因时间维度短而缩水 |
| 2 | **三数据维度** | 所有表格必须含点击+曝光+CTR，不可只有点击 |
| 3 | **环比** | **所有维度、所有频次**必须有环比（见 A0）。表格含变化列（绝对值+百分比） |
| 4 | **占比** | 地区/目录/Top 分层/渠道等细分须 **点击占比+曝光占比**；地区表双占比均须环比时可加占比变化列 |
| 5 | **深度洞察** | 每节末尾有 💡 洞察段落（暴露问题+积极出路+数据依据），不可只罗列数据 |
| 6 | **正面视角** | 核心洞察每条配建设性/积极视角 |
| 7 | **竞品词库** | 用真实 265 词库（来自 `1-2 Insight/Trident Insights/竞品核心非品牌词/` + 36 核心词），不用硬编码假词库 |
| 8 | **页面分类** | 首页独立列出为目录分类（**不可混入 "other"**）。canvas/login/auth 功能页独立 |
| 9 | **多语言** | 页面分析含多语言对比表（2+语言版本×6语言列，按slug聚合合并多语言变体） |
| 10 | **地区完整** | **月报**：每大区 **mini 月报**（GSC+品牌/非品牌+GA4+Top10 页面）+ **Top15** 品牌/非品牌词；**周报**：Top5 双表 + GA4 + Top5 页面；全部含环比 |
| 11 | **截断检查** | 写入后验证文档末尾包含最终章节，**不可截断** |
| 12 | **收录数据** | 主口径：有曝光 URL / 语料库 20k（~46% 量级）；见 **A0e** |
| 13 | **GSC 数据量** | 月报 5,000 词 / 周报 2,000 词 / 日报 200 词。不可缩减 |
| 14 | **全维度环比** | GSC 关键词：**点击+曝光+CTR 三者环比**；其他表格至少含主要指标环比 |
| 15 | **分层占比** | Top N、地区、目录、品牌/非品牌拆分：**点击占比+曝光占比** 不可缺 |
| 16 | **品牌词过筛** | SSOT：`lovart_brand_match.py`（禁止各脚本重复 `is_brand`）。含 lavort、lavart、lovert、`\blav[o0]rt\b` 等 typo；lova/love/art 变体+多语言 |
| 17 | **GA4 地区兼容** | `country_group()` 必须同时接受 GSC 缩写（usa/bra/ind）和 GA4 全名（United States/Brazil/India） |
| 18 | **曝光占比验证** | 所有地区曝光占比总和必须 ≤100%（±1%误差），总和>100% 视为计算错误 |
| 19 | **地区子区域拆分** | 「其他」必须拆为拉美/南亚/中东非洲/其他，不可合并为 80%+ catch-all |

---

## 四、地区定义（固定，不可改）

| 分组 | 包含国家 |
|------|----------|
| 北美 | 美国 + 加拿大 + 英国 + 澳大利亚 + 新西兰 |
| 大中华 | 中国大陆 + 香港 + 台湾 + **澳门** |
| 日本 | 日本 |
| 其他 | 所有其余国家 |

---

## 五、品牌词分类规则

> **🚨 SSOT 铁律**：品牌词分类的唯一代码来源是 `1-4 Dev/scripts/lovart_brand_match.py`。**禁止**在任何 Skill/报告/工作流中硬编码品牌词列表。所有品牌词判定必须通过 `is_brand()` 函数。

```python
from lovart_brand_match import is_brand, partition_keywords
brand, nonbrand = partition_keywords(keywords)
```

### 5 层匹配规则（详见 `lovart_brand_match.py`）

1. **正则匹配** — 40+ pattern：lovart/loveart/lovert/lavort 及多语言变体（日/韩/阿/俄/中文）
2. **分词匹配** — multi-token：lo+art、love+art 等组合
3. **紧凑形式匹配** — Levenshtein ≤ 2 模糊匹配
4. **模糊 token 匹配** — 品牌词根 + 排除列表（logo/login/local 等非品牌词）
5. **音译匹配** — 日文(ロバート)、韩文(로바트)、中文(洛瓦特)、阿拉伯文(لوفارت)、俄文(ловарт)

**代码 SSOT**：`1-4 Dev/scripts/lovart_brand_match.py` + `test_brand_match.py`（改 regex 只改一处）。

---

## 六、OKR 固定数据

> **生效版本：2026-05**（用户提供）。Agent **每次生成报告前**须问用户是否更新；未更新则使用下表。

**目标值：**

| OKR | 指标 | 日目标 | 周目标 | 月目标 |
|-----|------|:-----:|:-----:|:-----:|
| O1 | Organic UV | 32,000 | 224,000 | 960,000 |
| O1 | 注册（估） | 12,000 | 84,000 | 360,000 |
| O1 | 付费（估） | 760 | 5,320 | 22,800 |
| O3 | Referral UV | 12,000 | 84,000 | 360,000 |
| O3 | 注册（估） | 1,400 | 9,800 | 42,000 |
| O3 | 付费（估） | 100 | 700 | 3,000 |

**转化率（用于注册/付费估算）：**

| 路径 | 比率 |
|------|------|
| O1: Organic UV → 注册 | 37.5% |
| O1: 注册 → 付费 | 6.3% |
| O3: Referral UV → 注册 | 11.7% |
| O3: 注册 → 付费 | 7.1% |
| O2 | 无固定比率，通过全渠道UV增长+访客质量间接评估 |

---

## 七、各频次额外要求

| 要求 | 日报 | 周报 | 月报 | 季报 | 年报 |
|------|:--:|:--:|:--:|:--:|:--:|
| GA4 新老用户分层 | ✅ | ✅ | ✅ | ✅ | ✅ |
| GA4 全渠道占比 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 地区品牌/非品牌 Top5（周报）/ **Top15 + mini 月报（月报）** | ✅ | ✅ | ✅ | ✅ | ✅ |
| 地区 Top5 页面（周报）/ **Top10 页面（月报 mini）** | — | ✅ | ✅ | ✅ | ✅ |
| 关键词 movers（点击/曝光/CTR 变化 Top15） | — | — | ✅ | — | — |
| 各节 💡 洞察 + 📊 年均对比 | — | ✅ | ✅ | ✅ | ✅ |
| 收录数据 | — | ✅ | ✅ | ✅ | ✅ |
| 多语言页面对比(聚合slug) | — | — | ✅ | ✅ | ✅ |
| 年均对比备注 | — | — | ✅ | ✅ | ✅ |
| Bing补充 | — | — | ✅ | ✅ | ✅ |
| 趋势表 | 7日迷你 | 4周趋势 | — | 3月逐月 | 12月逐月 |
| OKR看板 | 日达成率 | 周达成率 | 月达成率 | 季达成率 | 年达成率 |

---

## 八、竞品词匹配引擎（SEO + Sentinel 共用）

竞品词库是三引擎之一，SEO 报告和 Sentinel 舆情报告共同调用。

```
GSC N 关键词 × 竞品 265 全量词（子串匹配）
  ├── Full Match: 宽口径，所有竞品词变体
  ├── Core Match: 严口径，36 个高优先级核心词
  ├── SEO 报告: 覆盖率+分层表现+缺失分析
  └── Sentinel: 行业词变化检测+竞品种子词对比
```

---

## 九、关键数据参考

| 数据 | 值 |
|------|-----|
| 收录数 | 9,268 / 20,000 (46.34%) |
| 竞品词库规模 | 265 全量 / 36 核心 |
| GA4 Property | 403618427 |
| GSC Site | `https://www.lovart.ai/` |

---

## 十、报告生成脚本

| 报告 | 脚本 |
|------|------|
| 月报 | `1-4 Dev/scripts/seo_monthly_v2.py`（逻辑：`seo_monthly_extras.py`；标准：`seo_report_standards.py`） |
| 复盘周报 | `1-4 Dev/scripts/weekly_review_v3.py` |
| 日报 | `1-4 Dev/scripts/sentinel/collect.py` |

---

## 十一、三引擎脚本链

| 步骤 | 脚本 | 引擎 | 用途 |
|:---:|------|------|------|
| 1 | `1-1 Harness/Skills/lovart-trident-data-engine/scripts/gsc_fetch.py` | GSC | 关键词拉取（月报 5K/周报 2K/日报 200） |
| 2 | `1-1 Harness/Skills/lovart-trident-data-engine/scripts/ga4_fetch.py` | GA4 | 全维度用户数据（Sessions/Users/Segments/Channels/Geo） |
| 3 | `1-4 Dev/scripts/competitor_deep_match.py` | 竞品词库 | 265全量词 + 36核心词 × GSC 关键词 子串匹配 |
| 4 | `1-1 Harness/Skills/lovart-trident-data-engine/scripts/unified_brief.py` | 汇总 | 三引擎统一情报摘要 |
| — | `1-4 Dev/scripts/seo_monthly_v2.py` | 生成 | 月报 V2（含 `seo_monthly_extras.py`：OKR/洞察/movers/分区 mini） |
| — | `1-4 Dev/scripts/weekly_review_v3.py` | 生成 | 周报最终生成（调用引擎 1-3） |

---

## 十二、一键运行

```bash
# 全量采集（GSC+GA4+Bing）
cd 1-1 Harness/Skills/lovart-trident-data-engine && bash scripts/run_all.sh

# 月报 V2（环比=上一自然月；详见 AGENTS.md A0d）
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month 2026-05
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month 2026-05 --resume       # GSC/GA4 快照断点续跑
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month 2026-05 --render-only  # 仅重渲染（改模板后）

# 复盘周报
python3 "1-4 Dev/scripts/weekly_review_v3.py"

# 仅竞品词匹配
python3 "1-4 Dev/scripts/competitor_deep_match.py"
```

---

## 十三、产出路径

| 频次 | 路径 |
|------|------|
| 月报 | `1-2 Insight/Trident Insights/reports/monthly/Lovart-SEO-YYYY-MM.md` |
| 周报 | `1-2 Insight/Trident Insights/reports/weekly/Lovart-SEO-review-YYYY-MM-DD-YYYY-MM-DD.md` |
| 日报 | `1-2 Insight/Trident Insights/reports/daily/Lovart-SEO-YYYY-MM-DD.md` |
| 季报 | `1-2 Insight/Trident Insights/reports/quarterly/Lovart-SEO-YYYY-QX.md` |
| 年报 | `1-2 Insight/Trident Insights/reports/annual/Lovart-SEO-YYYY-Annual.md` |

---

## 十四、数据依赖

| 依赖 | 位置 |
|------|------|
| 竞品词库（265+36） | `1-2 Insight/Trident Insights/竞品核心非品牌词/lovart_competitors_keywords.md` |
| GSC 5K JSON | `1-4 Dev/Output/Data Ingestion/gsc-5k-YYYY-MM.json` |
| GSC/GA4 月报快照 | `1-4 Dev/Output/Data Ingestion/monthly-snapshots/{gsc,ga4}-YYYY-MM.json` |
| 月报年均 metrics | `1-2 Insight/Trident Insights/reports/monthly/.metrics/YYYY-MM.json` |
| 收录缓存 / 语料库基线（可选） | `1-4 Dev/Output/Data Ingestion/indexing-YYYY-MM.json`；`1-2 Insight/Trident Insights/reports/indexing-baseline.json` |
| GA4 JSON | `1-4 Dev/Output/Data Ingestion/ga4-YYYY-MM.json` |
| 竞品词 JSON | `1-2 Insight/Trident Insights/reports/competitor_keywords.json` |
| Bing 数据 | `1-2 Insight/Trident Insights/reports/bing-full.json`（月报补充，文末） |

---

## 十五、检查清单（每次报告后自检）

- [ ] 报告类型环比基准正确（A0 表：月报=上自然月，周报=上同型周，等）
- [ ] 全部 7 板块都存在（不截断）
- [ ] **关键词相关**表格：点击+曝光+CTR + **三者环比**
- [ ] **细分**（Top/地区/目录）：点击占比+曝光占比
- [ ] GA4 / 竞品 / 页面等非关键词维度亦有环比
- [ ] 竞品词用真实 265 词库
- [ ] 首页独立列为目录
- [ ] **月报**：固定顺序 一～十三；§一 含 **30秒速览+🔴P0+TL;DR**（A0g）；§三 卡 A–F + **C-Bing/D-Bing/E-Bing**；§四–§十一 Google+Bing 对称（§4.12–4.16、§11.10 等）
- [ ] **月报**：§4.4–4.7 movers；§4.1 含曝光+CTR+三者环比
- [ ] **月报**：§11.0 大区总览；每区 **分区月报（双月）** + Top15；CTR/占比有环比
- [ ] **月报**：收录率 ~40%+（非 1.43%）；**lavort** 不在非品牌 Top10
- [ ] 每节（关键词/GA4/品牌/竞品/页面/地区）有 **💡**；月报有 **📊 年均对比**
- [ ] 核心洞察有正面视角 + 可执行缓解动作
- [ ] 地区定义正确（北美=5国，大中华=4地区）
- [ ] OKR：跑前已问用户是否更新（默认 2026-05 版）

---

## 十六、常见错误（Agent 禁止再犯）

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| 章节顺序乱/编号重复 | 严格按固定顺序 一～十三；子号随大号（4.x/5.x/6.x/8.x/9.x/11.x） |
| 核心洞察 5 条泛泛而谈，无首页/品牌 vs 内页/非品牌分工 | 三层叙事 + 顶部三层 TL;DR（流量/关键词/执行）+ 每要点首句加粗结论 + 明确页面/关键词布局 |
| 核心洞察正文密密麻麻堆全量数字 | 每点只留核心数据+环比（≤2 个数），其余「详见 §X / 卡 X」 |
| 关键词 §4.1 只有点击分层 | 含曝光、CTR、三者环比 + §4.4–4.7 movers |
| 地区每区仅 Top5 品牌/非品牌两张表 | 每区 **mini 月报** + **Top15** 词 |
| 无各节 💡 洞察 | 四～九、十一（总览+各区）均有 💡 |
| 无 2025/2026 年均备注 | 每节末 📊 年均对比（有缓存则填数） |
| 重跑月报时全量删改旧 Markdown | **增量**改脚本/模板，用 `--render-only` 重渲染 |
| 分区洞察品牌占比恒为 0% | `section_insight_region` 传入大区 `region_stats` 的 brand/nonbrand，勿把整个 map 当单区 dict |
| API 中断后从头拉 | 使用 `--resume` 读 `monthly-snapshots/` |
| 收录率恒为 1.43%（1000/70k） | `lovart_indexing_metrics` 分页 + 语料库 20k 主口径 |
| lavort 出现在非品牌 Top10 | 品牌 regex 只改 `lovart_brand_match.py` |
| Dashboard 单表混排 GSC/GA4/收录 | §三 卡 A–F 分开 |

---

## 十七、相关文档

- [AGENTS.md](./AGENTS.md) - 项目规则和标准
- [WORKFLOWS.md](./WORKFLOWS.md) - 运维手册
- [For-北美市场.md](./For-北美市场.md) - 北美市场操作指南
- [For-日本市场.md](./For-日本市场.md) - 日本市场操作指南
- [For-数据对接分析师.md](./For-数据对接分析师.md) - 数据对接操作指南

---

> **维护者**：Lovart 团队  
> **最后更新**：2026-06-04  
> **版本**：V1.0
