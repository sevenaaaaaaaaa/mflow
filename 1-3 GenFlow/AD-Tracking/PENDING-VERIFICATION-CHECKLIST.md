# 待人工核实清单 · 取证入口

> **进度：3.5/9 已完成**（巨量 ✅ · 百度 ✅ · 360 搜索+移动+回传API ✅ —— 2026-07-29 用户提供官方文档）
> 360 仅剩「展示广告花括号宏定义表」未拿到（现有来源为 open.e.360.cn 的 API 请求示例，`{qaid}` 语义未知）。

> 配套 `AD-TRACKING-PARAM-SPEC-v2-RESEARCH.md`。
> 分两类：**A 类**是公开页但机器抓不到（JS 渲染 / 图片 / 域名黑名单），用带渲染的浏览器打开即可；**B 类**必须你的登录态。
> 每项都写明：链接 → 打开后找什么 → 回来要给我什么。

---

## A 类 · 公开页，无需登录（可以让我用浏览器工具试，或你自己打开截图）

### ~~A1. 巨量引擎~~ ✅ 已完成（2026-07-29，用户提供《巨量 URL 规范》）

- **链接**：https://event-manager.oceanengine.com/docs/8650/track_url_doc
- **为什么抓不到**：整站 SPA，`web_fetch` 只返回空壳
- **打开后找什么**：页面里的「监测链接宏参数」大表格
- **要给我什么**：整张表（宏名 + 含义 + 取值枚举）。重点确认三件事：
  1. `__CSITE__` 的完整版位枚举（我现在只有部分区间）
  2. 搜索广告是否真的没有关键词宏（`__KEYWORD__` / `__QUERY__` / `__KEYWORD_ID__` / `__MATCH_TYPE__`）
  3. `__CONVERT_ID__` 的官方定义
- **备用入口**：巨量引擎后台 →【资产】→【事件管理】→ 新建转化时的宏说明浮层

### ~~A2. 百度~~ ✅ 已完成（2026-07-29，用户提供 4 份官方文档：信息流应用API埋码指南 / 搜索程序调用示例 / BD_VID注入方案 / IOS归因升级方案v1.9）

- **链接**：
  - 通配符主表 https://dev2.baidu.com/content?sceneType=0&pageId=100230&nodeId=332
  - 搜索监测参数 https://dev2.baidu.com/content?sceneType=0&pageId=101214&nodeId=662
  - 信息流监测参数 https://dev2.baidu.com/content?sceneType=0&pageId=101213&nodeId=663
- **为什么抓不到**：纯 JS 渲染，返回空 body
- **要给我什么**：通配符全表。重点确认：
  1. `{os}` / `{age}` / `{gender}` 到底存不存在（我判定不存在，需一锤定音）
  2. `{userid}` 在百度侧是否存在
  3. `{trig_flag}` / `{crowdid}` 的正式宏名（我只从线上真实投放 URL 里观察到 `a_trig_flag` / `a_crowdid`）
  4. `{matchtype}` 现行取值到底是「1精确/2短语/3广泛」还是「3=智能匹配」
  5. 信息流侧 `{{IDEA_ID}}` 是否正确

### ~~A3. 360 搜索~~ ✅ 已完成（2026-07-29，用户提供《360设置URL》+《360点睛-转化数据回传API对接文档 2025-07》，已覆盖搜索/展示/移动/点击下发四条产品线与完整回传规范）。⚠️ 仍缺：360 **展示广告的花括号宏定义表**（现有来源仅为 open.e.360.cn 的 API 请求示例，`{qaid}` 语义未知）

- **链接**：
  - 帮助中心 https://e.360.cn/static/help/list.html →【设置URL】与【URL通配符规则】两节（目录项是 `javascript:;`，需点开）
  - 营销学苑图文 http://yingxiao.360.cn/optimizate/58047ee98fa7b.html（3 张参数表是**图片**，需要截图给我）
- **要给我什么**：
  1. 那 3 张图（URL参数列表 / 参数映射表 / 可添加层级表）
  2. **`{wordid}` 与 `{keywordid}` 到底是什么关系** —— 两个来源直接矛盾：2015 官方说 `{wordid}` 是 CityHash64 且跨组不唯一；2022 代理商说 `{keywordid}` 每个关键词唯一。可能是新增/替换，也可能并存
  3. 360 是否有类似 `bd_vid` 的自动 click id

