# 落地页各类型 TOP100 正文语言错配审计 — 2026-08-03

> 谁会读：内容 / SEO / 发布负责人  
> 为什么现在读：TDK 已清一轮，正文层仍有高流量 EN 壳与错语种挂载  
> 读完改变什么：先修 GSC≥100 的 28 篇，再清 Feature/Tool EN 错挂与 Topic/Solution EN 壳  
> 下一步：按下方 P0 清单重写 body（非直译）；import 加 language↔body 门禁

## 结论

有，而且不轻。

各类型按 GSC 点击聚合取 TOP slug（不足 100 用 Sanity EN `_updatedAt` 补齐），再扫这些 slug 的全部语言版 `bodyJson` 正文。共检 **1544** 篇文档，命中错配 **266** 篇（**17.2%**）。

主形态两条线并行：

1. **EN 壳（155）**：`language`/title 已本地化，正文仍是英文（或整页复制英文 body）——DE/FR/IT/ZH/ZH-TW 最常见。
2. **EN 文档挂错语种（98）**：`language=en` 但正文是日文/韩文/俄文——Feature 53 + Tool 41 为主；含站内最高流量 Tool `nano-banana-free`（韩文正文）。

Product / Scenario 样本量小（5 / 8），本轮 **0** 错配。Topic / Solution 错配率最高（约 30%），几乎全是拉丁语 EN 壳。

同日已修的 Feature EN 错挂（15 篇）只覆盖旧 GSC TOP；本轮 Feature EN 错挂仍有 **53**（多数在补齐段低流量页），Tool EN 错挂 **41** 此前基本未动。

## 口径

- 排序：GSC live 报告（2026-05～07）按类型聚合 slug 点击；不足 100 用 EN 页补齐
- 实际 TOP 规模：feature 100 / tool 100 / topic 45 / solution 17 / product 5 / scenario 10（后四类 EN 总量不足 100）
- 正文：从 `bodyJson` 抽取可见文案（跳过 URL/asset key）
- 判定：CJK/假名/谚文/西里尔脚本分 + 拉丁功能词；形态经高流量样本人工复核为真阳

## 分类型

feature：672 篇检，99 错配（14.7%）——EN 挂 JA/KO 最多，其次 ZH/ZH-TW EN 壳与错挂 JA。  
tool：584 篇检，85 错配（14.6%）——EN 挂 KO/JA 重；FR/DE EN 壳含高点击页。  
topic：183 篇检，56 错配（30.6%）——DE/FR/IT/ZH-TW 几乎整组 EN 壳。  
solution：92 篇检，26 错配（28.3%）——DE 全中、ZH-TW 全中（标题本地化、正文英文）。  
product：5 篇检，0 错配。  
scenario：8 篇检，0 错配。

## 分语言（错配篇数）

en 98（挂 JA 51 / KO 38 / RU 8 / ZH 1）  
de 41 · zh-TW 32 · fr 29 · it 26 · zh 22 · ru 10 · ko 5 · pt 2 · ja 1

## 高流量 P0（GSC 合计点击 ≥100，共 28 篇）

已抽查正文，以下均为真问题（title 本地化 ≠ body 本地化，或 EN 挂错语种）：

1. tool/en `nano-banana-free` — 10270 — 正文韩文混排（站内最大单页风险）
2. feature/zh-TW `change-video-background` — 2218 — 繁中夹大量日文段落
3. feature/it `magazine-layout-design` — 1346 — 纯英文 body
4. tool/fr `free-ai-mockup-generator` — 1183 — EN 壳
5. feature/fr `ai-video-prompt-generator-veo-sora` — 1103 — EN 壳
6. feature/it `secure-student-id-card-design` — 1029 — EN 壳
7. tool/fr `image-to-image` — 815 — EN 壳
8. feature/de|fr|it `diploma-design` — 761×3 — 三语共享同一英文 body
9. tool/fr `free-ai-illustration-generator` — 718 — EN 壳
10. tool/de|fr `ai-image-upscaler` — 544×2 — EN 壳
11. tool/en `chat-to-image-ai-generator` — 488 — 正文韩文
12. feature/de|fr|it|zh `ai-twitch-overlay-generator` — 354×4 — 多语共享同一日文 body（且主题串成 affiliate ads）
13. feature/zh|zh-TW `ai-instagram-feed-planner` — 333×2 — 日文+中文混排
14. feature/zh|zh-TW `design-viral-youtube-thumbnails-ai` — 321×2 — 德文/英文壳
15. tool/en `mobile-design-app` — 241 — 正文韩文
16. tool/zh-TW `ai-anime-generator` — 231 — EN 壳
17. feature/zh `ai-video-background-remover` — 193 — 德文/英文壳
18. feature/ru|zh|zh-TW `ai-image-generator` — 148×3 — EN 壳（RU 仅有「Функция」标签）

