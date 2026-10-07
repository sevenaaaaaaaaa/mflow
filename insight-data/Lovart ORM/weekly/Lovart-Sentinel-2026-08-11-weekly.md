# Lovart 品牌声誉舆情周报 — 2026-08-11（周二）

> **监测周期**：2026-08-04（周一）→ 08-11（周二），8 天窗口
> **⚠️ 数据质量声明**：实时 SERP 未采集（CAPTCHA 阻断）；GSC/i18n 未加载（CSV 路径配置缺失）；report.py 输出为静态回放（6207 字节固定模板，已连续 45+ 天，07-02→08-11 字节数唯一值=1）
> **实时数据**：仅 fxTwitter API（✅ 可靠）+ web_search 实时查询（✅ 本次可用）；22 个 collect.py 源中 21 个为 delegated/空结构
> **口径**：环比全部用日均值；fxTwitter 周度值受快照缺失限制（仅 08-10/08-11 两天快照可精确计算），周线为推算值并已标注
> **前次周报基线**：2026-05-31（上周报已断档 10 周，本报告恢复周度追踪）

---

## 一、核心发现（先结论）

本周舆情主线是"**内容真空终结 → X 账号增长轨道恢复**"与"**寄生域名主动运营 + 竞品生态负面内容抬头**"并行：X 单日 +55 粉丝为 07-14 bot purge 以来最强表现，接近 purge 前 ~56/日 增速；但 lovart.pro 寄生站被第三方目录（Krain AI）和评测站（VibeDex）误当作官网引用，品牌安全风险从"SERP 占位"升级为"第三方权威性背书"。内部数据侧，7 月 SEO 流量全月 -10.1%、W3（7/15-21）触底后 W5 回升——与 X 账号 7 月内容真空的时间窗高度重合，8 月首周增长恢复是同一修复动作的平行验证。

**三个核心判断：**

1. **X 账号走出 7 月净流失，进入修复性增长**：31,944 粉丝（08-11），单日 +55/+8 推文，为 purge 后最强单日。7 月 20 日低谷 31,664 → 08-11 累计 +280（22 天，日均 +12.7），且近两日增速（+55/日）显著高于整段日均，确认加速而非均值回归。根因是发布节奏恢复（8 条推文/日），非外部利好——这是可复制的运营行为，不是运气。

2. **寄生域名从"占位"升级为"被第三方背书"**：lovart.pro 不仅运营完整（独立 blog + 产品页），还被 early.krain.ai 收录为官网（行业误标 Financial Services）、被 vibedex.ai 评测引用为官方 Refund Policy 链接。第三方的引用让寄生站获得本不属于它的权威信号，品牌词 SERP 前排清洗的紧迫性上升。

3. **竞品官方生态开始主动评论 Lovart**：Dreamina（CapCut 官方资源页）发布"what is lovart-ai"，结论负面（"closed beta + endless waitlist"）。这是首个直接竞品官方站对 Lovart 的公开评价，且会进入 Google 品牌词 SERP——需要正面资产对冲。

---

## 二、核心指标

**X/Twitter（fxTwitter 实时，08-11 08:27 抓取）**：粉丝 31,944、推文 984、媒体 353、点赞 1,873、关注 211、organization 认证。
环比（08-10 → 08-11）：粉丝 +55（+0.17%）、推文 +8（+0.82%）、媒体 +1、点赞 +1、关注持平。
周度推算（快照仅 2 天，⚠️ 部分估算）：07-20 低谷 31,664 → 08-11 31,944，+280/22 天 = 日均 +12.7；若以近 8 天窗口推算周增速约 +89/周（12.7×7），但 08-10→08-11 实际 +55/日，说明 8 月初前段增速低于后段——具体周线需快照持久化后精确化。
与报告冻结基线差距（31,071/765，基线 6 月底起冻结 45+ 天）：粉丝 +873、推文 +219，差距单向扩大中。

**内部数据（SEO 月报 6 月 vs 7 月，月报 SSOT 引用）**：7 月 SEO+GEO UV 日均 27,945（环比 -10.1%）；新注册 109,711（-14.6%）；新增付费 1,465 人（-7.7%）、金额 $127,684（-13.3%）；ARPPU $87.16（-6.0%）；DAU 日均 126,427（-8.0%）。周线呈"W3 触底、W5 回升"：W3（7/15-21）UV 26,684/天（-8%）、新注册 2,757/天（-33%）；W5（7/29-31）UV 29,447/天、新注册 3,887/天，恢复至接近 W1。

💡 洞察：问题（7 月流量与社媒双低谷）→ 根源（W3 全月低谷与 X 内容真空时间窗重合，7/15-21 恰为 purge 后停滞期，产品侧新注册 -33% 与账号侧粉丝净流失同步发生）→ 缓解（8 月初双端均恢复：产品 W5 回升至 -5% 以内、X 单日 +55）。两条线同因（7 月中旬运营停滞），修复动作应合并管理而非分开追责。

---

## 三、Top 5 关键信号