### A4. Snapchat —— 宏下拉字面量

- **链接**（5 篇，全是 Salesforce Experience Cloud JS 站）：
  - https://businesshelp.snapchat.com/s/article/url-parameters
  - https://businesshelp.snapchat.com/s/article/add-url-macros
  - https://businesshelp.snapchat.com/s/article/url-parameters-faq
  - https://businesshelp.snapchat.com/s/article/edit-dynamic-macros
  - https://businesshelp.snapchat.com/s/article/dynamic-ads-parameters
- **要给我什么**：宏列表的**逐字字面量**。重点确认：
  1. `{{adSet.id}}` 的 camelCase 大写 S 是否正确
  2. `{{creative.type}}` / `{{ad.is.swipeable}}` 是否真的不存在（我判定不存在）
  3. 是否有 `{{ad.name}}` / `{{placement}}`
  4. Collection Ads 有无专属参数
- **备用**：Snapchat Ads Manager 里编辑广告 → URL 字段旁的 Macros 下拉，直接截图更准

### A5. Naver —— `n_*` 取值字典 + GFA

- **链接**：
  - https://help.searchad.naver.com/（被我的抓取工具域名黑名单拦截，你打开没问题）
  - 搜索「자동 추적 URL 파라미터」
  - GFA：https://saedu.naver.com/ 或 성과형디스플레이광고 帮助中心
- **要给我什么**：
  1. `n_campaign_type` / `n_ad_group_type` / `n_media` / `n_rank` 的**取值枚举**（我只拿到了 `n_match` 的）
  2. 确认 `n_campaign`（无 `_type`）确实不存在
  3. **GFA（성과형 디스플레이광고）是否有 URL 宏** —— 这块我完全没证据

### A6. LinkedIn —— UI 花括号语法

- **链接**：https://www.linkedin.com/help/lms/answer/a5968064（LinkedIn help 全站返回空响应）
- **要给我什么**：Campaign Manager 里 URL tracking parameters 下拉给出的**字面量**。
  API 侧确认是裸枚举 `CAMPAIGN_ID`（UPPER_SNAKE_CASE），但 UI 是否包 `{{ }}` 未确证 —— 我现在按 `{{CAMPAIGN_ID}}` 写的，需要你确认。
- **备用（更准）**：Campaign Manager → 任意 Campaign →【Tracking】→ URL tracking parameters → 点开下拉截图

### A7. Reddit —— 宏字面量列

- **链接**：
  - https://advertising.reddithelp.com/en/categories/creating-ads/how-build-campaign（能抓到，但 markdown 转换把**宏字面量那一列丢了**，只剩描述列）
  - https://business.reddithelp.com/s/article/Set-up-third-party-measurement
- **要给我什么**：那张 19 行表的**宏字面量列**。我已确证的只有 `{{CAMPAIGN_ID}}` 和 `{{ADGROUP_ID}}`（出现在官方示例 URL 里），其余 17 个是按描述推断的。重点确认：
  1. 设备类型宏是 `{{DEVICE_TYPE}}` 还是 `{{DEVICE_GROUP}}`
  2. `{{IDFA}}` / `{{GAID}}` 是否存在（官方表第 3 行描述列是空的）
  3. `{{CAMPAIGN_NAME}}` 是否真的不存在
  4. `rdt_cid` 是否为官方自动追加的参数名

---

## B 类 · 必须你的登录态（我进不去）

### B1. 快手 —— 「附件一」宏全表

- **入口**：登录 `https://ad.e.kuaishou.com` →【资产】→【转化】→【转化追踪】→ 新建转化 → 页面内的宏说明浮层
- **要给我什么**：
  1. 完整宏白名单（这是关键 —— 快手会校验，不在白名单的宏直接报错）
  2. 确认 `__Dname__` 的官方大小写（文档正文写的是混合大小写，与"必须全大写"规则冲突，疑似官方笔误）
  3. 是否有明文 `__IMEI__` / `__IDFA__`（我只见到 md5 形式的 `__IMEI2__` / `__IDFA2__`）
- **另**：磁力金牛（电商）`https://niu.e.kuaishou.com` 的宏与回传文档，我完全没拿到

### B2. 小红书 —— 账户三方监测可选参数下拉

