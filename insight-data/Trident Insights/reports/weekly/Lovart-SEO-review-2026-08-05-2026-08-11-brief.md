# Lovart SEO 复盘周报 — 2026-08-05 至 2026-08-11

> **数据窗口**：复盘周 08/05(周三) 至 08/11(周二)，7 天；环比期 07/29(周三) 至 08/04(周二)，7 天。
> **GSC 口径**：2 天延迟截断，复盘周拉取 08/05~08/10（6 天），环比期拉取 07/29~08/03（6 天），同长度日均对比，公平。
> **⚠️ 数据缺口**：DataWorks CSV 仅入库至 08/04（复盘周 08/05~08/11 未入库），全渠道 UV/付费口径本周无法直接环比，以 GSC+GA4+Bing 三引擎为主数据源；环比期 DataWorks 可用作趋势参考。
> **报告生成**：2026-08-12（周三 cron）

---

## 五板块速览（简版）

**一、核心指标**：GA4 全站 Sessions 153.3 万（-3.2%），Organic Search 28.0 万（-3.8%）；GSC 点击 3.78 万（-24.8%，6d 口径）；Bing 8 月累计 4.34 万点击（7 月全月 15.0 万，环比 -13.6%）；付费口径（DataWorks 环比期）：payUV 538/天、付费金额 $29,726/天，金额口径健康。

**二、安全指标（盈利效率）**：付费金额日均 $29,726（环比期口径）远超 OKR 目标 $7,333/天（达成 405%）；注册→付费转化在 Bing 渠道（payUV 1,101 / UV 46,460 = 2.4%）仍高于 Google（1.5%）。

**三、获客数据**：品牌词 3.61 万点击占 95.5%（-25.3%），非品牌词 1,702（-11.2%，占比 4.5%）；竞品核心词命中 16/44、点击 367（-25.7%）；Top 页面首页 3.53 万占 81.3%（环比 84.0% 改善）。

**四、访问质量**：Organic 着陆页 /canvas 7.53 万 sessions（+3.6%）为第一入口；全站 New Users 24.6 万（-11.9%）为最弱项，新客获取放缓。

**五、OKR**：付费金额 405% 超额达成；自然搜索 UV 39%（27,409 vs 70,000 目标）；非品牌词占比 4.5% vs 30% 目标（达成 15%）；竞品核心词覆盖 36.4% vs 80% 目标（达成 45%）；首页曝光占比 81.3%（目标 75%，未达标但环比改善）。

---

## 一、核心洞察（6 条）

1. **GSC 点击 -24.8% 与 GA4 Organic -3.8% 背离，主因是品牌词大盘波动而非流量塌方**。复盘周 GSC 点击 37,840（日均 6,307）vs 环比期 50,320（日均 8,387），其中品牌词贡献 36,138（-25.3%）。而 GA4 Organic Search 仅从 291,174 降至 279,996（-3.8%），差距 6 倍——GSC 侧跌幅集中在「lovart」「lovart ai」两个词（合计 22,181 点击，占 58.6%），属于品牌搜索密度的周间波动，叠加 6d 窗口截断放大。缓解：继续监控品牌词周趋势，若连续两周 -20%+ 需排查 SERP 异常（品牌词被仿冒站挤占 / 用户搜索习惯迁移）。

2. **New Users -11.9% 是比 Sessions 更值得警惕的信号**。全站新用户 245,658 vs 278,859，跌幅是 Sessions（-3.2%）的 3.7 倍，说明存量用户仍在回来，但新客获取在放缓。根源：品牌词搜索密度下降（新客第一触点）+ Paid Social -85.3%（15,894→2,329 sessions，投放几乎停摆）。缓解：Paid Social 收缩需有对应自然流量补位（见第 5 条页面洞察），否则新客缺口会持续放大。

