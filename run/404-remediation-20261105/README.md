# Lovart.ai 404 修复包 · 2026-11-05（11-06 执行后更新）

数据源：GSC Coverage Drilldown 导出（2026-11-05，采样 1000 / 全站 10,236）× Sanity CMS 真值逐条核对（项目 `o11tm2qe` / `production`）× 线上 URL 实测。

## 执行状态

| 项 | 状态 |
|---|---|
| GSC 样本 1000 条分类 | ✅ 980 条可 301 挽回；13 条整族缺失需决策；7 条垃圾路径忽略 |
| 301 映射包 | ✅ 已生成（nginx / Cloudflare CSV），⏳ 待 Lovart 基础设施侧部署（本工作区无 CF 权限） |
| 站内正文死链 | ✅ 已实测并修复 **924 文档次 / 2417 条链接**（三批：1930 + 114 + 373，覆盖 811 个 unique 文档，Sanity live，`errors=0`）；另有 3 处重复 CTA 一并清理 |
| 剩余站内死链 | ✅ **0（实测）**：全站重扫 8,814 文档 / 22,609 内链，CMS 真值标出 30 处 / 12 unique，逐条 HTTP 实测全部 200；早期「3 条残留」为外链误判，已纠正（见 §六） |
| hreflang 指向 404 | ❌ 线上仍存在，需前端仓库修（实测样例 12 个 alternate 中 10 个 404） |
| sitemap 收录 404 | ❌ 线上仍存在（如 `/ko/tools/veo3.1`），需前端/站点地图生成侧修 |
| 验证 | ✅ 三批复查：2044/2044 + 373/373 目标在线、0 条旧链接残留；全站重扫 22,609 内链，站内死链 0；三批目标抽样/全量 HTTP 重测全 200 |

2026-11-06 00:31–00:55 执行两批 Sanity 写入（第一批 1930 条，第二批 114 处 tools→features），全部 `errors=0`；日志见 `inline-fix-live.log` / `inline-fix-batch2-live.log`。执行原则：开发机默认 dry-run，只有显式 `MFLOW_ALLOW_LIVE_WRITES=1` 才真写；三批均先单文档 canary 验证通过后再全量。

2026-11-06 17:05–17:10 执行第三批（batch3）：canary 单篇 `01-cluster-brand-kit-from-scratch` 通过后全量 **224 文档 / 372 条**（canary 已含 1 条），`errors=0`，日志 `inline-fix-live-batch3.log`；随后 `ops/verify_batch3.py` 复查 225 文档 / 373 链接：`links_applied=373`、`links_failed_or_target_missing=0`、`docs_fully_ok=225`；124 个 unique 修复目标线上重测 **124/124 = 200**（`target-recheck-batch3.json`）。

## 补回执行与复核 · 2026-11-06 18:00

17:05–17:10 的第三批实际已把剩余 373 行全部处理（224 文档 / 372 条 + canary 1 条，`errors=0`）。18:00 又对涉及的 225 文档做了一次独立复核：406 条站内链接中 388×200、13×308、5 条为 CDN 旧 404 缓存（`/canvas` 与 4 条 `/r/*`，加 `Cache-Control: no-cache` 即 200），**源站真实死链 0**。

同时补做两件事：

1. **从 Sanity 草稿恢复 7 篇已删文章**（保留原 slug）：`/blog/ai-design-vs-diy-canva-which-saves-more-time`、`/blog/best-ai-design-agent-for-day-spa-owner`、`/blog/best-ai-design-tools-for-non-designers-comparison`、`/blog/lovart-ai-community-deep-thinking-design`、`/blog/lovart-official-chinese-entry-guide`、`/blog/how-much-does-ai-design-cost-complete-breakdown`、`/blog/lovart-pro-ai-design-agent-logos-brands-video`。
2. **改指 7 条剩余链接**：`/wiki/getting-started-2027`→`/docs/getting-started/how-lovart-works`；`/ai-bar-menu-maker`→`/features/bar-menu-design`；`/ai-corporate-presentation-maker`→`/features/professional-corporate-presentation-design`；`/ja/agent/model-select`→`/ja/blog/complete-guide-ai-image-model-selection-2026`；`/wiki/create-brand-identity-ai-2027` de/fr 分别指向 `/de|fr/blog/how-to-create-brand-identity-ai-design-agent`。

注意：恢复页源站已 200，但部分 clean URL 仍可能被 CDN 旧 404 缓存命中，GSC「验证修复」前先 Cloudflare purge 或等 TTL。证据：`current-scan-summary.json`、`inline-dead-links-batch4.csv`、`inline-dead-links-batch5.csv`。