- **入口**：登录聚光 `https://ad.xiaohongshu.com` →【工具】→【账户工具】→【账户三方监测】
- **要给我什么**：可选参数的**完整下拉列表**。我现在只有 7 个，官方 FAQ 说"只拼接 clickID 不支持其他宏"，需要你确认后台实际暴露多少个。
- **顺便看**：创意监测（新建创意时逐条添加）的可选参数是否和账户级不同
- **API 文档**：`https://ad.xiaohongshu.com/openApiDoc`（需登录的 SPA），里面有 `event_type` / `scene` 全量码表

### B3. UC / 超级汇川 —— 广告主侧宏表

- **入口**：登录 `https://e.uc.cn` →【工具中心】→【计划辅助】→【转化追踪】
- **要给我什么**：
  1. 落地页可用的宏 token 名 —— 官方说"多落地页优选时每个页面都追加上组/计划/创意 ID"，但**没给宏名**
  2. 确认 `{UCTRACKID}` 的创意层写法（多个第三方引用，官方原文我没抓到）
  3. **是否存在 `__XXX__` 双下划线宏** —— 不要按东风的宏推断，两者方向相反
- **另**：向 UC 商务索取《网页线索 API 技术对接文档》PDF（公网链接返回 0 字节，疑似需 Referer/登录态）

### B4. 知乎 —— 最新版转化追踪 PDF

- **入口**：登录 `https://xg.zhihu.com` →【工具中心】→【转化追踪管理】→ 新建转化 → 下载文档
- **为什么要做**：我手上的两份官方 PDF 最新是 **2020-06**，六年前的了
- **要给我什么**：
  1. 最新宏表（是否新增了 CAID / OAID_MD5 等）
  2. **`__VALUE__` vs `__EVENTVALUE__` 到底哪个对** —— 两份 PDF 自相矛盾：宏替换规则表写 `__VALUE__`，callback URL 模板和全部示例写 `value=__EVENTVALUE__`
  3. `zhs2s=1` 的现行要求是否还有效

### B5. 微博 —— 飞书联调手册（需飞书权限）

- 三份官方手册在飞书文档里，例：`https://a6ni3h1q1k.feishu.cn/docx/AdqxdT6pdoOVR8xea8Tc8VK6nad`
- **要给我什么**：
  1. `behavior` 行为码的**完整枚举**（我只抓到 6 个：1001/1007/2001/3002/3003/3004）
  2. 新版 `__XXX__` 双下划线宏的官方定义表（我只从 API 应答示例里逆向观测到，没有正式定义）
  3. 曝光监测的宏规范 —— 微博官方开发者文档目录里**根本没有这一章**

### B6. Reddit / LinkedIn 后台（与 A6/A7 同项，后台版更准）

- Reddit Ads Manager → 创建 post → Destination URL 旁的三方 tracker 宏表
- LinkedIn Campaign Manager → Campaign →【Tracking】→ URL tracking parameters 下拉

---

## 优先级建议

| 优先级 | 项 | 理由 |
|:--:|---|---|
| ✅ 完成 | ~~A1 巨量~~ · ~~A2 百度~~ · ~~A3 360搜索~~ | 2026-07-29 已按官方文档全量覆盖 |
| 🔴 P0 | B1 快手 | 主力平台，且有宏白名单会**直接报错** |

| 🟡 P1 | B2 小红书 · A3′ 360展示 | 参数少但当前配置最不确定 |
| 🟡 P1 | A4 Snapchat · A7 Reddit | 整块未确证，投产会静默失败（占位符原样出现在 URL 里） |
| 🟢 P2 | A5 Naver · A6 LinkedIn · B3 UC · B4 知乎 · B5 微博 | 补全取值字典与语法细节 |

---

## 给我的时候怎么给最省事

- **截图**直接贴进对话即可，我能读图
- **复制文本**最好（宏的大小写和下划线数量至关重要，截图 OCR 可能出错）
- 一次给一个平台也行，我按平台增量更新 `PLATFORMS` 数组

**如果 A 类你不想一个个开** —— 我可以用浏览器工具自己去渲染这些公开页（A1–A7 都不需要登录）。之前的研究线程试过但 Chrome 工具超时无响应，可以再试一次。B 类则确实需要你的登录态。
