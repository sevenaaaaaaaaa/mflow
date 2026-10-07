# 投放链接追踪参数 · 官方核实版补全报告 (v2)

> 生成日期：2026-07-28
> 方法：5 条并行研究线程，逐平台抓取第一方官方文档（帮助中心 / 开放平台 API / 官方 PDF）。
> **每条参数均标注来源。凡未能在实际抓取到的来源中核实的，一律进 `⚠️ 未能证实` 区，不写入主表。**

---

## 0. 执行摘要 —— 先看这 8 条结论

1. **你现有配置里存在多个不存在的宏（编造/误记）**，直接投产会导致占位符原样出现在 URL 里。完整否证清单见 §11。最严重的：
   - Meta 的 `{{ad.format}}` `{{creative.id}}` `{{publisher_platform}}` `{{product.id}}` —— **官方仅 8 个宏，这些都不存在**
   - Bing 的 `{Custom1}~{Custom8}` —— **不是宏**，是"最多 8 个自命名 `{_key}`"被误记
   - TikTok 的 `__AD_FORMAT__` `__INTEREST_CATEGORY__` `__AGE__` `__GENDER__` —— **不存在**
   - 腾讯的 `__PLATFORM__` `__OS_VERSION__` `__CONNECTION_TYPE__` `__SITE_SET__` —— **不存在**
   - 快手的 `__PLATFORM__` `__OS_VERSION__` `__GENDER__` `__AGE__` —— **不存在，且快手有宏白名单校验会直接报错**
   - 百度的 `{os}` `{age}` `{gender}` —— **不存在**
   - 知乎的 `{position}` —— **不存在**（知乎根本不用花括号语法）
2. **"创意/素材层面回传"这个需求，绝大多数平台给不了。** 全行业只有 4 家真正提供素材级宏：**巨量引擎**（`__MID1__`~`__MID6__` 分图片/标题/视频/试玩/落地页/下载页）、**腾讯广告**（`__ELEMENT_INFO__` / `__CREATIVE_COMPONENTS_INFO__` JSON）、**TikTok**（`__CID__` creative 层）、**Google**（`{param1}/{param2}` + PMax `{assetgroupid}`）。其余平台最细只到 ad/creative ID，**没有任何平台回传 `ad_format` / `creative_type` 这类素材形态字段**（唯一例外：巨量 `__CTYPE__` 创意样式、快手品牌侧、腾讯 `__AD_TYPE__`）。
3. **X / Twitter Ads 完全没有 URL 宏体系**。只有 `twclid` + Pixel 事件参数。UTM 必须逐条广告手写静态值。
4. **Naver 不是宏，是开关**。勾选后 Naver 自动追加 10~12 个 `n_*` 真实 query key，广告主无占位符可写。
5. **小红书客观上就只有这么少**。官方三方监测仅支持「账户 / 创意」两级，官方 FAQ 明文"新链路不支持下发其他宏参数，只拼接 clickID"。你的 1 个参数不是漏配，是平台上限。
6. **腾讯的宏不在落地页 URL 上**。腾讯是两条链路：宏用于点击/曝光监测链接（服务端 GET 你的服务器），落地页上腾讯只自动追加 `gdt_vid`（微信流量）/ `qz_gdt`（非微信流量）。
7. **需新增的平台**：Google Demand Gen、Google App Campaigns（原缺失）、Google Shopping、Google Hotel/Travel、Bing Shopping、Bing Lodging、腾讯曝光监测、微博 APP 激活链路 —— 这些的宏集与主平台差异大到应独立成条目。
8. **需人工登录后台补齐的 6 项**（机器不可达）见 §12。

---

## 1. Google Ads Search

