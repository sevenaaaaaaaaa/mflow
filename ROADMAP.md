# MFlow 产品化 ROADMAP

> 目标：让任何公司 clone 下来 30 分钟跑通第一个内容工作流，并随使用深度逐步扩展。
> 状态标记：✅ 已交付 · 🔄 进行中 · 📋 规划

## Phase 0 · 产品化基座（2026-09-15 ✅）

- ✅ 首次引导向导：`首次引导 · Setup` 页，6 项检查清单（密码/LLM/知识库/日历/Demo/第一个工作流），每项一键跳转配置
- ✅ Demo 数据包：`docs/demo-reports/` 示例月报（数值条可视化）+ 示例舆情日报 + 一键注入演示任务
- ✅ Demo 生成回退：未配置 LLM Key 时自动出演示稿，完整跑通 生成→质检→状态机 闭环
- ✅ 部署文档三路径：`docs/deploy-guide.md`（本地 5 分钟 / systemd 生产 / Docker）
- ✅ 快速上手：`docs/quickstart.md`（首次使用 8 步）
- ✅ 模块扩展指南：`docs/modules.md`（四个注册点 / 数据源接入 / CMS 适配器 / 自我迭代）

## Phase 1 · 协作与日历（2026-09-15 ✅）

- ✅ Trello 式看板：卡片拖拽跨列、点击编辑（描述/负责人/截止日）、操作者署名（localStorage 轻协作）
- ✅ 看板 ↔ 内容日历打通：日历文章一键「加入看板」，卡片带 🔗 关联可跳回阅读
- ✅ 版本体系：`VERSION` + 侧栏版本号 + `/api/version`

## Phase 2 · 深度能力（2026-09-15 ✅ 全部交付）

- ✅ CJK 分词修复：post-write-check 词当量 = ASCII 词 + CJK 字符/2（perl unicode），680 汉字不再被记为 21 词，16/16 回归绿
- ✅ 质检可视化：hook 输出 ✓/✗/WARN 分项着色渲染（Loop 日志/质量钩子页复用 fmtHook）
- ✅ 媒体效果检验：分发页「效果归因」——已发布外链 canonical × GSC Top20 页面点击/曝光关联表（数据源可扩全量）
- ✅ CMS 适配器接口：`1-4 Dev/scripts/publish_adapters/`（接口约定 README + webhook 完整实现 + wordpress REST 骨架 + sanity 参考说明 + 统一 CLI）
- ✅ 报告可视化 R1 MVP：阅读器自动解析报告首个数值表 → 顶部指标卡仪表视图（月报即生效）
- ✅ Loop 并发与队列：移除单跑限制 → queued 状态 + 调度线程（并发上限 2）+ 每 Loop token 记账

## Phase 2.5 · 平台化多项目（2026-09-15 ✅ 计划外提前交付）

- ✅ 去 Lovart 化：登录页/后台文案/生成提示词全部通用化（"提及你的产品/工具"），内部 skill ID 保留
- ✅ 多项目架构：项目 = `run/projects/{id}/` 独立数据命名空间（管线状态/事件/看板/Loop/生成物）
- ✅ 项目 API：新建（slug 化 + meta.json）/ 切换（session 上下文）/ 删除（admin → _trash 回收站）
- ✅ 前端：侧栏项目切换器 + ＋新建项目；总览问候显示登录名
- ✅ 隔离 e2e：main 继承存量（7 任务/3 管线条目）→ 新建项目 B 全空 → B 加任务 → 切回 main 不串 → 删 B 进回收站
- ✅ 共享平台能力：用户/LLM 配置/模板/知识中台/报告中心/调度
- 📋 项目级调度与知识源隔离（每个项目独立知识源挂载）→ Phase 4

## Phase 5 · 自动化执行（2026-09-16 ✅ 全部交付）

- ✅ P5.1 自动排程执行器：全局线程每 5 分钟扫描——项目配额未满且选题队列有货时，自动从队首取题创建 Loop（demo/真实 LLM 通用，token 记账照常），执行日志随项目落 run/projects/{id}/schedule.log
- ✅ P5.2 选题队列：每项目 topics.json + 工作台设置页管理（批量粘贴/逐条删除/计数）
- ✅ 排程状态 API：/api/schedule/status（今日已建/配额/运行中/排队/队列长度/日志尾）
- ✅ P5.3 排程报表：/api/schedule/all 跨项目一行一项目（配额进度条/运行/排队/选题队列/日志尾）进「调度与日志」页
- ✅ P5.4 Loop 终态通知：done/blocked/failed 推飞书（stopped 不打扰）；设置页 admin 配 webhook + 测试；run/notify.json 600
- ✅ P5.5 项目独立 LLM：meta.llm{provider/base/key/model} 覆盖全局（优先级 项目>全局>demo），生成与 Loop 同走；GET 全程打码，空 Key 即清除回退
- ✅ P5.6 插件市场：plugins/marketplace.json 内置可装包（rss-source/webhook-publisher）+ 粘贴安装（自动 plugin_check，失败进 _trash）+ 卸载

