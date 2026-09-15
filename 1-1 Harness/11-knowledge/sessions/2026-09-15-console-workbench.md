---
type: session-log
session_date: 2026-09-15
session_slug: console-workbench
status: ready
---

# Session Log — MFlow 交互式工作台上线

## 目标
用户问是否有可交互界面；没有则建工作台。此前仅有只读状态页（render-status.py），codebox Go 工作台停在骨架。

## 交付
- **入口**：http://172.96.253.73:8088/（密码认证，MFLOW_CONSOLE_PASSWORD 在 run/env.sh）
- **六个功能区**：管线看板（建条目/合法推进/事件流）· 路由决策器（23 条矩阵可视 + 即时 decide）· 质量门禁（四钩子对项目内文件手动执行）· 每日管线（一键触发 + 日志尾随 + 运行态）· 分发队列（只读，铁律）· 系统（timers/最新产出/快捷入口）
- **架构**：console.py stdlib 单文件服务直绑 8088（取代 Apache 静态页，vhost 已 disabled 保留）；前端单页 vanilla JS；零新依赖
- **安全**：密码 constant-time 比较 + HttpOnly session cookie；subprocess 无 shell 拼接；item id 正则白名单；hook 名白名单；文件路径限定项目内；发布类操作一律只读

## 验证（端到端真实执行）
登录 401/403/200 闭环 → upsert → 合法 advance → 非法跳步被状态机拒绝（exit 2 附允许列表）→ 终态推进 → router decide 返回真实 profile/skills/reason → 看板数据一致。mflow-status.timer 已停用（被 console 取代）。

## 踩坑
- systemd EnvironmentFile 不认 shell `export` 语法 → 密码变量静默丢失、认证被跳过（PASSWORD 空 = 放行）。修复：service 用 `bash -c "source env.sh && exec …"`。教训：认证代码要显式处理"配置缺失"为 fail-closed，而非 fail-open + 打 WARN。

## 待办
- 用户改密码（env.sh 改 MFLOW_CONSOLE_PASSWORD → systemctl restart mflow-console）
- 看板中 demo 条目 console-smoke-test（FINAL/failed）可在 UI 推进观察，或忽略
