---
type: session-log
session_date: 2026-09-20
session_topic: "开工预热 warmup（真实只读/dry-run）+ 文档 SSOT 补到 Phase 22 + 修单测污染生产审计日志"
session_slug: warmup-docs-refresh
profiles_used: [profile-lovart-management]
tools_used: [console.py, warmup.py, run-tests.sh, test_console_units.py, ROADMAP.md, docs/capability-matrix.md, deploy/sync.sh]
agents: [cowork]
duration_min: 90
files_changed_count: 9
schema_bumps: 0
status: ready
---

# Context

用户目标：**明天就在后台用 Lovart Global**，不要再在本地摸索。要求每一块后台都像"已经用了一段时间"。
明确选择：**真实只读 / dry-run 跑一遍**（不造种子数据，不真写生产库）。四个板块全要：
内容生产与发布 · Agent 与剧本 · QA 编排与物料 · GEO 与报告。

约束：本次会话在 Cowork 沙箱，出口白名单封了 nownexts.com（403）与 SSH 端口（network unreachable），
`~/OpenFlowDev/.ssh` 也不在连接文件夹内 → **无法直接部署**。故交付形态是"本地备好 + 用户跑 `deploy/sync.sh`"。

# Solution

## 1. 开工预热 `1-4 Dev/scripts/warmup.py`（新增，纯标准库 ~600 行）

六板块 31 步，全部**只读或 dry-run**，把后台各页面的历史记录/findings/缺口/报告一次性跑出来：

| 板块 | 覆盖 |
|:--:|---|
| 0 | 健康基线 · 自检 · 一键自愈 · RAG 底座 |
| A | 内容库状态/同步 · 多语言覆盖 · 发布通道连通 · 落地页闭环 dry-run · 发布历史 |
| B | QA 扫描（真实读 Sanity）· findings 归类 · 修复编排 dry-run · 复检 delta · 物料台账 · alt 补齐 dry-run |
| C | OPC 装启推荐剧本 · 全剧本试运行预览 · 跑一次 dry-run 剧本 · Agent 真实一轮 · 执行画布历史 |
| D | GEO 探测 · 引用记录 · 效果归因 · 内链体检 · 月度自我迭代回顾 · 报告中心 |
| E | 失败→学习 · 降噪预览 · 治理面板 · 收件箱 · 健康终态 |

设计要点：
- **不提供 `--real` 开关**——真写仍走后台人工授权（铁律不破）。
- **fail 与 skip 严格区分**：`DATA_SKIPS` 词表把"缺数据/缺凭证"归为 skip，报告里的 ✗ 只代表真故障。
- 批量任务建完要 `wait_batch` 轮询到终态，否则历史停在 running。
- 报告落 `run/logs/warmup-*.md`，幂等，可重复跑。

## 2. 修复：单测污染生产审计日志（本次顺手抓到的真 bug）

`test_console_units.py` 通过 `importlib` 加载 console.py，而 `RUN_DIR = PROJECT / "run"` 是模块级常量
→ **import 那一刻起，所有落盘动作都写进生产 `run/`**。实测 2026-09-20 当天 `approvals.log`
92 条里几乎全是 `CHAIN-CREATE t1 -> batch-x dry_run=True` + `HOUSEKEEPING` 的单测噪音，真实操作被淹没。

修复：
1. `RUN_DIR` 改为可由 `MFLOW_RUN_DIR` 覆盖（默认行为不变）。
2. `run-tests.sh` 强制 `mktemp -d` 并拷入 `run/sites/` 只读种子，跑完 trap 清理。
3. 补 `TestRunDirIsolation` 3 个用例：env 被尊重 · 不指向仓库 run/ · 派生路径（TASKS_FILE/PROJECTS_DIR）一起搬走。
   → **单测 39 → 42，全绿**；实测 approvals.log mtime 跑测试后不变。

## 3. 文档 SSOT 补到 2026-09-20

- `ROADMAP.md` 止于 Phase 18（09-17），缺 3 天共 156 次提交。补入 **Phase 19–22**：
  知识治理/Anti-Slop/三模式（09-18）· Agent 化与可用性（09-19，93 commits）·
  剧本/MCP/自愈自进化（09-20）· 开工预热（本轮）。
- `docs/capability-matrix.md` 全量重写：15 → **41 项能力**，按 A 生产 / B 治理 / C Agent自动化 /
  D 情报效果 / E 知识开放 分组；待办补 U7（QA 84 项授权）U8（GEO 品牌词）U9（LLM 余额）；
  欠账补 T7（console.py 10.5k 行膨胀）T8（库→GEO 联动）T9（4 类页面无专属 skill）T10（OpenFlow L3–L6）。
