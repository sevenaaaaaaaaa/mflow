# Ad Tracking URL Parameter Specification

> 投放链接追踪参数规范（SSOT）。所有新投放链接按本文档生成，旧链接逐步迁移。
> v2.2（2026-07-29）已按各平台官方文档逐条核实；百度 / 360 / 巨量 三家已拿到一手官方文档全量覆盖（360 含回传 API）。
> 取证细节见 `AD-TRACKING-PARAM-SPEC-v2-RESEARCH.md`，待补清单见 `PENDING-VERIFICATION-CHECKLIST.md`。
> URL 生成工具：`url-builder/index.html`

## 三层追踪架构

```
Layer 3: Platform Macros     → 平台原生动态宏，用于平台后台归因 + oCPM 回传
Layer 2: UTM Parameters      → 跨平台标准，用于 GA4/BigQuery/BI 统一分析
Layer 1: Internal Tracking   → 自建追踪体系（sourceId / el / sec），CRM/漏斗闭环
```

## 规范字段（Layer 1 · 3 个 + Layer 2 · 6 个 + Layer 3 · 逐平台）

### Layer 1 — Internal Tracking（3 个）

| 字段 | 含义 | 必填 | 示例值 |
|------|------|:--:|--------|
| `sourceId` | 内部 CRM/归因唯一标识 | ✅ | `910001` |
| `el` | 页面内元素（按钮/链接位置） | — | `cta_hero`, `pricing_btn`, `nav_signup`, `footer_trial` |
| `sec` | 页面区块 | — | `hero`, `features`, `pricing`, `testimonials`, `faq` |

### Layer 2 — UTM Parameters（6 个）

| 字段 | 含义 | 必填 | 示例值 |
|------|------|:--:|--------|
| `utm_source` | 流量来源平台 | ✅ | `google`, `meta`, `gdt` |
| `utm_medium` | 投放形式 | ✅ | `cpc`, `cpa`, `social` |
| `utm_campaign` | 活动/系列名称 | ✅ | `seedance-2.0-launch` |
| `utm_term` | 搜索词/定向条件 | — | `seedance_group` |
| `utm_content` | 素材变体/差异化 | — | `variant_a` |
| `utm_id` | 内部系统映射 ID | — | `910001` |

### Layer 3 — Platform Macros（选填，逐平台差异极大）

**核心字段**（CSV/JSON 批量模板暴露的高频字段）

| 字段 | 含义 |
|------|------|
| `campaign_id` | 广告系列/计划 ID |
| `adgroup_id` | 广告组/单元 ID |
| `ad_id` | 广告 ID |
| `creative_id` | 创意 ID（与 ad_id 分层的平台） |
| `asset_group_id` | 资产组 ID（PMax） |
| `project_id` / `promotion_id` | 巨量引擎升级版结构 |
| `keyword` / `keyword_id` | 关键词文本 / ID |
| `matchtype` | 匹配方式 |
| `network` | 流量网络类型 |
| `device` | 设备类型 |
| `placement` | 版位/投放位置 |
| `site_set` | 流量版位集合（国内平台） |
| `creative_type` | 创意格式/样式 |
| `click_id` / `callback` / `callback_param` | 点击标识与回传凭证 |

> **不要假设字段跨平台通用。** 全部 39 个平台的完整宏表（514 个宏，361 条官方备注）以 `url-builder/index.html` 的 `PLATFORMS` 数组为 SSOT；上传的 CSV/JSON 表头可用其中任意字段名。
>
> **素材层面回传（`creative/asset` 粒度）全行业只有 4 家提供**：巨量引擎 `__MID1__~__MID6__`（图片/标题/视频/试玩/落地页/下载页，粒度最细）· 腾讯广告 `__ELEMENT_INFO__` / `__CREATIVE_COMPONENTS_INFO__`（JSON，含 AIGC 衍生素材）· TikTok `__CID__` · Google `{param1}/{param2}` + PMax `{assetgroupid}`。**没有任何平台回传 `ad_format` 这类素材形态字段**（近似替代：巨量 `__CTYPE__`、腾讯 `__AD_TYPE__`）。

## UTM 枚举值

### utm_source

```yaml
广告平台:
  google        - Google Ads
  meta          - Meta Ads (Facebook + Instagram)
  bing          - Microsoft Ads
  tiktok        - TikTok Ads (海外)
  douyin        - 抖音广告 (国内)
  baidu         - 百度广告
  gdt           - 腾讯广点通
  kuaishou      - 快手广告
  xiaohongshu   - 小红书广告
  zhihu         - 知乎广告
  weibo         - 微博广告
  q360          - 360广告
  uc            - UC广告
  snapchat      - Snapchat
  pinterest     - Pinterest
  reddit        - Reddit
  linkedin      - LinkedIn
  yandex        - Yandex
  naver         - Naver
  x             - X/Twitter
  cg            - CG联盟
  aifu          - AiFu联盟

内容分发:
  zhihu_organic  - 知乎自然分发
  baijiahao      - 百家号
  toutiao        - 头条号
  csdn           - CSDN
  juejin         - 掘金
  segmentfault   - 思否
  devto          - DEV.to
  medium         - Medium
  github         - GitHub Discussions
  hashnode       - Hashnode
  hackernews     - Hacker News
  blogger        - Blogger
  x_organic      - X/Twitter 自然
  reddit_organic - Reddit 自然

自有渠道:
  email          - 邮件营销
  affiliate      - 网盟/联盟
  content        - 站内内容缺口填充
  direct         - 直投
```

### utm_medium

```yaml
付费投放:
  cpc          - 搜索广告（点击付费）
  cpm          - 展示广告（千次曝光付费）
  cpa          - 效果投放（按转化付费）
  social       - 信息流广告（社交媒体）
  video        - 视频广告
  shopping     - 购物广告 / PLA
  pmax         - Performance Max
  display      - 展示网络 / 程序化
  retargeting  - 再营销/重定向

内容分发:
  native       - 站外内容分发（完整文章 + 回链）
  syndication  - 站外内容同步（摘要 + 回链）

自有渠道:
  email        - 邮件
  push         - 推送通知
  blog         - 站内 Blog
```

### UTM 取值治理原则（2026-07-29 定）

**规范只收录通用标准枚举。** 生产环境中已存在的非标准取值，一律记为「历史遗留」：
不追溯改造已在投的链接，但**新建链接一律用标准值**，历史值在统计口径里单独标记、后续逐步停用。

