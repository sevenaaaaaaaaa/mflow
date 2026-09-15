# Lovart Local Dev × MFlow 重新对接清单

> 整理日期：2026-08-01  
> 目的：Local Dev 已从文稿（`~/Documents`）迁到家目录；本文件是项目本体（MFlow）重新对齐路径的 SSOT 清单。

---

## ⚠️ 2026-09-14 现状校准（正文计划未全部落地，以本节为准）

实测核对结果（2026-09-14，Harness 管线修复会话）：

- **运行层实际仍在 `~/Documents/Lovart Local Dev`**——`~/Lovart Local Dev` 从未落地（不存在），"兼容软链"也未建成。`local-dev-env.sh` 默认值已改回 Documents 真相。
- **项目本体（vault）实际在 `~/Obsidian/MindRe/MindRe/1-Project/Lovart MFlow`**——正文写的 `~/Knowledge/Obsidian/MindRe` 已失效（目录不存在）。
- **路径契约已全量修复**：30 个活跃脚本的旧硬编码（seveno/Knowledge/iCloud）归零，统一改为脚本位置推导 + `$LOVART_RESOURCE_ROOT` / `$LOVART_LOCAL_DEV_ROOT`。
- **launchd 已重接**：`com.lovart.daily-pipeline`（08:00）/ `com.lovart.weekly-pipeline`（周一 07:00）/ `com.lovart.dream`（02:30），plist 源在 `1-4 Dev/automation/plists/`。
- 正文"必改清单"保留作历史记录，勿再按正文执行。

---

## 0. 一句话结论

| 项 | 旧值 | 新值 |
|---|---|---|
| **运行层根路径** | `~/Documents/Lovart Local Dev` | `~/Lovart Local Dev` |
| **兼容软链** | — | `~/Documents/Lovart Local Dev` → `~/Lovart Local Dev`（已建，旧硬编码暂不炸） |
| **项目本体（知识/脚本）** | `MindRe/1-Project/Lovart MFlow` | 仍在 `~/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow`（iCloud 文稿副本已空） |

**建议最终态**：把所有契约里的默认值改成 `$HOME/Lovart Local Dev`，软链可保留作过渡。

---

## 1. 必改环境变量 / 契约文件（项目本体）

按优先级改这些文件里的默认路径：

| # | 文件 | 字段 / 内容 | 改为 |
|---|---|---|---|
| 1 | `1-4 Dev/automation/local-dev-env.sh` | `LOVART_LOCAL_DEV_ROOT="$HOME/Documents/Lovart Local Dev"` | `$HOME/Lovart Local Dev` |
| 2 | `1-4 Dev/scripts/sync-local-dev.sh` | `LOCAL_DEV=...Documents...` | `$HOME/Lovart Local Dev` |
| 3 | `1-1 Harness/04-setup/路径契约.md` | 运行层路径全文 | 同上 |
| 4 | `1-1 Harness/10-config/产出路由规则.md` | `LOVART_LOCAL_DEV_ROOT=...` | 同上 |
| 5 | `1-1 Harness/Docs/参考配置/01-环境与配置.md` | Documents 路径 | 同上 |
| 6 | shell / launchd / Hermes profile | 凡写死 Documents 的 | 同上或改用 env |

全库硬编码扫描（约 142 处）：

```bash
rg -l 'Documents/Lovart Local Dev' \
  "$HOME/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow" \
  --glob '!**/tmp/**' --glob '!**/raw/**'
```

过渡期靠软链也能跑；长期应改默认值，避免再依赖 Documents。

---

## 2. 整理后的 Local Dev 目录（当前实态）