## Phase 4 · 放大项（2026-09-15/16 ✅ 首批交付）

- ✅ P4.1 多租户账号隔离：auth.json 用户绑定 projects（admin 全可见）；/api/projects 按用户过滤、switch 越权回落；create 自动绑定创建者；main 永远可见；设置页 admin 逐账号分配 UI；e2e 验证（受限用户只见绑定项目 + 无串扰）
- ✅ P4.2a 项目级知识源：meta.kb_extra（label/dir/glob，路径安全校验）→ 知识中台合并渲染 [项目] 源 + 域内搜索；知识中台页挂载表单
- ✅ P4.2b 项目调度配置：meta.schedule（daily_quota/auto_loop）存储 + 设置页当前项目配置卡；**自动排程执行器排 Phase 5**（当前保存意图）
- ✅ P4.3 报告可视化 R2（表格 → Chart.js 图表切换）/ R4（打印/PDF 样式与按钮）/ R3（双报告并排对比）/ R5（总览本周速览卡：新增报告/吞吐/token）
- ✅ P4.4 插件规范：docs/plugins.md（三类插件 + manifest + 权限模型）+ plugins/plugin_check.py 六项校验器（示例插件 PASS）+ sample-source 示例

## Phase 3 · 生态（2026-09-15 ✅ 全部交付）

**P3.1 账号体系 · 角色 · 审批流（2026-09-15 ✅）**
- ✅ 多用户 bcrypt 登录（auth.json，OpenFlow 13 用户迁移）+ 角色分级落地：admin 全部 / marketing·sales·operator 创作与质检 / viewer 只读拦截；admin-only 白名单（LLM 配置/账号管理/审批/管线触发/删除）
- ✅ 发布审批流：dispatch 单 admin「批准发布」按钮 + approved_by/approved_at + run/approvals.log 审计
- ✅ 账号管理：admin 在设置页查看 13 账号与角色、重置任意账号密码（审计留痕）；root CLI `deploy/reset-account.sh` 免登录重置
- ✅ 二级目录入口 nownexts.com/mflow/ + 当前用户显示 + 卡片负责人默认当前用户
- ✅ 归属人过滤（"我的任务"视图）（2026-09-16 Phase 5 收官交付）

**P3.2 模板市场雏形（2026-09-15 ✅）**
- ✅ 模板包格式 v1：{id/name/version + workflow 定义 + prompt(audience/tone/structure/anti_slop_extra) + kb_sources_suggestion} 单 JSON，`templates/` 随仓库分发
- ✅ 内置 3 个行业模板：电商内容（广告法禁例）/ SaaS 增长（ROI 承诺禁例）/ 本地服务（NAP 一致性）
- ✅ 生成联动：创作中心选模板 → gen_prompt 应用行业 audience/tone/结构/附加禁例；Loop 记录 template_id
- ✅ 市场页：模板卡（版本/作者/描述/工作流链）+ 查看 JSON + 导出下载 + 粘贴/文件导入（校验三要素）+ 自定义模板删除（内置保护）
- ✅ e2e：列表 3 → 导入 4 → 删除回 3；带模板生成 hook PASS

**P3.3 报告可视化 R1 完整版（2026-09-15 ✅）**
- ✅ 通用结构解析器：/api/report/structure 把任意 md 报告解析为 H2 分节 + 段落 + 表格（月报 20 节 29 表 / 舆情日报 15 节 12 表验证）
- ✅ 「报告仪表」独立页：分类+报告选择 → 仪表渲染（首个数值表升格为指标卡组，全部表格带比例条），一键切换原文阅读

**P3.4 自我迭代仪表（2026-09-15 ✅）**
- ✅ QA 历史埋点：所有质检执行（手动钩子/生成/Loop）记录 run/qa-history.jsonl
- ✅ 「自我迭代仪表」页三曲线：BLOCK 率（近 14 日）/ Token 消耗 / 吞吐（30 日全项目状态机推进）+ 质检明细
- ✅ 月度自动回顾：一键生成 `MFlow-自我迭代回顾-YYYY-MM.md` 写入报告中心（含质量/Token/吞吐三段 + 洞察框架）