## 根因形态

1. **多语言共享同一 bodyJson**：`diploma-design` DE=IT 长度与正文完全一致；`ai-twitch-overlay-generator` DE=ZH 同为日文 affiliate 串台。
2. **只译 TDK 不译正文**：今日 TDK 车道修了 title/seo，body 未动 → 列表卡看起来本地化，点进去仍是英文/错语种。
3. **EN 被挂上 JA/KO 模板**：低流量 Feature/Tool EN 大量「AIデザインツール / AI 디자인 도구」壳；高流量 Tool 亦中招。
4. **Topic/Solution 本地化半成品**：语言标签 + 英文 CTA/工作流段落。

## 与既有工作线关系

- 同日 TDK 审计：修的是 meta；本审计是 **正文层**，问题仍在。
- Feature EN 错挂 15 篇已修：只覆盖旧 TOP；本轮 Tool EN 错挂与 Feature 补齐段仍脏。
- Blog TOP100 正文 EN 壳（同日）：同一「译壳不译体」缺口在 Blog 侧的镜像。

## 建议动作（按 ROI）

1. **P0**：上表 28 篇高流量——优先 `nano-banana-free` EN、`change-video-background` zh-TW、`diploma-design` DE/FR/IT、`ai-twitch-overlay-generator` 多语串台。
2. **P0**：Tool `language=en` 且正文 KO/JA 的高点击页（chat-to-image、mobile-design-app）。
3. **P1**：Topic/Solution 拉丁语 + zh-TW EN 壳批量重写（或沉底，避免占本地化 URL）。
4. **P1**：Feature/Tool EN 错挂剩余池（约 90 篇，多在补齐段）按 traffic 或 `_updatedAt` 分批。
5. **门禁**：preflight 增加 `language ↔ body 脚本/功能词`；BLOCK EN 壳进非 EN、BLOCK 非拉丁脚本进 EN。

## 数据文件

- 全量：`~/Documents/Lovart Local Dev/Output/QA-Memo/landing-body-lang-mismatch-top100-2026-08-03.json`
- 含：top_slugs、stats、all_issues、high_traffic_issues、morphology

## 修复进度（2026-08-04）

### P0 GSC≥100 — 28/28 已修，语种复核 FAIL=0

方法：

1. **vault 同语言母稿覆盖** 19 篇（含 `nano-banana-free` EN、`chat-to-image` EN、`mobile-design-app` EN、多数 FR/DE/IT/ZH-TW EN 壳）
2. **EN vault → 目标语结构翻译** 5 篇（`diploma-design` IT；`ai-twitch-overlay-generator` DE/FR/IT；`ai-image-generator` RU）
3. **zh-TW 干净 twin → 简中适配** 4 篇（`ai-twitch`/`ai-instagram-feed-planner`/`ai-video-background-remover`/`ai-image-generator` ZH）

机器产物：

- 计划：`p0-body-fix-plan-2026-08-04.json`
- batch1 结果/备份：`p0-body-fix-batch1-results-2026-08-04.json` + `p0-body-fix-backup-batch1-*.json`
- batch2 结果/备份：`p0-body-fix-batch2-results-2026-08-04.json` + `p0-body-fix-backup-batch2-*.json`
- 复核：`p0-body-fix-verify-2026-08-04.json`（28/28 PASS）

质量分层说明：语种脚本已对齐；GT/繁简适配稿是 **过门禁级**，不是专栏终稿。部分页（如 `mobile-design-app` EN、`ai-video-background-remover` ZH）相对原 EN 壳变薄，后续可按流量扩写。

### 仍建议后续

1. P1：剩余 ~238 篇 TOP100 范围外/补齐段错配
2. 高流量页把 GT 稿换成 vault/人工重写（尤其 JA 串台已清的 Twitch 多语）
3. preflight 加 language↔body 门禁防回潮