- 新增 `docs/warmup.md`；`deploy/sync.sh` 纳入 warmup.py / warmup.sh。

# Verification（实测，非推断）

本地起隔离 console（`MFLOW_RUN_DIR=/tmp/wu3`，端口 8097）真实跑 warmup 三轮：

| 轮次 | 结果 | 说明 |
|---|---|---|
| 第 1 轮 | 19 ok · 6 skip · **7 fail** | 暴露脚本自身 3 个 bug + 4 处"缺数据"被误判成 fail |
| 第 2 轮 | 19 ok · 12 skip · 1 fail | 修完 8 处；剩 1 个剧本 fail（根因是上游 Sanity 连不上） |
| 第 3 轮 | 19 ok · **13 skip · 0 fail** | 上游归因后如实记 skip；报告正确落在隔离目录 |

修掉的脚本 bug：`/api/publish/history` 返回数组当 dict 解（AttributeError）· OPC 已装过时误报"0 个" ·
物料台账打印 `?` 页 · 治理面板 `?/?` · 剧本失败不说卡在哪步 · 报告目录未认 `MFLOW_RUN_DIR`。

会话门禁：**6/6 GATE PASS**，单测 42/42。冒烟残留（2 份 warmup 报告 + 1 份空数据生成的自我迭代回顾）已删除。

# Files Changed

| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/scripts/warmup.py` | add | 开工预热主程序（纯标准库） |
| `1-4 Dev/scripts/warmup.sh` | add | 包装：从 run/env.sh 读密码 |
| `docs/warmup.md` | add | 用法 / 板块 / 安全边界 / 读报告姿势 |
| `1-4 Dev/console/console.py` | modify | RUN_DIR 支持 MFLOW_RUN_DIR 覆盖 |
| `1-4 Dev/scripts/run-tests.sh` | modify | 强制临时 RUN_DIR + 种子拷贝 + trap 清理 |
| `1-4 Dev/tests/test_console_units.py` | modify | +TestRunDirIsolation 3 用例（39→42） |
| `ROADMAP.md` | modify | 补 Phase 19–22 + 顶部标注三份文档的分工 |
| `docs/capability-matrix.md` | modify | 重写至 41 项能力 + 待办/欠账刷新 |
| `deploy/sync.sh` | modify | 同步 warmup.py / warmup.sh |

# Decisions Made

- D1: **不造种子数据**。用户明确选真实只读——与项目"无数据不造假分""dry-run 下如实报未闭环"一致。
  一屏诚实的空状态，好过一屏漂亮的假数字。
- D2: warmup **不提供真写开关**。要真写就走后台人工授权，不给脚本开后门。
- D3: fail 与 skip 必须严格区分。否则"缺 WordPress 凭证"这种待办会伪装成故障，真故障反而看不见。
- D4: 单测隔离用 env 覆盖而非改测试——server 端行为零变化，风险最小。
- D5: 部署由用户跑 `deploy/sync.sh`（沙箱够不到服务器，且这本就是既有流程）。

# Patterns Observed

- P1: **模块级常量 = 隐式全局副作用**。`RUN_DIR = PROJECT/"run"` 让"import 一个模块"变成"写生产目录"，
  测试无从隔离。凡是落盘路径都应可由 env 覆盖。
- P2: 预热类脚本的价值有一半在 **fail/skip 的分类准确**。分不清"故障"和"还没配"，报告就没人看。
- P3: **冒烟测试必须在零数据环境跑**——正是空库才暴露出 4 处错误归类和 1 个 AttributeError。
- P4: 文档失真是有半衰期的：3 天 156 次提交就能让自称 SSOT 的能力矩阵完全失效。
  ROADMAP/能力矩阵/p1-plan 三者要显式声明分工，否则下一个接手的人按过期世界观做判断。

# Open Questions

- Q1: warmup 是否该进 launchd/systemd（比如每周一早跑一次，作为"这周系统还活着"的体检）？
- Q2: `--sync-library` 目前是全量（3 分钟）；T2 增量同步做完后应改为默认增量。
- Q3: 历史 approvals.log 里那 92 条单测噪音要不要清洗？（建议随 housekeeping 处理，保留原文件归档）
- Q4: U9（LLM 余额）09-18 记过 402，09-20 调用正常但无充值记录——需确认。

# Cross-References

- decisions: docs/warmup.md, docs/capability-matrix.md, ROADMAP.md
- related sessions: 2026-09-20-unify-automations-into-playbooks.md, 2026-09-18-closeout.md

# Tags

- relevant-tags: #warmup #onboarding #test-isolation #audit-noise #ssot #docs-drift
