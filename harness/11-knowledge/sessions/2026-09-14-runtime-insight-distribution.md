---
type: session-log
session_date: 2026-09-14
session_slug: runtime-rebuild-insight-hygiene-distribution-restart
status: draft
---

# Session Log — Hermes 运行时重建 + Insight 卫生 + 分发线重启

## 目标

承接上一轮（Harness 管线修复）的下一批 ROI 候选：Hermes 运行时重建、Insight 层卫生、分发线重启。目标状态分别是"运行时 = vault 镜像且每日再生"、"情报层无冲突副本无过程垃圾"、"分发机器热态、一次授权即可发射"。

## 完成

### 1. Hermes 运行时重建

- 根因：`install-hermes-lovart-profiles.sh` 从 `~/.hermes/skills/lovart/` 组装 8 个 profile，但没有任何环节把 vault 的 45 个 skill 同步进运行时——运行时只剩 4 个旧代 skill，profile 组装时大量 WARN missing。
- 修法：`harness_sync.py` 新增 `sync_hermes_skills()`（vault Skills/ 所有含 SKILL.md 的目录 → `~/.hermes/skills/lovart/`，copytree dirs_exist_ok，增量不删除运行时遗留），挂在 `sync_hermes_profiles()` 之前。
- 结果：运行时 49 skills（45 vault + 4 遗留）；8 个 profile 重新组装（各 5-10 个真实 skill）；harness_sync 由每日管线 D07 步骤驱动，"vault 为真相、运行时每日再生"闭环成立。
- 附带：audit.sh A4 对 cursor_rules 的计数改为 *.mdc（原来数 SKILL.md 恒为 0，误导）。

### 2. Insight 层卫生

- iCloud 冲突副本 16 处全量处理：md5 对比后 4 个完全相同已归档、9 个有内容分歧保留待人工复核、3 个无基名孤儿原地保留；完整判定清单在 `Local Dev/Backup/conflict-copies-2026-09-14/manifest.csv`。分歧集中在 Knowledge Base/Lovart News（1 篇 6 个副本）和 Trident 6 月报。
- SEO Reports 违规区第一次分流：归档 30 个过程产物到 `Local Dev Backup/seo-reports-archive-2026-09-14/`（5 个临时调试脚本、17 个零引用 chart png、3 个空模板 CSV、3 个 A/B/C backup 产物、6 月月报 v1+v2——月报 SSOT 在 Trident monthly）。目录内新增 README 说明新规则（过程产物不进 vault）。sitemap/ 子目录查明是 sync-local-dev.sh 映射目标，保留。
- 清理：`Trident Insights/排序分析/` 空目录删除；根目录 517KB 一次性 URL 清单 `blog_newline_fix_urls.md` 归档。
- 保留判断：根目录 25 个策略/提示词 md 是 PATH-MAP 回灌后的合法资产，原地保留未动。

### 3. 分发线重启（停在 ready，未外发）

- 库存盘点：Website-Ready 672 稿 = 530 ready（519 中文 T2 工具稿 + 11 "英文"——后证实分类器误判混有中文稿）/ 83 duplicate / 58 review。
- 打分脚本修复：`score-pages-for-distribution.py` 的 `trident_root()` 指向不存在的 iCloud LifeOS 路径（前轮扫描漏网——不含 seveno 字样），改为脚本位置推导。但页面级 GA4 快照（ga4-pages-*.json）本身不存在于任何快照目录（月度快照只有聚合数据），页面级打分链路的数据底座缺口与 8 月月报结论一致，本轮不硬造数据。
- 首批重启单：`queue/dispatch-restart-2026-09-14-batch1.json`（中文 5 篇最新 T2 稿走知乎 wechatsync 轨道、英文 2 篇挂 devto/blogger 待凭证；canonical_url 已补；approved=false）。
- 全链路干跑验证：dispatch-publish.js --dry-run 走通 调度器 → 授权闸（approved≠true 只预检不真发，符合发布铁律）→ 平台路由 → preflight 质量门。7/7 稿被 preflight 正确 BLOCK：稿件正文缺 utm_source 追踪链接（AD-Tracking SSOT 要求）。
- pending.json 更新：新增 restart 块（status: ready_awaiting_authorization + 三个 blocker）。

## 验证

- fm-check 91/91 OK；audit rc=0；launchd 3 任务在册（回归确认未破坏上一轮成果）。
- dispatch dry-run 输出结构完整（国内轨/海外 API 轨/爱贝壳轨/汇总）。

## 未尽事项（按 ROI 排）

1. **稿件 UTM 化**：530 篇 ready 稿发布前的最后一公里——批量在正文 CTA 链接追加 utm_source={platform}（工具用 `AD-Tracking/url-builder/index.html` 的规范，或写一次性脚本走 TOOLS-REGISTRY 注册）。这是分发线真正能发的前置。
2. **海外凭证**：DEVTO_API_KEY / Blogger OAuth 配置后 devto/blogger 通道即热。
3. **"英文"稿重筛**：11 篇所谓英文稿多为中文误判，分发批次如需海外轨应重筛或补写 EN 版。
4. **页面级打分数据底座**：ga4-pages 快照生成器缺失，score-pages-for-distribution 依赖它做优先级——与月报"补齐 From Datawork"是同一件事。
5. 冲突副本 9 处分歧 + 3 孤儿待人工过目（manifest 已给）。

## Lessons

- 漏扫教训：上一轮路径扫描用 "seveno|Knowledge/Obsidian" 做 grep 特征，score-pages 的 LifeOS 路径不含这些特征就漏了。更稳的特征是 iCloud 路径串 `Library/Mobile Documents` 或直接跑一遍脚本让 import/call 炸出来。
- "ready ≠ 可发"：分发线的质量门（utm/canonical/字数）是设计良好的，重启的价值在于让这些门重新拦得住东西。
- 运行时再生架构的补环方式不是"搬文件"而是"补同步函数挂进每日管线"，否则下次搬家又会漂移。