## 文件清单

| 文件 | 用途 |
|---|---|
| `Lovart-404分类处理-2026-11-05.xlsx` | GSC 1000 条分类 + 本次站内死链修复汇总/剩余清单 |
| `redirect-map.csv` | GSC 980 条 301 映射：`source_url, target_url, rule, last_crawled`（主数据） |
| `nginx-redirect-map.conf` | nginx `map $uri $redirect_target {...}` 精确映射，可直接 include |
| `cf-bulk-redirects.csv` | Cloudflare Bulk Redirects 导入格式（301，保留 query） |
| `inline-dead-links.csv` | 修复前站内死链全量明细（2446 行） |
| `inline-dead-links-by-doc.csv` | 修复前按文档聚合（830 文档） |
| `inline-dead-links-verified.csv` | 第一轮解析结果（候选目标均 HTTP 验证） |
| `inline-dead-links-final.csv` | 最终逐链接动作：`replace / manual / unlink_or_manual` + `resolved_via`（已含两批修复） |
| `inline-dead-links-batch2.csv` | 第二批 105 行 `/tools/* → /features/*` 修复清单 |
| `inline-dead-links-batch3.csv` | 第三批 373 行 / 225 文档修复清单（`resolved_via=batch3_manual_map`） |
| `batch3-map.csv` | 第三批 146 个 unique 旧 href → 目标映射（含 `target_status=200`） |
| `verify-batch3.json` | 第三批验证：`links_applied=373`、失败 0、225 文档全通过 |
| `target-recheck-batch3.json` | 124 个 unique 修复目标线上重测（124/124 = 200） |
| `inline-fix-live-batch3.log` | 第三批全量执行日志（canary + 224 文档，`errors=0`） |
| `recount-internal-dead.json` | 全站重扫（8,814 文档 / 22,609 内链）：CMS 真值标出 30 处 / 12 unique / 22 文档 |
| `recount-internal-dead.log` | 重扫过程日志（分页进度 + 最终口径） |
| `hreflang-alternates-truth.csv` | hreflang 真值清单：2,182 个 slug × 真实存在语言（前端用它裁剪 alternate） |
| `inline-dead-links-final-summary.json` | 最终分桶统计 |
| `before-fix/` | 修复前快照（审计/解析/最终 CSV），用于回滚对照 |
| `verify-inline-fix.json` | 修复后验证：应用数、残留旧链接、剩余死链 |
| `inline-fix-dryrun-v6.log` / `inline-fix-live.log` / `inline-fix-canary2.log` / `inline-fix-batch2-live.log` | dry-run、两批全量执行、canary 日志 |

## 一、站内死链：审计 → 修复 → 验证

**范围与方法**：扫描 Sanity 中 `blog / news / docs`（排除 drafts）正文 `body[].markDefs[].href` 与 CTA `link.external`，只保留站内链接（`/` 开头或 `lovart.ai` 域），用 CMS 真值（blog/news/docs/compositePage 的语言+slug 集合）判 404，并对每个候选修复目标做 HTTP 实测。`/docs/**`、`/home` 等 307/嵌套路由已排除；`pillar/cluster` 旧栏目按 missing 处理。

| 指标 | 修复前 | 修复后 |
|---|---:|---:|
| 扫描文档 | 8,801 | — |
| 站内链接 | 21,709 | — |
| 死链 | 2,446（11.27%） | **0（实测）**；CMS 真值口径 30 处 / 12 unique，逐条 HTTP 实测全 200 |
| 受影响文档 | 830（9.43%） | **0（实测）** |
| 唯一死链 href | 411 | **0（实测）**；CMS 真值口径 12 |

**可修复映射**（`inline-dead-links-final.csv`，2,417 行）：

| 动作 | 行数 | 文档数 | 说明 |
|---|---:|---:|---|
| `replace` | 2,044 | 699 | 目标已 HTTP 200 验证并写回 Sanity（第二批 114 处为 `/tools/*` → `/features/*`） |
| `manual` | 256 | — | 原文已删/无等价页，需人工决定重建或拔链 |
| `unlink_or_manual` | 117 | — | 工具页/旧栏目/杂项，建议拔链或补 301 |

**执行结果**：三批共 699 + 225 文档次（811 个 unique 文档）/ 2044 + 373 条替换全部写入（1930 + 114 + 373；另 +3 处同 href 的重复 CTA），`ifRevisionID` 乐观锁全程生效，`errors=0`；其中 336 条历史 block/markDefs 无 `_key`（Sanity 旧数据），改用数组索引路径 `body[i].markDefs[j].href` 定位。

