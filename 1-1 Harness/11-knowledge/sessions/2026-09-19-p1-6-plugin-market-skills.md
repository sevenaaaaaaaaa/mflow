---
session_date: 2026-09-19
session_topic: "P1-6 插件市场一键安装 + 全类型支持 + 启停 + Skills 目录"
session_slug: "p1-6-plugin-market-skills"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 60
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- P1-6：Skill/插件市场一键安装 UI。现状：市场页已有安装/卸载/校验，但需"填入安装框→校验并安装"两步，且 `plugin_install` 仅接受 source/publisher 两类；插件无启停；Skills 无浏览入口。

# Solution
1. **一键安装**：`plugin_market_install(mid)` 直接读 marketplace.json 取出 manifest+entry 安装；前端「一键安装」按钮（保留「查看/改代码」给高级用户）。
2. **全类型支持**：`plugin_install` 放开到 source/publisher/gate/transform/analyzer（模板包仍走模板市场）。
3. **启停**：`plugins/<id>/state.json` + `plugin_enabled/plugin_set_enabled` + `/api/plugins/toggle`；`plugins_inventory` 输出 `enabled`；UI 显示状态徽标与「启用/停用」。
4. **Skills 目录**：`skills_inventory(q)` 按分组返回（48 个），`/api/skills`；市场页新增「Skills 目录」卡（分组展示 + 检索）。
5. 实测：`/api/skills?q=landing` 命中 3；一键安装 rss-source 通过 plugin_check；停用/启用生效；测试后已卸载还原。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | plugin_market_install / 全类型 install / plugin_enabled·toggle / skills_inventory / 端点 |
| `1-4 Dev/console/console.html` | modify | 一键安装按钮 / 启停按钮 / Skills 目录卡 / 说明更新 |
| `docs/p1-plan.md` | modify | P1-6 标记完成 |

# Decisions Made
- D1: 一键安装默认装到启用态；停用是软开关（保留文件，便于再启用）。
- D2: Skills 只读浏览（不改动 Skills 体系），聚焦"看得见、搜得到"。
- D3: 安装仍强制过 plugin_check，不允许绕过校验。

# Patterns Observed
- P1: 市场类功能的"摩擦"常在最后一步（填表），一键化收益明显。
- P2: 类型白名单过窄会让生态形同虚设（只放 source/publisher，gate/transform/analyzer 都装不了）。
- P3: zsh 会吞掉 `$("id")` 与反引号，内联脚本改前端必须用 quoted heredoc。

# Open Questions
- Q1: 是否给插件加"配置项"编辑（manifest.config）与"运行一次测试"？
- Q2: 是否支持从远端 marketplace 拉取（而非本地文件）？

# Cross-References
- entities: ds-knowledge-base
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-p1-2-worker-heartbeat-liveness.md

# Tags
- relevant-tags: #p1-6 #plugins #marketplace #skills #one-click
