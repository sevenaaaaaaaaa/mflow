# For 数据对接分析师

> **文档定位**：面向数据对接分析师的操作指南  
> **更新日期**：2026-06-07  
> **适用范围**：Lovart 项目 GSC、Bing、GA4 数据回传到数仓相关人员

> **路径原则**：可执行脚本 SSOT 是 `1-4 Dev/scripts/trident/`。`1-1 Harness/Skills/lovart-trident-data-engine/` 保留为 Agent Skill、历史兼容入口和本地共享凭证位置。真实凭证允许本地项目内保存以便交接，但已通过 `.gitignore` 防止提交。

---

## 一、概述

本文档为数据对接分析师提供完整的操作指南，涵盖 GSC、Bing、GA4 数据采集流程、数据回传到数仓的步骤、云数仓摄入示例、数据表结构说明、常见问题排查等核心内容。

### 1.1 数据源概述

| 数据源 | 用途 | 数据量 | 更新频率 |
|--------|------|--------|----------|
| **GSC** | 关键词排名、点击、曝光、CTR | 5,000 词/月 | 每日（2天延迟） |
| **GA4** | 用户行为、会话、转化 | 全量 | 每日 |
| **Bing** | Bing 关键词排名 | 全量 | 每日 |

### 1.2 数据流架构

```
数据源 → 采集脚本 → JSON 文件 → 数仓摄入 → 云数仓
  ├── GSC API → gsc_fetch.py → gsc-YYYY-MM.json → BigQuery/Snowflake/PostgreSQL
  ├── GA4 API → ga4_fetch.py → ga4-YYYY-MM.json → BigQuery/Snowflake/PostgreSQL
  └── Bing API → bing_fetch.py → bing-YYYY-MM.json → BigQuery/Snowflake/PostgreSQL
```

---

## 二、GSC 数据采集流程

### 2.1 GSC 数据采集脚本

**脚本路径：** `1-4 Dev/scripts/trident/gsc_fetch.py`

**功能：** 从 Google Search Console 采集关键词数据

**数据字段：**
- `clicks`：点击次数
- `impressions`：曝光次数
- `ctr`：点击率
- `position`：平均排名
- `query`：搜索关键词
- `page`：页面 URL
- `country`：国家
- `date`：日期

### 2.2 GSC 数据采集命令

```bash
# 采集 GSC 数据（月报 5,000 词）
python3 "1-4 Dev/scripts/trident/gsc_fetch.py" --month 2026-05

# 采集 GSC 数据（周报 2,000 词）
python3 "1-4 Dev/scripts/trident/gsc_fetch.py" --week 2026-05-25

# 采集 GSC 数据（日报 200 词）
python3 "1-4 Dev/scripts/trident/gsc_fetch.py" --date 2026-05-31
```

### 2.3 GSC 数据产出路径

```
1-4 Dev/Output/Data Ingestion/
├── gsc-5k-2026-05.json          # GSC 5,000 词月报数据
├── gsc-2026-05.json             # GSC 全量月报数据
├── monthly-snapshots/
│   └── gsc-2026-05.json         # GSC 月报快照
```

### 2.4 GSC 数据表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | string | 搜索关键词 |
| `page` | string | 页面 URL |
| `clicks` | integer | 点击次数 |
| `impressions` | integer | 曝光次数 |
| `ctr` | float | 点击率 |
| `position` | float | 平均排名 |
| `country` | string | 国家代码 |
| `date` | string | 日期 |

---

## 三、GA4 数据采集流程

### 3.1 GA4 数据采集脚本

**脚本路径：** `1-4 Dev/scripts/trident/ga4_fetch.py`

**功能：** 从 Google Analytics 4 采集用户行为数据

**数据字段：**
- `sessions`：会话数
- `users`：用户数
- `newUsers`：新用户数
- `conversions`：转化数
- `country`：国家
- `date`：日期

### 3.2 GA4 数据采集命令

