# 补数运行记录

区间 2026-01-01 ~ 2026-08-31（契约区间）
运行时间 2026-09-13 15:11:39
脚本 benchmark_fetch_0508.py

## 文件覆盖区间体检

| 文件 | 实际覆盖 | 行数 | 契约区间内缺失 | 字面 '(other)' 行 |
|---|---|---|---|---|
| `bing_page_stats.csv` | 2025-05-30 ~ 2026-09-04 | 4,451 行 | 周粒度快照，非日粒度；67 个快照周 （2025-05-30 ~ 2026-09-04），契约区间内 35 个 | 0 |
| `bing_query_stats.csv` | 2025-05-30 ~ 2026-09-11 | 5,862 行 | 周粒度快照，非日粒度；68 个快照周 （2025-05-30 ~ 2026-09-11），契约区间内 35 个 | 0 |
| `bing_traffic_daily.csv` | 2025-05-13 ~ 2026-09-11 | 487 行 | 无 | 0 |
| `ga4_daily.csv` | 2026-01-01 ~ 2026-08-31 | 243 行 | 无 | 0 |
| `ga4_daily_by_channel.csv` | 2026-01-01 ~ 2026-08-31 | 27,614 行 | 无 | 0 |
| `ga4_daily_by_country.csv` | 2026-01-01 ~ 2026-08-31 | 48,527 行 | 无 | 0 |
| `ga4_daily_by_source_medium.csv` | 2026-01-01 ~ 2026-08-31 | 152,608 行 | 无 | 0 |
| `ga4_daily_nofilter.csv` | 2026-01-01 ~ 2026-08-31 | 243 行 | 无 | 0 |
| `ga4_daily_streamfilter.csv` | 2026-01-01 ~ 2026-08-31 | 243 行 | 无 | 0 |
| `ga4_hostname_audit.csv` | —— | 2,202 行 | 不适用 | 0 |
| `ga4_referral_detail.csv` | 2026-01-01 ~ 2026-08-31 | 8,565,488 行 | 无 | 0 |
| `ga4_referral_landing.csv` | 2026-01-01 ~ 2026-08-31 | 459,233 行 | 无 | 0 |
| `gsc_daily.csv` | 2026-01-01 ~ 2026-08-31 | 243 行 | 无 | 0 |
| `gsc_daily_by_country.csv` | 2026-01-01 ~ 2026-08-31 | 52,132 行 | 无 | 0 |
| `gsc_daily_by_device.csv` | 2026-01-01 ~ 2026-08-31 | 729 行 | 无 | 0 |
| `gsc_daily_by_type.csv` | 2026-01-01 ~ 2026-08-31 | 1,458 行 | discover 缺 0 天; googleNews 缺 0 天; image 缺 0 天; news 缺 0 天; video 缺 0 天; web 缺 0 天 | 0 |
| `gsc_monthly_page.csv` | 2026-01 ~ 2026-08（月粒度） | 63,536 行 | 不适用 | 0 |
| `gsc_monthly_query.csv` | 2026-01 ~ 2026-08（月粒度） | 271,942 行 | 不适用 | 0 |
| `gsc_query_coverage.csv` | 2026-01 ~ 2026-08（月粒度） | 8 行 | 不适用 | 0 |

## '(other)' 折叠核对（GA4 高基数维度）

- 全部产出文件里都没有字面 '(other)' 行（逐行核对）—— 即便 GA4 元数据报过 dataLossFromOtherRow，落到文件里的行都是真值

## 数据质量标记

- [INFO] GSC 可访问属性: https://www.lovart.art/(siteOwner), https://docs.lovart.ai/(siteUnverifiedUser), https://www.liblib.tv/(siteUnverifiedUser), https://blogs.lovart.ai/(siteUnverifiedUser), https://www.lovart.ai/(siteOwner)
- [WARN] GSC 属性 https://docs.lovart.ai/ 权限 siteUnverifiedUser 不足（searchanalytics 会 403），不参与口径选择
- [WARN] GSC 属性 https://www.liblib.tv/ 权限 siteUnverifiedUser 不足（searchanalytics 会 403），不参与口径选择
- [WARN] GSC 属性 https://blogs.lovart.ai/ 权限 siteUnverifiedUser 不足（searchanalytics 会 403），不参与口径选择
- [WARN] GSC 另有子域/它站 URL 前缀属性 ['https://www.lovart.art/'] —— 与 lovart.ai 网站口径不同，不并入
- [WARN] 账号下不存在 sc-domain:lovart.ai 域名属性，只有 URL 前缀口径，非 www 与子域的曝光量不在其中（这是 §3.3 差异的一个独立解释）
- [INFO] GSC 正式口径 = https://www.lovart.ai/（sfx=''）
- [INFO] GSC 各 searchType 点击: web=6,258,308, image=1,999, video=87, news=0, discover=22, googleNews=0
- [INFO] 品牌词判定使用 SSOT lovart_brand_match.is_brand()
- [INFO] GA4 账号下共 2 个属性:
      properties/403618427 | 北京奇点星宇科技有限公司 | account=qidianxingyu
      properties/524662832 | blogs.lovart.ai | account=Lovart Academy
