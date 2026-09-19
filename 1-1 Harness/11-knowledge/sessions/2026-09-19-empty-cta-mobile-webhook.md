---
session_date: 2026-09-19
session_topic: "可用性收尾：空状态 CTA 全覆盖、窄屏/移动端适配、出站 Webhook"
session_slug: "empty-cta-mobile-webhook"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/p1-plan.md, deploy/sync.sh]
agents: [opencode]
duration_min: 100
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 可用性第 5/6/7 项：空状态给 CTA、窄屏可用、事件能推外部。

# Solution
1. **空状态 CTA 全覆盖**：新增 `emptyBox(icon,text,label,action)`；批量/QA/Loop/样式/分发/管线/项目/维护/预设/KB/报告/活动等 17+ 处空态改为「图标 + 说明 + 一键动作」。
2. **窄屏/移动端适配**：≤900px 时侧栏改为浮层（`body.sb-open` + 遮罩 `#sb-mask`），主区去左边距；`.cols/.ov-grid/.tgrid/.pgrid/.metrics` 单列；顶栏导航隐藏、操作区换行、输入全宽；抽屉全宽；≤620px 指标两列、命令面板 96vw；汉堡按钮窄屏切浮层、宽屏折叠；点击侧栏项自动关闭浮层。
3. **出站 Webhook**：`run/webhooks.json`（name/url/events/secret/enabled）；`webhook_emit(event,payload)` 后台线程投递（可选 `X-MFlow-Signature` HMAC-SHA256），日志 `run/webhooks.log`；事件接线 task.done/failed/tripped、run.done/failed、automation.run、audit.rollback；端点 `/api/webhooks`、`save|delete|test`；设置页管理卡（列表/事件勾选/测试/启停/删除/日志）。
4. 实测：保存 httpbin webhook → 测试投递 200 → 跑一个 QA 任务 → 日志出现 `task.done -> 测试 HTTP 200` → 清理测试配置。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | webhooks 配置/emit/test + 事件接线 + hmac 导入 + 端点 |
| `1-4 Dev/console/console.html` | modify | emptyBox + 17 处空态 CTA + 移动端 CSS/交互 + Webhook 设置卡 |
| `docs/p1-plan.md` | modify | 标记 5/6/7 完成 |

# Decisions Made
- D1: Webhook 投递在后台线程、失败静默并记日志，绝不影响业务主流程。
- D2: 签名可选（`secret` 为空则不签名），兼容简单接收端。
- D3: 移动端以"浮层侧栏 + 单列 + 输入全宽"为最小可用集，不重做交互。

# Patterns Observed
- P1: 空状态的价值不在"告知为空"，而在"给出下一步"。
- P2: 桌面布局直接上手机 = 不可用；侧栏浮层 + 主区自适应是最小成本方案。
- P3: 出站通知应与入站解耦（事件总线式 `webhook_emit`），避免业务代码被通知细节污染。

# Open Questions
- Q1: 是否需要"事件重放/失败重试队列"？
- Q2: 是否支持按项目/按任务类型过滤事件？

# Cross-References
- decisions: docs/p1-plan.md
- related sessions: 2026-09-19-failure-digest-retry-all.md

# Tags
- relevant-tags: #usability #empty-state #mobile #webhook #events
