# Lovart Pipeline 数据流地图

> SSOT — 所有数据输入/输出路径。交付给接手人时确保以下路径都存在。

## 数据流全景

```
┌─────────────────────────────────────────────────────────────┐
│                        数据输入层                             │
│                                                              │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────────┐ │
│  │ GSC API  │     │ Notion        │     │ 本地 CSV          │ │
│  │ (优先)    │     │ Lovart-Home   │     │ (兜底)            │ │
│  │          │     │ (次选)        │     │                   │ │
│  │ 待配置    │     │ ✅ 已配置      │     │ ✅ 可用            │ │
│  └────┬─────┘     └──────┬───────┘     └────────┬─────────┘ │
│       │                  │                      │            │
│       └──────────────────┼──────────────────────┘            │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │  lovart-data-ingestion│                       │
│              │  (Step 1)            │                       │
│              │  三级降级拉取         │                       │
│              └───────────┬───────────┘                       │
│                          │                                   │
│  ┌───────────────────────┼──────────────────────────────┐   │
│  │  Sentinel 舆情报告     │    SEO 周报                    │   │
│  │  (外部生成后落地)      │    (手动撰写)                  │   │
│  │                       │                               │   │
│  │  Lovart Knowledge     │    1-6 Knowledge Base/     │   │
│  │  Base/Lovart ORM/     │    Insight/Keywords Research/ │   │
│  │  Sentinel Reports/    │    SEO Report/                │   │
│  │  ┌─ daily.md          │    ┌─ SEO周报_*.md            │   │
│  │  └─ raw/              │    └─ 品牌词非品牌词_*.md     │   │
│  └───────────┬───────────┴──────────────┬───────────────┘   │
│              │                          │                    │
│              └──────────┬───────────────┘                    │
│                         ▼                                    │
│              ┌──────────────────────┐                        │
│              │ intelligence-brief   │                        │
│              │ 1-2 Insight/Trident Insights/reports│                        │
│              │ /YYYY-MM-DD/         │                        │
│              └──────────┬───────────┘                        │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Step 2: calendar    │
              │  Step 3: 内容创作     │
              │  Step 3.5: 图片生成   │
              │  Step 4: 质量门禁     │
              │  Step 5: 分发推送     │
              │  Step 7: Sitemap      │
              └───────────────────────┘
```

---

## 输入路径（数据来源）

### GSC 关键词数据

| 层级 | 来源 | 路径 / ID | 状态 |
|------|------|----------|------|
| **数据输入** | | | |
| 1️⃣ GSC API | OAuth 2.0 `gsc-token.json` | ✅ `gsc_credentials/gsc_fetch.py` (关键词+收录+国家) |
| 2️⃣ GA4 API | OAuth 2.0 `ga4-token.json` | ✅ `ga4_credentials/ga4_fetch.py` (流量+用户+国家) |
| 3️⃣ Bing API | API Key `api_key` | ✅ `bing_credentials/` SOAP (关键词+页面+爬虫) |
| 3️⃣ Notion Lovart-Home | Token `ntn_...` | ✅ `lovart-notion-config.md` |
| 4️⃣ | 本地 CSV | 磁盘文件 | ✅ `Daily Raw Data/` + `Weekly Raw Data/` |
| 2️⃣ | Notion Lovart-Home | DB: `36ffc0c7-1bd5-80b3-b8f1-e1ec200104cc` | ✅ Token 已配置 (`lovart-notion-config.md`) |
| 3️⃣ | 本地 CSV | `1-6 Knowledge Base/Insight/Keywords Research/Daily Raw Data/` | ✅ 可用 |

**本地 CSV 目录结构**：
```
1-6 Knowledge Base/Insight/Keywords Research/
├── Daily Raw Data/                              ← GSC 日度
├── Weekly Raw Data/
│   ├── 谷歌 SEO 数据/                           ← GSC 周度
│   ├── Bing SEO 数据/                           ← Bing 周度
│   └── 用户获取情况/                             ← GA4
├── SEO Report/                                  ← SEO 周报 Markdown
│   ├── SEO周报_YYYYMMDD-YYYYMMDD.md
│   └── 品牌词非品牌词_*.md
└── diagrams/                                    ← 图表 SVG/PNG
```

### Sentinel 舆情报告

| 来源 | 路径 | 触发 |
|------|------|------|
| 外部生成 | `1-6 Knowledge Base/Sentinel Insights/reports/` | 落地后自动触发 Pipeline |
| 日报 | `Lovart-Sentinel-YYYY-MM-DD-daily.md` | 每日 |
| 周报 | `Lovart-Sentinel-YYYY-MM-DD-weekly.md` | 每周 |
| 原始数据 | `raw/YYYY-MM-DD/` (.json) | 随日报生成 |