3. **Google 是唯一失血引擎，中文生态与 Bing 逆势企稳**。GA4 sessionSource：google 296,565（-9.8%）、bing 31,712（+0.2%）、baidu 6,051（+6.0%）、cn.bing.com 16,789（-2.5%）、ntp.msn.cn 20,998（-4.3%）。中文搜索生态合计 ~43,838（baidu+cn.bing+ntp.msn）虽微降但远好于 Google。缓解：Google 侧优先修高曝光低 CTR 的 Tools 页（text-to-image-generator 曝光 6.35 万 CTR 仅 0.54%），中文侧维持 IndexNow 提交节奏。

4. **竞品词覆盖退步：命中 16/44（环比 20/44），点击 367（-25.7%）**。seedance（144 点击）仍是最强单点，但 veo 3（32）、sora（30）、ai video generator（27）体量有限；全量词库仅命中 5/253。距 OKR「竞品核心词覆盖 80%」目标（需命中 35/44）差距 19 词。缓解：优先补「text to video」「background remover」「ai avatar」「talking avatar」等 22 个未覆盖核心词的着陆页/博客（这些词在 Bing 侧已有流量验证）。

5. **首页依赖度改善但非首页流量池未跟上**：首页点击占比 81.3%（环比期 84.0%），Tools（1,552）+Blog（896）+Features（814）+本地化（4,230，合计 9.7%）在涨；GA4 侧 /canvas 着陆页 75,296（+3.6%）超过 /zh/home（57,074，-6.2%）成为第一入口，/pt（-22.1%）、/home（-8.8%）领跌。缓解：/pt、/pt/home 连续两周下滑，需排查葡语页面内容质量与内链；/canvas 增长证明功能页可承载有机流量，可复制到更多工具页。

6. **Bing 7 月 15.0 万点击（-13.6% vs 6 月 17.4 万）为年内次低，8 月日均 ~3,950**。Bing 关键词高度集中：lo v a r t（7 月 10.2 万）+ lovart ai官网（1.38 万）+ loveart（7,608）占绝对主导；页面侧 /zh（1.94 万）> /（9,004）> /zh/features（1,915），中文页在 Bing 的承接能力已验证。缓解：8 月剩余窗口主推 Bing 非品牌长尾词（Bing 词库 1,314 词 vs GSC 2,000 词取样，长尾空间仍在）。

---

## 二、关键词表现（GSC，6d 口径）

**品牌 vs 非品牌**：品牌词 714 词 36,138 点击（-25.3%），曝光 18.0 万，CTR 20.1%；非品牌词 1,286 词 1,702 点击（-11.2%），曝光 1.2 万，CTR 14.2%。非品牌占比 4.5%（环比期 3.8%），微升但距 30% OKR 目标差距巨大。

**品牌词 Top 10**（点击）：lovart 11,170（pos 1.0）/ lovart ai 11,011（1.2）/ loveart 3,401（1.1）/ loveart ai 1,806（1.0）/ love art 743（1.8）/ love art ai 653（1.0）/ lovart ia 350（2.0）/ lovart ai free 310（1.0）/ lovert 251（1.3）/ lovart.ia 240（1.0）。前两词合计 58.6%，是 GSC 点击波动的核心来源。

**非品牌词 Top 10**：civitai red 69（CTR 0.39%）/ 学生証作成 メーカー 39（55.7%）/ freepik ai 34（0.21%）/ seedance 2.0 free 32 / graphic design trends 2027 29 / civitai.red 28 / 无限画布 20 / artlist ai 18 / gerador de carteirinha de estudante 18 / مخرشقف 16。非品牌词以长尾+竞品词（civitai/freepik/artlist）为主，CTR 两极分化——竞品词曝光大但点击低（civitai red 曝光 1.78 万 CTR 0.39%），说明 SERP 上竞品更强。

**排名分层**（复盘周）：≤1 位 17,598（46.5%）/ ≤3 位 35,384（93.5%）/ ≤5 位 36,198 / ≤10 位 37,292 / ≤20 位 37,617。头部排名稳固，93.5% 点击来自 Top 3。