- ✅ 域名二级目录入口：`nownexts.com/mflow/`（Apache 双 vhost ProxyPass，见 session log v3.5）
- ✅ 子域名方案备用：`deploy/setup-domain.sh` + `docs/domain-setup.md`（DNS → 反代 → HTTPS 三步）
- ✅ Phase 5 收官（2026-09-16）：归属人过滤（"我的任务"）· 排程报表进调度页 · Loop 终态飞书通知（run/notify.json，admin 配置）· 项目独立 LLM Key（meta.llm，清空即回退全局）· 插件市场（marketplace.json + 安装/卸载/plugin_check 六项）· 钩子 PATH 修复（LOVART_PYTHON → 项目 venv 自动探测，smoketest 免 source 16/16）
- 📋 插件规范：第三方数据源/发布渠道按 §modules 协议贡献，TOOLS-REGISTRY 自动收录

## Phase 6 · GEO Content Loop（2026-09-16 ✅ 首批全链路）

- ✅ P6.2 GEO 门禁：`geo-check.sh`（可分块结构/统计密度/问答式标题/来源标注/墙式段落，--strict 升 BLOCK）接入 Loop 质检级联与单次生成；gen_prompt 注入 GEO_RULES（问答式 H2/数据点密度/自包含短段/来源链接）
- ✅ P6.1 引用感知：设置页配置品牌/竞品/目标查询 → 逐条走官方 OpenAI 兼容 API 问 AI 引擎，检测品牌/竞品提及与来源 URL → citations.jsonl；demo 模式 fail-clean 拒绝（演示稿不代表真实 AI 行为）
- ✅ P6.3 归因闭环：/api/impact 并入 geo（查询级提及率 + 竞品份额）
- ✅ P6.4 缺口自动选题：0 引用查询一键「→ 选题队列」→ 自动排程消化
- ✅ P6.5 改稿 Loop：0 引用查询一键「→ 改稿 Loop」（refresh-slug，brief 内置 GEO 重写指令，走既有 Loop 引擎）
- ✅ P6.6 GEO 仪表：设置页 GEO 卡——品牌提及率/竞品份额/近 14 日趋势迷你柱图/缺口清单

### P6 二批（2026-09-16 ✅）
- ✅ P6.7 每日自动探测：geo_scheduler 后台线程（每小时检查，09:30 后、当日无成功记录即探测）；设置页 GEO 卡「每日自动探测」开关；失败/记账行不阻塞当日重试
- ✅ P6.8 Perplexity sonar 真引用：providers 新增 perplexity（api.perplexity.ai）；GEO 卡选引擎 + 模型名（sonar/sonar-pro）；响应官方 citations 直接采信；llm_chat_full() 返回 (content, meta) 不走 demo 回退
- ✅ P6.9 citations × 已发布 URL 精确归因：canonical 路径归一化匹配（协议/子域/query/尾斜杠容错）→ GEO 卡「被 AI 引用的页面」（slug/平台/被引次数/命中查询）
- ✅ P6.10 GEO 曲线进自我迭代仪表：第四条曲线 = 品牌提及率 14 日（实心柱=被提及日）+ 缺口计数徽标

### P7 批次（2026-09-16 ✅）
- ✅ P7-B1 内容衰减监测：decay_analysis（发布≥30 天 × GSC Top20 无记录 × 无 AI 引用）→ 分发页衰减卡 + 一键改稿 Loop
- ✅ P7-B3 多引擎交叉探测：engines[] 任意 provider 直连（缺 Key 引擎级报错）+ per_engine 分拆 + 引擎分歧检测徽标
- ✅ P7-C 门禁固化：session-init GATE 5 console syntax（node --check JS × ast py × bash -n hooks）——4 处语法回归类事故自此有硬门禁；门禁自身 python 解析/glob 三 bug 顺修，服务器 5/5 PASS
- 📋 P7-B2 竞品引用源反向工程 · P7-B5 发布后自动复测 · P7-B6 GEO 综合分 · 衰减自动改稿 opt-in

### P7 二批（2026-09-16 ✅）
- ✅ P7-B2 竞品引用源反向工程：competitor_urls 按域聚合 + 一键对标选题
- ✅ P7-B5 发布后复测窗口：≤7 天新页 × 引用记录 → 复测状态卡（与每日自动探测联动）
- ✅ P7-B6 GEO 综合分：提及率40 + 缺口覆盖30 + 相对份额20 + 结构健康10 → 0-100（无数据不造假分）
- ✅ 衰减自动改稿 opt-in：auto_refresh 开关，每日 ≤2 篇 refresh Loop 自动排程（去重 + 审计）

## 原则

1. 文件即状态：不引入数据库也能跑，规模化时才换 PG（接口已预留）
2. 发布人工授权是不可协商的边界
3. 每个新能力必须让未配置的新用户 5 分钟内看到效果
4. 错误只犯一次：踩坑必须沉淀为 hook 检查项或 RULES 条款