**Sentinel 配置**: `1-4 Dev/scripts/sentinel/config.yaml`
- `base_path`: `1-Project/Lovart` (通过 `__file__` 相对解析，换电脑自动适配)
- `report_output`: `../1-6 Knowledge Base/Sentinel Insights/reports`
- `internal_sources.gsc_daily`: `../1-6 Knowledge Base/Insight/Keywords Research/Daily Raw Data/`

### 内容日历

| 路径 | 说明 |
|------|------|
| `1-6 Knowledge Base/Content Calendar/` | 14 品类, 3,221 篇 Markdown |
| `1-6 Knowledge Base/Content Archive/Lovart Fake/` | 新文章 |
| `1-6 Knowledge Base/Content Archive/Original/` | 已发布 |
| `1-6 Knowledge Base/Content Archive/pages-legacy/Features/` | Features JSON（1,914 条目, 9 语言） |
| `1-3 Content Gen/Page Gen/Pages/Tools/` | Tools JSON（composite-v2 正式源，与 production 对齐） |
| ~~`pages-legacy/Tools/`~~ | **已弃用**（历史 heroSection 归档） |

### 邮件数据

| 路径 | 说明 |
|------|------|
| `1-4 Dev/邮件复盘.md` | 送达率、退订率、打开率趋势（手动更新） |

---

## 输出路径（Pipeline 产出）

```
1-4 Dev/Output/
├── Data Ingestion/YYYY-MM-DD/          ← Step 1: intelligence-brief
├── Content Calendar/                   ← Step 2: 三大日历 + creation-tasks
├── Images/YYYY-MM-DD/                  ← Step 3.5: 封面 + 配图
├── Distribution/YYYY-WW/               ← Step 3: 分发草稿
├── Audit Reports/YYYY-MM-DD/           ← Step 4: 审计报告
├── Push Reports/                        ← Step 5+6: 推送结果
└── Pipeline Reports/                    ← 主编排器: 总报告
```

### Sitemap 产出

| 路径 | 说明 |
|------|------|
| `1-4 Dev/Sitemap/` | 32 个 SEO 文件（sitemap-*.xml, llms*.txt, robots.txt） |
| 部署目标 | `https://www.lovart.ai/sitemap-index.xml` |

### 分发产出（content-distributor 引擎）

| 路径 | 说明 |
|------|------|
| `Output/Push Reports/` | 飞书写入状态报告 |
| `Output/Push Reports/manual-platforms-YYYY-MM-DD.md` | 手动平台操作清单 |
| 飞书 Bitable | Base: `ZLWgbi6VIaCRiNsb22jcNpPRnfh`, Table: `tblfYkNiq83rotAh` |
| content-distributor 引擎 | `~/content-distributor/`（独立于 vault 安装） |

---

## 关键配置文件

| 文件 | 路径 | 说明 |
|------|------|------|
| sentinel config | `1-4 Dev/scripts/sentinel/config.yaml` | 品牌监控、数据源路径、告警阈值 |
| Notion 配置 | `Skills/lovart-notion-config.md` | Token + Database ID |
| Lovart API 配置 | `Skills/lovart-api-config.md` | Access Key + Secret Key（图片生成） |
| GSC API 引导 | `Skills/lovart-gsc-api-setup-guide.md` | OAuth 配置流程 |
| GA4 凭证 | `1-4 Dev/scripts/sentinel/ga4_credentials/` | service-account.json + ga4-token.json |
| SEO 配置 | `Skills/config.example.json` | Lovart 站点配置 |
| Sanity .env | `1-4 Dev/lovart.sanity.studio/.env` | PROJECT_ID + API Token |
| WP 发布脚本 | `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/scripts/publish-to-wp.py`（TODO/GAP: 重构中删除待恢复） | WordPress API 凭证 |

---

## 交付 checklist（接手人验证）

```bash
# 1. 确认用户名匹配 config.yaml 中的 base_path
whoami → 应为 "seveno"（否则改 config.yaml）

# 2. 确认数据输入路径存在
ls "1-6 Knowledge Base/Insight/Keywords Research/Daily Raw Data/"
ls "1-6 Knowledge Base/Sentinel Insights/reports/"

# 3. 确认 Notion token 生效
curl -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
     "https://api.notion.com/v1/databases/36ffc0c7-1bd5-80b3-b8f1-e1ec200104cc" \
     -H "Notion-Version: 2022-06-28"

# 4. 确认 sentinel 脚本路径正确
python3 "1-4 Dev/scripts/sentinel/daily.py" --dry-run

# 5. 确认 Output 目录存在
ls -d "1-4 Dev/Output/"*/
```
