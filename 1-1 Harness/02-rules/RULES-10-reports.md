---
type: rule
version: 1.0
updated: 2026-07-05
scope: "profile-report-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-10-reports.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 10 报告类（Reports）

> 适用路线：SEO 报告、舆情报告、竞品报告、SERP 报告、OKR 完成度
> 加载 Profile：`lovart-reports`

---

## 环比总则

**任何报告、任何维度，都必须有环比。** 不允许只出当期 snapshot。

| 报告 | 环比基准 | 示例 |
|------|----------|------|
| 日报 | 前日 | D vs D-1 |
| 自然周报 | 上上周同期（周一～周日） | — |
| 复盘周报 | 上上周三～上周二 | — |
| 月报 | 上一自然月 | 2026-05 vs 2026-04 |
| 季报 | 上一自然季 | Q2 vs Q1 |
| 年报 | 上一自然年 | 2026 vs 2025 |

环比格式：绝对变化 + 百分比（`↓-218,884 / -27.9%`）。GSC 关键词：**点击+曝光+CTR 三者环比**齐全。天数不等用日均值。

## OKR 目标

默认 **2026-05** 版。Agent 跑报告前必须问用户是否更新。

| OKR | 指标 | 月目标 |
|-----|------|:-----:|
| O1 | Organic UV | 960,000 |
| O1 | 注册（估） | 360,000 |
| O1 | 付费（估） | 22,800 |
| O3 | Referral UV | 360,000 |

转化率：O1 UV→注册 37.5%，注册→付费 6.3%；O3 UV→注册 11.7%，注册→付费 7.1%

## SEO 月报 V2 强制结构（13 章节）

固定顺序：一(核心洞察) → 二(OKR看板) → 三(Dashboard A-F + C-Bing/D-Bing/E-Bing) → 四(关键词分层 Google+Bing) → 五(GA4用户数据) → 六(DataWorks产品数据) → 七(品牌vs非品牌) → 八(竞品非品牌词) → 九(页面目录流量) → 十(页面查询明细) → 十一(分地区) → 十二(TODO) → 十三(Bing补充)

- 关键词表：点击+曝光+CTR + 三者环比 + 点击占比+曝光占比
- 地区每区 mini 月报 + Top15 品牌/非品牌词 + Top10 页面
- 每节 💡 洞察（问题/根源/缓解）+ 📊 年均对比
- 收录主口径：有曝光 URL / 语料库 20,000（**不是** sitemap 提交量÷1000）
- 代码 SSOT：`seo_monthly_v2.py` + `lovart_brand_match.py`

## 品牌词分类

品牌词 = lovart/loveart/lovert/lavart/lavort 等变体，含多语言 typo。代码 SSOT：`lovart_brand_match.py`（改 regex 只改一处）。

## 竞品词匹配

词库规模：265 全量 / 36 核心。子串匹配。输出：命中数、覆盖率、分层表现、缺失分析。

## 地区分组（固定，不可改）

| 分组 | 包含 |
|------|------|
| 北美 | 美国+加拿大+英国+澳大利亚+新西兰 |
| 大中华 | 中国大陆+香港+台湾+澳门 |
| 日本 | 日本 |
| 南亚 | 印度+巴基斯坦+印尼 |
| 拉美 | 巴西+墨西哥 |
| 中东非洲 | 伊朗+埃及+阿尔及利亚 |
| 其他 | 其余国家 |

## Sentinel 舆情（8 板块）

板块：关键指标 + 摘要核心发现 + 搜索舆情 + 社媒数据 + 品牌形象 + 用户画像 + 风险机遇 + SWOT+监测阈值 + 行动清单。与 SEO 报告明确分界（不含 OKR 看板、关键词分层等 SEO 专属指标）。

## GSC 数据量

月报 5000 词 / 周报 2000 词 / 日报 200 词。全维度：query/country/page/country×query/device。有 2 天延迟。
