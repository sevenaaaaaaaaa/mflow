# PRD：Lovart GEO 本地部署与定时调度方案

> v1.0 | 2026-06-04 | Lovart Growth Team
>
> 面向 macOS 本地部署的全自动定时调度方案。所有脚本通过 launchd plist 管理，无需 Docker/n8n（本地开发阶段）。

---

## 一、部署架构

```
┌─────────────────────────────────────────────────────────┐
│                    macOS (本机)                           │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ launchd  │  │ launchd  │  │ launchd  │  ...        │
│  │ plist A  │  │ plist B  │  │ plist C  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │             │                    │
│       ▼             ▼             ▼                    │
│  ┌──────────────────────────────────────────────┐      │
│  │           Python 脚本 + LLM API               │      │
│  │  (GSC/GA4/Bing 采集 → 报告生成 → 内容生成)    │      │
│  └──────────────────────┬───────────────────────┘      │
│                         │                               │
│                         ▼                               │
│  ┌──────────────────────────────────────────────┐      │
│  │  产出目录 (本地 Obsidian Vault)                │      │
│  │  1-2 Insight/  |  1-3 Content Gen/           │      │
│  │  1-4 Dev/  |  1-7 Output/                │      │
│  └──────────────────────────────────────────────┘      │
│                         │                               │
│                         ▼ (Agent 触发)                  │
│  ┌──────────────────────────────────────────────┐      │
│  │  Sanity 发布 (npx sanity dataset import)      │      │
│  │  WordPress 发布 (publish-to-wp.py)            │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

---

## 二、环境要求

| 组件 | 版本要求 | 用途 |
|------|----------|------|
| macOS | 14+ (Sonoma+) | 操作系统 |
| Python | 3.10+ | 所有数据采集和报告脚本 |
| Node.js | 18+ | Sanity CLI |
| pip 包 | google-api-python-client, google-auth-oauthlib, zeep, requests | GSC/GA4/Bing API |
| npm 包 | @sanity/cli, sanity | Sanity 内容管理 |

---

## 三、凭证清单

| 凭证文件 | 位置 | 用途 |
|----------|------|------|
| `gsc-token.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GSC OAuth token |
| `oauth-client.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GSC OAuth client |
| `ga4-token.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GA4 OAuth token |
| `service-account.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GA4 服务账号 |
| `api_key` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | Bing Webmaster API key |
| `.env` | `1-4 Dev/lovart.sanity.studio/` | Sanity 项目凭证 |
| `OPENAI_API_KEY` | 环境变量 `~/.zshrc` | LLM API |
| `ANTHROPIC_API_KEY` | 环境变量 `~/.zshrc` | LLM 备用 |
| `wp-auth.local.env` | `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/scripts/` | WordPress 凭证 |
| `feishu.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | 飞书应用凭证 |

> ⚠️ 所有凭证已在 `.gitignore` 排除。交接时通过安全渠道传输。

---

## 四、定时调度总表

所有任务按执行频次分类，由 macOS launchd 管理。

### 4.1 每日任务

| 时间 | 任务 | 脚本 | 产出 | 预计耗时 |
|------|------|------|------|----------|
| 00:05 | GSC 日报数据拉取 | `scripts/trident/gsc_fetch.py --daily` | `1-4 Dev/Output/Data Ingestion/gsc-daily.json` | 2 min |
| 00:10 | Sentinel 数据采集 | `1-4 Dev/scripts/sentinel/collect.py --source all` | `1-2 Insight/Lovart ORM/raw/YYYY-MM-DD/` | 5 min |
| 00:30 | Sentinel 日报生成 | `1-4 Dev/scripts/sentinel/report.py --daily` | `1-2 Insight/Lovart ORM/daily/` | 3 min |
| 08:00 | 缺口队列补充（3篇） | `lovart-pipeline-orchestrator` → Blog 生成 | `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/01-Drafts/` | 15 min |
| 10:00 | 多语言翻译队列 | `lovart-pipeline-orchestrator` → LLM 翻译 | `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/01-Drafts/` | 10 min |
| 18:00 | SEO 日报生成 | `1-4 Dev/scripts/sentinel/sources/gsc_daily.py` | `1-2 Insight/Lovart ORM/daily/` | 1 min |
| 20:00 | 每日汇总通知（飞书） | `scripts/trident/push_to_feishu.py --daily-summary` | 飞书消息 | 1 min |

