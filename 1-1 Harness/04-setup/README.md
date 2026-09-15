# Lovart GEO 自动化 — 新人自搭建指南

> 本文档面向接手此项目的任何人。按步骤执行，30 分钟内即可完成环境搭建，1 小时内产出第一份报告。
>
> 配套文档：[AGENTS.md](AGENTS.md) | [WORKFLOWS.md](WORKFLOWS.md) | [SKILLS_INVENTORY.md](SKILLS_INVENTORY.md) | [WORKFLOW_CHAIN.md](WORKFLOW_CHAIN.md) | [PRD-部署上线方案.md](PRD-部署上线方案.md)

---

## 前置条件

| 条件 | 说明 |
|------|------|
| macOS 14+ | launchd 定时任务需要 |
| Python 3.10+ | 所有脚本的运行环境 |
| Node.js 18+ | Sanity CLI |
| Git | 版本控制 |
| 网络 | 需访问 Google APIs、OpenAI API、Sanity API |
| Obsidian | 推荐（项目根是 Obsidian Vault） |

---

## Step 0：理解目录结构（5 分钟）

```
1-Project/
├── 1-1 GEO Readme/         ← 📖 从这里开始：AGENTS.md → WORKFLOWS.md → 本文档
├── 1-2 Insight/            ← 📊 报告产出：Trident(SEO) + Lovart ORM(Sentinel) + Keywords + Dataworks
├── 1-3 Content Gen/        ← ✍️  内容生成：Blog Pipeline + Content Calendar + Page Gen
├── 1-4 Dev/            ← 💻 代码区：scripts/ + sanity.studio/ + Sitemap/ + Output/
├── 1-1 Harness/            ← 🔧 工程控制：Skills/（规则文档见 1-1 Readme）
├── 1-6 Knowledge Base/     ← 📚 语料库：Lovart Docs + Lovart Introduction + Lovart News
├── 1-7 Output/             ← 📦 历史输出索引（新重输出默认外置）
└── 1-8 Backup/             ← 💾 历史备份索引（新重备份默认外置）
```

本机重输出目录：

```bash
bash "1-4 Dev/automation/bootstrap-local-dev.sh"
```

默认创建 `~/Documents/Lovart Local Dev/`，用于 `Output/`、`Backup/`、Sanity/WordPress 只读拉取缓存和 Git 外置维护区。详见 `1-1 GEO Readme/Lovart-Local-Dev-路径契约.md`。

脚本、Skills、workflow 仍留在 `1-Project` 内，不放到外部目录。外部目录只承接运行产物、只读缓存和本机临时文件。

---

## Step 1：安装依赖（10 分钟）

### 1.1 Python

```bash
pip3 install google-api-python-client google-auth-oauthlib zeep requests
```

### 1.2 Node.js（Sanity）

```bash
cd "1-4 Dev/lovart.sanity.studio"
npm install
```

### 1.3 验证

```bash
python3 -c "import googleapiclient; import requests; print('✅ Python OK')"
cd "1-4 Dev/lovart.sanity.studio" && npx sanity --version
```

---

## Step 2：获取凭证（从管理员）

需要从上一任管理员获取以下 **10 个凭证文件**（通过安全渠道传输，不要在 Git 中提交）：

| # | 凭证文件 | 放置位置 |
|---|----------|----------|
| 1 | `gsc-token.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` |
| 2 | `oauth-client.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` |
| 3 | `ga4-token.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` |
| 4 | `service-account.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` |
| 5 | `api_key` (Bing) | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` |
| 6 | `.env` (Sanity) | `1-4 Dev/lovart.sanity.studio/` |
| 7 | `wp-auth.local.env` | `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/scripts/` |
| 8 | `gsc-token.json` (Sentinel) | `1-4 Dev/scripts/sentinel/gsc_credentials/` |
| 9 | `ga4-token.json` (Sentinel) | `1-4 Dev/scripts/sentinel/ga4_credentials/` |
| 10 | `api_key` (Sentinel Bing) | `1-4 Dev/scripts/sentinel/bing_credentials/` |

说明：Trident 可执行脚本 SSOT 是 `1-4 Dev/scripts/trident/`。上表中的 `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` 是当前项目内共享凭证位置，脚本会自动读取；真实凭证允许本地保存，但不得提交到 Git。

**自行申请：**

| # | 凭证 | 申请方式 | 设置位置 |
|---|------|----------|----------|
| 11 | `OPENAI_API_KEY` | platform.openai.com → API Keys | `export OPENAI_API_KEY=sk-...` 写入 `~/.zshrc` |
| 12 | `ANTHROPIC_API_KEY` (可选) | console.anthropic.com | `export ANTHROPIC_API_KEY=...` 写入 `~/.zshrc` |

---

## Step 3：首次 OAuth 授权（10 分钟）

部分 API 需要首次交互式 OAuth 授权：

```bash
# GSC 首次授权（会弹出浏览器）
python3 "1-4 Dev/scripts/trident/gsc_auth.py"

