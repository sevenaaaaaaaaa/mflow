# 三引擎配置引导

> 按顺序配置 GSC > GA4 > Bing。全部打通后跑 `bash scripts/run_all.sh`。

## GSC (Google Search Console) — OAuth 2.0

### Step 1: 创建 GCP OAuth 凭证 (5 分钟)

1. https://console.cloud.google.com/ → 选择项目
2. 启用 "Google Search Console API"
3. APIs & Services → Credentials → Create OAuth Client ID
4. **应用类型: Desktop app**，名称随意
5. 下载 JSON → 放到 `credentials/oauth-client.json`

### Step 2: 首次授权 (2 分钟)

```bash
python3 scripts/gsc_auth.py
```

浏览器打开 → 选 Google 账号 → 允许 → 返回终端显示 ✅。

完成后 `credentials/gsc-token.json` 自动生成。

### Step 3: 验证

```bash
python3 scripts/gsc_fetch.py
```

应输出 Top 50 关键词 + 国家分布。

---

## GA4 (Google Analytics 4) — OAuth 2.0

### Step 1: 创建 GCP OAuth 凭证 (复用同一项目)

1. APIs & Services → Enable "Google Analytics Data API"
2. Credentials → Create OAuth Client ID → **Desktop app**
3. 下载 JSON → 放到 `credentials/service-account.json`

### Step 2: 首次授权

```bash
python3 scripts/ga4_auth.py
```

浏览器授权后自动列出你的 GA4 Properties。

### Step 3: 确认 Property ID

脚本 `ga4_fetch.py` 中 `PROPERTY` 变量需指向 lovart.ai 的 Property（默认 `properties/403618427`）。

### Step 4: 验证

```bash
python3 scripts/ga4_fetch.py
```

应输出 30 天有机流量 + 用户数据。

---

## Bing (Bing Webmaster) — API Key (最简单)

### Step 1: 获取 Key (1 分钟)

1. https://www.bing.com/webmasters/ → 登录
2. 右上角齿轮 → **API Access**
3. 复制 API Key

### Step 2: 保存

```bash
echo "YOUR_KEY" > credentials/api_key
```

### Step 3: 验证

```bash
python3 scripts/bing_fetch.py
```

应输出 4,000+ 关键词 + 爬虫统计 + `XXX 天 / N 月` 流量序列。

### Bing 月度口径说明（重要）

| 接口 | 时间粒度 | 用途 |
|------|:--:|------|
| `GetRankAndTrafficStats` | **日序列**（约 13 个月 Date/Clicks/Impressions） | 按月聚合 → 站点级**月度点击/曝光/CTR + 环比**（报告 §13.1） |
| `GetQueryStats` / `GetPageStats` | **每周快照**（QueryStats 记录含 `Date`，每周约 top~100 词/页） | **按 (月, 词/页) 聚合 → 月度关键词/页面**：clicks/impr 求和、`AvgImpressionPosition` 曝光加权 = 词位、自算 CTR、可环比 → 报告 §四/§九/§十 Bing 分块 |
| `GetCrawlStats` | 近 N 天 | 收录/爬取（§13.2） |

> ✅ **重大修正（2026-06）**：`GetQueryStats`/`GetPageStats` 实际返回 `QueryStats` 记录，字段为 `Query`(=词或URL)/`Clicks`/`Impressions`/`AvgImpressionPosition`/`AvgClickPosition`/**`Date`（每周）**。早期解析用错元素名（`ClickThroughRate`/`Position`）导致 CTR/排名恒为 0，且因忽略 `Date` 误判为「滚动累计、不可按月」。现 `bing_fetch.py` 输出 `keywords_monthly` / `pages_monthly`（键名对齐 GSC：`q`/`url`/`clicks`/`impr`/`ctr`/`pos`），Bing 关键词/页面已可**月度对比**。
>
> ⚠️ 仍有的限制：① Bing 每周仅 top~100 词（月度约 200+ 去重词，远少于 GSC 5K）；② `AvgClickPosition` 多为 -1，词位用 `AvgImpressionPosition`；③ **无 country/geo 维度** → 分地区（§十一）只 Google，Bing 分国需用 GA4 `country×sessionSource`。

---

## Yandex (Yandex Webmaster) — OAuth 2.0（需先验证站点）

> 仅当 lovart.ai 有俄语市场流量（站点有 `/ru/`）时有意义。**前置条件由用户在自己的 Yandex 账号完成**，Agent 无法代办。

### Step 1: 在 Yandex.Webmaster 添加并验证站点

1. https://webmaster.yandex.com/ → 登录 → 添加 `https://www.lovart.ai/`
2. 验证所有权（DNS TXT / HTML 文件 / meta 标签任一）

### Step 2: 注册 OAuth 应用拿 token

1. https://oauth.yandex.com/client/new → 平台选 **Web services**
2. Redirect URI: `https://oauth.yandex.ru/verification_code`
3. 勾选权限：`webmaster:hostinfo`（+ 如需验证 `webmaster:verify`）
4. 浏览器打开 `https://oauth.yandex.ru/authorize?response_type=token&client_id=<ClientID>`，授权后从回调 URL 的 `#access_token=` 取出 token（**有效期 6 个月**）
5. 保存：`echo "YOUR_TOKEN" > credentials/yandex_token`

### Step 3: 调 API（REST/JSON，base `https://api.webmaster.yandex.net/v4/`）

请求头：`Authorization: OAuth <token>`

| 步骤 | 端点 |
|------|------|
| 取 user_id | `GET /v4/user/` |
| 取 host_id | `GET /v4/user/{user_id}/hosts` |
| **月度查询时序** | `GET /v4/user/{uid}/hosts/{hid}/search-queries/all/history?query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`（**支持 date_from/date_to → 可按月拆分**）|
| 热门词 | `GET /v4/user/{uid}/hosts/{hid}/search-queries/popular` |
| 收录时序 | `GET /v4/user/{uid}/hosts/{hid}/search-urls/in-search/history` |

> Yandex 与 Bing 不同：查询分析**支持日期范围**，能真正按月对比。待用户放好 `credentials/yandex_token` 且站点已验证后，再实现 `yandex_fetch.py`（镜像 `bing_fetch.py`）。

---

## 一键运行

```bash
bash scripts/run_all.sh
```

产出:
- `gsc-full.json`
- `ga4-full.json`
- `bing-full.json`
- `intelligence-brief.md`

## 依赖安装

```bash
pip3 install google-api-python-client google-auth-oauthlib zeep requests
```
