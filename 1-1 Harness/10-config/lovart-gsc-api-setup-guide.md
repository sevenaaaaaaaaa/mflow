# GSC API 配置引导 — Lovart Pipeline 数据源

> ✅ 已完成配置 (2026-05-31)。以下为记录文档。

## 配置状态

| 步骤 | 状态 |
|------|------|
| Search Console API 启用 | ✅ |
| OAuth 2.0 桌面应用凭证 | ✅ |
| Refresh Token 已获取 | ✅ |
| 验证连接成功 | ✅ |

## 凭证位置

| 文件 | 路径 |
|------|------|
| OAuth Client JSON | `1-4 Dev/scripts/sentinel/gsc_credentials/oauth-client.json` |
| Refresh Token | `1-4 Dev/scripts/sentinel/gsc_credentials/gsc-token.json` |
| 拉取脚本 | `1-4 Dev/scripts/sentinel/gsc_credentials/gsc_fetch.py` |
| 授权脚本 | `1-4 Dev/scripts/sentinel/gsc_credentials/gsc_auth.py` |

## 日常使用

Pipeline Step 1 自动调用 `gsc_fetch.py` 拉取最近 28 天关键词数据。

```bash
python3 1-4 Dev/scripts/sentinel/gsc_credentials/gsc_fetch.py
```

Token 自动续期（refresh_token 机制），无需手动重新授权。

## 前置条件

- 你有 Lovart.ai (`www.lovart.ai`) 的 GSC 所有权（已验证）
- 你有 Google Cloud 账号
- 你已有 SEO Dashboard 项目（参考 `Product Project Management/SEO Dashboard/凭据申请 SOP.md` 的详细流程）

## Step 1: 确认 GSC Site URL

```bash
# 确认 site URL 格式
# 通常是 https://www.lovart.ai/ 或 sc_domain:lovart.ai
```

## Step 2: 创建 GCP 项目（如已存在可跳过）

1. 打开 https://console.cloud.google.com/
2. 新建项目或选择已有项目（如 "lovart-seo"）
3. 记下 **Project ID**

## Step 3: 启用 Search Console API

```bash
# 在 GCP Console 中搜索 "Google Search Console API" → 启用
# 或直接打开：
# https://console.developers.google.com/apis/api/searchconsole.googleapis.com
```

## Step 4: 创建 OAuth 2.0 凭证

1. 进入 **APIs & Services → Credentials**
2. 创建 **OAuth 2.0 Client ID**
3. 应用类型：**Desktop app**
4. 下载 JSON → 保存为 `config/credentials/gsc-oauth-client.json`

```json
{
  "installed": {
    "client_id": "...",
    "project_id": "lovart-seo",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "...",
    "redirect_uris": ["http://localhost"]
  }
}
```

## Step 5: 首次授权获取 Refresh Token

```bash
pip install google-api-python-client google-auth-oauthlib

python3 Scripts/gsc_auth.py
# → 打开浏览器授权
# → 保存 refresh token 到 config/credentials/gsc-token.json
```

## Step 6: 验证连接

```bash
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

with open('config/credentials/gsc-token.json') as f:
    creds = Credentials.from_authorized_user_info(json.load(f))

service = build('searchconsole', 'v1', credentials=creds)
sites = service.sites().list().execute()
print(sites)
"
```

## Step 7: 集成到 Pipeline

配置完成后，`lovart-data-ingestion` Phase 1a 会自动：

1. 使用 GSC API 拉取最近 28 天关键词数据
2. 提取：查询/点击/展示/CTR/排名
3. 写入 `1-2 Insight/Trident Insights/reports/YYYY-MM-DD/gsc-api/`
4. 供 Step 1b（Notion）或 Step 1c（本地 CSV）降级备用

## 常用 GSC API 查询

```python
# 关键词维度
request = {
    'startDate': '28daysAgo',
    'endDate': 'today',
    'dimensions': ['query'],
    'rowLimit': 100,
    'startRow': 0
}
response = service.searchanalytics().query(siteUrl='https://www.lovart.ai/', body=request).execute()
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `PERMISSION_DENIED` | GSC 所有权不匹配或 API 未启用 | 检查 GSC 站点所有权 → 启用 Search Console API |
| `QUOTA_EXCEEDED` | 每日配额用完 | 免费配额 200 查询/天，降低频率 |
| `401 Unauthorized` | OAuth token 过期 | 重新运行 `gsc_auth.py` 获取新 token |
| `403 Forbidden` | 没有该站点的读取权限 | 在 GSC 中添加该 Google 账号为所有者 |

## 参考

- `Product Project Management/SEO Dashboard/凭据申请 SOP.md` — 完整 8 步 SOP（含 GA4 + Bing + 后端 DB）
- `Product Project Management/GEO-内容引擎/PRD-GEO全自动内容更新工作流.md` — GEO 引擎架构参考
