# Lovart Notion Integration Config

## Access Token

```
ntn_<REDACTED-see-secrets/README>
```

```bash
export NOTION_API_KEY="ntn_<REDACTED-see-secrets/README>"
mkdir -p ~/.config/notion && echo "ntn_<REDACTED-see-secrets/README>" > ~/.config/notion/api_key && chmod 600 ~/.config/notion/api_key
```

## 数据库

### 1. Lovart-Home（父页面）

| 属性 | 值 |
|------|-----|
| Page ID | `36ffc0c7-1bd5-80b3-b8f1-e1ec200104cc` |
| 用途 | 顶级容器页面 |

### 2. Daily Keyword Tracker（每日关键词追踪）

| 属性 | 值 |
|------|-----|
| Database ID | `371fc0c7-1bd5-811c-af7f-fd50d065e869` |
| 用途 | GSC 关键词手动录入，Pipeline 二级降级数据源 |

### 3. Skill Index（技能索引）⭐ 新增

| 属性 | 值 |
|------|-----|
| Database ID | `372fc0c7-1bd5-81a7-a854-f7509cfee73a` |
| 用途 | 22 个 Lovart Skill 的版本/路径/状态索引 |
| 字段 | Name / Step / Version / Path / Status |
| 数据行 | 22 skills (18 Active + 4 Guide) |

⚠️ 使用前需在 Notion 中分享数据库给集成: 打开 Skill Index → "..." → Connections → 添加你的集成。

### 4. Content Calendar（内容日历）⭐ 新增 2026-06-09

| 属性 | 值 |
|------|-----|
| Database ID | `37afc0c7-1bd5-8124-a031-ca4eca128da2` |
| 父页面 | LifeOS PARA Command Center (`378fc0c7-1bd5-8179-8f67-dc2f306257d7`) |
| 用途 | Blog / Page / Landing / Distribution 全内容排期与状态追踪 |
| 字段数 | 20（Name, Slug, Status, Priority, Score, Bucket, Language, Canonical Slug, Cluster Type, Cluster Size, Target Keywords, URL, Publish Date, Author, Content Path, Notes, Content Type, Pipeline Stage）|
| 数据源 | 本地 MD frontmatter + `build-content-calendar-priority.js` 计算 |
| 同步方向 | 单向：本地 MD (SSOT) → Notion |
| 脚本 | `1-3 Content Gen/Content Calendar/scripts/sync-to-notion.py` |

#### Content Calendar Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| **Name** | Title | 文章标题 |
| **Slug** | Rich Text | URL slug |
| **Status** | Select | Backlog / Draft / In Progress / Ready / Scheduled / Published / Internal / Archived |
| **Priority** | Select | P0-Next Draft / P1-Good Candidate / P2-Backlog / P3-Published / P2-Risk Review |
| **Score** | Number | 0-120 优先级评分 |
| **Bucket** | Select | 14 个内容桶（01-How-To ~ 14-Product-Update） |
| **Language** | Select | en / zh / ja / pt / ru / zh-TW |
| **Canonical Slug** | Rich Text | 去重后归一化 slug |
| **Cluster Type** | Select | single / multilingual-cluster / same-language-duplicate |
| **Cluster Size** | Number | 簇内文件数 |
| **Target Keywords** | Rich Text | 目标关键词 |
| **URL** | URL | 发布后线上 URL |
| **Publish Date** | Date | 发布日期 |
| **Author** | Select | AI Agent / Human |
| **Content Path** | Rich Text | 本地 MD 文件相对路径 |
| **Notes** | Rich Text | 备注 |
| **Content Type** | Select | Blog / Page / Landing / Distribution / Other |
| **Pipeline Stage** | Select | S1-Data ~ S6-Monitor |

⚠️ 使用前需在 Notion 中分享数据库给集成: 打开 Content Calendar → "..." → Connections → 添加你的集成。

## Daily Keyword Tracker Schema

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| **Query** | Title | 搜索关键词 | `lovart ai` |
| **Date** | Date | 数据日期 | 2026-05-31 |
| **Clicks** | Number | 点击次数 | 128765 |
| **Impressions** | Number | 展示次数 | 243122 |
| **CTR** | Number (Percent) | 点击率 | 0.53 (53%) |
| **Position** | Number | 平均排名 | 1.1 |
| **Page** | URL | 着陆页链接 | `https://www.lovart.ai/` |
| **Country** | Select | 国家 | US / CN / JP / KR / DE / FR / PT / RU / IT / Other |
| **Device** | Select | 设备 | Desktop / Mobile / Tablet |
| **Category** | Select | 关键词分类 | Brand / Product / Competitor / How-To / Comparison / Industry / Other |
| **Notes** | Text | 备注（可选） | 观察、趋势变化等 |

## 每日操作

打开 Notion → Lovart-Home → Daily Keyword Tracker → 新增行 → 填入当天 GSC 数据：

1. 从 GSC 导出昨日 Top 50 关键词 CSV
2. 逐行复制 Query / Clicks / Impressions / CTR / Position
3. 选择 Country、Device、Category
4. Date 填当天

或者——GSC API 已配置 ✅，Pipeline 会自动拉取，Notion 只在 GSC API 不可用时才作为二级降级数据源。

## Pipeline 查询

```bash
# 查询最近 7 天数据
curl -s -X POST "https://api.notion.com/v1/databases/371fc0c7-1bd5-811c-af7f-fd50d065e869/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"sorts":[{"property":"Date","direction":"descending"}],"filter":{"property":"Date","date":{"past_week":{}}}}'
```