| 生产历史值 | 标准值 | 处置 |
|---|---|---|
| `utm_source=googleads_int` | `utm_source=google` | 历史遗留，新链接用 `google` |
| `utm_medium=paid_social` | `utm_medium=social` | 历史遗留，新链接用 `social` |
| `utm_medium=cpc`（广点通信息流） | `utm_medium=social` | 历史遗留，新链接按实际形式取值 |
| `utm_content={QueryString}`（Bing 搜索词） | `utm_content` 留给素材变体 | 历史遗留，搜索词建议另开 `query=` 参数 |

> BI 侧建议：建一张 `utm_source_alias` 映射表把历史值归一到标准值，比改链接便宜，也不影响历史数据可比性。

### utm_campaign 命名规范

格式: `{product}-{campaign_type}[-{geo}][-{variant}]`

- 全小写 kebab-case
- 必须包含产品/主题名
- 不可含下划线（仅连字符分隔）

### utm_term 命名规范

- 搜索广告: `{keyword_group}_group`（snake_case）
- 社交广告: `{interest}_interest`、`{audience}_lookalike`
- 再营销: `{segment}_{days}d`

### utm_content 命名规范

- 素材变体: `variant_a`, `variant_b`, `control`
- 素材格式: `image_16x9`, `video_9x16`, `carousel_3card`
- CTA 类型: `signup_cta`, `trial_cta`, `demo_cta`

## el / sec 预设值

```yaml
el (元素):
  - cta_hero          # Hero 区主 CTA
  - cta_pricing       # 定价表 CTA
  - cta_footer        # 页面底部 CTA
  - cta_sticky        # 悬浮导航 CTA
  - banner_top        # 顶部横幅
  - nav_signup        # 导航栏注册按钮
  - nav_login         # 导航栏登录按钮
  - card_01 ~ card_10 # 卡片位
  - link_footer       # 页脚文字链接
  - link_inline       # 正文内链

sec (区块):
  - hero
  - features
  - pricing
  - testimonials
  - faq
  - comparison
  - workflow
  - cta_section
  - footer
  - sidebar
  - nav
```

## 39 平台参数映射总表

> **v2（2026-07-28）已按官方文档逐条核实。** 完整来源链接、逐平台全量宏表、以及「判定为不存在/编造的宏」对照表见 `AD-TRACKING-PARAM-SPEC-v2-RESEARCH.md`。
> 工具内每个平台都带官方文档链接与 ⚠️ 警告横幅，宏后的 ⓘ 悬停可看官方备注。

### 海外 — Google（7 个条目）

| 平台 | code | Click ID | campaign_id | adgroup / asset_group | ad_id | 关键约束 |
|------|------|---------|-------------|----------------------|-------|---------|
| Google Search | `google` | `gclid` | `{campaignid}` | `{adgroupid}` | `{creative}` | AI Max 下 `{keyword}` 空、`{matchtype}=a`、`{targetid}=kwl-*` |
| Google PMax | `google_pmax` | `gclid`(Limited) | `{campaignid}` | `{assetgroupid}` ✅ | — | `{ifsearch:}`/`{ifcontent:}` 恒 false；`{network}` 恒 `x`；`{keyword}` 空 |
| Google Display | `google_display` | `gclid` | `{campaignid}` | `{adgroupid}` | `{creative}` | `{devicemodel}` 仅此可用；`{feeditemid}`/`{extensionid}` 不可用 |
| Google Demand Gen | `google_demandgen` | `gclid` | `{campaignid}` | `{adgroupid}` | `{creative}` | `{network}` 完全不返回；`{placement}`/`{target}`/`{keyword}`/`{targetid}` 不支持 |
| Google App Campaigns | `google_app` | `gclid` | `{campaignid}` | `{adgroupid}` | `{creative}` | ⚠️ 不支持 tracking template 挂三方 tracker；需 Confirmed Installs |
| Google Shopping | `google_shopping` | `gclid` | `{campaignid}` | `{adgroupid}` | `{creative}` | `{store_code}` 60 字符上限 |
| Google Hotel/Travel | `google_hotel` | `gclid` | `{campaignid}` | `{adgroupid}` | — | `{targetid}` 与 Hotel tROAS 不兼容 |

**Click ID 出现时机**：`gclid`（auto-tagging）· `wbraid`（iOS app→web）· `gbraid`（web→iOS app，**大小写敏感不可转换，仅 Search/Shopping/Display/PMax**）· `dclid` **不属 Google Ads**（DV360/CM360）。
**自定义参数**：`{_name}`，**最多 8 个**，除 account 外任意层级，name ≤16 字母数字，value ≤250 且可嵌套 ValueTrack。

### 海外 — Microsoft（4 个条目）

| 平台 | code | Click ID | campaign_id | adgroup / asset_group | ad_id | 关键约束 |
|------|------|---------|-------------|----------------------|-------|---------|
| Bing Ads | `bing` | `msclkid` | `{CampaignId}` | `{AdGroupId}` | `{AdId}` | 宏名大小写不敏感；tracking template ≤2048 字符 |
| Bing PMax | `bing_pmax` | `msclkid` | `{CampaignId}` | `{AdGroupId}` = asset group | — | ⚠️ 官方明示**不支持** asset group 宏 |
| Bing Shopping | `bing_shopping` | `msclkid` | `{CampaignId}` | `{AdGroupId}` | — | 用 `{CriterionId}`，无 `{ProductPartitionId}` |
| Bing Lodging | `bing_lodging` | `msclkid` | `{CampaignId}` | `{AdGroupId}` | — | `{property_id}` 而非 `{hotel_id}` |

**自定义参数（重点纠正）**：自命名 `{_yourkey}` —— **不存在 `{Custom1}~{Custom8}`**。Key ≤16 字节 / Value ≤250 字节；campaign / ad group / criterion / ad **各 8 个**，扩展默认 3 个。Microsoft **不校验**参数是否存在，不存在时占位符原样输出。

### 海外 — 社交（7 个条目）

| 平台 | code | Click ID | campaign_id | adgroup_id | ad / creative | 关键约束 |
|------|------|---------|-------------|-----------|--------------|---------|
| Meta (FB+IG) | `meta` | `fbclid`(官方未取证) | `{{campaign.id}}` | `{{adset.id}}` | `{{ad.id}}` | ⚠️ **官方仅 8 个宏，无任何创意/素材层宏**；URL parameters 字段覆盖 Website URL 同名参数 |
| TikTok | `tiktok` | `ttclid` | `__CAMPAIGN_ID__` | `__AID__` | `__CID__`(creative) | ⚠️ **AID=Ad Group、CID=Creative**；click id 宏是单下划线 `_CLICKID_` |
| Snapchat | `snapchat` | `ScCid` | `{{campaign.id}}` | `{{adSet.id}}` | `{{ad.id}}` | ⚠️ **全部未取证**（官方为 Salesforce JS 站），投产前须在后台核对 |
| Pinterest | `pinterest` | `_epik` cookie | `{campaignid}` | `{adgroupid}` | `{creative_id}` | ⚠️ **单花括号**；`{keyword}` 官方明确不支持 |
| Reddit | `reddit` | `rdt_cid` | `{{CAMPAIGN_ID}}` | `{{ADGROUP_ID}}` | `{{AD_ID}}` | 大小写敏感；官方表**无 CAMPAIGN_NAME** |
| X / Twitter | `x` | `twclid` | — | — | — | ⚠️ **完全没有 URL 宏体系**，只能手写静态 UTM |
| LinkedIn | `linkedin` | `li_fat_id` | `CAMPAIGN_ID` | `CAMPAIGN_GROUP_ID` | `CREATIVE_ID` | ⚠️ **UPPER_SNAKE_CASE**；只能设在 Campaign 层；不支持 Conversation/Message Ads |

