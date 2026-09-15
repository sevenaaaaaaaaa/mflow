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

## v2 追加（同日）——从"工程面板"重做为"内容运营工作台"

用户反馈：没有知识库、任务清单、报告，"这个后台我怎么用"。v1 只覆盖了管线状态机，是 agent 视角不是运营者视角。

**重做内容**：
- 总览：待办/管线/分发计数卡 + 最新月报/周报/舆情日报一键阅读 + 当日管线结果摘要
- 任务看板：手动任务（待办/进行/完成三列，tasks.json 持久化）+ 管线/分发队列自动同步只读区；预置 4 条真实待办
- 报告中心：10 分类（月报 27/周报 95/舆情日报 35/审计 38/404 分析 70/会话日志 55 等，共 400+ 份），markdown 渲染在线阅读（含表格）
- 知识库：KB 55M 目录浏览 + 全文搜索（文件名优先 + 内容命中带上下文，400 文件扫描上限）
- 认证 fail-closed（无密码配置时全拒）；路径穿越防护（400）；reader HTML 注入面 = 本地可信文档 + esc 渲染
- 新依赖：markdown==3.10.3（服务器 venv via uv；uv venv 无 pip，用 uv pip install --python）

**验证**：overview/reports(10 类)/kb tree+search/read(月报 149K html 含表格)/tasks 增改删/穿越防护 400/外部 200 全部真实通过。