- **来源**：[ValueTrack 主表 6305348](https://support.google.com/google-ads/answer/6305348) · [About ValueTrack 2375447](https://support.google.com/google-ads/answer/2375447) · [Custom parameters 6325879](https://support.google.com/google-ads/answer/6325879) · [API valuetrack-mapping](https://developers.google.com/google-ads/api/docs/reporting/valuetrack-mapping) · [iOS14 measurement 10417364](https://support.google.com/google-ads/answer/10417364)
- **Click ID (自动)**：`gclid`（auto-tagging）。iOS14+ 受 ATT 影响的 Google App 流量不再下发 gclid，`{gclid}` 为空，由 `wbraid` 承接。

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| campaign_id | `{campaignid}` | campaign | |
| adgroup_id | `{adgroupid}` | ad group | |
| feed item id | `{feeditemid}` | asset | **Display 不可用**；已被 `{extensionid}` 取代 |
| asset id | `{extensionid}` | asset | **Display 不可用** |
| target id | `{targetid}` | criterion | 前缀 `kwd`/`kwl`(AI Max keywordless)/`dsa`/`aud`/`pla`/`hpi`；多值顺序 `aud, dsa, kwd, pla, hpi`；**不含 affinity/in-market audience** |
| 兴趣地理 | `{loc_interest_ms}` | click | 仅"搜索目标地点"流量有值 |
| 物理地理 | `{loc_physical_ms}` | click | 仅"位于目标地点"流量有值 |
| 匹配类型 | `{matchtype}` | criterion | `e`/`p`/`b`/`a`(AI Max keywordless) |
| 网络 | `{network}` | click | `g`/`s`/`d`/`ytv`/`vp`/`gtv`/`x`(PMax全量)/`e`(ACe) |
| 设备 | `{device}` | click | `m`/`t`/`c` |
| 设备型号 | `{devicemodel}` | click | **仅 Display Network**（官方明文） |
| click id | `{gclid}` | click | |
| 条件宏 | `{ifmobile:X}` `{ifnotmobile:X}` `{ifsearch:X}` `{ifcontent:X}` | click | |
| 创意 ID | `{creative}` | ad | = `ad_group_ad.ad.id` |
| 关键词 | `{keyword}` | criterion | **AI Max / DSA / PMax 下返回空** |
| 展示位置 | `{placement}` | click | Display/Video |
| 位置类别 | `{target}` | criterion | **仅 placement-targeted campaigns** |
| 创意参数 | `{param1}` `{param2}` | ad/criterion | 需 AdParamService 设置 |
| 随机数 | `{random}` | click | unsigned 64-bit |
| 忽略追踪 | `{ignore}` | final URL only | 不能嵌套在其他宏内 |
| 广告位置 | `{adposition}` | click | 形如 `1t2`。**API 映射文档有，Help Center 主表未列** |

**URL 插入宏（仅 tracking template）**：`{lpurl}` `{lpurl+2}` `{lpurl+3}` `{unescapedlpurl}` `{escapedlpurl}` `{escapedlpurl+2}` `{escapedlpurl+3}`。拼接后缀：开头 `?`；非开头 `{lpurl}%3F` / `{lpurl+2}%253F` / `{lpurl+3}%25253F` / `{unescapedlpurl}?` / `{escapedlpurl}%3F`。DSA 与 auto-targets **所有层级都必须含插入宏**。

**AI Max 组合判别表**（Search 专属，排错必备）

| 流量类型 | `{matchtype}` | `{targetid}` | `{keyword}` |
|---|---|---|---|
| 标准关键词匹配 | e/p/b | `kwd-<id>` | 匹配到的关键词 |
| AI Max broad expansions | e/p/b | `kwd-<id>` | 匹配到的关键词 |
| AI Max keywordless | `a` | `kwl-3500001` / `kwl-<URL rule id>` | **空** |

**AI Max tracking template 兼容性（重要 gotcha）**：final URL expansion 会替换 advertiser URL。只有 `{lpurl}?` / `{lpurl}&` / `{lpurl}#` / 裸 `{lpurl}` 安全。静态 tracking URL（无 `{lpurl}`）会把用户导到静态页；`foo={lpurl}value` 会 404。

**自定义参数（官方全规则）**：`{_name}`；**最多 8 个**；可在除 account 外任意层级设置；name ≤ 16 字母数字；value ≤ 250 字符且**可嵌套 ValueTrack 参数**；同名取最具体层级；变更 24–48h 生效。

**`{ignore}` 完整行为**：仅 final URL / final mobile URL；用于降低抓取负载；**不能嵌套**（`{ifmobile:{ignore}}` 非法）；若 final URL 中任何内容可被第三方在点击时修改，**政策强制要求**使用（[6021546](https://support.google.com/adspolicy/answer/6021546)）。

**Click ID 出现时机**

| 参数 | 何时出现 |
|---|---|
| `gclid` | auto-tagging 开启后随点击追加 |
| `wbraid` | iOS app 内点击 → 落到网页（app-to-web），2021-03 引入 |
| `gbraid` | 网页点击 → 进入 iOS app（web-to-app）；**大小写敏感不可转换**；**仅 Search / Shopping / Display / PMax** |
| `dclid` | **属 DV360/CM360 体系，不是 Google Ads ValueTrack 宏** |

---

## 2. Google Performance Max

- **来源**：[6305348 PMax 段](https://support.google.com/google-ads/answer/6305348) · [API PMax ValueTrack](https://developers.google.com/google-ads/api/performance-max/valuetrack)
- **Click ID**：`{gclid}` —— 官方标注 **Limited support**。

| 宏字段 | 语法 | 支持度 | 备注 |
|---|---|---|---|
| **Asset group ID** | `{assetgroupid}` | **Fully supported** | ✅ PMax 独有，`{assetgroupid}` 确认完整可用 |
| campaign_id | `{campaignid}` | Fully | |
| 设备 | `{device}` | Fully | |
| 条件 | `{ifmobile:}` `{ifnotmobile:}` | Fully | |
| 地理 | `{loc_interest_ms}` `{loc_physical_ms}` | Fully | |
| URL 插入 | `{lpurl}` `{lpurl+2}` `{lpurl+3}` | Fully | |
| 随机 | `{random}` | Fully | |
| click id | `{gclid}` | **Limited** | |
| 广告类型 | `{adtype}` | Limited | `pla`/`pla_multichannel`/`pla_with_promotion`/`pla_with_pog` |
| 商品系列 | `{merchant_id}` `{product_channel}` `{product_id}` `{product_country}` `{product_language}` | Limited | 取决于是否有 product feed |

**PMax gotchas（官方明文）**
- `{ifsearch:}` `{ifcontent:}` `{ifpla:}` `{iflia:}` → **Evaluates to false**
- `{keyword}` → **返回空**
- `{network}` → **恒为 `x`**，官方："Statistics by specific inventory types are not provided"，API 对应 `AdNetworkType = MIXED`
- PMax 表**未列出**：`{adgroupid}` `{matchtype}` `{targetid}` `{feeditemid}` `{extensionid}` `{devicemodel}` `{placement}` `{target}` `{creative}` `{param1/2}` `{ignore}` `{product_partition_id}` `{store_code}`
- API 标记 **deprecated**：`{carrier}` `{ifauto:}` `{copy}` `{city}` `{keyword.}` `{localbusiness.}` `{lb.}`
- 自定义参数：官方明文支持 **asset group 与 campaign 两级**

---

## 3. Google Display Network

- **来源**：同 §1
- **Click ID**：`gclid`；`gbraid` 适用。**`{dclid}` 不是 Google Ads 宏。**

Display 专属/差异点（其余同 Search 主表）：

| 宏字段 | 语法 | 备注 |
|---|---|---|
| 设备型号 | `{devicemodel}` | **官方唯一点名 Display 专属的宏** —— ✅ 确认可用 |
| 网络 | `{network}` | 返回 `d`；Google video partners 返回 `vp`（API 均归 `CONTENT`） |
| 展示位置 | `{placement}` | 关键词定向→被点内容站点；位置定向→匹配的 placement 条件 |
| 位置类别 | `{target}` | **仅 placement-targeted** |
| 关键词 | `{keyword}` | 返回与内容匹配的账户关键词（语义与 Search 不同） |

**Display 不可用**：`{feeditemid}`、`{extensionid}`（官方明文）。

---

## 4. Google Demand Gen 【新增平台】

- **来源**：[6305348 Demand Gen 段](https://support.google.com/google-ads/answer/6305348) · [valuetrack-mapping](https://developers.google.com/google-ads/api/docs/reporting/valuetrack-mapping)
- **Click ID**：`gclid`（无特殊限制说明）
- **官方只给"不支持"清单**，这是唯一权威声明：

| 宏 | 状态 |
|---|---|
| `{placement}` | ❌ 不支持 |
| `{target}` | ❌ 不支持 |
| `{keyword}` | ❌ 不支持 |
| `{ifsearch:}` | ❌ 不支持 |
| `{ifcontent:}` | ❌ 不支持 |
| `{network}` | ❌ **完全不返回**（UI 显示 "Google-owned channels"，API enum `UNKNOWN`） |
| `{targetid}` | ❌ 不支持 |
| 其余主表宏 | 官方措辞"回落到主表"，但**未逐条列举** |

- **创意层**：`{creative}` 未被列入不支持清单，可用。Demand Gen 支持 business data feeds，但**无 feed 专属宏**。
- **自定义参数**：未被排除，按通用规则 8 个上限。

---

## 5. Google App Campaigns 【新增平台】

- **来源**：[2375447 App campaigns 段](https://support.google.com/google-ads/answer/2375447) · [第三方点击追踪 7382504](https://support.google.com/google-ads/answer/7382504) · [10417364](https://support.google.com/google-ads/answer/10417364)
- **最大结构性 gotcha（官方原文）**：
  > "Third-party click trackers … should be implemented … using Android and iOS **tracking templates across most campaign types, excluding App campaigns**"

  即 **App campaigns 不能用 tracking template 挂第三方 click tracker**。用 ValueTrack 的唯一前提：
  > "You can use ValueTrack parameters with your App campaigns if you're using a third-party analytics solution that uses **Confirmed Installs**."

| 宏 | 状态 |
|---|---|
| `{network}` | ✅ 主表定义 `e` = "all **App campaigns for engagement (ACe)** traffic, except Google search traffic" —— 主表中唯一显式提到 App campaigns 的取值 |
| `{campaignid}` `{adgroupid}` `{creative}` `{device}` `{loc_*}` `{random}` | 官方称 ValueTrack "compatible with App campaigns"，但**无 App 专属清单表** |
| **`{aceid}`** | ⚠️ **无法证实用于 App campaigns** —— 详见下 |

**关于 `{aceid}` —— 结论：否**
- Help Center 主表 6305348 中**已不存在** `{aceid}`
- 仅出现在 API PMax ValueTrack 页的参数清单里，且该表支持标记为图标不可判读
- **没有任何官方页面**表述"`{aceid}` 用于 App campaigns"
- 网上"实验/对照组 ID"的解释来自第三方博客，不采信

**Click ID**：`gclid`（auto-tagging 追加到 click tracker）；iOS 场景 `gbraid`/`wbraid`。⚠️ 但官方明确 `gbraid` **仅适用 Search/Shopping/Display/PMax**，App campaigns 不在列表内。

**App Attribution Partners**（Google 专用链接内置 ValueTrack）：Adjust / Airbridge / AppsFlyer / Branch / Kochava / Singular / Tenjin。

---

## 6. Google Shopping / Hotel & Travel / Video 【建议新增】

**Shopping only**：`{adtype}`（`pla`/`pla_multichannel`/`pla_with_promotion`/`pla_with_pog`）`{merchant_id}` `{product_channel}` `{product_id}` `{product_country}` `{product_language}` `{product_partition_id}` `{store_code}`（**60 字符上限**）。API 另列 `{product_feed_label}`。

**Hotel only**：`{hotelcenter_id}` `{hotel_id}` `{hotel_partition_id}` `{hotel_adtype}` `{travel_start_day|month|year}` `{travel_end_day|month|year}` `{advanced_booking_window}` `{date_type}` `{number_of_adults}` `{price_displayed_total}` `{price_displayed_tax}` `{user_currency}` `{user_language}` `{adtype}`(`travel_booking`/`travel_promoted`) `{rate_rule_id}`。

**Video only**：`{adgroupid}` `{campaignid}` `{creative}` `{device}` `{loc_*}` `{network}` `{placement}` **`{sourceid}`**（官方列出但未给定义）。

⚠️ **Vehicle Ads 专属参数：未找到任何官方文档**。6305348 无 Vehicle 分节，`{vehicle_id}` 之类无官方依据。
⚠️ **Things-to-do (Travel) 额外参数：除 Hotel 表内的 `{adtype}` 与 `{rate_rule_id}` 外未找到。**
⚠️ **Website Call Conversions：官方 ValueTrack 文档中没有 call conversion 专属宏。** API 清单里有 `{websitecallmetric}` 但**无任何官方定义**。实际是通过 gtag 的 `phone_conversion_number` / `phone_conversion_callback` / `phone_conversion_css_class` / `phone_conversion_options` 配置，这些是 gtag 配置项而非 URL 宏。

---

## 7. Meta Ads (Facebook + Instagram)

- **来源**：[Specifications for dynamic URL parameters](https://www.facebook.com/business/help/2360940870872492) · [Add URL Parameters](https://www.facebook.com/business/help/1016122818401732)
- **Click ID**：`fbclid` —— **官方文档完全未提及**，未取证（Conversions API 的 fbp/fbc 页被登录墙拦）。官方只说明 2024-01-01 起自动加：Campaign Source (Facebook/Instagram)、Campaign Medium (paid)、Ad ID、Campaign ID、Adset ID、Campaign Tracking Group ID。

**官方全部宏 —— 只有 8 个，一个不多**

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| 广告 ID | `{{ad.id}}` | Ad | |
| 广告组 ID | `{{adset.id}}` | Ad set | |
| 广告系列 ID | `{{campaign.id}}` | Campaign | |
| 广告名称 | `{{ad.name}}` | Ad | **锁定为首次发布时的名称**，之后改名不变 |
| 广告组名称 | `{{adset.name}}` | Ad set | 同上 |
| 广告系列名称 | `{{campaign.name}}` | Campaign | 同上 |
| 版位 | `{{placement}}` | 投放时 | 取值见下 |
| 站点来源 | `{{site_source_name}}` | 投放时 | `fb`/`ig`/`msg`/`an`/`th`(Threads) |

**`{{placement}}` 官方支持值**：`audience_network_classic`、`audience_network_rewarded_video`、`facebook_feed`(2026-03 起含 Friends tab)、`facebook_instream`、`facebook_marketplace`、`facebook_right_column`、`instagram_feed`、`instagram_stories`、`messenger_inbox`、`messenger_sponsored_messages`、`threads_stream`。
⚠️ 官方列表**没有** `instagram_reels` / `facebook_reels` / `instagram_explore` —— 部分实际版位不在文档中。

- **创意层面参数**：**完全没有**。无 creative、无 format、无 image/video ID。最细粒度就是 Ad 层。
- **自定义参数**：只支持自写静态 key=value（`&` 分隔，key 不可空值）。位置在广告层 **Tracking → URL parameters**。
- **URL parameters 字段 vs Website URL（官方规则）**：URL parameters 内容追加到 Website URL（去重）；**同名参数以 URL parameters 字段为准并覆盖 Website URL**；Ads Manager 里加的参数会覆盖别处设置（如 Instagram 默认参数）；URL 参数只作用于第一个落地/商品页。
- **限制**：动态参数**不支持** Instagram 版位的 collection 广告、app promotion 目标。**Catalog 目录销售 / Store locations 只有 URL parameters 字段，无 Website URL 字段**。发布后改 URL 参数可能触发重新学习期。
- **Catalog/Advantage+ 专属**：**官方无任何专属宏**。商品级归因需在 feed 的 `link` 字段自带参数。

---

## 8. Microsoft Advertising / Bing Ads

- **来源**：[What tracking or URL parameters can I use? (56799)](https://help.ads.microsoft.com/#apex/3/en/56799/2) · [URL Tracking with Upgraded URLs](https://learn.microsoft.com/en-us/advertising/guides/url-tracking-upgraded-urls?view=bingads-13) · [CustomParameter Data Object](https://learn.microsoft.com/en-us/advertising/campaign-management-service/customparameter?view=bingads-13)
- **Click ID**：`{msclkid}`。自动版本 = 账户级 "Add Microsoft Click ID (MSCLKID) to URLs"（Shared Library → Account level options）；2017-12-11 起新建转化目标时自动开启。
- **宏名大小写不敏感。**

### ① Destination URL / Final URL / Tracking template / Custom parameter 均可用

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| campaign_id | `{CampaignId}` | Campaign | |
| campaign_name | `{Campaign}` | Campaign | |
| adgroup_id | `{AdGroupId}` | Ad group | **PMax 用它代替 asset group ID** |
| adgroup_name | `{AdGroup}` | Ad group | **PMax 用它代替 asset group name** |
| target_id | `{TargetId}` | Criterion | `kwd`/`aud`/`dat`/`pla`/`loc` 前缀；多值顺序 aud, dat, kwd, pla；in-market audience 与 LinkedIn profile 定向**不返回** |
| 匹配类型 | `{MatchType}` | Keyword | e/p/b（expanded 也算 b） |
| 出价匹配类型 | `{BidMatchType}` | Keyword | be/bp/bb |
| 网络 | `{Network}` | 投放时 | `o`=owned&operated(Bing/AOL/Yahoo) / `s`=syndicated / `a`=audience placements |
| 设备 | `{Device}` | 投放时 | m/t/c |
| 条件宏 | `{IfMobile:s}` `{IfNotMobile:s}` `{IfSearch:s}` `{IfNative:s}` `{IfPLA:s}` | 投放时 | `{IfNative:}` = Microsoft Audience Ad 时替换 |
| ad_id | `{AdId}` | Ad | |
| 关键词 | `{keyword:default}` | Keyword | 空格转 `%20`；建议给 default |
| click id | `{msclkid}` | 投放时 | |
| order item id | `{OrderItemId}` | Keyword / 商品组 | Shopping 时返回 product group ID |
| 关键词自定义 | `{param1:d}` `{param2:d}` `{param3:d}` | Keyword | 取关键词的 Param1/2/3 设置 |
| 搜索词 | `{QueryString}` | 投放时 | 用户输入的查询文本 |
| 复制查询参数 | `{copy:queryparameter}` | 扩展 | **仅 Destination URL 有效，Final URL 无效** |
| 扩展 ID | `{feeditemid}` | Ad extension | 被点击的广告扩展 ID |
| 地理 | `{loc_physical_ms}` `{loc_interest_ms}` | 投放时 | |

> 官方提示：自定义参数放 tracking template 返回变量值，放 destination URL 返回**空值**。

### ② 仅 Tracking template
`{lpurl}` `{lpurl+2}` `{lpurl+3}` `{unescapedlpurl}` `{escapedlpurl}` `{escapedlpurl+2}` `{escapedlpurl+3}`
account/campaign/ad group 级 template **必须**至少含一个；必须以 `http://`、`https://`、`{lpurl}` 或 `{unescapedlpurl}` 开头；**上限 2,048 字符**。

### ③ 仅 Final URL
`{ignore}`（不能嵌套）

### ④ Shopping only
`{CriterionId}`(=`{OrderItemId}`) `{OrderItemId}` `{product_channel}` `{product_country}` `{ProductId}` `{product_language}` `{seller_name}`

### ⑤ Lodging / Travel only
`{hotelcenter_id}` `{property_id}` `{hotel_partition_id}` `{hotel_adtype}` `{travel_start_day|month|year}` `{travel_end_day|month|year}` `{advanced_booking_window}` `{date_type}` `{number_of_adults}` `{price_displayed_total}` `{price_displayed_tax}` `{user_currency}` `{user_language}` `{adtype}` `{rate_rule_id}`

**自定义参数（重点纠正）**：语法是**自命名** `{_key}`（Bulk service 必须带 `{_...}`；Campaign Management API 的 Key 字段不含大括号和下划线）。Key ≤ 16 UTF-8 字节，Value ≤ 250 字节（action/price/sitelink 扩展 200，pilot 635 提至 250）。**数量上限：campaign / ad group / ad group criterion / ad 各 8 个**；action、price、sitelink 扩展默认 **3 个**（pilot 下 8）。低层级覆盖高层级。Microsoft **不校验**自定义参数是否存在，不存在时占位符原样输出。

**Final URL suffix**：可放静态参数与以 MS URL 参数为值的参数；不能以 `?`/`&`/`#` 开头；不能含 `{ignore}` `{lpurl}` `{escapedlpurl}`。

- **创意层面参数**：仅 `{AdId}`；扩展层 `{feeditemid}`。**无素材/资产级宏。**

---

## 9. Bing Performance Max

- **来源**：[56799 PMax 注意事项](https://help.ads.microsoft.com/#apex/3/en/56799/2) · [Performance Max Campaigns](https://learn.microsoft.com/en-us/advertising/guides/performance-max?view=bingads-13) · [官方 Q&A 2289877](https://learn.microsoft.com/en-us/answers/questions/2289877/network-valuetrack-parameter-in-performance-max)
- **结论：Bing PMax 没有独立宏集**，沿用 §8 的 ①②③（Shopping 类 PMax 可用 ④）。唯一官方特殊说明：

| 项 | 结论 |
|---|---|
| Asset group ID | **官方明示不支持** asset group 宏，须用 `{AdGroupId}` 取资产组 ID |
| Asset group name | 须用 `{AdGroup}` |
| `{Network}` | PMax 仍只返回 o/s/a。官方支持确认：AOL Search、Microsoft sites and select traffic 都是 `o`；**Cross-network 没有独立取值** |
| 创意层 | **无**。最细到 `{AdGroupId}`（= asset group） |
| 自定义参数 | 与普通 campaign 相同，层级上限 8 |

⚠️ `{AssetGroupId}` / `{asset_group_id}` —— **官方明确不支持**。Google PMax 的 ValueTrack 页**不适用于** Microsoft。

---

## 10. 其余平台（简表 + 关键结论）

### TikTok Ads
- **来源**：[About UTM parameters](https://ads.tiktok.com/help/article/track-offsite-web-events-with-utm-parameters)（标注 Last updated: February 2026）· [About TikTok Click ID](https://ads.tiktok.com/help/article/tiktok-click-id?lang=en) · [How to add URL parameters](https://ads.tiktok.com/help/article/how-to-add-url-parameters-to-your-website-url-in-tiktok-ads-manager) · [Best practices](https://ads.tiktok.com/help/article/utm-parameters-best-practices)
- **Click ID**：`ttclid` 自动附加，有效期与 Attribution Manager 的 CTA 窗口一致。手填宏为**单下划线** `_CLICKID_`。
- **官方宏共 9 个：**

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| Campaign 名称 | `__CAMPAIGN_NAME__` | Campaign | |
| Campaign ID | `__CAMPAIGN_ID__` | Campaign | |
| 广告组名称 | `__AID_NAME__` | Ad Group | ⚠️ **AID = Ad Group，不是 Ad** |
| 广告组 ID | `__AID__` | Ad Group | |
| 广告名称 | `__ADID_V2_NAME__` | Ad | **仅 upgraded Smart+ campaigns** |
| 广告 ID | `__ADID_V2__` | Ad | **仅 Smart+** |
| 创意名称 | `__CID_NAME__` | Creative | ⚠️ **CID = Creative，不是 Campaign** |
| 创意 ID | `__CID__` | Creative | |
| 版位 | `__PLACEMENT__` | 投放 | TikTok / TikTok Pangle |

- **创意层**：`__CID__`/`__CID_NAME__` + Smart+ 的 `__ADID_V2__`。**Spark Ads 无任何专属宏/参数**，走同一套 UTM + ttclid。
- **自定义参数**：支持。Ad details → Edit → Build URL parameters → Custom parameters → Add。另有 **Auto-attach**（自动补 utm_source=TikTok / utm_medium=Paid / ID / name）与 **Autodetect**（扫描已有参数，开启后自动附加到 catalog 商品链接）。`#` 之后内容会被丢弃；UTM 大小写敏感。
- ⚠️ **`__AD_FORMAT__` `__INTEREST_CATEGORY__` `__AGE__` `__GENDER__` 官方宏表中完全不存在 —— 确认不存在。** TikTok 不通过 URL 宏回传定向/人群维度。`__CLICKID__`（双下划线）、`__ADGROUP_ID__`、`__AD_ID__`、`__CSITE__`、`__CTYPE__` 也不在官方表中。

### Snapchat Ads —— ⚠️ 全部未能取证
`businesshelp.snapchat.com` 是 Salesforce Experience Cloud 纯 JS 站，`web_fetch` 只返回 Loading/CSS Error；`r.jina.ai` 代理返回空；Chrome 工具超时。**Snap Marketing API（已抓取）无 URL 宏内容**，只有 `third_party_on_swipe_tracking_urls` / `third_party_paid_impression_tracking_urls` 字段与 `${GDPR}` / `${GDPR_CONSENT_755}` 占位符。

需人工核对的官方页：[url-parameters](https://businesshelp.snapchat.com/s/article/url-parameters?language=en_US) · [add-url-macros](https://businesshelp.snapchat.com/s/article/add-url-macros?language=en_US) · [url-parameters-faq](https://businesshelp.snapchat.com/s/article/url-parameters-faq?language=en_US) · [edit-dynamic-macros](https://businesshelp.snapchat.com/s/article/edit-dynamic-macros?language=en_US) · [dynamic-ads-parameters](https://businesshelp.snapchat.com/s/article/dynamic-ads-parameters?language=en_US)

**仅搜索摘要级别（未确证，勿投产）**：`{{campaign.name}}` `{{campaign.id}}` `{{adSet.name}}`（注意 camelCase 大写 S）`{{adSet.id}}` `{{creative.name}}` `{{ad.id}}`；Click ID `ScCid`。官方称部分为 "dynamic macros"，编辑后可实时更新、无需暂停广告。
⚠️ **`{{creative.type}}` / `{{ad.is.swipeable}}` 无任何官方或第三方证据，极可能不存在**（点分命名风格也不符合 Snap 的 `entity.field` 模式）。`{{ad.name}}` `{{placement}}` `{{site_source_name}}` 专项检索无命中。**Collection Ads 专属参数完全未能证实。**

### Pinterest Ads
- **来源**：[Third-party and dynamic tracking](https://help.pinterest.com/en/business/article/third-party-and-dynamic-tracking) · [Track a collections ad](https://help.pinterest.com/en/business/article/track-a-collections-ad) · [Tag parameters and cookies](https://help.pinterest.com/en/business/article/pinterest-tag-parameters-and-cookies)
- **关键语法结论：Pinterest 用单花括号 `{param}`，不是双花括号。** 你清单里的 `{{campaignid}}` 是错的。
- **Click ID**：官方只确证 `_epik` / `_derived_epik` **cookie**。URL 上 `epik=` query 参数名未在已抓取官方页中出现。另 Pinterest 自动加 `pp=0`/`pp=1` 区分首跳与下游流量。

**A. 标准广告 destination URL**

| 宏字段 | 语法 | 备注 |
|---|---|---|
| campaign_id | `{campaignid}` | |
| campaign_name | `{campaign_name}` / `{campaignname}` | 两种都支持 |
| adgroup_id | `{adgroupid}` | |
| adgroup_name | `{ad_group_name}` / `{adgroupname}` | 两种都支持 |
| **creative_id** | `{creative_id}` | ✅ 语法确认 = the Pin promotion id |
| ad_id | `{adid}` | 与上者同值 |
| 设备 | `{device}` | `t`/`c`/`m` |

**B. Parallel click & impression counting（比 A 更全）**
`{campaignid}` `{campaign_id}` `{campaign_name}` `{campaignname}` `{adgroupid}` `{ad_group_id}` `{adgroupname}` `{ad_group_name}` `{adid}` `{ad_id}` `{creativeid}` `{creative_id}` `{itemid}` `{item_id}` `{insertionid}` `{insertion_id}`（可当 cache buster）`{creative_name}` `{device}` `{device_platform}`(`iOS`/`Android`/空) `{publisher}`(硬编码 `Pinterest`) `{timestamp}` `{click_timestamp}`

**C. Shopping campaigns 专属**
`{product_name}` `{product_id}` `{product_partition_id}` `{promoted_product_group_id}` `{unescapedlpurl}` `{lpurl}`（取 feed 的 `ad_link` 或 `link`）

- **创意层**：Collections Ads 专属 `{adid}` `{ad_id}` `{organic_url}`（= Pin 创建时的完整 URL）。secondary creative 的 destination URL 不能只填参数，须给完整 URL 或 `{organic_url}`，如 `{organic_url}?campaignid={campaignid}`。**自动生成的 personalized collections ads 的 secondary creatives 沿用 C 组 shopping 参数。**
- **三方跟踪仅支持这些域**：`ad.doubleclick.net`、`bs.serving-sys.com`、`d9.flashtalking.com`、`servedby.flashtalking.com`；曝光计数伙伴仅 DCM / Sizmek / Flashtalking / Trueffect。
- **自定义参数**：支持（UTM 及任意 key/value）。dynamic parameters 在 Pin 预览时**不展开**。
- ⚠️ **`{keyword}` 官方明确不支持**："the `{keyword}` parameter is not supported for tracking links on any ads"。`{targetingtype}` 官方无此项，疑似不存在。

### Reddit Ads
- **来源**：[How to Build a Campaign](https://advertising.reddithelp.com/en/categories/creating-ads/how-build-campaign)（抓取成功，含宏表全部描述列，但 markdown 转换**丢失了宏字面量那一列**）
- **格式（官方原文）**：`parametername={{REDDIT_MACRO}}`，`&` 连接；**"all macros are case sensitive"**（全大写 + 双花括号 + 下划线）
- **Click ID**：官方宏 `{{CLICK_ID}}`。落地页自动附加的 `rdt_cid` **仅第三方来源**。
- **官方表共 19 行**（描述列逐字官方；字面量按可核对度分级）：

| 描述（官方逐字） | 语法 | 证实度 | 备注 |
|---|---|---|---|
| Reddit account Advertiser ID | `{{ADVERTISER_ID}}` | ⚠️ | |
| iOS IDFA or Android GAID | `{{ADVERTISING_ID}}` | ⚠️ | |
| (第 3 行描述列为空) | `{{IDFA}}` | ⚠️ 未证实 | |
| Android GAID | `{{GAID}}` | ⚠️ 未证实 | |
| ID of the Campaign | `{{CAMPAIGN_ID}}` | ✅ 示例 URL 中出现 | |
| ID of the Ad Group | `{{ADGROUP_ID}}` | ✅ 示例 URL 中出现 | |
| Name of the Ad Group | `{{ADGROUP_NAME}}` | ⚠️ | |
| ID of the Ad | `{{AD_ID}}` | ⚠️ | |
| Name of the Ad | `{{AD_NAME}}` | ⚠️ | |
| ID of the post | `{{POST_ID}}` | ⚠️ | 形如 `t3_6lebsh` |
| Reddit's Click ID | `{{CLICK_ID}}` | ⚠️ | |
| Country (2 位 ISO) | `{{COUNTRY}}` | ⚠️ | |
| Operating system | `{{OS}}` | ⚠️ | 值含前缀：`osgrp,IOS`/`osgrp,MACOS`/`osgrp,ANDROID`/`osgrp,WINDOWS`/`osgrp,LINUX` |
| Device type | `{{DEVICE_TYPE}}` 或 `{{DEVICE_GROUP}}` | ⚠️ 二者存疑 | 值：`devgrp,PHN`/`devgrp,TAB`/`devgrp,DSK`/`devgrp,UNWN` |
| Platform type | `{{PLATFORM}}` | ⚠️ | 值：`plt,MBL`/`plt,DSK` |
| UNIX timestamp UTC | `{{CACHEBUSTER}}` | ⚠️ | |
| Height of the native ad post | `{{HEIGHT}}` | ⚠️ | px，创意层 |
| Width of the native ad post | `{{WIDTH}}` | ⚠️ | px，创意层 |
| Device opt-out | `{{DEVICE_OPT_OUT}}` | ⚠️ | `1`=True `0`=False |

- **创意层**：仅 `{{HEIGHT}}` / `{{WIDTH}}` / `{{POST_ID}}`。
- 三方 tracker 只接受 Reddit 认证 provider：Adjust、Appsflyer、Artsai (AdXcel)、Branch、Comscore、Gamesigh、Google (DCM)、King Games、Kochava、Singular、Sizmek、Tenjin。
- **自定义参数**：无独立字段；Destination URL "can include a UTM URL"，自行拼接。
- ⚠️ **`{{CAMPAIGN_NAME}}` 官方 19 行表里没有 "Name of the Campaign" 这一行** —— 只有 Ad Group / Ad 有 name 宏，疑似不存在。`{{CREATIVE_ID}}` `{{IMPRESSION_ID}}` 只出现在新版 business.reddithelp.com 示例 URL（搜索摘要）。

### X / Twitter Ads
- **来源**：[Conversion tracking for websites](https://business.x.com/en/help/campaign-measurement-and-analytics/conversion-tracking-for-websites) · [About Conversion Tracking](https://business.x.com/en/help/campaign-measurement-and-analytics/conversion-tracking-for-websites/about-conversion-tracking)
- **核心结论：X / Twitter Ads 没有任何官方 URL 动态宏 / tracking template 体系。** 无 campaign/ad-set/ad 层 URL 宏。UTM 必须逐条广告手写静态值。也无 bulk ad upload。
- **Click ID**：`twclid` —— 官方原文："X click ID that can be included with any request. **The X Pixel already automatically passes twclid from URL or first-party cookie.** This parameter can be optionally used to force attribution to a certain ad click."
- CAPI 须至少带一个 identifier：twclid / hashed email / hashed E164 phone；若传 IP 或 UA 需再配一个 identifier。CSP 需放行 `ads-twitter.com` `ads-api.twitter.com` `analytics.twitter.com` 的 `img-src` 与 `connect-src`。
- **Website Tag（Pixel）参数**：

| 类别 | 参数 |
|---|---|
| Event | `value`(int/float) `currency`(ISO 4217) `conversion_id`(去重键，Pixel+CAPI 双跑强烈建议) `search_string` `description` `twclid` `status`(`started`/`completed`) `contents`(数组) |
| Sub | `content_type`(Google product taxonomy) `content_id`(Catalog 传 SKU，其他优先 GTIN) `content_name` `content_price` `num_items` `content_group_id` |
| User | `email_address`(Pixel 自动 SHA256) `phone_number`(`+11234567890`，自动哈希) |
| 设置 | `hide_page_location: true`（`twq('set',{...})` 须置于 `config`/`init` 之前） |

- 事件类型：Page View, Purchase, Download, Custom, Lead, Add to Cart, Checkout Initiated, Content View, Added Payment Info, Search, Subscribe, Start Trial, Add to Wishlist, Product Customization。**Page View 30 分钟去重；其他事件类型不去重。**
- 官方提示：参数勾选框只生成代码模板，**不会自动采集值**。

### LinkedIn Ads
- **来源**：[Dynamic UTM Tracking (Marketing API v202606)](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/dynamic-utm-tracking?view=li-lms-2026-06) · [Enabling Click IDs](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/enabling-first-party-cookies?view=li-lms-2026-04)
- **Click ID**：`li_fat_id`。需在 Insight Tag 上启用 **Enhanced conversion tracking**（新建默认开启；API 侧 Partial Update Insight Tag 把 `firstPartyTrackingEnabled` = `true`）。每次点击自动追加到落地页 URL；cookie 自最近一次点击起保留 **30 天**。CAPI idType = **`LINKEDIN_FIRST_PARTY_ADS_TRACKING_UUID`**。
- **API 权威枚举（`AdDynamicTrackingParameterValue`，API 里是裸枚举无花括号）**：

| 宏字段 | API 枚举值 | 层级 | 备注 |
|---|---|---|---|
| 广告账户 ID | `ACCOUNT_ID` | Account | |
| 广告账户名 | `ACCOUNT_NAME` | Account | |
| Campaign Group ID | `CAMPAIGN_GROUP_ID` | Campaign Group | |
| Campaign Group 名 | `CAMPAIGN_GROUP_NAME` | Campaign Group | |
| Campaign ID | `CAMPAIGN_ID` | Campaign | |
| Campaign 名 | `CAMPAIGN_NAME` | Campaign | |
| Creative ID | `CREATIVE_ID` | Creative | |
| Creative 名 | `CREATIVE_NAME` | Creative | **自 version 202606 起才可用** |

- 配置：`PUT /rest/adTrackingParameters/(adEntity:(sponsoredCampaign:{urn}))`，body 分 `dynamicValueParameters`（key → 上述枚举）与 `customValueParameters`（key → 任意字符串，原样拼接）。
- **官方硬约束**：跟踪参数**只能设在 Campaign 层**，自动作用于该 Campaign 下所有 creative（含新建）；改动实时生效且**广告无需重新审核**；同一 Creative 可跨多 Campaign 分别打标；已有短链会在渲染前被追加动态参数。**不支持的创意格式：Conversation Ads、Message Ads。**
- **自定义参数**：`customValueParameters`（API）/ UI 静态参数。官方警告：creative 上已有静态 UTM 且 Campaign 层又配同名动态参数会产生重复 key。
- ⚠️ **`{{campaignId}}` `{{campaignGroupId}}` `{{creativeId}}` `{{accountId}}` 这种 camelCase 写法在官方枚举中不存在** —— 枚举全部是 UPPER_SNAKE_CASE。UI 的 `{{...}}` 双花括号语法本身未经抓取确证（LinkedIn help 页全部返回空响应）。
- ⚠️ **Document Ads / Thought Leader Ads 无任何专属 URL 参数**（官方只点名 Conversation Ads 与 Message Ads 为不支持格式）。
- ⚠️ LinkedIn 2025-10 把 Campaign Group / Campaign / Creative 更名为 Campaign / Ad Set / Ad（第三方来源），但 **API 枚举名仍为旧名**，UI 标签可能与枚举名不一致。

### Yandex Direct —— ✅ 唯一拿到完整第一方参数表的区域平台
- **来源**：[URL tags (EN)](https://yandex.com/support/direct/en/statistics/url-tags) · [URL tags (RU)](https://yandex.ru/support/direct/ru/statistics/url-tags) · [yclid 自动标记公告](https://yandex.ru/adv/news/avtomaticheskaya-razmetka-ssylok-v-direkte)
- **Click ID**：`yclid` —— 2019-12 起自动追加。官方定位为**备用**归因：优先用绑定的 Metrica 计数器数据，该字段为空时才用 yclid 回溯。**URL 若超过 4096 字节，只有 `yclid` 和 openstat 的值会被传递，其他参数被丢弃。**

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| 广告 ID | `{ad_id}` / `{banner_id}` | 广告 | 两者等价 |
| 活动名 | `{campaign_name}` | 活动 | ≤255 字符 |
| 活动名（拉丁转写） | `{campaign_name_lat}` | 活动 | ≤255 |
| 活动类型 | `{campaign_type}` | 活动 | `type1`=EPK 统一效果活动；`type2`/`type3`/`type4` 已不再支持；`type6`=搜索横幅 |
| 活动 ID | `{campaign_id}` | 活动 | |
| 创意 ID | `{creative_id}` | 创意 | Ad Builder 创意 ID |
| 设备类型 | `{device_type}` | 点击 | `desktop`/`mobile`/`tablet` |
| 广告组 ID | `{gbid}` | 广告组 | |
| 关键词文本 | `{keyword}` | 关键词 | 仅 EPK 内文字图文广告或应用推广；不含否定词 |
| 关键词 ID | `{phrase_id}` | 关键词 | 同上 |
| 受众定向 ID | `{retargeting_id}` | 广告组 | |
| 出价调整 ID | `{coef_goal_context_id}` | 广告组 | |
| 匹配类型 | `{match_type}` | 点击 | **仅两个值**：`rm`=自动定向、`syn`=语义匹配 |
| 匹配到的词 | `{matched_keyword}` | 点击 | 官方注明"代替 `{match_type}` 使用" |
| 定向条件名 | `{adtarget_name}` | — | **官方标注已不再支持，建议删除** |
| 定向条件 ID | `{adtarget_id}` | — | |
| 位次 | `{position}` | 点击 | `0` = 展示在 YAN/外部网络；须与 `{position_type}` 配合 |
| 广告块类型 | `{position_type}` | 点击 | `premium`/`dynamic_places`/`other`/`none` |
| 展示位置 | `{source}` | 点击 | 网络投放=站点域名；Yandex 搜索=`none` |
| 网络类型 | `{source_type}` | 点击 | `search`/`context` |
| 地区名/ID | `{region_name}` / `{region_id}` | 点击 | |
| click id | `{yclid}` | 点击 | 也可手动写入 |

- **快速链接（sitelinks）特殊规则（官方注）**：`{campaign_id}` `{ad_id}` `{banner_id}` `{phrase_id}` 在快速链接中的值替换，**只有当广告本体 URL 中也含有这些同名参数时才被保证**。
- **自定义参数**：支持任意参数名；UTM 五标签（source/medium/campaign 必填）；`utm_content` 可用 `|` 或 `.` 拼多个宏，如 `utm_content={position_type}.{position}`。西里尔字符自动 UTF-8 编码。**`utm_source=yandex` 有可能被截断为 `ya`**（官方已知行为）。
- ⚠️ **`{addphrases}` 在当前 EN 与 RU 官方表中均不存在**（EN/RU 双版逐行核对）。搜索结果里的描述来自 OWOX 第三方旧文档，疑为已下线的历史参数。第三方流传的"`{keyword}`+`{phrase_id}`+`{retargeting_id}` 同时用会丢值"官方无此警告。

### Naver Search Ads —— ⚠️ 机制根本不是宏
- **来源**：[네이버 검색광고센터官方公告转载（页尾标注 출처: 네이버 검색광고센터）](https://m.diad.co.kr/Customer/NoticeView?idx=3165) · [Wisetracker 官方文档](https://document.wisetracker.co.kr/tracking-management/media_partner-management/major-media_partner/naver/search-ads.md)
- ⚠️ `help.searchad.naver.com` / `searchad.naver.com` 被抓取工具黑名单拦截（HTTP 403），Chrome 工具超时，**无法引用 Naver 第一方页面**。
- **机制**：不是"广告主写宏模板"，而是**开关式** —— 在 `광고시스템 > 캠페인 수정 > 고급옵션 > 추적기능` 选「자동 추적URL 파라미터」后，Naver 在落地页 URL 上**自动追加**下列固定 query key。**全部小写 + `n_` 前缀 + 下划线，不是 `{}` 也不是 `__X__`，不存在模板占位符形态。**

| 参数 | 层级 | 说明 |
|---|---|---|
| `n_campaign_type` | 캠페인 | 캠페인 유형 |
| `n_ad_group` | 광고그룹 | |
| `n_ad_group_type` | 광고그룹 | |
| `n_media` | 매체 | 展示媒体/지면 |
| `n_ad` | 소재/광고 | 素材层 |
| `n_keyword` | 키워드 | 触发的注册关键词 |
| `n_keyword_id` | 키워드 | |
| `n_query` | 点击 | 用户实际检索词 |
| `n_match` | 点击 | **2023-09-18 新增**。`1`=일치 `2`=키워드 확장 `3`=연관 검색 `4`=일치(유사 검색어) `5`=스마트 블록 |
| `n_rank` | 点击 | 广告顺位 |
| `n_mall_pid` | 상품 | **仅 쇼핑검색 캠페인** |
| `n_mall_id` | 몰 | **仅 쇼핑검색 캠페인** |

数量（官方公告原文）：**파워링크 = 10 个**（原 9 + n_match）；**쇼핑검색 = 12 个**（原 11 + n_match）。

- **自定义参数**：「추적기능」下另有并列选项 `추적 경유 사이트`（tracking via-site URL），可填第三方跳转/归因链接（MAT 常用）。**Naver 未提供可插入的动态宏占位符。**
- ⚠️ **`n_campaign` 在官方清单里不存在** —— 只有 `n_campaign_type`。请勿使用。
- ⚠️ **Naver 无 click ID**（无 gclid/yclid 等价物）。`n_campaign_type` / `n_ad_group_type` / `n_media` / `n_rank` 的取值枚举官方未公布（只给了 `n_match`）。
- ⚠️ **Naver GFA（성과형 디스플레이광고）的 URL 宏完全未能证实。** Wisetracker GFA 官方指南通篇只讲「전환 Key 生成 + Wiselink 归因链接 + Deep Link/Landing URL 五字段」，无任何落地页 URL 宏列表。Airbridge 的 GFA 页当前为 "Translation in Progress" 空页。

### 百度广告
- **来源**：官方 URL通配符页 [dev2.baidu.com pageId=100230](https://dev2.baidu.com/content?sceneType=0&pageId=100230&nodeId=332&subhead=)（⚠️ **纯 JS 渲染，未能读到正文**）· [极诣（引用官方链接并列出已下线通配符）](https://maxket.com/ppc-url-macro-google-analytics/) · [cnblogs 转 jingyan.baidu.com 旧版逐条定义](https://www.cnblogs.com/microtiger/p/8496475.html) · [神策·百度搜索](https://manual.sensorsdata.cn/sensorsadstracking/docs/app_bdss) · [神策·百度信息流](https://manual.sensorsdata.cn/sensorsadstracking/docs/app_bdxxl) · 线上真实投放 URL 样本（豆包、夸克）
- **Click ID**：`bd_vid` —— **不是通配符**，是点击后自动追加到落地页的点击标识（每次点击唯一）。开通转化追踪后约 1.5 小时开始出现；装了追踪代码就会有 bd_vid，**不代表流量来自 oCPC 包**。（二手来源共识，官方页未能读取。）

**搜索推广（凤巢），`{}` 单花括号 + 小写**

| 宏字段 | 语法 | 层级 | 核实状态 |
|---|---|---|---|
| 推广计划 ID | `{planid}` | 计划 | 极诣正文 + 线上真实 URL 双重核实 |
| 推广单元 ID | `{unitid}` | 单元 | 线上真实 URL 核实 |
| 关键词 ID | `{keywordid}` | 关键词 | 全局唯一 ID；无对应时替换为 `0` |
| 关键词文本(UTF-8) | `{kw_enc_utf8}` | 关键词 | 传**触发的注册关键词，不是检索词** |
| 创意 ID | `{creative}` | 创意 | 全局唯一 ID |
| 匹配方式 | `{matchtype}` | 关键词 | 旧定义 `1`精确 `2`短语 `3`广泛；现行普遍表述 `3`=智能匹配（两说均为二手来源） |
| 设备 | `{device}` | 点击 | pc / mobile |
| 是否动态创意 | `{dongtai}` | 创意 | `1`=展现为动态创意 `0`=未展现 |
| 账户 ID | `{userid}` | 账户 | ⚠️ 仅 360 侧核实，百度侧未核实 |
| 触发标记 | `{trig_flag}`（推测） | 点击 | ⚠️ 仅从线上 URL 观察到 `a_trig_flag=nm` |
| 人群 ID | `{crowdid}`（推测） | 点击 | ⚠️ 仅从线上 URL 观察到 `a_crowdid=0` |

**使用规则（官方 5 条）**：① 仅关键词与创意的访问 URL / 移动访问 URL、附加创意中的 PC 与无线蹊径子链可用，**显示 URL 不支持**；② **严格区分大小写**（写 `{Creative}` 不替换）；③ 同一 URL 内重复插入同一通配符每处都替换；④ 错误通配符不替换；⑤ 连通性由广告主保证。

**搜索 vs 信息流的关键差异**
- **搜索**：`{}` 单花括号 + 小写 —— `{planid}` `{unitid}` `{keywordid}` `{creative}`
- **信息流**：`{{ }}` **双花括号 + 全大写** —— 已核实 `{{PLAN_ID}}`（计划）、`{{UNIT_ID}}`（单元）；`{{IDEA_ID}}`（创意）置信度较低
- **联调期特殊要求（两条线均适用，神策官方明文）**：百度渠道内部逻辑互斥，在「转化追踪/事件管理」联调工具里填 URL 时必须**手动把 `{}` / `{{}}` 改成双下划线 `__X__`**，如 `channel_ad_id={creative}` → `channel_ad_id=__creative__`；`{{UNIT_ID}}` → `__UNIT_ID__`。**正式投放必须换回。**

- **自定义参数**：支持 —— 等号左边参数名可完全自定义（真实样本用 `a_planid` `a_creative`），只有 `{}` 内的宏名必须严格照写。可与 utm_* 混用。
- ⚠️ **`{os}` / `{age}` / `{gender}` 在所有来源（旧版 jingyan 全表、极诣正文、线上真实 URL 样本）中均未出现，倾向判断为不存在。** 百度只有设备维度 `{device}`。
- ⚠️ **已下线的历史通配符（勿再使用）**：`{pagenum}` `{adposition}` `{mediatype}` `{placement}` `{bidurl}` `{haoci}` `{abtest}`。（`{adposition}` 旧值：`cl`/`clg`/`cr`/`mt`/`mb` + 排名，如 `cl3`；`{mediatype}` `1`=凤巢 `2`=网盟。）
- ⚠️ **`{groupid}` 不属百度** —— 百度用 `{unitid}`（单元），`{groupid}` 是 360 的。

### 360 广告（点睛）
- **来源**：[360 点睛开放平台 banner_update API（官方，`links` 字段示例含全套展示宏）](https://open.e.360.cn/displayapi/banner_update.html) · [360 营销学苑《使用URL通配符的正确姿势》](http://yingxiao.360.cn/optimizate/58047ee98fa7b.html)（参数表为图片，正文文字可读）· [代理商转载《360搜索推广url通配符使用说明》](https://m.qujiafen.com/h-nd-237.html) · [官方帮助中心目录](https://e.360.cn/static/help/list.html)
- **Click ID**：搜索侧未发现自动 click id。展示侧有 `{clickid}`（官方 API 示例中 `qhclickid={clickid}`），但它是广告主主动插入的宏，非平台自动追加。

**搜索推广（全部 `{}` 小写；官方"大括号内容为规定标识，不可改动"）**

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| 账户 ID | `{userid}` | 账户 | |
| 推广计划 ID | `{planid}` | 计划 | |
| 推广组 ID | `{groupid}` | 推广组 | ⚠️ 百度对应的是 `{unitid}`，**不可互换** |
| 创意 ID | `{creativeid}` | 创意 | ⚠️ 百度是 `{creative}` |
| 关键词 ID（哈希） | `{wordid}` | 关键词 | **CityHash64 单向加密，不可反解；不同推广组下同一关键词值完全相同 → 不唯一**。官方要求 `{groupid}`+`{wordid}` 或 `{creativeid}`+`{wordid}` 配对才能唯一定位。返回值可能为负数 |
| 关键词 ID（唯一） | `{keywordid}` | 关键词 | ⚠️ 与 `{wordid}` 语义冲突，见下 |
| 设备 | `{device}` | 点击 | `pc` / `mobile` |

**可添加层级（官方）**：创意链接 URL、关键词 URL、**比翼子链 URL**，PC 与 Mobile 均生效。

**展示广告 / 信息流（来自官方 API 请求示例）**
`{impression_id}` `{exchange_id}` `{source_id}` `{bannerid}`（**无下划线**）`{creativeid}` `{clickid}` `{query}` `{keywordid}` `{qaid}`

官方示例原文：
```
https://xxx.com?impression_id={impression_id}&exchange_id={exchange_id}&mvosr={source_id}&bannerid={bannerid}&creativeid={creativeid}&vn=1&qhclickid={clickid}&q={query}&keywordid={keywordid}&qaid={qaid}
```

**自定义参数**：官方明确"plan、group、creative、word、device 字段可以随意定义，系统不做限制，但通配符 `{planid}`、`{groupid}`、`{creativeid}`、`{wordid}`、`{device}` 需严格按格式填写"。

**360 vs 百度 8 点差异（均已核实）**：① 组层级 360=`{groupid}` / 百度=`{unitid}`；② 创意 360=`{creativeid}` / 百度=`{creative}`；③ 360 **不明文提供关键词**（只给 CityHash64 哈希 `{wordid}`），百度给 `{kw_enc_utf8}` 明文；④ 360 **没有** `{matchtype}`；⑤ 360 **没有** `{dongtai}`/`{crowdid}`；⑥ 360 搜索与展示统一 `{}` 小写，百度搜索 `{}` 小写 / 信息流 `{{}}` 大写 + 联调期换 `__X__`；⑦ 360 展示侧独有曝光/交易/点击链路宏；⑧ 360 有 `{userid}`，百度侧未核实。

- ⚠️ **`{wordid}` 与 `{keywordid}` 的关系两个来源直接矛盾**：360 营销学苑（2015 官方内容站）说 `{wordid}` 是 CityHash64 哈希、跨组不唯一；代理商转载（2022）用 `{keywordid}` 并说"不同组下同一关键词 ID 不同"。可能后期新增/替换，也可能两套并存。**需实测确认。**
- ⚠️ **`{keyword}`（明文关键词）在 360 侧未找到任何来源**。极诣明确指出"360 为了安全起见并未明文提供关键字"。倾向不存在。
- ⚠️ 360 官方帮助中心「URL通配符规则」章节正文为 `javascript:;` 折叠，营销学苑那篇的 3 张参数表为图片，均未能读取。上表「必填/选填」非官方原文标注。`{qaid}` 语义完全未知。

### 腾讯广告 / 广点通 (GDT) —— ⚠️ 架构与你的假设不同
- **来源**：[DataNexus 点击监测（现行权威宏表）](https://datanexus.qq.com/doc/develop/guider/interface/conversion/ad_track_click) · [曝光监测](https://datanexus.qq.com/doc/develop/guider/interface/conversion/ad_track_impress) · [user_id](https://datanexus.qq.com/doc/develop/guider/interface/user_id) · [旧版点击监测（含不可用字段清单）](https://developers.e.qq.com/docs/guide/conversion/new_version/dianjijiance) · [微信小程序 API](https://developers.e.qq.com/docs/guide/conversion/new_version/wechat_mini_program_api) · [自归因](https://datanexus.qq.com/doc/develop/intro/inner_app_intro/attribution/attribution_common_self) · [秒针·腾讯网页回传](https://tongji.cn.miaozhen.com/help/zh-hans/docs/mediaCallbackIntro/tencentWebCallback/tencentWebCallback.html)

**关键架构结论：腾讯的宏不在落地页 URL 上。** 两条独立链路 —— 宏用于点击/曝光**监测链接**（腾讯服务端 GET 你的服务器）；落地页上腾讯只自动追加一个参数。

| 场景 | 参数 | 样例 |
|---|---|---|
| 落地页 · 微信流量（朋友圈/公众号/小程序/小游戏/视频号） | `gdt_vid` | `wx07ptidwiwn5fde`（10–50 位） |
| 落地页 · 非微信流量（QQ/看点/优量汇） | `qz_gdt` | `xeq36xvpaaacqkzgegxa`（20 位） |
| 点击监测链接 | `__CLICK_ID__` | `24oi6xq2aaakvagnqu7a` |

实现顺序：先取 `gdt_vid`，取不到再取 `qz_gdt`。官方**不建议**把点击下发的 id 与 `gdt_vid` 直接匹配归因；如必须匹配，官方建议用 `gdt_vid` 对齐 `__REQUEST_ID__` / `__IMPRESSION_ID__`。

**点击监测链接宏（¹ = 仅见于旧版文档）**

| 分组 | 宏 |
|---|---|
| 上下文（必填） | `__CLICK_ID__` `__CLICK_TIME__`（秒级）`__CALLBACK__`（URL-encode，decode 一次后作 POST url） |
| 上下文（选填） | `__IMPRESSION_TIME__` `__AD_PLATFORM_TYPE__`(1=GDT 5=经微信MP投放 9=移动联盟SSP) `__PROCESS_TIME__` `__REQUEST_ID__` `__IMPRESSION_ID__` `__IP__` `__IPV6__` `__IP_MD5__` `__IPV6_MD5__` `__USER_AGENT__` |
| 结构（新版） | `__ADGROUP_ID__`（新版中这才是"广告 id"）`__ADGROUP_NAME__` `__DYNAMIC_CREATIVE_ID__` `__DYNAMIC_CREATIVE_NAME__` `__SMART_PROJECT_ID__` `__SMART_DYNAMIC_CREATIVE_ID__` |
| 结构（旧版） | `__CAMPAIGN_ID__` `__CAMPAIGN_NAME__`¹ `__AD_ID__`（实际是创意 id）`__AD_NAME__`¹ |
| **素材/创意层** | **`__CREATIVE_COMPONENTS_INFO__`**（JSON，被点击组件，**可能返回 AIGC 衍生素材**）**`__ELEMENT_INFO__`**（JSON，被曝光的全部素材）**`__MATERIAL_PACKAGE_ID__`**（素材标签 ID）`__AD_TYPE__`(1=普通 2=动态创意 7=动态元素) |
| 营销目标 | `__MARKETING_GOAL__` `__MARKETING_SUB_GOAL__` `__MARKETING_TARGET_ID__` `__MARKETING_CARRIER_ID__` `__MARKETING_SUB_CARRIER_ID__` `__MARKETING_ASSET_ID__` |
| 账户 | `__ACCOUNT_ID__`（**必填**）`__AGENCY_ID__` |
| 版位 | `__SITE_SET_NAME__`（`SITE_SET_MOMENTS`/`SITE_SET_WECHAT`/`SITE_SET_CHANNELS`/`SITE_SET_MOBILE_UNION`/`SITE_SET_SMART`）`__ENCRYPTED_POSITION_ID__`（**仅联盟白名单账户下发**） |
| 推广对象 | `__PROMOTED_OBJECT_ID__`（应用类必填；投放小程序时**不下发**）`__PROMOTED_OBJECT_TYPE__`(12=Android 19=iOS 43=线索 46=微信小游戏 1000=网页) `__BILLING_EVENT__`(1CPC 2CPA 3CPS 4CPM 5CPD) |
| 落地页 | `__PAGE_URL__`（官方推荐用于区分同广告下多落地页）`__DEEPLINK_URL__`(Android) `__UNIVERSAL_LINK__`(iOS) `__CLICK_SKU_ID__` |
| 搜索 | `__KEYWORD_ID__`¹ `__KEYWORD_TEXT__`¹ |
| 设备 | `__DEVICE_OS_TYPE__`(`ios`/`android`/`harmony`，应用类必填) **`__DEVICE_OS_VERSION__`**（**正确写法**）`__MODEL__` `__CHANNEL_PACKAGE_ID__`(Android) `__MUID__` `__HASH_ANDROID_ID__` `__HASH_OAID__` `__CAID__`（URL-encode JSON 数组，**推荐**）`__QAID_CAA__`（**2025-03-31 后停止新增**） |
| 微信 | `__WECHAT_OPEN_ID__`（**字段名 wechat_openid，宏多一个下划线**；公众号/企微不可用） |
| 实验 | `__BOOST_EXP_INFO__`¹ `__BOOST_MODEL_ID__`¹（小程序不可用） |

**必填汇总**：应用-Android = `__ACCOUNT_ID__ __CLICK_ID__ __CLICK_TIME__ __DEVICE_OS_TYPE__ __HASH_ANDROID_ID__ __HASH_OAID__ __MUID__ __PROMOTED_OBJECT_ID__ __CALLBACK__`；网页/小程序/公众号/企微/小游戏/快应用 = 仅 `__ACCOUNT_ID__ __CLICK_ID__ __CLICK_TIME__ __CALLBACK__`。

**曝光监测差异**：去掉 `__CLICK_ID__`/`__CLICK_TIME__`/`__CLICK_SKU_ID__`，换为 `__IMPRESSION_ID__`/`__IMPRESSION_TIME__`/`__IMPRESSION_SKU_ID__`，其余一致。

**转化回传**

| 项 | 值 |
|---|---|
| 唯一回传宏 | `__CALLBACK__` |
| 端点（旧/关闭鉴权） | `http://tracking.e.qq.com/conv?cb=xxx&conv_id=123` |
| 端点（新/开启鉴权） | `https://api.e.qq.com/v3.0/user_actions/add?cb=xxx&conv_id=123` —— **2025 Q3 全量强制** |
| 鉴权 Header | `access-token`（**中划线**）、`timestamp`、`nonce` |
| 无 callback 时 | POST body `trace.click_id`（与 `user_id` 二选一必填） |
| 去重 | `outer_action_id`（按 `user_action_set_id + outer_action_id + action_type`） |
| 归因方式 | `claim_type`：0点击 1关注 2曝光 3注册 4激活 5视频播放 6关键页浏览 7回流 |
| Web GET 回传 | `http://tracking.e.qq.com/conv/web?clickid=&action_time=&action_type=&link=`（link 需 urlencode 且域名与转化规则一致） |
| 错误码 | 20001 CB_CONTENT_ERROR / 20002 CONV_ID_ILLEGAL / 20006 DECRYPT_B64_CB_ERROR / 30000 API_ERROR |

**自定义参数（官方明文）**：示例 `https://xx.xx.com?planid=123&channel=ams&click_id=__CLICK_ID__`。约束：宏名全大写双下划线；**不能含 `#`**；不占用平台参数名；必须 http/https + 正式域名，**不能用 IP**；https 时**不支持 SNI**。转化生效后**只允许改宏不允许改域名**。**未找到任何官方长度上限规定。**

**微信专属**：小程序落地页只带 `gdt_vid`。两条归因路径：(a) 点击下发 → 回传 `click_id` + `wechat_openid`；(b) 落地页 → 回传 gdt_vid 中的 traceid 作为 clickid。**小程序不可用宏**：`hash_android_id`/`hash_oaid`/`muid`/`ip`/`ipv6`/`qaid_caa`/`user_agent`/`boost_*`。

### 巨量引擎 / 抖音广告
- **来源**：[星图《星广联投任务监测服务说明》（官方，含宏格式规范）](https://www.xingtu.cn/help-center/demander/138287) · [AppsFlyer 官方预置巨量归因链接](https://support.appsflyer.com/hc/zh-cn/articles/115003019403) · [神策宏总表（`__CSITE__` 全量枚举）](https://manual.sensorsdata.cn/sensorsadstracking/docs/qdtgjs) · [引力引擎 `__MID1__`~`__MID6__` 逐项含义](https://doc.gravity-engine.com/turbo-integrated/callback_url.html) · [新版回传 API 实测](https://www.cnblogs.com/feixiablog/p/18561951)
- ⚠️ 权威页 `https://event-manager.oceanengine.com/docs/8650/track_url_doc` 为 SPA，**未能抓到正文**。下表由官方星图页 + AppsFlyer 官方 + 神策 + 引力交叉核实。
- **官方宏格式规范**：`__参数__` 左右各两下划线，**必须全大写**否则不替换。链接前缀须 `https://XXX.XXX.com?`，域名需同时支持 IPv4 & IPv6，**不能是下载链接**，总长 ≤ 10K。非法字符：孤立 `%`、空格、path 中连续 `//`。
- **Click ID**：落地页自动追加 `clickid`（**有效期 21 天**）。注意 `__CLICKID__`（落地页自动注入）与 `__CALLBACK_PARAM__`（监测链接主动埋的回传凭证）是**两套东西**。

| 分组 | 宏 |
|---|---|
| 账户 | `__ADVERTISER_ID__` |
| 升级版结构 | `__PROJECT_ID__` `__PROJECT_NAME__` `__PROMOTION_ID__` `__PROMOTION_NAME__` |
| 旧版结构 | `__CAMPAIGN_ID__`/`__CAMPAIGN_NAME__`（旧版第2层，广告组）`__AID__`/`__AID_NAME__`（旧版第3层，**广告计划，不是 campaign**） |
| 创意 | `__CID__` `__CID_NAME__` **`__CTYPE__`**（创意样式：2小图 3大图 4组图 5视频）|
| **素材层（全行业最细）** | **`__MID1__`** 图片素材 ID · **`__MID2__`** 标题素材 ID · **`__MID3__`** 视频素材 ID · **`__MID4__`** 搭配试玩素材 ID · **`__MID5__`** 落地页素材 ID · **`__MID6__`** 安卓下载详情页素材 ID |
| 流量 | `__CSITE__` `__UNION_SITE__`（穿山甲广告位） |
| 点击 | `__REQUEST_ID__` `__TS__`（**13 位毫秒，不是 `__TIMESTAMP__`**） |
| 设备 | `__OS__`(0Android 1iOS 2WP 3Others) `__MODEL__` `__SL__` `__UA__` `__IP__`（**混合下发 IPv4/IPv6，官方建议改用具体宏**）`__IPV4__` `__IPV6__` `__IMEI__`/`__IMEI_MD5__` `__OAID__`/`__OAID_MD5__` `__ANDROIDID__`（曝光链接变体 `__ANDROIDID1__`）`__ANDROIDID_MD5__`(Android 8+) `__IDFA__`/`__IDFA_MD5__` `__CAID_MD5__`（**JSON 格式** `[{"caid_md5":"…","version":"20230330"}]`）`__CAID2__`(20201230 版) |
| 回传 | `__CALLBACK_PARAM__`（API 回传**必填**）`__CALLBACK_URL__` `__CONVERT_ID__`（宏名已证实，官方定义未证实） |
| 星图 | `__DEMAND_ID__`（19 位任务 ID）`__ITEM_ID__` |

**`__CSITE__` 版位枚举**：头条 1–10000 / 80000–110001；西瓜 10001–10099；火山 30001–30099；**抖音 40001–40099**；番茄 26001–26099；穿山甲开屏 800000000；穿山甲网盟 900000000；通投 33013；**搜索 38016**。

**AppsFlyer 官方预置巨量点击链接（一手宏拼写参照）**
```
?pid=bytedance_int&af_siteid=__UNION_SITE__&af_c_id=__PROJECT_ID__&af_channel=__CSITE__&af_ad=__CID_NAME__&af_ad_id=__CID__&af_sub1=__MID1__&af_sub2=__MID2__&af_sub3=__MID3__&af_sub4=__MID4__&af_sub5=__MID6__&af_adset=__PROMOTION_NAME__&af_adset_id=__PROMOTION_ID__&af_r=__MID5__&clickid=__CALLBACK_PARAM__&md5_android_id=__ANDROIDID__&imei=__IMEI__&oaid=__OAID__&md5_oaid=__OAID_MD5__&os=__OS__&af_ip=__IP__&af_ua=__UA__&af_lang=__SL__&af_model=__MODEL__&convert_id=__CONVERT_ID__&request_id=__REQUEST_ID__&idfa=__IDFA__
```

**转化回传（神策明确"事件管理（建议）/ 转化追踪（将下线）"）**

| | 转化追踪（旧，GET） | 事件管理（新，POST JSON） |
|---|---|---|
| 端点 | `https://ad.oceanengine.com/track/activate/?callback=xxx&event_type=x` | `https://analytics.oceanengine.com/api/v2/conversion` |
| callback 来源 | `__CALLBACK_PARAM__` 实际值 | 落地页 query 的 `clickid` |
| event_type | 0激活 1注册 2付费 6次日留存 | body `event_type`（字符串，如 `form`） |
| 金额 | `props={"pay_amount":"1000"}` **单位分** | |
| body | — | `{"event_type":"form","context":{"ad":{"callback":"<clickid>"}},"timestamp":<毫秒>}` |

**与海外 TikTok 的差异（关键陷阱）**：`__AID__` 在 TikTok = ad set ID，在国内 = **广告计划 ID**；`__CID__` TikTok = ad/creative，国内 = 创意。**跨平台复用模板会串层级。** TikTok 有 `__GAID__`/`__PLACEMENT__`、click id 为 `ttclid`；国内无 GAID，用 `__CSITE__`（数字版位，粒度细得多）、click id 为 `clickid`；`__MID1__`~`__MID6__` 是国内独有。

⚠️ **搜索广告**：唯一已核实的是 `__CSITE__=38016`。`__KEYWORD__`/`__QUERY__`/`__KEYWORD_ID__`/`__MATCH_TYPE__` **在所有来源中均未出现**；神策宏总表中巨量的 keyword 列为空（百度列有 `{{WORDID}}`）。倾向结论：**巨量监测链接不下发关键词宏**，需用 UTM 或报表 API。
⚠️ **`__AD_FORMAT__` / `__INTEREST__` 不存在**（3 份含完整宏表的来源均无）。形态维度请用 `__CTYPE__`。

### 快手 / 磁力引擎
- **来源**：[官方 DSP-IAA](https://open.kuaishou.com/miniGameDocs/operation/DSP/DSP-IAA) · [官方线索类 API 归因](https://docs.qingque.cn/d/home/eZQDnexll3-ebbtlX3xEDvBN3) · [官方应用下载类](https://docs.qingque.cn/d/home/eZQCUW5cBE39_ZlarHp_BWWhP) · [Adjust 官方 partner 模板 + event_type 全枚举](https://help.adjust.com/en/article/set-up-kuaishou-domestic) · [官方文档原文转载](https://www.kuai-ad.com/jd/3350.html) · [官方品牌监测 MMA 标准](https://www.kuai-ad.com/jd/5233.html) · [官方 FAQ](https://www.kuaishouad.cn/new/162.html)
- **Click ID**：`callback`。落地页链接 / 小程序 deeplink 由系统**自动拼接**；小程序 `ks.getLaunchOptionsSync().query.callback`（仅商业化链路有）。加密串 < 1K，对每用户唯一不变。第三方监测链接场景必须手写 `__CALLBACK__`。

**DSP 效果广告宏**（全大写 + 双下划线，≤10K，仅 https，不能是下载链接，域名需支持 ipv4&ipv6）

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| 账户 ID | `__ACCOUNTID__` | 账户 | **中间无下划线，不是 `__ACCOUNT_ID__`** |
| 计划 ID | `__DID__` | campaign | |
| 计划名 | `__DNAME__` | campaign | ⚠️ 官方正文写作 `__Dname__`（混合大小写，与"必须全大写"规则冲突，属官方笔误） |
| 广告组 ID | `__AID__` | unit | |
| 创意 ID | `__CID__` | 创意 | 示例 `223372032123415808` —— **超 int32，必须按 int64 存** |
| 回调地址 | `__CALLBACK__` | — | **必填**；官方：不可写成 `__CALL_BACK__` |
| 设备 | `__IMEI2__`(小写后md5) `__OAID__`(**原值，不需MD5**) `__OAID2__` `__IDFA2__`(大写后md5) `__ANDROIDID2__`(小写后md5) **`__ADVERTISIINGID2__`**(GAID md5 —— ⚠️ **拼写就是 ADVERTISIING，多一个 I，快手官方拼写错误，必须原样使用**) `__MAC2__` | 设备 | |
| 环境 | `__IP__` `__UA__` | — | |

**品牌广告监测（MMA 标准，独立宏池）**：`__OS__` `__UA__` `__IP__` `__TS__`（毫秒）`__GEO__` `__BDID__`（快手 did，64 位 hex）。监测事件：展示 / 点击（异步）/ 播放 / 有效播放 / 播完。

⚠️ **DSP 有宏白名单校验。** 官方 FAQ 原文："不能使用不在列表里面的占位符，比如：`__OS__`"。这是强证据 —— `__PLATFORM__`/`__OS_VERSION__`/`__GENDER__`/`__AGE__` 若填入会**直接校验失败**。

**转化回传**：`GET https://ad.partner.gifshow.com/track/activate?event_type=1&event_time=<13位毫秒>&callback=<原值>`。返回 `{"result":1}` 成功。必须用下发的**完整原值**，否则报 `callbackinfo decoded failure`。付费传 `purchase_amount`；关键行为传 `key_action_category` + `key_action_threshold`。
event_type：1激活 2注册 3付费 7次留 8七留 10完件 11授信 12商品浏览 13加购 14提交订单 15付款成功 39人脸识别 40身份信息 41银行卡 42补充个人信息 43课程试听 44有效线索 69教育正价课 79用信 143关键行为。

**自定义参数**：支持，快手"上报时原样返回，不做任何修改"。小游戏可在广告组「启动参数」填 `aaaa=bbbb`。官方落地页示例：`https://www.test.com?utm_source=kuaishou&aid=__AID__&cid=__CID__&did=__DID__&dname=__Dname__`
**创意层监测**：官方明确"创意层级的监测作为广告相关信息下发，**不影响归因**" —— 与转化归因是两条链路。
⚠️ **磁力金牛（电商）未能证实**：`niu.e.kuaishou.com` 无 SSR / 需登录。

### 知乎广告
- **来源**：[官方 PDF《应用下载API转化追踪文档5》V3.2.2, 2020-06-30, 知乎商业团队](https://zhstatic.zhihu.com/commercial/bidding/应用下载API转化追踪文档5.pdf) · [官方 PDF《落地页转化追踪文档》V2.1, 2019-12-10](https://aliyun-resource.helplook.net/docker_production/hms4d9/article/63dNp2UA/attachments/落地页转化追踪文档.pdf) · [神策](https://manual.sensorsdata.cn/sensorsadstracking/docs/app_zh)
- **宏形式（官方原文）**：「宏参数均为大写，且参数前后均为两个连续的英文字符下划线」。**知乎全部使用 `__XXX__`，不存在 `{xxx}` 语法。**
- **Click ID**：**知乎没有自动追加的 click id。** 必须手写 `__CALLBACK__`，回调地址内自带 `si`（请求唯一 ID）与 `cid`（创意 ID）。

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| Android 设备 ID | `__IMEI__` | 设备 | **原值小写后 md5**，不支持原值 |
| OAID | `__OAID__` | 设备 | 原值 |
| AndroidID | `__ANDROIDID__` | 设备 | 原值小写后 md5 |
| iOS 设备 ID | `__IDFA__` | 设备 | **原值大写后 md5**，不支持原值 |
| 请求唯一 ID | `__SESSIONID__` | 请求 | uuid |
| 回调 URL | `__CALLBACK__` | — | **回传必填**，urlencode |
| 用户 IP | `__IP__` | 用户 | |
| UA | `__UA__` | 用户 | urlencode；**知乎会向 UA 添加「zhihu」信息** |
| 设备类型 | `__OS__` | 设备 | **Android=0，iOS=1** |
| 计划 ID | `__CAMPAIGN__` | 计划 | ⚠️ **不是 `__CAMPAIGN_ID__`** |
| 创意 ID | `__CREATIVE__` | 创意 | ⚠️ **不是 `__CREATIVE_ID__`** |
| 时间戳 | `__TS__` | — | **UTC 秒级** |

⚠️ **必带参数 `zhs2s=1`**：非友盟/AppsFlyer/Talkingdata 的第三方监测链接**必须包含 `zhs2s=1`**。知乎 2024-01 升级 API 监测链接，老链接需在尾部加 `&zhs2s=1`。
⚠️ **落地页 CALLBACK 参数名必须是 `cb`**：`cb=__CALLBACK__`；一个落地页链接**只能有一个 `?`**；实际投放的落地页也必须包含该参数。

**转化回传**：`https://sugar.zhihu.com/plutus_adreaper_callback?si=…&cid=…&event=__EVENTTYPE__&value=__EVENTVALUE__&ts=__TIMESTAMP__`
- `__EVENTTYPE__` 必填（多事件分次发送）；`__TIMESTAMP__` 必填**秒级**（为空取收到日志时间）
- ⚠️ **`__VALUE__` vs `__EVENTVALUE__` 官方文档自相矛盾**：宏替换规则表写 `__VALUE__`，callback URL 模板与全部示例写 `value=__EVENTVALUE__`。**两份 PDF 均有此矛盾。实施以 callback URL 中实际下发的 `__EVENTVALUE__` 为准。**
- EVENTTYPE — APP：`install`/`reged`/`payment`/`next_retain`/`key_behavior`（V3.1 起不再支持 `sale`）。落地页/小程序：`api_submit`/`api_ask`/`api_call`/`api_buy`/`api_view`/`api_get_cust`/`api_pay`。
- **联调 vs 真实环境差异**：联调下 AndroidID 为**原值**（非 md5）；`__OS__` 下发字符串 `ios`/`android`（真实为 `1`/`0`）；**IP 和 UA 联调不下发**。归因窗口默认 7 天点击 + 1 天曝光。

⚠️ **`{position}` 不存在。** 知乎不用花括号语法，官方全表中无任何版位/位置类宏。

### UC 广告 / 阿里汇川 —— ⚠️ 最重要的结构性发现
**阿里体系有两套完全不同方向的宏，市面上经常被混为一谈：**

| | 方向 | 语法 | 公开程度 |
|---|---|---|---|
| **东风 Dongfeng**（`tanx.com`） | 媒体/流量方 → 阿里妈妈上报 | `__XXX__` | **完整公开** |
| **超级汇川转化追踪**（广告主侧，`e.uc.cn`） | 汇川 → 广告主落地页；广告主 → 汇川回传 | `uctrackid`/`clickid`，创意层 `{UCTRACKID}` | **不公开，需登录后台** |

- **来源**：[官方东风监测链接说明（唯一公开完整宏表）](https://g.alicdn.com/mm/media/df/doc/tracking/details.html) · [官方转化追踪手册全文转载](https://www.uc-ad.com/jd/572.html) · [神策·阿里汇川](https://manual.sensorsdata.cn/sensorsadstracking/docs/app_alhc)
- **Click ID**：`uctrackid` —— 汇川自动向该账户下**全部落地页 URL** 追加，无需写宏。由数字、字母、`%` 组成。广告主须保证转化发生时值不变、回传时原样带回。首次使用需在后台确认「信息追加」条款。搜索/卧龙侧同义字段为 `clickid`。

**东风监测宏（`__XXX__`；替换内容包含下划线；除宏替换外不得修改或转码链接任何字符，否则加密校验失败）**

| 位 | 宏字段 | 语法 | 必填 | 备注 |
|---|---|---|---|---|
| a1 | 客户端真实 IP | `__IP__` | 必填 | 支持 IPv4/6；**不可为私有网段** |
| a2 | OS | `__OS__` | 移动端必填 | iOS=1, Android=2 |
| a3 | IDFA 明文 | `__IDFA__` | iOS 可获取时必填 | 36 位带连字符大写 |
| a4 | IMEI 原值 | `__IMEI__` | 与 md5 二选一 | |
| a5 | IMEI md5 | `__IMEI_MD5__` | 与原值二选一 | 32 位 |
| a6 | OAID | `__OAID__` | 可获取时必填 | 明文 |
| a7 | MAC | `__MAC__` | **OTT 必填** | 加密前去分隔符 + 转大写 |
| a8 | UA | `__UA__` | 必填 | **优先取 WebView UA**；取不到则不回传，禁止自定义 |
| a9 | 时间戳 | `__TS__` | 必填 | **秒级整数** |
| a17 | AndroidID | `__ANDROIDID__` | 选填 | |
| a26 | 阿里 AAID | `__ALI_AAID__` | iOS 可获取时必填 | 需集成阿里 SDK |
| a27 | 中广协 CAID | `__CAID__` | iOS 可获取时必填 | `版本号_值`，无版本号用 `0`；多个用 `,` 拼接后整体 URLEncode |

官方链接样例：曝光 `https://ef-dongfeng.tanx.com/nim?e=…&k=106&a1=__IP__&a2=__OS__&…`；点击 `https://ef-dongfeng.tanx.com/ncm?e=…`；H5 点击 `https://click.tanx.com/tfn?e=…&u=<落地页urlencode>&k=140&ext=a%3d__IMEI__%26b%3d__IDFA__…`
**限制**：点击监测链接最大 **500 字符**。设备号取不到时**禁止填默认值**（`null`/`0`/`02:00:00:00:00:00` 一律按无效流量过滤）。**东风无 campaign/adgroup/creative id 宏、无 click_id 宏、无 callback 宏** —— 广告位信息编码在加密的 `e=` 参数里。

**转化回传（汇川广告主侧不用 callback 宏机制）**：网页 JS/HTML 代码（**落地页及二/三级页每级都必须装**基础代码）/ 网页 API（回传 URL 必须完整携带 `uctrackid`）/ 应用 API（联调需 UC 浏览器扫码授权）/ 应用 SDK（GismSDK：`init/onLaunchApp/onEvent/onExitApp`，事件 `onRegisterEvent/onPayEvent/onRoleEVent/onUpgradeEvent/onCustomEvent`，`getOaid()` 避免与信通院 SDK 冲突）。转化与 **5 天内**的点击拼接。
**多落地页优选**：单计划最多 5 个落地页；官方说明"每个页面都追加上组/计划/创意 ID"，**但具体宏 token 名官方未给出**。
**关系澄清**：汇川 = 阿里妈妈效果广告平台，现名「超级汇川」(`yingxiao.uc.cn`，后台 `e.uc.cn`)，覆盖 UC 浏览器/UC 头条/神马搜索/优酷/豌豆荚。卧龙 = 原神马搜索系统，2021 并入。**东风是媒体接入侧，不要混用其宏。**
⚠️ **超级汇川广告主侧完整宏表不存在公开文档。** `uctrackid={UCTRACKID}` 创意层宏语法多个第三方一致引用但官方原文未抓到。**是否存在 `__CLICK_ID__` 之类双下划线宏：无任何证据，不要假设与东风相同。**

### 微博广告 / 粉丝通
- **来源**：[官方开发者文档目录（docsify，`#/path` → `.md` 可直取）](https://developers.biz.weibo.com/docs/_sidebar.md) · [track/guide](https://developers.biz.weibo.com/docs/track/guide.md) · [no_auth_activate](https://developers.biz.weibo.com/docs/track/no_auth_activate.md) · [auth_activate](https://developers.biz.weibo.com/docs/track/auth_activate.md) · [mark_info](https://developers.biz.weibo.com/docs/track/mark_info.md) · [monitor_list](https://developers.biz.weibo.com/docs/assets/monitor_list.md) · [官方《微博应用监测联调API对接文档 v1.7》PDF](https://aliyun-resource.helplook.net/docker_production/hms4d9/article/vHCDVmzT/attachments/微博应用监测联调API对接文档v1_7.pdf)

**Click ID —— 两个不同 ID，不要混淆**
- **`mark_id`** —— 落地页/网页场景，微博自动拼接。格式 `1_reallog_mark_ad:8|1_16000011273892000011273892`（urlencode 后 `4_reallog_mark_ad%3a8%7c4_…`）。**只允许 urlencode 一次**；302 跳转会自动再 encode，是 `markid format error (10012)` 的头号原因。可通过 `/v3/luming/mark-info` 反解出 AdId/CreativeId/CustomerId/Mid/TSID。
- **`IMP`** —— APP 激活场景。宏 `{IMP}`（新版 `__CALLBACK_PARAM__`），第三方必须原样带回。小程序场景用 `imp`。

**官方 v1.7 宏表（`{xxx}` 花括号，大小写敏感）**

| 宏字段 | 语法 | 必填 | 备注 |
|---|---|---|---|
| IMP | `{IMP}` | **是** | 激活回传必须原样带回 |
| idfa_md5 | `{idfa_MD5}` | iOS 激活必须 | 原串**大写带连字符** → MD5 → 再转大写 |
| imei_md5 | `{imei_MD5}` | Android 激活必须 | **字母转小写** → MD5 → 再转大写（**与 iOS 相反**） |
| oaid / oaid_md5 | `{oaid}` / `{oaid_MD5}` | Android 激活必须 | |
| androidid_MD5 | `{androidid_MD5}` | 否 | **仅支持安卓 8 以下替换** |
| mac_MD5 | `{mac_MD5}` | 否 | 转大写后 MD5 |
| ip / ipv4 | `{ip}` / `{ipv4}` | 强烈建议 | `{ip}` **优先下发 IPv6** |
| ua | `{ua}` | 强烈建议 | URLEncode；**联调阶段不下发 ua** |
| clicktime | `{clicktime}` | 否 | **13 位毫秒** |
| devicetype | `{devicetype}` | 否 | `android`/`ios` |
| osversion | `{osversion}` | 否 | 如 `android4.4.4`、`ios11.4.1` |
| MODEL | `{MODEL}` | 否 | 如 `vivovivo+X21` |
| RY_CAID | `{RY_CAID}` | 否 | 热云 CAID。**旧宏 `{CAID}` 已作废，会被替换为空** |
| GX_CAID | `{GX_CAID}` | 否 | 中广协 CAID，`ver_caid,ver_caid`，每次传两个（最新版+上一版） |
| ali_aaid | `{ALI_AAID}` | 否 | |
| customer_id | `{CUSTOMER_ID}` | 否 | 广告主层 |
| campaign_id / name | `{CAMPAIGN_ID}` / `{CAMPAIGN_NAME}` | 否 | 系列层 |
| ad_id / name | `{ad_id}`（**小写**）/ `{AD_NAME}`（大写） | 否 | 计划层 |
| creative_id / name | `{creative_id}`（**小写**）/ `{CREATIVE_NAME}`（大写） | 否 | 创意层 |
| mark_id | `mark_id=` | 平台自动追加 | 网页场景无需写宏 |

官方点击监测链接模板：
`http://adv.com?campaignid=xxx&ip={ip}&clicktime={clicktime}&idfa_md5={idfa_MD5}&IMP={IMP}&ad_id={ad_id}&creative_id={creative_id}&devicetype={devicetype}&osversion={osversion}&caid={GX_CAID}`

官方使用建议：安卓务必同时加 `imei_md5`+`oaid`+`androidid_MD5`（命中任一即回传）；加 `ip`(或 `ipv4`)+`ua` 做模糊归因；iOS 14+ 无 IDFA 时用 RY_CAID / GX_CAID / ALI_AAID 三选。

**新版 `__XXX__` 双下划线宏**（从 `/v3/ads/monitor_list` 官方应答示例逆向观测，`gateway.biz.weibo.com` 短链中两代语法混用）：`__OSVERSION__` `__IPV4__` `__TS__` `__IMEI__` `__CALLBACK_PARAM__`(=IMP) `__OAID_MD5__` `__ANDROIDID__` `__MODEL__` `__IDFA_MD5__` `__CAID__` `__UA__`。⚠️ **该语法未见于任何官方宏定义表，以 v1.7 的 `{xxx}` 表为准，双下划线仅作对照。**

**转化回传 A —— 落地页/网页/小程序**：`/v4/track/activate`（免鉴权）、`/v3/track/activate`（鉴权 `Authorization: Bearer TOKEN`），GET
`time`（必填 13 位毫秒）`mark_id`（**只 urlencode 一次**；为空计自然量）`behavior`（必填：1001表单提交 / 1007商品购买 / 2001付款订单商品数 / 3002注册(小程序) / 3003付费 / 3004微信关注）`imp`（小程序必填，urlencode）`paid_amount`（behavior=3003，元）`score`（behavior=1001，意向度 5/4/3/2，1=负向）`technical_provider`（用三方服务时必填，**未填影响结算**）`item_order_pay`（behavior=2001 必选，urlencode(JSON)）
**深浅层强制绑定**：回传深层必须同时回浅层 —— 2001→1007、3003→3002。

**转化回传 B —— APP 激活**：`GET https://appmonitor.biz.weibo.com/sdkserver/active`
`company`（必填，联调后台分配，**分配后不可修改**）`IMP`（必填原样）`action_type`（1激活 2下单 3注册 4付费 7次留 8app内访问；**激活+后续行为需回传两次**）`price`（action_type=4，元）`active_time`（十位）+ 归因用的设备参数。
返回成功 `{"result":"OK","Code":"0"}`；新版 track API 返回 `{"code":0,"message":"OK"}`，建议打印响应头 `X-OPEN-TRACEID` 排障。

**服务器白名单（官方必做）**：需放行微博出口 IP `123.125.25.145-149`、`123.125.25.22-26`、`39.156.11.16-20`、`39.156.11.36-40` 等。
**自定义参数（官方明文）**：`campaignid` 定义为"广告主（第三方）自定义的监测 id，与微博无关…参数名自定"。**约束：值必须是数字或字母，特殊字符可能报错。**
⚠️ **你原清单里的微博曝光宏 `__IP__ __TS__ __OS__ __IDFA__ __MAC__` 实际上是阿里妈妈东风的宏，不是微博的。** 微博官方是 `{ip} {clicktime} {idfa_MD5}` 花括号族。**微博官方开发者文档目录中没有曝光监测章节**，曝光宏规范未找到任何微博官方文档。

### 小红书聚光平台 —— ⚠️ 你的 1 个参数不是漏配，是平台上限
- **来源**：[转载《聚光广告平台-第三方监测功能升级》官方通知（2024-01-06）+ 对接手册](https://www.xiao-ad.com/jd/1071.html) · [转载《客资收集API对接》产品文档](https://www.xiao-ad.com/jd/1115.html) · [神策](https://manual.sensorsdata.cn/sensorsadstracking/docs/web_xhs) · [真实链接示例 + 回传 curl](https://attritouch.com/blog/china-ad-attribution-system-guide)
- **宏形式**：`__XXX__`（双下划线大写）。**不是 `{{}}` 也不是 `$$`。**
- **Click ID**：新链路 `click_id` / clickId，跳转落地页时**自动拼接**。旧链路 `track_id`，**2024-02-29 已下线**。联调环境 click_id 以 `atest` 开头，数据不进报表。生产值形如 `Mdo9fK5B62TSkrqg3fE082PYcu24bE-PkDGS6PNDKeMaMRM`。

**已核实宏列表 —— 公网可核实的全部，只有 7 个**

| 宏字段 | 语法 | 层级 | 备注 |
|---|---|---|---|
| Click ID | `__CLICK_ID__`（落地页外链由平台自动拼 `click_id=`） | 点击/创意 | 新链路唯一归因键 |
| OAID | `__OAID__` | 设备 | |
| OAID MD5 | `__OAID_MD5__` | 设备 | 监测链接下发的一般是 MD5 |
| 广告类型/场域 | `__PLACEMENT__` | 创意/账户 | **2024-01-06 新增**，区分信息流/搜索/视频流/全站智投 |
| 内容 | `__CONTENT__` | 创意 | **C2S 场景必须去掉**，否则报「监测链接非法」 |
| RED ID | `__RED_ID__` | 用户 | **平台默认不支持**，敏感参数必须删除否则报错 |
| CAID / CAID MD5 | `__CAID__` / `__CAID_MD5__` | 设备 | **平台默认不支持**，同上 |

**三方监测能力（官方通知原文）**
- 监测维度：**账户、创意两个层级**（⚠️ **不是** campaign/unit/creative 三层）
- 监测内容：曝光、点击；方式 **C2S**；类型**仅支持异步监测**
- 域名必须正式域名（不接受 IP / 下载链接）且**需提前加白**（销售提交邮件 + OA 申请）
- **参数只能在小红书已有的参数中选**，用 `&` 分隔
- 配置入口：创意监测 = 新建创意时逐条添加；账户监测 =「工具-账户工具-账户三方监测」（只需加一次，**数据不可拆分到创意**）
- 报错：【监测链接非法】= 含空格/字段拼错/域名未加白；【敏感参数】= 含 `__RED_ID__`/`__CAID__`/`__CAID_MD5__`

**转化回传**：`POST https://adapi.xiaohongshu.com/api/open/conversion`，body 必传 `click_id`、`advertiser_id`（**多账号时须用品牌账号 ID**）、`event_type`（如 411=App激活）、`scene`（如 701）、`timestamp`（毫秒）、`os`、`platform`；选填 `caid1_md5`。
⚠️ **硬约束：回传时间超过 1 小时即判「回传超时」。**

**自定义参数**：支持手工拼**自己的固定参数**（如 `channel=小红书聚光`）。但**动态宏只能从已有参数中选，不能自造**。官方 FAQ 明确：**新链路目前不支持下发其他宏参数，只拼接 clickID**。
⚠️ `__IP__` `__UA__` `__TIMESTAMP__` `__IMEI__` `__IDFA__` `__MODEL__` `__CAMPAIGN_ID__` `__UNIT_ID__` `__CREATIVE_ID__` `__NOTE_ID__` **在所有来源中均未出现，不做推测**。你要的 campaign/unit/creative 层级宏，**公网无证据表明存在**；报表侧可按单元/创意/关键词粒度看回传事件，但那是报表维度不是 URL 宏。
⚠️ **蒲公英/千帆/小红星/乘风的追踪参数完全未找到可核实技术文档。**

### CG 联盟 / AiFu 联盟 —— ❌ 找不到，不编造
用 6 组查询组合检索，**没有任何一条结果指向名为「CG联盟」或「AiFu联盟/爱扶联盟/爱付联盟」的实体**。搜索引擎持续把 "CG" 纠偏成 CJ (Commission Junction)，说明这两个名字在中文公开语料中几乎无索引。符合"小型联盟只在注册后后台提供文档、或 IM 私发 PDF"的特征。

**替代：联盟营销通用惯例（每条均来自实际抓取的标准文档）**

**A. TUNE / HasOffers**（多数国产联盟系统是其克隆）—— [Partner Sub-IDs and Macros](https://support.tune.com/hc/en-us/articles/1500008230302-Partner-Sub-IDs-and-Macros)
`offer_id`{offer_id} · `aff_id`{affiliate_id}/{partner_id} · **`aff_click_id`（渠道侧唯一 click ID，唯一值必须放这里）** · `aff_unique1`–`5` · `aff_sub`, `aff_sub2`–`5`（**只放非唯一值**；≤500 字符需 URL-encode。把唯一值塞进 aff_sub 是报表变慢的最常见原因）· `source`{SOURCE} · **`transaction_id`（回传/postback 主键）** · `amount` · `redirect`/`eredirect`（含 query string 时用后者）· 设备 `google_aid`/`google_aid_sha1`/`ios_ifa`/`ios_ifa_sha1`/`ios_ifv`/`windows_aid`/`unid` · 其他 `file_id`(素材)/`url_id`/`random_url`/`url`(deeplink)/`payout`/`ad_id`/`user_id`

**B. Affise**（`{}` 单花括号）—— [help-center.affise.com/6474898](https://help-center.affise.com/en/articles/6474898)
出向：`{clickid}`/`{click_id}`（**唯一强制宏**）`{pid}` `{offer_id}` `{ip}` `{geo}` `{sub1}`–`{sub8}`（高版本至 `{sub30}`）`{account_sub1/2}` `{deeplink}` `{device_ua}` `{rand}` `{time}` `{city}` `{os_version}` `{device_model}` `{fbclid}` `{impression_id}`
入向 postback：`{transactionid}` `{sub1}`–`{sub8}` `{status}`(1批准/2待定/3拒绝/5冻结) `{sum}` `{goal}` `{currency}` `{click_date}` `{uagent}` `{ext1}`–`{ext3}` `{custom_field1}`–`{custom_field7}`
⚠️ **官方明确警告：postback 没有 clickid 宏，回传时必须用 `{sub1}`–`{sub8}` 承载 click id。混用直接导致追踪失败。** sub 上限 255 字符。

**C. HugOffers**（中文联盟系统，参数命名最接近国产小联盟）—— [support.hugoffers.com](https://support.hugoffers.com/hugoffers-reference-guide/untitled.md)
渠道侧：`offer_id` `aff_sub`（**渠道 click id**）`aff_pub` `aff_sub2`–`aff_sub6` `aff_lang` `payout` `idfa` `advertising_id` `ip` `android_id` `user_agent` `site_id` `os` `os_version` `device_model` `event_name`
广告主侧宏：`{click_id}` `{aff_id}` `{aff_pub}` `{offer_id}` `{advertising_id}` `{idfa}` `{caid}` `{oaid}` `{android_id}` `{site_id}` `{ip}` `{user_agent}` `{data2}` `{event}`

**D. AppsFlyer** —— [207447163](https://support.appsflyer.com/hc/en-us/articles/207447163)
`pid` `c` `af_siteid` `af_sub_siteid` `af_adset` `af_ad` `af_sub1`–`af_sub5` `clickid` `advertising_id` `oaid` `idfa` `af_ip` `af_ua` `af_android_url` `af_ios_url` `af_web_dp`

**拿到 CG/AiFu 后台时，确认这 3 件事即可覆盖 90% 对接**：① click id 参数名叫什么、是 `{}` 还是 `__X__`；② postback 里 click id 用哪个字段回（Affise 系是 sub1，TUNE 系是 transaction_id）；③ 有几个自由 sub 位、字符上限多少。

---

## 11. ⚠️ 判定为不存在 / 编造的宏 —— 必须从现有配置中删除

| 平台 | 你现有的宏 | 结论 | 正确替代 |
|---|---|---|---|
| Meta | `{{ad.format}}` | **不存在**（官方仅 8 个宏） | 无（Meta 无创意形态宏） |
| Meta | `{{creative.id}}` | **不存在** | `{{ad.id}}` |
| Meta | `{{publisher_platform}}` | **不存在** | `{{site_source_name}}` |
| Meta | `{{platform}}` | **不存在** | `{{site_source_name}}` |
| Meta | `{{product.id}}` | **不存在** | feed 的 `link` 字段自带参数 |
| Bing | `{Custom0}`…`{Custom8}` | **不是宏** —— 把"最多 8 个自定义参数"误记成固定宏名 | 自命名 `{_yourkey}`，上限 8（扩展 3/8），**无 0 索引** |
| Bing | `{IfContent:}` | **不存在**（MS 无 content 网络概念） | `{IfNative:}` |
| Bing | `{SitelinkId}` | **不存在** | `{feeditemid}` |
| Bing | `{ProductPartitionId}` | **不存在** | `{CriterionId}` / `{OrderItemId}` |
| Bing PMax | `{AssetGroupId}` | **官方明确不支持** | `{AdGroupId}` / `{AdGroup}` |
| TikTok | `__AD_FORMAT__` | **不存在** | 无 |
| TikTok | `__INTEREST_CATEGORY__` | **不存在** | 无 |
| TikTok | `__AGE__` `__GENDER__` | **不存在** | 无（TikTok 不通过 URL 宏回传人群维度） |
| TikTok | `__CLICKID__`（双下划线） | 官方写 `_CLICKID_`（单下划线） | `_CLICKID_` / 自动 `ttclid` |
| Snapchat | `{{creative.type}}` `{{ad.is.swipeable}}` | **极可能不存在**（无任何证据，命名风格也不符） | — |
| Pinterest | `{{campaignid}}` 双花括号 | **语法错误** | 单花括号 `{campaignid}` |
| Pinterest | `{keyword}` | **官方明确不支持任何广告** | 无 |
| Pinterest | `{targetingtype}` | **官方文档无此项** | 无 |
| Reddit | `{{CAMPAIGN_NAME}}` | 官方 19 行表中**无 "Name of the Campaign"** 一行，疑似不存在 | 只有 `{{ADGROUP_NAME}}` / `{{AD_NAME}}` |
| X/Twitter | 任何 URL 宏 | **整个体系不存在** | 手写静态 UTM + `twclid` |
| LinkedIn | `{{campaignGroupId}}` camelCase | **枚举中不存在** | `CAMPAIGN_GROUP_ID`（UPPER_SNAKE_CASE） |
| Yandex | `{addphrases}` | **EN/RU 官方表均不存在**，疑为已下线历史参数 | `{match_type}` / `{matched_keyword}` |
| Naver | `n_campaign` | **官方清单中不存在** | `n_campaign_type` |
| 百度 | `{os}` `{age}` `{gender}` | **所有来源均未出现，倾向不存在** | 仅 `{device}` |
| 百度 | `{groupid}` | **不属百度** | `{unitid}`（这是 360 的宏） |
| 百度 | `{pagenum}` `{adposition}` `{mediatype}` `{placement}` `{bidurl}` `{haoci}` `{abtest}` | **已下线** | — |
| 腾讯 | `__PLATFORM__` | **不存在** | `__AD_PLATFORM_TYPE__` 或 `__DEVICE_OS_TYPE__` |
| 腾讯 | `__OS_VERSION__` | **不存在** | `__DEVICE_OS_VERSION__` |
| 腾讯 | `__CONNECTION_TYPE__` | **不存在**（腾讯宏表完全无 network/carrier/connection 类字段） | 无 |
| 腾讯 | `__PLACEMENT_ID__` | **不存在** | `__ENCRYPTED_POSITION_ID__`（仅联盟白名单）或 `__SITE_SET_NAME__` |
| 腾讯 | `__SITE_SET__` | **不存在** | `__SITE_SET_NAME__` |
| 巨量 | `__AD_FORMAT__` | **不存在** | `__CTYPE__`（2小图/3大图/4组图/5视频） |
| 巨量 | `__INTEREST__` | **不存在** | 无 |
| 巨量 | `__TIMESTAMP__` | **未证实** | `__TS__`（13 位毫秒） |
| 巨量 | `__KEYWORD__` `__QUERY__` `__KEYWORD_ID__` `__MATCH_TYPE__` | **未证实存在**，倾向不支持 | UTM 或报表 API |
| 快手 | `__CAMPAIGN_ID__` `__UNIT_ID__` `__CREATIVE_ID__` | **不是快手宏**（是小程序 query 的小写参数名） | `__DID__` / `__AID__` / `__CID__` |
| 快手 | `__ACCOUNT_ID__` | **不存在** | `__ACCOUNTID__`（无中间下划线） |
| 快手 | `__PLATFORM__` `__OS_VERSION__` `__GENDER__` `__AGE__` | **不存在**，且 DSP 有宏白名单校验会**直接报错**（官方 FAQ 举例连 `__OS__` 都被拒） | 无 |
| 快手 | `__IMEI__` `__IDFA__`（明文） | **未证实**，只见 md5 形式 | `__IMEI2__` / `__IDFA2__` |
| 知乎 | `{position}` | **不存在**（知乎不用花括号语法） | 无 |
| 知乎 | `__CAMPAIGN_ID__` `__CREATIVE_ID__` | **不存在** | `__CAMPAIGN__` / `__CREATIVE__` |
| 微博 | `__IP__` `__TS__` `__OS__` `__IDFA__` `__MAC__` | **这些是阿里妈妈东风的宏，不是微博的** | `{ip}` `{clicktime}` `{idfa_MD5}` 等花括号族 |
| 微博 | `{CAID}` | **已作废，会被替换为空** | `{RY_CAID}` / `{GX_CAID}` |
| 小红书 | `__IP__` `__UA__` `__TIMESTAMP__` `__IMEI__` `__IDFA__` `__MODEL__` `__CAMPAIGN_ID__` `__UNIT_ID__` `__CREATIVE_ID__` `__NOTE_ID__` | **所有来源均未出现** | 见 §10 小红书 7 宏 |
| Google | `{dclid}` | **不是 Google Ads ValueTrack 宏**（属 DV360/CM360） | `gclid`/`wbraid`/`gbraid` |
| Google | `{aceid}` 用于 App Campaigns | **无法证实** | — |
| Google | `{vehicle_id}` 等 Vehicle Ads 参数 | **无任何官方文档** | — |
| Google | Website Call Conversions URL 宏 | **不存在**；实际是 gtag 配置项 | `phone_conversion_*` gtag 配置 |

---

## 12. 需人工登录后台补齐的 6 项（机器不可达，按性价比排序）

| # | 平台 | 具体动作 |
|---|---|---|
| 1 | **巨量引擎** | 用真实浏览器渲染 `https://event-manager.oceanengine.com/docs/8650/track_url_doc`（唯一权威页，SPA） |
| 2 | **Snapchat** | 打开 `businesshelp.snapchat.com/s/article/add-url-macros` 与 `.../url-parameters`，复制宏下拉框里的字面量（Salesforce JS 站不可抓） |
| 3 | **快手** | 登录 `ad.e.kuaishou.com`【资产-转化-转化追踪】新建转化时页面内有宏说明浮层（"附件一"宏全表） |
| 4 | **小红书** | 登录聚光后台【工具-账户工具-账户三方监测】看可选参数下拉 |
| 5 | **百度 / 360** | 百度：打开 `https://dev2.baidu.com/content?sceneType=0&pageId=100230&nodeId=332` 截取通配符全表（纯 JS）。360：打开 `https://e.360.cn/static/help/list.html` 展开「设置URL」与「URL通配符规则」（`javascript:;` 折叠），并实测 `{wordid}` vs `{keywordid}` |
| 6 | **UC/汇川 · 知乎 · Naver · Reddit · LinkedIn** | 汇川：登录【工具中心-转化追踪】或向 UC 商务索取《网页线索 API 技术对接文档》PDF。知乎：登录 `xg.zhihu.com`【工具中心-转化追踪管理-新建转化】下载最新版 PDF（现有官方 PDF 最新为 2020-06）。Naver：登录 `help.searchad.naver.com` 核对 `n_*` 取值字典与 GFA 宏（域名被抓取黑名单拦截）。Reddit：在 Ads Manager 三方 tracker 宏表里复制 19 个宏的字面量列。LinkedIn：在 Campaign 层 URL tracking parameters 下拉里确认 UI 的花括号语法 |

---

## 13. 建议的代码改动清单（对应 `url-builder/index.html` 的 `PLATFORMS` 数组）

**新增平台条目（6 个）**
1. `google_demand_gen` —— 只放 `{campaignid}` `{adgroupid}` `{creative}` `{device}` `{gclid}` `{loc_*}` `{ifmobile:}` `{ifnotmobile:}` `{random}` `{ignore}` `{lpurl}` `{param1/2}`，并在 UI 上把 `{placement}` `{target}` `{keyword}` `{ifsearch:}` `{ifcontent:}` `{network}` `{targetid}` 标灰禁用
2. `google_app_campaigns` —— 加醒目提示：**不支持 tracking template 挂第三方 click tracker；需 Confirmed Installs**
3. `google_shopping` —— §6 Shopping 表
4. `google_hotel_travel` —— §6 Hotel 表
5. `bing_shopping` / `bing_lodging` —— §8 ④⑤
6. `tencent_impression` / `weibo_app_activate` —— 曝光链路与 APP 激活链路宏集与主链路差异大

**逐平台修正**
- Meta：宏数 13 → **8**，删掉 5 个不存在的
- Bing：删 `{Custom0-8}`/`{IfContent:}`/`{SitelinkId}`/`{ProductPartitionId}`；改为「自命名 `{_key}`，上限 8」的 UI 控件；补 `{BidMatchType}` `{QueryString}` `{copy:}` `{feeditemid}` `{loc_*}`
- Bing PMax：加"asset group 宏不支持，用 `{AdGroupId}`"提示
- TikTok：宏数 13 → **9**（官方表），修正 `__CLICKID__` → `_CLICKID_`，加 AID=AdGroup / CID=Creative 的层级提示
- Pinterest：双花括号 → **单花括号**，宏数 8 → 约 22（B 组 parallel counting）
- X/Twitter：宏数 5 → **0**，改为"仅支持静态 UTM + twclid"说明页
- LinkedIn：语法改 UPPER_SNAKE_CASE 枚举，加"只能设在 Campaign 层"约束，`CREATIVE_NAME` 标注 v202606+
- Yandex：删 `{addphrases}`，补 `{campaign_name_lat}` `{campaign_type}` `{coef_goal_context_id}` `{matched_keyword}` `{adtarget_id}` `{source_type}` `{region_*}`，加 4096 字节截断警告
- Naver：改为"开关式自动追加"说明，`n_campaign` → `n_campaign_type`，补 `n_match` `n_ad_group_type` `n_mall_pid` `n_mall_id`
- 百度：删 `{os}/{age}/{gender}`，拆分「搜索 `{}` 小写」与「信息流 `{{}}` 大写」两套，加联调期 `__X__` 转换提示
- 360：加 `{userid}`、展示广告宏组，标注 `{wordid}` 非唯一需配对
- 腾讯：11 → 约 50，且**必须区分「监测链接宏」与「落地页 `gdt_vid`/`qz_gdt`」两条链路**；删 4 个编造宏
- 巨量：10 → 约 40，重点补 `__MID1__`~`__MID6__` 素材层与 `__CSITE__` 枚举
- 快手：9 → 约 15，修正 `__ACCOUNTID__`，保留官方笔误 `__ADVERTISIINGID2__`，加宏白名单警告
- 知乎：语法 `{}` → `__XXX__`，删 `{position}`，补 `zhs2s=1` 与 `cb=` 强制要求
- UC：拆分「东风（媒体侧）」与「超级汇川（广告主侧）」两个条目
- 微博：4 → 约 24，语法为 `{xxx}` 大小写混合（`{ad_id}` 小写 vs `{AD_NAME}` 大写，易错）
- 小红书：1 → **7**（这就是上限），加"仅账户/创意两级、参数需加白"说明
- CG/AiFu：改为"未知联盟"模板，暴露 TUNE/Affise/HugOffers 三套通用参数供选