> 💡 **关键词洞察** — **问题**：品牌词周间波动 -25.3% 直接拖累大盘，非品牌词仅 4.5% 占比，竞品词命中下降。**根源**：品牌词搜索密度本身波动 + 竞品词 SERP 竞争加剧（civitai red CTR 0.39% 证明 Lovart 在竞品词上排名靠后但曝光被竞品压制）。**缓解**：非品牌词优先攻「学生証作成 メーカー」「gerador de carteirinha」这类 CTR>40% 的高意向长尾（说明内容匹配度已高，缺的是规模化）；竞品词优先补 22 个未覆盖核心词页面。

---

## 三、自然搜索用户数据（GA4，7d 口径）

**核心指标**：Sessions 1,533,494（-3.2%）、Users 917,494（-3.1%）、New Users 245,658（-11.9%）。全站 New/Return 分层：returning 121.3 万、new 25.5 万、bounce 均 <1%（产品内页）。设备：desktop 141.1 万（92%）主导，mobile 10.2 万。

**全渠道占比**：Direct 51.5 万（33.6%，+0.4%）/ Unassigned 37.7 万（24.6%，+53.3%）/ Referral 32.3 万（21.1%，-4.0%）/ Organic Search 28.0 万（18.3%，-3.8%）/ Paid Search 10.0 万（6.5%，-2.4%）/ Paid Social 2,329（-85.3%）/ Organic Social 8,113（-6.9%）。

**多搜索生态份额（sessionSource）**：google 296,565（-9.8%）/ bing 31,712（+0.2%）/ ntp.msn.cn 20,998（-4.3%）/ cn.bing.com 16,789（-2.5%）/ baidu 6,051（+6.0%）/ chatgpt.com 1,677（-1.5%）。Google 占比 ~71%，中文生态（baidu+cn.bing+ntp.msn）~10.5%，Bing 系（bing+cn.bing+ntp.msn）~16.6%。AI Assistant 渠道 1,700（-2.6%）。

> 💡 **GA4 洞察** — **问题**：Organic 微降但 New Users -11.9% 深层恶化；Paid Social -85.3% 加剧新客缺口。**根源**：品牌词新客触点减少 + 付费投放停摆 + 竞价词渠道（Paid Search -2.4%）同步收缩。**缓解**：GEO/AI 渠道（chatgpt.com 1,677 基本持平）是低成本新客来源，建议加大内容被 AI 引用（结构化数据+权威页面）而非依赖付费补量。

---

## 四、竞品非品牌词覆盖（265 词库）

**核心词（44 词）**：命中 16 词（环比 20），点击 367（环比 494，-25.7%）。命中明细：seedance 144 / graphic design 40 / veo 3 32 / text to image 31 / sora 30 / ai video generator 27 / seedream 18 / ai image generator 18 / image to video 12 / kling 6 / ai poster 3 / midjourney 2 / ai design generator 1 / lip sync 1 / ai banner 1 / logo design 1。

**全量词（253 词）**：命中 5 词、点击 83（环比 111，-25.2%）。未覆盖核心词 22 个：ai photo generator / workflow automation / background remover / text to video / talking avatar / ai avatar / motion control / character consistency / cinematic video / ai commercial / dall-e / flux / marketing video ai / ai ad generator / ugc generator / ai shorts / product video / social media video / brand video / ai logo generator。

> 💡 **竞品词洞察** — **问题**：核心词命中 16/44（36.4%）距 80% OKR 目标差 19 词，且环比再退 4 词。**根源**：覆盖集中在模型名（seedance/sora/veo 3/seedream 共 224 点击，占 61%）——这类词靠内容自然命中；而功能类词（text to video/background remover/ai avatar）Lovart 没有对应聚合页。**缓解**：用 seedance 模型验证过的「模型+场景」内容模板复制到 22 个未覆盖词；Bing 词库中搜索量 >100 的非品牌词优先建页。

---

## 五、页面目录流量（GSC，6d 口径）

