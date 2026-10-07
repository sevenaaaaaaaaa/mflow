# 任务：为「Lovart 海外增长 Benchmark」补齐曝光侧数据（GSC / GA4 / Bing）

## 背景
已有一份基于 DataWorks 三张表（大盘/SEO/SEM）的 5–8 月增长复盘，链路「访问→注册→生图
→付费」已算清，但缺曝光侧。缺这一层，「GAP 到底在媒体曝光→访问、还是访问→注册」只能
部分回答。你跑在本机原生环境，可直连 googleapis.com。只读取，不写任何线上系统。

## 优先直接跑现成脚本
```bash
cd ~/Obsidian/MindRe/MindRe/1-Project/Lovart\ MFlow/1-4\ Dev/scripts/trident
python3 benchmark_fetch_0508.py --audit-only            # 先跑审计，2 分钟，看 §3 结论
python3 benchmark_fetch_0508.py 2026-01-01 2026-08-31   # 审计没问题再拉全量
```
脚本已按 §2/§3 的全部要求实现（含翻页到底、全 searchType、hostName 过滤、抽样检测），
输出到 `insight-data/From Datawork/benchmark-2026-05-08/`，并自动生成 `_RUN-NOTES.md`。
跑不通就按 §2/§3 自己实现，产物契约以本文档为准。

治理：`benchmark_fetch_0508.py` 是新增脚本，请走 `lovart-new-tool-governance` →
`governance_check.py`，PASS 后在 `harness/09-scripts/TOOLS-REGISTRY.md` 追加一行
（owner: lovart-reports，purpose: 固定区间曝光侧补数）。

## §1 凭证（已验证可用，不要重新授权、不要轮换 token）
- GSC  `dev/scripts/sentinel/gsc_credentials/gsc-token.json`（`webmasters.readonly`）
- GA4  `dev/scripts/sentinel/ga4_credentials/ga4-token.json`（`analytics.readonly`）
      property `403618427`，stream `10524753059`
- Bing `dev/scripts/sentinel/bing_credentials/api_key`
解析顺序沿用 `trident/credential_paths.py`。

## §2 三个 API 的「默认只返回一部分」——必须显式绕开

这一节是本次任务的重点。按默认参数调用，三个源都会静默地只给你一部分数据。

### 2.1 GSC Search Analytics
| 默认行为 | 后果 | 必须怎么做 |
|---|---|---|
| `rowLimit` 默认 **1000** | 只拿到前 1000 行 | 设 25000（API 上限），用 `startRow` 翻页直到返回行数 < rowLimit |
| `startRow` 硬上限 **100000** | 超过就再也拿不到 | 触到就记进 notes，并把该维度改按更细时间段分段请求 |
| `type` 默认 **web** | 漏掉 image / video / news / discover / googleNews | 循环全部 6 种 searchType，各存一列；同时保留 web-only 一份对齐历史报告 |
| `dataState` 默认 **final** | 漏掉最近几天未定稿数据 | 设 `"all"` |
| `query` 维度有**匿名化阈值** | 低频词整条不返回，query 行点击数之和 < 日粒度总点击 | 必须计算并输出覆盖率：`sum(query clicks) / total clicks`，逐月记录 |

**匿名化这条最关键**：品牌词/非品牌词占比只在覆盖到的那部分里成立。请输出
`gsc_query_coverage.csv`（month, query_rows, clicks_in_query_rows, total_web_clicks, coverage），
覆盖率低于 70% 的月份要在 notes 里明确告警。另外 query 维度**按自然月**请求，不要按天——
按天会让更多词掉到匿名化阈值以下，覆盖率反而更差。