- [INFO] 目标属性 properties/403618427 → properties/403618427 | 北京奇点星宇科技有限公司 | account=qidianxingyu
- [INFO] 属性时区 = America/Los_Angeles，货币 = USD（日粒度与 DataWorks 大盘表对齐前必须确认时区一致，否则按天 join 会错位一天）
- [INFO] GA4 属性 properties/403618427 下共 4 个数据流:
      6653140555 | shakker | https://www.shakker.ai
      8142537412 | Picpic | https://www.picpic.art
      8142546104 | LiblibAI | https://www.liblib.art
      10524753059 | Lovart | https://www.lovart.ai
- [INFO] 写死的 stream 10524753059 → 10524753059 | Lovart | https://www.lovart.ai
- [WARN] 该属性有 4 个数据流，说明确实混了多个站/端 —— 本脚本用 hostName 含 'lovart.ai' 作为正式口径
- [INFO] GA4 保留期探测：2026-01-01~2026-08-31 有数据 243 天，最早 2026-01-01，最晚 2026-08-31
- [WARN] GA4 属性内 hostName 共 2202 个；lovart.ai 占会话 59.5% —— 属性确实混了别的站，必须按 hostName 过滤
- [WARN] GA4 ga4_referral_detail.csv 2026-01 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] GA4 ga4_referral_detail.csv 2026-02 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] GA4 ga4_referral_detail.csv 2026-03 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] GA4 ga4_referral_detail.csv 2026-04 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] GA4 ga4_referral_detail.csv 2026-05 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] GA4 ga4_referral_detail.csv 2026-06 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] GA4 ga4_referral_detail.csv 2026-07 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] GA4 ga4_referral_detail.csv 2026-08 出现 (other) 行折叠（metadata.dataLossFromOtherRow），高基数维度尾部被聚合
- [WARN] ga4_referral_detail.csv: 8,565,488 行 / 1112.1 MB —— 已按日×来源全量落盘，未做任何 top-N 裁剪
- [WARN] ga4_referral_landing.csv: 459,233 行 / 29.5 MB —— 已按日×来源全量落盘，未做任何 top-N 裁剪
- [INFO] Bing 账号下站点: https://blogs.lovart.ai/ | verified=False, https://www.liblib.tv/ | verified=False, https://www.lovart.ai/ | verified=True
- [WARN] 匹配到多个 lovart 站点 ['https://blogs.lovart.ai/', 'https://www.lovart.ai/']，使用 https://www.lovart.ai/（优先已验证）
- [INFO] Bing 正式口径 = https://www.lovart.ai/
- [INFO] Bing GetRankAndTrafficStats 无翻页参数即整段返回：窗口 2025-05-13 ~ 2026-09-11，487 天（含契约区间外的历史，未裁剪）。契约区间 2026-01-01~2026-08-31 内 243 天，点击 1,510,000 / 曝光 4,829,864
- [INFO] Bing 契约区间内无缺失日期
- [WARN] bing_query_stats.csv: 5,862 行 / 68 个周快照 × 每周 中位 100 条（min 30 / max 100），窗口 2025-05-30 ~ 2026-09-11。该接口每周只给 top-N 且无翻页参数，不是全量 —— 占比分析必须用 bing_traffic_daily.csv 做分母
- [WARN] bing_page_stats.csv: 4,451 行 / 67 个周快照 × 每周 中位 77 条（min 8 / max 100），窗口 2025-05-30 ~ 2026-09-04。该接口每周只给 top-N 且无翻页参数，不是全量 —— 占比分析必须用 bing_traffic_daily.csv 做分母
- [INFO] 品牌词规则快照已导出 brand_rules_snapshot.json（lovart_brand_match.py sha256 0fac3c9858feb12e）
- [INFO] 口径提醒：GA4 原始 date 为 YYYYMMDD，本脚本已统一归一成 YYYY-MM-DD，与 GSC/Bing 可直接按天 join；Bing QueryStats/PageStats 的 date 是每周快照标记日（每周一条，非日粒度）