**目录分布**（点击）：首页 35,322（81.3%，环比 84.0% 改善）/ Tools 1,552（112 URL）/ 本地化-ru 1,015（122 URL）/ Blog 896（770 URL）/ Features 814（172 URL）/ 本地化-ja 702 / 本地化-zh 602 / 本地化-pt 590 / 本地化-zh-TW 512 / 功能页（login/canvas）268 / Pricing 216 / 本地化-es 247 / 本地化-fr 211 / 本地化-ko 131 / 本地化-it 122 / 本地化-de 98。本地化合计 4,230 点击（9.7%）。

**Top 页面**（点击）：首页 35,322 / /ja 420 / /tools/nano-banana-free 394 / /tools/text-to-image-generator 343（曝光 6.35 万 CTR 0.54%）/ /tools/video-generator 288（曝光 5.95 万 CTR 0.48%）/ /pt 227 / /pricing 216（曝光 6.53 万 CTR 0.33%）/ /login 191 / /ru 183 / /zh 174。

**GA4 Organic 着陆页 Top 10**：/canvas 75,296（+3.6%）/ /zh/home 57,074（-6.2%）/ /home 24,682（-8.8%）/ / 19,315（-12.9%）/ /zh 14,435（-3.3%）/ /zh/projects 5,551（-8.2%）/ /pt/home 4,706（-12.8%）/ /pt 3,837（-22.1%）/ /zh-TW/home 2,233 / /es 1,939。

> 💡 **页面洞察** — **问题**：首页 81.3% 依赖度仍高于 OKR 75% 目标；Tools 高曝光低 CTR（text-to-image 0.54%、video-generator 0.48%）。**根源**：Tools 页 meta/title 与用户搜索意图不匹配（用户搜「text to image」看到的是工具介绍而非直接可用编辑器），/pt 系列连续下滑说明葡语内容未更新。**缓解**：Tools 页重写 meta（复用已有高 CTR 词「nano-banana-free」模板）+ /pt 内容刷新；首页占比环比降 2.7pp 是积极信号，继续扩 Tools/Blog 承接。

---

## 六、分地区表现

**GSC 大区**（点击，6d）：南亚 10,654（28.2%，环比期 13,807）/ 拉美 7,060（18.7%）/ 中东非 4,973（13.1%）/ 欧洲 3,491（9.2%）/ 北美 3,404（9.0%）/ 大中华 2,900（7.7%）/ 日本 1,363（3.6%）。

**GSC 国家 Top 10**：India 6,892（CTR 19.9%）/ Brazil 5,312（21.7%）/ USA 2,446（CTR 3.1%，pos 9.8）/ Iran 2,200（42.0%）/ Pakistan 2,188（29.2%）/ Japan 1,363（9.9%）/ China 1,276（7.2%）/ Egypt 1,017（26.3%）/ Mexico 927（16.8%）/ Russia 920（6.6%）。

**GA4 Organic 国家环比**：US 56,111（-5.7%）/ HK 35,463（-10.5%）/ CN 32,458（+10.3% 🔺）/ JP 29,967（-4.4%）/ SG 21,896（-1.5%）/ IN 17,189（-1.3%）/ TW 11,773（-5.2%）/ BR 11,520（-13.8% 🔻）/ PK 5,383 / DE 4,132（-5.1%）/ EG 4,069（-8.6%）/ MY 3,568（+2.4%）。

> 💡 **地区洞察** — **问题**：巴西 -13.8%、香港 -10.5% 领跌，美国 CTR 仅 3.1%（pos 9.8）持续垫底。**根源**：巴西/香港下滑与品牌词搜索密度下降同源（两地品牌词依赖度高）；美国是最高竞争市场，Lovart 品牌词在美 SERP 排名靠后（pos 9.8），竞品（Canva/Freepik/Adobe）压制。**缓解**：美国市场优先做非品牌长尾（graphic design trends 2027 CTR 26.6% 已验证）；中国 +10.3% 逆势增长，维持中文内容更新节奏；巴西排查 /pt 页面质量（着陆页 -22.1% 同源信号）。

---

## 七、OKR 达成情况（2026-06 OKR）

