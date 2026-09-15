# Blog 简体中文 SEO / 正文质量筛查 — 2026-08-07

## 结论（先看这句）

**不是「本地已优化、还没上传」。**  
线上简中 Blog（约 934–947 篇）的现状就是当前质量水位；夹杂英语的标题/描述、模板腔正文，大量已经在 production。本地也没有像 Features 那样一整批「blog-zh-batch ready」待 import 的优质 SEO 稿。

真正发生的是两层问题叠在一起：

1. **存量从未系统做过简中 TDK/正文重写**（缺字段 + 旧模板尾巴 + 英中混排正文）。
2. **近几日 404 ROI 批次（`blog-404fix-*-zh`，约 98 篇）已经上传**，但这次「优化」本身就是中英混搭模板（`— ChatCanvas 实操`、`Brand Kit / editable / readable`），所以你在前台看到的「标题夹英语、正文模板痕」很多就是刚写上去的，不是漏传。

---

## 数据口径

- 源：Sanity `o11tm2qe` / `production`，`_type=="blog" && language=="zh"`
- 对照：`1-2 Insight/QA/2026-08-03-blog-top100-body-language-mismatch.md`、`Output/QA-Memo/audit-zh-zhtw-ja-body-2026-07-22.json`
- 本地对照：`Output/QA-Memo/feature-zh-batch*`（有大量 Features ready）；Blog 侧无对等的全量 zh SEO ready 目录

---

## SEO 信息（标题 / 描述 / 关键词）

全量约 934 篇时点统计：

- 缺 `seo.title`：约 **313**（约 1/3）
- 缺 `seo.description`：约 **163**
- 缺 `seo.keywords`：约 **828**（约 89% 几乎没关键词）
- 描述过短（&lt;40 字）：约 **192**

模板与中英混排（已在线上）：

- SEO title 含 `| Lovart` 旧尾巴：约 **158**（几乎全在非 404 存量）
- SEO title 含 `Lovart AI 设计`：约 **57**
- SEO title 含 `ChatCanvas` / `— ChatCanvas`：约 **35 / 28**（高度集中在 404fix 批次：31/98）
- SEO title 重英混：约 **271**；页面 title 重英混：约 **174**
- SEO desc 带「更多AI设计工具 / 尽在Lovart / 在Lovart探索」尾巴：约 **62 / 24 / 14**
- SEO desc 堆 `Brand Kit` / `Touch Edit` / `Design Agent`：约 **51 / 42 / 31**

典型已上线形态（404 批次，2026-08-06~07 `_updatedAt`）：

- title：`一人公司选什么 Design Agent：改 offer 价比第一张好看更重要`
- seoTitle：`Solopreneur Design Agent — ChatCanvas 实操`
- seoDesc：`一人公司：Brand Kit、personal brand cover、disclaimer editable。`

这不是「没优化」，是**用英文骨架词填了中文 SEO 槽位**。

存量非 404 另有一类：title 已是像样中文专栏句，但 `seoTitle`/`seoDescription` 为空，或仍挂 `| Lovart AI 设计工具` 合成串（如部分 Firefly / 视频横评文档）。

---

## 正文

### 404 修复批次（已上传，模板最重）

近 40 篇抽样开篇几乎全部中英混排运营腔：`这条中文 URL`、`brief 合同`、`editable`、`readable`、`disclaimer`、`ChatCanvas`、`Brand Kit`、`Touch Edit` 密集复现。  
命中示意（40 篇样本）：Brand Kit 39、editable 38、ChatCanvas 37、disclaimer 37、brief 合同 31。  
这是脚本/批量改写痕迹，不是漏传的本地精品。

### 存量非 404

- 2026-07-22 body 审计（当时 zh≈789）：english_body **35**，heavy_en_mix **161**，moderate_en_mix **159**，light_en_mix **337**，empty **29**。
- 2026-08-03 前 100 语言错配：zh 仅 **2%** 纯 EN 壳——前排相对干净，是因为做了 `releaseDate` 分层沉底（zh Tier C 沉 **127**），**不是**全文 SEO/正文重写完成。
- 近期非 404 厚文开篇（如 Nano Banana Pro、设计趋势、海报印刷）中文专栏感明显更好，说明「能写好」，但覆盖面远小于全库。
- 正文块数：&lt;30 块约 **314**，30–79 约 **447**，≥80 约 **182**——大量中短文，Complete Guide 级密度不足。

### 本地是否有更好正文未上传？

- Features：本地有 `feature-zh-batch*` ready，属于「本地优化未全量上」形态。
- Blog：QA CSV 里有少量 `zh-*.md` ready（404 P0/P1），对应 slug 多数**已经**以 `blog-404fix-*-zh` 进库；本地 md 路径甚至已找不到——说明是发布过程产物，不是囤着的优质稿。
- **没有**发现一整批「简中 Blog TDK+正文已重写、待 patch」的 ready 队列。

因此：你看到的问题，主因是**根本没做完 / 做歪了**，不是「优化在本地卡住」。

---

## 和 Features 线的对比（帮助判断）

同日 Features i18n 正在本地整页重写 + TDK 门禁（`2026-08-07-feature-i18n-template-quality.md`）。  
Blog 简中没有对等流水线：只有 404 填坑式中英模板上传 + 早期沉底排序。

---

## 优化空间（按 ROI）

P0 — 先修 SERP 可见层（不碰 schema、不删文档）：

1. 清掉 404 批次 seoTitle/seoDesc 的 `ChatCanvas 实操` / 英文关键词清单腔，改成搜索用户会点的中文句（输入场景 + 结果 + 限定词）。
2. 给缺 `seo.title` / `seo.description` 的约 300+/160+ 篇补中文 TDK（禁 `| Lovart AI 设计工具` 合成尾巴）。
3. keywords：宁缺毋滥；有则写 5–8 个真实中文检索式，别塞英文碎片词。

P1 — 正文：

1. 404 批次开篇去模板：删「这条中文 URL」、降低 `editable/readable/disclaimer` 密度，改成具体场景与数字。
2. 按 2026-07-22 清单优先重写 heavy_en_mix + english_body（约 200 篇量级），不是再沉底。
3. 短正文（&lt;30 blocks）按 GSC 曝光/排名 4–10 先扩，不做全库灌水。

P2 — 门禁：

- Blog 引入与 Tools 类似的 `preflight_tdk_i18n`：拦截 `— ChatCanvas 实操`、纯英文 seoTitle、描述关键词清单、`| Lovart` 尾巴。
- import 前对 zh body 开英混比例阈值（404 批次应直接 BLOCK）。

---

## 一句话回答用户原问

标题夹英语、正文模板痕——**主要是线上现状；近期批次还把模板优化写进去了。本地没有大批更好简中 Blog 稿在等上传。** 该做的是 production 上的差量 patch（TDK 优先），不是找「未上传优化包」。


## 执行进展（同日）

已按 GSC 曝光优先生成 **Top40 简中 Blog TDK patch**，门禁 PASS，状态 ready 等人审。

本地包：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-zh-tdk-batch-2026-08-07/`


## 执行进展（授权后）

Top40 TDK **已 apply production**（40/40）。详见 `2026-08-07-blog-zh-tdk-top40-ready.md`。