### 2.2 GA4 Data API
| 默认行为 | 后果 | 必须怎么做 |
|---|---|---|
| `limit` 默认 **10000** | 高基数维度被截断 | 设 250000（上限），读 `rowCount` 用 `offset` 翻页到底 |
| 高基数维度折叠 **`(other)`** | 尾部被聚合成一行，明细丢失 | 检查 `metadata.dataLossFromOtherRow` + 扫描维度值里的 `(other)`，有就告警 |
| 长区间/高基数触发**抽样** | 数字不准但不报错 | 检查 `metadata.samplingMetadatas`，非空要记抽样率；按自然月分段请求降低概率 |
| `keepEmptyRows` 默认 false | 零值日期缺行，做日序列会断 | 设 true |
| 事件数据保留期（2 或 14 个月） | 1–4 月可能根本取不到 | 先探测，取不到就退到 5–8 月并在 notes 说明 |

### 2.3 Bing Webmaster API
`GetQueryStats` / `GetPageStats` 返回的是**每周快照的 top-N**，不是全量，而且没有翻页参数。
所以：
- **站点总量必须用 `GetRankAndTrafficStats`**，不要用 QueryStats 加总当分母
- QueryStats 只用来看词的相对结构，并在 notes 里写明「每周 N 条 × M 周」的实际覆盖
- Bing 数据窗口通常只有最近 6 个月，1 月大概率取不到

## §3 口径审计：先确认拉的是不是 lovart.ai 的数据

**GA 账号里接了不止 lovart.ai 一个站，这是本次最容易出错的地方。**
在拉大数据之前先跑 `--audit-only`，把下面四件事确认清楚，写进 `_RUN-NOTES.md`：

### 3.1 GA4 到底哪部分是 lovart.ai —— 三层都要查
1. **属性层**：调 Admin API `accountSummaries.list()`，列出账号下全部属性及 displayName，
   确认 `403618427` 对应的就是 lovart.ai，输出 `ga4_property_inventory.txt`。
   如果它其实是个汇总属性或别的站，立刻停下来报告，不要继续拉。
2. **数据流层**：调 `properties.dataStreams.list()`，列出该属性下所有数据流及其 `defaultUri`，
   输出 `ga4_stream_inventory.txt`。确认写死的 stream `10524753059` 的 defaultUri 含 lovart.ai。
   数据流数量 > 1 就说明属性确实混了多个站/端。
3. **内容层（正式口径）**：先出 `ga4_hostname_audit.csv`（不加任何过滤，维度 `hostName`，
   看这个属性里到底有哪些域名、各占多少会话）。然后**正式数据一律用
   `hostName CONTAINS "lovart.ai"` 过滤**，而不是用 streamId——streamId 只保证"哪个采集端"，
   不保证"哪个域名"，一个流服务多域名时会串。

同时导出三份日粒度总量做对照，让我能量化每层过滤丢了多少：
`ga4_daily_nofilter.csv`（不过滤）、`ga4_daily_streamfilter.csv`（旧 stream 口径）、
`ga4_daily.csv`（hostName 口径，正式）。

### 3.2 GA4 属性时区
调 `properties.get()` 拿 `timeZone` 写进 notes。DataWorks 大盘表是按业务日期分区的，
两边时区不一致的话按天 join 会整体错位一天，所有日环比都会错。

### 3.3 GSC 属性口径
调 `sites().list()` 列出全部可访问属性。现有脚本写死的是 URL 前缀属性
`https://www.lovart.ai/`，它会漏掉非 www 和其它子域。
**如果存在 `sc-domain:lovart.ai` 域名属性，两种口径都拉一份**，文件名用
`_scdomain` / `_urlprefix` 后缀区分。
背景：现有数据里 GSC 记录的 Google 点击约 11,198/天，而大盘口径下自然 SEO-Google 的
站内访问 UV 只有约 5,288/天，差 53%。先排除「属性口径漏量」这个解释，再谈归因损耗。

### 3.4 Bing 站点口径
调 `GetUserSites` 列出账号下全部站点，确认 lovart.ai 在 Bing 侧注册的 siteUrl 到底写成
`https://www.lovart.ai/` 还是 `https://lovart.ai/`，用匹配到的那个，输出 `bing_site_inventory.txt`。

