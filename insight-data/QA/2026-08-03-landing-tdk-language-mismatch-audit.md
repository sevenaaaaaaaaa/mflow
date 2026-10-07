# 落地页 SEO TDK 语言错配审计 — 2026-08-03

## 结论

你的判断成立，而且比「tools 英文 title」更大：

- 非英文落地页 **3554** 篇中，**1976** 篇（**55.6%**）在核心 TDK（`title` / `seo.title` / `seo.description` / `description`）上存在语言不对齐。
- 不限于 tools：feature **964**、tool **721**、topic **221**、solution **70** 都中招。
- 主形态不是「写错几个中文字」，而是 **EN 壳 / 未本地化**：英文 boilerplate、`[IT]` 前缀直出英文、slug Title Case、RU 无西里尔字母、JA/KO/ZH 标题纯拉丁文。

（若把 `seo.keywords` 也算上，脏页会到 ~2500；关键词常留英文品牌词，**核心 TDK 口径更准确**。）

## 分语言（核心 TDK）

| 语言 | 脏页 | 占该语言 | 突出问题 |
|------|------|----------|----------|
| ko | 340 | 92% | 标题/描述大量无韩文 |
| ru | 329 | 90% | 无西里尔字母 / EN 壳 |
| zh-TW | 359 | 84% | 标题/SEO 纯英文 |
| ja | 177 | 43% | 拉丁文标题壳 |
| zh | 138 | 28% | 英文 TDK 未汉化 |
| pt | 167 | 45% | EN boilerplate / 空 SEO |
| fr | 164 | 42% | EN 壳 + `[FR]` 标签 |
| it | 149 | 42% | 同上 |
| de | 153 | 40% | EN boilerplate / `[DE]` |

## 分类型（非英文）

| 类型 | 脏/总 | 比例 |
|------|-------|------|
| feature | 964/1695 | 56.9% |
| tool | 721/1323 | 54.5% |
| topic | 221/385 | 57.4% |
| solution | 70/100 | 70.0% |

## 根因形态（修复车道）

1. **EN title shell**：`Create professional…` / `Ai Foo Bar | Lovart` / `Professional Design Tool`
2. **`[IT]`/`[PT]` 前缀**：语言标签 + 英文正文，假装本地化
3. **描述未译**：title 已本地化，`seo.description` / `description` 仍是英文或混语言
4. **CJK/RU 脚本缺失**：language=ja/ko/zh/zh-TW/ru 但核心字段无对应文字系统
5. **空 SEO**：`seo.title` / `seo.description` 为空（尤其 tools）

## 与前两轮关系

- 前两轮清的是「错误文字脚本」（中文进 DE/JA 等）——硬污染。
- 本审计说明更大的池子是 **「语言字段对了，TDK 仍是英文壳」**——软污染，SEO 与 UX 同样受损。
- 列表混语言（L0 前端）与 TDK 错配是两条线；TDK 错配即使前端过滤 language，SERP/详情 meta 仍错。

## 建议修复顺序

1. P0：`title` + `seo.title` 未本地化（车道 B/C/D）— 直接影响列表卡与 SERP
2. P1：`seo.description` + `description` EN 壳（车道 E）
3. P2：空 SEO 回填；`seo.keywords` 按需本地化（品牌词可保留英文）
4. 权威源：优先 vault `Page Gen/*-{lang}.json`；缺失则从 EN 重写（非直译）
5. 门禁：import/preflight 增加「language ↔ TDK 脚本/boilerplate」检查，防止回潮

## 数据文件

- 全量：`~/Documents/Lovart Local Dev/Output/QA-Memo/tdk-language-mismatch-audit-2026-08-03.json`


## 修复进度（2026-08-03 晚）

### P0 标题车道 — 完成
- 修复 **1171** 篇 `title` + `seo.title`
- 复扫：非英文标题错配 **0%**
- 其中 vault 母语成稿 252；其余为过门禁的合成标题（脚本正确，质量分层：模板级，非专栏终稿）

### P1 描述车道 — 已批量推进
- 备份：`~/Documents/Lovart Local Dev/Output/QA-Memo/tdk-desc-lane-backup-2026-08-03.json`
- 标题车道备份：`tdk-title-lane-backup-2026-08-03.json`

### 仍建议后续
1. 高流量页把合成 TDK 换成 vault/人工重写（尤其 JA/KO/RU/ZH tools）
2. preflight 加 language↔TDK 门禁防回潮
3. 前端 L0 列表 language 过滤（独立任务）