```bash
# 采集 GA4 数据（月报）
python3 "1-4 Dev/scripts/trident/ga4_fetch.py" --month 2026-05

# 采集 GA4 数据（周报）
python3 "1-4 Dev/scripts/trident/ga4_fetch.py" --week 2026-05-25

# 采集 GA4 数据（日报）
python3 "1-4 Dev/scripts/trident/ga4_fetch.py" --date 2026-05-31
```

### 3.3 GA4 数据产出路径

```
1-4 Dev/Output/Data Ingestion/
├── ga4-2026-05.json             # GA4 月报数据
├── monthly-snapshots/
│   └── ga4-2026-05.json         # GA4 月报快照
```

### 3.4 GA4 数据表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `sessions` | integer | 会话数 |
| `users` | integer | 用户数 |
| `newUsers` | integer | 新用户数 |
| `conversions` | integer | 转化数 |
| `country` | string | 国家代码 |
| `date` | string | 日期 |

---

## 四、Bing 数据采集流程

### 4.1 Bing 数据采集脚本

**脚本路径：** `1-4 Dev/scripts/trident/bing_fetch.py`

**功能：** 从 Bing Webmaster API 采集关键词数据

**数据字段：**
- `clicks`：点击次数
- `impressions`：曝光次数
- `ctr`：点击率
- `position`：平均排名
- `query`：搜索关键词
- `page`：页面 URL
- `date`：日期

### 4.2 Bing 数据采集命令

```bash
# 采集 Bing 数据（月报）
python3 "1-4 Dev/scripts/trident/bing_fetch.py" --month 2026-05

# 采集 Bing 数据（周报）
python3 "1-4 Dev/scripts/trident/bing_fetch.py" --week 2026-05-25

# 采集 Bing 数据（日报）
python3 "1-4 Dev/scripts/trident/bing_fetch.py" --date 2026-05-31
```

### 4.3 Bing 数据产出路径

```
1-4 Dev/Output/Data Ingestion/
├── bing-2026-05.json            # Bing 月报数据
├── monthly-snapshots/
│   └── bing-2026-05.json        # Bing 月报快照
```

### 4.4 Bing 数据表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | string | 搜索关键词 |
| `page` | string | 页面 URL |
| `clicks` | integer | 点击次数 |
| `impressions` | integer | 曝光次数 |
| `ctr` | float | 点击率 |
| `position` | float | 平均排名 |
| `date` | string | 日期 |

---

## 五、一键全流程采集

### 5.1 全量采集脚本

**脚本路径：** `1-4 Dev/scripts/trident/run_all.sh`

**功能：** 一键采集 GSC、GA4、Bing 数据

### 5.2 全量采集命令

```bash
# 全量采集（GSC+GA4+Bing）
cd "1-4 Dev/scripts/trident" && bash run_all.sh
```

### 5.3 全量采集产出

```
1-4 Dev/Output/Data Ingestion/
├── gsc-2026-05.json             # GSC 月报数据
├── ga4-2026-05.json             # GA4 月报数据
├── bing-2026-05.json            # Bing 月报数据
├── monthly-snapshots/
│   ├── gsc-2026-05.json         # GSC 月报快照
│   ├── ga4-2026-05.json         # GA4 月报快照
│   └── bing-2026-05.json        # Bing 月报快照
```

---

## 六、数据回传到数仓

### 6.1 数据仓库结构

**数据仓库路径：** `1-4 Dev/Output/Warehouse/`

**数据仓库内容：**
- `trident_data.db`：SQLite 数据库
- `2026-05-31/`：CSV 导出目录

### 6.2 数据表结构

| 表 | 说明 | 入仓方式 |
|---|------|---------|
| snapshots | 每日指标快照 (GSC/GA4/Bing) | CSV |
| gsc_keywords | GSC 关键词排名 | CSV |
| gsc_countries | GSC 分国家 | CSV |
| ga4_organic | GA4 自然搜索日趋势 | CSV |
| ga4_trend | GA4 周/月环比 | CSV |
| ga4_channels | GA4 全渠道 | CSV |
| ga4_geo | GA4 分国家 | CSV |
| bing_keywords | Bing 关键词 | CSV |
| bing_pages | Bing 页面 | CSV |
| bing_crawl | Bing 爬虫日统计 | CSV |