### 海外 — 区域（2 个条目）

| 平台 | code | Click ID | campaign_id | adgroup_id | ad_id | 关键约束 |
|------|------|---------|-------------|-----------|-------|---------|
| Yandex Direct | `yandex` | `yclid` | `{campaign_id}` | `{gbid}` | `{ad_id}` / `{banner_id}` | ⚠️ URL >4096 字节时只保留 yclid + openstat；`{match_type}` 仅 `rm`/`syn` |
| Naver Search Ads | `naver` | 无 | `n_campaign_type` | `n_ad_group` | `n_ad` | ⚠️ **不是宏，是开关**，平台自动追加 10~12 个 `n_*` 真实 query key |

### 国内（17 个条目）

| 平台 | code | Click ID | campaign / 计划 | adgroup / 单元 | creative / 创意 | 关键约束 |
|------|------|---------|----------------|---------------|----------------|---------|
| 百度搜索（落地页通配符） | `baidu` | `bd_vid` | `{planid}` | `{unitid}` | `{creative}` | `{}` 小写严格区分大小写；显示 URL 不支持；此体系内无 `{os}/{age}/{gender}` |
| 百度应用API监测地址 ✅ | `baidu_app_api` | `__CLICK_ID__` | `__PLAN_ID__` | `__UNIT_ID__` | `__IDEA_ID__` | ⚠️ 搜索+信息流**通用**；`__XXX__` 与 `{{XXX}}` 两种写法等价；`__SIGN__` 必须最后；宏名与参数名错位（`__IMEI__`→imei_md5） |
| 360 搜索推广 ✅ | `q360` | `qhclickid` **16位**(自动) | `{planid}` | `{groupid}` | `{creativeid}` | 关键词宏是 `{keywordid}`；自动拼接位置有 4 条规则（见回传章节） |
| 360 展示广告 ✅ | `q360_display` | **`sourceid`** **12位**(自动) 🔴 | — | — | `{creativeid}` / `{bannerid}` | 🔴 落地页参数名 `sourceid` **与本规范 Layer 1 内部渠道号同名**，展示广告必须改名；回传字段名却是 `qhclickid` |
| 360 移动推广 ✅ | `q360_mobile` | `impression_id` **16/19位** | — | — | — | ⚠️ **不自动拼接**，须手写 `__impression_id__`；小写双下划线，与搜索的花括号是两套语法 |
| 360 搜索点击下发 ✅ | `q360_feedback` | `__UniqueID__` | `__planid__` | `__groupid__` | `__creativeid__` | 适用 app内/pc软件内转化。宏**大小写混用**；✅ 有明文 `__keyword__`（关键词词面） |
| 腾讯广告（点击监测） | `gdt` | `gdt_vid` / `qz_gdt` | `__CAMPAIGN_ID__`(旧版) | `__ADGROUP_ID__` | `__DYNAMIC_CREATIVE_ID__` | ⚠️ **宏不在落地页上**，只用于监测链接；落地页只自动带 gdt_vid/qz_gdt |
| 腾讯广告（曝光监测） | `gdt_impression` | `gdt_vid` | — | `__ADGROUP_ID__` | — | 用 `__IMPRESSION_*__` 替换 `__CLICK_*__` |
| 巨量引擎 / 抖音 ✅ | `douyin` | `clickid`(21天) | `__PROJECT_ID__` | `__PROMOTION_ID__` | `__MID1__~__MID6__` | ⚠️ 升级版用 PROJECT/PROMOTION，官方建议**忽略**原版的 AID/CID/CAMPAIGN_ID/CTYPE；`__TRACK_ID__` 串联落地页与监测链接；域名须企业备案 |
| 快手 DSP | `kuaishou` | `callback` | `__DID__` | `__AID__` | `__CID__` | ⚠️ **有宏白名单校验**，非法宏直接报错；`__ACCOUNTID__` 无中间下划线 |
| 快手品牌（MMA） | `kuaishou_brand` | 无 | — | — | — | 独立宏池：`__OS__ __UA__ __IP__ __TS__ __GEO__ __BDID__` |
| 知乎广告 | `zhihu` | 无 | `__CAMPAIGN__` | — | `__CREATIVE__` | ⚠️ **全部 `__XXX__`，无花括号语法**；落地页须 `cb=__CALLBACK__` + `zhs2s=1` |
| 超级汇川 / UC | `uc` | `uctrackid`(自动) | — | — | `{UCTRACKID}` | ⚠️ 广告主侧无公开宏表；转化与 5 天内点击拼接 |
| 阿里妈妈东风 | `uc_dongfeng` | 无 | — | — | — | ⚠️ **媒体接入侧**，方向与汇川相反；点击链接 ≤500 字符 |
| 微博（点击监测） | `weibo` | `mark_id` | `{CAMPAIGN_ID}` | `{ad_id}` | `{creative_id}` | ⚠️ 大小写混用；mark_id **只允许 urlencode 一次** |
| 微博（APP 激活） | `weibo_app` | `IMP` | — | — | — | `{IMP}` 必须原样带回；激活+后续行为需回传两次 |
| 小红书聚光 | `xiaohongshu` | `click_id`(自动) | — | — | — | ⚠️ **官方仅 7 个宏**，只支持账户/创意两级；回传 >1h 判超时 |

### 网盟（2 个条目 · 通用模板待核实）

| 平台 | code | 说明 |
|------|------|------|
| CG联盟 | `cg` | ⚠️ 中文公开语料无索引，未找到官方文档。占位为 TUNE/HasOffers 系通用参数 |
| AiFu联盟 | `aifu` | ⚠️ 同上。占位为 Affise 系通用参数；⚠️ Affise postback 无 clickid 宏，须用 `{sub1}`–`{sub8}` 承载 |

