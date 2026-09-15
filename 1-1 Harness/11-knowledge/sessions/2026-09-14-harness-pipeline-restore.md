---
type: session-log
session_date: 2026-09-14
session_slug: harness-pipeline-restore
status: ready
---

# Session Log — Harness 管线全量修复（生产可用性恢复）

## 目标

用户指令："按你的 ROI 判断排序，让这个工作流再次回到生产可用的程度。"即把因 vault 搬家而全线断停的 Harness（调度层 / 编排层 / 路径契约 / SSOT 文档）恢复到生产可用。

## 起点（变更前审计快照）

- 调度层全断：launchd 无任何 lovart 任务、无 crontab、Cursor Automations 从未落地（manifest 写了但 .cursor/automations/ 不存在）、hermes gateway 穇转
- fm-check 自 2026-09-02 停跑（每晚报告断档 12 天）
- `1-3 GenFlow/.pipeline/pipeline-state.json` 不存在（编排层状态丢失）
- 28+ 处活跃脚本硬编码旧路径（`/Users/seveno/Knowledge/Obsidian/MindRe`、iCloud LifeOS 路径）；`~/Knowledge` 目录已不存在
- audit 快照：A2 26 文件 frontmatter 缺失 / A3 hermes-mem 未引用 11-knowledge（ERROR）/ A4 claude+cursor skills 目录缺失（WARN）
- 根因链：vault 从 `~/Knowledge/Obsidian/MindRe` 搬到 `~/Obsidian/MindRe/MindRe` 后，所有绝对路径与调度全部脱锚；2026-08-01 PATH-MAP 计划的 `~/Lovart Local Dev` 迁移与 Cursor Automations 均未执行

## 完成

**1. 路径契约修复（30 文件，旧路径归零）**
- trident 9 个脚本、scripts 根 10 个、hooks 4 个、sync_to/from_notion、session-init、sync-local-dev、sentinel plist、local-dev-env、quality-cascade smoketest、hooks README
- 修法统一：Python 用 `Path(__file__).resolve().parents[N]` 推导；bash 用 `BASH_SOURCE` 推导或环境变量兜底；每处替换带 count==1 断言
- local-dev-env.sh 三处语义修正：LOCAL_DEV_ROOT 回归 Documents 真相；RESOURCE_ROOT 从 iCloud 3-Resource 改为 vault 根（与所有消费方语义一致）；GIT_DIR 改挂 LOCAL_DEV 下

**2. 编排层复活**
- `.pipeline/` 重建（pipeline_state.py init）
- smoke 全绿：pipeline-state 39/39、hooks 16/16、router 15/15、quality-cascade PASS
- session-init.sh 4 门禁全过

**3. 每日管线全绿（真实跑通，exit 0）**
- 建 trident-venv（`~/Documents/Lovart Local Dev/trident-venv`，py3.12 + google-auth/googleapiclient/pyyaml/requests）
- 新契约 `LOVART_PYTHON`（local-dev-env.sh 定义），三个 run-*.sh 统一消费
- 步骤结果：gsc-daily OK（GSC API 真实拉数，gsc-full.json 落盘）+ sentinel-collect 22/22 + sentinel-daily OK（舆情日报 2026-09-13/14 两份产出）+ harness-auto-optimize OK + harness-sync OK；feishu 按设计 SKIP（无凭据，非致命）

**4. 附带 bug 修复（试跑暴露）**
- gsc_fetch.py：sys.path 层级错（parents[4]→parents[5]）；删除本地过期 `is_brand` 影子函数（遮蔽 lovart_brand_match SSOT 导入且引用未定义 BRAND_PATTERNS——NameError 根因）
- run-weekly-pipeline.sh：run_all.sh 指向空的顶层 `Skills/lovart-trident-data-engine/`（真身在 01-strategy/ 下）
- report-notify.sh：feishu 凭证路径同病同修
- weekly/monthly 管线接通 LOVART_PYTHON + 语法校验过

**5. launchd 重接（3 任务已加载）**
- 新建 plist 源：`1-4 Dev/automation/plists/{com.lovart.daily-pipeline,com.lovart.weekly-pipeline,com.lovart.dream}.plist`（plutil lint 过）
- 日历：daily 08:00 / weekly 周一 07:00 / dream 02:30；`launchctl list` 三条在册 rc=0

