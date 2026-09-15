# 生产投放链接审计（2026-07-29）

> 输入：投放链接汇总表（bing ×3 / 百度 / 360 / 广点通 ×3 / 谷歌 ×2 / 小红书）
> 基准：`AD-TRACKING-PARAM-SPEC.md` v2.1（已按各平台官方文档核实）
> 结论：**宏本身基本都对**，问题集中在「Layer 1/2 不统一」和「小红书那条链路」。
>
> **2026-07-29 更新**：收到《360点睛-转化数据回传API对接文档 2025-07》后，新增一条 🔴🔴 级发现（P0-0），
> 并按你的反馈调整了三项定性 —— 谷歌两条已知、360 缺 UTM 属待启用而非错误、UTM 枚举按标准收敛。

---

## 0. 先说好消息：宏用得是对的

三处交叉验证成功，说明现有投放没有踩宏拼写的坑：

| 平台 | 生产链接用的宏 | 与官方文档比对 |
|---|---|---|
| Bing | `{Campaign}` `{CampaignId}` `{AdGroup}` `{AdGroupId}` `{AdId}` `{Network}` `{keyword:kw}` `{TargetId}` `{MatchType}` `{Device}` `{QueryString}` | ✅ 全部正确，`{keyword:kw}` 带默认值的写法也符合官方建议 |
| 360 | `{planid}` `{groupid}` `{keywordid}` `{creativeid}` | ✅ 全部正确 —— 且**独立印证**了官方《设置URL》里 `{keywordid}` 才是现行宏（不是旧资料里的 `{wordid}`） |
| 谷歌 | `{campaignid}` `{adgroupid}` `{creative}` `{network}` `{keyword}` `{targetid}` `{matchtype}` `{placement}` `{device}` `{target}` `{extensionid}` `{feeditemid}` `{gclid}` | ✅ 全部正确（`{devicemodel}` 除外，见 P0-2） |

---

## 🔴🔴 P0-0 —— 新发现：360 展示广告的 `sourceid` 与你的内部渠道号**完全撞名**

官方《360点睛-转化数据回传API对接文档》第 4 页原文：

> 展示广告：当广告被点击时，投放平台在推广落地页 URL 上自动拼接广告点击唯一编码（**12 位编码**），
> 标识来自 360 流量，如 **`sourceid=12345`**，该编码值对应 API 回传参数中的 `qhclickid`。

你现有的 360 链接是：

```
https://www.liblib.tv/?modelid=22111377&sourceid=006559&planid={planid}&groupid={groupid}&keywordid={keywordid}&creativeid={creativeid}
```

这里的 `sourceid=006559` 是**你的内部渠道号**。如果这条投的是**展示广告**，360 会再自动追加一个
`sourceid=<12位编码>` —— 同一个 URL 里出现两个同名参数：

```
...&sourceid=006559&planid=...&creativeid=...&sourceid=812345678901
        ↑ 你的渠道号                              ↑ 360 的 click id
```

**后果取决于你后端怎么解析**，两种都是坏的：
- 取**第一个** → 拿不到 360 的 click id → **oCPC 回传全废**（回传要用这个值当 qhclickid）
- 取**最后一个**（PHP `$_GET`、Express 默认行为等）→ **内部渠道号被 360 的编码覆盖** → 归因串到错误渠道

**要确认的第一件事**：这条 `sourceid=006559` 的链接投的是搜索还是展示？
- **搜索推广** → 安全。搜索自动拼的是 `qhclickid`（16 位），不撞名
- **展示广告** → 立刻改。把内部渠道号换成别的 key（如 `ch=006559`），或至少在展示广告线单独用一套参数名

**顺带**：360 三条产品线的 click id 完全不同，且官方明确「传错会被当作无效数据丢弃」——

