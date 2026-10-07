# Blog 前 100 正文语言错配审计 — 2026-08-03

## 结论

有，而且很严重——但不是「各语言均匀脏」，而是 **拉丁语系 + KO/RU 的前排大量 EN 壳**；**ZH / ZH-TW / JA（经分层排序后）前排相对干净**。

口径：各语言按前端排序字段 `releaseDate`（缺则 `publishedAt`/`_createdAt`）取前 100 篇；用 `pt::text(body)` 做脚本启发式 + `langdetect`（拉丁语）。共检 **1000** 篇，错配 **372** 篇（**37.2%**）。

主形态：**title 已本地化，body 仍是英文原文**（EN 壳 / 未重写）。

## 分语言（前 100）

| 语言 | 错配 | 率 | 主因 |
|------|-----:|---:|------|
| ko | 78 | 78% | 正文全英文；标题多为韩文 |
| pt | 62 | 62% | 正文英文；title 葡语 |
| ru | 59 | 59% | 正文英文；title 俄语 |
| fr | 55 | 55% | 正文英文 |
| it | 53 | 53% | 正文英文 |
| de | 46 | 46% | 正文英文 |
| ja | 10 | 10% | 仍混入 EN body（多为 `releaseDate=2025-01-01` Tier C）；部分 title 实为中文 |
| zh-TW | 6 | 6% | 简繁混用偏简（非纯 EN） |
| zh | 2 | 2% | 2 篇纯 EN body |
| en | 1 | 1% | 1 篇夹带较多汉字（弱信号） |

## 根因形态

1. **EN 壳（占比最大）**：`language` 正确、title 已译，body 仍是英文专栏/评测原文。
2. **JA 残留 Tier C**：分层排序已把大量 EN-ja 沉底，但优质 JA 不足 100，前 100 仍吸入约 10 篇 `2025-01-01` 英文正文。
3. **JA title 语言污染**：个别 `language=ja` 文档 title 是简中（如「AI角色设计指南…」），body 仍是英文。
4. **ZH-TW 简繁漂移**：6 篇正文汉字为主，但简体特征偏重（非「完全英文」类错配）。
5. **KO 未做与 JA/ZH-TW 同级的质量分层排序**：故前排 78% 仍是英文正文。

## 样本（形态示意）

- DE `ai-art-copyright-2026`：title 德语，body「The Complete Legal Guide…」
- KO `artlist-ai-review`：title 韩语，body「Artlist AI Review: When Music Platform…」
- RU `ai-art-copyright-2026`：title 俄语，body 同 EN 法律指南
- JA `ai-character-design-guide-…`：title 简中，body 英文，`releaseDate=2025-01-01`
- ZH `ai-brand-design-tutorial`：title 中文，body「Why Traditional Branding Takes Forever」

## 与既有工作线关系

- 落地页 TDK 错配（同日审计）是 **meta EN 壳**；本审计是 **Blog 正文 EN 壳**——同一生产缺口的正文层。
- JA/ZH-TW 曾用「语言匹配度 → 调 `releaseDate`」止血，解释了为何 JA/ZH 前排错配远低于 KO/PT/RU。
- 止血 ≠ 修好：沉底的英文正文仍在库里，SEO 深页仍暴露。

## 建议动作（按 ROI）

1. **P0**：对 KO/PT/RU/DE/FR/IT 复用 JA 三层 `releaseDate` 分层，先把 EN body 踢出前排。
2. **P0**：前 100 错配清单优先重写/替换正文（非直译），尤其 KO 78 篇。
3. **P1**：清 JA 前排 10 篇 EN + 中文 title 污染；ZH 2 篇 EN body。
4. **P1**：ZH-TW 6 篇简繁归一（繁体重写）。
5. **门禁**：import 前强制 `language ↔ body 脚本/langdetect`，BLOCK EN 壳进非 EN。

## 数据文件

- 全量 JSON：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-top100-body-language-mismatch-2026-08-03.json`

## 止血执行（2026-08-03 晚）

按 RULE 11 三层 `releaseDate` 分层（只改排序字段，不动 `publishedAt`）：

- 脚本：`~/Documents/Lovart Local Dev/scripts/active/blog_language_quality_tier_sort.py`
- 策略：Tier C→`2025-01-01` 沉底；Tier B→`2026-01-15`；Tier A **保留原 releaseDate**（仅从 B/C 误沉提升），避免打乱优质文时间序
- 已 apply：**2431** 篇（fail=0）
  - 沉底 C：ko 517 / pt 432 / ru 388 / fr 319 / de 290 / zh 127 / it 75 / zh-TW 11
  - 混排 B：zh-TW 91 / zh 27 / ru 23 / ja 12 / ko 9 …
  - 提升 A：ja 104（此前被沉的真日语正文回前排）等

### 前 100 复扫（止血后）

| 语言 | 前 | 后 | Δ |
|------|---:|---:|---:|
| de | 46 | 0 | -46 |
| fr | 55 | 0 | -55 |
| it | 53 | 0 | -53 |
| ja | 10 | 0 | -10 |
| ko | 78 | 14 | -64 |
| pt | 62 | 0 | -62 |
| ru | 59 | 0 | -59 |
| zh | 2 | 0 | -2 |
| zh-TW | 6 | 0 | -6 |
| en | 1 | 1 | 0 |

KO 仍 14/100：库内合格韩语正文仅约 **77** 篇，前 100 必然吸入 14 篇 Tier C。止血上限到此，剩余要靠重写正文。

复扫 JSON：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-top100-body-language-mismatch-rescan-2026-08-03.json`  
Apply 记录：`~/Documents/Lovart Local Dev/Output/QA-Memo/blog-language-quality-tier-apply-smart-2026-08-03.json`