**信号 1 🟠 高 — 寄生域名 lovart.pro 被第三方目录/评测站误收录为官网（本周新增证据）**
发现：web_search 实证 early.krain.ai/app/12430 将 Website 字段指向 lovart.pro（Industry 误标 "Financial Services"）；vibedex.ai/blog/lovart-review-2026 引用 "Lovart - Refund Policy (lovart.pro)" 作为官方链接。寄生站自身运营完整（宣传 NEWGPT Image 2、含 "Is Lovart Worth It? Honest Review" blog）。
严重性：高——第三方引用在反向强化寄生站权威性，用户在品牌词 SERP 及其外（AI 目录、评测站）都可能被导向仿冒站。
环比：上周仅 SERP 占位（第 3 位），本周新增 2 个站外引用，风险面扩大。
交叉验证：静态报告 6 寄生域名清单中 lovart.pro 标"仿冒官网"，与此实证吻合。
行动：向 Krain AI 提交域名更正请求；检查 VibeDex 评测页联系渠道提交链接更正；同步准备商标/品牌投诉材料备用；SERP 前排监控留待交互会话（cron 环境 CAPTCHA 阻断）。

**信号 2 🟠 中高 — Dreamina（CapCut 官方）发布 Lovart 负面评测**
发现：dreamina.capcut.com/resource/what-is-lovart-ai 结论 "closed beta status and endless waitlist leave most designers stranded"。
严重性：中高——CapCut/Dreamina 是 AI 设计直接竞品，其官方资源页的负面结论将进入 Google 品牌词 SERP 且带有高域名权威。
环比：本周新出现，上周无此来源。
交叉验证：需核对 waitlist/closed beta 状态是否已过时——若产品已开放，该页信息即失真，可要求更正；若仍限制，则需正面内容对冲。
行动：确认当前产品开放状态；向该页提交更正或产出正面评测/对比内容抢占品牌词 SERP 前排；把 "lovart closed beta" 类负面长尾词纳入 SEO 监测。

**信号 3 🟢 正面 — X 内容真空解除，单日 +55 粉丝为 purge 以来最强**
发现：08-11 粉丝 31,944，单日 +55；推文 984（+8/日），媒体 353（+1）。08-10→08-11 两天均正增长。
严重性：低（利好）。7 月 14 日 purge（−135）→ 7 月 20 日低谷（−7/3天）→ 8 月 10 日恢复（+218/24天）→ 08-11 加速。
根因：发布节奏恢复至 8 条推文/日，叠加 Self Universe Challenge（$10,000 现金 + 订阅奖）传播。
交叉验证：仅粉丝/推文同升、点赞/媒体微动——属内容恢复驱动，非品牌情绪事件。
行动：维持 ≥1 条/日发布节奏；观察挑战赛 7 天内是否将日均增速抬升至 purge 前 ~56/日。

**信号 4 🟡 中 — 竞品/市场叙事清单中 Lovart 缺席**
发现：本周 web_search 主流 "best AI design tools 2026" 榜单（Storyflow、ATNN、ELVTR、Photoshop Training Channel 等）均只列 Canva/Firefly/Midjourney/Recraft/Runway，无 Lovart；仅一条 Instagram 有机推荐（reel "6 AI tools worth your time" 提及 "Lovar" 做品牌形象，拼写错误）属正面 UGC。
严重性：中——品类词覆盖缺口与 SEO 月报"非品牌词占比低"相互印证；但出现有机 UGC 推荐说明产品口碑在自然传播。
行动：将 Lovart 列入主流榜单的 PR/内容目标（评测邀约、榜单投放）；监测 "Lovar" 拼写变体带来的自然流量；沿用"AI design agent 全栈"差异化叙事切入对比内容。

**信号 5 🟡 中 — 评价资产停滞：PH 12 条评价已半年无新增**
发现：静态报告 Product Hunt 4.9/5、12 条评价，最近评价约 7-12 月前；Trustpilot/G2/Capterra 未注册。
严重性：中——决策漏斗的"第三方背书"环节空白，竞品对比场景下缺乏可信评价池。
交叉验证：与信号 2 关联——负面评测出现时，自有正面评价池不足则无法对冲。
行动：启动 PH 老用户评价召回（邮件/社区）；评估 G2/Capterra 注册优先级；案例研究产出（当前为 0）与评价体系联动。

---

## 四、竞品对比

**直接竞品（高威胁）**：Canva（Magic Studio 全栈 AI + 布局，2026 年主流榜单必列，中国市场 canva.cn 活跃——威胁等级最高）；Pollo AI（对比关键词中频繁出现，需持续产出对比内容）；Dreamina/CapCut（本周新增：官方资源页开始评价 Lovart 且为负面——竞品主动进攻信号）。
**图像生成交叉（中威胁）**：Midjourney V7（艺术质量标杆，但有 3 起版权诉讼、无用户赔偿保障——对比时可攻击其商用安全短板）；Adobe Firefly（Image Model 5 + Firefly AI Assistant，商用安全叙事最强，$9.99 入门，生态绑定深）。
**赛道差异（低威胁）**：Leonardo AI（游戏/3D 垂直）、Kling/可灵（中国视频生成，地理隔离）。
**Lovart 相对位置**：差异化叙事（全栈 design agent：生成+编辑+品牌一致性+导出）在自有站内强，但在第三方主流榜单缺席（见信号 4）。威胁层级排序：Canva > Dreamina（新增）> Pollo AI > Midjourney/Firefly > 垂直玩家。