# GA4 首次授权
python3 "1-4 Dev/scripts/trident/ga4_auth.py"

# Sanity 登录
cd "1-4 Dev/lovart.sanity.studio"
npx sanity login
```

---

## Step 4：验证 API 连通性（5 分钟）

```bash
cd "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project"

# GSC（应输出关键词数据）
python3 "1-4 Dev/scripts/trident/gsc_fetch.py"

# GA4（应输出 GA4 指标）
python3 "1-4 Dev/scripts/trident/ga4_fetch.py"

# Bing（应输出 Bing 关键词）
python3 "1-4 Dev/scripts/trident/bing_fetch.py"

# 竞品词匹配
python3 "1-4 Dev/scripts/competitor_deep_match.py"

# Sanity 认证
cd "1-4 Dev/lovart.sanity.studio" && node scripts/check-sanity-auth.js
```

---

## Step 5：拉线上参照（5 分钟）

```bash
cd "1-4 Dev/lovart.sanity.studio"

# Blog 分类结构
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token

# Features/Tools 预检
node scripts/convert-features.js --dry-run
node scripts/convert-tools.js --dry-run
```

---

## Step 6：生成第一份报告（5 分钟）

```bash
cd "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project"

# Sentinel 舆情日报
python3 "1-4 Dev/scripts/sentinel/collect.py" --source all
python3 "1-4 Dev/scripts/sentinel/report.py" --daily

# SEO 复盘周报（如已有一周数据）
python3 "1-4 Dev/scripts/weekly_review_v3.py"
```

---

## Step 7：配置定时任务（5 分钟）

将 [PRD-部署上线方案.md](PRD-部署上线方案.md) 中的 7 个 plist 文件复制到 `~/Library/LaunchAgents/`。

```bash
# 加载所有定时任务
launchctl load ~/Library/LaunchAgents/com.lovart.sentinel.daily.plist
launchctl load ~/Library/LaunchAgents/com.lovart.sentinel.report.daily.plist
launchctl load ~/Library/LaunchAgents/com.lovart.trident.weekly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.seo.weekly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.sentinel.report.weekly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.seo.monthly.plist
launchctl load ~/Library/LaunchAgents/com.lovart.content.audit.plist

# 验证
launchctl list | grep lovart
```

---

## Step 8：验证产出

执行完 Step 6 后，验证以下目录有内容：

- [ ] `1-2 Insight/Lovart ORM/daily/` 中有舆情日报
- [ ] `1-2 Insight/Lovart ORM/raw/YYYY-MM-DD/` 中有 raw JSON
- [ ] `1-2 Insight/Trident Insights/reports/weekly/` 中有 SEO 周报
- [ ] `~/Documents/Lovart Local Dev/Output/Data Ingestion/` 中有 JSON 数据
- [ ] `1-2 Insight/Trident Insights/reports/competitor_match_result.json` 中有竞品匹配结果
- [ ] `1-3 Content Gen/CONTENT_LINK_INDEX.md` 和 `content-link-index.csv` 可重新生成

---

## Step 9：阅读关键文档

| 顺序 | 文档 | 位置 | 时间 |
|:---:|------|------|------|
| 1 | AGENTS.md | `1-1 GEO Readme/` | 15 min |
| 2 | WORKFLOW_CHAIN.md | `1-1 GEO Readme/` | 10 min |
| 3 | SKILLS_INVENTORY.md | `1-1 GEO Readme/` | 10 min |
| 4 | WORKFLOWS.md | `1-1 GEO Readme/` | 15 min |
| 5 | lovart-trident-data-engine SKILL.md | `1-1 Harness/Skills/` | 10 min |
| 6 | PRD-部署上线方案.md | `1-1 GEO Readme/` | 10 min |

---

## 常见问题

### Q: GSC 401 认证失败？
重新运行 `python3 "1-4 Dev/scripts/trident/gsc_auth.py"` 刷新 token。

### Q: `ModuleNotFoundError: googleapiclient`？
运行 `pip3 install google-api-python-client`。

### Q: OpenAI API 429？
检查 API Key 余额和速率限制。考虑切换到 GPT-4o-mini。

### Q: plist 不执行？
```bash
# 检查 plist 语法
plutil -lint ~/Library/LaunchAgents/com.lovart.sentinel.daily.plist
# 查看日志
tail -f /tmp/lovart-sentinel-daily.err
# 手动触发测试
launchctl start com.lovart.sentinel.daily
```

### Q: 路径中有空格怎么办？
所有脚本已使用引号包裹路径。在终端中手动执行时，用双引号包裹完整路径。

---

## 交付检查清单

交接时确认以下全部完成：

- [ ] 10 个凭证文件已安全传输
- [ ] Step 1-3 依赖安装和 OAuth 授权完成
- [ ] Step 4 全部 API 连通性验证通过
- [ ] Step 6 成功产出第一份日报和周报
- [ ] Step 7 定时任务加载成功
- [ ] Step 8 产出目录验证通过
- [ ] Step 9 关键文档已阅读
- [ ] 了解飞书告警 Webhook URL（如有）
