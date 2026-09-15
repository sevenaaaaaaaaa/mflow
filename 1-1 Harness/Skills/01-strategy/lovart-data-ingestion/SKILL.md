# lovart-data-ingestion

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-data-ingestion/SKILL.md` |

Step 1 of Lovart Content Pipeline — 拉取 GSC + GA4 + Bing 三源数据，生成全渠道情报摘要。

## Triggers

- "拉取最新数据" / "pull latest data"
- Sentinel 报告落地到 `1-2 Insight/Lovart ORM/` 后自动触发

## Triggers

- "拉取最新数据" / "pull latest data"
- "更新关键词研究" / "update keyword research"
- "数据采集" / "data ingestion"
- "扫描信息" / "scan all sources"
- Sentinel 报告落地到 `1-2 Insight/Lovart ORM/` 后自动触发
- Pipeline Orchestrator 调用 Step 1

## Prerequisites

- GSC API 配置（见 `Skills/lovart-gsc-api-setup-guide.md`）或 Notion 数据库已配置（见 `Skills/lovart-notion-config.md`）或本地 CSV 已导出
- Sentinel 配置完成（`1-4 Dev/scripts/sentinel/config.yaml`）
- 网络可用

## 数据源三级降级策略

```
┌─────────────────────────────────────┐
│ 1️⃣ GSC API (优先)                    │
│    └─ 失败/未配置 → 降级到 Notion     │
│                                       │
│ 2️⃣ Notion 数据库 (次选)              │
│    └─ 失败/未配置 → 降级到本地 CSV    │
│                                       │
│ 3️⃣ 本地 CSV (最后兜底)               │
│    扫描 1-6 Knowledge Base/        │
│    1-2 Insight/Keywords Research/         │
│    Daily Raw Data/                    │
└─────────────────────────────────────┘
```

### Phase 1a: GSC API 拉取（优先）

```bash
# GSC API 已配置 ✅
# 脚本: 1-4 Dev/scripts/sentinel/gsc_credentials/gsc_fetch.py
# 认证: gsc-token.json（OAuth 2.0 refresh token，自动续期）
# 拉取范围：最近 28 天，关键词/页面/国家/设备四维度
python3 1-4 Dev/scripts/sentinel/gsc_credentials/gsc_fetch.py
```

输出到：`1-2 Insight/Trident Insights/reports/keyword-digest.json`

### Phase 1b: GA4 流量拉取（并行）

```bash
# GA4 API 已配置 ✅
# 脚本: 1-4 Dev/scripts/sentinel/ga4_credentials/ga4_fetch.py
# Property: properties/403618427 (lovart.ai)
# 拉取范围：最近 30 天，流量渠道/着陆页/设备/国家
python3 1-4 Dev/scripts/sentinel/ga4_credentials/ga4_fetch.py
```

输出到：`1-2 Insight/Trident Insights/reports/ga4-digest.json`

### Phase 1c: Notion 拉取（GSC 降级）

如 GSC API 不可用，从 Notion Daily Keyword Tracker 读取：

```bash
# Database ID: 371fc0c7-1bd5-811c-af7f-fd50d065e869
# 查询最近 7 天、按点击降序
curl -s -X POST "https://api.notion.com/v1/databases/371fc0c7-1bd5-811c-af7f-fd50d065e869/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"sorts":[{"property":"Clicks","direction":"descending"}],"filter":{"property":"Date","date":{"past_week":{}}}}'
```

配置：`Skills/lovart-notion-config.md`

### Phase 1d: 本地 CSV 拉取（兜底）

扫描目录获取最新日期的 CSV：

```
1-2 1-2 Insight/Keywords Research/
├── Daily Raw Data/                                    ← GSC 日度 CSV
│   ├── www.lovart.ai_SearchPerformanceOverview_All_*.csv
│   └── GSC___www.lovart.ai_-Performance-on-Search-YYYY-MM-DD/
│       ├── 查询数.csv（关键词维度）
│       ├── 网页.csv（页面维度）
│       ├── 国家_地区.csv（地域维度）
│       └── 设备.csv（设备维度）
├── Weekly Raw Data/
│   ├── 谷歌 SEO 数据/谷歌 SEO 2026 年 X 月/      ← GSC 周度 CSV
│   ├── Bing SEO 数据/必应 SEO X 月/               ← Bing CSV
│   └── 用户获取情况/                                ← GA4 用户获取
└── reports/                                          ← Trident Insights 产出
    ├── SEO周报_YYYYMMDD-YYYYMMDD.md
    └── 品牌词非品牌词_*.md