### 4.2 每周任务

| 时间 | 任务 | 脚本 | 产出 | 预计耗时 |
|------|------|------|------|----------|
| 周一 06:00 | GA4 全量数据拉取 | `scripts/trident/ga4_fetch.py` | `1-4 Dev/Output/Data Ingestion/ga4-YYYY-MM.json` | 5 min |
| 周一 07:00 | GSC 全量数据拉取 | `scripts/trident/gsc_fetch.py` | `1-4 Dev/Output/Data Ingestion/gsc-5k-YYYY-MM.json` | 5 min |
| 周一 08:00 | Bing 数据拉取 | `scripts/trident/bing_fetch.py` | `1-2 Insight/Trident Insights/reports/bing-full.json` | 2 min |
| 周一 09:00 | SEO 复盘周报生成 | `1-4 Dev/scripts/weekly_review_v3.py` | `1-2 Insight/Trident Insights/reports/weekly/` | 10 min |
| 周一 09:00 | Semrush 排名拉取 | Playwright 脚本 | Google Sheets 日志表 | 5 min |
| 周一 10:00 | Sentinel 周报生成 | `1-4 Dev/scripts/sentinel/report.py --weekly` | `1-2 Insight/Lovart ORM/weekly/` | 5 min |
| 周一 11:00 | AI 搜索引用监测 | Playwright 脚本（check Perplexity/ChatGPT） | `1-2 Insight/Page Analytic/geo-monitor.json` | 10 min |
| 周三 09:00 | 自然周报生成 | `1-4 Dev/scripts/weekly_review_v3.py --natural` | `1-2 Insight/Trident Insights/reports/weekly/` | 10 min |

### 4.3 每月任务

| 时间 | 任务 | 脚本 | 产出 | 预计耗时 |
|------|------|------|------|----------|
| 每月 2 日 06:00 | DataWorks 数据检查 | 检查 `1-2 Insight/From Datawork/{YYYY-MM} SEO GEO.xlsx` 是否就位 | — | 1 min |
| 每月 3 日 06:00 | SEO 月报 V2 生成 | `1-4 Dev/scripts/seo_monthly_v2.py --month YYYY-MM` | `1-2 Insight/Trident Insights/reports/monthly/` | 20 min |
| 每月 3 日 12:00 | Sentinel 月报生成 | `1-4 Dev/scripts/sentinel/report.py --monthly` | `1-2 Insight/Lovart ORM/monthly/` | 5 min |
| 每月 5 日 09:00 | 内容老化检测 | `lovart-content-audit` → 扫描 6 个月以上文章 | Google Sheets | 5 min |
| 每月 5 日 10:00 | Sitemap 全量更新 | `lovart-sitemap-update` | `1-4 Dev/Sitemap/` | 3 min |

### 4.4 每季/每年任务

| 时间 | 任务 | 脚本 | 产出 | 预计耗时 |
|------|------|------|------|----------|
| 季末月 5 日 | SEO 季报生成 | `seo_monthly_v2.py`（季报模式） | `1-2 Insight/Trident Insights/reports/quarterly/` | 15 min |
| 季末月 5 日 | Sentinel 季报生成 | `1-4 Dev/scripts/sentinel/report.py --quarterly` | `1-2 Insight/Lovart ORM/` | 5 min |
| 每年 1 月 10 日 | SEO 年报生成 | `seo_monthly_v2.py`（年报模式） | `1-2 Insight/Trident Insights/reports/annual/` | 20 min |
| 每年 12 月 28 日 | 年度内容批量更新（年份替换） | LLM 批量任务 | 全部文章 | 1 hr |

---

## 五、macOS launchd Plist 完整配置

所有 plist 放置在 `~/Library/LaunchAgents/`。

### 5.1 每日 Sentinel 采集（00:10）

**文件:** `~/Library/LaunchAgents/com.lovart.sentinel.daily.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lovart.sentinel.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/scripts/sentinel/collect.py</string>
        <string>--source</string>
        <string>all</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>0</integer>
        <key>Minute</key><integer>10</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project</string>
    <key>StandardOutPath</key>
    <string>/tmp/lovart-sentinel-daily.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/lovart-sentinel-daily.err</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
```

### 5.2 每日 Sentinel 日报生成（00:30）