拿到联盟后台后确认 3 件事即可覆盖 90% 对接：① click id 参数名与括号形式；② postback 里 click id 用哪个字段回（Affise 系 = sub1，TUNE 系 = transaction_id）；③ 自由 sub 位数量与字符上限。

## 语法风格对照

| 风格 | 语法 | 示例 | 平台 |
|------|------|------|------|
| Google Curly (lower) | `{lowercase}` | `{campaignid}` | Google 全家桶、百度搜索、360、Pinterest |
| Google Curly (Pascal) | `{PascalCase}` | `{CampaignId}` | Microsoft 全家桶 |
| Google Curly (snake) | `{snake_case}` | `{campaign_id}` | Yandex Direct |
| Meta Mustache | `{{dot.path}}` | `{{campaign.id}}` | Meta、Snapchat |
| Mustache UPPER | `{{UPPER_SNAKE}}` | `{{CAMPAIGN_ID}}` | Reddit、LinkedIn |
| Baidu Dual | `__X__` 与 `{{X}}` 等价 | `__PLAN_ID__` / `{{PLAN_ID}}` | 百度应用API监测地址（搜索+信息流） |
| Q360 Curly | `{lowercase}` | `{planid}` | 360 搜索推广落地页、360 展示广告 |
| Q360 Macro | `__lowercase__` | `__impression_id__` | 360 移动推广落地页 |
| Q360 Mixed | `__混合大小写__` | `__UniqueID__` / `__IP__` / `__planid__` | 360 搜索点击下发 feedback_url |
| ByteDance Macro | `__UPPER__` | `__CAMPAIGN_ID__` | TikTok、巨量/抖音、腾讯、快手、知乎、小红书、东风 |
| Weibo Curly | `{混合大小写}` | `{ad_id}` / `{AD_NAME}` | 微博 |
| Naver Auto | `n_field`（平台自动追加） | `n_campaign_type` | Naver |
| Static Only | 无动态宏 | — | X / Twitter |

**易错点速查**
- Pinterest 是**单**花括号，不是双花括号
- LinkedIn 是 UPPER_SNAKE_CASE，camelCase 的 `{{campaignGroupId}}` 不存在
- TikTok `__AID__` = Ad Group；巨量 `__AID__` = 广告计划（旧版第 3 层）—— **跨平台复用模板会串层级**
- 百度搜索 `{}` 小写 vs 百度信息流 `{{}}` 大写，且联调期两者都要临时改成 `__X__`
- 知乎完全不用花括号
- 微博 `{ad_id}` 小写但 `{AD_NAME}` 大写
- **360 一家就有三套语法**：搜索落地页 `{planid}` 花括号 · 移动推广 `__impression_id__` 小写双下划线 · 点击下发 `__UniqueID__` 混合大小写
- 360 三条产品线的 click id 参数名/位数/回传字段名全不同，**传错会被当作无效数据直接丢弃**

## URL 结构规范

```
https://{domain}/{page_path}?sourceId={id}&el={el}&sec={sec}&utm_source={src}&utm_medium={med}&utm_campaign={camp}[&utm_term={term}][&utm_content={content}][&{macro1}={val1}&{macro2}={val2}...]
```

- Layer 1（sourceId/el/sec）在前
- Layer 2（UTM）居中
- Layer 3（平台宏）在后
- 参数按字母序排列（同层内）

## 常见场景 URL 示例

> 全部示例由 `url-builder/index.html` v2 实际生成（37 平台 JSDOM 冒烟测试通过）。
> 注意 `utm_campaign` 必须是纯 kebab-case，`seedance-2.0` 会被校验拒绝，应写 `seedance-2-0`。

### Google Ads 搜索广告

```
https://lovart.ai/tools/seedance?sourceId=910001&el=cta_primary&sec=hero-split&utm_source=google&utm_medium=cpc&utm_campaign=seedance-2-0&utm_term=seedance_group&utm_content=variant_a&campaign_id={campaignid}&adgroup_id={adgroupid}&ad_id={creative}&keyword={keyword}&device={device}
```

### Meta 信息流广告

```
https://lovart.ai/tools/seedance?sourceId=910001&el=cta_primary&sec=hero-split&utm_source=meta&utm_medium=social&utm_campaign=seedance-2-0&utm_content=variant_b&campaign_id={{campaign.id}}&adgroup_id={{adset.id}}&ad_id={{ad.id}}&placement={{placement}}&site_source_name={{site_source_name}}
```

### 巨量引擎 / 抖音（含素材层）

```
https://lovart.ai/tools/seedance?sourceId=910003&el=cta_primary&sec=hero-split&utm_source=douyin&utm_medium=social&utm_campaign=seedance-2-0&project_id=__PROJECT_ID__&promotion_id=__PROMOTION_ID__&creative_id=__CID__&creative_type=__CTYPE__&site_set=__CSITE__&callback_param=__CALLBACK_PARAM__&material_image_id=__MID1__&material_video_id=__MID3__
```

### 腾讯广告 / 广点通 —— ⚠️ 架构不同，勿照搬其他平台

腾讯的宏**不在落地页 URL 上**。落地页由腾讯自动追加 `gdt_vid`（微信流量）或 `qz_gdt`（非微信流量），**先取 gdt_vid，取不到再取 qz_gdt**：

```
落地页（你只需保留自己的 Layer 1/2 参数，腾讯会自动追加 gdt_vid）
https://lovart.ai/tools/seedance?sourceId=910002&el=cta_primary&sec=hero-split&utm_source=gdt&utm_medium=cpa&utm_campaign=seedance-2-0
  → 实际到达：...&gdt_vid=wx07ptidwiwn5fde
```

宏用于**点击监测链接**（腾讯服务端 GET 你的服务器）：

```
https://track.lovart.ai/gdt/click?click_id=__CLICK_ID__&click_time=__CLICK_TIME__&account_id=__ACCOUNT_ID__&callback=__CALLBACK__&adgroup_id=__ADGROUP_ID__&element_info=__ELEMENT_INFO__
```

网页/小程序载体的必填宏只有 4 个：`__ACCOUNT_ID__` `__CLICK_ID__` `__CLICK_TIME__` `__CALLBACK__`。

### 小红书聚光 —— 平台只给 clickID

```
https://lovart.ai/tools/seedance?sourceId=910004&el=cta_primary&sec=hero-split&utm_source=xiaohongshu&utm_medium=social&utm_campaign=seedance-2-0&click_id=__CLICK_ID__&placement=__PLACEMENT__
```

域名需提前加白（销售提交邮件 + OA 申请）；`__RED_ID__` / `__CAID__` / `__CAID_MD5__` 为敏感参数必须删除；C2S 场景须去掉 `__CONTENT__`。

### X / Twitter —— 无动态宏，只能静态 UTM