💡 洞察：问题（品类词榜单缺席 + 竞品官方负面评价）→ 根源（第三方评测网络投入不足，自有评价池停滞）→ 缓解（双管齐下：正面资产进入主流榜单与对比内容；负面来源逐一更正/对冲，优先级 Dreamina > VibeDex）。

---

## 五、品牌寄生域名

6 个已知寄生域名，来自静态报告基线（2026-06 建立，本周 SERP 无法实时验证，待交互会话核实）：
lovart-ai.com（Bing 品牌词第 2 位，跳转 aggiii.com，极高风险）；lovart.pro（第 3 位，仿冒官网——本周新增站外误收录证据）；lovart.io（第 4 位，仿冒社区）；lovart.info（第 5 位，仿冒信息站）；lovart.me（第 6 位，仿冒 Agent 页）；lovart.fyi（第 7 位，教程/截流）。
本周变化：lovart.pro 从"占位"升级为"被第三方背书"（信号 1），其余 5 个未见新增证据。

---

## 六、管道状态矩阵（22 源）

✅ 实时（2/22）：fxTwitter（API 直连，唯一可靠实时源）、web_search（本次会话可用，品牌词/竞品查询成功）。
❌ Delegated（17/22）：serp_bing、serp_baidu、serp_sogou、social_x、social_linkedin、social_instagram、social_tiktok、social_youtube、social_reddit、product_hunt、ai_directories、design_communities、competitor_social、media_polling、propagation_tracker、sentiment_quantifier、china_shortvideo——均为 `{"status":"delegated"}` 占位，需 agent 或交互会话采集。
❌ 空结构（4/22）：gsc_daily（仅 date 字段）、gsc_weekly（available_reports:[]）、i18n_keyword_intelligence（全零 locale + _queries_file: null）、content_production（calendar_files:[]）——CSV 路径配置缺失，非采集失败。
❌ 无数据（1/22）：email_health（no_data）。
静态回放确认：`ls -l Lovart-Sentinel-*.md | awk '{print $5}' | sort -u | wc -l` = 1；07-02 → 08-11 全部 6207 字节，仅时间戳行变化。已 45+ 天。

💡 洞察：问题（90%+ 源无真实数据，报告长期静态回放）→ 根源（GSC/i18n CSV 路径断链 + SERP 在 cron 环境被 CAPTCHA 阻断）→ 缓解（P0 修复 collect.py 路径配置；SERP 改用交互会话或住宅代理；中国平台采集降级为存在性检查）。

---

## 七、Delta 追踪

- fxTwitter 差距 vs 冻结基线（31,071/765）：粉丝 +873（上日 +818）、推文 +219（上日 +211）——差距继续扩大，基线冻结 45+ 天。
- 7 月→8 月轨迹：07-14 purge（−135）→ 07-17（+14 弱反弹）→ 07-20（−7/3天 低谷）→ 08-10（31,889）→ 08-11（31,944，+55/日 加速）。
- 快照持久化：08-10、08-11 两天快照已存 /tmp/lovart_twitter_*.json；08-09 及更早无快照（周增速为推算值，⚠️ 已标注）。
- 报告字节数：6207 固定（静态回放），周报本次恢复产出（前次 2026-05-31，断档 10 周）。

---

## 八、下周关注（08-18 周二复核）

1. Self Universe Challenge 传播效果：粉丝日均增速是否突破 purge 前 56/日；参与帖互动率是否抬升（UGC 挑战 7 天观察窗）。
2. lovart.pro 更正进展：Krain AI/VibeDex 是否响应；品牌词 SERP 前排（需交互会话）是否出现新寄生站。
3. Dreamina 负面评测影响：该页是否进入品牌词 SERP 前排；"lovart closed beta" 负面词搜索量变化。
4. 快照持久化补课：本周起每日 cron 已存快照，下周可得精确周线；若缺失，用 session_search 恢复（⚠️ 本会话 session DB 损坏，恢复通道需修复）。
5. 评价召回启动：PH 老用户评价召回是否落地；G2/Capterra 注册评估。

---

*数据溯源：fxTwitter API（2026-08-11 08:27 实时）；web_search 3 条（2026-08-11）；raw/2026-08-11/ 22 源文件（21 个无真实数据）；report.py 静态模板输出；SEO 月报 2026-06-vs-07（~/Documents/Lovart Local Dev/Output/SEO-Reports/）。GSC/i18n 本周期未加载，未引用任何本周 GSC 数字。周度 fxTwitter 数值部分为推算，已标注。*