```text
~/Lovart Local Dev/
├── AGENTS.md                 # 本仓库铁律（置顶 / Sanity / 多语言）
├── PATH-MAP.md               # 本清单
├── .sanity_config.json
├── .gitignore
│
├── Output/                   # ★ 运行产物 SSOT（契约保留）
├── Backup/                   # ★ 备份
├── Sanity/production-pulls/  # ★ 线上只读拉取
├── WordPress/readonly-pulls/
├── Logs/
├── Temp/
├── seo-documents/            # sitemap / llms / IndexNow 运维缓存
├── features/                 # 落地页 JSON 工作副本 → 对应 GenFlow/Page Gen/features
├── tools/                    # 轻量工具脚本 → 对应 1-4 Dev/tools
├── automation/               # Local 侧自动化（content-health 等）
├── scripts/
│   ├── *.py                  # 既有 patch / FAQ / portable text 脚本
│   └── active/               # 从根目录收拢的近期活跃脚本（见 §4）
│
├── _inbox/                   # 待回灌到 MFlow 的知识/提示词（非运行缓存）
│   ├── insight-docs/         # → 应对齐 1-2 Insight
│   └── prompts/              # → 应对齐 1-2 Insight 或 Design Gen
│
└── _archive/                 # 废弃迭代 / 凭据草稿 / 杂项（不进管线）
    ├── scripts-legacy/
    ├── credentials-scratch/
    ├── logs-scratch/
    └── misc/                 # Flowcoming 残留、1-4 Dev 空壳、lovart-wp-headless 等
```

契约目录（不要改名）：`Output` `Backup` `Sanity` `WordPress` `Logs` `Temp` `seo-documents` `features` `tools`。

---

## 3. Local Dev ↔ MFlow 模块对应表

| Local Dev 路径 | MFlow 对应 | 角色 | 同步方向 |
|---|---|---|---|
| `Output/Page Gen/` | `1-3 GenFlow/Page Gen/` | 页面生成产物 | Local → Vault（新文件） |
| `Output/Content Calendar/` | `1-3 GenFlow/Content Calendar/` | 日历稿 | Local → Vault |
| `Output/Lovart-Blog-Pipeline/` | `1-3 GenFlow/Lovart-Blog-Pipeline/` | Blog 管道产物 | Local → Vault |
| `Output/Knowledge Base/` | `1-2 Insight/Knowledge Base/` | 快照/缓存 | Local → Vault |
| `Output/SEO-Reports/` | `1-2 Insight/SEO Reports/` | **路由违规区**（应迁 Insight） | 清理后以 Vault 为准 |
| `Output/QA-Memo/` | （仅 Local） | pinned-list 等运行备忘 | 不进 Vault |
| `Output/自媒体稿件/` | `1-3 GenFlow/Content Distribution/` | 分发稿 | 按需 |
| `Output/Warehouse/asset-audits/` | — | TOOLS 素材审计 dump | 归档级 |
| `features/*.json` | `1-3 GenFlow/Page Gen/features/` | 落地页 JSON | Local → Vault |
| `tools/` | `1-4 Dev/tools/` | 工具脚本 | Local → Vault |
| `seo-documents/` | `1-2 Insight/SEO Reports/sitemap/` | sitemap/llms | Local → Vault |
| `automation/` | `1-4 Dev/automation/` | 运行侧脚本（部分镜像） | 各自维护 |
| `scripts/` + `scripts/active/` | `1-4 Dev/scripts/` | 运维/发布脚本 | 精选提升到 Vault |
| `_inbox/insight-docs/` | `1-2 Insight/` | 策略/方案文档 | **待回灌** |
| `_inbox/prompts/` | `1-2 Insight/` 或 `1-3 GenFlow/Design Gen/` | 提示词 | **待回灌** |
| `_archive/**` | — | 废弃 | 不对接 |

官方 sync 脚本：`1-4 Dev/scripts/sync-local-dev.sh`（先 dry-run，再 `--apply`）。

---

## 4. 本次移动明细（根目录清理）

### 4.1 → `_inbox/insight-docs/`（知识资产，应回灌 Insight）

- `COMPOSITEPAGE_全站素材需求.md`
- `CRO-funnel-analysis-2026-06-18.md`
- `Lovart-SEO-内链优化全景方案-2026-Q3.md`
- `README_四工具管线.md`
- `T2-003-Rapid-MLX.md` / `_百家号版` / `_知乎版`
- `TOOLS_15页方案_审核稿.md`
- `TOOLS_内容模板与SEO方案.md`
- `TOOLS_模块×尺寸×提示词对照表.md`
- `TOOLS_模块素材规格表.md`
- `TOOLS素材缺口排查报告.md`
- `i18n-localization.md`
- `kr1-cro-implementation-plan.md`
- `kr1-cro-meta-description-rewrite.md`
- `scrapling-research-report.md`

### 4.2 → `_inbox/prompts/`