```
https://lovart.ai/tools/seedance?sourceId=910005&el=cta_primary&sec=hero-split&utm_source=x&utm_medium=social&utm_campaign=seedance-2-0&utm_content=variant_a
```

`twclid` 由 X Pixel 自动从 URL 或首方 cookie 读取，无需手写。

### 内容分发（知乎自然分发）

```
https://lovart.ai/blog/ai-video-tools?sourceId=0&el=link_inline&utm_source=zhihu_organic&utm_medium=syndication&utm_campaign=offsite-ai-video-tools
```

## 转化回传（Callback）规范 —— 国内平台

> 落地页/监测链接的宏只解决「点击是谁」；回传解决「转化算给谁」。两者必须配套，本节按官方文档核实。

### 百度（应用 API）

| 项 | 值 |
|---|---|
| 端点 | `http://ocpc.baidu.com/ocpcapi/cb/actionCb` |
| 触发方式 | 从监测请求里取 `callback_url`（v1）或自行拼 `ext_info`（v2） |
| 必替换 | `{{ATYPE}}` → 转化类型；`{{AVALUE}}` → 转化金额 |
| 签名 | `sign = md5(替换后的完整回调URL（不含 &sign=） + akey)`，标准 32 位小写，**`&sign=` 必须加在最后** |
| akey | 业务端创建转化时自动生成，同一账号下唯一，在百度投放后台获取 |
| 成功响应 | `{"error_code":"0"}` |

**`a_type` 全量枚举（官方）**：`activate` 激活 · `register` 注册 · `orders` 付费成单 · `retain_1day` 次日留存 · `retain_2day`~`retain_7day` · `retain_14day` · `user_defined` 客户自定义 · `ec_buy` 商品下单成功 · `deep_page_access` 关键页面浏览 · `credit_granting` 授信 · `deeplink` / `feed_deeplink` 应用调起 · `pay_to_read` 付费阅读 · `enter_bookstore_read` 进入书城阅读 · `add_to_desktop` 添加至桌面 · `log_in` 登录 · `order_submit_success` 订单提交成功 · `pay_to_watch` 付费观剧 · `key_action` 关键行为 · `apply` 申请 · `payout` 放款 · `follow_success` 微信加粉成功

**`join_type` 必填**（告诉百度你是靠什么归上的，用于优化投放）：`imei` · `oaid` · `android_id` · `ip`（IP + ua/os_version/model）· `idfa` · `caid` · `mac` · `paid`（灰度）· `bt_ut`（灰度）· **`bd_vid`**

**其他回传字段**：`a_value`（付费金额，**单位分**，12.3 元 → `1230`；无金额填 `0`）· `a_time`（**10 位秒级** unix 时间戳，不可为未来时间）

**错误码**：`100` 签名错误 · `101` ext_info 为空/被截断/未 urlencode · `102` ATYPE 或 AVALUE 值错误 · `103` akey 不符合要求 · `104` searchid 验证失败 · `105` join_type 缺失或不合法 · `110` a_time 格式错误或为未来时间

**BD_VID 注入归因（Android，强烈推荐）**
- 原理：把 `bd_vid` 动态注入 APK 的 **V2 签名区**（签名 ID `0x710987bd`），用户装完 App 后读签名块即可 100% 准确归因
- 前置条件：① APK 支持 V2 及以上签名；② 推广包**托管在百度应用中心**（支持前卡应用下载 + 基木鱼页面应用下载）；③ 邮件申请白名单 → `zhzz@baidu.com;cvdb@baidu.com`，标题《【XX运营单位-Android应用-申请BD_VID注入归因能力】》，可按**主体**或**账户 ID** 粒度开通
- 客户端：拷贝 `com.baidu.appwalle` 包，调 `ChannelReader.get(context)`，返回 `{"bd_vid":"..."}`（内容经 Base64 编码，需替换占位符后解码）
- 回传：`&join_type=bd_vid&bd_vid=xxxx`
- ⚠️ 检查签名 ID `0x710987bd` 是否与你自己的签名块冲突
- 官方归因优先级：**BD_VID > OAID > IMEI > IP+MODEL > IP+OS_VERSION**

**iOS 归因优先级（官方 v1.9 / 2026-06）**：**IDFA > CAID > 模糊归因**
- CAID 两套并存：`vendor=0` 百度开源规则、`vendor=1` 中广协。归因建议**只用 CAID 的第 1+2 部分匹配，不用第 3 部分**（第 3 部分含用户名/运营商/国家码/系统启动时间，易变）
- 中广协 2026 新算法 `20260506` 已于 6/30 正式切换，`20250325` 作保底；**`20230330` 版本不再返回**
- 深度转化（次留、付费）建议：先用 CAID 或模糊归因把「激活」与「点击」归因，再用 **IDFV** 把深度转化与激活关联
- 模糊归因方案二 = IP + UA(系统版本) + 机型(`{{DEVICE_INFO}}`) 三者同时匹配，建议窗口期**点击→激活 24h 内**

### 360 点睛（两条并列链路，共 4 个产品线）

**⚠️ 第一件要知道的事：三个产品线的 click id 参数名、位数、上报字段名全都不一样，且不可混用**（官方 FAQ 明确「传错会被当作无效数据丢弃」）。

| 产品线 | `data_industry` | 落地页参数名 | 位数 | 谁来加 | 回传字段名 |
|---|---|---|:--:|---|---|
| PC 搜索推广 | `ocpc_ps_convert` | `qhclickid` | 16 | 平台自动 | `qhclickid` |
| 移动搜索 | `ocpc_ms_convert` | `qhclickid` | 16 | 平台自动 | `qhclickid` |
| 展示广告 | `ocpc_zs_convert` | **`sourceid`** 🔴 | 12 | 平台自动 | **`qhclickid`** |
| 移动推广 | `ocpc_web_convert` | `impression_id` | 16 或 19 | **广告主手动加宏** | `impression_id` |

> 🔴 **展示广告的 `sourceid` 与本规范 Layer 1 的内部渠道号同名**，详见 `PRODUCTION-LINK-AUDIT.md`。

**搜索推广落地页自动拼接位置规则**（URL 设计时要考虑）

| URL 中包含 | 追加位置及内容 |
|---|---|
| 有 `?` 无 `#` | 直接在末尾追加 `&qhclickid=...` |
| 有 `?` 有 `#` | 在最后一个 `?` 之后、第一个 `#` 之前追加 `&qhclickid=...` |
| 无 `?` 有 `#` | 在第一个 `#` 之前追加 `?qhclickid=...` |
| 无 `?` 无 `#` | 直接在末尾追加 `?qhclickid=...` |

#### 链路一：网页转化数据 API（适用所有转化类型）