- 第一批 + 第二批：`ops/verify_inline_fix.py` 复查 `links_applied=2044`、`links_failed_or_old_present=0`、`docs_fully_ok=699`，抽样 40 个目标 HTTP 全 200。
- 第三批（batch3）：`ops/verify_batch3.py` 复查 `links_applied=373`、`links_failed_or_target_missing=0`、`docs_fully_ok=225`；124 个 unique 修复目标线上重测 124/124 = 200。

**剩余项**：旧池约 408 条中，可解析的 373 行 / 225 文档 / 146 unique href 已由 batch3 全部修复（见上）；未处置的主要集中在 `fix_kind=manual / unlink_or_manual` 与 19 文档 26 条未进入解析清单的行，按 unique href 集中在：

| href / 类型 | 条数 | 建议 |
|---|---:|---|
| `/tools/veo3.1` | 63 | 无对应 feature 页，重建或 301 到视频工具索引 |
| `/01-pillar-best-ai-design-tools.md` | 40 | 旧 MD 栏目，确认后拔链 |
| `/blog/best-ai-brand-design-tools` | 33 | 原文已删，拔链或重写 |
| `/tools/free-ai-mockup-generator` | 25 | 工具页缺失，301/重建 |
| `/blog/how-nano-banana-makes-lovart-more-powerful` | 24 | 原文已删，拔链 |
| `/tools/image-generator` | 22 | 301 到 `/features/image-generator` 或重建 |
| `/pillar/ai-video-generation` | 15 | 旧栏目，301 到同级 pillar |
| `/tools/ai-background-remover` | 13 | 301/重建 |

## 二、GSC 404 根因（实测复核）

1. **中文迁移未 301**：旧中文 URL（`/blog/zh-*`、拼音 slug）散落在英/西/德/法语正文共 310 条，其中 304 条（98%）在 `/zh/` 下有活页，是最大可回收资产。
2. **本地化版本被删/从未发布**：467 条如 `/ja/blog/what-is-an-ai-design-agent` 404 而英文 200；301 到英文原版即可回收权重。
3. **hreflang 仍是死链入口**：实测 `https://www.lovart.ai/blog/what-is-an-ai-design-agent` 页面输出 12 个 `alternate`，其中 **10 个（de/es/fr/it/ja/ko/pt/ru/zh/zh-TW）为 404**，仅 en/x-default 200。这是 Google 持续发现死链的直接原因，必须在页面模板里只输出「该语言真实存在」的 alternate。
4. **sitemap 仍收录 404**：线上 sitemap 索引 19 个子图、12,446 URL；其中 `sitemap-lang-ko.xml` 含 `/ko/tools/veo3.1`、`/ko/tools/free-ai-mockup-generator` 等 404 页。注意：GSC 采样 980 条与当前 sitemap 零重合，说明 sitemap 问题影响的是另一批长尾 URL，仍需清理。

## 三、第 1 步 · 部署 301（CDN/边缘层，待执行）

**方式 A · nginx**：

```nginx
include /path/to/nginx-redirect-map.conf;   # map 块需位于 http 上下文

server {
    ...
    if ($redirect_target) {
        return 301 $redirect_target;
    }
}
```

**方式 B · Cloudflare**：Dashboard → Rules → Redirect Rules → Bulk Redirects，导入 `cf-bulk-redirects.csv`（需要 URL List 配额；或动态 Redirect Rule + map 表）。lovart.ai 的 CF 账号不在本工作区（`deploy/cf.env` 是 nownexts.com 且 token 失效），需 Lovart 基础设施侧执行。

## 四、第 2 步 · 站内死链（已完成 Sanity 写入）

复现/增量修复命令：

```bash
cd mflow
# 1) 重扫（会重建 /tmp 缓存；旧缓存不失效，改动后先删 /tmp/mflow_inline_links_v2.json）
SANITY_PROJECT=o11tm2qe SANITY_DATASET=production python3 ops/inline_links_audit.py
# 2) 解析候选目标（HTTP 200 才接受）
python3 ops/inline_resolve_links.py
python3 ops/inline_resolve_localized.py
# 3) 先 dry-run 看计划，再真写（开发机必须显式放行）
SANITY_PROJECT=o11tm2qe SANITY_DATASET=production python3 ops/inline_fix_links.py
MFLOW_ALLOW_LIVE_WRITES=1 SANITY_PROJECT=o11tm2qe SANITY_DATASET=production python3 ops/inline_fix_links.py
# 4) 验证
SANITY_PROJECT=o11tm2qe SANITY_DATASET=production python3 ops/verify_inline_fix.py
```