### 6.3 数据回传流程

**数据回传流程：**

1. **数据采集**：使用采集脚本采集数据
2. **数据转换**：将 JSON 数据转换为 CSV 格式
3. **数据验证**：验证数据完整性和准确性
4. **数据上传**：将 CSV 文件上传到云数仓
5. **数据摄入**：将 CSV 数据摄入到云数仓表中

### 6.4 数据回传命令

```bash
# 1. 数据采集
cd "1-4 Dev/scripts/trident" && bash run_all.sh

# 2. 数据转换（JSON → CSV）
python3 "1-4 Dev/scripts/convert_json_to_csv.py" --month 2026-05

# 3. 数据验证
python3 "1-4 Dev/scripts/validate_data.py" --month 2026-05

# 4. 数据上传到云数仓
# 具体命令取决于使用的云数仓类型
```

---

## 七、云数仓摄入示例

### 7.1 BigQuery 摄入示例

```bash
# 上传 CSV 文件到 Google Cloud Storage
gsutil cp 2026-05-31/snapshots.csv gs://my-bucket/2026-05-31/snapshots.csv

# 摄入到 BigQuery
bq load --source_format=CSV \
  lovart_trident.snapshots \
  gs://my-bucket/2026-05-31/snapshots.csv
```

### 7.2 Snowflake 摄入示例

```sql
-- 创建 stage
CREATE STAGE my_stage
  URL = 's3://my-bucket/2026-05-31/'
  CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'xxx');

-- 摄入数据
COPY INTO lovart_trident.snapshots
FROM @my_stage/2026-05-31/snapshots.csv
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

### 7.3 PostgreSQL 摄入示例

```sql
-- 创建表
CREATE TABLE snapshots (
  date DATE,
  gsc_clicks INTEGER,
  gsc_impressions INTEGER,
  gsc_ctr FLOAT,
  gsc_position FLOAT,
  ga4_sessions INTEGER,
  ga4_users INTEGER,
  ga4_new_users INTEGER,
  ga4_conversions INTEGER,
  bing_clicks INTEGER,
  bing_impressions INTEGER,
  bing_ctr FLOAT,
  bing_position FLOAT
);

-- 摄入数据
\copy snapshots FROM '2026-05-31/snapshots.csv' CSV HEADER;
```

### 7.4 本地 SQLite 查询

```bash
# 查询最新数据
sqlite3 trident_data.db "SELECT * FROM snapshots ORDER BY date DESC LIMIT 20"

# 查询 GSC 关键词
sqlite3 trident_data.db "SELECT * FROM gsc_keywords ORDER BY clicks DESC LIMIT 20"

# 查询 GA4 趋势
sqlite3 trident_data.db "SELECT * FROM ga4_trend ORDER BY date DESC LIMIT 20"
```

---

## 八、数据验证和质量检查

### 8.1 数据验证脚本

**脚本路径：** `1-4 Dev/scripts/validate_data.py`

**功能：** 验证数据完整性和准确性

### 8.2 数据验证命令

```bash
# 验证月报数据
python3 "1-4 Dev/scripts/validate_data.py" --month 2026-05

# 验证周报数据
python3 "1-4 Dev/scripts/validate_data.py" --week 2026-05-25

# 验证日报数据
python3 "1-4 Dev/scripts/validate_data.py" --date 2026-05-31
```

### 8.3 数据质量检查清单

- [ ] 数据完整性：所有字段都有值
- [ ] 数据准确性：数据范围合理
- [ ] 数据一致性：不同数据源数据一致
- [ ] 数据时效性：数据是最新的
- [ ] 数据唯一性：没有重复数据

---

## 九、常见问题排查

### 9.1 GSC 数据采集问题

**问题：** GSC 数据采集失败
**可能原因：**
- OAuth token 过期
- API 配额超限
- 网络连接问题

**解决方案：**
```bash
# 重新授权 OAuth token
python3 "1-4 Dev/scripts/trident/gsc_auth.py"