```
POST https://convert.dop.360.cn/uploadWebConvert
HEADER:
  App-Key:  $Key
  App-Sign: md5($Secret . POSTDATA)      ← Secret 与 POSTDATA 直接连接后做 32 位小写 md5
  Content-Type: application/json;charset=utf-8
BODY:
{"data":{"request_time":1545033743,"data_industry":"ocpc_ps_convert","data_detail":{
  "qhclickid":"9356596331006111412","trans_id":"202cb962...","event":"SUBMIT",
  "event_time":1545033743,"event_param":{"value":2345}}}}
```

成功返回 `{"errno":0,"error":"Success"}`

| 字段 | 必填 | 说明 |
|---|:--:|---|
| `data_industry` | ✅ | 见上表四选一 |
| `qhclickid` | ✅ | ps / ms / zs 三条产品线必填 |
| `impression_id` | ✅ | 仅 `ocpc_web_convert`（移动推广）必填，其他产品线不需要 |
| `jzqs` | ✅ | 仅展示广告必填，展示广告主 ID |
| `event` | ✅ | 转化类型枚举，见下 |
| `trans_id` | 条件必填 | `event=SUBMIT` 或 `ORDER` 时必填；用于**去重**（表单内容或订单 ID 做 md5） |
| `event_time` / `request_time` | — | UTC 秒级 |
| `data_source` | 条件必填 | 第三方咨询工具上报时必填，客户自报时不填 |

**`event_param` 子字段**

| 键 | 含义 | 适用 |
|---|---|---|
| `value` | 订单金额，**单位分** | `event` = ORDER / LOW_PAY / PAY_SUCCESS / PAY |
| `score` | 价值分，大于 0 的正整数 | ps / ms / zs 全部转化类型 |
| `outeruserid` | 用户唯一标识 | ps / ms / zs 全部转化类型 |
| `bname` | 业务名称 | 仅 zs |
| `urtime` | 用户注册时间，10 位秒级 | zs / ps，且 event = ORDER / COUSTOMIZE |
| `spare` | **1001 = 无效转化**（空号、乱码、骚扰、答非所问）· **1002 = 非无效转化** | ps / ms / zs 全部转化类型 |

> 二次回传规则：确认后的二次回传，`qhclickid` / `trans_id` / `event` 必须与第一次一致；若确认后产生了**新类型**转化，请启用新的 `event`。

#### 链路二：搜索点击下发（feedback_url + callback_url，适用 app 内 / pc 软件内转化）

**feedback_url**（你提供地址，360 GET 你）—— 宏为 `__xxx__`，**大小写混用，必须逐字照抄**：

```
http://your.com/clickdata?UniqueID=__UniqueID__&clicktime=__clicktime__&IP=__IP__&UA=__UA__
  &oaid_md5=__oaid_md5__&imei_md5=__imei_md5__&IDFA=__IDFA__&callback_url=__callback_url__
```

必填：`__UniqueID__`（驼峰）· `__clicktime__` · `__IP__`（大写）· `__UA__`（大写）· `__callback_url__`；移动搜索另必填 `__oaid_md5__` · `__imei_md5__` · `__IDFA__`（大写）
选填：`__userid__` · `__planid__` · `__groupid__` · `__creativeid__` · **`__keyword__`（关键词词面）** · `__keywordid__`

> ✅ **修正**：此前根据旧资料判断「360 出于安全不明文提供关键词」是**错的** —— feedback_url 链路确实下发明文 `keyword`。
> 兜底规则：`clicktime` 未被替换时取收到点击数据的时间；`IP` 未被替换时取收到的客户端 IP。

**callback_url**（360 提供，你 GET 它）

```
GET https://convert.dop.360.cn/ms/third?qhclickid=abcde&event=__event__
    &trans_id=__trans_id__&value=__value__&event_time=__event_time__
    &request_time=__request_time__&qid=123&sendVer=10
```

- 只需替换 `event`（`trans_id` 在 event=ORDER/SUBMIT 时必填），其余字段原样不动
- 官方特别提示：需把参数值 **`__event__` 整个替换**为枚举值（**连双下划线一起替换掉**）
- `qhclickid` / `qid` / `sendVer` 无需广告主替换
- `value` 单位**分**，适用 ORDER / LOW_PAY / PAY_SUCCESS / PAY

#### `event` 转化类型枚举（约 50 个，× 表示该产品线不支持）

**四条产品线都支持**：`SUBMIT` 表单提交 · `CALL` 有效电话拨打 · `ADVISORY` 一句话咨询 · `SITEDOWNLOAD` 下载按钮点击

**移动推广仅支持上面 4 个**，以下全部为 ×；PC搜索 / 移动搜索 / 展示广告支持：
`SUBMIT_BUTTON` · `ADVISORY_BUTTON` · `CALL_BUTTON` · `SHOP_BUTTON` · `CART_BUTTON`（展示 ×）· `ORDER` · `REGISTERED` · `ROLE_CREAT` · `SITE_VISIT_DEPTH` 深度页面访问(≥3) · `COUSTOMIZE`（注意官方拼写少一个 S）· `MIDDLE_PAGE` · `REGISTER_BUTTON` · `BROWSE_DEPTH` · `BROWSETIME` · `SCAN_BUTTON` · `ADVISORY_DEPTH` 三句话咨询(≥3条) · `LOW_PAY` · `ADD_FANS_WX` · `PAY` · `SCAN_CODE` · `APPLET_STARTUP` · `LOGIN` · `ADD_TO_CART` · `VPPV` · `INTENTIONAL` · `REAL_NAME` · `RETENTION` 次留 · `PLACE_ORDER` · `EFFECTIVE_ADVISORY` · `ORDER_VALIDITY`（展示 ×）· `ACTIVATION` · `DETAILS_PAGE_ARRIVED` · `PAY_SUCCESS` · `CREDIT` · `WX_BUTTON_C` · `CONCEM` 关注（注意官方拼写不是 CONCERN）· `LEAVE_CONTACT` · `RELEASE` · `TRY_TO_PLAY` · `SUBMIT_RESUME` · `ENTERPRISE_CERTIFICATION` · `VISIT_CLINIC` · `TRIAL`

**仅展示广告**：`APPLET_PAY` 小程序内付费 · `APPLET_ROLE_CREAT` 小程序内创角 · `TRIAL_LESSON_PERFORM` 试听到课 · `TRIAL_LESSON_COMPLETE` 试听完课

#### 错误码与运维

| errno | 含义 | 排查 |
|:--:|---|---|
| 1 | `app_key` 未验证 | 字段格式、有无空格、key 与账号是否一致 |
| 2 | `app_sign` 未验证 | 加密方式必须是 `md5(secret + POSTDATA)`，32 位小写 |
| 3 | `data` 未验证 | 上报 data 格式与文档不一致 |