**文件:** `~/Library/LaunchAgents/com.lovart.sentinel.report.daily.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lovart.sentinel.report.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/scripts/sentinel/report.py</string>
        <string>--daily</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>0</integer>
        <key>Minute</key><integer>30</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project</string>
    <key>StandardOutPath</key>
    <string>/tmp/lovart-sentinel-report-daily.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/lovart-sentinel-report-daily.err</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
```

### 5.3 每周一 GSC + GA4 + Bing 全量采集（周一 06:00-08:00）

**文件:** `~/Library/LaunchAgents/com.lovart.trident.weekly.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lovart.trident.weekly</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-1 Harness/Skills/lovart-trident-data-engine/scripts/run_all.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>6</integer>
        <key>Minute</key><integer>0</integer>
        <key>Weekday</key><integer>1</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project</string>
    <key>StandardOutPath</key>
    <string>/tmp/lovart-trident-weekly.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/lovart-trident-weekly.err</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
```

### 5.4 每周一 SEO 复盘周报（周一 09:00）

**文件:** `~/Library/LaunchAgents/com.lovart.seo.weekly.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lovart.seo.weekly</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/scripts/weekly_review_v3.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>9</integer>
        <key>Minute</key><integer>0</integer>
        <key>Weekday</key><integer>1</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project</string>
    <key>StandardOutPath</key>
    <string>/tmp/lovart-seo-weekly.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/lovart-seo-weekly.err</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
```

### 5.5 每周一 Sentinel 周报（周一 10:00）

**文件:** `~/Library/LaunchAgents/com.lovart.sentinel.report.weekly.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lovart.sentinel.report.weekly</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/scripts/sentinel/report.py</string>
        <string>--weekly</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>10</integer>
        <key>Minute</key><integer>0</integer>
        <key>Weekday</key><integer>1</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project</string>
    <key>StandardOutPath</key>
    <string>/tmp/lovart-sentinel-weekly.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/lovart-sentinel-weekly.err</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
```

### 5.6 每月 SEO 月报 V2（每月 3 日 06:00）

**文件:** `~/Library/LaunchAgents/com.lovart.seo.monthly.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lovart.seo.monthly</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>MONTH=$(date -v-1m +%Y-%m); /usr/bin/python3 "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/scripts/seo_monthly_v2.py" --month $MONTH</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>6</integer>
        <key>Minute</key><integer>0</integer>
        <key>Day</key><integer>3</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project</string>
    <key>StandardOutPath</key>
    <string>/tmp/lovart-seo-monthly.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/lovart-seo-monthly.err</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
```

### 5.7 每月内容老化检测（每月 5 日 09:00）

**文件:** `~/Library/LaunchAgents/com.lovart.content.audit.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lovart.content.audit</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/scripts/sentinel/sources/content_production.py</string>
        <string>--audit</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>9</integer>
        <key>Minute</key><integer>0</integer>
        <key>Day</key><integer>5</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project</string>
    <key>StandardOutPath</key>
    <string>/tmp/lovart-content-audit.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/lovart-content-audit.err</string>
    <key>RunAtLoad</key><false/>
</dict>
</plist>
```

---

## 六、plist 快捷管理命令

```bash
# 加载所有 plist
launchctl load ~/Library/LaunchAgents/com.lovart.sentinel.daily.plist
launchctl load ~/Library/LaunchAgents/com.lovart.sentinel.report.daily.plist
launchctl load ~/Library/LaunchAgents/com.lovart.trident.weekly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.seo.weekly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.sentinel.report.weekly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.seo.monthly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.content.audit.plist

# 卸载
launchctl unload ~/Library/LaunchAgents/com.lovart.sentinel.daily.plist

# 列出所有 Lovart 任务
launchctl list | grep lovart

# 立即手动触发（测试用）
launchctl start com.lovart.sentinel.daily

# 查看日志
tail -f /tmp/lovart-sentinel-daily.out
tail -f /tmp/lovart-sentinel-daily.err
```

---

## 七、健康检查脚本

**文件:** `1-1 Harness/Skills/check-deps.sh`