说明：`env_guard` 会在 import 时剥离 `--live`，因此脚本以 `MFLOW_ALLOW_LIVE_WRITES=1` 判断真写；dry-run 完全离线，不发送 mutate。回滚依据：`before-fix/inline-dead-links-final.csv` 保留每条旧 href，可反向生成修复补丁。

## 五、第 3 步 · hreflang 与 sitemap（前端仓库，待执行）

- **hreflang**：只输出该语言文档真实存在的 alternate；至少 `/blog/what-is-an-ai-design-agent` 这类多语言缺失页，当前 12 个 alternate 中 10 个 404。修完后 Google 不会再从这些页面发现死链。
  - 已从 CMS 生成真值清单 `hreflang-alternates-truth.csv`（2,182 个 blog slug）：**1,069 个 slug 只有 1 种语言**（模板却输出 12 条 alternate → 10 条无效）、1,113 个多语言 slug 中 162 个仅 2 种语言。前端按此表裁剪即可。
  - 注意：多语言缺文档时前端会做 en 回退渲染（`/zh/features/ai-moodboard` = 200 但 CMS 无 zh 文档），所以 alternate 不能只看 CMS 有无，最好用「该 locale URL 实测 200」为准。
- **sitemap**：生成时过滤 404 页面（尤其 `sitemap-lang-*.xml` 中已下线的 tools/本地化页），并重新提交。
- 复核命令：

```bash
curl -s https://www.lovart.ai/blog/what-is-an-ai-design-agent | grep -o 'hrefLang="[^"]*" href="[^"]*"'
curl -s https://www.lovart.ai/sitemap-lang-ko.xml | grep -c '/ko/tools/veo3.1'
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' https://www.lovart.ai/ja/blog/what-is-an-ai-design-agent
```

## 六、第 4 步 · 剩余人工决策

**batch3 已消化**：373 行（225 文档 / 146 unique href）中 `replace` 全部写回（`resolved_via=batch3_manual_map`，映射见 `batch3-map.csv`），验证 373/373 目标在线。

**batch3 文档内站内死链残留 = 0**（修正后口径）。早前报的「3 个残留 404」是**误判**，实为 6 处**外链**，被 `urlparse(h).path` 截成站内路径后再拿 CMS 真值判定：

| 外链 | 出现处 | 实测 | 处理 |
|---|---:|---|---|
| `https://litslink.com/blog/ai-agents-vs-traditional-software` | 4 文档 4 处 | 403（反爬，非 404） | 不动 |
| `https://www.manypixels.co/blog/brand-design/logo-design-trends` | 1 处 | 200 | 不动 |
| `https://www.potatopro.com/news/2025/pepsico-unveils-new-logo-and-global-rebrand` | 1 处 | 200 | 不动 |

同时确认 1 个 CMS 判 missing 但线上正常的内链：`/zh/features/ai-moodboard` = **200**（CMS 只有 de/en/fr/it/ja/ko/pt/ru 文档，前端按 en 回退渲染，614 KB 正常页），属 classifier 对本地化回退页的误报。

**已修 classifier**：`ops/verify_batch3.py` 增加 `internal_path()`，只对 `lovart.ai / www.lovart.ai` 与 `/` 开头的链接做真值判定，第三方外链不再参与；修后重跑 `remaining_dead_links_in_batch3_docs=1`（即上述 zh 回退页），站内死链实为 0。教训：**验证脚本必须和内链审计用同一套「什么算站内」判据**，否则外部链接的 path 会被当自家路由判死。

**上一轮遗留清单**（`inline-dead-links-final.csv` 中 `fix_kind != replace`）：

- `manual` 256 行：blog/pillar 原文已删，决定「重写/重建 → 改指」或「拔链保留文本」。
- `unlink_or_manual` 117 行：旧 MD 栏目、`/cluster/*`、少量 `/tools/*`；优先拔链，避免继续向 404 输送权重。
- 同一 href 在多个文档重复出现，按 unique href 批量决策即可；另有 19 文档 26 条未进入解析清单，可用 `ops/inline_links_audit.py` 重扫补全（重扫前先删 `/tmp/mflow_inline_links_v2.json`）。

## 七、第 5 步 · 验证收尾

- GSC → 页面索引 → 未找到 (404) → 对已修 URL「验证修复」；301 部署后抽查：

```bash
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://www.lovart.ai/es/blog/zh-menu-design-restaurant
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://www.lovart.ai/ja/blog/what-is-an-ai-design-agent
```

- 观察 404 曲线 2–4 周（基线 10,236 @ 10-23；修复日 11-06）。站内死链修复只影响爬虫从正文发现的路径，GSC 曲线的主回落仍取决于 301 与 hreflang 修复。