- **不支持批量上报**，官方建议实时逐条（否则优化师看到的实时成本没有意义）
- 回传失败**同一自然天内可重复回传**
- 同主体多账户可共享对接，**不建议超过 30 个**；搜索与移动推广自动共享，**PC 展示需发邮件 g-FAQ-PC@360.cn 申请**
- 技术支持：搜索 g-faq-search-ocpc@360.cn · 展示 g-FAQ-PC@360.cn · 移动 g-FAQ-Mobile@360.cn
- 验证方式：返回 Success 代表链路通；建议观察 1~2 个工作日，对比系统转化数与实际回传数

### 巨量引擎

| 项 | 旧「转化追踪」（将下线） | 新「事件管理」（建议） |
|---|---|---|
| 端点 | `https://ad.oceanengine.com/track/activate/` | `https://analytics.oceanengine.com/api/v2/conversion` |
| 方法 | GET | POST JSON |
| 凭证来源 | `__CALLBACK_PARAM__` 实际值 | 落地页 query 的 `clickid` |
| 金额 | `props={"pay_amount":"1000"}`，**单位分** | body 内 |

`__CALLBACK_URL__` 宏会直接下发拼好的回传 URL，可省去手工拼接。

### 快手

`GET https://ad.partner.gifshow.com/track/activate?event_type=1&event_time=<13位毫秒>&callback=<原值>`，返回 `{"result":1}` 为成功。必须用下发的**完整原值**，否则报 `callbackinfo decoded failure`。

### 腾讯广告

2025 Q3 起全量强制 `https://api.e.qq.com/v3.0/user_actions/add`（鉴权 Header：`access-token` 中划线 / `timestamp` / `nonce`），旧端点 `http://tracking.e.qq.com/conv` 逐步下线。去重键 `outer_action_id`。

### 小红书

`POST https://adapi.xiaohongshu.com/api/open/conversion`。⚠️ **回传时间超过 1 小时即判「回传超时」**。

### 知乎

`https://sugar.zhihu.com/plutus_adreaper_callback?si=…&cid=…&event=__EVENTTYPE__&value=__EVENTVALUE__&ts=__TIMESTAMP__`（`ts` 秒级）。

### 微博

落地页/小程序 `/v4/track/activate`（免鉴权）或 `/v3/track/activate`（Bearer Token）；APP 激活 `https://appmonitor.biz.weibo.com/sdkserver/active`。**深浅层强制绑定**：回传 2001 必须同时回 1007，回传 3003 必须同时回 3002。

## 变更记录

### v2.2 — 2026-07-29（360 回传 API 官方文档，360 拆为 4 个产品线）

用户提供《360点睛-转化数据回传API对接文档 2025-07》。平台 37 → **39**，宏 499 → **514**，备注 344 → **361**。

**🔴🔴 最重要的一条**：360 展示广告落地页自动拼接的参数名是 **`sourceid`**（12 位），与本规范 Layer 1 的内部渠道号**完全同名**。生产链接 `?sourceid=006559&planid={planid}...` 若投的是展示广告，会出现两个 sourceid —— 详见 `PRODUCTION-LINK-AUDIT.md` P0-0。

**360 拆成 4 个条目**（一家平台三套语法）
- `q360` 搜索推广落地页 —— `{planid}` 花括号；`qhclickid` **16 位**自动拼接，含 4 条拼接位置规则
- `q360_display` 展示广告 —— `sourceid` **12 位**自动拼接 🔴；回传字段名却是 `qhclickid`；`jzqs` 必填
- `q360_mobile` 移动推广 —— **不自动拼接**，须手写 `__impression_id__`（小写双下划线），16/19 位
- `q360_feedback` 搜索点击下发 —— 14 个宏，**大小写混用**（`__UniqueID__` 驼峰 / `__IP__` `__UA__` `__IDFA__` 大写 / 其余小写）

**推翻此前判断**
- ✅ **360 有明文关键词**：`q360_feedback` 的 `__keyword__` 就是「关键词词面」。此前依据 2015 年旧资料写的「360 出于安全不明文提供关键词」是错的
- ✅ `{userid}`（账户 ID）确实存在，"待实测"标记解除

**新增 `## 转化回传规范 · 360 点睛` 完整章节**
- 两条并列链路：网页转化数据 API（`POST convert.dop.360.cn/uploadWebConvert`，HEADER 鉴权 `App-Sign: md5(Secret+POSTDATA)`）与 搜索点击下发（feedback_url + callback_url）
- `data_industry` 四值枚举与产品线对应关系
- `event` 转化类型枚举 **约 50 个**，并标注移动推广仅支持其中 4 个
- `event_param` 六个子字段：`value`(分) `score` `outeruserid` `bname` `urtime` **`spare`（1001 无效转化 / 1002 非无效转化）**
- 错误码 errno 1/2/3、二次回传一致性规则、不支持批量上报、账户共享上限 30 个

**按用户反馈调整的定性**
- 谷歌搜索系列误用 `{devicemodel}` —— 用户已知悉，仅存档
- 360 缺 UTM —— 属「投放同学暂未启用，后续会启用」，从问题降级为待办
- **新增《UTM 取值治理原则》**：规范只收录通用标准枚举；生产中的 `googleads_int` / `paid_social` 等记为历史遗留，不追溯改造，新链接用标准值，BI 侧用 alias 映射表归一
- 其余一律以官方文档为准，无官方依据的记为「🔍 生产观察，待测试」

### v2.1 — 2026-07-29（百度 / 360 / 巨量 官方文档到手，逐条覆盖）

用户提供 6 份官方文档：《360设置URL》《百度信息流-应用API埋码指南》《百度搜索-程序调用示例》《百度Android BD_VID注入归因增强方案 v20250303》《Baidu IOS端归因升级方案 v1.9 / 2026-06》《巨量 URL 规范》。宏 450 → **492**，备注 288 → **337**。

**结构性修正**
- **百度拆成两个体系**：`baidu`（落地页 URL 通配符，`{}` 小写）与新增 `baidu_app_api`（应用 API 监测地址，**搜索与信息流通用**，28 个宏）。原先猜测的 `baidu_feed`「双花括号全大写」不准确 —— 官方是 `__XXX__` 与 `{{XXX}}` **两种写法等价**
- **`__SIGN__` 必须是 URL 最后一个参数** —— 工具已加排序逻辑强制保证，勾选任何可选宏都不会把它挤到中间
- 新增 `## 转化回传（Callback）规范` 一节：百度 a_type 全量枚举（23 个）、join_type、错误码 100–110、巨量新旧端点对比、各平台端点汇总

