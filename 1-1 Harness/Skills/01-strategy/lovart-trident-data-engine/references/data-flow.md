# 三引擎数据流

## 架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   GSC API   │     │   GA4 API   │     │  Bing API   │
│ (OAuth 2.0) │     │ (OAuth 2.0) │     │  (API Key)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       ▼                   ▼                   ▼
  gsc_fetch.py       ga4_fetch.py       bing_fetch.py
       │                   │                   │
       ▼                   ▼                   ▼
  gsc-full.json      ga4-full.json      bing-full.json
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
        unified_brief  warehouse  feishu
                │          │          │
                ▼          ▼          ▼
        brief.md   SQLite+CSV  Bitable
```

## 输出路径

所有输出到 `1-6 Knowledge Base/Insight/Keywords Research/SEO Report/`：

| 文件 | 来源 | 大小 (典型) |
|------|------|-----------|
| `gsc-full.json` | GSC API | ~21KB |
| `ga4-full.json` | GA4 API | ~24KB |
| `bing-full.json` | Bing API | ~620KB |
| `intelligence-brief.md` | unified_brief.py | ~2KB |

## 数仓输出

所有输出到 `Lovart/Output/Warehouse/`：

| 文件 | 说明 |
|------|------|
| `trident_data.db` | SQLite 数仓 (10 张表) |
| `YYYY-MM-DD/*.csv` | 每日 CSV 导出 |
| `YYYY-MM-DD/*.parquet` | 每日 Parquet 导出 (需 pyarrow) |

## 飞书输出

| 目标 | 说明 |
|------|------|
| Base `ZLWgbi6VIaCRiNsb22jcNpPRnfh` | Lovart-Home |
| 表 "SEO 数据看板" | 自动创建，每日追加快照 |

## 凭证位置

| 凭证 | 路径 | 格式 |
|------|------|------|
| GSC OAuth Client | `credentials/oauth-client.json` | OAuth 2.0 desktop app |
| GSC Token | `credentials/gsc-token.json` | Auto-generated (refresh token) |
| GA4 OAuth Client | `credentials/service-account.json` | OAuth 2.0 desktop app |
| GA4 Token | `credentials/ga4-token.json` | Auto-generated (refresh token) |
| Bing API Key | `credentials/api_key` | Plain text |

## Token 续期

- GSC: `gsc-token.json` 中的 `refresh_token` 自动续期，无需手动操作
- GA4: `ga4-token.json` 同上，refresh_token 自动续期
- Bing: API Key 长期有效，无需续期

## 数据量

| 引擎 | 数据覆盖 | 关键词数 | 每日新增 |
|------|---------|---------|---------|
| GSC | 28 天 | 100 (API limit) | ~3 KB |
| GA4 | 30 天 | N/A | ~2 KB |
| Bing | 全部历史 | 4,421 | ~20 KB |
