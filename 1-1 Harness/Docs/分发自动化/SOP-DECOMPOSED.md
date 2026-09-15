# 全渠道内容分发 SOP — 拆解步骤表

> 源自 GA 驱动全渠道规划 + 平台清单。Canonical SOP 在 Obsidian `2-Area/Product Project Management/全渠道内容分发自动化SOP.md`。

## 步骤总览

| # | 阶段 | 输入 | 输出 | 工具/负责人 | 自动化 |
|---|------|------|------|-------------|--------|
| 1 | 数据摄入 | Trident GA4 页面 + GSC 页面/查询快照 | `queue/candidates-{date}.json` | `score-pages-for-distribution.py` | 全自动 |
| 2 | 候选筛选 | candidates JSON | S/A/B/C 分层 + 推荐平台 | 脚本 + 规则表 | 全自动 |
| 3 | 轨道判定 | 页面 tier + 路径类型 | A=摘要分发 / B=站外原生 | RUNBOOK §轨道 | 半自动 |
| 4 | 内容适配 | 主站 URL + 母稿摘要 | `drafts/{platform}-{slug}.md` | Agent + `channels/*.md` + `templates/` | 半自动 |
| 5 | 质量门禁 | 平台稿 + 主站元数据 | pass / block 报告 | `preflight-distribution.js` | 全自动 |
| 6 | 人工审核 | preflight 通过稿 | approved / rejected | 运营 | 手动 |
| 7 | 发布 | approved 稿 | 平台 URL | `publish-*.js` 或手动后台 | 半自动/手动 |
| 8 | 日志归档 | 发布结果 | `logs/` + `queue/published.json` | 脚本 append | 全自动 |
| 9 | 站外原生选题 | GSC 竞品未覆盖词 | `queue/offsite-briefs.json` | Trident 月报 §5 + Agent | 半自动 |
| 10 | 周报复盘 | logs + UTM | `logs/weekly-{date}.md` | 人工 / Automation | 半自动 |

## 平台矩阵

| 平台 | 轨道 A 摘要 | 轨道 B 原生 | 发布方式 |
|------|-------------|-------------|----------|
| Medium | 是 | 是 | API 半自动 |
| DEV.to | 是 | 是 | API 半自动 |
| Hashnode | 是 | 是 | GraphQL 半自动 |
| LinkedIn | 是 | 是 | 手动/营销 API |
| Pinterest | 是（tools） | 否 | API 半自动 |
| Reddit | 链接帖 only | 是 | 手动 |
| HackerNews | 链接帖 only | 是 | 手动 |
| 知乎 | 是 | 是 | 手动 |
| 百家号 | 是 | 是 | 手动 |
| DeviantArt | 是（视觉 tools） | 否 | 手动 |

## Gate 0 红线（每步必过）

1. 禁止主站全文镜像到站外可索引平台
2. 必须 canonical / 主站链接 + UTM
3. 标题不得与主站 `<title>` 完全相同
4. 站外正文 ≤ 主站 40%（教程）或清单体
5. 主站发布 ≥7 天后再分发（品牌页 ≥14 天）
6. 黑名单：首页、/pricing、品牌词 Top10 着陆页
7. 同一主站 URL ≤2 平台/月

## 数据依赖（Trident）

| 数据 | 默认路径（可 `TRIDENT_ROOT` 覆盖） |
|------|-------------------------------------|
| GA4 页面快照 | `{TRIDENT}/Output/Data Ingestion/monthly-snapshots/ga4-pages-{ym}.json` |
| GSC 页面目录 | 月报 `pdirs` 或 `gsc-pages-{ym}.json` |
| 竞品缺口 | 月报 §5 Core 未覆盖词列表 |

默认 `TRIDENT_ROOT`：

`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/Lovart Dev`

或 `1-4 Dev`（若已迁移）。