| 产品线 | 落地页参数名 | 位数 | 谁来加 | 回传字段名 |
|---|---|:--:|---|---|
| PC/移动搜索 | `qhclickid` | 16 | 平台自动 | `qhclickid` |
| 展示广告 | **`sourceid`** 🔴 | 12 | 平台自动 | `qhclickid` |
| 移动推广 | `impression_id` | 16/19 | **需手动写 `__impression_id__` 宏** | `impression_id` |

---

## 🔴 P0 —— 会造成数据丢失或归因断裂

### P0-1. `sourceId` 与 `sourceid` 大小写不统一

| 用 `sourceid`（小写 i） | 用 `sourceId`（大写 I） |
|---|---|
| bing ×3、360、广点通 ×3、谷歌 ×2 | 百度、小红书 |

规范文档（`AD-TRACKING-PARAM-SPEC.md` Layer 1）定义的是 **`sourceId`**，但生产里 8/10 条用的是小写。

**为什么要紧**：URL query key 在绝大多数后端框架里是**大小写敏感**的（Nginx、Express、Spring 的 `@RequestParam`、GA4 的自定义维度都区分）。只要接收端不是显式做了 lowercase 归一，这两种写法就会落到两个不同的字段里 —— 表现为「一部分渠道的 sourceId 永远是空」。

**建议**：先确认后端到底认哪个，然后**全量统一成一个**，并把规范文档改成与生产一致的那个（改文档比改链接便宜）。

### ~~P0-2. 谷歌两条链接在 Search 系列上用了 `{devicemodel}`~~ ✅ 你已知悉，此处仅存档

```
...&devicemodel={devicemodel}&placement={placement}&device={device}&target={target}...
```

Google 官方对 `{devicemodel}` 的定义原文是 **"Only available on Display Network campaigns"**。这两条从 utm_campaign 看（`china_search_SD2_KV_tcpa_pageview`、`china_search_industry_zhang_tcpa_sign`）都是**搜索**系列 → `devicemodel=` 会恒为空值。

同理 `{placement}` 和 `{target}` 也是 Display/placement-targeted 专用，在 Search 上一样返回空。

**建议**：搜索系列删掉 `devicemodel` / `placement` / `target` 三个参数，减少无效参数占用 URL 长度；确实要区分机型只能从 UA 解析。

### P0-3 → 降级为「待启用」. 360 链接没有 UTM

```
https://www.liblib.tv/?modelid=22111377&sourceid=006559&planid={planid}&groupid={groupid}&keywordid={keywordid}&creativeid={creativeid}
```

只有 Layer 1（sourceid）+ Layer 3（平台宏），**Layer 2 全缺**。

✅ **已确认为投放同学暂未启用 UTM，后续会启用** —— 不是配置错误，从问题清单降级为待办。启用时按标准枚举取值：
`utm_source=q360&utm_medium=cpc&utm_campaign=<活动名>`（展示广告用 `utm_medium=display`，移动推广用 `cpa`）。

在启用之前，这条流量在 GA4 里会落到 `(direct)/(none)`。

---

## 🟡 P1 —— 数据质量问题，BI 里会算错

### P1-1. `utm_source` 取值不统一

| 生产实际值 | 规范枚举值 | 影响 |
|---|---|---|
| `googleads_int` | `google` | 谷歌流量在 BI 里独立成一行，跨期对比断裂 |
| `bing` | `bing` | ✅ |
| `gdt` | `gdt` | ✅ |
| `xiaohongshu` | `xiaohongshu` | ✅ |
| （360 无） | `q360` | 见 P0-3 |
| （百度无） | `baidu` | 百度那条只有 sourceId + keyword，也缺 UTM |

`googleads_int` 看着像是投放服务商（meetsocial）的命名习惯。

✅ **已定策略：规范只收录通用标准枚举**（`google`）。`googleads_int` 记为**历史遗留**，不追溯改造已在投链接，
新建链接一律用标准值，历史值在统计口径里单独标记、后续停用。详见规范文档《UTM 取值治理原则》一节。
BI 侧建议建 `utm_source_alias` 映射表做归一，比改链接便宜。