## §4 产物契约
区间 **2026-01-01 ~ 2026-08-31**（受保留期限制取不到就退到 2026-05-01 ~ 08-31 并注明）。
UTF-8 CSV 带表头，落到 `insight-data/From Datawork/benchmark-2026-05-08/`。

**审计类**
`ga4_property_inventory.txt` · `ga4_stream_inventory.txt` · `ga4_hostname_audit.csv`
`bing_site_inventory.txt` · `gsc_query_coverage.csv` · `_RUN-NOTES.md`

**GSC**（若两种属性都在，每个文件出两份，带 `_scdomain` / `_urlprefix` 后缀）
| 文件 | 维度 | 指标 |
|---|---|---|
| `gsc_daily.csv` | date（web only） | clicks, impressions, ctr, position |
| `gsc_daily_by_type.csv` | date, search_type（6 种全量） | 同上 |
| `gsc_daily_by_device.csv` | date, device | 同上 |
| `gsc_daily_by_country.csv` | date, country | 同上 |
| `gsc_monthly_query.csv` | month, query, **is_brand** | 同上 |
| `gsc_monthly_page.csv` | month, page | 同上 |

**GA4**（指标统一：sessions, totalUsers, newUsers, activeUsers, engagedSessions,
averageSessionDuration, bounceRate, screenPageViews）
| 文件 | 维度 | 过滤 |
|---|---|---|
| `ga4_daily.csv` | date | hostName ∋ lovart.ai（正式） |
| `ga4_daily_streamfilter.csv` | date | streamId 旧口径（对照） |
| `ga4_daily_nofilter.csv` | date | 无（对照） |
| `ga4_daily_by_channel.csv` | date, sessionDefaultChannelGroup, firstUserDefaultChannelGroup | hostName |
| `ga4_daily_by_source_medium.csv` | date, sessionSource, sessionMedium | hostName |
| `ga4_daily_by_country.csv` | date, country | hostName |
| `ga4_referral_detail.csv` | date, sessionSource, pageReferrer | hostName + sessionMedium=referral |
| `ga4_referral_landing.csv` | date, sessionSource, landingPage | hostName + sessionMedium=referral |

**Bing**
`bing_traffic_daily.csv`（date, impressions, clicks，来自 GetRankAndTrafficStats）·
`bing_query_stats.csv` · `bing_page_stats.csv`

其它要求：
- **日粒度不要预聚合**，不要只给 top-N 汇总，分析侧要自己切
- `is_brand` 列用项目 SSOT `dev/scripts/lovart_brand_match.py` 的 `is_brand()` 生成，
  **不要自己另写品牌词规则**；同时导出 `brand_rules_snapshot.json` 记录当前生效规则

### 为什么要 referral 明细（§4 里最有价值的一项）
大盘里「Referer 引荐」是全站最大流量来源（278 万 UV，占 33.8%），但平台归因 **100% 是
"未知"**，无法下钻。它生图率全渠道最高、付费率全渠道最低，这个反差很可能是里面混了
性质完全不同的子来源被平均掉了。拆出真实来源域名基本能直接改写整份复盘的第 4、5 节。

## §5 `_RUN-NOTES.md` 必须包含
- §3 四项审计的结论（尤其：403618427 是不是 lovart.ai、属性内 lovart.ai 占多少会话、属性时区）
- 每个文件实际覆盖的日期区间，缺失日期逐个列出
- GA4：哪些请求被抽样、抽样率；哪些出现 `(other)` 折叠
- GSC：query 覆盖率逐月数值；哪些请求触到 25000/100000 上限被截断；最后一个完整数据日期
- Bing：QueryStats 实际是「每周 N 条 × M 周」，以及数据窗口起止
- 任何一步失败的原始报错（不要吞掉）

## §6 不要做的事
- 不要重新授权或轮换任何 token
- 不要改动 `trident/` 下已有脚本
- 不要写入任何线上系统（Sanity / 飞书 / 数据仓库）
- 不要用 top-N 汇总代替明细，不要为了"看起来干净"丢掉尾部
- 不要自己下结论或写分析报告，只交数据 + `_RUN-NOTES.md`