**百度新发现**
- **`__BD_VID__`**（Android APK V2 签名注入归因，签名 ID `0x710987bd`）—— 100% 准确归因，官方归因优先级 **BD_VID > OAID > IMEI > IP+MODEL > IP+OS_VERSION**。需邮件申请白名单 + 推广包托管百度应用中心
- **宏名与参数名错位**（最大的坑）：`__IMEI__` 下发的是 imei_md5、`__ANDROIDID__` 下发的是 android_id_md5、`__MAC__` → 参数 mac1、`__MAC1__` → 参数 mac_md5
- 我之前判定「百度无 `{os}`」需修正为：**落地页通配符体系确实没有**，但应用 API 监测地址有 `__OS_TYPE__`（安卓2/iOS1/**鸿蒙5**）与 `__OS_VERSION__`。旧的 `OS` / `{{OS}}` 已于 2023-03-15 下线
- 新增宏：`__USER_ID__` `__SIZE__` `__COMBID__` `__DEEPLINK_URL__` `__EXT_INFO__` `__IPV6__` `__CAID__`
- 百度自动追加、无需手写：`ip_type` · `actType`(2点击/3曝光) · `interactionsType`(1点击/2有效播放/6曝光归因) · `attribution_eshow_score`
- `__DEVICE_INFO__` **官方文档自相矛盾**：信息流附录标注 2023-03-15 已下线，但 2026-06 版归因方案仍将其列为模糊归因方案二的必需字段
- iOS：CAID 归因建议只用第 1+2 部分；中广协 `20260506` 新算法 6/30 已切换，**`20230330` 不再返回**；深度转化建议用 IDFV 关联

**360 修正**
- 官方现行关键词宏是 **`{keywordid}`**（每个关键词唯一 ID，不同组下同一关键词 ID 不同）。旧资料里的 `{wordid}`（CityHash64、跨组不唯一）**已不在官方文档中**，降级为历史遗留标注
- `{userid}` 未出现在官方《设置URL》中，标记为待实测
- 确认可插入位置：创意点击链接 / 关键词 URL / 比翼子链，PC 与移动端均可用

**巨量修正与补全**（宏 29 → 46）
- **`__OS__` 的 2 是鸿蒙不是 WP** —— 原配置错误
- **升级版应忽略原版宏**：官方原文"建议您在投放升级版时可忽略或不添加"AID / AID_NAME / CID / CID_NAME / CAMPAIGN_ID / CAMPAIGN_NAME / CTYPE。默认勾选项已改为 PROJECT_ID / PROMOTION_ID / CSITE / CALLBACK_PARAM / TS / TRACK_ID
- 新增 **`__TRACK_ID__`**（请求 id & 创意 id 的 md5，16 位）—— 官方 FAQ 明确这是**串联落地页与监测链接**的推荐方式
- 新增 `__GEO__` `__CITY_CODE__` `__PRODUCTID__`（仅站内）`__OUTERID__`（站内+穿山甲）`__CAID__`（推荐，`__CAID_MD5__` 仅星图支持）`__CALLBACK_URL__`
- `__ANDROIDID__` 下发的是**原值的 md5**（宏名无 _MD5 但值是 md5）
- 展示监测**不支持双 IP 方案**（`__IPV4__`/`__IPV6__`/`__ADVERTISER_ID__` 仅有效触点）；展示场景用 `__IP__`
- 营销目的 = 销售线索收集时，IDFA / IDFA_MD5 / ANDROIDID / OAID / OAID_MD5 / CAID **均不下发**
- **监测域名须企业备案**，否则报"该监测链接域名无企业备案"
- `__IMEI__` / `__IMEI_MD5__` **未出现在官方参数列表**中，降级为待实测

**剩余待补**：Snapchat · 快手「附件一」· 小红书后台下拉 · UC汇川 · 知乎最新 PDF · Naver 取值字典 · Reddit 字面量列 · LinkedIn UI 语法（见 `PENDING-VERIFICATION-CHECKLIST.md`）

### v2 — 2026-07-28（官方文档逐条核实）

- 平台 **22 → 37**（新增 Google Demand Gen / App Campaigns / Shopping / Hotel、Bing Shopping / Lodging、百度信息流、360 展示、腾讯曝光监测、快手品牌 MMA、阿里妈妈东风、微博 APP 激活）
- 宏 **204 → 450**，新增 **288 条官方备注**与 **34 条平台级警告**
- **删除约 40 个经核实不存在的宏**，重点：
  - Meta：`{{ad.format}}` `{{creative.id}}` `{{publisher_platform}}` `{{platform}}` `{{product.id}}`（官方仅 8 个宏）
  - Bing：`{Custom1}~{Custom8}`（是"上限 8 个自命名 `{_key}`"被误记）、`{IfContent:}` `{SitelinkId}` `{ProductPartitionId}`、Bing PMax `{AssetGroupId}`
  - TikTok：`__AD_FORMAT__` `__INTEREST_CATEGORY__` `__AGE__` `__GENDER__`
  - 腾讯：`__PLATFORM__` `__OS_VERSION__` `__CONNECTION_TYPE__` `__SITE_SET__` `__PLACEMENT_ID__`
  - 快手：`__PLATFORM__` `__OS_VERSION__` `__GENDER__` `__AGE__`（且 DSP 有宏白名单校验会直接报错）
  - 百度：`{os}` `{age}` `{gender}`、`{groupid}`（属 360）、7 个已下线通配符
  - 知乎：`{position}` 及全部花括号写法（知乎只用 `__XXX__`）
  - X / Twitter：全部 5 个宏（整个体系不存在）
  - Yandex：`{addphrases}`；Naver：`n_campaign`；Pinterest：双花括号写法与 `{keyword}`
- 语法修正：Pinterest 改单花括号、LinkedIn 改 UPPER_SNAKE_CASE、知乎改 `__XXX__`、微博改混合大小写花括号
- 工具增强：平台级 ⚠️ 警告横幅、官方文档链接、宏级 ⓘ 悬停备注、未确证宏黄色描边、CSV 模板收敛为核心字段
- 备份：`url-builder/index.html.bak-20260728`、`AD-TRACKING-PARAM-SPEC.md.bak-20260728`
- 详细取证过程与来源链接：`AD-TRACKING-PARAM-SPEC-v2-RESEARCH.md`

**仍需人工登录后台补齐（6 项）**：巨量权威页渲染 · Snapchat 宏下拉 · 快手「附件一」宏全表 · 小红书账户三方监测下拉 · 百度/360 图片版参数表 · UC汇川 PDF / 知乎最新 PDF / Naver 取值字典 / Reddit 字面量列 / LinkedIn UI 花括号语法