```bash
#!/bin/bash
# 每日 00:01 执行 — 检查所有依赖和凭证

echo "=== Lovart Health Check $(date) ==="

# Python 依赖
python3 -c "import googleapiclient; import requests; import zeep" 2>/dev/null
if [ $? -eq 0 ]; then echo "✅ Python deps OK"; else echo "❌ Python deps MISSING"; fi

# 凭证文件
check_cred() {
    if [ -f "$1" ]; then echo "✅ $2 OK"; else echo "⚠️  $2 MISSING: $1"; fi
}

CRED_DIR="1-1 Harness/Skills/lovart-trident-data-engine/credentials"
check_cred "$CRED_DIR/gsc-token.json" "GSC token"
check_cred "$CRED_DIR/ga4-token.json" "GA4 token"
check_cred "$CRED_DIR/service-account.json" "GA4 service account"
check_cred "$CRED_DIR/api_key" "Bing API key"

# Sanity
if [ -f "1-4 Dev/lovart.sanity.studio/.env" ]; then
    echo "✅ Sanity .env OK"
else
    echo "❌ Sanity .env MISSING"
fi

# OpenAI
if [ -n "$OPENAI_API_KEY" ]; then echo "✅ OpenAI API key OK"; else echo "❌ OPENAI_API_KEY not set"; fi

# 目录结构
check_dir() {
    if [ -d "$1" ]; then echo "✅ $2 OK"; else echo "⚠️  $2 MISSING: $1"; fi
}
check_dir "1-2 Insight/" "Insight"
check_dir "1-3 Content Gen/" "Content Gen"
check_dir "1-4 Dev/" "Geo Dev"
check_dir "1-1 Harness/" "Harness"
check_dir "1-6 Knowledge Base/" "Knowledge Base"
check_dir "1-7 Output/" "Output"

echo "=== Health Check Done ==="
```

---

## 八、成本预估（本地部署）

| 项目 | 月成本 | 说明 |
|------|--------|------|
| OpenAI API (GPT-4o) | ¥600-1500 | 每日 5-10 篇 × 2000 字 × 8000 tokens |
| OpenAI API (GPT-4o-mini) | ¥100-300 | 舆情分析 + FAQ + 翻译 |
| Anthropic API (备用) | ¥0-200 | 仅 GPT-4o 不可用时切换 |
| 总计 | **¥700-2000** | 无需服务器费用（本地运行） |

> 对比：加 1 名内容写手年成本 ¥15-30 万。系统月投入仅为加 1 人的 5-10%。

---

## 九、故障处理

| 故障 | 表现 | 排查 |
|------|------|------|
| plist 未执行 | `launchctl list | grep lovart` 无输出 | 检查 plist 文件语法：`plutil -lint file.plist` |
| GSC 认证过期 | 脚本报 401 | 重新运行 `gsc_auth.py` |
| API 限流 | 脚本报 429 | 等待 60 秒后重试，或降低并发的采集量 |
| Sentienl 无数据 | raw/ 目录为空 | 检查网络和 API key，查看 stderr 日志 |
| 磁盘空间不足 | 系统提示 | 清理 `1-7 Output/` 和旧 raw 数据 |

---

## 十、附录

### A. plist 文件索引

| plist 文件 | 任务 | 频次 |
|-----------|------|------|
| `com.lovart.sentinel.daily.plist` | Sentinel 数据采集 | 每日 00:10 |
| `com.lovart.sentinel.report.daily.plist` | Sentinel 日报生成 | 每日 00:30 |
| `com.lovart.trident.weekly.plist` | GSC+GA4+Bing 全量采集 | 每周一 06:00 |
| `com.lovart.seo.weekly.plist` | SEO 复盘周报 | 每周一 09:00 |
| `com.lovart.sentinel.report.weekly.plist` | Sentinel 周报 | 每周一 10:00 |
| `com.lovart.seo.monthly.plist` | SEO 月报 V2 | 每月 3 日 06:00 |
| `com.lovart.content.audit.plist` | 内容老化检测 | 每月 5 日 09:00 |

### B. 时间线示意图

```
每日时间轴:
00:00 ─── 健康检查
00:10 ─── Sentinel 采集开始
00:30 ─── Sentinel 日报生成
08:00 ─── 缺口队列补充
10:00 ─── 多语言翻译
18:00 ─── SEO 日报
20:00 ─── 飞书汇总

每周一时间轴:
06:00 ─── GSC/GA4/Bing 全量采集
09:00 ─── SEO 复盘周报
10:00 ─── Sentinel 周报
11:00 ─── AI 搜索引用监测

每月 3 日:
06:00 ─── SEO 月报 V2
12:00 ─── Sentinel 月报

每月 5 日:
09:00 ─── 内容老化检测
10:00 ─── Sitemap 更新
```