## KO 前排 14 篇正文重写（2026-08-04）

按 `lovart-blog-signal-writer` 约束重写并 Portable Text patch 回 Sanity（只改 `body`/`seo`/`releaseDate`，slug/_id/category 保持）。

- Wave1（4）：`how-to-chat-generate-illustration`, `seedance-ai-review`, `capcut-ai-review`, `pollo-ai-review-…`
- Wave2/3（10）：`meta-imagine`, `artlist`, `best-agent-social`, `5-minute-workflow`, `dessert/digital/dropship/dtc`, `subscription-fatigue`, `create-3d-characters`
- 门禁：各篇 ≥7500 어절、hangul≥0.20、无 ZH 泄漏、PT validate ok
- **复扫：KO top100 错配 14 → 0**

草稿：`~/Documents/Lovart Local Dev/Output/Lovart-Blog-Pipeline/Lovart-Blogs/01-Drafts/ko-wave{1,2,3}/`  
结果：`~/Documents/Lovart Local Dev/Output/QA-Memo/ko-rewrite-2026-08-03/`

## KO 14 篇专栏精修（2026-08-05）

问题：首轮为凑 7500 어절，出现大量「실전 확장 노트 N」重复块。

处理：
- 去掉编号注水头；重写各篇核心立场/矩阵/失败案例/FAQ
- 用城市×角色的独特现场故事扩写（非同句复制）
- 14/14 再 patch；本地稿：`01-Drafts/ko-polished/`
- 脚本：`~/Documents/Lovart Local Dev/scripts/active/polish_ko_top14_blogs.py`
- 复扫：KO top100 错配仍为 **0**

## KO 前三专栏深修（2026-08-05 晚）

对象（当时列表前三）：
1. `ai-subscription-fatigue-utility-gap`
2. `best-agent-for-social-media-marketing-manager`
3. `create-3d-characters`

相对上一轮「城市现场故事」扩写：核心章节重写为专栏结构（立场/矩阵/案例/会议话术/FAQ），去掉旧注水头；字数仍 ≥7500，hangul≈0.63。  
稿：`01-Drafts/ko-deep/` · 脚本：`scripts/active/deep_polish_ko_top3.py`

## KO #4–#6 专栏深修（2026-08-05）

1. `capcut-ai-review` — 7578어절, hangul≈0.58
2. `seedance-ai-review` — 7543어절, hangul≈0.57
3. `pollo-ai-review-an-honest-look-at-this-all-in-one-ai-video-platform` — 7548어절, hangul≈0.58

结果：`QA-Memo/ko-rewrite-2026-08-03/deep/deep-4to6-results.json`

## KO #7–#9 专栏深修（2026-08-05）

1. `meta-imagine-ai-review` — 7540어절, hangul≈0.57
2. `best-ai-design-agent-for-dessert-shop-owner` — 7561어절, hangul≈0.59
3. `best-ai-design-agent-for-digital-marketing-manager` — 7642어절, hangul≈0.59

结果：`QA-Memo/ko-rewrite-2026-08-03/deep/deep-7to9-results.json`

## KO #10–#12 专栏深修（2026-08-05）

1. `artlist-ai-review` — 7629어절, hangul≈0.55
2. `best-ai-design-agent-for-dtc-founder` — 7655어절, hangul≈0.55
3. `5-minute-workflow-busy-founders-ai-design` — 7627어절, hangul≈0.56

结果：`QA-Memo/ko-rewrite-2026-08-03/deep/deep-10to12-results.json`

## KO 原 14 篇深修收尾（2026-08-05）

剩余两篇已深修并 patch：
1. `best-ai-design-agent-for-dropshipper` — 7616어절, hangul≈0.56
2. `how-to-chat-generate-illustration` — 7634어절, hangul≈0.57

齐套复验：原 14 篇 hangul 全 ≥0.55、无旧注水头；KO top100 错配仍为 **0**。  
结果：`QA-Memo/ko-rewrite-2026-08-03/deep/deep-remaining2-results.json`
