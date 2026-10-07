---
type: session-log
session_date: 2026-09-16
session_slug: phase4-first-batch
status: ready
---

# Session Log — Phase 4 首批（多租户 / 项目知识源 / R2-R5 / 插件规范）

## 交付（全部 e2e 验证）
1. **P4.1 多租户**：auth.json 用户绑定 projects；/api/projects 按用户过滤；switch 越权自动回落；创建项目自动绑定创建者；main 永远可见（修复：绑定非空时 main 被挤出的 bug）；设置页 admin 逐账号分配 UI。
2. **P4.2 项目级知识源与调度**：meta.kb_extra（路径安全校验）合并进知识中台（[项目] 前缀源 + 域内搜索 11 hits 验证）；meta.schedule 存储与设置页配置卡（自动排程执行器排 Phase 5）。
3. **P4.3 R2-R5**：表格→Chart.js 图表切换；打印/PDF 样式；双报告并排对比；总览本周速览卡（/api/digest：7 日新增报告/吞吐/token）。
4. **P4.4 插件规范**：docs/plugins.md（source/publisher/template 三类 + manifest + 权限模型）+ plugin_check.py 六项校验（sample-source PASS）。

## 踩坑
- user_projects 初版把默认 main 挤出可见集（绑定非空时 or 默认逻辑失效）——e2e 逮住，修为 main 恒并入。
- 大 patch heredoc 中文/引号转义反复出问题——改为 Write 脚本文件再执行，转义地狱终结。

## Phase 4 剩余（Phase 5）：自动排程执行器、项目级独立调度、报告 R3 diff 高亮深化、插件市场分发、正式多租户账号管理 UI。

## v4.1 追加——Phase 5 自动排程执行器（首批）

- 执行器：全局线程每 5 分钟扫描 run/projects/*/meta.json——auto_loop 开且配额未满且队列有选题 → 从队首取题建 Loop（upsert 管线条目 + queued 入队，由既有 queue worker 执行，token 记账照常）；schedule.log 项目内审计
- 选题队列：topics.json + 工作台设置页管理（批量粘贴/删除/计数）
- /api/schedule/status：配额/今日已建/运行中/排队/队列长/日志尾
- 路由修复：P5 patch 曾把两个 GET 路由错插进 do_POST——404 已搬回 do_GET
- e2e：排程器按配额建 Loop（日志 1/3）+ 探针 queued loop 8 秒内被 worker 执行全闭环（demo 质检 PASS → S4-qa）→ 测试残留全清（auto_loop 关/队列空/日志清/探针草稿删/临时号删）

**Phase 5 剩余**：排程报表进仪表、Loop 完成后自动通知、每项目独立 LLM Key。