### P1-2. `utm_medium` 超出枚举

小红书用了 `paid_social`，规范枚举里是 `social`。同样会在 BI 里分裂成两个 medium。

✅ 同上，按「标准枚举 + 历史遗留归一」处理。

### P1-3. Bing 把搜索词塞进了 `utm_content`

```
utm_content={QueryString}   ← 用户实际检索词
utm_term={keyword:kw}       ← 触发的关键词
```

`utm_term` 用法正确。但规范里 `utm_content` 的定义是「素材变体/差异化」（`variant_a` / `image_16x9` 这类），现在被搜索词占了 —— 意味着 Bing 渠道**无法做素材维度分析**，且搜索词这种高基数值会把 utm_content 维度撑爆。

**建议**：搜索词另开一个参数（如 `query={QueryString}`），把 utm_content 留给素材变体。

### P1-4. 百度把关键词 **ID** 赋给了名为 `keyword` 的参数

```
https://www.liblib.tv/skill/?sourceId=110002&keyword={keywordid}&attr_tracker_id=rwramK
```

`{keywordid}` 返回的是数字 ID，不是关键词文本。参数名叫 `keyword` 会让 BI 侧和看数的人误以为是词本身。

**建议**：改成 `keyword_id={keywordid}`；如果真要词本身，百度的宏是 **`{kw_enc_utf8}`**（UTF-8 编码的**触发的注册关键词**，注意不是检索词）。

### P1-5. 广点通信息流标成了 `utm_medium=cpc`

广点通那条是信息流投放，规范枚举里对应 `social`（或按计费方式 `cpa`），`cpc` 会和搜索广告混在一起。

✅ 同上，历史遗留归一处理。

---

## 🟢 P2 —— 新发现的宏，需要你验证

生产链接里出现了几个**官方文档没有收录**的宏。我已经加进工具里并标注为「🔍 生产观察，待验证」，但**不建议在确认前扩大使用**：

### 广点通（liblib.tv sourceid=080015）

| 宏 | 官方 DataNexus 宏表 | 判断 |
|---|---|---|
| `__CREATIVE_ID__` | ❌ 未收录 | 官方对应的是 `__DYNAMIC_CREATIVE_ID__`（新版）或 `__AD_ID__`（旧版） |
| **`__IMAGE_ID__`** | ❌ 未收录 | **如果有效，这是腾讯少有的素材级宏，价值很高** |
| **`__VIDEO_ID__`** | ❌ 未收录 | 同上 |
| `__AID__` | ❌ 未收录 | 疑似把巨量的宏拿过来了 —— 腾讯对应字段是 `__ADGROUP_ID__` |

**怎么验证**：这条链接已经在跑，直接去看落地页实际收到的 query —— 有效的宏会被替换成数字，无效的会**原样保留** `__IMAGE_ID__` 这样的字面量。看一眼日志就知道了，比查文档快。

> 另：我之前在规范里写的「腾讯的宏不在落地页 URL 上」说得太绝对了，这条生产链接证明落地页 URL 里也能写宏。已修正为「两条链路都可用宏，但官方宏定义表是按监测链接场景写的」。

### 小红书

`__CREATIVITY_ID__` / `__CREATIVITY_NAME__` —— 注意拼写是 **CREATIVITY** 不是 CREATIVE。官方公开资料完全没有这两个，见下节。

---

## 🔍 专项：小红书那条为什么拿不到回传

```
https://www.liblib.tv/wappro?sourceId=120001&utm_source=xiaohongshu&utm_medium=paid_social
  &utm_campaign=xhs_libtv_alwayson_form&utm_content=form_home&agency=dx&objective=form
  &ad_platform=xhs_juguang
  &xhsc=__CLICK_ID__
  &attr_tracker_id=rwram5
  &creative_id=__CREATIVITY_ID__
  &creative_name=__CREATIVITY_NAME__
```