```

**操作步骤**：

1. **检查最新 CSV 日期**：
   ```bash
   ls -lt "1-2 1-2 Insight/Keywords Research/Daily Raw Data/" | head -5
   ```
   若最新文件 > 2 天前 → 降级到下一级数据源。

2. **解析关键词 CSV**：提取 `查询` / `点击次数` / `展示次数` / `CTR` / `排名`
   - Top 50 关键词（按点击降序）
   - 标记排名变化 > ±5 的「异动词」

3. **解析页面 CSV**：Top 30 流量页面，标记新进入/跌出

4. **解析 GA4 CSV**：有机用户数、新用户、回访用户、有机占比

5. **写入结构化摘要**：
   ```
   1-2 Insight/Trident Insights/reports/YYYY-MM-DD/
   ├── keyword-digest.json        # Top 50 关键词 + 异动词 + P0/P1/P2 评分
   ├── page-performance.json      # Top 30 页面 + 变化
   └── geo-device-summary.json    # 地域 + 设备分布
   ```

### Phase 2: 拉取舆情报告

Sentinel 报告由你在另一个地方生成，保存到以下位置后自动触发 Pipeline：

```
1-2 Insight/Lovart ORM/
├── Lovart-Sentinel-YYYY-MM-DD-daily.md       ← 日报
└── raw/YYYY-MM-DD/
    ├── serp_bing.json
    ├── social_x.json
    ├── product_hunt.json
    └── ...
```

**文件夹监控逻辑**：Orchestrator 检测到该目录下新文件后自动触发 Pipeline Step 1。

### Phase 3: 本地信息补充与交叉分析

Agent 需读取以下本地文件，提取增量信号：

| 来源 | 路径 | 提取内容 |
|------|------|---------|
| 邮件复盘 | `Lovart/邮件复盘.md` | 送达率、退订率、打开率趋势 |
| 内容产出 | `1-3 Content Gen/Content Calendar/` | 14 品类待发/已发文章统计 |
| 翻译进度 | `1-4 Dev/lovart.sanity.studio/scripts/translation-progress.md` | 翻译完成度 |
| 竞品动态 | `1-2 Insight/Lovart ORM/raw/` | 竞品重大变化 |
| SEO 周报 | `1-2 Insight/Trident Insights/reports/SEO周报_*.md` | 品牌词/非品牌词趋势 |
| 关键词分类 | `lovart-keywords-intake` skill（旧版 v1.0 → 委托） | 8 类关键词分类 + P0/P1/P2 优先级 |

### Phase 4: 生成统一情报摘要

```
1-2 Insight/Trident Insights/reports/YYYY-MM-DD/
└── intelligence-brief.md          ← 下游 Step 2 的输入
```

**摘要结构**：

```markdown
# Intelligence Brief — YYYY-MM-DD

## 🔑 关键词洞察
- Top 5 上升关键词（附 clicks/position 变化）
- Top 5 下降关键词
- 3 个新发现的长尾关键词机会
- P0/P1/P2 优先级分类

## 📊 流量异动
- 流量异动页面列表（涨/跌 > 20%）
- 新进入 Top 30 的页面

## 📢 舆情信号
- 品牌声量变化（正/负/中性）
- 竞品重大动态
- 社区讨论热点

## 📧 邮件健康
- 送达率 / 打开率 / 退订率

## 📝 内容缺口
- Content Calendar 14 品类翻译完成度
- 竞品有但我们没有的内容话题

## 🎯 建议行动 (Top 5)
1. ...
2. ...
```

## Output

```
1-2 Insight/Trident Insights/reports/YYYY-MM-DD/
├── keyword-digest.json
├── page-performance.json
├── geo-device-summary.json
└── intelligence-brief.md
```

## Downstream

完成后自动触发 → `lovart-content-calendar` (Step 2)