# 检查 API 配额
python3 "1-4 Dev/scripts/trident/gsc_fetch.py" --check-quota

# 检查网络连接
ping google.com
```

### 9.2 GA4 数据采集问题

**问题：** GA4 数据采集失败
**可能原因：**
- 服务账号权限问题
- API 配额超限
- 属性 ID 错误

**解决方案：**
```bash
# 检查服务账号权限
python3 "1-4 Dev/scripts/trident/ga4_auth.py"

# 检查 API 配额
python3 "1-4 Dev/scripts/trident/ga4_fetch.py" --check-quota

# 检查属性 ID
python3 "1-4 Dev/scripts/trident/ga4_fetch.py" --check-property
```

### 9.3 Bing 数据采集问题

**问题：** Bing 数据采集失败
**可能原因：**
- API key 错误
- API 配额超限
- 站点验证问题

**解决方案：**
```bash
# 检查 API key
python3 "1-4 Dev/scripts/trident/bing_fetch.py" --check-api-key

# 检查 API 配额
python3 "1-4 Dev/scripts/trident/bing_fetch.py" --check-quota

# 检查站点验证
python3 "1-4 Dev/scripts/trident/bing_fetch.py" --check-site
```

### 9.4 数据回传问题

**问题：** 数据回传到数仓失败
**可能原因：**
- CSV 文件格式错误
- 数仓连接问题
- 权限问题

**解决方案：**
```bash
# 检查 CSV 文件格式
head -5 2026-05-31/snapshots.csv

# 检查数仓连接
python3 "1-4 Dev/scripts/check_warehouse_connection.py"

# 检查权限
python3 "1-4 Dev/scripts/check_warehouse_permissions.py"
```

---

## 十、凭证管理

### 10.1 凭证文件位置

| 文件 | 路径 | 用途 | 获取方式 |
|------|------|------|----------|
| `gsc-token.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GSC OAuth token | 运行 `gsc_auth.py` 首次授权 |
| `oauth-client.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GSC OAuth client | GCP Console → OAuth 2.0 桌面应用 |
| `ga4-token.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GA4 OAuth token | 运行 `ga4_auth.py` 首次授权 |
| `service-account.json` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | GA4 服务账号 | GCP Console → IAM 服务账号 |
| `api_key` | `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` | Bing Webmaster API | Bing Webmaster → API 访问 |

读取顺序：显式文件环境变量 → `LOVART_TRIDENT_CREDENTIALS_DIR` → 用户私有目录 → 项目内 `1-1 Harness/Skills/lovart-trident-data-engine/credentials/` → 脚本目录 fallback。当前策略允许项目内保留真实凭证，重点是不提交到 Git。

### 10.2 凭证更新流程

```bash
# 更新 GSC 凭证
python3 "1-4 Dev/scripts/trident/gsc_auth.py"

# 更新 GA4 凭证
python3 "1-4 Dev/scripts/trident/ga4_auth.py"

# 更新 Bing 凭证
# 手动更新 credentials/api_key 文件
```

### 10.3 凭证安全

⚠️ 所有凭证文件已在 `.gitignore` 中排除。共享项目时需安全分发，不能通过 Git 传输。

---

## 十一、相关文档

- [AGENTS.md](./AGENTS.md) - 项目规则和标准
- [WORKFLOWS.md](./WORKFLOWS.md) - 运维手册
- [For-SEO-负责人.md](./For-SEO-负责人.md) - SEO 负责人操作指南
- [For-北美市场.md](./For-北美市场.md) - 北美市场操作指南
- [For-日本市场.md](./For-日本市场.md) - 日本市场操作指南

---

> **维护者**：Lovart 团队  
> **最后更新**：2026-06-04  
> **版本**：V1.0