按官方约束，按**排查成本从低到高**列：

**① 先看落地页实际收到了什么**（5 分钟，能直接定位到底是哪一层断的）
- 如果 `xhsc=` 收到的是 `__CLICK_ID__` 字面量 → 宏没被替换，问题在链接配置
- 如果收到的是 `atest` 开头的值 → 这是**联调环境**的 click_id，官方明确「数据不进报表」
- 如果 `creative_id=` 是 `__CREATIVITY_ID__` 字面量 → 这两个宏不存在，且可能触发【监测链接非法】导致整条链接被拒

**② 域名是否加白**（最常见的原因）
官方要求监测/落地域名**必须提前加白**（销售提交邮件 + OA 申请），且必须是正式域名、不接受 IP 和下载链接。`liblib.tv` 加过白名单吗？没加的话报【监测链接非法】。

**③ 参数只能从小红书已有的参数里选**
官方原文：「参数只能在小红书已有的参数中选，用 `&` 分隔」。`__CREATIVITY_ID__` / `__CREATIVITY_NAME__` 如果不在下拉列表里，就属于非法参数。
→ 这也是 **B2 项**（登录聚光后台看【工具-账户工具-账户三方监测】的可选参数下拉）优先级要提上来的原因。

**④ 回传时限**
官方硬约束：**转化回传超过 1 小时即判「回传超时」**。表单类转化如果是走 T+1 批量回传的，一条都不会算。

**⑤ advertiser_id 用错**
回传 body 里的 `advertiser_id`，**多账号时必须用品牌账号 ID**，用了子账号 ID 会静默失败。

**⑥ 官方 FAQ 的兜底结论**
小红书新链路官方明确说「**目前不支持下发其他宏参数，只拼接 clickID**」。也就是说，即使前面几条都对，`creative_id` / `creative_name` 也很可能永远拿不到值 —— 创意维度只能回小红书后台报表看，没法带回自有系统。

---

## 建议的下一步（按性价比）

| 优先级 | 动作 | 成本 | 状态 |
|:--:|---|---|---|
| 🔴 1 | **确认 `sourceid=006559` 那条 360 链接投的是搜索还是展示**；若是展示，立刻把内部渠道号改名 | 1 分钟确认 | 待办 |
| 🔴 2 | 查一次落地页日志，确认 `__IMAGE_ID__` / `__VIDEO_ID__` / `__CREATIVITY_ID__` 是否被替换 | 5 分钟，一次解决全部 P2 疑问 | 待办 |
| 🟡 3 | 统一 `sourceId` 大小写（改后端归一 or 改链接，二选一） | 决策 + 小改 | 待办 |
| 🟡 4 | 登录聚光后台看三方监测可选参数下拉（B2 项） | 定性小红书能不能做创意维度 | 待办 |
| 🟢 5 | 360 启用 UTM（按标准枚举） | 用工具生成 | 已排期 |
| 🟢 6 | 百度那条补 UTM | 用工具生成 | 待办 |
| ✅ — | 谷歌搜索系列 `devicemodel`/`placement`/`target` | 你已知悉 | 已知 |
| ✅ — | UTM 枚举收敛策略 | 规范只收标准值，历史值归一 | 已定 |

## 附：需要你确认的一个技术细节

Bing 那三条的备注说「监测链接在账户纬度」。Microsoft 账户级有**两个**不同的字段，行为完全不同：

- **Tracking template** —— 必须至少包含一个 `{lpurl}` 系列宏，否则报错；上限 2048 字符
- **Final URL suffix** —— 只放参数串，**不能**以 `?` `&` `#` 开头，**不能**含 `{lpurl}`

汇总表【其他】列里那串是 `bing_customer_id=...&utm_source=bing&...` 这种纯参数串、没有 `{lpurl}`，所以**应该是配在 Final URL suffix 里**才对。如果误配进了 tracking template，Bing 会直接拒绝或导致落地页跳转异常。确认一下即可。