**6. SSOT 文档校准**
- 00-INDEX.md 重写为 v3.1：清掉 19 处失效引用（WORKFLOWS.md / PROJECT_OVERVIEW.md / ANTI-BUGS-REGISTRY 等），全部条目对照磁盘实存核验，新增"会话启动门禁"节
- skills-usage.md 重写：目录结构对照实存（45 skill），编排层 12 skill 分代标注，删除幽灵目录树（00-core 74 个等）
- TOOLS-REGISTRY.md：统计同步（core 19 / hooks 4 / 总 42）、合并重复 Hooks 段、归档路径注记、新增 trident-venv 运行环境契约
- MEMORY-PROJECT.md v1.9：编号混乱修复（双 §9→§9/§13、双 §12→§12/§14）、追加 §6.32 修复记录
- PATH-MAP.md：顶部加"2026-09-14 现状校准"节（正文迁移计划未落地，防止后续 agent 误执行）
- AGENTS.md：技能目录真相更正（.cursor/skills 不存在，harness_sync 生成 .cursor/rules）+ 会话启动门禁接线
- hermes MEMORY.md：顶部加 11-knowledge 指针（修 A3 ERROR）

**7. 治理工具自身修复**
- audit.sh A4 目录清单对齐现实（3 目录：hermes/cursor_rules/harness）
- fm-check.py 发现 --fix 未实现（仅文档），另写脚本补齐 26 个 session 文件 frontmatter → fm-check 90 文件全绿

## 验证

- 最终 audit：rc=0（A1 仅 informational orphans；A2-A6 全 OK）
- fm-check：90/90 OK
- session-init：4 门禁全过
- 每日管线：exit 0 全绿
- launchctl list：3 任务在册

## 决策与理由

- 选 launchd 而非 Cursor Automations 作为当前调度真相：manifest 的 Cursor 方案需人工在 Cursor UI 保存 workflow，此前从未落地；launchd 可脚本化验证。manifest 保留，用户日后可在 Cursor UI 落地后切换。
- sentinel 独立 plist 不加载：daily pipeline 已含 sentinel 步骤，避免双跑。
- `~/Lovart Local Dev` 迁移计划不执行：PATH-MAP 是 8/1 的计划，Documents 路径是全部脚本的既成事实，修复以现实为准（已有 2026-09-14 校准节说明）。

## 未尽事项（按 ROI 排）

1. weekly 管线未试跑（下周一 07:00 首跑需人工瞄一眼日志 `~/Documents/Lovart Local Dev/Logs/com.lovart.weekly-pipeline.out.log`）
2. 飞书凭据未配（feishu.json），配好前每日管线飞书推送持续 SKIP
3. Insight 层卫生：SEO Reports 路由违规区归位、根目录 _inbox 回灌、iCloud 冲突副本清理
4. 分发线重启（Drafts ~2200 文件积压 vs queue 停在 6 月）
5. Hermes 运行时重建（现仅 4 skill / 8 profile 目录，vault 45 skill 为真相，可由 harness_sync 每日再生）

## 触动文件（约 40）

- 路径修复 30 个（见 §6.32 清单）
- 新建：trident-venv、3 个 plist、本 session log
- 重写：00-INDEX.md、skills-usage.md
- 修补：TOOLS-REGISTRY.md、MEMORY-PROJECT.md、PATH-MAP.md、AGENTS.md、~/.hermes/memories/MEMORY.md、audit.sh、26 个 session frontmatter
- 状态：`1-3 GenFlow/.pipeline/{pipeline-state.json,events.jsonl}` 重建

## Lessons

- vault 搬家必须同步迁移三类东西：脚本硬编码、launchd plist、运行时凭证路径——本次三类全断了，且断了 6 周无人发现（fm-check 报告断档是唯一哨兵）。
- "索引腐烂"是启动协议架构的特有风险：所有 agent 第一口奶是 00-INDEX，索引错 = 每个新会话都带病启动。
- 试跑即验证：gsc_fetch 的三个 bug（venv 缺库、path 层级、影子函数）只有真跑才暴露，语法校验全过≠可用。
