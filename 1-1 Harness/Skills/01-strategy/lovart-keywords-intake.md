# Lovart Keywords Intake Skill

## Description

Daily SEO data ingestion skill. Scans `Keywords Research/Daily Raw/` for GSC and Bing Webmaster CSV exports, parses and scores keywords, cross-references against Sanity published content, and auto-updates the content calendar. Outputs a prioritized production briefing.

**Use Cases**: "关键词分析" / "keywords intake" / "每日数据" / "analyze keywords" / "daily SEO"

---

## Skill Configuration

**Name**: Lovart Keywords Intake
**Version**: 1.0.0
**Dependencies**: `lovart-academy-content-calendar-v1.md`, Sanity MCP (project `o11tm2qe`)
**Input Path**: `1-Project/Insight/Keywords Research/Daily Raw Data/`
**Output**: Prioritized keyword list + auto-updated `lovart-academy-content-calendar-v1.md`

---

## Step 1: Scan Daily Raw Directory

```bash
ls -lt "Keywords Research/Daily Raw/" 2>/dev/null
```

### Supported Formats

| Format | Detection | Priority |
|---|---|---|
| GSC folder (含 查询数.csv) | Directory with `查询数.csv` | Parse queries |
| GSC single CSV | `*GSC*.csv` or `*SearchPerformance*.csv` | Parse queries |
| Bing CSV | `*Bing*.csv` or `*bing*.csv` | Parse queries |
| Overview CSV | `*Overview*.csv` or `*PerformanceOverview*.csv` | Trend only |

### Empty Directory Fallback

If `Daily Raw/` is empty → output:

```
📊 今日无新 SEO 数据。请导入 GSC/Bing 导出文件到 Keywords Research/Daily Raw/
   输入 "retry" 重新扫描。
```

---

## Step 2: Parse & Normalize

### GSC Data (查询数.csv)

Columns detected: `热门查询, 点击次数, 展示, 点击率, 排名`

Parse with Python, normalize to:
```
query, clicks, impressions, ctr, position, source
```

### Bing Data (if present)

Same normalization, source = `bing`.

### Merge & Deduplicate

Merge GSC + Bing by query. Keep higher-impression entry. Add source flag: `gsc` / `bing` / `both`.

---

## Step 3: Brand Filter & Classification

> **🚨 SSOT 铁律**：品牌词分类的唯一代码来源是 `1-4 Dev/scripts/lovart_brand_match.py`。禁止硬编码品牌词列表。

```python
from lovart_brand_match import is_brand, partition_keywords
```

Any query with `is_brand(q) == True` → flag as `brand`, exclude from non-brand analysis (but track for brand health monitoring).

### Non-Brand Classification

For each non-brand keyword, classify:

| Pattern | Content Type | Example |
|---|---|---|
| `[tool] vs` or `[tool] alternative` | Comparison | "pixai vs lovart" |
| `how to [action]` or `[action] with ai` | Tutorial | "how to create product photos with ai" |
| `best ai [category]` or `[category] ai tool` | Comparison / Pillar | "best ai design tools" |
| `[tool name]` (competitor) | Comparison | "pixai", "luma dream machine" |
| `free [tool type]` or `[tool type] free` | Comparison / Tutorial | "free ai logo generator" |
| `[industry] design [tool/ai]` | Segment Deep-Dive | "real estate design ai" |
| Design principle / theory | Better Design | "color theory design" |
| Fallback | Tutorial (How-To) | — |

---

## Step 4: Priority Scoring

```
For each non-brand keyword:
  score = 0
  
  // Position signal
  if 6 <= position <= 20:
    score += 30  // Can be pushed to top 5 with content
  if position > 20:
    score += 10  // Long-term opportunity
  
  // Impression signal
  if impressions > 1000: score += 25
  elif impressions > 500: score += 15
  elif impressions > 100: score += 5
  
  // CTR signal (low CTR = opportunity)
  if position <= 5 and ctr < 3: score += 10  // Meta optimization
  if position <= 5 and ctr < 1: score += 10  // Urgent meta fix
  
  // Novelty signal (not in calendar)
  if not_in_calendar: score += 10
  
  Final priority:
    score >= 40 → P0 (today)
    score >= 20 → P1 (this week)
    score < 20  → P2 (this month)
```

---

## Step 5: Sanity Cross-Reference

Query Sanity MCP to check which keywords already have matching content:

```
*[_type == "blog" && title match $kw || seoDescription match $kw] {
  title, "slug": slug.current, language
}
[0...5]
```

Tag each keyword: `has_content: yes | no | partial`

---

## Step 6: Calendar Auto-Update

For P0 keywords not in the calendar:

1. Map to content type using the classification rules (Step 3)
2. Generate a suggested title
3. Insert into `lovart-academy-content-calendar-v1.md` in the appropriate section
4. Tag with source: `[GSC Daily YYYY-MM-DD]` or `[Bing Daily YYYY-MM-DD]`
5. Update the `生成日期` timestamp at the top of the calendar file

---

## Step 7: Output — Daily Briefing

```
📊 SEO 数据简报 (YYYY-MM-DD)

   ── 数据源 ──
   GSC: [filename] — [N] keywords
   Bing: [filename | 无数据]
   非品牌词: [N] / 品牌词: [N]

   ── 趋势 ──
   本周展示: [trend], 本周点击: [trend], 本周CTR: [trend]

   ── 优先级 ──
   🔴 P0 (今天): [N] keywords
      [top 5 with impressions, position, suggested content type]
   🟡 P1 (本周): [N] keywords
      [top 3]
   🟢 P2 (本月): [N] keywords

   ── 日历更新 ──
   新纳入日历: [N] items (P0 × N, P1 × N)

   输入 "produce P0" 开始生产。
   输入 "review" 查看完整列表。
```

---

## Shortcut Reference

| Command | Action |
|---|---|
| `关键词分析` / `keywords intake` | Full pipeline: scan → parse → score → update calendar → briefing |
| `retry` | Re-scan Daily Raw directory |
| `review` | Show full keyword list with scores |
| `仅GSC` | Parse GSC data only, ignore Bing |