- `bento-4-prompts.md`
- `capability-tabs-bento2-prompts.md`
- `comparison-before-after-prompts.md`
- `competitor-landing-prompts.md`
- `feature-detail-prompts.md`

### 4.3 → `scripts/active/`（近期仍在用的脚本）

含：`sanity_helpers.py`、`_patch_zh_blogs.py`、`zh_expand_uploader.py`、`quality_demote.py`、各 `audit_*` / `fix_*` / `_build_articles.py` / `translate_it_reliable.py` 等共 35 个。  
对接时：需要进本体的，提升到 `1-4 Dev/scripts/`；其余留 Local。

### 4.4 → `_archive/scripts-legacy/`

历史 `translate_*` 迭代、`test_*`、token/curl 临时脚本（约 31 个）。**不要**再挂进 cron / skill。

### 4.5 → `Output/...`

| 原路径 | 新路径 |
|---|---|
| `自媒体稿件/` | `Output/自媒体稿件/`（已合并） |
| `asset-specs/` | `Output/asset-specs/` |
| `blog-cover-design/` | `Output/blog-cover-design/` |
| `tools_*.json/csv`、`p1_asset_matches.json` | `Output/Warehouse/asset-audits/` |

### 4.6 → `_archive/misc/` 等

- `Flowcoming/`（仅残留 `.env`）
- `1-4 Dev/`（Local 内空壳，非本体）
- `lovart-wp-headless/`
- `newtake_crawl_output/` + crawler
- `entities.json` / `mempalace.yaml`
- `.token_*` / `*_b64*` → `_archive/credentials-scratch/`
- 根目录 translate 日志 → `_archive/logs-scratch/`

根目录现仅保留：`AGENTS.md` + `PATH-MAP.md` + 契约目录。

---

## 5. 你重新对接时的操作清单（勾选）

1. [ ] 确认软链存在：`ls -l ~/Documents/Lovart\ Local\ Dev`
2. [ ] 改 `local-dev-env.sh` 默认根路径为 `$HOME/Lovart Local Dev`
3. [ ] 改 `路径契约.md` / `产出路由规则.md` 文档中的路径
4. [ ] `bash 1-4 Dev/scripts/sync-local-dev.sh`（dry-run）确认还能找到 Local
5. [ ] 决定 `_inbox/insight-docs` + `prompts`：回灌 Insight，或确认 Vault 已有更新副本后删除 inbox
6. [ ] 从 `scripts/active/` 挑选要升格到 `1-4 Dev/scripts/` 的正式脚本
7. [ ] 扫描并批量替换硬编码：`Documents/Lovart Local Dev` → `Lovart Local Dev`（或统一改 env）
8. [ ] 注意 Insight 路径：iCloud `.../Documents/MindRe/.../Lovart MFlow` 已空；本体在 `~/Knowledge/Obsidian/MindRe/...`——凡写 iCloud 文稿路径的也要一并改
9. [ ] Cursor / Hermes / launchd 工作区若仍指向旧 Documents，改绑到 `~/Lovart Local Dev`
10. [ ] 验证：`Output/QA-Memo/pinned-list.json` 可读；`seo-documents/`、`features/` 路径未断

---

## 6. 双本体路径提醒（易混）

| 名称 | 路径 | 状态 |
|---|---|---|
| MFlow 本体（应用这个） | `~/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow` | 完整 ~379MB |
| iCloud 文稿旧位 | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MindRe/1-Project/Lovart MFlow` | **空目录** |
| Downloads 备份包 | `~/Downloads/Lovart MFlow`（+ zip） | 不完整 ~170MB，勿当 SSOT |
| Local Dev 运行层 | `~/Lovart Local Dev` | 本次整理对象 |

---

## 7. 快速验证命令

```bash
# 运行层
test -d "$HOME/Lovart Local Dev/Output/QA-Memo" && echo LOCAL_OK

# 旧路径兼容
test -d "$HOME/Documents/Lovart Local Dev/Output" && echo SYMLINK_OK

# 本体
test -f "$HOME/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/1-4 Dev/automation/local-dev-env.sh" && echo MFLOW_OK

# 加载契约
source "$HOME/Knowledge/Obsidian/MindRe/1-Project/Lovart MFlow/1-4 Dev/automation/local-dev-env.sh"
echo "$LOVART_LOCAL_DEV_ROOT"
```
