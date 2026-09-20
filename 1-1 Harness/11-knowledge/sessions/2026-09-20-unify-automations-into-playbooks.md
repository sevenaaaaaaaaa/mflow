---
session_date: 2026-09-20
session_topic: "消除重复：automations 合并进 Playbook（单一'定时工作'模型）"
session_slug: "unify-automations-into-playbooks"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 110
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- automations 与 playbooks 在"定时/启停/dry-run/硬闸/last_run/runs_today"上高度重复，属技术债。用户要求消除重复。

# Solution
1. **单一模型**：Playbook 为唯一"定时工作"模型；automation 等价于**单步剧本**（`preset` / `spec` / `loop`）。
2. **新增 loop 步骤类型**：`playbook_run` 在发起时创建 Loop 并记录为 `note` 步骤（复用既有 loop_new）。
3. **迁移** `migrate_automations()`：启动时幂等把 `run/automations.json` 转为 playbooks（写入 `legacy_automation` 映射），成功后归档原文件为 `automations.migrated-*.json`。
4. **兼容层**：`automations_list/save/delete/run` 全部映射到 playbooks；`automation_tick` 置空（调度统一由 `playbook_tick`），避免双重触发。
5. **UI 合并**：自动化页只保留「剧本」列表（唯一入口）+「历史执行记录」（按剧本触发的 Run，可跳画布）。
6. 实测：2 条自动化迁移为剧本（映射正确）；兼容端点运行 → run_id；pending 0→40（单次，无失控）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | loop 步骤 + _automation_to_steps + migrate_automations + 兼容层重写 + 启动迁移 |
| `1-4 Dev/console/console.html` | modify | 自动化页合并为剧本列表 + 历史记录 |
| `docs/p1-plan.md` | modify | 追加统一说明 |

# Decisions Made
- D1: 不删除旧端点（外部/历史调用可能依赖），用兼容层映射。
- D2: 迁移幂等且归档原文件，可回滚。
- D3: 调度只保留一条链路（playbook_tick），避免双重触发（上次事故的教训）。

# Patterns Observed
- P1: 两套"触发/硬闸/计数"必然漂移；统一成单一模型是根治。
- P2: UI 层历史记录要注意接口返回形状（数组 vs {items}），否则静默空白。
- P3: 迁移要幂等 + 归档，且启动时执行一次即可。

# Open Questions
- Q1: `automation.migrated-*.json` 保留多久？（建议随 housekeeping 清理）
- Q2: 是否把「自动化」页改名为「定时工作」以正名？

# Cross-References
- decisions: docs/p1-plan.md
- related sessions: 2026-09-20-playbook-automation.md

# Tags
- relevant-tags: #refactor #unify #playbook #automation #migration