**O1 自然搜索 UV +87%（34,885 → 70,000/日）**：环比期 DataWorks SEO+GEO UV 日均 27,409（上一报告周期 26,570），达成率 39.2%，❌ 差距大。
- KR1 首页曝光占比：81.3%（目标 ≤75%）— ⚠️ 未达标但环比改善（84.0%→81.3%）
- KR2 Tools 页：112 个 URL 有曝光，text-to-image-generator CTR 0.54% 远低于 3% 目标 — ❌
- KR3 非品牌词占比 4.5%（目标 30%）— ❌ 达成 15%；竞品核心词覆盖 36.4%（目标 80%）— ❌ 达成 45%

**O2 新增付费 +133%（1,714 → 4,000/月）**：环比期 DataWorks payUV 日均 538（上期 554，-2.8%），月化 ~16,140 已超额；付费金额日均 $29,726（上期 $28,787，+3.3%），月化 $89.2 万 vs 目标 $22 万 — ✅✅ 金额 405% 达成。
- KR1 UV→注册 14.4%→18%：缺注册字段无法直接验证（DataWorks 复盘周缺失）

**O3 Referral+GEO UV 14,200/日**：环比期 Referral 渠道 GA4 32.3 万/7d（日均 4.6 万，含非搜索流量，口径不完全对齐）；GEO 渠道 DataWorks 日均约 500（openi 935 + chatgpt 754 + doubao 738 + perplexity 266 + feishu 213 + yandex 808 + quark 538 中 GEO 部分）/ 目标 2,200 — ⚠️ 约 23%。GEO 付费率：chatgpt 30/754=4.0%、openi 27/935=2.9% 仍远高于 SEO 均值。

> 💡 **OKR 洞察** — **问题**：O1（UV/非品牌/竞品覆盖）全面落后，O2 金额维度超额但人数维度 -2.8%。**根源**：增长仍靠品牌词存量（95.5%），非品牌池和竞品词池没建起来；付费金额高是因为 ARPPU 强而非人数多。**缓解**：把 O1 KR3 拆成周粒度执行项——每周新增 5 个未覆盖竞品核心词页面 + 3 个高 CTR 长尾页，8 月目标核心词覆盖 50%。

---

## 八、TODO（P0/P1/P2）

**P0（本周）**
1. Tools 页 meta 重写：text-to-image-generator（曝光 6.35 万 CTR 0.54%）、video-generator（5.95 万/0.48%）、pricing（6.53 万/0.33%）——曝光巨大 CTR 极低，是最大浪费流量池。复用 nano-banana-free（CTR 2.87%）模板。
2. /pt 系列排查：着陆页 -22.1%、-12.8% 连续下滑，检查葡语页面是否被降权/内容过期。
3. DataWorks 复盘周数据入库：CSV 缺失导致全渠道口径断档，确认数据同步管道。

**P1（两周内）**
4. 竞品核心词补页：22 个未覆盖词中优先「text to video」「background remover」「ai avatar」「ai logo generator」（Bing 侧搜索量已验证）。
5. 美国市场非品牌词：graphic design trends 2027（CTR 26.6%）类长尾扩量，降低对 pos 9.8 的品牌词依赖。
6. GEO 扩量：chatgpt.com 付费率 4.0%，持续优化 FAQ/HowTo 结构化数据。

**P2（持续）**
7. 中国区维持 +10.3% 增长：中文内容更新 + IndexNow 提交节奏不变。
8. Bing 长尾：8 月剩余窗口从 Bing 1,314 词库筛搜索量 >100 非品牌词建页。
9. 品牌词监控：若「lovart/lovart ai」连续两周 -20%+，排查 SERP 仿冒/排名异常。

---

> **数据源**：GSC API（双 6d 窗口，6 维度全量拉取 08-12） + GA4 API（双 7d 窗口，stream-filtered，08-12） + Bing Webmaster API（08-12 刷新，含 8 月累计） + DataWorks CSV（环比期 6 天，复盘周缺失）+ 竞品词库（核心 44/全量 253）
> **报告生成时间**：2026-08-12
